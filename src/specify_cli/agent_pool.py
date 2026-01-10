"""
Distributed Agent Pool for parallel Claude API execution.

This module provides a pool of async Anthropic clients that can execute
multiple agent tasks concurrently, respecting rate limits and handling
retries with exponential backoff.

Architecture:
    ┌─────────────────────────────────────────────────────┐
    │            DistributedAgentPool                      │
    │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌─────┐ │
    │  │ Client 1  │ │ Client 2  │ │ Client 3  │ │ ... │ │
    │  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └──┬──┘ │
    │        └─────────────┴─────────────┴──────────┘    │
    │                      │                              │
    │         ┌────────────┴────────────┐                │
    │         │  Semaphore (pool_size)  │                │
    │         └─────────────────────────┘                │
    └─────────────────────────────────────────────────────┘

Usage:
    pool = DistributedAgentPool(pool_size=4)
    tasks = [AgentTask(name="task1", prompt="..."), ...]
    results = await pool.execute_wave(tasks)
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

import anthropic
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


class ModelTier(str, Enum):
    """Model tiers for agent execution."""
    OPUS = "claude-opus-4-5-20251101"
    SONNET = "claude-sonnet-4-5-20250929"
    HAIKU = "claude-3-5-haiku-20241022"


# Pricing per 1M tokens (USD) - as of January 2025
MODEL_RATES: Dict[str, Dict[str, float]] = {
    "opus": {"input": 15.00, "output": 75.00},
    "sonnet": {"input": 3.00, "output": 15.00},
    "haiku": {"input": 0.25, "output": 1.25},
}


def model_id_to_tier(model_id: str) -> str:
    """Convert full model ID to tier name (opus/sonnet/haiku)."""
    if "opus" in model_id.lower():
        return "opus"
    elif "sonnet" in model_id.lower():
        return "sonnet"
    elif "haiku" in model_id.lower():
        return "haiku"
    return "sonnet"  # default


def calculate_cost(model_tier: str, tokens_in: int, tokens_out: int) -> float:
    """Calculate cost in USD for given token usage."""
    rates = MODEL_RATES.get(model_tier, MODEL_RATES["sonnet"])
    return (tokens_in * rates["input"] + tokens_out * rates["output"]) / 1_000_000


@dataclass
class AgentTask:
    """
    Represents a single agent task to be executed.

    Attributes:
        name: Unique identifier for the task (typically the agent role)
        prompt: The prompt to send to the Claude API
        model: Claude model to use (defaults to Sonnet for balance of speed/quality)
        depends_on: List of task names that must complete before this task
        priority: Execution priority (lower = higher priority, default 5)
        role_group: Grouping for resource allocation (e.g., "ANALYSIS", "GENERATION")
        system_prompt: Optional system prompt for the agent
        max_tokens: Maximum tokens for the response
        temperature: Sampling temperature (0.0-1.0)
        metadata: Additional metadata for tracking/logging
    """
    name: str
    prompt: str
    model: str = ModelTier.SONNET.value
    depends_on: List[str] = field(default_factory=list)
    priority: int = 5
    role_group: str = "DEFAULT"
    system_prompt: Optional[str] = None
    max_tokens: int = 8192
    temperature: float = 0.7
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """
    Result of executing an agent task.

    Attributes:
        name: Task name that produced this result
        output: The text output from the agent
        success: Whether the task completed successfully
        duration_ms: Execution time in milliseconds
        model_used: Actual model that was used
        model_tier: Model tier (opus/sonnet/haiku)
        tokens_in: Input tokens consumed
        tokens_out: Output tokens generated
        cost: Cost in USD for this request
        error: Error message if success is False
        stop_reason: Reason the model stopped generating
    """
    name: str
    output: str
    success: bool
    duration_ms: int
    model_used: str
    model_tier: str
    tokens_in: int
    tokens_out: int
    cost: float
    error: Optional[str] = None
    stop_reason: Optional[str] = None


@dataclass
class PoolConfig:
    """
    Configuration for the agent pool.

    Attributes:
        pool_size: Number of concurrent clients/tasks
        default_model: Default model for tasks without explicit model
        requests_per_minute: Rate limit for API requests
        tokens_per_minute: Rate limit for tokens
        max_retries: Maximum retry attempts for failed requests
        backoff_base: Base wait time for exponential backoff (seconds)
        backoff_max: Maximum wait time for backoff (seconds)
        batch_mode: Enable cross-wave batch aggregation for latency reduction
        max_batch_size: Maximum tasks per aggregated batch
        batch_timeout_ms: Time to wait for more requests before executing batch
    """
    pool_size: int = 8
    default_model: str = ModelTier.SONNET.value
    requests_per_minute: int = 50
    tokens_per_minute: int = 100000
    max_retries: int = 3
    backoff_base: float = 1.0
    backoff_max: float = 10.0
    # Batch aggregation settings (Strategy 1.3)
    batch_mode: bool = True
    max_batch_size: int = 10
    batch_timeout_ms: int = 100


class DistributedAgentPool:
    """
    Pool of async Anthropic clients for parallel agent execution.

    This class manages a pool of clients that can execute multiple agent
    tasks concurrently while respecting rate limits and handling failures
    with exponential backoff retry logic.

    Example:
        ```python
        pool = DistributedAgentPool(pool_size=4)
        tasks = [
            AgentTask(name="analyzer", prompt="Analyze this code..."),
            AgentTask(name="generator", prompt="Generate tests...", depends_on=["analyzer"]),
        ]
        results = await pool.execute_wave(tasks)
        print(f"Completed {len(results)} tasks")
        ```
    """

    def __init__(
        self,
        pool_size: int = 4,
        config: Optional[PoolConfig] = None
    ):
        """
        Initialize the agent pool.

        Args:
            pool_size: Number of concurrent execution slots
            config: Optional configuration override
        """
        self.config = config or PoolConfig(pool_size=pool_size)
        self.pool_size = self.config.pool_size

        # Create pool of async clients
        # Each client maintains its own connection pool
        self.clients: List[anthropic.AsyncAnthropic] = [
            anthropic.AsyncAnthropic() for _ in range(self.pool_size)
        ]

        # Semaphore limits concurrent executions
        self.semaphore = asyncio.Semaphore(self.pool_size)

        # Track results and pending tasks
        self.results: Dict[str, AgentResult] = {}
        self.pending: Dict[str, AgentTask] = {}

        # Statistics
        self.total_requests = 0
        self.total_tokens_in = 0
        self.total_tokens_out = 0
        self.total_duration_ms = 0

        # Per-model statistics
        self.by_model: Dict[str, Dict[str, Any]] = {
            "opus": {"tokens_in": 0, "tokens_out": 0, "requests": 0, "cost": 0.0},
            "sonnet": {"tokens_in": 0, "tokens_out": 0, "requests": 0, "cost": 0.0},
            "haiku": {"tokens_in": 0, "tokens_out": 0, "requests": 0, "cost": 0.0},
        }

    async def execute_wave(
        self,
        tasks: List[AgentTask]
    ) -> Dict[str, AgentResult]:
        """
        Execute multiple agent tasks in parallel within concurrency limit.

        Args:
            tasks: List of tasks to execute (should have no dependencies on each other)

        Returns:
            Dictionary mapping task names to their results
        """
        async def run_task(task: AgentTask, client_idx: int) -> AgentResult:
            async with self.semaphore:
                client = self.clients[client_idx % self.pool_size]
                return await self._execute_single(task, client)

        # Launch all tasks with round-robin client assignment
        coroutines = [
            run_task(task, i) for i, task in enumerate(tasks)
        ]

        # Gather results, handling exceptions
        results_list = await asyncio.gather(*coroutines, return_exceptions=True)

        # Process results
        wave_results: Dict[str, AgentResult] = {}
        for task, result in zip(tasks, results_list):
            if isinstance(result, Exception):
                # Convert exception to failed result
                wave_results[task.name] = AgentResult(
                    name=task.name,
                    output="",
                    success=False,
                    duration_ms=0,
                    model_used=task.model,
                    model_tier=model_id_to_tier(task.model),
                    tokens_in=0,
                    tokens_out=0,
                    cost=0.0,
                    error=str(result),
                )
            else:
                wave_results[task.name] = result

            # Update global results
            self.results[task.name] = wave_results[task.name]

        return wave_results

    async def _execute_single(
        self,
        task: AgentTask,
        client: anthropic.AsyncAnthropic
    ) -> AgentResult:
        """
        Execute a single agent task with retry logic.

        Uses tenacity for exponential backoff on transient failures.
        """
        start_time = time.monotonic()

        @retry(
            stop=stop_after_attempt(self.config.max_retries),
            wait=wait_exponential(
                multiplier=self.config.backoff_base,
                max=self.config.backoff_max
            ),
            retry=retry_if_exception_type((
                anthropic.RateLimitError,
                anthropic.APIConnectionError,
                anthropic.InternalServerError,
            )),
            reraise=True,
        )
        async def make_request() -> anthropic.types.Message:
            messages = [{"role": "user", "content": task.prompt}]

            kwargs: Dict[str, Any] = {
                "model": task.model,
                "max_tokens": task.max_tokens,
                "messages": messages,
            }

            if task.system_prompt:
                kwargs["system"] = task.system_prompt

            if task.temperature is not None:
                kwargs["temperature"] = task.temperature

            return await client.messages.create(**kwargs)

        try:
            response = await make_request()
            duration_ms = int((time.monotonic() - start_time) * 1000)

            # Extract text content
            output = ""
            for block in response.content:
                if hasattr(block, "text"):
                    output += block.text

            # Update statistics
            self.total_requests += 1
            self.total_tokens_in += response.usage.input_tokens
            self.total_tokens_out += response.usage.output_tokens
            self.total_duration_ms += duration_ms

            # Update per-model statistics
            tier = model_id_to_tier(task.model)
            cost = calculate_cost(tier, response.usage.input_tokens, response.usage.output_tokens)
            self.by_model[tier]["tokens_in"] += response.usage.input_tokens
            self.by_model[tier]["tokens_out"] += response.usage.output_tokens
            self.by_model[tier]["requests"] += 1
            self.by_model[tier]["cost"] += cost

            return AgentResult(
                name=task.name,
                output=output,
                success=True,
                duration_ms=duration_ms,
                model_used=task.model,
                model_tier=tier,
                tokens_in=response.usage.input_tokens,
                tokens_out=response.usage.output_tokens,
                cost=cost,
                stop_reason=response.stop_reason,
            )

        except Exception as e:
            duration_ms = int((time.monotonic() - start_time) * 1000)
            return AgentResult(
                name=task.name,
                output="",
                success=False,
                duration_ms=duration_ms,
                model_used=task.model,
                model_tier=model_id_to_tier(task.model),
                tokens_in=0,
                tokens_out=0,
                cost=0.0,
                error=str(e),
            )

    def get_statistics(self) -> Dict[str, Any]:
        """Return pool execution statistics with per-model breakdown."""
        total_cost = sum(m["cost"] for m in self.by_model.values())
        return {
            "total_requests": self.total_requests,
            "total_tokens_in": self.total_tokens_in,
            "total_tokens_out": self.total_tokens_out,
            "total_tokens": self.total_tokens_in + self.total_tokens_out,
            "total_cost": total_cost,
            "total_duration_ms": self.total_duration_ms,
            "avg_duration_ms": (
                self.total_duration_ms / self.total_requests
                if self.total_requests > 0 else 0
            ),
            "pool_size": self.pool_size,
            "completed_tasks": len(self.results),
            "by_model": {
                tier: {
                    "requests": stats["requests"],
                    "tokens_in": stats["tokens_in"],
                    "tokens_out": stats["tokens_out"],
                    "tokens_total": stats["tokens_in"] + stats["tokens_out"],
                    "cost": stats["cost"],
                }
                for tier, stats in self.by_model.items()
                if stats["requests"] > 0  # Only include models that were used
            },
        }

    async def close(self) -> None:
        """Close all clients and release resources."""
        for client in self.clients:
            await client.close()
        self.clients.clear()

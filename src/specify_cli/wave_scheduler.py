"""
Wave Scheduler for DAG-based agent execution.

This module provides dependency-aware scheduling of agent tasks,
organizing them into waves that can be executed in parallel while
respecting inter-task dependencies.

Architecture:
    ┌─────────────────────────────────────────────────────────────┐
    │                    Wave Scheduler                            │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │   Tasks with Dependencies (DAG)                             │
    │   ┌────┐     ┌────┐     ┌────┐                              │
    │   │ A  │────▶│ C  │────▶│ E  │                              │
    │   └────┘     └────┘     └────┘                              │
    │   ┌────┐        │                                           │
    │   │ B  │────────┘                                           │
    │   └────┘                                                    │
    │   ┌────┐                                                    │
    │   │ D  │─────────────────────▶(no deps)                     │
    │   └────┘                                                    │
    │                                                             │
    │   Waves:                                                    │
    │   ┌─────────────────────────────────────────────────────┐   │
    │   │ Wave 1: [A, B, D]  (no dependencies)                │   │
    │   │ Wave 2: [C]        (depends on A, B)                │   │
    │   │ Wave 3: [E]        (depends on C)                   │   │
    │   └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │   Wave Overlap (80% threshold):                             │
    │   ───[Wave 1: A,B,D]────┐                                   │
    │              80%─────────[Wave 2: C]─────┐                  │
    │                                 80%───────[Wave 3: E]───    │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

Usage:
    pool = DistributedAgentPool(pool_size=4)
    scheduler = WaveScheduler(pool)
    results = await scheduler.execute_all(tasks)
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Callable, Any
from enum import Enum

from .agent_pool import AgentTask, AgentResult, DistributedAgentPool


class ExecutionStrategy(str, Enum):
    """Strategy for wave execution."""
    SEQUENTIAL = "sequential"    # Execute waves one after another
    OVERLAPPED = "overlapped"    # Start next wave at threshold
    AGGRESSIVE = "aggressive"    # Start next wave ASAP when deps satisfied
    BATCHED = "batched"          # Cross-wave batch aggregation (Strategy 1.3)


@dataclass
class WaveConfig:
    """
    Configuration for wave execution.

    Attributes:
        max_parallel: Maximum tasks to run in parallel per wave
        overlap_enabled: Whether to overlap wave execution
        overlap_threshold: Percentage of wave completion before starting next (0.0-1.0)
        strategy: Execution strategy for waves
        fail_fast: Stop all execution on first failure
        timeout_per_task_ms: Optional timeout per individual task
        timeout_total_ms: Optional timeout for entire execution
        batch_mode: Enable cross-wave batch aggregation (Strategy 1.3)
        max_batch_size: Maximum tasks per aggregated batch
        cross_wave_batching: Whether to batch tasks across wave boundaries
    """
    max_parallel: int = 3
    overlap_enabled: bool = True
    overlap_threshold: float = 0.80
    strategy: ExecutionStrategy = ExecutionStrategy.OVERLAPPED
    fail_fast: bool = True
    timeout_per_task_ms: Optional[int] = None
    timeout_total_ms: Optional[int] = None
    # Batch aggregation settings (Strategy 1.3)
    batch_mode: bool = False
    max_batch_size: int = 10
    cross_wave_batching: bool = True


@dataclass
class Wave:
    """
    Represents a single execution wave.

    Attributes:
        index: Wave number (0-indexed)
        tasks: Tasks in this wave
        completed: Set of completed task names
        failed: Set of failed task names
        started: Whether wave execution has started
        finished: Whether wave execution has completed
    """
    index: int
    tasks: List[AgentTask]
    completed: Set[str] = field(default_factory=set)
    failed: Set[str] = field(default_factory=set)
    started: bool = False
    finished: bool = False

    @property
    def completion_ratio(self) -> float:
        """Return ratio of completed tasks (0.0-1.0)."""
        if not self.tasks:
            return 1.0
        return len(self.completed) / len(self.tasks)

    @property
    def is_threshold_met(self, threshold: float = 0.80) -> bool:
        """Check if wave has met completion threshold."""
        return self.completion_ratio >= threshold

    @property
    def all_succeeded(self) -> bool:
        """Check if all tasks in wave succeeded."""
        return len(self.completed) == len(self.tasks) and len(self.failed) == 0


@dataclass
class ExecutionReport:
    """
    Report of a complete execution run.

    Attributes:
        waves: List of waves executed
        results: All task results
        total_duration_ms: Total execution time
        success: Whether all tasks succeeded
        failed_tasks: List of task names that failed
    """
    waves: List[Wave]
    results: Dict[str, AgentResult]
    total_duration_ms: int
    success: bool
    failed_tasks: List[str] = field(default_factory=list)

    def summary(self) -> str:
        """Generate human-readable summary."""
        lines = [
            f"Execution {'succeeded' if self.success else 'FAILED'}",
            f"  Waves: {len(self.waves)}",
            f"  Tasks: {len(self.results)}",
            f"  Duration: {self.total_duration_ms}ms",
        ]
        if self.failed_tasks:
            lines.append(f"  Failed: {', '.join(self.failed_tasks)}")
        return "\n".join(lines)


class WaveScheduler:
    """
    DAG-based scheduler for agent task execution.

    Organizes tasks into waves based on their dependencies, then
    executes waves in sequence (with optional overlap) using
    the DistributedAgentPool for parallel execution within each wave.

    Example:
        ```python
        pool = DistributedAgentPool(pool_size=4)
        scheduler = WaveScheduler(pool)

        tasks = [
            AgentTask(name="analyze", prompt="..."),
            AgentTask(name="generate", prompt="...", depends_on=["analyze"]),
            AgentTask(name="review", prompt="...", depends_on=["generate"]),
        ]

        results = await scheduler.execute_all(tasks)
        print(results["review"].output)
        ```
    """

    def __init__(
        self,
        pool: DistributedAgentPool,
        config: Optional[WaveConfig] = None
    ):
        """
        Initialize the scheduler.

        Args:
            pool: Agent pool for execution
            config: Optional configuration override
        """
        self.pool = pool
        self.config = config or WaveConfig()
        self.completed: Dict[str, AgentResult] = {}
        self.waves: List[Wave] = []
        self._on_task_complete: Optional[Callable[[str, AgentResult], None]] = None
        self._on_wave_complete: Optional[Callable[[Wave], None]] = None

    def on_task_complete(
        self,
        callback: Callable[[str, AgentResult], None]
    ) -> "WaveScheduler":
        """Register callback for task completion. Returns self for chaining."""
        self._on_task_complete = callback
        return self

    def on_wave_complete(
        self,
        callback: Callable[[Wave], None]
    ) -> "WaveScheduler":
        """Register callback for wave completion. Returns self for chaining."""
        self._on_wave_complete = callback
        return self

    def build_waves(self, tasks: List[AgentTask]) -> List[Wave]:
        """
        Build execution waves from task dependency graph.

        Uses topological sorting to organize tasks into waves where
        all tasks in a wave can execute in parallel (no inter-dependencies).

        Args:
            tasks: List of tasks with dependencies

        Returns:
            List of Wave objects in execution order

        Raises:
            ValueError: If circular dependency detected
        """
        waves: List[Wave] = []
        remaining = {t.name: t for t in tasks}
        completed_names: Set[str] = set()
        wave_index = 0

        while remaining:
            # Find all tasks whose dependencies are satisfied
            ready: List[AgentTask] = []
            for task in remaining.values():
                deps = task.depends_on or []
                if all(dep in completed_names for dep in deps):
                    ready.append(task)

            if not ready:
                # No tasks can proceed - circular dependency
                remaining_names = list(remaining.keys())
                raise ValueError(
                    f"Circular dependency detected among: {remaining_names}"
                )

            # Sort by priority (lower = higher priority)
            ready.sort(key=lambda t: t.priority)

            # Limit to max_parallel per wave
            wave_tasks = ready[:self.config.max_parallel]

            # Create wave
            wave = Wave(index=wave_index, tasks=wave_tasks)
            waves.append(wave)

            # Update tracking
            for t in wave_tasks:
                del remaining[t.name]
                completed_names.add(t.name)

            wave_index += 1

        self.waves = waves
        return waves

    async def execute_all(
        self,
        tasks: List[AgentTask]
    ) -> Dict[str, AgentResult]:
        """
        Execute all tasks respecting dependencies and parallelism.

        Args:
            tasks: List of tasks to execute

        Returns:
            Dictionary mapping task names to results
        """
        import time
        start_time = time.monotonic()

        # Build waves from task graph
        waves = self.build_waves(tasks)

        if self.config.strategy == ExecutionStrategy.BATCHED:
            await self._execute_batched(waves)
        elif self.config.strategy == ExecutionStrategy.SEQUENTIAL:
            await self._execute_sequential(waves)
        elif self.config.strategy == ExecutionStrategy.OVERLAPPED:
            await self._execute_overlapped(waves)
        else:  # AGGRESSIVE
            await self._execute_aggressive(waves)

        total_duration = int((time.monotonic() - start_time) * 1000)

        # Check for failures
        failed_tasks = [
            name for name, result in self.completed.items()
            if not result.success
        ]

        return self.completed

    async def _execute_sequential(self, waves: List[Wave]) -> None:
        """Execute waves one after another (no overlap)."""
        for wave in waves:
            wave.started = True
            results = await self.pool.execute_wave(wave.tasks)

            for name, result in results.items():
                self.completed[name] = result
                if result.success:
                    wave.completed.add(name)
                else:
                    wave.failed.add(name)

                if self._on_task_complete:
                    self._on_task_complete(name, result)

            wave.finished = True

            if self._on_wave_complete:
                self._on_wave_complete(wave)

            # Check fail_fast
            if self.config.fail_fast and wave.failed:
                raise RuntimeError(
                    f"Wave {wave.index} failed: {wave.failed}"
                )

    async def _execute_overlapped(self, waves: List[Wave]) -> None:
        """
        Execute waves with overlap at threshold.

        Starts the next wave when current wave reaches completion threshold.
        """
        pending_waves: List[asyncio.Task] = []
        wave_events: Dict[int, asyncio.Event] = {}

        async def execute_wave_with_threshold(wave: Wave) -> None:
            wave.started = True

            # Wait for previous wave threshold if not first wave
            if wave.index > 0:
                prev_event = wave_events.get(wave.index - 1)
                if prev_event:
                    await prev_event.wait()

            # Create threshold event for this wave
            threshold_event = asyncio.Event()
            wave_events[wave.index] = threshold_event

            # Execute tasks
            results = await self.pool.execute_wave(wave.tasks)

            for name, result in results.items():
                self.completed[name] = result
                if result.success:
                    wave.completed.add(name)
                else:
                    wave.failed.add(name)

                if self._on_task_complete:
                    self._on_task_complete(name, result)

                # Check if threshold met
                if wave.completion_ratio >= self.config.overlap_threshold:
                    threshold_event.set()

            # Ensure threshold event is set even if we didn't hit it during execution
            threshold_event.set()
            wave.finished = True

            if self._on_wave_complete:
                self._on_wave_complete(wave)

        # Start all waves (they'll wait for their predecessors)
        for wave in waves:
            task = asyncio.create_task(execute_wave_with_threshold(wave))
            pending_waves.append(task)

        # Wait for all waves
        await asyncio.gather(*pending_waves)

        # Check for failures
        if self.config.fail_fast:
            for wave in waves:
                if wave.failed:
                    raise RuntimeError(
                        f"Wave {wave.index} failed: {wave.failed}"
                    )

    async def _execute_aggressive(self, waves: List[Wave]) -> None:
        """
        Execute tasks as soon as their dependencies are satisfied.

        Most parallel but also most complex - individual tasks start
        immediately when their deps complete, regardless of wave structure.
        """
        # For now, fall back to overlapped with lower threshold
        original_threshold = self.config.overlap_threshold
        self.config.overlap_threshold = 0.0  # Start next wave immediately
        try:
            await self._execute_overlapped(waves)
        finally:
            self.config.overlap_threshold = original_threshold

    async def _execute_batched(self, waves: List[Wave]) -> None:
        """
        Execute using cross-wave batch aggregation (Strategy 1.3).

        Groups independent tasks from multiple waves into larger batches,
        minimizing the number of sequential wave boundaries and reducing
        overall API round-trip latency by 50-70%.

        Example:
            Original waves: [A,B,C] → [D,E] → [F]  (3 boundaries)
            After batching: [A,B,C,E,F] → [D]      (2 boundaries, if D depends on A)
        """
        from .batch_aggregator import BatchAggregator, BatchConfig

        # Create aggregator with current config
        batch_config = BatchConfig(
            enabled=self.config.batch_mode or self.config.strategy == ExecutionStrategy.BATCHED,
            max_batch_size=self.config.max_batch_size,
            cross_wave_batching=self.config.cross_wave_batching,
        )
        aggregator = BatchAggregator(batch_config)

        # Aggregate waves into optimized batches
        batches = aggregator.aggregate(waves)

        # Build wave index to Wave mapping for status updates
        wave_map = {w.index: w for w in waves}

        # Execute each batch
        for batch in batches:
            # Execute all tasks in batch as one parallel burst
            results = await self.pool.execute_wave(batch.tasks)

            # Update tracking and wave status
            for name, result in results.items():
                self.completed[name] = result

                # Find which wave this task belonged to and update its status
                for wave_idx in batch.wave_indices:
                    wave = wave_map.get(wave_idx)
                    if wave:
                        # Check if this task is in this wave
                        if any(t.name == name for t in wave.tasks):
                            wave.started = True
                            if result.success:
                                wave.completed.add(name)
                            else:
                                wave.failed.add(name)

                            # Check if wave is complete
                            if len(wave.completed) + len(wave.failed) == len(wave.tasks):
                                wave.finished = True
                                if self._on_wave_complete:
                                    self._on_wave_complete(wave)

                if self._on_task_complete:
                    self._on_task_complete(name, result)

            # Check fail_fast after each batch
            if self.config.fail_fast:
                failed_in_batch = [
                    name for name, result in results.items()
                    if not result.success
                ]
                if failed_in_batch:
                    raise RuntimeError(
                        f"Batch execution failed: {failed_in_batch}"
                    )

    def get_execution_plan(self, tasks: List[AgentTask]) -> str:
        """
        Generate a human-readable execution plan.

        Useful for dry-run mode to show what would be executed.
        """
        waves = self.build_waves(tasks)
        lines = [f"Execution Plan ({len(waves)} waves):"]
        lines.append("")

        for wave in waves:
            task_names = [t.name for t in wave.tasks]
            lines.append(f"  Wave {wave.index + 1}: {task_names}")

            for task in wave.tasks:
                deps = task.depends_on or []
                deps_str = f" (depends on: {deps})" if deps else ""
                lines.append(f"    - {task.name}{deps_str}")

        return "\n".join(lines)

    def generate_report(self) -> ExecutionReport:
        """Generate execution report after completion."""
        failed_tasks = [
            name for name, result in self.completed.items()
            if not result.success
        ]

        total_duration = sum(
            r.duration_ms for r in self.completed.values()
        )

        return ExecutionReport(
            waves=self.waves,
            results=self.completed,
            total_duration_ms=total_duration,
            success=len(failed_tasks) == 0,
            failed_tasks=failed_tasks,
        )

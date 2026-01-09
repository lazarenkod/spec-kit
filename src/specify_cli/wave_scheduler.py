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
from pathlib import Path
import re
import time

from .agent_pool import AgentTask, AgentResult, DistributedAgentPool


class QgTest003ViolationError(Exception):
    """
    Raised when QG-TEST-003 is violated: test passes when it should fail.

    In TDD, tests MUST fail before implementation (Red phase).
    If a test passes immediately, it indicates either:
    - Missing/weak assertions
    - Implementation already exists
    - Test is not testing the right thing

    Attributes:
        test_file: Path to the test file
        test_task: Name of the test task
        exit_code: Exit code from test runner
        stdout: Test runner stdout (truncated)
        stderr: Test runner stderr (truncated)
    """

    def __init__(
        self,
        test_file: str,
        test_task: str,
        exit_code: int,
        stdout: str = "",
        stderr: str = "",
    ):
        self.test_file = test_file
        self.test_task = test_task
        self.exit_code = exit_code
        self.stdout = stdout[:500]  # Truncate for readability
        self.stderr = stderr[:500]
        super().__init__(
            f"QG-TEST-003 VIOLATION: Test '{test_task}' passed (exit code {exit_code}) "
            f"when it should fail (TDD Red phase). File: {test_file}"
        )


# Optional async file I/O support
try:
    from .async_file_ops import load_artifacts_parallel, is_async_available
    ASYNC_FILE_OPS_AVAILABLE = True
except ImportError:
    ASYNC_FILE_OPS_AVAILABLE = False


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
        early_test_verification: Enable early test verification for TDD waves (experimental)
    """
    max_parallel: int = 6
    overlap_enabled: bool = True
    overlap_threshold: float = 0.60
    strategy: ExecutionStrategy = ExecutionStrategy.OVERLAPPED
    fail_fast: bool = True
    timeout_per_task_ms: Optional[int] = None
    timeout_total_ms: Optional[int] = None
    # Batch aggregation settings (Strategy 1.3)
    batch_mode: bool = True
    max_batch_size: int = 10
    cross_wave_batching: bool = True
    # Early test verification (Phase 2 optimization, experimental)
    early_test_verification: bool = False
    # TDD verification sub-config (see TddVerificationConfig for details)
    tdd_config: Optional["TddVerificationConfig"] = None


@dataclass
class TddVerificationConfig:
    """
    Configuration for TDD Red phase verification.

    Controls how test verification is performed to ensure TDD strictness
    while minimizing risk through circuit breakers and graceful degradation.

    Attributes:
        enabled: Whether TDD verification is enabled
        timeout_ms: Max time to wait for test execution (30s default)
        max_unlocks_per_wave: Circuit breaker - max early unlocks per wave
        verify_unit_tests_only: Only verify unit tests, not E2E (Phase 1)
        retry_delay_ms: Delay between retries when waiting for test file
        max_retries: Max retries when waiting for test file to appear
        fallback_to_normal_flow: Fall back to normal wave flow on any error
        block_on_qg_test_003: (Phase 2) Raise error if test PASSES when it should fail
    """
    enabled: bool = False
    timeout_ms: int = 30000  # 30 seconds per test
    max_unlocks_per_wave: int = 5  # Circuit breaker
    verify_unit_tests_only: bool = True  # Phase 1: only unit tests
    retry_delay_ms: int = 500
    max_retries: int = 3
    fallback_to_normal_flow: bool = True  # Graceful degradation
    block_on_qg_test_003: bool = False  # Phase 2: block on TDD violation


@dataclass
class TestVerificationResult:
    """
    Result of running actual test verification.

    Captures whether the test was executed and whether it failed (TDD Red).

    Attributes:
        test_ran: Whether the test was actually executed
        test_failed: True if test failed (TDD Red confirmed)
        exit_code: Process exit code from test runner
        stdout: Standard output from test runner
        stderr: Standard error from test runner
        duration_ms: How long the test took to run
        test_file: Path to the test file
        error: Error message if verification couldn't complete
    """
    test_ran: bool
    test_failed: bool  # True = TDD Red confirmed
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int
    test_file: Optional[str] = None
    error: Optional[str] = None


class TestFrameworkDetector:
    """
    Detect test framework and generate appropriate test commands.

    Supports Python (pytest), TypeScript/JavaScript (jest/vitest), and Go.
    """

    FRAMEWORKS: Dict[str, Dict[str, Any]] = {
        "python": {
            "detect": ["pyproject.toml", "pytest.ini", "setup.py", "setup.cfg", "tox.ini"],
            "command": ["pytest", "{test_file}", "-v", "--tb=short", "-x"],
            "fail_exit_codes": [1],  # 1 = test failures
        },
        "typescript": {
            "detect": ["package.json", "jest.config.js", "jest.config.ts", "vitest.config.ts"],
            "command": ["npm", "test", "--", "--testPathPattern={test_file}", "--passWithNoTests=false"],
            "fail_exit_codes": [1],
        },
        "go": {
            "detect": ["go.mod"],
            "command": ["go", "test", "-v", "-run", "{test_pattern}", "./..."],
            "fail_exit_codes": [1],
        },
    }

    @classmethod
    def detect(cls, project_root: Path) -> Optional[str]:
        """
        Detect project's test framework.

        Args:
            project_root: Root directory of the project

        Returns:
            Language identifier or None if not detected
        """
        for lang, config in cls.FRAMEWORKS.items():
            for detect_file in config["detect"]:
                if (project_root / detect_file).exists():
                    return lang
        return None

    @classmethod
    def get_test_command(cls, lang: str, test_file: str) -> List[str]:
        """
        Get test command for language.

        Args:
            lang: Language identifier from detect()
            test_file: Path to test file

        Returns:
            Command list ready for subprocess
        """
        config = cls.FRAMEWORKS.get(lang, {})
        cmd_template = config.get("command", [])
        # Extract test pattern from filename for Go
        test_pattern = Path(test_file).stem.replace("test_", "Test").replace("_test", "")
        return [
            c.format(test_file=test_file, test_pattern=test_pattern)
            for c in cmd_template
        ]

    @classmethod
    def get_fail_exit_codes(cls, lang: str) -> List[int]:
        """Get exit codes that indicate test failure."""
        config = cls.FRAMEWORKS.get(lang, {})
        return config.get("fail_exit_codes", [1])


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
        config: Optional[WaveConfig] = None,
        feature_dir: Optional[Path] = None
    ):
        """
        Initialize the scheduler.

        Args:
            pool: Agent pool for execution
            config: Optional configuration override
            feature_dir: Optional feature directory for async artifact loading
        """
        self.pool = pool
        self.config = config or WaveConfig()
        self.completed: Dict[str, AgentResult] = {}
        self.waves: List[Wave] = []
        self._on_task_complete: Optional[Callable[[str, AgentResult], None]] = None
        self._on_wave_complete: Optional[Callable[[Wave], None]] = None
        self.feature_dir = feature_dir
        # TDD verification state
        self._unlocks_this_wave: int = 0  # Circuit breaker counter
        self._tdd_config = self.config.tdd_config or TddVerificationConfig()

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

    async def load_artifacts_async(
        self,
        filenames: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Load feature artifacts in parallel using async I/O.

        This is significantly faster than loading files sequentially:
        - Sequential: 4 files × 200ms = 800ms
        - Parallel:   1 × 200ms = 200ms (4x speedup)

        Args:
            filenames: List of filenames to load. Defaults to standard artifacts.

        Returns:
            Dictionary mapping filename to content

        Raises:
            ValueError: If feature_dir was not provided during initialization
        """
        if not self.feature_dir:
            raise ValueError(
                "feature_dir must be set during initialization to use async loading"
            )

        if not ASYNC_FILE_OPS_AVAILABLE:
            # Fallback to synchronous loading
            return self._load_artifacts_sync(filenames)

        # Import here to avoid import errors if aiofiles not installed
        from .async_file_ops import load_artifacts_parallel

        return await load_artifacts_parallel(self.feature_dir, filenames)

    def _load_artifacts_sync(
        self,
        filenames: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Synchronous fallback for loading artifacts.

        Used when async_file_ops is not available or feature_dir not set.
        """
        if not self.feature_dir:
            return {}

        if filenames is None:
            filenames = [
                "spec.md",
                "plan.md",
                "tasks.md",
                "constitution.md",
                "concept.md",
                "baseline.md",
            ]

        artifacts = {}
        for filename in filenames:
            path = self.feature_dir / filename
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        artifacts[filename] = f.read()
                except Exception as e:
                    artifacts[filename] = f"# ERROR: {str(e)}"
            else:
                artifacts[filename] = ""

        return artifacts

    def _extract_test_file_path(
        self,
        test_task: AgentTask,
        test_result: AgentResult
    ) -> Optional[str]:
        """
        Extract test file path from task metadata or output.

        Priority:
        1. task.metadata["test_file"]
        2. Parse test_result.output for file creation patterns
        3. Infer from task name pattern

        Args:
            test_task: The test creation task
            test_result: Result from creating the test

        Returns:
            Path to test file or None if cannot determine
        """
        # Check metadata first
        if test_task.metadata.get("test_file"):
            return test_task.metadata["test_file"]

        # Parse output for file creation patterns
        patterns = [
            r"[Cc]reated?\s+([^\s]+test[^\s]*\.(py|ts|js|go|java|kt))",
            r"[Ww]riting\s+(?:to\s+)?([^\s]+test[^\s]*\.(py|ts|js|go|java|kt))",
            r"[Tt]est\s+file[:\s]+([^\s]+)",
            r"tests?/([^\s]+\.(py|ts|js))",
        ]

        for pattern in patterns:
            match = re.search(pattern, test_result.output)
            if match:
                return match.group(1)

        # Infer from task name (e.g., "test-scaffolder-auth" -> tests/test_auth.py)
        task_name = test_task.name.lower()
        if "test" in task_name:
            parts = task_name.replace("-", "_").split("_")
            for i, part in enumerate(parts):
                if part == "test" and i + 1 < len(parts):
                    component = parts[i + 1]
                    return f"tests/test_{component}.py"

        return None

    async def _verify_tdd_red(
        self,
        test_task: AgentTask,
        test_result: AgentResult,
    ) -> TestVerificationResult:
        """
        Actually run the test and verify it FAILS (TDD Red phase).

        Uses asyncio.create_subprocess_exec for safe subprocess execution
        (no shell injection risk as arguments are passed as list).

        Args:
            test_task: The test creation task
            test_result: Result from creating the test

        Returns:
            TestVerificationResult with actual test run outcome
        """
        start_time = time.monotonic()

        # Extract test file path
        test_file = self._extract_test_file_path(test_task, test_result)
        if not test_file:
            return TestVerificationResult(
                test_ran=False, test_failed=False, exit_code=-1,
                stdout="", stderr="Could not determine test file path",
                duration_ms=0, error="NO_TEST_FILE_PATH"
            )

        # Determine project root
        project_root = self.feature_dir.parent if self.feature_dir else Path.cwd()
        test_path = project_root / test_file

        # Wait for file with retries (handles filesystem latency)
        for _ in range(self._tdd_config.max_retries):
            if test_path.exists():
                break
            await asyncio.sleep(self._tdd_config.retry_delay_ms / 1000)
        else:
            return TestVerificationResult(
                test_ran=False, test_failed=False, exit_code=-1,
                stdout="",
                stderr=f"Test file not found: {test_path}",
                duration_ms=int((time.monotonic() - start_time) * 1000),
                test_file=str(test_file), error="FILE_NOT_FOUND"
            )

        # Detect test framework
        lang = TestFrameworkDetector.detect(project_root)
        if not lang:
            return TestVerificationResult(
                test_ran=False, test_failed=True,  # Assume valid (graceful)
                exit_code=0, stdout="Skipped - no test framework", stderr="",
                duration_ms=int((time.monotonic() - start_time) * 1000),
                test_file=str(test_file), error="NO_TEST_FRAMEWORK"
            )

        # Build test command (safe - passed as list, not shell string)
        cmd = TestFrameworkDetector.get_test_command(lang, str(test_file))

        try:
            # Safe subprocess execution - no shell injection
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(project_root)
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=self._tdd_config.timeout_ms / 1000
                )
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
                return TestVerificationResult(
                    test_ran=True, test_failed=False, exit_code=-1,
                    stdout="", stderr="Test execution timed out",
                    duration_ms=self._tdd_config.timeout_ms,
                    test_file=str(test_file), error="TIMEOUT"
                )

            duration_ms = int((time.monotonic() - start_time) * 1000)
            exit_code = proc.returncode or 0

            # TDD Red = test should FAIL (exit code in fail codes)
            fail_codes = TestFrameworkDetector.get_fail_exit_codes(lang)
            test_failed = exit_code in fail_codes

            return TestVerificationResult(
                test_ran=True, test_failed=test_failed, exit_code=exit_code,
                stdout=stdout.decode("utf-8", errors="replace")[:2000],
                stderr=stderr.decode("utf-8", errors="replace")[:2000],
                duration_ms=duration_ms, test_file=str(test_file)
            )

        except Exception as e:
            return TestVerificationResult(
                test_ran=False, test_failed=False, exit_code=-1,
                stdout="", stderr=str(e),
                duration_ms=int((time.monotonic() - start_time) * 1000),
                test_file=str(test_file), error=str(type(e).__name__)
            )

    async def _verify_test_and_unlock(
        self,
        test_task: AgentTask,
        test_result: AgentResult,
        impl_tasks: List[AgentTask]
    ) -> List[AgentTask]:
        """
        Verify test failure and unlock dependent implementation tasks.

        Enhanced with actual test execution to verify TDD Red phase.
        Uses circuit breaker to prevent runaway unlocks and graceful
        degradation on errors.

        Args:
            test_task: The completed test task
            test_result: Result of the test task execution
            impl_tasks: List of implementation tasks that may depend on this test

        Returns:
            List of implementation tasks that can now start early
        """
        if not self.config.early_test_verification:
            return []

        # Circuit breaker - prevent runaway unlocks
        if self._unlocks_this_wave >= self._tdd_config.max_unlocks_per_wave:
            return []

        # Only proceed if test task succeeded (test file created)
        if not test_result.success:
            return []

        # Skip E2E tests in Phase 1 if configured
        if self._tdd_config.verify_unit_tests_only:
            if "e2e" in test_task.name.lower() or "integration" in test_task.name.lower():
                return []

        # Actually run the test and verify it fails (TDD Red)
        verification = await self._verify_tdd_red(test_task, test_result)

        # Gate: test must actually run
        if not verification.test_ran:
            if self._tdd_config.fallback_to_normal_flow:
                return []  # Graceful degradation
            return []

        # Gate: QG-TEST-003 - test must FAIL (TDD Red)
        if not verification.test_failed:
            # Phase 2: optionally block on QG-TEST-003 violation
            if self._tdd_config.block_on_qg_test_003:
                raise QgTest003ViolationError(
                    test_file=verification.test_file or "unknown",
                    test_task=test_task.name,
                    exit_code=verification.exit_code,
                    stdout=verification.stdout,
                    stderr=verification.stderr,
                )
            return []  # Graceful degradation (Phase 1 default)

        # TDD Red verified! Now unlock implementation tasks
        unlocked_tasks = []

        for impl_task in impl_tasks:
            deps = impl_task.depends_on or []
            if test_task.name in deps:
                other_deps = [d for d in deps if d != test_task.name]
                if all(d in self.completed for d in other_deps):
                    unlocked_tasks.append(impl_task)
                    self._unlocks_this_wave += 1

        return unlocked_tasks

    def _is_test_task(self, task: AgentTask) -> bool:
        """
        Check if a task is a test generation task.

        Uses task metadata or naming convention to identify test tasks.

        Args:
            task: Task to check

        Returns:
            True if this is a test generation task
        """
        # Check metadata first
        if task.metadata.get("is_test_task"):
            return True

        # Check role group
        if task.role_group in ["TESTING", "TEST_SCAFFOLDING"]:
            return True

        # Check name patterns
        test_patterns = ["test-scaffolder", "e2e-test-scaffolder", "test_"]
        return any(pattern in task.name.lower() for pattern in test_patterns)

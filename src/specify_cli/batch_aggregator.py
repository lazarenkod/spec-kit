"""
Batch Aggregator for cross-wave task grouping.

This module provides intelligent batching of independent agent tasks
across wave boundaries to minimize API round-trip latency.

Architecture:
    ┌─────────────────────────────────────────────────────────────┐
    │                   BatchAggregator                            │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │   Input: Waves with dependencies                            │
    │   ┌────────────────────────────────────────────────────┐   │
    │   │ Wave 1: [A, B, C]    Wave 2: [D, E]   Wave 3: [F] │   │
    │   │         D depends on A                             │   │
    │   └────────────────────────────────────────────────────┘   │
    │                           │                                 │
    │                           ▼                                 │
    │   Dependency Analysis                                       │
    │   ┌────────────────────────────────────────────────────┐   │
    │   │ Independent: [A, B, C, E, F]  Chain: A → D         │   │
    │   └────────────────────────────────────────────────────┘   │
    │                           │                                 │
    │                           ▼                                 │
    │   Output: Optimized Batches                                 │
    │   ┌────────────────────────────────────────────────────┐   │
    │   │ Batch 1: [A, B, C, E, F]   Batch 2: [D]            │   │
    │   │ (5 parallel calls)         (1 call after A done)   │   │
    │   └────────────────────────────────────────────────────┘   │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

Usage:
    aggregator = BatchAggregator(config)
    batches = aggregator.aggregate(waves)
    for batch in batches:
        results = await pool.execute_wave(batch.tasks)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict

from .agent_pool import AgentTask


@dataclass
class BatchConfig:
    """
    Configuration for batch aggregation.

    Attributes:
        enabled: Whether batch aggregation is enabled
        max_batch_size: Maximum number of tasks per batch
        batch_timeout_ms: Time to wait for more requests before executing
        cross_wave_batching: Whether to batch tasks across wave boundaries
    """
    enabled: bool = False
    max_batch_size: int = 10
    batch_timeout_ms: int = 100
    cross_wave_batching: bool = True


@dataclass
class BatchGroup:
    """
    A group of tasks that can be executed together in parallel.

    Attributes:
        tasks: List of tasks in this batch
        wave_indices: Set of original wave indices these tasks came from
        dependency_level: Topological level (0 = no deps, higher = more deps)
    """
    tasks: List[AgentTask] = field(default_factory=list)
    wave_indices: Set[int] = field(default_factory=set)
    dependency_level: int = 0

    def __len__(self) -> int:
        return len(self.tasks)

    @property
    def task_names(self) -> List[str]:
        """Return names of all tasks in this batch."""
        return [t.name for t in self.tasks]


class BatchAggregator:
    """
    Groups independent tasks into optimized batches for parallel execution.

    The aggregator analyzes task dependencies and groups tasks that can
    safely execute in parallel, even if they were originally in different
    waves. This minimizes the number of sequential execution boundaries
    (wave transitions) and reduces overall API round-trip latency.

    Example:
        ```python
        config = BatchConfig(enabled=True, max_batch_size=10)
        aggregator = BatchAggregator(config)

        waves = [
            Wave(index=0, tasks=[task_a, task_b, task_c]),
            Wave(index=1, tasks=[task_d, task_e]),  # task_d depends on task_a
            Wave(index=2, tasks=[task_f]),
        ]

        batches = aggregator.aggregate(waves)
        # Result: [BatchGroup([A,B,C,E,F], level=0), BatchGroup([D], level=1)]
        ```
    """

    def __init__(self, config: Optional[BatchConfig] = None):
        """
        Initialize the aggregator.

        Args:
            config: Batch configuration settings
        """
        self.config = config or BatchConfig()

    def aggregate(self, waves: "List[Wave]") -> List[BatchGroup]:
        """
        Analyze task DAG and group independent tasks into batches.

        Algorithm:
        1. Extract all tasks and build dependency graph
        2. Compute topological levels (tasks at same level are independent)
        3. Group tasks by level, respecting max_batch_size
        4. Return ordered list of BatchGroups

        Args:
            waves: List of Wave objects containing tasks

        Returns:
            List of BatchGroup objects in execution order
        """
        if not self.config.enabled:
            # If disabled, return one batch per wave (original behavior)
            return self._waves_to_batches(waves)

        # Extract all tasks with wave index tracking
        all_tasks: List[Tuple[AgentTask, int]] = []
        for wave in waves:
            for task in wave.tasks:
                all_tasks.append((task, wave.index))

        if not all_tasks:
            return []

        # Build dependency graph
        task_map = {task.name: (task, wave_idx) for task, wave_idx in all_tasks}
        deps_graph = self._build_dependency_graph(all_tasks)

        # Compute topological levels
        levels = self._compute_topological_levels(task_map, deps_graph)

        # Group by level into batches
        batches = self._group_by_levels(task_map, levels)

        return batches

    def _waves_to_batches(self, waves: "List[Wave]") -> List[BatchGroup]:
        """Convert waves to batches (1:1 mapping when batching disabled)."""
        batches = []
        for wave in waves:
            if wave.tasks:
                batch = BatchGroup(
                    tasks=list(wave.tasks),
                    wave_indices={wave.index},
                    dependency_level=wave.index,
                )
                batches.append(batch)
        return batches

    def _build_dependency_graph(
        self,
        all_tasks: List[Tuple[AgentTask, int]]
    ) -> Dict[str, Set[str]]:
        """
        Build a dependency graph from task list.

        Args:
            all_tasks: List of (task, wave_index) tuples

        Returns:
            Dict mapping task name to set of dependency names
        """
        graph: Dict[str, Set[str]] = {}
        task_names = {task.name for task, _ in all_tasks}

        for task, _ in all_tasks:
            # Only include dependencies that exist in our task set
            deps = set(task.depends_on or []) & task_names
            graph[task.name] = deps

        return graph

    def _compute_topological_levels(
        self,
        task_map: Dict[str, Tuple[AgentTask, int]],
        deps_graph: Dict[str, Set[str]]
    ) -> Dict[str, int]:
        """
        Compute topological level for each task.

        Level 0: Tasks with no dependencies
        Level N: Tasks whose dependencies are all at levels < N

        Args:
            task_map: Map of task name to (task, wave_index)
            deps_graph: Dependency graph

        Returns:
            Dict mapping task name to level
        """
        levels: Dict[str, int] = {}
        remaining = set(deps_graph.keys())

        current_level = 0
        max_iterations = len(remaining) + 1  # Prevent infinite loop

        while remaining and max_iterations > 0:
            max_iterations -= 1

            # Find tasks whose deps are all resolved (in levels dict)
            ready = []
            for task_name in remaining:
                deps = deps_graph[task_name]
                if all(dep in levels for dep in deps):
                    ready.append(task_name)

            if not ready:
                # Circular dependency - shouldn't happen if waves are valid
                # Assign remaining tasks to current level
                for task_name in remaining:
                    levels[task_name] = current_level
                break

            # Assign level to ready tasks
            for task_name in ready:
                if deps_graph[task_name]:
                    # Level is max of dependency levels + 1
                    dep_levels = [levels[d] for d in deps_graph[task_name]]
                    levels[task_name] = max(dep_levels) + 1
                else:
                    levels[task_name] = 0
                remaining.remove(task_name)

            current_level += 1

        return levels

    def _group_by_levels(
        self,
        task_map: Dict[str, Tuple[AgentTask, int]],
        levels: Dict[str, int]
    ) -> List[BatchGroup]:
        """
        Group tasks by topological level into batches.

        Tasks at the same level are independent and can run in parallel.
        Respects max_batch_size by splitting large levels into multiple batches.

        Args:
            task_map: Map of task name to (task, wave_index)
            levels: Map of task name to topological level

        Returns:
            List of BatchGroup objects
        """
        # Group by level
        level_groups: Dict[int, List[Tuple[AgentTask, int]]] = defaultdict(list)
        for task_name, level in levels.items():
            task, wave_idx = task_map[task_name]
            level_groups[level].append((task, wave_idx))

        # Convert to batches, splitting by max_batch_size
        batches: List[BatchGroup] = []
        for level in sorted(level_groups.keys()):
            tasks_at_level = level_groups[level]

            # Sort by priority within level
            tasks_at_level.sort(key=lambda x: x[0].priority)

            # Split into batches of max_batch_size
            for i in range(0, len(tasks_at_level), self.config.max_batch_size):
                chunk = tasks_at_level[i:i + self.config.max_batch_size]
                batch = BatchGroup(
                    tasks=[t for t, _ in chunk],
                    wave_indices={w for _, w in chunk},
                    dependency_level=level,
                )
                batches.append(batch)

        return batches

    def can_batch_together(
        self,
        task_a: AgentTask,
        task_b: AgentTask
    ) -> bool:
        """
        Check if two tasks can execute in the same batch.

        Tasks can be batched if neither depends on the other.

        Args:
            task_a: First task
            task_b: Second task

        Returns:
            True if tasks can be batched together
        """
        a_deps = set(task_a.depends_on or [])
        b_deps = set(task_b.depends_on or [])

        # Neither should depend on the other
        return task_a.name not in b_deps and task_b.name not in a_deps

    def get_aggregation_stats(
        self,
        waves: "List[Wave]",
        batches: List[BatchGroup]
    ) -> Dict[str, any]:
        """
        Calculate statistics about the aggregation.

        Args:
            waves: Original waves
            batches: Aggregated batches

        Returns:
            Dict with aggregation statistics
        """
        original_boundaries = len(waves)
        new_boundaries = len(batches)
        total_tasks = sum(len(b.tasks) for b in batches)

        # Calculate theoretical latency reduction
        if original_boundaries > 0:
            reduction_pct = (1 - new_boundaries / original_boundaries) * 100
        else:
            reduction_pct = 0

        return {
            "original_waves": original_boundaries,
            "aggregated_batches": new_boundaries,
            "total_tasks": total_tasks,
            "boundary_reduction_pct": round(reduction_pct, 1),
            "avg_batch_size": (
                total_tasks / new_boundaries if new_boundaries > 0 else 0
            ),
            "cross_wave_tasks": sum(
                1 for b in batches if len(b.wave_indices) > 1
                for _ in b.tasks
            ),
        }


# Type import for Wave (avoid circular import)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wave_scheduler import Wave

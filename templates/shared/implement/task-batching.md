# Task-Level Batching

## Purpose

Group independent tasks from tasks.md into batches and execute them as parallel Task tool calls in a **single message**, achieving true parallelism and reducing API round-trips by 4-8x.

## Performance Impact

| Mode | Round-trips | Time | Savings |
|------|-------------|------|---------|
| Sequential tasks | N (per task) | ~10 min | baseline |
| Batched tasks (4-8) | N/4-8 | ~2-3 min | 3-5x faster |

## Configuration

```yaml
task_batching:
  enabled: true
  skip_flag: "--sequential-tasks"
  max_batch_size: 8                     # Max tasks per batch (rate limit safe)
  batch_by: dependency_level            # Group by topological level
  file_conflict_resolution: queue       # Tasks on same file → next batch
  parallel_marker: "[P]"                # Explicit parallel marker (optional)
```

---

## Core Algorithm: BATCH_TASKS

```text
FUNCTION BATCH_TASKS(tasks_md_path):
  """
  Parse tasks.md, build dependency graph, group into optimal batches.

  Returns: List[Batch] where each Batch contains independent tasks.
  """

  # Step 1: Parse tasks from tasks.md
  tasks = PARSE_TASKS(tasks_md_path)

  # Step 2: Build dependency graph
  graph = {}
  FOR EACH task IN tasks:
    task_id = task.id  # e.g., "T001"

    # Extract explicit dependencies [DEP:Txxx]
    explicit_deps = EXTRACT_PATTERN(task.text, /\[DEP:T(\d+)\]/)

    # Extract target files for conflict detection
    target_files = EXTRACT_FILES(task)

    graph[task_id] = {
      task: task,
      deps: explicit_deps,
      files: target_files,
      phase: task.phase,  # Setup, Tests, Core, Integration, Polish
      markers: task.markers,  # [P], [SCAFFOLD], [TEST:], etc.
      level: null  # Computed in Step 3
    }

  # Step 3: Compute topological levels
  levels = COMPUTE_TOPOLOGICAL_LEVELS(graph)

  # Step 4: Split levels by file conflicts and max_batch_size
  batches = []
  FOR level IN sorted(levels.keys()):
    tasks_at_level = levels[level]
    level_batches = SPLIT_BY_FILE_CONFLICT(tasks_at_level, config.max_batch_size)
    batches.extend(level_batches)

  RETURN batches
```

---

## Topological Level Computation

```text
FUNCTION COMPUTE_TOPOLOGICAL_LEVELS(graph):
  """
  Kahn's algorithm variant: assign level based on longest path from roots.
  Tasks at same level have no interdependencies → can run in parallel.
  """

  levels = {}
  remaining = set(graph.keys())
  current_level = 0

  WHILE remaining:
    # Find tasks with all dependencies satisfied
    ready = []
    FOR task_id IN remaining:
      deps = graph[task_id].deps
      unsatisfied = [d for d IN deps WHERE d IN remaining]
      IF len(unsatisfied) == 0:
        ready.append(task_id)

    IF len(ready) == 0:
      # Circular dependency detected
      ERROR "Circular dependency in tasks: {remaining}"
      BREAK

    # Assign level to ready tasks
    levels[current_level] = [graph[tid].task FOR tid IN ready]

    # Update graph
    FOR task_id IN ready:
      graph[task_id].level = current_level
    remaining -= set(ready)
    current_level += 1

  RETURN levels
```

---

## File Conflict Resolution

```text
FUNCTION SPLIT_BY_FILE_CONFLICT(tasks, max_size):
  """
  Tasks modifying the same file cannot be in the same batch.
  Split into multiple batches to ensure file isolation.
  """

  batches = []
  current_batch = []
  files_in_batch = set()

  FOR task IN tasks:
    task_files = set(task.files or [])

    # Check for file conflict
    IF task_files & files_in_batch:  # Intersection
      # Conflict - start new batch
      IF current_batch:
        batches.append(Batch(tasks=current_batch, files=files_in_batch))
      current_batch = [task]
      files_in_batch = task_files

    # Check batch size limit
    ELIF len(current_batch) >= max_size:
      batches.append(Batch(tasks=current_batch, files=files_in_batch))
      current_batch = [task]
      files_in_batch = task_files

    # Add to current batch
    ELSE:
      current_batch.append(task)
      files_in_batch |= task_files

  # Don't forget last batch
  IF current_batch:
    batches.append(Batch(tasks=current_batch, files=files_in_batch))

  RETURN batches
```

---

## Batch Execution

```text
FUNCTION EXECUTE_BATCH(batch, batch_index, total_batches):
  """
  Execute ALL tasks in batch as parallel Task tool calls in SINGLE message.

  CRITICAL: To achieve parallelism, ALL Task calls MUST be in same response.
  """

  # Display batch header
  PRINT "📦 Batch {batch_index}/{total_batches} ({len(batch.tasks)} tasks)"
  FOR task IN batch.tasks:
    model = SELECT_MODEL(task)
    PRINT "├── {task.id} [{model}]: {task.title}"
  PRINT "⏳ Executing batch in parallel..."

  # Build Task tool calls
  task_calls = []
  FOR task IN batch.tasks:
    prompt = BUILD_TASK_PROMPT(task)
    model = SELECT_MODEL(task)

    task_calls.append(
      Task(
        description: "{task.id}: {task.title[:40]}",
        prompt: prompt,
        subagent_type: "general-purpose",
        model: model,
        run_in_background: false
      )
    )

  # EMIT ALL CALLS IN SINGLE MESSAGE (achieves parallelism)
  results = EMIT_PARALLEL_TASK_CALLS(task_calls)

  # Process results
  success_count = 0
  FOR i, result IN enumerate(results):
    task = batch.tasks[i]
    IF result.success:
      MARK_TASK_COMPLETE(task.id)  # [ ] → [X] in tasks.md
      success_count += 1
      PRINT "├── ✓ {task.id}: {result.summary}"
    ELSE:
      MARK_TASK_BLOCKED(task.id, result.error)  # [ ] → [!]
      PRINT "├── ✗ {task.id}: {result.error}"

  PRINT "✓ Batch {batch_index}/{total_batches} complete ({success_count}/{len(batch.tasks)} succeeded)"

  RETURN results
```

---

## Task Prompt Construction

```text
FUNCTION BUILD_TASK_PROMPT(task):
  """
  Build complete prompt for Task agent with full context.
  """

  prompt = """
Feature Directory: {FEATURE_DIR}

## Task
{task.id}: {task.title}

## Description
{task.description}

## Target Files
{task.files}

## Requirements
- Follow existing code patterns in the codebase
- Add @speckit annotations for traceability
- Run tests if applicable

## Markers
{task.markers}

## Acceptance Criteria
{task.acceptance_criteria or "Task completes without errors"}

---
Complete this task. Report any blockers.
"""

  RETURN prompt
```

---

## Model Selection per Task

```text
FUNCTION SELECT_MODEL(task):
  """
  Select optimal model based on task type and complexity.
  Optimizes for cost while maintaining quality.
  """

  markers = task.markers or []

  # Infrastructure tasks → haiku (fast, cheap)
  IF "[SCAFFOLD]" IN markers OR "[CONFIG]" IN markers OR "[DEPS]" IN markers:
    RETURN "haiku"

  # Test scaffolding → haiku
  IF "[TDD:scaffold]" IN markers OR task.id matches /T\d{3}.*scaffold/i:
    RETURN "haiku"

  # Test implementation → sonnet
  IF "[TEST:" IN markers OR "[TDD:" IN markers:
    RETURN "sonnet"

  # Complex business logic or architecture → opus
  IF "[COMPLEX]" IN markers OR "[ARCH]" IN markers OR "[CRITICAL]" IN markers:
    RETURN "opus"

  # API/backend logic → sonnet
  IF "[API]" IN markers OR "[FR:" IN markers:
    RETURN "sonnet"

  # Default
  RETURN "sonnet"
```

---

## Integration with Wave System

Task batching operates **within** wave execution:

```text
WAVE_WITH_TASK_BATCHING(wave, tasks_for_wave):
  """
  Within each wave, batch tasks for maximum parallelism.
  """

  # Filter tasks belonging to this wave
  wave_tasks = [t for t IN tasks_for_wave WHERE t.wave == wave.id]

  # Apply batching algorithm
  batches = BATCH_TASKS(wave_tasks)

  # Execute batches sequentially (batches depend on each other)
  FOR batch_index, batch IN enumerate(batches):
    EXECUTE_BATCH(batch, batch_index + 1, len(batches))
```

---

## Complete Execution Flow

```text
BATCHED_IMPLEMENTATION(tasks_md_path):
  """
  Main entry point for batched task execution.
  """

  # Step 1: Parse and batch tasks
  LOG "🔄 Analyzing task dependencies..."
  batches = BATCH_TASKS(tasks_md_path)

  total_tasks = sum(len(b.tasks) for b IN batches)
  LOG "📊 Batching complete: {total_tasks} tasks → {len(batches)} batches"

  # Step 2: Display execution plan
  FOR i, batch IN enumerate(batches):
    LOG "  Batch {i+1}: {[t.id for t IN batch.tasks]}"

  # Step 3: Execute batches
  LOG "🚀 Starting batched execution..."

  all_results = []
  FOR batch_index, batch IN enumerate(batches):
    results = EXECUTE_BATCH(batch, batch_index + 1, len(batches))
    all_results.extend(results)

    # Check for critical failures
    critical_failures = [r for r IN results WHERE r.is_critical AND NOT r.success]
    IF critical_failures:
      LOG "⛔ Critical task failed, halting execution"
      BREAK

  # Step 4: Summary
  success = sum(1 for r IN all_results WHERE r.success)
  failed = len(all_results) - success

  LOG """
📊 Batched Execution Complete
├── Total Tasks: {len(all_results)}
├── Succeeded: {success}
├── Failed: {failed}
├── Batches: {len(batches)}
└── Parallelism: {total_tasks / len(batches):.1f}x avg
"""
```

---

## Progress Output Format

### Batch Start

```text
📦 Batch 1/4 (3 tasks)
├── T001 [haiku]: Create project scaffold
├── T002 [haiku]: Install dependencies
└── T003 [sonnet]: Configure database connection

⏳ Executing batch in parallel...
```

### Batch Complete

```text
✓ Batch 1/4 complete (2.3s)
├── ✓ T001: Created 5 files in src/
├── ✓ T002: Installed 12 packages
└── ✓ T003: Configured PostgreSQL connection
```

### Final Summary

```text
📊 Batched Execution Complete
├── Total Tasks: 20
├── Succeeded: 19
├── Failed: 1 (T015 - external API timeout)
├── Batches: 5
├── Parallelism: 4.0x avg
└── Time Saved: ~65% vs sequential
```

---

## Skip Flag

```text
IF "--sequential-tasks" IN ARGS:
  LOG "⚠️ Task batching DISABLED (sequential mode)"
  SKIP batching, execute tasks one-by-one
```

---

## Error Handling

```text
BATCH_ERROR_STRATEGY:

  # Non-critical task failure
  IF task fails AND NOT task.is_critical:
    - Mark task as [!] blocked
    - Continue with remaining batch tasks
    - Log failure for summary
    - Skip dependent tasks in future batches

  # Critical task failure
  IF task fails AND task.is_critical:
    - Mark task as [!] blocked
    - Complete current batch (don't abort in-flight)
    - HALT execution after batch
    - Report all failures

  # Batch timeout
  IF batch exceeds timeout:
    - Mark incomplete tasks as [?] timeout
    - Continue to next batch
    - Report timeout in summary
```

---

## Configuration Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enable task batching |
| `skip_flag` | `--sequential-tasks` | Disable batching flag |
| `max_batch_size` | `8` | Max tasks per batch |
| `batch_by` | `dependency_level` | Grouping strategy |
| `file_conflict_resolution` | `queue` | How to handle same-file tasks |
| `parallel_marker` | `[P]` | Explicit parallel marker |

# Operation Batching Framework

## Purpose

Batch independent operations (file reads, searches, validations) into parallel calls within a **single message**, reducing API round-trips and improving execution speed.

## Performance Impact

| Mode | Round-trips | Time | Savings |
|------|-------------|------|---------|
| Sequential operations | N | ~10s | baseline |
| Batched operations (4-8) | N/4-8 | ~2-3s | 3-5x faster |

## Configuration

```yaml
operation_batching:
  enabled: true
  skip_flag: "--sequential"
  strategies:
    - context_reads      # Batch file reads for context gathering
    - searches           # Batch Explore agents
    - validations        # Batch QG/validation checks
    - prefetch           # Speculative parallel load
```

---

## Core Algorithms

### CONTEXT_BATCH

```text
FUNCTION CONTEXT_BATCH(file_paths):
  """
  Batch multiple file reads into a single message.
  Use for loading context files before processing.
  """

  IF len(file_paths) == 0:
    RETURN {}

  IF len(file_paths) == 1:
    RETURN {file_paths[0]: READ(file_paths[0])}

  # Emit all Read calls in single message (parallel)
  PRINT "📖 Context batch ({len(file_paths)} files)..."

  results = EMIT_PARALLEL([
    Read(file_path=path) FOR path IN file_paths
  ])

  # Collect results
  context = {}
  FOR i, path IN enumerate(file_paths):
    IF results[i].success:
      context[path] = results[i].content
      PRINT "├── ✓ {path}"
    ELSE:
      PRINT "├── ⚠ {path}: {results[i].error}"

  PRINT "✓ Context loaded ({len(context)}/{len(file_paths)} files)"

  RETURN context
```

### SEARCH_BATCH

```text
FUNCTION SEARCH_BATCH(queries, model="haiku"):
  """
  Batch multiple searches into parallel Explore agents.
  Each query runs as separate Task with Explore subagent.
  """

  IF len(queries) == 0:
    RETURN []

  IF len(queries) == 1:
    RETURN [SEARCH(queries[0])]

  PRINT "🔍 Search batch ({len(queries)} queries)..."

  agents = []
  FOR query IN queries:
    agents.append(
      Task(
        description: "Search: {query[:30]}...",
        prompt: query,
        subagent_type: "Explore",
        model: model
      )
    )

  # Single message with multiple Task calls
  results = EMIT_PARALLEL(agents)

  FOR i, query IN enumerate(queries):
    IF results[i].success:
      PRINT "├── ✓ {query[:40]}"
    ELSE:
      PRINT "├── ✗ {query[:40]}"

  PRINT "✓ Search complete"

  RETURN results
```

### VALIDATE_BATCH

```text
FUNCTION VALIDATE_BATCH(checks, model="haiku"):
  """
  Run multiple validation/QG checks in parallel.
  """

  IF len(checks) == 0:
    RETURN {passed: [], failed: []}

  PRINT "✅ Validation batch ({len(checks)} checks)..."

  validators = []
  FOR check IN checks:
    validators.append(
      Task(
        description: "QG: {check.id}",
        prompt: BUILD_VALIDATION_PROMPT(check),
        subagent_type: "general-purpose",
        model: model
      )
    )

  results = EMIT_PARALLEL(validators)

  passed = []
  failed = []
  FOR i, check IN enumerate(checks):
    IF results[i].success:
      passed.append(check)
      PRINT "├── ✓ {check.id}: {check.name}"
    ELSE:
      failed.append({check: check, error: results[i].error})
      PRINT "├── ✗ {check.id}: {results[i].error}"

  PRINT "✓ Validation: {len(passed)} passed, {len(failed)} failed"

  RETURN {passed: passed, failed: failed}
```

### PREFETCH_BATCH

```text
FUNCTION PREFETCH_BATCH(paths, optional_paths=[]):
  """
  Speculative parallel load of all potentially-needed files.
  Required paths must exist; optional paths may not exist.
  """

  all_paths = paths + optional_paths

  PRINT "⚡ Prefetch batch ({len(all_paths)} files)..."

  results = EMIT_PARALLEL([
    Read(file_path=path) FOR path IN all_paths
  ])

  cache = {}
  loaded = 0
  FOR i, path IN enumerate(all_paths):
    IF results[i].success:
      cache[path] = results[i].content
      loaded += 1
      PRINT "├── ✓ {path}"
    ELIF path IN optional_paths:
      PRINT "├── ○ {path} (optional, not found)"
    ELSE:
      PRINT "├── ✗ {path} (required, MISSING)"

  PRINT "✓ Prefetched {loaded}/{len(all_paths)} files"

  RETURN cache
```

---

## Subagent Batching

### SUBAGENT_BATCH

```text
FUNCTION SUBAGENT_BATCH(subagents, context):
  """
  Execute independent subagents in parallel.
  Subagents with depends_on=[] can run together.
  """

  # Group by wave (dependency level)
  waves = GROUP_BY_DEPENDENCY(subagents)

  all_results = {}

  FOR wave_idx, wave_subagents IN enumerate(waves):
    PRINT "📦 Wave {wave_idx + 1}/{len(waves)} ({len(wave_subagents)} agents)"

    tasks = []
    FOR agent IN wave_subagents:
      tasks.append(
        Task(
          description: "{agent.role}: {agent.prompt[:30]}",
          prompt: INJECT_CONTEXT(agent.prompt, context),
          subagent_type: "general-purpose",
          model: agent.model_override OR "sonnet"
        )
      )

    # Execute wave in parallel
    results = EMIT_PARALLEL(tasks)

    FOR i, agent IN enumerate(wave_subagents):
      all_results[agent.role] = results[i]
      status = "✓" IF results[i].success ELSE "✗"
      PRINT "├── {status} {agent.role}"

    PRINT "✓ Wave {wave_idx + 1} complete"

  RETURN all_results
```

---

## Integration with Commands

### Specify Command

```text
# Before main processing
CONTEXT = PREFETCH_BATCH(
  paths=[
    "memory/constitution.md",
    "templates/spec-template.md",
    "templates/shared/core/language-loading.md"
  ],
  optional_paths=[
    "specs/concept.md",
    "specs/baseline.md"
  ]
)
```

### Plan Command

```text
# Research phase
RESEARCH_RESULTS = SEARCH_BATCH([
  "Find architecture patterns in codebase",
  "Search for existing API patterns",
  "Find database schema patterns",
  "Check dependency management approach"
])
```

### Tasks Command

```text
# Parallel mappers where no dependency
BATCH_1_RESULTS = SUBAGENT_BATCH([
  {role: "dependency-analyzer", depends_on: []},
  {role: "fr-mapper", depends_on: []}
], context)

# Sequential: as-mapper depends on fr-mapper
BATCH_2_RESULTS = SUBAGENT_BATCH([
  {role: "as-mapper", depends_on: ["fr-mapper"]}
], MERGE(context, BATCH_1_RESULTS))
```

### Clarify Command

```text
# Parallel gap search
GAP_RESULTS = SEARCH_BATCH([
  "Search spec.md for vague terms and ambiguities",
  "Search plan.md for undefined references",
  "Search tasks.md for missing acceptance criteria"
])
```

### Design Command

```text
# Pre-cache design context
DESIGN_CONTEXT = PREFETCH_BATCH(
  paths=[
    "memory/constitution.md",
    "{FEATURE_DIR}/spec.md"
  ],
  optional_paths=[
    "design-system/tokens.json",
    "design-system/components.md",
    ".speckit/design-presets.yaml"
  ]
)
```

---

## Progress Output Format

### Batch Start

```text
📖 Context batch (4 files)...
├── ✓ memory/constitution.md
├── ✓ templates/spec-template.md
├── ✓ specs/concept.md
├── ○ specs/baseline.md (optional, not found)
✓ Context loaded (3/4 files)
```

### Search Batch

```text
🔍 Search batch (3 queries)...
├── ✓ Find architecture patterns...
├── ✓ Search for existing API...
├── ✓ Find database schema...
✓ Search complete
```

### Validation Batch

```text
✅ Validation batch (4 checks)...
├── ✓ IG-SPEC-001: Constitution Alignment
├── ✓ IG-SPEC-002: Ambiguity Detection
├── ✗ IG-SPEC-003: FR-AS Coverage
├── ✓ IG-SPEC-004: Implementation Details
✓ Validation: 3 passed, 1 failed
```

---

## Skip Flag

```text
IF "--sequential" IN ARGS:
  LOG "⚠️ Operation batching DISABLED (sequential mode)"
  SKIP batching, execute operations one-by-one
```

---

## Error Handling

```text
BATCH_ERROR_STRATEGY:

  # Non-critical operation failure
  IF operation fails AND NOT operation.required:
    - Log warning
    - Continue with remaining operations
    - Mark as optional/skipped in results

  # Critical operation failure
  IF operation fails AND operation.required:
    - Log error
    - Complete current batch (don't abort in-flight)
    - Report all failures
    - Consider blocking or degraded mode
```

---

## Configuration Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enable operation batching |
| `skip_flag` | `--sequential` | Disable batching flag |
| `strategies.context_reads` | `true` | Batch file reads |
| `strategies.searches` | `true` | Batch Explore agents |
| `strategies.validations` | `true` | Batch QG checks |
| `strategies.prefetch` | `true` | Speculative parallel load |

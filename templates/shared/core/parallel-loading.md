# Parallel File Loading

## Purpose

Unified parallel file loading for all Spec Kit commands. This module replaces sequential file reads with batched parallel operations to reduce initialization time by 2-3 seconds per command.

## Instructions for AI Agents

Execute parallel loading at the **start** of any command that requires multiple file reads.

### Performance Context

```text
SEQUENTIAL READS (SLOW):
  Read(file1)   150ms
  Read(file2)   200ms
  Read(file3)   300ms
  Total: 650ms

PARALLEL READS (FAST):
  Read([file1, file2, file3])  300ms total
  Savings: ~350ms (54% faster)
```

---

## Parallel Batch Read Pattern

### Step 1: Identify Independent Files

Before reading, group files that have **no dependencies on each other**:

```text
INDEPENDENT (can parallelize):
- language-loading.md      # No deps
- complexity-scoring.md    # No deps
- brownfield-detection.md  # No deps
- constitution.md          # No deps
- baseline.md              # No deps

DEPENDENT (must sequence):
- concept.md → depends on constitution.md read first
- spec.md → may depend on concept.md
```

### Step 2: Execute Parallel Read

Use Claude Code's parallel tool execution:

```text
PARALLEL_BATCH_READ:
  Read IN PARALLEL (single message, multiple Read tool calls):
  - `templates/shared/core/language-loading.md`
  - `templates/shared/complexity-scoring.md`
  - `templates/shared/core/brownfield-detection.md`
```

**Implementation Note**: In Claude Code, make multiple Read tool calls in a single assistant message to achieve parallelism.

### Step 3: Execute After All Loaded

Only after ALL parallel reads complete, execute the loaded modules:

```text
EXECUTE language-loading → ARTIFACT_LANGUAGE
EXECUTE complexity-scoring → COMPLEXITY_TIER, COMPLEXITY_SCORE
EXECUTE brownfield-detection → BROWNFIELD_MODE
```

---

## Speculative Pre-fetching

For commands that frequently need certain files, pre-fetch them in background before they're requested.

### Pre-fetch Lists by Command

```yaml
specify:
  always:
    - memory/constitution.md
    - templates/spec-template.md
  conditional:
    - specs/concept.md           # If concept-driven
    - specs/*/baseline.md        # If brownfield mode

plan:
  always:
    - memory/constitution.md
    - templates/plan-template.md
    - FEATURE_DIR/spec.md
  conditional:
    - specs/concept.md           # If concept-driven

tasks:
  always:
    - memory/constitution.md
    - templates/tasks-template.md
    - FEATURE_DIR/spec.md
    - FEATURE_DIR/plan.md
  conditional:
    - specs/concept.md           # If concept-driven

implement:
  always:
    - FEATURE_DIR/tasks.md
    - FEATURE_DIR/plan.md
    - memory/constitution.md
  conditional:
    - FEATURE_DIR/checklists/*.md

design:
  always:
    - FEATURE_DIR/spec.md
    - memory/constitution.md
  conditional:
    - templates/design-tokens/*.md
```

### Pre-fetch Execution Pattern

```text
FUNCTION speculative_prefetch(command: str, feature_dir: str):

  # Get prefetch list for command
  prefetch_list = PREFETCH_LISTS[command].always

  # Add conditional files if they exist
  FOR file IN PREFETCH_LISTS[command].conditional:
    IF file_exists(resolve_path(file, feature_dir)):
      prefetch_list.append(file)

  # Launch background parallel read (don't wait)
  background_task = PARALLEL_READ_ASYNC(prefetch_list)

  # Store task handle for later retrieval
  PREFETCH_CACHE[command] = background_task

  RETURN  # Continue with command execution immediately
```

---

## Integration with Commands

### Standard Init Pattern

Replace sequential reads in command Init sections with:

```markdown
## Init [REF:INIT-001]

### Parallel Context Load

Read IN PARALLEL (batch for performance):
- `templates/shared/core/language-loading.md`
- `templates/shared/complexity-scoring.md`
- `templates/shared/core/brownfield-detection.md`

### Execute Loaded Modules

```text
EXECUTE language-loading → ARTIFACT_LANGUAGE
EXECUTE complexity-scoring → COMPLEXITY_TIER, COMPLEXITY_SCORE
EXECUTE brownfield-detection → BROWNFIELD_MODE

REPORT: "Context loaded in {LOAD_TIME}ms (parallel)"
```
```

### Feature-Specific Parallel Loads

When loading feature artifacts:

```markdown
### Load Feature Context

Read IN PARALLEL:
- `{FEATURE_DIR}/spec.md`
- `{FEATURE_DIR}/plan.md` (if exists)
- `memory/constitution.md`

Store loaded content for subsequent steps.
```

---

## Performance Metrics

Track parallel loading performance:

```text
PARALLEL_LOAD_METRICS:
  files_loaded: N
  total_time_ms: T
  sequential_estimate_ms: S  # Sum of individual file sizes / avg read speed
  savings_ms: S - T
  savings_percent: ((S - T) / S) * 100

REPORT: "Loaded {N} files in {T}ms (saved {savings_ms}ms, {savings_percent}% faster)"
```

---

## Error Handling

```text
FUNCTION parallel_read_with_fallback(files: list):

  results = PARALLEL_READ(files)

  FOR file, result IN results:
    IF result.error:
      IF file IN REQUIRED_FILES:
        FAIL "Required file missing: {file}"
      ELSE:
        LOG "Optional file not found: {file} (continuing)"
        results[file] = null

  RETURN results
```

---

## Caching

For repeated reads within a session:

```text
PARALLEL_READ_CACHE:
  key: file_path + file_mtime
  value: file_content
  ttl: session_duration

FUNCTION cached_parallel_read(files: list):
  uncached = []
  results = {}

  FOR file IN files:
    IF file IN CACHE AND not stale(file):
      results[file] = CACHE[file]
    ELSE:
      uncached.append(file)

  IF uncached:
    new_results = PARALLEL_READ(uncached)
    FOR file, content IN new_results:
      CACHE[file] = content
      results[file] = content

  RETURN results
```

---

## API-Level Prompt Caching [REF:PC-001]

Beyond file-level caching, use Anthropic's native prompt caching for API calls.

**Integration**: See `templates/shared/caching-strategy.md` for full documentation.

### Quick Reference

```yaml
# In command frontmatter
claude_code:
  cache_control:
    system_prompt: ephemeral    # Cache command instructions
    constitution: ephemeral      # Cache project principles
    templates: ephemeral         # Cache loaded templates
    artifacts: ephemeral         # Cache spec/plan/tasks
    ttl: session                 # session | 3600 | permanent
```

### Expected Savings

| Layer | Hit Rate | Savings |
|-------|----------|---------|
| File caching (L1) | 60-70% | 10-50ms per hit |
| Prompt caching (L0) | 80-90% | 80-90% input tokens |

### Cache Hierarchy

```
L0: Prompt Cache (Anthropic API) ← API-level, 80-90% token reduction
L1: File Cache (In-Memory)       ← File-level, 60-70% hit rate
L2: Session Cache                ← Response caching
```

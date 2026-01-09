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
| `strategies.sections` | `true` | Batch plan sections by dependency |

---

## Section Batching

### SECTION_BATCH Algorithm

**PURPOSE**: Batch independent plan sections into parallel Task calls, reducing sequential execution.

```text
FUNCTION SECTION_BATCH(sections, dependency_config):
  """
  Execute independent plan sections in parallel waves.
  Sections with no dependencies run together.
  Sections depending on prior outputs wait for their wave.
  """

  # Build dependency graph
  graph = {}
  FOR section IN sections:
    graph[section.id] = {
      section: section,
      depends_on: section.depends_on OR [],
      resolved: false
    }

  # Topological sort into waves
  waves = []
  resolved_ids = set()

  WHILE len(resolved_ids) < len(sections):
    # Find sections with all dependencies resolved
    current_wave = []
    FOR section_id, node IN graph.items():
      IF node.resolved:
        CONTINUE

      deps_met = ALL(dep IN resolved_ids FOR dep IN node.depends_on)
      IF deps_met:
        current_wave.append(node.section)

    IF len(current_wave) == 0:
      ERROR: "Circular dependency detected in section config"
      BREAK

    # Mark as resolved
    FOR section IN current_wave:
      graph[section.id].resolved = true
      resolved_ids.add(section.id)

    waves.append(current_wave)

  # Execute waves
  all_results = {}
  wave_idx = 0

  FOR wave IN waves:
    wave_idx += 1
    section_names = [s.name FOR s IN wave]
    PRINT "📦 Section Wave {wave_idx}/{len(waves)} ({len(wave)} sections)"
    PRINT "├── " + ", ".join(section_names)

    # Build Task calls for all sections in wave
    task_calls = []
    FOR section IN wave:
      task_calls.append(
        Task(
          description: "Generate {section.name}",
          prompt: BUILD_SECTION_PROMPT(section, all_results),
          subagent_type: "general-purpose",
          model: section.model OR "sonnet"
        )
      )

    # CRITICAL: Execute ALL in SINGLE message (parallel)
    results = EMIT_PARALLEL(task_calls)

    # Collect results
    FOR i, section IN enumerate(wave):
      IF results[i].success:
        all_results[section.id] = results[i].content
        PRINT "├── ✓ {section.name}"
      ELSE:
        PRINT "├── ✗ {section.name}: {results[i].error}"
        all_results[section.id] = null

    PRINT "✓ Wave {wave_idx} complete"

    # Update METRICS_STATE per wave
    emit_wave_token_summary(wave_idx, results)

  RETURN all_results
```

### BUILD_SECTION_PROMPT

```text
FUNCTION BUILD_SECTION_PROMPT(section, prior_results):
  """
  Build prompt for section generation with context from prior waves.
  """

  prompt = """
  Generate the "{section.name}" section for plan.md.

  **Source files**: {section.sources}
  **Output format**: Markdown section
  """

  # Inject results from dependencies
  IF section.depends_on:
    prompt += "\n\n**Context from prior sections**:\n"
    FOR dep_id IN section.depends_on:
      IF dep_id IN prior_results AND prior_results[dep_id]:
        prompt += "\n### {dep_id}:\n{prior_results[dep_id][:2000]}...\n"

  RETURN prompt
```

### Section Dependency Configuration

Define section dependencies in command YAML frontmatter:

```yaml
section_batching:
  enabled: true
  skip_flag: "--sequential-sections"

  sections:
    # Wave 1: Independent sections (no dependencies)
    - id: strategic_narrative
      name: "Strategic Narrative"
      depends_on: []
      sources: [concept.md]
      model: sonnet

    - id: pre_mortem
      name: "Pre-Mortem Analysis"
      depends_on: []
      sources: [concept.md]
      model: sonnet

    - id: technical_context
      name: "Technical Context"
      depends_on: []
      sources: [spec.md, constitution.md]
      model: sonnet

    - id: nfr_definition
      name: "NFR Definition"
      depends_on: []
      sources: [spec.md]
      model: sonnet

    - id: dependency_registry
      name: "Dependency Registry"
      depends_on: []
      sources: [spec.md]
      model: sonnet

    # Wave 2: Depends on Wave 1
    - id: adrs
      name: "Architecture Decisions"
      depends_on: [technical_context, nfr_definition]
      sources: [spec.md]
      model: sonnet

    # Wave 3: Depends on Wave 2
    - id: rtm
      name: "Requirements Traceability Matrix"
      depends_on: [adrs]
      sources: [spec.md]
      model: sonnet

    - id: observability
      name: "Observability Plan"
      depends_on: [nfr_definition]
      sources: [spec.md]
      model: sonnet

    - id: scalability
      name: "Scalability Strategy"
      depends_on: [nfr_definition, technical_context]
      sources: [spec.md]
      model: sonnet
```

### Section Batching Progress Output

```text
📦 Section Wave 1/3 (5 sections)
├── Strategic Narrative, Pre-Mortem, Technical Context, NFR Definition, Dependency Registry
├── ✓ Strategic Narrative
├── ✓ Pre-Mortem Analysis
├── ✓ Technical Context
├── ✓ NFR Definition
├── ✓ Dependency Registry
✓ Wave 1 complete

📊 Wave 1 Token Summary:
| Model  | Tokens In | Tokens Out | Cost    |
|--------|-----------|------------|---------|
| sonnet | 45,230    | 12,450     | $0.3218 |

📦 Section Wave 2/3 (1 section)
├── Architecture Decisions
├── ✓ Architecture Decisions
✓ Wave 2 complete

📦 Section Wave 3/3 (3 sections)
├── RTM, Observability Plan, Scalability Strategy
├── ✓ Requirements Traceability Matrix
├── ✓ Observability Plan
├── ✓ Scalability Strategy
✓ Wave 3 complete
```

### TodoWrite Integration

```text
# Instead of per-section todos, show wave progress:

TodoWrite([
  {content: "Wave 1: Strategic + Pre-Mortem + Context + NFRs + Deps", status: "in_progress", activeForm: "Generating Wave 1 sections..."},
  {content: "Wave 2: Architecture Decisions (ADRs)", status: "pending", activeForm: "Generating Architecture Decisions..."},
  {content: "Wave 3: RTM + Observability + Scalability", status: "pending", activeForm: "Generating Wave 3 sections..."},
  {content: "Self-review and validation", status: "pending", activeForm: "Running self-review..."}
])

# Update as waves complete:
AFTER wave_1_complete:
  TodoWrite([
    {content: "Wave 1: Strategic + Pre-Mortem + Context + NFRs + Deps", status: "completed", ...},
    {content: "Wave 2: Architecture Decisions (ADRs)", status: "in_progress", ...},
    ...
  ])
```

---

## Artifact Extraction

### Purpose

Extract structured data from artifacts to minimize token consumption for subagents.
See `templates/shared/artifact-extraction.md` for full extraction algorithms.

### EXTRACT_BATCH Algorithm

```text
FUNCTION EXTRACT_BATCH(artifacts):
  """
  Extract structured data from multiple artifacts in parallel.
  Returns cached extraction results.
  """

  IMPORT: templates/shared/artifact-extraction.md

  IF len(artifacts) == 0:
    RETURN {}

  PRINT "📊 Extraction batch ({len(artifacts)} artifacts)..."

  results = {}

  # Process each artifact type
  FOR artifact IN artifacts:
    SWITCH artifact.type:
      CASE "spec":
        results["spec"] = EXTRACT_SPEC(artifact.path)
        PRINT "├── ✓ spec: {len(results.spec.fr_list)} FRs, {len(results.spec.as_list)} ASs"

      CASE "plan":
        results["plan"] = EXTRACT_PLAN(artifact.path)
        PRINT "├── ✓ plan: {len(results.plan.phases)} phases"

      CASE "concept":
        result = EXTRACT_CONCEPT(artifact.path)
        IF result:
          results["concept"] = result
          PRINT "├── ✓ concept: {len(results.concept.epic_ids)} epics"
        ELSE:
          PRINT "├── ○ concept: not found (optional)"

  # Calculate savings
  original_size = SUM(artifact.size FOR artifact IN artifacts)
  extracted_size = estimate_size(results)
  reduction_pct = round((1 - extracted_size / original_size) * 100)

  PRINT "✓ Extraction complete: {original_size}KB → {extracted_size}KB ({reduction_pct}% reduction)"

  RETURN results
```

### Integration with Prefetch

```text
## Step 0: Prefetch and Extract

# 1. Prefetch files (parallel)
PREFETCH_BATCH(
  paths=[constitution, templates, spec.md, plan.md],
  optional_paths=[concept.md]
)

# 2. Extract data (uses cached file contents)
IF artifact_extraction.enabled:
  EXTRACTED = EXTRACT_BATCH([
    {type: "spec", path: FEATURE_DIR/spec.md},
    {type: "plan", path: FEATURE_DIR/plan.md},
    {type: "concept", path: specs/concept.md}
  ])

  # Make available for subagents
  SESSION_CACHE["SPEC_DATA"] = EXTRACTED.spec
  SESSION_CACHE["PLAN_DATA"] = EXTRACTED.plan
```

### Subagent Context Injection

```text
# When context_injection: extracted is set on subagent

FUNCTION INJECT_EXTRACTED_CONTEXT(subagent, prompt):
  """
  Replace {SPEC_DATA.*} and {PLAN_DATA.*} placeholders
  with extracted data from SESSION_CACHE.
  """

  SPEC_DATA = SESSION_CACHE.get("SPEC_DATA", {})
  PLAN_DATA = SESSION_CACHE.get("PLAN_DATA", {})

  # Replace placeholders
  prompt = prompt.replace("{SPEC_DATA.fr_list}", format_list(SPEC_DATA.fr_list))
  prompt = prompt.replace("{SPEC_DATA.fr_summaries}", format_summaries(SPEC_DATA.fr_summaries))
  prompt = prompt.replace("{SPEC_DATA.as_list}", format_list(SPEC_DATA.as_list))
  prompt = prompt.replace("{SPEC_DATA.as_summaries}", format_summaries(SPEC_DATA.as_summaries))
  prompt = prompt.replace("{SPEC_DATA.story_priorities}", format_dict(SPEC_DATA.story_priorities))
  prompt = prompt.replace("{PLAN_DATA.tech_stack}", PLAN_DATA.tech_stack)
  prompt = prompt.replace("{PLAN_DATA.dependencies}", PLAN_DATA.dependencies)
  prompt = prompt.replace("{PLAN_DATA.phases}", format_list(PLAN_DATA.phases))
  prompt = prompt.replace("{PLAN_DATA.adr_decisions}", format_list(PLAN_DATA.adr_decisions))

  RETURN prompt
```

### Configuration Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `artifact_extraction.enabled` | `true` | Enable artifact extraction |
| `artifact_extraction.skip_flag` | `--full-context` | Disable extraction flag |
| `artifact_extraction.spec_fields` | `[fr_list, as_list, ...]` | Fields to extract from spec |
| `artifact_extraction.plan_fields` | `[tech_stack, ...]` | Fields to extract from plan |

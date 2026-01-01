# Parallel Agent Orchestration Instructions

> **For Claude Code**: This section instructs you how to execute subagents defined in `claude_code.subagents` using parallel Task tool calls.

## Overview

When this command defines `claude_code.subagents` in its YAML frontmatter, you MUST execute them using parallel Task tool calls organized into dependency waves.

## Ultrathink Mode Detection

**Activation**: Ultrathink mode is active when BOTH conditions are met:
```yaml
claude_code:
  reasoning_mode: extended      # REQUIRED for ultrathink
  thinking_budget: 8000         # REQUIRED (recommended: 8000-16000)
```

**Ultrathink Behavior**:
- Enables deep reasoning for complex architectural decisions
- Allocates extended thinking time for each subagent
- Uses opus model by default for high-stakes tasks
- Increases wave completion verification rigor

**Detection Logic**:
```text
IF claude_code.reasoning_mode == "extended" AND claude_code.thinking_budget >= 8000:
  ULTRATHINK_MODE = true
  DEFAULT_MODEL = claude_code.model OR "opus"
  LOG "⚡ Ultrathink mode activated (budget: {thinking_budget})"
ELSE:
  ULTRATHINK_MODE = false
  DEFAULT_MODEL = "sonnet"
```

## Model Routing Guidelines

Select models based on task complexity and cost/performance tradeoffs:

| Model | Use For | Thinking Budget | Cost Factor |
|-------|---------|-----------------|-------------|
| **haiku** | Simple tasks: scaffolding, config files, dependency install, file copying | 2000-4000 | 1x (baseline) |
| **sonnet** | Standard tasks: data layer, API building, test generation, documentation | 4000-8000 | 10x |
| **opus** | Complex tasks: architecture decisions, business logic, multi-file refactoring | 8000-16000 | 25x |

**Model Selection by Role Group**:
```text
INFRA → haiku (scaffolding, deps, config)
BACKEND → sonnet/opus (data layer: sonnet, business logic: opus)
FRONTEND → sonnet (UI components, state management)
TESTING → sonnet (test generation, mocking)
REVIEW → sonnet (code review, quality checks)
DOCS → haiku (documentation generation)
```

**Override Priority**:
1. `subagent.model_override` (highest - explicit per-agent)
2. Adaptive routing matrix (complexity_tier × role_group)
3. Role group default (from table above)
4. `claude_code.model` (command default)
5. "sonnet" (fallback)

---

## Adaptive Model Routing

> **Purpose**: Dynamically select the optimal model (haiku/sonnet/opus) for each subagent based on feature complexity and role group, reducing costs by 40-85% for simpler features.

### Step 0: Determine Complexity Tier

Execute BEFORE building waves. Analyze spec.md to determine feature complexity.

```text
FUNCTION determine_complexity_tier(FEATURE_DIR):

  spec_path = "{FEATURE_DIR}/spec.md"

  IF NOT exists(spec_path):
    LOG "⚠️ No spec.md found, defaulting to MODERATE"
    RETURN "MODERATE", 50

  # Count complexity signals
  spec_content = read(spec_path)

  user_story_count = count_pattern(spec_content, "### User Story")
  fr_count = count_pattern(spec_content, "FR-\d{3}")
  as_count = count_pattern(spec_content, "AS-\d")
  api_count = count_pattern(spec_content, "API-\d{3}|PKG-\d{3}")

  # Technical complexity signals
  tech_signals = count_keywords(spec_content, [
    "real-time", "distributed", "cache", "queue", "ML",
    "async", "websocket", "migration", "legacy"
  ])

  # Calculate score (0-100)
  score = 0
  score += min(25, user_story_count * 5)   # Max 25 from stories
  score += min(25, fr_count * 2)            # Max 25 from FRs
  score += min(25, api_count * 8)           # Max 25 from integrations
  score += min(25, tech_signals * 5)        # Max 25 from tech signals

  # Determine tier
  IF score <= 25:     tier = "TRIVIAL"
  ELIF score <= 50:   tier = "SIMPLE"
  ELIF score <= 75:   tier = "MODERATE"
  ELSE:               tier = "COMPLEX"

  LOG "📊 Complexity: {tier} (score: {score}/100)"
  LOG "   Stories: {user_story_count}, FRs: {fr_count}, APIs: {api_count}"

  RETURN tier, score
```

### Step 0.5: Apply Model Routing Matrix

```text
MODEL_ROUTING_MATRIX = {
  "TRIVIAL": {
    "INFRA": "haiku", "BACKEND": "sonnet", "FRONTEND": "haiku",
    "TESTING": "haiku", "REVIEW": "haiku", "DOCS": "haiku"
  },
  "SIMPLE": {
    "INFRA": "haiku", "BACKEND": "sonnet", "FRONTEND": "sonnet",
    "TESTING": "haiku", "REVIEW": "sonnet", "DOCS": "haiku"
  },
  "MODERATE": {
    "INFRA": "haiku", "BACKEND": "opus", "FRONTEND": "sonnet",
    "TESTING": "sonnet", "REVIEW": "opus", "DOCS": "haiku"
  },
  "COMPLEX": {
    "INFRA": "sonnet", "BACKEND": "opus", "FRONTEND": "opus",
    "TESTING": "sonnet", "REVIEW": "opus", "DOCS": "sonnet"
  }
}

FUNCTION apply_model_routing(subagents, complexity_tier):

  assignments = {}

  FOR EACH agent IN subagents:

    # Priority 1: Explicit model_override (skip routing)
    IF agent.model_override IS SET:
      assignments[agent.role] = {model: agent.model_override, reason: "explicit"}
      CONTINUE

    # Priority 2: Matrix lookup by role_group
    role_group = agent.role_group OR "BACKEND"
    selected = MODEL_ROUTING_MATRIX[complexity_tier][role_group]
    agent.model_override = selected
    assignments[agent.role] = {model: selected, reason: "{complexity_tier}/{role_group}"}

  RETURN assignments
```

### Cost Report

Display after routing to show cost savings:

```text
FUNCTION report_routing(assignments, tier, score):

  COSTS = {haiku: 0.001, sonnet: 0.012, opus: 0.060}  # $/agent approx

  haiku_n = count(assignments WHERE model="haiku")
  sonnet_n = count(assignments WHERE model="sonnet")
  opus_n = count(assignments WHERE model="opus")

  adaptive_cost = haiku_n * COSTS.haiku + sonnet_n * COSTS.sonnet + opus_n * COSTS.opus
  opus_cost = len(assignments) * COSTS.opus
  savings = opus_cost - adaptive_cost
  savings_pct = (savings / opus_cost * 100) IF opus_cost > 0 ELSE 0

  PRINT "
🎯 Adaptive Model Routing
├── Complexity: {tier} (score: {score}/100)
├── Models: haiku({haiku_n}) sonnet({sonnet_n}) opus({opus_n})
├── Assignments:"

  FOR role, a IN assignments:
    PRINT "│   └── {role}: {a.model} ({a.reason})"

  PRINT "├── Cost: ${adaptive_cost:.3f} (vs ${opus_cost:.3f} all-opus)
└── Savings: ${savings:.3f} ({savings_pct:.0f}%)
"
```

### Skip Flag

```text
IF "--no-adaptive-model" IN ARGS:
  LOG "⚡ Adaptive routing DISABLED (using template defaults)"
  SKIP Step 0, Step 0.5
```

### Complexity Tier Reference

| Tier | Score | Typical Feature | Default Model Mix |
|------|-------|-----------------|-------------------|
| TRIVIAL | 0-25 | Bug fix, config change | 90% haiku, 10% sonnet |
| SIMPLE | 26-50 | Single component feature | 50% haiku, 40% sonnet, 10% opus |
| MODERATE | 51-75 | Multi-component feature | 30% haiku, 40% sonnet, 30% opus |
| COMPLEX | 76-100 | System-wide change | 10% haiku, 40% sonnet, 50% opus |

---

## Execution Algorithm

### Step 1: Parse Subagents

Extract all subagents from `claude_code.subagents` where `parallel: true`.

For each subagent, capture:
- `role` — unique identifier and Task description
- `prompt` — the task prompt (inject feature context)
- `depends_on` — list of role names that must complete first
- `priority` — lower number = higher priority (default: 5)
- `model_override` — optional model (haiku/sonnet/opus)
- `role_group` — grouping for parallel execution (INFRA, BACKEND, FRONTEND, TESTING, REVIEW)

### Step 2: Build Dependency Waves

Organize subagents into waves using topological sort:

```
Wave 1: Agents with depends_on = [] (no dependencies)
Wave 2: Agents whose depends_on are all in Wave 1
Wave 3: Agents whose depends_on are all in Waves 1-2
...and so on
```

**Constraints**:
- Maximum agents per wave: `orchestration.max_parallel` (default: 3)
- Within a wave, sort by `priority` (lower first)
- If wave exceeds max_parallel, split into sub-waves

### Step 3: Execute Each Wave

For each wave, launch ALL agents in a **SINGLE message** with multiple Task tool calls:

```
Wave 1 Execution:
├── Task(role="project-scaffolder", ...)
├── Task(role="dependency-installer", ...)
└── Task(role="config-generator", ...)
    ↓ (all execute in parallel)
    ↓
[Wait for all Wave 1 agents to complete]
    ↓
Wave 2 Execution:
├── Task(role="data-layer-builder", ...)
├── Task(role="ui-foundation-builder", ...)
└── Task(role="api-builder", ...)
```

**CRITICAL**: To achieve parallelism, ALL Task calls for a wave MUST be in the same response message. Separate messages execute sequentially.

### Step 4: Wave Overlap (Optional)

If `orchestration.wave_overlap.enabled: true`:
- Start Wave N+1 when Wave N reaches `overlap_threshold` (default: 80%)
- Use `run_in_background: true` for background execution
- Check completion with `TaskOutput` before proceeding

## Task Tool Call Pattern

For each subagent, construct a Task call:

```
Task(
  description: "{role}",
  prompt: "{expanded_prompt}",
  subagent_type: "general-purpose",
  model: "{model_override or 'sonnet'}"
)
```

### Prompt Expansion

Expand the subagent's `prompt` with feature context:

```
Feature: {FEATURE_DIR}
Spec: {FEATURE_DIR}/spec.md
Plan: {FEATURE_DIR}/plan.md
Tasks: {FEATURE_DIR}/tasks.md

{original subagent prompt}

Output your results clearly. Report any blockers or issues.
```

## Example: /speckit.implement

The implement command defines 10 subagents across 4 waves:

```yaml
subagents:
  # Wave 1: Infrastructure
  - role: project-scaffolder
    depends_on: []
    priority: 10

  - role: dependency-installer
    depends_on: [project-scaffolder]
    priority: 9

  # Wave 2: Core Implementation
  - role: data-layer-builder
    depends_on: [dependency-installer]
    role_group: BACKEND

  - role: ui-foundation-builder
    depends_on: [dependency-installer]
    role_group: FRONTEND

  - role: api-builder
    depends_on: [data-layer-builder]
    role_group: BACKEND

  - role: ui-feature-builder
    depends_on: [ui-foundation-builder, api-builder]
    role_group: FRONTEND

  # Wave 3: Testing
  - role: unit-test-generator
    depends_on: [data-layer-builder, api-builder]
    role_group: TESTING

  - role: integration-test-generator
    depends_on: [unit-test-generator]
    role_group: TESTING

  # Wave 4: Review
  - role: self-reviewer
    depends_on: [ui-feature-builder, integration-test-generator]
    role_group: REVIEW
```

**Wave Execution Plan**:
1. Wave 1: [project-scaffolder] → then [dependency-installer]
2. Wave 2: [data-layer-builder, ui-foundation-builder] → then [api-builder, ui-feature-builder]
3. Wave 3: [unit-test-generator] → then [integration-test-generator]
4. Wave 4: [self-reviewer]

## Error Handling

**Fail-Fast Mode** (default when `orchestration.fail_fast: true`):
- If any agent in a wave fails, STOP execution
- Report the failure with agent name and error
- Do not proceed to next wave

**Continue Mode**:
- Log failed agents but continue with remaining
- Skip dependent agents whose dependencies failed
- Report all failures at the end

## Progress Reporting

After each wave completes, report:
```
Wave N/M completed:
  ✓ {agent1}: {brief summary}
  ✓ {agent2}: {brief summary}
  ✗ {agent3}: {error if failed}

Proceeding to Wave {N+1}...
```

## Dry Run Mode

When `--dry-run` flag is present, output the execution plan without running:

```
Parallel Execution Plan:
========================
Wave 1 (2 agents):
  - project-scaffolder [priority: 10, model: haiku]
  - config-generator [priority: 9, model: haiku]

Wave 2 (3 agents, max_parallel: 3):
  - data-layer-builder [depends: dependency-installer]
  - ui-foundation-builder [depends: dependency-installer]
  - api-builder [depends: data-layer-builder]

Total: 4 waves, 10 agents
Estimated speedup: 20-30% vs sequential
```

## Configuration Reference

```yaml
claude_code:
  orchestration:
    max_parallel: 3              # Max concurrent agents per wave
    conflict_resolution: queue   # How to handle file conflicts
    timeout_per_agent: 300000    # 5 min timeout per agent (ms)
    retry_on_failure: 1          # Retry failed agents once
    role_isolation: true         # Isolate agent outputs
    wave_overlap:
      enabled: true              # Start next wave at threshold
      skip_flag: "--sequential"  # Flag to disable overlap
      overlap_threshold: 0.80    # 80% completion triggers next wave
      critical_deps_only: true   # Only wait for critical path deps
```

## Wave Status Tracking

During execution, maintain and display wave progress:

### Status Format (per wave)

```text
🌊 Wave {N}/{TOTAL} - {WAVE_NAME}
├── Model: {DEFAULT_MODEL} (ultrathink: {ON|OFF})
├── Agents: {COMPLETED}/{TOTAL} ({PERCENTAGE}%)
├── Status: {RUNNING|COMPLETE|BLOCKED}
│
├── ✓ {agent1} [{model}]: {status} ({duration}s)
├── ✓ {agent2} [{model}]: {status} ({duration}s)
├── ⏳ {agent3} [{model}]: in progress...
└── ⏸ {agent4} [{model}]: waiting for deps
```

### Completion Summary

```text
📊 Orchestration Complete
├── Total Waves: {N}
├── Total Agents: {M}
├── Execution Time: {TOTAL_TIME}s
├── Parallelism Achieved: {PARALLEL_RATIO}x
│
├── Model Usage:
│   ├── haiku: {count} agents ({cost_pct}%)
│   ├── sonnet: {count} agents ({cost_pct}%)
│   └── opus: {count} agents ({cost_pct}%)
│
├── Wave Timing:
│   ├── Wave 1: {time}s ({agents} agents)
│   ├── Wave 2: {time}s ({agents} agents)
│   └── Wave N: {time}s ({agents} agents)
│
└── Estimated Savings: {SAVINGS}% vs sequential
```

### Error Recovery in Ultrathink Mode

When ultrathink mode is active and an agent fails:

```text
IF ULTRATHINK_MODE AND agent.failed:
  # Extended recovery with deep reasoning
  1. Analyze failure root cause with extended thinking
  2. Check if dependencies produced valid output
  3. Attempt retry with increased thinking_budget (+50%)
  4. If retry fails, mark dependents as BLOCKED
  5. Report detailed failure analysis
```

### Live Progress (Background Agents)

For long-running waves with `run_in_background: true`:

```text
EVERY 30 seconds:
  CHECK TaskOutput(agent_id, block=false)
  UPDATE wave status display
  IF wave >= 80% complete AND wave_overlap.enabled:
    TRIGGER next wave start
```

---

## Streaming Output

> **Purpose**: Provide real-time visibility into parallel agent execution. Claude doesn't support true mid-message streaming, so we use **checkpoint-based output** — emitting new progress sections after each significant event.

### Streaming Configuration

```yaml
streaming:
  enabled: true                    # Enable streaming output
  checkpoint_on: agent_complete    # Emit after each agent finishes
  show_progress_bar: true          # Visual progress indicator
  show_running_metrics: true       # Time, tokens, cost
  collapse_completed_waves: true   # Minimize finished waves
```

### Checkpoint Trigger Events

| Event | Action |
|-------|--------|
| Wave start | Emit wave header with agent list |
| Agent complete | Update wave display with ✓/✗ status |
| Wave 80% threshold | Announce overlap trigger (if enabled) |
| Wave complete | Emit summary, collapse wave |
| All waves complete | Emit final orchestration report |

### Streaming Output Format

```text
FUNCTION emit_wave_progress(wave, agents_status, metrics):

  # Progress bar calculation
  completed = count(agents_status WHERE status IN ["success", "failed"])
  total = len(wave.agents)
  pct = (completed / total) * 100
  bar_filled = floor(pct / 5)  # 20 chars total
  bar_empty = 20 - bar_filled

  PRINT "
🌊 Wave {wave.index}/{TOTAL_WAVES} - {wave.name}
├── Progress: [{'█' * bar_filled}{'░' * bar_empty}] {pct:.0f}%
├── Agents: {completed}/{total}
├── Elapsed: {metrics.elapsed}s | Tokens: {metrics.tokens_total:,}
│"

  FOR agent IN wave.agents:
    status = agents_status[agent.role]
    IF status.state == "success":
      PRINT "├── ✓ {agent.role} [{status.model}]: {status.duration}s"
    ELIF status.state == "failed":
      PRINT "├── ✗ {agent.role} [{status.model}]: {status.error}"
    ELIF status.state == "running":
      PRINT "├── ⏳ {agent.role} [{status.model}]: running..."
    ELSE:
      PRINT "├── ⏸ {agent.role}: waiting"

  IF wave.overlap_triggered:
    PRINT "│"
    PRINT "└── 🚀 Overlap threshold reached — Wave {wave.index + 1} started early"
```

### Live Metrics Tracking

```text
METRICS_STATE = {
  start_time: timestamp(),
  tokens_in: 0,
  tokens_out: 0,
  cost_estimate: 0.0,
  agents_completed: 0,
  agents_failed: 0
}

FUNCTION update_metrics(agent_result):
  METRICS_STATE.tokens_in += agent_result.tokens_in
  METRICS_STATE.tokens_out += agent_result.tokens_out
  METRICS_STATE.cost_estimate += calculate_cost(agent_result)

  IF agent_result.success:
    METRICS_STATE.agents_completed += 1
  ELSE:
    METRICS_STATE.agents_failed += 1

FUNCTION calculate_cost(result):
  RATES = {
    haiku: {input: 0.25, output: 1.25},    # per 1M tokens
    sonnet: {input: 3.00, output: 15.00},
    opus: {input: 15.00, output: 75.00}
  }
  rate = RATES[result.model_used]
  RETURN (result.tokens_in * rate.input + result.tokens_out * rate.output) / 1_000_000
```

### Execution Loop with Streaming

```text
FUNCTION execute_wave_with_streaming(wave):

  # 1. Emit wave start
  emit_wave_header(wave)

  # 2. Launch all agents in parallel (single message with multiple Task calls)
  agent_tasks = launch_parallel_agents(wave.agents)

  # 3. Collect results as they complete
  agents_status = {}
  FOR agent IN wave.agents:
    agents_status[agent.role] = {state: "running", model: agent.model}

  WHILE NOT all_complete(agent_tasks):

    # Check for completed agents (non-blocking)
    FOR task IN agent_tasks:
      IF task.completed AND task.role NOT IN agents_status.completed:
        result = get_task_result(task)
        update_metrics(result)
        agents_status[task.role] = {
          state: "success" IF result.success ELSE "failed",
          duration: result.duration_ms / 1000,
          model: result.model_used,
          error: result.error
        }

        # CHECKPOINT: Emit updated progress
        emit_wave_progress(wave, agents_status, METRICS_STATE)

    # Check overlap threshold
    IF wave_overlap.enabled AND wave.completion_ratio >= 0.80:
      IF NOT wave.overlap_triggered:
        wave.overlap_triggered = true
        LOG "🚀 Starting Wave {wave.index + 1} early (80% threshold)"
        # Next wave will be started by orchestrator

  # 4. Emit wave completion summary
  emit_wave_complete(wave, agents_status, METRICS_STATE)
```

### Collapsed Wave Format (After Completion)

After a wave completes, collapse it to save screen space:

```text
<details>
<summary>✅ Wave {N} Complete — {agent_count} agents, {duration}s, ${cost:.3f}</summary>

| Agent | Model | Duration | Status |
|-------|-------|----------|--------|
| {role1} | haiku | 12s | ✓ |
| {role2} | sonnet | 34s | ✓ |
| {role3} | opus | 45s | ✓ |

</details>
```

### Skip Flag

```text
IF "--no-streaming" IN ARGS OR "--quiet" IN ARGS:
  streaming.enabled = false
  LOG "📴 Streaming output disabled"
  # Fall back to batch-mode reporting (existing behavior)
```

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

## Plan Mode Integration Hook

**Trigger:** Before wave execution (after model routing, before Step 1)

```text
FUNCTION orchestrate_with_plan_mode(subagents, feature_dir, user_input, flags):
    """
    Universal orchestration with Plan Mode support.

    Phases:
    - Phase 0: Exploration (depth-dependent, 0-180s)
    - Phase 1: Design (existing waves, context-enriched)
    - Phase 2: Review (depth-dependent, 0-120s)
    - Phase 3: Finalize (quality scoring, handoff)
    """

    # Step 0: Detect depth level
    depth_level, reason = determine_depth_level(
        command=command,
        user_input=user_input,
        spec_path=f"{feature_dir}/spec.md",
        flags=flags
    )

    depth_name = DEPTH_LEVELS[depth_level]["name"]

    IF depth_level == 0:
        LOG f"📝 Depth Level 0 (Standard): ENABLED ({reason})"
        RETURN orchestrate_standard(subagents)

    LOG f"🔍 Depth Level {depth_level} ({depth_name}): ENABLED ({reason})"

    # Phase 0: Exploration (if depth >= 1)
    exploration_findings = None
    IF depth_level >= 1:
        LOG "📂 Phase 0: Exploration"
        exploration_findings = execute_exploration_phase(
            feature_dir=feature_dir,
            user_input=user_input,
            depth_level=depth_level
        )

        IF exploration_findings.failed:
            WARN "Exploration phase failed, falling back to standard mode"
            RETURN orchestrate_standard(subagents)

    # Phase 1: Design (with context injection)
    LOG "📂 Phase 1: Design"
    enriched_subagents = inject_exploration_context(subagents, exploration_findings)
    design_results = orchestrate_standard(enriched_subagents)

    # Phase 2: Review (if depth >= 2)
    IF depth_level >= 2:
        LOG "📂 Phase 2: Review"
        review_results = execute_review_phase(
            feature_dir=feature_dir,
            design_results=design_results,
            depth_level=depth_level
        )

        IF review_results.has_critical_failures:
            BLOCK: Report violations and exit

    # Phase 3: Finalize
    LOG "📂 Phase 3: Finalize"
    finalize_results = execute_finalize_phase(
        feature_dir=feature_dir,
        exploration_findings=exploration_findings,
        review_results=review_results if depth_level >= 2 else None
    )

    RETURN design_results
```

**Details:** See `templates/shared/plan-mode/framework.md` for complete algorithm, agent specifications, and review pass definitions.

**Depth Levels:**
- **Level 0 (Standard)**: Current behavior, no Plan Mode (0% overhead)
- **Level 1 (Lite)**: Quick exploration (2 agents, 90s, +12% time)
- **Level 2 (Moderate)**: Full exploration + constitution review (180s + 30s, +27% time)
- **Level 3 (Full)**: Exploration + 4 review passes (180s + 120s, +42% time)

**Auto-Enable:** Depth level determined by command defaults, complexity tier, and keyword triggers. See `templates/shared/plan-mode/triggers.md`.

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

### Final Token & Cost Summary

**ALWAYS emit at command completion:**

```text
FUNCTION emit_final_token_summary():

  elapsed = timestamp() - METRICS_STATE.start_time
  cost_per_min = (METRICS_STATE.total_cost / elapsed) * 60 IF elapsed > 0 ELSE 0

  PRINT "
══════════════════════════════════════════════════════════════════════════════════
                              📊 TOKEN STATISTICS
══════════════════════════════════════════════════════════════════════════════════

┌────────────┬──────────────┬──────────────┬──────────────┬─────────────────────┐
│ Model      │ Requests     │ Input        │ Output       │ Cost                │
├────────────┼──────────────┼──────────────┼──────────────┼─────────────────────┤
│ opus       │ {METRICS_STATE.by_model.opus.requests:>10} │ {METRICS_STATE.by_model.opus.tokens_in:>10,} │ {METRICS_STATE.by_model.opus.tokens_out:>10,} │ ${METRICS_STATE.by_model.opus.cost:>15.4f} │
│ sonnet     │ {METRICS_STATE.by_model.sonnet.requests:>10} │ {METRICS_STATE.by_model.sonnet.tokens_in:>10,} │ {METRICS_STATE.by_model.sonnet.tokens_out:>10,} │ ${METRICS_STATE.by_model.sonnet.cost:>15.4f} │
│ haiku      │ {METRICS_STATE.by_model.haiku.requests:>10} │ {METRICS_STATE.by_model.haiku.tokens_in:>10,} │ {METRICS_STATE.by_model.haiku.tokens_out:>10,} │ ${METRICS_STATE.by_model.haiku.cost:>15.4f} │
├────────────┼──────────────┼──────────────┼──────────────┼─────────────────────┤
│ TOTAL      │ {METRICS_STATE.agents_completed:>10} │ {METRICS_STATE.total_tokens_in:>10,} │ {METRICS_STATE.total_tokens_out:>10,} │ ${METRICS_STATE.total_cost:>15.4f} │
└────────────┴──────────────┴──────────────┴──────────────┴─────────────────────┘

⏱️  Duration: {elapsed:.1f}s | 💰 Cost/min: ${cost_per_min:.4f}

══════════════════════════════════════════════════════════════════════════════════
"
```

**Integration Point:**

```text
AT command_complete:
  # 1. Emit orchestration summary (existing)
  emit_orchestration_summary()

  # 2. ALWAYS emit token statistics
  emit_final_token_summary()

  # 3. Continue to handoff
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
├── Elapsed: {metrics.elapsed}s | Tokens: {METRICS_STATE.total_tokens_in + METRICS_STATE.total_tokens_out:,} | Cost: ${METRICS_STATE.total_cost:.4f}
│"

  FOR agent IN wave.agents:
    status = agents_status[agent.role]
    IF status.state == "success":
      # Display with token stats
      PRINT "├── ✓ {agent.role} [{status.model}]: {status.duration}s | 📊 +{status.tokens_in:,} in / +{status.tokens_out:,} out | ${status.cost:.4f}"
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

### Token Streaming Display

After EACH agent completes, display inline token statistics:

```text
FUNCTION emit_agent_token_stats(agent_result):
  cost = calculate_cost(agent_result.model_used, agent_result.tokens_in, agent_result.tokens_out)

  PRINT "   📊 {agent_result.role}: +{agent_result.tokens_in:,} in / +{agent_result.tokens_out:,} out | ${cost:.4f}"
```

After EACH wave completes, display wave token summary:

```text
FUNCTION emit_wave_token_summary(wave_index, wave_tokens_in, wave_tokens_out, wave_cost, wave_duration):

  PRINT "
══════════════════════════════════════════════════════════════════════════════
📊 Wave {wave_index} Complete | Tokens: {wave_tokens_in + wave_tokens_out:,} | Cost: ${wave_cost:.4f} | Time: {wave_duration:.1f}s
══════════════════════════════════════════════════════════════════════════════
"

  # Store in history
  METRICS_STATE.waves.append({
    wave_id: wave_index,
    tokens_in: wave_tokens_in,
    tokens_out: wave_tokens_out,
    cost: wave_cost,
    duration: wave_duration
  })
```

### Live Metrics Tracking

```text
MODEL_RATES = {  # per 1M tokens (USD)
  haiku:  { input: 0.25,  output: 1.25  },
  sonnet: { input: 3.00,  output: 15.00 },
  opus:   { input: 15.00, output: 75.00 }
}

METRICS_STATE = {
  start_time: timestamp(),

  # Per-model breakdown
  by_model: {
    opus:   { tokens_in: 0, tokens_out: 0, requests: 0, cost: 0.0 },
    sonnet: { tokens_in: 0, tokens_out: 0, requests: 0, cost: 0.0 },
    haiku:  { tokens_in: 0, tokens_out: 0, requests: 0, cost: 0.0 }
  },

  # Totals
  total_tokens_in: 0,
  total_tokens_out: 0,
  total_cost: 0.0,

  # Tracking
  agents_completed: 0,
  agents_failed: 0,

  # Per-wave history
  waves: []  # [{wave_id, tokens_in, tokens_out, cost, duration}]
}

FUNCTION calculate_cost(model, tokens_in, tokens_out):
  rate = MODEL_RATES[model]
  RETURN (tokens_in * rate.input + tokens_out * rate.output) / 1_000_000

FUNCTION update_metrics(agent_result):
  model = agent_result.model_used  # "opus" | "sonnet" | "haiku"
  cost = calculate_cost(model, agent_result.tokens_in, agent_result.tokens_out)

  # Update per-model stats
  METRICS_STATE.by_model[model].tokens_in += agent_result.tokens_in
  METRICS_STATE.by_model[model].tokens_out += agent_result.tokens_out
  METRICS_STATE.by_model[model].requests += 1
  METRICS_STATE.by_model[model].cost += cost

  # Update totals
  METRICS_STATE.total_tokens_in += agent_result.tokens_in
  METRICS_STATE.total_tokens_out += agent_result.tokens_out
  METRICS_STATE.total_cost += cost

  # Update counts
  IF agent_result.success:
    METRICS_STATE.agents_completed += 1
  ELSE:
    METRICS_STATE.agents_failed += 1

  RETURN cost  # For inline display
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

---

## Operation Batching

> **Purpose**: Batch independent operations (file reads, searches, validations) into parallel calls within a **single message**, reducing API round-trips across all commands.

### Batching Hierarchy

```text
┌─────────────────────────────────────────────────────────────────┐
│ Level 0: Operation Batching (cross-command)                     │
│   - Context reads: batch file reads before processing           │
│   - Searches: batch Explore agents                              │
│   - Validations: batch QG/inline gate checks                    │
│   - Controlled by: operation_batching.strategies                │
├─────────────────────────────────────────────────────────────────┤
│ Level 1: Wave Parallelism (subagent-level)                      │
│   - Agents in same wave execute in parallel                     │
├─────────────────────────────────────────────────────────────────┤
│ Level 2: Task Batching (task-level, implement.md only)          │
│   - Tasks grouped by dependencies                               │
└─────────────────────────────────────────────────────────────────┘
```

### Configuration

```yaml
operation_batching:
  enabled: true
  skip_flag: "--sequential"
  framework: templates/shared/operation-batching.md
  strategies:
    context_reads: true    # Batch file reads
    searches: true         # Batch Explore agents
    validations: true      # Batch QG checks
    prefetch: true         # Speculative parallel load
```

### Core Algorithms

#### CONTEXT_BATCH

```text
# Batch multiple file reads
CONTEXT = CONTEXT_BATCH([
  "memory/constitution.md",
  "templates/spec-template.md",
  "{FEATURE_DIR}/spec.md"
])

# Result: Single message with multiple Read calls → 3x faster
```

#### SEARCH_BATCH

```text
# Batch multiple searches
RESULTS = SEARCH_BATCH([
  "Find architecture patterns in codebase",
  "Search for existing API patterns",
  "Find database schema patterns"
])

# Result: Single message with multiple Explore agents → 3x faster
```

#### VALIDATE_BATCH

```text
# Batch inline gate checks
VALIDATION = VALIDATE_BATCH([
  {id: "IG-SPEC-001", check: constitution_alignment},
  {id: "IG-SPEC-002", check: ambiguity_detection},
  {id: "IG-SPEC-003", check: fr_as_coverage}
])

# Result: Parallel validation → faster gate checking
```

### Command-Specific Batching

| Command | Batching Strategy |
|---------|-------------------|
| `/speckit.specify` | Context reads + prefetch |
| `/speckit.plan` | Context reads + research searches |
| `/speckit.tasks` | Context reads + parallel mappers |
| `/speckit.clarify` | Gap search batch |
| `/speckit.design` | Design context pre-cache |
| `/speckit.implement` | Task-level batching (see below) |

### Performance Impact

| Mode | Round-trips | Savings |
|------|-------------|---------|
| Sequential reads (4 files) | 4 | baseline |
| Batched reads (4 files) | 1 | 4x faster |
| Sequential searches (3 queries) | 3 | baseline |
| Batched searches (3 queries) | 1 | 3x faster |

### Skip Flag

```text
IF "--sequential" IN ARGS:
  operation_batching.enabled = false
  LOG "⚠️ Operation batching DISABLED (sequential mode)"
```

See `templates/shared/operation-batching.md` for full framework.

---

## Task-Level Batching

> **Purpose**: While subagent-level parallelism executes agents within waves in parallel, **task-level batching** groups individual tasks from tasks.md into batches and executes them as parallel Task tool calls in a **single message**, achieving maximum parallelism.

### Parallelism Hierarchy

```text
┌─────────────────────────────────────────────────────────────────┐
│ Level 1: Wave Parallelism (subagent-level)                     │
│   - Agents in same wave execute in parallel                    │
│   - Sequential across waves (Wave 1 → Wave 2 → ...)            │
│   - Controlled by: orchestration.max_parallel                  │
├─────────────────────────────────────────────────────────────────┤
│ Level 2: Task Batching (task-level) ← NEW                      │
│   - Tasks within agent execution grouped by dependencies       │
│   - Independent tasks → single message with multiple Task calls│
│   - Controlled by: orchestration.task_batching                 │
└─────────────────────────────────────────────────────────────────┘
```

### Configuration

```yaml
task_batching:
  enabled: true
  skip_flag: "--sequential-tasks"
  max_batch_size: 8                     # Max tasks per batch
  batch_by: dependency_level            # Topological grouping
  file_conflict_resolution: queue       # Same-file → next batch
```

### Integration with Subagent Execution

When a subagent receives tasks to execute:

```text
FUNCTION execute_subagent_with_batching(agent, tasks):

  IF NOT task_batching.enabled OR "--sequential-tasks" IN ARGS:
    # Fallback: sequential execution
    FOR task IN tasks:
      execute_task(task)
    RETURN

  # Apply batching
  batches = BATCH_TASKS(tasks)

  LOG "📦 Batching: {len(tasks)} tasks → {len(batches)} batches"

  FOR batch IN batches:
    # CRITICAL: All Task calls in SINGLE message
    results = EXECUTE_BATCH_PARALLEL(batch)
    update_tasks_md(results)
```

### Performance Impact

| Mode | Round-trips | Time | Savings |
|------|-------------|------|---------|
| Sequential tasks | N (per task) | ~10 min | baseline |
| Batched (4-8 per batch) | N/4-8 | ~2-3 min | 60-75% |

### Batching Algorithm Summary

1. **Parse tasks.md** → extract task IDs, dependencies, target files
2. **Build dependency graph** → topological sort
3. **Group by level** → tasks at same level are independent
4. **Split by file conflicts** → same-file tasks in different batches
5. **Execute batches** → parallel Task calls per batch

See `templates/shared/implement/task-batching.md` for full algorithm.

### Batch Output Format

```text
📦 Batch 1/4 (3 tasks)
├── T001 [haiku]: Create project scaffold
├── T002 [haiku]: Install dependencies
└── T003 [sonnet]: Configure database

⏳ Executing batch in parallel...

✓ Batch 1/4 complete (2.3s)
├── ✓ T001: Created 5 files
├── ✓ T002: Installed 12 packages
└── ✓ T003: Configured PostgreSQL
```

### Skip Flag

```text
IF "--sequential-tasks" IN ARGS:
  task_batching.enabled = false
  LOG "⚠️ Task batching DISABLED (sequential mode)"
```

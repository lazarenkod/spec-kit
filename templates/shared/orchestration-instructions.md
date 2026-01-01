# Parallel Agent Orchestration Instructions

> **For Claude Code**: This section instructs you how to execute subagents defined in `claude_code.subagents` using parallel Task tool calls.

## Overview

When this command defines `claude_code.subagents` in its YAML frontmatter, you MUST execute them using parallel Task tool calls organized into dependency waves.

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

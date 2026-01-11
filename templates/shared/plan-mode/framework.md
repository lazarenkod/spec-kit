# Plan Mode Framework

> **Version**: 1.0.0
> **Status**: Active
> **Applies to**: All Spec Kit commands with `plan_mode.enabled: auto`

## Overview

The Plan Mode Framework enhances Spec Kit commands with the same level of logic and research depth as Claude Code's Plan Mode. It adds **exploration** and **review** phases to existing workflows, with 4 configurable depth levels.

**Problems Solved:**
- ❌ **Insufficient research**: Commands commit to first approach without exploring alternatives
- ❌ **Missing edge cases**: Edge cases discovered during implementation, not proactively in spec

**Solution:**
- ✅ **Phase 0: Exploration** — Research agents analyze patterns, alternatives, and constraints
- ✅ **Phase 2: Review** — Validation passes check constitution, completeness, edge cases, testability
- ✅ **Context injection**: Exploration findings enrich existing wave execution

---

## Depth Level System

### Levels Overview

| Level | Name | Exploration | Review | Time | Cost | Auto-Enable |
|-------|------|-------------|--------|------|------|-------------|
| **0** | Standard | None | None | +0% | +0% | TRIVIAL, SIMPLE |
| **1** | Lite | 2 agents (90s) | None | +12% | +1% | MODERATE* |
| **2** | Moderate | 4 agents (180s) | 1 pass (30s) | +27% | +6% | COMPLEX* |
| **3** | Full | 4 agents (180s) | 4 passes (120s) | +42% | +12% | Manual only |

*Default varies by command (see per-command defaults below)

### Per-Command Depth Defaults

```yaml
COMMAND_DEPTH_DEFAULTS = {
  "speckit.plan": {
    TRIVIAL: 0,     # 0-25: Standard
    SIMPLE: 0,      # 26-50: Standard
    MODERATE: 1,    # 51-70: Lite
    COMPLEX: 2      # 71+: Moderate
  },
  "speckit.specify": {
    TRIVIAL: 0,
    SIMPLE: 0,
    MODERATE: 1,
    COMPLEX: 2
  },
  "speckit.tasks": {
    TRIVIAL: 0,
    SIMPLE: 0,
    MODERATE: 0,    # tasks is fast, stay at standard
    COMPLEX: 1      # lite only for COMPLEX
  },
  "speckit.concept": {
    TRIVIAL: 0,
    SIMPLE: 1,      # concept benefits from exploration even for SIMPLE
    MODERATE: 2,
    COMPLEX: 3      # Full depth for COMPLEX concepts
  },
  "speckit.implement": {
    TRIVIAL: 0,
    SIMPLE: 0,
    MODERATE: 0,    # implement is long, minimize overhead
    COMPLEX: 1      # lite only
  }
}
```

### Detection Algorithm

```python
def determine_depth_level(command, user_input, spec_path, flags):
    """
    Determine the Plan Mode depth level to use.

    Priority Order:
    1. Explicit --depth-level flag (highest priority)
    2. Backward compat flags (--plan-mode, --no-plan-mode)
    3. Keyword triggers (upgrade by +1 level)
    4. Complexity-based default for this command

    Returns:
        (level: int, reason: str)
    """

    # Priority 1: Explicit --depth-level flag
    if "--depth-level" in flags:
        level = parse_int(flags["--depth-level"], min=0, max=3)
        if level < 0 or level > 3:
            raise ValueError(f"--depth-level must be 0-3, got {level}")
        return level, f"explicit flag (--depth-level {level})"

    # Priority 2: Backward compat flags
    if "--plan-mode" in flags:
        return 3, "explicit flag (--plan-mode → depth 3)"
    if "--no-plan-mode" in flags:
        return 0, "explicit flag (--no-plan-mode → depth 0)"

    # Priority 3: Complexity-based default for this command
    complexity_tier = calculate_complexity_tier(spec_path)
    default_level = COMMAND_DEPTH_DEFAULTS[command][complexity_tier]

    # Priority 4: Keyword triggers (upgrade to next level)
    keywords = [
        "distributed", "multi-service", "migration",
        "security-critical", "real-time", "high-availability",
        "microservices", "event-driven", "data-intensive"
    ]
    for kw in keywords:
        if kw in user_input.lower():
            upgraded_level = min(default_level + 1, 3)
            if upgraded_level > default_level:
                return upgraded_level, f"keyword trigger '{kw}' (upgraded from {default_level} to {upgraded_level})"

    return default_level, f"default for {command}/{complexity_tier}"
```

---

## Orchestration Algorithm

### Main Workflow

```python
FUNCTION orchestrate_with_plan_mode(command, subagents, feature_dir, user_input, flags):
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

### Integration Point

**File:** `orchestration-instructions.md`
**Line:** 206 (before "## Execution Algorithm")

**Insert:**

```markdown
---

## Plan Mode Integration Hook

**Trigger:** Before wave execution (after model routing, before Step 1)

See `templates/shared/plan-mode/framework.md` for complete algorithm.

```text
FUNCTION orchestrate_with_plan_mode(subagents, feature_dir, user_input, flags):
    # Detect depth level
    depth_level, reason = determine_depth_level(...)

    # Phase 0: Exploration (depth >= 1)
    IF depth_level >= 1:
        exploration_findings = execute_exploration_phase(...)

    # Phase 1: Design (context-enriched)
    enriched_subagents = inject_exploration_context(subagents, exploration_findings)
    design_results = orchestrate_standard(enriched_subagents)

    # Phase 2: Review (depth >= 2)
    IF depth_level >= 2:
        review_results = execute_review_phase(...)
        IF review_results.has_critical_failures:
            BLOCK

    # Phase 3: Finalize
    finalize_results = execute_finalize_phase(...)

    RETURN design_results
```

**Details:** See `templates/shared/plan-mode/framework.md`
```

---

## Context Injection

### Mechanism

```python
def inject_exploration_context(base_prompt, research_md):
    """
    Prepend exploration findings to agent prompts.

    Args:
        base_prompt: Original agent prompt
        research_md: Output from exploration phase (or None if depth 0)

    Returns:
        Enriched prompt with exploration context
    """
    if not research_md:
        return base_prompt

    context = f"""

## 🔍 Plan Mode: Exploration Findings

**Existing Patterns:**
{research_md.patterns_summary}

**Recommended Approach:**
{research_md.recommended_approach} (scored {research_md.score}/25)

**Key Constraints:**
{research_md.constraints_summary}

**Edge Cases to Address:**
{research_md.edge_cases}

**Rationale:**
{research_md.rationale_summary}

---

**Instructions:** Consider these findings when generating your artifact. Align with recommended approach unless there's a strong reason to deviate (document reasoning).

"""
    return base_prompt + context
```

### Effect

Agents in Wave 1-N receive pre-researched context → generate better artifacts without additional time cost in wave execution (time is spent upfront in exploration phase).

---

## Quality Metrics

### Aggregate Quality Score

```python
def calculate_aggregate_quality_score(command, artifacts):
    """
    Calculate quality score based on command type.

    Scores:
    - /speckit.plan: PQS (Plan Quality Score, 0-100)
    - /speckit.specify: SQS (Spec Quality Score, 0-100)
    - /speckit.concept: CQS (Concept Quality Score, 0-120)
    - /speckit.tasks: Task Quality Score (0-100)

    Threshold: ≥80 for PASS (≥96 for CQS)
    """
    if command == "speckit.plan":
        return calculate_pqs(artifacts["plan.md"])
    elif command == "speckit.specify":
        return calculate_sqs(artifacts["spec.md"])
    elif command == "speckit.concept":
        return calculate_cqs(artifacts["concept.md"])
    elif command == "speckit.tasks":
        return calculate_task_quality(artifacts["tasks.md"])
    else:
        return 100  # No scoring for other commands
```

### Gate Enforcement

```python
def enforce_quality_gate(score, threshold, complexity_tier):
    """
    Enforce quality gate PM-006.

    Rules:
    - COMPLEX: Score must be >= threshold (BLOCK if not)
    - MODERATE/SIMPLE/TRIVIAL: WARN only
    """
    if score >= threshold:
        return "PASS"

    if complexity_tier == "COMPLEX":
        raise QualityGateViolation(f"PM-006: Score {score} < {threshold}")
    else:
        WARN f"PM-006: Score {score} < {threshold} (non-blocking for {complexity_tier})"
        return "WARN"
```

---

## Performance Budget

### By Depth Level

| Component | L0 | L1 | L2 | L3 |
|-----------|----|----|----|----|
| Complexity calc | 0.5s | 0.5s | 0.5s | 0.5s |
| Model routing | 0.1s | 0.1s | 0.1s | 0.1s |
| Depth detect | — | 0.2s | 0.2s | 0.2s |
| **Exploration** | — | **90s** | **180s** | **180s** |
| Wave execution | 780s | 750s | 600s* | 600s* |
| **Review** | — | — | **30s** | **120s** |
| Finalize | 60s | 70s | 80s | 90s |
| **TOTAL** | **780s** | **870s** | **990s** | **1110s** |
| **Delta** | — | **+12%** | **+27%** | **+42%** |

*Wave execution time reduced because exploration context prevents iterations

### Cost Breakdown

| Level | Exploration | Review | Total | Delta |
|-------|-------------|--------|-------|-------|
| L0 | $0 | $0 | $0.60 | — |
| L1 | $0.006 (2 haiku) | $0 | $0.606 | +1% |
| L2 | $0.021 (3 haiku + 1 sonnet) | $0.012 (1 sonnet) | $0.633 | +6% |
| L3 | $0.021 | $0.048 (4 sonnet) | $0.669 | +12% |

---

## CLI Flags

### Flag Definitions

```yaml
flags:
  depth_level:
    name: "--depth-level"
    type: int
    range: [0, 3]
    default: auto
    description: "Override depth level (0=Standard, 1=Lite, 2=Moderate, 3=Full)"
    priority: 1

  plan_mode:
    name: "--plan-mode"
    type: bool
    default: false
    description: "Enable full Plan Mode (alias for --depth-level 3)"
    priority: 2
    alias_for: "--depth-level 3"

  no_plan_mode:
    name: "--no-plan-mode"
    type: bool
    default: false
    description: "Disable Plan Mode (alias for --depth-level 0)"
    priority: 2
    alias_for: "--depth-level 0"
```

### Usage Examples

```bash
# Auto-enable based on complexity (default)
/speckit.plan

# Force specific depth level
/speckit.plan --depth-level 1  # Lite
/speckit.plan --depth-level 3  # Full

# Backward compat (v0.3.x style)
/speckit.plan --plan-mode       # → depth 3
/speckit.plan --no-plan-mode    # → depth 0

# Force disable even for COMPLEX
/speckit.specify --depth-level 0
/speckit.specify --no-plan-mode  # Same as above
```

---

## Error Handling

### Exploration Failure

```python
def handle_exploration_failure(error, feature_dir):
    """
    Gracefully fallback to standard mode if exploration fails.
    """
    LOG f"⚠️ Exploration phase failed: {error}"
    LOG "Falling back to Standard mode (depth 0)"

    # Remove partial research.md if it exists
    research_path = f"{feature_dir}/research.md"
    if os.path.exists(research_path):
        os.remove(research_path)

    # Continue with standard orchestration
    return None  # No exploration findings
```

### Review Failure

```python
def handle_review_failure(review_pass, severity, error):
    """
    Block on CRITICAL, warn on others.
    """
    if severity == "CRITICAL":
        raise QualityGateViolation(f"Review pass '{review_pass}' FAILED: {error}")
    else:
        WARN f"Review pass '{review_pass}' FAILED: {error} (non-blocking)"
```

---

## References

- Exploration Phase: `templates/shared/plan-mode/exploration-phase.md`
- Review Phase: `templates/shared/plan-mode/review-phase.md`
- Triggers: `templates/shared/plan-mode/triggers.md`
- Quality Gates: `memory/domains/quality-gates.md` (PM-001 to PM-006)
- Complexity Scoring: `templates/shared/complexity-scoring.md`
- Orchestration: `templates/shared/orchestration-instructions.md`

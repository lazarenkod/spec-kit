# Adaptive Model Selection Framework

## Purpose

General-purpose framework for cost-optimized Claude model selection across all SpecKit commands. Enables intelligent routing between Haiku, Sonnet, and Opus based on task complexity while preserving quality.

## Philosophy

**Quality-First Optimization**: Reduce costs only where reasoning complexity allows, never compromise on quality gates or critical decision points.

## Model Characteristics

| Model | Cost (Input/Output per 1M tokens) | Speed | Best For |
|-------|-----------------------------------|-------|----------|
| **Haiku** | $0.25 / $1.25 | 4x faster | Template-based, mechanical, simple orchestration |
| **Sonnet** | $3.00 / $15.00 | Baseline | Standard reasoning, quality gates, structured tasks |
| **Opus** | $15.00 / $75.00 | Baseline | Strategic decisions, architecture, complex analysis |

## Cost Optimization Principles

### ✅ Safe to Downgrade

Commands/tasks with these characteristics can use cheaper models:

1. **Template-based operations**
   - Mechanical conversion (tasks → GitHub issues)
   - Schema-driven generation (copying feature lineage)
   - Pattern-based output (checklists from templates)

2. **Bounded scope**
   - Single-entity CRUD specifications
   - Static mockup generation
   - File listing and registry display

3. **No critical decision-making**
   - Context gathering (loading parent specs)
   - Parsing and extraction (entity detection)
   - Validation against fixed rules (syntax checking)

### ❌ Cannot Downgrade

Commands/tasks requiring full reasoning capacity:

1. **Quality gates**
   - SQS/CQS calculation (multi-dimensional scoring)
   - Cross-artifact consistency validation
   - Security and accessibility audits

2. **Architectural decisions**
   - Trade-off analysis (performance vs maintainability)
   - Technology selection (framework, database, hosting)
   - System design patterns

3. **Strategic reasoning**
   - Market research and competitive analysis
   - Product discovery and validation
   - Complex dependency graph construction

4. **Multi-pass analysis**
   - Ambiguity detection (heuristic + metacognitive)
   - Self-review with anti-pattern detection
   - Iterative refinement loops

## Adaptive Routing Patterns

### Pattern 1: Complexity-Based Routing

**Use case**: Commands where task complexity varies significantly

**Example**: `/speckit.specify` (simple CRUD vs complex system-wide features)

```yaml
adaptive_model:
  enabled: true
  complexity_framework: templates/shared/specify/complexity-detection.md
  tier_routing:
    SIMPLE:
      orchestrator: sonnet
      thinking_budget: 8000
    MODERATE:
      orchestrator: sonnet
      thinking_budget: 12000
    COMPLEX:
      orchestrator: opus
      thinking_budget: 16000
```

**Savings**: 30-50% for simple features, 0% for complex features

### Pattern 2: Mode-Based Routing

**Use case**: Commands with distinct operational modes

**Example**: `/speckit.preview` (static vs interactive vs animated)

```yaml
adaptive_model:
  enabled: true
  mode_detection: true
  mode_routing:
    static_mockup:
      orchestrator: haiku
      thinking_budget: 4000
    interactive_preview:
      orchestrator: sonnet
      thinking_budget: 8000
    animated_preview:
      orchestrator: opus
      thinking_budget: 16000
```

**Savings**: 40-60% for static mockups, 0-20% for interactive

### Pattern 3: Phase-Based Routing

**Use case**: Commands with sequential phases of varying complexity

**Example**: `/speckit.implement` (setup → core → tests → docs)

```yaml
phases:
  setup:
    model: haiku
    thinking_budget: 2000
  core:
    model: opus
    thinking_budget: 10000
  tests:
    model: sonnet
    thinking_budget: 4000
  docs:
    model: haiku
    thinking_budget: 2000
```

**Savings**: 60-70% overall through phase optimization

### Pattern 4: Role-Based Routing

**Use case**: Multi-agent workflows with specialized roles

**Example**: `/speckit.extend` (context loading vs validation)

```yaml
subagents:
  - role: context-loader
    role_group: ANALYSIS
    model_override: haiku  # Mechanical copying
  - role: extension-planner
    role_group: ANALYSIS
    model_override: sonnet  # Quality gate
```

**Savings**: 50% for mechanical roles

## Implementation Guide

### Step 1: Add Adaptive Configuration

In command YAML front-matter:

```yaml
claude_code:
  model: opus  # Default model, overridden by adaptive selection
  adaptive_model:
    enabled: true
    # Choose pattern: complexity_framework OR mode_detection OR phase_routing
    complexity_framework: templates/shared/{command}/complexity-detection.md
    tier_routing:
      TIER_1:
        orchestrator: haiku|sonnet|opus
        thinking_budget: 4000-16000
      TIER_2: ...
    override_flag: "--model"  # User override
```

### Step 2: Add Detection Logic

In command workflow (typically Step 0):

```text
## Step 0: Detect Complexity/Mode

IF adaptive_model.enabled = true AND --model flag not present:

  # Load detection framework
  READ adaptive_model.complexity_framework

  # Run detection algorithm
  EXECUTE detection_algorithm → TIER, SCORE, RECOMMENDED_MODEL

  # Apply routing
  ORCHESTRATOR_MODEL = adaptive_model.tier_routing[TIER].orchestrator
  THINKING_BUDGET = adaptive_model.tier_routing[TIER].thinking_budget

  # Display cost savings
  DISPLAY:
  ┌─────────────────────────────────────────┐
  │ Tier:     {TIER}                        │
  │ Model:    {ORCHESTRATOR_MODEL}          │
  │ Savings:  {SAVINGS}%                    │
  └─────────────────────────────────────────┘
```

### Step 3: Apply Subagent Overrides

```text
# If tier-specific subagent overrides exist
IF adaptive_model.subagent_overrides[TIER]:
  FOR EACH subagent IN workflow:
    IF subagent.role IN adaptive_model.subagent_overrides[TIER]:
      subagent.model_override = adaptive_model.subagent_overrides[TIER][subagent.role]
```

### Step 4: Quality Preservation

**Critical**: Ensure quality gates remain intact:

```yaml
# Example: Specification quality gate
pre_handoff_action:
  gates:
    - name: "SQS Gate"
      threshold: 80
      # Quality gate applies REGARDLESS of model used
      # If sonnet-generated spec fails → auto-remediate or escalate
```

## Cost Tracking

### Display Format

```text
┌─────────────────────────────────────────────────┐
│ Model Selection Summary                         │
├─────────────────────────────────────────────────┤
│ Complexity:     SIMPLE (35/100)                 │
│ Model:          sonnet                          │
│                                                 │
│ Cost Estimate:                                  │
│   Orchestrator: $0.08 (sonnet)                  │
│   Subagents:    $0.12 (mixed)                   │
│   Total:        $0.20                           │
│                                                 │
│ vs. All-Opus:   $0.50                           │
│ Savings:        $0.30 (60%)                     │
│                                                 │
│ Expected time:  30-60s                          │
└─────────────────────────────────────────────────┘
```

### Tracking File

Store per-feature cost data:

```yaml
# .speckit/cost-tracking.yaml
features:
  - id: "001-login"
    commands:
      - name: specify
        model: sonnet
        tier: SIMPLE
        cost_actual: $0.18
        cost_baseline: $0.50
        savings: 64%
      - name: implement
        model: adaptive
        tier: SIMPLE
        cost_actual: $6.20
        cost_baseline: $18.50
        savings: 66%
    total_cost: $6.38
    total_baseline: $19.00
    total_savings: 66%
```

## Examples by Command Type

### High-Complexity Commands (Keep Opus Default)

```yaml
# /speckit.concept - Market research, strategic reasoning
claude_code:
  model: opus
  # No adaptive_model - always opus for quality
```

### Variable-Complexity Commands (Enable Adaptive)

```yaml
# /speckit.specify - Ranges from simple CRUD to complex system-wide
claude_code:
  model: opus
  adaptive_model:
    enabled: true
    complexity_framework: templates/shared/specify/complexity-detection.md
```

### Low-Complexity Commands (Downgrade to Haiku/Sonnet)

```yaml
# /speckit.taskstoissues - Template-based conversion
claude_code:
  model: haiku  # Always haiku, no adaptive needed
```

## Override Flags

All commands support user overrides:

```bash
# Force specific model
/speckit.specify --model=haiku     # Use haiku (risky for complex features)
/speckit.specify --model=sonnet    # Use sonnet
/speckit.specify --model=opus      # Disable adaptive, force opus

# Control adaptive behavior
/speckit.implement --no-adaptive-model    # Disable adaptive, use default
/speckit.implement --tier=COMPLEX         # Force complexity tier
```

## Quality Assurance

### Validation After Optimization

After implementing adaptive routing, validate:

1. **Quality gate pass rates**
   ```bash
   # Run analyze on adaptively-generated specs
   /speckit.analyze --profile=spec_validate
   # Ensure SQS >= 80 maintained
   ```

2. **User satisfaction**
   - Track rework requests (indication of quality degradation)
   - Monitor spec clarity scores
   - Collect feedback on generated artifacts

3. **Cost vs quality trade-off**
   ```
   Acceptable: 60% cost reduction, 95% quality retention
   Unacceptable: 80% cost reduction, 70% quality retention
   ```

### Rollback Strategy

If quality degrades:

1. **Per-command rollback**
   ```yaml
   adaptive_model:
     enabled: false  # Revert to default opus
   ```

2. **Per-tier adjustment**
   ```yaml
   tier_routing:
     SIMPLE:
       orchestrator: sonnet  # Was haiku, upgraded to sonnet
   ```

3. **Increase thresholds**
   ```yaml
   # Make SIMPLE tier harder to trigger
   complexity_detection:
     thresholds:
       SIMPLE: 0-30  # Was 0-40
   ```

## Future Enhancements

### Calibration Loop

Track actual outcomes to refine routing:

```yaml
# .speckit/calibration-data.yaml
models:
  - command: specify
    predicted_tier: SIMPLE
    actual_effort: MODERATE  # Took longer than expected
    model_used: sonnet
    quality_score: 72  # Below threshold
    recommendation: "Increase SIMPLE threshold or upgrade to opus"
```

### Cost Budget Mode

```bash
# Global cost control
/speckit.specify --budget=low     # Aggressive haiku usage
/speckit.specify --budget=medium  # Balanced (default adaptive)
/speckit.specify --budget=high    # Conservative opus preference
```

### Per-Project Defaults

```yaml
# constitution.md
model_preferences:
  default_tier: MODERATE  # Bias towards higher quality
  cost_optimization: balanced  # low | balanced | quality-first
  override_adaptive:
    specify: opus  # Always opus for this project
    implement: adaptive  # Keep adaptive for implement
```

## Summary

**Adaptive model selection enables 30-70% cost savings** on appropriate commands while preserving quality through:

1. **Complexity/mode detection** - Route to appropriate model tier
2. **Subagent optimization** - Mix models within workflows
3. **Quality gate preservation** - Never compromise validation thresholds
4. **User overrides** - Allow manual control when needed
5. **Cost tracking** - Measure actual savings vs baseline

**Golden Rule**: When in doubt, use opus. Cost savings are worthless if quality degrades.

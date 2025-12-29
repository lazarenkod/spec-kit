# Complexity-Based Model Selection

## Purpose

Automatically select the appropriate model (haiku/sonnet/opus) based on feature complexity tier to optimize cost and speed without sacrificing quality.

## Performance Impact

| Complexity | Default Model | Optimized | Cost Savings | Speed Gain |
|------------|---------------|-----------|--------------|------------|
| TRIVIAL | opus | haiku | 90% | 4x faster |
| SIMPLE | opus | sonnet/haiku | 60-80% | 2-3x faster |
| MODERATE | opus | opus | 0% | baseline |
| COMPLEX | opus | opus | 0% | baseline |

## Configuration

```yaml
model_selection:
  enabled: true
  skip_flag: "--no-adaptive-model"
  default_model: opus
  tier_overrides:
    trivial:
      default: haiku
      core: sonnet  # Business logic still needs quality
    simple:
      default: sonnet
      docs: haiku
      tests: haiku
    moderate:
      default: opus
    complex:
      default: opus
```

## Model Selection Algorithm

```text
FUNCTION select_model(complexity_tier, task_type, role_group):

  # 1. Check complexity tier
  tier_config = model_selection.tier_overrides.get(
    complexity_tier.lower(),
    {default: "opus"}
  )

  # 2. Check task-type specific override
  IF task_type IN tier_config:
    RETURN tier_config[task_type]

  # 3. Check role-group specific override
  role_model_map = {
    TRIVIAL: {
      INFRA: "haiku",
      BACKEND: "sonnet",  # Core logic needs quality
      FRONTEND: "haiku",
      TESTING: "haiku",
      REVIEW: "haiku",
      DOCS: "haiku"
    },
    SIMPLE: {
      INFRA: "haiku",
      BACKEND: "sonnet",
      FRONTEND: "sonnet",
      TESTING: "haiku",
      REVIEW: "sonnet",
      DOCS: "haiku"
    },
    MODERATE: {
      INFRA: "haiku",
      BACKEND: "opus",
      FRONTEND: "sonnet",
      TESTING: "sonnet",
      REVIEW: "opus",
      DOCS: "haiku"
    },
    COMPLEX: {
      INFRA: "sonnet",
      BACKEND: "opus",
      FRONTEND: "opus",
      TESTING: "sonnet",
      REVIEW: "opus",
      DOCS: "sonnet"
    }
  }

  IF complexity_tier IN role_model_map:
    IF role_group IN role_model_map[complexity_tier]:
      RETURN role_model_map[complexity_tier][role_group]

  # 4. Fallback to tier default
  RETURN tier_config.default


FUNCTION get_task_type(task, agent):
  # Infer task type from markers and agent role
  IF "[TEST:" IN task.markers:
    RETURN "tests"
  IF agent.role CONTAINS "documentation":
    RETURN "docs"
  IF agent.role CONTAINS "scaffold" OR agent.role CONTAINS "installer":
    RETURN "setup"
  IF agent.role CONTAINS "builder":
    RETURN "core"
  RETURN "default"
```

## Complexity-Adaptive Execution

```text
IMPLEMENT_ADAPTATION_BY_TIER = {

  TRIVIAL: {
    description: "Minimal feature, straightforward implementation",
    workflow: {
      skip_vision_validation: true,
      skip_full_self_review: true,
      self_review_criteria: ["SR-IMPL-01", "SR-IMPL-02", "SR-IMPL-03", "SR-IMPL-07"],  # Critical only
      max_parallel: 5,
      default_model: "haiku"
    },
    expected_time: "45-90s"
  },

  SIMPLE: {
    description: "Standard feature, limited scope",
    workflow: {
      skip_vision_validation: false,
      vision_viewports: ["desktop"],  # Single viewport only
      self_review_criteria: ["SR-IMPL-01" through "SR-IMPL-10"],  # Abbreviated
      max_parallel: 4,
      default_model: "sonnet"
    },
    expected_time: "100-180s"
  },

  MODERATE: {
    description: "Full feature, standard workflow",
    workflow: {
      skip_vision_validation: false,
      vision_viewports: ["mobile", "tablet", "desktop"],  # All viewports
      self_review_criteria: "ALL",  # Full review
      max_parallel: 3,
      default_model: "opus"
    },
    expected_time: "200-400s"
  },

  COMPLEX: {
    description: "Large feature, extensive validation",
    workflow: {
      skip_vision_validation: false,
      vision_viewports: ["mobile", "tablet", "desktop"],
      vision_states: ["default", "loading", "error", "empty", "success", "edge"],  # Extra states
      self_review_criteria: "ALL",
      self_review_iterations: 3,  # Multiple passes
      max_parallel: 3,  # Conservative for stability
      default_model: "opus"
    },
    expected_time: "350-700s"
  }
}
```

## Subagent Model Override

```text
FUNCTION apply_model_to_subagents(subagents, complexity_tier):

  FOR agent IN subagents:
    # Check if agent has explicit model_override
    IF agent.model_override IS NOT None:
      CONTINUE  # Respect explicit override

    # Calculate optimal model
    task_type = get_task_type_for_agent(agent)
    optimal_model = select_model(
      complexity_tier,
      task_type,
      agent.role_group
    )

    # Apply model
    agent.model_override = optimal_model

    LOG f"Agent {agent.role}: model → {optimal_model} (tier={complexity_tier}, group={agent.role_group})"

  RETURN subagents
```

## Cost Estimation

```text
MODEL_COSTS = {
  haiku: {
    input: 0.25,   # $/1M tokens
    output: 1.25,
    cache_read: 0.03,
    cache_write: 0.30
  },
  sonnet: {
    input: 3.00,
    output: 15.00,
    cache_read: 0.30,
    cache_write: 3.75
  },
  opus: {
    input: 15.00,
    output: 75.00,
    cache_read: 1.50,
    cache_write: 18.75
  }
}

FUNCTION estimate_cost(complexity_tier, task_count):
  tier_config = IMPLEMENT_ADAPTATION_BY_TIER[complexity_tier]

  # Estimate tokens per task by type
  tokens_estimate = {
    setup: {input: 2000, output: 1000},
    core: {input: 5000, output: 3000},
    tests: {input: 3000, output: 2000},
    docs: {input: 1000, output: 1500}
  }

  total_cost = 0
  FOR task_type, count IN estimate_task_distribution(task_count):
    model = select_model(complexity_tier, task_type, None)
    tokens = tokens_estimate[task_type]

    cost = (
      tokens.input * MODEL_COSTS[model].input / 1_000_000 +
      tokens.output * MODEL_COSTS[model].output / 1_000_000
    ) * count

    total_cost += cost

  RETURN total_cost


FUNCTION compare_cost_savings(complexity_tier, task_count):
  # Cost with all-opus
  opus_cost = estimate_cost_all_opus(task_count)

  # Cost with adaptive selection
  adaptive_cost = estimate_cost(complexity_tier, task_count)

  savings = opus_cost - adaptive_cost
  savings_pct = (savings / opus_cost) * 100

  RETURN {
    opus_cost: opus_cost,
    adaptive_cost: adaptive_cost,
    savings: savings,
    savings_pct: savings_pct
  }
```

## Integration with implement.md

Add to `claude_code` section:

```yaml
claude_code:
  model_selection:
    enabled: true
    skip_flag: "--no-adaptive-model"
  # Read complexity tier from spec.md or calculate
  complexity_tier: "${COMPLEXITY_TIER}"  # TRIVIAL, SIMPLE, MODERATE, COMPLEX
```

Reference at start of implementation:

```text
Read `templates/shared/implement/model-selection.md` and apply.

# At implementation start
complexity_tier = read_from_spec() OR calculate_complexity()
subagents = apply_model_to_subagents(subagents, complexity_tier)
workflow_config = IMPLEMENT_ADAPTATION_BY_TIER[complexity_tier]

# Log adaptation
LOG f"Complexity: {complexity_tier}"
LOG f"Workflow adaptation: {workflow_config.description}"
LOG f"Cost estimate: ${estimate_cost(complexity_tier, task_count):.2f}"
```

## Output Format

```text
🎯 Complexity-Adaptive Execution
├── Detected Tier: SIMPLE (score: 42/100)
├── Workflow Adaptations:
│   ├── Vision: Single viewport (desktop only)
│   ├── Self-review: Abbreviated (10 criteria)
│   └── Max parallel: 4
├── Model Selection:
│   ├── project-scaffolder: haiku
│   ├── dependency-installer: haiku
│   ├── data-layer-builder: sonnet
│   ├── ui-foundation-builder: sonnet
│   ├── api-builder: sonnet
│   ├── ui-feature-builder: sonnet
│   ├── unit-test-generator: haiku
│   ├── integration-test-generator: haiku
│   ├── code-reviewer: sonnet
│   └── documentation-generator: haiku
├── Cost Comparison:
│   ├── All-opus estimate: $18.50
│   ├── Adaptive estimate: $6.20
│   └── Savings: $12.30 (66%)
└── Expected time: 100-180s
```

## Override Flags

```text
# Force all opus (disable adaptation)
/speckit.implement --no-adaptive-model

# Force specific tier behavior
/speckit.implement --tier=COMPLEX  # Full validation even for simple features

# Force specific model for all agents
/speckit.implement --model=sonnet  # Override all selections
```

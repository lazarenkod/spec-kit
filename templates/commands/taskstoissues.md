---
description: Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts.
tools: ['github/github-mcp-server/issue_write']
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
flags:
  - name: --thinking-depth
    type: choice
    choices: [minimal, quick, standard, thorough]
    default: minimal
    description: |
      Thinking budget (Claude Code Max tier):
      - minimal: 4K budget, ~30s (~$0.06)
      - quick: 8K budget, ~60s (~$0.12)
      - standard: 16K budget, ~90s (~$0.24)
      - thorough: 32K budget, ~120s (~$0.48)

      Free tier: 25% budgets | Pro tier: 50-67% budgets
claude_code:
  model: haiku  # Template-based conversion, minimal orchestration reasoning required
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        minimal: 1000    # 25% of 4K
        quick: 2000      # 25% of 8K
        standard: 4000   # 25% of 16K
        thorough: 8000   # 25% of 32K
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90

      pro:
        minimal: 2000    # 50% of 4K
        quick: 4000      # 50% of 8K
        standard: 10720  # 67% of 16K
        thorough: 21440  # 67% of 32K
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80

      max:
        minimal: 4000
        quick: 8000
        standard: 16000
        thorough: 32000
        max_parallel: 8
        batch_delay: 2000
        wave_overlap_threshold: 0.70

  depth_defaults:
    minimal:
      thinking_budget: 4000
      timeout: 30

    quick:
      thinking_budget: 8000
      timeout: 60

    standard:
      thinking_budget: 16000
      timeout: 90

    thorough:
      thinking_budget: 32000
      timeout: 120

  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier == 'free' AND requested_depth == 'thorough'"
        fallback_depth: "standard"
        fallback_thinking: 16000
        warning_message: |
          ⚠️ **Thorough mode requires Pro tier or higher**.
          Auto-downgrading to **Standard** mode (16K budget).

      - condition: "user_tier == 'free' AND requested_depth == 'standard'"
        fallback_depth: "quick"
        fallback_thinking: 8000
        warning_message: |
          ⚠️ **Standard mode requires Pro tier**.
          Auto-downgrading to **Quick** mode (8K budget).

  cost_breakdown:
    minimal: {cost: $0.06, time: "30s"}
    quick: {cost: $0.12, time: "60s"}
    standard: {cost: $0.24, time: "90s"}
    thorough: {cost: $0.48, time: "120s"}

  cache_hierarchy: full
  subagents:
    # Wave 1: Task Parsing
    - role: task-parser
      role_group: ANALYSIS
      parallel: false
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        Parse tasks.md for all task entries.
        Extract task IDs, descriptions, dependencies.
        Build dependency graph for ordering.
        Validate GitHub remote URL before proceeding.
        Output: parsed tasks with dependency order.

    # Wave 2: Issue Creation (sequential after parsing)
    - role: issue-creator
      role_group: DOCS
      parallel: false
      depends_on: [task-parser]
      priority: 20
      model_override: sonnet
      prompt: |
        Create GitHub issues using MCP server.
        Maintain dependency order in issue references.
        Add labels, milestones if configured.
        Link issues to spec and plan artifacts.
        Output: created issue URLs with mapping.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").
1. From the executed script, extract the path to **tasks**.
1. Get the Git remote by running:

```bash
git config --get remote.origin.url
```

> [!CAUTION]
> ONLY PROCEED TO NEXT STEPS IF THE REMOTE IS A GITHUB URL

1. For each task in the list, use the GitHub MCP server to create a new issue in the repository that is representative of the Git remote.

> [!CAUTION]
> UNDER NO CIRCUMSTANCES EVER CREATE ISSUES IN REPOSITORIES THAT DO NOT MATCH THE REMOTE URL

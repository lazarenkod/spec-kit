---
description: Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts.
tools: ['github/github-mcp-server/issue_write']
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 8000
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

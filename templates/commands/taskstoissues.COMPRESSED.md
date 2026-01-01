---
description: Convert existing tasks into actionable, dependency-ordered GitHub issues
tools: [github/github-mcp-server/issue_write]
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
claude_code:
  model: sonnet
  reasoning_mode: normal
  thinking_budget: 2000
  cache_hierarchy: full
---

## Input
```text
$ARGUMENTS
```

---

## Workflow

```text
1. Run {SCRIPT} → FEATURE_DIR, tasks path
2. Get Git remote: git config --get remote.origin.url

⚠️ ONLY PROCEED IF REMOTE IS A GITHUB URL

3. FOR EACH task:
   - Use GitHub MCP server to create issue
   - Preserve dependencies and order

⛔ NEVER CREATE ISSUES IN REPOSITORIES THAT DON'T MATCH REMOTE URL
```

---

## Context

{ARGS}

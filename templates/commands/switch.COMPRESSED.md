---
description: Switch to a different feature to continue working on it
handoffs:
  - label: Continue Specification
    agent: speckit.specify
    condition: ["status = CREATED or IN_PROGRESS"]
  - label: Create Plan
    agent: speckit.plan
    condition: ["status = SPEC_COMPLETE"]
  - label: Generate Tasks
    agent: speckit.tasks
    condition: ["status = PLANNED"]
  - label: Implement
    agent: speckit.implement
    condition: ["status = TASKED or IMPLEMENTING"]
scripts:
  sh: mkdir -p .speckit && echo "{FEATURE_ID}" > .speckit/active
  ps: $null = New-Item -ItemType Directory -Force -Path .speckit; Set-Content -Path ".speckit/active" -Value "{FEATURE_ID}"
claude_code:
  model: sonnet
  reasoning_mode: normal
  thinking_budget: 2000
---

## Input
```text
$ARGUMENTS
```

---

## Purpose

Switch active feature context to resume work on a previously created feature.

---

## Argument Parsing

```text
/speckit.switch 001              # By ID only
/speckit.switch user-auth        # By name only
/speckit.switch 001-user-auth    # Full feature name

Parse INPUT:
  IF /^\d{3}$/ → LOOKUP_MODE = "id"
  ELIF /^\d{3}-/ → LOOKUP_MODE = "full"
  ELSE → LOOKUP_MODE = "name"
```

---

## Execution Flow

### Step 1: Validate Input

```text
IF INPUT is empty:
  OUTPUT: "Usage: /speckit.switch <feature-id or name>"
  OUTPUT: "Run /speckit.list to see available features."
  EXIT
```

### Step 2: Find Feature

```text
Read MANIFEST_FILE = specs/features/.manifest.md

MATCH LOOKUP_MODE:
  "id" → find where ID = FEATURE_ID
  "full" → find where "{ID}-{Name}" = INPUT
  "name" → find where Name contains INPUT
    IF multiple matches → prompt for specific ID

IF NOT found → show available features
```

### Step 3: Validate Directory

```text
FEATURE_DIR = specs/features/{ID}-{Name}/
IF NOT exists(FEATURE_DIR):
  Warn: "Feature directory not found"
  Suggest: mkdir -p {FEATURE_DIR}
```

### Step 4: Update Active State

```text
mkdir -p .speckit
write "{ID}-{Name}" to .speckit/active
```

### Step 5: Git Branch Switch

```text
IF is_git_repo():
  BRANCH_NAME = "{ID}-{Name}"

  IF branch_exists(BRANCH_NAME):
    IF has_uncommitted_changes():
      Warn: "Uncommitted changes. Stash or commit first."
    ELSE:
      git checkout {BRANCH_NAME}
  ELSE:
    Note: "Branch does not exist. Create with: git checkout -b {BRANCH_NAME}"
```

### Step 6: Determine Status

```text
files = { spec, plan, tasks, baseline }

actual_status:
  NOT spec → "CREATED"
  has_clarification_markers → "IN_PROGRESS"
  NOT plan → "SPEC_COMPLETE"
  NOT tasks → "PLANNED"
  ELSE → trust manifest
```

### Step 7: Display Confirmation

```markdown
## ✅ Switched to Feature: {ID}-{Name}

**Status**: {actual_status}
**Last Updated**: {date}

| File | Status |
|------|--------|
| spec.md | ✓/✗ |
| plan.md | ✓/✗ |
| tasks.md | ✓/✗ |

### Recommended Next Step
{Based on status}
```

---

## Next Step Suggestions

| Status | Suggestion |
|--------|------------|
| CREATED | 📝 `/speckit.specify` |
| IN_PROGRESS | 📝 `/speckit.clarify` |
| SPEC_COMPLETE | 📋 `/speckit.plan` |
| PLANNED | ✅ `/speckit.tasks` |
| TASKED/IMPLEMENTING | 🔨 `/speckit.implement` |
| MERGED | ✨ No action needed |
| ABANDONED | ⚠️ Update manifest status |

---

## CLI Flags

| Flag | Description |
|------|-------------|
| `<id>` | Switch by feature ID (e.g., `001`) |
| `<name>` | Switch by feature name |
| `--json` | Output in JSON format |
| `--repair` | Regenerate manifest from directory structure |
| `--no-git` | Skip git branch checkout |

---

## JSON Output

```json
{
  "success": true,
  "feature": { "id": "001", "name": "user-auth", "status": "IN_PROGRESS" },
  "files": { "spec": true, "plan": false, "tasks": false },
  "git": { "branch_exists": true, "switched": true },
  "next_action": "/speckit.plan"
}
```

---

## Context

{ARGS}

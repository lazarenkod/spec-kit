---
description: List all features in the project with their current status
handoffs:
  - label: Switch to Feature
    agent: speckit.switch
    auto: false
  - label: Create New Feature
    agent: speckit.specify
    auto: false
scripts:
  sh: echo "Feature list - no prerequisites required"
  ps: Write-Host "Feature list - no prerequisites required"
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

## Purpose

Display all features registered in the project manifest with their status and which is currently active.

---

## Execution Flow

### Step 1: Locate Files

```text
MANIFEST_FILE = specs/features/.manifest.md
ACTIVE_FILE = .speckit/active

IF NOT exists(MANIFEST_FILE):
  OUTPUT: "No features found. Run /speckit.specify to create your first feature."
  EXIT

ACTIVE_FEATURE = read(ACTIVE_FILE) OR get_current_branch()
```

### Step 2: Parse & Display

**Normal Mode**:
```markdown
## Feature Registry

| | ID | Name | Status | Last Updated |
|---|-----|------|--------|--------------|
| → | 001 | user-auth | IN_PROGRESS | 2024-12-22 |
|   | 002 | payment | SPEC_COMPLETE | 2024-12-23 |

**Active Feature**: 001-user-auth (→)

### Status Legend
CREATED → IN_PROGRESS → SPEC_COMPLETE → PLANNED → TASKED → IMPLEMENTING → MERGED
```

### Step 3: Status Detection

```text
FOR each feature in manifest:
  feature_dir = specs/features/{ID}-{Name}/

  IF NOT exists(feature_dir) → "MISSING"
  ELIF NOT exists(spec.md) → "CREATED"
  ELIF has_clarification_markers → "IN_PROGRESS"
  ELIF NOT exists(plan.md) → "SPEC_COMPLETE"
  ELIF NOT exists(tasks.md) → "PLANNED"
  ELIF NOT all_tasks_complete → "IMPLEMENTING"
  ELSE → "TASKED" or check merge status
```

---

## CLI Flags

| Flag | Description |
|------|-------------|
| (none) | Show feature table with status |
| `--verbose`, `-v` | Include file details per feature |
| `--json` | Output in JSON format |
| `--status <X>` | Filter by status |
| `--tree` | Show feature evolution tree |
| `--evolution <id>` | Show full lineage for feature |

---

## Verbose Mode (`-v`)

```markdown
### 001-user-auth (ACTIVE)
**Status**: IN_PROGRESS
**Files**: ✓ spec.md | ✗ plan.md | ✗ tasks.md | ✗ baseline.md
**Next Step**: /speckit.plan
```

---

## Feature Evolution Tree (`--tree`)

```markdown
**auth/login.md**
└── 001-login (MERGED) ──────── CREATES
    ├── 015-rate-limiting (MERGED) ── EXTENDS
    │   └── 025-rate-v2 (MERGED) ──── REFINES
    └── 023-2fa (IMPLEMENTING) ────── EXTENDS

### Statistics
| Metric | Count |
|--------|-------|
| Root Features | 3 |
| Extension Features | 6 |
| Max Depth | 3 |
```

---

## JSON Output (`--json`)

```json
{
  "active": "001-user-auth",
  "features": [{
    "id": "001", "name": "user-auth",
    "status": "IN_PROGRESS", "is_active": true,
    "files": { "spec": true, "plan": false, "tasks": false }
  }],
  "summary": { "total": 3, "by_status": { "IN_PROGRESS": 1 } }
}
```

---

## Edge Cases

| Scenario | Response |
|----------|----------|
| Empty manifest | "No features registered yet. Run /speckit.specify" |
| Corrupted manifest | Attempt reconstruction from specs/features/ directory |
| Active not in manifest | Warning + suggest /speckit.switch |

---

## Actions After Display

```markdown
- **Switch feature**: `/speckit.switch <ID or name>`
- **Create new feature**: `/speckit.specify <description>`
- **Continue current**: The active feature is ready for `{next_command}`
```

---

## Context

{ARGS}

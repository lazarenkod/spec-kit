---
description: List all features in the project with their current status. Shows feature registry from manifest and indicates which feature is currently active.
handoffs:
  - label: Switch to Feature
    agent: speckit.switch
    prompt: Switch to a different feature
    auto: false
  - label: Create New Feature
    agent: speckit.specify
    prompt: Create a new feature specification
    auto: false
scripts:
  sh: echo "Feature list - no prerequisites required"
  ps: Write-Host "Feature list - no prerequisites required"
claude_code:
  model: haiku
  reasoning_mode: extended
  thinking_budget: 4000
  subagents:
    - role: registry-reader
      role_group: ANALYSIS
      parallel: false
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        Read and display feature registry from manifest.
        Parse specs/features/.manifest.md for feature list.
        Detect active feature from .speckit/active.
        Verify status by checking actual file existence.
        Support --verbose, --json, --tree, --evolution modes.
        Output formatted feature table with status legend.
---

## User Input

```text
$ARGUMENTS
```

## Feature Registry

This command displays all features registered in the project manifest, their current status in the development lifecycle, and which feature is currently active.

### Execution Flow

1. **Locate Manifest File**:
   ```text
   MANIFEST_FILE = specs/features/.manifest.md

   IF NOT exists(MANIFEST_FILE):
     OUTPUT: "No features found. Run /speckit.specify to create your first feature."
     EXIT
   ```

2. **Read Active Feature**:
   ```text
   ACTIVE_FILE = .speckit/active

   IF exists(ACTIVE_FILE):
     ACTIVE_FEATURE = read(ACTIVE_FILE).trim()
   ELSE:
     ACTIVE_FEATURE = get_current_branch()  # fallback to git/highest number
   ```

3. **Parse Manifest**:
   ```text
   Parse markdown table from MANIFEST_FILE
   Extract columns: ID, Name, Status, Created, Last Updated
   ```

4. **Display Feature Registry**:

   **Output Format (Normal Mode)**:
   ````markdown
   ## Feature Registry

   | | ID | Name | Status | Last Updated |
   |---|-----|------|--------|--------------|
   | → | 001 | user-auth | IN_PROGRESS | 2024-12-22 |
   |   | 002 | payment | SPEC_COMPLETE | 2024-12-23 |
   |   | 003 | notifications | CREATED | 2024-12-24 |

   **Active Feature**: 001-user-auth (→)

   ### Status Legend

   ```text
   CREATED → IN_PROGRESS → SPEC_COMPLETE → PLANNED → TASKED → IMPLEMENTING → MERGED
   ```

   - `CREATED` — directory exists, no spec yet
   - `IN_PROGRESS` — spec.md exists but incomplete
   - `SPEC_COMPLETE` — spec.md done, ready for plan
   - `PLANNED` — plan.md complete
   - `TASKED` — tasks.md generated
   - `IMPLEMENTING` — implementation started
   - `MERGED` — merged to system specs
   - `ABANDONED` — explicitly abandoned
   ````

5. **Verbose Mode** (if `--verbose` or `-v` in $ARGUMENTS):

   For each feature, also show file existence:
   ```markdown
   ### 001-user-auth (ACTIVE)

   **Status**: IN_PROGRESS
   **Files**:
   - ✓ spec.md
   - ✗ plan.md
   - ✗ tasks.md
   - ✗ baseline.md

   **Next Step**: /speckit.plan
   ```

6. **Summary Statistics**:
   ```markdown
   ### Summary

   | Status | Count |
   |--------|-------|
   | CREATED | 1 |
   | IN_PROGRESS | 1 |
   | SPEC_COMPLETE | 1 |
   | MERGED | 0 |
   | **Total** | 3 |
   ```

### Status Detection Logic

If manifest status is outdated, verify by checking actual files:

```text
FOR each feature in manifest:
  feature_dir = specs/features/{ID}-{Name}/

  IF NOT exists(feature_dir):
    status = "MISSING"  # Directory deleted
  ELIF NOT exists(feature_dir/spec.md):
    status = "CREATED"
  ELIF has_clarification_markers(feature_dir/spec.md):
    status = "IN_PROGRESS"
  ELIF NOT exists(feature_dir/plan.md):
    status = "SPEC_COMPLETE"
  ELIF NOT exists(feature_dir/tasks.md):
    status = "PLANNED"
  ELIF NOT all_tasks_complete(feature_dir/tasks.md):
    status = "IMPLEMENTING"
  ELSE:
    status = "TASKED" or check for merge status

  IF status != manifest_status:
    WARN: "Status mismatch for {ID}: manifest says {manifest_status}, actual is {status}"
```

### Available Actions

After displaying the registry, suggest relevant actions:

```markdown
### Actions

- **Switch feature**: `/speckit.switch <ID or name>` (e.g., `/speckit.switch 001`)
- **Create new feature**: `/speckit.specify <description>`
- **Continue current**: The active feature is ready for `/speckit.plan`
```

### Edge Cases

1. **Empty Manifest** (header only, no rows):
   ```text
   No features registered yet. Run /speckit.specify to create your first feature.
   ```

2. **Corrupted Manifest** (parse error):
   ```text
   Warning: Could not parse manifest file. It may be corrupted.
   Attempting to reconstruct from specs/features/ directory...

   [List directories found and their file status]

   Run /speckit.switch --repair to regenerate manifest from directory structure.
   ```

3. **Active Feature Not in Manifest**:
   ```text
   Warning: Active feature "{ACTIVE_FEATURE}" not found in manifest.
   This may indicate the manifest is out of sync.

   Options:
   1. Add it manually to manifest
   2. Switch to a registered feature: /speckit.switch <ID>
   ```

### JSON Output Mode

If `--json` in $ARGUMENTS:

```json
{
  "active": "001-user-auth",
  "features": [
    {
      "id": "001",
      "name": "user-auth",
      "full_name": "001-user-auth",
      "status": "IN_PROGRESS",
      "created": "2024-12-20",
      "last_updated": "2024-12-22",
      "is_active": true,
      "files": {
        "spec": true,
        "plan": false,
        "tasks": false
      }
    }
  ],
  "summary": {
    "total": 3,
    "by_status": {
      "CREATED": 1,
      "IN_PROGRESS": 1,
      "SPEC_COMPLETE": 1
    }
  }
}
```

## Quick Reference

| Argument | Description |
|----------|-------------|
| (none) | Show feature table with status |
| `--verbose`, `-v` | Include file details per feature |
| `--json` | Output in JSON format |
| `--status <status>` | Filter by status (e.g., `--status IN_PROGRESS`) |
| `--tree` | Show feature evolution tree (parent-child relationships) |
| `--evolution <id>` | Show full lineage for a specific feature |

---

## Feature Evolution Tree (--tree)

**Display parent-child relationships between features based on Feature Lineage:**

When `--tree` is in $ARGUMENTS, output a hierarchical view organized by system specs:

```markdown
## Feature Evolution Tree

### By System Spec

**auth/login.md**
└── 001-login (MERGED) ─────────────── CREATES
    ├── 015-rate-limiting (MERGED) ─── EXTENDS
    │   └── 025-rate-v2 (MERGED) ───── REFINES
    ├── 018-login-bugfix (MERGED) ──── FIXES
    └── 023-2fa (IMPLEMENTING) ─────── EXTENDS

**payments/checkout.md**
└── 005-checkout (MERGED) ──────────── CREATES
    └── 030-payment-methods (TASKED) ─ EXTENDS

**notifications/push.md**
└── 010-push-notif (MERGED) ────────── CREATES
    └── 032-push-v2 (IN_PROGRESS) ──── DEPRECATES

### Orphan Features (no system spec impact)
- 002-dashboard (SPEC_COMPLETE) — No system spec impact defined
- 008-analytics (CREATED) — Spec incomplete

### Statistics
| Metric | Count |
|--------|-------|
| Root Features (CREATES) | 3 |
| Extension Features | 6 |
| Max Depth | 3 (025-rate-v2) |
| Orphan Features | 2 |
```

**Tree Building Logic:**

```text
1. Parse all features from manifest
2. For each feature with Feature Lineage section:
   - Extract parent feature reference
   - Add to parent's children list
   - Record relationship type
3. Organize by system spec:
   - Group features by "System Specs Affected"
   - Build tree within each group
4. Identify orphans:
   - Features without Feature Lineage AND
   - No children extending them AND
   - No system spec impact
5. Render as ASCII tree with relationship types
```

---

## Feature Evolution History (--evolution <id>)

**Display the full lineage of a specific feature:**

When `--evolution 015` is provided, show the complete evolution history:

````markdown
## Feature Evolution: 015-rate-limiting

### Lineage Chain (ancestors → feature → descendants)

```text
001-login (MERGED 2024-01-15)
    │
    └── EXTENDS ──→ 015-rate-limiting (MERGED 2024-03-01) ← YOU ARE HERE
                        │
                        └── REFINES ──→ 025-rate-v2 (MERGED 2024-05-10)
```

### Ancestor Context

**001-login** (Root feature)
- Status: MERGED
- Merged: 2024-01-15
- System Specs Created: auth/login.md
- Key Decisions:
  - Session-based authentication
  - JWT for API access
  - Rate limiting deferred to future feature

### Current Feature

**015-rate-limiting**
- Status: MERGED
- Extends: 001-login (EXTENDS)
- Merged: 2024-03-01
- Changes to System Spec:
  - Added rate limiting middleware
  - 100 req/min per user
  - Exponential backoff on exceed

### Descendants

| Feature | Relationship | Status | Changes |
|---------|--------------|--------|---------|
| 025-rate-v2 | REFINES | MERGED | Increased limit to 200/min, added burst |

### System Spec Timeline

**auth/login.md** version history from this lineage:

| Version | Feature | Relationship | Date | Changes |
|---------|---------|--------------|------|---------|
| 1.0 | 001-login | CREATES | 2024-01-15 | Initial creation |
| 1.1 | 015-rate-limiting | EXTENDS | 2024-03-01 | Added rate limiting |
| 1.2 | 025-rate-v2 | REFINES | 2024-05-10 | Refined rate limits |

### Related Commands
- View full system spec: `/speckit.view system/auth/login.md`
- Analyze impact: `/speckit.analyze --impact system/auth/login.md`
- Create extension: `/speckit.extend 015-rate-limiting "Add custom rate limits"`
````

**Evolution Query Logic:**

```text
1. Find target feature by ID or name
2. Trace ancestors:
   - Parse Feature Lineage section
   - Recursively follow parent references
   - Build ancestor chain to root
3. Find descendants:
   - Scan all features' Feature Lineage
   - Find features that extend target
   - Recursively find their descendants
4. Extract context from each feature:
   - Key decisions from spec.md
   - Changes from .merged file
   - Version history from system specs
5. Build timeline visualization
```

---

## JSON Output for Tree/Evolution

If `--json --tree` provided:

```json
{
  "tree": {
    "system/auth/login.md": {
      "root": "001-login",
      "children": [
        {
          "id": "015",
          "name": "rate-limiting",
          "relationship": "EXTENDS",
          "status": "MERGED",
          "children": [
            {
              "id": "025",
              "name": "rate-v2",
              "relationship": "REFINES",
              "status": "MERGED",
              "children": []
            }
          ]
        }
      ]
    }
  },
  "orphans": ["002-dashboard", "008-analytics"],
  "statistics": {
    "root_features": 3,
    "extension_features": 6,
    "max_depth": 3
  }
}
```

If `--json --evolution 015` provided:

```json
{
  "feature": "015-rate-limiting",
  "ancestors": [
    {"id": "001", "name": "login", "relationship": "root"}
  ],
  "descendants": [
    {"id": "025", "name": "rate-v2", "relationship": "REFINES"}
  ],
  "system_specs": ["system/auth/login.md"],
  "version_history": [
    {"version": "1.0", "feature": "001-login", "relationship": "CREATES"},
    {"version": "1.1", "feature": "015-rate-limiting", "relationship": "EXTENDS"},
    {"version": "1.2", "feature": "025-rate-v2", "relationship": "REFINES"}
  ]
}

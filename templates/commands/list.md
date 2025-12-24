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
---

## User Input

```text
$ARGUMENTS
```

## Feature Registry

This command displays all features registered in the project manifest, their current status in the development lifecycle, and which feature is currently active.

### Execution Flow

1. **Locate Manifest File**:
   ```
   MANIFEST_FILE = specs/features/.manifest.md

   IF NOT exists(MANIFEST_FILE):
     OUTPUT: "No features found. Run /speckit.specify to create your first feature."
     EXIT
   ```

2. **Read Active Feature**:
   ```
   ACTIVE_FILE = .speckit/active

   IF exists(ACTIVE_FILE):
     ACTIVE_FEATURE = read(ACTIVE_FILE).trim()
   ELSE:
     ACTIVE_FEATURE = get_current_branch()  # fallback to git/highest number
   ```

3. **Parse Manifest**:
   ```
   Parse markdown table from MANIFEST_FILE
   Extract columns: ID, Name, Status, Created, Last Updated
   ```

4. **Display Feature Registry**:

   **Output Format (Normal Mode)**:
   ```markdown
   ## Feature Registry

   | | ID | Name | Status | Last Updated |
   |---|-----|------|--------|--------------|
   | → | 001 | user-auth | IN_PROGRESS | 2024-12-22 |
   |   | 002 | payment | SPEC_COMPLETE | 2024-12-23 |
   |   | 003 | notifications | CREATED | 2024-12-24 |

   **Active Feature**: 001-user-auth (→)

   ### Status Legend

   ```
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
   ```

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

```
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
   ```
   No features registered yet. Run /speckit.specify to create your first feature.
   ```

2. **Corrupted Manifest** (parse error):
   ```
   Warning: Could not parse manifest file. It may be corrupted.
   Attempting to reconstruct from specs/features/ directory...

   [List directories found and their file status]

   Run /speckit.switch --repair to regenerate manifest from directory structure.
   ```

3. **Active Feature Not in Manifest**:
   ```
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

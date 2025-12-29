# Feature Manifest Update

## Purpose

Unified feature manifest update logic for all Spec Kit commands. Ensures consistent status tracking across the entire SDD workflow.

## Manifest File Location

```text
MANIFEST_FILE = specs/features/.manifest.md
```

## Status Lifecycle

```text
DRAFT → SPEC_COMPLETE → PLANNED → TASKED → IMPLEMENTING → MERGED
                                              ↓
                                         ABANDONED (optional)
```

### Status Transition Table

| From Status | To Status | Triggered By | Description |
|-------------|-----------|--------------|-------------|
| (new) | DRAFT | `/speckit.specify` (partial) | Specification in progress |
| DRAFT | SPEC_COMPLETE | `/speckit.specify` (complete) | Spec validated and ready |
| SPEC_COMPLETE | PLANNED | `/speckit.plan` | Technical plan created |
| PLANNED | TASKED | `/speckit.tasks` | Task breakdown complete |
| TASKED | IMPLEMENTING | `/speckit.implement` | Development started |
| IMPLEMENTING | MERGED | `/speckit.merge` | Feature merged to main |
| (any) | ABANDONED | `/speckit.abandon` | Feature cancelled |

## Instructions for AI Agents

### Parameters Required

When calling this module, the caller must provide:

```text
NEW_STATUS = The status to set (from transition table above)
CALLER_COMMAND = The command triggering the update (for validation)
```

### Step 1: Extract Feature ID

```text
FEATURE_ID = extract from current git branch

# Pattern: feature/NNN-feature-name or NNN-feature-name
# Extract first 3 digits: "feature/001-user-auth" → "001"

IF branch does not match pattern:
  FEATURE_ID = extract from FEATURE_DIR name (first 3 digits)

IF still no FEATURE_ID:
  WARN: "Could not determine feature ID. Manifest not updated."
  SKIP manifest update
```

### Step 2: Validate Transition

```text
VALID_TRANSITIONS = {
  SPEC_COMPLETE: [specify],
  PLANNED: [plan],
  TASKED: [tasks],
  IMPLEMENTING: [implement],
  MERGED: [merge],
  ABANDONED: [abandon]
}

IF CALLER_COMMAND not in VALID_TRANSITIONS[NEW_STATUS]:
  ERROR: "Invalid status transition. {CALLER_COMMAND} cannot set status to {NEW_STATUS}"
  ABORT
```

### Step 3: Update Manifest

```text
IF exists(MANIFEST_FILE):
  1. Parse manifest table (markdown table format)
  2. Find row where ID column = FEATURE_ID

  IF row found:
    3. Update "Status" column: current → NEW_STATUS
    4. Update "Last Updated" column: today's date (YYYY-MM-DD)
    5. Write updated manifest back to file

    LOG: "Feature {FEATURE_ID} status updated: {old_status} → {NEW_STATUS}"

  ELSE:
    # Feature not in manifest - caller should handle this case
    # This happens when specify creates a NEW feature
    WARN: "Feature {FEATURE_ID} not found in manifest"

ELSE:
  # Manifest doesn't exist
  IF CALLER_COMMAND = "specify":
    # Create new manifest with this feature
    Create MANIFEST_FILE with table structure
    Add row for FEATURE_ID with status = NEW_STATUS
    LOG: "Created new manifest with feature {FEATURE_ID}"
  ELSE:
    WARN: "Manifest file not found at {MANIFEST_FILE}. Run /speckit.specify first."
```

### Step 4: Verify Update

```text
# Re-read manifest to confirm update
Read MANIFEST_FILE
Parse table and find FEATURE_ID row
VERIFY Status column = NEW_STATUS

IF verification fails:
  ERROR: "Manifest update verification failed"
```

## Manifest Table Format

```markdown
# Feature Manifest

| ID | Name | Status | Branch | Created | Last Updated | Description |
|----|------|--------|--------|---------|--------------|-------------|
| 001 | user-auth | SPEC_COMPLETE | feature/001-user-auth | 2025-01-15 | 2025-01-16 | User authentication |
| 002 | payments | PLANNED | feature/002-payments | 2025-01-17 | 2025-01-18 | Payment processing |
```

## Usage in Commands

### Example: plan.md

```markdown
## Step N: Update Feature Manifest

Read `templates/shared/core/manifest-update.md` and apply with:
- NEW_STATUS = "PLANNED"
- CALLER_COMMAND = "plan"
```

### Example: tasks.md

```markdown
## Step N: Update Feature Manifest

Read `templates/shared/core/manifest-update.md` and apply with:
- NEW_STATUS = "TASKED"
- CALLER_COMMAND = "tasks"
```

### Example: implement.md

```markdown
## Step N: Update Feature Manifest

Read `templates/shared/core/manifest-update.md` and apply with:
- NEW_STATUS = "IMPLEMENTING"
- CALLER_COMMAND = "implement"
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| "Feature ID not found" | Branch name doesn't match pattern | Use --feature-id flag |
| "Manifest not found" | First feature in project | Create manifest (specify only) |
| "Invalid transition" | Wrong command for status | Check workflow order |
| "Verification failed" | Write error or race condition | Retry once, then report |

## Backward Compatibility

This module is backward compatible:
- If manifest doesn't exist, commands continue without status tracking
- If feature not in manifest, warning is logged but command proceeds
- Old manifest formats (without all columns) are handled gracefully

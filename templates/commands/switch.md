---
description: Switch to a different feature to continue working on it. Updates the active feature state and optionally checks out the corresponding git branch.
handoffs:
  - label: Continue Specification
    agent: speckit.specify
    prompt: Continue working on the feature specification
    auto: false
    condition:
      - "status = CREATED or IN_PROGRESS"
  - label: Create Plan
    agent: speckit.plan
    prompt: Create implementation plan for this feature
    auto: false
    condition:
      - "status = SPEC_COMPLETE"
  - label: Generate Tasks
    agent: speckit.tasks
    prompt: Generate task breakdown for this feature
    auto: false
    condition:
      - "status = PLANNED"
  - label: Implement
    agent: speckit.implement
    prompt: Continue implementing this feature
    auto: false
    condition:
      - "status = TASKED or IMPLEMENTING"
scripts:
  sh: |
    # Inline script - updates .speckit/active
    mkdir -p .speckit
    echo "{FEATURE_ID}" > .speckit/active
  ps: |
    # Inline PowerShell - updates .speckit/active
    New-Item -ItemType Directory -Force -Path .speckit | Out-Null
    Set-Content -Path ".speckit/active" -Value "{FEATURE_ID}"
---

## User Input

```text
$ARGUMENTS
```

## Feature Switch

This command switches the active feature context, allowing you to resume work on a previously created feature.

### Argument Parsing

The user can specify the feature in multiple ways:

```
/speckit.switch 001              # By ID only
/speckit.switch user-auth        # By name only
/speckit.switch 001-user-auth    # Full feature name
```

**Parse Logic**:
```
INPUT = $ARGUMENTS.trim()

IF INPUT matches /^\d{3}$/:
  # ID only (e.g., "001")
  FEATURE_ID = INPUT
  LOOKUP_MODE = "id"

ELIF INPUT matches /^\d{3}-/:
  # Full name (e.g., "001-user-auth")
  FEATURE_ID = INPUT[0:3]
  FEATURE_FULL_NAME = INPUT
  LOOKUP_MODE = "full"

ELSE:
  # Name only (e.g., "user-auth")
  FEATURE_NAME = INPUT
  LOOKUP_MODE = "name"
```

### Execution Flow

1. **Validate Input**:
   ```
   IF INPUT is empty:
     OUTPUT: "Usage: /speckit.switch <feature-id or name>"
     OUTPUT: "Example: /speckit.switch 001 or /speckit.switch user-auth"
     OUTPUT: ""
     OUTPUT: "Run /speckit.list to see available features."
     EXIT
   ```

2. **Read Manifest**:
   ```
   MANIFEST_FILE = specs/features/.manifest.md

   IF NOT exists(MANIFEST_FILE):
     OUTPUT: "No features found. Run /speckit.specify to create your first feature."
     EXIT

   Parse manifest into features list
   ```

3. **Find Target Feature**:
   ```
   MATCH case LOOKUP_MODE:
     "id":
       feature = find in manifest where ID = FEATURE_ID
     "full":
       feature = find in manifest where "{ID}-{Name}" = FEATURE_FULL_NAME
     "name":
       feature = find in manifest where Name contains FEATURE_NAME
       IF multiple matches:
         OUTPUT: "Multiple features match '{FEATURE_NAME}':"
         FOR each match: OUTPUT "  - {ID}-{Name}"
         OUTPUT: "Please specify the full ID (e.g., /speckit.switch 001)"
         EXIT

   IF feature NOT found:
     OUTPUT: "Feature not found: {INPUT}"
     OUTPUT: ""
     OUTPUT: "Available features:"
     FOR each f in manifest: OUTPUT "  - {f.ID}-{f.Name} ({f.Status})"
     EXIT
   ```

4. **Validate Feature Directory Exists**:
   ```
   FEATURE_DIR = specs/features/{feature.ID}-{feature.Name}/

   IF NOT exists(FEATURE_DIR):
     OUTPUT: "Warning: Feature directory not found at {FEATURE_DIR}"
     OUTPUT: "The manifest may be out of sync with the filesystem."
     OUTPUT: ""
     OUTPUT: "Options:"
     OUTPUT: "  1. Create missing directory: mkdir -p {FEATURE_DIR}"
     OUTPUT: "  2. Remove from manifest manually"
     EXIT
   ```

5. **Update Active Feature State**:
   ```
   ACTIVE_FILE = .speckit/active
   FEATURE_FULL = "{feature.ID}-{feature.Name}"

   mkdir -p .speckit
   write FEATURE_FULL to ACTIVE_FILE
   ```

6. **Git Branch Switch** (if git repo):
   ```
   IF is_git_repo():
     BRANCH_NAME = "{feature.ID}-{feature.Name}"

     IF branch_exists(BRANCH_NAME):
       # Check for uncommitted changes
       IF has_uncommitted_changes():
         OUTPUT: "⚠️ You have uncommitted changes. Please commit or stash them first."
         OUTPUT: ""
         OUTPUT: "  git stash        # Temporarily save changes"
         OUTPUT: "  git checkout {BRANCH_NAME}"
         OUTPUT: "  git stash pop    # Restore changes"
         # Still update .speckit/active so feature context is correct
       ELSE:
         git checkout {BRANCH_NAME}
         OUTPUT: "Checked out branch: {BRANCH_NAME}"

     ELSE:
       OUTPUT: "Note: Branch '{BRANCH_NAME}' does not exist."
       OUTPUT: "Feature context updated, but staying on current branch."
       OUTPUT: "Create branch with: git checkout -b {BRANCH_NAME}"
   ```

7. **Determine Feature Status and Files**:
   ```
   FEATURE_DIR = specs/features/{feature.ID}-{feature.Name}/

   files = {
     spec: exists(FEATURE_DIR/spec.md),
     plan: exists(FEATURE_DIR/plan.md),
     tasks: exists(FEATURE_DIR/tasks.md),
     baseline: exists(FEATURE_DIR/baseline.md)
   }

   # Determine actual status from files
   IF NOT files.spec:
     actual_status = "CREATED"
   ELIF has_clarification_markers(FEATURE_DIR/spec.md):
     actual_status = "IN_PROGRESS"
   ELIF NOT files.plan:
     actual_status = "SPEC_COMPLETE"
   ELIF NOT files.tasks:
     actual_status = "PLANNED"
   ELSE:
     actual_status = feature.Status  # Trust manifest for later stages
   ```

8. **Display Switch Confirmation**:
   ```markdown
   ## ✅ Switched to Feature: {feature.ID}-{feature.Name}

   **Status**: {actual_status}
   **Last Updated**: {feature.LastUpdated}

   ### Files

   | File | Status |
   |------|--------|
   | spec.md | {✓ or ✗} |
   | plan.md | {✓ or ✗} |
   | tasks.md | {✓ or ✗} |
   | baseline.md | {✓ or ✗} |

   ### Recommended Next Step

   {Suggest action based on actual_status}
   ```

9. **Suggest Next Action**:
   ```
   MATCH actual_status:
     "CREATED":
       OUTPUT: "📝 Continue specification: This feature needs a spec.md"
       OUTPUT: "   Run: /speckit.specify (to continue editing spec)"

     "IN_PROGRESS":
       OUTPUT: "📝 Complete specification: spec.md has unresolved clarifications"
       OUTPUT: "   Run: /speckit.clarify"

     "SPEC_COMPLETE":
       OUTPUT: "📋 Create implementation plan"
       OUTPUT: "   Run: /speckit.plan"

     "PLANNED":
       OUTPUT: "✅ Generate task breakdown"
       OUTPUT: "   Run: /speckit.tasks"

     "TASKED":
       OUTPUT: "🔨 Start implementation"
       OUTPUT: "   Run: /speckit.implement"

     "IMPLEMENTING":
       OUTPUT: "🔨 Continue implementation"
       OUTPUT: "   Run: /speckit.implement"

     "MERGED":
       OUTPUT: "✨ This feature has been merged to system specs."
       OUTPUT: "   No further action needed."

     "ABANDONED":
       OUTPUT: "⚠️ This feature was abandoned."
       OUTPUT: "   To resume, update its status in the manifest."
   ```

### Error Handling

**Feature Not Found**:
```markdown
❌ Feature not found: {INPUT}

Available features:
| ID | Name | Status |
|----|------|--------|
| 001 | user-auth | IN_PROGRESS |
| 002 | payment | SPEC_COMPLETE |

Use the ID or name to switch: `/speckit.switch 001`
```

**Ambiguous Match**:
```markdown
⚠️ Multiple features match "{INPUT}":

- 001-user-auth
- 003-user-profile

Please specify the full ID: `/speckit.switch 001`
```

### JSON Output Mode

If `--json` in $ARGUMENTS:

```json
{
  "success": true,
  "feature": {
    "id": "001",
    "name": "user-auth",
    "full_name": "001-user-auth",
    "status": "IN_PROGRESS",
    "last_updated": "2024-12-22"
  },
  "files": {
    "spec": true,
    "plan": false,
    "tasks": false,
    "baseline": false
  },
  "git": {
    "branch_exists": true,
    "switched": true
  },
  "next_action": "/speckit.plan"
}
```

### Repair Mode

If `--repair` in $ARGUMENTS:

Regenerate manifest from directory structure:
```
1. Scan specs/features/ for all directories matching NNN-*
2. For each directory:
   - Determine status from file existence
   - Extract ID and name from directory name
   - Get dates from file modification times
3. Write new .manifest.md
4. Report changes
```

## Quick Reference

| Argument | Description |
|----------|-------------|
| `<id>` | Switch by feature ID (e.g., `001`) |
| `<name>` | Switch by feature name (e.g., `user-auth`) |
| `<full>` | Switch by full name (e.g., `001-user-auth`) |
| `--json` | Output in JSON format |
| `--repair` | Regenerate manifest from directory structure |
| `--no-git` | Skip git branch checkout |

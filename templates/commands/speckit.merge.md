---
description: Finalize feature and update system specs after PR merge. Converts feature requirements into living system documentation.
handoffs:
  - label: Analyze System Specs
    agent: speckit.analyze
    prompt: Validate cross-references between feature and system specs
  - label: Create New Feature
    agent: speckit.specify
    prompt: Create a new feature that extends the merged system specs
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 8000
  subagents:
    - role: code-explorer
      role_group: REVIEW
      parallel: false
      depends_on: []
      priority: 5
      trigger: "when validating implementation matches system specs"
      prompt: "Explore codebase for {PATTERN} to validate spec accuracy"
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

After a feature PR is merged, this command:

1. **Validates** the feature spec is complete and implementation-ready
2. **Creates** new system specs defined in "System Spec Impact → Creates"
3. **Updates** existing system specs defined in "System Spec Impact → Updates"
4. **Archives** the feature spec by adding `.merged` marker
5. **Validates** cross-references and dependency integrity

This command transforms **point-in-time requirements** (feature specs) into **living documentation** (system specs).

## Two-Folder Architecture

```text
specs/
├── features/           # Historical feature specs (frozen after merge)
│   ├── 001-login/
│   │   ├── spec.md    # Original login requirements
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   └── .merged    # Marker: feature was merged
│   └── 009-2fa/
│       └── spec.md    # 2FA requirements (references login)
│
└── system/             # Living system specs (current behavior)
    ├── _index.md       # System spec registry
    ├── auth/
    │   ├── login.md   # Current login spec (created by 001, updated by 009)
    │   └── 2fa.md     # 2FA spec (created by 009)
    └── payments/
        └── checkout.md
```

## Operating Constraints

- **Requires completed implementation**: Only run after PR merge to main/master
- **Requires System Spec Impact section**: Feature spec must define what system specs to create/update
- **Preserves history**: Never overwrites system spec history, only appends
- **Validates dependencies**: Ensures dependent specs are updated consistently

## Execution Steps

### 1. Initialize Context

Run `{SCRIPT}` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive paths:

- FEATURE_SPEC = FEATURE_DIR/spec.md
- FEATURE_PLAN = FEATURE_DIR/plan.md (optional)
- FEATURE_TASKS = FEATURE_DIR/tasks.md (optional)
- SYSTEM_DIR = specs/system/

Abort with error if:
- Feature spec doesn't exist
- `.merged` marker already exists (already merged)
- System Spec Impact section is missing or empty

### 2. Parse System Spec Impact

Extract from feature spec:

```markdown
## System Spec Impact

### Creates
| System Spec | Domain | Description |
|-------------|--------|-------------|
| system/auth/2fa.md | auth | Two-factor authentication flow |

### Updates
| System Spec | Changes | Breaking? |
|-------------|---------|-----------|
| system/auth/login.md | Added 2FA verification step | No |

### Breaking Changes
| System Spec | Breaking Change | Migration Path |
|-------------|-----------------|----------------|
```

Build internal model:
- **creates[]**: New system specs to generate
- **updates[]**: Existing system specs to modify
- **breaking[]**: Breaking changes requiring version bump

### 3. Validate Prerequisites

For each system spec in **updates[]**:
- Verify file exists at specified path
- Parse existing Spec History to get current version
- Verify dependencies are satisfied

For each system spec in **creates[]**:
- Verify parent directory exists (create if needed)
- Verify no conflicting file exists

### 4. Generate/Update System Specs

#### For Creates:

1. Copy `templates/system-spec-template.md` to target path
2. Replace placeholders:
   - `[Component Name]` → Extract from path (e.g., `auth/2fa.md` → "2FA")
   - `[Domain]` → Extract from path (e.g., `auth`)
   - `[DATE]` → Current date
3. Populate **Spec History** with Relationship:
   ```markdown
   | Version | Feature | Relationship | Date | Author | Changes |
   |---------|---------|--------------|------|--------|---------|
   | 1.0 | [FEATURE_BRANCH] | CREATES | [DATE] | [@author] | Initial creation |
   ```
   Note: Relationship is always CREATES for new system specs.
4. Populate **Current Behavior** from feature spec's User Stories
5. Populate **Business Rules** from feature spec's Functional Requirements
6. Populate **Dependencies** from feature spec's context

#### For Updates:

1. Read existing system spec
2. **Extract Relationship from Feature Lineage**:
   ```text
   IF feature spec has "Feature Lineage" section:
     Parse the Relationship column from Feature Lineage table
     RELATIONSHIP = value from table (EXTENDS | REFINES | FIXES | DEPRECATES)
   ELSE:
     RELATIONSHIP = EXTENDS (default for updates without lineage)
   ```
3. Append to **Spec History** with Relationship:
   ```markdown
   | [VERSION] | [FEATURE_BRANCH] | [RELATIONSHIP] | [DATE] | [@author] | [CHANGES_SUMMARY] |
   ```
   Version increment based on Relationship:
   - EXTENDS: Minor bump (1.0 → 1.1)
   - REFINES: Patch bump (1.0 → 1.0.1)
   - FIXES: Patch bump (1.0 → 1.0.2)
   - DEPRECATES: Major bump (1.0 → 2.0)
4. Update **Current Behavior** section with new/modified scenarios
5. Update **Business Rules** if changed
6. Update **Dependents** list if this spec gained new dependents
7. If **Breaking?** is "Yes" or Relationship is DEPRECATES:
   - Increment major version
   - Add deprecation notice if applicable

### 5. Update System Index

If `specs/system/_index.md` exists, add entries for new system specs:

```markdown
## auth Domain

| System Spec | Status | Last Updated | Description |
|-------------|--------|--------------|-------------|
| [login.md](auth/login.md) | ACTIVE | 2024-03-20 | User authentication flow |
| [2fa.md](auth/2fa.md) | ACTIVE | 2024-03-20 | Two-factor authentication |
```

If `_index.md` doesn't exist, create it with registry structure.

### 6. Update Feature Manifest

Update the feature registry to mark this feature as merged:

```text
MANIFEST_FILE = specs/features/.manifest.md
FEATURE_ID = extract from FEATURE_BRANCH (first 3 digits)

IF exists(MANIFEST_FILE):
  Find row where ID = FEATURE_ID
  Update Status column: IMPLEMENTING → MERGED
  Update "Last Updated" column: today's date
```

### 7. Update Parent Feature (if extending)

If the feature has a Feature Lineage section (extends another feature):

```text
IF feature spec has "Feature Lineage" section:
  PARENT_FEATURE = extract from Feature Lineage table
  PARENT_ID = extract feature ID from parent reference

  Update parent's "Extended By" tracking:
  - Option A: Update manifest Extended By column
  - Option B: Append to parent's .merged file

  Log: "Updated parent feature {PARENT_ID} to reference extension {FEATURE_ID}"
```

### 8. Mark Feature as Merged

Create `.merged` marker in feature directory:

```json
{
  "merged_at": "2024-03-20T14:30:00Z",
  "merged_by": "@author",
  "system_specs_created": ["system/auth/2fa.md"],
  "system_specs_updated": ["system/auth/login.md"],
  "breaking_changes": false,
  "extends_feature": "001-login",
  "relationship": "EXTENDS"
}
```

Note: `extends_feature` and `relationship` fields are only present if this feature extends another.

### 9. Generate Merge Report

Output summary:

```markdown
## Merge Report: [FEATURE_BRANCH]

**Status**: ✅ Merged successfully

### Feature Lineage
<!-- Only shown if feature extends another -->
**Extends**: [PARENT_FEATURE] (via [RELATIONSHIP] relationship)
**Parent updated**: Extended By now includes [FEATURE_ID]

### System Specs Created
| Path | Version | Relationship | Status |
|------|---------|--------------|--------|
| `system/auth/2fa.md` | 1.0 | CREATES | Created |

### System Specs Updated
| Path | Old Version | New Version | Relationship | Changes |
|------|-------------|-------------|--------------|---------|
| `system/auth/login.md` | 1.0 | 1.1 | EXTENDS | Added 2FA verification step |

### Breaking Changes
None

### Feature Archived
- Feature spec marked as merged
- Historical requirements preserved at `specs/features/[branch]/`
- Feature Lineage traceability established

### Next Steps
- Run `/speckit.analyze --system` to validate system spec integrity
- Run `/speckit.list --tree` to view feature evolution
- Update dependent features if breaking changes were introduced
```

## Maintenance Mode

If called with `--maintain` flag or on an existing system spec (not feature):

```bash
/speckit.merge --maintain system/auth/login.md
```

This mode allows:
- Documentation corrections without new feature
- Clarifications from production observations
- Deprecation of obsolete functionality

Creates a maintenance entry in Spec History:
```markdown
| 1.1.1 | MAINTENANCE | [DATE] | [@author] | [MAINTENANCE_REASON] |
```

## Impact Analysis Mode

If called with `--impact` flag:

```bash
/speckit.merge --impact system/auth/login.md
```

Outputs:
- List of dependent system specs
- List of active features referencing this spec
- Suggested review checklist
- Breaking change warnings

(This analysis is also available via `/speckit.analyze --impact`)

## Operating Principles

### Traceability
- Every system spec change links back to a feature or maintenance event
- History is append-only (never rewritten)
- Breaking changes require explicit acknowledgment

### Consistency
- System specs represent CURRENT behavior (single source of truth)
- Feature specs represent HISTORICAL requirements (frozen after merge)
- Cross-references must resolve correctly

### Progressive Enhancement
- Start with minimal system spec structure
- Enhance detail as more features modify the spec
- Never remove information without deprecation notice

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "Missing System Spec Impact" | Feature spec doesn't have the section | Add section to spec.md before merge |
| "System spec not found" | Update references non-existent spec | Create spec first or fix path |
| "Already merged" | `.merged` marker exists | Feature already processed |
| "Circular dependency" | Spec update would create cycle | Refactor dependency structure |

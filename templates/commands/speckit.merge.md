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
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: standard
    tiers:
      standard:
        thinking_budget: 16000
        max_parallel: 6
        batch_delay: 1500
        wave_overlap_threshold: 0.65
      ultrathink:
        thinking_budget: 48000
        max_parallel: 4
        batch_delay: 2500
        wave_overlap_threshold: 0.60
        cost_multiplier: 3.0

  depth_defaults:
    standard:
      thinking_budget: 16000
      timeout: 90
    ultrathink:
      thinking_budget: 48000
      additional_agents: [spec-historian, dependency-analyzer]
      timeout: 180

  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 16000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (48K thinking budget).
          Auto-downgrading to **Standard** mode (16K budget).

  cost_breakdown:
    standard: {cost: $0.48, time: "90-120s"}
    ultrathink: {cost: $1.44, time: "180-220s"}

  cache_hierarchy: full
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
flags:
  max_model: "--max-model <opus|sonnet|haiku>"  # Override model cap
  thinking_depth: |
    --thinking-depth <standard|ultrathink>
    Thinking budget control:
    - standard: 16K budget (~$0.48) [RECOMMENDED]
    - ultrathink: 48K budget, deep analysis (~$1.44) [REQUIRES Max tier]
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

## Parallel Execution

{{include: shared/orchestration-instructions.md}}

Execute subagents defined in `claude_code.subagents` using parallel Task calls per wave.

---

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

## Generate Migration Guide

After successful merge with breaking changes, generate migration documentation:

```text
IF breaking_changes_detected:
  1. EXTRACT_VERSION_INFO():
     - Read all updated system specs
     - Extract old_version and new_version from Spec History
     - Determine major/minor/patch based on breaking changes
     - old_version = min(all old versions)
     - new_version = max(all new versions)

  2. COLLECT_BREAKING_CHANGES():
     breaking_changes = []
     FOR EACH updated_spec IN system_specs_updated:
       Read updated_spec
       Extract "Spec History" section
       Find latest entry with breaking_changes = true

       FOR EACH breaking_change IN entry.breaking_changes:
         breaking_changes.append({
           "component": updated_spec.component_name,
           "change": breaking_change.description,
           "old_behavior": breaking_change.before,
           "new_behavior": breaking_change.after,
           "reason": breaking_change.reason,
           "migration_path": breaking_change.migration,
           "version": new_version,
           "source_spec": updated_spec.path
         })

  3. EXTRACT_API_CHANGES():
     IF EXISTS("contracts/api.yaml"):
       Read contracts/api.yaml
       Extract version info from "info.version"
       api_changes = []

       FOR EACH endpoint IN api.paths:
         IF endpoint.deprecated OR endpoint.removed:
           api_changes.append({
             "endpoint": endpoint.path,
             "method": endpoint.method,
             "change_type": "removed" OR "deprecated",
             "replacement": endpoint.x-replacement,
             "migration": endpoint.x-migration-guide
           })

  4. EXTRACT_CONFIGURATION_CHANGES():
     config_changes = {
       "removed": [],
       "added": [],
       "modified": []
     }

     IF EXISTS(".env.example"):
       # Compare with previous version if available
       # Extract added/removed/modified environment variables

     FOR EACH breaking_change IN breaking_changes:
       IF breaking_change relates to configuration:
         config_changes[change_type].append({
           "variable": var_name,
           "old_value": old_format,
           "new_value": new_format,
           "migration": migration_steps
         })

  5. GENERATE_MIGRATION_GUIDE():
     Read templates/docs/migration-guide-template.md for structure

     Generate docs/changelog/migration-v{old_version}-to-v{new_version}.md:
     ```markdown
     # Migration Guide: v{old_version} to v{new_version}

     > **Migration Complexity**: {LOW/MEDIUM/HIGH based on breaking_changes count}
     > **Estimated Time**: {estimate based on complexity}
     > **Downtime Required**: {Yes/No based on infrastructure changes}

     ## Overview

     This guide helps you migrate from **{Project Name} v{old_version}** to **v{new_version}**.

     **What's New:**
     {Extract from CHANGELOG.md for this version}

     **Breaking Changes:** {breaking_changes.length}
     **Deprecations:** {deprecations.length}
     **Database Changes:** {Yes/No}

     ---

     ## Should You Upgrade?

     ### Reasons to Upgrade

     ✅ **You should upgrade if:**
     - {Extract benefits from feature specs that were merged}
     - {Extract fixed issues from CHANGELOG}

     ### Reasons to Wait

     ⚠️ **Consider waiting if:**
     - You're using deprecated features without migration plan
     - {Extract compatibility concerns from breaking changes}

     ---

     ## Pre-Migration Checklist

     **Before starting, ensure:**
     - [ ] Full backup created
     - [ ] Migration tested in staging environment
     - [ ] Team notified of planned upgrade
     - [ ] Rollback plan documented

     ---

     ## Breaking Changes

     {FOR EACH breaking_change IN breaking_changes}:
     ### Breaking Change {index}: {change.component} - {change.change}

     **Impact:** {HIGH/MEDIUM/LOW based on affected users}
     **Affects:** {change.component}

     **Old Behavior** (v{old_version}):
     ```
     {change.old_behavior}
     ```

     **New Behavior** (v{new_version}):
     ```
     {change.new_behavior}
     ```

     **Why Changed:** {change.reason}

     **Migration Steps:**

     {change.migration_path}

     **Source:** {change.source_spec}

     ---
     {END FOR EACH}

     ## API Changes

     {IF api_changes exists}:
     **Removed Endpoints:**

     | Old Endpoint | Replacement | Migration Notes |
     |--------------|-------------|-----------------|
     {FOR EACH removed_endpoint IN api_changes.removed}:
     | `{method} {path}` | `{replacement}` | {migration} |
     {END FOR EACH}

     **Deprecated Endpoints:**

     | Endpoint | Deprecation Date | Removal Planned | Replacement |
     |----------|------------------|-----------------|-------------|
     {FOR EACH deprecated_endpoint IN api_changes.deprecated}:
     | `{method} {path}` | v{deprecation_version} | v{removal_version} | {replacement} |
     {END FOR EACH}
     {END IF}

     ---

     ## Configuration Changes

     {IF config_changes exists}:
     ### Environment Variables

     **Removed:**
     | Variable | Replacement | Migration |
     |----------|-------------|-----------|
     {FOR EACH removed_var IN config_changes.removed}:
     | `{var.name}` | `{var.replacement}` | {var.migration} |
     {END FOR EACH}

     **Added:**
     | Variable | Description | Required | Default |
     |----------|-------------|----------|---------|
     {FOR EACH added_var IN config_changes.added}:
     | `{var.name}` | {var.description} | {var.required} | {var.default} |
     {END FOR EACH}

     **Modified:**
     | Variable | Old Format | New Format | Migration |
     |----------|-----------|------------|-----------|
     {FOR EACH modified_var IN config_changes.modified}:
     | `{var.name}` | {var.old_format} | {var.new_format} | {var.migration} |
     {END FOR EACH}
     {END IF}

     ---

     ## Migration Steps

     ### Step 1: Backup

     ⚠️ **Critical: Always backup before upgrading**

     ```bash
     # Backup database
     {database backup command from admin-guide}

     # Backup configuration
     cp .env .env.backup

     # Backup application files
     {backup command}
     ```

     ### Step 2: Update Dependencies

     {Extract dependency updates from plan.md}

     ### Step 3: Database Migration

     {IF database changes}:
     ```bash
     # Run migrations
     {migration command}

     # Verify migration
     {verification command}
     ```
     {END IF}

     ### Step 4: Update Application Code

     {FOR EACH breaking_change IN breaking_changes}:
     {Extract code update steps from migration_path}
     {END FOR EACH}

     ### Step 5: Update Configuration

     {Extract .env updates from config_changes}

     ### Step 6: Verify Migration

     **Post-migration checklist:**
     - [ ] Application starts successfully
     - [ ] Health checks passing
     - [ ] Database migrations applied
     - [ ] API endpoints responding
     - [ ] Key features functional

     ---

     ## Rollback Procedure

     If migration fails:

     ```bash
     # Stop application
     {stop command}

     # Restore database backup
     {restore command}

     # Restore configuration
     cp .env.backup .env

     # Deploy previous version
     {rollback deployment command}
     ```

     ---

     ## Getting Help

     **Having issues?**
     - 📖 Read this guide thoroughly
     - 🔍 Search [known issues]({issues_url}?q=label%3Amigration)
     - 💬 Ask in [discussions]({discussions_url})

     ---

     *Last updated: {generation timestamp}*
     *Generated from: System spec history, CHANGELOG.md, API contracts*
     ```

  6. UPDATE_MIGRATION_INDEX():
     IF NOT EXISTS("docs/changelog/index.md"):
       Create docs/changelog/index.md

     Update docs/changelog/index.md:
     - Add link to new migration guide
     - Update version history table
     - Maintain reverse chronological order

  7. OUTPUT_SUMMARY():
     Log migration guide generation:
     ```text
     📝 Migration Guide Generated:

     ✅ docs/changelog/migration-v{old_version}-to-v{new_version}.md

     Breaking Changes: {breaking_changes.length}
     - {breaking_change_1}
     - {breaking_change_2}

     Configuration Changes: {config_changes.total}
     - {config_summary}

     💡 Migration Complexity: {complexity}
     💡 Estimated Migration Time: {time_estimate}

     Next Steps:
     - Review migration guide in docs/changelog/
     - Test migration in staging environment
     - Update CHANGELOG.md with migration notes
     ```

ELSE:
  OUTPUT: "No breaking changes detected, migration guide not needed"
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

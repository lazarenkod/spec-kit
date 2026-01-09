---
description: Extend a merged feature with new capabilities. Creates a new feature branch with Feature Lineage pre-populated, loading context from the parent feature and its system specs.
handoffs:
  - label: Complete Feature Specification
    agent: speckit.specify
    prompt: Complete the specification for the extension feature
    auto: true
    condition:
      - "Feature created with Feature Lineage populated"
      - "Parent context loaded successfully"
    gates:
      - name: "Extension Valid Gate"
        check: "Feature Lineage section has valid parent reference"
        block_if: "Parent feature reference is broken or invalid"
        message: "Ensure parent feature exists and Feature Lineage is correctly populated"
    post_actions:
      - "log: Extension feature created, proceeding to specification"
  - label: View Parent Spec
    agent: speckit.view
    prompt: Display the parent feature specification
    auto: false
  - label: Analyze Feature Lineage
    agent: speckit.analyze
    prompt: Validate Feature Lineage references and system spec consistency
    auto: false
scripts:
  sh: scripts/bash/create-new-feature.sh --json --extends "{PARENT}" "{DESCRIPTION}"
  ps: scripts/powershell/create-new-feature.ps1 -Json -Extends "{PARENT}" "{DESCRIPTION}"
claude_code:
  model: sonnet
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 4000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 8000
        max_parallel: 3
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 16000
        max_parallel: 6
        batch_delay: 1500
        wave_overlap_threshold: 0.65
  cache_hierarchy: full
  orchestration:
    max_parallel: 6
  subagents:
    # Wave 1: Context Loading
    - role: context-loader
      role_group: ANALYSIS
      parallel: false
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        Validate parent feature exists and is merged.
        Load parent spec, plan, and .merged file.
        Extract system specs affected by parent.
        Gather key user stories, constraints, and decisions.
        Output: parent context summary for extension.

    # Wave 2: Extension Planning (sequential after context)
    - role: extension-planner
      role_group: ANALYSIS
      parallel: false
      depends_on: [context-loader]
      priority: 20
      model_override: sonnet
      prompt: |
        Create extension feature with Feature Lineage.
        Suggest relationship type based on description keywords.
        Pre-populate inherited context section.
        Identify system specs to update.
        Output: new feature spec with lineage established.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** parse the user input to extract:
- **PARENT**: The feature ID or name to extend (e.g., "001", "001-login")
- **DESCRIPTION**: The description of the new extension feature

## Goal

Create a new feature that extends an already-merged feature, establishing explicit **Feature Lineage** for traceability. This is the recommended workflow when:

1. Adding new capabilities to an existing feature (e.g., "Add rate limiting to login")
2. Enhancing behavior of a merged feature
3. Fixing issues discovered in production
4. Deprecating or replacing functionality

## Why Use /speckit.extend vs /speckit.specify

| Scenario | Use |
|----------|-----|
| Brand new feature | `/speckit.specify` |
| Modify merged feature | `/speckit.extend` ← this command |
| Fix bug in merged feature | `/speckit.extend` with FIXES relationship |
| Replace feature behavior | `/speckit.extend` with DEPRECATES relationship |

## Execution Steps

### 1. Parse Arguments

```text
INPUT = "$ARGUMENTS"

Parse patterns:
- "/speckit.extend 001 Add rate limiting" → PARENT=001, DESCRIPTION="Add rate limiting"
- "/speckit.extend 001-login Add 2FA support" → PARENT=001-login, DESCRIPTION="Add 2FA support"
- "/speckit.extend 001 --relationship FIXES Fix login timeout" → PARENT=001, RELATIONSHIP=FIXES, DESCRIPTION="Fix login timeout"

DEFAULT: RELATIONSHIP = EXTENDS (unless specified)
```

### 2. Validate Parent Feature

```bash
Run: scripts/bash/create-new-feature.sh --json --extends "{PARENT}" "{DESCRIPTION}"

Parse output:
- BRANCH_NAME: New feature branch
- SPEC_FILE: Path to new spec.md
- FEATURE_NUM: New feature number
- EXTENDS: Parent feature name
- EXTENDS_ID: Parent feature ID

IF error (parent not found):
  Display error with available features
  Suggest: "Did you mean one of these features?"
  ABORT
```

### 3. Load Parent Context

After feature creation, load context from parent:

```text
PARENT_SPEC = specs/features/{EXTENDS}/spec.md
PARENT_PLAN = specs/features/{EXTENDS}/plan.md (if exists)
PARENT_MERGED = specs/features/{EXTENDS}/.merged

Read and extract:
1. From PARENT_SPEC:
   - Key user stories and requirements
   - Business rules
   - Constraints

2. From PARENT_MERGED (if exists):
   - System specs created/updated
   - Breaking changes introduced
   - Implementation date

3. From System Specs (if referenced in PARENT_MERGED):
   - Current behavior
   - API contracts
   - Dependencies
```

### 4. Pre-populate Extension Spec

The Feature Lineage section should already be populated by the script.

Additionally help the user by:

```markdown
## Context Inherited from Parent

<!-- Auto-populated from {EXTENDS}/spec.md -->

### Parent User Stories
[Extract key stories that this extension relates to]

### Parent Constraints
[List constraints from parent that must be respected]

### System Specs to Update
[List from PARENT_MERGED.system_specs_created/updated]
```

### 5. Suggest Relationship Type

Based on description keywords, suggest the appropriate relationship:

```text
IF DESCRIPTION contains "add", "new", "implement", "support" → EXTENDS
IF DESCRIPTION contains "improve", "enhance", "optimize", "refactor" → REFINES
IF DESCRIPTION contains "fix", "bug", "issue", "correct", "patch" → FIXES
IF DESCRIPTION contains "replace", "remove", "deprecate", "migrate" → DEPRECATES

Display suggestion:
"Based on your description, this appears to be an EXTENDS relationship.
Is this correct? (The relationship affects how system specs are versioned)"
```

### 6. Output Summary

```markdown
## Extension Created: {BRANCH_NAME}

**Extends**: {EXTENDS} (Feature #{EXTENDS_ID})
**Relationship**: {RELATIONSHIP}

### Feature Lineage Established
- Parent spec loaded: specs/features/{EXTENDS}/spec.md
- System specs to update: {SYSTEM_SPECS}
- Parent status: {MERGED | IN_PROGRESS}

### Inherited Context Preview
[Brief summary from parent spec]

### Next Steps
1. Review the pre-populated Feature Lineage in your new spec
2. Complete the specification with new requirements
3. Run `/speckit.specify` to finalize (auto-handoff)

### Related Commands
- `/speckit.list --tree` - View feature evolution tree
- `/speckit.analyze --lineage` - Validate Feature Lineage
```

## Relationship Types Reference

| Relationship | Use When | Version Impact |
|--------------|----------|----------------|
| `EXTENDS` | Adding new capability | Minor version bump (1.0 → 1.1) |
| `REFINES` | Improving existing behavior | Patch version bump (1.0 → 1.0.1) |
| `FIXES` | Correcting bugs/issues | Patch version bump (1.0 → 1.0.1) |
| `DEPRECATES` | Replacing functionality | Major version bump (1.0 → 2.0) |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "Parent feature not found" | Invalid feature ID/name | Check `specs/features/` for available features |
| "Parent feature not merged" | Extending in-progress feature | Wait for parent to merge, or use `/speckit.specify` |
| "Circular extension detected" | A extends B extends A | Refactor feature hierarchy |
| "System spec mismatch" | Parent references non-existent system spec | Run `/speckit.analyze` on parent first |

## Example Usage

```bash
# Extend login feature with rate limiting
/speckit.extend 001-login "Add rate limiting to protect against brute force attacks"

# Fix bug in payment processing
/speckit.extend 005-payments --relationship FIXES "Fix decimal precision in currency conversion"

# Add 2FA to existing auth
/speckit.extend 001 "Add two-factor authentication support"

# Replace legacy notification system
/speckit.extend 010-notifications --relationship DEPRECATES "Replace email with push notifications"
```

## Integration with Merge Workflow

When the extension feature is merged via `/speckit.merge`:

1. **System Spec History** is updated with:
   ```markdown
   | 1.1 | {NEW_FEATURE} | EXTENDS | {DATE} | @author | {CHANGES} |
   ```

2. **Parent's "Extended By"** in manifest is updated

3. **Feature Lineage** is validated for consistency

4. **Evolution tree** can be viewed with `/speckit.list --tree`

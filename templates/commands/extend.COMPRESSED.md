---
description: Extend a merged feature with new capabilities. Creates a new feature branch with Feature Lineage pre-populated.
handoffs:
  - label: Complete Feature Specification
    agent: speckit.specify
    auto: true
    condition: ["Feature Lineage populated", "Parent context loaded"]
    gates: ["Feature Lineage has valid parent reference"]
  - label: View Parent Spec
    agent: speckit.view
    auto: false
  - label: Analyze Feature Lineage
    agent: speckit.analyze
    auto: false
scripts:
  sh: scripts/bash/create-new-feature.sh --json --extends "{PARENT}" "{DESCRIPTION}"
  ps: scripts/powershell/create-new-feature.ps1 -Json -Extends "{PARENT}" "{DESCRIPTION}"
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 4000
---

## Input
```text
$ARGUMENTS
```

Parse: **PARENT** (feature ID or name) and **DESCRIPTION** (new feature description)

---

## Purpose

Create a new feature that extends an already-merged feature with explicit **Feature Lineage** traceability.

**Use When**:
- Adding new capabilities to existing feature
- Enhancing merged feature behavior
- Fixing issues discovered in production
- Deprecating or replacing functionality

| Scenario | Use |
|----------|-----|
| Brand new feature | `/speckit.specify` |
| Modify merged feature | `/speckit.extend` ← this |
| Fix bug in merged feature | `/speckit.extend` with FIXES |
| Replace feature behavior | `/speckit.extend` with DEPRECATES |

---

## Execution Flow

### Step 1: Parse Arguments

```text
"/speckit.extend 001 Add rate limiting"
  → PARENT=001, DESCRIPTION="Add rate limiting"

"/speckit.extend 001 --relationship FIXES Fix login timeout"
  → PARENT=001, RELATIONSHIP=FIXES, DESCRIPTION="Fix login timeout"

DEFAULT: RELATIONSHIP = EXTENDS
```

### Step 2: Validate Parent

```bash
Run: scripts/bash/create-new-feature.sh --json --extends "{PARENT}" "{DESCRIPTION}"

Parse: BRANCH_NAME, SPEC_FILE, FEATURE_NUM, EXTENDS, EXTENDS_ID

IF error (parent not found) → show available features, ABORT
```

### Step 3: Load Parent Context

```text
Read:
  - specs/features/{EXTENDS}/spec.md → user stories, requirements, constraints
  - specs/features/{EXTENDS}/.merged → system specs, breaking changes, date
  - System Specs (if referenced) → current behavior, API contracts
```

### Step 4: Pre-populate Extension Spec

```markdown
## Context Inherited from Parent
<!-- Auto-populated from {EXTENDS}/spec.md -->

### Parent User Stories
[Key stories this extension relates to]

### Parent Constraints
[Constraints that must be respected]

### System Specs to Update
[From PARENT_MERGED.system_specs_created/updated]
```

### Step 5: Suggest Relationship Type

```text
Keywords → Relationship:
  "add", "new", "implement" → EXTENDS
  "improve", "enhance", "optimize" → REFINES
  "fix", "bug", "issue" → FIXES
  "replace", "remove", "deprecate" → DEPRECATES
```

### Step 6: Output

```markdown
## Extension Created: {BRANCH_NAME}

**Extends**: {EXTENDS} (Feature #{EXTENDS_ID})
**Relationship**: {RELATIONSHIP}

### Feature Lineage Established
- Parent spec: specs/features/{EXTENDS}/spec.md
- System specs to update: {SYSTEM_SPECS}

### Next Steps
1. Review pre-populated Feature Lineage
2. Complete specification with new requirements
3. Run `/speckit.specify` to finalize
```

---

## Relationship Types

| Relationship | Use When | Version Impact |
|--------------|----------|----------------|
| EXTENDS | Adding new capability | Minor (1.0 → 1.1) |
| REFINES | Improving existing behavior | Patch (1.0 → 1.0.1) |
| FIXES | Correcting bugs/issues | Patch (1.0 → 1.0.1) |
| DEPRECATES | Replacing functionality | Major (1.0 → 2.0) |

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Parent not found | Check `specs/features/` for available features |
| Parent not merged | Wait for parent to merge, or use `/speckit.specify` |
| Circular extension | Refactor feature hierarchy |
| System spec mismatch | Run `/speckit.analyze` on parent first |

---

## Example Usage

```bash
/speckit.extend 001-login "Add rate limiting to protect against brute force"
/speckit.extend 005-payments --relationship FIXES "Fix decimal precision"
/speckit.extend 010-notifications --relationship DEPRECATES "Replace email with push"
```

---

## Context

{ARGS}

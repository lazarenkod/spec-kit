---
description: Create or update the project constitution with layered architecture support (base → domain → project layers).
handoffs:
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
  - label: Analyze Compliance
    agent: speckit.analyze
    prompt: Check artifacts for constitution compliance
scripts:
  sh: echo "Constitution management - no prerequisites required"
  ps: Write-Host "Constitution management - no prerequisites required"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Layered Constitution Architecture

The constitution uses a 3-layer inheritance model:

```text
Layer 0: /memory/constitution.base.md ─── Enterprise defaults (READ-ONLY)
    ↓ inherits
Layer 1: /memory/constitution.domain.md ─ Domain-specific (fintech, healthcare, etc.)
    ↓ inherits
Layer 2: /memory/constitution.md ──────── Project overrides
```

**Inheritance Rules**:
- Higher layers INHERIT all principles from lower layers
- Higher layers can STRENGTHEN (SHOULD → MUST) but NEVER weaken (MUST → SHOULD)
- Higher layers can ADD new principles
- Higher layers can REFINE parameters (e.g., coverage 80% → 90%)

## Available Domains

| Domain | File | Use Cases |
|--------|------|-----------|
| fintech | `domains/fintech.md` | Payments, trading, banking, investment |
| healthcare | `domains/healthcare.md` | EHR, patient portals, HIPAA-regulated |
| e-commerce | `domains/e-commerce.md` | Online stores, marketplaces, checkout |
| saas | `domains/saas.md` | Multi-tenant B2B platforms |
| uxq | `domains/uxq.md` | B2C apps, dashboards, onboarding, forms, consumer products |

**Domain Combinations**: Domains can be combined for hybrid contexts:
- `uxq + saas` → Multi-tenant apps with consumer-grade UX
- `uxq + healthcare` → Patient-facing health applications
- `uxq + e-commerce` → Shopping experiences with delight moments

When combining domains, copy both to `constitution.domain.md` and merge principles (stricter level wins).

## Execution Flow

### 1. Determine Operation Mode

Parse user input for operation:

| User Says | Operation |
|-----------|-----------|
| "set domain fintech" | Select domain layer |
| "add principle" / "strengthen" | Modify project layer |
| "set language ru" / "язык русский" | Configure artifact language |
| "--merge" / "show effective" | Generate merged view |
| (no specific flag) | Interactive edit of project layer |

### 2. Load Existing Layers

Load available constitution layers:

```text
1. Read /memory/constitution.base.md (always exists)
2. Check if /memory/constitution.domain.md exists
   - If yes, read and identify domain
   - If no, note that no domain is selected
3. Read /memory/constitution.md (project layer)
```

### 3a. Domain Selection (if requested)

If user requests domain selection:

1. Validate domain exists in `/memory/domains/[domain].md`
2. Copy domain file to `/memory/constitution.domain.md`
3. Update project constitution header: `Domain Layer: [domain]`
4. Report domain principles added/strengthened

### 3b. Project Layer Edit (default)

If editing project layer:

1. Identify placeholder tokens `[ALL_CAPS_IDENTIFIER]`
2. Collect/derive values:
   - From user input if supplied
   - From repo context (README, docs, prior versions)
   - Dates: ISO format YYYY-MM-DD
3. Ensure overrides follow inheritance rules:
   - Cannot weaken base/domain MUST principles
   - Can strengthen SHOULD → MUST
   - Can add PRJ-xxx project principles

### 3c. Merge View (if --merge)

If generating merged view:

```text
FOR EACH principle in base:
  IF domain overrides it:
    Use domain version
  IF project overrides it:
    Use project version
  ELSE:
    Use base version

ADD domain-specific principles
ADD project-specific principles

OUTPUT merged constitution
```

### 3d. Project Settings (if "set language" or similar)

If configuring project settings:

1. Locate the **Project Settings** table in `/memory/constitution.md`
2. Update the requested setting:

   | Setting | Valid Values | Default |
   |---------|--------------|---------|
   | language | `en`, `ru`, `de`, `fr`, `es`, `zh`, `ja`, `ko`, `pt`, `it`, `pl`, `uk`, `ar`, `hi` | `en` |
   | date_format | `ISO`, `US`, `EU` | `ISO` |
   | measurements | `metric`, `imperial` | `metric` |

3. Report: "Project setting updated: language = ru"

**Language affects all artifact generation commands** (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.design`, `/speckit.concept`).

See `templates/shared/language-context.md` for language behavior details:
- All prose content generated in configured language
- IDs, technical terms, and code remain in English

### 4. Validation

Before finalizing:

- [ ] No unexplained bracket tokens remain
- [ ] No MUST → SHOULD weakening (violation = ERROR)
- [ ] Version updated if changes made
- [ ] Dates in ISO format

**Version Semantics**:
- MAJOR: Principle removal or incompatible redefinition
- MINOR: New principle or significant expansion
- PATCH: Clarifications, parameter tweaks

### 5. Consistency Propagation

Check dependent templates for alignment:

| File | Check |
|------|-------|
| `/templates/plan-template.md` | Constitution Check section aligns |
| `/templates/spec-template.md` | Requirements don't conflict with principles |
| `/templates/tasks-template.md` | Task types reflect principle domains |

### 6. Output

**Sync Impact Report** (as HTML comment in constitution):

```html
<!--
SYNC REPORT - [DATE]
Version: [OLD] → [NEW]
Domain: [DOMAIN or none]

Modified Principles:
- [ID]: [CHANGE]

Added Principles:
- [ID]: [NAME]

Templates Checked:
✅ plan-template.md
✅ spec-template.md
⚠ tasks-template.md (manual review needed)

Follow-up TODOs:
- [ITEM]
-->
```

**User Summary**:
- New version and bump rationale
- Domain status (active/none)
- Files flagged for manual follow-up
- Suggested commit message

## Examples

### Example 1: Select Domain

**Input**: "set domain fintech"

**Actions**:
1. Copy `/memory/domains/fintech.md` → `/memory/constitution.domain.md`
2. Update `/memory/constitution.md` header
3. Report: "Activated fintech domain. 6 principles strengthened, 6 domain principles added."

### Example 2: Strengthen Principle

**Input**: "strengthen QUA-001 to MUST with 95% coverage because we're building critical infrastructure"

**Actions**:
1. Add to Strengthened Principles table in constitution.md
2. Validate: base QUA-001 is SHOULD (can strengthen)
3. Version bump: MINOR (principle strength change)

### Example 3: Add Project Principle

**Input**: "add principle: all API responses must include request-id header for debugging"

**Actions**:
1. Create PRJ-001: Request ID Header
2. Set level: MUST
3. Add validation and violation severity
4. Version bump: MINOR (new principle)

### Example 4: View Effective Constitution

**Input**: "--merge"

**Actions**:
1. Merge all layers
2. Output complete effective constitution
3. Show principle count by domain and level

## Formatting Requirements

- Use Markdown headings exactly as in template
- Lines < 100 chars where practical
- Single blank line between sections
- No trailing whitespace
- Principle IDs: [DOMAIN]-[NNN] (e.g., SEC-001, PRJ-002)

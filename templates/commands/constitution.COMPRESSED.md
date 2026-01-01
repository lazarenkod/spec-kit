---
description: Create or update the project constitution with layered architecture support (base → domain → project layers)
handoffs:
  - label: Build Specification
    agent: speckit.specify
  - label: Analyze Compliance
    agent: speckit.analyze
scripts:
  sh: echo "Constitution management - no prerequisites required"
  ps: Write-Host "Constitution management - no prerequisites required"
claude_code:
  model: opus
  reasoning_mode: extended
  thinking_budget: 8000
  cache_hierarchy: full
---

## Input
```text
$ARGUMENTS
```

---

## Layered Architecture

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

---

## Available Domains

| Domain | Use Cases |
|--------|-----------|
| fintech | Payments, trading, banking, investment |
| healthcare | EHR, patient portals, HIPAA-regulated |
| e-commerce | Online stores, marketplaces, checkout |
| saas | Multi-tenant B2B platforms |
| uxq | B2C apps, dashboards, onboarding, forms |

**Combinations**: `uxq + saas` → Multi-tenant with consumer-grade UX

---

## Operation Modes

| User Says | Operation |
|-----------|-----------|
| "set domain fintech" | Select domain layer |
| "add principle" / "strengthen" | Modify project layer |
| "set language ru" | Configure artifact language |
| "--merge" / "show effective" | Generate merged view |
| (none) | Interactive edit of project layer |

---

## Execution Flow

### 1. Load Existing Layers

```text
1. Read /memory/constitution.base.md (always exists)
2. Check /memory/constitution.domain.md (if exists, identify domain)
3. Read /memory/constitution.md (project layer)
```

### 2a. Domain Selection

```text
1. Validate domain exists in /memory/domains/[domain].md
2. Copy → /memory/constitution.domain.md
3. Update project constitution header: Domain Layer: [domain]
4. Report principles added/strengthened
```

### 2b. Project Layer Edit

```text
1. Identify placeholder tokens [ALL_CAPS_IDENTIFIER]
2. Collect/derive values from user input, repo context, dates
3. Ensure overrides follow inheritance rules:
   - Cannot weaken base/domain MUST principles
   - Can strengthen SHOULD → MUST
   - Can add PRJ-xxx project principles
```

### 2c. Merge View (`--merge`)

```text
FOR EACH principle in base:
  Use domain override if exists
  Use project override if exists
ADD domain-specific principles
ADD project-specific principles
OUTPUT merged constitution
```

### 2d. Project Settings

| Setting | Valid Values | Default |
|---------|--------------|---------|
| language | en, ru, de, fr, es, zh, ja, ko, pt, it, pl, uk, ar, hi | en |
| date_format | ISO, US, EU | ISO |
| measurements | metric, imperial | metric |

---

## Validation

- [ ] No unexplained bracket tokens remain
- [ ] No MUST → SHOULD weakening (violation = ERROR)
- [ ] Version updated if changes made
- [ ] Dates in ISO format

**Version Semantics**:
- MAJOR: Principle removal or incompatible redefinition
- MINOR: New principle or significant expansion
- PATCH: Clarifications, parameter tweaks

---

## Output

```html
<!--
SYNC REPORT - [DATE]
Version: [OLD] → [NEW]
Domain: [DOMAIN or none]

Modified Principles: [ID]: [CHANGE]
Added Principles: [ID]: [NAME]

Templates Checked:
✅ plan-template.md
✅ spec-template.md
⚠ tasks-template.md (manual review needed)
-->
```

**User Summary**: Version bump rationale, domain status, files for follow-up, commit message.

---

## Examples

| Input | Action |
|-------|--------|
| "set domain fintech" | Copy domains/fintech.md → constitution.domain.md |
| "strengthen QUA-001 to MUST with 95% coverage" | Add to Strengthened Principles, bump MINOR |
| "add principle: all API responses must include request-id header" | Create PRJ-001, set MUST, bump MINOR |
| "--merge" | Output complete effective constitution |

---

## Formatting

- Markdown headings exactly as template
- Lines < 100 chars
- Single blank line between sections
- Principle IDs: [DOMAIN]-[NNN] (e.g., SEC-001, PRJ-002)

---

## Context

{ARGS}

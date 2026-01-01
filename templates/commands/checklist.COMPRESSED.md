---
description: Generate a custom checklist for the current feature based on user requirements
persona: product-agent
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 4000
  cache_hierarchy: full
---

## Input
```text
$ARGUMENTS
```

---

## Core Concept: "Unit Tests for Requirements"

**Checklists validate REQUIREMENTS QUALITY, NOT implementation behavior.**

| ❌ WRONG (Tests Implementation) | ✅ CORRECT (Tests Requirements) |
|---------------------------------|---------------------------------|
| "Verify button displays correctly" | "Are button visual specs defined with states?" |
| "Test error handling works" | "Are error handling requirements specified for all failure modes?" |
| "Confirm API returns 200" | "Are success response formats documented?" |
| "Check hover state works" | "Are hover state requirements consistent across components?" |

**Quality Dimensions** (tag each item):
- `[Completeness]` - Are all requirements present?
- `[Clarity]` - Are requirements unambiguous?
- `[Consistency]` - Do requirements align?
- `[Measurability]` - Can requirements be verified?
- `[Coverage]` - Are all scenarios addressed?
- `[Gap]` - Missing requirement detected

---

## Workflow (7 Steps)

```text
1. Setup: Run {SCRIPT} → FEATURE_DIR, AVAILABLE_DOCS

2. Clarify intent: Generate up to 3 contextual questions:
   - Scope refinement, risk prioritization, depth calibration
   - Skip if already unambiguous in $ARGUMENTS
   - Defaults: Standard depth, Reviewer audience, Top 2 clusters

3. Understand request: Combine $ARGUMENTS + answers:
   - Derive theme (security, review, deploy, ux)
   - Map focus selections to categories

4. Load context: Read from FEATURE_DIR:
   - spec.md (requirements), plan.md (technical), tasks.md (implementation)
   - Progressive disclosure: summarize, don't dump

5. Generate checklist:
   - Create FEATURE_DIR/checklists/{domain}.md
   - Number items: CHK001, CHK002...
   - Group by quality dimension
   - ≥80% items must have [Spec §X.Y] or [Gap] traceability

6. Apply template: Use templates/checklist-template.md format

7. Report: Output path, item count, focus areas
```

---

## Item Patterns

**✅ REQUIRED PATTERNS**:
```text
- "Are [requirements] defined/specified/documented for [scenario]?"
- "Is [vague term] quantified/clarified with specific criteria?"
- "Are requirements consistent between [section A] and [section B]?"
- "Can [requirement] be objectively measured?"
- "Does the spec define [missing aspect]?"
```

**🚫 PROHIBITED PATTERNS** (implementation tests):
```text
- "Verify/Test/Confirm/Check" + behavior
- "displays correctly", "works properly", "functions as expected"
- "click", "navigate", "render", "load", "execute"
```

**Example Items by Dimension**:

| Dimension | Example |
|-----------|---------|
| Completeness | "Are error handling requirements defined for all API failure modes? [Gap]" |
| Clarity | "Is 'fast loading' quantified with specific timing thresholds? [Clarity, Spec §NFR-2]" |
| Consistency | "Do navigation requirements align across all pages? [Consistency, Spec §FR-10]" |
| Coverage | "Are zero-state scenarios (no data) addressed? [Coverage, Edge Case]" |
| Measurability | "Can 'visual hierarchy' be objectively verified? [Measurability, Spec §FR-1]" |

---

## Self-Review Phase [REF:SR-001]

### Quality Criteria

| ID | Check | Severity |
|----|-------|----------|
| SR-CHK-01 | No implementation tests | CRITICAL |
| SR-CHK-02 | All items test requirement quality | CRITICAL |
| SR-CHK-03 | CHK IDs sequential (no gaps) | HIGH |
| SR-CHK-04 | Quality dimensions tagged | HIGH |
| SR-CHK-05 | ≥80% traceability ([Spec §X.Y] or [Gap]) | HIGH |
| SR-CHK-06 | No prohibited words + behavior | CRITICAL |
| SR-CHK-07 | Required patterns used | HIGH |
| SR-CHK-08 | Categories structured | MEDIUM |
| SR-CHK-09 | 10-40 items (consolidate if >40) | MEDIUM |
| SR-CHK-10 | No duplicates | MEDIUM |

### Anti-Pattern Detection

```text
PROHIBITED_PATTERNS = [
  /^Verify .* (displays|works|renders|loads|executes)/i,
  /^Test .* (correctly|properly|successfully)/i,
  /^Confirm .* (navigates|responds|behaves)/i,
  /displays correctly|works properly|functions as expected/i
]

FOR EACH item: IF matches any → ERROR, rewrite
```

### Verdict Logic

```text
PASS: No prohibited patterns, ≥80% required patterns → complete
FAIL: Prohibited pattern found → self-correct (max 3 iterations)
WARN: Low pattern coverage → proceed with warning
```

### Rewrite Examples

| WRONG | CORRECT |
|-------|---------|
| "Verify page loads in <2s" | "Are performance requirements quantified with thresholds?" |
| "Test form submits data" | "Are form submission and validation rules defined?" |
| "Check hover state works" | "Are hover states consistently defined across components?" |

---

## Output Format

```text
┌─────────────────────────────────────────────────────────────┐
│ /speckit.checklist Complete                                  │
├─────────────────────────────────────────────────────────────┤
│ Checklist: {domain}.md                                       │
│ Items: {count}                                               │
│                                                              │
│ Focus Areas: {areas}                                         │
│ Depth: {Standard|Thorough|Light}                            │
│ Audience: {Author|Reviewer|QA}                              │
│                                                              │
│ Quality Dimensions:                                          │
│   Completeness: {n}  Clarity: {n}  Consistency: {n}         │
│   Coverage: {n}  Measurability: {n}                         │
│                                                              │
│ Self-Review: {PASS|WARN}                                    │
│ Traceability: {n}% with references                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Context

{ARGS}

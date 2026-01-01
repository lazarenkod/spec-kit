---
description: Capture complete service concept before detailed specification
persona: product-agent
handoffs:
  - { label: Create Specification, agent: speckit.specify, auto: true }
  - { label: Validate Concept, agent: speckit.analyze, auto: false }
claude_code:
  model: opus
  reasoning_mode: extended
  thinking_budget: 10000
  cache_control: {system_prompt: ephemeral, constitution: ephemeral, templates: ephemeral}
  semantic_cache: {enabled: true, encoder: all-MiniLM-L6-v2, threshold: 0.95, scope: session}
  cache_hierarchy: full
  plan_mode_trigger: true
skills: [market-research, ux-audit]
scripts:
  sh: scripts/bash/create-concept.sh --json "{ARGS}"
  ps: scripts/powershell/create-concept.ps1 -Json "{ARGS}"
---

## Input
```text
$ARGUMENTS
```

---

## Init [REF:INIT-001]

```text
EXECUTE language-loading → ARTIFACT_LANGUAGE
EXECUTE project-type-detection → PROJECT_TYPE, REQUIRED_FOUNDATIONS
```

---

## Mode Detection

| Mode | Triggers | Action |
|------|----------|--------|
| **Discovery** | Vague terms ("maybe", "like X but..."), single-sentence, uncertainty | Execute Phases 0a-0c |
| **Capture** | Structured lists (3+ items), personas named, metrics stated | Skip to Step 5 |
| **Validation** | concept.md exists, missing sections, CQS < 60 | Add missing sections |

---

## Phase 0: Discovery Mode

### 0a: Problem Discovery

| Question | Listen For |
|----------|-----------|
| What frustration triggered this? | Pain points, workarounds |
| How many face this? How often? | Market size, frequency |
| Current solutions? What's wrong? | Competitor gaps |
| What happens if unsolved? Cost? | Urgency, willingness to pay |
| Ideal outcome if solved? | Success criteria, features |

### 0b: Market Research

**Actions** (use WebSearch):
1. Competitor analysis → feature gaps, pricing, complaints
2. Market trends → growth signals, investment activity
3. User pain points → unmet needs, workarounds

**TAM/SAM/SOM Output**:
```text
| Metric | Value | Calculation | Source |
|--------|-------|-------------|--------|
| TAM | $XB | Total addressable market | [Source] |
| SAM | $XM | TAM × segment filters | [Source] |
| SOM | $XM | SAM × realistic capture | [Assumptions] |
```

**Competitive Matrix**:
```text
| Capability | Us | Comp A | Comp B | Gap |
|------------|:--:|:------:|:------:|-----|
| Feature 1 | ✓+ | ✓ | ✗ | Differentiation |
```

### 0c: Concept Synthesis

```text
Synthesize findings into structured concept:
- Vision statement (single sentence)
- Value proposition (problem → solution → benefit)
- Key differentiators (3-5 points)
- Target personas with JTBD
```

---

## Workflow (11 Steps)

### Steps 1-4: Setup
1. Initialize `specs/concept.md` from template
2. Mode detection (Discovery/Capture/Validation)
3. Project type detection
4. Load constitution and foundations

### Step 5: Extract Vision

| Element | Format |
|---------|--------|
| Vision Statement | Single concrete sentence (no vague words) |
| Value Proposition | Problem → Solution → Benefit chain |
| Key Differentiators | 3-5 specific competitive advantages |

### Step 6: Build Feature Hierarchy

**ID Format**:
- Epic: `EPIC-001`, `EPIC-002`
- Feature: `EPIC-001.F01`, `EPIC-001.F02`
- Story: `EPIC-001.F01.S01`

**Priority Format**:
- `P1a/b/c`: MVP critical path (ordered)
- `P2a/b`: Important post-MVP
- `P3`: Nice-to-have

### Step 7: Map User Journeys

```text
FOR EACH persona:
  1. Identify primary goal
  2. Map steps to achieve goal
  3. Link each step to Feature ID
  4. Document edge cases
  5. Note journey intersections
```

**Golden Path (J000)**: Core journey validating Wave 1-2 completion

### Step 8: Detect Foundations & Dependencies

**Foundation Patterns**:
| Type | Patterns | Wave |
|------|----------|------|
| AUTH | auth*, login*, signin*, oauth* | 1 |
| USER_MGMT | user*, account*, profile*, role* | 1 |
| CORE_DATA | schema*, database*, migration* | 1 |
| NAV | nav*, route*, menu*, sidebar* | 2 |
| LAYOUT | layout*, shell*, header*, footer* | 1 |

**Dependency Matrix**: Build DAG, detect cycles

### Step 9: Assign Waves

| Wave | Content | Priority |
|------|---------|----------|
| Wave 1 | Foundation Layer (AUTH, LAYOUT, DATA) | P1a |
| Wave 2 | Experience Layer (NAV, FTUE, FEEDBACK) | P1b |
| Wave 3+ | Business Features | P2+ |

### Step 10: Capture Ideas Backlog

```text
- [ ] [Idea] - not started
- [?] [Idea] - needs validation
- [>] [Idea] - deferred
- [x] [Idea] - rejected (with reason)
```

### Step 11: Write concept.md

---

## CQS Calculation [REF:VG-002]

**Formula**: `CQS = (Market×0.25 + Persona×0.20 + Metrics×0.15 + Features×0.20 + Risk×0.10 + Tech×0.10) × 100`

| Component | Scoring Criteria |
|-----------|------------------|
| Market (25%) | TAM/SAM/SOM (55), Competitive Matrix (25), Validation Signals (20) |
| Persona (20%) | 2+ personas (30), JTBD tables (40), WTP (15), Success criteria (15) |
| Metrics (15%) | North Star (40), SMART validation (40), Leading/lagging (20) |
| Features (20%) | Hierarchy valid (40), Waves complete (30), Golden Path (30) |
| Risk (10%) | 3+ risks (40), Mitigations (30), Pivot criteria (30) |
| Technical (10%) | Domain entities (40), API estimation (30), Constitution review (30) |

**Quality Gate**:
| CQS | Status |
|-----|--------|
| ≥ 80 | Ready for specification |
| 60-79 | Proceed with caution |
| < 60 | Not ready — complete discovery |

---

## Self-Review Phase [REF:SR-001]

### Quality Criteria

| ID | Check | Severity |
|----|-------|----------|
| SR-CONCEPT-01 | Vision concrete (no vague words) | CRITICAL |
| SR-CONCEPT-02 | 2+ personas with goals | CRITICAL |
| SR-CONCEPT-03 | All IDs follow format | CRITICAL |
| SR-CONCEPT-04 | Epics have Features | HIGH |
| SR-CONCEPT-05 | Features have Stories | HIGH |
| SR-CONCEPT-06 | IDs unique | CRITICAL |
| SR-CONCEPT-07 | No circular dependencies | CRITICAL |
| SR-CONCEPT-08 | 1+ journey per persona | HIGH |
| SR-CONCEPT-11 | Foundation layer populated | CRITICAL |
| SR-CONCEPT-14 | Golden Path (J000) exists | CRITICAL |
| SR-CONCEPT-16 | TAM/SAM/SOM present | HIGH |
| SR-CONCEPT-17 | JTBD personas | HIGH |
| SR-CONCEPT-21 | CQS calculated | HIGH |
| SR-CONCEPT-22 | CQS ≥ 60 | HIGH |

### Validation Loop

```text
FOR iteration IN 1..3:
  Validate hierarchy structure
  Check foundation layer
  Calculate CQS
  IF all pass → BREAK
  ELSE → self-correct, re-validate

VERDICT:
  PASS: CRITICAL=0, HIGH=0 → handoff
  WARN: Only MEDIUM → proceed with warnings
  FAIL: CRITICAL>0 → fix, retry (max 3)
```

---

## Output Structure

```text
specs/concept.md with:
- Vision Statement
- Value Proposition
- User Personas (with JTBD)
- Feature Hierarchy (EPIC > Feature > Story)
- User Journeys (including Golden Path J000)
- Execution Order (Waves 1-3+)
- Dependencies (Mermaid DAG)
- Ideas Backlog
- Technical Discovery Hints
- Traceability Skeleton
- CQS Score
```

---

## Report Format

```text
┌────────────────────────────────────────────────────┐
│ /speckit.concept Complete                           │
├────────────────────────────────────────────────────┤
│ Mode: {Discovery | Capture | Validation}            │
│ Epics: {N}  Features: {M}  Stories: {K}            │
│ Ideas Backlog: {L} items                            │
│                                                     │
│ CQS: {score}/100 ({status})                         │
│ Golden Path: {defined | missing}                    │
│ Dependencies: DAG {valid | cycles detected}         │
├────────────────────────────────────────────────────┤
│ Wave Distribution:                                  │
│   Wave 1 (Foundation): {N} features                 │
│   Wave 2 (Experience): {M} features                 │
│   Wave 3+ (Business):  {K} features                 │
└────────────────────────────────────────────────────┘
```

### Next Steps

```text
IF CQS >= 80:
  → /speckit.specify EPIC-001.F01.S01 (start Wave 1)
ELIF CQS >= 60:
  → Proceed with caution, flag gaps
ELSE:
  → Complete discovery before specification
```

---

## Context

{ARGS}

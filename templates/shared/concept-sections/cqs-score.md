# Concept Quality Score (CQS) — Evidence-Based (CQS-E)

> **Purpose**: Quantify concept readiness with evidence quality tracking before proceeding to specification.

## CQS-E Calculation

**Formula**:
```
CQS-E = (
  Market × 0.20 +
  Persona × 0.15 +
  Metrics × 0.15 +
  Features × 0.15 +
  Risk × 0.10 +
  Technical × 0.10 +
  Strategic × 0.10 +      # NEW: Framework completeness
  Validation × 0.05       # NEW: Hypothesis test status
) × 100 × Evidence_Multiplier
```

| Component | Score | Weight | Weighted | Evidence Quality | Notes |
|-----------|:-----:|:------:|:--------:|:----------------:|-------|
| Market Validation | /100 | 0.20 | | HIGH/MED/LOW | [Gaps to address] |
| Persona Depth | /100 | 0.15 | | HIGH/MED/LOW | [Gaps to address] |
| Metrics Quality | /100 | 0.15 | | HIGH/MED/LOW | [Gaps to address] |
| Feature Completeness | /100 | 0.15 | | HIGH/MED/LOW | [Gaps to address] |
| Risk Assessment | /100 | 0.10 | | HIGH/MED/LOW | [Gaps to address] |
| Technical Hints | /100 | 0.10 | | HIGH/MED/LOW | [Gaps to address] |
| **Strategic Depth** | /100 | 0.10 | | HIGH/MED/LOW | [Framework coverage] |
| **Validation Rigor** | /100 | 0.05 | | HIGH/MED/LOW | [Hypothesis status] |
| **Base CQS** | | | **/100** | | |
| **Evidence Multiplier** | | | **×[0.8-1.2]** | | |
| **CQS-E Total** | | | **/120** | | |

---

## Evidence Multiplier

Adjust CQS based on citation and evidence quality:

| Multiplier | Criteria | Description |
|:----------:|----------|-------------|
| **1.2** | All claims sourced | Primary research, verified data, recent citations |
| **1.1** | Most claims sourced | Credible secondary sources, some primary |
| **1.0** | Adequate sourcing | Mix of sourced and reasoned assumptions |
| **0.9** | Partial sourcing | Some claims lack evidence |
| **0.8** | Weak sourcing | Most claims unsourced or outdated |

**Current Evidence Multiplier**: [1.2/1.1/1.0/0.9/0.8] — [Justification]

---

## Quality Gate

| CQS Range | Status | Recommendation |
|-----------|:------:|----------------|
| **80-100** | ✅ Ready | Proceed to `/speckit.specify` with high confidence |
| **60-79** | ⚠️ Caution | Proceed but flag gaps during specification |
| **< 60** | ⛔ Not Ready | Complete discovery before specification |

**Current Status**: [✅/⚠️/⛔] — [Recommendation]

---

## Component Scoring Criteria

### Market Validation (25% weight)

| Criterion | Points | Achieved | Score |
|-----------|:------:|:--------:|:-----:|
| TAM defined with methodology | 30 | ✓/✗ | |
| SAM calculated with filters | 25 | ✓/✗ | |
| SOM estimated realistically | 20 | ✓/✗ | |
| Competitive matrix completed | 25 | ✓/✗ | |
| **Subtotal** | 100 | | **/100** |

### Persona Depth (20% weight)

| Criterion | Points | Achieved | Score |
|-----------|:------:|:--------:|:-----:|
| ≥2 distinct personas defined | 30 | ✓/✗ | |
| JTBD (functional) for each | 25 | ✓/✗ | |
| JTBD (emotional/social) for each | 15 | ✓/✗ | |
| Willingness to pay assessed | 15 | ✓/✗ | |
| Success criteria per persona | 15 | ✓/✗ | |
| **Subtotal** | 100 | | **/100** |

### Metrics Quality (15% weight)

| Criterion | Points | Achieved | Score |
|-----------|:------:|:--------:|:-----:|
| North Star metric identified | 40 | ✓/✗ | |
| All metrics pass SMART validation | 30 | ✓/✗ | |
| Leading indicators defined | 15 | ✓/✗ | |
| Lagging indicators defined | 15 | ✓/✗ | |
| **Subtotal** | 100 | | **/100** |

### Feature Completeness (15% weight)

| Criterion | Points | Achieved | Score |
|-----------|:------:|:--------:|:-----:|
| Epic/Feature/Story hierarchy | 30 | ✓/✗ | |
| Wave assignments (1/2/3+) | 25 | ✓/✗ | |
| Golden Path (J000) defined | 25 | ✓/✗ | |
| UX Foundations identified | 20 | ✓/✗ | |
| **Subtotal** | 100 | | **/100** |

### Risk Assessment (10% weight)

| Criterion | Points | Achieved | Score |
|-----------|:------:|:--------:|:-----:|
| ≥3 risks identified | 30 | ✓/✗ | |
| Mitigations documented | 25 | ✓/✗ | |
| Contingencies defined | 15 | ✓/✗ | |
| Pivot criteria documented | 30 | ✓/✗ | |
| **Subtotal** | 100 | | **/100** |

### Technical Hints (10% weight)

| Criterion | Points | Achieved | Score |
|-----------|:------:|:--------:|:-----:|
| Domain entities sketched | 35 | ✓/✗ | |
| API surface estimated | 25 | ✓/✗ | |
| Integration complexity assessed | 20 | ✓/✗ | |
| Constitution conflicts resolved | 20 | ✓/✗ | |
| **Subtotal** | 100 | | **/100** |

### Strategic Depth (10% weight) — NEW

| Criterion | Points | Achieved | Score |
|-----------|:------:|:--------:|:-----:|
| PR/FAQ completed (Amazon format) | 25 | ✓/✗ | |
| Blue Ocean Canvas (ERRC grid) | 20 | ✓/✗ | |
| Business Model Canvas with unit economics | 20 | ✓/✗ | |
| Three Horizons allocation | 15 | ✓/✗ | |
| Trade-off Resolution hierarchy | 10 | ✓/✗ | |
| Scope Exclusions documented | 10 | ✓/✗ | |
| **Subtotal** | 100 | | **/100** |

### Validation Rigor (5% weight) — NEW

| Criterion | Points | Achieved | Score |
|-----------|:------:|:--------:|:-----:|
| ≥3 hypotheses documented | 30 | ✓/✗ | |
| At least 1 per type (D/F/V) | 25 | ✓/✗ | |
| Evidence collected for each | 25 | ✓/✗ | |
| Pre-mortem scenarios documented | 20 | ✓/✗ | |
| **Subtotal** | 100 | | **/100** |

---

## Validation Checklist

Complete these items to improve CQS:

### Market (if score < 80)
- [ ] Calculate TAM with bottom-up or top-down methodology
- [ ] Define SAM with geographic/segment filters
- [ ] Estimate SOM with realistic market share assumptions
- [ ] Complete competitive positioning matrix

### Persona (if score < 80)
- [ ] Define at least 2 distinct personas
- [ ] Document functional JTBD for each persona
- [ ] Assess willingness to pay for each persona
- [ ] Define success criteria and deal breakers

### Metrics (if score < 80)
- [ ] Identify North Star metric with rationale
- [ ] Validate all metrics against SMART criteria
- [ ] Define leading indicators (predictive)
- [ ] Define lagging indicators (outcome)

### Features (if score < 80)
- [ ] Structure features as Epic → Feature → Story
- [ ] Assign wave priorities (Wave 1/2/3+)
- [ ] Define Golden Path journey (J000)
- [ ] Identify required UX Foundations

### Risk (if score < 80)
- [ ] Identify at least 3 significant risks
- [ ] Document mitigation for each risk
- [ ] Define contingency plans
- [ ] Establish pivot criteria and kill criteria

### Technical (if score < 80)
- [ ] Sketch key domain entities
- [ ] Estimate API surface (endpoints count)
- [ ] Assess external integration complexity
- [ ] Check for constitution principle conflicts

### Strategic (if score < 80) — NEW
- [ ] Complete PR/FAQ using Amazon Working Backwards
- [ ] Fill Blue Ocean Canvas (ERRC grid)
- [ ] Document Business Model Canvas with unit economics
- [ ] Allocate features to Three Horizons
- [ ] Define Trade-off Resolution hierarchy
- [ ] Document explicit Scope Exclusions

### Validation (if score < 80) — NEW
- [ ] Document at least 3 hypotheses (HYP-001 format)
- [ ] Include at least 1 Desirability, 1 Feasibility, 1 Viability hypothesis
- [ ] Collect evidence for each hypothesis
- [ ] Document Pre-Mortem failure scenarios

---

## CQS History

Track CQS evolution across iterations:

| Date | CQS | Change | Key Improvements |
|------|:---:|:------:|------------------|
| [Date] | [Score] | — | Initial assessment |
| [Date] | [Score] | +[X] | [What was added/improved] |
| [Date] | [Score] | +[X] | [What was added/improved] |

---

## Next Steps Based on CQS

### If CQS ≥ 80
1. ✅ Proceed to `/speckit.specify` for feature specification
2. Use concept as source of truth for requirements
3. Reference personas and metrics during specification

### If CQS 60-79
1. ⚠️ Review gaps highlighted in component scores
2. Decide: Address gaps now OR proceed with documented risks
3. If proceeding, flag incomplete areas during specification

### If CQS < 60
1. ⛔ Do not proceed to specification
2. Address highest-weight gaps first (Market, Features, Persona)
3. Re-run `/speckit.concept` in Validation Mode
4. Target CQS ≥ 60 before specification

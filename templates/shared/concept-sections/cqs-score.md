# Concept Quality Score (CQS)

> **Purpose**: Quantify concept readiness before proceeding to specification.

## CQS Calculation

**Formula**: `CQS = (Market × 0.25 + Persona × 0.20 + Metrics × 0.15 + Features × 0.20 + Risk × 0.10 + Technical × 0.10) × 100`

| Component | Score | Weight | Weighted | Notes |
|-----------|:-----:|:------:|:--------:|-------|
| Market Validation | /100 | 0.25 | | [Gaps to address] |
| Persona Depth | /100 | 0.20 | | [Gaps to address] |
| Metrics Quality | /100 | 0.15 | | [Gaps to address] |
| Feature Completeness | /100 | 0.20 | | [Gaps to address] |
| Risk Assessment | /100 | 0.10 | | [Gaps to address] |
| Technical Hints | /100 | 0.10 | | [Gaps to address] |
| **CQS Total** | | | **/100** | |

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

### Feature Completeness (20% weight)

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

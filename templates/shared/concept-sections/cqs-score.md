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
  Strategic × 0.05 +      # Framework completeness
  Validation × 0.05 +     # Hypothesis test status
  Transparency × 0.05     # NEW: Decision transparency
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
| **Strategic Depth** | /100 | 0.05 | | HIGH/MED/LOW | [Framework coverage] |
| **Validation Rigor** | /100 | 0.05 | | HIGH/MED/LOW | [Hypothesis status] |
| **Transparency** | /100 | 0.05 | | HIGH/MED/LOW | [Decision rationale] |
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

## Evidence-Based Scoring (Enhanced)

> **Upgrade**: Replace binary (✓/✗) with evidence tier scoring for higher accuracy.

### Evidence Tiers

| Tier | Code | Points | Criteria |
|------|:----:|:------:|----------|
| **VERY_STRONG** | VS | 30 | Primary research (n≥10), verified data, multiple independent sources |
| **STRONG** | S | 25 | Credible secondary sources, recent data (<1 year), industry reports |
| **MEDIUM** | M | 20 | Analyst estimates, expert opinions, comparable company data |
| **WEAK** | W | 5 | Assumptions, extrapolations, outdated data (>2 years) |
| **NONE** | N | 0 | No evidence provided |

### Minimum Evidence Requirements

| Component | Critical Claim | Minimum Evidence | Tier Required |
|-----------|----------------|------------------|:-------------:|
| **Market** | TAM Calculation | ≥3 independent sources | STRONG |
| **Market** | Competitive Matrix | ≥3 competitors with pricing | STRONG |
| **Persona** | Persona Definition | ≥5 interviews OR ≥100 surveys | STRONG |
| **Persona** | Willingness to Pay | Pricing research conducted | STRONG |
| **Metrics** | North Star Metric | ≥2 comparable benchmarks | STRONG |
| **Features** | Golden Path | Validated with ≥3 users | STRONG |
| **Technical** | Domain Entities | Architecture review OR prototype | STRONG |

---

## Source Credibility Matrix

Assign evidence tier based on source type and recency:

| Source Type | Base Tier | Recency Adjustment | Final Tier |
|-------------|:---------:|:------------------:|:----------:|
| Primary research (n≥10) | VS | None | VS |
| Industry report (Gartner, Forrester, IDC) | VS | -1 tier if >1 year old | S |
| Official company data (10-K, S-1) | S | -1 tier if >6 months old | M |
| Review platforms (G2, Capterra, TrustRadius) | S | -1 tier if >1 year old | M |
| Community forums (Reddit, HN) | M | -1 tier if >6 months old | W |
| Social media mentions | M | -1 tier if >3 months old | W |
| Expert opinion (no data backing) | W | N/A | W |
| PM assumption (no source) | N | N/A | N |

### Recency Decay Formula

```
Tier_Final = Tier_Base - floor((Age_Days / Decay_Threshold_Days))

Decay Thresholds:
- Industry reports: 365 days
- Review platforms: 365 days
- Community forums: 180 days
- Social media: 90 days
- Company filings: 180 days
```

### Tier Decay Examples

| Source | Age | Decay Threshold | Tiers Lost | Final Tier |
|--------|:---:|:---------------:|:----------:|:----------:|
| Gartner 2024 | 400 days | 365 | 1 | S → M |
| G2 Review | 200 days | 365 | 0 | S → S |
| Reddit Post | 200 days | 180 | 1 | M → W |

### Conflict Detection Rules

When multiple sources provide contradictory information:

| Scenario | Resolution | Action |
|----------|------------|--------|
| Same tier, different values | Average values, note variance | Flag if variance >30% |
| Higher tier vs lower tier | Use higher tier value | Note discrepancy in registry |
| All sources weak/none | Mark claim as UNVALIDATED | Block if critical claim |
| Conflicting qualitative claims | Document both perspectives | Require human resolution |

**Conflict Registry**:

| ID | Claims | Sources | Discrepancy | Resolution | Resolved By |
|:--:|--------|---------|-------------|------------|:-----------:|
| CF-001 | [Claim A vs B] | [EV-X vs EV-Y] | [% or description] | [How resolved] | AI/Human |

---

### Evidence Gap Report

| Component | Claim | Current | Required | Gap | Priority |
|-----------|-------|:-------:|:--------:|:---:|:--------:|
| [Component] | [Claim] | [N/W/M/S/VS] | [Tier] | [-X pts] | [P0/P1/P2] |

**Total Evidence Gap**: [X] points — [Action required]

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

### Market Validation (20% weight)

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| TAM defined with methodology | 30 | N/W/M/S/VS | | [Source IDs] |
| SAM calculated with filters | 25 | N/W/M/S/VS | | [Source IDs] |
| SOM estimated realistically | 20 | N/W/M/S/VS | | [Source IDs] |
| Competitive matrix completed | 25 | N/W/M/S/VS | | [Source IDs] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- TAM: ≥3 independent sources, bottom-up AND top-down (variance <30%)
- Competitors: ≥3 analyzed with pricing data

### Persona Depth (15% weight)

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| ≥2 distinct personas defined | 30 | N/W/M/S/VS | | [Source IDs] |
| JTBD (functional) for each | 25 | N/W/M/S/VS | | [Source IDs] |
| JTBD (emotional/social) for each | 15 | N/W/M/S/VS | | [Source IDs] |
| Willingness to pay assessed | 15 | N/W/M/S/VS | | [Source IDs] |
| Success criteria per persona | 15 | N/W/M/S/VS | | [Source IDs] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- Personas: ≥5 customer interviews OR ≥100 survey responses
- WTP: Van Westendorp analysis OR pricing research conducted

### Metrics Quality (15% weight)

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| North Star metric identified | 40 | N/W/M/S/VS | | [Source IDs] |
| All metrics pass SMART validation | 30 | N/W/M/S/VS | | [Source IDs] |
| Leading indicators defined | 15 | N/W/M/S/VS | | [Source IDs] |
| Lagging indicators defined | 15 | N/W/M/S/VS | | [Source IDs] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- North Star: ≥2 comparable company benchmarks
- SMART: Each metric has baseline + target with measurement methodology

### Feature Completeness (15% weight)

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| Epic/Feature/Story hierarchy | 30 | N/W/M/S/VS | | [Source IDs] |
| Wave assignments (1/2/3+) | 25 | N/W/M/S/VS | | [Source IDs] |
| Golden Path (J000) defined | 25 | N/W/M/S/VS | | [Source IDs] |
| UX Foundations identified | 20 | N/W/M/S/VS | | [Source IDs] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- Golden Path: Validated with ≥3 target users
- Feature hierarchy: Each feature traced to ≥1 JTBD

### Risk Assessment (10% weight)

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| ≥3 risks identified | 30 | N/W/M/S/VS | | [Source IDs] |
| Mitigations documented | 25 | N/W/M/S/VS | | [Source IDs] |
| Contingencies defined | 15 | N/W/M/S/VS | | [Source IDs] |
| Pivot criteria documented | 30 | N/W/M/S/VS | | [Source IDs] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- Risks: Industry research OR expert consultation
- Pivot criteria: Quantitative thresholds defined

### Technical Hints (10% weight)

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| Domain entities sketched | 35 | N/W/M/S/VS | | [Source IDs] |
| API surface estimated | 25 | N/W/M/S/VS | | [Source IDs] |
| Integration complexity assessed | 20 | N/W/M/S/VS | | [Source IDs] |
| Constitution conflicts resolved | 20 | N/W/M/S/VS | | [Source IDs] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- Domain entities: Architecture review OR working prototype
- Integrations: Documentation review completed

### Strategic Depth (5% weight)

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| **Product Alternatives generated** ← NEW | **30** | N/W/M/S/VS | | [Source IDs] |
| PR/FAQ completed (Amazon format) | 15 | N/W/M/S/VS | | [Source IDs] |
| Blue Ocean Canvas (ERRC grid) | 15 | N/W/M/S/VS | | [Source IDs] |
| Business Model Canvas with unit economics | 15 | N/W/M/S/VS | | [Source IDs] |
| Three Horizons allocation | 10 | N/W/M/S/VS | | [Source IDs] |
| Trade-off Resolution hierarchy | 10 | N/W/M/S/VS | | [Source IDs] |
| Scope Exclusions documented | 5 | N/W/M/S/VS | | [Source IDs] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- **Product Alternatives**: ≥3 alternatives documented with scoring (Problem Fit, Differentiation, Feasibility, Time)
- **Selection Rationale**: Clear explanation of why chosen alternative over others
- Unit economics: Based on actual cost data OR comparable company analysis
- Blue Ocean: Competitive differentiation validated with users

**Scoring Logic for Product Alternatives**:
```
IF alternatives_count >= 5 AND selected_alternative documented AND selection_rationale >= 3 reasons:
    SCORE = 30 points
ELIF alternatives_count >= 3 AND selected_alternative documented:
    SCORE = 25 points
ELIF alternatives_count >= 3:
    SCORE = 15 points
ELSE:
    SCORE = 0 points
```

### Validation Rigor (5% weight)

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| ≥3 hypotheses documented | 30 | N/W/M/S/VS | | [Source IDs] |
| At least 1 per type (D/F/V) | 25 | N/W/M/S/VS | | [Source IDs] |
| Evidence collected for each | 25 | N/W/M/S/VS | | [Source IDs] |
| Pre-mortem scenarios documented | 20 | N/W/M/S/VS | | [Source IDs] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- Hypotheses: Each has testable success criteria
- Pre-mortem: Based on industry failure analysis

### Transparency (5% weight)

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| Per-feature JTBD links (>80%) | 30 | N/W/M/S/VS | | [Source IDs] |
| At least 3 reasoning traces (Problem→JTBD→Feature) | 25 | N/W/M/S/VS | | [Source IDs] |
| Wave rationale for each wave | 20 | N/W/M/S/VS | | [Source IDs] |
| Feature selection table complete | 15 | N/W/M/S/VS | | [Source IDs] |
| 3 scope variants documented (OPTIONAL bonus) | 10 | N/W/M/S/VS | | [Source IDs] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- JTBD links: Traced to user research evidence
- Reasoning traces: Show decision chain from problem to feature
- Scope variants: OPTIONAL in v2.0 (use /speckit.concept-variants to generate)

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

### Transparency (if score < 80) — NEW
- [ ] Document 3 concept variants (MINIMAL, BALANCED, AMBITIOUS)
- [ ] Link each feature to JTBD (>80% coverage required)
- [ ] Add wave rationale for each wave (why grouped together)
- [ ] Create at least 3 reasoning traces (RT-001 format)
- [ ] Complete feature selection table with alternatives

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

# Concept Quality Score (CQS) — Evidence-Based (CQS-E)

> **Purpose**: Quantify concept readiness with evidence quality tracking before proceeding to specification.

## CQS-E Calculation

**Formula** (Updated v0.7.0 — 11 Components):
```
CQS-E = (
  Market × 0.16 +            # Market validation (↓ from 0.18)
  Persona × 0.12 +           # Persona depth (↓ from 0.14)
  Metrics × 0.12 +           # Metrics quality (↓ from 0.14)
  Features × 0.12 +          # Feature completeness (↓ from 0.14)
  Risk × 0.08 +              # Risk assessment (↓ from 0.10)
  Technical × 0.08 +         # Technical hints (↓ from 0.10)
  Strategic_Clarity × 0.08 + # Strategic positioning (↑ from 0.05)
  Strategic_Depth × 0.10 +   # NEW: Three Pillars, Differentiation, Recommendations
  Validation × 0.05 +        # Hypothesis test status
  Transparency × 0.05 +      # Decision transparency
  Quality_Intent × 0.04      # Quality targets from constitution (↓ from 0.05)
) × 100 × Evidence_Multiplier
```

**Change Log (v0.7.0)**:
- **Added**: Strategic Depth (10% weight) - Three Pillars, Differentiation Strategy, Strategic Recommendations
- **Rebalanced weights**: Market (18%→16%), Persona/Metrics/Features (14%→12%), Risk/Technical (10%→8%), Strategic_Clarity (5%→8%), Quality_Intent (5%→4%)
- **Rationale**: Strategic depth (why/how we'll win) now weighted equally with market/persona/metrics/features

**Previous Versions**:
- v0.6.1: 10 components, added Quality Intent (5%)
- v0.6.0: Renamed Strategic → Strategic Clarity

| Component | Score | Weight | Weighted | Evidence Quality | Notes |
|-----------|:-----:|:------:|:--------:|:----------------:|-------|
| Market Validation | /100 | 0.16 | | HIGH/MED/LOW | [Gaps to address] |
| Persona Depth | /100 | 0.12 | | HIGH/MED/LOW | [Gaps to address] |
| Metrics Quality | /100 | 0.12 | | HIGH/MED/LOW | [Gaps to address] |
| Feature Completeness | /100 | 0.12 | | HIGH/MED/LOW | [Gaps to address] |
| Risk Assessment | /100 | 0.08 | | HIGH/MED/LOW | [Gaps to address] |
| Technical Hints | /100 | 0.08 | | HIGH/MED/LOW | [Gaps to address] |
| **Strategic Clarity** | /100 | 0.08 | | HIGH/MED/LOW | [Positioning, GTM, strategy] |
| **Strategic Depth** | /100 | 0.10 | | HIGH/MED/LOW | [Three Pillars, Differentiation, Recommendations] |
| **Validation Rigor** | /100 | 0.05 | | HIGH/MED/LOW | [Hypothesis status] |
| **Transparency** | /100 | 0.05 | | HIGH/MED/LOW | [Decision rationale] |
| **Quality Intent** | /100 | 0.04 | | HIGH/MED/LOW | [Constitution quality targets] |
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

### Market Validation (16% weight)

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

### Persona Depth (12% weight)

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

### Metrics Quality (12% weight)

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

### Feature Completeness (12% weight)

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

### Risk Assessment (8% weight)

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

### Technical Hints (8% weight)

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

### Strategic Clarity (8% weight)

> **Updated v0.6.1**: Expanded to include strategic positioning from Q6-Q10 in `/speckit.concept`

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| Market positioning defined with rationale | 20 | N/W/M/S/VS | | [§ Strategic Positioning] |
| Differentiation strategy clear with evidence | 30 | N/W/M/S/VS | | [§ Strategic Positioning] |
| GTM strategy documented with tactics + metrics | 30 | N/W/M/S/VS | | [§ Strategic Positioning] |
| Timeline realistic with milestones | 10 | N/W/M/S/VS | | [§ Strategic Positioning] |
| Success metric (North Star) defined with Y1 target | 10 | N/W/M/S/VS | | [§ Strategic Positioning] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- **Market Positioning**: Documented in § Strategic Positioning with rationale from market research
- **Differentiation**: Competitive matrix showing advantage in chosen area
- **GTM Strategy**: Tactics with CAC targets, conversion rates, channel-specific metrics
- **Timeline**: Aligned with feature scope (aggressive timeline = reduced scope)
- **North Star Metric**: Definition + Y1 target + leading indicators

**Scoring Logic**:
```
Market Positioning (20 pts):
  IF positioning documented + rationale + implications: 20 pts
  ELIF positioning documented: 10 pts
  ELSE: 0 pts

Differentiation (30 pts):
  IF differentiation + competitive matrix + evidence: 30 pts
  ELIF differentiation + competitive matrix: 20 pts
  ELIF differentiation documented: 10 pts
  ELSE: 0 pts

GTM Strategy (30 pts):
  IF GTM + tactics + metrics (CAC, conversion): 30 pts
  ELIF GTM + tactics: 20 pts
  ELIF GTM documented: 10 pts
  ELSE: 0 pts

Timeline (10 pts):
  IF timeline + milestones + risks: 10 pts
  ELIF timeline documented: 5 pts
  ELSE: 0 pts

North Star Metric (10 pts):
  IF metric + definition + Y1 target + leading indicators: 10 pts
  ELIF metric + Y1 target: 5 pts
  ELSE: 0 pts
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

### Strategic Depth (10% weight) — NEW v0.7.0

> **Purpose**: Evaluate strategic foundation (why we'll win) through Three Foundational Pillars, Differentiation Strategy, and Phase-based Strategic Recommendations.

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| Three Foundational Pillars defined with proof points | 25 | N/W/M/S/VS | | [§ Three Foundational Pillars] |
| Five Breakthrough Differentiators with barriers to entry | 25 | N/W/M/S/VS | | [§ Differentiation Strategy] |
| Phase-based Strategic Recommendations (Foundation/Scale/Dominate) | 25 | N/W/M/S/VS | | [§ Strategic Recommendations] |
| Critical Success Factors documented (≥5 CSFs) | 15 | N/W/M/S/VS | | [§ Strategic Recommendations] |
| Risk/Mitigation matrix complete (≥5 risks) | 10 | N/W/M/S/VS | | [§ Strategic Recommendations] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- **Three Pillars**: Each pillar has ≥2 proof points with STRONG+ evidence tier, addresses ≥1 top-5 pain point from Problem Analysis
- **Differentiators**: Each differentiator has Market Reality (statistics), Our Approach (3-5 tactics), Proof Point (measurable claim), Time to Imitation estimate
- **Strategic Recommendations**: 3 phases with 3-5 actions each, Phase 1 targets aligned with 6-month milestones, success criteria quantified
- **Critical Success Factors**: 5-7 CSFs with "How to Ensure" specifics, linked to Three Pillars or Differentiation Strategy
- **Risk/Mitigation**: ≥5 risks with likelihood (H/M/L), impact (H/M/L), mitigation strategy, owner assigned

**Scoring Logic**:
```
Three Foundational Pillars (25 pts):
  IF 3 pillars + ≥2 proof points each (STRONG+) + pain point links: 25 pts
  ELIF 3 pillars + ≥1 proof point each: 20 pts
  ELIF 3 pillars defined: 15 pts
  ELIF 1-2 pillars defined: 10 pts
  ELSE: 0 pts

Breakthrough Differentiators (25 pts):
  IF 5 differentiators + proof points + time to imitation: 25 pts
  ELIF 5 differentiators + proof points: 20 pts
  ELIF 3-4 differentiators documented: 15 pts
  ELIF 1-2 differentiators documented: 10 pts
  ELSE: 0 pts

Strategic Recommendations (25 pts):
  IF 3 phases + 3-5 actions each + success criteria: 25 pts
  ELIF 3 phases + actions: 20 pts
  ELIF 2 phases documented: 15 pts
  ELIF 1 phase documented: 10 pts
  ELSE: 0 pts

Critical Success Factors (15 pts):
  IF ≥7 CSFs with "How to Ensure": 15 pts
  ELIF 5-6 CSFs with specifics: 12 pts
  ELIF 3-4 CSFs documented: 8 pts
  ELIF 1-2 CSFs documented: 4 pts
  ELSE: 0 pts

Risk/Mitigation Matrix (10 pts):
  IF ≥5 risks + likelihood/impact/mitigation/owner: 10 pts
  ELIF ≥5 risks + mitigation: 8 pts
  ELIF 3-4 risks documented: 5 pts
  ELIF 1-2 risks documented: 2 pts
  ELSE: 0 pts
```

**Integration with Concept**:
- § Three Foundational Pillars → feeds into Differentiation Strategy
- § Differentiation Strategy → expands on pillars with 5 specific differentiators
- § Strategic Recommendations → Phase 1 actions build pillar foundations
- § Problem Analysis → Pillars address top 5 pain points

---

### Quality Intent (4% weight) — v0.6.1

> **Purpose**: Evaluate quality standards set in `/memory/constitution.md` (Project Settings) from `/speckit.constitution` questionnaire.

| Criterion | Max Pts | Evidence Tier | Score | Sources |
|-----------|:-------:|:-------------:|:-----:|---------|
| Performance targets set with rationale | 30 | N/W/M/S/VS | | [constitution.md § Project Settings] |
| Reliability targets set with rationale | 30 | N/W/M/S/VS | | [constitution.md § Project Settings] |
| Accessibility targets set with rationale | 20 | N/W/M/S/VS | | [constitution.md § Project Settings] |
| Quality-first principles strengthened (≥3 MUST) | 20 | N/W/M/S/VS | | [constitution.md § Strengthened Principles] |
| **Subtotal** | 100 | | **/100** | |

**Evidence Requirements**:
- **Performance targets**: `perf_priority` documented AND (`response_time_p95_ms` set OR `perf_priority` = best-in-class)
- **Reliability targets**: `uptime_sla` documented AND (`uptime_sla` ≥ 99.9% OR `error_tolerance` documented)
- **Accessibility targets**: `accessibility_level` ≥ wcag21-a AND (`a11y_groups` non-empty if level ≥ AA)
- **Quality-first principles**: ≥3 principles strengthened to MUST (PERF-010, REL-010/011, A11Y-001..005)

**Scoring Logic**:
```
Performance Targets (30 pts):
  IF perf_priority = best-in-class AND response_time_p95_ms < 200: 30 pts
  ELIF perf_priority >= competitive AND response_time_p95_ms set: 25 pts
  ELIF perf_priority documented: 15 pts
  ELSE: 0 pts

Reliability Targets (30 pts):
  IF uptime_sla >= 99.99% AND error_tolerance = zero: 30 pts
  ELIF uptime_sla >= 99.9% OR error_tolerance documented: 25 pts
  ELIF uptime_sla documented: 15 pts
  ELSE: 0 pts

Accessibility Targets (20 pts):
  IF accessibility_level >= wcag22-aa AND a11y_groups.length >= 2: 20 pts
  ELIF accessibility_level >= wcag21-aa: 15 pts
  ELIF accessibility_level documented: 10 pts
  ELSE: 0 pts

Quality-First Principles (20 pts):
  IF ≥5 principles strengthened to MUST: 20 pts
  ELIF ≥3 principles strengthened to MUST: 15 pts
  ELIF ≥1 principle strengthened to MUST: 10 pts
  ELSE: 0 pts
```

**Integration with Concept**:
- If § Strategic Positioning → Differentiation = "Performance": Expect `perf_priority` = best-in-class
- If § Strategic Positioning → Differentiation = "Reliability": Expect `uptime_sla` ≥ 99.99%
- If § Strategic Positioning → GTM Strategy = "Sales-Led Growth": Expect `uptime_sla` ≥ 99.9% (enterprise)
- If § Strategic Positioning → Market Position = "Premium": Expect `accessibility_level` ≥ wcag22-aa

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

### Strategic Clarity (if score < 80) — v0.7.0
- [ ] Document market positioning (Premium/Value/Budget/Niche/Disruptive) with rationale
- [ ] Define differentiation strategy (Technology/UX/Price/Performance/Integration/Service)
- [ ] Complete GTM strategy with tactics, CAC targets, and conversion metrics
- [ ] Set realistic timeline with milestones (Alpha, Beta, Launch)
- [ ] Define North Star metric with Year 1 target and leading indicators

### Strategic Depth (if score < 80) — NEW v0.7.0
- [ ] Define Three Foundational Pillars (memorable 3-4 word names)
- [ ] Link each pillar to ≥1 pain point from top 5 (Problem Analysis)
- [ ] Provide ≥2 proof points per pillar with STRONG+ evidence tier
- [ ] Explain "Why We Win" and "Why Competitors Lose" for each pillar
- [ ] Estimate time to imitation for each pillar with justification
- [ ] Define 5 Breakthrough Differentiators (Market Reality, Our Approach, Proof Point)
- [ ] Document barriers to entry and defensibility for differentiators
- [ ] Create time to imitation matrix with moat types
- [ ] Create Phase-based Strategic Recommendations (Foundation/Scale/Dominate)
- [ ] Define 3-5 actions per phase with measurable targets
- [ ] Document 5-7 Critical Success Factors with "How to Ensure"
- [ ] Create Risk/Mitigation matrix with ≥5 risks (likelihood/impact/mitigation/owner)

### Validation (if score < 80)
- [ ] Document at least 3 hypotheses (HYP-001 format)
- [ ] Include at least 1 Desirability, 1 Feasibility, 1 Viability hypothesis
- [ ] Collect evidence for each hypothesis
- [ ] Document Pre-Mortem failure scenarios

### Transparency (if score < 80)
- [ ] Document 3 concept variants (MINIMAL, BALANCED, AMBITIOUS)
- [ ] Link each feature to JTBD (>80% coverage required)
- [ ] Add wave rationale for each wave (why grouped together)
- [ ] Create at least 3 reasoning traces (RT-001 format)
- [ ] Complete feature selection table with alternatives

### Quality Intent (if score < 80) — v0.6.1
- [ ] Run `/speckit.constitution` to set quality targets (if not done)
- [ ] Set performance priority (`perf_priority`) and response time budget
- [ ] Set reliability targets (`uptime_sla`, `error_tolerance`)
- [ ] Set accessibility level (`accessibility_level`, `a11y_groups`)
- [ ] Review § Strengthened Principles: Verify ≥3 principles are MUST
- [ ] Cross-check with § Differentiation Strategy:
  - [ ] If Differentiator emphasizes Performance → perf_priority = best-in-class
  - [ ] If Differentiator emphasizes Reliability → uptime_sla ≥ 99.99%
  - [ ] If GTM = Sales-Led Growth → uptime_sla ≥ 99.9%
  - [ ] If Positioning = Premium → accessibility_level ≥ wcag22-aa

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

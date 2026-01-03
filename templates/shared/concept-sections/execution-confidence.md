# Execution Confidence Matrix

> **Purpose**: Systematically assess confidence levels across critical execution domains, identifying areas requiring de-risking before major resource commitment and establishing clear go/no-go criteria.

## Confidence Overview

```
                    Technical   Market   Team   Financial
                    ─────────  ──────  ─────  ─────────
    GREEN (High)       ●                 ●
    YELLOW (Medium)              ●              ●
    RED (Low)
                    ─────────  ──────  ─────  ─────────
    Overall Confidence: YELLOW - Proceed with mitigations
```

| Confidence Level | Definition | Investment Implication |
|:----------------:|------------|------------------------|
| **GREEN** | High confidence (>80%) | Full speed ahead, standard oversight |
| **YELLOW** | Medium confidence (50-80%) | Proceed with specific mitigations |
| **RED** | Low confidence (<50%) | Pause, de-risk before major commitment |

---

## Domain Confidence Assessment

### Technical Confidence

| Factor | Confidence | Evidence | Gap/Risk |
|--------|:----------:|----------|----------|
| Core technology feasibility | [R/Y/G] | [Prototype/POC/Production proven] | [Gap description] |
| Architecture scalability | [R/Y/G] | [Load tests/projections/assumptions] | [Gap description] |
| Integration complexity | [R/Y/G] | [API docs/experience/unknown] | [Gap description] |
| Security requirements | [R/Y/G] | [Audit/review/not assessed] | [Gap description] |
| Performance targets | [R/Y/G] | [Benchmarks/estimates/TBD] | [Gap description] |
| Data architecture | [R/Y/G] | [Schema/model/undefined] | [Gap description] |
| **Technical Overall** | **[R/Y/G]** | — | — |

**Technical Confidence Scoring Criteria:**
- **GREEN**: Proven in production at scale, team has deep expertise, <10% unknown unknowns
- **YELLOW**: Prototyped successfully, team has adjacent expertise, 10-30% unknowns
- **RED**: Unproven technology, new domain for team, >30% unknowns

### Market Confidence

| Factor | Confidence | Evidence | Gap/Risk |
|--------|:----------:|----------|----------|
| Problem validation | [R/Y/G] | [[X] customer interviews / surveys] | [Gap description] |
| Solution desirability | [R/Y/G] | [Prototype tests / concept tests] | [Gap description] |
| Willingness to pay | [R/Y/G] | [Pre-sales / pricing tests / assumption] | [Gap description] |
| Market timing | [R/Y/G] | [Trend data / expert input / gut] | [Gap description] |
| Competitive dynamics | [R/Y/G] | [Win-loss analysis / research / limited] | [Gap description] |
| Go-to-market path | [R/Y/G] | [Proven channel / new channel / TBD] | [Gap description] |
| **Market Overall** | **[R/Y/G]** | — | — |

**Market Confidence Scoring Criteria:**
- **GREEN**: >20 validated customer interviews, proven WTP, clear GTM, <2 major competitors
- **YELLOW**: 5-20 interviews, indicated WTP, GTM hypothesis, known competition
- **RED**: <5 interviews, assumed WTP, unclear GTM, crowded market

### Team Confidence

| Factor | Confidence | Evidence | Gap/Risk |
|--------|:----------:|----------|----------|
| Domain expertise | [R/Y/G] | [Years experience / hires needed] | [Gap description] |
| Technical skills match | [R/Y/G] | [Skill matrix / training needs] | [Gap description] |
| Capacity availability | [R/Y/G] | [Committed resources / competing priorities] | [Gap description] |
| Leadership alignment | [R/Y/G] | [Sponsor commitment / political support] | [Gap description] |
| Cross-functional collaboration | [R/Y/G] | [History / new relationships] | [Gap description] |
| Execution track record | [R/Y/G] | [Similar projects delivered / first attempt] | [Gap description] |
| **Team Overall** | **[R/Y/G]** | — | — |

**Team Confidence Scoring Criteria:**
- **GREEN**: Proven team with domain expertise, fully staffed, strong sponsorship
- **YELLOW**: Capable team learning new domain, 70%+ staffed, adequate sponsorship
- **RED**: Significant skill gaps, <70% staffed, weak/unclear sponsorship

### Financial Confidence

| Factor | Confidence | Evidence | Gap/Risk |
|--------|:----------:|----------|----------|
| Cost estimation accuracy | [R/Y/G] | [Bottom-up / analogous / rough guess] | [Gap description] |
| Revenue projections | [R/Y/G] | [Market-validated / modeled / assumed] | [Gap description] |
| Unit economics viability | [R/Y/G] | [Proven / calculated / theoretical] | [Gap description] |
| Funding availability | [R/Y/G] | [Committed / allocated / requested] | [Gap description] |
| Payback timeline | [R/Y/G] | [Calculated / estimated / unknown] | [Gap description] |
| Sensitivity to assumptions | [R/Y/G] | [Stress-tested / single scenario / fragile] | [Gap description] |
| **Financial Overall** | **[R/Y/G]** | — | — |

**Financial Confidence Scoring Criteria:**
- **GREEN**: Bottom-up estimates, validated assumptions, committed funding, <2yr payback
- **YELLOW**: Analogous estimates, modeled assumptions, allocated funding, 2-3yr payback
- **RED**: Rough estimates, untested assumptions, unfunded, >3yr or unknown payback

---

## External Dependency Confidence

| Dependency | Owner | Confidence | Mitigation if Fails |
|------------|-------|:----------:|---------------------|
| [Partner/Vendor X] | [External] | [R/Y/G] | [Alternative / impact] |
| [Regulatory approval Y] | [Government] | [R/Y/G] | [Timeline / workaround] |
| [Platform/API Z] | [Third party] | [R/Y/G] | [Abstraction / alternative] |
| [Key hire] | [Recruiting] | [R/Y/G] | [Consultant / delay] |
| [Customer commitment] | [Prospect] | [R/Y/G] | [Other customers / pivot] |

---

## Confidence Improvement Actions

*Prioritized actions to move RED/YELLOW to YELLOW/GREEN*

| Domain | Current | Target | Action | Owner | Timeline | Cost |
|--------|:-------:|:------:|--------|-------|:--------:|:----:|
| [Technical] | [R] | [Y] | [Spike/POC on technology X] | [Name] | [X] weeks | $[X]K |
| [Market] | [Y] | [G] | [10 more customer interviews] | [Name] | [X] weeks | $[X]K |
| [Team] | [R] | [Y] | [Hire senior engineer] | [Name] | [X] weeks | $[X]K |
| [Financial] | [Y] | [G] | [Pricing experiment] | [Name] | [X] weeks | $[X]K |
| [External] | [R] | [Y] | [Secure backup vendor] | [Name] | [X] weeks | $[X]K |

---

## Composite Confidence Score

| Domain | Weight | Score | Weighted |
|--------|:------:|:-----:|:--------:|
| Technical | [X]% | [1-3] | [X] |
| Market | [X]% | [1-3] | [X] |
| Team | [X]% | [1-3] | [X] |
| Financial | [X]% | [1-3] | [X] |
| External Dependencies | [X]% | [1-3] | [X] |
| **Composite Score** | 100% | — | **[X]/3** |

*Scoring: GREEN=3, YELLOW=2, RED=1*

---

## Project Greenlight Criteria (Google-Style)

### Go/No-Go Assessment

| Criterion | Threshold | Current | Status |
|-----------|:---------:|:-------:|:------:|
| No RED in any domain | 0 RED | [X] RED | [ ] Pass [ ] Fail |
| Composite score | ≥2.0 | [X] | [ ] Pass [ ] Fail |
| Technical + Market both GREEN or YELLOW | Both ≥YELLOW | [Tech/Market status] | [ ] Pass [ ] Fail |
| Funding committed | 100% Phase 1 | [X]% | [ ] Pass [ ] Fail |
| Executive sponsor confirmed | Named sponsor | [Name/None] | [ ] Pass [ ] Fail |
| De-risk plan for all YELLOW/RED | Plan complete | [Yes/No] | [ ] Pass [ ] Fail |

### Greenlight Decision

| Decision | Criteria Met | Recommended Action |
|----------|:------------:|-------------------|
| **FULL GREENLIGHT** | All criteria pass | Proceed with full resources |
| **CONDITIONAL GREENLIGHT** | Minor gaps | Proceed, complete mitigations in parallel |
| **STAGED GREENLIGHT** | Significant gaps | Phase 1 only, re-assess at gate |
| **NO-GO** | Critical failures | Do not proceed until resolved |

**Current Status**: [ ] FULL [ ] CONDITIONAL [ ] STAGED [ ] NO-GO

**Rationale**: [Why this decision, key factors]

---

## Confidence Review Cadence

| Review Type | Frequency | Participants | Focus |
|-------------|:---------:|--------------|-------|
| Domain check-in | Weekly | Domain leads | Track improvement actions |
| Confidence update | Bi-weekly | Core team | Update matrix, adjust actions |
| Greenlight review | Monthly | Steering committee | Go/No-Go re-assessment |
| Deep dive | On trigger | Full team | RED domain deep analysis |

---

## Execution Confidence Quality Checklist

- [ ] All four domains (Technical, Market, Team, Financial) assessed
- [ ] Each domain has specific factors with evidence cited
- [ ] RED ratings have explicit de-risk actions with owners and timelines
- [ ] External dependencies identified and assessed
- [ ] Composite score calculated with appropriate weights
- [ ] Greenlight criteria defined and evaluated
- [ ] Confidence improvement actions are prioritized and resourced
- [ ] Review cadence established

---

## Integration Notes

- **Feeds into**: Risk matrix (confidence gaps = risks), Strategic options (confidence affects option value)
- **Depends on**: Market framework (market confidence inputs), Team assessment (team confidence inputs)
- **CQS Impact**: Improves Risk (+5 pts) and Feasibility (+3 pts) scores through systematic confidence assessment

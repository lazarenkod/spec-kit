# Hypothesis Testing Log (OpenAI-Style)

> **Purpose**: Track assumptions systematically with evidence to validate desirability, feasibility, and viability before committing resources.

## Hypothesis Testing Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    EVIDENCE-BASED VALIDATION                     │
│                                                                  │
│  Assumption → Hypothesis → Test → Evidence → Decision           │
│                                                                  │
│  "We don't guess. We test, measure, and decide with data."      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hypothesis Entry Template

### HYP-001: [Hypothesis Title]

**Type**: `DESIRABILITY` | `FEASIBILITY` | `VIABILITY`

**Statement**:
> We believe that [specific user segment] will [specific behavior/action] because [rationale/insight].

**Assumption Being Tested**:
[What underlying assumption does this validate?]

**Test Method(s)**:
- [ ] User interviews (target: n=10+)
- [ ] Landing page / signup conversion (target: >X%)
- [ ] Prototype / usability testing
- [ ] Survey / quantitative research
- [ ] Market data / secondary research
- [ ] Technical spike / proof of concept
- [ ] Other: [specify]

**Success Criteria**:

| Metric | Target | Minimum Viable |
|--------|:------:|:--------------:|
| Quantitative | [e.g., >40% express intent to pay] | [e.g., >25%] |
| Qualitative | [e.g., 8/10 describe problem as "critical"] | [e.g., 6/10] |

**Evidence Collected**:

| Date | Method | Sample Size | Result | Confidence |
|:----:|--------|:-----------:|--------|:----------:|
| MM/DD | Interview | n=12 | 9/12 validated | `HIGH` |
| MM/DD | Survey | n=45 | 62% agree | `MEDIUM` |
| MM/DD | Landing page | 500 visitors | 4.2% conversion | `HIGH` |

**Status**: ✅ `Validated` | ⚠️ `Partially Validated` | ❌ `Invalidated` | 🔄 `Testing`

**Implications**:
- If validated: [What we do next]
- If invalidated: [How we pivot or what changes]

---

## Hypothesis Types Explained

| Type | Question Answered | Example Hypothesis |
|------|-------------------|-------------------|
| **Desirability** | Do users want this? | "Engineers will pay for AI code review because manual reviews slow them down" |
| **Feasibility** | Can we build this? | "We can achieve <100ms latency with our architecture" |
| **Viability** | Is this a good business? | "CAC will be <$50 via content marketing" |

---

## Hypothesis Tracking Summary

| ID | Type | Hypothesis (Short) | Status | Confidence | Evidence Count |
|:--:|:----:|-------------------|:------:|:----------:|:--------------:|
| HYP-001 | Desirability | [Summary] | ✅ | HIGH | 3 |
| HYP-002 | Viability | [Summary] | 🔄 | — | 1 |
| HYP-003 | Feasibility | [Summary] | ⚠️ | MEDIUM | 2 |

---

## Validation Prioritization Matrix

Prioritize hypothesis testing based on risk and effort:

```
                    HIGH RISK
                        │
     ┌──────────────────┼──────────────────┐
     │   TEST FIRST     │   TEST SECOND    │
     │   (Critical)     │   (Important)    │
     │                  │                  │
LOW ─┼──────────────────┼──────────────────┼─ HIGH
EFFORT                  │                  │   EFFORT
     │   TEST THIRD     │   TEST IF TIME   │
     │   (Quick wins)   │   (Nice to have) │
     │                  │                  │
     └──────────────────┼──────────────────┘
                        │
                    LOW RISK
```

---

## Evidence Quality Guidelines

| Confidence Level | Criteria |
|:----------------:|----------|
| `HIGH` | Primary research, n>30, statistically significant, recent data |
| `MEDIUM` | Primary research n<30, or credible secondary sources |
| `LOW` | Anecdotal, outdated, or single data point |
| `NONE` | Assumption without evidence |

---

## Hypothesis Testing Quality Checklist

- [ ] At least 1 hypothesis per type (Desirability, Feasibility, Viability)
- [ ] Riskiest assumptions identified and prioritized for testing
- [ ] Success criteria are specific and measurable
- [ ] Evidence collected with confidence levels assigned
- [ ] Status updated based on evidence (not opinions)
- [ ] Implications documented for both validation and invalidation
- [ ] Invalidated hypotheses have clear pivot actions

---

## Integration Notes

- **Feeds into**: Risk Assessment (validated vs unvalidated assumptions), Decision Log (evidence-based decisions)
- **Depends on**: Persona-JTBD (desirability hypotheses), Business Model Canvas (viability hypotheses), Technical Hints (feasibility hypotheses)
- **Connected to**: Pre-Mortem (failure scenarios become hypotheses), CQS Score (Validation dimension)
- **CQS Impact**: Improves Validation (+5 pts) through systematic evidence tracking

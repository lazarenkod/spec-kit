# Pre-Mortem Analysis

> **Purpose**: Imagine failure before it happens to identify preventable scenarios and establish early warning systems.

## Pre-Mortem Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRE-MORTEM EXERCISE                          │
│                                                                  │
│  "It's 12 months from now. This product has failed.            │
│   What went wrong?"                                              │
│                                                                  │
│  Imagine failure → Identify causes → Prevent proactively        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Failure Scenario Template

### FAIL-001: [Failure Mode Name]

**Probability**: `HIGH` | `MEDIUM` | `LOW`
**Impact**: `CRITICAL` | `MAJOR` | `MINOR`
**Risk Score**: [Probability × Impact]

#### Failure Story
[Narrative description of how this failure unfolds. Be specific and vivid. Include the sequence of events that leads to failure.]

#### Root Causes
1. [Primary cause]
2. [Contributing factor]
3. [Enabler that allowed it to happen]

#### Early Warning Signs
- [ ] [Metric dropping below X threshold]
- [ ] [User feedback pattern to watch for]
- [ ] [Competitive move indicator]
- [ ] [Team/operational signal]

#### Prevention Strategy
| Action | Owner | Timeline | Status |
|--------|:-----:|:--------:|:------:|
| [Preventive measure 1] | [Name] | [When] | `Not Started` |
| [Preventive measure 2] | [Name] | [When] | `Not Started` |

#### Contingency Plan
If early warning signs appear:
1. [Immediate response action]
2. [Escalation path]
3. [Fallback option]

#### Kill Criteria
```
IF [specific metric] < [threshold] BY [date], THEN [pivot/kill/major change]
```

---

## Most Likely Failure Scenarios

Document at least 3 failure scenarios in priority order:

| ID | Failure Mode | Probability | Impact | Risk Score | Status |
|:--:|--------------|:-----------:|:------:|:----------:|:------:|
| FAIL-001 | [e.g., Market timing wrong] | HIGH | CRITICAL | 9 | `Monitoring` |
| FAIL-002 | [e.g., Key hire doesn't work out] | MEDIUM | MAJOR | 6 | `Mitigating` |
| FAIL-003 | [e.g., Technical debt blocks scale] | LOW | MAJOR | 3 | `Accepted` |

---

## Failure Categories

Ensure coverage across these failure types:

| Category | Example Failures | Covered? |
|----------|------------------|:--------:|
| **Market** | Wrong timing, no PMF, competitor wins | [ ] |
| **Product** | Wrong features, poor UX, complexity | [ ] |
| **Technical** | Can't scale, security breach, tech debt | [ ] |
| **Team** | Key person leaves, hiring fails, burnout | [ ] |
| **Financial** | Runway runs out, CAC too high, churn | [ ] |
| **External** | Regulation, economic downturn, dependency fails | [ ] |

---

## Failure Prevention Checklist

### Weekly Review
- [ ] Check all early warning metrics against thresholds
- [ ] Review customer feedback for failure pattern signals
- [ ] Assess team health and capacity

### Monthly Checkpoint
- [ ] Hypothesis validation progress against plan
- [ ] Prevention strategy execution status
- [ ] Update probability/impact based on new information

### Quarterly Strategic Review
- [ ] Full pre-mortem scenario reassessment
- [ ] New failure modes to add?
- [ ] Scenarios to retire (no longer relevant)?
- [ ] Kill criteria evaluation

---

## Pre-Mortem Quality Checklist

- [ ] At least 3 failure scenarios documented
- [ ] All 6 failure categories considered
- [ ] Each scenario has specific early warning signs (not generic)
- [ ] Prevention strategies have owners and timelines
- [ ] Kill criteria are specific and measurable
- [ ] Weekly/monthly/quarterly review cadence established

---

## Integration Notes

- **Feeds into**: Risk Assessment Matrix (failure scenarios → risks), Hypothesis Testing (assumptions to validate)
- **Depends on**: Business Model Canvas (financial failure modes), Technical Hints (technical failure modes)
- **Connected to**: Decision Log (pivot decisions), Scope Exclusions (kill criteria outcomes)
- **CQS Impact**: Improves Risk (+3 pts) through proactive failure identification

# Decision Log (Stripe-Style)

> **Purpose**: Document key decisions with rationale to enable rapid pivots, support post-mortems, and preserve institutional knowledge.

## Decision Log Overview

Track all significant decisions made during concept development:

```
┌──────────────────────────────────────────────────────────────────┐
│                     DECISION LIFECYCLE                          │
│                                                                  │
│  Proposed → Under Review → Decided → [Implemented] → [Revisited]│
│                                                                  │
│  Each stage documented with rationale and evidence              │
└──────────────────────────────────────────────────────────────────┘
```

---

## Decision Entry Template

### DEC-001: [Decision Title]

**Date**: YYYY-MM-DD
**Status**: `Proposed` | `Under Review` | `Decided` | `Revisit by [date]`
**Owner**: [Decision maker name/role]

#### Context
[What situation prompted this decision? What problem are we solving?]

#### Options Considered

| Option | Description | Pros | Cons | Effort |
|:------:|-------------|------|------|:------:|
| **A** | [Option A description] | [Benefits] | [Drawbacks] | [S/M/L/XL] |
| **B** | [Option B description] | [Benefits] | [Drawbacks] | [S/M/L/XL] |
| **C** | Do nothing | Zero investment | [Opportunity cost, risk] | — |

#### Decision
**Chosen**: [Option X]

#### Rationale
[Detailed reasoning for the choice. Include:
- Data or evidence that informed the decision
- Alignment with strategic goals
- Why alternatives were rejected]

#### Consequences
- **What we gain**: [Expected positive outcomes]
- **What we give up**: [Trade-offs accepted]
- **Dependencies created**: [New constraints or requirements]

#### Reversibility
| Aspect | Assessment |
|--------|:----------:|
| Technical reversibility | Easy / Medium / Hard |
| Cost to reverse | Low / Medium / High |
| Time to reverse | Days / Weeks / Months |

**Overall**: [Type 1 (irreversible) / Type 2 (reversible)]

#### Review Trigger
Revisit this decision if:
- [ ] [Specific metric crosses threshold]
- [ ] [Market condition changes]
- [ ] [New information emerges]
- [ ] By [specific date] regardless

---

## Decision Log Table (Summary View)

| ID | Decision | Date | Status | Reversibility | Owner |
|:--:|----------|:----:|:------:|:-------------:|:-----:|
| DEC-001 | [Title] | YYYY-MM-DD | Decided | Type 2 | [Name] |
| DEC-002 | [Title] | YYYY-MM-DD | Under Review | Type 1 | [Name] |
| DEC-003 | [Title] | YYYY-MM-DD | Proposed | Type 2 | [Name] |

---

## Decision Categories

| Category | Examples | Typical Reversibility |
|----------|----------|:---------------------:|
| **Architecture** | Tech stack, data model, infrastructure | Type 1 (Hard) |
| **Product** | Feature scope, pricing, positioning | Type 2 (Medium) |
| **Go-to-Market** | Target segment, channel, messaging | Type 2 (Easy) |
| **Resource** | Headcount, budget allocation, timeline | Type 2 (Medium) |
| **Partnership** | Vendor selection, integrations | Type 1-2 (Varies) |

---

## Decision-Making Principles

1. **Document before deciding**: Write down options before discussing
2. **Explicit > implicit**: Unstated decisions are still decisions
3. **Owner accountable**: Every decision has one owner (not a committee)
4. **Reversible = fast**: Type 2 decisions should be made quickly
5. **Evidence-based**: Cite data, not opinions, where possible

---

## Decision Quality Checklist

- [ ] Context clearly explains the problem/opportunity
- [ ] At least 3 options considered (including "do nothing")
- [ ] Pros/cons documented for each option
- [ ] Rationale explains why chosen option is best
- [ ] Reversibility assessed realistically
- [ ] Review triggers defined for non-trivial decisions
- [ ] Owner assigned and accountable

---

## Integration Notes

- **Feeds into**: Risk Matrix (decisions create risks), Technical Discovery (architecture decisions)
- **Depends on**: Constitution (principles guide decisions), PR/FAQ (strategic context)
- **CQS Impact**: Improves Risk (+2 pts) through decision traceability

# Trade-off Resolution Framework

> **Purpose**: Establish a consistent hierarchy for resolving competing priorities, enabling faster decisions and alignment across stakeholders.

## Trade-off Hierarchy

When values or priorities conflict, resolve in this order:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRIORITY HIERARCHY                        │
│                                                              │
│  1. SAFETY & SECURITY        ─────────────────── ABSOLUTE   │
│     Never compromise user data or security                   │
│                                                              │
│  2. USER VALUE               ─────────────────── PRIMARY    │
│     Optimize for user outcomes over internal convenience     │
│                                                              │
│  3. SIMPLICITY               ─────────────────── CORE       │
│     Remove before adding; justify every complexity           │
│                                                              │
│  4. SPEED                    ─────────────────── TACTICAL   │
│     Ship MVP, iterate with data; perfect is enemy of good   │
│                                                              │
│  5. REVERSIBLE > ANALYSIS    ─────────────────── DEFAULT    │
│     For reversible choices, decide fast and learn            │
└─────────────────────────────────────────────────────────────┘
```

---

## Trade-off Hierarchy Details

### 1. Safety & Security (Absolute Priority)
**Never compromise, even for speed or features**

| Principle | Application |
|-----------|-------------|
| Data protection | Never expose user data, even in logs |
| Security vulnerabilities | Never ship known vulnerabilities |
| Compliance | Never bypass regulatory requirements |
| User consent | Never collect without explicit consent |

**Example**: "We'll delay launch by 2 weeks to fix the auth vulnerability, even though investors expect us to ship Friday."

---

### 2. User Value > Internal Convenience
**Optimize for user outcomes over our development speed**

| Principle | Application |
|-----------|-------------|
| User experience | Accept tech debt if it delivers user value faster |
| Performance | Invest in perceived speed even if backend is more complex |
| Reliability | Over-engineer reliability; under-engineer features |

**Example**: "We'll add a loading skeleton even though it's extra work, because users perceive it as faster."

---

### 3. Simplicity > Features
**Remove before adding; every feature must justify its complexity**

| Principle | Application |
|-----------|-------------|
| Feature count | Fewer, better features over feature parity |
| UI complexity | Hide advanced options; surface common paths |
| Codebase | Delete code aggressively; fight entropy |

**Example**: "We'll ship with 3 report types instead of 12, focusing on the ones 80% of users need."

---

### 4. Speed > Perfection
**Ship MVP, iterate based on data; perfect is the enemy of good**

| Principle | Application |
|-----------|-------------|
| MVP scope | Launch with minimum viable, not minimum marketable |
| Polish | 80% polish now beats 100% polish in 3 months |
| Documentation | Inline comments over comprehensive docs |

**Example**: "We'll launch with manual onboarding and automate it after we understand the patterns."

---

### 5. Reversible Decisions > Extensive Analysis
**For reversible choices, decide quickly and learn from outcomes**

| Decision Type | Approach |
|---------------|----------|
| **Type 1** (irreversible) | Deep analysis, stakeholder review, document thoroughly |
| **Type 2** (reversible) | Decide in <24 hours, learn from outcome, adjust |

**Example**: "Button color is Type 2—let's A/B test rather than debate for 3 meetings."

---

## This Concept's Key Trade-offs

Document specific trade-offs made in this concept:

| Trade-off | Options | Our Choice | Rationale | Impact |
|-----------|---------|:----------:|-----------|--------|
| Speed vs Quality | [Fast MVP / Polished v1] | [Choice] | [Why] | [Consequence] |
| Features vs Simplicity | [Full parity / Core only] | [Choice] | [Why] | [Consequence] |
| Build vs Buy | [Custom / Third-party] | [Choice] | [Why] | [Consequence] |
| Generalist vs Specialist | [Broad appeal / Niche focus] | [Choice] | [Why] | [Consequence] |

---

## Constitution Principle Conflicts

When Constitution principles conflict, document resolution:

| Conflict | Principle A | Principle B | Resolution | Rationale |
|----------|-------------|-------------|:----------:|-----------|
| [Conflict name] | [Principle ID] | [Principle ID] | A / B / Hybrid | [How resolved] |

**Reference**: Link to Constitution document for principle definitions.

---

## Trade-off Quality Checklist

- [ ] Trade-off hierarchy understood by all stakeholders
- [ ] Key trade-offs for this concept documented with rationale
- [ ] Constitution principle conflicts explicitly resolved
- [ ] No "have it all" thinking—real trade-offs acknowledged
- [ ] Reversibility assessed for each major trade-off

---

## Integration Notes

- **Feeds into**: Decision Log (documents trade-off choices), Scope Exclusions (what we sacrifice)
- **Depends on**: Constitution (principle definitions), PR/FAQ (strategic positioning)
- **CQS Impact**: Improves Risk (+2 pts) and Features (+1 pt) through strategic clarity

# Scope Exclusions ("What We're NOT Building")

> **Purpose**: Explicitly define what is out of scope to prevent scope creep, align stakeholders, and focus resources on what matters most.

## Why Document Non-Goals?

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCOPE BOUNDARY VALUE                          │
│                                                                  │
│  "A feature not in scope is as important as a feature in scope" │
│                                                                  │
│  • Prevents scope creep during development                       │
│  • Aligns stakeholder expectations early                         │
│  • Enables confident "no" to feature requests                    │
│  • Documents strategic intent, not just capability               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Explicit Non-Goals

### Features We Are NOT Building (v1.0)

| Feature/Capability | Why Excluded | Alternative for Users | Revisit When |
|-------------------|--------------|----------------------|--------------|
| [Feature X] | [Strategic reason] | [Workaround or competitor] | [Trigger condition] |
| [Integration Y] | [Resource reason] | [Manual process] | [User demand threshold] |
| [Market segment Z] | [Focus reason] | [Refer to partner] | [Scale milestone] |

### Segments We Are NOT Serving

| Segment | Why Excluded | Risk if We Try | Revisit When |
|---------|--------------|----------------|--------------|
| [Enterprise >10K employees] | [Complexity, sales cycle] | [Dilute product, slow iteration] | [After $XM ARR] |
| [Consumers] | [Different JTBD, CAC] | [Brand confusion] | [Never / Adjacent product] |

### Platforms We Are NOT Supporting (v1.0)

| Platform | Why Excluded | Impact | Revisit When |
|----------|--------------|--------|--------------|
| [Mobile native] | [Web-first strategy] | [~20% of market] | [After web PMF] |
| [Self-hosted] | [Support complexity] | [Enterprise subset] | [Enterprise tier] |

---

## Scope Guardrails

Before adding ANY feature to scope, it must pass ALL of these gates:

```markdown
## Scope Addition Checklist

The default answer to "should we add X?" is NO unless:

- [ ] **JTBD Alignment**: Directly supports primary Jobs-to-be-Done
- [ ] **User Evidence**: >30% of target users explicitly need it (evidence required)
- [ ] **Effort Justified**: Can be built in <[X] weeks with current team
- [ ] **Simplicity Preserved**: Doesn't compromise core product simplicity
- [ ] **Strategic Fit**: Aligns with Blue Ocean positioning (not feature parity)

If ANY checkbox is unchecked, the feature goes to:
- **Idea Backlog** (potential future)
- **Scope Exclusions** (strategic no)
```

---

## Rejected Alternatives

Document features/approaches that were considered and explicitly rejected:

| Alternative | Why Considered | Why Rejected | Owner | Reconsider If |
|-------------|----------------|--------------|:-----:|---------------|
| [Feature A] | [User request / competitive parity] | [Complexity, not core JTBD] | [Name] | [Condition] |
| [Approach B] | [Technical elegance] | [Over-engineering, YAGNI] | [Name] | [Scale trigger] |
| [Integration C] | [Partnership opportunity] | [Dependency risk, distraction] | [Name] | [Partner terms change] |

---

## Horizon Mapping for Exclusions

Connect scope exclusions to Three Horizons framework:

| Exclusion | Horizon | Status | Rationale |
|-----------|:-------:|:------:|-----------|
| [Feature X] | H2 | Deferred | Will build when [condition] |
| [Feature Y] | H3 | Exploring | May build if [hypothesis validates] |
| [Feature Z] | Never | Excluded | Against strategy, won't reconsider |

**Legend**:
- **Deferred (H2/H3)**: Not now, but on strategic radar
- **Excluded (Never)**: Strategic decision to NOT build, even long-term

---

## Stakeholder Communication

### How to Say "No" to Feature Requests

| Request Type | Response Template |
|--------------|-------------------|
| **From customers** | "We've documented this in our non-goals because [reason]. We recommend [alternative]. We'll revisit if [condition]." |
| **From executives** | "This is in Scope Exclusions (see concept doc). Adding it would [trade-off]. Do you want to override? If yes, what do we deprioritize?" |
| **From team** | "Great idea! Let's add it to Idea Backlog and evaluate against Scope Guardrails." |

---

## Scope Exclusion Quality Checklist

- [ ] At least 5 explicit non-goals documented
- [ ] Each exclusion has a "why" rationale (not just "later")
- [ ] Alternatives provided for users who need excluded features
- [ ] Revisit triggers defined (not open-ended "maybe someday")
- [ ] Scope Guardrails defined with specific thresholds
- [ ] Rejected alternatives documented with reconsider conditions
- [ ] Exclusions mapped to Three Horizons (deferred vs never)

---

## Integration Notes

- **Feeds into**: Feature Hierarchy (what's IN scope), Ideas Backlog (deferred items)
- **Depends on**: Three Horizons (horizon mapping), Trade-off Resolution (why we sacrifice)
- **Connected to**: PR/FAQ Internal FAQ ("What are we NOT building?")
- **CQS Impact**: Improves Features (+2 pts) and Risk (+1 pt) through scope clarity

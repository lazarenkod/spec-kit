# Feature Selection Rationale

> **Purpose**: Document WHY each feature was included or excluded, with JTBD traceability, alternatives considered, and evidence supporting the decision. Eliminates "black box" feature selection.

## Integration Notes

- **Depends on**: persona-jtbd.md (JTBD IDs), concept-variants.md (variant assignment), market-framework.md (competitive evidence)
- **Feeds into**: Feature Hierarchy (JTBD links), spec.md (requirement traceability)
- **CQS Impact**: Transparency component — Per-feature JTBD links criterion (25 points)

---

## Feature Selection Framework

### Selection Criteria Weights

Each feature is evaluated against 5 criteria:

| Criterion | Weight | Description | Evidence Sources |
|-----------|:------:|-------------|------------------|
| **JTBD Alignment** | 30% | Does it directly enable a documented JTBD? | Persona JTBD table |
| **Persona Fit** | 20% | Does primary persona need this? | User interviews, surveys |
| **Differentiation** | 20% | Does it create competitive advantage? | Blue Ocean, competitive analysis |
| **Feasibility** | 15% | Can we build it with current resources? | Technical hints, team skills |
| **Reversibility** | 15% | Can we change approach later if wrong? | Architecture assessment |

### Selection Decision Outcomes

| Decision | Meaning | Documentation Required |
|----------|---------|------------------------|
| **INCLUDE** | Feature selected for concept | JTBD link, alternatives, evidence |
| **EXCLUDE** | Deliberately not building | Why excluded, alternative for users |
| **DEFER** | Not in this version | When to reconsider, prerequisite |

---

## Template: Feature Selection Rationale Section

```markdown
## Feature Selection Rationale

<!--
  PURPOSE: Transparent decision log for all feature inclusion/exclusion decisions.
  This section answers: "Why did you choose THESE features specifically?"

  RULE: Every feature in Feature Hierarchy MUST have a corresponding SEL-XXX entry.
  RULE: Every JTBD in persona-jtbd.md MUST have at least one feature addressing it.
-->

### Selection Criteria Applied

| Criterion | Weight | How We Applied It |
|-----------|:------:|-------------------|
| JTBD Alignment | 30% | Feature must link to JTBD-xxx from Persona section |
| Persona Fit | 20% | Primary persona ([Name]) must need this capability |
| Differentiation | 20% | Scored against Blue Ocean ERRC grid |
| Feasibility | 15% | T-shirt size must be achievable within variant timeline |
| Reversibility | 15% | Type 2 decisions preferred for MVP |

---

### Selection Decision Table

| ID | Feature | Decision | Variant | JTBD | Alternatives | Why This Choice |
|:--:|---------|:--------:|:-------:|------|--------------|-----------------|
| SEL-001 | User Registration | INCLUDE | ALL | JTBD-FUNC-001 | OAuth-only, Magic link | B2B segment expects email/password |
| SEL-002 | Social Login | INCLUDE | BALANCED+ | JTBD-FUNC-002 | SAML SSO, Passwordless | Reduces friction; SSO deferred to H2 |
| SEL-003 | AI Suggestions | EXCLUDE | — | JTBD-EMOT-002 | Rule-based, Manual | Technical risk too high for MVP |
| SEL-004 | Mobile App | DEFER | H2 | JTBD-SOC-001 | PWA, Responsive | Web-first; mobile after PMF |

---

### Detailed Feature Rationale

#### SEL-001: User Registration

**Feature**: EPIC-001.F01 User Registration
**Decision**: INCLUDE in ALL variants

**JTBD Connection**:
```text
When I [start using the product for the first time],
I want to [create a personal account with my credentials],
So I can [save my work and access it from anywhere].

JTBD ID: JTBD-FUNC-001
Persona: [Primary Persona Name]
Job Type: Functional (Primary)
```

**Persona Pain Point Addressed**:
> "[Quote from user research about current pain with registration/access]"
> — [Persona Name], User Interview #[N]

**Alternatives Analyzed**:

| Alternative | Score | Pros | Cons | Why Not Chosen |
|-------------|:-----:|------|------|----------------|
| Email/Password | 8.5 | Familiar to users, works offline, enterprise-friendly | Friction, password fatigue | **SELECTED** |
| OAuth-only (Google/GitHub) | 7.0 | Low friction, no password | Not all users have accounts; enterprise blocks | B2B segment often blocks OAuth |
| Magic Link (email) | 7.5 | Passwordless, modern | Email deliverability risk, slower | **DEFERRED** to Wave 2 enhancement |
| Anonymous + later account | 6.0 | Fastest onboarding | Data migration complexity, no personalization | Incompatible with B2B segment |

**Evidence Supporting Decision**:
- User interviews: 8/12 participants prefer traditional email/password for work tools
- Competitive analysis: 4/5 competitors offer email/password as primary method
- Enterprise requirement: [Customer X] explicitly requires non-OAuth login option

**Reversibility Assessment**:
| Aspect | Score |
|--------|:-----:|
| Technical reversibility | Easy (can add OAuth without breaking existing) |
| Cost to reverse | Low (additive change) |
| Time to reverse | Days |
| **Overall** | **Type 2** (easily reversible) |

---

#### SEL-003: AI Suggestions

**Feature**: EPIC-003.F01 AI-Powered Suggestions
**Decision**: EXCLUDE from all variants

**Why Considered**:
- JTBD-EMOT-002: "Feel confident I'm not missing opportunities"
- Competitive differentiation potential
- User request frequency: 3/12 interviews mentioned "smart suggestions"

**Why Excluded**:
1. **Technical risk**: ML pipeline not validated; no in-house expertise
2. **Data requirement**: Need 10K+ user actions for meaningful training
3. **Scope impact**: Adds 6+ weeks to timeline, 2 FTEs
4. **Reversibility concern**: AI features create user expectations hard to roll back

**Alternative for Users**:
- Manual workflow with templates covers 80% of use case
- Document common patterns in help content
- Consider rule-based suggestions as stepping stone

**Revisit Trigger**:
- [ ] After 1000 MAU (sufficient data for ML)
- [ ] If competitor launches AI feature successfully
- [ ] If technical POC proves feasibility in <2 weeks

---

### JTBD Coverage Analysis

<!--
  This matrix ensures EVERY documented JTBD has feature coverage.
  GAPs indicate potential scope issues or explicit non-goals.
-->

| JTBD ID | Job Description | Type | Features Addressing | Coverage | Gap Action |
|---------|-----------------|------|---------------------|:--------:|------------|
| JTBD-FUNC-001 | Create and save work | Functional | F01, F02 | FULL | — |
| JTBD-FUNC-002 | Quick access to recent | Functional | F03 | FULL | — |
| JTBD-FUNC-003 | Share with team | Functional | — | GAP | Deferred to H2 (SEL-004) |
| JTBD-EMOT-001 | Feel in control | Emotional | F04 | PARTIAL | Add settings in v1.1 |
| JTBD-EMOT-002 | Confident not missing opp | Emotional | — | GAP | Excluded: AI risk (SEL-003) |
| JTBD-SOC-001 | Look competent to boss | Social | F05 | FULL | — |

**Gap Analysis Summary**:
- **2 JTBD have gaps**: JTBD-FUNC-003, JTBD-EMOT-002
- **Acceptable because**: Both are secondary jobs; primary jobs fully covered
- **Mitigation**: Manual workarounds documented; revisit triggers defined

---

### Excluded Features Rationale

| Feature | Why Considered | Why Excluded | Alternative for Users | Revisit When |
|---------|----------------|--------------|----------------------|--------------|
| AI Suggestions | User delight, differentiation | Technical risk, data requirement | Manual templates | 1000+ MAU |
| Mobile Native | JTBD-SOC-001 coverage | Web-first strategy, resource constraint | Responsive web | After web PMF |
| Self-hosting | Enterprise request | Support complexity, security surface | Cloud-only with SOC2 | Enterprise tier defined |
| Real-time Collab | Team productivity | Complexity, requires operational overhead | Async workflow | After core stable |

---

### Feature-Persona Mapping

| Persona | Primary JTBD | Features Addressing | Coverage |
|---------|--------------|---------------------|:--------:|
| [Persona 1] | JTBD-FUNC-001, JTBD-EMOT-001 | F01, F02, F04 | 100% |
| [Persona 2] | JTBD-FUNC-002, JTBD-SOC-001 | F03, F05 | 100% |
| [Persona 3 - Secondary] | JTBD-FUNC-003 | — | 0% (Deferred) |

```

---

## Validation Checklist

Before finalizing Feature Selection Rationale section:

- [ ] Every feature in Feature Hierarchy has a SEL-XXX entry
- [ ] Every SEL-XXX has explicit JTBD link (JTBD-xxx-xxx format)
- [ ] At least 2 alternatives analyzed for each INCLUDE decision
- [ ] EXCLUDE decisions have "Why Excluded" + "Alternative for Users" + "Revisit When"
- [ ] DEFER decisions have explicit trigger conditions
- [ ] JTBD Coverage Analysis shows no unexplained gaps
- [ ] Evidence cited for major decisions (user quotes, data, competitive analysis)
- [ ] Reversibility assessed for all INCLUDE decisions

---

## ID Format Standards

### Selection Decision IDs

Format: `SEL-NNN` where NNN is sequential (001, 002, 003...)

```text
SEL-001  ← First selection decision
SEL-002  ← Second selection decision
...
SEL-025  ← Twenty-fifth selection decision
```

### JTBD Reference Format

When referencing JTBD from persona-jtbd.md:

```text
JTBD-FUNC-001  ← Functional job #1
JTBD-FUNC-002  ← Functional job #2
JTBD-EMOT-001  ← Emotional job #1
JTBD-SOC-001   ← Social job #1
```

### Feature Reference Format

When referencing features from Feature Hierarchy:

```text
EPIC-001.F01   ← Epic 1, Feature 1
F01, F02       ← Shorthand in tables (context clear)
```

---

## Integration with Other Sections

### Feature Hierarchy Enhancement

Each feature entry gains a "Selection" reference:

```markdown
#### Feature: [EPIC-001.F01] User Registration

**Description**: Allow users to create accounts
**User Value**: Save work, personalized experience
**Priority**: P1a
**Dependencies**: None
**Selection**: SEL-001 (see Feature Selection Rationale)
```

### Traceability to Specification

When running `/speckit.specify`, selection rationale carries forward:

```markdown
## Traceability

| Concept ID | Selection ID | JTBD | Requirement |
|------------|--------------|------|-------------|
| EPIC-001.F01.S01 | SEL-001 | JTBD-FUNC-001 | FR-001: User Registration |
```

### CQS Scoring Integration

Selection Rationale contributes to Transparency component:

| Criterion | Points | Check |
|-----------|:------:|-------|
| Selection table complete | 15 | Every feature has SEL-XXX |
| Per-feature JTBD links | 25 | >80% features have JTBD reference |
| Alternatives documented | 10 | INCLUDE decisions have 2+ alternatives |

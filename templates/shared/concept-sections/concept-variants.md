# Concept Variants

> **Purpose**: Generate scope variations (MINIMAL/BALANCED/AMBITIOUS) of the selected product alternative to make MVP planning transparent.

> **IMPORTANT**: In v2.0, this is DIFFERENT from Product Alternatives (see product-alternatives.md)

## Distinction: Product Alternatives vs Concept Variants

| Aspect | Product Alternatives | Concept Variants (this file) |
|--------|---------------------|------------------------------|
| **What** | Different product VISIONS | Different SCOPE levels |
| **Question** | "WHAT should we build?" | "HOW MUCH should we build?" |
| **Phase** | Phase 0d (Discovery) | Step 12 (Optional) |
| **Examples** | Chat app vs Doc app vs Visual workspace | Chat app with 5 vs 12 vs 25 features |
| **Status** | REQUIRED in v2.0 | OPTIONAL in v2.0 |
| **Command** | `/speckit.concept` (Phase 0d) | `/speckit.concept-variants` |
| **CQS Impact** | Strategic Depth (30/100 pts) | Transparency (10/100 pts bonus) |

## Integration Notes

- **Depends on**: Feature Hierarchy, persona-jtbd.md, effort estimates
- **Feeds into**: Implementation planning, roadmap, release scoping
- **CQS Impact**: Transparency component (10% bonus, OPTIONAL in v2.0)
- **Status in v2.0**: OPTIONAL — Generated via `/speckit.concept-variants` command
- **Relationship**: Scope variants are for the selected Product Alternative (from Phase 0d/0e)

---

## Variant Generation Algorithm

```text
INPUTS:
  - Solution approaches from Phase 0c (Option 1-5)
  - JTBD prioritization from persona-jtbd.md
  - Technical hints from Phase 4

FOR EACH feature candidate:
  1. Classify by JTBD priority:
     - MUST_HAVE: Directly enables PRIMARY functional JTBD
     - SHOULD_HAVE: Enables SECONDARY JTBD or emotional jobs
     - COULD_HAVE: Enables social jobs or nice-to-have

  2. Assign to variants:
     MINIMAL:   MUST_HAVE only
     BALANCED:  MUST_HAVE + SHOULD_HAVE (Impact/Effort > threshold)
     AMBITIOUS: All features (MUST + SHOULD + COULD)

  3. Calculate variant metrics:
     - Feature count
     - Estimated effort (sum of feature T-shirt sizes)
     - Risk score (technical complexity weighted average)
     - Differentiation score (from Blue Ocean analysis)

  4. Generate recommendation:
     DEFAULT: BALANCED (unless constraints dictate otherwise)
     OVERRIDE if:
       - Timeline < 8 weeks → recommend MINIMAL
       - "Land and expand" strategy → recommend MINIMAL
       - Competitive pressure high → recommend AMBITIOUS
```

---

## Template: Concept Variants Section

```markdown
## Concept Variants

<!--
  PURPOSE: Make feature selection transparent by showing alternatives.
  This section answers: "Why THIS set of features and not another?"

  Three variants represent strategic trade-offs:
  - MINIMAL: Speed to market, validate hypothesis
  - BALANCED: Core value + differentiation
  - AMBITIOUS: Full vision, market leadership
-->

### Variant Comparison Matrix

| Dimension | MINIMAL | BALANCED | AMBITIOUS |
|-----------|:-------:|:--------:|:---------:|
| Time to MVP | [X] weeks | [Y] weeks | [Z] weeks |
| Team Size | [N] FTEs | [N] FTEs | [N] FTEs |
| Feature Count | [N] features | [N] features | [N] features |
| Risk Level | Low | Medium | High |
| Differentiation | Table stakes | Competitive | Market leader |
| Estimated Cost | $[X]K | $[Y]K | $[Z]K |
| JTBD Coverage | Primary only | Primary + Secondary | All JTBD |

### Recommended Variant: [BALANCED]

**Why this recommendation**:
1. **[Constraint/Goal fit]**: [How BALANCED aligns with timeline/budget]
2. **[Differentiation]**: [What BALANCED includes that makes us competitive]
3. **[Risk balance]**: [What risky features BALANCED avoids vs AMBITIOUS]

**When to choose differently**:
- Choose MINIMAL if: [specific condition, e.g., "runway < 6 months"]
- Choose AMBITIOUS if: [specific condition, e.g., "funding secured for 18 months"]

---

### Variant: MINIMAL MVP

**Philosophy**: Ship fastest, validate core hypothesis, iterate based on feedback

**Target Timeline**: [X] weeks
**Team Requirement**: [N] FTEs
**Risk Profile**: Low — proven patterns, minimal dependencies

#### Included Features ([N] total)

| Feature ID | Name | JTBD | Priority | Why Included |
|------------|------|------|----------|--------------|
| EPIC-001.F01 | [Feature Name] | JTBD-FUNC-001 | P1a | Core value proposition |
| EPIC-001.F02 | [Feature Name] | JTBD-FUNC-002 | P1a | Required for primary journey |
| ... | ... | ... | ... | ... |

#### What MINIMAL Sacrifices

| Feature | JTBD Impact | Risk of Exclusion | Mitigation |
|---------|-------------|-------------------|------------|
| [Feature A] | JTBD-FUNC-003 unaddressed | Users may not see differentiation | Manual workaround documented |
| [Feature B] | JTBD-SOC-001 unaddressed | Limited to solo users | Add in v1.1 based on feedback |

#### Best For
- [ ] Pre-seed/seed stage startups
- [ ] Quick hypothesis validation
- [ ] Resource-constrained teams
- [ ] "Land and expand" go-to-market

---

### Variant: BALANCED (Recommended)

**Philosophy**: Core value proposition + key differentiators that create competitive advantage

**Target Timeline**: [Y] weeks
**Team Requirement**: [N] FTEs
**Risk Profile**: Medium — includes some technical complexity for differentiation

#### Included Features ([N] total)

| Feature ID | Name | JTBD | Priority | Why Included |
|------------|------|------|----------|--------------|
| [All MINIMAL features] | | | | |
| EPIC-002.F01 | [Feature Name] | JTBD-FUNC-003 | P1b | Key differentiator |
| EPIC-002.F02 | [Feature Name] | JTBD-EMOT-001 | P2a | User delight |
| ... | ... | ... | ... | ... |

#### What BALANCED Adds Over MINIMAL

| Feature ID | Name | Why Added | JTBD | Effort |
|------------|------|-----------|------|--------|
| EPIC-002.F01 | [Feature] | Competitive parity with [Competitor] | JTBD-FUNC-003 | M |
| EPIC-002.F02 | [Feature] | Top user request from research | JTBD-EMOT-001 | S |

#### What BALANCED Excludes vs AMBITIOUS

| Feature | Why Excluded | When to Reconsider |
|---------|--------------|-------------------|
| [Feature X] | Technical risk unvalidated | After POC proves feasibility |
| [Feature Y] | Nice-to-have, not core | After PMF achieved |

#### Best For
- [ ] Series A/B companies
- [ ] Competitive markets requiring differentiation
- [ ] Teams with 6-12 month runway
- [ ] Products seeking product-market fit

---

### Variant: AMBITIOUS

**Philosophy**: Full product vision, maximum differentiation, market leadership position

**Target Timeline**: [Z] weeks
**Team Requirement**: [N] FTEs
**Risk Profile**: High — includes unproven technical approaches, larger scope

#### What AMBITIOUS Adds Over BALANCED

| Feature ID | Name | Why Added | Risk | Effort |
|------------|------|-----------|------|--------|
| EPIC-003.F01 | [Feature] | Market leadership differentiator | HIGH: Unproven tech | XL |
| EPIC-003.F02 | [Feature] | Addresses aspirational JTBD | MEDIUM: Complex UX | L |
| ... | ... | ... | ... | ... |

#### Additional Risks in AMBITIOUS

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| Technical feasibility of [Feature X] | Medium | High | POC before full build |
| Scope creep from interconnected features | High | Medium | Strict phase gates |
| Team scaling challenges | Medium | Medium | Hiring plan defined |

#### Best For
- [ ] Well-funded companies (Series B+)
- [ ] Markets with high switching costs
- [ ] Teams with proven execution track record
- [ ] "Winner takes all" competitive dynamics

---

### Variant Selection Decision Log

| Decision Point | Considered | Chosen | Rationale |
|----------------|------------|:------:|-----------|
| Overall approach | MINIMAL, BALANCED, AMBITIOUS | BALANCED | [Specific reasoning] |
| [Feature X] in scope | Include / Exclude | Include | [Why: JTBD alignment, competitive need] |
| [Feature Y] in scope | Include / Exclude | Exclude | [Why: Technical risk, can add later] |

```

---

## Validation Checklist

Before finalizing Concept Variants section:

- [ ] All three variants (MINIMAL, BALANCED, AMBITIOUS) are documented
- [ ] Comparison matrix has all 7 dimensions filled
- [ ] Recommendation includes specific "why" rationale (not just "it's recommended")
- [ ] Each variant lists included features with JTBD links
- [ ] MINIMAL shows what it sacrifices and why that's acceptable
- [ ] BALANCED shows what it adds over MINIMAL with justification
- [ ] AMBITIOUS shows additional risks and when it makes sense
- [ ] "When to choose differently" guidance is specific, not generic
- [ ] Decision log captures key trade-off decisions

---

## Example: SaaS Analytics Platform

```markdown
### Variant Comparison Matrix

| Dimension | MINIMAL | BALANCED | AMBITIOUS |
|-----------|:-------:|:--------:|:---------:|
| Time to MVP | 6 weeks | 12 weeks | 20 weeks |
| Team Size | 2 FTEs | 4 FTEs | 7 FTEs |
| Feature Count | 8 features | 18 features | 32 features |
| Risk Level | Low | Medium | High |
| Differentiation | Table stakes | Competitive | Market leader |
| Estimated Cost | $120K | $280K | $520K |
| JTBD Coverage | Primary only | Primary + Secondary | All JTBD |

### Recommended Variant: BALANCED

**Why this recommendation**:
1. **Timeline fit**: 12-week timeline aligns with Q3 launch window before competitor's announced release
2. **Differentiation**: Includes real-time dashboards (EPIC-002.F01) — key differentiator vs spreadsheet alternatives
3. **Risk balance**: Excludes AI predictions (EPIC-003.F01) which has unproven ML pipeline, can add post-PMF

**When to choose differently**:
- Choose MINIMAL if: Runway drops below 8 months or key developer leaves
- Choose AMBITIOUS if: Strategic partnership with data vendor materializes (reduces ML risk)
```

---

## Integration with Other Sections

### Executive Summary Update

After generating variants, update Executive Summary:

```markdown
### Our Approach
[2-3 sentences describing BALANCED approach]

**Concept Variant**: BALANCED — [brief rationale]
See "Concept Variants" section for alternatives (MINIMAL, AMBITIOUS) and detailed comparison.
```

### Feature Hierarchy Linkage

Each feature in Feature Hierarchy should reference its variant assignment:

```markdown
#### Feature: [EPIC-001.F01] User Registration

**Description**: ...
**User Value**: ...
**Priority**: P1a
**Variants**: ALL (MINIMAL, BALANCED, AMBITIOUS)
```

### CQS Scoring Integration

Concept Variants contributes to Transparency component of CQS-E:

| Criterion | Points | Check |
|-----------|:------:|-------|
| 3 variants documented | 25 | MINIMAL + BALANCED + AMBITIOUS present |
| Comparison matrix complete | 15 | All 7 dimensions have values |
| Recommendation rationale | 10 | "Why this recommendation" has 3+ specific reasons |

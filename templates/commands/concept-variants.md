---
description: Generate MINIMAL/BALANCED/AMBITIOUS scope variants for existing concept
claude_code:
  model: sonnet
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 4000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 8000
        max_parallel: 3
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 16000
        max_parallel: 6
        batch_delay: 1500
        wave_overlap_threshold: 0.65
  cache_hierarchy: full
---

# /speckit.concept-variants

## Purpose

Generate scope variations (MINIMAL/BALANCED/AMBITIOUS) for an existing concept.md.

**Use this when**: You have a complete concept and want to explore different scope levels for MVP planning.

**Important Distinction**:
- **Product Alternatives** (`/speckit.concept` Phase 0d) = Different VISIONS (what to build)
- **Scope Variants** (this command) = Different SCOPE levels (how much to build) of SAME vision

## Prerequisites

Before running this command, ensure:
- [ ] `specs/concept.md` exists and is complete
- [ ] Feature Hierarchy section is populated
- [ ] Personas with JTBD (Jobs-to-be-Done) are defined
- [ ] Features have effort estimates (S/M/L/XL)

## Execution Flow

### Step 1: Load and Validate Concept

```text
1. Read specs/concept.md
2. Validate prerequisites:
   - Feature Hierarchy exists with ≥5 features
   - JTBD section populated
   - Effort estimates present (≥50% of features)
3. If validation fails:
   - ERROR: "Cannot generate variants - missing [prerequisite]"
   - SUGGEST: "Complete concept first with /speckit.concept"
```

### Step 2: Classify Features by Priority

Apply JTBD-based classification:

```text
FOR EACH feature in Feature Hierarchy:
  1. Extract JTBD linkage (if present)
  2. Classify by JTBD type:
     - MUST_HAVE: Enables PRIMARY functional JTBD (JTBD-FUNC-xxx with P1a/P1b priority)
     - SHOULD_HAVE: Enables SECONDARY JTBD or emotional jobs (P2a/P2b priority)
     - COULD_HAVE: Enables social jobs or nice-to-have (P3 priority)

  3. If no JTBD linkage, infer from feature priority:
     - P1a/P1b → MUST_HAVE
     - P2a/P2b → SHOULD_HAVE
     - P3/P4 → COULD_HAVE

  4. Store classification for variant assignment
```

### Step 3: Assign Features to Variants

```text
VARIANT ASSIGNMENT ALGORITHM:

MINIMAL Variant:
  - Include: All MUST_HAVE features
  - Rationale: Minimum viable feature set to validate core hypothesis
  - Philosophy: "Ship fastest, learn fastest"

BALANCED Variant:
  - Include: All MUST_HAVE features
  - Include: SHOULD_HAVE features where (Impact/Effort > threshold)
  - Threshold: SHOULD_HAVE features with HIGH impact and ≤M effort
  - Rationale: Core value + key differentiators
  - Philosophy: "Competitive without overbuilding"

AMBITIOUS Variant:
  - Include: All features (MUST_HAVE + SHOULD_HAVE + COULD_HAVE)
  - Rationale: Full product vision, market leadership
  - Philosophy: "Complete vision, maximum differentiation"
```

### Step 4: Calculate Variant Metrics

For each variant, calculate:

```text
1. Feature Count:
   MINIMAL_COUNT = count(MUST_HAVE features)
   BALANCED_COUNT = count(MUST_HAVE + selected SHOULD_HAVE)
   AMBITIOUS_COUNT = count(all features)

2. Estimated Effort:
   Sum T-shirt sizes (S=1, M=2, L=4, XL=8 weeks)
   MINIMAL_EFFORT = sum(effort for MINIMAL features)
   BALANCED_EFFORT = sum(effort for BALANCED features)
   AMBITIOUS_EFFORT = sum(effort for all features)

3. Risk Score:
   Average technical complexity (Low=1, Med=2, High=3)
   MINIMAL_RISK = avg(complexity for MINIMAL features)
   BALANCED_RISK = avg(complexity for BALANCED features)
   AMBITIOUS_RISK = avg(complexity for all features)

4. Differentiation Score (if Blue Ocean section exists):
   Sum "Create" and "Raise" factors covered by variant
   Scale: Low=1-3, Medium=4-6, High=7-10

5. JTBD Coverage:
   MINIMAL: Primary functional JTBD only
   BALANCED: Primary + secondary JTBD
   AMBITIOUS: All JTBD (functional + emotional + social)
```

### Step 5: Generate Recommendation

```text
DEFAULT_RECOMMENDATION = "BALANCED"

OVERRIDE RULES:
  IF timeline_constraint < 8 weeks:
    RECOMMEND "MINIMAL"
    REASON = "Timeline constraint requires fastest MVP"

  IF strategy matches "land and expand":
    RECOMMEND "MINIMAL"
    REASON = "Land-and-expand strategy prioritizes speed to market"

  IF competitive_pressure == "HIGH" AND funding_secured >= 12_months:
    RECOMMEND "AMBITIOUS"
    REASON = "Market leadership position required to compete"

  IF risk_tolerance == "LOW":
    RECOMMEND "MINIMAL"
    REASON = "Low risk tolerance favors proven features only"

DOCUMENT RATIONALE:
  1. Timeline/Constraint fit
  2. Differentiation reasoning
  3. Risk balance rationale
```

### Step 6: Generate Comparison Matrix

Create comparison table:

```markdown
### Variant Comparison Matrix

| Dimension | MINIMAL | BALANCED | AMBITIOUS |
|-----------|:-------:|:--------:|:---------:|
| Time to MVP | [X] weeks | [Y] weeks | [Z] weeks |
| Team Size | [N] FTEs | [N] FTEs | [N] FTEs |
| Feature Count | [N] features | [N] features | [N] features |
| Risk Level | [Low/Med/High] | [Low/Med/High] | [Low/Med/High] |
| Differentiation | [Low/Med/High] | [Low/Med/High] | [Low/Med/High] |
| Estimated Cost | $[X]K | $[Y]K | $[Z]K |
| JTBD Coverage | Primary only | Primary + Secondary | All JTBD |

### Recommended Variant: [BALANCED]

**Why this recommendation**:
1. **[Timeline fit]**: [Specific reasoning]
2. **[Differentiation]**: [Specific reasoning]
3. **[Risk balance]**: [Specific reasoning]

**When to choose differently**:
- Choose MINIMAL if: [Specific condition, e.g., "runway < 6 months"]
- Choose AMBITIOUS if: [Specific condition, e.g., "funding secured for 18 months"]
```

### Step 7: Generate Detailed Variant Sections

For each variant, generate:

```markdown
---

### Variant: [MINIMAL MVP / BALANCED / AMBITIOUS]

**Philosophy**: [Variant philosophy statement]

**Target Timeline**: [X] weeks | **Team**: [N] FTEs | **Risk**: [Low/Med/High]

#### Included Features ([N] total)

| Feature ID | Name | JTBD | Priority | Why Included |
|------------|------|------|----------|--------------|
| EPIC-001.F01 | [Feature] | JTBD-FUNC-001 | P1a | [Reasoning] |
| ... | ... | ... | ... | ... |

#### [For BALANCED/AMBITIOUS] What [VARIANT] Adds Over [PREVIOUS]

| Feature ID | Name | Why Added | Effort | Risk |
|------------|------|-----------|--------|------|
| EPIC-002.F01 | [Feature] | [Reasoning] | M | Med |

#### [For MINIMAL/BALANCED] What [VARIANT] Excludes

| Feature | JTBD Impact | Risk of Exclusion | When to Reconsider |
|---------|-------------|-------------------|-------------------|
| [Feature X] | JTBD-FUNC-003 unaddressed | Users may not see differentiation | After PMF achieved |

#### Best For

- [ ] [Context where this variant makes sense]
- [ ] [Another suitable context]
```

### Step 8: Update Concept.md

```text
1. Locate "Concept Variants (OPTIONAL)" section in specs/concept.md
2. Update status: [ ] Not generated → [x] Generated
3. Replace placeholder content with generated variants
4. Update Section Completion Checklist if present
5. Save updated concept.md
```

### Step 9: Report to User

```text
✅ Generated 3 scope variants:
   - MINIMAL: [N] features, [X] weeks, [Risk level]
   - BALANCED: [M] features, [Y] weeks, [Risk level] ← RECOMMENDED
   - AMBITIOUS: [P] features, [Z] weeks, [Risk level]

📄 Updated: specs/concept.md (Concept Variants section)

💡 Recommendation: [BALANCED]
   Rationale: [Brief reasoning]

Next steps:
- Review variants in specs/concept.md
- Choose variant for specification: /speckit.specify [feature-id]
```

## Reference

**Template**: `templates/shared/concept-sections/concept-variants.md`
**Related Command**: `/speckit.concept` (includes Product Alternatives generation)

## Example Usage

```bash
# After completing concept:
/speckit.concept

# Generate scope variants on-demand:
/speckit.concept-variants

# Output: specs/concept.md updated with MINIMAL/BALANCED/AMBITIOUS variants
```

## Error Handling

| Error Condition | Message | Suggested Action |
|----------------|---------|------------------|
| No concept.md | `ERROR: specs/concept.md not found` | Run `/speckit.concept` first |
| No Feature Hierarchy | `ERROR: Feature Hierarchy section empty` | Complete concept with features |
| No JTBD data | `WARN: No JTBD data found, using priority-based classification` | Continue with fallback |
| <5 features | `WARN: Only [N] features found, variants may not be meaningful` | Consider adding more features or skip variants |

## Quality Checks

Before completing:
- [ ] All 3 variants generated (MINIMAL, BALANCED, AMBITIOUS)
- [ ] Comparison matrix complete with all dimensions
- [ ] Recommendation includes specific rationale (≥3 reasons)
- [ ] Each variant shows included features with JTBD links
- [ ] "What excludes" and "When to reconsider" documented for MINIMAL/BALANCED
- [ ] Variant assignment reflects actual feature priorities

## Notes

- **NOT required** in v2.0 - Product Alternatives are the primary exploration mechanism
- **USE WHEN**: You need MVP scope planning for selected product alternative
- **SKIP WHEN**: You haven't selected a product alternative yet (run `/speckit.concept` first)
- Scope variants can be generated at any time after concept completion
- Variants help with roadmap planning and release scoping

# CQS Formula - Concept Quality Score

**Version**: 0.7.0  
**Scale**: 0-120 points  
**Purpose**: Validate strategic concept readiness before specification phase

## Formula (11 Components)

```
CQS-E = (
  Market × 0.16 +            # Market Framework quality
  Persona × 0.12 +           # Persona-JTBD depth
  Metrics × 0.12 +           # Metrics SMART validation
  Features × 0.12 +          # Feature completeness
  Risk × 0.08 +              # Risk assessment quality
  Technical × 0.08 +         # Technical architecture
  Strategic_Clarity × 0.08 +  # Vision clarity
  Strategic_Depth × 0.10 +    # Pillars, differentiators, roadmap
  Validation × 0.05 +         # Evidence backing
  Transparency × 0.05 +       # Decision rationale
  Quality_Intent × 0.04       # Rigor signals
) × 100 × Evidence_Multiplier
```

## Component Definitions

### Market (16% weight, 100 pts max)
- **TAM/SAM/SOM analysis**: Is market sizing triangulated with top-down + bottom-up?
- **Porter's 5 Forces**: Market dynamics assessed (rivalry, entry, substitutes, buyer power, supplier power)?
- **Blue Ocean Canvas**: Competitive differentiation mapped with ERRC Grid?
- **Evidence tier**: STRONG+ required (≥3 sources per claim)

### Persona (12% weight, 100 pts max)
- **2-4 personas defined**: Demographics, pain points, goals, buying behavior?
- **JTBD synthesis**: Functional, emotional, social jobs articulated?
- **Willingness-to-Pay**: WTP range per persona with price anchors?
- **Evidence tier**: STRONG+ required

### Metrics (12% weight, 100 pts max)
- **SMART validation**: Goals are Specific, Measurable, Achievable, Relevant, Time-bound?
- **North Star defined**: Primary metric aligned with business model + growth stage?
- **Leading indicators**: 3-5 leading indicators that predict North Star?
- **Evidence tier**: MEDIUM+ required

### Features (12% weight, 100 pts max)
- **Epic/Feature/Story hierarchy**: Structured requirement breakdown?
- **User journey mapping**: How features flow through customer journey?
- **MVP clarity**: What's in MVP vs nice-to-have vs future?
- **Evidence tier**: MEDIUM+ required

### Risk (8% weight, 100 pts max)
- **≥5 risks documented**: Technical, market, execution, financial risks?
- **Impact/Likelihood assessed**: HIGH/MEDIUM/LOW ratings for each risk?
- **Mitigations defined**: What will we do to reduce each risk?
- **Evidence tier**: MEDIUM required

### Technical (8% weight, 100 pts max)
- **Architecture outlined**: Layers, services, data model?
- **Dependencies identified**: Third-party services, infrastructure, tech stack?
- **Scalability considered**: Can we reach target users/revenue?
- **Evidence tier**: MEDIUM required

### Strategic Clarity (8% weight, 100 pts max)
- **Vision is concrete**: Not vague ("be great"), but specific ("dominate X segment with Y feature")?
- **Why now**: Timing justified by trends, maturity, adoption signals?
- **Long-term positioning**: Year 1, 3, 5 vision articulated?
- **Evidence tier**: MEDIUM required

### Strategic Depth (10% weight, 100 pts max)
**NEW component capturing full strategic thinking**

**Three Foundational Pillars** (25 pts):
- Are 3 pillars defined with memorable names? (5 pts)
- Do they address ≥2 pain points each with PP-XXX links? (5 pts)
- Do they have ≥2 proof points each with STRONG+ evidence? (10 pts)
- Is differentiation specific to competitors? (5 pts)

**Five Breakthrough Differentiators** (25 pts):
- Are 5 differentiators defined? (5 pts)
- Do they have market reality + specific tactics? (10 pts)
- Are barriers to entry documented? (5 pts)
- Is time to imitation justified? (5 pts)

**Phase-Based Strategic Recommendations** (25 pts):
- Are 3 phases defined (Foundation/Scale/Dominate)? (5 pts)
- Do phases have 3-5 actions each with measurable targets? (10 pts)
- Are success criteria quantitative (≥4) + qualitative (≥2)? (5 pts)
- Are actions linked to Three Pillars? (5 pts)

**Critical Success Factors** (15 pts):
- Are ≥5 CSFs documented? (5 pts)
- Do CSFs have "How to Ensure" guidance? (5 pts)
- Are CSFs derived from Pillars/Differentiation? (5 pts)

**Risk/Mitigation Matrix** (10 pts):
- Are ≥5 risks documented? (3 pts)
- Do risks have likelihood/impact/mitigation/owner? (4 pts)
- Are contingency plans defined for HIGH-HIGH risks? (3 pts)

### Validation (5% weight, 100 pts max)
- **Evidence tier**: What % of claims are backed by STRONG+/MEDIUM/WEAK evidence?
- **Source quality**: Are sources authoritative (Gartner, peer-reviewed, industry leaders)?
- **Recency**: Is evidence from last 12 months (not stale)?

### Transparency (5% weight, 100 pts max)
- **Trade-offs documented**: What were alternatives considered + why rejected?
- **Assumptions explicit**: What are key assumptions that could be wrong?
- **Decision rationale**: Why this direction over alternatives?

### Quality Intent (4% weight, 100 pts max)
- **Rigor signals**: Evidence of thorough thinking (frameworks applied, alternatives considered, edge cases addressed)?
- **Not AI-generic**: Concept reflects deep knowledge of domain + competitive landscape?

## Scoring Guidance

### Quality Gates
- **≥80**: READY (Green) — Proceed to specification
- **60-79**: CAUTION (Yellow) — Address gaps, then proceed
- **<60**: NOT READY (Red) — Substantial rework required

### Evidence Multiplier
- **If ≥90% claims have STRONG+**: 1.2× multiplier
- **If 70-89% claims have STRONG+**: 1.1× multiplier
- **If 50-69% claims have STRONG+**: 1.0× multiplier (no bonus)
- **If <50% claims have STRONG+**: 0.9× multiplier (penalty)

## Application

When running `/speckit.concept`:

1. **Concept-Quality-Validator agent** calculates CQS after all research complete
2. **For each variant**: Calculate component scores (0-100), apply weights
3. **Calculate base CQS**: Sum all weighted components
4. **Apply evidence multiplier**: Adjust based on source quality
5. **Output**: CQS-E score with 11-component breakdown
6. **Quality gate**: Flag if <80 for improvement recommendations

## Template References

This formula is referenced from:
- `templates/commands/concept.md` — Lines 767-830 (concept-quality-auditor agent)
- `templates/commands/concept.md` — Lines 1923-1958 (CQS calculation)
- Used for concept variant selection and strategic readiness validation

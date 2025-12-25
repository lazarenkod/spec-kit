---
description: Perform comprehensive competitive analysis for product positioning and differentiation
---

## User Input

```text
$ARGUMENTS
```

## Purpose

This skill performs deep competitive analysis to inform product strategy, positioning, and feature prioritization. Uses web research combined with Claude Code's analysis capabilities.

## When to Use

- Before `/speckit.concept` for new product ideas
- When evaluating feature differentiation
- During strategic planning and roadmap decisions
- When responding to competitive pressure

## Execution Steps

### 1. Parse Competitive Context

Extract from user input:
- **Product Domain**: What market/category?
- **Known Competitors**: Any mentioned by name?
- **Our Product**: Current positioning (if exists)
- **Focus Area**: Features, pricing, UX, market share?

### 2. Competitor Identification

Use WebSearch to find competitors:

```text
Search queries:
1. "[domain] software solutions 2025 market leaders"
2. "[product type] alternatives comparison"
3. "best [domain] tools for [target user]"
4. "[known competitor] competitors alternatives"
```

Build competitor list (aim for 5-10 relevant competitors).

### 3. Deep Competitor Analysis

For each competitor, research:

#### 3a. Product Analysis
```text
Search: "[competitor] features capabilities"
Search: "[competitor] product updates 2025"
Search: "[competitor] documentation API"

Extract:
- Core features and unique capabilities
- Recent product updates and direction
- Technical architecture (if visible)
- Integration ecosystem
```

#### 3b. Market Position
```text
Search: "[competitor] pricing plans"
Search: "[competitor] customers case studies"
Search: "[competitor] market share"

Extract:
- Pricing model and tiers
- Target customer segments
- Market positioning (enterprise vs SMB vs consumer)
- Notable customers
```

#### 3c. User Perception
```text
Search: "[competitor] reviews complaints"
Search: "[competitor] vs alternatives reddit"
Search: "[competitor] problems frustrations"

Extract:
- Common praise (what they do well)
- Common complaints (pain points)
- Feature requests from users
- Support quality perception
```

### 4. Competitive Matrix

Build comparison matrix:

```markdown
| Dimension | Competitor A | Competitor B | Our Product | Opportunity |
|-----------|--------------|--------------|-------------|-------------|
| Core Features | [list] | [list] | [list] | [gaps] |
| Pricing | [model] | [model] | [model] | [position] |
| Target Users | [segment] | [segment] | [segment] | [underserved] |
| Strengths | [pros] | [pros] | [pros] | [leverage] |
| Weaknesses | [cons] | [cons] | [cons] | [exploit] |
| User Sentiment | [+/-] | [+/-] | [+/-] | [improve] |
```

### 5. Differentiation Analysis

Identify opportunities:

```markdown
## Blue Ocean Opportunities
(Features/capabilities no competitor offers well)
1. [Opportunity] - Why competitors miss this
2. [Opportunity] - User demand evidence

## Red Ocean Battles
(Must-have features where we compete directly)
1. [Feature] - Table stakes requirement
2. [Feature] - Competitive necessity

## Positioning Options
1. **Option A**: [position] - Compete on [dimension]
   - Pros: [advantages]
   - Cons: [challenges]

2. **Option B**: [position] - Differentiate via [dimension]
   - Pros: [advantages]
   - Cons: [challenges]
```

### 6. Generate Report

Create `specs/research/competitive-analysis.md`:

```markdown
# Competitive Analysis: [DOMAIN]

**Date**: [DATE]
**Analyst**: Claude Code (competitive-analysis skill)

## Executive Summary

[2-3 sentence key findings and recommendation]

## Competitive Landscape

### Tier 1 Competitors (Direct)
| Competitor | Position | Threat Level | Key Differentiator |
|------------|----------|--------------|-------------------|
| [Name] | [Position] | High/Med/Low | [What makes them stand out] |

### Tier 2 Competitors (Indirect)
| Competitor | Position | Overlap Area |
|------------|----------|--------------|
| [Name] | [Position] | [Where we compete] |

## Detailed Competitor Profiles

### [Competitor Name]

**Overview**: [1-2 sentences]

**Strengths**:
- [Strength with evidence]

**Weaknesses**:
- [Weakness with evidence]

**User Sentiment**: [Positive/Mixed/Negative]
- "[Quote from user review]"

**Pricing**: [Model and tiers]

**Key Takeaway**: [What to learn/avoid]

## Feature Comparison Matrix

| Feature | Us | Comp A | Comp B | Comp C | Priority |
|---------|-----|--------|--------|--------|----------|
| [Feature] | ✓/✗/◐ | ✓/✗/◐ | ✓/✗/◐ | ✓/✗/◐ | Must/Should/Could |

Legend: ✓ = Has, ✗ = Missing, ◐ = Partial

## Strategic Recommendations

### Differentiation Strategy
[Recommended positioning with rationale]

### Feature Priorities
1. **Must Build**: [Feature] - [competitive necessity]
2. **Should Build**: [Feature] - [differentiation opportunity]
3. **Consider**: [Feature] - [nice-to-have]

### Competitive Responses
- **If [Competitor] does X**: [Our response]
- **If [Competitor] does Y**: [Our response]

## Sources

- [URL 1]
- [URL 2]
```

## Output

1. Report saved to `specs/research/competitive-analysis.md`
2. Key findings summary
3. Recommended next: `/speckit.prioritization` or `/speckit.concept`

## Integration with Spec Kit

Feeds into:
- `/speckit.concept` → Market positioning and differentiation
- `/speckit.specify` → Feature prioritization rationale
- Product roadmap decisions

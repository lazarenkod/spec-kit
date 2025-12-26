# RICE Prioritization Framework Guide

## Overview

RICE is a prioritization framework developed by Intercom to score and rank product initiatives. It provides a quantitative approach to prioritization, reducing bias and making trade-offs explicit.

**RICE stands for**: Reach, Impact, Confidence, Effort

## The RICE Formula

```text
RICE Score = (Reach × Impact × Confidence) / Effort
```

Higher score = Higher priority

## RICE Components

### Reach

**Definition**: How many users/customers will this impact in a given time period?

**Time Period**: Usually per quarter (3 months) or per month

**Measurement**:
| Type | How to Measure |
|------|----------------|
| Customer-facing feature | Users who will encounter it |
| Internal tool | Employees who will use it |
| Infrastructure | Users affected by improvement |

**Examples**:
- "10,000 users/quarter will see this onboarding change"
- "500 customers/month use this feature"
- "All 200,000 users benefit from performance improvement"

**Tips**:
- Use real data from analytics when possible
- For new features, use comparable feature adoption rates
- Be conservative if uncertain

### Impact

**Definition**: How much will this move the metric for each user who encounters it?

**Scale** (Intercom's original):
| Score | Meaning | Example |
|-------|---------|---------|
| 3 | Massive | Transformative, life-changing feature |
| 2 | High | Significant improvement |
| 1 | Medium | Noticeable improvement |
| 0.5 | Low | Minor improvement |
| 0.25 | Minimal | Barely noticeable |

**Metric Alignment**:
- Tie impact to your North Star metric
- "This will improve conversion by X%"
- "This will reduce churn by Y%"

**Tips**:
- Be honest about impact level
- Ask "would users notice if we removed this?"
- Consider both positive and negative impact

### Confidence

**Definition**: How sure are you about your estimates for Reach, Impact, and Effort?

**Scale**:
| Percentage | Meaning | Evidence |
|------------|---------|----------|
| 100% | High confidence | Strong data, proven pattern |
| 80% | Medium confidence | Some data, reasonable assumptions |
| 50% | Low confidence | Limited data, gut feeling |
| 20% | Very low | Pure speculation |

**What affects confidence**:
- User research (interviews, surveys)
- Analytics data
- A/B test results
- Competitive intelligence
- Technical feasibility assessment

**Tips**:
- Never use 100% unless you have definitive data
- Low confidence isn't bad — it flags need for research
- Be consistent across items

### Effort

**Definition**: How much work is required to complete this initiative?

**Unit**: Person-months (how many months of work for one person)

**Examples**:
| Estimate | Meaning |
|----------|---------|
| 0.5 | One person, 2 weeks |
| 1 | One person, 1 month |
| 2 | One person, 2 months OR two people, 1 month |
| 6 | Major project, multiple people, quarter |

**What to include**:
- Design time
- Engineering time
- Testing time
- Documentation
- Rollout and monitoring

**Tips**:
- Include all roles, not just engineering
- Account for context switching
- Add buffer for unknowns
- Get estimates from people doing the work

## RICE Calculation Examples

### Example 1: New Onboarding Flow

| Factor | Value | Reasoning |
|--------|-------|-----------|
| Reach | 5,000/quarter | New signups per quarter |
| Impact | 2 (High) | Significantly improves activation |
| Confidence | 80% | User research supports this |
| Effort | 2 person-months | Design + Eng + Testing |

```text
RICE = (5000 × 2 × 0.8) / 2 = 4,000
```

### Example 2: Performance Optimization

| Factor | Value | Reasoning |
|--------|-------|-----------|
| Reach | 50,000/quarter | All active users |
| Impact | 0.5 (Low) | Subtle improvement |
| Confidence | 100% | Technical certainty |
| Effort | 1 person-month | Well-scoped work |

```text
RICE = (50000 × 0.5 × 1.0) / 1 = 25,000
```

### Example 3: Experimental Feature

| Factor | Value | Reasoning |
|--------|-------|-----------|
| Reach | 2,000/quarter | Subset of users |
| Impact | 3 (Massive) | If it works, game-changer |
| Confidence | 20% | Highly uncertain |
| Effort | 3 person-months | Complex implementation |

```text
RICE = (2000 × 3 × 0.2) / 3 = 400
```

**Insight**: Despite massive potential impact, low confidence dramatically reduces the score. Consider running a cheaper experiment first.

## ICE: The Simpler Alternative

**ICE Score** = Impact × Confidence × Ease

| Factor | Scale | Description |
|--------|-------|-------------|
| Impact | 1-10 | How much will this move metrics? |
| Confidence | 1-10 | How sure are we? |
| Ease | 1-10 | How easy is this? (Inverse of effort) |

**When to use ICE**:
- Faster prioritization sessions
- When Reach is similar across items
- Early-stage ideation

**RICE vs ICE**:
| Aspect | RICE | ICE |
|--------|------|-----|
| Precision | Higher | Lower |
| Speed | Slower | Faster |
| Reach consideration | Explicit | Implicit in Impact |
| Best for | Roadmap planning | Quick prioritization |

## RICE Prioritization Matrix

After scoring, plot initiatives:

```text
High RICE Score
      │
      │   ★ Quick Wins      ★ Major Bets
      │   (High score,       (High score,
      │    low effort)       high effort)
      │
      ├─────────────────────────────────────
      │
      │   ✗ Don't Do        ? Maybe Later
      │   (Low score,        (Low score,
      │    any effort)       low effort)
      │
Low RICE Score ────────────────────────────►
                Low Effort       High Effort
```

## RICE Prioritization Template

```markdown
# RICE Prioritization: [Quarter/Cycle]

## Scoring Parameters
- **Time Period**: Q1 2024 (Jan-Mar)
- **North Star Metric**: [Metric name]
- **Impact Scale**: 3=Massive, 2=High, 1=Medium, 0.5=Low, 0.25=Minimal

## Initiatives

| Initiative | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|------------|-------|--------|------------|--------|------------|----------|
| [Name 1] | X | X | X% | X PM | X | P1 |
| [Name 2] | X | X | X% | X PM | X | P2 |
| [Name 3] | X | X | X% | X PM | X | P3 |

## Decisions

### Do Now (P0-P1)
- [Initiative]: RICE [score], because [rationale]

### Do Next (P2)
- [Initiative]: RICE [score], blocked by [dependency]

### Backlog (P3+)
- [Initiative]: RICE [score], revisit when [condition]

### Not Doing
- [Initiative]: RICE [score], reason: [rationale]
```

## Common RICE Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Inflating Reach | Everything "affects all users" | Be specific about who encounters it |
| Impact optimism | Everything is "High" impact | Calibrate against past features |
| Ignoring Confidence | Treating estimates as facts | Be honest about uncertainty |
| Underestimating Effort | Dev-only estimates | Include all roles, add buffer |
| Gaming the system | Adjusting to get desired priority | Have someone else validate |
| Comparing apples/oranges | Different time periods | Standardize Reach timeframe |

## Calibration Exercises

### Historical Calibration

Review past features and score them retrospectively:

| Feature | Predicted Impact | Actual Impact | Lesson |
|---------|-----------------|---------------|--------|
| Feature A | 3 (Massive) | 1 (Medium) | We overestimate new features |
| Feature B | 0.5 (Low) | 2 (High) | Bug fixes undervalued |

### Cross-Team Calibration

Have multiple people score the same item independently, then discuss differences.

## RICE Variations

### Weighted RICE

Add weights to each factor based on strategic priorities:

```text
RICE = (Reach × w1 × Impact × w2 × Confidence × w3) / Effort

Where:
w1 = Reach weight (e.g., 1.0)
w2 = Impact weight (e.g., 1.5 if growth is priority)
w3 = Confidence weight (e.g., 1.2 if de-risking is priority)
```

### RICE with Strategic Alignment

Add a strategic multiplier:

```text
RICE = (Reach × Impact × Confidence × Strategic Fit) / Effort

Strategic Fit:
1.5 = Directly supports current OKR
1.0 = Neutral
0.5 = Misaligned with current focus
```

## When RICE Isn't Enough

RICE should inform decisions, not make them. Consider also:

| Factor | Why It Matters |
|--------|----------------|
| **Dependencies** | Can't do B before A |
| **Strategic narrative** | Does this tell a coherent story? |
| **Team morale** | All tech debt, no fun projects? |
| **Learning value** | Will this teach us something? |
| **Deadline constraints** | External commitments |

## Resources

- **Original Source**: [Intercom's RICE framework](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)
- **Tools**: Spreadsheet templates, Productboard, Airfocus
- **Related Frameworks**: ICE, WSJF (SAFe), MoSCoW

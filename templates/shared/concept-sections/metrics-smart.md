# Success Metrics Framework (SMART + OKRs)

> **Purpose**: Define measurable success criteria with validated quality.

## North Star Metric

**Metric**: [Name]
**Definition**: [Precise calculation/definition]

| Attribute | Description |
|-----------|-------------|
| **Why this metric?** | [How it connects user value to business value] |
| **User value signal** | [What user success does this reflect?] |
| **Business value signal** | [What business outcome does this drive?] |
| **Manipulation risk** | [How could this be gamed? Safeguards?] |

### Supporting Metrics

| Type | Metric | Relationship to North Star |
|------|--------|---------------------------|
| **Leading** | [Predictive metric] | [Early signal of North Star movement] |
| **Leading** | [Predictive metric] | [Early signal of North Star movement] |
| **Lagging** | [Outcome metric] | [Confirms North Star impact] |
| **Lagging** | [Outcome metric] | [Confirms North Star impact] |
| **Counter** | [Guardrail metric] | [Prevents gaming/negative externalities] |

---

## Metric Quality Validation (SMART)

| Metric | S | M | A | R | T | Score | Notes |
|--------|:-:|:-:|:-:|:-:|:-:|:-----:|-------|
| [North Star] | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | X/5 | [Improvement needed] |
| [Leading 1] | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | X/5 | [Improvement needed] |
| [Leading 2] | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | X/5 | [Improvement needed] |
| [Lagging 1] | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | X/5 | [Improvement needed] |

### SMART Criteria Reference

| Letter | Meaning | Question to Ask |
|--------|---------|-----------------|
| **S** | Specific | Is it clear what exactly we're measuring? |
| **M** | Measurable | Can we track it with available tools/data? |
| **A** | Achievable | Is the target realistic given resources? |
| **R** | Relevant | Does it matter for user/business success? |
| **T** | Time-bound | Is there a deadline or timeframe? |

### Metrics Needing Improvement
- [ ] [Metric]: [Which SMART criteria fails] → [How to fix]
- [ ] [Metric]: [Which SMART criteria fails] → [How to fix]

---

## Metric Categorization

**Synthesis from**: Three Foundational Pillars (strategic), Product Features (product), Business Model (business)

### Strategic Metrics (Positioning & Moat)

Measure competitive position, market share, and defensibility of strategic pillars.

| Metric | Definition | Target | Why Strategic |
|--------|------------|--------|---------------|
| [Strategic 1] | [Calculation] | [Target] | [Measures pillar strength or market position] |
| [Strategic 2] | [Calculation] | [Target] | [Measures competitive moat or differentiation] |

**Examples**:
- Market share in beachhead segment (measures dominance)
- Net Promoter Score relative to competitors (measures differentiation perception)
- Time-to-value vs. alternatives (measures pillar effectiveness)
- Partner ecosystem size (measures network effects moat)

### Product Metrics (Engagement & Value)

Measure product usage, feature adoption, and user value delivery.

| Metric | Definition | Target | Why Product |
|--------|------------|--------|-------------|
| [Product 1] | [Calculation] | [Target] | [Measures feature usage or engagement] |
| [Product 2] | [Calculation] | [Target] | [Measures user value or retention] |

**Examples**:
- Daily/Weekly Active Users (engagement)
- Feature adoption rate (value discovery)
- Time spent in core workflow (engagement quality)
- Retention cohorts (long-term value)

### Business Metrics (Economics & Growth)

Measure unit economics, revenue, and business model health.

| Metric | Definition | Target | Why Business |
|--------|------------|--------|-------------|
| [Business 1] | [Calculation] | [Target] | [Measures revenue or profitability] |
| [Business 2] | [Calculation] | [Target] | [Measures growth or efficiency] |

**Examples**:
- MRR/ARR (revenue growth)
- CAC/LTV ratio (unit economics)
- Net Revenue Retention (expansion)
- Gross margin (profitability)

### Metric Hierarchy

```
                   [North Star Metric]
                          |
        +----------------+----------------+
        |                |                |
   Strategic         Product          Business
   Metrics           Metrics          Metrics
        |                |                |
 Pillar strength    Engagement      Unit economics
 Market position    Value delivery   Revenue growth
 Differentiation    Retention        Profitability
```

**North Star Selection Logic**: Choose the metric that best bridges user value and business value. Should be influenced by all three categories.

---

## Outcome vs. Output Metrics

**Synthesis from**: Strategic Recommendations (outcome-focused), Hypothesis Testing (learning metrics)

### Outcome-Based Metrics (PREFERRED)

Measure **results and impact**, not just activity. Answers "Did we achieve the desired change?"

| Outcome Metric | Output Metric (Avoid) | Why Outcome is Better |
|----------------|----------------------|----------------------|
| [Customer success rate] | [Features shipped] | Measures actual value, not just delivery |
| [Time saved per user] | [API calls made] | Measures impact, not just usage |
| [Revenue per customer] | [Users onboarded] | Measures monetization, not just growth |
| [Problem resolution rate] | [Support tickets closed] | Measures effectiveness, not just throughput |

### Output Metrics (Use Sparingly)

Output metrics track **activity and effort**. Useful for:
- Early-stage validation (before outcomes measurable)
- Leading indicators (predict outcomes)
- Operational health (capacity/efficiency)

**When Output Metrics are OK**:
- Pre-PMF: "X customer interviews completed" (learning metric)
- Infrastructure: "99.9% uptime" (operational health)
- Leading indicator: "Sign-ups per week" (predicts future revenue)

**When to Avoid**:
- Post-PMF: "Features shipped" doesn't prove value
- Vanity metrics: "Page views" without conversion context
- Activity traps: "Meetings held" doesn't measure progress

### Outcome Validation Checklist

For each metric, ask:
- [ ] **User benefit**: Does this measure a result users care about?
- [ ] **Business impact**: Does this tie to revenue, retention, or strategic goals?
- [ ] **Causality**: Can we influence this through our actions?
- [ ] **Manipulation-resistant**: Hard to game without delivering real value?

**Example Outcome-Focused Metric Definition**:

| Attribute | Good (Outcome) | Bad (Output) |
|-----------|----------------|--------------|
| **Metric** | "Hours saved per executive per week" | "Features used per session" |
| **Why Better** | Measures actual impact on customer's life | Measures activity, not value |
| **Ties to** | Willingness to pay, retention | Usage != value |
| **Validation** | Customer testimonials, renewal rate | Engagement can be high but valueless |

---

## OKR Structure

### Objective 1: [Qualitative goal statement]
*[Inspirational, memorable, time-bound goal]*

| Key Result | Baseline | Target | Confidence |
|------------|----------|--------|------------|
| **KR1**: [Quantitative result] | [Current] | [Goal] | [%] |
| **KR2**: [Quantitative result] | [Current] | [Goal] | [%] |
| **KR3**: [Quantitative result] | [Current] | [Goal] | [%] |

**Initiatives to achieve this objective**:
1. [Initiative/project] → Impacts KR[X]
2. [Initiative/project] → Impacts KR[X]

---

### Objective 2: [Qualitative goal statement]
*[Inspirational, memorable, time-bound goal]*

| Key Result | Baseline | Target | Confidence |
|------------|----------|--------|------------|
| **KR1**: [Quantitative result] | [Current] | [Goal] | [%] |
| **KR2**: [Quantitative result] | [Current] | [Goal] | [%] |
| **KR3**: [Quantitative result] | [Current] | [Goal] | [%] |

---

## Metrics by Wave

| Wave | Primary Metric | Target | Rationale |
|------|---------------|--------|-----------|
| **Wave 1** (Infrastructure) | [Technical metric] | [Target] | [Foundation validation] |
| **Wave 2** (Experience) | [UX metric] | [Target] | [User value validation] |
| **Wave 3+** (Business) | [Business metric] | [Target] | [Market validation] |

---

## Measurement Infrastructure

| Metric | Data Source | Collection Method | Dashboard |
|--------|-------------|-------------------|-----------|
| [Metric] | [Database/API/Tool] | [Automatic/Manual] | [Location] |
| [Metric] | [Database/API/Tool] | [Automatic/Manual] | [Location] |

### Metrics Not Yet Measurable
| Metric | Blocker | Resolution | ETA |
|--------|---------|------------|-----|
| [Metric] | [Why we can't measure] | [What we need to build] | [When] |

---

## Benchmark References

| Metric | Our Target | Industry Average | Top Quartile | Source |
|--------|------------|------------------|--------------|--------|
| [Metric] | [Target] | [Avg] | [Top 25%] | [Source] |
| [Metric] | [Target] | [Avg] | [Top 25%] | [Source] |

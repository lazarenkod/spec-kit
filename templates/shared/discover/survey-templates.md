# Survey Templates

## Purpose

Generate survey templates for quantitative validation of problem hypotheses, market sizing, and feature prioritization.

## Survey Types

### 1. Problem Validation Survey

**Use when**: Validating problem exists at scale after qualitative interviews
**Target responses**: 100-500
**Distribution**: Email list, social media, paid panels

```markdown
# [Problem Domain] Research Survey

## Screening (2 questions)

Q1. What best describes your role?
- [ ] [Role A - target persona]
- [ ] [Role B - target persona]
- [ ] [Role C - non-target]
- [ ] Other: ___
- [ ] None of the above (disqualify)

Q2. How often do you deal with [problem domain]?
- [ ] Daily
- [ ] Weekly
- [ ] Monthly
- [ ] Rarely
- [ ] Never (disqualify)

## Problem Severity (4 questions)

Q3. How much of a problem is [specific problem] for you?
- [ ] Critical problem - costs me significant time/money
- [ ] Moderate problem - causes regular frustration
- [ ] Minor problem - occasionally annoying
- [ ] Not a problem at all

Q4. How much time do you spend per week dealing with [problem]?
- [ ] Less than 1 hour
- [ ] 1-3 hours
- [ ] 3-5 hours
- [ ] 5-10 hours
- [ ] More than 10 hours

Q5. What impact does [problem] have on your work? (select all)
- [ ] Missed deadlines
- [ ] Quality issues
- [ ] Team frustration
- [ ] Customer complaints
- [ ] Revenue loss
- [ ] Other: ___

Q6. Have you actively looked for a solution in the past 6 months?
- [ ] Yes, actively searching now
- [ ] Yes, searched but stopped
- [ ] No, but thinking about it
- [ ] No, not a priority

## Current Solutions (3 questions)

Q7. What do you currently use to handle [problem]? (select all)
- [ ] [Competitor A]
- [ ] [Competitor B]
- [ ] Spreadsheets/manual process
- [ ] In-house built tool
- [ ] Nothing specific
- [ ] Other: ___

Q8. How satisfied are you with your current solution?
- [ ] Very satisfied
- [ ] Somewhat satisfied
- [ ] Neutral
- [ ] Somewhat dissatisfied
- [ ] Very dissatisfied

Q9. What's the biggest limitation of your current approach?
[Open text]

## Willingness to Pay (3 questions)

Q10. What do you currently spend on tools for [problem domain]?
- [ ] $0 (free tools only)
- [ ] $1-50/month
- [ ] $51-200/month
- [ ] $201-500/month
- [ ] $500+/month

Q11. If a tool could [value proposition], how much would you consider paying?
- [ ] Would not pay
- [ ] $1-25/month
- [ ] $26-50/month
- [ ] $51-100/month
- [ ] $100+/month

Q12. Who approves tool purchases in your organization?
- [ ] I can decide myself
- [ ] Need manager approval
- [ ] Requires department head approval
- [ ] Requires procurement/IT approval

## Follow-up (1 question)

Q13. Would you be interested in early access to a new solution?
- [ ] Yes, contact me (email: ___)
- [ ] Maybe later
- [ ] No thanks
```

### 2. Feature Prioritization Survey

**Use when**: Deciding what to build first
**Target responses**: 50-200 from target users
**Method**: MaxDiff or simple ranking

```markdown
# Feature Prioritization Survey

## Context
We're building [product] to help you [value proposition].
We want to build what matters most to you.

## MaxDiff Questions (5 rounds)

For each set, select the MOST important and LEAST important feature:

### Round 1
| Feature | Most Important | Least Important |
|---------|----------------|-----------------|
| [Feature A] | [ ] | [ ] |
| [Feature B] | [ ] | [ ] |
| [Feature C] | [ ] | [ ] |
| [Feature D] | [ ] | [ ] |

[Repeat for 5 rounds with different combinations]

## Open Questions

Q6. What feature would make this a "must-have" for you?
[Open text]

Q7. What would prevent you from using this product?
[Open text]

## Priority Ranking (Backup)

If MaxDiff not available, use simple ranking:

Rank these features from 1 (most important) to N (least important):
- [ ] Feature A: [Description]
- [ ] Feature B: [Description]
- [ ] Feature C: [Description]
- [ ] Feature D: [Description]
- [ ] Feature E: [Description]
```

### 3. Landing Page Smoke Test Survey

**Use when**: Testing value prop and positioning
**Target responses**: 200-1000 landing page visitors
**Method**: Embedded or exit survey

```markdown
# Quick Feedback Survey (30 seconds)

Shown after signup or to exiting visitors:

## For Signups

Q1. What convinced you to sign up? (select one)
- [ ] [Value prop A from headline]
- [ ] [Value prop B from subheadline]
- [ ] [Feature benefit C]
- [ ] The pricing
- [ ] A recommendation
- [ ] Other: ___

Q2. What problem are you hoping this will solve?
[Open text - 1 sentence]

Q3. How urgent is this problem for you?
- [ ] Need to solve it this week
- [ ] Need to solve it this month
- [ ] Looking for the future
- [ ] Just curious

## For Exit (No Signup)

Q1. What stopped you from signing up today?
- [ ] Not the right solution for me
- [ ] Pricing concerns
- [ ] Need to see it working first
- [ ] Need to check with my team
- [ ] Missing a specific feature: ___
- [ ] Other: ___

Q2. What would change your mind?
[Open text]
```

### 4. NPS / Satisfaction Survey

**Use when**: Measuring product-market fit post-launch
**Target responses**: All active users
**Frequency**: 30 days after activation, then quarterly

```markdown
# Quick Check-in

Q1. How likely are you to recommend [Product] to a colleague?

0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10
Not at all likely                    Extremely likely

Q2. Why did you give that score?
[Open text]

Q3. What's the ONE thing we could do to improve?
[Open text]

## Sean Ellis Test (Product-Market Fit)

Q4. How would you feel if you could no longer use [Product]?
- [ ] Very disappointed
- [ ] Somewhat disappointed
- [ ] Not disappointed (it's not really that useful)
- [ ] N/A - I no longer use it

Note: 40%+ "Very disappointed" indicates product-market fit
```

## Survey Best Practices

### Design Principles

1. **Keep it short**: 5-10 questions max for general surveys
2. **Screen aggressively**: Only target users who match your persona
3. **Randomize options**: Prevent order bias
4. **Include "Other"**: Capture unexpected responses
5. **Mix question types**: Rating, multiple choice, open text
6. **Mobile-first**: Many respondents on mobile devices

### Response Rate Optimization

| Tactic | Expected Lift |
|--------|---------------|
| Personalized subject line | +20-30% |
| Incentive ($5-25 gift card) | +50-100% |
| Promise to share results | +10-20% |
| Keep under 5 minutes | +30-40% |
| Send reminder after 3 days | +15-25% |

### Statistical Significance

```yaml
sample_size_calculator:
  base_rate: 0.10  # Expected response rate
  margin_of_error: 0.05  # ±5%
  confidence_level: 0.95  # 95%

  recommended_samples:
    problem_validation: 385  # For yes/no at 95% CI
    feature_ranking: 100     # For preference ordering
    maxdiff: 50-200         # Per feature set
    nps: 250                # For segment analysis
```

## Survey Analysis Template

```markdown
## Survey Results: [Survey Name]

### Response Summary
- Distributed to: N people
- Responses received: N (X% response rate)
- Completed: N (Y% completion rate)
- Qualified respondents: N

### Key Findings

#### Problem Validation
- X% rated problem as "Critical" or "Moderate"
- Top pain points: [List with %]
- Active solution seekers: X%

#### Current Solutions
| Solution | Usage % | Satisfaction |
|----------|---------|--------------|
| [Tool A] | X% | X.X/5 |

#### Willingness to Pay
- Would not pay: X%
- $1-25/month: X%
- $26-50/month: X%
- $50+/month: X%

**Price sensitivity indicator**: [High/Medium/Low]

### Statistical Notes
- Margin of error: ±X% at 95% confidence
- Significant findings (p < 0.05): [List]

### Recommended Actions
1. [Action based on data]
2. [Action based on data]

### Segments to Investigate
- [Segment A] showed significantly different responses
- [Segment B] has higher WTP - investigate further
```

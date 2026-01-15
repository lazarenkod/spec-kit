# Growth PM Cheat Sheet

**Quick Reference for Experimentation-First Product Development**

Print this and keep it at your desk. Use it before writing any spec or launching any experiment.

---

## The Growth PM Mindset

```
Traditional PM: "Let's build this feature"
Growth PM: "Let's test if this change moves our metric"

Traditional PM: "Feature is done when shipped"
Growth PM: "Feature is done when metric is proven to move"

Traditional PM: "Users will love this"
Growth PM: "Let's see if users actually use this"
```

---

## Before Writing Any Spec

### The 5 Critical Questions

1. **What metric are we moving?**
   - [ ] North Star metric defined
   - [ ] AARRR category identified (Acquisition/Activation/Retention/Referral/Revenue)
   - [ ] Baseline measured (current state)

2. **By how much?**
   - [ ] Target improvement specified (e.g., "+10%")
   - [ ] Minimum detectable effect (e.g., "≥5% to be worth it")
   - [ ] Statistical significance criteria (typically 95% confidence, p<0.05)

3. **Why do we believe this will work?**
   - [ ] User research evidence (qual: interviews, quant: analytics)
   - [ ] Hypothesis mechanism explained (how change → metric improvement)
   - [ ] Supporting data or competitor analysis

4. **How will we measure it?**
   - [ ] Event taxonomy defined
   - [ ] Tracking plan documented
   - [ ] Dashboard/tool identified

5. **What are our kill criteria?**
   - [ ] Failure conditions predetermined
   - [ ] Decision-maker identified
   - [ ] Timeline for decision gate (e.g., "Week 4 review")

**If you can't answer all 5, you're not ready to spec. Do more discovery.**

---

## Netflix's Hypothesis Template

Fill this out for every feature:

```
If we [CHANGE X],
then [METRIC Y] will improve by [Z%],
because [REASONING/MECHANISM].

Example:
If we show personalized recommendations above-the-fold,
then time-to-play will decrease by 15%,
because users will find relevant content faster without scrolling.
```

---

## Amplitude's 7% Retention Rule

**Critical Benchmark**: If you get just **7% of your original cohort to return on Day 7**, you've crossed into the **top 25%** for activation performance.

**Action**: For any new feature aimed at activation:
- [ ] Measure D7 retention for feature cohort
- [ ] Target: ≥7% (minimum) to top 10% (excellent: 15%+)
- [ ] If <7%: Kill or iterate immediately

Source: [Amplitude 2025 Product Benchmark Report](https://amplitude.com/blog/7-percent-retention-rule)

---

## Facebook's Activation Playbook

**Find Your Magic Number**: What action correlates with long-term retention?

Facebook's discovery: **7 friends in 10 days → 90%+ retention**

**How to find yours**:
1. Analyze retention cohorts by user behavior
2. Find correlation: Users who do X have Y% retention
3. Make THIS your activation metric
4. Optimize onboarding to get users to X faster

**Your magic number**:
- [ ] Action: _______________________________
- [ ] Timeframe: _____________________________
- [ ] Retention correlation: ___________________
- [ ] Current % reaching magic number: _________
- [ ] Target % reaching magic number: __________

---

## AARRR Quick Reference

For every spec, identify which pirate metric(s) you're affecting:

### Acquisition
- **Metric**: Cost per acquisition (CPA), Conversion rate (visitor → signup)
- **Question**: How do users discover us?
- **Tools**: Google Analytics, UTM tracking, attribution tools

### Activation
- **Metric**: Activation rate (signup → aha moment), Time to value
- **Question**: Do users have a great first experience?
- **Tools**: Funnel analysis, onboarding completion rate

### Retention
- **Metric**: D1/D7/D30 retention, Churn rate, DAU/MAU (stickiness)
- **Question**: Do users come back?
- **Tools**: Cohort analysis, retention curves

### Referral
- **Metric**: Viral coefficient (k-factor), Invites sent, Referral conversion
- **Question**: Do users tell others?
- **Tools**: Referral tracking, attribution

### Revenue
- **Metric**: ARPU, LTV, LTV/CAC ratio, Conversion rate (free → paid)
- **Question**: Do users pay?
- **Tools**: Subscription analytics, revenue cohorts

**Check**: Does this feature improve at least ONE of these? If not, why are we building it?

---

## Experiment Design Checklist

Before launching any A/B test:

### Setup
- [ ] **Hypothesis documented**: If [change], then [metric] by [%], because [reason]
- [ ] **Variants defined**: Control (current) vs Treatment(s)
- [ ] **Target audience**: Who sees this test (segment, geo, device)
- [ ] **Traffic allocation**: 50/50 or custom split
- [ ] **Sample size calculated**: Use power calculator (95% confidence, 80% power)
- [ ] **Duration planned**: Typically 2-4 weeks minimum

### Metrics
- [ ] **Primary metric**: The ONE metric that determines ship/kill
- [ ] **Secondary metrics**: Supporting indicators (2-3 max)
- [ ] **Guardrail/Counter metrics**: Metrics that must NOT degrade (e.g., quality, trust)

### Decision Framework
- [ ] **Success criteria**: Ship if [primary metric ≥X%, guardrails OK]
- [ ] **Kill criteria**: Kill if [metric degrades OR no movement after full sample]
- [ ] **Iterate criteria**: Directionally positive but below threshold

### Infrastructure
- [ ] **Feature flag configured**: Can turn on/off instantly
- [ ] **Events instrumented**: Tracking plan implemented
- [ ] **Dashboard live**: Real-time monitoring ready
- [ ] **Rollback plan**: Automated or manual process defined

**Don't launch until ALL boxes checked.**

---

## Success vs. Kill Criteria Template

Copy-paste this into every spec:

```markdown
## Success Criteria (Predetermined)

Ship to 100% if ALL of:
- [ ] [Primary metric] improves ≥[X%] (statistically significant, p<0.05)
- [ ] [Secondary metric 1] improves or stays neutral
- [ ] [Secondary metric 2] improves or stays neutral
- [ ] [Guardrail metric] does not degrade >[Y%]
- [ ] No critical bugs or user complaint spike (>10 tickets/day)

## Kill Criteria (Predetermined)

Kill feature if ANY of:
- [ ] [Primary metric] degrades >[X%] (95% confidence)
- [ ] [Guardrail metric] degrades >[Y%] (e.g., retention drops >5%)
- [ ] No movement in metrics after [Z weeks] at full sample size
- [ ] Technical issues affect >[N%] of users (e.g., >5% error rate)
- [ ] Support tickets exceed [M] per day (e.g., >10/day)

## Decision Timeline
- **Week 2**: Early signal review (20% of data)
- **Week 4**: Interim analysis (50% of data)
- **Week 6**: Final decision gate (100% of data)

**Decision-maker**: [PM name] + [Eng Lead] + [Data Lead]
**Escalation**: If kill criteria met but team wants to continue → [VP Product approval]
```

**Critical**: Set these BEFORE development starts, not after problems appear.

---

## Analytics Event Taxonomy

**Naming Convention**: `<feature>_<step>_<action>`

Examples:
- `onboarding_started`
- `onboarding_step1_completed`
- `onboarding_abandoned`
- `checkout_payment_clicked`
- `checkout_payment_failed`

**Standard Properties to Include**:
- `user_id` (required)
- `timestamp` (required)
- `session_id` (required)
- `device_type` (enum: mobile | desktop | tablet)
- `platform` (enum: ios | android | web)
- `user_tenure` (enum: new_0-30d | core_31-90d | power_90d+)
- `experiment_variant` (string, for A/B tests)

**Custom Properties**: Add feature-specific properties as needed

**Validation**:
- [ ] Events fire on correct triggers (tested)
- [ ] All required properties present (validated)
- [ ] No duplicate events (deduplication logic in place)
- [ ] Delivery rate >99% (monitored)

---

## Feature Flag Rollout Plan

**Standard Phases**:

| Phase | Audience | Duration | Purpose | Rollback if... |
|-------|----------|----------|---------|----------------|
| **0: Internal** | 0% prod (dev/QA only) | Week 1 | Validate feature works | Any bug |
| **1: Canary** | 5% of users | Week 2 | Early signal detection | Error rate >5% |
| **2: Beta** | 25% of users | Week 3 | Segment analysis | Primary metric degrades >10% |
| **3: Majority** | 75% of users | Week 4 | Validation before full | Kill criteria met |
| **4: Full** | 100% of users | Week 5+ | General availability | Major issue |

**Rollback Triggers** (automatic or manual):
- Error rate exceeds [X%] (e.g., 5%)
- Primary metric degrades >[Y%] (e.g., 10%)
- Latency increases >[Z%] (e.g., 50%)
- Support tickets spike (>[N] per day)

**Keep feature flag enabled for 30 days after 100% rollout for easy rollback.**

---

## Cohort Analysis Quick Reference

**Types of Cohorts**:
1. **Acquisition cohort**: Grouped by signup date (e.g., "Jan 2025 signups")
2. **Behavior cohort**: Grouped by action (e.g., "First purchase in Q1")
3. **Feature cohort**: Grouped by exposure (e.g., "Saw new onboarding")

**Standard Retention Table**:
```
Cohort      D0     D1    D7    D30   D60   D90
──────────────────────────────────────────────
Jan 2025   100%   [%]   [%]   [%]   [%]   [%]
Feb 2025   100%   [%]   [%]   [%]   [%]   [%]
Mar 2025   100%   [%]   [%]   [%]   [%]   —
```

**What to Look For**:
- **Improving over time?**: Feb > Jan = product improvements working
- **Flattening curve?**: Retention stabilizing by D90 = core retained users found
- **D7 benchmark**: ≥7% = top 25% of products (Amplitude)
- **Leaky bucket**: Retention keeps dropping, never flattens = fundamental product issue

**Alert if**: Any cohort's D7 retention drops >10% vs. prior period

---

## Funnel Optimization Framework

**Standard E-commerce Funnel**:
1. Product page view → 100%
2. Add to cart → 30%
3. Checkout initiated → 20%
4. Payment info entered → 15%
5. Purchase complete → 12%

**Analysis**:
- **Biggest drop**: Where is the largest % drop-off?
- **Target that step**: Focus optimization efforts there first
- **Measure time**: How long between steps? Long gaps = friction

**Optimization Tactics by Step**:
- **Awareness → Interest**: Improve messaging, value prop clarity
- **Interest → Action**: Reduce friction, simplify form, improve trust signals
- **Action → Complete**: Remove distractions, optimize load time, fix bugs

---

## Viral Coefficient (k-factor) Calculator

**Formula**: k = (Invites sent per user) × (Conversion rate)

**Example**:
- Average user sends 3 invites
- 40% of invites convert to signups
- k = 3 × 0.4 = **1.2** (VIRAL GROWTH!)

**Thresholds**:
- **k > 1.0**: Viral growth (each user brings >1 new user)
- **k = 0.5-1.0**: Strong referral contribution, but need paid acquisition too
- **k < 0.5**: Weak viral loop, fix or deprioritize

**Optimization Levers**:
1. **Increase invites sent**: Make sharing frictionless, incentivize
2. **Increase conversion rate**: Better incentives, clearer messaging
3. **Decrease time to invite**: Trigger sharing at high-value moments

**Current viral coefficient**: _________
**Target viral coefficient**: _________
**Path to k>1.0**: _________

---

## User Research → Spec Requirements

**Process**:
1. **Conduct research**: Interviews (qual) + Analytics (quant)
2. **Identify patterns**: ≥3 mentions = pattern
3. **Prioritize**: High frequency + High impact = High priority
4. **Derive requirement**: Pattern → Spec requirement (REQ-XXX)

**Template**:
```markdown
### Finding: [Title]
**Source**: [User interviews N=12]
**Evidence**: "[Quote from user]" — User #7
**Frequency**: [9/12 participants mentioned this]
**Impact**: [Business/user impact - e.g., "77% drop off"]

**Spec Requirement**:
→ [REQ-001]: [Specific, testable requirement]
```

**Don't spec without research. Opinions don't ship features. Data does.**

---

## Feedback Loop Types

| Method | Frequency | Sample Size | Purpose |
|--------|-----------|-------------|---------|
| **In-app survey** (NPS/CES) | Weekly | 100+/week | Quantitative sentiment |
| **User interviews** | Bi-weekly | 5-10/session | Qualitative depth |
| **Support tickets** | Weekly review | All tickets | Pain point detection |
| **Session recordings** | Weekly | 50/week | Behavior observation |
| **Analytics** | Daily | All users | Quantitative behavior |

**Synthesis Cadence**: Weekly review → Identify patterns (≥3 sources) → Create experiment backlog

**Close the loop**: Email users when their feedback is implemented

---

## LTV/CAC Ratio Quick Check

**Formula**: LTV (Lifetime Value) / CAC (Customer Acquisition Cost)

**Thresholds**:
- **>3:1**: Healthy (for every $1 spent acquiring, you make $3+)
- **1:1 to 3:1**: Needs improvement (low margin)
- **<1:1**: Broken unit economics (losing money on each customer)

**Improvement Levers**:
- **Increase LTV**: Improve retention (reduces churn), Upsell/cross-sell, Pricing optimization
- **Decrease CAC**: Referral programs (viral loops), SEO/organic, Conversion rate optimization

**Your numbers**:
- LTV: $_______
- CAC: $_______
- Ratio: _______
- **Action**: _______________________________

---

## Top 10 Growth PM Commandments

1. **Thou shalt not ship without hypothesis** - Every feature is a testable hypothesis
2. **Thou shalt set kill criteria early** - Before development starts, not after
3. **Thou shalt A/B test big changes** - Feature flags + gradual rollout = standard
4. **Thou shalt instrument everything** - Analytics is not optional
5. **Thou shalt follow the data** - Opinions start, data decides
6. **Thou shalt measure retention** - Activation without retention is vanity
7. **Thou shalt close feedback loops** - User research is continuous, not one-time
8. **Thou shalt know thy North Star** - Every feature ties to company metric
9. **Thou shalt optimize for learning** - Fast iterations > perfect launches
10. **Thou shalt kill bad ideas fast** - Sunk cost fallacy kills companies

---

## Tools & Resources

### Analytics
- **Amplitude** / **Mixpanel**: User behavior, cohort analysis, funnels
- **Google Analytics 4**: Traffic, acquisition sources
- **Segment**: Event routing layer
- **Looker** / **Tableau**: Custom dashboards

### Experimentation
- **LaunchDarkly** / **Split.io**: Feature flags
- **Optimizely** / **VWO**: A/B testing
- **Statsig** / **GrowthBook**: Open-source alternatives

### Feedback
- **Hotjar** / **Qualaroo**: In-app surveys
- **FullStory** / **LogRocket**: Session recordings
- **Dovetail** / **Productboard**: User research synthesis

### Sample Size Calculators
- [Evan Miller A/B Test Calculator](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely Sample Size Calculator](https://www.optimizely.com/sample-size-calculator/)

### Further Reading
- Netflix Tech Blog: [Experimentation Platform](https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15)
- Amplitude: [7% Retention Rule](https://amplitude.com/blog/7-percent-retention-rule)
- Reforge: [Growth Series](https://www.reforge.com/growth-series)

---

## Daily Workflow Checklist

**Before writing a spec**:
- [ ] Metric identified (North Star or AARRR)
- [ ] Baseline measured (current state)
- [ ] Hypothesis formed (If X, then Y by Z%, because...)
- [ ] User research reviewed (qual + quant)
- [ ] Success criteria defined
- [ ] Kill criteria defined

**Before launching an experiment**:
- [ ] Feature flag configured
- [ ] Events instrumented and validated
- [ ] Dashboard live
- [ ] Sample size calculated
- [ ] Rollback plan ready
- [ ] Team aligned on decision framework

**After experiment completes**:
- [ ] Results analyzed (primary + secondary + guardrail metrics)
- [ ] Statistical significance checked (p<0.05)
- [ ] Decision made (Ship / Iterate / Kill)
- [ ] Learnings documented in spec
- [ ] Next experiment planned (if iterating)

**Weekly review**:
- [ ] Cohort retention trends reviewed
- [ ] User feedback synthesized
- [ ] Experiment backlog prioritized
- [ ] Metrics dashboard checked for anomalies

---

**Last Updated**: 2026-01-01
**Maintained by**: Spec Kit Team
**Print this and keep it visible while working!**

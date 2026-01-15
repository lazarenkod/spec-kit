# Growth-Focused Specification Patterns

**World-Class Templates for Experimentation-First Product Development**

This document provides actionable templates and patterns for writing growth-optimized product specifications based on practices from Netflix, Facebook, Amplitude, and leading growth teams in 2025.

---

## Table of Contents

1. [Experimentation-First Specifications](#1-experimentation-first-specifications)
2. [Growth Metrics in Specs](#2-growth-metrics-in-specs)
3. [Data-Driven Specification](#3-data-driven-specification)
4. [Iterative Specification](#4-iterative-specification)
5. [User Research Integration](#5-user-research-integration)
6. [Complete Templates](#6-complete-templates)

---

## 1. Experimentation-First Specifications

### 1.1 Netflix's Hypothesis-Driven Approach

**Pattern**: Turn every feature idea into a testable hypothesis with measurable outcomes.

**Template Structure**:

```markdown
## Hypothesis

**Statement**: If we make [CHANGE X], it will improve the member experience in a way that makes [METRIC Y] improve by [Z%].

**Example**: If we show members the Top 10 trending content, it will help them find something to watch faster, increasing member joy and reducing time-to-play by 15%.

### Rationale
- **Why this change**: [Context and user pain point]
- **Expected mechanism**: [How the change should work]
- **Supporting evidence**: [User research, competitor analysis, or data insights]

### Success Metrics
- **Primary metric**: [North Star impact - e.g., retention, engagement]
- **Secondary metrics**: [Supporting indicators - e.g., time-to-value, activation]
- **Counter metrics**: [Guardrails - e.g., quality, trust & safety]

### Experiment Design
- **Target population**: [Who will see this - e.g., "New users in first 7 days"]
- **Allocation method**:
  - [ ] Real-time allocation (dynamic, based on user behavior)
  - [ ] Batch allocation (fixed cohort)
- **Variants**:
  - **Control**: [Current experience]
  - **Treatment A**: [Primary variant]
  - **Treatment B** (optional): [Alternative approach]
- **Sample size**: [Required users per variant for statistical significance]
- **Duration**: [Run time - typically 2-4 weeks]
- **Statistical criteria**:
  - Confidence level: 95%
  - Minimum detectable effect: [e.g., 5% relative lift]
  - p-value threshold: < 0.05

### Kill Criteria (Predetermined)
This experiment will be STOPPED if any of the following occur:
- [ ] Primary metric shows **>5% negative impact** (95% confidence)
- [ ] Counter metric degrades by **>10%** (e.g., user complaints spike)
- [ ] No movement in metrics after **full sample size reached**
- [ ] Technical issues affect **>5% of users** in treatment

### Decision Framework
- **Ship to 100%**: Primary metric improves ≥[X%], no counter-metric degradation
- **Iterate**: Directionally positive but below threshold
- **Kill**: Negative impact or no movement after full test duration
```

**Key Insight from Netflix**: [Netflix's experimentation platform](https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15) requires that "all product ideas are subjected to the scientific method, with actual data supporting changes before changes are rolled out to all users."

---

### 1.2 Heterogeneous Treatment Effects (Advanced)

For mature products, specify how effects might vary across segments.

```markdown
## Segment-Specific Hypotheses

We expect treatment effects to vary by:

### By Device Type
- **Mobile**: Hypothesis: [Expected behavior and metric impact]
- **Desktop**: Hypothesis: [Expected behavior and metric impact]
- **TV**: Hypothesis: [Expected behavior and metric impact]

### By User Tenure
- **New users (D0-D30)**: [Expected impact and reasoning]
- **Core users (D31-D90)**: [Expected impact and reasoning]
- **Power users (D90+)**: [Expected impact and reasoning]

### Analysis Plan
- Run heterogeneous treatment effect (HTE) analysis
- Report posterior probability of null hypothesis by segment
- Alert developers to genuine problems vs. false positives
```

**Reference**: [Netflix's 2025 Heterogeneous Treatment Effects approach](https://netflixtechblog.medium.com/heterogeneous-treatment-effects-at-netflix-da5c3dd58833)

---

## 2. Growth Metrics in Specs

### 2.1 AARRR Framework Integration

Every growth feature spec should address relevant pirate metrics.

**Template**:

```markdown
## Growth Impact Analysis

### Acquisition Metrics
**Relevant?**: [ ] Yes / [ ] No

If yes:
- **Target CAC reduction**: [X%] (from $[current] to $[target])
- **Traffic source impact**: [Which channels this affects]
- **Conversion rate goal**: [Current] → [Target]
- **Tracking requirements**:
  - UTM parameters: [list]
  - Attribution window: [days]
  - Source/medium/campaign taxonomy

### Activation Metrics
**Relevant?**: [ ] Yes / [ ] No

If yes:
- **Activation definition**: [e.g., "User completes 3 core actions in first session"]
- **Current activation rate**: [X%]
- **Target activation rate**: [Y%] (uplift: [Z%])
- **Time to aha moment**:
  - Current: [X minutes/actions]
  - Target: [Y minutes/actions]
- **Aha moment definition**: [Specific user experience that demonstrates value]

**Example (Facebook's 7 in 10)**: Users adding 7+ friends in first 10 days → 90%+ retention
**Example (Slack)**: Teams sending 2,000+ messages → 93% retention

### Retention Metrics
**Relevant?**: [ ] Yes / [ ] No

If yes:
- **Current retention curve**:
  - D1: [X%]
  - D7: [X%]
  - D30: [X%]
  - D90: [X%]
- **Target retention improvements**:
  - D1: [+Xpp] (percentage points)
  - D7: [+Xpp]
  - D30: [+Xpp]
- **Critical threshold**: [e.g., "7% D7 retention" per Amplitude benchmark]
- **Cohort analysis plan**: [Weekly/monthly cohorts to track]

**The 7% Rule**: [Amplitude's 2025 research](https://amplitude.com/blog/7-percent-retention-rule) shows that achieving 7% D7 retention puts you in the top 25% of products.

### Referral/Viral Metrics
**Relevant?**: [ ] Yes / [ ] No

If yes:
- **Viral coefficient (k-factor)**:
  - Current: [X] (invites/user × conversion rate)
  - Target: [Y]
  - Path to k>1.0: [Strategy]
- **Invitation mechanics**:
  - Invites sent per user: [Current] → [Target]
  - Invite conversion rate: [Current] → [Target]
  - Sharing friction points: [List and solutions]
- **Incentive structure**:
  - Referrer reward: [What they get and when]
  - Referee reward: [What they get and when]
  - **Two-sided?**: [ ] Yes / [ ] No (Uber/Dropbox pattern)

### Revenue Metrics
**Relevant?**: [ ] Yes / [ ] No

If yes:
- **Free-to-paid conversion**: [Current] → [Target]
- **ARPU impact**: [Current] → [Target]
- **LTV/CAC ratio**: [Current] → [Target] (healthy = >3:1)
- **Monetization trigger**: [When/how do users encounter paywall]
```

---

### 2.2 North Star Metric Alignment

**Template**:

```markdown
## North Star Metric Impact

**Company North Star**: [e.g., "Nights Booked" (Airbnb), "Messages Sent by Teams" (Slack)]

### Direct Impact
This feature [increases/decreases/neutral] the North Star by:
- **Mechanism**: [How this feature influences the North Star]
- **Expected magnitude**: [X% change in North Star]
- **Time horizon**: [When we expect to see impact]

### Input Metrics (North Star Drivers)
This feature primarily affects:
- [Input metric 1]: [How and by how much]
- [Input metric 2]: [How and by how much]

### North Star Tree Position
```
North Star: [Company metric]
  ↓
Input Metric: [Category this feature affects]
  ↓
Feature Metric: [Specific metric for this feature]
  ↓
Work Stream: [Initiative name]
```

**Example (Airbnb)**:
```
North Star: Nights Booked
  ↓
Input Metric: Supply Growth (New Listings)
  ↓
Feature Metric: Host Activation Rate
  ↓
Work Stream: Professional Photography Program
```
```

---

## 3. Data-Driven Specification

### 3.1 Analytics Instrumentation Requirements

Based on [Amplitude's 5-step analytics instrumentation guide](https://amplitude.com/blog/analytics-instrumentation).

**Template**:

```markdown
## Analytics & Instrumentation

### Event Taxonomy

**Naming Convention**: `<feature_name>_<step/subpage>_<action>`

#### Events to Track

| Event Name | Description | Trigger | Properties | Owner |
|------------|-------------|---------|------------|-------|
| `feature_name_viewed` | User views feature entry point | Page load | `source`, `device_type`, `user_tenure` | [Team] |
| `feature_name_step1_clicked` | User clicks primary CTA | Click | `button_variant`, `position` | [Team] |
| `feature_name_step1_completed` | User completes step 1 | Action completion | `time_to_complete`, `method` | [Team] |
| `feature_name_abandoned` | User exits without completing | Exit | `exit_point`, `time_spent` | [Team] |

#### Event Properties (Standard)

**User Properties** (who):
- `user_id` (string, required)
- `user_tenure` (enum: new_0-30d | core_31-90d | power_90d+)
- `subscription_tier` (enum: free | premium | enterprise)
- `device_type` (enum: mobile | desktop | tablet | tv)
- `platform` (enum: ios | android | web)

**Event Properties** (what/how):
- `timestamp` (datetime, required)
- `session_id` (string, required)
- `source` (enum: organic | referral | paid | direct)
- `variant` (string, for A/B tests)

#### User Actions (Custom Properties)

For this feature, also track:
- [Custom property 1]: [Type, description, values]
- [Custom property 2]: [Type, description, values]

### Tracking Plan

**Repository**: [Link to GitHub/Notion tracking plan repo]

**Implementation Process**:
1. [ ] Add events to tracking plan (this spec)
2. [ ] Create Jira ticket for instrumentation
3. [ ] Implement tracking (backend/frontend)
4. [ ] Validate in dev environment
5. [ ] QA verification checklist:
   - [ ] Events fire on correct triggers
   - [ ] All required properties present
   - [ ] Property values match spec
   - [ ] No duplicate events
6. [ ] Monitor in production (first 48 hours)

### Analytics Tools Integration
- [ ] **Amplitude/Mixpanel**: User behavior and cohort analysis
- [ ] **Google Analytics 4**: Traffic and acquisition sources
- [ ] **Custom Dashboard**: [Link to feature-specific dashboard]

### Data Quality Requirements
- **Event delivery**: >99% of events successfully recorded
- **Property completeness**: >95% of events have all required properties
- **Validation period**: 7 days post-launch
- **Owner**: [Analytics team member]
```

**Key Reference**: [Mixpanel's Tracking Plan Best Practices](https://docs.mixpanel.com/docs/tracking-best-practices/tracking-plan)

---

### 3.2 Cohort Analysis Specifications

Based on [2025 cohort analysis best practices](https://www.sarasanalytics.com/glossary/cohort-analysis).

**Template**:

```markdown
## Cohort Analysis Requirements

### Cohort Definitions

#### Acquisition Cohorts
Group users by **first interaction date** (signup/install):
- **Cohort key**: `signup_date`
- **Time buckets**: Weekly (for fast-moving products) or Monthly
- **Segments to analyze**:
  - By acquisition channel: organic, paid, referral, direct
  - By device type: mobile, desktop, tablet
  - By geography: [key markets]

#### Behavior Cohorts
Group users by **specific action completion**:
- **Cohort key**: `first_[action]_date`
- **Key behaviors**:
  - First purchase
  - First [core feature use]
  - Activation milestone reached

#### Feature Cohorts
Group users by **exposure to this feature**:
- **Cohort key**: `feature_exposure_date`
- **Variants**: Control vs Treatment A vs Treatment B

### Retention Analysis Specifications

**Retention Curve Requirements**:
```
Cohort      D0     D1    D7    D30   D60   D90
─────────────────────────────────────────────────
Jan 2025   100%   [%]   [%]   [%]   [%]   [%]
Feb 2025   100%   [%]   [%]   [%]   [%]   [%]
Mar 2025   100%   [%]   [%]   [%]   [%]   [%]
```

**Analysis Plan**:
1. **Weekly review**: D1, D7 trends across recent cohorts
2. **Monthly review**: D30, D90 trends, cohort quality comparison
3. **Alerts**: Flag if any cohort's D7 retention drops >10% vs. prior period

### Key Metrics by Cohort

For each cohort, track:
- **Retention rate**: % still active at D1, D7, D30, D90
- **Activation rate**: % reaching activation milestone
- **Time to activation**: Median time from signup to activation
- **Feature adoption**: % using core features
- **LTV**: Cumulative revenue per cohort member

### Data Requirements
- [ ] Tracking: `user_cohort_key` property on all events
- [ ] Minimum data freshness: 24 hours
- [ ] Historical data: 90 days minimum
- [ ] Tool: [Amplitude/Mixpanel/Custom]

### Dashboard Requirements
- [ ] Cohort retention heatmap (weekly/monthly view)
- [ ] Cohort comparison charts (overlay curves)
- [ ] Segment drill-downs (by channel, device, geo)
- [ ] Export capability for detailed analysis
```

---

### 3.3 Funnel Analysis Specifications

**Template**:

```markdown
## Funnel Analysis

### Funnel Definition

**Goal**: [End conversion action - e.g., "Complete purchase", "Activate account"]

**Steps**:
1. **[Step 1 Name]**: [Trigger event] → [Expected %]
2. **[Step 2 Name]**: [Trigger event] → [Expected %]
3. **[Step 3 Name]**: [Trigger event] → [Expected %]
4. **[Goal]**: [Trigger event] → [Expected %]

**Example (SaaS Onboarding)**:
1. Sign up form view → 100%
2. Email verified → 70%
3. Profile completed → 50%
4. First core action → 30%
5. Activated (aha moment) → 20%

### Drop-Off Analysis

**For each step, identify**:
- **Current drop-off rate**: [%]
- **Target drop-off rate**: [%]
- **Hypothesized friction points**: [List]
- **Mitigation strategies**: [List]

### Time-to-Convert Specifications

Track time between funnel steps:
- **Median time to complete full funnel**: [Current] → [Target]
- **Step-by-step timing**:
  - Step 1 → Step 2: [Median time]
  - Step 2 → Step 3: [Median time]
- **Abandonment windows**: Flag users who spend >[X] time on step

### Segment Comparisons

Analyze funnel conversion by:
- Acquisition source: [Which channels convert best?]
- Device type: [Mobile vs desktop differences?]
- User type: [New vs returning?]

### Experiment Impact on Funnel

This feature affects:
- [Step X]: Expected improvement: [%]
- [Step Y]: Expected improvement: [%]
- **Overall funnel conversion**: [Current %] → [Target %]
```

---

## 4. Iterative Specification

### 4.1 MVP Scoping with Kill Criteria

Based on [2025 MVP specification best practices](https://www.f22labs.com/blogs/mvp-specification-document-2025-complete-software-requirement-specification/) and [kill criteria frameworks](https://medium.com/@rajeshdutta/kill-criteria-the-uncomfortable-pill-to-swallow-for-product-managers-5f130b3a28a5).

**Template**:

```markdown
## MVP Definition & Scope

### Core Value Proposition
**User need**: [Job to be done]
**Minimum viable solution**: [Simplest way to address need]
**Out of scope for MVP**: [Features deferred to V2+]

### MVP Success Criteria (Predetermined)

**These must be set BEFORE development begins.**

#### Activation Success
- [ ] **≥[X%] of users** reach activation milestone within [Y days]
- [ ] **Median time to aha moment**: ≤[X minutes]

#### Retention Success
- [ ] **D7 retention**: ≥[X%] (minimum: 7% per Amplitude benchmark)
- [ ] **D30 retention**: ≥[X%]

#### Engagement Success
- [ ] **DAU/MAU ratio**: ≥[X%] (stickiness)
- [ ] **Sessions per user per week**: ≥[X]

#### Business Success
- [ ] **Conversion rate** (free to paid): ≥[X%]
- [ ] **CAC payback period**: ≤[X months]

### MVP Kill Criteria (Predetermined)

**This MVP will be DISCONTINUED if:**

#### Activation Failures
- [ ] **<[X%] activation rate** after 4 weeks with ≥[N] signups
- [ ] **Median time to aha moment >[X minutes]** (too much friction)

#### Retention Failures
- [ ] **D7 retention <[X%]** for 3 consecutive weekly cohorts
- [ ] **D30 retention <[X%]** for 2 consecutive monthly cohorts
- [ ] **Retention curve shows no flattening** by D30 (leaky bucket)

#### Engagement Failures
- [ ] **<[X%] of activated users** return in Week 2
- [ ] **Average session duration <[X minutes]** (insufficient value)

#### Business Failures
- [ ] **CAC exceeds LTV** after 6 months (unit economics broken)
- [ ] **Feature adoption <[X%]** of target user segment

#### Technical Failures
- [ ] **System downtime >[X%]** (reliability issues)
- [ ] **Load time >[X seconds]** (performance issues)

#### Timeline Failure
- [ ] **No statistically significant improvement** in primary metric after [X weeks]

### Kill Criteria Review Process
1. **Week 2**: Early signals review (activation, time-to-value)
2. **Week 4**: Retention review (D7, D30 cohorts)
3. **Week 8**: Full evaluation vs. success/kill criteria
4. **Decision gate**: Ship to 100% / Iterate / Kill

**Decision-maker**: [PM + Engineering Lead + Data Lead]
**Escalation path**: If kill criteria met but team wants to continue → [VP Product approval required]
```

**Key Insight**: [Kill criteria should be set during discovery](https://medium.com/@rajeshdutta/kill-criteria-the-uncomfortable-pill-to-swallow-for-product-managers-5f130b3a28a5), not after problems emerge. This removes emotion from shutdown decisions.

---

### 4.2 Feature Flags & Gradual Rollout

Based on [2025 feature flag best practices](https://www.featbit.co/articles2025/feature-flag-api-strategies-2025).

**Template**:

```markdown
## Feature Flag Strategy

### Flag Configuration

**Flag name**: `feature_[name]_enabled`
**Flag type**: [ ] Boolean / [ ] Multivariate / [ ] Percentage rollout

### Rollout Plan

#### Phase 0: Internal Testing (Week 1)
- **Audience**: Engineering team + QA (N=[X])
- **Percentage**: 0% of production users
- **Validation**:
  - [ ] Feature works as expected
  - [ ] Analytics events firing correctly
  - [ ] No performance degradation
  - [ ] Error rate <0.1%

#### Phase 1: Canary Release (Week 2)
- **Audience**: 5% of users, randomly selected
- **Duration**: 7 days
- **Success criteria**:
  - [ ] Error rate <1%
  - [ ] No customer support spike (baseline +10%)
  - [ ] Primary metric: [expected trend]
- **Rollback triggers**:
  - Error rate >5%
  - Customer complaints >10 in 24h
  - Primary metric degrades >10%

#### Phase 2: Expanded Beta (Week 3)
- **Audience**: 25% of users
- **Duration**: 7 days
- **Segments**:
  - 10% new users (D0-D30)
  - 10% core users (D31-D90)
  - 5% power users (D90+)
- **Success criteria**: Same as Phase 1
- **Analysis**: Segment-specific metrics

#### Phase 3: Majority Rollout (Week 4)
- **Audience**: 75% of users
- **Duration**: 7 days
- **Holdback group**: Maintain 25% control group
- **Purpose**: Long-term A/B test for validation

#### Phase 4: Full Release (Week 5)
- **Audience**: 100% of users
- **Condition**: All success criteria met in Phase 3
- **Feature flag**: Keep enabled for 30 days for easy rollback

### Targeting Rules

**Include**:
- [ ] User segments: [List]
- [ ] Geographies: [List]
- [ ] Device types: [List]

**Exclude**:
- [ ] VIP/beta users: [Yes/No]
- [ ] High-value accounts: [Yes/No]
- [ ] Specific organizations: [List]

### Rollback Plan

**Automatic rollback if**:
- Error rate exceeds [X%]
- Latency increases >[X%]
- Primary metric degrades >[X%]

**Manual rollback process**:
1. Toggle flag to 0% via [tool]
2. Notify stakeholders in #[channel]
3. Investigate root cause
4. Document incident in [location]

### Feature Flag Cleanup

**Planned removal date**: [Date - typically 30 days post-100% rollout]
**Cleanup process**:
1. [ ] Confirm feature at 100% for 30+ days
2. [ ] Remove flag from codebase
3. [ ] Archive flag in [tool]
4. [ ] Update documentation
```

---

### 4.3 Iterative Learning Framework

**Template**:

```markdown
## Learning & Iteration Plan

### Build-Measure-Learn Cycles

#### Cycle 1: MVP Launch (Weeks 1-2)
**Build**: [Core feature set]
**Measure**:
- Activation rate
- Time to aha moment
- Initial retention (D1, D7)
**Learn**:
- Does the feature solve the problem?
- Where do users get stuck?
- What's working well?
**Decide**: Ship to more users / Iterate / Kill

#### Cycle 2: Optimization (Weeks 3-4)
**Build**: [Based on Cycle 1 learnings]
**Measure**: [Same metrics + any new hypotheses]
**Learn**: [Expected insights]
**Decide**: [Decision gate]

### Experiment Backlog

Based on initial learnings, plan to test:

| Hypothesis | Expected Impact | Effort | Priority |
|------------|----------------|--------|----------|
| [Hypothesis 1] | [Metric +X%] | S/M/L | High/Med/Low |
| [Hypothesis 2] | [Metric +X%] | S/M/L | High/Med/Low |

### Continuous Improvement Metrics

Track week-over-week improvements:
- **Activation rate delta**: [Trend]
- **Retention improvement**: [Trend]
- **Feature adoption**: [Trend]

### Pivot Criteria

We will consider a MAJOR PIVOT if:
- [ ] Kill criteria approached after 2 iteration cycles
- [ ] User feedback reveals fundamentally different need
- [ ] Competitor launches superior solution
- [ ] Market dynamics shift significantly
```

---

## 5. User Research Integration

### 5.1 Research Findings → Spec Requirements

Based on [2025 customer feedback loop best practices](https://getthematic.com/insights/building-effective-user-feedback-loops-for-continuous-improvement).

**Template**:

```markdown
## User Research Foundation

### Research Summary

**Research methods used**:
- [ ] User interviews (N=[X], date: [YYYY-MM])
- [ ] Surveys (N=[X], date: [YYYY-MM])
- [ ] Usability testing (N=[X], date: [YYYY-MM])
- [ ] Support ticket analysis ([X] tickets over [Y] months)
- [ ] Session recordings ([X] sessions analyzed)
- [ ] Behavioral analytics (from [tool], date range: [X])

### Key Findings

#### Finding 1: [Title]
**Source**: [Research method]
**Evidence**: [Quote/data point]
**User segment**: [Who experiences this]
**Frequency**: [How common - e.g., "73% of users", "Top 3 support issue"]
**Impact**: [Business/user impact]

**Spec requirement derived**:
→ Requirement ID [REQ-001]: [Specific requirement]

#### Finding 2: [Title]
**Source**: [Research method]
**Evidence**: [Quote/data point]
**User segment**: [Who experiences this]
**Frequency**: [How common]
**Impact**: [Business/user impact]

**Spec requirement derived**:
→ Requirement ID [REQ-002]: [Specific requirement]

### Jobs to Be Done (JTBD)

**Primary job**:
> When [situation], I want to [motivation], so I can [expected outcome].

**Current alternatives**: [How users solve this today]
**Limitations of alternatives**: [Why current solutions fail]
**Our solution**: [How this feature addresses JTBD]

### User Personas Affected

#### Persona 1: [Name/Role]
- **Goals**: [What they want to achieve]
- **Pain points**: [Specific to this feature]
- **Expected behavior**: [How they'll use the feature]
- **Success criteria**: [What success looks like for them]

### Feedback Loop Integration

**During Development**:
- [ ] Week 2: Prototype testing with [N] users from research pool
- [ ] Week 4: Usability test of alpha version ([N] users)

**Post-Launch**:
- [ ] Week 1: In-app survey (NPS + feature satisfaction)
- [ ] Week 2: User interviews ([N] early adopters)
- [ ] Week 4: Support ticket analysis (feature-related issues)
- [ ] Ongoing: Feedback widget in feature UI

**Feedback channels**:
- In-app feedback widget
- Customer support tickets (tagged: [tag])
- User interview requests (incentive: [X])
- Email surveys (trigger: Day 7 post-activation)
```

---

### 5.2 Quantitative + Qualitative Integration

**Template**:

```markdown
## Mixed-Methods Research Integration

### Quantitative Foundation

**Analytics data** (past [X] months):
- **Metric 1**: [Current value, trend]
- **Metric 2**: [Current value, trend]
- **Problem identified**: [What data shows is broken]

**Example**:
- **Activation rate**: 23% (target: 35%)
- **Median time to aha moment**: 47 minutes (target: <15 minutes)
- **Problem**: 77% of users not reaching activation milestone

### Qualitative Depth

**User interviews** (N=[X]):
> "When I first signed up, I had no idea what to do next. I just closed the tab."
> — User #7, D1 churned user

**Synthesis**:
- **Theme 1**: Onboarding confusion (mentioned by [X/Y] participants)
- **Theme 2**: [Theme]

### Hypothesis Formation

**Quantitative insight**: [What the data shows]
**Qualitative insight**: [Why it's happening per users]
**Hypothesis**: [Combined hypothesis]

**Example**:
- **Quant**: 77% don't activate (drop off after signup)
- **Qual**: "No idea what to do next" (onboarding confusion)
- **Hypothesis**: If we add guided onboarding, activation rate will increase from 23% to 35%

### Validation Plan

**Before build**:
- [ ] Prototype test with [N] users
- [ ] Measure comprehension and usability

**After launch**:
- [ ] Quantitative: Activation rate trend
- [ ] Qualitative: Post-activation interviews (N=[X])
- [ ] Synthesis: Does quant improvement match qual feedback?
```

---

### 5.3 Continuous Feedback Integration

**Template**:

```markdown
## Feedback Loop Specifications

### Collection Methods

#### 1. In-App Feedback
- **Trigger**: [When users see the prompt - e.g., "After completing onboarding"]
- **Question**: [e.g., "How easy was it to get started?" (CES - Customer Effort Score)]
- **Scale**: [e.g., 1-7, very difficult to very easy]
- **Follow-up**: Open text for scores ≤3
- **Volume target**: [X] responses per week

#### 2. Support Ticket Analysis
- **Tag**: `feature:[name]`
- **Review cadence**: Weekly
- **Metrics**:
  - Volume of tickets (trend)
  - Top issues (categorized)
  - Resolution time
- **Alert threshold**: >10 tickets/week = investigate

#### 3. Session Recordings
- **Tool**: [Fullstory/Hotjar/etc.]
- **Sample**: 50 sessions per week (25 activated, 25 not activated)
- **Analysis**: Identify friction points in user flow

#### 4. User Interviews
- **Cadence**: Bi-weekly (N=5 per session)
- **Participant criteria**:
  - 2 activated users
  - 2 non-activated users
  - 1 churned user
- **Incentive**: [Gift card value]
- **Owner**: [PM/UXR]

### Synthesis & Action

**Weekly feedback review**:
1. Aggregate data from all sources
2. Identify patterns (3+ mentions = pattern)
3. Prioritize: High frequency + High impact
4. Create experiment backlog items
5. Update spec with new learnings

**Feedback → Spec Update Process**:
- [ ] Feedback identified
- [ ] Pattern confirmed (≥3 sources)
- [ ] Hypothesis formed
- [ ] Experiment designed
- [ ] Spec updated with new requirement
- [ ] Backlog prioritized

### Metrics Dashboard

**Feedback health metrics**:
- **Response rate**: [X%] (target: >20%)
- **NPS**: [score] (target: >50)
- **CES** (Customer Effort Score): [score] (target: <3 on 1-7 scale)
- **Feature satisfaction**: [X/5 stars]

### Closing the Loop

**Communicate back to users**:
- [ ] Email update: "We heard you and built [X]"
- [ ] In-app announcement of improvements
- [ ] Changelog updates
- [ ] User who reported issue gets personal thank you
```

**Key Insight**: [96% of customers who describe an interaction as "high effort" become disloyal](https://qualaroo.com/blog/how-to-build-feedback-into-your-products-lifecycle/). Measuring and acting on Customer Effort Score is critical.

---

## 6. Complete Templates

### 6.1 Growth Feature Specification (Full Template)

```markdown
# Feature Specification: [Feature Name]

**Author**: [Name]
**Date**: [YYYY-MM-DD]
**Status**: [Draft / In Review / Approved / In Development]
**Version**: [0.1]

---

## 1. Hypothesis & Rationale

### Hypothesis Statement
**If we** [CHANGE], **then** [METRIC] will improve by [X%], **because** [REASONING].

**Example**: If we add personalized onboarding based on user role, then activation rate will improve from 23% to 35%, because users will immediately see relevant features for their job-to-be-done.

### Rationale
**User problem**: [Description]
**Current state**: [How users solve this today]
**Limitations**: [Why current solution fails]
**Our solution**: [How we'll solve it]

### Supporting Evidence
- **User research**: [Finding from interviews/surveys]
- **Analytics**: [Data supporting the problem]
- **Market**: [Competitor insights or trends]

---

## 2. Growth Impact Analysis

### North Star Metric Alignment
**Company North Star**: [e.g., "Weekly Active Teams" (Slack)]
**This feature impacts**: [Direct/Indirect]
**Mechanism**: [How it affects North Star]
**Expected magnitude**: [X% improvement over Y weeks]

### AARRR Metrics

#### Acquisition
- [ ] Not applicable
- [ ] Relevant
  - **Current CAC**: $[X]
  - **Target CAC**: $[X]
  - **Conversion rate**: [X%] → [Y%]

#### Activation
- [ ] Not applicable
- [x] Relevant
  - **Activation definition**: [e.g., "Complete 3 core actions in first session"]
  - **Current rate**: [X%]
  - **Target rate**: [Y%]
  - **Time to aha moment**: [X min] → [Y min]

#### Retention
- [ ] Not applicable
- [x] Relevant
  - **D7 retention**: [X%] → [Y%] (target: >7% per Amplitude)
  - **D30 retention**: [X%] → [Y%]

#### Referral
- [ ] Not applicable
- [ ] Relevant
  - **Viral coefficient (k)**: [X] → [Y]
  - **Invites sent/user**: [X] → [Y]

#### Revenue
- [ ] Not applicable
- [ ] Relevant
  - **Conversion rate**: [X%] → [Y%]
  - **ARPU**: $[X] → $[Y]
  - **LTV/CAC**: [X] → [Y]

---

## 3. User Research Foundation

### Research Summary
**Methods**: [Interviews (N=X), Surveys (N=Y), Analytics from Z tool]
**Date range**: [YYYY-MM to YYYY-MM]

### Key Findings
1. **[Finding]**: [Evidence + impact]
   → Requirement: [REQ-001]
2. **[Finding]**: [Evidence + impact]
   → Requirement: [REQ-002]

### Jobs to Be Done
> When [situation], I want to [motivation], so I can [outcome].

---

## 4. Experiment Design

### Target Population
**Who**: [e.g., "New users in first 7 days, US market, mobile devices"]
**Size**: [X users expected over test duration]

### Variants
- **Control**: [Current experience]
- **Treatment A**: [Primary variant]
- **Treatment B** (optional): [Alternative approach]

### Allocation
- [ ] Real-time (dynamic based on behavior)
- [x] Batch (fixed cohort)
- **Traffic split**: 50/50 (Control/Treatment) or 33/33/33

### Sample Size & Duration
- **Minimum sample**: [X] users per variant
- **Duration**: [Y] weeks
- **Confidence level**: 95%
- **Minimum detectable effect**: [Z%]

### Success Metrics
**Primary**: [Metric] improves by [X%]
**Secondary**:
- [Metric 1]: [Expected direction]
- [Metric 2]: [Expected direction]
**Counter/Guardrail**:
- [Metric]: No degradation >5%

---

## 5. Analytics & Instrumentation

### Event Taxonomy

| Event Name | Trigger | Properties | Owner |
|------------|---------|------------|-------|
| `feature_viewed` | Page load | `source`, `device_type` | [Team] |
| `feature_step1_completed` | Action | `time_to_complete` | [Team] |
| `feature_completed` | Goal | `completion_time`, `path` | [Team] |

### Cohort Analysis Plan
**Cohorts**:
- Acquisition cohort (by signup week)
- Feature exposure cohort (Control vs Treatment)

**Metrics by cohort**:
- Activation rate
- D7/D30 retention
- Feature adoption rate

### Funnel Analysis
**Steps**:
1. View feature → 100%
2. Start interaction → [X%]
3. Complete step 1 → [Y%]
4. Complete goal → [Z%]

**Target**: Overall funnel conversion [Current] → [Target]

---

## 6. MVP & Iteration Plan

### MVP Scope
**Core features**:
- [Feature 1]
- [Feature 2]

**Out of scope for V1**:
- [Feature deferred to V2]

### Success Criteria (Predetermined)
- [ ] Activation rate ≥[X%]
- [ ] D7 retention ≥7% (Amplitude benchmark)
- [ ] Time to aha moment ≤[X] minutes

### Kill Criteria (Predetermined)
**Kill if**:
- [ ] Activation rate <[X%] after 4 weeks
- [ ] D7 retention <[X%] for 3 consecutive weekly cohorts
- [ ] No metric movement after full sample size

### Decision Framework
- **Ship to 100%**: All success criteria met
- **Iterate**: Directionally positive, needs optimization
- **Kill**: Kill criteria met

---

## 7. Feature Flag & Rollout Plan

### Rollout Phases
- **Phase 0**: Internal (0% prod users, Week 1)
- **Phase 1**: Canary (5%, Week 2)
- **Phase 2**: Beta (25%, Week 3)
- **Phase 3**: Majority (75%, Week 4)
- **Phase 4**: Full (100%, Week 5)

### Rollback Triggers
- Error rate >5%
- Primary metric degrades >10%
- Support tickets >10/day

---

## 8. Feedback Loop

### Collection Methods
- [ ] In-app survey (CES, NPS)
- [ ] User interviews (N=5 bi-weekly)
- [ ] Support ticket analysis
- [ ] Session recordings

### Synthesis Cadence
- **Weekly**: Review feedback, identify patterns
- **Bi-weekly**: User interviews
- **Monthly**: Update spec with learnings

---

## 9. Requirements

### Functional Requirements
**[REQ-001]**: [Requirement derived from user research]
**[REQ-002]**: [Requirement]

### Non-Functional Requirements
**Performance**: [e.g., "Page load <2s"]
**Accessibility**: [WCAG 2.1 AA compliance]
**Analytics**: [All events firing correctly]

---

## 10. Success Summary

**This feature is successful if**:
- [Primary metric] improves by ≥[X%]
- [Secondary metric 1] improves or stays neutral
- [Secondary metric 2] improves or stays neutral
- No degradation in [counter metrics]
- User feedback is positive (NPS >50, CES <3)

**Timeline to success**: [X] weeks post-launch

---

## Appendix

### Research Artifacts
- [Link to interview notes]
- [Link to survey results]
- [Link to analytics dashboard]

### Design Mocks
- [Link to Figma]

### Tracking Plan
- [Link to event taxonomy repo]
```

---

### 6.2 Rapid Experiment Spec (Lightweight Template)

For fast-moving tests, use this lightweight version:

```markdown
# Experiment: [Name]

**Owner**: [PM]
**Date**: [YYYY-MM-DD]
**Status**: [Planning / Running / Complete]

---

## Hypothesis
If [CHANGE], then [METRIC] will improve by [X%].

## Why Now?
[Quick context: problem + evidence]

## Experiment Design
- **Audience**: [Who]
- **Duration**: [Weeks]
- **Variants**: Control vs Treatment
- **Traffic**: 50/50
- **Sample size**: [N] per variant

## Metrics
- **Primary**: [Metric + target]
- **Guardrails**: [Metrics that must not degrade]

## Kill Criteria
- [ ] [Condition 1]
- [ ] [Condition 2]

## Instrumentation
Events:
- `[event_name]`: [trigger]

## Decision
- **Ship if**: Primary metric ≥[X%] improvement
- **Kill if**: Kill criteria met
- **Iterate if**: Directional but below threshold

## Results
[After experiment completes]
- **Primary metric**: [Result]
- **Decision**: [Ship/Kill/Iterate]
- **Learnings**: [Key insights]
```

---

## Summary: What Makes Growth Specs World-Class

### 1. **Hypothesis-Driven**
Every feature is a testable hypothesis with clear success/failure criteria BEFORE building.

### 2. **Metrics-First**
Growth specs start with metrics (North Star, AARRR), not features. Metrics drive requirements.

### 3. **Experimentation-Integrated**
A/B testing, feature flags, and gradual rollouts are specified upfront, not added later.

### 4. **Kill Criteria**
Predetermined conditions for killing features remove emotion and prevent sunk cost fallacy.

### 5. **Instrumentation = First-Class**
Analytics tracking is as important as feature code. Event taxonomy is part of spec.

### 6. **User Research → Requirements**
Specs are grounded in real user research (qual + quant), not opinions.

### 7. **Iterative by Design**
MVP → Measure → Learn → Iterate cycles are planned from the start.

### 8. **Feedback Loops**
Continuous user feedback collection and synthesis is built into the process.

---

## References & Further Reading

### Netflix Experimentation
- [Netflix Experimentation Platform](https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15)
- [Heterogeneous Treatment Effects at Netflix](https://netflixtechblog.medium.com/heterogeneous-treatment-effects-at-netflix-da5c3dd58833)

### Growth Metrics
- [Product-Led Growth Metrics](https://www.productled.org/foundations/product-led-growth-metrics)
- [The 7% Retention Rule - Amplitude](https://amplitude.com/blog/7-percent-retention-rule)
- [PLG Metrics: Activation & Retention - Statsig](https://www.statsig.com/perspectives/plg-metrics-activation-retention)

### Analytics & Instrumentation
- [Analytics Instrumentation Guide - Amplitude](https://amplitude.com/blog/analytics-instrumentation)
- [Tracking Plan Best Practices - Mixpanel](https://docs.mixpanel.com/docs/tracking-best-practices/tracking-plan)
- [Event Tracking Spec Guide](https://medium.com/@disvianas/event-tracking-spec-in-product-analytics-bridging-the-gap-between-business-metrics-and-technical-9b6b0f2b8785)

### Experimentation Best Practices
- [Feature Experimentation Best Practices - Flagship](https://www.flagship.io/experimentation-best-practices/)
- [What to Test in Product Experiments - Statsig](https://www.statsig.com/perspectives/test-product-experiments-framework)

### MVP & Feature Flags
- [MVP Specification Document 2025](https://www.f22labs.com/blogs/mvp-specification-document-2025-complete-software-requirement-specification/)
- [Feature Flag System Design 2025](https://www.featbit.co/articles2025/feature-flag-system-design-2025)

### User Research & Feedback
- [Building Effective User Feedback Loops](https://getthematic.com/insights/building-effective-user-feedback-loops-for-continuous-improvement)
- [Customer Feedback Loop Guide](https://getthematic.com/insights/customer-feedback-loop-guide)
- [Master Product Feedback in 2025](https://qualaroo.com/blog/how-to-build-feedback-into-your-products-lifecycle/)

### Kill Criteria
- [Kill Criteria for Product Managers](https://medium.com/@rajeshdutta/kill-criteria-the-uncomfortable-pill-to-swallow-for-product-managers-5f130b3a28a5)
- [Why Failure Criteria is Essential - Terem](https://terem.tech/why-failure-criteria-is-essential-for-product-success/)

---

**Last Updated**: 2026-01-01
**Maintained by**: Spec Kit Team
**Feedback**: [How to contribute improvements to these templates]

# Growth Integration Guide

**How to Integrate Growth-Focused Patterns into Spec Kit Workflow**

This guide shows how to adapt Spec Kit's templates and commands to support experimentation-first, metrics-driven product development based on practices from Netflix, Facebook, Amplitude, and leading growth teams.

---

## Table of Contents

1. [Overview: Growth-Optimized SDD](#overview-growth-optimized-sdd)
2. [Template Enhancements](#template-enhancements)
3. [Command Workflow Adjustments](#command-workflow-adjustments)
4. [Example: Growth Feature Walkthrough](#example-growth-feature-walkthrough)
5. [Integration with Existing Tools](#integration-with-existing-tools)

---

## Overview: Growth-Optimized SDD

### Traditional SDD vs. Growth SDD

| Aspect | Traditional SDD | Growth SDD |
|--------|----------------|------------|
| **Starting point** | Requirements | Hypothesis + metrics |
| **Success criteria** | Features shipped | Metrics moved |
| **Build approach** | Full feature first | MVP → test → iterate |
| **Decision gate** | Stakeholder approval | Data (success/kill criteria) |
| **User research** | Before spec (one-time) | Continuous feedback loop |
| **Analytics** | Added after launch | Specified with feature |

### Key Principle
> "Specs should specify WHAT metrics to move and WHY, not just WHAT features to build."

---

## Template Enhancements

### 1. Enhanced `spec-template.md`

Add these sections to the standard spec template:

```markdown
# Feature Specification: [Name]

[... existing sections ...]

---

## Hypothesis & Growth Impact

### Hypothesis Statement
**If we** [CHANGE], **then** [METRIC] will improve by [X%], **because** [REASONING].

### North Star Alignment
- **Company North Star**: [e.g., "Weekly Active Teams"]
- **Impact mechanism**: [How this feature affects North Star]
- **Expected magnitude**: [X% over Y weeks]

### AARRR Impact
Check all that apply and specify targets:

- [ ] **Acquisition**: [Metric] from [Current] to [Target]
- [ ] **Activation**: [Metric] from [Current] to [Target]
- [ ] **Retention**: D7 from [X%] to [Y%], D30 from [A%] to [B%]
- [ ] **Referral**: Viral coefficient from [X] to [Y]
- [ ] **Revenue**: [Metric] from [Current] to [Target]

---

## User Research Foundation

### Research Summary
**Methods**: [Interviews N=X, Surveys N=Y, Analytics from Z]
**Date**: [YYYY-MM]

### Key Findings → Requirements
1. **[Finding]**: [Evidence]
   - **Impact**: [Frequency + severity]
   - **Spec Requirement**: [REQ-001]: [Derived requirement]

### Jobs to Be Done
> When [situation], I want to [motivation], so I can [outcome].

**Current alternatives**: [How users solve this now]
**Why they fail**: [Limitations]

---

## Experiment Design

### Experiment Setup
- **Target audience**: [Segment]
- **Sample size**: [N] per variant (95% confidence)
- **Duration**: [X] weeks
- **Variants**:
  - Control: [Current experience]
  - Treatment: [New experience]

### Metrics
- **Primary**: [Metric + target improvement]
- **Secondary**: [Supporting metrics]
- **Guardrails**: [Metrics that must not degrade]

### Statistical Criteria
- **Confidence level**: 95%
- **p-value threshold**: <0.05
- **Minimum detectable effect**: [X%]

---

## Success & Kill Criteria

### Success Criteria (Predetermined)
Ship to 100% if ALL of:
- [ ] [Primary metric] improves ≥[X%] (statistically significant)
- [ ] [Secondary metric 1] improves or neutral
- [ ] [Guardrail metrics] no degradation >[Y%]
- [ ] No critical bugs or user complaints spike

### Kill Criteria (Predetermined)
Kill feature if ANY of:
- [ ] [Primary metric] degrades >[X%] (95% confidence)
- [ ] [Critical guardrail] degrades >[Y%] (e.g., retention drops >5%)
- [ ] No movement in metrics after [Z] weeks at full sample size
- [ ] Technical issues affect >[N%] of users
- [ ] Support tickets >[M] per day

### Decision Timeline
- **Week 2**: Early signal review
- **Week 4**: Interim analysis (50% of data)
- **Week 6**: Final decision gate

**Decision-maker**: [PM + Eng Lead + Data Lead]

---

## Analytics & Instrumentation

### Event Taxonomy

**Naming convention**: `<feature>_<step>_<action>`

| Event Name | Trigger | Properties | Owner |
|------------|---------|------------|-------|
| `[feature]_viewed` | User sees feature | `source`, `device_type`, `user_tenure` | [Team] |
| `[feature]_started` | User begins interaction | `entry_point` | [Team] |
| `[feature]_completed` | User finishes goal | `completion_time`, `path` | [Team] |
| `[feature]_abandoned` | User exits early | `exit_point`, `time_spent` | [Team] |

### Cohort Analysis Requirements
**Cohorts to track**:
- Acquisition cohort (by signup week)
- Feature exposure cohort (Control vs Treatment)
- Behavior cohort (activated vs not)

**Metrics per cohort**:
- Activation rate
- D1, D7, D30 retention
- Feature adoption rate

### Funnel Specification
**Goal**: [End action]
**Steps**:
1. [Step 1] → [Expected %]
2. [Step 2] → [Expected %]
3. [Step 3] → [Expected %]
4. [Goal] → [Expected %]

**Target**: Overall conversion from [X%] to [Y%]

### Tracking Plan Link
[Link to tracking plan repo/doc]

---

## MVP & Iteration Plan

### MVP Scope
**In scope**:
- [Core feature 1]
- [Core feature 2]

**Out of scope** (V2+):
- [Deferred feature]

### Learning Cycles

**Cycle 1: MVP (Weeks 1-2)**
- Build: [MVP features]
- Measure: [Key metrics]
- Learn: [Expected insights]
- Decide: Ship more / Iterate / Kill

**Cycle 2: Optimization (Weeks 3-4)**
- Build: [Based on learnings]
- Measure: [Same + new metrics]
- Learn: [Expected insights]
- Decide: [Next step]

---

## Feature Flag & Rollout

### Rollout Phases
- **Phase 0**: Internal (0% prod, Week 1) - QA validation
- **Phase 1**: Canary (5%, Week 2) - Early signal
- **Phase 2**: Beta (25%, Week 3) - Segment analysis
- **Phase 3**: Majority (75%, Week 4) - Validation
- **Phase 4**: Full (100%, Week 5) - General availability

### Rollback Plan
**Automatic rollback if**:
- Error rate >[X%]
- Primary metric degrades >[Y%]

**Manual rollback process**:
1. Set feature flag to 0%
2. Notify team in [#slack-channel]
3. Root cause analysis
4. Document in [location]

---

## Feedback Loop

### Collection Methods
- [ ] In-app survey (NPS, CES) - Week 1 post-activation
- [ ] User interviews - Bi-weekly, N=5
- [ ] Support ticket analysis - Weekly review
- [ ] Session recordings - 50/week

### Synthesis Cadence
- **Weekly**: Review feedback, identify patterns
- **Bi-weekly**: Conduct user interviews
- **Monthly**: Update spec with learnings, prioritize experiments

### Feedback → Action Process
1. Feedback collected from multiple sources
2. Pattern identified (≥3 mentions)
3. Hypothesis formed
4. Experiment spec'd
5. Backlog prioritized

---

[... rest of spec template ...]
```

---

### 2. Enhanced `plan-template.md`

Add experimentation and instrumentation sections:

```markdown
# Implementation Plan: [Feature Name]

[... existing sections ...]

---

## Experimentation Infrastructure

### Feature Flag Implementation
**Flag name**: `feature_[name]_enabled`
**Flag service**: [LaunchDarkly / Split / Custom]

**Targeting rules**:
- User segment: [Criteria]
- Geography: [Restrictions if any]
- Device type: [Restrictions if any]

**Rollout schedule**:
- Phase 1 (5%): [Date]
- Phase 2 (25%): [Date]
- Phase 3 (75%): [Date]
- Phase 4 (100%): [Date]

### Variant Assignment Logic
```python
# Pseudocode
if feature_flag_enabled(user_id, "feature_name"):
    variant = get_experiment_variant(user_id, experiment_id)
    if variant == "treatment":
        # New experience
    else:
        # Control (current experience)
```

---

## Analytics Implementation

### Event Instrumentation

**Backend events**:
| Event | Trigger | Properties | Endpoint |
|-------|---------|------------|----------|
| `feature_viewed` | API call to /feature | `user_id`, `device_type` | POST /analytics/track |

**Frontend events**:
| Event | Trigger | Properties | Tool |
|-------|---------|------------|------|
| `feature_button_clicked` | Click handler | `button_id`, `position` | Segment/Amplitude |

### Implementation checklist
- [ ] Add event tracking code
- [ ] Validate events fire in dev environment
- [ ] Test all properties present and correct
- [ ] QA in staging
- [ ] Monitor first 48h in production

### Dashboard Setup
- [ ] Create feature dashboard in [Amplitude/Mixpanel]
- [ ] Add key metrics charts:
  - Funnel conversion
  - Cohort retention
  - Metric trends (treatment vs control)
- [ ] Set up alerts for anomalies

---

## Data Quality Requirements

### Pre-Launch Validation
- [ ] Event schema documented in tracking plan
- [ ] Events fire on correct triggers (unit tested)
- [ ] All properties present (integration tested)
- [ ] No duplicate events (deduplication logic in place)
- [ ] Latency <100ms (performance tested)

### Post-Launch Monitoring
- [ ] Event delivery rate >99%
- [ ] Property completeness >95%
- [ ] No schema drift (validated weekly)

---

[... rest of plan template ...]
```

---

### 3. Enhanced `tasks-template.md`

Add analytics and experimentation tasks:

```markdown
# Task Breakdown: [Feature Name]

[... existing sections ...]

---

## Analytics & Instrumentation Tasks

### A1: Event Schema Definition
**Description**: Define all events, properties, and tracking plan
**Deliverable**: Tracking plan document in [repo/tool]
**Acceptance**:
- [ ] Event taxonomy follows naming convention
- [ ] All properties documented (name, type, values)
- [ ] Reviewed by analytics team

**Effort**: [X hours]
**Dependencies**: None
**Owner**: [PM]

---

### A2: Backend Event Implementation
**Description**: Implement server-side event tracking
**Deliverable**: Events firing from backend services
**Acceptance**:
- [ ] Events implemented per tracking plan
- [ ] Unit tests cover event triggers
- [ ] Properties validated (type, completeness)
- [ ] Integration tested in staging

**Effort**: [X hours]
**Dependencies**: A1
**Owner**: [Backend Engineer]

---

### A3: Frontend Event Implementation
**Description**: Implement client-side event tracking
**Deliverable**: Events firing from UI interactions
**Acceptance**:
- [ ] Events implemented per tracking plan
- [ ] Click handlers instrumented
- [ ] Session tracking working
- [ ] Cross-browser tested

**Effort**: [X hours]
**Dependencies**: A1
**Owner**: [Frontend Engineer]

---

### A4: Dashboard Creation
**Description**: Build analytics dashboard for experiment monitoring
**Deliverable**: Dashboard in [Amplitude/Mixpanel/Looker]
**Acceptance**:
- [ ] Key metrics charts (funnel, retention, trends)
- [ ] Cohort comparison views (treatment vs control)
- [ ] Filters by segment (device, geo, tenure)
- [ ] Shared with team

**Effort**: [X hours]
**Dependencies**: A2, A3
**Owner**: [Data Analyst]

---

## Experimentation Tasks

### E1: Feature Flag Setup
**Description**: Configure feature flag in [tool]
**Deliverable**: Flag configured and testable
**Acceptance**:
- [ ] Flag created with correct name
- [ ] Targeting rules configured
- [ ] Rollout schedule set
- [ ] Tested in dev environment

**Effort**: [X hours]
**Dependencies**: None
**Owner**: [Engineer]

---

### E2: Experiment Configuration
**Description**: Set up A/B test in experimentation platform
**Deliverable**: Experiment live in [tool]
**Acceptance**:
- [ ] Experiment ID generated
- [ ] Traffic allocation set (50/50 or custom)
- [ ] Sample size calculated
- [ ] Metrics configured (primary, secondary, guardrails)
- [ ] Reviewed by data team

**Effort**: [X hours]
**Dependencies**: E1, A1
**Owner**: [PM + Data]

---

### E3: Variant Assignment Logic
**Description**: Implement code to assign users to variants
**Deliverable**: Users consistently bucketed into control/treatment
**Acceptance**:
- [ ] Assignment logic implemented
- [ ] Consistent across sessions (same user = same variant)
- [ ] Logged for analysis
- [ ] Tested with multiple users

**Effort**: [X hours]
**Dependencies**: E1, E2
**Owner**: [Engineer]

---

### E4: Rollback Plan Implementation
**Description**: Build automated rollback triggers
**Deliverable**: Monitoring + auto-rollback if criteria met
**Acceptance**:
- [ ] Error rate monitoring in place
- [ ] Metric degradation alerts configured
- [ ] Auto-rollback script tested
- [ ] Manual rollback procedure documented

**Effort**: [X hours]
**Dependencies**: E1
**Owner**: [DevOps + Engineer]

---

[... rest of tasks ...]
```

---

## Command Workflow Adjustments

### Updated Workflow with Growth Focus

```
/speckit.constitution
    ↓
/speckit.concept (optional, for large products 50+ requirements)
    ↓
/speckit.specify (WITH hypothesis + metrics + experiment design)
    ↓
/speckit.clarify (optional, includes metrics clarifications)
    ↓
/speckit.baseline (optional, for brownfield - includes current metrics)
    ↓
/speckit.plan (includes analytics + feature flag implementation)
    ↓
/speckit.tasks (includes instrumentation + experimentation tasks)
    ↓
/speckit.implement
    ↓
[EXPERIMENT RUNS]
    ↓
/speckit.analyze-experiment (NEW - analyze results, make decision)
    ↓
[Decision: Ship / Iterate / Kill]
    ↓
/speckit.analyze (post-implementation QA)
    ↓
/speckit.merge (if shipping to 100%)
```

---

### New Command: `/speckit.analyze-experiment`

**Purpose**: Analyze experiment results and make data-driven decision

**Prompt Template**:

```markdown
You are analyzing the results of an A/B test experiment.

## Context
- **Feature**: [Name]
- **Hypothesis**: [Statement]
- **Experiment duration**: [X weeks]
- **Sample size**: [N per variant]

## Experiment Results

### Primary Metric
- **Metric**: [Name]
- **Control**: [Value]
- **Treatment**: [Value]
- **Lift**: [X%]
- **Statistical significance**: p-value = [Y], confidence interval = [A, B]

### Secondary Metrics
- **[Metric 1]**: Control [X], Treatment [Y], Lift [Z%]
- **[Metric 2]**: Control [X], Treatment [Y], Lift [Z%]

### Guardrail Metrics
- **[Metric 1]**: [No degradation / Degraded by X%]
- **[Metric 2]**: [No degradation / Degraded by X%]

### Segment Analysis
**By device type**:
- Mobile: [Lift]
- Desktop: [Lift]

**By user tenure**:
- New (D0-D30): [Lift]
- Core (D31-D90): [Lift]
- Power (D90+): [Lift]

## Decision Framework (from spec)

**Ship to 100%** if:
- [x] Primary metric improves ≥[X%] (statistically significant)
- [ ] No guardrail degradation >[Y%]

**Kill** if:
- [ ] Primary metric degrades
- [ ] Kill criteria met

**Iterate** if:
- [ ] Directionally positive but below threshold

## Your Task

1. **Analyze the results**: Evaluate if success criteria met
2. **Check for segments**: Are there segments where it works better/worse?
3. **Recommend decision**: Ship / Iterate / Kill
4. **If iterate**: What should we test next?
5. **Update spec**: Document learnings in spec file

## Output

Generate:
1. **Experiment Analysis Report** (experiment-results.md)
2. **Updated Spec** with learnings section
3. **Next Steps** (if iterating, create new experiment spec)
```

---

## Example: Growth Feature Walkthrough

Let's walk through building a **personalized onboarding feature** with growth-optimized Spec Kit.

---

### Step 1: `/speckit.constitution`

Define growth principles:

```markdown
## Growth Principles

1. **Metrics-Driven**: Every feature must have a measurable hypothesis
2. **Experimentation First**: All major changes are A/B tested before full rollout
3. **Kill Criteria**: We set predetermined failure criteria to avoid sunk cost fallacy
4. **Continuous Learning**: User feedback loops integrated into every feature
5. **North Star Focus**: All work ties back to our North Star metric: [Weekly Active Users]
```

---

### Step 2: `/speckit.specify`

Create hypothesis-driven spec:

```markdown
# Feature Specification: Personalized Onboarding

## Hypothesis & Growth Impact

### Hypothesis Statement
**If we** show personalized onboarding based on user role (Designer vs Developer),
**then** activation rate will improve from 23% to 35%,
**because** users will immediately see relevant features for their job-to-be-done.

### North Star Alignment
- **Company North Star**: Weekly Active Users
- **Impact mechanism**: Higher activation → higher retention → more WAU
- **Expected magnitude**: +5% WAU over 8 weeks

### AARRR Impact
- [x] **Activation**: From 23% to 35% (+12pp)
  - Activation = User completes 3 core actions in first session
  - Time to aha moment: 47 min → 15 min
- [x] **Retention**: D7 from 18% to 25% (+7pp) via better activation

## User Research Foundation

### Research Summary
**Methods**: User interviews (N=12), Session recordings (N=50), Support tickets (N=143)
**Date**: 2025-11

### Key Findings → Requirements
1. **"No idea what to do next"** - 9/12 interviewees mentioned confusion post-signup
   - **Impact**: 77% drop off without activating
   - **Spec Requirement**: [REQ-001]: Provide clear next steps immediately after signup

2. **Role-specific needs** - Designers want templates, Developers want API docs
   - **Impact**: Users who find role-relevant feature in first session have 3x activation
   - **Spec Requirement**: [REQ-002]: Ask user role during signup, show role-specific onboarding

### Jobs to Be Done
> When I sign up for a new tool, I want to quickly see how it helps MY specific role, so I can decide if it's worth my time to set up.

## Experiment Design

### Experiment Setup
- **Target audience**: New signups (first 7 days), all geos, all devices
- **Sample size**: 2,000 per variant (95% confidence, 80% power)
- **Duration**: 4 weeks (estimate 1,000 signups/week)
- **Variants**:
  - **Control**: Current generic onboarding
  - **Treatment**: Role-based personalized onboarding

### Metrics
- **Primary**: Activation rate (23% → 35%)
- **Secondary**:
  - Time to aha moment (47 min → <20 min)
  - First-session feature adoption (+20%)
- **Guardrails**:
  - Signup completion rate (no degradation >5%)
  - Time spent in onboarding (<5 min avg)

## Success & Kill Criteria

### Success Criteria
Ship to 100% if ALL of:
- [x] Activation rate ≥32% (>9pp lift, statistically significant p<0.05)
- [x] Time to aha moment ≤20 min
- [x] Signup completion rate no degradation >5%

### Kill Criteria
Kill if ANY of:
- [ ] Activation rate <25% (no meaningful improvement)
- [ ] Signup completion rate drops >10% (too much friction)
- [ ] No movement after 4 weeks at full sample

## Analytics & Instrumentation

### Event Taxonomy

| Event Name | Trigger | Properties |
|------------|---------|------------|
| `onboarding_started` | Signup complete | `user_id`, `device_type` |
| `onboarding_role_selected` | User picks role | `role` (designer/developer) |
| `onboarding_step_completed` | Step done | `step_number`, `time_to_complete` |
| `onboarding_completed` | All steps done | `total_time`, `steps_completed` |
| `onboarding_abandoned` | User exits | `exit_step`, `time_spent` |
| `activation_milestone_reached` | 3 actions done | `actions_list`, `time_since_signup` |

### Cohort Analysis
**Cohorts**:
- Acquisition: By signup week
- Experiment: Control vs Treatment
- Role: Designer vs Developer (for treatment group)

**Metrics per cohort**:
- Activation rate
- D1, D7, D30 retention
- Time to aha moment

### Funnel
1. Signup complete → 100%
2. Role selected → 90%
3. Step 1 complete → 70%
4. Step 2 complete → 50%
5. Onboarding complete → 40%
6. Activation (3 actions) → 35%

## Feature Flag & Rollout

### Rollout Phases
- **Phase 0**: Internal QA (Week 1)
- **Phase 1**: 5% canary (Week 2)
- **Phase 2**: 25% beta (Week 3)
- **Phase 3**: 75% majority (Week 4)
- **Phase 4**: 100% full (Week 5)

[... rest of spec ...]
```

---

### Step 3: `/speckit.plan`

Plan includes analytics implementation:

```markdown
# Implementation Plan: Personalized Onboarding

[... architecture, data model, API design ...]

## Experimentation Infrastructure

### Feature Flag
**Flag name**: `personalized_onboarding_enabled`
**Service**: LaunchDarkly
**Targeting**: Random 50% of new signups (Control vs Treatment)

### Variant Assignment
```javascript
// On signup complete
const variant = getExperimentVariant(userId, "personalized_onboarding_exp");
if (variant === "treatment") {
  showRoleSelectionModal();
} else {
  showGenericOnboarding();
}
```

## Analytics Implementation

### Backend Events
- POST /api/onboarding/start → Track `onboarding_started`
- POST /api/onboarding/role → Track `onboarding_role_selected`

### Frontend Events
- User clicks "Complete step" → Track `onboarding_step_completed`
- User closes onboarding → Track `onboarding_abandoned`

### Dashboard
Create in Amplitude:
- Funnel: Signup → Role Select → Steps → Activation
- Cohort retention: Treatment vs Control
- Metric trends: Daily activation rate by variant

[... rest of plan ...]
```

---

### Step 4: `/speckit.tasks`

Tasks include instrumentation:

```markdown
# Task Breakdown: Personalized Onboarding

## Phase 1: Analytics & Experimentation

### A1: Event Schema Definition ✅
**Deliverable**: Tracking plan in Notion
**Owner**: PM
**Effort**: 2h

### A2: Backend Event Tracking ⏳
**Deliverable**: Events firing from API
**Owner**: Backend Engineer
**Effort**: 4h
**Dependencies**: A1

### E1: Feature Flag Setup ⏳
**Deliverable**: Flag in LaunchDarkly
**Owner**: Engineer
**Effort**: 2h

## Phase 2: Feature Development

[... feature tasks ...]

## Phase 3: QA & Launch

### Q1: Analytics QA
**Deliverable**: All events validated
**Acceptance**:
- [x] Events fire on triggers
- [x] Properties correct
- [x] Dashboard live
**Owner**: QA + PM
**Effort**: 4h
```

---

### Step 5: `/speckit.implement`

Implement with tracking:

```javascript
// Frontend: Role selection
function handleRoleSelection(role) {
  // Track event
  analytics.track('onboarding_role_selected', {
    role: role,
    user_id: currentUser.id,
    device_type: getDeviceType()
  });

  // Show role-specific onboarding
  if (role === 'designer') {
    showDesignerOnboarding();
  } else {
    showDeveloperOnboarding();
  }
}
```

---

### Step 6: Run Experiment (4 weeks)

Monitor dashboard daily:
- Activation rate: Treatment 34% vs Control 24% ✅
- Time to aha: Treatment 16 min vs Control 45 min ✅
- Signup completion: Treatment 92% vs Control 94% ✅ (within threshold)

---

### Step 7: `/speckit.analyze-experiment`

**Prompt**:
> Analyze the experiment results for Personalized Onboarding.
> Results:
> - Activation: Treatment 34% vs Control 24% (p=0.003)
> - Time to aha: Treatment 16 min vs Control 45 min
> - Signup completion: Treatment 92% vs Control 94%
>
> Success criteria: Activation ≥32%, Time to aha ≤20 min, Signup >90%

**Output**:
```markdown
# Experiment Analysis Report: Personalized Onboarding

## Decision: SHIP TO 100% ✅

### Results Summary
- **Primary metric (Activation)**: 34% vs 24% = +10pp (43% relative lift)
  - **Statistical significance**: p=0.003 (highly significant)
  - **Exceeds target**: 32% → Achieved 34% ✅
- **Secondary (Time to aha)**: 16 min vs 45 min = -29 min (64% reduction)
  - **Exceeds target**: <20 min → Achieved 16 min ✅
- **Guardrail (Signup)**: 92% vs 94% = -2pp (within threshold)
  - **Threshold**: >90% → Achieved 92% ✅

### Segment Analysis
**By role**:
- Designers: 37% activation (even better!)
- Developers: 31% activation (still above target)

**By device**:
- Mobile: 30% activation
- Desktop: 36% activation

### Recommendation
**Ship to 100%** immediately. All success criteria exceeded.

### Learnings for Future
1. Role-specific onboarding highly effective for both roles
2. Designers respond especially well → consider more design-focused features
3. Mobile experience slightly lower → opportunity for mobile optimization

### Next Steps
1. Roll out to 100% via feature flag
2. Monitor for 1 week to confirm results hold
3. Remove feature flag after 30 days (make permanent)
4. Plan iteration: Mobile-optimized onboarding (new experiment)
```

---

### Step 8: `/speckit.merge`

After shipping to 100%, update system specs:

```markdown
## Feature: Personalized Onboarding

**Status**: Live (100% rollout)
**Shipped**: 2026-01-15
**Impact**:
- Activation rate: 23% → 34% (+11pp)
- Time to aha: 47 min → 16 min (-66%)
- D7 retention: 18% → 24% (+6pp)

**Implementation**:
- Role selection modal on signup
- Role-specific onboarding flows (Designer vs Developer)
- Feature flag: `personalized_onboarding_enabled` (permanent ON)

**Analytics**:
- Events: `onboarding_role_selected`, `onboarding_step_completed`
- Dashboard: [link]
```

---

## Integration with Existing Tools

### Analytics Tools

**Amplitude / Mixpanel**:
- Use for event tracking, funnel analysis, cohort retention
- Dashboard templates available in `/outputs/dashboards/`

**Google Analytics 4**:
- Use for acquisition source tracking (UTM parameters)
- Integrate with signup flow for attribution

**Segment**:
- Use as event routing layer (send to Amplitude + GA4 + data warehouse)
- Simplified SDK integration

---

### Experimentation Platforms

**LaunchDarkly / Split.io**:
- Feature flag management
- Gradual rollout controls
- Targeting rules

**Optimizely / VWO**:
- A/B testing for frontend changes
- Visual editor for non-engineers

**Statsig / GrowthBook**:
- Open-source alternatives
- Built-in analytics + experimentation

---

### Feedback Tools

**In-App Surveys**:
- Hotjar, Qualaroo, Survicate
- Trigger: Day 7 post-signup for NPS/CES

**User Interviews**:
- Calendly for scheduling
- Zoom for sessions
- Dovetail for synthesis

**Session Recordings**:
- FullStory, LogRocket, Hotjar
- Watch 10 activated + 10 not-activated users per week

---

## Best Practices Summary

### 1. Start with Metrics
Before writing spec, define:
- What metric are we moving?
- By how much?
- Why do we believe this change will move it?

### 2. Set Kill Criteria Early
Don't wait until after launch. Define failure conditions in spec before development starts.

### 3. Instrument Everything
Analytics is not optional. Event tracking is part of feature definition, not an afterthought.

### 4. Experiment by Default
For any user-facing change, default to A/B test before 100% rollout. Use feature flags.

### 5. Close the Feedback Loop
User research doesn't stop at launch. Continuous feedback informs iteration.

### 6. Data-Driven Decisions
Opinions start the hypothesis, but data makes the final call on ship/kill.

---

## Checklist: Is Your Spec Growth-Optimized?

Before starting development, verify:

- [ ] **Hypothesis stated**: "If [change], then [metric] will improve by [X%], because [reasoning]"
- [ ] **North Star aligned**: Feature ties to company North Star metric
- [ ] **Metrics defined**: Primary, secondary, guardrail metrics specified
- [ ] **User research**: Findings documented with evidence (qual + quant)
- [ ] **Experiment designed**: Control/treatment, sample size, duration
- [ ] **Success criteria**: Predetermined thresholds for shipping
- [ ] **Kill criteria**: Predetermined conditions for killing feature
- [ ] **Analytics spec'd**: Event taxonomy, properties, funnels, cohorts
- [ ] **Feature flag plan**: Rollout phases and rollback triggers
- [ ] **Feedback loop**: Collection methods and synthesis cadence

If all checked ✅, your spec is ready for growth-optimized development!

---

**Last Updated**: 2026-01-01
**Maintained by**: Spec Kit Team

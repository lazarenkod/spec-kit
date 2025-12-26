# Product Requirements Document (PRD) Template

> **Purpose**: Define what we're building, why, and how we'll measure success.
> **When to Use**: Before starting development of any significant feature or product.
> **Philosophy**: Specs should focus on problems and outcomes, not solutions. Leave the "how" to implementation.

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Product/Feature Name** | [Name] |
| **Document Owner** | [PM Name] |
| **Status** | [Draft | In Review | Approved | Deprecated] |
| **Version** | [X.Y] |
| **Created** | [YYYY-MM-DD] |
| **Last Updated** | [YYYY-MM-DD] |
| **Target Release** | [Quarter/Version] |

### Stakeholders & Approvers

| Role | Name | Status |
|------|------|--------|
| Product Manager | [Name] | ✅ Approved |
| Engineering Lead | [Name] | ⏳ Pending |
| Design Lead | [Name] | ⏳ Pending |
| QA Lead | [Name] | ⏳ Pending |

---

## 1. Executive Summary

### One-Liner
[Single sentence describing what this feature does and why it matters]

### Elevator Pitch (30 seconds)
For [target users]
Who [have this problem/need]
The [product/feature name]
Is a [category]
That [key benefit].
Unlike [current alternative],
Our solution [key differentiator].

---

## 2. Problem Statement

### The Problem
[Clear description of the problem we're solving. Focus on user pain, not solution.]

### Evidence

| Evidence Type | Source | Finding |
|---------------|--------|---------|
| User Research | [N interviews] | [Key insight] |
| Support Tickets | [N tickets/month] | [Pattern identified] |
| Analytics | [Data source] | [Metric showing problem] |
| Competitive Analysis | [Competitor] | [Gap/opportunity] |

### Jobs to Be Done (JTBD)

**Core Functional Job**:
> When [situation/trigger], I want to [motivation], so I can [expected outcome].

**Related Jobs**:
1. When [situation], I want to [action], so I can [outcome].
2. When [situation], I want to [action], so I can [outcome].

**Emotional Jobs**:
- Feel [emotion] when [situation]
- Avoid feeling [emotion] when [situation]

**Social Jobs**:
- Be seen as [perception] by [audience]

### Current State (How users solve this today)

| Current Solution | Pain Points | Frequency |
|------------------|-------------|-----------|
| [Workaround 1] | [Problems] | [How often] |
| [Workaround 2] | [Problems] | [How often] |
| [Competitor] | [Problems] | [How often] |

---

## 3. Goals & Success Metrics

### Objectives
| Objective | Key Result | Baseline | Target |
|-----------|------------|----------|--------|
| [Objective 1] | [Measurable KR] | [Current] | [Goal] |
| [Objective 2] | [Measurable KR] | [Current] | [Goal] |
| [Objective 3] | [Measurable KR] | [Current] | [Goal] |

### North Star Metric
**Primary Metric**: [Metric Name]
- **Definition**: [How it's calculated]
- **Current**: [Baseline value]
- **Target**: [Goal value]
- **Why This Metric**: [Connection to user value]

### Leading Indicators (Early signals)
| Indicator | Target | Measurement |
|-----------|--------|-------------|
| [Indicator 1] | [Target] | [How measured] |
| [Indicator 2] | [Target] | [How measured] |

### Lagging Indicators (Long-term impact)
| Indicator | Target | Timeframe |
|-----------|--------|-----------|
| [Indicator 1] | [Target] | [When measurable] |
| [Indicator 2] | [Target] | [When measurable] |

### Counter-Metrics (What we DON'T want to hurt)
| Metric | Current | Alert Threshold |
|--------|---------|-----------------|
| [Metric 1] | [Value] | [If drops below X] |
| [Metric 2] | [Value] | [If drops below X] |

---

## 4. Target Users

### Primary Persona

**Name**: [Persona Name]

**Demographics**:
- Role: [Job title / role]
- Company: [Size / type]
- Technical level: [Low | Medium | High]

**Behaviors**:
- [Behavior pattern 1]
- [Behavior pattern 2]

**Goals**:
- [Goal 1]
- [Goal 2]

**Frustrations**:
- [Pain point 1]
- [Pain point 2]

**Quote**: "[Actual quote from user research]"

### Secondary Personas

| Persona | Description | Importance |
|---------|-------------|------------|
| [Persona 2] | [Brief description] | [Why matters] |
| [Persona 3] | [Brief description] | [Why matters] |

### Anti-Personas (Who is this NOT for)

| Anti-Persona | Why Not | Risk if We Build for Them |
|--------------|---------|---------------------------|
| [Anti-persona 1] | [Reason] | [What we'd over-complicate] |
| [Anti-persona 2] | [Reason] | [What we'd over-complicate] |

---

## 5. User Stories & Requirements

### User Story Map

```
Backbone (Activities):
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  Activity 1 │  Activity 2 │  Activity 3 │  Activity 4 │
└─────────────┴─────────────┴─────────────┴─────────────┘

Walking Skeleton (MVP):
┌─────────────┬─────────────┬─────────────┬─────────────┐
│   Story A   │   Story D   │   Story G   │   Story J   │
└─────────────┴─────────────┴─────────────┴─────────────┘

Release 1:
┌─────────────┬─────────────┬─────────────┐
│   Story B   │   Story E   │   Story H   │
└─────────────┴─────────────┴─────────────┘

Release 2:
┌─────────────┬─────────────┐
│   Story C   │   Story F   │
└─────────────┴─────────────┘
```

### Requirements by Priority

#### P0 - Must Have (MVP)

| ID | User Story | Acceptance Criteria | JTBD Link |
|----|------------|---------------------|-----------|
| US-001 | As a [user], I want to [action], so that [benefit] | - [ ] Criterion 1<br>- [ ] Criterion 2 | [Job reference] |
| US-002 | As a [user], I want to [action], so that [benefit] | - [ ] Criterion 1<br>- [ ] Criterion 2 | [Job reference] |

#### P1 - Should Have (Target Release)

| ID | User Story | Acceptance Criteria | JTBD Link |
|----|------------|---------------------|-----------|
| US-003 | As a [user], I want to [action], so that [benefit] | - [ ] Criterion 1 | [Job reference] |

#### P2 - Nice to Have (Future)

| ID | User Story | Acceptance Criteria | Notes |
|----|------------|---------------------|-------|
| US-004 | As a [user], I want to [action], so that [benefit] | - [ ] Criterion 1 | Consider for v2 |

### Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-001 | [System shall...] | P0 | |
| FR-002 | [System shall...] | P0 | |
| FR-003 | [System shall...] | P1 | |

### Non-Functional Requirements

| Category | Requirement | Target | Notes |
|----------|-------------|--------|-------|
| **Performance** | Page load time | < 2s (p95) | |
| **Performance** | API response time | < 200ms (p95) | |
| **Scalability** | Concurrent users | 10,000 | |
| **Availability** | Uptime | 99.9% | |
| **Security** | Authentication | OAuth 2.0 + MFA | |
| **Accessibility** | WCAG compliance | AA | |
| **Localization** | Languages | EN, ES, DE | |

---

## 6. Scope

### In Scope
- ✅ [Feature/capability 1]
- ✅ [Feature/capability 2]
- ✅ [Feature/capability 3]

### Out of Scope
- ❌ [Explicitly excluded 1] — *Reason: [why not now]*
- ❌ [Explicitly excluded 2] — *Reason: [why not now]*
- ❌ [Explicitly excluded 3] — *Reason: [why not now]*

### Future Considerations
- 🔮 [Potential future enhancement 1]
- 🔮 [Potential future enhancement 2]

---

## 7. Solution Overview

> **Note**: This section provides high-level direction. Detailed design belongs in separate design docs.

### Proposed Approach
[High-level description of the solution direction]

### Key User Flows

**Flow 1: [Flow Name]**
```
[Step 1] → [Step 2] → [Step 3] → [Step 4]
                ↓ (if error)
           [Error handling]
```

### Design Principles
1. **[Principle 1]**: [Why this matters for this feature]
2. **[Principle 2]**: [Why this matters for this feature]
3. **[Principle 3]**: [Why this matters for this feature]

### Key Decisions Made

| Decision | Choice | Rationale | ADR Link |
|----------|--------|-----------|----------|
| [Decision 1] | [What we chose] | [Why] | [ADR-XXX] |
| [Decision 2] | [What we chose] | [Why] | [ADR-XXX] |

---

## 8. Prioritization

### RICE Scoring

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| [Feature 1] | [#users] | [0.25-3] | [50-100%] | [person-months] | **[Score]** |
| [Feature 2] | [#users] | [0.25-3] | [50-100%] | [person-months] | **[Score]** |
| [Feature 3] | [#users] | [0.25-3] | [50-100%] | [person-months] | **[Score]** |

**RICE Formula**: (Reach × Impact × Confidence) / Effort

**Impact Scale**:
- 3 = Massive (game changer)
- 2 = High (significant improvement)
- 1 = Medium (notable improvement)
- 0.5 = Low (minor improvement)
- 0.25 = Minimal

### MoSCoW Classification

| Must Have | Should Have | Could Have | Won't Have |
|-----------|-------------|------------|------------|
| [Feature] | [Feature] | [Feature] | [Feature] |
| [Feature] | [Feature] | [Feature] | [Feature] |

---

## 9. Risks & Mitigations

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation plan] | [Name] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Mitigation plan] | [Name] |

### Dependencies

| Dependency | Type | Status | Risk if Delayed |
|------------|------|--------|-----------------|
| [Dependency 1] | Internal/External | [Status] | [Impact] |
| [Dependency 2] | Internal/External | [Status] | [Impact] |

### Assumptions
1. [Assumption 1] — *If wrong, then [consequence]*
2. [Assumption 2] — *If wrong, then [consequence]*

---

## 10. Go-to-Market

### Launch Plan

| Phase | Audience | Goal | Success Criteria |
|-------|----------|------|------------------|
| Alpha | Internal team | Bug finding | < 5 P0 bugs |
| Beta | [N] early users | Validate value prop | [Metric target] |
| GA | All users | Full launch | [Metric target] |

### Communication Plan

| Audience | Channel | Message | Timing |
|----------|---------|---------|--------|
| Internal | Slack | Feature overview | T-2 weeks |
| Sales | Training session | Demo + FAQ | T-1 week |
| Customers | Email + In-app | Value prop | Launch day |
| Public | Blog post | Announcement | Launch day |

### Support Readiness
- [ ] Knowledge base articles updated
- [ ] Support team trained
- [ ] FAQ documented
- [ ] Escalation path defined

---

## 11. Timeline & Milestones

| Milestone | Date | Deliverable | Exit Criteria |
|-----------|------|-------------|---------------|
| Kickoff | [Date] | PRD approved | Stakeholder sign-off |
| Design Complete | [Date] | Figma designs | Design review passed |
| Dev Complete | [Date] | Feature code | All tests passing |
| QA Complete | [Date] | Test report | < 0 P0/P1 bugs |
| Launch | [Date] | GA release | Monitoring green |

---

## 12. Open Questions

| # | Question | Status | Decision | Date |
|---|----------|--------|----------|------|
| 1 | [Open question] | Open/Closed | [Decision made] | [Date] |
| 2 | [Open question] | Open/Closed | [Decision made] | [Date] |

---

## Appendix

### Competitive Analysis

| Feature | Us | Competitor A | Competitor B |
|---------|----|--------------| --------------|
| [Feature 1] | [✅/❌/🔶] | [✅/❌/🔶] | [✅/❌/🔶] |
| [Feature 2] | [✅/❌/🔶] | [✅/❌/🔶] | [✅/❌/🔶] |

### User Research Insights
[Link to research repository/findings]

### Technical Notes
[Link to technical design doc]

### Design Assets
[Link to Figma/design files]

### Related Documents
- [Link to vision doc]
- [Link to competitive analysis]
- [Link to user research]

---

# PRD Quality Checklist

Before finalizing, verify:

## Problem Definition
- [ ] Problem is clearly stated (not solution-focused)
- [ ] Evidence supports the problem exists
- [ ] JTBD is articulated
- [ ] Target users are specific, not generic

## Success Definition
- [ ] North Star metric is defined
- [ ] Success metrics are measurable
- [ ] Counter-metrics identified (what we don't want to hurt)
- [ ] Leading and lagging indicators distinguished

## Scope Clarity
- [ ] In scope is explicit
- [ ] Out of scope is explicit with rationale
- [ ] P0 vs P1 vs P2 clearly separated
- [ ] MVP is defined

## Stakeholder Alignment
- [ ] All key stakeholders have reviewed
- [ ] Open questions are tracked
- [ ] Risks and dependencies documented
- [ ] Timeline agreed upon

## Anti-Pattern Check
- [ ] No solution bias in problem statement
- [ ] Requirements tied to personas, not "users"
- [ ] Every feature has a success metric
- [ ] No infinite backlog (ruthless prioritization)

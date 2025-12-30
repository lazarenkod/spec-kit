# Product Requirements Document (PRD) Template

## Purpose

Comprehensive template for writing Product Requirements Documents that clearly communicate what to build, why, and success criteria.

---

## PRD Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                         PRD Sections                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. OVERVIEW ──────── What and why (executive summary)          │
│  2. PROBLEM ───────── Customer pain points and evidence         │
│  3. GOALS ─────────── Success metrics and business impact       │
│  4. SOLUTION ──────── Features and user flows                   │
│  5. SCOPE ─────────── In scope, out of scope, future            │
│  6. REQUIREMENTS ──── Functional and non-functional             │
│  7. DESIGN ────────── Wireframes and specifications             │
│  8. RISKS ─────────── Dependencies and mitigation               │
│  9. TIMELINE ──────── Milestones and launch plan                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## PRD Template

```markdown
# PRD: [Feature Name]

**Document Owner:** [Name]
**Last Updated:** [Date]
**Status:** [Draft | Review | Approved | In Development | Shipped]
**Target Release:** [Version/Quarter]

---

## 1. Overview

### 1.1 Summary
<!-- 2-3 sentence description of the feature -->

### 1.2 Background
<!-- Context: Why are we considering this now? What changed? -->

### 1.3 Objective
<!-- Clear statement of what we want to achieve -->

---

## 2. Problem Statement

### 2.1 Customer Problem
<!-- What problem are we solving for customers? -->

### 2.2 Evidence
<!-- How do we know this is a real problem? -->

| Source | Finding |
|--------|---------|
| Customer interviews | [Finding] |
| Support tickets | [X tickets/month about this] |
| Analytics | [Data showing the problem] |
| Churn analysis | [Correlation] |

### 2.3 Current State
<!-- How do customers solve this today? -->

### 2.4 Desired State
<!-- How will customers solve this with our solution? -->

---

## 3. Goals & Success Metrics

### 3.1 Business Goals
<!-- What business outcomes are we driving? -->

| Goal | Target | Baseline |
|------|--------|----------|
| [Primary metric] | [Target] | [Current] |
| [Secondary metric] | [Target] | [Current] |

### 3.2 User Goals
<!-- What do users want to accomplish? -->

### 3.3 Success Criteria
<!-- How do we know if this was successful? -->

- [ ] [Metric] increases by [X]% within [timeframe]
- [ ] [Behavior] adoption reaches [X]% of users
- [ ] [Satisfaction] score improves to [X]

### 3.4 Non-Goals
<!-- What are we explicitly NOT trying to achieve? -->

---

## 4. Solution

### 4.1 Proposed Solution
<!-- High-level description of the solution -->

### 4.2 User Stories

| As a... | I want to... | So that... | Priority |
|---------|-------------|------------|----------|
| [Persona] | [Action] | [Benefit] | P0/P1/P2 |

### 4.3 User Flows

#### Primary Flow
```
[Step 1] → [Step 2] → [Step 3] → [Success State]
```

#### Alternate Flows
<!-- Edge cases, error states -->

### 4.4 Feature Details

#### Feature 1: [Name]
- **Description:** [What it does]
- **User benefit:** [Why it matters]
- **Acceptance criteria:**
  - [ ] [Criteria 1]
  - [ ] [Criteria 2]

---

## 5. Scope

### 5.1 In Scope
<!-- What's included in this release -->

- [ ] [Feature/Capability 1]
- [ ] [Feature/Capability 2]

### 5.2 Out of Scope
<!-- What's explicitly excluded (and why) -->

- [ ] [Feature] - [Reason]
- [ ] [Feature] - [Reason]

### 5.3 Future Considerations
<!-- What might come later -->

- [Potential future feature]
- [Enhancement idea]

---

## 6. Requirements

### 6.1 Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | [Description] | P0 | |
| FR-2 | [Description] | P1 | |

### 6.2 Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| Performance | [e.g., Page load < 2s] |
| Scalability | [e.g., Support 10K concurrent users] |
| Security | [e.g., Data encrypted at rest] |
| Accessibility | [e.g., WCAG 2.1 AA compliance] |
| Compatibility | [e.g., Chrome, Firefox, Safari, Edge] |

### 6.3 Technical Requirements

<!-- From engineering, if known -->

- [Technical constraint or requirement]
- [Integration requirement]

---

## 7. Design

### 7.1 Wireframes
<!-- Link to Figma/design files -->

[Link to designs]

### 7.2 Key Screens

| Screen | Description | Link |
|--------|-------------|------|
| [Screen name] | [Purpose] | [Link] |

### 7.3 Design Considerations
<!-- Important UX decisions and rationale -->

---

## 8. Risks & Dependencies

### 8.1 Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk description] | High/Med/Low | High/Med/Low | [Mitigation plan] |

### 8.2 Dependencies

| Dependency | Owner | Status | Required By |
|------------|-------|--------|-------------|
| [Dependency] | [Team/Person] | [Status] | [Date] |

### 8.3 Open Questions

| Question | Answer | Owner | Due |
|----------|--------|-------|-----|
| [Question] | [Pending/Answer] | [Name] | [Date] |

---

## 9. Timeline

### 9.1 Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| PRD Approval | [Date] | [Status] |
| Design Complete | [Date] | [Status] |
| Development Start | [Date] | [Status] |
| Beta/Testing | [Date] | [Status] |
| Launch | [Date] | [Status] |

### 9.2 Launch Plan

- **Rollout strategy:** [Big bang / Phased / Beta → GA]
- **Feature flag:** [Yes/No]
- **Documentation:** [Required updates]
- **Marketing:** [Announcement plan]

---

## Appendix

### A. Glossary
<!-- Define terms -->

### B. References
<!-- Links to related documents -->

### C. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial version |
```

---

## PRD Best Practices

```yaml
best_practices:
  clarity:
    - "Write for engineers who don't have context"
    - "Be specific about what, vague about how"
    - "Define success upfront"
    - "Use examples liberally"

  brevity:
    - "Start with a one-pager, expand as needed"
    - "Executive summary should stand alone"
    - "Link to details rather than inline"

  collaboration:
    - "Get engineering input early"
    - "Review with design before finalizing"
    - "Share with stakeholders for feedback"
    - "Update as decisions are made"

  maintenance:
    - "Keep PRD as living document"
    - "Update status and decisions"
    - "Archive when feature ships"
```

---

## PRD Checklist

```yaml
prd_checklist:
  before_writing:
    - [ ] Problem validated with customers
    - [ ] Aligned with company goals
    - [ ] Stakeholder buy-in obtained

  content_quality:
    - [ ] Problem clearly articulated
    - [ ] Success metrics defined
    - [ ] Scope clearly bounded
    - [ ] User stories written
    - [ ] Acceptance criteria defined

  review_readiness:
    - [ ] Engineering reviewed for feasibility
    - [ ] Design reviewed for UX
    - [ ] Dependencies identified
    - [ ] Risks documented
    - [ ] Timeline estimated

  approval:
    - [ ] Stakeholder sign-off
    - [ ] Engineering commitment
    - [ ] Resources allocated
```

---

## Mini-PRD (One-Pager)

For smaller features, use this condensed format:

```markdown
# [Feature Name] - Mini PRD

**Owner:** [Name] | **Target:** [Date]

## Problem
[2-3 sentences describing the problem]

## Proposed Solution
[2-3 sentences describing the solution]

## Success Metric
[Primary metric we'll track]

## Scope
**In:** [Bullet list]
**Out:** [Bullet list]

## Key User Stories
1. As a [user], I want [action] so that [benefit]
2. ...

## Dependencies
- [Dependency 1]

## Timeline
- Start: [Date]
- Ship: [Date]
```

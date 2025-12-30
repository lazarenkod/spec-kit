# Product Roadmap Template

## Purpose

Create clear, actionable product roadmaps that communicate strategic direction, priorities, and timelines to stakeholders.

---

## Roadmap Types

```yaml
roadmap_types:
  strategic:
    timeframe: "12-24 months"
    audience: "Executives, investors, board"
    detail_level: "Themes and goals"
    format: "Narrative + themes"

  tactical:
    timeframe: "Quarterly (3 months)"
    audience: "Engineering, design, stakeholders"
    detail_level: "Features and milestones"
    format: "Timeline + features"

  release:
    timeframe: "1-2 sprints"
    audience: "Development team"
    detail_level: "Stories and tasks"
    format: "Kanban/Sprint board"
```

---

## Strategic Roadmap Template

### 12-Month Strategic Roadmap

```markdown
# [Product Name] Strategic Roadmap

**Vision:** [One-line product vision]
**Last Updated:** [Date]
**Owner:** [Name]

---

## Annual Themes

### Q1: [Theme Name]
**Objective:** [What we're trying to achieve]
**Key Results:**
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

**Major Initiatives:**
1. [Initiative 1] - [Brief description]
2. [Initiative 2] - [Brief description]

---

### Q2: [Theme Name]
**Objective:** [What we're trying to achieve]
**Key Results:**
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

**Major Initiatives:**
1. [Initiative 1]
2. [Initiative 2]

---

### Q3: [Theme Name]
[Similar structure...]

---

### Q4: [Theme Name]
[Similar structure...]

---

## Strategic Pillars

| Pillar | Description | Q1 | Q2 | Q3 | Q4 |
|--------|-------------|----|----|----|----|
| Growth | User acquisition & expansion | ▓▓░░ | ▓▓▓░ | ▓▓▓▓ | ▓▓▓▓ |
| Retention | Reduce churn, increase engagement | ▓▓▓░ | ▓▓▓░ | ▓▓░░ | ▓▓░░ |
| Platform | Infrastructure & scalability | ▓░░░ | ▓▓░░ | ▓▓▓░ | ▓▓░░ |
| Innovation | New products & capabilities | ░░░░ | ▓░░░ | ▓▓░░ | ▓▓▓░ |

Legend: ░ = Low focus | ▓ = Medium focus | ▓▓ = High focus

---

## Success Metrics

| Metric | Current | Q1 Target | Q2 Target | Q3 Target | Q4 Target |
|--------|---------|-----------|-----------|-----------|-----------|
| [Metric 1] | [X] | [Y] | [Y] | [Y] | [Y] |
| [Metric 2] | [X] | [Y] | [Y] | [Y] | [Y] |

---

## Dependencies & Risks

| Risk/Dependency | Impact | Mitigation |
|-----------------|--------|------------|
| [Item] | High/Med/Low | [Plan] |

---

## Resource Allocation

| Team | Q1 Focus | Q2 Focus | Q3 Focus | Q4 Focus |
|------|----------|----------|----------|----------|
| Engineering | [Focus] | [Focus] | [Focus] | [Focus] |
| Design | [Focus] | [Focus] | [Focus] | [Focus] |
```

---

## Quarterly Roadmap Template

```markdown
# Q[X] [Year] Product Roadmap

**Quarter Goals:**
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

---

## Monthly Breakdown

### Month 1: [Name/Theme]

| Feature | Status | Owner | Target |
|---------|--------|-------|--------|
| [Feature 1] | 🟡 In Progress | @name | Week 2 |
| [Feature 2] | 🔵 Planned | @name | Week 4 |
| [Feature 3] | 🟢 Complete | @name | Done |

**Key Milestones:**
- Week 2: [Milestone]
- Week 4: [Milestone]

---

### Month 2: [Name/Theme]

| Feature | Status | Owner | Target |
|---------|--------|-------|--------|
| [Feature 1] | 🔵 Planned | @name | Week 6 |
| [Feature 2] | 🔵 Planned | @name | Week 8 |

---

### Month 3: [Name/Theme]

| Feature | Status | Owner | Target |
|---------|--------|-------|--------|
| [Feature 1] | 🔵 Planned | @name | Week 10 |
| [Feature 2] | 🔵 Planned | @name | Week 12 |

---

## Status Legend
- 🟢 Complete
- 🟡 In Progress
- 🔵 Planned
- 🔴 Blocked
- ⚪ Backlog

---

## Dependencies

| Dependency | Required By | Status | Owner |
|------------|-------------|--------|-------|
| [Item] | [Feature] | [Status] | @name |

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Plan] |
```

---

## Now-Next-Later Roadmap

A flexible, outcome-focused format:

```markdown
# [Product Name] Roadmap

**Updated:** [Date]

---

## NOW (Current Quarter)

**Theme:** [Current focus]

| Initiative | Description | Status | Owner |
|------------|-------------|--------|-------|
| [Name] | [Brief description] | [%] | @name |

**Outcomes we're targeting:**
- [Outcome 1]
- [Outcome 2]

---

## NEXT (Next Quarter)

**Theme:** [Upcoming focus]

| Initiative | Description | Confidence |
|------------|-------------|------------|
| [Name] | [Brief description] | High/Med/Low |

**Why these initiatives:**
- [Strategic rationale]

---

## LATER (Future Quarters)

**Theme:** [Future direction]

| Idea | Description | When |
|------|-------------|------|
| [Name] | [Brief description] | [Q/Year] |

**Considerations:**
- [What might change this]
- [Dependencies]

---

## NOT DOING (Explicit Exclusions)

| Idea | Why Not Now |
|------|-------------|
| [Feature] | [Reason] |
```

---

## Visual Timeline Format

```
Q1 2024                    Q2 2024                    Q3 2024                    Q4 2024
├─────────────────────────┼─────────────────────────┼─────────────────────────┼─────────────────────────┤

GROWTH
├── User Onboarding v2 ────────────────┤
                          ├── Referral Program ─────────────────────────────────────────────────────────┤
                                                    ├── Enterprise Features ──────────────────────────┤

PLATFORM
├── API v3 ────────────────────────────────────────┤
                                        ├── Performance Optimization ───────────────────────────────────┤

RETENTION
          ├── Engagement Features ─────────────────────────────┤
                                                              ├── Advanced Analytics ─────────────────┤
```

---

## Roadmap Communication

### For Executives

```yaml
executive_format:
  focus_on:
    - "Strategic themes and outcomes"
    - "Business impact and metrics"
    - "Resource allocation"
    - "Key risks and dependencies"

  avoid:
    - "Detailed feature specs"
    - "Technical implementation details"
    - "Specific dates (use quarters)"

  frequency: "Quarterly updates"
```

### For Engineering

```yaml
engineering_format:
  focus_on:
    - "What we're building and why"
    - "Priority order"
    - "Dependencies and blockers"
    - "Technical requirements"
    - "Milestones and deadlines"

  include:
    - "PRD links"
    - "Design specs"
    - "Acceptance criteria"

  frequency: "Sprint planning + monthly"
```

### For Customers

```yaml
customer_format:
  focus_on:
    - "Benefits, not features"
    - "General direction"
    - "Rough timing (quarters, not dates)"

  avoid:
    - "Specific commitments"
    - "Detailed timelines"
    - "Unannounced features"

  disclaimer: "Subject to change based on feedback and priorities"
```

---

## Roadmap Review Process

```yaml
review_cadence:
  weekly:
    - "Status updates"
    - "Blocker identification"
    - "Priority adjustments"

  monthly:
    - "Progress against goals"
    - "Scope adjustments"
    - "Resource reallocation"

  quarterly:
    - "Goal setting for next quarter"
    - "Retrospective on completed quarter"
    - "Strategic alignment check"
    - "Stakeholder presentations"

  annually:
    - "Vision and strategy refresh"
    - "Major initiative planning"
    - "Resource planning"
```

---

## Roadmap Best Practices

```yaml
best_practices:
  principles:
    - "Outcomes over outputs"
    - "Flexibility over precision"
    - "Transparency about uncertainty"
    - "Regular updates"

  common_mistakes:
    - "Too much detail too far out"
    - "Feature lists without outcomes"
    - "No flexibility for learning"
    - "Promising specific dates"
    - "Not updating when things change"

  tips:
    - "Use confidence levels for future items"
    - "Link to strategy and goals"
    - "Show what you're NOT doing"
    - "Update status regularly"
    - "Get stakeholder input"
```

---

## Roadmap Template Checklist

```yaml
roadmap_checklist:
  content:
    - [ ] Vision/strategy clearly stated
    - [ ] Goals and metrics defined
    - [ ] Initiatives aligned to goals
    - [ ] Priorities clear
    - [ ] Dependencies identified
    - [ ] Risks documented

  format:
    - [ ] Appropriate for audience
    - [ ] Easy to update
    - [ ] Accessible to stakeholders
    - [ ] Version controlled

  process:
    - [ ] Regular review scheduled
    - [ ] Update process defined
    - [ ] Stakeholder feedback loop
```

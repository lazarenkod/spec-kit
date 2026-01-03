# MOALS Framework & Operating System Model (Amazon)

> **Purpose**: Define the mechanisms, learning loops, and operational cadence that drive consistent execution at scale. This framework ensures the business operates as a self-improving system, not a collection of ad-hoc processes.

## MOALS Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           OPERATING SYSTEM MODEL                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   MECHANISMS ──────► OUTPUTS ──────► ACTIONS ──────► LEARNING               │
│        │                │                │                │                  │
│        │                ▼                ▼                ▼                  │
│        │         ┌──────────┐     ┌──────────┐     ┌──────────┐             │
│        │         │  Metrics │     │ Decisions│     │ Insights │             │
│        │         │  Results │     │  Changes │     │ Patterns │             │
│        │         └──────────┘     └──────────┘     └──────────┘             │
│        │                                                  │                  │
│        └──────────────────── SYSTEMS ◄───────────────────┘                  │
│                           (Feedback Loop)                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Component | Definition | Example | Owner |
|:---------:|------------|---------|:-----:|
| **Mechanisms** | Repeatable processes that guarantee outcomes | Weekly metrics review | [Role] |
| **Outputs** | Measurable results from mechanisms | Dashboard, reports, alerts | [Role] |
| **Actions** | Decisions and changes triggered by outputs | Escalations, pivots, investments | [Role] |
| **Learning** | Insights captured for systemic improvement | Post-mortems, pattern recognition | [Role] |
| **Systems** | Tools and infrastructure enabling the loop | Data pipelines, automation | [Role] |

---

## Flywheel Model

```
                           ┌─────────────────┐
                           │   [Driver 1]    │
                           │  e.g., Lower    │
                           │     Prices      │
                           └────────┬────────┘
                                    │
                                    ▼
       ┌─────────────────┐    ┌─────────────────┐
       │   [Driver 5]    │    │   [Driver 2]    │
       │  e.g., Lower    │◄───│  e.g., More     │
       │  Cost Structure │    │   Customers     │
       └────────┬────────┘    └────────┬────────┘
                │                      │
                │                      ▼
       ┌────────┴────────┐    ┌─────────────────┐
       │   [Driver 4]    │    │   [Driver 3]    │
       │  e.g., More     │◄───│  e.g., More     │
       │    Sellers      │    │     Traffic     │
       └─────────────────┘    └─────────────────┘
```

### Flywheel Components

| Stage | Driver | Metric | Investment | Acceleration Lever |
|:-----:|--------|:------:|:----------:|-------------------|
| 1 | [Initial driver, e.g., "Product quality"] | [NPS / Quality score] | [X]% of effort | [How to spin faster] |
| 2 | [Second driver, e.g., "Customer acquisition"] | [CAC / Growth rate] | [X]% of effort | [How to spin faster] |
| 3 | [Third driver, e.g., "Network effects"] | [Engagement / Virality] | [X]% of effort | [How to spin faster] |
| 4 | [Fourth driver, e.g., "Data/learning"] | [Model accuracy] | [X]% of effort | [How to spin faster] |
| 5 | [Fifth driver, e.g., "Unit economics"] | [Margin / LTV:CAC] | [X]% of effort | [How to spin faster] |

### Flywheel Health

| Indicator | Current | Target | Status |
|-----------|:-------:|:------:|:------:|
| Flywheel velocity (cycle time) | [X] days | [X] days | [Green/Yellow/Red] |
| Stage 1→2 conversion | [X]% | [X]% | [Green/Yellow/Red] |
| Stage 2→3 conversion | [X]% | [X]% | [Green/Yellow/Red] |
| Self-reinforcing growth | [X]% organic | [X]% organic | [Green/Yellow/Red] |

---

## Key Mechanisms

### Mechanism Inventory

| Mechanism | Purpose | Cadence | Input | Output | Owner |
|-----------|---------|:-------:|-------|--------|:-----:|
| **Weekly Business Review (WBR)** | Operational health check | Weekly | Metrics pack | Action items | [Role] |
| **Monthly Business Review (MBR)** | Strategic progress review | Monthly | WBR rollups | Strategy adjustments | [Role] |
| **Quarterly Business Review (QBR)** | Long-term planning | Quarterly | MBR trends | Resource allocation | [Role] |
| **[Custom mechanism 1]** | [Purpose] | [Cadence] | [Input] | [Output] | [Role] |
| **[Custom mechanism 2]** | [Purpose] | [Cadence] | [Input] | [Output] | [Role] |

### Mechanism Design Template

| Element | Description |
|---------|-------------|
| **Name** | [Mechanism name] |
| **Purpose** | [What outcome does this guarantee?] |
| **Trigger** | [What starts this mechanism?] |
| **Cadence** | [How often does it run?] |
| **Participants** | [Who must be involved?] |
| **Inputs** | [What data/artifacts are required?] |
| **Process** | [Step-by-step what happens?] |
| **Outputs** | [What artifacts/decisions result?] |
| **Escalation** | [When/how to escalate issues?] |
| **Owner** | [Single-threaded owner] |

---

## Weekly Business Review (WBR)

### WBR Dashboard

| Category | Metric | Week-1 | Current | WoW Δ | Target | Status |
|----------|--------|:------:|:-------:|:-----:|:------:|:------:|
| **Growth** | [Active users] | [X] | [X] | [+/-X%] | [X] | [G/Y/R] |
| **Growth** | [New signups] | [X] | [X] | [+/-X%] | [X] | [G/Y/R] |
| **Engagement** | [Core action rate] | [X]% | [X]% | [+/-X%] | [X]% | [G/Y/R] |
| **Engagement** | [Retention D7/W4] | [X]% | [X]% | [+/-X%] | [X]% | [G/Y/R] |
| **Revenue** | [MRR/ARR] | $[X]K | $[X]K | [+/-X%] | $[X]K | [G/Y/R] |
| **Revenue** | [ARPU] | $[X] | $[X] | [+/-X%] | $[X] | [G/Y/R] |
| **Quality** | [Error rate] | [X]% | [X]% | [+/-X%] | <[X]% | [G/Y/R] |
| **Quality** | [Customer satisfaction] | [X] | [X] | [+/-X%] | [X] | [G/Y/R] |

### WBR Agenda

| Time | Topic | Owner | Outcome |
|:----:|-------|:-----:|---------|
| 5 min | Metric review (reds first) | [Owner] | Issues identified |
| 10 min | Root cause discussion | All | Causes understood |
| 10 min | Action item review (prior week) | [Owner] | Progress tracked |
| 10 min | New action items | All | Owners assigned |
| 5 min | Blockers and escalations | [Owner] | Escalations documented |

### WBR Rules

1. **Single-threaded ownership**: Every metric has exactly one owner
2. **Andon cord**: Anyone can escalate; no penalty for raising issues
3. **Data-driven**: Decisions based on metrics, not opinions
4. **Action-oriented**: Every red metric gets an action item with owner and deadline
5. **No surprises**: Issues should surface here, not in executive reviews

---

## Learning Loops

### Learning Loop Framework

| Loop Type | Cycle Time | Input | Process | Output |
|-----------|:----------:|-------|---------|--------|
| **Operational** | Daily/Weekly | Metrics, incidents | WBR, retrospectives | Process improvements |
| **Tactical** | Weekly/Monthly | A/B tests, experiments | Experiment review | Feature decisions |
| **Strategic** | Quarterly | Market data, trends | QBR, planning | Strategy pivots |
| **Systemic** | Annual | All learnings | Annual review | Operating model updates |

### Learning Capture Template

| Field | Content |
|-------|---------|
| **Date** | [YYYY-MM-DD] |
| **Category** | [Operational / Tactical / Strategic] |
| **Context** | [What happened?] |
| **Observation** | [What did we notice?] |
| **Insight** | [What does this mean?] |
| **Action** | [What mechanism/process change results?] |
| **Owner** | [Who implements?] |
| **Validation** | [How do we know it worked?] |

### Learning Inventory

| # | Learning | Source | Mechanism Change | Status |
|:-:|----------|--------|------------------|:------:|
| 1 | [Key insight from operations] | [WBR / Incident] | [What changed] | [Implemented/Pending] |
| 2 | [Key insight from experiments] | [A/B test] | [What changed] | [Implemented/Pending] |
| 3 | [Key insight from customers] | [Feedback] | [What changed] | [Implemented/Pending] |
| 4 | [Key insight from market] | [Research] | [What changed] | [Implemented/Pending] |

---

## Operational Metrics Dashboard

### Input Metrics (Leading Indicators)

| Category | Metric | Definition | Owner | Target | Alert Threshold |
|----------|--------|------------|:-----:|:------:|:---------------:|
| **Acquisition** | [Traffic / Signups] | [Definition] | [Role] | [X]/day | <[X]/day |
| **Activation** | [First action rate] | [Definition] | [Role] | [X]% | <[X]% |
| **Engagement** | [Session frequency] | [Definition] | [Role] | [X]/week | <[X]/week |
| **Quality** | [Error rate] | [Definition] | [Role] | <[X]% | >[X]% |

### Output Metrics (Lagging Indicators)

| Category | Metric | Definition | Owner | Target | Alert Threshold |
|----------|--------|------------|:-----:|:------:|:---------------:|
| **Revenue** | [MRR/ARR] | [Definition] | [Role] | $[X]K | <$[X]K |
| **Retention** | [Churn rate] | [Definition] | [Role] | <[X]% | >[X]% |
| **Growth** | [Net growth rate] | [Definition] | [Role] | [X]% MoM | <[X]% MoM |
| **Profitability** | [Gross margin] | [Definition] | [Role] | [X]% | <[X]% |

### Metric Hierarchy

```
North Star Metric: [e.g., "Weekly Active Value Created"]
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   [Pillar 1]          [Pillar 2]          [Pillar 3]
   Acquisition         Engagement          Monetization
        │                   │                   │
   ┌────┴────┐        ┌────┴────┐        ┌────┴────┐
   ▼         ▼        ▼         ▼        ▼         ▼
[Metric] [Metric]  [Metric] [Metric]  [Metric] [Metric]
```

---

## Systems & Automation

### System Inventory

| System | Purpose | Automation Level | Dependencies | Owner |
|--------|---------|:----------------:|--------------|:-----:|
| **Data pipeline** | Collect and transform metrics | [Full/Partial/Manual] | [Infrastructure] | [Role] |
| **Alerting** | Surface issues proactively | [Full/Partial/Manual] | [Data pipeline] | [Role] |
| **Reporting** | Generate WBR/MBR dashboards | [Full/Partial/Manual] | [Data pipeline] | [Role] |
| **Experimentation** | Run and analyze A/B tests | [Full/Partial/Manual] | [Data pipeline] | [Role] |
| **[Custom system]** | [Purpose] | [Full/Partial/Manual] | [Dependencies] | [Role] |

### Automation Roadmap

| System | Current State | Target State | Investment | Timeline |
|--------|:-------------:|:------------:|:----------:|:--------:|
| Data pipeline | [Manual/Partial] | Full automation | [X] eng-weeks | Q[X] |
| Alerting | [Manual/Partial] | Real-time + smart | [X] eng-weeks | Q[X] |
| Reporting | [Manual/Partial] | Self-serve | [X] eng-weeks | Q[X] |

---

## Operating Cadence

### Annual Calendar

| Month | Key Activities | Reviews | Planning |
|:-----:|----------------|---------|----------|
| Jan | [Annual planning] | Annual Review | OKR setting |
| Apr | [Q1 review] | QBR | Q2 planning |
| Jul | [Q2 review, mid-year] | QBR + Mid-year | Q3 planning |
| Oct | [Q3 review] | QBR | Q4 + next year planning |

### Weekly Cadence

| Day | Activity | Participants | Duration |
|:---:|----------|--------------|:--------:|
| Mon | WBR preparation | Data team | 2 hrs |
| Tue | Weekly Business Review | Leadership | 1 hr |
| Wed | Action item execution | Owners | Ongoing |
| Thu | Team syncs | Teams | 30 min each |
| Fri | Learning capture | All | 30 min |

---

## MOALS Quality Checklist

- [ ] Flywheel model defined with 4-6 self-reinforcing drivers
- [ ] At least 3 formal mechanisms documented (WBR, MBR, QBR minimum)
- [ ] Every key metric has a single-threaded owner
- [ ] Learning loop process defined with capture template
- [ ] North Star metric defined with supporting metric hierarchy
- [ ] Automation roadmap identifies current gaps and target state
- [ ] Operating cadence documented (weekly, monthly, quarterly, annual)
- [ ] Escalation paths clear for all critical metrics

---

## Integration Notes

- **Feeds into**: Metrics-SMART (operational metrics), Risk matrix (operational risks), Three Horizons (resource allocation tracking)
- **Depends on**: Business Model Canvas (what to measure), Persona-JTBD (customer metrics), Technical Hints (system architecture)
- **CQS Impact**: Improves Metrics (+4 pts) and Risk (+2 pts) scores through operational rigor

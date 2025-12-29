# Risk Assessment & Contingency Planning

> **Purpose**: Surface blockers early and define pivot criteria before building.

## Execution Risks

| Risk | Likelihood | Impact | L×I Score | Mitigation | Contingency |
|------|:----------:|:------:|:---------:|------------|-------------|
| [Risk 1] | [1-5] | [1-5] | [1-25] | [Proactive action] | [If it happens...] |
| [Risk 2] | [1-5] | [1-5] | [1-25] | [Proactive action] | [If it happens...] |
| [Risk 3] | [1-5] | [1-5] | [1-25] | [Proactive action] | [If it happens...] |
| [Risk 4] | [1-5] | [1-5] | [1-25] | [Proactive action] | [If it happens...] |
| [Risk 5] | [1-5] | [1-5] | [1-25] | [Proactive action] | [If it happens...] |

### Risk Scoring Guide
| Score | Likelihood | Impact |
|-------|------------|--------|
| 1 | Rare (<10%) | Negligible |
| 2 | Unlikely (10-30%) | Minor delay |
| 3 | Possible (30-50%) | Moderate setback |
| 4 | Likely (50-70%) | Major impact |
| 5 | Almost certain (>70%) | Project failure |

**Priority**: Address risks with L×I ≥ 12 first

---

## Risk Categories

### Technical Risks
| Risk | L×I | Status |
|------|:---:|:------:|
| Key dependency becomes unavailable/deprecated | [X] | [Mitigated/Open] |
| Performance doesn't meet requirements | [X] | [Mitigated/Open] |
| Integration complexity underestimated | [X] | [Mitigated/Open] |
| Security vulnerability in critical path | [X] | [Mitigated/Open] |

### Market Risks
| Risk | L×I | Status |
|------|:---:|:------:|
| Market timing shifts (too early/late) | [X] | [Mitigated/Open] |
| Competitor launches similar product | [X] | [Mitigated/Open] |
| Regulatory changes affect viability | [X] | [Mitigated/Open] |
| Target segment smaller than estimated | [X] | [Mitigated/Open] |

### Execution Risks
| Risk | L×I | Status |
|------|:---:|:------:|
| Wave 1 delays cascade to later waves | [X] | [Mitigated/Open] |
| Key team member unavailable | [X] | [Mitigated/Open] |
| Scope creep extends timeline 2x | [X] | [Mitigated/Open] |
| User adoption slower than expected | [X] | [Mitigated/Open] |

---

## Dependency Failure Scenarios

| Dependency | Type | If Unavailable... | Fallback | Cost of Fallback |
|------------|------|-------------------|----------|------------------|
| [Service/API] | External | [Impact on feature] | [Alternative] | [Effort/Time] |
| [Library/SDK] | Technical | [Impact on feature] | [Alternative] | [Effort/Time] |
| [Team/Skill] | Resource | [Impact on timeline] | [Alternative] | [Effort/Time] |
| [Data source] | Integration | [Impact on feature] | [Alternative] | [Effort/Time] |

### Critical Dependencies (No Fallback)
- [ ] [Dependency]: [Why no alternative exists] — **Must validate before Wave 1**
- [ ] [Dependency]: [Why no alternative exists] — **Must validate before Wave 1**

---

## Assumptions Register

| Assumption | If Wrong... | Validation Method | Validated? |
|------------|-------------|-------------------|:----------:|
| [Assumption 1] | [Consequence] | [How to test] | ✓/✗ |
| [Assumption 2] | [Consequence] | [How to test] | ✓/✗ |
| [Assumption 3] | [Consequence] | [How to test] | ✓/✗ |

**High-risk unvalidated assumptions**: [List assumptions that could invalidate project]

---

## Pivot Criteria

### Pivot Triggers
Define conditions that would cause a strategic pivot:

| Trigger | Threshold | Pivot Direction |
|---------|-----------|-----------------|
| User acquisition cost | > $[X] per user | [Narrower segment / Different channel] |
| User retention | < [X]% at 30 days | [Feature pivot / Persona pivot] |
| Technical feasibility | > [X] months delay | [Simpler MVP / Different approach] |
| Competitive pressure | [Condition] | [Differentiation pivot] |

### Pivot Decision Framework
```
IF [condition 1] AND [condition 2]
THEN pivot to [alternative direction]
ELSE continue current path
```

### Pivot Options (Pre-defined)
| Pivot Type | From | To | Trigger |
|------------|------|-----|---------|
| Segment pivot | [Current segment] | [New segment] | [When] |
| Feature pivot | [Current focus] | [New focus] | [When] |
| Channel pivot | [Current channel] | [New channel] | [When] |
| Technology pivot | [Current stack] | [New stack] | [When] |

---

## Kill Criteria

**Kill the project if**:
- [ ] [Condition that proves thesis fundamentally invalid]
- [ ] [Condition that proves thesis fundamentally invalid]
- [ ] [Condition that makes project economically unviable]

### Kill Decision Process
1. **Data review**: [Who reviews kill criteria metrics]
2. **Discussion**: [Forum for kill decision]
3. **Decision maker**: [Who has final authority]
4. **Communication**: [How to communicate kill decision]

---

## Risk Monitoring

| Risk Category | Review Frequency | Owner | Escalation Path |
|---------------|-----------------|-------|-----------------|
| Technical | [Weekly/Bi-weekly] | [Role] | [Who to escalate to] |
| Market | [Monthly] | [Role] | [Who to escalate to] |
| Execution | [Weekly] | [Role] | [Who to escalate to] |

### Early Warning Indicators
| Indicator | Yellow Threshold | Red Threshold | Action |
|-----------|-----------------|---------------|--------|
| [Metric] | [Warning level] | [Critical level] | [Response] |
| [Metric] | [Warning level] | [Critical level] | [Response] |

# Migration Risk Assessment Matrix

> **Purpose**: Identify and mitigate migration-specific risks before execution.
> **Risk ID Format**: `RISK-MIG-xxx` (e.g., RISK-MIG-001)

## Migration Risk Categories

| Category | Focus Areas | Examples |
|----------|-------------|----------|
| **Technical** | Data loss, downtime, performance regression | Schema incompatibility, data corruption, API breaking changes |
| **Operational** | Team skills, process changes | Training gaps, runbook gaps, tooling unfamiliarity |
| **Business** | Revenue impact, customer disruption | SLA violations, feature unavailability, user churn |
| **Schedule** | Timeline overrun, dependency delays | Resource conflicts, blocked dependencies, scope creep |

## Probability Scale (1-5)

| Score | Level | Probability | Description |
|:-----:|-------|:-----------:|-------------|
| 1 | Rare | <10% | Exceptional circumstances only |
| 2 | Unlikely | 10-25% | Could occur but not expected |
| 3 | Possible | 25-50% | Reasonable chance of occurrence |
| 4 | Likely | 50-75% | More likely than not |
| 5 | Almost Certain | >75% | Expected to occur |

## Impact Scale (1-5)

| Score | Level | Data | Downtime | Revenue | Customer |
|:-----:|-------|------|----------|---------|----------|
| 1 | Minimal | No loss | <5 min | None | Unnoticed |
| 2 | Minor | Recoverable | <1 hour | <$1K | Few affected |
| 3 | Moderate | Partial loss | 1-4 hours | $1K-$10K | Some disruption |
| 4 | Major | Significant loss | 4-24 hours | $10K-$100K | Major disruption |
| 5 | Critical | Unrecoverable | >24 hours | >$100K | Mass exodus |

## Risk Matrix (Probability x Impact)

```
IMPACT →   1-Min   2-Minor  3-Mod   4-Major  5-Crit
PROB ↓   ┌───────┬───────┬───────┬───────┬───────┐
5-Cert   │   5   │  10   │  15   │  20   │  25   │
         │ 🟡    │ 🟠    │ 🔴    │ 🔴    │ 🔴    │
4-Like   ├───────┼───────┼───────┼───────┼───────┤
         │   4   │   8   │  12   │  16   │  20   │
         │ 🟢    │ 🟡    │ 🟠    │ 🔴    │ 🔴    │
3-Poss   ├───────┼───────┼───────┼───────┼───────┤
         │   3   │   6   │   9   │  12   │  15   │
         │ 🟢    │ 🟡    │ 🟡    │ 🟠    │ 🔴    │
2-Unli   ├───────┼───────┼───────┼───────┼───────┤
         │   2   │   4   │   6   │   8   │  10   │
         │ 🟢    │ 🟢    │ 🟡    │ 🟡    │ 🟠    │
1-Rare   ├───────┼───────┼───────┼───────┼───────┤
         │   1   │   2   │   3   │   4   │   5   │
         │ 🟢    │ 🟢    │ 🟢    │ 🟢    │ 🟡    │
         └───────┴───────┴───────┴───────┴───────┘
```

| Zone | Score | Action |
|------|:-----:|--------|
| 🟢 Low | 1-4 | Monitor; accept with documentation |
| 🟡 Medium | 5-9 | Mitigate; active monitoring required |
| 🟠 High | 10-15 | Mitigate urgently; escalate to stakeholders |
| 🔴 Critical | 16-25 | Block migration until resolved |

## Mitigation Strategies by Risk Type

### Technical Risks
| Risk ID | Risk | Mitigation | Contingency |
|---------|------|------------|-------------|
| RISK-MIG-001 | Data loss during transfer | Checksums, parallel writes, verified backups | Rollback from backup |
| RISK-MIG-002 | Extended downtime | Blue-green deployment, feature flags | Immediate rollback |
| RISK-MIG-003 | Performance regression | Load testing pre-migration, capacity buffer | Scale up or rollback |
| RISK-MIG-004 | Schema incompatibility | Schema diff analysis, transformation scripts | Manual data patching |

### Operational Risks
| Risk ID | Risk | Mitigation | Contingency |
|---------|------|------------|-------------|
| RISK-MIG-005 | Team skill gaps | Training before migration, pair execution | On-call expert support |
| RISK-MIG-006 | Runbook gaps | Dry runs in staging, documented procedures | Escalation to senior engineer |
| RISK-MIG-007 | Tooling failures | Tool validation, backup tooling | Manual procedures |

### Business Risks
| Risk ID | Risk | Mitigation | Contingency |
|---------|------|------------|-------------|
| RISK-MIG-008 | SLA violation | Maintenance window, customer notification | SLA credits, fast rollback |
| RISK-MIG-009 | Revenue loss | Off-peak timing, phased rollout | Immediate rollback |
| RISK-MIG-010 | Customer churn | Communication plan, support readiness | Proactive outreach |

### Schedule Risks
| Risk ID | Risk | Mitigation | Contingency |
|---------|------|------------|-------------|
| RISK-MIG-011 | Timeline overrun | Buffer time, parallel workstreams | Scope reduction |
| RISK-MIG-012 | Dependency delays | Early dependency validation, alternatives | Delayed migration |
| RISK-MIG-013 | Resource conflicts | Resource booking, backup personnel | Timeline adjustment |

## Risk Register Template

| Risk ID | Category | Description | P | I | Score | Owner | Mitigation | Status |
|---------|----------|-------------|:-:|:-:|:-----:|-------|------------|:------:|
| RISK-MIG-xxx | [Tech/Ops/Bus/Sched] | [Description] | [1-5] | [1-5] | [P*I] | [Name] | [Action] | [Open/Mitigated] |

**Priority**: Address risks with Score >= 12 before migration approval.

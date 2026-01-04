# Rollback Strategy Template

## ROLLBACK_TRIGGERS

| Trigger | Threshold | Detection Method |
|---------|-----------|------------------|
| Error Rate | >5% for 5 minutes | APM alerts, error tracking |
| Latency Degradation | p99 > 2x baseline | Metrics dashboard, SLO breach |
| Data Integrity | Any corruption detected | Consistency checks, audit logs |
| Manual Trigger | Operator decision | On-call escalation, war room |

## ROLLBACK_TYPES

### Immediate (Traffic Routing)
- Switch load balancer to previous version
- Duration: <1 minute
- Use when: Critical errors, security issues

### Gradual (Reverse Traffic Shift)
- Incrementally route traffic back: 90% → 50% → 10% → 0% new
- Duration: 10-30 minutes
- Use when: Performance degradation, partial failures

### Full (Revert All Changes + Restore Data)
- Revert code deployment + restore database state
- Duration: 30-60 minutes
- Use when: Data corruption, schema incompatibility

## ROLLBACK_CHECKLIST

### Pre-Rollback
- [ ] Confirm rollback trigger condition met
- [ ] Notify stakeholders (Slack, PagerDuty)
- [ ] Capture current state for post-mortem

### During Rollback
- [ ] Execute rollback procedure per type selected
- [ ] Monitor error rates and latency in real-time
- [ ] Verify traffic routing to stable version

### Post-Rollback
- [ ] Confirm system stability (5-min observation)
- [ ] Update status page / incident channel
- [ ] Schedule post-rollback analysis

## DATA_ROLLBACK_STRATEGY

| Method | RPO | Use Case |
|--------|-----|----------|
| Point-in-Time Recovery | <5 min | Database-level rollback |
| Transaction Log Replay | <1 min | Undo specific transactions |
| Backup Restore | <24 hr | Full disaster recovery |

### Execution Steps
1. Identify last known good state timestamp
2. Stop writes to affected tables/services
3. Execute recovery method
4. Validate data integrity checksums
5. Resume normal operations

## ROLLBACK_VALIDATION

- [ ] Health checks pass on all instances
- [ ] Error rate returned to baseline (<0.1%)
- [ ] Latency metrics within SLO
- [ ] Data consistency verified
- [ ] Dependent services functional
- [ ] User-facing flows tested (smoke tests)

## POST_ROLLBACK_ANALYSIS

### Incident Summary
- **Rollback Time**: [timestamp]
- **Trigger**: [error rate | latency | data | manual]
- **Duration**: [minutes from detection to stable]

### Root Cause
- What failed:
- Why detection took [X] minutes:
- Contributing factors:

### Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| Fix root cause | | |
| Improve detection | | |
| Update runbook | | |

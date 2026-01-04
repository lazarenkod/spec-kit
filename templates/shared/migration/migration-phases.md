# Migration Phases Template

## Phase ID Format

**MIG-xxx** (e.g., MIG-001, MIG-002, MIG-003)

Sequential numbering within a migration project. IDs are immutable once assigned.

---

## Phase Template

```markdown
### MIG-xxx: [Phase Name]

| Attribute        | Value                                      |
|------------------|--------------------------------------------|
| **Pattern**      | Strangler Fig / Big Bang / Parallel Run    |
| **Duration**     | X weeks                                    |
| **Risk Level**   | LOW / MEDIUM / HIGH                        |
| **Effort**       | X story points                             |
| **Status**       | PLANNED                                    |
| **Owner**        | @team-or-individual                        |

#### Modules Affected

- `module-a` — Brief description of changes
- `module-b` — Brief description of changes

#### Steps

1. Step one description
2. Step two description
3. Step three description

#### Success Metrics

- [ ] Metric 1 (measurable, with threshold)
- [ ] Metric 2 (measurable, with threshold)
- [ ] Metric 3 (measurable, with threshold)

#### Rollback Strategy

See [rollback-strategy.md](./rollback-strategy.md#MIG-xxx) for detailed procedure.

- **Trigger**: Conditions that initiate rollback
- **RTO**: X hours
- **Data Recovery**: Approach for data consistency

#### Dependencies

- `MIG-xxx` — Must complete before this phase starts
- `MIG-yyy` — Can run in parallel with coordination
```

---

## Phase Status Values

| Status         | Description                                      |
|----------------|--------------------------------------------------|
| `PLANNED`      | Phase defined, not yet started                   |
| `IN_PROGRESS`  | Active migration work underway                   |
| `VALIDATING`   | Migration complete, running verification checks  |
| `COMPLETED`    | All success metrics met, phase signed off        |
| `ROLLED_BACK`  | Phase reverted due to failure or issues          |

---

## Phase Sequencing Rules

1. **Dependency Graph**: Phases form a DAG (Directed Acyclic Graph)
2. **Critical Path**: Identify longest dependency chain for timeline planning
3. **Parallel Execution**: Independent phases may run concurrently
4. **Gate Reviews**: Each phase requires sign-off before dependents start
5. **Buffer Time**: Add 20% buffer between dependent phases for issues

---

## Example Phase

### MIG-001: Authentication Service Migration

| Attribute        | Value                                      |
|------------------|--------------------------------------------|
| **Pattern**      | Strangler Fig                              |
| **Duration**     | 3 weeks                                    |
| **Risk Level**   | HIGH                                       |
| **Effort**       | 21 story points                            |
| **Status**       | IN_PROGRESS                                |
| **Owner**        | @platform-team                             |

#### Modules Affected

- `auth-legacy` — Deprecate OAuth 1.0 endpoints
- `auth-service` — Deploy OAuth 2.0 + OIDC provider
- `api-gateway` — Route splitting between old/new auth

#### Steps

1. Deploy new auth service alongside legacy system
2. Configure API gateway for gradual traffic shifting (10% → 50% → 100%)
3. Migrate user sessions with zero-downtime token exchange
4. Deprecate legacy endpoints after 2-week observation period

#### Success Metrics

- [ ] P99 auth latency < 100ms (baseline: 250ms)
- [ ] Zero authentication failures during cutover
- [ ] 100% of active sessions migrated within 24 hours
- [ ] Legacy endpoint traffic reduced to 0%

#### Rollback Strategy

See [rollback-strategy.md](./rollback-strategy.md#MIG-001) for detailed procedure.

- **Trigger**: Auth failure rate > 0.1% or latency P99 > 500ms
- **RTO**: 15 minutes
- **Data Recovery**: Session tokens remain valid in both systems during transition

#### Dependencies

- `MIG-000` — Infrastructure provisioning must complete first
- `MIG-002` — User data migration can run in parallel

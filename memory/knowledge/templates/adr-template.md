# Architecture Decision Record (ADR) Template

> **Purpose**: Document significant architectural decisions with context, rationale, and consequences.
> **When to Use**: Any decision that affects the system's structure, technology choices, or non-functional requirements.
> **Reference**: Based on Michael Nygard's original ADR format, enhanced with FAANG practices.

---

## ADR-[NUMBER]: [TITLE]

**Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

**Date**: YYYY-MM-DD

**Decision Makers**: [Names/Roles]

**Technical Area**: [Infrastructure | Data | Security | API | Frontend | Backend | DevOps | Integration]

**Linked Requirements**:
- **Functional**: FR-xxx, FR-yyy — [How this decision satisfies them]
- **Non-Functional**: NFR-xxx — [How this decision achieves them]

---

## Context

### Problem Statement
[1-2 sentences describing the problem or need that drove this decision]

### Current State
[Brief description of how things work now, if applicable]

### Constraints
- **Technical**: [e.g., Must integrate with existing PostgreSQL database]
- **Business**: [e.g., Must launch before Q2]
- **Regulatory**: [e.g., Must comply with GDPR]
- **Resources**: [e.g., Team has no Go experience]

### Requirements
| Requirement | Priority | Notes |
|-------------|----------|-------|
| [Requirement 1] | Must Have | |
| [Requirement 2] | Should Have | |
| [Requirement 3] | Nice to Have | |

---

## Decision Drivers

1. **[Driver 1]**: [Why this matters]
2. **[Driver 2]**: [Why this matters]
3. **[Driver 3]**: [Why this matters]

*Priority order: [1] > [2] > [3]*

---

## Options Considered

### Option 1: [Name] ⭐ CHOSEN

**Description**: [What this option entails]

**Pros**:
- ✅ [Advantage 1]
- ✅ [Advantage 2]

**Cons**:
- ❌ [Disadvantage 1]
- ❌ [Disadvantage 2]

**Effort**: [Low | Medium | High]

**Risk Level**: [Low | Medium | High]

---

### Option 2: [Name]

**Description**: [What this option entails]

**Pros**:
- ✅ [Advantage 1]
- ✅ [Advantage 2]

**Cons**:
- ❌ [Disadvantage 1]
- ❌ [Disadvantage 2]

**Why Not Chosen**: [Specific reason]

---

### Option 3: [Name]

**Description**: [What this option entails]

**Pros**:
- ✅ [Advantage 1]

**Cons**:
- ❌ [Disadvantage 1]
- ❌ [Disadvantage 2]

**Why Not Chosen**: [Specific reason]

---

## Decision

**We will**: [Clear statement of what we decided to do]

**Rationale**: [Why this option best addresses our decision drivers]

---

## Consequences

### Positive
- ✅ [Benefit 1]
- ✅ [Benefit 2]

### Negative
- ⚠️ [Tradeoff 1] — **Mitigation**: [How we'll address this]
- ⚠️ [Tradeoff 2] — **Mitigation**: [How we'll address this]

### Neutral
- ➡️ [Change that is neither positive nor negative]

---

## Implementation

### Phases
| Phase | Scope | Timeline | Owner |
|-------|-------|----------|-------|
| 1 | [Minimal implementation] | [Timeframe] | [Team/Person] |
| 2 | [Extension] | [Timeframe] | [Team/Person] |

### Migration Strategy
[If replacing existing system, how will migration happen?]

### Rollback Plan
[What happens if this doesn't work? How do we revert?]

---

## Validation

### Success Metrics
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| [Metric 1] | [Baseline] | [Goal] | [How to measure] |
| [Metric 2] | [Baseline] | [Goal] | [How to measure] |

### Fitness Functions
```
# Automated checks to validate architecture compliance

[ ] [Check 1]: [Description]
    - Tool: [e.g., ArchUnit, dependency-cruiser]
    - Threshold: [e.g., < 10ms latency]

[ ] [Check 2]: [Description]
    - Tool: [Tool name]
    - Threshold: [Threshold]
```

### Review Schedule
- **Initial Review**: [Date, 30 days after implementation]
- **Periodic Review**: [Frequency, e.g., Quarterly]

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-XXX | Supersedes | |
| ADR-XXX | Depends on | |
| ADR-XXX | Related to | |

---

## References

- [Link to relevant documentation]
- [Link to proof of concept]
- [Link to benchmarks]

---

## Appendix

### Comparison Matrix

| Criteria | Weight | Option 1 | Option 2 | Option 3 |
|----------|--------|----------|----------|----------|
| [Criteria 1] | 30% | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| [Criteria 2] | 25% | ⭐⭐ | ⭐⭐⭐ | ⭐ |
| [Criteria 3] | 25% | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| [Criteria 4] | 20% | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Weighted Score** | | **X.X** | **X.X** | **X.X** |

### Glossary
- **[Term 1]**: [Definition]
- **[Term 2]**: [Definition]

---

# Example: ADR-001 API Gateway Selection

**Status**: Accepted

**Date**: 2024-01-15

**Decision Makers**: Platform Team, Security Lead

**Technical Area**: Infrastructure

**Linked Requirements**:
- **Functional**: FR-012 (API Gateway), FR-015 (Auth centralization)
- **Non-Functional**: NFR-PERF-003 (< 5ms latency), NFR-SEC-001 (Centralized auth)

---

## Context

### Problem Statement
Our microservices need a unified entry point for authentication, rate limiting, and request routing.

### Current State
Each service handles its own authentication, leading to inconsistent security and duplicate code.

### Constraints
- **Technical**: Must support gRPC and REST
- **Business**: Budget < $5000/month for managed solutions
- **Resources**: Team familiar with Go and Kubernetes

### Requirements
| Requirement | Priority | Notes |
|-------------|----------|-------|
| JWT validation | Must Have | OAuth 2.0 + OIDC |
| Rate limiting | Must Have | Per-client quotas |
| Request transformation | Should Have | Header injection |
| WebSocket support | Nice to Have | For real-time features |

---

## Decision Drivers

1. **Security**: Centralized auth reduces attack surface
2. **Developer Experience**: Easy configuration and debugging
3. **Performance**: < 5ms latency overhead

---

## Options Considered

### Option 1: Kong Gateway ⭐ CHOSEN

**Description**: Open-source API gateway with enterprise features.

**Pros**:
- ✅ Rich plugin ecosystem (auth, rate limiting, logging)
- ✅ Kubernetes-native with Ingress Controller
- ✅ Active community, good documentation

**Cons**:
- ❌ Lua plugins have learning curve
- ❌ Enterprise features require license

**Effort**: Medium

**Risk Level**: Low

---

### Option 2: AWS API Gateway

**Pros**:
- ✅ Fully managed, no ops overhead
- ✅ Native AWS integration

**Cons**:
- ❌ $3.50/million requests (expensive at scale)
- ❌ Vendor lock-in
- ❌ Cold start latency

**Why Not Chosen**: Cost prohibitive at projected 100M+ requests/month

---

### Option 3: Build Custom

**Pros**:
- ✅ Full control

**Cons**:
- ❌ 3-6 months development time
- ❌ Ongoing maintenance burden
- ❌ Security risk from custom code

**Why Not Chosen**: Not our core competency, reinventing the wheel

---

## Decision

**We will**: Deploy Kong Gateway on Kubernetes using the Ingress Controller.

**Rationale**: Best balance of features, cost, and team familiarity with Kubernetes.

---

## Consequences

### Positive
- ✅ Unified authentication across all services
- ✅ Centralized rate limiting and monitoring
- ✅ Reduced code duplication in services

### Negative
- ⚠️ New technology for team — **Mitigation**: 2-day training session
- ⚠️ Single point of failure — **Mitigation**: Multi-zone deployment with health checks

---

## Implementation

### Phases
| Phase | Scope | Timeline | Owner |
|-------|-------|----------|-------|
| 1 | Deploy Kong, migrate auth service | 2 weeks | Platform Team |
| 2 | Migrate remaining services | 4 weeks | Service Teams |

### Rollback Plan
Keep existing auth code in services for 30 days. Feature flag to route traffic back to direct service calls.

---

## Validation

### Success Metrics
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| Auth latency | N/A | < 5ms p99 | Prometheus + Grafana |
| Security incidents | 2/quarter | 0/quarter | Security dashboard |

### Fitness Functions
```
[x] Latency Check: p99 latency < 10ms
    - Tool: Prometheus alerting
    - Threshold: Alert if > 10ms for 5 minutes

[x] Security Scan: No critical vulnerabilities
    - Tool: Trivy container scanning
    - Threshold: 0 critical, < 5 high
```

---

## References

- [Kong Documentation](https://docs.konghq.com)
- [PoC Results](link-to-internal-doc)
- [Cost Analysis Spreadsheet](link-to-spreadsheet)

---

# ADR Quality Checklist

Before finalizing an ADR, verify:

## Content
- [ ] Problem statement is clear and specific
- [ ] At least 3 options were seriously considered
- [ ] Pros and cons are balanced (not biased toward chosen option)
- [ ] Decision drivers are prioritized
- [ ] Consequences include both positive AND negative
- [ ] Mitigations are defined for negative consequences

## Actionability
- [ ] Implementation phases are defined
- [ ] Success metrics are measurable
- [ ] Rollback plan exists
- [ ] Review schedule is set

## Context
- [ ] Constraints are explicitly stated
- [ ] Related ADRs are linked
- [ ] References include evidence (benchmarks, PoCs)

## Clarity
- [ ] Non-experts can understand the decision
- [ ] Technical jargon is defined in glossary
- [ ] Diagrams or comparison matrices clarify complex points

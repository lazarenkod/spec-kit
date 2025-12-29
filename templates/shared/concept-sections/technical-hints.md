# Technical Discovery Hints

> **Purpose**: Surface architectural considerations early to reduce surprises during planning.

## Domain Entities (Sketch)

| Entity | Key Attributes | Relationships | Persistence | Notes |
|--------|----------------|---------------|-------------|-------|
| User | id, email, role, created_at | → Account, → Sessions | PostgreSQL | [Auth system integration] |
| [Entity] | [key attrs] | [→ Related entities] | [Store] | [Notes] |
| [Entity] | [key attrs] | [→ Related entities] | [Store] | [Notes] |
| [Entity] | [key attrs] | [→ Related entities] | [Store] | [Notes] |
| [Entity] | [key attrs] | [→ Related entities] | [Store] | [Notes] |

### Entity Relationships Diagram (ASCII)
```
┌──────────┐     ┌──────────┐     ┌──────────┐
│   User   │────→│  Account │←────│  [Entity]│
└──────────┘     └──────────┘     └──────────┘
      │                │
      ▼                ▼
┌──────────┐     ┌──────────┐
│ Sessions │     │ [Entity] │
└──────────┘     └──────────┘
```

### Data Considerations
- **PII fields**: [Which entities contain personal data]
- **High-volume entities**: [Which entities will have most records]
- **Audit requirements**: [Which entities need change tracking]
- **Soft delete candidates**: [Which entities should never hard delete]

---

## API Surface Estimation

| Domain | Operations | Auth Required | Rate Limited | External Integration |
|--------|------------|:-------------:|:------------:|---------------------|
| Users | CRUD, search, bulk | ✓ | ✓ | SSO providers |
| [Domain] | [ops] | ✓/✗ | ✓/✗ | [integrations] |
| [Domain] | [ops] | ✓/✗ | ✓/✗ | [integrations] |
| [Domain] | [ops] | ✓/✗ | ✓/✗ | [integrations] |

### API Complexity Estimate
| Complexity | Count | Examples |
|------------|:-----:|----------|
| Simple CRUD | [X] | [List endpoints] |
| Complex queries | [X] | [List endpoints] |
| Real-time/WebSocket | [X] | [List endpoints] |
| External integrations | [X] | [List endpoints] |
| Background jobs | [X] | [List jobs] |

**Total estimated endpoints**: [X] (rough order of magnitude)

---

## Integration Complexity

| External System | Protocol | Auth Method | Complexity | Risk | Notes |
|-----------------|----------|-------------|:----------:|:----:|-------|
| [System/API] | REST/GraphQL/gRPC | OAuth/API Key/JWT | Low/Med/High | [Notes] | [Documentation quality] |
| [System/API] | REST/GraphQL/gRPC | OAuth/API Key/JWT | Low/Med/High | [Notes] | [Documentation quality] |
| [System/API] | REST/GraphQL/gRPC | OAuth/API Key/JWT | Low/Med/High | [Notes] | [Documentation quality] |

### Integration Risk Factors
| Factor | [System 1] | [System 2] | [System 3] |
|--------|:----------:|:----------:|:----------:|
| Documentation quality | Good/Fair/Poor | Good/Fair/Poor | Good/Fair/Poor |
| Sandbox/test environment | ✓/✗ | ✓/✗ | ✓/✗ |
| Rate limits | [Limit] | [Limit] | [Limit] |
| SLA/uptime | [%] | [%] | [%] |
| Vendor lock-in risk | Low/Med/High | Low/Med/High | Low/Med/High |

---

## State Management Hints

| State Type | Scope | Persistence | Sync Strategy |
|------------|-------|-------------|---------------|
| User session | Client + Server | Session storage + DB | [JWT / Cookie] |
| UI state | Client | Memory / localStorage | [Redux / Zustand / Context] |
| Application data | Server | Database | [REST / GraphQL / Real-time] |
| Cache | Both | Memory / Redis | [Invalidation strategy] |

### State Complexity Indicators
- [ ] Multi-tab synchronization needed
- [ ] Offline-first requirements
- [ ] Real-time collaboration features
- [ ] Optimistic updates required
- [ ] Complex undo/redo requirements

---

## Constitution Principle Conflicts

| Feature | Principle | Potential Conflict | Resolution |
|---------|-----------|-------------------|------------|
| [Feature name] | SEC-001 | [What might conflict] | [How to resolve] |
| [Feature name] | [Principle ID] | [What might conflict] | [How to resolve] |
| [Feature name] | [Principle ID] | [What might conflict] | [How to resolve] |

### Principles Requiring Attention
- [ ] **[Principle ID]**: [Feature X] may violate [aspect] — needs design review
- [ ] **[Principle ID]**: [Feature Y] may violate [aspect] — needs design review

---

## Technical Debt Forecast

| Category | Likely Debt | Why | Payback Priority |
|----------|-------------|-----|:----------------:|
| Architecture | [What shortcuts we'll take] | [Time/resource constraint] | [P0/P1/P2] |
| Testing | [What we'll under-test] | [Speed to market] | [P0/P1/P2] |
| Documentation | [What won't be documented] | [Iteration speed] | [P0/P1/P2] |
| Performance | [What won't be optimized] | [Premature optimization] | [P0/P1/P2] |

---

## Infrastructure Requirements (Rough)

| Component | Wave 1 | Wave 2 | Wave 3+ | Notes |
|-----------|--------|--------|---------|-------|
| Compute | [Size/type] | [Size/type] | [Size/type] | [Scaling strategy] |
| Database | [Type/size] | [Type/size] | [Type/size] | [Scaling strategy] |
| Storage | [Type/size] | [Type/size] | [Type/size] | [Growth estimate] |
| CDN/Edge | [Needed?] | [Needed?] | [Needed?] | [Regions] |
| Queue/Workers | [Needed?] | [Needed?] | [Needed?] | [Job types] |

### Cost Estimate (Order of Magnitude)
| Phase | Monthly Cost | Key Drivers |
|-------|-------------|-------------|
| Development | $[X] | [Main cost drivers] |
| MVP Launch | $[X] | [Main cost drivers] |
| Scale (1K users) | $[X] | [Main cost drivers] |
| Scale (10K users) | $[X] | [Main cost drivers] |

---

## Security Considerations (Early)

| Concern | Applies? | Notes |
|---------|:--------:|-------|
| Authentication (users) | ✓/✗ | [SSO? MFA? Passwordless?] |
| Authorization (RBAC/ABAC) | ✓/✗ | [Role model complexity] |
| Data encryption at rest | ✓/✗ | [Which data?] |
| Data encryption in transit | ✓/✗ | [TLS everywhere?] |
| PII handling | ✓/✗ | [GDPR? CCPA? Other?] |
| Audit logging | ✓/✗ | [What actions?] |
| Rate limiting | ✓/✗ | [Which endpoints?] |
| Input validation | ✓/✗ | [Sanitization needs] |

### Compliance Requirements
- [ ] **GDPR**: [If handling EU user data]
- [ ] **SOC 2**: [If enterprise customers]
- [ ] **HIPAA**: [If healthcare data]
- [ ] **PCI-DSS**: [If handling payments]
- [ ] **[Other]**: [Industry-specific]

# Enterprise Constitution (Layer 0)

**Version**: 1.1
**Status**: READ-ONLY (shipped with Spec Kit)
**Purpose**: Universal enterprise principles that apply to 95%+ of professional software projects

---

## How This Works

This is **Layer 0** of the layered constitution system:

```
Layer 0: constitution.base.md (this file) - Enterprise defaults, READ-ONLY
    ↓ extends
Layer 1: constitution.domain.md - Domain-specific (fintech, healthcare, etc.)
    ↓ extends
Layer 2: constitution.md - Project-specific overrides
```

**Inheritance Rules**:
- Higher layers INHERIT all principles from lower layers
- Higher layers can STRENGTHEN (SHOULD → MUST) but NEVER weaken (MUST → SHOULD)
- Higher layers can ADD new principles
- Higher layers can REFINE parameters (e.g., coverage 80% → 90%)

---

## Principle Format

Each principle follows this structure:

```
### [ID]: [Name]

**Level**: MUST | SHOULD
**Applies to**: [scope]

[Description with rationale]

**Validation**: [How to verify compliance]
**Violations**: [What happens if violated in /analyze]
```

- **MUST** = Non-negotiable. Violations are CRITICAL severity, block implementation.
- **SHOULD** = Strongly recommended. Violations are MEDIUM severity, require justification.

---

## SEC: Security

### SEC-001: No Hardcoded Secrets

**Level**: MUST
**Applies to**: All code, configuration, scripts

Credentials, API keys, tokens, passwords, and connection strings MUST be loaded from environment variables, secret managers, or encrypted configuration. Never commit secrets to version control.

**Validation**: Grep for common patterns (password=, api_key=, secret=, token=) in code
**Violations**: CRITICAL - Security breach risk

---

### SEC-002: Input Validation

**Level**: MUST
**Applies to**: All external inputs (HTTP, CLI, files, databases)

All external input MUST be validated, sanitized, and typed before processing. Validation MUST occur at system boundaries, not deep in business logic.

**Validation**: Review input handlers for validation logic
**Violations**: CRITICAL - Injection attack vector

---

### SEC-003: Output Encoding

**Level**: MUST
**Applies to**: All output (HTML, SQL, JSON, XML, shell)

All output MUST be encoded appropriately for its context. HTML must be escaped, SQL must use parameterized queries, shell commands must escape arguments.

**Validation**: Review output generation for encoding
**Violations**: CRITICAL - XSS/injection attack vector

---

### SEC-004: Dependency Security

**Level**: MUST
**Applies to**: All third-party dependencies

Dependencies MUST be scanned for known vulnerabilities. Updates for critical CVEs MUST be applied within SLA (typically 7 days for critical, 30 days for high).

**Validation**: Check for dependency scanning in CI/CD
**Violations**: CRITICAL - Known vulnerability exposure

---

### SEC-005: Authentication Required

**Level**: MUST
**Applies to**: All non-public endpoints and resources

All non-public endpoints MUST require authentication. Anonymous access MUST be explicitly allowlisted and justified.

**Validation**: Review endpoint security configuration
**Violations**: CRITICAL - Unauthorized access risk

---

### SEC-006: Least Privilege

**Level**: SHOULD
**Applies to**: All components, services, users

Components SHOULD operate with minimum required permissions. Database users SHOULD have only necessary grants. Services SHOULD have only required IAM roles.

**Validation**: Review permission assignments
**Violations**: MEDIUM - Blast radius of compromise

---

### SEC-007: RBAC Authorization

**Level**: MUST
**Applies to**: All protected endpoints and resources

Every protected endpoint MUST perform authorization check before executing business logic. Role-Based Access Control (RBAC) MUST be enforced consistently. Authorization decisions MUST be logged.

**Validation**: Review middleware/decorator for auth checks on all protected routes
**Violations**: CRITICAL - Unauthorized access to protected resources

---

### SEC-008: SQL Injection Prevention

**Level**: MUST
**Applies to**: All database queries

All database queries MUST use parameterized queries or prepared statements. String concatenation for query building is FORBIDDEN. ORM usage MUST avoid raw query injection points.

**Validation**: Grep for string concatenation in SQL contexts
**Violations**: CRITICAL - Database compromise risk

---

## OBS: Observability

### OBS-001: Structured Logging

**Level**: MUST
**Applies to**: All services and applications

All logs MUST use structured format (JSON preferred) with:
- Timestamp (ISO 8601)
- Log level (ERROR, WARN, INFO, DEBUG)
- Correlation/Request ID
- Service name and version
- Contextual fields (user_id, resource_id, etc.)

**Validation**: Review logging configuration and sample logs
**Violations**: HIGH - Debugging and audit impaired

---

### OBS-002: Error Tracking

**Level**: MUST
**Applies to**: All production services

Unhandled exceptions and critical errors MUST be captured, reported, and alerted. Error tracking MUST include stack traces, context, and user impact.

**Validation**: Verify error tracking integration (Sentry, etc.)
**Violations**: HIGH - Silent failures in production

---

### OBS-003: Health Endpoints

**Level**: SHOULD
**Applies to**: All services

Services SHOULD expose health check endpoints:
- `/health` - Basic liveness check
- `/ready` - Readiness including dependencies

**Validation**: Verify health endpoints exist and are monitored
**Violations**: MEDIUM - Deployment and scaling impaired

---

### OBS-004: Performance Metrics

**Level**: SHOULD
**Applies to**: Critical paths and external calls

Key operations SHOULD emit timing metrics (latency, throughput). External calls SHOULD track success rate, latency percentiles, and error rates.

**Validation**: Review metrics collection configuration
**Violations**: LOW - Performance visibility limited

---

## ERR: Error Exposure

### ERR-001: No Stack Traces in Production

**Level**: MUST
**Applies to**: All production error responses

Stack traces, internal paths, and debugging information MUST NEVER be exposed to users in production. Error details MUST be logged server-side only. Production errors MUST return sanitized messages.

**Validation**: Review error handlers for production mode behavior
**Violations**: CRITICAL - Information disclosure, attack surface exposure

---

### ERR-002: Generic User-Facing Errors

**Level**: MUST
**Applies to**: All user-visible error messages

User-facing errors MUST be generic and non-technical (e.g., "Something went wrong. Please try again."). Internal error codes and correlation IDs MAY be shown for support purposes. Sensitive details (table names, field names, query fragments) MUST be hidden.

**Validation**: Review error message templates for user-facing contexts
**Violations**: HIGH - Information leakage, poor UX

---

### ERR-003: Correlation ID in All Errors

**Level**: MUST
**Applies to**: All logged errors

Every error MUST be logged with a correlation ID (request ID) that links to the user session. This ID SHOULD be displayed to users for support escalation. Correlation IDs MUST propagate across service boundaries.

**Validation**: Verify correlation ID middleware and error logging
**Violations**: HIGH - Debugging and support severely impaired

---

## QUA: Quality

### QUA-001: Unit Test Coverage

**Level**: SHOULD
**Applies to**: New and modified code

New code SHOULD maintain minimum 80% unit test coverage. Critical business logic SHOULD have 90%+ coverage. Coverage MUST NOT decrease without justification.

**Validation**: Check coverage reports in CI
**Violations**: MEDIUM - Regression risk

---

### QUA-002: Integration Testing

**Level**: SHOULD
**Applies to**: Critical user paths

Critical user paths SHOULD have integration tests that verify end-to-end behavior. Happy path and primary error cases SHOULD be covered.

**Validation**: Review integration test coverage
**Violations**: MEDIUM - Integration bugs slip through

---

### QUA-003: Code Review Required

**Level**: MUST
**Applies to**: All changes to main/production branches

All changes MUST be reviewed by at least one other team member before merge. Self-merges MUST be prohibited for non-emergency changes.

**Validation**: Check branch protection rules
**Violations**: HIGH - Quality and knowledge sharing impaired

---

### QUA-004: Documentation

**Level**: SHOULD
**Applies to**: Public APIs and complex logic

Public APIs SHOULD have documentation (OpenAPI, JSDoc, etc.). Complex algorithms and business rules SHOULD have explanatory comments.

**Validation**: Review documentation coverage
**Violations**: LOW - Maintainability reduced

---

### QUA-005: Technical Debt Tracking

**Level**: SHOULD
**Applies to**: All known issues and shortcuts

Known issues SHOULD be tracked as TODOs linked to tickets. Technical debt SHOULD be documented with context for future resolution.

**Validation**: Review TODO comments and debt backlog
**Violations**: LOW - Accumulating hidden debt

---

### QUA-006: Code Style Enforcement

**Level**: SHOULD
**Applies to**: All source code

Codebase SHOULD use automated linting and formatting tools. Style rules MUST be enforced in CI (lint errors fail build). Formatting SHOULD be auto-applied on save or pre-commit.

**Validation**: Check for linter config (.eslintrc, .prettierrc, ruff.toml, etc.)
**Violations**: LOW - Inconsistent style, review friction

---

### QUA-007: Integration Tests for APIs

**Level**: SHOULD
**Applies to**: All API endpoints

All API endpoints SHOULD have integration tests covering:
- Happy path (200/201 responses)
- Authentication failures (401)
- Authorization failures (403)
- Validation failures (400)
- Not found cases (404)

**Validation**: Review API test coverage
**Violations**: MEDIUM - API contract violations undetected

---

## REL: Reliability

### REL-001: Error Handling

**Level**: MUST
**Applies to**: All operations that can fail

All errors MUST be caught and handled appropriately. Errors MUST NOT be silently swallowed. Users MUST receive appropriate error messages.

**Validation**: Review error handling patterns
**Violations**: HIGH - Unpredictable behavior

---

### REL-002: Graceful Degradation

**Level**: SHOULD
**Applies to**: Services with external dependencies

Services SHOULD degrade gracefully when dependencies fail. Non-critical features SHOULD fail independently without blocking core functionality.

**Validation**: Review circuit breakers and fallback logic
**Violations**: MEDIUM - Cascading failures

---

### REL-003: Idempotency

**Level**: SHOULD
**Applies to**: Write operations, especially external calls

Write operations SHOULD be idempotent where possible. Retry-safe operations SHOULD use idempotency keys or natural idempotency.

**Validation**: Review mutation operations for idempotency
**Violations**: MEDIUM - Duplicate operations on retry

---

### REL-004: Transaction Boundaries

**Level**: MUST
**Applies to**: Database operations

Database operations that must be atomic MUST use explicit transaction boundaries. Transactions MUST NOT span network calls.

**Validation**: Review database access patterns
**Violations**: HIGH - Data inconsistency risk

---

### REL-005: Retry Policies

**Level**: SHOULD
**Applies to**: External service calls

External calls SHOULD implement retry with exponential backoff. Retries SHOULD respect rate limits and use jitter.

**Validation**: Review external call patterns
**Violations**: MEDIUM - Transient failure sensitivity

---

### REL-006: Optimistic Locking

**Level**: SHOULD
**Applies to**: Concurrent update scenarios

Entities subject to concurrent updates SHOULD use optimistic locking (version field/ETag). Conflicting updates MUST be detected and rejected with 409 Conflict. Users MUST be able to retry with fresh data.

**Validation**: Review data models for version/updatedAt fields
**Violations**: MEDIUM - Lost updates, data corruption

---

## API: API Design

### API-001: Versioning

**Level**: MUST
**Applies to**: All APIs (REST, GraphQL, gRPC)

APIs MUST be versioned using URL path (/v1/), header (Api-Version), or content negotiation. Version MUST be explicit, not implicit.

**Validation**: Check API versioning strategy
**Violations**: HIGH - Breaking changes affect clients

---

### API-002: Backwards Compatibility

**Level**: MUST
**Applies to**: Released APIs

Breaking changes MUST increment major version. Deprecations MUST be communicated with migration timeline. Old versions MUST be supported per SLA.

**Validation**: Review API change history
**Violations**: CRITICAL - Client breakage

---

### API-003: Rate Limiting

**Level**: SHOULD
**Applies to**: Public and partner APIs

Public APIs SHOULD implement rate limiting per client/user. Limits SHOULD be documented. Exceeded limits SHOULD return 429 with retry guidance.

**Validation**: Check rate limiting configuration
**Violations**: MEDIUM - DoS vulnerability, unfair usage

---

### API-004: Error Responses

**Level**: MUST
**Applies to**: All API error cases

API errors MUST return structured error objects with:
- Error code (machine-readable)
- Message (human-readable)
- Details (debugging context)
- Request ID (correlation)

**Validation**: Review error response format
**Violations**: HIGH - Poor developer experience

---

### API-005: API Specification

**Level**: SHOULD
**Applies to**: All REST/HTTP APIs

APIs SHOULD have machine-readable specification (OpenAPI 3.x, AsyncAPI). Specification SHOULD be auto-generated or validated against implementation. Documentation SHOULD be generated from specification.

**Validation**: Check for openapi.json/yaml in project
**Violations**: MEDIUM - Integration friction, documentation drift

---

### API-006: Pagination

**Level**: SHOULD
**Applies to**: List endpoints returning many items

List endpoints SHOULD implement pagination. Cursor-based pagination SHOULD be used for large/real-time datasets. Offset-based pagination MAY be used for stable, small datasets. Page size MUST have a maximum limit.

**Validation**: Review list endpoints for pagination implementation
**Violations**: MEDIUM - Performance issues, memory exhaustion

---

## PRF: Performance

### PRF-001: Response Time SLA

**Level**: SHOULD
**Applies to**: User-facing endpoints

API responses SHOULD complete within 500ms at p95. User-facing pages SHOULD achieve Core Web Vitals thresholds (LCP < 2.5s, FID < 100ms).

**Validation**: Check performance monitoring
**Violations**: MEDIUM - User experience degraded

---

### PRF-002: Resource Limits

**Level**: MUST
**Applies to**: All operations

Operations MUST have timeout limits. Memory-intensive operations MUST have size limits. Runaway processes MUST be prevented.

**Validation**: Review timeout and limit configuration
**Violations**: HIGH - Resource exhaustion risk

---

### PRF-003: Query Optimization

**Level**: SHOULD
**Applies to**: Database queries

Database queries SHOULD use appropriate indexes. N+1 query patterns SHOULD be avoided. Query performance SHOULD be monitored.

**Validation**: Review query plans and patterns
**Violations**: MEDIUM - Performance degradation

---

### PRF-004: Caching Strategy

**Level**: SHOULD
**Applies to**: Frequently accessed data

Repeated reads SHOULD use appropriate caching (memory, Redis, CDN). Cache invalidation strategy MUST be defined. Cache hit rates SHOULD be monitored.

**Validation**: Review caching implementation
**Violations**: LOW - Suboptimal performance

---

## CMP: Compliance

### CMP-001: Audit Logging

**Level**: MUST
**Applies to**: Security-relevant actions

Security-relevant actions MUST be audit logged:
- Authentication events (login, logout, failures)
- Authorization decisions (access granted/denied)
- Data modifications (create, update, delete)
- Administrative actions (config changes, user management)

Audit logs MUST be tamper-evident and retained per policy.

**Validation**: Review audit logging coverage
**Violations**: CRITICAL - Compliance and forensics impaired

---

### CMP-002: Data Retention

**Level**: SHOULD
**Applies to**: All stored data

Data SHOULD have defined retention policies. Expired data SHOULD be automatically purged. Legal hold capabilities SHOULD exist.

**Validation**: Review retention configuration
**Violations**: MEDIUM - Storage costs, legal exposure

---

### CMP-003: Privacy by Design

**Level**: SHOULD
**Applies to**: Personal and sensitive data

PII SHOULD be minimized (collect only what's needed). Sensitive data SHOULD be encrypted. Data access SHOULD be logged.

**Validation**: Review data handling practices
**Violations**: MEDIUM - Privacy risk

---

### CMP-004: Accessibility

**Level**: SHOULD
**Applies to**: User interfaces

UI SHOULD meet WCAG 2.1 AA standards:
- Keyboard navigation
- Screen reader support
- Color contrast ratios
- Focus indicators

**Validation**: Run accessibility audit tools
**Violations**: MEDIUM - Exclusion of users with disabilities

---

## Summary

| Domain | Principles | MUST | SHOULD |
|--------|------------|------|--------|
| SEC (Security) | 8 | 7 | 1 |
| OBS (Observability) | 4 | 2 | 2 |
| ERR (Error Exposure) | 3 | 3 | 0 |
| QUA (Quality) | 7 | 1 | 6 |
| REL (Reliability) | 6 | 2 | 4 |
| API (API Design) | 6 | 3 | 3 |
| PRF (Performance) | 4 | 1 | 3 |
| CMP (Compliance) | 4 | 1 | 3 |
| **Total** | **42** | **20** | **22** |

---

## Next Steps

To customize for your project:

1. **Select domain** (optional): Copy `domains/fintech.md` to `constitution.domain.md` if applicable
2. **Add project overrides**: Edit `constitution.md` to strengthen or add principles
3. **Run validation**: Use `/speckit.analyze` to check compliance

See `constitution.md` for project-specific customization.

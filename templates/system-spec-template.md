# [Component Name] System Specification

**Domain**: [auth | payments | users | api | ...]
**Status**: ACTIVE
**Last Updated**: [DATE]

---

## Overview

[Brief description of this system component - what it does and why it exists]

---

## Current Behavior

### [Scenario 1 - Happy Path]

[Description of primary behavior]

**Flow**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

### [Scenario 2 - Error Handling]

[Description of error handling behavior]

---

## API Contract

<!--
  Define the interface that other components depend on.
  For REST APIs: endpoints with request/response formats.
  For internal modules: function signatures and data contracts.

  IMPORTANT: Include version information for traceability and to prevent
  AI agents from hallucinating non-existent API methods.
-->

### Contract Version

**API Version**: [e.g., v1, 2024-12-18]
**Stability**: [STABLE | BETA | DEPRECATED]
**Sunset Date**: [date if deprecated, or N/A]
**Migration Guide**: [URL if deprecated, or N/A]

### External Dependencies

<!--
  Document external packages/services this component uses.
  Reference plan.md Dependency Registry where applicable.
-->

| Dependency | Version | Documentation | Purpose |
|------------|---------|---------------|---------|
| [package/API] | [version] | [docs URL] | [why used] |

### Endpoints / Functions

| Method | Path / Signature | Description | Since Version |
|--------|------------------|-------------|---------------|
| `POST` | `/api/v1/[resource]` | [What it does] | v1.0 |
| `GET`  | `/api/v1/[resource]/{id}` | [What it does] | v1.0 |

### Request/Response Formats

**[Endpoint/Function Name]** *(since v1.0)*:
```json
// Request
{
  "field": "type",          // required | optional
  "field2": "type"          // required | optional
}

// Response (200 OK)
{
  "field": "type"
}

// Error Response (4xx/5xx)
{
  "error": "string",
  "code": "ERROR_CODE",
  "details": {}             // optional
}
```

### Rate Limiting

| Endpoint Pattern | Limit | Window | Burst |
|------------------|-------|--------|-------|
| `/api/v1/*` | [n] req | [time] | [burst] |

### Authentication

**Method**: [Bearer Token | API Key | OAuth2 | Session | None]
**Scopes Required**: [list of scopes, or N/A]
**Documentation**: [auth docs URL, or internal reference]

---

## Business Rules

<!--
  Rules that MUST be enforced by this component.
  Reference constitution principles where applicable.
-->

| Rule ID | Description | Constitution Ref |
|---------|-------------|------------------|
| BR-001 | [Business rule] | [SEC-xxx or N/A] |
| BR-002 | [Business rule] | [REL-xxx or N/A] |

---

## Dependencies

<!--
  Other system specs this component depends on.
  Type: REQUIRES (hard dependency) | OPTIONAL (soft dependency)
-->

| Depends On | Type | Notes |
|------------|------|-------|
| `system/[domain]/[name].md` | REQUIRES | [Why needed] |
| `system/[domain]/[name].md` | OPTIONAL | [Why optional] |

---

## Dependents

<!--
  Other system specs that depend on THIS component.
  Auto-populated by /speckit.analyze --impact.
-->

| System Spec | Impact if Changed |
|-------------|-------------------|
| `system/[domain]/[name].md` | [What breaks if this changes] |

---

## Spec History

<!--
  Version history linking to feature specs that created/modified this system spec.
  Updated by /speckit.merge after each feature merge.

  Relationship column indicates how the feature relates to this system spec:
  - CREATES: Feature created this system spec from scratch
  - EXTENDS: Feature added new capability to existing spec
  - REFINES: Feature improved/modified existing behavior
  - FIXES: Feature corrected issues in this spec
  - DEPRECATES: Feature marked functionality for removal
  - MAINTENANCE: Manual update without feature (docs, clarifications)
-->

| Version | Feature | Relationship | Date | Author | Changes |
|---------|---------|--------------|------|--------|---------|
| 1.0 | [NNN-feature-name] | CREATES | [DATE] | [@author] | Initial creation |

---

## Test Coverage *(mandatory)*

<!--
  MANDATORY: Every system spec MUST have test coverage.
  Links Acceptance Scenario IDs (AS-xxx) from feature specs to test files.
  Validated by Pass W in /speckit.analyze.

  Status values:
  - ❌ Pending: Test not yet written
  - ⏭️ Skipped: Intentionally not tested (requires justification)
  - 🔄 In progress: Test being written
  - ✅ Passing: Test exists and passes
  - ❌ Failing: Test exists but fails
-->

### Scenario Coverage

| Scenario | AS-ID | Test File | Test Function | Status |
|----------|-------|-----------|---------------|--------|
| [Happy path: user login] | AS-1A | `tests/auth/login.test.ts` | `testLoginSuccess` | ❌ Pending |
| [Error: invalid credentials] | AS-1B | `tests/auth/login.test.ts` | `testLoginFailure` | ❌ Pending |
| [Edge case: rate limiting] | EC-001 | `tests/auth/ratelimit.test.ts` | `testRateLimitExceeded` | ❌ Pending |

### Coverage Metrics

<!--
  Auto-populated by /speckit.merge or manually updated.
  System spec is considered "covered" when Required Coverage >= 80%.
-->

| Metric | Count | Covered | Skipped | Coverage |
|--------|-------|---------|---------|----------|
| Scenarios (AS) | X | 0 | 0 | 0% |
| Edge Cases (EC) | X | 0 | 0 | 0% |
| **Total** | X | 0 | 0 | 0% |

**Required Coverage**: [e.g., 80% | 100% for security-critical]
**Last Verified**: [DATE]
**Verification Method**: [automated CI | manual | /speckit.analyze]

### Skipped Tests

<!--
  Justification for any scenario not covered by automated tests.
  Corresponds to [NO-TEST:] markers in tasks.md.
-->

| Scenario | Reason | Alternative Validation |
|----------|--------|------------------------|
| [example] | [e.g., "UI-only, no backend logic"] | Manual QA checklist |

---

## Related Specs

<!--
  Links to related system specs for navigation.
-->

- **Parent domain**: `system/[domain]/_index.md`
- **Related**: `system/[domain]/[related-name].md`

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
-->

### Endpoints / Functions

| Method | Path / Signature | Description |
|--------|------------------|-------------|
| `POST` | `/api/v1/[resource]` | [What it does] |
| `GET`  | `/api/v1/[resource]/{id}` | [What it does] |

### Request/Response Formats

**[Endpoint/Function Name]**:
```json
// Request
{
  "field": "type"
}

// Response
{
  "field": "type"
}
```

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
-->

| Version | Feature | Date | Author | Changes |
|---------|---------|------|--------|---------|
| 1.0 | [NNN-feature-name] | [DATE] | [@author] | Initial creation |

---

## Test Coverage

<!--
  Links to test files that validate this system spec.
  Auto-populated during implementation or manually maintained.
-->

| Scenario | Test File | Status |
|----------|-----------|--------|
| [Scenario from Current Behavior] | `tests/[path]/[file].test.ts` | [Pending/Passing/Failing] |

---

## Related Specs

<!--
  Links to related system specs for navigation.
-->

- **Parent domain**: `system/[domain]/_index.md`
- **Related**: `system/[domain]/[related-name].md`

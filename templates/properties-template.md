# Property-Based Testing Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`
**Generated**: [DATE]
**Source Spec**: `specs/[feature]/spec.md`
**Property Quality Score (PQS)**: XX.X / 100

---

## Executive Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total Properties | N | - | - |
| FR Coverage | XX% | >= 80% | PASS/FAIL |
| AS (Boundary) Coverage | XX% | >= 90% | PASS/FAIL |
| EC (Security) Coverage | XX% | >= 95% | PASS/FAIL |
| Type Diversity | N/6 | >= 3 | PASS/FAIL |
| Shrunk Examples | N | >= 3 | PASS/FAIL |
| EARS Transformation | XX% | >= 85% | PASS/FAIL |

**Recommendation**: [Ready for implementation | Improve coverage | Address gaps]

---

## Property Traceability Matrix

<!--
  Complete traceability from spec artifacts to properties to test files.
  Each property has:
  - Unique ID (PROP-NNN)
  - Type (inverse, idempotent, invariant, commutative, model_based, boundary)
  - Source artifacts (AS-xxx, EC-xxx, FR-xxx, NFR-xxx)
  - Formula (mathematical/logical)
  - Priority (P1 critical, P2 important, P3 optional)
  - Generated test files per language
-->

| PROP ID | Type | Source Artifacts | Formula | Priority | Test Files |
|---------|------|------------------|---------|----------|------------|
| PROP-001 | inverse | AS-1A, FR-001 | `delete(create(x)) == no_x` | P1 | `test_*.py`, `*.test.ts` |
| PROP-002 | invariant | NFR-PERF-001 | `forall req: latency < 200ms` | P1 | `test_*.py` |
| PROP-003 | boundary | EC-001 | `forall invalid: reject(x)` | P1 | `test_*.py`, `*.test.ts` |
| PROP-004 | idempotent | FR-002 | `f(f(x)) == f(x)` | P2 | `test_*.py` |

---

## EARS Intermediate Representation

<!--
  EARS (Easy Approach to Requirements Syntax) transformations.
  Each spec artifact is transformed to one of:
  - UBIQUITOUS: "The system SHALL [action]"
  - EVENT-DRIVEN: "WHEN [trigger], the system SHALL [action]"
  - STATE-DRIVEN: "WHILE [condition], the system SHALL [behavior]"
  - UNWANTED: "IF [condition], THEN the system SHALL [mitigation]"
  - OPTION: "WHERE [feature], the system SHALL [action]"
-->

### EARS-001: [Requirement Title] (Event-Driven)

**Source**: AS-1A, FR-001
**Original**: "Given a user on registration page, When they submit valid credentials, Then account is created"
**EARS Form**: WHEN user submits valid credentials on registration page, the system SHALL create an account with the submitted email.

**Derived Properties**:
- PROP-001: Inverse property (create/delete round-trip)
- PROP-004: Idempotent property (duplicate registration rejection)

**Confidence**: 0.95

---

### EARS-002: [Requirement Title] (Unwanted)

**Source**: EC-001
**Original**: "Invalid email format rejected"
**EARS Form**: IF email does not match RFC 5322 pattern, THEN the system SHALL reject registration with ValidationError.

**Derived Properties**:
- PROP-003: Boundary property (invalid email formats)

**Confidence**: 0.90

---

### EARS-003: [Requirement Title] (State-Driven)

**Source**: NFR-PERF-001
**Original**: "Response time < 200ms at p95 under normal load"
**EARS Form**: WHILE concurrent users <= 1000, the system SHALL respond in < 200ms at p95.

**Derived Properties**:
- PROP-002: Invariant property (latency bound)

**Confidence**: 0.88

---

## Properties by Type

### Inverse Properties

<!--
  Round-trip properties: applying inverse operation restores original state.
  Formula: f_inverse(f(x)) == x
  Typical sources: CRUD operations, encode/decode, serialize/deserialize
-->

#### PROP-001: [Property Name]

**Type**: Inverse
**Trace**: AS-1A, FR-001
**EARS Reference**: EARS-001

**Formula**:
```
delete_account(create_account(user)) == no_account_exists
```

**Description**: Creating and then deleting a user account should result in no account existing for that email.

**Generator Hints**:
```yaml
entity: User
valid_strategy: "builds(User, email=emails(), password=valid_password(), name=names())"
boundary_strategy: "builds(User, email=boundary_email(), password=valid_password())"
```

**Example Code** (Python/Hypothesis):
```python
@given(valid_user())
@settings(max_examples=100)
@example(User(email="a@b.c", password="Password1", name="X"))  # Shrunk
def test_prop_001_user_create_delete_inverse(user):
    """
    Property: delete(create(user)) == no_user
    @speckit[PROP:PROP-001,AS:AS-1A,FR:FR-001]
    """
    created = create_user(**user)
    assert user_exists(user.email)
    delete_user(created.id)
    assert not user_exists(user.email)
```

---

### Idempotent Properties

<!--
  Properties where applying operation twice equals applying once.
  Formula: f(f(x)) == f(x)
  Typical sources: PUT/UPDATE, normalization, sorting
-->

#### PROP-004: [Property Name]

**Type**: Idempotent
**Trace**: FR-002, AS-2A
**EARS Reference**: EARS-001

**Formula**:
```
normalize(normalize(email)) == normalize(email)
```

**Description**: Normalizing an email address twice should produce the same result as normalizing once.

**Example Code** (TypeScript/fast-check):
```typescript
describe('PROP-004: Email normalization idempotent', () => {
  // @speckit[PROP:PROP-004,FR:FR-002]
  it('should satisfy: normalize(normalize(x)) == normalize(x)', () => {
    fc.assert(
      fc.property(fc.emailAddress(), (email) => {
        const once = normalizeEmail(email);
        const twice = normalizeEmail(once);
        return once === twice;
      }),
      { numRuns: 100 }
    );
  });
});
```

---

### Invariant Properties

<!--
  Properties that always hold regardless of input.
  Formula: forall x: invariant(x) == true
  Typical sources: NFRs, business rules, constraints
-->

#### PROP-002: [Property Name]

**Type**: Invariant
**Trace**: NFR-PERF-001
**EARS Reference**: EARS-003

**Formula**:
```
forall request under_normal_load: response_time_p95 < 200ms
```

**Description**: All requests under normal load should complete within 200ms at p95.

**Example Code** (Go/rapid):
```go
// @speckit[PROP:PROP-002,NFR:NFR-PERF-001]
func TestProp002_LatencyInvariant(t *testing.T) {
    rapid.Check(t, func(t *rapid.T) {
        request := genValidRequest().Draw(t, "request")

        start := time.Now()
        _, err := handleRequest(request)
        latency := time.Since(start)

        if err != nil {
            t.Skip("Request failed, not measuring latency")
        }

        if latency > 200*time.Millisecond {
            t.Fatalf("Latency %v exceeds 200ms limit", latency)
        }
    })
}
```

---

### Boundary Properties

<!--
  Properties defining behavior at edge values.
  Formula: forall x in boundary: expected_behavior(x)
  Typical sources: EC-xxx (security, validation, boundary categories)
-->

#### PROP-003: [Property Name]

**Type**: Boundary
**Trace**: EC-001
**EARS Reference**: EARS-002
**Severity**: HIGH

**Formula**:
```
forall email not matching RFC5322: register(email) -> ValidationError
```

**Description**: All invalid email formats must be rejected with ValidationError.

**Boundary Generator**:
```python
invalid_email = st.one_of(
    st.just(""),           # Empty
    st.just("@"),          # No local part
    st.just("a@"),         # No domain
    st.just("@b.com"),     # No local part
    st.text().filter(lambda x: "@" not in x),  # Missing @
    st.text().filter(lambda x: x.count("@") > 1),  # Multiple @
)
```

**Shrunk Examples**:
| Example | Found Date | Iteration | Status |
|---------|------------|-----------|--------|
| `""` | 2026-01-03 | 1 | Preserved |
| `"@"` | 2026-01-03 | 1 | Preserved |
| `"a@"` | 2026-01-03 | 2 | Preserved |

**Example Code** (Java/jqwik):
```java
/**
 * Property: Invalid emails must be rejected
 * @speckit[PROP:PROP-003,EC:EC-001]
 */
@Property(tries = 100)
void prop003_invalidEmailBoundary(@ForAll("invalidEmails") String email) {
    assertThrows(ValidationException.class, () -> {
        userService.register(email, "ValidPass1", "Test User");
    });
}

@Provide
Arbitrary<String> invalidEmails() {
    return Arbitraries.oneOf(
        Arbitraries.just(""),
        Arbitraries.just("@"),
        Arbitraries.just("a@"),
        Arbitraries.strings().filter(s -> !s.contains("@"))
    );
}
```

---

### Commutative Properties

<!--
  Properties where order of operations doesn't matter.
  Formula: f(a, b) == f(b, a)
  Typical sources: Mathematical operations, set operations
-->

#### PROP-005: [Property Name] (if applicable)

**Type**: Commutative
**Trace**: FR-xxx
**Formula**: `add_to_cart(A, B) == add_to_cart(B, A)` (cart total)

---

### Model-Based Properties

<!--
  Properties verified by comparing system to simplified model.
  Formula: system_transitions ⊆ model_transitions
  Typical sources: State machines, workflows
-->

#### PROP-006: [Property Name] (if applicable)

**Type**: Model-Based
**Trace**: FR-xxx, STATE-xxx

**State Model**:
```
DRAFT -> SUBMITTED -> APPROVED -> PUBLISHED
              |           |
              v           v
           REJECTED    ARCHIVED
```

**Example Code** (Hypothesis Stateful):
```python
class OrderStateMachine(RuleBasedStateMachine):
    """
    Model-based test for order lifecycle
    @speckit[PROP:PROP-006,STATE:*]
    """
    def __init__(self):
        super().__init__()
        self.model = OrderModel()
        self.system = OrderService()

    @invariant()
    def states_match(self):
        assert self.model.state == self.system.get_state()

    @rule()
    def submit(self):
        assume(self.model.can_submit())
        self.model.submit()
        self.system.submit()
```

---

## Shrunk Examples Registry

<!--
  Preserved minimal counterexamples from property test runs.
  These are used for regression testing and documentation.
  Each example should be included as @example in generated tests.
-->

| PROP ID | Property | Shrunk Example | Found Date | Iteration | Resolution |
|---------|----------|----------------|------------|-----------|------------|
| PROP-001 | User Inverse | `User(email="a@b.c", password="P1", name="X")` | 2026-01-03 | 1 | Preserved |
| PROP-003 | Email Boundary | `""` | 2026-01-03 | 1 | Preserved |
| PROP-003 | Email Boundary | `"@"` | 2026-01-03 | 1 | Preserved |
| PROP-003 | Email Boundary | `"a@"` | 2026-01-03 | 2 | Preserved |

### Shrunk Examples JSON

```json
{
  "PROP-001": [
    {"email": "a@b.c", "password": "P1", "name": "X"}
  ],
  "PROP-003": ["", "@", "a@"]
}
```

---

## Generator Definitions

<!--
  Custom generators for domain entities.
  These are generated from spec entity analysis and can be customized.
-->

### Python (Hypothesis)

```python
# specs/[feature]/generators.py

from hypothesis import strategies as st
from hypothesis.strategies import builds, just, one_of, text, emails

# =============================================================================
# ENTITY GENERATORS
# =============================================================================

# Valid generators
valid_email = emails()
valid_password = text(min_size=8, max_size=128).filter(
    lambda p: any(c.isupper() for c in p) and
              any(c.islower() for c in p) and
              any(c.isdigit() for c in p)
)
valid_name = text(min_size=1, max_size=100)

valid_user = builds(
    dict,
    email=valid_email,
    password=valid_password,
    name=valid_name
)

# Boundary generators
invalid_email = one_of(
    just(""),
    just("@"),
    just("a@"),
    just("@b.com"),
    text().filter(lambda x: "@" not in x),
    text().filter(lambda x: x.count("@") > 1),
)

boundary_password = one_of(
    just(""),                    # Empty
    text(max_size=7),            # Too short
    just("password"),            # No uppercase/digit
    just("PASSWORD1"),           # No lowercase
    just("Password"),            # No digit
)

# Security generators (for PROP-004 etc.)
sql_injection_payloads = one_of(
    just("'; DROP TABLE users; --"),
    just("' OR '1'='1"),
    just("admin'--"),
    just("1; SELECT * FROM users"),
)
```

### TypeScript (fast-check)

```typescript
// specs/[feature]/generators.ts

import fc from 'fast-check';

// Valid generators
export const validEmail = fc.emailAddress();
export const validPassword = fc.string({ minLength: 8, maxLength: 128 })
  .filter(p => /[A-Z]/.test(p) && /[a-z]/.test(p) && /[0-9]/.test(p));
export const validName = fc.string({ minLength: 1, maxLength: 100 });

export const validUser = fc.record({
  email: validEmail,
  password: validPassword,
  name: validName,
});

// Boundary generators
export const invalidEmail = fc.oneof(
  fc.constant(''),
  fc.constant('@'),
  fc.constant('a@'),
  fc.string().filter(s => !s.includes('@')),
);

// Security generators
export const sqlInjectionPayloads = fc.oneof(
  fc.constant("'; DROP TABLE users; --"),
  fc.constant("' OR '1'='1"),
  fc.constant("admin'--"),
);
```

### Go (rapid)

```go
// generators_test.go

package main

import "pgregory.net/rapid"

// Valid generators
func genValidEmail() *rapid.Generator[string] {
    return rapid.StringMatching(`[a-z]+@[a-z]+\.[a-z]{2,4}`)
}

func genValidPassword() *rapid.Generator[string] {
    return rapid.Custom(func(t *rapid.T) string {
        base := rapid.StringOfN(rapid.RuneFrom(nil, 'a', 'z'), 6, 6).Draw(t, "base")
        upper := string(rapid.RuneFrom(nil, 'A', 'Z').Draw(t, "upper"))
        digit := string(rapid.RuneFrom(nil, '0', '9').Draw(t, "digit"))
        return base + upper + digit
    })
}

// Boundary generators
func genInvalidEmail() *rapid.Generator[string] {
    return rapid.OneOf(
        rapid.Just(""),
        rapid.Just("@"),
        rapid.Just("a@"),
        rapid.StringMatching(`[^@]+`),
    )
}
```

### Java (jqwik)

```java
// Generators.java

import net.jqwik.api.*;

public class Generators {

    @Provide
    public Arbitrary<String> validEmails() {
        return Arbitraries.emails();
    }

    @Provide
    public Arbitrary<String> validPasswords() {
        return Arbitraries.strings()
            .ofMinLength(8)
            .ofMaxLength(128)
            .filter(p -> p.matches(".*[A-Z].*") &&
                        p.matches(".*[a-z].*") &&
                        p.matches(".*[0-9].*"));
    }

    @Provide
    public Arbitrary<String> invalidEmails() {
        return Arbitraries.oneOf(
            Arbitraries.just(""),
            Arbitraries.just("@"),
            Arbitraries.just("a@"),
            Arbitraries.strings().filter(s -> !s.contains("@"))
        );
    }
}
```

### Kotlin (kotest-property)

```kotlin
// Generators.kt

import io.kotest.property.Arb
import io.kotest.property.arbitrary.*

// Valid generators
val validEmail = Arb.email()
val validPassword = Arb.string(8..128).filter { p ->
    p.any { it.isUpperCase() } &&
    p.any { it.isLowerCase() } &&
    p.any { it.isDigit() }
}

// Boundary generators
val invalidEmail = Arb.choice(
    Arb.constant(""),
    Arb.constant("@"),
    Arb.constant("a@"),
    Arb.string().filter { !it.contains("@") }
)

// Security generators
val sqlInjectionPayloads = Arb.choice(
    Arb.constant("'; DROP TABLE users; --"),
    Arb.constant("' OR '1'='1"),
    Arb.constant("admin'--")
)
```

---

## Quality Gates Status

| Gate ID | Name | Status | Actual | Threshold | Severity |
|---------|------|--------|--------|-----------|----------|
| VG-PROP | Property Coverage | PASS/FAIL | XX% | >= 80% | CRITICAL |
| VG-EARS | EARS Transformation | PASS/FAIL | XX% | >= 85% | HIGH |
| VG-SHRUNK | Shrunk Examples | PASS/FAIL | N | >= 3 | MEDIUM |
| VG-PGS | PGS Resolution | PASS/FAIL | N | 0 unresolved | CRITICAL |

---

## PQS (Property Quality Score) Breakdown

```
Requirement Coverage:  XX.X × 0.30 = XX.X
Type Diversity:        XX.X × 0.20 = XX.X
Generator Quality:     XX.X × 0.20 = XX.X
Shrunk Examples:       XX.X × 0.15 = XX.X
EARS Alignment:        XX.X × 0.15 = XX.X
───────────────────────────────────────
TOTAL PQS:                       XX.X / 100
```

**Status**: [Ready (>= 80) | Needs Work (60-79) | Block (< 60)]

---

## Coverage Gaps

<!--
  Requirements without property coverage.
  Action items for improving PQS.
-->

### Missing Property Coverage

| Artifact | Type | Reason | Suggested Property |
|----------|------|--------|-------------------|
| FR-003 | Functional | No testable criteria | Add invariant for data validation |
| EC-005 | Edge Case | Complex state condition | Consider model-based property |

### Ambiguous Requirements

| Artifact | Ambiguity | Suggested Clarification |
|----------|-----------|------------------------|
| FR-007 | Auth method unspecified | Clarify: email/password, SSO, or OAuth? |

---

## Generated Test Files

| Language | Framework | File Path | Properties Covered |
|----------|-----------|-----------|-------------------|
| Python | Hypothesis | `tests/properties/test_[feature]_properties.py` | PROP-001, PROP-002, PROP-003 |
| TypeScript | fast-check | `tests/properties/[feature].property.test.ts` | PROP-001, PROP-003, PROP-004 |
| Go | rapid | `[package]_property_test.go` | PROP-001, PROP-002 |
| Java | jqwik | `src/test/java/.../[Feature]PropertyTest.java` | PROP-001, PROP-003 |
| Kotlin | kotest | `src/test/kotlin/.../[Feature]PropertyTest.kt` | PROP-001, PROP-003 |

---

## Next Steps

1. [ ] Review generated properties for accuracy
2. [ ] Run property tests: `pytest tests/properties/ --hypothesis-show-statistics`
3. [ ] Address coverage gaps (missing properties for FR-003, EC-005)
4. [ ] If counterexamples found, run `/speckit.properties --profile pgs` for refinement
5. [ ] Proceed to `/speckit.implement` when PQS >= 80

---

## Appendix: Command Used

```bash
/speckit.properties --profile full --language all
```

**Generated by**: Claude Code (`/speckit.properties`)
**Template version**: 0.0.76

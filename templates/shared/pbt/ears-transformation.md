# EARS Transformation Rules

This document defines the transformation rules for converting specification artifacts (AS, EC, FR, NFR) into EARS (Easy Approach to Requirements Syntax) canonical forms.

## EARS Overview

EARS was developed by Alistair Mavin at Rolls-Royce to reduce requirements ambiguity. It provides five syntactic templates that force precision in requirement statements.

### EARS Types

| Type | Pattern | Use Case |
|------|---------|----------|
| **Ubiquitous** | "The \<system\> SHALL \<response\>" | Always-on behavior, no trigger |
| **Event-Driven** | "WHEN \<trigger\>, the \<system\> SHALL \<response\>" | Triggered behavior |
| **State-Driven** | "WHILE \<state\>, the \<system\> SHALL \<behavior\>" | State-dependent behavior |
| **Unwanted** | "IF \<trigger\>, THEN the \<system\> SHALL \<mitigation\>" | Preventing bad states |
| **Option** | "WHERE \<feature\>, the \<system\> SHALL \<response\>" | Optional features |

---

## Transformation Rules by Artifact Type

### 1. Functional Requirements (FR-xxx)

**Detection Logic**:
```
IF FR contains explicit trigger words (when, upon, after, before):
  → EVENT_DRIVEN
ELIF FR contains state conditions (while, during, as long as):
  → STATE_DRIVEN
ELIF FR describes optional feature (if enabled, when configured):
  → OPTION
ELSE:
  → UBIQUITOUS
```

**Transformation Examples**:

| Original FR | EARS Type | Transformed |
|-------------|-----------|-------------|
| "System MUST validate emails" | Ubiquitous | "The system SHALL validate all email addresses" |
| "When user logs in, system must create session" | Event-Driven | "WHEN user logs in, the system SHALL create session" |
| "System must maintain connection while active" | State-Driven | "WHILE session is active, the system SHALL maintain connection" |
| "Premium users can export data" | Option | "WHERE premium is active, the system SHALL enable data export" |

**Extraction Patterns**:
```yaml
event_driven_triggers:
  - "when"
  - "upon"
  - "after"
  - "before"
  - "on receipt of"
  - "if user"

state_driven_conditions:
  - "while"
  - "during"
  - "as long as"
  - "whenever"
  - "in state"

option_indicators:
  - "if enabled"
  - "when configured"
  - "for premium"
  - "optionally"
  - "can be configured to"
```

---

### 2. Acceptance Scenarios (AS-xxx)

**Structure**: Given/When/Then maps directly to Event-Driven EARS.

**Transformation Rule**:
```
GIVEN → precondition (optional context)
WHEN → trigger
THEN → response (system SHALL)
```

**Classification Influence**:

| Classification | Primary EARS | Property Hints |
|---------------|--------------|----------------|
| HAPPY_PATH | Event-Driven | Inverse, Idempotent |
| ALT_PATH | Event-Driven | Commutative |
| ERROR_PATH | Unwanted | Boundary |
| BOUNDARY | Unwanted | Boundary, Invariant |
| SECURITY | Unwanted | Security, Boundary |

**Transformation Examples**:

```yaml
# HAPPY_PATH → Event-Driven
source:
  id: AS-1A
  classification: HAPPY_PATH
  given: "user is on registration page"
  when: "user submits valid credentials"
  then: "account is created"

ears:
  type: event_driven
  trigger: "user submits valid credentials on registration page"
  precondition: "user is on registration page"
  response: "create account with submitted email"
  statement: |
    WHEN user submits valid credentials on registration page,
    the system SHALL create account with submitted email.

properties:
  - type: inverse
    formula: "delete(create(user)) == no_user"
  - type: idempotent
    formula: "create(same_email) twice → DuplicateError second time"
```

```yaml
# BOUNDARY → Unwanted
source:
  id: AS-1B
  classification: BOUNDARY
  given: "user on registration page"
  when: "user submits empty email"
  then: "validation error is shown"

ears:
  type: unwanted
  condition: "email is empty"
  trigger: "user submits registration"
  mitigation: "reject with ValidationError"
  statement: |
    IF email is empty,
    THEN the system SHALL reject registration with ValidationError.

properties:
  - type: boundary
    formula: 'forall empty_email: register("") → ValidationError'
```

---

### 3. Edge Cases (EC-xxx)

**Primary EARS Type**: Unwanted (preventing bad outcomes)

**Transformation by Category**:

| EC Category | EARS Pattern | Property Type |
|-------------|--------------|---------------|
| security | IF \<attack\>, THEN \<prevent\> | Security/Boundary |
| validation | IF \<invalid input\>, THEN \<reject\> | Boundary |
| boundary | IF \<edge value\>, THEN \<handle\> | Boundary |
| concurrency | WHILE \<concurrent\>, THEN \<safe\> | Invariant |
| integration | IF \<external fails\>, THEN \<fallback\> | Invariant |
| performance | WHILE \<load\>, THEN \<degrade gracefully\> | Invariant |

**Transformation Examples**:

```yaml
# Security Edge Case
source:
  id: EC-002
  category: security
  severity: CRITICAL
  condition: "SQL injection in email field"
  expected: "input is sanitized and rejected"

ears:
  type: unwanted
  condition: "email contains SQL injection patterns"
  trigger: "user submits registration"
  mitigation: "sanitize AND reject with error"
  safe_state: "no SQL executed, no data compromised"
  statement: |
    IF email contains SQL injection patterns,
    THEN the system SHALL sanitize input AND reject with ValidationError,
    ensuring no SQL is executed.

properties:
  - type: boundary
    formula: "forall sql_payload: register(payload) → ValidationError"
    security_category: "OWASP A03 Injection"
    generator: "sql_injection_payloads()"
```

```yaml
# Boundary Edge Case
source:
  id: EC-003
  category: boundary
  severity: MEDIUM
  condition: "password at exact minimum length (8 chars)"
  expected: "accepted if other criteria met"

ears:
  type: event_driven  # boundary that should work
  trigger: "user submits 8-character password meeting all criteria"
  response: "accept password"
  statement: |
    WHEN user submits 8-character password with uppercase, lowercase, and digit,
    the system SHALL accept the password.

properties:
  - type: boundary
    formula: "forall p where len(p)==8 AND valid_chars(p): accept(p)"
    generator: "exact_min_length_password()"
```

---

### 4. Non-Functional Requirements (NFR-xxx)

**Primary EARS Type**: State-Driven (constraints under conditions)

**Transformation by NFR Category**:

| NFR Category | EARS Pattern | Property Type |
|--------------|--------------|---------------|
| NFR-PERF-xxx | WHILE \<load\>, SHALL \<metric bound\> | Invariant |
| NFR-SEC-xxx | The system SHALL \<security measure\> | Invariant (always) |
| NFR-REL-xxx | WHILE \<operational\>, SHALL \<availability\> | Invariant |
| NFR-SCAL-xxx | WHILE \<scale\>, SHALL \<performance\> | Invariant |
| NFR-A11Y-xxx | The system SHALL \<accessibility\> | Invariant |

**Transformation Examples**:

```yaml
# Performance NFR → State-Driven
source:
  id: NFR-PERF-001
  category: performance
  text: "API response time < 200ms p95 under normal load"
  measurement: "APM monitoring"
  threshold: "p95 < 200ms, p99 < 500ms"

ears:
  type: state_driven
  state: "concurrent users <= 1000 (normal load)"
  behavior: "respond to API requests"
  constraint: "p95 latency < 200ms"
  statement: |
    WHILE concurrent users <= 1000,
    the system SHALL respond to API requests with p95 latency < 200ms.

properties:
  - type: invariant
    formula: "forall request under_normal_load: latency_p95 < 200ms"
    statistical: true
    sample_size: 1000
```

```yaml
# Security NFR → Ubiquitous
source:
  id: NFR-SEC-001
  category: security
  text: "All data in transit MUST use TLS 1.3"

ears:
  type: ubiquitous
  behavior: "encrypt all data in transit"
  constraint: "TLS 1.3 minimum"
  statement: |
    The system SHALL encrypt all data in transit using TLS 1.3 or higher.

properties:
  - type: invariant
    formula: "forall connection: tls_version >= 1.3"
```

---

## Property Derivation from EARS

### EARS to Property Type Mapping

| EARS Type | Primary Properties | Secondary Properties |
|-----------|-------------------|---------------------|
| Event-Driven | Inverse, Idempotent | Model-Based |
| Unwanted | Boundary, Security | Invariant |
| State-Driven | Invariant | Performance |
| Ubiquitous | Invariant | - |
| Option | Invariant | Model-Based |

### Property Extraction Heuristics

```yaml
inverse_heuristics:
  patterns:
    - "create" + "delete" in same domain
    - "add" + "remove"
    - "encode" + "decode"
    - "serialize" + "deserialize"
    - "open" + "close"
    - "start" + "stop"
  formula_template: "inverse(f(x)) == x"

idempotent_heuristics:
  patterns:
    - "update" or "PUT" operation
    - "normalize" or "format"
    - "sort" or "order"
    - "deduplicate"
    - "cache"
  formula_template: "f(f(x)) == f(x)"

invariant_heuristics:
  patterns:
    - "always", "never", "must"
    - NFR constraints
    - data integrity rules
    - business rules
  formula_template: "forall x: P(x) == true"

boundary_heuristics:
  patterns:
    - edge case (EC-xxx)
    - "minimum", "maximum"
    - "empty", "null", "zero"
    - validation rules
  formula_template: "forall x in boundary: expected_behavior(x)"

commutative_heuristics:
  patterns:
    - order-independent operations
    - set operations
    - accumulative calculations
  formula_template: "f(a, b) == f(b, a)"

model_based_heuristics:
  patterns:
    - state machine description
    - workflow steps
    - lifecycle states
  formula_template: "system_transitions ⊆ model_transitions"
```

---

## Confidence Scoring

Each transformation receives a confidence score based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Pattern Match | 0.40 | How well source matches EARS pattern |
| Completeness | 0.30 | All required EARS components present |
| Ambiguity | 0.20 | Absence of vague terms |
| Traceability | 0.10 | Clear links to other artifacts |

**Confidence Thresholds**:
- HIGH (>= 0.90): Proceed automatically
- MEDIUM (0.70 - 0.89): Proceed with review note
- LOW (< 0.70): Flag for manual review

---

## Ambiguity Detection

### Vague Terms to Flag

```yaml
vague_terms:
  performance:
    - "fast"
    - "responsive"
    - "quick"
    - "efficient"
  quantity:
    - "many"
    - "few"
    - "some"
    - "several"
  quality:
    - "user-friendly"
    - "intuitive"
    - "robust"
    - "reliable" (without metric)
  time:
    - "soon"
    - "quickly"
    - "timely"
    - "promptly"
```

### Ambiguity Resolution Suggestions

```yaml
ambiguity_resolutions:
  - vague: "fast response"
    suggest: "Specify latency threshold (e.g., <200ms p95)"

  - vague: "many users"
    suggest: "Specify concurrent user count (e.g., 1000 concurrent)"

  - vague: "user-friendly"
    suggest: "Specify usability metric (e.g., task completion <3 clicks)"

  - vague: "reliable"
    suggest: "Specify availability percentage (e.g., 99.9% uptime)"
```

---

## Output Format

### EARS Intermediate YAML Schema

```yaml
transformations:
  - id: EARS-NNN
    type: event_driven|ubiquitous|state_driven|unwanted|option

    source:
      artifact: AS-xxx|EC-xxx|FR-xxx|NFR-xxx
      artifact_type: acceptance_scenario|edge_case|functional_requirement|nfr
      classification: HAPPY_PATH|ALT_PATH|ERROR_PATH|BOUNDARY|SECURITY
      severity: CRITICAL|HIGH|MEDIUM|LOW
      category: security|validation|boundary|concurrency|...
      original_text: "..."
      location: "spec.md:NN"

    ears_form:
      # Type-specific fields
      trigger: "..."        # event_driven
      precondition: "..."   # event_driven (optional)
      state: "..."          # state_driven
      condition: "..."      # unwanted
      mitigation: "..."     # unwanted
      safe_state: "..."     # unwanted
      feature_condition: "..." # option
      action: "..."
      outcome: "..."
      constraint: "..."
      statement: "..."      # Full EARS statement

    properties_derived:
      - id: PROP-NNN
        type: inverse|idempotent|invariant|commutative|model_based|boundary
        formula: "..."
        confidence: 0.XX
        generator_hint: "..."
        security_category: "..." # if applicable

    confidence: 0.XX
    ambiguity_notes: ["..."]

    trace:
      functional_requirements: [FR-xxx]
      edge_cases: [EC-xxx]
      nfr: [NFR-xxx]
```

---

## Integration with Property Extraction

After EARS transformation, properties are extracted using `property-extraction.md` rules:

1. Each EARS form generates 1+ properties
2. Properties are assigned PROP-xxx IDs
3. Properties link back to EARS-xxx and source artifacts
4. Generator hints are derived from entity analysis
5. Shrunk example hints may be added from similar patterns

**Flow**:
```
spec.md → EARS Transformation → ears-intermediate.yaml
                                       ↓
                              Property Extraction → properties.md
                                       ↓
                              Code Generation → test files
```

# Property Extraction Algorithm

This document defines the algorithm for extracting testable properties from EARS-transformed requirements.

## Property Types Overview

| Type | Formula | Detection Heuristics | Sources |
|------|---------|---------------------|---------|
| **Inverse** | `f_inv(f(x)) == x` | CRUD pairs, encode/decode | AS HAPPY_PATH |
| **Idempotent** | `f(f(x)) == f(x)` | PUT, normalize, sort | AS HAPPY_PATH |
| **Invariant** | `forall x: P(x)` | Constraints, NFRs | NFR-xxx |
| **Commutative** | `f(a,b) == f(b,a)` | Order-independent ops | AS ALT_PATH |
| **Model-Based** | `sys ⊆ model` | State machines | Workflows |
| **Boundary** | `forall x ∈ boundary: B(x)` | Edge cases | EC-xxx |

---

## Extraction Algorithm

### Phase 1: EARS-to-Property Mapping

```
FOR EACH ears_form IN ears-intermediate.yaml:

  MATCH ears_form.type:

    CASE "event_driven":
      # Check for inverse pairs
      IF has_inverse_action(ears_form.action):
        CREATE inverse_property(ears_form)

      # Check for idempotent behavior
      IF is_idempotent_candidate(ears_form.action):
        CREATE idempotent_property(ears_form)

      # Check for model-based (workflows)
      IF is_state_transition(ears_form):
        ADD_TO model_candidates(ears_form)

    CASE "unwanted":
      # Security and boundary properties
      IF ears_form.source.category IN ["security", "validation"]:
        CREATE boundary_property(ears_form, security=true)
      ELSE:
        CREATE boundary_property(ears_form)

    CASE "state_driven":
      # Invariant under conditions
      CREATE invariant_property(ears_form, conditional=true)

    CASE "ubiquitous":
      # Always-true invariant
      CREATE invariant_property(ears_form, conditional=false)

    CASE "option":
      # Feature-gated invariant
      CREATE invariant_property(ears_form, feature_gated=true)
```

### Phase 2: Cross-Artifact Analysis

```
# Detect commutative properties
FOR EACH pair IN cartesian_product(ears_forms, ears_forms):
  IF is_commutative_pair(pair.a, pair.b):
    CREATE commutative_property(pair)

# Build model-based properties from state candidates
IF model_candidates.length > 2:
  state_model = build_state_model(model_candidates)
  CREATE model_based_property(state_model)

# Link related properties
FOR EACH property:
  property.related = find_related_properties(property)
```

---

## Property Type Extraction Details

### 1. Inverse Properties

**Heuristics**:
```yaml
inverse_action_pairs:
  # CRUD operations
  - [create, delete]
  - [add, remove]
  - [insert, delete]
  - [open, close]
  - [start, stop]
  - [enable, disable]
  - [lock, unlock]

  # Encoding operations
  - [encode, decode]
  - [encrypt, decrypt]
  - [compress, decompress]
  - [serialize, deserialize]
  - [marshal, unmarshal]
  - [stringify, parse]

  # Transaction operations
  - [begin, rollback]
  - [push, pop]
  - [enqueue, dequeue]
```

**Extraction Function**:
```python
def extract_inverse_property(ears_form):
    action = ears_form.action
    inverse_action = find_inverse(action)

    if not inverse_action:
        return None

    return Property(
        id=generate_prop_id(),
        type="inverse",
        formula=f"{inverse_action}({action}(x)) == x",
        description=f"Applying {action} then {inverse_action} returns original state",
        source_artifacts=[ears_form.source.artifact],
        generators={
            "valid": f"valid_{entity}()",
            "boundary": f"boundary_{entity}()"
        },
        priority=infer_priority(ears_form)
    )
```

**Example**:
```yaml
source_ears:
  action: "create_user"
  outcome: "user exists"

property:
  id: PROP-001
  type: inverse
  formula: "delete_user(create_user(data)) == no_user_exists(data.email)"
  generators:
    valid: "valid_user()"
```

---

### 2. Idempotent Properties

**Heuristics**:
```yaml
idempotent_indicators:
  # HTTP methods
  - "PUT"
  - "update"
  - "set"
  - "replace"

  # Normalization
  - "normalize"
  - "format"
  - "trim"
  - "lowercase"
  - "uppercase"
  - "canonicalize"

  # Ordering
  - "sort"
  - "order"
  - "arrange"

  # Deduplication
  - "deduplicate"
  - "unique"
  - "distinct"

  # Caching
  - "cache"
  - "memoize"
```

**Extraction Function**:
```python
def extract_idempotent_property(ears_form):
    action = ears_form.action

    if not is_idempotent_candidate(action):
        return None

    return Property(
        id=generate_prop_id(),
        type="idempotent",
        formula=f"{action}({action}(x)) == {action}(x)",
        description=f"Applying {action} twice equals applying once",
        source_artifacts=[ears_form.source.artifact],
        generators={
            "valid": f"valid_{infer_entity(action)}()"
        }
    )
```

**Example**:
```yaml
source_ears:
  action: "normalize_email"

property:
  id: PROP-002
  type: idempotent
  formula: "normalize_email(normalize_email(e)) == normalize_email(e)"
  generators:
    valid: "emails()"
```

---

### 3. Invariant Properties

**Heuristics**:
```yaml
invariant_keywords:
  always:
    - "always"
    - "must always"
    - "shall always"
    - "continuously"

  never:
    - "never"
    - "must not"
    - "shall not"
    - "cannot"

  constraint:
    - "at least"
    - "at most"
    - "between"
    - "within"
    - "<", ">", "<=", ">="

  business_rules:
    - "balance cannot be negative"
    - "quantity must be positive"
    - "date must be in future"
```

**Types of Invariants**:

| Subtype | Pattern | Example |
|---------|---------|---------|
| Universal | `forall x: P(x)` | "All emails are valid RFC5322" |
| Conditional | `while C: forall x: P(x)` | "Under load: latency < 200ms" |
| Feature-gated | `if F: forall x: P(x)` | "If premium: can export" |
| Statistical | `P(x) with probability p` | "p95 latency < 200ms" |

**Extraction Function**:
```python
def extract_invariant_property(ears_form, conditional=False, feature_gated=False):
    if conditional:
        condition = ears_form.state
        formula = f"while {condition}: forall x: {ears_form.constraint}"
    elif feature_gated:
        feature = ears_form.feature_condition
        formula = f"if {feature}: forall x: {ears_form.action}"
    else:
        formula = f"forall x: {ears_form.constraint}"

    return Property(
        id=generate_prop_id(),
        type="invariant",
        formula=formula,
        description=f"Invariant: {ears_form.statement}",
        source_artifacts=[ears_form.source.artifact],
        statistical=is_statistical(ears_form),
        sample_size=1000 if is_statistical(ears_form) else None
    )
```

**Example**:
```yaml
source_ears:
  type: state_driven
  state: "concurrent_users <= 1000"
  constraint: "latency_p95 < 200ms"

property:
  id: PROP-003
  type: invariant
  formula: "while concurrent_users <= 1000: forall request: latency_p95 < 200ms"
  statistical: true
  sample_size: 1000
```

---

### 4. Boundary Properties

**Heuristics**:
```yaml
boundary_sources:
  # Edge case categories
  edge_case_categories:
    - security
    - validation
    - boundary

  # Edge case severity (prioritization)
  severity_priority:
    CRITICAL: P1
    HIGH: P1
    MEDIUM: P2
    LOW: P3

  # Boundary patterns
  boundary_patterns:
    - empty: '""', '[]', '{}'
    - null: 'null', 'None', 'nil'
    - zero: '0', '0.0'
    - negative: '-1', '-0.01'
    - max: 'MAX_INT', 'MAX_SIZE'
    - min: 'MIN_INT', 'MIN_SIZE'
    - overflow: 'MAX + 1'
    - underflow: 'MIN - 1'
```

**Security Generators**:
```yaml
security_generators:
  sql_injection:
    - "'; DROP TABLE users; --"
    - "' OR '1'='1"
    - "admin'--"
    - "1; SELECT * FROM users"

  xss:
    - "<script>alert('xss')</script>"
    - "<img src=x onerror=alert('xss')>"
    - "javascript:alert('xss')"

  path_traversal:
    - "../../../etc/passwd"
    - "..\\..\\..\\windows\\system32"
    - "%2e%2e%2f"

  command_injection:
    - "; rm -rf /"
    - "| cat /etc/passwd"
    - "$(whoami)"
```

**Extraction Function**:
```python
def extract_boundary_property(ears_form, security=False):
    condition = ears_form.condition
    mitigation = ears_form.mitigation

    if security:
        generator_name = infer_security_generator(condition)
        security_category = map_to_owasp(condition)
    else:
        generator_name = infer_boundary_generator(condition)
        security_category = None

    return Property(
        id=generate_prop_id(),
        type="boundary",
        formula=f"forall x in boundary({condition}): {mitigation}",
        description=f"Boundary: {ears_form.statement}",
        source_artifacts=[ears_form.source.artifact],
        severity=ears_form.source.severity,
        security_category=security_category,
        generators={
            "boundary": generator_name
        }
    )
```

**Example**:
```yaml
source_ears:
  type: unwanted
  condition: "email contains SQL injection"
  mitigation: "reject with ValidationError"
  source:
    category: security
    severity: CRITICAL

property:
  id: PROP-004
  type: boundary
  formula: "forall sql_payload: register(sql_payload) → ValidationError"
  security_category: "OWASP A03:2021 Injection"
  severity: CRITICAL
  generators:
    boundary: "sql_injection_payloads()"
```

---

### 5. Commutative Properties

**Heuristics**:
```yaml
commutative_operations:
  # Mathematical
  - addition
  - multiplication
  - union
  - intersection

  # Domain-specific
  - "add items to cart"
  - "apply filters"
  - "merge settings"
  - "combine permissions"
```

**Detection Logic**:
```python
def detect_commutative_pair(ears_a, ears_b):
    """
    Check if two operations are commutative.
    """
    # Same action on same entity type
    if ears_a.entity != ears_b.entity:
        return False

    # Order-independent outcome
    if not is_order_independent(ears_a.action, ears_b.action):
        return False

    return True
```

**Example**:
```yaml
source_ears:
  - action: "add_item_A_to_cart"
  - action: "add_item_B_to_cart"

property:
  id: PROP-005
  type: commutative
  formula: "add_to_cart(A, B).total == add_to_cart(B, A).total"
  description: "Cart total is independent of item addition order"
```

---

### 6. Model-Based Properties

**Detection Heuristics**:
```yaml
state_machine_indicators:
  - "state transition"
  - "workflow step"
  - "lifecycle"
  - "status change"
  - "from ... to ..."

  valid_states:
    - DRAFT, SUBMITTED, APPROVED, REJECTED
    - PENDING, PROCESSING, COMPLETED, FAILED
    - CREATED, ACTIVE, SUSPENDED, DELETED
```

**Model Building**:
```python
def build_state_model(ears_forms):
    """
    Build state model from multiple EARS forms.
    """
    states = set()
    transitions = []

    for ears in ears_forms:
        if has_state_info(ears):
            from_state = extract_from_state(ears)
            to_state = extract_to_state(ears)
            trigger = ears.trigger

            states.add(from_state)
            states.add(to_state)
            transitions.append({
                "from": from_state,
                "to": to_state,
                "trigger": trigger,
                "guard": extract_guard(ears)
            })

    return StateModel(
        states=states,
        initial_state=infer_initial(states),
        transitions=transitions
    )
```

**Example**:
```yaml
source_ears:
  - action: "submit_order"
    transition: "DRAFT → SUBMITTED"
  - action: "approve_order"
    transition: "SUBMITTED → APPROVED"
  - action: "reject_order"
    transition: "SUBMITTED → REJECTED"

property:
  id: PROP-006
  type: model_based
  formula: "system_transitions ⊆ model_transitions"
  model:
    states: [DRAFT, SUBMITTED, APPROVED, REJECTED]
    initial: DRAFT
    transitions:
      - { from: DRAFT, to: SUBMITTED, trigger: submit }
      - { from: SUBMITTED, to: APPROVED, trigger: approve }
      - { from: SUBMITTED, to: REJECTED, trigger: reject }
  invariants:
    - "once APPROVED or REJECTED, no further transitions"
```

---

## Generator Creation

### Entity-to-Generator Mapping

```python
def create_generators(entities):
    """
    Create generators for all entities from spec.
    """
    generators = {}

    for entity in entities:
        # Valid generator
        generators[f"valid_{entity.name.lower()}"] = build_valid_generator(entity)

        # Boundary generator
        generators[f"boundary_{entity.name.lower()}"] = build_boundary_generator(entity)

        # If has security-sensitive fields
        if has_security_fields(entity):
            generators[f"security_{entity.name.lower()}"] = build_security_generator(entity)

    return generators
```

### Generator Templates by Attribute Type

```yaml
string_generators:
  valid:
    email: "emails()"
    uuid: "uuids()"
    url: "urls()"
    default: "text(min_size=1, max_size=100)"

  boundary:
    email: 'one_of(just(""), just("@"), text().filter(no_at))'
    default: 'one_of(just(""), text(min_size=MAX+1))'

  security:
    email: "sql_injection_payloads()"
    default: "one_of(sql_injection(), xss_payloads())"

numeric_generators:
  valid:
    positive: "integers(min_value=1)"
    non_negative: "integers(min_value=0)"
    default: "integers()"

  boundary:
    positive: "one_of(just(0), just(-1), just(MAX_INT+1))"
    default: "one_of(just(MIN_INT-1), just(MAX_INT+1))"

boolean_generators:
  valid: "booleans()"
  # No boundary for booleans

date_generators:
  valid:
    future: "dates(min_value=date.today())"
    past: "dates(max_value=date.today())"
    default: "dates()"

  boundary:
    future: "dates(max_value=date.today() - timedelta(days=1))"
    past: "dates(min_value=date.today() + timedelta(days=1))"
```

---

## Priority Assignment

### Priority Rules

```yaml
priority_rules:
  P1_critical:
    - severity: CRITICAL
    - category: security
    - classification: HAPPY_PATH with business_critical

  P2_important:
    - severity: HIGH
    - category: validation
    - classification: BOUNDARY

  P3_optional:
    - severity: MEDIUM or LOW
    - category: performance (non-critical)
```

### Automatic Priority Inference

```python
def infer_priority(ears_form):
    source = ears_form.source

    # Security always P1
    if source.category == "security" or source.severity == "CRITICAL":
        return "P1"

    # Happy path with high severity
    if source.classification == "HAPPY_PATH" and source.severity in ["CRITICAL", "HIGH"]:
        return "P1"

    # Validation and boundary
    if source.category in ["validation", "boundary"] or source.severity == "HIGH":
        return "P2"

    return "P3"
```

---

## Output Format

### Property Definition Schema

```yaml
properties:
  - id: PROP-NNN
    type: inverse|idempotent|invariant|commutative|model_based|boundary

    formula: "mathematical/logical formula"
    description: "Human-readable description"

    source:
      ears_id: EARS-NNN
      artifacts: [AS-xxx, EC-xxx, FR-xxx, NFR-xxx]
      location: "spec.md:NN"

    priority: P1|P2|P3
    severity: CRITICAL|HIGH|MEDIUM|LOW  # for boundary

    # Type-specific fields
    security_category: "OWASP Axxx"  # for security boundary
    statistical: true|false  # for invariants
    sample_size: NNN  # for statistical
    model: {...}  # for model_based

    generators:
      valid: "generator_expression"
      boundary: "boundary_generator"
      security: "security_generator"  # if applicable

    shrunk_examples: []  # populated after test runs

    related_properties: [PROP-xxx]  # linked properties

    confidence: 0.XX
```

---

## Quality Metrics

### Coverage Calculation

```python
def calculate_coverage(properties, spec):
    """
    Calculate property coverage metrics.
    """
    fr_with_props = count_frs_with_properties(properties, spec.frs)
    as_boundary_with_props = count_boundary_as_with_properties(properties, spec.acceptance_scenarios)
    ec_security_with_props = count_security_ec_with_properties(properties, spec.edge_cases)

    return {
        "fr_coverage": fr_with_props / len(spec.frs),
        "as_boundary_coverage": as_boundary_with_props / count_boundary_as(spec),
        "ec_security_coverage": ec_security_with_props / count_security_ec(spec),
        "type_diversity": count_unique_types(properties) / 6
    }
```

### PQS (Property Quality Score)

```python
def calculate_pqs(properties, spec, ears_intermediate):
    """
    Calculate Property Quality Score (0-100).
    """
    coverage = calculate_coverage(properties, spec)

    # Component scores
    requirement_coverage = (
        coverage["fr_coverage"] * 0.4 +
        coverage["as_boundary_coverage"] * 0.3 +
        coverage["ec_security_coverage"] * 0.3
    )

    type_diversity = coverage["type_diversity"]

    generator_quality = assess_generator_quality(properties)

    shrunk_examples = min(count_shrunk_examples(properties) / 3, 1.0)

    ears_alignment = ears_intermediate.validation.ears_coverage.coverage_percent / 100

    # Weighted sum
    pqs = (
        requirement_coverage * 0.30 +
        type_diversity * 0.20 +
        generator_quality * 0.20 +
        shrunk_examples * 0.15 +
        ears_alignment * 0.15
    ) * 100

    return round(pqs, 1)
```

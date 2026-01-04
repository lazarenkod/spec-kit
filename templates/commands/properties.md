---
description: Extract properties from spec artifacts and generate property-based tests with EARS transformation. Creates PROP-xxx traced to AS/EC/FR/NFR for comprehensive edge case discovery via PGS (Property-Generated Solver) methodology.
persona: qa-agent

handoff:
  requires: specs/[feature]/spec.md
  generates: specs/[feature]/properties.md

handoffs:
  - label: "Generate Property Tests"
    agent: speckit.implement
    prompt: "Implement property-based tests from generated properties.md"
    auto: false
    condition:
      - "Properties extracted successfully"
      - "Language targets specified"
      - "PQS >= 80"
    gates:
      - name: "Property Quality Gate"
        check: "PQS >= 80"
        block_if: "PQS < 80"
        message: "Property Quality Score too low. Review and improve properties."

  - label: "Update Specification"
    agent: speckit.specify
    prompt: "Add discovered edge cases to spec.md as EC-xxx entries"
    auto: false
    condition:
      - "New edge cases discovered via property testing"
      - "Counterexamples suggest missing scenarios"

  - label: "Validate Property Coverage"
    agent: speckit.analyze
    prompt: "Validate property coverage against requirements"
    auto: true
    condition:
      - "Properties generated"
      - "Coverage analysis requested"
    gates:
      - name: "Property Coverage Gate"
        check: "PROP coverage >= 80%"
        block_if: "PROP coverage < 80%"
        message: "Insufficient property coverage. Add properties for uncovered requirements."

scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-spec
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireSpec

claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 16000
  cache_hierarchy: full
  orchestration:
    max_parallel: 5
    role_isolation: true
    wave_overlap:
      enabled: true
      overlap_threshold: 0.80
  semantic_cache:
    enabled: true
    encoder: all-MiniLM-L6-v2
    similarity_threshold: 0.95
    scope: session

  subagents:
    # =========================================================================
    # WAVE 1: EXTRACTION (Parallel - No Dependencies)
    # =========================================================================
    - role: ears-transformer
      role_group: EXTRACT
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      trigger: "when transforming spec artifacts to EARS format"
      prompt: |
        Transform specification artifacts to EARS (Easy Approach to Requirements Syntax) canonical forms.

        EARS Types:
        1. UBIQUITOUS: "The <system> SHALL <response>"
           - Source: FR-xxx without explicit triggers
           - Example: FR-001 "System must validate emails" → "The system SHALL validate all email addresses"

        2. EVENT-DRIVEN: "WHEN <trigger>, the <system> SHALL <response>"
           - Source: AS-xxx (Given/When/Then scenarios)
           - Example: AS-1A "Given user on page, When submit, Then create account"
                    → "WHEN user submits valid credentials, the system SHALL create an account"

        3. STATE-DRIVEN: "WHILE <condition>, the <system> SHALL <behavior>"
           - Source: NFR-xxx constraints with state conditions
           - Example: NFR-PERF-001 "Response time < 200ms under normal load"
                    → "WHILE concurrent users <= 1000, the system SHALL respond in < 200ms p95"

        4. UNWANTED: "IF <trigger>, THEN the <system> SHALL <mitigation>"
           - Source: EC-xxx (security, boundary, validation)
           - Example: EC-001 "SQL injection in email field"
                    → "IF email contains SQL injection patterns, THEN the system SHALL reject with ValidationError"

        5. OPTION: "WHERE <feature included>, the <system> SHALL <response>"
           - Source: Optional features, feature flags
           - Example: "WHERE premium subscription active, the system SHALL enable advanced analytics"

        Output Format (YAML):
        ```yaml
        transformations:
          - id: EARS-NNN
            type: event_driven|ubiquitous|state_driven|unwanted|option
            source:
              artifact: AS-xxx|EC-xxx|FR-xxx|NFR-xxx
              text: "Original requirement text"
            ears_form:
              trigger: "..." (for event-driven)
              condition: "..." (for unwanted/state-driven)
              state: "..." (for state-driven)
              action: "..."
              outcome: "..."
            confidence: 0.XX
            ambiguity_notes: ["Any unclear aspects"]
        ```

    - role: property-extractor
      role_group: EXTRACT
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      trigger: "when extracting property candidates from spec"
      prompt: |
        Analyze specification artifacts to identify property-based testing candidates.

        Property Types to Detect:

        1. INVERSE Properties (Round-trip)
           - Pattern: Operation has a reverse that restores original state
           - Heuristics: CRUD pairs (create/delete, encode/decode, serialize/deserialize)
           - Formula: f_inverse(f(x)) == x
           - Example: "delete(create(user)) leaves no user"

        2. IDEMPOTENT Properties
           - Pattern: Applying operation multiple times equals applying once
           - Heuristics: PUT/UPDATE, normalization, sorting, deduplication
           - Formula: f(f(x)) == f(x)
           - Example: "sorting twice equals sorting once"

        3. INVARIANT Properties
           - Pattern: Condition that always holds regardless of input
           - Heuristics: Constraints, limits, business rules, NFRs
           - Formula: forall x: invariant(x) == true
           - Example: "account balance is never negative"

        4. COMMUTATIVE Properties
           - Pattern: Order of operations doesn't matter
           - Heuristics: Mathematical operations, set operations
           - Formula: f(a, b) == f(b, a)
           - Example: "adding items A then B equals adding B then A"

        5. MODEL-BASED Properties
           - Pattern: System behavior matches simplified model
           - Heuristics: State machines, workflows, business processes
           - Formula: transitions(system) ⊆ transitions(model)
           - Example: "order state transitions follow valid order lifecycle"

        6. BOUNDARY Properties
           - Pattern: Specific behavior at edge values
           - Heuristics: Min/max values, empty states, limits
           - Formula: forall x in boundary: specific_behavior(x)
           - Example: "empty list returns empty result"

        For each identified property, output:
        ```yaml
        property_candidates:
          - id: PROP-NNN
            type: inverse|idempotent|invariant|commutative|model_based|boundary
            source_artifacts: [AS-xxx, FR-xxx, EC-xxx]
            formula: "mathematical/logical formula"
            description: "Human readable description"
            priority: P1|P2|P3
            generator_hints:
              entity: "Entity name"
              valid_strategy: "How to generate valid inputs"
              boundary_strategy: "How to generate boundary inputs"
            confidence: 0.XX
        ```

    - role: entity-analyzer
      role_group: EXTRACT
      parallel: true
      depends_on: []
      priority: 10
      model_override: haiku
      trigger: "when analyzing domain entities for generators"
      prompt: |
        Analyze specification to identify domain entities for property-based test generators.

        For each entity found in spec (from Key Entities section or inferred from FRs):

        1. Extract entity structure:
           - Name and description
           - Key attributes with types
           - Constraints on each attribute
           - Relationships to other entities

        2. Identify generation strategies:
           - Valid value ranges
           - Invalid/boundary values
           - Required vs optional fields
           - Format patterns (email, UUID, etc.)

        3. Map to PBT generator primitives:
           - Strings: text(), emails(), from_regex()
           - Numbers: integers(), floats(), decimals()
           - Compound: builds(), fixed_dictionaries()
           - Special: one_of(), just(), sampled_from()

        Output Format:
        ```yaml
        entities:
          - name: User
            attributes:
              - name: email
                type: string
                constraints: ["RFC 5322 format", "unique"]
                generator: "emails()"
                boundary_generator: 'one_of(just(""), just("@"), text())'
              - name: password
                type: string
                constraints: ["min 8 chars", "has uppercase", "has digit"]
                generator: "valid_password()"
                boundary_generator: 'one_of(just(""), text(max_size=7))'
            relationships:
              - to: Account
                type: one-to-one
        ```

    # =========================================================================
    # WAVE 2: PROPERTY GENERATION (Parallel - Depends on Wave 1)
    # =========================================================================
    - role: invariant-detector
      role_group: GENERATE
      parallel: true
      depends_on: [property-extractor, ears-transformer]
      priority: 8
      model_override: sonnet
      trigger: "when generating invariant properties"
      prompt: |
        Generate INVARIANT properties from EARS transformations and property candidates.

        Focus on:
        1. NFR constraints (performance bounds, limits)
        2. Business rules that must always hold
        3. Data integrity constraints
        4. Security invariants

        For each invariant, generate:
        - PROP-xxx ID with trace to source
        - Mathematical formula
        - Generator strategy
        - Example shrunk value (minimal failing case hint)

        Output complete property definitions ready for code generation.

    - role: boundary-detector
      role_group: GENERATE
      parallel: true
      depends_on: [property-extractor, ears-transformer]
      priority: 8
      model_override: sonnet
      trigger: "when generating boundary properties"
      prompt: |
        Generate BOUNDARY properties from EARS UNWANTED forms and EC-xxx edge cases.

        Focus on:
        1. Security edge cases (injection, overflow)
        2. Validation boundaries (min/max, empty, null)
        3. Format boundaries (invalid patterns)
        4. State boundaries (empty collections, zero values)

        Each boundary property must include:
        - Specific boundary condition
        - Expected behavior (exception type, error message pattern)
        - Boundary generator strategy
        - Severity from source EC-xxx

    - role: relationship-detector
      role_group: GENERATE
      parallel: true
      depends_on: [property-extractor, ears-transformer]
      priority: 8
      model_override: sonnet
      trigger: "when generating relationship properties (inverse, idempotent, commutative)"
      prompt: |
        Generate RELATIONSHIP properties (inverse, idempotent, commutative) from spec.

        Inverse Properties:
        - Identify CRUD operation pairs
        - Encode/decode, serialize/deserialize pairs
        - Transaction commit/rollback pairs

        Idempotent Properties:
        - PUT/UPDATE operations
        - Normalization functions
        - Cache operations
        - Deduplication

        Commutative Properties:
        - Order-independent operations
        - Set operations
        - Accumulative calculations

        For each, provide complete property definition with formula and generators.

    - role: model-detector
      role_group: GENERATE
      parallel: true
      depends_on: [property-extractor, ears-transformer, entity-analyzer]
      priority: 8
      model_override: opus
      trigger: "when generating model-based properties"
      prompt: |
        Generate MODEL-BASED properties from state machines and workflows in spec.

        Detect:
        1. State transitions (order lifecycle, user states)
        2. Workflow sequences
        3. Business process models

        For each model:
        - Define simplified state model
        - List valid transitions
        - Generate model-based test structure
        - Include invariants at each state

        Use stateful testing patterns (Hypothesis stateful, fast-check model).

    - role: security-detector
      role_group: GENERATE
      parallel: true
      depends_on: [property-extractor, ears-transformer]
      priority: 9
      model_override: sonnet
      trigger: "when generating security-focused properties"
      prompt: |
        Generate SECURITY properties from spec security requirements and EC-xxx.

        Focus areas:
        1. Input validation (injection prevention)
        2. Authentication invariants
        3. Authorization boundaries
        4. Data protection properties
        5. OWASP Top 10 relevant properties

        For each security property:
        - Link to OWASP category if applicable
        - Include attack pattern generators
        - Define expected safe behavior
        - Mark as CRITICAL severity

        Security generators:
        - sql_injection_payloads()
        - xss_payloads()
        - path_traversal_payloads()
        - auth_bypass_attempts()

    # =========================================================================
    # WAVE 3: CODE GENERATION (Parallel - Depends on Wave 2)
    # =========================================================================
    - role: hypothesis-generator
      role_group: CODEGEN
      parallel: true
      depends_on: [invariant-detector, boundary-detector, relationship-detector, security-detector]
      priority: 7
      model_override: sonnet
      trigger: "when generating Python Hypothesis test code"
      prompt: |
        Generate Python Hypothesis property-based tests from properties.

        Read templates/shared/pbt/generators/python-hypothesis.md for patterns.

        For each PROP-xxx, generate:
        1. Test function with @given decorator
        2. Custom strategies for domain entities
        3. @example decorators for shrunk examples
        4. @speckit annotation for traceability
        5. Proper settings (max_examples, deadline)

        Output to: tests/properties/test_[feature]_properties.py

    - role: fastcheck-generator
      role_group: CODEGEN
      parallel: true
      depends_on: [invariant-detector, boundary-detector, relationship-detector, security-detector]
      priority: 7
      model_override: sonnet
      trigger: "when generating TypeScript fast-check test code"
      prompt: |
        Generate TypeScript fast-check property-based tests from properties.

        Read templates/shared/pbt/generators/typescript-fastcheck.md for patterns.

        For each PROP-xxx, generate:
        1. Test with fc.assert and fc.property
        2. Custom arbitraries for domain entities
        3. examples array for shrunk counterexamples
        4. @speckit annotation in docstring
        5. Proper configuration (numRuns, verbose)

        Output to: tests/properties/[feature].property.test.ts

    - role: rapid-generator
      role_group: CODEGEN
      parallel: true
      depends_on: [invariant-detector, boundary-detector, relationship-detector, security-detector]
      priority: 7
      model_override: sonnet
      trigger: "when generating Go rapid test code"
      prompt: |
        Generate Go rapid property-based tests from properties.

        Read templates/shared/pbt/generators/go-rapid.md for patterns.

        For each PROP-xxx, generate:
        1. Test function using rapid.Check
        2. Custom generators with rapid.Custom
        3. Minimal failing examples as comments
        4. @speckit annotation for traceability

        Output to: [package]_property_test.go

    - role: jqwik-generator
      role_group: CODEGEN
      parallel: true
      depends_on: [invariant-detector, boundary-detector, relationship-detector, security-detector]
      priority: 7
      model_override: sonnet
      trigger: "when generating Java jqwik test code"
      prompt: |
        Generate Java jqwik property-based tests from properties.

        Read templates/shared/pbt/generators/java-jqwik.md for patterns.

        For each PROP-xxx, generate:
        1. @Property annotated test method
        2. Custom @Provide arbitraries
        3. @Example for shrunk counterexamples
        4. @speckit annotation in Javadoc
        5. Proper configuration (tries, shrinking)

        Output to: src/test/java/[package]/[Feature]PropertyTest.java

    - role: kotest-generator
      role_group: CODEGEN
      parallel: true
      depends_on: [invariant-detector, boundary-detector, relationship-detector, security-detector]
      priority: 7
      model_override: sonnet
      trigger: "when generating Kotlin kotest-property test code"
      prompt: |
        Generate Kotlin kotest-property tests from properties.

        Read templates/shared/pbt/generators/kotlin-kotest.md for patterns.

        For each PROP-xxx, generate:
        1. PropertySpec or FunSpec with checkAll
        2. Custom Arb generators
        3. withEdgeCases for shrunk examples
        4. @speckit annotation in KDoc
        5. Proper configuration (iterations, seed)

        Output to: src/test/kotlin/[package]/[Feature]PropertyTest.kt

    # =========================================================================
    # WAVE 4: VALIDATION
    # =========================================================================
    - role: coverage-validator
      role_group: VALIDATE
      parallel: true
      depends_on: [hypothesis-generator, fastcheck-generator, rapid-generator, jqwik-generator, kotest-generator]
      priority: 6
      model_override: haiku
      trigger: "when validating property coverage"
      prompt: |
        Validate property coverage against specification requirements.

        Check:
        1. FR coverage: % of FRs with at least one PROP-xxx
        2. AS coverage: % of BOUNDARY/SECURITY AS with PROP-xxx
        3. EC coverage: % of security/validation EC with PROP-xxx
        4. Type diversity: % of property types used (target: >= 3 types)
        5. Generator quality: All entities have valid generators

        Calculate PQS (Property Quality Score):
        PQS = (
          Requirement_Coverage × 0.30 +
          Type_Diversity × 0.20 +
          Generator_Quality × 0.20 +
          Shrunk_Examples × 0.15 +
          EARS_Alignment × 0.15
        ) × 100

        Output coverage report with gaps identified.

    # =========================================================================
    # WAVE 5: PGS ITERATION (pgs profile only)
    # =========================================================================
    - role: counterexample-analyzer
      role_group: ITERATE
      parallel: false
      depends_on: [coverage-validator]
      priority: 5
      model_override: opus
      trigger: "when analyzing counterexamples in PGS mode"
      prompt: |
        Analyze counterexamples from property test execution.

        For each failing property:
        1. Examine shrunk counterexample
        2. Classify the failure:
           - PROPERTY_TOO_STRICT: Property needs relaxation
           - IMPLEMENTATION_BUG: Code needs fixing
           - SPEC_AMBIGUITY: Specification is unclear
           - GENERATOR_ISSUE: Generator producing invalid inputs

        3. Recommend resolution:
           - Refine property formula
           - Suggest implementation fix
           - Flag for /speckit.clarify
           - Adjust generator constraints

        4. Check for deception patterns:
           - Property oscillation (A→B→A)
           - Persistent counterexample
           - Coverage stagnation
           - Agent conflict

        Output resolution recommendations.

    - role: property-refiner
      role_group: ITERATE
      parallel: true
      depends_on: [counterexample-analyzer]
      priority: 4
      model_override: sonnet
      trigger: "when refining properties based on counterexamples"
      prompt: |
        Refine properties based on counterexample analysis.

        For PROPERTY_TOO_STRICT:
        - Add preconditions (assume clause)
        - Narrow generator scope
        - Add valid input filters

        For GENERATOR_ISSUE:
        - Fix generator constraints
        - Add boundary exclusions
        - Improve shrinking strategy

        Update property definitions and regenerate test code.

    - role: spec-flagger
      role_group: ITERATE
      parallel: true
      depends_on: [counterexample-analyzer]
      priority: 4
      model_override: haiku
      trigger: "when flagging spec ambiguities from PGS analysis"
      prompt: |
        Generate clarification questions for spec ambiguities.

        For each SPEC_AMBIGUITY finding:
        1. Identify the ambiguous requirement
        2. Formulate clarifying question
        3. Suggest possible interpretations
        4. Link to counterexample that exposed ambiguity

        Output in format for /speckit.clarify integration.

# =============================================================================
# VALIDATION PROFILES
# =============================================================================
validation_profiles:
  quick:
    description: "Fast property extraction without code generation"
    passes: [EXTRACT]
    gates:
      property_count:
        threshold: 5
        severity: HIGH
    timeout_seconds: 60
    output_mode: compact

  full:
    description: "Complete property extraction and code generation"
    passes: [EXTRACT, GENERATE, CODEGEN, VALIDATE]
    gates:
      property_coverage:
        threshold: 80
        severity: CRITICAL
      pqs_score:
        threshold: 80
        severity: HIGH
    timeout_seconds: 300
    output_mode: detailed

  pgs:
    description: "PGS-style collaborative agent mode with iterative refinement"
    passes: [EXTRACT, GENERATE, CODEGEN, VALIDATE, ITERATE]
    gates:
      property_coverage:
        threshold: 90
        severity: CRITICAL
      counterexample_resolution:
        threshold: 100
        severity: CRITICAL
      pqs_score:
        threshold: 85
        severity: CRITICAL
    timeout_seconds: 600
    max_iterations: 5
    output_mode: detailed
    anti_deception:
      enabled: true
      oscillation_detection: true
      stagnation_threshold: 3

# =============================================================================
# QUALITY GATES
# =============================================================================
quality_gates:
  VG-PROP:
    id: VG-PROP
    name: "Property Coverage Gate"
    pass: VALIDATE
    check: "property_coverage >= threshold"
    thresholds:
      mvp: 60
      full_feature: 80
      production: 90
    block_if: "property_coverage < threshold"
    severity: CRITICAL
    message: "Property coverage {actual}% below {threshold}%. Add properties for: {uncovered}"

  VG-EARS:
    id: VG-EARS
    name: "EARS Transformation Gate"
    pass: EXTRACT
    check: "ears_transformation_coverage >= threshold"
    thresholds:
      mvp: 70
      full_feature: 85
      production: 95
    block_if: "ears_transformation_coverage < threshold"
    severity: HIGH
    message: "EARS transformation coverage {actual}% below {threshold}%. Ambiguous requirements: {ambiguous}"

  VG-SHRUNK:
    id: VG-SHRUNK
    name: "Shrunk Example Gate"
    pass: VALIDATE
    check: "shrunk_example_count >= threshold"
    thresholds:
      default: 3
    severity: MEDIUM
    message: "Insufficient shrunk examples ({actual}/{threshold}). Run more property tests."

  VG-PGS:
    id: VG-PGS
    name: "PGS Iteration Gate"
    pass: ITERATE
    check: "unresolved_counterexamples == 0"
    trigger: "profile == pgs"
    block_if: "unresolved_counterexamples > 0"
    severity: CRITICAL
    message: "PGS mode found {unresolved} unresolved counterexamples. Review and fix."
---

## User Input

```text
$ARGUMENTS
```

## Purpose

This command extracts testable properties from specification artifacts (AS-xxx, EC-xxx, FR-xxx, NFR-xxx), transforms them through EARS intermediate representation, and generates property-based tests for comprehensive edge case discovery.

Based on:
- **PGS (Property-Generated Solver)** research: 23-37% pass@1 improvements over traditional TDD
- **Kiro IDE** methodology: Natural language → EARS → Properties → Hypothesis tests
- **Real-world validation**: PBT catching vulnerabilities that traditional testing misses

## Command Arguments

```text
/speckit.properties [OPTIONS] [FEATURE_PATH]

OPTIONS:
  --language <lang>    Target language(s): python|typescript|go|java|kotlin|all
                       Default: all (generates for detected project languages)

  --profile <name>     Execution profile:
                       - quick: Extract properties only (no code generation)
                       - full: Complete extraction and code generation (default)
                       - pgs: PGS mode with iterative refinement

  --iterations <n>     Max PGS iterations for counterexample resolution
                       Default: 5 (only applies to pgs profile)

  --coverage <n>       Minimum property coverage percentage
                       Default: 80

  --output <path>      Output directory for generated tests
                       Default: specs/[feature]/properties/

  --dry-run            Show extracted properties without generating code

  --verbose            Include EARS transformation details in output

EXAMPLES:
  /speckit.properties                              # Full extraction for active feature
  /speckit.properties --language python            # Python Hypothesis only
  /speckit.properties --profile pgs --iterations 10  # PGS mode
  /speckit.properties specs/001-user-auth/         # Specific feature path
  /speckit.properties --dry-run                    # Preview properties
```

## Execution Flow

### Phase 0: Prerequisites

```text
1. Verify spec.md exists in feature directory
2. Check for constitution.md (optional, for security context)
3. Detect project languages from:
   - package.json → TypeScript
   - pyproject.toml/setup.py → Python
   - go.mod → Go
   - pom.xml/build.gradle → Java
   - build.gradle.kts → Kotlin
4. Load existing properties.md if present (incremental mode)
```

### Phase 1: EARS Transformation

```text
Read templates/shared/pbt/ears-transformation.md

FOR EACH artifact IN spec.md:
  MATCH artifact.type:

    FR-xxx (Functional Requirement):
      IF has_trigger(artifact):
        → EARS Event-Driven
      ELIF has_state_condition(artifact):
        → EARS State-Driven
      ELSE:
        → EARS Ubiquitous

    AS-xxx (Acceptance Scenario):
      Parse Given/When/Then structure
      → EARS Event-Driven
      Category informs property type:
        - HAPPY_PATH → Inverse/Idempotent candidates
        - BOUNDARY → Boundary properties
        - SECURITY → Security properties
        - ERROR_PATH → Unwanted behavior properties

    EC-xxx (Edge Case):
      → EARS Unwanted
      Severity determines priority:
        - CRITICAL → P1, must have property
        - HIGH → P1, strongly recommended
        - MEDIUM → P2
        - LOW → P3

    NFR-xxx (Non-Functional Requirement):
      → EARS State-Driven (constraints under conditions)
      Category mapping:
        - NFR-PERF-xxx → Performance invariants
        - NFR-SEC-xxx → Security properties
        - NFR-REL-xxx → Reliability invariants

OUTPUT: ears-intermediate.yaml
```

### Phase 2: Property Extraction

```text
Read templates/shared/pbt/property-extraction.md

FOR EACH ears_form IN ears-intermediate.yaml:
  Detect property type using heuristics:

  1. INVERSE Detection:
     - CRUD operation pairs (create/delete, add/remove)
     - Encode/decode patterns
     - Serialize/deserialize
     → Formula: f_inv(f(x)) == x

  2. IDEMPOTENT Detection:
     - PUT/UPDATE operations
     - Normalization (toLowerCase, trim)
     - Sorting, deduplication
     → Formula: f(f(x)) == f(x)

  3. INVARIANT Detection:
     - Constraints with "always", "never", "must"
     - NFR bounds (latency < X, availability > Y)
     - Business rules
     → Formula: forall x: invariant(x) == true

  4. COMMUTATIVE Detection:
     - Order-independent operations
     - Set operations (union, intersection)
     - Accumulative calculations
     → Formula: f(a, b) == f(b, a)

  5. MODEL-BASED Detection:
     - State machine patterns
     - Workflow sequences
     - Lifecycle states
     → Formula: system_transitions ⊆ model_transitions

  6. BOUNDARY Detection:
     - Edge case conditions
     - Min/max values
     - Empty/null states
     → Formula: forall x in boundary: expected_behavior(x)

  FOR EACH property:
    Generate PROP-xxx ID
    Link trace: [source_artifacts]
    Create generator hints from entity analysis
    Assign priority based on source severity

OUTPUT: Property candidates with formulas
```

### Phase 3: Code Generation

```text
Read templates/shared/pbt/generators/[language].md

FOR EACH target_language:
  FOR EACH property:
    Generate test code using language template:

    Python (Hypothesis):
      - @given(generator) decorator
      - @settings(max_examples=100)
      - @example(shrunk_value) for regression
      - @speckit[PROP:xxx,AS:xxx] annotation

    TypeScript (fast-check):
      - fc.assert(fc.property(...))
      - Custom arbitraries
      - examples array
      - JSDoc with @speckit

    Go (rapid):
      - rapid.Check(t, func(t *rapid.T) {...})
      - rapid.Custom generators
      - t.Fatalf for assertions

    Java (jqwik):
      - @Property annotation
      - @Provide arbitraries
      - @Example for known cases

    Kotlin (kotest-property):
      - checkAll { ... }
      - Arb.* generators
      - withEdgeCases

OUTPUT: Test files per language in tests/properties/
```

### Phase 4: Validation

```text
Calculate coverage metrics:

FR_Coverage = FRs_with_properties / Total_FRs
AS_Coverage = Boundary_AS_with_properties / Total_Boundary_AS
EC_Coverage = Security_EC_with_properties / Total_Security_EC
Type_Diversity = Unique_property_types / 6

Calculate PQS (Property Quality Score):
PQS = (
  FR_Coverage × 0.30 +
  Type_Diversity × 0.20 +
  Generator_Quality × 0.20 +
  Shrunk_Examples × 0.15 +
  EARS_Alignment × 0.15
) × 100

Check quality gates:
- VG-PROP: property_coverage >= 80%
- VG-EARS: ears_transformation_coverage >= 85%
- VG-SHRUNK: shrunk_examples >= 3
```

### Phase 5: PGS Iteration (pgs profile only)

```text
Read templates/shared/pbt/pgs-protocol.md

WHILE iteration < max_iterations AND unresolved_counterexamples > 0:

  1. Execute property tests
  2. Capture counterexamples and shrink
  3. Analyze each counterexample:
     - PROPERTY_TOO_STRICT → Refine property
     - IMPLEMENTATION_BUG → Flag for fix
     - SPEC_AMBIGUITY → Generate clarify question
     - GENERATOR_ISSUE → Fix generator

  4. Check anti-deception:
     - Property oscillation (A→B→A pattern)
     - Persistent counterexample (same across iterations)
     - Coverage stagnation (no improvement for 3 iterations)
     - Agent conflict (contradictory outputs)

  5. Apply resolutions and regenerate

  iteration++

OUTPUT: Refined properties, resolved counterexamples, clarify questions
```

## Output Artifacts

### 1. properties.md

Main output document with all extracted properties:

```markdown
# Property-Based Testing Specification

**Feature**: {{FEATURE_ID}}
**Generated**: {{TIMESTAMP}}
**PQS**: {{SCORE}}/100

## Property Traceability Matrix
| PROP ID | Type | Source | Formula | Test File |
|---------|------|--------|---------|-----------|
| PROP-001 | inverse | AS-1A, FR-001 | delete(create(x)) == initial | test_user_properties.py |

## EARS Intermediate Forms
[EARS transformations with source mapping]

## Properties by Type
[Properties grouped by type with code examples]

## Shrunk Examples Registry
[Preserved minimal counterexamples for regression]

## Generator Definitions
[Custom generators for domain entities]

## Quality Gates Status
| Gate | Status | Value | Threshold |
```

### 2. ears-intermediate.yaml

EARS transformation intermediate representation:

```yaml
apiVersion: speckit.dev/v1
kind: EarsIntermediate
metadata:
  feature: "{{FEATURE_ID}}"
transformations:
  - id: EARS-001
    type: event_driven
    source: {artifact: AS-1A, text: "..."}
    ears_form: {trigger: "...", action: "...", outcome: "..."}
    properties_derived: [PROP-001, PROP-002]
```

### 3. Test Files

Generated property test files per language:
- `tests/properties/test_[feature]_properties.py`
- `tests/properties/[feature].property.test.ts`
- `[package]_property_test.go`
- `src/test/java/[package]/[Feature]PropertyTest.java`
- `src/test/kotlin/[package]/[Feature]PropertyTest.kt`

## Integration Points

### With /speckit.specify

Properties can be fed back to spec.md:
- New EC-xxx from discovered edge cases
- Property hints in "Property-Based Testing Hints" section

### With /speckit.tasks

PBT tasks are added to tasks.md:
- TASK-PBT-xxx with property references
- Dependency on implementation tasks

### With /speckit.analyze

New validation pass W2 checks property coverage:
- VG-PROP quality gate
- PQS in quality metrics

### With /speckit.implement

PBT tests run in testing wave:
- pytest for Hypothesis
- npm test for fast-check
- go test for rapid
- mvn test for jqwik
- gradle test for kotest

## Success Metrics

| Metric | Target |
|--------|--------|
| Property Coverage | >= 80% |
| EARS Transformation | >= 85% |
| Type Diversity | >= 3 types |
| PQS Score | >= 80 |
| Shrunk Examples | >= 3 |

## Troubleshooting

### Low Property Coverage

1. Check if FRs have clear testable criteria
2. Verify AS scenarios have concrete Given/When/Then
3. Add EC-xxx for security and boundary cases
4. Run /speckit.clarify for ambiguous requirements

### PGS Mode Not Converging

1. Check for property oscillation (inspect iteration history)
2. Verify generators produce valid domain inputs
3. Consider if spec is inherently ambiguous
4. Reduce max_iterations and review manually

### Generator Issues

1. Ensure entity attributes have clear constraints
2. Check for circular dependencies in generators
3. Add explicit boundary exclusions
4. Review generated generators in properties.md

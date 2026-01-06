# Self-Review Criteria: Specification (SR-SPEC)

> Validation criteria for `/speckit.specify` output. Import in self-review phase.

## Purpose

Ensure specification artifacts meet quality standards for:
1. Completeness - all required sections filled
2. Traceability - all IDs properly linked
3. Testability - acceptance scenarios are verifiable
4. Security - edge cases cover security triggers
5. Entity coverage - validation for detected entity types

---

## Criteria Table

| ID | Name | Description | Severity | Auto-Fix |
|----|------|-------------|----------|----------|
| SR-SPEC-01 | All FRs Have AS | Every FR-xxx links to at least one AS-xxx | CRITICAL | ❌ |
| SR-SPEC-02 | AS Format Valid | All AS use Given/When/Then format | HIGH | ✅ |
| SR-SPEC-03 | EC Coverage | At least 3 edge cases per user story | MEDIUM | ❌ |
| SR-SPEC-04 | Priority Assigned | All user stories have P1/P2/P3 priority | HIGH | ❌ |
| SR-SPEC-05 | Success Criteria | At least 3 measurable SC-xxx items | HIGH | ❌ |
| SR-SPEC-06 | No Placeholders | No TODO, TBD, FIXME, [placeholder] markers | HIGH | ❌ |
| SR-SPEC-07 | ID Uniqueness | No duplicate AS-xxx, EC-xxx, FR-xxx IDs | CRITICAL | ✅ |
| SR-SPEC-08 | Story Independence | Each user story testable independently | MEDIUM | ❌ |
| SR-SPEC-09 | Technical Deps | External APIs/packages documented with versions | MEDIUM | ❌ |
| SR-SPEC-10 | Traceability Summary | FR → AS → EC links complete | HIGH | ✅ |
| SR-SPEC-11 | AC Completeness Score | Acceptance criteria completeness >= 0.80 | HIGH | ❌ |
| SR-SPEC-12 | Entity Type Coverage | All detected entity types have heuristic edge cases | MEDIUM | ✅ |
| SR-SPEC-13 | Security EC Coverage | Security edge cases for auth/input/session features | HIGH | ❌ |
| SR-SPEC-14 | No Vague Terms | No "fast", "user-friendly", etc. without metrics | HIGH | ❌ |
| SR-SPEC-15 | Quantities Defined | All "some/many/few" have specific numbers | MEDIUM | ❌ |
| SR-SPEC-16 | Error Path Coverage | Ratio of error:happy scenarios >= 0.5 | HIGH | ❌ |
| SR-SPEC-17 | Security Triggers Covered | All auth/input/file triggers have security reqs | CRITICAL | ❌ |
| SR-SPEC-18 | Completeness Score | Overall completeness >= 0.75 | HIGH | ❌ |
| SR-SPEC-19 | Quality Score Pass | Overall G-Eval quality score >= 70 (Grade C+) | HIGH | ❌ |
| SR-SPEC-20 | No Failing Dimensions | All quality dimensions score >= 0.50 | MEDIUM | ❌ |
| SR-SPEC-21 | Consistency Check | No CRITICAL contradictions detected | CRITICAL | ❌ |
| SR-SPEC-22 | Scenario Confidence | All acceptance scenarios have confidence >= 0.70 | MEDIUM | ❌ |

---

## Detailed Criteria

### SR-SPEC-01: All FRs Have AS

```text
SR-SPEC-01:
  severity: CRITICAL
  auto_fixable: false

  check_fn(artifact):
    fr_ids = EXTRACT_IDS(artifact, pattern="FR-\\d+")
    as_ids = EXTRACT_IDS(artifact, pattern="AS-\\d+[A-Z]?")

    FOR fr_id IN fr_ids:
      linked_as = FIND_LINKED_AS(artifact, fr_id)
      IF linked_as.length == 0:
        RETURN {status: FAIL, details: "{fr_id} has no linked AS"}

    RETURN {status: PASS}
```

---

### SR-SPEC-02: AS Format Valid

```text
SR-SPEC-02:
  severity: HIGH
  auto_fixable: true

  check_fn(artifact):
    as_tables = FIND_TABLES(artifact, header_pattern="Given.*When.*Then")
    invalid = []

    FOR table IN as_tables:
      FOR row IN table.rows:
        IF row.given IS EMPTY OR row.when IS EMPTY OR row.then IS EMPTY:
          invalid.append(row.id)

    IF invalid.length > 0:
      RETURN {status: FAIL, details: "Invalid AS format: {invalid.join(', ')}"}
    RETURN {status: PASS}

  fix_fn(artifact, issue):
    # Attempt to reformat AS rows with placeholder text
    FOR id IN issue.invalid:
      IF row.given IS EMPTY:
        row.given = "[state to be defined]"
      # Similar for when/then
    RETURN artifact
```

---

### SR-SPEC-03: EC Coverage

```text
SR-SPEC-03:
  severity: MEDIUM
  auto_fixable: false

  check_fn(artifact):
    user_stories = COUNT_USER_STORIES(artifact)
    ec_count = COUNT_IDS(artifact, pattern="EC-\\d+")

    min_expected = user_stories * 3
    IF ec_count < min_expected:
      RETURN {status: FAIL, details: "{ec_count} EC found, need at least {min_expected}"}
    RETURN {status: PASS}
```

---

### SR-SPEC-04: Priority Assigned

```text
SR-SPEC-04:
  severity: HIGH
  auto_fixable: false

  check_fn(artifact):
    stories = FIND_USER_STORIES(artifact)
    unassigned = []

    FOR story IN stories:
      IF NOT story.priority MATCHES /P[1-3][a-z]?/:
        unassigned.append(story.title)

    IF unassigned.length > 0:
      RETURN {status: FAIL, details: "No priority: {unassigned.join(', ')}"}
    RETURN {status: PASS}
```

---

### SR-SPEC-05: Success Criteria

```text
SR-SPEC-05:
  severity: HIGH
  auto_fixable: false

  check_fn(artifact):
    sc_ids = EXTRACT_IDS(artifact, pattern="SC-\\d+")

    IF sc_ids.length < 3:
      RETURN {status: FAIL, details: "Only {sc_ids.length} success criteria (need 3+)"}
    RETURN {status: PASS}
```

---

### SR-SPEC-06: No Placeholders

```text
SR-SPEC-06:
  severity: HIGH
  auto_fixable: false

  check_fn(artifact):
    PLACEHOLDER_PATTERNS = [
      "TODO", "TBD", "FIXME", "XXX",
      "[placeholder]", "[to be defined]", "[NEEDS CLARIFICATION]"
    ]

    matches = []
    FOR pattern IN PLACEHOLDER_PATTERNS:
      IF CONTAINS(artifact.content, pattern):
        matches.append(pattern)

    IF matches.length > 0:
      RETURN {status: FAIL, details: "Found placeholders: {matches.join(', ')}"}
    RETURN {status: PASS}
```

---

### SR-SPEC-07: ID Uniqueness

```text
SR-SPEC-07:
  severity: CRITICAL
  auto_fixable: true

  check_fn(artifact):
    all_ids = EXTRACT_IDS(artifact, pattern="(AS|EC|FR|SC|VR|IR)-\\d+[A-Z]?")
    duplicates = FIND_DUPLICATES(all_ids)

    IF duplicates.length > 0:
      RETURN {status: FAIL, details: "Duplicate IDs: {duplicates.join(', ')}"}
    RETURN {status: PASS}

  fix_fn(artifact, issue):
    FOR dup_id IN issue.duplicates:
      occurrences = FIND_ALL_OCCURRENCES(artifact, dup_id)
      FOR i, occurrence IN occurrences[1:]:  # Skip first, renumber rest
        new_id = INCREMENT_ID(dup_id, i)
        REPLACE(artifact, occurrence, new_id)
    RETURN artifact
```

---

### SR-SPEC-08: Story Independence

```text
SR-SPEC-08:
  severity: MEDIUM
  auto_fixable: false

  check_fn(artifact):
    stories = FIND_USER_STORIES(artifact)

    FOR story IN stories:
      IF NOT HAS_SECTION(story, "Independent Test"):
        RETURN {status: FAIL, details: "Story '{story.title}' missing Independent Test section"}
      IF story.independent_test CONTAINS "depends on" OR story.independent_test CONTAINS "requires":
        RETURN {status: FAIL, details: "Story '{story.title}' not independently testable"}

    RETURN {status: PASS}
```

---

### SR-SPEC-09: Technical Deps

```text
SR-SPEC-09:
  severity: MEDIUM
  auto_fixable: false

  check_fn(artifact):
    # Check if Technical Dependencies section exists when external deps mentioned
    external_mentions = FIND_PATTERNS(artifact, ["API", "npm", "pip", "package", "library"])

    IF external_mentions.length > 0:
      IF NOT HAS_SECTION(artifact, "Technical Dependencies"):
        RETURN {status: FAIL, details: "External dependencies mentioned but Technical Dependencies section missing"}

      deps_section = GET_SECTION(artifact, "Technical Dependencies")
      IF NOT CONTAINS_VERSION_INFO(deps_section):
        RETURN {status: FAIL, details: "Technical Dependencies missing version info"}

    RETURN {status: PASS}
```

---

### SR-SPEC-10: Traceability Summary

```text
SR-SPEC-10:
  severity: HIGH
  auto_fixable: true

  check_fn(artifact):
    IF NOT HAS_SECTION(artifact, "Traceability Summary"):
      RETURN {status: FAIL, details: "Traceability Summary section missing"}

    fr_ids = EXTRACT_IDS(artifact, pattern="FR-\\d+")
    traceability = GET_SECTION(artifact, "Traceability Summary")

    missing = []
    FOR fr_id IN fr_ids:
      IF fr_id NOT IN traceability:
        missing.append(fr_id)

    IF missing.length > 0:
      RETURN {status: FAIL, details: "Missing from traceability: {missing.join(', ')}"}
    RETURN {status: PASS}

  fix_fn(artifact, issue):
    traceability = GET_SECTION(artifact, "Traceability Summary")
    FOR fr_id IN issue.missing:
      linked_as = FIND_LINKED_AS(artifact, fr_id)
      ADD_ROW(traceability, {requirement: fr_id, scenarios: linked_as, status: "Defined"})
    RETURN artifact
```

---

### SR-SPEC-11: AC Completeness Score (NEW)

```text
SR-SPEC-11:
  severity: HIGH
  auto_fixable: false
  reference: "templates/shared/quality/edge-case-heuristics.md"

  check_fn(artifact):
    # Completeness score from acceptance-criteria-generator
    # Score formula: (happy + error + boundary + security + entities) / max_possible

    scenarios = EXTRACT_AS(artifact)

    classification_counts = {
      HAPPY_PATH: 0,
      ALT_PATH: 0,
      ERROR_PATH: 0,
      BOUNDARY: 0,
      SECURITY: 0
    }

    FOR scenario IN scenarios:
      classification_counts[scenario.classification] += 1

    # Scoring: minimum 1 of each type for completeness
    happy_score = MIN(1.0, classification_counts.HAPPY_PATH / 1)
    error_score = MIN(1.0, classification_counts.ERROR_PATH / 1)
    boundary_score = MIN(1.0, classification_counts.BOUNDARY / 1)

    # Entity coverage score
    entities_detected = DETECT_ENTITIES(artifact)
    entities_covered = COUNT_EC_BY_ENTITY(artifact, entities_detected)
    entity_score = entities_covered / MAX(entities_detected.length, 1)

    completeness_score = (happy_score + error_score + boundary_score + entity_score) / 4

    IF completeness_score < 0.80:
      RETURN {
        status: FAIL,
        details: "Completeness score {completeness_score:.2f} < 0.80 threshold",
        breakdown: {happy: happy_score, error: error_score, boundary: boundary_score, entity: entity_score}
      }

    RETURN {status: PASS, details: "Completeness score {completeness_score:.2f}"}
```

---

### SR-SPEC-12: Entity Type Coverage (NEW)

```text
SR-SPEC-12:
  severity: MEDIUM
  auto_fixable: true
  reference: "templates/shared/quality/edge-case-heuristics.md"

  check_fn(artifact):
    # Import entity detection from edge-case-heuristics.md
    LOAD DETECT_ENTITY_TYPE from "templates/shared/quality/edge-case-heuristics.md"

    # Extract entities from spec
    entities = EXTRACT_ENTITIES(artifact)
    edge_cases = EXTRACT_EDGE_CASES(artifact)

    uncovered = []
    FOR entity IN entities:
      entity_type = DETECT_ENTITY_TYPE(entity.name, entity.context)

      # Count EC for this entity type
      entity_ec = FILTER(edge_cases, ec =>
        ec.category == "validation" AND
        ec.condition CONTAINS entity.name
      )

      # Minimum expected EC by type (from heuristics)
      min_expected = {
        email: 3, password: 4, file: 4, string: 3,
        numeric: 3, date: 3, url: 3, phone: 2,
        array: 2, boolean: 1, id: 2
      }[entity_type] OR 2

      IF entity_ec.length < min_expected:
        uncovered.append({
          name: entity.name,
          type: entity_type,
          found: entity_ec.length,
          expected: min_expected
        })

    IF uncovered.length > 0:
      names = uncovered.map(e => "{e.name} ({e.found}/{e.expected})")
      RETURN {
        status: FAIL,
        details: "Missing EC for entities: {names.join(', ')}",
        uncovered: uncovered
      }

    RETURN {status: PASS, details: "All {entities.length} entities have heuristic EC"}

  fix_fn(artifact, issue):
    LOAD GENERATE_HEURISTIC_EDGE_CASES from "templates/shared/quality/edge-case-heuristics.md"

    FOR entity IN issue.uncovered:
      new_ec = GENERATE_HEURISTIC_EDGE_CASES([entity])
      APPEND_TO_EDGE_CASES(artifact, new_ec)

    RETURN artifact
```

---

### SR-SPEC-13: Security EC Coverage (NEW)

```text
SR-SPEC-13:
  severity: HIGH
  auto_fixable: false
  reference: "templates/shared/quality/security-patterns.md"

  check_fn(artifact):
    # Import security detection from security-patterns.md
    LOAD DETECT_SECURITY_TRIGGERS from "templates/shared/quality/security-patterns.md"
    LOAD CALCULATE_SECURITY_COVERAGE from "templates/shared/quality/security-patterns.md"

    # Extract requirements text
    requirements = EXTRACT_REQUIREMENTS(artifact)
    requirements_text = JOIN(requirements, " ")

    # Detect security triggers
    triggers = DETECT_SECURITY_TRIGGERS(requirements_text)

    IF triggers.length == 0:
      RETURN {status: PASS, details: "No security features detected"}

    # Get existing edge cases
    edge_cases = EXTRACT_EDGE_CASES(artifact)
    security_ec = FILTER(edge_cases, ec => ec.category == "security")

    # Calculate coverage
    coverage = CALCULATE_SECURITY_COVERAGE(triggers, security_ec)

    IF coverage.score < 1.0:
      uncovered = FILTER(coverage.category_details, d => d.status != "covered")
      categories = uncovered.map(c => c.category)
      RETURN {
        status: FAIL,
        details: "Missing security EC for: {categories.join(', ')}",
        triggers: triggers,
        coverage: coverage
      }

    RETURN {
      status: PASS,
      details: "{triggers.length} security categories covered ({security_ec.length} EC)"
    }
```

---

### SR-SPEC-14: No Vague Terms (NEW)

```text
SR-SPEC-14:
  severity: HIGH
  auto_fixable: false
  reference: "templates/shared/quality/ambiguity-patterns.md"

  check_fn(artifact):
    # Import vague term patterns from ambiguity-patterns.md
    LOAD VAGUE_TERM_PATTERNS from "templates/shared/quality/ambiguity-patterns.md"

    requirements = EXTRACT_REQUIREMENTS(artifact)
    vague_terms_found = []

    FOR requirement IN requirements:
      FOR category, config IN VAGUE_TERM_PATTERNS:
        matches = REGEX_MATCH(requirement.text, config.pattern, IGNORE_CASE)
        FOR match IN matches:
          # Check if term has associated metric
          IF NOT HAS_ASSOCIATED_METRIC(requirement, match):
            vague_terms_found.append({
              requirement_id: requirement.id,
              term: match,
              category: category,
              suggestion: config.suggestion
            })

    IF vague_terms_found.length > 0:
      terms = vague_terms_found.map(t => "{t.requirement_id}: '{t.term}'")
      RETURN {
        status: FAIL,
        details: "Vague terms without metrics: {terms.join(', ')}",
        vague_terms: vague_terms_found
      }

    RETURN {status: PASS, details: "No unmeasured vague terms found"}
```

---

### SR-SPEC-15: Quantities Defined (NEW)

```text
SR-SPEC-15:
  severity: MEDIUM
  auto_fixable: false
  reference: "templates/shared/quality/ambiguity-patterns.md"

  check_fn(artifact):
    # Import quantity patterns from ambiguity-patterns.md
    LOAD MISSING_QUANTITY_PATTERNS from "templates/shared/quality/ambiguity-patterns.md"

    QUANTITY_VAGUE_TERMS = ["some", "many", "few", "several", "most", "numerous", "various", "multiple"]

    requirements = EXTRACT_REQUIREMENTS(artifact)
    undefined_quantities = []

    FOR requirement IN requirements:
      FOR term IN QUANTITY_VAGUE_TERMS:
        IF CONTAINS(requirement.text.lower(), term):
          # Check if there's an explicit number nearby
          IF NOT HAS_EXPLICIT_QUANTITY(requirement.text):
            undefined_quantities.append({
              requirement_id: requirement.id,
              term: term,
              context: EXTRACT_PHRASE(requirement.text, term)
            })

    IF undefined_quantities.length > 0:
      items = undefined_quantities.map(q => "{q.requirement_id}: '{q.term}'")
      RETURN {
        status: FAIL,
        details: "Undefined quantities: {items.join(', ')}",
        undefined: undefined_quantities
      }

    RETURN {status: PASS, details: "All quantities explicitly defined"}
```

---

### SR-SPEC-16: Error Path Coverage (NEW)

```text
SR-SPEC-16:
  severity: HIGH
  auto_fixable: false
  reference: "templates/shared/quality/completeness-checklist.md"

  check_fn(artifact):
    # Count scenarios by classification
    scenarios = EXTRACT_AS(artifact)

    happy_path_count = COUNT(scenarios, s => s.classification == "HAPPY_PATH")
    error_path_count = COUNT(scenarios, s => s.classification == "ERROR_PATH")

    # Also count edge cases with error handling
    edge_cases = EXTRACT_EC(artifact)
    error_ec_count = COUNT(edge_cases, ec => ec.category == "error" OR ec.category == "validation")

    total_error_coverage = error_path_count + error_ec_count
    ratio = total_error_coverage / MAX(happy_path_count, 1)

    IF ratio < 0.5:
      RETURN {
        status: FAIL,
        details: "Error path ratio {ratio:.2f} < 0.5 ({total_error_coverage} error vs {happy_path_count} happy)",
        breakdown: {
          happy_path: happy_path_count,
          error_path: error_path_count,
          error_ec: error_ec_count,
          ratio: ratio
        }
      }

    RETURN {
      status: PASS,
      details: "Error path ratio {ratio:.2f} >= 0.5"
    }
```

---

### SR-SPEC-17: Security Triggers Covered (NEW)

```text
SR-SPEC-17:
  severity: CRITICAL
  auto_fixable: false
  reference: "templates/shared/quality/completeness-checklist.md"

  check_fn(artifact):
    # Import security triggers from completeness-checklist.md
    LOAD CHECK_SECURITY_REQUIREMENTS from "templates/shared/quality/completeness-checklist.md"

    security_check = CHECK_SECURITY_REQUIREMENTS(artifact)

    # Extract all detected triggers
    triggers = security_check.detected_triggers

    IF triggers.length == 0:
      RETURN {status: PASS, details: "No security triggers detected"}

    # Check coverage for each trigger
    uncovered = []
    FOR trigger IN triggers:
      IF NOT security_check.has_requirement_for(trigger):
        uncovered.append(trigger)

    IF uncovered.length > 0:
      RETURN {
        status: FAIL,
        details: "Security triggers without requirements: {uncovered.join(', ')}",
        triggers: triggers,
        uncovered: uncovered
      }

    RETURN {
      status: PASS,
      details: "All {triggers.length} security triggers have requirements"
    }
```

---

### SR-SPEC-18: Completeness Score (NEW)

```text
SR-SPEC-18:
  severity: HIGH
  auto_fixable: false
  reference: "templates/shared/quality/completeness-checklist.md"

  check_fn(artifact):
    # Import completeness calculation from completeness-checklist.md
    LOAD CALCULATE_COMPLETENESS_SCORE from "templates/shared/quality/completeness-checklist.md"

    result = CALCULATE_COMPLETENESS_SCORE(artifact)

    IF result.score < 0.75:
      # Build breakdown report
      breakdown_items = []
      FOR category, score IN result.category_scores:
        status = "✅" IF score >= 0.75 ELSE "⚠️" IF score >= 0.50 ELSE "❌"
        breakdown_items.append("{status} {category}: {score:.2f}")

      RETURN {
        status: FAIL,
        details: "Completeness score {result.score:.2f} < 0.75 threshold",
        breakdown: breakdown_items.join("\n"),
        gaps: result.gaps
      }

    RETURN {
      status: PASS,
      details: "Completeness score {result.score:.2f} >= 0.75"
    }
```

---

### SR-SPEC-19: Quality Score Pass (NEW)

```text
SR-SPEC-19:
  severity: HIGH
  auto_fixable: false
  reference: "templates/shared/quality/spec-quality-scorer.md"

  check_fn(artifact):
    # Import quality scoring from spec-quality-scorer.md
    LOAD SCORE_SPECIFICATION from "templates/shared/quality/spec-quality-scorer.md"

    # Get quality score result
    quality_result = SCORE_SPECIFICATION(artifact)

    IF quality_result.overall_score < 70.0:
      RETURN {
        status: FAIL,
        details: "Quality score {quality_result.overall_score:.1f} < 70 (Grade: {quality_result.grade})",
        score: quality_result.overall_score,
        grade: quality_result.grade,
        dimensions: quality_result.dimensions,
        recommendation: quality_result.recommendation
      }

    RETURN {
      status: PASS,
      details: "Quality score {quality_result.overall_score:.1f} (Grade: {quality_result.grade})"
    }
```

---

### SR-SPEC-20: No Failing Dimensions (NEW)

```text
SR-SPEC-20:
  severity: MEDIUM
  auto_fixable: false
  reference: "templates/shared/quality/spec-quality-scorer.md"

  check_fn(artifact):
    # Import quality scoring from spec-quality-scorer.md
    LOAD SCORE_SPECIFICATION from "templates/shared/quality/spec-quality-scorer.md"

    quality_result = SCORE_SPECIFICATION(artifact)

    # Check each dimension for minimum threshold
    failing_dimensions = []
    FOR dimension IN quality_result.dimensions:
      IF dimension.score < 0.50:
        failing_dimensions.append({
          name: dimension.name,
          score: dimension.score,
          weight: dimension.weight,
          suggestions: dimension.improvement_suggestions
        })

    IF failing_dimensions.length > 0:
      names = failing_dimensions.map(d => "{d.name}: {d.score:.2f}")
      RETURN {
        status: FAIL,
        details: "Failing dimensions (< 0.50): {names.join(', ')}",
        failing_dimensions: failing_dimensions
      }

    RETURN {
      status: PASS,
      details: "All {quality_result.dimensions.length} dimensions >= 0.50"
    }
```

---

### SR-SPEC-21: Consistency Check (NEW)

```text
SR-SPEC-21:
  severity: CRITICAL
  auto_fixable: false
  reference: "templates/shared/quality/spec-quality-scorer.md"

  check_fn(artifact):
    # Import consistency evaluation from spec-quality-scorer.md
    LOAD EVALUATE_CONSISTENCY from "templates/shared/quality/spec-quality-scorer.md"

    consistency_result = EVALUATE_CONSISTENCY(artifact)

    # Check for CRITICAL contradictions
    critical_contradictions = FILTER(
      consistency_result.contradictions,
      c => c.severity == "CRITICAL"
    )

    IF critical_contradictions.length > 0:
      contradiction_desc = critical_contradictions.map(c =>
        "{c.req_a} vs {c.req_b}: {c.type}"
      )
      RETURN {
        status: FAIL,
        details: "CRITICAL contradictions: {contradiction_desc.join('; ')}",
        contradictions: critical_contradictions,
        total_contradictions: consistency_result.contradictions.length
      }

    # Warn for HIGH severity contradictions
    high_contradictions = FILTER(
      consistency_result.contradictions,
      c => c.severity == "HIGH"
    )

    IF high_contradictions.length > 0:
      RETURN {
        status: WARN,
        details: "{high_contradictions.length} HIGH severity contradictions",
        contradictions: high_contradictions
      }

    RETURN {
      status: PASS,
      details: "No CRITICAL contradictions (consistency score: {consistency_result.score:.2f})"
    }
```

---

### SR-SPEC-22: Scenario Confidence (NEW v0.0.80)

```text
SR-SPEC-22:
  severity: MEDIUM
  auto_fixable: false
  reference: "AI_AUGMENTED_SPEC_ARCHITECTURE.md section 1.1"

  check_fn(artifact):
    # Extract all acceptance scenarios with confidence scores
    scenarios = EXTRACT_SCENARIOS(artifact)

    IF scenarios.length == 0:
      RETURN {status: SKIP, details: "No acceptance scenarios found"}

    # Filter scenarios with confidence_score field
    scenarios_with_confidence = FILTER(scenarios, s => s.confidence_score IS DEFINED)

    IF scenarios_with_confidence.length == 0:
      RETURN {
        status: WARN,
        details: "No scenarios have confidence_score field (legacy spec)"
      }

    # Check for low confidence scenarios
    low_confidence = FILTER(
      scenarios_with_confidence,
      s => s.confidence_score < 0.70
    )

    IF low_confidence.length > 0:
      scenario_ids = low_confidence.map(s => s.id).join(', ')
      avg_confidence = SUM(low_confidence.map(s => s.confidence_score)) / low_confidence.length

      RETURN {
        status: FAIL,
        details: "{low_confidence.length} scenarios with confidence < 0.70: {scenario_ids}",
        avg_low_confidence: avg_confidence,
        recommendation: "Review and clarify Given/When/Then, ensure measurable outcomes"
      }

    # Calculate overall confidence
    avg_confidence = SUM(scenarios_with_confidence.map(s => s.confidence_score)) / scenarios_with_confidence.length

    RETURN {
      status: PASS,
      details: "All {scenarios_with_confidence.length} scenarios have confidence >= 0.70 (avg: {avg_confidence:.2f})",
      avg_confidence: avg_confidence
    }

  remediation:
    """
    For scenarios with confidence < 0.70:

    1. **Review Given clause**: Is the initial state specific enough?
       - ❌ "User on homepage"
       - ✅ "User on homepage, logged in, cart contains 2 items"

    2. **Review When clause**: Is the action clear and atomic?
       - ❌ "User completes checkout"
       - ✅ "User clicks 'Place Order' button"

    3. **Review Then clause**: Is the outcome measurable?
       - ❌ "Order is processed successfully"
       - ✅ "Order confirmation displayed, confirmation email sent to user@example.com, order ID >= 1000"

    4. **Check reasoning field**: Does it explain why this scenario is essential?
       - If reasoning is vague or missing, add 1-2 sentences explaining the risk this scenario mitigates

    5. **Consider splitting**: If scenario covers multiple concerns, split into separate scenarios
       - Example: "User registration and profile update" → split into AS-1A (registration) and AS-1B (profile update)
    """
```

---

## Integration with Self-Review Framework

```text
# In specify.md self-review phase:

SPEC_CRITERIA = [
  SR-SPEC-01, SR-SPEC-02, SR-SPEC-03, SR-SPEC-04, SR-SPEC-05,
  SR-SPEC-06, SR-SPEC-07, SR-SPEC-08, SR-SPEC-09, SR-SPEC-10,
  SR-SPEC-11, SR-SPEC-12, SR-SPEC-13,  # AC completeness + Edge case coverage
  SR-SPEC-14, SR-SPEC-15, SR-SPEC-16, SR-SPEC-17, SR-SPEC-18,  # Ambiguity + Completeness
  SR-SPEC-19, SR-SPEC-20, SR-SPEC-21,  # G-Eval quality scoring + Consistency
  SR-SPEC-22  # NEW v0.0.80: AI confidence scoring
]

# Criteria activated by complexity tier:
TIER_CRITERIA = {
  TRIVIAL: [SR-SPEC-01, SR-SPEC-02, SR-SPEC-07],  # Critical only
  SIMPLE: [SR-SPEC-01..SR-SPEC-06, SR-SPEC-07],
  MODERATE: [SR-SPEC-01..SR-SPEC-13, SR-SPEC-14, SR-SPEC-15, SR-SPEC-16, SR-SPEC-19],  # + Quality score
  COMPLEX: [SR-SPEC-01..SR-SPEC-22]  # All including G-Eval quality + consistency + AI confidence
}
```

---

## Quality Gate Thresholds

| Severity | Threshold for FAIL | Threshold for WARN |
|----------|-------------------|-------------------|
| CRITICAL | >= 1 | N/A |
| HIGH | >= 3 | >= 1 |
| MEDIUM | >= 5 | >= 3 |
| LOW | N/A | >= 5 |

**Minimum Quality Score**: 80% for PASS verdict

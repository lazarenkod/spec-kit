# Edge Case Heuristics by Entity Type

> Systematic edge case discovery based on data entity types. Import this module in acceptance-criteria-generator and edge-case-detector subagents.

## Purpose

Prevent specifications from missing predictable edge cases by:
1. Automatically detecting entity types from field names
2. Applying type-specific edge case patterns
3. Assigning appropriate severity levels
4. Ensuring comprehensive validation coverage

---

## Entity Type Detection

```text
DETECT_ENTITY_TYPE(field_name, context):

  field_lower = field_name.lower()

  # Email patterns
  IF field_lower MATCHES /email|e-mail|mail_address|user_email/:
    RETURN "email"

  # Phone patterns
  IF field_lower MATCHES /phone|tel|mobile|cell|fax|sms/:
    RETURN "phone"

  # Date/time patterns
  IF field_lower MATCHES /date|time|timestamp|created|updated|expires|birth|deadline|scheduled/:
    RETURN "date"

  # Numeric patterns
  IF field_lower MATCHES /amount|price|cost|quantity|count|total|score|age|size|limit|rate|percent/:
    RETURN "numeric"

  # Password patterns
  IF field_lower MATCHES /password|passwd|secret|pin|code|token|key/:
    RETURN "password"

  # File patterns
  IF field_lower MATCHES /file|upload|attachment|document|image|photo|avatar|media/:
    RETURN "file"

  # URL patterns
  IF field_lower MATCHES /url|link|href|uri|website|endpoint/:
    RETURN "url"

  # Array/collection patterns
  IF field_lower MATCHES /list|items|tags|options|selections|choices|categories/:
    RETURN "array"

  # Boolean patterns
  IF field_lower MATCHES /is_|has_|can_|should_|enabled|active|visible|flag/:
    RETURN "boolean"

  # ID/reference patterns
  IF field_lower MATCHES /id$|_id$|uuid|guid|ref|reference/:
    RETURN "id"

  # Default
  RETURN "string"
```

---

## Edge Cases by Type

### Email Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-EMAIL-001 | Invalid format (missing @) | Return validation error with specific message | HIGH |
| EC-EMAIL-002 | Duplicate (already exists) | Return conflict error (HTTP 409) | HIGH |
| EC-EMAIL-003 | With + alias (user+tag@domain) | Accept and normalize | LOW |
| EC-EMAIL-004 | Internationalized domain (IDN) | Accept Unicode domains per RFC 6531 | LOW |
| EC-EMAIL-005 | Very long local part (>64 chars) | Return validation error | MEDIUM |
| EC-EMAIL-006 | Empty string | Return required field error | HIGH |
| EC-EMAIL-007 | Disposable email domain | Warn or reject per business rule | MEDIUM |

---

### Phone Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-PHONE-001 | Invalid characters (letters, special) | Return validation error | HIGH |
| EC-PHONE-002 | Missing country code | Require or infer from context | MEDIUM |
| EC-PHONE-003 | With spaces/dashes/parentheses | Accept and normalize to E.164 | LOW |
| EC-PHONE-004 | Too short (<7 digits) | Return validation error | MEDIUM |
| EC-PHONE-005 | Too long (>15 digits) | Return validation error | MEDIUM |
| EC-PHONE-006 | Empty string | Return required field error | HIGH |

---

### Date Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-DATE-001 | Past date (when future required) | Return validation error | HIGH |
| EC-DATE-002 | Future date (when past required) | Return validation error | HIGH |
| EC-DATE-003 | Far past (>100 years ago) | Return validation error | MEDIUM |
| EC-DATE-004 | Far future (>100 years ahead) | Return validation error | MEDIUM |
| EC-DATE-005 | Invalid date (Feb 30, Apr 31) | Return validation error | HIGH |
| EC-DATE-006 | Timezone edge (DST transition) | Handle timezone correctly | MEDIUM |
| EC-DATE-007 | Leap year edge (Feb 29) | Accept in leap years only | MEDIUM |
| EC-DATE-008 | Null/empty (optional field) | Accept as unset | LOW |
| EC-DATE-009 | Date range inverted (start > end) | Return validation error | HIGH |

---

### Numeric Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-NUM-001 | Negative (when positive required) | Return validation error | HIGH |
| EC-NUM-002 | Zero value | Handle explicitly per business rule | HIGH |
| EC-NUM-003 | Exceeds max safe integer (>2^53-1) | Return validation error | MEDIUM |
| EC-NUM-004 | Decimal (when integer required) | Return validation error or truncate | MEDIUM |
| EC-NUM-005 | NaN or Infinity | Return validation error | HIGH |
| EC-NUM-006 | Leading zeros (0042) | Accept and normalize | LOW |
| EC-NUM-007 | Scientific notation (1e10) | Accept or reject per context | LOW |
| EC-NUM-008 | Currency precision (>2 decimals) | Round or reject | MEDIUM |

---

### String Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-STR-001 | Empty string | Return required error or accept default | HIGH |
| EC-STR-002 | Only whitespace | Trim and validate as empty | HIGH |
| EC-STR-003 | SQL injection attempt (`'; DROP TABLE`) | Sanitize/reject, log attempt | CRITICAL |
| EC-STR-004 | XSS payload (`<script>`, `onclick`) | Sanitize/reject, log attempt | CRITICAL |
| EC-STR-005 | Exceeds max length | Truncate or return error | MEDIUM |
| EC-STR-006 | Unicode characters (emoji, CJK) | Support UTF-8 correctly | LOW |
| EC-STR-007 | Control characters (null bytes) | Sanitize or reject | HIGH |
| EC-STR-008 | Path traversal (`../`, `..\\`) | Sanitize, log attempt | CRITICAL |
| EC-STR-009 | CRLF injection | Sanitize newline characters | HIGH |

---

### Password Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-PASS-001 | Too short (<8 chars) | Return complexity error | HIGH |
| EC-PASS-002 | Too long (>128 chars) | Accept or set reasonable limit | LOW |
| EC-PASS-003 | No uppercase letter | Return complexity error (if required) | MEDIUM |
| EC-PASS-004 | No lowercase letter | Return complexity error (if required) | MEDIUM |
| EC-PASS-005 | No digit | Return complexity error (if required) | MEDIUM |
| EC-PASS-006 | No special character | Return complexity error (if required) | MEDIUM |
| EC-PASS-007 | Common password (top 10000) | Return weak password error | HIGH |
| EC-PASS-008 | Equals username/email | Return similarity error | HIGH |
| EC-PASS-009 | Contains username substring | Return similarity error | MEDIUM |
| EC-PASS-010 | Unicode characters | Support UTF-8 passwords | LOW |

---

### File Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-FILE-001 | Exceeds size limit | Return size error before upload completes | HIGH |
| EC-FILE-002 | Type not allowed (by extension) | Return type validation error | HIGH |
| EC-FILE-003 | Type mismatch (extension vs magic bytes) | Reject, log attempt | CRITICAL |
| EC-FILE-004 | Malicious content (virus signature) | Scan and reject, log attempt | CRITICAL |
| EC-FILE-005 | Path traversal in filename (`../`) | Sanitize filename, log attempt | CRITICAL |
| EC-FILE-006 | Zero-byte file | Return validation error | MEDIUM |
| EC-FILE-007 | Double extension (`.jpg.exe`) | Reject or sanitize | CRITICAL |
| EC-FILE-008 | Very long filename (>255 chars) | Truncate or reject | MEDIUM |
| EC-FILE-009 | Special characters in filename | Sanitize to safe characters | MEDIUM |

---

### URL Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-URL-001 | Invalid format | Return validation error | HIGH |
| EC-URL-002 | Missing protocol | Prepend https:// or reject | MEDIUM |
| EC-URL-003 | JavaScript protocol (`javascript:`) | Reject, log attempt | CRITICAL |
| EC-URL-004 | Data URI (`data:`) | Reject or handle per policy | HIGH |
| EC-URL-005 | Private/internal IP | Reject (SSRF prevention) | CRITICAL |
| EC-URL-006 | Very long URL (>2048 chars) | Truncate or reject | MEDIUM |
| EC-URL-007 | Unicode/punycode domain | Normalize and validate | MEDIUM |

---

### Array Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-ARR-001 | Empty array (when required) | Return validation error | MEDIUM |
| EC-ARR-002 | Single item (when min > 1) | Return min count error | MEDIUM |
| EC-ARR-003 | Exceeds max size | Return limit error | MEDIUM |
| EC-ARR-004 | Duplicate items | Remove or return error per rule | LOW |
| EC-ARR-005 | Mixed types in array | Validate each item type | HIGH |
| EC-ARR-006 | Null item in array | Filter or reject | MEDIUM |

---

### Boolean Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-BOOL-001 | Null/undefined (when required) | Return validation error or default | MEDIUM |
| EC-BOOL-002 | String "true"/"false" | Coerce or reject | LOW |
| EC-BOOL-003 | Numeric 0/1 | Coerce or reject | LOW |
| EC-BOOL-004 | Empty string | Coerce to false or reject | LOW |

---

### ID/Reference Type

| ID Pattern | Condition | Expected Behavior | Severity |
|------------|-----------|-------------------|----------|
| EC-ID-001 | Invalid format (wrong length/chars) | Return validation error | HIGH |
| EC-ID-002 | Non-existent reference | Return 404 or validation error | HIGH |
| EC-ID-003 | Self-reference (circular) | Detect and reject | HIGH |
| EC-ID-004 | SQL injection in ID field | Sanitize, use parameterized queries | CRITICAL |
| EC-ID-005 | Negative ID (when positive required) | Return validation error | MEDIUM |

---

## Generation Algorithm

```text
GENERATE_HEURISTIC_EDGE_CASES(entities, min_severity = "MEDIUM"):

  edge_cases = []
  ec_counter = 1

  FOR entity IN entities:
    # Detect type
    type = DETECT_ENTITY_TYPE(entity.name, entity.context)

    # Load type-specific edge cases
    type_cases = EDGE_CASES_BY_TYPE[type]

    FOR case IN type_cases:
      # Filter by minimum severity
      IF SEVERITY_RANK[case.severity] >= SEVERITY_RANK[min_severity]:

        # Check if entity is marked critical (higher coverage)
        IF entity.is_critical:
          include = true
        ELSE:
          include = (case.severity IN ["CRITICAL", "HIGH"])

        IF include:
          edge_cases.append({
            id: FORMAT("EC-{:03d}", ec_counter),
            condition: SUBSTITUTE(case.condition, entity.name),
            expected_behavior: case.expected_behavior,
            severity: case.severity,
            category: "validation",
            entity_type: type,
            entity_name: entity.name,
            auto_generated: true,
            confidence: 0.90
          })
          ec_counter += 1

  RETURN edge_cases

SEVERITY_RANK = {
  "CRITICAL": 4,
  "HIGH": 3,
  "MEDIUM": 2,
  "LOW": 1
}
```

---

## Completeness Calculation

```text
CALCULATE_ENTITY_COVERAGE(entities, edge_cases):

  coverage = {
    total_entities: entities.length,
    covered_entities: 0,
    entity_details: []
  }

  FOR entity IN entities:
    entity_type = DETECT_ENTITY_TYPE(entity.name, entity.context)

    # Count EC for this entity
    entity_ec = FILTER(edge_cases, e => e.entity_name == entity.name)
    ec_count = entity_ec.length

    # Minimum expected EC by type
    min_expected = {
      "email": 3,
      "password": 4,
      "file": 4,
      "string": 3,
      "numeric": 3,
      "date": 3,
      "url": 3,
      "phone": 2,
      "array": 2,
      "boolean": 1,
      "id": 2
    }[entity_type] OR 2

    IF ec_count >= min_expected:
      coverage.covered_entities += 1
      status = "covered"
    ELSE:
      status = "partial"

    coverage.entity_details.append({
      name: entity.name,
      type: entity_type,
      ec_count: ec_count,
      min_expected: min_expected,
      status: status
    })

  coverage.score = coverage.covered_entities / coverage.total_entities

  RETURN coverage
```

---

## Integration with Self-Review

Entity coverage triggers SR-SPEC-12 validation:

```text
SR-SPEC-12: All detected entity types have heuristic edge cases?
  severity: MEDIUM
  auto_fixable: true

  check_fn(artifact):
    entities = EXTRACT_ENTITIES(artifact)
    edge_cases = EXTRACT_EDGE_CASES(artifact)
    coverage = CALCULATE_ENTITY_COVERAGE(entities, edge_cases)

    IF coverage.score >= 1.0:
      RETURN {status: PASS, details: "All {entities.length} entities covered"}
    ELSE:
      uncovered = FILTER(coverage.entity_details, d => d.status != "covered")
      RETURN {
        status: FAIL,
        details: "Missing EC for: {uncovered.map(e => e.name).join(', ')}"
      }

  fix_fn(artifact, issue):
    FOR entity IN issue.uncovered:
      new_ec = GENERATE_HEURISTIC_EDGE_CASES([entity])
      APPEND_TO_EDGE_CASES(artifact, new_ec)
    RETURN artifact
```

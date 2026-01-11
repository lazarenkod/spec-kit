# Review Phase

> **Version**: 1.0.0
> **Phase**: 2 (Post-Design)
> **Budget**: 30s (Moderate) or 120s (Full)
> **Applies to**: Depth levels 2-3

## Overview

The Review Phase validates generated artifacts through multi-pass checks. It catches issues proactively before handoff/implementation.

**Review Passes:**
1. **Constitution Alignment** (CRITICAL) — Tech stack, security, dependencies
2. **Completeness Check** (HIGH) — FR/NFR coverage, test strategy
3. **Edge Case Detection** (HIGH) — Failure scenarios, validation, concurrency
4. **Testability Audit** (MEDIUM) — Acceptance criteria, observability

**Execution:**
- Depth 2 (Moderate): Pass 1 only (constitution) — 30s
- Depth 3 (Full): All 4 passes — 120s (4 × 30s sequential)

---

## Execution Flow by Depth Level

### Depth Level 2: Moderate (30s)

```text
EMIT Task(role="review-constitution", subagent_type="general-purpose", model="sonnet", timeout=30s)
WAIT for result

IF result.failed:
    BLOCK: Constitution violation detected
    REPORT violations to user
    EXIT workflow

ELSE:
    LOG "✅ Constitution Alignment: PASS"
```

### Depth Level 3: Full (120s)

```text
FOR pass IN [constitution_alignment, completeness_check, edge_case_detection, testability_audit]:
    EMIT Task(role=f"review-{pass}", subagent_type="general-purpose", model="sonnet", timeout=30s)
    WAIT for result

    IF result.failed:
        IF pass.severity == "CRITICAL":
            BLOCK: Report violations, exit workflow
        ELSE:
            WARN: Log violations, continue to next pass

    ELSE:
        LOG f"✅ {pass}: PASS"
```

**Total time:**
- Moderate: 30s (1 pass)
- Full: 120s (4 × 30s sequential)

---

## Review Pass Specifications

### Pass 1: Constitution Alignment (CRITICAL)

**Severity:** CRITICAL (blocks on failure)
**Model:** sonnet
**Timeout:** 30s
**Applies to:** Depth 2-3

**Validation Criteria:**

1. **Tech Stack Compliance**
   - All languages/frameworks in `constitution.allowed_stack`
   - No prohibited technologies used
   - Versions match constitution specs (if specified)

2. **Security Anti-Patterns**
   - No hardcoded secrets (API keys, passwords, tokens)
   - No SQL injection vulnerabilities (raw SQL with user input)
   - No XSS vulnerabilities (unescaped user content in HTML)
   - No SSRF vulnerabilities (user-controlled URLs in fetch)
   - Auth/authz properly enforced

3. **Dependency Compliance**
   - All dependencies in `constitution.approved_dependencies` (if list exists)
   - No known vulnerable dependencies (check against security advisories if available)

**Prompt:**

```markdown
You are a security and compliance auditor. Review the generated artifacts for constitution violations.

**Constitution Path:** {constitution_path}
**Artifacts to Review:**
- {artifact_paths}

**Task:**

1. Read constitution.md and artifacts
2. Check for violations:
   - Tech stack: Are all technologies allowed?
   - Security: Any anti-patterns (hardcoded secrets, SQL injection, XSS, SSRF)?
   - Dependencies: Are all dependencies approved?

3. For each violation found:
   - **Severity:** CRITICAL/HIGH/MEDIUM/LOW
   - **Location:** File and line number (if applicable)
   - **Description:** What's wrong
   - **Remediation:** How to fix it

**Output Format:**

```json
{
  "pass": "constitution_alignment",
  "status": "PASS" | "FAIL",
  "violations": [
    {
      "severity": "CRITICAL",
      "category": "security_antipattern",
      "location": "src/api/auth.ts:42",
      "description": "Hardcoded API key: 'sk-abc123...'",
      "remediation": "Move to environment variable: process.env.API_KEY"
    }
  ],
  "summary": "Found 1 CRITICAL violation: hardcoded API key"
}
```

**Exit Criteria:**
- No CRITICAL violations
- All HIGH violations have remediation plans
```

**Block Condition:** Any CRITICAL violation found

---

### Pass 2: Completeness Check (HIGH)

**Severity:** HIGH (warns on failure, does not block)
**Model:** sonnet
**Timeout:** 30s
**Applies to:** Depth 3 only

**Validation Criteria:**

1. **FR Coverage ≥ 90%**
   - All FRs from spec.md addressed in plan.md/tasks.md
   - Each FR has implementation section
   - Traceability: FR-xxx → TASK-xxx

2. **NFR Coverage ≥ 90%**
   - All NFRs have measurable criteria
   - Each NFR has validation method
   - NFRs not silently ignored

3. **Test Strategy for All AS-xxx**
   - Each acceptance scenario has corresponding test task
   - Test type specified (unit, integration, E2E)
   - QG-TEST-001 satisfied (100% AS coverage)

**Prompt:**

```markdown
You are a requirements engineer. Verify that all requirements are addressed in the implementation artifacts.

**Spec Path:** {feature_dir}/spec.md
**Plan Path:** {feature_dir}/plan.md
**Tasks Path:** {feature_dir}/tasks.md

**Task:**

1. Extract FRs from spec.md (FR-001, FR-002, ...)
2. Verify each FR is addressed in plan.md or tasks.md
3. Calculate FR coverage: (addressed FRs / total FRs) * 100

4. Extract NFRs from spec.md
5. Verify each NFR has measurable criteria and validation method
6. Calculate NFR coverage

7. Extract acceptance scenarios (AS-xxx)
8. Verify each AS has corresponding test task in tasks.md
9. Calculate test coverage: (test tasks / total AS) * 100

**Output Format:**

```json
{
  "pass": "completeness_check",
  "status": "PASS" | "WARN",
  "metrics": {
    "fr_coverage": 94.5,  // percentage
    "nfr_coverage": 87.0,
    "test_coverage": 100.0
  },
  "missing_coverage": [
    {
      "type": "FR",
      "id": "FR-007",
      "description": "User profile editing",
      "addressed": false
    }
  ],
  "summary": "FR: 94.5%, NFR: 87.0%, Test: 100% (NFR coverage below 90%)"
}
```

**Exit Criteria:**
- FR coverage ≥ 90%
- NFR coverage ≥ 90%
- Test coverage = 100%
```

**Block Condition:** None (warns only)

---

### Pass 3: Edge Case Detection (HIGH)

**Severity:** HIGH (warns on failure, does not block)
**Model:** sonnet
**Timeout:** 30s
**Applies to:** Depth 3 only

**Validation Criteria:**

1. **Pre-Mortem ≥ 3 Scenarios**
   - Failure scenarios identified
   - Each scenario: description, impact, mitigation
   - Coverage: Technical + Integration edge cases

2. **Error Handling for API Calls**
   - All external API calls have error handling
   - Network errors handled (timeout, connection refused)
   - HTTP error codes handled (4xx, 5xx)

3. **Input Validation**
   - User inputs validated (type, range, format)
   - SQL injection protection (parameterized queries)
   - XSS protection (output escaping)

**Prompt:**

```markdown
You are a chaos engineer. Identify missing edge cases and error handling.

**Artifacts to Review:** {artifact_paths}

**Task:**

1. **Pre-Mortem Analysis:**
   - Read artifacts
   - Identify: Does Pre-Mortem section exist?
   - Count failure scenarios (need ≥3)
   - Verify: description, impact, mitigation for each

2. **Error Handling Audit:**
   - Find all external API calls (fetch, axios, http.get, etc.)
   - Check: Does each call have try/catch or .catch()?
   - Check: Are timeout errors handled?

3. **Input Validation Audit:**
   - Find all user inputs (req.body, req.query, form fields)
   - Check: Is each input validated?
   - Check: SQL injection protection (parameterized queries)?
   - Check: XSS protection (escaping/sanitization)?

**Output Format:**

```json
{
  "pass": "edge_case_detection",
  "status": "PASS" | "WARN",
  "findings": {
    "pre_mortem_scenarios": 5,  // count
    "unhandled_api_calls": [
      {
        "location": "src/api/payment.ts:78",
        "call": "fetch('/api/charge')",
        "missing": "No try/catch or timeout handling"
      }
    ],
    "unvalidated_inputs": [
      {
        "location": "src/api/user.ts:42",
        "input": "req.body.email",
        "missing": "No email format validation"
      }
    ]
  },
  "summary": "Pre-Mortem: 5 scenarios ✓, 2 unhandled API calls, 1 unvalidated input"
}
```

**Exit Criteria:**
- Pre-Mortem ≥ 3 scenarios
- All API calls have error handling
- All user inputs validated
```

**Block Condition:** None (warns only)

---

### Pass 4: Testability Audit (MEDIUM)

**Severity:** MEDIUM (warns on failure, does not block)
**Model:** sonnet
**Timeout:** 30s
**Applies to:** Depth 3 only

**Validation Criteria:**

1. **Acceptance Criteria Measurable**
   - Each FR has "how to verify" criteria
   - Criteria use quantifiable terms (not "fast", but "<100ms")
   - Criteria testable by automated tests

2. **NFR Measurement Methods**
   - Performance: Load testing strategy defined
   - Security: Penetration testing/SAST defined
   - Scalability: Stress testing defined

3. **Test Doubles Strategy**
   - External dependencies have mocking strategy
   - Database: Test fixtures or in-memory DB
   - APIs: Mock server or VCR (recorded responses)

4. **Observability**
   - SLIs defined (latency, error rate, throughput)
   - SLOs defined (e.g., P95 latency < 100ms)
   - Alerting defined (when SLO breached)

**Prompt:**

```markdown
You are a test engineer. Verify that the implementation is testable and observable.

**Artifacts to Review:** {artifact_paths}

**Task:**

1. **Acceptance Criteria Audit:**
   - Extract FRs
   - Check: Does each FR have measurable acceptance criteria?
   - Check: Are criteria quantifiable?

2. **NFR Measurement Audit:**
   - Extract NFRs
   - Check: Does each NFR have measurement method?

3. **Test Doubles Audit:**
   - Find external dependencies (DB, APIs, services)
   - Check: Is mocking/stubbing strategy defined?

4. **Observability Audit:**
   - Check: Are SLIs defined?
   - Check: Are SLOs defined?
   - Check: Is alerting defined?

**Output Format:**

```json
{
  "pass": "testability_audit",
  "status": "PASS" | "WARN",
  "findings": {
    "measurable_criteria": {
      "total_frs": 10,
      "measurable": 9,
      "percentage": 90.0
    },
    "nfr_measurement": {
      "total_nfrs": 5,
      "with_measurement": 4,
      "percentage": 80.0
    },
    "test_doubles": {
      "database": "✓ In-memory SQLite",
      "payment_api": "✗ No mocking strategy"
    },
    "observability": {
      "slis_defined": true,
      "slos_defined": false,
      "alerting_defined": false
    }
  },
  "summary": "AC: 90% measurable, NFR: 80% with measurement, SLOs/alerting missing"
}
```

**Exit Criteria:**
- Acceptance criteria ≥ 90% measurable
- NFR measurement ≥ 90% defined
- Test doubles strategy for all external deps
- SLIs, SLOs, alerting defined
```

**Block Condition:** None (warns only)

---

## Quality Gates

### PM-004: Review Pass Compliance

**Threshold:** 0 CRITICAL failures

**Validation:**
- constitution_alignment: PASS (or workflow blocked)
- completeness_check: PASS or WARN
- edge_case_detection: PASS or WARN
- testability_audit: PASS or WARN

**Block:** Any CRITICAL failure (constitution violations)

### PM-005: Edge Case Coverage

**Threshold:** ≥3 edge cases identified

**Validation:**
- Pre-Mortem section has ≥3 failure scenarios
- Each scenario: description, impact, mitigation
- Coverage: Technical + Integration edge cases

**Block:** 0 edge cases AND complexity tier = COMPLEX

---

## Error Handling

### Review Failure (CRITICAL)

```python
def handle_review_failure_critical(pass_name, violations):
    """
    Block workflow on CRITICAL review failure.
    """
    LOG f"❌ Review Pass '{pass_name}': FAILED (CRITICAL)"
    LOG f"Violations found: {len(violations)}"

    for v in violations:
        LOG f"  - {v.severity}: {v.description}"
        LOG f"    Location: {v.location}"
        LOG f"    Fix: {v.remediation}"

    raise QualityGateViolation(
        gate_id="PM-004",
        message=f"Review pass '{pass_name}' found CRITICAL violations",
        violations=violations
    )
```

### Review Failure (HIGH/MEDIUM)

```python
def handle_review_failure_warn(pass_name, findings):
    """
    Warn on HIGH/MEDIUM review failure, but continue.
    """
    LOG f"⚠️ Review Pass '{pass_name}': WARN"
    LOG f"Issues found (non-blocking):"

    for issue in findings:
        LOG f"  - {issue.description}"

    # Continue to next pass
```

---

## References

- Framework: `templates/shared/plan-mode/framework.md`
- Quality Gates: `memory/domains/quality-gates.md` (PM-004, PM-005)
- QG-TEST-001: `memory/domains/quality-gates.md` (Test coverage gate)

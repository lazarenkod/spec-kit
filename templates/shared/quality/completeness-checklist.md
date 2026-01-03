# Specification Completeness Checklist

> Semantic analysis for detecting missing requirements. Import this module in completeness-checker subagent.

## Purpose

Prevent incomplete specifications that miss critical aspects:
1. **40% of specs** miss error handling paths (2025 systematic review)
2. Non-functional requirements often omitted
3. Cross-cutting concerns (logging, monitoring) forgotten
4. Prerequisite features not identified

---

## Completeness Categories

| Category | Check | Severity | Weight |
|----------|-------|----------|--------|
| ERROR_HANDLING | Every happy path has error scenario | HIGH | 0.20 |
| NETWORK_ERRORS | Timeout, disconnect, retry logic | MEDIUM | 0.10 |
| PERFORMANCE | Latency/throughput requirements for APIs | HIGH | 0.15 |
| SECURITY | Auth/authz for protected features | CRITICAL | 0.20 |
| OBSERVABILITY | Logging, metrics, alerting | MEDIUM | 0.10 |
| ACCESSIBILITY | WCAG compliance for UI features | HIGH | 0.10 |
| PREREQUISITES | Dependencies identified before build | HIGH | 0.15 |

**Total Weight**: 1.00

---

## NFR Requirements Validation

### Mandatory NFR Categories

Every specification MUST include at least 3 NFRs with proper ID format:

| Category | ID Prefix | Required | Example |
|----------|-----------|:--------:|---------|
| Performance | NFR-PERF- | ✅ MUST | NFR-PERF-001: API response <200ms p95 |
| Security | NFR-SEC- | ✅ MUST | NFR-SEC-001: TLS 1.3 required |
| Reliability | NFR-REL- | ✅ MUST | NFR-REL-001: 99.9% availability |
| Scalability | NFR-SCAL- | Optional | NFR-SCAL-001: Horizontal scaling |
| Observability | NFR-OBS- | Optional | NFR-OBS-001: Structured logging |
| Accessibility | NFR-A11Y- | Optional | NFR-A11Y-001: WCAG 2.1 AA |
| Compliance | NFR-CMP- | Optional | NFR-CMP-001: GDPR data retention |
| Maintainability | NFR-MNT- | Optional | NFR-MNT-001: 80% code coverage |

### NFR Check Algorithm

```text
CHECK_NFR_REQUIREMENTS(spec):

  gaps = []

  # Check for NFR section existence
  IF NOT HAS_SECTION(spec, "Non-Functional Requirements"):
    gaps.append({
      category: "NFR_STRUCTURE",
      missing_aspect: "No NFR section found",
      explanation: "Specification MUST include Non-Functional Requirements section",
      severity: "CRITICAL",
      suggested_requirement: "Add NFR section with NFR-PERF-*, NFR-SEC-*, NFR-REL-* requirements"
    })
    RETURN gaps

  nfr_section = GET_SECTION(spec, "Non-Functional Requirements")
  nfr_ids = EXTRACT_IDS(nfr_section, pattern="NFR-[A-Z]+-\\d{3}")

  # Check mandatory categories
  MANDATORY_CATEGORIES = ["PERF", "SEC", "REL"]

  FOR category IN MANDATORY_CATEGORIES:
    pattern = "NFR-{category}-"
    IF NOT ANY(id.startswith(pattern) FOR id IN nfr_ids):
      gaps.append({
        category: "NFR_MANDATORY",
        missing_aspect: "Missing NFR-{category}-* requirement",
        explanation: "{category} is mandatory for all specifications",
        severity: "CRITICAL",
        suggested_requirement: "Add at least one NFR-{category}-xxx requirement"
      })

  # Check minimum NFR count
  IF len(nfr_ids) < 3:
    gaps.append({
      category: "NFR_COUNT",
      missing_aspect: "Insufficient NFR count",
      explanation: "Found {len(nfr_ids)} NFRs, minimum 3 required",
      severity: "HIGH",
      suggested_requirement: "Add NFRs to reach minimum of 3"
    })

  # Check NFR → AS traceability
  FOR nfr_id IN nfr_ids:
    as_pattern = "AS-{nfr_id.replace('NFR-', 'NFR-')}"
    IF NOT HAS_ACCEPTANCE_SCENARIO(spec, nfr_id):
      gaps.append({
        category: "NFR_TRACEABILITY",
        missing_aspect: "NFR without acceptance scenario",
        explanation: "{nfr_id} has no linked AS-NFR-* scenario",
        severity: "MEDIUM",
        suggested_requirement: "Add acceptance scenario for {nfr_id}"
      })

  # Check for quantified metrics (no vague terms)
  VAGUE_TERMS = ["fast", "quick", "good", "reasonable", "adequate", "secure", "reliable"]
  nfr_text = nfr_section.lower()

  FOR term IN VAGUE_TERMS:
    IF term IN nfr_text AND NOT FOLLOWED_BY_NUMBER(nfr_text, term):
      gaps.append({
        category: "NFR_QUANTIFICATION",
        missing_aspect: "Vague NFR term: '{term}'",
        explanation: "NFRs must have quantified metrics, not vague descriptions",
        severity: "HIGH",
        suggested_requirement: "Replace '{term}' with specific metric (e.g., '<200ms p95')"
      })

  RETURN gaps
```

### NFR Scoring Integration

| Check | Weight | Threshold |
|-------|--------|-----------|
| NFR section exists | 0.30 | MUST have section |
| 3 mandatory categories | 0.40 | PERF + SEC + REL required |
| NFR → AS traceability | 0.20 | Each NFR has AS-NFR-* |
| Quantified metrics | 0.10 | No vague terms |

---

## Error Handling Completeness

### Check Algorithm

```text
CHECK_ERROR_HANDLING(spec):

  gaps = []
  acceptance_scenarios = spec.acceptance_scenarios OR []

  # Count happy path vs error scenarios
  happy_paths = FILTER(acceptance_scenarios, s => "error" NOT IN s.then.lower())
  error_paths = FILTER(acceptance_scenarios, s => "error" IN s.then.lower())

  # Heuristic: Minimum 1 error scenario per 2 happy paths
  expected_error_count = CEIL(happy_paths.length / 2)

  IF error_paths.length < expected_error_count:
    gaps.append({
      category: "ERROR_HANDLING",
      missing_aspect: "Insufficient error scenarios",
      explanation: "Found {error_paths.length} error scenarios, expected ~{expected_error_count}",
      severity: "HIGH",
      suggested_requirement: "Add error handling scenarios for: network failures, validation errors, authorization failures"
    })

  # Check for specific error types
  error_text = JOIN([s.then FOR s IN error_paths], " ").lower()

  CRITICAL_ERROR_TYPES = {
    "network": ["timeout", "connection", "network", "unreachable"],
    "validation": ["invalid", "validation", "format", "required"],
    "auth": ["unauthorized", "forbidden", "expired", "denied"],
    "rate_limit": ["rate limit", "throttle", "quota", "429"],
    "database": ["constraint", "duplicate", "not found", "conflict"]
  }

  FOR error_type, keywords IN CRITICAL_ERROR_TYPES:
    IF NOT ANY(keyword IN error_text FOR keyword IN keywords):
      # Check if feature likely needs this error type
      IF FEATURE_REQUIRES_ERROR_TYPE(spec, error_type):
        gaps.append({
          category: "ERROR_HANDLING",
          missing_aspect: "{error_type} error handling",
          explanation: "No scenarios cover {error_type} errors",
          severity: "MEDIUM",
          suggested_requirement: "Add acceptance scenario for {error_type} error case"
        })

  RETURN gaps

FEATURE_REQUIRES_ERROR_TYPE(spec, error_type):
  requirements_text = JOIN(spec.functional_requirements, " ").lower()

  TRIGGERS = {
    "network": ["api", "fetch", "request", "external", "webhook"],
    "validation": ["input", "form", "field", "submit", "data"],
    "auth": ["login", "auth", "permission", "role", "token"],
    "rate_limit": ["api", "limit", "quota", "request"],
    "database": ["create", "update", "delete", "store", "save"]
  }

  RETURN ANY(trigger IN requirements_text FOR trigger IN TRIGGERS[error_type])
```

---

## Performance Requirements

### Check Algorithm

```text
CHECK_PERFORMANCE(spec):

  gaps = []
  requirements_text = JOIN(spec.functional_requirements, " ").lower()

  # Features that typically need performance requirements
  PERFORMANCE_TRIGGERS = {
    "api_latency": {
      keywords: ["api", "endpoint", "request", "response", "fetch"],
      check: "Define response time requirement (e.g., '<200ms p95')",
      severity: "HIGH"
    },
    "throughput": {
      keywords: ["batch", "bulk", "import", "export", "process"],
      check: "Define throughput requirement (e.g., '1000 records/sec')",
      severity: "HIGH"
    },
    "page_load": {
      keywords: ["page", "load", "display", "render", "show"],
      check: "Define page load time (e.g., '<3s LCP')",
      severity: "MEDIUM"
    },
    "search": {
      keywords: ["search", "filter", "query", "find"],
      check: "Define search response time (e.g., '<500ms for 10k records')",
      severity: "HIGH"
    }
  }

  # Check if spec has any NFRs section
  has_nfr_section = HAS_SECTION(spec, "Non-Functional Requirements") OR
                    HAS_SECTION(spec, "Performance Requirements")

  FOR trigger_type, config IN PERFORMANCE_TRIGGERS:
    IF ANY(keyword IN requirements_text FOR keyword IN config.keywords):
      # Feature needs performance requirements
      IF NOT has_nfr_section OR NOT HAS_PERFORMANCE_METRIC(spec, trigger_type):
        gaps.append({
          category: "PERFORMANCE",
          missing_aspect: "{trigger_type} performance requirement",
          explanation: "Feature involves {trigger_type} but lacks performance criteria",
          severity: config.severity,
          suggested_requirement: config.check
        })

  RETURN gaps
```

---

## Security Requirements

### Check Algorithm

```text
CHECK_SECURITY(spec):

  gaps = []
  requirements_text = JOIN(spec.functional_requirements, " ").lower()

  # Security dimensions to check (aligned with OWASP Top 10)
  SECURITY_DIMENSIONS = {
    "authentication": {
      triggers: ["login", "auth", "password", "token", "signin", "register"],
      requirements: ["credential storage", "session management", "brute force protection"],
      owasp: "A07:2021 Identification and Authentication Failures"
    },
    "authorization": {
      triggers: ["permission", "role", "access", "admin", "owner", "share"],
      requirements: ["access control checks", "privilege escalation prevention"],
      owasp: "A01:2021 Broken Access Control"
    },
    "input_validation": {
      triggers: ["input", "form", "field", "search", "query", "filter", "upload"],
      requirements: ["input sanitization", "injection prevention", "file type validation"],
      owasp: "A03:2021 Injection"
    },
    "data_protection": {
      triggers: ["encrypt", "sensitive", "personal", "pii", "password", "secret"],
      requirements: ["encryption at rest", "encryption in transit", "secure hashing"],
      owasp: "A02:2021 Cryptographic Failures"
    },
    "session_management": {
      triggers: ["session", "cookie", "remember", "logout", "token"],
      requirements: ["session timeout", "secure cookie flags", "CSRF protection"],
      owasp: "A07:2021"
    }
  }

  edge_cases = spec.edge_cases OR []
  security_ec = FILTER(edge_cases, ec => ec.category == "security")

  FOR dimension, config IN SECURITY_DIMENSIONS:
    IF ANY(trigger IN requirements_text FOR trigger IN config.triggers):
      # Feature involves this security dimension
      has_security_req = HAS_SECURITY_REQUIREMENT(spec, dimension)
      has_security_ec = ANY(dimension IN ec.condition.lower() FOR ec IN security_ec)

      IF NOT has_security_req:
        gaps.append({
          category: "SECURITY",
          missing_aspect: "{dimension} security requirement",
          explanation: "Feature involves {dimension} but lacks explicit security requirements. {config.owasp}",
          severity: "CRITICAL",
          suggested_requirement: "Add requirement for: {JOIN(config.requirements, ', ')}"
        })

  RETURN gaps
```

---

## Observability Requirements

### Check Algorithm

```text
CHECK_OBSERVABILITY(spec):

  gaps = []
  requirements_text = JOIN(spec.functional_requirements, " ").lower()

  OBSERVABILITY_DIMENSIONS = {
    "logging": {
      check: "Audit logging for security-relevant actions",
      triggers: ["create", "update", "delete", "login", "permission"],
      severity: "MEDIUM"
    },
    "metrics": {
      check: "Performance metrics for monitoring",
      triggers: ["api", "request", "process", "batch"],
      severity: "MEDIUM"
    },
    "alerting": {
      check: "Error rate alerting thresholds",
      triggers: ["error", "fail", "critical"],
      severity: "LOW"
    },
    "tracing": {
      check: "Distributed tracing for debugging",
      triggers: ["service", "microservice", "external", "api"],
      severity: "LOW"
    }
  }

  # Check if spec mentions any observability
  has_observability = ANY(
    keyword IN requirements_text FOR keyword IN
    ["log", "metric", "monitor", "alert", "trace", "audit"]
  )

  IF NOT has_observability:
    # Check if feature likely needs observability
    is_critical_feature = ANY(
      trigger IN requirements_text FOR trigger IN
      ["auth", "payment", "admin", "permission", "security"]
    )

    IF is_critical_feature:
      gaps.append({
        category: "OBSERVABILITY",
        missing_aspect: "No observability requirements",
        explanation: "Critical feature has no logging, metrics, or alerting defined",
        severity: "MEDIUM",
        suggested_requirement: "Add requirements for: audit logging, performance metrics, error alerting"
      })

  RETURN gaps
```

---

## Accessibility Requirements

### Check Algorithm

```text
CHECK_ACCESSIBILITY(spec):

  gaps = []

  # Only check if feature has UI
  IF NOT spec.has_ui:
    RETURN []

  requirements_text = JOIN(spec.functional_requirements, " ").lower()

  ACCESSIBILITY_CHECKS = {
    "keyboard_nav": {
      check: "All interactive elements keyboard accessible",
      triggers: ["button", "form", "input", "modal", "menu", "dropdown"],
      wcag: "2.1.1 Keyboard"
    },
    "screen_reader": {
      check: "Screen reader compatibility with ARIA labels",
      triggers: ["image", "icon", "chart", "graph", "table"],
      wcag: "1.1.1 Non-text Content"
    },
    "color_contrast": {
      check: "Color contrast ratio >= 4.5:1",
      triggers: ["text", "button", "link", "status", "badge"],
      wcag: "1.4.3 Contrast"
    },
    "focus_visible": {
      check: "Focus indicator visible for all interactive elements",
      triggers: ["input", "button", "link", "interactive"],
      wcag: "2.4.7 Focus Visible"
    }
  }

  has_accessibility_section = HAS_SECTION(spec, "Accessibility")

  IF NOT has_accessibility_section:
    gaps.append({
      category: "ACCESSIBILITY",
      missing_aspect: "No accessibility requirements",
      explanation: "UI feature has no WCAG compliance requirements defined",
      severity: "HIGH",
      suggested_requirement: "Add WCAG 2.1 AA compliance requirements"
    })

  RETURN gaps
```

---

## Prerequisites Check

### Check Algorithm

```text
CHECK_PREREQUISITES(spec, codebase_context):

  gaps = []
  requirements_text = JOIN(spec.functional_requirements, " ").lower()

  # Check for implicit dependencies
  DEPENDENCY_PATTERNS = {
    "authentication": {
      keywords: ["authenticated user", "logged in", "current user"],
      prerequisite: "Authentication system must exist",
      check_fn: codebase_context => EXISTS_AUTH_SYSTEM(codebase_context)
    },
    "database": {
      keywords: ["store", "save", "retrieve", "fetch from db"],
      prerequisite: "Database schema must be defined",
      check_fn: codebase_context => EXISTS_DB_MODELS(codebase_context)
    },
    "api_client": {
      keywords: ["external api", "third-party", "integration"],
      prerequisite: "API client configuration must exist",
      check_fn: codebase_context => EXISTS_API_CONFIG(codebase_context)
    },
    "permissions": {
      keywords: ["admin only", "permission required", "role-based"],
      prerequisite: "Permission system must exist",
      check_fn: codebase_context => EXISTS_PERMISSION_SYSTEM(codebase_context)
    }
  }

  FOR dep_type, config IN DEPENDENCY_PATTERNS:
    IF ANY(keyword IN requirements_text FOR keyword IN config.keywords):
      IF codebase_context AND NOT config.check_fn(codebase_context):
        gaps.append({
          category: "PREREQUISITES",
          missing_aspect: "{dep_type} prerequisite",
          explanation: "Feature assumes {dep_type} exists but not found in codebase",
          severity: "HIGH",
          suggested_requirement: config.prerequisite
        })

  # Check technical dependencies section
  IF NOT HAS_SECTION(spec, "Technical Dependencies") AND
     ANY(keyword IN requirements_text FOR keyword IN ["api", "library", "package", "sdk"]):
    gaps.append({
      category: "PREREQUISITES",
      missing_aspect: "Technical dependencies not documented",
      explanation: "Feature mentions external dependencies but none documented",
      severity: "MEDIUM",
      suggested_requirement: "Add Technical Dependencies section with versions"
    })

  RETURN gaps
```

---

## Completeness Score Calculation

```text
CALCULATE_COMPLETENESS_SCORE(spec, codebase_context = null):

  CATEGORY_WEIGHTS = {
    ERROR_HANDLING: 0.20,
    PERFORMANCE: 0.15,
    SECURITY: 0.20,
    OBSERVABILITY: 0.10,
    ACCESSIBILITY: 0.10,
    PREREQUISITES: 0.15,
    EDGE_CASES: 0.10
  }

  # Run all checks
  all_gaps = []
  all_gaps.extend(CHECK_ERROR_HANDLING(spec))
  all_gaps.extend(CHECK_PERFORMANCE(spec))
  all_gaps.extend(CHECK_SECURITY(spec))
  all_gaps.extend(CHECK_OBSERVABILITY(spec))
  all_gaps.extend(CHECK_ACCESSIBILITY(spec))
  all_gaps.extend(CHECK_PREREQUISITES(spec, codebase_context))

  # Calculate score per category
  category_scores = {}

  FOR category, weight IN CATEGORY_WEIGHTS:
    category_gaps = FILTER(all_gaps, g => g.category == category)

    IF category_gaps.length == 0:
      category_scores[category] = 1.0  # Fully complete
    ELSE:
      # Deduct based on severity
      deductions = SUM(
        0.5 IF gap.severity == "CRITICAL" ELSE
        0.3 IF gap.severity == "HIGH" ELSE
        0.15 IF gap.severity == "MEDIUM" ELSE
        0.05
        FOR gap IN category_gaps
      )
      category_scores[category] = MAX(0.0, 1.0 - deductions)

  # Calculate weighted total
  total_score = SUM(
    category_scores[cat] * weight
    FOR cat, weight IN CATEGORY_WEIGHTS
  )

  RETURN {
    score: ROUND(total_score, 2),
    category_scores: category_scores,
    gaps: all_gaps,
    status: "PASS" IF total_score >= 0.75 ELSE "FAIL"
  }
```

---

## LLM Gap Analysis

```text
LLM_GAP_ANALYSIS(spec, codebase_context):

  prompt = """You are a senior product manager reviewing a feature specification for completeness.

CURRENT SPEC:
User Stories: {len(spec.user_stories)}
Functional Requirements: {len(spec.functional_requirements)}
Acceptance Scenarios: {len(spec.acceptance_scenarios)}
Edge Cases: {len(spec.edge_cases)}

FUNCTIONAL REQUIREMENTS:
{FORMAT_REQUIREMENTS(spec.functional_requirements)}

ACCEPTANCE SCENARIOS:
{FORMAT_SCENARIOS(spec.acceptance_scenarios)}

EXISTING CODEBASE CONTEXT:
{FORMAT_CODEBASE_CONTEXT(codebase_context) OR "No codebase context provided"}

TASK:
Identify MISSING aspects that would make this spec incomplete.

Consider these dimensions:
1. **Error handling**: What could go wrong? Network failures? Invalid input? Race conditions?
2. **Performance**: Any latency/throughput requirements needed?
3. **Security**: Authentication? Authorization? Data protection? Input validation?
4. **Accessibility**: If UI feature, WCAG compliance?
5. **Observability**: Logging? Metrics? Alerting? Debugging support?
6. **Prerequisites**: What must exist before this can be built? Database schema? Auth system?
7. **Edge cases**: Boundary conditions? Empty states? Concurrent access?

OUTPUT FORMAT (strict JSON):
{
  "gaps": [
    {
      "category": "error_handling|performance|security|accessibility|observability|prerequisites",
      "missing_aspect": "concise description of what's missing",
      "explanation": "why this matters for implementation",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "suggested_requirement": "specific requirement text to add"
    }
  ]
}

Only report GENUINE gaps (things truly missing, not nice-to-haves).
Prioritize gaps that would cause implementation failures or security issues."""

  response = LLM_CALL(prompt, temperature=0.3)
  RETURN PARSE_JSON(response).gaps
```

---

## Integration with /speckit.specify

```text
# Completeness check runs after edge case detection

STEP 1: Run Completeness Checks
  gaps = []
  gaps.extend(CHECK_ERROR_HANDLING(spec))
  gaps.extend(CHECK_PERFORMANCE(spec))
  gaps.extend(CHECK_SECURITY(spec))
  gaps.extend(CHECK_OBSERVABILITY(spec))
  gaps.extend(CHECK_ACCESSIBILITY(spec))
  gaps.extend(CHECK_PREREQUISITES(spec, codebase_context))

STEP 2: LLM Gap Analysis
  llm_gaps = LLM_GAP_ANALYSIS(spec, codebase_context)
  all_gaps = MERGE_AND_DEDUPLICATE(gaps, llm_gaps)

STEP 3: Calculate Score
  result = CALCULATE_COMPLETENESS_SCORE(spec, codebase_context)

STEP 4: Generate Completeness Analysis Section
  OUTPUT:
    ### Completeness Analysis

    | Category | Status | Details |
    |----------|--------|---------|
    {FOR cat IN CATEGORIES:}
    | {cat} | {STATUS_ICON(result.category_scores[cat])} | {DETAILS(cat, all_gaps)} |

    **Completeness Score**: {result.score} / 1.00

STEP 5: Quality Gate
  IF result.score < 0.75:
    FLAG as SR-SPEC-18 violation
    SUGGEST gap remediation
```

---

## Status Icons

```text
STATUS_ICON(score):
  IF score >= 0.9: RETURN "✅ Covered"
  IF score >= 0.6: RETURN "⚠️ Partial"
  RETURN "❌ Missing"
```

---

## Quality Gate Integration

Completeness checking triggers these self-review criteria:

| Criteria ID | Check | Threshold |
|-------------|-------|-----------|
| SR-SPEC-16 | Error path coverage | ratio >= 0.5 |
| SR-SPEC-17 | Security triggers covered | 100% for auth/input |
| SR-SPEC-18 | Overall completeness score | >= 0.75 |

---

## Quick Reference: Common Gaps

| Feature Type | Commonly Missing |
|--------------|------------------|
| API endpoint | Rate limiting, timeout handling, error responses |
| User auth | Brute force protection, session expiry, password policy |
| Data input | Validation errors, sanitization, size limits |
| File upload | Type validation, size limits, malware scanning |
| Admin panel | Audit logging, permission checks, privilege escalation |
| Search | Performance thresholds, empty results, query limits |
| Payment | Idempotency, retry logic, reconciliation |

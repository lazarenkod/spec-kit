# Requirement Ambiguity Detection Patterns

> Detect and repair ambiguous requirements to reduce code generation errors. Import this module in ambiguity-detector subagent.

## Purpose

Prevent implementation failures caused by ambiguous requirements:
1. **30% code generation errors** from vague terms (SpecFix research, Stanford 2025)
2. Misaligned implementations requiring costly rework
3. Specification ping-pong between stakeholders

---

## Ambiguity Types

| Type | Pattern Examples | Severity | Auto-Fixable |
|------|-----------------|----------|--------------|
| VAGUE_TERM | "fast", "user-friendly", "secure", "simple" | HIGH | ❌ |
| MISSING_QUANTITY | "retain data" (how long?), "multiple" (how many?) | HIGH | ❌ |
| UNCLEAR_ACTOR | "system", "it", "the user" (which user?) | MEDIUM | ❌ |
| UNDEFINED_TERM | Domain jargon without definition | MEDIUM | ✅ |
| CONDITIONAL_GAP | "if X" with no "else" branch | HIGH | ✅ |
| INCOMPLETE_LIST | "etc.", "...", "and more", "such as" | MEDIUM | ❌ |

---

## Pattern Library

### Vague Term Patterns

```text
VAGUE_TERM_PATTERNS = {
  "performance": {
    pattern: "fast|quickly|responsive|slow|real-time|instant|immediate"
    severity: HIGH
    suggestion: "Define performance threshold (e.g., '<200ms p95 latency')"
    examples: [
      BAD:  "System must be fast"
      GOOD: "System must respond within 200ms at p95"
    ]
  },

  "quality_ux": {
    pattern: "user-friendly|intuitive|simple|easy|clean|modern|elegant"
    severity: HIGH
    suggestion: "Define measurable UX criteria (e.g., '90% task completion rate')"
    examples: [
      BAD:  "Interface should be intuitive"
      GOOD: "First-time users complete login in <30s with zero help"
    ]
  },

  "security": {
    pattern: "secure|safe|protected|reliable|robust|stable"
    severity: CRITICAL
    suggestion: "Define security requirements (e.g., 'OWASP Top 10 mitigation')"
    examples: [
      BAD:  "Data must be secure"
      GOOD: "Data encrypted at rest with AES-256, in transit with TLS 1.3"
    ]
  },

  "quantity_vague": {
    pattern: "some|many|few|several|most|numerous|various|multiple"
    severity: HIGH
    suggestion: "Specify exact quantity or range (e.g., '3-5 items')"
    examples: [
      BAD:  "Support multiple file formats"
      GOOD: "Support PNG, JPEG, and WebP formats"
    ]
  },

  "frequency": {
    pattern: "often|rarely|occasionally|sometimes|frequently|usually"
    severity: MEDIUM
    suggestion: "Specify frequency (e.g., 'at least once per hour')"
    examples: [
      BAD:  "Sync data frequently"
      GOOD: "Sync data every 5 minutes when app is active"
    ]
  },

  "size_vague": {
    pattern: "large|small|big|tiny|huge|minimal|significant"
    severity: MEDIUM
    suggestion: "Specify exact size/threshold (e.g., '>10MB', '<100 items')"
    examples: [
      BAD:  "Handle large files"
      GOOD: "Support file uploads up to 100MB"
    ]
  },

  "time_vague": {
    pattern: "soon|later|eventually|immediately|quickly|recently"
    severity: HIGH
    suggestion: "Specify exact time (e.g., 'within 5 seconds', 'after 30 days')"
    examples: [
      BAD:  "Delete data eventually"
      GOOD: "Delete data after 90 days of account inactivity"
    ]
  }
}
```

---

### Missing Quantity Patterns

```text
MISSING_QUANTITY_PATTERNS = {
  "retention": {
    trigger: "retain|store|keep|save|archive"
    question: "For how long? (e.g., 30 days, 1 year, forever)"
    severity: HIGH
  },

  "rate_limit": {
    trigger: "rate limit|throttle|limit requests|quota"
    question: "What limit? (e.g., 100 requests/minute, 1000/day)"
    severity: HIGH
  },

  "pagination": {
    trigger: "list|show|display|return results"
    question: "How many items per page? (e.g., 20, 50, 100)"
    severity: MEDIUM
  },

  "timeout": {
    trigger: "timeout|expire|wait for"
    question: "What duration? (e.g., 30 seconds, 5 minutes)"
    severity: HIGH
  },

  "retry": {
    trigger: "retry|attempt again|repeat"
    question: "How many retries? What backoff strategy?"
    severity: MEDIUM
  },

  "max_length": {
    trigger: "text|input|field|name|description"
    question: "Maximum character length? (e.g., 255, 1000, unlimited)"
    severity: MEDIUM
  }
}
```

---

### Unclear Actor Patterns

```text
UNCLEAR_ACTOR_PATTERNS = {
  "generic_system": {
    pattern: "the system|it|this|application"
    severity: MEDIUM
    suggestion: "Specify component (e.g., 'API server', 'frontend', 'database')"
  },

  "generic_user": {
    pattern: "user|the user|users"
    severity: MEDIUM
    suggestion: "Specify user type (e.g., 'admin', 'member', 'guest')"
  },

  "passive_voice": {
    pattern: "is displayed|will be sent|should be validated|must be stored"
    severity: MEDIUM
    suggestion: "Use active voice: 'X does Y' (e.g., 'Server validates input')"
  }
}
```

---

### Conditional Gap Patterns

```text
CONDITIONAL_GAP_DETECTION = {
  trigger: "if|when|in case|provided that|unless"

  check_fn(requirement):
    # Find all conditional statements
    conditionals = FIND_PATTERNS(requirement, CONDITIONAL_TRIGGERS)

    FOR conditional IN conditionals:
      # Check for corresponding else/otherwise/error case
      IF NOT HAS_ALTERNATE_BRANCH(conditional):
        RETURN {
          ambiguity_type: CONDITIONAL_GAP,
          ambiguous_text: conditional.text,
          explanation: "Missing behavior for 'else' case",
          severity: HIGH,
          suggestion: "Define what happens when condition is NOT met"
        }

    RETURN null

  examples: [
    BAD:  "If user is authenticated, show dashboard"
    GOOD: "If user is authenticated, show dashboard; otherwise redirect to login"
  ]
}
```

---

### Incomplete List Patterns

```text
INCOMPLETE_LIST_PATTERNS = {
  pattern: "etc\\.|\\.\\.\\.|and more|such as|including|like|for example"
  severity: MEDIUM
  suggestion: "Enumerate all items explicitly or define a clear scope"

  examples: [
    BAD:  "Support authentication methods like OAuth, SSO, etc."
    GOOD: "Support OAuth2 and SAML SSO. Additional methods require change request."
  ]
}
```

---

## Detection Algorithm

```text
DETECT_AMBIGUITIES(functional_requirements, glossary = {}):

  reports = []

  FOR i, requirement IN functional_requirements:
    req_id = "FR-{i+1:03d}"

    # Pass 1: Vague term detection
    FOR category, config IN VAGUE_TERM_PATTERNS:
      matches = REGEX_MATCH(requirement, config.pattern, IGNORE_CASE)
      FOR match IN matches:
        reports.append({
          requirement_id: req_id,
          ambiguity_type: "VAGUE_TERM",
          ambiguous_text: match,
          explanation: "Term '{match}' is subjective and unmeasurable",
          category: category,
          severity: config.severity,
          suggested_clarification: config.suggestion
        })

    # Pass 2: Missing quantity detection
    FOR category, config IN MISSING_QUANTITY_PATTERNS:
      IF CONTAINS(requirement.lower(), config.trigger):
        IF NOT HAS_EXPLICIT_QUANTITY(requirement):
          reports.append({
            requirement_id: req_id,
            ambiguity_type: "MISSING_QUANTITY",
            ambiguous_text: EXTRACT_PHRASE(requirement, config.trigger),
            explanation: "Missing specific quantity/threshold",
            category: category,
            severity: config.severity,
            suggested_clarification: config.question
          })

    # Pass 3: Unclear actor detection
    FOR category, config IN UNCLEAR_ACTOR_PATTERNS:
      matches = REGEX_MATCH(requirement, config.pattern, IGNORE_CASE)
      FOR match IN matches:
        reports.append({
          requirement_id: req_id,
          ambiguity_type: "UNCLEAR_ACTOR",
          ambiguous_text: match,
          explanation: "Actor '{match}' is ambiguous",
          severity: config.severity,
          suggested_clarification: config.suggestion
        })

    # Pass 4: Conditional gap detection
    gap = CONDITIONAL_GAP_DETECTION.check_fn(requirement)
    IF gap:
      reports.append({requirement_id: req_id, ...gap})

    # Pass 5: Incomplete list detection
    IF REGEX_MATCH(requirement, INCOMPLETE_LIST_PATTERNS.pattern):
      reports.append({
        requirement_id: req_id,
        ambiguity_type: "INCOMPLETE_LIST",
        ambiguous_text: EXTRACT_LIST_CONTEXT(requirement),
        explanation: "Open-ended list creates ambiguity",
        severity: INCOMPLETE_LIST_PATTERNS.severity,
        suggested_clarification: INCOMPLETE_LIST_PATTERNS.suggestion
      })

    # Pass 6: Undefined term detection
    domain_terms = EXTRACT_DOMAIN_TERMS(requirement)
    FOR term IN domain_terms:
      IF term NOT IN glossary AND NOT IS_COMMON_TERM(term):
        reports.append({
          requirement_id: req_id,
          ambiguity_type: "UNDEFINED_TERM",
          ambiguous_text: term,
          explanation: "Domain term '{term}' not defined in glossary",
          severity: "MEDIUM",
          suggested_clarification: "Add definition for '{term}' to glossary"
        })

  RETURN DEDUPLICATE_BY_TEXT(reports)
```

---

## LLM Metacognitive Analysis

```text
LLM_AMBIGUITY_ANALYSIS(functional_requirements, context):

  prompt = """You are a requirements analyst detecting ambiguities.

FUNCTIONAL REQUIREMENTS:
{FORMAT_REQUIREMENTS(functional_requirements)}

GLOSSARY:
{context.glossary OR "No glossary provided"}

TASK:
For each requirement, analyze whether it has MULTIPLE VALID INTERPRETATIONS.

Use this metacognitive approach:
1. Ask yourself: "What CANNOT I understand clearly from this requirement?"
2. Generate at least 2 different interpretations for anything unclear
3. Flag requirements where interpretations lead to DIFFERENT implementations

For each ambiguous requirement, provide:
1. Requirement ID (FR-XXX)
2. Ambiguous phrase/word
3. Multiple possible interpretations (at least 2)
4. Why this matters (implementation impact)
5. Suggested clarification question

OUTPUT FORMAT (strict JSON):
{
  "ambiguities": [
    {
      "requirement_id": "FR-001",
      "ambiguous_text": "retain user data",
      "interpretations": [
        "Retain forever (no automatic deletion)",
        "Retain for 30 days after last login",
        "Retain until user explicitly deletes account"
      ],
      "implementation_impact": "Affects database schema, retention policies, GDPR compliance",
      "clarification_question": "How long should user data be retained?",
      "severity": "CRITICAL"
    }
  ]
}

Only report requirements with GENUINE ambiguity (>1 valid interpretation).
Do NOT flag requirements that are merely underspecified but unambiguous."""

  response = LLM_CALL(prompt, temperature=0.2)
  RETURN PARSE_JSON(response).ambiguities
```

---

## Repair Algorithm

```text
REPAIR_AMBIGUITY(ambiguity, user_clarification):

  prompt = """Repair this ambiguous requirement:

ORIGINAL REQUIREMENT: {ambiguity.original_requirement}
AMBIGUOUS TEXT: {ambiguity.ambiguous_text}
AMBIGUITY TYPE: {ambiguity.ambiguity_type}
USER CLARIFICATION: {user_clarification}

TASK: Rewrite the requirement to eliminate ambiguity.

Rules:
- Use specific, measurable terms
- Include quantities, thresholds, time periods where relevant
- Define technical terms inline or reference glossary
- Be technology-agnostic but precise
- Preserve original intent while removing ambiguity

OUTPUT: Repaired requirement (plain text, no explanation)"""

  response = LLM_CALL(prompt, temperature=0.1)  # Low temperature for consistency
  RETURN response.strip()
```

---

## Severity Classification

| Severity | Description | Action |
|----------|-------------|--------|
| CRITICAL | Could cause security vulnerabilities or data loss | BLOCK until clarified |
| HIGH | Will cause implementation divergence | WARN, require clarification |
| MEDIUM | May cause minor inconsistencies | SUGGEST clarification |
| LOW | Style/preference issues | NOTE for improvement |

---

## Integration with /speckit.clarify

```text
# Enhanced clarification workflow

STEP 1: Automatic Ambiguity Detection
  ambiguities = DETECT_AMBIGUITIES(spec.functional_requirements, spec.glossary)
  llm_ambiguities = LLM_AMBIGUITY_ANALYSIS(spec.functional_requirements, context)
  all_ambiguities = MERGE_AND_DEDUPLICATE(ambiguities, llm_ambiguities)
  top_ambiguities = SORT_BY_SEVERITY(all_ambiguities)[:5]

STEP 2: Present to User
  > I've analyzed the spec and detected {count} ambiguities:
  >
  > 1. [CRITICAL] FR-001: "retain user data" - How long?
  >    Interpretations: forever / 30 days / until deletion
  >
  > 2. [HIGH] FR-003: "fast login" - Define threshold
  >    Interpretations: <200ms / <500ms / <1s
  >
  > Please clarify each ambiguity.

STEP 3: Collect User Input
  FOR ambiguity IN top_ambiguities:
    clarification = PROMPT_USER(ambiguity.clarification_question)
    repaired = REPAIR_AMBIGUITY(ambiguity, clarification)
    UPDATE_SPEC(spec, ambiguity.requirement_id, repaired)

STEP 4: Verify Repairs
  remaining = DETECT_AMBIGUITIES(spec.functional_requirements, spec.glossary)
  IF remaining.length > 0:
    RECURSE with remaining ambiguities
```

---

## Quality Gate Integration

Ambiguity detection triggers these self-review criteria:

| Criteria ID | Check | Threshold |
|-------------|-------|-----------|
| SR-SPEC-14 | No vague terms without metrics | 0 HIGH severity |
| SR-SPEC-15 | All quantities defined | 0 MISSING_QUANTITY |

---

## Quick Reference: Common Ambiguities

| Ambiguous | Clarified |
|-----------|-----------|
| "fast" | "response time <200ms at p95" |
| "secure" | "encrypted with AES-256 at rest" |
| "retain data" | "retain for 90 days after account deletion" |
| "user" | "authenticated member user" |
| "if valid" | "if valid; otherwise return 400 Bad Request" |
| "etc." | "PNG, JPEG, and WebP formats only" |
| "multiple" | "between 3 and 10" |
| "recently" | "within the last 7 days" |

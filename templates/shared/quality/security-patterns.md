# Security Pattern Detection (OWASP-Based)

> Detect security-relevant features and generate appropriate edge cases. Import this module in edge-case-detector subagent.

## Purpose

Prevent specifications from missing security edge cases by:
1. Detecting security-relevant triggers in requirements
2. Applying OWASP Top 10 patterns
3. Generating security-specific edge cases with CRITICAL severity
4. Ensuring audit-ready security coverage

---

## Security Trigger Detection

```text
DETECT_SECURITY_TRIGGERS(requirements_text):

  triggers_found = []
  text_lower = requirements_text.lower()

  FOR category, config IN SECURITY_CATEGORIES:
    FOR keyword IN config.keywords:
      IF keyword IN text_lower:
        triggers_found.append({
          category: category,
          keyword_matched: keyword,
          edge_cases: config.edge_cases,
          owasp_ref: config.owasp
        })
        BREAK  # One match per category is enough

  RETURN DEDUPLICATE_BY_CATEGORY(triggers_found)
```

---

## Security Trigger Categories

### Authentication (OWASP A07:2021 - Identification and Authentication Failures)

**Trigger Keywords**:
```text
auth, login, logout, signin, signout, sign-in, sign-out,
password, credential, token, session, jwt, oauth, sso,
register, signup, sign-up, forgot, reset, 2fa, mfa, otp
```

**Edge Cases**:

| ID | Condition | Expected Behavior | Severity |
|----|-----------|-------------------|----------|
| EC-SEC-AUTH-001 | Invalid credentials | Return generic "invalid credentials" (no user enumeration) | CRITICAL |
| EC-SEC-AUTH-002 | Expired token/session | Return 401, redirect to login | CRITICAL |
| EC-SEC-AUTH-003 | Brute force attempt (5+ failures in 5min) | Implement rate limiting, temporary account lockout | CRITICAL |
| EC-SEC-AUTH-004 | Concurrent sessions from different locations | Enforce policy: allow/deny/notify user | HIGH |
| EC-SEC-AUTH-005 | Session fixation attempt | Regenerate session ID on successful login | CRITICAL |
| EC-SEC-AUTH-006 | Missing auth header on protected route | Return 401 with WWW-Authenticate header | HIGH |
| EC-SEC-AUTH-007 | Malformed JWT (invalid signature) | Return 401, do not expose cryptographic details | HIGH |
| EC-SEC-AUTH-008 | Token with tampered claims | Reject, log as security event | CRITICAL |
| EC-SEC-AUTH-009 | Password reset with expired/used token | Return clear error, require new reset request | HIGH |

---

### Input Validation (OWASP A03:2021 - Injection)

**Trigger Keywords**:
```text
input, form, field, search, query, filter, parameter,
submit, data, user input, text, content, message, comment
```

**Edge Cases**:

| ID | Condition | Expected Behavior | Severity |
|----|-----------|-------------------|----------|
| EC-SEC-INJ-001 | SQL injection attempt (`'; DROP TABLE--`) | Use parameterized queries, reject/sanitize | CRITICAL |
| EC-SEC-INJ-002 | XSS payload (`<script>alert(1)</script>`) | Sanitize output, implement CSP | CRITICAL |
| EC-SEC-INJ-003 | Command injection (`; rm -rf /`) | Reject shell metacharacters, never use shell exec | CRITICAL |
| EC-SEC-INJ-004 | LDAP injection (`*)(uid=*))(|(uid=*`) | Escape special LDAP characters | CRITICAL |
| EC-SEC-INJ-005 | XML injection (XXE) (`<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>`) | Disable external entities in XML parser | CRITICAL |
| EC-SEC-INJ-006 | Template injection (`{{constructor.constructor('return this')()}}`) | Escape template syntax, use sandboxed templates | CRITICAL |
| EC-SEC-INJ-007 | NoSQL injection (`{"$gt": ""}`) | Validate input types, use ODM/ORM | CRITICAL |
| EC-SEC-INJ-008 | Header injection (CRLF) (`%0d%0a`) | Sanitize newline characters in headers | HIGH |

---

### Access Control (OWASP A01:2021 - Broken Access Control)

**Trigger Keywords**:
```text
permission, role, admin, access, authorize, authorization,
grant, deny, restrict, owner, shared, private, public,
tenant, organization, team, member, user role
```

**Edge Cases**:

| ID | Condition | Expected Behavior | Severity |
|----|-----------|-------------------|----------|
| EC-SEC-AC-001 | Privilege escalation attempt (user → admin) | Deny, log as security event | CRITICAL |
| EC-SEC-AC-002 | IDOR - accessing other user's resource by ID | Return 404 (not 403) to prevent enumeration | CRITICAL |
| EC-SEC-AC-003 | Missing authorization check on endpoint | Enforce auth on all protected routes (deny by default) | CRITICAL |
| EC-SEC-AC-004 | Role bypass via parameter tampering | Server-side role validation, ignore client role claims | CRITICAL |
| EC-SEC-AC-005 | Deleted/suspended user accessing resources | Deny immediately, invalidate all sessions | HIGH |
| EC-SEC-AC-006 | Cross-tenant data access | Enforce tenant isolation at database level | CRITICAL |
| EC-SEC-AC-007 | Path traversal to access restricted files | Validate paths, use allowlists | CRITICAL |

---

### Session Management (OWASP A07:2021)

**Trigger Keywords**:
```text
session, cookie, remember, logout, idle, timeout,
refresh, persist, stay logged in, keep me signed in
```

**Edge Cases**:

| ID | Condition | Expected Behavior | Severity |
|----|-----------|-------------------|----------|
| EC-SEC-SESS-001 | Session hijacking attempt (stolen session ID) | Bind session to user agent, consider IP binding | CRITICAL |
| EC-SEC-SESS-002 | Session timeout after idle period | Expire after configured idle time (default: 30min) | HIGH |
| EC-SEC-SESS-003 | Logout does not invalidate server-side session | Server-side session destruction required | CRITICAL |
| EC-SEC-SESS-004 | Cookie without security flags | Set Secure, HttpOnly, SameSite=Strict | HIGH |
| EC-SEC-SESS-005 | CSRF attack on state-changing operation | Implement CSRF tokens, verify Origin header | CRITICAL |
| EC-SEC-SESS-006 | Predictable session ID | Use cryptographically secure random generation | CRITICAL |

---

### File Upload (OWASP A04:2021 - Insecure Design)

**Trigger Keywords**:
```text
upload, file, attachment, image, document, photo,
avatar, media, import, csv, excel, pdf, export
```

**Edge Cases**:

| ID | Condition | Expected Behavior | Severity |
|----|-----------|-------------------|----------|
| EC-SEC-FILE-001 | Malicious file content (virus, malware) | Virus scan before storage, quarantine suspicious | CRITICAL |
| EC-SEC-FILE-002 | File type bypass (MIME vs magic bytes mismatch) | Validate content type by magic bytes, not extension | CRITICAL |
| EC-SEC-FILE-003 | Path traversal in filename (`../../../etc/passwd`) | Sanitize filename to alphanumeric + limited chars | CRITICAL |
| EC-SEC-FILE-004 | Oversized file causing DoS | Enforce limits early, stream processing | HIGH |
| EC-SEC-FILE-005 | Polyglot file (image containing script) | Set Content-Disposition: attachment, serve from separate domain | HIGH |
| EC-SEC-FILE-006 | ZIP bomb (decompression attack) | Limit decompression ratio and depth | HIGH |
| EC-SEC-FILE-007 | SVG with embedded JavaScript | Sanitize SVG, remove script elements | CRITICAL |

---

### API Security (OWASP A06:2021 - Vulnerable Components + API Security Top 10)

**Trigger Keywords**:
```text
api, endpoint, rest, graphql, webhook, integration,
rate, limit, throttle, quota, key, secret, bearer
```

**Edge Cases**:

| ID | Condition | Expected Behavior | Severity |
|----|-----------|-------------------|----------|
| EC-SEC-API-001 | Rate limit exceeded | Return 429 with Retry-After header | HIGH |
| EC-SEC-API-002 | API key theft/misuse from different IP | Alert, consider key rotation, scope limiting | CRITICAL |
| EC-SEC-API-003 | Replay attack (reusing signed request) | Timestamp validation, nonce, request signing | HIGH |
| EC-SEC-API-004 | Mass assignment (unexpected fields in request) | Whitelist accepted fields, ignore others | HIGH |
| EC-SEC-API-005 | Excessive data exposure in response | Return only needed fields, use DTOs | MEDIUM |
| EC-SEC-API-006 | Missing rate limiting on expensive operations | Implement per-endpoint, per-user limits | HIGH |
| EC-SEC-API-007 | GraphQL introspection in production | Disable introspection, limit query depth | HIGH |
| EC-SEC-API-008 | Broken function level authorization | Verify permissions per endpoint, not just authentication | CRITICAL |

---

### Data Protection (OWASP A02:2021 - Cryptographic Failures)

**Trigger Keywords**:
```text
encrypt, decrypt, hash, secret, sensitive, personal,
pii, gdpr, hipaa, pci, credit card, ssn, password store
```

**Edge Cases**:

| ID | Condition | Expected Behavior | Severity |
|----|-----------|-------------------|----------|
| EC-SEC-DATA-001 | Sensitive data in logs | Mask/redact PII in all log outputs | CRITICAL |
| EC-SEC-DATA-002 | Unencrypted sensitive data at rest | Encrypt with AES-256 or equivalent | CRITICAL |
| EC-SEC-DATA-003 | Weak hashing algorithm for passwords | Use bcrypt/scrypt/argon2, not MD5/SHA1 | CRITICAL |
| EC-SEC-DATA-004 | Hardcoded secrets in code/config | Use secrets manager, environment variables | CRITICAL |
| EC-SEC-DATA-005 | Sensitive data in URL parameters | Use POST body or headers, not query string | HIGH |
| EC-SEC-DATA-006 | Missing TLS for data in transit | Enforce HTTPS, HSTS | CRITICAL |

---

## Generation Algorithm

```text
GENERATE_SECURITY_EDGE_CASES(functional_requirements, existing_ec = []):

  edge_cases = []
  requirements_text = JOIN(functional_requirements)

  # Detect security triggers
  triggers = DETECT_SECURITY_TRIGGERS(requirements_text)

  FOR trigger IN triggers:
    FOR ec IN trigger.edge_cases:
      # Skip if similar EC already exists
      IF NOT EXISTS_SIMILAR(existing_ec, ec.condition):
        edge_cases.append({
          id: ec.id,
          condition: ec.condition,
          expected_behavior: ec.expected_behavior,
          severity: ec.severity,
          category: "security",
          owasp_ref: trigger.owasp_ref,
          trigger_keyword: trigger.keyword_matched,
          auto_generated: true,
          confidence: 0.95  # High confidence for pattern-matched security
        })

  # Deduplicate by ID
  RETURN DEDUPLICATE_BY_ID(edge_cases)

EXISTS_SIMILAR(edge_cases, condition):
  # Check for semantic similarity to avoid duplicates
  FOR ec IN edge_cases:
    IF SIMILARITY(ec.condition, condition) > 0.8:
      RETURN true
  RETURN false
```

---

## Confidence Scoring

| Detection Method | Confidence |
|-----------------|------------|
| Direct keyword match + OWASP pattern | 0.95 |
| Inferred from context (e.g., "user data" implies input validation) | 0.75 |
| Entity-type heuristic (e.g., password field) | 0.80 |
| LLM-generated (novel security scenario) | 0.60 |

---

## Coverage Calculation

```text
CALCULATE_SECURITY_COVERAGE(triggers, edge_cases):

  coverage = {
    triggers_found: triggers.length,
    categories_covered: 0,
    category_details: []
  }

  FOR trigger IN triggers:
    # Count EC for this category
    category_ec = FILTER(edge_cases, e =>
      e.category == "security" AND
      e.owasp_ref == trigger.owasp_ref
    )

    # Minimum expected EC per category
    min_expected = {
      "auth": 3,
      "injection": 3,
      "access_control": 3,
      "session": 2,
      "file": 3,
      "api": 2,
      "data": 2
    }[trigger.category] OR 2

    IF category_ec.length >= min_expected:
      coverage.categories_covered += 1
      status = "covered"
    ELSE:
      status = "partial"

    coverage.category_details.append({
      category: trigger.category,
      owasp: trigger.owasp_ref,
      keyword: trigger.keyword_matched,
      ec_count: category_ec.length,
      min_expected: min_expected,
      status: status
    })

  IF coverage.triggers_found > 0:
    coverage.score = coverage.categories_covered / coverage.triggers_found
  ELSE:
    coverage.score = 1.0  # No security features = no security EC needed

  RETURN coverage
```

---

## Integration with Self-Review

Security coverage triggers SR-SPEC-13 validation:

```text
SR-SPEC-13: Security edge cases for auth/input features?
  severity: HIGH
  auto_fixable: false  # Security EC require human review

  check_fn(artifact):
    requirements = EXTRACT_REQUIREMENTS(artifact)
    edge_cases = EXTRACT_EDGE_CASES(artifact)

    triggers = DETECT_SECURITY_TRIGGERS(JOIN(requirements))

    IF triggers.length == 0:
      RETURN {status: PASS, details: "No security features detected"}

    coverage = CALCULATE_SECURITY_COVERAGE(triggers, edge_cases)

    IF coverage.score >= 1.0:
      RETURN {
        status: PASS,
        details: "{triggers.length} security categories fully covered"
      }
    ELSE:
      uncovered = FILTER(coverage.category_details, d => d.status != "covered")
      RETURN {
        status: FAIL,
        details: "Missing security EC for: {uncovered.map(c => c.category).join(', ')}",
        suggestions: GENERATE_SECURITY_EDGE_CASES(requirements, edge_cases)
      }
```

---

## Quick Reference: Minimum Security EC by Feature Type

| Feature Type | Trigger Keywords | Minimum CRITICAL EC |
|--------------|-----------------|---------------------|
| User login | auth, login | 3 (credentials, brute force, session) |
| Form input | input, form, submit | 2 (SQL injection, XSS) |
| User registration | register, signup | 3 (enumeration, password, validation) |
| Admin panel | admin, permission, role | 3 (escalation, IDOR, authorization) |
| File upload | upload, file, attachment | 3 (malware, type bypass, path traversal) |
| API endpoint | api, endpoint | 2 (rate limit, broken auth) |
| Password reset | reset, forgot | 2 (token security, enumeration) |
| Session management | session, cookie | 2 (hijacking, CSRF) |
| Data export | export, download, pii | 2 (unauthorized access, data exposure) |

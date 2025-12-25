---
description: Perform security audit of specification and/or code against OWASP and constitution principles
---

## User Input

```text
$ARGUMENTS
```

## Purpose

This skill performs a comprehensive security audit against OWASP Top 10, constitution security principles (SEC-xxx), and industry best practices. Can audit specifications (pre-implementation) or code (post-implementation).

## When to Use

- After `/speckit.specify` to validate security requirements
- Before `/speckit.implement` to identify security concerns
- During `/speckit.analyze` QA mode for security verification
- When preparing for security review or compliance

## Execution Steps

### 1. Determine Audit Mode

```text
IF codebase exists AND user wants code audit:
  MODE = CODE_AUDIT
  Use Task(subagent_type="Explore") for code analysis
ELSE:
  MODE = SPEC_AUDIT
  Analyze specification documents only
```

### 2. Load Security Context

```text
1. Read memory/constitution.md for SEC-xxx principles
2. Read memory/constitution.base.md for base security requirements
3. Read memory/constitution.domain.md for domain-specific security (if exists)
4. Read spec.md for feature security requirements
```

### 3. OWASP Top 10 Checklist (2021)

Evaluate against each OWASP category:

#### A01: Broken Access Control
```markdown
## A01: Broken Access Control

**Spec Audit**:
- [ ] Authorization requirements defined for all endpoints
- [ ] Role-based access documented
- [ ] Resource ownership rules specified
- [ ] Privilege escalation scenarios covered

**Code Audit** (if applicable):
- [ ] Authorization checks present on all routes
- [ ] No IDOR vulnerabilities (object references validated)
- [ ] Default deny policy implemented
- [ ] JWT/session validation on protected routes

**Finding**: [PASS/WARN/FAIL]
**Details**: [specific findings]
```

#### A02: Cryptographic Failures
```markdown
## A02: Cryptographic Failures

**Spec Audit**:
- [ ] Sensitive data classification defined
- [ ] Encryption requirements specified
- [ ] Key management approach documented
- [ ] Data-at-rest and in-transit encryption required

**Code Audit**:
- [ ] TLS 1.2+ enforced
- [ ] Strong algorithms used (no MD5, SHA1, DES)
- [ ] Secrets not hardcoded
- [ ] Proper key rotation mechanism

**Finding**: [PASS/WARN/FAIL]
```

#### A03: Injection
```markdown
## A03: Injection

**Spec Audit**:
- [ ] Input validation requirements specified
- [ ] Sanitization rules documented
- [ ] Parameterized query requirement stated

**Code Audit**:
- [ ] SQL injection: parameterized queries used
- [ ] XSS: output encoding applied
- [ ] Command injection: input not passed to shell
- [ ] LDAP/NoSQL injection: proper escaping

**Finding**: [PASS/WARN/FAIL]
```

#### A04: Insecure Design
```markdown
## A04: Insecure Design

**Spec Audit**:
- [ ] Threat model documented
- [ ] Security requirements derived from threats
- [ ] Abuse cases considered
- [ ] Defense in depth approach

**Code Audit**:
- [ ] Security controls at multiple layers
- [ ] Rate limiting implemented
- [ ] Resource limits defined
- [ ] Fail-secure defaults

**Finding**: [PASS/WARN/FAIL]
```

#### A05: Security Misconfiguration
```markdown
## A05: Security Misconfiguration

**Spec Audit**:
- [ ] Security configuration requirements documented
- [ ] Default credentials prohibited
- [ ] Error handling requirements specified

**Code Audit**:
- [ ] Security headers configured
- [ ] Debug mode disabled in production
- [ ] Directory listing disabled
- [ ] Unnecessary features removed

**Finding**: [PASS/WARN/FAIL]
```

#### A06: Vulnerable Components
```markdown
## A06: Vulnerable Components

**Spec Audit**:
- [ ] Dependency management policy defined
- [ ] Version pinning required
- [ ] Security update process documented

**Code Audit**:
- [ ] No known CVEs in dependencies (npm audit, snyk)
- [ ] Dependencies up to date
- [ ] Unused dependencies removed
- [ ] License compliance checked

**Finding**: [PASS/WARN/FAIL]
```

#### A07: Authentication Failures
```markdown
## A07: Authentication Failures

**Spec Audit**:
- [ ] Password policy defined
- [ ] MFA requirements specified
- [ ] Session management documented
- [ ] Account lockout policy defined

**Code Audit**:
- [ ] Secure password storage (bcrypt, argon2)
- [ ] Session timeout implemented
- [ ] Brute force protection
- [ ] Secure session tokens

**Finding**: [PASS/WARN/FAIL]
```

#### A08: Data Integrity Failures
```markdown
## A08: Data Integrity Failures

**Spec Audit**:
- [ ] Data validation requirements defined
- [ ] Integrity checks specified
- [ ] CI/CD security requirements documented

**Code Audit**:
- [ ] Signed artifacts in CI/CD
- [ ] Integrity verification on downloads
- [ ] Deserialization safety

**Finding**: [PASS/WARN/FAIL]
```

#### A09: Security Logging Failures
```markdown
## A09: Security Logging Failures

**Spec Audit**:
- [ ] Security event logging required
- [ ] Log retention policy defined
- [ ] Alerting requirements specified

**Code Audit**:
- [ ] Login attempts logged
- [ ] Sensitive operations audited
- [ ] Logs tamper-protected
- [ ] No sensitive data in logs

**Finding**: [PASS/WARN/FAIL]
```

#### A10: SSRF
```markdown
## A10: Server-Side Request Forgery

**Spec Audit**:
- [ ] External request requirements documented
- [ ] Allowed destinations whitelisted

**Code Audit**:
- [ ] URL validation before requests
- [ ] Internal network access blocked
- [ ] Response validation

**Finding**: [PASS/WARN/FAIL]
```

### 4. Constitution Security Principles

Check against SEC-xxx from constitution:

```text
FOR EACH SEC-xxx principle in constitution:
  Validate compliance
  Document finding
  Rate: PASS/WARN/FAIL
```

### 5. Domain-Specific Security

If domain layer is active (fintech, healthcare, etc.):

```text
Load domain-specific security requirements
Validate additional compliance needs:
- Fintech: PCI-DSS considerations
- Healthcare: HIPAA considerations
- SaaS: Multi-tenant isolation
```

### 6. Generate Audit Report

Create security audit report:

```markdown
# Security Audit Report

**Feature**: [spec path]
**Date**: [DATE]
**Mode**: [SPEC_AUDIT/CODE_AUDIT]
**Auditor**: Claude Code (security-audit skill)

## Executive Summary

**Overall Rating**: [PASS/CONCERNS/FAIL]
**Critical Issues**: [N]
**High Issues**: [N]
**Medium Issues**: [N]
**Low Issues**: [N]

## OWASP Top 10 Summary

| Category | Status | Issues |
|----------|--------|--------|
| A01: Broken Access Control | ✓/⚠/✗ | [count] |
| A02: Cryptographic Failures | ✓/⚠/✗ | [count] |
| A03: Injection | ✓/⚠/✗ | [count] |
| A04: Insecure Design | ✓/⚠/✗ | [count] |
| A05: Security Misconfiguration | ✓/⚠/✗ | [count] |
| A06: Vulnerable Components | ✓/⚠/✗ | [count] |
| A07: Authentication Failures | ✓/⚠/✗ | [count] |
| A08: Data Integrity Failures | ✓/⚠/✗ | [count] |
| A09: Logging Failures | ✓/⚠/✗ | [count] |
| A10: SSRF | ✓/⚠/✗ | [count] |

## Constitution Compliance

| Principle | Level | Status |
|-----------|-------|--------|
| SEC-001 | MUST | ✓/✗ |
| SEC-002 | MUST | ✓/✗ |
| ... | ... | ... |

## Critical Issues

### [ISSUE-001]: [Title]
- **Category**: A0X - [OWASP Category]
- **Severity**: CRITICAL
- **Location**: [spec section / code file:line]
- **Description**: [what's wrong]
- **Impact**: [potential damage]
- **Recommendation**: [how to fix]
- **References**: [CWE/CVE links]

## High Issues
[Similar format]

## Medium Issues
[Similar format]

## Low Issues
[Similar format]

## Recommendations

### Immediate Actions (Critical/High)
1. [Action with priority]

### Short-term (Medium)
1. [Action]

### Long-term (Low)
1. [Action]

## Next Steps

- [ ] Address all CRITICAL issues before implementation
- [ ] Address HIGH issues before release
- [ ] Schedule MEDIUM issues for next sprint
- [ ] Track LOW issues in backlog
```

## Output

1. Audit report (inline or saved to `specs/[feature]/security-audit.md`)
2. Issue count by severity
3. Constitution compliance status
4. Recommended next steps

## Integration with Spec Kit

Feeds into:
- `/speckit.specify` → Security requirement gaps
- `/speckit.analyze` → QA mode security verification
- `/speckit.implement` → Security-conscious implementation

## Quick Mode

For rapid security check:

```text
/speckit.security-audit --quick

Checks:
- OWASP Top 10 high-level
- Constitution SEC principles
- Obvious vulnerabilities

Skips:
- Detailed code analysis
- Full report generation
```

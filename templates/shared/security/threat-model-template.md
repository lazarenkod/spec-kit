# Threat Model: {{FEATURE_NAME}}

> **STRIDE-based threat analysis for security requirements derivation**

**Feature**: {{FEATURE_NAME}}
**Data Classification**: {{DATA_CLASSIFICATION}}
**Created**: {{DATE}}
**Last Updated**: {{DATE}}
**Status**: [ Draft | In Review | Approved ]

---

## 1. System Overview

### 1.1 Description

<!--
  Describe what the feature does, its purpose, and how users interact with it.
  Include the data flow at a high level.
-->

[Describe the feature and its core functionality]

### 1.2 Data Sensitivity

| Classification | Data Types | Justification |
|----------------|------------|---------------|
| **Restricted** | [e.g., API keys, passwords] | [why this classification] |
| **Confidential** | [e.g., user PII, payment info] | [why this classification] |
| **Internal** | [e.g., analytics, logs] | [why this classification] |
| **Public** | [e.g., product catalog] | [why this classification] |

**Highest Classification**: {{HIGHEST_CLASSIFICATION}}

### 1.3 Architecture Diagram

<!--
  Include or reference an architecture diagram showing:
  - Components involved
  - Data flows
  - Trust boundaries
-->

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET (Untrusted)                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ═══════════════════════════ Trust Boundary 1
                                │
┌─────────────────────────────────────────────────────────────────┐
│                         DMZ / Edge                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ WAF / CDN   │───▶│ Load Balancer│───▶│ API Gateway │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ═══════════════════════════ Trust Boundary 2
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      Application Tier                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ Auth Service│    │ Feature Svc │    │ Other Svcs  │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ═══════════════════════════ Trust Boundary 3
                                │
┌─────────────────────────────────────────────────────────────────┐
│                         Data Tier                                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  Database   │    │    Cache    │    │  File Store │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Assets

<!--
  List all assets that need protection in this feature.
  Assets = data, functionality, or resources that have value.
-->

| Asset ID | Name | Description | Classification | Owner | Location |
|----------|------|-------------|----------------|-------|----------|
| ASSET-001 | User credentials | Usernames, password hashes | Restricted | Auth Service | Database |
| ASSET-002 | Session tokens | JWT/session data | Restricted | Auth Service | Memory/Cookie |
| ASSET-003 | User PII | Name, email, address | Confidential | User Service | Database |
| ASSET-004 | Order data | Purchase history | Confidential | Order Service | Database |
| ASSET-005 | Product catalog | Public product info | Public | Catalog Service | Database |

---

## 3. Trust Boundaries

<!--
  Define where trust changes in the system.
  Each boundary crossing requires validation.
-->

| Boundary ID | Name | From | To | Validation Required |
|-------------|------|------|----|--------------------|
| TB-001 | Internet → Edge | Untrusted users | WAF/CDN | Rate limiting, basic filtering |
| TB-002 | Edge → Application | API Gateway | Services | JWT validation, authorization |
| TB-003 | Application → Data | Services | Database | Connection auth, query validation |
| TB-004 | Service → Service | Internal service | Internal service | mTLS, service tokens |

---

## 4. STRIDE Threat Analysis

<!--
  For each threat category, identify specific threats to this feature.
  Use the asset and trust boundary inventory above.
-->

### 4.1 Spoofing (Identity)

> Pretending to be something or someone else

| Threat ID | Threat | Asset | Attack Vector | Likelihood | Impact | Risk |
|-----------|--------|-------|---------------|------------|--------|------|
| T-S-001 | Credential theft via phishing | ASSET-001 | Social engineering | Medium | High | HIGH |
| T-S-002 | Session hijacking | ASSET-002 | XSS, network sniffing | Medium | High | HIGH |
| T-S-003 | API key theft | ASSET-001 | Code leak, logs | Medium | Critical | CRITICAL |

**Mitigations**:
| Threat ID | Mitigation | Control Type | Mapped Requirement |
|-----------|------------|--------------|-------------------|
| T-S-001 | MFA for sensitive operations | Preventive | SEC-AUTHN-001 |
| T-S-002 | Secure cookie flags, short session TTL | Preventive | SEC-AUTHN-002 |
| T-S-003 | Secret scanning, env-based secrets | Detective/Preventive | SEC-CONFIG-001 |

### 4.2 Tampering (Integrity)

> Modifying data or code

| Threat ID | Threat | Asset | Attack Vector | Likelihood | Impact | Risk |
|-----------|--------|-------|---------------|------------|--------|------|
| T-T-001 | Man-in-the-middle attack | All transit | Network interception | Low | High | MEDIUM |
| T-T-002 | Parameter manipulation | ASSET-004 | Modified requests | Medium | Medium | MEDIUM |
| T-T-003 | Database tampering | All | SQL injection | Low | Critical | HIGH |

**Mitigations**:
| Threat ID | Mitigation | Control Type | Mapped Requirement |
|-----------|------------|--------------|-------------------|
| T-T-001 | TLS 1.3 everywhere, HSTS | Preventive | SEC-CRYPTO-001 |
| T-T-002 | Server-side validation, signed params | Preventive | SEC-INPUT-001 |
| T-T-003 | Parameterized queries, ORM | Preventive | SEC-INPUT-002 |

### 4.3 Repudiation (Audit)

> Claiming not to have performed an action

| Threat ID | Threat | Asset | Attack Vector | Likelihood | Impact | Risk |
|-----------|--------|-------|---------------|------------|--------|------|
| T-R-001 | Deny transaction | ASSET-004 | Missing audit trail | Medium | Medium | MEDIUM |
| T-R-002 | Tampered logs | Audit logs | Log manipulation | Low | High | MEDIUM |

**Mitigations**:
| Threat ID | Mitigation | Control Type | Mapped Requirement |
|-----------|------------|--------------|-------------------|
| T-R-001 | Comprehensive audit logging | Detective | SEC-LOG-001 |
| T-R-002 | Tamper-evident logging, log shipping | Detective | SEC-LOG-002 |

### 4.4 Information Disclosure (Confidentiality)

> Exposing information to unauthorized parties

| Threat ID | Threat | Asset | Attack Vector | Likelihood | Impact | Risk |
|-----------|--------|-------|---------------|------------|--------|------|
| T-I-001 | PII exposure in logs | ASSET-003 | Log access | Medium | High | HIGH |
| T-I-002 | Verbose error messages | System info | Error handling | High | Low | MEDIUM |
| T-I-003 | Unauthorized data access | ASSET-003,004 | Broken access control | Medium | High | HIGH |

**Mitigations**:
| Threat ID | Mitigation | Control Type | Mapped Requirement |
|-----------|------------|--------------|-------------------|
| T-I-001 | PII masking in logs | Preventive | SEC-LOG-003 |
| T-I-002 | Generic error messages, detailed internal | Preventive | SEC-CONFIG-002 |
| T-I-003 | Complete mediation, ownership checks | Preventive | SEC-AUTHZ-001 |

### 4.5 Denial of Service (Availability)

> Making the system unavailable

| Threat ID | Threat | Asset | Attack Vector | Likelihood | Impact | Risk |
|-----------|--------|-------|---------------|------------|--------|------|
| T-D-001 | API rate abuse | Service availability | Automated requests | High | Medium | HIGH |
| T-D-002 | Resource exhaustion | Database | Expensive queries | Medium | High | HIGH |

**Mitigations**:
| Threat ID | Mitigation | Control Type | Mapped Requirement |
|-----------|------------|--------------|-------------------|
| T-D-001 | Rate limiting, WAF rules | Preventive | SEC-AVAIL-001 |
| T-D-002 | Query timeouts, pagination limits | Preventive | SEC-AVAIL-002 |

### 4.6 Elevation of Privilege (Authorization)

> Gaining capabilities without authorization

| Threat ID | Threat | Asset | Attack Vector | Likelihood | Impact | Risk |
|-----------|--------|-------|---------------|------------|--------|------|
| T-E-001 | Privilege escalation | Admin functions | Broken access control | Medium | Critical | CRITICAL |
| T-E-002 | IDOR (Insecure Direct Object Ref) | ASSET-003,004 | Guessable IDs | High | High | HIGH |

**Mitigations**:
| Threat ID | Mitigation | Control Type | Mapped Requirement |
|-----------|------------|--------------|-------------------|
| T-E-001 | RBAC enforcement, least privilege | Preventive | SEC-AUTHZ-002 |
| T-E-002 | UUID for references, ownership validation | Preventive | SEC-AUTHZ-003 |

---

## 5. DREAD Risk Scoring

<!--
  Score each high/critical threat for prioritization.
  Scale: 1-3 (Low-High)
-->

| Threat ID | Damage | Reproducibility | Exploitability | Affected Users | Discoverability | Total | Priority |
|-----------|--------|-----------------|----------------|----------------|-----------------|-------|----------|
| T-S-003 | 3 | 2 | 2 | 3 | 2 | 12 | P0 |
| T-E-001 | 3 | 2 | 2 | 3 | 2 | 12 | P0 |
| T-E-002 | 2 | 3 | 3 | 2 | 3 | 13 | P0 |
| T-S-001 | 2 | 3 | 2 | 2 | 3 | 12 | P1 |
| T-S-002 | 2 | 2 | 2 | 2 | 2 | 10 | P1 |
| T-I-003 | 2 | 2 | 2 | 2 | 2 | 10 | P1 |

**Priority Legend**:
- P0 (12-15): Must address before implementation
- P1 (9-11): Address in initial release
- P2 (6-8): Address in subsequent release
- P3 (3-5): Accept or defer

---

## 6. Security Requirements Derived

<!--
  Map mitigations to formal security requirements for spec.md
-->

| Req ID | Description | Source Threats | Priority | Acceptance Criteria |
|--------|-------------|----------------|----------|---------------------|
| SEC-AUTHN-001 | MFA for sensitive operations | T-S-001 | P1 | MFA prompt on payment, password change |
| SEC-AUTHN-002 | Secure session management | T-S-002 | P0 | HttpOnly, Secure, SameSite=Strict, 15min idle timeout |
| SEC-AUTHZ-001 | Complete mediation | T-I-003, T-E-001 | P0 | Every request validates user permissions |
| SEC-AUTHZ-002 | RBAC enforcement | T-E-001 | P0 | Role-based access with least privilege |
| SEC-AUTHZ-003 | No IDOR vulnerabilities | T-E-002 | P0 | UUID references, ownership validation |
| SEC-CRYPTO-001 | TLS 1.3 everywhere | T-T-001 | P0 | No plaintext connections, HSTS enabled |
| SEC-INPUT-001 | Server-side validation | T-T-002 | P0 | All inputs validated on server |
| SEC-INPUT-002 | SQL injection prevention | T-T-003 | P0 | Parameterized queries only |
| SEC-LOG-001 | Audit logging | T-R-001 | P1 | Auth, access, changes logged |
| SEC-LOG-002 | Tamper-evident logs | T-R-002 | P2 | Log shipping, immutable storage |
| SEC-LOG-003 | PII masking | T-I-001 | P1 | No PII in logs |
| SEC-CONFIG-001 | Secret management | T-S-003 | P0 | Env-based secrets, no hardcoding |
| SEC-CONFIG-002 | Error handling | T-I-002 | P1 | Generic errors to users |
| SEC-AVAIL-001 | Rate limiting | T-D-001 | P1 | 100 req/min per user |
| SEC-AVAIL-002 | Query protection | T-D-002 | P1 | Timeouts, pagination |

---

## 7. Residual Risks

<!--
  Risks that remain after mitigations, requiring acceptance or monitoring.
-->

| Risk ID | Description | Mitigation Status | Residual Level | Acceptance |
|---------|-------------|-------------------|----------------|------------|
| RR-001 | Phishing attacks | Partial (MFA helps) | Medium | Accepted - user education |
| RR-002 | Zero-day vulnerabilities | Monitoring only | Medium | Accepted - incident response |
| RR-003 | Insider threats | Audit logging | Medium | Accepted - background checks |

---

## 8. Review & Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Author | [Name] | {{DATE}} | Draft |
| Security Review | [Name] | - | Pending |
| Tech Lead | [Name] | - | Pending |
| Product Owner | [Name] | - | Pending |

---

## Appendix: STRIDE Reference

| Category | Definition | Question to Ask |
|----------|------------|-----------------|
| **S**poofing | Impersonating something or someone | Can an attacker pretend to be a user/system? |
| **T**ampering | Modifying data or code | Can an attacker modify data in transit/at rest? |
| **R**epudiation | Denying having performed an action | Can an attacker deny their actions? |
| **I**nfo Disclosure | Exposing information | Can an attacker access unauthorized data? |
| **D**enial of Service | Making system unavailable | Can an attacker disrupt service? |
| **E**levation of Privilege | Gaining unauthorized access | Can an attacker gain higher permissions? |

---

*Threat Model Template v1.0 | Part of Spec Kit Security by Design Framework*

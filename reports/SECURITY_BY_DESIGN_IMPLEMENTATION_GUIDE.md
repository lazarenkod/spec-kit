# Security by Design: Practical Implementation Guide for Spec-Kit

**Purpose:** Step-by-step guide to actually implement Security by Design in your projects using spec-kit commands

**Audience:** Product teams, architects, developers using /speckit.* workflow

---

## Part 1: Before You Start

### Decide Your Security Framework

Choose based on your needs:

**Choose OWASP if:**
- Shipping consumer/SaaS products
- Focused on architectural design
- Want design-phase security checklist
- Team size: small to medium

**Choose NIST SSDF if:**
- Working on government contracts
- Need compliance certification (OMB M-22-18)
- Building enterprise software for regulated orgs
- Team size: medium to large
- Risk tolerance: very low

**Choose ISO 27001 if:**
- Managing information security system company-wide
- Need formal ISMS audit/certification
- Working with enterprises requiring ISO compliance
- Team size: large
- Focus: governance + controls

**Hybrid Approach (Recommended):**
Use OWASP for design-phase security + NIST SSDF structure + ISO 27001 controls mapping

### Assess Your Risk Profile

**Ask these questions:**

1. **What data do you handle?**
   - Financial data → PCI DSS required
   - Health data → HIPAA required
   - Personal data (any) → GDPR required
   - Authentication data → Always sensitive

2. **Who are your threat actors?**
   - External attackers (most common)
   - Insiders with access
   - Competitors
   - Regulators/compliance entities
   - Nation-state actors (rare but possible)

3. **What's your risk tolerance?**
   - Startup: Medium (fail fast, but protect customer data)
   - SMB: Medium-High (reputational damage is costly)
   - Enterprise: Very Low (regulatory requirements strict)
   - Healthcare/Finance: Extremely Low (legal liability)

4. **What's your customer's security expectation?**
   - B2C consumers: Basic encryption + privacy
   - SMB customers: SOC 2 Type II desired
   - Enterprise customers: SOC 2 Type II mandatory; possibly FedRAMP/ISO
   - Regulated industry: Specific compliance required (HIPAA, PCI)

**Action:** Document risk profile in `/speckit.constitution` (see Part 2)

---

## Part 2: Constitution Phase - Establish Governance

### Task: Create Security Constitution

**Command:** Use `/speckit.constitution` to create `constitution.md`

**Template:**

```markdown
# Project Security Constitution

## Security Philosophy
We build security in from day one, following [OWASP | NIST | ISO 27001] principles.
Security is a design constraint, not an afterthought.

## Core Security Principles

### 1. Least Privilege
Every user, service, and component gets minimum permissions needed.
- Default: Deny all access
- Grant: Only specific permissions required for function
- Review: Quarterly access audit to revoke unused permissions

### 2. Defense in Depth
Multiple layers of security controls prevent single point of compromise.
- Authentication (who are you?)
- Authorization (what can you do?)
- Encryption (protect data)
- Logging (detect attacks)
- Monitoring (respond to incidents)

### 3. Secure Defaults
Safe, secure configuration out-of-the-box.
- Default: Users opt-out of unsafe features
- Not: Users opt-in to security features
- Example: Encryption enabled by default; users disable if needed

### 4. Minimize Attack Surface
Only expose what's necessary.
- Dependencies: Justify every external package
- Endpoints: Don't expose unused APIs
- Ports: Close what's not needed
- Features: Remove unused functionality

### 5. Complete Mediation
Verify authorization everywhere, always.
- API Gateway checks authentication
- Each microservice re-verifies authorization (don't trust gateway)
- Database access includes user context
- No caching of permission decisions (except short-term with validation)

## Security Governance

### Roles and Responsibilities

| Role | Responsibility | Review Authority |
|------|-----------------|-----------------|
| Security Architect | Threat modeling, architecture review, security standards | Approve all security designs |
| Product Manager | Include security requirements in spec; prioritize security fixes | Approve threat models |
| Tech Lead | Implement secure code; code reviews; secure defaults | Approve code before merge |
| QA Lead | Security testing; penetration testing; validation | Approve security tests |
| DevOps | Infrastructure hardening; secrets management; monitoring | Approve deployment config |
| Leadership | Security budget; incident response; breach disclosure | Overall security posture |

### Security Review Gates

**Code Review Gate:**
```
Before merging security-related code, require:
- Code review from security architect OR senior engineer trained in secure coding
- SAST tool passes (SonarQube/Checkmarx)
- No hardcoded secrets (automated check)
- Dependency check passes
```

**Architecture Review Gate:**
```
Before implementation, require:
- Threat model created and reviewed
- Security architecture documented
- Control design approved
- Test strategy for security validated
```

**Deployment Gate:**
```
Before production release, require:
- Penetration testing completed
- All high-severity findings remediated
- Infrastructure security checklist passed
- Incident response plan activated
- Monitoring dashboard operational
```

## Security Standards

### Frameworks We Follow
- **Design Phase:** OWASP Secure-by-Design Framework
- **SDLC:** NIST SSDF v1.1 (42 tasks across 4 categories)
- **Controls:** ISO 27001 Annex A (security controls)
- **Requirements:** OWASP ASVS (what to build)
- **Testing:** OWASP Top 10 + CWE Top 25 (what to test)

### Secure Coding Standards
- **Language:** [Your language] OWASP Secure Coding Practices
- **Crypto:** Use approved libraries (OpenSSL, libsodium, TweetNaCl)
- **Secrets:** Never hardcode; use vault or environment variables
- **Input:** Validate and sanitize all external input
- **Output:** Encode output appropriate to context (HTML/JSON/URL)
- **Errors:** Fail securely; don't expose internals

### Security Tools

**Code & Dependency Analysis:**
- SAST: [Tool] (runs in CI pipeline)
- SCA: [Tool] (dependency scanning)
- Container: [Tool] (image scanning)
- Secrets: GitGuardian or similar

**Infrastructure & Deployment:**
- IaC scanning: Trivy/Checkov
- Secrets management: Vault/AWS Secrets Manager
- Network: [Firewall rules, WAF rules]
- Monitoring: [SIEM/logging platform]

## Communication & Escalation

**Security Issue Discovery:**
1. Finder reports to security architect immediately (don't leave on issue tracker)
2. Security architect assesses severity and impact
3. If critical: Breach protocol (CEO, legal, customers informed per policy)
4. If high: Fix immediately; communicate in post-incident review
5. If medium/low: Track as normal bug; prioritize accordingly

**Quarterly Security Review:**
- Security team reviews threat models vs. actual incidents
- Update threat models based on new threat vectors
- Review compliance status
- Present security metrics to leadership

## Security Incident Response

**On Security Incident Discovery:**
1. Immediate: Contain the problem (disable access, roll back changes)
2. Within 1 hour: Notify security architect and leadership
3. Within 4 hours: Assess impact (what data/systems affected)
4. Within 24 hours: Notify customers if personal data exposed (regulatory requirement)
5. Post-incident: Root cause analysis; threat model update; preventive measures

**Incident Response Team:**
- Security architect: Leads investigation
- CTO: Authorizes remediation decisions
- DevOps: Executes containment/recovery
- Legal: Advises on notification obligations
- Communications: Manages customer/PR messaging

## Security Budget & Investment

**Annual Budget Allocation:**
- Security tooling: [X]% of engineering budget
- Security training: [X]% of engineering budget
- Penetration testing: [X]% of engineering budget
- Incident response: [X]% of engineering budget
- Security hiring: [X]% of headcount

**Infrastructure & Tools Investment:**
- SAST/SCA licenses: [Amount]
- Penetration testing: [Amount per quarter]
- Security monitoring: [Amount per month]
- Vault/Secrets management: [Amount per month]
- DDoS/WAF protection: [Amount per month]

## Compliance & Audit

**Certifications We Target:**
- [SOC 2 Type II - deadline]
- [ISO 27001 - if applicable]
- [Industry-specific: HIPAA/PCI/etc]

**External Audits:**
- SOC 2 audit: Annual
- Penetration testing: Bi-annual (or on-demand for major releases)
- Compliance audit: Annual

**Documentation & Evidence:**
- Threat models: Stored in [location]; versioned
- Architecture decisions: Stored in ADRs
- Security test results: Attached to release notes
- Incident logs: Centralized logging; 1-year retention
- Access audit logs: 90-day retention minimum

## Appendix: Quick Reference Links

- [Threat Modeling: 5-Step Process](#threat-modeling-5-steps)
- [Security Requirements Template](#requirements-template)
- [STRIDE Threat Categories](#stride-reference)
```

**Output:** Security Constitution document that establishes governance and principles

---

## Part 3: Concept Phase - Threat Landscape & Compliance

### Task: Map Threat Landscape and Compliance Requirements

**Command:** Use `/speckit.concept` with security-focused sections

**Template:**

```markdown
# Product Concept: [Product Name]

## Threat Landscape Analysis

### Our Industry Threats
- [Threat 1: External attackers exploiting web vulnerabilities]
- [Threat 2: Insider access with intent to steal data]
- [Threat 3: Infrastructure compromise via supply chain]
- [Threat 4: Regulatory fines for non-compliance]
- [Threat 5: Reputation damage from security incident]

### Threat Actors & Motivations

**External Attackers:**
- Motivation: Data theft (resell, ransom, or use for fraud)
- Capability: Script kiddies to sophisticated cybercriminals
- Target: Vulnerable endpoints, authentication systems
- Likelihood: Medium (if public-facing)

**Insider Threats:**
- Motivation: Data exfiltration for competing company or personal use
- Capability: Direct access to systems via legitimate credentials
- Target: Sensitive data, admin access
- Likelihood: Low (with proper access controls)

**Regulatory/Compliance:**
- Motivation: Ensure legal compliance
- Capability: Audit and inspection authority
- Target: Data handling, security controls documentation
- Likelihood: Certain (for regulated data)

### Key Attack Scenarios

**Scenario 1: Customer Data Breach**
- Attacker: External criminal
- Attack Vector: SQL injection in user API
- Impact: Customer PII exposed; GDPR fines ($20-50M); customer trust loss
- Mitigation: Input validation, parameterized queries, Web Application Firewall

**Scenario 2: Unauthorized Access by Insider**
- Attacker: Disgruntled employee with system access
- Attack Vector: Escalation of privilege; accessing customer data outside their role
- Impact: Lawsuit; jail time (likely); reputation damage
- Mitigation: Role-based access control; audit logging; monitoring for anomalies

**Scenario 3: Infrastructure Compromise via Supply Chain**
- Attacker: Nation-state or sophisticated cybercriminal
- Attack Vector: Compromised dependency or infrastructure tool
- Impact: System compromise; data theft; persistent access
- Mitigation: Dependency scanning; supply chain security; secrets management

## Compliance & Regulatory Requirements

### Applicable Frameworks

| Framework | Applicability | Deadline | Owner | Impact |
|-----------|---------------|----------|-------|--------|
| **GDPR** | Any EU customer data | Always | Product | Data minimization, retention, breach notification |
| **SOC 2 Type II** | Enterprise customer requirement | GA | Security | Audit controls, monitoring, incident response |
| **PCI DSS** | If processing payments | GA | DevOps | Encryption, access controls, monitoring |
| **HIPAA** | If health data (if applicable) | Varies | CTO | Encryption, audit, business associates |
| **Industry Standard** | [Your industry] | [Deadline] | [Owner] | [Impact] |

### Compliance Requirements Mapping

```
GDPR Requirement: Data Minimization
↓
Product Impact: Collect only data needed for feature
↓
Design Impact: Schema design must limit fields
↓
Implementation: Database design; data model review
↓
Testing: Audit log review; no unnecessary data collection

GDPR Requirement: Data Retention
↓
Product Impact: Delete data after 12 months of inactivity
↓
Design Impact: Implement scheduled deletion task
↓
Implementation: Cron job; data deletion query
↓
Testing: Verify data deleted after retention period
↓
Operations: Monitor deletion task; handle failures
```

### Data Classification

| Classification | Examples | Encryption | Access | Retention | Audit |
|-----------------|----------|-----------|--------|-----------|-------|
| **Public** | Product marketing, public API docs | No | Anyone | Indefinite | No |
| **Internal** | Employee emails, internal docs | Recommended | Employees only | 1-2 years | Yes |
| **Confidential** | Financial data, product roadmap | Required | Leadership only | Project duration | Yes |
| **PII** | User names, emails, phone | Required | User or admin only | Per compliance | Yes |
| **Secrets** | API keys, passwords, certs | Required (vault) | Service only | Until rotation | Yes |

## Security Competitive Advantage

**Our security positioning:**
- "Built-in security, not bolted-on" → Customer benefit: Lower risk
- "Transparent threat models" → Customer benefit: Know what's protected
- "Regular penetration testing" → Customer benefit: Proactive vulnerability hunting
- "Compliance by design" → Customer benefit: SOC 2/GDPR handled, not hacked in later

## Risk Assessment

### High-Risk Scenarios to Avoid

1. [Scenario]: Customer data exposed
   - Probability: Medium
   - Impact: Extreme ($20-50M GDPR fines, customer lawsuit, loss of trust)
   - Mitigation: Encryption, access controls, audit logging, penetration testing

2. [Scenario]: Service unavailable (DDoS or infrastructure failure)
   - Probability: Medium
   - Impact: High (SLA breach, customer churn, reputation)
   - Mitigation: DDoS protection, auto-scaling, multi-region failover, monitoring

3. [Scenario]: Insider steals data
   - Probability: Low
   - Impact: High (lawsuit, jail time, customer breach, reputation)
   - Mitigation: Role-based access, audit logging, anomaly detection, background checks

### Residual Risk

After implementing planned security controls, residual risk for this product:
- Data breach: Low (mitigated by encryption + access controls + monitoring)
- Compliance violation: Low (mitigated by designed-in compliance checks)
- Service disruption: Medium (mitigated by infrastructure redundancy)
- Insider threat: Low (mitigated by access controls + audit)

## Next Phase

Move to `/speckit.specify` to define security requirements for each feature
```

**Output:** Concept document mapping threat landscape, compliance requirements, and risk scenarios

---

## Part 4: Specify Phase - Security Requirements

### Task: Include Security Requirements in Feature Specifications

**Command:** Use `/speckit.specify` with dedicated security requirements section

**Template:**

```markdown
# Feature Specification: [Feature Name]

## Overview
[Feature description, user stories, business value]

## Functional Requirements
[What the feature does]

## Non-Functional Requirements

### Performance
[Performance requirements]

### Reliability
[Uptime, failover, recovery]

### Security Requirements ← **THIS IS NEW**

#### 1. Authentication & Authorization

**Requirement:** Only authenticated users can [perform action]
- Who can authenticate? [All users / Specific roles / Subscribers only]
- Authentication method: [OAuth 2.0 / JWT / MFA]
- Authorization method: [Role-based / Attribute-based]
- Audit: Log all access (user, timestamp, success/failure)

**Threat Mitigated:** Unauthorized access; account takeover
**Test Case:** Unauthenticated user attempts to access → Returns 401 Unauthorized

**Requirement:** User can only [action] on their own data
- Scope: User can only access [their own profile / their org / their team]
- Admin exception: Admins can access any data [with audit logging]
- Data isolation: Database queries filtered by user context

**Threat Mitigated:** Unauthorized data access; user impersonation
**Test Case:** User A attempts to access User B's data → Returns 403 Forbidden

**Requirement:** Admin-only actions require elevated authentication
- Admin actions: [List of actions requiring admin]
- Elevated auth: [Re-authentication / MFA / IP whitelist]
- Audit: Log all admin actions (user, action, timestamp, result)

**Threat Mitigated:** Privilege escalation; insider abuse
**Test Case:** Non-admin user attempts admin action → Returns 403

#### 2. Data Protection

**Requirement:** Sensitive data encrypted at rest
- Data: [PII fields, financial data, health info]
- Encryption: AES-256; key managed in vault
- Scope: All storage (database, cache, backups)
- Key rotation: Every [90 days / annually]

**Threat Mitigated:** Data theft from compromised storage
**Test Case:** Database inspected; sensitive columns encrypted

**Requirement:** Sensitive data encrypted in transit
- Protocol: TLS 1.2+ required (no downgrade to TLS 1.0/1.1)
- Certificate: Valid, chains to trusted root
- Endpoints: All API communication; no unencrypted fallback
- Testing: SSL Labs rating A or A+

**Threat Mitigated:** Man-in-the-middle attack; data tampering in transit
**Test Case:** HTTPS required; HTTP redirects to HTTPS or fails

**Requirement:** Sensitive data never logged
- Excluded from logs: [Passwords, PII, tokens, credit cards]
- If necessary to log: Tokenize or hash (never plaintext)
- Log retention: [Time period] before automatic deletion
- Access: Only security/support team can view logs; encrypted audit trail

**Threat Mitigated:** Credential theft from logs; data exposure via logging
**Test Case:** Application logs reviewed; no sensitive data present

#### 3. Input Validation & Output Encoding

**Requirement:** All user input validated
- Validation rules: [List input rules per field]
  - User name: Alphanumeric + underscore; 3-20 chars
  - Email: RFC 5322 compliant email format
  - Description: Max 500 chars; no HTML allowed
  - Price: Numeric; 2 decimal places; max 999999.99
- Rejection: Invalid input returns 400 Bad Request with error message
- No system details in error (e.g., "Invalid email" not "regex error at position 5")

**Threat Mitigated:** Injection attacks; data corruption; denial of service
**Test Case:** Invalid input rejected; valid input accepted

**Requirement:** All output encoded appropriately
- HTML context: HTML-encode special characters
- JSON context: JSON-encode strings
- URL context: URL-encode special characters
- SQL context: Use parameterized queries (never string concatenation)

**Threat Mitigated:** Cross-site scripting (XSS); SQL injection; template injection
**Test Case:** Try to inject script tags in input; output is escaped

#### 4. Audit & Logging

**Requirement:** All [action] events logged
- Event: [List events to log]
  - User login (success and failure)
  - Data access/export
  - Admin actions
  - Permission changes
  - Configuration changes
- Log details: Timestamp, user_id, action, result, IP address
- Sensitive data: Never log passwords, keys, PII (tokenize instead)

**Threat Mitigated:** Denial of repudiation; incident investigation; anomaly detection
**Test Case:** Event logged to central logging system with correct details

**Requirement:** Logs immutable and retained per compliance
- Retention: [Time period] before archive
- Immutability: Application cannot modify/delete logs
- Access: Read-only; separate authentication for log access
- Encryption: Logs encrypted in transit and at rest

**Threat Mitigated:** Log tampering (cover-up of unauthorized access)
**Test Case:** Verify logs cannot be deleted by application; access is audited

#### 5. Compliance

**GDPR Requirements:**
- Data minimization: Only collect [list fields] needed for feature
- Retention: Delete data after [time period] or user request
- Right to access: User can export data via [mechanism]
- Right to forget: User can request deletion via [mechanism]
- Data processing agreement: If processing on behalf of customer

**SOC 2 Requirements:**
- Audit controls: All access logged and retention [time period]
- Change management: All deployments logged; approved before execute
- Incident response: Incident response plan in place; tested [frequency]
- Monitoring: Security monitoring active 24/7; alerts [response time]

**PCI DSS Requirements** (if payment-related):
- No storage of: Full PAN, card verification code
- Tokenization: Credit cards replaced with tokens
- Encryption: PCI data encrypted; keys managed separately
- Network: PCI data isolated on separate network segment
```

**Output:** Feature specification with explicit security requirements mapped to threats and compliance

---

## Part 5: Plan Phase - Threat Modeling

### Task: Create Threat Model Before Implementation

**Command:** Use `/speckit.plan` with detailed threat modeling section

**Step 1: Create Architecture Diagram (DFD)**

```
Draw: [User] --> [Web Server] --> [API] --> [Database]
              --> [Cache]

Trust Boundary 1: Between user and web server (user input untrusted)
Trust Boundary 2: Between API and database (internal, more trusted)
```

**Step 2: List Components & Data Flows**

```
Components:
- User (external)
- Web Server (internal)
- API Service (internal)
- Database (internal)
- Cache (internal)
- Message Queue (internal)
- Analytics Service (external API call)

Data Flows:
1. User Request: HTTP request from user to web server (untrusted)
2. Server to API: Internal API call (semi-trusted; same organization)
3. API to DB: SQL query with user data (trusted format but user-influenced data)
4. API to Cache: Cache write with sensitive data (internal; encrypted)
5. API to Analytics: User action event sent (PII must be tokenized)
```

**Step 3: Apply STRIDE - Identify Threats**

```markdown
## Threat Identification

**Data Flow 1: User HTTP Request → Web Server**

Threat: Spoofing Identity
- Attacker: Malicious user pretends to be legitimate user
- Mechanism: Forge HTTP request with another user's ID
- Impact: Access another user's data
- Likelihood: High (trivial to forge request)
- Risk: 8/10 (Critical)
- Mitigation Design: Authenticate user with OAuth 2.0 + JWT token; validate token on every request
- Test: Unauthenticated request → 401; token from User B used by User A → 403

Threat: Tampering with Data
- Attacker: Attacker modifies request in transit
- Mechanism: Man-in-the-middle; intercept HTTP request and modify
- Impact: Modify user's data; cause unwanted actions
- Likelihood: Medium (possible on public WiFi)
- Risk: 7/10 (High)
- Mitigation Design: Enforce HTTPS with TLS 1.2+; certificate pinning on mobile
- Test: HTTP request → redirected to HTTPS or rejected; invalid cert → connection denied

Threat: Repudiation
- Attacker: User denies performing an action (no audit trail)
- Mechanism: Action not logged; no proof who did what
- Impact: Dispute over data modifications; regulatory violation
- Likelihood: High (if no logging)
- Risk: 7/10 (High)
- Mitigation Design: Log all requests (user_id, timestamp, action, result); immutable logs
- Test: Action logged to centralized logging; cannot be deleted

Threat: Information Disclosure
- Attacker: User sees another user's data (authorization bypass)
- Mechanism: Access unprotected endpoint; modify ID parameter
- Impact: Confidentiality breach; customer PII exposed
- Likelihood: High (common vulnerability)
- Risk: 9/10 (Critical)
- Mitigation Design: Check authorization on every data access; return 403 if denied; don't leak user existence via different error codes
- Test: User A cannot access User B's data; returns 403 (not 404 which leaks user exists)

Threat: Denial of Service
- Attacker: Attacker floods endpoint with requests
- Mechanism: Send thousands of requests per second
- Impact: Service unavailable; legitimate users can't access
- Likelihood: Medium
- Risk: 6/10 (High)
- Mitigation Design: Rate limiting per IP; DDoS protection (CloudFlare); auto-scaling
- Test: Exceed rate limit → 429 Too Many Requests; DDoS test via security vendor

Threat: Elevation of Privilege
- Attacker: Non-admin user becomes admin (escalates permissions)
- Mechanism: Modify token/session; exploit role-checking code
- Impact: Attacker can delete data, access everything, modify system
- Likelihood: Low (if authorization properly implemented)
- Risk: 9/10 (Critical if successful)
- Mitigation Design: Verify admin status on every admin action; role stored in backend (not client); audit all admin operations
- Test: Non-admin attempts admin action → 403; jwt decode attempt → token not trusted for role

**Data Flow 2: API Service → Database**

[Similar analysis for internal API call...]

**Data Flow 3: API → External Analytics Service**

Threat: Information Disclosure
- Attacker: Attacker intercepts API call to analytics; sees PII
- Impact: Customer PII exposed
- Likelihood: Low (internal communication)
- Risk: 7/10 (High)
- Mitigation Design: Tokenize/hash PII before sending to analytics; don't send plaintext email/phone
- Test: Audit analytics API call payloads; verify no PII sent

[Continue for all components and flows...]
```

**Step 4: Map Controls to Requirements**

```markdown
## Threat-Control-Requirement Mapping

| Threat | Component | Mitigation Control | Requirement | Implementation | Test |
|--------|-----------|-------------------|-------------|-----------------|------|
| Spoofing | User→WS | OAuth 2.0 + JWT | Auth & AuthZ | /speckit.implement token validation | Unauthenticated: 401 |
| Tampering | User→WS | TLS 1.2+ HTTPS | Data Protection | /speckit.implement TLS enforcement | HTTPS required; HTTP→HTTPS |
| Repudiation | All | Immutable audit logging | Audit Logging | /speckit.implement centralized logging | Event logged; retention verified |
| Info Disclosure | API→DB | Authorization checks | Auth & AuthZ | /speckit.implement authorization layer | User A: 403 for User B data |
| DoS | WS | Rate limiting | Resilience | /speckit.implement rate limiter | Exceed limit → 429 |
| Elevation | Admin | Backend role check | Auth & AuthZ | /speckit.implement RBAC | Non-admin: 403 for admin action |
```

**Step 5: Validation Plan**

```markdown
## Security Testing & Validation Plan

### Unit Tests
- [ ] User A cannot read/modify User B's data
- [ ] JWT validation rejects invalid tokens
- [ ] Admin role check rejects non-admins
- [ ] Input validation rejects invalid data

### Integration Tests
- [ ] Authorization flow: authenticate → verify permissions → access allowed/denied
- [ ] Audit logging: action logged with correct details
- [ ] Data encryption: sensitive fields encrypted in database
- [ ] Error handling: no sensitive data in error messages

### Penetration Testing
- [ ] Authorization bypass attempts
- [ ] JWT token forgery attempts
- [ ] SQL injection attempts
- [ ] XSS injection attempts
- [ ] Rate limiting bypass attempts

### Code Review Checklist
- [ ] No hardcoded credentials
- [ ] Parameterized queries (not string concatenation)
- [ ] Input validation on all external input
- [ ] Output encoding on all sensitive output
- [ ] No logging of sensitive data
- [ ] Proper error handling (no system details leaked)
```

**Output:** Threat model with STRIDE analysis, control design, and validation plan

---

## Part 6: Tasks Phase - Security Tasks

### Task: Define Security Implementation & Testing Tasks

**Command:** Use `/speckit.tasks` with security-focused task breakdown

**Template:**

```markdown
# Task Breakdown: [Feature Name]

## Implementation Tasks

### Task: Implement Authorization Check
**Description:** Add authorization check to API endpoint to verify user owns data
**Acceptance Criteria:**
- [ ] Code: User context extracted from JWT token; checked on every request
- [ ] Code: Return 403 Forbidden if user doesn't own data (not 404)
- [ ] Test: Unit test confirms User A cannot access User B
- [ ] Test: Integration test validates authorization flow end-to-end
- [ ] Review: Code review approved by [security architect]
- [ ] Merge gate: All tests pass; SAST tool finds no issues

**Security Requirements Addressed:**
- Non-functional requirement: "Only user can update their own data"
- Threat mitigated: Information Disclosure (unauthorized data access)
- Compliance: GDPR user data isolation; SOC 2 access controls

**Implementation Notes:**
```javascript
// DON'T DO THIS (insecure):
const userId = req.params.userId; // From URL; user can change it!

// DO THIS (secure):
const userId = req.user.id; // From JWT token; user cannot forge
if (req.params.userId !== userId && !req.user.isAdmin) {
  return res.status(403).json({ error: "Forbidden" });
}
```

**Estimated Effort:** 5 story points
**Owner:** Backend Engineer
**Validator:** Security Architect (code review)

---

### Task: Implement TLS/HTTPS Enforcement
**Description:** Enforce TLS 1.2+ for all communication; redirect HTTP to HTTPS
**Acceptance Criteria:**
- [ ] Config: Load balancer enforces TLS 1.2+ minimum
- [ ] Config: HTTP traffic redirected to HTTPS
- [ ] Config: HSTS header set (Strict-Transport-Security)
- [ ] Cert: Valid certificate; chains to trusted root
- [ ] Test: SSL Labs rating A or A+ (https://www.ssllabs.com/ssltest/)
- [ ] Test: HTTP request redirected or rejected
- [ ] Test: TLS 1.0/1.1 rejected
- [ ] Perf: Load test confirms <5% latency impact

**Security Requirements Addressed:**
- Non-functional requirement: "Sensitive data encrypted in transit"
- Threat mitigated: Tampering with Data; Man-in-the-Middle attack
- Compliance: GDPR data protection; SOC 2 encryption

**Estimated Effort:** 4 story points
**Owner:** DevOps Engineer
**Validator:** Security Architect (infrastructure review)

---

### Task: Implement Audit Logging
**Description:** Log all user actions to centralized logging system
**Acceptance Criteria:**
- [ ] Code: Log created for: login, data access, data modification, admin actions
- [ ] Log format: {timestamp, user_id, action, result, ip_address, user_agent}
- [ ] Sensitive data: Passwords, keys, PII tokenized or excluded (never plaintext)
- [ ] Retention: Logs retained for [90 days / 1 year] before deletion
- [ ] Immutability: Application cannot delete/modify logs (read-only access)
- [ ] Access: Only [support team / security team] can access logs
- [ ] Encryption: Logs encrypted in transit (TLS) and at rest
- [ ] Test: Action causes log entry; entry includes correct details
- [ ] Test: Attempt to delete log → fails

**Security Requirements Addressed:**
- Non-functional requirement: "All actions logged"
- Threat mitigated: Repudiation (deny performing action); Incident investigation
- Compliance: GDPR audit trail; SOC 2 logging; PCI DSS logging

**Estimated Effort:** 6 story points
**Owner:** Backend Engineer + DevOps
**Validator:** Security Architect (log review)

---

### Task: Dependency Security Audit
**Description:** Scan dependencies for vulnerabilities; create SBOM
**Acceptance Criteria:**
- [ ] Tool: SCA tool (Snyk/Dependabot) configured in CI pipeline
- [ ] SBOM: Software Bill of Materials generated and committed
- [ ] Scan: All dependencies scanned for known vulnerabilities
- [ ] High-severity: All high-severity vulns fixed or justified (why we accept risk)
- [ ] Medium-severity: Tracked in issue tracker; fix scheduled
- [ ] Low-severity: Acknowledged; fix scheduled or deferred
- [ ] CI gate: Merge blocked if high-severity vulns detected
- [ ] Update policy: Policy documented for [key dependencies]

**Security Requirements Addressed:**
- Threat mitigated: Supply chain compromise; undetected vulnerabilities
- Compliance: NIST SSDF PS-3; SBOM requirement for federal contracts

**Estimated Effort:** 3 story points
**Owner:** DevOps / Tech Lead
**Validator:** Security Architect

---

## Security Testing Tasks

### Task: Penetration Testing - Authorization Bypass
**Description:** Attempt to bypass authorization controls; confirm they work
**Test Cases:**
```
Test Case 1: Direct ID Substitution
- Request: GET /api/users/123/profile
- Attempt: Change to GET /api/users/124/profile (access different user)
- Expected: Return 403 Forbidden (not 200 or 404)
- Pass: Only authorized user can access own profile

Test Case 2: JWT Token Manipulation
- Request: GET /api/users/123/profile with valid JWT
- Attempt: Decode JWT, change user_id claim to 124, re-encode
- Expected: Invalid signature; token rejected (not accepted)
- Pass: Token cannot be forged by client

Test Case 3: Race Condition
- Request 1: User A fetches profile (user_id=123)
- Request 2: User B fetches profile (user_id=124)
- Attempt: Send both simultaneously; see if user_id check races
- Expected: Each user gets their own data (no data swap)
- Pass: Authorization check is atomic

Test Case 4: Parameter Pollution
- Request: GET /api/users/123/profile?user_id=124&user_id=123
- Attempt: Multiple user_id params; see which one is used
- Expected: Request rejected or only first param used (123)
- Pass: No bypass via parameter confusion
```

**Estimated Effort:** 4 story points
**Owner:** QA / Security Tester
**Validator:** Security Architect

---

### Task: Secure Code Review - Cryptography
**Description:** Code review focusing on cryptographic implementation
**Review Checklist:**
- [ ] Approved library used (no home-grown crypto)
- [ ] Key generation: Secure random; not seeded with predictable values
- [ ] Key storage: Keys never logged; stored in vault; access audited
- [ ] Algorithm: No deprecated algorithms (MD5, SHA1, DES); use AES-256, SHA-256+
- [ ] Password hashing: bcrypt/scrypt/Argon2 (not MD5/SHA-256/plaintext)
- [ ] Randomness: crypto.getRandomBytes(); not Math.random()
- [ ] Timing attacks: Timing-safe comparison for sensitive data
- [ ] Hardcoded secrets: None; all secrets from environment/vault

**Estimated Effort:** 4 story points
**Owner:** Security Architect
**Validator:** CTO or cryptography expert

---

## Security Review Gates

### Code Merge Gate
**Before merging security-related PR, verify:**
- [ ] Code review completed; security comments addressed
- [ ] SAST tool passed (SonarQube/Checkmarx)
- [ ] SCA tool passed (Snyk/Dependabot)
- [ ] No hardcoded secrets detected (GitGuardian)
- [ ] Unit tests for security code pass (>90% coverage)
- [ ] Pre-commit hooks passed (no secrets committed)
- [ ] All feedback from security team addressed

**Gate Owner:** Tech Lead + Security Architect

---

### Pre-Release Security Gate
**Before releasing to production, verify:**
- [ ] Threat model complete and reviewed
- [ ] All high-severity threats have mitigations
- [ ] Penetration testing completed; all high findings fixed
- [ ] SAST scan passed (no critical/high findings)
- [ ] SCA scan passed (no high-severity vulns)
- [ ] Infrastructure security review passed
- [ ] Audit logging verified operational in staging
- [ ] Secrets manager configured and validated
- [ ] Monitoring and alerting active
- [ ] Incident response plan activated
- [ ] Documentation updated with security architecture

**Gate Owner:** Security Architect + CTO

```

**Output:** Task breakdown with explicit security tasks, test scenarios, and gates

---

## Part 7: Implementation Phase - Verification Checklist

### Task: Verify Security Controls Implemented

**Use `/speckit.implement` with security verification section:**

```markdown
# Implementation Verification Checklist

## Code Security
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] All external input validated per spec
- [ ] All sensitive output encoded per spec
- [ ] Error messages don't leak system internals
- [ ] No use of deprecated cryptographic algorithms
- [ ] Cryptographic keys managed per security design
- [ ] Logging excludes sensitive data (PII tokenized)
- [ ] Race conditions prevented (atomic operations)

## Dependency Security
- [ ] Dependencies locked to specific versions
- [ ] SBOM (Software Bill of Materials) generated
- [ ] Vulnerability scan completed; no high-severity vulns
- [ ] Critical dependencies have update strategy
- [ ] License compliance verified (no GPL in proprietary)

## Authentication & Authorization
- [ ] Authentication required on all protected endpoints
- [ ] Authorization check on every data access
- [ ] Token/session management per design
- [ ] MFA available (if required)
- [ ] Rate limiting prevents brute force
- [ ] Audit logging of all access

## Encryption & Data Protection
- [ ] Data at rest encrypted per design (AES-256)
- [ ] Data in transit encrypted (TLS 1.2+)
- [ ] Encryption keys managed per design
- [ ] Key rotation scheduled (per design period)
- [ ] Secrets managed in vault (not environment variables)
- [ ] PII tokenized in logs

## Testing & Validation
- [ ] Unit tests for security-critical code (>90% coverage)
- [ ] Integration tests for authorization flow
- [ ] Security-focused code review completed
- [ ] SAST scan passes (no critical/high findings)
- [ ] SCA scan passes (no high-severity vulns)
- [ ] Threat model mitigations validated via testing

## Infrastructure & Operations
- [ ] TLS/HTTPS enforced (A+ rating on SSL Labs)
- [ ] Firewall rules configured per architecture
- [ ] Database encryption enabled
- [ ] Secrets manager configured and tested
- [ ] Centralized logging configured and operational
- [ ] Backup/recovery tested and documented
- [ ] Disaster recovery plan in place

## CI/CD Security
- [ ] Security scans in CI pipeline (SAST, SCA, container)
- [ ] Failed security scans block merge
- [ ] Artifact signing configured (if applicable)
- [ ] Access controls on deployment keys
- [ ] Deployment audit trail enabled and audited

## Compliance & Documentation
- [ ] Security controls mapped to compliance frameworks
- [ ] Threat model documented and reviewed
- [ ] Security architecture documented
- [ ] Test results documented (penetration testing, etc.)
- [ ] Change log includes security fixes
- [ ] Incident response procedure documented and ready
- [ ] Security runbooks prepared for on-call team
- [ ] Security training completed for team members

## Pre-Launch Review
- [ ] Security architect sign-off obtained
- [ ] All acceptance criteria met
- [ ] All open security findings addressed
- [ ] Monitoring and alerting active
- [ ] Incident response team briefed
- [ ] Security release notes prepared
```

---

## Part 8: Post-Launch - Operations & Maintenance

### Task: Maintain Security Posture

**Ongoing Security Operations:**

```markdown
## Post-Launch Security Checklist

### Daily
- [ ] Security alerts reviewed (monitoring dashboard)
- [ ] Failed authentication attempts reviewed for patterns
- [ ] Error logs reviewed for anomalies

### Weekly
- [ ] Vulnerability alerts reviewed (Snyk, security vendor newsletters)
- [ ] Penetration test feedback actioned
- [ ] Security incident retrospectives documented

### Monthly
- [ ] Dependency security updates reviewed and patched
- [ ] Access audit: Who has what permissions? (Least privilege review)
- [ ] Log review: Any unauthorized access attempts?
- [ ] Backup restoration test performed (can we recover from incident?)

### Quarterly
- [ ] Threat model review: New threats identified? Mitigations still valid?
- [ ] Penetration testing or security audit
- [ ] Compliance audit (SOC 2, GDPR, PCI, etc.)
- [ ] Security training refresher for team
- [ ] Incident response drill

### Annually
- [ ] Comprehensive security assessment
- [ ] External penetration testing
- [ ] SOC 2 Type II audit
- [ ] Architect review of entire security architecture
- [ ] Update threat models based on incidents from past year

### On Security Incident
- [ ] Containment: Disable access, roll back changes
- [ ] Investigation: Root cause analysis
- [ ] Notification: Customer/regulatory notification if required
- [ ] Remediation: Prevent recurrence
- [ ] Review: Update threat models, security controls, procedures
```

---

## Part 9: Quick Checklists by Role

### For Product Managers
```
Before Finalizing Spec:
- [ ] Security requirements captured (authentication, authorization, encryption, audit)
- [ ] Threat actors identified
- [ ] Compliance requirements noted (GDPR, HIPAA, PCI, etc.)
- [ ] High-risk scenarios documented
- [ ] Security architect has reviewed spec

During Development:
- [ ] Security review gates are not being bypassed
- [ ] Security bugs prioritized and fixed (don't defer to "later")
- [ ] Penetration testing scheduled before release

Before Launch:
- [ ] Threat model complete and reviewed
- [ ] All security testing completed
- [ ] Incident response plan activated
- [ ] Security monitoring dashboard active
```

### For Architects
```
Before Design Review:
- [ ] Threat model created (STRIDE analysis)
- [ ] Security architecture documented
- [ ] Controls mapped to threats
- [ ] Validation plan defined

During Architecture Review:
- [ ] Defenses in depth (multiple layers)
- [ ] Least privilege applied
- [ ] Secure defaults assumed
- [ ] Attack surface minimized

Before Implementation:
- [ ] All stakeholders understand threat model
- [ ] Implementation tasks clear
- [ ] Code review process defined
- [ ] Security test cases prepared
```

### For Developers
```
Before Coding:
- [ ] Threat model reviewed and understood
- [ ] Security architecture documented
- [ ] Secure coding guidelines obtained
- [ ] Security task acceptance criteria understood

While Coding:
- [ ] All external input validated
- [ ] Sensitive data never logged
- [ ] No hardcoded secrets
- [ ] Parameterized queries used
- [ ] Error handling is secure
- [ ] No use of deprecated algorithms

Before Code Review:
- [ ] SAST tool scanned code; no findings
- [ ] SCA tool scanned dependencies; no vulns
- [ ] Unit tests pass
- [ ] No hardcoded secrets detected

Code Review Checklist:
- [ ] Security considerations addressed
- [ ] Threat mitigations implemented
- [ ] No common vulnerabilities (OWASP Top 10)
- [ ] Crypto used correctly
- [ ] Tests are sufficient
```

### For DevOps
```
Infrastructure Design:
- [ ] Network architecture per threat model (segmentation)
- [ ] Database encryption enabled
- [ ] TLS certificates configured
- [ ] Secrets vault configured
- [ ] Logging infrastructure ready (ELK, etc.)
- [ ] Monitoring and alerting configured

Pre-Deployment:
- [ ] Security hardening applied (OS patches, kernel configs)
- [ ] Firewall rules configured per architecture
- [ ] Access controls configured (IAM)
- [ ] Backup/recovery tested
- [ ] Disaster recovery plan validated

Post-Deployment:
- [ ] Monitoring dashboard verified operational
- [ ] Alerts tested and working
- [ ] Logs flowing to central logging
- [ ] Backup jobs running and tested
- [ ] On-call runbooks prepared
```

---

## References & Templates

- See **`SECURITY_BY_DESIGN_RESEARCH.md`** for comprehensive deep-dives
- See **`SECURITY_BY_DESIGN_EXECUTIVE_SUMMARY.md`** for quick reference
- OWASP: https://owasp.org/www-project-secure-by-design-framework/
- NIST: https://csrc.nist.gov/projects/ssdf
- ISO: https://www.iso.org/standard/27001

---

**Next Steps:**
1. Adapt these templates for your organization
2. Assign security ownership (architect, code reviewers)
3. Pilot on next feature with threat modeling
4. Iterate and refine based on team feedback
5. Make security a cultural value, not a checklist

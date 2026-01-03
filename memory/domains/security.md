# Domain Extension: Security by Design (Layer 1)

**Extends**: constitution.base.md v1.0
**Regulatory Context**: OWASP, NIST SSDF, ISO 27001, SOC 2
**Typical Projects**: All software handling user data, authentication, or sensitive operations
**Philosophy**: "Security is not a feature, it's a foundation"

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Security by Design** | Embedding security considerations from the earliest stages of development |
| **Threat Model** | Structured analysis of potential threats, assets, and mitigations |
| **STRIDE** | Threat categorization: Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation |
| **DREAD** | Risk scoring: Damage, Reproducibility, Exploitability, Affected Users, Discoverability |
| **Data Classification** | Categorizing data by sensitivity level for appropriate protection |
| **Attack Surface** | All points where an attacker could try to enter or extract data |

---

## Core Principles

### SBD-001: Least Privilege

**Level**: MUST
**Statement**: Every component, user, and process MUST operate with the minimum permissions necessary to accomplish its task.

**Implementation**:
- Default to no permissions; explicitly grant only what's needed
- Time-bound elevated privileges where possible
- Separate service accounts per component
- Regular permission audits

**Validation**:
```bash
# Check for overly permissive roles
grep -r "admin\|root\|superuser" src/ --include="*.ts" --include="*.py"
```

**Violations**: HIGH - Excessive permissions enable lateral movement

---

### SBD-002: Defense in Depth

**Level**: MUST
**Statement**: Multiple independent security layers MUST protect critical assets; no single point of failure.

**Implementation**:
- Network segmentation + firewall rules
- Application-level authentication + authorization
- Database-level access controls
- Encryption at rest AND in transit
- Input validation at multiple layers

**Architecture Pattern**:
```
┌─────────────────────────────────────────────────────┐
│  WAF / DDoS Protection                              │
├─────────────────────────────────────────────────────┤
│  API Gateway (rate limiting, auth)                  │
├─────────────────────────────────────────────────────┤
│  Application (input validation, business logic)     │
├─────────────────────────────────────────────────────┤
│  Data Layer (encryption, access control)            │
└─────────────────────────────────────────────────────┘
```

**Violations**: CRITICAL - Single compromised layer exposes entire system

---

### SBD-003: Secure Defaults

**Level**: MUST
**Statement**: Systems MUST be secure out-of-the-box; insecurity requires explicit opt-in.

**Implementation**:
- HTTPS by default, HTTP requires explicit configuration
- Authentication required by default for all endpoints
- Strict Content-Security-Policy headers
- Secure cookie flags (HttpOnly, Secure, SameSite)
- Password complexity requirements enabled by default

**Anti-Patterns**:
```typescript
// BAD: Insecure default
const config = { secure: options.secure ?? false };

// GOOD: Secure default
const config = { secure: options.secure ?? true };
```

**Violations**: HIGH - Users assume default is safe

---

### SBD-004: Minimize Attack Surface

**Level**: MUST
**Statement**: Exposed functionality MUST be minimized; unused features MUST be disabled or removed.

**Implementation**:
- Disable unused HTTP methods (TRACE, OPTIONS if not needed)
- Remove debug endpoints in production
- Limit exposed ports and services
- No unnecessary dependencies
- Feature flags for sensitive operations

**Validation**:
```bash
# Check for debug endpoints
grep -r "debug\|test\|dev" src/routes/ --include="*.ts"

# Check for unused dependencies
npx depcheck
```

**Violations**: MEDIUM - Every feature is a potential entry point

---

### SBD-005: Complete Mediation

**Level**: MUST
**Statement**: Every access to every resource MUST be validated; no bypass paths.

**Implementation**:
- Centralized authorization middleware
- Validate permissions on every request (not just first)
- Check authorization at data access layer, not just API
- No direct object references without validation

**Anti-Patterns**:
```typescript
// BAD: Direct object reference
app.get('/users/:id', (req, res) => {
  return db.users.findById(req.params.id); // No auth check!
});

// GOOD: Complete mediation
app.get('/users/:id', authorize('read:users'), (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    throw new ForbiddenError();
  }
  return db.users.findById(req.params.id);
});
```

**Violations**: CRITICAL - Authorization bypass vulnerabilities

---

## OWASP Top 10 (2021) Mapping

| ID | Vulnerability | Prevention Pattern | Spec Requirement Template |
|----|---------------|-------------------|---------------------------|
| A01 | Broken Access Control | RBAC, ABAC, complete mediation | SEC-AUTHZ-xxx |
| A02 | Cryptographic Failures | TLS 1.3+, AES-256-GCM, proper key mgmt | SEC-CRYPTO-xxx |
| A03 | Injection | Parameterized queries, input validation | SEC-INPUT-xxx |
| A04 | Insecure Design | Threat modeling, secure patterns | SEC-DESIGN-xxx |
| A05 | Security Misconfiguration | Hardened defaults, automated config | SEC-CONFIG-xxx |
| A06 | Vulnerable Components | Dependency scanning, SBOM | SEC-DEPS-xxx |
| A07 | Auth Failures | MFA, secure session mgmt, rate limiting | SEC-AUTHN-xxx |
| A08 | Data Integrity Failures | Signed updates, CI/CD security | SEC-INTEG-xxx |
| A09 | Logging Failures | Security audit logs, tamper-proof | SEC-LOG-xxx |
| A10 | SSRF | URL allowlisting, network segmentation | SEC-SSRF-xxx |

### OWASP Prevention Checklist

```markdown
## A01: Broken Access Control
- [ ] Deny by default except for public resources
- [ ] Implement access control once, reuse everywhere
- [ ] Enforce record ownership (users can only access their data)
- [ ] Disable directory listing
- [ ] Log access control failures with alerting
- [ ] Rate limit API access

## A02: Cryptographic Failures
- [ ] Classify data by sensitivity
- [ ] No sensitive data in URLs or logs
- [ ] TLS 1.2+ for all transmissions
- [ ] Strong algorithms (AES-256, RSA-2048+, SHA-256+)
- [ ] Proper key management (rotation, secure storage)
- [ ] Encrypt sensitive data at rest

## A03: Injection
- [ ] Use parameterized queries / prepared statements
- [ ] Positive server-side input validation
- [ ] Escape special characters for interpreters
- [ ] Use LIMIT in queries to prevent mass disclosure
- [ ] Code review for injection points

## A04: Insecure Design
- [ ] Threat model for critical flows
- [ ] Secure design patterns in libraries
- [ ] Unit and integration tests for security
- [ ] Plausibility checks (e.g., order total matches items)
- [ ] Tiered access for different trust levels

## A05: Security Misconfiguration
- [ ] Hardened, minimal deployments
- [ ] Remove unused features and frameworks
- [ ] Review cloud storage permissions
- [ ] Automated configuration verification
- [ ] Segmented architecture

## A06: Vulnerable Components
- [ ] Inventory all dependencies (SBOM)
- [ ] Remove unused dependencies
- [ ] Continuous monitoring for vulnerabilities
- [ ] Only obtain from official sources
- [ ] Monitor unmaintained libraries

## A07: Authentication Failures
- [ ] Implement MFA where possible
- [ ] No default credentials
- [ ] Weak password checks against breach databases
- [ ] Rate limiting / account lockout
- [ ] Secure session management
- [ ] High-entropy session IDs

## A08: Data Integrity Failures
- [ ] Verify software/data from expected sources
- [ ] CI/CD pipeline security (no unauthorized changes)
- [ ] Digitally sign updates
- [ ] Review serialization for untrusted data
- [ ] SRI for client-side libraries

## A09: Logging Failures
- [ ] Log authentication, access control, input failures
- [ ] Sufficient context for forensics
- [ ] Tamper-evident log format
- [ ] Monitoring and alerting
- [ ] No sensitive data in logs

## A10: SSRF
- [ ] Sanitize and validate all URLs
- [ ] URL schema/port/destination allowlist
- [ ] Do not send raw responses to clients
- [ ] Disable HTTP redirects
- [ ] Network segmentation for URL fetching
```

---

## Data Classification

| Level | Label | Examples | Encryption | Access | Retention |
|-------|-------|----------|------------|--------|-----------|
| 1 | **Public** | Marketing content, docs | Optional | Anyone | Indefinite |
| 2 | **Internal** | Internal docs, analytics | At-rest | Employees | 3 years |
| 3 | **Confidential** | PII, financial, health | At-rest + Transit | Need-to-know | Per regulation |
| 4 | **Restricted** | Secrets, keys, passwords | HSM/Vault | Named individuals | Minimal |

### Classification Decision Tree

```
Is the data publicly available?
  → Yes: PUBLIC
  → No: Would exposure harm the company?
      → No: INTERNAL
      → Yes: Is it PII, financial, or health data?
          → No: CONFIDENTIAL
          → Yes: Is it credentials, keys, or secrets?
              → No: CONFIDENTIAL
              → Yes: RESTRICTED
```

---

## Authentication Patterns

### Pattern: Session-Based (Web Applications)

```typescript
// Server-side session with secure cookies
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 3600000 // 1 hour
  },
  resave: false,
  saveUninitialized: false
}));
```

### Pattern: JWT (APIs)

```typescript
// Short-lived access token + refresh token
const accessToken = jwt.sign(
  { sub: user.id, scope: user.permissions },
  process.env.JWT_SECRET,
  { expiresIn: '15m', algorithm: 'RS256' }
);

const refreshToken = crypto.randomBytes(64).toString('hex');
// Store refresh token hash in database with expiry
```

### Pattern: API Keys (Service-to-Service)

```typescript
// Hashed API keys with scope limitations
const apiKeyHash = crypto.createHash('sha256')
  .update(apiKey)
  .digest('hex');

// Verify: hash(provided) === stored_hash
// Check: key.scopes includes required_scope
// Check: key.expiresAt > now
```

---

## Authorization Patterns

### Pattern: RBAC (Role-Based Access Control)

```typescript
// Define roles and permissions
const ROLES = {
  viewer: ['read:products', 'read:orders:own'],
  customer: ['read:products', 'read:orders:own', 'write:orders:own'],
  admin: ['read:*', 'write:*', 'delete:*']
};

// Check permission
function hasPermission(userRole: string, required: string): boolean {
  const permissions = ROLES[userRole] || [];
  return permissions.some(p =>
    p === required || p === '*' || p.endsWith(':*') && required.startsWith(p.slice(0, -1))
  );
}
```

### Pattern: ABAC (Attribute-Based Access Control)

```typescript
// Policy-based decisions
const policy = {
  resource: 'order',
  action: 'read',
  conditions: [
    { attribute: 'user.id', operator: 'equals', value: 'resource.userId' },
    { attribute: 'user.role', operator: 'in', value: ['admin', 'support'] }
  ],
  effect: 'allow'
};
```

---

## Encryption Standards

| Use Case | Algorithm | Key Size | Notes |
|----------|-----------|----------|-------|
| Symmetric encryption | AES-256-GCM | 256-bit | Authenticated encryption |
| Password hashing | Argon2id | N/A | Memory-hard, side-channel resistant |
| Digital signatures | Ed25519 or RSA | 256-bit / 2048-bit | Prefer Ed25519 |
| TLS | TLS 1.3 | N/A | Disable TLS 1.0/1.1 |
| Key derivation | HKDF or PBKDF2 | 256-bit | For deriving keys from passwords |

---

## Summary

| Type | Count |
|------|-------|
| Core Principles (SBD-xxx) | 5 |
| OWASP Top 10 Mappings | 10 |
| Data Classification Levels | 4 |
| Auth Patterns | 3 |
| Authz Patterns | 2 |

---

## When to Use

Apply this domain extension when:
- Building software that handles user data
- Implementing authentication or authorization
- Processing financial or health information
- Exposing public APIs
- Operating in regulated industries

---

## Combining with Other Domains

| Combined With | Notes |
|---------------|-------|
| **Quality Gates** | Security gates (QG-SEC-xxx) enforce security before deployment |
| **FinTech** | Strengthen crypto requirements, add PCI DSS compliance |
| **Healthcare** | Add HIPAA-specific logging and encryption requirements |
| **Enterprise** | Add SSO/SAML patterns, compliance audit trails |

---

## Usage

```bash
# Activate security domain
cp memory/domains/security.md memory/constitution.domain.md

# Or combine with other domains
cat memory/constitution.base.md memory/domains/security.md > memory/constitution.md

# Validate against security principles
/speckit.analyze --profile security
```

---

## Related Templates

- `templates/shared/security/threat-model-template.md` - STRIDE threat modeling
- `templates/shared/security/owasp-checklist.md` - OWASP Top 10 checklist
- `templates/verify-template.yaml` - OWASP ZAP scanning configuration

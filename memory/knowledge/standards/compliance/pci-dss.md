# PCI-DSS (Payment Card Industry Data Security Standard)

> **Purpose**: Implementation checklist for PCI-DSS v4.0 compliance. Referenced during specification and planning for payment features.
>
> **Evidence Tier**: AUTHORITATIVE (official PCI Security Standards Council standard)

---

## Standard Overview

**Full Name**: Payment Card Industry Data Security Standard
**Version**: 4.0
**Published**: 2022-03-31 (v4.0), effective 2025-03-31
**Authority**: PCI Security Standards Council (PCI SSC)
**Official Document**: <https://www.pcisecuritystandards.org/document_library/>
**Applicability**: Any organization that stores, processes, or transmits cardholder data

---

## Key Requirements

### Requirement 3.2: Do not store sensitive authentication data after authorization

**Severity**: CRITICAL
**Evidence**: PCI-DSS v4.0, Section 3.2 [AUTHORITATIVE]

#### Description

Sensitive authentication data (SAD) must NEVER be stored after authorization, even if encrypted. This includes full track data, CVV2/CVC2/CID, and PINs.

#### Implementation Guidance

1. **Code Review**: Scan codebase for prohibited data patterns
2. **Database Schema**: Ensure NO columns for CVV, full track, PIN
3. **Log Sanitization**: Strip sensitive data from logs
4. **Memory Management**: Clear sensitive data from RAM after use

**Prohibited Data**:
- Full track data (magnetic stripe, chip data)
- CVV2, CVC2, CID (card verification codes)
- PIN, PIN block, PIN data

**Permitted Data** (if encrypted per Req 3.4):
- PAN (Primary Account Number)
- Cardholder name
- Expiration date
- Service code

#### Verification

- Code review: `grep -ri "cvv\|cvc\|pin" src/` should return no storage patterns
- Schema audit: No columns named `cvv`, `cvc`, `pin`, `track_data`
- Log analysis: Ensure logs don't contain prohibited patterns
- Memory dump analysis: No sensitive data in core dumps

#### Auto-NFR Generation

```markdown
NFR-SEC-PCI-001: Do not store CVV/CVC [CRITICAL]
- Acceptance: No CVV/CVC/CID fields in database schema or logs
- Evidence: PCI-DSS v4.0 Req 3.2 [AUTHORITATIVE]
- Verification: Schema review + log analysis + code scan
- Traceability: → FR-XXX (Payment processing)

NFR-SEC-PCI-002: Do not store full track data [CRITICAL]
- Acceptance: No magnetic stripe or chip data persisted after authorization
- Evidence: PCI-DSS v4.0 Req 3.2 [AUTHORITATIVE]
- Verification: Database audit + code review
- Traceability: → FR-XXX (Payment processing)
```

#### Common Pitfalls

- ❌ **Logging card data**: Accidentally logging CVV in error messages
- ❌ **Temporary storage**: Storing CVV "temporarily" in session or cache
- ❌ **Third-party SDKs**: SDK stores prohibited data without developer knowledge

#### Related Requirements

- Req 3.4: Encrypt PAN at rest
- Req 4.2: Encrypt PAN in transit (TLS 1.2+)

---

### Requirement 3.4: Render PAN unreadable anywhere it is stored

**Severity**: CRITICAL
**Evidence**: PCI-DSS v4.0, Section 3.4 [AUTHORITATIVE]

#### Description

Primary Account Number (PAN) must be rendered unreadable using one of the following: encryption, truncation, tokenization, or hashing (with index tables).

#### Implementation Guidance

**Option A: Encryption**
- Algorithm: AES-256 (minimum)
- Key management: Separate from data (HSM or key management service)
- Key rotation: Every 90 days or per cryptoperiod policy

```python
# Example: Encrypt PAN before storage
from cryptography.fernet import Fernet

key = load_encryption_key_from_hsm()
cipher = Fernet(key)
encrypted_pan = cipher.encrypt(pan.encode())
db.save(encrypted_pan)
```

**Option B: Tokenization**
- Replace PAN with surrogate value (token)
- Maintain mapping in secure token vault
- Tokens are non-reversible without vault access

**Option C: Truncation**
- Display only last 4 digits
- CANNOT use for authorization (requires full PAN)
- Suitable for receipts, statements, customer service

**Option D: Hashing with Index**
- One-way hash function (SHA-256+)
- Index table to search (meets PCI requirements)
- Cannot reverse hash to recover PAN

#### Verification

- Encryption audit: Verify algorithm (AES-256), key strength (256-bit)
- Key management: Keys stored separately from encrypted data
- Display masking: UI shows only last 4 digits (`****1234`)
- Database inspection: No plaintext PANs in any table

#### Auto-NFR Generation

```markdown
NFR-SEC-PCI-003: Encrypt PAN at rest (AES-256) [CRITICAL]
- Acceptance: All stored PANs encrypted with AES-256 or stronger
- Evidence: PCI-DSS v4.0 Req 3.4 [AUTHORITATIVE]
- Verification: Database audit + encryption validation
- Traceability: → FR-XXX (Payment data storage)

NFR-SEC-PCI-004: Mask PAN when displayed [HIGH]
- Acceptance: UI displays only last 4 digits of PAN
- Evidence: PCI-DSS v4.0 Req 3.4 [AUTHORITATIVE]
- Verification: UI testing + screenshot review
- Traceability: → FR-XXX (Payment UI)
```

#### Common Pitfalls

- ❌ **Weak encryption**: Using DES or 3DES (deprecated)
- ❌ **Hardcoded keys**: Embedding encryption keys in source code
- ❌ **Insufficient masking**: Showing first 6 + last 4 (BIN + last 4) violates PCI

#### Related Requirements

- Req 3.2: Do not store SAD
- Req 3.5: Key management procedures
- Req 8.2: MFA for administrative access to CDE

---

### Requirement 4.2: Encrypt transmission of cardholder data across open, public networks

**Severity**: CRITICAL
**Evidence**: PCI-DSS v4.0, Section 4.2 [AUTHORITATIVE]

#### Description

PAN must be encrypted during transmission using strong cryptography (TLS 1.2+, IPSEC). HTTP, FTP, Telnet are prohibited for cardholder data.

#### Implementation Guidance

1. **TLS Configuration**:
   - Minimum version: TLS 1.2 (TLS 1.3 recommended)
   - Cipher suites: Only strong ciphers (ECDHE, AES-GCM)
   - Certificate validation: Proper hostname verification

2. **API Security**:
   - HTTPS endpoints only
   - Certificate pinning for mobile apps
   - Mutual TLS for server-to-server

```yaml
# Nginx TLS Configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256';
ssl_prefer_server_ciphers on;
```

#### Verification

- SSL Labs scan: A+ rating required
- Certificate validation: Valid, not expired, proper SAN
- Protocol test: TLS 1.0/1.1 disabled, only 1.2+ accepted
- Cipher suite audit: No weak ciphers (DES, RC4, MD5)

#### Auto-NFR Generation

```markdown
NFR-SEC-PCI-005: TLS 1.2+ for card data transmission [CRITICAL]
- Acceptance: All cardholder data transmitted via TLS 1.2 or higher
- Evidence: PCI-DSS v4.0 Req 4.2 [AUTHORITATIVE]
- Verification: SSL Labs scan + certificate validation
- Traceability: → FR-XXX (Payment API)

NFR-SEC-PCI-006: Strong cipher suites only [HIGH]
- Acceptance: Only PCI-approved cipher suites enabled
- Evidence: PCI-DSS v4.0 Req 4.2 [AUTHORITATIVE]
- Verification: Cipher suite audit
- Traceability: → FR-XXX (TLS configuration)
```

#### Common Pitfalls

- ❌ **Weak protocols**: Supporting TLS 1.0/1.1 (deprecated)
- ❌ **Self-signed certs**: Using self-signed certificates in production
- ❌ **Mixed content**: Loading payment page assets over HTTP

#### Related Requirements

- Req 2.2: Secure system configurations
- Req 6.2: Patch management for TLS vulnerabilities

---

### Requirement 6.5.10: Validate input to prevent injection attacks

**Severity**: HIGH
**Evidence**: PCI-DSS v4.0, Section 6.5.10 [AUTHORITATIVE]

#### Description

Applications must validate all input to prevent injection attacks (SQL injection, XSS, command injection, LDAP injection).

#### Implementation Guidance

1. **Input Validation**:
   - Whitelist acceptable characters/patterns
   - Reject unexpected input formats
   - Validate length, type, format

2. **Parameterized Queries**:
   - Use prepared statements (NOT string concatenation)
   - Bind variables for all user input

```python
# GOOD: Parameterized query
cursor.execute("SELECT * FROM payments WHERE user_id = ?", (user_id,))

# BAD: String concatenation (SQL injection risk)
cursor.execute(f"SELECT * FROM payments WHERE user_id = {user_id}")
```

3. **Output Encoding**:
   - HTML-encode user input before display
   - Use framework-provided escaping functions

#### Verification

- Static analysis: SAST tools scan for injection vulnerabilities
- Dynamic testing: DAST/penetration testing with payloads
- Code review: Verify all user inputs validated/parameterized

#### Auto-NFR Generation

```markdown
NFR-SEC-PCI-007: Prevent SQL injection [HIGH]
- Acceptance: All database queries use parameterized statements
- Evidence: PCI-DSS v4.0 Req 6.5.10 [AUTHORITATIVE]
- Verification: Code review + SAST scan (Bandit, SonarQube)
- Traceability: → FR-XXX (Payment queries)

NFR-SEC-PCI-008: Prevent XSS attacks [HIGH]
- Acceptance: All user input HTML-encoded before display
- Evidence: PCI-DSS v4.0 Req 6.5.10 [AUTHORITATIVE]
- Verification: DAST scan + manual testing
- Traceability: → FR-XXX (Payment UI)
```

#### Common Pitfalls

- ❌ **Trusting client-side validation**: Server must re-validate all input
- ❌ **Incomplete sanitization**: Blacklisting instead of whitelisting
- ❌ **ORM misuse**: Assuming ORM automatically prevents injection

#### Related Requirements

- Req 6.2: Secure coding practices
- Req 11.3: Penetration testing

---

## Compliance Triggers

### Keyword Detection

Auto-generate compliance NFRs when specification contains:

| Keyword/Pattern | Triggered Requirement | Auto-NFR |
|-----------------|------------------------|----------|
| "store credit card" | PCI-DSS Req 3.4 | NFR-SEC-PCI-003 (encrypt) |
| "store card" | PCI-DSS Req 3.4 | NFR-SEC-PCI-003 (encrypt) |
| "display card number" | PCI-DSS Req 3.4 | NFR-SEC-PCI-004 (mask) |
| "process payment" | PCI-DSS Req 4.2, 6.5.10 | NFR-SEC-PCI-005, 007 |
| "transmit card data" | PCI-DSS Req 4.2 | NFR-SEC-PCI-005 (TLS) |
| "payment API" | PCI-DSS Req 4.2, 6.5.10 | NFR-SEC-PCI-005, 007 |
| "CVV" | PCI-DSS Req 3.2 | NFR-SEC-PCI-001 (NEVER store) |
| "card verification" | PCI-DSS Req 3.2 | NFR-SEC-PCI-001 (NEVER store) |

---

## Implementation Checklist

### Requirement 3: Protect Stored Cardholder Data

- [ ] **3.2**: Do not store sensitive authentication data (CVV, track, PIN)
  - Mapped to: NFR-SEC-PCI-001, NFR-SEC-PCI-002
  - Verification: Schema audit + code review

- [ ] **3.4**: Render PAN unreadable (encryption/tokenization/truncation)
  - Mapped to: NFR-SEC-PCI-003, NFR-SEC-PCI-004
  - Verification: Encryption audit + display masking test

### Requirement 4: Encrypt Transmission

- [ ] **4.2**: Encrypt cardholder data in transit (TLS 1.2+)
  - Mapped to: NFR-SEC-PCI-005, NFR-SEC-PCI-006
  - Verification: SSL Labs scan + cipher audit

### Requirement 6: Develop Secure Systems

- [ ] **6.5.10**: Validate input to prevent injection attacks
  - Mapped to: NFR-SEC-PCI-007, NFR-SEC-PCI-008
  - Verification: SAST/DAST scan + penetration test

---

## Verification Matrix

| Requirement | Implementation | Verification Method | Status | Evidence |
|-------------|----------------|---------------------|:------:|----------|
| 3.2 (No SAD) | No CVV/track columns | Schema audit + code scan | ⚠️ | Pending schema review |
| 3.4 (Encrypt PAN) | AES-256 encryption | Encryption validation | ⚠️ | Pending implementation |
| 4.2 (TLS) | TLS 1.2+ enforced | SSL Labs scan | ⚠️ | Pending scan |
| 6.5.10 (Injection) | Parameterized queries | SAST + DAST | ⚠️ | Pending testing |

**Legend**:
- ✅ Compliant
- ⚠️ Partial / Needs Review
- ❌ Non-compliant

---

## Penalty & Risk

**Non-compliance penalties**:
- **Card brand fines**: $5,000 - $100,000 per month until compliant
- **Increased transaction fees**: +0.5% to 2% per transaction
- **Loss of card processing privileges**: Account termination

**Risk exposure**:
- **Legal**: Class action lawsuits, regulatory investigations
- **Financial**: Breach costs average $4.24M (IBM 2023), card reissuance costs
- **Reputational**: Loss of customer trust, negative press coverage

---

## Maintenance

**Last Updated**: 2025-01-10
**Reviewed By**: standards-researcher-ai
**Standard Version**: PCI-DSS v4.0 (effective 2025-03-31)
**Review Frequency**: Annual (PCI-DSS updates published annually)
**Evidence Tier**: AUTHORITATIVE
**Source**: <https://www.pcisecuritystandards.org/document_library/>

# Domain Extension: Healthcare / HIPAA (Layer 1)

**Extends**: constitution.base.md v1.0
**Regulatory Context**: HIPAA, HITECH, FDA (for medical devices)
**Typical Projects**: EHR systems, patient portals, telehealth, medical devices

---

## Key Concepts

- **PHI** (Protected Health Information): Any health data that can identify a patient
- **Covered Entity**: Healthcare providers, health plans, healthcare clearinghouses
- **Business Associate**: Third parties handling PHI on behalf of covered entities
- **Minimum Necessary**: Access only the PHI needed for the specific purpose

---

## Strengthened Principles

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| CMP-003 | SHOULD | MUST | PHI protection is legally mandated |
| SEC-005 | MUST | MUST (with MFA) | Healthcare requires strong authentication |
| SEC-006 | SHOULD | MUST | Minimum necessary access is HIPAA requirement |
| CMP-001 | MUST | MUST (6 years) | HIPAA requires 6-year audit retention |
| OBS-001 | MUST | MUST (with PHI masking) | Logs must not contain PHI |

---

## Additional Principles

### HIP-001: PHI Encryption

**Level**: MUST
**Applies to**: All PHI data

PHI MUST be encrypted at rest (AES-256 or equivalent) and in transit (TLS 1.2+). Encryption keys MUST be managed separately from data.

**Validation**: Review encryption configuration
**Violations**: CRITICAL - HIPAA violation

---

### HIP-002: PHI Access Logging

**Level**: MUST
**Applies to**: All PHI access

All access to PHI MUST be logged with:
- User identity
- Patient identifier (hashed or tokenized in logs)
- Access timestamp
- Purpose/context
- Data accessed

Logs MUST be retained for 6 years minimum.

**Validation**: Review PHI access logging
**Violations**: CRITICAL - HIPAA audit failure

---

### HIP-003: Minimum Necessary

**Level**: MUST
**Applies to**: All PHI disclosure and access

Access to PHI MUST follow minimum necessary principle:
- Role-based access with granular permissions
- Purpose limitation for each access
- No "god mode" access to all patient data

**Validation**: Review access control model
**Violations**: CRITICAL - HIPAA violation

---

### HIP-004: Patient Rights

**Level**: MUST
**Applies to**: Patient-facing systems

Systems MUST support patient rights:
- Access to own records
- Request for amendment
- Accounting of disclosures
- Authorization management

**Validation**: Verify patient rights features
**Violations**: HIGH - HIPAA patient rights violation

---

### HIP-005: Breach Notification

**Level**: MUST
**Applies to**: Systems handling PHI

Systems MUST have breach detection and notification capability:
- Anomaly detection for unusual access patterns
- Breach assessment workflow
- Notification templates (60-day HHS requirement)

**Validation**: Review breach response procedures
**Violations**: CRITICAL - Breach notification failure

---

### HIP-006: BAA Tracking

**Level**: SHOULD
**Applies to**: Third-party integrations

All third-party services handling PHI SHOULD be tracked with Business Associate Agreement status.

**Validation**: Review vendor BAA registry
**Violations**: MEDIUM - Compliance risk

---

## PHI Data Classification

| Category | Examples | Handling |
|----------|----------|----------|
| Direct Identifiers | Name, SSN, MRN | Always encrypt, strict access |
| Indirect Identifiers | DOB, ZIP, dates | Encrypt, de-identify when possible |
| Clinical Data | Diagnoses, medications | Encrypt, role-based access |
| Administrative | Appointments, billing codes | Encrypt, broader access allowed |

---

## Summary

| Type | Count |
|------|-------|
| Strengthened from base | 5 |
| New MUST principles | 5 |
| New SHOULD principles | 1 |
| **Total additional requirements** | **11** |

---

## Usage

```bash
cp memory/domains/healthcare.md memory/constitution.domain.md
```

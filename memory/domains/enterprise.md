# Domain Extension: Enterprise (Layer 1)

**Extends**: constitution.base.md v1.1
**Regulatory Context**: SOC 2, ISO 27001, GDPR, enterprise security policies
**Typical Projects**: Enterprise SaaS, B2B platforms, regulated industries, mission-critical systems
**Philosophy**: "Compliance is a feature, not an afterthought"

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Compliance Framework** | Set of regulatory requirements (GDPR, SOC2, HIPAA, PCI-DSS) |
| **Approval Matrix** | Authority assignment for different decision types |
| **Technology Radar** | Categorization of technologies by adoption status |
| **SLA Targets** | Service level objectives for availability, recovery |
| **Security Baseline** | Minimum security controls required |
| **Data Classification** | Categorization of data sensitivity (Public, Internal, Confidential, Restricted) |

---

## Strengthened Principles

These principles from `constitution.base.md` are elevated or enhanced for enterprise:

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| SEC-001 | MUST | MUST (with rotation) | Secrets rotation mandatory for compliance |
| SEC-002 | MUST | MUST (with MFA) | Multi-factor auth for privileged access |
| OBS-001 | MUST | MUST (with retention) | Audit logs retained per compliance requirements |
| OBS-002 | MUST | MUST (with context) | Error tracking includes PII handling rules |
| CMP-001 | MUST | MUST (with immutability) | Audit trail cannot be modified |
| DOC-001 | SHOULD | MUST | All APIs documented for compliance audits |

---

## Additional Principles

### ENT-001: Compliance-Driven Design

**Level**: MUST
**Applies to**: All system architecture

Systems MUST be designed with compliance requirements from day one. Data classification, retention policies, and audit trails MUST be part of initial design.

**Implementation**:
- Document compliance requirements in spec.md
- Include data classification in entity definitions
- Define retention policies per data type
- Plan audit trail from architecture phase

**Validation**: Compliance requirements documented in spec.md
**Violations**: CRITICAL - Costly retrofitting required

---

### ENT-002: Approval Workflow Enforcement

**Level**: MUST
**Applies to**: Breaking changes, security exceptions

Changes requiring approval per Approval Matrix MUST go through formal approval workflow. Approvals MUST be recorded with timestamp and approver identity.

**Implementation**:
- Define approval matrix in constitution.md
- Integrate approval gates in CI/CD pipeline
- Maintain audit log of all approvals
- Require approval evidence for compliance audits

**Validation**: Review approval records in change management system
**Violations**: HIGH - Unauthorized changes

---

### ENT-003: Technology Governance

**Level**: SHOULD
**Applies to**: New technology adoption

New technologies MUST be assessed against Technology Radar before adoption. "Hold" technologies MUST NOT be introduced without exception approval.

**Implementation**:
- Maintain Technology Radar in constitution.md
- Review radar quarterly
- Require radar assessment for new dependencies
- Document migration paths for "Hold" technologies

**Validation**: Review dependency additions against radar
**Violations**: MEDIUM - Technical debt accumulation

---

### ENT-004: SLA Monitoring

**Level**: MUST
**Applies to**: Production services

All SLA metrics MUST be monitored continuously. Breaches MUST trigger automated escalation per defined procedures.

**Implementation**:
- Define SLA targets in constitution.md
- Configure alerting thresholds per metric
- Automate escalation based on breach duration
- Generate SLA reports for stakeholders

**Validation**: Verify SLA dashboards and alerting
**Violations**: HIGH - Undetected service degradation

---

### ENT-005: Data Classification

**Level**: MUST
**Applies to**: All data handling

All data MUST be classified (Public, Internal, Confidential, Restricted). Handling procedures MUST match classification level.

**Classification Levels**:
| Level | Definition | Handling |
|-------|------------|----------|
| **Public** | No impact if disclosed | No restrictions |
| **Internal** | Minor impact if disclosed | Access control |
| **Confidential** | Significant impact if disclosed | Encryption + access control |
| **Restricted** | Severe impact if disclosed | Encryption + MFA + audit logging |

**Validation**: Review data flow diagrams with classification labels
**Violations**: CRITICAL - Data breach risk

---

### ENT-006: Vendor Risk Assessment

**Level**: SHOULD
**Applies to**: Third-party integrations

External vendors and services SHOULD undergo security assessment before integration. Vendor compliance certifications SHOULD be verified.

**Assessment Criteria**:
- SOC 2 Type II certification
- Data processing agreement (DPA)
- Subprocessor list
- Incident notification SLA
- Data residency compliance

**Validation**: Review vendor assessment records
**Violations**: MEDIUM - Supply chain risk

---

## Compliance Framework Integration

### Framework-Specific Requirements

| Framework | Key Requirements | ENT Principles |
|-----------|------------------|----------------|
| **GDPR** | DPA, DPIA, data subject rights, 72h breach notification | ENT-005, ENT-006 |
| **SOC 2** | Security, availability, processing integrity, confidentiality, privacy | ENT-001, ENT-004 |
| **HIPAA** | PHI protection, audit controls, access management | ENT-005, ENT-002 |
| **PCI-DSS** | Cardholder data protection, network security, access control | ENT-001, ENT-005 |
| **ISO 27001** | ISMS, risk assessment, security controls | ENT-001, ENT-003 |

---

## Summary

| Type | Count |
|------|-------|
| Strengthened from base | 6 |
| New MUST principles | 4 |
| New SHOULD principles | 2 |
| **Total additional requirements** | **12** |

---

## When to Use

Apply this domain extension when:
- Building enterprise SaaS or B2B platforms
- Operating in regulated industries
- Targeting enterprise customers requiring compliance
- Managing mission-critical systems with SLA requirements
- Needing formal approval workflows and governance

---

## Combining with Other Domains

| Combined With | Notes |
|---------------|-------|
| **Production** | Full enterprise + production observability stack |
| **FinTech** | Add FIN-* principles for financial regulations (PCI-DSS, SOX) |
| **Healthcare** | Add HIPAA-specific PHI handling requirements |
| **SaaS** | Multi-tenant enterprise SaaS with tenant isolation |

---

## Usage

To apply enterprise domain:

```bash
cp memory/domains/enterprise.md memory/constitution.domain.md
```

Or combine with other domains:

```bash
cat memory/domains/enterprise.md memory/domains/production.md > memory/constitution.domain.md
```

Then customize `memory/constitution.md` for project-specific overrides.

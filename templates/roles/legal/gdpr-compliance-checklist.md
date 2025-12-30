# GDPR Compliance Checklist

## Purpose

Comprehensive checklist for General Data Protection Regulation (GDPR) compliance. Covers technical, organizational, and documentation requirements for handling EU/EEA personal data.

> **Disclaimer**: This checklist is a starting point for compliance, not legal advice. GDPR requirements depend on your specific data processing activities. Consult a qualified data protection professional.

---

## GDPR Compliance Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    GDPR Compliance Areas                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LAWFULNESS ───────▶ Legal basis for processing                 │
│  TRANSPARENCY ─────▶ Privacy notices, communication             │
│  DATA SUBJECT ─────▶ Rights management                          │
│  SECURITY ─────────▶ Technical measures                         │
│  ACCOUNTABILITY ───▶ Documentation, governance                  │
│  THIRD PARTIES ────▶ Vendors, transfers                         │
│  BREACH RESPONSE ──▶ Incident handling                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Assessment

### Does GDPR Apply to You?

```yaml
gdpr_applies_if:
  any_true:
    - "You are established in the EU/EEA"
    - "You offer goods/services to EU/EEA residents"
    - "You monitor behavior of EU/EEA residents"
    - "You process personal data of EU/EEA residents"

personal_data_includes:
  - "Names and contact information"
  - "Email addresses"
  - "IP addresses"
  - "Cookie identifiers"
  - "Location data"
  - "Any data that can identify a person"
```

---

## 1. Lawful Basis for Processing

### 1.1 Identify Legal Basis

```yaml
lawful_basis_checklist:
  for_each_processing_activity:
    - [ ] Identified specific lawful basis
    - [ ] Documented in Records of Processing
    - [ ] Can demonstrate compliance if challenged

  lawful_bases:
    consent:
      when: "User freely gives specific, informed consent"
      requirements:
        - [ ] Clear opt-in (no pre-ticked boxes)
        - [ ] Easy to withdraw as to give
        - [ ] Separate consent for different purposes
        - [ ] Records of consent maintained

    contract:
      when: "Processing necessary to fulfill a contract"
      requirements:
        - [ ] Processing directly required for contract
        - [ ] Cannot be performed without the data
        - [ ] Clearly documented in contract terms

    legitimate_interest:
      when: "Necessary for legitimate business purposes"
      requirements:
        - [ ] Legitimate Interest Assessment (LIA) completed
        - [ ] Balanced against data subject rights
        - [ ] Processing is necessary, not just useful
        - [ ] Data subjects can reasonably expect it

    legal_obligation:
      when: "Required by law"
      requirements:
        - [ ] Specific legal requirement identified
        - [ ] Limited to what law requires

    vital_interests:
      when: "Protecting someone's life"
      requirements:
        - [ ] Life-threatening situation
        - [ ] No other lawful basis available

    public_task:
      when: "Public authority functions"
      requirements:
        - [ ] Official authority or public interest task
```

### 1.2 Special Category Data

```yaml
special_category_data:
  types:
    - "Racial or ethnic origin"
    - "Political opinions"
    - "Religious or philosophical beliefs"
    - "Trade union membership"
    - "Genetic data"
    - "Biometric data (for identification)"
    - "Health data"
    - "Sex life or sexual orientation"

  checklist:
    - [ ] Identified all special category data processed
    - [ ] Identified additional lawful basis (Article 9)
    - [ ] Implemented enhanced security measures
    - [ ] Documented necessity of processing
```

---

## 2. Transparency & Privacy Notices

### 2.1 Privacy Notice Requirements

```yaml
privacy_notice_checklist:
  content_requirements:
    - [ ] Controller identity and contact details
    - [ ] DPO contact details (if applicable)
    - [ ] Purposes of processing
    - [ ] Lawful basis for each purpose
    - [ ] Categories of personal data
    - [ ] Recipients or categories of recipients
    - [ ] International transfer information
    - [ ] Retention periods
    - [ ] Data subject rights
    - [ ] Right to withdraw consent
    - [ ] Right to lodge complaint with supervisory authority
    - [ ] Source of data (if not collected directly)
    - [ ] Automated decision-making information

  accessibility:
    - [ ] Written in clear, plain language
    - [ ] Easily accessible from all collection points
    - [ ] Available in relevant languages
    - [ ] Updated when processing changes
```

### 2.2 Collection Point Notices

```yaml
collection_points:
  website_forms:
    - [ ] Link to privacy notice
    - [ ] Purpose statement at collection
    - [ ] Consent checkboxes where required

  mobile_apps:
    - [ ] Privacy notice accessible in app
    - [ ] Just-in-time notices for permissions

  offline_collection:
    - [ ] Privacy notice provided at collection
    - [ ] Verbal notices where appropriate

  third_party_data:
    - [ ] Notify within 1 month of receipt
    - [ ] Or at first communication
```

---

## 3. Data Subject Rights

### 3.1 Rights Implementation

```yaml
data_subject_rights:
  right_to_access:
    requirements:
      - [ ] Can provide copy of all personal data
      - [ ] Include processing information
      - [ ] Response within 1 month
      - [ ] Free of charge (first request)
    implementation:
      - [ ] Self-service data export available
      - [ ] Manual process documented
      - [ ] Identity verification process

  right_to_rectification:
    requirements:
      - [ ] Can correct inaccurate data
      - [ ] Can complete incomplete data
      - [ ] Response within 1 month
    implementation:
      - [ ] Self-service profile editing
      - [ ] Support request process

  right_to_erasure:
    requirements:
      - [ ] Can delete data when:
        - Consent withdrawn
        - No longer necessary
        - Unlawful processing
        - Legal requirement
      - [ ] Response within 1 month
    implementation:
      - [ ] Account deletion process
      - [ ] Data retention exceptions documented
      - [ ] Propagation to third parties

  right_to_restrict:
    requirements:
      - [ ] Can restrict processing during disputes
      - [ ] Mark data as restricted
      - [ ] Stop processing (except storage)
    implementation:
      - [ ] Account suspension capability
      - [ ] Restricted flag in database

  right_to_portability:
    requirements:
      - [ ] Provide data in structured, common format
      - [ ] Machine-readable (JSON, CSV)
      - [ ] Only data provided by subject
    implementation:
      - [ ] Data export in standard format
      - [ ] API for data transfer (optional)

  right_to_object:
    requirements:
      - [ ] Stop processing for:
        - Direct marketing (absolute)
        - Legitimate interests (unless compelling grounds)
      - [ ] Inform at first communication
    implementation:
      - [ ] Unsubscribe from marketing
      - [ ] Objection handling process
```

### 3.2 Rights Request Process

```yaml
rights_request_process:
  intake:
    - [ ] Clear request submission method
    - [ ] Identity verification procedure
    - [ ] Request logging system

  processing:
    - [ ] Acknowledge within [X] days
    - [ ] Complete within 1 month
    - [ ] Extension process (up to 2 additional months)
    - [ ] Fee policy for excessive requests

  response:
    - [ ] Template responses prepared
    - [ ] Secure delivery method
    - [ ] Record of completion
```

---

## 4. Security Measures

### 4.1 Technical Security

```yaml
technical_security:
  encryption:
    - [ ] Data encrypted in transit (TLS 1.2+)
    - [ ] Data encrypted at rest
    - [ ] Encryption key management

  access_control:
    - [ ] Role-based access control (RBAC)
    - [ ] Principle of least privilege
    - [ ] Regular access reviews
    - [ ] Privileged access management

  authentication:
    - [ ] Strong password requirements
    - [ ] Multi-factor authentication (MFA)
    - [ ] Session management
    - [ ] Account lockout policies

  infrastructure:
    - [ ] Firewalls and network segmentation
    - [ ] Intrusion detection/prevention
    - [ ] Regular security patching
    - [ ] Vulnerability scanning

  application:
    - [ ] Secure development practices
    - [ ] Input validation
    - [ ] Output encoding
    - [ ] Security testing (SAST/DAST)

  logging:
    - [ ] Security event logging
    - [ ] Log integrity protection
    - [ ] Log retention (appropriate period)
    - [ ] Log monitoring
```

### 4.2 Organizational Security

```yaml
organizational_security:
  policies:
    - [ ] Information security policy
    - [ ] Acceptable use policy
    - [ ] Data handling procedures
    - [ ] Incident response plan

  personnel:
    - [ ] Background checks (where appropriate)
    - [ ] Confidentiality agreements
    - [ ] Security awareness training
    - [ ] Regular training refreshers

  physical:
    - [ ] Office access controls
    - [ ] Secure disposal of documents
    - [ ] Clean desk policy
    - [ ] Visitor management
```

---

## 5. Accountability & Governance

### 5.1 Data Protection Officer (DPO)

```yaml
dpo_requirements:
  mandatory_when:
    - "Public authority or body"
    - "Core activities require regular, systematic monitoring at scale"
    - "Core activities involve special category data at scale"

  checklist:
    - [ ] DPO appointment assessed
    - [ ] DPO contact published
    - [ ] DPO registered with supervisory authority
    - [ ] DPO has adequate resources
    - [ ] DPO reports to highest management level
    - [ ] DPO independence ensured
```

### 5.2 Records of Processing Activities (ROPA)

```yaml
ropa_checklist:
  required_when:
    - "250+ employees, OR"
    - "Processing likely to result in risk to rights and freedoms, OR"
    - "Processing is not occasional, OR"
    - "Processing includes special categories or criminal data"

  content:
    - [ ] Name and contact details of controller
    - [ ] Purposes of processing
    - [ ] Categories of data subjects
    - [ ] Categories of personal data
    - [ ] Categories of recipients
    - [ ] International transfers
    - [ ] Retention periods
    - [ ] Security measures description

  maintenance:
    - [ ] Updated when processing changes
    - [ ] Version controlled
    - [ ] Available for supervisory authority
```

### 5.3 Data Protection Impact Assessment (DPIA)

```yaml
dpia_requirements:
  required_when:
    - "Systematic and extensive profiling with significant effects"
    - "Large-scale processing of special categories"
    - "Systematic monitoring of public areas"
    - "New technologies with potential high risk"

  checklist:
    - [ ] DPIA threshold assessment for new processing
    - [ ] DPIA template available
    - [ ] DPO consulted in DPIA process
    - [ ] Risks identified and assessed
    - [ ] Mitigation measures documented
    - [ ] Supervisory authority consulted if high risk remains
```

---

## 6. Third Parties & International Transfers

### 6.1 Vendor Management

```yaml
vendor_checklist:
  before_engagement:
    - [ ] Due diligence on data protection practices
    - [ ] Security assessment
    - [ ] Sub-processor identification

  contracts:
    - [ ] Data Processing Agreement (DPA) signed
    - [ ] Article 28 requirements included
    - [ ] Security obligations specified
    - [ ] Sub-processor approval process
    - [ ] Audit rights included
    - [ ] Breach notification obligations
    - [ ] Data deletion on termination

  ongoing:
    - [ ] Regular compliance reviews
    - [ ] Sub-processor monitoring
    - [ ] Security assessment updates
```

### 6.2 International Transfers

```yaml
international_transfers:
  assessment:
    - [ ] Identified all transfers outside EU/EEA
    - [ ] Mapped data flows to third countries
    - [ ] Documented recipients in third countries

  mechanisms:
    adequacy_decision:
      countries: ["UK", "Switzerland", "Japan", "etc."]
      check: "No additional safeguards needed"

    standard_contractual_clauses:
      - [ ] Correct module selected
      - [ ] Annexes completed
      - [ ] Transfer Impact Assessment done
      - [ ] Supplementary measures if needed

    binding_corporate_rules:
      - [ ] Approved by supervisory authority
      - [ ] Binding on all group members

    derogations:
      - "Explicit consent (limited use)"
      - "Contract necessity"
      - "Legal claims"

  supplementary_measures:
    - [ ] Encryption with EU-held keys
    - [ ] Pseudonymization
    - [ ] Split processing
```

---

## 7. Data Breach Response

### 7.1 Breach Preparation

```yaml
breach_preparation:
  policies:
    - [ ] Breach detection procedures
    - [ ] Breach response plan
    - [ ] Roles and responsibilities defined
    - [ ] Communication templates prepared

  training:
    - [ ] Staff trained on breach recognition
    - [ ] Escalation procedures known
    - [ ] Regular breach drills

  detection:
    - [ ] Security monitoring in place
    - [ ] Anomaly detection
    - [ ] User reporting mechanism
```

### 7.2 Breach Response Checklist

```yaml
breach_response:
  immediate:
    - [ ] Contain the breach
    - [ ] Assess scope and impact
    - [ ] Document everything
    - [ ] Preserve evidence

  assessment:
    - [ ] What data was affected?
    - [ ] How many individuals affected?
    - [ ] What is the risk to individuals?
    - [ ] Is notification required?

  supervisory_authority:
    deadline: "72 hours from becoming aware"
    required_when: "Risk to rights and freedoms"
    notification_content:
      - [ ] Nature of breach
      - [ ] Categories and numbers affected
      - [ ] DPO contact details
      - [ ] Likely consequences
      - [ ] Measures taken or proposed

  individuals:
    required_when: "High risk to rights and freedoms"
    notification_content:
      - [ ] Clear description of breach
      - [ ] DPO contact details
      - [ ] Likely consequences
      - [ ] Measures taken
      - [ ] Advice for protection

  documentation:
    - [ ] Breach register updated
    - [ ] Timeline documented
    - [ ] Decisions recorded
    - [ ] Lessons learned captured
```

---

## 8. Ongoing Compliance

### 8.1 Regular Reviews

```yaml
regular_reviews:
  quarterly:
    - [ ] Access rights review
    - [ ] Third-party vendor review
    - [ ] Breach register review
    - [ ] Rights request metrics

  annual:
    - [ ] Privacy notice accuracy
    - [ ] ROPA completeness
    - [ ] Training completion
    - [ ] Policy updates
    - [ ] Security assessment
    - [ ] Retention schedule compliance

  triggered:
    - [ ] New processing activities (DPIA assessment)
    - [ ] New vendors (due diligence)
    - [ ] Regulatory changes (policy updates)
    - [ ] Security incidents (post-mortem)
```

### 8.2 Documentation Maintenance

```yaml
documentation:
  maintain:
    - "Privacy notices"
    - "Records of Processing (ROPA)"
    - "Consent records"
    - "DPIAs"
    - "Data Processing Agreements"
    - "Breach register"
    - "Rights request log"
    - "Training records"
    - "Policy documents"

  retention:
    - "Keep for duration of processing + [X] years"
    - "Consent records: duration of consent + [X] years"
    - "Breach records: [X] years"
```

---

## GDPR Compliance Score

```yaml
compliance_scoring:
  sections:
    lawful_basis:
      weight: 20%
      score: "[X]%"

    transparency:
      weight: 15%
      score: "[X]%"

    data_subject_rights:
      weight: 20%
      score: "[X]%"

    security:
      weight: 20%
      score: "[X]%"

    accountability:
      weight: 15%
      score: "[X]%"

    third_parties:
      weight: 10%
      score: "[X]%"

  overall_score: "[X]%"

  risk_levels:
    high: "< 50% - Significant remediation needed"
    medium: "50-75% - Gaps to address"
    low: "75-90% - Minor improvements needed"
    compliant: "> 90% - Maintain and monitor"
```

---

## Quick Reference

```yaml
key_deadlines:
  breach_notification: "72 hours"
  rights_requests: "1 month (extendable to 3)"
  consent_withdrawal: "Without undue delay"
  dpo_appointment: "Before processing begins"

key_fines:
  tier_1:
    amount: "Up to €10M or 2% of global turnover"
    violations: "Records, security, DPO, breach notification"

  tier_2:
    amount: "Up to €20M or 4% of global turnover"
    violations: "Core principles, consent, rights, transfers"

useful_resources:
  - "ICO (UK): ico.org.uk"
  - "EDPB: edpb.europa.eu"
  - "CNIL (France): cnil.fr"
  - "Local supervisory authorities"
```

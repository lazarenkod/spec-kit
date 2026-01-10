# {{STANDARD_NAME}} ({{RFC/ISO/Compliance Standard}})

> **Purpose**: Summary and implementation checklist for {{STANDARD_NAME}}. Referenced during specification and planning to ensure compliance.

> **Evidence Tier**: AUTHORITATIVE (official standard/regulation)

---

## Standard Overview

**Full Name**: {{Full Standard Name}}
**Version**: {{Version Number}}
**Published**: YYYY-MM-DD
**Authority**: {{Issuing Body (IETF, ISO, PCI SSC, etc.)}}
**Official Document**: {{URL to official source}}
**Applicability**: {{When this standard applies}}

---

## Key Requirements

### Requirement {{NUMBER}}: {{Title}}

**Severity**: [CRITICAL | HIGH | MEDIUM | LOW]
**Evidence**: {{STANDARD}} Section {{X.X}} [AUTHORITATIVE]

#### Description

{{1-2 sentence summary of the requirement}}

#### Implementation Guidance

{{Step-by-step guidance on how to implement}}

1. Step 1
2. Step 2
3. Step 3

#### Verification

{{How to verify compliance}}

- Code review for {{specific pattern}}
- {{Tool}} scan for {{specific check}}
- Manual audit of {{artifact}}

#### Auto-NFR Generation

```markdown
NFR-{{CATEGORY}}-{{STANDARD}}-{{NUMBER}}: {{Requirement Title}} [{{SEVERITY}}]
- Acceptance: {{Specific, measurable acceptance criteria}}
- Evidence: {{STANDARD}} Req {{NUMBER}} [AUTHORITATIVE]
- Verification: {{How to test/verify}}
- Traceability: → {{Related FRs}}
```

#### Common Pitfalls

- ❌ Anti-pattern 1: {{Description}}
- ❌ Anti-pattern 2: {{Description}}

#### Related Requirements

- {{REQ-XXX}}: {{Related requirement}}

---

## Compliance Triggers

### Keyword Detection

Auto-generate compliance NFRs when specification contains:

| Keyword/Pattern | Triggered Requirement | Auto-NFR |
|-----------------|------------------------|----------|
| "{{keyword}}" | {{STANDARD}} Req {{N}} | NFR-{{CATEGORY}}-{{N}} |

**Example**: "store credit card" → PCI-DSS Req 3.2 → NFR-SEC-PCI-001

---

## Implementation Checklist

Full checklist for {{STANDARD}} compliance:

### Category: {{Category Name}}

- [ ] **REQ-{{N}}**: {{Requirement summary}}
  - Mapped to: {{FR-XXX, NFR-XXX}}
  - Status: [Not Started | In Progress | Complete]
  - Evidence: {{Verification artifact}}

---

## Verification Matrix

| Requirement | Implementation | Verification Method | Status | Evidence |
|-------------|----------------|---------------------|:------:|----------|
| REQ-{{N}} | {{Where implemented}} | {{How verified}} | ✅/⚠️/❌ | {{Artifact}} |

**Legend**:
- ✅ Compliant
- ⚠️ Partial / Needs Review
- ❌ Non-compliant

---

## Penalty & Risk

**Non-compliance penalties**:
- {{Penalty type}}: {{Details}}
- {{Fine range}}: {{Amount}}

**Risk exposure**:
- Legal: {{Risk description}}
- Financial: {{Cost impact}}
- Reputational: {{Brand impact}}

---

## Maintenance

**Last Updated**: YYYY-MM-DD
**Reviewed By**: [Agent or Human]
**Standard Version**: {{Version}}
**Review Frequency**: {{Annual | Quarterly}} (standards are evergreen, but implementation guidance should be reviewed)
**Evidence Tier**: AUTHORITATIVE

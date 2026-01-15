# Security by Design: Executive Summary for Spec-Kit

**Purpose:** Quick reference guide for integrating Security by Design into spec-driven development workflow

---

## The Four Core Questions

### 1. What are the core principles of Security by Design?

**The Five Pillars:**

1. **Least Privilege** → Give users/apps only minimum permissions needed
2. **Defense in Depth** → Layer multiple security controls (no single point of failure)
3. **Secure Defaults** → Secure configuration out-of-box; users opt-out, not opt-in
4. **Minimize Attack Surface** → Reduce exposed ports, libraries, access points
5. **Complete Mediation** → Verify authorization at every boundary (zero-trust)

**Supporting Principles:**
- Fail Securely (errors default to denied/safe state)
- Separation of Duties (single task requires multiple actors)
- Keep It Simple (fewer vulnerabilities = simpler designs)

---

## 2. How do leading frameworks define Security by Design?

### OWASP Secure by Design Framework
- **Focus:** Design-phase security with architectural patterns
- **Key Component:** Design-Phase Security Checklist
- **Best For:** Architects, product designers
- **Workflow:** Plan (define requirements) → Design (apply SbD principles) → Verify (threat modeling) → Develop (implement per ASVS) → Test (security testing) → Deploy

### NIST SSDF (Secure Software Development Framework)
- **Focus:** Comprehensive SDLC security practices
- **Structure:** 42 tasks across 4 categories (Prepare Organization, Prepare Lifecycle, Protect Software, Protect Supply Chain)
- **Requirement:** Mandated for U.S. federal agencies (OMB M-22-18)
- **Best For:** Organizations, compliance teams, government contracts

### ISO 27001:2022 Control 8.27 (Secure System Architecture)
- **Focus:** Engineering principles embedded throughout lifecycle
- **Key Mandate:** "Security by design and default" (not bolted-on)
- **Architecture Layers:** Business, Data, Application, Network, Technology
- **Best For:** Information security management systems, compliance teams

---

## 3. Key phases where security must be embedded

| Phase | What | Why | Who | When |
|-------|------|-----|-----|------|
| **Requirements** | Security objectives, threat landscape, compliance map | Cost of fixing security issues increases 10x per phase | Product + Security | Sprint planning |
| **Design** | Threat models, security architecture, architecture decisions | Design flaws require architectural rework (expensive) | Architects + Security | Before coding |
| **Implementation** | Secure code, secure coding practices, dependency audit | Code-level vulnerabilities easier to fix than architecture | Developers + AppSec | During coding |
| **Testing** | Penetration testing, validation of controls, vulnerability scanning | Catch remaining issues before production | QA + Security | Before release |
| **Deployment** | Secure configuration, monitoring, incident response | Prevent exploitation in production | DevOps + Security | Release process |
| **Maintenance** | Security patches, incident response, threat updates | Continuous security posture | DevSecOps | Ongoing |

**Cost Impact:** A security issue caught in Requirements costs $100 to fix; Design: $1,000; Implementation: $10,000; Testing: $100,000; Production: $1,000,000+

---

## 4. Security artifacts required at each phase

### Requirements Phase Artifacts
- Security requirements document (explicit non-functional requirements)
- Risk assessment report (threat + vulnerability identification)
- Compliance mapping matrix (which frameworks apply; what must we meet)
- Threat modeling kickoff (scope and threat actors identified)

### Design Phase Artifacts
- Threat model(s) with STRIDE analysis (threats identified + controls designed)
- Security architecture document (auth, crypto, audit, network design)
- Design review checklist (verification of requirements addressed)
- API security specification (endpoints, authentication, rate limiting)

### Implementation Phase Artifacts
- Secure coding guidelines (language-specific standards)
- SAST (Static Code Analysis) report (code vulnerabilities found + fixed)
- Dependency/supply chain report (SBOM + vulnerability tracking)
- Security implementation checklist (all controls implemented)

### Testing Phase Artifacts
- Penetration testing report (vulnerabilities found in running app)
- Threat model validation report (proof that mitigations work)
- Vulnerability assessment summary (all scanning results)
- Security test plan & results (requirements traceability)

### Deployment Phase Artifacts
- Deployment security checklist (hardening verified)
- Security operations runbook (incident response, patch procedures)
- Production security dashboard (real-time monitoring)
- Change control & audit trail (all changes logged)

### Maintenance Phase Artifacts
- Security incident log (incidents + root causes + remediation)
- Patch management log (updates applied + tested)
- Continuous vulnerability reports (ongoing monitoring)
- Updated threat models (new threats identified)

---

## How It Maps to Spec-Driven Development

```
/speckit.constitution
    ↓ Establish security principles & governance
/speckit.concept
    ↓ Identify threat landscape & compliance requirements
/speckit.specify
    ↓ Define security requirements for feature
/speckit.plan
    ↓ Threat model & security architecture design
/speckit.tasks
    ↓ Security implementation & testing tasks
/speckit.implement
    ↓ Verify controls implemented; generate artifacts
```

### By Phase:

**`/speckit.constitution`** → Define security governance
```
- Security as first-class principle
- Commitment to frameworks (OWASP/NIST/ISO)
- Review gates and sign-offs
- Roles and responsibilities
```

**`/speckit.concept`** → Map threat landscape & compliance
```
- Who are threat actors?
- What regulations apply?
- What's our security differentiator?
- What are high-risk scenarios?
```

**`/speckit.specify`** → Security requirements in feature spec
```
- Authentication & authorization requirements
- Data protection & encryption requirements
- Audit & logging requirements
- Input validation requirements
- Compliance mappings
```

**`/speckit.plan`** → Threat model & architecture
```
- Threat model (STRIDE-based)
- Security architecture (auth, crypto, logging)
- Design decisions documented
- Test strategy for security
```

**`/speckit.tasks`** → Implementation & testing tasks
```
- Specific security implementation tasks
- Unit & integration test scenarios
- Penetration test cases
- Code review requirements
- Security gates (merge, deployment)
```

**`/speckit.implement`** → Execution & verification
```
- Security controls implemented per design
- SAST/SCA scans passed
- Threat model mitigations validated
- Artifacts generated (SBOM, reports)
- Documentation updated
```

---

## Quick Threat Modeling Primer

**What:** Structured process to identify threats and design mitigations before code exists

**When:** Design phase (2+ hours minimum; decompose for larger systems)

**The Five Steps:**

1. **Define Security Requirements** → What data? Who accesses? What regulations?
2. **Create Diagram** → Draw system architecture showing components, data flows, trust boundaries
3. **Identify Threats** (STRIDE) → For each component/flow, ask:
   - Spoofing: Can someone fake identity?
   - Tampering: Can someone modify data?
   - Repudiation: Is there an audit trail?
   - Info Disclosure: Can someone see secrets?
   - Denial of Service: Can someone prevent access?
   - Elevation of Privilege: Can someone get more permissions?
4. **Design Mitigations** → For each threat, design a control
5. **Validate** → Prove during testing that each mitigation works

**Example Threat:**
```
Threat: User A accesses User B's profile via API
Mitigation: Check in code: if (requester.user_id != profile.user_id AND !is_admin) return 403
Test: Unit test confirms User A cannot read User B's profile
```

---

## Frameworks at a Glance

| Framework | When to Use | Key Artifact | Effort |
|-----------|------------|--------------|--------|
| **OWASP SbD** | Design-heavy products | Security architecture checklist | Medium |
| **NIST SSDF** | Compliance-required work (gov, regulated) | Compliance mapping matrix | High |
| **ISO 27001** | Information security management | Control 8.27 implementation | Medium |
| **OWASP ASVS** | Requirements & testing | Security requirement templates | Medium |
| **OWASP Top 10** | Common vulnerabilities | Code review checklist | Low |

---

## Critical Success Factors

1. **Security Early:** Requirements phase security costs 1/100th of production fixes
2. **Threat-Driven Design:** Threat model identifies what controls are needed
3. **Multiple Layers:** Defense in depth beats single strong control
4. **Automation:** SAST/SCA/container scan in CI pipeline catches issues fast
5. **Documentation:** Threat models & architecture decisions enable knowledge transfer
6. **Regular Updates:** Threat models become stale; update when architecture changes
7. **Team Alignment:** Product, architecture, dev, infra must all own security

---

## Implementation Checklist for Next Project

```
Before Starting:
- [ ] Read constitution (security principles established)
- [ ] Know threat actors and compliance requirements (concept phase)

During Planning:
- [ ] Write security requirements (specify phase)
- [ ] Create threat model (2+ hour session with architect)
- [ ] Design security architecture per mitigations (plan phase)
- [ ] Define security testing tasks (tasks phase)

During Development:
- [ ] Follow secure coding guidelines
- [ ] Run SAST/SCA in CI pipeline
- [ ] Code review with security focus
- [ ] Implement all mitigations from threat model

Before Release:
- [ ] Penetration testing completed
- [ ] All high-severity findings remediated
- [ ] Threat model validated (controls proven to work)
- [ ] Deployment security checklist passed
- [ ] Monitoring and incident response ready
```

---

## Key Resources

**Official Frameworks:**
- OWASP: https://owasp.org/www-project-secure-by-design-framework/
- NIST: https://csrc.nist.gov/projects/ssdf
- ISO: https://www.iso.org/standard/27001

**Quick Guides:**
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [CMS Threat Modeling Handbook](https://security.cms.gov/learn/cms-threat-modeling-handbook)
- [Microsoft Threat Modeling Tool](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)

**Secure Development:**
- [OWASP Top 10](https://owasp.org/Top10/) (most common vulnerabilities)
- [CWE Top 25](https://cwe.mitre.org/top25/) (dangerous weaknesses)
- [CISA Secure by Design](https://www.cisa.gov/securebydesign)

---

## For More Detail

See **`SECURITY_BY_DESIGN_RESEARCH.md`** for:
- Detailed principle explanations
- Framework deep-dives
- Artifact templates
- Complete integration examples
- 20+ authoritative references

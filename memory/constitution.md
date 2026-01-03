# [PROJECT_NAME] Constitution (Layer 2)

**Base Layer**: constitution.base.md v1.1
**Domain Layer**: [none | fintech | healthcare | e-commerce | saas]
**Effective Date**: [DATE]

---

## How Layered Constitution Works

This is **Layer 2** (project-specific) of the constitution:

```text
Layer 0: constitution.base.md ──────── 20 enterprise principles (READ-ONLY)
    ↓ inherits
Layer 1: constitution.domain.md ────── Domain-specific (fintech, healthcare, etc.)
    ↓ inherits
Layer 2: constitution.md (this file) ─ Your project overrides
```

**Rules**:
- You INHERIT all principles from Layer 0 (and Layer 1 if domain selected)
- You can STRENGTHEN principles (SHOULD → MUST) but NEVER weaken (MUST → SHOULD)
- You can ADD new project-specific principles
- You can REFINE parameters (e.g., coverage 80% → 90%)

---

## Quick Start

1. **Review base principles**: Read `constitution.base.md` to understand defaults
2. **Select domain** (optional): Copy `domains/[domain].md` to `constitution.domain.md`
3. **Configure project settings**: Set language and other preferences below
4. **Add overrides below**: Strengthen or add principles as needed

---

## Project Settings

<!-- Project-wide settings that affect artifact generation -->

| Setting | Value | Description |
|---------|-------|-------------|
| **language** | `en` | Primary language for generated artifacts. Options: `en` (English), `ru` (Russian), `de` (German), `fr` (French), `es` (Spanish), `zh` (Chinese), `ja` (Japanese), `ko` (Korean), `pt` (Portuguese), `it` (Italian), `pl` (Polish), `uk` (Ukrainian), `ar` (Arabic), `hi` (Hindi) |
| **date_format** | `ISO` | Date format in documents. Options: `ISO` (2024-01-15), `US` (01/15/2024), `EU` (15.01.2024) |
| **measurements** | `metric` | Unit system. Options: `metric`, `imperial` |

### Language Guidelines

When `language` is set:
- All generated artifacts (spec.md, plan.md, tasks.md, design.md, concept.md) use this language
- Technical terms (API, CRUD, JWT, etc.) remain in English
- Code comments follow project's code style (usually English)
- User-facing content (acceptance criteria, user stories) uses the configured language

**Example for Russian**:
```markdown
language: ru

# Results in:
## Функциональные требования
### FR-001: Аутентификация пользователя
Пользователь ДОЛЖЕН иметь возможность войти в систему используя email и пароль.
```

---

## Strengthened Principles

<!--
Override base/domain principles here.
You can only strengthen (SHOULD → MUST) or tighten parameters.
Example:
-->

| Base ID | Original Level | New Level | Rationale |
|---------|----------------|-----------|-----------|
| QUA-001 | SHOULD (80%) | MUST (90%) | Critical system, high coverage required |
| OBS-003 | SHOULD | MUST | Kubernetes deployment requires health checks |

---

## Project-Specific Principles

<!--
Add principles unique to your project.
Use format: PRJ-001, PRJ-002, etc.
-->

### PRJ-001: [Principle Name]

**Level**: MUST | SHOULD
**Applies to**: [scope]

[Description of the principle and its rationale]

**Validation**: [How to verify compliance]
**Violations**: [Severity - CRITICAL, HIGH, MEDIUM, LOW]

---

### PRJ-002: [Principle Name]

**Level**: MUST | SHOULD
**Applies to**: [scope]

[Description]

**Validation**: [How to verify]
**Violations**: [Severity]

---

## Technology Constraints

<!-- Project-specific technology decisions that affect principles -->

| Category | Decision | Rationale |
|----------|----------|-----------|
| Language | [e.g., Python 3.11+] | [why] |
| Framework | [e.g., FastAPI] | [why] |
| UI Framework | [React \| Vue \| Angular \| Svelte \| None] | [frontend framework - triggers library recommendations] |
| Database | [e.g., PostgreSQL 15] | [why] |
| Cloud | [e.g., AWS] | [why] |

---

## Compliance Requirements

<!-- Mark applicable compliance frameworks. These drive security and audit requirements. -->

| Framework | Required | Scope | Certification Date |
|-----------|:--------:|-------|:------------------:|
| **GDPR** | [ ] | EU personal data processing | [DATE] |
| **SOC 2 Type II** | [ ] | Security, availability, confidentiality | [DATE] |
| **HIPAA** | [ ] | Protected health information (PHI) | [DATE] |
| **PCI-DSS** | [ ] | Payment card data | [DATE] |
| **ISO 27001** | [ ] | Information security management | [DATE] |
| **FedRAMP** | [ ] | US federal cloud services | [DATE] |
| **CCPA** | [ ] | California consumer privacy | [DATE] |

### Compliance Notes

[Document compliance scope, DPO contact, audit schedule]

---

## Security Standards

<!-- Define security implementation requirements -->

| Category | Standard | Implementation |
|----------|----------|----------------|
| **Authentication** | OAuth2/OIDC | [Provider: Auth0/Cognito/Keycloak] |
| **Authorization** | RBAC/ABAC | [Implementation notes] |
| **Encryption (Transit)** | TLS 1.3 | [Certificate management] |
| **Encryption (Rest)** | AES-256 | [Key management] |
| **Secrets Management** | Vault/Secrets Manager | [Provider] |
| **MFA** | Required/Optional | [Scope: admin/all users] |
| **SSO** | SAML 2.0/OIDC | [Provider] |

### Security Contacts

| Role | Contact | Escalation |
|------|---------|------------|
| Security Lead | [Name] | [Email] |
| DPO (Data Protection Officer) | [Name] | [Email] |
| Incident Response | [Team] | [Pager] |

---

## Approval Matrix

<!-- Define decision authority and escalation paths -->

| Decision Type | Authority | Approval Required | Escalation |
|---------------|-----------|:-----------------:|------------|
| Architecture breaking changes | Architecture Board | Yes | CTO |
| Security exceptions | Security Team | Yes | CISO |
| Data model changes | Data Team | Yes | Data Architect |
| API breaking changes | API Guild | Yes | Tech Lead |
| Dependency major upgrades | Tech Lead | No | Architecture Board |
| New external integrations | Security Team | Yes | CTO |
| Production deployment | DevOps Lead | No | On-call Engineer |

### Escalation SLA

| Priority | Initial Response | Resolution |
|----------|-----------------|------------|
| P0 (Critical) | 15 minutes | 4 hours |
| P1 (High) | 1 hour | 24 hours |
| P2 (Medium) | 4 hours | 72 hours |
| P3 (Low) | 24 hours | 1 week |

---

## Technology Radar

<!-- Categorize technologies by adoption status. Review quarterly. -->

| Category | Adopt | Trial | Assess | Hold |
|----------|-------|-------|--------|------|
| **Languages** | [Current stack] | [Evaluating] | [Watching] | [Deprecated] |
| **Frameworks** | | | | |
| **Databases** | | | | |
| **Infrastructure** | | | | |
| **Observability** | | | | |
| **Security** | | | | |

### Radar Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| **Adopt** | Production-ready, recommended | Use in new projects |
| **Trial** | Proven in PoC, ready for production pilot | Use with monitoring |
| **Assess** | Worth exploring, not production-ready | Research only |
| **Hold** | Deprecated or problematic | Migrate away |

### Technology Decisions Log

| Date | Technology | From | To | Rationale |
|------|------------|------|-----|-----------|
| [DATE] | [Tech] | [Status] | [Status] | [Why] |

---

## SLA Targets

<!-- Define service level objectives -->

| Metric | Target | Critical Threshold | Measurement |
|--------|:------:|:------------------:|-------------|
| **Availability** | 99.9% | 99.5% | Uptime monitoring |
| **RTO (Recovery Time)** | 4 hours | 8 hours | Disaster recovery drill |
| **RPO (Recovery Point)** | 1 hour | 4 hours | Backup verification |
| **MTTR (Mean Time to Repair)** | 30 minutes | 2 hours | Incident log |
| **P99 Latency** | 500ms | 2s | APM |
| **Error Rate** | < 0.1% | < 1% | Error tracking |

### SLA Tiers by Environment

| Environment | Availability | Support Hours | RTO |
|-------------|:------------:|---------------|:---:|
| Production | 99.9% | 24/7 | 4h |
| Staging | 99% | Business hours | 24h |
| Development | Best effort | Business hours | 72h |

### SLA Breach Escalation

| Breach Duration | Action | Notification |
|-----------------|--------|--------------|
| < 15 min | Automated alert | On-call engineer |
| 15-60 min | Incident declared | Team lead |
| > 60 min | War room | Director/VP |
| > 4 hours | Executive escalation | CTO |

---

## Design System Configuration

<!--
  Configure your UI framework, theme tokens, and enforcement level.
  This section enables DSS (Design System) principle enforcement.
  Presets available: shadcn/ui, mui, vuetify, tailwind, bootstrap, none
  See templates/shared/design-system-presets.md for preset values.
-->

### Framework Selection

| Setting | Value | Options |
|---------|-------|---------|
| **framework** | `none` | `shadcn/ui`, `mui`, `vuetify`, `angular-material`, `skeleton-ui`, `tailwind`, `bootstrap`, `none` |
| **component_library_url** | - | URL to documentation (auto-filled by preset) |
| **enforcement_level** | `warn` | `strict` (block deployment), `warn` (report violations), `off` (disabled) |

### Theme Tokens

Configure your design system tokens below. Use a preset or define custom tokens:

```yaml
design_system:
  # Preset: uncomment ONE to use predefined tokens, or define custom below
  # preset: "shadcn/ui"   # See design-system-presets.md
  # preset: "mui"
  # preset: "tailwind"

  framework: "none"

  theme:
    colors:
      # Core palette
      primary: "#3B82F6"
      secondary: "#10B981"
      background: "#FFFFFF"
      foreground: "#1F2937"
      muted: "#F3F4F6"
      accent: "#8B5CF6"
      destructive: "#EF4444"

      # Component-specific (optional)
      # border: "#E5E7EB"
      # ring: "#3B82F6"
      # card: "#FFFFFF"
      # popover: "#FFFFFF"

    typography:
      font_family: "Inter, system-ui, sans-serif"
      font_family_mono: "JetBrains Mono, monospace"
      scale:
        xs: "0.75rem"    # 12px
        sm: "0.875rem"   # 14px
        base: "1rem"     # 16px
        lg: "1.125rem"   # 18px
        xl: "1.25rem"    # 20px
        2xl: "1.5rem"    # 24px
        3xl: "1.875rem"  # 30px

    spacing:
      unit: "4px"        # Base unit for spacing calculations

    radii:
      none: "0"
      sm: "0.25rem"      # 4px
      md: "0.375rem"     # 6px
      lg: "0.5rem"       # 8px
      xl: "0.75rem"      # 12px
      full: "9999px"

  component_library_url: ""
  enforcement_level: "warn"   # strict | warn | off
```

### Enforcement Behavior

| Level | DSS-001 (Components) | DSS-002 (Colors) | DSS-003 (Typography) |
|-------|---------------------|------------------|---------------------|
| `strict` | HIGH (blocks) | CRITICAL (blocks) | HIGH (blocks) |
| `warn` | MEDIUM (reports) | HIGH (reports) | MEDIUM (reports) |
| `off` | Disabled | Disabled | Disabled |

---

## Exceptions

<!--
Document any TEMPORARY exceptions to principles.
Exceptions must have expiration dates and remediation plans.
-->

| Principle ID | Exception | Expiration | Remediation Plan |
|--------------|-----------|------------|------------------|
| [ID] | [What is excepted] | [Date] | [How it will be fixed] |

---

## Governance

- This constitution is enforced by `/speckit.analyze` command
- MUST violations are CRITICAL severity and block implementation
- SHOULD violations are MEDIUM severity and require justification
- Amendments require team review and version update

---

## Effective Principles Summary

<!--
This section can be auto-generated by running:
/speckit.constitution --merge

It will show all active principles from all layers.
-->

Run `/speckit.constitution --merge` to generate merged view.

---

**Version**: 1.0.0
**Created**: [DATE]
**Last Amended**: [DATE]

# Domain Extension: SaaS / Multi-Tenant (Layer 1)

**Extends**: constitution.base.md v1.0
**Regulatory Context**: SOC 2, GDPR (data residency), industry-specific (HIPAA, PCI if applicable)
**Typical Projects**: B2B platforms, productivity tools, developer tools, analytics platforms

---

## Key Concepts

- **Tenant**: A customer organization using the platform
- **Tenant Isolation**: Ensuring one tenant cannot access another's data
- **Noisy Neighbor**: One tenant's usage affecting others' performance
- **Data Residency**: Where tenant data is physically stored

---

## Strengthened Principles

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| API-003 | SHOULD | MUST | Multi-tenant requires fair resource allocation |
| SEC-005 | MUST | MUST (with tenant context) | Every request must have tenant identity |
| OBS-001 | MUST | MUST (with tenant_id) | All logs must include tenant context |
| PRF-002 | MUST | MUST (per-tenant limits) | Prevent noisy neighbor |
| CMP-001 | MUST | MUST (tenant-aware) | Audit logs must identify tenant |

---

## Additional Principles

### SAS-001: Tenant Isolation

**Level**: MUST
**Applies to**: All data access

Tenant data MUST be isolated:
- Row-level security or schema/database per tenant
- Tenant context MUST be injected at request entry
- Cross-tenant queries MUST be impossible without explicit super-admin

**Validation**: Review data access patterns for tenant filtering
**Violations**: CRITICAL - Data breach

---

### SAS-002: Usage Metering

**Level**: MUST
**Applies to**: Billable resources

All billable resource usage MUST be metered:
- API calls, storage, compute
- Metering MUST be accurate to billing precision
- Metering data MUST be retained for billing disputes

**Validation**: Review metering implementation
**Violations**: HIGH - Revenue leakage or overbilling

---

### SAS-003: Tenant Provisioning

**Level**: SHOULD
**Applies to**: Onboarding

Tenant provisioning SHOULD be automated:
- Self-service signup (for PLG)
- Automated resource allocation
- Default configuration templates

**Validation**: Review provisioning workflow
**Violations**: MEDIUM - Scaling friction

---

### SAS-004: Tenant Configuration

**Level**: SHOULD
**Applies to**: Customizable features

Per-tenant configuration SHOULD be supported:
- Feature flags per tenant
- Custom branding (white-label)
- Integration settings

**Validation**: Review configuration management
**Violations**: LOW - Flexibility limited

---

### SAS-005: Data Residency

**Level**: SHOULD
**Applies to**: Global deployments

Data residency requirements SHOULD be supported:
- Region selection during signup
- Data location transparency
- Cross-region data transfer controls

**Validation**: Review data storage architecture
**Violations**: MEDIUM - GDPR/compliance risk for EU customers

---

### SAS-006: Tenant Offboarding

**Level**: MUST
**Applies to**: Account deletion

Tenant offboarding MUST:
- Export all tenant data in portable format
- Completely delete tenant data within 30 days
- Provide deletion confirmation

**Validation**: Review offboarding workflow
**Violations**: HIGH - GDPR right to erasure

---

### SAS-007: Service Level Tiers

**Level**: SHOULD
**Applies to**: Multi-tier offerings

Systems SHOULD support tiered service levels:
- Different rate limits per tier
- Feature gating by subscription level
- Resource allocation by tier

**Validation**: Review tier implementation
**Violations**: LOW - Monetization flexibility limited

---

### SAS-008: Noisy Neighbor Prevention

**Level**: MUST
**Applies to**: Shared infrastructure

Resource usage MUST be bounded per tenant:
- CPU/memory quotas
- Rate limiting per tenant
- Queue prioritization
- Resource reservation for premium tiers

**Validation**: Review resource isolation
**Violations**: HIGH - Platform-wide performance impact

---

## Multi-Tenancy Patterns

| Pattern | Use Case | Isolation Level |
|---------|----------|-----------------|
| Shared schema (row-level) | High volume, low customization | Medium |
| Schema per tenant | Moderate volume, some customization | High |
| Database per tenant | Enterprise, high customization | Highest |
| Hybrid | Mixed customer base | Variable |

Chosen pattern: [TO BE DETERMINED BY PROJECT]

---

## Summary

| Type | Count |
|------|-------|
| Strengthened from base | 5 |
| New MUST principles | 4 |
| New SHOULD principles | 4 |
| **Total additional requirements** | **13** |

---

## Usage

```bash
cp memory/domains/saas.md memory/constitution.domain.md
```

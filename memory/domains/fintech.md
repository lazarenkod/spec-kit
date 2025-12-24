# Domain Extension: Financial Technology (Layer 1)

**Extends**: constitution.base.md v1.0
**Regulatory Context**: PCI-DSS, SOX, banking regulations
**Typical Projects**: Payment processing, trading platforms, banking apps, investment tools

---

## Strengthened Principles

These base principles are elevated from SHOULD to MUST for fintech:

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| CMP-001 | MUST | MUST | Already MUST, emphasize immutability |
| CMP-002 | SHOULD | MUST | Financial record retention requirements (7+ years) |
| PRF-001 | SHOULD (<500ms) | MUST (<200ms) | Trading/payment latency requirements |
| OBS-004 | SHOULD | MUST | Transaction timing is regulatory requirement |
| SEC-006 | SHOULD | MUST | Financial data requires strict access control |

---

## Additional Principles

### FIN-001: Transaction Atomicity

**Level**: MUST
**Applies to**: All financial transactions

Financial transactions MUST be atomic. Money movement MUST use saga patterns or two-phase commit. Partial transactions MUST be rolled back completely.

**Validation**: Review transaction handling code
**Violations**: CRITICAL - Financial inconsistency

---

### FIN-002: Audit Trail Immutability

**Level**: MUST
**Applies to**: All audit logs and transaction records

Audit records and transaction logs MUST be immutable once written. Append-only storage MUST be used. Deletion or modification MUST be cryptographically impossible.

**Validation**: Verify append-only audit storage
**Violations**: CRITICAL - Regulatory non-compliance

---

### FIN-003: Dual Control

**Level**: SHOULD
**Applies to**: High-value operations

Operations above threshold (e.g., transfers > $10,000) SHOULD require dual approval. Administrative actions SHOULD require separate authorization.

**Validation**: Review approval workflows
**Violations**: HIGH - Fraud risk

---

### FIN-004: Regulatory Reporting

**Level**: MUST
**Applies to**: Reportable transactions

Transactions meeting regulatory thresholds MUST be flagged for reporting. SAR/CTR generation MUST be automated where possible.

**Validation**: Review regulatory reporting integration
**Violations**: CRITICAL - Regulatory violation

---

### FIN-005: Reconciliation

**Level**: MUST
**Applies to**: Financial ledgers

All ledgers MUST reconcile. Reconciliation MUST run at least daily. Discrepancies MUST trigger alerts.

**Validation**: Check reconciliation jobs
**Violations**: HIGH - Undetected errors

---

### FIN-006: Money Precision

**Level**: MUST
**Applies to**: All monetary calculations

Monetary values MUST use appropriate precision (Decimal, not float). Currency MUST be explicit. Rounding rules MUST be defined and consistent.

**Validation**: Review money handling code
**Violations**: CRITICAL - Financial calculation errors

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

To apply this domain extension:

```bash
cp memory/domains/fintech.md memory/constitution.domain.md
```

Then customize `memory/constitution.md` for project-specific overrides.

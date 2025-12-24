# Domain Extension: E-Commerce (Layer 1)

**Extends**: constitution.base.md v1.0
**Regulatory Context**: PCI-DSS (payment), GDPR/CCPA (privacy), consumer protection laws
**Typical Projects**: Online stores, marketplaces, subscription services, checkout systems

---

## Strengthened Principles

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| PRF-001 | SHOULD (<500ms) | MUST (<300ms) | Cart abandonment increases with latency |
| PRF-004 | SHOULD | MUST | Product catalog must be cached for performance |
| REL-003 | SHOULD | MUST | Payment operations must be idempotent |
| SEC-002 | MUST | MUST (with rate limiting) | Prevent credential stuffing, card testing |
| CMP-003 | SHOULD | MUST | GDPR/CCPA require privacy by design |

---

## Additional Principles

### ECM-001: PCI Compliance

**Level**: MUST
**Applies to**: Payment processing

Payment card data MUST be handled per PCI-DSS:
- Never store CVV/CVC
- Tokenize or encrypt card numbers
- Use PCI-compliant payment processors
- Quarterly vulnerability scans

**Validation**: Review payment data handling
**Violations**: CRITICAL - PCI non-compliance

---

### ECM-002: Inventory Consistency

**Level**: MUST
**Applies to**: Product inventory

Inventory MUST be eventually consistent with bounded staleness. Overselling MUST be prevented for limited stock. Stock reservations MUST timeout.

**Validation**: Review inventory management
**Violations**: HIGH - Customer experience, fulfillment issues

---

### ECM-003: Cart Persistence

**Level**: SHOULD
**Applies to**: Shopping cart

Shopping cart SHOULD persist across sessions (24-48 hours minimum). Cart recovery emails SHOULD be supported for abandoned carts.

**Validation**: Check cart persistence implementation
**Violations**: MEDIUM - Lost revenue

---

### ECM-004: Order Immutability

**Level**: MUST
**Applies to**: Order management

Placed orders MUST be immutable. Changes MUST create amendments, not modifications. Order history MUST be preserved for disputes.

**Validation**: Review order data model
**Violations**: HIGH - Dispute resolution impaired

---

### ECM-005: Price Consistency

**Level**: MUST
**Applies to**: Pricing display and checkout

Price shown at product MUST match price at checkout. Price changes MUST NOT affect items already in cart (honor cart price).

**Validation**: Review pricing flow
**Violations**: CRITICAL - Legal issues, customer trust

---

### ECM-006: Fraud Prevention

**Level**: SHOULD
**Applies to**: Checkout and account creation

Systems SHOULD implement fraud prevention:
- Address verification (AVS)
- Velocity checks
- Device fingerprinting
- 3D Secure for high-risk transactions

**Validation**: Review fraud prevention measures
**Violations**: HIGH - Financial loss

---

### ECM-007: SEO Friendliness

**Level**: SHOULD
**Applies to**: Product pages

Product pages SHOULD be SEO-friendly:
- Server-side rendering or pre-rendering
- Structured data (JSON-LD)
- Canonical URLs
- Fast loading (Core Web Vitals)

**Validation**: Run SEO audit
**Violations**: LOW - Discoverability reduced

---

## Performance Thresholds

| Page Type | Target p95 | Rationale |
|-----------|-----------|-----------|
| Product listing | < 200ms | Browse abandonment |
| Product detail | < 300ms | Add to cart conversion |
| Cart | < 200ms | Checkout funnel |
| Checkout | < 500ms | Payment completion |
| Search | < 150ms | Search abandonment |

---

## Summary

| Type | Count |
|------|-------|
| Strengthened from base | 5 |
| New MUST principles | 4 |
| New SHOULD principles | 3 |
| **Total additional requirements** | **12** |

---

## Usage

```bash
cp memory/domains/e-commerce.md memory/constitution.domain.md
```

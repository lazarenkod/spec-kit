# Stripe API Technical Constraints

> **Purpose**: Documented technical limitations, quotas, and rate limits for Stripe API. Used during planning to validate NFRs and generate constraint-driven requirements.
>
> **Evidence Standard**: [AUTHORITATIVE] tier (official Stripe documentation updated 2025-01-01).

---

## Platform Overview

**Vendor**: Stripe, Inc.
**Technology**: Stripe API v2023-10-16 (latest stable)
**Documentation**: <https://stripe.com/docs>
**Last Updated**: 2025-01-01
**Evidence Tier**: AUTHORITATIVE

---

## Rate Limits

| Operation | Limit | Scope | Penalty | Workaround |
|-----------|-------|-------|---------|------------|
| API requests | 100 req/sec | Per account (default) | 429 Too Many Requests | Exponential backoff, request increase |
| API requests (high volume) | 1000 req/sec | Per account (approved) | 429 Too Many Requests | Contact support for rate limit increase |
| Webhook delivery | 1000 events/sec | Per endpoint | Event loss, retry | Multiple endpoints, event log polling |
| File uploads | 10 MB | Per file | 413 Payload Too Large | Compress files, split large uploads |
| Connect OAuth | 25 req/min | Per platform | 429 Too Many Requests | Cache tokens, retry with backoff |
| Search API | 20 req/sec | Per account | 429 Too Many Requests | Use list endpoints with pagination |
| Payment intents (test mode) | 500 req/hr | Per account | 429 Too Many Requests | Optimize test workflows |

### Rate Limit Implementation Notes

**Exponential Backoff Pattern**:

```python
import time
import stripe

def create_payment_with_retry(amount, currency):
    max_retries = 3
    retry_count = 0
    base_delay = 1  # seconds

    while retry_count < max_retries:
        try:
            return stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                automatic_payment_methods={'enabled': True}
            )
        except stripe.error.RateLimitError as e:
            retry_count += 1
            if retry_count >= max_retries:
                raise

            # Exponential backoff with jitter
            delay = base_delay * (2 ** retry_count) + random.uniform(0, 1)
            time.sleep(delay)
```

**Best Practice**: Always implement exponential backoff for production APIs

---

## Resource Quotas

| Resource | Limit | Hard/Soft | Upgrade Path |
|----------|-------|-----------|--------------|
| Connected accounts | 100,000 | Soft | Contact support |
| Products | 50,000 | Soft | Contact support |
| Prices per product | 100 | Soft | Contact support |
| Metadata keys per object | 50 | Hard | Cannot increase |
| Metadata value length | 500 chars | Hard | Cannot increase |
| Custom fields (per object) | 20 | Soft | Contact support |
| Webhook endpoints | 16 | Soft | Contact support |
| Payment methods per customer | 100 | Soft | Contact support |

### Quota Monitoring

- **Alert threshold**: 80% of quota
- **Escalation**: Email to account manager with business justification
- **Cost impact**: No additional cost for quota increases (subject to approval)

**Monitoring Script**:

```python
# Check current usage against quotas
def check_stripe_quotas():
    products_count = stripe.Product.list(limit=1).get('total_count', 0)
    if products_count > 40000:  # 80% of 50,000
        send_alert(f"Products quota at {products_count}/50000")
```

---

## Performance Constraints

| Metric | Limit | Context | Impact |
|--------|-------|---------|--------|
| API latency | ~200ms (P50) | Global average | Acceptable for async operations |
| API latency | ~500ms (P95) | Global average | May impact user-facing flows |
| API latency | ~1000ms (P99) | Global average | Timeout risk for slow connections |
| Webhook delivery timeout | 30 seconds | Per webhook attempt | Endpoint must respond <30s |
| Webhook retry window | 3 days | Failed deliveries | Events discarded after 3 days |
| Idempotency key TTL | 24 hours | Duplicate prevention | Stale keys treated as new requests |
| Checkout session TTL | 24 hours | Payment page expiration | Customer must complete within 24h |
| Payment intent confirmation | 5 minutes | SCA timeout | 3DS must complete within 5 min |

### Performance Optimization

**Batch Operations**:

```python
# Instead of 100 individual API calls:
for customer_id in customer_ids:
    stripe.Customer.retrieve(customer_id)  # 100 API calls

# Use list with filtering:
customers = stripe.Customer.list(limit=100).auto_paging_iter()  # 1-2 API calls
```

**Caching Strategy**:

- Cache product/price catalogs (TTL: 1 hour)
- Cache customer objects (TTL: 5 minutes)
- NEVER cache: payment intents, charges (real-time data)

---

## Storage Limits

| Type | Limit | Retention | Cost |
|------|-------|-----------|------|
| Event log retention | 30 days (default) | 30-90 days | Free (30 days), $0.0001/event/day (extended) |
| File storage | Unlimited | Indefinite | $0.02/GB/month |
| Payment method data | Unlimited | Per card network rules | Included |
| Customer metadata | 50 keys × 500 chars | Indefinite | Included |

**Retention Best Practices**:

- Export event logs to data warehouse for analysis >30 days
- Use file storage for receipts, invoices, dispute evidence
- Clean up old payment methods (PCI compliance)

---

## Auto-NFR Generation

### Performance NFRs

```markdown
NFR-PERF-STRIPE-001: Handle API rate limit (100 req/sec) [HIGH]
- Acceptance: Exponential backoff implemented for 429 responses
- Evidence: Stripe Rate Limits [AUTHORITATIVE]
- Constraint: 100 req/sec per account (default tier)
- Traceability: → FR-XXX (Payment processing)

NFR-PERF-STRIPE-002: Webhook response time <10 seconds [MEDIUM]
- Acceptance: Webhook endpoint responds within 10 seconds (30s hard limit)
- Evidence: Stripe Webhook Documentation [AUTHORITATIVE]
- Constraint: 30 second timeout
- Traceability: → FR-XXX (Payment notifications)

NFR-PERF-STRIPE-003: Implement idempotency keys [HIGH]
- Acceptance: All POST requests include Idempotency-Key header
- Evidence: Stripe Idempotency Documentation [AUTHORITATIVE]
- Constraint: 24-hour key TTL
- Traceability: → FR-XXX (Payment reliability)
```

### Reliability NFRs

```markdown
NFR-REL-STRIPE-001: Handle webhook delivery failures [MEDIUM]
- Acceptance: Poll event log for missed webhooks every 5 minutes
- Evidence: Stripe Webhook Best Practices [AUTHORITATIVE]
- Constraint: 3-day retry window
- Traceability: → FR-XXX (Payment status sync)

NFR-REL-STRIPE-002: Validate webhook signatures [CRITICAL]
- Acceptance: Reject webhooks with invalid signatures
- Evidence: Stripe Webhook Security [AUTHORITATIVE]
- Constraint: Signature verification required for production
- Traceability: → FR-XXX (Payment security)
```

### Scalability NFRs

```markdown
NFR-SCALE-STRIPE-001: Request rate limit increase for high volume [LOW]
- Acceptance: Request 1000 req/sec limit when approaching 80 req/sec
- Evidence: Stripe Rate Limit Increase Process [AUTHORITATIVE]
- Constraint: Approval required, 2-4 week lead time
- Traceability: → FR-XXX (Scale projections)
```

---

## Known Issues & Gotchas

### Issue: Webhook Delivery Order Not Guaranteed

**Description**: Stripe webhooks may arrive out of order (e.g., `payment_intent.succeeded` before `payment_intent.created`)

**Workaround**:
- Use `event.created` timestamp to order events
- Poll Event API for missing events
- Implement event deduplication by `event.id`

**Status**: By Design
**Evidence**: <https://stripe.com/docs/webhooks/best-practices#event-ordering>

```python
# Handle out-of-order webhooks
def process_webhook(event):
    # Check if already processed
    if EventLog.exists(event.id):
        return  # Idempotent

    # Process event
    handle_event(event)

    # Mark as processed
    EventLog.create(id=event.id, timestamp=event.created)
```

### Issue: Idempotency Key Required for Retries

**Description**: Retrying failed API calls without idempotency keys can create duplicate charges

**Workaround**:
- Generate UUID for each payment operation
- Store idempotency key with transaction record
- Reuse same key for retries within 24 hours

**Status**: By Design (safety feature)
**Evidence**: <https://stripe.com/docs/api/idempotent_requests>

```python
# Generate and persist idempotency key
def create_payment_intent(order_id, amount):
    idempotency_key = get_or_create_idempotency_key(order_id)

    return stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        idempotency_key=idempotency_key
    )
```

### Issue: Metadata Limitations (50 keys × 500 chars)

**Description**: Metadata cannot store large JSON objects or unlimited fields

**Workaround**:
- Store reference ID in metadata, full data in your database
- Use multiple metadata keys for structured data (e.g., `user_id`, `order_id`, `campaign_id`)
- Compress data if necessary (Base64 encode)

**Status**: Hard Limit
**Evidence**: <https://stripe.com/docs/api/metadata>

### Issue: 3DS Authentication Timeout (5 minutes)

**Description**: Payment intents requiring SCA (3D Secure) expire after 5 minutes

**Workaround**:
- Display clear countdown timer to customer
- Create new payment intent if timeout occurs
- Use `setup_future_usage` to save card for future (non-SCA) use

**Status**: By Design (security requirement)
**Evidence**: <https://stripe.com/docs/strong-customer-authentication>

---

## Integration Checklist

When using Stripe API in architecture:

- [ ] Rate limits validated against expected load (100 req/sec default)
- [ ] Exponential backoff implemented for 429/503 responses
- [ ] Webhook endpoint responds within 10 seconds (30s hard limit)
- [ ] Webhook signature verification implemented
- [ ] Idempotency keys generated for all POST requests
- [ ] Event log polling for missed webhooks (every 5 min)
- [ ] Monitoring alerts set at 80 req/sec (80% of limit)
- [ ] Cost estimation includes file storage, extended event retention
- [ ] Fallback strategy for webhook delivery failures
- [ ] Metadata usage within limits (50 keys × 500 chars)
- [ ] 3DS timeout handling (5 minutes)
- [ ] Test mode API keys separated from production

---

## Maintenance

**Last Updated**: 2025-01-10
**Reviewed By**: community-intelligence-ai, constraints-analyzer-ai
**Evidence Tier**: AUTHORITATIVE
**Source URL**: <https://stripe.com/docs>
**Freshness**: 10 days (threshold: 90 days)
**Next Review**: 2025-03-01

# Fintech Best Practices

> **Purpose**: Curated collection of proven patterns for fintech applications. Referenced during architecture planning to inform ADR decisions.
>
> **Evidence Standard**: Each practice requires [AUTHORITATIVE] or [STRONG] evidence tier (vendor docs, research papers, regulatory guidance).

---

## Practice: Idempotency Keys for Payment Operations

**Category**: Reliability
**Applicability**: All payment API integrations (Stripe, PayPal, Adyen, etc.)
**Evidence Tier**: AUTHORITATIVE
**Source**: Stripe API Documentation (<https://stripe.com/docs/api/idempotent_requests>)

### Description

Use idempotency keys to prevent duplicate payment charges caused by network retries, user double-clicks, or application crashes. Idempotency ensures that multiple identical requests produce the same result as a single request.

### Implementation

1. **Generate UUID for each payment operation**:

```python
import uuid
from datetime import datetime, timedelta

def create_payment_with_idempotency(order_id, amount, currency='usd'):
    # Generate or retrieve existing idempotency key
    idempotency_key = get_or_create_idempotency_key(order_id)

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            metadata={'order_id': order_id},
            idempotency_key=idempotency_key
        )
        return payment_intent
    except stripe.error.IdempotencyError:
        # Key reused with different parameters
        raise ValueError("Payment parameters changed, cannot reuse key")

def get_or_create_idempotency_key(order_id):
    # Check database for existing key (within 24h TTL)
    key_record = IdempotencyKey.query.filter_by(
        order_id=order_id,
        created_at__gte=datetime.now() - timedelta(hours=24)
    ).first()

    if key_record:
        return key_record.key

    # Generate new key
    new_key = str(uuid.uuid4())
    IdempotencyKey.create(order_id=order_id, key=new_key)
    return new_key
```

2. **Store key with transaction record**:

```sql
CREATE TABLE idempotency_keys (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(255) NOT NULL,
    key VARCHAR(36) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id),
    INDEX idx_key (key)
);
```

3. **Key TTL = 24 hours** (Stripe standard, other processors may vary)

### Rationale

**Problem**: Network failures, slow responses, or application crashes can cause payment retries, leading to duplicate charges.

**Solution**: Idempotency keys ensure that retrying the same request (same key) returns the original result without creating a new charge.

**Evidence**: Stripe processes 500M+ API requests/day; idempotency prevents millions of duplicate charges annually.

### Trade-offs

**Pros**:
- ✅ Eliminates duplicate charges (critical for trust and compliance)
- ✅ Safe retries after network failures
- ✅ Prevents race conditions from concurrent requests
- ✅ Required by PCI-DSS for payment reliability

**Cons**:
- ❌ Requires database storage for key-transaction mapping
- ❌ Key generation adds ~1-2ms overhead per request
- ❌ 24-hour key TTL requires cleanup job

**Risks**:
- ⚠️ **Key reuse with different parameters**: Raises IdempotencyError. Mitigation: Validate parameters match before reusing key.
- ⚠️ **Database failure**: Cannot generate/store keys. Mitigation: Cache keys in Redis with 24h TTL.

### When NOT to Use

- **Read-only operations** (GET requests are naturally idempotent)
- **Non-critical writes** (logging, analytics) where duplicates are acceptable
- **Internal async jobs** where job queue provides deduplication

### Related Patterns

- **Optimistic Locking**: Prevents race conditions at database level
- **Event Sourcing**: Append-only log naturally supports idempotency
- **CQRS**: Separate command (write) and query (read) paths

### Traceability

**Maps to**:
- Constitution principles: REL-001 (Reliability patterns)
- Quality gates: QG-004 (Production readiness)
- NFR categories: NFR-REL-001 (Idempotent operations)

---

## Practice: Daily Payment Reconciliation

**Category**: Financial Operations
**Applicability**: All systems processing payments
**Evidence Tier**: STRONG
**Source**: "Financial Systems Architecture" (IEEE, 2023), "Payment Reconciliation Best Practices" (NACHA)

### Description

Implement daily reconciliation between your internal ledger and external payment processor statements to detect discrepancies, catch errors, and ensure financial accuracy.

### Implementation

1. **Nightly batch reconciliation**:

```python
from datetime import datetime, timedelta

def reconcile_daily_payments():
    yesterday = datetime.now() - timedelta(days=1)

    # 1. Get internal ledger totals
    internal_total = Ledger.query.filter(
        Ledger.date == yesterday.date()
    ).sum(Ledger.amount)

    # 2. Get payment processor totals (e.g., Stripe)
    stripe_balance = stripe.BalanceTransaction.list(
        created={'gte': int(yesterday.timestamp())}
    )
    external_total = sum([txn.amount for txn in stripe_balance.data])

    # 3. Compare totals
    variance = abs(internal_total - external_total)
    variance_pct = (variance / internal_total) * 100 if internal_total else 0

    # 4. Alert if variance exceeds threshold
    if variance_pct > 0.01:  # 0.01% threshold
        send_alert(f"Reconciliation variance: {variance_pct:.4f}%")
        flag_for_manual_review(yesterday, variance)

    # 5. Log reconciliation result
    ReconciliationLog.create(
        date=yesterday,
        internal_total=internal_total,
        external_total=external_total,
        variance=variance,
        status='PASS' if variance_pct <= 0.01 else 'FAIL'
    )
```

2. **Exception handling workflow**:

```python
def investigate_discrepancy(date, variance):
    # Find missing or mismatched transactions
    internal_txns = get_internal_transactions(date)
    external_txns = get_external_transactions(date)

    missing_from_internal = external_txns - internal_txns
    missing_from_external = internal_txns - external_txns

    # Generate investigation report
    return {
        'missing_from_internal': list(missing_from_internal),
        'missing_from_external': list(missing_from_external),
        'action_required': True
    }
```

### Rationale

**Problem**: Payment processors may experience failures, bugs, or network issues causing missed transactions. Without reconciliation, financial records become inaccurate.

**Solution**: Daily reconciliation detects discrepancies early (within 24 hours), enabling quick resolution before errors compound.

**Evidence**: Financial institutions universally implement reconciliation; NACHA requires reconciliation for ACH processors.

### Trade-offs

**Pros**:
- ✅ Early detection of payment failures or processor bugs
- ✅ Audit trail for financial compliance (SOX, SOC 2)
- ✅ Prevents revenue leakage
- ✅ Builds customer trust (accurate billing)

**Cons**:
- ❌ Engineering overhead to build reconciliation system
- ❌ Nightly batch job increases infrastructure complexity
- ❌ Manual investigation required for discrepancies

**Risks**:
- ⚠️ **False positives**: Timing differences (settlement lag) trigger alerts. Mitigation: Use T+1 or T+2 settlement window.
- ⚠️ **Missed discrepancies**: Threshold too high. Mitigation: Use 0.01% threshold for high-value transactions.

### When NOT to Use

- **Low-volume systems** (<10 transactions/day): Manual review may suffice
- **Non-monetary transactions** (e.g., loyalty points): Lower criticality

### Related Patterns

- **Double-Entry Bookkeeping**: Ensures all transactions balanced at source
- **Event Sourcing**: Immutable audit trail simplifies reconciliation
- **CQRS**: Separate write path (payments) from read path (reconciliation)

### Traceability

**Maps to**:
- Constitution principles: CMP-002 (Audit trail), SEC-003 (Financial integrity)
- Quality gates: QG-005 (Financial accuracy)
- NFR categories: NFR-CMP-001 (Reconciliation process)

---

## Practice: AES-256 Encryption with Key Rotation

**Category**: Security
**Applicability**: All systems storing PAN (Primary Account Number) or sensitive financial data
**Evidence Tier**: AUTHORITATIVE
**Source**: PCI-DSS v4.0 Requirement 3.4, NIST SP 800-57 (Key Management)

### Description

Encrypt all stored cardholder data (PAN) using AES-256 with cryptoperiod-based key rotation to comply with PCI-DSS and minimize impact of key compromise.

### Implementation

1. **Encryption with AWS KMS**:

```python
import boto3
from cryptography.fernet import Fernet

kms_client = boto3.client('kms')

def encrypt_pan(pan, customer_id):
    # 1. Generate data encryption key (DEK) from KMS
    response = kms_client.generate_data_key(
        KeyId='alias/payment-data-key',  # Customer Master Key (CMK)
        KeySpec='AES_256'
    )

    plaintext_key = response['Plaintext']
    encrypted_dek = response['CiphertextBlob']

    # 2. Encrypt PAN with DEK
    cipher = Fernet(plaintext_key)
    encrypted_pan = cipher.encrypt(pan.encode())

    # 3. Store encrypted DEK alongside encrypted PAN
    PaymentData.create(
        customer_id=customer_id,
        encrypted_pan=encrypted_pan,
        encrypted_dek=encrypted_dek  # DEK encrypted by CMK
    )

    # 4. Clear plaintext key from memory
    del plaintext_key

def decrypt_pan(payment_data):
    # 1. Decrypt DEK using KMS
    response = kms_client.decrypt(
        CiphertextBlob=payment_data.encrypted_dek
    )
    plaintext_key = response['Plaintext']

    # 2. Decrypt PAN using DEK
    cipher = Fernet(plaintext_key)
    pan = cipher.decrypt(payment_data.encrypted_pan).decode()

    # 3. Clear plaintext key from memory
    del plaintext_key

    return pan
```

2. **Key rotation every 90 days**:

```python
def rotate_encryption_key():
    # 1. Generate new CMK version in KMS
    kms_client.enable_key_rotation(
        KeyId='alias/payment-data-key'
    )

    # 2. Re-encrypt all DEKs with new CMK (KMS handles automatically)
    # 3. Log rotation event for audit
    AuditLog.create(
        event='KEY_ROTATION',
        key_id='payment-data-key',
        timestamp=datetime.now()
    )
```

### Rationale

**Problem**: Stored PAN is a high-value target for attackers. Plaintext storage violates PCI-DSS and exposes customers to fraud.

**Solution**: AES-256 encryption renders stolen data useless without encryption keys. Key rotation limits blast radius of key compromise.

**Evidence**: PCI-DSS Req 3.4 mandates encryption; NIST recommends 90-day key rotation for high-value data.

### Trade-offs

**Pros**:
- ✅ PCI-DSS compliant (Req 3.4)
- ✅ Protects against database breaches
- ✅ HSM-backed key storage (KMS) prevents key extraction
- ✅ Automatic key rotation reduces operational burden

**Cons**:
- ❌ KMS API calls add latency (~10-50ms per decrypt)
- ❌ KMS costs: $1/month per CMK + $0.03 per 10k API requests
- ❌ Re-encryption required after key rotation (background job)

**Risks**:
- ⚠️ **Key deletion**: Accidental CMK deletion loses all data. Mitigation: 7-day CMK deletion window, backup keys.
- ⚠️ **KMS outage**: Cannot decrypt data. Mitigation: Cache decrypted DEKs (encrypted by backup key).

### When NOT to Use

- **Tokenization available**: Use tokenization (replaces PAN) instead of encryption
- **Last 4 digits only**: Truncation sufficient (no need to encrypt masked data)

### Related Patterns

- **Tokenization**: Replaces PAN with surrogate value (no decryption key needed)
- **Key Management Service**: Centralized key storage and rotation
- **Envelope Encryption**: Two-tier key hierarchy (CMK encrypts DEKs)

### Traceability

**Maps to**:
- Constitution principles: SEC-001 (Encryption at rest), CMP-001 (PCI compliance)
- Quality gates: QG-007 (Security validation)
- NFR categories: NFR-SEC-001 (Data encryption)

---

## Practice: Webhook Signature Verification

**Category**: Security
**Applicability**: All systems receiving webhooks from payment processors
**Evidence Tier**: AUTHORITATIVE
**Source**: Stripe Webhook Security (<https://stripe.com/docs/webhooks/signatures>), Adyen Webhooks

### Description

Verify webhook signatures to prevent attackers from forging payment notifications and triggering unauthorized actions (e.g., fulfilling orders without payment).

### Implementation

1. **Stripe signature verification**:

```python
import stripe
from flask import request, abort

@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.environ['STRIPE_WEBHOOK_SECRET']

    try:
        # Verify signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        # Invalid payload
        abort(400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        abort(401)

    # Process verified event
    handle_event(event)
    return '', 200
```

2. **PayPal signature verification**:

```python
from paypal.standard.ipn.models import PayPalIPN

@app.route('/webhooks/paypal', methods=['POST'])
def paypal_ipn():
    ipn = PayPalIPN(request.POST)

    if not ipn.verify():
        # Invalid signature
        abort(401)

    # Process verified IPN
    handle_paypal_ipn(ipn)
    return '', 200
```

### Rationale

**Problem**: Attackers can send fake webhook requests to `/webhooks/payment` endpoint, triggering order fulfillment without actual payment.

**Solution**: Signature verification ensures webhook originated from legitimate payment processor using HMAC with shared secret.

**Evidence**: Stripe, PayPal, Adyen all require signature verification for production webhooks.

### Trade-offs

**Pros**:
- ✅ Prevents webhook forgery attacks
- ✅ Required for PCI compliance (secure communication)
- ✅ Zero performance overhead (signature check <1ms)
- ✅ No additional infrastructure required

**Cons**:
- ❌ Webhook secret must be securely stored (environment variable, secrets manager)
- ❌ Signature verification failure requires debugging (clock skew, wrong secret)

**Risks**:
- ⚠️ **Exposed webhook secret**: Attacker can forge webhooks. Mitigation: Rotate secret, store in AWS Secrets Manager.
- ⚠️ **Clock skew**: Timestamp validation fails. Mitigation: Allow 5-minute tolerance window.

### When NOT to Use

- **Internal webhooks**: Between services you control (still use authentication)
- **Public webhooks**: User-facing webhooks (use API keys instead)

### Related Patterns

- **HMAC Authentication**: Webhook signature algorithm
- **API Keys**: Alternative authentication for synchronous APIs
- **OAuth 2.0**: For user-delegated authorization

### Traceability

**Maps to**:
- Constitution principles: SEC-002 (Authentication), SEC-004 (API security)
- Quality gates: QG-007 (Security validation)
- NFR categories: NFR-SEC-002 (Webhook security)

---

## Maintenance

**Last Updated**: 2025-01-10
**Reviewed By**: academic-researcher-ai, standards-researcher-ai
**Evidence Quality**: AUTHORITATIVE (Stripe docs), STRONG (IEEE papers, NACHA guidelines)
**Source URLs**:
- <https://stripe.com/docs/api/idempotent_requests>
- <https://stripe.com/docs/webhooks/signatures>
- IEEE Xplore: "Financial Systems Architecture" (2023)
- NIST SP 800-57: Key Management Recommendations

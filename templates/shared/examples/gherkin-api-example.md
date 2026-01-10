# Gherkin API Example

This example demonstrates how to write acceptance criteria in Gherkin format for API features.

## User Story: Payment Processing

**As a** customer
**I want to** process payments securely
**So that** I can complete purchases

**Priority**: P1a
**Concept Reference**: EPIC-001.F03.S01

---

## Acceptance Criteria (Gherkin)

<!--
  IMPORTANT: Executable Gherkin format for BDD frameworks (Cucumber, Behave, SpecFlow).
  Each scenario has a unique ID (AS-NNN) for traceability to tasks.md.
-->

```gherkin
Feature: Payment Processing

Process credit card payments with validation, fraud detection, and receipt generation.

Scenario: AS-1A - Successful payment with credit card [HAPPY_PATH] [Confidence: 0.95]
  Given user is authenticated with email "customer@example.com"
  And payment method "card_4242424242424242" is saved
  And account balance is 0.00 USD
  When I POST /api/payments with:
    | amount          | 5000              |
    | currency        | usd               |
    | payment_method  | card_4242424242424242 |
    | description     | Order #12345      |
  Then response status is 200
  And response.id matches /^pay_[A-Za-z0-9]{24}$/
  And response.status is "succeeded"
  And response.amount is 5000
  And response.currency is "usd"
  And response.payment_method.last4 is "4242"
  And response.receipt_url matches /^https:\/\/receipts\.stripe\.com\//
  And payment confirmation email is sent to "customer@example.com"
  And transaction is recorded in ledger with type "charge"
  And processing time is less than 2000ms

Scenario: AS-1B - Failed payment with insufficient funds [ERROR_PATH] [Confidence: 0.92]
  Given user is authenticated with email "customer@example.com"
  And payment method "card_4000000000009995" is saved (insufficient funds card)
  When I POST /api/payments with:
    | amount          | 5000              |
    | currency        | usd               |
    | payment_method  | card_4000000000009995 |
  Then response status is 402
  And response.error.code is "card_declined"
  And response.error.decline_code is "insufficient_funds"
  And response.error.message is "Your card has insufficient funds."
  And no charge is created
  And no confirmation email is sent
  And failed attempt is logged with reason "insufficient_funds"
  And user is notified to update payment method

Scenario: AS-1C - Duplicate payment prevention (idempotency) [BOUNDARY] [Confidence: 0.88]
  Given user is authenticated with email "customer@example.com"
  And payment method "card_4242424242424242" is saved
  And previous payment "pay_abc123" was created with idempotency key "order-12345"
  When I POST /api/payments with:
    | amount          | 5000              |
    | currency        | usd               |
    | payment_method  | card_4242424242424242 |
    | idempotency_key | order-12345       |
  Then response status is 200
  And response.id is "pay_abc123"
  And response.status is "succeeded"
  And no new charge is created
  And no duplicate email is sent
  And idempotency cache hit is logged

Scenario: AS-1D - Payment with expired card [ERROR_PATH] [Confidence: 0.85]
  Given user is authenticated with email "customer@example.com"
  And payment method "card_4000000000000069" is saved (expired card)
  When I POST /api/payments with:
    | amount          | 5000              |
    | currency        | usd               |
    | payment_method  | card_4000000000000069 |
  Then response status is 402
  And response.error.code is "card_declined"
  And response.error.decline_code is "expired_card"
  And response.error.message is "Your card has expired."
  And no charge is created
  And failed attempt is logged with reason "expired_card"
  And user is prompted to update card expiration date

Scenario: AS-1E - Payment amount validation (zero amount) [BOUNDARY] [Confidence: 0.80]
  Given user is authenticated with email "customer@example.com"
  And payment method "card_4242424242424242" is saved
  When I POST /api/payments with:
    | amount          | 0                 |
    | currency        | usd               |
    | payment_method  | card_4242424242424242 |
  Then response status is 400
  And response.error.code is "amount_invalid"
  And response.error.message is "Amount must be at least $0.50 usd"
  And no charge is created
  And validation error is logged

Scenario: AS-1F - Payment amount validation (exceeds maximum) [BOUNDARY] [Confidence: 0.75]
  Given user is authenticated with email "customer@example.com"
  And payment method "card_4242424242424242" is saved
  When I POST /api/payments with:
    | amount          | 100000000         |
    | currency        | usd               |
    | payment_method  | card_4242424242424242 |
  Then response status is 400
  And response.error.code is "amount_too_large"
  And response.error.message is "Amount cannot exceed $999,999.99 usd"
  And no charge is created
  And validation error is logged

Scenario: AS-1G - Fraud detection triggers review [SECURITY] [Confidence: 0.90]
  Given user is authenticated with email "customer@example.com"
  And payment method "card_4242424242424242" is saved
  And user has made 3 payments in the last 5 minutes
  And IP address is from a high-risk country
  When I POST /api/payments with:
    | amount          | 10000             |
    | currency        | usd               |
    | payment_method  | card_4242424242424242 |
  Then response status is 202
  And response.id matches /^pay_[A-Za-z0-9]{24}$/
  And response.status is "requires_review"
  And response.review_reason is "suspected_fraud"
  And payment is held for manual review
  And fraud alert is sent to security team
  And user receives "payment under review" email
  And review must be completed within 24 hours

Scenario: AS-1H - Refund successful payment [ALT_PATH] [Confidence: 0.85]
  Given user is authenticated with email "customer@example.com"
  And payment "pay_abc123" was successful with amount 5000 USD
  And payment was created less than 90 days ago
  When I POST /api/refunds with:
    | payment         | pay_abc123        |
    | amount          | 5000              |
    | reason          | requested_by_customer |
  Then response status is 200
  And response.id matches /^re_[A-Za-z0-9]{24}$/
  And response.status is "succeeded"
  And response.amount is 5000
  And response.payment is "pay_abc123"
  And refund confirmation email is sent to "customer@example.com"
  And refund is recorded in ledger with type "refund"
  And original payment status is updated to "refunded"
```

---

## Key Patterns in This Example

### 1. Feature Block
Groups all payment-related scenarios under a single feature.

### 2. Scenario Structure
- **ID**: AS-1A, AS-1B, etc. (unique identifier for traceability)
- **Description**: Brief summary of what's being tested
- **Classification**: [HAPPY_PATH], [ERROR_PATH], [BOUNDARY], [SECURITY], [ALT_PATH]
- **Confidence**: 0.0-1.0 score indicating importance (0.90+ = critical)

### 3. Given Steps (Setup)
- Specific initial states with actual data
- Use concrete values: `user "customer@example.com"` not `user exists`
- Include all prerequisites needed for the test

### 4. When Steps (Action)
- HTTP method + endpoint clearly stated
- Data tables for request body (POST, PUT, PATCH)
- Structured format makes it easy to generate test code

### 5. Then Steps (Assertions)
- Response status code first
- Field-level assertions with specific values
- Nested field checks: `response.error.code`
- Timing expectations: `less than 2000ms`
- Side effects: emails, logging, state changes
- Negative assertions: `no charge is created`

### 6. Entity-Specific Patterns
For payment features:
- **Given**: Payment method with test card numbers
- **When**: POST /api/payments with amount, currency, payment_method
- **Then**: Status, payment ID format, success indicators, emails, ledger records

### 7. Edge Cases Covered
- Happy path (AS-1A)
- Error paths (AS-1B, AS-1D, AS-1E, AS-1F)
- Boundary conditions (AS-1C, AS-1E, AS-1F)
- Security scenarios (AS-1G)
- Alternative flows (AS-1H - refunds)

### 8. Testability
Each scenario can be directly implemented as a test using:
- **Cucumber** (Ruby, JavaScript)
- **Behave** (Python)
- **SpecFlow** (.NET)
- **Pytest-BDD** (Python)

Example Behave implementation:
```python
@when('I POST /api/payments with:')
def step_post_payment(context):
    data = {row['key']: row['value'] for row in context.table}
    context.response = requests.post('/api/payments', json=data)

@then('response status is {code:d}')
def step_response_status(context, code):
    assert context.response.status_code == code

@then('response.status is "{status}"')
def step_response_status_field(context, status):
    assert context.response.json()['status'] == status
```

---

## Comparison: Old vs New Format

### Old Table Format (BAD)
```markdown
| AS-1A | HAPPY_PATH | user authenticated, card saved | POST /api/payments | 200, payment successful | YES | 0.95 |
```

**Problems**:
- Not executable by BDD frameworks
- Missing detailed request/response structure
- No timing expectations
- No side effects specified
- Hard to generate actual test code

### New Gherkin Format (GOOD)
```gherkin
Scenario: AS-1A - Successful payment [HAPPY_PATH] [Confidence: 0.95]
  Given user is authenticated with email "customer@example.com"
  And payment method "card_4242424242424242" is saved
  When I POST /api/payments with:
    | amount          | 5000              |
    | currency        | usd               |
    | payment_method  | card_4242424242424242 |
  Then response status is 200
  And response.status is "succeeded"
  And payment confirmation email is sent
  And processing time is less than 2000ms
```

**Advantages**:
- Directly executable by Cucumber, Behave, SpecFlow
- Clear API contract (endpoint, method, request structure)
- Detailed assertions (status, fields, timing)
- Side effects explicit (email, logging)
- Can generate test code automatically
- Includes state setup and multiple assertions

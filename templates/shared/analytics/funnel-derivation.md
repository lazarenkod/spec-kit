# Funnel Derivation from Acceptance Scenarios

This document describes the algorithm for automatically deriving analytics funnels from acceptance scenarios (AS-xxx) in feature specifications.

## Purpose

In Spec-Driven Development, acceptance scenarios (AS-xxx) describe user actions and expected outcomes. These scenarios naturally map to analytics funnels, which track user progression through multi-step flows.

**Example**: A signup flow with 3 acceptance scenarios naturally becomes a 3-step funnel.

## Algorithm

```text
INPUT: List of AS-xxx acceptance scenarios from spec.md
OUTPUT: Funnel definitions for analytics provider

ALGORITHM:
1. Group AS-xxx scenarios by user journey (infer from FR-xxx or feature name)
2. For each journey:
   a. Extract sequential steps from AS descriptions (Given → When → Then)
   b. Map each step to an analytics event name
   c. Identify funnel start (first AS) and end (last AS)
   d. Define target conversion rates based on industry benchmarks
3. Generate funnel configuration for analytics provider (PostHog, Mixpanel, Amplitude)
```

## Step 1: Group by User Journey

### Example: Signup Journey

```markdown
**Acceptance Scenarios**:
- AS-1A: User can view landing page
- AS-1B: User can view signup form
- AS-1C: User can submit signup form
- AS-1D: User receives confirmation email
```

These are grouped as "Signup Journey" because they share FR-001 (User Authentication).

### Example: Checkout Journey

```markdown
**Acceptance Scenarios**:
- AS-3A: User can add item to cart
- AS-3B: User can view cart
- AS-3C: User can enter shipping address
- AS-3D: User can enter payment info
- AS-3E: User can complete purchase
```

These are grouped as "Checkout Journey" because they share FR-003 (E-commerce Checkout).

## Step 2: Extract Steps and Map to Events

### Mapping Rules

| AS Step Type | Event Type | Event Name Pattern |
|--------------|------------|-------------------|
| "User can view [page]" | Page view | `page_viewed` with `path` property |
| "User can click [button]" | Button click | `button_clicked` with `button_id` property |
| "User can submit [form]" | Form submission | `form_submitted` with `form_id` property |
| "User can complete [action]" | Action completed | `[action]_completed` |
| "User receives [notification]" | Notification received | `[notification]_received` |

### Example: Signup Journey Mapping

| AS | Given/When/Then | Event Name | Properties |
|----|-----------------|------------|------------|
| AS-1A | User visits landing page | `page_viewed` | `{ path: "/" }` |
| AS-1B | User navigates to signup form | `page_viewed` | `{ path: "/signup" }` |
| AS-1C | User submits signup form | `user_signed_up` | `{ method: "email" }` |
| AS-1D | System sends confirmation email | `confirmation_email_sent` | `{ type: "signup" }` |

## Step 3: Define Target Conversion Rates

Use industry benchmarks to set target conversion rates:

### B2C SaaS Benchmarks

| Funnel | Step | Typical Conversion | Good Conversion | Excellent Conversion |
|--------|------|-------------------|-----------------|---------------------|
| **Signup** | Landing → Signup Page | 40% | 50% | 60% |
| **Signup** | Signup Page → Submit | 15% | 25% | 35% |
| **Signup** | Submit → Confirm Email | 60% | 70% | 80% |
| **Onboarding** | Signup → First Action | 30% | 50% | 70% |
| **Checkout** | Cart → Shipping | 60% | 70% | 80% |
| **Checkout** | Shipping → Payment | 70% | 80% | 90% |
| **Checkout** | Payment → Complete | 85% | 90% | 95% |

### B2B SaaS Benchmarks

| Funnel | Step | Typical Conversion | Good Conversion | Excellent Conversion |
|--------|------|-------------------|-----------------|---------------------|
| **Free Trial Signup** | Landing → Form | 3% | 5% | 10% |
| **Free Trial → Paid** | Trial Start → Conversion | 15% | 25% | 40% |

### E-commerce Benchmarks

| Funnel | Step | Typical Conversion | Good Conversion | Excellent Conversion |
|--------|------|-------------------|-----------------|---------------------|
| **Product Discovery** | Homepage → Product Page | 30% | 40% | 50% |
| **Add to Cart** | Product Page → Cart | 2% | 4% | 8% |
| **Checkout** | Cart → Purchase | 20% | 35% | 50% |

## Step 4: Generate Funnel Configuration

### PostHog Funnel Definition

```typescript
// Auto-generated from AS-1A, AS-1B, AS-1C
const signupFunnel = {
  name: 'Signup Journey',
  description: 'User progression from landing page to signup confirmation',
  steps: [
    {
      event: 'page_viewed',
      properties: [{ key: 'path', value: '/', type: 'equals' }],
      name: 'Landing Page'
    },
    {
      event: 'page_viewed',
      properties: [{ key: 'path', value: '/signup', type: 'equals' }],
      name: 'Signup Page'
    },
    {
      event: 'user_signed_up',
      name: 'Signup Complete'
    }
  ],
  target_conversion: {
    'Landing Page → Signup Page': 0.50,  // 50%
    'Signup Page → Signup Complete': 0.25 // 25%
  }
}
```

### Mixpanel Funnel Definition

```javascript
// Auto-generated from AS-3A, AS-3B, AS-3C, AS-3D, AS-3E
mixpanel.track_funnel('Checkout Journey', [
  { event: 'item_added_to_cart' },
  { event: 'cart_viewed' },
  { event: 'shipping_address_entered' },
  { event: 'payment_info_entered' },
  { event: 'purchase_completed' }
])
```

### Amplitude Funnel Definition

```javascript
// Auto-generated from AS-1A, AS-1B, AS-1C
const signupFunnel = {
  funnel_name: 'Signup Journey',
  steps: [
    { event_type: 'page_viewed', filters: [{ prop: 'path', op: 'is', value: '/' }] },
    { event_type: 'page_viewed', filters: [{ prop: 'path', op: 'is', value: '/signup' }] },
    { event_type: 'user_signed_up' }
  ]
}
```

## Example: Complete Derivation

### Input: Feature Specification

```markdown
## FR-001: User Authentication

### AS-1A: View landing page
**Given** user visits the homepage
**When** page loads
**Then** landing page is displayed with signup CTA

### AS-1B: Navigate to signup
**Given** user is on landing page
**When** user clicks "Sign Up" button
**Then** signup form is displayed

### AS-1C: Submit signup form
**Given** user is on signup form
**When** user enters email, password, and clicks "Create Account"
**Then** account is created and user is logged in
```

### Output: Funnel Definition

```yaml
funnel:
  name: Signup Journey
  description: Derived from FR-001 acceptance scenarios
  feature_reference: FR-001

  steps:
    - name: Landing Page View
      as_reference: AS-1A
      event: page_viewed
      properties:
        path: "/"
      target_conversion: 100% # Baseline

    - name: Signup Page View
      as_reference: AS-1B
      event: page_viewed
      properties:
        path: "/signup"
      target_conversion: 50% # 50% of landing page visitors

    - name: Signup Complete
      as_reference: AS-1C
      event: user_signed_up
      properties: {}
      target_conversion: 25% # 25% of landing page visitors, 50% of signup page visitors

  alerts:
    - metric: step_2_conversion
      threshold: < 40%
      action: Send Slack notification to #product

    - metric: step_3_conversion
      threshold: < 20%
      action: Email product team
```

## Funnel Visualization

```text
Signup Journey (FR-001)

┌─────────────────────┐
│  Landing Page View  │  AS-1A
│    (page_viewed)    │  100% baseline
└──────────┬──────────┘
           │ 50% conversion target
           ↓
┌─────────────────────┐
│  Signup Page View   │  AS-1B
│    (page_viewed)    │  50% of landing
└──────────┬──────────┘
           │ 50% conversion target
           ↓
┌─────────────────────┐
│   Signup Complete   │  AS-1C
│  (user_signed_up)   │  25% of landing (50% of signup page)
└─────────────────────┘
```

## Multi-Journey Funnels

Some features have multiple journeys that should be tracked separately:

### Example: Social Platform

```markdown
FR-002: User can create and share content

Journeys:
1. **Create Journey**: AS-2A → AS-2B → AS-2C (create post)
2. **Share Journey**: AS-2D → AS-2E (share post)
3. **Engagement Journey**: AS-2F → AS-2G (like/comment)
```

Each journey becomes a separate funnel.

## Conditional Steps

Some funnels have conditional steps (e.g., optional signup methods):

```markdown
AS-1C-1: User can sign up with email
AS-1C-2: User can sign up with Google OAuth
AS-1C-3: User can sign up with GitHub OAuth
```

**Handling**: Create a funnel with branching:

```yaml
funnel:
  name: Signup Journey
  steps:
    - name: Landing Page
      event: page_viewed
      properties: { path: "/" }

    - name: Signup Page
      event: page_viewed
      properties: { path: "/signup" }

    - name: Signup Complete
      event: user_signed_up
      # This event has multiple triggers (email, google, github)
      # Track them all as one funnel step, but segment by 'method' property
```

## Alerts and Monitoring

Auto-generate alerts based on conversion drop-offs:

```yaml
alerts:
  - name: Signup Conversion Drop
    condition: step_2_conversion < 40%  # Below benchmark
    severity: warning
    action: Slack #product-alerts

  - name: Signup Conversion Critical
    condition: step_2_conversion < 30%  # Severely below benchmark
    severity: critical
    action: PagerDuty
```

## Usage in Commands

### `/speckit.specify`

During specification generation:
1. Parse AS-xxx scenarios
2. Generate Event Schema table
3. Group AS by journey
4. Store journey metadata for `/speckit.plan`

### `/speckit.plan`

During planning:
1. Read Event Schema from spec.md
2. Apply funnel derivation algorithm
3. Generate § Analytics Monitoring Plan with funnels
4. Include target conversion rates

### `/speckit.tasks`

During task generation:
1. Read funnels from plan.md
2. Generate T2f-07 task: "Set up analytics dashboards"
3. Include funnel creation as sub-task

## Resources

- [PostHog Funnels Docs](https://posthog.com/docs/user-guides/funnels)
- [Mixpanel Funnels](https://help.mixpanel.com/hc/en-us/articles/115004561246)
- [Amplitude Funnels](https://help.amplitude.com/hc/en-us/articles/231275508)
- [Conversion Benchmarks (Mixpanel)](https://mixpanel.com/blog/conversion-benchmarks/)

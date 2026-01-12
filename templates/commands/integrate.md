---
name: integrate
description: Quick integration with common third-party services
version: 1.0.0
persona: developer-agent
skills:
  - integration-wizard
inputs:
  service:
    type: string
    required: true
    description: Service to integrate (e.g., stripe, clerk, resend)
  category:
    type: enum
    options: [auth, payments, email, analytics, storage, database, search, ai]
    required: false
    description: Service category (helps disambiguate)
outputs:
  - src/lib/integrations/{service}.ts
  - docs/integrations/{service}.md
  - .env.example (updated)
quality_gates:
  - name: env_configured
    condition: "all_required_env_vars_present"
    severity: error
  - name: smoke_test_passed
    condition: "integration_imports_without_error"
    severity: warning
handoffs:
  - label: Continue Implementation
    agent: speckit.implement
    condition: "integration_complete"
claude_code:
  model: sonnet
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 4000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 8000
        max_parallel: 3
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 16000
        max_parallel: 6
        batch_delay: 1500
        wave_overlap_threshold: 0.65
  cache_hierarchy: full
  orchestration:
    max_parallel: 6
    fail_fast: true
    wave_overlap:
      enabled: true
      overlap_threshold: 0.65
  subagents:
    # Wave 1: Analysis (parallel)
    - role: service-analyzer
      role_group: ANALYSIS
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Analyze selected third-party service for integration.
        Identify: SDK package, required environment variables.
        Determine webhook requirements and endpoints.
        Check for existing integrations in src/lib/integrations/.
        Output: service analysis with configuration requirements.

    - role: api-designer
      role_group: BACKEND
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Design API wrapper interface for the service.
        Define typed operations based on service capabilities.
        Plan error handling with typed error classes.
        Design retry logic for transient failures.
        Output: API design specification.

    # Wave 2: Analytics Provider Selection (conditional)
    - role: analytics-provider-selector
      role_group: INTEGRATION
      parallel: false
      depends_on: [service-analyzer]
      priority: 25
      model_override: haiku
      prompt: |
        CONDITIONAL: Only execute if analytics enabled AND product analytics selected AND provider not set.

        1. Read /memory/constitution.md § Project Settings
        2. Check: analytics_enabled == true AND "product" in analytics_types AND analytics_provider is empty
        3. If TRUE:
           a. Ask user to select product analytics provider using AskUserQuestion tool
           b. Options: PostHog (self-hosted or cloud), Mixpanel (cloud), Amplitude (cloud), None (skip)
           c. Update constitution with selected provider
           d. Add SDK dependencies to package.json/requirements.txt/go.mod
           e. If PostHog self-hosted selected, update docker-compose.yml
        4. If FALSE:
           Skip provider selection

    # Wave 3: Code Generation (after analysis and provider selection)
    - role: contract-generator
      role_group: BACKEND
      parallel: true
      depends_on: [service-analyzer, api-designer, analytics-provider-selector]
      priority: 30
      model_override: sonnet
      prompt: |
        Generate integration code based on analysis and design.
        Create SDK wrapper: src/lib/integrations/{service}.ts.
        Add webhook handler if needed: src/app/api/webhooks/{service}/route.ts.
        Update .env.example with required variables.
        Generate documentation: docs/integrations/{service}.md.
        Verify TypeScript compiles and imports work.
flags:
  max_model: "--max-model <opus|sonnet|haiku>"  # Override model cap
---

# /speckit.integrate

## Purpose

Quickly set up integrations with common third-party services including authentication, payments, email, analytics, storage, and AI. Each integration includes SDK setup, environment configuration, error handling, and usage examples.

## When to Use

- Adding authentication to your app
- Setting up payment processing
- Integrating email services
- Adding analytics tracking
- Connecting to storage/database services
- Adding AI capabilities

## Integration Catalog

```
┌─────────────────────────────────────────────────────────────────┐
│                    Available Integrations                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AUTH                    PAYMENTS              EMAIL             │
│  ├── Clerk              ├── Stripe            ├── Resend        │
│  ├── Auth0              ├── Paddle            ├── SendGrid      │
│  ├── Supabase Auth      └── LemonSqueezy      └── Postmark      │
│  └── Firebase Auth                                               │
│                                                                  │
│  ANALYTICS              STORAGE               DATABASE           │
│  ├── PostHog            ├── AWS S3            ├── Supabase      │
│  ├── Mixpanel           ├── Cloudflare R2     ├── PlanetScale   │
│  └── Amplitude          └── Supabase Storage  └── Neon          │
│                                                                  │
│  SEARCH                 AI                                       │
│  ├── Algolia            ├── OpenAI                              │
│  ├── Meilisearch        ├── Anthropic                           │
│  └── Typesense          └── Replicate                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      /speckit.integrate                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. SELECT                                                       │
│     └── Choose service from catalog (interactive)                │
│                                                                  │
│  2. CONFIGURE                                                    │
│     ├── Generate .env template                                   │
│     ├── Guide API key creation                                   │
│     └── Set up webhook endpoints (if needed)                     │
│                                                                  │
│  3. GENERATE                                                     │
│     ├── SDK wrapper with TypeScript types                        │
│     ├── Error handling utilities                                 │
│     ├── Common operation helpers                                 │
│     └── Webhook handlers (if needed)                             │
│                                                                  │
│  4. DOCUMENT                                                     │
│     ├── Setup instructions                                       │
│     ├── Usage examples                                           │
│     └── Troubleshooting guide                                    │
│                                                                  │
│  5. TEST                                                         │
│     ├── Import verification                                      │
│     └── Smoke test (if credentials available)                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Command Execution

### Step 1: Select Service

```yaml
# Interactive selection
selection:
  service: "{{service}}"
  category: "{{category}}"

  details:
    name: "{{full_service_name}}"
    description: "{{what_it_does}}"
    pricing: "{{pricing_summary}}"
    docs: "{{documentation_url}}"
```

### Step 2: Environment Configuration

```bash
# Required environment variables
{{ENV_VAR_1}}=        # {{description}}
{{ENV_VAR_2}}=        # {{description}}

# How to obtain:
# 1. Create account at {{provider_url}}
# 2. Navigate to {{settings_path}}
# 3. Generate API keys
# 4. Copy values to .env.local
```

### Step 3: Generate Integration Code

Each integration generates:

1. **SDK Wrapper** (`src/lib/integrations/{service}.ts`)
   - Client initialization with validation
   - Type-safe operation wrappers
   - Error handling with typed errors
   - Retry logic for transient failures

2. **Webhook Handler** (if applicable)
   - Signature verification
   - Event routing
   - Idempotency handling

3. **Environment Updates**
   - `.env.example` updated with new variables
   - `.env.local` template for development

### Step 4: Documentation

```markdown
# {{Service}} Integration

## Quick Start
1. Get API key from {{provider}}
2. Add to `.env.local`
3. Import and use

## Usage Examples
[Generated code examples]

## Troubleshooting
[Common issues and solutions]
```

### Step 5: Verification

```yaml
verification:
  - check: "Package installed"
    command: "npm ls {{package}}"

  - check: "Environment configured"
    validate: "required env vars present"

  - check: "Import works"
    command: "node -e \"require('./src/lib/integrations/{{service}}')\""

  - check: "TypeScript compiles"
    command: "npx tsc --noEmit"
```

## Integration Examples

### Authentication (Clerk)

```bash
speckit integrate clerk
```

Generates:
- `src/lib/integrations/clerk.ts` - Middleware and hooks
- `src/middleware.ts` - Auth middleware
- `src/components/auth-button.tsx` - Sign in/out component

### Payments (Stripe)

```bash
speckit integrate stripe
```

Generates:
- `src/lib/integrations/stripe.ts` - Stripe client and helpers
- `src/app/api/webhooks/stripe/route.ts` - Webhook handler
- `src/app/api/checkout/route.ts` - Checkout session API

### Email (Resend)

```bash
speckit integrate resend
```

Generates:
- `src/lib/integrations/resend.ts` - Email client
- `src/emails/welcome.tsx` - Email template (React Email)
- `src/emails/index.ts` - Email exports

### Analytics (PostHog)

```bash
speckit integrate posthog
```

Generates:
- `src/lib/integrations/posthog.ts` - PostHog client
- `src/providers/posthog-provider.tsx` - React provider
- Event tracking helpers

### AI (Anthropic)

```bash
speckit integrate anthropic
```

Generates:
- `src/lib/integrations/anthropic.ts` - Anthropic client
- Streaming helpers
- Token counting utilities

## Analytics Provider Selection

**Condition**: Only prompt if `analytics_enabled == true` AND `"product"` in `analytics_types` AND `analytics_provider` is empty in constitution.

**Purpose**: Let user select product analytics provider and configure dependencies.

### Provider Options

| Provider | Hosting | Free Tier | Best For |
|----------|---------|-----------|----------|
| **PostHog** | Self-hosted or Cloud | Unlimited events (self-hosted) | Privacy-first, full control, session recording |
| **Mixpanel** | Cloud | 20M events/month | Strong funnel analysis, cohorts |
| **Amplitude** | Cloud | 10M events/month | Retention analysis, behavioral cohorts |

### Prompt

```
🔍 **Analytics Configuration**

This project has product analytics enabled. Please select a provider:

**Product Analytics** (tracks user behavior events, funnels):
- [ ] PostHog (self-hosted or cloud)
- [ ] Mixpanel (cloud, free tier: 20M events/month)
- [ ] Amplitude (cloud, free tier: 10M events/month)
- [ ] None (skip for now)

**Note**: Selection will update constitution and add SDK dependencies.
```

### After Selection

1. **Update Constitution**: Write `analytics_provider` to `/memory/constitution.md` § Project Settings
2. **Add SDK Dependencies**:
   - **PostHog**: `npm install posthog-js` or `pip install posthog` or `go get github.com/posthog/posthog-go`
   - **Mixpanel**: `npm install mixpanel-browser` or `pip install mixpanel`
   - **Amplitude**: `npm install @amplitude/analytics-browser` or `pip install amplitude-analytics`
3. **Update Docker Compose** (if PostHog self-hosted):
   - Add PostHog service from `templates/shared/observability-stack.md`
4. **Report to User**:
   - "Product analytics provider set to [provider]"
   - "Run `/speckit.staging` to provision analytics infrastructure"

## Output Structure

```
src/
├── lib/
│   └── integrations/
│       └── {{service}}.ts      # SDK wrapper
├── app/
│   └── api/
│       └── webhooks/
│           └── {{service}}/
│               └── route.ts    # Webhook handler (if needed)
└── components/
    └── {{service}}/            # UI components (if applicable)

docs/
└── integrations/
    └── {{service}}.md          # Integration docs

.env.example                    # Updated with new vars
```

## Quality Gates

| Gate | Condition | Severity |
|------|-----------|----------|
| Env Configured | All required env vars present | Error |
| Package Installed | npm package available | Error |
| Types Valid | TypeScript compiles | Warning |
| Smoke Test | Basic import works | Warning |

## Integration Best Practices

### Error Handling

```typescript
// All integrations include typed errors
import { {{Service}}Error } from '@/lib/integrations/{{service}}';

try {
  await {{operation}}();
} catch (error) {
  if (error instanceof {{Service}}Error) {
    switch (error.code) {
      case 'rate_limited':
        // Handle rate limiting
        break;
      case 'invalid_credentials':
        // Handle auth error
        break;
    }
  }
}
```

### Environment Validation

```typescript
// Validated at import time
// src/lib/integrations/{{service}}.ts

const requiredEnvVars = ['{{ENV_1}}', '{{ENV_2}}'];
for (const v of requiredEnvVars) {
  if (!process.env[v]) {
    throw new Error(`Missing required environment variable: ${v}`);
  }
}
```

### Type Safety

```typescript
// All operations are fully typed
import type { {{ServiceTypes}} } from '@/lib/integrations/{{service}}';

const result: {{ResultType}} = await {{operation}}({
  // TypeScript autocomplete here
});
```

## Anti-Patterns

- Hardcoding API keys in source code
- Not handling rate limits
- Missing webhook signature verification
- Not logging integration errors
- Exposing server-only keys to client
- Not using environment variables

## Integration Points

| Command | Integration |
|---------|-------------|
| `/speckit.implement` | Can trigger integrate for dependencies |
| `/speckit.ship` | Verifies integrations configured |
| `/speckit.monitor` | Tracks integration API calls |

## Usage

```bash
# Interactive mode
speckit integrate

# Specify service
speckit integrate stripe

# Specify category
speckit integrate --category auth

# List available integrations
speckit integrate --list
```

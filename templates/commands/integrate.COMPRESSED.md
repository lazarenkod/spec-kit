---
description: Quick integration with common third-party services
persona: developer-agent
skills: [integration-wizard]
inputs:
  service: { type: string, required: true, description: "Service to integrate (stripe, clerk, resend)" }
  category: { type: enum, options: [auth, payments, email, analytics, storage, database, search, ai], required: false }
outputs:
  - src/lib/integrations/{service}.ts
  - docs/integrations/{service}.md
  - .env.example (updated)
handoffs:
  - label: Continue Implementation
    agent: speckit.implement
    condition: integration_complete
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 4000
---

## Input
```text
$ARGUMENTS
```

---

## Purpose

Quick setup for third-party service integrations: SDK setup, environment config, error handling, usage examples.

---

## Integration Catalog

| AUTH | PAYMENTS | EMAIL |
|------|----------|-------|
| Clerk, Auth0, Supabase Auth, Firebase Auth | Stripe, Paddle, LemonSqueezy | Resend, SendGrid, Postmark |

| ANALYTICS | STORAGE | DATABASE |
|-----------|---------|----------|
| PostHog, Mixpanel, Amplitude | AWS S3, Cloudflare R2, Supabase Storage | Supabase, PlanetScale, Neon |

| SEARCH | AI |
|--------|------|
| Algolia, Meilisearch, Typesense | OpenAI, Anthropic, Replicate |

---

## Workflow (5 Steps)

### Step 1: Select Service

```yaml
selection:
  service: "{{service}}"
  category: "{{category}}"
  details: { name, description, pricing, docs_url }
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

```text
1. SDK Wrapper (src/lib/integrations/{service}.ts):
   - Client initialization with validation
   - Type-safe operation wrappers
   - Error handling with typed errors
   - Retry logic for transient failures

2. Webhook Handler (if applicable):
   - Signature verification
   - Event routing
   - Idempotency handling

3. Environment Updates:
   - .env.example updated
   - .env.local template
```

### Step 4: Documentation

```markdown
# {{Service}} Integration

## Quick Start
1. Get API key from {{provider}}
2. Add to `.env.local`
3. Import and use

## Usage Examples | ## Troubleshooting
```

### Step 5: Verification

```yaml
checks:
  - "Package installed: npm ls {{package}}"
  - "Environment configured: required env vars present"
  - "Import works: node -e \"require('./src/lib/integrations/{{service}}')\""
  - "TypeScript compiles: npx tsc --noEmit"
```

---

## Output Structure

```text
src/lib/integrations/{{service}}.ts  # SDK wrapper
src/app/api/webhooks/{{service}}/    # Webhook handler (if needed)
docs/integrations/{{service}}.md     # Documentation
.env.example                         # Updated
```

---

## Quality Gates

| Gate | Condition | Severity |
|------|-----------|----------|
| Env Configured | All required env vars present | Error |
| Package Installed | npm package available | Error |
| Types Valid | TypeScript compiles | Warning |
| Smoke Test | Basic import works | Warning |

---

## Anti-Patterns

- Hardcoding API keys in source code
- Not handling rate limits
- Missing webhook signature verification
- Exposing server-only keys to client
- Not logging integration errors

---

## Usage

```bash
speckit integrate           # Interactive mode
speckit integrate stripe    # Specify service
speckit integrate --category auth  # Filter by category
speckit integrate --list    # List available
```

---

## Context

{ARGS}

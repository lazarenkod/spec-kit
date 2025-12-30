# Integration Wizard Skill

## Purpose

Guide users through setting up third-party service integrations with SDK wrappers, environment configuration, error handling, and usage examples.

## Trigger

- User wants to add a third-party service (auth, payments, email, etc.)
- User asks about integrating a specific service
- After `/speckit.implement` when integrations are needed

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `service` | Yes | Service to integrate (e.g., stripe, clerk, resend) |
| `category` | No | Category if service ambiguous (auth, payments, etc.) |
| `stack` | No | Technology stack for SDK selection |

## Available Integrations

```yaml
catalog:
  auth:
    - clerk       # Modern auth with prebuilt UI
    - auth0       # Enterprise identity platform
    - supabase-auth  # Part of Supabase ecosystem
    - firebase-auth  # Google ecosystem

  payments:
    - stripe      # Industry standard
    - paddle      # MoR for SaaS
    - lemonsqueezy  # Simple SaaS payments

  email:
    - resend      # Modern API with React support
    - sendgrid    # Enterprise email
    - postmark    # Transactional email

  analytics:
    - posthog     # Open-source analytics
    - mixpanel    # Product analytics
    - amplitude   # Enterprise analytics

  storage:
    - s3          # AWS S3
    - cloudflare-r2  # S3-compatible, no egress
    - supabase-storage  # Part of Supabase

  database:
    - supabase    # PostgreSQL + more
    - planetscale # MySQL at scale
    - neon        # Serverless PostgreSQL

  search:
    - algolia     # Search as a service
    - meilisearch # Open-source search
    - typesense   # Open-source alternative

  ai:
    - openai      # GPT models
    - anthropic   # Claude models
    - replicate   # Model marketplace
```

## Skill Execution

### Step 1: Select Integration

```yaml
selection:
  service: "{{service}}"
  category: "{{category}}"

  from_catalog:
    name: "{{service_name}}"
    description: "{{service_description}}"
    pricing: "{{pricing_info}}"
    docs: "{{docs_url}}"
```

### Step 2: Gather Requirements

```yaml
requirements:
  env_vars:
    - name: "{{ENV_VAR_NAME}}"
      description: "{{description}}"
      required: true
      how_to_get: "{{instructions}}"

  packages:
    node: ["{{package_1}}", "{{package_2}}"]
    python: ["{{package_1}}", "{{package_2}}"]

  account_setup:
    - "Create account at {{provider_url}}"
    - "Create application/project"
    - "Generate API keys"
    - "Configure webhook endpoints (if needed)"
```

### Step 3: Generate Integration Code

```typescript
// Template for SDK wrapper
// src/lib/integrations/{{service}}.ts

import { {{SDKClass}} } from '{{package}}';

// Validate environment
const requiredEnvVars = [{{env_var_list}}];
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`${envVar} environment variable is required`);
  }
}

// Initialize client
export const {{clientName}} = new {{SDKClass}}({
  {{config_options}}
});

// Type definitions
export interface {{ServiceName}}Error extends Error {
  code: string;
  statusCode?: number;
}

// Error handling wrapper
async function withErrorHandling<T>(
  operation: () => Promise<T>,
  context: string
): Promise<T> {
  try {
    return await operation();
  } catch (error) {
    console.error(`[{{service}}] ${context}:`, error);
    throw error;
  }
}

// Main operations
export async function {{primaryOperation}}(params: {{ParamsType}}): Promise<{{ReturnType}}> {
  return withErrorHandling(async () => {
    // Implementation
  }, '{{primaryOperation}}');
}

// Additional operations...
```

### Step 4: Update Environment

```bash
# .env.local additions
{{ENV_VAR_1}}=your_value_here
{{ENV_VAR_2}}=your_value_here

# .env.example additions (no real values)
{{ENV_VAR_1}}=
{{ENV_VAR_2}}=
```

### Step 5: Generate Documentation

```markdown
# {{Service Name}} Integration

## Overview
{{Description of what this integration provides}}

## Setup

### 1. Create Account
- Go to {{provider_url}}
- Sign up for an account
- Create a new project/application

### 2. Get API Keys
- Navigate to {{settings_location}}
- Copy the following keys:
  - {{key_1}}: {{description}}
  - {{key_2}}: {{description}}

### 3. Configure Environment
Add to your `.env.local`:
```
{{ENV_VAR_1}}=your_api_key
{{ENV_VAR_2}}=your_secret
```

### 4. Install Package
```bash
npm install {{packages}}
```

## Usage

### Basic Example
```typescript
import { {{operation}} } from '@/lib/integrations/{{service}}';

const result = await {{operation}}({
  // params
});
```

### Error Handling
```typescript
try {
  const result = await {{operation}}(params);
} catch (error) {
  if (error.code === '{{common_error}}') {
    // Handle specific error
  }
}
```

## Webhook Setup (if applicable)
{{webhook_instructions}}

## Testing
{{testing_instructions}}

## Troubleshooting
| Error | Cause | Solution |
|-------|-------|----------|
| {{error_1}} | {{cause_1}} | {{solution_1}} |
```

### Step 6: Test Integration

```yaml
verification:
  steps:
    - name: "Install packages"
      command: "npm install"
      expect: "success"

    - name: "Check env vars"
      command: "node -e \"require('dotenv').config(); console.log(!!process.env.{{PRIMARY_ENV_VAR}})\""
      expect: "true"

    - name: "Import test"
      command: "node -e \"require('./src/lib/integrations/{{service}}')\""
      expect: "no errors"

    - name: "Smoke test"
      command: "npm run test:integration:{{service}}"
      expect: "pass"
```

## Output Format

```yaml
integration_output:
  files_created:
    - path: "src/lib/integrations/{{service}}.ts"
      description: "SDK wrapper with error handling"

    - path: "docs/integrations/{{service}}.md"
      description: "Integration documentation"

  files_modified:
    - path: ".env.example"
      changes: "Added {{env_var_count}} new variables"

    - path: "package.json"
      changes: "Added {{package_count}} dependencies"

  next_steps:
    - "Add API keys to .env.local"
    - "Review generated code"
    - "Run smoke test"
    - "Implement usage in application"
```

## Common Patterns

### Webhook Handler Pattern

```typescript
// src/app/api/webhooks/{{service}}/route.ts
import { headers } from 'next/headers';
import { {{service}} } from '@/lib/integrations/{{service}}';

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get('{{signature_header}}');

  if (!signature) {
    return new Response('Missing signature', { status: 400 });
  }

  try {
    const event = await {{service}}.verifyWebhook(body, signature);

    switch (event.type) {
      case '{{event_1}}':
        await handle{{Event1}}(event.data);
        break;
      case '{{event_2}}':
        await handle{{Event2}}(event.data);
        break;
    }

    return new Response('OK', { status: 200 });
  } catch (error) {
    console.error('Webhook error:', error);
    return new Response('Webhook error', { status: 400 });
  }
}
```

### Rate Limiting Pattern

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
});

export async function {{rateLimitedOperation}}(userId: string, params: any) {
  const { success, limit, reset, remaining } = await ratelimit.limit(userId);

  if (!success) {
    throw new Error(`Rate limited. Try again in ${reset - Date.now()}ms`);
  }

  return {{originalOperation}}(params);
}
```

## Integration

This skill is used by:
- `/speckit.integrate` - Main integration workflow
- `/speckit.implement` - When integrations needed during development

References:
- `templates/shared/integrate/integration-catalog.md` - Full catalog

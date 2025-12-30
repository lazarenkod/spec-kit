# Integration Catalog

## Purpose

Provide standardized integration templates for common third-party services. Each integration includes SDK setup, environment configuration, error handling, and usage examples.

## Catalog Structure

```
integrations/
├── auth/
│   ├── clerk.md
│   ├── auth0.md
│   ├── supabase-auth.md
│   └── firebase-auth.md
├── payments/
│   ├── stripe.md
│   ├── paddle.md
│   └── lemonsqueezy.md
├── email/
│   ├── resend.md
│   ├── sendgrid.md
│   └── postmark.md
├── analytics/
│   ├── posthog.md
│   ├── mixpanel.md
│   └── amplitude.md
├── storage/
│   ├── s3.md
│   ├── cloudflare-r2.md
│   └── supabase-storage.md
├── database/
│   ├── supabase.md
│   ├── planetscale.md
│   └── neon.md
├── search/
│   ├── algolia.md
│   ├── meilisearch.md
│   └── typesense.md
└── ai/
    ├── openai.md
    ├── anthropic.md
    └── replicate.md
```

---

## Authentication

### Clerk

```yaml
id: clerk
category: auth
name: Clerk
description: Complete user management with prebuilt UI components
pricing: Free up to 10,000 MAU
docs: https://clerk.com/docs

env_vars:
  - CLERK_PUBLISHABLE_KEY
  - CLERK_SECRET_KEY

packages:
  node: "@clerk/nextjs"
  react: "@clerk/clerk-react"

setup:
  1. "Create account at clerk.com"
  2. "Create application and get API keys"
  3. "Add environment variables"
  4. "Install SDK and configure middleware"
```

```typescript
// src/lib/integrations/clerk.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isProtectedRoute = createRouteMatcher(['/dashboard(.*)']);

export default clerkMiddleware((auth, req) => {
  if (isProtectedRoute(req)) {
    auth().protect();
  }
});

export const config = {
  matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)'],
};

// Usage in components
import { SignInButton, SignedIn, SignedOut, UserButton } from '@clerk/nextjs';

export function AuthButton() {
  return (
    <>
      <SignedOut>
        <SignInButton />
      </SignedOut>
      <SignedIn>
        <UserButton />
      </SignedIn>
    </>
  );
}
```

### Auth0

```yaml
id: auth0
category: auth
name: Auth0
description: Enterprise-grade identity platform
pricing: Free up to 7,000 MAU
docs: https://auth0.com/docs

env_vars:
  - AUTH0_SECRET
  - AUTH0_BASE_URL
  - AUTH0_ISSUER_BASE_URL
  - AUTH0_CLIENT_ID
  - AUTH0_CLIENT_SECRET

packages:
  node: "@auth0/nextjs-auth0"
```

```typescript
// src/lib/integrations/auth0.ts
import { handleAuth, handleLogin, handleLogout } from '@auth0/nextjs-auth0';

export const GET = handleAuth({
  login: handleLogin({
    returnTo: '/dashboard',
  }),
  logout: handleLogout({
    returnTo: '/',
  }),
});

// Usage
import { useUser } from '@auth0/nextjs-auth0/client';

export function Profile() {
  const { user, error, isLoading } = useUser();
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;
  if (!user) return <a href="/api/auth/login">Login</a>;
  return <div>Hello {user.name}</div>;
}
```

---

## Payments

### Stripe

```yaml
id: stripe
category: payments
name: Stripe
description: Payment processing and billing
pricing: 2.9% + $0.30 per transaction
docs: https://stripe.com/docs

env_vars:
  - STRIPE_SECRET_KEY
  - STRIPE_PUBLISHABLE_KEY
  - STRIPE_WEBHOOK_SECRET

packages:
  node: "stripe"
  react: "@stripe/stripe-js @stripe/react-stripe-js"
```

```typescript
// src/lib/integrations/stripe.ts
import Stripe from 'stripe';

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error('STRIPE_SECRET_KEY is required');
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2023-10-16',
  typescript: true,
});

// Create checkout session
export async function createCheckoutSession(params: {
  priceId: string;
  customerId?: string;
  successUrl: string;
  cancelUrl: string;
}) {
  return stripe.checkout.sessions.create({
    mode: 'subscription',
    customer: params.customerId,
    line_items: [{ price: params.priceId, quantity: 1 }],
    success_url: params.successUrl,
    cancel_url: params.cancelUrl,
  });
}

// Webhook handler
export async function handleWebhook(body: string, signature: string) {
  const event = stripe.webhooks.constructEvent(
    body,
    signature,
    process.env.STRIPE_WEBHOOK_SECRET!
  );

  switch (event.type) {
    case 'checkout.session.completed':
      // Handle successful checkout
      break;
    case 'customer.subscription.updated':
      // Handle subscription change
      break;
    case 'customer.subscription.deleted':
      // Handle cancellation
      break;
  }

  return { received: true };
}
```

### LemonSqueezy

```yaml
id: lemonsqueezy
category: payments
name: LemonSqueezy
description: All-in-one payments, tax, and subscriptions for SaaS
pricing: 5% + $0.50 per transaction (includes tax handling)
docs: https://docs.lemonsqueezy.com

env_vars:
  - LEMONSQUEEZY_API_KEY
  - LEMONSQUEEZY_STORE_ID
  - LEMONSQUEEZY_WEBHOOK_SECRET

packages:
  node: "@lemonsqueezy/lemonsqueezy.js"
```

```typescript
// src/lib/integrations/lemonsqueezy.ts
import {
  lemonSqueezySetup,
  createCheckout,
  getSubscription,
} from '@lemonsqueezy/lemonsqueezy.js';

lemonSqueezySetup({
  apiKey: process.env.LEMONSQUEEZY_API_KEY!,
});

export async function createLemonCheckout(params: {
  variantId: string;
  email: string;
  customData?: Record<string, any>;
}) {
  const checkout = await createCheckout(
    process.env.LEMONSQUEEZY_STORE_ID!,
    params.variantId,
    {
      checkoutData: {
        email: params.email,
        custom: params.customData,
      },
    }
  );
  return checkout.data?.attributes.url;
}
```

---

## Email

### Resend

```yaml
id: resend
category: email
name: Resend
description: Modern email API with React support
pricing: Free up to 3,000 emails/month
docs: https://resend.com/docs

env_vars:
  - RESEND_API_KEY

packages:
  node: "resend"
  react: "@react-email/components"
```

```typescript
// src/lib/integrations/resend.ts
import { Resend } from 'resend';

if (!process.env.RESEND_API_KEY) {
  throw new Error('RESEND_API_KEY is required');
}

export const resend = new Resend(process.env.RESEND_API_KEY);

// Send email
export async function sendEmail(params: {
  to: string | string[];
  subject: string;
  react?: React.ReactElement;
  html?: string;
  from?: string;
}) {
  return resend.emails.send({
    from: params.from || 'noreply@yourdomain.com',
    to: params.to,
    subject: params.subject,
    react: params.react,
    html: params.html,
  });
}

// Email template with React
import { Html, Head, Body, Container, Text, Button } from '@react-email/components';

export function WelcomeEmail({ name, actionUrl }: { name: string; actionUrl: string }) {
  return (
    <Html>
      <Head />
      <Body>
        <Container>
          <Text>Welcome, {name}!</Text>
          <Button href={actionUrl}>Get Started</Button>
        </Container>
      </Body>
    </Html>
  );
}
```

---

## Analytics

### PostHog

```yaml
id: posthog
category: analytics
name: PostHog
description: Open-source product analytics with feature flags
pricing: Free up to 1M events/month
docs: https://posthog.com/docs

env_vars:
  - NEXT_PUBLIC_POSTHOG_KEY
  - NEXT_PUBLIC_POSTHOG_HOST

packages:
  node: "posthog-node"
  react: "posthog-js"
```

```typescript
// src/lib/integrations/posthog.ts
import posthog from 'posthog-js';
import { PostHog } from 'posthog-node';

// Client-side
export function initPostHog() {
  if (typeof window !== 'undefined') {
    posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://app.posthog.com',
      capture_pageview: false,
    });
  }
}

// Server-side
export const posthogServer = new PostHog(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
  host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://app.posthog.com',
});

// Track event
export function trackEvent(event: string, properties?: Record<string, any>) {
  posthog.capture(event, properties);
}

// Feature flags
export function isFeatureEnabled(flag: string): boolean {
  return posthog.isFeatureEnabled(flag) ?? false;
}
```

---

## Storage

### Cloudflare R2

```yaml
id: cloudflare-r2
category: storage
name: Cloudflare R2
description: S3-compatible object storage with no egress fees
pricing: Free up to 10GB storage, 1M Class A ops
docs: https://developers.cloudflare.com/r2

env_vars:
  - R2_ACCOUNT_ID
  - R2_ACCESS_KEY_ID
  - R2_SECRET_ACCESS_KEY
  - R2_BUCKET_NAME

packages:
  node: "@aws-sdk/client-s3"
```

```typescript
// src/lib/integrations/r2.ts
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

const r2 = new S3Client({
  region: 'auto',
  endpoint: `https://${process.env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: process.env.R2_ACCESS_KEY_ID!,
    secretAccessKey: process.env.R2_SECRET_ACCESS_KEY!,
  },
});

export async function uploadFile(key: string, body: Buffer, contentType: string) {
  await r2.send(new PutObjectCommand({
    Bucket: process.env.R2_BUCKET_NAME!,
    Key: key,
    Body: body,
    ContentType: contentType,
  }));
  return `https://${process.env.R2_BUCKET_NAME}.r2.dev/${key}`;
}

export async function getSignedUploadUrl(key: string) {
  return getSignedUrl(r2, new PutObjectCommand({
    Bucket: process.env.R2_BUCKET_NAME!,
    Key: key,
  }), { expiresIn: 3600 });
}
```

---

## Database

### Supabase

```yaml
id: supabase
category: database
name: Supabase
description: Open-source Firebase alternative with PostgreSQL
pricing: Free up to 500MB database, 1GB storage
docs: https://supabase.com/docs

env_vars:
  - SUPABASE_URL
  - SUPABASE_ANON_KEY
  - SUPABASE_SERVICE_ROLE_KEY

packages:
  node: "@supabase/supabase-js"
```

```typescript
// src/lib/integrations/supabase.ts
import { createClient } from '@supabase/supabase-js';
import type { Database } from '@/types/supabase';

// Client-side (uses anon key)
export const supabase = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Server-side (uses service role key)
export const supabaseAdmin = createClient<Database>(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

// Type-safe queries
export async function getUser(id: string) {
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('id', id)
    .single();

  if (error) throw error;
  return data;
}
```

### Neon

```yaml
id: neon
category: database
name: Neon
description: Serverless PostgreSQL with branching
pricing: Free up to 0.5GB storage, 1 compute
docs: https://neon.tech/docs

env_vars:
  - DATABASE_URL

packages:
  node: "@neondatabase/serverless drizzle-orm"
```

```typescript
// src/lib/integrations/neon.ts
import { neon, neonConfig } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';
import * as schema from './schema';

neonConfig.fetchConnectionCache = true;

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });

// Usage with Drizzle
import { eq } from 'drizzle-orm';
import { users } from './schema';

export async function getUserById(id: string) {
  const result = await db.select().from(users).where(eq(users.id, id));
  return result[0];
}
```

---

## AI

### Anthropic (Claude)

```yaml
id: anthropic
category: ai
name: Anthropic Claude
description: Claude AI models for text generation
pricing: Pay per token (varies by model)
docs: https://docs.anthropic.com

env_vars:
  - ANTHROPIC_API_KEY

packages:
  node: "@anthropic-ai/sdk"
```

```typescript
// src/lib/integrations/anthropic.ts
import Anthropic from '@anthropic-ai/sdk';

if (!process.env.ANTHROPIC_API_KEY) {
  throw new Error('ANTHROPIC_API_KEY is required');
}

export const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export async function generateText(params: {
  prompt: string;
  maxTokens?: number;
  model?: string;
}) {
  const message = await anthropic.messages.create({
    model: params.model || 'claude-3-sonnet-20240229',
    max_tokens: params.maxTokens || 1024,
    messages: [{ role: 'user', content: params.prompt }],
  });

  return message.content[0].type === 'text' ? message.content[0].text : '';
}

// Streaming
export async function* streamText(params: {
  prompt: string;
  model?: string;
}) {
  const stream = await anthropic.messages.stream({
    model: params.model || 'claude-3-sonnet-20240229',
    max_tokens: 1024,
    messages: [{ role: 'user', content: params.prompt }],
  });

  for await (const event of stream) {
    if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
      yield event.delta.text;
    }
  }
}
```

### OpenAI

```yaml
id: openai
category: ai
name: OpenAI
description: GPT models for text generation and embeddings
pricing: Pay per token (varies by model)
docs: https://platform.openai.com/docs

env_vars:
  - OPENAI_API_KEY

packages:
  node: "openai"
```

```typescript
// src/lib/integrations/openai.ts
import OpenAI from 'openai';

if (!process.env.OPENAI_API_KEY) {
  throw new Error('OPENAI_API_KEY is required');
}

export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function generateCompletion(params: {
  prompt: string;
  model?: string;
}) {
  const response = await openai.chat.completions.create({
    model: params.model || 'gpt-4-turbo-preview',
    messages: [{ role: 'user', content: params.prompt }],
  });

  return response.choices[0].message.content;
}

export async function generateEmbedding(text: string) {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });

  return response.data[0].embedding;
}
```

---

## Integration Checklist

```yaml
checklist:
  setup:
    - [ ] "Create account on service provider"
    - [ ] "Generate API keys"
    - [ ] "Add environment variables to .env.local"
    - [ ] "Install required packages"

  implementation:
    - [ ] "Create integration wrapper in src/lib/integrations/"
    - [ ] "Add error handling with typed errors"
    - [ ] "Add retry logic for transient failures"
    - [ ] "Add logging for debugging"

  testing:
    - [ ] "Test in development with real credentials"
    - [ ] "Add mock for unit tests"
    - [ ] "Document usage examples"

  deployment:
    - [ ] "Add env vars to hosting platform"
    - [ ] "Configure webhook endpoints if needed"
    - [ ] "Set up monitoring for API calls"
```

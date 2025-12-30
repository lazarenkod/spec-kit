# SEO Setup Guide

## Purpose

Configure search engine optimization for product launches, including technical SEO, on-page optimization, structured data, and analytics integration.

## SEO Checklist

### Technical SEO

```yaml
technical_seo:
  indexing:
    - [ ] Sitemap.xml generated and submitted
    - [ ] Robots.txt configured correctly
    - [ ] No accidental noindex tags
    - [ ] Google Search Console verified
    - [ ] Bing Webmaster Tools set up

  performance:
    - [ ] Core Web Vitals passing
    - [ ] Page load < 3 seconds
    - [ ] Mobile-friendly test passing
    - [ ] Images optimized (WebP, lazy loading)
    - [ ] CSS/JS minified and compressed

  security:
    - [ ] HTTPS enforced (SSL certificate)
    - [ ] HSTS headers configured
    - [ ] No mixed content warnings

  structure:
    - [ ] Canonical URLs set
    - [ ] Hreflang tags (if multilingual)
    - [ ] Clean URL structure
    - [ ] 404 page customized
    - [ ] Redirects (301) for changed URLs
```

### On-Page SEO

```yaml
on_page_seo:
  title_tags:
    format: "[Primary Keyword] - [Secondary] | [Brand]"
    max_length: 60
    examples:
      homepage: "Task Management for Teams - Free Project Tracker | ProductName"
      features: "Kanban Boards & Sprints - ProductName Features"
      pricing: "Pricing Plans - Start Free | ProductName"

  meta_descriptions:
    max_length: 155
    include:
      - Value proposition
      - Call to action
      - Unique differentiator
    example: "Manage your team's tasks with ease. Free kanban boards, sprint planning, and time tracking. Start free, no credit card required."

  headings:
    - [ ] Single H1 per page
    - [ ] H1 includes primary keyword
    - [ ] Logical H2-H6 hierarchy
    - [ ] Keywords in subheadings naturally

  content:
    - [ ] Primary keyword in first 100 words
    - [ ] LSI keywords throughout
    - [ ] Internal linking to key pages
    - [ ] External links to authoritative sources
    - [ ] Alt text for all images
```

### Structured Data (Schema.org)

```yaml
structured_data:
  organization:
    type: "Organization"
    required:
      - name
      - url
      - logo
      - sameAs (social profiles)
    optional:
      - description
      - foundingDate
      - founders

  product:
    type: "SoftwareApplication"
    required:
      - name
      - applicationCategory
      - operatingSystem
    optional:
      - offers (pricing)
      - aggregateRating
      - review

  faq:
    type: "FAQPage"
    use_when: "FAQ section on page"

  breadcrumb:
    type: "BreadcrumbList"
    use_when: "Multi-level navigation"
```

---

## Implementation Templates

### Sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/features</loc>
    <lastmod>2024-01-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://example.com/pricing</loc>
    <lastmod>2024-01-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <!-- Add all public pages -->
</urlset>
```

### Robots.txt

```text
# robots.txt for {{product_name}}

User-agent: *
Allow: /

# Block admin and API routes
Disallow: /admin/
Disallow: /api/
Disallow: /dashboard/

# Block auth pages
Disallow: /login
Disallow: /signup
Disallow: /reset-password

# Sitemap location
Sitemap: https://example.com/sitemap.xml
```

### Meta Tags (Next.js)

```typescript
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
  title: {
    default: '{{product_name}} - {{tagline}}',
    template: '%s | {{product_name}}',
  },
  description: '{{meta_description}}',
  keywords: ['{{keyword1}}', '{{keyword2}}', '{{keyword3}}'],
  authors: [{ name: '{{company_name}}' }],
  creator: '{{company_name}}',
  publisher: '{{company_name}}',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://example.com',
    siteName: '{{product_name}}',
    title: '{{product_name}} - {{tagline}}',
    description: '{{meta_description}}',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: '{{product_name}}',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: '{{product_name}} - {{tagline}}',
    description: '{{meta_description}}',
    images: ['/og-image.png'],
    creator: '@{{twitter_handle}}',
  },
  verification: {
    google: '{{google_verification}}',
  },
  alternates: {
    canonical: 'https://example.com',
  },
};
```

### Organization Schema

```typescript
// components/organization-schema.tsx
export function OrganizationSchema() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: '{{company_name}}',
    url: 'https://example.com',
    logo: 'https://example.com/logo.png',
    description: '{{company_description}}',
    foundingDate: '{{founding_year}}',
    founders: [
      {
        '@type': 'Person',
        name: '{{founder_name}}',
      },
    ],
    sameAs: [
      'https://twitter.com/{{handle}}',
      'https://linkedin.com/company/{{handle}}',
      'https://github.com/{{handle}}',
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      contactType: 'customer support',
      email: 'support@example.com',
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

### Software Application Schema

```typescript
// components/product-schema.tsx
export function ProductSchema() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: '{{product_name}}',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Web',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
      description: 'Free tier available',
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: '4.8',
      ratingCount: '150',
      bestRating: '5',
      worstRating: '1',
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

### FAQ Schema

```typescript
// components/faq-schema.tsx
export function FAQSchema({ faqs }: { faqs: Array<{ q: string; a: string }> }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.q,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.a,
      },
    })),
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

---

## Analytics Setup

### Google Analytics 4

```typescript
// lib/analytics.ts
export const GA_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA_ID;

// Track page views
export function pageview(url: string) {
  if (typeof window.gtag !== 'undefined') {
    window.gtag('config', GA_MEASUREMENT_ID, {
      page_path: url,
    });
  }
}

// Track events
export function event({
  action,
  category,
  label,
  value,
}: {
  action: string;
  category: string;
  label?: string;
  value?: number;
}) {
  if (typeof window.gtag !== 'undefined') {
    window.gtag('event', action, {
      event_category: category,
      event_label: label,
      value: value,
    });
  }
}
```

### PostHog Analytics

```typescript
// lib/posthog.ts
import posthog from 'posthog-js';

export function initAnalytics() {
  if (typeof window !== 'undefined') {
    posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST,
      capture_pageview: false, // Manual control
      capture_pageleave: true,
    });
  }
}

// Conversion events
export const trackSignup = (source: string) => {
  posthog.capture('signup_completed', { source });
};

export const trackTrialStart = (plan: string) => {
  posthog.capture('trial_started', { plan });
};

export const trackPurchase = (plan: string, value: number) => {
  posthog.capture('purchase_completed', { plan, value });
};
```

---

## UTM Parameter Strategy

```yaml
utm_parameters:
  sources:
    - organic (search engines)
    - direct (direct traffic)
    - referral (other websites)
    - social (social media)
    - email (email campaigns)
    - paid (paid advertising)

  mediums:
    - cpc (cost per click)
    - display (display ads)
    - social (social posts)
    - email (email)
    - affiliate (affiliate links)

  campaigns:
    format: "[year]-[quarter]-[campaign-name]"
    examples:
      - "2024-q1-launch"
      - "2024-q1-producthunt"
      - "2024-q1-blackfriday"

  examples:
    product_hunt: "?utm_source=producthunt&utm_medium=referral&utm_campaign=2024-launch"
    twitter: "?utm_source=twitter&utm_medium=social&utm_campaign=2024-launch"
    email_launch: "?utm_source=email&utm_medium=email&utm_campaign=2024-launch-announcement"
```

---

## SEO Monitoring

```yaml
monitoring:
  weekly:
    - Check Search Console for errors
    - Review Core Web Vitals
    - Monitor keyword rankings
    - Check for broken links

  monthly:
    - Analyze organic traffic trends
    - Review top landing pages
    - Check competitor rankings
    - Update underperforming content

  quarterly:
    - Full technical SEO audit
    - Content gap analysis
    - Backlink profile review
    - Strategy adjustment
```

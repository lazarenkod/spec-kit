# Smoke Test Landing Page

## Purpose

Generate conversion-optimized landing pages for validating demand before building. Measure signup conversion to validate problem-solution fit.

## Landing Page Structure

### Minimal Viable Landing Page

```html
<!-- smoke-test-landing.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{PRODUCT_NAME}} - {{TAGLINE}}</title>

  <!-- SEO -->
  <meta name="description" content="{{META_DESCRIPTION}}">

  <!-- Open Graph -->
  <meta property="og:title" content="{{PRODUCT_NAME}} - {{TAGLINE}}">
  <meta property="og:description" content="{{META_DESCRIPTION}}">
  <meta property="og:image" content="{{OG_IMAGE_URL}}">
  <meta property="og:type" content="website">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{PRODUCT_NAME}} - {{TAGLINE}}">
  <meta name="twitter:description" content="{{META_DESCRIPTION}}">
  <meta name="twitter:image" content="{{OG_IMAGE_URL}}">

  <!-- Analytics -->
  <script defer data-domain="{{DOMAIN}}" src="https://plausible.io/js/script.js"></script>

  <style>
    /* Minimal CSS - inline for fast load */
    :root {
      --primary: {{PRIMARY_COLOR}};
      --text: #1a1a1a;
      --muted: #6b7280;
      --bg: #ffffff;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: system-ui, -apple-system, sans-serif;
      line-height: 1.6;
      color: var(--text);
      background: var(--bg);
    }

    .container {
      max-width: 640px;
      margin: 0 auto;
      padding: 4rem 1.5rem;
      text-align: center;
    }

    .logo { font-size: 1.5rem; font-weight: 700; margin-bottom: 2rem; }

    h1 {
      font-size: 2.5rem;
      font-weight: 800;
      line-height: 1.2;
      margin-bottom: 1rem;
    }

    .subtitle {
      font-size: 1.25rem;
      color: var(--muted);
      margin-bottom: 2rem;
    }

    .form {
      display: flex;
      gap: 0.5rem;
      justify-content: center;
      flex-wrap: wrap;
      margin-bottom: 1rem;
    }

    input[type="email"] {
      padding: 0.875rem 1rem;
      font-size: 1rem;
      border: 1px solid #e5e7eb;
      border-radius: 0.5rem;
      width: 280px;
    }

    button {
      padding: 0.875rem 1.5rem;
      font-size: 1rem;
      font-weight: 600;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: 0.5rem;
      cursor: pointer;
      transition: opacity 0.2s;
    }

    button:hover { opacity: 0.9; }

    .social-proof {
      font-size: 0.875rem;
      color: var(--muted);
    }

    .benefits {
      margin-top: 4rem;
      text-align: left;
      display: grid;
      gap: 1.5rem;
    }

    .benefit {
      display: flex;
      gap: 1rem;
      align-items: flex-start;
    }

    .benefit-icon {
      width: 24px;
      height: 24px;
      color: var(--primary);
      flex-shrink: 0;
    }

    .benefit h3 { font-size: 1.125rem; margin-bottom: 0.25rem; }
    .benefit p { font-size: 0.9375rem; color: var(--muted); }

    .success {
      padding: 1rem;
      background: #ecfdf5;
      border-radius: 0.5rem;
      color: #065f46;
      display: none;
    }

    .success.show { display: block; }
    .form.hide { display: none; }
  </style>
</head>
<body>
  <div class="container">
    <div class="logo">{{PRODUCT_NAME}}</div>

    <h1>{{HEADLINE}}</h1>
    <p class="subtitle">{{SUBHEADLINE}}</p>

    <form class="form" id="signup-form">
      <input
        type="email"
        name="email"
        placeholder="Enter your email"
        required
        autocomplete="email"
      >
      <button type="submit">{{CTA_TEXT}}</button>
    </form>

    <div class="success" id="success-message">
      {{SUCCESS_MESSAGE}}
    </div>

    <p class="social-proof">{{SOCIAL_PROOF}}</p>

    <div class="benefits">
      {{#each BENEFITS}}
      <div class="benefit">
        <svg class="benefit-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 13l4 4L19 7"/>
        </svg>
        <div>
          <h3>{{title}}</h3>
          <p>{{description}}</p>
        </div>
      </div>
      {{/each}}
    </div>
  </div>

  <script>
    const form = document.getElementById('signup-form');
    const success = document.getElementById('success-message');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = form.email.value;

      // Track conversion
      if (window.plausible) {
        plausible('Signup', { props: { email: email.split('@')[1] }});
      }

      // Send to backend
      try {
        await fetch('{{SIGNUP_ENDPOINT}}', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, source: 'smoke-test' })
        });
      } catch (err) {
        console.error('Signup error:', err);
      }

      // Show success
      form.classList.add('hide');
      success.classList.add('show');
    });
  </script>
</body>
</html>
```

## Landing Page Variants

### A/B Test Headlines

```yaml
variant_a:
  headline: "{{PROBLEM_FOCUSED_HEADLINE}}"
  # Example: "Stop Wasting Hours on Manual Data Entry"
  hypothesis: "Problem-focused resonates with pain-aware audience"

variant_b:
  headline: "{{SOLUTION_FOCUSED_HEADLINE}}"
  # Example: "Automate Your Data Entry in Minutes"
  hypothesis: "Solution-focused works for solution-aware audience"

variant_c:
  headline: "{{OUTCOME_FOCUSED_HEADLINE}}"
  # Example: "Get 10 Hours Back Every Week"
  hypothesis: "Outcome-focused emphasizes transformation"
```

### CTA Variations

```yaml
cta_variants:
  - "Get Early Access"      # Exclusivity
  - "Join the Waitlist"     # FOMO
  - "Start Free Trial"      # Low risk
  - "See How It Works"      # Curiosity
  - "Get Started Free"      # Zero barrier
  - "Request Demo"          # High-touch for B2B
```

## Configuration Template

```yaml
# smoke-test-config.yaml

product:
  name: "{{PRODUCT_NAME}}"
  tagline: "{{SHORT_TAGLINE}}"
  domain: "example.com"

content:
  headline: "{{PRIMARY_HEADLINE}}"
  subheadline: "{{SUPPORTING_STATEMENT}}"
  cta_text: "Get Early Access"
  success_message: "You're on the list! We'll be in touch soon."
  social_proof: "Join 500+ people on the waitlist"

benefits:
  - title: "{{BENEFIT_1_TITLE}}"
    description: "{{BENEFIT_1_DESCRIPTION}}"
  - title: "{{BENEFIT_2_TITLE}}"
    description: "{{BENEFIT_2_DESCRIPTION}}"
  - title: "{{BENEFIT_3_TITLE}}"
    description: "{{BENEFIT_3_DESCRIPTION}}"

seo:
  meta_description: "{{META_DESCRIPTION_155_CHARS}}"
  og_image: "/og-image.png"

branding:
  primary_color: "#4F46E5"
  logo_url: "/logo.svg"

tracking:
  analytics: "plausible"  # or "posthog", "google"
  domain: "example.com"

backend:
  signup_endpoint: "https://api.example.com/waitlist"
  # Or use: "https://formspree.io/f/xxxxx"
  # Or use: "https://getform.io/f/xxxxx"
```

## Conversion Benchmarks

```yaml
conversion_benchmarks:
  smoke_test_landing:
    excellent: ">10%"      # Strong signal
    good: "5-10%"          # Proceed with caution
    weak: "2-5%"           # Needs iteration
    fail: "<2%"            # Pivot or abort

  source_expectations:
    paid_ads: "2-5%"       # Cold traffic
    social_organic: "3-8%" # Warm audience
    email_list: "8-15%"    # Hot audience
    product_hunt: "3-7%"   # Mixed intent
```

## Validation Decision Framework

```yaml
validation_criteria:
  green_light:
    - conversion_rate: ">5%"
    - signups: ">100"
    - source_diversity: ">3 channels"
    - organic_sharing: "present"

  yellow_light:
    - conversion_rate: "2-5%"
    - signups: "50-100"
    - recommendation: "iterate messaging, retest"

  red_light:
    - conversion_rate: "<2%"
    - signups: "<50"
    - recommendation: "pivot hypothesis or kill"

decision_tree:
  IF conversion > 5% AND signups > 100:
    DECISION: "GO - Proceed to build MVP"

  ELIF conversion > 5% AND signups < 100:
    DECISION: "EXTEND - Drive more traffic, revalidate"

  ELIF conversion 2-5%:
    DECISION: "ITERATE - Test new headlines/value props"
    max_iterations: 3

  ELSE:
    DECISION: "STOP - Problem hypothesis likely wrong"
```

## Quick Deploy Options

### Option 1: Static (Recommended for speed)

```bash
# Deploy to Vercel in seconds
npx vercel deploy --prod

# Or Netlify
npx netlify deploy --prod

# Or Cloudflare Pages
npx wrangler pages publish ./dist
```

### Option 2: Form Backend Services

```yaml
no_code_backends:
  - service: "Formspree"
    signup_endpoint: "https://formspree.io/f/YOUR_FORM_ID"
    free_tier: "50 submissions/month"

  - service: "Getform"
    signup_endpoint: "https://getform.io/f/YOUR_FORM_ID"
    free_tier: "50 submissions/month"

  - service: "Basin"
    signup_endpoint: "https://usebasin.com/f/YOUR_FORM_ID"
    free_tier: "100 submissions/month"

  - service: "Formcarry"
    signup_endpoint: "https://formcarry.com/s/YOUR_FORM_ID"
    free_tier: "100 submissions/month"
```

### Option 3: Full Analytics Setup

```html
<!-- PostHog (recommended for product analytics) -->
<script>
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
  posthog.init('{{POSTHOG_KEY}}', {api_host: 'https://app.posthog.com'})
</script>
```

## Success Metrics Dashboard

```yaml
metrics_to_track:
  traffic:
    - unique_visitors
    - page_views
    - bounce_rate
    - time_on_page

  conversion:
    - email_form_views
    - email_submissions
    - conversion_rate
    - by_source_utm

  engagement:
    - scroll_depth
    - cta_clicks
    - exit_intent_triggers

  quality:
    - email_domain_distribution
    - duplicate_submissions
    - fake_email_rate
```

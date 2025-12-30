# Landing Page Generator Skill

## Purpose

Generate conversion-optimized smoke test landing pages to validate demand before building. Create minimal viable landing pages that measure signup conversion to validate problem-solution fit.

## Trigger

- User wants to test demand for a product idea
- User needs a smoke test landing page
- User wants to validate willingness-to-pay before building

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `product_name` | Yes | Name of the product/service |
| `value_proposition` | Yes | Core value prop (1 sentence) |
| `target_persona` | Yes | Who this is for |
| `primary_benefit` | Yes | Main benefit for the user |
| `secondary_benefits` | No | Additional benefits (2-3) |
| `pricing_hint` | No | Price point to test (optional) |

## Skill Execution

### Step 1: Generate Messaging Framework

```yaml
messaging:
  headline_variants:
    problem_focused: "Stop [Pain Point] Forever"
    solution_focused: "[Action] Your [Domain] in Minutes"
    outcome_focused: "Get [Specific Result] Without [Usual Hassle]"

  subheadline: "[Expand on headline with specific benefit]"

  cta_variants:
    - "Get Early Access"      # Exclusivity
    - "Join the Waitlist"     # FOMO
    - "Start Free Trial"      # Low risk
    - "See How It Works"      # Curiosity

  social_proof: "Join {{count}}+ people on the waitlist"
```

### Step 2: Define Benefits

```yaml
benefits:
  - title: "{{primary_benefit_title}}"
    description: "{{primary_benefit_description}}"
    icon: "check"

  - title: "{{secondary_benefit_1_title}}"
    description: "{{secondary_benefit_1_description}}"
    icon: "check"

  - title: "{{secondary_benefit_2_title}}"
    description: "{{secondary_benefit_2_description}}"
    icon: "check"
```

### Step 3: Generate Landing Page HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{product_name}} - {{tagline}}</title>

  <!-- SEO -->
  <meta name="description" content="{{meta_description}}">

  <!-- Open Graph -->
  <meta property="og:title" content="{{product_name}} - {{tagline}}">
  <meta property="og:description" content="{{meta_description}}">
  <meta property="og:image" content="{{og_image_url}}">
  <meta property="og:type" content="website">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{product_name}} - {{tagline}}">
  <meta name="twitter:description" content="{{meta_description}}">

  <!-- Analytics (Plausible - privacy-friendly) -->
  <script defer data-domain="{{domain}}" src="https://plausible.io/js/script.js"></script>

  <style>
    :root {
      --primary: {{primary_color}};
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
    }

    .benefits {
      margin-top: 4rem;
      text-align: left;
      display: grid;
      gap: 1.5rem;
    }

    .benefit { display: flex; gap: 1rem; }
    .benefit h3 { font-size: 1.125rem; margin-bottom: 0.25rem; }
    .benefit p { font-size: 0.9375rem; color: var(--muted); }
  </style>
</head>
<body>
  <div class="container">
    <div class="logo">{{product_name}}</div>
    <h1>{{headline}}</h1>
    <p class="subtitle">{{subheadline}}</p>

    <form class="form" id="signup-form">
      <input type="email" name="email" placeholder="Enter your email" required>
      <button type="submit">{{cta_text}}</button>
    </form>

    <p class="social-proof">{{social_proof}}</p>

    <div class="benefits">
      {{#each benefits}}
      <div class="benefit">
        <div>
          <h3>{{title}}</h3>
          <p>{{description}}</p>
        </div>
      </div>
      {{/each}}
    </div>
  </div>

  <script>
    document.getElementById('signup-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = e.target.email.value;

      // Track conversion
      if (window.plausible) {
        plausible('Signup', { props: { domain: email.split('@')[1] }});
      }

      // Send to backend
      await fetch('{{signup_endpoint}}', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, source: 'smoke-test' })
      });

      // Show success
      e.target.innerHTML = '<p style="color: #065f46;">{{success_message}}</p>';
    });
  </script>
</body>
</html>
```

### Step 4: Generate Configuration

```yaml
# smoke-test-config.yaml
product:
  name: "{{product_name}}"
  tagline: "{{value_proposition}}"
  domain: "{{domain}}"

content:
  headline: "{{headline}}"
  subheadline: "{{subheadline}}"
  cta_text: "Get Early Access"
  success_message: "You're on the list! We'll be in touch soon."
  social_proof: "Join 500+ people on the waitlist"

benefits:
  - title: "{{benefit_1_title}}"
    description: "{{benefit_1_desc}}"
  - title: "{{benefit_2_title}}"
    description: "{{benefit_2_desc}}"
  - title: "{{benefit_3_title}}"
    description: "{{benefit_3_desc}}"

seo:
  meta_description: "{{meta_description_155_chars}}"
  og_image: "/og-image.png"

branding:
  primary_color: "#4F46E5"

tracking:
  analytics: "plausible"
  domain: "{{domain}}"

backend:
  signup_endpoint: "https://formspree.io/f/xxxxx"
```

### Step 5: Deployment Instructions

```markdown
## Quick Deploy Options

### Option 1: Vercel (Recommended)
```bash
npx vercel deploy --prod
```

### Option 2: Netlify
```bash
npx netlify deploy --prod
```

### Option 3: Cloudflare Pages
```bash
npx wrangler pages publish ./
```

### Form Backend Options (No Code)

| Service | Free Tier | Endpoint Format |
|---------|-----------|-----------------|
| Formspree | 50/month | `https://formspree.io/f/YOUR_ID` |
| Getform | 50/month | `https://getform.io/f/YOUR_ID` |
| Basin | 100/month | `https://usebasin.com/f/YOUR_ID` |
```

### Step 6: Define Success Metrics

```yaml
conversion_benchmarks:
  excellent: ">10%"    # Strong demand signal
  good: "5-10%"        # Proceed with caution
  weak: "2-5%"         # Needs iteration
  fail: "<2%"          # Pivot or abort

traffic_source_expectations:
  paid_ads: "2-5%"
  social_organic: "3-8%"
  email_list: "8-15%"
  product_hunt: "3-7%"

validation_decision:
  IF conversion > 5% AND signups > 100:
    decision: "GO - Build MVP"
  ELIF conversion > 5% AND signups < 100:
    decision: "EXTEND - Drive more traffic"
  ELIF conversion 2-5%:
    decision: "ITERATE - Test new messaging"
  ELSE:
    decision: "STOP - Hypothesis likely wrong"
```

## Output Format

```yaml
landing_page_package:
  files:
    - path: "index.html"
      content: "[Generated HTML]"
    - path: "smoke-test-config.yaml"
      content: "[Configuration]"

  deployment:
    recommended: "vercel"
    alternatives: ["netlify", "cloudflare"]
    form_backend: "formspree"

  tracking:
    events: ["page_view", "form_start", "signup"]
    dashboard_url: "https://plausible.io/{{domain}}"

  validation:
    target_signups: 100
    target_conversion: "5%"
    test_duration: "7-14 days"
```

## A/B Testing Setup

```yaml
ab_test_variants:
  headlines:
    control: "{{problem_focused_headline}}"
    variant_a: "{{solution_focused_headline}}"
    variant_b: "{{outcome_focused_headline}}"

  ctas:
    control: "Get Early Access"
    variant_a: "Join the Waitlist"
    variant_b: "Start Free Trial"

  setup:
    tool: "Plausible Goals + URL params"
    traffic_split: "33/33/34"
    minimum_sample: "100 per variant"
    significance: "95%"
```

## Integration

This skill is used by:
- `/speckit.discover` - Demand validation workflow
- `/speckit.concept` - When smoke_test flag is set

References:
- `templates/shared/discover/smoke-test-landing.md` - Full template details
- `templates/shared/launch/seo-setup.md` - SEO configuration

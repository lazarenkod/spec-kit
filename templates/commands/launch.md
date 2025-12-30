---
name: launch
description: Automate product launch and go-to-market activities
version: 1.0.0
persona: marketing-agent
skills:
  - launch-prep
  - seo-optimizer
  - press-kit-generator
inputs:
  product_name:
    type: string
    required: true
    description: Name of the product to launch
  launch_date:
    type: date
    required: true
    description: Target launch date
  channels:
    type: array
    items: [product-hunt, hacker-news, twitter, linkedin, email, press]
    required: false
    default: [product-hunt, twitter, email]
    description: Launch channels to prepare
  press_outreach:
    type: boolean
    required: false
    default: false
    description: Whether to prepare press kit and outreach
outputs:
  - docs/launch/launch-plan.md
  - docs/launch/readiness-report.md
  - docs/press-kit/ (if press_outreach)
  - docs/launch/social-content.md
  - docs/launch/email-templates.md
  - public/og-images/
quality_gates:
  - name: readiness_score
    condition: "overall_readiness >= 90%"
    severity: error
  - name: assets_complete
    condition: "all_required_assets_present"
    severity: error
  - name: tracking_verified
    condition: "analytics_events_configured"
    severity: warning
handoffs:
  - label: Ship Product
    agent: speckit.ship
    condition: "NOT deployed"
  - label: Setup Monitoring
    agent: speckit.monitor
    condition: "launch_day AND monitoring_needed"
  - label: Continue Implementation
    agent: speckit.implement
    condition: "readiness_score < 90%"
---

# /speckit.launch

## Purpose

Automate the entire go-to-market process for product launches, including readiness assessment, asset generation, channel preparation, and launch day coordination.

## When to Use

- Product is ready for public release
- After `/speckit.ship` has deployed to production
- Preparing for Product Hunt, Hacker News, or press launch
- Need comprehensive launch checklist and assets

## Launch Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      /speckit.launch                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐               │
│  │  ASSESS   │───▶│  PREPARE  │───▶│  EXECUTE  │               │
│  └───────────┘    └───────────┘    └───────────┘               │
│       │                │                │                        │
│       ▼                ▼                ▼                        │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐                 │
│  │Readiness│      │ Assets  │      │ Launch  │                 │
│  │ Check   │      │  Gen    │      │  Day    │                 │
│  └─────────┘      └─────────┘      └─────────┘                 │
│       │                │                │                        │
│       ▼                ▼                ▼                        │
│  • Product        • Press Kit     • War Room                    │
│  • Marketing      • Social        • Monitoring                  │
│  • Technical      • Email         • Engagement                  │
│  • Legal          • SEO           • Support                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        Launch Flow                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. ASSESS ──────────────────────────────────────────────────── │
│     │                                                            │
│     ├── Product Readiness    [Features, Performance, Security]  │
│     ├── Marketing Readiness  [Landing, Assets, Copy]            │
│     ├── Technical Readiness  [Analytics, SEO, Monitoring]       │
│     └── Legal Readiness      [ToS, Privacy, Compliance]         │
│                                                                  │
│  2. PREPARE ─────────────────────────────────────────────────── │
│     │                                                            │
│     ├── Press Kit            [Release, Fact Sheet, Bios]        │
│     ├── Social Content       [Twitter Thread, LinkedIn, etc.]   │
│     ├── Email Templates      [Launch, Waitlist, Follow-up]      │
│     ├── Channel Setup        [PH, HN, Communities]              │
│     └── Analytics Config     [Events, UTMs, Goals]              │
│                                                                  │
│  3. EXECUTE ─────────────────────────────────────────────────── │
│     │                                                            │
│     ├── T-7 to T-1           [Final prep, soft launch]          │
│     ├── Launch Day           [Coordinated release]              │
│     └── T+1 to T+7           [Follow-up, iteration]             │
│                                                                  │
│  4. ANALYZE ─────────────────────────────────────────────────── │
│     │                                                            │
│     ├── Metrics Collection   [Traffic, Signups, Conversion]     │
│     ├── Feedback Synthesis   [Comments, Reviews, Requests]      │
│     └── Retrospective        [What worked, what didn't]         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Command Execution

### Step 1: Launch Readiness Assessment

```yaml
readiness_assessment:
  product:
    core_features:
      - check: "MVP features complete"
        verify: "Run feature checklist"
      - check: "Critical bugs fixed"
        verify: "Check issue tracker"
      - check: "Performance optimized"
        verify: "Core Web Vitals report"

    user_experience:
      - check: "Onboarding flow smooth"
        verify: "Test signup to value"
      - check: "Error handling graceful"
        verify: "Trigger error states"
      - check: "Mobile responsive"
        verify: "Test on devices"

  marketing:
    landing_page:
      - check: "Value proposition clear"
        verify: "5-second test"
      - check: "CTA prominent"
        verify: "Above fold, contrasting"
      - check: "Social proof present"
        verify: "Testimonials, logos"

    assets:
      - check: "Screenshots ready"
        verify: "High-res, annotated"
      - check: "Demo video created"
        verify: "30-90 seconds"
      - check: "OG images set"
        verify: "All platforms"

  technical:
    analytics:
      - check: "Tracking installed"
        verify: "Events firing"
      - check: "UTM scheme defined"
        verify: "All channels covered"
      - check: "Conversion goals set"
        verify: "Goals in dashboard"

    seo:
      - check: "Meta tags complete"
        verify: "Title, description"
      - check: "Sitemap submitted"
        verify: "Search Console"
      - check: "Structured data valid"
        verify: "Rich results test"

    infrastructure:
      - check: "Monitoring active"
        verify: "Dashboards, alerts"
      - check: "Scaling ready"
        verify: "Load test passed"
      - check: "Backups verified"
        verify: "Restore tested"

  legal:
    compliance:
      - check: "Terms of Service"
        verify: "Accessible, dated"
      - check: "Privacy Policy"
        verify: "GDPR/CCPA compliant"
      - check: "Cookie consent"
        verify: "Banner functional"

# Output: readiness-report.md with scores
```

### Step 2: Asset Generation

```yaml
asset_generation:
  press_kit:
    enabled: "{{press_outreach}}"
    files:
      - "docs/press-kit/press-release.md"
      - "docs/press-kit/fact-sheet.md"
      - "docs/press-kit/founder-bios.md"
      - "docs/press-kit/media-assets.zip"

  social_content:
    twitter:
      - type: "launch_thread"
        posts: 5-7
        includes: ["hook", "problem", "solution", "features", "cta"]
      - type: "announcement"
        length: "280 chars"

    linkedin:
      - type: "announcement"
        length: "1300 chars"
        structure: ["hook", "story", "features", "cta"]

    # Additional platforms as needed

  email_templates:
    - name: "launch_announcement"
      audience: "waitlist"
      subject_lines: 3  # A/B test options

    - name: "early_access"
      audience: "beta_users"

    - name: "press_pitch"
      audience: "journalists"
      enabled: "{{press_outreach}}"

  og_images:
    - "public/og-default.png"     # 1200x630
    - "public/og-twitter.png"     # 1200x675
    - "public/og-launch.png"      # Special launch variant
```

### Step 3: Channel Preparation

```yaml
channel_prep:
  product_hunt:
    enabled: "{{channels.includes('product-hunt')}}"
    tasks:
      - "Create ship page"
      - "Upload all assets"
      - "Write tagline (60 chars)"
      - "Write description (260 chars)"
      - "Draft maker comment"
      - "Prepare gallery images (5+)"
      - "Schedule launch (12:01 AM PT)"
      - "Notify supporters"

  hacker_news:
    enabled: "{{channels.includes('hacker-news')}}"
    tasks:
      - "Draft Show HN post"
      - "Prepare technical details"
      - "Plan posting time (9-10 AM ET)"
      - "Prepare for tough questions"

  twitter:
    enabled: "{{channels.includes('twitter')}}"
    tasks:
      - "Schedule launch thread"
      - "Prepare engagement responses"
      - "Set up monitoring"
      - "List supporters to tag"

  linkedin:
    enabled: "{{channels.includes('linkedin')}}"
    tasks:
      - "Draft announcement post"
      - "Identify groups to share in"
      - "Prepare employee amplification"

  email:
    enabled: "{{channels.includes('email')}}"
    tasks:
      - "Segment waitlist"
      - "Schedule launch email"
      - "Prepare follow-up sequence"
      - "Test deliverability"

  press:
    enabled: "{{press_outreach}}"
    tasks:
      - "Finalize press kit"
      - "Build journalist list"
      - "Send embargoed previews"
      - "Schedule distribution"
```

### Step 4: Launch Day Coordination

```yaml
launch_day:
  war_room:
    setup:
      - "Create #launch-war-room channel"
      - "Open all dashboards"
      - "Brief team on roles"
      - "Test escalation paths"

    schedule:
      "00:00": "Product Hunt goes live"
      "06:00": "Morning shift starts"
      "09:00": "Email blast to waitlist"
      "10:00": "Hacker News post"
      "12:00": "Midday metrics check"
      "15:00": "Press release (if applicable)"
      "18:00": "Evening engagement push"
      "21:00": "Day 1 wrap-up"

    monitoring:
      metrics:
        - "Real-time visitors"
        - "Signup rate"
        - "Error rate"
        - "Product Hunt rank"

      alerts:
        - "Error rate > 1%"
        - "Response time > 2s"
        - "Conversion < expected"

    engagement:
      - "Respond to ALL Product Hunt comments"
      - "Reply to tweets within 15 min"
      - "Answer HN questions promptly"
      - "Thank supporters publicly"
```

### Step 5: Post-Launch Analysis

```yaml
post_launch:
  day_1_metrics:
    - unique_visitors
    - signups
    - activation_rate
    - product_hunt_rank
    - social_mentions
    - press_coverage

  week_1_tasks:
    - "Daily metrics tracking"
    - "Feedback synthesis"
    - "Bug fixes"
    - "Testimonial collection"
    - "Press follow-ups"

  retrospective:
    questions:
      - "What worked well?"
      - "What didn't work?"
      - "What surprised us?"
      - "What would we do differently?"

    documentation:
      - "Metrics summary"
      - "Key learnings"
      - "Recommendations for next launch"
```

## Output Structure

```
docs/
├── launch/
│   ├── launch-plan.md           # Timeline and assignments
│   ├── readiness-report.md      # Pre-launch checklist results
│   ├── social-content.md        # All social posts
│   ├── email-templates.md       # Email copy
│   └── retrospective.md         # Post-launch analysis
│
├── press-kit/                   # If press_outreach enabled
│   ├── press-release.md
│   ├── fact-sheet.md
│   ├── founder-bios.md
│   └── media-assets/
│       ├── logo-pack/
│       ├── screenshots/
│       └── headshots/
│
public/
├── og-default.png
├── og-twitter.png
└── og-launch.png
```

## Quality Gates

| Gate | Condition | Severity | Action if Failed |
|------|-----------|----------|------------------|
| Readiness Score | >= 90% | Error | Block launch, address gaps |
| Assets Complete | All required present | Error | Generate missing assets |
| Tracking Verified | Events firing | Warning | Fix before launch |
| Team Briefed | Roles assigned | Warning | Brief team |
| Channels Ready | All scheduled | Warning | Complete setup |

## Launch Timing Recommendations

```yaml
timing:
  product_hunt:
    best_days: ["Tuesday", "Wednesday", "Thursday"]
    launch_time: "12:01 AM PT"
    avoid: ["Fridays", "Weekends", "Major holidays"]

  hacker_news:
    best_times: ["9-10 AM ET", "1-2 PM ET"]
    best_days: ["Tuesday", "Wednesday"]
    avoid: ["Major news days", "Weekends"]

  general:
    avoid:
      - "Major tech conferences"
      - "Apple/Google announcements"
      - "Elections, major news"
      - "End of quarter (budget freezes)"

    consider:
      - "Industry events (related)"
      - "Seasonal relevance"
      - "Team availability"
```

## Contingency Plans

```yaml
contingencies:
  site_down:
    trigger: "Uptime < 99% or error rate > 5%"
    actions:
      - "Notify team immediately"
      - "Switch to status page"
      - "Deploy rollback if needed"
      - "Communicate on social"
    owner: "Engineering"

  viral_load:
    trigger: "Traffic > 10x baseline"
    actions:
      - "Scale infrastructure"
      - "Enable aggressive caching"
      - "Prioritize critical paths"
    owner: "Engineering"

  negative_feedback:
    trigger: "Significant criticism"
    actions:
      - "Assess validity"
      - "Prepare response"
      - "Engage constructively"
      - "Document learnings"
    owner: "Founder"

  low_engagement:
    trigger: "PH rank dropping, low comments"
    actions:
      - "Boost social promotion"
      - "Activate supporter network"
      - "Consider timing for next push"
    owner: "Marketing"
```

## Integration Points

| Command | Integration |
|---------|-------------|
| `/speckit.ship` | Prerequisites - product must be deployed |
| `/speckit.monitor` | Launch day monitoring dashboards |
| `/speckit.implement` | If readiness check fails |
| `/speckit.integrate` | Analytics integration needed |

## Usage

```bash
# Full launch preparation
speckit launch "ProductName" --date 2024-02-15 --channels product-hunt,twitter,email

# With press outreach
speckit launch "ProductName" --date 2024-02-15 --press-outreach

# Quick launch (minimal channels)
speckit launch "ProductName" --date 2024-02-15 --channels twitter,email

# Check readiness only
speckit launch "ProductName" --readiness-check-only
```

## Success Metrics

```yaml
success_metrics:
  launch_day:
    product_hunt_rank: "Top 5"
    signups: "> 100"
    conversion_rate: "> 5%"

  week_1:
    total_signups: "> 500"
    activation_rate: "> 30%"
    press_mentions: "> 3"

  indicators_of_success:
    - "Organic word-of-mouth sharing"
    - "Unsolicited testimonials"
    - "Feature requests (signal of engagement)"
    - "Return visits"
```

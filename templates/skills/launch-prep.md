# Launch Prep Skill

## Purpose

Prepare and execute product launches with comprehensive checklists, asset generation, and go-to-market coordination.

## Trigger

- User is preparing to launch a product
- After `/speckit.ship` when product is ready for public release
- User asks about launch strategy or Product Hunt

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `product_name` | Yes | Name of the product being launched |
| `launch_date` | Yes | Target launch date |
| `launch_channels` | No | Channels to launch on (Product Hunt, HN, etc.) |
| `press_outreach` | No | Whether to do press outreach |

## Skill Execution

### Step 1: Launch Readiness Assessment

```yaml
readiness_check:
  product:
    - name: "Core Features Complete"
      check: "All MVP features implemented and tested"
      status: "{{pass|fail|skip}}"

    - name: "Performance Optimized"
      check: "Core Web Vitals passing, load time < 3s"
      status: "{{pass|fail|skip}}"

    - name: "Security Audit"
      check: "No critical vulnerabilities, HTTPS enforced"
      status: "{{pass|fail|skip}}"

    - name: "Error Handling"
      check: "Graceful error pages, logging configured"
      status: "{{pass|fail|skip}}"

  marketing:
    - name: "Landing Page"
      check: "Value prop clear, CTA prominent, mobile responsive"
      status: "{{pass|fail|skip}}"

    - name: "Visual Assets"
      check: "Screenshots, demo video, OG images ready"
      status: "{{pass|fail|skip}}"

    - name: "Copy Complete"
      check: "Tagline, descriptions, FAQ written"
      status: "{{pass|fail|skip}}"

  technical:
    - name: "Analytics"
      check: "Tracking configured, conversion events defined"
      status: "{{pass|fail|skip}}"

    - name: "SEO"
      check: "Meta tags, sitemap, structured data"
      status: "{{pass|fail|skip}}"

    - name: "Monitoring"
      check: "Alerting active, dashboards ready"
      status: "{{pass|fail|skip}}"

  legal:
    - name: "Terms of Service"
      check: "ToS published and accessible"
      status: "{{pass|fail|skip}}"

    - name: "Privacy Policy"
      check: "Privacy policy compliant with jurisdictions"
      status: "{{pass|fail|skip}}"

readiness_score:
  formula: "(passed_checks / total_checks) * 100"
  thresholds:
    green: ">= 90%"
    yellow: "70-89%"
    red: "< 70%"
```

### Step 2: Generate Launch Assets

```yaml
asset_generation:
  press_kit:
    - file: "docs/press-kit/press-release.md"
      template: "templates/shared/launch/press-kit.md#press-release"

    - file: "docs/press-kit/fact-sheet.md"
      template: "templates/shared/launch/press-kit.md#fact-sheet"

    - file: "docs/press-kit/founder-bios.md"
      template: "templates/shared/launch/press-kit.md#founder-bios"

  social_content:
    twitter_thread:
      - "🚀 We're launching {{product_name}} today!"
      - "The problem: {{problem_statement}}"
      - "The solution: {{solution_summary}}"
      - "Key features: {{feature_list}}"
      - "Try it now: {{url}} {{hashtags}}"

    linkedin_post: |
      Excited to announce the launch of {{product_name}}!

      {{problem_statement}}

      That's why we built {{product_name}} - {{solution_summary}}.

      Key features:
      {{feature_bullets}}

      Try it today: {{url}}

      #{{hashtag1}} #{{hashtag2}} #{{hashtag3}}

  email_templates:
    launch_announcement:
      subject: "{{product_name}} is live! 🚀"
      preview: "{{tagline}} - Try it now"

    waitlist_notification:
      subject: "You're in! {{product_name}} is ready"
      preview: "Thanks for waiting - here's your early access"

  product_hunt:
    tagline: "{{tagline_60_chars}}"
    description: "{{description_260_chars}}"
    first_comment: |
      Hey Product Hunt! 👋

      I'm {{founder_name}}, {{founder_title}} of {{product_name}}.

      **Why we built this:**
      {{origin_story}}

      **What it does:**
      {{key_features}}

      **What's next:**
      {{roadmap_preview}}

      Would love your feedback! Happy to answer any questions. 🙏
```

### Step 3: Configure Analytics & Tracking

```yaml
analytics_setup:
  events_to_track:
    acquisition:
      - page_view
      - landing_page_visit
      - source_attribution

    activation:
      - signup_started
      - signup_completed
      - onboarding_step_1
      - onboarding_complete

    engagement:
      - feature_used
      - return_visit
      - session_duration

    conversion:
      - trial_started
      - upgrade_clicked
      - purchase_completed

    referral:
      - share_clicked
      - invite_sent
      - referral_signup

  utm_scheme:
    product_hunt: "?utm_source=producthunt&utm_medium=referral&utm_campaign={{year}}-launch"
    twitter: "?utm_source=twitter&utm_medium=social&utm_campaign={{year}}-launch"
    linkedin: "?utm_source=linkedin&utm_medium=social&utm_campaign={{year}}-launch"
    hacker_news: "?utm_source=hackernews&utm_medium=referral&utm_campaign={{year}}-launch"
    email: "?utm_source=email&utm_medium=email&utm_campaign={{year}}-launch-announcement"
    press: "?utm_source=press&utm_medium=referral&utm_campaign={{year}}-launch"

  conversion_goals:
    primary: "signup_completed"
    secondary: ["trial_started", "feature_used"]
    revenue: "purchase_completed"
```

### Step 4: Create Launch Timeline

```yaml
launch_timeline:
  t_minus_7:
    - "Finalize all marketing assets"
    - "Complete press kit"
    - "Schedule social media posts"
    - "Prepare email campaigns"
    - "Test all tracking"

  t_minus_3:
    - "Soft launch to beta users"
    - "Collect initial feedback"
    - "Fix critical issues"
    - "Prepare Product Hunt ship page"

  t_minus_1:
    - "Final production verification"
    - "Pre-schedule Product Hunt launch"
    - "Brief team on launch day roles"
    - "Set up war room communication"

  launch_day:
    "00:00": "Product Hunt goes live (12:01 AM PT)"
    "06:00": "Morning social push (US East)"
    "09:00": "Email to waitlist"
    "10:00": "Hacker News Show HN post"
    "12:00": "Midday engagement check"
    "15:00": "Press release distribution"
    "18:00": "Evening social push"
    "21:00": "Day 1 wrap-up"

  t_plus_1:
    - "Compile Day 1 metrics"
    - "Respond to all comments/feedback"
    - "Address critical issues"
    - "Thank early supporters"

  t_plus_7:
    - "Week 1 retrospective"
    - "Collect testimonials"
    - "Plan follow-up content"
    - "Iterate based on feedback"
```

### Step 5: War Room Setup

```yaml
war_room:
  channels:
    primary: "#launch-war-room"
    alerts: "#launch-alerts"
    support: "#launch-support"

  dashboards:
    - "Product Hunt live stats"
    - "Real-time analytics (PostHog/GA)"
    - "Error monitoring (Sentry)"
    - "Infrastructure (Grafana)"

  escalation:
    p0_critical:
      definition: "Site down, payments broken, data loss"
      response: "All hands, immediate"
      notify: ["founders", "engineering"]

    p1_high:
      definition: "Major feature broken, conversion blocked"
      response: "Within 30 minutes"
      notify: ["engineering", "support"]

    p2_medium:
      definition: "Minor issues, workarounds exist"
      response: "Within 2 hours"
      notify: ["engineering"]

  roles:
    founder:
      - "Product Hunt engagement"
      - "Press inquiries"
      - "Strategic decisions"

    marketing:
      - "Social media monitoring"
      - "Community engagement"
      - "Content publishing"

    engineering:
      - "System monitoring"
      - "Bug fixes"
      - "Performance issues"

    support:
      - "User questions"
      - "Bug reports"
      - "Feedback collection"
```

## Output Format

```yaml
launch_prep_output:
  readiness_report:
    file: "docs/launch/readiness-report.md"
    sections:
      - Product Readiness Score
      - Marketing Readiness Score
      - Technical Readiness Score
      - Legal Readiness Score
      - Overall Launch Readiness
      - Blockers and Risks

  launch_plan:
    file: "docs/launch/launch-plan.md"
    sections:
      - Timeline (T-7 to T+7)
      - Team Assignments
      - Channel Strategy
      - Contingency Plans

  assets_generated:
    - "docs/press-kit/"
    - "docs/launch/social-content.md"
    - "docs/launch/email-templates.md"
    - "public/og-images/"

  tracking_configured:
    - "Analytics events defined"
    - "UTM scheme documented"
    - "Conversion goals set"

  next_steps:
    - "Review and approve all assets"
    - "Add API keys to production"
    - "Schedule automated posts"
    - "Brief team on responsibilities"
```

## Launch Channel Strategies

### Product Hunt

```yaml
product_hunt:
  timing:
    best_day: "Tuesday-Thursday"
    launch_time: "12:01 AM PT"
    reason: "Full 24-hour cycle, active community"

  preparation:
    - "Build hunter relationship (if using one)"
    - "Prepare ship page 1 week early"
    - "Write compelling first comment"
    - "Notify supporters to engage early"
    - "Prepare responses for common questions"

  day_of:
    - "Monitor and respond to every comment"
    - "Share on social with link"
    - "Update with milestones"
    - "Thank supporters publicly"

  success_metrics:
    top_5: "Strong launch, significant exposure"
    top_10: "Good launch, solid validation"
    top_20: "Decent visibility"
    below_20: "Limited impact, analyze and iterate"
```

### Hacker News

```yaml
hacker_news:
  post_format:
    title: "Show HN: {{product_name}} – {{one_line_description}}"
    text: |
      Hey HN!

      {{brief_intro}}

      {{problem_you_solve}}

      {{how_it_works}}

      {{tech_stack_if_interesting}}

      Would love feedback on {{specific_question}}.

      {{url}}

  timing:
    best_times: ["9-10 AM ET", "1-2 PM ET"]
    best_days: ["Tuesday", "Wednesday", "Thursday"]
    avoid: "Weekends, major news days"

  engagement:
    - "Respond to every comment quickly"
    - "Be genuine and humble"
    - "Accept criticism gracefully"
    - "Share technical details when asked"
```

## Quality Gates

| Gate | Condition | Severity |
|------|-----------|----------|
| Readiness Score | >= 90% | Error |
| Assets Complete | All required assets generated | Error |
| Tracking Verified | Analytics events firing | Warning |
| Team Briefed | All roles assigned | Warning |

## Integration

This skill is used by:
- `/speckit.launch` - Main launch workflow
- `/speckit.ship` - Post-deployment launch preparation

References:
- `templates/shared/launch/gtm-checklist.md` - Full go-to-market checklist
- `templates/shared/launch/press-kit.md` - Press kit templates
- `templates/shared/launch/seo-setup.md` - SEO configuration

---
name: launch
description: Automate product launch and go-to-market activities
version: 1.0.0
persona: marketing-agent
model: opus
thinking_budget: 16000

skills:
  - launch-prep
  - seo-optimizer
  - press-kit-generator

flags:
  - name: --thinking-depth
    type: choice
    choices: [standard, ultrathink]
    default: standard
    description: |
      Thinking budget per agent:
      - standard: 16K budget, launch prep, 120s (~$0.24) [RECOMMENDED]
      - ultrathink: 48K budget, deep market analysis, 240s (~$0.72)
  - name: --max-model
    type: string
    default: null
    description: "--max-model <opus|sonnet|haiku> - Override model cap"

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
  growth_focus:
    type: enum
    options: [community, directories, viral, partnerships, all]
    required: false
    default: all
    description: Zero-budget growth strategies to focus on
outputs:
  - docs/launch/launch-plan.md
  - docs/launch/readiness-report.md
  - docs/press-kit/ (if press_outreach)
  - docs/launch/social-content.md
  - docs/launch/email-templates.md
  - docs/launch/growth-playbook.md
  - docs/launch/directory-tracker.md
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
claude_code:
  model: opus
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
        timeout_per_agent: 180000
        retry_on_failure: 1
      pro:
        thinking_budget: 8000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
        timeout_per_agent: 300000
        retry_on_failure: 2
      max:
        thinking_budget: 16000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
        timeout_per_agent: 900000
        retry_on_failure: 3
      ultrathink:
        thinking_budget: 48000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 3.0
  depth_defaults:
    standard:
      thinking_budget: 8000
      skip_agents: []
      timeout: 120
    ultrathink:
      thinking_budget: 48000
      additional_agents: [launch-deepdive, market-analyst]
      timeout: 240
  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 8000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (48K thinking budget).
          Auto-downgrading to **Standard** mode (8K budget).
  cost_breakdown:
    standard: {cost: $0.24, time: "120-150s"}
    ultrathink: {cost: $0.72, time: "240-280s"}
  cache_control:
    system_prompt: ephemeral
    constitution: ephemeral
    templates: ephemeral
    artifacts: ephemeral
    ttl: session
  cache_hierarchy: full
  orchestration:
    max_parallel: 6
    conflict_resolution: queue
    timeout_per_agent: 600000
    retry_on_failure: 2
    role_isolation: true
    wave_overlap:
      enabled: true
      threshold: 0.65
  operation_batching:
    enabled: true
    skip_flag: "--sequential"
    framework: templates/shared/operation-batching.md
  subagents:
    # Wave 1: Content Generation (parallel)
    - role: release-notes-generator
      role_group: DOCS
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Generate comprehensive release notes for the product launch.

        Analyze:
        - Recent git commits and changelog
        - Feature specifications in specs/
        - User-facing changes and improvements

        Generate:
        - Clear, user-friendly release notes
        - Feature highlights with benefits
        - Breaking changes (if any)
        - Migration notes (if applicable)

        Output:
        - docs/launch/release-notes.md
        - Key features summary for other agents

    - role: changelog-compiler
      role_group: DOCS
      parallel: true
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        Compile and format the project changelog for launch.

        Tasks:
        - Parse existing CHANGELOG.md
        - Extract entries since last release
        - Format for public consumption
        - Group by category (Added, Changed, Fixed, etc.)

        Output:
        - Formatted changelog section for launch materials
        - Version number and date confirmation

    # Wave 2: Marketing Assets (depends on content generation)
    - role: press-kit-generator
      role_group: MARKETING
      parallel: true
      depends_on: [release-notes-generator]
      priority: 20
      model_override: sonnet
      prompt: |
        Generate complete press kit for product launch.

        Using release notes and product information:

        Create:
        - docs/press-kit/press-release.md (journalist-ready)
        - docs/press-kit/fact-sheet.md (key stats and features)
        - docs/press-kit/founder-bios.md (team bios)
        - Media asset requirements checklist

        Format:
        - Professional press release style
        - Quotable founder statements
        - Key metrics and differentiators

        Output:
        - Complete press kit directory
        - Media distribution list suggestions

    - role: announcement-drafter
      role_group: MARKETING
      parallel: true
      depends_on: [release-notes-generator]
      priority: 20
      model_override: sonnet
      prompt: |
        Draft launch announcements for all channels.

        Using release notes and product details:

        Create for each channel:
        - Twitter/X: Launch thread (5-7 tweets)
        - LinkedIn: Long-form announcement
        - Product Hunt: Tagline, description, maker comment
        - Hacker News: Show HN post draft
        - Email: Waitlist announcement template

        Follow channel best practices:
        - Character limits
        - Optimal posting times
        - CTA placement
        - Hashtag strategy

        Output:
        - docs/launch/social-content.md
        - docs/launch/email-templates.md
        - Platform-specific formatting

    # Wave 3: Coordination (depends on all assets)
    - role: distribution-coordinator
      role_group: MARKETING
      parallel: true
      depends_on: [press-kit-generator, announcement-drafter]
      priority: 30
      model_override: haiku
      prompt: |
        Coordinate launch distribution and create launch plan.

        Compile all generated assets into:

        1. Launch Plan (docs/launch/launch-plan.md):
           - Timeline with specific dates/times
           - Channel posting schedule
           - Team responsibilities
           - War room setup checklist

        2. Readiness Report (docs/launch/readiness-report.md):
           - Asset completion status
           - Quality gate results
           - Risk assessment
           - Go/No-Go recommendation

        3. Growth Playbook (docs/launch/growth-playbook.md):
           - Directory submission tracker
           - Community engagement plan
           - Partnership opportunities

        Output:
        - Complete launch documentation
        - Readiness score (target: >= 90%)
        - Action items for any gaps
flags:
  max_model: "--max-model <opus|sonnet|haiku>"  # Override model cap
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

### Step 3.5: Zero-Budget Growth Strategies

> **Philosophy**: Launch day is just the beginning. Sustainable growth requires consistent effort over 6-12 months. Time investment > money investment. Authenticity wins over promotion.

```yaml
zero_budget_growth:
  mindset:
    principles:
      - "Compound effects take 6-12 months"
      - "Be genuinely helpful first, promotional second"
      - "Build relationships, not just links"
      - "Consistency > intensity"

    time_allocation:
      daily: "30-60 min community engagement"
      weekly: "2-3 hours content creation"
      monthly: "Directory submissions, partnership outreach"
```

#### 3.5.1 Community Growth Playbook

```yaml
community_growth:
  reddit:
    philosophy: "95/5 rule - 95% value, 5% product mention"

    preparation:
      timeline: "2-3 months before launch"
      actions:
        - "Create personal account (NOT corporate)"
        - "Build karma organically with helpful comments"
        - "Become known in relevant communities"
        - "NEVER use new accounts for promotion"

    target_subreddits:
      general:
        - r/SaaS
        - r/startups
        - r/Entrepreneur
        - r/smallbusiness
        - r/InternetIsBeautiful
        - r/SideProject

      tech_specific:
        - r/webdev
        - r/programming
        - r/devops
        - r/selfhosted
        - r/opensource

      industry_specific:
        - "r/[your_industry]"
        - "Find via redditlist.com"

    content_strategy:
      allowed:
        - "Share journey/story posts"
        - "Ask for feedback genuinely"
        - "Answer questions in your domain"
        - "Comment with expertise first"

      forbidden:
        - "Direct product links in posts"
        - "Self-promotion without context"
        - "New accounts posting"
        - "Multiple posts same day"
        - "Asking for upvotes"

    example_post: |
      Title: "I built [X] after struggling with [Problem] - feedback?"
      Body: Story about problem, why existing solutions failed,
            what you built, specific questions for community.
            Link in comments if asked.

  indie_hackers:
    why: "23% conversion rate vs Product Hunt 3%"

    content_types:
      high_performing:
        - "Revenue milestone posts ($100 MRR, $1K MRR)"
        - "Challenge/failure posts with lessons"
        - "Building in public updates"
        - "Detailed launch retrospectives"

      avoid:
        - "Pure promotional posts"
        - "Vague updates without numbers"

    engagement:
      - "Comment on 5-10 posts daily"
      - "Share genuine insights from experience"
      - "Build relationships with other founders"
      - "Respond to every comment on your posts"

    product_listing:
      - "Add to IH Products directory"
      - "Update weekly with progress"
      - "Respond to all questions"

  discord_slack_communities:
    approach: "Join → Help → Beta test → Mention"

    target_communities:
      - "Industry-specific Discords"
      - "Tool-specific communities (Figma, Notion, etc.)"
      - "Slack groups (OnDeck, Lenny's, etc.)"
      - "Founder communities"

    engagement_playbook:
      week_1_4: "Observe and help"
      week_5_8: "Share expertise, answer questions"
      week_9_12: "Soft mention when relevant"
      ongoing: "Genuine community member"

    rules:
      - "Read community rules FIRST"
      - "Never DM spam"
      - "Contribute before asking"
      - "Offer beta access, not sales pitches"

  hacker_news:
    # Beyond Show HN
    strategies:
      show_hn:
        - "Technical focus, not marketing"
        - "Answer every question"
        - "Be humble about limitations"

      organic:
        - "Comment with genuine expertise"
        - "Share technical blog posts"
        - "Engage in relevant discussions"

    timing:
      best: ["9-10 AM ET", "1-2 PM ET"]
      avoid: ["Weekends", "Major news days"]
```

#### 3.5.2 Directory & Listing Submissions

```yaml
directory_listings:
  strategy:
    batch_size: "10-20 per week"
    priority: "Start with Tier 1, work down"
    track_in: "docs/launch/directory-tracker.md"

  tier_1_essential:
    description: "High traffic, high authority - submit first"
    sites:
      - name: "G2"
        url: "g2.com"
        type: "B2B reviews"
        free: true
        priority: "critical"
        notes: "Target 100+ reviews for visibility"

      - name: "Capterra"
        url: "capterra.com"
        type: "Software reviews"
        free: true
        priority: "critical"
        notes: "Huge SMB traffic, owned by Gartner"

      - name: "TrustRadius"
        url: "trustradius.com"
        type: "B2B reviews"
        free: true
        priority: "high"
        notes: "Enterprise focus"

      - name: "AlternativeTo"
        url: "alternativeto.net"
        type: "Alternative finder"
        free: true
        priority: "critical"
        notes: "Position against competitors"

      - name: "GetApp"
        url: "getapp.com"
        type: "Comparison"
        free: true
        priority: "high"
        notes: "Side-by-side comparison"

      - name: "Product Hunt"
        url: "producthunt.com"
        type: "Launch platform"
        free: true
        priority: "critical"
        notes: "Covered in main launch"

      - name: "Software Advice"
        url: "softwareadvice.com"
        type: "B2B reviews"
        free: true
        priority: "high"
        notes: "Gartner network"

  tier_2_saas_directories:
    description: "SaaS-specific directories"
    sites:
      - name: "SaaSHub"
        url: "saashub.com"
        notes: "Large SaaS directory"

      - name: "SaaSworthy"
        url: "saasworthy.com"
        notes: "75K+ software listed"

      - name: "SoftwareSuggest"
        url: "softwaresuggest.com"
        notes: "India-focused, global reach"

      - name: "SourceForge"
        url: "sourceforge.net"
        notes: "Dev tools, open source"

      - name: "Crozdesk"
        url: "crozdesk.com"
        notes: "B2B software"

      - name: "Serchen"
        url: "serchen.com"
        notes: "Cloud services"

      - name: "Slashdot"
        url: "slashdot.org"
        notes: "Tech news, software"

      - name: "FileHippo"
        url: "filehippo.com"
        notes: "Software downloads"

      - name: "Softpedia"
        url: "softpedia.com"
        notes: "Software reviews"

      - name: "CNET Downloads"
        url: "download.cnet.com"
        notes: "Large audience"

  tier_3_startup_launch_sites:
    description: "Startup launch and discovery"
    sites:
      - name: "BetaList"
        url: "betalist.com"
        notes: "Pre-launch, $129 for instant"

      - name: "Launching Next"
        url: "launchingnext.com"
        notes: "Startup launches"

      - name: "BetaPage"
        url: "betapage.co"
        notes: "Beta testing community"

      - name: "StartupLift"
        url: "startuplift.com"
        notes: "Startup feedback"

      - name: "StartupBuffer"
        url: "startupbuffer.com"
        notes: "Startup promotion"

      - name: "Startup Ranking"
        url: "startupranking.com"
        notes: "Startup leaderboard"

      - name: "KillerStartups"
        url: "killerstartups.com"
        notes: "Startup reviews"

      - name: "Land-book"
        url: "land-book.com"
        notes: "Design-focused"

      - name: "StartupStash"
        url: "startupstash.com"
        notes: "Startup resources"

      - name: "SideProjectors"
        url: "sideprojectors.com"
        notes: "Side project marketplace"

      - name: "Launched"
        url: "launched.io"
        notes: "Launch showcase"

      - name: "10words"
        url: "10words.io"
        notes: "Describe in 10 words"

      - name: "Startup Collections"
        url: "startupcollections.com"
        notes: "Curated lists"

  tier_4_business_directories:
    description: "Business and startup databases"
    sites:
      - name: "Crunchbase"
        url: "crunchbase.com"
        priority: "high"
        notes: "Startup database, VC visibility"

      - name: "AngelList"
        url: "angel.co"
        notes: "Startup jobs, funding"

      - name: "F6S"
        url: "f6s.com"
        notes: "Startup programs"

      - name: "Gust"
        url: "gust.com"
        notes: "Investor connections"

      - name: "StartupBlink"
        url: "startupblink.com"
        notes: "Startup ecosystem"

      - name: "Wellfound"
        url: "wellfound.com"
        notes: "Jobs and funding"

      - name: "LinkedIn Company Page"
        url: "linkedin.com"
        priority: "high"
        notes: "Professional network"

  tier_5_niche_specific:
    dev_tools:
      - name: "GitHub Marketplace"
        url: "github.com/marketplace"
        notes: "Developer tools"

      - name: "VS Code Marketplace"
        url: "marketplace.visualstudio.com"
        notes: "VS Code extensions"

      - name: "JetBrains Marketplace"
        url: "plugins.jetbrains.com"
        notes: "IDE plugins"

      - name: "npm"
        url: "npmjs.com"
        notes: "Node packages"

      - name: "PyPI"
        url: "pypi.org"
        notes: "Python packages"

      - name: "DevHunt"
        url: "devhunt.org"
        notes: "Developer tools"

      - name: "Console.dev"
        url: "console.dev"
        notes: "Dev tool newsletter"

      - name: "StackShare"
        url: "stackshare.io"
        notes: "Tech stack sharing"

      - name: "LibHunt"
        url: "libhunt.com"
        notes: "Library discovery"

      - name: "Awesome Lists"
        url: "awesome.re"
        notes: "GitHub awesome lists"

    ai_ml:
      - name: "There's An AI For That"
        url: "theresanaiforthat.com"
        notes: "AI tool directory"

      - name: "AI Tool Hunt"
        url: "aitoolhunt.com"
        notes: "AI tool discovery"

      - name: "Futurepedia"
        url: "futurepedia.io"
        notes: "AI tool directory"

      - name: "TopAI.tools"
        url: "topai.tools"
        notes: "AI rankings"

      - name: "AI Valley"
        url: "aivalley.ai"
        notes: "AI tools"

      - name: "Future Tools"
        url: "futuretools.io"
        notes: "AI resources"

      - name: "AI Scout"
        url: "aiscout.net"
        notes: "AI discovery"

      - name: "Hugging Face"
        url: "huggingface.co"
        notes: "ML models, spaces"

    no_code:
      - name: "NoCode.tech"
        url: "nocode.tech"
        notes: "No-code tools"

      - name: "Makerpad"
        url: "makerpad.co"
        notes: "No-code community"

      - name: "Zapier App Directory"
        url: "zapier.com/apps"
        notes: "Integration listing"

      - name: "Notion Integrations"
        url: "notion.so/integrations"
        notes: "Notion ecosystem"

      - name: "Airtable Marketplace"
        url: "airtable.com/marketplace"
        notes: "Airtable apps"

    design:
      - name: "Dribbble"
        url: "dribbble.com"
        notes: "Design community"

      - name: "Behance"
        url: "behance.net"
        notes: "Portfolio showcase"

      - name: "Figma Community"
        url: "figma.com/community"
        notes: "Figma resources"

      - name: "UI8"
        url: "ui8.net"
        notes: "Design resources"

    marketing:
      - name: "GrowthHackers"
        url: "growthhackers.com"
        notes: "Growth community"

      - name: "Indiehackers Products"
        url: "indiehackers.com/products"
        notes: "IH product listings"

    productivity:
      - name: "Slant"
        url: "slant.co"
        notes: "Product recommendations"

      - name: "AppSumo Marketplace"
        url: "appsumo.com"
        notes: "Lifetime deals"

      - name: "SetApp"
        url: "setapp.com"
        notes: "Mac app bundle"

  tier_6_regional:
    description: "Region-specific directories"
    sites:
      europe:
        - "EU-Startups.com"
        - "Tech.eu"
        - "Sifted.eu"

      asia:
        - "TechInAsia.com"
        - "e27.co"
        - "KrASIA.com"

      latam:
        - "Contxto.com"
        - "LatamList.com"

      india:
        - "YourStory.com"
        - "Inc42.com"

      russia_cis:
        - "vc.ru"
        - "Spark.ru"
        - "Rusbase.com"

  tier_7_aggregators:
    description: "Meta-directories and aggregators"
    sites:
      - name: "BuiltWith"
        url: "builtwith.com"
        notes: "Tech detection"

      - name: "SimilarWeb"
        url: "similarweb.com"
        notes: "Traffic analysis"

      - name: "Wappalyzer"
        url: "wappalyzer.com"
        notes: "Tech profiler"

  submission_checklist:
    per_directory:
      - "Complete profile with logo"
      - "Compelling description (unique per site)"
      - "High-quality screenshots"
      - "Video demo if supported"
      - "Accurate categorization"
      - "Links to documentation"

    ongoing:
      - "Request reviews from happy customers"
      - "Respond to ALL reviews (positive & negative)"
      - "Update quarterly with new features"
      - "Track rankings and traffic"
```

#### 3.5.3 Viral & Referral Loops

```yaml
viral_loops:
  types:
    inherent_virality:
      description: "Product usage naturally involves others"
      examples:
        - "Calendly - share scheduling link"
        - "Zoom - invite to meeting"
        - "Figma - collaborate on design"
        - "Notion - share workspace"

      implementation:
        - "'Powered by [Product]' on outputs"
        - "Share/invite as core action"
        - "Collaboration as value prop"

    incentivized_referrals:
      description: "Rewards for bringing new users"
      structures:
        one_sided:
          - "Give $X credit per referral"
          - "Unlock features at milestones"

        two_sided:
          - "Both referrer and referred get reward"
          - "Higher conversion, higher cost"

      examples:
        - "Dropbox: 500MB per referral"
        - "Uber: Free rides both sides"
        - "Notion: $5 credit per referral"

    waitlist_virality:
      description: "Move up queue by referring"
      mechanics:
        - "Show position in queue"
        - "Refer to jump ahead"
        - "Gamify with leaderboard"

      tools:
        - "Viral Loops"
        - "KickoffLabs"
        - "Custom build"

  implementation_checklist:
    - "Identify natural share moments"
    - "Make sharing 1-click frictionless"
    - "Provide shareable assets (images, links)"
    - "Track attribution (UTMs, referral codes)"
    - "Thank referrers publicly"
    - "A/B test incentive structures"

  metrics:
    k_factor:
      formula: "invites_per_user × conversion_rate"
      target: "> 1 for viral growth"

    referral_rate:
      formula: "referred_users / total_users"
      benchmark: "10-30% is strong"
```

#### 3.5.4 Partnership & Integration Marketing

```yaml
partnership_growth:
  why: "Partners drive ~38% of SaaS revenue on average"

  integration_marketplaces:
    tier_1_must_have:
      - name: "Zapier"
        url: "zapier.com/platform"
        reach: "6M+ users"
        effort: "Medium"
        notes: "Highest ROI for most SaaS"

      - name: "Slack App Directory"
        url: "slack.com/apps"
        reach: "Millions daily active"
        effort: "Medium-High"
        notes: "Great for B2B tools"

      - name: "Chrome Web Store"
        url: "chrome.google.com/webstore"
        reach: "Billions of users"
        effort: "Low-Medium"
        notes: "Extensions, browser tools"

    tier_2_category_specific:
      - name: "Shopify App Store"
        category: "E-commerce"
        notes: "If relevant to merchants"

      - name: "HubSpot Marketplace"
        category: "Marketing/Sales"
        notes: "CRM ecosystem"

      - name: "Salesforce AppExchange"
        category: "Enterprise"
        notes: "Large enterprise reach"

      - name: "WordPress Plugin Directory"
        category: "Web/Content"
        notes: "Massive install base"

      - name: "Atlassian Marketplace"
        category: "Dev/Project Mgmt"
        notes: "Jira, Confluence users"

  co_marketing_playbook:
    types:
      joint_webinars:
        effort: "Medium"
        reach: "Combined audiences"
        template: |
          "How [Your Tool] + [Their Tool] helps [Audience] achieve [Outcome]"

      guest_content:
        effort: "Low-Medium"
        options:
          - "Guest post on partner blog"
          - "Podcast appearance"
          - "Case study feature"

      mutual_promotion:
        effort: "Low"
        options:
          - "Newsletter swap"
          - "Social media cross-promotion"
          - "Integration announcement"

  outreach_template: |
    Subject: Integration idea: {{your_product}} × {{their_product}}

    Hi {{name}},

    I'm {{your_name}}, founder of {{your_product}}. We help {{value_prop}}.

    I noticed many of our users also use {{their_product}}, and I think
    there's a natural integration opportunity:

    {{specific_integration_idea}}

    This could help both our users {{benefit}}.

    Would you be open to a quick call to explore this?

    Best,
    {{your_name}}

  partnership_tiers:
    tier_1_integration:
      commitment: "Build integration"
      ask: "Marketplace listing, co-announcement"

    tier_2_referral:
      commitment: "Mutual recommendation"
      ask: "Affiliate/referral arrangement"

    tier_3_content:
      commitment: "Co-create content"
      ask: "Guest posts, webinars, case studies"
```

#### 3.5.5 Build in Public Strategy

```yaml
build_in_public:
  philosophy: |
    Share your journey authentically. Revenue numbers, challenges, failures.
    Build audience while building product. Turn followers into customers.

  platforms:
    twitter_x:
      why: "Fastest growth, tech-savvy audience"
      content_mix:
        40_percent: "Insights and lessons"
        30_percent: "Behind the scenes"
        20_percent: "Milestones and numbers"
        10_percent: "Product updates"

      content_ideas:
        - "Revenue milestones ($100 MRR, $1K MRR)"
        - "User milestones (100 users, 1000 users)"
        - "Feature shipping announcements"
        - "Challenges and how you solved them"
        - "Decisions and reasoning"
        - "Tech stack insights"
        - "Customer feedback highlights"

      cadence: "1-3 posts per day"
      engagement: "Reply to every comment"

    linkedin:
      why: "B2B audience, longer content"
      content_types:
        - "Founder journey posts"
        - "Business lessons"
        - "Hiring/team updates"
        - "Industry insights"

      cadence: "3-5 posts per week"
      format: "Story-driven, personal"

    indie_hackers:
      why: "Founder community, high engagement"
      content: "Detailed journey posts with numbers"
      cadence: "Weekly or biweekly updates"

  content_rules:
    do:
      - "Share real numbers"
      - "Admit failures and mistakes"
      - "Show the messy process"
      - "Engage with commenters"
      - "Be consistent"
      - "Give more than you ask"

    dont:
      - "Only share wins"
      - "Be promotional every post"
      - "Ignore negative feedback"
      - "Post inconsistently"
      - "Fake numbers or vanity metrics"

  milestone_templates:
    revenue: |
      🎉 Just hit ${{X}} MRR with {{product}}!

      Here's what got us here:
      - {{key_action_1}}
      - {{key_action_2}}
      - {{key_action_3}}

      Biggest lesson: {{lesson}}

      What should we focus on next?

    users: |
      📈 {{product}} just crossed {{X}} users!

      The journey:
      - Month 1: {{early_numbers}}
      - Month 3: {{mid_numbers}}
      - Today: {{current}}

      What worked: {{insight}}

      Thanks to everyone who believed early! 🙏
```

#### 3.5.6 Cold Outreach Playbook

```yaml
cold_outreach:
  prerequisites:
    - "Clear ICP (Ideal Customer Profile)"
    - "5+ testimonials or case studies"
    - "Proven product-market fit signals"
    - "Email deliverability verified"

  finding_prospects:
    tools:
      - "LinkedIn Sales Navigator"
      - "Apollo.io (free tier)"
      - "Hunter.io"
      - "Clearbit"

    sources:
      - "Competitor reviews (G2, Capterra)"
      - "LinkedIn posts about pain point"
      - "Twitter conversations"
      - "Industry events attendees"
      - "Job postings mentioning problem"

  email_sequence:
    email_1_value_first:
      timing: "Day 1"
      goal: "Provide value, ask question"
      template: |
        Subject: Quick question about {{their_challenge}}

        Hi {{name}},

        I noticed {{personalized_observation}}.

        We've helped {{similar_company}} solve {{problem}} and
        achieve {{result}}.

        I put together a quick {{resource}} that might help:
        {{value_link}}

        Curious - how are you currently handling {{challenge}}?

        Best,
        {{your_name}}

    email_2_case_study:
      timing: "Day 3-4"
      goal: "Social proof"
      template: |
        Subject: How {{similar_company}} solved {{problem}}

        Hi {{name}},

        Following up on my last note.

        Wanted to share how {{similar_company}} used {{product}}
        to {{specific_result}}.

        {{brief_case_study_summary}}

        Worth a 15-min chat to see if this applies to {{their_company}}?

        {{your_name}}

    email_3_breakup:
      timing: "Day 10-14"
      goal: "Final attempt, respect time"
      template: |
        Subject: Should I close your file?

        Hi {{name}},

        I've reached out a couple times about {{topic}}.

        I don't want to be a pest, so this will be my last email.

        If {{problem}} becomes a priority, I'm here to help.

        All the best,
        {{your_name}}

  rules:
    - "Personalize every email (no mass blast)"
    - "Max 3 emails per prospect"
    - "Provide value in first touch"
    - "Respect 'not interested' immediately"
    - "Track opens/replies, iterate"

  metrics:
    benchmarks:
      open_rate: "40-60% (cold)"
      reply_rate: "5-15%"
      meeting_rate: "1-5%"
```

#### 3.5.7 Growth Timeline

```yaml
growth_timeline:
  month_1_2:
    focus: "Foundation"
    activities:
      - "Set up all Tier 1 directory listings"
      - "Build Reddit/community karma"
      - "Start Build in Public content"
      - "Join 5-10 relevant communities"

    time_per_week: "5-8 hours"

  month_3_4:
    focus: "Expansion"
    activities:
      - "Complete Tier 2-3 directory submissions"
      - "Launch first integration (Zapier)"
      - "Start partnership outreach"
      - "Implement referral program"

    time_per_week: "8-10 hours"

  month_5_6:
    focus: "Scale"
    activities:
      - "Tier 4-5 directories"
      - "First co-marketing partnership"
      - "Cold outreach to ideal customers"
      - "Optimize based on data"

    time_per_week: "6-8 hours"

  month_7_12:
    focus: "Compound"
    activities:
      - "Double down on what works"
      - "Cut what doesn't"
      - "Automate where possible"
      - "Build on relationships"

    expected_results:
      - "Consistent organic traffic"
      - "Word-of-mouth referrals"
      - "Partnership pipeline"
      - "Community recognition"
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
│   ├── growth-playbook.md       # Zero-budget tactics summary
│   ├── directory-tracker.md     # Listing submission tracker
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

# Focus on specific zero-budget growth strategies
speckit launch "ProductName" --date 2024-02-15 --growth-focus directories
speckit launch "ProductName" --date 2024-02-15 --growth-focus community

# Full zero-budget growth playbook
speckit launch "ProductName" --date 2024-02-15 --growth-focus all
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

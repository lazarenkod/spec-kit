---
description: Automate product launch and go-to-market activities
persona: marketing-agent
inputs:
  product_name: { type: string, required: true }
  launch_date: { type: date, required: true }
  channels: { type: array, default: [product-hunt, twitter, email] }
  press_outreach: { type: boolean, default: false }
  growth_focus: { type: enum, options: [community, directories, viral, partnerships, all], default: all }
outputs:
  - docs/launch/launch-plan.md
  - docs/launch/readiness-report.md
  - docs/launch/growth-playbook.md
  - docs/press-kit/ (if press_outreach)
quality_gates:
  - { name: readiness_score, condition: ">= 90%", severity: error }
  - { name: assets_complete, condition: "all present", severity: error }
  - { name: tracking_verified, condition: "events firing", severity: warning }
handoffs:
  - { label: Ship Product, agent: speckit.ship, condition: "NOT deployed" }
  - { label: Setup Monitoring, agent: speckit.monitor, condition: "launch_day" }
  - { label: Continue Implementation, agent: speckit.implement, condition: "readiness < 90%" }
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 6000
  cache_hierarchy: full
---

## Input
```text
$ARGUMENTS
```

---

## Workflow Overview

```text
ASSESS → PREPARE → EXECUTE → ANALYZE

1. Readiness Check  → readiness-report.md (4 categories)
2. Asset Generation → press-kit/, social-content.md, email-templates.md
3. Channel Setup    → Per-channel task lists
4. Growth Playbook  → growth-playbook.md (5 strategies)
5. Launch Day       → War room, schedule, monitoring
6. Post-Launch      → Metrics, retrospective
```

---

## Step 1: Readiness Assessment

### Categories

| Category | Key Checks | Verify Method |
|----------|------------|---------------|
| **Product** | MVP complete, bugs fixed, Core Web Vitals pass | Feature checklist, issue tracker |
| **Marketing** | Landing page ready, value prop clear, assets present | 5-second test, screenshot review |
| **Technical** | Analytics installed, SEO configured, monitoring active | Events firing, Search Console |
| **Legal** | ToS, Privacy Policy, Cookie consent | Accessible links, GDPR/CCPA |

### Scoring

```text
Overall Readiness = Σ(category_score × weight) / 100
  Product: 30%    Marketing: 25%
  Technical: 25%  Legal: 20%

GATE: readiness >= 90% → proceed
      readiness < 90% → block, address gaps
```

---

## Step 2: Asset Generation

### Press Kit (if press_outreach)

| File | Content |
|------|---------|
| press-release.md | Who, What, When, Why, How + quotes |
| fact-sheet.md | Product details, metrics, pricing |
| founder-bios.md | Team backgrounds, photos |
| media-assets.zip | Logos, screenshots, headshots |

### Social Content

| Platform | Format | Notes |
|----------|--------|-------|
| Twitter | 5-7 post thread | hook → problem → solution → features → CTA |
| LinkedIn | 1300 char post | story structure, professional tone |
| Product Hunt | Tagline (60), Description (260), Maker comment | Schedule 12:01 AM PT |
| Hacker News | Show HN post | Technical focus, honest tone |

### Email Templates

| Template | Audience | A/B Subject Lines |
|----------|----------|-------------------|
| launch_announcement | Waitlist | 3 variants |
| early_access | Beta users | Feature highlights |
| press_pitch | Journalists | Personalized |

### OG Images

- `public/og-default.png` (1200×630)
- `public/og-twitter.png` (1200×675)
- `public/og-launch.png` (launch variant)

---

## Step 3: Channel Preparation

### Task Lists per Channel

| Channel | Key Tasks |
|---------|-----------|
| Product Hunt | Ship page, gallery (5+ images), tagline, description, maker comment, schedule |
| Hacker News | Show HN post, technical details, prepare for tough questions |
| Twitter | Schedule thread, engagement responses, monitoring, supporter tags |
| LinkedIn | Draft post, request reshares, prep engagement |
| Email | Segment lists, schedule blasts, track opens/clicks |

---

## Step 4: Zero-Budget Growth Strategies

### 4.1 Community Building

| Tactic | Effort | Timeline |
|--------|--------|----------|
| Build in Public | Low | Ongoing |
| Discord/Slack community | Medium | Week 2+ |
| Reddit engagement | Low | Immediate |
| Twitter presence | Low | Immediate |
| Newsletter | Medium | Week 1+ |

### 4.2 Directory Submissions

| Tier | Examples | Priority |
|------|----------|----------|
| 1 - Tech Launch | Product Hunt, Hacker News, BetaList | HIGH |
| 2 - Software Aggregators | AlternativeTo, G2, Capterra, SaaSHub | HIGH |
| 3 - Startup Ecosystems | IndieHackers, StartupBase, Launching Next | MEDIUM |
| 4 - Business DBs | Crunchbase, AngelList, LinkedIn | MEDIUM |
| 5 - Niche Specific | DevHunt (dev), TAAFT (AI), NoCode.tech | Per niche |
| 6 - Regional | EU-Startups, TechInAsia, vc.ru | Per region |

**Per submission**: Complete profile, compelling description, screenshots, categorization

### 4.3 Viral Loops

| Type | Mechanics | Example |
|------|-----------|---------|
| Inherent virality | Usage involves others | Calendly, Zoom, Figma |
| Incentivized referral | Rewards for referrals | Dropbox (500MB), Notion ($5) |
| Waitlist virality | Move up queue by referring | Leaderboard, referral codes |

**K-Factor**: `invites_per_user × conversion_rate` (target > 1)

### 4.4 Partnership Marketing

| Type | Effort | ROI |
|------|--------|-----|
| Integration marketplaces | Medium | High (Zapier, Slack, Chrome) |
| Joint webinars | Medium | Combined audiences |
| Guest content | Low | Authority building |
| Newsletter swaps | Low | Quick reach |

---

## Step 5: Launch Day Coordination

### War Room Setup

```text
#launch-war-room channel
Dashboards: Analytics, Error tracking, Social monitoring
Roles: Engineering (site), Marketing (engagement), Support (questions)
```

### Schedule

| Time | Action |
|------|--------|
| 00:00 | Product Hunt live |
| 06:00 | Morning shift starts |
| 09:00 | Email blast |
| 10:00 | Hacker News post |
| 12:00 | Midday metrics |
| 18:00 | Evening push |
| 21:00 | Day 1 wrap-up |

### Monitoring Alerts

| Metric | Threshold | Action |
|--------|-----------|--------|
| Error rate | > 1% | Investigate, rollback if needed |
| Response time | > 2s | Scale, cache |
| Conversion | < expected | Boost promotion |

---

## Step 6: Post-Launch Analysis

### Day 1 Metrics

- Unique visitors, signups, activation rate
- Product Hunt rank, social mentions
- Press coverage (if applicable)

### Week 1 Tasks

- Daily metrics tracking
- Feedback synthesis
- Bug fixes
- Testimonial collection
- Press follow-ups

### Retrospective Template

```text
1. What worked well?
2. What didn't work?
3. What surprised us?
4. What would we do differently?
```

---

## Contingency Plans

| Scenario | Trigger | Actions |
|----------|---------|---------|
| Site down | Uptime < 99%, errors > 5% | Notify team, status page, rollback |
| Viral load | Traffic > 10x baseline | Scale infra, aggressive caching |
| Negative feedback | Significant criticism | Assess, respond constructively |
| Low engagement | PH rank dropping | Boost social, activate supporters |

---

## Timing Recommendations

### Product Hunt
- **Best**: Tuesday-Thursday
- **Launch**: 12:01 AM PT
- **Avoid**: Fridays, weekends, holidays

### Hacker News
- **Best**: Tuesday-Wednesday, 9-10 AM ET
- **Avoid**: Major news days, weekends

### General Avoid
- Major tech conferences
- Apple/Google announcements
- Elections, major news
- End of quarter (budget freezes)

---

## Quality Gates

| Gate | Condition | Severity | If Failed |
|------|-----------|----------|-----------|
| Readiness | >= 90% | Error | Block, address gaps |
| Assets | All present | Error | Generate missing |
| Tracking | Events firing | Warning | Fix before launch |
| Team | Roles assigned | Warning | Brief team |
| Channels | All scheduled | Warning | Complete setup |

---

## Output Structure

```text
docs/
├── launch/
│   ├── launch-plan.md
│   ├── readiness-report.md
│   ├── social-content.md
│   ├── email-templates.md
│   ├── growth-playbook.md
│   ├── directory-tracker.md
│   └── retrospective.md
├── press-kit/ (if enabled)
│   ├── press-release.md
│   ├── fact-sheet.md
│   ├── founder-bios.md
│   └── media-assets/
public/
├── og-default.png
├── og-twitter.png
└── og-launch.png
```

---

## Success Metrics

| Timeframe | Metric | Target |
|-----------|--------|--------|
| Launch Day | PH Rank | Top 5 |
| Launch Day | Signups | > 100 |
| Launch Day | Conversion | > 5% |
| Week 1 | Total Signups | > 500 |
| Week 1 | Activation Rate | > 30% |
| Week 1 | Press Mentions | > 3 |

### Success Indicators
- Organic word-of-mouth sharing
- Unsolicited testimonials
- Feature requests (engagement signal)
- Return visits

---

## Usage

```bash
# Full launch
speckit launch "ProductName" --date 2024-02-15 --channels product-hunt,twitter,email

# With press
speckit launch "ProductName" --date 2024-02-15 --press-outreach

# Readiness check only
speckit launch "ProductName" --readiness-check-only

# Focus growth strategy
speckit launch "ProductName" --date 2024-02-15 --growth-focus directories
```

---

## Context

{ARGS}

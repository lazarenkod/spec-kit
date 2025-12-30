# Go-to-Market Checklist

## Purpose

Comprehensive checklist for product launches, organized by timeline. Ensures nothing is forgotten during the critical launch period.

## Launch Timeline

```
T-14 ──── T-7 ──── T-3 ──── T-1 ──── T-0 ──── T+1 ──── T+7 ──── T+14
  │         │        │        │        │        │        │        │
  │         │        │        │        │        │        │        └── Post-Launch Analysis
  │         │        │        │        │        │        └── Week 1 Follow-up
  │         │        │        │        │        └── Day 1 Response
  │         │        │        │        └── LAUNCH DAY
  │         │        │        └── Final Checks
  │         │        └── Soft Launch / Beta
  │         └── Launch Week Prep
  └── Pre-Launch Prep
```

---

## Pre-Launch (T-14 to T-7)

### Product Readiness

```yaml
product:
  - [ ] Core features complete and tested
  - [ ] Critical bugs fixed, known issues documented
  - [ ] Performance optimized (Core Web Vitals pass)
  - [ ] Security audit completed
  - [ ] Error handling and user feedback implemented
  - [ ] Analytics and tracking configured
  - [ ] Onboarding flow tested end-to-end
```

### Marketing Assets

```yaml
marketing_assets:
  landing_page:
    - [ ] Headline and value proposition finalized
    - [ ] Social proof elements (testimonials, logos)
    - [ ] CTA buttons optimized
    - [ ] Mobile responsive verified
    - [ ] A/B test variants prepared

  visual_assets:
    - [ ] Product screenshots (high-res, annotated)
    - [ ] Demo video / GIF (30-60 seconds)
    - [ ] OG images (1200x630px)
    - [ ] Logo variations (light/dark, sizes)
    - [ ] Favicon and app icons

  copy:
    - [ ] Tagline (< 10 words)
    - [ ] Elevator pitch (30 seconds)
    - [ ] Product description (250 words)
    - [ ] Feature highlights (3-5 key features)
    - [ ] FAQ section
```

### Technical Setup

```yaml
technical:
  seo:
    - [ ] Meta titles and descriptions
    - [ ] Sitemap.xml generated
    - [ ] Robots.txt configured
    - [ ] Structured data (JSON-LD)
    - [ ] Canonical URLs set

  analytics:
    - [ ] Google Analytics / PostHog configured
    - [ ] Conversion events defined
    - [ ] UTM parameter scheme documented
    - [ ] Funnel tracking set up

  infrastructure:
    - [ ] CDN configured
    - [ ] SSL certificate valid
    - [ ] Monitoring and alerting active
    - [ ] Backup systems verified
    - [ ] Scaling plan documented
```

### Communication Prep

```yaml
communications:
  press:
    - [ ] Press release drafted
    - [ ] Press kit assembled
    - [ ] Media list compiled
    - [ ] Embargoed outreach scheduled

  social:
    - [ ] Social media posts drafted
    - [ ] Hashtag strategy defined
    - [ ] Community posts prepared
    - [ ] Influencer outreach initiated

  email:
    - [ ] Launch announcement email
    - [ ] Welcome email sequence
    - [ ] Waitlist notification ready
```

---

## Launch Week (T-7 to T-1)

### Final Preparations

```yaml
final_prep:
  - [ ] Staging environment mirrors production
  - [ ] Load testing completed
  - [ ] Rollback procedure documented
  - [ ] Support documentation ready
  - [ ] Team responsibilities assigned
```

### Soft Launch / Beta

```yaml
soft_launch:
  - [ ] Beta users invited
  - [ ] Feedback collection mechanism active
  - [ ] Critical issues triaged
  - [ ] Final iterations completed
```

### Channel Preparation

```yaml
channels:
  product_hunt:
    - [ ] Ship page created
    - [ ] Hunter confirmed (if using one)
    - [ ] First comment drafted
    - [ ] Assets uploaded
    - [ ] Supporters notified

  hacker_news:
    - [ ] Show HN post drafted
    - [ ] Timing researched (best times)
    - [ ] Response strategy prepared

  reddit:
    - [ ] Relevant subreddits identified
    - [ ] Post content prepared
    - [ ] Community guidelines reviewed

  twitter_x:
    - [ ] Launch thread drafted
    - [ ] Scheduled posts ready
    - [ ] Engagement list prepared
```

### Coordination

```yaml
coordination:
  - [ ] Launch day schedule finalized
  - [ ] Team availability confirmed
  - [ ] Communication channels set up (Slack/Discord)
  - [ ] War room scheduled
  - [ ] Escalation paths documented
```

---

## Launch Day (T-0)

### Morning (Pre-Launch)

```yaml
morning:
  - [ ] Final production verification
  - [ ] Monitoring dashboards open
  - [ ] Team standup completed
  - [ ] Support channels staffed
```

### Launch Execution

```yaml
launch_execution:
  - [ ] Product Hunt launch (12:01 AM PT recommended)
  - [ ] Social media posts published
  - [ ] Email to waitlist sent
  - [ ] Press release distributed
  - [ ] Community posts published
```

### Active Monitoring

```yaml
monitoring:
  - [ ] Traffic and conversion monitoring
  - [ ] Error rate monitoring
  - [ ] Social media engagement tracking
  - [ ] Customer support response
  - [ ] Press coverage tracking
```

### Engagement

```yaml
engagement:
  - [ ] Respond to Product Hunt comments
  - [ ] Reply to tweets and mentions
  - [ ] Answer HN/Reddit comments
  - [ ] Handle support tickets
  - [ ] Thank early adopters
```

---

## Post-Launch (T+1 to T+14)

### Day 1 (T+1)

```yaml
day_1:
  analysis:
    - [ ] Launch metrics compiled
    - [ ] Top feedback themes identified
    - [ ] Critical issues triaged
    - [ ] Press coverage collected

  follow_up:
    - [ ] Thank you posts published
    - [ ] Influencer engagement continued
    - [ ] Support backlog cleared
```

### Week 1 (T+1 to T+7)

```yaml
week_1:
  - [ ] Daily metrics tracking
  - [ ] User feedback synthesized
  - [ ] Bug fixes deployed
  - [ ] Conversion optimization started
  - [ ] Press follow-ups sent
  - [ ] Testimonials collected
```

### Week 2 (T+7 to T+14)

```yaml
week_2:
  - [ ] Launch retrospective completed
  - [ ] Learnings documented
  - [ ] Metrics report generated
  - [ ] Next iteration planned
  - [ ] Case studies drafted
```

---

## Launch Metrics Dashboard

```yaml
metrics_to_track:
  traffic:
    - unique_visitors
    - page_views
    - bounce_rate
    - traffic_sources
    - geographic_distribution

  conversion:
    - signup_rate
    - trial_starts
    - activation_rate
    - conversion_by_source

  engagement:
    - time_on_site
    - pages_per_session
    - feature_adoption
    - return_visits

  social:
    - product_hunt_upvotes
    - twitter_mentions
    - press_coverage
    - backlinks

  quality:
    - error_rate
    - load_time
    - support_tickets
    - nps_score
```

---

## Launch Day War Room

```yaml
war_room:
  schedule:
    "00:00-02:00": "Product Hunt launch, initial monitoring"
    "06:00-08:00": "Morning shift - US East Coast wake up"
    "09:00-12:00": "Peak engagement period"
    "12:00-15:00": "US West Coast peak"
    "15:00-18:00": "Afternoon monitoring"
    "18:00-21:00": "Evening wrap-up"

  roles:
    founder: "Product Hunt engagement, press"
    marketing: "Social media, email, community"
    engineering: "Monitoring, bug fixes"
    support: "Customer tickets, feedback"

  tools:
    monitoring:
      - Grafana dashboard
      - PostHog analytics
      - Product Hunt live stats
    communication:
      - Slack #launch-war-room
      - Zoom for emergencies
    social:
      - TweetDeck / Buffer
      - Mention tracking
```

---

## Contingency Plans

```yaml
contingency:
  site_down:
    trigger: "Error rate > 5% or uptime < 99%"
    response:
      - "Notify team immediately"
      - "Switch to status page"
      - "Deploy rollback if needed"
      - "Communicate on social media"

  viral_load:
    trigger: "Traffic > 10x baseline"
    response:
      - "Scale infrastructure"
      - "Enable caching"
      - "Prioritize critical paths"

  negative_press:
    trigger: "Significant negative coverage"
    response:
      - "Assess validity of criticism"
      - "Prepare official response"
      - "Engage constructively"
      - "Document learnings"

  low_engagement:
    trigger: "PH upvotes < 50 at midday"
    response:
      - "Boost social promotion"
      - "Activate supporter network"
      - "Consider timing for next launch"
```

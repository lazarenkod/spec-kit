# Content Calendar Template

## Purpose

Plan, organize, and execute content marketing across channels. Ensures consistent publishing, strategic alignment, and efficient workflows.

---

## Content Calendar Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                     Content Calendar                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STRATEGY ──────▶ What topics align with goals?                 │
│       │                                                          │
│       ▼                                                          │
│  PLANNING ──────▶ What content types for each channel?          │
│       │                                                          │
│       ▼                                                          │
│  SCHEDULING ────▶ When to publish what?                         │
│       │                                                          │
│       ▼                                                          │
│  PRODUCTION ────▶ Who creates what by when?                     │
│       │                                                          │
│       ▼                                                          │
│  DISTRIBUTION ──▶ How to promote each piece?                    │
│       │                                                          │
│       ▼                                                          │
│  ANALYSIS ──────▶ What performed? What to optimize?             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Monthly Content Calendar Template

```markdown
# [Month Year] Content Calendar

## Monthly Theme: [Theme]

### Goals
- [ ] [Content goal 1]
- [ ] [Content goal 2]

### Content Pillars This Month
1. [Pillar 1] - [% of content]
2. [Pillar 2] - [% of content]
3. [Pillar 3] - [% of content]

---

## Week 1: [Date Range]

| Day | Channel | Content Type | Topic | Status | Owner |
|-----|---------|--------------|-------|--------|-------|
| Mon | Blog | Tutorial | [Topic] | Draft | @name |
| Tue | Twitter | Thread | [Topic] | Scheduled | @name |
| Wed | LinkedIn | Post | [Topic] | Published | @name |
| Thu | Email | Newsletter | [Topic] | Draft | @name |
| Fri | YouTube | Video | [Topic] | Recording | @name |

### Week 1 Focus
- [Key initiative]
- [Campaign tie-in]

---

## Week 2: [Date Range]

[Same format...]

---

## Week 3: [Date Range]

[Same format...]

---

## Week 4: [Date Range]

[Same format...]

---

## Monthly Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Blog posts published | X | |
| Social impressions | X | |
| Email subscribers gained | X | |
| Newsletter open rate | X% | |
```

---

## Content Pillars

Define 3-5 content pillars that align with business goals:

```yaml
content_pillars:
  pillar_1:
    name: "Product Education"
    description: "Help users get value from the product"
    content_types:
      - Tutorials
      - How-to guides
      - Feature spotlights
      - Best practices
    target_percentage: "40%"
    keywords: ["how to", "guide", "tutorial"]

  pillar_2:
    name: "Industry Insights"
    description: "Establish thought leadership"
    content_types:
      - Trend analysis
      - Opinion pieces
      - Research reports
      - Expert interviews
    target_percentage: "25%"
    keywords: ["trends", "future of", "why"]

  pillar_3:
    name: "Customer Success"
    description: "Social proof and inspiration"
    content_types:
      - Case studies
      - Customer stories
      - Testimonials
      - Use case showcases
    target_percentage: "20%"
    keywords: ["how X achieved", "case study"]

  pillar_4:
    name: "Company Culture"
    description: "Build brand and attract talent"
    content_types:
      - Team spotlights
      - Behind the scenes
      - Values content
      - Hiring posts
    target_percentage: "15%"
    keywords: ["team", "culture", "hiring"]
```

---

## Channel-Specific Cadence

### Blog

```yaml
blog:
  frequency: "2-4 posts per week"
  content_types:
    - long_form: "1500-2500 words, 1x/week"
    - tutorials: "800-1500 words, 1x/week"
    - news: "400-800 words, as needed"

  schedule:
    monday: "Long-form thought leadership"
    wednesday: "Tutorial or how-to"
    friday: "Quick tips or news (optional)"

  best_practices:
    - "SEO optimize all posts"
    - "Include 3-5 images"
    - "Add CTAs throughout"
    - "Link to related content"
```

### Social Media

```yaml
social:
  twitter:
    frequency: "1-3 posts per day"
    content_mix:
      - threads: "2x per week"
      - single_posts: "daily"
      - engagement: "5+ replies per day"
    best_times: ["9 AM", "12 PM", "5 PM"]

  linkedin:
    frequency: "1 post per day"
    content_mix:
      - long_posts: "2x per week"
      - short_updates: "3x per week"
      - shares: "1-2x per week"
    best_times: ["8 AM", "12 PM"]

  youtube:
    frequency: "1 video per week"
    content_types:
      - tutorials: "5-15 minutes"
      - vlogs: "3-10 minutes"
      - shorts: "< 60 seconds"
```

### Email

```yaml
email:
  newsletter:
    frequency: "Weekly"
    day: "Tuesday or Thursday"
    time: "10 AM local"
    sections:
      - "Featured content"
      - "Product updates"
      - "Community highlights"
      - "Resources/links"

  product_updates:
    frequency: "Monthly or as needed"
    content:
      - "New features"
      - "Improvements"
      - "Coming soon"

  nurture_sequences:
    - onboarding: "5 emails over 14 days"
    - re_engagement: "3 emails over 7 days"
```

---

## Content Status Workflow

```yaml
content_status:
  stages:
    idea:
      description: "Content idea proposed"
      next: "outline"

    outline:
      description: "Structure and key points defined"
      next: "draft"

    draft:
      description: "First version written"
      next: "review"

    review:
      description: "Being reviewed/edited"
      next: "scheduled"

    scheduled:
      description: "Ready to publish, date set"
      next: "published"

    published:
      description: "Live on channel"
      next: "promoted"

    promoted:
      description: "Actively being promoted"
      next: "complete"

  status_icons:
    "💡": "Idea"
    "📝": "Outline"
    "✍️": "Draft"
    "👀": "Review"
    "📅": "Scheduled"
    "✅": "Published"
    "📢": "Promoted"
```

---

## Content Production Workflow

```yaml
production_workflow:
  blog_post:
    day_1: "Topic research and outline"
    day_2_3: "Write first draft"
    day_4: "Internal review"
    day_5: "Revisions"
    day_6: "Final review and scheduling"
    day_7: "Publish and promote"

  video:
    week_1:
      - "Script writing"
      - "Storyboard (if needed)"
    week_2:
      - "Recording"
      - "Initial edit"
    week_3:
      - "Review and revisions"
      - "Final edit"
      - "Thumbnail creation"
      - "Publishing"

  social_content:
    batch_creation: "Create 1 week of content in 1 session"
    review: "Get approval day before"
    scheduling: "Use scheduling tool"
```

---

## Content Repurposing Matrix

```yaml
repurposing:
  blog_post:
    becomes:
      - "Twitter thread (key points)"
      - "LinkedIn post (summary)"
      - "Newsletter section"
      - "Infographic"
      - "YouTube video"
      - "Podcast episode"

  podcast_episode:
    becomes:
      - "Blog post (transcript + insights)"
      - "Quote graphics"
      - "Short video clips"
      - "Twitter thread"

  webinar:
    becomes:
      - "YouTube video"
      - "Blog post (key takeaways)"
      - "Slide deck (SlideShare)"
      - "Email series"
      - "Social clips"

  customer_interview:
    becomes:
      - "Case study"
      - "Testimonial quotes"
      - "Video clips"
      - "Social posts"
```

---

## Editorial Calendar (Annual)

```yaml
annual_calendar:
  Q1:
    january:
      theme: "Year planning / fresh starts"
      key_dates:
        - "New Year content"
    february:
      theme: "Optimization / efficiency"
      key_dates: []
    march:
      theme: "Spring cleaning / Q1 wrap-up"
      key_dates:
        - "End of Q1 content"

  Q2:
    april:
      theme: "Growth / scaling"
      key_dates: []
    may:
      theme: "Mid-year check-in"
      key_dates: []
    june:
      theme: "Summer prep / H1 review"
      key_dates:
        - "Mid-year review content"

  Q3:
    july:
      theme: "Optimization / summer content"
      key_dates: []
    august:
      theme: "Planning / back-to-school"
      key_dates: []
    september:
      theme: "Fall initiatives / Q4 prep"
      key_dates: []

  Q4:
    october:
      theme: "Year-end planning"
      key_dates:
        - "Halloween (optional)"
    november:
      theme: "Thanksgiving / gratitude"
      key_dates:
        - "Black Friday (if relevant)"
    december:
      theme: "Year review / holiday"
      key_dates:
        - "End of year content"
        - "Holiday break"
```

---

## Content Metrics

```yaml
metrics:
  blog:
    - "Page views"
    - "Time on page"
    - "Bounce rate"
    - "Organic traffic"
    - "Conversions"

  social:
    - "Impressions"
    - "Engagement rate"
    - "Follower growth"
    - "Click-through rate"
    - "Share rate"

  email:
    - "Open rate"
    - "Click rate"
    - "Unsubscribe rate"
    - "List growth"

  video:
    - "Views"
    - "Watch time"
    - "Subscriber growth"
    - "Engagement"
```

---

## Content Planning Meeting

```yaml
planning_meeting:
  frequency: "Weekly (30-60 min)"
  attendees:
    - "Content lead"
    - "Marketing manager"
    - "Social media manager"

  agenda:
    - "Review last week's performance (10 min)"
    - "This week's content status (10 min)"
    - "Next week's content planning (20 min)"
    - "Ideas and brainstorm (10 min)"
    - "Blockers and resources (10 min)"

  outputs:
    - "Updated content calendar"
    - "Assigned tasks"
    - "Identified gaps"
```

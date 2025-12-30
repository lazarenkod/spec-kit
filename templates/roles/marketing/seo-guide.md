# SEO Guide for Product Marketing

## Purpose

Practical SEO guide for product teams to improve search visibility, drive organic traffic, and convert visitors.

---

## SEO Fundamentals

```
┌─────────────────────────────────────────────────────────────────┐
│                      SEO Components                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TECHNICAL SEO ────▶ Can search engines crawl your site?        │
│  ON-PAGE SEO ──────▶ Is your content optimized for keywords?    │
│  OFF-PAGE SEO ─────▶ Do other sites link to you?                │
│  CONTENT SEO ──────▶ Do you have valuable, relevant content?    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technical SEO Checklist

### Crawlability & Indexability

```yaml
crawlability:
  robots_txt:
    - [ ] Located at /robots.txt
    - [ ] Not blocking important pages
    - [ ] Blocks admin, API, private pages
    - [ ] Includes sitemap reference

  sitemap:
    - [ ] XML sitemap at /sitemap.xml
    - [ ] Submitted to Google Search Console
    - [ ] Submitted to Bing Webmaster Tools
    - [ ] Auto-updates with new pages
    - [ ] No 404s in sitemap

  indexing:
    - [ ] No unintentional noindex tags
    - [ ] Canonical URLs set correctly
    - [ ] No duplicate content issues
    - [ ] Key pages are indexed
```

### Site Performance

```yaml
performance:
  core_web_vitals:
    LCP:
      description: "Largest Contentful Paint"
      target: "< 2.5 seconds"
      impact: "User experience + ranking"

    FID:
      description: "First Input Delay"
      target: "< 100 milliseconds"
      impact: "Interactivity + ranking"

    CLS:
      description: "Cumulative Layout Shift"
      target: "< 0.1"
      impact: "Visual stability + ranking"

  optimization:
    - [ ] Images optimized (WebP, compressed)
    - [ ] Lazy loading implemented
    - [ ] CSS/JS minified
    - [ ] CDN enabled
    - [ ] Caching configured
    - [ ] GZIP/Brotli compression
```

### Mobile & Security

```yaml
mobile_security:
  mobile:
    - [ ] Mobile-friendly test passing
    - [ ] Responsive design
    - [ ] Touch-friendly navigation
    - [ ] No horizontal scrolling
    - [ ] Readable font sizes

  security:
    - [ ] HTTPS enabled (SSL certificate)
    - [ ] HTTP redirects to HTTPS
    - [ ] HSTS configured
    - [ ] No mixed content warnings
```

---

## On-Page SEO

### Title Tags

```yaml
title_tags:
  format: "[Primary Keyword] - [Secondary Keyword] | [Brand]"
  length: "50-60 characters"

  examples:
    homepage: "Project Management Software for Teams | TaskFlow"
    features: "Kanban Boards & Sprint Planning - TaskFlow Features"
    pricing: "Simple Pricing Plans - Start Free | TaskFlow"
    blog: "10 Best Practices for Remote Teams | TaskFlow Blog"

  best_practices:
    - "Primary keyword near the beginning"
    - "Unique for each page"
    - "Compelling and click-worthy"
    - "Brand name at end (optional)"
```

### Meta Descriptions

```yaml
meta_descriptions:
  length: "120-160 characters"

  formula: "[Value proposition]. [Key benefit]. [Call to action]."

  examples:
    good: "Manage projects effortlessly with TaskFlow. Kanban boards, time tracking, and team collaboration in one place. Start free today."
    bad: "TaskFlow is a project management tool."

  best_practices:
    - "Include primary keyword"
    - "Compelling and actionable"
    - "Unique for each page"
    - "Include value proposition"
    - "Add CTA when appropriate"
```

### Heading Structure

```yaml
headings:
  h1:
    rules:
      - "Exactly one per page"
      - "Include primary keyword"
      - "Matches search intent"

  h2_h6:
    rules:
      - "Logical hierarchy (no skipping)"
      - "Include secondary keywords naturally"
      - "Describe section content"

  example_structure:
    h1: "Project Management Software for Remote Teams"
    h2: "Why Teams Choose TaskFlow"
    h3: "Simple Kanban Boards"
    h3: "Built-in Time Tracking"
    h2: "Features That Make Work Easy"
    h3: "Real-time Collaboration"
```

### Content Optimization

```yaml
content_optimization:
  keywords:
    - "Primary keyword in first 100 words"
    - "Keyword density 1-2% (natural)"
    - "LSI keywords throughout"
    - "Keywords in headings"

  structure:
    - "Short paragraphs (2-4 sentences)"
    - "Bullet points for scanability"
    - "Clear headings every 300 words"
    - "Table of contents for long content"

  media:
    - "Alt text for all images"
    - "Descriptive file names"
    - "Compressed images"
    - "Video transcripts"

  internal_linking:
    - "Link to related content"
    - "Descriptive anchor text"
    - "5-10 internal links per post"
    - "Link to key pages from every page"
```

### URL Structure

```yaml
url_structure:
  format: "https://domain.com/category/keyword-phrase"

  best_practices:
    - "Short and descriptive"
    - "Include target keyword"
    - "Use hyphens (not underscores)"
    - "Lowercase only"
    - "No special characters"
    - "Avoid dates in URLs (for evergreen content)"

  examples:
    good:
      - "/features/kanban-boards"
      - "/blog/remote-team-management-guide"
      - "/pricing"

    bad:
      - "/features/index.php?id=123"
      - "/blog/2024/01/15/post-title"
      - "/features/Kanban_Boards"
```

---

## Keyword Research

### Research Process

```yaml
keyword_research:
  step_1_seed_keywords:
    - "List core product/service terms"
    - "List customer problem terms"
    - "List competitor brand terms"
    - "List industry terms"

  step_2_expand:
    tools:
      - "Google Keyword Planner (free)"
      - "Ahrefs / SEMrush (paid)"
      - "AnswerThePublic (questions)"
      - "Google Suggest (autocomplete)"
      - "People Also Ask (related questions)"

  step_3_analyze:
    metrics:
      - "Search volume (monthly searches)"
      - "Keyword difficulty (competition)"
      - "Search intent (informational/transactional)"
      - "Click-through opportunity"

  step_4_prioritize:
    high_priority:
      - "High volume + low difficulty"
      - "Strong transactional intent"
      - "Relevant to product/service"

    matrix:
      | Volume | Difficulty | Priority |
      |--------|------------|----------|
      | High   | Low        | Top      |
      | High   | High       | Long-term|
      | Low    | Low        | Quick win|
      | Low    | High       | Skip     |
```

### Search Intent

```yaml
search_intent:
  informational:
    signals: ["how to", "what is", "guide", "tutorial"]
    content: "Blog posts, guides, tutorials"
    examples:
      - "how to manage remote teams"
      - "what is kanban"

  navigational:
    signals: ["brand name", "login", "pricing"]
    content: "Brand pages, product pages"
    examples:
      - "taskflow login"
      - "taskflow pricing"

  commercial:
    signals: ["best", "vs", "review", "comparison"]
    content: "Comparison pages, reviews"
    examples:
      - "best project management tools"
      - "asana vs monday"

  transactional:
    signals: ["buy", "sign up", "free trial", "demo"]
    content: "Product pages, landing pages"
    examples:
      - "project management software free trial"
      - "buy kanban tool"
```

---

## Content SEO

### Content Types for SEO

```yaml
content_types:
  blog_posts:
    purpose: "Target informational keywords"
    length: "1500-2500 words"
    frequency: "2-4 per week"
    examples:
      - "How-to guides"
      - "Tutorials"
      - "Industry insights"

  landing_pages:
    purpose: "Target commercial/transactional keywords"
    length: "1000-2000 words"
    types:
      - "Feature pages"
      - "Use case pages"
      - "Industry pages"
      - "Comparison pages"

  pillar_pages:
    purpose: "Comprehensive topic coverage"
    length: "3000-5000+ words"
    structure:
      - "Overview of topic"
      - "Links to cluster content"
      - "Regularly updated"

  glossary_pages:
    purpose: "Target definitional keywords"
    length: "300-800 words each"
    examples:
      - "What is [term]"
      - "[Term] definition"
```

### Content Cluster Strategy

```yaml
content_clusters:
  structure:
    pillar:
      topic: "Project Management"
      url: "/guides/project-management"
      keywords: ["project management", "project management guide"]

    cluster_content:
      - topic: "Kanban"
        url: "/blog/what-is-kanban"
        links_to: "/guides/project-management"

      - topic: "Agile"
        url: "/blog/agile-methodology-guide"
        links_to: "/guides/project-management"

      - topic: "Sprint Planning"
        url: "/blog/sprint-planning-tips"
        links_to: "/guides/project-management"

  benefits:
    - "Establishes topical authority"
    - "Improves internal linking"
    - "Helps Google understand site structure"
    - "Better user experience"
```

---

## Off-Page SEO

### Link Building

```yaml
link_building:
  strategies:
    content_marketing:
      - "Create linkable assets"
      - "Original research/data"
      - "Free tools/templates"
      - "Infographics"

    outreach:
      - "Guest posting"
      - "Broken link building"
      - "Resource page outreach"
      - "HARO responses"

    earned:
      - "Press coverage"
      - "Industry mentions"
      - "Reviews and awards"
      - "Social shares"

  quality_signals:
    good_links:
      - "Relevant to your industry"
      - "From high-authority sites"
      - "Natural anchor text"
      - "From unique domains"

    avoid:
      - "Link farms"
      - "Paid links (against guidelines)"
      - "Exact match anchor text spam"
      - "Low-quality directories"
```

### Brand Signals

```yaml
brand_signals:
  - "Google Business Profile (if applicable)"
  - "Consistent NAP across web"
  - "Social media presence"
  - "Wikipedia/Crunchbase mentions"
  - "Industry directories"
  - "Review sites (G2, Capterra)"
```

---

## SEO Tools

```yaml
seo_tools:
  free:
    - "Google Search Console (essential)"
    - "Google Analytics"
    - "Google PageSpeed Insights"
    - "Google Mobile-Friendly Test"
    - "Bing Webmaster Tools"

  freemium:
    - "Ubersuggest"
    - "Answer The Public"
    - "GTmetrix"

  paid:
    - "Ahrefs (backlinks, keywords)"
    - "SEMrush (all-in-one)"
    - "Moz (domain authority)"
    - "Screaming Frog (technical)"

  wordpress:
    - "Yoast SEO"
    - "RankMath"

  technical:
    - "Schema Markup Validator"
    - "Rich Results Test"
```

---

## SEO Metrics to Track

```yaml
metrics:
  organic_traffic:
    - "Total organic sessions"
    - "Organic traffic growth"
    - "Organic traffic by page"
    - "Organic traffic by keyword"

  rankings:
    - "Position for target keywords"
    - "Ranking changes over time"
    - "Featured snippet wins"
    - "SERP feature appearances"

  technical:
    - "Core Web Vitals scores"
    - "Crawl errors"
    - "Index coverage"
    - "Page speed"

  conversions:
    - "Organic conversion rate"
    - "Goal completions from organic"
    - "Revenue from organic"

  authority:
    - "Domain authority/rating"
    - "Backlinks gained"
    - "Referring domains"
```

---

## Monthly SEO Checklist

```yaml
monthly_checklist:
  week_1:
    - [ ] Review Search Console for errors
    - [ ] Check Core Web Vitals
    - [ ] Review keyword rankings
    - [ ] Analyze organic traffic

  week_2:
    - [ ] Publish new content
    - [ ] Update underperforming content
    - [ ] Build internal links
    - [ ] Fix broken links

  week_3:
    - [ ] Outreach for backlinks
    - [ ] Guest post submissions
    - [ ] Competitor analysis
    - [ ] HARO responses

  week_4:
    - [ ] Monthly performance report
    - [ ] Content planning for next month
    - [ ] Technical SEO audit
    - [ ] Strategy adjustment
```

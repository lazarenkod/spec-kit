# Press Kit Generator

## Purpose

Generate professional press kits for product launches, including press releases, founder bios, media assets, and key facts.

## Press Kit Structure

```
press-kit/
├── press-release.md
├── fact-sheet.md
├── founder-bios.md
├── media-assets/
│   ├── logo-pack/
│   │   ├── logo-dark.svg
│   │   ├── logo-light.svg
│   │   ├── logo-icon.svg
│   │   └── logo-wordmark.svg
│   ├── screenshots/
│   │   ├── screenshot-1.png
│   │   ├── screenshot-2.png
│   │   └── screenshot-annotated.png
│   ├── og-images/
│   │   ├── og-default.png
│   │   └── og-launch.png
│   └── demo-video.mp4
└── contact.md
```

---

## Press Release Template

```markdown
# [COMPANY NAME] Launches [PRODUCT NAME] to [SOLVE PROBLEM]

**[City, State] – [Date]** – [Company Name], [brief company description], today announced the launch of [Product Name], [one sentence value proposition].

## The Problem

[2-3 sentences describing the problem your product solves. Include statistics if available.]

## The Solution

[Product Name] [brief description of what it does and how it's different].

Key features include:
- **[Feature 1]**: [One sentence benefit]
- **[Feature 2]**: [One sentence benefit]
- **[Feature 3]**: [One sentence benefit]

## Founder Quote

"[Compelling quote about why you built this and what it means for users]," said [Founder Name], [Title] of [Company Name]. "[Second sentence reinforcing the vision]."

## Availability and Pricing

[Product Name] is available starting today at [website]. [Pricing information - free tier, starting price, etc.]

## About [Company Name]

[Company Name] [2-3 sentences about the company, mission, and team background]. For more information, visit [website].

## Media Contact

[Contact Name]
[Email]
[Phone]

### ###

*[Boilerplate about embargo if applicable]*
```

---

## Fact Sheet Template

```markdown
# [Product Name] Fact Sheet

## Overview

| | |
|---|---|
| **Product** | [Product Name] |
| **Category** | [e.g., SaaS, Developer Tool, Consumer App] |
| **Website** | [URL] |
| **Founded** | [Year] |
| **Headquarters** | [City, Country] |
| **Founders** | [Names] |

## The Problem

[One paragraph describing the problem]

## The Solution

[One paragraph describing your solution]

## Key Features

1. **[Feature]**: [Description]
2. **[Feature]**: [Description]
3. **[Feature]**: [Description]

## Target Users

- [User type 1]
- [User type 2]
- [User type 3]

## Pricing

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | [Key features] |
| Pro | $X/mo | [Key features] |
| Enterprise | Custom | [Key features] |

## Key Statistics

- [Metric]: [Number]
- [Metric]: [Number]
- [Metric]: [Number]

## Funding (if applicable)

- **Total Raised**: $X
- **Investors**: [Names]
- **Latest Round**: [Stage] - $X ([Date])

## Awards & Recognition

- [Award/Recognition]
- [Award/Recognition]

## Press Coverage

- "[Quote]" – [Publication]
- "[Quote]" – [Publication]

## Contact

**Media**: [email]
**General**: [email]
**Twitter**: @[handle]
```

---

## Founder Bio Template

```markdown
# Founder Bios

## [Founder Name] – [Title]

![Headshot](./media-assets/founder-1.jpg)

[Founder Name] is the [Title] of [Company Name]. [2-3 sentences about background and relevant experience].

Before [Company Name], [they] [previous relevant experience - 1-2 sentences]. [They] [hold/holds] a [degree] from [University].

[Founder Name] is passionate about [relevant passion that ties to the product]. [Optional: Personal detail that humanizes].

**Connect**:
- Twitter: @[handle]
- LinkedIn: [URL]
- Email: [email]

---

## [Co-Founder Name] – [Title]

![Headshot](./media-assets/founder-2.jpg)

[Similar structure...]
```

---

## Media Assets Specifications

```yaml
logo_pack:
  formats:
    - svg (primary, scalable)
    - png (1024px, 512px, 256px, 128px)
    - eps (for print)

  variants:
    - logo-full (logo + wordmark)
    - logo-icon (icon only)
    - logo-wordmark (text only)
    - logo-dark (for light backgrounds)
    - logo-light (for dark backgrounds)

  guidelines:
    minimum_size: "32px height"
    clear_space: "Equal to height of icon on all sides"
    background: "Use appropriate variant for background"
    dont:
      - "Don't stretch or distort"
      - "Don't change colors"
      - "Don't add effects"

screenshots:
  resolution: "2x retina (2880x1800 for desktop)"
  format: "PNG with transparency where appropriate"
  naming: "screenshot-[feature]-[number].png"

  recommended:
    - Hero shot (main interface)
    - Key feature 1
    - Key feature 2
    - Mobile view (if applicable)
    - Before/after (if applicable)

og_images:
  twitter:
    size: "1200x675px"
    format: "PNG or JPG"

  linkedin:
    size: "1200x627px"
    format: "PNG or JPG"

  facebook:
    size: "1200x630px"
    format: "PNG or JPG"

  content:
    - Product name/logo
    - Tagline
    - Key visual
    - Clear at small sizes

demo_video:
  length: "30-90 seconds"
  format: "MP4 (H.264)"
  resolution: "1920x1080 or 2560x1440"
  audio: "Optional music, voiceover recommended"

  structure:
    - "Hook (0-5s): Problem statement"
    - "Solution (5-15s): What product does"
    - "Demo (15-60s): Key features in action"
    - "CTA (last 5-10s): Call to action"
```

---

## Press Outreach Template

```markdown
Subject: [PRODUCT NAME] - [Short Hook] [Embargo if applicable]

Hi [Name],

[Personalized opener - reference their recent article, beat, etc.]

I'm reaching out because I think [Product Name] would be interesting to [Publication] readers.

**The Quick Pitch:**
[2-3 sentences: what it is, why it matters, why now]

**Why This Matters:**
- [Key stat or trend]
- [Problem scope]
- [Unique angle]

**What's Available:**
- Exclusive interview with founder
- Early access / demo
- Full press kit with assets

[Product Name] launches [date]. Happy to provide more details or set up a call.

Best,
[Your Name]
[Title]
[Contact]

P.S. [Optional personal note or additional hook]
```

---

## Press List Categories

```yaml
press_targets:
  tier_1:
    description: "Major publications, high impact"
    examples:
      - TechCrunch
      - The Verge
      - Wired
      - VentureBeat
    approach: "Exclusive angle, early access"

  tier_2:
    description: "Industry publications, targeted reach"
    examples:
      - "[Industry] Today"
      - "[Industry] Magazine"
      - Niche tech blogs
    approach: "Detailed pitch, specific angle"

  tier_3:
    description: "Blogs, newsletters, influencers"
    examples:
      - Popular Substack writers
      - YouTube reviewers
      - Podcast hosts
    approach: "Product access, partnership potential"

  tier_4:
    description: "Aggregators and directories"
    examples:
      - Product Hunt
      - Hacker News
      - BetaList
      - AlternativeTo
    approach: "Self-submission, community engagement"
```

---

## Press Kit Generation Checklist

```yaml
checklist:
  content:
    - [ ] Press release written and proofread
    - [ ] Fact sheet complete with current stats
    - [ ] Founder bios written
    - [ ] Quotes prepared for different angles
    - [ ] FAQ for common journalist questions

  assets:
    - [ ] Logo pack (all formats and variants)
    - [ ] High-res screenshots (annotated and clean)
    - [ ] OG images for all platforms
    - [ ] Demo video/GIF
    - [ ] Founder headshots

  distribution:
    - [ ] Press kit hosted publicly (Notion, website, Dropbox)
    - [ ] Shareable link created
    - [ ] PDF version for email attachments
    - [ ] Media contact information included

  outreach:
    - [ ] Press list compiled
    - [ ] Personalized pitches drafted
    - [ ] Embargo strategy decided
    - [ ] Follow-up schedule planned
```

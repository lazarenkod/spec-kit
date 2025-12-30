# Prioritization Framework

## Purpose

Systematic approaches to prioritizing features, initiatives, and tasks. Helps make defensible decisions and communicate rationale to stakeholders.

---

## Framework Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   Prioritization Methods                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  IMPACT-BASED                EFFORT-BASED                       │
│  ├── RICE                    ├── T-Shirt Sizing                 │
│  ├── ICE                     ├── Story Points                   │
│  └── Value vs Effort         └── Time Estimates                 │
│                                                                  │
│  STRATEGIC                   CUSTOMER-CENTRIC                   │
│  ├── MoSCoW                  ├── Kano Model                     │
│  ├── Weighted Scoring        ├── JTBD Prioritization            │
│  └── OKR Alignment           └── Customer Value Score           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## RICE Framework

The most comprehensive and data-driven approach.

### Formula

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

### Components

```yaml
rice:
  reach:
    definition: "How many users will this affect in a given period?"
    measurement: "Number of users per quarter"
    examples:
      - "10,000 users/quarter = 10,000"
      - "500 enterprise accounts = 500"
      - "All users = total user count"

  impact:
    definition: "How much will this move the needle for each user?"
    scale:
      3: "Massive - transformative change"
      2: "High - significant improvement"
      1: "Medium - noticeable improvement"
      0.5: "Low - minor improvement"
      0.25: "Minimal - barely noticeable"

  confidence:
    definition: "How confident are we in our estimates?"
    scale:
      100%: "High - have data, validated"
      80%: "Medium - some data, reasonable assumptions"
      50%: "Low - gut feeling, hypothesis"

  effort:
    definition: "How many person-months will this take?"
    measurement: "Person-months (1 person for 1 month = 1)"
    examples:
      - "1 engineer for 2 weeks = 0.5"
      - "2 engineers for 3 months = 6"
```

### RICE Scoring Template

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Feature A | 5000 | 2 | 80% | 2 | 4,000 |
| Feature B | 1000 | 3 | 100% | 1 | 3,000 |
| Feature C | 10000 | 0.5 | 50% | 3 | 833 |

### RICE Example

```yaml
example:
  feature: "In-app onboarding tour"
  reach: 8000  # New users per quarter
  impact: 2    # High - improves activation significantly
  confidence: 80%  # Have data from similar features
  effort: 1.5  # 1.5 person-months

  calculation: "(8000 × 2 × 0.8) / 1.5 = 8,533"
  interpretation: "High priority - good reach, high impact, reasonable effort"
```

---

## ICE Framework

Simpler, faster version of RICE.

### Formula

```
ICE Score = Impact × Confidence × Ease
```

### Components

```yaml
ice:
  impact:
    scale: "1-10"
    question: "How much will this impact our goal?"

  confidence:
    scale: "1-10"
    question: "How confident are we this will work?"

  ease:
    scale: "1-10"
    question: "How easy is this to implement?"

  # All scores averaged or multiplied
```

### ICE Scoring Template

| Feature | Impact (1-10) | Confidence (1-10) | Ease (1-10) | ICE Score |
|---------|---------------|-------------------|-------------|-----------|
| Feature A | 8 | 7 | 5 | 280 |
| Feature B | 6 | 9 | 8 | 432 |
| Feature C | 9 | 4 | 3 | 108 |

---

## Value vs Effort Matrix

Visual 2x2 prioritization.

```
        HIGH VALUE
             │
    ┌────────┼────────┐
    │  DO    │ PLAN   │
    │ FIRST  │  FOR   │
    │        │ LATER  │
LOW ├────────┼────────┤ HIGH
EFF │ QUICK  │  DON'T │
ORT │ WINS   │   DO   │
    │        │        │
    └────────┴────────┘
         LOW VALUE
```

### Quadrants

```yaml
quadrants:
  do_first:
    criteria: "High value, low effort"
    action: "Prioritize immediately"
    examples: "Bug fixes with big impact, small UX improvements"

  plan_for:
    criteria: "High value, high effort"
    action: "Plan strategically, break into phases"
    examples: "Major features, platform rewrites"

  quick_wins:
    criteria: "Low value, low effort"
    action: "Do when convenient, fill gaps"
    examples: "Minor improvements, polish items"

  dont_do:
    criteria: "Low value, high effort"
    action: "Avoid or reconsider"
    examples: "Nice-to-haves, vanity features"
```

---

## MoSCoW Method

Categorical prioritization.

```yaml
moscow:
  must_have:
    definition: "Non-negotiable, product fails without it"
    criteria:
      - "Core functionality"
      - "Legal/compliance requirements"
      - "Critical bugs"
    percentage: "~60% of effort"

  should_have:
    definition: "Important but not critical"
    criteria:
      - "High value features"
      - "Expected functionality"
      - "Significant improvements"
    percentage: "~20% of effort"

  could_have:
    definition: "Nice to have if time permits"
    criteria:
      - "Enhancements"
      - "Lower priority improvements"
      - "Polish items"
    percentage: "~20% of effort"

  wont_have:
    definition: "Explicitly out of scope (for now)"
    criteria:
      - "Future considerations"
      - "Deprioritized items"
      - "Out of scope requests"
    note: "Document for future reference"
```

### MoSCoW Template

| Feature | Category | Rationale |
|---------|----------|-----------|
| User authentication | Must Have | Core functionality |
| Password reset | Must Have | Security requirement |
| Social login | Should Have | Improves conversion |
| Profile customization | Could Have | Nice to have |
| Gamification | Won't Have | Not aligned with MVP |

---

## Kano Model

Customer satisfaction-based prioritization.

```yaml
kano:
  basic:
    name: "Must-Haves"
    description: "Expected features, absence causes dissatisfaction"
    satisfaction_curve: "Negative if absent, neutral if present"
    examples:
      - "Login/logout"
      - "Basic security"
      - "Core functionality"

  performance:
    name: "One-Dimensional"
    description: "More is better, linear satisfaction"
    satisfaction_curve: "Proportional to quality"
    examples:
      - "Speed/performance"
      - "Storage space"
      - "Feature depth"

  excitement:
    name: "Delighters"
    description: "Unexpected features that create joy"
    satisfaction_curve: "Neutral if absent, high if present"
    examples:
      - "Thoughtful UX touches"
      - "Surprise features"
      - "Exceeding expectations"

  indifferent:
    name: "Neutral"
    description: "Features users don't care about"
    satisfaction_curve: "Flat"
    action: "Deprioritize or remove"

  reverse:
    name: "Dissatisfiers"
    description: "Features some users actively dislike"
    satisfaction_curve: "Negative when present"
    action: "Make optional or remove"
```

### Kano Survey Questions

For each feature, ask:
1. "How would you feel if you had this feature?" (Functional)
2. "How would you feel if you didn't have this feature?" (Dysfunctional)

```yaml
response_options:
  - "I like it"
  - "I expect it"
  - "I'm neutral"
  - "I can tolerate it"
  - "I dislike it"

# Map responses to category using Kano evaluation table
```

---

## Weighted Scoring

Custom scoring based on strategic criteria.

### Setup

```yaml
weighted_scoring:
  criteria:
    - name: "Strategic alignment"
      weight: 30%
      scale: "1-5"

    - name: "Customer impact"
      weight: 25%
      scale: "1-5"

    - name: "Revenue potential"
      weight: 20%
      scale: "1-5"

    - name: "Technical feasibility"
      weight: 15%
      scale: "1-5"

    - name: "Time to market"
      weight: 10%
      scale: "1-5"
```

### Scoring Template

| Feature | Strategic (30%) | Customer (25%) | Revenue (20%) | Technical (15%) | Time (10%) | Total |
|---------|-----------------|----------------|---------------|-----------------|------------|-------|
| Feature A | 4 (1.2) | 5 (1.25) | 3 (0.6) | 4 (0.6) | 3 (0.3) | 3.95 |
| Feature B | 5 (1.5) | 4 (1.0) | 5 (1.0) | 3 (0.45) | 2 (0.2) | 4.15 |

---

## OKR Alignment

Prioritize based on company/team objectives.

```yaml
okr_alignment:
  process:
    1. "List current OKRs"
    2. "Score each feature's contribution to each OKR"
    3. "Prioritize features that move multiple OKRs"
    4. "Deprioritize features not linked to OKRs"

  template:
    | Feature | OKR 1 (40%) | OKR 2 (35%) | OKR 3 (25%) | Alignment Score |
    |---------|-------------|-------------|-------------|-----------------|
```

---

## Prioritization Process

### Step-by-Step

```yaml
prioritization_process:
  1_gather:
    - "Collect all feature requests/ideas"
    - "Document source and context"
    - "Remove duplicates"

  2_filter:
    - "Check strategic alignment"
    - "Verify technical feasibility"
    - "Confirm resource availability"

  3_score:
    - "Apply chosen framework"
    - "Score consistently"
    - "Document assumptions"

  4_rank:
    - "Sort by score"
    - "Apply constraints"
    - "Consider dependencies"

  5_validate:
    - "Review with stakeholders"
    - "Sanity check results"
    - "Adjust if needed"

  6_communicate:
    - "Share prioritized list"
    - "Explain rationale"
    - "Set expectations"
```

---

## Prioritization Pitfalls

```yaml
common_mistakes:
  hippo:
    name: "Highest Paid Person's Opinion"
    problem: "Deferring to seniority over data"
    solution: "Use frameworks, present data"

  recency_bias:
    name: "Last Thing Heard"
    problem: "Prioritizing recent requests"
    solution: "Batch decisions, regular reviews"

  squeaky_wheel:
    name: "Loudest Customer"
    problem: "Prioritizing vocal minorities"
    solution: "Aggregate feedback, segment analysis"

  sunk_cost:
    name: "We've Already Invested"
    problem: "Continuing due to past investment"
    solution: "Evaluate future value only"

  pet_projects:
    name: "Personal Favorites"
    problem: "Bias toward own ideas"
    solution: "Transparent scoring, peer review"
```

---

## Prioritization Meeting Agenda

```yaml
meeting_agenda:
  before:
    - "Prepare list of items to prioritize"
    - "Pre-score using framework"
    - "Identify contentious items"

  during:
    - "Review goals and constraints (5 min)"
    - "Walk through scores (20 min)"
    - "Discuss disagreements (15 min)"
    - "Finalize priorities (10 min)"
    - "Assign next steps (5 min)"

  after:
    - "Document decisions and rationale"
    - "Communicate to stakeholders"
    - "Update roadmap"
```

---

## Quick Reference

```yaml
when_to_use:
  RICE: "Data-driven, product with good analytics"
  ICE: "Fast decisions, early-stage products"
  Value_Effort: "Visual discussion with stakeholders"
  MoSCoW: "Scope negotiation, fixed deadlines"
  Kano: "Customer research, feature discovery"
  Weighted: "Complex decisions, multiple criteria"
  OKR: "Strategic alignment, goal-driven teams"

decision_matrix:
  | Situation | Recommended Framework |
  |-----------|----------------------|
  | Quarterly planning | RICE or Weighted |
  | Sprint planning | ICE or Value/Effort |
  | Stakeholder negotiation | MoSCoW |
  | Customer research | Kano |
  | Strategic initiatives | OKR Alignment |
```

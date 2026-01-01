---
name: discover
description: Validate problem-solution fit before building through customer discovery
version: 1.0.0
persona: product-agent
skills:
  - customer-interview
  - landing-generator
inputs:
  problem_hypothesis:
    type: string
    required: true
    description: The problem you believe exists in the market
  target_persona:
    type: string
    required: true
    description: Who experiences this problem
  validation_method:
    type: enum
    options: [interviews, survey, landing_page, all]
    default: interviews
    description: How to validate the hypothesis
outputs:
  - docs/discover/hypothesis.md                    # Artifact 1: Problem hypothesis & assumptions
  - docs/discover/interview-guide.md               # Artifact 2: Interview script (Mom Test)
  - docs/discover/scoring-template.md              # Artifact 3: Interview scoring framework
  - docs/discover/analysis.md                      # Artifact 4: Quantitative & qualitative synthesis
  - docs/discover/decision.md                      # Artifact 5: Go/No-Go decision matrix
  - docs/discover/discovery-report.md              # Artifact 6: Executive summary
  - docs/discover/interviews/interview-NNN.md      # Artifact 7: Individual interview notes (1 per interview)
  - docs/discover/surveys/survey-results.md        # Artifact 8: Survey aggregation (if survey selected)
  - docs/discover/landing-spec.md                  # Artifact 9: Landing page specification (if landing_page selected)
  - public/landing/index.html                      # Artifact 10: Smoke test landing page (if landing_page selected)
  - docs/discover/landing-metrics.md               # Artifact 11: Landing page analytics tracking (if landing_page selected)
quality_gates:
  - name: minimum_interviews
    condition: "interviews_completed >= 10 OR survey_responses >= 50 OR landing_conversion >= 5%"
    severity: warning
  - name: signal_strength
    condition: "avg_problem_severity >= 3.5"
    severity: error
handoffs:
  - label: Proceed to Concept
    agent: speckit.concept
    condition: "validation_passed"
  - label: Pivot Hypothesis
    agent: speckit.discover
    condition: "validation_failed AND pivot_direction_identified"
---

# /speckit.discover

## Purpose

Validate that a real problem exists before investing in building a solution. This command guides you through customer discovery using proven methodologies (Mom Test, Lean Startup) to extract actionable insights about problems, behaviors, and willingness to pay.

## When to Use

- **Before** starting any new product or feature
- When you have a hypothesis but no customer evidence
- When pivoting to test a new direction
- When stakeholders disagree about the problem

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     /speckit.discover                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. HYPOTHESIZE                                                  │
│     └── Define problem hypothesis + target persona               │
│                                                                  │
│  2. PREPARE                                                      │
│     ├── Generate interview scripts (Mom Test methodology)        │
│     ├── Create survey templates (if quantitative validation)     │
│     └── Build smoke test landing page (if demand validation)     │
│                                                                  │
│  3. EXECUTE                                                      │
│     ├── Conduct interviews (minimum 10)                          │
│     ├── Distribute surveys (minimum 50 responses)                │
│     └── Drive traffic to landing page (minimum 500 visitors)     │
│                                                                  │
│  4. ANALYZE                                                      │
│     ├── Score each interview (problem severity, WTP, urgency)    │
│     ├── Aggregate survey results                                 │
│     └── Calculate landing page conversion                        │
│                                                                  │
│  5. DECIDE                                                       │
│     ├── GREEN: Proceed to /speckit.concept                       │
│     ├── YELLOW: Iterate and re-validate                          │
│     └── RED: Pivot or kill hypothesis                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Command Execution

### Step 0: Load Project Language

Read `/memory/constitution.md` and extract the `language` value from the Project Settings table.

```text
IF Project Settings section exists AND language row found:
  ARTIFACT_LANGUAGE = extracted value (e.g., "ru", "en", "de")
ELSE:
  ARTIFACT_LANGUAGE = "en" (default)

Apply language rules from templates/shared/language-context.md:
- Generate all prose content in ARTIFACT_LANGUAGE
- Keep IDs, technical terms, and code in English
- Interview questions should be in ARTIFACT_LANGUAGE (for local interviews)
```

Report: "Generating discovery artifacts in {LANGUAGE_NAME} ({ARTIFACT_LANGUAGE})..."

### Step 1: Capture Hypothesis

**Output**: `docs/discover/hypothesis.md`

1. Create `docs/discover/` directory if it doesn't exist
2. Generate `hypothesis.md` from template (Artifact 1)
3. Capture problem hypothesis, target persona, validation method
4. Define assumptions to validate with their methods
5. Set success criteria thresholds

```yaml
hypothesis:
  problem: "{{problem_hypothesis}}"
  persona: "{{target_persona}}"

  assumptions:
    - assumption: "The problem exists and is significant"
      validation_method: interviews

    - assumption: "Target persona experiences this regularly"
      validation_method: interviews

    - assumption: "Current solutions are inadequate"
      validation_method: interviews + survey

    - assumption: "People would pay to solve this"
      validation_method: pricing_interview + landing_page
```

### Step 2: Generate Discovery Assets

**Output**: `docs/discover/interview-guide.md`, `docs/discover/scoring-template.md`

Based on `validation_method`, generate appropriate assets:

#### If interviews (default):

1. Load `customer-interview` skill
2. Generate `interview-guide.md` from template (Artifact 2)
3. Generate `scoring-template.md` from template (Artifact 3)
4. Create `docs/discover/interviews/` directory for interview notes

#### If survey:

1. Load survey templates from `templates/shared/discover/survey-templates.md`
2. Generate problem validation survey in `docs/discover/surveys/survey-template.md`
3. Create `docs/discover/surveys/` directory for responses
4. Configure distribution (email, social, paid panel)

#### If landing_page:

1. Load `landing-generator` skill
2. Generate `landing-spec.md` with page structure (Artifact 9)
3. Generate `public/landing/index.html` smoke test page (Artifact 10)
4. Generate `landing-metrics.md` for tracking (Artifact 11)
5. Configure analytics (GA4) and form backend (Formspree)

#### If all:

Execute all three methods, generating all corresponding artifacts.

### Step 3: Execute Discovery

Provide guidance for each method:

```markdown
## Interview Execution Guide

### Finding Interviewees
- Reach out to your network (LinkedIn, Twitter, communities)
- Ask for referrals at the end of each interview
- Use screener questions to qualify participants
- Aim for 10-20 interviews for qualitative saturation

### Conducting Interviews
- Record with permission (for later analysis)
- Listen 80%, talk 20%
- Ask about past behavior, not hypothetical future
- Follow emotional responses with "tell me more"
- Never pitch your solution during discovery

### Note-Taking
- Capture verbatim quotes (in their words)
- Note emotional intensity (frustration, excitement)
- Record specific numbers (time spent, money lost)
- Mark surprising insights
```

### Step 4: Analyze Results

**Output**: `docs/discover/analysis.md`

1. Read completed `scoring-template.md` with interview scores
2. Aggregate quantitative data from all sources
3. Synthesize qualitative insights (quotes, patterns, surprises)
4. Validate each assumption against evidence
5. Generate `analysis.md` from template (Artifact 4)

```yaml
analysis_framework:
  qualitative:
    per_interview_scoring:
      problem_severity: "[1-5]"
      current_solution_pain: "[1-5]"
      willingness_to_pay: "[1-5]"
      urgency: "[1-5]"
      decision_authority: "[1-5]"

    synthesis:
      top_problems: "List problems mentioned by >50% of interviewees"
      key_quotes: "Most powerful verbatim quotes"
      surprising_insights: "Things you didn't expect"
      patterns: "Common behaviors or workflows"

  quantitative:
    survey_analysis:
      response_rate: "X%"
      problem_severity_distribution: "Chart"
      current_solution_satisfaction: "Chart"
      willingness_to_pay_range: "Distribution"

    landing_page_analysis:
      visitors: "N"
      signups: "N"
      conversion_rate: "X%"
      traffic_sources: "Breakdown"
```

### Step 5: Make Go/No-Go Decision

**Output**: `docs/discover/decision.md`, `docs/discover/discovery-report.md`

1. Read `analysis.md` to get aggregated metrics
2. Apply decision matrix criteria
3. Determine GO / ITERATE / STOP decision
4. Generate `decision.md` from template (Artifact 5)
5. Generate `discovery-report.md` executive summary (Artifact 6)
6. Update `hypothesis.md` assumption statuses

```yaml
decision_matrix:
  green_light:
    criteria:
      - interviews_completed: ">= 10"
      - avg_problem_severity: ">= 4.0"
      - avg_willingness_to_pay: ">= 3.5"
      - OR landing_conversion: ">= 5%"
      - OR survey_problem_critical: ">= 40%"

    action: "Proceed to /speckit.concept"
    confidence: "High"

  yellow_light:
    criteria:
      - interviews_completed: "5-9"
      - avg_problem_severity: "3.0-3.9"
      - OR landing_conversion: "2-5%"

    action: "Iterate hypothesis and re-validate"
    max_iterations: 3
    confidence: "Medium"

  red_light:
    criteria:
      - interviews_completed: "< 5"
      - avg_problem_severity: "< 3.0"
      - OR landing_conversion: "< 2%"

    action: "Pivot or kill hypothesis"
    confidence: "High (negative)"
```

## Output Artifacts

Each phase generates a separate artifact file in `docs/discover/`:

---

### Artifact 1: `docs/discover/hypothesis.md`

**Created in**: Step 1 (Capture Hypothesis)

```markdown
# Problem Hypothesis

## Core Hypothesis

**Problem Statement**: {{problem_hypothesis}}

**Target Persona**: {{target_persona}}

**Validation Method**: {{validation_method}}

## Assumptions to Validate

| # | Assumption | Validation Method | Status |
|---|------------|-------------------|--------|
| A1 | The problem exists and is significant | interviews | ⏳ Pending |
| A2 | Target persona experiences this regularly | interviews | ⏳ Pending |
| A3 | Current solutions are inadequate | interviews + survey | ⏳ Pending |
| A4 | People would pay to solve this | pricing_interview + landing_page | ⏳ Pending |

## Success Criteria

- **Minimum interviews**: 10
- **Problem severity threshold**: ≥ 3.5/5.0
- **Willingness to pay threshold**: ≥ 3.0/5.0

## Pivot History

| Date | Original Hypothesis | Pivot Reason | New Direction |
|------|---------------------|--------------|---------------|
| {{date}} | {{problem_hypothesis}} | Initial | - |

---
Created: {{date}}
Status: Active
```

---

### Artifact 2: `docs/discover/interview-guide.md`

**Created in**: Step 2 (Generate Discovery Assets)

```markdown
# Interview Guide

## Pre-Interview Checklist

- [ ] Recording permission obtained
- [ ] 45-60 minutes blocked
- [ ] Quiet environment confirmed
- [ ] Notes template ready

## Opening (5 min)

"Thank you for taking the time. I'm researching [problem area] and want to learn from your experience. There are no wrong answers - I'm here to learn, not to pitch anything."

## Problem Discovery Questions (20 min)

### Current Situation
1. "Walk me through how you currently handle [problem area]."
2. "What tools/processes do you use today?"
3. "How often do you deal with this?"

### Pain Points
4. "What's the most frustrating part of [current process]?"
5. "Tell me about the last time [problem] happened. What did you do?"
6. "What have you tried to solve this? What worked/didn't work?"

### Impact
7. "How much time/money does this cost you?"
8. "What happens if this problem isn't solved?"
9. "Who else is affected by this problem?"

## Solution Exploration (15 min)

10. "If you could wave a magic wand, what would the ideal solution look like?"
11. "What would make you switch from your current approach?"
12. "Have you looked for solutions? What did you find?"

## Willingness to Pay (5 min)

13. "Have you ever paid for tools to solve similar problems?"
14. "What would solving this be worth to you? (time/money)"
15. "Who would need to approve a purchase decision?"

## Closing (5 min)

16. "Is there anything I should have asked but didn't?"
17. "Who else should I talk to about this?"

## Mom Test Reminders

- ❌ Don't ask "Would you use..."
- ❌ Don't pitch your idea
- ❌ Don't accept vague compliments
- ✅ Ask about past behavior
- ✅ Follow emotions with "tell me more"
- ✅ Get specific examples

---
Hypothesis: {{problem_hypothesis}}
Created: {{date}}
```

---

### Artifact 3: `docs/discover/scoring-template.md`

**Created in**: Step 2 (Generate Discovery Assets)

```markdown
# Interview Scoring Template

## Instructions

After each interview, score the following dimensions from 1-5:
- **1** = Not a problem / No interest
- **3** = Moderate problem / Some interest
- **5** = Critical problem / Strong interest

## Interview Log

| # | Interviewee | Date | Problem Severity | Solution Pain | WTP | Urgency | Authority | Notes |
|---|-------------|------|------------------|---------------|-----|---------|-----------|-------|
| 1 | | | /5 | /5 | /5 | /5 | /5 | |
| 2 | | | /5 | /5 | /5 | /5 | /5 | |
| 3 | | | /5 | /5 | /5 | /5 | /5 | |
| 4 | | | /5 | /5 | /5 | /5 | /5 | |
| 5 | | | /5 | /5 | /5 | /5 | /5 | |
| 6 | | | /5 | /5 | /5 | /5 | /5 | |
| 7 | | | /5 | /5 | /5 | /5 | /5 | |
| 8 | | | /5 | /5 | /5 | /5 | /5 | |
| 9 | | | /5 | /5 | /5 | /5 | /5 | |
| 10 | | | /5 | /5 | /5 | /5 | /5 | |

## Scoring Dimensions

### Problem Severity (1-5)
- **5**: "This keeps me up at night" / Daily frustration
- **4**: Weekly issue, significant impact
- **3**: Monthly issue, moderate impact
- **2**: Occasional annoyance
- **1**: Not really a problem

### Current Solution Pain (1-5)
- **5**: "Current tools are terrible" / Active searching for alternatives
- **4**: Significant workarounds required
- **3**: Works but not ideal
- **2**: Minor inconveniences
- **1**: Satisfied with current solution

### Willingness to Pay (1-5)
- **5**: Named a specific price / Already paying for similar
- **4**: "Would definitely pay" with examples
- **3**: "Would consider paying"
- **2**: "Maybe if it was cheap"
- **1**: "Would only use if free"

### Urgency (1-5)
- **5**: "Need this yesterday" / Active buying process
- **4**: Planning to solve in next quarter
- **3**: On the roadmap for this year
- **2**: "Would be nice someday"
- **1**: No timeline

### Decision Authority (1-5)
- **5**: Final decision maker with budget
- **4**: Key influencer / recommender
- **3**: User but not buyer
- **2**: Limited influence
- **1**: No decision power

---
Hypothesis: {{problem_hypothesis}}
Created: {{date}}
```

---

### Artifact 4: `docs/discover/analysis.md`

**Created in**: Step 4 (Analyze Results)

```markdown
# Discovery Analysis

## Quantitative Summary

### Interview Metrics (N = {{count}})

| Dimension | Average | Min | Max | Std Dev |
|-----------|---------|-----|-----|---------|
| Problem Severity | X.X | X | X | X.X |
| Solution Pain | X.X | X | X | X.X |
| Willingness to Pay | X.X | X | X | X.X |
| Urgency | X.X | X | X | X.X |
| Decision Authority | X.X | X | X | X.X |

**Overall Score**: X.X / 5.0

### Survey Results (N = {{count}})

| Question | Distribution | Key Finding |
|----------|--------------|-------------|
| Problem frequency | | |
| Current solution satisfaction | | |
| Budget range | | |

### Landing Page Results

| Metric | Value |
|--------|-------|
| Visitors | {{N}} |
| Signups | {{N}} |
| Conversion Rate | {{X}}% |
| Top Traffic Source | |

## Qualitative Synthesis

### Top Problems (mentioned by >50%)

1. **[Problem 1]**
   - Frequency: X/{{count}} interviews
   - Key quote: "_______"

2. **[Problem 2]**
   - Frequency: X/{{count}} interviews
   - Key quote: "_______"

### Key Verbatim Quotes

| Theme | Quote | Interviewee |
|-------|-------|-------------|
| Problem | "..." | #X |
| Solution Pain | "..." | #X |
| Willingness to Pay | "..." | #X |

### Surprising Discoveries

1. [Unexpected insight]
2. [Unexpected insight]

### Common Patterns

- [Behavior pattern]
- [Workflow pattern]
- [Decision pattern]

## Assumption Validation

| # | Assumption | Evidence | Verdict |
|---|------------|----------|---------|
| A1 | Problem exists | X/10 confirmed, avg severity X.X | ✅ Validated |
| A2 | Regular experience | X/10 daily/weekly | ⚠️ Partial |
| A3 | Solutions inadequate | X/10 actively searching | ✅ Validated |
| A4 | Willingness to pay | avg WTP X.X, X named price | ❌ Not validated |

---
Analysis Date: {{date}}
Based on: {{count}} interviews, {{survey_count}} surveys, {{visitors}} landing page visitors
```

---

### Artifact 5: `docs/discover/decision.md`

**Created in**: Step 5 (Make Go/No-Go Decision)

```markdown
# Discovery Decision

## Decision Matrix Results

### Quantitative Assessment

| Criterion | Threshold | Actual | Pass |
|-----------|-----------|--------|------|
| Interviews completed | ≥ 10 | {{count}} | ✅/❌ |
| Avg problem severity | ≥ 3.5 | X.X | ✅/❌ |
| Avg willingness to pay | ≥ 3.0 | X.X | ✅/❌ |
| Landing conversion | ≥ 5% | X% | ✅/❌ |
| Survey problem_critical | ≥ 40% | X% | ✅/❌ |

### Signal Strength

```
█████████░░░░░░░░░░░ 45% (Example)
```

## DECISION: [🟢 GO / 🟡 ITERATE / 🔴 STOP]

**Confidence Level**: [High / Medium / Low]

**Rationale**:
[2-3 sentences explaining why this decision]

## Recommendations

### If GO → Proceed to `/speckit.concept`

**Focus areas for concept**:
1. Primary problem to solve: [most validated problem]
2. Target segment: [segment with highest scores]
3. Differentiation angle: [based on solution gaps discovered]

**De-risked assumptions**:
- [Assumption that was validated]

**Remaining risks**:
- [Assumption that needs more validation]

### If ITERATE → Re-run Discovery

**Hypothesis adjustments**:
- [ ] Pivot problem statement to: [new direction]
- [ ] Target different persona: [alternative segment]
- [ ] Test different value proposition: [refined pitch]

**Additional evidence needed**:
- [ ] Interview X more [specific segment]
- [ ] Run survey with [different audience]
- [ ] Test landing page with [different messaging]

**Max iterations remaining**: X

### If STOP → Kill Hypothesis

**Kill reasons**:
1. [Primary reason]
2. [Secondary reason]

**Adjacent opportunities discovered**:
- [Pivot direction 1]
- [Pivot direction 2]

**Learnings to preserve**:
- [Insight to carry forward]

---
Decision Date: {{date}}
Decision Maker: {{author}}
Review Date: [if ITERATE]
```

---

### Artifact 6: `docs/discover/discovery-report.md`

**Created in**: Final (Executive Summary)

```markdown
# Discovery Report: {{problem_hypothesis}}

## Executive Summary

| Attribute | Value |
|-----------|-------|
| **Hypothesis** | {{problem_hypothesis}} |
| **Target Persona** | {{target_persona}} |
| **Validation Method** | {{validation_method}} |
| **Decision** | [🟢 GO / 🟡 ITERATE / 🔴 STOP] |
| **Confidence** | [High / Medium / Low] |
| **Discovery Duration** | X weeks |

## Key Findings

### Problems Validated ✅
1. [Problem with evidence strength]
2. [Problem with evidence strength]

### Problems NOT Validated ❌
1. [Assumption that was wrong]

### Surprising Discoveries 💡
1. [Unexpected insight]

## Evidence Summary

| Source | Count | Key Metric |
|--------|-------|------------|
| Interviews | {{count}} | Avg severity: X.X |
| Survey responses | {{count}} | Problem critical: X% |
| Landing visitors | {{count}} | Conversion: X% |

## Artifacts Index

| Artifact | Path | Status |
|----------|------|--------|
| Hypothesis | [hypothesis.md](./hypothesis.md) | ✅ Complete |
| Interview Guide | [interview-guide.md](./interview-guide.md) | ✅ Complete |
| Scoring Template | [scoring-template.md](./scoring-template.md) | ✅ Complete |
| Analysis | [analysis.md](./analysis.md) | ✅ Complete |
| Decision | [decision.md](./decision.md) | ✅ Complete |
| Interview Notes | [interviews/](./interviews/) | {{count}} files |
| Survey Data | [surveys/](./surveys/) | {{count}} files |
| Landing Spec | [landing-spec.md](./landing-spec.md) | ✅/⏭️ |
| Landing Page | [/public/landing/](../../public/landing/) | ✅/⏭️ |
| Landing Metrics | [landing-metrics.md](./landing-metrics.md) | ✅/⏭️ |

## Next Steps

| Priority | Action | Owner | Due |
|----------|--------|-------|-----|
| P0 | [Next action based on decision] | | |
| P1 | [Follow-up action] | | |

## Handoff

- **If GO**: Run `/speckit.concept` with validated problems
- **If ITERATE**: Re-run `/speckit.discover` with adjusted hypothesis
- **If STOP**: Archive learnings, explore pivot directions

---
Generated by /speckit.discover
Report Date: {{date}}
```

---

### Artifact 7: `docs/discover/interviews/interview-NNN.md`

**Created in**: Step 3 (Execute Discovery) — one file per interview

```markdown
# Interview #{{number}}: {{interviewee_role}}

## Metadata

| Attribute | Value |
|-----------|-------|
| **Date** | {{date}} |
| **Duration** | {{duration}} min |
| **Interviewee** | {{role/title}} |
| **Company Size** | {{size}} |
| **Industry** | {{industry}} |

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Problem Severity | /5 | |
| Solution Pain | /5 | |
| Willingness to Pay | /5 | |
| Urgency | /5 | |
| Decision Authority | /5 | |

**Overall**: X.X / 5.0

## Key Quotes

> "[Verbatim quote about the problem]"

> "[Verbatim quote about current solution pain]"

> "[Verbatim quote about willingness to pay]"

## Problem Discovery

### Current Situation
- [How they handle the problem today]
- [Tools/processes they use]

### Pain Points
- [Main frustrations]
- [Workarounds they've tried]

### Impact
- Time lost: [X hours/week]
- Money lost: [$ amount]
- Other impact: [describe]

## Surprising Insights

1. [Unexpected finding]
2. [Unexpected finding]

## Follow-up Actions

- [ ] [Action item from this interview]
- [ ] Referral: {{name}} ({{contact}})

---
Recorded: [Yes/No]
Consent: [Verbal/Written]
```

---

### Artifact 8: `docs/discover/surveys/survey-results.md`

**Created in**: Step 3 (Execute Discovery) — if survey method selected

```markdown
# Survey Results

## Survey Metadata

| Attribute | Value |
|-----------|-------|
| **Survey Tool** | [Typeform/Google Forms/etc.] |
| **Distribution** | [email/social/paid panel] |
| **Date Range** | {{start_date}} - {{end_date}} |
| **Responses** | {{count}} |
| **Completion Rate** | {{X}}% |

## Response Summary

### Q1: Problem Frequency
| Response | Count | % |
|----------|-------|---|
| Daily | | |
| Weekly | | |
| Monthly | | |
| Rarely | | |

### Q2: Problem Severity (1-5)
| Score | Count | % |
|-------|-------|---|
| 5 (Critical) | | |
| 4 | | |
| 3 | | |
| 2 | | |
| 1 (Not a problem) | | |

**Average**: X.X

### Q3: Current Solution Satisfaction
[Distribution chart/table]

### Q4: Budget Range
| Range | Count | % |
|-------|-------|---|
| $0 (free only) | | |
| $1-50/mo | | |
| $50-200/mo | | |
| $200+/mo | | |

## Open-Ended Responses

### "Describe your biggest frustration"
- "[Response 1]"
- "[Response 2]"
- "[Response 3]"

### Themes Identified
1. [Theme] — {{count}} mentions
2. [Theme] — {{count}} mentions

## Statistical Analysis

| Metric | Value |
|--------|-------|
| % with problem severity ≥ 4 | {{X}}% |
| % actively searching for solution | {{X}}% |
| % with budget > $50/mo | {{X}}% |

---
Export Date: {{date}}
Raw Data: [link to CSV/spreadsheet]
```

---

### Artifact 9: `docs/discover/landing-spec.md`

**Created in**: Step 2 (Generate Discovery Assets) — if landing_page method selected

```markdown
# Landing Page Specification

## Purpose

Smoke test landing page to validate demand before building the product.
Goal: Measure conversion rate (email signups / visitors) as proxy for product-market fit.

## Target Metrics

| Metric | Target | Minimum Viable |
|--------|--------|----------------|
| Visitors | 500+ | 200 |
| Conversion Rate | ≥ 5% | ≥ 2% |
| Email Signups | 25+ | 10 |

## Page Structure

### Hero Section
- **Headline**: [Problem-focused, not solution-focused]
- **Subheadline**: [Who this is for + key benefit]
- **CTA**: "Get Early Access" / "Join Waitlist"
- **Social Proof**: [If available]

### Problem Section
- **Problem Statement**: {{problem_hypothesis}}
- **Pain Points**: 3 bullet points from interview insights
- **Current Alternative Pain**: Why existing solutions fail

### Solution Teaser
- **Value Proposition**: [What they'll get]
- **Key Features**: 3 high-level benefits (not features)
- **Differentiation**: Why this is different

### Social Proof (if available)
- Testimonial quotes from interviews
- Company logos (if B2B)
- Numbers (users, savings, etc.)

### CTA Section
- **Form Fields**: Email only (minimize friction)
- **Button Text**: Action-oriented ("Get Early Access")
- **Privacy Note**: "We'll only email you about launch"

### Footer
- Company/project name
- Privacy policy link
- Contact email

## Design Guidelines

- **Style**: Clean, minimal, fast-loading
- **Colors**: Use brand colors or neutral palette
- **Images**: Hero image optional, avoid stock photos
- **Mobile**: Must be mobile-responsive

## Technical Requirements

- **Hosting**: Vercel / Netlify / GitHub Pages
- **Analytics**: Google Analytics 4 or Plausible
- **Form Backend**: Formspree / Netlify Forms / ConvertKit
- **Load Time**: < 3 seconds

## Traffic Sources

| Source | Target Visitors | Method |
|--------|-----------------|--------|
| LinkedIn | 200 | Personal posts, groups |
| Twitter/X | 100 | Threads, hashtags |
| Reddit | 100 | Relevant subreddits |
| Communities | 100 | Slack, Discord, forums |

## A/B Testing (Optional)

| Element | Variant A | Variant B |
|---------|-----------|-----------|
| Headline | Problem-focused | Benefit-focused |
| CTA | "Get Early Access" | "Join Waitlist" |

---
Hypothesis: {{problem_hypothesis}}
Created: {{date}}
```

---

### Artifact 10: `public/landing/index.html`

**Created in**: Step 2 (Generate Discovery Assets) — if landing_page method selected

```html
<!DOCTYPE html>
<html lang="{{ARTIFACT_LANGUAGE}}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{product_name}} - {{headline}}</title>
  <meta name="description" content="{{subheadline}}">

  <!-- Open Graph -->
  <meta property="og:title" content="{{headline}}">
  <meta property="og:description" content="{{subheadline}}">
  <meta property="og:type" content="website">

  <!-- Analytics (replace with your tracking ID) -->
  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>

  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.6;
      color: #1a1a1a;
    }
    .container { max-width: 800px; margin: 0 auto; padding: 0 20px; }

    /* Hero */
    .hero {
      min-height: 80vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      text-align: center;
      padding: 60px 20px;
    }
    .hero h1 { font-size: 2.5rem; margin-bottom: 1rem; }
    .hero p { font-size: 1.25rem; color: #666; margin-bottom: 2rem; }

    /* Form */
    .signup-form {
      display: flex;
      gap: 10px;
      justify-content: center;
      flex-wrap: wrap;
    }
    .signup-form input {
      padding: 12px 16px;
      font-size: 1rem;
      border: 2px solid #ddd;
      border-radius: 6px;
      width: 300px;
    }
    .signup-form button {
      padding: 12px 24px;
      font-size: 1rem;
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
    }
    .signup-form button:hover { background: #1d4ed8; }

    /* Problem Section */
    .problem {
      padding: 60px 20px;
      background: #f9fafb;
    }
    .problem h2 { text-align: center; margin-bottom: 2rem; }
    .pain-points { list-style: none; }
    .pain-points li {
      padding: 1rem;
      margin-bottom: 1rem;
      background: white;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* CTA Section */
    .cta {
      padding: 60px 20px;
      text-align: center;
    }
    .cta h2 { margin-bottom: 1rem; }

    /* Footer */
    footer {
      padding: 20px;
      text-align: center;
      color: #666;
      font-size: 0.875rem;
    }

    /* Thank you state */
    .thank-you { display: none; }
    .thank-you.show { display: block; }
    .form-container.hide { display: none; }
  </style>
</head>
<body>
  <!-- Hero Section -->
  <section class="hero">
    <div class="container">
      <h1>{{headline}}</h1>
      <p>{{subheadline}}</p>

      <div class="form-container">
        <form class="signup-form" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
          <input type="email" name="email" placeholder="{{email_placeholder}}" required>
          <button type="submit">{{cta_button}}</button>
        </form>
        <p style="margin-top: 1rem; font-size: 0.875rem; color: #666;">
          {{privacy_note}}
        </p>
      </div>

      <div class="thank-you">
        <h2>🎉 {{thank_you_title}}</h2>
        <p>{{thank_you_message}}</p>
      </div>
    </div>
  </section>

  <!-- Problem Section -->
  <section class="problem">
    <div class="container">
      <h2>{{problem_section_title}}</h2>
      <ul class="pain-points">
        <li>❌ {{pain_point_1}}</li>
        <li>❌ {{pain_point_2}}</li>
        <li>❌ {{pain_point_3}}</li>
      </ul>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="cta">
    <div class="container">
      <h2>{{cta_headline}}</h2>
      <form class="signup-form" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
        <input type="email" name="email" placeholder="{{email_placeholder}}" required>
        <button type="submit">{{cta_button}}</button>
      </form>
    </div>
  </section>

  <!-- Footer -->
  <footer>
    <p>© {{year}} {{company_name}}. {{footer_text}}</p>
  </footer>

  <script>
    // Track form submission
    document.querySelectorAll('.signup-form').forEach(form => {
      form.addEventListener('submit', function(e) {
        gtag('event', 'sign_up', { method: 'email' });
      });
    });

    // Show thank you message after submission (if using AJAX)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('submitted') === 'true') {
      document.querySelectorAll('.form-container').forEach(el => el.classList.add('hide'));
      document.querySelectorAll('.thank-you').forEach(el => el.classList.add('show'));
    }
  </script>
</body>
</html>
```

---

### Artifact 11: `docs/discover/landing-metrics.md`

**Created in**: Step 3 (Execute Discovery) — if landing_page method selected

```markdown
# Landing Page Metrics Tracking

## Campaign Overview

| Attribute | Value |
|-----------|-------|
| **Landing URL** | {{landing_url}} |
| **Launch Date** | {{launch_date}} |
| **End Date** | {{end_date}} |
| **Goal** | {{signup_goal}} signups |

## Daily Metrics

| Date | Visitors | Signups | Conv. Rate | Top Source | Notes |
|------|----------|---------|------------|------------|-------|
| {{date}} | | | % | | |
| {{date}} | | | % | | |
| {{date}} | | | % | | |
| {{date}} | | | % | | |
| {{date}} | | | % | | |
| {{date}} | | | % | | |
| {{date}} | | | % | | |

## Traffic Source Breakdown

| Source | Visitors | Signups | Conv. Rate | Cost | CPA |
|--------|----------|---------|------------|------|-----|
| LinkedIn | | | % | $0 | - |
| Twitter/X | | | % | $0 | - |
| Reddit | | | % | $0 | - |
| Direct | | | % | - | - |
| Other | | | % | - | - |
| **Total** | | | % | | |

## Funnel Analysis

```
Impressions: {{N}}
    ↓ CTR: X%
Visitors: {{N}}
    ↓ Engagement: X%
Scrolled 50%+: {{N}}
    ↓ Intent: X%
Started Form: {{N}}
    ↓ Completion: X%
Signups: {{N}}
```

**Overall Conversion**: {{signups}} / {{visitors}} = {{X}}%

## A/B Test Results (if applicable)

| Variant | Visitors | Signups | Conv. Rate | Winner |
|---------|----------|---------|------------|--------|
| A (Control) | | | % | |
| B (Treatment) | | | % | |

**Statistical Significance**: [Yes/No at 95% confidence]

## Qualitative Signals

### Comments/Replies from Posts
- "[Quote from comment]" — [Source]
- "[Quote from comment]" — [Source]

### DMs/Emails Received
- {{count}} people reached out directly
- Common questions: [list]

## Decision Criteria

| Criterion | Threshold | Actual | Pass |
|-----------|-----------|--------|------|
| Total Visitors | ≥ 500 | {{N}} | ✅/❌ |
| Conversion Rate | ≥ 5% | {{X}}% | ✅/❌ |
| Total Signups | ≥ 25 | {{N}} | ✅/❌ |

## Insights

### What Worked
1. [Traffic source or message that performed well]
2. [Element that drove conversions]

### What Didn't Work
1. [Traffic source or message that underperformed]
2. [Friction point identified]

### Learnings for Product
1. [Insight about target audience]
2. [Insight about messaging/positioning]

---
Last Updated: {{date}}
Analytics Source: [Google Analytics / Plausible / etc.]
```

## Integration Points

| Command | Integration |
|---------|-------------|
| `/speckit.concept` | Receives validated problems, proceeds if GO |
| `/speckit.specify` | Uses discovery insights for requirements |
| `/speckit.launch` | References discovery for positioning |

## Quality Gates

| Gate | Condition | Severity |
|------|-----------|----------|
| Minimum Evidence | interviews >= 10 OR survey >= 50 OR landing visitors >= 500 | Warning |
| Signal Strength | avg_problem_severity >= 3.5 | Error |
| Decision Made | go_no_go != null | Error |

## Anti-Patterns

- Skipping discovery because "we know our customers"
- Interviewing only friends and family
- Leading questions that confirm your bias
- Treating "that would be nice" as validation
- Building before reaching minimum evidence threshold
- Ignoring negative signals

## Success Metrics

Discovery is successful when:
- [ ] Minimum evidence threshold reached
- [ ] Clear go/no-go decision made
- [ ] Key insights documented
- [ ] Next steps identified
- [ ] Stakeholder alignment achieved

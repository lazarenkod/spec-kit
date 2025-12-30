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
  - docs/discovery.md
  - docs/interviews/ (if interviews selected)
  - docs/surveys/ (if survey selected)
  - public/landing/ (if landing_page selected)
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

### Step 1: Capture Hypothesis

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

Based on `validation_method`, generate appropriate assets:

#### If interviews (default):

1. Load `customer-interview` skill
2. Generate interview script for problem discovery
3. Create scoring template
4. Prepare synthesis framework

#### If survey:

1. Load survey templates from `templates/shared/discover/survey-templates.md`
2. Generate problem validation survey
3. Configure distribution (email, social, paid panel)

#### If landing_page:

1. Load `landing-generator` skill
2. Generate smoke test landing page
3. Configure analytics and form backend
4. Prepare deployment instructions

#### If all:

Execute all three methods in sequence.

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

## Output: discovery.md

```markdown
# Discovery Report: {{problem_hypothesis}}

## Executive Summary

**Hypothesis**: {{problem_hypothesis}}
**Target Persona**: {{target_persona}}
**Validation Method**: {{validation_method}}
**Decision**: [GO / ITERATE / STOP]
**Confidence**: [High / Medium / Low]

## Validation Results

### Interviews (N = {{count}})

| Dimension | Avg Score | Range | Key Quote |
|-----------|-----------|-------|-----------|
| Problem Severity | X.X | X-X | "..." |
| Solution Pain | X.X | X-X | "..." |
| Willingness to Pay | X.X | X-X | "..." |
| Urgency | X.X | X-X | "..." |

### Survey Results (N = {{count}})

[If applicable - charts and analysis]

### Landing Page Results

[If applicable - conversion data]

## Key Insights

### Problems Validated
1. [Problem with evidence]
2. [Problem with evidence]

### Problems NOT Validated
1. [Assumption that was wrong]

### Surprising Discoveries
1. [Unexpected insight]

## Recommendations

### If GO:
- Proceed to `/speckit.concept` with these validated problems
- Focus MVP on [top problem]
- Target [specific segment] first

### If ITERATE:
- Test alternative hypothesis: [suggestion]
- Interview additional segment: [suggestion]
- Adjust value proposition to: [suggestion]

### If STOP:
- Kill current hypothesis
- Consider pivot to: [adjacent problem discovered]
- Or: Move to different market

## Evidence Appendix

### Interview Summaries
[Link to docs/interviews/]

### Survey Raw Data
[Link to docs/surveys/]

### Landing Page Analytics
[Link to analytics dashboard]

---
Generated by /speckit.discover
Validation Date: {{date}}
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

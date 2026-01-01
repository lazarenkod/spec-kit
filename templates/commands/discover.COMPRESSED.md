---
description: Customer discovery before building
persona: research-agent
inputs:
  problem_hypothesis: { type: string, required: true }
  target_persona: { type: string, required: true }
  method: { type: enum, options: [interviews, survey, landing_page, all], default: interviews }
outputs:
  - docs/discover/hypothesis.md
  - docs/discover/interview-guide.md
  - docs/discover/analysis.md
  - docs/discover/decision.md
  - docs/discover/discovery-report.md
quality_gates:
  - { name: minimum_interviews, condition: ">= 10", severity: warning }
  - { name: signal_strength, condition: "avg >= 3.5", severity: error }
handoffs:
  - { label: Create Concept, agent: speckit.concept, condition: "GO decision" }
  - { label: Specify Feature, agent: speckit.specify, condition: "Validated problem" }
  - { label: Design Launch, agent: speckit.launch, condition: "Landing page insights" }
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 8000
  cache_hierarchy: full
---

## Input
```text
$ARGUMENTS
```

---

## Init [REF:INIT-001]

```text
EXECUTE language-loading → ARTIFACT_LANGUAGE
SET DISCOVERY_METHOD = method (interviews | survey | landing_page | all)
CREATE docs/discover/ directory
```

---

## Workflow Overview

```text
HYPOTHESIZE → PREPARE → EXECUTE → ANALYZE → DECIDE

1. Frame hypothesis      → hypothesis.md
2. Generate assets       → interview-guide.md, survey.md, landing-spec.md
3. Execute discovery     → interview-notes/, survey-results.md, landing-metrics.md
4. Analyze findings      → analysis.md, scoring.md
5. Make decision         → decision.md, discovery-report.md
```

---

## Step 0: Frame Problem Hypothesis

```text
IF problem_hypothesis provided → validate format
ELSE → ask: "What problem are you solving, for whom, and why it matters?"

Hypothesis Format:
  "[Target Persona] has [Problem] when [Context], causing [Pain/Cost].
   Current workarounds ([Alternatives]) are inadequate because [Gap].
   A solution that [Value Prop] would be worth [WTP Signal] to them."
```

Output: `docs/discover/hypothesis.md`

---

## Step 1: Select Discovery Method

| Method | Best For | Evidence | Time |
|--------|----------|----------|------|
| **Interviews** | Deep insights, B2B, complex problems | 10-20 conversations | 2-4 weeks |
| **Survey** | Quantitative validation, large N | 50+ responses | 1-2 weeks |
| **Landing Page** | Demand testing, consumer | 500+ visitors, 5%+ CVR | 1-2 weeks |
| **All** | High-stakes, investor-ready | Combined evidence | 4-6 weeks |

---

## Step 2: Generate Discovery Assets

### 2a: Interview Guide (if method includes interviews)

```text
Mom Test Principles:
- Talk about THEIR life, not your idea
- Ask about specifics in the PAST, not hypotheticals
- Talk less, listen more
- Bad data: compliments, fluff, hypotheticals
- Good data: past behaviors, workarounds, money spent
```

**Core Questions**:

| Category | Example Questions |
|----------|-------------------|
| Context | "Walk me through the last time you [problem area]..." |
| Problem | "What made that frustrating?" "What happened next?" |
| Severity | "How often does this happen?" "What does it cost you?" |
| Workarounds | "What do you do today to solve this?" |
| Commitment | "Have you paid for any solutions?" "How much?" |

Output: `docs/discover/interview-guide.md`

### 2b: Survey Template (if method includes survey)

**Question Types**:

| Type | Questions |
|------|-----------|
| Screener | Role, industry, frequency of problem |
| Problem Severity | 1-5 scale, frequency, impact |
| Current Solutions | What they use, satisfaction, spend |
| Interest | WTP, feature priorities |
| Open-ended | Biggest frustration, ideal solution |

Output: `docs/discover/survey-template.md`

### 2c: Landing Page Spec (if method includes landing_page)

| Element | Content |
|---------|---------|
| Headline | Problem-focused (not solution) |
| Subheadline | Who + key benefit |
| CTA | "Get Early Access" / "Join Waitlist" |
| Form | Email only (minimize friction) |

**Metrics Target**: 500+ visitors, ≥5% conversion rate

Output: `docs/discover/landing-spec.md`, `public/landing/index.html`

---

## Step 3: Execute Discovery

### 3a: Interview Execution

```text
Per Interview:
1. Schedule 30-45 min conversation
2. Use interview guide (but stay flexible)
3. Record with permission OR take detailed notes
4. Capture direct quotes
5. Score immediately after (5-point scales)

Scoring Dimensions:
- Problem Severity (1-5)
- Frequency (daily/weekly/monthly/rarely)
- Current Spend ($0 / $1-50 / $50-200 / $200+)
- Urgency (active search / passive / not looking)
- Decision Authority (yes/no/influence)
```

Output: `docs/discover/interviews/{{name}}-{{date}}.md`

### 3b: Survey Execution

```text
Distribution channels: email list, social, paid panel, communities
Target: 50+ responses minimum
Track: completion rate, drop-off points
```

Output: `docs/discover/survey-results.md`

### 3c: Landing Page Execution

```text
Traffic sources: LinkedIn, Twitter/X, Reddit, communities
Track daily: visitors, signups, conversion rate, top sources
Run for: 7-14 days minimum
```

Output: `docs/discover/landing-metrics.md`

---

## Step 4: Analyze Findings

### 4a: Pattern Recognition

```text
AGGREGATE all interview scores
IDENTIFY recurring themes (3+ mentions = pattern)
CALCULATE:
  - % with problem severity ≥ 4
  - % actively searching for solution
  - % with budget > $50/mo
  - Average problem severity
```

### 4b: Signal Strength Matrix

| Signal | Strong (✅) | Weak (❌) |
|--------|------------|----------|
| Problem | Specific past examples, emotional language | Vague, hypothetical |
| Frequency | Daily/weekly occurrence | Monthly/rarely |
| Spend | Already paying for workarounds | Expects free |
| Urgency | Actively searching | "Nice to have" |
| Authority | Decision maker | Need to check |

### 4c: Pivot/Persevere Signals

| Signal Type | What It Means |
|-------------|---------------|
| **STRONG GO** | 7+ interviews with severity ≥4, specific pain, WTP evidence |
| **WEAK GO** | 5-6 interviews with mixed signals, needs more data |
| **PIVOT** | <5 with high severity, problem exists but different persona |
| **NO-GO** | Consistent low severity, happy with alternatives, no WTP |

Output: `docs/discover/analysis.md`

---

## Step 5: Make Decision

### Decision Framework

| Criterion | GO Threshold | Actual | Pass |
|-----------|--------------|--------|------|
| Interviews completed | ≥ 10 | | |
| Avg problem severity | ≥ 3.5/5 | | |
| % with severity ≥4 | ≥ 50% | | |
| % actively searching | ≥ 30% | | |
| WTP signals | ≥ 3 concrete | | |

### Decision Options

| Decision | Criteria | Next Action |
|----------|----------|-------------|
| **GO** | All thresholds met, clear problem-solution fit | → /speckit.concept |
| **ITERATE** | Some signals, need refinement | Refine hypothesis, more interviews |
| **PIVOT** | Different persona or problem emerging | New hypothesis, restart discovery |
| **NO-GO** | Insufficient evidence after good effort | Document learnings, move on |

Output: `docs/discover/decision.md`

---

## Artifact Summary

| # | Artifact | Created In | Purpose |
|---|----------|------------|---------|
| 1 | hypothesis.md | Step 0 | Problem hypothesis statement |
| 2 | interview-guide.md | Step 2a | Mom Test question guide |
| 3 | survey-template.md | Step 2b | Survey questions + distribution |
| 4 | landing-spec.md | Step 2c | Landing page wireframe |
| 5 | landing/index.html | Step 2c | Smoke test landing page |
| 6 | interviews/*.md | Step 3a | Individual interview notes |
| 7 | survey-results.md | Step 3b | Aggregated survey data |
| 8 | landing-metrics.md | Step 3c | Landing page performance |
| 9 | analysis.md | Step 4 | Pattern analysis, scoring |
| 10 | decision.md | Step 5 | GO/NO-GO decision + rationale |
| 11 | discovery-report.md | Step 5 | Executive summary |

---

## Self-Review Phase [REF:SR-001]

### Quality Criteria

| ID | Check | Severity |
|----|-------|----------|
| SR-DISCOVER-01 | Hypothesis clearly stated | CRITICAL |
| SR-DISCOVER-02 | Minimum interviews reached (≥10) | HIGH |
| SR-DISCOVER-03 | Mom Test principles followed | HIGH |
| SR-DISCOVER-04 | All interviews scored | MEDIUM |
| SR-DISCOVER-05 | Patterns identified (≥3) | HIGH |
| SR-DISCOVER-06 | Signal strength calculated | HIGH |
| SR-DISCOVER-07 | Decision made (GO/ITERATE/PIVOT/NO-GO) | CRITICAL |
| SR-DISCOVER-08 | Next steps documented | HIGH |
| SR-DISCOVER-09 | Quotes captured (≥5 good quotes) | MEDIUM |
| SR-DISCOVER-10 | Anti-patterns avoided | MEDIUM |

### Anti-Patterns

```text
- Skipping discovery ("we know our customers")
- Interviewing only friends/family
- Leading questions confirming bias
- Treating "that would be nice" as validation
- Building before minimum evidence
- Ignoring negative signals
```

---

## Quality Gates

| Gate | Condition | Severity |
|------|-----------|----------|
| Minimum Evidence | interviews ≥ 10 OR survey ≥ 50 OR visitors ≥ 500 | Warning |
| Signal Strength | avg_problem_severity ≥ 3.5 | Error |
| Decision Made | go_no_go != null | Error |

---

## Integration Points

| Command | Integration |
|---------|-------------|
| `/speckit.concept` | Receives validated problems if GO |
| `/speckit.specify` | Uses discovery insights for requirements |
| `/speckit.launch` | References discovery for positioning |

---

## Report Format

```text
┌─────────────────────────────────────────────────────────────┐
│ /speckit.discover Complete                                   │
├─────────────────────────────────────────────────────────────┤
│ Hypothesis: {problem_hypothesis}                             │
│ Method: {interviews | survey | landing_page | all}           │
│                                                              │
│ Evidence Collected:                                          │
│   Interviews: {N}    Surveys: {N}    Landing Visitors: {N}  │
│                                                              │
│ Signal Strength: {X.X}/5.0                                   │
│ Decision: {GO | ITERATE | PIVOT | NO-GO}                    │
│                                                              │
│ Artifacts Created: {count}                                   │
└─────────────────────────────────────────────────────────────┘
```

### Next Steps

| Decision | Action |
|----------|--------|
| GO | → `/speckit.concept` to capture product vision |
| ITERATE | Refine hypothesis, schedule more interviews |
| PIVOT | Document learnings, create new hypothesis |
| NO-GO | Archive learnings, explore different problem |

---

## Context

{ARGS}

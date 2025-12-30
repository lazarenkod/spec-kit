# Customer Interview Skill

## Purpose

Generate structured interview scripts and synthesis frameworks for customer discovery, following the Mom Test methodology to extract actionable insights about problems, behaviors, and willingness to pay.

## Trigger

- User needs to validate a problem hypothesis
- User wants to conduct customer discovery interviews
- User asks for interview questions or scripts

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `problem_hypothesis` | Yes | The problem you believe exists |
| `target_persona` | Yes | Who experiences this problem |
| `interview_type` | No | discovery, validation, or pricing (default: discovery) |
| `current_solutions` | No | Known alternatives in the market |

## Skill Execution

### Step 1: Analyze Problem Hypothesis

```yaml
hypothesis_analysis:
  problem_statement: "{{problem_hypothesis}}"
  target_persona: "{{target_persona}}"

  assumptions_to_validate:
    - "The problem exists and is significant"
    - "The target persona experiences this problem"
    - "Current solutions are inadequate"
    - "People would pay to solve this problem"

  risk_level: "[High/Medium/Low based on novelty]"
```

### Step 2: Generate Interview Script

Based on interview_type, generate appropriate script:

#### Discovery Interview (30-45 min)

```markdown
## Opening (2 min)
"Thanks for taking the time to chat. I'm researching [problem domain] to understand
how people currently handle [specific challenge]. I'm not selling anything - just
trying to understand your experience."

## Context Questions (5 min)
1. "Tell me about your role and what you do day-to-day."
2. "How does [problem domain] fit into your work?"
3. "Who else in your organization deals with this?"

## Problem Exploration (15 min)
4. "Walk me through the last time you dealt with [specific problem]."
   - Follow-up: "What happened next?"
   - Follow-up: "How did that make you feel?"

5. "What's the most frustrating part of [current process]?"
   - Follow-up: "Why is that particularly frustrating?"

6. "How often does this problem come up?"
   - Follow-up: "Can you estimate the time/cost impact?"

## Current Solutions (10 min)
7. "What do you currently use to handle this?"
   - Follow-up: "What do you like about it?"
   - Follow-up: "What do you wish was different?"

8. "Have you tried other solutions? Why did you switch/stay?"

9. "If you could wave a magic wand, what would the ideal solution do?"

## Closing (5 min)
10. "Is there anything else about [problem] I should have asked?"
11. "Would you be open to a follow-up conversation once we have something to show?"
12. "Is there anyone else you'd recommend I talk to about this?"
```

#### Validation Interview (45-60 min)

For validating a specific solution direction after initial discovery.

#### Pricing Interview (30 min)

For validating willingness to pay and pricing model.

### Step 3: Create Question Bank

Generate follow-up questions using Mom Test principles:

```yaml
question_bank:
  past_behavior:
    - "When was the last time you tried to solve this?"
    - "What have you already tried?"
    - "How much time did you spend on this last week?"

  pain_severity:
    - "What happens when you don't solve this?"
    - "Who else is affected by this problem?"
    - "What's the cost of leaving this unsolved?"

  current_solutions:
    - "What are you currently spending on this?"
    - "Why did you choose [current solution]?"
    - "What would make you switch?"

  decision_process:
    - "Who else would need to approve a new solution?"
    - "What's your timeline for solving this?"
    - "What budget do you have for tools like this?"
```

### Step 4: Generate Scoring Framework

```yaml
signal_scoring:
  after_each_interview:
    problem_severity:
      score: "[1-5]"
      evidence: "Specific quote or observation"

    current_solution_pain:
      score: "[1-5]"
      evidence: "What they said about alternatives"

    willingness_to_pay:
      score: "[1-5]"
      evidence: "Budget mentioned, current spending"

    urgency:
      score: "[1-5]"
      evidence: "Timeline, active searching"

    decision_authority:
      score: "[1-5]"
      evidence: "Can buy alone, needs approval"

  scoring_guide:
    5: "Strong positive signal with concrete evidence"
    4: "Positive signal with some specifics"
    3: "Neutral or mixed signals"
    2: "Weak or concerning signal"
    1: "Strong negative signal"
```

### Step 5: Output Interview Package

```markdown
## Interview Package: {{problem_hypothesis}}

### Target Persona
{{target_persona}}

### Interview Script
[Generated script based on type]

### Question Bank
[Context-specific follow-ups]

### Scoring Template
[Per-interview scoring sheet]

### Synthesis Template
[For aggregating across interviews]

### Mom Test Reminders
- Listen more than you talk (80/20)
- Ask about past behavior, not hypothetical future
- Look for emotional responses
- Don't pitch - discover
- Take verbatim notes
```

## Output Format

```yaml
interview_package:
  metadata:
    problem: "{{problem_hypothesis}}"
    persona: "{{target_persona}}"
    interview_type: "{{interview_type}}"
    generated_at: "{{timestamp}}"

  script:
    duration: "30-45 minutes"
    sections: [opening, context, exploration, solutions, closing]
    questions: [...]

  question_bank:
    categories: [past_behavior, pain_severity, current_solutions, decision_process]
    questions: [...]

  scoring:
    dimensions: [problem_severity, solution_pain, wtp, urgency, authority]
    template: "..."

  synthesis:
    minimum_interviews: 10
    template: "..."
```

## Mom Test Anti-Patterns

| Bad Question | Why It's Bad | Good Alternative |
|--------------|--------------|------------------|
| "Would you buy this?" | Hypothetical, people please | "What have you tried to solve this?" |
| "Do you think this is a good idea?" | Opinion, not behavior | "How are you handling this today?" |
| "How much would you pay?" | Hypothetical pricing | "What are you currently spending?" |
| "Would this feature be useful?" | Leading, vague | "Walk me through your workflow" |

## Validation Thresholds

```yaml
go_no_go_criteria:
  green_light:
    interviews_completed: ">= 10"
    avg_problem_severity: ">= 4.0"
    avg_willingness_to_pay: ">= 3.5"
    decision_makers_interviewed: ">= 50%"

  yellow_light:
    interviews_completed: "5-9"
    avg_problem_severity: "3.0-3.9"
    recommendation: "Continue interviewing, refine hypothesis"

  red_light:
    interviews_completed: "< 5"
    avg_problem_severity: "< 3.0"
    recommendation: "Pivot hypothesis or kill"
```

## Integration

This skill is used by:
- `/speckit.discover` - Main discovery workflow
- `/speckit.concept` - When validation_needed flag is set

References:
- `templates/shared/discover/interview-scripts.md` - Full script templates
- `templates/shared/discover/survey-templates.md` - Quantitative follow-up

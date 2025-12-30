# Customer Interview Scripts

## Purpose

Generate structured interview scripts for customer discovery, focusing on problem validation, willingness-to-pay assessment, and solution-market fit.

## Interview Types

### 1. Problem Discovery Interview

**Duration**: 30-45 minutes
**Stage**: Early discovery (validating problem exists)

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

### 2. Solution Validation Interview

**Duration**: 45-60 minutes
**Stage**: Mid discovery (validating solution direction)

```markdown
## Opening (2 min)
"Thanks for chatting again. Based on conversations like ours, we've been thinking
about [solution direction]. I'd love to get your reaction and feedback."

## Recap Problem (5 min)
1. "Last time you mentioned [key problem]. Is that still a priority?"
2. "Has anything changed since we last spoke?"

## Solution Walkthrough (15 min)
3. "Let me describe what we're thinking..." [Present concept/mockup]
   - Pause after each section for reactions

4. "What's your initial reaction?"
   - Follow-up: "What excites you?"
   - Follow-up: "What concerns you?"

5. "How would this fit into your current workflow?"

## Feature Prioritization (10 min)
6. "If you could only have one of these features, which would it be?"
7. "Which feature would you NOT miss if we removed it?"
8. "What's missing that you'd need before you could use this?"

## Willingness to Pay (10 min)
9. "If this solved [main problem], would it be worth paying for?"
10. "What budget would you have for something like this?"
    - Or: "What do you currently spend on [related solutions]?"
11. "Who would need to approve a purchase like this?"

## Closing (5 min)
12. "Would you be interested in being an early tester?"
13. "What would make you say 'I need to try this right now'?"
14. "Any final thoughts or suggestions?"
```

### 3. Pricing Validation Interview

**Duration**: 30 minutes
**Stage**: Late discovery (validating pricing model)

```markdown
## Opening (2 min)
"We're finalizing our pricing and I'd love your input to make sure it makes
sense for people like you."

## Value Recap (5 min)
1. "What would be the biggest benefit of [product] for you?"
2. "How much time/money would this save you per [week/month]?"

## Pricing Exploration (15 min)
3. "I'm going to share some price points. Just react naturally."

   Present anchors:
   - "At $X/month, would this be an obvious yes?"
   - "At $Y/month, would this be too expensive?"
   - "At $Z/month, how would you feel?"

4. "What pricing model makes sense?"
   - Per user / per seat
   - Usage-based
   - Flat rate
   - Tiered

5. "Would you prefer monthly or annual billing?"
6. "What would make the higher tier worth it for you?"

## Competitive Context (5 min)
7. "What do you currently pay for [similar solution]?"
8. "How does our pricing compare to what you expected?"

## Closing (3 min)
9. "Based on everything we discussed, would you buy at $X?"
10. "What's the one thing that would make you hesitate?"
```

## Interview Best Practices

### Do's
- Listen more than you talk (aim for 80/20)
- Ask "why" and "tell me more" frequently
- Take verbatim notes on exact words used
- Look for emotional responses (frustration, excitement)
- Ask about past behavior, not hypothetical future
- Record with permission for later analysis

### Don'ts
- Don't pitch your solution too early
- Don't lead with what you want to hear
- Don't ask "would you use X?" (everyone says yes)
- Don't interrupt - let them fill silence
- Don't take "that would be nice" as validation
- Don't skip the willingness-to-pay questions

## Question Framework: The Mom Test

Based on Rob Fitzpatrick's methodology:

| Bad Question | Good Question |
|--------------|---------------|
| "Would you buy this?" | "When was the last time you tried to solve this?" |
| "Do you think this is a good idea?" | "What have you already tried?" |
| "How much would you pay?" | "What are you currently spending?" |
| "Would this feature be useful?" | "Walk me through how you handle this today" |

## Signal Scoring

After each interview, score the following (1-5):

```yaml
problem_severity:
  score: _
  evidence: "Quote or observation"

current_solution_pain:
  score: _
  evidence: "Quote or observation"

willingness_to_pay:
  score: _
  evidence: "Budget range mentioned, alternatives paid for"

urgency:
  score: _
  evidence: "Active searching, timeline pressure"

decision_authority:
  score: _
  evidence: "Can buy alone, needs approval, influencer only"

interview_quality:
  score: _
  notes: "How candid were they? Did we get real data?"
```

## Interview Synthesis Template

After N interviews (N >= 10), synthesize findings:

```markdown
## Discovery Synthesis: [Problem Domain]

### Sample
- Interviews conducted: N
- Personas represented: [List]
- Companies represented: [List by type/size]

### Problem Validation
**Strongest problems (mentioned by >50%):**
1. [Problem] - mentioned N times
2. [Problem] - mentioned N times

**Surprising findings:**
- [Insight with quote]

### Current Solutions Landscape
| Solution | % Using | Satisfaction | Switching Likelihood |
|----------|---------|--------------|---------------------|
| [Tool A] | X% | Low/Med/High | Low/Med/High |

### Willingness to Pay
- Average budget range: $X - $Y/month
- Decision maker in interviews: X%
- Average decision timeline: X weeks

### Go/No-Go Assessment

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Problem severity | _/5 | [Summary] |
| Market size | _/5 | [Summary] |
| Willingness to pay | _/5 | [Summary] |
| Competitive advantage | _/5 | [Summary] |

**Recommendation:** [GO / NO-GO / PIVOT]
**Confidence:** [High / Medium / Low]

### If GO: Key Requirements
1. Must-have: [Feature from interviews]
2. Must-have: [Feature from interviews]
3. Nice-to-have: [Feature from interviews]

### If PIVOT: Direction Suggested
[Based on adjacent problems discovered]
```

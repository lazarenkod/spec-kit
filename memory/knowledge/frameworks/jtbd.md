# Jobs-to-Be-Done (JTBD) Framework Guide

## Overview

Jobs-to-Be-Done is a theory of consumer behavior that focuses on understanding the "job" a customer is trying to accomplish when they "hire" a product or service. Instead of focusing on demographics or product features, JTBD focuses on the progress customers are trying to make in specific circumstances.

**Origin**: Clayton Christensen (Harvard Business School), further developed by Anthony Ulwick (Outcome-Driven Innovation) and Alan Klement (Jobs Stories).

## Core Concepts

### The Job Statement

**Format**: "When [situation], I want to [motivation], so I can [expected outcome]"

| Component | Description | Questions to Ask |
|-----------|-------------|------------------|
| **When (Situation)** | The context or trigger | What circumstances prompt this? What just happened? |
| **I want to (Motivation)** | The action or capability needed | What are they trying to do? What progress do they seek? |
| **So I can (Outcome)** | The desired end state | What does success look like? What's the benefit? |

**Example**:
```
When I'm running late for a meeting and need breakfast,
I want to get something quick and filling,
So I can start my day energized without being late.
```

### Three Types of Jobs

| Type | Description | Example |
|------|-------------|---------|
| **Functional** | Practical task to accomplish | "Transfer money to my friend" |
| **Emotional** | How the customer wants to feel | "Feel confident my money arrived safely" |
| **Social** | How the customer wants to be perceived | "Be seen as generous and reliable by my friend" |

**Hierarchy**: Emotional and social jobs often outweigh functional jobs in purchasing decisions.

### Hiring and Firing

Customers "hire" products to get a job done and "fire" them when they don't perform.

```text
Current Solution ──────────────────────────────► New Solution
       │                                              │
       │  Push of Current Situation                   │
       │  "This is frustrating, too slow"             │
       │                                              │
       │  Pull of New Solution                        │
       │  "That looks better, easier"                 │
       │                                              │
       │  ◄───── Anxiety of New ─────►                │
       │  "Will it work? Is it risky?"                │
       │                                              │
       │  ◄───── Habit of Current ───►                │
       │  "I know how this works"                     │
       └──────────────────────────────────────────────┘
```

**Four Forces of Progress**:
1. **Push**: Frustration with current solution
2. **Pull**: Attraction to new solution
3. **Anxiety**: Fear of the new solution
4. **Habit**: Comfort with the current way

For a switch to happen: Push + Pull > Anxiety + Habit

## JTBD Interview Techniques

### The Timeline Interview

Walk backwards from a purchase/switch decision:

```text
Purchase ◄─── First Use ◄─── Evaluation ◄─── First Thought ◄─── Trigger
    │             │              │               │                │
    ▼             ▼              ▼               ▼                ▼
"When did    "What was    "What did     "When did you    "What happened
you buy?"    first use    you           first think      that made you
             like?"       compare?"     about this?"     start looking?"
```

**Key Questions**:
1. "Tell me about when you [purchased/switched to X]..."
2. "What was going on in your life at that time?"
3. "What other solutions did you consider?"
4. "What almost stopped you from switching?"
5. "How did you feel after the switch?"

### Switch Interview Template

```markdown
## Before
- What were you using before?
- What worked about it?
- What didn't work?

## Trigger
- What happened that made you start looking?
- When did this happen?
- Who else was involved in the decision?

## Search
- How did you find alternatives?
- What did you compare?
- What criteria mattered most?

## Decision
- What almost stopped you?
- What convinced you to switch?
- Who influenced the decision?

## After
- How was the first use?
- What surprised you?
- Would you recommend it?
```

## Job Mapping

### Eight Steps of a Job

Every job follows a similar lifecycle:

| Step | Description | Example (Hiring a Contractor) |
|------|-------------|-------------------------------|
| 1. **Define** | Determine goals and plan | "What work needs to be done?" |
| 2. **Locate** | Gather inputs and resources | "Where do I find contractors?" |
| 3. **Prepare** | Set up the environment | "Get quotes, check references" |
| 4. **Confirm** | Verify readiness | "Is everything in place to start?" |
| 5. **Execute** | Perform the job | "Contractor does the work" |
| 6. **Monitor** | Check progress | "Is it on schedule? Quality ok?" |
| 7. **Modify** | Make adjustments | "Handle unexpected issues" |
| 8. **Conclude** | Finish and wrap up | "Final inspection, payment" |

### Opportunity Identification

For each step, identify:
- **Desired outcomes**: What does success look like?
- **Pain points**: Where does the current solution fail?
- **Underserved needs**: What's not being addressed?
- **Overserved needs**: What's more than necessary?

## Outcome-Driven Innovation (ODI)

### Outcome Statement Format

**Format**: [Direction] + [Metric] + [Object of control] + [Context]

**Examples**:
- "Minimize the time it takes to find relevant information when researching"
- "Minimize the likelihood of making an error when entering data"
- "Increase the ability to understand the status at a glance"

### Opportunity Score

```text
Opportunity = Importance + max(0, Importance - Satisfaction)

Where:
- Importance: 1-10 scale (how important is this outcome)
- Satisfaction: 1-10 scale (how satisfied with current solution)
```

| Score | Interpretation |
|-------|----------------|
| 15+ | Underserved (high opportunity) |
| 10-15 | Appropriately served |
| <10 | Overserved (low opportunity) |

### Opportunity Landscape

```text
High Importance
        │
        │  UNDERSERVED          WELL-SERVED
        │  (Opportunity!)       (Maintain)
        │       ●                   ●
        │           ●           ●
        │                   ●
        │───────────────────────────────────
        │                           ●
        │  TABLE STAKES             ●
        │  (Must have)          OVERSERVED
        │       ●               (Reduce?)
        │
Low Importance ─────────────────────────────►
                Low              High
               Satisfaction    Satisfaction
```

## Jobs Stories vs User Stories

### User Story (Persona-Based)

```
As a [persona],
I want [feature],
So that [benefit].
```

**Problem**: Focuses on persona, not situation. Can lead to feature bloat.

### Jobs Story (Situation-Based)

```
When [situation],
I want to [motivation],
So I can [expected outcome].
```

**Advantage**: Focuses on context, leads to solutions that fit the moment.

### Comparison

| Aspect | User Story | Jobs Story |
|--------|------------|------------|
| Focus | Who (persona) | When (situation) |
| Leads to | Features for personas | Solutions for moments |
| Risk | Feature creep | May miss user types |
| Best for | Known user segments | Novel problems |

## Common JTBD Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Job = Task | Tasks are actions, jobs are progress | Focus on the progress, not the activity |
| Job = Feature | Features are solutions, not jobs | Ask "what job does this feature address?" |
| Too abstract | "Be happy" is not actionable | Make it specific and observable |
| Too narrow | "Click the button" is a task | Zoom out to the real goal |
| Ignoring emotional jobs | Functional alone misses 70% of motivation | Always ask "how do you want to feel?" |

## JTBD Canvas Template

```markdown
# Job Canvas: [Job Title]

## The Job
When [situation], I want to [motivation], so I can [outcome].

## Job Executor
Who is doing the job? (Note: not a persona, but role in this situation)

## Functional Aspects
- What practical tasks must be accomplished?
- What's the input and output?

## Emotional Aspects
- How does the person want to feel?
- What anxieties exist?

## Social Aspects
- How do they want to be perceived?
- Who else is involved or watching?

## Current Solutions
| Solution | Hired Because | Fired Because |
|----------|---------------|---------------|
| [Current 1] | [Pros] | [Cons] |
| [Current 2] | [Pros] | [Cons] |

## Desired Outcomes
| Outcome | Importance (1-10) | Satisfaction (1-10) | Opportunity |
|---------|-------------------|---------------------|-------------|
| [Outcome 1] | X | Y | I + max(0, I-S) |

## Opportunities
Based on underserved outcomes, what solutions could we create?
```

## Resources

- **Books**:
  - "Competing Against Luck" by Clayton Christensen
  - "The Jobs to Be Done Playbook" by Jim Kalbach
  - "When Coffee and Kale Compete" by Alan Klement

- **Tools**:
  - JTBD Canvas (Strategyzer)
  - Switch Interview template
  - Outcome-Driven Innovation scoring

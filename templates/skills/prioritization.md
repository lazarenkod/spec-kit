---
description: Prioritize features using ICE/RICE frameworks with data-driven scoring
---

## User Input

```text
$ARGUMENTS
```

## Purpose

This skill applies structured prioritization frameworks (ICE, RICE, MoSCoW, Weighted Scoring) to features, stories, or backlog items. Produces defensible, data-informed priority rankings.

## When to Use

- After `/speckit.concept` to prioritize epics and features
- During sprint planning to rank stories
- When stakeholders disagree on priorities
- For roadmap planning and trade-off decisions

## Execution Steps

### 1. Gather Prioritization Context

Parse from user input or load from artifacts:

```text
1. Read specs/concept.md for feature list (if exists)
2. Read current spec.md for requirements (if exists)
3. Identify items to prioritize:
   - Epics (EPIC-xxx)
   - Features (EPIC-xxx.Fxx)
   - Stories (EPIC-xxx.Fxx.Sxx)
   - Requirements (FR-xxx, NFR-xxx)
```

### 2. Select Framework

Choose based on context:

| Framework | Best For | Key Factors |
|-----------|----------|-------------|
| **ICE** | Quick prioritization, early stage | Impact, Confidence, Ease |
| **RICE** | Data-driven decisions, growth teams | Reach, Impact, Confidence, Effort |
| **MoSCoW** | Scope management, stakeholder alignment | Must/Should/Could/Won't |
| **Weighted** | Complex multi-factor decisions | Custom criteria + weights |

Default to **RICE** unless user specifies otherwise.

### 3. Define Scoring Criteria

#### ICE Framework
```text
Impact (1-10): How much will this improve key metrics?
  10 = Massive impact on core KPIs
  5  = Moderate improvement
  1  = Minimal/unknown impact

Confidence (1-10): How sure are we about impact?
  10 = Have data/experiments proving impact
  5  = Some evidence or strong intuition
  1  = Pure speculation

Ease (1-10): How easy to implement?
  10 = Days of work, low complexity
  5  = Weeks of work, moderate complexity
  1  = Months of work, high complexity

ICE Score = (Impact × Confidence × Ease) / 10
```

#### RICE Framework
```text
Reach (users/quarter): How many users affected?
  Estimate based on:
  - User segments targeted
  - Feature visibility
  - Activation patterns

Impact (0.25-3): How much per user?
  3   = Massive (10x improvement)
  2   = High (significant improvement)
  1   = Medium (noticeable improvement)
  0.5 = Low (minimal improvement)
  0.25= Minimal

Confidence (%): How sure are we?
  100% = High confidence, have data
  80%  = Medium, some evidence
  50%  = Low, speculation

Effort (person-weeks): How much work?
  Estimate total person-weeks

RICE Score = (Reach × Impact × Confidence) / Effort
```

### 4. Score Each Item

For each feature/story:

```text
1. Define what "success" looks like
2. Estimate Impact based on:
   - User value (from personas)
   - Business value (from objectives)
   - Strategic alignment
3. Estimate Effort based on:
   - Technical complexity
   - Dependencies
   - Team expertise
4. Assess Confidence based on:
   - Existing data/research
   - Similar past features
   - User feedback strength
5. Calculate score using chosen formula
```

### 5. Generate Priority Matrix

```markdown
## Prioritization Results

**Framework**: [ICE/RICE/MoSCoW/Weighted]
**Date**: [DATE]
**Items Scored**: [N]

### Priority Ranking

| Rank | Item | Score | Impact | Effort | Confidence | Recommendation |
|------|------|-------|--------|--------|------------|----------------|
| 1 | [ID] [Name] | [score] | [H/M/L] | [weeks] | [%] | Must do |
| 2 | [ID] [Name] | [score] | [H/M/L] | [weeks] | [%] | Should do |
| ... | ... | ... | ... | ... | ... | ... |

### Priority Distribution

```text
MUST (P1):   ████████ 8 items (40%)
SHOULD (P2): ████ 4 items (20%)
COULD (P3):  ██████ 6 items (30%)
WON'T:       ██ 2 items (10%)
```

### Effort vs Impact Matrix

```text
           Low Effort    High Effort
High      |  QUICK WINS  |  BIG BETS   |
Impact    |  [items]     |  [items]    |
          |--------------|-------------|
Low       |  FILL-INS    |  MONEY PITS |
Impact    |  [items]     |  [items]    |
```
```

### 6. Stakeholder Alignment

Generate talking points for each priority tier:

```markdown
## Priority Justification

### P1 (Must Have)

**[Item Name]**
- **Why P1**: [business justification]
- **User Impact**: [who benefits, how much]
- **Risk if Delayed**: [consequences]
- **Dependencies**: [what it blocks]

### P2 (Should Have)

**[Item Name]**
- **Why P2**: [value vs effort trade-off]
- **Upgrade Path**: [what would make it P1]
- **Downgrade Risk**: [what would make it P3]

### P3 (Could Have)

**[Item Name]**
- **Why P3**: [nice-to-have rationale]
- **Future Consideration**: [when might this become priority]
```

### 7. Output

Save to `specs/research/prioritization.md` and update:

```text
1. Update concept.md priorities if they changed
2. Update spec.md FR priorities if applicable
3. Generate handoff summary for stakeholders
```

## Quick Mode

For rapid prioritization without full analysis:

```text
/speckit.prioritization --quick

Quick scores using simplified 1-5 scale:
- Value: How much users want this (1-5)
- Effort: How hard to build (1-5)
- Priority Score = Value / Effort
```

## Integration with Spec Kit

This skill feeds into:
- `/speckit.concept` → Hierarchy priority assignments (P1a, P1b, P2)
- `/speckit.specify` → FR priority fields
- `/speckit.plan` → Implementation sequencing
- `/speckit.tasks` → Sprint planning order

## Example

**Input**: "Prioritize features for our project management MVP"

**Output**:
```text
Priority Ranking (RICE):

1. EPIC-002.F01 Task Creation (Score: 156)
   - Reach: 1000 users, Impact: 2, Confidence: 90%, Effort: 3w
   - Recommendation: P1a - Core MVP functionality

2. EPIC-001.F01 User Registration (Score: 112)
   - Reach: 800 users, Impact: 1, Confidence: 100%, Effort: 2w
   - Recommendation: P1a - Prerequisite for everything

3. EPIC-003.F01 Time Tracking (Score: 48)
   - Reach: 400 users, Impact: 2, Confidence: 60%, Effort: 4w
   - Recommendation: P2 - Post-MVP enhancement
```

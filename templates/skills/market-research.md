---
description: Research market landscape, competitors, and user pain points for a feature concept
---

## User Input

```text
$ARGUMENTS
```

## Purpose

This skill performs comprehensive market research to validate a feature concept before detailed specification. It uses web search to gather real data about competitors, user complaints, and market trends.

## Execution Steps

### 1. Parse Research Context

Extract from user input or current concept.md:
- **Domain/Industry**: What market space?
- **Problem Statement**: What pain point being addressed?
- **Target Users**: Who are the users?
- **Known Competitors**: Any mentioned alternatives?

### 2. Competitor Analysis

Use WebSearch to research:

```text
Search queries to execute:
1. "[domain] software solutions 2025"
2. "[problem] tools alternatives comparison"
3. "[competitor name] reviews complaints" (for each known competitor)
4. "[domain] market leaders features"
```

For each competitor found, document:
- Name and positioning
- Key features
- Pricing model (if public)
- User complaints/limitations
- What they do well

### 3. User Pain Points Research

Use WebSearch to find:

```text
Search queries:
1. "[target user role] workflow challenges 2025"
2. "[problem domain] frustrations reddit"
3. "[problem domain] complaints hackernews"
4. "[existing solution] missing features"
```

Document:
- Common frustrations
- Workaround patterns users employ
- Feature requests from forums
- Unmet needs

### 4. Market Trends

Use WebSearch for:

```text
Search queries:
1. "[industry] software trends 2025"
2. "[domain] emerging technologies"
3. "[problem] AI solutions new"
```

Document:
- Growth signals
- Emerging technologies
- Investment activity in space
- Regulatory changes

### 5. Generate Research Report

Create or update `specs/research/market-analysis.md`:

```markdown
# Market Research: [FEATURE/DOMAIN]

**Research Date**: [DATE]
**Researcher**: Claude Code (market-research skill)

## Executive Summary

[2-3 sentence summary of key findings]

## Competitor Landscape

| Competitor | Positioning | Strengths | Weaknesses | Pricing |
|------------|-------------|-----------|------------|---------|
| [Name] | [Position] | [Pros] | [Cons] | [Price] |

## User Pain Points

### Top Frustrations
1. [Pain point with evidence]
2. [Pain point with evidence]
3. [Pain point with evidence]

### Unmet Needs
- [Need not addressed by current solutions]

## Market Trends

### Growing
- [Trend with source]

### Declining
- [Trend with source]

## Differentiation Opportunities

Based on research, opportunities to differentiate:
1. [Gap in market]
2. [Underserved need]
3. [Technology advantage]

## Sources

- [URL 1]
- [URL 2]
```

## Output

After completing research:
1. Report file location: `specs/research/market-analysis.md`
2. Summary of key findings
3. Recommended next step: `/speckit.concept` or `/speckit.specify`

## Integration with Spec Kit

This skill is typically invoked:
- **Before** `/speckit.concept` for greenfield projects
- **During** `/speckit.concept` Phase 0b (Discovery Mode)
- **Manually** when validating a feature idea

Results feed into:
- Concept document's "Market Research" section
- Feature specification's differentiation rationale
- Product decisions and prioritization

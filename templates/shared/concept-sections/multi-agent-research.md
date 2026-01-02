# Multi-Agent Research Protocol

> **Purpose**: Leverage AI agents to accelerate market research, competitive analysis, and validation with evidence-backed insights.

## Research Orchestration Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                 AI-AUGMENTED RESEARCH PROTOCOL                   │
│                                                                  │
│  Human Strategy → Agent Research → Human Synthesis → Decision   │
│                                                                  │
│  Cost: ~$0.50-1.00/concept | Benefit: 2-4 hours saved           │
│  ROI: 100x+ vs manual research at $50-100/hour                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Research Agent Types

### 1. Market Intelligence Agent

**Triggers**: TAM/SAM/SOM section, Market Framework, Business Model Canvas

**Research Tasks**:
| Task | Sources | Output |
|------|---------|--------|
| Market sizing | Industry reports, analyst estimates, SEC filings | TAM/SAM/SOM with citations |
| Growth trends | Market research, news, earnings calls | CAGR estimates with sources |
| Regulatory landscape | Government sites, legal databases | Compliance requirements |

**Prompt Template**:
```
Research the market for [product category] targeting [segment]:
1. Total Addressable Market (TAM) with methodology
2. Serviceable Addressable Market (SAM) for [geography/segment]
3. Key growth drivers and headwinds
4. Cite all sources with dates
```

---

### 2. Competitor Analyst Agent

**Triggers**: Blue Ocean Canvas, Porter's Five Forces, Competitive Positioning

**Research Tasks**:
| Task | Sources | Output |
|------|---------|--------|
| Feature comparison | Competitor websites, G2/Capterra reviews | Feature matrix |
| Pricing analysis | Pricing pages, case studies | Pricing tier comparison |
| Market positioning | Marketing materials, job postings | Positioning map |
| Weakness identification | Review complaints, support forums | Opportunity gaps |

**Prompt Template**:
```
Analyze competitors for [product category]:
1. List top 5 competitors by market share
2. Create feature comparison matrix
3. Identify pricing tiers and models
4. Find positioning gaps and weaknesses
5. Cite sources (prefer reviews, job postings for internal signals)
```

---

### 3. Validation Agent

**Triggers**: Hypothesis Testing, Pre-Mortem, Risk Assessment

**Research Tasks**:
| Task | Sources | Output |
|------|---------|--------|
| Similar launches | Tech news, post-mortems, case studies | Historical precedent analysis |
| Failure patterns | Startup databases, pivot stories | Common failure modes |
| Success factors | Founder interviews, growth stories | Validated success patterns |

**Prompt Template**:
```
Research validation evidence for [product hypothesis]:
1. Find 3+ similar products/launches
2. Document outcomes (success/failure/pivot)
3. Identify common success factors
4. Identify common failure patterns
5. Assess relevance to our hypothesis
```

---

## Research Execution Protocol

### Phase 0b Integration

```yaml
research_workflow:
  step_1_human:
    action: Define research questions from concept gaps
    output: Specific, answerable questions

  step_2_agents:
    parallel_execution:
      - market_intelligence: TAM/SAM/SOM, growth trends
      - competitor_analyst: Feature matrix, positioning gaps
      - validation_agent: Historical precedent
    timeout: 5 minutes per agent

  step_3_human:
    action: Synthesize agent outputs
    validation: Cross-check citations, assess confidence
    output: Evidence-backed concept sections
```

### Quality Control

| Check | Criteria | Action if Fails |
|-------|----------|-----------------|
| Citation validity | All claims have verifiable sources | Request re-research with sources |
| Recency | Data within 12 months (or justified) | Flag as potentially outdated |
| Relevance | Directly answers research question | Refine prompt and retry |
| Confidence | Multiple corroborating sources | Note low confidence, seek primary |

---

## Evidence Integration

### Source Quality Tiers

| Tier | Sources | Confidence |
|:----:|---------|:----------:|
| **1** | Primary research, SEC filings, peer-reviewed | HIGH |
| **2** | Industry reports (Gartner, IDC), major news | MEDIUM-HIGH |
| **3** | Company blogs, G2 reviews, job postings | MEDIUM |
| **4** | Social media, forums, single anecdotes | LOW |

### Citation Format
```
[Claim] — Source: [Publication], [Date], [URL/Reference]
Confidence: HIGH/MEDIUM/LOW
```

---

## Cost-Benefit Analysis

| Metric | Manual Research | AI-Augmented | Improvement |
|--------|:---------------:|:------------:|:-----------:|
| Time per concept | 4-8 hours | 30-60 minutes | **6-8x faster** |
| Cost per concept | $200-400 (at $50/hr) | $0.50-1.00 API | **200-400x cheaper** |
| Coverage breadth | Limited by time | Comprehensive | **3-5x broader** |
| Citation quality | Variable | Enforced | **Consistent** |

---

## Research Quality Checklist

- [ ] Research questions defined before agent execution
- [ ] All three agent types triggered where relevant
- [ ] Agent outputs reviewed by human for accuracy
- [ ] Citations verified (spot-check minimum 20%)
- [ ] Confidence levels assigned to each finding
- [ ] Low-confidence claims flagged for primary research
- [ ] Synthesis documented with agent attribution

---

## Integration Notes

- **Feeds into**: Market Framework (TAM/SAM/SOM), Blue Ocean Canvas (competitor gaps), Hypothesis Testing (validation evidence)
- **Depends on**: Concept scope definition (research questions)
- **Connected to**: CQS-E (evidence quality multiplier), Phase 0b workflow
- **CQS Impact**: Improves Market (+3 pts) and Strategic (+2 pts) through evidence-backed analysis

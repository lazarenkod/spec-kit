# Multi-Agent Research Framework

> **Purpose**: Orchestrate parallel AI agents for comprehensive market research, reducing research time from 4-8 hours to 30-45 minutes while improving evidence quality.

## Agent Configuration

```yaml
research_framework:
  version: "1.0"
  orchestration:
    max_parallel: 4
    timeout_minutes: 15
    retry_policy: exponential_backoff
    shared_memory: research_db

  agents:
    - role: market-intelligence-ai
      model: sonnet-4.5
      tools: [web_search, context7_docs, greptile_search]
      parallel: true
      priority: 1
      outputs:
        - tam_analysis
        - sam_analysis
        - som_analysis
        - growth_signals
        - regulatory_landscape
      prompt_template: |
        ## Task: Market Intelligence Research

        Research market opportunity for: {{USER_INPUT}}

        ### Required Outputs

        1. **TAM (Total Addressable Market)**
           - Calculate using BOTH bottom-up AND top-down methodology
           - Require ≥3 independent sources
           - Document calculation methodology
           - Flag if variance between methods >30%

        2. **SAM (Serviceable Addressable Market)**
           - Apply geographic filters
           - Apply segment filters
           - Document assumptions

        3. **SOM (Serviceable Obtainable Market)**
           - Realistic 3-year capture estimate
           - Comparable company penetration rates

        4. **Growth Signals**
           - YoY market growth rate
           - Emerging segments
           - Investment trends (VC funding in space)

        5. **Regulatory Landscape**
           - Compliance requirements
           - Upcoming regulations
           - Geographic restrictions

        ### Output Format
        Return structured JSON with evidence_links[] for each claim.

    - role: competitive-intelligence-ai
      model: sonnet-4.5
      tools: [web_search, greptile_code_reviews]
      parallel: true
      priority: 1
      outputs:
        - competitor_matrix
        - feature_gap_analysis
        - pricing_intel
        - positioning_map
      prompt_template: |
        ## Task: Competitive Intelligence Research

        Analyze competitive landscape for: {{USER_INPUT}}

        ### Required Outputs

        1. **Competitor Matrix**
           - Identify ≥5 direct competitors
           - Identify ≥3 indirect competitors
           - For each: funding, headcount, key features
           - Require ≥2 sources per competitor

        2. **Feature Gap Analysis**
           - Core features comparison grid
           - Differentiator identification
           - Table stakes vs. competitive advantages

        3. **Pricing Intelligence**
           - Pricing models (subscription, usage, freemium)
           - Price points with tiers
           - Enterprise vs. SMB positioning

        4. **Positioning Map**
           - 2x2 positioning axes
           - White space identification
           - Recommended positioning

        ### Output Format
        Return structured JSON with evidence_links[] for each claim.

    - role: persona-researcher-ai
      model: opus-4.5
      tools: [web_search, context7_docs, review_analyzer, job_posting_parser, sentiment_analyzer]
      parallel: true
      priority: 1
      data_sources:
        b2b_reviews:
          - platform: G2
            search_query: "{{PRODUCT_CATEGORY}} reviews"
            extract: [pain_points, feature_requests, ratings, quotes]
          - platform: Capterra
            search_query: "{{PRODUCT_CATEGORY}} software reviews"
            extract: [pros, cons, ratings, company_size]
          - platform: TrustRadius
            search_query: "{{PRODUCT_CATEGORY}} reviews"
            extract: [trueScore, pain_points, alternatives]
        prosumer:
          - platform: Reddit
            subreddits: ["{{RELEVANT_SUBREDDIT}}", "SaaS", "startups", "Entrepreneur"]
            extract: [complaints, recommendations, alternatives, upvote_counts]
          - platform: HackerNews
            search_query: "{{PRODUCT_CATEGORY}}"
            extract: [discussions, pain_points, tool_mentions]
        job_postings:
          - platform: LinkedIn
            search_query: "{{TARGET_ROLE}} job description 2025"
            extract: [responsibilities, tools_used, kpis, salary_range]
          - platform: Indeed
            search_query: "{{TARGET_ROLE}}"
            extract: [requirements, tech_stack, company_size]
        industry_reports:
          - sources: [Gartner, Forrester, McKinsey, IDC]
            search_query: "{{MARKET}} market size 2025"
            extract: [tam_estimates, growth_rates, buyer_segments, budget_data]
      outputs:
        - ai_synthesized_personas
        - jtbd_with_evidence
        - pain_point_ranking
        - wtp_analysis
        - evidence_citations
      prompt_template: |
        ## Task: AI-Assisted Persona Synthesis

        Synthesize data-validated personas for: {{USER_INPUT}}

        ### Phase 1: Data Collection

        1. **Review Mining** (G2, Capterra, Reddit):
           - Search: "{{PRODUCT_CATEGORY}} reviews"
           - Extract: pain points, feature requests, sentiment
           - Count frequency of each pain point (frequency = severity)
           - Capture direct quotes with source attribution [EV-XXX]

        2. **Job Posting Analysis**:
           - Search: "{{TARGET_ROLE}} job description 2025"
           - Extract: responsibilities, required tools, KPIs
           - Infer: tech comfort, decision authority, team size
           - Capture 3+ job postings per persona segment

        3. **Pricing Research**:
           - Search: competitor pricing pages
           - Extract: price points, tiers, enterprise vs SMB
           - Infer: budget authority, WTP range
           - Document: "We pay $X/mo for..." quotes from reviews

        ### Phase 2: Persona Synthesis

        For each persona (synthesize 2-4):
        - Cluster similar pain points → persona segments
        - Match job posting patterns → demographics
        - Correlate pricing tolerance → WTP
        - Validate: ≥3 evidence points per JTBD

        ### Phase 3: Evidence Documentation

        For EACH claim in persona output:
        - Assign evidence ID: [EV-XXX]
        - Record source: platform, URL, date
        - Assign tier: VS/S/M/W/N based on source credibility
        - Include direct quote or data point

        ### Required Outputs

        1. **Persona Profiles**: Name, role, demographics, context
        2. **JTBD with Evidence**: Each job linked to [EV-XXX] citations
        3. **Pain Point Ranking**: Severity × Frequency matrix
        4. **WTP Analysis**: Budget data, price sensitivity, switching costs
        5. **Evidence Citations**: Full source list with URLs, dates, excerpts

        ### Output Format
        Return structured JSON with evidence_registry[] for automatic CQS integration.

    - role: trend-analyst-ai
      model: sonnet-4.5
      tools: [web_search]
      parallel: true
      priority: 1
      outputs:
        - trend_signals
        - timing_analysis
        - risk_factors
        - opportunity_windows
      prompt_template: |
        ## Task: Trend & Timing Analysis

        Analyze market timing for: {{USER_INPUT}}

        ### Required Outputs

        1. **Trend Signals**
           - Technology trends enabling this solution
           - Behavioral trends in target market
           - Economic trends affecting demand
           - Require ≥2 sources per trend

        2. **Timing Analysis**
           - Why now? (enabling factors)
           - Why not before? (past blockers)
           - Window of opportunity estimate

        3. **Risk Factors**
           - Market risks
           - Technology risks
           - Competitive risks
           - Regulatory risks

        4. **Opportunity Windows**
           - First-mover advantage assessment
           - Platform shifts to leverage
           - Partnership opportunities

        ### Output Format
        Return structured JSON with evidence_links[] for each claim.
```

---

## Cross-Validation Rules

Ensure research quality through automated cross-validation:

### TAM Cross-Validation

```yaml
cross_validation:
  tam_calculation:
    rule: "bottom_up AND top_down required"
    variance_threshold: 0.30
    on_exceed: "FLAG_FOR_REVIEW"
    resolution: |
      If variance >30%:
      1. Document both calculations
      2. Identify source of discrepancy
      3. Use conservative estimate (lower value)
      4. Flag uncertainty in CQS
```

### Competitor Cross-Validation

```yaml
cross_validation:
  competitor_claims:
    rule: "≥2 independent sources per claim"
    source_types: ["official_website", "press_release", "third_party_report", "user_review"]
    on_single_source: "MARK_AS_UNVERIFIED"
```

### Persona Cross-Validation

```yaml
cross_validation:
  jtbd_claims:
    rule: "≥3 evidence points per JTBD"
    evidence_types: ["interview_quote", "survey_response", "behavioral_data", "support_ticket"]
    on_insufficient: "REQUEST_MORE_RESEARCH"
```

---

## Shared Memory Structure

Agents share a common research database for cross-referencing:

```yaml
shared_memory:
  research_db:
    tables:
      - name: evidence_registry
        schema:
          id: "EV-XXX"
          claim: string
          component: enum[Market, Persona, Metrics, etc.]
          source: string
          tier: enum[VS, S, M, W, N]
          date: date
          agent: string
          confidence: float

      - name: cross_references
        schema:
          claim_id: string
          related_claims: string[]
          validation_status: enum[VALIDATED, CONFLICTING, PENDING]
          notes: string

      - name: conflicts
        schema:
          id: string
          claims: string[]
          discrepancy: string
          resolution: string
          resolved_by: enum[AGENT, HUMAN]
```

---

## Agent Coordination Protocol

### Phase 1: Parallel Research (0-10 min)

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ market-intel-ai │  │ competitive-ai  │  │ persona-ai      │  │ trend-analyst   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │                    │
         ▼                    ▼                    ▼                    ▼
    [TAM/SAM/SOM]       [Competitors]        [Personas]          [Trends]
         │                    │                    │                    │
         └────────────────────┴────────────────────┴────────────────────┘
                                      │
                                      ▼
                              [Shared Memory]
```

### Phase 2: Cross-Validation (10-12 min)

```yaml
validation_sequence:
  - step: 1
    action: "Compare TAM calculations"
    agents: [market-intelligence-ai]
    check: variance < 30%

  - step: 2
    action: "Verify competitor claims"
    agents: [competitive-intelligence-ai]
    check: sources >= 2 per claim

  - step: 3
    action: "Validate JTBD evidence"
    agents: [persona-researcher-ai]
    check: evidence_points >= 3 per JTBD

  - step: 4
    action: "Cross-reference trends with market data"
    agents: [trend-analyst-ai, market-intelligence-ai]
    check: trend_claims supported by market_data
```

### Phase 3: Synthesis (12-15 min)

```yaml
synthesis:
  coordinator: orchestrator
  inputs:
    - market-intelligence-ai.outputs
    - competitive-intelligence-ai.outputs
    - persona-researcher-ai.outputs
    - trend-analyst-ai.outputs
  outputs:
    - unified_evidence_registry
    - cross_validation_report
    - concept_inputs
    - confidence_scores
```

---

## Output Artifacts

### Evidence Registry (Auto-populated)

| ID | Claim | Component | Source | Tier | Agent | Confidence |
|:--:|-------|-----------|--------|:----:|-------|:----------:|
| EV-001 | TAM = $50B | Market | Gartner 2024 | S | market-intel | 0.85 |
| EV-002 | 5 direct competitors | Competitive | Web research | M | competitive | 0.90 |
| EV-003 | DevOps primary persona | Persona | Industry reports | M | persona | 0.80 |

### Cross-Validation Report

```markdown
## Cross-Validation Summary

### TAM Calculation
- Bottom-up: $48B
- Top-down: $52B
- Variance: 8% ✅ (threshold: 30%)

### Competitor Claims
- Total claims: 25
- Verified (≥2 sources): 22 (88%)
- Unverified: 3 ⚠️

### JTBD Evidence
- Total JTBDs: 8
- Fully evidenced (≥3 points): 6 (75%)
- Needs more evidence: 2 ⚠️
```

---

## Cost Estimation

| Agent | Model | Avg Tokens | Est. Cost |
|-------|-------|:----------:|:---------:|
| market-intelligence-ai | sonnet-4.5 | 15,000 | $0.15 |
| competitive-intelligence-ai | sonnet-4.5 | 12,000 | $0.12 |
| persona-researcher-ai | opus-4.5 | 20,000 | $0.40 |
| trend-analyst-ai | sonnet-4.5 | 8,000 | $0.08 |
| **Total per concept** | | | **~$0.75-1.00** |

---

## Integration with Concept Workflow

Research agents are invoked during **Phase 0b** of `/speckit.concept`:

```yaml
concept_workflow:
  phase_0b:
    name: "Multi-Agent Research Orchestration"
    trigger: "User provides concept description"
    steps:
      - launch_agents: [market-intelligence-ai, competitive-intelligence-ai, persona-researcher-ai, trend-analyst-ai]
      - await_completion: timeout_minutes: 15
      - run_cross_validation
      - generate_evidence_registry
      - proceed_to: phase_1
```

See `concept.md` Phase 0b for full integration details.

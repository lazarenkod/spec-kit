# Multi-Agent Research Framework

> **Purpose**: Orchestrate parallel AI agents for comprehensive market research, reducing research time from 4-8 hours to 30-45 minutes while improving evidence quality.

## Agent Configuration

```yaml
research_framework:
  version: "2.0"
  orchestration:
    max_parallel: 9
    timeout_minutes: 20
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

    - role: standards-researcher-ai
      model: sonnet-4.5
      tools: [web_search, web_fetch]
      parallel: true
      priority: 10
      outputs:
        - compliance_requirements
        - regulatory_checklists
        - official_standards
        - compliance_triggers
      prompt_template: |
        ## Task: Standards & Compliance Research

        Research official standards and regulatory requirements for: {{USER_INPUT}}

        ### Phase 1: Domain Detection

        1. **Load Domain Context**:
           - Read memory/constitution.md (Domain Layer)
           - Extract domain: fintech | healthcare | e-commerce | saas | other
           - Identify applicable regulatory frameworks

        2. **Domain → Standards Mapping**:
           - Fintech → PCI-DSS, SOX, AML/KYC, GDPR (if EU)
           - Healthcare → HIPAA, FHIR, HL7, 21 CFR Part 11, GDPR (if EU)
           - E-commerce → PCI-DSS, CCPA, GDPR, consumer protection laws
           - SaaS → SOC2, ISO27001, GDPR (if EU users)

        ### Phase 2: Standards Collection

        For EACH applicable standard:

        1. **Official Documentation**:
           - WebSearch: "[STANDARD] official documentation 2025"
           - WebSearch: "[STANDARD] compliance requirements checklist"
           - WebFetch: Official standard website (PCI SSC, NIST, W3C, IETF)
           - Evidence tier: AUTHORITATIVE (official source)

        2. **Key Requirements Extraction**:
           - Critical requirements (severity: CRITICAL)
           - High-priority requirements (severity: HIGH)
           - Implementation guidance
           - Verification methods

        3. **Compliance Triggers**:
           - Keyword patterns that trigger this standard
           - Example: "store credit card" → PCI-DSS Req 3.4
           - Example: "patient data" → HIPAA Privacy Rule
           - Example: "EU users" → GDPR Art. 17

        ### Phase 3: Auto-NFR Templates

        For each requirement, generate NFR template:

        ```
        NFR-SEC-[STANDARD]-XXX: [Requirement Title] [SEVERITY]
        - Acceptance: [Specific acceptance criteria]
        - Evidence: [Standard] [Version] Req [Number] [AUTHORITATIVE]
        - Verification: [How to verify compliance]
        - Traceability: → FR-XXX (will be mapped during specify)
        ```

        ### Required Outputs

        1. **Compliance Requirements List**: All applicable standards with key requirements
        2. **Regulatory Checklists**: Implementation checklists per standard
        3. **Official Standards**: Links to official documentation
        4. **Compliance Triggers**: Keyword → Standard mapping table
        5. **Evidence Registry Entries**: [EV-XXX] with tier AUTHORITATIVE

        ### Output Format
        Return structured JSON with:
        - standards[]: {name, version, authority, requirements[], triggers[]}
        - nfr_templates[]: Ready-to-use NFR specifications
        - evidence_links[]: Official documentation URLs
        - evidence_tier: AUTHORITATIVE

    - role: academic-researcher-ai
      model: sonnet-4.5
      tools: [web_search, web_fetch]
      parallel: true
      priority: 10
      outputs:
        - best_practices
        - research_citations
        - validated_patterns
        - implementation_guides
      prompt_template: |
        ## Task: Academic Research & Best Practices

        Research peer-reviewed best practices and patterns for: {{USER_INPUT}}

        ### Phase 1: Literature Search

        1. **Academic Sources**:
           - WebSearch: "{{DOMAIN}} best practices research paper site:scholar.google.com"
           - WebSearch: "{{TECHNOLOGY}} architecture patterns site:arxiv.org"
           - WebSearch: "{{DOMAIN}} implementation guide site:ieeexplore.ieee.org"
           - WebSearch: "{{TECHNOLOGY}} design patterns ACM Digital Library"

        2. **Industry Whitepapers**:
           - WebSearch: "{{TECHNOLOGY}} whitepaper site:aws.amazon.com"
           - WebSearch: "{{DOMAIN}} best practices site:stripe.com/docs"
           - WebSearch: "{{TECHNOLOGY}} implementation guide site:cloud.google.com"
           - WebSearch: "{{DOMAIN}} patterns site:microsoft.com/azure"

        3. **Technical Standards Bodies**:
           - WebSearch: "RFC {{PROTOCOL}}"
           - WebSearch: "W3C {{STANDARD}} specification"
           - WebSearch: "OWASP {{SECURITY_TOPIC}} guidelines"

        ### Phase 2: Best Practice Extraction

        For EACH identified best practice:

        1. **Practice Documentation**:
           - Name: Clear, descriptive name
           - Category: Reliability | Security | Performance | Scalability
           - Applicability: When to use this practice
           - Evidence tier: STRONG (peer-reviewed) or MEDIUM (industry whitepaper)

        2. **Implementation Details**:
           - Description: What the practice does
           - Implementation: Code examples or architectural patterns
           - Rationale: Why this practice works (with evidence)
           - Trade-offs: Pros/Cons with specific metrics

        3. **Evidence Citations**:
           - Source: Full citation (journal, conference, vendor)
           - URL: Link to original paper/whitepaper
           - Date: Publication date for freshness tracking
           - Key findings: 1-2 sentences summarizing evidence

        ### Phase 3: Pattern Validation

        For critical patterns (security, payments, data integrity):
        - Require ≥2 independent sources
        - Cross-validate recommendations
        - Flag conflicting advice for manual review

        ### Required Outputs

        1. **Best Practices Catalog**: Structured list with evidence
        2. **Research Citations**: Full bibliography with URLs
        3. **Validated Patterns**: Patterns with ≥2 sources
        4. **Implementation Guides**: Code examples and architecture diagrams
        5. **Evidence Registry Entries**: [EV-XXX] with tier STRONG

        ### Output Format
        Return structured JSON with:
        - best_practices[]: {name, category, description, implementation, evidence[]}
        - citations[]: {source, url, date, tier}
        - patterns[]: {name, validated, sources[]}
        - evidence_tier: STRONG (papers) or MEDIUM (whitepapers)

    - role: community-intelligence-ai
      model: haiku
      tools: [web_search]
      parallel: true
      priority: 10
      outputs:
        - technical_constraints
        - known_issues
        - community_workarounds
        - real_world_gotchas
      prompt_template: |
        ## Task: Community Intelligence Mining

        Mine community knowledge for constraints, gotchas, and workarounds: {{USER_INPUT}}

        ### Phase 1: Technical Constraints Discovery

        1. **Rate Limits & Quotas**:
           - WebSearch: "{{TECHNOLOGY}} rate limit site:stackoverflow.com"
           - WebSearch: "{{API}} API quota exceeded site:github.com"
           - WebSearch: "{{SERVICE}} pricing limits site:reddit.com/r/{{SUBREDDIT}}"
           - Extract: Exact numbers, scopes, penalties, workarounds

        2. **Performance Constraints**:
           - WebSearch: "{{TECHNOLOGY}} timeout site:stackoverflow.com"
           - WebSearch: "{{DATABASE}} connection pool limits site:github.com"
           - WebSearch: "{{PLATFORM}} memory limits site:news.ycombinator.com"
           - Extract: Limits, typical values, optimization strategies

        3. **Storage & Size Limits**:
           - WebSearch: "{{SERVICE}} max file size site:stackoverflow.com"
           - WebSearch: "{{DATABASE}} row size limit site:dba.stackexchange.com"
           - Extract: Hard limits, soft limits, upgrade paths

        ### Phase 2: Known Issues & Gotchas

        1. **Common Pitfalls**:
           - WebSearch: "{{TECHNOLOGY}} gotchas site:stackoverflow.com"
           - WebSearch: "{{FRAMEWORK}} common mistakes site:dev.to"
           - WebSearch: "{{SERVICE}} issues site:github.com/{{REPO}}/issues"
           - Prioritize: By upvotes, comment count, recency

        2. **Breaking Changes**:
           - WebSearch: "{{TECHNOLOGY}} breaking changes site:github.com"
           - WebSearch: "{{API}} deprecated site:stackoverflow.com"
           - Extract: Migration guides, timeline, alternatives

        3. **Edge Cases**:
           - WebSearch: "{{TECHNOLOGY}} edge case site:stackoverflow.com"
           - WebSearch: "{{SERVICE}} unexpected behavior site:reddit.com"
           - Extract: Conditions, symptoms, workarounds

        ### Phase 3: Workaround Catalog

        For EACH constraint/issue:
        1. **Problem**: Clear description of the limitation
        2. **Workaround**: Community-validated solution
        3. **Trade-off**: Costs of workaround (complexity, performance)
        4. **Evidence**: Stack Overflow answer ID, GitHub issue #, upvote count
        5. **Tier**: MEDIUM (high upvotes) or WEAK (low engagement)

        ### Required Outputs

        1. **Technical Constraints Catalog**: Rate limits, quotas, timeouts
        2. **Known Issues List**: Gotchas with reproduction steps
        3. **Community Workarounds**: Validated solutions with evidence
        4. **Real-World Gotchas**: Edge cases from production experience
        5. **Evidence Registry Entries**: [EV-XXX] with tier MEDIUM or WEAK

        ### Output Format
        Return structured JSON with:
        - constraints[]: {type, limit, scope, penalty, workaround, evidence}
        - issues[]: {title, symptoms, root_cause, solution, upvotes}
        - gotchas[]: {scenario, problem, mitigation}
        - evidence_tier: MEDIUM (upvotes ≥50) or WEAK (upvotes <50)

    - role: glossary-builder-ai
      model: haiku
      tools: []
      parallel: true
      priority: 20
      depends_on: [market-intelligence-ai, standards-researcher-ai, academic-researcher-ai]
      outputs:
        - domain_glossary
        - term_definitions
        - usage_examples
      prompt_template: |
        ## Task: Domain Glossary Construction

        Build comprehensive domain glossary from all research outputs: {{USER_INPUT}}

        ### Phase 1: Term Extraction

        Extract domain-specific terms from:

        1. **Market Research Output**:
           - TAM/SAM/SOM terminology
           - Industry-specific jargon
           - Market segment names
           - Competitor product names
           - Example: "ACH", "SEPA", "SWIFT" in fintech

        2. **Standards Research Output**:
           - Regulatory terminology
           - Compliance acronyms
           - Standard-specific terms
           - Example: "PAN", "CVV", "3DS" in PCI-DSS

        3. **Academic Research Output**:
           - Technical terminology
           - Architecture pattern names
           - Algorithm names
           - Example: "Idempotency", "CQRS", "Event Sourcing"

        4. **Community Intelligence Output**:
           - Platform-specific terms
           - Developer slang
           - Tool abbreviations
           - Example: "K8s", "TLS", "MTLS"

        ### Phase 2: Term Categorization

        Group terms by category:
        - **Regulatory**: Compliance terms (PCI-DSS, GDPR, HIPAA)
        - **Technical**: Architecture, algorithms, patterns
        - **Business**: Market metrics, KPIs, pricing models
        - **Process**: Workflows, methodologies, frameworks
        - **Domain**: Industry-specific terminology

        ### Phase 3: Definition Enrichment

        For EACH term:
        1. **Definition**: Clear, concise explanation (1-2 sentences)
        2. **Context**: Where/when this term is used
        3. **Example**: Real-world usage example from research
        4. **Related Terms**: Links to related glossary entries
        5. **Source**: Which agent/research provided this term

        ### Required Outputs

        1. **Domain Glossary**: Structured table with all terms
        2. **Term Definitions**: Clear definitions with context
        3. **Usage Examples**: Real-world examples from research
        4. **Category Mapping**: Terms grouped by category

        ### Output Format

        Return markdown table:
        ```markdown
        | Term | Definition | Context | Example |
        |------|------------|---------|---------|
        | ACH | Automated Clearing House | US banking | "Process ACH debit" |
        ```

        Save to: memory/knowledge/glossaries/{{DOMAIN}}.md

    - role: constraints-analyzer-ai
      model: sonnet-4.5
      tools: []
      parallel: true
      priority: 20
      depends_on: [community-intelligence-ai]
      outputs:
        - constraints_profile
        - nfr_suggestions
        - limit_validations
      prompt_template: |
        ## Task: Technical Constraints Analysis

        Analyze technical constraints for NFR generation: {{USER_INPUT}}

        ### Phase 1: Constraint Extraction

        From community-intelligence-ai output, extract:

        1. **Performance Constraints**:
           - Rate limits: requests/sec, requests/min
           - Throughput limits: MB/s, records/s
           - Latency thresholds: P50, P95, P99
           - Connection limits: max connections, pool size

        2. **Reliability Constraints**:
           - Timeout values: API timeout, connection timeout
           - Retry policies: max retries, backoff strategy
           - Failure modes: error codes, recovery strategies
           - SLA guarantees: uptime %, response time

        3. **Scalability Constraints**:
           - Resource quotas: storage, compute, memory
           - Scaling limits: max instances, max size
           - Cost implications: pricing tiers, overage fees
           - Upgrade paths: how to increase limits

        ### Phase 2: Constraint Classification

        For EACH constraint:
        1. **Type**: Performance | Reliability | Scale | Cost
        2. **Hard vs Soft**: Hard (cannot exceed) or Soft (can request increase)
        3. **Scope**: Per account | Per API key | Per endpoint
        4. **Workaround**: How to handle when limit reached
        5. **Cost**: Monetary or complexity cost of workaround

        ### Phase 3: Auto-NFR Generation

        Generate NFR templates from constraints:

        ```
        NFR-PERF-{{TECH}}-XXX: Handle {{CONSTRAINT}} [PRIORITY]
        - Acceptance: {{IMPLEMENTATION_STRATEGY}}
        - Evidence: {{SOURCE}} [{{TIER}}]
        - Constraint: {{LIMIT_VALUE}} per {{SCOPE}}
        - Traceability: → FR-XXX (will be mapped)
        ```

        Examples:
        - Rate limit 100 req/sec → NFR-PERF-STRIPE-001: Exponential backoff
        - Webhook timeout 30s → NFR-PERF-STRIPE-002: Async processing
        - File size 10MB → NFR-PERF-AWS-001: Chunked upload

        ### Phase 4: NFR Validation Rules

        Create validation rules for plan phase:
        ```yaml
        validation:
          - rule: "IF NFR requires {{X}} req/sec AND constraint = {{Y}} req/sec"
            action: "FLAG if X > Y"
            suggestion: "Use batching OR rate limiting queue"
        ```

        ### Required Outputs

        1. **Constraints Profile**: Complete catalog of limits
        2. **NFR Suggestions**: Auto-generated NFR templates
        3. **Limit Validations**: Rules for plan phase validation
        4. **Workaround Strategies**: For each constraint

        ### Output Format

        Return structured JSON with:
        - constraints[]: {type, limit, scope, hard_soft, workaround}
        - nfr_templates[]: Ready-to-use NFR specifications
        - validation_rules[]: For plan.md Phase 0.2

        Save to: memory/knowledge/constraints/platforms/{{TECH}}.md
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

### Wave 1: Parallel Research (0-12 min, priority 10)

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ market-     │  │competitive- │  │ persona-    │  │ trend-      │
│ intel-ai    │  │ ai          │  │ ai          │  │ analyst-ai  │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │                │
       ▼                ▼                ▼                ▼
  [TAM/SAM/SOM]   [Competitors]    [Personas]       [Trends]

┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ standards-  │  │ academic-   │  │ community-  │
│ researcher  │  │ researcher  │  │ intelligence│
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       ▼                ▼                ▼
  [Compliance]     [Best Practices]  [Constraints]
       │                │                │
       └────────────────┴────────────────┴────────────────┘
                        │
                        ▼
                [Shared Memory]
```

### Wave 2: Synthesis & Analysis (12-18 min, priority 20)

```
              [Shared Memory]
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
┌─────────────┐            ┌─────────────┐
│ glossary-   │            │ constraints-│
│ builder-ai  │            │ analyzer-ai │
└──────┬──────┘            └──────┬──────┘
       │                           │
       ▼                           ▼
  [Glossary]               [NFR Templates]
       │                           │
       └─────────────┬─────────────┘
                     ▼
            [Knowledge Base]
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
| standards-researcher-ai | sonnet-4.5 | 12,000 | $0.12 |
| academic-researcher-ai | sonnet-4.5 | 10,000 | $0.10 |
| community-intelligence-ai | haiku | 8,000 | $0.02 |
| glossary-builder-ai | haiku | 6,000 | $0.015 |
| constraints-analyzer-ai | sonnet-4.5 | 10,000 | $0.10 |
| **Total per concept** | | | **~$1.50-1.75** |

---

## Integration with Concept Workflow

Research agents are invoked during **Phase 0b** of `/speckit.concept`:

```yaml
concept_workflow:
  phase_0b:
    name: "Multi-Agent Research Orchestration (9 agents)"
    trigger: "User provides concept description"

    wave_1_research:
      parallel: true
      priority: 10
      timeout_minutes: 12
      agents:
        - market-intelligence-ai
        - competitive-intelligence-ai
        - persona-researcher-ai
        - trend-analyst-ai
        - standards-researcher-ai
        - academic-researcher-ai
        - community-intelligence-ai
      outputs:
        - Shared research_db populated
        - Evidence registry with AUTHORITATIVE tier

    wave_2_synthesis:
      parallel: true
      priority: 20
      timeout_minutes: 6
      depends_on: wave_1_research
      agents:
        - glossary-builder-ai
        - constraints-analyzer-ai
      outputs:
        - memory/knowledge/glossaries/{{DOMAIN}}.md
        - memory/knowledge/constraints/platforms/{{TECH}}.md

    phase_0b_2_knowledge_base:
      name: "Knowledge Base Population"
      depends_on: wave_2_synthesis
      timeout_minutes: 2
      steps:
        - save_glossary_to_knowledge_base
        - save_best_practices_catalog
        - save_standards_compliance_docs
        - save_constraints_profiles
        - proceed_to: phase_1
```

See `concept.md` Phase 0b for full integration details.

---

## Knowledge Base Outputs

After Phase 0b completion, the following files are auto-generated:

| File | Content | Evidence Tier | Source Agent |
|------|---------|:-------------:|:------------:|
| `memory/knowledge/glossaries/{{DOMAIN}}.md` | Domain terminology with definitions | N/A | glossary-builder-ai |
| `memory/knowledge/best-practices/by-domain/{{DOMAIN}}.md` | Best practices with evidence citations | STRONG | academic-researcher-ai |
| `memory/knowledge/standards/compliance/{{STANDARD}}.md` | Compliance requirements and checklists | AUTHORITATIVE | standards-researcher-ai |
| `memory/knowledge/constraints/platforms/{{TECH}}.md` | Technical constraints with NFR templates | MEDIUM | constraints-analyzer-ai |

These knowledge base files are then automatically loaded during `/speckit.specify` and `/speckit.plan` phases for domain-aware specification and planning.

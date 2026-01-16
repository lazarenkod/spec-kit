---
description: Capture complete service concept before detailed specification. Creates hierarchical feature breakdown with full traceability. Use BEFORE /speckit.specify for large projects (50+ requirements).
handoffs:
  - label: Create Specification
    agent: speckit.specify
    prompt: Generate detailed specification from concept for stories
    send: true
  - label: Validate Concept
    agent: speckit.analyze
    prompt: Check concept completeness and consistency
plan_mode:
  enabled: auto

  # Default depth levels by complexity tier
  # Concept benefits from deep exploration even for SIMPLE features
  depth_defaults:
    TRIVIAL: 0   # Standard
    SIMPLE: 1    # Lite (exploration even for simple concepts)
    MODERATE: 2  # Moderate
    COMPLEX: 3   # Full depth

  # Depth level definitions (same as other commands)
  depth_levels:
    0:
      name: "Standard"
      exploration: false
      review_passes: []
    1:
      name: "Lite"
      exploration:
        agents: [pattern-researcher, constraint-mapper]
        budget_s: 90
      review_passes: []
    2:
      name: "Moderate"
      exploration:
        agents: [pattern-researcher, alternative-analyzer, constraint-mapper, best-practice-synthesizer]
        budget_s: 180
      review_passes: [constitution_alignment]
      budget_s: 210
    3:
      name: "Full"
      exploration:
        agents: [pattern-researcher, alternative-analyzer, constraint-mapper, best-practice-synthesizer]
        budget_s: 180
      review_passes: [constitution_alignment, completeness_check, edge_case_detection, testability_audit]
      budget_s: 300

  keyword_triggers:
    - distributed
    - multi-service
    - migration
    - security-critical
    - real-time
    - high-availability
    - microservices
    - event-driven
    - data-intensive

  flags:
    depth: "--depth-level <0-3>"
    enable: "--plan-mode"
    disable: "--no-plan-mode"
    max_model: "--max-model <opus|sonnet|haiku>"
claude_code:
  model: opus
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: ultrathink  # Changed for autonomous concept generation with deep strategic thinking
    tiers:
      free:
        thinking_budget: 8000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 16000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 32000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
      ultrathink:  # NEW TIER for world-class strategic concepts
        thinking_budget: 120000  # 4× deeper reasoning for strategic analysis
        max_parallel: 4          # Lower parallelism for deeper serial reasoning
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 3.5
  cache_control:
    system_prompt: ephemeral
    constitution: ephemeral
    templates: ephemeral
    ttl: session
  semantic_cache:
    enabled: true
    encoder: all-MiniLM-L6-v2
    similarity_threshold: 0.95
    cache_scope: session
    cacheable_fields: [user_input, feature_description]
    ttl: 3600
  cache_hierarchy: full
  plan_mode_trigger: true
  orchestration:
    max_parallel: 8
    wave_overlap:
      enabled: true
      threshold: 0.65
  subagents:
    # Wave 1: Discovery & Research (parallel)
    - role: market-researcher
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      role_description: "Strategic Market Analyst & Co-Founder"
      # OPTIMIZATION v0.5.0: Prompt extracted to templates/shared/agent-prompt-template.md
      # Load market-researcher section from agent prompt template
      prompt_ref: market-researcher
    - role: competitive-analyst
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      role_description: "Strategic Competitive Intelligence Analyst"
      # OPTIMIZATION v0.5.0: Prompt extracted to templates/shared/agent-prompt-template.md
      prompt_ref: competitive-analyst
    - role: persona-designer
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      role_description: "Strategic Persona & JTBD Researcher"
      # OPTIMIZATION v0.5.0: Prompt extracted to templates/shared/agent-prompt-template.md
      prompt_ref: persona-designer

    # NEW: Domain-specific research agents
    - role: standards-researcher
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      # OPTIMIZATION v0.5.0: Prompt extracted to templates/shared/agent-prompt-template.md
      prompt_ref: standards-researcher

    - role: academic-researcher
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      # OPTIMIZATION v0.5.0: Prompt extracted to templates/shared/agent-prompt-template.md
      prompt_ref: academic-researcher

    - role: community-intelligence
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        ## Context
        Project: {{PROJECT_ROOT}}
        User Input: {{ARGUMENTS}}

        ## Task
        Mine community knowledge for gotchas, constraints, and workarounds:
        1. Search Stack Overflow for common issues
        2. Search GitHub discussions/issues for limitations
        3. Search Reddit/HackerNews for real-world experiences

        Use WebSearch queries:
        - "{TECHNOLOGY} rate limits stack overflow"
        - "{TECHNOLOGY} common issues github"
        - "{TECHNOLOGY} vs alternatives reddit"
        - "{TECHNOLOGY} production gotchas"

        ## Output
        - Technical constraints catalog (rate limits, quotas, API limits)
        - Known issues and workarounds
        - Evidence tier: MEDIUM

    # Wave 2: Synthesis (after research)
    - role: jtbd-analyst
      role_group: ANALYSIS
      parallel: true
      depends_on: [persona-designer]
      priority: 20
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      prompt: |
        ## Context
        Personas: (from persona-designer)

        ## Task
        Analyze Jobs-to-Be-Done:
        1. Map functional jobs for each persona
        2. Identify emotional and social jobs
        3. Define success criteria per job
        4. Prioritize by frequency and importance

        ## Output
        - JTBD framework per persona
        - Job prioritization matrix
        - Success metrics per job
    - role: value-prop-designer
      role_group: ANALYSIS
      parallel: true
      depends_on: [market-researcher, competitive-analyst]
      priority: 20
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      prompt: |
        ## Context
        Market Research: (from market-researcher)
        Competitive Analysis: (from competitive-analyst)
        User Input: {{ARGUMENTS}}

        ## Task
        Design value proposition:
        1. Articulate unique value proposition
        2. Define key differentiators vs competition
        3. Create positioning statement
        4. Develop messaging hierarchy

        ## Output
        - Value proposition canvas
        - Positioning statement
        - Key messaging points

    # NEW: Domain knowledge extraction agents
    - role: glossary-builder
      role_group: ANALYSIS
      parallel: true
      depends_on: [market-researcher, standards-researcher, academic-researcher]
      priority: 20
      model_override: haiku
      prompt: |
        ## Context
        Market Research: (from market-researcher)
        Standards Research: (from standards-researcher)
        Academic Research: (from academic-researcher)

        ## Task
        Build domain glossary from all research outputs:
        1. Extract domain-specific terms from all research
        2. For each term: Definition | Context | Example usage
        3. Categorize: Regulatory, Technical, Business, Process

        ## Output Format
        Generate memory/knowledge/glossaries/{DOMAIN}.md:
        | Term | Definition | Context | Example |
        |------|------------|---------|---------|
        | ACH  | Automated Clearing House | US banking | "Process ACH debit" |

        ## Output
        - Domain glossary markdown file
        - Terms categorized by type
        - Evidence tier: AUTHORITATIVE (for regulatory), STRONG (for technical)

    - role: constraints-analyzer
      role_group: ANALYSIS
      parallel: true
      depends_on: [community-intelligence]
      priority: 20
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      prompt: |
        ## Context
        Community Intelligence: (from community-intelligence)

        ## Task
        Document technical constraints for NFR generation:
        1. Analyze community intelligence for rate limits, quotas, timeouts
        2. Categorize by constraint type (Performance, Reliability, Scale)
        3. Include workarounds and mitigation strategies

        ## Output Format
        Generate memory/knowledge/constraints/platforms/{TECH}.md:
        | Operation | Limit | Scope | Penalty | Workaround |
        |-----------|-------|-------|---------|------------|
        | API calls | 100/sec | Account | 429 | Exponential backoff |

        Auto-generate NFR suggestions:
        - Rate limit → NFR-PERF-{TECH}-001
        - Timeout → NFR-REL-{TECH}-001
        - Quota → NFR-SCALE-{TECH}-001

        ## Output
        - Technical constraints profile
        - NFR suggestions with traceability
        - Evidence tier: MEDIUM (community), AUTHORITATIVE (vendor docs)

    # Wave 3: Validation Framework (after synthesis)
    - role: metrics-designer
      role_group: VALIDATION
      parallel: true
      depends_on: [value-prop-designer]
      priority: 30
      model_override: sonnet
      role_description: "Strategic Metrics Architect"
      prompt: |
        ## Context
        Value Proposition: (from value-prop-designer)
        JTBD Analysis: (from jtbd-analyst)
        Three Foundational Pillars: (if available)

        ## Your Role
        You are a Strategic Metrics Architect designing outcome-based measurement systems that prove business value.

        ## Task
        Design success metrics framework that answers: "How do we measure strategic success, not just product usage?"

        **Critical Principle**: Focus on OUTCOMES (results, impact), NOT OUTPUTS (activity, features shipped).

        1. **North Star Metric Selection**:
           - Choose metric that bridges user value AND business value
           - Must be influenced by all Three Pillars
           - Example: "Hours saved per executive per week" (outcome) NOT "Features used per session" (output)
           - Validate: Can this be gamed without delivering real value? How?

        2. **Metric Categorization** (Strategic/Product/Business):
           - **Strategic Metrics**: Measure competitive position, market share, pillar strength
             Example: "Market share in beachhead segment", "NPS vs competitors"
           - **Product Metrics**: Measure engagement, value delivery, retention
             Example: "Weekly active executives", "Feature adoption rate"
           - **Business Metrics**: Measure unit economics, revenue, growth
             Example: "MRR growth rate", "CAC/LTV ratio", "Net revenue retention"

        3. **Outcome vs. Output Metrics**:
           - PREFER outcome-based: "Hours saved per executive per week" (measures impact)
           - AVOID output metrics: "Features used per session" (measures activity, not value)
           - Validate: Does metric tie to willingness-to-pay?

        ## Output
        - North Star metric with user/business value bridge
        - SMART-validated metrics (Specific, Measurable, Achievable, Relevant, Time-bound)
        - Metric categorization (Strategic/Product/Business)
        - Outcome-focused metrics (not output metrics)
    - role: risk-assessor
      role_group: VALIDATION
      parallel: true
      depends_on: [jtbd-analyst, value-prop-designer]
      priority: 30
      model_override: sonnet
      prompt: |
        ## Context
        Value Proposition: (from value-prop-designer)
        Market Research: (from market-researcher)
        JTBD Analysis: (from jtbd-analyst)

        ## Task
        Assess risks and mitigation:
        1. Identify market, technical, and execution risks
        2. Score by impact and likelihood (1-5)
        3. Propose mitigation strategies
        4. Define pivot criteria/triggers

        ## Output
        - Risk matrix (impact vs likelihood)
        - Mitigation strategies
        - Pivot trigger definitions

    # Wave 4: Technical Discovery (after validation)
    - role: technical-hint-generator
      role_group: TECHNICAL
      parallel: true
      depends_on: [value-prop-designer]
      priority: 40
      model_override: sonnet
      role_description: "Technology Architecture Strategist"
      prompt: |
        ## Context
        Value Proposition: (from value-prop-designer)
        Three Foundational Pillars: (if available from strategic-synthesis-ai)
        Project Type: {{PROJECT_TYPE}}

        ## Your Role
        You are a Technology Architecture Strategist translating business strategy into technical architecture principles.

        ## Task
        Generate strategic technical discovery by answering:
        "What technology decisions enable competitive advantage and long-term defensibility?"

        1. **Strategic Architecture Principles** (not just tech stack):
           - What architectural decisions create moats? (data network effects, platform extensibility, API-first)
           - What enables fast iteration? (microservices, feature flags, experimentation framework)
           - What enables scale? (horizontal scaling, caching strategy, CDN)
           - What technical choices differentiate us? (AI/ML capabilities, real-time processing, offline-first)

        2. **Core Domain Entities** (business-focused):
           - Identify entities that represent business value, not just technical objects
           - Link to Three Foundational Pillars: Which entities enable which pillar?
           - Example: "Executive" entity (not "User") because we're CEO-focused
           - Example: "Strategic Decision" entity (enables decision intelligence pillar)

        3. **API Surface & Integration Strategy**:
           - What business capabilities does API expose? (not just CRUD endpoints)
           - What strategic integrations create network effects? (calendar, email, CRM = data moat)
           - What integration strategy enables ecosystem? (webhook platform, plugin architecture)

        4. **Technical Risk Areas** (business impact framing):
           - NOT: "Database scaling risk"
           - YES: "Data growth >1M records/month could increase infrastructure cost 3x by Month 12, impacting unit economics"
           - Link technical risks to business metrics (CAC, margins, time-to-value)

        ## Output Format
        Generate content for templates/shared/concept-sections/technical-hints.md:

        ```markdown
        # Technology Architecture Strategy

        ## Strategic Architecture Principles
        1. **[Principle 1]** — [Why this creates competitive advantage]
           - Business Impact: [Faster iteration / Lower CAC / Higher retention]
           - Moat Type: [Data / Platform / Speed]
           - Example: [Concrete technical decision]

        ## Core Domain Entities (Business-Focused)
        | Entity | Business Purpose | Pillar Enabled | Strategic Value |
        |--------|------------------|----------------|-----------------|
        | [Entity 1] | [What business capability] | [Pillar 1] | [Data moat / Network effect] |

        ## API Strategy & Integration Points
        **Strategic Integrations** (create network effects):
        - [Integration 1]: [Business capability enabled] → [Moat created]

        **API Surface** (business capabilities):
        - [Capability 1]: [Business outcome] (not just "GET /users")

        ## Technical Risk Assessment (Business Impact)
        | Risk | Business Impact | Probability | Mitigation |
        |------|----------------|-------------|------------|
        | [Technical risk] | [Impact on CAC/LTV/TTM] | H/M/L | [Strategy] |
        ```

        ## Output
        - Architecture principles linked to competitive advantage
        - Domain entities mapped to business pillars
        - API strategy focused on business capabilities
        - Technical risks framed by business impact

    # Wave 5: Strategic Synthesis (after validation & technical discovery)
    - role: strategic-synthesis-ai
      role_group: SYNTHESIS
      parallel: false
      depends_on: [market-researcher, competitive-analyst, persona-designer, jtbd-analyst, value-prop-designer]
      priority: 50
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      role_description: "Strategic Synthesis Architect"
      prompt: |
        ## Context
        Market Research: (from market-researcher)
        Competitive Analysis: (from competitive-analyst)
        Persona & JTBD: (from persona-designer, jtbd-analyst)
        Value Proposition: (from value-prop-designer)
        Problem Analysis: (from earlier research)

        ## Your Role
        You are a Strategic Synthesis Architect synthesizing research findings into Three Foundational Pillars that form the strategic core of this product.

        ## Task
        Generate Three Foundational Pillars by:

        1. **Analyze Research Findings**:
           - Review top 10 pain points from Problem Analysis
           - Identify market gaps from Competitive Analysis
           - Map JTBD to unmet needs
           - Extract strategic themes from all research

        2. **Identify Top 3 Strategic Themes** that:
           - Address highest-severity pain points (Impact Score ≥ 15/20)
           - Leverage identified market gaps and white space
           - Create defensible competitive advantage
           - Enable sustainable business model

        3. **For Each Pillar, Define**:
           - **Name**: Memorable, strategic (3-4 words) - NOT feature names
           - **Problem Addressed**: Link to specific pain points (use PP-XXX IDs)
           - **Solution Approach**: How we uniquely solve it (capabilities, not features)
           - **Proof Points**: 2+ evidence-backed claims (STRONG+ tier required)
           - **Differentiation**: Why we win, why competitors lose, time to imitation
           - **Strategic Value**: Market positioning, moat type, business impact

        4. **Ensure Pillar Quality**:
           - Pillars are interdependent (synergy matrix)
           - Each addresses ≥2 pain points
           - Each has ≥2 proof points with evidence citations [EV-XXX]
           - Differentiation is specific to competitor weaknesses
           - Time to imitation justified (6-36 months realistic range)

        ## Output Format
        Generate content for templates/shared/concept-sections/three-pillars.md:

        ```markdown
        # Three Foundational Pillars

        ## Pillar 1: [Strategic Name]

        ### Problem Addressed
        - Primary: [Pain Point Name] (PP-001) - Impact: [X]/20
        - Secondary: [Pain Point Name] (PP-003) - Impact: [X]/20

        ### Solution Approach
        [75-125 words explaining unique capability, not feature list]

        **Core Capabilities**:
        1. [Capability 1] - [Business outcome enabled]
        2. [Capability 2] - [Business outcome enabled]
        3. [Capability 3] - [Business outcome enabled]

        ### Proof Points
        | Claim | Evidence | Source | Tier |
        |-------|----------|--------|------|
        | [Measurable claim] | [Data/study] | [EV-001] | STRONG |
        | [Measurable claim] | [Data/study] | [EV-002] | STRONG |

        ### Differentiation Analysis
        **Why We Win**:
        1. [Unique advantage] - [Barrier to entry]
        2. [Unique advantage] - [Barrier to entry]
        3. [Unique advantage] - [Barrier to entry]

        **Why Competitors Lose**:
        | Competitor Type | Why They Can't/Won't | Barrier |
        |----------------|----------------------|---------|
        | [Incumbent X] | [Structural limitation] | [Business model conflict] |
        | [Startup Y] | [Resource constraint] | [Requires 2+ years R&D] |

        **Time to Imitation**: [12-24] months — [Justification: complexity, moat type, resource requirements]

        ### Strategic Value
        - **Market Positioning**: [How this positions us in market]
        - **Moat Type**: [Network effects / Data / Brand / Tech / Switching costs]
        - **Business Impact**: [Revenue / Retention / Market share impact]

        [Repeat for Pillar 2 and Pillar 3]

        ## Pillar Synergy Matrix
        | Pillar Pair | Synergy | Value Created |
        |-------------|---------|---------------|
        | P1 + P2 | [How they reinforce] | [1+1=3 effect] |
        | P1 + P3 | [How they reinforce] | [Compounding value] |
        | P2 + P3 | [How they reinforce] | [Ecosystem effect] |

        ## Pillar-to-Pain Point Mapping
        | Pain Point | Pillar 1 | Pillar 2 | Pillar 3 | Coverage |
        |------------|:--------:|:--------:|:--------:|:--------:|
        | PP-001 | ● | ○ | | Primary |
        | PP-002 | ○ | ● | | Primary |
        | PP-003 | | ● | ● | Dual |

        Legend: ● Primary solution, ○ Secondary contribution
        ```

        ## Quality Checklist
        - [ ] Each pillar has memorable 3-4 word name (strategic, not feature-focused)
        - [ ] Each addresses ≥2 pain points with explicit PP-XXX references
        - [ ] Each has ≥2 proof points with STRONG+ evidence tier
        - [ ] Differentiation specific to named competitors
        - [ ] Time to imitation justified (not generic "hard to copy")
        - [ ] Strategic value explains market positioning and moat type
        - [ ] Synergy matrix shows 1+1=3 effects

        ## Output
        - Three Foundational Pillars section content
        - Pillar-to-pain-point mapping with traceability
        - Evidence citations (EV-XXX) for all proof points
        - Synergy analysis showing interdependencies

    # Wave 6: Strategic Recommendations (after strategic synthesis)
    - role: strategic-recommendations-ai
      role_group: SYNTHESIS
      parallel: false
      depends_on: [strategic-synthesis-ai, risk-assessor, metrics-designer]
      priority: 60
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      role_description: "Strategic Roadmap Architect"
      prompt: |
        ## Context
        Three Foundational Pillars: (from strategic-synthesis-ai)
        Risk Assessment: (from risk-assessor)
        Metrics Framework: (from metrics-designer)
        Differentiation Strategy: (from value-prop-designer)
        Market Analysis: (from market-researcher)

        ## Your Role
        You are a Strategic Roadmap Architect creating actionable, phase-based execution plan that sequences pillar development, manages risks, and defines critical success factors.

        ## Task
        Generate Phase-Based Strategic Recommendations by:

        1. **Determine Timeline & Phases**:
           - Parse {{TIMELINE_TARGET}} from user input or infer from market complexity
           - Divide into 3 phases: Foundation (20%), Scale (40%), Dominate (40%)
           - Adjust if regulated industry (longer) or consumer product (shorter)
           - Default: B2B SaaS 36 months (Foundation 0-6mo, Scale 7-18mo, Dominate 19-36mo)

        2. **Phase 1 Actions** (Foundation - Months 0-6):
           - **Build MVP**: Select features addressing top 3 pain points from Problem Analysis
           - **Establish Pillar Foundations**: Prove core hypothesis for Pillar 1 (most critical)
           - **Prove Unit Economics**: First 10-100 customers, validate CAC/LTV
           - **Establish Metrics Baseline**: Set targets for North Star metric
           - Each action needs: Description (50-75 words), 3-4 sub-actions, measurable target

        3. **Phase 2 Actions** (Scale - Months 7-18):
           - **Expand Capabilities**: Develop Pillars 2-3, add features from roadmap Waves 2-3
           - **Build Distribution**: Scale GTM from Market Framework
           - **Develop Network Effects**: Implement differentiators with network moat
           - **Achieve PMF at Scale**: 100-500 customers, positive unit economics, repeatable GTM

        4. **Phase 3 Actions** (Dominate - Months 19-36):
           - **Market Leadership**: Category definition, analyst recognition (Gartner/Forrester)
           - **Vertical Expansion**: Industry-specific versions
           - **Enterprise Expansion**: Upmarket motion with enterprise features
           - **Ecosystem Development**: Plugin platform, partnerships, community

        5. **Critical Success Factors** (5-7 CSFs):
           - Extract from Three Pillars (what MUST work for pillars to succeed)
           - Extract from Differentiation Strategy (what enables differentiators)
           - Add execution factors (speed, focus, trust, quality)
           - Each CSF needs: Brief explanation + "How to Ensure" (actions/metrics)

        6. **Risks & Mitigations** (≥5 risks):
           - Competitive risks: From Competitive Analysis (Microsoft/Google enters market)
           - Execution risks: From Features and Technical Hints (complexity, timeline)
           - Market risks: From Market Framework (timing, adoption rate, regulation)
           - Financial risks: From Business Model (CAC too high, retention issues)
           - Each risk needs: Likelihood (H/M/L), Impact (H/M/L), Mitigation, Owner

        ## Output Format
        Generate content for templates/shared/concept-sections/strategic-recommendations.md:

        ```markdown
        # Strategic Recommendations

        ## Phase Structure Overview
        | Phase | Duration | Focus | Success Criteria |
        |-------|:--------:|-------|------------------|
        | **Phase 1: Foundation** | Months 0-6 | Build MVP, prove unit economics, establish PMF signals | 10-100 paying customers, core metrics validated |
        | **Phase 2: Scale** | Months 7-18 | Scale acquisition, expand capabilities, build network effects | 100-500 customers, positive unit economics, repeatable GTM |
        | **Phase 3: Dominate** | Months 19-36 | Market leadership, category definition, ecosystem development | 500-5,000 customers, category leader, defensible moat |

        ## Phase 1: Foundation (Months 0-6)
        > **Objective**: Validate core hypothesis, build MVP, prove first customers will pay, establish baseline metrics

        ### Key Actions
        #### 1. [Action 1 Name] (e.g., "Build MVP with Laser Focus")
        **Description** (50-75 words):
        [WHAT to build and WHY this is the priority. Link to Three Pillars: "Focus on Pillar 1 [Name] first because..."]

        **Sub-Actions**:
        - [Sub-action 1]: [Specific deliverable with milestone]
        - [Sub-action 2]: [Specific deliverable with milestone]
        - [Sub-action 3]: [Specific deliverable with milestone]
        - [Sub-action 4]: [Specific deliverable with milestone] (optional)

        **Target**: [Measurable outcome with timeline - e.g., "20 design partners providing weekly feedback; 90% report 'valuable' by Month 3"]

        [Repeat for Actions 2-4]

        ### Phase 1 Success Criteria
        **Quantitative**:
        - [Metric 1]: [Target value] (e.g., "First 10 paying customers at $X/month")
        - [Metric 2]: [Target value] (e.g., "NPS ≥ 50")
        - [Metric 3]: [Target value] (e.g., "CAC < $800, LTV > $5,000")
        - [Metric 4]: [Target value] (e.g., "Time saved: 5+ hours/week average")

        **Qualitative**:
        - [Criterion 1]: [Description] (e.g., "Strong PMF signals: customers refer others unprompted")
        - [Criterion 2]: [Description] (e.g., "Clear value prop: customers explain in 1 sentence")

        [Repeat Phase 2 and Phase 3 with same structure]

        ## Critical Success Factors
        **To win, we must**:

        1. **[CSF 1 Name]** — [50-75 word explanation of why this is critical and what happens if we fail]

           **How to Ensure**: [Specific actions or metrics to track - e.g., "Automated onboarding flow with personalized insights in <15 min; track 'aha moment' metric weekly; iterate until 70%+ threshold met"]

        [Repeat for CSFs 2-7]

        ## Risks & Mitigations
        | Risk | Likelihood | Impact | Mitigation | Owner |
        |------|:----------:|:------:|------------|:-----:|
        | [Risk 1] | H/M/L | H/M/L | [Specific mitigation actions] | [Role] |
        | [Risk 2] | H/M/L | H/M/L | [Mitigation actions] | [Role] |
        | [Risk 3] | H/M/L | H/M/L | [Mitigation actions] | [Role] |
        | [Risk 4] | H/M/L | H/M/L | [Mitigation actions] | [Role] |
        | [Risk 5] | H/M/L | H/M/L | [Mitigation actions] | [Role] |

        ### Contingency Plans
        For HIGH likelihood + HIGH impact risks, define:

        **Risk**: [Description of high-priority risk]
        **Trigger**: [Specific metric/signal that activates contingency - e.g., "Microsoft announces CEO-specific product at Ignite conference (Nov 2026)"]
        **Contingency**: [Alternative plan if mitigation fails - numbered steps]
        ```

        ## Quality Checklist
        - [ ] 3 phases defined with realistic timelines
        - [ ] 3-5 actions per phase with measurable targets
        - [ ] Success criteria: ≥4 quantitative + ≥2 qualitative per phase
        - [ ] 5-7 CSFs with "How to Ensure" guidance
        - [ ] ≥5 risks with likelihood/impact/mitigation/owner
        - [ ] Contingency plans for HIGH-HIGH risks
        - [ ] Timeline realism validated against market benchmarks
        - [ ] Actions explicitly reference Three Pillars

        ## Output
        - Strategic Recommendations section content
        - Phase timeline with concrete milestones
        - CSF list with actionable guidance
        - Risk matrix with specific mitigations
        - Contingency plans for critical risks

    # Wave 7: Quality Validation (final)
    - role: concept-quality-scorer
      role_group: REVIEW
      parallel: false
      depends_on: [metrics-designer, risk-assessor, technical-hint-generator, strategic-synthesis-ai, strategic-recommendations-ai]
      priority: 70
      model_override: opus
      thinking_budget: 120000
      reasoning_mode: extended
      role_description: "Concept Quality Auditor"
      prompt: |
        ## Context
        All Concept Artifacts: (from previous agents)
        - Problem Analysis: Top 10 pain points
        - Market Framework: TAM/SAM/SOM, segmentation
        - Three Foundational Pillars: (from strategic-synthesis-ai)
        - Differentiation Strategy: 5 breakthrough differentiators
        - Strategic Recommendations: Phase-based roadmap
        - Metrics Framework: North Star, categorization
        - Risk Assessment: Risk matrix

        ## Your Role
        You are a Concept Quality Auditor applying CQS Formula v0.7.0 to validate strategic readiness.

        ## Task
        Calculate Concept Quality Score (CQS-E) using formula v0.7.0.

        **OPTIMIZATION v0.5.0**: CQS formula extracted to templates/shared/cqs-formula.md

        **Formula Reference** (11 Components, 0-120 scale):
        - See templates/shared/cqs-formula.md for complete formula with component definitions
        - Market (16%), Persona (12%), Metrics (12%), Features (12%), Risk (8%), Technical (8%)
        - Strategic_Clarity (8%), Strategic_Depth (10%), Validation (5%), Transparency (5%), Quality_Intent (4%)

        **Focus on Strategic Depth Component** (100 pts max, 10% weight):
        1. **Three Foundational Pillars** (25 pts):
           - Are 3 pillars defined with memorable names? (5 pts)
           - Do they address ≥2 pain points each with PP-XXX links? (5 pts)
           - Do they have ≥2 proof points each with STRONG+ evidence? (10 pts)
           - Is differentiation specific to competitors? (5 pts)

        2. **Five Breakthrough Differentiators** (25 pts):
           - Are 5 differentiators defined? (5 pts)
           - Do they have market reality + specific tactics? (10 pts)
           - Are barriers to entry documented? (5 pts)
           - Is time to imitation justified? (5 pts)

        3. **Phase-Based Strategic Recommendations** (25 pts):
           - Are 3 phases defined (Foundation/Scale/Dominate)? (5 pts)
           - Do phases have 3-5 actions each with measurable targets? (10 pts)
           - Are success criteria quantitative (≥4) + qualitative (≥2)? (5 pts)
           - Are actions linked to Three Pillars? (5 pts)

        4. **Critical Success Factors** (15 pts):
           - Are ≥5 CSFs documented? (5 pts)
           - Do CSFs have "How to Ensure" guidance? (5 pts)
           - Are CSFs derived from Pillars/Differentiation? (5 pts)

        5. **Risk/Mitigation Matrix** (10 pts):
           - Are ≥5 risks documented? (3 pts)
           - Do risks have likelihood/impact/mitigation/owner? (4 pts)
           - Are contingency plans defined for HIGH-HIGH risks? (3 pts)

        **Evidence Tier Requirements**:
        - Pillars proof points: STRONG+ required
        - Differentiators: MEDIUM+ required
        - Strategic Recommendations: MEDIUM+ required

        **Quality Gates**:
        - ≥80: READY (Green) — Proceed to specification
        - 60-79: CAUTION (Yellow) — Address gaps, then proceed
        - <60: NOT READY (Red) — Substantial rework required

        ## Output
        Generate content for templates/shared/concept-sections/cqs-score.md:
        - CQS-E score with 11-component breakdown
        - Strategic Depth score (0-100) with subscores
        - Evidence multiplier calculation
        - Quality gate verdict with color coding
        - Improvement recommendations (prioritized by impact)
        - Missing evidence list (EV-XXX citations needed)
skills:
  - name: market-research
    trigger: "Phase 0b: Market & User Research"
    usage: "Read templates/skills/market-research.md for comprehensive competitor and market analysis"
  - name: ux-audit
    trigger: "When validating concept for UX quality"
    usage: "Read templates/skills/ux-audit.md to validate UXQ compliance before specification"
scripts:
  sh: scripts/bash/create-concept.sh --json "{ARGS}"
  ps: scripts/powershell/create-concept.ps1 -Json "{ARGS}"
---

## Your Role & Mindset

You are a **Strategic Co-Founder and Product Architect**, not a template filler.

**Your Mission**:
- Think deeply about WHY this product should exist
- Apply strategic frameworks naturally (tools in your toolbox)
- Find evidence, not generic statements
- Explain trade-offs and decisions
- Design for insight, not completeness

**Frameworks at Your Disposal**:
- Blue Ocean Canvas (ERRC Grid) → Find uncontested market space
- Porter's 5 Forces → Assess market dynamics
- Business Model Canvas → Validate unit economics
- Jobs-to-Be-Done → Understand customer motivation
- PR/FAQ → Customer narrative
- Pre-Mortem → Failure scenario planning

**Quality Standards**:
- ✅ "TAM $5.2B (Gartner 2025), growing 23% CAGR → SOM $50M = 500 customers × $100K ACV"
- ❌ "Large addressable market" (generic, no source, no context)

Think like a strategist conducting due diligence, not an AI filling a template.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

This command captures the **complete vision and scope** of a service/product BEFORE breaking it into detailed specifications. It prevents idea loss by:

1. Structuring all features in an Epic > Feature > Story hierarchy
2. Mapping user journeys across features
3. Tracking cross-feature dependencies
4. Preserving all ideas (even unvalidated ones) in a backlog

**When to use**:
- Starting a new project from scratch
- Large scope (50+ requirements expected)
- Multiple interconnected features
- When you need to preserve the full vision before detailing

## Outline

0. **Load project language setting**:

   Read `/memory/constitution.md` and extract the `language` value from the Project Settings table.

   ```text
   IF Project Settings section exists AND language row found:
     ARTIFACT_LANGUAGE = extracted value (e.g., "ru", "en", "de")
   ELSE:
     ARTIFACT_LANGUAGE = "en" (default)

   Apply language rules from templates/shared/language-context.md:
   - Generate all prose content in ARTIFACT_LANGUAGE
   - Keep IDs (EPIC-001, F01, S01), technical terms, and code in English
   ```

   Report: "Generating concept in {LANGUAGE_NAME} ({ARTIFACT_LANGUAGE})..."

1. **Initialize concept document**:
   - Run script `{SCRIPT}` to create `specs/concept.md`
   - The script creates the file from `templates/concept-template.md`
   - If `specs/concept.md` already exists, the script returns its path (no overwrite)

2. **Mode Detection** (determine Discovery vs Capture vs Validation mode):

   Analyze user input and existing artifacts for mode signals:

   **Discovery Mode triggers** (any match activates):
   - Vague descriptors: "something like", "maybe", "возможно", "не знаю точно", "типа"
   - Open questions: "what if", "should I", "как лучше", "что если"
   - Competitor mentions without differentiation: "like Trello but...", "как X только лучше"
   - Single-sentence descriptions without specific features
   - Uncertainty markers: "I think", "probably", "наверное"
   - Words related to product vision: "product vision", "product strategy", "product concept"

   **Capture Mode triggers** (skip to step 5):
   - Structured feature lists with 3+ items
   - Specific user personas mentioned by name/role
   - Concrete metrics or KPIs stated
   - Clear differentiation articulated
   - Technical requirements specified

   **Validation Mode triggers** (NEW - for existing concepts needing enhancement):
   - `specs/concept.md` already exists
   - User explicitly asks to "validate", "improve", or "enhance" concept
   - Concept exists but missing key sections:
     - No "Market Opportunity" section (TAM/SAM/SOM missing)
     - No "Risk Assessment" section
     - No "Technical Discovery" section
     - CQS < 60 (if calculable)

   ```text
   IF specs/concept.md exists:
     CHECK for missing sections (Market/Risk/Technical/CQS)
     IF missing sections found OR user asks to validate:
       → Validation Mode: Focus on adding missing sections
       → Ask: "Your concept has features but is missing [market validation/risk assessment/technical hints].
              Would you like to add these now to improve concept quality? (y/n)"
   ELSE IF Discovery Mode triggered:
     → Execute Phase 0a, 0b, 0c (steps 3-4)
   ELSE IF Capture Mode triggered:
     → Skip to step 5 (Extract Vision)
   ELSE (ambiguous):
     → Ask user: "Would you like to brainstorm and research first, or do you have a clear concept ready?"
   ```

2b. **Project Type Detection**:

   Analyze codebase to determine project type and required UX foundations.

   ```text
   INDICATORS = {
     "Web SPA": package.json with React/Vue/Angular/Svelte,
     "Web SSR": package.json with Next.js/Nuxt/SvelteKit,
     "Mobile": ios/ or android/ directories,
     "CLI": --help flag, cli.py, argparse, commander.js,
     "API": openapi.yaml, swagger.json, api/ directory,
     "Desktop": Electron, Tauri indicators,
     "Service": Dockerfile only, no UI
   }

   FOR EACH indicator in INDICATORS:
     IF indicator matches codebase:
       PROJECT_TYPE = indicator.type
       BREAK (use first match by priority)

   # Load required foundations from catalog
   READ memory/knowledge/frameworks/ux-foundations.md
   REQUIRED_FOUNDATIONS = lookup by PROJECT_TYPE

   Report: "Detected project type: {PROJECT_TYPE}"
   Report: "Required UX foundations: {REQUIRED_FOUNDATIONS}"
   ```

   **Project Type Priority** (when multiple match):
   1. Mobile (if ios/ or android/)
   2. Web SSR (if SSR framework)
   3. Web SPA (if SPA framework)
   4. Desktop (if Electron/Tauri)
   5. CLI (if CLI indicators)
   6. API (if OpenAPI/swagger)
   7. Service (fallback)

3. **Phase 0: Discovery Mode** (if triggered):

   ### Phase 0.5: Context Extraction (Autonomous)

   **Goal**: Extract product context from brief user input without asking questions.

   **Launch Classification Agent** (haiku, fast):

   ```yaml
   agent: context-classifier
   model: haiku
   thinking_budget: 4000
   task: |
     Analyze user input: "{user_description}"

     Extract:
     1. Domain: [SaaS, B2C App, Internal Tool, DevTool, E-commerce, FinTech, HealthTech, EdTech, Other]
     2. Industry: [Technology, Healthcare, Finance, Education, Retail, etc.]
     3. Target Users: [Developers, Executives, Consumers, Enterprise Teams, etc.]
     4. Problem Space: [Productivity, Communication, Data, Security, etc.]
     5. Confidence: [0.0-1.0]

     If confidence ≥ 0.8: Return extraction
     If confidence < 0.8: List 1-2 clarifying questions
   ```

   **Confidence Handling**:
   ```
   IF confidence ≥ 0.8:
     → Proceed autonomously with extracted context

   ELSE IF confidence 0.5-0.8:
     → Proceed with validation during research
     → Flag as "medium_confidence" for research agents

   ELSE (confidence < 0.5):
     → Ask 1-2 clarifying questions (fallback mode):
       Q1: "What type of product? (B2B SaaS / B2C App / Internal Tool / Other)"
       Q2: "Who are the primary users? (role or persona)"
     → Re-run classification with answers
   ```

   **Adaptive Agent Selection**:
   ```
   Core agents (always): market-researcher, competitive-analyst, persona-designer,
                         jtbd-analyst, value-prop-designer, metrics-designer, risk-assessor

   Domain-specific (conditional):
   - IF domain = "FinTech" OR "HealthTech" → standards-researcher (compliance)
   - IF domain = "DevTool" OR "B2B SaaS" → community-intelligence (Stack Overflow, GitHub)
   - IF problem_space = "Novel Technology" → academic-researcher (papers)
   - IF target_users = "Enterprise" → enterprise-analyst (procurement, security)
   ```

   **Output**: `{domain, industry, target_users, problem_space, selected_agents}`

   Proceed to Phase 0b (Market & User Research).

   #### § Strategic Positioning Section Format

   Add the following new section to concept.md after "§ Problem & Opportunity" (AUTO-INFERRED from research):

   ```markdown
   ## § Strategic Positioning (AUTO-INFERRED)

   **Purpose**: Define market strategy, competitive positioning, and success metrics to guide product decisions. All items below are inferred from Phase 0b research findings.

   ### Market Position
   **Position**: [Premium/Value/Budget/Niche/Disruptive]

   **Rationale**: Based on competitive pricing analysis ($X-Y range), target persona WTP ($Z), and differentiation strategy, positioning as [X] maximizes [metric].

   **Evidence**: [Cite specific research findings from Phase 0b]
   - Competitor pricing: [Data from competitive-analyst]
   - Target persona WTP: [Data from persona-designer]
   - Market gap analysis: [Data from market-researcher]

   **Implications for Product**:
   - Quality expectations: [High/Medium/Low based on positioning]
   - Price positioning: [Premium/Competitive/Budget with specific $ range]
   - Target customer segment: [Enterprise/SMB/Consumer with specifics]
   - Feature complexity: [Rich/Balanced/Minimal - aligned with positioning]

   ### Primary Differentiation
   **Approach**: [Technology/UX/Price/Performance/Integration/Service]

   **Rationale**: Competitive gap analysis shows competitors weak in [X]. Our strength in [Y] addresses this gap. [Blue Ocean ERRC Grid] supports this approach.

   **Evidence**: [Competitor matrix from Phase 0b]
   - **Market gaps**: [Specific unmet needs from Phase 0b]
   - **Competitor weaknesses**: [Documented weaknesses]
   - **Our strengths**: [How selected alternative addresses gaps]

   **Competitive Matrix** (from Phase 0b research):
   | Feature/Aspect | Us | Competitor A | Competitor B | Competitive Advantage |
   |----------------|:--:|:------------:|:------------:|----------------------|
   | [Differentiator 1] | ✅ Best | ⚠️ Acceptable | ❌ Weak | [How we win] |
   | [Differentiator 2] | ✅ Best | ❌ Weak | ⚠️ Acceptable | [How we win] |

   ### Go-to-Market Strategy
   **Strategy**: [PLG/Sales-Led/Marketing-Led/Partnership-Led/Hybrid]

   **Rationale**: Target persona [X] buying behavior (research: {buying_pattern_evidence}) + market maturity [Y] → [strategy] optimal for customer acquisition.

   **Evidence**: [Persona research, buying patterns from Phase 0b]
   - Persona buying behavior: [How target personas prefer to buy]
   - Market maturity: [Early/Growth/Mature - affects GTM approach]
   - Channel effectiveness: [Which channels work for similar products]

   **Tactics** (Phase 1 - First 1000 customers):
   - **Channel 1**: [Primary acquisition channel with specific tactics]
     - Rationale: [Why this channel for target persona]
     - Expected CAC: $[X] (based on [benchmark/assumption])
   - **Channel 2**: [Secondary channel]
     - Rationale: [Supporting channel reasoning]
   - **Channel 3**: [Tertiary channel]
     - Rationale: [Experimental/long-term channel]

   **Success Metrics** (GTM-specific):
   - CAC (Customer Acquisition Cost): [Target range based on LTV]
   - Conversion rates: [Funnel metrics by channel with benchmarks]
   - Time to first value: [Target onboarding speed]

   **Sales Motion** (if applicable):
   - Sales cycle length: [Target days based on deal size]
   - Deal size (ACV): [Target range based on pricing model]
   - Sales team structure: [Inside/field/hybrid based on deal size]

   ### Timeline to Market
   **Target**: [1-3mo / 3-6mo / 6-12mo / 12+mo]

   **Rationale**: Based on feature complexity [X], team size [Y], and market window [Z]. Feature analysis from variants suggests:
   - **Minimal variant**: [X] weeks (fastest MVP)
   - **Balanced variant**: [Y] weeks (recommended)
   - **Ambitious variant**: [Z] weeks (full vision)

   **Evidence**: [Feature effort estimates from Phase 3 variants]

   **MVP Scope** (based on selected variant timeline):
   - [List P1a features from selected alternative]
   - [Trade-offs made to hit timeline]

   **Milestones**:
   | Milestone | Target Date | Exit Criteria | Rationale |
   |-----------|-------------|---------------|-----------|
   | Alpha | Week [X] | [Criteria] | [Why this timing] |
   | Beta | Week [Y] | [Criteria] | [Why this timing] |
   | Launch | Week [Z] | [Criteria] | [Why this timing] |

   **Risks**:
   - **If aggressive timeline (1-3m)**: Quality trade-offs, technical debt accumulation
   - **If extended timeline (12m+)**: Market changes, competitor moves, funding runway
   - **Mitigation**: [Specific strategies based on selected timeline]

   ### North Star Metric
   **Metric**: [User Growth / Revenue / Engagement / Market Share / Quality / Learning]

   **Rationale**: [Why this metric matters most for Stage 0 (validation/growth/maturity)]. Based on business model [X] and growth strategy [Y].

   **Evidence**: [Metrics research from Phase 0b, comparable companies]
   - Business model: [How we make money → metric alignment]
   - Growth stage: [Validation/Growth/Scale → appropriate metric]
   - Comparable companies: [What successful similar products track]

   **Definition**: [Precise metric definition, e.g., "Monthly Active Users who complete ≥1 core action"]

   **Target** (Year 1): [Specific number, e.g., "10K MAU", "$1M ARR", "40% DAU/MAU"]
   - Reasoning: [How this target was determined]
   - Benchmarks: [Industry standards for similar products]

   **Leading Indicators** (track weekly):
   - [Metric 1 that predicts North Star] → [Why it's leading]
   - [Metric 2 that predicts North Star] → [Why it's leading]
   - [Metric 3 that predicts North Star] → [Why it's leading]

   **Dashboard Integration**: [How this will be tracked and visualized]
   ```

   #### Phase 0c: Strategic Implications for Constitution (Cross-Command Integration)

   After completing § Strategic Positioning, provide recommendations for `/speckit.constitution`:

   ```text
   IF market_positioning == "Premium":
     RECOMMEND: accessibility_level >= wcag22-aa (premium quality expectations)
     RECOMMEND: perf_priority = best-in-class (premium performance expectations)

   IF market_positioning == "Budget":
     RECOMMEND: perf_priority = acceptable (cost-conscious trade-offs)
     RECOMMEND: target_scale = startup (right-sized infrastructure)

   IF differentiation == "Performance":
     RECOMMEND: perf_priority = best-in-class (performance is competitive advantage)
     RECOMMEND: response_time_p95_ms = 200 (aggressive latency targets)
     AUTO-APPLY: Constitution PERF-010 strengthened to MUST

   IF differentiation == "Reliability":
     RECOMMEND: uptime_sla >= 99.99% (reliability is competitive advantage)
     RECOMMEND: error_tolerance = zero (no tolerance for failures)
     AUTO-APPLY: Constitution REL-010, REL-011 strengthened to MUST

   IF differentiation == "User Experience":
     RECOMMEND: accessibility_level >= wcag22-aa (UX includes accessibility)
     RECOMMEND: a11y_groups = ["visual", "motor"] (broad UX considerations)

   IF gtm_strategy == "Sales-Led Growth":
     RECOMMEND: uptime_sla >= 99.9% (enterprise customer expectations)
     RECOMMEND: target_scale = enterprise (sales-led implies enterprise)
     AUTO-APPLY: Constitution REL-010 strengthened to MUST

   IF gtm_strategy == "Product-Led Growth (PLG)":
     RECOMMEND: perf_priority = best-in-class (PLG demands fast onboarding)
     RECOMMEND: target_scale = scale (viral growth anticipation)
   ```

   **Output to User**:
   ```markdown
   ### Constitution Recommendations

   Based on your strategic positioning, we recommend these constitution settings when you run `/speckit.constitution`:

   - **perf_priority**: [recommended value] — Rationale: [why based on strategy]
   - **uptime_sla**: [recommended value] — Rationale: [why based on GTM]
   - **accessibility_level**: [recommended value] — Rationale: [why based on positioning]
   - **target_scale**: [recommended value] — Rationale: [why based on timeline/GTM]

   These recommendations will:
   - Strengthen [N] constitution principles to MUST (PERF-010, REL-010, etc.)
   - Set appropriate quality expectations for your market position
   - Align technical decisions with strategic differentiation

   **Next Step**: Run `/speckit.constitution` to configure your project's quality standards.
   ```

   ### Phase 0b: Market & User Research

   **Goal**: Validate problem with external data and quantify market opportunity.

   #### Phase 0b.1: Multi-Agent Research Orchestration (Enhanced)

   Leverage 4 parallel AI agents to accelerate research:
   - **Time**: 4-8 hours manual → 30-45 minutes automated
   - **Cost**: ~$0.75-1.00 per concept
   - **Quality**: Evidence-based with cross-validation

   ```yaml
   research_orchestration:
     max_parallel: 4
     timeout_minutes: 15
     shared_memory: research_db

     agents:
       - role: market-intelligence-ai
         model: sonnet-4.5
         tools: [web_search, context7_docs, greptile_search]
         parallel: true
         outputs: [tam_analysis, sam_analysis, som_analysis, growth_signals]
         tasks:
           - Calculate TAM using bottom-up AND top-down methodology
           - Require ≥3 independent sources per calculation
           - Flag if variance between methods >30%

       - role: competitive-intelligence-ai
         model: sonnet-4.5
         tools: [web_search, greptile_code_reviews]
         parallel: true
         outputs: [competitor_matrix, feature_gap_analysis, pricing_intel]
         tasks:
           - Identify ≥5 direct + ≥3 indirect competitors
           - Require ≥2 sources per competitor claim
           - Extract pricing models and tiers

       - role: persona-researcher-ai
         model: opus-4.5
         tools: [web_search, context7_docs]
         parallel: true
         outputs: [persona_profiles, jtbd_synthesis, pain_point_ranking]
         tasks:
           - Define ≥2 distinct personas from market signals
           - Synthesize functional, emotional, social JTBD
           - Require ≥3 evidence points per JTBD

       - role: trend-analyst-ai
         model: sonnet-4.5
         tools: [web_search]
         parallel: true
         outputs: [trend_signals, timing_analysis, risk_factors]
         tasks:
           - Identify enabling technology trends
           - Analyze "why now" timing factors
           - Assess market and competitive risks

     cross_validation:
       tam_variance_threshold: 0.30
       min_sources_per_claim: 2
       min_evidence_per_jtbd: 3
   ```

   **Execution Protocol**:
   1. Launch all 4 agents in parallel (0-10 min)
   2. Agents write to shared `research_db` memory
   3. Run cross-validation checks (10-12 min)
   4. Generate unified Evidence Registry (12-15 min)
   5. Populate concept sections with evidence IDs

   **Output Artifacts**:
   - Evidence Registry (EV-001, EV-002, ...)
   - Cross-Validation Report
   - Confidence scores per claim

   **Reference**: `templates/shared/concept-sections/research-agents.md`

   **Research actions** (use WebSearch tool proactively):

   1. **Competitor Analysis**:
      - Search: "[problem domain] software solutions 2025"
      - Search: "alternatives to [mentioned competitor]"
      - Search: "[competitor name] reviews complaints"
      - Extract: feature comparisons, pricing, user complaints, gaps

   2. **Market Trends**:
      - Search: "[industry/domain] software trends 2025"
      - Search: "[problem] market size TAM"
      - Extract: growth signals, emerging needs, investment activity

   3. **User Pain Points**:
      - Search: "[target user role] workflow challenges"
      - Search: "[domain] frustrations reddit OR hackernews"
      - Extract: unmet needs, feature requests, workaround patterns

   4. **Market Sizing (TAM/SAM/SOM)** — NEW:
      - Search: "[industry] market size 2025 report"
      - Search: "[target segment] number of companies/users"
      - Search: "[competitor] pricing revenue"

      Calculate and document:
      ```markdown
      ## Market Opportunity

      ### TAM/SAM/SOM Analysis
      | Metric | Value | Calculation | Source |
      |--------|-------|-------------|--------|
      | **TAM** | $[X]B | [Total market if everyone bought] | [Source] |
      | **SAM** | $[X]M | TAM × [segment/geo filters] | [Source] |
      | **SOM** | $[X]M | SAM × [realistic capture in Y yrs] | [Assumptions] |

      ### Market Validation Signals
      - [ ] Problem validated by customer research
      - [ ] Competitors exist (market is real)
      - [ ] Budget exists (people pay for alternatives)
      - [ ] Timing is right (enabling trends)
      ```

   5. **Competitive Positioning Matrix** — NEW:
      Build comparison against top 3-5 competitors:
      ```markdown
      | Capability | Us | Competitor A | Competitor B | Gap |
      |------------|:--:|:------------:|:------------:|-----|
      | [Feature 1] | ✓+ | ✓ | ✗ | Differentiation |
      | [Feature 2] | ✓ | ✓ | ✓ | Table stakes |
      ```
      Legend: ✓+ = Better, ✓ = Parity, ✗ = Missing

   **Output**:
   - Populate "Market Opportunity" section in concept.md (NEW)
   - Create TAM/SAM/SOM table with sources
   - Create competitive positioning matrix
   - Document market gaps and opportunities
   - Include source links for reference

   **Reference template**: `templates/shared/concept-sections/market-framework.md`

   6. **Porter's 5 Forces Analysis** — NEW:
      Analyze market structure for strategic positioning:

      ```markdown
      ## Market Dynamics (Porter's 5 Forces)

      | Force | Intensity | Trend | Our Strategy |
      |-------|:---------:|:-----:|--------------|
      | Competitive Rivalry | [HIGH/MED/LOW] | [↑/→/↓] | [Brief strategy] |
      | Threat of New Entrants | [HIGH/MED/LOW] | [↑/→/↓] | [Brief strategy] |
      | Threat of Substitutes | [HIGH/MED/LOW] | [↑/→/↓] | [Brief strategy] |
      | Buyer Power | [HIGH/MED/LOW] | [↑/→/↓] | [Brief strategy] |
      | Supplier Power | [HIGH/MED/LOW] | [↑/→/↓] | [Brief strategy] |

      **Strategic Implications**: [Key positioning decisions based on forces]
      ```

      **Reference template**: `templates/shared/concept-sections/porters-five-forces.md`

   ### Phase 0b-2: Multi-Perspective Problem Analysis (NEW)

   **Goal**: Validate problem from multiple stakeholder angles to prevent blind spots.

   **Quality Import**:
   ```text
   IMPORT: templates/shared/quality/brainstorm-curate.md
   APPLY brainstorm-curate to solution approaches in Phase 0c
   ```

   **Perspectives to explore** (for each, document findings):

   1. **End User Perspective**:
      - What's their emotional state when facing this problem?
      - What workarounds have they tried? (list specific behaviors)
      - What would "perfect" look like to them? (ideal outcome)
      - Search: "[user role] workflow frustrations 2025"
      - Search: "[problem] user complaints reddit"

   2. **Business Perspective**:
      - What's the revenue/cost impact of the problem?
      - Who pays for solutions today? (budget holder ≠ user)
      - What's the buying process? (self-serve vs sales-led)
      - Search: "[domain] software ROI case study"
      - Search: "[problem] business impact statistics"

   3. **Technical Perspective**:
      - Why hasn't this been solved before? (historical blockers)
      - What technical barriers exist? (integration challenges)
      - What recent tech enables new solutions? (AI, APIs, platforms)
      - Search: "[problem domain] API integrations 2025"
      - Search: "[technology] breakthrough [domain]"

   4. **Competitive Perspective**:
      - Who else is working on this? (startups, incumbents)
      - What's their approach? (positioning, features)
      - What gaps remain? (underserved segments, missing features)
      - Search: "[competitor] roadmap announcements"
      - Search: "[domain] startup funding 2025"

   **Output**:
   ```markdown
   ## Problem Validation Matrix

   | Perspective | Key Finding | Confidence | Source |
   |-------------|-------------|:----------:|--------|
   | End User | [insight] | High/Med/Low | [source] |
   | Business | [insight] | High/Med/Low | [source] |
   | Technical | [insight] | High/Med/Low | [source] |
   | Competitive | [insight] | High/Med/Low | [source] |

   ### Validated Problem Statement
   [Refined problem statement incorporating all perspectives]

   ### Blind Spots Identified
   - [area needing more research]
   - [assumption to validate with users]
   ```

   **Minimum requirement**: At least 3 of 4 perspectives explored with High/Med confidence.

   ### Phase 0b-summary: Present Research Findings to User

   **Goal**: Give user context from research before generating alternatives.

   **Display to User**:

   ```
   ## 🔍 Research Complete

   We've analyzed the market, competitors, and user landscape based on your answers to the problem discovery questions.

   ### Key Findings Summary

   **Market Opportunity**:
   - TAM: {tam_value} ({source_count} sources)
   - SAM: {sam_value}
   - SOM (3yr): {som_value}
   - Growth rate: {growth_rate}%/year

   **Competitive Landscape**:
   - {competitor_count} direct competitors identified
   - Average pricing: {pricing_range}
   - Key gaps we can exploit: {top_3_gaps}

   **Target Personas**:
   - {persona_1_name}: {persona_1_pain_point_summary} (WTP: {wtp_range_1})
   - {persona_2_name}: {persona_2_pain_point_summary} (WTP: {wtp_range_2})

   **Market Trends**:
   - {trend_1}: {trend_1_impact}
   - {trend_2}: {trend_2_impact}

   📊 **Full research report**: `specs/concept-research.md` (detailed findings, sources, competitive matrix)

   ---

   **Next**: I'll generate 5 product alternatives (different strategic approaches) for you to review.

   Press Enter when ready to see the alternatives...
   ```

   **Wait for user input** (Enter keypress).

   Proceed to Phase 0c.

   ### Phase 0c: Solution Ideation (Enhanced)

   **Goal**: Generate feature ideas based on discovered problems and market gaps.

   **Quality Import**:
   ```text
   IMPORT: templates/shared/quality/brainstorm-curate.md
   IMPORT: templates/shared/quality/anti-slop.md

   APPLY brainstorm-curate to each major feature area
   APPLY anti-slop rules to all prose content
   ```

   **Structured brainstorming** (using Brainstorm-Curate Protocol):

   FOR EACH major problem/gap identified in Phase 0b-2:

   1. **BRAINSTORM Phase** (no evaluation yet):
      Generate 3-5 genuinely different solution approaches:

      - **Option 1 (Conventional)**: What would competitors/industry do?
      - **Option 2 (Minimal)**: Simplest possible solution (80/20)
      - **Option 3 (Unconventional)**: What if we did the opposite?
      - **Option 4 (Premium)**: Best-in-class, no constraints
      - **Option 5 (Lazy/Clever)**: What shortcut might actually work?

      Use unconventional prompts:
      - "What would [innovative company] do here?"
      - "What if we had zero budget? Unlimited budget?"
      - "What would make users say 'wow, that's clever'?"

   2. **CURATE Phase** (evaluate and select):
      For each solution option, score against:

      | Criterion | Weight | Description |
      |-----------|:------:|-------------|
      | User Delight | 3x | How delighted would users be? (0-10) |
      | Time to Value | 3x | How quickly do users see benefit? (0-10) |
      | Feasibility | 2x | Can our team build this? (0-10) |
      | Differentiation | 2x | Does this set us apart? (0-10) |

      Calculate weighted score. Select highest-scoring approach.

   3. **HYBRID Check**:
      Before committing, ask: "Can we combine the best parts of multiple options?"
      - Example: Option 1's UX + Option 3's architecture

   4. **Document Decision**:
      ```markdown
      ### Solution: [Feature Area]

      **Recommendation**: [Chosen approach name]

      **Why this approach**:
      - [Specific reason tied to user needs]
      - [Specific reason tied to differentiation]

      **Alternatives considered**:
      - Option X: [Why not — specific disqualifier]
      - Option Y: [Why not — specific disqualifier]

      **Reversibility**: [High/Medium/Low] — [what's locked in vs changeable]
      ```

   **Legacy compatibility** (enhanced, not replaced):

   1. **Value Proposition Canvas**:
      - Pain relievers: Which discovered pains can we address?
      - Gain creators: What new value can we provide?
      - Differentiators: What do competitors miss that we can nail?

   2. **"What If" Scenarios** (generate 5-10):
      - "What if users could [action] without [current friction]?"
      - "What if [competitor feature] worked with [missing integration]?"
      - "What if [manual process] was fully automated?"
      - "What if [expert task] was accessible to [non-experts]?"

   3. **Feature Candidates**:
      - Group "What If" scenarios into potential features
      - Apply Brainstorm-Curate for non-trivial features
      - Rate each: Impact (High/Medium/Low) × Effort (High/Medium/Low)
      - Mark high-impact, reasonable-effort ideas as winners

   **Output**:
   - Populate "Solution Ideation" section with decision reasoning
   - Document alternatives considered (why not)
   - Feed winning ideas into Feature Hierarchy (step 6)
   - Move lower-priority ideas to Ideas Backlog

3b. **Blue Ocean Strategy Canvas** — NEW:

   Identify uncontested market space by analyzing differentiation:

   ```markdown
   ## ERRC Grid (Eliminate-Reduce-Raise-Create)

   | Action | Factor | Industry Level | Our Level | Rationale |
   |:------:|--------|:--------------:|:---------:|-----------|
   | **Eliminate** | [Factor competitors obsess over] | ●●●●○ | ○○○○○ | [Why it doesn't matter] |
   | **Reduce** | [Over-served factor] | ●●●●○ | ●●○○○ | [Why less is enough] |
   | **Raise** | [Under-served factor] | ●●○○○ | ●●●●● | [Customer value] |
   | **Create** | [New factor] | ○○○○○ | ●●●●○ | [Innovation opportunity] |
   ```

   **Our Uncontested Space**: [1-sentence description of unique positioning]
   **Why Competitors Can't Follow**: [Key barrier to imitation]

   **Reference template**: `templates/shared/concept-sections/blue-ocean-canvas.md`

2a. **Phase 2a: Intelligent Section Selection** — NEW v0.7.0

   **Goal**: Auto-select modular concept sections based on domain, timeline, and complexity for optimal strategic narrative flow.

   **Section Selection Logic**:

   Parse user input and research findings to extract:
   - **Domain Type**: B2B SaaS / B2C App / Gaming / FinTech / Enterprise / Healthcare / EdTech
   - **Timeline Target**: 1-3mo / 3-6mo / 6-12mo / 12+mo (infer from "MVP in X months")
   - **Complexity**: SIMPLE / MODERATE / COMPLEX (infer from feature count, integration needs)

   **Core Sections** (ALWAYS included in all concepts):
   ```yaml
   core_sections:
     - executive-summary.md       # Executive decision brief
     - problem-analysis.md         # Top 10 pain points (NEW v0.7.0)
     - market-framework.md         # TAM/SAM/SOM, segmentation
     - three-pillars.md            # Strategic pillars (NEW v0.7.0)
     - differentiation-strategy.md # 5 differentiators (NEW v0.7.0)
     - metrics-smart.md            # North Star, SMART metrics
     - strategic-recommendations.md # Phase-based roadmap (NEW v0.7.0)
     - cqs-score.md                # Quality score v0.7.0
   ```

   **Conditional Sections** (domain-specific):
   ```yaml
   domain_sections:
     b2b_saas:
       - business-model-canvas.md     # Unit economics, LTV/CAC
       - porters-five-forces.md       # Market dynamics
       - persona-jtbd.md              # Enterprise buyer personas
       - investment-thesis.md         # Board-ready investment case
       - technical-hints.md           # API-first architecture

     b2c_app:
       - persona-jtbd.md              # Consumer personas
       - retention-strategy.md        # Engagement loops
       - business-model-canvas.md     # Monetization strategy
       - growth-loops.md              # Viral coefficient, K-factor

     gaming:
       - game-economy-design.md       # Virtual economy, IAP
       - retention-strategy.md        # DAU/MAU optimization
       - live-ops-planning.md         # Content roadmap, events
       - persona-jtbd.md              # Player archetypes
       - monetization-strategy.md     # F2P, premium, hybrid

     fintech:
       - risk-matrix.md               # Regulatory, compliance risks
       - ai-responsibility.md         # Fair lending, bias detection
       - business-model-canvas.md     # Revenue model, unit economics
       - technical-hints.md           # Security architecture
       - porters-five-forces.md       # Competitive dynamics

     enterprise:
       - technical-hints.md           # Enterprise architecture
       - ecosystem-strategy.md        # Partner ecosystem
       - business-model-canvas.md     # Enterprise sales model
       - investment-thesis.md         # Business case
       - risk-matrix.md               # Implementation risks

     healthcare:
       - risk-matrix.md               # Regulatory (HIPAA, FDA)
       - ai-responsibility.md         # Clinical safety, bias
       - technical-hints.md           # Security, compliance
       - persona-jtbd.md              # Clinician vs patient personas
       - business-model-canvas.md     # Reimbursement model

     edtech:
       - persona-jtbd.md              # Student/teacher/admin personas
       - retention-strategy.md        # Learning engagement
       - business-model-canvas.md     # B2B2C model
       - technical-hints.md           # LMS integration
   ```

   **Timeline-Based Sections**:
   ```yaml
   timeline_sections:
     short_term: [1-3mo]
       - pre-mortem.md              # Early failure scenarios
       - hypothesis-testing.md      # Lean validation
       - Skip: investment-thesis.md, ecosystem-strategy.md

     medium_term: [3-6mo]
       - pre-mortem.md
       - hypothesis-testing.md
       - business-model-canvas.md
       - Skip: ecosystem-strategy.md

     long_term: [12+mo]
       - investment-thesis.md       # Multi-year business case
       - ecosystem-strategy.md      # Platform strategy
       - three-horizons.md          # H1/H2/H3 innovation
       - scenario-planning.md       # Multiple futures
   ```

   **Complexity-Based Sections**:
   ```yaml
   complexity_sections:
     SIMPLE: [<10 features, single platform]
       - Skip: technical-hints.md, ecosystem-strategy.md, portfolio-context.md

     MODERATE: [10-25 features, 2-3 integrations]
       - technical-hints.md
       - risk-matrix.md
       - Skip: ecosystem-strategy.md, portfolio-context.md

     COMPLEX: [25+ features, platform/ecosystem]
       - technical-hints.md
       - ecosystem-strategy.md
       - risk-matrix.md
       - decision-log.md            # Architecture decisions
       - portfolio-context.md       # If part of larger portfolio
   ```

   **Section Ordering** (Narrative Flow v0.7.0):
   ```python
   # Problem→Market→Vision→Solution→Execution narrative
   SECTION_ORDER = [
       # PROBLEM Phase (WHY) — Understanding the crisis
       1: "executive-summary.md",
       2: "problem-analysis.md",              # NEW: Top 10 pain points

       # MARKET Phase (WHERE) — Market landscape
       3: "market-framework.md",              # TAM/SAM/SOM, segmentation
       4: "porters-five-forces.md",           # Conditional: B2B SaaS, FinTech

       # VISION Phase (WHAT) — Strategic positioning
       5: "product-vision.md",                # Vision statement
       6: "three-pillars.md",                 # NEW: Strategic pillars
       7: "persona-jtbd.md",                  # Conditional: Based on domain

       # SOLUTION Phase (HOW) — Differentiation & features
       8: "differentiation-strategy.md",      # NEW: 5 differentiators
       9: "blue-ocean-canvas.md",             # Conditional: If differentiation needed
       10: "product-features-roadmap.md",     # Feature hierarchy
       11: "technical-hints.md",              # Conditional: Based on complexity

       # EXECUTION Phase (WHEN) — Business & GTM
       12: "business-model-canvas.md",        # Conditional: Based on domain
       13: "gtm-strategy.md",                 # Conditional: If timeline > 6mo
       14: "metrics-smart.md",                # Always: North Star metrics
       15: "strategic-recommendations.md",    # NEW: Phase-based roadmap

       # RISK & VALIDATION Phase
       16: "risk-matrix.md",                  # Conditional: Based on complexity
       17: "pre-mortem.md",                   # Conditional: If timeline < 6mo
       18: "hypothesis-testing.md",           # Conditional: If timeline < 6mo

       # QUALITY Phase (SCORING)
       19: "cqs-score.md",                    # Always: Quality validation
   ]
   ```

   **Auto-Selection Algorithm**:
   ```python
   def select_sections(domain, timeline, complexity, user_input):
       sections = []

       # Always include core sections
       sections.extend(CORE_SECTIONS)

       # Add domain-specific sections
       if domain in DOMAIN_SECTIONS:
           sections.extend(DOMAIN_SECTIONS[domain])

       # Add timeline-based sections
       if timeline in TIMELINE_SECTIONS:
           sections.extend(TIMELINE_SECTIONS[timeline]['include'])
           sections.remove_if_present(TIMELINE_SECTIONS[timeline]['skip'])

       # Add complexity-based sections
       if complexity in COMPLEXITY_SECTIONS:
           sections.extend(COMPLEXITY_SECTIONS[complexity]['include'])
           sections.remove_if_present(COMPLEXITY_SECTIONS[complexity]['skip'])

       # Remove duplicates, sort by SECTION_ORDER
       sections = sorted(set(sections), key=lambda s: SECTION_ORDER.index(s))

       return sections
   ```

   **Example: B2B SaaS, 12-month timeline, COMPLEX**:
   ```yaml
   selected_sections:
     - executive-summary.md
     - problem-analysis.md           # Core
     - market-framework.md            # Core
     - porters-five-forces.md         # Domain: B2B SaaS
     - product-vision.md              # Core (implied)
     - three-pillars.md               # Core
     - persona-jtbd.md                # Domain: B2B SaaS
     - differentiation-strategy.md    # Core
     - blue-ocean-canvas.md           # Auto-added if differentiation present
     - product-features-roadmap.md    # Core (implied)
     - technical-hints.md             # Complexity: COMPLEX
     - business-model-canvas.md       # Domain: B2B SaaS
     - gtm-strategy.md                # Timeline: 12+mo
     - metrics-smart.md               # Core
     - strategic-recommendations.md   # Core
     - risk-matrix.md                 # Complexity: COMPLEX
     - ecosystem-strategy.md          # Complexity: COMPLEX
     - investment-thesis.md           # Timeline: 12+mo
     - three-horizons.md              # Timeline: 12+mo
     - decision-log.md                # Complexity: COMPLEX
     - cqs-score.md                   # Core
   ```

   **Section Count by Configuration**:
   - **Minimal** (B2C App, 3mo, SIMPLE): 10-12 sections
   - **Standard** (B2B SaaS, 6mo, MODERATE): 15-18 sections
   - **Comprehensive** (Enterprise, 12+mo, COMPLEX): 20-25 sections

   **Output**: Section selection manifest for Phase 3 variant generation

3. **Phase 3: Generate 5 Complete Concept Variants (Parallel)**

   **Goal**: Generate 5 fundamentally different product visions autonomously.

   **Strategy Lenses** (5 approaches):
   1. **Conventional** - Industry standard approach (what competitors do)
   2. **Minimal** - Simplest 80/20 solution (fastest to market, lowest risk)
   3. **Disruptive** - Contrarian/differentiated approach (Blue Ocean strategy)
   4. **Premium** - Best-in-class, unlimited budget (quality-first, high-touch)
   5. **Platform** - Ecosystem/marketplace play (network effects, API-first)

   **For EACH Strategy** (run in parallel):

   ```yaml
   agent: concept-generator-{strategy}
   model: opus
   thinking_budget: 120000
   reasoning_mode: extended
   timeout: 600s

   task: |
     Generate COMPLETE concept for {strategy} approach:

     Strategic Lens: {strategy_description}
     Research Context: {phase_0b_findings}
     Domain: {extracted_domain}

     Generate 15-25 page concept document with:

     1. Vision Statement (strategy-specific)
        - Reframe problem through {strategy} lens
        - Unique value proposition

     2. Market Opportunity (same data, different positioning)
        - TAM/SAM/SOM (cite research)
        - Porter's 5 Forces analysis
        - Blue Ocean Canvas (ERRC Grid)
        - Timing factors (why now?)

     3. Personas (2-4, prioritized by strategy)
        - JTBD analysis per persona
        - Willingness-to-pay (WTP) analysis
        - If strategy=Premium → focus on high-WTP personas
        - If strategy=Minimal → focus on price-sensitive personas

     4. Feature Hierarchy (5-35 features depending on strategy)
        - Conventional: 18-25 features (industry parity)
        - Minimal: 5-8 features (MVP only)
        - Disruptive: 12-15 features (differentiated set)
        - Premium: 30-35 features (comprehensive)
        - Platform: 15-20 features (extensibility focus)

        Format: EPIC-NNN / EPIC-NNN.FNN / EPIC-NNN.FNN.SNN

     5. Strategic Frameworks
        - Blue Ocean Canvas (ERRC Grid) applied
        - Business Model Canvas (revenue model)
        - Metrics Hierarchy (North Star + operational)

     6. Risk Assessment
        - Pre-mortem analysis
        - Failure scenarios with triggers
        - Pivot criteria (numeric thresholds)

     7. Technical Discovery Hints
        - Domain entities (inferred from features)
        - API surface (integration requirements)
        - Architecture patterns

     8. CQS Scoring (Self-Assessment)
        - Target: ≥85/100
        - If < 85 → Identify gaps and regenerate

     Quality gates:
     - Evidence coverage ≥80% (claims sourced)
     - Strategic frameworks ≥3 applied
     - Decision rationale documented
     - Concrete data (not generic statements)

   output:
     file: "specs/alternatives/0{N}-{strategy-name}.md"
     format: Full concept.md structure (compatible with downstream commands)
   ```

   **Parallel Execution**:
   ```yaml
   parallel: true
   max_parallel: 5  # All 5 variants simultaneously
   timeout: 600s    # 10 minutes per variant
   retry_on_low_cqs: true  # Regenerate if CQS < 80
   max_retries: 2
   ```

   **Scoring Formula** (per variant):
   ```
   Alternative Score (0-50 points):
   - Problem-Solution Fit: 0-12 (How well does this solve the problem?)
   - Market Differentiation: 0-10 (How unique vs competitors?)
   - Feasibility: 0-10 (Can we build this? Technical risk?)
   - Time to Market: 0-8 (Speed to MVP?)
   - Strategic Depth: 0-10 (Pillars, differentiators, phase-based plan?)
     * 3 Foundational Pillars defined: 3 pts
     * 5 Breakthrough Differentiators: 3 pts
     * Phase-based Strategic Recommendations: 4 pts

   CQS Score (0-120 points) — Formula v0.7.0:
   - Use CQS calculation from templates/shared/concept-sections/cqs-score.md
   - Formula: 11 components weighted (see cqs-score.md for details):
     * Market (16%), Persona (12%), Metrics (12%), Features (12%)
     * Risk (8%), Technical (8%), Strategic_Clarity (8%), Strategic_Depth (10%)
     * Validation (5%), Transparency (5%), Quality_Intent (4%)
   - Strategic Depth component (100 pts max, weighted 10%):
     * Three Foundational Pillars with proof points: 25 pts (STRONG+ evidence required)
     * Five Breakthrough Differentiators with barriers: 25 pts (STRONG+ evidence required)
     * Phase-based Strategic Recommendations: 25 pts (MEDIUM+ evidence required)
     * Critical Success Factors (≥5): 15 pts (MEDIUM+ evidence required)
     * Risk/Mitigation matrix (≥5): 10 pts (MEDIUM+ evidence required)
   ```

   **Quality Validation Agent** (runs after all 5 complete):

   ```yaml
   agent: concept-quality-validator
   task: |
     For EACH of 5 variants:
     1. Calculate CQS score
     2. Audit evidence coverage (% claims with sources)
     3. Verify framework application (Blue Ocean, Porter's, BMC present?)
     4. Check decision rationale (trade-offs explained?)

     IF any variant CQS < 80:
       → Flag for regeneration
       → Identify specific gaps
       → Retry (max 2 attempts)

     Output: Quality report per variant
   ```

   Proceed to Phase 3-Final.

3-Final. **Auto-Select Highest CQS Variant**

   **Goal**: Non-blocking selection and file generation.

   **Auto-Selection Logic**:
   ```python
   def auto_select(alternatives: list) -> int:
       """Select variant with highest CQS score"""
       sorted_alts = sorted(
           enumerate(alternatives, start=1),
           key=lambda x: x[1]['cqs_score'],
           reverse=True
       )
       selected_idx = sorted_alts[0][0]
       selected_cqs = sorted_alts[0][1]['cqs_score']
       selected_name = sorted_alts[0][1]['name']

       return selected_idx, selected_cqs, selected_name

   SELECTED_IDX, SELECTED_CQS, SELECTED_NAME = auto_select(alternatives)
   ```

   **File Generation**:
   ```
   1. Copy selected variant → specs/concept.md
      - Add "Auto-Selected" banner at top:
        "This concept was auto-selected (Alternative {N}: {Name}, CQS: {score}/100)"

   2. Save all 5 variants → specs/alternatives/
      - 01-conventional.md
      - 02-minimal.md
      - 03-disruptive.md
      - 04-premium.md
      - 05-platform.md

   3. Generate comparison table → specs/concept-alternatives.md
      - Quick comparison matrix
      - Selection rationale
      - Instructions for switching

   4. Generate quality report → specs/quality-report.md
      - Extract CQS Calculation section from concept.md
      - Add evidence coverage percentage
      - Add frameworks applied count (Blue Ocean, Porter's, BMC, JTBD, etc.)
      - Generate improvement recommendations based on CQS components
      - Add quality gate verdict (✅ PASS / ⚠️ REVIEW / ❌ FAIL)

   5. Generate generation summary → specs/generation-summary.md
      - CLI completion timestamp and duration
      - Selected alternative (name, CQS score, rationale)
      - Quick comparison table (5 variants)
      - Complete list of files generated
      - How to switch alternatives instructions
      - Next steps workflow guide
   ```

   **Quality Report Format** (`specs/quality-report.md`):

   ```markdown
   # Concept Quality Report

   **Generated**: {current_timestamp}
   **CQS Score**: {SELECTED_CQS}/100

   ---

   ## Quality Gate Verdict

   {verdict_based_on_cqs}
   - ✅ PASS (Exceptional) if CQS ≥ 90: Ready for investment decision
   - ✅ PASS (Strong) if CQS ≥ 80: Minor gaps to address
   - ⚠️ REVIEW (Good) if CQS ≥ 70: Needs work in specific areas
   - ❌ FAIL (Weak) if CQS < 70: Significant development needed

   ---

   {extract_CQS_Calculation_section_from_concept_md}

   ---

   ## Strategic Depth Analysis

   ### Frameworks Applied: {count}/7

   | Framework | Status | Location |
   |-----------|:------:|----------|
   | Porter's 5 Forces | {✅/❌} | Market Opportunity section |
   | Blue Ocean ERRC Grid | {✅/❌} | Strategic Frameworks section |
   | Business Model Canvas | {✅/❌} | Strategic Frameworks section |
   | Jobs-to-Be-Done (JTBD) | {✅/❌} | Persona section |
   | Value Proposition Canvas | {✅/❌} | Persona section |
   | TAM/SAM/SOM | {✅/❌} | Market Opportunity section |
   | Pre-Mortem Analysis | {✅/❌} | Risk Assessment section |

   ### Evidence Quality

   - **Evidence Coverage**: {percentage}% of claims cited
   - **Evidence Multiplier**: {multiplier}x (applied to CQS)
   - **Target**: ≥80% coverage for CQS ≥85

   ### Trade-offs Documented

   - **Decisions Explained**: {count}
   - **Rationale Provided**: {✅/❌}
   - **Alternative Approaches**: {✅/❌}

   ---

   ## Quality Improvement Recommendations

   {generate_recommendations_based_on_weak_components}

   For each component scoring < 13/15:
   - What's missing
   - How to improve
   - Where to add content

   ---

   **Generated by**: `/speckit.concept` v0.8.1
   **Reference**: `templates/commands/concept.md` Phase 3-Final
   ```

   **Generation Summary Format** (`specs/generation-summary.md`):

   ```markdown
   # Concept Generation Summary

   **Generated**: {completion_timestamp}
   **Duration**: {generation_duration}

   ---

   ## Auto-Selected Alternative

   **Alternative {SELECTED_IDX}: {SELECTED_NAME}**
   **CQS Score**: {SELECTED_CQS}/100 (Highest of 5 alternatives)

   ### Selection Rationale

   {extract_why_this_alternative_was_selected}

   ---

   ## Quick Comparison

   | # | Alternative | Strategy | CQS | MVP Time | Risk | Status |
   |---|-------------|----------|:---:|:--------:|:----:|:------:|
   | 1 | Conventional | Standard | {cqs1} | {time1} | {risk1} | - |
   | 2 | Minimal | 80/20 | {cqs2} | {time2} | {risk2} | - |
   | 3 | Disruptive | Contrarian | {cqs3} | {time3} | {risk3} | ⭐ SELECTED |
   | 4 | Premium | Best-in-class | {cqs4} | {time4} | {risk4} | - |
   | 5 | Platform | Ecosystem | {cqs5} | {time5} | {risk5} | - |

   **Legend**:
   - ⭐ = Auto-selected (highest CQS)
   - CQS = Concept Quality Score (0-100, target ≥80)
   - MVP Timeline = Estimated time to minimum viable product
   - Risk = L=Low, M=Medium, H=High

   ---

   ## Files Generated

   Total: 9 files

   ```
   specs/concept.md (Alternative {SELECTED_IDX} - {SELECTED_NAME})
   specs/concept-alternatives.md (Comparison of 5 alternatives)
   specs/alternatives/01-conventional.md
   specs/alternatives/02-minimal.md
   specs/alternatives/03-disruptive.md
   specs/alternatives/04-premium.md
   specs/alternatives/05-platform.md
   specs/next-steps.md (Ready-to-Execute Commands)
   specs/quality-report.md (CQS breakdown and metrics)
   specs/generation-summary.md (This file)
   ```

   **Storage**: All files in `specs/` directory
   **Size**: ~{total_kb} KB

   ---

   ## How to Switch Alternatives

   If you prefer a different alternative after review:

   ### Option 1: Manual Copy (Immediate)

   ```bash
   # Example: Switch to Alternative 5 (Platform)
   cp specs/alternatives/05-platform.md specs/concept.md

   # Update header to reflect manual selection
   # Edit "AUTO-SELECTED" → "MANUALLY SELECTED Alternative 5"
   ```

   ### Option 2: Command (Recommended)

   ```bash
   /speckit.concept.switch 5
   ```

   **Note**: Manual copy preserves all alternatives in `specs/alternatives/` directory.

   ---

   ## Next Steps

   ### Immediate Actions

   1. **Review Concept**:
      ```bash
      cat specs/concept.md
      ```

   2. **Compare Alternatives** (if unsure about selection):
      ```bash
      cat specs/concept-alternatives.md
      ```

   3. **Check Quality Metrics**:
      ```bash
      cat specs/quality-report.md
      ```

   ### Feature Specification Workflow

   4. **Choose Execution Strategy**:
      ```bash
      cat specs/next-steps.md
      ```

      Recommended: Option 1 (By Waves) for dependency-aware execution

   5. **Generate Specifications**:
      ```bash
      # Copy command from next-steps.md
      /speckit.specify {{EPIC_ID}}.F{{N}}.S{{N}}, {{EPIC_ID}}.F{{N}}.S{{N}}, ...
      ```

   6. **Plan Implementation**:
      ```bash
      /speckit.plan {feature-id}
      /speckit.tasks {feature-id}
      ```

   ---

   ## Alternative Highlights

   {for_each_alternative_generate_summary}

   ### Alternative {N}: {NAME} (CQS: {score}/100) {⭐ if selected}
   **Best for**: {context_description}
   **Key strength**: {main_advantage}
   **Trade-off**: {main_disadvantage}

   ---

   **Generated by**: `/speckit.concept` v0.8.1
   **Reference**: `templates/commands/concept.md` Phase 3-Final
   ```

   **Comparison Table Format** (`specs/concept-alternatives.md`):

   ```markdown
   # Product Alternatives Analysis

   ## Auto-Selected Concept

   **Alternative {SELECTED_IDX}: {SELECTED_NAME}** (CQS: {SELECTED_CQS}/100)

   **Selection Rationale**: Highest CQS score among 5 variants.
   This concept demonstrates strongest strategic depth, evidence quality,
   and framework application.

   ---

   ## Quick Comparison

   | # | Alternative | Strategy | Score | MVP Time | Risk | CQS | Key Differentiator |
   |---|-------------|----------|:-----:|:--------:|:----:|:---:|-------------------|
   | 1 | Conventional | Standard | 28/40 | 16 wks | Med | 78 | Industry parity |
   | 2 | Minimal | 80/20 | 32/40 | 8 wks | Low | 72 | Fastest MVP |
   | **3** | **Disruptive** | **Contrarian** | **36/40** | **20 wks** | **High** | **92** ← | **Blue Ocean positioning** |
   | 4 | Premium | Best-in-class | 30/40 | 24 wks | Med | 88 | Comprehensive features |
   | 5 | Platform | Ecosystem | 34/40 | 32 wks | High | 85 | Network effects |

   ---

   ## How to Switch to a Different Variant

   If you prefer a different alternative:

   ```bash
   /speckit.concept.switch 5
   ```

   This will:
   1. Replace `specs/concept.md` with selected variant
   2. Update "Auto-Selected" banner
   3. Preserve all 5 alternatives in `specs/alternatives/`

   ---

   ## Detailed Variant Summaries

   ### Alternative 1: Conventional
   **Strategy**: Industry standard approach
   **Best For**: Low-risk market entry, competitive parity
   **Vision**: [Summary...]
   **Core Features**: [List 5-7 epics...]
   **Pros**: Market validation, established patterns, lower learning curve
   **Cons**: Limited differentiation, crowded space

   [Repeat for all 5 alternatives...]
   ```

   **CLI Output** (display to user, non-blocking):

   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ Concept Generation Complete (15 min 32s)

   Auto-selected: Alternative 3 - Disruptive (CQS: 92/100)

   Quick Comparison:
   | # | Alternative   | Strategy   | Score | MVP Time | Risk | CQS |
   |---|---------------|------------|:-----:|:--------:|:----:|:---:|
   | 1 | Conventional  | Standard   | 28/40 | 16 wks   | Med  | 78  |
   | 2 | Minimal       | 80/20      | 32/40 |  8 wks   | Low  | 72  |
   | 3 | **Disruptive**| Contrarian | 36/40 | 20 wks   | High | **92** ← SELECTED
   | 4 | Premium       | Best       | 30/40 | 24 wks   | Med  | 88  |
   | 5 | Platform      | Ecosystem  | 34/40 | 32 wks   | High | 85  |

   📁 Files Generated:
      - specs/concept.md (selected alternative)
      - specs/alternatives/01-conventional.md
      - specs/alternatives/02-minimal.md
      - specs/alternatives/03-disruptive.md
      - specs/alternatives/04-premium.md
      - specs/alternatives/05-platform.md
      - specs/concept-alternatives.md (comparison)
      - specs/next-steps.md (ready-to-execute commands) ← MANDATORY FILE
      - specs/quality-report.md (CQS breakdown)
      - specs/generation-summary.md (generation summary)

   ✅ VALIDATION PASSED:
      - specs/next-steps.md created and validated ({file_size_kb} KB)
      - {foundation_count} foundation stories generated (Wave 1: {wave1_count}, Wave 2: {wave2_count})
      - {total_stories} total stories across {epic_count} epics

   💡 Quick Start:
      cat specs/next-steps.md  # View execution strategies
      cat specs/quality-report.md  # Check quality metrics

   💡 To switch to a different variant: /speckit.concept.switch [1-5]

   Next steps:
      - Review concept: cat specs/concept.md
      - Choose strategy: cat specs/next-steps.md
      - Specify features: [copy command from next-steps.md]
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Concept generation complete. Review at your convenience.
   ```

   **No user interaction required** - Generation complete, proceed to done state.

4. **Transition: Discovery → Structure** (if Discovery Mode was used):

   **Synthesis step** before proceeding to structured capture:

   1. **Summarize discoveries** to user:
      - "Top problems validated: [list]"
      - "Key market gaps identified: [list]"
      - "Winning feature candidates: [list]"

   2. **Synthesize vision statement**:
      "Based on our discovery, here's the emerging concept:
      [draft vision statement combining problem + solution + differentiation]"

   3. **User confirmation**:
      "Does this capture your intent? Any adjustments before we structure the full concept?"

   4. After confirmation, proceed to Clarification Gate.

4b. **Clarification Gate** (NEW — before proceeding to Capture):

   **Goal**: Ensure sufficient clarity before writing concept. Prevents wasted effort on vague inputs.

   **Quality Import**:
   ```text
   IMPORT: templates/shared/quality/anti-slop.md
   APPLY specificity checks to all answers
   ```

   **Clarity Checklist** (must pass before proceeding):

   ```text
   CLARITY_CHECK = {
     target_user: {
       check: "Is target user specific? (persona ≠ 'users')",
       pass_examples: ["Marketing Manager at 50-200 employee B2B SaaS", "Solo indie hackers"],
       fail_examples: ["users", "businesses", "people who need X"]
     },
     core_problem: {
       check: "Is core problem specific? (not generic 'improve efficiency')",
       pass_examples: ["Spend 4+ hours/week copying data between tools", "Can't find relevant docs in 50K+ file repos"],
       fail_examples: ["inefficient processes", "need better workflow", "improve productivity"]
     },
     differentiation: {
       check: "Is differentiation articulated? (not 'better than competitors')",
       pass_examples: ["Only tool with native Figma integration", "10x faster via local-first architecture"],
       fail_examples: ["better UX", "more features", "easier to use"]
     },
     success_measurable: {
       check: "Is success measurable? (has concrete metrics)",
       pass_examples: ["Reduce time-to-first-report from 2 hours to 10 minutes", "Achieve 40% weekly active usage"],
       fail_examples: ["users are happy", "adoption increases", "efficiency improves"]
     }
   }

   FAILED_CHECKS = []
   FOR EACH check IN CLARITY_CHECK:
     IF check fails:
       FAILED_CHECKS.append(check)
   ```

   **If any check fails**, ask clarifying questions BEFORE proceeding:

   ```text
   MAX_QUESTIONS_PER_ROUND = 3  # Avoid overwhelming user

   CLARIFYING_QUESTION_TEMPLATES = {
     target_user: [
       "You mentioned '[vague term]' — can you be more specific?",
       "What's their job title? Company size? Industry?",
       "What does a typical day look like for this person?"
     ],
     core_problem: [
       "The problem is '[vague description]' — which specific process?",
       "What's the cost of this problem? (time/money/frustration)",
       "How do they solve this today? What's wrong with that approach?"
     ],
     differentiation: [
       "How is this different from [competitor]?",
       "What's the one thing competitors do wrong that you'll fix?",
       "Why would someone switch from their current solution?"
     ],
     success_measurable: [
       "How would you measure if this succeeds?",
       "What number would need to change for this to be worth it?",
       "What would users be able to do that they can't do today?"
     ]
   }

   # Select up to 3 most critical questions
   FOR i IN range(min(3, len(FAILED_CHECKS))):
     ASK question from CLARIFYING_QUESTION_TEMPLATES[FAILED_CHECKS[i]]

   WAIT for answers before proceeding
   UPDATE concept with clarified information
   RE-RUN clarity check
   ```

   **Gate Decision**:
   - **PASS (all checks green)**: Proceed to step 5 (Extract Vision)
   - **PARTIAL (1-2 checks fail)**: Ask clarifying questions, then proceed
   - **FAIL (3+ checks fail)**: Return to Discovery Mode (Phase 0a)

   **Output**: Document clarifications in "Assumptions & Clarifications" section.

4c. **Scope Variants (OPTIONAL)** — MOVED TO STEP 12:

   **NOTE**: Scope variant generation (MINIMAL/BALANCED/AMBITIOUS) has been moved to Step 12 and is now OPTIONAL.

   **Reason**: Product Alternatives (Phase 0d/0e) explore WHAT to build (different visions).
   Scope Variants explore HOW MUCH to build (different scope levels of same vision).

   **When Generated**:
   - OPTIONAL: Only if user requests with `--generate-variants` flag
   - OR: After concept complete, via `/speckit.concept-variants` command

   **See**: Step 12 for scope variant generation logic.
   **Reference**: `templates/shared/concept-sections/concept-variants.md`

5. **Extract Vision and Business Context**:

   **Priority Order**:
   1. **IF SELECTED_ALT exists** (from Phase 0e): Use selected alternative's vision
   2. **ELSE IF** clear user input (Capture Mode): Extract from user description
   3. **ELSE**: Use Discovery findings (Phase 0 outputs)

   **From Selected Alternative** (if Phase 0e ran):
   ```text
   # Use Alternative [N]'s components:
   - **Vision Statement**: Selected alternative's vision statement
   - **Core Features**: Expand selected alternative's 5-7 epics into full Feature Hierarchy
   - **Value Proposition**: Selected alternative's value proposition
   - **Differentiation**: Selected alternative's differentiation points
   - **Success Metrics**: Infer metrics from value proposition (what would prove this works?)

   # Document Selection:
   - Add "Product Alternatives" section to concept.md
   - Include selection rationale (why this alternative over others)
   - Reference full analysis in specs/concept-alternatives.md
   ```

   **From User Input** (Capture Mode, no alternatives generated):

   Parse the user description to identify:
   - **Vision Statement**: What is this? Who is it for? What problem does it solve?
   - **Problem Space**: Specific pain points being addressed
   - **Target Users**: Personas with Jobs-to-be-Done (JTBD)
   - **Success Metrics**: Business KPIs validated against SMART criteria

   For each element:
   - If clearly stated in input: Extract directly
   - If implied: Infer from context and document as assumption
   - If unclear: Use reasonable industry defaults (or use Discovery findings if available)

5-PR. **Amazon Working Backwards: PR/FAQ** — NEW:

   Define the customer experience before building by writing the launch press release:

   ```markdown
   ## Press Release (Draft — Launch Day Vision)

   **Headline**: [Product Name] Helps [Target Customer] [Achieve Outcome]

   **Problem**: [2-3 sentences on the pain point]

   **Solution**: [1 paragraph on how we solve it]

   **Customer Quote** (imagined):
   > "[How the product changed their workflow/life]"
   > — [Persona Name], [Role]

   **Getting Started**: [How customers begin using it]
   ```

   **Customer FAQ Example**:
   - "How is this different from [competitor]?" → [Differentiation]
   - "How long until I see value?" → [Time to value]

   **Internal FAQ Example**:
   - "Why build this now?" → [Market timing rationale]
   - "What are we NOT building?" → [Explicit scope exclusions]

   **Reference template**: `templates/shared/concept-sections/pr-faq.md`

5-TR. **Trade-off Resolution Framework** — NEW:

   Establish hierarchy for resolving competing priorities:

   ```markdown
   ## Trade-off Hierarchy

   When in conflict, prioritize in this order:
   1. **Safety & Security** > everything (never compromise)
   2. **User Value** > internal convenience
   3. **Simplicity** > features (remove before adding)
   4. **Speed** > perfection (ship MVP, iterate)
   5. **Reversible decisions** > extensive analysis

   ## This Concept's Key Trade-offs
   | Trade-off | Options | Our Choice | Rationale |
   |-----------|---------|:----------:|-----------|
   | Speed vs Quality | [Fast/Polished] | [Choice] | [Why] |
   | Features vs Simplicity | [Full/Core] | [Choice] | [Why] |
   | Build vs Buy | [Custom/3rd party] | [Choice] | [Why] |
   ```

   **Connected to**: Constitution principles, Decision Log

   **Reference template**: `templates/shared/concept-sections/tradeoff-resolution.md`

5a. **Deep Persona Framework (JTBD-Enhanced)** — NEW:

   For each identified persona, capture Jobs-to-be-Done:

   ```markdown
   ### Persona: [Name] — [Role]

   #### Demographics
   - **Segment**: [B2B SMB / B2B Enterprise / B2C Consumer / B2C Prosumer]
   - **Tech Comfort**: [Low / Medium / High]
   - **Frequency of Use**: [Daily / Weekly / Monthly / One-time]

   #### Jobs-to-be-Done
   | Job Type | When I... | I want to... | So I can... |
   |----------|-----------|--------------|-------------|
   | Functional | [situation] | [action] | [outcome] |
   | Emotional | [situation] | [feel] | [state] |
   | Social | [situation] | [appear] | [perception] |

   #### Willingness to Pay
   - **Current spend on alternatives**: $[X]/mo
   - **Pain severity**: [1-10]
   - **Switching cost tolerance**: [Low/Med/High]

   #### Success Criteria
   - **Must have**: [non-negotiable outcomes]
   - **Nice to have**: [delighters]
   - **Deal breaker**: [instant churn triggers]
   ```

   **Minimum requirement**: At least 2 personas with JTBD defined.

   **Reference template**: `templates/shared/concept-sections/persona-jtbd.md`

5aa. **Success Metrics Framework (SMART + OKRs)** — NEW:

   Validate all success metrics against SMART criteria:

   ```markdown
   ## Success Metrics

   ### North Star Metric
   **[Metric Name]**: [Definition]
   - **Why this metric?**: [connects user value to business value]
   - **Leading indicators**: [predictive metrics]
   - **Lagging indicators**: [outcome metrics]

   ### Metric Quality Validation
   | Metric | S | M | A | R | T | Score |
   |--------|:-:|:-:|:-:|:-:|:-:|:-----:|
   | [metric] | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | X/5 |

   **Legend**: S=Specific, M=Measurable, A=Achievable, R=Relevant, T=Time-bound

   ### OKR Structure (if applicable)
   **Objective**: [qualitative goal]
   - **KR1**: [quantitative result] — [baseline → target]
   - **KR2**: [quantitative result] — [baseline → target]
   ```

   **Validation rule**: Metrics with score < 4/5 should be refined before specification.

   **Reference template**: `templates/shared/concept-sections/metrics-smart.md`

5ab. **Business Model Canvas** — NEW:

   Visualize the complete business model to ensure value creation and capture coherence:

   ```markdown
   ## Business Model Canvas Summary

   | Component | Description |
   |-----------|-------------|
   | **Customer Segments** | [Who we serve — primary, secondary] |
   | **Value Propositions** | [What value we deliver — by segment] |
   | **Channels** | [How we reach customers — awareness → purchase → delivery] |
   | **Customer Relationships** | [Relationship type — self-serve / assisted / dedicated] |
   | **Revenue Streams** | [How we make money — pricing model, billing] |
   | **Key Resources** | [What we need — people, IP, infrastructure] |
   | **Key Activities** | [What we do — product, acquisition, operations] |
   | **Key Partnerships** | [Who helps us — suppliers, integrations, distribution] |
   | **Cost Structure** | [What we spend — fixed, variable, drivers] |

   ## Unit Economics
   | Metric | Current | Target | Benchmark |
   |--------|:-------:|:------:|:---------:|
   | CAC (Customer Acquisition Cost) | $[X] | $[X] | $[X] |
   | LTV (Lifetime Value) | $[X] | $[X] | $[X] |
   | LTV:CAC Ratio | [X]:1 | 3:1+ | 3:1 |
   | Payback Period | [X] mo | <12 mo | 12-18 mo |
   ```

   **Validation rule**: LTV:CAC ratio < 2:1 is a red flag — reconsider pricing or CAC.

   **Reference template**: `templates/shared/concept-sections/business-model-canvas.md`

5ab-IT. **Investment Thesis (Board-Ready)** — NEW:

   Articulate a compelling, evidence-based investment case for executives and investors:

   ```markdown
   ## Investment Thesis

   ### Executive Summary
   | Element | Description |
   |---------|-------------|
   | **Opportunity** | [Market opportunity size in $ — reference TAM/SAM/SOM] |
   | **Solution** | [One-sentence description of what we're building] |
   | **Moat** | [Sustainable competitive advantage — why we win] |
   | **Ask** | [Investment required: $X over Y months] |
   | **Return** | [Expected ROI / multiples / payback period] |

   ### Key Assumptions
   | Assumption | Evidence | Confidence | Sensitivity |
   |------------|----------|:----------:|:-----------:|
   | [Market size] | [Source] | H/M/L | High/Med/Low |
   | [Growth rate] | [Source] | H/M/L | High/Med/Low |

   ### Risk-Adjusted Returns
   | Scenario | Probability | Revenue Y3 | NPV | Key Drivers |
   |----------|:-----------:|:----------:|:---:|-------------|
   | Upside | [X]% | $[X]M | $[X]M | [Key assumption exceeds] |
   | Base | [X]% | $[X]M | $[X]M | [Plan execution] |
   | Downside | [X]% | $[X]M | $[X]M | [Key risk materializes] |
   ```

   **Purpose**: This is the "one-pager" that answers "Why should we invest?"
   **Minimum requirement**: Executive summary table + 3 scenarios + 5 key assumptions.

   **Reference template**: `templates/shared/concept-sections/investment-thesis.md`

5ab-SA. **Strategic Alternatives Analysis (Build/Buy/Partner)** — NEW:

   Evaluate all options before committing to "Build":

   ```markdown
   ## Strategic Alternatives

   ### Options Comparison
   | Option | Description | Pros | Cons | Est. Cost | Time |
   |--------|-------------|------|------|:---------:|:----:|
   | **BUILD** | Internal development | Control, IP | Time, risk | $[X] | [X]mo |
   | **BUY** | Acquire capability | Speed | Integration | $[X] | [X]mo |
   | **PARTNER** | Strategic alliance | Speed, low cost | Dependency | $[X] | [X]mo |
   | **NOTHING** | Status quo | No cost | Opportunity cost | $0 | — |

   ### Weighted Decision Matrix
   | Criterion | Weight | BUILD | BUY | PARTNER | NOTHING |
   |-----------|:------:|:-----:|:---:|:-------:|:-------:|
   | Speed to market | 25% | 2 | 4 | 3 | 1 |
   | Strategic fit | 30% | 5 | 3 | 3 | 1 |
   | Total cost | 20% | 2 | 1 | 4 | 5 |
   | Risk | 25% | 2 | 2 | 3 | 4 |
   | **SCORE** | 100% | [X] | [X] | [X] | [X] |

   **Recommendation**: [Option] because [rationale]
   ```

   **Purpose**: Justify "Build" decision to board — show alternatives were considered.

   **Reference template**: `templates/shared/concept-sections/strategic-alternatives.md`

5ab-FS. **Financial Sensitivity Analysis** — NEW:

   Stress-test financial assumptions with NPV/IRR calculations:

   ```markdown
   ## Financial Sensitivity

   ### NPV Calculation
   | Scenario | Revenue Y1 | Revenue Y3 | NPV | IRR |
   |----------|:----------:|:----------:|:---:|:---:|
   | Base | $[X] | $[X] | $[X] | [X]% |
   | Optimistic (+20%) | $[X] | $[X] | $[X] | [X]% |
   | Pessimistic (-20%) | $[X] | $[X] | $[X] | [X]% |

   ### Sensitivity Table (NPV impact)
   | Variable | -20% | -10% | Base | +10% | +20% |
   |----------|:----:|:----:|:----:|:----:|:----:|
   | Market size | ($X) | ($X) | $X | $X | $X |
   | Conversion rate | ($X) | ($X) | $X | $X | $X |
   | ARPU | ($X) | ($X) | $X | $X | $X |
   | CAC | ($X) | ($X) | $X | $X | $X |

   ### Break-Even Analysis
   - Units to break even: [X]
   - Revenue to break even: $[X]
   - Months to break even: [X]
   ```

   **Purpose**: Identify which assumptions have highest impact on returns.

   **Reference template**: `templates/shared/concept-sections/financial-sensitivity.md`

5b. **Extract UX Foundation Layer**:

   Generate foundation features based on detected project type.

   **CRITICAL PRE-CHECK**:

   Before loading foundation scenarios, verify catalog file exists:

   ```bash
   # Check file existence
   FILE_PATH=".specify/memory/knowledge/frameworks/ux-foundations.md"

   if [ ! -f "$FILE_PATH" ]; then
     echo "❌ CRITICAL ERROR: Foundation catalog missing"
     echo "   Expected: $FILE_PATH"
     echo "   This file is required for foundation layer generation."
     echo ""
     echo "   Resolution:"
     echo "   1. Ensure you initialized project with: specify init <project>"
     echo "   2. Verify .specify/memory/knowledge/frameworks/ directory exists"
     echo "   3. Re-run /speckit.concept after restoring catalog"
     exit 1
   fi
   ```

   **IF file missing**: HALT execution, show error to user, request re-initialization

   **IF file exists**: Continue with foundation extraction as documented

   ```text
   # Load foundation scenarios from catalog
   READ memory/knowledge/frameworks/ux-foundations.md

   FOR EACH foundation in REQUIRED_FOUNDATIONS:
     1. Load scenario definitions (UXF-xxx IDs)
     2. Generate corresponding Epic/Feature/Story entries:
        - AUTH → EPIC-001 User Access
          - F01 Registration (UXF-AUTH-001, UXF-AUTH-002)
          - F02 Session Management (UXF-AUTH-003, UXF-AUTH-004)
        - ERROR → Infrastructure layer (cross-cutting)
        - LAYOUT → Infrastructure layer (cross-cutting)
        - NAV → Feature in EPIC-001 or separate EPIC
        - FTUE → EPIC for Onboarding
        - FEEDBACK → Infrastructure layer (cross-cutting)

     3. Assign Wave:
        - Wave 1: AUTH, LAYOUT, ERROR (core infrastructure)
        - Wave 2: NAV, FTUE, FEEDBACK (user experience)

     4. Auto-set priority:
        - Wave 1 foundations → P1a (always highest priority)
        - Wave 2 foundations → P1b

     5. Mark in "UX Foundation Layer" section of concept.md
   ```

   **POST-GENERATION VALIDATION**:

   After generating foundation Epic/Features/Stories, validate output:

   ```text
   VALIDATE Foundation Generation:
   1. Count generated foundations
   2. Verify minimum set present (AUTH, ERROR, LAYOUT for Web/Mobile/Desktop)
   3. Verify each foundation has Epic-XXX.FXX.SXX story IDs
   4. Verify Wave assignments (Wave 1: AUTH/ERROR/LAYOUT, Wave 2: NAV/FEEDBACK/ADMIN/INTEGRATION)
   5. Verify Priority assignments (Wave 1 → P1a, Wave 2 → P1b)

   MINIMUM_FOUNDATIONS = {
     "Web SPA": ["AUTH", "ERROR", "LAYOUT"],
     "Web SSR": ["AUTH", "ERROR", "LAYOUT"],
     "Mobile": ["AUTH", "ERROR", "LAYOUT"],
     "Desktop": ["AUTH", "ERROR", "LAYOUT"],
     "CLI": ["ERROR", "HELP"],
     "API": ["AUTH", "ERROR"],
     "Service": ["ERROR", "HEALTH"]
   }

   IF generated_count < MINIMUM_FOUNDATIONS[project_type]:
     HALT with error:
     "❌ Foundation generation incomplete. Expected {MINIMUM_FOUNDATIONS[project_type]} but got {generated_list}"
     "   Check ux-foundations.md for project type '{project_type}'"

   IF any foundation missing story IDs:
     HALT with error:
     "❌ Foundation {name} has no story IDs. Generation failed at Epic/Feature/Story creation step."
   ```

   **Success criteria**:
   - ✅ Minimum foundations generated
   - ✅ Each foundation has ≥1 story ID
   - ✅ Wave assignments correct
   - ✅ Priority assignments correct

   **On failure**: HALT, show diagnostic info, request retry

   **Output**:
   - Populate "UX Foundation Layer" section with detected foundations
   - Generate foundation Epic/Features/Stories BEFORE user-defined features
   - Set up "Foundation Scenarios" mapping table

5b-PM. **Pre-Mortem Analysis** — NEW:

   Imagine failure before it happens to identify preventable scenarios:

   ```markdown
   ## Pre-Mortem Analysis

   *"It's 12 months from now. This product has failed. What went wrong?"*

   ### FAIL-001: [Failure Mode Name]
   **Probability**: HIGH | MEDIUM | LOW
   **Impact**: CRITICAL | MAJOR | MINOR

   **Failure Story**: [Narrative of how this failure unfolds]

   **Early Warning Signs**:
   - [ ] [Metric dropping below X]
   - [ ] [User feedback pattern]
   - [ ] [Competitive move]

   **Prevention Strategy**:
   | Action | Owner | Timeline |
   |--------|:-----:|:--------:|
   | [Preventive measure] | [Name] | [When] |

   **Kill Criteria**: IF [metric] < [threshold] BY [date], THEN [pivot/kill]
   ```

   **Purpose**: Identify preventable failures and establish early warning systems.
   **Minimum requirement**: Document at least 3 failure scenarios with prevention strategies.

   **Reference template**: `templates/shared/concept-sections/pre-mortem.md`

5c. **Risk Assessment Matrix** — NEW:

   Identify and document execution risks before detailed planning:

   ```markdown
   ## Risk Assessment

   ### Execution Risks
   | Risk | Likelihood | Impact | L×I | Mitigation | Contingency |
   |------|:----------:|:------:|:---:|------------|-------------|
   | [Risk 1] | [1-5] | [1-5] | [X] | [Proactive action] | [If it happens...] |
   | [Risk 2] | [1-5] | [1-5] | [X] | [Proactive action] | [If it happens...] |
   | [Risk 3] | [1-5] | [1-5] | [X] | [Proactive action] | [If it happens...] |

   ### Dependency Failure Scenarios
   | Dependency | If unavailable... | Fallback | Cost of fallback |
   |------------|-------------------|----------|------------------|
   | [service/API] | [impact] | [alternative] | [effort/time] |

   ### Pivot Criteria
   - **Pivot if**: [condition 1], [condition 2]
   - **Pivot to**: [alternative direction]
   - **Kill if**: [condition that proves thesis invalid]
   ```

   **Risk scoring**: Likelihood × Impact. Address risks with score ≥ 12 first.

   **Minimum requirement**: At least 3 risks with mitigations documented.

   **Reference template**: `templates/shared/concept-sections/risk-matrix.md`

5c-SP. **Scenario Planning (Shell/McKinsey 2×2)** — NEW:

   Map possible futures to build robust strategies:

   ```markdown
   ## Scenario Planning Matrix

   ### Uncertainty Axes
   - **X-axis**: [Key uncertainty 1, e.g., Market growth: Slow ↔ Fast]
   - **Y-axis**: [Key uncertainty 2, e.g., Competition: Fragmented ↔ Consolidated]

   ### Four Futures
   | Scenario | Quadrant | Probability | Strategy | Early Warning |
   |----------|----------|:-----------:|----------|---------------|
   | **Best Case** | Fast + Fragmented | [X]% | Aggressive expansion | [Signal] |
   | **Niche Win** | Slow + Fragmented | [X]% | Deep specialization | [Signal] |
   | **Race** | Fast + Consolidated | [X]% | Speed + partnerships | [Signal] |
   | **Survival** | Slow + Consolidated | [X]% | Efficiency, pivots | [Signal] |

   ### Robust Strategies
   [Strategies that work across 3+ scenarios]
   ```

   **Purpose**: Prepare for multiple futures instead of betting on one forecast.

   **Reference template**: `templates/shared/concept-sections/scenario-planning.md`

5c-SO. **Strategic Options Valuation (Real Options)** — NEW:

   Value flexibility and optionality in the investment:

   ```markdown
   ## Strategic Options

   ### Option Inventory
   | Option Type | Description | Trigger | Value | Cost to Maintain |
   |-------------|-------------|---------|:-----:|:----------------:|
   | **Expand** | Scale to new markets | Revenue > $X | $[X]M | $[X]K/yr |
   | **Delay** | Wait for market clarity | If uncertainty > Y | $[X]M | Opportunity cost |
   | **Abandon** | Exit gracefully | If loss > $X | $[X]M | Sunk costs only |
   | **Pivot** | Change direction | If hypothesis invalid | $[X]M | $[X]K/yr |
   | **Stage** | Phased investment | Each milestone | $[X]M | Minimal |

   ### Total Option Value
   NPV of base case: $[X]M
   + Value of options: $[X]M
   = **Total project value**: $[X]M
   ```

   **Purpose**: Justify "Build" over "Buy" by quantifying flexibility value.

   **Reference template**: `templates/shared/concept-sections/strategic-options.md`

5c-EC. **Execution Confidence Matrix** — NEW:

   Assess organizational readiness to execute:

   ```markdown
   ## Execution Confidence Assessment

   ### Confidence by Domain
   | Domain | Score | Evidence | Key Risks |
   |--------|:-----:|----------|-----------|
   | **Technology** | 🟢/🟡/🔴 | [Track record] | [Gap] |
   | **Go-to-Market** | 🟢/🟡/🔴 | [Experience] | [Gap] |
   | **Operations** | 🟢/🟡/🔴 | [Capacity] | [Gap] |
   | **Team** | 🟢/🟡/🔴 | [Skills match] | [Gap] |
   | **Capital** | 🟢/🟡/🔴 | [Runway] | [Gap] |

   ### Greenlight Criteria (Google-style)
   - [ ] Tech lead assigned with relevant experience
   - [ ] Prototype validates core assumption
   - [ ] GTM channel identified and tested
   - [ ] 12-month runway secured
   - [ ] Team alignment confirmed (>80% buy-in)

   **Overall Confidence**: 🟢 HIGH | 🟡 MEDIUM | 🔴 LOW
   ```

   **Purpose**: Surface capability gaps before committing resources.

   **Reference template**: `templates/shared/concept-sections/execution-confidence.md`

5c-PC. **Portfolio Context** — NEW:

   Position this concept within the broader investment portfolio:

   ```markdown
   ## Portfolio Positioning

   ### Strategic Fit
   | Dimension | Assessment |
   |-----------|------------|
   | **Core vs Adjacent vs Transform** | [Category] |
   | **Horizon** | H1 (0-12mo) / H2 (12-24mo) / H3 (24+mo) |
   | **Investment Theme** | [Which strategic priority this serves] |

   ### Resource Allocation
   | Resource | This Concept | Portfolio Total | % of Total |
   |----------|:------------:|:---------------:|:----------:|
   | Budget | $[X]M | $[X]M | [X]% |
   | Headcount | [N] FTE | [N] FTE | [X]% |
   | Exec Attention | [H/M/L] | — | — |

   ### Cannibalization Analysis
   | Existing Product | Impact | Mitigation |
   |------------------|:------:|------------|
   | [Product A] | -[X]% revenue | [Strategy] |

   ### Synergies
   | With Product | Synergy Type | Value |
   |--------------|--------------|:-----:|
   | [Product B] | Shared infrastructure | $[X]K/yr saved |
   ```

   **Purpose**: Enable portfolio-level capital allocation decisions.

   **Reference template**: `templates/shared/concept-sections/portfolio-context.md`

5c-ES. **Ecosystem Strategy Canvas** — NEW:

   Map platform/partnership strategy for network effects:

   ```markdown
   ## Ecosystem Strategy

   ### Ecosystem Map
   | Role | Players | Value Exchange | Our Strategy |
   |------|---------|----------------|--------------|
   | **Core Platform** | [Us] | [Value delivered] | [Build/Operate] |
   | **Complementors** | [Partners] | [Value exchange] | [Enable/Integrate] |
   | **Customers** | [Segments] | [Value received] | [Acquire/Retain] |
   | **Suppliers** | [Vendors] | [Inputs] | [Contract/Partner] |

   ### Partner Economics
   | Partner Type | Revenue Share | Integration Cost | Break-Even |
   |--------------|:-------------:|:----------------:|:----------:|
   | [Type A] | [X]% | $[X]K | [X] months |

   ### API Strategy
   | API Tier | Access | Pricing | Purpose |
   |----------|--------|:-------:|---------|
   | Public | Open | Free | Adoption |
   | Standard | Registered | $[X]/mo | Monetization |
   | Enterprise | Contracted | Custom | Strategic |
   ```

   **Purpose**: Design for network effects and platform dynamics.

   **Reference template**: `templates/shared/concept-sections/ecosystem-strategy.md`

5c-HTL. **Hypothesis Testing Log (OpenAI-Style)** — NEW:

   Track assumptions systematically with evidence:

   ```markdown
   ## Hypothesis Testing Log

   ### HYP-001: [Hypothesis Title]
   **Type**: DESIRABILITY | FEASIBILITY | VIABILITY

   **Statement**: We believe that [specific user segment] will [behavior] because [rationale].

   **Test Method**:
   - [ ] User interviews (n=10+)
   - [ ] Landing page conversion (>5%)
   - [ ] Prototype testing
   - [ ] Market research

   **Success Criteria**:
   | Metric | Target | Minimum Viable |
   |--------|:------:|:--------------:|
   | Quantitative | [e.g., >40% intent to pay] | [e.g., >25%] |
   | Qualitative | [e.g., 8/10 say "critical"] | [e.g., 6/10] |

   **Evidence Collected**:
   | Date | Method | Sample | Result | Confidence |
   |:----:|--------|:------:|--------|:----------:|
   | MM/DD | Interview | n=12 | 9/12 validated | HIGH |

   **Status**: ✅ Validated | ⚠️ Partially | ❌ Invalidated | 🔄 Testing

   **Implications**: [What changes based on evidence]
   ```

   **Purpose**: Validate assumptions before investing in build.
   **Minimum requirement**: At least 3 hypotheses (1 Desirability, 1 Feasibility, 1 Viability).

   **Reference template**: `templates/shared/concept-sections/hypothesis-testing.md`

5c-AIR. **AI Responsibility Assessment** — NEW (if applicable):

   *Required for concepts with AI/ML components. Skip if no AI functionality.*

   ```markdown
   ## AI Responsibility Assessment

   ### Bias & Fairness
   - [ ] Training data sources reviewed for bias
   - [ ] Performance tested across demographic groups
   - [ ] Disparate impact analysis completed

   ### Transparency
   - [ ] AI involvement clearly disclosed to users
   - [ ] Confidence levels communicated
   - [ ] Human override available

   ### Privacy
   - [ ] Data minimization applied
   - [ ] User consent mechanisms in place
   - [ ] Right to deletion implemented

   ### Safety
   - [ ] Failure modes identified
   - [ ] Graceful degradation designed
   - [ ] Human-in-the-loop for critical decisions
   ```

   **Purpose**: Ensure responsible AI development with appropriate safeguards.

   **Reference template**: `templates/shared/concept-sections/ai-responsibility.md`

5c-DL. **Decision Log (Stripe-Style)** — NEW:

   Document key decisions with rationale to enable pivots and preserve knowledge:

   ```markdown
   ## Decision Log

   ### DEC-001: [Decision Title]
   **Date**: YYYY-MM-DD | **Status**: Decided | **Owner**: [Name]

   **Context**: [What prompted this decision]

   **Options Considered**:
   | Option | Pros | Cons | Effort |
   |:------:|------|------|:------:|
   | **A** | [Benefits] | [Drawbacks] | [S/M/L] |
   | **B** | [Benefits] | [Drawbacks] | [S/M/L] |
   | **C** | Do nothing | [Opportunity cost] | — |

   **Decision**: [Option X]
   **Rationale**: [Why this choice, with evidence]
   **Reversibility**: [Type 1 (hard) / Type 2 (easy)]
   **Review Trigger**: Revisit if [condition]
   ```

   **Minimum requirement**: Document at least 3 key decisions with alternatives considered.

   **Reference template**: `templates/shared/concept-sections/decision-log.md`

5d. **Technical Discovery Hints** — NEW:

   Surface architectural considerations early to reduce surprises during planning:

   ```markdown
   ## Technical Discovery

   ### Domain Entities (Sketch)
   | Entity | Key Attributes | Relationships | Persistence |
   |--------|----------------|---------------|-------------|
   | User | id, email, role | → Account, → Sessions | PostgreSQL |
   | [Entity] | [attrs] | [relations] | [store] |

   ### API Surface Estimation
   | Domain | Operations | Auth Required | External Integration |
   |--------|------------|:-------------:|---------------------|
   | Users | CRUD + search | ✓ | SSO providers |
   | [Domain] | [ops] | ✓/✗ | [integrations] |

   ### Integration Complexity
   | External System | Protocol | Complexity | Risk |
   |-----------------|----------|:----------:|------|
   | [system] | REST/GraphQL | Low/Med/High | [notes] |

   ### Constitution Principle Conflicts
   | Feature | Principle | Conflict | Resolution |
   |---------|-----------|----------|------------|
   | [feature] | [ID] | [what conflicts] | [how to resolve] |
   ```

   **Purpose**: Identify potential blockers and architectural decisions before specification.

   **Reference template**: `templates/shared/concept-sections/technical-hints.md`

5d-MO. **MOALS/OSM Framework (Amazon Operating Model)** — NEW:

   Define operational mechanisms for sustainable execution:

   ```markdown
   ## Amazon MOALS Framework

   ### Mechanisms (Self-Reinforcing Systems)
   | Mechanism | Description | Owner | Cadence |
   |-----------|-------------|:-----:|:-------:|
   | [Weekly Business Review] | Review metrics, identify issues | [Role] | Weekly |
   | [Customer Obsession Review] | Review customer feedback trends | [Role] | Bi-weekly |
   | [Operational Excellence Review] | Process improvements | [Role] | Monthly |

   ### Outputs (Observable Results)
   | Output | Metric | Current | Target | Owner |
   |--------|--------|:-------:|:------:|:-----:|
   | [Customer Satisfaction] | NPS | [X] | [X] | [Role] |
   | [Operational Efficiency] | [Metric] | [X] | [X] | [Role] |

   ### Actions (Daily Operations)
   | Action | Trigger | SLA | Escalation |
   |--------|---------|:---:|------------|
   | [Customer inquiry response] | Inbound ticket | <4h | Manager at 6h |
   | [Incident triage] | Alert fired | <15m | On-call chain |

   ### Learning Systems (Flywheel)
   | Flywheel Component | Input | Output | Metric |
   |--------------------|-------|--------|--------|
   | [Customer Feedback] | Surveys, tickets | Product improvements | Time-to-fix |
   | [A/B Testing] | Experiment ideas | Validated learnings | Win rate |

   ### Systems (Infrastructure)
   | System | Purpose | Owner | Health Check |
   |--------|---------|:-----:|--------------|
   | [Monitoring] | Observability | [Team] | [Dashboard] |
   | [Data Pipeline] | Analytics | [Team] | [Dashboard] |
   ```

   **Purpose**: Build sustainable operational excellence from day one.
   **Origin**: Amazon's internal operating system that powers 6-pagers and WBRs.

   **Reference template**: `templates/shared/concept-sections/moals-osm.md`

6. **Build Feature Hierarchy**:

   Analyze the user description to identify capabilities and organize them:

   ```text
   FOR EACH capability mentioned:
     1. Classify as Epic (large area) or Feature (specific functionality)
     2. If capability is too large for single Feature:
        - Create Epic containing multiple Features
     3. Break each Feature into user-facing Stories
     4. Assign hierarchical IDs: EPIC-NNN.FNN.SNN
     5. Assign initial priority based on:
        - Explicitly stated priority from user
        - Dependency order (foundations first)
        - User value (core journey enablers higher)
   ```

   **ID Format Rules**:
   - Epic: `EPIC-001`, `EPIC-002`, etc.
   - Feature: `EPIC-001.F01`, `EPIC-001.F02`, etc.
   - Story: `EPIC-001.F01.S01`, `EPIC-001.F01.S02`, etc.

   **Priority Format**:
   - `P1a`, `P1b`, `P1c`: MVP critical path (ordered sequence)
   - `P2a`, `P2b`: Important but post-MVP
   - `P3`: Nice-to-have, future enhancements

6a. **Scope Exclusions ("What We're NOT Building")** — NEW:

   Explicitly define what is out of scope to prevent scope creep and align expectations:

   ```markdown
   ## Explicit Non-Goals (v1.0)

   ### Features We Are NOT Building
   | Feature/Capability | Why Excluded | Alternative for Users | Revisit When |
   |-------------------|--------------|----------------------|--------------|
   | [Feature X] | [Strategic reason] | [Workaround or competitor] | [Trigger condition] |

   ### Segments We Are NOT Serving
   | Segment | Why Excluded | Risk if We Try | Revisit When |
   |---------|--------------|----------------|--------------|
   | [Segment] | [Focus reason] | [Dilution risk] | [Scale milestone] |

   ## Scope Guardrails
   Before adding ANY feature, it must pass ALL gates:
   - [ ] JTBD Alignment: Directly supports primary Jobs-to-be-Done
   - [ ] User Evidence: >30% of target users explicitly need it
   - [ ] Effort Justified: Can be built in <[X] weeks
   - [ ] Simplicity Preserved: Doesn't compromise core UX
   - [ ] Strategic Fit: Aligns with Blue Ocean positioning

   ## Rejected Alternatives
   | Alternative | Why Considered | Why Rejected | Reconsider If |
   |-------------|----------------|--------------|---------------|
   | [Approach X] | [Reason] | [Rationale] | [Trigger] |
   ```

   **Purpose**: Enable confident "no" to feature requests and preserve strategic focus.
   **Minimum requirement**: Document at least 5 explicit non-goals with rationale.

   **Reference template**: `templates/shared/concept-sections/scope-exclusions.md`

6b. **Three Horizons Framework (McKinsey)** — NEW:

   Allocate features across innovation horizons to balance execution with growth:

   ```markdown
   ## Three Horizons Resource Allocation

   | Horizon | Time Frame | Focus | Resource % | Features |
   |:-------:|:----------:|-------|:----------:|----------|
   | **H1** | 0-12 mo | Defend & extend core | **70%** | [MVP features, P1 priorities] |
   | **H2** | 12-24 mo | Scale emerging opportunities | **20%** | [P2 features, new segments] |
   | **H3** | 24-36+ mo | Create future options | **10%** | [P3 exploration, R&D bets] |

   ## Horizon Assignment
   | Feature ID | Horizon | Rationale |
   |------------|:-------:|-----------|
   | EPIC-001.F01 | H1 | Core MVP, revenue protection |
   | EPIC-002.F03 | H2 | New market segment entry |
   | EPIC-003.F01 | H3 | Exploratory AI capability |
   ```

   **Promotion Criteria**: H3 → H2 when validated; H2 → H1 when proven unit economics
   **Kill Criteria**: No progress after 2 stage-gates (H2) or no learning after X months (H3)

   **Reference template**: `templates/shared/concept-sections/three-horizons.md`

6c. **Document Feature Selection Rationale** (NEW — Transparency Enhancement):

   **Goal**: For each feature, document WHY it was included, alternatives considered, and JTBD link.
   This eliminates "black box" feature selection.

   **Reference template**: `templates/shared/concept-sections/selection-rationale.md`

   ```text
   FOR EACH feature in Feature Hierarchy:
     1. Assign Selection ID: SEL-NNN (sequential)

     2. Document JTBD Link (REQUIRED):
        - Primary JTBD this feature enables
        - Format: JTBD-FUNC-001, JTBD-EMOT-001, JTBD-SOC-001

     3. Document Selection Decision:
        - INCLUDE: Feature selected for concept
        - EXCLUDE: Deliberately not building (move to 6a Scope Exclusions)
        - DEFER: Not in this version (document when to reconsider)

     4. Document Alternatives Analyzed (min 2 for P1a features):
        | Alternative | Score | Pros | Cons | Why Not Chosen |
        |-------------|:-----:|------|------|----------------|

     5. Assign Variant:
        - ALL: Included in MINIMAL, BALANCED, AMBITIOUS
        - MINIMAL+: Included in MINIMAL and above
        - BALANCED+: Included in BALANCED and above
        - AMBITIOUS: Only in AMBITIOUS variant

     6. Assess Reversibility:
        - Type 1: Irreversible, locked-in (careful!)
        - Type 2: Reversible, can change later (preferred for MVP)
   ```

   **Output for Feature Selection Rationale section**:

   ```markdown
   ### Selection Decision Table

   | ID | Feature | Decision | Variant | JTBD | Alternatives | Why This Choice |
   |:--:|---------|:--------:|:-------:|------|--------------|-----------------|
   | SEL-001 | [Name] | INCLUDE | ALL | JTBD-FUNC-001 | [Alt 1], [Alt 2] | [Rationale] |
   | SEL-002 | [Name] | INCLUDE | BALANCED+ | JTBD-FUNC-002 | [Alt] | [Rationale] |
   | SEL-003 | [Name] | EXCLUDE | — | JTBD-EMOT-001 | [Alt] | [Rationale] |

   ### JTBD Coverage Analysis

   | JTBD ID | Job Description | Features Addressing | Coverage | Gap Action |
   |---------|-----------------|---------------------|:--------:|------------|
   | JTBD-FUNC-001 | [Job] | F01, F02 | FULL | — |
   | JTBD-FUNC-002 | [Job] | — | GAP | Deferred to H2 |
   ```

   **Validation Rules**:
   - Every feature MUST have a JTBD link (CQS penalty if missing)
   - Every primary JTBD MUST have at least one feature addressing it
   - P1a features MUST have 2+ alternatives documented

7. **Map User Journeys**:

   Identify end-to-end flows that cross features:

   ```text
   FOR EACH user persona:
     1. Identify primary goal they want to achieve
     2. Map the steps to achieve that goal
     3. Link each step to Feature IDs
     4. Document edge cases per journey
     5. Note where journeys share features (integration points)
   ```

7b. **Scenario Completeness Validation**:

   Validate each non-foundation story has complete context.

   ```text
   COMPLETENESS_CHECKS = {
     "Entry Point": "How does user navigate here?",
     "Auth Context": "GUEST | AUTHENTICATED | ADMIN?",
     "Error Handling": "What if the action fails?",
     "Exit Point": "Where does user go after success?"
   }

   FOR EACH story in Feature Hierarchy:
     IF story.wave >= 3:  # Non-foundation story
       FOR EACH check in COMPLETENESS_CHECKS:
         IF check not documented:
           WARN: "Story {story.id} missing: {check}"

   # Generate completeness table
   | Story ID | Entry Point | Auth | Error | Exit | Complete? |
   |----------|-------------|------|-------|------|-----------|
   | EPIC-002.F01.S01 | Nav menu | AUTH | Shows error toast | Returns to list | ✓ |
   | EPIC-002.F01.S02 | Direct link | AUTH | ? | ? | ⚠ INCOMPLETE |
   ```

   **Output**:
   - List of incomplete stories with missing fields
   - Recommendation: "Complete scenario context before specification"

7c. **Generate Golden Path**:

   Create J000 journey that validates Wave 1-2 completion.

   ```text
   GOLDEN_PATH_TEMPLATE = [
     "[Guest] Views home page → LAYOUT",
     "[Guest] Clicks Sign Up → NAV",
     "[Guest] Registers account → AUTH",
     "[User] Completes onboarding → FTUE",
     "[User] Performs first action → First P1a feature",
     "[User] Sees confirmation → FEEDBACK"
   ]

   FOR EACH step in GOLDEN_PATH_TEMPLATE:
     1. Find matching feature in hierarchy
     2. Link to Feature ID
     3. Note Wave number
     4. Set status = [ ] (pending)

   ADD to "Execution Order" section as "Golden Path"
   ```

8. **Document Cross-Feature Dependencies**:

   Build dependency matrix:

   ```text
   FOR EACH Feature:
     1. Identify: What must be built BEFORE this feature?
     2. Identify: What does this feature BLOCK?
     3. Note integration points and shared entities
   ```

   Generate Mermaid diagram for visual representation.

8b. **Foundation Layer Detection (Pattern-Based)**:

   Identify user-defined features that ARE foundations (even if not from catalog).

   ```text
   FOUNDATION_PATTERNS = {
     "AUTH": ["auth*", "login*", "signin*", "signup*", "register*", "session*", "oauth*", "sso*"],
     "USER_MGMT": ["user*", "account*", "profile*", "permission*", "role*", "member*"],
     "CORE_DATA": ["schema*", "database*", "migration*", "model*", "entity*"],
     "INFRASTRUCTURE": ["config*", "env*", "logging*", "error*", "monitoring*"],
     "NAV": ["nav*", "route*", "router*", "menu*", "sidebar*"],
     "LAYOUT": ["layout*", "shell*", "frame*", "container*", "header*", "footer*"]
   }

   FOR EACH feature in Feature Hierarchy:
     feature_name_lower = lowercase(feature.name)

     FOR EACH (foundation_type, patterns) in FOUNDATION_PATTERNS:
       FOR EACH pattern in patterns:
         IF feature_name_lower MATCHES pattern (glob-style):
           MARK feature.is_foundation = true
           MARK feature.foundation_type = foundation_type

           # Auto-assign Wave based on foundation type
           IF foundation_type in ["AUTH", "USER_MGMT", "CORE_DATA", "INFRASTRUCTURE", "LAYOUT"]:
             SET feature.wave = 1
             IF feature.priority > "P1a":
               WARN: "Elevating {feature.id} to P1a (foundation)"
               SET feature.priority = "P1a"
           ELSE IF foundation_type in ["NAV"]:
             SET feature.wave = 2
             IF feature.priority > "P1b":
               SET feature.priority = "P1b"

           BREAK  # First match wins
   ```

   **Output**:
   - List of detected foundation features with their types
   - Wave assignments for all foundations
   - Priority elevation warnings (if any)

8c. **Populate Execution Order**:

   Organize all features into Waves in the concept.md template.

   ```text
   WAVE_1_FEATURES = filter(features, wave == 1)
   WAVE_2_FEATURES = filter(features, wave == 2)
   WAVE_3_PLUS = filter(features, wave >= 3)

   FOR EACH feature in WAVE_1_FEATURES:
     ADD to "Wave 1: Foundation Layer" table

   FOR EACH feature in WAVE_2_FEATURES:
     ADD to "Wave 2: Experience Layer" table

   FOR EACH feature in WAVE_3_PLUS:
     ADD to "Wave 3+: Business Features" table

   # Calculate what each feature blocks
   FOR EACH feature:
     feature.blocks = find_features_that_depend_on(feature.id)
   ```

8d. **Document Wave Rationale** (NEW — Transparency Enhancement):

   **Goal**: Explain WHY features are grouped in each wave and what dependency chains determined the order.

   **Reference template**: `templates/shared/concept-sections/wave-rationale.md`

   ```text
   FOR EACH wave:
     1. Document "Why these features are grouped together":
        - Technical dependencies (what must exist first)
        - Logical coherence (form a complete capability)

     2. Document "What blocks next wave":
        - Specific capabilities that must be complete
        - Data/APIs that next wave depends on

     3. Document "Alternative groupings considered":
        | Alternative | Why Not Chosen |
        |-------------|----------------|
        - E.g., "Could split auth and user mgmt" → "Would create integration risk"

     4. Visualize dependency chain:
        ```text
        Wave 1 (Foundation) → Wave 2 (Experience) → Wave 3 (Business Value)
             ↓                      ↓                      ↓
         Auth exists         User can navigate      User achieves goal
        ```
   ```

   **Output for Execution Order section**:

   ```markdown
   #### Wave 1 Rationale

   **Why these features are grouped together**:
   - [Technical dependency explanation]
   - [Logical coherence explanation]

   **What blocks Wave 2**:
   - [ ] [Specific capability or API]
   - [ ] [Data requirement]

   **Alternative groupings considered**:
   | Alternative | Why Not Chosen |
   |-------------|----------------|
   | [Alt approach] | [Reason] |
   ```

   **Validation**: Every wave MUST have rationale documented (CQS requirement).

9. **Capture Ideas Backlog**:

   **CRITICAL**: No idea should be lost. For each idea that doesn't fit current scope:

   ```markdown
   - [ ] [Idea] - Status: not started
   - [?] [Idea] - Status: needs validation (unclear value/feasibility)
   - [>] [Idea] - Status: deferred to future phase
   - [x] [Idea] - Status: rejected with reason
   ```

   Categories:
   - Potential future Epics
   - Feature enhancement ideas
   - Technical explorations
   - Rejected ideas (preserve rationale)

10. **Initialize Traceability Skeleton**:

   Create empty traceability matrix for each Story:

   | Concept ID | Spec Created | Spec Requirements | Tasks | Tests | Status |
   |------------|--------------|-------------------|-------|-------|--------|
   | [ID] | [ ] | - | - | - | Not started |

   This will be populated by subsequent commands (`/speckit.specify`, `/speckit.tasks`).

10b. **Generate Reasoning Trace** (NEW — Transparency Enhancement):

   **Goal**: Visualize the decision chain from Problem → JTBD → Feature for key features.
   Makes AI reasoning transparent and auditable.

   **Reference template**: `templates/shared/concept-sections/reasoning-trace.md`

   ```text
   # Generate at least 3 reasoning traces (more for complex concepts)
   TRACE_COUNT = max(3, count(P1a_features))

   FOR EACH P1a feature (and key excluded features):
     1. Assign Trace ID: RT-NNN (sequential)

     2. Build trace chain:
        PROBLEM: [Specific user problem from discovery]
            ↓
        PERSONA: [Which persona] experiences this when [situation]
            ↓
        JTBD: [JTBD-xxx-xxx] — "[When/I want/So I can]"
            ↓
        FEATURE: [EPIC-xxx.Fxx] [Feature Name]
            ↓
        PRIORITY: [P1a/P1b/etc] — [Why this priority]
            ↓
        VARIANT: [ALL/MINIMAL+/BALANCED+/AMBITIOUS] — [Why this variant]
            ↓
        SELECTION: [SEL-xxx] — Chosen over [alternatives] because [rationale]

     3. For EXCLUDED features, continue trace to:
        DECISION: EXCLUDE
            ↓
        RATIONALE: [Why excluded]
            ↓
        ALTERNATIVE: [How users accomplish similar outcome]
            ↓
        REVISIT TRIGGER: [When to reconsider]
   ```

   **Output for Reasoning Trace section**:

   ```markdown
   ### Reasoning Summary

   | Trace ID | Problem | JTBD | Feature | Decision | Key Rationale |
   |:--------:|---------|------|---------|:--------:|---------------|
   | RT-001 | [Problem] | JTBD-FUNC-001 | F01 | INCLUDE | [1-line rationale] |
   | RT-002 | [Problem] | JTBD-EMOT-001 | [Feature] | EXCLUDE | [1-line rationale] |

   ### Key Decision Points

   1. **[Decision 1]**: We chose [A] over [B] because [evidence/rationale]
      - Impact: [What this enabled/prevented]
      - Reversibility: [Type 1/Type 2]
   ```

   **Mermaid Diagram Generation**:
   ```text
   Generate visual flow:
   graph LR
       subgraph Problem["Problem Space"]
           P1[Problem: ...]
       end
       subgraph JTBD["Jobs to Be Done"]
           J1[JTBD-FUNC-001: ...]
       end
       subgraph Features["Feature Decisions"]
           F1[EPIC-001.F01: ...]
           F2[EXCLUDED: ...]
       end
       P1 --> J1
       J1 --> F1
       J1 --> F2
       style F2 fill:#ffcccc
   ```

   **Validation**: At least 3 reasoning traces required (CQS criterion).

12. **Generate Scope Variants (OPTIONAL)** — Moved from Step 4c:

   **Goal**: Generate MINIMAL/BALANCED/AMBITIOUS scope variations of the selected product alternative.

   **When to Generate**:
   - OPTIONAL: Only if user explicitly requests with `--generate-variants` flag
   - OR: User asks during interaction: "Can you generate scope variants?"
   - OTHERWISE: Skip this step (mark Concept Variants section as "Optional")

   **Distinction**:
   - **Product Alternatives** (Phase 0d): Different VISIONS (what to build)
   - **Scope Variants** (this step): Different SCOPE levels (how much to build) of SAME vision

   **Reference template**: `templates/shared/concept-sections/concept-variants.md`

   **Variant Generation Algorithm**:

   ```text
   INPUTS:
     - Features from Feature Hierarchy (step 6)
     - JTBD prioritization from persona analysis (step 5)
     - Effort estimates from step 6

   FOR EACH feature candidate:
     1. Classify by JTBD priority:
        - MUST_HAVE: Directly enables PRIMARY functional JTBD
        - SHOULD_HAVE: Enables SECONDARY JTBD or emotional jobs
        - COULD_HAVE: Enables social jobs or nice-to-have

     2. Assign to variants:
        MINIMAL:   MUST_HAVE only
        BALANCED:  MUST_HAVE + SHOULD_HAVE (Impact/Effort > threshold)
        AMBITIOUS: All features (MUST + SHOULD + COULD)

     3. Calculate variant metrics:
        - Feature count
        - Estimated effort (sum of feature T-shirt sizes)
        - Risk score (technical complexity weighted average)
        - Differentiation score (from Blue Ocean analysis if available)

     4. Generate recommendation:
        DEFAULT: BALANCED (unless constraints dictate otherwise)
        OVERRIDE if:
          - Timeline < 8 weeks → recommend MINIMAL
          - "Land and expand" strategy → recommend MINIMAL
          - Competitive pressure high → recommend AMBITIOUS
   ```

   **Output for Concept Variants section** (if generated):

   ```markdown
   ## Concept Variants (OPTIONAL)

   **Status**: [x] Generated

   ### Variant Comparison Matrix

   | Dimension | MINIMAL | BALANCED | AMBITIOUS |
   |-----------|:-------:|:--------:|:---------:|
   | Time to MVP | [X] weeks | [Y] weeks | [Z] weeks |
   | Team Size | [N] FTEs | [N] FTEs | [N] FTEs |
   | Feature Count | [N] | [N] | [N] |
   | Risk Level | Low | Medium | High |
   | Differentiation | Table stakes | Competitive | Market leader |
   | JTBD Coverage | Primary only | Primary + Secondary | All JTBD |

   ### Recommended Variant: [BALANCED]

   **Why this recommendation**:
   1. [Timeline/constraint fit]
   2. [Differentiation reasoning]
   3. [Risk balance rationale]

   **When to choose differently**:
   - MINIMAL if: [specific condition]
   - AMBITIOUS if: [specific condition]

   [Detailed variant breakdowns...]
   ```

   **If Skipped**:

   Mark Concept Variants section in concept.md as:
   ```markdown
   ## Concept Variants (OPTIONAL)

   **Status**: [ ] Not generated

   To generate scope variants (MINIMAL/BALANCED/AMBITIOUS), use:
   ```
   /speckit.concept-variants
   ```

   **Note**: Scope variants are different from Product Alternatives.
   Product Alternatives explored different visions (what to build).
   Scope variants explore different scope levels (how much to build) of the selected vision.
   ```

   **Integration**:
   - If generated: Feed variant assignment into Feature Hierarchy — each feature
     indicates which variants it belongs to (ALL, MINIMAL+, BALANCED+, AMBITIOUS only)
   - If skipped: Features in hierarchy have no variant assignment (can be added later)

13. **Write concept.md** to `specs/concept.md` using template structure.

## Validation Gates

Before completing, verify:

**Core Gates (always required)**:
- [ ] Vision statement is concrete (no vague words like "better", "improved")
- [ ] At least 2 user personas defined with specific goals
- [ ] At least 1 user journey per primary persona
- [ ] All Epics have at least one Feature
- [ ] All Features have at least one Story
- [ ] All Features have unique IDs following the format
- [ ] Dependencies form a DAG (no circular dependencies)
- [ ] Ideas backlog section is populated (even if "No additional ideas")
- [ ] Glossary includes all domain-specific terms

**Discovery Mode Gates** (if Discovery Mode was used):
- [ ] Problem statement refined from initial vague input
- [ ] At least 1 competitor analyzed with strengths/weaknesses
- [ ] At least 3 "What If" scenarios explored
- [ ] Market research sources documented
- [ ] User confirmed synthesized vision before structured capture
- [ ] Discovery findings connected to Feature Hierarchy (winning ideas became features)

**Transparency Gates** (NEW — always required):
- [ ] 3 concept variants documented (MINIMAL, BALANCED, AMBITIOUS)
- [ ] Variant comparison matrix complete (all 7 dimensions)
- [ ] Recommendation includes specific rationale (not generic)
- [ ] Every feature has JTBD link (JTBD-xxx-xxx format)
- [ ] Selection Decision Table has entry for each feature
- [ ] >80% of features have alternatives documented
- [ ] Wave Rationale documented for each wave
- [ ] At least 3 Reasoning Traces (RT-001, RT-002, RT-003)
- [ ] JTBD Coverage Analysis shows no unexplained gaps

## Quality Guidelines

### Hierarchy Best Practices

**Epic Granularity**:
- Too broad: "Core Platform" (meaningless)
- Too narrow: "User Login" (this is a Feature)
- Good: "User Management", "Payment Processing", "Analytics"

**Feature Granularity**:
- Too broad: "Authentication" (could be multiple features)
- Too narrow: "Validate Email Format" (this is implementation detail)
- Good: "User Registration", "Social Login", "Password Reset"

**Story Granularity**:
- Too broad: "User can manage their account" (vague)
- Good: "As a user, I want to update my email address so that I receive notifications at my current address"

### Dependency Mapping

Identify dependencies for:
- Data entities (shared models)
- UI components (shared layouts)
- Business logic (shared services)
- External integrations (API contracts)

### Ideas Backlog

**Do capture**:
- Half-formed ideas
- "What if..." scenarios
- Competitive feature ideas
- User-requested enhancements
- Technical debt considerations

**Don't discard**:
- Ideas that seem "obvious" (document them)
- Ideas that seem "too hard" (mark as needs-validation)
- Ideas outside current scope (mark as deferred)

## Output

After completion:

1. `specs/concept.md` with complete hierarchy
2. Report summary:
   - N Epics, M Features, K Stories captured
   - L Ideas in backlog
   - Dependency graph validated: Yes/No
3. Recommended next steps:
   - Stories ready for specification (P1a priority)
   - Example: `/speckit.specify {{EPIC_ID}}.F{{N}}.S{{N}}, {{EPIC_ID}}.F{{N}}.S{{N}}`

## Example

**User Input**: "I want to build a task management app where teams can create projects, assign tasks, track time, and generate reports"

**Resulting Hierarchy**:

```text
EPIC-001: User Management (P1)
  F01: Registration (P1a)
    S01: User registers with email
    S02: User verifies email
  F02: Team Management (P1b)
    S01: User creates team
    S02: User invites members

EPIC-002: Project Management (P1)
  F01: Project CRUD (P1a)
    S01: User creates project
    S02: User archives project
  F02: Task Management (P1a)
    S01: User creates task
    S02: User assigns task
    S03: User sets deadline

EPIC-003: Time Tracking (P2)
  F01: Time Entry (P2a)
    S01: User logs time
    S02: User edits time entry

EPIC-004: Reporting (P2)
  F01: Basic Reports (P2b)
    S01: User generates time report

Ideas Backlog:
- [ ] Recurring tasks - potential EPIC-002.F03
- [?] AI task suggestions - needs validation
- [>] Mobile app - deferred to v2.0
```

---

## Executive Summary Synthesis (Step 5-ES)

**After completing all concept sections, synthesize the Executive Summary.**

The Executive Summary provides 90-second decision context for executives by consolidating key information from all sections.

### Executive Summary Template Reference

```markdown
<!-- @include: ../shared/concept-sections/executive-summary.md -->
```

### Synthesis Instructions

Generate the Executive Summary by synthesizing from completed sections:

| Executive Summary Section | Source Sections | Key Data |
|---------------------------|-----------------|----------|
| **The Ask** | Vision Statement, Business Model Canvas | Decision/resources needed |
| **Why Now** | Market Framework, Porter's Five Forces | Timing signals, urgency |
| **The Opportunity** | Market Framework, Persona-JTBD | TAM/SAM/SOM, WTP |
| **Our Approach** | Blue Ocean Canvas, PR/FAQ | Differentiation, strategy |
| **Investment Required** | Business Model Canvas, Technical Hints | FTEs, budget, opportunity cost |
| **Key Risks & Mitigations** | Risk Matrix, Pre-Mortem | Top 3 risks with status |
| **Success Criteria** | Metrics-SMART | 6/12/36 month targets |
| **Recommendation** | CQS-E Score, Quality Gate | GO/NO-GO/CONDITIONAL |

### Quality Check

Before proceeding to Self-Review:
- [ ] The Ask is 1 actionable sentence
- [ ] Why Now has evidence-backed timing signals
- [ ] Opportunity includes validated TAM/SAM/SOM
- [ ] Approach has 2-3 defensible differentiators
- [ ] Investment covers headcount + budget + opportunity cost
- [ ] Top 3 risks have active mitigations
- [ ] Success metrics are SMART-validated
- [ ] Recommendation includes CQS-E score

**Output**: Update Executive Summary section at top of concept.md (after Vision Statement).

---

## Self-Review Phase (MANDATORY)

**Before declaring concept.md complete, you MUST perform self-review.**

This ensures the concept hierarchy is valid, complete, and ready for specification.

### Step 1: Re-read Generated Artifact

Read the concept file you created:
- `specs/concept.md`

Parse to extract hierarchy and validate structure.

### Step 2: Quality Criteria

| ID | Criterion | Check | Severity |
|----|-----------|-------|----------|
| SR-CONCEPT-01 | Vision Concrete | No vague words ("better", "improved", "enhanced") | CRITICAL |
| SR-CONCEPT-02 | Personas Defined | At least 2 user personas with specific goals | CRITICAL |
| SR-CONCEPT-03 | Hierarchy Valid | All IDs follow EPIC-NNN.FNN.SNN format | CRITICAL |
| SR-CONCEPT-04 | Epics Have Features | Every Epic has ≥1 Feature | HIGH |
| SR-CONCEPT-05 | Features Have Stories | Every Feature has ≥1 Story | HIGH |
| SR-CONCEPT-06 | IDs Unique | No duplicate EPIC/Feature/Story IDs | CRITICAL |
| SR-CONCEPT-07 | Dependencies Acyclic | No circular dependencies in DAG | CRITICAL |
| SR-CONCEPT-08 | Journeys Mapped | At least 1 journey per primary persona | HIGH |
| SR-CONCEPT-09 | Backlog Populated | Ideas Backlog section exists (even if empty note) | MEDIUM |
| SR-CONCEPT-10 | Glossary Present | Domain-specific terms defined | MEDIUM |
| SR-CONCEPT-11 | Foundation Detected | UX Foundation Layer populated with detected type | CRITICAL |
| SR-CONCEPT-12 | Foundations are P1a | All Wave 1 foundations have P1a priority | HIGH |
| SR-CONCEPT-13 | Execution Order Valid | Wave assignments complete, no Wave 3 without Wave 1-2 | HIGH |
| SR-CONCEPT-14 | Golden Path Exists | J000 journey defined covering Wave 1-2 features | CRITICAL |
| SR-CONCEPT-15 | No Orphan Features | All features assigned to a Wave | MEDIUM |
| SR-CONCEPT-16 | Market Opportunity | TAM/SAM/SOM analysis present with sources | HIGH |
| SR-CONCEPT-17 | JTBD Personas | Personas include Jobs-to-be-Done | HIGH |
| SR-CONCEPT-18 | SMART Metrics | Success metrics validated against SMART criteria | HIGH |
| SR-CONCEPT-19 | Risk Assessment | ≥3 risks documented with mitigations | MEDIUM |
| SR-CONCEPT-20 | Technical Hints | Domain entities or API surface estimated | MEDIUM |
| SR-CONCEPT-21 | CQS Calculated | Concept Quality Score computed and displayed | HIGH |
| SR-CONCEPT-22 | CQS Quality Gate | CQS ≥ 60 for specification readiness | HIGH |
| SR-CONCEPT-23 | Variants Generated | 3 concept variants (MINIMAL/BALANCED/AMBITIOUS) documented | HIGH |
| SR-CONCEPT-24 | Per-Feature Rationale | Every feature has JTBD link and selection rationale | HIGH |
| SR-CONCEPT-25 | Wave Rationale | Each wave has grouping explanation and dependencies | MEDIUM |
| SR-CONCEPT-26 | Reasoning Trace | At least 3 traces (Problem → Feature) documented | MEDIUM |
| SR-CONCEPT-27 | Next Steps File Created | File `specs/next-steps.md` exists with ≥500 bytes and 4 command variants | CRITICAL |
| SR-CONCEPT-28 | Foundation Commands Included | Wave 1/2 commands include foundation story IDs (AUTH, ERROR, LAYOUT, NAV, ADMIN, INTEGRATION if applicable) | HIGH |
| SR-CONCEPT-29 | Story IDs Valid | All story IDs follow EPIC-###.F##.S##, no duplicates, epics match hierarchy | CRITICAL |

### Step 3: Hierarchy Validation

Verify hierarchy structure:

```text
EPICS = {}
FEATURES = {}
STORIES = {}

FOR EACH line matching EPIC-NNN pattern:
  Validate format: EPIC-NNN
  Check uniqueness
  EPICS[id] = entry

FOR EACH line matching EPIC-NNN.FNN pattern:
  Validate parent EPIC exists
  Check uniqueness
  FEATURES[id] = entry

FOR EACH line matching EPIC-NNN.FNN.SNN pattern:
  Validate parent Feature exists
  Check uniqueness
  STORIES[id] = entry

# Validate completeness
FOR EACH epic in EPICS:
  IF no features reference this epic:
    ERROR: "Epic {id} has no features"

FOR EACH feature in FEATURES:
  IF no stories reference this feature:
    ERROR: "Feature {id} has no stories"
```

### Step 3b: Foundation & Wave Validation

Verify UX Foundation Layer and Execution Order:

```text
# SR-CONCEPT-11: Foundation Detected
IF "UX Foundation Layer" section is empty OR PROJECT_TYPE not set:
  ERROR: "Foundation layer not populated"

# SR-CONCEPT-12: Foundations are P1a
FOR EACH feature WHERE wave == 1:
  IF feature.priority != "P1a":
    ERROR: "Wave 1 feature {id} must be P1a, found {priority}"

# SR-CONCEPT-13: Execution Order Valid
WAVE_1_COUNT = count(features WHERE wave == 1)
WAVE_2_COUNT = count(features WHERE wave == 2)
WAVE_3_COUNT = count(features WHERE wave >= 3)

IF WAVE_3_COUNT > 0 AND WAVE_1_COUNT == 0:
  ERROR: "Wave 3 features exist but no Wave 1 foundations"

IF WAVE_3_COUNT > 0 AND WAVE_2_COUNT == 0:
  WARN: "Wave 3 features exist but no Wave 2 experience layer"

# SR-CONCEPT-14: Golden Path Exists
IF "Golden Path" section is empty OR J000 not defined:
  ERROR: "Golden Path (J000) not defined"

GOLDEN_PATH_FEATURES = extract features from J000
FOR EACH feature in GOLDEN_PATH_FEATURES:
  IF feature not in FEATURES:
    ERROR: "Golden Path references undefined feature: {id}"

# SR-CONCEPT-15: No Orphan Features
FOR EACH feature in FEATURES:
  IF feature.wave is undefined:
    WARN: "Feature {id} not assigned to any Wave"
```

### Step 3c: CQS Calculation — NEW

Calculate Concept Quality Score from 6 components:

```text
# Component Scoring (see templates/shared/concept-sections/cqs-score.md for full criteria)

MARKET_SCORE = 0
IF "TAM/SAM/SOM" section present with values: MARKET_SCORE += 55
IF "Competitive Positioning Matrix" present: MARKET_SCORE += 25
IF "Market Validation Signals" checklist present: MARKET_SCORE += 20

PERSONA_SCORE = 0
IF count(personas) >= 2: PERSONA_SCORE += 30
IF personas have JTBD tables: PERSONA_SCORE += 40
IF "Willingness to Pay" documented: PERSONA_SCORE += 15
IF "Success Criteria" documented: PERSONA_SCORE += 15

METRICS_SCORE = 0
IF "North Star Metric" identified: METRICS_SCORE += 40
IF SMART validation table present: METRICS_SCORE += 40
IF leading/lagging indicators defined: METRICS_SCORE += 20

FEATURES_SCORE = 0
IF Epic/Feature/Story hierarchy valid: FEATURES_SCORE += 40
IF Wave assignments complete: FEATURES_SCORE += 30
IF Golden Path (J000) defined: FEATURES_SCORE += 30

RISK_SCORE = 0
IF count(risks) >= 3: RISK_SCORE += 40
IF mitigations documented: RISK_SCORE += 30
IF pivot criteria defined: RISK_SCORE += 30

TECH_SCORE = 0
IF "Domain Entities" sketched: TECH_SCORE += 40
IF "API Surface Estimation" present: TECH_SCORE += 30
IF "Constitution Principle Conflicts" reviewed: TECH_SCORE += 30

# Calculate weighted CQS-E (Evidence-Based)
STRATEGIC_SCORE = 0
IF "PR/FAQ" completed: STRATEGIC_SCORE += 25
IF "Blue Ocean Canvas" completed: STRATEGIC_SCORE += 20
IF "Business Model Canvas" completed: STRATEGIC_SCORE += 20
IF "Three Horizons" allocated: STRATEGIC_SCORE += 15
IF "Trade-off Resolution" defined: STRATEGIC_SCORE += 10
IF "Scope Exclusions" documented: STRATEGIC_SCORE += 10

VALIDATION_SCORE = 0
IF count(hypotheses) >= 3: VALIDATION_SCORE += 30
IF has_hypothesis_per_type(D, F, V): VALIDATION_SCORE += 25
IF evidence_collected: VALIDATION_SCORE += 25
IF "Pre-Mortem" scenarios documented: VALIDATION_SCORE += 20

# CQS-E Formula with Evidence Multiplier
CQS_BASE = (MARKET_SCORE × 0.20) + (PERSONA_SCORE × 0.15) + (METRICS_SCORE × 0.15) +
           (FEATURES_SCORE × 0.15) + (RISK_SCORE × 0.10) + (TECH_SCORE × 0.10) +
           (STRATEGIC_SCORE × 0.10) + (VALIDATION_SCORE × 0.05)

# Evidence Multiplier (0.8-1.2)
EVIDENCE_MULTIPLIER = assess_evidence_quality()
  # 1.2: All claims sourced with primary research
  # 1.0: Most claims have credible sources
  # 0.8: Many claims unsourced

CQS_E = CQS_BASE × EVIDENCE_MULTIPLIER

# SR-CONCEPT-21: CQS-E Calculated
STORE CQS_E for report output

# SR-CONCEPT-22: CQS-E Quality Gate
IF CQS_E < 60:
  WARN: "CQS-E {CQS_E}/100 — Concept not ready for specification"
  WARN: "Low scoring components: [list components < 60]"
  WARN: "Evidence quality: {EVIDENCE_MULTIPLIER}"
ELSE IF CQS_E < 80:
  INFO: "CQS-E {CQS_E}/100 — Proceed with caution, flag gaps during specification"
ELSE:
  INFO: "CQS-E {CQS_E}/100 — Concept ready for specification"

**Reference template**: `templates/shared/concept-sections/cqs-score.md`
```

### Step 3d: Transparency Validation

Verify transparency and explainability:

```text
# SR-CONCEPT-23: Scope Variants (OPTIONAL in v2.0)
SCOPE_VARIANTS_COUNT = count(sections matching "Variant: MINIMAL|BALANCED|AMBITIOUS")
IF SCOPE_VARIANTS_COUNT >= 3:
  INFO: "Scope variants generated ({SCOPE_VARIANTS_COUNT} variants)"
  IF "Recommended Variant" section missing:
    WARN: "No recommended variant with rationale"
ELSE:
  INFO: "Scope variants not generated (optional in v2.0)"

# SR-CONCEPT-27: Product Alternatives (NEW — REQUIRED in v2.0)
PRODUCT_ALTERNATIVES_COUNT = count(sections matching "Alternative [0-9]+:")
IF PRODUCT_ALTERNATIVES_COUNT < 3:
  ERROR: "Only {PRODUCT_ALTERNATIVES_COUNT} product alternatives documented, need ≥3"
IF NOT check("Selected Alternative:"):
  WARN: "No selected alternative indicated — unclear which approach was chosen"
IF NOT check("Selection Rationale:" OR "Why this alternative"):
  WARN: "Missing selection rationale — why was this alternative chosen over others?"

# SR-CONCEPT-24: Per-Feature Rationale
FEATURES_WITH_JTBD = 0
TOTAL_FEATURES = count(features in Feature Hierarchy)
FOR EACH feature in Feature Selection Rationale:
  IF feature has JTBD link (non-empty):
    FEATURES_WITH_JTBD += 1
COVERAGE = FEATURES_WITH_JTBD / TOTAL_FEATURES
IF COVERAGE < 0.80:
  ERROR: "Only {COVERAGE*100}% features have JTBD links, need >80%"
IF "Selection Decision Table" section missing:
  ERROR: "Feature Selection Rationale table not found"

# SR-CONCEPT-25: Wave Rationale
WAVES_WITH_RATIONALE = 0
FOR EACH wave in Execution Order (1, 2, 3+):
  IF wave has "Wave N Rationale" subsection:
    WAVES_WITH_RATIONALE += 1
  ELSE:
    WARN: "Wave {N} missing rationale explanation"
IF WAVES_WITH_RATIONALE < 2:
  ERROR: "Only {WAVES_WITH_RATIONALE} waves have rationale, need ≥2"

# SR-CONCEPT-26: Reasoning Trace
TRACE_COUNT = count(sections matching "Trace [0-9]+:" OR "RT-[0-9]+")
IF TRACE_COUNT < 3:
  ERROR: "Only {TRACE_COUNT} reasoning traces documented, need ≥3"
IF no EXCLUDE trace found:
  WARN: "No EXCLUDE reasoning trace — add at least 1 to show scope decisions"
IF "Reasoning Summary" table missing:
  WARN: "Add Reasoning Summary table for trace overview"

**Reference templates**:
- `templates/shared/concept-sections/concept-variants.md`
- `templates/shared/concept-sections/selection-rationale.md`
- `templates/shared/concept-sections/wave-rationale.md`
- `templates/shared/concept-sections/reasoning-trace.md`
```

### Step 4: Dependency Validation

Check for circular dependencies:

```text
BUILD directed graph from dependency declarations:
  - Feature A depends on Feature B → edge B → A

RUN topological sort:
  IF cycle detected:
    Extract cycle path
    ERROR: "Circular dependency: {path}"

VALIDATE cross-Epic dependencies are documented
```

### Step 5: Verdict

- **PASS**: All CRITICAL/HIGH criteria pass, hierarchy valid → proceed to handoff
- **FAIL**: Any CRITICAL issue → self-correct (max 3 iterations)
  - Duplicate IDs → renumber
  - Missing hierarchy levels → add
  - Circular dependencies → break cycle
- **WARN**: Only MEDIUM issues → show warnings, proceed

### Step 6: Self-Correction Loop

```text
IF issues found AND iteration < 3:
  1. Fix each issue:
     - Renumber duplicate IDs
     - Add missing Features/Stories
     - Break circular dependencies
     - Add Ideas Backlog section
     - Populate Glossary
  2. Re-run self-review from Step 1
  3. Report: "Self-review iteration {N}: Fixed {issues}, re-validating..."

IF still failing after 3 iterations:
  - STOP and report to user
  - List hierarchy validation failures
  - Do NOT proceed to handoff
```

### Step 7: Self-Review Report

After passing self-review, output:

```text
## Self-Review Complete ✓

**Artifact**: specs/concept.md
**Iterations**: {N}

### Hierarchy Summary

| Level | Count | Status |
|-------|-------|--------|
| Epics | {N} | ✓ All have Features |
| Features | {N} | ✓ All have Stories |
| Stories | {N} | ✓ All IDs unique |

### Validation Results

| Check | Result |
|-------|--------|
| Vision | ✓ Concrete (no vague terms) |
| Personas | ✓ {N} defined |
| ID Format | ✓ All valid |
| Dependencies | ✓ DAG valid (no cycles) |
| User Journeys | ✓ {N} journeys mapped |
| Ideas Backlog | ✓ {N} ideas captured |

### Foundation Layer

| Check | Result |
|-------|--------|
| Project Type | ✓ {PROJECT_TYPE} detected |
| Foundations | ✓ {N} required, {N} defined |
| Golden Path | ✓ J000 defined with {N} steps |

### Wave Distribution

| Wave | Features | Status |
|------|----------|--------|
| Wave 1 (Foundation) | {N} | ✓ All P1a |
| Wave 2 (Experience) | {N} | ✓ All P1b |
| Wave 3+ (Business) | {N} | Ready after Wave 1-2 |

### Priority Distribution

| Priority | Stories |
|----------|---------|
| P1a | {N} |
| P1b | {N} |
| P2 | {N} |
| P3 | {N} |

### Concept Quality Score (CQS) — NEW

**Formula**: See templates/shared/cqs-formula.md (v0.7.0 with 11 components, 0-120 scale)
**Reporting Format**: Simplified 6-component view in self-review report (Market/Persona/Metrics/Features/Risk/Technical)

| Component | Score | Weight | Weighted |
|-----------|:-----:|:------:|:--------:|
| Market Validation | {MARKET_SCORE}/100 | 0.25 | {WEIGHTED} |
| Persona Depth | {PERSONA_SCORE}/100 | 0.20 | {WEIGHTED} |
| Metrics Quality | {METRICS_SCORE}/100 | 0.15 | {WEIGHTED} |
| Feature Completeness | {FEATURES_SCORE}/100 | 0.20 | {WEIGHTED} |
| Risk Assessment | {RISK_SCORE}/100 | 0.10 | {WEIGHTED} |
| Technical Hints | {TECH_SCORE}/100 | 0.10 | {WEIGHTED} |
| **CQS Total** | | | **{CQS}/100** |

**Quality Gate**: {CQS_STATUS}
- CQS ≥ 80: ✅ Ready for specification with high confidence
- CQS 60-79: ⚠️ Proceed with caution — flag gaps during specification
- CQS < 60: ⛔ Not ready — complete discovery before specification

**Reference**: `templates/shared/concept-sections/cqs-score.md`

### Ready for Specification

Concept capture complete.

**Recommended order** (Wave-based):
See "Ready-to-Execute Commands" section below for copy-paste ready commands.

**Golden Path status**: [ ] Not yet testable (requires Wave 1-2 completion)
```

## Helper: Parse Story Metadata

Extracts structured data from generated concept.md:
- Story IDs from Feature Hierarchy section
- Wave assignments from Execution Order section
- Priorities from Feature Priority fields

## Helper: Group Stories by Feature

**CRITICAL**: Maintains feature-level grouping in all command variants.
Stories of same feature always appear consecutively in output commands.

**Example:**
- ✓ Good: `/speckit.specify {{EPIC}}.F{{1}}.S{{1}}, {{EPIC}}.F{{1}}.S{{2}}, {{EPIC}}.F{{2}}.S{{1}}`  (same feature grouped)
- ✗ Bad: `/speckit.specify {{EPIC}}.F{{1}}.S{{1}}, {{EPIC}}.F{{2}}.S{{1}}, {{EPIC}}.F{{1}}.S{{2}}`  (features interleaved)

---

### Step 7b: Generate Ready-to-Execute Commands

After completing the self-review report, generate ready-to-execute `/speckit.specify` commands for all implementation strategies.

**Process:**

1. **Parse generated concept.md** to collect story metadata:

   ```text
   a. Scan "Feature Hierarchy" section:
      - Extract all story IDs matching pattern: [EPIC-XXX.FXX.SXX]
      - Extract parent feature_id (EPIC-XXX.FXX)
      - Extract parent epic_id (EPIC-XXX)

   b. Scan "Execution Order" section (Wave Planning tables):
      - Find Wave 1, Wave 2, Wave 3+ feature assignments
      - Map: feature_id → wave_number
      - Assign wave to each story based on parent feature

   c. Scan "Feature Hierarchy" for priorities:
      - Extract "Priority: P1a" (or P1b, P2, P3) from each Feature
      - Map: feature_id → priority
      - Assign priority to each story based on parent feature

   d. Build stories array:
      [
        {id: "EPIC-001.F01.S01", epic: "EPIC-001", feature: "EPIC-001.F01", wave: 1, priority: "P1a"},
        {id: "EPIC-001.F01.S02", epic: "EPIC-001", feature: "EPIC-001.F01", wave: 1, priority: "P1a"},
        ...
      ]
   ```

2. **Generate 4 command variants**:

   **VARIANT 1: BY WAVES (RECOMMENDED)**
   ```text
   - Group stories by wave (1, 2, 3+)
   - Keep stories of same feature together (adjacent)
   - Generate one command per wave
   - Format: /speckit.specify STORY1, STORY2, STORY3, ...

   Algorithm:
   waves = {1: [], 2: [], 3: []}
   FOR feature_id IN unique(stories.feature_id):
     feature_stories = stories WHERE feature_id matches
     wave = feature_stories[0].wave  # All stories in feature share same wave
     waves[wave].extend(feature_stories.map(s => s.id))

   FOR wave IN sorted(waves.keys()):
     OUTPUT: "/speckit.specify " + ", ".join(waves[wave])
   ```

   **VARIANT 2: BY EPICS**
   ```text
   - Group all stories by epic_id
   - Generate one command per epic
   - Format: /speckit.specify STORY1, STORY2, ...

   Algorithm:
   epics = {}
   FOR story IN stories:
     epics[story.epic_id].append(story.id)

   FOR epic_id IN sorted(epics.keys()):
     OUTPUT: "/speckit.specify " + ", ".join(epics[epic_id])
   ```

   **VARIANT 3: BY PRIORITIES**
   ```text
   - Group stories by priority (P1a, P1b, P2, P3)
   - Sort in priority order
   - Generate one command per priority level
   - Format: /speckit.specify STORY1, STORY2, ...

   Algorithm:
   priorities = {}
   FOR feature_id IN unique(stories.feature_id):
     feature_stories = stories WHERE feature_id matches
     priority = feature_stories[0].priority
     priorities[priority].extend(feature_stories.map(s => s.id))

   FOR priority IN ["P1a", "P1b", "P1c", "P2a", "P2b", "P2c", "P3"]:
     IF priority IN priorities:
       OUTPUT: "/speckit.specify " + ", ".join(priorities[priority])
   ```

   **VARIANT 4: ENTIRE CONCEPT**
   ```text
   - Collect ALL story IDs
   - Generate single command with all stories
   - Format: /speckit.specify STORY1, STORY2, ..., STORYN

   Algorithm:
   all_story_ids = [story.id FOR story IN stories]
   OUTPUT: "/speckit.specify " + ", ".join(all_story_ids)
   ```

3. **Handle edge cases**:

   ```text
   - Empty wave: Show "Wave X (0 stories - not applicable)", skip command generation
   - Long command (>500 chars or >15 stories): Split into feature-group sub-commands
   - Missing priority: Default to P3, log warning
   - Missing wave: Infer from dependencies or default to Wave 1
   - Wave 3+: If Wave 3, 4, 5 exist, group into "Wave 3+" section
   ```

4. **Format and output** the "Ready-to-Execute Commands" section:

   ```text
   - Include section header
   - Add 4 option blocks (By Waves, By Epics, By Priorities, Entire Concept)
   - Mark "By Waves" as RECOMMENDED
   - Include Infrastructure Prerequisites warning before Wave 1 (INFRA-AUTH, INFRA-LAYOUT, INFRA-ERROR)
   - Include story counts: ({N} stories)
   - Include epic names: [Epic Name] from Feature Hierarchy
   - Add "When to use" guidance for each option
   - Add "Next Steps" guidance at end (including infrastructure prerequisites step)
   - Use bash code blocks for commands
   ```

**Output:** Continue to "Ready-to-Execute Commands" section below.

---

### Ready-to-Execute Commands

Concept capture complete. Use these ready-to-execute commands to begin specification.

---

#### Option 1: By Waves (RECOMMENDED)

**Why this order:** Wave-based execution ensures dependencies are satisfied and enables incremental testing.

**⚠️ Infrastructure Prerequisites:**

Before executing Wave 1, ensure infrastructure foundation tasks are completed (if applicable):

- **INFRA-AUTH**: Authentication infrastructure (session management, JWT, OAuth providers)
- **INFRA-LAYOUT**: Base layout/shell components (header, footer, navigation, error boundaries)
- **INFRA-ERROR**: Error handling infrastructure (logging, monitoring, error pages)

These tasks typically come from `/speckit.plan` Phase 0 (Foundation) and should be implemented before feature stories.

---

**Wave 1: Foundation Layer** ({N} stories)
```bash
/speckit.specify EPIC-001.F01.S01, EPIC-001.F01.S02, EPIC-001.F02.S01
```

**Wave 2: Experience Layer** ({N} stories)
```bash
/speckit.specify EPIC-001.F03.S01, EPIC-002.F01.S01, EPIC-002.F01.S02
```

**Wave 3+: Business Features** ({N} stories)
```bash
/speckit.specify EPIC-003.F01.S01, EPIC-003.F02.S01
```

**Sequential execution:**
1. Execute Wave 1 command → Implement → Test
2. After Wave 1 complete, execute Wave 2 command → Implement → Test
3. After Golden Path testable, execute Wave 3+ command

---

#### Option 2: By Epics

**When to use:** Execute one epic at a time for focused domain work.

**EPIC-001: [Epic Name]** ({N} stories)
```bash
/speckit.specify EPIC-001.F01.S01, EPIC-001.F01.S02, EPIC-001.F02.S01
```

**EPIC-002: [Epic Name]** ({N} stories)
```bash
/speckit.specify EPIC-002.F01.S01, EPIC-002.F01.S02
```

**EPIC-003: [Epic Name]** ({N} stories)
```bash
/speckit.specify EPIC-003.F01.S01, EPIC-003.F02.S01
```

---

#### Option 3: By Priorities

**When to use:** Maximize business value delivery by priority.

**P1a: Critical Path** ({N} stories)
```bash
/speckit.specify EPIC-001.F01.S01, EPIC-001.F01.S02, EPIC-002.F01.S01
```

**P1b: MVP Must-Haves** ({N} stories)
```bash
/speckit.specify EPIC-001.F02.S01, EPIC-002.F01.S02
```

**P2a: Post-MVP Important** ({N} stories)
```bash
/speckit.specify EPIC-003.F01.S01, EPIC-003.F02.S01
```

**P3: Future Enhancements** ({N} stories)
```bash
/speckit.specify EPIC-004.F01.S01
```

---

#### Option 4: Entire Concept (All at Once)

**When to use:** For comprehensive specification generation (recommended for experienced teams).

**All Stories** ({N} total)
```bash
/speckit.specify EPIC-001.F01.S01, EPIC-001.F01.S02, EPIC-001.F02.S01, EPIC-001.F03.S01, EPIC-002.F01.S01, EPIC-002.F01.S02, EPIC-003.F01.S01, EPIC-003.F02.S01, EPIC-004.F01.S01
```

---

**Next Steps:**
1. Choose your execution strategy (Option 1-4)
2. Copy and execute the command(s)
3. Review generated `specs/NNN-feature/spec.md`
4. Run `/speckit.plan` to create implementation plan
5. Run `/speckit.tasks` to generate task breakdown
6. **Before implementation**: Complete infrastructure prerequisites (INFRA-AUTH, INFRA-LAYOUT, INFRA-ERROR) from Phase 0 if applicable

---

### Step 7c: Create specs/next-steps.md (MANDATORY)

**CRITICAL**: This step is MANDATORY and BLOCKING. Do not proceed without creating this file.

**Purpose**: Create `specs/next-steps.md` with copy-paste ready commands for immediate use.

**Why mandatory**:
- Primary output for developer workflow
- Contains ALL execution strategies (by waves, epics, priorities, all-at-once)
- Users depend on this file for next steps
- Without it, concept is incomplete

**Process:**

1. **Extract Ready-to-Execute Commands**:
   - Copy entire "Ready-to-Execute Commands" section from Step 7b output
   - Include infrastructure prerequisites warnings
   - Include all 4 command variants (waves, epics, priorities, all-at-once)
   - Include Next Commands After Specify section

2. **Build next-steps.md content**:

```markdown
# Ready-to-Execute Commands

**Generated**: {current_timestamp}
**Source**: specs/concept.md Feature Hierarchy
**Concept Version**: {concept_version}
**Project Type**: {detected_project_type}

This file contains pre-generated `/speckit.specify` commands to streamline feature specification workflow.

---

## Infrastructure Prerequisites

⚠️ **Complete these BEFORE running specify commands:**

Before executing any `/speckit.specify` commands, ensure infrastructure prerequisites from Phase 0 are completed:

- **INFRA-AUTH**: Authentication infrastructure (session management, JWT, OAuth providers)
- **INFRA-LAYOUT**: Base layout/shell components (header, footer, navigation, error boundaries)
- **INFRA-ERROR**: Error handling infrastructure (logging, monitoring, error pages)
- **INFRA-STATE**: State management setup (Redux, Context, or equivalent)

These tasks typically come from `/speckit.plan` Phase 0 (Foundation) and must be implemented **BEFORE** feature stories.

---

{PASTE_4_COMMAND_VARIANTS_FROM_STEP_7b}

---

## Next Commands After Specify

```bash
# After /speckit.specify completes:
/speckit.plan {feature-id}      # Generate implementation plan
/speckit.tasks {feature-id}     # Break down into tasks
/speckit.staging                # Provision test environment
/speckit.implement {feature-id} # Execute TDD implementation
```

---

**Generated by**: `/speckit.concept` v0.8.2+
**Reference**: `templates/commands/concept.md` Step 7c
```

3. **Write file (MANDATORY ACTION)**:

```python
# This is NOT optional - file MUST be created
import os

next_steps_path = "specs/next-steps.md"
os.makedirs("specs", exist_ok=True)  # Ensure directory exists

with open(next_steps_path, "w", encoding="utf-8") as f:
    f.write(next_steps_content)

print(f"✅ Created: {next_steps_path}")
```

4. **Validate file creation (BLOCKING)**:

```python
# Verify file was actually created
if not os.path.exists("specs/next-steps.md"):
    raise FileNotFoundError(
        "❌ CRITICAL: specs/next-steps.md was not created. "
        "This is a mandatory output file. Retry Step 7c."
    )

# Verify file has content
file_size = os.path.getsize("specs/next-steps.md")
if file_size < 500:  # Minimum reasonable size
    raise ValueError(
        f"❌ CRITICAL: specs/next-steps.md is too small ({file_size} bytes). "
        "File may be empty or incomplete. Retry Step 7c."
    )

print(f"✅ Validated: specs/next-steps.md ({file_size} bytes)")
```

**Error Handling**:
- **If directory creation fails**: HALT with error "Cannot create specs/ directory"
- **If file write fails**: HALT with error "Cannot write specs/next-steps.md"
- **If file empty**: HALT with error "File created but empty, retry"
- **Do NOT skip this step** - it is mandatory for concept completion

**Quality Gate**: **QG-CONCEPT-NEXTSTEPS** (NEW)
- **Severity**: CRITICAL
- **Check**: File exists AND size >= 500 bytes AND contains all 4 command variants
- **On failure**: HALT concept generation, show error, request retry

**Console output**:
```
✅ Ready-to-Execute Commands saved: specs/next-steps.md (1.2 KB)
   - Option 1: By Waves (recommended)
   - Option 2: By Epics
   - Option 3: By Priorities
   - Option 4: Entire Concept
```

**Output**: File created at `specs/next-steps.md`, validated, continue to next phase.

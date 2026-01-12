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
    default_tier: max
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
      model_override: sonnet
      prompt: |
        ## Context
        Project: {{PROJECT_ROOT}}
        User Input: {{ARGUMENTS}}

        ## Task
        Conduct market research:
        1. Analyze TAM/SAM/SOM for the product category
        2. Research industry trends and growth projections
        3. Identify market entry barriers and opportunities
        4. Document regulatory considerations if applicable

        ## Output
        - Market size estimates with sources
        - Industry trend analysis
        - Entry barrier assessment
    - role: competitive-analyst
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        ## Context
        Project: {{PROJECT_ROOT}}
        User Input: {{ARGUMENTS}}

        ## Task
        Analyze competitive landscape:
        1. Identify direct and indirect competitors
        2. Map competitor features and positioning
        3. Find gaps and differentiation opportunities
        4. Analyze competitor pricing and business models

        ## Output
        - Competitor matrix with features
        - Gap analysis
        - Differentiation opportunities
    - role: persona-designer
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        ## Context
        Project: {{PROJECT_ROOT}}
        User Input: {{ARGUMENTS}}

        ## Task
        Design user personas:
        1. Identify primary and secondary user segments
        2. Create detailed persona profiles with demographics
        3. Document pain points and motivations
        4. Estimate willingness-to-pay for each segment

        ## Output
        - Persona cards (2-4 personas)
        - Pain point inventory
        - WTP analysis per segment

    # NEW: Domain-specific research agents
    - role: standards-researcher
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        ## Context
        Project: {{PROJECT_ROOT}}
        User Input: {{ARGUMENTS}}

        ## Task
        Research compliance standards and regulations for the domain:
        1. Load domain from memory/constitution.md (Domain Layer)
        2. For fintech → PCI-DSS, SOX, AML/KYC
        3. For healthcare → HIPAA, FHIR, HL7, 21 CFR Part 11
        4. For e-commerce → PCI-DSS, CCPA, GDPR

        Use WebSearch for official sources:
        - "PCI-DSS requirements 2025 official"
        - "GDPR compliance checklist"
        - "HIPAA technical safeguards"
        - "{DOMAIN} regulatory requirements 2025"

        ## Output
        - Compliance requirements list
        - Regulatory checklists
        - Evidence tier: AUTHORITATIVE

    - role: academic-researcher
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        ## Context
        Project: {{PROJECT_ROOT}}
        User Input: {{ARGUMENTS}}

        ## Task
        Research academic papers and whitepapers for best practices:
        1. Search Google Scholar, arXiv, IEEE Xplore
        2. Focus on peer-reviewed papers and industry whitepapers
        3. Extract validated best practices with evidence

        Use WebSearch queries:
        - "{DOMAIN} best practices research paper"
        - "{TECHNOLOGY} architecture patterns whitepaper"
        - "{PROBLEM} academic research"

        ## Output
        - Best practices catalog with citations
        - Evidence tier: STRONG

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
      model_override: sonnet
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
      model_override: sonnet
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
      prompt: |
        ## Context
        Value Proposition: (from value-prop-designer)
        JTBD Analysis: (from jtbd-analyst)

        ## Task
        Design success metrics:
        1. Define North Star metric
        2. Create SMART goals for launch
        3. Design metric hierarchy (input/output/outcome)
        4. Set realistic benchmarks

        ## Output
        - North Star metric definition
        - SMART launch goals
        - Metric dashboard spec
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
      prompt: |
        ## Context
        Value Proposition: (from value-prop-designer)
        Project Type: {{PROJECT_TYPE}}

        ## Task
        Generate technical discovery hints:
        1. Identify core domain entities
        2. Sketch API surface area
        3. Note integration requirements
        4. Flag technical risk areas

        ## Output
        - Domain entity list
        - API surface sketch
        - Integration requirements
        - Technical risk notes

    # Wave 5: Quality Validation (final)
    - role: concept-quality-scorer
      role_group: REVIEW
      parallel: false
      depends_on: [metrics-designer, risk-assessor, technical-hint-generator]
      priority: 50
      model_override: opus
      prompt: |
        ## Context
        All Concept Artifacts: (from previous agents)

        ## Task
        Calculate Concept Quality Score (CQS):
        1. Score each dimension (0-20 points):
           - Problem Clarity (personas, JTBD defined)
           - Solution Viability (value prop, differentiation)
           - Market Validation (TAM/SAM/SOM, competition)
           - Risk Awareness (risks identified, mitigations)
           - Technical Readiness (domain hints, API surface)
        2. Calculate total CQS (0-100)
        3. Generate improvement recommendations

        ## Output
        - CQS score with breakdown
        - Quality gate verdict (PASS >= 80, REVIEW 60-79, FAIL < 60)
        - Improvement recommendations
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

   ### Phase 0a: Problem Discovery (Brainstorming)

   **Goal**: Help user articulate the real problem before jumping to solutions.

   **Interactive questioning flow** (ask sequentially, adapt based on answers):

   1. **Root Problem Question**:
      "What specific frustration or inefficiency triggered this idea?"
      - Listen for: pain points, workarounds, failed alternatives
      - If answer is vague, probe deeper: "Can you describe a specific moment when this was frustrating?"

   2. **Scale Question**:
      "How many people/companies face this problem? How often does it occur?"
      - Listen for: market size signals, frequency, severity

   3. **Current Solutions Question**:
      "How do people solve this today? What's wrong with those approaches?"
      - Listen for: competitor gaps, differentiation opportunities

   4. **Stakes Question**:
      "What happens if this problem remains unsolved? What's the cost?"
      - Listen for: urgency, willingness to pay, business impact

   5. **Vision Question**:
      "Describe the ideal outcome if this were perfectly solved."
      - Listen for: success criteria, feature hints, user delight moments

   6. **Market Positioning Question**:
      "How will your product be positioned in the market?"

      **Options** (use AskUserQuestion with header "Market Position"):
      - **Premium/High-end**: Highest quality, best experience, premium pricing
      - **Value/Mid-market**: Good quality/price balance, competitive pricing
      - **Budget/Mass-market**: Lowest price, acceptable quality
      - **Niche/Specialized**: Focused on specific segment, premium pricing for domain expertise
      - **Disruptive/Category-creating**: Creating new market category, redefining how users solve the problem

      - Listen for: quality expectations, pricing strategy, target customer segment
      - Store in concept.md § Strategic Positioning → "Market Position: [answer]"

   7. **Primary Differentiation Question**:
      "What will be your primary competitive advantage?"

      **Options** (use AskUserQuestion with header "Differentiation"):
      - **Technology/Innovation**: Better tech, faster algorithms, novel approach
      - **User Experience**: Simpler, more intuitive, better design
      - **Price**: Cheaper, better value, generous free tier
      - **Performance**: Faster, more reliable, higher uptime
      - **Integration/Ecosystem**: Better integrations, platform effects, marketplace
      - **Service/Support**: Better support, professional services, community

      - Listen for: what makes you unique, why customers will switch
      - Store in concept.md § Strategic Positioning → "Differentiation: [answer]"
      - **Cross-integration**: If "Performance" selected → recommend perf_priority=best-in-class in constitution

   8. **Go-to-Market Strategy Question**:
      "What's your primary go-to-market strategy?"

      **Options** (use AskUserQuestion with header "GTM Strategy"):
      - **Product-Led Growth (PLG)**: Free tier, viral loops, self-serve signup, low-touch onboarding
      - **Sales-Led Growth**: Enterprise sales, demos, pilots, high-touch onboarding
      - **Marketing-Led Growth**: Content marketing, ads, SEO, community building
      - **Partnership-Led Growth**: Integrations, OEM deals, white-label, channel partners
      - **Hybrid**: Combination of above (PLG for SMB, Sales for Enterprise)

      - Listen for: how you'll acquire first 100 customers, channel strategy
      - Store in concept.md § Strategic Positioning → "GTM Strategy: [answer]"
      - **Cross-integration**: If "Sales-Led Growth" selected → recommend uptime_sla=99.9%+ in constitution

   9. **Target Timeline Question**:
      "What's your target timeline to launch MVP?"

      **Options** (use AskUserQuestion with header "Timeline"):
      - **1-3 months**: Rapid prototype, minimal features, accept technical debt
      - **3-6 months**: Solid MVP, core features polished, production-grade
      - **6-12 months**: Full product, polished UX, comprehensive feature set
      - **12+ months**: Complex platform, enterprise-grade, high polish

      - Listen for: urgency, market window, funding runway, scope ambition
      - Store in concept.md § Strategic Positioning → "Timeline: [answer]"

   10. **Success Metric Priority Question**:
       "What's your most important success metric in first year?"

       **Options** (use AskUserQuestion with header "Success Metric"):
       - **User Growth**: MAU, signups, viral coefficient, activation rate
       - **Revenue/ARR**: MRR, ARPU, LTV, net revenue retention
       - **Engagement**: DAU/MAU ratio, retention curves, session time, feature adoption
       - **Market Share**: Competitive displacement, category leadership, brand awareness
       - **Product Quality**: NPS, CSAT, low churn, bug resolution time
       - **Learning/Validation**: Experiments run, hypotheses tested, pivot readiness

       - Listen for: what "winning" looks like, how you'll measure success
       - Store in concept.md § Strategic Positioning → "North Star Metric: [answer]"

   **Output**: Document all 10 answers in "Problem Discovery" and new "Strategic Positioning" sections of concept.md

   #### § Strategic Positioning Section Format

   Add the following new section to concept.md after "§ Problem & Opportunity":

   ```markdown
   ## § Strategic Positioning

   **Purpose**: Define market strategy, competitive positioning, and success metrics to guide product decisions.

   ### Market Position
   [Answer from Q6: Premium/Value/Budget/Niche/Disruptive]

   **Rationale**: [Why this positioning? Evidence from market research]

   **Implications for Product**:
   - Quality expectations: [High/Medium/Low based on positioning]
   - Price positioning: [Premium/Competitive/Budget]
   - Target customer segment: [Enterprise/SMB/Consumer]
   - Feature complexity: [Rich/Balanced/Minimal]

   ### Primary Differentiation
   [Answer from Q7: Technology/UX/Price/Performance/Integration/Service]

   **How we'll win**: [Specific advantages over competitors]

   **Evidence**: [Market gaps, competitor weaknesses, our strengths from research]

   **Competitive Matrix** (from Phase 0b research):
   | Feature/Aspect | Us | Competitor A | Competitor B |
   |----------------|:--:|:------------:|:------------:|
   | [Differentiator] | ✅ Best | ⚠️ Acceptable | ❌ Weak |

   ### Go-to-Market Strategy
   [Answer from Q8: PLG/Sales-Led/Marketing-Led/Partnership-Led/Hybrid]

   **Tactics** (Phase 1 - First 1000 customers):
   - **Channel 1**: [Primary acquisition channel with specific tactics]
   - **Channel 2**: [Secondary channel]
   - **Channel 3**: [Tertiary channel]

   **Success Metrics** (GTM-specific):
   - CAC (Customer Acquisition Cost): [Target range]
   - Conversion rates: [Funnel metrics by channel]
   - Time to first value: [Target onboarding speed]

   **Sales Motion** (if applicable):
   - Sales cycle length: [Target days]
   - Deal size (ACV): [Target range]
   - Sales team structure: [Inside/field/hybrid]

   ### Timeline to Market
   [Answer from Q9: 1-3 months / 3-6 months / 6-12 months / 12+ months]

   **MVP Scope** (based on timeline):
   - [List P1a features aligned with timeline]
   - [Trade-offs made to hit timeline]

   **Milestones**:
   | Milestone | Target Date | Exit Criteria |
   |-----------|-------------|---------------|
   | Alpha | [Date] | [Criteria] |
   | Beta | [Date] | [Criteria] |
   | Launch | [Date] | [Criteria] |

   **Risks**:
   - **Aggressive timeline (1-3m)**: Quality trade-offs, technical debt accumulation
   - **Extended timeline (12m+)**: Market changes, competitor moves, funding runway
   - **Mitigation**: [Specific strategies]

   ### North Star Metric
   [Answer from Q10: User Growth / Revenue / Engagement / Market Share / Quality / Learning]

   **Definition**: [Precise metric definition, e.g., "Monthly Active Users who complete ≥1 core action"]

   **Target** (Year 1): [Specific number, e.g., "10K MAU", "$1M ARR", "40% DAU/MAU"]

   **Why this metric**: [Alignment with business model, stage, and strategy]

   **Leading Indicators** (track weekly):
   - [Metric 1 that predicts North Star]
   - [Metric 2 that predicts North Star]
   - [Metric 3 that predicts North Star]

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

3c. **Product Alternatives Generation** — NEW:

   **Goal**: Generate 3-5 fundamentally different product visions solving the same problem.
   Ensures exploration of design space before committing to one approach.

   **When**: Always run in Discovery Mode. For Capture Mode, skip unless user requests alternatives.

   **Five Generation Strategies**:

   Apply these strategic lenses to generate alternatives:

   1. **Conventional**: Industry standard approach (what competitors do)
   2. **Minimal**: Simplest 80/20 solution (fastest to market)
   3. **Disruptive**: Opposite/contrarian approach (differentiated)
   4. **Premium**: Best-in-class, unlimited budget (quality-first)
   5. **Platform**: Ecosystem/marketplace play (network effects)

   **For EACH strategy**:
   - Formulate 1-2 sentence vision statement
   - List 5-7 core epics/features
   - Define value proposition
   - Identify key differentiators vs competitors
   - List 3 pros and 3 cons
   - Estimate effort (S/M/L/XL) and risk (Low/Med/High)
   - Calculate Time to MVP estimate

   **Scoring** (40 points total):
   - Problem-Solution Fit (30%): 0-12 points
   - Market Differentiation (25%): 0-10 points
   - Feasibility (25%): 0-10 points
   - Time to Market (20%): 0-8 points

   **Use Brainstorm-Curate Protocol**:
   ```text
   IMPORT: templates/shared/quality/brainstorm-curate.md

   BRAINSTORM Phase (divergent):
   - Suspend judgment during generation
   - Use provocative prompts:
     * "What would [Innovative Company] do?"
     * "What if we had zero/unlimited budget?"
     * "What's the opposite of best practices?"
   - Make alternatives concretely different (not just scope variations)

   CURATE Phase (convergent):
   - Score each alternative on 4 criteria
   - Identify potential hybrids
   - Document trade-offs explicitly
   ```

   **Output**: Create `specs/concept-alternatives.md` with:
   - All 5 alternatives documented
   - Comparison matrix with scores
   - Quick summary (highest score, fastest, lowest risk, most differentiated)

   **Quality Check**:
   - At least 3 alternatives generated (5 preferred)
   - Alternatives are meaningfully different (not just MINIMAL/BALANCED/AMBITIOUS scope variants)
   - Each has concrete features, not vague descriptions
   - Scores grounded in evidence from Phases 0a-0c

   **Reference template**: `templates/shared/concept-sections/product-alternatives.md`

3d. **User Selects Preferred Alternative** — NEW:

   **Goal**: User reviews alternatives and selects one to expand into full concept.

   **Interactive Flow**:

   1. **Display Summary**:
      ```markdown
      ## Product Alternatives Summary

      | Alternative | Strategy | Score | MVP Time | Risk | Highlights |
      |-------------|----------|:-----:|:--------:|:----:|------------|
      | 1. [Name] | [Type] | X/40 | X weeks | [L/M/H] | [Key differentiator] |
      | 2. [Name] | [Type] | X/40 | X weeks | [L/M/H] | [Key differentiator] |
      | 3. [Name] | [Type] | X/40 | X weeks | [L/M/H] | [Key differentiator] |
      | 4. [Name] | [Type] | X/40 | X weeks | [L/M/H] | [Key differentiator] |
      | 5. [Name] | [Type] | X/40 | X weeks | [L/M/H] | [Key differentiator] |
      ```

   2. **ASK USER**: "Which alternative would you like to expand into a full concept? (1-5, or ask questions)"

   3. **Allow Questions**: User can ask for clarification about any alternative before deciding

   4. **WAIT** for user selection

   5. **Store Selection**: `SELECTED_ALT = [N]` for use in step 5 (Vision Extraction)

   6. **Confirm**: "I'll expand Alternative [N]: [Name] ([Strategy] approach) into the full concept"

   **Document in Concept**:
   - Add "Product Alternatives" section with selected alternative highlighted
   - Document selection rationale (why this alternative over others)
   - Reference full analysis in `specs/concept-alternatives.md`

   **Output**: Selected alternative index stored for Vision and Feature Hierarchy generation.

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
   - Example: `/speckit.specify EPIC-001.F01.S01, EPIC-001.F01.S02`

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

**Formula**: CQS = (Market × 0.25 + Persona × 0.20 + Metrics × 0.15 + Features × 0.20 + Risk × 0.10 + Technical × 0.10) × 100

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
- ✓ Good: `/speckit.specify EPIC-001.F01.S01, EPIC-001.F01.S02, EPIC-001.F02.S01`
- ✗ Bad: `/speckit.specify EPIC-001.F01.S01, EPIC-001.F02.S01, EPIC-001.F01.S02`

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

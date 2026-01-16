---
name: softlaunch
description: |
  Geographic soft launch framework for mobile games.
  Manages 3-phase regional rollout with KPI thresholds, pivot/kill decision trees,
  and automated go/no-go recommendations based on industry benchmarks.

version: 1.0.0
persona: product-manager-agent
model: opus
thinking_budget: 24000

skills:
  - regional-analytics
  - cohort-analysis
  - ab-testing
  - market-research

flags:
  - name: --thinking-depth
    type: choice
    choices: [quick, standard, ultrathink]
    default: standard
    description: |
      Thinking budget per agent:
      - quick: 16K budget, core KPI analysis, 90s (~$0.12)
      - standard: 32K budget, full analysis with pivot options, 180s (~$0.24) [RECOMMENDED]
      - ultrathink: 96K budget, deep market analysis, 300s (~$0.72)
  - name: --max-model
    type: string
    default: null
    description: "--max-model <opus|sonnet|haiku> - Override model cap"

inputs:
  soft_launch_phase:
    type: enum
    options: [planning, test_market, scale_test, global_prep]
    default: planning
    description: Current phase of soft launch
  test_markets:
    type: array
    items: string
    default: ["PH", "AU", "CA"]
    description: ISO country codes for test markets
  genre:
    type: enum
    options: [casual, mid-core, hardcore, hyper-casual, idle, puzzle, rpg, strategy]
    required: true
    description: Game genre for benchmark selection
  monetization:
    type: enum
    options: [f2p_iap, f2p_ads, hybrid, premium]
    default: f2p_iap
    description: Primary monetization model

outputs:
  - docs/soft-launch/soft-launch-plan.md            # Master plan
  - docs/soft-launch/phase-1-test-market.md         # Phase 1 details
  - docs/soft-launch/phase-2-scale-test.md          # Phase 2 details
  - docs/soft-launch/phase-3-global-prep.md         # Phase 3 details
  - docs/soft-launch/kpi-dashboard.md               # KPI tracking template
  - docs/soft-launch/decision-log.md                # Go/pivot/kill decisions
  - reports/soft-launch/metrics-{{phase}}.json      # Phase metrics

quality_gates:
  - name: QG-SOFTLAUNCH-001
    description: Phase 1 Retention Gate
    condition: "D1 retention meets genre benchmark"
    threshold: "D1 >= benchmark (genre-specific)"
    severity: CRITICAL
  - name: QG-SOFTLAUNCH-002
    description: Phase 2 Monetization Gate
    condition: "ARPDAU meets minimum threshold"
    threshold: "ARPDAU >= $0.03 (genre-adjusted)"
    severity: HIGH
  - name: QG-SOFTLAUNCH-003
    description: Phase 3 LTV/CPI Gate
    condition: "LTV/CPI ratio > 1.0 for sustainable UA"
    threshold: "LTV/CPI > 1.0 (prefer > 1.5)"
    severity: CRITICAL
  - name: QG-SOFTLAUNCH-004
    description: Technical Stability
    condition: "Crash-free rate >= 99.5%"
    threshold: "≥ 99.5%"
    severity: CRITICAL
  - name: QG-SOFTLAUNCH-005
    description: Organic Discovery
    condition: "Organic installs >= 20% of total"
    threshold: "≥ 20% organic"
    severity: MEDIUM

pre_gates:
  - name: QG-SOFTLAUNCH-000
    description: Balance and playtest gates passed
    condition: "QG-BALANCE-* and QG-PLAYTEST-* all passed"
    severity: CRITICAL

inline_gates:
  enabled: true
  gates:
    - id: IG-SOFTLAUNCH-001
      name: Build Readiness
      check: "Production build deployed to test markets"
      severity: CRITICAL
    - id: IG-SOFTLAUNCH-002
      name: Analytics Integration
      check: "Analytics SDK integrated and events firing"
      severity: CRITICAL
    - id: IG-SOFTLAUNCH-003
      name: Store Presence
      check: "Store listings localized for test markets"
      severity: HIGH

handoffs:
  - label: Setup Analytics
    agent: speckit.analytics
    auto: true
    condition:
      - "Phase = planning"
      - "Analytics not yet configured"
  - label: Plan LiveOps
    agent: speckit.liveops
    auto: false
    condition:
      - "Phase 1 passed"
      - "Ready for retention events"
  - label: Global Launch
    agent: speckit.launch
    auto: false
    condition:
      - "All QG-SOFTLAUNCH-* passed"
      - "LTV/CPI > 1.5"
  - label: Iterate
    agent: speckit.balance
    auto: false
    condition:
      - "Metrics below threshold"
      - "Pivot recommended"

claude_code:
  model: opus
  reasoning_mode: extended
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 4000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
        timeout_per_agent: 180000
        retry_on_failure: 1
      pro:
        thinking_budget: 8000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
        timeout_per_agent: 300000
        retry_on_failure: 2
      max:
        thinking_budget: 32000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
        timeout_per_agent: 900000
        retry_on_failure: 3
      ultrathink:
        thinking_budget: 96000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 6.0
  depth_defaults:
    quick:
      thinking_budget: 16000
      skip_agents: [optional-synthesizers]
      timeout: 90
    standard:
      thinking_budget: 32000
      skip_agents: []
      timeout: 180
    ultrathink:
      thinking_budget: 96000
      additional_agents: [market-deepdive, pivot-strategist]
      timeout: 300
  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 32000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (96K thinking budget).
          Auto-downgrading to **Standard** mode (32K budget).
  cost_breakdown:
    quick: {cost: $0.12, time: "90-120s"}
    standard: {cost: $0.24, time: "180-240s"}
    ultrathink: {cost: $0.72, time: "300-360s"}
  cache_control:
    system_prompt: ephemeral
    constitution: ephemeral
    templates: ephemeral
    artifacts: ephemeral
    ttl: session
  cache_hierarchy: full
  orchestration:
    max_parallel: 5
    conflict_resolution: queue
    timeout_per_agent: 600000
    retry_on_failure: 2
  operation_batching:
    enabled: true
    skip_flag: "--sequential"
    framework: templates/shared/operation-batching.md

  subagents:
    # Wave 1: Planning (parallel)
    - role: market-selector
      role_group: STRATEGY
      parallel: true
      depends_on: []
      priority: 10
      model_override: opus
      prompt: |
        Select and validate test markets for soft launch.

        Based on genre and monetization:

        1. **Recommend Test Markets**:
           Phase 1 (Test Market): 1-2 countries
           - Low CPI, representative demographics
           - English-speaking for initial feedback
           - Recommendations by genre:
             * Casual: Philippines, Australia, New Zealand
             * Mid-Core: Canada, Australia, Nordic countries
             * RPG: Canada, Australia, Singapore
             * Hyper-Casual: Brazil, India, Philippines

        2. **Scale Markets** (Phase 2):
           - Add 3-5 more countries
           - Include one high-LTV market (US/UK proxy)
           - Include one high-volume market (BR/IN)

        3. **Market Profile per Country**:
           | Country | CPI Range | LTV Potential | Volume | Pros | Cons |
           |---------|-----------|---------------|--------|------|------|

        4. **Timeline Recommendations**:
           - Phase 1: 2-4 weeks (find PMF)
           - Phase 2: 4-8 weeks (optimize)
           - Phase 3: 2-4 weeks (scale prep)

        OUTPUT: docs/soft-launch/soft-launch-plan.md (market section)

    - role: benchmark-loader
      role_group: DATA
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Load genre-specific benchmarks for soft launch KPIs.

        **Industry Benchmarks by Genre**:

        CASUAL:
        - D1: 35-45%
        - D7: 12-18%
        - D30: 4-8%
        - ARPDAU: $0.05-0.15
        - LTV (D30): $0.50-2.00

        MID-CORE:
        - D1: 30-40%
        - D7: 10-15%
        - D30: 3-6%
        - ARPDAU: $0.10-0.30
        - LTV (D30): $1.00-5.00

        RPG:
        - D1: 25-35%
        - D7: 8-12%
        - D30: 2-5%
        - ARPDAU: $0.15-0.50
        - LTV (D30): $2.00-10.00

        HYPER-CASUAL:
        - D1: 40-50%
        - D7: 8-12%
        - D30: 1-3%
        - ARPDAU: $0.02-0.06 (ads)
        - LTV (D30): $0.10-0.50

        IDLE:
        - D1: 35-45%
        - D7: 15-20%
        - D30: 5-10%
        - ARPDAU: $0.08-0.20
        - LTV (D30): $1.00-4.00

        **Top Performer Benchmarks (Supercell/King)**:
        - D1: 40%+
        - D7: 20%+
        - D30: 10%+
        - ARPDAU: $0.15-0.30
        - LTV (D30): $3.00+
        - Conversion: 5%+
        - Crash-free: 99.9%+

        OUTPUT: Benchmark config for gate validation

    - role: kpi-planner
      role_group: STRATEGY
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Create KPI tracking framework for soft launch.

        Define metrics to track per phase:

        **Phase 1 (Product-Market Fit)**:
        Focus: Retention, Engagement
        - D1/D3/D7 retention
        - Session length, sessions/day
        - Tutorial completion rate
        - Core loop engagement
        - NPS (qualitative)

        **Phase 2 (Monetization)**:
        Focus: Revenue, Conversion
        - ARPDAU, ARPPU
        - Conversion rate
        - IAP revenue distribution
        - Ad revenue (if applicable)
        - Whale/dolphin ratio

        **Phase 3 (Scale Readiness)**:
        Focus: Unit Economics, Scale
        - LTV (D7, D30, projected)
        - CPI by channel
        - LTV/CPI ratio
        - Organic rate
        - K-factor

        **Always Track**:
        - DAU/MAU
        - Crash-free rate
        - Load time
        - Error rates
        - Support tickets

        OUTPUT: docs/soft-launch/kpi-dashboard.md

    # Wave 2: Phase Documents (parallel)
    - role: phase1-designer
      role_group: PLANNING
      parallel: true
      depends_on: [market-selector, benchmark-loader, kpi-planner]
      priority: 20
      model_override: opus
      prompt: |
        Create Phase 1: Test Market plan.

        docs/soft-launch/phase-1-test-market.md:

        ## Phase 1: Test Market (Product-Market Fit)

        ### Objective
        Validate core gameplay resonates with target audience.

        ### Markets
        {{SELECTED_MARKETS}}

        ### Duration
        2-4 weeks

        ### Entry Criteria
        - [ ] Production build deployed
        - [ ] Analytics integrated
        - [ ] Store listing live
        - [ ] Support channels ready

        ### KPI Targets

        | Metric | Minimum | Target | Top 10% |
        |--------|---------|--------|---------|
        | D1 | {{MIN}} | {{TARGET}} | {{TOP}} |
        | D7 | {{MIN}} | {{TARGET}} | {{TOP}} |
        | Tutorial | 70% | 80% | 90% |
        | Session | 5 min | 8 min | 12 min |
        | Crash-free | 99% | 99.5% | 99.9% |

        ### Decision Tree

        ```
        IF D1 >= Target:
          IF D7 >= Target:
            → PROCEED to Phase 2
          ELSE:
            → ITERATE (engagement focus)
        ELSE IF D1 >= Minimum:
          → ITERATE (FTUE optimization)
        ELSE:
          → PIVOT or KILL
        ```

        ### Exit Criteria
        - [ ] D1 >= {{MINIMUM}}%
        - [ ] Tutorial >= 70%
        - [ ] No P0 bugs
        - [ ] Clear iteration plan OR proceed decision

    - role: phase2-designer
      role_group: PLANNING
      parallel: true
      depends_on: [market-selector, benchmark-loader, kpi-planner]
      priority: 20
      model_override: opus
      prompt: |
        Create Phase 2: Scale Test plan.

        docs/soft-launch/phase-2-scale-test.md:

        ## Phase 2: Scale Test (Monetization Validation)

        ### Objective
        Validate monetization and optimize for LTV.

        ### Markets
        Add: {{SCALE_MARKETS}}
        Total: {{TOTAL_MARKETS}}

        ### Duration
        4-8 weeks

        ### Entry Criteria
        - [ ] Phase 1 passed
        - [ ] Monetization features complete
        - [ ] A/B testing framework ready
        - [ ] LiveOps events planned

        ### KPI Targets

        | Metric | Minimum | Target | Top 10% |
        |--------|---------|--------|---------|
        | D30 | {{MIN}} | {{TARGET}} | {{TOP}} |
        | ARPDAU | {{MIN}} | {{TARGET}} | {{TOP}} |
        | Conversion | 2% | 4% | 6% |
        | ARPPU | {{MIN}} | {{TARGET}} | {{TOP}} |

        ### A/B Tests to Run
        1. Pricing tiers
        2. First-time buyer offer
        3. Ad placement (if hybrid)
        4. Battle Pass structure
        5. Event frequency

        ### Decision Tree

        ```
        IF ARPDAU >= Target:
          IF D30 >= Target:
            → PROCEED to Phase 3
          ELSE:
            → ITERATE (retention focus)
        ELSE IF ARPDAU >= Minimum:
          → ITERATE (monetization optimization)
        ELSE:
          → PIVOT monetization model
        ```

        ### Exit Criteria
        - [ ] ARPDAU >= {{MINIMUM}}
        - [ ] D30 >= {{MINIMUM}}%
        - [ ] Monetization funnel optimized
        - [ ] LTV projection calculable

    - role: phase3-designer
      role_group: PLANNING
      parallel: true
      depends_on: [market-selector, benchmark-loader, kpi-planner]
      priority: 20
      model_override: opus
      prompt: |
        Create Phase 3: Global Prep plan.

        docs/soft-launch/phase-3-global-prep.md:

        ## Phase 3: Global Prep (Scale Validation)

        ### Objective
        Validate unit economics and UA scalability.

        ### Markets
        Add: High-value markets (US, UK, JP, KR proxies)
        Total: {{TOTAL_MARKETS}}

        ### Duration
        2-4 weeks

        ### Entry Criteria
        - [ ] Phase 2 passed
        - [ ] UA budget allocated
        - [ ] Creative assets ready
        - [ ] Localization complete

        ### KPI Targets

        | Metric | Minimum | Target | Top 10% |
        |--------|---------|--------|---------|
        | LTV (D30) | {{MIN}} | {{TARGET}} | {{TOP}} |
        | CPI | < {{MAX}} | < {{TARGET}} | < {{MIN}} |
        | LTV/CPI | > 1.0 | > 1.5 | > 2.0 |
        | Organic | 15% | 25% | 40% |

        ### UA Channels to Test
        1. Facebook/Meta
        2. Google UAC
        3. TikTok
        4. Unity Ads
        5. AppLovin
        6. Influencer

        ### Decision Tree

        ```
        IF LTV/CPI > 1.5:
          → GLOBAL LAUNCH
        ELSE IF LTV/CPI > 1.0:
          IF Organic > 20%:
            → GLOBAL LAUNCH (conservative)
          ELSE:
            → ITERATE (UA optimization)
        ELSE:
          → DO NOT LAUNCH
          → PIVOT or KILL
        ```

        ### Exit Criteria
        - [ ] LTV/CPI > 1.0 (minimum) or > 1.5 (confident)
        - [ ] UA strategy validated
        - [ ] Scale infrastructure ready
        - [ ] Global launch plan finalized

    # Wave 3: Decision Framework
    - role: decision-architect
      role_group: STRATEGY
      parallel: false
      depends_on: [phase1-designer, phase2-designer, phase3-designer]
      priority: 30
      model_override: opus
      prompt: |
        Create decision framework and log template.

        docs/soft-launch/decision-log.md:

        ## Soft Launch Decision Framework

        ### Decision Types

        **GO**: Proceed to next phase
        - All gate metrics met
        - Clear positive trajectory
        - Team confident

        **ITERATE**: Stay in phase, make changes
        - Some metrics below target but above minimum
        - Clear improvement hypothesis
        - Max 2-3 iterations per phase

        **PIVOT**: Fundamental change
        - Core metrics failing
        - Clear alternative direction
        - Requires re-validation

        **KILL**: Stop development
        - No path to viable metrics
        - Multiple pivots failed
        - Better opportunities elsewhere

        ### Decision Log

        | Date | Phase | Metrics | Decision | Rationale | Owner |
        |------|-------|---------|----------|-----------|-------|
        | YYYY-MM-DD | 1 | D1: XX% | GO/ITERATE/PIVOT/KILL | {{WHY}} | {{WHO}} |

        ### Pivot Criteria

        Pivot if:
        - D1 < minimum after 2 FTUE iterations
        - ARPDAU < minimum after 3 monetization tests
        - LTV/CPI < 0.8 after UA optimization

        Kill if:
        - 3+ pivots without improvement
        - Core loop fundamentally unfun
        - Market opportunity closed
        - Team morale/budget exhausted

        ### Example Decision

        ```markdown
        ## Decision: 2026-01-15 (Phase 1, Week 2)

        **Metrics**:
        - D1: 32% (target: 35%, minimum: 28%)
        - D7: 11% (target: 15%, minimum: 10%)
        - Tutorial: 78%

        **Decision**: ITERATE

        **Rationale**:
        D1 above minimum but below target. Tutorial completion shows friction.
        D7 at minimum suggests engaged users stay, but funnel is narrow.

        **Action Plan**:
        1. Simplify tutorial (remove steps 3-4)
        2. Add skip option for returning players
        3. A/B test first reward timing

        **Success Criteria for Next Check**:
        - D1 >= 35%
        - Tutorial >= 85%

        **Timeline**: 1 week, then reassess
        ```

flags:
  phase: "--phase <1|2|3>"                         # Focus on specific phase
  markets: "--markets <PH,AU,CA>"                  # Override test markets
  benchmark_tier: "--benchmark <minimum|target|top>"  # Comparison tier
  analyze: "--analyze <metrics-file>"              # Analyze existing data
  decision: "--decision <go|iterate|pivot|kill>"  # Log a decision
  export: "--export <pdf|notion|confluence>"       # Export reports
  max_model: "--max-model <opus|sonnet|haiku>"     # Override model cap
---

# /speckit.softlaunch - Geographic Soft Launch Framework

## Purpose

The `/speckit.softlaunch` command provides a structured framework for mobile game soft launches, including:

1. **Market Selection**: Data-driven test market recommendations
2. **Phase Planning**: 3-phase rollout with clear gates
3. **KPI Tracking**: Genre-specific benchmarks and targets
4. **Decision Framework**: Go/Iterate/Pivot/Kill criteria
5. **Documentation**: Audit trail for all decisions

## When to Use

- **Pre-Soft Launch**: Create soft launch strategy
- **During Soft Launch**: Track metrics and make decisions
- **Phase Transitions**: Document go/no-go decisions
- **Post-Mortem**: Analyze soft launch performance

## Soft Launch Phases

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOFT LAUNCH TIMELINE                         │
│                                                                  │
│  Phase 1          Phase 2           Phase 3         Global      │
│  Test Market      Scale Test        Global Prep     Launch      │
│  ┌────────┐      ┌──────────┐      ┌──────────┐   ┌──────────┐ │
│  │2-4 wks │  →   │ 4-8 wks  │  →   │ 2-4 wks  │ → │ LAUNCH!  │ │
│  │        │      │          │      │          │   │          │ │
│  │ PMF    │      │ Monetize │      │ UA Scale │   │ Scale    │ │
│  └────────┘      └──────────┘      └──────────┘   └──────────┘ │
│                                                                  │
│  Focus:           Focus:            Focus:                       │
│  - Retention      - ARPDAU          - LTV/CPI                   │
│  - Engagement     - Conversion      - Organic %                 │
│  - FTUE           - A/B tests       - UA channels               │
│                                                                  │
│  Markets:         Markets:          Markets:                     │
│  1-2 countries    3-7 countries     Include high-value          │
│  (PH, AU, NZ)     (Add CA, BR)      (US/UK proxy)               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Market Selection

### Recommended Test Markets by Genre

| Genre | Phase 1 | Phase 2 | Phase 3 |
|-------|---------|---------|---------|
| **Casual** | PH, AU | +NZ, CA, BR | +UK, DE |
| **Mid-Core** | CA, AU | +NZ, SG, PH | +UK, KR |
| **RPG** | CA, AU | +SG, TW, PH | +UK, JP |
| **Hyper-Casual** | PH, BR | +IN, MX, ID | +US, UK |
| **Idle** | AU, NZ | +CA, PH, SG | +UK, DE |

### Market Profiles

| Country | CPI | LTV | Volume | Best For |
|---------|-----|-----|--------|----------|
| **PH** (Philippines) | $0.10-0.30 | Low | High | Volume testing |
| **AU** (Australia) | $1.50-3.00 | High | Low | Quality signal |
| **CA** (Canada) | $2.00-4.00 | High | Med | US proxy |
| **NZ** (New Zealand) | $1.00-2.00 | Med | Low | Quick iterations |
| **SG** (Singapore) | $1.50-3.00 | High | Low | Asia proxy |
| **BR** (Brazil) | $0.20-0.50 | Low | High | LATAM testing |

## Genre Benchmarks

### Retention Benchmarks

| Genre | D1 Min | D1 Target | D7 Min | D7 Target | D30 Min | D30 Target |
|-------|--------|-----------|--------|-----------|---------|------------|
| Casual | 30% | 40% | 10% | 15% | 3% | 6% |
| Mid-Core | 25% | 35% | 8% | 12% | 2% | 5% |
| RPG | 20% | 30% | 6% | 10% | 2% | 4% |
| Hyper-Casual | 35% | 45% | 6% | 10% | 1% | 2% |
| Idle | 30% | 40% | 12% | 18% | 4% | 8% |

### Monetization Benchmarks

| Genre | ARPDAU Min | ARPDAU Target | Conv Min | Conv Target |
|-------|------------|---------------|----------|-------------|
| Casual | $0.03 | $0.08 | 2% | 4% |
| Mid-Core | $0.08 | $0.20 | 3% | 5% |
| RPG | $0.12 | $0.35 | 2% | 4% |
| Hyper-Casual | $0.02 | $0.04 | N/A (ads) | N/A |
| Idle | $0.05 | $0.12 | 3% | 5% |

### Top Performer Benchmarks (Supercell/King Level)

| Metric | Supercell | King | Industry Top 10% |
|--------|-----------|------|------------------|
| D1 | 45%+ | 40%+ | 40%+ |
| D7 | 25%+ | 20%+ | 18%+ |
| D30 | 12%+ | 10%+ | 8%+ |
| ARPDAU | $0.25+ | $0.15+ | $0.15+ |
| Conversion | 6%+ | 5%+ | 5%+ |
| LTV (D30) | $4.00+ | $2.50+ | $2.00+ |

## Quality Gates

### QG-SOFTLAUNCH-001: Phase 1 Retention

**Purpose**: Validate product-market fit

**Threshold**: D1 >= genre-specific minimum

| Genre | Minimum | Target |
|-------|---------|--------|
| Casual | 30% | 40% |
| Mid-Core | 25% | 35% |
| RPG | 20% | 30% |
| Hyper-Casual | 35% | 45% |

**If Failed**:
- Analyze FTUE drop-offs
- A/B test tutorial changes
- Review first session experience
- Consider core loop changes

### QG-SOFTLAUNCH-002: Phase 2 Monetization

**Purpose**: Validate revenue potential

**Threshold**: ARPDAU >= genre-specific minimum

**If Failed**:
- Analyze monetization funnel
- A/B test pricing
- Review IAP value perception
- Consider monetization model change

### QG-SOFTLAUNCH-003: Phase 3 Unit Economics

**Purpose**: Validate sustainable UA

**Threshold**: LTV/CPI > 1.0 (minimum), > 1.5 (confident)

```
LTV/CPI Interpretation:
< 0.8  → DO NOT LAUNCH (losing money)
0.8-1.0 → Risky (needs optimization)
1.0-1.5 → Viable (proceed cautiously)
1.5-2.0 → Good (proceed confidently)
> 2.0  → Excellent (scale aggressively)
```

**If Failed**:
- Optimize CPI (creative, targeting)
- Improve LTV (retention, monetization)
- Focus on organic growth
- Consider niche launch

### QG-SOFTLAUNCH-004: Technical Stability

**Purpose**: Ensure production readiness

**Threshold**: Crash-free rate >= 99.5%

**Additional Checks**:
- Load time < 5 seconds
- Error rate < 1%
- Server uptime > 99.9%

### QG-SOFTLAUNCH-005: Organic Discovery

**Purpose**: Validate market pull

**Threshold**: Organic installs >= 20% of total

**Why Important**:
- Indicates word-of-mouth potential
- Reduces UA dependency
- Signals strong retention (viral loop)

## Decision Framework

### Decision Tree

```
START
│
├── Phase 1: Test Market
│   │
│   ├── D1 >= Target?
│   │   ├── YES → Check D7
│   │   │         ├── D7 >= Target? → GO to Phase 2
│   │   │         └── D7 < Target? → ITERATE (engagement)
│   │   │
│   │   └── NO (D1 < Target)
│   │       ├── D1 >= Minimum? → ITERATE (FTUE)
│   │       └── D1 < Minimum? → PIVOT or KILL
│   │
│   └── Max 3 iterations, then decision required
│
├── Phase 2: Scale Test
│   │
│   ├── ARPDAU >= Target?
│   │   ├── YES → Check D30
│   │   │         ├── D30 >= Target? → GO to Phase 3
│   │   │         └── D30 < Target? → ITERATE (retention)
│   │   │
│   │   └── NO (ARPDAU < Target)
│   │       ├── ARPDAU >= Minimum? → ITERATE (monetization)
│   │       └── ARPDAU < Minimum? → PIVOT model
│   │
│   └── Max 3 iterations
│
├── Phase 3: Global Prep
│   │
│   ├── LTV/CPI > 1.5?
│   │   └── YES → GLOBAL LAUNCH
│   │
│   ├── LTV/CPI > 1.0?
│   │   ├── Organic > 20%? → LAUNCH (conservative)
│   │   └── Organic < 20%? → ITERATE (UA)
│   │
│   └── LTV/CPI < 1.0? → DO NOT LAUNCH
│
END
```

### Pivot Criteria

**When to Pivot**:
1. D1 < minimum after 2 FTUE iterations
2. ARPDAU < minimum after 3 monetization A/B tests
3. Core loop feedback consistently negative
4. Technical architecture blocking improvements

**Pivot Options**:
| Issue | Pivot Option |
|-------|--------------|
| Low D1 | Redesign FTUE, simplify mechanics |
| Low D7 | Add meta progression, daily hooks |
| Low ARPDAU | Change monetization model |
| Low conversion | Adjust pricing, add starter packs |
| High CPI | New creative strategy, niche targeting |

### Kill Criteria

**When to Kill**:
1. 3+ pivots without meaningful improvement
2. Core gameplay fundamentally unfun (NPS < 0)
3. Technical debt insurmountable
4. Market window closed
5. Better opportunities available

**Kill Decision Checklist**:
- [ ] All reasonable pivots attempted
- [ ] Data clearly shows no path to success
- [ ] Team alignment on decision
- [ ] Learnings documented
- [ ] Assets salvageable for future projects?

## KPI Dashboard Template

```markdown
# Soft Launch KPI Dashboard

**Game**: {{GAME_NAME}}
**Phase**: {{CURRENT_PHASE}}
**Markets**: {{ACTIVE_MARKETS}}
**Date Range**: {{START_DATE}} - {{END_DATE}}

---

## Key Metrics Summary

| Metric | Current | Target | Status | Trend |
|--------|---------|--------|--------|-------|
| D1 | XX% | XX% | ✅/⚠️/❌ | ↑/→/↓ |
| D7 | XX% | XX% | ✅/⚠️/❌ | ↑/→/↓ |
| D30 | XX% | XX% | ✅/⚠️/❌ | ↑/→/↓ |
| ARPDAU | $X.XX | $X.XX | ✅/⚠️/❌ | ↑/→/↓ |
| LTV (D30) | $X.XX | $X.XX | ✅/⚠️/❌ | ↑/→/↓ |
| CPI | $X.XX | $X.XX | ✅/⚠️/❌ | ↑/→/↓ |
| LTV/CPI | X.XX | >1.5 | ✅/⚠️/❌ | ↑/→/↓ |

---

## Retention Curve

```
Day    D0    D1    D3    D7    D14   D30
     ─────┬─────┬─────┬─────┬─────┬─────
     100% │ XX% │ XX% │ XX% │ XX% │ XX%
          │     │     │     │     │
Current   ████████████████████████████
Target    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

---

## Monetization Funnel

```
                    ┌─────────────────┐
                    │  DAU: {{N}}     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Store Views: X% │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Conversions: X% │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Revenue: $XXX   │
                    └─────────────────┘
```

---

## A/B Test Results

| Test | Variant A | Variant B | Winner | Lift |
|------|-----------|-----------|--------|------|
| {{TEST_NAME}} | XX% | XX% | A/B | +X% |

---

## Action Items

- [ ] {{ACTION_1}}
- [ ] {{ACTION_2}}
- [ ] {{ACTION_3}}

## Next Decision Point

**Date**: {{DATE}}
**Criteria**: {{CRITERIA}}
```

## Example Output

```
/speckit.softlaunch --phase=planning --genre=mid-core --markets="CA,AU"

✅ Wave 1: Planning
   ├── Selected markets: CA (primary), AU (secondary)
   ├── Loaded mid-core benchmarks
   └── Created KPI framework

📋 Soft Launch Plan Summary:

   Phase 1 (Test Market):
   - Markets: CA, AU
   - Duration: 3 weeks
   - Focus: D1 >= 25%, D7 >= 8%

   Phase 2 (Scale Test):
   - Add: NZ, SG, PH
   - Duration: 6 weeks
   - Focus: ARPDAU >= $0.08, D30 >= 2%

   Phase 3 (Global Prep):
   - Add: UK (US proxy)
   - Duration: 3 weeks
   - Focus: LTV/CPI > 1.5

✅ Wave 2: Phase Documents Generated
   ├── phase-1-test-market.md
   ├── phase-2-scale-test.md
   └── phase-3-global-prep.md

✅ Wave 3: Decision Framework
   └── decision-log.md

📁 Generated Artifacts:
   ├── docs/soft-launch/soft-launch-plan.md
   ├── docs/soft-launch/phase-1-test-market.md
   ├── docs/soft-launch/phase-2-scale-test.md
   ├── docs/soft-launch/phase-3-global-prep.md
   ├── docs/soft-launch/kpi-dashboard.md
   └── docs/soft-launch/decision-log.md

🔗 Recommended Handoffs:
   → /speckit.analytics (Setup tracking before Phase 1)
   → /speckit.liveops (Plan retention events for Phase 2)
```

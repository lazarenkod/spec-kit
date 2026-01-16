---
name: games.concept
version: 0.1.0
description: Autonomous mobile game concept generation with 5 genre variants (Sorting, Match-3, Idle, Arcade, Puzzle)
persona: game-designer-agent
model: opus
thinking_budget: 120000
reasoning_mode: extended
priority: P0

plan_mode:
  enabled: true
  ultrathink:
    thinking_budget: 120000
    max_parallel: 4
    batch_delay: 3000
    wave_overlap_threshold: 0.75
    cost_multiplier: 3.5

depth_defaults:
  quick:
    agents: 3
    timeout: 60
    thinking_budget: 32000
  standard:
    agents: 5
    timeout: 180
    thinking_budget: 80000
  world-class:
    agents: 12
    timeout: 300
    thinking_budget: 120000

depth_levels:
  quick:
    description: "Fast prototyping with minimal research (3 agents, 60s timeout)"
    agents_included: [market-benchmarker, competitive-analyst, genre-researcher]
    use_case: "Rapid idea validation, early exploration"
    max_thinking_per_agent: 32000

  standard:
    description: "Balanced research depth (5 agents, 180s timeout)"
    agents_included: [market-benchmarker, competitive-analyst, monetization-researcher, genre-researcher, retention-researcher]
    use_case: "Most game concepts, production planning"
    max_thinking_per_agent: 80000

  world-class:
    description: "Maximum research depth (12 agents, 300s timeout)"
    agents_included: [market-benchmarker, competitive-analyst, monetization-researcher, viral-mechanics-researcher, retention-researcher, genre-researcher, player-psychology-researcher, economy-simulator, player-archetype-researcher, platform-roadmap-researcher, liveops-feasibility-researcher, cultural-localization-researcher]
    use_case: "High-budget projects, critical decisions, AAA studio-grade artifacts"
    max_thinking_per_agent: 120000

user_tier_fallback:
  enabled: true
  description: "Auto-fallback for non-Claude Code Max users"
  rules:
    - condition: "user_tier != 'max' AND requested_depth == 'world-class'"
      fallback_depth: "standard"
      fallback_thinking: 80000
      warning_message: |
        ⚠️  **World-class mode requires Claude Code Max tier** (120K thinking budget per agent).
        Your current tier allows 80K thinking. Auto-downgrading to **Standard** mode for this concept.
        
        **World-class features you'll miss**:
        - Viral mechanics research (K-factor analysis)
        - Advanced player psychology (Bartle + SDT framework)
        - Live ops feasibility assessment
        - Cultural localization research
        
        **Recommendation**: Upgrade to Claude Code Max for world-class game concepts.
        💡 Standard mode is excellent for 95% of game concepts.

    - condition: "user_tier == 'free' AND requested_depth == 'standard'"
      fallback_depth: "quick"
      fallback_thinking: 32000
      warning_message: |
        ⚠️  **Standard mode limited for Free tier** (32K thinking budget per agent).
        Auto-downgrading to **Quick** mode for baseline concept.
        
        **Standard features you'll miss**:
        - Monetization research
        - Retention mechanics design
        - Economy simulation
        
        **Recommendation**: Free tier is perfect for rapid idea validation.
        Upgrade to Pro for production-ready concepts.

# Phase 5 v0.9.8: Cost breakdown and transparency
cost_breakdown:
  enabled: true
  show_before_execution: true
  calculation:
    quick:
      agents: 3
      thinking_per_agent: 32000
      total_thinking: 96000  # 3 × 32K
      estimated_cost_usd: 0.40
      execution_time: "60-90s"

    standard:
      agents: 5
      thinking_per_agent: 80000
      total_thinking: 400000  # 5 × 80K
      estimated_cost_usd: 2.00
      execution_time: "180-240s"

    world-class:
      agents: 12
      thinking_per_agent: 120000
      total_thinking: 1440000  # 12 × 120K
      estimated_cost_usd: 7.20  # 3.5× cost multiplier
      execution_time: "300-420s"

  warning_threshold_usd: 2.00  # Warn if cost > $2

# Cost warning configuration
cost_warning:
  enabled: true
  threshold_usd: 2.00
  warning_message_template: |
    ⚠️  **HIGH COST OPERATION DETECTED**

    This execution will cost approximately **${COST} USD**.

    **Details**:
    - Depth: {DEPTH}
    - Genre: {GENRE}
    - Agents: {AGENT_COUNT}
    - Thinking budget: {THINKING_BUDGET}K per agent
    - Total thinking tokens: {TOTAL_TOKENS}

    **Cost breakdown**:
    - Thinking: {THINKING_COST} USD
    - Context: {CONTEXT_COST} USD
    - Output: {OUTPUT_COST} USD

    💡 **To reduce cost**:
    - Use --depth=standard instead of world-class (-72% cost)
    - Use --genre=single instead of all 5 variants (-80% cost)

    ❓ **Continue anyway?** [Y/n]

inputs:
  game_idea:
    type: string
    required: true
    description: High-level game idea (1-3 sentences describing core concept)
    example: "A zen puzzle game where players organize colorful objects into satisfying patterns"

  target_audience:
    type: string
    default: "casual mobile gamers 25-45"
    description: Target player demographic
    examples:
      - "casual mobile gamers 25-45"
      - "hardcore RPG players 18-35"
      - "family-friendly all ages"

  platform:
    type: enum
    options: [ios, android, cross-platform]
    default: cross-platform
    description: Target platform(s)

  monetization_preference:
    type: enum
    options: [f2p-ads, f2p-iap, hybrid, premium]
    default: hybrid
    description: Preferred monetization model
    details:
      f2p-ads: "Ad-supported free-to-play (hyper-casual)"
      f2p-iap: "In-app purchases focused (mid-core)"
      hybrid: "Mix of ads and IAP (casual)"
      premium: "Paid download (premium indie)"

  complexity_budget:
    type: enum
    options: [hyper-casual, casual, mid-core]
    default: casual
    description: Game complexity level
    details:
      hyper-casual: "2-5 min sessions, minimal meta"
      casual: "10-15 min sessions, light meta"
      mid-core: "20-30 min sessions, deep meta"

flags:
  depth:
    type: enum
    options: [quick, standard, world-class]
    default: standard
    description: |
      Research depth level:
      - quick: 3 agents, 60s timeout (~$0.40)
      - standard: 5 agents, 180s timeout (~$2.00)
      - world-class: 12 agents, 300s timeout (~$7.20)

  genre:
    type: enum
    options: [sorting, match3, idle, arcade, puzzle, all]
    default: all
    description: Generate specific genre or all 5 variants

  dry-run:
    type: boolean
    default: false
    description: |
      Show estimated token cost and execution plan without running.
      Useful for budget planning and understanding what will execute.

outputs:
  - specs/game-concept.md                    # Auto-selected highest CQS-Game
  - specs/alternatives/01-sorting.md          # Sorting game variant
  - specs/alternatives/02-match3.md           # Match-3 variant
  - specs/alternatives/03-idle.md             # Idle game variant
  - specs/alternatives/04-arcade.md           # Arcade variant
  - specs/alternatives/05-puzzle.md           # Puzzle variant
  - specs/game-alternatives.md                # Comparison table
  - specs/quality-report.md                   # CQS-Game breakdown
  - specs/concept-research.md                 # Market research findings

quality_gates:
  - name: QG-GCONCEPT-001
    description: CQS-Game Threshold
    condition: "CQS-Game score >= 85/120"
    severity: HIGH
    rationale: "Mobile game market is highly competitive, stricter threshold than B2B concepts"

  - name: QG-GCONCEPT-002
    description: Genre Fit Validation
    condition: "Core mechanics align with genre best practices"
    threshold: ">=80% alignment"
    severity: HIGH
    validation: "Compare against genre templates in templates/shared/game-genres/"

  - name: QG-GCONCEPT-003
    description: Monetization Ethics
    condition: "No predatory patterns (GAM-004 compliance)"
    threshold: "0 violations"
    severity: CRITICAL
    references: ["memory/domains/quality-gates.md GAM-004"]

handoffs:
  - label: Design Game Mechanics
    agent: speckit.games.mechanics
    auto: false
    condition: ["CQS-Game >= 85", "User approves concept"]
    description: "Detailed mechanics design and prototyping"

  - label: Generate GDD
    agent: speckit.gdd
    auto: false
    condition: ["Concept approved"]
    description: "Create full Game Design Document"

  - label: Switch Variant
    agent: speckit.concept.switch
    auto: false
    description: "Switch to different genre variant (1-5)"

workflow:
  phases:
    - phase: 0
      name: Context Extraction
      agents: 1
      parallel: false

    - phase: 1
      name: Deep Research
      agents: 3-7 (based on depth flag)
      parallel: true

    - phase: 2
      name: Genre Variant Generation
      agents: 5 (or 1 if specific genre)
      parallel: true

    - phase: 3
      name: Quality Validation
      agents: 1
      parallel: false

    - phase: 4
      name: File Generation
      agents: 1
      parallel: false

---

# Game Concept Generation Command

**Purpose**: Autonomous mobile game concept generation with 5 genre-based variants

**Target Users**: Game designers, indie developers, studios exploring new game ideas

# `/speckit.games.concept` — Game Concept Generation

## Overview

This command generates comprehensive mobile game concepts with 5 genre-based variants. Unlike `/speckit.concept` which focuses on business strategies, `/speckit.games.concept` is optimized for mobile game development with:

- **Genre-based variants**: Sorting, Match-3, Idle, Arcade, Puzzle (instead of Conventional, Minimal, Disruptive, Premium, Platform)
- **CQS-Game scoring**: 9-component formula (0-120 scale) focused on game-specific metrics
- **Game research agents**: 10 specialized agents for KPI benchmarks, retention, monetization
- **Stricter threshold**: CQS-Game ≥ 85/120 (vs CQS-E's 80/120)

## When to Use

**✅ Use `/speckit.games.concept` when:**
- Creating a new mobile game from scratch
- Exploring different genre approaches for one core idea
- Need CEO-focused GDD with market research
- Large project with 50+ requirements
- Seeking data-driven genre recommendation

**❌ Do NOT use when:**
- Game concept already well-defined (use `/speckit.gdd` directly)
- Working on existing game features (use `/speckit.specify`)
- Need quick mechanics prototyping (use `/speckit.games.mechanics`)

## Usage Examples

```bash
# Generate single variant with standard research (default, fast)
/speckit.games.concept --depth=standard

# Quick mode for rapid idea validation (3 agents, 60s)
/speckit.games.concept --depth=quick --genre=match3

# All 5 genre variants for comparison
/speckit.games.concept --depth=standard --genre=all

# World-class research for high-budget project (12 agents, 120K thinking)
# Auto-downgrade applies if not Claude Code Max tier
/speckit.games.concept --depth=world-class --genre=all
```

## User Tier Auto-Fallback (NEW v0.5.0)

**OPTIMIZATION**: If you request `--depth=world-class` but don't have Claude Code Max tier, this command automatically downgrades to `--depth=standard` with an explanatory warning message.

**Why**: World-class mode requires 120K thinking budget per agent. Tier limits:
- **Free tier**: 16K thinking max → auto-fallback to Quick mode
- **Pro tier**: 32K thinking max → auto-fallback to Quick mode
- **Max tier**: 120K thinking max → world-class available

**What you get**:
- ✅ Your concept still generates successfully
- ✅ No payment surprises from unexpectedly high token consumption
- ✅ Clear warning message explaining what features were skipped
- ✅ Upgrade recommendations if you want world-class

**Example fallback message**:
```
⚠️  World-class mode requires Claude Code Max tier (120K thinking budget per agent).
Your current tier allows 80K thinking. Auto-downgrading to Standard mode for this concept.

World-class features you'll miss:
- Viral mechanics research (K-factor analysis)
- Advanced player psychology (Bartle + SDT framework)
- Live ops feasibility assessment
- Cultural localization research

Recommendation: Upgrade to Claude Code Max for world-class game concepts.
```

## Agent Architecture

### Phase 0: Context Extraction (Priority 5)

Single agent extracts game parameters from user input:
- Core mechanics hints (sorting, matching, tapping)
- Theme/setting implications (zen, fantasy, sci-fi)
- Target audience implications
- Monetization feasibility

### Phase 1: Game Research (Priority 10, Parallel)

**Wave 1 Agents** (13 parallel):

1. **game-market-benchmarker** (opus, 120K)

   **Research Objective**: Establish baseline metrics with STRONG evidence from industry reports

   **Step 1: Retention Benchmarks by Genre**

   **Data sources**: Sensor Tower Q3 2025, GameRefinery Mobile Gaming Benchmark Report 2025

   **Genre benchmarks**:
   ```
   | Genre | D1 Retention | D7 Retention | D30 Retention | Source |
   |-------|--------------|--------------|---------------|--------|
   | Match-3 | 40-50% | 20-25% | 8-12% | Sensor Tower |
   | Idle | 45-55% | 25-35% | 10-20% | GameRefinery |
   | Arcade | 30-40% | 12-20% | 4-10% | Sensor Tower |
   | Puzzle | 35-45% | 18-28% | 8-15% | GameRefinery |
   | Sorting | 35-45% | 15-25% | 6-12% | Sensor Tower |
   ```

   **Validation rules**:
   - If concept targets > benchmark + 20%: Require justification (unique mechanic, IP, etc.)
   - If concept targets < benchmark - 20%: Flag as concern (poor retention design)

   **Step 2: CPI (Cost Per Install) by Region**

   **Regional CPI benchmarks** (US iOS = baseline, adjust for other regions):
   ```
   | Region | Casual/Puzzle | Mid-core | Adjustment |
   |--------|---------------|----------|------------|
   | US iOS | $1.50-4.00 | $2.00-6.00 | 1.0x (baseline) |
   | US Android | $1.00-2.80 | $1.40-4.20 | 0.7x iOS |
   | EU iOS | $1.20-3.20 | $1.60-4.80 | 0.8x US |
   | APAC iOS | $0.80-2.00 | $1.00-3.00 | 0.5x US |
   ```

   **CPI volatility factors**:
   - Q4 (holiday season): +30-50% CPI (increased competition)
   - New iOS release: +20-30% CPI (early adopter premium)
   - Genre saturation: Match-3 CPI inflated 2x vs 2020

   **Step 3: LTV (Lifetime Value) Ranges by Player Segment**

   **Player segmentation** (by spending behavior):
   ```
   | Segment | % of Players | LTV Range | Revenue Contribution |
   |---------|--------------|-----------|----------------------|
   | Minnows (non-payers) | 80-90% | $0.50-2.00 | 5-15% (ads only) |
   | Dolphins (small spenders) | 8-15% | $5-20 | 20-35% |
   | Whales (big spenders) | 1-3% | $50-500 | 50-75% |
   ```

   **Blended LTV calculation**:
   ```
   Blended LTV = (85% × $1.00) + (12% × $10) + (3% × $150)
              = $0.85 + $1.20 + $4.50
              = $6.55 per user
   ```

   **LTV/CAC Target Ratios**:
   - Minimum: 1.5x (break-even)
   - Healthy: 3.0x (sustainable UA)
   - Excellent: 5.0x+ (aggressive growth)

   **Step 4: ARPDAU (Average Revenue Per Daily Active User) by Genre**

   **Genre ARPDAU benchmarks**:
   ```
   | Genre | ARPDAU Range | Primary Monetization | Source |
   |-------|--------------|----------------------|--------|
   | Hyper-casual | $0.05-0.15 | Ads (rewarded video, interstitials) | Sensor Tower |
   | Casual | $0.15-0.40 | Hybrid (IAP + ads) | GameRefinery |
   | Mid-core | $0.30-0.80 | IAP (gacha, VIP pass) | Sensor Tower |
   | Hardcore | $0.80-2.50 | IAP (competitive advantage) | GameRefinery |
   ```

   **ARPDAU components**:
   - Ad ARPDAU = (impressions/DAU) × (eCPM/1000) × fill_rate
   - IAP ARPDAU = (conversion%) × ARPPU

   **Step 5: Market Size Estimation (TAM/SAM/SOM)**

   **Mobile gaming TAM** (Total Addressable Market):
   - Global: $100B annually (Newzoo 2025)
   - US: $25B annually (30% of global)

   **Genre SAM** (Serviceable Addressable Market):
   - Match-3: $5B (5% of TAM)
   - Idle: $3B (3% of TAM)
   - Arcade: $8B (8% of TAM)

   **Realistic SOM** (Serviceable Obtainable Market):
   - Indie studio: 0.001-0.01% of SAM ($50K-500K annually)
   - Mid-tier studio: 0.01-0.1% of SAM ($500K-5M annually)
   - Top-tier studio: 0.1-1.0% of SAM ($5M-50M annually)

   **Output Format**:
   1. Retention benchmarks table with genre comparison
   2. CPI estimates by region with volatility factors
   3. LTV ranges by segment with blended LTV calculation
   4. ARPDAU targets with monetization breakdown
   5. Market size estimation (TAM/SAM/SOM) with realistic revenue projections

   **Evidence tier**: STRONG (cite Sensor Tower Q3 2025, GameRefinery 2025, Newzoo Global Games Market Report)

2. **game-competitive-analyst** (opus, 120K)

   **Research Objective**: Analyze top-grossing games using ERRC Grid framework

   **Step 1: Competitive Feature Matrix** (5-10 features × 3-5 competitors)

   Create table with format:
   ```
   | Feature | Competitor A | Competitor B | Competitor C | Our Concept |
   |---------|--------------|--------------|--------------|-------------|
   | Lives system | ✓ (5 lives) | ✓ (unlimited) | ✓ (pay to refill) | ? |
   | Boosters | 8 types | 5 types | 12 types | ? |
   | Social features | Friend leaderboard | Guild system | None | ? |
   ```

   Data sources: App Annie Top Grossing, Sensor Tower revenue data, feature screenshots

   **Step 2: ERRC Grid Analysis** (Blue Ocean Strategy framework)

   **ELIMINATE** (remove industry pain points):
   - Identify: What pain points do ALL competitors have?
   - Example: "Eliminate wait timers (Match-3 genre fatigue)"
   - Our approach: Competitor pain point → We remove it

   **REDUCE** (cut unnecessary complexity):
   - Identify: What features are over-engineered or bloated?
   - Example: "Reduce booster types from 12 to 5 (decision paralysis)"
   - Our approach: Genre bloat → We simplify

   **RAISE** (amplify key differentiators):
   - Identify: What standard features should be elevated to core?
   - Example: "Raise social features to guild wars level (AFK Arena standard)"
   - Our approach: Standard feature → We make it premium

   **CREATE** (invent new value):
   - Identify: What does NO competitor offer?
   - Example: "Create narrative progression (puzzles unlock story chapters)"
   - Our approach: Genre gap → We pioneer

   **Step 3: Gap Identification** (white space opportunities)
   - Where do all competitors converge (crowded space)?
   - Where do all competitors fail (opportunity)?
   - Example: "All Match-3 games have lives system (frustration) → opportunity for unlimited play + different monetization"

   **Output Format**:
   1. Feature matrix with 5-10 features × 3-5 competitors
   2. ERRC grid with specific examples (not generic statements)
   3. Gap analysis with actionable opportunities
   4. Core loop teardown (Action-Reward-Progression-Engagement)
   5. Monetization teardown (IAP structure, ad placements, estimated LTV)

   **Evidence tier**: STRONG (cite AppAnnie Top Grossing data, feature screenshots, revenue reports)

3. **game-monetization-researcher** (opus, 120K)

   **Research Objective**: Design monetization strategy with validated LTV/CAC models and GAM-004 ethics

   **Step 1: Genre-Specific Monetization Patterns**

   **Hyper-casual (F2P-Ads)**:
   - Primary: Rewarded video (eCPM $8-15 US iOS)
   - Secondary: Interstitial ads (eCPM $5-10)
   - ARPDAU target: $0.10-0.18
   - Example: Subway Surfers, Crossy Road

   **Casual (Hybrid: Ads + IAP)**:
   - Primary: IAP (extra moves, boosters)
   - Secondary: Rewarded video (2x rewards)
   - ARPDAU target: $0.18-0.40
   - Example: Candy Crush, Homescapes

   **Mid-core (F2P-IAP)**:
   - Primary: Gacha (hero summons), VIP pass
   - Secondary: Rewarded video (optional)
   - ARPDAU target: $0.80-2.50
   - Example: AFK Arena, Idle Heroes

   **Step 2: LTV/CAC Model with Payback Period**

   **LTV Calculation** (Lifetime Value per user):
   ```
   LTV = ARPDAU × Average Lifetime Days

   Breakdown by cohort:
   - Minnows (non-payers): LTV = $0.50-2.00 (ad revenue only)
   - Dolphins (small spenders): LTV = $5-20 (1-3 IAP purchases)
   - Whales (big spenders): LTV = $50-500 (recurring IAP, VIP)

   Blended LTV = (% Minnows × LTV_M) + (% Dolphins × LTV_D) + (% Whales × LTV_W)
   ```

   **CAC Benchmarks** (Cost to Acquire Customer):
   - US iOS: $1.50-4.00 (puzzle, casual)
   - US iOS: $2.00-6.00 (mid-core)
   - Android: 60-70% of iOS CAC

   **Target LTV/CAC Ratios**:
   - Minimum viable: 1.5x (break-even with margins)
   - Healthy: 3.0x (sustainable UA scaling)
   - Excellent: 5.0x+ (aggressive growth mode)

   **Payback Period** (time to recover CAC):
   - D7 LTV target: 50-100% of CAC (7-day payback)
   - D30 LTV target: 150-300% of CAC (1-month ROI positive)

   **Step 3: Conversion Funnel Analysis**

   **IAP Conversion Funnel** (F2P → Payer):
   - Install → D1 active: 100% → 40% (D1 retention)
   - D1 active → D7 active: 40% → 18% (D7 retention)
   - D7 active → First IAP: 18% → 3.6% (20% conversion)
   - First IAP → Repeat buyer: 3.6% → 1.8% (50% repeat rate)

   **Conversion triggers** (why players pay):
   - Stuck: Out of lives/energy (40% of first IAP)
   - Convenience: Skip wait timers (25%)
   - FOMO: Limited-time offer (20%)
   - Status: Exclusive skins, VIP badge (15%)

   **Step 4: GAM-004 Ethical Monetization Compliance**

   **Prohibited Patterns** (predatory mechanics):
   - ❌ Loot boxes with <1% odds (predatory gacha)
   - ❌ Dark patterns: Hidden costs, forced clicks
   - ❌ Pay-to-win: Impossible levels without IAP
   - ❌ Whale exploitation: Uncapped spending (>$1000/month)

   **Required Safeguards**:
   - ✅ Transparent odds disclosure (EU loot box laws)
   - ✅ Spending limits ($100/week prompt, parental controls)
   - ✅ F2P viable path (can finish game without IAP)
   - ✅ No FOMO manipulation of minors (<13 age gate)

   **Step 5: ARPDAU Estimation**

   **ARPDAU Formula**:
   ```
   ARPDAU = (Ad Revenue per DAU) + (IAP Revenue per DAU)

   Ad Revenue = (Ad impressions per DAU) × (eCPM / 1000) × Fill Rate
   Example: 5 impressions × ($10 / 1000) × 0.85 = $0.0425

   IAP Revenue = (IAP conversion %) × (ARPPU)
   Example: 5% × $10 = $0.50

   Total ARPDAU = $0.0425 + $0.50 = $0.54
   ```

   **Output Format**:
   1. Genre-specific monetization pattern recommendation
   2. LTV/CAC model with D7/D30 targets
   3. Conversion funnel analysis with trigger identification
   4. GAM-004 compliance check (prohibited patterns flagged)
   5. ARPDAU forecast with sensitivity analysis (±20%)

   **Evidence tier**: STRONG (cite Sensor Tower ARPDAU reports, GameRefinery IAP structures, published LTV/CAC case studies)

4. **game-viral-mechanics-researcher** (opus, 120K)
   - K-factor analysis with validated formula: K = i × c × t
   - K-factor benchmarks by genre (hyper-casual: 0.1-0.3, social: 0.4-0.8, multiplayer: 0.6-1.2)
   - Organic UA patterns (social sharing, invites)
   - Community building features
   - Cite published K-factor data from Sensor Tower, GameRefinery
   - Evidence tier: STRONG

5. **game-retention-researcher** (opus, 120K)

   **Research Objective**: Design retention mechanics with STRONG evidence and psychological triggers

   **Step 1: D1/D7/D30 Benchmark Validation**

   Cite Sensor Tower / GameRefinery genre benchmarks:
   - Match-3: D1 = 45% (Sensor Tower Q3 2025), D7 = 22%, D30 = 10%
   - Idle: D1 = 50%, D7 = 28%, D30 = 12%
   - Arcade: D1 = 35%, D7 = 15%, D30 = 6%
   - Puzzle: D1 = 40%, D7 = 22%, D30 = 10%
   - Sorting: D1 = 38%, D7 = 18%, D30 = 7%

   **If target exceeds benchmark**: Justify with unique mechanic, premium audience, or IP advantage
   - Example: "Our target D1 = 50% vs genre 45% because [unique onboarding feature X]"

   **Step 2: Daily Engagement Loop with Psychological Triggers**

   Map daily loop to psychological triggers (FOMO, Streaks, Variable Rewards, Social Proof):

   **Login phase**:
   - Psychological trigger: **Streaks** (loss aversion)
   - Design: "Don't break your 7-day streak! Day 7 = 100 gems"
   - Evidence: Duolingo streak feature increased D7 retention by 15% (Sensor Tower case study)

   **Daily quest phase**:
   - Psychological trigger: **Variable rewards** (slot machine effect)
   - Design: Quest reward = 10-100 gems (random), not fixed 50 gems
   - Evidence: Variable rewards increase dopamine 3x vs fixed rewards (behavioral economics research)

   **Event phase**:
   - Psychological trigger: **FOMO** (scarcity + urgency)
   - Design: "Limited-time hero! Only 48 hours to unlock!"
   - Evidence: Fortnite limited skins drive 20% of IAP revenue (Epic Games investor report)

   **Social phase**:
   - Psychological trigger: **Social proof**
   - Design: "Your friend scored 8000! Can you beat it?"
   - Evidence: Friend leaderboards increase session length by 18% (GameRefinery social features report)

   **Step 3: Long-Term Hooks (30-60-90 Day Roadmap)**

   **30-day milestone**:
   - Hook: First major character unlock or prestige reset
   - Reference: AFK Arena unlocks Celestial heroes at Day 30 (30% still active)

   **60-day milestone**:
   - Hook: Guild wars unlock (social retention)
   - Reference: Idle Heroes guild wars at D60 (25% still active)

   **90-day milestone**:
   - Hook: Endgame content (raids, PvP ranked season)
   - Reference: Clash of Clans Clan Wars at D90 (18% still active)

   **Step 4: Churn Intervention with A/B Test Plan**

   **Identify churn triggers**:
   - Stuck on level 50 (15% churn)
   - Out of soft currency (20% churn)
   - 3 days no login (40% churn)

   **Design interventions**:
   - Trigger: Stuck on level 50 → Gift free booster via notification
   - Trigger: Out of currency → Show rewarded ad for 500 coins
   - Trigger: 3 days absent → Push notification "We miss you! Here's 50 gems"

   **A/B test hypothesis**:
   - "Free booster at level 50 reduces D7 churn by 15%"
   - Test: 50% get booster (treatment), 50% don't (control)
   - Success metric: D7 retention delta ≥ 5%

   **Output Format**:
   1. D1/D7/D30 targets validated vs genre benchmarks
   2. Daily engagement loop mapped to 4 psychological triggers
   3. 30-60-90 day roadmap with milestone hooks
   4. Churn intervention plan with A/B test hypotheses
   5. Retention curve forecast (expected % active over 180 days)

   **Evidence tier**: STRONG (cite Sensor Tower retention data, behavioral economics research, Quantic Foundry motivations)

6. **game-genre-researcher** (haiku, 8K)
   - Genre best practices and patterns
   - **OPTIMIZATION v0.5.0**: Downgraded to Haiku for simple pattern matching (saves 24K thinking)
   - Core loop structures (4-phase: Action-Reward-Progression-Engagement)
   - Session length optimization
   - Evidence tier: MEDIUM

7. **game-platform-constraints-researcher** (haiku, 8K)
   - iOS/Android App Store policies
   - **OPTIMIZATION v0.5.0**: Downgraded to Haiku for policy research (saves 24K thinking)
   - Platform-specific requirements (IDFA, privacy)
   - Technical constraints (file size, performance)
   - Evidence tier: MEDIUM

8. **game-player-psychology-researcher** (opus, 120K)

   **Research Objective**: Analyze player psychology using THREE frameworks

   **Framework 1: Bartle Taxonomy** (Achievers, Explorers, Socializers, Killers)

   **Genre-specific distribution** (estimate with evidence):
   - Match-3: Achievers 70%, Explorers 20%, Socializers 8%, Killers 2%
   - Idle: Achievers 50%, Explorers 15%, Socializers 25%, Killers 10%
   - Arcade: Achievers 60%, Explorers 10%, Socializers 10%, Killers 20%
   - Puzzle: Achievers 70%, Explorers 25%, Socializers 3%, Killers 2%
   - Sorting: Achievers 65%, Explorers 30%, Socializers 3%, Killers 2%

   **Core loop mapping**:
   ```
   | Bartle Type | Core Loop Phase | Design Element |
   |-------------|-----------------|----------------|
   | Achievers | Progression | Unlock all 200 levels, 3-star every level |
   | Explorers | Engagement | Discover hidden combos, secret levels |
   | Socializers | Engagement | Guild chat, friend leaderboards |
   | Killers | Reward | PvP arena, top 10 rankings |
   ```

   **Framework 2: Self-Determination Theory (SDT)** (Autonomy, Competence, Relatedness)

   **Core loop SDT satisfaction**:
   - **Autonomy**: Player choice in [X] (e.g., team composition, loadout, upgrade path)
   - **Competence**: Mastery curve from [Y] to [Z] (e.g., 2-min levels → 20-min levels, score 100 → score 10,000)
   - **Relatedness**: Social features [W] (e.g., guild wars, friend gifting, leaderboards)

   **SDT violations to avoid**:
   - ❌ Forced social (low autonomy): "Must join guild to progress"
   - ❌ Impossible difficulty (low competence): "Level 100 requires IAP to pass"
   - ❌ No social (low relatedness): "Single-player only" (⚠️ OK for premium puzzles)

   **Framework 3: Flow Theory** (Csikszentmihalyi)

   **Flow channel analysis**:
   - **Easy start**: First 10 levels (skill requirement: low, challenge: low)
   - **Flow zone**: Levels 11-100 (skill grows with challenge in lockstep)
   - **Anxiety zone**: Levels 100+ (challenge >> skill, must be optional or gated)

   **Flow state triggers**:
   - Clear goals: "Match 3 to clear tiles"
   - Immediate feedback: Visual effects, score increase, sound cues
   - Challenge-skill balance: Difficulty curve matches player skill growth trajectory

   **Output Format**:
   1. Bartle distribution for target genre (% breakdown with justification)
   2. SDT satisfaction matrix (Autonomy/Competence/Relatedness scoring 0-10)
   3. SDT violation check (identify potential design anti-patterns)
   4. Flow channel diagram (easy/flow/anxiety zones with level ranges)
   5. Psychological trigger recommendations (loss aversion, variable rewards, social proof, FOMO)

   **Evidence tier**: STRONG (cite Quantic Foundry player motivation data, academic SDT research, Bartle's MUD studies)

9. **game-economy-simulator** (opus, 120K)
   - Simulate 1000-player economy over 30 days
   - Model soft currency (coins) and hard currency (gems) flows
   - Calculate sink/source ratio (target: 0.9-1.1), inflation rate (target: <5%/month)
   - Identify IAP conversion trigger points (when F2P runs out of resources)
   - Validate against genre benchmarks (Match-3: sinks at level 50-100, Idle: prestige resets)
   - Output: Economy parameters table (GAM-005 compliance)
   - Evidence tier: STRONG

10. **game-player-archetype-researcher** (opus, 120K)
    - Analyze THREE frameworks: Bartle Types, Quantic Foundry (12 motivations), SDT
    - Estimate Bartle distribution by genre with evidence
    - Map core loop to Quantic Foundry motivations (Action, Social, Mastery, Achievement, Immersion, Creativity)
    - Validate SDT satisfaction (Autonomy, Competence, Relatedness) and identify potential violations
    - Output: Player archetype matrix with design implications
    - Evidence tier: STRONG

11. **game-platform-roadmap-researcher** (haiku, 8K)
    - Platform prioritization: Primary (iOS/Android), Secondary (Steam/Epic), Future (Console)
    - **OPTIMIZATION v0.5.0**: Downgraded to Haiku for roadmap planning (saves 24K thinking)
    - Platform-specific constraints: iOS App Store guidelines, Google Play policies, Steam requirements
    - Cross-platform features: Cloud save sync, cross-platform IAP, platform-specific monetization
    - Launch sequence recommendations with rationale
    - Output: Platform roadmap with launch timeline
    - Evidence tier: MEDIUM

12. **game-liveops-feasibility-researcher** (haiku, 8K)
    - Content cadence by genre: Hyper-casual (none), Casual (monthly events), Mid-core (weekly events)
    - **OPTIMIZATION v0.5.0**: Downgraded to Haiku for resource estimation (saves 24K thinking)
    - Team resourcing: Estimate team size (1-5 people), required skills (designer, economy, QA, community)
    - Tools: Remote config (Firebase), A/B testing (Optimizely)
    - 90-day event calendar: Month 1 (onboarding optimization), Month 2 (first seasonal event), Month 3 (new content)
    - Output: Live ops roadmap with resource requirements
    - Evidence tier: WEAK

13. **game-cultural-localization-researcher** (haiku, 8K)
    - Target markets beyond US/EU: China (Tencent, censorship), Japan (gacha laws), Korea (GRAC), Middle East (Ramadan)
    - **OPTIMIZATION v0.5.0**: Downgraded to Haiku for localization patterns (saves 24K thinking)
    - Art/theme localization: Color symbolism, character design preferences, monetization norms
    - Launch sequence: Tier 1 (US/UK/CA/AU), Tier 2 (Western EU), Tier 3 (APAC with partnerships)
    - Market-specific adaptations and compliance requirements
    - Output: Localization roadmap with market priorities
    - Evidence tier: MEDIUM

**Wave 2 Agents** (2 synthesis, Priority 20):

14. **game-economy-synthesizer** (haiku, 8K)
    - Integrate findings from monetization-researcher and economy-simulator
    - **OPTIMIZATION v0.5.0**: Downgraded to Haiku for synthesis (saves 24K thinking)
    - Generate economy parameters for simulation
    - Use templates/shared/concept-sections/game-economy-design.md schema
    - Currency types, income/expense balance, progression gates

15. **game-liveops-synthesizer** (haiku, 8K)
    - Integrate findings from liveops-feasibility-researcher
    - **OPTIMIZATION v0.5.0**: Downgraded to Haiku for synthesis (saves 24K thinking)
    - 90-day event calendar (seasonal events, limited-time offers)
    - A/B test recommendations
    - Content update cadence

### Phase 2: Genre Variant Generation (Priority 20, Parallel)

**OPTIMIZATION v0.5.0 - Lazy Loading**: By default, generate only the selected variant (if `--genre` specified).
Generate all 5 variants only if `--genre=all` (explicit opt-in).

**Conditional Logic**:
```yaml
if cli_flag('--genre') == 'all':
  generator_count: 5  # Generate all variants
  template_count: 5 variants (Sorting, Match-3, Idle, Arcade, Puzzle)
elif cli_flag('--genre') in ['sorting', 'match3', 'idle', 'arcade', 'puzzle']:
  generator_count: 1  # Generate single variant only
  template_count: 1 variant (user-selected)
else:
  # Default: no --genre specified
  generator_count: 1  # Generate single highest-scoring variant in Phase 3
  template_count: 1 variant (auto-selected)
```

**Token Savings**:
- Full generation (all 5): 5 × opus × 80K = $1.60
- Default (single variant): 1 × opus × 80K = $0.32 (-80% tokens)
- Estimated monthly savings (20 executions): 64 full generations tokens

**Usage Examples**:
```bash
# Quick single variant (faster, cheaper)
/speckit.games.concept --depth=standard

# Specific genre (user selects one)
/speckit.games.concept --depth=standard --genre=match3

# All 5 variants for comparison (original behavior)
/speckit.games.concept --depth=standard --genre=all
```

**Generator Selection** (conditional):
If `--genre=all`, include all 5 generators. Otherwise, load only selected generator:

1. **sorting-concept-generator** (opus, 80K)
   - Genre lens: Sorting (satisfying order from chaos)
   - Core pattern: Organize items by attribute (color, shape, size)
   - Session: 2-5 min hyper-casual, 10-15 min casual
   - Examples: Sort It 3D, Goods Sort, Water Sort Puzzle
   - Generate: Vision, Core Loop, Monetization, Retention, Psychology, Tech, CQS-Game

2. **match3-concept-generator** (opus, 80K)
   - Genre lens: Match-3 (satisfying cascades and combos)
   - Core pattern: Match 3+ items to clear board
   - Session: 10-15 min casual, 15-20 min mid-core
   - Examples: Candy Crush, Homescapes, Gardenscapes
   - Generate: Vision, Core Loop, Monetization, Retention, Psychology, Tech, CQS-Game

3. **idle-concept-generator** (opus, 80K)
   - Genre lens: Idle (passive progression, offline rewards)
   - Core pattern: Automated resource generation with strategic upgrades
   - Session: 5-10 min check-ins, 30-60 min deep sessions
   - Examples: AFK Arena, Idle Heroes, AdVenture Capitalist
   - Generate: Vision, Core Loop, Monetization, Retention, Psychology, Tech, CQS-Game

4. **arcade-concept-generator** (opus, 80K)
   - Genre lens: Arcade (reflex-based, skill mastery)
   - Core pattern: Fast-paced action with increasing difficulty
   - Session: 2-5 min runs, 10-15 min total
   - Examples: Subway Surfers, Temple Run, Crossy Road
   - Generate: Vision, Core Loop, Monetization, Retention, Psychology, Tech, CQS-Game

5. **puzzle-concept-generator** (opus, 80K)
   - Genre lens: Puzzle (logic, spatial reasoning)
   - Core pattern: Solve increasingly complex puzzles
   - Session: 5-10 min per puzzle, 20-30 min total
   - Examples: Monument Valley, The Room, Cut the Rope
   - Generate: Vision, Core Loop, Monetization, Retention, Psychology, Tech, CQS-Game

**Each generator produces:**

```markdown
# [Genre] Variant: [Game Name]

## Vision Statement
[1-2 paragraphs: Problem→Solution→Impact]

## Core Loop (4 Phases)
1. **Action**: [What player does]
2. **Reward**: [Immediate feedback]
3. **Progression**: [Long-term goals]
4. **Engagement**: [Retention hooks]

## Monetization Strategy
- Primary: [IAA/IAP model]
- Secondary: [Alternative revenue]
- ARPDAU Target: [$X.XX-X.XX]
- Ethics: [GAM-004 compliance notes]

## Retention Mechanics
- D1 Hook: [Instant gratification]
- D7 Hook: [Daily engagement]
- D30 Hook: [Long-term progression]

## Player Psychology
- Bartle Types: [Distribution %]
- SDT Needs: [Autonomy/Competence/Relatedness]
- Flow State: [Difficulty curve]

## Technical Requirements
- Engine: [Unity/Unreal/Custom]
- Backend: [Minimal/Moderate/Complex]
- Platform: [iOS/Android/Cross-platform]

## CQS-Game Self-Assessment
[Calculate using templates/shared/concept-sections/cqs-game.md]
- Market: [0-16]
- Mechanics: [0-14]
- Monetization: [0-14]
- Viral Potential: [0-12]
- Retention: [0-12]
- Tech Feasibility: [0-10]
- Competition: [0-8]
- Innovation: [0-8]
- Risk: [0-6]
- Evidence Multiplier: [0.8-1.2]
**Total: [0-120]**
```

### Phase 3: Quality Validation (Priority 30)

**concept-quality-validator** (opus, 40K):

For EACH of 5 genre variants:

1. **Calculate CQS-Game v2.0** (0-120 scale)
   - Apply 10-component formula from templates/shared/concept-sections/cqs-game.md
   - Components: Market (15%), Mechanics (13%), Monetization (13%), Viral (11%), Retention (11%), Strategic Depth (10%), Tech (9%), Competition (8%), Innovation (8%), Risk (2%)
   - Apply Evidence Multiplier (0.8-1.2 based on source quality)
   - Document scoring rationale

2. **Validate Quality Gates**
   - QG-GCONCEPT-001: CQS-Game ≥ 90/120 (world-class threshold, v2.0)
   - QG-GCONCEPT-002: Genre fit ≥ 80% (compare to templates/shared/game-genres/)
   - QG-GCONCEPT-003: No predatory patterns (GAM-004 check)

3. **Multi-Pass Regeneration Logic** (max 3 passes)
   - **Pass 1**: Initial scoring
   - **Pass 2**: IF CQS-Game < 90 → Regenerate weakest component (lowest score)
   - **Pass 3**: Final regeneration attempt if still < 90
   - **After 3 passes**: If still < 90 → Flag for user review (don't auto-fail)
   - Document: Component breakdown, evidence gaps, regeneration history

### Phase 3.5: Comparative Validation (Priority 35) [NEW]

**comparative-validator** (opus, 60K):

Cross-validate all 5 genre variants for consistency and detect self-assessment bias:

1. **CQS-Game Score Distribution Analysis**
   - Flag if all variants score 85-95 (too clustered, likely inflated)
   - Expected spread: 75-110 (some genres fit better than others)
   - Example flagging: "All 5 variants scored 88-92 → suspicious uniformity, possible self-assessment bias"

2. **Component Score Cross-Check**
   - Compare same component across variants
   - Flag contradictions:
     - Sorting: "Market = 90/100 (huge genre)"
     - Match-3: "Market = 92/100 (huge genre)"
     - **Contradiction**: Both can't be "huge" if competing for same audience
   - Validate relative positioning makes sense

3. **Retention Claims Validation**
   - Cross-reference D1/D7/D30 targets with genre benchmarks from game-market-benchmarker
   - Flag if variant claims exceed genre benchmarks without justification:
     - Sorting template: D1 = 35-45%, D7 = 15-25%
     - Variant claims: D1 = 60%, D7 = 40%
     - **Flag**: "Claims 50% above genre norm, needs validation or unique mechanic justification"

4. **Unique Mechanic Differentiation**
   - Ensure each variant has truly distinct mechanic (not just theme reskin)
   - Flag if mechanics overlap:
     - Sorting: "Organize items by color"
     - Puzzle: "Organize items by color"
     - **Flag**: Same mechanic, different genre label → insufficient differentiation

5. **Self-Assessment Bias Detection**
   - Downgrade scores if lacking external validation:
     - Mechanics component = 95/100 but no competitor analysis → Downgrade to 80/100
     - Innovation component = 90/100 but no market gap evidence → Downgrade to 70/100
   - Require STRONG evidence tier for scores > 85/100

6. **Regeneration Triggers**
   - IF any variant's adjusted CQS-Game < 85 after bias correction → Trigger regeneration
   - IF contradictions found → Regenerate conflicting components
   - Max 2 regeneration cycles at this phase

**Output**:
- Validation report per variant (PASS / FLAGGED / REGENERATE)
- Score adjustments (if bias detected)
- Consistency report (cross-variant comparison table)

### Phase 4: Auto-Selection & File Generation (Priority 40)

**file-generator** (sonnet, 16K):

Dependencies: Phase 3 (Quality Validation) AND Phase 3.5 (Comparative Validation)

1. **Select Best Variant**
   - Rank all 5 variants by CQS-Game score
   - Select highest score as primary concept
   - Generate comparison table for alternatives

2. **Generate 8 Output Files**

**File 1: `specs/game-concept.md`** (selected variant)
```markdown
# [Game Name] — Concept

> 🏆 **Auto-Selected**: Highest CQS-Game score ([X]/120)
> 📊 **Genre**: [Sorting/Match-3/Idle/Arcade/Puzzle]
> 🎯 **Target**: [Audience]
> 💰 **Monetization**: [Model]

[Full concept content from winning variant]

---

**See alternatives**: specs/game-alternatives.md
**Quality report**: specs/quality-report.md
**Research findings**: specs/concept-research.md
```

**File 2-6: `specs/alternatives/01-sorting.md` through `05-puzzle.md`**
- Full concept for each genre variant
- Individual CQS-Game scores
- Genre-specific recommendations

**File 7: `specs/game-alternatives.md`** (comparison table)
```markdown
# Game Concept Alternatives — Comparison

| Dimension | Sorting | Match-3 | Idle | Arcade | Puzzle |
|-----------|---------|---------|------|--------|--------|
| **CQS-Game** | [X]/120 | [X]/120 | [X]/120 | [X]/120 | [X]/120 |
| **D1 Target** | X% | X% | X% | X% | X% |
| **ARPDAU** | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX |
| **Session Length** | X min | X min | X min | X min | X min |
| **Dev Timeline** | X weeks | X weeks | X weeks | X weeks | X weeks |
| **Complexity** | [Low/Med/High] | ... | ... | ... | ... |
| **Innovation** | [X]/8 | [X]/8 | [X]/8 | [X]/8 | [X]/8 |

## Recommendation

**Primary**: [Genre] ([CQS-Game]/120)
**Rationale**: [1-2 sentences explaining why this genre scored highest]

**Runner-up**: [Genre] ([CQS-Game]/120)
**Consider if**: [Conditions under which runner-up might be better]
```

**File 8: `specs/quality-report.md`** (CQS-Game breakdown)
```markdown
# Quality Report — CQS-Game Breakdown

## Scoring Summary

| Variant | CQS-Game | Status | Notes |
|---------|----------|--------|-------|
| Sorting | [X]/120 | [✅/⚠️/⛔] | [...] |
| Match-3 | [X]/120 | [✅/⚠️/⛔] | [...] |
| Idle | [X]/120 | [✅/⚠️/⛔] | [...] |
| Arcade | [X]/120 | [✅/⚠️/⛔] | [...] |
| Puzzle | [X]/120 | [✅/⚠️/⛔] | [...] |

## Component Breakdown (per variant)

### [Genre] Variant

#### Market (16 pts possible)
- Genre market size: [X]/30 pts
- Growth trend: [X]/25 pts
- Demographic sizing: [X]/25 pts
- Geographic fit: [X]/20 pts
**Subtotal**: [X]/100 × 0.16 = [X]/16

[Repeat for all 9 components]

#### Evidence Multiplier
- Source quality: [0.8-1.2]
- Rationale: [...]

**Final Score**: [X]/120

## Quality Gate Results

- QG-GCONCEPT-001: [✅ PASS | ⛔ FAIL]
- QG-GCONCEPT-002: [✅ PASS | ⛔ FAIL]
- QG-GCONCEPT-003: [✅ PASS | ⛔ FAIL]

## Recommendations

[Next steps based on scores]
```

**File 9: `specs/concept-research.md`** (market research)
```markdown
# Concept Research — Market Findings

## Executive Summary

[1-2 paragraphs of key findings from all research agents]

## Market Benchmarks

[Output from game-market-benchmarker]

## Competitive Analysis

[Output from game-competitive-analyst]

## Monetization Insights

[Output from game-monetization-researcher]

[... etc for all research agents]
```

## Integration with Existing Components

This command reads and validates against:

1. **`templates/shared/concept-sections/game-economy-design.md`**
   - Economy parameters schema used by game-economy-synthesizer
   - Currency types, balance metrics, progression gates

2. **`templates/shared/concept-sections/retention-strategy.md`**
   - D1/D7/D30 benchmarks validated by game-retention-researcher
   - Habit loops and engagement hooks

3. **`templates/shared/concept-sections/monetization-strategy.md`**
   - LTV targets and ethical monetization (GAM-004)
   - Conversion funnels and ARPDAU calculations

4. **`templates/shared/concept-sections/player-psychology.md`**
   - Bartle Types distribution validation
   - Self-Determination Theory framework
   - Flow Theory for difficulty curves

5. **`templates/shared/game-genres/`** (5 templates)
   - Genre-specific best practices
   - Core loop patterns (4-phase structure)
   - Session length and retention profiles

## Cost Estimation

**OPTIMIZATION v0.5.0** — 7 research agents downgraded from Sonnet (32K) to Haiku (8K) = **168K thinking tokens saved per world-class run**

**Default Mode** (single variant, standard depth):
- Phase 0: 1 agent × haiku × 8K = $0.00
- Phase 1: 5 agents × (3 opus × 120K + 2 haiku × 8K) = $1.44
- Phase 2: 1 agent × opus × 80K = $0.32 ← **80% reduction from lazy loading**
- Phase 3: 1 agent × opus × 40K = $0.20
- Phase 4: 1 agent × haiku × 16K = $0.04

**Total**: ~$1.98 per concept (single variant) ← **58% reduction vs v1.0**

**Cost by depth** (single variant, lazy loading):
- Quick (3 agents): ~$0.60
- Standard (5 agents): ~$1.98 ← **Default**
- World-class (12 agents): ~$3.20

**World-class mode breakdown** (all 5 genres):
- Phase 1 Wave 1: 13 agents (8 opus × 120K + 5 haiku × 8K) = ~$3.20 ← **-$1.60 from Haiku downgrade**
- Phase 1 Wave 2: 2 agents (2 haiku × 8K) = ~$0.00 ← **-$0.04 from Haiku downgrade**
- Phase 2: 5 agents (5 opus × 80K) = ~$1.60 ← **-$0.32 savings if single variant**
- Phase 3: 1 agent (1 opus × 40K) = ~$0.16
- Phase 3.5: 1 agent (1 opus × 60K) = ~$0.24
- Phase 4: 1 agent (1 haiku × 16K) = ~$0.04 ← **-$0.08 from Haiku downgrade**
- **Total**: ~$5.24 per concept (all 5 genres) ← **-25% reduction from v1.0 ($6.96)**
- **Single variant**: ~$3.20 ← **-54% reduction for user tier optimization**

**Savings Summary**:
- Downgrading 7 agents Sonnet → Haiku: **168K thinking tokens saved**
- Default single-variant lazy loading: **$1.28 per concept saved**
- World-class 5-genre comparison: **$1.72 per concept saved**
- Monthly savings (20 executions): **$25-34/month** or **5.6M-6.8M thinking tokens**

## Success Metrics

After generating concept, track:
- CQS-Game score ≥ 85/120 (QG-GCONCEPT-001)
- Genre fit ≥ 80% (QG-GCONCEPT-002)
- Zero GAM-004 violations (QG-GCONCEPT-003)
- User selects generated concept for GDD phase
- Concept leads to successful game launch (6-month follow-up)

## Troubleshooting

**Issue**: CQS-Game scores too low (< 85)
**Solution**:
- Increase depth flag to world-class
- Provide more specific game_idea input
- Check that target_audience and monetization_preference are realistic

**Issue**: Research agents timeout
**Solution**:
- Reduce depth flag to quick
- Use --genre flag to generate single variant
- Check network connectivity for web research

**Issue**: Genre variants too similar
**Solution**:
- Ensure game_idea is genre-agnostic
- Review genre templates for differentiation
- Adjust complexity_budget to allow genre-specific mechanics

## Related Commands

- **`/speckit.concept`** — B2B product concepts (business strategy variants)
- **`/speckit.gdd`** — Full Game Design Document from concept
- **`/speckit.games.mechanics`** — Detailed mechanics design (follow-up)
- **`/speckit.concept.switch [1-5]`** — Switch between genre variants
- **`/speckit.balance`** — Balance testing for selected concept

## Version History

- **v0.1.0** (2026-01-13): Initial release with 5 mobile game genres
  - 10 game-specific research agents
  - CQS-Game formula (9 components)
  - Auto-selection logic

---

**Next**: After concept approval → `/speckit.gdd` or `/speckit.games.mechanics`

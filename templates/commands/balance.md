---
name: balance
description: |
  Game balance testing and Monte Carlo simulation for mobile games.
  Validates difficulty curves, economy balance, meta concentration, and power variance
  to ensure fair, engaging gameplay for all player segments.

version: 1.0.0
persona: game-economist-agent
model: opus
thinking_budget: 32000

skills:
  - economy-simulation
  - difficulty-analysis
  - meta-analysis
  - power-variance

inputs:
  balance_type:
    type: enum
    options: [economy, difficulty, pvp_meta, full]
    default: full
    description: Type of balance analysis to perform
  simulation_runs:
    type: integer
    default: 10000
    description: Number of Monte Carlo simulations per archetype
  simulation_days:
    type: integer
    default: 90
    description: Simulation duration in days
  custom_thresholds:
    type: object
    description: Override default quality gate thresholds

outputs:
  - reports/balance/balance-report.md              # Comprehensive report
  - reports/balance/economy-simulation.md          # Economy analysis
  - reports/balance/difficulty-analysis.md         # Difficulty curve analysis
  - reports/balance/meta-report.md                 # PvP meta concentration
  - reports/balance/metrics.json                   # Raw metrics data
  - reports/balance/recommendations.md             # Prioritized fixes

quality_gates:
  - name: QG-BALANCE-001
    description: Gini Coefficient
    condition: "Wealth inequality between player archetypes"
    threshold: "Gini < 0.6"
    severity: HIGH
  - name: QG-BALANCE-002
    description: Difficulty Curve Smoothness
    condition: "No difficulty spikes > 2x in adjacent levels"
    threshold: "Max spike < 2.0x"
    severity: HIGH
  - name: QG-BALANCE-003
    description: Meta Concentration
    condition: "Top strategy usage in PvP"
    threshold: "Top meta < 30% usage"
    severity: MEDIUM
  - name: QG-BALANCE-004
    description: Power Variance
    condition: "Character/unit power variance"
    threshold: "CV < 0.25 (25%)"
    severity: HIGH
  - name: QG-BALANCE-005
    description: F2P Milestone Reachability
    condition: "All milestones achievable by F2P within time budgets"
    threshold: "100% reachable"
    severity: CRITICAL
  - name: QG-BALANCE-006
    description: Pay-to-Win Detection
    condition: "PvP power gap between F2P and whale"
    threshold: "Power gap < 2.0x at same time"
    severity: CRITICAL

pre_gates:
  - name: QG-BALANCE-000
    description: Economy design exists
    condition: "GDD section 04-economy.md or game-economy-design.md exists"
    severity: CRITICAL

inline_gates:
  enabled: true
  gates:
    - id: IG-BALANCE-001
      name: Simulation Convergence
      check: "< 5% of simulations are outliers (>5σ)"
      severity: MEDIUM
    - id: IG-BALANCE-002
      name: Data Completeness
      check: "All required economy parameters present"
      severity: CRITICAL

handoffs:
  - label: Update Economy Design
    agent: speckit.gdd
    auto: false
    condition:
      - "QG-BALANCE-001 or QG-BALANCE-005 failed"
    prompt: "Update economy section with balance recommendations"
  - label: Rebalance Characters
    agent: speckit.tasks
    auto: true
    condition:
      - "QG-BALANCE-004 failed"
      - "Character balance issues detected"
  - label: Soft Launch Check
    agent: speckit.softlaunch
    auto: false
    condition:
      - "All balance gates passed"
    prompt: "Economy validated, ready for soft launch metrics"

claude_code:
  model: opus
  reasoning_mode: extended
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 10000
        max_parallel: 2
      pro:
        thinking_budget: 20000
        max_parallel: 4
      max:
        thinking_budget: 32000
        max_parallel: 8
  cache_hierarchy: full
  orchestration:
    max_parallel: 6
    conflict_resolution: queue
    timeout_per_agent: 1200000  # 20 min for heavy simulations
    retry_on_failure: 2

  subagents:
    # Wave 1: Data Collection (parallel)
    - role: economy-parser
      role_group: DATA
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Parse and validate economy design parameters.

        SEARCH for economy data in:
        1. docs/gdd/sections/04-economy.md (primary)
        2. templates/shared/concept-sections/game-economy-design.md
        3. specs/features/*/spec.md (economy sections)

        EXTRACT:
        - Currency definitions (hard, soft, premium)
        - Earn rates (F2P, dolphin, whale)
        - Sink rates (upgrades, gacha, consumables)
        - Progression milestones with time budgets
        - Gacha rates and pity systems
        - PvP power scaling formulas

        VALIDATE:
        - All required fields present (IG-BALANCE-002)
        - Earn rates are positive
        - Time budgets are reasonable (< 365 days for any milestone)
        - Gacha rates sum to 100%

        OUTPUT: Structured economy config for simulation

    - role: difficulty-parser
      role_group: DATA
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Parse difficulty curve parameters.

        SEARCH for difficulty data in:
        1. docs/gdd/sections/02-core-loop.md
        2. docs/gdd/sections/03-metagame.md
        3. Level/stage configuration files

        EXTRACT:
        - Level progression (power requirements per level)
        - Enemy scaling formulas
        - Expected player power curve
        - Difficulty checkpoints
        - Time-to-complete estimates

        CALCULATE:
        - Difficulty delta between adjacent levels
        - Expected player power at each checkpoint
        - Gap between required and expected power

        OUTPUT: Difficulty curve data for analysis

    - role: meta-parser
      role_group: DATA
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Parse PvP meta and character/unit data.

        SEARCH for meta data in:
        1. docs/gdd/sections/09-social.md (PvP section)
        2. Character/unit configuration files
        3. Balance spreadsheets (if available)

        EXTRACT:
        - Character/unit roster (names, roles, rarities)
        - Stats per character (HP, ATK, DEF, SPD, etc.)
        - Skill multipliers and effects
        - PvP matchmaking parameters
        - Historical usage data (if available)

        CALCULATE:
        - Power rating per character
        - Tier list estimation (S/A/B/C/D)
        - Synergy scores (team compositions)

        OUTPUT: Meta data for concentration analysis

    # Wave 2: Simulation (parallel, heavy compute)
    - role: economy-simulator
      role_group: SIMULATION
      parallel: true
      depends_on: [economy-parser]
      priority: 20
      model_override: opus
      prompt: |
        Run Monte Carlo economy simulations.

        Using economy config from economy-parser:

        1. **Define Player Archetypes**:
           - F2P: $0/month, 1-2 hrs/day
           - Dolphin: $25/month, 2-4 hrs/day
           - Whale: $500/month, 4-8 hrs/day

        2. **Run Simulations** ({{simulation_runs}} per archetype):
           FOR each archetype:
             FOR run in range(simulation_runs):
               - Initialize player state
               - FOR day in range(simulation_days):
                   - Earn currency (with variance)
                   - Spend currency (gacha, upgrades)
                   - Update power level
                   - Check milestone completion
               - Record final state

        3. **Calculate Metrics**:
           - Gini coefficient (wealth inequality)
           - Inflation rate (cost growth)
           - Milestone completion rates per archetype
           - Power gap (whale vs F2P at day 30)

        4. **Validate Gates**:
           - QG-BALANCE-001: Gini < 0.6
           - QG-BALANCE-005: F2P milestones 100% reachable
           - QG-BALANCE-006: Power gap < 2.0x

        5. **Check Convergence** (IG-BALANCE-001):
           - Detect outliers (>5σ)
           - Flag if >5% outliers

        OUTPUT: reports/balance/economy-simulation.md

    - role: difficulty-analyzer
      role_group: ANALYSIS
      parallel: true
      depends_on: [difficulty-parser]
      priority: 20
      model_override: sonnet
      prompt: |
        Analyze difficulty curve for smoothness and fairness.

        Using difficulty data:

        1. **Plot Difficulty Curve**:
           ```
           Difficulty
             ▲
             │     ╱╲    ← Spike (bad)
             │ ───╱  ╲───╱───
             │╱          ╲╱
             └──────────────────▶ Level
           ```

        2. **Detect Spikes**:
           FOR each pair of adjacent levels:
             delta = level[i+1].difficulty / level[i].difficulty
             IF delta > 2.0:
               FLAG as spike (QG-BALANCE-002 violation)

        3. **Check Pacing**:
           - Early game (levels 1-10): Should be easy (ramp-up)
           - Mid game (levels 11-30): Gradual increase
           - Late game (levels 31+): Challenge peaks

        4. **Identify Problem Levels**:
           - Levels where player power < required power
           - Levels requiring grinding > 2 days

        5. **Recommend Fixes**:
           - Smooth spikes with suggested difficulty values
           - Add progression aids (power-ups, skip options)

        OUTPUT: reports/balance/difficulty-analysis.md

    - role: meta-analyzer
      role_group: ANALYSIS
      parallel: true
      depends_on: [meta-parser]
      priority: 20
      model_override: sonnet
      prompt: |
        Analyze PvP meta concentration and character balance.

        Using meta data:

        1. **Calculate Power Variance** (QG-BALANCE-004):
           - Compute mean power across all characters
           - Compute standard deviation
           - CV (Coefficient of Variation) = σ / μ
           - Target: CV < 0.25

        2. **Generate Tier List**:
           | Tier | Characters | Power Range | % of Roster |
           |------|------------|-------------|-------------|
           | S | [names] | X-Y | Z% |
           | A | [names] | X-Y | Z% |
           | B | [names] | X-Y | Z% |
           | C | [names] | X-Y | Z% |
           | D | [names] | X-Y | Z% |

           Healthy distribution: S<10%, A<20%, B~40%, C<20%, D<10%

        3. **Meta Concentration** (QG-BALANCE-003):
           - Estimate top strategy usage
           - IF simulated/historical data available:
             - Top team composition usage %
           - ELSE:
             - Estimate from tier list (S-tier concentration)

           Target: Top meta < 30% usage

        4. **Identify Outliers**:
           - Overtuned: Power > μ + 2σ
           - Undertuned: Power < μ - 2σ

        5. **Recommend Nerfs/Buffs**:
           - Specific stat adjustments per character
           - Expected impact on tier list

        OUTPUT: reports/balance/meta-report.md

    # Wave 3: Synthesis & Reporting
    - role: balance-synthesizer
      role_group: REPORTING
      parallel: false
      depends_on: [economy-simulator, difficulty-analyzer, meta-analyzer]
      priority: 30
      model_override: opus
      prompt: |
        Synthesize all balance analyses into comprehensive report.

        AGGREGATE results from:
        - economy-simulation.md
        - difficulty-analysis.md
        - meta-report.md

        GENERATE reports/balance/balance-report.md:

        ## Executive Summary
        - Overall Balance Health Score (0-100)
        - Gate status summary
        - Top 3 issues

        ## Economy Balance
        - Gini coefficient result
        - Inflation rate result
        - F2P milestone reachability
        - P2W analysis

        ## Difficulty Balance
        - Curve smoothness
        - Spike locations
        - Pacing assessment

        ## Meta Balance
        - Power variance
        - Tier distribution
        - Meta concentration

        ## Quality Gate Results

        | Gate | Threshold | Actual | Status |
        |------|-----------|--------|--------|
        | QG-BALANCE-001 | Gini < 0.6 | X.XX | ✅/❌ |
        | QG-BALANCE-002 | Spike < 2.0x | X.Xx | ✅/❌ |
        | QG-BALANCE-003 | Meta < 30% | XX% | ✅/❌ |
        | QG-BALANCE-004 | CV < 0.25 | X.XX | ✅/❌ |
        | QG-BALANCE-005 | F2P 100% | XX% | ✅/❌ |
        | QG-BALANCE-006 | Gap < 2.0x | X.Xx | ✅/❌ |

        ## Recommendations
        - Prioritized list of fixes
        - Specific parameter adjustments
        - Expected impact

        GENERATE reports/balance/metrics.json:
        - All raw metrics in JSON format

        GENERATE reports/balance/recommendations.md:
        - Detailed fix recommendations with code examples

flags:
  economy_only: "--economy-only"                  # Run economy simulation only
  difficulty_only: "--difficulty-only"            # Run difficulty analysis only
  meta_only: "--meta-only"                        # Run meta analysis only
  runs: "--runs <N>"                              # Override simulation runs
  days: "--days <N>"                              # Override simulation days
  threshold: "--threshold <gate>=<value>"         # Override specific threshold
  export_csv: "--export-csv"                      # Export data as CSV
  compare: "--compare <previous-report>"          # Compare to previous run
  max_model: "--max-model <opus|sonnet|haiku>"    # Override model cap
---

# /speckit.balance - Balance Testing & Simulation

## Purpose

The `/speckit.balance` command provides comprehensive game balance validation through:

1. **Monte Carlo Economy Simulation**: Validate wealth distribution, inflation, F2P progression
2. **Difficulty Curve Analysis**: Detect spikes, pacing issues, grinding requirements
3. **PvP Meta Analysis**: Measure power variance, tier distribution, meta concentration
4. **Actionable Recommendations**: Specific parameter tweaks to fix imbalances

## When to Use

- **Pre-Production**: Validate economy design before implementation
- **Alpha/Beta**: Detect balance issues before wider testing
- **Pre-Soft Launch**: Final balance check before metrics
- **Live Operations**: Regular balance audits (weekly/monthly)
- **Post-Update**: Validate balance after content patches

## Balance Types

| Type | Focus | Key Metrics |
|------|-------|-------------|
| **economy** | Currency flow, progression | Gini, inflation, milestones |
| **difficulty** | Level progression | Spike ratio, grind time |
| **pvp_meta** | Character balance | Power CV, meta concentration |
| **full** | All above | All metrics |

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                       /speckit.balance                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WAVE 1: Data Collection (parallel)                             │
│  ├── Economy Parser → economy config                            │
│  ├── Difficulty Parser → difficulty curve data                  │
│  └── Meta Parser → character/unit data                          │
│                                                                  │
│  WAVE 2: Analysis (parallel)                                    │
│  ├── Economy Simulator → 30K Monte Carlo runs                   │
│  ├── Difficulty Analyzer → spike detection                      │
│  └── Meta Analyzer → power variance, tiers                      │
│                                                                  │
│  WAVE 3: Reporting                                              │
│  └── Balance Synthesizer → reports/*.md, metrics.json           │
│                                                                  │
│  QUALITY GATES:                                                 │
│  ├── QG-BALANCE-001: Gini < 0.6                                 │
│  ├── QG-BALANCE-002: Spike < 2.0x                               │
│  ├── QG-BALANCE-003: Meta < 30%                                 │
│  ├── QG-BALANCE-004: CV < 0.25                                  │
│  ├── QG-BALANCE-005: F2P 100% milestones                        │
│  └── QG-BALANCE-006: P2W gap < 2.0x                             │
│                                                                  │
│  HANDOFFS:                                                      │
│  ├── Failed economy gates → /speckit.gdd (update economy)       │
│  ├── Failed meta gates → /speckit.tasks (rebalance)             │
│  └── All passed → /speckit.softlaunch                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quality Gates Detail

### QG-BALANCE-001: Gini Coefficient

**Measures**: Wealth inequality across player population

```
Gini = 0   → Perfect equality (everyone has same wealth)
Gini = 1   → Perfect inequality (one player has everything)
```

**Threshold**: Gini < 0.6

**Industry Benchmarks**:
| Tier | Gini | Interpretation |
|------|------|----------------|
| Supercell | 0.4-0.5 | Healthy |
| King | 0.5-0.6 | Acceptable |
| P2W Heavy | 0.7+ | Problematic |

**If Failed**:
- Increase F2P earn rates
- Reduce whale-exclusive advantages
- Add soft currency catch-up mechanics

### QG-BALANCE-002: Difficulty Spike

**Measures**: Maximum difficulty increase between adjacent levels

```
Spike Ratio = Level[i+1].difficulty / Level[i].difficulty
```

**Threshold**: Max spike < 2.0x

**Example**:
```
Level 10: Difficulty 100
Level 11: Difficulty 250  ← SPIKE! (2.5x)
Level 12: Difficulty 260
```

**If Failed**:
- Smooth difficulty curve
- Add intermediate levels
- Provide power-ups at spike points

### QG-BALANCE-003: Meta Concentration

**Measures**: Usage of dominant strategy in PvP

**Threshold**: Top meta < 30% usage

**Healthy Meta**:
| Top Strategy Usage | Interpretation |
|--------------------|----------------|
| <15% | Diverse meta (excellent) |
| 15-30% | Healthy meta |
| 30-50% | Concentrated meta |
| >50% | Solved meta (needs nerf) |

**If Failed**:
- Nerf dominant strategy
- Buff weak strategies
- Add hard counters

### QG-BALANCE-004: Power Variance

**Measures**: Statistical spread of character power levels

```
CV (Coefficient of Variation) = Standard Deviation / Mean
```

**Threshold**: CV < 0.25 (25%)

**Interpretation**:
| CV | Interpretation |
|----|----------------|
| <0.15 | Very balanced |
| 0.15-0.25 | Healthy variance |
| 0.25-0.40 | Some outliers |
| >0.40 | Severe imbalance |

**If Failed**:
- Nerf overtuned characters (power > μ + 2σ)
- Buff undertuned characters (power < μ - 2σ)

### QG-BALANCE-005: F2P Milestone Reachability

**Measures**: Can F2P players reach all progression milestones?

**Threshold**: 100% milestones reachable within time budgets

**Example Milestones**:
| Milestone | F2P Budget | Actual (p50) | Status |
|-----------|------------|--------------|--------|
| Level 10 | 7 days | 6.2 days | ✅ |
| Raid Unlock | 30 days | 28 days | ✅ |
| Max Level | 120 days | 180 days | ❌ |

**If Failed**:
- Reduce milestone requirements
- Increase F2P earn rates
- Add catch-up events

### QG-BALANCE-006: Pay-to-Win Detection

**Measures**: Power advantage of whales over F2P at same time investment

```
P2W Gap = Whale Power (Day 30) / F2P Power (Day 30)
```

**Threshold**: Gap < 2.0x

**Interpretation**:
| Gap | Interpretation |
|-----|----------------|
| <1.5x | Skill-based (excellent) |
| 1.5-2.0x | Acceptable advantage |
| 2.0-3.0x | Significant P2W |
| >3.0x | Heavy P2W |

**If Failed**:
- Reduce whale power scaling
- Increase skill factor in PvP
- Cap power advantages in matchmaking

## Economy Simulation Details

### Player Archetypes

```python
F2P_ARCHETYPE = {
    "spending": 0,          # $0/month
    "playtime": 1.5,        # hours/day
    "hard_earn": 50,        # gems/day
    "soft_earn": 1000,      # gold/day
    "efficiency": 0.7,      # 70% optimal play
    "retention": 0.5,       # 50% at day 90
}

DOLPHIN_ARCHETYPE = {
    "spending": 25,         # $25/month
    "playtime": 3,          # hours/day
    "hard_earn": 550,       # gems/day (base + purchase)
    "soft_earn": 1500,      # gold/day
    "efficiency": 0.85,
    "retention": 0.7,
}

WHALE_ARCHETYPE = {
    "spending": 500,        # $500/month
    "playtime": 6,          # hours/day
    "hard_earn": 5050,      # gems/day
    "soft_earn": 2500,      # gold/day
    "efficiency": 0.95,
    "retention": 0.9,
}
```

### Simulation Algorithm

```python
def simulate_player(archetype, economy, days=90):
    state = {
        "hard_currency": 0,
        "soft_currency": 0,
        "power": 100,
        "milestones": [],
        "gacha_pulls": 0,
        "pity": 0,
    }

    for day in range(1, days + 1):
        # Earn (with ±20% variance)
        state["hard_currency"] += archetype["hard_earn"] * uniform(0.8, 1.2)
        state["soft_currency"] += archetype["soft_earn"] * uniform(0.8, 1.2)

        # Spend (gacha if affordable)
        while state["hard_currency"] >= economy["gacha_cost"]:
            state["hard_currency"] -= economy["gacha_cost"]
            state["gacha_pulls"] += 1
            state["pity"] += 1

            # Pity system
            if state["pity"] >= economy["pity_threshold"]:
                state["power"] += roll_ssr()
                state["pity"] = 0
            elif random() < economy["ssr_rate"]:
                state["power"] += roll_ssr()
                state["pity"] = 0
            else:
                state["power"] += roll_common()

        # Progression
        for milestone in economy["milestones"]:
            if state["power"] >= milestone["power"] and milestone not in state["milestones"]:
                state["milestones"].append(milestone)

    return state
```

## Difficulty Analysis Details

### Spike Detection Algorithm

```python
def detect_spikes(levels, threshold=2.0):
    spikes = []
    for i in range(len(levels) - 1):
        current = levels[i]["difficulty"]
        next_lvl = levels[i + 1]["difficulty"]
        ratio = next_lvl / current

        if ratio > threshold:
            spikes.append({
                "from_level": levels[i]["id"],
                "to_level": levels[i + 1]["id"],
                "ratio": ratio,
                "recommended_difficulty": current * 1.5,  # Smooth to 1.5x
            })
    return spikes
```

### Pacing Guidelines

```
┌─────────────────────────────────────────────────────────────┐
│                    IDEAL DIFFICULTY CURVE                    │
│                                                              │
│ Difficulty                                                   │
│     ▲                                                        │
│     │                            ╱── Late Game               │
│     │                     ╱─────╱    (Challenge)             │
│     │              ╱─────╱                                   │
│     │       ╱─────╱  Mid Game                                │
│     │ ╱────╱         (Growth)                                │
│     │╱                                                       │
│     │  Early Game                                            │
│     │  (Ramp-up)                                             │
│     └────────────────────────────────────────────────▶ Level │
│         1-10       11-30       31+                           │
└─────────────────────────────────────────────────────────────┘

Phase Guidelines:
- Early (1-10): Max 1.2x spike, total 3x growth
- Mid (11-30): Max 1.5x spike, total 5x growth
- Late (31+): Max 1.8x spike, no ceiling
```

## Meta Analysis Details

### Power Calculation

```python
def calculate_character_power(char):
    """
    Weighted power formula (customize per game)
    """
    base_stats = (
        char["hp"] * 0.3 +
        char["atk"] * 0.3 +
        char["def"] * 0.2 +
        char["spd"] * 0.2
    )

    skill_factor = sum(skill["multiplier"] for skill in char["skills"]) / len(char["skills"])

    rarity_bonus = {"SSR": 1.5, "SR": 1.2, "R": 1.0}[char["rarity"]]

    return base_stats * skill_factor * rarity_bonus
```

### Tier List Generation

```python
def generate_tier_list(characters):
    powers = [calculate_character_power(c) for c in characters]
    mean = np.mean(powers)
    std = np.std(powers)

    tiers = {"S": [], "A": [], "B": [], "C": [], "D": []}

    for char, power in zip(characters, powers):
        z_score = (power - mean) / std
        if z_score > 1.5:
            tiers["S"].append(char)
        elif z_score > 0.5:
            tiers["A"].append(char)
        elif z_score > -0.5:
            tiers["B"].append(char)
        elif z_score > -1.5:
            tiers["C"].append(char)
        else:
            tiers["D"].append(char)

    return tiers
```

## Report Templates

### Balance Report Summary

```markdown
# Game Balance Report

**Report Date**: {{DATE}}
**Build Version**: {{VERSION}}
**Simulation Runs**: {{RUNS}} per archetype

---

## Executive Summary

### Balance Health Score: {{SCORE}}/100

| Component | Score | Weight |
|-----------|-------|--------|
| Economy | X/100 | 40% |
| Difficulty | X/100 | 30% |
| Meta | X/100 | 30% |

### Gate Summary

| Gate | Status | Value | Threshold |
|------|--------|-------|-----------|
| QG-BALANCE-001 | ✅/❌ | X.XX | < 0.6 |
| QG-BALANCE-002 | ✅/❌ | X.Xx | < 2.0x |
| QG-BALANCE-003 | ✅/❌ | XX% | < 30% |
| QG-BALANCE-004 | ✅/❌ | X.XX | < 0.25 |
| QG-BALANCE-005 | ✅/❌ | XX% | 100% |
| QG-BALANCE-006 | ✅/❌ | X.Xx | < 2.0x |

### Top Issues

1. **{{ISSUE_1}}**: {{DESCRIPTION}}
2. **{{ISSUE_2}}**: {{DESCRIPTION}}
3. **{{ISSUE_3}}**: {{DESCRIPTION}}
```

### Recommendations Template

```markdown
# Balance Recommendations

## P0: Critical Fixes (Pre-Launch Blockers)

### FIX-001: {{TITLE}}

**Issue**: {{DESCRIPTION}}
**Gate Violated**: QG-BALANCE-XXX
**Current Value**: {{VALUE}}
**Target Value**: {{TARGET}}

**Recommended Change**:
```yaml
# Before
parameter_name: {{OLD_VALUE}}

# After
parameter_name: {{NEW_VALUE}}
```

**Expected Impact**:
- Metric will improve from X to Y
- No negative side effects expected

---

## P1: High Priority (Pre-Soft Launch)

### FIX-002: {{TITLE}}
...

## P2: Medium Priority (Pre-Global)
...

## P3: Low Priority (Post-Launch Polish)
...
```

## Industry Benchmarks

### Economy Benchmarks (F2P Mobile)

| Metric | Supercell | King | Voodoo | Your Target |
|--------|-----------|------|--------|-------------|
| Gini | 0.4-0.5 | 0.5-0.6 | N/A | < 0.6 |
| F2P Content | 95%+ | 90%+ | 100% | 95%+ |
| Time to Max | 2+ years | 1+ years | N/A | 6+ months |
| P2W Gap | 1.5x | 2.0x | 1.0x | < 2.0x |

### Difficulty Benchmarks

| Genre | Avg Session | Levels/Day | Spike Tolerance |
|-------|-------------|------------|-----------------|
| Casual | 5-10 min | 3-5 | < 1.5x |
| Mid-Core | 15-30 min | 1-3 | < 2.0x |
| Hardcore | 30-60 min | 0.5-1 | < 2.5x |

### Meta Benchmarks

| Game | Top Meta % | Power CV | Roster Size |
|------|-----------|----------|-------------|
| Clash Royale | 15-20% | 0.15 | 100+ cards |
| Brawl Stars | 10-15% | 0.18 | 60+ brawlers |
| Mobile Legends | 20-25% | 0.22 | 100+ heroes |
| Target | < 30% | < 0.25 | - |

## Example Output

```
/speckit.balance --balance_type=full --runs=10000 --days=90

✅ Wave 1: Data Collection
   ├── Parsed economy from docs/gdd/sections/04-economy.md
   ├── Parsed difficulty from 50 levels
   └── Parsed meta from 35 characters

✅ Wave 2: Analysis (30,000 simulations)
   ├── Economy simulation: 10K F2P + 10K Dolphin + 10K Whale
   ├── Difficulty analysis: 50 levels scanned
   └── Meta analysis: 35 characters evaluated

📊 Quality Gate Results:

   QG-BALANCE-001 (Gini): 0.52 < 0.6 ✅
   QG-BALANCE-002 (Spike): 1.8x < 2.0x ✅
   QG-BALANCE-003 (Meta): 28% < 30% ✅
   QG-BALANCE-004 (CV): 0.32 > 0.25 ❌
   QG-BALANCE-005 (F2P): 100% ✅
   QG-BALANCE-006 (P2W): 1.9x < 2.0x ✅

⚠️ Issues Found:
   ├── P1: Character power variance too high (CV=0.32)
   │   └── Overtuned: Hero_X (+2.1σ), Hero_Y (+1.8σ)
   │   └── Undertuned: Hero_Z (-2.3σ)
   └── P2: Level 25 difficulty spike approaching threshold (1.8x)

📁 Generated Reports:
   ├── reports/balance/balance-report.md
   ├── reports/balance/economy-simulation.md
   ├── reports/balance/difficulty-analysis.md
   ├── reports/balance/meta-report.md
   ├── reports/balance/metrics.json
   └── reports/balance/recommendations.md

💯 Balance Health Score: 78/100

🔗 Recommended Handoffs:
   → /speckit.tasks (Create rebalance tasks for Hero_X, Hero_Y, Hero_Z)
```

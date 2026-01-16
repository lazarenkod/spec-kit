---
description: Design comprehensive game progression - 200+ levels, difficulty curves, unlock gates, meta-progression (prestige, skill trees, ascension), and Flow Channel validation
flags:
  - name: --thinking-depth
    type: choice
    choices: [quick, standard, ultrathink]
    default: standard
    description: |
      Research depth and thinking budget per agent:
      - quick: 16K budget, 5 core agents, 90s timeout (~$0.32)
      - standard: 32K budget, 9 agents, 180s timeout (~$1.15) [RECOMMENDED]
      - ultrathink: 120K budget, 9 agents, 300s timeout (~$4.32) [EXPERT MODE]
handoffs:
  - label: Implement Progression
    agent: speckit.implement
  - label: Validate Balance
    agent: speckit.analyze
  - label: Generate Virality Hooks
    agent: speckit.games.virality
scripts:
  sh: echo "Game Progression Design - analyzing mechanics and concept for context"
  ps: Write-Host "Game Progression Design - analyzing mechanics and concept for context"
claude_code:
  model: opus
  reasoning_mode: extended
  thinking_budget: 120000
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
      ultrathink:
        thinking_budget: 120000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 3.5

  depth_defaults:
    quick:
      thinking_budget: 16000
      agents: 5
      timeout: 90
      skip_agents:
        - standards-researcher
        - academic-researcher
    standard:
      thinking_budget: 32000
      agents: 9
      timeout: 180
      skip_agents:
        - standards-researcher
        - academic-researcher
    ultrathink:
      thinking_budget: 120000
      agents: 9
      timeout: 300
      agent_selection: all

  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 32000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (120K thinking budget).
          Auto-downgrading to **Standard** mode (32K budget).

  cost_breakdown:
    quick: {cost: $0.32, time: "90-120s"}
    standard: {cost: $1.15, time: "180-240s"}
    ultrathink: {cost: $4.32, time: "300-360s"}

  cache_hierarchy: full
---

## Input
```text
$ARGUMENTS
```

---

## Purpose

**Design world-class game progression systems** with:

1. **200+ Level Design**: Tutorial (1-10), Easy (11-50), Medium (51-100), Hard (101-150), Expert (151-200+)
2. **Difficulty Formulas**: Mathematical models (exponential/logarithmic/s-curve) for balanced scaling
3. **Flow Channel Validation**: Ensure challenge matches player skill (avoid boredom/anxiety zones)
4. **Unlock Gates**: Timeline for introducing mechanics, power-ups, and features
5. **Meta-Progression**: Prestige systems, skill trees, account leveling, ascension mechanics
6. **Genre-Specific Templates**: Customized for match-3, idle, shooter, arcade, puzzle, runner

**Output Files** (4):
- `specs/games/progression.md` — Master progression spec (~30 pages)
- `specs/games/difficulty-curve.csv` — Level-by-level data (200+ rows)
- `specs/games/unlock-schedule.md` — Mechanic/power-up unlock timeline
- `specs/games/meta-progression.md` — Prestige, skill trees, account leveling, ascension

---

## Context Requirements

**MUST Read** (for context):
1. `specs/games/mechanics.md` — Core loop, mechanics, balancing formulas (from `/speckit.games.mechanics`)
2. `specs/games/concept.md` — Genre, target audience, monetization strategy (from `/speckit.games.concept`)

**Optional Read** (if exists):
3. `specs/games/virality.md` — K-factor, social hooks (for meta-progression rewards)

**Validation**:
- If `mechanics.md` or `concept.md` missing → ERROR: "Run /speckit.games.mechanics and /speckit.games.concept first"

---

## CLI Flags

### Required Flags

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--genre` | match3, idle, shooter, arcade, puzzle, runner, platformer | (required) | Game genre for template selection |

### Optional Flags

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--level-count` | 50, 100, 200, 500, infinite | 200 | Target number of levels to design |
| `--difficulty-model` | linear, exponential, logarithmic, s-curve | exponential | Mathematical model for difficulty scaling |
| `--flow-validation` | true, false | true | Enable Flow Channel validation during design |
| `--meta-depth` | basic, standard, deep | deep | Meta-progression depth (prestige only / + skill tree / + ascension) |
| `--csv-export` | true, false | true | Export difficulty-curve.csv for Excel/Google Sheets |
| `--skip-gates` | true, false | false | Skip quality gate validation (not recommended) |

### Usage Examples

```bash
# Match-3 game with 200 levels, exponential difficulty, full meta-progression
/speckit.games.progression --genre match3 --level-count 200 --meta-depth deep

# Idle game with infinite levels, fast scaling, ascension focus
/speckit.games.progression --genre idle --level-count infinite --difficulty-model exponential --meta-depth deep

# Shooter with 50 campaign levels, slow scaling, skill tree focus
/speckit.games.progression --genre shooter --level-count 50 --difficulty-model logarithmic --meta-depth standard

# Arcade with 100 levels, s-curve difficulty, basic meta
/speckit.games.progression --genre arcade --level-count 100 --difficulty-model s-curve --meta-depth basic
```

---

## Genre-Specific Templates

Each genre has customized parameters for optimal player experience:

| Genre | Levels | Difficulty Growth | Unlock Cadence | Meta Focus | Notes |
|-------|--------|-------------------|----------------|------------|-------|
| **Match-3** | 200 | 5% per level (moderate) | Every 10 levels | Prestige + skill tree | Balanced progression, emphasis on combos |
| **Idle** | Infinite | 8% per level (fast) | Every 5 levels | Prestige + ascension | Exponential scaling, prestige-driven |
| **Shooter** | 50 campaign + infinite survival | 3% per level (slow) | Every 5 levels | Skill tree + account level | Precision-based, slower scaling |
| **Arcade** | 100 | 6% per level (fast) | Every 8 levels | Account level + leaderboard | Fast-paced, score-driven |
| **Puzzle** | 150 | 4% per level (moderate) | Every 12 levels | Prestige + brain training | Logic-based, slower unlock cadence |
| **Runner** | Infinite | N/A (endless) | Every 500m distance | Prestige + character upgrades | Distance-based progression |
| **Platformer** | 60 | 4% per level (moderate) | Every 6 levels | Skill tree + collectibles | Skill-based, exploration rewards |

**Template Selection**:
- Genre flag automatically loads template parameters
- User can override with additional flags (--difficulty-model, --level-count)

---

## Execution Flow: 5 Phases, 7 Agents

### Phase 1: Context Analysis (1 agent)

**Agent**: `context-analyzer-agent`
**Model**: sonnet (8K thinking budget)
**Input**: mechanics.md, concept.md, CLI flags
**Output**: Context report (genre, mechanics summary, target audience, difficulty constraints)

**Tasks**:
1. Load and parse mechanics.md → extract core loop phases, mechanics, existing balancing formulas
2. Load and parse concept.md → extract genre, target audience, monetization model
3. Parse CLI flags → genre, level-count, difficulty-model, meta-depth
4. Identify progression constraints:
   - Genre-specific difficulty growth rate (from template)
   - Target level count (from flag or genre default)
   - Meta-progression requirements (from flag)
5. Generate context report:
   ```yaml
   genre: match3
   level_count: 200
   difficulty_model: exponential
   growth_rate: 0.05  # 5% per level (from match3 template)
   unlock_cadence: 10  # New unlock every 10 levels
   meta_depth: deep  # Prestige + skill tree + ascension
   target_audience: casual_mid_core
   monetization: f2p_iap
   core_mechanics: [swap, match3, special_tiles, combos]
   ```

**Validation**:
- ✅ mechanics.md exists and parsed
- ✅ concept.md exists and parsed
- ✅ Genre flag valid (one of 7 genres)
- ✅ Difficulty model valid (linear/exponential/logarithmic/s-curve)

---

### Phase 2: Difficulty Formula & Flow Channel Design (2 agents, parallel)

**Agent 1**: `difficulty-formula-agent`
**Model**: opus (24K thinking budget)
**Input**: Context report, genre template
**Output**: Difficulty formulas (difficulty scaling, component formulas, edge cases)

**Tasks**:
1. Design base difficulty formula based on genre and difficulty model:
   - **Linear**: `difficulty(level) = base + (level × growth_constant)`
   - **Exponential**: `difficulty(level) = base × (1 + growth_rate)^(level - 1)`
   - **Logarithmic**: `difficulty(level) = base × (1 + log(level) × growth_rate)`
   - **S-Curve**: `difficulty(level) = base × (1 / (1 + e^(-steepness × (level - midpoint))))`

2. Design component formulas (genre-specific):
   - **Match-3**: enemy_hp, move_limit, obstacle_density, special_tile_frequency
   - **Idle**: enemy_hp, enemy_damage, spawn_rate, boss_frequency
   - **Shooter**: enemy_hp, enemy_damage, enemy_speed, ai_complexity
   - **Arcade**: enemy_hp, enemy_speed, spawn_rate, pattern_complexity
   - **Puzzle**: piece_complexity, time_limit, constraint_difficulty
   - **Runner**: obstacle_density, speed_multiplier, gap_frequency

3. Validate difficulty slope between adjacent levels:
   - Calculate ratio: `slope = difficulty(level+1) / difficulty(level)`
   - Enforce constraint: `0.8 ≤ slope ≤ 1.2` (QG-PROGRESSION-001)
   - If violation detected → adjust formula parameters

4. Generate formula library with code examples:
   ```python
   # Match-3 Difficulty Formula (Exponential)
   def calculate_difficulty(level: int) -> float:
       base_difficulty = 10
       growth_rate = 0.05  # 5% per level
       return base_difficulty * ((1 + growth_rate) ** (level - 1))

   # Component Formulas
   def enemy_hp(level: int, difficulty: float) -> int:
       base_hp = 100
       return int(base_hp * difficulty)

   def move_limit(level: int, difficulty: float) -> int:
       base_moves = 30
       return max(10, int(base_moves - (level / 5)))

   def obstacle_density(level: int, difficulty: float) -> float:
       return min(0.4, 0.05 + (level * 0.002))  # Cap at 40%
   ```

**Edge Cases**:
- Level 1: Ensure minimal difficulty (tutorial)
- Level 100+: Prevent exponential explosion (cap or switch models)
- Infinite levels: Design asymptotic formula

---

**Agent 2**: `flow-channel-agent`
**Model**: opus (16K thinking budget)
**Input**: Context report, difficulty formulas (from Agent 1)
**Output**: Flow Channel boundaries, player skill growth model, validation results

**Tasks**:
1. Define Flow Channel theory for game design:
   - **Flow State**: Optimal challenge-skill balance (player fully engaged)
   - **Boredom Zone**: Challenge < Skill - 20% (too easy, player disengages)
   - **Anxiety Zone**: Challenge > Skill + 20% (too hard, player frustrated)
   - **Target**: Challenge ≈ Skill ± 5% (optimal flow)

2. Design player skill growth model:
   ```python
   def player_skill(level: int) -> float:
       base_skill = 10  # Starting competency
       skill_growth_rate = 0.6  # Player improves 60% per level
       return base_skill + (level * skill_growth_rate)
   ```

3. Calculate Flow Channel boundaries for each level:
   ```python
   skill = player_skill(level)
   boredom_threshold = skill * 0.8  # 20% below skill
   anxiety_threshold = skill * 1.2  # 20% above skill
   optimal_challenge = skill  # 1:1 ratio
   ```

4. Validate all levels against Flow Channel:
   - For each level 1-200:
     - Calculate difficulty (from Agent 1 formulas)
     - Calculate skill (from skill growth model)
     - Determine status: FLOW / BOREDOM / ANXIETY
     - If BOREDOM or ANXIETY → flag for adjustment

5. Generate validation report:
   ```markdown
   ## Flow Channel Validation Results

   - **Levels in Flow**: 198/200 (99%)
   - **Levels in Boredom Zone**: 2/200 (1%) — Levels 5, 12
   - **Levels in Anxiety Zone**: 0/200 (0%)

   **Status**: ✅ PASS (≥95% in Flow Channel)

   ### Adjustments Recommended:
   - Level 5: Reduce move limit from 28 to 25 (increase difficulty)
   - Level 12: Add obstacle density from 0.08 to 0.12 (increase difficulty)
   ```

**Validation** (QG-PROGRESSION-002):
- ✅ ≥95% of levels in Flow Channel (target: 100%)
- ✅ No critical anxiety spikes (player would rage quit)

---

### Phase 3: Level Design & Unlock Schedule (2 agents, parallel)

**Agent 3**: `level-designer-agent`
**Model**: opus (32K thinking budget)
**Input**: Difficulty formulas, Flow Channel validation, context report
**Output**: Level-by-level specifications (200+ levels), difficulty-curve.csv

**Tasks**:
1. Design level tiers with clear progression:

   **Tier 1: Tutorial (Levels 1-10)**
   - Purpose: Onboarding, teach core mechanics
   - Difficulty Range: 10-18 (growth factor 1.8x)
   - Objectives:
     - Level 1: Introduce swap mechanic (1-2 moves)
     - Level 2: Introduce match-3 detection (3 moves)
     - Level 3: Introduce special tiles (row/column clear, 5 moves)
     - Level 4: Introduce cascading (automatic chains, 8 moves)
     - Level 5: Introduce combo system (manual chains, 10 moves)
     - Level 6-10: Master core mechanics, gradual difficulty increase

   **Tier 2: Easy (Levels 11-50)**
   - Purpose: Core gameplay loop, build mastery
   - Difficulty Range: 20-120 (growth factor 6x)
   - Objectives:
     - Level 11-20: Master core mechanics, introduce soft obstacles (ice)
     - Level 21-30: Introduce hard obstacles (crates, chains)
     - Level 31-40: Introduce moving tiles, time pressure
     - Level 41-50: First boss/challenge level, reward milestone

   **Tier 3: Medium (Levels 51-100)**
   - Purpose: Deepen mastery, introduce complexity
   - Difficulty Range: 125-450 (growth factor 3.6x)
   - Objectives:
     - Level 51-60: Limited moves mode, strategic thinking
     - Level 61-70: Multiple objectives (collect + clear obstacles)
     - Level 71-80: Advanced special tiles (color bombs, lightning)
     - Level 81-90: Moving boards, environmental hazards
     - Level 91-100: Mid-game boss, prestige system unlock

   **Tier 4: Hard (Levels 101-150)**
   - Purpose: Expert gameplay, test mastery
   - Difficulty Range: 475-1100 (growth factor 2.3x)
   - Objectives:
     - Level 101-115: Complex boards (irregular shapes)
     - Level 116-130: Time attack + limited moves hybrid
     - Level 131-145: Multi-phase levels (change mid-level)
     - Level 146-150: Hard boss, skill tree second branch unlock

   **Tier 5: Expert (Levels 151-200)**
   - Purpose: Endgame challenge, prestige incentive
   - Difficulty Range: 1150-1800 (growth factor 1.6x)
   - Objectives:
     - Level 151-170: Maximum complexity, all mechanics combined
     - Level 171-190: Epic challenges, leaderboard push
     - Level 191-200: Ultimate boss, ascension unlock

2. Generate per-level specifications:
   ```markdown
   ### Level 42: "Crate Chaos"

   **Tier**: Easy (Mid-point milestone)
   **Difficulty**: 98.5
   **Objectives**:
   - Clear 20 crates (wooden boxes blocking tiles)
   - Collect 30 blue tiles
   - Complete in 25 moves or less

   **Mechanics Active**:
   - Swap, match-3, special tiles (row/column clear)
   - Cascading enabled
   - Combo system enabled
   - Obstacles: Crates (20 total, 2HP each)

   **Difficulty Components**:
   - Enemy HP: 9850 (98.5 × 100)
   - Move Limit: 25 (30 - 42/5 = 25)
   - Obstacle Density: 0.134 (0.05 + 42 × 0.002)
   - Special Tile Frequency: 15% (moderate)

   **Flow Channel Status**: ✅ FLOW (difficulty 98.5 vs skill 95.2, within ±20%)

   **Unlock**: None (mid-tier progression)

   **Rewards**:
   - Stars: 1-3 (based on moves remaining)
   - Coins: 150 (base) + 10 per star
   - XP: 420 (base) + 50 per star
   ```

3. Export difficulty-curve.csv:
   ```csv
   level,difficulty,enemy_hp,move_limit,obstacle_density,spawn_rate,skill_required,flow_status,unlock
   1,10,1000,30,0.052,0.5,10,FLOW,swap_mechanic
   2,10.5,1050,30,0.054,0.52,10.6,FLOW,match3_detection
   3,11,1100,29,0.056,0.54,11.2,FLOW,special_tiles
   ...
   42,98.5,9850,25,0.134,2.1,95.2,FLOW,
   ...
   100,450,45000,20,0.25,5.0,70,FLOW,prestige_unlock
   ...
   200,1800,180000,15,0.45,10.0,130,FLOW,ascension_unlock
   ```

4. Validate level count:
   - ✅ Level count ≥ target (QG-PROGRESSION-003)
   - ✅ All tiers have balanced progression
   - ✅ No sudden difficulty spikes (QG-PROGRESSION-001)

**Output Files**:
- `progression.md` — Full level specifications (~25 pages, levels 1-200)
- `difficulty-curve.csv` — Machine-readable data (200+ rows)

---

**Agent 4**: `unlock-scheduler-agent`
**Model**: sonnet (16K thinking budget)
**Input**: Level specifications, context report, genre template
**Output**: Unlock schedule (mechanics, power-ups, features)

**Tasks**:
1. Design unlock waves with proper pacing:

   **Wave 1: Core Mechanics (Levels 1-20)**
   - Purpose: Teach foundational gameplay
   - Cadence: Every 2-5 levels (frequent early unlocks)
   - Unlocks:
     - Level 1: Swap mechanic
     - Level 2: Match-3 detection
     - Level 3: Special tiles (row/column clear)
     - Level 5: Cascading (automatic chains)
     - Level 7: Combo system (manual chains)
     - Level 10: Power-up store unlock
     - Level 15: Cascade bonus multiplier
     - Level 20: Daily challenges unlock

   **Wave 2: Advanced Mechanics (Levels 21-50)**
   - Purpose: Deepen core loop, introduce complexity
   - Cadence: Every 5-10 levels (moderate pacing)
   - Unlocks:
     - Level 25: Obstacles (ice, crates)
     - Level 30: Moving tiles
     - Level 35: Limited moves mode
     - Level 40: Time attack mode
     - Level 45: Multi-objective levels
     - Level 50: Boss battles, first milestone reward

   **Wave 3: Power-Ups (Levels 51-100)**
   - Purpose: Player agency, strategic options
   - Cadence: Every 5-15 levels (slower, higher value)
   - Unlocks:
     - Level 55: Hammer (break 1 tile)
     - Level 60: Shuffle (randomize board)
     - Level 70: Extra moves (+5 moves)
     - Level 80: Color bomb (clear all of 1 color)
     - Level 90: Lightning (clear row + column)
     - Level 100: Rainbow (clear all tiles), prestige system unlock

   **Wave 4: Meta-Progression (Levels 101-150)**
   - Purpose: Long-term engagement, retention hooks
   - Cadence: Every 10-25 levels (major milestones)
   - Unlocks:
     - Level 100: Prestige system (soft reset with permanent bonuses)
     - Level 110: Skill tree (first branch: Offense)
     - Level 120: Account leveling system
     - Level 125: Skill tree (second branch: Defense)
     - Level 140: Prestige tier 2 (higher bonuses)
     - Level 150: Skill tree (third branch: Utility), hard boss

   **Wave 5: Endgame (Levels 151-200+)**
   - Purpose: Infinite replayability, prestige incentives
   - Cadence: Every 10-50 levels (rare, high-value)
   - Unlocks:
     - Level 160: Ascension (infinite progression, exponential difficulty)
     - Level 175: Legendary power-ups (rainbow+, ultimate combo)
     - Level 190: Ultimate challenges (extreme difficulty, leaderboard)
     - Level 200: Infinite mode (procedural levels, high scores)

2. Validate unlock pacing (QG-PROGRESSION-004):
   - ✅ New unlock every 5-15 levels (average)
   - ✅ No gaps > 15 levels without new content
   - ✅ Unlock cadence slows as levels increase (early: frequent, late: rare but valuable)

3. Generate unlock-schedule.md:
   ```markdown
   # Unlock Schedule

   ## Summary
   - **Total Unlocks**: 32
   - **Cadence**: Every 6.25 levels on average (200 levels / 32 unlocks)
   - **Validation**: ✅ PASS (no gaps > 15 levels)

   ## Wave 1: Core Mechanics (Levels 1-20)
   - Level 1: Swap mechanic
   - Level 2: Match-3 detection
   - Level 3: Special tiles (row/column clear)
   - Level 5: Cascading (automatic chains)
   - Level 7: Combo system (manual chains)
   - Level 10: Power-up store unlock
   - Level 15: Cascade bonus multiplier
   - Level 20: Daily challenges unlock

   ## Wave 2: Advanced Mechanics (Levels 21-50)
   ... (full wave specs)

   ## Wave 3: Power-Ups (Levels 51-100)
   ... (full wave specs)

   ## Wave 4: Meta-Progression (Levels 101-150)
   ... (full wave specs)

   ## Wave 5: Endgame (Levels 151-200+)
   ... (full wave specs)
   ```

**Output File**:
- `unlock-schedule.md` — Complete unlock timeline (~5 pages)

**Validation**:
- ✅ QG-PROGRESSION-004: Unlock cadence 5-15 levels
- ✅ Early game (1-50): Frequent unlocks (retention critical)
- ✅ Mid-game (51-150): Moderate pace (mastery building)
- ✅ Endgame (151-200+): Rare high-value unlocks (prestige incentive)

---

### Phase 4: Meta-Progression Design (1 agent)

**Agent 5**: `meta-progression-agent`
**Model**: opus (24K thinking budget)
**Input**: Level specifications, unlock schedule, context report, --meta-depth flag
**Output**: Meta-progression systems (prestige, skill trees, account leveling, ascension)

**Tasks**:
1. Design prestige system:

   **Prestige Mechanics**:
   - **Trigger**: Complete level 100, 200, 300, etc. (every 100 levels)
   - **Soft Reset**: Player restarts from level 1, loses progress
   - **Permanent Bonuses**: Keep prestige level, earn stars (prestige currency)
   - **Formula**: `prestige_level = floor(total_levels_completed / 100)`
   - **Bonus Scaling**: `permanent_bonus = 1 + (prestige_level × 0.1)` (10% per prestige)

   **Prestige Bonuses** (additive):
   - +10% coin earn rate per prestige level
   - +5% power-up effectiveness per prestige level
   - +3% XP earn rate per prestige level
   - Unlock exclusive skins at prestige 3, 5, 10
   - Unlock special power-ups at prestige 5, 10, 20

   **Prestige Currency: Stars**:
   - Earned on prestige: `stars = prestige_level × 100`
   - Used for: Permanent upgrades in star shop
   - Star shop items:
     - Coin multiplier: +10% (cost: 50 stars)
     - Power-up slots: +1 slot (cost: 100 stars)
     - Move bonus: +5 starting moves (cost: 150 stars)
     - Skip level: Skip 1 level (cost: 200 stars, limited use)

   **Prestige Milestones**:
   - Prestige 1 (Level 100): +10% bonuses, unlock star shop
   - Prestige 2 (Level 200): +20% bonuses, unlock prestige skins
   - Prestige 3 (Level 300): +30% bonuses, unlock special tiles
   - Prestige 5 (Level 500): +50% bonuses, unlock legendary power-ups
   - Prestige 10 (Level 1000): +100% bonuses, unlock infinite mode

   **Prestige Incentives**:
   - First 100 levels take ~10 hours (first-time learning)
   - With prestige bonuses, second run takes ~6 hours (40% faster)
   - Prestige 10 players can complete 100 levels in ~2 hours (80% faster)
   - Creates satisfying "power fantasy" loop

2. Design skill tree system:

   **Architecture**:
   - **Branches**: 3 (Offense, Defense, Utility)
   - **Total Nodes**: 60 (20 per branch)
   - **Max Depth**: 10 tiers per branch
   - **Unlock**: Level 110 (first branch), 125 (second), 150 (third)

   **Branch 1: Offense** (20 nodes)
   - Tier 1: +5% damage (cost: 10 stars)
   - Tier 2: +10% crit chance (cost: 20 stars, requires Tier 1)
   - Tier 3: +15% combo multiplier (cost: 40 stars, requires Tier 2)
   - Tier 4: +20% special tile spawn rate (cost: 80 stars, requires Tier 3)
   - Tier 5: +25% cascade bonus (cost: 160 stars, requires Tier 4)
   - Tier 6: +30% power-up duration (cost: 320 stars, requires Tier 5)
   - Tier 7: +35% boss damage (cost: 640 stars, requires Tier 6)
   - Tier 8: +40% final score multiplier (cost: 1280 stars, requires Tier 7)
   - Tier 9: +50% legendary power-up chance (cost: 2560 stars, requires Tier 8)
   - Tier 10: Ultimate Offense (cost: 5120 stars, requires Tier 9)

   **Branch 2: Defense** (20 nodes)
   - Tier 1: +10% move limit (cost: 10 stars)
   - Tier 2: +15% obstacle resistance (cost: 20 stars, requires Tier 1)
   - Tier 3: +20% starting power-ups (cost: 40 stars, requires Tier 2)
   - Tier 4: +25% revive chance (cost: 80 stars, requires Tier 3)
   - Tier 5: +30% shield duration (cost: 160 stars, requires Tier 4)
   - Tier 6: +35% damage reduction (cost: 320 stars, requires Tier 5)
   - Tier 7: +40% extra lives (cost: 640 stars, requires Tier 6)
   - Tier 8: +50% board healing (cost: 1280 stars, requires Tier 7)
   - Tier 9: +60% prestige bonus retention (cost: 2560 stars, requires Tier 8)
   - Tier 10: Ultimate Defense (cost: 5120 stars, requires Tier 9)

   **Branch 3: Utility** (20 nodes)
   - Tier 1: +10% coin earn rate (cost: 10 stars)
   - Tier 2: +15% XP earn rate (cost: 20 stars, requires Tier 1)
   - Tier 3: +20% daily challenge rewards (cost: 40 stars, requires Tier 2)
   - Tier 4: +25% star earn rate (cost: 80 stars, requires Tier 3)
   - Tier 5: +30% quest completion speed (cost: 160 stars, requires Tier 4)
   - Tier 6: +35% leaderboard score (cost: 320 stars, requires Tier 5)
   - Tier 7: +40% social bonus multiplier (cost: 640 stars, requires Tier 6)
   - Tier 8: +50% ascension efficiency (cost: 1280 stars, requires Tier 7)
   - Tier 9: +60% infinite mode scaling (cost: 2560 stars, requires Tier 8)
   - Tier 10: Ultimate Utility (cost: 5120 stars, requires Tier 9)

   **Total Cost**:
   - Full tree: 30,690 stars (all 60 nodes)
   - Single branch: 10,230 stars (20 nodes)
   - Average completion time: ~30 prestiges (~3000 levels)

   **Respec**:
   - Cost: 500 stars (refund 80% of spent stars)
   - Unlimited respec (encourages experimentation)

3. Design account leveling system:

   **XP Formula**:
   - `xp_required(account_level) = 100 × (account_level ^ 1.5)`
   - Level 1 → 2: 100 XP
   - Level 2 → 3: 283 XP
   - Level 10 → 11: 3,162 XP
   - Level 50 → 51: 35,355 XP
   - Level 100 → 101: 100,000 XP

   **XP Sources**:
   - Complete level: `base_xp + (level_number × 2)`
   - First-time completion: `bonus_xp = base_xp × 2`
   - 3-star completion: `bonus_xp = base_xp × 3`
   - Daily challenges: 500 XP each
   - Prestige: 5,000 XP
   - Boss defeats: 2,000 XP
   - Ascension milestones: 10,000 XP

   **Rewards per Account Level**:
   - Every level: 50 coins
   - Every 5 levels: 100 coins + 1 power-up pack
   - Every 10 levels: 200 coins + 5 stars + exclusive avatar
   - Every 25 levels: 500 coins + 20 stars + exclusive skin
   - Every 50 levels: 1,000 coins + 50 stars + legendary power-up
   - Every 100 levels: 5,000 coins + 200 stars + ultimate reward

   **Account Level Benefits**:
   - Permanent stat boosts (+1% all stats per level)
   - Unlock new game modes (level 25, 50, 100)
   - Prestige efficiency (+5% stars per 10 levels)
   - Social features (level 10: friends, level 25: guilds)

4. Design ascension mechanics (endgame):

   **Unlock Conditions**:
   - Account level 50+
   - Prestige level 5+
   - Complete level 200

   **Ascension Mechanics**:
   - **Infinite Progression**: No level cap, procedural generation
   - **Exponential Scaling**: `ascension_difficulty = base_difficulty × (2 ^ ascension_level)`
   - **Ascension Points**: Earned every 10 ascension levels, spent on permanent upgrades
   - **Leaderboard**: Global ranking for highest ascension level reached

   **Ascension Bonuses**:
   - Permanent 2× coin multiplier
   - Permanent 2× XP multiplier
   - Unlock ascension-exclusive power-ups:
     - Mega Rainbow (clear entire board)
     - Time Freeze (pause timer for 10 seconds)
     - Board Nuke (destroy all obstacles)
   - Access to infinite level generator
   - Ascension-only leaderboard

   **Ascension Formula**:
   ```python
   def ascension_difficulty(ascension_level: int) -> float:
       base_difficulty = 1800  # Level 200 difficulty
       return base_difficulty * (2 ** ascension_level)

   # Examples:
   # Ascension 1: 3,600 difficulty (2× level 200)
   # Ascension 5: 57,600 difficulty (32× level 200)
   # Ascension 10: 1,843,200 difficulty (1,024× level 200)
   ```

   **Ascension Incentives**:
   - Compete with top players globally
   - Showcase mastery and dedication
   - Infinite replayability
   - Prestige resets become faster (ascension bonuses stack with prestige)

5. Generate meta-progression.md:
   ```markdown
   # Meta-Progression Specification

   ## 1. Prestige System

   ### Formula
   prestige_level = floor(total_levels_completed / 100)
   permanent_bonus = 1 + (prestige_level × 0.1)  // 10% bonus per prestige

   ### Mechanics
   - **Soft Reset**: Player restarts from level 1 but keeps prestige bonuses
   - **Permanent Bonuses**:
     - +10% coin earn rate per prestige level
     - +5% power-up effectiveness per prestige level
     - +3% XP earn rate per prestige level
     - Unlock exclusive skins at prestige 3, 5, 10
   - **Prestige Currency: Stars** (earned on reset, used for permanent upgrades)

   ### Prestige Milestones
   - Prestige 1 (Level 100): +10% bonuses, unlock star shop
   - Prestige 2 (Level 200): +20% bonuses, unlock prestige skins
   - Prestige 3 (Level 300): +30% bonuses, unlock special tiles
   - Prestige 5 (Level 500): +50% bonuses, unlock legendary power-ups
   - Prestige 10 (Level 1000): +100% bonuses, unlock infinite mode

   ## 2. Skill Tree

   ### Architecture
   3 branches: Offense, Defense, Utility
   Total nodes: 60 (20 per branch)
   Max depth: 10 tiers

   ### Branch 1: Offense
   - Tier 1: +5% damage (cost: 10 stars)
   - Tier 2: +10% crit chance (cost: 20 stars, requires Tier 1)
   - Tier 3: +15% combo multiplier (cost: 40 stars, requires Tier 2)
   ... (60 nodes total)

   ### Branch 2: Defense
   ... (20 nodes)

   ### Branch 3: Utility
   ... (20 nodes)

   ### Total Cost
   - Full tree: 30,690 stars
   - Single branch: 10,230 stars
   - Average completion time: ~30 prestiges (~3000 levels)

   ## 3. Account Leveling

   ### XP Formula
   xp_required(account_level) = 100 × (account_level ^ 1.5)

   ### XP Sources
   - Complete level: base_xp + (level_number × 2)
   - First-time completion: bonus_xp = base_xp × 2
   - 3-star completion: bonus_xp = base_xp × 3
   - Daily challenges: 500 XP each
   - Prestige: 5,000 XP

   ### Rewards per Account Level
   - Every 5 levels: 100 coins + 1 power-up pack
   - Every 10 levels: 200 coins + 5 stars + exclusive avatar
   - Every 25 levels: 500 coins + 20 stars + exclusive skin
   - Every 50 levels: 1,000 coins + 50 stars + legendary power-up

   ## 4. Ascension Mechanics (Endgame)

   ### Unlock Condition
   - Account level 50+
   - Prestige level 5+
   - Complete level 200

   ### Ascension Bonuses
   - Permanent 2× coin multiplier
   - Unlock ascension-exclusive power-ups
   - Access to infinite level generator
   - Leaderboard for highest ascension level reached

   ### Ascension Formula
   ascension_difficulty = base_difficulty × (2 ^ ascension_level)
   // Exponential difficulty scaling for endgame challenge
   ```

**Output File**:
- `meta-progression.md` — Complete meta-progression systems (~8 pages)

**Validation** (QG-PROGRESSION-005):
- ✅ If --meta-depth=deep → Prestige + Skill Tree + Account Leveling + Ascension
- ✅ If --meta-depth=standard → Prestige + Skill Tree OR Account Leveling
- ✅ If --meta-depth=basic → Prestige only

---

### Phase 5: Validation & Export (1 agent)

**Agent 6**: `validator-exporter-agent`
**Model**: sonnet (16K thinking budget)
**Input**: All outputs from Phases 2-4, quality gate thresholds
**Output**: Validation report, CSV export, quality gate results

**Tasks**:
1. Validate difficulty slope (QG-PROGRESSION-001):
   ```python
   violations = []
   for level in range(1, 200):
       diff_current = difficulty(level)
       diff_next = difficulty(level + 1)
       slope = diff_next / diff_current

       if slope < 0.8 or slope > 1.2:
           violations.append({
               "level": level,
               "slope": slope,
               "severity": "CRITICAL"
           })

   # Status: PASS if violations == 0
   ```

2. Validate Flow Channel compliance (QG-PROGRESSION-002):
   ```python
   flow_violations = []
   for level in range(1, 200):
       difficulty = calculate_difficulty(level)
       skill = player_skill(level)
       gap = (difficulty - skill) / skill  # Percentage gap

       if gap < -0.2:
           flow_violations.append({"level": level, "status": "BOREDOM"})
       elif gap > 0.2:
           flow_violations.append({"level": level, "status": "ANXIETY"})

   # Status: PASS if flow_violations <= 5% of levels (10/200)
   ```

3. Validate level count (QG-PROGRESSION-003):
   ```python
   target_level_count = 200  # From --level-count flag
   actual_level_count = len(levels)

   if actual_level_count < target_level_count:
       status = "FAIL"
   else:
       status = "PASS"
   ```

4. Validate unlock gate pacing (QG-PROGRESSION-004):
   ```python
   unlocks = parse_unlock_schedule()
   gaps = []

   for i in range(len(unlocks) - 1):
       gap = unlocks[i+1].level - unlocks[i].level
       if gap > 15:
           gaps.append({
               "from": unlocks[i].level,
               "to": unlocks[i+1].level,
               "gap": gap,
               "severity": "MEDIUM"
           })

   # Status: PASS if gaps == 0
   ```

5. Validate meta-progression depth (QG-PROGRESSION-005):
   ```python
   meta_depth_flag = "deep"  # From --meta-depth flag

   requirements = {
       "basic": ["prestige"],
       "standard": ["prestige", "skill_tree OR account_leveling"],
       "deep": ["prestige", "skill_tree", "account_leveling", "ascension"]
   }

   actual_systems = parse_meta_progression()
   required_systems = requirements[meta_depth_flag]

   if all(system in actual_systems for system in required_systems):
       status = "PASS"
   else:
       status = "FAIL"
   ```

6. Export difficulty-curve.csv:
   ```python
   import csv

   with open("specs/games/difficulty-curve.csv", "w") as f:
       writer = csv.writer(f)
       writer.writerow([
           "level", "difficulty", "enemy_hp", "move_limit",
           "obstacle_density", "spawn_rate", "skill_required",
           "flow_status", "unlock"
       ])

       for level in range(1, 201):
           difficulty = calculate_difficulty(level)
           enemy_hp = enemy_hp_formula(level, difficulty)
           move_limit = move_limit_formula(level, difficulty)
           obstacle_density = obstacle_density_formula(level, difficulty)
           spawn_rate = spawn_rate_formula(level, difficulty)
           skill = player_skill(level)
           flow_status = calculate_flow_status(difficulty, skill)
           unlock = get_unlock_at_level(level) or ""

           writer.writerow([
               level, difficulty, enemy_hp, move_limit,
               obstacle_density, spawn_rate, skill,
               flow_status, unlock
           ])
   ```

7. Generate validation report:
   ```markdown
   # Validation Report

   ## Quality Gate Results

   ### QG-PROGRESSION-001: Difficulty Slope Compliance
   - **Status**: ✅ PASS
   - **Violations**: 0/200 levels
   - **Threshold**: 0.8 ≤ slope ≤ 1.2

   ### QG-PROGRESSION-002: Flow Channel Compliance
   - **Status**: ✅ PASS
   - **In Flow**: 198/200 (99%)
   - **Boredom Zone**: 2/200 (1%)
   - **Anxiety Zone**: 0/200 (0%)
   - **Threshold**: ≥95% in Flow Channel

   ### QG-PROGRESSION-003: Level Count Minimum
   - **Status**: ✅ PASS
   - **Target**: 200 levels
   - **Actual**: 200 levels

   ### QG-PROGRESSION-004: Unlock Gate Pacing
   - **Status**: ✅ PASS
   - **Gaps > 15 levels**: 0
   - **Average Cadence**: 6.25 levels per unlock
   - **Threshold**: New unlock every 5-15 levels

   ### QG-PROGRESSION-005: Meta-Progression Depth
   - **Status**: ✅ PASS
   - **Required**: Prestige + Skill Tree + Account Leveling + Ascension
   - **Actual**: All systems present

   ## Overall Status
   - **Status**: ✅ ALL GATES PASSED (5/5)
   - **Severity**: No CRITICAL or HIGH violations
   - **Ready for Implementation**: Yes

   ## Export Summary
   - ✅ progression.md generated (200 levels, ~30 pages)
   - ✅ difficulty-curve.csv exported (200 rows)
   - ✅ unlock-schedule.md generated (32 unlocks)
   - ✅ meta-progression.md generated (4 systems)
   ```

**Output Files** (finalized):
- `specs/games/progression.md`
- `specs/games/difficulty-curve.csv`
- `specs/games/unlock-schedule.md`
- `specs/games/meta-progression.md`
- `specs/games/progression-validation-report.md`

---

## Quality Gates (QG-PROGRESSION-001 through QG-PROGRESSION-005)

### QG-PROGRESSION-001: Difficulty Slope Compliance

**Category**: Progression Balancing
**Phase**: POST
**Severity**: CRITICAL

**Threshold**: `0.8 ≤ slope ≤ 1.2` between adjacent levels

**Description**: Ensures smooth difficulty progression without sudden spikes or drops. Difficulty slope is the ratio of difficulty between two adjacent levels: `slope = difficulty(level+1) / difficulty(level)`.

**Validation**:
```python
for level in range(1, total_levels):
    slope = difficulty(level + 1) / difficulty(level)
    assert 0.8 <= slope <= 1.2, f"Level {level}: slope {slope} out of range"
```

**Rationale**:
- Slope < 0.8: Difficulty drops (player feels regression, bad UX)
- Slope 0.8-1.0: Difficulty plateaus (acceptable for resting phases)
- Slope 1.0: Perfect continuity (ideal)
- Slope 1.0-1.2: Smooth increase (optimal challenge growth)
- Slope > 1.2: Sudden spike (player frustration, rage quit risk)

**Violations**:
- **CRITICAL**: Any slope < 0.8 or > 1.2 → blocks implementation
- **Fix**: Adjust difficulty formula parameters or add level-specific overrides

---

### QG-PROGRESSION-002: Flow Channel Compliance

**Category**: Player Experience
**Phase**: POST
**Severity**: HIGH

**Threshold**: ≥95% of levels within Flow Channel (challenge ≈ skill ± 20%)

**Description**: Validates that difficulty matches player skill growth to maintain Flow state (optimal engagement). Based on Mihaly Csikszentmihalyi's Flow theory:
- **Flow Zone**: Challenge ≈ Skill ± 20% (optimal engagement)
- **Boredom Zone**: Challenge < Skill - 20% (too easy, disengagement)
- **Anxiety Zone**: Challenge > Skill + 20% (too hard, frustration)

**Validation**:
```python
flow_count = 0
for level in range(1, total_levels):
    difficulty = calculate_difficulty(level)
    skill = player_skill(level)
    gap = abs((difficulty - skill) / skill)

    if gap <= 0.2:
        flow_count += 1

flow_percentage = (flow_count / total_levels) * 100
assert flow_percentage >= 95, f"Flow compliance: {flow_percentage}% < 95%"
```

**Rationale**:
- Flow state = maximum engagement, satisfaction, retention
- Boredom = player leaves (not challenged)
- Anxiety = player leaves (overwhelmed)
- Target: 100% in Flow, threshold: ≥95% (allow 5% edge cases)

**Violations**:
- **HIGH**: Flow compliance < 95% → requires review
- **Fix**: Adjust difficulty curve or player skill growth model

---

### QG-PROGRESSION-003: Level Count Minimum

**Category**: Content Depth
**Phase**: POST
**Severity**: HIGH

**Threshold**: `actual_level_count ≥ target_level_count` (from --level-count flag)

**Description**: Ensures sufficient content for target game depth. Prevents incomplete progression systems.

**Validation**:
```python
target = cli_flags["level_count"]  # e.g., 200
actual = len(levels_designed)

assert actual >= target, f"Level count {actual} < target {target}"
```

**Rationale**:
- Too few levels = incomplete progression, bad retention
- Target varies by genre:
  - Match-3: 200+ levels (standard)
  - Idle: Infinite (procedural generation)
  - Shooter: 50+ campaign levels
  - Arcade: 100+ levels

**Violations**:
- **HIGH**: Missing levels → blocks implementation
- **Fix**: Design remaining levels or adjust target

---

### QG-PROGRESSION-004: Unlock Gate Pacing

**Category**: Content Cadence
**Phase**: POST
**Severity**: MEDIUM

**Threshold**: New mechanic/power-up every 5-15 levels, no gaps > 15 levels

**Description**: Validates regular introduction of new content to prevent monotony. Players need fresh mechanics to maintain engagement.

**Validation**:
```python
unlocks = parse_unlock_schedule()
gaps = []

for i in range(len(unlocks) - 1):
    gap = unlocks[i+1].level - unlocks[i].level
    if gap > 15:
        gaps.append(gap)

assert len(gaps) == 0, f"Found {len(gaps)} gaps > 15 levels"
```

**Rationale**:
- Early game (1-50): Frequent unlocks (every 5 levels) for onboarding
- Mid game (51-150): Moderate pace (every 10 levels) for mastery
- Late game (151-200+): Rare unlocks (every 15 levels) for high-value rewards
- Gap > 15 levels = content drought, player boredom

**Violations**:
- **MEDIUM**: Gaps > 15 levels → requires review
- **Fix**: Add intermediate unlocks (cosmetics, minor power-ups)

---

### QG-PROGRESSION-005: Meta-Progression Depth

**Category**: Long-Term Retention
**Phase**: POST
**Severity**: HIGH (if --meta-depth flag enabled)

**Threshold**: Systems present match --meta-depth flag requirements

**Description**: Validates that meta-progression systems are specified according to requested depth:
- **basic**: Prestige system only
- **standard**: Prestige + (Skill Tree OR Account Leveling)
- **deep**: Prestige + Skill Tree + Account Leveling + Ascension

**Validation**:
```python
meta_depth = cli_flags["meta_depth"]  # "basic" | "standard" | "deep"
actual_systems = parse_meta_progression()

requirements = {
    "basic": ["prestige"],
    "standard": ["prestige", "skill_tree OR account_leveling"],
    "deep": ["prestige", "skill_tree", "account_leveling", "ascension"]
}

required = requirements[meta_depth]
assert all(s in actual_systems for s in required), f"Missing systems: {required}"
```

**Rationale**:
- Meta-progression = long-term retention (months, not weeks)
- Prestige = soft reset loop (proven retention mechanic)
- Skill Tree = player agency, customization
- Account Leveling = permanent progression, session goals
- Ascension = infinite endgame, competitive leaderboard

**Violations**:
- **HIGH**: Missing required systems → blocks implementation
- **Fix**: Design missing systems or reduce --meta-depth flag

---

## Self-Review Criteria

Before completing, validate:

### 1. Context Validation
- ✅ mechanics.md loaded and parsed
- ✅ concept.md loaded and parsed
- ✅ Genre flag valid and template loaded
- ✅ Difficulty model valid (linear/exponential/logarithmic/s-curve)

### 2. Formula Validation
- ✅ Difficulty formula defined with clear parameters
- ✅ Component formulas defined (genre-specific: HP, damage, etc.)
- ✅ Edge cases handled (Level 1, Level 100+, infinite)
- ✅ Code examples provided in Python/pseudocode

### 3. Level Design Validation
- ✅ 5 tiers defined (Tutorial, Easy, Medium, Hard, Expert)
- ✅ All 200 levels specified (or target level count)
- ✅ Per-level objectives clear (what player must do)
- ✅ Difficulty components calculated (HP, moves, obstacles, etc.)
- ✅ Flow Channel status validated for each level

### 4. Unlock Schedule Validation
- ✅ 5 waves defined (Core, Advanced, Power-Ups, Meta, Endgame)
- ✅ Unlock cadence appropriate (frequent early, rare late)
- ✅ No gaps > 15 levels without new content
- ✅ Each unlock clearly described (name, level, effect)

### 5. Meta-Progression Validation
- ✅ Prestige system defined (formula, bonuses, milestones)
- ✅ Skill tree defined (3 branches, 60 nodes, 10 tiers)
- ✅ Account leveling defined (XP formula, rewards)
- ✅ Ascension defined (unlock conditions, mechanics, bonuses)
- ✅ Meta-depth matches --meta-depth flag

### 6. Export Validation
- ✅ progression.md generated (~25-30 pages)
- ✅ difficulty-curve.csv exported (200+ rows, 9 columns)
- ✅ unlock-schedule.md generated (~5 pages)
- ✅ meta-progression.md generated (~8 pages)
- ✅ All files in specs/games/ directory

### 7. Quality Gates Validation
- ✅ QG-PROGRESSION-001: Difficulty slope 0.8-1.2 (PASS)
- ✅ QG-PROGRESSION-002: Flow Channel ≥95% (PASS)
- ✅ QG-PROGRESSION-003: Level count ≥ target (PASS)
- ✅ QG-PROGRESSION-004: Unlock pacing 5-15 levels (PASS)
- ✅ QG-PROGRESSION-005: Meta-depth matches flag (PASS)

---

## Genre-Specific Parameter Reference

### Match-3 (Default Template)

```yaml
genre: match3
base_difficulty: 10
growth_rate: 0.05  # 5% per level
difficulty_model: exponential
level_count: 200
unlock_cadence: 10  # New unlock every 10 levels

component_formulas:
  enemy_hp: base_hp × difficulty_multiplier
  move_limit: max(10, 30 - (level / 5))
  obstacle_density: min(0.4, 0.05 + (level × 0.002))
  special_tile_frequency: 0.15  # 15%
  cascade_bonus: 1.2  # 20% bonus per cascade

skill_growth:
  base_skill: 10
  skill_growth_rate: 0.6  # Player improves 60% per level

flow_channel:
  boredom_threshold: -0.2  # Skill - 20%
  anxiety_threshold: 0.2   # Skill + 20%
  optimal_zone: 0.05       # Skill ± 5%

meta_progression:
  prestige:
    trigger_level: 100
    bonus_per_prestige: 0.1  # 10%
    star_earn_rate: 100 per prestige
  skill_tree:
    branches: [offense, defense, utility]
    nodes_per_branch: 20
    unlock_levels: [110, 125, 150]
  account_leveling:
    xp_formula: "100 × (level ^ 1.5)"
    reward_cadence: [5, 10, 25, 50]
  ascension:
    unlock_level: 200
    scaling_formula: "base × (2 ^ ascension_level)"
```

### Idle (Fast Progression)

```yaml
genre: idle
base_difficulty: 100
growth_rate: 0.08  # 8% per level (faster scaling)
difficulty_model: exponential
level_count: infinite  # Procedural generation
unlock_cadence: 5  # New unlock every 5 levels

component_formulas:
  enemy_hp: base_hp × (difficulty ^ 1.2)  # Exponential HP
  enemy_damage: base_dmg × (difficulty ^ 0.9)
  spawn_rate: base_rate + (level / 10)
  boss_frequency: every_10_levels

skill_growth:
  base_skill: 100
  skill_growth_rate: 1.0  # Player improves 100% per level (DPS scaling)

flow_channel:
  boredom_threshold: -0.3  # More forgiving (idle mechanics)
  anxiety_threshold: 0.3
  optimal_zone: 0.1

meta_progression:
  prestige:
    trigger_level: 100
    bonus_per_prestige: 0.15  # 15% (higher for idle)
    star_earn_rate: 200 per prestige
  skill_tree:
    branches: [dps, gold, prestige]
    nodes_per_branch: 25  # More nodes for idle
    unlock_levels: [50, 100, 150]
  account_leveling:
    xp_formula: "100 × (level ^ 1.3)"  # Faster leveling
    reward_cadence: [5, 10, 20, 40]
  ascension:
    unlock_level: 500
    scaling_formula: "base × (3 ^ ascension_level)"  # Faster scaling
```

### Shooter (Precision-Based)

```yaml
genre: shooter
base_difficulty: 50
growth_rate: 0.03  # 3% per level (slower scaling)
difficulty_model: logarithmic  # Gradual increase
level_count: 50  # Campaign + infinite survival mode
unlock_cadence: 5  # New weapon/ability every 5 levels

component_formulas:
  enemy_hp: base_hp × (difficulty ^ 0.8)  # Slower HP scaling
  enemy_damage: base_dmg × (difficulty ^ 1.1)  # Faster damage scaling
  enemy_speed: base_speed + (level × 0.05)
  ai_complexity: min(5, 1 + (level / 10))  # AI tiers 1-5

skill_growth:
  base_skill: 50
  skill_growth_rate: 0.4  # Player improves 40% per level (skill-based)

flow_channel:
  boredom_threshold: -0.15  # Tighter (precision game)
  anxiety_threshold: 0.15
  optimal_zone: 0.03

meta_progression:
  prestige:
    trigger_level: 50
    bonus_per_prestige: 0.08  # 8% (lower for skill-based)
    star_earn_rate: 50 per prestige
  skill_tree:
    branches: [weapon_mastery, movement, survival]
    nodes_per_branch: 20
    unlock_levels: [25, 40, 50]
  account_leveling:
    xp_formula: "100 × (level ^ 1.6)"  # Slower leveling (skill-based)
    reward_cadence: [10, 25, 50]
  ascension:
    unlock_level: 100
    scaling_formula: "base × (1.5 ^ ascension_level)"  # Moderate scaling
```

### Arcade (Fast-Paced)

```yaml
genre: arcade
base_difficulty: 20
growth_rate: 0.06  # 6% per level (fast scaling)
difficulty_model: exponential
level_count: 100
unlock_cadence: 8  # New feature every 8 levels

component_formulas:
  enemy_hp: base_hp × difficulty
  enemy_speed: base_speed × (1 + level × 0.03)
  spawn_rate: base_rate + (level × 0.1)  # Fast spawning
  pattern_complexity: min(10, 1 + (level / 10))

skill_growth:
  base_skill: 20
  skill_growth_rate: 0.7  # Player improves 70% per level

flow_channel:
  boredom_threshold: -0.25  # More forgiving (fast-paced)
  anxiety_threshold: 0.25
  optimal_zone: 0.08

meta_progression:
  prestige:
    trigger_level: 100
    bonus_per_prestige: 0.12  # 12%
    star_earn_rate: 150 per prestige
  skill_tree:
    branches: [score_multiplier, lives, power_ups]
    nodes_per_branch: 15  # Simpler tree
    unlock_levels: [50, 75, 100]
  account_leveling:
    xp_formula: "100 × (level ^ 1.4)"
    reward_cadence: [5, 10, 25, 50]
  ascension:
    unlock_level: 200
    scaling_formula: "base × (2.5 ^ ascension_level)"
```

### Puzzle (Logic-Based)

```yaml
genre: puzzle
base_difficulty: 5
growth_rate: 0.04  # 4% per level (moderate)
difficulty_model: linear  # Steady increase
level_count: 150
unlock_cadence: 12  # New mechanic every 12 levels (slower)

component_formulas:
  piece_complexity: 1 + (level / 20)  # Gradual increase
  time_limit: max(30, 180 - (level × 2))  # Decreasing time
  constraint_difficulty: min(5, 1 + (level / 30))
  hint_availability: max(0, 5 - (level / 30))

skill_growth:
  base_skill: 5
  skill_growth_rate: 0.5  # Player improves 50% per level

flow_channel:
  boredom_threshold: -0.2
  anxiety_threshold: 0.2
  optimal_zone: 0.05

meta_progression:
  prestige:
    trigger_level: 150
    bonus_per_prestige: 0.10  # 10%
    star_earn_rate: 100 per prestige
  skill_tree:
    branches: [logic, speed, creativity]
    nodes_per_branch: 18
    unlock_levels: [75, 100, 125]
  account_leveling:
    xp_formula: "100 × (level ^ 1.5)"
    reward_cadence: [10, 20, 50]
  ascension:
    unlock_level: 250
    scaling_formula: "base × (1.8 ^ ascension_level)"
```

### Runner (Endless)

```yaml
genre: runner
base_difficulty: null  # Infinite runner, no fixed difficulty
growth_rate: null
difficulty_model: distance_based  # Difficulty scales with distance
level_count: infinite
unlock_cadence: every_500m  # New unlock every 500m

component_formulas:
  obstacle_density: 0.1 + (distance / 1000) × 0.05  # 5% per 1000m
  speed_multiplier: 1.0 + (distance / 500) × 0.1  # 10% per 500m
  gap_frequency: 0.2 + (distance / 2000) × 0.05  # 5% per 2000m
  power_up_spawn_rate: max(0.1, 0.5 - (distance / 5000) × 0.1)

skill_growth:
  base_skill: null  # Reaction time improves with play time
  skill_growth_rate: 0.3  # Player improves 30% per 1000m

flow_channel:
  boredom_threshold: -0.3  # Forgiving (endless game)
  anxiety_threshold: 0.3
  optimal_zone: 0.1

meta_progression:
  prestige:
    trigger_distance: 10000m  # Prestige every 10km
    bonus_per_prestige: 0.15  # 15%
    star_earn_rate: 50 per prestige
  skill_tree:
    branches: [speed, agility, magnetism]
    nodes_per_branch: 20
    unlock_milestones: [5000m, 10000m, 20000m]
  account_leveling:
    xp_formula: "distance / 10"  # 1 XP per 10m
    reward_cadence: [1000m, 5000m, 10000m]
  ascension:
    unlock_distance: 50000m
    scaling_formula: "base × (2 ^ ascension_level)"
```

---

## Example Output Files

### 1. progression.md (Sample Structure)

```markdown
# Game Progression Specification

## Metadata
- **Genre**: Match-3
- **Total Levels**: 200
- **Difficulty Model**: Exponential
- **Flow Channel**: Enabled
- **Meta-Depth**: Deep (Prestige + Skill Tree + Account Leveling + Ascension)

---

## Difficulty Formula

### Base Formula
difficulty(level) = base_difficulty × (1 + growth_rate)^(level - 1)

**Parameters**:
- Base difficulty: 10
- Growth rate: 0.05 (5% per level)

### Component Formulas

**Enemy HP**:
```python
def enemy_hp(level: int, difficulty: float) -> int:
    base_hp = 100
    return int(base_hp * difficulty)
```

**Move Limit**:
```python
def move_limit(level: int) -> int:
    base_moves = 30
    return max(10, int(base_moves - (level / 5)))
```

**Obstacle Density**:
```python
def obstacle_density(level: int) -> float:
    return min(0.4, 0.05 + (level * 0.002))
```

---

## Level Tiers

### Tier 1: Tutorial (Levels 1-10)

**Purpose**: Onboarding, teach core mechanics
**Difficulty Range**: 10-18 (growth factor 1.8x)

#### Level 1: "First Match"
- **Difficulty**: 10
- **Objective**: Make 1 match-3 (swap 2 tiles)
- **Mechanics**: Swap only, no special tiles
- **Move Limit**: 1-2 moves
- **Rewards**: 50 coins, 100 XP
- **Flow Status**: ✅ FLOW (difficulty 10 vs skill 10)

#### Level 2: "Learning the Basics"
- **Difficulty**: 10.5
- **Objective**: Make 3 match-3 combinations
- **Mechanics**: Swap + match-3 detection
- **Move Limit**: 3 moves
- **Rewards**: 60 coins, 120 XP
- **Flow Status**: ✅ FLOW (difficulty 10.5 vs skill 10.6)

... (levels 3-10)

### Tier 2: Easy (Levels 11-50)
... (full tier specs)

### Tier 3: Medium (Levels 51-100)
... (full tier specs)

### Tier 4: Hard (Levels 101-150)
... (full tier specs)

### Tier 5: Expert (Levels 151-200)
... (full tier specs)

---

## Flow Channel Validation

### Player Skill Growth Model
skill(level) = base_skill + (level × skill_growth_rate)
- Base skill: 10 (starting competency)
- Skill growth: 0.6 per level (player improves 60% per level)

### Flow Channel Boundaries
- **Boredom Threshold**: skill - 20% (challenge too easy)
- **Anxiety Threshold**: skill + 20% (challenge too hard)
- **Target**: skill ± 5% (optimal flow state)

### Validation Results
- ✅ Levels in Flow: 198/200 (99%)
- ⚠️ Levels in Boredom Zone: 2/200 (1%) — Levels 5, 12
- ✅ Levels in Anxiety Zone: 0/200 (0%)

**Status**: ✅ PASS (≥95% in Flow Channel)

### Adjustments Made
- Level 5: Reduced move limit from 28 to 25 (increased difficulty)
- Level 12: Added obstacle density from 0.08 to 0.12 (increased difficulty)

---

## Difficulty Slope Validation

### Validation Results
- ✅ All 199 slopes within range 0.8-1.2
- Average slope: 1.049 (optimal)
- Min slope: 0.98 (Level 45 → 46, gradual increase)
- Max slope: 1.18 (Level 99 → 100, pre-prestige milestone)

**Status**: ✅ PASS (QG-PROGRESSION-001)

---

## Summary

- **Total Levels**: 200
- **Total Unlocks**: 32
- **Meta-Progression Systems**: 4 (Prestige, Skill Tree, Account Leveling, Ascension)
- **Quality Gates**: 5/5 PASSED
- **Estimated Completion Time**: 80 hours (casual player, first playthrough)
- **Prestige Completion Time**: 30 hours (with prestige bonuses)
- **Retention Target**: 30-day retention ≥40%, 90-day retention ≥20%

---

**Version**: 1.0.0
**Generated**: 2026-01-14
**Command**: /speckit.games.progression --genre match3 --level-count 200 --meta-depth deep
```

---

### 2. difficulty-curve.csv (Sample Rows)

```csv
level,difficulty,enemy_hp,move_limit,obstacle_density,spawn_rate,skill_required,flow_status,unlock
1,10,1000,30,0.052,0.5,10,FLOW,swap_mechanic
2,10.5,1050,30,0.054,0.52,10.6,FLOW,match3_detection
3,11,1100,29,0.056,0.54,11.2,FLOW,special_tiles
4,11.6,1160,29,0.058,0.56,11.8,FLOW,
5,12.2,1220,29,0.06,0.58,12.4,FLOW,cascading
10,15.5,1550,28,0.07,0.7,16,FLOW,power_up_store
20,25.3,2530,26,0.09,1.0,22,FLOW,daily_challenges
50,120,12000,20,0.15,2.5,40,FLOW,boss_battle
100,450,45000,15,0.25,5.0,70,FLOW,prestige_unlock
150,1100,110000,12,0.35,7.5,100,FLOW,skill_tree_branch_3
200,1800,180000,10,0.45,10.0,130,FLOW,ascension_unlock
```

---

### 3. unlock-schedule.md (Sample Structure)

```markdown
# Unlock Schedule

## Summary
- **Total Unlocks**: 32
- **Average Cadence**: 6.25 levels per unlock (200 / 32)
- **Validation**: ✅ PASS (no gaps > 15 levels, QG-PROGRESSION-004)

---

## Wave 1: Core Mechanics (Levels 1-20)
**Purpose**: Teach foundational gameplay
**Cadence**: Every 2-5 levels (frequent early unlocks)

| Level | Unlock | Type | Description |
|-------|--------|------|-------------|
| 1 | Swap Mechanic | Core | Swap two adjacent tiles |
| 2 | Match-3 Detection | Core | System detects and clears 3+ matches |
| 3 | Special Tiles | Core | Row/Column clear tiles on match-4/5 |
| 5 | Cascading | Core | Automatic chain reactions |
| 7 | Combo System | Core | Manual chaining for bonus points |
| 10 | Power-Up Store | Feature | Purchase power-ups with coins |
| 15 | Cascade Bonus | Feature | +20% points per cascade level |
| 20 | Daily Challenges | Feature | Complete daily tasks for rewards |

---

## Wave 2: Advanced Mechanics (Levels 21-50)
**Purpose**: Deepen core loop, introduce complexity
**Cadence**: Every 5-10 levels (moderate pacing)

| Level | Unlock | Type | Description |
|-------|--------|------|-------------|
| 25 | Obstacles | Mechanic | Ice and crates blocking tiles |
| 30 | Moving Tiles | Mechanic | Tiles shift position mid-game |
| 35 | Limited Moves Mode | Mode | Complete objective in N moves |
| 40 | Time Attack Mode | Mode | Complete objective before timer expires |
| 45 | Multi-Objective Levels | Mechanic | Multiple goals per level |
| 50 | Boss Battles | Event | Epic challenge levels with unique mechanics |

---

## Wave 3: Power-Ups (Levels 51-100)
**Purpose**: Player agency, strategic options
**Cadence**: Every 5-15 levels (slower, higher value)

| Level | Unlock | Type | Description |
|-------|--------|------|-------------|
| 55 | Hammer | Power-Up | Break 1 tile manually |
| 60 | Shuffle | Power-Up | Randomize entire board |
| 70 | Extra Moves | Power-Up | +5 moves to move limit |
| 80 | Color Bomb | Power-Up | Clear all tiles of 1 color |
| 90 | Lightning | Power-Up | Clear row + column |
| 100 | Rainbow | Power-Up | Clear all tiles on board |

---

## Wave 4: Meta-Progression (Levels 101-150)
**Purpose**: Long-term engagement, retention hooks
**Cadence**: Every 10-25 levels (major milestones)

| Level | Unlock | Type | Description |
|-------|--------|------|-------------|
| 100 | Prestige System | Meta | Soft reset with permanent bonuses |
| 110 | Skill Tree (Branch 1) | Meta | Offense branch: damage, crits, combos |
| 120 | Account Leveling | Meta | Permanent account progression |
| 125 | Skill Tree (Branch 2) | Meta | Defense branch: moves, shields, revives |
| 140 | Prestige Tier 2 | Meta | Higher prestige bonuses (20% → 30%) |
| 150 | Skill Tree (Branch 3) | Meta | Utility branch: coins, XP, rewards |

---

## Wave 5: Endgame (Levels 151-200+)
**Purpose**: Infinite replayability, prestige incentives
**Cadence**: Every 10-50 levels (rare, high-value)

| Level | Unlock | Type | Description |
|-------|--------|------|-------------|
| 160 | Ascension | Meta | Infinite progression with exponential difficulty |
| 175 | Legendary Power-Ups | Power-Up | Mega Rainbow, Time Freeze, Board Nuke |
| 190 | Ultimate Challenges | Event | Extreme difficulty, leaderboard ranking |
| 200 | Infinite Mode | Mode | Procedural levels, endless high score chase |

---

## Unlock Gaps Analysis

**Largest Gaps**:
- Level 150 → 160: 10 levels (acceptable, post-major milestone)
- Level 175 → 190: 15 levels (threshold, acceptable for late game)
- Level 190 → 200: 10 levels (acceptable, final unlock)

**Status**: ✅ PASS (no gaps > 15 levels)

---

**Version**: 1.0.0
**Generated**: 2026-01-14
```

---

### 4. meta-progression.md (Sample Structure)

```markdown
# Meta-Progression Specification

## Overview

This document specifies all meta-progression systems for long-term player retention:
1. **Prestige System** — Soft reset with permanent bonuses
2. **Skill Tree** — Player customization and specialization
3. **Account Leveling** — Permanent account progression
4. **Ascension** — Infinite endgame progression

---

## 1. Prestige System

### Formula
```python
prestige_level = floor(total_levels_completed / 100)
permanent_bonus = 1 + (prestige_level × 0.1)  # 10% bonus per prestige
```

### Mechanics

**Soft Reset**:
- Player restarts from level 1
- Loses all level progress, coins, power-ups
- Keeps prestige level, stars (prestige currency), account level

**Permanent Bonuses** (additive):
- +10% coin earn rate per prestige level
- +5% power-up effectiveness per prestige level
- +3% XP earn rate per prestige level
- Unlock exclusive skins at prestige 3, 5, 10
- Unlock special power-ups at prestige 5, 10, 20

### Prestige Currency: Stars

**Earn Rate**:
- `stars = prestige_level × 100` (earned on prestige)
- Example: Prestige 5 → earn 500 stars

**Star Shop** (permanent upgrades):
| Item | Cost | Effect |
|------|------|--------|
| Coin Multiplier +10% | 50 stars | Permanent +10% coin earn rate |
| Power-Up Slot +1 | 100 stars | Unlock additional power-up slot |
| Move Bonus +5 | 150 stars | Start each level with +5 moves |
| Skip Level Token | 200 stars | Skip 1 level (limited to 10 uses) |
| Prestige Speed +20% | 500 stars | Prestige runs complete 20% faster |

### Prestige Milestones

| Prestige Level | Total Levels | Bonuses | Special Unlocks |
|----------------|--------------|---------|-----------------|
| Prestige 1 | 100 | +10% | Star shop unlock |
| Prestige 2 | 200 | +20% | Prestige skins (5 skins) |
| Prestige 3 | 300 | +30% | Special tiles (prestige-exclusive) |
| Prestige 5 | 500 | +50% | Legendary power-ups |
| Prestige 10 | 1000 | +100% | Infinite mode unlock |
| Prestige 20 | 2000 | +200% | Ultimate prestige skin |

### Prestige Incentives

**Time Reduction** (with bonuses):
- First run (no prestige): ~10 hours to level 100
- Prestige 1 run (+10%): ~6 hours to level 100 (40% faster)
- Prestige 5 run (+50%): ~4 hours to level 100 (60% faster)
- Prestige 10 run (+100%): ~2 hours to level 100 (80% faster)

**Power Fantasy**:
- Early levels become trivial (one-shot enemies)
- Player feels god-like progression
- Satisfying "I was weak, now I'm strong" loop

---

## 2. Skill Tree

### Architecture

- **Branches**: 3 (Offense, Defense, Utility)
- **Total Nodes**: 60 (20 per branch)
- **Max Depth**: 10 tiers per branch
- **Unlock**: Level 110 (first branch), 125 (second), 150 (third)

### Branch 1: Offense (20 nodes)

| Tier | Node Name | Cost | Effect | Requires |
|------|-----------|------|--------|----------|
| 1 | Damage Boost | 10 stars | +5% damage | None |
| 2 | Critical Hit | 20 stars | +10% crit chance | Tier 1 |
| 3 | Combo Master | 40 stars | +15% combo multiplier | Tier 2 |
| 4 | Special Spawn | 80 stars | +20% special tile spawn | Tier 3 |
| 5 | Cascade God | 160 stars | +25% cascade bonus | Tier 4 |
| 6 | Power-Up Duration | 320 stars | +30% power-up time | Tier 5 |
| 7 | Boss Slayer | 640 stars | +35% boss damage | Tier 6 |
| 8 | Score Multiplier | 1280 stars | +40% final score | Tier 7 |
| 9 | Legendary Chance | 2560 stars | +50% legendary drop | Tier 8 |
| 10 | Ultimate Offense | 5120 stars | +100% all offensive stats | Tier 9 |

**Total Cost**: 10,230 stars (single branch)

### Branch 2: Defense (20 nodes)

| Tier | Node Name | Cost | Effect | Requires |
|------|-----------|------|--------|----------|
| 1 | Extra Moves | 10 stars | +10% move limit | None |
| 2 | Obstacle Resist | 20 stars | +15% obstacle resist | Tier 1 |
| 3 | Starting Power-Ups | 40 stars | +20% starting power-ups | Tier 2 |
| 4 | Revive Chance | 80 stars | +25% revive chance | Tier 3 |
| 5 | Shield Duration | 160 stars | +30% shield time | Tier 4 |
| 6 | Damage Reduction | 320 stars | +35% damage reduction | Tier 5 |
| 7 | Extra Lives | 640 stars | +40% extra lives | Tier 6 |
| 8 | Board Healing | 1280 stars | +50% board heal | Tier 7 |
| 9 | Prestige Retention | 2560 stars | +60% prestige bonus | Tier 8 |
| 10 | Ultimate Defense | 5120 stars | +100% all defensive stats | Tier 9 |

**Total Cost**: 10,230 stars (single branch)

### Branch 3: Utility (20 nodes)

| Tier | Node Name | Cost | Effect | Requires |
|------|-----------|------|--------|----------|
| 1 | Coin Bonus | 10 stars | +10% coin earn | None |
| 2 | XP Bonus | 20 stars | +15% XP earn | Tier 1 |
| 3 | Daily Rewards | 40 stars | +20% daily rewards | Tier 2 |
| 4 | Star Bonus | 80 stars | +25% star earn | Tier 3 |
| 5 | Quest Speed | 160 stars | +30% quest speed | Tier 4 |
| 6 | Leaderboard Boost | 320 stars | +35% leaderboard score | Tier 5 |
| 7 | Social Bonus | 640 stars | +40% social multiplier | Tier 6 |
| 8 | Ascension Efficiency | 1280 stars | +50% ascension bonus | Tier 7 |
| 9 | Infinite Scaling | 2560 stars | +60% infinite mode | Tier 8 |
| 10 | Ultimate Utility | 5120 stars | +100% all utility stats | Tier 9 |

**Total Cost**: 10,230 stars (single branch)

### Skill Tree Totals

- **Full Tree Cost**: 30,690 stars (all 60 nodes)
- **Average Completion Time**: ~30 prestiges (~3000 levels)
- **Respec Cost**: 500 stars (refund 80% of spent stars)
- **Respec Limit**: Unlimited (encourages experimentation)

---

## 3. Account Leveling

### XP Formula

```python
def xp_required(account_level: int) -> int:
    return 100 * (account_level ** 1.5)
```

**Examples**:
- Level 1 → 2: 100 XP
- Level 2 → 3: 283 XP
- Level 10 → 11: 3,162 XP
- Level 50 → 51: 35,355 XP
- Level 100 → 101: 100,000 XP

### XP Sources

| Source | XP Earned |
|--------|-----------|
| Complete level | `base_xp + (level_number × 2)` |
| First-time completion | `base_xp × 2` |
| 3-star completion | `base_xp × 3` |
| Daily challenge | 500 XP each |
| Prestige | 5,000 XP |
| Boss defeat | 2,000 XP |
| Ascension milestone | 10,000 XP |

### Rewards per Account Level

| Frequency | Reward |
|-----------|--------|
| Every level | 50 coins |
| Every 5 levels | 100 coins + 1 power-up pack |
| Every 10 levels | 200 coins + 5 stars + exclusive avatar |
| Every 25 levels | 500 coins + 20 stars + exclusive skin |
| Every 50 levels | 1,000 coins + 50 stars + legendary power-up |
| Every 100 levels | 5,000 coins + 200 stars + ultimate reward |

### Account Level Benefits

**Permanent Stat Boosts**:
- +1% all stats per account level
- Example: Account level 50 = +50% all stats

**Feature Unlocks**:
- Level 10: Friends system
- Level 25: Guilds / Clans
- Level 50: Ascension mode
- Level 100: Ultimate challenges

**Prestige Efficiency**:
- +5% stars earned per 10 account levels
- Example: Account level 50 = +25% star earn rate

---

## 4. Ascension Mechanics (Endgame)

### Unlock Conditions

- ✅ Account level 50+
- ✅ Prestige level 5+
- ✅ Complete level 200

### Ascension Mechanics

**Infinite Progression**:
- No level cap
- Procedurally generated levels
- Exponential difficulty scaling

**Formula**:
```python
def ascension_difficulty(ascension_level: int) -> float:
    base_difficulty = 1800  # Level 200 difficulty
    return base_difficulty * (2 ** ascension_level)
```

**Examples**:
- Ascension 1: 3,600 difficulty (2× level 200)
- Ascension 5: 57,600 difficulty (32× level 200)
- Ascension 10: 1,843,200 difficulty (1,024× level 200)
- Ascension 20: 1,887,436,800 difficulty (1,048,576× level 200)

### Ascension Bonuses

**Permanent Multipliers**:
- 2× coin earn rate
- 2× XP earn rate
- 1.5× star earn rate (prestige currency)

**Exclusive Power-Ups**:
- **Mega Rainbow**: Clear entire board (3 uses per ascension run)
- **Time Freeze**: Pause timer for 10 seconds (5 uses)
- **Board Nuke**: Destroy all obstacles (2 uses)

**Leaderboard**:
- Global ranking for highest ascension level reached
- Weekly / monthly / all-time leaderboards
- Top 100 players get exclusive rewards

### Ascension Incentives

**Competitive Play**:
- Showcase mastery and dedication
- Compete with top players globally
- Seasonal leaderboard resets

**Infinite Replayability**:
- Always a higher level to reach
- No ceiling on progression
- Perfect for streamers / content creators

**Prestige Acceleration**:
- Ascension bonuses stack with prestige bonuses
- Prestige runs become faster (50% faster at ascension 5)
- Encourages prestige loop (ascend → prestige → ascend higher)

---

## Meta-Progression Summary

| System | Unlock Level | Purpose | Completion Time |
|--------|--------------|---------|-----------------|
| **Prestige** | 100 | Soft reset loop | Infinite (10 prestiges = ~1000 levels) |
| **Skill Tree** | 110 | Player customization | ~3000 levels (30 prestiges) |
| **Account Leveling** | 0 (always active) | Permanent progression | ~5000 levels (account level 100) |
| **Ascension** | 200 | Infinite endgame | Infinite (exponential scaling) |

**Total Meta-Progression Depth**:
- Casual player (no prestige): ~10 hours to level 100
- Mid-core player (10 prestiges): ~50 hours to max prestige bonuses
- Hardcore player (skill tree + ascension): 200+ hours for full completion

---

**Version**: 1.0.0
**Generated**: 2026-01-14
```

---

## Handoffs

### Automatic Handoffs

**On Success** (all quality gates passed):
→ `/speckit.implement`
- Handoff context: progression.md, difficulty-curve.csv, unlock-schedule.md, meta-progression.md
- Implementation tasks: Level generation logic, difficulty scaling, meta-progression systems

### Manual Handoffs

**On Validation Failure**:
→ `/speckit.analyze --profile qa`
- Run full quality analysis to identify root cause
- Review Flow Channel violations, difficulty spikes

**For Virality Integration**:
→ `/speckit.games.virality`
- Use progression milestones for social hooks (prestige rewards, leaderboard)
- Use meta-progression as K-factor multipliers

---

## Cost Estimate

**Per Execution**:
- 7 agents (3 opus @ 24K-32K, 4 sonnet @ 8K-16K)
- Total thinking budget: 120K tokens
- **Cost**: ~$4.80 (opus: $3.60, sonnet: $1.20)

**Genre-Specific Adjustments**:
- Match-3/Puzzle: $4.80 (standard, 200 levels)
- Idle/Runner: $5.40 (infinite levels, more complex formulas)
- Shooter/Arcade: $3.60 (fewer levels, simpler progression)

---

## Workflow Integration

```text
/speckit.games.concept
    ↓
/speckit.games.mechanics
    ↓
/speckit.games.progression ⭐ NEW
    ↓
/speckit.implement
```

**Input Dependencies**:
- REQUIRED: `specs/games/mechanics.md` (from `/speckit.games.mechanics`)
- REQUIRED: `specs/games/concept.md` (from `/speckit.games.concept`)
- OPTIONAL: `specs/games/virality.md` (for social hook integration)

**Output Files**:
- `specs/games/progression.md` — Master progression spec (~30 pages)
- `specs/games/difficulty-curve.csv` — Level data (200+ rows)
- `specs/games/unlock-schedule.md` — Unlock timeline (~5 pages)
- `specs/games/meta-progression.md` — Meta systems (~8 pages)

---

## Troubleshooting

### Issue: Flow Channel Validation Fails (QG-PROGRESSION-002)

**Symptom**: >5% of levels in boredom/anxiety zones

**Diagnosis**:
1. Check skill growth rate vs difficulty growth rate
2. Identify which levels fail (early, mid, late game?)
3. Calculate skill-challenge gap for failed levels

**Fix**:
- If boredom zone: Increase difficulty (reduce moves, add obstacles)
- If anxiety zone: Decrease difficulty (increase moves, reduce obstacles)
- Adjust player skill growth rate (slower = more forgiving)

### Issue: Difficulty Slope Violations (QG-PROGRESSION-001)

**Symptom**: Slope < 0.8 or > 1.2 between adjacent levels

**Diagnosis**:
1. Identify which level pairs violate (e.g., Level 50 → 51)
2. Calculate current slope: `slope = difficulty(51) / difficulty(50)`
3. Check if edge case (prestige milestone, boss level)

**Fix**:
- If slope > 1.2: Add intermediate level or smooth formula
- If slope < 0.8: Remove level or adjust formula to avoid drops
- Add level-specific overrides for milestones (prestige, bosses)

### Issue: Unlock Gate Gaps Too Large (QG-PROGRESSION-004)

**Symptom**: Gaps > 15 levels without new content

**Diagnosis**:
1. Identify gap location (e.g., Level 75 → 90)
2. Check if gap is in late game (acceptable) or mid game (fix)

**Fix**:
- Add intermediate unlock (cosmetic, minor power-up)
- Split large unlock into multiple unlocks (e.g., power-up tiers)
- Adjust unlock cadence for genre (faster for arcade, slower for puzzle)

### Issue: Meta-Progression Depth Mismatch (QG-PROGRESSION-005)

**Symptom**: Missing required meta systems (e.g., deep flag but no ascension)

**Diagnosis**:
1. Check --meta-depth flag value
2. Check which systems are present in meta-progression.md
3. Compare required vs actual

**Fix**:
- Design missing system (prestige, skill tree, account leveling, ascension)
- Or reduce --meta-depth flag to match implemented systems
- Ensure all formulas and mechanics are specified (not placeholders)

---

## Version History

### 1.0.0 (Initial Release)
- 7-agent orchestration across 5 phases
- 5 quality gates (QG-PROGRESSION-001 through 005)
- Genre-specific templates for 7 genres
- 4 output files (progression.md, difficulty-curve.csv, unlock-schedule.md, meta-progression.md)
- Flow Channel validation during design
- Meta-progression depth: basic/standard/deep

---

**Command**: `/speckit.games.progression`
**Version**: 1.0.0
**Model**: opus (thinking_budget: 120000)
**Cost**: ~$4.80 per execution
**Agents**: 7 (3 opus, 4 sonnet)
**Quality Gates**: 5 (QG-PROGRESSION-001..005)
**Output Files**: 4 (progression.md, difficulty-curve.csv, unlock-schedule.md, meta-progression.md)
**Estimated Execution Time**: 12-15 minutes (for 200 levels)

---

**Generated**: 2026-01-14
**Author**: Spec Kit Team
**License**: MIT

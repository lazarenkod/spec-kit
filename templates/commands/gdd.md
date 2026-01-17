---
name: gdd
description: |
  Living Game Design Document (GDD) management for mobile games.
  Creates, validates, and maintains a modular GDD with auto-sync to specs and implementation artifacts.

version: 1.0.0
persona: game-designer-agent
model: opus
thinking_budget: 32000

skills:
  - game-design-patterns
  - core-loop-analysis
  - narrative-design
  - ux-flow-design

inputs:
  game_type:
    type: enum
    options: [casual, mid-core, hardcore, hyper-casual, idle, puzzle, rpg, strategy, simulation]
    required: true
    description: Primary game genre/type
  platform:
    type: enum
    options: [mobile, pc, console, cross-platform]
    default: mobile
    description: Target platform
  monetization:
    type: enum
    options: [f2p, premium, hybrid, subscription]
    default: f2p
    description: Monetization model
  target_audience:
    type: string
    required: true
    description: Target player demographic (e.g., "casual 25-45 women")

flags:
  - name: --thinking-depth
    type: choice
    choices: [quick, standard, thorough, deep, expert, ultrathink]
    default: standard
    description: |
      Research depth and thinking budget per agent:
      - quick: 16K budget, 5 core agents, 90s timeout (~$0.32)
      - standard: 32K budget, 9 agents, 180s timeout (~$1.15) [RECOMMENDED]
      - thorough: 64K budget, 12 agents, 240s timeout (~$2.30)
      - deep: 96K budget, 15 agents, 300s timeout (~$3.46)
      - expert: 120K budget, 18 agents, 360s timeout (~$4.32)
      - ultrathink: 192K budget, 18 agents, 480s timeout (~$6.91) [EXPERT MODE]

outputs:
  - docs/gdd/gdd.md                           # Master GDD document
  - docs/gdd/sections/01-vision.md            # Section 1: Vision & Pillars
  - docs/gdd/sections/02-core-loop.md         # Section 2: Core Loop
  - docs/gdd/sections/03-metagame.md          # Section 3: Meta Game & Progression
  - docs/gdd/sections/04-economy.md           # Section 4: Economy Design
  - docs/gdd/sections/05-monetization.md      # Section 5: Monetization
  - docs/gdd/sections/06-ux-flow.md           # Section 6: UX & Flow
  - docs/gdd/sections/07-art-audio.md         # Section 7: Art & Audio Direction
  - docs/gdd/sections/08-narrative.md         # Section 8: Narrative & Lore
  - docs/gdd/sections/09-social.md            # Section 9: Social Features
  - docs/gdd/sections/10-liveops.md           # Section 10: LiveOps Hooks
  - docs/gdd/gdd-changelog.md                 # Change history
  - docs/gdd/gdd-validation.md                # Validation report

quality_gates:
  - name: QG-GDD-001
    description: Core Loop Completeness
    condition: "Core loop has all 4 phases (action, reward, progression, engagement)"
    threshold: "100% phases defined"
    severity: CRITICAL
  - name: QG-GDD-002
    description: GDD Quality Score (GDDQS)
    condition: "GDDQS >= 70 across all 10 sections"
    threshold: "≥ 70/100"
    severity: HIGH
  - name: QG-GDD-003
    description: Monetization Ethics Check
    condition: "No predatory patterns detected (loot boxes disclosed, no aggressive timers)"
    threshold: "0 violations"
    severity: HIGH
  - name: QG-GDD-004
    description: Platform Guidelines Compliance
    condition: "iOS App Store / Google Play policy compliance"
    threshold: "100% compliant"
    severity: CRITICAL

pre_gates:
  - name: QG-GDD-000
    description: Constitution with game domain exists
    condition: "constitution.md contains game_type setting"
    severity: HIGH

inline_gates:
  enabled: true
  gates:
    - id: IG-GDD-001
      name: Vision Clarity
      check: "Vision statement is 1-2 sentences, clear elevator pitch exists"
      severity: HIGH
    - id: IG-GDD-002
      name: Core Loop Definition
      check: "4-phase loop documented with time estimates"
      severity: CRITICAL
    - id: IG-GDD-003
      name: Economy Validation
      check: "Sinks/sources balance documented"
      severity: HIGH

handoffs:
  - label: Validate Economy
    agent: speckit.balance
    auto: true
    condition:
      - "Section 04-economy.md complete"
      - "Currency types defined"
    gates:
      - name: "QG-ECONOMY-001"
        check: "Gini coefficient < 0.6"
  - label: Create Feature Specs
    agent: speckit.specify
    auto: false
    condition:
      - "GDD approved by stakeholders"
  - label: Create Concept
    agent: speckit.concept
    auto: false
    condition:
      - "GDD is first artifact in project"
    prompt: "Use GDD sections as input for concept generation"
  - label: Setup Analytics
    agent: speckit.analytics
    auto: false
    condition:
      - "Monetization section complete"

claude_code:
  model: opus
  reasoning_mode: extended
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 8000
        max_parallel: 2
      pro:
        thinking_budget: 16000
        max_parallel: 4
      max:
        thinking_budget: 32000
        max_parallel: 8
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
  orchestration:
    max_parallel: 6
    conflict_resolution: queue
    timeout_per_agent: 900000
    retry_on_failure: 3
    role_isolation: true

  subagents:
    # Wave 1: Foundation (parallel)
    - role: vision-architect
      role_group: STRATEGY
      parallel: true
      depends_on: []
      priority: 10
      model_override: opus
      prompt: |
        Create the Vision & Pillars section (01-vision.md).

        Based on inputs (game_type, platform, monetization, target_audience):
        1. Craft compelling 1-2 sentence vision statement
        2. Define 3-5 design pillars (e.g., "Instant Gratification", "Social Competition")
        3. Identify target player psychographics (Bartle types, motivations)
        4. Set success metrics (D1, D7, D30 retention targets)
        5. Define unique selling proposition (USP)

        Reference benchmarks:
        - Supercell: "Minutes to learn, lifetime to master"
        - King: "Accessible fun for everyone"
        - Voodoo: "Instantly fun, endlessly replayable"

        Output: docs/gdd/sections/01-vision.md

    - role: core-loop-designer
      role_group: DESIGN
      parallel: true
      depends_on: []
      priority: 10
      model_override: opus
      prompt: |
        Create the Core Loop section (02-core-loop.md).

        Design a compelling 4-phase core loop:
        1. **ACTION**: What does the player DO? (tap, swipe, build, match)
        2. **REWARD**: What do they GET? (coins, XP, items, progress)
        3. **PROGRESSION**: How do they GROW? (levels, unlocks, power)
        4. **ENGAGEMENT**: What brings them BACK? (daily rewards, events, social)

        Include:
        - Session length targets (hyper-casual: 2-3 min, mid-core: 10-15 min)
        - Loop frequency (sessions per day)
        - Mastery curve (easy → medium → hard)
        - "Aha moment" definition (when player understands the fun)

        Validate against QG-GDD-001: All 4 phases must be complete.

        Output: docs/gdd/sections/02-core-loop.md

    - role: narrative-designer
      role_group: DESIGN
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Create the Narrative & Lore section (08-narrative.md).

        Design narrative framework:
        1. Story premise (1 paragraph)
        2. World setting & tone
        3. Character archetypes (protagonist, antagonist, NPCs)
        4. Story progression tied to gameplay
        5. Dialogue style guide

        For casual games: Light narrative, mascot characters
        For RPGs: Deep lore, branching narratives
        For puzzle: Minimal story, themed content

        Output: docs/gdd/sections/08-narrative.md

    # Wave 2: Mechanics (depends on Wave 1)
    - role: metagame-designer
      role_group: DESIGN
      parallel: true
      depends_on: [core-loop-designer]
      priority: 20
      model_override: opus
      prompt: |
        Create the Meta Game & Progression section (03-metagame.md).

        Build on core loop to design progression systems:
        1. **Horizontal Progression**: Unlocks, collection, variety
        2. **Vertical Progression**: Power increase, stats, upgrades
        3. **Milestone System**: Achievement gates, chapter unlocks
        4. **Prestige/Rebirth**: Long-term engagement hooks

        Define:
        - XP curves (linear vs exponential)
        - Level cap and pacing
        - Unlock gates (soft gates vs hard gates)
        - Collection mechanics (characters, items, achievements)

        Reference: Supercell's Trophy Road, King's Episode System

        Output: docs/gdd/sections/03-metagame.md

    - role: economy-designer
      role_group: DESIGN
      parallel: true
      depends_on: [core-loop-designer]
      priority: 20
      model_override: opus
      prompt: |
        Create the Economy Design section (04-economy.md).

        Design balanced virtual economy:
        1. **Currencies**:
           - Soft currency (gold, coins) - farmable
           - Hard currency (gems, crystals) - limited/purchased
           - Premium currency (season pass, VIP) - subscription

        2. **Sources & Sinks**:
           - Document all earn methods (gameplay, dailies, ads)
           - Document all spend methods (upgrades, gacha, cosmetics)
           - Balance equation: sources ≈ sinks over time

        3. **Pricing Strategy**:
           - F2P earn rates (X gems/day)
           - Whale spend potential ($500+ value packs)
           - Dolphin sweet spot ($10-50/month)

        4. **Time-to-Content**:
           - F2P: Unlock character in X days
           - Payer: Unlock character in Y days

        Reference: Supercell Gini <0.5, King's soft currency balance

        Output: docs/gdd/sections/04-economy.md

    - role: ux-flow-designer
      role_group: DESIGN
      parallel: true
      depends_on: [core-loop-designer]
      priority: 20
      model_override: sonnet
      prompt: |
        Create the UX & Flow section (06-ux-flow.md).

        Design user experience flows:
        1. **FTUE (First Time User Experience)**:
           - Onboarding steps (max 3-5 screens)
           - Tutorial pacing (show, don't tell)
           - First win moment (within 30 seconds)

        2. **Main Menu Architecture**:
           - Hub structure (1 tap to core gameplay)
           - Navigation patterns
           - UI hierarchy (primary, secondary, tertiary)

        3. **Session Flow**:
           - Pre-session (load, dailies check)
           - In-session (core loop)
           - Post-session (rewards, next hook)

        4. **Friction Points**:
           - Identify potential drop-off points
           - Mitigation strategies

        Include wireframe descriptions for key screens.

        Output: docs/gdd/sections/06-ux-flow.md

    # Wave 3: Monetization & Social (depends on Wave 2)
    - role: monetization-designer
      role_group: STRATEGY
      parallel: true
      depends_on: [economy-designer]
      priority: 30
      model_override: opus
      prompt: |
        Create the Monetization section (05-monetization.md).

        Design ethical monetization strategy:
        1. **IAP Strategy**:
           - Starter pack ($0.99-4.99)
           - Value packs (best $/gem ratio)
           - Whale packs ($99.99+)
           - Battle Pass ($9.99/month)

        2. **Ad Strategy** (if applicable):
           - Rewarded video placements
           - Interstitial frequency caps
           - Ad-free option

        3. **Subscription Options**:
           - VIP tiers and benefits
           - Pricing psychology

        4. **Ethical Constraints**:
           - Loot box odds disclosure (Apple/Google policy)
           - No FOMO exploitation
           - Spending limits/warnings
           - No pay-to-win in competitive modes

        Validate against QG-GDD-003: Zero predatory patterns.

        Reference benchmarks:
        - Supercell ARPDAU: $0.15-0.30
        - King ARPDAU: $0.08-0.12
        - Voodoo ARPDAU: $0.03-0.06 (ad-based)

        Output: docs/gdd/sections/05-monetization.md

    - role: social-designer
      role_group: DESIGN
      parallel: true
      depends_on: [metagame-designer]
      priority: 30
      model_override: sonnet
      prompt: |
        Create the Social Features section (09-social.md).

        Design social engagement systems:
        1. **Async Social**:
           - Leaderboards (global, friends, local)
           - Sharing (replays, achievements)
           - Gifting system

        2. **Sync Social** (if applicable):
           - Real-time PvP matchmaking
           - Co-op modes
           - Clan/Guild systems

        3. **Viral Mechanics**:
           - Invite rewards (k-factor boost)
           - Social media integration
           - User-generated content

        4. **Community Features**:
           - In-game chat
           - Friend system
           - Player profiles

        Output: docs/gdd/sections/09-social.md

    - role: art-audio-director
      role_group: CREATIVE
      parallel: true
      depends_on: [vision-architect]
      priority: 30
      model_override: sonnet
      prompt: |
        Create the Art & Audio Direction section (07-art-audio.md).

        Define visual and audio identity:
        1. **Art Style**:
           - Visual style (2D/3D, cartoon/realistic)
           - Color palette (primary, secondary, accent)
           - Character design guidelines
           - Environment art direction

        2. **UI Design Language**:
           - Button styles
           - Typography
           - Iconography
           - Animation principles

        3. **Audio Design**:
           - Music style and mood
           - SFX categories (UI, gameplay, feedback)
           - Voice acting (if any)
           - Dynamic audio triggers

        4. **Technical Specs**:
           - Asset resolution targets
           - Memory budget per screen
           - Compression guidelines

        Output: docs/gdd/sections/07-art-audio.md

    # Wave 4: LiveOps & Validation (depends on Wave 3)
    - role: liveops-planner
      role_group: OPERATIONS
      parallel: true
      depends_on: [economy-designer, monetization-designer]
      priority: 40
      model_override: sonnet
      prompt: |
        Create the LiveOps Hooks section (10-liveops.md).

        Design live operations framework:
        1. **Event System**:
           - Event types (limited time, seasonal, collaboration)
           - Event cadence (weekly mini, monthly major)
           - Event templates (challenge, collection, tournament)

        2. **Content Calendar Hooks**:
           - Where new content slots in
           - Update frequency targets
           - A/B testing points

        3. **Remote Config Points**:
           - Tunable parameters (economy, difficulty, timers)
           - Feature flags
           - Segmentation variables

        4. **Retention Mechanics**:
           - Daily login rewards
           - Streak bonuses
           - Comeback campaigns

        Output: docs/gdd/sections/10-liveops.md

    - role: gdd-validator
      role_group: QA
      parallel: true
      depends_on: [vision-architect, core-loop-designer, economy-designer, monetization-designer]
      priority: 50
      model_override: opus
      prompt: |
        Validate complete GDD and generate reports.

        1. **Assemble Master GDD** (docs/gdd/gdd.md):
           - Create table of contents
           - Link all 10 sections
           - Add version control header

        2. **Calculate GDDQS (GDD Quality Score)**:
           Score each section (0-10):
           - Vision: Clarity, differentiation, market fit
           - Core Loop: Completeness, timing, engagement
           - Metagame: Depth, pacing, replayability
           - Economy: Balance, sinks/sources, fairness
           - Monetization: Ethics, value, conversion
           - UX: Accessibility, flow, friction
           - Art/Audio: Consistency, quality, identity
           - Narrative: Coherence, engagement, integration
           - Social: Virality, engagement, retention
           - LiveOps: Flexibility, scalability, hooks

           GDDQS = sum(section_scores) * 10 / 100

        3. **Validate Quality Gates**:
           - QG-GDD-001: Core Loop complete
           - QG-GDD-002: GDDQS >= 70
           - QG-GDD-003: Ethics check
           - QG-GDD-004: Platform compliance

        4. **Generate Validation Report** (docs/gdd/gdd-validation.md)

        5. **Create Changelog** (docs/gdd/gdd-changelog.md)

flags:
  skip_validation: "--skip-validation"           # Skip QG validation (not recommended)
  section: "--section <name>"                    # Generate specific section only
  update: "--update"                             # Update existing GDD (preserve unchanged sections)
  export_unity: "--export-unity"                 # Export to Unity ScriptableObjects format
  export_unreal: "--export-unreal"               # Export to Unreal Data Assets format
  strict: "--strict"                             # Treat HIGH severity as CRITICAL
  max_model: "--max-model <opus|sonnet|haiku>"   # Override model cap
---

# /speckit.gdd - Living Game Design Document

## Purpose

The `/speckit.gdd` command creates and maintains a comprehensive, modular Game Design Document (GDD) for mobile game development. Unlike traditional static GDDs that become outdated, this creates a "living document" that:

1. **Auto-syncs** with spec and implementation artifacts
2. **Validates** design decisions against quality gates
3. **Integrates** with Unity/Unreal via export formats
4. **Evolves** with version tracking and change history

## When to Use

- **Project Start**: Create foundational GDD before any development
- **Pivot/Redesign**: Update GDD when changing game direction
- **Pre-Production**: Finalize GDD before production begins
- **Feature Planning**: Reference GDD when creating feature specs

## User Input

$ARGUMENTS

Parse arguments:
- `--skip-validation`: Skip quality gate validation (not recommended for production)
- `--section <name>`: Generate or update specific section only (vision, core-loop, economy, etc.)
- `--update`: Update existing GDD, preserving unchanged sections
- `--export-unity`: Export to Unity ScriptableObjects format
- `--export-unreal`: Export to Unreal Data Assets format
- `--strict`: Treat HIGH severity gates as CRITICAL (blocking)
- `--max-model <model>`: Override model cap

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        /speckit.gdd                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WAVE 1: Foundation (parallel)                                  │
│  ├── Vision Architect → 01-vision.md                            │
│  ├── Core Loop Designer → 02-core-loop.md                       │
│  └── Narrative Designer → 08-narrative.md                       │
│                                                                  │
│  WAVE 2: Mechanics (parallel)                                   │
│  ├── Metagame Designer → 03-metagame.md                         │
│  ├── Economy Designer → 04-economy.md                           │
│  └── UX Flow Designer → 06-ux-flow.md                           │
│                                                                  │
│  WAVE 3: Monetization & Social (parallel)                       │
│  ├── Monetization Designer → 05-monetization.md                 │
│  ├── Social Designer → 09-social.md                             │
│  └── Art/Audio Director → 07-art-audio.md                       │
│                                                                  │
│  WAVE 4: LiveOps & Validation                                   │
│  ├── LiveOps Planner → 10-liveops.md                            │
│  └── GDD Validator → gdd.md, gdd-validation.md                  │
│                                                                  │
│  HANDOFFS:                                                      │
│  ├── Economy complete → /speckit.balance                        │
│  ├── GDD approved → /speckit.specify                            │
│  └── Monetization ready → /speckit.analytics                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Execution Steps

### Step 0: Load Project Context

```text
READ /memory/constitution.md:
  EXTRACT: game_type, platform, language

IF game_type NOT in constitution:
  PROMPT user for game_type, monetization, target_audience

SET ARTIFACT_LANGUAGE from constitution (default: "en")
```

### Step 1: Generate GDD Sections

Execute 4 waves of parallel agent generation as defined in `subagents` section.

**Wave 1 (Foundation)**:
- 01-vision.md: Vision & Design Pillars
- 02-core-loop.md: Core Loop Definition
- 08-narrative.md: Narrative & Lore

**Wave 2 (Mechanics)**:
- 03-metagame.md: Meta Game & Progression
- 04-economy.md: Economy Design
- 06-ux-flow.md: UX & Flow

**Wave 3 (Monetization & Social)**:
- 05-monetization.md: Monetization Strategy
- 09-social.md: Social Features
- 07-art-audio.md: Art & Audio Direction

**Wave 4 (LiveOps & Validation)**:
- 10-liveops.md: LiveOps Hooks
- gdd.md: Master Document Assembly
- gdd-validation.md: Validation Report

### Step 2: Validate Quality Gates

```text
VALIDATE QG-GDD-001 (Core Loop Completeness):
  CHECK: 02-core-loop.md contains all 4 phases
  - [ ] ACTION phase defined
  - [ ] REWARD phase defined
  - [ ] PROGRESSION phase defined
  - [ ] ENGAGEMENT phase defined

  IF any phase missing:
    STATUS = FAIL
    BLOCK handoffs

VALIDATE QG-GDD-002 (GDD Quality Score):
  CALCULATE GDDQS from 10 section scores

  IF GDDQS < 70:
    STATUS = FAIL
    GENERATE improvement recommendations

VALIDATE QG-GDD-003 (Monetization Ethics):
  SCAN 05-monetization.md for patterns:
  - [ ] Loot box odds disclosed
  - [ ] No aggressive countdown timers
  - [ ] Spending limits mentioned
  - [ ] No pay-to-win in PvP

  IF violations found:
    STATUS = FAIL
    LIST violations with severity

VALIDATE QG-GDD-004 (Platform Compliance):
  CHECK against iOS App Store Guidelines:
  - 3.1.1: In-App Purchase requirements
  - 3.1.2: Subscriptions disclosure

  CHECK against Google Play Policy:
  - Real-money gambling disclosure
  - Loot box odds requirements
```

### Step 3: Generate Master GDD

Assemble `docs/gdd/gdd.md`:

```markdown
# Game Design Document: {{GAME_NAME}}

**Version**: {{VERSION}}
**Last Updated**: {{DATE}}
**GDDQS**: {{SCORE}}/100

## Table of Contents

1. [Vision & Pillars](./sections/01-vision.md)
2. [Core Loop](./sections/02-core-loop.md)
3. [Meta Game & Progression](./sections/03-metagame.md)
4. [Economy Design](./sections/04-economy.md)
5. [Monetization](./sections/05-monetization.md)
6. [UX & Flow](./sections/06-ux-flow.md)
7. [Art & Audio Direction](./sections/07-art-audio.md)
8. [Narrative & Lore](./sections/08-narrative.md)
9. [Social Features](./sections/09-social.md)
10. [LiveOps Hooks](./sections/10-liveops.md)

## Quick Reference

| Attribute | Value |
|-----------|-------|
| **Game Type** | {{GAME_TYPE}} |
| **Platform** | {{PLATFORM}} |
| **Monetization** | {{MONETIZATION}} |
| **Target Audience** | {{TARGET_AUDIENCE}} |
| **Session Length** | {{SESSION_LENGTH}} |
| **Core Loop Time** | {{LOOP_TIME}} |

## Validation Status

| Gate | Status | Notes |
|------|--------|-------|
| QG-GDD-001 | {{STATUS}} | Core Loop Complete |
| QG-GDD-002 | {{STATUS}} | GDDQS {{SCORE}}/100 |
| QG-GDD-003 | {{STATUS}} | Ethics Check |
| QG-GDD-004 | {{STATUS}} | Platform Compliance |
```

## Output Artifacts

### Section Templates

#### 01-vision.md Template

```markdown
# Vision & Design Pillars

## Vision Statement

{{VISION_STATEMENT}}

## Elevator Pitch

{{ELEVATOR_PITCH}}

## Design Pillars

### Pillar 1: {{PILLAR_NAME}}
{{PILLAR_DESCRIPTION}}

### Pillar 2: {{PILLAR_NAME}}
{{PILLAR_DESCRIPTION}}

### Pillar 3: {{PILLAR_NAME}}
{{PILLAR_DESCRIPTION}}

## Target Player

### Demographics
- **Age Range**: {{AGE_RANGE}}
- **Gender Split**: {{GENDER_SPLIT}}
- **Regions**: {{REGIONS}}

### Psychographics (Bartle Types)
- **Primary**: {{PRIMARY_TYPE}} ({{PERCENTAGE}}%)
- **Secondary**: {{SECONDARY_TYPE}} ({{PERCENTAGE}}%)

### Player Motivations
1. {{MOTIVATION_1}}
2. {{MOTIVATION_2}}
3. {{MOTIVATION_3}}

## Success Metrics

| Metric | Target | Benchmark |
|--------|--------|-----------|
| D1 Retention | {{TARGET}}% | Supercell: 40% |
| D7 Retention | {{TARGET}}% | Supercell: 20% |
| D30 Retention | {{TARGET}}% | Supercell: 10% |
| Avg Session | {{TARGET}} min | - |
| Sessions/Day | {{TARGET}} | - |

## Unique Selling Proposition (USP)

{{USP_STATEMENT}}

## Competitive Positioning

| Competitor | Our Advantage |
|------------|---------------|
| {{COMPETITOR_1}} | {{ADVANTAGE}} |
| {{COMPETITOR_2}} | {{ADVANTAGE}} |
```

#### 02-core-loop.md Template

```markdown
# Core Loop

## Loop Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     CORE GAMEPLAY LOOP                       │
│                                                              │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   │  ACTION  │───▶│  REWARD  │───▶│PROGRESSION│───▶│ENGAGEMENT│
│   │          │    │          │    │          │    │          │
│   │ {{ACT}}  │    │ {{REW}}  │    │ {{PROG}} │    │ {{ENG}}  │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘
│        ▲                                               │
│        └───────────────────────────────────────────────┘
│                                                              │
│   Loop Time: {{LOOP_TIME}}                                   │
│   Session Target: {{SESSION_LENGTH}}                         │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: ACTION

**What the player DOES**:
- Primary mechanic: {{PRIMARY_MECHANIC}}
- Input method: {{INPUT_METHOD}}
- Skill expression: {{SKILL_TYPE}}

**Example Flow**:
1. {{ACTION_STEP_1}}
2. {{ACTION_STEP_2}}
3. {{ACTION_STEP_3}}

**Time**: {{ACTION_TIME}} seconds

## Phase 2: REWARD

**What the player GETS**:
- Primary reward: {{PRIMARY_REWARD}}
- Secondary reward: {{SECONDARY_REWARD}}
- Feedback type: {{FEEDBACK_TYPE}}

**Reward Schedule**:
| Outcome | Reward | Frequency |
|---------|--------|-----------|
| Win | {{REWARD}} | {{FREQ}} |
| Partial | {{REWARD}} | {{FREQ}} |
| Lose | {{REWARD}} | {{FREQ}} |

## Phase 3: PROGRESSION

**How the player GROWS**:
- XP system: {{XP_DESCRIPTION}}
- Unlock cadence: {{UNLOCK_CADENCE}}
- Power curve: {{POWER_CURVE}}

**Milestone Map**:
| Milestone | Unlock | Time to Reach |
|-----------|--------|---------------|
| Level 5 | {{UNLOCK}} | {{TIME}} |
| Level 10 | {{UNLOCK}} | {{TIME}} |
| Level 20 | {{UNLOCK}} | {{TIME}} |

## Phase 4: ENGAGEMENT

**What brings them BACK**:
- Daily hook: {{DAILY_HOOK}}
- Weekly hook: {{WEEKLY_HOOK}}
- Social hook: {{SOCIAL_HOOK}}

**Engagement Triggers**:
1. {{TRIGGER_1}}
2. {{TRIGGER_2}}
3. {{TRIGGER_3}}

## Session Structure

**Pre-Session** (30 sec):
- {{PRE_SESSION_ACTIVITY}}

**In-Session** ({{SESSION_LENGTH}}):
- {{IN_SESSION_ACTIVITIES}}

**Post-Session** (15 sec):
- {{POST_SESSION_ACTIVITY}}

## "Aha Moment"

**Definition**: The moment when the player understands why the game is fun.

**Target Time**: Within {{AHA_TIME}} of first play

**Trigger**: {{AHA_TRIGGER}}

## Mastery Curve

```
Skill
  ▲
  │                    ┌─ Mastery
  │               ┌────┘
  │          ┌────┘
  │     ┌────┘
  │ ────┘
  └──────────────────────────────▶ Time
      Easy    Medium    Hard
```

**Pacing**:
- Easy phase: {{EASY_DURATION}}
- Medium phase: {{MEDIUM_DURATION}}
- Hard phase: {{HARD_DURATION}}
```

## Unity/Unreal Export

### Unity ScriptableObject Export

```csharp
// Auto-generated from GDD
[CreateAssetMenu(fileName = "GameDesignConfig", menuName = "GDD/GameDesignConfig")]
public class GameDesignConfig : ScriptableObject
{
    [Header("Vision")]
    public string visionStatement = "{{VISION_STATEMENT}}";
    public string[] designPillars = { {{PILLARS}} };

    [Header("Core Loop")]
    public float loopTimeSeconds = {{LOOP_TIME}};
    public float targetSessionMinutes = {{SESSION_LENGTH}};

    [Header("Economy")]
    public int softCurrencyEarnRate = {{SOFT_EARN}};
    public int hardCurrencyEarnRate = {{HARD_EARN}};

    [Header("Retention")]
    public float targetD1 = {{D1_TARGET}};
    public float targetD7 = {{D7_TARGET}};
    public float targetD30 = {{D30_TARGET}};
}
```

### Unreal Data Asset Export

```cpp
// Auto-generated from GDD
UCLASS(BlueprintType)
class UGameDesignConfig : public UDataAsset
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Vision")
    FString VisionStatement = TEXT("{{VISION_STATEMENT}}");

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Core Loop")
    float LoopTimeSeconds = {{LOOP_TIME}};

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Economy")
    int32 SoftCurrencyEarnRate = {{SOFT_EARN}};
};
```

## GDD Quality Score (GDDQS) Calculation

| Section | Weight | Score | Weighted |
|---------|--------|-------|----------|
| Vision | 10% | /10 | |
| Core Loop | 15% | /10 | |
| Metagame | 10% | /10 | |
| Economy | 15% | /10 | |
| Monetization | 10% | /10 | |
| UX/Flow | 10% | /10 | |
| Art/Audio | 10% | /10 | |
| Narrative | 5% | /10 | |
| Social | 10% | /10 | |
| LiveOps | 5% | /10 | |
| **Total** | 100% | | /100 |

**Thresholds**:
- **≥ 85**: Production Ready
- **70-84**: Ready with minor polish
- **50-69**: Needs iteration
- **< 50**: Major rework required

## Industry Benchmarks

### Retention Targets

| Tier | D1 | D7 | D30 |
|------|----|----|-----|
| **Supercell** | 40%+ | 20%+ | 10%+ |
| **King** | 35%+ | 15%+ | 8%+ |
| **Good** | 30%+ | 12%+ | 5%+ |
| **Average** | 25% | 8% | 3% |

### Monetization Benchmarks

| Tier | ARPDAU | LTV | Conversion |
|------|--------|-----|------------|
| **Supercell** | $0.20+ | $5+ | 5%+ |
| **King** | $0.10 | $2-3 | 3-4% |
| **Voodoo** | $0.04 | $0.50 | Ad-based |

### Session Metrics

| Genre | Session Length | Sessions/Day |
|-------|----------------|--------------|
| Hyper-Casual | 2-3 min | 5-8 |
| Casual | 5-10 min | 3-5 |
| Mid-Core | 10-20 min | 2-4 |
| Hardcore | 20-60 min | 1-3 |

## Integration Points

| Command | Integration |
|---------|-------------|
| `/speckit.concept` | Uses GDD as input for market validation |
| `/speckit.specify` | Creates feature specs from GDD sections |
| `/speckit.balance` | Validates economy from Section 04 |
| `/speckit.analytics` | Sets up KPIs from vision metrics |
| `/speckit.playtest` | References UX flow for test scenarios |

## Example Output

```
/speckit.gdd --game_type=casual --monetization=f2p --target_audience="casual women 25-45"

✅ Loading project context from constitution.md
✅ Wave 1: Generating foundation sections...
   ├── 01-vision.md (Vision Architect)
   ├── 02-core-loop.md (Core Loop Designer)
   └── 08-narrative.md (Narrative Designer)

✅ Wave 2: Generating mechanics sections...
   ├── 03-metagame.md (Metagame Designer)
   ├── 04-economy.md (Economy Designer)
   └── 06-ux-flow.md (UX Flow Designer)

✅ Wave 3: Generating monetization & social...
   ├── 05-monetization.md (Monetization Designer)
   ├── 07-art-audio.md (Art/Audio Director)
   └── 09-social.md (Social Designer)

✅ Wave 4: LiveOps & validation...
   ├── 10-liveops.md (LiveOps Planner)
   └── Assembling master GDD...

📊 GDD Quality Score: 82/100

✅ Quality Gate Results:
   ├── QG-GDD-001: PASS (Core loop complete)
   ├── QG-GDD-002: PASS (GDDQS 82 ≥ 70)
   ├── QG-GDD-003: PASS (Ethics check passed)
   └── QG-GDD-004: PASS (Platform compliant)

📁 Generated Artifacts:
   ├── docs/gdd/gdd.md (Master document)
   ├── docs/gdd/sections/*.md (10 sections)
   ├── docs/gdd/gdd-validation.md
   └── docs/gdd/gdd-changelog.md

🔗 Recommended Handoffs:
   → /speckit.balance (Economy validation)
   → /speckit.specify (Feature specs)
```

# /speckit.liveops

```yaml
id: speckit.liveops
version: 1.0.0
persona: liveops-manager-agent
model: opus
thinking_budget: 80000

description: |
  Live Operations Planning for mobile games. Generates content calendars,
  seasonal event schedules, remote config strategies, and LiveOps playbooks.
  Integrates with Firebase Remote Config, PlayFab, and Unity Gaming Services.

skills:
  - liveops-planning
  - content-calendar
  - event-design
  - remote-config
  - ab-testing-strategy

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
  - name: --max-model
    type: string
    default: null
    description: "--max-model <opus|sonnet|haiku> - Override model cap"

inputs:
  required:
    - memory/gdd.md         # Game Design Document (Core Loop, Economy)
    - memory/analytics.md   # Analytics setup with KPI definitions
  optional:
    - memory/softlaunch-report.md  # Post-softlaunch metrics
    - memory/balance-report.md     # Economy simulation results
    - memory/content-backlog.md    # Existing content ideas

outputs:
  primary:
    - memory/liveops-calendar.md   # 12-week content calendar
    - memory/liveops-playbook.md   # Standard operating procedures
    - memory/event-templates.md    # Reusable event blueprints
  secondary:
    - memory/remote-config.json    # Config schema export
    - memory/ab-test-plan.md       # A/B testing roadmap

quality_gates:
  - id: QG-LIVEOPS-001
    name: Content Velocity
    threshold: "≥2 events/week minimum"
    severity: HIGH
    description: "Sufficient content to maintain engagement"

  - id: QG-LIVEOPS-002
    name: Revenue Event Coverage
    threshold: "≥1 monetization event/week"
    severity: CRITICAL
    description: "Consistent revenue touchpoints"

  - id: QG-LIVEOPS-003
    name: Event Lead Time
    threshold: "≥14 days before go-live"
    severity: HIGH
    description: "Adequate preparation time for QA and localization"

  - id: QG-LIVEOPS-004
    name: Remote Config Rollback
    threshold: "100% configs have fallback values"
    severity: CRITICAL
    description: "All remote configs must be safe to disable"

  - id: QG-LIVEOPS-005
    name: Calendar Coverage
    threshold: "≥12 weeks planned"
    severity: HIGH
    description: "Minimum planning horizon for stability"

pre_gates:
  - id: PG-LIVEOPS-001
    check: "GDD exists with Core Loop and Economy defined"
    source: memory/gdd.md

  - id: PG-LIVEOPS-002
    check: "Analytics SDK integrated with event tracking"
    source: memory/analytics.md

inline_gates:
  - id: IG-LIVEOPS-001
    phase: event_design
    check: "Each event has clear success metrics"
    severity: HIGH

  - id: IG-LIVEOPS-002
    phase: calendar
    check: "No content gaps >3 days"
    severity: MEDIUM

  - id: IG-LIVEOPS-003
    phase: remote_config
    check: "All configs have default values"
    severity: CRITICAL

handoffs:
  - command: /speckit.analytics
    condition: "Analytics not configured"
    context: "Set up analytics before LiveOps planning"

  - command: /speckit.softlaunch
    condition: "Ready for regional testing"
    context: "Test LiveOps in soft launch markets"

  - command: /speckit.implement
    condition: "LiveOps features need implementation"
    context: "Implement event systems and remote config"

claude_code:
  model: opus
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: standard
    tiers:
      quick:
        thinking_budget: 16000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
        timeout_per_agent: 180000
        retry_on_failure: 1
      standard:
        thinking_budget: 32000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
        timeout_per_agent: 300000
        retry_on_failure: 2
      thorough:
        thinking_budget: 64000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
        timeout_per_agent: 600000
        retry_on_failure: 3
      deep:
        thinking_budget: 96000
        max_parallel: 6
        batch_delay: 2000
        wave_overlap_threshold: 0.60
        timeout_per_agent: 900000
        retry_on_failure: 3
      expert:
        thinking_budget: 120000
        max_parallel: 4
        batch_delay: 2500
        wave_overlap_threshold: 0.60
        timeout_per_agent: 1200000
        retry_on_failure: 3
      ultrathink:
        thinking_budget: 192000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        timeout_per_agent: 1500000
        retry_on_failure: 3
        cost_multiplier: 6.0  depth_defaults:
    quick:
      thinking_budget: 16000
      skip_agents: [optional-pattern-researchers]
      timeout: 90
    standard:
      thinking_budget: 32000
      skip_agents: []
      timeout: 180
    thorough:
      thinking_budget: 64000
      skip_agents: []
      timeout: 240
    deep:
      thinking_budget: 96000
      additional_agents: [liveops-deepdive]
      timeout: 300
    expert:
      thinking_budget: 120000
      additional_agents: [liveops-deepdive, monetization-auditor]
      timeout: 360
    ultrathink:
      thinking_budget: 192000
      additional_agents: [liveops-deepdive, monetization-auditor, retention-optimizer]
      timeout: 480
  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "expert"
        fallback_thinking: 120000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (192K thinking budget).
          Auto-downgrading to **Expert** mode (120K budget).
      - condition: "user_tier != 'max' AND requested_depth in ['expert', 'deep']"
        fallback_depth: "thorough"
        fallback_thinking: 64000
        warning_message: |
          ⚠️ **Expert/Deep mode requires Claude Code Max tier**.
          Auto-downgrading to **Thorough** mode (64K budget).
  cost_breakdown:
    quick: {cost: $0.32, time: "90-120s"}
    standard: {cost: $1.15, time: "180-240s"}
    thorough: {cost: $2.30, time: "240-300s"}
    deep: {cost: $3.46, time: "300-360s"}
    expert: {cost: $4.32, time: "360-420s"}
    ultrathink: {cost: $6.91, time: "480-540s"}
  cache_control:
    system_prompt: ephemeral
    constitution: ephemeral
    templates: ephemeral
    artifacts: ephemeral
    ttl: session
  cache_hierarchy: full
  orchestration:
    max_parallel: 8
    role_isolation: false
  operation_batching:
    enabled: true
    skip_flag: "--sequential"
    framework: templates/shared/operation-batching.md
  subagents:
    wave_1_analysis:
      parallel: true
      agents:
        - name: liveops-auditor
          task: "Analyze existing content and identify gaps"
          model: sonnet

        - name: calendar-researcher
          task: "Research seasonal opportunities and competitor cadence"
          model: sonnet

        - name: economy-analyst
          task: "Map economy sinks/faucets to event opportunities"
          model: sonnet

    wave_2_planning:
      parallel: true
      depends_on: wave_1_analysis
      agents:
        - name: calendar-planner
          task: "Generate 12-week content calendar"
          model: opus

        - name: event-designer
          task: "Design event templates and blueprints"
          model: opus

        - name: config-architect
          task: "Design remote config schema"
          model: sonnet

    wave_3_validation:
      parallel: true
      depends_on: wave_2_planning
      agents:
        - name: liveops-validator
          task: "Validate calendar and quality gates"
          model: sonnet

        - name: ab-test-planner
          task: "Create A/B testing roadmap"
          model: sonnet
```

---

## Overview

`/speckit.liveops` creates comprehensive Live Operations plans for mobile games, ensuring consistent content delivery, revenue optimization, and player engagement. The command generates:

1. **12-Week Content Calendar** - Detailed schedule of events, updates, and promotions
2. **LiveOps Playbook** - Standard operating procedures for event execution
3. **Event Templates** - Reusable blueprints for common event types
4. **Remote Config Schema** - Feature flag and config architecture
5. **A/B Testing Roadmap** - Experimentation plan for optimization

### Why LiveOps Matters

| Metric | Games with Strong LiveOps | Games without |
|--------|---------------------------|---------------|
| D30 Retention | +15-25% | Baseline |
| Monthly Revenue | +30-50% | Baseline |
| Player LTV | 2-3x | 1x |
| Content Engagement | 60-80% | 20-40% |

**Industry Benchmarks (Top Performers):**
- Supercell: 3-4 events/week, 48-hour event cadence
- King: Daily challenges, weekly tournaments
- Mihoyo: 6-week update cycles, limited-time banners
- Voodoo: A/B test everything, 2-week iteration cycles

---

## Inputs

### Required Inputs

#### 1. Game Design Document (`memory/gdd.md`)

```markdown
## Required Sections for LiveOps Planning

### Core Loop
- Primary engagement mechanics
- Session structure
- Progression systems

### Economy Design
- Currency types and exchange rates
- Sink/faucet balance
- Monetization touchpoints

### Metagame Systems
- Collections and achievements
- Social features
- Competitive modes
```

#### 2. Analytics Setup (`memory/analytics.md`)

```markdown
## Required Analytics Events

### Engagement Events
- session_start, session_end
- level_complete, level_fail
- feature_interaction

### Economy Events
- currency_earn, currency_spend
- purchase_complete
- reward_claim

### LiveOps Events
- event_start, event_complete
- banner_view, banner_click
- offer_view, offer_purchase
```

### Optional Inputs

| Input | Purpose |
|-------|---------|
| `memory/softlaunch-report.md` | Real player behavior data |
| `memory/balance-report.md` | Economy constraints |
| `memory/content-backlog.md` | Existing content ideas |

---

## Process

### Phase 1: LiveOps Audit & Research

**Duration: 15-20 minutes**

#### 1.1 Current State Analysis

```markdown
## LiveOps Audit Checklist

### Content Inventory
- [ ] Existing events and their performance
- [ ] Content pipeline status
- [ ] Asset availability

### Technical Capabilities
- [ ] Remote config integration
- [ ] Event system implementation
- [ ] A/B testing infrastructure

### Team Capacity
- [ ] Content production rate
- [ ] QA turnaround time
- [ ] Localization lead time
```

#### 1.2 Competitive Cadence Research

```markdown
## Competitor LiveOps Analysis

### Direct Competitors
| Competitor | Event Frequency | Event Types | Avg Duration |
|------------|-----------------|-------------|--------------|
| [Name] | X/week | [Types] | [Days] |

### Genre Leaders
| Game | Key LiveOps Features | Success Metrics |
|------|----------------------|-----------------|
| [Game] | [Features] | [Metrics] |
```

#### 1.3 Seasonal Opportunity Mapping

```markdown
## Annual Event Calendar Framework

### Tier 1 Events (Major - 7+ days)
- New Year (Dec 31 - Jan 7)
- Lunar New Year (varies)
- Valentine's Day (Feb 7-14)
- Easter (varies)
- Summer Event (June-July)
- Halloween (Oct 24-31)
- Black Friday (Nov 22-29)
- Christmas (Dec 18-25)

### Tier 2 Events (Medium - 3-5 days)
- St. Patrick's Day
- April Fools
- Mother's/Father's Day
- Back to School
- Thanksgiving

### Tier 3 Events (Mini - 1-2 days)
- International Days
- Game Anniversary
- Milestone Celebrations
- Flash Sales
```

---

### Phase 2: Content Calendar Design

**Duration: 25-35 minutes**

#### 2.1 Calendar Structure

```markdown
## 12-Week Content Calendar

### Week [N]: [Theme/Focus]

#### Events
| Day | Event Name | Type | Duration | Revenue Goal |
|-----|------------|------|----------|--------------|
| Mon | [Event] | [Type] | [Hours] | [Goal] |

#### Content Releases
- [ ] New [content type]: [name]
- [ ] [Feature] update
- [ ] Bug fixes

#### A/B Tests
- [ ] Test [variation] for [metric]

#### Communications
- [ ] Push notification: [message]
- [ ] In-game news: [topic]
- [ ] Social post: [content]
```

#### 2.2 Event Type Definitions

```yaml
event_types:
  challenge_event:
    description: "Time-limited goals with rewards"
    duration: "24-72 hours"
    reward_budget: "2-3x daily earn rate"
    engagement_target: "40-60% DAU participation"
    example: "Weekend Challenge - Collect 100 gems"

  tournament:
    description: "Competitive leaderboard event"
    duration: "3-7 days"
    reward_budget: "5-10x for top tier"
    engagement_target: "20-30% DAU participation"
    example: "Weekly Tournament - High Score Competition"

  collection_event:
    description: "Collect items for milestone rewards"
    duration: "7-14 days"
    reward_budget: "Progressive, 10x for completion"
    engagement_target: "30-50% DAU start, 10-20% complete"
    example: "Spring Collection - Gather 50 flowers"

  sale_event:
    description: "Discounted IAP offers"
    duration: "24-48 hours"
    discount_range: "30-70% off"
    conversion_target: "2-5x normal purchase rate"
    example: "Flash Sale - 50% off gem packs"

  season_pass:
    description: "Multi-week progression with premium track"
    duration: "4-8 weeks"
    free_vs_paid: "60% free, 40% paid rewards"
    attach_rate_target: "5-15% of active players"
    example: "Battle Pass Season 1"

  limited_content:
    description: "Exclusive time-limited content"
    duration: "7-14 days"
    fomo_factor: "Content not returning for 6+ months"
    engagement_target: "50-70% DAU interaction"
    example: "Halloween Exclusive Skin Pack"
```

#### 2.3 Content Velocity Requirements

```markdown
## Minimum Content Cadence by Genre

### Casual Games (Puzzle, Match-3)
| Content Type | Frequency | Lead Time |
|--------------|-----------|-----------|
| New Levels | Weekly (20-50 levels) | 2 weeks |
| Events | 2-3/week | 1 week |
| Seasonal Theme | 4-6/year | 4 weeks |
| New Mechanics | Monthly | 6 weeks |

### Mid-Core Games (Strategy, RPG)
| Content Type | Frequency | Lead Time |
|--------------|-----------|-----------|
| New Units/Characters | Bi-weekly | 4 weeks |
| Events | 3-4/week | 2 weeks |
| Raids/Dungeons | Monthly | 6 weeks |
| Story Updates | Bi-monthly | 8 weeks |

### Hyper-Casual
| Content Type | Frequency | Lead Time |
|--------------|-----------|-----------|
| New Skins | Daily | 3 days |
| Challenges | Daily | 1 day |
| New Levels | Continuous | 1 week |
```

---

### Phase 3: Event Templates & Blueprints

**Duration: 20-25 minutes**

#### 3.1 Event Blueprint Template

```markdown
# Event Blueprint: [Event Name]

## Overview
- **Type:** [challenge/tournament/collection/sale/season/limited]
- **Duration:** [start] to [end] ([X] days)
- **Theme:** [visual/narrative theme]
- **Target Segment:** [all/payers/engaged/new/churned]

## Goals & Success Metrics

### Primary Goals
| Goal | Target | Measurement |
|------|--------|-------------|
| Engagement | [X]% DAU participation | event_start / DAU |
| Revenue | $[X] ARPDAU lift | period revenue delta |
| Retention | +[X]% D7 | cohort comparison |

### Secondary Goals
| Goal | Target | Measurement |
|------|--------|-------------|
| New Feature Adoption | [X]% trial | feature_first_use |
| Social Sharing | [X] shares | share_event |

## Mechanics

### Core Loop
1. [Step 1 - Player action]
2. [Step 2 - Reward/Progress]
3. [Step 3 - Repeat/Complete]

### Progression
| Milestone | Requirement | Reward |
|-----------|-------------|--------|
| Tier 1 | [X points] | [Reward] |
| Tier 2 | [X points] | [Reward] |
| Tier 3 | [X points] | [Reward] |
| Completion | [X points] | [Grand Prize] |

### Economy Impact
- **Currency Injection:** [X] soft currency per active player
- **Premium Opportunity:** [IAP offers tied to event]
- **Sink Integration:** [How event promotes spending]

## Content Requirements

### Art Assets
| Asset | Spec | Status |
|-------|------|--------|
| Event Banner | 1920x1080 | [ ] |
| Progress UI | [spec] | [ ] |
| Reward Icons | 256x256 each | [ ] |
| Theme Elements | [list] | [ ] |

### Audio
| Asset | Type | Status |
|-------|------|--------|
| Event Music | [duration] | [ ] |
| Reward SFX | [count] | [ ] |

### Localization
| Language | Status | Reviewer |
|----------|--------|----------|
| English | [ ] | [name] |
| [Lang 2] | [ ] | [name] |

## Technical Implementation

### Remote Config Keys
```json
{
  "event_[name]_enabled": true,
  "event_[name]_start_ts": "[timestamp]",
  "event_[name]_end_ts": "[timestamp]",
  "event_[name]_config": {
    "milestones": [...],
    "rewards": [...]
  }
}
```

### Required Events
- `event_[name]_start`
- `event_[name]_progress`
- `event_[name]_complete`
- `event_[name]_reward_claim`

### Feature Flags
- `ff_event_[name]`: Main event toggle
- `ff_event_[name]_iap`: IAP offers toggle

## Rollout Plan

### Pre-Launch (T-7 days)
- [ ] Art assets finalized
- [ ] QA testing complete
- [ ] Localization approved
- [ ] Remote config staged

### Launch Day
- [ ] Enable remote config at [time] UTC
- [ ] Push notification sent
- [ ] Social posts scheduled
- [ ] Support team briefed

### During Event
- [ ] Monitor participation hourly for first 4 hours
- [ ] Check revenue against projections daily
- [ ] Respond to player feedback

### Post-Event
- [ ] Disable event config
- [ ] Collect analytics report
- [ ] Document learnings
- [ ] Update template for next iteration

## Risk Mitigation

| Risk | Mitigation | Fallback |
|------|------------|----------|
| Low participation | Boost notifications | Extend duration |
| Economy imbalance | Reward tuning | Emergency patch |
| Technical issues | Remote disable | Compensation plan |
| Negative feedback | Community response | Adjust difficulty |

## Approval Checklist
- [ ] Design Lead approved
- [ ] Economy approved (no inflation)
- [ ] Legal approved (gambling laws)
- [ ] QA sign-off
- [ ] Localization complete
```

#### 3.2 Standard Event Templates

```yaml
templates:
  weekend_challenge:
    name: "Weekend Challenge"
    duration: "Friday 00:00 - Sunday 23:59 UTC"
    frequency: "Weekly"
    structure:
      - goal: "Complete X actions"
      - milestones: [3, 5, 10, 20, 30]
      - rewards: ["Small", "Medium", "Large", "Premium", "Grand"]
    best_practices:
      - "Launch Friday morning for maximum visibility"
      - "Set achievable goals for 60% of active players"
      - "Premium reward should be attainable with effort"

  daily_challenge:
    name: "Daily Challenge"
    duration: "24 hours, reset at 00:00 UTC"
    frequency: "Daily"
    structure:
      - goals: 3
      - difficulty: "Easy, Medium, Hard"
      - bonus: "Complete all 3 for bonus reward"
    best_practices:
      - "Easy should complete in normal session"
      - "Hard should require dedicated effort"
      - "Bonus creates completion incentive"

  limited_time_offer:
    name: "Limited Time Offer"
    duration: "24-48 hours"
    frequency: "2-3x per week"
    structure:
      - discount: "30-70% off"
      - items: "1-3 items per offer"
      - countdown: "Show remaining time"
    best_practices:
      - "Personalize based on player segment"
      - "Best conversion with 24h urgency"
      - "Stack value, don't just discount"

  collection_event:
    name: "Collection Event"
    duration: "7-14 days"
    frequency: "Monthly"
    structure:
      - collectibles: "5-10 unique items"
      - sources: "Gameplay, challenges, purchases"
      - milestones: "25%, 50%, 75%, 100%"
    best_practices:
      - "F2P must be able to complete with effort"
      - "Paying players get faster completion"
      - "Final reward should be exclusive/memorable"

  season_pass:
    name: "Season Pass"
    duration: "4-8 weeks"
    frequency: "Per season (4-6/year)"
    structure:
      - levels: 30-100
      - tracks: "Free + Premium"
      - xp_sources: "Daily play, challenges, purchases"
    best_practices:
      - "Level 1 should complete in first session"
      - "Premium price: 1-2 weeks of average spend"
      - "Premium track value should be 3-5x cost"
```

---

### Phase 4: Remote Config Architecture

**Duration: 15-20 minutes**

#### 4.1 Config Schema Design

```json
{
  "$schema": "remote-config-schema",
  "version": "1.0.0",
  "categories": {
    "feature_flags": {
      "description": "Boolean toggles for features",
      "naming": "ff_[feature_name]",
      "examples": {
        "ff_daily_rewards_v2": {
          "type": "boolean",
          "default": false,
          "description": "Enable new daily rewards UI"
        },
        "ff_tournament_mode": {
          "type": "boolean",
          "default": true,
          "description": "Enable tournament feature"
        }
      }
    },
    "tuning_values": {
      "description": "Numeric values for game balance",
      "naming": "tv_[system]_[parameter]",
      "examples": {
        "tv_economy_daily_coin_cap": {
          "type": "integer",
          "default": 1000,
          "min": 0,
          "max": 10000,
          "description": "Maximum coins earnable per day"
        },
        "tv_difficulty_enemy_hp_multiplier": {
          "type": "float",
          "default": 1.0,
          "min": 0.5,
          "max": 2.0,
          "description": "Global enemy HP scaling"
        }
      }
    },
    "events": {
      "description": "Event configurations",
      "naming": "event_[event_id]",
      "examples": {
        "event_halloween_2024": {
          "type": "object",
          "default": null,
          "schema": {
            "enabled": "boolean",
            "start_ts": "timestamp",
            "end_ts": "timestamp",
            "config": "object"
          }
        }
      }
    },
    "offers": {
      "description": "IAP offer configurations",
      "naming": "offer_[offer_id]",
      "examples": {
        "offer_starter_pack": {
          "type": "object",
          "schema": {
            "enabled": "boolean",
            "price_tier": "string",
            "contents": "array",
            "discount_percent": "integer",
            "show_after_level": "integer",
            "expires_hours": "integer"
          }
        }
      }
    },
    "ab_tests": {
      "description": "A/B test configurations",
      "naming": "ab_[test_id]",
      "examples": {
        "ab_onboarding_flow_v2": {
          "type": "object",
          "schema": {
            "enabled": "boolean",
            "allocation_percent": "integer",
            "variants": "array",
            "metrics": "array"
          }
        }
      }
    },
    "segments": {
      "description": "Player segment definitions",
      "naming": "seg_[segment_name]",
      "examples": {
        "seg_whales": {
          "type": "object",
          "schema": {
            "criteria": {
              "total_spend_usd_gte": 100,
              "last_purchase_days_lte": 30
            }
          }
        }
      }
    }
  }
}
```

#### 4.2 Platform Integration

```markdown
## Firebase Remote Config Setup

### 1. Parameter Groups
- `live_ops` - Event configurations
- `economy` - Tuning values
- `features` - Feature flags
- `monetization` - IAP configs
- `experiments` - A/B tests

### 2. Conditions
```
// High-Value Players
"total_revenue" > 50 AND "days_since_install" > 7

// New Players
"days_since_install" <= 3

// Churning Players
"days_since_last_session" >= 3 AND "days_since_last_session" <= 7

// Regional
"country" in ["US", "CA", "UK"]
```

### 3. Fetch Strategy
- Minimum fetch interval: 12 hours
- Expiration: 24 hours
- Activate on app foreground

## PlayFab Title Data Setup

### 1. Title Data Keys
```json
{
  "LiveOpsConfig": {
    "events": [...],
    "offers": [...],
    "segments": [...]
  },
  "GameTuning": {
    "economy": {...},
    "difficulty": {...}
  }
}
```

### 2. Player Data Segmentation
- Use GetPlayerSegments for targeting
- CloudScript for dynamic configs
- PlayStream for real-time events

## Unity Gaming Services

### 1. Remote Config Groups
- Environment: `production`, `staging`, `development`
- Settings: Per-environment configs
- Rules: Targeting conditions

### 2. Analytics Integration
- Link configs to Analytics events
- Automatic A/B test tracking
```

#### 4.3 Safety & Rollback

```markdown
## Remote Config Safety Rules

### 1. Default Values (MANDATORY)
Every config MUST have a safe default that works if backend unavailable:
- Feature flags → `false` (features off)
- Tuning values → Conservative values
- Events → `null` (no active event)
- Offers → Standard pricing

### 2. Rollback Procedures

#### Immediate Rollback (< 5 minutes)
1. Open remote config dashboard
2. Set `ff_emergency_rollback` = true
3. All clients will disable affected feature on next fetch

#### Staged Rollback
1. Set `ff_[feature]_percentage` = 0%
2. Monitor for 1 hour
3. Verify issue resolved
4. Document incident

### 3. Change Management

#### Low Risk Changes (Self-Approve)
- Typo fixes in text
- Minor tuning adjustments (±10%)
- Enabling tested features

#### Medium Risk Changes (Peer Review)
- New event launches
- Economy changes (±25%)
- New A/B tests

#### High Risk Changes (Team Approval)
- Economy changes (>25%)
- Monetization changes
- Feature rollbacks
- Emergency patches

### 4. Monitoring Alerts

| Alert | Condition | Action |
|-------|-----------|--------|
| Revenue Drop | >20% vs expected | Pause changes, investigate |
| Crash Spike | >2x baseline | Check recent configs |
| Error Rate | >1% of sessions | Check feature flags |
| Engagement Drop | D1 -5% | Review event performance |
```

---

### Phase 5: A/B Testing Roadmap

**Duration: 10-15 minutes**

#### 5.1 Test Prioritization Framework

```markdown
## A/B Test Prioritization Matrix

### Impact vs Effort
| Priority | Impact | Effort | Examples |
|----------|--------|--------|----------|
| P0 | High Revenue | Low | Price testing, offer timing |
| P1 | High Engagement | Low | UI placement, copy changes |
| P2 | High Revenue | High | New features, mechanics |
| P3 | High Engagement | High | Progression redesign |
| P4 | Low Impact | Any | Polish, minor improvements |

### Test Categories

#### Monetization Tests (Priority Focus)
1. Price point optimization
2. Offer timing and triggers
3. Bundle composition
4. Discount strategies
5. IAP placement

#### Engagement Tests
1. Notification timing and copy
2. Event difficulty and rewards
3. Session length optimization
4. Social feature placement
5. Reward schedules

#### Retention Tests
1. Onboarding flow
2. Day 1 experience
3. Re-engagement mechanics
4. Content pacing
5. Difficulty curves
```

#### 5.2 12-Week A/B Test Roadmap

```markdown
## A/B Testing Roadmap

### Weeks 1-4: Foundation
| Week | Test Name | Hypothesis | Metric | Duration |
|------|-----------|------------|--------|----------|
| 1 | Price Test v1 | Lower price = higher volume | Revenue/DAU | 14 days |
| 2 | Offer Timing | End of session = higher CVR | Conversion | 7 days |
| 3 | Push Copy | Urgency = higher open rate | Open Rate | 7 days |
| 4 | Event Rewards | Higher rewards = more engagement | Participation | 7 days |

### Weeks 5-8: Optimization
| Week | Test Name | Hypothesis | Metric | Duration |
|------|-----------|------------|--------|----------|
| 5 | Winning price at scale | Validate price finding | Revenue | 14 days |
| 6 | Bundle Test | 3 items > 5 items | AOV | 7 days |
| 7 | Difficulty Curve | Easier D1 = better D7 | D7 Retention | 14 days |
| 8 | Social Prompts | More prompts = more shares | Virality | 7 days |

### Weeks 9-12: Expansion
| Week | Test Name | Hypothesis | Metric | Duration |
|------|-----------|------------|--------|----------|
| 9 | Season Pass Price | $4.99 vs $9.99 | Attach Rate | 14 days |
| 10 | Reward Frequency | Daily > Weekly | Session Count | 14 days |
| 11 | VIP System | Exclusive access drives spend | Whale Revenue | 21 days |
| 12 | Consolidate Winners | Apply all winning variants | Overall LTV | Ongoing |
```

#### 5.3 Test Implementation Guide

```markdown
## A/B Test Implementation Checklist

### Pre-Launch
- [ ] Hypothesis documented
- [ ] Primary and secondary metrics defined
- [ ] Sample size calculated (power analysis)
- [ ] Duration estimated
- [ ] Variants implemented and QA'd
- [ ] Analytics events verified
- [ ] Rollback plan ready

### Sample Size Calculator
```
Required N per variant = 16 * (σ/δ)² * (1 + 1/k)

Where:
- σ = Standard deviation of metric
- δ = Minimum detectable effect (e.g., 5% lift)
- k = Number of variants

Example:
- σ = 20% (typical conversion std dev)
- δ = 5% (want to detect 5% improvement)
- k = 2 (control + 1 variant)

N = 16 * (0.20/0.05)² * 1.5 = 16 * 16 * 1.5 = 384 per variant
```

### During Test
- [ ] Monitor daily for data quality issues
- [ ] Check for sample ratio mismatch
- [ ] Watch for guardrail metric violations
- [ ] Document any incidents

### Post-Test
- [ ] Statistical significance achieved (p < 0.05)
- [ ] Practical significance evaluated
- [ ] Segment analysis completed
- [ ] Winner decision documented
- [ ] Implementation plan for winner
- [ ] Learnings added to knowledge base
```

---

## Quality Gates

### QG-LIVEOPS-001: Content Velocity
```yaml
id: QG-LIVEOPS-001
name: Content Velocity
threshold: "≥2 events per week minimum"
severity: HIGH

validation:
  method: "Count events in 12-week calendar"
  formula: "total_events / 12 >= 2"

evidence_required:
  - 12-week calendar with event counts per week
  - Event type distribution

failure_action:
  - Add filler events (challenges, sales)
  - Reduce event complexity to increase frequency
  - Consider automated event generation
```

### QG-LIVEOPS-002: Revenue Event Coverage
```yaml
id: QG-LIVEOPS-002
name: Revenue Event Coverage
threshold: "≥1 monetization event per week"
severity: CRITICAL

validation:
  method: "Count revenue-focused events"
  formula: "revenue_events / total_weeks >= 1"

revenue_event_types:
  - Sale events
  - Limited offers
  - Season pass launches
  - Premium content drops
  - Special bundles

failure_action:
  - Add sale events between content updates
  - Create limited-time offers tied to events
  - MUST NOT proceed without revenue touchpoints
```

### QG-LIVEOPS-003: Event Lead Time
```yaml
id: QG-LIVEOPS-003
name: Event Lead Time
threshold: "≥14 days before go-live"
severity: HIGH

validation:
  method: "Check calendar dates vs current date"
  formula: "all events have (go_live_date - plan_date) >= 14"

rationale:
  - 3-5 days: QA testing
  - 3-5 days: Localization
  - 2-3 days: Staging and verification
  - 2-3 days: Buffer for issues

failure_action:
  - Reduce event scope
  - Use template-based events
  - Consider automated content
```

### QG-LIVEOPS-004: Remote Config Rollback
```yaml
id: QG-LIVEOPS-004
name: Remote Config Rollback
threshold: "100% configs have fallback values"
severity: CRITICAL

validation:
  method: "Audit all remote config keys"
  formula: "configs_with_defaults / total_configs == 1.0"

checks:
  - Every feature flag defaults to false
  - Every tuning value has conservative default
  - Every event config has null default
  - Client handles missing configs gracefully

failure_action:
  - Add defaults to all configs
  - Test offline behavior
  - MUST NOT deploy without fallbacks
```

### QG-LIVEOPS-005: Calendar Coverage
```yaml
id: QG-LIVEOPS-005
name: Calendar Coverage
threshold: "≥12 weeks planned"
severity: HIGH

validation:
  method: "Count weeks in content calendar"
  formula: "weeks_planned >= 12"

rationale:
  - 12 weeks = 1 quarter planning horizon
  - Allows for content pipeline management
  - Enables marketing coordination
  - Supports seasonal planning

failure_action:
  - Extend calendar with placeholder events
  - Focus on repeatable event templates
  - Document assumptions for later weeks
```

---

## Outputs

### Primary Output: LiveOps Calendar (`memory/liveops-calendar.md`)

```markdown
# LiveOps Content Calendar

## Metadata
- **Generated:** [timestamp]
- **Planning Horizon:** Weeks 1-12
- **Total Events:** [count]
- **Revenue Events:** [count]
- **A/B Tests:** [count]

## Calendar Overview

| Week | Theme | Events | Revenue Focus | Key Dates |
|------|-------|--------|---------------|-----------|
| 1 | [Theme] | [Count] | [Event] | [Dates] |
...

## Detailed Weekly Breakdown

### Week 1: [Theme]
[Detailed breakdown per week as shown in Phase 2]

## Event Summary

### By Type
| Type | Count | Total Duration | Revenue Share |
|------|-------|----------------|---------------|
| Challenge | X | X days | X% |
| Tournament | X | X days | X% |
| Sale | X | X days | X% |
| Collection | X | X days | X% |
| Season | X | X days | X% |

### By Revenue Impact
| Tier | Events | Expected Revenue |
|------|--------|------------------|
| High ($$$) | [list] | $X |
| Medium ($$) | [list] | $X |
| Low ($) | [list] | $X |

## Dependencies

### Art Assets Required
[List with due dates]

### Development Work
[List with sprint allocation]

### External Dependencies
[Holidays, marketing campaigns, etc.]
```

### Primary Output: LiveOps Playbook (`memory/liveops-playbook.md`)

```markdown
# LiveOps Playbook

## Standard Operating Procedures

### Daily Operations
1. [Morning] Check overnight metrics
2. [Morning] Review player feedback
3. [Midday] Verify active events
4. [Evening] Prepare next day content

### Event Launch Checklist
[Detailed checklist from event template]

### Emergency Procedures
[Incident response for various scenarios]

## Team Responsibilities

### LiveOps Manager
- Calendar ownership
- Event performance
- Revenue targets

### Content Team
- Asset creation
- Event design
- Quality assurance

### Engineering
- Remote config
- Feature implementation
- Bug fixes

## Escalation Matrix
[When to escalate, to whom, for what issues]

## Key Contacts
[Team directory with responsibilities]
```

### Secondary Output: Remote Config Export (`memory/remote-config.json`)

```json
{
  "schema_version": "1.0.0",
  "generated_at": "[timestamp]",
  "platform": "firebase|playfab|unity",
  "parameters": {
    "feature_flags": {...},
    "tuning_values": {...},
    "events": {...},
    "offers": {...}
  },
  "conditions": [...],
  "defaults": {...}
}
```

---

## Industry Benchmarks

### Event Frequency by Genre

| Genre | Events/Week | Event Types | Avg Duration |
|-------|-------------|-------------|--------------|
| Casual (Match-3, Puzzle) | 3-4 | Challenges, Collections | 2-3 days |
| Mid-Core (Strategy, RPG) | 4-6 | Raids, Tournaments, Story | 3-7 days |
| Hyper-Casual | 2-3 | Simple challenges | 1-2 days |
| Social Casino | 5-7 | Tournaments, Bonuses | 1-3 days |

### Top Performer Benchmarks

| Company | Key Metric | Target |
|---------|------------|--------|
| Supercell | Event Participation | 60-80% DAU |
| King | Daily Event Completion | 40-60% |
| Mihoyo | Banner Revenue Share | 30-40% monthly |
| Zynga | LiveOps Revenue Lift | +40% vs baseline |

### A/B Test Win Rates

| Test Category | Expected Win Rate | Typical Lift |
|---------------|-------------------|--------------|
| Price Testing | 30-40% | 5-15% revenue |
| UI Changes | 20-30% | 3-8% conversion |
| Copy Changes | 15-25% | 2-5% engagement |
| Feature Variations | 10-20% | 5-20% (varies) |

---

## Examples

### Example 1: Casual Match-3 Game

```markdown
## 12-Week LiveOps Calendar - Match-3

### Week 1: New Year Fresh Start
- Mon: New Year Challenge (72h) - Complete 50 levels
- Thu: Flash Sale (24h) - 50% off lives bundle
- Sat: Weekend Tournament (48h) - High score competition

### Week 2: Winter Wonderland (Theme Week)
- Mon: Collection Event Start (7 days) - Collect snowflakes
- Wed: Daily Challenges (ongoing)
- Fri: Limited Offer (48h) - Winter character pack

[Continue for 12 weeks...]

## Event Templates Used
- weekend_challenge: 12 instances
- daily_challenge: Daily
- collection_event: 2 instances
- sale_event: 8 instances
- limited_content: 4 instances

## A/B Tests
1. Week 2: Test challenge difficulty (Easy vs Normal)
2. Week 4: Test sale timing (Start of week vs weekend)
3. Week 6: Test reward values (+20% vs baseline)
4. Week 8: Test notification frequency (2/day vs 3/day)
```

### Example 2: Mid-Core RPG

```markdown
## 12-Week LiveOps Calendar - Mobile RPG

### Season 4: Rise of the Dragon (8 weeks)

#### Week 1: Season Launch
- Battle Pass Season 4 Launch
- Login Event: 7-day dragon-themed rewards
- Banner: New SSR Dragon Knight

#### Week 2: Dragon's Challenge
- Raid Event: Dragon's Lair (Hard mode)
- Guild War Season Start
- Limited Shop: Dragon equipment

[Continue with detailed weekly plans...]

## Key Revenue Moments
1. Season Pass Launch (Week 1) - Target: $X ARPDAU lift
2. Mid-Season Banner (Week 4) - Target: 3x normal revenue
3. End-Season FOMO (Week 7-8) - Target: 2x week-over-week

## Content Pipeline
- New characters needed: 4 (SSR: 2, SR: 2)
- New equipment sets: 2
- New story chapters: 3
- New raid bosses: 2
```

---

## Handoffs

### To `/speckit.analytics`
```markdown
When: Analytics setup incomplete
Context:
- Required events for LiveOps tracking
- KPI dashboards needed
- A/B test infrastructure
```

### To `/speckit.softlaunch`
```markdown
When: Ready to test LiveOps in market
Context:
- Event calendar for test markets
- Remote config setup
- Success metrics
```

### To `/speckit.implement`
```markdown
When: LiveOps features need development
Context:
- Event system architecture
- Remote config integration
- A/B testing framework
```

---

## Appendix

### A. Seasonal Event Calendar (Global)

```markdown
## Major Holidays (Tier 1)
| Holiday | Date Range | Regions | Revenue Potential |
|---------|------------|---------|-------------------|
| New Year | Dec 31 - Jan 7 | Global | High |
| Lunar New Year | Jan-Feb (varies) | APAC | Very High |
| Valentine's Day | Feb 7-14 | Western | Medium |
| Easter | Mar-Apr (varies) | Western | Medium |
| Golden Week | Apr 29 - May 5 | Japan | Very High |
| Summer Event | June-July | Global | High |
| Halloween | Oct 24-31 | Western | High |
| Singles Day | Nov 11 | China | Very High |
| Black Friday | Nov 22-29 | Western | Very High |
| Christmas | Dec 18-25 | Western | Very High |
```

### B. Push Notification Best Practices

```markdown
## Timing
- Best hours: 12-2pm, 7-9pm local time
- Avoid: Late night, early morning
- Frequency: Max 2-3/day

## Copy Templates
- Urgency: "Only 2 hours left! [Event] ends soon"
- FOMO: "Don't miss [Reward] - today only!"
- Achievement: "You're so close! Just 3 more to complete"
- Social: "[Friend] just beat your high score!"

## Personalization
- Use player name when possible
- Reference specific progress
- Segment by behavior
```

### C. LiveOps Metrics Dashboard

```markdown
## Real-Time Metrics
- Active events and participation %
- Revenue vs target
- Player complaints/issues

## Daily Metrics
- Event start/complete rates
- A/B test health
- Config change log

## Weekly Metrics
- Content velocity actual vs planned
- Revenue by event type
- Player segment engagement
```

---

**Document Version:** 1.0.0
**Last Updated:** 2025-01-12
**Compatible with:** Spec-Kit v0.4.0+

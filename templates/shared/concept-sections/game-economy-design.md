# Game Economy Design Framework

## Overview

Framework для проектирования игровой экономики, включая валюты, источники дохода, и механики расходования.

## Currency Types

| Type | Characteristics | Examples | Monetization |
|------|-----------------|----------|--------------|
| Soft Currency | Earned through play, abundant | Coins, Gold | Time = currency |
| Hard Currency | Scarce, purchased with money | Gems, Diamonds | Direct IAP |
| Time-Gated | Limited by cooldowns | Energy, Stamina | Patience or IAP |
| Social Currency | Earned through social actions | Friend points | Engagement driver |

## Income Sources (Generators)

- Core loop rewards (per session, per level)
- Daily login rewards
- Achievement/milestone rewards
- Social rewards (gifting, referrals)
- Time-based generators (idle mechanics)
- IAP (direct purchase)
- Rewarded ads

**Calculation**: Daily income per player = ∑(source × frequency × amount)

## Expense Sinks (Consumers)

- Progression gates (level up, unlock)
- Consumables (powerups, boosts)
- Cosmetics (skins, emotes)
- Gacha/loot boxes
- Speed-ups (skip timers)
- Retries (extra lives, continues)

**Calculation**: Daily expenses = ∑(sink × usage rate × cost)

## Balance Framework

**Target**: Income ≈ Expenses (slight deficit for monetization pressure)

**Metrics**:
- **Gini Coefficient**: Wealth inequality (target <0.6 for fairness)
- **Inflation Rate**: Currency value over time (target <10%/month)
- **F2P Progression Rate**: Days to reach milestone X without spending
- **Whale Impact**: % of economy controlled by top 1% spenders

**Formula**:
```
Daily Deficit = Daily Expenses - Daily Income
Monetization Pressure = Daily Deficit / Avg IAP Package Value
```

**Tuning**:
- Hyper-casual: Heavy income, minimal sinks (focus on engagement, not monetization)
- Casual: Balanced with gentle monetization pressure
- Mid-core: Medium deficit, IAP speed-ups attractive
- Core: High deficit in late game, cosmetics primary monetization

## Progression Gates

| Milestone | F2P Time | IAP Bypass | Rationale |
|-----------|----------|------------|-----------|
| Tutorial completion | 5 min | N/A | Must be instant |
| First wall | 1-2 days | $1-5 | Early conversion attempt |
| Mid-game wall | 1-2 weeks | $10-20 | Core player filter |
| Endgame wall | 1-3 months | $50-100 | Whale retention |

## Anti-Patterns to Avoid

❌ **Hyperinflation**: Doubling costs without doubling income (frustration)
❌ **Pay-to-win PvP**: Direct power from money in competitive modes
❌ **Dark patterns**: Hidden costs, misleading bundles
❌ **Economy locks**: No F2P path to progression
❌ **Sink-only events**: Events that only drain currency without income

## Validation Checklist

- [ ] F2P path exists to all core content (not just cosmetics)
- [ ] Daily income/expense ratio calculated for days 1, 7, 30
- [ ] Gini coefficient <0.6 (wealth inequality acceptable)
- [ ] Inflation rate <10%/month
- [ ] Progression gates aligned with genre norms
- [ ] IAP prices provide clear time-saving value
- [ ] No pay-to-win in competitive modes (GAM-004 compliance)

## Simulation-Ready Parameters

> **For `/speckit.analyze --profile game-economy`**: Add these parameters to enable Monte Carlo simulation

### Currency Configuration

```yaml
currencies:
  hard_currency:
    name: "Gems"
    earn_rate_f2p: 50  # gems per day (F2P baseline)
    earn_rate_whale: 5000  # gems per day (includes purchases)
    primary_sources:
      - "Daily login: 10 gems"
      - "Quest completion: 20 gems"
      - "Event rewards: 50-100 gems"
    primary_sinks:
      - "Gacha pulls: 300 gems"
      - "Stamina refills: 50 gems"
      - "Premium upgrades: 1000+ gems"

  soft_currency:
    name: "Gold"
    earn_rate: 1000  # gold per day
    primary_sources:
      - "Battles: 50 gold"
      - "Quests: 200 gold"
      - "Auto-farming: variable"
    primary_sinks:
      - "Upgrades: 500-5000 gold"
      - "Crafting: 1000 gold"
      - "Unit leveling: 2000 gold"

  premium_currency:  # optional
    name: "Battle Pass Points"
    earn_rate: "Monthly subscription ($9.99)"
    benefits:
      - "2x rewards multiplier"
      - "Exclusive cosmetics"
      - "500 bonus gems per week"
```

### Progression Milestones

```yaml
progression_milestones:
  early_game:  # Days 1-14
    - name: "Reach Level 10"
      f2p_time_budget: 7  # days
      whale_time_budget: 1  # days
      power_requirement: 500
      rewards: "Unlock PvP"

    - name: "Clear Chapter 3"
      f2p_time_budget: 10
      whale_time_budget: 2
      power_requirement: 800
      rewards: "Unlock Raid Mode"

    - name: "Unlock Hero Slot 4"
      f2p_time_budget: 14
      whale_time_budget: 3
      power_requirement: 1200
      rewards: "+1 team slot"

  mid_game:  # Days 15-60
    - name: "Unlock Raid Mode"
      f2p_time_budget: 30
      whale_time_budget: 3
      power_requirement: 2000
      rewards: "Guild content"

    - name: "Reach Level 30"
      f2p_time_budget: 45
      whale_time_budget: 7
      power_requirement: 3500
      rewards: "Advanced upgrades"

    - name: "Clear Chapter 10"
      f2p_time_budget: 60
      whale_time_budget: 10
      power_requirement: 5000
      rewards: "Endgame content"

  late_game:  # Days 61+
    - name: "Reach Level 50"
      f2p_time_budget: 120
      whale_time_budget: 20
      power_requirement: 8000
      rewards: "Max level cap"

    - name: "Clear All Chapters"
      f2p_time_budget: 180
      whale_time_budget: 30
      power_requirement: 12000
      rewards: "Completion reward"
```

### Gacha System (if applicable)

```yaml
gacha:
  type: "character_summon"
  rates:
    ssr: 0.01  # 1% (premium characters)
    sr: 0.10  # 10% (rare characters)
    r: 0.89  # 89% (common characters)
  cost_per_pull: 300  # gems
  pity_system:
    enabled: true
    threshold: 90  # pulls
    guarantee: "SSR"
  duplicate_handling: "Convert to upgrade materials (1 SSR = 100 shards)"
  expected_value:
    f2p: "1 SSR per 9,000 gems (180 days at 50/day)"
    whale: "1 SSR per 9,000 gems (1.8 days at 5000/day)"
```

### PvP System

```yaml
pvp:
  enabled: true
  power_scaling: "linear"  # or "exponential" (less fair)
  skill_factor: 0.30  # 30% skill can overcome power disadvantage
  matchmaking: "±20% power bracket"
  rewards: "Cosmetic only"  # or "Power items" (P2W concern)
  competitive_balance:
    power_gap_tolerance: 2.0  # whale vs F2P should be <2.0x
    exclusive_content: false  # No PvP-critical items locked
    seasonal_resets: "Quarterly"
```

### Player Archetypes (for simulation)

```yaml
player_archetypes:
  f2p:
    spending: 0  # $0/month
    playtime_hours_per_day: 1.5  # 1-2 hours
    efficiency: 0.70  # 70% optimal resource usage
    retention_rate: 0.50  # 50% still playing after 90 days

  dolphin:
    spending: 25  # $25/month
    playtime_hours_per_day: 3  # 2-4 hours
    efficiency: 0.85  # 85% optimal
    retention_rate: 0.70  # 70% retention

  whale:
    spending: 500  # $500/month
    playtime_hours_per_day: 6  # 4-8 hours
    efficiency: 0.95  # 95% optimal
    retention_rate: 0.90  # 90% retention
```

### Monetization Strategy

```yaml
monetization:
  pricing:
    small_pack: {price: "$0.99", gems: 100, value_multiplier: "2x"}
    medium_pack: {price: "$4.99", gems: 600, value_multiplier: "2.4x"}
    large_pack: {price: "$9.99", gems: 1300, value_multiplier: "2.6x"}
    whale_pack: {price: "$99.99", gems: 15000, value_multiplier: "3x"}
    battle_pass: {price: "$9.99/month", rewards: "2000 gems + cosmetics"}

  conversion_funnel:
    trial_payers: "5% convert at $0.99"
    dolphins: "2% convert at $10-50/month"
    whales: "0.5% convert at $500+/month"

  ethical_constraints:
    loot_box_disclosures: "Display odds prominently"
    spending_limits: "Warn at $100/day, hard cap at $500/day"
    no_fomo: "Limited events return quarterly"
    no_predatory_timers: "Wait timers skippable with soft currency"
```

## Example: Mid-Core RPG Economy

**Soft Currency (Gold)**:
- Income: 10,000/day (quests + dailies)
- Sinks: 12,000/day (equipment upgrades)
- Deficit: 2,000/day = $2 IAP package value
- F2P can grind extra 2 hours for deficit

**Hard Currency (Gems)**:
- Income: 50/day (free), 1000/day (subscription)
- Sinks: Gacha pulls (250 gems), Energy refills (100 gems)
- Conversion: 1 gem = $0.01 (100 gems = $1 IAP)

## References

- Deconstructor of Fun (blog on game economy teardowns)
- "Designing Games" by Tynan Sylvester (economy chapter)
- "Free-to-Play: Making Money From Games You Give Away" by Will Luton

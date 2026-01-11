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

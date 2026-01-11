# Retention Strategy Framework

## Overview

Framework для максимизации показателей удержания D1/D7/D30 через механики формирования привычки, инвестиции игрока и долгосрочного вовлечения.

## Retention Funnel

| Stage | Definition | Metric | Goal |
|-------|------------|--------|------|
| Install | User downloads app | Installs | 100% |
| First Session | User opens app first time | Install → FTU completion | 70-80% |
| Day 1 (D1) | User returns next day | D1 retention rate | Genre-specific (see below) |
| Day 7 (D7) | User returns after 7 days | D7 retention rate | Genre-specific (see below) |
| Day 30 (D30) | User returns after 30 days | D30 retention rate | Genre-specific (see below) |

**Calculation**:
```
D1 Retention = (Users returning on Day 1) / (Users who installed on Day 0)
D7 Retention = (Users returning on Day 7) / (Users who installed on Day 0)
D30 Retention = (Users returning on Day 30) / (Users who installed on Day 0)
```

## Genre Benchmarks

| Genre | D1 Retention | D7 Retention | D30 Retention | Core Loop Duration |
|-------|--------------|--------------|---------------|-------------------|
| Hyper-casual | 35-45% | 15-25% | 5-10% | 30-60 sec |
| Casual | 40-50% | 20-30% | 10-15% | 1-3 min |
| Mid-core | 50-60% | 30-40% | 15-25% | 5-10 min |
| Core | 60-70% | 40-50% | 25-35% | 15-30 min |

**Source**: Deconstructor of Fun, GameRefinery Mobile Gaming Benchmark 2025

## Retention Mechanics by Phase

### First Session (0-5 minutes) — The Hook

**Objective**: Show core loop value immediately

**Mechanics**:
- Minimal tutorial (skip-able after first completion)
- Core loop demo within first 60 seconds
- First win guaranteed
- Immediate positive feedback (rewards, praise)
- Clear progression preview (show what's next)

**Anti-Pattern**: Long exposition, text-heavy tutorial, no agency

**Target**: 70-80% FTU completion rate

### Days 1-7 — Habit Formation

**Objective**: Build daily play habit through scheduled rewards

**Mechanics**:
- Daily login rewards (escalating value, streak bonus)
- Daily quests/missions (2-3 achievable in 10-15 min)
- Energy system (regenerates every 4-6 hours, caps at 5 refills/day)
- Push notifications (optimal: 10am, 6pm local time)
- Streaks (3-day, 7-day milestones with bonus)
- Time-limited events (24-48 hour windows)

**Psychological Triggers** (Hooked Model):
1. **Trigger**: Push notification "Your energy is full!"
2. **Action**: Open app, play 1-2 sessions
3. **Variable Reward**: Loot drop, gacha pull, quest completion
4. **Investment**: Spend resources, upgrade character

**Target**: D7 retention ≥ 50% of D1 retention

### Days 7-30 — Depth & Investment

**Objective**: Deepen engagement through meta-progression and social bonds

**Mechanics**:
- Meta-progression (account level, skill trees, collection systems)
- Social features (friends list, gifting, co-op missions)
- Guild/clan system (unlocks at Day 3-5)
- Weekly events (7-day cycles)
- FOMO mechanics (limited-time offers, seasonal content)
- Sunk cost fallacy (collection completion, ascension systems)

**Investment Layers**:
1. Time investment (hours played)
2. Progress investment (levels, unlocks)
3. Social investment (friends, guild status)
4. Identity investment (customization, achievements)
5. Financial investment (IAP history)

**Target**: D30 retention ≥ 40% of D7 retention

### Days 30+ — Endgame & Community

**Objective**: Provide infinite progression and social status

**Mechanics**:
- Competitive ladder (PvP seasons, leaderboards)
- Guilds as core loop (guild wars, raids)
- Content treadmill (new events every 2-4 weeks)
- Prestige systems (reset progress for permanent bonuses)
- User-generated content (if applicable)
- Esports/streaming integration (for core games)

**Endgame Loops**:
- **Vertical progression**: Power scaling (new tiers, rarities)
- **Horizontal progression**: Collection completion (cosmetics, variants)
- **Social progression**: Guild rank, leaderboard position
- **Skill progression**: Mastery systems, competitive rating

**Target**: D90 retention ≥ 70% of D30 retention

## Churn Risk Detection

### Leading Indicators (Alert Thresholds)

| Indicator | Definition | Threshold | Action |
|-----------|------------|-----------|--------|
| Session gap | Time since last session | >48 hours | Re-engagement notification |
| Declining session count | Sessions/day dropping | <50% of avg | Offer incentive (gift, bonus) |
| Negative progression | Stuck on same level | >3 days | Difficulty adjustment |
| Social isolation | No friend interactions | 7 days | Friend invite bonus |
| Zero IAP after 30 days | No purchase history | Day 30 | Starter pack offer |

### Intervention Strategies

1. **Win-back notifications**: "We miss you! Here's 500 gems"
2. **Difficulty adjustment**: Dynamic balancing for stuck players
3. **Social nudges**: "5 friends are online now"
4. **Personalized offers**: 50% discount on player's favorite item
5. **Content unlocks**: Free trial of premium feature

## Anti-Churn Design Principles (MBG-008 Compliance)

**MBG-008**: Design must respect player autonomy and avoid manipulative retention tactics

✅ **Ethical Retention**:
- Optional daily bonuses (not punishment for missing)
- Generous energy caps (allow binge sessions)
- Clear progression paths (no mystery gates)
- Offline progress (idle rewards)
- Respectful notifications (opt-in, not spam)

❌ **Dark Patterns to Avoid**:
- Streak-breaking punishment (losing all progress)
- Aggressive timers (fear of missing out)
- Fake social proof ("1000 players online now!")
- Hidden paywalls (bait-and-switch)
- Manipulation of vulnerable players

## Cohort Analysis

### Cohort Definition

**Cohort**: Group of users who installed on the same date

**Cohort Slicing**:
- By acquisition channel (organic, paid, influencer)
- By geography (US, EU, APAC)
- By device (iOS, Android, high-end vs low-end)
- By behavior (spenders vs F2P, hardcore vs casual)

### Metrics Table

| Cohort | D1 | D7 | D30 | D90 | ARPU | Conversion Rate |
|--------|----|----|-----|-----|------|-----------------|
| 2026-01-01 | 55% | 35% | 18% | 12% | $1.20 | 3.5% |
| 2026-01-08 | 58% | 38% | 20% | — | $1.35 | 4.1% |
| 2026-01-15 | 52% | 32% | — | — | $0.95 | 2.8% |

**Analysis**:
- Week 2 cohort has better retention (+3% D1) → investigate changes made
- Week 3 cohort has worse conversion (-1.3%) → check IAP pricing changes

## Validation Checklist

- [ ] D1/D7/D30 targets defined based on genre benchmarks
- [ ] Habit loop identified: Trigger → Action → Reward → Investment
- [ ] Daily engagement mechanics (login rewards, dailies, energy)
- [ ] Meta-progression unlocks at Day 3-7 (guilds, social features)
- [ ] Churn detection system with leading indicators
- [ ] Win-back campaigns for lapsed users (>48 hours)
- [ ] Cohort tracking by acquisition channel
- [ ] No dark patterns or manipulative retention tactics (MBG-008)
- [ ] Offline progress or idle rewards (respect player time)
- [ ] Push notifications opt-in with clear value proposition

## Example: Mid-Core RPG Retention Strategy

**D1 Hook (First 5 minutes)**:
- Tutorial battle (guaranteed win) → 3 loot drops → level up
- Show progression tree (50 unlockable skills)
- Tease social feature: "Unlock guilds at Level 5"

**D1-D7 Habit (Daily Loop)**:
- Daily login: 100 gems (escalates to 500 on Day 7)
- 3 daily quests (10 min each, rewards: 1000 gold, 50 gems)
- Energy system: 5 energy, regenerates 1/4 hours
- Push notification: "Your energy is full!" (10am, 6pm)

**D7-D30 Depth (Meta-Progression)**:
- Guild unlocked at Level 10 (Day 5 avg)
- Weekly guild raid (requires coordination)
- Collection system: 200 heroes, 50 weapons
- Seasonal event every 2 weeks (limited-time hero)

**D30+ Endgame (Infinite Loop)**:
- PvP season (monthly leaderboard reset)
- Guild wars (inter-guild competition)
- Prestige system: Reset account for +10% permanent stats
- Content treadmill: New hero class every month

**Retention Targets**:
- D1: 55% (mid-core benchmark: 50-60%)
- D7: 35% (64% of D1, target ≥50%)
- D30: 18% (51% of D7, target ≥40%)
- Churn intervention: <48h gap triggers win-back notification

## References

- "Hooked: How to Build Habit-Forming Products" by Nir Eyal
- Deconstructor of Fun (retention teardowns)
- GameRefinery Mobile Gaming Benchmark 2025
- "The Art of Game Design" by Jesse Schell (engagement loops)

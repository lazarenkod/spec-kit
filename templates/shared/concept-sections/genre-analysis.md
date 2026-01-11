# Genre Analysis Framework

## Overview

Framework для классификации жанров мобильных игр и определения must-have фич. Помогает выбрать правильные KPI targets, retention benchmarks, и дизайн-паттерны.

## Mobile Game Genre Taxonomy

| Genre | Session Length | Control Complexity | Retention Target | CPI Target | Monetization |
|-------|----------------|-------------------|------------------|------------|--------------|
| Hyper-Casual | 2-5 min | One-thumb | D1: 35-45%, D7: 10-15% | <$0.50 | Ads + IAP removal |
| Casual | 10-20 min | Simple tap/swipe | D1: 40-50%, D7: 20-30% | $1-3 | Hybrid (IAP + Ads) |
| Mid-Core | 20-45 min | Multi-button | D1: 45-55%, D7: 30-40% | $3-10 | F2P + IAP |
| Core | 45+ min | Complex controls | D1: 50-60%, D7: 40-50% | $10-50 | Cosmetics + Battle Pass |

## Hyper-Casual Genre

**Characteristics**:
- One-thumb controls, instant gameplay
- No tutorials, pure skill expression
- 2-5 minute session length
- Viral loop potential (share scores)

**Examples**: Flappy Bird, Helix Jump, Balls vs Blocks, Stack

**Must-Have Features**:
- Instant restart (<1 sec)
- Progressive difficulty (easy start, hard mastery)
- Score/combo system
- Social sharing hooks
- Optional video ads for continues

**KPI Targets**:
- D1 Retention: 35-45%
- CPI: <$0.50
- Session length: 3-5 min
- Sessions/day: 4-6
- ARPDAU: $0.05-0.15
- Ad load: 3-5 ads/session

**Monetization**: 80% ads, 20% IAP (ad removal, cosmetics)

## Casual Genre

**Characteristics**:
- 10-20 minute sessions
- Meta-progression (stars, currencies)
- Social features (leaderboards, lives)
- Regular content updates (levels, events)

**Examples**: Candy Crush, Homescapes, Township, Merge Dragons

**Must-Have Features**:
- Level-based progression (100+ levels)
- Energy/lives system (5 lives, 20 min refill)
- Powerups/boosters (3-5 types)
- Daily rewards calendar
- Social lives/gifting
- Events (weekly themes)

**KPI Targets**:
- D1 Retention: 40-50%
- D7 Retention: 20-30%
- D30 Retention: 10-15%
- CPI: $1-3
- Session length: 12-18 min
- ARPDAU: $0.20-0.50
- Conversion: 3-7%

**Monetization**: Hybrid (50% IAP, 50% ads)

## Mid-Core Genre

**Characteristics**:
- 20-45 minute sessions
- Deep progression systems (levels, gear, skills)
- PvP/guild features
- Gacha/collection mechanics
- Daily/weekly grind loops

**Examples**: Clash Royale, AFK Arena, RAID: Shadow Legends, Genshin Impact

**Must-Have Features**:
- Hero/character collection (50+ units)
- Gear/equipment system (rarities, upgrades)
- PvP arena (ranked ladder)
- Guild/clan system (chat, raids)
- Daily quests (5-10 objectives)
- Idle/auto-battle mechanics
- Gacha/loot boxes
- VIP/subscription system

**KPI Targets**:
- D1 Retention: 45-55%
- D7 Retention: 30-40%
- D30 Retention: 15-25%
- CPI: $3-10
- Session length: 25-40 min
- ARPDAU: $0.50-2.00
- Conversion: 5-15%
- Whale LTV: $100-1000

**Monetization**: F2P + IAP (gacha pulls, speed-ups, subscriptions)

## Core Genre

**Characteristics**:
- 45+ minute sessions
- High skill ceiling
- Competitive PvP focus
- Esports potential
- Premium graphics/production

**Examples**: PUBG Mobile, Call of Duty Mobile, League of Legends: Wild Rift, Genshin Impact

**Must-Have Features**:
- Skill-based matchmaking (MMR)
- Ranked seasons (monthly/quarterly)
- Battle Pass system (100 tiers)
- Cosmetics shop (skins, emotes)
- Clan/team features
- Spectator mode
- Replays/highlights
- Cross-platform play (optional)

**KPI Targets**:
- D1 Retention: 50-60%
- D7 Retention: 40-50%
- D30 Retention: 25-35%
- CPI: $10-50
- Session length: 50-90 min
- ARPDAU: $1.00-5.00
- Conversion: 10-30%
- Whale LTV: $500-5000

**Monetization**: Cosmetics (70%) + Battle Pass (30%)

## Genre-Specific Design Patterns

### Hyper-Casual Patterns

| Pattern | Description | Examples |
|---------|-------------|----------|
| Endless Runner | Avoid obstacles, collect items | Subway Surfers, Temple Run |
| Timing/Rhythm | Tap to precise beat | Piano Tiles, Dancing Line |
| Physics Puzzle | Drop/place objects | Cut the Rope, Where's My Water |
| Swerve Control | Left/right dodge | Traffic Run, Aquapark.io |
| Merge/Stack | Combine identical items | 2048, Merge Plane |

### Casual Patterns

| Pattern | Description | Examples |
|---------|-------------|----------|
| Match-3 | Swap tiles to match 3+ | Candy Crush, Bejeweled |
| Merge | Combine 2 items → 1 upgrade | Merge Dragons, EverMerge |
| Builder | Construct/decorate spaces | Homescapes, Township |
| Bubble Shooter | Aim and pop bubbles | Bubble Witch, Panda Pop |
| Hidden Object | Find items in scenes | June's Journey, Pearl's Peril |

### Mid-Core Patterns

| Pattern | Description | Examples |
|---------|-------------|----------|
| Gacha Collector | Pull for heroes, build teams | RAID, AFK Arena |
| 4X Strategy | Expand, exploit, exterminate | Rise of Kingdoms, Clash of Clans |
| Auto-Battler | Team composition, minimal input | Auto Chess, TFT |
| Idle RPG | Progress while offline | AFK Arena, Idle Heroes |
| Tower Defense | Place units to defend | Kingdom Rush, Bloons TD |

### Core Patterns

| Pattern | Description | Examples |
|---------|-------------|----------|
| MOBA | 5v5 lanes, destroy base | League of Legends: Wild Rift, Mobile Legends |
| Battle Royale | 100 players, last one standing | PUBG Mobile, Free Fire |
| FPS | First-person shooter | Call of Duty Mobile, Modern Combat |
| MMORPG | Persistent world, quests, raids | Black Desert Mobile, Lineage 2M |

## Competitive Analysis Template

**Game**: [Name]

**Genre**: [Primary/Secondary]

**Strengths**:
- Feature X (quantified metric)
- Mechanic Y (player quote/review)

**Weaknesses**:
- Missing feature Z (opportunity)
- Friction point W (rating mention)

**Opportunities**:
- Underserved segment (demographic data)
- Emerging trend (market research link)

**Must-Match Features**:
- [ ] Feature A (table stakes for genre)
- [ ] Feature B (players expect this)

**Must-Avoid Anti-Patterns**:
- [ ] Dark pattern C (player backlash)
- [ ] Mechanic D (negative review theme)

## Validation Checklist

- [ ] Genre selected from taxonomy (Hyper/Casual/Mid/Core)
- [ ] Session length target matches genre (±5 min tolerance)
- [ ] Retention targets realistic for genre (±5% tolerance)
- [ ] Must-have features identified (3-5 core features)
- [ ] Monetization strategy aligned with genre norms
- [ ] Competitive analysis completed (3-5 top games)
- [ ] Must-match features list (5-10 items)
- [ ] Must-avoid anti-patterns list (3-5 items)
- [ ] KPI targets set (D1, D7, D30, CPI, ARPDAU)

## References

- **GameRefinery**: Genre taxonomy and feature tracking (gamerefinery.com)
- **Sensor Tower**: Market intelligence and genre benchmarks (sensortower.com)
- **Deconstructor of Fun**: Genre analysis and monetization breakdowns (deconstructoroffun.com)
- **PocketGamer.biz**: Genre trends and market reports
- **Mobile Dev Memo**: Genre-specific retention and monetization data

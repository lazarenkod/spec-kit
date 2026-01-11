# Player Psychology Framework

## Overview

Framework для анализа и дизайна игровой мотивации с использованием проверенных психологических моделей. Все техники должны соответствовать MBG-008 (Ethical Psychology) — игра мотивирует через fun, не через манипуляцию.

**Core Principle**: Intrinsic motivation (fun, mastery, autonomy) > Extrinsic manipulation (FOMO, addiction, exploitation)

## Bartle's Player Types

### Overview

Классификация игроков по мотивации (Bartle, 1996). Разработана для MUD, применима к любым играм с социальным компонентом.

**Distribution** (approximate, varies by genre):
- Achievers: 40%
- Explorers: 20%
- Socializers: 20%
- Killers: 20%

### ♦ Achievers (Acting on World)

**Motivation**: Progression, completion, mastery

**What They Want**:
- Clear goals and metrics (levels, achievements, leaderboards)
- Progression systems (XP, skill trees, unlocks)
- Status symbols (rare titles, cosmetics)
- Challenges to overcome (hard modes, speedruns)

**Design For**:
- Achievement lists with % completion
- Leaderboards (global, friends, weekly)
- Progression transparency (XP bars, next unlock visible)
- Difficulty tiers (Normal → Hard → Nightmare)

**KPIs**: Completion rate, achievement unlock rate, time to max level

**Example Games**: Diablo, Call of Duty, WoW

### ♠ Explorers (Interacting with World)

**Motivation**: Discovery, knowledge, understanding systems

**What They Want**:
- Hidden content (secret areas, easter eggs)
- Deep mechanics to master (emergent gameplay)
- Lore and worldbuilding (collectible logs, environmental storytelling)
- Experimentation (crafting, build diversity)

**Design For**:
- Non-linear exploration (metroidvania gates, open world)
- Hidden collectibles (100% map completion)
- Lore codex (discoverable entries)
- Complex systems (skill synergies, elemental interactions)

**KPIs**: Map exploration %, collectible discovery rate, unique build diversity

**Example Games**: Zelda: Breath of the Wild, Elden Ring, Terraria

### ♥ Socializers (Interacting with Players)

**Motivation**: Relationships, community, shared experiences

**What They Want**:
- Social features (friends, guilds, chat)
- Cooperative content (raids, team modes)
- Self-expression (character customization, player housing)
- Shared goals (guild events, clan wars)

**Design For**:
- Guild/clan systems with progression
- In-game chat with emotes/stickers
- Cooperative PvE (not just PvP)
- Social spaces (hubs, lobbies, player homes)

**KPIs**: Friend count, guild membership %, daily social interactions

**Example Games**: Animal Crossing, Among Us, Final Fantasy XIV

### ♣ Killers (Acting on Players)

**Motivation**: Competition, domination, testing skill

**What They Want**:
- PvP modes (ranked, arenas, duels)
- Skill-based matchmaking (fair fights)
- Public recognition (kill cams, MVP awards)
- Power expression (outplays, 1vX)

**Design For**:
- Ranked competitive modes with visible MMR
- Spectator features (replays, kill cams)
- Skill-based gameplay (not pay-to-win)
- Leaderboards with skill tiers (Bronze → Grandmaster)

**KPIs**: PvP participation rate, competitive retention, rank distribution

**Example Games**: League of Legends, Fortnite, Street Fighter

### Balance Note

**All 4 types should have paths to enjoyment** in your game, even if one type dominates. Example:
- RPG (Achiever-focused): Still needs exploration (secrets), social (guilds), PvP (arenas)
- Battle Royale (Killer-focused): Still needs progression (battle pass), social (squads), exploration (map)

**Risk**: Ignoring minority types → 60% of potential audience alienated.

## Self-Determination Theory (SDT)

### Overview

Framework для intrinsic motivation (Ryan & Deci, 2000). Players stay engaged when 3 psychological needs are met:

### 1. Autonomy

**Definition**: Player feels in control, not forced

**Design For**:
- Meaningful choices (skill trees, playstyles, dialogue options)
- Player agency (multiple solutions to problems)
- Opt-in difficulty (hard mode toggle, assist options)
- Respect player time (no mandatory daily grind)

**Anti-Patterns**:
- ❌ Forced tutorials (skippable after first time)
- ❌ Linear progression (one viable build)
- ❌ Daily login punishment (missing = permanent loss)

### 2. Competence

**Definition**: Player feels capable and improving

**Design For**:
- Clear feedback (damage numbers, "Great!" popups)
- Progressive difficulty (tutorial → challenge → mastery)
- Visible progression (levels, unlocks, achievements)
- Skill-based success (not RNG-gated)

**Anti-Patterns**:
- ❌ Unclear failure states (why did I die?)
- ❌ Difficulty spikes (level 10 boss is impossible)
- ❌ Progress gatekeeping (paywall, grindwall)

### 3. Relatedness

**Definition**: Player feels connected to others

**Design For**:
- Social features (guilds, friends, chat)
- Cooperative gameplay (not just competitive)
- Shared goals (clan events, world events)
- Spectator features (watch friends, streamers)

**Anti-Patterns**:
- ❌ Solo-only content (no co-op option)
- ❌ Toxic competitive modes (no moderation)
- ❌ Isolated progression (can't help friends)

### Result

When all 3 needs met → **Intrinsic motivation** → Long-term engagement without manipulation.

## Flow Theory (Csikszentmihalyi)

### Overview

Players experience "flow" (optimal engagement) when challenge matches skill. Too easy = boredom, too hard = frustration.

```
   Challenge
      ^
      |
  A3  |  [Flow Channel]  F3
      |  /            \
  A2  | /   FLOW       \ F2
      |/                 \
  A1  +--------------------→ Skill
      |  \   BOREDOM   /
  B1  |   \          /
      |    [Anxiety]
      |
```

**Flow Channel**: Narrow band where challenge slightly exceeds skill (promotes growth)

### Dynamic Difficulty Adjustment (DDA)

**Techniques**:
1. **Rubber Banding** (racing games): AI slows down if player far behind
2. **Adaptive Spawns** (shooters): Fewer enemies if player low health
3. **Hidden Assists** (platformers): Slightly larger hitboxes after repeated deaths
4. **Difficulty Scaling** (RPGs): Enemy levels scale with player level

**Ethical Implementation**:
- ✅ Transparent (player aware of assists, can disable)
- ✅ Opt-in (hard mode available)
- ❌ Hidden manipulation (fake difficulty)
- ❌ Performance punishment (good players get harder game with no reward)

### KPI Impact

- **Retention**: Players in flow → higher D7 retention (+20-40%)
- **Session Length**: Flow state → longer sessions (+30-50%)
- **Conversion**: Competence feeling → more likely to pay (ego investment)

## Dopamine Loops

### Overview

Game loops trigger dopamine release (reward anticipation). Ethical use = fun, unethical = addiction.

### Core Loop (10-60 seconds)

**Example**: Kill enemy → Loot drop → Equip better gear → Kill stronger enemy

**Dopamine Trigger**: Immediate reward, variable ratio (loot RNG)

**Design**:
- Fast feedback (hit markers, XP popup)
- Variable rewards (sometimes common, sometimes legendary)
- Always progression (even "bad" loot = salvage materials)

**Ethical Boundary**: Not slot-machine RNG (Diablo loot = OK, gacha pulls = predatory)

### Progress Loop (5-20 minutes)

**Example**: Complete quest → Level up → Unlock new ability → Access new area

**Dopamine Trigger**: Milestone achievement, power spike

**Design**:
- Clear next goal (XP bar, quest tracker)
- Frequent milestones (level every 15-20 min, not 2 hours)
- Tangible rewards (new skill, not just +1 stat)

**Ethical Boundary**: Not grindwall requiring payment to progress

### Social Loop (Daily)

**Example**: Join guild event → Win with team → Earn recognition (MVP award) → Social validation

**Dopamine Trigger**: Social status, belonging

**Design**:
- Daily guild activities (raid, clan war)
- Public recognition (MVP, top DPS, best healer)
- Shared rewards (whole guild gets bonus)

**Ethical Boundary**: Not toxic competition (don't pit guild members against each other)

### FOMO Loop (Time-Limited)

**Example**: Limited-time event → Exclusive reward → "Get it before it's gone!"

**Dopamine Trigger**: Loss aversion, urgency

**Design**:
- Seasonal events (Halloween, Christmas)
- Battle pass (premium rewards, time-limited)
- Rotating shop (daily deals)

**Ethical Boundary**:
- ✅ Cosmetics only (no power advantage)
- ✅ Reasonable timeframe (30 days, not 24 hours)
- ✅ Returns eventually (event cosmetics come back next year)
- ❌ Predatory pressure (fake countdown, "last chance!")
- ❌ Mandatory participation (core content locked behind event)

## Ethical Use of Cognitive Biases

### ✅ Ethical Biases (MBG-008 Compliant)

#### Loss Aversion
**Bias**: People hate losing more than they enjoy gaining

**Ethical Use**:
- Daily login streaks (but missing 1 day = 1-day setback, not total reset)
- Battle pass progression (progress carries over to next season)
- Ranked decay (slow, transparent, preventable)

**Unethical Use**:
- ❌ Durability systems (equipment breaks, pay to repair)
- ❌ Energy drain (offline = lose resources)
- ❌ Streak resets (miss 1 day = lose 30-day streak)

#### Endowment Effect
**Bias**: People value things more once they own them

**Ethical Use**:
- Free trial characters (play for 3 days, then decide to buy)
- Starter packs (free gems to experience IAP value)
- Beta access (invested players more likely to stay)

**Unethical Use**:
- ❌ Bait-and-switch (free trial ends mid-quest, pay to finish)
- ❌ Rental mechanics (temporary power, then removed)

#### Anchoring
**Bias**: First number seen becomes reference point

**Ethical Use**:
- Show "worst value" IAP first ($99.99 → $19.99 seems cheap)
- "Best value" badges on mid-tier packs
- Regional pricing (anchored to local purchasing power)

**Unethical Use**:
- ❌ Fake discounts ("90% off!" but never sold at full price)
- ❌ Misleading bundles (filler items to inflate perceived value)

### ❌ Unethical Biases (Dark Patterns)

#### Sunk Cost Fallacy
- ❌ "You've spent 100 hours, don't waste it by quitting now"
- ❌ Time-limited events after player invested money

#### Variable Ratio Schedule (Slot Machine)
- ❌ Gacha mechanics with <1% drop rates
- ❌ Loot boxes with real money (gambling)

#### Whale Exploitation
- ❌ VIP tiers requiring $1000+ spend
- ❌ Competitive advantage locked behind spending

#### Social Pressure
- ❌ "Your friends are ahead of you" notifications
- ❌ Publicly visible spending (leaderboards by $ spent)

## Validation Checklist

- [ ] All 4 Bartle types have engaging content paths
- [ ] SDT needs met: Autonomy (choice), Competence (clear feedback), Relatedness (social features)
- [ ] Dynamic difficulty keeps players in flow channel
- [ ] Dopamine loops use ethical timings (not predatory FOMO)
- [ ] Core loop fun without spending (F2P viable)
- [ ] No dark patterns (sunk cost, fake urgency, misleading pricing)
- [ ] MBG-008 compliance: Would you be proud to show this psychology to a regulatory board?
- [ ] Retention driven by fun, not addiction mechanics

## References

- **Bartle, R. (1996).** "Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs"
- **Csikszentmihalyi, M. (1990).** "Flow: The Psychology of Optimal Experience"
- **Ryan, R. M., & Deci, E. L. (2000).** "Self-Determination Theory and the Facilitation of Intrinsic Motivation"
- **Eyal, N. (2014).** "Hooked: How to Build Habit-Forming Products" (study carefully, use ethically)
- **Nodder, C. (2013).** "Evil by Design" (what NOT to do — dark patterns catalog)
- **Hopson, J. (2001).** "Behavioral Game Design" (dopamine loops in games)

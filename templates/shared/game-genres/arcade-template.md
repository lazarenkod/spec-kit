# Arcade Genre Template

**Genre**: Arcade (Reflex-Based Action)
**Core Appeal**: Fast-paced action, skill mastery, high scores
**Target Audience**: Hyper-casual gamers, reflex-driven players, score chasers

---

## Genre Profile

| Attribute | Value |
|-----------|-------|
| **Core Pattern** | Fast-paced action with increasing difficulty |
| **Session Length** | 2-5 min runs, 10-15 min total session |
| **Retention Profile** | D1: 30-40%, D7: 12-20%, D30: 4-10% |
| **Monetization Fit** | F2P-ads (primary), Hybrid (with IAP) |
| **ARPDAU Range** | $0.08-0.25 (hyper-casual), $0.15-0.40 (casual with meta) |
| **CPI Range** | $0.30-1.50 (US iOS) |
| **Development Time** | 3-5 months (hyper-casual), 6-9 months (casual with meta) |

---

## Unique Mechanics

### Core Arcade Patterns
- **Reflex-based action** — Tap/swipe to avoid obstacles, collect items
- **Infinite runner** — Endless gameplay with increasing difficulty
- **Score-based progression** — High score as primary goal
- **Procedural generation** — Levels/obstacles generated algorithmically

### Progression Mechanics
- **Increasing speed** — Game accelerates over time
- **Obstacle density** — More hazards as game progresses
- **Lives system** — Limited attempts (or single-hit death)
- **Power-ups** — Temporary boosts (shield, magnet, double points)

### Advanced Features (casual tier)
- **Character unlocks** — Unlock skins, characters with coins
- **Mission system** — Daily/weekly objectives (e.g., "Collect 100 coins")
- **Leaderboards** — Friends, global top 100
- **Seasonal events** — Limited-time themes, characters

---

## Reference Games

| Game | Revenue | Key Innovation | Learning |
|------|---------|----------------|----------|
| **Subway Surfers** | $500M+/year | Infinite runner, character collection | Character variety drives retention |
| **Temple Run** | $200M+/year | Swipe controls, 3D perspective | Pioneered mobile endless runner |
| **Crossy Road** | $100M+/year | Voxel art, charming characters | Art style differentiation |
| **Flappy Bird** | $50M (peak) | Ultra-simple, ultra-hard | Viral simplicity |

---

## Core Loop (4 Phases)

### 1. Action (Player Input)
- **Primary**: Swipe/tap to avoid obstacles
- **Secondary**: Collect coins, power-ups
- **Feedback**: Immediate death or obstacle clear
- **Error handling**: Collision = instant death (or damage)

### 2. Reward (Immediate Feedback)
- **Score increase**: Points per obstacle cleared, coin collected
- **High score**: "New Record!" celebration
- **Power-up activation**: Visual effects, temporary invincibility
- **Run summary**: Total score, coins, missions completed

### 3. Progression (Long-term Goals)
- **Coin accumulation**: Earn 50-200 coins per run
- **Character unlocks**: 500-5000 coins per character
- **Mission completion**: 3 missions = 1 key, 3 keys = prize box
- **Skill mastery**: Improve reflexes, learn patterns

### 4. Engagement (Retention Hooks)
- **Daily missions**: "Collect 50 coins", "Score 5000"
- **Character collection**: 50-100+ characters to unlock
- **Leaderboards**: Beat friends, climb global rankings
- **Limited-time events**: Seasonal characters, themed runs

---

## Monetization Strategy

### Primary Revenue: Rewarded Video Ads
- **Frequency**: 1 rewarded video per death (for revive/continue)
- **Placement**: "Continue for 100m" button on death screen
- **Expected fill rate**: 85-95%
- **eCPM**: $8-15 (US iOS)

### Secondary Revenue: Interstitial Ads
- **Frequency**: 1 interstitial per 3 deaths
- **Timing**: After death screen (not during gameplay)
- **Expected fill rate**: 70-85%
- **eCPM**: $5-10 (US iOS)

### IAP Structure (Optional)
- **Ad removal**: $2.99 (one-time purchase, 3-8% conversion)
- **Coin packs**: $0.99 (500 coins), $4.99 (3000 coins)
- **Character bundles**: $1.99-4.99 (5-pack of characters)
- **Starter pack**: $0.99 (first-time buyer incentive)

### ARPDAU Target
- **Hyper-casual** (ads only): $0.10-0.18
- **Casual** (ads + IAP): $0.18-0.40

### LTV Estimates
- **D7 LTV**: $0.80-1.50 (ad revenue)
- **D30 LTV**: $2.50-5.00 (ad revenue + IAP)
- **D180 LTV**: $5.00-12.00 (long-tail retention)

---

## Retention Mechanics

### D1 Hook (Day 1 Retention: 30-40%)
- **Instant gameplay**: No tutorial, tap to start
- **Simple controls**: Single mechanic (swipe or tap)
- **Quick deaths**: Runs end in 30s-2min (fast retry loop)
- **Early unlocks**: First character unlock at 500 coins (10 runs)
- **"Just one more run"**: Fast retry loop

### D7 Hook (Day 7 Retention: 12-20%)
- **Daily missions**: 3 missions per day, rewards
- **Character unlocks**: Unlock 3-5 characters by D7
- **Leaderboards**: Friend rankings, social pressure
- **Limited-time events**: Weekend character, theme
- **Skill improvement**: Visible progress (higher scores)

### D30 Hook (Day 30 Retention: 4-10%)
- **Character collection**: 20-30% of characters unlocked
- **Mastery challenges**: Score 10K+, survive 1000m
- **Seasonal events**: Monthly themed content
- **Community**: Discord, subreddit, fan art
- **Leaderboard climbing**: Top 100, top 10, top 1

---

## Player Psychology

### Bartle Types Distribution
- **Achievers** (60%): High scores, mission completion
- **Explorers** (10%): Discovering character abilities
- **Socializers** (10%): Leaderboards, sharing scores
- **Killers** (20%): Beating friends' scores, competition

### Self-Determination Theory (SDT)
- **Competence**: Reflex mastery, improving scores
- **Autonomy**: Choice of character (cosmetic)
- **Relatedness**: Friend leaderboards, social sharing

### Flow State
- **Easy start**: First 30s-1min are forgiving
- **Gradual acceleration**: Speed increases over time
- **Skill ceiling**: Mastery takes hours of practice
- **Frustration curve**: Hard but fair (death feels earned)

### Psychological Triggers
- **Near-miss mechanics**: "Almost beat high score!"
- **Loss aversion**: "Just 10 more coins for new character"
- **Social proof**: "Your friend scored 8000, can you beat it?"
- **Variable rewards**: Random power-up spawns

---

## Technical Requirements

### Engine
- **Recommended**: Unity (2D or 3D)
- **Alternative**: Unreal (if high-fidelity 3D needed)
- **Rationale**: Unity has strong mobile support, asset store, physics

### Backend (Minimal)
- **Required**:
  - Leaderboards (Firebase, PlayFab)
  - Analytics (GameAnalytics, Firebase)
- **Optional**:
  - Cloud save (progress backup)
  - Social features (friend system)

### Platform
- **Primary**: iOS/Android cross-platform
- **Orientation**: Portrait (primary) or Landscape
- **Resolution**: Support all aspect ratios (18:9, 19.5:9, 21:9)
- **File size**: <150MB (hyper-casual), <300MB (casual)

### Performance Targets
- **FPS**: 60 FPS on mid-tier devices (2018+ phones)
- **Load time**: <2 seconds to first playable run
- **Battery usage**: <8% drain per 30 min session

### Analytics Events
- **Critical**: run_start, run_end, death_cause, high_score
- **Monetization**: ad_impression, ad_click, iap_purchase
- **Retention**: daily_login, mission_complete, character_unlock

---

## Competitive Positioning

### Strengths (vs Reference Games)
- **Low barrier to entry**: Instant gameplay, no tutorial
- **High virality**: Easy to share scores, challenge friends
- **Low CPI**: $0.50-1.50 makes UA profitable

### Weaknesses (vs Reference Games)
- **Low D30 retention**: Hyper-casual typically retains 5-10%
- **Repetitive**: Core loop can feel samey after hours
- **Genre fatigue**: Infinite runner market saturated

### ERRC Grid (Eliminate-Reduce-Raise-Create)
- **Eliminate**: Complex tutorials, unnecessary UI
- **Reduce**: Frustration (deaths feel fair, not random)
- **Raise**: Visual polish (VFX, animations, art style)
- **Create**: Unique theme or mechanic twist

---

## Session Flow (Typical Player Journey)

### Hyper-casual Flow (2-5 min)
1. **Open app** (0s) — Immediate gameplay (no menu)
2. **Play run** (30s-2min) — Tap/swipe to play, die
3. **Watch rewarded ad** (30s) — Continue for 100m
4. **Play 2-3 more runs** (2-4 min) — Die, retry
5. **Session end** (2-5 min) — Close app naturally

### Casual Flow (10-15 min)
1. **Daily login** (5s) — Claim mission rewards
2. **Check missions** (10s) — "Collect 50 coins", etc.
3. **Play 5-10 runs** (5-10 min) — Attempt missions
4. **Unlock character** (30s) — Spend 1000 coins
5. **Check leaderboard** (1 min) — See friend rankings
6. **Session end** (10-15 min) — Close app

---

## Difficulty Curve

### Early (0-500m)
- **Speed**: Slow (base speed)
- **Obstacles**: Low density, wide gaps
- **Power-ups**: Frequent spawns (shield, magnet)
- **Survival rate**: 80-90% of runs survive to 500m

### Mid (500-1500m)
- **Speed**: Moderate (1.5x base speed)
- **Obstacles**: Medium density, narrower gaps
- **Power-ups**: Moderate spawns
- **Survival rate**: 30-50% survive to 1500m

### Late (1500-5000m)
- **Speed**: Fast (2x base speed)
- **Obstacles**: High density, tight gaps
- **Power-ups**: Rare spawns
- **Survival rate**: 10-20% survive to 5000m

### Expert (5000m+)
- **Speed**: Very fast (3x base speed)
- **Obstacles**: Maximum density, pixel-perfect timing
- **Power-ups**: Very rare
- **Survival rate**: <5% survive to 10000m

---

## Development Milestones

### Phase 1: Prototype (3-4 weeks)
- Core arcade mechanic (tap/swipe, obstacles)
- Procedural generation (basic)
- Basic UI (score, pause)
- 1-2 characters

### Phase 2: Alpha (6-8 weeks)
- Core loop polish (VFX, SFX, feedback)
- 20-30 characters
- Mission system
- Ad integration (rewarded video, interstitial)

### Phase 3: Beta (4-6 weeks)
- 50-100 characters
- Leaderboards integration
- Analytics integration
- Soft launch testing (CPI, D1 retention)

### Phase 4: Launch (2-3 weeks)
- Bug fixes from beta
- ASO optimization (keywords, screenshots, video)
- Marketing assets (trailer, ads, creatives)

---

## Risk Assessment

### High Risks
- **Low D30 retention**: Hyper-casual typically 5-10%
  - **Mitigation**: Add casual meta (missions, collections)
- **CPI volatility**: CPI can spike to $2-3 if creatives fail
  - **Mitigation**: A/B test 10+ creative variants

### Medium Risks
- **Genre saturation**: Many infinite runners on market
  - **Mitigation**: Unique art style, theme, mechanic twist
- **Ad fill rate drops**: <70% fill makes monetization unviable
  - **Mitigation**: Multiple ad networks (waterfall)

### Low Risks
- **Technical complexity**: Arcade mechanics are simple
  - **Mitigation**: Unity has proven arcade templates
- **Platform rejection**: Low risk if content age-appropriate
  - **Mitigation**: Follow App Store/Play Store guidelines

---

## Success Metrics (30 days post-launch)

| Metric | Target | Stretch Goal |
|--------|--------|--------------|
| **D1 Retention** | 35% | 45% |
| **D7 Retention** | 15% | 22% |
| **D30 Retention** | 6% | 10% |
| **CPI (US iOS)** | $1.00 | $0.60 |
| **ARPDAU** | $0.15 | $0.30 |
| **Session Length** | 6 min | 10 min |
| **Ad Impressions/DAU** | 4.0 | 6.0 |
| **IAP Conversion** | 4% | 8% |

---

## Example Concept (Arcade Genre)

**Game Title**: "Neon Rush: Cyber Runner"

**Vision**: A cyberpunk infinite runner where players control a hacker fleeing through neon-lit cityscapes. Swipe to change lanes, tap to hack obstacles (convert to power-ups). Unlock 100+ cyberpunk characters (hackers, androids, cyborgs).

**Unique Twist**: Hack mechanic — tap obstacles to convert them to power-ups (limited uses per run). Adds strategic layer to reflex gameplay.

**Monetization**: Hybrid model — rewarded ads for revive/continue, IAP for ad removal ($2.99) and character packs ($1.99-4.99).

**Target Audience**: Hyper-casual gamers 15-35, cyberpunk fans, reflex-driven players.

**CQS-Game Estimate**: 86/120 (strong Mechanics, Tech Feasibility; moderate Market due to saturation, good Innovation from hack mechanic)

---

## Genre Compliance Checklist (Required for CQS-Game v2.0 Validation)

### Core Mechanics (Must-Have)
- [ ] Reflex-based action (tap/swipe to avoid obstacles, collect items)
- [ ] Increasing difficulty (speed/obstacle density increases over time)
- [ ] Score-based progression (high score as primary goal)
- [ ] Procedural generation (levels/obstacles generated algorithmically)

### Retention Mechanics (Must-Have)
- [ ] Daily missions (collect X coins, score Y, survive Z distance)
- [ ] Character unlocks (50-100+ characters with coins)
- [ ] Leaderboards (friend rankings OR global top 100)

### Monetization (Must-Have for F2P)
- [ ] Ads: Rewarded video (revive/continue after death, 1 per death)
- [ ] Ads: Interstitial ads (1 per 3-5 deaths, after death screen)
- [ ] IAP: Ad removal ($2.99), Coin packs ($0.99-4.99), Character bundles ($1.99-4.99)

### Nice-to-Have (Premium Tier)
- [ ] Mission system (daily/weekly objectives with rewards)
- [ ] Seasonal events (limited-time themes, characters)
- [ ] Social features (friend leaderboards, social sharing)
- [ ] Power-ups (shield, magnet, double points)

### Red Flags (Avoid)
- ❌ Impossible difficulty without IAP (player skill irrelevant) → GAM-004 violation
- ❌ Forced ads mid-run (interrupts gameplay flow) → User frustration
- ❌ No retry loop (slow retry = broken core loop) → Genre expectation violation
- ❌ Pay-to-win power-ups (must spend to compete) → GAM-004 violation

**Validation Logic** (for concept-quality-validator):
- Core mechanics: 100% compliance required
- Retention mechanics: ≥80% required
- Monetization: ≥80% if F2P model
- Genre Fit Score = (Must-Have compliance + Nice-to-Have compliance) / 2
- **Target**: ≥80% for QG-GCONCEPT-002 pass

---

## Related Templates

- **Sorting**: templates/shared/game-genres/sorting-template.md
- **Match-3**: templates/shared/game-genres/match3-template.md
- **Idle**: templates/shared/game-genres/idle-template.md
- **Puzzle**: templates/shared/game-genres/puzzle-template.md

---

**Last Updated**: 2026-01-13
**Version**: 1.0.0

# Match-3 Genre Template

**Genre**: Match-3 (Cascading Combos)
**Core Appeal**: Satisfying matches, cascades, strategic combos
**Target Audience**: Casual mobile gamers, puzzle enthusiasts, progression-driven players

---

## Genre Profile

| Attribute | Value |
|-----------|-------|
| **Core Pattern** | Match 3+ items to clear board and achieve objectives |
| **Session Length** | 10-15 min (casual), 15-20 min (mid-core with meta) |
| **Retention Profile** | D1: 40-50%, D7: 20-30%, D30: 8-15% |
| **Monetization Fit** | Hybrid (IAP + ads), F2P-IAP (mid-core) |
| **ARPDAU Range** | $0.20-0.50 (casual), $0.50-1.50 (mid-core) |
| **CPI Range** | $1.50-4.00 (US iOS) |
| **Development Time** | 6-9 months (casual), 9-12 months (mid-core with meta) |

---

## Unique Mechanics

### Core Match-3 Patterns
- **Match-3+ items** — Primary mechanic (swap or tap to match)
- **Cascading combos** — Matches trigger new pieces falling
- **Power-ups** — Special pieces from 4+, 5+ matches
- **Board objectives** — Clear X items, reach Y score, collect Z resources

### Progression Mechanics
- **Increasing difficulty** — More objectives, blockers, limited moves
- **Move limits** — Finite attempts per level (vs infinite)
- **Lives system** — 5 lives, regenerate 1 per 30 min (standard)
- **Boosters** — Pre-level boosters (hammer, shuffle, extra moves)

### Advanced Features (mid-core tier)
- **Meta game** — Build/restore town, garden, mansion
- **Narrative** — Story progression tied to levels
- **Characters** — Unlockable characters with unique abilities
- **Events** — Limited-time tournaments, challenges
- **Social** — Lives gifting, leaderboards, team play

---

## Reference Games

| Game | Revenue | Key Innovation | Learning |
|------|---------|----------------|----------|
| **Candy Crush Saga** | $1B+/year | Lives system, social virality | King of Match-3, hard to beat |
| **Homescapes** | $500M+/year | Meta game (mansion restoration) | Meta drives retention |
| **Gardenscapes** | $500M+/year | Narrative + meta game | Story hooks players |
| **Toon Blast** | $300M+/year | Team-based play, no energy | Social + no energy = high retention |

---

## Core Loop (4 Phases)

### 1. Action (Player Input)
- **Primary**: Swap adjacent pieces to match 3+
- **Secondary**: Tap boosters, activate power-ups
- **Feedback**: Visual explosion, cascade animation
- **Error handling**: Invalid swaps bounce back

### 2. Reward (Immediate Feedback)
- **Match effects**: Particles, sound effects, haptic feedback
- **Cascade bonuses**: Extra points for chain reactions
- **Power-up creation**: 4+ match creates rocket, 5+ match creates bomb
- **Level completion**: Stars (1-3), coins, boosters

### 3. Progression (Long-term Goals)
- **Level unlocks**: 1000+ levels in progression map
- **Meta game**: Restore mansion, build garden, complete story
- **Character unlocks**: New avatars with passive bonuses
- **Difficulty tiers**: Easy → Medium → Hard → Expert

### 4. Engagement (Retention Hooks)
- **Daily challenges**: Special levels with bonus rewards
- **Lives system**: 5 lives, gifting from friends
- **Limited-time events**: Weekend tournaments, seasonal challenges
- **Team play**: Join teams, compete in team events
- **Leaderboards**: Friends, team, global rankings

---

## Monetization Strategy

### Primary Revenue: In-App Purchases
- **Lives refill**: $0.99 (5 lives immediately)
- **Boosters**: $1.99-4.99 (bundles of hammers, shuffle, extra moves)
- **Gold bars**: $4.99 (50 bars), $9.99 (120 bars), $19.99 (300 bars)
- **Starter packs**: $0.99 (first-time buyer incentive)
- **VIP pass**: $9.99/month (unlimited lives, daily boosters, no ads)

### Secondary Revenue: Rewarded Video Ads
- **Frequency**: 1 rewarded video per failed level (for extra moves)
- **Placement**: "Get 5 more moves" button on level fail
- **Expected fill rate**: 85-95%
- **eCPM**: $10-20 (US iOS)

### Tertiary Revenue: Interstitial Ads (optional)
- **Frequency**: 1 interstitial per 10 levels (only for non-payers)
- **Timing**: After level completion
- **Expected fill rate**: 60-75%
- **eCPM**: $5-10 (US iOS)

### ARPDAU Target
- **Casual** (low IAP): $0.20-0.35
- **Mid-core** (high IAP): $0.50-1.50

### LTV Estimates
- **D7 LTV**: $2.00-5.00 (early IAP conversion)
- **D30 LTV**: $8.00-20.00 (mid-game monetization)
- **D180 LTV**: $30.00-80.00 (whale retention)

---

## Retention Mechanics

### D1 Hook (Day 1 Retention: 40-50%)
- **Instant fun**: Satisfying match-3 mechanics from level 1
- **Easy onboarding**: First 10 levels are tutorial-lite (≤5 min)
- **Early rewards**: Free boosters, coins, first character unlock
- **Meta game intro**: Show mansion/garden at level 5-10
- **Social prompts**: Connect to Facebook for lives (optional)

### D7 Hook (Day 7 Retention: 20-30%)
- **Daily login rewards**: Day 1: coins, Day 7: booster bundle
- **Lives gifting**: Request/send lives from friends (F2P lives source)
- **Meta game milestones**: Complete first room/area (visible progress)
- **Events introduction**: First limited-time event at D3-D5
- **Team play**: Join a team at level 20-30 (social retention)

### D30 Hook (Day 30 Retention: 8-15%)
- **Deep meta progression**: Mansion/garden 30-50% complete
- **Character collection**: Unlock 3-5 characters with abilities
- **Seasonal events**: Monthly tournaments, holiday themes
- **Team competitions**: Weekly team challenges, rewards
- **Narrative payoffs**: Story milestones every 50-100 levels

---

## Player Psychology

### Bartle Types Distribution
- **Achievers** (60%): 3-star ratings, level completion, meta progress
- **Explorers** (15%): Discovering power-up combos, meta secrets
- **Socializers** (20%): Team play, lives gifting, leaderboards
- **Killers** (5%): Tournament competition, team rankings

### Self-Determination Theory (SDT)
- **Competence**: Mastery of combos, strategic play
- **Autonomy**: Choice of which meta task to complete next
- **Relatedness**: Team membership, lives gifting, social features

### Flow State
- **Easy start**: Levels 1-30 have generous move limits
- **Gradual difficulty**: Introduce blockers, objectives every 10 levels
- **Skill ceiling**: Optimal play requires combo planning
- **Difficulty spikes**: "Hard levels" every 20-30 levels (monetization gates)

### Psychological Triggers
- **Near-miss mechanics**: "Almost won, just 1 more move!"
- **Loss aversion**: Lives system creates urgency
- **Collection completion**: "Just 2 more characters to unlock"
- **Social pressure**: "Your friend beat this level, can you?"

---

## Technical Requirements

### Engine
- **Recommended**: Unity (2D)
- **Alternative**: Cocos2d-x, proprietary engine (for performance)
- **Rationale**: Unity has strong 2D support, asset store, cross-platform

### Backend (Moderate)
- **Required**:
  - Lives system (server-authoritative timing)
  - Leaderboards (Firebase, PlayFab, custom)
  - Team system (matchmaking, chat)
  - Meta game sync (cloud save)
  - Analytics (GameAnalytics, Firebase)
- **Optional**:
  - PvP tournaments (matchmaking, brackets)
  - Replay system (share solutions)

### Platform
- **Primary**: iOS/Android cross-platform
- **Orientation**: Portrait (primary), Landscape (alternative)
- **Resolution**: Support all aspect ratios (18:9, 19.5:9, 21:9)
- **File size**: <300MB (casual), <500MB (mid-core with assets)

### Performance Targets
- **FPS**: 60 FPS on mid-tier devices (2018+ phones)
- **Load time**: <5 seconds to level select
- **Battery usage**: <8% drain per 30 min session

### Analytics Events
- **Critical**: level_start, level_complete, level_fail, level_attempts
- **Monetization**: iap_purchase, ad_impression, booster_used
- **Retention**: daily_login, lives_gifted, team_joined
- **Meta**: meta_task_complete, character_unlock, event_participate

---

## Competitive Positioning

### Strengths (vs Reference Games)
- **Proven genre**: Match-3 has 10+ years of proven success
- **Broad appeal**: Accessible to all ages, demographics
- **Deep monetization**: Lives + boosters + meta = high LTV

### Weaknesses (vs Reference Games)
- **High competition**: King, Playrix dominate Top Grossing
- **High CPI**: $2-4 CPI makes UA challenging
- **Long development**: 9-12 months for competitive quality

### ERRC Grid (Eliminate-Reduce-Raise-Create)
- **Eliminate**: Complex tutorials, unnecessary UI
- **Reduce**: Monetization pressure (vs Candy Crush)
- **Raise**: Meta game quality (Homescapes level)
- **Create**: Unique theme (e.g., underwater, space, fantasy)

---

## Session Flow (Typical Player Journey)

### Casual Flow (10-15 min)
1. **Open app** (5s) — Daily login bonus popup
2. **Claim rewards** (10s) — Day X reward, check lives (5/5)
3. **Play main levels** (5-8 min) — Attempt 3-5 levels, fail 1-2
4. **Use booster** (30s) — Buy extra moves ($0.99) or watch rewarded ad
5. **Complete meta task** (2-3 min) — Restore 1 room in mansion
6. **Check team** (1 min) — See team progress, chat
7. **Session end** (10-15 min) — Lives depleted (2/5 remaining)

### Mid-core Flow (15-20 min)
1. **Daily login bonus** (10s) — Claim streak reward
2. **Play daily challenge** (3 min) — Special level, bonus reward
3. **Main progression** (8-12 min) — Play 5-10 levels
4. **Meta game tasks** (3-5 min) — Complete 2-3 mansion rooms
5. **Team event** (2-3 min) — Contribute to team tournament
6. **Optional: IAP** (1-2 min) — Buy booster pack if stuck
7. **Session end** (15-20 min) — Lives depleted, return in 30 min

---

## Difficulty Curve

### Beginner (Levels 1-50)
- **Objectives**: Simple (clear X pieces, reach Y score)
- **Blockers**: None or minimal (1-2 types)
- **Moves**: Generous (25-30 moves per level)
- **Failure rate**: 10-20% (easy wins to build confidence)

### Intermediate (Levels 51-200)
- **Objectives**: Multi-objective (clear X + collect Y)
- **Blockers**: 3-5 types (ice, chains, locked pieces)
- **Moves**: Moderate (20-25 moves)
- **Failure rate**: 30-40% (some challenge)

### Advanced (Levels 201-500)
- **Objectives**: Complex (3+ objectives, order matters)
- **Blockers**: 5-10 types (cascading blockers)
- **Moves**: Limited (15-20 moves)
- **Failure rate**: 50-60% (significant challenge)

### Expert (Levels 501+)
- **Objectives**: "Hard levels" every 10-20 levels
- **Blockers**: All types, tight spaces
- **Moves**: Strict (12-18 moves)
- **Failure rate**: 70-80% on hard levels (monetization gates)

---

## Development Milestones

### Phase 1: Prototype (6-8 weeks)
- Core match-3 mechanic (swap, match, cascade)
- 20 levels for testing
- Basic UI (level select, pause, settings)
- Power-ups (rocket, bomb, rainbow)

### Phase 2: Alpha (12-16 weeks)
- 200 levels with progression
- Core loop polish (VFX, SFX, feedback)
- Lives system + boosters
- Meta game prototype (1-2 rooms)
- Analytics integration

### Phase 3: Beta (8-12 weeks)
- 500 levels total
- Full meta game (10-20 rooms)
- Daily challenges, events system
- Team play (basic)
- Soft launch testing (D1/D7/D30, LTV)

### Phase 4: Launch (4-6 weeks)
- 1000 levels ready (or level generator)
- Bug fixes from beta
- ASO optimization (keywords, screenshots, video)
- Marketing assets (trailer, ads, creatives)

---

## Risk Assessment

### High Risks
- **Competition from King**: Candy Crush dominates genre
  - **Mitigation**: Unique theme, superior meta game, team play focus
- **High CPI**: $3-4 CPI makes profitability challenging
  - **Mitigation**: Optimize creatives, test A/B, regional targeting

### Medium Risks
- **Low D7 retention**: Genre average 20-25%, needs meta game
  - **Mitigation**: Invest in meta game quality (Homescapes level)
- **Development complexity**: 9-12 months, $300K-500K budget
  - **Mitigation**: Phased launch, early soft launch testing

### Low Risks
- **Technical complexity**: Match-3 is well-understood genre
  - **Mitigation**: Unity has proven match-3 asset templates
- **Platform rejection**: Low risk if content age-appropriate
  - **Mitigation**: Follow App Store/Play Store guidelines

---

## Success Metrics (30 days post-launch)

| Metric | Target | Stretch Goal |
|--------|--------|--------------|
| **D1 Retention** | 45% | 55% |
| **D7 Retention** | 23% | 30% |
| **D30 Retention** | 10% | 15% |
| **CPI (US iOS)** | $3.00 | $2.00 |
| **ARPDAU** | $0.40 | $0.80 |
| **Session Length** | 12 min | 18 min |
| **IAP Conversion** | 4% | 8% |
| **D7 LTV / CPI** | 1.5x | 2.5x |

---

## Example Concept (Match-3 Genre)

**Game Title**: "Garden Saga: Match & Restore"

**Vision**: A match-3 puzzle game where players restore a neglected Victorian garden to its former glory. Each level completed unlocks garden restoration tasks (plant flowers, rebuild fountains, unlock new areas). Narrative follows a character inheriting their grandmother's estate.

**Unique Twist**: Seasonal garden transformations (Spring blooms, Summer harvest, Fall colors, Winter snow). Players vote on which areas to restore next (community-driven content).

**Monetization**: Hybrid model — IAP for lives/boosters ($0.99-9.99), optional VIP pass ($9.99/month for unlimited lives + daily boosters).

**Target Audience**: Casual mobile gamers 30-50, match-3 fans, gardening enthusiasts, story-driven players.

**CQS-Game Estimate**: 92/120 (strong Market, Mechanics, Monetization, Retention; high competition but differentiated)

---

## Genre Compliance Checklist (Required for CQS-Game v2.0 Validation)

### Core Mechanics (Must-Have)
- [ ] Match-3+ core pattern (swap adjacent, match 3+ same color)
- [ ] Lives system OR energy system (F2P monetization hook)
- [ ] Booster system (3-8 booster types for IAP)
- [ ] Level-based progression (50-200+ levels)

### Retention Mechanics (Must-Have)
- [ ] Daily login bonuses (streak system)
- [ ] Limited lives (5 lives, 30-min refill) OR energy (100 energy, 1/min refill)
- [ ] Social features (friend leaderboard OR guild)

### Monetization (Must-Have for F2P)
- [ ] IAP: Extra moves ($0.99), Booster packs ($1.99-4.99)
- [ ] IAP: Lives refill ($0.99 for 5 lives) OR Unlimited lives ($9.99/month)
- [ ] Ads: Rewarded video (2x rewards, extra lives)

### Nice-to-Have (Premium Tier)
- [ ] Meta game (restore mansion, build garden, unlock areas)
- [ ] Narrative (story unlocks with progression)
- [ ] Character collection (unlock heroes with unique abilities)
- [ ] Events (weekly tournaments, seasonal levels)

### Red Flags (Avoid)
- ❌ No lives/energy system (no monetization hook for F2P)
- ❌ Pay-to-win (levels impossible without IAP) → GAM-004 violation
- ❌ Predatory ads (forced interstitials every level) → GAM-004 violation
- ❌ Overly aggressive difficulty spikes (frustration without skill improvement)

**Validation Logic** (for concept-quality-validator):
- Core mechanics: 100% compliance required
- Retention mechanics: ≥80% required
- Monetization: ≥80% if F2P model
- Genre Fit Score = (Must-Have compliance + Nice-to-Have compliance) / 2
- **Target**: ≥80% for QG-GCONCEPT-002 pass

---

## Related Templates

- **Sorting**: templates/shared/game-genres/sorting-template.md
- **Idle**: templates/shared/game-genres/idle-template.md
- **Arcade**: templates/shared/game-genres/arcade-template.md
- **Puzzle**: templates/shared/game-genres/puzzle-template.md

---

**Last Updated**: 2026-01-13
**Version**: 1.0.0

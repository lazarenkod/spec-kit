# Sorting Genre Template

**Genre**: Sorting (Order from Chaos)
**Core Appeal**: Satisfying organization, visual clarity, completionist satisfaction
**Target Audience**: Casual mobile gamers, stress relief seekers, puzzle enthusiasts

---

## Genre Profile

| Attribute | Value |
|-----------|-------|
| **Core Pattern** | Organize items by attribute (color, shape, size, type) |
| **Session Length** | 2-5 min (hyper-casual), 10-15 min (casual with meta) |
| **Retention Profile** | D1: 35-45%, D7: 15-25%, D30: 5-10% |
| **Monetization Fit** | F2P-ads (primary), Hybrid (with IAP) |
| **ARPDAU Range** | $0.05-0.20 (hyper-casual), $0.10-0.30 (casual with meta) |
| **CPI Range** | $0.50-2.00 (US iOS) |
| **Development Time** | 2-3 months (hyper-casual), 4-6 months (casual) |

---

## Unique Mechanics

### Core Sorting Patterns
- **Drag-and-drop sorting** — Primary interaction (touch-based)
- **Category-based organization** — Group by color, shape, size, type
- **Spatial arrangement** — Physical organization of objects in 3D/2D space
- **Completion criteria** — All items sorted correctly

### Progression Mechanics
- **Increasing complexity** — More items, more categories, less space
- **Combo multipliers** — Speed sorting bonuses
- **Time pressure vs zen mode** — Toggle between timed challenges and relaxed play
- **Hint/undo systems** — Help mechanics for stuck players

### Advanced Features (casual tier)
- **Themed collections** — Unlock new item sets (kitchen, office, fantasy)
- **Customization** — Personalize containers, backgrounds
- **Daily challenges** — Special sorting puzzles
- **Leaderboards** — Speed sorting competition

---

## Reference Games

| Game | Revenue | Key Innovation | Learning |
|------|---------|----------------|----------|
| **Sort It 3D** | $50M+ (est.) | 3D physics-based sorting | Satisfying tactile feedback |
| **Goods Sort** | $30M+ (est.) | Household item theming | Relatable objects boost engagement |
| **Water Sort Puzzle** | $100M+ (est.) | Liquid physics simulation | Simple concept, deep complexity |
| **Tangle Master 3D** | $20M+ (est.) | Rope untangling mechanic | Spatial reasoning challenge |

---

## Core Loop (4 Phases)

### 1. Action (Player Input)
- **Primary**: Drag items to containers/zones
- **Secondary**: Tap to select, swipe to sort
- **Feedback**: Haptic response on correct placement
- **Error handling**: Visual shake on wrong placement

### 2. Reward (Immediate Feedback)
- **Visual satisfaction**: Order from chaos animation
- **Score increase**: Points per correct placement
- **Star rating**: 1-3 stars per level completion
- **Celebration effects**: Confetti, sparkles, sound effects

### 3. Progression (Long-term Goals)
- **Level unlocks**: 50-100+ levels in progression
- **New items**: Unlock thematic collections
- **Difficulty increase**: More items, categories, constraints
- **Meta progression**: Unlock zen mode, time attack mode

### 4. Engagement (Retention Hooks)
- **Daily challenges**: Special puzzles with bonus rewards
- **Streak bonuses**: Login rewards for consecutive days
- **Leaderboards**: Friend rankings, global top 100
- **Limited-time events**: Seasonal themes (holidays, seasons)

---

## Monetization Strategy

### Primary Revenue: Rewarded Video Ads
- **Frequency**: 1 rewarded video per 3 levels (for hints/extra moves)
- **Placement**: Between levels, on hint button
- **Expected fill rate**: 85-95%
- **eCPM**: $8-15 (US iOS)

### Secondary Revenue: Interstitial Ads
- **Frequency**: 1 interstitial per 5 levels
- **Timing**: After level completion (not during gameplay)
- **Expected fill rate**: 70-85%
- **eCPM**: $5-10 (US iOS)

### IAP Structure (Optional)
- **Ad removal**: $2.99 (one-time purchase, 5-10% conversion)
- **Hint packs**: $0.99 (10 hints), $4.99 (100 hints)
- **Theme bundles**: $1.99-4.99 (cosmetic collections)
- **Energy refills**: $0.99 (if energy system used)

### ARPDAU Target
- **Hyper-casual** (ads only): $0.08-0.15
- **Casual** (ads + IAP): $0.15-0.30

### LTV Estimates
- **D7 LTV**: $0.50-1.00 (ad revenue)
- **D30 LTV**: $1.50-3.00 (ad revenue + IAP)
- **D180 LTV**: $3.00-8.00 (long-tail retention)

---

## Retention Mechanics

### D1 Hook (Day 1 Retention: 35-45%)
- **Instant gratification**: Immediate satisfaction from sorting
- **Smooth onboarding**: Tutorial in first 3 levels (≤60 seconds)
- **Early wins**: Easy levels to build confidence
- **Feedback loops**: Visual/audio rewards on every action
- **"Just one more level"**: Short sessions encourage replays

### D7 Hook (Day 7 Retention: 15-25%)
- **Daily challenges**: Unique puzzles with bonus rewards
- **Streak bonuses**: Login rewards (coins, hints, themes)
- **Progression milestones**: Unlock zen mode after 20 levels
- **Social features**: Friend leaderboards, share progress
- **Content updates**: New levels weekly (if casual tier)

### D30 Hook (Day 30 Retention: 5-10%)
- **Themed events**: Seasonal content (Halloween, Christmas, etc.)
- **Collection completion**: 100% completionist goals
- **Mastery challenges**: Speed sorting, perfect runs
- **Community engagement**: Discord, Facebook group
- **Meta progression**: Unlock all themes, zen mode mastery

---

## Player Psychology

### Bartle Types Distribution
- **Achievers** (70%): Completionist satisfaction, 3-star ratings
- **Explorers** (20%): Discovering new item themes, mechanics
- **Socializers** (5%): Leaderboards, sharing progress
- **Killers** (5%): Speed sorting competition, time attack

### Self-Determination Theory (SDT)
- **Competence**: Mastery of sorting patterns, improving speed
- **Autonomy**: Choice between zen mode (untimed) and time attack
- **Relatedness**: Friend leaderboards, social sharing

### Flow State
- **Easy start**: First 10 levels tutorial-like
- **Gradual difficulty**: Increase items/categories every 5-10 levels
- **Skill ceiling**: Speed sorting creates high-skill mastery
- **Zen mode**: Remove time pressure for relaxation

### Psychological Triggers
- **Completion bias**: Urge to finish organizing
- **Visual clarity**: Satisfaction of organized space
- **ASMR-like appeal**: Relaxing, repetitive actions
- **Stress relief**: Meditative gameplay

---

## Technical Requirements

### Engine
- **Recommended**: Unity (2D/3D hybrid)
- **Alternative**: Unreal (if high-fidelity 3D needed)
- **Rationale**: Unity has strong mobile support, asset store, physics

### Backend (Minimal)
- **Required**:
  - Leaderboards (Firebase, PlayFab)
  - Daily challenge sync (if online)
  - Analytics (GameAnalytics, Firebase)
- **Optional**:
  - Cloud save (progress backup)
  - Social features (friend system)

### Platform
- **Primary**: iOS/Android cross-platform
- **Orientation**: Portrait (single-handed play)
- **Resolution**: Support all aspect ratios (18:9, 19.5:9, 21:9)
- **File size**: <150MB (hyper-casual), <300MB (casual)

### Performance Targets
- **FPS**: 60 FPS on mid-tier devices (2018+ phones)
- **Load time**: <3 seconds to first playable level
- **Battery usage**: <5% drain per 30 min session

### Analytics Events
- **Critical**: level_start, level_complete, level_fail
- **Monetization**: ad_impression, ad_click, iap_purchase
- **Retention**: daily_login, streak_milestone, theme_unlock

---

## Competitive Positioning

### Strengths (vs Reference Games)
- **Accessible**: Easier than Water Sort (no liquid physics complexity)
- **Relatable**: More relatable than abstract puzzles
- **Flexible**: Can theme to any setting (kitchen, office, fantasy)

### Weaknesses (vs Reference Games)
- **Lower virality**: Less "wow" factor than 3D physics games
- **Genre saturation**: Many sorting games on market
- **Limited depth**: Hard to add meta progression

### ERRC Grid (Eliminate-Reduce-Raise-Create)
- **Eliminate**: Complex tutorials, unnecessary UI clutter
- **Reduce**: Number of taps (optimize for drag-and-drop)
- **Raise**: Visual satisfaction (polish animations, haptics)
- **Create**: Zen mode toggle (time attack vs relaxation)

---

## Session Flow (Typical Player Journey)

### Hyper-casual Flow (2-5 min)
1. **Open app** (0s) — Immediate level select
2. **Play level** (30s-60s) — Sort items, see ad after 3 levels
3. **Watch rewarded ad** (30s) — Get hint or extra moves
4. **Play 2-3 more levels** (1-2 min) — Continue progression
5. **Session end** (2-5 min) — Close app naturally

### Casual Flow (10-15 min)
1. **Daily login bonus** (5s) — Claim streak reward
2. **Play daily challenge** (2 min) — Special puzzle
3. **Main progression** (5-10 min) — Play 5-10 levels
4. **Check leaderboards** (30s) — Compare with friends
5. **Optional: IAP browse** (1-2 min) — Browse new themes
6. **Session end** (10-15 min) — Save progress, close

---

## Difficulty Curve

### Beginner (Levels 1-20)
- **Items**: 5-10 items
- **Categories**: 2-3 categories
- **Constraints**: None
- **Time limit**: None (zen mode default)

### Intermediate (Levels 21-50)
- **Items**: 10-20 items
- **Categories**: 3-5 categories
- **Constraints**: Limited space, some locked slots
- **Time limit**: Optional time attack mode

### Advanced (Levels 51-100)
- **Items**: 20-30 items
- **Categories**: 5-7 categories
- **Constraints**: Physics-based, moving objects
- **Time limit**: Time pressure increases

### Expert (Levels 100+)
- **Items**: 30-50 items
- **Categories**: 7-10 categories
- **Constraints**: Complex rules (sort by 2 attributes)
- **Time limit**: Speed sorting challenges

---

## Development Milestones

### Phase 1: Prototype (2-4 weeks)
- Core sorting mechanic (drag-and-drop)
- 10 levels for testing
- Basic UI (level select, pause)

### Phase 2: Alpha (4-6 weeks)
- 50 levels with progression
- Core loop polish (animations, feedback)
- Ad integration (rewarded video, interstitial)

### Phase 3: Beta (2-4 weeks)
- 100 levels total
- Daily challenges system
- Analytics integration
- Soft launch testing (CPI, D1 retention)

### Phase 4: Launch (1-2 weeks)
- Bug fixes from beta
- ASO optimization (keywords, screenshots)
- Marketing assets (trailer, ads)

---

## Risk Assessment

### High Risks
- **Genre saturation**: Many sorting games already exist
  - **Mitigation**: Unique theme, superior polish, zen mode toggle
- **Low D7 retention**: Hyper-casual typically retains 15-20%
  - **Mitigation**: Add casual meta progression (themes, collections)

### Medium Risks
- **CPI too high**: $2+ makes user acquisition unprofitable
  - **Mitigation**: Optimize creatives, test regional targeting
- **Ad fill rate drops**: <70% fill makes monetization unviable
  - **Mitigation**: Multiple ad networks (waterfall), test ad providers

### Low Risks
- **Technical complexity**: Sorting mechanic is simple
  - **Mitigation**: Unity has strong mobile physics support
- **Platform rejection**: Low risk of App Store/Play Store issues
  - **Mitigation**: Follow guidelines, age-appropriate content

---

## Success Metrics (30 days post-launch)

| Metric | Target | Stretch Goal |
|--------|--------|--------------|
| **D1 Retention** | 40% | 50% |
| **D7 Retention** | 18% | 25% |
| **D30 Retention** | 7% | 12% |
| **CPI (US iOS)** | $1.50 | $1.00 |
| **ARPDAU** | $0.12 | $0.20 |
| **Session Length** | 4 min | 6 min |
| **Ad Impressions/DAU** | 3.5 | 5.0 |
| **IAP Conversion** | 2% | 5% |

---

## Example Concept (Sorting Genre)

**Game Title**: "Sort Haven"

**Vision**: A zen puzzle game where players organize chaotic household items into satisfying order. Inspired by Marie Kondo's "Tidying Up," Sort Haven offers two modes: Time Attack for competitive players and Zen Mode for relaxation.

**Unique Twist**: Themed rooms (Kitchen, Office, Garage, Garden) with realistic 3D objects. Players unlock new rooms by completing collections.

**Monetization**: Hybrid model — rewarded ads for hints, IAP for ad removal ($2.99) and premium room themes ($1.99 each).

**Target Audience**: Casual mobile gamers 25-45, stress relief seekers, fans of ASMR/organization content.

**CQS-Game Estimate**: 88/120 (strong Market, Mechanics, Retention; moderate Viral Potential, Innovation)

---

## Genre Compliance Checklist (Required for CQS-Game v2.0 Validation)

### Core Mechanics (Must-Have)
- [ ] Drag-and-drop OR tap-to-sort interaction (primary control scheme)
- [ ] Category-based organization (color, shape, size, type)
- [ ] Clear completion criteria (all items sorted correctly)
- [ ] Visual feedback on correct/incorrect placement

### Retention Mechanics (Must-Have)
- [ ] Progression system (unlock new themes, levels, or item sets)
- [ ] Daily challenges OR streak system (login incentive)
- [ ] Combo multipliers OR speed bonuses (skill expression)

### Monetization (Must-Have for F2P)
- [ ] IAP: Remove ads ($2.99), OR hint packs ($0.99-1.99)
- [ ] Ads: Rewarded video (2x rewards, extra hints)
- [ ] Ads: Interstitial ads (1 per 5 levels, max)

### Nice-to-Have (Premium Tier)
- [ ] Zen mode (no time pressure, relaxation focus)
- [ ] Themed collections (kitchen, office, fantasy, seasonal)
- [ ] Customization (containers, backgrounds, item skins)
- [ ] Leaderboards (speed sorting, fewest moves)

### Red Flags (Avoid)
- ❌ Forced wait timers (anti-pattern for zen sorting genre)
- ❌ Pay-to-win mechanics (impossible levels without IAP) → GAM-004 violation
- ❌ Excessive interstitial ads (>1 per 3 levels) → User frustration
- ❌ Overly complex sorting rules (cognitive overload for hyper-casual)

**Validation Logic** (for concept-quality-validator):
- Core mechanics: 100% compliance required
- Retention mechanics: ≥80% required
- Monetization (F2P): ≥80% required
- Genre Fit Score = (Must-Have compliance + Nice-to-Have compliance) / 2
- **Target**: ≥80% for QG-GCONCEPT-002 pass

---

## Related Templates

- **Match-3**: templates/shared/game-genres/match3-template.md
- **Idle**: templates/shared/game-genres/idle-template.md
- **Arcade**: templates/shared/game-genres/arcade-template.md
- **Puzzle**: templates/shared/game-genres/puzzle-template.md

---

**Last Updated**: 2026-01-13
**Version**: 1.0.0

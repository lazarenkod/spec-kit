# Puzzle Genre Template

**Genre**: Puzzle (Logic & Spatial Reasoning)
**Core Appeal**: Intellectual challenge, "aha!" moments, elegant solutions
**Target Audience**: Puzzle enthusiasts, premium indie game fans, strategic thinkers

---

## Genre Profile

| Attribute | Value |
|-----------|-------|
| **Core Pattern** | Solve increasingly complex puzzles using logic or spatial reasoning |
| **Session Length** | 5-10 min per puzzle, 20-30 min total session |
| **Retention Profile** | D1: 35-45%, D7: 18-28%, D30: 8-15% |
| **Monetization Fit** | Premium (paid download), Hybrid (F2P + IAP), F2P-ads |
| **ARPDAU Range** | $0.05-0.15 (F2P-ads), $0.15-0.40 (hybrid), N/A (premium) |
| **CPI Range** | $1.50-4.00 (US iOS) |
| **Development Time** | 6-12 months (indie), 12-24 months (AAA quality) |

---

## Unique Mechanics

### Core Puzzle Patterns
- **Logic-based** — Deduce solution from rules (e.g., Sudoku)
- **Spatial reasoning** — Manipulate objects in space (e.g., Monument Valley)
- **Physics-based** — Use physics to solve (e.g., Cut the Rope)
- **Narrative-driven** — Puzzles advance story (e.g., The Room)

### Progression Mechanics
- **Mechanic introduction** — Introduce 1 new mechanic every 5-10 levels
- **Difficulty curve** — Gradual increase in complexity
- **Hint system** — Optional hints (F2P: watch ad, premium: unlimited)
- **Undo/reset** — Allow players to experiment without penalty

### Advanced Features (premium tier)
- **Narrative** — Story unfolds through puzzle completion
- **Art direction** — Unique visual style (isometric, hand-drawn, etc.)
- **Ambient audio** — Relaxing music, ASMR-like sound design
- **Level editor** — User-generated content (optional)

---

## Reference Games

| Game | Revenue | Key Innovation | Learning |
|------|---------|----------------|----------|
| **Monument Valley** | $30M+ | Isometric illusions, art direction | Premium puzzle can be profitable |
| **The Room** | $50M+ | Physical puzzle boxes, tactile | Tactile interaction boosts engagement |
| **Cut the Rope** | $100M+ | Physics-based, cute character | Character-driven puzzles work |
| **Brain It On!** | $20M+ | User-generated content | UGC extends content lifespan |

---

## Core Loop (4 Phases)

### 1. Action (Player Input)
- **Primary**: Manipulate objects, test hypotheses
- **Secondary**: Use hints if stuck
- **Feedback**: Immediate validation (correct/incorrect)
- **Error handling**: Undo/reset freely

### 2. Reward (Immediate Feedback)
- **"Aha!" moment**: Satisfaction of discovering solution
- **Visual feedback**: Puzzle completion animation
- **Star rating**: 1-3 stars (optional objectives)
- **Story progression**: Unlock next chapter

### 3. Progression (Long-term Goals)
- **Level unlocks**: 50-200 levels in progression
- **Mechanic mastery**: Combine mechanics in later levels
- **Narrative payoffs**: Story climax, ending
- **Completionist goals**: 100% completion, all stars

### 4. Engagement (Retention Hooks)
- **Daily puzzles**: Special puzzle each day
- **Challenge mode**: Time attack, limited moves
- **Leaderboards**: Speed solving, fewest moves
- **Level editor**: Create and share puzzles (UGC)

---

## Monetization Strategy

### Premium Model (Paid Download)
- **Price**: $2.99-9.99 (one-time purchase)
- **No IAP**: All content included
- **No ads**: Clean experience
- **Pros**: Higher perceived value, no F2P stigma
- **Cons**: Lower install volume, no ongoing revenue

### Hybrid Model (F2P + IAP)
- **Base game**: Free with 20-50 levels
- **IAP**: $2.99-4.99 to unlock full game (150+ levels)
- **Hint packs**: $0.99 (10 hints), $2.99 (unlimited)
- **Ad removal**: $1.99 (optional)
- **Pros**: Higher install volume, trial before buy
- **Cons**: IAP friction, some players never convert

### F2P-Ads Model (Free with Ads)
- **Rewarded ads**: Watch ad for hints
- **Interstitial ads**: 1 per 5 levels
- **ARPDAU**: $0.08-0.20
- **Pros**: Lowest barrier to entry
- **Cons**: Ads disrupt zen puzzle experience

**Recommended**: Premium or Hybrid (puzzle genre = premium audience)

---

## Retention Mechanics

### D1 Hook (Day 1 Retention: 35-45%)
- **Smooth onboarding**: First 5 levels teach mechanics intuitively
- **Early "aha!" moments**: Simple but satisfying puzzles
- **Art style appeal**: Visually distinctive (first impression matters)
- **Story hook**: Narrative intro (if story-driven)
- **No frustration**: Generous hints, undo/reset

### D7 Hook (Day 7 Retention: 18-28%)
- **Mechanic variety**: Introduce 2-3 new mechanics by D7
- **Difficulty sweet spot**: Challenging but solvable
- **Daily puzzles**: Special puzzle each day (if F2P)
- **Story progression**: Chapter 1-2 complete (if narrative)
- **Completionist drive**: "Just 5 more levels to finish chapter"

### D30 Hook (Day 30 Retention: 8-15%)
- **Late-game complexity**: Combine all mechanics in clever ways
- **Narrative payoff**: Story climax, emotional beats
- **Challenge mode**: Time attack, leaderboards
- **Community**: Discord, subreddit, fan creations
- **Level editor**: UGC extends content (if supported)

---

## Player Psychology

### Bartle Types Distribution
- **Achievers** (70%): Completing all levels, 100% stars
- **Explorers** (25%): Discovering elegant solutions, secrets
- **Socializers** (3%): Sharing solutions, discussing puzzles
- **Killers** (2%): Speed solving, leaderboard competition

### Self-Determination Theory (SDT)
- **Competence**: Solving progressively harder puzzles
- **Autonomy**: Multiple solution paths (if open-ended)
- **Relatedness**: Sharing solutions, discussing with community

### Flow State
- **Easy start**: First 10 levels are tutorial-lite
- **Gradual difficulty**: Introduce 1 mechanic every 5-10 levels
- **Skill ceiling**: Late-game puzzles require deep thinking
- **Zen experience**: Relaxing music, no time pressure

### Psychological Triggers
- **"Aha!" dopamine**: Sudden insight is addictive
- **Sunk cost**: "I've spent 10 min, I'll solve this!"
- **Completionist drive**: "Just 3 more levels to finish chapter"
- **Intellectual pride**: "I solved it without hints"

---

## Technical Requirements

### Engine
- **Recommended**: Unity (2D or 3D)
- **Alternative**: Unreal (if high-fidelity 3D needed)
- **Rationale**: Unity has strong mobile support, asset store, physics

### Backend (Minimal)
- **Required**:
  - Cloud save (progress backup) — Optional
  - Analytics (GameAnalytics, Firebase)
- **Optional**:
  - Leaderboards (speed solving)
  - Level editor backend (UGC hosting)

### Platform
- **Primary**: iOS/Android cross-platform
- **Secondary**: PC/Mac (Steam) for premium indie
- **Orientation**: Portrait or Landscape (depends on puzzle type)
- **Resolution**: Support all aspect ratios (18:9, 19.5:9, 21:9)
- **File size**: <200MB (mobile), <1GB (PC with high-res assets)

### Performance Targets
- **FPS**: 60 FPS on mid-tier devices (2018+ phones)
- **Load time**: <3 seconds to puzzle select
- **Battery usage**: <5% drain per 30 min session

### Analytics Events
- **Critical**: puzzle_start, puzzle_complete, hint_used
- **Monetization**: iap_purchase, ad_impression
- **Retention**: daily_login, chapter_complete
- **Difficulty**: puzzle_attempts, avg_solve_time

---

## Competitive Positioning

### Strengths (vs Reference Games)
- **Premium audience**: Puzzle fans willing to pay upfront
- **Timeless**: Not dependent on trends, viral loops
- **Critical acclaim**: High-quality puzzles get featured by Apple/Google

### Weaknesses (vs Reference Games)
- **Limited audience**: Puzzle genre is niche vs casual
- **High bar**: Players compare to Monument Valley, The Room
- **Content creation**: Each puzzle requires design time

### ERRC Grid (Eliminate-Reduce-Raise-Create)
- **Eliminate**: Frustration (generous hints, undo/reset)
- **Reduce**: Grind (no filler levels, every puzzle matters)
- **Raise**: Art direction (visual appeal is critical)
- **Create**: Unique mechanic or narrative twist

---

## Session Flow (Typical Player Journey)

### Premium Flow (20-30 min)
1. **Open app** (5s) — Resume from last puzzle
2. **Play puzzle** (5-10 min) — Attempt solution, experiment
3. **Stuck** (2 min) — Consider hint, try different approach
4. **Solve** (1 min) — "Aha!" moment, completion animation
5. **Play 2-3 more puzzles** (10-20 min) — Continue chapter
6. **Session end** (20-30 min) — Natural stopping point

### F2P Flow (10-20 min)
1. **Daily puzzle** (5 min) — Complete special puzzle
2. **Main progression** (5-10 min) — Play 2-3 levels
3. **Stuck** (30s) — Watch rewarded ad for hint
4. **See interstitial ad** (30s) — After 5 levels
5. **Session end** (10-20 min) — Hit paywall or tired

---

## Difficulty Curve

### Beginner (Levels 1-20)
- **Mechanics**: 1-2 core mechanics
- **Complexity**: Simple, single solution path
- **Time to solve**: 2-5 minutes
- **Hints used**: 20-30% of players use hints

### Intermediate (Levels 21-50)
- **Mechanics**: 3-4 mechanics combined
- **Complexity**: Multiple solution paths
- **Time to solve**: 5-10 minutes
- **Hints used**: 40-50% use hints

### Advanced (Levels 51-100)
- **Mechanics**: 5-6 mechanics, clever combinations
- **Complexity**: Non-obvious solutions, lateral thinking
- **Time to solve**: 10-20 minutes
- **Hints used**: 60-70% use hints

### Expert (Levels 100+)
- **Mechanics**: All mechanics, emergent complexity
- **Complexity**: Multiple steps, planning required
- **Time to solve**: 20-40 minutes
- **Hints used**: 80-90% use hints (optional end-game)

---

## Development Milestones

### Phase 1: Prototype (8-12 weeks)
- Core puzzle mechanic (1-2 mechanics)
- 20 levels for testing
- Basic UI (puzzle view, undo, reset)
- Art style exploration (concept art)

### Phase 2: Alpha (16-24 weeks)
- 100 levels with progression
- Core loop polish (animations, feedback)
- Hint system
- Narrative structure (if story-driven)

### Phase 3: Beta (12-16 weeks)
- 150-200 levels total
- Full narrative (if story-driven)
- Polish pass (VFX, SFX, UI)
- Analytics integration
- Soft launch testing (completion rate, hint usage)

### Phase 4: Launch (4-6 weeks)
- Bug fixes from beta
- ASO optimization (keywords, screenshots, video)
- Press outreach (TouchArcade, indie game media)
- Marketing assets (trailer, screenshots)

---

## Risk Assessment

### High Risks
- **High quality bar**: Players compare to Monument Valley, The Room
  - **Mitigation**: Focus on unique mechanic or art style
- **Limited audience**: Puzzle genre is niche
  - **Mitigation**: Target premium audience, Steam/mobile crossover

### Medium Risks
- **Content creation**: Each puzzle requires design time
  - **Mitigation**: Level editor for UGC, or procedural generation
- **Monetization**: Premium model = low install volume
  - **Mitigation**: Hybrid model (F2P + IAP unlock)

### Low Risks
- **Technical complexity**: Puzzle mechanics are moderate
  - **Mitigation**: Unity has proven puzzle game templates
- **Platform rejection**: Low risk if content age-appropriate
  - **Mitigation**: Follow App Store/Play Store guidelines

---

## Success Metrics (30 days post-launch)

| Metric | Target | Stretch Goal |
|--------|--------|--------------|
| **D1 Retention** | 40% | 50% |
| **D7 Retention** | 22% | 30% |
| **D30 Retention** | 10% | 18% |
| **Completion Rate** | 30% | 50% (of all players finish game) |
| **Avg Session Length** | 20 min | 30 min |
| **Hint Usage** | 50% | 40% (lower = better difficulty balance) |
| **Premium Conversion** | 5% | 12% (F2P → paid unlock) |
| **App Store Rating** | 4.5 | 4.8 |

---

## Example Concept (Puzzle Genre)

**Game Title**: "Echoes of the Void"

**Vision**: A narrative puzzle game where players manipulate time to solve spatial puzzles in a surreal, Escher-inspired world. Each puzzle is a memory fragment, and solving all 100 puzzles reveals the protagonist's story (a scientist who accidentally created a black hole).

**Unique Twist**: Time manipulation mechanic — rewind object positions while keeping others frozen. Combine with spatial illusions (Monument Valley style) for unique puzzles.

**Monetization**: Premium model — $4.99 paid download, no IAP, no ads.

**Target Audience**: Puzzle enthusiasts 25-45, premium indie game fans, fans of Monument Valley, The Witness.

**CQS-Game Estimate**: 90/120 (strong Mechanics, Innovation, Tech Feasibility; moderate Market due to niche genre, high art/narrative quality compensates)

---

## Genre Compliance Checklist (Required for CQS-Game v2.0 Validation)

### Core Mechanics (Must-Have)
- [ ] Logic OR spatial reasoning core (deduce solution from rules OR manipulate objects)
- [ ] Undo/reset system (allow experimentation without penalty)
- [ ] Hint system (optional hints, F2P: watch ad, premium: unlimited)
- [ ] Gradual difficulty curve (introduce 1 mechanic every 5-10 levels)

### Retention Mechanics (Must-Have)
- [ ] Daily puzzles (if F2P) OR completionist goals (100% completion, all stars)
- [ ] Mechanic variety (introduce 2-3 new mechanics by D7)
- [ ] Narrative progression (if story-driven) OR challenge mode (time attack, leaderboards)

### Monetization (Must-Have for F2P)
- [ ] Premium: $2.99-9.99 (one-time purchase, all content included)
- [ ] Hybrid: F2P base (20-50 levels) + IAP unlock ($2.99-4.99 for full game)
- [ ] F2P-Ads: Rewarded ads (hints), Interstitial ads (1 per 5 levels)
- [ ] IAP: Hint packs ($0.99-2.99), Ad removal ($1.99)

### Nice-to-Have (Premium Tier)
- [ ] Narrative (story unfolds through puzzle completion)
- [ ] Unique art direction (isometric, hand-drawn, Escher-inspired)
- [ ] Ambient audio (relaxing music, ASMR-like sound design)
- [ ] Level editor (user-generated content)

### Red Flags (Avoid)
- ❌ Levels impossible without hints (no skill-based solution) → GAM-004 violation
- ❌ Forced frustration mechanics (artificial difficulty without logic) → User frustration
- ❌ Excessive ads (>1 per 3 levels, disrupts zen experience) → Genre mismatch
- ❌ Pay-to-win hints (must spend to progress) → GAM-004 violation

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
- **Arcade**: templates/shared/game-genres/arcade-template.md

---

**Last Updated**: 2026-01-13
**Version**: 1.0.0

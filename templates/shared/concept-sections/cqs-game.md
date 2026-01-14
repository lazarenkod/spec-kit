# CQS-Game (Concept Quality Score for Games)

**Version**: 2.0.0
**Last Updated**: 2026-01-13
**Adapted From**: CQS-E (Concept Quality Score - Evidence-based) v0.7.0

---

## Overview

CQS-Game is a specialized scoring framework for evaluating mobile game concepts. Version 2.0 introduces the **Strategic Depth** component and upgrades evidence standards to world-class quality.

**Key Differences from CQS-E:**
- **Removed**: Persona Depth, Transparency, Quality Intent (B2B-focused)
- **Added**: Mechanics (13%), Viral Potential (11%), Retention (11%), **Strategic Depth (10%)**
- **Reweighted**: All components rebalanced for Strategic Depth inclusion
- **Stricter threshold**: ≥90/120 (world-class tier, up from 85/120)
- **Evidence upgrades**: Viral Potential → STRONG, Retention → STRONG

**v2.0 World-Class Enhancements** (2026-01):
- **Strategic Depth** component (Three Pillars + ERRC + Positioning)
- Upgraded evidence standards (Viral: STRONG, Retention: STRONG with psychological triggers)
- Quality threshold raised (85 → 90 for world-class)
- Framework operationalization (K-factor formula, Bartle Types, SDT, Flow Theory)

---

## Formula (10 Components, 0-120 Scale)

```
CQS-Game v2.0 = (
  Market × 0.15 +              # Market opportunity (15%)
  Mechanics × 0.13 +           # Core mechanics depth (13%)
  Monetization × 0.13 +        # Monetization strategy (13%)
  Viral_Potential × 0.11 +     # Viral/social mechanics (11%)
  Retention × 0.11 +           # Retention mechanics (11%)
  Strategic_Depth × 0.10 +     # Strategic differentiation (10%) [NEW]
  Tech_Feasibility × 0.09 +    # Technical feasibility (9%)
  Competition × 0.08 +         # Competitive positioning (8%)
  Innovation × 0.08 +          # Innovation/differentiation (8%)
  Risk × 0.02                  # Risk assessment (2%)
) × 100 × Evidence_Multiplier

Target: ≥90/120 (75% of maximum, world-class tier)
```

**Weight Changes from v1.0:**
- Market: 16% → 15% (-1%)
- Mechanics: 14% → 13% (-1%)
- Monetization: 14% → 13% (-1%)
- Viral Potential: 12% → 11% (-1%)
- Retention: 12% → 11% (-1%)
- **Strategic Depth: 0% → 10% (+10%)** [NEW]
- Tech Feasibility: 10% → 9% (-1%)
- Risk: 6% → 2% (-4%, execution matters more for games)
- Competition, Innovation: unchanged

---

## Component Breakdown

### 1. Market Opportunity (15%)

**Maximum Score**: 100 points → 15 points after weighting

| Criterion | Max Points | Evidence Tier | Validation |
|-----------|:----------:|:-------------:|------------|
| Genre market size validated | 30 | STRONG | Sensor Tower, App Annie, GameRefinery data |
| Market growth trend positive | 25 | STRONG | YoY growth rates, genre trends |
| Target demographic sizing | 25 | MEDIUM | Player surveys, demographic studies |
| Geographic market fit | 20 | MEDIUM | Regional preferences, cultural fit |

**Scoring Guidelines:**

**Genre Market Size (30 pts)**:
- 30 pts: $1B+ annual revenue, Top 10 genre
- 25 pts: $500M-$1B, Top 20 genre
- 20 pts: $100M-$500M, Top 50 genre
- 10 pts: <$100M or declining genre
- 0 pts: No market data found

**Market Growth Trend (25 pts)**:
- 25 pts: >20% YoY growth with strong evidence
- 20 pts: 10-20% YoY growth
- 15 pts: 5-10% YoY growth
- 10 pts: Stable (0-5% growth)
- 0 pts: Declining market (<0% growth)

**Target Demographic Sizing (25 pts)**:
- 25 pts: 100M+ addressable players with evidence
- 20 pts: 50M-100M addressable players
- 15 pts: 10M-50M addressable players
- 10 pts: <10M addressable players
- 0 pts: No demographic data

**Geographic Market Fit (20 pts)**:
- 20 pts: Global appeal with regional validation
- 15 pts: Strong fit in 2+ major markets (US/EU/APAC)
- 10 pts: Niche regional appeal
- 5 pts: Limited geographic fit
- 0 pts: Cultural barriers identified

---

### 2. Core Mechanics (13%)

**Maximum Score**: 100 points → 13 points after weighting

| Criterion | Max Points | Evidence Tier | Validation |
|-----------|:----------:|:-------------:|------------|
| Core loop complete (4 phases) | 35 | N/A | Action→Reward→Progression→Engagement |
| Mastery curve designed | 25 | N/A | Skill ceiling, learning curve |
| Session flow optimized | 20 | MEDIUM | Session length benchmarks |
| Control scheme validated | 20 | MEDIUM | Touch controls, ergonomics |

**Scoring Guidelines:**

**Core Loop Complete (35 pts)** (Self-assessed, no evidence tier):
- 35 pts: All 4 phases fully defined (Action, Reward, Progression, Engagement)
- 25 pts: 3/4 phases defined
- 15 pts: 2/4 phases defined
- 5 pts: 1/4 phase defined
- 0 pts: Core loop not defined

**Mastery Curve (25 pts)** (Self-assessed):
- 25 pts: Clear skill progression, difficulty curve, mastery mechanics
- 20 pts: Basic difficulty progression defined
- 10 pts: Minimal difficulty variation
- 0 pts: No mastery curve

**Session Flow (20 pts)** (Evidence: MEDIUM):
- 20 pts: Session length matches genre benchmarks (±10%)
- 15 pts: Session length within ±20% of benchmarks
- 10 pts: Session length not optimized
- 0 pts: Session flow not considered

**Control Scheme (20 pts)** (Evidence: MEDIUM):
- 20 pts: Touch controls validated for mobile, ergonomics considered
- 15 pts: Basic touch controls defined
- 10 pts: Control scheme mentioned but not validated
- 0 pts: No control scheme defined

---

### 3. Monetization (13%)

**Maximum Score**: 100 points → 13 points after weighting

| Criterion | Max Points | Evidence Tier | Validation |
|-----------|:----------:|:-------------:|------------|
| Monetization model defined | 30 | STRONG | IAP/IAA strategy with benchmarks |
| IAP structure designed | 25 | MEDIUM | Price points, conversion funnels |
| Ethics compliance (GAM-004) | 25 | N/A | No predatory patterns |
| ARPDAU/LTV targets realistic | 20 | STRONG | Genre benchmarks, revenue models |

**Scoring Guidelines:**

**Monetization Model (30 pts)** (Evidence: STRONG):
- 30 pts: Model defined with genre benchmarks (F2P-ads/IAP/hybrid/premium)
- 25 pts: Model defined with partial benchmarks
- 15 pts: Model defined without benchmarks
- 0 pts: No monetization model

**IAP Structure (25 pts)** (Evidence: MEDIUM):
- 25 pts: Full IAP structure (price points, bundles, conversion funnel)
- 20 pts: IAP price points defined
- 10 pts: Basic IAP mention
- 0 pts: No IAP structure

**GAM-004 Ethics Compliance (25 pts)** (Self-assessed, CRITICAL):
- 25 pts: No predatory patterns (loot box disclosures, spending limits, no P2W)
- 15 pts: Minor ethical concerns (needs review)
- 0 pts: Predatory patterns detected (auto-fail QG-GCONCEPT-003)

**ARPDAU/LTV Targets (20 pts)** (Evidence: STRONG):
- 20 pts: Realistic ARPDAU/LTV with genre benchmarks
- 15 pts: Targets defined without benchmarks
- 10 pts: Aspirational targets (not validated)
- 0 pts: No revenue targets

---

### 4. Viral Potential (11%)

**Maximum Score**: 100 points → 11 points after weighting

| Criterion | Max Points | Evidence Tier | Validation |
|-----------|:----------:|:-------------:|------------|
| Sharing mechanics designed | 30 | MEDIUM | Social features, referrals |
| K-factor estimation **with validated formula** | 25 | **STRONG** | K = i × c × t formula with benchmarks |
| Social features planned | 25 | N/A | Multiplayer, guilds, leaderboards |
| Community building strategy | 20 | WEAK | Discord, events, UGC |

**Scoring Guidelines:**

**Sharing Mechanics (30 pts)** (Evidence: MEDIUM):
- 30 pts: Multiple sharing mechanics (social share, referrals, gifting)
- 20 pts: Basic sharing (social share only)
- 10 pts: Sharing mentioned but not designed
- 0 pts: No sharing mechanics

**K-factor (25 pts)** (Evidence: **STRONG** - UPGRADED):
**REQUIRED: Use K-factor formula with validated benchmarks**
```
K = i × c × t
Where:
i = Invitation rate (% of users who share)
c = Conversion rate (% of invites who install)
t = Time cycle (days from install to first share)

Genre Benchmarks (cite published data):
- Hyper-casual: K = 0.1-0.3 (viral loops rare)
- Social puzzle: K = 0.4-0.8 (share progress)
- Multiplayer: K = 0.6-1.2 (invite friends)
```
- 25 pts: K-factor >0.5 with formula validation + benchmark citation
- 20 pts: K-factor 0.3-0.5 with formula validation
- 10 pts: K-factor <0.3 or estimated without formula
- 0 pts: No viral coefficient considered

**Social Features (25 pts)** (Self-assessed):
- 25 pts: Multiplayer, guilds, leaderboards, chat
- 20 pts: 2-3 social features
- 10 pts: 1 social feature
- 0 pts: Single-player only

**Community Building (20 pts)** (Evidence: WEAK):
- 20 pts: Community strategy (Discord, events, UGC, influencer plan)
- 15 pts: Basic community plan
- 5 pts: Community mentioned
- 0 pts: No community strategy

---

### 5. Retention (11%)

**Maximum Score**: 100 points → 11 points after weighting

| Criterion | Max Points | Evidence Tier | Validation |
|-----------|:----------:|:-------------:|------------|
| D1/D7/D30 targets **validated vs genre benchmarks** | 30 | STRONG | Sensor Tower, GameRefinery with justification |
| Daily engagement loop **with psychological triggers** | 25 | **STRONG** | FOMO, streaks, variable rewards |
| Long-term hooks **with 30-60-90 day roadmap** | 25 | **STRONG** | Reference games with proven retention |
| Churn intervention **with A/B test plan** | 20 | **MEDIUM** | Hypothesis + trigger identification |

**Scoring Guidelines:**

**D1/D7/D30 Targets (30 pts)** (Evidence: **STRONG** - UPGRADED):
**REQUIRED: Benchmark validation with justification if targets exceed genre norms**
- 30 pts: All targets with genre benchmarks (±5%) + justification if exceeding
- 25 pts: All targets defined without benchmarks
- 15 pts: Partial targets (D1/D7 only)
- 0 pts: No retention targets

**Example**: "Match-3 genre D1 = 45% (Sensor Tower Q3 2025), our target = 50% justified by unique mechanic X"

**Daily Engagement Loop (25 pts)** (Evidence: **STRONG** - UPGRADED):
**REQUIRED: Map daily loop to psychological triggers**

Psychological Trigger Framework:
- **FOMO**: Limited-time offers, timed events ("Only 24 hours!")
- **Streaks**: Loss aversion ("Don't break your 7-day streak!")
- **Variable rewards**: Slot machine effect (10-100 gems random)
- **Social proof**: Friend rankings ("Your friend scored 8000!")

- 25 pts: Complete daily loop with 3+ psychological triggers mapped
- 20 pts: Basic daily mechanics with 1-2 triggers
- 10 pts: Daily engagement without trigger mapping
- 0 pts: No daily loop

**Long-term Hooks (25 pts)** (Evidence: **STRONG** - UPGRADED):
**REQUIRED: 30-60-90 day roadmap with reference games**
- 25 pts: Roadmap defined with proven retention patterns (cite reference games)
- 20 pts: Roadmap defined without reference validation
- 10 pts: Generic long-term hooks mentioned
- 0 pts: No long-term hooks

**Example**:
- 30-day: First character unlock milestone (AFK Arena pattern)
- 60-day: Guild wars unlock (Idle Heroes pattern)
- 90-day: Endgame raids (proven by Game X with 15% D90 retention)

**Churn Intervention (20 pts)** (Evidence: **MEDIUM** - UPGRADED):
**REQUIRED: A/B test hypothesis with trigger identification**
- 20 pts: Churn triggers identified + A/B test hypothesis ("Free booster at level 50 reduces D7 churn by 15%")
- 15 pts: Basic re-engagement plan with triggers
- 5 pts: Churn mentioned without interventions
- 0 pts: No churn strategy

---

### 6. Strategic Depth (10%) [NEW]

**Maximum Score**: 100 points → 10 points after weighting

**Purpose**: Evaluate strategic differentiation using Three Pillars framework + ERRC Grid + Positioning analysis.

| Criterion | Max Points | Evidence Tier | Validation |
|-----------|:----------:|:-------------:|------------|
| **Three Foundational Pillars** | 40 | STRONG | Core differentiation, Market positioning, Defensibility |
| - Pillar 1: Core differentiation (unique mechanic) | 15 | STRONG | Novel mechanic with validation |
| - Pillar 2: Market positioning (Blue Ocean space) | 15 | STRONG | White space identification |
| - Pillar 3: Defensibility (why hard to copy) | 10 | MEDIUM | Execution complexity, IP, network effects |
| **ERRC Grid Analysis** | 30 | MEDIUM | Eliminate-Reduce-Raise-Create framework |
| - Eliminate: Genre pain points removed | 8 | MEDIUM | Competitor weaknesses addressed |
| - Reduce: Unnecessary complexity cut | 7 | WEAK | Simplified vs competitors |
| - Raise: Key experience amplified | 8 | MEDIUM | Core differentiator enhanced |
| - Create: New value delivered | 7 | MEDIUM | Innovation vs genre norms |
| **Positioning Map** | 30 | MEDIUM | 2x2 matrix with white space |
| - 2x2 matrix (e.g., Complexity vs Social) | 15 | MEDIUM | Clear axes with competitor plotting |
| - White space identification | 15 | WEAK | Gap in market positioning |

**Scoring Guidelines:**

**Three Foundational Pillars (40 pts)**:

**Pillar 1: Core Differentiation (15 pts)** (Evidence: STRONG):
- 15 pts: Unique mechanic validated with proof (not present in top 10 competitors)
- 12 pts: Novel mechanic with partial validation
- 8 pts: Incremental improvement over existing mechanics
- 0 pts: No unique differentiation

**Pillar 2: Market Positioning (15 pts)** (Evidence: STRONG):
- 15 pts: Clear Blue Ocean space identified with competitive mapping
- 12 pts: Partial white space (some competition)
- 8 pts: Crowded space with minor differentiation
- 0 pts: No positioning strategy

**Pillar 3: Defensibility (10 pts)** (Evidence: MEDIUM):
- 10 pts: Multiple defensibility factors (execution complexity + IP + network effects)
- 8 pts: 1-2 defensibility factors
- 4 pts: Weak defensibility (easily copied)
- 0 pts: No defensibility consideration

**ERRC Grid Analysis (30 pts)** (Evidence: MEDIUM):

**Eliminate (8 pts)**: Remove industry pain points
- 8 pts: Clear elimination of 2+ genre pain points with evidence
- 5 pts: 1 pain point eliminated
- 0 pts: No eliminations

**Example**: "Eliminate wait timers (Match-3 genre fatigue documented in 1000+ reviews)"

**Reduce (7 pts)**: Cut unnecessary complexity
- 7 pts: Simplification with complexity comparison vs competitors
- 4 pts: Generic simplification claim
- 0 pts: No reduction

**Example**: "Reduce booster types from 12 (Candy Crush) to 5 (decision paralysis fix)"

**Raise (8 pts)**: Amplify key differentiators
- 8 pts: Clear amplification with competitor benchmark
- 5 pts: Generic "raise" claim
- 0 pts: No amplification

**Example**: "Raise social features to guild wars level (AFK Arena benchmark)"

**Create (7 pts)**: Invent new value
- 7 pts: Novel value creation not present in genre
- 4 pts: Incremental new value
- 0 pts: No creation

**Example**: "Create narrative progression (puzzles unlock story chapters) - not present in top Match-3 games"

**Positioning Map (30 pts)** (Evidence: MEDIUM):

**2x2 Matrix (15 pts)**:
- 15 pts: Clear axes (e.g., Complexity vs Social) with 5+ competitors plotted
- 10 pts: Basic 2x2 with 2-3 competitors
- 5 pts: Axes defined but no competitor plotting
- 0 pts: No positioning map

**White Space Identification (15 pts)**:
- 15 pts: Clear gap identified with validation (no competitors in quadrant)
- 10 pts: Partial white space (1-2 weak competitors)
- 5 pts: Generic "we're different" claim
- 0 pts: No white space identified

---

### 7. Tech Feasibility (9%)

**Maximum Score**: 100 points → 9 points after weighting

| Criterion | Max Points | Evidence Tier | Validation |
|-----------|:----------:|:-------------:|------------|
| Engine/platform justified | 35 | MEDIUM | Unity/Unreal/Custom with rationale |
| Development timeline realistic | 30 | WEAK | Scope-based estimate |
| Backend requirements scoped | 20 | WEAK | Auth, storage, matchmaking |
| Platform compliance verified | 15 | N/A | iOS/Android policies |

**Scoring Guidelines:**

**Engine/Platform (35 pts)** (Evidence: MEDIUM):
- 35 pts: Engine justified with genre fit analysis (Unity/Unreal/Custom)
- 25 pts: Engine selected with partial justification
- 10 pts: Engine mentioned without justification
- 0 pts: No engine selected

**Development Timeline (30 pts)** (Evidence: WEAK):
- 30 pts: Realistic timeline with milestones (prototype, alpha, beta, launch)
- 20 pts: High-level timeline (X months/years)
- 10 pts: Aspirational timeline (not validated)
- 0 pts: No timeline

**Backend Requirements (20 pts)** (Evidence: WEAK):
- 20 pts: Backend scoped (auth, storage, matchmaking, analytics)
- 15 pts: Partial backend scoping
- 5 pts: Backend mentioned
- 0 pts: No backend consideration

**Platform Compliance (15 pts)** (Self-assessed):
- 15 pts: iOS/Android policies verified (IDFA, privacy, content ratings)
- 10 pts: Basic compliance awareness
- 0 pts: Compliance not considered

---

### 8. Competition (8%)

**Maximum Score**: 100 points → 8 points after weighting

| Criterion | Max Points | Evidence Tier | Validation |
|-----------|:----------:|:-------------:|------------|
| Top 5 competitors analyzed | 40 | STRONG | App Annie, Sensor Tower data |
| Competitor weaknesses identified | 30 | MEDIUM | Gap analysis, player reviews |
| Positioning strategy defined | 30 | N/A | Unique value proposition |

**Scoring Guidelines:**

**Top 5 Competitors (40 pts)** (Evidence: STRONG):
- 40 pts: Top 5 analyzed (revenue, downloads, features, monetization)
- 30 pts: Top 3 analyzed
- 20 pts: Top 1-2 analyzed
- 0 pts: No competitive analysis

**Competitor Weaknesses (30 pts)** (Evidence: MEDIUM):
- 30 pts: Clear weaknesses identified with player review evidence
- 20 pts: Weaknesses identified without evidence
- 10 pts: Generic weaknesses (e.g., "too grindy")
- 0 pts: No weaknesses identified

**Positioning Strategy (30 pts)** (Self-assessed):
- 30 pts: Clear UVP, ERRC grid (Eliminate-Reduce-Raise-Create)
- 20 pts: Basic positioning statement
- 10 pts: Positioning mentioned
- 0 pts: No positioning strategy

---

### 9. Innovation (8%)

**Maximum Score**: 100 points → 8 points after weighting

| Criterion | Max Points | Evidence Tier | Validation |
|-----------|:----------:|:-------------:|------------|
| 2+ unique differentiators | 40 | MEDIUM | Novel mechanics, IP, theme |
| Innovation defensibility | 30 | WEAK | Patents, trade secrets, execution |
| Player delight moments | 30 | N/A | "Wow" moments, surprises |

**Scoring Guidelines:**

**Unique Differentiators (40 pts)** (Evidence: MEDIUM):
- 40 pts: 3+ unique differentiators with validation
- 30 pts: 2 unique differentiators
- 20 pts: 1 unique differentiator
- 10 pts: Incremental improvements only
- 0 pts: No differentiation

**Innovation Defensibility (30 pts)** (Evidence: WEAK):
- 30 pts: Defensible innovation (patents, execution complexity)
- 20 pts: Partially defensible (hard to clone)
- 10 pts: Easily copied
- 0 pts: No innovation defense

**Player Delight Moments (30 pts)** (Self-assessed):
- 30 pts: Multiple "wow" moments designed (surprises, Easter eggs, delight)
- 20 pts: 1-2 delight moments
- 10 pts: Delight mentioned
- 0 pts: No delight moments

---

### 10. Risk Assessment (2%)

**Maximum Score**: 100 points → 2 points after weighting

| Criterion | Max Points | Evidence Tier | Validation |
|-----------|:----------:|:-------------:|------------|
| Top 5 risks identified | 35 | MEDIUM | Market, technical, competitive |
| Mitigations documented | 35 | WEAK | Actionable risk mitigation plans |
| Pivot criteria defined | 30 | N/A | Trigger metrics for pivot/kill |

**Scoring Guidelines:**

**Top 5 Risks (35 pts)** (Evidence: MEDIUM):
- 35 pts: 5+ risks identified with probability/impact analysis
- 25 pts: 3-4 risks identified
- 15 pts: 1-2 risks identified
- 0 pts: No risk assessment

**Mitigations (35 pts)** (Evidence: WEAK):
- 35 pts: Actionable mitigation plan for each risk
- 25 pts: Partial mitigation plans
- 10 pts: Mitigations mentioned
- 0 pts: No mitigations

**Pivot Criteria (30 pts)** (Self-assessed):
- 30 pts: Clear pivot/kill criteria (e.g., "D1 < 30% after 1 month")
- 20 pts: High-level pivot criteria
- 10 pts: Pivot mentioned
- 0 pts: No pivot criteria

---

## Evidence Multiplier

**Applied AFTER component scoring:**

| Multiplier | Criteria | Examples |
|:----------:|----------|----------|
| **1.2** | All claims sourced from credible sources | Sensor Tower, App Annie, GameRefinery, academic papers |
| **1.1** | Most claims sourced (80%+) | Mix of primary sources + credible secondary |
| **1.0** | Adequate sourcing (50-80%) | Some sources + reasonable assumptions |
| **0.9** | Partial sourcing (30-50%) | Limited sources, many assumptions |
| **0.8** | Weak sourcing (<30%) | Mostly assumptions, few sources |

**Source Quality Tiers:**

- **VERY_STRONG** (30 pts): Sensor Tower, App Annie, GameRefinery, Unity Analytics reports
- **STRONG** (25 pts): Industry reports (Newzoo, SuperData), academic papers, K-factor validation
- **MEDIUM** (20 pts): Game dev blogs (Deconstructor of Fun), developer postmortems
- **WEAK** (5 pts): Reddit discussions, Twitter polls, anecdotal evidence
- **NONE** (0 pts): No sources, pure speculation

---

## Quality Gate Thresholds

| CQS-Game Range | v1.0 Status | v2.0 Status | Recommendation |
|----------------|:-----------:|:-----------:|----------------|
| **95-120** | ✅ EXCELLENT | ✅ **WORLD-CLASS** | AAA studio pitch deck ready |
| **90-94** | ✅ READY | ✅ **EXCELLENT** | Investor-grade quality |
| **85-89** | ✅ READY | ⚠️ **GOOD** | Proceed with minor improvements |
| **80-84** | ⚠️ CAUTION | ⚠️ **CAUTION** | Improve weakest components |
| **70-79** | ⚠️ CAUTION | ⛔ **NOT READY** | Substantial rework required |
| **< 70** | ⛔ NOT READY | ⛔ **FAILED** | Reconsider game idea |

**Key Change**: World-class threshold raised from 85 → 90 to reflect higher standards.

**Component-Specific Thresholds:**

- **Market < 11**: Reconsider genre or target audience (15% weight)
- **Mechanics < 9**: Core loop needs major work (13% weight)
- **Monetization < 9**: Revenue model not viable (13% weight)
- **Retention < 8**: Engagement hooks insufficient (11% weight)
- **Strategic Depth < 7**: Differentiation weak, crowded space (10% weight)
- **GAM-004 violation**: Auto-fail (QG-GCONCEPT-003)

---

## Example Calculation (v2.0)

**Hypothetical Match-3 Concept:**

1. **Market**: 85/100 × 0.15 = **12.75**/15
   - Genre size: 30/30 (Match-3 is $2B+ market)
   - Growth: 20/25 (Stable but not growing)
   - Demographics: 20/25 (Broad appeal)
   - Geographic: 15/20 (Strong in West, weak in Asia)

2. **Mechanics**: 90/100 × 0.13 = **11.7**/13
   - Core loop: 35/35 (Complete 4-phase loop)
   - Mastery: 25/25 (Difficulty curve validated)
   - Session flow: 15/20 (Slightly long sessions)
   - Controls: 15/20 (Touch optimized)

3. **Monetization**: 80/100 × 0.13 = **10.4**/13
   - Model: 30/30 (Hybrid IAP+ads with benchmarks)
   - IAP: 20/25 (Price points defined)
   - Ethics: 25/25 (GAM-004 compliant)
   - LTV: 15/20 (Targets realistic but conservative)

4. **Viral Potential**: 60/100 × 0.11 = **6.6**/11
   - Sharing: 15/30 (Basic social share)
   - K-factor: **20/25** (K=0.4 with formula validation, hyper-casual benchmark cited)
   - Social: 10/25 (Leaderboards only)
   - Community: 15/20 (Discord + events)

5. **Retention**: 90/100 × 0.11 = **9.9**/11
   - D1/D7/D30: 30/30 (Benchmarked with justification)
   - Daily loop: **25/25** (Complete with FOMO + streaks + variable rewards)
   - Long-term: **25/25** (30-60-90 roadmap with AFK Arena patterns)
   - Churn: **10/20** (A/B test hypothesis: "Free booster at level 50")

6. **Strategic Depth**: 75/100 × 0.10 = **7.5**/10 [NEW]
   - Three Pillars: 30/40 (Pillar 1: 12/15, Pillar 2: 12/15, Pillar 3: 6/10)
   - ERRC Grid: 22/30 (Eliminate: 6/8, Reduce: 5/7, Raise: 6/8, Create: 5/7)
   - Positioning: 23/30 (2x2 matrix: 12/15, White space: 11/15)

7. **Tech Feasibility**: 80/100 × 0.09 = **7.2**/9
   - Engine: 30/35 (Unity justified)
   - Timeline: 25/30 (12-month realistic)
   - Backend: 15/20 (Auth + storage scoped)
   - Compliance: 10/15 (iOS/Android verified)

8. **Competition**: 70/100 × 0.08 = **5.6**/8
   - Top 5: 30/40 (Top 3 analyzed only)
   - Weaknesses: 25/30 (Gaps identified)
   - Positioning: 15/30 (Generic UVP)

9. **Innovation**: 60/100 × 0.08 = **4.8**/8
   - Differentiators: 30/40 (2 unique mechanics)
   - Defensibility: 15/30 (Somewhat defensible)
   - Delight: 15/30 (Few wow moments)

10. **Risk**: 75/100 × 0.02 = **1.5**/2
    - Top 5 risks: 25/35 (4 risks identified)
    - Mitigations: 25/35 (Partial plans)
    - Pivot: 25/30 (Pivot criteria defined)

**Subtotal**: 12.75 + 11.7 + 10.4 + 6.6 + 9.9 + 7.5 + 7.2 + 5.6 + 4.8 + 1.5 = **77.95**/100

**Evidence Multiplier**: 1.15 (85% sourced from Sensor Tower, App Annie, GameRefinery + K-factor validation)

**Final CQS-Game v2.0**: 77.95 × 1.15 = **89.64**/120

**Status**: ⚠️ GOOD (just below 90 world-class threshold)

**Recommendation**: Improve Strategic Depth (+2 pts) or Innovation (+1 pt) to reach 90+ world-class tier

---

## Usage in `/speckit.games.concept`

1. **Phase 2**: Each genre generator self-assesses CQS-Game v2.0 for its variant
2. **Phase 3**: concept-quality-validator recalculates and validates all scores
3. **Phase 3.5**: comparative-validator cross-checks variants for consistency [NEW]
4. **Phase 4**: file-generator selects highest CQS-Game variant as primary
5. **Output**: specs/quality-report.md contains full CQS-Game v2.0 breakdown per variant

---

## Changelog

- **v2.0.0** (2026-01-13): World-class upgrade
  - **ADDED**: Strategic Depth component (10% weight) with Three Pillars + ERRC + Positioning
  - **UPGRADED**: Viral Potential evidence tier (MEDIUM → STRONG) with K-factor formula requirement
  - **UPGRADED**: Retention evidence tiers (STRONG with psychological triggers + 30-60-90 roadmap)
  - **CHANGED**: All component weights rebalanced (-1% each from Market/Mechanics/Monetization/Viral/Retention/Tech, -4% from Risk)
  - **CHANGED**: Quality threshold raised (85/120 → 90/120 for world-class tier)
  - **CHANGED**: Evidence multiplier now includes K-factor validation for higher scores

- **v1.0.0** (2026-01-13): Initial release adapted from CQS-E v0.7.0
  - 9 components (removed Persona Depth, Strategic Depth, Transparency, Quality Intent)
  - Added Mechanics (14%), Viral Potential (12%), Retention (12%)
  - Stricter threshold: 85/120 (vs CQS-E's 80/120)
  - Game-specific evidence tiers and benchmarks

---

**See Also:**
- `/speckit.concept` — Uses CQS-E formula for B2B concepts
- `/speckit.games.concept` — Uses this CQS-Game formula
- `templates/shared/concept-sections/cqs-score.md` — Original CQS-E formula

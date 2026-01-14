---
name: games.virality
version: 0.1.0
description: Engineer built-in viral mechanics, shareability, TikTok hooks, and K-factor optimization for mobile games
persona: viral-engineer-agent
model: opus
thinking_budget: 32000
reasoning_mode: extended
priority: P1

inputs:
  game_concept_path:
    type: string
    required: true
    description: Path to game concept or GDD
    default: specs/game-concept.md
    examples:
      - "specs/game-concept.md"
      - "docs/gdd/gdd.md"
      - "specs/alternatives/01-sorting.md"

  platform_focus:
    type: enum
    options: [tiktok, instagram, youtube-shorts, multi-platform]
    default: multi-platform
    description: Primary platform for viral content optimization

  k_factor_target:
    type: float
    options: [0.8, 1.0, 1.2, 1.5]
    default: 1.0
    description: Target viral coefficient (K-factor, where 1.0 = each user brings 1 new user)
    details:
      0.8: "Conservative target (80% viral growth, typical for casual games)"
      1.0: "Balanced target (100% viral growth, sustainable)"
      1.2: "Aggressive target (120% viral growth, requires strong mechanics)"
      1.5: "Exponential target (150% viral growth, rare, requires exceptional design)"

flags:
  platform:
    type: enum
    options: [tiktok, instagram, youtube-shorts, multi-platform]
    default: multi-platform
    description: |
      Platform optimization focus:
      - tiktok: Optimize for TikTok algorithm (ASMR, satisfying moments, skill showcases)
      - instagram: Optimize for Instagram Reels (aesthetic, lifestyle, challenges)
      - youtube-shorts: Optimize for YouTube Shorts (tutorials, tips, compilations)
      - multi-platform: Balanced approach for all platforms

  k-factor-target:
    type: float
    options: [0.8, 1.0, 1.2, 1.5]
    default: 1.0
    description: Target viral coefficient (K = invites × conversion × time-factor)

  skip-gates:
    type: boolean
    default: false
    description: Skip quality gates validation (not recommended)

  max-model:
    type: enum
    options: [opus, sonnet, haiku]
    default: opus
    description: Maximum model tier to use (cost control)

outputs:
  - specs/virality.md                           # Viral mechanics blueprint (master)
  - specs/virality/share-features.md            # Share UX & triggers
  - specs/virality/challenge-modes.md           # Challenge design
  - specs/virality/tiktok-hooks.md              # TikTok content calendar
  - specs/virality/influencer-kit.md            # Influencer seeding materials
  - specs/virality/social-proof.md              # Social elements (leaderboards, clans)

quality_gates:
  - name: QG-VIRALITY-001
    description: K-Factor Feasibility
    condition: "Calculated K-factor achievable for genre and budget"
    threshold: "K-factor target within ±20% of genre benchmarks"
    severity: HIGH
    rationale: "Unrealistic K-factor targets lead to feature bloat and wasted development"
    validation: |
      Compare target vs genre benchmarks:
      - Hyper-casual: 0.1-0.3
      - Social casual: 0.4-0.8
      - Multiplayer: 0.6-1.2
      If target exceeds genre max by >20%, require justification or downgrade target

  - name: QG-VIRALITY-002
    description: Platform Guidelines Compliance
    condition: "All share mechanics comply with platform policies"
    threshold: "0 policy violations"
    severity: CRITICAL
    validation: |
      Check compliance with:
      - TikTok Community Guidelines (no spam, fake engagement)
      - Instagram Terms of Service (no artificial likes/follows)
      - YouTube Shorts Policies (no misleading thumbnails, click-bait)
      - App Store Review Guidelines (no incentivized reviews)
    references:
      - "TikTok Community Guidelines 2025"
      - "Instagram Platform Policy"
      - "YouTube Community Guidelines"

  - name: QG-VIRALITY-003
    description: Organic Share Authenticity
    condition: "No forced/fake sharing incentives (dark patterns)"
    threshold: "0 violations"
    severity: CRITICAL
    rationale: "Fake virality damages brand and violates platform policies"
    validation: |
      Prohibited patterns:
      - ❌ Forced sharing (must share to unlock content)
      - ❌ Fake social proof (bot followers, fake likes)
      - ❌ Misleading incentives ("Share to win" without real prizes)
      - ❌ Spam mechanics (auto-post to timeline without consent)

      Allowed patterns:
      - ✅ Optional sharing with rewards (clear disclosure)
      - ✅ One-tap share with preview (user sees before posting)
      - ✅ Challenge invites (genuine friend engagement)
      - ✅ Achievement sharing (user-initiated celebration)
    references:
      - "memory/domains/quality-gates.md GAM-004"

  - name: QG-VIRALITY-004
    description: Content Hook Specificity
    condition: "TikTok hooks are concrete, actionable, not generic"
    threshold: ">= 5 specific hooks with examples"
    severity: HIGH
    rationale: "Generic hooks like 'create engaging content' are not actionable"
    validation: |
      Each hook must have:
      - Specific game moment (e.g., "Level 50 boss defeat animation")
      - Concrete format (e.g., "15-second slow-motion replay")
      - Target emotion (e.g., "Satisfying ASMR sensation")
      - Example script or storyboard

      ❌ Bad: "Share exciting moments"
      ✅ Good: "Auto-record 10-second slow-motion replay of perfect combo with particle effects, export as TikTok-ready 9:16 video"

pre_gates:
  - name: QG-VIRALITY-000
    description: Game Concept Exists
    condition: "Game concept or GDD file exists at specified path"
    severity: CRITICAL
    validation: "Check file exists: specs/game-concept.md OR docs/gdd/gdd.md"

handoffs:
  - label: Optimize App Store Presence
    agent: speckit.games.aso
    auto: false
    condition:
      - "Virality mechanics designed"
      - "Share features complete"
      - "Content hooks defined"
    description: "App Store Optimization with viral hooks integration"
    prompt: "Use viral mechanics and share features as ASO differentiators"

  - label: Setup Analytics Tracking
    agent: speckit.games.analytics
    auto: false
    condition:
      - "K-factor calculation defined"
      - "Viral funnels specified"
    description: "Track viral metrics, referral attribution, K-factor"
    prompt: |
      Setup analytics for:
      - K-factor tracking (invites sent/accepted/converted)
      - Referral attribution (which users came from viral shares)
      - Share funnel (views → clicks → installs → D1 retention)
      - Content performance (TikTok views, engagement rate)

  - label: Create GDD Section
    agent: speckit.gdd
    auto: false
    condition:
      - "User wants to integrate virality into GDD"
    description: "Add social/viral section to Game Design Document"
    prompt: "Create Section 09: Social & Viral Features from virality specs"

  - label: Balance Viral Rewards
    agent: speckit.balance
    auto: false
    condition:
      - "Share incentives use in-game currency"
      - "Referral rewards defined"
    description: "Validate viral rewards don't break economy"
    prompt: "Simulate economy impact of referral rewards and share incentives"

workflow:
  phases:
    - phase: 0
      name: Context Analysis
      agents: 1
      parallel: false
      description: Extract game mechanics, genre, target audience from concept/GDD

    - phase: 1
      name: Viral Research
      agents: 4
      parallel: true
      description: K-factor benchmarks, platform trends, competitor viral analysis, share psychology

    - phase: 2
      name: Mechanics Design
      agents: 3
      parallel: true
      description: Built-in viral mechanics, share UX, challenge modes

    - phase: 3
      name: Content Strategy
      agents: 2
      parallel: true
      description: TikTok hooks, influencer kit, content calendar

    - phase: 4
      name: Validation & File Generation
      agents: 1
      parallel: false
      description: Quality gates validation, K-factor calculation, file generation

---

# Game Virality Engineering Command

**Purpose**: Engineer built-in viral mechanics, shareability features, and TikTok content hooks for mobile games

**Target Users**: Game designers, growth marketers, indie developers optimizing for organic user acquisition

# `/speckit.games.virality` — Viral Mechanics & Content Strategy

## Overview

This command engineers viral growth mechanics into mobile games through three integrated approaches:

1. **Built-in Viral Mechanics** — Features that naturally encourage sharing (perfect run recording, challenge creator, satisfying moments)
2. **Share UX Optimization** — Frictionless one-tap sharing with custom thumbnails and social templates
3. **Content Strategy** — Platform-specific content hooks (TikTok ASMR, Instagram aesthetics, YouTube tutorials)

**Key Outputs:**
- K-factor calculation and feasibility analysis
- 6 comprehensive specification files
- Platform-specific content calendar (Week 1-4)
- Influencer seeding kit
- Quality-gated validation (4 gates)

**Differentiators from Generic Growth Tools:**
- **Game-Specific**: Viral mechanics designed for game loops (not generic social sharing)
- **Platform-Optimized**: TikTok algorithm understanding (ASMR, satisfying moments, skill showcases)
- **Evidence-Based**: K-factor benchmarks from Sensor Tower, GameRefinery data
- **Ethical**: QG-VIRALITY-003 blocks dark patterns (forced sharing, fake engagement)

## When to Use

**✅ Use `/speckit.games.virality` when:**
- Game mechanics are finalized (use AFTER `/speckit.games.mechanics`)
- Designing for organic user acquisition (low CAC)
- Creating social or multiplayer features
- Optimizing for TikTok/Instagram virality
- Planning influencer partnerships

**❌ Do NOT use when:**
- Game concept still being explored (use `/speckit.games.concept` first)
- Pure paid UA strategy (no organic component)
- Single-player premium game (no social features)
- Before core loop is fun (virality can't fix unfun games)

**Workflow Position:**
```
/speckit.games.concept → /speckit.games.mechanics → /speckit.games.virality → /speckit.games.aso → /speckit.games.analytics
```

## Usage Examples

```bash
# Multi-platform viral design with balanced K-factor
/speckit.games.virality --platform=multi-platform --k-factor-target=1.0

# TikTok-optimized viral mechanics with aggressive K-factor
/speckit.games.virality --platform=tiktok --k-factor-target=1.2

# Instagram Reels focus with conservative K-factor
/speckit.games.virality --platform=instagram --k-factor-target=0.8

# Quick validation with cost control (use sonnet instead of opus)
/speckit.games.virality --max-model=sonnet --skip-gates
```

## Agent Architecture

### Phase 0: Context Analysis (Priority 5)

**context-analyzer** (sonnet, 8K):

Extract from game concept or GDD:
- **Game genre**: Hyper-casual, casual, mid-core, multiplayer
- **Core loop**: Action-Reward-Progression-Engagement phases
- **Target audience**: Age, demographics, player motivations
- **Existing social features**: Leaderboards, guilds, co-op, PvP
- **Session length**: 2-5 min (hyper-casual), 10-15 min (casual), 20+ min (mid-core)
- **Monetization model**: F2P-Ads, F2P-IAP, hybrid, premium

**Determine baseline virality potential:**
- High: Multiplayer, social, competitive games (natural sharing triggers)
- Medium: Single-player with leaderboards, achievements
- Low: Pure puzzle, premium, offline games

**Output**: Context summary with genre-specific viral opportunities

---

### Phase 1: Viral Research (Priority 10, Parallel)

**Wave 1 Agents** (4 parallel):

#### 1. **k-factor-benchmarker** (opus, 32K)

**Research Objective**: Establish K-factor benchmarks and validate target feasibility

**Step 1: K-Factor Formula & Calculation**

**Formula**:
```
K = i × c × t

Where:
i = Average invites sent per user
c = Conversion rate (% of invites that install)
t = Time factor (viral cycle speed)
```

**Example Calculation**:
```
Game: Social puzzle game
i = 3.0 invites/user (via friend challenges)
c = 0.15 (15% of invited friends install)
t = 0.95 (viral cycle takes 3 days, dampening factor)

K = 3.0 × 0.15 × 0.95 = 0.43

Result: Sub-viral (K < 1.0), but respectable for casual genre
```

**Step 2: Genre Benchmarks** (with STRONG evidence)

**K-Factor by Genre** (Sensor Tower, GameRefinery 2025):
```
| Genre | K-Factor Range | Evidence | Example Games |
|-------|----------------|----------|---------------|
| Hyper-casual | 0.1-0.3 | Sensor Tower Q3 2025 | Subway Surfers, Crossy Road |
| Social casual | 0.4-0.8 | GameRefinery Social Report | Candy Crush, Words With Friends |
| Multiplayer | 0.6-1.2 | App Annie Growth Study | Among Us, Brawl Stars, Stumble Guys |
| Competitive | 0.8-1.5 | Sensor Tower Viral Games | Fortnite Mobile, PUBG Mobile |
| IO games | 1.0-2.0 | GameRefinery IO Analysis | Agar.io, Slither.io (peak 2016) |
```

**Validation Rule**:
- If target K-factor exceeds genre max by >20% → Flag as unrealistic
- If target K-factor < genre min → Flag as under-optimized opportunity

**Step 3: K-Factor Component Breakdown**

**Invites per User (i)**:
- Hyper-casual: 0.5-1.5 (low engagement, casual sharing)
- Social casual: 2.0-4.0 (friend challenges, leaderboards)
- Multiplayer: 3.0-6.0 (team invites, guild recruitment)
- Competitive: 4.0-8.0 (tournaments, ranked seasons)

**Conversion Rate (c)**:
- Cold invite (no context): 5-10%
- Warm invite (friend recommendation): 10-20%
- Challenge invite (competitive hook): 15-30%
- Influencer referral: 20-40%

**Time Factor (t)**:
- Instant viral loop (< 1 day): t = 1.0
- Fast viral loop (1-2 days): t = 0.9-0.95
- Moderate viral loop (3-5 days): t = 0.8-0.9
- Slow viral loop (7+ days): t = 0.6-0.8

**Step 4: Achievable K-Factor Calculation**

Based on genre, calculate realistic K-factor:
```
Genre: Social puzzle game
Baseline i: 2.5 (friend challenges)
Baseline c: 0.12 (warm invites)
Baseline t: 0.90 (2-day cycle)

Baseline K = 2.5 × 0.12 × 0.90 = 0.27

With optimization:
Optimized i: 3.5 (add tournament invites)
Optimized c: 0.18 (improved challenge UX)
Optimized t: 0.95 (faster onboarding)

Optimized K = 3.5 × 0.18 × 0.95 = 0.60

Uplift: +122% vs baseline
Verdict: Achievable with viral mechanics design
```

**Output Format**:
1. Genre benchmark table with evidence sources
2. K-factor formula breakdown with game-specific values
3. Achievable K-factor calculation (baseline vs optimized)
4. Feasibility verdict (achievable / stretch goal / unrealistic)
5. Component optimization recommendations (where to improve i, c, t)

**Evidence tier**: STRONG (cite Sensor Tower Q3 2025, GameRefinery Viral Mechanics Report, App Annie Growth Study)

---

#### 2. **platform-trends-researcher** (opus, 32K)

**Research Objective**: Identify platform-specific viral content patterns and algorithm priorities

**Step 1: TikTok Algorithm Priorities (2025)**

**Content Types TikTok Promotes**:
1. **ASMR & Satisfying Moments** (High engagement)
   - Smooth animations, particle effects, perfect combos
   - Sounds: Tapping, slicing, popping, whoosh effects
   - Visual: Color gradients, symmetry, cascading animations
   - Example: Candy Crush level clear animation (10M+ views)

2. **Impossible → Possible Transitions** (Viral hook)
   - Show failure first (struggle, stuck level)
   - Then show success (clutch win, perfect execution)
   - Format: Split-screen or before/after transition
   - Example: "I was stuck on Level 100 for 3 days... then THIS happened"

3. **Skill Showcases** (Aspirational content)
   - Top 1% player runs (speedruns, no-hit runs)
   - Hidden techniques, secret combos
   - Difficulty: Hard but achievable (not impossible)
   - Example: Geometry Dash level completions

4. **Before/After Transformations** (Progress)
   - Level 1 character vs Level 100 character
   - Beginner base vs endgame base
   - Satisfying visual contrast
   - Example: Idle game progression time-lapses

**TikTok Technical Specs**:
- Aspect ratio: 9:16 (vertical)
- Duration: 7-15 seconds (sweet spot for completion rate)
- Captions: On-screen text (80% watch with sound off)
- Hashtags: 3-5 per video (#gaming #mobilegames #[genre])
- Posting times: 6-9am, 12-2pm, 7-11pm (user timezone)

**Step 2: Instagram Reels Best Practices**

**Content Types Instagram Promotes**:
1. **Aesthetic & Lifestyle** (High shareability)
   - Beautiful art style, color harmony
   - Cozy, satisfying, relaxing vibes
   - Example: Unpacking, A Little to the Left (aesthetic puzzle games)

2. **Challenges & Trends** (Viral participation)
   - Participate in trending audio/formats
   - Create game-specific challenge (e.g., "Can you beat my score?")
   - Example: "Duet this!" challenges

3. **Tutorial & Tips** (Educational)
   - "3 tricks to beat Level 50"
   - "Hidden feature you didn't know about"
   - Format: Quick tips with on-screen annotations

**Instagram Technical Specs**:
- Aspect ratio: 9:16 (vertical) or 1:1 (square)
- Duration: 15-30 seconds (Reels algorithm favors <30s)
- Audio: Trending audio increases reach by 20-30%
- Hashtags: 5-8 per Reel (#gamersofinstagram #mobilegaming)

**Step 3: YouTube Shorts Optimization**

**Content Types YouTube Promotes**:
1. **Tutorial & How-To** (Searchable)
   - "How to unlock [character]"
   - "Best strategy for [level/mode]"
   - Longer format OK (up to 60 seconds)

2. **Compilations** (Watch time)
   - "Top 10 satisfying moments"
   - "Funniest fails compilation"
   - Clips from streams/gameplay

3. **News & Updates** (Timeliness)
   - "New update just dropped!"
   - "Secret code for free gems"
   - Patch notes breakdowns

**YouTube Shorts Technical Specs**:
- Aspect ratio: 9:16 (vertical)
- Duration: Up to 60 seconds (longer than TikTok/Reels)
- Thumbnail: Critical for search visibility (use text overlays)
- Title: Keyword-optimized (appears in search)

**Step 4: Cross-Platform Strategy**

**Content Repurposing Matrix**:
```
| Content Type | TikTok | Instagram | YouTube |
|--------------|--------|-----------|---------|
| ASMR moments | ✅ Primary | ✅ Secondary | ❌ Low reach |
| Skill showcases | ✅ Primary | ⚠️ Works | ✅ Primary |
| Tutorials | ❌ Too slow | ⚠️ Works | ✅ Primary |
| Challenges | ✅ Primary | ✅ Primary | ⚠️ Works |
| Compilations | ⚠️ Works | ❌ Low engagement | ✅ Primary |
```

**Platform Prioritization** (by genre):
- **Hyper-casual**: TikTok > Instagram > YouTube (ASMR, satisfying moments)
- **Social casual**: Instagram > TikTok > YouTube (challenges, aesthetic)
- **Mid-core**: YouTube > TikTok > Instagram (tutorials, strategy guides)
- **Competitive**: TikTok > YouTube > Instagram (skill showcases, tournaments)

**Output Format**:
1. Platform algorithm priorities table
2. Content type examples with view benchmarks
3. Technical specs checklist (aspect ratio, duration, hashtags)
4. Cross-platform repurposing matrix
5. Platform prioritization by genre

**Evidence tier**: STRONG (cite TikTok Creator Portal 2025, Instagram Business Blog, YouTube Creator Academy)

---

#### 3. **competitor-viral-analyzer** (opus, 32K)

**Research Objective**: Analyze top viral games' share mechanics and K-factor strategies

**Step 1: Viral Game Case Studies** (Top 10 by genre)

**Case Study 1: Among Us** (K-factor: 1.2-1.8 peak)

**Viral Mechanics**:
- **Built-in recording**: Auto-capture "killer reveal" moments
- **Friend lobbies**: 4-10 player lobbies require friend invites
- **Asymmetric gameplay**: Different roles create shareable moments
- **Meme potential**: "Sus" moments are inherently funny

**Share Features**:
- Discord integration (one-tap invite to voice chat)
- Custom lobby codes (easy to share via text)
- Post-game summary (shareable victory/defeat screens)

**K-Factor Components**:
- i = 6.0 (players invite 4-10 friends to fill lobbies)
- c = 0.25 (25% of invited friends install, game was trending)
- t = 1.0 (instant lobbies, same-day viral cycle)
- K = 6.0 × 0.25 × 1.0 = 1.5 (exponential growth)

**Case Study 2: Stumble Guys** (K-factor: 0.8-1.2)

**Viral Mechanics**:
- **Fail compilation**: Auto-record funny ragdoll physics fails
- **Party mode**: 2-4 player squads (requires friend invites)
- **Custom games**: Create private lobbies with friends
- **Emotes**: Victory dances and taunts (shareable)

**Share Features**:
- One-tap TikTok export (auto-formatted 9:16 clips)
- Friend leaderboards (social proof, "beat my score")
- Squad invites via push notifications

**K-Factor Components**:
- i = 4.0 (squad invites + challenge shares)
- c = 0.20 (20% conversion, mobile-first audience)
- t = 0.95 (1-2 day viral cycle)
- K = 4.0 × 0.20 × 0.95 = 0.76 (sub-viral but high organic growth)

**Case Study 3: Brawl Stars** (K-factor: 0.6-0.9)

**Viral Mechanics**:
- **Club recruitment**: Guild system requires friend invites
- **Duo/Trio modes**: Team-based matches (2-3 players)
- **Friend battles**: Custom matches with friends
- **Replay system**: Save and share epic plays

**Share Features**:
- In-game replay viewer (no external app needed)
- Club chat (built-in social network)
- Friend suggestions (based on skill level)

**K-Factor Components**:
- i = 3.5 (club invites + duo mode)
- c = 0.18 (18% conversion, competitive game)
- t = 0.90 (2-3 day viral cycle, longer onboarding)
- K = 3.5 × 0.18 × 0.90 = 0.57 (strong organic UA)

**Step 2: Share Mechanics Teardown**

**Common Patterns Across Viral Games**:
1. **Multiplayer lobbies** (Among Us, Stumble Guys, Brawl Stars)
   - Requires friend invites to fill lobbies
   - Natural sharing trigger (can't play alone)

2. **Auto-capture moments** (Among Us, Stumble Guys)
   - Game records shareable moments automatically
   - No manual recording needed (frictionless)

3. **Friend leaderboards** (Stumble Guys, Brawl Stars)
   - Social proof ("I'm better than my friends")
   - Challenge mechanic ("Beat my score!")

4. **Guild/Club systems** (Brawl Stars, Clash Royale)
   - Long-term social retention
   - Guild recruitment drives invites

5. **Asymmetric gameplay** (Among Us)
   - Different roles create unique stories
   - High meme potential (shareable moments)

**Step 3: K-Factor Estimation from Growth Data**

Using App Annie / Sensor Tower DAU growth curves:

**Among Us** (Aug-Nov 2020 peak):
- DAU: 100K → 3.5M in 60 days
- Growth rate: 35x in 60 days
- Implied K-factor: 1.5-1.8 (exponential phase)

**Stumble Guys** (2022 launch):
- DAU: 500K → 5M in 90 days
- Growth rate: 10x in 90 days
- Implied K-factor: 0.8-1.2 (super-linear growth)

**Brawl Stars** (2018-2020):
- DAU: 1M → 8M in 12 months (steady growth)
- Growth rate: 8x in 365 days
- Implied K-factor: 0.6-0.9 (organic UA + paid)

**Output Format**:
1. Case studies (3-5 viral games) with K-factor analysis
2. Share mechanics teardown (common patterns)
3. K-factor component breakdown (i, c, t values)
4. Growth curve analysis (DAU over time)
5. Actionable insights for genre

**Evidence tier**: STRONG (cite App Annie Top Charts, Sensor Tower DAU data, official game stats)

---

#### 4. **share-psychology-researcher** (sonnet, 16K)

**Research Objective**: Understand psychological triggers for organic game sharing

**Step 1: Jonah Berger's STEPPS Framework**

**STEPPS = 6 Principles of Virality**:

1. **Social Currency** — Sharing makes me look good
   - Game: Unlock rare achievement, top leaderboard rank
   - Share trigger: "Look what I accomplished!"
   - Example: Dark Souls "I beat the boss!" screenshots

2. **Triggers** — Top-of-mind = tip-of-tongue
   - Game: Daily streak, limited-time event
   - Share trigger: Reminder to share (push notification)
   - Example: Wordle daily puzzle (everyone plays at same time)

3. **Emotion** — High-arousal emotions drive sharing
   - Positive: Awe, excitement, amusement (funny fails)
   - Negative: Anger, anxiety (controversial moments)
   - Game: Epic clutch victory, hilarious fail, impossible challenge
   - Example: Fortnite Victory Royale (adrenaline rush)

4. **Public** — Make private behavior public
   - Game: Public leaderboards, visible status symbols
   - Share trigger: "Everyone can see I'm #1"
   - Example: Pokemon GO gym badges (visible to all players)

5. **Practical Value** — Useful information spreads
   - Game: Tips, tricks, hidden secrets
   - Share trigger: "This will help my friends"
   - Example: "Secret code for 1000 free gems!" (viral)

6. **Stories** — People share narratives, not ads
   - Game: Memorable moments with story arc
   - Share trigger: "You won't believe what happened..."
   - Example: Among Us betrayal stories, Minecraft adventures

**Step 2: Player Motivations for Sharing**

**Quantic Foundry Gamer Motivations** (relevant to sharing):

1. **Competition** (25% of players, high share rate)
   - Motivation: "I want to prove I'm better"
   - Share content: Leaderboard ranks, tournament wins, skill showcases
   - Example: Fighting game replays, speedrun records

2. **Achievement** (35% of players, medium share rate)
   - Motivation: "I want to show my progress"
   - Share content: 100% completion, rare unlocks, milestone badges
   - Example: "I finally beat the final boss after 50 tries!"

3. **Social** (15% of players, high share rate)
   - Motivation: "I want to play with friends"
   - Share content: Guild recruitment, co-op invites, friend challenges
   - Example: "Join my guild! We need 5 more players for raid"

4. **Immersion** (20% of players, low share rate)
   - Motivation: "I want to experience the story"
   - Share content: Story moments, emotional scenes (rare)
   - Example: The Last of Us story reactions (not gameplay)

5. **Creativity** (5% of players, very high share rate)
   - Motivation: "I want to create and share"
   - Share content: Custom levels, art, mods, replays
   - Example: Minecraft builds, Mario Maker levels

**Step 3: Sharing Barriers & Friction Points**

**Why Players DON'T Share** (remove these barriers):
1. **Friction**: Too many steps (open app → record → edit → post)
2. **Embarrassment**: Fear of looking bad ("What if I'm not good enough?")
3. **Privacy**: Don't want friends to know they play mobile games
4. **Effort**: Recording/editing takes too long
5. **Timing**: Moment passed before they could share

**Friction Reduction Strategies**:
- **Auto-capture**: Game records moments automatically (no manual recording)
- **One-tap share**: Single button to post (no editing required)
- **Private challenges**: Share with select friends only (not public)
- **Pre-formatted templates**: Game generates caption and thumbnail

**Step 4: Organic vs Incentivized Sharing**

**Organic Sharing** (Authentic, high engagement):
- Player chooses to share without rewards
- Motivated by pride, humor, social connection
- Examples: Victory screenshots, funny fails, friend challenges
- Engagement: High (friends watch full video)

**Incentivized Sharing** (Lower authenticity, risk of spam):
- Player rewarded for sharing (coins, gems, lives)
- Motivated by rewards, not genuine interest
- Examples: "Share to get 5 extra lives"
- Engagement: Low (friends ignore spam)

**Best Practice**: Blend organic + light incentives
- Primary: Make organic sharing satisfying (auto-capture, templates)
- Secondary: Small incentive for first share (one-time bonus)
- Avoid: Aggressive rewards (spam, fake engagement)

**Output Format**:
1. STEPPS framework applied to game mechanics
2. Player motivation mapping (Quantic Foundry types)
3. Sharing barriers and friction reduction strategies
4. Organic vs incentivized sharing trade-offs
5. Psychological trigger recommendations

**Evidence tier**: MEDIUM (cite Jonah Berger's "Contagious", Quantic Foundry player motivations, viral marketing research)

---

### Phase 2: Mechanics Design (Priority 20, Parallel)

**Wave 2 Agents** (3 parallel):

#### 1. **built-in-viral-designer** (opus, 32K)

**Design Objective**: Engineer viral mechanics directly into core gameplay loop

**Built-in Viral Mechanics** (5 Categories):

**1. Perfect Run Recording** (Auto-capture best moments)

**Concept**: Game automatically records player's best performances

**Implementation**:
- **Trigger**: Record when player achieves new personal best
- **Format**: 10-15 second highlight reel (not full session)
- **Content**:
  - Pre-game: 2 seconds (player prepares)
  - Peak moment: 6-8 seconds (the achievement)
  - Post-game: 2 seconds (celebration animation)
- **Export**: Auto-formatted for TikTok (9:16), Instagram (1:1), YouTube (16:9)
- **Storage**: Store last 10 recordings (auto-delete old ones)

**Example (Match-3 game)**:
- Trigger: Player clears 50+ tiles in one combo
- Recording:
  - [2s] Board state before match
  - [6s] Cascade animation (slow-motion)
  - [2s] Score celebration ("+5000 points!" text)
- Export: TikTok-ready 10-second clip with ASMR sounds

**Privacy**: Player previews before sharing (opt-in)

---

**2. Challenge Creator** (Design custom challenges for friends)

**Concept**: Players create challenges and invite friends to beat them

**Implementation**:
- **Challenge Types**:
  - Score challenge: "Beat my score of 8,500"
  - Speed challenge: "Complete level in under 60 seconds"
  - Perfect challenge: "Complete with 0 mistakes"
  - Custom level: "Try this level I designed"
- **Flow**:
  - Player: Create challenge → Invite friends → Wait for results
  - Friend: Accept challenge → Play → Share result
- **Rewards**:
  - Winner: Bragging rights badge
  - Creator: Bonus if many friends attempt (incentivize challenge creation)

**Example (Arcade game)**:
- Player achieves 10,000 points on Level 15
- Game prompts: "Challenge your friends to beat 10,000!"
- Player taps "Create Challenge" → Sends push notification to 5 friends
- Friends compete → Results displayed in leaderboard
- Winner gets "Challenge Champion" badge (shareable)

**Viral Loop**:
```
Player 1 creates challenge → Invites 5 friends → 3 friends accept → 2 friends create own challenges → Invites 10 more friends
K-factor = 0.6-1.2 (depending on acceptance rate)
```

---

**3. Satisfying Moments Compilation** (ASMR-friendly exports)

**Concept**: Game compiles satisfying moments into shareable clips

**Satisfying Moment Types**:
- **Visual**:
  - Smooth animations (cascading matches)
  - Particle effects (explosions, sparkles)
  - Color harmony (rainbow gradients)
  - Symmetry (perfect patterns)
- **Audio**:
  - ASMR sounds (tapping, slicing, popping)
  - Whoosh effects (fast movement)
  - Chimes (achievement unlocks)
  - Musical feedback (notes on actions)

**Auto-Compilation Logic**:
- Game tracks "satisfying score" per action
  - Perfect combo: +100 satisfying points
  - Rainbow cascade: +80 satisfying points
  - Symmetrical pattern: +60 satisfying points
- When player accumulates 500+ satisfying points in one session → Compile highlights
- Export as 15-second TikTok clip (most satisfying moments back-to-back)

**Example (Sorting game)**:
- 5 perfect sorts in a row (ASMR tapping sounds)
- Rainbow color cascade (smooth animation)
- Final object snaps into place (satisfying chime)
- Text overlay: "Perfectly sorted ✨"
- Export: TikTok 9:16 with caption "So satisfying! 🎨"

---

**4. Streak Badges** (Shareable achievements)

**Concept**: Long-term achievements that players want to brag about

**Streak Types**:
- Daily login streak: 7, 30, 100, 365 days
- Win streak: 5, 10, 25 wins in a row
- Perfect streak: 10 levels completed with 3 stars
- Challenge streak: 5 friend challenges won

**Share-Worthy Design**:
- **Visual**: Badge with animated effects (gold shimmer, particle trail)
- **Rarity**: Show % of players who achieved (e.g., "Only 2% reached 100-day streak!")
- **Milestone notifications**: Push notification on day 99 ("1 day until 100-day badge!")
- **Social proof**: Badge displayed on profile (visible to friends)

**Example (Puzzle game)**:
- Player hits 30-day login streak
- Game shows celebration screen: "🔥 30-Day Streak!"
- Auto-generates shareable card:
  - Background: Gradient with streak flames
  - Text: "I've played for 30 days straight!"
  - Badge: Golden trophy with "30" number
  - Call-to-action: "Can you beat my streak?"
- Player shares to Instagram Stories

---

**5. Before/After Transformations** (Progress showcases)

**Concept**: Visualize player progress over time (satisfying transformation)

**Transformation Types**:
- Character evolution: Level 1 character → Level 100 character
- Base building: Starter base → Endgame base
- Skill progression: Beginner gameplay → Pro gameplay (side-by-side)
- Collection showcase: "I unlocked all 50 characters!"

**Implementation**:
- **Auto-snapshot**: Game takes screenshot at key milestones (Level 1, 10, 25, 50, 100)
- **Time-lapse**: Compile snapshots into 10-second time-lapse video
- **Text overlay**: "Day 1 vs Day 90" with date stamps
- **Export**: TikTok-ready with trending audio

**Example (Idle game)**:
- Player starts with simple farm (Day 1)
- After 30 days, farm is massive city
- Game compiles 30 snapshots into 15-second time-lapse
- Text overlay: "30 days of progress 🚀"
- Player shares to TikTok with #idlegame #satisfying

---

**Output Format**:
1. **Built-in viral mechanics** (5 types with implementation details)
2. **Technical requirements** (recording engine, storage limits, export formats)
3. **Privacy considerations** (opt-in sharing, preview before post)
4. **K-factor contribution** (estimated viral lift per mechanic)
5. **UI mockups** (share button placement, preview screens)

---

#### 2. **share-ux-designer** (opus, 32K)

**Design Objective**: Create frictionless, one-tap sharing with platform-optimized templates

**Share UX Design** (4 Components):

**1. One-Tap Share Flows** (Minimize friction)

**Current Friction** (typical mobile game):
```
1. Finish achievement
2. Screenshot manually
3. Open photo editor
4. Crop/edit screenshot
5. Open TikTok app
6. Upload video
7. Write caption
8. Add hashtags
9. Post
Total: 9 steps, 3-5 minutes
```

**Optimized Flow** (one-tap):
```
1. Finish achievement
2. Tap "Share to TikTok" button
3. Preview post (with auto-generated caption)
4. Tap "Post"
Total: 4 steps, 10 seconds
```

**Implementation**:
- **Share button placement**:
  - After achievement (victory screen, level complete)
  - On profile page (share profile card)
  - In replay viewer (share replay)
- **Platform integrations**:
  - TikTok SDK (direct upload, no app switch)
  - Instagram API (Reels upload)
  - System share sheet (fallback for other platforms)
- **Auto-generation**:
  - Video: Pre-rendered highlight reel (10-15 seconds)
  - Caption: Auto-generated text with game title and CTA
  - Hashtags: Pre-filled (#gamename #mobilegaming #genre)
  - Thumbnail: Custom-generated image (see next section)

**Example (Victory screen)**:
- Player finishes level with 3 stars
- Victory screen shows: [Replay] [Share] [Next Level]
- Player taps "Share" → Platform picker (TikTok, Instagram, X)
- Player selects TikTok → Preview screen shows:
  - Video: 10-second highlight reel
  - Caption: "I just beat Level 50 with 3 stars! 🌟 Can you do it?"
  - Hashtags: #GameName #PuzzleGame #MobileGaming
- Player taps "Post" → Video uploads directly (no app switch)
- Confirmation: "Posted to TikTok! 🎉"

---

**2. Custom Thumbnail Generation** (Visual appeal)

**Concept**: Auto-generate eye-catching thumbnails for shares

**Thumbnail Templates** (by content type):

**Achievement Thumbnail**:
- Background: Gradient matching game theme
- Icon: Large achievement badge/trophy
- Text: "LEVEL 100 COMPLETED!" (bold, readable)
- Player stats: Score, time, stars
- Logo: Small game logo in corner

**Challenge Thumbnail**:
- Split-screen: Creator photo vs blank (for friend)
- Text: "CAN YOU BEAT MY SCORE?"
- Score: Large number (e.g., "8,500")
- CTA: "Tap to accept challenge"

**Transformation Thumbnail**:
- Side-by-side: Before vs After
- Text: "DAY 1 VS DAY 90"
- Arrow: Showing progression
- Satisfying visual contrast

**Technical Implementation**:
- **Template engine**: 10-15 pre-designed templates
- **Dynamic text**: Player name, score, achievement
- **Image composition**: LayerCake rendering (text overlays, filters)
- **Export**: 1080x1920 (9:16) or 1080x1080 (1:1)
- **Customization**: Player can choose from 3-5 template variants

**Example (Sorting game)**:
- Template: Pastel gradient background
- Text: "I SORTED 1,000 OBJECTS!" (white bold text)
- Icon: Sorting icon with sparkles
- Player name: "@username" (bottom right)
- Logo: Game logo (top left corner)
- Export: 1080x1920 TikTok thumbnail

---

**3. Social Media Template Specifications** (Platform-optimized)

**TikTok Template**:
```
Video Format:
- Aspect ratio: 9:16 (1080x1920 px)
- Duration: 7-15 seconds (optimal completion rate)
- FPS: 30 fps (smooth animations)
- Codec: H.264 (TikTok standard)

Audio:
- Include game sounds (ASMR-friendly)
- Optional: Trending audio overlay (if licensed)
- Volume: -14 LUFS (TikTok audio normalization)

Captions:
- On-screen text: Large, readable (80% watch without sound)
- Position: Center or lower-third
- Style: Bold sans-serif (Arial, Helvetica)

Hashtags:
- Format: "#GameName #Genre #Trending"
- Count: 3-5 hashtags (TikTok algorithm prefers 3-5)

CTA:
- Text: "Can you beat this?" or "Try it now!"
- Position: End of video (last 2 seconds)
```

**Instagram Reels Template**:
```
Video Format:
- Aspect ratio: 9:16 or 1:1 (Reels supports both)
- Duration: 15-30 seconds (Reels algorithm favors <30s)
- FPS: 30 fps
- Codec: H.264

Audio:
- Trending audio: Use trending sounds for reach
- Volume: -14 LUFS

Captions:
- On-screen text: Minimal (users prefer audio on)
- Position: Top or bottom

Hashtags:
- Format: Mix of broad and niche (#Gaming #PuzzleGame #GameName)
- Count: 5-8 hashtags

CTA:
- Text: "Link in bio" or "DM for code"
- Position: End screen
```

**YouTube Shorts Template**:
```
Video Format:
- Aspect ratio: 9:16 (1080x1920 px)
- Duration: Up to 60 seconds (longer than TikTok/Reels)
- FPS: 60 fps (YouTube supports high FPS)
- Codec: H.264

Audio:
- Clear voiceover or captions
- Music: Royalty-free (YouTube Content ID strict)

Title:
- Keyword-optimized: "How to Beat Level 50 in [Game Name]"
- Length: 50-60 characters

Thumbnail:
- Critical: Custom thumbnail (text + image)
- Size: 1280x720 (16:9, YouTube standard)

CTA:
- Text: "Subscribe for more tips!"
- Position: End screen with subscribe button
```

---

**4. Share Trigger Design** (When/where to prompt)

**Share Trigger Matrix**:

| Trigger Event | Timing | Share Prompt Type | Expected Share Rate |
|---------------|--------|-------------------|---------------------|
| **Victory** | Immediately after level complete | "Share your victory!" | 8-15% |
| **Achievement unlocked** | After rare achievement | "Show off your badge!" | 10-20% |
| **High score** | After beating personal best | "Challenge your friends!" | 12-18% |
| **Streak milestone** | On day 7, 30, 100 streaks | "Celebrate your streak!" | 15-25% |
| **Friend challenge won** | After winning challenge | "Brag about your win!" | 20-30% |
| **Perfect run** | After flawless execution | "Share your perfect run!" | 10-15% |

**Best Practices**:
- **Timing**: Show prompt within 3 seconds of trigger event (strike while emotion is hot)
- **Frequency cap**: Max 1 share prompt per session (avoid spam)
- **Dismissible**: Easy to close (X button, swipe down)
- **Preview**: Show what will be shared (build trust)
- **Incentive**: Optional small reward for first share (one-time 50 gems)

**Bad Practices to Avoid**:
- ❌ Forced sharing (must share to progress)
- ❌ Fake rewards ("Share to unlock" but no unlock)
- ❌ Spam prompts (every action triggers share prompt)
- ❌ Misleading previews (shows different content than what's shared)

**Example Share Prompt**:
```
[Victory screen after Level 50 complete]

┌────────────────────────────────────┐
│   ⭐⭐⭐ LEVEL 50 COMPLETE! ⭐⭐⭐    │
│                                    │
│   Score: 12,500 (New Record! 🔥)   │
│                                    │
│   [🎥 Share Victory]               │
│   [Next Level]                     │
│                                    │
│   Share your epic win on TikTok!  │
│   (Get 50 bonus gems for first    │
│    share)                          │
└────────────────────────────────────┘

Tap "Share Victory" → Preview screen → Post to TikTok
Tap "Next Level" → Continue playing
```

---

**Output Format**:
1. **One-tap share flows** (step-by-step UX diagrams)
2. **Custom thumbnail templates** (10-15 designs with specs)
3. **Platform-specific specifications** (TikTok, Instagram, YouTube)
4. **Share trigger matrix** (when/where to prompt)
5. **UI mockups** (share buttons, preview screens, confirmation)
6. **Technical requirements** (SDK integrations, APIs, storage)

---

#### 3. **challenge-mode-designer** (sonnet, 16K)

**Design Objective**: Create friend-vs-friend challenge system to drive invites

**Challenge System Design**:

**1. Challenge Types**

**Score Challenge**:
- Creator: Achieves score X on level Y
- Prompt: "Challenge friends to beat X!"
- Friend: Attempts same level, tries to beat score X
- Result: Winner displayed on shared leaderboard
- Reward: Winner gets badge, creator gets "challenge master" points

**Speedrun Challenge**:
- Creator: Completes level in T seconds
- Prompt: "Can your friends beat your time?"
- Friend: Attempts to complete level faster
- Result: Time leaderboard (fastest to slowest)
- Reward: Fastest time gets "Speedrunner" badge

**Perfect Challenge**:
- Creator: Completes level with 0 mistakes
- Prompt: "Perfect run! Challenge friends!"
- Friend: Attempts perfect run
- Result: Pass/fail (no mistakes = pass)
- Reward: All who pass get "Perfect" badge

**Custom Level Challenge**:
- Creator: Designs custom level (if game supports level editor)
- Prompt: "Share your level!"
- Friend: Plays custom level, rates difficulty
- Result: Level popularity score
- Reward: Creator gets currency based on plays

---

**2. Challenge Flow (UX)**

**Creator Flow**:
```
1. Player achieves score (e.g., 10,000 on Level 15)
2. Game shows prompt: "🏆 Challenge your friends to beat 10,000!"
3. Player taps "Create Challenge"
4. Friend picker: Select 1-10 friends (or share link)
5. Push notification sent: "@Player challenged you! Can you beat 10,000?"
6. Challenge created, waiting for responses
7. Results page: Shows who attempted, who won
```

**Friend Flow (Accepter)**:
```
1. Friend receives push notification: "Challenge from @Player!"
2. Friend taps notification → Opens game
3. Game shows challenge screen:
   - "@Player scored 10,000 on Level 15"
   - "Your best: 8,500"
   - [Accept Challenge] [Decline]
4. Friend taps "Accept Challenge" → Starts level
5. Friend plays level → Scores 10,500 (wins!)
6. Victory screen: "You beat @Player's score! 🎉"
7. Friend can share victory or create counter-challenge
```

---

**3. Challenge Leaderboards**

**Challenge-Specific Leaderboard**:
- Shows all friends who attempted challenge
- Ranked by score (descending) or time (ascending)
- Visual indicators:
  - 🥇 Gold: Top scorer (beat creator)
  - 🥈 Silver: 2nd place
  - 🥉 Bronze: 3rd place
  - 👑 Crown: Creator (original challenger)
- Tap player name → Challenge them back

**Example Leaderboard**:
```
┌────────────────────────────────────┐
│  CHALLENGE: Beat 10,000 on Lv 15   │
├────────────────────────────────────┤
│  🥇 @Friend2      12,500           │
│  🥈 @Friend1      10,500           │
│  👑 @You          10,000 (Creator) │
│  🥉 @Friend3       9,800           │
│  @Friend4          8,500           │
│  @Friend5       Pending...         │
└────────────────────────────────────┘

[Challenge Back] [Share Results]
```

---

**4. Asymmetric Challenges** (Different roles)

**Concept**: Creator and friend play different roles (more engaging)

**Examples**:

**Hide & Seek Challenge**:
- Creator: Hides object in level
- Friend: Finds hidden object
- Result: Time to find (faster = winner)

**Defense vs Offense**:
- Creator: Builds defense (tower defense game)
- Friend: Attacks defense
- Result: Can friend break through?

**Race Track Creator**:
- Creator: Designs race track
- Friend: Completes track as fast as possible
- Result: Fastest time wins

**Asymmetric Benefit**:
- More replay value (can play both roles)
- More shareable (unique experience)
- Higher K-factor (requires friend to play opposite role)

---

**5. Tournament Brackets** (Multi-round challenges)

**Concept**: 4-16 player tournaments with bracket elimination

**Format**:
- Round 1: 8 players → 4 winners (quarterfinals)
- Round 2: 4 players → 2 winners (semifinals)
- Round 3: 2 players → 1 winner (finals)

**Progression**:
- Each round lasts 24-48 hours
- Players notified when their match starts
- Async gameplay (play anytime within time limit)

**Example (8-player tournament)**:
```
Round 1:
- Match 1: @You (10,000) vs @Friend1 (8,500) → You win
- Match 2: @Friend2 (12,000) vs @Friend3 (9,000) → Friend2 wins
- Match 3: @Friend4 (11,000) vs @Friend5 (11,500) → Friend5 wins
- Match 4: @Friend6 (9,500) vs @Friend7 (10,500) → Friend7 wins

Round 2 (Semifinals):
- Match 1: @You (10,000) vs @Friend2 (12,000) → Friend2 wins
- Match 2: @Friend5 (11,500) vs @Friend7 (10,500) → Friend5 wins

Round 3 (Finals):
- @Friend2 (13,000) vs @Friend5 (12,500) → Friend2 wins! 🏆
```

**Rewards**:
- Winner: Trophy, exclusive badge, in-game currency
- Runner-up: Silver badge
- All participants: Participation reward (small currency bonus)

---

**6. Matchmaking Logic** (Fair challenges)

**Skill-Based Matchmaking**:
- Match players of similar skill level
- Use player rating (Elo-like system)
- Avoid mismatches (beginner vs expert)

**Example**:
- Player A: Rating 1500 (intermediate)
- System suggests friends with rating 1400-1600
- Avoids suggesting friend with rating 2000 (too hard)

**Benefit**: Fair challenges → higher acceptance rate → higher K-factor

---

**7. Reward Structure** (Incentivize participation)

**For Creator**:
- 10 gems per friend who attempts challenge (max 100 gems/day)
- "Challenge Master" badge after 10 challenges created
- Leaderboard: Top challenge creators (most attempts)

**For Friend (Accepter)**:
- 50 gems for accepting challenge (one-time per friend)
- 100 gems bonus for winning challenge
- Victory badge (shareable)

**For Both**:
- Social XP: Levels up "Friend Level" (unlocks perks)
- Mutual rewards: Both get bonus if 5+ friends participate

**Balance**: Rewards should encourage participation, not spam
- Cap: Max 10 challenges per day (avoid spam)
- Cooldown: Can't challenge same friend twice in 24 hours

---

**Output Format**:
1. **Challenge types** (4-5 types with rules)
2. **Challenge flow diagrams** (creator and friend flows)
3. **Leaderboard designs** (UI mockups)
4. **Asymmetric challenge examples** (3-5 ideas)
5. **Tournament bracket system** (if applicable)
6. **Matchmaking logic** (skill-based or random)
7. **Reward structure** (gems, badges, XP)
8. **K-factor contribution** (estimated viral lift from challenges)

---

### Phase 3: Content Strategy (Priority 30, Parallel)

**Wave 3 Agents** (2 parallel):

#### 1. **tiktok-content-strategist** (opus, 32K)

**Strategy Objective**: Create 4-week TikTok content calendar with concrete hooks

**TikTok Content Calendar** (Week 1-4):

**Week 1: Launch Phase** (Build awareness)

**Day 1-2**: ASMR Moments
- Hook: "POV: The most satisfying level clear 😌"
- Content: 10-second level clear with cascading animations
- Sound: ASMR tapping, whoosh effects, chimes
- Hashtags: #ASMR #Satisfying #MobileGaming #GameName
- CTA: "Download to try it yourself!"

**Day 3-4**: Impossible → Possible Transition
- Hook: "I failed this level 50 times… then THIS happened"
- Content: Split-screen (left: fails, right: success)
- Format:
  - [0-5s] Montage of fails (frustration)
  - [5-7s] Transition effect (screen wipe)
  - [7-12s] Perfect execution (triumph)
- Sound: Dramatic music buildup
- Hashtags: #Gaming #ChallengeAccepted #Victory
- CTA: "Can you beat Level 50?"

**Day 5-7**: Skill Showcase
- Hook: "Watch me beat the hardest level with 0 mistakes"
- Content: Full playthrough of difficult level (sped up 2x)
- Format: 15 seconds (30-second gameplay compressed)
- Text overlay: "Only 2% of players can do this"
- Hashtags: #ProGamer #SkillCheck #HardMode
- CTA: "Are you in the 2%?"

---

**Week 2: Engagement Phase** (Build community)

**Day 8-10**: Challenge Mode
- Hook: "I challenge YOU to beat my score 🏆"
- Content: Player's high score + challenge invitation
- Format:
  - [0-3s] Score reveal (large number)
  - [3-8s] Gameplay highlights
  - [8-10s] Challenge screen with QR code
- Sound: Upbeat music
- Hashtags: #Challenge #BeatMyScore #FYP
- CTA: "Scan QR code to accept challenge!"

**Day 11-13**: Behind-the-Scenes
- Hook: "How this game is made (dev team vlog)"
- Content: Office tour, whiteboard sketches, playtesting
- Format: Fast-paced montage (TikTok loves BTS content)
- Sound: Trending audio
- Hashtags: #GameDev #IndieGame #BehindTheScenes
- CTA: "Follow for more dev updates!"

**Day 14**: User-Generated Content (UGC)
- Hook: "Your best moments this week! 🌟"
- Content: Compilation of user-submitted clips
- Format: 3-5 second clips × 4-5 users
- Text overlay: "@username absolutely crushing it!"
- Hashtags: #Community #UGC #FanLove
- CTA: "Tag us for a chance to be featured!"

---

**Week 3: Viral Push** (Maximize reach)

**Day 15-17**: Before/After Transformation
- Hook: "Day 1 vs Day 30... the glow-up is REAL"
- Content: Side-by-side comparison (starter → endgame)
- Format:
  - [0-5s] Day 1 (simple character/base)
  - [5-7s] Transition (calendar pages flip)
  - [7-12s] Day 30 (maxed character/base)
- Sound: Trending glow-up audio
- Hashtags: #GlowUp #Transformation #Progress
- CTA: "Start your journey today!"

**Day 18-20**: Funny Fails Compilation
- Hook: "These fails are PAINFUL to watch 😂"
- Content: Ragdoll physics fails, mistimed jumps, epic fumbles
- Format: 3-second clips × 5 fails
- Sound: Comedic sound effects (boink, crash)
- Hashtags: #Fails #Funny #Gaming
- CTA: "Don't let this be you, download now!"

**Day 21**: Trend Participation
- Hook: (Use trending audio/challenge format)
- Content: Game-themed version of trending meme
- Example: "Tell me you're a mobile gamer without telling me" → Show game UI
- Sound: Trending audio (changes weekly)
- Hashtags: #Trending #FYP #Viral
- CTA: Implicit (trend participation = discovery)

---

**Week 4: Retention Phase** (Keep audience engaged)

**Day 22-24**: Tutorial/Tips
- Hook: "3 tricks the devs don't want you to know 🤫"
- Content: Hidden features, secret combos, pro tips
- Format:
  - [0-3s] Hook (text overlay)
  - [3-6s] Tip 1 (quick demo)
  - [6-9s] Tip 2
  - [9-12s] Tip 3
- Sound: Mysterious music
- Hashtags: #Tips #LifeHack #ProTips
- CTA: "Save this for later!"

**Day 25-27**: Leaderboard Showcase
- Hook: "The #1 player in the world is INSANE"
- Content: Spectate top player's gameplay
- Format: 10-second highlight reel of #1 player
- Text overlay: "Rank #1: @TopPlayer - 500,000 points"
- Hashtags: #Leaderboard #Top1 #Champion
- CTA: "Can you dethrone the king?"

**Day 28-30**: Community Event Teaser
- Hook: "HUGE update dropping next week! 🚀"
- Content: Sneak peek of new features
- Format:
  - [0-3s] "Coming soon..." text
  - [3-8s] Quick cuts of new content (no full reveals)
  - [8-10s] "Stay tuned!" + countdown
- Sound: Epic trailer music
- Hashtags: #Update #NewContent #ComingSoon
- CTA: "Turn on notifications!"

---

**TikTok Hook Examples** (10-15 concrete examples):

1. **ASMR Hook**: "POV: You clear 100 tiles at once 😌" (cascading animation, satisfying sounds)
2. **Fail → Win Hook**: "50 attempts later... FINALLY! 🎉" (split-screen fail montage → success)
3. **Skill Hook**: "Only 1% can beat this level without power-ups" (difficult level showcase)
4. **Challenge Hook**: "I bet you can't beat my score of 15,000" (challenge screen + QR code)
5. **Transformation Hook**: "Level 1 me vs Level 100 me" (character evolution side-by-side)
6. **Funny Fail Hook**: "This is the worst fail I've ever seen 😂" (ragdoll physics fail)
7. **Secret Hook**: "This hidden combo breaks the game 🤫" (secret mechanic reveal)
8. **Record Hook**: "I just set the WORLD RECORD! 🏆" (leaderboard #1 proof)
9. **Trend Hook**: "Tell me you're addicted without telling me" → Shows 500-day streak
10. **Drama Hook**: "The dev nerfed my favorite character 😭" (patch notes reaction)
11. **Nostalgia Hook**: "Remember when Level 50 was IMPOSSIBLE?" (old vs new difficulty)
12. **Flex Hook**: "Spent $0 and unlocked everything 💎" (F2P flex)
13. **Lucky Hook**: "This is the luckiest run EVER" (perfect RNG moments)
14. **Speedrun Hook**: "Beat the game in 5 minutes (WR pace)" (speedrun timer overlay)
15. **Cute Hook**: "The animations in this game are SO CUTE 🥺" (wholesome moments)

---

**Hashtag Strategy**:

**Tier 1 - Brand Hashtags** (Always include):
- #GameName
- #GameNameCommunity

**Tier 2 - Genre Hashtags** (High relevance):
- #PuzzleGame
- #MobileGaming
- #IndieGame

**Tier 3 - Trending Hashtags** (Discoverability):
- #FYP (For You Page)
- #Viral
- #Gaming

**Tier 4 - Niche Hashtags** (Targeted):
- #ASMR (for satisfying content)
- #Speedrun (for skill showcases)
- #Challenge (for friend challenges)

**Best Practice**: 3-5 hashtags per video (mix of Tier 1-4)

---

**Posting Schedule**:
- **Best times**: 6-9am, 12-2pm, 7-11pm (user's local timezone)
- **Frequency**: 1-2 posts per day (consistency > volume)
- **Days**: 7 days/week (TikTok algorithm rewards daily posting)

**Content Mix**:
- 40%: ASMR & satisfying moments (highest engagement)
- 30%: Skill showcases & challenges (aspirational)
- 20%: Community content (UGC, leaderboards)
- 10%: Tutorials & tips (educational)

---

**Output Format**:
1. **4-week content calendar** (30 days of posts with hooks, formats, hashtags)
2. **10-15 TikTok hook examples** (concrete, actionable)
3. **ASMR moment identification** (specific game sounds/animations)
4. **Hashtag strategy** (tiered system with examples)
5. **Posting schedule** (best times, frequency, content mix)
6. **Technical specs** (aspect ratio, duration, captions)

---

#### 2. **influencer-kit-designer** (sonnet, 16K)

**Kit Objective**: Create comprehensive influencer seeding materials

**Influencer Kit Components**:

**1. Press Kit** (Digital media pack)

**Contents**:
- **Fact Sheet** (1-page PDF):
  - Game name, genre, platform
  - Release date, price (F2P/premium)
  - Key features (3-5 bullet points)
  - Target audience
  - Developer studio info
  - Contact email
- **Screenshots** (10-15 high-res images):
  - Gameplay moments (5 images)
  - Character/environment art (3 images)
  - UI mockups (2 images)
  - Victory/achievement screens (2 images)
- **Logo Pack**:
  - Primary logo (PNG, transparent background)
  - Icon (app store icon, 1024x1024 px)
  - Horizontal lockup (for banners)
  - Monochrome version (black/white)
- **Trailers** (3 videos):
  - 15-second teaser (TikTok/Reels)
  - 30-second gameplay trailer (Instagram)
  - 60-second full trailer (YouTube)
- **GIFs** (5-10 looping clips):
  - Core gameplay loop (3-5 seconds)
  - Power-ups/special moves
  - Character animations
  - Victory celebrations
- **Presskit URL**: Hosted on website (e.g., gamename.com/press)

---

**2. Creator Codes** (Attribution tracking)

**System Design**:
- Each influencer gets unique code (e.g., "STREAMER10")
- Code provides benefit to their audience (10% bonus gems, exclusive skin)
- Tracks:
  - Code redemptions (# of players)
  - Installs attributed to code
  - Retention of code users (D1, D7, D30)
  - Revenue from code users (LTV)

**Example**:
```
Influencer: @TechTokGamer
Code: TECHGAMER10
Benefit: 500 free gems + exclusive "TechTok" badge
Tracking:
  - 5,000 code redemptions
  - 3,500 installs (70% conversion)
  - D7 retention: 25% (above baseline 18%)
  - LTV: $2.50 per user (baseline: $1.80)
Verdict: High-quality traffic, offer more codes
```

**Creator Dashboard**:
- Live stats (redemptions, installs, retention)
- Earnings (if rev-share partnership)
- Downloadable graphics (custom codes as images)

---

**3. Early Access Program**

**Structure**:
- **Tier 1 - Beta Testers** (Nano influencers, 1K-10K followers):
  - Access: 2 weeks before launch
  - Perks: All content unlocked, exclusive badge
  - NDA: Light (can share gameplay, no negative reviews until launch)
  - Deliverable: 1 TikTok post + honest feedback survey
- **Tier 2 - Launch Partners** (Micro influencers, 10K-100K followers):
  - Access: 1 week before launch
  - Perks: Custom creator code, rev-share (5% of attributed revenue)
  - NDA: Embargo until launch day (coordinate simultaneous launch posts)
  - Deliverable: 2 TikTok posts + 1 Instagram Reel + stream (optional)
- **Tier 3 - Flagship Creators** (Macro influencers, 100K-1M+ followers):
  - Access: Same-day launch (coordinated)
  - Perks: Paid sponsorship ($500-5K depending on reach), custom in-game item named after them
  - NDA: Contract-based (specific deliverables)
  - Deliverable: Dedicated video (YouTube), 3 TikToks, stream integration

---

**4. Partnership Tiers** (Compensation structure)

**Tier 1 - Code-Only Partnership** (Free):
- Influencer gets custom code
- No upfront payment
- Earns 5% of revenue from code users (rev-share)
- Best for: Nano influencers, community building

**Tier 2 - Hybrid Partnership** ($100-500 + rev-share):
- Small upfront payment ($100-500)
- Plus 5% rev-share from code users
- Requires: 2-3 content pieces (TikToks, Reels)
- Best for: Micro influencers, proven reach

**Tier 3 - Paid Sponsorship** ($500-5K flat rate):
- Flat fee based on follower count ($0.01-0.05 per follower)
- No rev-share (flat payment only)
- Requires: Dedicated video + 3 short-form posts + stream
- Best for: Macro influencers, launch campaigns

**Example Pricing**:
- Nano (5K followers): Code-only (no upfront cost)
- Micro (50K followers): $250 + 5% rev-share
- Macro (500K followers): $2,500 flat rate (no rev-share)
- Mega (2M followers): $10K flat rate (negotiated)

---

**5. Content Guidelines** (Brand safety)

**Required**:
- ✅ Show actual gameplay (no misleading footage)
- ✅ Disclose partnership (#ad, "sponsored by GameName")
- ✅ Honest opinion (can mention flaws)
- ✅ Credit game in caption (@GameName on TikTok)

**Prohibited**:
- ❌ Fake gameplay (showing competitor's game)
- ❌ Misleading promises ("Get rich quick!")
- ❌ Offensive language (hate speech, slurs)
- ❌ Copyright music (unless licensed)
- ❌ Competitor mentions (no "better than [Game X]")

**Best Practices**:
- Show tutorial (how to get started)
- Highlight unique features (what makes game special)
- Authentic reaction (genuine excitement, not forced)
- Call-to-action (download link in bio, code in caption)

---

**6. Outreach Templates**

**Email Template 1 - Cold Outreach (Nano/Micro)**:
```
Subject: Partnership Opportunity: [Game Name] x @YourHandle

Hi @YourHandle,

We're [Studio Name], creators of [Game Name] - a [genre] mobile game launching on [date].

We've been following your content and think your audience would LOVE our game! Here's why:
- [Feature 1 aligned with their audience]
- [Feature 2 aligned with their content style]
- [Feature 3]

We'd love to send you early access + a custom creator code for your community.

Interested? Reply and I'll send the press kit!

Best,
[Your Name]
[Studio Name]
[Email] | [Website]
```

**Email Template 2 - Paid Partnership (Macro)**:
```
Subject: Paid Sponsorship: [Game Name] Launch Campaign

Hi @CreatorName,

We're launching [Game Name] on [date] and would love to work with you on a paid partnership.

Campaign Details:
- Deliverables: 1 YouTube video (5-10 min) + 3 TikToks
- Compensation: $[Amount] flat rate
- Timeline: Content published on [launch date]
- Creative freedom: We trust your style, just show gameplay!

Press kit attached. Let me know if you're interested and we can discuss terms!

Best,
[Your Name]
```

---

**7. Success Metrics** (Track influencer ROI)

**Per-Influencer Metrics**:
- **Reach**: Views, impressions
- **Engagement**: Likes, comments, shares
- **Conversions**: Code redemptions, installs
- **Retention**: D1, D7, D30 retention of attributed users
- **LTV**: Revenue per user from influencer traffic
- **ROI**: (Revenue from influencer users) / (Cost of partnership)

**Example Dashboard**:
```
Influencer: @TechTokGamer
Campaign: Launch Week

Reach: 500K views
Engagement: 25K likes, 1.2K comments, 800 shares
Conversions: 3,500 installs via code TECHGAMER10
Retention: D1 = 35%, D7 = 25%, D30 = 12%
LTV: $2.50 per user
Revenue: $8,750 (3,500 installs × $2.50 LTV)
Cost: $500 (payment to influencer)
ROI: 17.5x ($8,750 / $500)

Verdict: Excellent ROI, prioritize for future campaigns
```

---

**Output Format**:
1. **Press kit contents** (fact sheet, screenshots, logo pack, trailers)
2. **Creator code system** (attribution tracking, dashboard)
3. **Early access program structure** (3 tiers with perks)
4. **Partnership tiers** (pricing, deliverables, compensation)
5. **Content guidelines** (brand safety, required/prohibited)
6. **Outreach templates** (cold outreach, paid partnership emails)
7. **Success metrics** (per-influencer ROI tracking)

---

### Phase 4: Validation & File Generation (Priority 40)

**file-generator** (sonnet, 16K):

**Dependencies**: Phase 1 (Viral Research) + Phase 2 (Mechanics Design) + Phase 3 (Content Strategy)

**Validation Steps**:

1. **QG-VIRALITY-001: K-Factor Feasibility**
   - Compare calculated K-factor vs genre benchmarks
   - If target exceeds genre max by >20% → Downgrade target or add justification
   - Example: Genre = Casual (max K = 0.8), Target = 1.2 → FAIL (50% above max)

2. **QG-VIRALITY-002: Platform Guidelines Compliance**
   - Check TikTok/Instagram/YouTube policies
   - Flag violations: Forced sharing, fake engagement, spam mechanics
   - Example: "Share to unlock" mechanic → FAIL (forced sharing)

3. **QG-VIRALITY-003: Organic Share Authenticity**
   - Scan for dark patterns (forced sharing, misleading incentives)
   - Validate GAM-004 compliance (ethical monetization)
   - Example: "Share for 1000 gems" → PASS (optional, clear disclosure)

4. **QG-VIRALITY-004: Content Hook Specificity**
   - Count TikTok hooks with concrete examples
   - Require >= 5 hooks with formats, scripts, hashtags
   - Example: "Create engaging content" → FAIL (generic)
   - Example: "10-second ASMR level clear with cascading animation" → PASS (specific)

---

**File Generation** (6 files):

**File 1: `specs/virality.md`** (Master blueprint)
```markdown
# Viral Mechanics Blueprint — [Game Name]

> 🎯 **K-Factor Target**: [X.X] ([Achievable / Stretch Goal / Unrealistic])
> 📱 **Platform Focus**: [TikTok / Instagram / YouTube / Multi-platform]
> 🔥 **Estimated Viral Lift**: +[X]% organic installs

## Executive Summary

[1-2 paragraphs: Current state, viral opportunities, expected impact]

## K-Factor Calculation

**Formula**: K = i × c × t

**Components**:
- **i (Invites per User)**: [X.X] ([Source: friend challenges, tournament invites])
- **c (Conversion Rate)**: [X%] ([Source: warm invites, challenge UX])
- **t (Time Factor)**: [X.X] ([Source: viral cycle speed])

**Baseline K**: [X.X] (current state)
**Optimized K**: [X.X] (with viral mechanics)
**Uplift**: +[X]% vs baseline

**Feasibility**: [Verdict with justification]

## Built-In Viral Mechanics

1. **Perfect Run Recording** — [1-2 sentences]
2. **Challenge Creator** — [1-2 sentences]
3. **Satisfying Moments Compilation** — [1-2 sentences]
4. **Streak Badges** — [1-2 sentences]
5. **Before/After Transformations** — [1-2 sentences]

[See specs/virality/share-features.md for implementation details]

## Share Features

- One-tap share (TikTok SDK integration)
- Custom thumbnail generation (10 templates)
- Social media templates (TikTok, Instagram, YouTube)
- Share triggers (victory, achievement, streak)

[See specs/virality/share-features.md for UX flows]

## Platform Strategy

**Primary Platform**: [TikTok / Instagram / YouTube]
**Content Focus**: [ASMR / Skill showcases / Tutorials]
**Posting Frequency**: [X posts/week]

[See specs/virality/tiktok-hooks.md for content calendar]

## Success Metrics

- **K-Factor**: Track actual K vs target [X.X]
- **Share Rate**: [X]% of players share content
- **Viral Installs**: [X]% of installs from organic shares
- **Content Reach**: [X]M views on TikTok

## Implementation Roadmap

**Phase 1: Foundation** (Weeks 1-2)
- Implement recording engine
- Build share UX flows
- Create thumbnail templates

**Phase 2: Mechanics** (Weeks 3-4)
- Challenge mode system
- Friend leaderboards
- Reward structure

**Phase 3: Content** (Weeks 5-6)
- TikTok content calendar
- Influencer kit
- Press kit materials

**Phase 4: Launch** (Week 7)
- Soft launch with influencers
- Monitor K-factor metrics
- Iterate based on data

---

**See also**:
- specs/virality/share-features.md — Share UX implementation
- specs/virality/challenge-modes.md — Challenge system design
- specs/virality/tiktok-hooks.md — TikTok content strategy
- specs/virality/influencer-kit.md — Influencer partnerships
- specs/virality/social-proof.md — Leaderboards, guilds, social features
```

---

**File 2-6**: See plan Phase 2 for detailed specifications

---

**Output**: 6 markdown files in `specs/virality/` directory

---

## Integration Points

This command integrates with:

1. **`/speckit.games.concept`** — Extract game genre, target audience
2. **`/speckit.gdd`** — Reference core loop, monetization model
3. **`/speckit.games.mechanics`** — Build on existing mechanics (PREREQUISITE)
4. **`/speckit.games.aso`** — Use viral hooks for app store optimization (HANDOFF)
5. **`/speckit.games.analytics`** — Track K-factor, referral metrics (HANDOFF)
6. **`/speckit.balance`** — Validate viral reward economy impact (OPTIONAL)

---

## Cost Estimation

**Per execution** (all agents, full workflow):
- Phase 0: 1 agent × sonnet × 8K = $0.02
- Phase 1: 4 agents × opus × 32K = $0.64 (k-factor, platform, competitor, psychology)
- Phase 2: 3 agents × (2 opus × 32K + 1 sonnet × 16K) = $0.52 (viral designer, share UX, challenge)
- Phase 3: 2 agents × (1 opus × 32K + 1 sonnet × 16K) = $0.20 (TikTok, influencer)
- Phase 4: 1 agent × sonnet × 16K = $0.04

**Total**: ~$1.42 per execution (full workflow, 10 agents)

**Cost by max-model**:
- Opus (default): $1.42
- Sonnet (cost control): $0.60 (3x cheaper, lower quality)
- Haiku (quick draft): $0.20 (7x cheaper, draft quality only)

---

## Success Metrics

Track these metrics post-launch:
- **K-Factor**: Actual vs target (measure monthly)
- **Share Rate**: % of DAU who share content
- **Viral Installs**: % of installs from organic shares (not paid UA)
- **Content Performance**: TikTok views, engagement rate, follower growth
- **Influencer ROI**: Revenue per influencer partnership

**Targets** (by genre):
- Hyper-casual: K = 0.2, Share Rate = 5%
- Social casual: K = 0.6, Share Rate = 10%
- Multiplayer: K = 1.0, Share Rate = 15%

---

## Troubleshooting

**Issue**: K-factor target unrealistic (exceeds genre max by >20%)
**Solution**:
- Downgrade target to genre benchmark + 20%
- Add justification for higher target (unique mechanic, IP advantage)
- Focus on optimizing i, c, t components (see Phase 1, Agent 1)

**Issue**: Platform compliance violations (QG-VIRALITY-002 fails)
**Solution**:
- Review TikTok Community Guidelines, Instagram ToS
- Remove forced sharing mechanics
- Add opt-in preview before posting
- Disclose incentives clearly (#ad, "Earn 50 gems for sharing")

**Issue**: TikTok hooks too generic (QG-VIRALITY-004 fails)
**Solution**:
- Add concrete examples (specific level, format, duration)
- Include scripts or storyboards
- Reference successful viral game examples
- Must have >= 5 specific hooks

**Issue**: Low share rate in production (< 5%)
**Solution**:
- A/B test share prompt timing (victory vs achievement)
- Reduce friction (ensure one-tap share works)
- Improve thumbnail quality (more eye-catching)
- Add small incentive for first share (50 gems one-time)

---

## Related Commands

- **`/speckit.games.concept`** — Generate mobile game concepts with genre variants
- **`/speckit.games.mechanics`** — Design core gameplay mechanics (PREREQUISITE)
- **`/speckit.games.aso`** — App Store Optimization with viral hooks (HANDOFF)
- **`/speckit.games.analytics`** — Track viral metrics and K-factor (HANDOFF)
- **`/speckit.gdd`** — Game Design Document (integrate virality as Section 09)
- **`/speckit.balance`** — Validate viral reward economy (optional)
- **`/speckit.softlaunch`** — Soft launch strategy with influencer seeding

---

## Version History

- **v0.1.0** (2026-01-13): Initial release
  - 10 agents across 4 phases
  - K-factor calculation and benchmarking
  - Built-in viral mechanics (5 types)
  - Share UX optimization (one-tap share, thumbnails)
  - TikTok content strategy (4-week calendar)
  - Influencer seeding kit
  - 4 quality gates (K-factor feasibility, platform compliance, authenticity, specificity)
  - 6 output files (virality.md + 5 subdirectory files)

---

**Next**: After virality design → `/speckit.games.aso` or `/speckit.games.analytics`

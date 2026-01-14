# AQS (Art Quality Score) Rubric v1.0

> **Formal definition of the 30-checkpoint game art pipeline quality scoring system**

---

## Overview

The Art Quality Score (AQS) measures game art pipeline readiness for production across 6 dimensions with 30 individual checkpoints. This rubric ensures art specifications meet world-class mobile game standards before asset creation begins.

**Formula**: `AQS = VisualStyle + AssetCompleteness + AnimationPolish + VFXBelievability + AudioFidelity + PerformanceBudget`

**Maximum Score**: 120 points

---

## Thresholds

| Score Range | Status | Action Required |
|-------------|--------|-----------------|
| **≥95** | World-Class | AAA-quality production ready |
| **90-94** | Excellent | Production ready with minor polish |
| **80-89** | Good | Address flagged dimensions |
| **70-79** | Needs Improvement | Substantial rework required |
| **<70** | Not Ready | Block production, major revision needed |

**Target**: ≥90/120 (75% of maximum, world-class tier)

---

## Dimension 1: Visual Style (25 points)

*Measures coherence, originality, and platform-appropriateness of visual direction*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| VS-01 | **Style Guide Completeness** | 5 | Mood board, color palette, typography, rendering style documented |
| VS-02 | **Visual Language Consistency** | 5 | Unified art direction across characters, environments, UI, VFX |
| VS-03 | **Market Benchmarking** | 5 | 3-5 reference games analyzed, differentiation strategy clear |
| VS-04 | **Emotional Tone Alignment** | 5 | Visual style matches target player emotion (casual, epic, cozy, competitive) |
| VS-05 | **Mobile Platform Adaptation** | 5 | Clarity at small sizes, legibility, high-contrast UI |

### Scoring Scale (per checkpoint)
- **5 points**: Fully compliant, world-class execution
- **4 points**: Minor issues (1-2 instances needing fix)
- **3 points**: Moderate issues (3-5 instances)
- **2 points**: Significant issues (6-10 instances)
- **1 point**: Major issues (>10 instances)
- **0 points**: Not addressed at all

### Anti-Patterns

| Bad | Good |
|-----|------|
| Generic "mobile game" aesthetic | Distinctive visual identity (e.g., Clash Royale's claymation style) |
| Inconsistent style (realistic characters, cartoony UI) | Unified visual language across all elements |
| No reference games cited | 3-5 benchmarks with "avoid" vs "emulate" notes |
| Color palette with 20+ hues | Focused palette (5-7 primary, 3-5 semantic, environment variants) |

---

## Dimension 2: Asset Completeness (25 points)

*Measures catalog coverage, prioritization, and technical specifications*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| AC-01 | **Catalog Size** | 5 | ≥200 assets cataloged with unique IDs (CHAR-xxx, ENV-xxx, UI-xxx, VFX-xxx, SFX-xxx) |
| AC-02 | **Character Asset Coverage** | 5 | ≥20 character assets (player, enemies, NPCs) with sprite sheets/model specs |
| AC-03 | **Environment Asset Coverage** | 5 | ≥10 environment zones with tileset/prop/background specs |
| AC-04 | **UI Component Library** | 5 | ≥100 UI elements (buttons, icons, panels) with states and variants |
| AC-05 | **Asset Variants and Priority** | 5 | P0/P1/P2 prioritization, variants documented (idle, hit, death, etc.) |

### Scoring Scale (per checkpoint)
- **5 points**: Exceeds minimum (120%+), all specs complete
- **4 points**: Meets minimum (100-119%)
- **3 points**: Near minimum (80-99%)
- **2 points**: Below minimum (60-79%)
- **1 point**: Significantly below (40-59%)
- **0 points**: <40% or not cataloged

### Category Minimums

| Category | Minimum Count | Critical Assets |
|----------|---------------|-----------------|
| CHAR-xxx | ≥20 | Player character, main enemies, bosses |
| ENV-xxx | ≥10 | Level zones, backgrounds, tilesets |
| PROP-xxx | ≥20 | Interactive objects, collectibles |
| UI-xxx | ≥100 | Buttons, icons, panels, HUD |
| VFX-xxx | ≥20 | Combo, clear, explosion, ambient effects |
| SFX-xxx | ≥30 | UI sounds, gameplay actions, ambience |

---

## Dimension 3: Animation Polish (20 points)

*Measures animation timing, state machine design, and juiciness*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| AP-01 | **Frame Rate Standards** | 4 | UI 60fps, gameplay 30fps, background 15-20fps documented |
| AP-02 | **Timing and Easing Curves** | 4 | Duration + easing specified per animation (cubic-bezier values) |
| AP-03 | **State Machine Design** | 4 | FSM diagrams for characters (idle → move → action → hit → death) |
| AP-04 | **Juiciness Principles** | 4 | Squash & stretch, anticipation, overshoot parameters documented |
| AP-05 | **ASMR Integration** | 4 | Animation timing synced with audio (<50ms latency budget) |

### Scoring Scale (per checkpoint)
- **4 points**: All animated assets have complete specs
- **3 points**: 80%+ assets have specs
- **2 points**: 60-79% assets have specs
- **1 point**: 40-59% assets have specs
- **0 points**: <40% assets have specs

### Animation Quality Indicators

| Indicator | Expected |
|-----------|----------|
| State machine completeness | 100% character FSMs with transition conditions |
| Easing curve library | ≥8 curves (ease-out-game, spring, bounce, etc.) |
| Squash & stretch ratios | 1.2-1.5x for characters, 1.1-1.3x for objects |
| Frame budget | ≤10MB animation memory |

---

## Dimension 4: VFX Believability (20 points)

*Measures particle systems, screen effects, and visual feedback quality*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| VF-01 | **Particle System Specifications** | 4 | Count, duration, colors, blend modes documented for all effects |
| VF-02 | **Screen Effect Parameters** | 4 | Shake, flash, vignette with intensity/duration/easing specified |
| VF-03 | **Feedback Hierarchy** | 4 | Clear priority: gameplay > feedback > ambient (no visual clutter) |
| VF-04 | **Performance Budget Compliance** | 4 | ≤150 particles on-screen (combo 80, clear 60, UI 20, ambient 30) |
| VF-05 | **Blend Mode and Layering** | 4 | Z-index system documented (background → objects → fx → UI → overlay) |

### Scoring Scale (per checkpoint)
- **4 points**: All VFX have complete technical specs
- **3 points**: 80%+ VFX have specs
- **2 points**: 60-79% VFX have specs
- **1 point**: 40-59% VFX have specs
- **0 points**: <40% VFX have specs

### VFX Categories

| Category | Minimum Effects | Max Particles/Effect |
|----------|-----------------|----------------------|
| Combo Effects (VFX-COMBO-xxx) | 4 (2x, 3x, 4x, MEGA) | 80 total |
| Clear Effects (VFX-CLEAR-xxx) | 4 (line, match, special, complete) | 60 total |
| Explosion Effects (VFX-EXPLODE-xxx) | 4 (small, medium, large, mega) | 100 peak |
| Ambient Effects (VFX-AMBIENT-xxx) | 3 (sparkle, dust, glow) | 30 total |
| UI Effects (VFX-UI-xxx) | 5 (button, notification, achievement, currency, level-up) | 20 total |

---

## Dimension 5: Audio Fidelity (15 points)

*Measures ASMR sound design, latency compliance, and audio system architecture*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| AF-01 | **Material Sound Library Coverage** | 3 | ≥8 materials (wood, metal, glass, stone, fabric, liquid, organic, magical) |
| AF-02 | **Latency Compliance** | 3 | <50ms documented with preload strategies (UI <20ms, gameplay <30ms) |
| AF-03 | **Music Integration** | 3 | Track list, layering system, ducking rules, loop points specified |
| AF-04 | **ASMR Quality Design** | 3 | Tactile, proximity, precision, satisfaction ratings (≥4/5 for feedback sounds) |
| AF-05 | **Spatial Audio and Reverb** | 3 | Environment-specific reverb zones, 3D positioning for gameplay sounds |

### Scoring Scale (per checkpoint)
- **3 points**: Fully specified with technical parameters
- **2 points**: Most scenarios covered (80%+)
- **1 point**: Partial coverage (50-79%)
- **0 points**: Not specified (<50%)

### Audio Latency Requirements

| Sound Category | Max Latency | Priority | Optimization Strategy |
|----------------|-------------|----------|----------------------|
| UI Tap | <20ms | CRITICAL | Preload, uncompressed |
| Gameplay Action | <30ms | HIGH | Preload, low-latency codec |
| Feedback | <50ms | HIGH | Streaming with buffer |
| Music/Ambience | <100-200ms | MEDIUM | Streaming |

### Material Sound Library

Each material MUST have:
- **Tap/Click** (light interaction)
- **Place/Drop** (object placement)
- **Break/Destroy** (destruction)
- **Combo/Special** (enhanced feedback)

**ASMR Rating**: 1-5 scale (target ≥4 for feedback sounds)

---

## Dimension 6: Performance Budget (15 points)

*Measures mobile platform optimization and memory constraints*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| PB-01 | **Texture Memory Budget** | 3 | ≤256MB total, ≤2048x2048 max resolution, atlas grouping documented |
| PB-02 | **Audio Memory Budget** | 3 | ≤64MB total, compressed formats (Ogg Vorbis/AAC), streaming strategy |
| PB-03 | **Polygon Budget** | 3 | Characters ≤5K tris, props ≤2K tris, environments ≤10K tris per zone |
| PB-04 | **Draw Call Budget** | 3 | ≤100 draw calls per frame, batching strategy documented |
| PB-05 | **Resolution Tiers** | 3 | @1x/@2x/@3x variants for devices, dynamic quality settings |

### Scoring Scale (per checkpoint)
- **3 points**: All budgets compliant, optimization strategies documented
- **2 points**: Most budgets compliant (80%+)
- **1 point**: Partial compliance (50-79%)
- **0 points**: Exceeds budgets (<50% compliant)

### Mobile Platform Targets

| Device Tier | Target | Texture Quality | Audio Quality | Particle Budget |
|-------------|--------|-----------------|---------------|-----------------|
| High (iPhone 14+) | 60fps | @3x (2048px) | 48kHz 256kbps | 150 particles |
| Medium (iPhone 11-13) | 60fps | @2x (1024px) | 44.1kHz 192kbps | 100 particles |
| Low (iPhone X, Android mid) | 30fps | @1x (512px) | 44.1kHz 128kbps | 50 particles |

---

## AQS Calculation Worksheet

```markdown
## AQS Score Calculation

### Visual Style (max 25)
- [ ] VS-01 Style Guide Completeness: __/5
- [ ] VS-02 Visual Language Consistency: __/5
- [ ] VS-03 Market Benchmarking: __/5
- [ ] VS-04 Emotional Tone Alignment: __/5
- [ ] VS-05 Mobile Platform Adaptation: __/5
**Visual Style Total**: __/25

### Asset Completeness (max 25)
- [ ] AC-01 Catalog Size (≥200 assets): __/5
- [ ] AC-02 Character Asset Coverage (≥20): __/5
- [ ] AC-03 Environment Asset Coverage (≥10): __/5
- [ ] AC-04 UI Component Library (≥100): __/5
- [ ] AC-05 Asset Variants and Priority: __/5
**Asset Completeness Total**: __/25

### Animation Polish (max 20)
- [ ] AP-01 Frame Rate Standards: __/4
- [ ] AP-02 Timing and Easing Curves: __/4
- [ ] AP-03 State Machine Design: __/4
- [ ] AP-04 Juiciness Principles: __/4
- [ ] AP-05 ASMR Integration: __/4
**Animation Polish Total**: __/20

### VFX Believability (max 20)
- [ ] VF-01 Particle System Specifications: __/4
- [ ] VF-02 Screen Effect Parameters: __/4
- [ ] VF-03 Feedback Hierarchy: __/4
- [ ] VF-04 Performance Budget Compliance: __/4
- [ ] VF-05 Blend Mode and Layering: __/4
**VFX Believability Total**: __/20

### Audio Fidelity (max 15)
- [ ] AF-01 Material Sound Library Coverage (≥8): __/3
- [ ] AF-02 Latency Compliance (<50ms): __/3
- [ ] AF-03 Music Integration: __/3
- [ ] AF-04 ASMR Quality Design: __/3
- [ ] AF-05 Spatial Audio and Reverb: __/3
**Audio Fidelity Total**: __/15

### Performance Budget (max 15)
- [ ] PB-01 Texture Memory Budget (≤256MB): __/3
- [ ] PB-02 Audio Memory Budget (≤64MB): __/3
- [ ] PB-03 Polygon Budget: __/3
- [ ] PB-04 Draw Call Budget (≤100): __/3
- [ ] PB-05 Resolution Tiers: __/3
**Performance Budget Total**: __/15

---

## TOTAL AQS: __/120

**Status**: [ ] World-Class (≥95) | [ ] Excellent (90-94) | [ ] Good (80-89) | [ ] Needs Work (70-79) | [ ] Block (<70)

**Required for Production**: ≥90/120
```

---

## Automated Validation

AQS can be partially automated using the following tools:

| Checkpoint | Tool | Automation Level |
|------------|------|------------------|
| AC-01 Catalog Size | `grep -c "^[A-Z]+-[0-9]+" asset-catalog.md` | Full |
| PB-01 Texture Memory | `find . -name "*.png" \| xargs du -ch` | Full |
| PB-02 Audio Memory | `find . -name "*.ogg" -o -name "*.mp3" \| xargs du -ch` | Full |
| PB-03 Polygon Budget | Unity Profiler, Asset Post-Processor | Partial |
| PB-04 Draw Call Budget | Frame Debugger | Partial |
| AF-02 Latency | High-speed camera, Audio profiler | Manual |

---

## Integration

### With /speckit.design --game-art-pipeline

The game art pipeline command MUST generate specifications that score ≥90 AQS by default.

### With /speckit.analyze

```bash
/speckit.analyze --profile aqs
```

Generates full AQS assessment with per-checkpoint scores from:
- `specs/games/art-spec.md` (VS-* checkpoints)
- `specs/games/asset-catalog.md` (AC-* checkpoints)
- `specs/games/animation-library.md` (AP-* checkpoints)
- `specs/games/vfx-requirements.md` (VF-* checkpoints)
- `specs/games/audio-requirements.md` (AF-* checkpoints)
- All output files (PB-* checkpoints)

### Quality Gates

| Gate ID | Threshold | Phase | Action |
|---------|-----------|-------|--------|
| QG-ART-001 | AQS ≥ 90 | Pre-Production | Block asset creation |
| QG-ART-002 | AC-01 ≥ 4 (≥200 assets) | Pre-Production | Block production kickoff |
| QG-ART-003 | PB-* all ≥ 2 | Pre-Production | Block implementation |
| QG-ART-004 | AF-02 = 3 (<50ms) | Post-Production | Block release |
| QG-ART-005 | VS-02 ≥ 4 | Post-Production | Block release |
| QG-ART-006 | AP-01 ≥ 3 | Post-Production | Warn (SHOULD level) |

---

## Comparison: AQS vs DQS vs CQS

| Score System | Max Points | Dimensions | Checkpoints | Target Threshold | Purpose |
|--------------|------------|------------|-------------|------------------|---------|
| **AQS** | 120 | 6 | 30 | ≥90 (75%) | Game art pipeline quality |
| **CQS-Game** | 120 | 10 | 10 | ≥90 (75%) | Game concept quality |
| **DQS** | 100 | 5 | 25 | ≥70 (70%) | Design system quality |
| **SQS** | 100 | 5 | 25 | ≥80 (80%) | Feature specification quality |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-01-14 | Initial 30-checkpoint AQS rubric for game art pipeline |

---

*AQS Rubric v1.0 | Part of Spec Kit Game Art Quality Framework*

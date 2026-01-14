# Game Art Specification

---
metadata:
  version: "1.0"
  engine: "[Unity/Unreal/Custom]"
  platform: "Mobile (iOS/Android)"
  target_genres: "[Sorting, Match-3, Idle, Arcade, Puzzle]"
  memory_budget:
    textures: "256MB"
    audio: "64MB"
    total: "320MB"
  resolution_targets:
    - "iPhone: 2436×1125 (Super Retina)"
    - "Android: 2340×1080 (FHD+)"
  created: "[YYYY-MM-DD]"
  last_updated: "[YYYY-MM-DD]"
  status: "Draft | In Review | Approved | Production Ready"
  aqs_score: "__/120"
---

> **Purpose**: Complete visual style guide for world-class mobile game art production.
> **Scope**: Mood boards, color palette, typography, rendering style, lighting, camera angles.
> **Handoff**: → Asset catalog (200+ assets), Animation library, VFX specs, Audio requirements.

---

## 1. Mood Board References

### Reference Anchors

Visual inspiration drawn from these games:

| Reference Game | Studio | Year | What We Emulate | What We Avoid |
|----------------|--------|------|-----------------|---------------|
| **[Game 1]** | [Studio] | [Year] | [Art direction strength] | [Weakness to avoid] |
| **[Game 2]** | [Studio] | [Year] | [Art direction strength] | [Weakness to avoid] |
| **[Game 3]** | [Studio] | [Year] | [Art direction strength] | [Weakness to avoid] |

**Example**:
```markdown
| Clash Royale | Supercell | 2016 | Claymation aesthetic, chunky characters, readable at small sizes | Overused style, too cartoony for mature audiences |
| Monument Valley | ustwo | 2014 | Minimalist geometry, elegant color palette, optical illusions | Too abstract for action games |
| Genshin Impact | miHoYo | 2020 | Anime-inspired, vibrant environments, particle-rich VFX | Too realistic for casual mobile |
```

### Emotional Tone

**Target Emotion**: [Cozy, Epic, Competitive, Relaxing, Chaotic, Satisfying]

**Mood Keywords** (5-7 adjectives):
- [Keyword 1] — [Brief explanation]
- [Keyword 2] — [Brief explanation]
- [Keyword 3] — [Brief explanation]

**Example**:
```markdown
**Target Emotion**: Satisfying + Cozy

**Mood Keywords**:
- **Tactile** — Physical sensation, ASMR-friendly sound design
- **Polished** — High-quality shaders, smooth animations
- **Warm** — Inviting color palette, soft lighting
- **Playful** — Not serious, gentle humor in character designs
- **Organized** — Clean UI, everything has its place (sorting theme)
```

### Avoid List

**Anti-Patterns** (what this game is NOT):
- ❌ [Anti-pattern 1] — [Why it doesn't fit]
- ❌ [Anti-pattern 2] — [Why it doesn't fit]
- ❌ [Anti-pattern 3] — [Why it doesn't fit]

**Example**:
```markdown
- ❌ Generic mobile game look — No stock Unity assets, no overused fonts (ComicSans, Papyrus)
- ❌ Aggressive/dark — Not a battle royale, not horror-themed
- ❌ Minimalist to a fault — Not Flappy Bird simplicity, needs visual richness
```

---

## 2. Art Direction Principles

### Core Principles (4-6 principles)

1. **[Principle 1]** — [Description, rationale, examples]
2. **[Principle 2]** — [Description, rationale, examples]
3. **[Principle 3]** — [Description, rationale, examples]
4. **[Principle 4]** — [Description, rationale, examples]

**Example**:
```markdown
1. **Clarity First** — Every object must be readable at 1x scale on iPhone SE (4.7"). No tiny details that disappear on small screens.
2. **Personality Over Realism** — Characters with exaggerated features (big eyes, expressive faces) over realistic proportions.
3. **Performance Over Fidelity** — 60fps > high poly count. Use texture tricks (normal maps) instead of geometry.
4. **Consistency Above All** — Same visual language for all assets. One icon style, one rendering style, one color palette.
```

### Differentiation Strategy

**How We Stand Out**:
- [Unique aspect 1] — [How it's different from competitors]
- [Unique aspect 2] — [How it's different from competitors]
- [Unique aspect 3] — [How it's different from competitors]

**Example**:
```markdown
- **Claymation-meets-papercraft** — Soft, rounded characters (Clash Royale) + flat, layered environments (Alto's Adventure)
- **Pastel gradients** — Not solid colors. Every surface has subtle gradient (sky blue → lavender, grass green → lime)
- **Liquid physics** — Sorting game with fluid simulation. Balls have weight, stack naturally, wobble on impact.
```

---

## 3. Rendering Style Specification

### Art Style Type

**Primary Style**: [2D Sprite, 3D Low-Poly, 3D High-Poly, 2.5D (3D rendered to sprites), Voxel, Pixel Art]

**Rationale**: [Why this style fits the game, genre, target audience]

**Example**:
```markdown
**Primary Style**: 2.5D (3D High-Poly rendered to sprites)

**Rationale**:
- Allows complex lighting/shadows at bake time (no runtime cost)
- Sprites scale well across device resolutions (@1x, @2x, @3x)
- Art team can iterate in 3D (faster than pixel art)
- Players perceive as "high quality" vs pure 2D sprites
```

### Shading Model

**Shading**: [Flat/Unlit, Toon/Cel-Shaded, PBR (Physically Based Rendering), Custom]

**Parameters**:
- **Base Color**: [sRGB, linear, HDR]
- **Smoothness**: [0-1 range, typical values]
- **Metallic**: [0-1 range, typical values]
- **Emission**: [Yes/No, typical use cases]

**Example**:
```markdown
**Shading**: Toon/Cel-Shaded with 3-tone gradient

**Parameters**:
- **Base Color**: sRGB (no HDR needed for mobile)
- **Smoothness**: 0.3-0.5 (slightly matte, not glossy)
- **Metallic**: 0.0 (no metallic surfaces, pure diffuse)
- **Emission**: Yes (UI elements glow, combo effects, collectibles)

**Gradient Zones**:
- **Highlight**: Lightest tone (facing light source)
- **Midtone**: Base color
- **Shadow**: 30% darker than base (facing away from light)
```

### Outline Style

**Outlines**: [None, Thin (1-2px), Medium (3-4px), Thick (5-8px), Variable by distance]

**Implementation**: [Inverted hull, post-process edge detection, baked into texture]

**Color**: [Black, Dark variant of base color, Custom per material]

**Example**:
```markdown
**Outlines**: Medium (3px) on characters, Thin (1px) on props, None on environment

**Implementation**: Inverted hull (duplicate mesh, flip normals, offset by 3px)

**Color**: Dark variant of base color (not pure black). Example: Red ball → Dark red outline (#8B0000)

**Rationale**: Separates gameplay objects from background, improves readability on busy screens.
```

### Shadow and Lighting

**Shadows**: [Hard, Soft, Baked, Real-time, None]

**Shadow Resolution**: [256x256, 512x512, 1024x1024 per light]

**Ambient Occlusion**: [Yes/No, baked/real-time, intensity]

**Example**:
```markdown
**Shadows**: Baked soft shadows for environment, real-time blob shadows for characters

**Shadow Resolution**: 512x512 for character blob shadows (performance budget)

**Ambient Occlusion**: Yes, baked into diffuse texture (no runtime cost). Intensity: 0.6

**Rationale**: Baked AO adds depth without performance hit. Real-time character shadows ground them to environment.
```

---

## 4. Color Palette

### Primary Palette

**5-7 core colors** that define the game's visual identity:

| Color Name | Hex | RGB | Use Case | WCAG Contrast (on white) |
|------------|-----|-----|----------|--------------------------|
| **Primary** | #[XXXXXX] | (R, G, B) | Main UI, player character | [4.5:1 for text] |
| **Secondary** | #[XXXXXX] | (R, G, B) | Secondary UI, enemy characters | [4.5:1 for text] |
| **Accent** | #[XXXXXX] | (R, G, B) | CTAs, highlights, combos | [3:1 for large text] |
| **Background** | #[XXXXXX] | (R, G, B) | Environment base | [1.5:1 ambient] |
| **Neutral** | #[XXXXXX] | (R, G, B) | UI panels, text backgrounds | [4.5:1 for text] |

**Example**:
```markdown
| Lavender Sky | #A78BFA | (167, 139, 250) | Sky gradient top, UI highlights | 3.2:1 ✅ (large text) |
| Mint Green | #6EE7B7 | (110, 231, 183) | Grass, success states, currency | 2.8:1 ⚠️ (use dark variant for text) |
| Coral Accent | #FB7185 | (251, 113, 133) | CTAs, combo effects, hearts | 3.5:1 ✅ (large text) |
| Cream Base | #FEF3C7 | (254, 243, 199) | Panel backgrounds, neutral UI | 1.2:1 (ambient only) |
| Slate Gray | #475569 | (71, 85, 105) | Body text, disabled states | 9.8:1 ✅ (excellent) |
```

### Semantic Colors

**Functional colors** for UI feedback:

| Semantic | Hex | Use Case |
|----------|-----|----------|
| **Success** | #[XXXXXX] | Level complete, correct action, achievements |
| **Error** | #[XXXXXX] | Lives lost, failed action, warnings |
| **Warning** | #[XXXXXX] | Low health, time running out, alerts |
| **Info** | #[XXXXXX] | Tutorials, hints, notifications |

**Example**:
```markdown
| Success | #10B981 | ✅ Emerald green (level complete, +100 points) |
| Error | #EF4444 | ❌ Red (lives lost, game over) |
| Warning | #F59E0B | ⚠️ Amber (5 seconds left, low energy) |
| Info | #3B82F6 | ℹ️ Blue (tutorial popups, "Tap to continue") |
```

### Environment-Specific Palettes

**Color schemes per level/zone**:

| Environment | Primary | Secondary | Accent | Mood |
|-------------|---------|-----------|--------|------|
| **Zone 1** | [Color] | [Color] | [Color] | [Mood description] |
| **Zone 2** | [Color] | [Color] | [Color] | [Mood description] |
| **Zone 3** | [Color] | [Color] | [Color] | [Mood description] |

**Example**:
```markdown
| Garden (Levels 1-20) | Mint Green (#6EE7B7) | Lavender (#A78BFA) | Coral (#FB7185) | Fresh, spring, beginner-friendly |
| Desert (Levels 21-40) | Sand Tan (#FCD34D) | Terracotta (#FB923C) | Turquoise (#06B6D4) | Warm, dry, challenging |
| Ocean (Levels 41-60) | Deep Blue (#1E40AF) | Aqua Cyan (#06B6D4) | Pearl White (#F3F4F6) | Cool, calm, mysterious |
```

### Gradient Guidelines

**Gradient Formula**: [Linear, Radial, Angular]

**Direction**: [Top-to-bottom, Left-to-right, Center-outward]

**Stop Points**: [2-stop, 3-stop, 5-stop]

**Example**:
```markdown
**Background Gradients**: Linear, top-to-bottom, 2-stop
- Sky: Lavender (#A78BFA) → Light Blue (#BFDBFE)
- Ground: Mint Green (#6EE7B7) → Emerald (#10B981)

**UI Panel Gradients**: Radial, center-outward, 3-stop
- Center: White (#FFFFFF)
- Mid: Cream (#FEF3C7)
- Edge: Light Gray (#E5E7EB)

**Button Gradients**: Linear, top-to-bottom, 2-stop (on press: reverse)
- Normal: Coral Light (#FCA5A5) → Coral Dark (#EF4444)
- Pressed: Coral Dark (#EF4444) → Coral Light (#FCA5A5)
```

---

## 5. Typography

### Game-Specific Font Scale

**Font Stack** (3-tier hierarchy):

| Tier | Font Family | Weight | Use Case | Fallback |
|------|-------------|--------|----------|----------|
| **Title** | [Font Name] | [Weight] | Level titles, menus, big numbers | [Fallback] |
| **UI** | [Font Name] | [Weight] | Buttons, labels, body text | [Fallback] |
| **Numeric** | [Font Name] | [Weight] | Scores, timers, currency | [Fallback] |

**Example**:
```markdown
| Title | Fredoka One | Bold (700) | Level titles ("LEVEL 42"), menus | Arial Black, sans-serif |
| UI | Inter | Medium (500) | Button labels, settings, tutorial text | Helvetica, sans-serif |
| Numeric | Roboto Mono | SemiBold (600) | Score (12,345), timer (01:23), coins (999) | Courier New, monospace |
```

### Mobile-Optimized Size Scale

**Minimum sizes** for legibility:

| Context | Font Size | Line Height | Letter Spacing | Min Touch Target |
|---------|-----------|-------------|----------------|------------------|
| **Headline** | 32-48px | 1.2 | -0.02em | N/A |
| **Subheadline** | 24-32px | 1.3 | -0.01em | N/A |
| **Body** | 16-20px | 1.5 | 0em | N/A |
| **Small** | 12-14px | 1.4 | 0.01em | N/A |
| **Button** | 16-18px | 1.2 | 0.02em (uppercase) | 44x44px |

**Example**:
```markdown
| Level Title | 40px (iPhone), 48px (iPad) | 1.1 | -0.02em (tight, impactful) | N/A |
| Button Label | 18px | 1.2 | 0.05em (uppercase, "PLAY") | 44x44px min |
| Score Counter | 28px (numeric, monospace) | 1.0 | 0em | N/A |
| Tutorial Text | 16px (left-aligned, multi-line) | 1.6 | 0em | N/A |
| Small Print | 12px (legal, credits) | 1.4 | 0.01em | N/A |
```

### Text Effects

**Drop Shadow**: [Yes/No, offset, blur, color, opacity]

**Outline**: [Yes/No, thickness, color]

**Glow**: [Yes/No, color, intensity]

**Example**:
```markdown
**Title Drop Shadow**: Yes
- Offset: (2px, 4px) — slight right, more down
- Blur: 8px
- Color: Black (#000000)
- Opacity: 0.3

**Button Outline**: Yes
- Thickness: 2px
- Color: Dark variant of button color

**Score Glow** (on increment): Yes
- Color: Yellow (#FDE047)
- Intensity: Fade in 200ms, hold 100ms, fade out 300ms
- Use case: +100 points popup
```

---

## 6. Lighting Guidelines

### Lighting Setup

**Primary Light**: [Directional, Point, Spot, Ambient]

**Direction**: [Angle in degrees, world coordinates]

**Intensity**: [0-1 scale or lumens]

**Color Temperature**: [Kelvin, or hex color]

**Example**:
```markdown
**Primary Light**: Directional (sun)
- Direction: 45° from top-left (315° azimuth, 45° elevation)
- Intensity: 0.8 (slightly softer than harsh noon sun)
- Color Temperature: 5500K (neutral daylight, slight warm tint)

**Fill Light**: Ambient hemisphere
- Sky Color: Lavender (#A78BFA), Intensity: 0.3
- Ground Color: Mint Green (#6EE7B7), Intensity: 0.2
- Simulates light bouncing from environment
```

### Lighting by Environment

**Per-zone lighting variations**:

| Environment | Primary Light | Secondary Light | Ambient | Mood |
|-------------|---------------|-----------------|---------|------|
| **Zone 1** | [Setup] | [Setup] | [Color] | [Mood] |
| **Zone 2** | [Setup] | [Setup] | [Color] | [Mood] |
| **Zone 3** | [Setup] | [Setup] | [Color] | [Mood] |

**Example**:
```markdown
| Garden | Sun (45°, Intensity 0.8) | Sky ambient (Lavender, 0.3) | Mint Green (#6EE7B7) | Bright, cheerful |
| Desert | Sun (60°, Intensity 1.0) | Point light (Campfire, 0.5) | Sand Tan (#FCD34D) | Harsh, hot |
| Ocean | Moon (30°, Intensity 0.4) | Underwater caustics (Animated, 0.6) | Deep Blue (#1E40AF) | Mysterious, cool |
```

### Special Lighting Effects

**Rim Lighting**: [Yes/No, color, intensity, use case]

**God Rays**: [Yes/No, density, color, use case]

**Light Cookies**: [Yes/No, texture, use case]

**Example**:
```markdown
**Rim Lighting**: Yes
- Color: White (#FFFFFF) with slight hue shift (warmer on organic, cooler on metal)
- Intensity: 0.5
- Use Case: Characters and interactive objects (makes them "pop" from background)

**God Rays**: Yes (Zone 3: Ocean only)
- Density: 0.3 (subtle)
- Color: Aqua Cyan (#06B6D4)
- Use Case: Underwater scenes, light shafts from surface

**Light Cookies**: No (performance budget concern on mobile)
```

---

## 7. Camera Angles

### Gameplay Camera

**View Type**: [Orthographic, Perspective, Isometric, Top-Down, Side-Scroller]

**Field of View**: [Degrees for perspective, units for orthographic]

**Camera Distance**: [Units from gameplay plane]

**Rotation**: [Euler angles or locked axis]

**Example**:
```markdown
**View Type**: Orthographic (no perspective distortion, consistent object sizes)

**Orthographic Size**: 5.4 units (fits 10 rows of balls at 0.5 units each + UI padding)

**Camera Distance**: 10 units from Z=0 gameplay plane

**Rotation**: Locked (no player control), slight top-down angle (X: 10°, Y: 0°, Z: 0°)

**Rationale**: Orthographic eliminates depth confusion. Players can precisely target balls regardless of depth.
```

### Menu/UI Camera

**View Type**: [Orthographic (preferred for 2D UI), Perspective]

**Overlay**: [Screen Space - Overlay, Screen Space - Camera, World Space]

**Safe Area**: [Padding for notches, rounded corners]

**Example**:
```markdown
**View Type**: Orthographic (2D UI)

**Overlay**: Screen Space - Overlay (always on top, resolution-independent)

**Safe Area Padding**:
- Top: 44px (iPhone notch)
- Bottom: 34px (iPhone home indicator)
- Left/Right: 20px (rounded corners)

**Canvas Scaler**: Scale With Screen Size, Reference Resolution: 1125x2436 (iPhone X)
```

### Cutscene Camera (if applicable)

**View Type**: [Perspective (cinematic)]

**Camera Movement**: [Static, Dolly, Pan, Orbit]

**Duration**: [Seconds]

**Skippable**: [Yes/No]

**Example**:
```markdown
**View Type**: Perspective (FOV: 60°)

**Camera Movement**:
- 0-2s: Dolly in from Z=20 to Z=10 (establish environment)
- 2-4s: Pan left to right (showcase level layout)
- 4-5s: Zoom to character (focus player attention)

**Duration**: 5 seconds

**Skippable**: Yes (tap anywhere to skip), auto-skip after first viewing
```

---

## 8. Technical Constraints

### Mobile Performance Budget

| Resource | Budget | Measurement | Enforcement |
|----------|--------|-------------|-------------|
| **Texture Memory** | ≤256MB | Sum of all texture assets | QG-ART-003 |
| **Audio Memory** | ≤64MB | Sum of all audio assets | QG-ART-003 |
| **Polygon Count** | Characters ≤5K, Props ≤2K, Envs ≤10K/zone | Profiler | QG-ART-003 |
| **Draw Calls** | ≤100 per frame | Frame Debugger | QG-ART-003 |
| **Particle Count** | ≤150 simultaneous | Profiler (combo 80, clear 60, UI 20, ambient 30) | QG-ART-003 |

### Asset Size Limits

**Per-Asset Maximums**:
- **Character Sprite Sheet**: 2048x2048px @3x, 1024x1024px @2x, 512x512px @1x
- **Environment Atlas**: 4096x4096px @3x (split into multiple 2048x2048 atlases if exceeded)
- **UI Icon**: 256x256px @3x (typical: 128x128 @3x for 44pt icons)
- **VFX Texture**: 512x512px (particle sprites, dissolve masks)
- **Audio File**: <500KB per file (compressed Ogg Vorbis or AAC)

### File Format Requirements

| Asset Type | Format | Compression | Color Space | Alpha |
|------------|--------|-------------|-------------|-------|
| **Character Sprites** | PNG | Lossless | sRGB | Premultiplied |
| **UI Icons** | PNG | Lossless | sRGB | Straight |
| **Environment Textures** | PNG/ETC2 (Unity), ASTC (iOS) | Adaptive | sRGB | None or premultiplied |
| **VFX Particles** | PNG | Lossless | Linear | Premultiplied |
| **Audio (UI)** | Ogg Vorbis (Android), AAC (iOS) | 192kbps | N/A | N/A |
| **Audio (Music)** | Ogg Vorbis (Android), AAC (iOS) | 128kbps | N/A | N/A |

**Example**:
```markdown
**Character Export Settings** (from 3D software):
- Resolution: 2048x2048 @3x (source), downsample to 1024 @2x, 512 @1x at build time
- Format: PNG-24 (RGB + Alpha)
- Alpha: Premultiplied (avoids white fringing)
- Color Space: sRGB (gamma 2.2)
- Compression: Lossless (no JPEG artifacts)

**Import Settings** (Unity):
- Texture Type: Sprite (2D and UI)
- Sprite Mode: Multiple (sprite sheet)
- Pixels Per Unit: 100
- Filter Mode: Bilinear
- Compression: ETC2 (Android), ASTC 6x6 (iOS)
```

---

## 9. Platform Adaptation Notes

### iOS-Specific Considerations

- **Device Range**: iPhone SE (4.7", 1334x750) to iPhone 15 Pro Max (6.7", 2796x1290)
- **Safe Areas**: Notch (top), Home Indicator (bottom), respect UIKit safe area insets
- **Performance**: Target iPhone 11 (2019, A13 Bionic) as baseline for 60fps
- **Shaders**: Metal Shading Language (MSL), avoid unsupported features

### Android-Specific Considerations

- **Device Range**: Galaxy A-series (mid-tier, 720p) to Galaxy S-series (flagship, 1440p)
- **Safe Areas**: Punch-hole cameras (top), gesture navigation (bottom)
- **Performance**: Target Galaxy S10 (2019, Snapdragon 855) as baseline for 60fps
- **Shaders**: OpenGL ES 3.0+ or Vulkan, test on Mali/Adreno GPUs

### Resolution Strategy

**Adaptive Quality Settings**:
```
High-End (iPhone 14+, Galaxy S21+):
- Render Scale: 1.0x (native resolution)
- Texture Quality: @3x (2048px)
- Particle Budget: 150
- Shadows: Real-time soft

Mid-Tier (iPhone 11-13, Galaxy S10-S20):
- Render Scale: 0.8x (slight downscale)
- Texture Quality: @2x (1024px)
- Particle Budget: 100
- Shadows: Real-time blob

Low-End (iPhone X, Galaxy A-series):
- Render Scale: 0.6x
- Texture Quality: @1x (512px)
- Particle Budget: 50
- Shadows: Baked only
```

---

## 10. Quality Validation Checklist

**Use this checklist when self-reviewing the art specification**:

### Visual Style (VS-* checkpoints)
- [ ] VS-01: Style guide complete (mood board, color palette, typography, rendering style documented)
- [ ] VS-02: Visual language consistent across characters, environments, UI, VFX
- [ ] VS-03: 3-5 reference games analyzed with "emulate vs avoid" notes
- [ ] VS-04: Emotional tone clearly defined and visual choices support it
- [ ] VS-05: Mobile platform adaptations documented (clarity at small sizes, high-contrast UI)

### Asset Completeness (AC-* checkpoints)
- [ ] AC-01: Asset catalog lists ≥200 assets with unique IDs
- [ ] AC-02: ≥20 character assets with sprite sheets/model specs
- [ ] AC-03: ≥10 environment zones with tileset/prop/background specs
- [ ] AC-04: ≥100 UI elements with states and variants
- [ ] AC-05: P0/P1/P2 prioritization complete, variants documented

### Animation Polish (AP-* checkpoints)
- [ ] AP-01: Frame rate standards documented (UI 60fps, gameplay 30fps, background 15-20fps)
- [ ] AP-02: Easing curves library complete with cubic-bezier values
- [ ] AP-03: State machines designed for characters (idle → move → action → hit → death)
- [ ] AP-04: Squash & stretch parameters documented (1.2-1.5x for characters)
- [ ] AP-05: Animation timing synced with audio (<50ms latency budget)

### VFX Believability (VF-* checkpoints)
- [ ] VF-01: Particle system specs complete (count, duration, colors, blend modes)
- [ ] VF-02: Screen effects documented (shake, flash, vignette with parameters)
- [ ] VF-03: Feedback hierarchy clear (gameplay > feedback > ambient)
- [ ] VF-04: Performance budget compliant (≤150 particles on-screen)
- [ ] VF-05: Z-index layering system documented (background → objects → fx → UI → overlay)

### Audio Fidelity (AF-* checkpoints)
- [ ] AF-01: Material sound library covers ≥8 materials (wood, metal, glass, stone, fabric, liquid, organic, magical)
- [ ] AF-02: Latency compliance documented (<50ms with preload strategies)
- [ ] AF-03: Music integration complete (track list, layering, ducking, loop points)
- [ ] AF-04: ASMR quality ratings assigned (≥4/5 for feedback sounds)
- [ ] AF-05: Spatial audio and reverb zones specified

### Performance Budget (PB-* checkpoints)
- [ ] PB-01: Texture memory ≤256MB with atlas grouping
- [ ] PB-02: Audio memory ≤64MB with compression strategy
- [ ] PB-03: Polygon budgets set (characters ≤5K, props ≤2K, environments ≤10K/zone)
- [ ] PB-04: Draw call budget ≤100 with batching strategy
- [ ] PB-05: Resolution tiers documented (@1x/@2x/@3x variants)

**AQS Target**: ≥90/120 (world-class threshold)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [YYYY-MM-DD] | [Agent: visual-style-agent] | Initial art specification |

---

**Next Steps**:
1. → Generate asset catalog (200+ assets) via asset-cataloger-agent
2. → Define animation library via animation-designer-agent
3. → Specify VFX requirements via vfx-designer-agent
4. → Design ASMR audio system via audio-designer-agent
5. → Validate AQS ≥ 90 via `/speckit.analyze --profile aqs`
6. → Handoff to `/speckit.tasks` for asset production task breakdown

---

*Art Specification v1.0 | Generated by `/speckit.design --game-art-pipeline` | Part of World-Class Mobile Game Art Production Pipeline*

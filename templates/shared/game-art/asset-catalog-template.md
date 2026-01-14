# Game Asset Catalog

---
metadata:
  version: "1.0"
  total_assets: "[Count ≥200]"
  categories: "6 (Characters, Environments, Props, UI, VFX, Audio)"
  created: "[YYYY-MM-DD]"
  last_updated: "[YYYY-MM-DD]"
  status: "Draft | In Review | Approved | Production Ready"
  memory_budget:
    textures: "__/256MB"
    audio: "__/64MB"
    total: "__/320MB"
---

> **Purpose**: Complete registry of all visual and audio assets for production tracking.
> **Scope**: 200+ assets across 6 categories with unique IDs, technical specs, and priority tiers.
> **Handoff**: → Production task breakdown via `/speckit.tasks`.

---

## Asset Naming Convention

### Naming Pattern

```
[prefix]_[category]_[name]_[variant]_[resolution].[extension]
```

### Components

| Component | Description | Example |
|-----------|-------------|---------|
| **prefix** | Asset type abbreviation | `char`, `env`, `ui`, `vfx`, `sfx`, `mus` |
| **category** | Subcategory | `hero`, `enemy`, `npc`, `tile`, `btn`, `icon` |
| **name** | Descriptive name (lowercase, underscore-separated) | `warrior`, `forest`, `button`, `explosion` |
| **variant** | Animation state or variant | `idle`, `walk`, `hit`, `death`, `01`, `02` |
| **resolution** | Device tier | `@1x`, `@2x`, `@3x` (omit for source files) |
| **extension** | File format | `.png`, `.jpg`, `.ogg`, `.mp3`, `.aac` |

### Examples

```
char_hero_warrior_idle@2x.png          → Character, Hero, Warrior, Idle animation, 2x resolution
env_forest_tileset_ground@3x.png       → Environment, Forest, Tileset, Ground tiles, 3x resolution
ui_btn_play_normal@2x.png              → UI, Button, Play button, Normal state, 2x resolution
vfx_combo_explosion_4x@2x.png          → VFX, Combo, Explosion, 4x combo variant, 2x resolution
sfx_ui_tap_01.ogg                      → Audio, UI, Tap sound, Variant 01, Ogg Vorbis
mus_level_theme_forest.mp3             → Audio, Music, Level theme, Forest zone, MP3
```

---

## Category 1: Characters (CHAR-xxx)

**Minimum**: ≥20 character assets (player, enemies, NPCs)

| ID | Name | Type | Poly Count | Texture Res | Format | Priority | Status | Notes |
|----|------|------|------------|-------------|--------|----------|--------|-------|
| CHAR-001 | Player Character | Hero | 3,500 tris | 2048x2048 @3x | PNG-24 | P0 | Pending | Main protagonist |
| CHAR-002 | Warrior Enemy | Enemy | 2,800 tris | 1024x1024 @2x | PNG-24 | P0 | Pending | Melee attacker |
| CHAR-003 | Mage Enemy | Enemy | 2,600 tris | 1024x1024 @2x | PNG-24 | P1 | Pending | Ranged attacker |
| CHAR-004 | Boss: Dragon | Boss | 4,500 tris | 2048x2048 @3x | PNG-24 | P1 | Pending | Level 20 boss |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Asset Requirements per Character**:
- **Idle**: Looping animation (1-2 seconds)
- **Move**: Walk/run animation (0.5-1 second loop)
- **Action**: Attack/cast/interact (0.3-0.8 seconds)
- **Hit**: React to damage (0.2-0.4 seconds)
- **Death**: Final animation (0.5-1.5 seconds, no loop)
- **Victory**: Celebration (1-2 seconds, optional for heroes only)

**Technical Specs**:
- **Poly Count**: ≤5K tris (mobile budget)
- **Texture Resolution**: 2048x2048 @3x max (characters), 1024x1024 @2x (enemies)
- **Bones**: ≤50 bones per character (mobile rigging budget)
- **Sprite Sheet Layout**: Power-of-2 (512, 1024, 2048), atlas packing for variants

**Total CHAR Assets**: [Count ≥20]

---

## Category 2: Environments (ENV-xxx)

**Minimum**: ≥10 environment assets (zones, tilesets, props)

| ID | Name | Type | Poly Count | Texture Res | Format | Priority | Status | Notes |
|----|------|------|------------|-------------|--------|----------|--------|-------|
| ENV-001 | Garden Zone | Tileset | 8,000 tris/zone | 4096x4096 @3x | PNG-24 | P0 | Pending | Levels 1-20 |
| ENV-002 | Desert Zone | Tileset | 7,500 tris/zone | 4096x4096 @3x | PNG-24 | P1 | Pending | Levels 21-40 |
| ENV-003 | Ocean Zone | Tileset | 9,000 tris/zone | 4096x4096 @3x | PNG-24 | P1 | Pending | Levels 41-60 |
| ENV-004 | Forest Background | Parallax | N/A (2D) | 2048x1024 @3x | PNG-24 | P0 | Pending | Scrolling bg |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Asset Requirements per Environment**:
- **Ground Tiles**: Seamless tiling (256x256 base tile)
- **Background Layers**: 3-5 parallax layers (different scroll speeds)
- **Foreground Props**: Decorative elements (trees, rocks, clouds)
- **Lighting**: Pre-baked lightmaps (1024x1024 per zone)

**Technical Specs**:
- **Poly Count**: ≤10K tris per zone (all tiles + props combined)
- **Texture Resolution**: 4096x4096 @3x max (split into 2048x2048 atlases)
- **Tileset Layout**: Modular tiles (corner, edge, center), seamless edges
- **Parallax Layers**: 3-5 layers at 0.2x, 0.5x, 1.0x, 1.5x scroll speeds

**Total ENV Assets**: [Count ≥10]

---

## Category 3: Props (PROP-xxx)

**Minimum**: ≥20 prop assets (interactive, collectibles, decorative)

| ID | Name | Type | Poly Count | Texture Res | Format | Priority | Status | Notes |
|----|------|------|------------|-------------|--------|----------|--------|-------|
| PROP-001 | Coin | Collectible | 500 tris | 256x256 @3x | PNG-24 | P0 | Pending | Currency pickup |
| PROP-002 | Heart | Collectible | 400 tris | 256x256 @3x | PNG-24 | P0 | Pending | Health restore |
| PROP-003 | Treasure Chest | Interactive | 1,800 tris | 512x512 @3x | PNG-24 | P0 | Pending | Opens on tap |
| PROP-004 | Tree (Small) | Decorative | 1,200 tris | 512x512 @2x | PNG-24 | P1 | Pending | Garden zone |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Asset Requirements per Prop**:
- **Static Props**: Single sprite (no animation)
- **Interactive Props**: 2-3 states (closed, opening, open for chest)
- **Collectibles**: Idle animation (subtle bob/rotate) + collect animation (scale up + fade)

**Technical Specs**:
- **Poly Count**: ≤2K tris per prop
- **Texture Resolution**: 512x512 @3x max (most props: 256x256 @3x)
- **Pivot Point**: Bottom-center for ground props, center for floating props
- **Collision**: Simple box/sphere collider (no mesh collider for performance)

**Total PROP Assets**: [Count ≥20]

---

## Category 4: UI Elements (UI-xxx)

**Minimum**: ≥100 UI elements (buttons, icons, panels, HUD)

| ID | Name | Type | Size (pt) | Texture Res | Format | Priority | Status | Notes |
|----|------|------|-----------|-------------|--------|----------|--------|-------|
| UI-001 | Play Button | Button | 88x88 pt | 264x264 @3x | PNG-24 | P0 | Pending | Main menu CTA |
| UI-002 | Settings Icon | Icon | 44x44 pt | 132x132 @3x | PNG-24 | P0 | Pending | Gear icon |
| UI-003 | Pause Button | Button | 44x44 pt | 132x132 @3x | PNG-24 | P0 | Pending | Top-right HUD |
| UI-004 | Coin Icon | Icon | 32x32 pt | 96x96 @3x | PNG-24 | P0 | Pending | Currency HUD |
| UI-005 | Panel Background | Panel | Variable | 512x512 @3x | PNG-24 | P0 | Pending | 9-slice panel |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**UI Subcategories**:
| Subcategory | Count | Examples |
|-------------|-------|----------|
| **Buttons** | ≥20 | Play, pause, settings, close, next, retry |
| **Icons** | ≥40 | Currency, lives, energy, achievements, power-ups |
| **Panels** | ≥10 | Dialog boxes, settings panel, level complete panel |
| **HUD Elements** | ≥15 | Score counter, timer, progress bar, lives display |
| **Misc UI** | ≥15 | Loading spinner, checkmark, star rating, dividers |

**Asset Requirements per UI Element**:
- **Buttons**: 3 states (normal, pressed, disabled)
- **Icons**: Single state (static) or animated (optional glow effect)
- **Panels**: 9-slice capable (corners + edges + center, scalable)
- **HUD Elements**: Dynamic text fields (use Unity TextMeshPro or similar)

**Technical Specs**:
- **Texture Resolution**: 44pt icon = 132x132 @3x, 264x264 for 88pt buttons
- **Format**: PNG-24 with alpha (premultiplied or straight depending on engine)
- **Padding**: 8px transparent padding around edges (prevents bleeding)
- **9-Slice**: Define slice points (top, bottom, left, right insets)

**Total UI Assets**: [Count ≥100]

---

## Category 5: VFX (VFX-xxx)

**Minimum**: ≥20 VFX assets (particles, screen effects)

| ID | Name | Type | Particle Count | Texture Res | Format | Priority | Status | Notes |
|----|------|------|----------------|-------------|--------|----------|--------|-------|
| VFX-001 | Combo 2x | Particle | 40 particles | 512x512 @2x | PNG-24 | P0 | Pending | Burst + "2x" text |
| VFX-002 | Combo 3x | Particle | 60 particles | 512x512 @2x | PNG-24 | P0 | Pending | Larger burst + "3x" |
| VFX-003 | Line Clear | Particle | 30 particles | 256x256 @2x | PNG-24 | P0 | Pending | Horizontal sweep |
| VFX-004 | Explosion (Small) | Particle | 20 particles | 256x256 @2x | PNG-24 | P0 | Pending | Pop effect |
| VFX-005 | Sparkle Ambient | Particle | 15 particles | 128x128 @2x | PNG-24 | P1 | Pending | Background twinkle |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**VFX Subcategories**:
| Subcategory | Count | Max Particles | Examples |
|-------------|-------|---------------|----------|
| **Combo Effects** | ≥4 | 80 total | 2x, 3x, 4x, MEGA combos |
| **Clear Effects** | ≥4 | 60 total | Line, match, special, level complete |
| **Explosion Effects** | ≥4 | 100 peak | Small, medium, large, mega |
| **Ambient Effects** | ≥3 | 30 total | Sparkle, dust, glow |
| **UI Effects** | ≥5 | 20 total | Button glow, notification, achievement, currency, level-up |

**Asset Requirements per VFX**:
- **Particle Sprite**: Single texture (smoke, spark, star, etc.)
- **Particle System Settings**: YAML or JSON config (count, lifetime, velocity, color, blend mode)
- **Screen Effects**: Post-process shader (shake, flash, vignette) with parameters

**Technical Specs**:
- **Particle Budget**: ≤150 particles on-screen simultaneously (QG-ART-003)
- **Texture Resolution**: 512x512 @2x max (most: 256x256 @2x)
- **Blend Mode**: Additive for glows/explosions, Alpha Blend for smoke
- **Lifetime**: 0.5-2.0 seconds (short-lived for performance)
- **Sorting Layer**: VFX layer (z-index above gameplay, below UI)

**Total VFX Assets**: [Count ≥20]

---

## Category 6: Audio (SFX-xxx, MUS-xxx)

**Minimum**: ≥30 audio assets (UI sounds, gameplay, music, ambience)

### Sound Effects (SFX-xxx)

| ID | Name | Material | Duration | Format | File Size | Priority | Status | Notes |
|----|------|----------|----------|--------|-----------|----------|--------|-------|
| SFX-001 | UI Tap | Glass (Ting) | 0.1s | Ogg/AAC | <50KB | P0 | Pending | Button press |
| SFX-002 | Coin Collect | Metal (Clink) | 0.2s | Ogg/AAC | <75KB | P0 | Pending | Currency pickup |
| SFX-003 | Ball Place | Wood (Drop) | 0.3s | Ogg/AAC | <80KB | P0 | Pending | Place ball in slot |
| SFX-004 | Match Clear | Crystal (Shimmer) | 0.5s | Ogg/AAC | <100KB | P0 | Pending | Line clear |
| SFX-005 | Combo 2x | Magical (Whoosh) | 0.4s | Ogg/AAC | <90KB | P0 | Pending | Combo effect |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Material Sound Library** (≥8 materials):
| Material | Tap | Place | Break | Combo | ASMR Rating |
|----------|-----|-------|-------|-------|-------------|
| **Wood** | Knock light | Drop heavy | Crack | Thud | 4/5 |
| **Metal** | Coin clink | Sword unsheathe | Clang | Gong | 5/5 |
| **Glass** | Crystal ting | Bottle clink | Shatter | Chime | 5/5 |
| **Stone** | Tap echo | Rock drop | Crumble | Rumble | 3/5 |
| **Fabric** | Soft brush | Cloth place | Rip | Swoosh | 4/5 |
| **Liquid** | Drop | Pour | Splash | Bubble pop | 5/5 |
| **Organic** | Squish | Plop | Squelch | Slime stretch | 4/5 |
| **Magical** | Sparkle | Whoosh | Poof | Enchant | 5/5 |

**Total SFX Assets**: [Count ≥30]

### Music (MUS-xxx)

| ID | Name | Zone | Duration | Loop | Format | File Size | Priority | Status | Notes |
|----|------|------|----------|------|--------|-----------|----------|--------|-------|
| MUS-001 | Main Menu Theme | Menu | 2:30 | Yes | Ogg/AAC | <3MB | P0 | Pending | Upbeat, welcoming |
| MUS-002 | Garden Level Theme | Zone 1 | 2:00 | Yes | Ogg/AAC | <2.5MB | P0 | Pending | Calm, spring-like |
| MUS-003 | Desert Level Theme | Zone 2 | 2:15 | Yes | Ogg/AAC | <2.8MB | P1 | Pending | Warm, adventurous |
| MUS-004 | Boss Battle Theme | Boss | 1:45 | Yes | Ogg/AAC | <2.2MB | P1 | Pending | Intense, epic |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Music Requirements**:
- **Loop Points**: Seamless loop (no gap or click)
- **Layering**: 3-4 layers (drums, bass, melody, harmony) for adaptive music
- **Ducking**: Automatic volume reduction when SFX plays (music -6dB)
- **Bitrate**: 128kbps (music), 192kbps (UI/gameplay SFX)

**Total MUS Assets**: [Count ≥5]

---

## Summary Statistics

### Asset Count by Category

| Category | Target | Current | % Complete | Status |
|----------|--------|---------|------------|--------|
| CHAR-xxx | ≥20 | [Count] | [%] | 🔴 Not Started / 🟡 In Progress / 🟢 Complete |
| ENV-xxx | ≥10 | [Count] | [%] | 🔴 / 🟡 / 🟢 |
| PROP-xxx | ≥20 | [Count] | [%] | 🔴 / 🟡 / 🟢 |
| UI-xxx | ≥100 | [Count] | [%] | 🔴 / 🟡 / 🟢 |
| VFX-xxx | ≥20 | [Count] | [%] | 🔴 / 🟡 / 🟢 |
| SFX-xxx | ≥30 | [Count] | [%] | 🔴 / 🟡 / 🟢 |
| MUS-xxx | ≥5 | [Count] | [%] | 🔴 / 🟡 / 🟢 |
| **TOTAL** | **≥200** | **[Count]** | **[%]** | **QG-ART-002: [PASS/FAIL]** |

### Priority Breakdown

| Priority | Description | Count | % of Total |
|----------|-------------|-------|------------|
| **P0** | MVP (Minimum Viable Product) | [Count] | [%] |
| **P1** | Soft Launch | [Count] | [%] |
| **P2** | Full Launch | [Count] | [%] |

### Status Breakdown

| Status | Count | % of Total |
|--------|-------|------------|
| **Pending** | [Count] | [%] |
| **In Progress** | [Count] | [%] |
| **Complete** | [Count] | [%] |
| **Approved** | [Count] | [%] |

### Memory Budget Tracking

| Resource | Budget | Current | % Used | Status |
|----------|--------|---------|--------|--------|
| **Texture Memory** | 256MB | [Current MB] | [%] | 🟢 OK / 🟡 Warning (>80%) / 🔴 Over Budget |
| **Audio Memory** | 64MB | [Current MB] | [%] | 🟢 / 🟡 / 🔴 |
| **Total** | 320MB | [Current MB] | [%] | **QG-ART-003: [PASS/FAIL]** |

---

## Production Workflow

### Asset Creation Pipeline

```
1. Concept Art → 2D sketch, reference gathering
2. 3D Modeling (if applicable) → Blender/Maya/ZBrush
3. Texturing → Substance Painter, Photoshop
4. Rigging (characters) → Bone hierarchy, weight painting
5. Animation → Keyframe animation, export as sprite sheet
6. Rendering → Render to PNG @3x resolution
7. Post-Processing → Color correction, alpha cleanup
8. Compression → Downscale to @2x, @1x, compress to target format
9. Import to Engine → Unity/Unreal asset import
10. Testing → Visual validation, performance profiling
11. Approval → Art director review, QG-ART-005 validation
```

### Folder Structure

```
/assets/
  /characters/
    /hero/
      char_hero_warrior_idle@3x.png
      char_hero_warrior_walk@3x.png
      ...
    /enemies/
      char_enemy_skeleton_idle@2x.png
      ...
  /environments/
    /garden/
      env_garden_tileset_ground@3x.png
      ...
  /props/
    char_prop_coin@3x.png
    ...
  /ui/
    /buttons/
      ui_btn_play_normal@3x.png
      ui_btn_play_pressed@3x.png
      ...
    /icons/
      ui_icon_settings@3x.png
      ...
  /vfx/
    vfx_combo_2x@2x.png
    ...
  /audio/
    /sfx/
      sfx_ui_tap_01.ogg
      ...
    /music/
      mus_level_theme_garden.mp3
      ...
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [YYYY-MM-DD] | [Agent: asset-cataloger-agent] | Initial asset catalog |

---

**Next Steps**:
1. → Populate catalog with all 200+ assets (fill in [Count] placeholders)
2. → Assign unique IDs (CHAR-001, ENV-001, etc.)
3. → Prioritize assets (P0 for MVP, P1/P2 for later phases)
4. → Validate QG-ART-002 (≥200 assets cataloged)
5. → Handoff to `/speckit.tasks` for production task breakdown
6. → Track progress: Update status column as assets move through pipeline

---

*Asset Catalog v1.0 | Generated by asset-cataloger-agent | Part of World-Class Mobile Game Art Production Pipeline*

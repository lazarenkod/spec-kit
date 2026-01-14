# Audio Requirements (ASMR Design)

---
metadata:
  version: "1.0"
  audio_engine: "[FMOD/Wwise/Unity Audio/Unreal Audio/Custom]"
  total_audio_assets: "[Count ≥35 (30 SFX + 5 music)]"
  latency_budget: "<50ms (UI: <20ms, Gameplay: <30ms)"
  memory_budget: "≤64MB"
  format_primary: "Ogg Vorbis (Android), AAC (iOS)"
  bitrate_sfx: "192kbps"
  bitrate_music: "128kbps"
  sample_rate: "44.1kHz (standard)"
  created: "[YYYY-MM-DD]"
  last_updated: "[YYYY-MM-DD]"
  status: "Draft | In Review | Approved | Production Ready"
---

> **Purpose**: Complete ASMR-quality audio design specifications for world-class mobile game production.
> **Scope**: Material-specific sound library, audio layers, adaptive music, spatial audio, latency optimization.
> **Integration**: Synced with animation library (<50ms latency budget, animation event triggers).

---

## 1. ASMR Sound Design Principles

### What is ASMR Audio Design?

**ASMR** (Autonomous Sensory Meridian Response): Tingling, satisfying sensation triggered by specific audio stimuli.

**In Games**: High-fidelity, material-specific sounds with <50ms latency that create tactile, satisfying interactions.

**Why It Matters**:
- **Player Retention**: Satisfying sounds = players stay engaged longer
- **Perceived Quality**: High-quality audio = "premium" feel, justifies IAP pricing
- **Competitive Advantage**: Most mobile games have generic audio (stock sound libraries)
- **Viral Potential**: ASMR moments → social media clips, word-of-mouth

### Core ASMR Principles (5 pillars)

| Principle | Description | Implementation | Example |
|-----------|-------------|----------------|---------|
| **Tactile** | Sounds must feel physical, like real objects | Material-specific recordings (wood, metal, glass) | Coin clink (metal), not generic "ding" |
| **Proximity** | Close-mic recordings, intimate feel | High-fidelity, minimal reverb for UI sounds | Hear finger sliding on glass, not distant tap |
| **Precision** | Timing synchronized with visuals (<50ms) | Preload critical sounds, audio-on-touch | Ball hits slot exactly when animation completes |
| **Satisfaction** | Sounds must resolve tension (complete the loop) | Pitched correctly, natural decay | Match clear = ascending chime (resolved) |
| **Subtlety** | Not loud/aggressive, gentle and pleasant | Volume mixing, no harsh frequencies | Soft "plop" for ball placement, not "thud" |

**ASMR Rating Scale** (1-5):
- **5/5**: World-class ASMR (e.g., glass crystal ting, liquid pour, metal coin clink)
- **4/5**: High-quality satisfying (e.g., wood knock, fabric swoosh, organic squish)
- **3/5**: Good but not peak (e.g., stone tap, generic click)
- **2/5**: Functional but not satisfying (e.g., stock UI beep)
- **1/5**: Poor quality (e.g., compressed, harsh, generic)

**Target**: ≥4/5 ASMR rating for all feedback sounds (UI taps, gameplay actions)

---

## 2. Material-Specific Sound Categories

### Material Sound Library (8 materials minimum)

Each material MUST have 4 core sounds: **Tap, Place, Break, Combo**

#### 2.1. Wood Sounds (MAT-WOOD-xxx)

| Sound ID | Event | ASMR Rating | Duration | Pitch | Description |
|----------|-------|-------------|----------|-------|-------------|
| MAT-WOOD-001 | Tap (Light) | 4/5 | 0.1s | C5 (523Hz) | Knuckle knock on oak table |
| MAT-WOOD-002 | Place (Drop) | 4/5 | 0.3s | G4 (392Hz) | Wooden block placed on desk |
| MAT-WOOD-003 | Break (Crack) | 4/5 | 0.5s | D4 (294Hz) | Snapping twig, dry crack |
| MAT-WOOD-004 | Combo (Thud) | 4/5 | 0.4s | A3 (220Hz) | Heavy wood impact, resonance |

**Use Cases**: Wooden boxes, barrels, platforms, forest props

**Recording Notes**:
- Wood type: Oak (resonant), Balsa (light), Bamboo (hollow)
- Close-mic (6 inches), capture natural reverb
- Avoid splinters (harsh frequencies), focus on mid-range (200-800Hz)

---

#### 2.2. Metal Sounds (MAT-METAL-xxx)

| Sound ID | Event | ASMR Rating | Duration | Pitch | Description |
|----------|-------|-------------|----------|-------|-------------|
| MAT-METAL-001 | Tap (Coin Clink) | 5/5 | 0.15s | E5 (659Hz) | Two coins clinking together |
| MAT-METAL-002 | Place (Sword Unsheathe) | 5/5 | 0.4s | C4 (262Hz) | Blade sliding on metal scabbard |
| MAT-METAL-003 | Break (Clang) | 4/5 | 0.6s | G3 (196Hz) | Metal sheet impact, reverb |
| MAT-METAL-004 | Combo (Gong) | 5/5 | 1.2s | A2 (110Hz) | Gong strike, long decay |

**Use Cases**: Coins, treasure, weapons, armor, machinery

**Recording Notes**:
- Metal type: Brass (warm), Steel (bright), Gold (soft)
- Capture long decay (3-5 seconds), trim to fit
- High-frequency content (1kHz-8kHz), EQ to taste

---

#### 2.3. Glass/Crystal Sounds (MAT-GLASS-xxx)

| Sound ID | Event | ASMR Rating | Duration | Pitch | Description |
|----------|-------|-------------|----------|-------|-------------|
| MAT-GLASS-001 | Tap (Crystal Ting) | 5/5 | 0.2s | A5 (880Hz) | Wine glass rim tap, clear pitch |
| MAT-GLASS-002 | Place (Bottle Clink) | 5/5 | 0.25s | E5 (659Hz) | Glass bottle set on table |
| MAT-GLASS-003 | Break (Shatter) | 4/5 | 0.8s | Multi-pitch | Wine glass breaking, clean shards |
| MAT-GLASS-004 | Combo (Chime) | 5/5 | 1.5s | C6 (1047Hz) | Wind chime, multiple pitches, reverb |

**Use Cases**: Potions, crystals, gems, magic items

**Recording Notes**:
- Glass type: Wine glass (pure tone), Bottle (lower pitch), Crystal (bright)
- Record at 96kHz (capture ultrasonic harmonics), downsample to 44.1kHz
- Very high ASMR potential, prioritize these sounds

---

#### 2.4. Stone/Rock Sounds (MAT-STONE-xxx)

| Sound ID | Event | ASMR Rating | Duration | Pitch | Description |
|----------|-------|-------------|----------|-------|-------------|
| MAT-STONE-001 | Tap (Echo) | 3/5 | 0.3s | D4 (294Hz) | Knocking on stone wall, echo |
| MAT-STONE-002 | Place (Rock Drop) | 3/5 | 0.4s | G3 (196Hz) | Stone dropped on concrete |
| MAT-STONE-003 | Break (Crumble) | 3/5 | 0.7s | Multi-pitch | Rock crushing, debris |
| MAT-STONE-004 | Combo (Rumble) | 3/5 | 1.0s | C2 (65Hz) | Boulder rolling, low-frequency |

**Use Cases**: Castle walls, caves, boulders, statues

**Recording Notes**:
- Stone type: Granite (hard), Limestone (soft), Marble (resonant)
- Low-frequency content (50-500Hz), use subwoofer-capable monitoring
- Natural reverb (caves, quarries) adds authenticity

---

#### 2.5. Fabric/Cloth Sounds (MAT-FABRIC-xxx)

| Sound ID | Event | ASMR Rating | Duration | Pitch | Description |
|----------|-------|-------------|----------|-------|-------------|
| MAT-FABRIC-001 | Tap (Brush) | 4/5 | 0.15s | White noise | Soft fabric brush, ASMR trigger |
| MAT-FABRIC-002 | Place (Cloth Drop) | 4/5 | 0.3s | Pitched noise | Silk cloth settling on surface |
| MAT-FABRIC-003 | Break (Rip) | 3/5 | 0.5s | Crackle | Fabric tearing, satisfying rip |
| MAT-FABRIC-004 | Combo (Swoosh) | 4/5 | 0.4s | Airy | Large flag waving, air movement |

**Use Cases**: Cloaks, flags, tents, inventory bags

**Recording Notes**:
- Fabric type: Silk (smooth), Linen (crisp), Velvet (soft)
- Close-mic (contact mic on fabric), capture texture
- High-frequency noise (5kHz-15kHz), gentle and pleasant

---

#### 2.6. Liquid/Water Sounds (MAT-LIQUID-xxx)

| Sound ID | Event | ASMR Rating | Duration | Pitch | Description |
|----------|-------|-------------|----------|-------|-------------|
| MAT-LIQUID-001 | Tap (Drop) | 5/5 | 0.1s | E5 (659Hz) | Single water drop, plop |
| MAT-LIQUID-002 | Place (Pour) | 5/5 | 0.8s | Broadband | Pouring water into cup, glug-glug |
| MAT-LIQUID-003 | Break (Splash) | 4/5 | 0.6s | Multi-pitch | Object falling into water, splash |
| MAT-LIQUID-004 | Combo (Bubble Pop) | 5/5 | 0.2s | Variable | Bubble bursting, satisfying pop |

**Use Cases**: Potions, rivers, rain, fountains

**Recording Notes**:
- Liquid type: Water (clean), Thick liquid (honey, syrup)
- Close-mic (hydrophone for underwater), capture bubble details
- Very high ASMR potential, pitch variation adds interest

---

#### 2.7. Organic/Soft Sounds (MAT-ORGANIC-xxx)

| Sound ID | Event | ASMR Rating | Duration | Pitch | Description |
|----------|-------|-------------|----------|-------|-------------|
| MAT-ORGANIC-001 | Tap (Squish) | 4/5 | 0.2s | Low-pitch | Soft sponge squished |
| MAT-ORGANIC-002 | Place (Plop) | 4/5 | 0.25s | G3 (196Hz) | Jelly dropped on plate |
| MAT-ORGANIC-003 | Break (Squelch) | 3/5 | 0.5s | Wet noise | Soft object bursting, gooey |
| MAT-ORGANIC-004 | Combo (Slime Stretch) | 4/5 | 0.7s | Crackle | Slime stretched and released |

**Use Cases**: Slimes, blobs, flesh, plants

**Recording Notes**:
- Materials: Slime (homemade), Gelatin, Fruit (squishing)
- Contact mic, capture internal sounds
- Slightly gross but satisfying (tread carefully)

---

#### 2.8. Magical/Synth Sounds (MAT-MAGICAL-xxx)

| Sound ID | Event | ASMR Rating | Duration | Pitch | Description |
|----------|-------|-------------|----------|-------|-------------|
| MAT-MAGICAL-001 | Tap (Sparkle) | 5/5 | 0.3s | A5 (880Hz) + harmonics | Ascending glissando, bell-like |
| MAT-MAGICAL-002 | Place (Whoosh) | 5/5 | 0.5s | Swept | Frequency sweep, magical energy |
| MAT-MAGICAL-003 | Break (Poof) | 4/5 | 0.4s | Descending | Object vanishing, downward sweep |
| MAT-MAGICAL-004 | Combo (Enchant) | 5/5 | 1.0s | Layered | Multiple tones, shimmer, reverb |

**Use Cases**: Magic spells, power-ups, special effects

**Recording Notes**:
- Synthesized (not recorded), use Serum/Omnisphere
- Layering: Bell + synth pad + shimmer reverb
- Pitch bending, modulation for "magic" feel

---

## 3. Audio Layers (Hierarchy Diagram)

### Layer Architecture

```
Master Output (0dB)
├── Music Layer (-6dB)
│   ├── Drums (sub-layer)
│   ├── Bass (sub-layer)
│   ├── Melody (sub-layer)
│   └── Harmony (sub-layer)
├── SFX Layer (-3dB)
│   ├── Combat (sub-layer, -3dB)
│   ├── Feedback (sub-layer, 0dB)
│   └── Environment (sub-layer, -6dB)
├── UI Layer (0dB, highest priority)
│   ├── Button Taps
│   ├── Notifications
│   └── Error/Success
└── Ambience Layer (-12dB, lowest priority)
    ├── Wind
    ├── Crickets
    └── Background loops
```

### Layer Specifications

| Layer | Volume (dB) | Priority | Duck When | Use Case |
|-------|-------------|----------|-----------|----------|
| **Master** | 0dB | N/A | N/A | Final output, user-controlled |
| **Music** | -6dB | Low | SFX plays | Background music, loops |
| **SFX Combat** | -3dB | High | N/A | Attacks, explosions, impacts |
| **SFX Feedback** | 0dB | Highest | N/A | Coin collect, match clear (never duck) |
| **SFX Environment** | -6dB | Medium | Combat SFX | Footsteps, ambience |
| **UI** | 0dB | Highest | N/A | Button taps, notifications (never duck) |
| **Ambience** | -12dB | Lowest | Any SFX | Wind, crickets, background loops |

### Volume Mixing Guidelines

**Reference Levels** (RMS, normalized):

| Layer | RMS Target | Peak Target | Notes |
|-------|------------|-------------|-------|
| **Music** | -18dB RMS | -6dB peak | Compressed, mastered |
| **SFX (Feedback)** | -12dB RMS | -3dB peak | Prominent, cuts through music |
| **SFX (Combat)** | -15dB RMS | -6dB peak | Balanced with music |
| **UI Taps** | -10dB RMS | -3dB peak | Very prominent, instant feedback |
| **Ambience** | -24dB RMS | -18dB peak | Barely audible, subconscious |

**Ducking Rules**:
- **Music** ducks -6dB when SFX plays (side-chain compression, 50ms attack, 200ms release)
- **Ambience** ducks -10dB when any SFX plays
- **UI** and **Feedback** SFX NEVER duck (critical for game feel)

### User Controls

**Volume Sliders** (independent control):
| Control | Default | Range | Storage |
|---------|---------|-------|---------|
| **Master** | 80% | 0-100% | PlayerPrefs (persistent) |
| **Music** | 70% | 0-100% | PlayerPrefs |
| **SFX** | 100% | 0-100% | PlayerPrefs |
| **Mute All** | Off | On/Off | PlayerPrefs |

**Haptic Feedback** (iOS: UIImpactFeedbackGenerator, Android: Vibrator):
- **Light**: Button taps (10ms, intensity 0.3)
- **Medium**: Coin collect (20ms, intensity 0.6)
- **Heavy**: Match clear (30ms, intensity 1.0)

---

## 4. Audio Format Specifications

### Platform-Specific Formats

| Platform | Format | Codec | Bitrate | Sample Rate | Container |
|----------|--------|-------|---------|-------------|-----------|
| **iOS** | AAC | AAC-LC | 192kbps (SFX), 128kbps (music) | 44.1kHz | .m4a |
| **Android** | Ogg Vorbis | Vorbis | 192kbps (SFX), 128kbps (music) | 44.1kHz | .ogg |
| **WebGL** | WebM Opus | Opus | 128kbps (all) | 48kHz | .webm |

### Technical Specifications

**SFX (UI, Gameplay)**:
- **Format**: Ogg Vorbis (Android), AAC-LC (iOS)
- **Bitrate**: 192kbps (VBR, quality 6)
- **Sample Rate**: 44.1kHz
- **Channels**: Mono (UI), Stereo (gameplay SFX with spatial positioning)
- **Normalization**: -3dB peak (headroom for mixing)
- **File Size**: <500KB per file (target: 100-200KB)

**Music (Loops)**:
- **Format**: Ogg Vorbis (Android), AAC-LC (iOS)
- **Bitrate**: 128kbps (VBR, quality 5)
- **Sample Rate**: 44.1kHz
- **Channels**: Stereo
- **Normalization**: -6dB peak (more headroom, mastered with limiting)
- **File Size**: <3MB per track (target: 2-2.5MB for 2-minute loop)

### Source Requirements (for audio engineers)

**Recording Specs** (before compression):
- **Format**: WAV (uncompressed)
- **Bit Depth**: 24-bit (source), 16-bit (final)
- **Sample Rate**: 48kHz (recording), 44.1kHz (final, sample rate conversion)
- **Headroom**: -6dB peak (allow for processing)
- **Noise Floor**: <-60dB (clean recordings, no hiss)

**Processing Chain**:
```
1. Recording (24-bit, 48kHz, WAV)
2. Editing (trim silence, remove clicks)
3. EQ (high-pass filter at 80Hz, remove rumble)
4. Compression (gentle 2:1 ratio, -20dB threshold)
5. Normalization (-3dB peak for SFX, -6dB for music)
6. Sample Rate Conversion (48kHz → 44.1kHz, high-quality SRC)
7. Dithering (24-bit → 16-bit, POW-r dithering)
8. Encoding (Ogg Vorbis Q6 / AAC 192kbps)
9. Validation (A/B comparison, listening test)
```

---

## 5. Adaptive Audio System

### Music Layering (Horizontal Re-Sequencing)

**Dynamic Music**: Music intensity adapts to gameplay state (calm → tense → combat).

**Layer Configuration**:
| Layer | State | Instruments | Volume |
|-------|-------|-------------|--------|
| **Layer 1** | Calm (Idle) | Pad + Ambient | Full |
| **Layer 2** | Tense (Low Health) | + Strings | Full |
| **Layer 3** | Combat (Active) | + Drums + Bass | Full |
| **Layer 4** | Boss Battle | + Brass + Choir | Full |

**Implementation** (FMOD/Wwise parameters):
```yaml
music_intensity:
  parameter: "gameplay_state"  # 0 = calm, 1 = tense, 2 = combat, 3 = boss
  layers:
    - layer: "pad_ambient"
      volume_curve: [1.0, 0.8, 0.6, 0.4]  # Fades out as intensity increases
    - layer: "strings"
      volume_curve: [0.0, 1.0, 1.0, 1.0]  # Fades in at tense+
    - layer: "drums_bass"
      volume_curve: [0.0, 0.0, 1.0, 1.0]  # Fades in at combat+
    - layer: "brass_choir"
      volume_curve: [0.0, 0.0, 0.0, 1.0]  # Only in boss battle
```

### Dynamic Mixing (Vertical Remixing)

**Ducking**: Automatic volume adjustment when multiple sounds play.

**Implementation**:
```yaml
ducking_rules:
  - source: "sfx_combat"
    target: "music"
    reduction: -6dB
    attack: 50ms
    release: 200ms
  - source: "ui_notification"
    target: "ambience"
    reduction: -10dB
    attack: 10ms
    release: 500ms
```

### Spatial Audio (3D Positioning)

**3D Audio**: Sounds positioned in 3D space, volume/pan based on distance/direction.

**Configuration**:
| Sound Type | 3D/2D | Min Distance | Max Distance | Rolloff | Use Case |
|------------|-------|--------------|--------------|---------|----------|
| **UI Taps** | 2D | N/A | N/A | N/A | Always center, full volume |
| **Footsteps** | 3D | 1 unit | 10 units | Logarithmic | Character movement |
| **Combat SFX** | 3D | 2 units | 20 units | Linear | Attacks, impacts |
| **Ambience** | 3D | 0 units | 50 units | Logarithmic | Wind, water, birds |

**Rolloff Curves**:
- **Logarithmic**: Realistic (inverse-square law), sounds drop off quickly
- **Linear**: Gradual falloff, easier to tune
- **Custom**: Artist-defined curve (e.g., steep drop near max distance)

**Reverb Zones**:
| Zone | Reverb Type | Decay Time | Wet/Dry | Use Case |
|------|-------------|------------|---------|----------|
| **Garden (Outdoor)** | Open space | 0.8s | 20% / 80% | Levels 1-20 |
| **Cave (Indoor)** | Large hall | 2.5s | 50% / 50% | Levels 21-40 |
| **Ocean (Underwater)** | Underwater | 1.5s | 40% / 60% | Levels 41-60 |

---

## 6. Sound Effect Categories

### UI Sounds (UI-xxx)

| Sound ID | Event | Latency Target | Format | Use Case |
|----------|-------|----------------|--------|----------|
| UI-SFX-001 | Button Tap | <20ms | Ogg/AAC, Preloaded | Any button press |
| UI-SFX-002 | Button Hover | <30ms | Ogg/AAC, Preloaded | Desktop hover (mobile: no hover) |
| UI-SFX-003 | Panel Slide In | <50ms | Ogg/AAC, Streamed | Settings panel opens |
| UI-SFX-004 | Panel Slide Out | <50ms | Ogg/AAC, Streamed | Settings panel closes |
| UI-SFX-005 | Notification | <50ms | Ogg/AAC, Preloaded | Achievement unlocked |
| UI-SFX-006 | Error | <30ms | Ogg/AAC, Preloaded | Invalid action |
| UI-SFX-007 | Success | <30ms | Ogg/AAC, Preloaded | Level complete, purchase success |

**Preload Strategy**: All UI sounds <100KB preloaded at app start (critical path).

---

### Gameplay Sounds (GAME-xxx)

| Sound ID | Event | Latency Target | Format | Use Case |
|----------|-------|----------------|--------|----------|
| GAME-SFX-001 | Ball Place | <30ms | Ogg/AAC, Preloaded | Place ball in slot |
| GAME-SFX-002 | Match Clear | <30ms | Ogg/AAC, Preloaded | Line/group cleared |
| GAME-SFX-003 | Combo 2x | <30ms | Ogg/AAC, Preloaded | 2x combo triggered |
| GAME-SFX-004 | Combo 3x | <30ms | Ogg/AAC, Preloaded | 3x combo triggered |
| GAME-SFX-005 | Combo 4x+ | <30ms | Ogg/AAC, Preloaded | 4x+ combo triggered |
| GAME-SFX-006 | Coin Collect | <30ms | Ogg/AAC, Preloaded | Currency pickup |
| GAME-SFX-007 | Power-Up | <50ms | Ogg/AAC, Preloaded | Power-up activated |

---

### Combat Sounds (if applicable)

| Sound ID | Event | Latency Target | Format | Use Case |
|----------|-------|----------------|--------|----------|
| COMBAT-SFX-001 | Sword Swing | <40ms | Ogg/AAC, Preloaded | Melee attack |
| COMBAT-SFX-002 | Hit Impact | <30ms | Ogg/AAC, Preloaded | Attack connects |
| COMBAT-SFX-003 | Bow Release | <40ms | Ogg/AAC, Preloaded | Ranged attack |
| COMBAT-SFX-004 | Magic Cast | <50ms | Ogg/AAC, Preloaded | Spell cast |
| COMBAT-SFX-005 | Explosion | <50ms | Ogg/AAC, Streamed | Large area damage |

---

## 7. Music Requirements

### Track List

| Track ID | Name | Zone | Duration | Loop Point | Mood | BPM |
|----------|------|------|----------|------------|------|-----|
| MUS-001 | Main Menu Theme | Menu | 2:30 | 0:00 → 2:30 | Upbeat, welcoming | 120 |
| MUS-002 | Garden Level Theme | Zone 1 | 2:00 | 0:00 → 2:00 | Calm, spring-like | 100 |
| MUS-003 | Desert Level Theme | Zone 2 | 2:15 | 0:00 → 2:15 | Warm, adventurous | 110 |
| MUS-004 | Ocean Level Theme | Zone 3 | 2:20 | 0:00 → 2:20 | Cool, mysterious | 95 |
| MUS-005 | Boss Battle Theme | Boss | 1:45 | 0:00 → 1:45 | Intense, epic | 140 |

### Music Composition Guidelines

**Genre**: [Orchestral, Electronic, Chiptune, Hybrid, etc.]

**Instrumentation**:
- **Lead**: [Piano, Synth, Guitar, etc.]
- **Harmony**: [Strings, Pads, Choir, etc.]
- **Rhythm**: [Drums, Percussion, etc.]
- **Bass**: [Bass guitar, Sub bass, 808, etc.]

**Emotional Arc** (per track):
```
0:00-0:30 — Introduction (establish theme)
0:30-1:30 — Development (variation, build)
1:30-2:00 — Climax (full instrumentation)
2:00-2:30 — Outro (fade to loop point)
```

**Loop Points** (seamless transition):
- **Tempo-Synced**: Loop on downbeat (bar 1, beat 1)
- **Crossfade**: 1-2 second crossfade at loop point (overlapping tails)
- **No Silence**: Gap-free loop (use DAW's loop markers)

---

## 8. Latency Requirements

### Latency Targets by Category

| Sound Category | Max Latency | Priority | Optimization Strategy |
|----------------|-------------|----------|----------------------|
| **UI Tap** | <20ms | CRITICAL | Preload, uncompressed (WAV on mobile) |
| **Gameplay Action** | <30ms | HIGH | Preload, low-latency codec (Ogg Vorbis Q6) |
| **Feedback** | <50ms | HIGH | Streaming OK if preload buffer <50ms |
| **Music** | <100-200ms | MEDIUM | Streaming (acceptable latency) |
| **Ambience** | <200ms | LOW | Streaming, low priority |

### Latency Optimization Techniques

**1. Preloading** (eliminate disk I/O latency):
```csharp
// Unity example: Preload critical sounds at app start
void Start() {
    AudioClip uiTap = Resources.Load<AudioClip>("UI/tap");
    uiTap.LoadAudioData();  // Force load into memory
}
```

**2. Low-Latency Audio Settings** (engine configuration):
```yaml
# Unity Audio Settings
dsp_buffer_size: 256  # Lower = less latency (512 default, 256 low-latency)
sample_rate: 44100    # Standard (48000 for pro audio)
output_format: Stereo
```

**3. Uncompressed Formats** (UI sounds <20ms):
- **UI Tap**: WAV (uncompressed) on mobile, <100KB each
- **Trade-off**: Larger file size (5-10x) vs latency (<5ms)

**4. Audio Pool** (object pooling):
```csharp
// Reuse AudioSource components (avoid GC allocation)
AudioSource[] audioSourcePool = new AudioSource[10];
int currentIndex = 0;

void PlaySound(AudioClip clip) {
    audioSourcePool[currentIndex].clip = clip;
    audioSourcePool[currentIndex].Play();
    currentIndex = (currentIndex + 1) % audioSourcePool.Length;
}
```

**5. Native Platform APIs** (lowest possible latency):
- **iOS**: AVAudioEngine (CoreAudio), <10ms with 256 buffer
- **Android**: OpenSL ES / AAudio, <20ms with 192-256 buffer
- **Unity**: Enable "Best Latency" in Audio Settings

---

## 9. Quality Validation Checklist

**Use this checklist when self-reviewing audio requirements**:

### Audio Fidelity (AF-* checkpoints)
- [ ] AF-01: Material sound library covers ≥8 materials (wood, metal, glass, stone, fabric, liquid, organic, magical)
- [ ] AF-02: Latency compliance documented (<50ms total, UI <20ms, gameplay <30ms)
- [ ] AF-03: Music integration complete (track list, layering system, ducking rules, loop points)
- [ ] AF-04: ASMR quality ratings assigned (≥4/5 for feedback sounds, tactile/proximity/precision/satisfaction/subtlety)
- [ ] AF-05: Spatial audio and reverb zones specified (3D positioning, rolloff curves, reverb per environment)

### Technical Validation
- [ ] All audio assets have format specifications (Ogg Vorbis/AAC, bitrate, sample rate)
- [ ] Memory budget ≤64MB (sum of all audio assets)
- [ ] Preload strategy documented (UI sounds preloaded, music/ambience streamed)
- [ ] Latency targets achievable (<50ms validated with profiler or high-speed camera)
- [ ] Volume mixing guidelines defined (RMS targets, ducking rules, user controls)

### Integration Validation
- [ ] Audio cues mapped to animation events (footsteps, attacks, impacts)
- [ ] Animation timing synced with audio (<50ms latency budget, QG-ART-004)
- [ ] VFX triggers mapped to audio events (explosion sound + particle spawn)

---

## 10. Audio Asset Summary

### Asset Count by Category

| Category | Target | Current | % Complete | Status |
|----------|--------|---------|------------|--------|
| UI Sounds | ≥10 | [Count] | [%] | 🔴 / 🟡 / 🟢 |
| Gameplay SFX | ≥15 | [Count] | [%] | 🔴 / 🟡 / 🟢 |
| Material Sounds | ≥8 materials × 4 sounds = 32 | [Count] | [%] | 🔴 / 🟡 / 🟢 |
| Music Tracks | ≥5 | [Count] | [%] | 🔴 / 🟡 / 🟢 |
| **TOTAL AUDIO** | **≥35** | **[Count]** | **[%]** | **QG-ART-002 (Audio Component)** |

### Memory Budget Tracking

| Resource | Budget | Current | % Used | Status |
|----------|--------|---------|--------|--------|
| **Audio Memory** | 64MB | [Current MB] | [%] | 🟢 OK / 🟡 Warning (>80%) / 🔴 Over Budget |

---

## 11. Production Workflow

### Audio Creation Pipeline

```
1. Design Brief → Define sound requirements (material, mood, ASMR rating)
2. Reference Gathering → Find inspiration (Freesound, commercial games)
3. Recording (if applicable) → High-quality recording (24-bit, 48kHz, close-mic)
4. Synthesis (if applicable) → Create sound in DAW (Serum, Omnisphere)
5. Editing → Trim silence, remove noise, normalize to -6dB
6. Processing → EQ, compression, reverb (if needed)
7. Export Source → WAV, 16-bit, 44.1kHz
8. Encoding → Ogg Vorbis Q6 (Android), AAC 192kbps (iOS)
9. Import to Engine → Unity/Unreal audio import
10. Testing → Latency validation (high-speed camera), A/B listening test
11. Approval → Audio director review, QG-ART-004 validation (latency <50ms)
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [YYYY-MM-DD] | [Agent: audio-designer-agent] | Initial audio requirements |

---

**Next Steps**:
1. → Record/synthesize all material sounds (8 materials × 4 sounds = 32 files)
2. → Compose music tracks (5 tracks minimum)
3. → Validate latency targets (<50ms total, UI <20ms)
4. → Integrate with animation library (map audio events to animation frames)
5. → Test on target devices (profiler, high-speed camera validation)
6. → Validate QG-ART-004 (audio latency compliance)

---

*Audio Requirements v1.0 | Generated by audio-designer-agent | Part of World-Class Mobile Game Art Production Pipeline*

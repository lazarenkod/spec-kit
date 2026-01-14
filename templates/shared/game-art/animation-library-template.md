# Animation Library

---
metadata:
  version: "1.0"
  engine: "[Unity/Unreal/Custom]"
  animation_system: "[Mecanim/Animation Blueprint/Spine/Custom]"
  total_animations: "[Count]"
  frame_rate_targets:
    ui: "60fps"
    gameplay: "30fps"
    background: "15-20fps"
  memory_budget: "≤10MB"
  created: "[YYYY-MM-DD]"
  last_updated: "[YYYY-MM-DD]"
  status: "Draft | In Review | Approved | Production Ready"
---

> **Purpose**: Complete animation specifications for world-class mobile game animation production.
> **Scope**: Animation principles, timing, easing curves, state machines, performance budgets.
> **Integration**: Synced with audio requirements (<50ms latency budget for ASMR quality).

---

## 1. Animation System Overview

### State Machine Architecture

**Animation Controller Pattern**: Hierarchical State Machine (HSM)

```
Root State Machine
├── Base Layer (full body animations)
│   ├── Locomotion States (idle, walk, run)
│   ├── Action States (attack, cast, interact)
│   ├── Reaction States (hit, stagger, death)
│   └── Special States (victory, taunt)
├── Upper Body Layer (overrides, additive)
│   ├── Aim/Look At (head tracking)
│   └── Upper Body Actions (wave, point)
└── FX Layer (VFX triggers, no mesh deformation)
    ├── Particle Emitters
    └── Material Property Animations
```

### Layer Architecture

| Layer | Weight | Blend Mode | Purpose | Example |
|-------|--------|------------|---------|---------|
| **Base Layer** | 1.0 | Override | Full-body locomotion and actions | Idle, walk, attack |
| **Upper Body Layer** | 0.5-1.0 | Additive | Upper body overrides while moving | Wave while walking |
| **FX Layer** | 1.0 | Override | Visual effects triggers | Particle spawn on attack |

**Rationale**: Layered system allows walk + wave simultaneously (upper body additive on locomotion).

---

## 2. Animation Types

### Core Animation Categories

| Category | Count | Frame Rate | Loop | Priority | Examples |
|----------|-------|------------|------|----------|----------|
| **Idle** | [Count] | 30fps | Yes | P0 | Breathing, blinking, subtle movement |
| **Locomotion** | [Count] | 30fps | Yes | P0 | Walk, run, jump, land |
| **Action** | [Count] | 30fps | No | P0 | Attack, cast, interact, collect |
| **Reaction** | [Count] | 30fps | No | P0 | Hit, stagger, knockback, death |
| **Transition** | [Count] | 60fps | No | P1 | Idle→Walk, Walk→Run, smooth blends |
| **Victory/Defeat** | [Count] | 30fps | No | P1 | Win pose, lose animation |
| **Special/Emote** | [Count] | 30fps | No | P2 | Taunt, dance, emote |

### UI Animation Categories

| Category | Count | Frame Rate | Loop | Priority | Examples |
|----------|-------|------------|------|----------|----------|
| **Button States** | [Count] | 60fps | No | P0 | Normal→Pressed, Pressed→Normal |
| **Panel Transitions** | [Count] | 60fps | No | P0 | Slide in/out, fade in/out, scale |
| **HUD Elements** | [Count] | 60fps | Partial | P0 | Score increment, timer pulse, progress bar fill |
| **Notification** | [Count] | 60fps | No | P1 | Achievement popup, level up, combo text |

---

## 3. Animation Timing Specifications

### Frame Rate Standards

**Mobile Optimization**: Different frame rates for different animation types to balance quality and performance.

| Animation Type | Target FPS | Budget | Rationale |
|----------------|------------|--------|-----------|
| **UI Animations** | 60fps | Always 60fps (no reduction) | Responsiveness critical for UX, short duration (0.1-0.3s) |
| **Gameplay Characters** | 30fps | 60fps on high-end, 30fps on mid/low | Smooth enough, 50% less animation data |
| **Background Animations** | 15-20fps | 20fps high-end, 15fps mid/low | Barely noticeable, minimal performance impact |
| **VFX Particles** | 30-60fps | 60fps high-end, 30fps mid/low | Fast-moving particles look smooth at 30fps |

**Battery Mode Adjustments**:
```
High-End Devices (iPhone 14+):
- UI: 60fps (always)
- Gameplay: 30fps → 20fps (low power mode)
- Background: 20fps → 10fps
- VFX: 60fps → 30fps

Mid-Tier Devices (iPhone 11-13):
- UI: 60fps (always)
- Gameplay: 30fps (default)
- Background: 15fps (default)
- VFX: 30fps (default)

Low-End Devices (iPhone X):
- UI: 60fps (always, short durations compensate)
- Gameplay: 20fps (reduced from 30fps)
- Background: 10fps (reduced from 15fps)
- VFX: 20fps (reduced particle count also)
```

### Duration Guidelines

**Recommended durations per animation type**:

| Animation Type | Min Duration | Max Duration | Typical | Notes |
|----------------|--------------|--------------|---------|-------|
| **Button Press** | 0.1s | 0.2s | 0.15s | Instant feedback (<100ms perceived latency) |
| **Panel Transition** | 0.2s | 0.4s | 0.3s | Smooth but not slow |
| **Idle Loop** | 1.0s | 3.0s | 2.0s | Subtle, non-distracting |
| **Walk Cycle** | 0.4s | 0.8s | 0.6s | Matches typical walk speed |
| **Attack** | 0.3s | 0.8s | 0.5s | Snappy, readable |
| **Hit Reaction** | 0.2s | 0.4s | 0.3s | Quick, doesn't interrupt gameplay |
| **Death** | 0.5s | 1.5s | 1.0s | Dramatic but not too long |
| **Victory** | 1.0s | 2.0s | 1.5s | Celebratory, repeatable |

**Example**:
```markdown
**Button Press Animation**:
- Duration: 0.15s (150ms total)
- Breakdown: Scale down (0.05s) → Hold (0.05s) → Scale up (0.05s)
- Frame count: 9 frames @ 60fps (60 × 0.15 = 9)

**Character Attack**:
- Duration: 0.5s (500ms total)
- Breakdown: Wind-up (0.1s) → Strike (0.1s) → Follow-through (0.3s)
- Frame count: 15 frames @ 30fps (30 × 0.5 = 15)
```

---

## 4. Easing Curves Library

### Standard Easing Curves

**Built-in curves** (available in most engines):

| Curve Name | Cubic Bezier | Use Case | Example |
|------------|--------------|----------|---------|
| **Linear** | (0, 0, 1, 1) | Constant speed, mechanical movement | Conveyor belt, rotating platform |
| **Ease In** | (0.42, 0, 1, 1) | Accelerate from stop | Heavy object starting to move |
| **Ease Out** | (0, 0, 0.58, 1) | Decelerate to stop | Object landing, UI sliding in |
| **Ease In-Out** | (0.42, 0, 0.58, 1) | Smooth acceleration and deceleration | Camera pan, natural movement |

### Performance-Optimized Curves

**Custom curves for mobile games** (smooth but not CPU-intensive):

| Curve Name | Cubic Bezier | Use Case | Example |
|------------|--------------|----------|---------|
| **Ease Out Game** | (0, 0.5, 0.5, 1) | Fast start, slow end (common in games) | UI popups, projectiles landing |
| **Ease In Game** | (0.5, 0, 1, 0.5) | Slow start, fast end | Object launching, anticipation |
| **Spring** | Custom (overshoot) | Bounce effect, playful feel | Button press, collectible pickup |
| **Bounce** | Custom (multiple peaks) | Exaggerated impact | Object dropping, ball bounce |

**Cubic Bezier Reference**:
```css
/* CSS cubic-bezier(x1, y1, x2, y2) */
ease-out-game: cubic-bezier(0, 0.5, 0.5, 1);
ease-in-game: cubic-bezier(0.5, 0, 1, 0.5);
spring: cubic-bezier(0.5, 1.5, 0.5, 1);  /* Overshoot to 1.5, settle at 1 */
bounce: /* Multi-keyframe required, not a single cubic-bezier */
```

### Game-Specific Curves

**Custom curves for this game's feel**:

| Curve Name | Cubic Bezier | Use Case | Example |
|------------|--------------|----------|---------|
| **[Custom 1]** | (x1, y1, x2, y2) | [Specific use case] | [Example animation] |
| **[Custom 2]** | (x1, y1, x2, y2) | [Specific use case] | [Example animation] |

**Example**:
```markdown
| Satisfying Sort | (0.2, 0.8, 0.3, 1.1) | Ball sliding into slot, slight overshoot | Ball placement animation |
| Quick Snap | (0.8, 0, 1, 0.2) | Instant acceleration, quick stop | UI button snap to position |
```

### Easing by Animation Type

**Recommended easing per animation category**:

| Animation Type | Easing Curve | Rationale |
|----------------|--------------|-----------|
| **Button Press** | Ease Out Game | Fast response, slow settle (feels snappy) |
| **Panel Slide In** | Ease Out | Smooth entry, decelerates at end |
| **Panel Slide Out** | Ease In | Accelerates away, feels responsive |
| **Projectile Launch** | Ease In | Slow start (anticipation), fast end (impact) |
| **Projectile Land** | Ease Out + Bounce | Decelerates, bounces on impact |
| **Score Increment** | Linear | Constant speed for readability |
| **Combo Text** | Spring | Overshoot (playful, satisfying) |
| **Death Animation** | Ease Out | Slow collapse, dramatic |

---

## 5. Squash & Stretch Parameters

### Animation Principles (from Disney's 12 Principles)

**Squash & Stretch**: Exaggerate deformation to convey weight, speed, and impact.

**Parameters**:
| Object Type | Squash Ratio | Stretch Ratio | Use Case |
|-------------|--------------|---------------|----------|
| **Characters** | 1.2-1.5x | 1.2-1.5x | Landing (squash 1.3x), jumping (stretch 1.4x) |
| **Objects (Soft)** | 1.3-1.6x | 1.3-1.6x | Ball bouncing (squash 1.5x on impact) |
| **Objects (Rigid)** | 1.1-1.2x | 1.1-1.2x | Minimal squash (metal, wood), slight stretch on fast movement |
| **UI Elements** | 0.9-1.1x | 0.95-1.05x | Subtle (buttons scale down 0.95x on press) |

**Example**:
```markdown
**Character Jump Animation**:
- Frame 1-3: Anticipation (squash to 1.0x width, 0.8x height)
- Frame 4-6: Launch (stretch to 0.8x width, 1.3x height)
- Frame 7-9: Peak (return to 1.0x width, 1.0x height)
- Frame 10-12: Fall (slight stretch to 0.9x width, 1.1x height)
- Frame 13-15: Land (squash to 1.3x width, 0.7x height)
- Frame 16-18: Recovery (return to 1.0x width, 1.0x height)

**Ball Bounce Animation**:
- Impact: Squash to 1.5x width, 0.6x height (40% height reduction)
- Hold: 2 frames at squash (feels weighted)
- Rebound: Stretch to 0.7x width, 1.4x height (40% height increase)
- Apex: Return to 1.0x width, 1.0x height (sphere shape)
```

### Anticipation and Follow-Through

**Anticipation**: Wind-up before action (telegraph for player readability).

| Action | Anticipation Duration | Anticipation Movement | Use Case |
|--------|----------------------|----------------------|----------|
| **Attack** | 0.1-0.2s (10-20% of total) | Pull back, crouch | Player can see attack coming, react |
| **Jump** | 0.1s | Crouch down | Conveys weight, builds energy |
| **Dash** | 0.05s | Lean forward | Minimal anticipation (fast action) |

**Follow-Through**: Overshoot and settle after action (natural momentum).

| Action | Follow-Through Duration | Overshoot | Use Case |
|--------|------------------------|-----------|----------|
| **Swing** | 0.2-0.3s (40-60% of total) | Weapon swings past target | Natural momentum |
| **Land** | 0.1s | Squash on impact, recover | Conveys weight |
| **Stop** | 0.1s | Slide 1-2 units past target | Character can't stop instantly |

---

## 6. Animation State Machines

### Player Character FSM

**State Machine Diagram** (ASCII art):

```
           ┌──────────────────────────────────────┐
           │                                      │
           │         ┌────────┐                   │
           └────────▶│  Idle  │◀──────────────────┘
                     └────┬───┘
                          │
                ┌─────────┼─────────┐
                │                   │
                ▼                   ▼
          ┌──────────┐        ┌──────────┐
          │   Walk   │        │   Jump   │
          └──────┬───┘        └────┬─────┘
                 │                 │
                 │                 ▼
                 │           ┌──────────┐
                 │           │   Fall   │
                 │           └────┬─────┘
                 │                │
                 │                ▼
                 │           ┌──────────┐
                 └──────────▶│   Land   │──────┐
                             └──────────┘      │
                                   │           │
                                   └───────────┘
                                       (back to Idle)

          ┌──────────┐        ┌──────────┐        ┌──────────┐
          │  Attack  │───────▶│   Hit    │───────▶│  Death   │
          └──────────┘        └──────────┘        └──────────┘
               │                     │
               └─────────────────────┘
                   (back to Idle if alive)
```

**State Transition Table**:

| From State | To State | Trigger | Blend Duration | Notes |
|------------|----------|---------|----------------|-------|
| **Idle** | Walk | `speed > 0.1` | 0.1s | Crossfade |
| **Idle** | Jump | `jump_pressed` | 0.05s | Instant transition |
| **Idle** | Attack | `attack_pressed` | 0.05s | Instant transition |
| **Walk** | Idle | `speed < 0.1` | 0.2s | Smooth deceleration |
| **Walk** | Jump | `jump_pressed` | 0.05s | From walk to jump |
| **Jump** | Fall | `velocity_y < 0` | 0.1s | Apex of jump |
| **Fall** | Land | `grounded` | 0.05s | Impact |
| **Land** | Idle | `animation_finished` | 0.1s | Recovery complete |
| **Any** | Hit | `damage_received` | 0.0s | Interrupt (no blend) |
| **Hit** | Idle | `animation_finished && alive` | 0.1s | Recover from hit |
| **Hit** | Death | `health <= 0` | 0.05s | Transition to death |
| **Death** | [None] | N/A | N/A | Terminal state |

**Blend Tree (Locomotion)**:

```yaml
# 1D Blend Tree for locomotion speed
blend_tree:
  type: "1D"
  parameter: "speed"  # 0.0 = idle, 1.0 = walk, 2.0 = run
  children:
    - motion: "idle"
      threshold: 0.0
    - motion: "walk"
      threshold: 1.0
    - motion: "run"
      threshold: 2.0
```

### Enemy Character FSM (simplified)

```
          ┌──────────┐        ┌──────────┐        ┌──────────┐
          │  Patrol  │───────▶│  Chase   │───────▶│  Attack  │
          └─────┬────┘        └─────┬────┘        └─────┬────┘
                │                   │                   │
                │                   └───────────────────┘
                │                         (back to Patrol)
                │
                ▼
          ┌──────────┐        ┌──────────┐
          │   Hit    │───────▶│  Death   │
          └──────────┘        └──────────┘
```

**State Transition Table** (Enemy):

| From State | To State | Trigger | Duration | Notes |
|------------|----------|---------|----------|-------|
| **Patrol** | Chase | `player_in_range` | 0.1s | Switch to aggressive |
| **Chase** | Attack | `player_in_attack_range` | 0.05s | Start attack |
| **Attack** | Chase | `animation_finished && player_out_of_attack_range` | 0.1s | Resume chase |
| **Chase** | Patrol | `player_out_of_range` | 0.2s | Give up chase |
| **Any** | Hit | `damage_received` | 0.0s | Interrupt |
| **Hit** | [Previous State] | `animation_finished && alive` | 0.1s | Resume previous |
| **Hit** | Death | `health <= 0` | 0.05s | Terminal |

---

## 7. Performance Budgets

### Animation Memory Budget

**Target**: ≤10MB total animation data (all clips combined)

| Category | Memory Allocation | Typical Clips | Notes |
|----------|-------------------|---------------|-------|
| **Player Character** | 3MB | 15 clips (idle, walk, attack, hit, death, etc.) | Highest quality, most visible |
| **Enemy Characters** | 4MB | 10 clips per enemy × 3 enemy types | Shared animations where possible |
| **UI Animations** | 1MB | 20 clips (button presses, panel transitions) | Short durations, low memory |
| **VFX Animations** | 1MB | Particle UVs, material animations | Texture-based, minimal bone data |
| **Background Animations** | 1MB | Ambient loops (flags, water, clouds) | Low priority, lowest quality |

### Bone Count Limits

**Mobile Rigging Budget**: ≤50 bones per character (Unity Mecanim, Unreal Skeletal Mesh)

| Character Type | Max Bones | Typical Bones | Notes |
|----------------|-----------|---------------|-------|
| **Hero** | 50 | 40 (spine 5, head 3, arms 16, legs 16) | Full expressiveness |
| **Enemy** | 40 | 30 (simplified spine, no fingers) | Reduced for performance |
| **NPC** | 30 | 20 (minimal facial, no fingers) | Background characters |

### Blend Time Budget

**Crossfade Duration**: Balance smoothness vs responsiveness

| Transition Type | Blend Duration | Rationale |
|-----------------|----------------|-----------|
| **Idle ↔ Walk** | 0.1-0.2s | Smooth, natural |
| **Idle → Jump** | 0.05s | Instant response (gameplay critical) |
| **Jump → Fall** | 0.1s | Natural progression |
| **Any → Hit** | 0.0s | Interrupt immediately (feedback critical) |
| **Hit → Idle** | 0.1s | Smooth recovery |

---

## 8. Quality Validation Checklist

**Use this checklist when self-reviewing animation specifications**:

### Animation Polish (AP-* checkpoints)
- [ ] AP-01: Frame rate standards documented (UI 60fps, gameplay 30fps, background 15-20fps)
- [ ] AP-02: Duration + easing specified per animation (cubic-bezier values)
- [ ] AP-03: State machines complete (player FSM, enemy FSM with transition tables)
- [ ] AP-04: Squash & stretch parameters documented (1.2-1.5x for characters, 1.3-1.6x for soft objects)
- [ ] AP-05: Animation timing synced with audio (<50ms latency budget for ASMR integration)

### Technical Validation
- [ ] All animated assets mapped to animation clips
- [ ] Frame counts calculated (duration × FPS)
- [ ] Memory budget ≤10MB (sum of all animation data)
- [ ] Bone count ≤50 per character (mobile rigging budget)
- [ ] Blend times specified (0.0s for interrupts, 0.1-0.2s for smooth transitions)

### Integration Validation
- [ ] Animation library synced with asset catalog (all animated assets have animation specs)
- [ ] Audio cues mapped to animation events (footsteps, attacks, impacts)
- [ ] VFX triggers mapped to animation events (particle spawn on attack frame 8)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [YYYY-MM-DD] | [Agent: animation-designer-agent] | Initial animation library |

---

**Next Steps**:
1. → Implement state machines in engine (Unity Animator, Unreal Animation Blueprint)
2. → Create animation clips (keyframe in DCC tool, export to engine)
3. → Test frame rates on target devices (profile with Instruments, Android GPU Inspector)
4. → Validate QG-ART-006 (animation frame rate compliance)
5. → Sync with audio requirements (audio-designer-agent output)

---

*Animation Library v1.0 | Generated by animation-designer-agent | Part of World-Class Mobile Game Art Production Pipeline*

# Mobile Game UI Patterns

## Overview

This document provides comprehensive UI/UX patterns for mobile game development, covering HUD layouts, touch controls, monetization interfaces, onboarding flows, accessibility requirements, and performance optimization. These patterns are optimized for touch-based mobile devices (iOS and Android) and align with modern mobile gaming standards and ethical guidelines.

---

## HUD Layouts

### 1. Corner HUD (Action Games)

**Usage**: First-person shooters (FPS), Battle Royale (BR), MOBA (Multiplayer Online Battle Arena)

**Layout**:
- **Top-Left**: Score/Kills/Timer, Team Status
- **Top-Right**: Minimap, Objectives, Quest Tracker
- **Bottom-Left**: Health Bar, Shield, Abilities/Skills
- **Bottom-Right**: Weapon Display, Ammo Count, Reload Indicator

**Safe Area**: 44pt margin from screen edges (notch/home indicator area)

**Examples**:
- PUBG Mobile
- Call of Duty Mobile
- Mobile Legends

```
┌─[Score: 1250]─────────────────[Minimap]─┐
│  [Timer: 2:45]              [Objectives] │
│                                           │
│              [GAMEPLAY AREA]              │
│                                           │
│ [HP: ████░]              [Weapon: AK-47] │
│ [Shield: ███░░]                 [30/120] │
└─[Ability Icons]─────────────[Reload Btn]─┘
```

### 2. Center HUD (Casual Games)

**Usage**: Match-3, Merge Games, Puzzle Games

**Layout**:
- **Top-Center**: Score, Level Number, Moves Remaining/Timer
- **Center**: Game Board (primary interaction area)
- **Bottom-Center**: Boosters/Power-ups, Pause/Menu Button

**Safe Area**: 20pt margin from top/bottom edges

**Examples**:
- Candy Crush Saga
- Homescapes
- Merge Dragons

```
┌──────[Level 42]──[Score: 8,500]──[Moves: 12]──────┐
│                                                    │
│              ┌─────────────────┐                  │
│              │                 │                  │
│              │   GAME BOARD    │                  │
│              │   (9x9 Grid)    │                  │
│              │                 │                  │
│              └─────────────────┘                  │
│                                                    │
│   [Booster 1] [Booster 2] [Booster 3] [Menu]     │
└────────────────────────────────────────────────────┘
```

### 3. Bottom Bar HUD (RPG)

**Usage**: RPG (Role-Playing Games), Strategy Games, MMORPGs

**Layout**:
- **Bottom Bar**: Action Bar with Skills (4-8 slots), Attack Button, Jump/Dodge
- **Top Bar**: HP/MP/Experience Bar, Buffs/Debuffs, Character Level
- **Left Side**: Minimap, Quest Tracker
- **Right Side**: Inventory Quick Access, Settings

**Safe Area**: 34pt above home indicator area (iPhone), 24pt on Android

**Examples**:
- Genshin Impact
- Raid: Shadow Legends
- Black Desert Mobile

```
┌[Lv.45][HP:████░][MP:███░░][XP:██████░░░░]─[Quest]┐
│                                                    │
│  [Minimap]         [GAMEPLAY AREA]      [Bag]     │
│  [Compass]                             [Settings] │
│                                                    │
└[Skill1][Skill2][Skill3][Skill4]──[Attack][Jump]───┘
```

---

## Touch Control Patterns

### 1. Virtual Joystick

**Best For**: Action games with continuous movement (FPS, TPS, Racing)

**Specifications**:
| Property | Value |
|----------|-------|
| Diameter | 120-160px |
| Position | Bottom-left or bottom-right corner |
| Dead Zone | 10% (center area with no input) |
| Type | Dynamic (appears on touch) or Fixed (always visible) |
| Visual | Semi-transparent circle with directional indicator |

**Accessibility**:
- Customizable size (80%-120%)
- Adjustable position
- Opacity control (30%-100%)

**Implementation Notes**:
```
// Unity Example
joystickThreshold = 0.1f; // Dead zone
maxRadius = 80f; // Max displacement from center
returnSpeed = 5f; // Spring-back speed when released
```

### 2. Gesture Controls

**Best For**: Casual games, puzzle games, card games

**Gesture Types**:
| Gesture | Action | Feedback |
|---------|--------|----------|
| **Tap** | Select, Confirm | Haptic + Scale animation |
| **Swipe** | Move, Slide, Throw | Particle trail effect |
| **Pinch** | Zoom In/Out | Scale animation |
| **Double-Tap** | Quick Action, Special Move | Flash effect + sound |
| **Long Press** | Contextual Menu, Hold Action | Radial progress indicator |

**Feedback Requirements**:
- Haptics: Light (tap), Medium (success), Heavy (special action)
- Visual: Particle effects, scale animations, color changes
- Audio: Short, non-intrusive sound effects

### 3. Touch Zones

**Best For**: Fighting games, rhythm games, competitive action games

**Layout**:
- **Left Half**: Movement controls (joystick or directional buttons)
- **Right Half**: Action buttons (attack, special moves, defend)

**Visual Options**:
- No visual overlay (invisible zones)
- Semi-transparent overlay (20%-30% opacity)
- Button outlines only

**Customization**:
- Zone size adjustment
- Zone position shift
- Button layout presets (Default, Competitive, Left-Handed)

```
┌───────────────┬───────────────┐
│               │               │
│   MOVEMENT    │    ACTIONS    │
│     ZONE      │     ZONE      │
│  (Left Half)  │ (Right Half)  │
│               │               │
└───────────────┴───────────────┘
```

---

## Monetization UI

### 1. Shop Modal

**Purpose**: In-App Purchase (IAP) storefront

**Layout**:
- 2-3 column grid layout
- "Best Value" or "Most Popular" badge on featured items
- Dual currency display (real money + virtual currency)
- Clear "Buy" CTAs with price

**Ethics Compliance (GAM-004)**:
- **Transparent Pricing**: Show exact USD/local currency amount
- **No Hidden Costs**: All taxes/fees included in displayed price
- **Clear CTAs**: "Buy $4.99" not "Get Now"
- **Refund Policy**: Link to refund information visible

**Example Structure**:
```
┌─────────────── SHOP ───────────────┐
│  [Coins] [Gems] [Bundles] [Offers] │
├────────────────────────────────────┤
│  ┌──────┐  ┌──────┐  ┌──────┐     │
│  │ 100  │  │ 500  │  │ 1000 │     │
│  │COINS │  │COINS │  │COINS │     │
│  │$0.99 │  │$4.99 │  │$9.99 │     │
│  └[Buy]─┘  └[Buy]─┘  └[Buy]─┘     │
│  ┌──────────────────┐              │
│  │  BEST VALUE ⭐   │              │
│  │   5000 COINS     │              │
│  │     $39.99       │              │
│  │   (Save 20%)     │              │
│  └────[Buy]─────────┘              │
└──[Restore Purchases]─[Refund Info]─┘
```

### 2. Rewarded Video Placement

**Purpose**: Opt-in advertisements for in-game rewards

**Trigger Points**:
| Trigger | Reward | Timing |
|---------|--------|--------|
| After fail/death | Extra life, Continue run | Immediate |
| Energy depletion | +20 energy refill | When energy hits 0 |
| Before boss fight | Temporary power-up (2x damage) | Pre-battle screen |
| Chest unlock | Skip 2-hour timer | Chest detail screen |

**Frequency Cap**: Maximum 5 rewarded videos per hour (GAM-004 compliance)

**Ethics Compliance**:
- **Always Optional**: Never block progress with forced ads
- **Clear Reward Preview**: Show exactly what player gets before watching
- **No Bait-and-Switch**: Deliver promised reward immediately after video
- **Skip After 5s**: Allow skip for technical issues (video won't load)

**UI Pattern**:
```
┌─────────── WATCH & EARN ───────────┐
│                                     │
│   🎬  Watch a short video           │
│       to get:                       │
│                                     │
│       💎 50 Gems                    │
│                                     │
│   ┌─────────┐      ┌─────────┐    │
│   │  Watch  │      │   No    │    │
│   │  Video  │      │ Thanks  │    │
│   └─────────┘      └─────────┘    │
│                                     │
│   Videos remaining today: 3/5      │
└─────────────────────────────────────┘
```

### 3. Battle Pass UI

**Purpose**: Seasonal progression system with free and premium tiers

**Layout**:
- Horizontal scrollable track showing levels 1-100
- Current level highlighted with glowing indicator
- Free tier (top row) and Premium tier (bottom row)
- XP progress bar showing progress to next level

**Progression**:
- Daily Quests: 3 tasks = 500 XP each
- Weekly Quests: 5 tasks = 2000 XP each
- Milestones every 5 levels: Epic reward chest

**Example**:
```
┌────────── SEASON 3 PASS ──────────┐
│  [Level 12/100] [XP: 1,200/2,000] │
├───────────────────────────────────┤
│ Free  → [Coins] [Chest] [Coins]   │
│ Tier    Lv.10   Lv.11   Lv.12    │
├───────────────────────────────────┤
│Premium→ [Skin]  [Gems]  [Epic]    │
│ Tier    Lv.10   Lv.11   Lv.12    │
├───────────────────────────────────┤
│  Daily Quests:                    │
│  ☑ Win 3 Matches (500 XP)         │
│  ☐ Collect 50 Coins (500 XP)      │
│  ☐ Play 5 Games (500 XP)          │
└──[Upgrade to Premium: $9.99]──────┘
```

---

## Onboarding Flow

### 1. Interactive Tutorial

**Duration by Genre**:
| Genre | Tutorial Length | Key Principle |
|-------|----------------|---------------|
| Hyper-Casual | 30s - 1min | Show, don't tell |
| Casual | 2-3min | Guided practice |
| Mid-Core | 5-8min | Progressive teaching |
| Core/Hardcore | 10-15min | Deep mechanics explanation |

**Structure**:
1. **Immediate Gameplay** (0-10s): Let player interact immediately, no intro cutscene
2. **Guided Hand** (10s-2min): Visual hand/arrow shows where to tap/swipe
3. **Celebration** (after each step): Positive reinforcement (confetti, sound, "Great!")
4. **Gradual Feature Introduction**: Introduce 1 feature per minute, not all at once

**Skip Option**:
- Allow skip after Step 1 (after core mechanic shown)
- "Skip Tutorial" button in top-right corner
- Confirm dialog: "Are you sure? You can replay tutorial from Settings"

**KPI**: Tutorial completion rate should be >70%. If lower, tutorial is too long/complex.

**Example Flow**:
```
Step 1 (10s): "Tap to jump!" → Player taps → Character jumps → "Awesome!"
Step 2 (20s): "Swipe left to move!" → Player swipes → "Perfect!"
Step 3 (30s): "Collect 3 coins!" → Player collects → "Well done! +100 XP"
Step 4 (1min): "Now try defeating this enemy!" → Combat introduced
[Skip Tutorial] button available from Step 2 onward
```

### 2. Progressive Disclosure

**Principle**: Unlock features gradually as player progresses, avoiding cognitive overload

**Feature Unlock Sequence**:
| Level/Stage | Features Unlocked | Tooltip |
|-------------|-------------------|---------|
| **Level 1** | Core gameplay loop | "Tap to play!" |
| **Level 3** | Progression system (XP, Levels) | "You leveled up! Earn XP to unlock rewards" |
| **Level 5** | Social features (Friends, Leaderboards) | "Connect with friends to compete!" |
| **Level 7** | Monetization (Shop, IAPs) | "Visit the shop for power-ups!" |
| **Level 10** | Advanced mechanics (Combos, Special Moves) | "Master combos for higher scores!" |

**Just-in-Time Tooltips**:
- Show tooltips only when feature becomes relevant
- Auto-dismiss after 5 seconds or on tap
- Never show more than 1 tooltip simultaneously

**Example**:
```
Level 1: Player plays core game loop (match tiles)
Level 3: After completing level → [NEW!] badge on XP bar
         Tooltip: "You earned 50 XP! Level up to unlock rewards"
Level 5: After 5 levels → [NEW!] badge on Friends icon
         Tooltip: "Tap here to connect with friends and compare scores!"
```

---

## Accessibility for Mobile Games

### 1. Colorblind Modes

**Requirement**: MUST implement per GAM-005 and MOB-007

**Supported Filters**:
| Mode | Deficiency | Affected Colors | Solution |
|------|-----------|-----------------|----------|
| **Deuteranopia** | Green-blind | Red/Green confusion | Use Blue/Yellow palette |
| **Protanopia** | Red-blind | Red/Green confusion | Use Blue/Orange palette |
| **Tritanopia** | Blue-blind | Blue/Yellow confusion | Use Red/Cyan palette |

**Coverage Areas**:
- Health bars (green → blue, red → orange)
- Enemy types (color-coded → add shapes/patterns)
- Team colors (Red Team/Blue Team → add team icons)
- UI highlights (green success → checkmark, red error → X icon)

**Settings Location**: Settings > Accessibility > Colorblind Mode > [Dropdown]

### 2. Touch Target Size

**Requirement**: MUST meet minimum sizes per MOB-007

**Platform Standards**:
| Platform | Minimum Size | Recommendation |
|----------|-------------|----------------|
| **iOS** | 44pt × 44pt | 48pt × 48pt |
| **Android** | 48dp × 48dp | 56dp × 56dp |

**Exception**: Competitive games may use 40pt minimum IF customizable in settings

**Spacing**: 8pt minimum gap between adjacent touch targets

**Validation**:
```
// Unity validation example
if (buttonRect.width < 44 || buttonRect.height < 44) {
    Debug.LogWarning("Touch target too small: " + buttonName);
}
```

### 3. Haptic Feedback

**Requirement**: SHOULD implement per MOB-007 (recommended, not mandatory)

**Haptic Levels**:
| Intensity | Use Case | iOS API | Android API |
|-----------|----------|---------|-------------|
| **Light** | Button tap, UI interaction | `.selection` | `VibrationEffect.EFFECT_TICK` |
| **Medium** | Success, Level Up, Reward | `.notification(.success)` | `VibrationEffect.EFFECT_CLICK` |
| **Heavy** | Damage, Death, Boss Appearance | `.impact(.heavy)` | `VibrationEffect.EFFECT_HEAVY_CLICK` |

**Settings Toggle**: Settings > Audio & Haptics > Haptic Feedback [ON/OFF]

**Implementation Note**: Always provide toggle; some users dislike haptics or have sensory sensitivities

### 4. Screen Reader Support

**Requirement**: MUST support per MOB-007

**Challenge**: Game canvas (WebGL, Unity, Unreal) not natively accessible to screen readers

**Workaround Solutions**:
- **Unity UI**: Use Unity's built-in accessibility system with labels
  ```csharp
  button.GetComponent<Accessible>().label = "Play Button";
  button.GetComponent<Accessible>().hint = "Starts new game";
  ```
- **Native UI Overlay**: Render critical UI (menus, shop) with native iOS/Android controls
- **Text-to-Speech**: Implement custom TTS for in-game events
  ```csharp
  TextToSpeech.Speak("You collected 10 coins");
  ```

**Priority Elements**: Main menu buttons, Shop items, Tutorial text, Level completion screens

---

## Performance Optimization

### 1. UI Frame Rate

**Target**: 60 FPS UI rendering even if game logic runs at 30 FPS

**Implementation**:
- **Separate UI Render Thread**: Decouple UI updates from game loop
  ```csharp
  // Unity example
  Canvas.renderMode = RenderMode.ScreenSpaceCamera;
  uiCamera.targetFrameRate = 60;
  gameCamera.targetFrameRate = 30;
  ```
- **UI-Only Updates**: Only redraw UI elements that changed, not entire canvas
- **Animation Optimization**: Use GPU-accelerated transforms (scale, rotation) over position changes

### 2. Overdraw Reduction

**Problem**: Overlapping transparent UI elements cause GPU to render same pixel multiple times

**Solution**:
| Technique | Benefit | Implementation |
|-----------|---------|----------------|
| **UI Atlases** | Single draw call for all UI | Pack sprites into texture atlas |
| **Avoid Nested Canvas** | Reduces batch count | Flatten Canvas hierarchy |
| **Disable Hidden UI** | Skip rendering off-screen elements | `SetActive(false)` on hidden panels |

**Validation Tool**: Unity Frame Debugger → Check Overdraw mode (red = high overdraw)

**Example**:
```csharp
// BAD: 4 Canvas elements = 4 draw calls
Canvas -> Background (Canvas)
       -> HUD (Canvas)
       -> Buttons (Canvas)
       -> Tooltips (Canvas)

// GOOD: 1 Canvas = 1 draw call
Canvas -> Background (Image)
       -> HUD (Image)
       -> Buttons (Image)
       -> Tooltips (Image)
```

### 3. Asset Loading

**Pattern**: Asynchronous loading for UI sprites to avoid frame drops

**Implementation**:
| Technology | Approach | Code Example |
|------------|----------|--------------|
| **Unity Addressables** | Load on-demand | `Addressables.LoadAssetAsync<Sprite>("icon_shop")` |
| **iOS On-Demand Resources** | Download from App Store | `NSBundleResourceRequest` |
| **Android Asset Bundles** | Download from CDN | `AssetBundle.LoadFromFileAsync()` |

**Loading States**:
1. Show placeholder/spinner while loading
2. Cache loaded assets in memory
3. Unload unused assets after 5 minutes idle

**Example**:
```csharp
async void LoadShopUI() {
    showLoadingSpinner();
    var handle = Addressables.LoadAssetAsync<GameObject>("ShopPanel");
    await handle.Task;
    Instantiate(handle.Result);
    hideLoadingSpinner();
}
```

---

## Validation Checklist

Use this checklist to validate mobile game UI implementation:

- [ ] **HUD Safe Area**: All UI elements respect 44pt margin from screen edges (notch/home indicator zones)
- [ ] **Touch Target Size**: All interactive elements meet minimum 44pt × 44pt (iOS) or 48dp × 48dp (Android)
- [ ] **Transparent Pricing**: Shop displays exact USD/local currency with taxes included (GAM-004 compliance)
- [ ] **Optional Ads**: Rewarded videos are opt-in, never block progress (GAM-004 compliance)
- [ ] **Tutorial Completion**: Tutorial completion rate >70% (if lower, simplify tutorial)
- [ ] **Colorblind Modes**: At least 3 filters implemented (Deuteranopia, Protanopia, Tritanopia) per GAM-005
- [ ] **Haptic Feedback**: Haptics implemented with Light/Medium/Heavy levels and Settings toggle per MOB-007
- [ ] **60 FPS UI**: UI maintains 60 FPS even during heavy gameplay (separate render thread)
- [ ] **Screen Reader Support**: Critical UI elements (menus, shop) have accessibility labels per MOB-007
- [ ] **Overdraw Check**: Use Frame Debugger to verify overdraw <2x on most screens
- [ ] **Progressive Disclosure**: Features unlock gradually (Level 1: core, Level 5: social, Level 7: monetization)
- [ ] **Async Asset Loading**: UI sprites load asynchronously with loading indicators, no frame drops

---

## References

- **GAM-004**: Ethical monetization practices (transparent pricing, optional ads)
- **GAM-005**: Colorblind accessibility requirements
- **MOB-007**: Mobile accessibility standards (touch targets, haptics, screen readers)
- **iOS Human Interface Guidelines**: [developer.apple.com/design](https://developer.apple.com/design/human-interface-guidelines/)
- **Android Material Design**: [material.io/design](https://material.io/design)

---

**Document Version**: 1.0
**Last Updated**: 2026-01-11
**Template Type**: Design Pattern Library

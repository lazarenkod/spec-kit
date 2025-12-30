# Stitch Generation Skill

> Standalone skill for generating visual mockups from wireframes via Google Stitch browser automation with **anti-detection bypass**.

## Skill Metadata

```yaml
name: stitch-generation
version: 3.0.0
trigger: "Generate visual mockups from wireframes using Google Stitch"
invocation: /speckit.stitch
aliases:
  - /speckit.mockup
  - /speckit.visual
category: design
requires:
  - playwright OR patchright (for stealth mode)
  - chromium
  - design artifacts (wireframes)
anti_detection:
  enabled: true
  modes: [cdp, stealth, turbo, assisted]
  default_mode: auto
```

## Purpose

This skill provides standalone access to Google Stitch mockup generation without requiring the full `/speckit.design` workflow. Use it when:

- You already have wireframes and want mockups
- You need to regenerate specific screens
- You want to experiment with Stitch prompts
- You're running in assisted mode (prompts only)
- **Google is blocking automation** and you need to bypass detection

## Anti-Detection Strategy (v3)

```text
┌─────────────────────────────────────────────────────────────────────┐
│  MODE PRIORITY (Auto-fallback)                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. CDP MODE (Best)                                                 │
│     Connect to user's existing Chrome via --remote-debugging-port   │
│     → Real fingerprint, real profile, zero detection                │
│                                                                     │
│  2. STEALTH MODE (Good)                                             │
│     Patchright + Humanization + Persistent Profile                  │
│     → Patched CDP, Bezier mouse, random delays                      │
│                                                                     │
│  3. TURBO MODE (Risky)                                              │
│     Standard Playwright + basic stealth args                        │
│     → Fast but may trigger detection                                │
│                                                                     │
│  4. ASSISTED MODE (Fallback)                                        │
│     Human-Assisted workflow (prepare → manual → collect)            │
│     → 100% reliable when automation blocked                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Usage

### Basic Commands

```bash
# Generate mockups for current feature's wireframes (auto mode selection)
/speckit.stitch

# Generate for all app wireframes
/speckit.stitch --all

# Specific screens only
/speckit.stitch --screens "login,dashboard,settings"

# Custom prompt for single screen
/speckit.stitch --prompt "Create a modern dashboard with dark theme"
```

### Mode Selection

```bash
# Auto mode (tries CDP → Stealth → Turbo → Assisted)
/speckit.stitch

# Explicit CDP mode (requires Chrome with debugging port)
/speckit.stitch --mode cdp

# Stealth mode (Patchright + full humanization)
/speckit.stitch --mode stealth

# Turbo mode (fast, higher detection risk)
/speckit.stitch --mode turbo

# Assisted mode (human-assisted workflow)
/speckit.stitch --mode assisted
```

### CDP Mode Setup

```bash
# Show instructions for launching Chrome with debugging port
/speckit.stitch --setup-cdp

# Then in another terminal, run the Chrome command shown
# Finally, generate mockups using CDP mode:
/speckit.stitch --mode cdp
```

### Speed Control (Humanization Intensity)

```bash
# Slow mode - maximum humanization, safest (2x delays)
/speckit.stitch --speed slow

# Normal mode - balanced humanization (default)
/speckit.stitch --speed normal

# Fast mode - minimal delays, riskier (0.5x delays)
/speckit.stitch --speed fast
```

### Assisted Mode Workflow

```bash
# Phase 1: Generate prompts only (no browser automation)
/speckit.stitch --prepare

# Phase 2: User manually generates mockups in Stitch
# Place exports in .speckit/stitch/exports/{screen-name}/

# Phase 3: Collect and organize exports
/speckit.stitch --collect
```

### Other Options

```bash
# Force re-authentication
/speckit.stitch --reauth

# Skip Figma export
/speckit.stitch --no-figma

# Skip screenshot capture
/speckit.stitch --no-screenshots

# Ignore rate limit warning
/speckit.stitch --force
```

## Prerequisites Check

```text
BEFORE execution:

  1. CHECK Playwright installation:
     npm ls playwright 2>/dev/null
     IF not found:
       PROMPT "Playwright not installed. Install now? [Y/n]"
       IF yes: npm install playwright

  2. CHECK Chromium browser:
     npx playwright install --dry-run chromium
     IF not installed:
       LOG "Installing Chromium..."
       npx playwright install chromium

  3. CHECK design artifacts exist:
     SCAN for wireframes:
       - specs/app-design/**/*.md
       - specs/*/design.md
       - .preview/wireframes/*.html

     IF no wireframes found:
       ERROR "No wireframes found. Create design specs first with /speckit.design"
       EXIT

  4. CHECK Google Stitch session:
     IF .speckit/stitch/session/ exists:
       LOG "Found existing session"
     ELSE:
       LOG "No session found. Will need to authenticate."
```

## Workflow

```text
1. LOAD automation modules:
   READ templates/shared/stitch-integration.md
   READ templates/shared/stitch-anti-detection.md  # NEW: humanization & bypass
   READ templates/shared/stitch-prompts.md
   READ templates/shared/stitch-selectors.md

2. HANDLE special commands:
   IF --setup-cdp:
     PRINT CDP setup instructions
     EXIT
   IF --prepare:
     GENERATE prompts only (assisted mode phase 1)
     EXIT
   IF --collect:
     COLLECT manual exports (assisted mode phase 3)
     EXIT

3. SELECT automation mode:
   IF --mode specified:
     MODE = specified_mode
   ELSE:
     MODE = auto_select()  # CDP → Stealth → Turbo → Assisted

4. DETERMINE scope:
   IF --screens specified:
     WIREFRAMES = filter_by_names(specified_screens)
   ELIF --all:
     WIREFRAMES = all_discovered_wireframes()
   ELIF --prompt specified:
     WIREFRAMES = [custom_prompt_wireframe]
   ELSE:
     WIREFRAMES = current_feature_wireframes()

5. EXECUTE generation pipeline:
   CALL stitch_main(WIREFRAMES, {
     mode: MODE,
     speed: --speed OR 'normal',
     ...OPTIONS
   })

6. HANDLE detection fallback:
   IF CAPTCHA detected twice:
     SWITCH to assisted mode for remaining screens

7. OUTPUT results:
   - Generated mockups in .preview/stitch-mockups/
   - Gallery at .preview/stitch-mockups/index.html
   - Mode statistics in .speckit/stitch/usage.json
   - Report summary with mode used
```

## Arguments

### Mode Selection

| Argument | Description | Default |
|----------|-------------|---------|
| `--mode` | Automation mode: `cdp`, `stealth`, `turbo`, `assisted` | `auto` (tries all) |
| `--setup-cdp` | Print Chrome launch command for CDP mode | - |
| `--speed` | Humanization intensity: `slow`, `normal`, `fast` | `normal` |

### Scope Selection

| Argument | Description | Default |
|----------|-------------|---------|
| `--all` | Generate for all wireframes in app-design | Current feature only |
| `--screens` | Comma-separated screen names | All in scope |
| `--prompt` | Custom prompt for single generation | From wireframe |

### Assisted Mode

| Argument | Description | Default |
|----------|-------------|---------|
| `--prepare` | Generate prompts only, no automation | - |
| `--collect` | Collect manual exports from `.speckit/stitch/exports/` | - |

### Export Options

| Argument | Description | Default |
|----------|-------------|---------|
| `--format` | Export format: `html`, `tailwind`, `both` | `both` |
| `--no-figma` | Skip Figma clipboard export | Include Figma |
| `--no-screenshots` | Skip screenshot capture | Include screenshots |

### Other Options

| Argument | Description | Default |
|----------|-------------|---------|
| `--reauth` | Force re-authentication | Use existing session |
| `--force` | Ignore rate limit warnings | Respect rate limit |

## Custom Prompt Mode

When using `--prompt`, you can specify a custom Stitch prompt directly:

```bash
/speckit.stitch --prompt "Create a modern SaaS dashboard with:
- Dark theme with purple accent
- Sidebar navigation
- Main area with 4 metric cards
- Activity feed below
- Clean, minimal design"
```

This will:
1. Skip wireframe discovery
2. Use your prompt directly with Stitch
3. Save output to `.preview/stitch-mockups/custom/`

## Interactive Mode

When run without arguments, the skill enters interactive mode:

```text
🎨 Stitch Mockup Generation (v3 - Anti-Detection)

Mode: AUTO (will try CDP → Stealth → Turbo → Assisted)
Speed: NORMAL

Found {N} wireframes:
  1. login (specs/app-design/foundations/auth-design.md)
  2. dashboard (specs/app-design/waves/wave-1/EPIC-001.F01-design.md)
  3. settings (specs/app-design/waves/wave-2/EPIC-002.F01-design.md)

Options:
  [A] Generate all ({N} screens)
  [S] Select specific screens
  [P] Enter custom prompt
  [M] Mode selection (cdp/stealth/turbo/assisted)
  [C] CDP setup instructions
  [Q] Quit

Choice: _
```

## Output Structure

```text
.preview/stitch-mockups/
├── {feature}/
│   └── {screen-name}/
│       ├── code.html               # Generated HTML
│       ├── code.css                # Extracted/generated CSS
│       ├── screenshot-desktop.png  # Desktop viewport
│       ├── screenshot-mobile.png   # Mobile viewport
│       ├── figma-clipboard.json    # Figma paste data
│       └── prompt.txt              # Prompt used
├── manual/                         # Manual exports (assisted mode)
│   └── {screen-name}/
├── index.html                      # Master gallery view
└── mockup-report.md                # Generation report

.speckit/stitch/
├── session/                    # Persistent browser profile (stealth mode)
├── chrome-profile/             # User data for CDP mode
├── exports/                    # Manual exports staging (assisted mode)
├── prompts/                    # Generated prompts (assisted mode)
├── usage.json                  # Rate limit + mode statistics
└── fingerprint.json            # Randomized browser fingerprint
```

### Mode Statistics in usage.json

```json
{
  "month": "2025-01",
  "generations": {
    "used": 45,
    "limit": 350,
    "last": "2025-01-15T10:30:00Z"
  },
  "mode_stats": {
    "cdp": { "attempts": 20, "successes": 20, "failures": 0, "captcha_triggered": 0 },
    "stealth": { "attempts": 25, "successes": 23, "failures": 2, "captcha_triggered": 1 },
    "turbo": { "attempts": 5, "successes": 3, "failures": 2, "captcha_triggered": 2 },
    "assisted": { "attempts": 2, "successes": 2, "failures": 0, "captcha_triggered": 0 }
  }
}
```

## Rate Limit Awareness

Google Stitch has usage limits:
- **Standard mode**: 350 generations/month
- **Experimental mode**: 50 generations/month

The skill tracks usage in `.speckit/stitch/usage.json`:

```text
BEFORE each generation:
  CHECK usage.json
  IF standard.used >= 350:
    WARN "Rate limit reached. Switching to manual mode."
    SWITCH to manual mode

  IF approaching limit (>300 used):
    WARN "Approaching rate limit ({used}/350). {remaining} generations remaining."
```

## Error Recovery

| Error | Recovery Action |
|-------|-----------------|
| Session expired | Auto-trigger re-authentication |
| Rate limit reached | Switch to assisted mode |
| CAPTCHA detected (1st) | Pause 60s for user to solve |
| CAPTCHA detected (2nd) | Switch to assisted mode for remaining |
| CDP connection failed | Fall back to stealth mode |
| Stealth mode blocked | Fall back to turbo mode |
| Turbo mode blocked | Fall back to assisted mode |
| Generation timeout | Retry once, then skip |
| Export failed | Screenshot fallback |
| Network error | Retry with exponential backoff |

## Integration with /speckit.design

This skill is automatically invoked when running:

```bash
/speckit.design --mockup
```

The design command provides additional context:
- Design system tokens (colors, fonts)
- Component specifications
- Persona preferences
- Wave-based prioritization

For full context-aware generation, prefer `/speckit.design --mockup`.

## Assisted Mode Guide

When using `--prepare` or when automation is blocked, prompts are saved for manual generation:

```text
OUTPUT .speckit/stitch/prompts/manual-generation-guide.md:

# Assisted Mode - Manual Mockup Generation Guide

## Overview

Automation was blocked or you chose assisted mode.
Complete the generation manually using the prompts below.

## Steps

1. Open https://stitch.withgoogle.com
2. Sign in with Google (use the same account as always)
3. For each screen below:
   a. Copy the prompt
   b. Paste into Stitch
   c. Generate the mockup
   d. Export: Code → Copy HTML
   e. Save to: .speckit/stitch/exports/{screen-name}/code.html
   f. Take screenshot if needed

4. When done, run: /speckit.stitch --collect

## Screens ({N} total)

### 1. {screen_name}

**Feature**: {feature_name}
**Prompt**:
```
{generated_prompt}
```

**Export to**: .speckit/stitch/exports/{screen_name}/
  - code.html (required)
  - mockup.png (optional)
  - figma.json (optional)

---

### 2. {next_screen_name}
...
```

### Collect Phase

After manual generation, collect and organize exports:

```bash
/speckit.stitch --collect
```

This will:
1. Scan `.speckit/stitch/exports/` for exported files
2. Move to `.preview/stitch-mockups/manual/`
3. Generate gallery and report

## Quality Validation

After generation, the skill validates outputs:

```text
FOR each generated mockup:
  CHECK:
    - [ ] HTML file exists and non-empty
    - [ ] Screenshot captured successfully
    - [ ] Figma clipboard data valid JSON

  IF checks pass:
    STATUS = "success"
  ELIF partial:
    STATUS = "partial"
    LOG warnings
  ELSE:
    STATUS = "failed"
    ADD to retry list
```

## Completion Report

```text
┌─────────────────────────────────────────────────────────────────────┐
│  🎨 /speckit.stitch Complete (v3)                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Mode: {mode.toUpperCase()}                                         │
│  Speed: {speed}                                                     │
│                                                                     │
│  Screens: {success_count}/{total}                                   │
│  Success: {success_count}  Partial: {partial}  Failed: {failed}     │
│                                                                     │
│  Exports:                                                           │
│    HTML/CSS: {html_count}                                           │
│    Screenshots: {screenshot_count}                                  │
│    Figma: {figma_count}                                             │
│                                                                     │
│  Rate Limit: {used}/{limit} this month                              │
│                                                                     │
│  📁 Output: .preview/stitch-mockups/                                │
│  📊 Gallery: .preview/stitch-mockups/index.html                     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  Next Steps:                                                        │
│   → open .preview/stitch-mockups/index.html                         │
│   → /speckit.preview (serve gallery)                                │
│   → /speckit.stitch --screens "{failed}" (retry failures)           │
└─────────────────────────────────────────────────────────────────────┘
```

### Fallback Report (when CAPTCHA triggered)

```text
┌─────────────────────────────────────────────────────────────────────┐
│  ⚠️  AUTOMATION BLOCKED - Switched to Assisted Mode                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Mode: {mode} → ASSISTED (fallback)                                 │
│  Reason: CAPTCHA detected {captcha_count} times                     │
│                                                                     │
│  Completed: {completed}/{total} screens                             │
│  Remaining: {remaining} screens                                     │
│                                                                     │
│  📝 Manual prompts saved to:                                        │
│     .speckit/stitch/prompts/manual-generation-guide.md              │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  Next Steps:                                                        │
│   1. Open manual-generation-guide.md                                │
│   2. Generate remaining {remaining} screens in Stitch               │
│   3. Export to .speckit/stitch/exports/{screen}/                    │
│   4. Run: /speckit.stitch --collect                                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Dependencies

```yaml
npm_packages:
  # Choose one based on mode:
  - playwright: "^1.40.0"           # For turbo/cdp mode
  - patchright: "^1.40.0"           # For stealth mode (recommended)

browser:
  - chromium (via Playwright/Patchright)
  - Google Chrome (for CDP mode - user's installed browser)

files:
  - templates/shared/stitch-integration.md
  - templates/shared/stitch-anti-detection.md  # NEW: humanization functions
  - templates/shared/stitch-prompts.md
  - templates/shared/stitch-selectors.md

external:
  - Google Stitch (stitch.withgoogle.com)
  - Google account for authentication
```

## Mode Comparison

| Aspect | CDP | Stealth | Turbo | Assisted |
|--------|-----|---------|-------|----------|
| Detection Risk | Minimal | Low | Medium-High | Zero |
| Setup Complexity | Medium | Low | None | None |
| Speed | Fast | Medium | Fastest | Slowest (manual) |
| Reliability | High | Medium | Low | 100% |
| Requires User Action | Chrome launch | None | None | Full workflow |
| Best For | Production | Default | Dev/testing | Fallback |

## Troubleshooting

### Browser not launching

```bash
# Reinstall Chromium
npx playwright install chromium --force
```

### Session issues

```bash
# Clear session and re-authenticate
rm -rf .speckit/stitch/session/
/speckit.stitch --reauth
```

### Rate limit errors

```bash
# Check current usage
cat .speckit/stitch/usage.json

# Reset for new month (automatic, or manual)
# Usage resets on 1st of each month
```

### Selector failures

```text
IF selectors fail:
  1. Stitch UI may have changed
  2. Check templates/shared/stitch-selectors.md version
  3. Update selectors if needed
  4. Fall back to manual mode
```

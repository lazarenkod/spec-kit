# Stitch Generation Skill

> Standalone skill for generating visual mockups from wireframes via Google Stitch browser automation.

## Skill Metadata

```yaml
name: stitch-generation
trigger: "Generate visual mockups from wireframes using Google Stitch"
invocation: /speckit.stitch
aliases:
  - /speckit.mockup
  - /speckit.visual
category: design
requires:
  - playwright
  - chromium
  - design artifacts (wireframes)
```

## Purpose

This skill provides standalone access to Google Stitch mockup generation without requiring the full `/speckit.design` workflow. Use it when:

- You already have wireframes and want mockups
- You need to regenerate specific screens
- You want to experiment with Stitch prompts
- You're running in manual mode (prompts only)

## Usage

```bash
# Generate mockups for current feature's wireframes
/speckit.stitch

# Generate for all app wireframes
/speckit.stitch --all

# Specific screens only
/speckit.stitch --screens "login,dashboard,settings"

# Manual mode (generate prompts, no automation)
/speckit.stitch --manual

# Re-authenticate with Google
/speckit.stitch --reauth

# Custom prompt for single screen
/speckit.stitch --prompt "Create a modern dashboard with dark theme"
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
   READ templates/shared/stitch-prompts.md
   READ templates/shared/stitch-selectors.md

2. DETERMINE scope:
   IF --screens specified:
     WIREFRAMES = filter_by_names(specified_screens)
   ELIF --all:
     WIREFRAMES = all_discovered_wireframes()
   ELIF --prompt specified:
     WIREFRAMES = [custom_prompt_wireframe]
   ELSE:
     WIREFRAMES = current_feature_wireframes()

3. EXECUTE generation pipeline:
   CALL stitch_main(WIREFRAMES, OPTIONS)

4. OUTPUT results:
   - Generated mockups in .preview/stitch-mockups/
   - Gallery at .preview/stitch-mockups/index.html
   - Report summary
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--all` | Generate for all wireframes in app-design | Current feature only |
| `--screens` | Comma-separated screen names | All in scope |
| `--manual` | Generate prompts only, no automation | Auto mode |
| `--reauth` | Force re-authentication | Use existing session |
| `--prompt` | Custom prompt for single generation | From wireframe |
| `--format` | Export format: `html`, `tailwind`, `both` | `both` |
| `--no-figma` | Skip Figma clipboard export | Include Figma |
| `--no-screenshots` | Skip screenshot capture | Include screenshots |

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
🎨 Stitch Mockup Generation

Found {N} wireframes:
  1. login (specs/app-design/foundations/auth-design.md)
  2. dashboard (specs/app-design/waves/wave-1/EPIC-001.F01-design.md)
  3. settings (specs/app-design/waves/wave-2/EPIC-002.F01-design.md)

Options:
  [A] Generate all ({N} screens)
  [S] Select specific screens
  [P] Enter custom prompt
  [M] Manual mode (prompts only)
  [Q] Quit

Choice: _
```

## Output Structure

```text
.preview/stitch-mockups/
├── {screen-name}/
│   ├── stitch-output.html      # Generated HTML
│   ├── stitch-output.css       # Extracted/generated CSS
│   ├── screenshot-desktop.png  # 1440px width
│   ├── screenshot-mobile.png   # 375px width
│   ├── figma-clipboard.json    # Figma paste data
│   └── prompt.txt              # Prompt used
├── index.html                  # Gallery view
└── report.md                   # Generation report

.speckit/stitch/
├── session/                    # Browser session data
├── usage.json                  # Rate limit tracking
└── prompts-cache/              # Cached prompts
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
| Rate limit reached | Switch to manual mode |
| CAPTCHA detected | Pause and prompt user |
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

## Manual Mode Guide

When using `--manual` or when automation fails, prompts are saved for manual use:

```text
OUTPUT .speckit/stitch/manual-generation-guide.md:

# Manual Mockup Generation Guide

## Steps

1. Open https://stitch.withgoogle.com
2. Sign in with Google
3. For each screen, paste prompt and export

## Screens

### {screen_name}
**Prompt**:
{generated_prompt}

**Export to**: .preview/stitch-mockups/{screen}/
```

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
│  🎨 /speckit.stitch Complete                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Screens: {processed}/{total}                                       │
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

## Dependencies

```yaml
npm_packages:
  - playwright: "^1.40.0"

browser:
  - chromium (via Playwright)

files:
  - templates/shared/stitch-integration.md
  - templates/shared/stitch-prompts.md
  - templates/shared/stitch-selectors.md

external:
  - Google Stitch (stitch.withgoogle.com)
  - Google account for authentication
```

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

# Google Stitch Integration Module

> Browser automation module for generating high-fidelity visual mockups from wireframes using Google Stitch (stitch.withgoogle.com).

## Module Metadata

```yaml
version: 3.1.0
last_updated: 2026-01-06
status: active
anti_detection: enabled
modes: [cdp, stealth, turbo, assisted]
enhancements: [robust_selectors, interactive_fallback, clipboard_input, visibility_checks]
```

## Overview

Google Stitch is an AI-powered design tool from Google Labs that generates UI designs from text prompts using Gemini 2.5 Pro/Flash. Since Stitch has no public API, this module uses Playwright browser automation with **multi-mode anti-detection** to:

1. Navigate to stitch.withgoogle.com
2. Authenticate via Google OAuth (persistent session)
3. Generate UI mockups from wireframe-derived prompts
4. Export results in multiple formats (HTML, PNG, Figma)

### Anti-Detection Strategy (v3)

Google detects browser automation through multiple vectors. This module implements a **hybrid multi-mode strategy** with automatic fallback:

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
│     Standard Playwright + enhanced stealth args                     │
│     → Fast but may trigger detection                                │
│                                                                     │
│  4. ASSISTED MODE (Fallback)                                        │
│     Human-Assisted workflow (prepare → manual → collect)            │
│     → 100% reliable when automation blocked                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Robustness Enhancements (v3.1.0)

This version includes proven patterns from production Stitch automation:

**1. Robust Element Finding with Visibility Checks**
- Try primary selector + all fallbacks with 5s timeouts each (not 10s total)
- Check `isVisible()` before using any element
- Log which selector worked for debugging
- Continue to next fallback if element found but hidden

**2. Interactive Fallback Mode**
- When all selectors fail, ask user to click the element
- Use `:focus` selector to capture user's choice
- Beautiful console UI guides user through the process
- Enable with `--allow-interactive` flag

**3. Clipboard-based Input (10x faster)**
- Try clipboard paste first (instant vs ~140ms per char)
- Automatic OS detection (Meta+V for Mac, Ctrl+V for Windows/Linux)
- Fallback to typing if clipboard fails
- Override with `--prefer-typing` if needed

**4. Better Error Recovery**
- Session re-authentication detection
- Platform-aware keyboard shortcuts
- Detailed logging of element finding process
- Graceful degradation from fast to slow methods

Example usage with new features:
```bash
# Standard mode (clipboard + auto-fallbacks)
/speckit.design --mockup

# Interactive mode (asks user to click elements if automation fails)
/speckit.design --mockup --allow-interactive

# Force typing mode (more human-like, useful in CDP mode)
/speckit.design --mockup --prefer-typing
```

## Prerequisites

### Required Dependencies

```bash
# Check Playwright installation
npm ls playwright || npm install playwright

# (Optional) Install Patchright for enhanced stealth mode
npm install patchright

# Install browser if needed
npx playwright install chromium
```

### CDP Mode Setup (Recommended)

For best anti-detection results, connect to your existing Chrome browser:

```bash
# Launch Chrome with debugging port (do this once)
# macOS:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.speckit/chrome-profile"

# Windows:
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="%USERPROFILE%\.speckit\chrome-profile"

# Linux:
google-chrome --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.speckit/chrome-profile"
```

Then sign in to Google manually and run `/speckit.stitch --mode cdp`.

### Directory Structure

```text
.speckit/stitch/
├── session/                    # Playwright persistent context (browser profile)
│   └── Default/                # Chromium profile data
├── usage.json                  # Rate limit tracking
├── mode-history.json           # Mode success/failure tracking
├── fingerprint.json            # Cached browser fingerprint
└── prompts-cache/              # Saved prompts for retry/manual mode
    ├── {feature}/
    │   └── {screen-name}.txt

.preview/stitch-mockups/
├── {feature}/
│   ├── {screen-name}/
│   │   ├── stitch-output.html
│   │   ├── stitch-output.css
│   │   ├── screenshot-desktop.png
│   │   ├── screenshot-mobile.png
│   │   ├── figma-clipboard.json
│   │   └── prompt.txt
│   └── index.html              # Feature gallery
└── index.html                  # Master gallery
```

### Module Imports

```text
# Load anti-detection functions from shared module
IMPORT * FROM templates/shared/stitch-anti-detection.md:
  - gaussian_random, random_int, random_float, random_choice
  - ease_in_out_cubic, lerp, bezier_curve, fitts_time, distance
  - humanize_typing, move_and_click, random_wait
  - scroll_to_element, smooth_viewport_resize
  - generate_fingerprint, STEALTH_ARGS, build_stealth_context_options
  - connect_via_cdp, select_stitch_mode, track_mode_result
  - detect_captcha, handle_captcha, detect_rate_limit, handle_rate_limit
  - validate_session, reset_session

# Load selectors from versioned file
IMPORT SELECTORS FROM templates/shared/stitch-selectors.md

# Load output processor functions for enhanced exports
IMPORT * FROM templates/shared/stitch-output-processor.md:
  - stitch_export_screenshots_enhanced
  - convert_screenshots_to_webp
  - generate_interactive_preview
  - GENERATE_INTERACTIVE_JS
  - INTERACTIVE_CSS
  - OUTPUT_PROCESSOR_CONFIG

# Load parallel engine for concurrent generation
IMPORT * FROM templates/shared/stitch-parallel-engine.md:
  - stitch_generate_mockups_parallel
  - create_browser_pool
  - create_progress_tracker
  - PARALLEL_ENGINE_CONFIG

# Load cache manager for incremental generation and session reuse
IMPORT * FROM templates/shared/stitch-cache-manager.md:
  - cache_prompt
  - get_cached_prompt
  - detect_incremental_screens
  - hash_design_context
  - save_browser_session
  - load_browser_session
  - restore_browser_session
  - clear_cached_session
  - CACHE_MANAGER_CONFIG
```

---

## Phase 0: Preflight Check & Mode Selection

```text
FUNCTION stitch_preflight_check(options):

  1. CHECK Playwright installation:
     RUN: npm ls playwright --json
     IF not found:
       LOG "Installing Playwright..."
       RUN: npm install playwright
       IF fails: ERROR "Failed to install Playwright"

  2. CHECK browser availability:
     RUN: npx playwright install chromium --dry-run
     IF not installed:
       LOG "Installing Chromium browser..."
       RUN: npx playwright install chromium
       IF fails: ERROR "Failed to install Chromium"

  3. CHECK session directory:
     IF NOT EXISTS .speckit/stitch/session/:
       CREATE directory
       SET needs_auth = true
     ELSE:
       SET needs_auth = false

  4. CHECK rate limits:
     IF EXISTS .speckit/stitch/usage.json:
       LOAD usage data
       current_month = DATE.format("YYYY-MM")

       IF usage.month != current_month:
         RESET usage counters
         LOG "New month - rate limits reset"

       IF usage.standard.used >= 350:
         WARN "Standard mode rate limit reached (350/month)"
         SUGGEST "Use --mode assisted or wait for next month"

       IF usage.standard.used >= 300:
         WARN "Approaching rate limit: {used}/350 generations this month"

  5. SELECT automation mode:
     mode_result = stitch_select_mode(options)

     LOG """
     ┌─────────────────────────────────────────────┐
     │  Mode: {mode_result.mode.toUpperCase()}     │
     │  {mode_description(mode_result.mode)}       │
     └─────────────────────────────────────────────┘
     """

  6. RETURN {
       playwright_ready: true,
       browser_ready: true,
       needs_auth: needs_auth,
       rate_limit_ok: usage.standard.used < 350,
       mode: mode_result
     }


FUNCTION stitch_select_mode(options):
  """
  Select best available automation mode.
  Priority: CDP → Stealth → Turbo → Assisted
  """

  requested_mode = options.mode OR 'auto'

  # User explicitly requested a mode
  IF requested_mode !== 'auto':
    LOG "Using explicitly requested mode: {requested_mode}"
    RETURN { mode: requested_mode }

  # Auto-selection: try modes in priority order

  # 1. Try CDP connection (best - uses real browser)
  IF NOT options.skip_cdp:
    TRY:
      cdp_result = await connect_via_cdp('http://localhost:9222')
      IF cdp_result:
        LOG "✅ CDP connection successful - using real browser"
        RETURN { mode: 'cdp', ...cdp_result }
    CATCH:
      LOG "ℹ️ CDP not available (Chrome not running with --remote-debugging-port)"

  # 2. Check if Patchright is available (stealth mode)
  TRY:
    patchright = require('patchright')
    LOG "✅ Patchright available - using stealth mode"
    RETURN { mode: 'stealth', launcher: patchright }
  CATCH:
    LOG "ℹ️ Patchright not installed - using standard Playwright"

  # 3. Fall back to standard Playwright (turbo mode)
  playwright = require('playwright')
  LOG "⚠️ Using turbo mode (higher detection risk)"
  RETURN { mode: 'turbo', launcher: playwright }


FUNCTION mode_description(mode):
  descriptions = {
    cdp: "Connected to your Chrome browser - zero detection risk",
    stealth: "Patchright + humanization - low detection risk",
    turbo: "Standard Playwright - faster but higher detection risk",
    assisted: "Human-assisted workflow - prompts only, no automation"
  }
  RETURN descriptions[mode] OR "Unknown mode"
```

---

## Phase 1: Authentication

### Multi-Mode Browser Context Creation

```text
FUNCTION stitch_create_browser_context(mode_result, options):
  """
  Create browser context based on selected mode.
  Each mode has different anti-detection characteristics.
  """

  # Generate or load fingerprint for consistency
  fingerprint = stitch_get_or_create_fingerprint()

  SWITCH mode_result.mode:

    CASE 'cdp':
      # Already connected via CDP in mode selection
      browser = mode_result.browser
      context = mode_result.context OR browser.contexts()[0]

      IF NOT context:
        context = await browser.newContext({
          viewport: fingerprint.viewport
        })

      LOG "Using CDP-connected browser context"
      RETURN { context, browser, mode: 'cdp' }

    CASE 'stealth':
      # Use Patchright with full stealth configuration
      patchright = mode_result.launcher

      context_options = build_stealth_context_options(fingerprint)

      context = await patchright.chromium.launchPersistentContext(
        ".speckit/stitch/session/",
        context_options
      )

      LOG "Launched stealth browser with Patchright"
      RETURN { context, mode: 'stealth' }

    CASE 'turbo':
      # Standard Playwright with enhanced stealth args
      playwright = mode_result.launcher

      context = await playwright.chromium.launchPersistentContext(
        ".speckit/stitch/session/",
        {
          headless: false,
          viewport: fingerprint.viewport,
          timezoneId: fingerprint.timezoneId,
          locale: fingerprint.locale,
          args: STEALTH_ARGS,
          ignoreDefaultArgs: ['--enable-automation']
        }
      )

      LOG "Launched turbo browser (standard Playwright + stealth args)"
      RETURN { context, mode: 'turbo' }

    CASE 'assisted':
      # No browser needed for assisted mode
      LOG "Assisted mode - no browser automation"
      RETURN { context: null, mode: 'assisted' }

    DEFAULT:
      ERROR "Unknown mode: {mode_result.mode}"


FUNCTION stitch_get_or_create_fingerprint():
  """
  Get cached fingerprint or generate new one.
  Fingerprint is cached per session for consistency.
  """

  fingerprint_file = ".speckit/stitch/fingerprint.json"

  IF EXISTS fingerprint_file:
    fingerprint = LOAD fingerprint_file
    # Check if fingerprint is recent (< 7 days)
    IF fingerprint.created_at > Date.now() - 7 * 24 * 60 * 60 * 1000:
      LOG "Using cached fingerprint"
      RETURN fingerprint

  # Generate new fingerprint
  fingerprint = generate_fingerprint()
  fingerprint.created_at = Date.now()

  SAVE fingerprint TO fingerprint_file
  LOG "Generated new browser fingerprint"

  RETURN fingerprint
```

### Authentication Flow

```text
FUNCTION stitch_authenticate(context):

  page = context.pages[0] OR context.newPage()

  1. NAVIGATE to Stitch:
     await page.goto("https://stitch.withgoogle.com")
     await page.waitForLoadState("networkidle")

  2. CHECK if already authenticated:
     # Look for workspace indicators
     workspace_selector = '.workspace, [data-workspace], main[role="main"]'
     login_selector = 'button:has-text("Sign in"), [data-action="sign-in"]'

     IF await page.locator(workspace_selector).count() > 0:
       LOG "Already authenticated"
       RETURN { authenticated: true, page: page }

     IF await page.locator(login_selector).count() > 0:
       LOG "Authentication required"

       3. PROMPT user for manual sign-in:
          DISPLAY """
          ┌─────────────────────────────────────────────────────────────┐
          │  Google Stitch Authentication Required                       │
          ├─────────────────────────────────────────────────────────────┤
          │                                                             │
          │  A browser window has opened to stitch.withgoogle.com       │
          │                                                             │
          │  Please sign in with your Google account.                   │
          │  The session will be saved for future use.                  │
          │                                                             │
          │  Waiting for authentication...                              │
          └─────────────────────────────────────────────────────────────┘
          """

       4. WAIT for successful auth:
          await page.waitForSelector(workspace_selector, {
            timeout: 300000  # 5 minutes for user to complete OAuth
          })

          LOG "Authentication successful!"
          RETURN { authenticated: true, page: page }

  ERROR "Could not detect Stitch interface state"
```

### Re-authentication

```text
FUNCTION stitch_reauth(context):
  # Force re-authentication (--reauth flag)

  1. CLEAR session:
     DELETE .speckit/stitch/session/*

  2. CREATE fresh context:
     context = stitch_create_browser_context()

  3. RUN auth flow:
     RETURN stitch_authenticate(context)
```

---

## Phase 2: Wireframe Discovery

### Scan Design Artifacts

```text
FUNCTION stitch_discover_wireframes(scope):

  wireframes = []

  # Define scan paths based on scope
  IF scope == "feature":
    paths = [
      "specs/{current_feature}/design.md"
    ]
  ELIF scope == "app":
    paths = [
      "specs/app-design/foundations/*.md",
      "specs/app-design/waves/**/*-design.md",
      "specs/app-design/journeys/*.md"
    ]
  ELIF scope.screens:
    # Specific screens from --screens flag
    paths = resolve_screen_paths(scope.screens)

  FOR each path IN paths:
    FOR each file IN glob(path):
      content = READ file

      # Extract ASCII wireframe blocks
      wireframe_blocks = REGEX.findAll(
        content,
        /```(?:text|ascii)?\n([\s\S]*?┌[\s\S]*?┘[\s\S]*?)```/g
      )

      FOR each block IN wireframe_blocks:
        wireframe = {
          source_file: file,
          screen_name: extract_screen_name(file, block),
          ascii_content: block,
          components: extract_components(block),
          context: extract_surrounding_context(content, block)
        }
        wireframes.push(wireframe)

  RETURN wireframes
```

### Extract Screen Name

```text
FUNCTION extract_screen_name(file, block):

  # Try to find screen name from context
  # 1. Look for "### Screen: {name}" header before block
  # 2. Look for "## {name}" section header
  # 3. Derive from filename

  IF preceding_header MATCHES /###?\s+(?:Screen:?\s+)?(.+)/i:
    RETURN slugify(match[1])

  RETURN slugify(basename(file, ".md"))
```

### Extract Components

```text
FUNCTION extract_components(ascii_block):

  components = []

  # Common patterns in ASCII wireframes
  patterns = {
    button: /\[([^\]]+)\]/g,           # [Button Text]
    input: /\[_+\]|\[Input\]/gi,       # [____] or [Input]
    header: /^[│├┤].*Header/mi,
    sidebar: /Sidebar|Nav/i,
    card: /┌─+┐[\s\S]*?└─+┘/g,
    table: /\|.*\|.*\|/g,
    icon: /\([●○◆◇★☆]\)/g
  }

  FOR each pattern_name, regex IN patterns:
    matches = ascii_block.matchAll(regex)
    FOR each match IN matches:
      components.push({
        type: pattern_name,
        content: match[0],
        position: match.index
      })

  RETURN components
```

---

## Phase 3: Prompt Generation

### Load Design Context

```text
FUNCTION stitch_load_design_context():

  context = {}

  # Load design system tokens
  IF EXISTS specs/app-design/design-system.md:
    design_system = PARSE specs/app-design/design-system.md
    context.colors = design_system.colors
    context.typography = design_system.typography
    context.style = design_system.style_keywords

  ELIF EXISTS memory/constitution.md:
    constitution = PARSE memory/constitution.md
    context.colors = constitution.design_system.colors
    context.brand_name = constitution.project_name

  # Load persona context
  IF EXISTS specs/concept.md:
    concept = PARSE specs/concept.md
    context.personas = concept.personas
    context.primary_persona = concept.personas[0]

  RETURN context
```

### Generate Stitch Prompt

```text
FUNCTION stitch_generate_prompt(wireframe, design_context):

  # Load prompt template
  READ templates/shared/stitch-prompts.md

  # Analyze wireframe structure
  layout = analyze_layout(wireframe.ascii_content)
  components = wireframe.components

  # Build prompt from template
  prompt = TEMPLATE("""
    Create a {screen_type} screen for {app_name}.

    ## Layout
    {layout_description}

    ## Components
    {component_list}

    ## Style
    - Primary color: {primary_color}
    - Font: {font_family}
    - Theme: {theme}
    - Border radius: {border_radius}
    - Style: {style_keywords}

    ## Content
    {content_description}

    ## Additional Context
    {persona_context}

    Mood: {mood}
  """, {
    screen_type: detect_screen_type(wireframe),
    app_name: design_context.brand_name OR "Application",
    layout_description: layout.description,
    component_list: format_components(components),
    primary_color: design_context.colors?.primary OR "#3B82F6",
    font_family: design_context.typography?.font_family OR "Inter, system-ui",
    theme: design_context.theme OR "light",
    border_radius: design_context.border_radius OR "8px",
    style_keywords: design_context.style?.join(", ") OR "modern, clean",
    content_description: wireframe.context,
    persona_context: format_persona_context(design_context.primary_persona),
    mood: detect_mood(design_context.style)
  })

  # Save prompt for retry/manual mode
  WRITE prompt TO .speckit/stitch/prompts-cache/{feature}/{screen}.txt

  RETURN prompt
```

### Analyze Layout

```text
FUNCTION analyze_layout(ascii_content):

  layout = {
    has_header: /Header|Nav.*bar/i.test(ascii_content),
    has_sidebar: /Sidebar|Side.*nav/i.test(ascii_content),
    has_footer: /Footer|Action.*bar/i.test(ascii_content),
    columns: detect_columns(ascii_content),
    sections: detect_sections(ascii_content)
  }

  # Generate description
  parts = []

  IF layout.has_header:
    parts.push("Header/navigation bar at top")

  IF layout.has_sidebar:
    parts.push("Sidebar navigation on left")

  IF layout.columns > 1:
    parts.push("{columns}-column layout in main area".format(layout.columns))

  IF layout.has_footer:
    parts.push("Footer/action bar at bottom")

  layout.description = parts.join(", ") OR "Single column layout"

  RETURN layout
```

---

## Phase 4: Generation Pipeline

### DOM Selectors

```text
# Load selectors from versioned file
READ templates/shared/stitch-selectors.md

SELECTORS = {
  # Input
  promptInput: 'textarea[placeholder*="Describe"], .prompt-input, [data-testid="prompt-input"]',
  generateButton: 'button:has-text("Generate"), [data-action="generate"], button[type="submit"]',

  # Loading
  loadingSpinner: '[data-loading="true"], .loading-indicator, [aria-busy="true"]',
  loadingComplete: '.preview-container, [data-preview], canvas',

  # Canvas/Preview
  previewCanvas: '.preview-container, [data-preview], .design-canvas',
  previewFrame: 'iframe.preview-frame',

  # Export
  exportButton: 'button:has-text("Export"), [aria-label*="Export"], button:has-text("Code")',
  codeTab: '[data-tab="code"], button:has-text("Code")',
  htmlOption: 'button:has-text("HTML"), [data-format="html"]',
  tailwindOption: 'button:has-text("Tailwind"), [data-format="tailwind"]',
  copyButton: 'button:has-text("Copy"), [aria-label*="Copy"]',
  codeOutput: 'pre, code, .code-output, [data-code]',

  # Figma
  figmaButton: 'button:has-text("Figma"), [aria-label*="Figma"], button:has-text("Copy to Figma")',

  # Error
  errorMessage: '.error-message, [role="alert"], .toast-error'
}
```

### Helper Functions for Robust Element Finding

```text
FUNCTION stitch_find_element_robust(page, selector_config, options = {}):
  """
  Robustly find element using selector config with fallback strategies.
  Tries primary + all fallbacks, checks visibility, logs which worked.

  Based on proven patterns from production Stitch automation.

  Args:
    page: Playwright page object
    selector_config: { primary, fallbacks[], description, required, timeout }
    options: { allow_interactive_fallback: bool, log: bool }

  Returns:
    { element, selector_used, method } or null
  """

  LOG "🔍 Finding element: {selector_config.description}"

  # Try primary selector first
  TRY:
    element = await page.waitForSelector(selector_config.primary, {
      timeout: 5000,  # Short timeout per selector (not total)
      state: 'attached'
    })

    IF element:
      is_visible = await element.isVisible()
      IF is_visible:
        LOG "  ✅ PRIMARY works: {selector_config.primary}"
        RETURN { element, selector_used: selector_config.primary, method: 'primary' }
      ELSE:
        LOG "  ⚠️  PRIMARY found but hidden: {selector_config.primary}"
  CATCH error:
    LOG "  ❌ PRIMARY failed: {selector_config.primary}"

  # Try fallback selectors
  FOR each fallback, index IN selector_config.fallbacks:
    TRY:
      element = await page.waitForSelector(fallback, {
        timeout: 5000,
        state: 'attached'
      })

      IF element:
        is_visible = await element.isVisible()
        IF is_visible:
          LOG "  ✅ FALLBACK {index + 1} works: {fallback}"
          RETURN { element, selector_used: fallback, method: 'fallback' }
        ELSE:
          LOG "  ⚠️  FALLBACK {index + 1} found but hidden: {fallback}"
    CATCH error:
      LOG "  ❌ FALLBACK {index + 1} failed: {fallback}"
      CONTINUE

  # All selectors failed - try interactive fallback if enabled
  IF options.allow_interactive_fallback:
    LOG "  ⚠️  All selectors failed. Switching to interactive mode..."
    RETURN await stitch_wait_for_user_click(page, selector_config)

  # No interactive fallback - fail if required
  IF selector_config.required:
    THROW {
      code: 'SELECTOR_NOT_FOUND',
      message: "Could not find {selector_config.description}",
      selector_config: selector_config
    }

  RETURN null


FUNCTION stitch_wait_for_user_click(page, selector_config):
  """
  Interactive fallback: Ask user to click the element.
  Uses :focus selector to capture what user clicked.

  Returns:
    { element, selector_used: ':focus', method: 'interactive' }
  """

  console_print("╔════════════════════════════════════════════════════════╗")
  console_print("║  🖱️  INTERACTIVE MODE                                  ║")
  console_print("╠════════════════════════════════════════════════════════╣")
  console_print("║                                                        ║")
  console_print("║  Could not find: {selector_config.description}        ║")
  console_print("║                                                        ║")
  console_print("║  Please click the element in the browser window.      ║")
  console_print("║  Then press Enter in this terminal...                 ║")
  console_print("║                                                        ║")
  console_print("╚════════════════════════════════════════════════════════╝")

  # Wait for user to press Enter
  await wait_for_enter_key()

  # Get the focused element (what user clicked)
  element = await page.waitForSelector(':focus', { timeout: 5000 })

  IF element:
    LOG "  ✅ User identified element via click"
    RETURN { element, selector_used: ':focus', method: 'interactive' }
  ELSE:
    THROW {
      code: 'INTERACTIVE_FAILED',
      message: "User did not click any focusable element"
    }


FUNCTION stitch_enter_text_clipboard(page, element, text, options = {}):
  """
  Enter text using clipboard (fast) with typing fallback.

  Clipboard method is 10x faster than typing (instant vs ~140ms per char).

  Args:
    page: Playwright page object
    element: Target input element
    text: Text to enter
    options: { prefer_typing: bool, typing_delay_ms: int }

  Returns:
    { method: 'clipboard' | 'typing', chars_entered: int }
  """

  IF options.prefer_typing:
    # User explicitly requested typing
    await element.type(text, { delay: options.typing_delay_ms OR 2 })
    RETURN { method: 'typing', chars_entered: text.length }

  # Try clipboard method first (faster)
  TRY:
    # Write to clipboard
    await page.evaluate(async (text_to_copy) => {
      await navigator.clipboard.writeText(text_to_copy)
    }, text)

    # Click element to focus
    await element.click()
    await sleep(100)

    # Paste with keyboard shortcut
    # Detect OS from page context
    platform = await page.evaluate(() => navigator.platform)

    IF platform.includes('Mac'):
      await page.keyboard.press('Meta+v')  # Cmd+V
    ELSE:
      await page.keyboard.press('Control+v')  # Ctrl+V

    await sleep(500)  # Wait for paste to complete

    LOG "  ✅ Text entered via clipboard (fast)"
    RETURN { method: 'clipboard', chars_entered: text.length }

  CATCH error:
    # Clipboard failed - fallback to typing
    LOG "  ⚠️  Clipboard paste failed, using typing fallback"
    LOG "  Error: {error.message}"

    await element.click()
    await element.type(text, { delay: options.typing_delay_ms OR 2 })

    LOG "  ✅ Text entered via typing (slow but reliable)"
    RETURN { method: 'typing', chars_entered: text.length }


FUNCTION wait_for_enter_key():
  """
  Wait for user to press Enter in the terminal.
  Cross-platform implementation.
  """

  # Python readline implementation
  RETURN NEW Promise((resolve) => {
    readline = require_module('readline')
    rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    })

    rl.question('Press Enter when ready...', () => {
      rl.close()
      resolve()
    })
  })
```

### Generate Single Mockup (Humanized)

```text
FUNCTION stitch_generate_mockup(page, prompt, output_dir, options = {}):
  """
  Generate a single mockup with human-like behavior.
  Uses Bezier mouse movements, Gaussian typing delays, and random waits.
  """

  speed = options.speed OR 'normal'  # slow, normal, fast

  # Speed multipliers for humanization
  SPEED_MULTIPLIERS = {
    slow: 1.5,     # More human-like, safer
    normal: 1.0,   # Balanced
    fast: 0.5      # Faster but riskier
  }
  speed_mult = SPEED_MULTIPLIERS[speed]

  TRY:
    1. ENSURE on Stitch page:
       current_url = page.url()
       IF NOT current_url.includes("stitch.withgoogle.com"):
         await page.goto("https://stitch.withgoogle.com")
         await page.waitForLoadState("networkidle")
         # Human-like page load pause
         await random_wait(1500 * speed_mult, 3000 * speed_mult)

    2. CHECK for CAPTCHA/blocks:
       captcha = await detect_captcha(page)
       IF captcha.detected:
         LOG "⚠️ CAPTCHA detected before input"
         await handle_captcha(page, { action: 'prompt' })

    3. FIND and interact with prompt input:
       # Load selector config from stitch-selectors.md
       IMPORT SELECTORS FROM templates/shared/stitch-selectors.md

       # Use robust element finding with visibility checks
       find_result = await stitch_find_element_robust(page, SELECTORS.promptInput, {
         allow_interactive_fallback: options.allow_interactive OR false
       })

       IF NOT find_result:
         THROW { code: 'PROMPT_INPUT_NOT_FOUND', message: "Could not find prompt input field" }

       input = find_result.element
       LOG "  📍 Using selector: {find_result.selector_used} (method: {find_result.method})"

       # Scroll to input if needed
       await scroll_to_element(page, input)

       # Human-like click on input (Bezier mouse movement)
       await move_and_click(page, input, {
         hover_time: { mean: 150 * speed_mult, std: 50 }
       })

       # Small pause after clicking (human reacts)
       await random_wait(200 * speed_mult, 500 * speed_mult)

    4. CLEAR previous prompt:
       # Select all with keyboard (more natural than triple-click)
       platform = await page.evaluate(() => navigator.platform)

       IF platform.includes('Mac'):
         await page.keyboard.press('Meta+a')  # Cmd+A on Mac
       ELSE:
         await page.keyboard.press('Control+a')  # Ctrl+A on Windows/Linux

       await random_wait(100 * speed_mult, 300 * speed_mult)
       await page.keyboard.press('Backspace')
       await random_wait(200 * speed_mult, 400 * speed_mult)

    5. ENTER new prompt (clipboard-first with typing fallback):
       # Try clipboard method first (10x faster than typing)
       entry_result = await stitch_enter_text_clipboard(page, input, prompt, {
         prefer_typing: options.prefer_typing OR false,
         typing_delay_ms: 70 * speed_mult  # Used if clipboard fails
       })

       LOG "  ⌨️  Text entry method: {entry_result.method} ({entry_result.chars_entered} chars)"

       # Pause after entering text (human reviews what they typed)
       await random_wait(500 * speed_mult, 1500 * speed_mult)

    6. CLICK generate button:
       # Use robust element finding with visibility checks
       button_result = await stitch_find_element_robust(page, SELECTORS.generateButton, {
         allow_interactive_fallback: options.allow_interactive OR false
       })

       IF NOT button_result:
         THROW { code: 'GENERATE_BUTTON_NOT_FOUND', message: "Could not find generate button" }

       generate_btn = button_result.element
       LOG "  🔘 Using selector: {button_result.selector_used} (method: {button_result.method})"

       # Scroll to button if needed
       await scroll_to_element(page, generate_btn)

       # Human-like click with Bezier movement
       await move_and_click(page, generate_btn, {
         hover_time: { mean: 200 * speed_mult, std: 80 }
       })

    7. WAIT for generation:
       # Wait for loading to start (may miss if fast)
       await page.waitForSelector(SELECTORS.loadingSpinner, { timeout: 5000 })
         .catch(() => {})

       # Wait for loading to complete
       await page.waitForSelector(SELECTORS.loadingComplete, {
         timeout: 60000,
         state: "visible"
       })

       # Human-like wait after generation (reviewing result)
       await random_wait(2000 * speed_mult, 4000 * speed_mult)

    8. CHECK for errors and blocks:
       # Check for CAPTCHA that appeared during generation
       captcha = await detect_captcha(page)
       IF captcha.detected:
         LOG "⚠️ CAPTCHA detected after generation"
         await handle_captcha(page, { action: 'prompt' })

       # Check for rate limit
       rate_limit = await detect_rate_limit(page)
       IF rate_limit.detected:
         THROW { code: 'RATE_LIMIT', message: "Rate limit detected" }

       # Check for error messages
       error = await page.$(SELECTORS.errorMessage)
       IF error:
         error_text = await error.textContent()
         THROW Error("Generation failed: " + error_text)

    9. UPDATE usage tracking:
       usage = LOAD .speckit/stitch/usage.json OR { standard: { used: 0 }, month: DATE.format("YYYY-MM") }
       usage.standard.used += 1
       usage.last_generation = new Date().toISOString()
       SAVE usage TO .speckit/stitch/usage.json

    10. RETURN success:
        track_mode_result(options.mode, true)
        RETURN { success: true, page: page }

  CATCH error:
    LOG "Generation error: {error.message}"
    track_mode_result(options.mode, false, error)

    # Handle specific errors
    IF error.code === 'RATE_LIMIT':
      RETURN { success: false, error: 'RATE_LIMIT', fallback: 'assisted' }

    IF error.code === 'CAPTCHA_DETECTED':
      RETURN { success: false, error: 'CAPTCHA', fallback: error.switch_mode }

    RETURN { success: false, error: error.message }
```

---

## Phase 5: Export Pipeline

### Export HTML/CSS (Humanized)

```text
FUNCTION stitch_export_html(page, output_dir, options = {}):
  """
  Export generated mockup as HTML/CSS with human-like interaction.
  """

  speed_mult = options.speed_mult OR 1.0

  TRY:
    1. OPEN export panel:
       export_btn = await page.waitForSelector(SELECTORS.exportButton, { timeout: 5000 })

       # Human-like click to open export
       await move_and_click(page, export_btn, {
         hover_time: { mean: 150 * speed_mult, std: 50 }
       })

       # Wait for panel to open
       await random_wait(400 * speed_mult, 800 * speed_mult)

    2. SELECT HTML format:
       # Try Tailwind first (preferred), fallback to plain HTML
       tailwind_option = await page.$(SELECTORS.tailwindOption)
       IF tailwind_option:
         await move_and_click(page, tailwind_option)
       ELSE:
         html_option = await page.$(SELECTORS.htmlOption)
         IF html_option:
           await move_and_click(page, html_option)

       # Wait for format to load
       await random_wait(300 * speed_mult, 600 * speed_mult)

    3. COPY code:
       copy_btn = await page.waitForSelector(SELECTORS.copyButton)
       await move_and_click(page, copy_btn)

       # Human pause after clicking copy
       await random_wait(200 * speed_mult, 500 * speed_mult)

       # Get code from clipboard or code output element
       code = await page.evaluate(() => navigator.clipboard.readText())
         .catch(async () => {
           # Fallback: read from code output element
           code_el = await page.$(SELECTORS.codeOutput)
           RETURN code_el ? await code_el.textContent() : null
         })

       IF NOT code:
         THROW Error("Could not extract code")

    4. PARSE and save:
       # Separate HTML and CSS if combined
       IF code.includes("<style>"):
         html_match = code.match(/<style>([\s\S]*?)<\/style>/)
         css = html_match ? html_match[1] : ""
         html = code.replace(/<style>[\s\S]*?<\/style>/, "")
       ELSE:
         html = code
         css = ""

       WRITE html TO {output_dir}/stitch-output.html
       IF css:
         WRITE css TO {output_dir}/stitch-output.css

    5. CLOSE export panel:
       await random_wait(200 * speed_mult, 400 * speed_mult)
       await page.keyboard.press("Escape")
       await random_wait(300 * speed_mult, 600 * speed_mult)

    RETURN { success: true, files: ["stitch-output.html", "stitch-output.css"] }

  CATCH error:
    LOG "HTML export failed: " + error.message
    RETURN { success: false, error: error.message }
```

### Export Screenshots (Humanized)

```text
FUNCTION stitch_export_screenshots(page, output_dir, options = {}):
  """
  Capture screenshots at different viewport sizes with smooth resizing.
  Uses smooth_viewport_resize to avoid detection.
  """

  speed_mult = options.speed_mult OR 1.0
  fingerprint = options.fingerprint OR { viewport: { width: 1440, height: 900 } }

  TRY:
    1. FIND preview element:
       preview = await page.waitForSelector(SELECTORS.previewCanvas)

       # If preview is in iframe, switch context
       preview_frame = await page.$(SELECTORS.previewFrame)
       IF preview_frame:
         frame = await preview_frame.contentFrame()
         preview = await frame.$("body")

    2. CAPTURE desktop screenshot (1440px):
       # Smooth resize to desktop viewport
       await smooth_viewport_resize(page, 1440, 900)

       # Wait for content to stabilize
       await random_wait(400 * speed_mult, 800 * speed_mult)

       await preview.screenshot({
         path: "{output_dir}/screenshot-desktop.png",
         type: "png"
       })
       LOG "Saved desktop screenshot"

    3. CAPTURE mobile screenshot (375px):
       # Smooth resize to mobile viewport
       await smooth_viewport_resize(page, 375, 812)

       # Wait for responsive layout to adjust
       await random_wait(600 * speed_mult, 1200 * speed_mult)

       await preview.screenshot({
         path: "{output_dir}/screenshot-mobile.png",
         type: "png"
       })
       LOG "Saved mobile screenshot"

    4. RESTORE viewport:
       # Smooth resize back to original fingerprint viewport
       await smooth_viewport_resize(
         page,
         fingerprint.viewport.width,
         fingerprint.viewport.height
       )

    RETURN { success: true, files: ["screenshot-desktop.png", "screenshot-mobile.png"] }

  CATCH error:
    LOG "Screenshot export failed: " + error.message
    RETURN { success: false, error: error.message }
```

### Export to Figma (Humanized)

```text
FUNCTION stitch_export_figma(page, output_dir, options = {}):
  """
  Export design to Figma clipboard format with human-like interaction.
  """

  speed_mult = options.speed_mult OR 1.0

  TRY:
    1. FIND Figma export button:
       figma_btn = await page.$(SELECTORS.figmaButton)

       IF NOT figma_btn:
         LOG "Figma export not available for this design"
         RETURN { success: false, error: "Figma export not available" }

    2. CLICK Figma export:
       # Human-like click
       await move_and_click(page, figma_btn, {
         hover_time: { mean: 150 * speed_mult, std: 50 }
       })

       # Wait for clipboard operation
       await random_wait(800 * speed_mult, 1500 * speed_mult)

    3. CAPTURE clipboard data:
       # Figma uses clipboard for transfer
       clipboard_data = await page.evaluate(() => {
         return navigator.clipboard.read()
           .then(items => items[0]?.getType("text/html"))
           .then(blob => blob?.text())
       })

       IF clipboard_data:
         WRITE clipboard_data TO {output_dir}/figma-clipboard.json

         LOG """
         Figma export ready!
         To import: Open Figma → Cmd/Ctrl+V to paste
         Clipboard data saved to: {output_dir}/figma-clipboard.json
         """

    RETURN { success: true, files: ["figma-clipboard.json"] }

  CATCH error:
    LOG "Figma export failed: " + error.message
    RETURN { success: false, error: error.message }
```

---

## Phase 6: Gallery Generation

### Generate Feature Gallery

```text
FUNCTION stitch_generate_feature_gallery(feature_name, screens):

  html = TEMPLATE("""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{feature_name} - Stitch Mockups</title>
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Inter, system-ui, sans-serif; background: #f5f5f5; }
        .header { padding: 2rem; background: white; border-bottom: 1px solid #e5e5e5; }
        .header h1 { font-size: 1.5rem; font-weight: 600; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 2rem; padding: 2rem; }
        .card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .card img { width: 100%; aspect-ratio: 16/10; object-fit: cover; }
        .card-body { padding: 1rem; }
        .card-title { font-weight: 600; margin-bottom: 0.5rem; }
        .card-actions { display: flex; gap: 0.5rem; margin-top: 1rem; }
        .btn { padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.875rem; cursor: pointer; border: none; }
        .btn-primary { background: #3b82f6; color: white; }
        .btn-secondary { background: #f3f4f6; color: #374151; }
        .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; background: #dcfce7; color: #166534; }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>{feature_name}</h1>
        <p>Generated {count} mockups via Google Stitch</p>
      </div>
      <div class="grid">
        {screen_cards}
      </div>
    </body>
    </html>
  """, {
    feature_name: feature_name,
    count: screens.length,
    screen_cards: screens.map(screen => TEMPLATE("""
      <div class="card">
        <img src="{screen_name}/screenshot-desktop.png" alt="{screen_name}">
        <div class="card-body">
          <div class="card-title">{screen_name}</div>
          <span class="badge">Generated</span>
          <div class="card-actions">
            <a href="{screen_name}/stitch-output.html" class="btn btn-primary">View HTML</a>
            <a href="{screen_name}/screenshot-mobile.png" class="btn btn-secondary">Mobile</a>
            <a href="{screen_name}/prompt.txt" class="btn btn-secondary">Prompt</a>
          </div>
        </div>
      </div>
    """, screen)).join("")
  })

  WRITE html TO .preview/stitch-mockups/{feature_name}/index.html
```

### Generate Master Gallery

```text
FUNCTION stitch_generate_master_gallery(features):

  stats = {
    total: 0,
    generated: 0,
    failed: 0
  }

  FOR each feature IN features:
    stats.total += feature.screens.length
    stats.generated += feature.screens.filter(s => s.success).length
    stats.failed += feature.screens.filter(s => !s.success).length

  html = TEMPLATE("""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Stitch Mockups Gallery</title>
      <style>
        /* ... similar styles ... */
        .stats { display: flex; gap: 2rem; margin-top: 1rem; }
        .stat { text-align: center; }
        .stat-value { font-size: 2rem; font-weight: 700; }
        .stat-label { font-size: 0.875rem; color: #6b7280; }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>Stitch Mockups Gallery</h1>
        <div class="stats">
          <div class="stat">
            <div class="stat-value">{total}</div>
            <div class="stat-label">Total Screens</div>
          </div>
          <div class="stat">
            <div class="stat-value" style="color: #16a34a">{generated}</div>
            <div class="stat-label">Generated</div>
          </div>
          <div class="stat">
            <div class="stat-value" style="color: #dc2626">{failed}</div>
            <div class="stat-label">Failed</div>
          </div>
        </div>
      </div>
      <div class="features">
        {feature_list}
      </div>
    </body>
    </html>
  """, {
    total: stats.total,
    generated: stats.generated,
    failed: stats.failed,
    feature_list: features.map(f => """
      <a href="{f.name}/index.html" class="feature-card">
        <h2>{f.name}</h2>
        <p>{f.screens.length} screens</p>
      </a>
    """).join("")
  })

  WRITE html TO .preview/stitch-mockups/index.html
```

---

## Phase 7: Error Handling

### Error Recovery Strategy

```text
ERRORS = {
  SESSION_EXPIRED: {
    detection: "redirect to accounts.google.com",
    recovery: stitch_reauth,
    retry: true
  },
  RATE_LIMIT: {
    detection: "429, quota exceeded, rate limit",
    recovery: stitch_fallback_manual,
    retry: false
  },
  CAPTCHA: {
    detection: "recaptcha, captcha, verify you're human",
    recovery: stitch_pause_for_user,
    retry: true
  },
  GENERATION_TIMEOUT: {
    detection: "timeout after 60s",
    recovery: stitch_retry_once,
    retry: true,
    max_retries: 1
  },
  EXPORT_FAILED: {
    detection: "clipboard empty, no code output",
    recovery: stitch_screenshot_fallback,
    retry: false
  },
  NETWORK_ERROR: {
    detection: "net::ERR_, network error",
    recovery: stitch_retry_with_backoff,
    retry: true,
    max_retries: 3
  }
}

FUNCTION stitch_handle_error(error, context):

  FOR each error_type, handler IN ERRORS:
    IF error.message.match(handler.detection):

      LOG "Detected error: {error_type}"

      IF handler.retry AND context.retries < (handler.max_retries OR 1):
        context.retries += 1
        LOG "Attempting recovery: {handler.recovery.name}"
        RETURN handler.recovery(context)

      ELSE:
        LOG "Max retries reached or non-recoverable error"
        RETURN { success: false, error: error_type, fallback: true }

  # Unknown error
  LOG "Unknown error: {error.message}"
  RETURN { success: false, error: "UNKNOWN", message: error.message }
```

### Fallback to Manual Mode

```text
FUNCTION stitch_fallback_manual(pending_wireframes):

  # Save all pending prompts
  FOR each wireframe IN pending_wireframes:
    prompt = stitch_generate_prompt(wireframe)
    path = ".speckit/stitch/prompts-cache/{feature}/{screen}.txt"
    WRITE prompt TO path

  # Generate manual guide
  guide = TEMPLATE("""
    # Manual Mockup Generation Guide

    Automation encountered issues. Please generate mockups manually.

    ## Steps

    1. Open https://stitch.withgoogle.com
    2. Sign in with your Google account
    3. For each screen below, copy the prompt and generate

    ## Pending Screens

    {screen_list}

    ## After Generation

    Export each result:
    1. Click "Export" → "Tailwind" or "HTML"
    2. Save to: `.preview/stitch-mockups/{feature}/{screen}/stitch-output.html`
    3. Take screenshots at 1440px and 375px width
    4. (Optional) Click "Copy to Figma" for Figma import

    ## Re-run Automation

    After resolving issues, re-run:
    ```bash
    /speckit.design --mockup
    ```
  """, {
    screen_list: pending_wireframes.map(w => """
      ### {w.screen_name}

      **Prompt file**: `.speckit/stitch/prompts-cache/{w.feature}/{w.screen_name}.txt`

      **Output to**: `.preview/stitch-mockups/{w.feature}/{w.screen_name}/`

      - [ ] Generated
      - [ ] HTML exported
      - [ ] Screenshots captured
    """).join("\n")
  })

  WRITE guide TO .speckit/stitch/manual-generation-guide.md
  LOG "Manual generation guide saved to .speckit/stitch/manual-generation-guide.md"

  # Open in editor
  EXEC: code .speckit/stitch/manual-generation-guide.md
    OR open .speckit/stitch/manual-generation-guide.md
```

---

## Phase 8: Quality Report

### Generate Report

```text
FUNCTION stitch_generate_report(results):

  report = {
    total: results.length,
    generated: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
    exports: {
      html: results.filter(r => r.exports?.html).length,
      screenshots: results.filter(r => r.exports?.screenshots).length,
      figma: results.filter(r => r.exports?.figma).length
    },
    usage: LOAD .speckit/stitch/usage.json
  }

  markdown = TEMPLATE("""
    # Mockup Generation Report

    **Generated**: {timestamp}
    **Tool**: Google Stitch (via browser automation)

    ## Summary

    | Metric | Value |
    |--------|-------|
    | Total Screens | {total} |
    | Generated | {generated} |
    | Failed | {failed} |
    | Success Rate | {success_rate}% |

    ## Export Status

    | Format | Count |
    |--------|-------|
    | HTML/CSS | {html} |
    | Screenshots | {screenshots} |
    | Figma | {figma} |

    ## Rate Limit Status

    - Standard mode: {used}/{limit} ({remaining} remaining)
    - Month: {month}

    ## Screen Details

    | Screen | Status | HTML | Desktop | Mobile | Figma |
    |--------|--------|------|---------|--------|-------|
    {screen_rows}

    ## Failed Screens

    {failed_details}

    ## Next Steps

    {next_steps}
  """, {
    timestamp: new Date().toISOString(),
    total: report.total,
    generated: report.generated,
    failed: report.failed,
    success_rate: Math.round(report.generated / report.total * 100),
    html: report.exports.html,
    screenshots: report.exports.screenshots,
    figma: report.exports.figma,
    used: report.usage.standard.used,
    limit: 350,
    remaining: 350 - report.usage.standard.used,
    month: report.usage.month,
    screen_rows: results.map(r => """
      | {r.screen_name} | {r.success ? '✅' : '❌'} | {r.exports?.html ? '✅' : '❌'} | {r.exports?.desktop ? '✅' : '❌'} | {r.exports?.mobile ? '✅' : '❌'} | {r.exports?.figma ? '✅' : '❌'} |
    """).join("\n"),
    failed_details: results.filter(r => !r.success).map(r => """
      - **{r.screen_name}**: {r.error}
    """).join("\n") OR "None",
    next_steps: report.failed > 0
      ? "- Retry failed screens: `/speckit.design --mockup --retry`\n- Or use manual mode: See `.speckit/stitch/manual-generation-guide.md`"
      : "- Preview mockups: Open `.preview/stitch-mockups/index.html`\n- Continue to planning: `/speckit.plan`"
  })

  WRITE markdown TO .preview/stitch-mockups/mockup-report.md
  LOG "Report saved to .preview/stitch-mockups/mockup-report.md"

  RETURN report
```

---

## Main Orchestration

```text
FUNCTION stitch_main(options):

  LOG "Starting Google Stitch mockup generation (v3 - Anti-Detection)..."

  # Determine speed multiplier from --speed option
  speed_mult = SWITCH options.speed:
    CASE 'slow': 2.0      # Maximum humanization, safest
    CASE 'fast': 0.5      # Minimal delays, riskier
    DEFAULT: 1.0          # Normal humanization

  # Handle --setup-cdp helper command
  IF options.setup_cdp:
    LOG """
    ┌─────────────────────────────────────────────────────────────────────┐
    │  CDP MODE SETUP                                                     │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │  Run this command to start Chrome with debugging enabled:           │
    │                                                                     │
    │  macOS/Linux:                                                       │
    │    /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome │
    │      --remote-debugging-port=9222                                   │
    │      --user-data-dir="$HOME/.speckit/chrome-profile"                │
    │                                                                     │
    │  Windows:                                                           │
    │    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"     │
    │      --remote-debugging-port=9222                                   │
    │      --user-data-dir="%USERPROFILE%\\.speckit\\chrome-profile"      │
    │                                                                     │
    │  Then run: /speckit.stitch --mode cdp                               │
    └─────────────────────────────────────────────────────────────────────┘
    """
    RETURN

  # Handle --prepare (assisted mode - prompts only)
  IF options.prepare:
    LOG "Assisted Mode: Generating prompts only (no browser automation)"
    wireframes = stitch_discover_wireframes(options)
    design_context = stitch_load_design_context()
    stitch_fallback_manual(wireframes, design_context)
    RETURN { mode: 'assisted', phase: 'prepare' }

  # Handle --collect (assisted mode - collect exports)
  IF options.collect:
    LOG "Assisted Mode: Collecting exports from .speckit/stitch/exports/"
    results = stitch_collect_manual_exports()
    stitch_generate_master_gallery(results)
    RETURN { mode: 'assisted', phase: 'collect', results }

  # Handle --audit-selectors (diagnostic mode - test selectors without mockup generation)
  IF options.audit_selectors:
    LOG "Selector Audit Mode: Testing all Stitch UI selectors (no mockup generation)"
    LOG ""

    # Load debug utilities
    IMPORT * FROM templates/shared/stitch-debug-utils.md:
      - audit_all_selectors
      - test_selector
      - inspect_element_at_selector
      - ENSURE_DIRECTORY_EXISTS

    # Preflight check (need browser for audit)
    preflight = stitch_preflight_check()
    IF NOT preflight.playwright_ready OR NOT preflight.browser_ready:
      THROW Error("Playwright not ready. Run: npx playwright install chromium")

    # Select mode and create browser context
    mode_result = stitch_select_mode({
      preferred: options.mode OR 'stealth',
      speed: options.speed OR 'normal'
    })

    LOG "Using {mode_result.mode} mode for selector audit"
    LOG ""

    browser_context = stitch_create_browser_context(mode_result, options)
    browser = browser_context.browser
    page = browser_context.page

    # Authenticate to access Stitch UI
    TRY:
      auth_result = stitch_authenticate(browser, page, options)

      IF NOT auth_result.authenticated:
        LOG "❌ Authentication failed. Cannot audit selectors without access to Stitch."
        await browser.close()
        RETURN { mode: 'audit', success: false, error: 'authentication_failed' }

      # Run selector audit
      audit_result = await audit_all_selectors(page, {
        verbose: options.log_level === 'debug' OR options.verbose,
        screenshot_failures: true,
        categories: options.audit_categories  # Optional: filter by category
      })

      # Cleanup
      await browser.close()

      # Return audit results
      RETURN {
        mode: 'audit',
        success: audit_result.summary.all_working,
        audit_results: audit_result,
        total: audit_result.total,
        working: audit_result.working,
        broken: audit_result.broken,
        critical_failures: audit_result.summary.critical_failures
      }

    CATCH error:
      LOG "❌ Audit failed: {error.message}"

      TRY:
        await browser.close()
      CATCH:
        # Ignore cleanup errors

      RETURN {
        mode: 'audit',
        success: false,
        error: error.message
      }

  # Phase 0: Preflight with mode selection
  preflight = stitch_preflight_check()
  IF NOT preflight.playwright_ready OR NOT preflight.browser_ready:
    IF options.mode != 'assisted':
      WARN "Playwright not ready, falling back to assisted mode"
      options.mode = 'assisted'

  # Rate limit check
  IF NOT preflight.rate_limit_ok:
    IF options.force:
      WARN "Proceeding despite rate limit (--force)"
    ELSE:
      LOG "Rate limit reached. Switching to assisted mode."
      wireframes = stitch_discover_wireframes(options)
      design_context = stitch_load_design_context()
      stitch_fallback_manual(wireframes, design_context)
      RETURN { mode: 'assisted', reason: 'rate_limit' }

  # Select automation mode (CDP → Stealth → Turbo → Assisted)
  mode_result = stitch_select_mode({
    preferred: options.mode,      # User's explicit choice if any
    speed: options.speed
  })

  LOG "Selected mode: {mode_result.mode} ({mode_result.reason})"

  # If assisted mode selected, use manual workflow
  IF mode_result.mode == 'assisted':
    wireframes = stitch_discover_wireframes(options)
    design_context = stitch_load_design_context()
    stitch_fallback_manual(wireframes, design_context)
    RETURN { mode: 'assisted', reason: mode_result.reason }

  # Phase 1: Create browser context with anti-detection
  context_result = stitch_create_browser_context(mode_result, {
    speed: options.speed,
    headless: false  # Always visible for Stitch
  })

  IF NOT context_result.success:
    WARN "Browser context creation failed: {context_result.error}"
    WARN "Falling back to assisted mode"
    wireframes = stitch_discover_wireframes(options)
    design_context = stitch_load_design_context()
    stitch_fallback_manual(wireframes, design_context)
    RETURN { mode: 'assisted', reason: 'browser_failed' }

  context = context_result.context
  active_mode = mode_result.mode

  # Phase 1b: Session restoration or Authentication
  page = null

  # Try to restore cached session first (if enabled)
  IF options.reuse_session !== false:
    session_load_result = load_browser_session()

    IF session_load_result.valid:
      LOG "🔄 Attempting to restore cached session..."

      # Navigate to Stitch first
      temp_page = await context.newPage()
      await temp_page.goto("https://stitch.withgoogle.com")

      # Restore session
      restore_result = await restore_browser_session(
        context,
        temp_page,
        session_load_result.session_state
      )

      IF restore_result.authenticated:
        LOG "✅ Session restored successfully (~30s saved)"
        page = temp_page
      ELSE:
        LOG "⚠️  Session restore failed, falling back to authentication"
        await temp_page.close()
    ELSE:
      LOG "⏭️  No valid session cache: {session_load_result.reason}"

  # If session not restored, authenticate normally
  IF NOT page:
    LOG "🔐 Authenticating with Google..."
    auth_result = stitch_authenticate(context, { speed_mult })
    IF NOT auth_result.authenticated:
      ERROR "Authentication failed: {auth_result.error}"
      await context.close()
      RETURN { mode: active_mode, error: 'auth_failed' }

    page = auth_result.page

  # Phase 2: Discover wireframes
  scope = options.all ? "app" : "feature"
  IF options.screens:
    scope = { screens: options.screens.split(",") }

  wireframes = stitch_discover_wireframes(scope)
  LOG "Found {wireframes.length} wireframes to process"

  IF wireframes.length == 0:
    WARN "No wireframes found. Run /speckit.design first."
    await context.close()
    RETURN { mode: active_mode, error: 'no_wireframes' }

  # Phase 2b: Incremental detection (skip unchanged screens)
  skipped_screens = []
  incremental_stats = { skip_count: 0, time_saved_est_seconds: 0 }

  IF options.incremental !== false AND NOT options.force:
    LOG "🔍 Checking for unchanged screens (incremental mode)..."

    # Load design context early for hash calculation
    design_context = stitch_load_design_context()
    design_context_hash = hash_design_context(design_context)

    # Detect which screens can be skipped
    incremental_result = detect_incremental_screens(wireframes, design_context, {
      force: options.force,
      incremental: options.incremental
    })

    # Update wireframes list to only those needing generation
    wireframes = incremental_result.to_generate
    skipped_screens = incremental_result.to_skip
    incremental_stats = incremental_result.stats

    # Early exit if nothing to generate
    IF wireframes.length == 0:
      LOG "✅ All {skipped_screens.length} screens up-to-date. Nothing to generate!"
      await context.close()

      RETURN {
        mode: active_mode,
        results: [],
        skipped: skipped_screens.length,
        incremental_stats: incremental_stats,
        message: "All screens unchanged (incremental mode)"
      }
  ELSE:
    # Load design context normally (not loaded yet in non-incremental mode)
    design_context = stitch_load_design_context()
    design_context_hash = hash_design_context(design_context)

  # Phase 3: Design context loaded (either in Phase 2b or above)
  # (no additional action needed, design_context and design_context_hash already set)

  # Phase 4-5: Generate and export (PARALLEL or SEQUENTIAL)
  results = []
  generation_stats = null

  # BRANCH: Parallel vs Sequential mode
  IF options.parallel !== false:
    # ========================================
    # PARALLEL MODE (default, 3-5x faster)
    # ========================================

    LOG "⚡ Using parallel generation (max {options.max_parallel OR 3} concurrent)"
    LOG "   Rate limit protection: {options.batch_delay OR 5000}ms between batches"

    # Close single-context browser (we'll use pool instead)
    await context.close()

    # Generate all mockups in parallel
    parallel_result = await stitch_generate_mockups_parallel(wireframes, design_context, {
      max_parallel: options.max_parallel OR 3,
      batch_delay: options.batch_delay OR 5000,
      speed_mult: speed_mult,
      mode: active_mode,
      viewports: options.viewports,
      no_webp: options.no_webp,
      no_optimize: options.no_optimize,
      interactive: options.interactive,
      no_figma: options.no_figma
    })

    results = parallel_result.results
    generation_stats = parallel_result.stats

    # Note: Browser pool is cleaned up inside parallel function
    # Skip to Phase 6 (galleries)

  ELSE:
    # ========================================
    # SEQUENTIAL MODE (legacy, for debugging)
    # ========================================

    LOG "🐌 Using sequential generation (--no-parallel flag detected)"

    captcha_count = 0
    MAX_CAPTCHA_BEFORE_FALLBACK = 2

    FOR each wireframe, index IN wireframes:
    LOG "Processing [{index + 1}/{wireframes.length}]: {wireframe.screen_name}"

    # Create output directory
    output_dir = ".preview/stitch-mockups/{wireframe.feature}/{wireframe.screen_name}"
    MKDIR output_dir

    # Generate prompt
    prompt = stitch_generate_prompt(wireframe, design_context)
    WRITE prompt TO {output_dir}/prompt.txt

    # Cache prompt for reuse (retry/manual mode)
    cache_prompt(wireframe, prompt, design_context_hash)

    # Generate mockup with humanization
    gen_result = stitch_generate_mockup(page, prompt, output_dir, {
      speed_mult: speed_mult,
      mode: active_mode
    })

    # Handle CAPTCHA detection - trigger fallback
    IF gen_result.captcha_detected:
      captcha_count++
      LOG "⚠️  CAPTCHA detected ({captcha_count}/{MAX_CAPTCHA_BEFORE_FALLBACK})"

      IF captcha_count >= MAX_CAPTCHA_BEFORE_FALLBACK:
        WARN "Multiple CAPTCHAs detected. Google may be blocking automation."
        WARN "Switching to assisted mode for remaining screens."

        # Close browser and generate manual prompts for remaining
        await context.close()
        remaining = wireframes.slice(index)
        stitch_fallback_manual(remaining, design_context)

        # Update mode stats
        stitch_update_mode_stats(active_mode, {
          attempts: index,
          successes: results.filter(r => r.success).length,
          failures: results.filter(r => !r.success).length,
          captcha_triggered: true
        })

        RETURN {
          mode: active_mode,
          fallback: 'assisted',
          reason: 'captcha_detected',
          results: results,
          remaining: remaining.length
        }

      # Try to handle CAPTCHA (pause for user)
      handled = handle_captcha_detection(page)
      IF NOT handled:
        results.push({
          screen_name: wireframe.screen_name,
          feature: wireframe.feature,
          success: false,
          error: 'captcha_not_resolved'
        })
        CONTINUE

    IF gen_result.success:
      # Export HTML/CSS (standard)
      html_result = stitch_export_html(page, output_dir, { speed_mult })

      # Export screenshots with multi-viewport and WebP (ENHANCED)
      screenshot_result = stitch_export_screenshots_enhanced(page, output_dir, {
        speed_mult: speed_mult,
        viewports: options.viewports OR ['desktop', 'tablet', 'mobile'],
        no_webp: options.no_webp,
        no_optimize: options.no_optimize
      })

      # Generate interactive preview (NEW)
      interactive_result = { success: false }
      IF options.interactive !== false AND html_result.success:
        # Extract HTML/CSS content for interactive preview
        html_content = READ_FILE("{output_dir}/stitch-output.html")
        css_content = READ_FILE("{output_dir}/stitch-output.css") OR ""

        interactive_result = generate_interactive_preview(
          html_content,
          css_content,
          output_dir
        )

      # Figma export optional (standard)
      figma_result = { success: false }
      IF NOT options.no_figma:
        figma_result = stitch_export_figma(page, output_dir, { speed_mult })

      results.push({
        screen_name: wireframe.screen_name,
        feature: wireframe.feature,
        success: true,
        exports: {
          html: html_result.success,
          desktop: screenshot_result.success,
          tablet: screenshot_result.success,  // NEW
          mobile: screenshot_result.success,
          webp: !options.no_webp && screenshot_result.success,  // NEW
          interactive: interactive_result.success,  // NEW
          figma: figma_result.success
        },
        stats: screenshot_result.stats  // WebP compression stats
      })

      # Random delay between screens (humanization)
      IF index < wireframes.length - 1:
        await random_wait(2000 * speed_mult, 5000 * speed_mult)

    ELSE:
      results.push({
        screen_name: wireframe.screen_name,
        feature: wireframe.feature,
        success: false,
        error: gen_result.error
      })

    # Save browser session for reuse (sequential mode only)
    IF options.reuse_session !== false:
      save_result = await save_browser_session(context, page)
      IF save_result.success:
        LOG "💾 Session saved for next run (~30s saved)"

    # Close browser context (sequential mode only)
    await context.close()

  # END BRANCH (parallel/sequential)
  # Note: Parallel mode manages its own browser pool and session saving

  # Phase 6: Generate galleries
  features = group_by_feature(results)
  FOR each feature IN features:
    stitch_generate_feature_gallery(feature.name, feature.screens)
  stitch_generate_master_gallery(features)

  # Phase 7: Update usage tracking
  stitch_update_usage(results.filter(r => r.success).length)

  # Phase 8: Update mode statistics
  stitch_update_mode_stats(active_mode, {
    attempts: wireframes.length,
    successes: results.filter(r => r.success).length,
    failures: results.filter(r => !r.success).length,
    captcha_triggered: captcha_count > 0
  })

  # Phase 9: Generate report
  report = stitch_generate_report(results)

  # Close browser
  await context.close()

  # Calculate success stats
  success_count = results.filter(r => r.success).length
  partial_count = results.filter(r => r.success && !r.exports.figma).length
  failed_count = results.filter(r => !r.success).length

  # Output summary with mode info
  LOG """
  ┌─────────────────────────────────────────────────────────────────────┐
  │  🎨 STITCH MOCKUP GENERATION COMPLETE (v3)                          │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  Mode: {active_mode.toUpperCase()}                                  │
  │  Speed: {options.speed OR 'normal'}                                 │
  │                                                                     │
  │  Screens: {success_count}/{wireframes.length}                       │
  │  Success: {success_count}  Partial: {partial_count}  Failed: {failed_count}
  │                                                                     │
  │  Exports:                                                           │
  │    HTML/CSS: {report.exports.html}                                  │
  │    Screenshots: {report.exports.screenshots}                        │
  │    Figma: {report.exports.figma}                                    │
  │                                                                     │
  │  Rate limit: {report.usage.standard.used}/350 this month            │
  │                                                                     │
  │  📁 Output: .preview/stitch-mockups/                                │
  │  📊 Gallery: .preview/stitch-mockups/index.html                     │
  │                                                                     │
  ├─────────────────────────────────────────────────────────────────────┤
  │  Next Steps:                                                        │
  │   → open .preview/stitch-mockups/index.html                         │
  │   → /speckit.preview (serve gallery)                                │
  └─────────────────────────────────────────────────────────────────────┘
  """

  RETURN { mode: active_mode, report, results }


/**
 * Collect manual exports from assisted mode
 */
FUNCTION stitch_collect_manual_exports():
  exports_dir = ".speckit/stitch/exports/"

  IF NOT EXISTS(exports_dir):
    ERROR "No exports directory found. Place your exports in {exports_dir}"
    RETURN []

  results = []

  # Scan for exported files
  FOR each screen_dir IN list_dirs(exports_dir):
    screen_name = basename(screen_dir)

    # Check what files exist
    has_html = EXISTS("{screen_dir}/code.html")
    has_png = EXISTS("{screen_dir}/mockup.png")
    has_figma = EXISTS("{screen_dir}/figma.json")

    IF has_html OR has_png:
      # Move to output directory
      output_dir = ".preview/stitch-mockups/manual/{screen_name}"
      MKDIR output_dir

      IF has_html:
        COPY "{screen_dir}/code.html" TO "{output_dir}/code.html"
      IF has_png:
        COPY "{screen_dir}/mockup.png" TO "{output_dir}/screenshot-desktop.png"
      IF has_figma:
        COPY "{screen_dir}/figma.json" TO "{output_dir}/figma-clipboard.json"

      results.push({
        screen_name: screen_name,
        feature: 'manual',
        success: true,
        exports: {
          html: has_html,
          desktop: has_png,
          mobile: false,
          figma: has_figma
        }
      })

  LOG "Collected {results.length} manual exports"
  RETURN results


/**
 * Update mode statistics for tracking success rates
 */
FUNCTION stitch_update_mode_stats(mode, stats):
  stats_file = ".speckit/stitch/usage.json"
  usage = READ_JSON(stats_file) OR { mode_stats: {} }

  IF NOT usage.mode_stats[mode]:
    usage.mode_stats[mode] = {
      attempts: 0,
      successes: 0,
      failures: 0,
      captcha_triggered: 0
    }

  usage.mode_stats[mode].attempts += stats.attempts
  usage.mode_stats[mode].successes += stats.successes
  usage.mode_stats[mode].failures += stats.failures
  IF stats.captcha_triggered:
    usage.mode_stats[mode].captcha_triggered++

  WRITE_JSON(stats_file, usage)
  LOG "Updated mode stats for {mode}"
```

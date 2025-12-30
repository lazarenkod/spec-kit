# Stitch Anti-Detection Module

> Humanization techniques and automation bypass strategies for Google Stitch browser automation.

## Module Metadata

```yaml
version: 1.0.0
last_updated: 2025-01-01
status: active
dependencies:
  - playwright OR patchright
  - chromium
```

---

## Overview

Google detects browser automation through multiple vectors. This module provides techniques to evade detection while maintaining automation reliability.

### Detection Vectors & Mitigations

| Vector | Detection Method | Mitigation |
|--------|------------------|------------|
| CDP Detection | `Runtime.enable` traces | CDP mode or Patchright |
| navigator.webdriver | Property set to `true` | Stealth args + Patchright |
| Behavioral Analysis | Fixed delays, linear mouse | Humanization functions |
| Fingerprinting | Canvas, WebGL, viewport | Random fingerprint generation |
| Timing Patterns | Consistent intervals | Random distributions |

---

## Utility Functions

### Random Distributions

```javascript
/**
 * Gaussian (normal) distribution random number
 * Uses Box-Muller transform
 */
FUNCTION gaussian_random(mean, std_dev):
  u1 = Math.random()
  u2 = Math.random()

  // Box-Muller transform
  z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2)

  RETURN mean + z0 * std_dev


/**
 * Exponential distribution random number
 * Good for wait times (more short waits, occasional long ones)
 */
FUNCTION exponential_random(mean):
  RETURN -mean * Math.log(Math.random())


/**
 * Clamp value between min and max
 */
FUNCTION clamp(value, min, max):
  RETURN Math.max(min, Math.min(max, value))


/**
 * Random integer in range [min, max] inclusive
 */
FUNCTION random_int(min, max):
  RETURN Math.floor(Math.random() * (max - min + 1)) + min


/**
 * Random float in range [min, max]
 */
FUNCTION random_float(min, max):
  RETURN Math.random() * (max - min) + min


/**
 * Pick random element from array
 */
FUNCTION random_choice(array):
  RETURN array[Math.floor(Math.random() * array.length)]
```

### Easing Functions

```javascript
/**
 * Ease-in-out cubic - natural acceleration/deceleration
 */
FUNCTION ease_in_out_cubic(t):
  IF t < 0.5:
    RETURN 4 * t * t * t
  ELSE:
    RETURN 1 - Math.pow(-2 * t + 2, 3) / 2


/**
 * Linear interpolation
 */
FUNCTION lerp(start, end, progress):
  RETURN start + (end - start) * progress
```

### Bezier Curve Generation

```javascript
/**
 * Generate Bezier curve path for mouse movement
 * Creates natural-looking curved path between two points
 */
FUNCTION bezier_curve(start, end, options = {}):
  control_points = options.control_points OR 2
  steps = options.steps OR 20

  // Generate random control points for curve variance
  controls = []

  FOR i IN range(control_points):
    // Control points deviate from straight line
    progress = (i + 1) / (control_points + 1)

    // Base point on straight line
    base_x = lerp(start.x, end.x, progress)
    base_y = lerp(start.y, end.y, progress)

    // Add random deviation (larger in middle of path)
    deviation_factor = Math.sin(progress * Math.PI) * 100
    deviation_x = gaussian_random(0, deviation_factor)
    deviation_y = gaussian_random(0, deviation_factor * 0.5)

    controls.push({
      x: base_x + deviation_x,
      y: base_y + deviation_y
    })

  // Build full control point array: [start, ...controls, end]
  all_points = [start, ...controls, end]

  // Generate path points using De Casteljau's algorithm
  path = []
  FOR step IN range(steps + 1):
    t = step / steps
    point = de_casteljau(all_points, t)
    path.push(point)

  RETURN path


/**
 * De Casteljau's algorithm for Bezier curve evaluation
 */
FUNCTION de_casteljau(points, t):
  IF points.length == 1:
    RETURN points[0]

  new_points = []
  FOR i IN range(points.length - 1):
    new_points.push({
      x: lerp(points[i].x, points[i + 1].x, t),
      y: lerp(points[i].y, points[i + 1].y, t)
    })

  RETURN de_casteljau(new_points, t)
```

### Fitts's Law Timing

```javascript
/**
 * Calculate movement time using Fitts's Law
 * Models human motor control for pointing tasks
 *
 * Formula: MT = a + b * log2(D/W + 1)
 * Where: D = distance, W = target width
 */
FUNCTION fitts_time(distance, target_width, options = {}):
  // Empirical constants (calibrated for mouse movement)
  a = options.a OR 50   // Base time in ms
  b = options.b OR 150  // Scaling factor

  // Fitts's Law calculation
  index_of_difficulty = Math.log2(distance / target_width + 1)
  base_time = a + b * index_of_difficulty

  // Add human variance (±20%)
  variance = gaussian_random(1.0, 0.1)

  RETURN Math.max(100, base_time * variance)


/**
 * Calculate distance between two points
 */
FUNCTION distance(p1, p2):
  dx = p2.x - p1.x
  dy = p2.y - p1.y
  RETURN Math.sqrt(dx * dx + dy * dy)
```

---

## Humanization Functions

### Human-Like Typing

```javascript
/**
 * Type text with human-like timing and occasional typos
 *
 * Features:
 * - Gaussian-distributed keystroke delays
 * - Occasional typos with corrections (2% chance)
 * - Pauses at punctuation
 * - Variable rhythm based on character sequences
 */
FUNCTION humanize_typing(element, text, options = {}):
  mean_delay = options.mean_delay OR 70      // ms between keystrokes
  std_delay = options.std_delay OR 30        // variance
  typo_rate = options.typo_rate OR 0.02      // 2% typo chance

  // Keyboard layout for typo generation (nearby keys)
  KEYBOARD_NEIGHBORS = {
    'a': ['s', 'q', 'w', 'z'],
    'b': ['v', 'g', 'h', 'n'],
    'c': ['x', 'd', 'f', 'v'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'],
    'e': ['w', 's', 'd', 'r'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'i': ['u', 'j', 'k', 'o'],
    'j': ['h', 'u', 'i', 'k', 'm', 'n'],
    'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'],
    'm': ['n', 'j', 'k'],
    'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'k', 'l', 'p'],
    'p': ['o', 'l'],
    'q': ['w', 'a'],
    'r': ['e', 'd', 'f', 't'],
    's': ['a', 'w', 'e', 'd', 'x', 'z'],
    't': ['r', 'f', 'g', 'y'],
    'u': ['y', 'h', 'j', 'i'],
    'v': ['c', 'f', 'g', 'b'],
    'w': ['q', 'a', 's', 'e'],
    'x': ['z', 's', 'd', 'c'],
    'y': ['t', 'g', 'h', 'u'],
    'z': ['a', 's', 'x']
  }

  FUNCTION get_nearby_key(char):
    lower = char.toLowerCase()
    IF lower IN KEYBOARD_NEIGHBORS:
      neighbors = KEYBOARD_NEIGHBORS[lower]
      nearby = random_choice(neighbors)
      // Preserve case
      RETURN char === char.toUpperCase() ? nearby.toUpperCase() : nearby
    RETURN char

  // Type each character
  FOR i, char IN enumerate(text):
    // Calculate base delay with Gaussian distribution
    delay = Math.max(20, gaussian_random(mean_delay, std_delay))

    // Adjust delay based on character type
    IF char === ' ':
      // Slightly longer pause at word boundaries
      delay *= random_float(1.1, 1.3)
    ELIF char IN ['shift', 'caps']:
      // Modifier key combinations take longer
      delay *= random_float(1.2, 1.5)

    // Occasional typo (skip for punctuation/special chars)
    IF Math.random() < typo_rate AND char.match(/[a-zA-Z]/):
      wrong_char = get_nearby_key(char)

      // Type wrong character
      await element.type(wrong_char, { delay: delay })

      // Reaction delay before noticing mistake
      await sleep(gaussian_random(200, 80))

      // Delete wrong character
      await element.press('Backspace')

      // Short pause before correction
      await sleep(gaussian_random(100, 40))

    // Type correct character
    await element.type(char, { delay: delay })

    // Pause at punctuation (sentence boundaries)
    IF char IN ['.', '!', '?']:
      await sleep(gaussian_random(800, 300))
    ELIF char IN [',', ';', ':']:
      await sleep(gaussian_random(300, 100))

    // Occasional thinking pause mid-sentence (0.5% chance)
    IF Math.random() < 0.005 AND i < text.length - 1:
      await sleep(gaussian_random(1500, 500))
```

### Human-Like Mouse Movement and Click

```javascript
/**
 * Move mouse along Bezier curve and click with human-like behavior
 *
 * Features:
 * - Bezier curve path (not straight line)
 * - Fitts's Law timing
 * - Hover pause before click
 * - Position jitter on click
 * - Optional scroll to element first
 */
FUNCTION move_and_click(page, element, options = {}):
  scroll_first = options.scroll_first !== false  // Default true
  hover_time = options.hover_time OR { mean: 200, std: 80 }

  // Get element bounding box
  box = await element.boundingBox()
  IF NOT box:
    THROW Error("Element not visible or has no bounding box")

  // Scroll element into view if needed
  IF scroll_first:
    await scroll_to_element(page, element)

  // Calculate target with jitter (not exact center)
  target = {
    x: box.x + box.width / 2 + random_float(-5, 5),
    y: box.y + box.height / 2 + random_float(-5, 5)
  }

  // Get current mouse position (or random start if unknown)
  current = await get_mouse_position(page)
  IF NOT current:
    current = {
      x: random_int(100, 500),
      y: random_int(100, 300)
    }

  // Generate Bezier curve path
  path = bezier_curve(current, target, {
    control_points: 2,
    steps: random_int(15, 25)
  })

  // Calculate total movement time using Fitts's Law
  total_time = fitts_time(
    distance(current, target),
    Math.min(box.width, box.height)
  )

  // Move along path with ease-in-out timing
  FOR i, point IN enumerate(path):
    // Ease-in-out progress
    progress = ease_in_out_cubic(i / (path.length - 1))

    // Time for this segment with variance
    segment_time = (total_time / path.length) * random_float(0.7, 1.3)

    await page.mouse.move(point.x, point.y)
    await sleep(segment_time)

  // Hover pause before clicking (humans don't click instantly)
  await sleep(gaussian_random(hover_time.mean, hover_time.std))

  // Click with slight position adjustment
  click_x = target.x + random_float(-2, 2)
  click_y = target.y + random_float(-2, 2)

  await page.mouse.click(click_x, click_y)

  // Small post-click delay (finger leaving mouse)
  await sleep(gaussian_random(50, 20))


/**
 * Get current mouse position from page
 */
FUNCTION get_mouse_position(page):
  TRY:
    position = await page.evaluate(() => {
      RETURN window.__mousePosition OR null
    })
    RETURN position
  CATCH:
    RETURN null


/**
 * Double-click with human timing
 */
FUNCTION move_and_double_click(page, element, options = {}):
  // First click
  await move_and_click(page, element, options)

  // Brief pause between clicks (human double-click timing)
  await sleep(gaussian_random(80, 20))

  // Second click at same position (slight drift)
  box = await element.boundingBox()
  click_x = box.x + box.width / 2 + random_float(-3, 3)
  click_y = box.y + box.height / 2 + random_float(-3, 3)

  await page.mouse.click(click_x, click_y)
```

### Random Wait Replacement

```javascript
/**
 * Human-like random wait with exponential distribution
 * Replaces fixed waitForTimeout calls
 *
 * Usage:
 *   await random_wait(400, 800)   // Instead of waitForTimeout(500)
 *   await random_wait(1500, 3500) // Instead of waitForTimeout(2000)
 */
FUNCTION random_wait(min_ms, max_ms, options = {}):
  distribution = options.distribution OR 'exponential'

  IF distribution === 'exponential':
    // Exponential feels more human (many short, few long)
    mean = (min_ms + max_ms) / 2
    delay = exponential_random(mean)
    delay = clamp(delay, min_ms, max_ms)
  ELIF distribution === 'gaussian':
    mean = (min_ms + max_ms) / 2
    std = (max_ms - min_ms) / 4
    delay = gaussian_random(mean, std)
    delay = clamp(delay, min_ms, max_ms)
  ELSE:
    // Uniform distribution
    delay = random_float(min_ms, max_ms)

  await sleep(delay)
  RETURN delay  // Return actual delay for logging


/**
 * Convenience wrappers for common wait scenarios
 */
FUNCTION wait_short():
  RETURN random_wait(200, 500)

FUNCTION wait_medium():
  RETURN random_wait(500, 1500)

FUNCTION wait_long():
  RETURN random_wait(1500, 4000)

FUNCTION wait_page_load():
  RETURN random_wait(2000, 5000)
```

### Scroll Simulation

```javascript
/**
 * Scroll to element with human-like chunked scrolling
 *
 * Features:
 * - Checks if element is in viewport first
 * - Scrolls in variable-sized chunks
 * - Adds reading pauses
 * - Includes scroll jitter
 */
FUNCTION scroll_to_element(page, element, options = {}):
  reading_pause = options.reading_pause !== false  // Default true

  box = await element.boundingBox()
  IF NOT box:
    RETURN  // Element not visible

  viewport = await page.viewportSize()
  current_scroll = await page.evaluate('window.pageYOffset')

  // Check if element is already reasonably visible
  element_top = box.y
  element_visible_threshold = viewport.height * 0.7

  IF element_top < element_visible_threshold AND element_top > 50:
    // Element is visible enough, no scroll needed
    RETURN

  // Calculate target scroll position (element at 1/3 of viewport)
  target_scroll = current_scroll + box.y - viewport.height / 3
  target_scroll = Math.max(0, target_scroll)

  // Don't scroll if distance is tiny
  scroll_distance = Math.abs(target_scroll - current_scroll)
  IF scroll_distance < 50:
    RETURN

  // Scroll in chunks (3-8 steps)
  steps = random_int(3, 8)

  FOR i IN range(steps):
    // Calculate scroll amount for this step
    remaining = target_scroll - current_scroll

    // Ease-out: bigger steps first, smaller at end
    progress = (i + 1) / steps
    step_factor = 1 - ease_in_out_cubic(progress) * 0.5

    scroll_amount = (remaining / (steps - i)) * step_factor

    // Add jitter to scroll amount
    scroll_amount += gaussian_random(0, 20)

    await page.evaluate(f'window.scrollBy(0, {scroll_amount})')
    current_scroll += scroll_amount

    // Variable delay between scroll chunks
    await sleep(gaussian_random(100, 40))

  // Reading pause after scroll (simulates eye finding target)
  IF reading_pause:
    await sleep(gaussian_random(500, 200))
```

### Smooth Viewport Resize

```javascript
/**
 * Resize viewport smoothly with human-like increments
 * Replaces instant setViewportSize calls
 */
FUNCTION smooth_viewport_resize(page, target_width, target_height, options = {}):
  steps = options.steps OR random_int(3, 6)

  current = await page.viewportSize()

  // Add slight jitter to target (humans don't resize to exact pixels)
  target_width += random_int(-10, 10)
  target_height += random_int(-10, 10)

  // Skip if already at target size (within tolerance)
  IF Math.abs(current.width - target_width) < 20 AND
     Math.abs(current.height - target_height) < 20:
    RETURN

  FOR i IN range(steps):
    // Ease-in-out progress
    progress = ease_in_out_cubic((i + 1) / steps)

    new_width = Math.round(lerp(current.width, target_width, progress))
    new_height = Math.round(lerp(current.height, target_height, progress))

    await page.setViewportSize({
      width: new_width,
      height: new_height
    })

    await sleep(gaussian_random(150, 50))

  // Stabilization delay after resize
  await sleep(gaussian_random(400, 150))
```

---

## Fingerprint Generation

### Random Browser Fingerprint

```javascript
/**
 * Generate random but consistent browser fingerprint
 * Called once per session to set viewport, locale, timezone
 */
FUNCTION generate_fingerprint():
  // Common desktop viewport sizes (realistic distribution)
  VIEWPORT_PRESETS = [
    { width: 1920, height: 1080, weight: 0.35 },  // Full HD (most common)
    { width: 1366, height: 768, weight: 0.25 },   // HD
    { width: 1536, height: 864, weight: 0.15 },   // Scaled Full HD
    { width: 1440, height: 900, weight: 0.10 },   // MacBook Pro 15"
    { width: 1680, height: 1050, weight: 0.08 }, // WSXGA+
    { width: 2560, height: 1440, weight: 0.07 }   // QHD
  ]

  // Weighted random selection
  FUNCTION weighted_choice(items):
    total = items.reduce((sum, item) => sum + item.weight, 0)
    r = Math.random() * total
    cumulative = 0
    FOR item IN items:
      cumulative += item.weight
      IF r <= cumulative:
        RETURN item
    RETURN items[items.length - 1]

  viewport_preset = weighted_choice(VIEWPORT_PRESETS)

  // Add slight variation to viewport
  viewport = {
    width: viewport_preset.width + random_int(-20, 20),
    height: viewport_preset.height + random_int(-20, 20)
  }

  // Timezone/locale combinations (realistic pairings)
  LOCALE_CONFIGS = [
    { timezone: 'America/New_York', locale: 'en-US' },
    { timezone: 'America/Los_Angeles', locale: 'en-US' },
    { timezone: 'America/Chicago', locale: 'en-US' },
    { timezone: 'Europe/London', locale: 'en-GB' },
    { timezone: 'Europe/Berlin', locale: 'de-DE' },
    { timezone: 'Europe/Paris', locale: 'fr-FR' },
    { timezone: 'Asia/Tokyo', locale: 'ja-JP' },
    { timezone: 'Australia/Sydney', locale: 'en-AU' }
  ]

  locale_config = random_choice(LOCALE_CONFIGS)

  // User agent hints (for consistency)
  USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
  ]

  RETURN {
    viewport: viewport,
    timezoneId: locale_config.timezone,
    locale: locale_config.locale,
    userAgent: random_choice(USER_AGENTS),
    // Color scheme preference
    colorScheme: random_choice(['light', 'dark', 'no-preference']),
    // Device scale factor
    deviceScaleFactor: random_choice([1, 1.25, 1.5, 2])
  }
```

---

## Browser Launch Configurations

### Stealth Browser Arguments

```javascript
/**
 * Browser launch arguments for maximum stealth
 * Use with Playwright or Patchright
 */
STEALTH_ARGS = [
  // Core anti-detection
  '--disable-blink-features=AutomationControlled',
  '--disable-features=IsolateOrigins,site-per-process',
  '--disable-site-isolation-trials',

  // Remove automation indicators
  '--no-first-run',
  '--no-default-browser-check',
  '--disable-infobars',
  '--disable-popup-blocking',
  '--disable-notifications',
  '--disable-save-password-bubble',

  // Performance/stability
  '--disable-dev-shm-usage',
  '--disable-accelerated-2d-canvas',
  '--disable-gpu-sandbox',
  '--no-sandbox',  // Required for some environments

  // Privacy/tracking
  '--disable-background-networking',
  '--disable-background-timer-throttling',
  '--disable-backgrounding-occluded-windows',
  '--disable-breakpad',
  '--disable-client-side-phishing-detection',
  '--disable-component-update',
  '--disable-default-apps',
  '--disable-domain-reliability',
  '--disable-extensions',
  '--disable-features=TranslateUI',
  '--disable-hang-monitor',
  '--disable-ipc-flooding-protection',
  '--disable-prompt-on-repost',
  '--disable-renderer-backgrounding',
  '--disable-sync',

  // WebRTC leak prevention
  '--disable-webrtc-hw-encoding',
  '--disable-webrtc-hw-decoding',
  '--enforce-webrtc-ip-permission-check',
  '--force-webrtc-ip-handling-policy=disable_non_proxied_udp',

  // Fingerprint masking
  '--disable-reading-from-canvas',
  '--disable-3d-apis'
]


/**
 * Build complete browser context options
 */
FUNCTION build_stealth_context_options(fingerprint):
  RETURN {
    userDataDir: ".speckit/stitch/session/",
    headless: false,  // Headless mode is easily detected
    viewport: fingerprint.viewport,
    timezoneId: fingerprint.timezoneId,
    locale: fingerprint.locale,
    userAgent: fingerprint.userAgent,
    colorScheme: fingerprint.colorScheme,
    deviceScaleFactor: fingerprint.deviceScaleFactor,
    args: STEALTH_ARGS,
    ignoreDefaultArgs: [
      '--enable-automation',
      '--enable-blink-features=IdleDetection'
    ],
    // Permissions to grant (reduces prompts)
    permissions: ['clipboard-read', 'clipboard-write'],
    // Bypass CSP for some operations
    bypassCSP: true
  }
```

### CDP Connection

```javascript
/**
 * Connect to existing Chrome browser via CDP
 * Requires user to launch Chrome with:
 *   chrome --remote-debugging-port=9222 --user-data-dir="~/.speckit/chrome-profile"
 */
FUNCTION connect_via_cdp(endpoint_url = 'http://localhost:9222'):
  TRY:
    browser = await chromium.connectOverCDP({
      endpointURL: endpoint_url,
      timeout: 10000
    })

    // Verify connection
    contexts = await browser.contexts()
    IF contexts.length === 0:
      // Create new context in connected browser
      context = await browser.newContext()
    ELSE:
      context = contexts[0]

    LOG "Successfully connected to Chrome via CDP"
    RETURN { browser, context, mode: 'cdp' }

  CATCH error:
    LOG "CDP connection failed: {error.message}"
    RETURN null
```

---

## Mode Selection Logic

```javascript
/**
 * Select best available automation mode
 * Priority: CDP → Stealth → Turbo → Assisted
 */
FUNCTION select_stitch_mode(options = {}):
  requested_mode = options.mode OR 'auto'

  IF requested_mode !== 'auto':
    // User explicitly requested a mode
    RETURN requested_mode

  // Auto-selection: try modes in priority order

  // 1. Try CDP connection (best - uses real browser)
  cdp_result = await connect_via_cdp()
  IF cdp_result:
    RETURN { ...cdp_result }

  // 2. Check if Patchright is available (stealth mode)
  TRY:
    patchright = require('patchright')
    RETURN { mode: 'stealth', launcher: patchright }
  CATCH:
    LOG "Patchright not installed, using standard Playwright"

  // 3. Fall back to standard Playwright (turbo mode)
  playwright = require('playwright')
  RETURN { mode: 'turbo', launcher: playwright }


/**
 * Mode detection statistics tracking
 */
FUNCTION track_mode_result(mode, success, error = null):
  stats_file = '.speckit/stitch/mode-history.json'

  stats = LOAD stats_file OR {
    cdp: { attempts: 0, successes: 0, failures: 0 },
    stealth: { attempts: 0, successes: 0, failures: 0 },
    turbo: { attempts: 0, successes: 0, failures: 0 },
    assisted: { attempts: 0, successes: 0, failures: 0 }
  }

  stats[mode].attempts++
  IF success:
    stats[mode].successes++
  ELSE:
    stats[mode].failures++
    stats[mode].last_error = error?.message

  SAVE stats_file, stats
```

---

## Detection Response Handlers

### CAPTCHA Detection

```javascript
/**
 * Detect if CAPTCHA is present on page
 */
FUNCTION detect_captcha(page):
  captcha_selectors = [
    'iframe[src*="recaptcha"]',
    'iframe[src*="hcaptcha"]',
    '.g-recaptcha',
    '[data-sitekey]',
    'iframe[title*="reCAPTCHA"]',
    '#captcha',
    '.captcha-container'
  ]

  FOR selector IN captcha_selectors:
    element = await page.$(selector)
    IF element:
      RETURN { detected: true, type: selector }

  RETURN { detected: false }


/**
 * Handle CAPTCHA detection
 * Options: wait for user, switch to assisted mode, or fail
 */
FUNCTION handle_captcha(page, options = {}):
  action = options.action OR 'prompt'

  IF action === 'prompt':
    LOG "⚠️ CAPTCHA detected. Please solve it manually in the browser."
    LOG "Press Enter when done..."

    // Wait for CAPTCHA to disappear (user solved it)
    await wait_for_captcha_solved(page, { timeout: 300000 })  // 5 min

  ELIF action === 'switch':
    LOG "CAPTCHA detected. Switching to assisted mode."
    THROW { code: 'CAPTCHA_DETECTED', switch_mode: 'assisted' }

  ELSE:
    THROW Error("CAPTCHA detected and could not be bypassed")


FUNCTION wait_for_captcha_solved(page, options = {}):
  timeout = options.timeout OR 300000
  check_interval = 2000

  start_time = Date.now()
  WHILE Date.now() - start_time < timeout:
    captcha = await detect_captcha(page)
    IF NOT captcha.detected:
      LOG "CAPTCHA solved, continuing..."
      RETURN
    await sleep(check_interval)

  THROW Error("CAPTCHA solve timeout")
```

### Rate Limit Detection

```javascript
/**
 * Detect rate limit messages on page
 */
FUNCTION detect_rate_limit(page):
  rate_limit_patterns = [
    'rate limit',
    'too many requests',
    'quota exceeded',
    'try again later',
    'slow down',
    '429'
  ]

  page_text = await page.evaluate(() => document.body.innerText.toLowerCase())

  FOR pattern IN rate_limit_patterns:
    IF pattern IN page_text:
      RETURN { detected: true, pattern: pattern }

  RETURN { detected: false }


/**
 * Handle rate limit detection
 */
FUNCTION handle_rate_limit(options = {}):
  wait_time = options.wait_time OR 60000  // 1 minute default

  LOG "⚠️ Rate limit detected. Waiting {wait_time/1000}s before retry..."
  await sleep(wait_time)

  // Exponential backoff for subsequent hits
  RETURN wait_time * 2
```

---

## Session Management

```javascript
/**
 * Validate existing session is still authenticated
 */
FUNCTION validate_session(page):
  // Navigate to Stitch
  await page.goto('https://stitch.withgoogle.com', {
    waitUntil: 'networkidle'
  })

  await random_wait(1000, 2000)

  // Check for authenticated indicators
  auth_selectors = [
    '[data-user-avatar]',
    '.user-avatar',
    'img[alt*="profile"]',
    '[aria-label*="Account"]'
  ]

  FOR selector IN auth_selectors:
    element = await page.$(selector)
    IF element:
      RETURN { valid: true, indicator: selector }

  // Check for sign-in button (indicates not authenticated)
  sign_in = await page.$('button:has-text("Sign in")')
  IF sign_in:
    RETURN { valid: false, reason: 'sign_in_required' }

  // Uncertain state
  RETURN { valid: false, reason: 'unknown' }


/**
 * Clear and reset session data
 */
FUNCTION reset_session():
  session_dir = '.speckit/stitch/session/'

  IF EXISTS session_dir:
    REMOVE_DIR session_dir
    LOG "Session data cleared"

  CREATE_DIR session_dir
```

---

## Export Functions

```javascript
/**
 * Export module functions for use in stitch-integration.md
 */
MODULE_EXPORTS = {
  // Utility functions
  gaussian_random,
  exponential_random,
  clamp,
  random_int,
  random_float,
  random_choice,
  ease_in_out_cubic,
  lerp,
  bezier_curve,
  fitts_time,
  distance,

  // Humanization functions
  humanize_typing,
  move_and_click,
  move_and_double_click,
  random_wait,
  wait_short,
  wait_medium,
  wait_long,
  wait_page_load,
  scroll_to_element,
  smooth_viewport_resize,

  // Fingerprint & browser
  generate_fingerprint,
  STEALTH_ARGS,
  build_stealth_context_options,
  connect_via_cdp,

  // Mode selection
  select_stitch_mode,
  track_mode_result,

  // Detection handlers
  detect_captcha,
  handle_captcha,
  wait_for_captcha_solved,
  detect_rate_limit,
  handle_rate_limit,

  // Session management
  validate_session,
  reset_session
}
```

---

## Usage Example

```javascript
// Example: Full humanized Stitch interaction

IMPORT * FROM 'stitch-anti-detection.md'

ASYNC FUNCTION generate_mockup(prompt):
  // 1. Select mode and launch browser
  mode_config = await select_stitch_mode()

  IF mode_config.mode === 'cdp':
    { context } = mode_config
  ELSE:
    fingerprint = generate_fingerprint()
    options = build_stealth_context_options(fingerprint)
    context = await mode_config.launcher.chromium.launchPersistentContext(options)

  page = await context.newPage()

  // 2. Navigate and validate session
  session = await validate_session(page)
  IF NOT session.valid:
    LOG "Please sign in to Google Stitch..."
    // Wait for manual sign-in
    await page.waitForSelector('[data-user-avatar]', { timeout: 300000 })

  // 3. Find and interact with prompt input
  prompt_input = await page.$('textarea[placeholder*="Describe"]')
  await scroll_to_element(page, prompt_input)
  await move_and_click(page, prompt_input)
  await humanize_typing(prompt_input, prompt)

  // 4. Click generate with human-like behavior
  generate_btn = await page.$('button:has-text("Generate")')
  await move_and_click(page, generate_btn)

  // 5. Wait for generation with random delay
  await page.waitForSelector('.preview-container', { timeout: 60000 })
  await random_wait(2000, 4000)

  // 6. Check for issues
  captcha = await detect_captcha(page)
  IF captcha.detected:
    await handle_captcha(page)

  rate_limit = await detect_rate_limit(page)
  IF rate_limit.detected:
    await handle_rate_limit()
    // Retry logic...

  // 7. Export result
  // ... (see stitch-integration.md for export logic)

  track_mode_result(mode_config.mode, true)
```

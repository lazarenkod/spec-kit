# Stitch Debugging Utilities

Debugging and diagnostic tools for Google Stitch UI automation.
Helps identify and troubleshoot selector failures when Google updates their UI.

---

## Overview

This module provides utilities for:
- **Selector Testing**: Test individual selectors against live Stitch UI
- **Selector Auditing**: Test all selectors at once with summary report
- **Element Inspection**: Get detailed DOM information about elements
- **Debug Screenshots**: Capture screenshots when selectors fail

---

## Core Functions

### 1. Test Single Selector

```pseudocode
FUNCTION test_selector(page, selector_name, selector_config):
  """
  Test all selector variants (primary + fallbacks) and report which ones work.
  Useful for debugging when specific selectors break.

  Args:
    page: Playwright page object
    selector_name: String identifier (e.g., "promptInput")
    selector_config: Selector configuration object with primary/fallbacks

  Returns:
    { success: boolean, working_selector: string|null, attempted: number }
  """

  LOG "🔍 Testing selector: {selector_name}"
  LOG "   Description: {selector_config.description}"
  LOG "   Required: {selector_config.required ? 'YES' : 'NO'}"

  attempted_count = 0

  # Test primary selector
  attempted_count += 1
  LOG "   Trying PRIMARY [{attempted_count}]: {selector_config.primary}"

  element = await page.$(selector_config.primary)
  IF element:
    LOG "   ✅ PRIMARY works: {selector_config.primary}"
    RETURN {
      success: true,
      working_selector: selector_config.primary,
      selector_type: 'primary',
      attempted: attempted_count
    }
  ELSE:
    LOG "   ❌ PRIMARY failed"

  # Test fallback selectors
  FOR each fallback, index IN selector_config.fallbacks:
    attempted_count += 1
    LOG "   Trying FALLBACK [{attempted_count}]: {fallback}"

    element = await page.$(fallback)
    IF element:
      LOG "   ✅ FALLBACK {index + 1} works: {fallback}"
      RETURN {
        success: true,
        working_selector: fallback,
        selector_type: 'fallback',
        fallback_index: index + 1,
        attempted: attempted_count
      }
    ELSE:
      LOG "   ❌ FALLBACK {index + 1} failed"

  # All selectors failed
  LOG "   ❌ ALL SELECTORS FAILED ({attempted_count} variants tried)"

  # Take debug screenshot for failed selector
  screenshot_dir = ".speckit/debug/selector-failures"
  ENSURE_DIRECTORY_EXISTS(screenshot_dir)

  screenshot_path = "{screenshot_dir}/{selector_name}-{TIMESTAMP}.png"

  TRY:
    await page.screenshot({
      path: screenshot_path,
      fullPage: true
    })
    LOG "   📸 Screenshot saved: {screenshot_path}"
  CATCH error:
    LOG "   ⚠️ Could not save screenshot: {error.message}"

  RETURN {
    success: false,
    working_selector: null,
    attempted: attempted_count,
    screenshot: screenshot_path
  }
```

---

### 2. Audit All Selectors

```pseudocode
FUNCTION audit_all_selectors(page, options = {}):
  """
  Test all selectors in SELECTORS config and generate comprehensive report.

  Args:
    page: Playwright page object
    options: {
      verbose: boolean (default: true) - Show detailed output per selector
      screenshot_failures: boolean (default: true) - Capture screenshots for failures
      categories: array|null - Only test specific categories (e.g., ['authentication', 'export'])
    }

  Returns:
    {
      total: number,
      working: number,
      broken: number,
      results: object,
      summary: object
    }
  """

  # Header
  LOG ""
  LOG "╔══════════════════════════════════════════════════════════════════╗"
  LOG "║  STITCH SELECTOR AUDIT - {CURRENT_TIMESTAMP}                      ║"
  LOG "╚══════════════════════════════════════════════════════════════════╝"
  LOG ""

  results = {}
  categories_tested = {}

  # Get selectors to test
  selectors_to_test = SELECTORS
  IF options.categories:
    selectors_to_test = FILTER_BY_CATEGORIES(SELECTORS, options.categories)

  # Test each selector
  FOR each selector_name, selector_config IN selectors_to_test:
    category = selector_config.category OR 'uncategorized'

    IF NOT categories_tested[category]:
      categories_tested[category] = { working: 0, broken: 0, total: 0 }

    IF options.verbose:
      LOG "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Test the selector
    result = test_selector(page, selector_name, selector_config)

    # Store result
    results[selector_name] = {
      ...result,
      category: category,
      description: selector_config.description,
      required: selector_config.required
    }

    # Update category stats
    categories_tested[category].total += 1
    IF result.success:
      categories_tested[category].working += 1
    ELSE:
      categories_tested[category].broken += 1

    IF options.verbose:
      LOG ""

  # Calculate totals
  total = Object.keys(results).length
  working = Object.values(results).filter(r => r.success).length
  broken = total - working

  # Summary Report
  LOG ""
  LOG "╔══════════════════════════════════════════════════════════════════╗"
  LOG "║  AUDIT SUMMARY                                                   ║"
  LOG "╠══════════════════════════════════════════════════════════════════╣"
  LOG "║  Total Selectors Tested: {total}                                  ║"
  LOG "║  ✅ Working: {working} ({PERCENTAGE(working, total)}%)             ║"
  LOG "║  ❌ Broken:  {broken} ({PERCENTAGE(broken, total)}%)               ║"
  LOG "╚══════════════════════════════════════════════════════════════════╝"
  LOG ""

  # Category Breakdown
  IF Object.keys(categories_tested).length > 1:
    LOG "📊 Breakdown by Category:"
    LOG ""
    FOR each category, stats IN categories_tested:
      status_icon = stats.broken === 0 ? "✅" : "⚠️"
      LOG "  {status_icon} {category}:"
      LOG "     Working: {stats.working}/{stats.total}"
      IF stats.broken > 0:
        LOG "     Broken:  {stats.broken}/{stats.total}"
    LOG ""

  # List broken selectors if any
  IF broken > 0:
    LOG "❌ Broken Selectors (require update):"
    LOG ""

    FOR each selector_name, result IN results:
      IF NOT result.success:
        required_badge = result.required ? "[REQUIRED]" : "[OPTIONAL]"
        LOG "  • {selector_name} {required_badge}"
        LOG "    Category: {result.category}"
        LOG "    Description: {result.description}"
        LOG "    Variants tried: {result.attempted}"
        IF result.screenshot:
          LOG "    Screenshot: {result.screenshot}"
        LOG ""
  ELSE:
    LOG "🎉 All selectors working correctly!"

  LOG ""
  LOG "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  LOG ""

  RETURN {
    total: total,
    working: working,
    broken: broken,
    results: results,
    categories: categories_tested,
    summary: {
      success_rate: PERCENTAGE(working, total),
      all_working: broken === 0,
      critical_failures: Object.values(results).filter(r => !r.success && r.required).length
    }
  }
```

---

### 3. Inspect Element

```pseudocode
FUNCTION inspect_element_at_selector(page, selector, options = {}):
  """
  Get detailed DOM information about an element found by a selector.
  Useful for discovering new selector patterns after UI changes.

  Args:
    page: Playwright page object
    selector: CSS/XPath selector string
    options: {
      show_computed_styles: boolean (default: false)
      show_bounding_box: boolean (default: true)
      screenshot: boolean (default: false)
    }

  Returns:
    {
      found: boolean,
      tag: string,
      id: string,
      classes: array,
      attributes: object,
      text_content: string,
      bounding_box: object,
      computed_styles: object|null,
      screenshot_path: string|null
    }
  """

  LOG "🔎 Inspecting element: {selector}"
  LOG ""

  # Find element
  element = await page.$(selector)

  IF NOT element:
    LOG "❌ Element not found with selector: {selector}"
    RETURN {
      found: false,
      selector: selector
    }

  # Get basic info
  tag = await element.evaluate(el => el.tagName.toLowerCase())
  id = await element.evaluate(el => el.id)
  class_name = await element.evaluate(el => el.className)
  classes = class_name ? class_name.split(/\s+/).filter(c => c) : []

  # Get all attributes
  attributes = await element.evaluate(el => {
    const attrs = {}
    for (const attr of el.attributes) {
      attrs[attr.name] = attr.value
    }
    return attrs
  })

  # Get text content (truncated)
  text_content = await element.evaluate(el => el.textContent.trim())
  IF text_content.length > 100:
    text_content = text_content.substring(0, 100) + "..."

  # Get bounding box
  bounding_box = null
  IF options.show_bounding_box !== false:
    bounding_box = await element.boundingBox()

  # Get computed styles (if requested)
  computed_styles = null
  IF options.show_computed_styles:
    computed_styles = await element.evaluate(el => {
      const computed = window.getComputedStyle(el)
      return {
        display: computed.display,
        visibility: computed.visibility,
        opacity: computed.opacity,
        position: computed.position,
        z_index: computed.zIndex,
        width: computed.width,
        height: computed.height
      }
    })

  # Take screenshot (if requested)
  screenshot_path = null
  IF options.screenshot:
    screenshot_dir = ".speckit/debug/element-inspection"
    ENSURE_DIRECTORY_EXISTS(screenshot_dir)
    screenshot_path = "{screenshot_dir}/element-{TIMESTAMP}.png"

    TRY:
      await element.screenshot({ path: screenshot_path })
      LOG "📸 Element screenshot saved: {screenshot_path}"
    CATCH error:
      LOG "⚠️ Could not save element screenshot: {error.message}"

  # Display info
  LOG "✅ Element found!"
  LOG ""
  LOG "Tag:        <{tag}>"
  LOG "ID:         {id || '(none)'}"
  LOG "Classes:    {classes.length > 0 ? classes.join(', ') : '(none)'}"
  LOG ""

  LOG "Attributes:"
  FOR each attr_name, attr_value IN attributes:
    # Truncate long attribute values
    display_value = attr_value
    IF attr_value.length > 80:
      display_value = attr_value.substring(0, 80) + "..."
    LOG "  {attr_name} = \"{display_value}\""
  LOG ""

  IF text_content:
    LOG "Text Content: \"{text_content}\""
    LOG ""

  IF bounding_box:
    LOG "Bounding Box:"
    LOG "  x: {bounding_box.x}px, y: {bounding_box.y}px"
    LOG "  width: {bounding_box.width}px, height: {bounding_box.height}px"
    LOG ""

  IF computed_styles:
    LOG "Computed Styles:"
    FOR each style_name, style_value IN computed_styles:
      LOG "  {style_name}: {style_value}"
    LOG ""

  # Suggest selectors
  LOG "💡 Suggested Selectors:"
  suggested_selectors = []

  # By ID
  IF id:
    suggested_selectors.push("#{id}")

  # By classes (most specific combinations)
  IF classes.length > 0:
    # Single class
    FOR each class IN classes:
      suggested_selectors.push(".{class}")

    # Tag + class
    IF classes.length > 0:
      suggested_selectors.push("{tag}.{classes[0]}")

    # Multiple classes (up to 3)
    IF classes.length >= 2:
      suggested_selectors.push(".{classes[0]}.{classes[1]}")

  # By tag
  suggested_selectors.push(tag)

  # By attributes
  IF attributes['data-testid']:
    suggested_selectors.push("[data-testid='{attributes['data-testid']}']")
  IF attributes['aria-label']:
    suggested_selectors.push("[aria-label*='{attributes['aria-label'].substring(0, 20)}']")
  IF attributes['placeholder']:
    suggested_selectors.push("[placeholder*='{attributes['placeholder'].substring(0, 20)}']")
  IF attributes['name']:
    suggested_selectors.push("[name='{attributes['name']}']")

  FOR each selector IN suggested_selectors:
    LOG "  • {selector}"
  LOG ""

  RETURN {
    found: true,
    selector: selector,
    tag: tag,
    id: id,
    classes: classes,
    attributes: attributes,
    text_content: text_content,
    bounding_box: bounding_box,
    computed_styles: computed_styles,
    screenshot_path: screenshot_path,
    suggested_selectors: suggested_selectors
  }
```

---

### 4. Interactive Selector Explorer

```pseudocode
FUNCTION explore_selectors_interactively(page):
  """
  Interactive mode for exploring Stitch UI and discovering new selectors.
  Allows clicking elements and seeing their selector info.

  This is useful when Google updates their UI and you need to find new selectors.

  Args:
    page: Playwright page object

  Usage:
    1. Run this function
    2. Click on elements in the browser
    3. See suggested selectors in console
    4. Press 'q' to quit
  """

  LOG "🎯 Interactive Selector Explorer"
  LOG ""
  LOG "Instructions:"
  LOG "  • Click any element on the page to inspect it"
  LOG "  • Suggested selectors will appear in console"
  LOG "  • Press ESC or 'q' to quit"
  LOG ""
  LOG "Starting in 3 seconds..."
  await SLEEP(3000)

  # Inject click handler into page
  await page.evaluate(() => {
    window.__selectorExplorerActive = true

    document.addEventListener('click', (event) => {
      if (!window.__selectorExplorerActive) return

      event.preventDefault()
      event.stopPropagation()

      const element = event.target

      # Send element info back to Node.js context
      window.__lastClickedElement = element
      window.__lastClickedElementInfo = {
        tagName: element.tagName.toLowerCase(),
        id: element.id,
        className: element.className,
        textContent: element.textContent.trim().substring(0, 50)
      }
    }, true)

    # ESC key listener
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' || event.key === 'q') {
        window.__selectorExplorerActive = false
        console.log('Selector explorer deactivated')
      }
    })
  })

  LOG "✅ Explorer active! Click elements to inspect them."
  LOG ""

  # Poll for clicked elements
  WHILE true:
    await SLEEP(500)

    # Check if still active
    is_active = await page.evaluate(() => window.__selectorExplorerActive)
    IF NOT is_active:
      LOG ""
      LOG "👋 Explorer deactivated. Exiting..."
      BREAK

    # Check for clicked element
    element_info = await page.evaluate(() => {
      const info = window.__lastClickedElementInfo
      window.__lastClickedElementInfo = null
      return info
    })

    IF element_info:
      LOG "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      LOG "Clicked: <{element_info.tagName}> \"{element_info.textContent}\""
      LOG ""

      # Build selector from element info
      selector = element_info.tagName
      IF element_info.id:
        selector = "#{element_info.id}"
      ELSE IF element_info.className:
        first_class = element_info.className.split(/\s+/)[0]
        IF first_class:
          selector = ".{first_class}"

      # Inspect the element
      await inspect_element_at_selector(page, selector, {
        show_bounding_box: true,
        show_computed_styles: false
      })
```

---

## Helper Functions

### Ensure Directory Exists

```pseudocode
FUNCTION ENSURE_DIRECTORY_EXISTS(dir_path):
  """Create directory if it doesn't exist"""
  TRY:
    fs.mkdirSync(dir_path, { recursive: true })
  CATCH error:
    # Ignore if already exists
    IF error.code !== 'EEXIST':
      THROW error
```

### Calculate Percentage

```pseudocode
FUNCTION PERCENTAGE(part, total):
  """Calculate percentage and format to 1 decimal place"""
  IF total === 0:
    RETURN "0.0"
  RETURN ((part / total) * 100).toFixed(1)
```

### Get Timestamp

```pseudocode
FUNCTION CURRENT_TIMESTAMP():
  """Get current timestamp in ISO format"""
  RETURN new Date().toISOString()
```

### Timestamp for Filenames

```pseudocode
FUNCTION TIMESTAMP():
  """Get timestamp suitable for filenames (no colons)"""
  RETURN new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '')
```

---

## Usage Examples

### Example 1: Test Single Selector

```javascript
# Test if promptInput selector works
const result = await test_selector(page, 'promptInput', SELECTORS.promptInput)

if (result.success) {
  console.log(`Selector works: ${result.working_selector}`)
} else {
  console.log('Selector broken, check screenshot at:', result.screenshot)
}
```

### Example 2: Full Audit

```javascript
# Audit all selectors
const audit = await audit_all_selectors(page, {
  verbose: true,
  screenshot_failures: true
})

if (audit.summary.all_working) {
  console.log('All selectors working!')
} else {
  console.log(`${audit.broken} selectors need updating`)
}
```

### Example 3: Inspect Specific Element

```javascript
# Inspect the prompt input field
const info = await inspect_element_at_selector(
  page,
  'textarea[placeholder*="Describe"]',
  {
    show_computed_styles: true,
    screenshot: true
  }
)

if (info.found) {
  console.log('Suggested selectors:', info.suggested_selectors)
}
```

### Example 4: Discover New Selectors After UI Change

```javascript
# When Google updates Stitch UI, use this to find new selectors
await page.goto('https://stitch.withgoogle.com')
await explore_selectors_interactively(page)

# Click elements in browser to see their selector info
# Use suggested selectors to update stitch-selectors.md
```

---

## Integration with Main Workflow

### Debug Mode Integration

In `stitch-integration.md`, add this at the beginning:

```javascript
# If debug mode enabled, run full selector audit before proceeding
IF options.debug:
  LOG "🐛 Debug mode enabled - running selector audit..."

  IMPORT * FROM templates/shared/stitch-debug-utils.md

  audit_result = await audit_all_selectors(page, {
    verbose: options.log_level === 'debug',
    screenshot_failures: true
  })

  IF audit_result.summary.critical_failures > 0:
    LOG "⚠️ WARNING: {audit_result.summary.critical_failures} required selectors are broken!"
    LOG "This may cause mockup generation to fail."
    LOG ""

    IF NOT options.force:
      THROW Error("Critical selectors broken. Fix selectors or use --force to continue anyway.")
```

### Audit-Only Mode Integration

In `stitch-integration.md`, add this as early exit option:

```javascript
# If audit-selectors flag set, just run audit and exit
IF options.audit_selectors:
  LOG "Running selector audit mode (no mockup generation)..."
  LOG ""

  # Setup browser and authenticate
  { browser, page } = await stitch_setup_browser(options)
  await stitch_authenticate(browser, page)

  # Run audit
  IMPORT audit_all_selectors FROM templates/shared/stitch-debug-utils.md

  audit_result = await audit_all_selectors(page, {
    verbose: true,
    screenshot_failures: true,
    categories: options.audit_categories  # Optional: filter by category
  })

  # Cleanup
  await browser.close()

  # Return audit results (don't generate mockups)
  RETURN {
    mode: 'audit',
    audit_results: audit_result,
    success: audit_result.summary.all_working
  }
```

---

## Maintenance Notes

When updating this module:

1. **Add new debugging tools** as helper functions
2. **Keep output format consistent** for easy parsing
3. **Include timestamps** in all log outputs for troubleshooting
4. **Save debug artifacts** (.speckit/debug/) for offline analysis
5. **Test with real Stitch UI** after each change

When Google updates Stitch UI:

1. Run `--audit-selectors` to identify broken selectors
2. Use `explore_selectors_interactively()` to discover new patterns
3. Update `stitch-selectors.md` with new selectors
4. Run audit again to verify fixes
5. Update version history in stitch-selectors.md

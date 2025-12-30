# Stitch DOM Selectors

> Versioned DOM selectors for Google Stitch browser automation. Update this file when Stitch UI changes.

## Selector Registry

| Version | Last Verified | Status |
|---------|---------------|--------|
| 1.0.0 | 2025-01-01 | Current |

---

## Selector Definitions

### Authentication

```javascript
SELECTORS.auth = {
  // Sign in button on landing/unauthenticated page
  signInButton: {
    primary: 'button:has-text("Sign in with Google")',
    fallbacks: [
      'button:has-text("Sign in")',
      '[data-action="sign-in"]',
      'a[href*="accounts.google.com"]',
      '.sign-in-button',
      'button[aria-label*="Sign in"]'
    ],
    description: 'Google OAuth sign-in button',
    required: true
  },

  // Indicator that user is authenticated and workspace is loaded
  workspaceLoaded: {
    primary: '[data-workspace]',
    fallbacks: [
      '.workspace',
      '.app-container',
      'main[role="main"]',
      '.design-canvas',
      '[data-testid="workspace"]',
      '.prompt-input-container'
    ],
    description: 'Main workspace container indicating successful auth',
    required: true,
    timeout: 300000  // 5 minutes for OAuth flow
  },

  // User profile/avatar indicating logged in state
  userAvatar: {
    primary: '[data-user-avatar]',
    fallbacks: [
      '.user-avatar',
      'img[alt*="profile"]',
      '[aria-label*="Account"]',
      '.account-button'
    ],
    description: 'User avatar/account button',
    required: false
  }
}
```

### Prompt Input

```javascript
SELECTORS.input = {
  // Main prompt input textarea
  promptInput: {
    primary: 'textarea[placeholder*="Describe"]',
    fallbacks: [
      '.prompt-input',
      '[data-testid="prompt-input"]',
      'textarea[aria-label*="prompt"]',
      'textarea[name="prompt"]',
      '.input-area textarea',
      '[contenteditable="true"].prompt'
    ],
    description: 'Main prompt input textarea',
    required: true,
    timeout: 10000
  },

  // Generate/Submit button
  generateButton: {
    primary: 'button:has-text("Generate")',
    fallbacks: [
      '[data-action="generate"]',
      'button[type="submit"]',
      '.generate-button',
      'button:has-text("Create")',
      'button[aria-label*="Generate"]',
      '[data-testid="generate-button"]'
    ],
    description: 'Button to submit prompt and generate design',
    required: true,
    timeout: 5000
  },

  // Character/token counter
  charCounter: {
    primary: '.char-counter',
    fallbacks: [
      '[data-char-count]',
      '.token-count',
      '.prompt-length'
    ],
    description: 'Prompt length indicator',
    required: false
  },

  // Clear/reset prompt button
  clearButton: {
    primary: 'button:has-text("Clear")',
    fallbacks: [
      '[aria-label*="Clear"]',
      '.clear-prompt',
      'button:has(svg[data-icon="x"])'
    ],
    description: 'Button to clear prompt input',
    required: false
  }
}
```

### Loading States

```javascript
SELECTORS.loading = {
  // Loading indicator while generating
  loadingSpinner: {
    primary: '[data-loading="true"]',
    fallbacks: [
      '.loading-indicator',
      '[aria-busy="true"]',
      '.spinner',
      '.generating',
      '[data-state="loading"]',
      '.progress-indicator',
      'svg.animate-spin'
    ],
    description: 'Loading spinner during generation',
    required: false,  // May not catch it if generation is fast
    timeout: 5000
  },

  // Generation complete indicator
  loadingComplete: {
    primary: '.preview-container',
    fallbacks: [
      '[data-preview]',
      '.design-canvas',
      'canvas',
      '.generated-design',
      '[data-state="complete"]',
      '.preview-frame'
    ],
    description: 'Indicator that generation completed successfully',
    required: true,
    timeout: 60000  // Max generation time
  },

  // Generation progress text
  progressText: {
    primary: '.generation-progress',
    fallbacks: [
      '[data-progress-text]',
      '.status-text',
      '.generating-text'
    ],
    description: 'Text showing generation progress',
    required: false
  }
}
```

### Preview/Canvas

```javascript
SELECTORS.preview = {
  // Main preview container
  previewCanvas: {
    primary: '.preview-container',
    fallbacks: [
      '[data-preview]',
      '.design-canvas',
      '.preview-area',
      '[data-testid="preview"]',
      '.generated-output'
    ],
    description: 'Container holding the generated design preview',
    required: true
  },

  // Preview iframe (if design is rendered in iframe)
  previewFrame: {
    primary: 'iframe.preview-frame',
    fallbacks: [
      'iframe[data-preview]',
      '.preview-container iframe',
      'iframe[title*="preview"]',
      'iframe[name="preview"]'
    ],
    description: 'Iframe containing rendered preview',
    required: false  // Not all designs use iframe
  },

  // Preview viewport controls
  viewportSelector: {
    primary: '[data-viewport-selector]',
    fallbacks: [
      '.viewport-controls',
      '.device-selector',
      'button:has-text("Desktop")',
      'button:has-text("Mobile")'
    ],
    description: 'Viewport size selector (desktop/tablet/mobile)',
    required: false
  },

  // Zoom controls
  zoomControl: {
    primary: '[data-zoom]',
    fallbacks: [
      '.zoom-control',
      'input[type="range"][aria-label*="zoom"]',
      '.zoom-slider'
    ],
    description: 'Zoom level control for preview',
    required: false
  }
}
```

### Export Panel

```javascript
SELECTORS.export = {
  // Main export button to open export panel
  exportButton: {
    primary: 'button:has-text("Export")',
    fallbacks: [
      '[aria-label*="Export"]',
      'button:has-text("Code")',
      '.export-button',
      '[data-action="export"]',
      'button:has(svg[data-icon="download"])',
      'button:has(svg[data-icon="code"])'
    ],
    description: 'Button to open export options',
    required: true,
    timeout: 5000
  },

  // Code/HTML tab in export panel
  codeTab: {
    primary: '[data-tab="code"]',
    fallbacks: [
      'button:has-text("Code")',
      '[role="tab"]:has-text("Code")',
      '.tab-code',
      '[aria-controls*="code"]'
    ],
    description: 'Tab to switch to code export view',
    required: false  // May be default view
  },

  // HTML export option
  htmlOption: {
    primary: 'button:has-text("HTML")',
    fallbacks: [
      '[data-format="html"]',
      '[data-export-type="html"]',
      'option:has-text("HTML")',
      '[value="html"]'
    ],
    description: 'Option to export as HTML',
    required: true
  },

  // Tailwind export option
  tailwindOption: {
    primary: 'button:has-text("Tailwind")',
    fallbacks: [
      '[data-format="tailwind"]',
      '[data-export-type="tailwind"]',
      'option:has-text("Tailwind")',
      '[value="tailwind"]'
    ],
    description: 'Option to export as Tailwind CSS',
    required: false  // Preferred but not always available
  },

  // Copy to clipboard button
  copyButton: {
    primary: 'button:has-text("Copy")',
    fallbacks: [
      '[aria-label*="Copy"]',
      '[data-action="copy"]',
      '.copy-button',
      'button:has(svg[data-icon="clipboard"])',
      'button:has(svg[data-icon="copy"])'
    ],
    description: 'Button to copy code to clipboard',
    required: true
  },

  // Code output element (where code is displayed)
  codeOutput: {
    primary: 'pre code',
    fallbacks: [
      '.code-output',
      '[data-code]',
      'pre.highlight',
      '.prism-code',
      'code.language-html',
      '.monaco-editor',
      'textarea[readonly]'
    ],
    description: 'Element containing the generated code',
    required: true
  },

  // Figma export button
  figmaButton: {
    primary: 'button:has-text("Copy to Figma")',
    fallbacks: [
      'button:has-text("Figma")',
      '[aria-label*="Figma"]',
      '[data-action="figma-export"]',
      '.figma-export-button',
      'button:has(svg[data-icon="figma"])'
    ],
    description: 'Button to copy design for Figma import',
    required: false  // May not be available for all designs
  },

  // Download button (for assets)
  downloadButton: {
    primary: 'button:has-text("Download")',
    fallbacks: [
      '[aria-label*="Download"]',
      '[data-action="download"]',
      'a[download]',
      '.download-button'
    ],
    description: 'Button to download generated assets',
    required: false
  },

  // Close export panel
  closeExport: {
    primary: 'button[aria-label="Close"]',
    fallbacks: [
      '[data-action="close"]',
      '.modal-close',
      'button:has(svg[data-icon="x"])',
      '.close-button'
    ],
    description: 'Button to close export panel/modal',
    required: false
  }
}
```

### Error States

```javascript
SELECTORS.error = {
  // Error message container
  errorMessage: {
    primary: '.error-message',
    fallbacks: [
      '[role="alert"]',
      '.toast-error',
      '[data-type="error"]',
      '.error-toast',
      '.notification-error',
      '[aria-live="assertive"]:has-text("error")'
    ],
    description: 'Error message display element',
    required: false
  },

  // Rate limit warning
  rateLimitWarning: {
    primary: ':has-text("rate limit")',
    fallbacks: [
      ':has-text("quota")',
      ':has-text("too many requests")',
      '.rate-limit-message',
      '[data-error="rate-limit"]'
    ],
    description: 'Rate limit exceeded message',
    required: false
  },

  // CAPTCHA container
  captchaContainer: {
    primary: 'iframe[src*="recaptcha"]',
    fallbacks: [
      '.g-recaptcha',
      '[data-sitekey]',
      'iframe[title*="reCAPTCHA"]',
      '.captcha-container'
    ],
    description: 'CAPTCHA challenge container',
    required: false
  },

  // Retry button on error
  retryButton: {
    primary: 'button:has-text("Retry")',
    fallbacks: [
      'button:has-text("Try again")',
      '[data-action="retry"]',
      '.retry-button'
    ],
    description: 'Button to retry failed operation',
    required: false
  }
}
```

### Navigation

```javascript
SELECTORS.nav = {
  // New design button
  newDesignButton: {
    primary: 'button:has-text("New")',
    fallbacks: [
      '[data-action="new-design"]',
      'button:has-text("Create new")',
      '.new-design-button',
      'button:has(svg[data-icon="plus"])'
    ],
    description: 'Button to start new design',
    required: false
  },

  // History/previous designs
  historyButton: {
    primary: 'button:has-text("History")',
    fallbacks: [
      '[data-action="history"]',
      '.history-button',
      'button:has-text("Recent")'
    ],
    description: 'Button to view previous generations',
    required: false
  },

  // Settings menu
  settingsButton: {
    primary: 'button[aria-label="Settings"]',
    fallbacks: [
      '[data-action="settings"]',
      '.settings-button',
      'button:has(svg[data-icon="settings"])'
    ],
    description: 'Settings/preferences button',
    required: false
  }
}
```

---

## Selector Utility Functions

```javascript
/**
 * Try to find element using primary selector, falling back to alternatives
 */
FUNCTION findElement(page, selectorConfig):

  // Try primary selector first
  element = await page.$(selectorConfig.primary)
  IF element:
    RETURN element

  // Try fallbacks in order
  FOR each fallback IN selectorConfig.fallbacks:
    element = await page.$(fallback)
    IF element:
      LOG "Used fallback selector: {fallback} for {selectorConfig.description}"
      RETURN element

  // No element found
  IF selectorConfig.required:
    THROW Error("Required element not found: {selectorConfig.description}")

  RETURN null


/**
 * Wait for element with timeout, trying all selectors
 */
FUNCTION waitForElement(page, selectorConfig, options = {}):

  timeout = options.timeout OR selectorConfig.timeout OR 10000
  state = options.state OR "visible"

  // Build combined selector for waiting
  allSelectors = [selectorConfig.primary, ...selectorConfig.fallbacks]
  combinedSelector = allSelectors.join(", ")

  TRY:
    element = await page.waitForSelector(combinedSelector, {
      timeout: timeout,
      state: state
    })
    RETURN element
  CATCH error:
    IF selectorConfig.required:
      THROW Error("Timeout waiting for: {selectorConfig.description}")
    RETURN null


/**
 * Check if any selector matches (for condition checking)
 */
FUNCTION elementExists(page, selectorConfig):

  allSelectors = [selectorConfig.primary, ...selectorConfig.fallbacks]

  FOR each selector IN allSelectors:
    count = await page.locator(selector).count()
    IF count > 0:
      RETURN true

  RETURN false
```

---

## Version History

### v1.0.0 (2025-01-01)

Initial selector definitions based on Stitch UI as of January 2025.

**Known UI patterns:**
- Single-page application
- React-based interface
- Material Design inspired components
- Modal-based export panel
- Iframe-based preview rendering

**Verified working:**
- Authentication flow
- Prompt input and submission
- Basic export (HTML/Tailwind)
- Screenshot capture from canvas

**Untested/uncertain:**
- Figma export (feature availability varies)
- Experimental mode selectors
- Mobile/tablet viewport selectors

---

## Maintenance Guide

### When to Update

Update this file when:
1. Stitch UI changes (selectors stop working)
2. New features are added to Stitch
3. New export formats become available
4. Better selectors are discovered

### How to Update

1. Increment version number
2. Update "Last Verified" date
3. Add/modify selectors as needed
4. Document changes in Version History
5. Test with automation pipeline

### Testing Selectors

```javascript
// Test script for verifying selectors
FUNCTION testSelectors():

  browser = await playwright.chromium.launch({ headless: false })
  page = await browser.newPage()
  await page.goto("https://stitch.withgoogle.com")

  // Test each selector group
  FOR each group IN SELECTORS:
    LOG "Testing {group} selectors..."
    FOR each name, config IN SELECTORS[group]:
      exists = await elementExists(page, config)
      status = exists ? "✅" : (config.required ? "❌" : "⚠️")
      LOG "  {status} {name}: {exists ? 'found' : 'not found'}"

  await browser.close()
```

---

## Troubleshooting

### Common Issues

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Sign-in button not found | UI change or not yet loaded | Increase timeout, check fallbacks |
| Generate button unresponsive | Form validation failed | Check prompt input is focused |
| Export panel empty | Design not fully rendered | Wait longer after generation |
| Figma export missing | Feature not available | Skip Figma export, continue |
| CAPTCHA appears | Too many requests | Pause for user, use manual mode |

### Selector Debugging

```javascript
// Dump all matching elements for debugging
FUNCTION debugSelector(page, selector):

  elements = await page.$$(selector)
  LOG "Found {elements.length} elements for: {selector}"

  FOR each el, i IN elements:
    tagName = await el.evaluate(e => e.tagName)
    className = await el.evaluate(e => e.className)
    text = await el.evaluate(e => e.textContent?.slice(0, 50))
    LOG "  [{i}] <{tagName}> class='{className}' text='{text}'"
```

---

## Integration

```javascript
// Import selectors in stitch-integration.md
SELECTORS = LOAD "templates/shared/stitch-selectors.md"

// Use with utility functions
promptInput = await waitForElement(page, SELECTORS.input.promptInput)
await promptInput.fill(prompt)

generateBtn = await findElement(page, SELECTORS.input.generateButton)
await generateBtn.click()

await waitForElement(page, SELECTORS.loading.loadingComplete)
```

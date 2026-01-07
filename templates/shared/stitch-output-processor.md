# Stitch Output Processor Module

**Version**: 1.0.0
**Purpose**: Enhanced mockup output generation with multi-viewport screenshots, WebP optimization, and interactive HTML previews
**Dependencies**: `stitch-anti-detection.md` (humanization functions)

---

## Overview

This module extends the standard Stitch export capabilities with:

1. **Multi-Viewport Screenshots**: Desktop (1440px), Tablet (768px), Mobile (375px), + custom viewports
2. **WebP Optimization**: PNG → WebP conversion for 30-50% file size reduction
3. **Interactive HTML Previews**: JavaScript injection for hover/click interactivity (non-functional but visually interactive)

---

## Configuration

```javascript
OUTPUT_PROCESSOR_CONFIG = {
  // Viewport presets
  viewports: {
    desktop: { width: 1440, height: 900, deviceScaleFactor: 2 },
    tablet: { width: 768, height: 1024, deviceScaleFactor: 2 },
    mobile: { width: 375, height: 812, deviceScaleFactor: 2 }
  },

  // WebP optimization
  webp: {
    enabled: true,
    quality: 85,
    keepOriginal: true  // Keep PNG alongside WebP
  },

  // Interactive preview
  interactive: {
    enabled: true,
    outputFilename: "preview-interactive.html"
  },

  // Performance
  parallel: {
    webp_conversion: true,  // Convert to WebP in parallel
    max_concurrent: 3
  }
}
```

---

## Core Functions

### 1. Enhanced Screenshot Export

```text
FUNCTION stitch_export_screenshots_enhanced(page, output_dir, options = {}):
  """
  Capture screenshots at multiple viewport sizes with WebP optimization.
  Extends standard screenshot export with tablet viewport and WebP conversion.

  Args:
    page: Playwright page object
    output_dir: Output directory path
    options: {
      speed_mult: Speed multiplier for humanization (default: 1.0)
      fingerprint: Browser fingerprint with viewport info
      viewports: Array of viewport names to capture (default: ['desktop', 'tablet', 'mobile'])
      no_webp: Disable WebP conversion (default: false)
      no_optimize: Skip all optimization (default: false)
    }

  Returns:
    {
      success: boolean,
      files: Array of generated file paths,
      stats: {
        png_total_size: number (bytes),
        webp_total_size: number (bytes),
        compression_ratio: number (percentage)
      }
    }
  """

  speed_mult = options.speed_mult OR 1.0
  fingerprint = options.fingerprint OR { viewport: { width: 1440, height: 900 } }
  enabled_viewports = options.viewports OR ['desktop', 'tablet', 'mobile']

  generated_files = []
  png_screenshots = []

  TRY:
    # Step 1: Find preview element
    preview = await page.waitForSelector(SELECTORS.previewCanvas, { timeout: 5000 })

    # If preview is in iframe, switch context
    preview_frame = await page.$(SELECTORS.previewFrame)
    IF preview_frame:
      frame = await preview_frame.contentFrame()
      preview = await frame.$("body")

    # Step 2: Capture all enabled viewports
    FOR viewport_name IN enabled_viewports:
      IF NOT OUTPUT_PROCESSOR_CONFIG.viewports[viewport_name]:
        LOG "⚠️  Unknown viewport '{viewport_name}', skipping"
        CONTINUE

      viewport = OUTPUT_PROCESSOR_CONFIG.viewports[viewport_name]

      # Smooth resize to viewport (anti-detection)
      await smooth_viewport_resize(page, viewport.width, viewport.height)

      # Wait for content to stabilize (longer for mobile/tablet due to responsive adjustments)
      wait_time = viewport_name == 'desktop' ?
        random_between(400 * speed_mult, 800 * speed_mult) :
        random_between(600 * speed_mult, 1200 * speed_mult)

      await wait(wait_time)

      # Capture PNG screenshot with device pixel ratio for Retina displays
      png_path = "{output_dir}/screenshot-{viewport_name}.png"
      await preview.screenshot({
        path: png_path,
        type: "png",
        deviceScaleFactor: viewport.deviceScaleFactor
      })

      generated_files.push(png_path)
      png_screenshots.push({ path: png_path, viewport: viewport_name })

      LOG "✓ Saved {viewport_name} screenshot ({viewport.width}x{viewport.height})"

    # Step 3: Restore viewport to original fingerprint
    await smooth_viewport_resize(
      page,
      fingerprint.viewport.width,
      fingerprint.viewport.height
    )

    # Wait for restoration
    await random_wait(200 * speed_mult, 400 * speed_mult)

    # Step 4: WebP optimization (parallel conversion)
    webp_stats = { png_total_size: 0, webp_total_size: 0 }

    IF NOT options.no_webp AND NOT options.no_optimize:
      webp_results = await convert_screenshots_to_webp(png_screenshots, {
        quality: OUTPUT_PROCESSOR_CONFIG.webp.quality,
        parallel: OUTPUT_PROCESSOR_CONFIG.parallel.webp_conversion,
        max_concurrent: OUTPUT_PROCESSOR_CONFIG.parallel.max_concurrent
      })

      generated_files = generated_files.concat(webp_results.files)
      webp_stats = webp_results.stats

      LOG "✓ WebP optimization complete: {webp_stats.compression_ratio}% size reduction"

    RETURN {
      success: true,
      files: generated_files,
      stats: webp_stats
    }

  CATCH error:
    LOG "Screenshot export failed: " + error.message
    RETURN { success: false, error: error.message }
```

---

### 2. WebP Conversion Pipeline

```text
FUNCTION convert_screenshots_to_webp(screenshots, options = {}):
  """
  Convert PNG screenshots to WebP format with parallel processing.

  Args:
    screenshots: Array of { path: string, viewport: string }
    options: {
      quality: number (0-100, default: 85)
      parallel: boolean (default: true)
      max_concurrent: number (default: 3)
      keep_original: boolean (default: true)
    }

  Returns:
    {
      files: Array of WebP file paths,
      stats: {
        png_total_size: number,
        webp_total_size: number,
        compression_ratio: number
      }
    }
  """

  quality = options.quality OR 85
  max_concurrent = options.max_concurrent OR 3

  webp_files = []
  png_total_size = 0
  webp_total_size = 0

  # Conversion function for a single screenshot
  FUNCTION convert_single(screenshot):
    png_path = screenshot.path
    webp_path = png_path.replace(".png", ".webp")

    TRY:
      # Get PNG file size
      png_size = GET_FILE_SIZE(png_path)
      png_total_size += png_size

      # Convert using sharp/imagemagick (pseudo-code for CLI agent to execute)
      # In practice, this would use a Node.js library like 'sharp' or CLI tool like 'cwebp'

      # Using sharp (preferred):
      # const sharp = require('sharp');
      # await sharp(png_path)
      #   .webp({ quality: quality })
      #   .toFile(webp_path);

      # Using cwebp CLI (fallback):
      # EXEC: cwebp -q {quality} {png_path} -o {webp_path}

      CONVERT_TO_WEBP(png_path, webp_path, quality)

      # Get WebP file size
      webp_size = GET_FILE_SIZE(webp_path)
      webp_total_size += webp_size

      reduction = ((png_size - webp_size) / png_size * 100).toFixed(1)
      LOG "  ✓ {screenshot.viewport}: {png_size} → {webp_size} ({reduction}% reduction)"

      RETURN webp_path

    CATCH error:
      LOG "  ✗ WebP conversion failed for {screenshot.viewport}: {error.message}"
      RETURN null

  # Execute conversions (parallel or sequential)
  IF options.parallel:
    # Process in batches to avoid resource exhaustion
    batches = chunk_array(screenshots, max_concurrent)

    FOR batch IN batches:
      batch_results = await Promise.all(
        batch.map(screenshot => convert_single(screenshot))
      )
      webp_files = webp_files.concat(batch_results.filter(f => f !== null))
  ELSE:
    # Sequential conversion
    FOR screenshot IN screenshots:
      result = await convert_single(screenshot)
      IF result:
        webp_files.push(result)

  # Calculate overall compression ratio
  compression_ratio = png_total_size > 0 ?
    ((png_total_size - webp_total_size) / png_total_size * 100).toFixed(1) :
    0

  RETURN {
    files: webp_files,
    stats: {
      png_total_size: png_total_size,
      webp_total_size: webp_total_size,
      compression_ratio: compression_ratio
    }
  }
```

---

### 3. Interactive HTML Preview Generator

```text
FUNCTION generate_interactive_preview(html_content, css_content, output_dir, options = {}):
  """
  Create an interactive HTML preview with JavaScript injection for hover/click states.

  Args:
    html_content: Base HTML content from Stitch
    css_content: CSS styles from Stitch
    output_dir: Output directory
    options: {
      filename: Output filename (default: "preview-interactive.html")
      enable_hover: Enable hover effects (default: true)
      enable_click: Enable click animations (default: true)
      enable_focus: Enable form focus states (default: true)
      enable_modals: Enable modal overlay simulation (default: true)
    }

  Returns:
    {
      success: boolean,
      file: string (path to generated file)
    }
  """

  filename = options.filename OR OUTPUT_PROCESSOR_CONFIG.interactive.outputFilename

  TRY:
    # Inject interactivity JavaScript
    interactive_js = GENERATE_INTERACTIVE_JS({
      enable_hover: options.enable_hover !== false,
      enable_click: options.enable_click !== false,
      enable_focus: options.enable_focus !== false,
      enable_modals: options.enable_modals !== false
    })

    # Build complete HTML document
    interactive_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Interactive Preview - Stitch Mockup</title>
  <style>
    /* Base styles from Stitch */
    {css_content}

    /* Interactive enhancements */
    {INTERACTIVE_CSS}
  </style>
</head>
<body>
  <!-- Content from Stitch -->
  {html_content}

  <!-- Interactivity script -->
  <script>
    {interactive_js}
  </script>
</body>
</html>
"""

    # Write to file
    output_path = "{output_dir}/{filename}"
    WRITE interactive_html TO output_path

    LOG "✓ Generated interactive preview: {filename}"

    RETURN { success: true, file: output_path }

  CATCH error:
    LOG "Interactive preview generation failed: {error.message}"
    RETURN { success: false, error: error.message }
```

---

### 4. Interactive JavaScript Generator

```text
FUNCTION GENERATE_INTERACTIVE_JS(options):
  """
  Generate JavaScript code for interactive preview enhancements.

  Returns: String (JavaScript code)
  """

  RETURN """
(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    enableHover: """ + options.enable_hover + """,
    enableClick: """ + options.enable_click + """,
    enableFocus: """ + options.enable_focus + """,
    enableModals: """ + options.enable_modals + """
  };

  // 1. HOVER EFFECTS
  if (CONFIG.enableHover) {
    // Add hover effects to interactive elements
    const interactiveSelectors = 'button, a, [role="button"], .btn, .link';
    const interactiveElements = document.querySelectorAll(interactiveSelectors);

    interactiveElements.forEach(el => {
      el.addEventListener('mouseenter', function() {
        this.style.transition = 'all 0.2s ease';
        this.style.transform = 'translateY(-1px)';
        this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
      });

      el.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '';
      });
    });
  }

  // 2. CLICK ANIMATIONS
  if (CONFIG.enableClick) {
    document.addEventListener('click', function(e) {
      const target = e.target.closest('button, a, [role="button"], .btn');
      if (!target) return;

      // Prevent default navigation for links
      if (target.tagName === 'A') {
        e.preventDefault();
      }

      // Add click ripple effect
      target.style.transition = 'transform 0.1s ease';
      target.style.transform = 'scale(0.95)';

      setTimeout(() => {
        target.style.transform = '';
      }, 100);

      // Visual feedback
      const ripple = document.createElement('div');
      ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        width: 20px;
        height: 20px;
        pointer-events: none;
        animation: ripple-effect 0.6s ease-out;
      `;

      const rect = target.getBoundingClientRect();
      ripple.style.left = (e.clientX - rect.left - 10) + 'px';
      ripple.style.top = (e.clientY - rect.top - 10) + 'px';

      target.style.position = 'relative';
      target.appendChild(ripple);

      setTimeout(() => ripple.remove(), 600);
    });

    // Add ripple animation CSS
    if (!document.getElementById('ripple-animation')) {
      const style = document.createElement('style');
      style.id = 'ripple-animation';
      style.textContent = `
        @keyframes ripple-effect {
          to {
            transform: scale(4);
            opacity: 0;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }

  // 3. FORM FOCUS STATES
  if (CONFIG.enableFocus) {
    const formElements = document.querySelectorAll('input, textarea, select');

    formElements.forEach(el => {
      el.addEventListener('focus', function() {
        this.style.outline = '2px solid #3b82f6';
        this.style.outlineOffset = '2px';
        this.style.transition = 'all 0.2s ease';
      });

      el.addEventListener('blur', function() {
        this.style.outline = '';
        this.style.outlineOffset = '';
      });
    });
  }

  // 4. MODAL OVERLAY SIMULATION
  if (CONFIG.enableModals) {
    // Detect potential modal triggers (buttons with text containing 'open', 'show', 'modal', etc.)
    const modalTriggers = Array.from(document.querySelectorAll('button, [role="button"]'))
      .filter(el => {
        const text = el.textContent.toLowerCase();
        return text.includes('open') || text.includes('show') || text.includes('modal') ||
               text.includes('dialog') || text.includes('popup');
      });

    modalTriggers.forEach(trigger => {
      trigger.addEventListener('click', function(e) {
        e.preventDefault();

        // Create overlay
        const overlay = document.createElement('div');
        overlay.style.cssText = `
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 9999;
          animation: fade-in 0.2s ease;
        `;

        // Create modal content
        const modal = document.createElement('div');
        modal.style.cssText = `
          background: white;
          padding: 2rem;
          border-radius: 8px;
          box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
          max-width: 500px;
          width: 90%;
          animation: slide-up 0.3s ease;
        `;
        modal.innerHTML = `
          <h2 style="margin: 0 0 1rem 0;">Modal Preview</h2>
          <p style="margin: 0 0 1.5rem 0; color: #666;">
            This is a simulated modal overlay. In the real application,
            this would show actual content.
          </p>
          <button style="
            padding: 0.5rem 1rem;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
          ">Close</button>
        `;

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        // Close modal on overlay click or button click
        overlay.addEventListener('click', function(e) {
          if (e.target === overlay || e.target.tagName === 'BUTTON') {
            overlay.style.animation = 'fade-out 0.2s ease';
            setTimeout(() => overlay.remove(), 200);
          }
        });
      });
    });

    // Add modal animations CSS
    if (!document.getElementById('modal-animations')) {
      const style = document.createElement('style');
      style.id = 'modal-animations';
      style.textContent = `
        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes fade-out {
          from { opacity: 1; }
          to { opacity: 0; }
        }
        @keyframes slide-up {
          from {
            transform: translateY(20px);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }

  // 5. ADD NOTIFICATION
  setTimeout(() => {
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #10b981;
      color: white;
      padding: 1rem 1.5rem;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      font-size: 14px;
      animation: slide-in-right 0.3s ease;
      z-index: 10000;
    `;
    notification.innerHTML = `
      <strong>✨ Interactive Preview</strong><br>
      <span style="opacity: 0.9; font-size: 12px;">
        Hover and click elements to see interactions
      </span>
    `;

    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
      notification.style.animation = 'slide-out-right 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 5000);

    // Add notification animations
    if (!document.getElementById('notification-animations')) {
      const style = document.createElement('style');
      style.id = 'notification-animations';
      style.textContent = `
        @keyframes slide-in-right {
          from {
            transform: translateX(400px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        @keyframes slide-out-right {
          from {
            transform: translateX(0);
            opacity: 1;
          }
          to {
            transform: translateX(400px);
            opacity: 0;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }, 500);
})();
"""
```

---

### 5. Interactive CSS Enhancements

```text
CONST INTERACTIVE_CSS = """
/* Interactive preview enhancements */
* {
  box-sizing: border-box;
}

/* Smooth transitions for all interactive elements */
button, a, [role="button"], .btn, .link,
input, textarea, select {
  transition: all 0.2s ease;
}

/* Cursor hints */
button, a, [role="button"], .btn, .link {
  cursor: pointer;
}

/* Disable text selection on buttons */
button, [role="button"], .btn {
  user-select: none;
  -webkit-user-select: none;
}

/* Form field enhancements */
input:focus, textarea:focus, select:focus {
  transition: all 0.2s ease;
}

/* Prevent link navigation visual feedback */
a {
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
"""
```

---

## Integration with Main Workflow

### Updated Export Phase

Replace the standard export calls in `stitch-integration.md` Phase 5 with:

```text
# Phase 5: Export all formats with enhancements
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
    interactive_result = generate_interactive_preview(
      html_result.html_content,
      html_result.css_content,
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
```

---

## Output Directory Structure

After running with output processor enhancements:

```
.preview/stitch-mockups/
└── {feature}/
    └── {screen}/
        ├── screenshot-desktop.png          (existing)
        ├── screenshot-desktop.webp         (NEW - ~50% smaller)
        ├── screenshot-tablet.png           (NEW)
        ├── screenshot-tablet.webp          (NEW - ~50% smaller)
        ├── screenshot-mobile.png           (existing)
        ├── screenshot-mobile.webp          (NEW - ~50% smaller)
        ├── stitch-output.html              (existing)
        ├── stitch-output.css               (existing)
        ├── preview-interactive.html        (NEW - with JS interactivity)
        ├── figma-clipboard.json            (existing - optional)
        └── prompt.txt                      (existing)
```

---

## Performance Considerations

### WebP Conversion

- **Parallel conversion**: Processes multiple screenshots simultaneously (default: 3 concurrent)
- **Target compression**: 30-50% file size reduction at 85% quality
- **Fallback**: If conversion fails, PNG files remain available

### Viewport Capture

- **Humanized delays**: Smooth viewport resizing with anti-detection timing
- **Retina support**: 2x device scale factor for high-DPI displays
- **Responsive stabilization**: Longer waits for tablet/mobile to allow layout adjustments

---

## Error Handling

All functions include comprehensive error handling:

1. **Screenshot failures**: Falls back to available viewports, logs specific errors
2. **WebP conversion failures**: Keeps original PNG, logs conversion issues
3. **Interactive preview failures**: Non-blocking, original HTML still available
4. **Resource exhaustion**: Batching prevents overwhelming the system

---

## Testing & Validation

### Unit Tests

```javascript
// Test multi-viewport capture
ASSERT screenshot_desktop.png exists
ASSERT screenshot_tablet.png exists
ASSERT screenshot_mobile.png exists

// Test WebP conversion
ASSERT screenshot_desktop.webp exists
ASSERT webp_file_size < png_file_size * 0.7  // At least 30% reduction

// Test interactive preview
ASSERT preview-interactive.html exists
ASSERT file_contains(preview-interactive.html, "CONFIG.enableHover")
ASSERT file_contains(preview-interactive.html, "ripple-effect")
```

### Integration Test

```bash
# Full workflow test
/speckit.design --mockup --viewports "desktop,tablet,mobile"

# Verify outputs
ls .preview/stitch-mockups/{feature}/{screen}/
# Expected: 6 screenshots (3 PNG + 3 WebP) + interactive preview
```

---

## Backward Compatibility

✅ **Fully backward compatible**:

- Default viewports include existing desktop + mobile
- WebP files generated alongside PNG (not replacing)
- Interactive preview is additional file (doesn't modify stitch-output.html)
- All existing export functions remain unchanged

🔧 **Opt-out flags**:

- `--no-webp`: Disable WebP conversion
- `--no-optimize`: Skip all optimizations
- `--viewports "desktop,mobile"`: Exclude tablet
- `--interactive false`: Disable interactive preview generation

---

## Version History

- **v1.0.0** (2026-01-06): Initial implementation
  - Multi-viewport screenshots (desktop/tablet/mobile)
  - WebP optimization with parallel conversion
  - Interactive HTML preview with JS injection

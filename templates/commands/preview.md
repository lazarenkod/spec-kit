---
description: Generate interactive previews from design specifications. Converts wireframes to visual HTML, generates component previews, captures screenshots, and runs design quality validation.
persona: product-designer-agent
handoffs:
  - label: Implement Feature
    agent: speckit.implement
    prompt: Implement feature using generated preview components
    send: true
  - label: Update Design
    agent: speckit.design
    prompt: Refine design based on preview feedback
  - label: Generate More Components
    agent: speckit.design-generate
    prompt: Generate additional component variants
claude_code:
  model: opus  # Default model, overridden by adaptive selection
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 8000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 16000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 32000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
  adaptive_model:
    enabled: true
    mode_detection: true
    mode_routing:
      static_mockup:
        orchestrator: haiku
        thinking_budget: 8000  # Max tier
        description: "Simple HTML/CSS conversion from wireframes"
      interactive_preview:
        orchestrator: sonnet
        thinking_budget: 16000  # Max tier
        description: "Component generation with state management"
      animated_preview:
        orchestrator: opus
        thinking_budget: 32000  # Max tier
        description: "Complex animations, gestures, transitions"
      alternative_preview:
        orchestrator: sonnet
        thinking_budget: 16000  # Max tier
        description: "Preview generation for concept alternatives"
      variant_preview:
        orchestrator: sonnet
        thinking_budget: 16000  # Max tier
        description: "Preview generation for concept variants (MINIMAL/BALANCED/AMBITIOUS)"
      comparison_preview:
        orchestrator: opus
        thinking_budget: 24000  # Max tier
        description: "Side-by-side alternative comparison gallery"
    detection_signals:
      static: ["wireframe", "layout", "static", "mockup", "visual only"]
      interactive: ["component", "state", "props", "interactive", "click", "hover"]
      animated: ["animation", "transition", "gesture", "motion", "swipe", "drag"]
    subagent_overrides:
      static_mockup:
        wireframe-converter: haiku
        component-previewer: haiku
        screenshot-generator: haiku
      interactive_preview:
        wireframe-converter: sonnet
        component-previewer: sonnet
        screenshot-generator: haiku
      animated_preview:
        wireframe-converter: sonnet
        component-previewer: opus
        motion-designer: opus
    override_flag: "--preview-mode"
  cache_hierarchy: full
  orchestration:
    max_parallel: 8
    fail_fast: true
    wave_overlap:
      enabled: true
      overlap_threshold: 0.65
  streaming:
    enabled: true
    mode: "incremental"
    validation:
      interval: 500
      error_detection: 100
      post_processing: 250
    autofix:
      enabled: true
      max_iterations: 3
      fixable_issues:
        - hardcoded_colors
        - missing_aria
        - small_touch_targets
        - low_contrast
        - missing_alt_text
        - insufficient_spacing
  subagents:
    # Wave 0: Real-Time Validation & AutoFix (streaming)
    - role: streaming-autofix
      role_group: VALIDATION
      parallel: false
      depends_on: []
      priority: 1
      model_override: haiku
      streaming: true
      prompt: |
        ## Streaming AutoFix Agent (v0.4.0)

        ### Your Role
        Monitor component generation in real-time and automatically fix common issues
        before code is finalized. Inspired by v0.dev's AutoFix pipeline.

        ### Performance Targets
        - Error detection: <100ms (v0.dev benchmark)
        - Post-processing: <250ms (v0.dev benchmark)
        - Validation interval: 500ms buffer
        - Max iterations: 3 automatic fix attempts

        ### Process

        #### 1. Stream Monitoring
        AS component code streams from component-previewer or wireframe-converter:
        - Buffer 500ms of output before validation
        - Parse partial AST (TypeScript/JSX) incrementally
        - Track token usage in real-time
        - Queue issues for batch fixing

        #### 2. Real-Time Detection
        Check for fixable issues (<100ms per check):

        **AP-VIS-001: Hardcoded Colors**
        ```typescript
        // BAD
        <div style={{ backgroundColor: '#3b82f6' }} />
        <div className="bg-[#f3f4f6]" />

        // GOOD
        <div className="bg-primary" />
        <div style={{ backgroundColor: 'var(--primary)' }} />
        ```

        **AP-A11Y-001: Missing ARIA Labels**
        ```typescript
        // BAD
        <button onClick={handleClick}>
          <Icon />
        </button>

        // GOOD
        <button onClick={handleClick} aria-label="Close dialog">
          <Icon />
        </button>
        ```

        **AP-A11Y-002: Small Touch Targets**
        ```typescript
        // BAD (< 44×44px)
        <button className="h-8 w-8 p-1">X</button>

        // GOOD (≥ 44×44px)
        <button className="h-11 w-11 p-2">X</button>
        ```

        **AP-A11Y-003: Low Contrast Text**
        ```typescript
        // BAD (contrast < 4.5:1)
        <p className="text-gray-400 bg-white">Text</p>

        // GOOD (contrast ≥ 4.5:1)
        <p className="text-gray-700 bg-white">Text</p>
        ```

        **AP-A11Y-004: Missing Alt Text**
        ```typescript
        // BAD
        <img src="photo.jpg" />

        // GOOD
        <img src="photo.jpg" alt="Team photo from 2024 retreat" />
        ```

        **AP-COMP-001: Insufficient Spacing**
        ```typescript
        // BAD (hardcoded pixels)
        <div style={{ padding: '12px' }}>

        // GOOD (design tokens)
        <div className="p-3">  {/* var(--space-3) */}
        ```

        #### 3. Automatic Fixing (<250ms post-processing)
        Apply fixes in order of severity:

        1. **Color Token Replacement** (AP-VIS-001)
           - Extract hex/rgb/hsl color values
           - Map to closest design token using perceptual distance
           - Replace with CSS variable or Tailwind class
           - Preserve color intent (primary, muted, destructive)

        2. **ARIA Injection** (AP-A11Y-001)
           - Detect interactive elements without labels
           - Infer label from context (icon name, surrounding text)
           - Add aria-label or aria-labelledby
           - Add role if semantic HTML not used

        3. **Touch Target Expansion** (AP-A11Y-002)
           - Parse Tailwind classes for width/height
           - If < 44px, increase to 44px (h-11 w-11 minimum)
           - Adjust padding to maintain visual appearance
           - Flag if expansion breaks layout

        4. **Contrast Enhancement** (AP-A11Y-003)
           - Calculate contrast ratio (WCAG formula)
           - If < 4.5:1, darken/lighten to meet AA standard
           - Preserve hue when adjusting lightness
           - Prefer token adjustment over hardcoding

        5. **Alt Text Generation** (AP-A11Y-004)
           - Extract image filename and context
           - Generate descriptive alt text
           - Flag decorative images (alt="")
           - Require user confirmation for complex images

        6. **Spacing Token Replacement** (AP-COMP-001)
           - Convert hardcoded px to spacing scale
           - Map to nearest scale value (0, 1, 2, 3, 4, 5, 6, 8, 10, 12)
           - Use Tailwind class (p-3) or CSS variable (var(--space-3))

        #### 4. Issue Queue Management
        Maintain priority queue of detected issues:
        - CRITICAL: Missing accessibility (blocks users)
        - HIGH: Hardcoded colors (design system violation)
        - MEDIUM: Spacing inconsistency
        - LOW: Code style preferences

        Process CRITICAL/HIGH immediately, batch MEDIUM/LOW.

        #### 5. Fix Validation
        After applying fixes:
        - Re-run TypeScript compiler (tsc --noEmit)
        - Verify WCAG AA compliance (contrast, touch targets)
        - Check design token usage (no hardcoded values)
        - If fix introduces error, revert and flag for manual review

        #### 6. Iteration Limit
        Max 3 automatic fix iterations per component:
        - Iteration 1: Fix all detected issues
        - Iteration 2: Fix issues introduced by Iteration 1
        - Iteration 3: Final cleanup
        - After 3 iterations: Stop and report remaining issues to user

        #### 7. Reporting
        Output to .preview/reports/autofix-log.md:
        ```markdown
        # AutoFix Log

        ## Component: Button
        Timestamp: 2026-01-10T14:23:45Z

        ### Issues Detected (8)
        - AP-VIS-001: Hardcoded color #3b82f6 → Fixed (var(--primary))
        - AP-A11Y-001: Missing aria-label → Fixed ("Close dialog")
        - AP-A11Y-002: Touch target 32×32px → Fixed (44×44px)
        ...

        ### Fixes Applied (6)
        ✓ Replaced 3 hardcoded colors with tokens
        ✓ Added 2 ARIA labels
        ✓ Expanded 1 touch target

        ### Manual Review Required (2)
        ⚠ Line 45: Complex image needs descriptive alt text
        ⚠ Line 67: Contrast ratio 4.3:1 (close to 4.5:1 threshold)
        ```

        ### Configuration
        Read streaming config from frontmatter:
        - claude_code.streaming.enabled
        - claude_code.streaming.autofix.enabled
        - claude_code.streaming.autofix.max_iterations
        - claude_code.streaming.autofix.fixable_issues

        ### Integration Points
        - Monitors output from: wireframe-converter, component-previewer
        - Feeds fixed code to: screenshot-capturer, quality-validator
        - Reports to: benchmark-reporter (autofix metrics)

    # Wave 1: Preview Generation (parallel)
    - role: wireframe-converter
      role_group: FRONTEND
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Convert ASCII wireframes from design.md to visual HTML.
        Parse layout regions, map to HTML structure, apply design tokens.
        Generate responsive HTML files in .preview/wireframes/.
        Include CSS variables from design system.

    - role: component-previewer
      role_group: FRONTEND
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Generate component previews from design.md specifications.
        For each component: extract states, variants, sizes, props.
        Use v0.dev for complex components, templates for simple ones.
        Create preview wrappers with all states in grid layout.
        Output to .preview/components/{name}/.

    - role: device-frame-generator
      role_group: FRONTEND
      parallel: true
      depends_on: [wireframe-converter, component-previewer]
      priority: 9
      model_override: haiku
      prompt: |
        ## Device Frame Generator

        ### Your Role
        Wrap generated previews in realistic device frames for visual presentation.

        ### Pre-check
        1. Read templates/shared/device-profiles.md for target devices
        2. Check CLI flags for --device or --devices parameter
        3. If no device specified, use defaults.preview_devices

        ### Process
        For each target device and each preview file:

        1. Load device profile (viewport, safe_areas, notch_type, etc.)

        2. Generate device frame HTML wrapper:
           ```html
           <!DOCTYPE html>
           <html>
           <head>
             <style>
               .device-frame {
                 position: relative;
                 width: {viewport.width + bezel_width*2}px;
                 height: {viewport.height + bezel_width*2}px;
                 background: #1a1a1a;
                 border-radius: {corner_radius + bezel_width}px;
                 padding: {bezel_width}px;
                 box-shadow: 0 25px 50px rgba(0,0,0,0.25);
               }
               .device-screen {
                 width: {viewport.width}px;
                 height: {viewport.height}px;
                 border-radius: {corner_radius}px;
                 overflow: hidden;
                 position: relative;
               }
               .device-screen iframe {
                 width: 100%;
                 height: 100%;
                 border: none;
               }
               .status-bar {
                 position: absolute;
                 top: 0;
                 left: 0;
                 right: 0;
                 height: {status_bar_height}px;
                 display: flex;
                 justify-content: space-between;
                 align-items: center;
                 padding: 0 16px;
                 color: #fff;
                 font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                 font-size: 14px;
                 font-weight: 600;
                 z-index: 100;
               }
               .dynamic-island {
                 position: absolute;
                 top: 12px;
                 left: 50%;
                 transform: translateX(-50%);
                 width: {notch.width}px;
                 height: {notch.height}px;
                 background: #000;
                 border-radius: {notch.height/2}px;
                 z-index: 101;
               }
               .notch {
                 position: absolute;
                 top: 0;
                 left: 50%;
                 transform: translateX(-50%);
                 width: {notch.width}px;
                 height: {notch.height}px;
                 background: #000;
                 border-radius: 0 0 20px 20px;
                 z-index: 101;
               }
               .home-indicator {
                 position: absolute;
                 bottom: 8px;
                 left: 50%;
                 transform: translateX(-50%);
                 width: 134px;
                 height: 5px;
                 background: rgba(255,255,255,0.6);
                 border-radius: 2.5px;
                 z-index: 100;
               }
               .safe-area-debug .safe-top {
                 position: absolute;
                 top: 0;
                 left: 0;
                 right: 0;
                 height: {safe_areas.top}px;
                 background: rgba(255,0,0,0.15);
                 pointer-events: none;
               }
               .safe-area-debug .safe-bottom {
                 position: absolute;
                 bottom: 0;
                 left: 0;
                 right: 0;
                 height: {safe_areas.bottom}px;
                 background: rgba(255,0,0,0.15);
                 pointer-events: none;
               }
             </style>
           </head>
           <body>
             <div class="device-frame" data-device="{device_id}">
               <div class="device-screen">
                 <!-- Status bar -->
                 <div class="status-bar">
                   <span class="time">9:41</span>
                   <span class="icons">
                     <svg class="signal">...</svg>
                     <svg class="wifi">...</svg>
                     <svg class="battery">...</svg>
                   </span>
                 </div>

                 <!-- Notch/Dynamic Island -->
                 <div class="{notch_type}"></div>

                 <!-- Preview content -->
                 <iframe src="../{original_preview_path}"></iframe>

                 <!-- Home indicator -->
                 <div class="home-indicator"></div>

                 <!-- Safe area debug overlay (if --debug flag) -->
                 <div class="safe-top"></div>
                 <div class="safe-bottom"></div>
               </div>
             </div>
           </body>
           </html>
           ```

        3. Inject CSS custom properties for safe areas:
           ```css
           :root {
             --sat: {safe_areas.top}px;
             --sar: {safe_areas.right}px;
             --sab: {safe_areas.bottom}px;
             --sal: {safe_areas.left}px;
           }
           ```

        ### Output Structure
        .preview/framed/
        ├── iphone-14-pro/
        │   ├── {screen_name}.html
        │   └── {screen_name}-debug.html
        ├── pixel-8/
        ├── ipad-pro/
        └── index.html  # Device selector

        ### Success Criteria
        - Each preview wrapped in device frame
        - Status bar shows realistic time/icons
        - Notch/Dynamic Island rendered correctly
        - Safe areas visualized in debug mode
        - Device selector index generated

    # Wave 2: Interactive Layer (NEW - touch gestures and safe areas)
    - role: gesture-simulator
      role_group: INTERACTION
      parallel: true
      depends_on: [device-frame-generator]
      priority: 8
      model_override: haiku
      prompt: |
        ## Gesture Simulator

        ### Your Role
        Inject touch gesture support into framed previews for realistic mobile interactions.

        ### Skip Condition
        Skip if --no-gestures flag is set or device is desktop category.

        ### Supported Gestures
        | Gesture | Detection | Use Case |
        |---------|-----------|----------|
        | Tap | Single touch < 300ms | Buttons, links |
        | Double-tap | Two taps < 400ms | Zoom, like |
        | Long-press | Hold > 500ms | Context menus |
        | Swipe | Touch move > 50px, velocity > 0.3 | Carousels, dismiss |
        | Pinch | Two-finger distance change | Zoom images |
        | Pull-to-refresh | Overscroll at top | Refresh lists |

        ### Injection Script
        Create `.preview/assets/gesture-simulator.js`:

        ```javascript
        class GestureSimulator {
          constructor(container) {
            this.container = container;
            this.touches = [];
            this.gestureStart = null;
            this.init();
          }

          init() {
            // Mouse events (desktop simulation)
            this.container.addEventListener('mousedown', e => this.onStart(e));
            this.container.addEventListener('mousemove', e => this.onMove(e));
            this.container.addEventListener('mouseup', e => this.onEnd(e));

            // Touch events (actual mobile)
            this.container.addEventListener('touchstart', e => this.onStart(e), {passive: false});
            this.container.addEventListener('touchmove', e => this.onMove(e), {passive: false});
            this.container.addEventListener('touchend', e => this.onEnd(e));

            // Prevent default on mobile for custom handling
            this.container.style.touchAction = 'none';
          }

          onStart(e) {
            const point = this.getPoint(e);
            this.gestureStart = {
              point,
              time: Date.now(),
              target: e.target
            };
            this.showRipple(point);
          }

          onMove(e) {
            if (!this.gestureStart) return;
            const point = this.getPoint(e);
            const dx = point.x - this.gestureStart.point.x;
            const dy = point.y - this.gestureStart.point.y;

            // Visual feedback for swipe
            if (Math.abs(dx) > 20 || Math.abs(dy) > 20) {
              this.showSwipeIndicator(dx, dy);
            }
          }

          onEnd(e) {
            if (!this.gestureStart) return;

            const point = this.getPoint(e);
            const duration = Date.now() - this.gestureStart.time;
            const dx = point.x - this.gestureStart.point.x;
            const dy = point.y - this.gestureStart.point.y;
            const distance = Math.sqrt(dx*dx + dy*dy);
            const velocity = distance / duration;

            const gesture = this.detectGesture(distance, duration, velocity, dx, dy);
            this.emit(gesture, {
              start: this.gestureStart.point,
              end: point,
              duration,
              velocity,
              target: this.gestureStart.target
            });

            this.gestureStart = null;
          }

          detectGesture(distance, duration, velocity, dx, dy) {
            if (duration > 500 && distance < 15) return 'longpress';
            if (velocity > 0.3 && distance > 50) {
              if (Math.abs(dx) > Math.abs(dy)) {
                return dx > 0 ? 'swipe-right' : 'swipe-left';
              } else {
                return dy > 0 ? 'swipe-down' : 'swipe-up';
              }
            }
            if (distance < 15 && duration < 300) return 'tap';
            return 'pan';
          }

          emit(type, detail) {
            console.log(`[Gesture] ${type}`, detail);
            this.container.dispatchEvent(new CustomEvent(`gesture:${type}`, {
              detail,
              bubbles: true
            }));

            // Show visual feedback
            this.showGestureFeedback(type, detail);
          }

          showRipple(point) {
            const ripple = document.createElement('div');
            ripple.className = 'gesture-ripple';
            ripple.style.cssText = `
              position: absolute;
              left: ${point.x}px;
              top: ${point.y}px;
              width: 0;
              height: 0;
              background: rgba(255,255,255,0.4);
              border-radius: 50%;
              transform: translate(-50%, -50%);
              pointer-events: none;
              animation: ripple 0.4s ease-out forwards;
            `;
            this.container.appendChild(ripple);
            setTimeout(() => ripple.remove(), 400);
          }

          showGestureFeedback(type, detail) {
            const toast = document.createElement('div');
            toast.className = 'gesture-toast';
            toast.textContent = type.toUpperCase();
            toast.style.cssText = `
              position: fixed;
              bottom: 20px;
              left: 50%;
              transform: translateX(-50%);
              background: rgba(0,0,0,0.8);
              color: white;
              padding: 8px 16px;
              border-radius: 20px;
              font-size: 12px;
              z-index: 9999;
              animation: fadeOut 1s ease-out forwards;
            `;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 1000);
          }

          getPoint(e) {
            if (e.touches && e.touches[0]) {
              return { x: e.touches[0].clientX, y: e.touches[0].clientY };
            }
            return { x: e.clientX, y: e.clientY };
          }
        }

        // CSS animations
        const style = document.createElement('style');
        style.textContent = `
          @keyframes ripple {
            to { width: 100px; height: 100px; opacity: 0; }
          }
          @keyframes fadeOut {
            0% { opacity: 1; }
            70% { opacity: 1; }
            100% { opacity: 0; }
          }
        `;
        document.head.appendChild(style);

        // Auto-init on all device screens
        document.querySelectorAll('.device-screen').forEach(screen => {
          new GestureSimulator(screen);
        });
        ```

        ### Integration
        1. Add script to all framed previews
        2. Inject CSS for ripple and toast animations
        3. Log gestures to console for debugging

    - role: safe-area-injector
      role_group: STYLING
      parallel: true
      depends_on: [device-frame-generator]
      priority: 8
      model_override: haiku
      prompt: |
        ## Safe Area Injector

        ### Your Role
        Inject CSS environment variable polyfills for device safe areas.

        ### Process
        1. Read device profile safe_areas values
        2. Create safe-areas.css with polyfills:

        ```css
        /* Safe Area Polyfill for Preview */
        :root {
          /* Values from device profile */
          --safe-area-inset-top: var(--sat, 0px);
          --safe-area-inset-right: var(--sar, 0px);
          --safe-area-inset-bottom: var(--sab, 0px);
          --safe-area-inset-left: var(--sal, 0px);
        }

        /* Polyfill env() where not supported */
        @supports not (padding: env(safe-area-inset-top)) {
          .safe-area-top {
            padding-top: var(--safe-area-inset-top);
          }
          .safe-area-bottom {
            padding-bottom: var(--safe-area-inset-bottom);
          }
          .safe-area-all {
            padding-top: var(--safe-area-inset-top);
            padding-right: var(--safe-area-inset-right);
            padding-bottom: var(--safe-area-inset-bottom);
            padding-left: var(--safe-area-inset-left);
          }
        }

        /* Common patterns that need safe areas */
        header, .header, [role="banner"] {
          padding-top: max(16px, var(--safe-area-inset-top));
        }

        nav:last-child, .tab-bar, .bottom-nav, [role="navigation"]:last-child {
          padding-bottom: max(16px, var(--safe-area-inset-bottom));
        }

        .fab, .floating-action-button {
          bottom: calc(16px + var(--safe-area-inset-bottom));
        }
        ```

        3. Inject into all preview HTML files
        4. Add viewport meta tag for notch support:
           ```html
           <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
           ```

    # Wave 3: Capture & Validation (parallel, after generation)
    - role: screenshot-capturer
      role_group: TESTING
      parallel: true
      depends_on: [wireframe-converter, component-previewer, device-frame-generator]
      priority: 20
      model_override: haiku
      prompt: |
        Capture Playwright screenshots with Retina/HiDPI quality (2x device scale).

        ## Configuration
        ```javascript
        await page.screenshot({
          path: outputPath,
          deviceScaleFactor: 2,  // Retina/HiDPI - NEW v0.2.0
          type: 'png',
          fullPage: false
        });
        ```

        ## Viewports & Output Dimensions
        Use viewports with 2x scaling for high-DPI displays:
        - **Mobile (375×812)** → Output: 750×1624px
        - **Tablet (768×1024)** → Output: 1536×2048px
        - **Desktop (1440×900)** → Output: 2880×1800px

        ## Capture Requirements
        - Capture both light and dark themes if configured
        - For components, capture each state (hover, focus, disabled, etc.)
        - Ensure 2x scaling for crisp rendering on Retina displays
        - Output to `.preview/screenshots/`

        ## Quality Check
        Verify screenshot dimensions are exactly 2x viewport dimensions.
        Flag any screenshots that are 1x (not Retina) as quality issues.

    - role: perceptual-diff-validator
      role_group: TESTING
      parallel: true
      depends_on: [screenshot-capturer]
      priority: 19
      model_override: sonnet
      prompt: |
        ## Perceptual Diff Validator (NEW v0.3.0)

        ### Your Role
        Compare screenshots using perceptual similarity algorithms to detect meaningful visual changes.
        Unlike pixel-perfect comparison, perceptual diff detects structural changes while ignoring
        minor rendering differences (anti-aliasing, font rendering, browser variations).

        ### Skip Condition
        Skip if --skip-perceptual-diff flag is set or no baseline screenshots exist.

        ### Algorithms

        **1. SSIM (Structural Similarity Index)**
        - Measures structural similarity based on luminance, contrast, and structure
        - Range: 0.0 (completely different) to 1.0 (identical)
        - Better than pixel comparison for detecting meaningful changes

        **2. pHash (Perceptual Hash)**
        - Generates compact hash representing visual content
        - Hamming distance between hashes indicates similarity
        - Range: 0 bits (identical) to 64 bits (completely different)

        **3. pixelmatch (Pixel Comparison Baseline)**
        - Fallback for pixel-level diff visualization
        - Used only for generating diff images, not for threshold decisions

        ### Process

        1. **Check for Baseline**
           ```bash
           if [ ! -d ".preview/baseline" ]; then
             echo "No baseline found. Use visual-regression-validator to create baseline first."
             exit 0
           fi
           ```

        2. **Compare Using SSIM**
           ```javascript
           import { ssim } from 'ssim.js';

           async function compareSSIM(currentPath, baselinePath) {
             const current = await loadImage(currentPath);
             const baseline = await loadImage(baselinePath);

             // Calculate SSIM
             const ssimValue = ssim(current, baseline);

             return {
               algorithm: 'SSIM',
               score: ssimValue,
               similarity: (ssimValue * 100).toFixed(2) + '%'
             };
           }
           ```

        3. **Compare Using pHash**
           ```javascript
           import { pHash, hammingDistance } from 'phash';

           async function comparePHash(currentPath, baselinePath) {
             const currentHash = await pHash(currentPath);
             const baselineHash = await pHash(baselinePath);

             const distance = hammingDistance(currentHash, baselineHash);

             return {
               algorithm: 'pHash',
               distance: distance,
               similarity: ((64 - distance) / 64 * 100).toFixed(2) + '%'
             };
           }
           ```

        4. **Classify Changes Using Thresholds**

           **SSIM Thresholds:**
           | SSIM Score | Classification | Action |
           |------------|----------------|--------|
           | >= 0.95 | IDENTICAL | Auto-pass |
           | 0.85-0.95 | MINOR_CHANGE | Warning, review recommended |
           | < 0.85 | SIGNIFICANT_CHANGE | Error, requires approval |

           **pHash Thresholds:**
           | Hamming Distance | Classification | Action |
           |------------------|----------------|--------|
           | 0-5 bits | IDENTICAL | Auto-pass |
           | 6-10 bits | MINOR_CHANGE | Warning, review recommended |
           | 11-20 bits | SIGNIFICANT_CHANGE | Error, requires approval |
           | > 20 bits | MAJOR_CHANGE | Error, likely different content |

        5. **Determine Overall Status**
           ```javascript
           function classifyChange(ssimResult, pHashResult) {
             // Both algorithms must agree for auto-pass
             if (ssimResult.score >= 0.95 && pHashResult.distance <= 5) {
               return {
                 status: 'PASS',
                 severity: 'IDENTICAL',
                 message: 'No perceptual difference detected'
               };
             }

             // Warning if either algorithm detects minor change
             if (ssimResult.score >= 0.85 && pHashResult.distance <= 10) {
               return {
                 status: 'WARNING',
                 severity: 'MINOR_CHANGE',
                 message: 'Minor perceptual differences detected',
                 details: {
                   ssim: ssimResult.similarity,
                   phash: pHashResult.similarity
                 }
               };
             }

             // Error for significant changes
             return {
               status: 'ERROR',
               severity: 'SIGNIFICANT_CHANGE',
               message: 'Significant perceptual differences detected',
               details: {
                 ssim: ssimResult.similarity,
                 phash: pHashResult.similarity
               }
             };
           }
           ```

        6. **Generate Perceptual Diff Report**
           Create detailed comparison report with both algorithm results:

           ```markdown
           # Perceptual Diff Report

           ## Summary
           - Total Screenshots: {total}
           - Identical: {identical_count}
           - Minor Changes: {minor_count}
           - Significant Changes: {significant_count}

           ## Screenshot Comparisons

           ### {screen_name}
           - **SSIM Score**: {ssim_score} ({similarity}%)
           - **pHash Distance**: {phash_distance} bits ({similarity}%)
           - **Classification**: {severity}
           - **Status**: {status}

           #### Analysis
           {detailed_analysis_of_what_changed}
           ```

        ### Output Structure

        ```text
        .preview/reports/
        ├── perceptual-diff.md       # Markdown report
        ├── perceptual-diff.json     # Machine-readable results
        └── perceptual-diff.html     # Interactive visual comparison
        ```

        ### Exit Codes
        - **0**: All comparisons passed (SSIM >= 0.95, pHash <= 5 bits)
        - **1**: Warnings detected (minor changes)
        - **2**: Errors detected (significant changes requiring approval)

        ### Integration with CI/CD
        Use exit codes to gate deployments:
        ```yaml
        - name: Perceptual Diff Check
          run: ./scripts/perceptual-diff.sh
          continue-on-error: false  # Block on significant changes
        ```

        ### Why This Approach is Better
        - **Perceptual algorithms** ignore minor rendering differences (anti-aliasing, font hinting)
        - **Dual validation** (SSIM + pHash) reduces false positives
        - **Structural focus** detects layout changes, not just pixel differences
        - **Fast execution** (~100-200ms per comparison vs. 500ms+ for pixelmatch)

    - role: design-quality-validator
      role_group: REVIEW
      parallel: true
      depends_on: [wireframe-converter]
      priority: 20
      model_override: sonnet
      prompt: |
        Calculate Design Quality Score (DQS) for generated previews.
        Check: contrast ratios, typography hierarchy, spacing consistency.
        Verify accessibility: ARIA labels, keyboard navigation, focus indicators.
        Validate token usage and component pattern adherence.
        Generate DQS report with grade and issues list.

    - role: touch-target-validator
      role_group: REVIEW
      parallel: true
      depends_on: [wireframe-converter, component-previewer, device-frame-generator]
      priority: 7
      model_override: sonnet
      prompt: |
        ## Touch Target Validator

        ### Your Role
        Validate all interactive elements meet minimum touch target requirements per WCAG 2.1 AAA and platform guidelines.

        ### Standards
        | Platform | Minimum | Recommended | Spacing |
        |----------|---------|-------------|---------|
        | iOS (Apple HIG) | 44x44 CSS px | 44x44 | 8px |
        | Android (Material) | 48x48 dp | 48x48 | 8dp |
        | WCAG 2.1 AAA | 44x44 CSS px | 48x48 | - |

        ### Process
        1. Parse all preview HTML files (.preview/wireframes/, .preview/components/, .preview/framed/)
        2. Find interactive elements using selectors:
           ```javascript
           const INTERACTIVE_SELECTORS = [
             'button', 'a[href]', 'input', 'select', 'textarea',
             '[role="button"]', '[role="link"]', '[role="checkbox"]',
             '[role="radio"]', '[role="switch"]', '[role="tab"]',
             '[role="menuitem"]', '[role="option"]',
             '[onclick]', '[tabindex="0"]', '[tabindex]:not([tabindex="-1"])'
           ];
           ```
        3. Calculate bounding box size for each element
        4. Check spacing between adjacent interactive elements
        5. Generate validation report

        ### Validation Script
        Create `.preview/assets/touch-target-validator.js`:

        ```javascript
        class TouchTargetValidator {
          constructor(options = {}) {
            this.minSize = options.minSize || 44;
            this.minSpacing = options.minSpacing || 8;
            this.violations = [];
          }

          validate(container) {
            const selectors = [
              'button', 'a[href]', 'input', 'select', 'textarea',
              '[role="button"]', '[role="link"]', '[role="checkbox"]',
              '[role="radio"]', '[role="switch"]', '[role="tab"]',
              '[onclick]', '[tabindex="0"]'
            ];

            const elements = container.querySelectorAll(selectors.join(','));
            const rects = [];

            elements.forEach((el, index) => {
              const rect = el.getBoundingClientRect();
              const computedStyle = window.getComputedStyle(el);

              // Skip hidden elements
              if (computedStyle.display === 'none' ||
                  computedStyle.visibility === 'hidden' ||
                  rect.width === 0 || rect.height === 0) {
                return;
              }

              // Size check
              if (rect.width < this.minSize || rect.height < this.minSize) {
                this.violations.push({
                  type: 'SIZE',
                  element: this.describeElement(el),
                  actual: { width: Math.round(rect.width), height: Math.round(rect.height) },
                  required: this.minSize,
                  severity: this.getSeverity(rect.width, rect.height),
                  location: this.getLocation(el)
                });
              }

              rects.push({ el, rect, index });
            });

            // Spacing check between adjacent elements
            for (let i = 0; i < rects.length; i++) {
              for (let j = i + 1; j < rects.length; j++) {
                const spacing = this.calculateSpacing(rects[i].rect, rects[j].rect);
                if (spacing >= 0 && spacing < this.minSpacing) {
                  this.violations.push({
                    type: 'SPACING',
                    element1: this.describeElement(rects[i].el),
                    element2: this.describeElement(rects[j].el),
                    actual: Math.round(spacing),
                    required: this.minSpacing,
                    severity: 'warning'
                  });
                }
              }
            }

            return this.violations;
          }

          getSeverity(width, height) {
            const minDim = Math.min(width, height);
            if (minDim < 24) return 'critical';
            if (minDim < 32) return 'error';
            return 'warning';
          }

          calculateSpacing(rect1, rect2) {
            const horizontalGap = Math.max(rect1.left, rect2.left) -
                                  Math.min(rect1.right, rect2.right);
            const verticalGap = Math.max(rect1.top, rect2.top) -
                                Math.min(rect1.bottom, rect2.bottom);

            if (horizontalGap > 0 && verticalGap > 0) {
              return Math.sqrt(horizontalGap * horizontalGap + verticalGap * verticalGap);
            }
            return Math.max(horizontalGap, verticalGap);
          }

          describeElement(el) {
            const tag = el.tagName.toLowerCase();
            const id = el.id ? `#${el.id}` : '';
            const classes = el.className ? `.${el.className.split(' ').join('.')}` : '';
            const text = el.textContent?.trim().substring(0, 30) || '';
            return `<${tag}${id}${classes}>${text ? ` "${text}"` : ''}`;
          }

          getLocation(el) {
            const rect = el.getBoundingClientRect();
            return { x: Math.round(rect.x), y: Math.round(rect.y) };
          }

          generateReport() {
            const critical = this.violations.filter(v => v.severity === 'critical');
            const errors = this.violations.filter(v => v.severity === 'error');
            const warnings = this.violations.filter(v => v.severity === 'warning');

            return {
              summary: {
                total: this.violations.length,
                critical: critical.length,
                errors: errors.length,
                warnings: warnings.length,
                passed: this.violations.length === 0
              },
              violations: this.violations,
              grade: this.calculateGrade()
            };
          }

          calculateGrade() {
            const critical = this.violations.filter(v => v.severity === 'critical').length;
            const errors = this.violations.filter(v => v.severity === 'error').length;
            if (critical > 0) return 'F';
            if (errors > 3) return 'D';
            if (errors > 0) return 'C';
            if (this.violations.length > 5) return 'B';
            if (this.violations.length > 0) return 'A-';
            return 'A';
          }
        }
        ```

        ### Output Report
        Generate `.preview/reports/touch-targets.md`:

        ```markdown
        # Touch Target Validation Report

        **Preview**: {preview_name}
        **Device**: {device_id}
        **Standard**: WCAG 2.1 AAA (44x44px minimum)

        ## Summary

        | Severity | Count |
        |----------|-------|
        | Critical (< 24px) | {N} |
        | Error (< 32px) | {N} |
        | Warning (< 44px) | {N} |
        | Spacing Issues | {N} |

        **Grade**: {A/B/C/D/F}
        **Mobile Usability**: {Excellent/Good/Needs Work/Poor}

        ## Violations

        ### Critical

        | Element | Current Size | Required | Location |
        |---------|--------------|----------|----------|
        | {element_desc} | {W}x{H}px | 44x44px | ({x}, {y}) |

        ### Recommendations

        1. {specific_fix_recommendations}
        ```

        ### Integration with DQS
        Add touch target score to DQS calculation:
        - 10 points for touch target compliance
        - Deduct 3 points per critical violation
        - Deduct 1 point per error/warning

    # Wave 4: Multi-Device & Sharing (NEW)
    - role: multi-device-gallery
      role_group: OUTPUT
      parallel: true
      depends_on: [device-frame-generator, screenshot-capturer]
      priority: 3
      model_override: haiku
      prompt: |
        ## Multi-Device Gallery Generator

        ### Your Role
        Create synchronized multi-device comparison views for stakeholder review.

        ### Skip Condition
        Skip if --no-gallery flag is set or only one device was previewed.

        ### Gallery Types

        **1. Side-by-Side Comparison** (default)
        ```html
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            .device-comparison {
              display: flex;
              gap: 24px;
              padding: 24px;
              overflow-x: auto;
              background: #f5f5f5;
            }
            .device-column {
              flex: 0 0 auto;
              text-align: center;
            }
            .device-column h3 {
              margin: 0 0 16px;
              font-family: -apple-system, sans-serif;
            }
            .device-column iframe {
              border: none;
              border-radius: 8px;
              box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
          </style>
        </head>
        <body>
          <div class="device-comparison">
            {FOR device IN target_devices}
            <div class="device-column">
              <h3>{device.name}</h3>
              <iframe
                src="framed/{device.id}/{screen}.html"
                width="{device.viewport.width + device.bezel_width*2}"
                height="{device.viewport.height + device.bezel_width*2}">
              </iframe>
            </div>
            {/FOR}
          </div>
        </body>
        </html>
        ```

        **2. Synchronized Scroll View**
        ```javascript
        // sync-scroll.js
        class SyncScroll {
          constructor(iframes) {
            this.iframes = Array.from(iframes);
            this.syncing = false;
            this.init();
          }

          init() {
            this.iframes.forEach(iframe => {
              iframe.addEventListener('load', () => {
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                doc.addEventListener('scroll', (e) => this.onScroll(iframe, e));
              });
            });
          }

          onScroll(source, e) {
            if (this.syncing) return;
            this.syncing = true;

            const sourceDoc = source.contentDocument;
            const scrollPercent = sourceDoc.documentElement.scrollTop /
              (sourceDoc.documentElement.scrollHeight - sourceDoc.documentElement.clientHeight);

            this.iframes.forEach(iframe => {
              if (iframe === source) return;
              const doc = iframe.contentDocument;
              const maxScroll = doc.documentElement.scrollHeight - doc.documentElement.clientHeight;
              doc.documentElement.scrollTop = scrollPercent * maxScroll;
            });

            requestAnimationFrame(() => this.syncing = false);
          }
        }

        // Initialize on load
        new SyncScroll(document.querySelectorAll('.device-column iframe'));
        ```

        **3. Device Carousel**
        ```html
        <div class="device-carousel">
          <button class="carousel-prev" aria-label="Previous device">&#8592;</button>
          <div class="carousel-track">
            {device_frames}
          </div>
          <button class="carousel-next" aria-label="Next device">&#8594;</button>
          <div class="carousel-dots">
            {device_dots}
          </div>
        </div>

        <script>
          class DeviceCarousel {
            constructor(container) {
              this.track = container.querySelector('.carousel-track');
              this.items = this.track.children;
              this.current = 0;
              this.init(container);
            }

            init(container) {
              container.querySelector('.carousel-prev').onclick = () => this.prev();
              container.querySelector('.carousel-next').onclick = () => this.next();
              document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft') this.prev();
                if (e.key === 'ArrowRight') this.next();
              });
            }

            goto(index) {
              this.current = Math.max(0, Math.min(index, this.items.length - 1));
              this.track.style.transform = `translateX(-${this.current * 100}%)`;
              this.updateDots();
            }

            updateDots() {
              // Update dot indicators
            }

            prev() { this.goto(this.current - 1); }
            next() { this.goto(this.current + 1); }
          }
        </script>
        ```

        **4. Responsive Breakpoint Slider**
        ```html
        <div class="responsive-tester">
          <div class="breakpoint-controls">
            <input type="range" id="width-slider"
                   min="320" max="1920" value="375"
                   aria-label="Viewport width">
            <span class="current-width">375px</span>
            <div class="breakpoint-markers">
              <button data-width="320">XS</button>
              <button data-width="640">SM</button>
              <button data-width="768">MD</button>
              <button data-width="1024">LG</button>
              <button data-width="1280">XL</button>
              <button data-width="1536">2XL</button>
            </div>
          </div>
          <div class="preview-container">
            <iframe id="responsive-preview" src="{preview_url}" title="Responsive preview"></iframe>
          </div>
        </div>

        <script>
          const slider = document.getElementById('width-slider');
          const preview = document.getElementById('responsive-preview');
          const display = document.querySelector('.current-width');

          slider.oninput = (e) => {
            const width = e.target.value;
            preview.style.width = width + 'px';
            display.textContent = width + 'px';
          };

          document.querySelectorAll('.breakpoint-markers button').forEach(btn => {
            btn.onclick = () => {
              slider.value = btn.dataset.width;
              slider.dispatchEvent(new Event('input'));
            };
          });
        </script>
        ```

        ### Output Structure
        .preview/gallery/
        ├── index.html           # Main gallery navigation
        ├── comparison.html      # Side-by-side view
        ├── carousel.html        # Device carousel
        ├── responsive.html      # Breakpoint slider
        ├── sync-scroll.html     # Synchronized scrolling
        └── assets/
            ├── gallery.css
            ├── gallery.js
            └── sync-scroll.js

    - role: shareable-preview-deployer
      role_group: DEPLOY
      parallel: false
      depends_on: [multi-device-gallery, touch-target-validator]
      priority: 2
      prompt: |
        ## Shareable Preview Deployer

        ### Your Role
        Deploy interactive previews for stakeholder review with shareable links.

        ### Skip Condition
        Skip if --no-deploy flag is set or running in offline mode.

        ### Supported Platforms
        Check availability in order:
        1. **Firebase Hosting** (recommended for teams using Firebase)
        2. **Vercel** (recommended for frontend teams)
        3. **Cloudflare Pages** (recommended for performance)
        4. **Surge.sh** (simplest setup)
        5. **ngrok** (fallback for local sharing)

        ### Platform Detection
        ```bash
        # Check for available CLIs
        if command -v firebase &> /dev/null; then
          PLATFORM="firebase"
        elif command -v vercel &> /dev/null; then
          PLATFORM="vercel"
        elif command -v wrangler &> /dev/null; then
          PLATFORM="cloudflare"
        elif command -v surge &> /dev/null; then
          PLATFORM="surge"
        elif command -v ngrok &> /dev/null; then
          PLATFORM="ngrok"
        else
          PLATFORM="none"
        fi
        ```

        ### Deployment Commands

        **Firebase**:
        ```bash
        # Create preview channel (expires in 7 days)
        firebase hosting:channel:deploy preview-{feature_name} \
          --expires 7d \
          --only hosting \
          --project {project_id}
        ```

        **Vercel**:
        ```bash
        vercel deploy .preview/ \
          --name {project}-preview \
          --yes \
          --no-clipboard
        ```

        **Cloudflare Pages**:
        ```bash
        wrangler pages deploy .preview/ \
          --project-name {project}-preview \
          --branch preview-{feature}
        ```

        **Surge**:
        ```bash
        surge .preview/ {project}-preview.surge.sh
        ```

        **ngrok** (local tunnel):
        ```bash
        # Start local server first
        python -m http.server 3456 -d .preview/ &
        ngrok http 3456 --log stdout
        ```

        ### Pre-Deploy Optimization
        1. Minify HTML/CSS/JS
        2. Optimize images (convert to WebP, compress PNGs)
        3. Generate manifest.json for PWA support
        4. Create robots.txt (noindex for previews)
        5. Add expiration headers

        ### Password Protection
        If --password flag is set, inject a simple auth gate:
        - Store hashed password in sessionStorage after verification
        - Display access denied message for incorrect passwords
        - Use btoa for simple encoding (sufficient for preview protection)

        ### QR Code Generation
        Generate QR code for mobile testing using available tools:
        - qrcode-terminal npm package
        - Python qrcode library
        - ASCII art fallback for terminal display

        ### Output Summary
        ```markdown
        ## Preview Deployed

        **URL**: {preview_url}
        **Platform**: {platform}
        **Expires**: {expiration_date}

        ### QR Code (for mobile testing)
        [Generated QR code for the URL]

        ### Share Instructions
        1. Send the URL to stakeholders
        2. Preview works on any device with a browser
        3. Password: {password if set, otherwise "Not required"}

        ### Included Views
        - Main Preview: {url}/
        - Device Gallery: {url}/gallery/
        - Components: {url}/components/
        - Touch Target Report: {url}/reports/touch-targets.html

        ### Quick Links
        - Desktop View: {url}?viewport=desktop
        - Mobile View: {url}?viewport=mobile
        - Tablet View: {url}?viewport=tablet
        ```

    # =========================================================================
    # WAVE 5: QUALITY VALIDATION (NEW - v0.0.92)
    # =========================================================================
    # These subagents form the Mockup Quality Engine for Figma-quality mockups.
    # They provide automated quality validation, scoring, and improvement loops.
    #
    # Run with: speckit preview --validate-quality
    # =========================================================================

    - role: mockup-quality-analyzer
      role_group: REVIEW
      parallel: true
      depends_on: [wireframe-converter, component-previewer, screenshot-capturer]
      priority: 6
      model_override: sonnet
      prompt: |
        ## Mockup Quality Analyzer

        ### Your Role
        Analyze generated mockups using Claude Vision API for quality issues.
        You are the primary quality gatekeeper for visual output.

        ### Skip Condition
        Skip if --skip-quality flag is set or no screenshots exist.

        ### Analysis Dimensions

        #### 1. Visual Polish Check (25 points max)
        Analyze each screenshot for:
        - **Consistent spacing and alignment** (8 pts)
          - Elements aligned to grid
          - Uniform margins/padding
          - No orphaned elements
        - **Shadow and border consistency** (5 pts)
          - Same shadow style throughout
          - Consistent border radii
          - Unified elevation system
        - **Color harmony and palette adherence** (5 pts)
          - Colors from design system
          - No clashing combinations
          - Proper contrast ratios
        - **Typography hierarchy clarity** (4 pts)
          - Clear heading levels
          - Consistent font sizes
          - Proper line heights
        - **Professional, non-"AI" appearance** (3 pts)
          - No generic look
          - Unique visual identity
          - Polished details

        #### 2. Design Token Compliance (20 points max)
        Cross-reference with design.md:
        - Compare colors to defined palette (6 pts)
        - Verify spacing follows grid system (6 pts)
        - Check typography matches scale (5 pts)
        - Flag hardcoded values (3 pts)

        #### 3. Component Consistency (15 points max)
        Check across all screenshots:
        - Similar components styled consistently (5 pts)
        - Button/input styles match throughout (4 pts)
        - Icon style consistency (3 pts)
        - State styling uniformity (3 pts)

        #### 4. Layout Analysis (15 points max)
        Visual structure assessment:
        - Visual balance and weight distribution (5 pts)
        - White space usage (4 pts)
        - Content hierarchy clarity (3 pts)
        - Responsive adaptation quality (3 pts)

        ### Vision API Prompts

        For each screenshot, use these analysis prompts:

        ```text
        VISUAL_POLISH_PROMPT:
          Analyze this UI mockup for visual polish.

          Rate each dimension 0-10:
          1. Spacing consistency (are margins/padding uniform?)
          2. Alignment (are elements properly aligned to a grid?)
          3. Shadow/elevation (consistent shadow styles?)
          4. Color harmony (do colors work well together?)
          5. Typography (clear hierarchy, readable fonts?)
          6. Professional appearance (polished, not generic AI look?)

          Return JSON:
          {
            "spacing_score": number,
            "alignment_score": number,
            "shadow_score": number,
            "color_score": number,
            "typography_score": number,
            "professionalism_score": number,
            "issues": [
              {
                "type": string,
                "location": string,
                "description": string,
                "severity": "critical"|"warning"|"info"
              }
            ],
            "suggestions": string[]
          }
        ```

        ### Output
        Generate `.preview/reports/mqs-analysis.md`:

        ```markdown
        # Mockup Quality Analysis

        **Analyzed**: {timestamp}
        **Screenshots**: {count}

        ## Visual Fidelity Score: {score}/25

        ### Breakdown
        | Criterion | Score | Max | Notes |
        |-----------|-------|-----|-------|
        | Spacing & Alignment | {s} | 8 | {notes} |
        | Shadows & Borders | {s} | 5 | {notes} |
        | Color Harmony | {s} | 5 | {notes} |
        | Typography | {s} | 4 | {notes} |
        | Professionalism | {s} | 3 | {notes} |

        ## Issues Found

        ### Critical
        {list of critical issues with screenshots}

        ### Warnings
        {list of warnings}

        ## Improvement Suggestions
        1. {suggestion with specific location}
        2. {suggestion}
        ```

        Also generate annotated screenshots in `.preview/reports/annotated/`
        with issue locations marked.

    - role: token-compliance-validator
      role_group: REVIEW
      parallel: true
      depends_on: [wireframe-converter, component-previewer]
      priority: 7
      model_override: haiku
      prompt: |
        ## Token Compliance Validator

        ### Your Role
        Parse generated HTML/CSS and verify all values match design tokens.
        Ensure design system integrity by detecting hardcoded values.

        ### Skip Condition
        Skip if no design.md exists or --skip-token-check flag is set.

        ### Reference Document
        Read `templates/shared/token-patterns.md` for detection patterns.
        Read `templates/shared/mqs-rubric.md` for scoring rubric.

        ### Process

        1. **Extract Tokens from design.md**
           Parse design.md to find defined tokens:
           ```yaml
           color_tokens:
             - pattern: "--color-*"
             - values: ["--color-primary", "--color-secondary", ...]

           spacing_tokens:
             - pattern: "--space-*"
             - values: ["--space-1", "--space-2", ...]

           typography_tokens:
             - pattern: "--text-*, --font-*, --leading-*"
             - values: [...]
           ```

        2. **Scan Generated Files**
           Parse all files in `.preview/`:
           - `**/*.css` - CSS stylesheets
           - `**/*.html` - Inline styles
           - `**/*.tsx` - styled-components/Tailwind classes

        3. **Detect Violations**
           Using patterns from token-patterns.md:

           **Color Violations**:
           ```regex
           # Hex colors
           #[0-9a-fA-F]{3,8}\b

           # RGB/RGBA
           rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)
           rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)

           # HSL/HSLA
           hsl\(\s*\d+\s*,\s*[\d.]+%\s*,\s*[\d.]+%\s*\)
           ```

           **Spacing Violations**:
           ```regex
           # Hardcoded pixels (not 0)
           :\s*[1-9]\d*px(?:\s|;|$)

           # Magic numbers in margin/padding
           (margin|padding):\s*\d+px
           ```

           **Typography Violations**:
           ```regex
           font-size:\s*\d+(px|rem|em)
           font-weight:\s*\d{3}
           line-height:\s*[\d.]+
           ```

        4. **Calculate Compliance Score**
           ```
           compliance_rate = compliant_values / total_values
           token_score = compliance_rate × 20  # Max 20 points
           ```

        5. **Generate Auto-Fix Suggestions**
           For each violation, find nearest token:
           - Color: Find closest by deltaE color difference
           - Spacing: Find nearest value in scale
           - Typography: Map to type scale

        ### Output
        Generate `.preview/reports/token-compliance.md`:

        ```markdown
        ## Token Compliance Report

        **Scanned**: {file_count} files
        **Total Values**: {total_values}
        **Compliant**: {compliant_count} ({percentage}%)

        ### Score: {score}/20

        ### Summary by Category

        | Category | Compliant | Violations | Compliance |
        |----------|-----------|------------|------------|
        | Colors | {c_ok}/{c_total} | {c_violations} | {c_pct}% |
        | Spacing | {s_ok}/{s_total} | {s_violations} | {s_pct}% |
        | Typography | {t_ok}/{t_total} | {t_violations} | {t_pct}% |
        | Borders/Shadows | {b_ok}/{b_total} | {b_violations} | {b_pct}% |

        ### Violations

        #### Critical (Must Fix)

        | File | Line | Property | Found | Suggested Token |
        |------|------|----------|-------|-----------------|
        | button.css | 12 | color | #3b82f6 | var(--color-primary) |
        | card.css | 45 | padding | 13px | var(--space-3) |

        #### Warning (Should Fix)

        | File | Line | Property | Found | Suggested Token |
        |------|------|----------|-------|-----------------|
        | ... | ... | ... | ... | ... |

        ### Auto-Fix Available

        Run to apply automatic fixes:
        ```bash
        .preview/reports/token-fixes.sh
        ```

        Fixes that can be applied automatically:
        - [ ] button.css:12 - Replace #3b82f6 with var(--color-primary)
        - [ ] card.css:45 - Replace 13px with var(--space-3)
        ```

        Also generate `.preview/reports/token-fixes.sh` with sed commands.

    - role: accessibility-overlay-generator
      role_group: REVIEW
      parallel: true
      depends_on: [screenshot-capturer, touch-target-validator]
      priority: 5
      model_override: haiku
      prompt: |
        ## Accessibility Overlay Generator

        ### Your Role
        Generate annotated screenshots showing accessibility issues visually.
        Create overlays that make a11y issues immediately visible.

        ### Skip Condition
        Skip if --skip-a11y-overlay flag is set.

        ### Reference Document
        Read `templates/shared/a11y-overlay-styles.md` for overlay CSS.
        Read `templates/shared/mqs-rubric.md` for accessibility scoring.

        ### Overlay Types

        #### 1. Contrast Overlay
        Analyze text contrast and generate visual overlay:
        - **Red boxes**: Failed contrast (< 4.5:1 for text)
        - **Orange boxes**: Warning (4.5-7:1)
        - **Green checkmarks**: Passing (≥ 7:1)
        - Show actual ratio as label

        Implementation:
        ```javascript
        // For each text element
        function analyzeContrast(element) {
          const textColor = getComputedStyle(element).color;
          const bgColor = getEffectiveBackgroundColor(element);
          const ratio = calculateContrastRatio(textColor, bgColor);

          return {
            element: element,
            ratio: ratio.toFixed(2),
            status: ratio >= 7 ? 'pass' : ratio >= 4.5 ? 'warning' : 'fail',
            bounds: element.getBoundingClientRect()
          };
        }
        ```

        #### 2. Touch Target Overlay
        Visualize interactive element sizes:
        - **Red boxes**: Critical (< 24px)
        - **Orange boxes**: Too small (24-44px)
        - **Blue outlines**: Passing (≥ 44px)
        - Show dimensions as label
        - Draw 44px ghost box for small targets

        #### 3. Focus Indicator Overlay
        Check keyboard accessibility:
        - **Red dashed outline**: Missing focus state
        - **Orange outline**: Weak focus (low contrast)
        - **Green outline**: Good focus
        - Show tab order numbers

        #### 4. ARIA Overlay
        Validate semantic markup:
        - **Red badge "No label"**: Missing accessible name
        - **Orange badge "No role"**: Missing role attribute
        - **Green badge with role**: Correct implementation
        - Outline landmark regions (nav, main, footer)

        ### SVG Overlay Generation

        Generate SVG overlays that can be composited onto screenshots:

        ```xml
        <svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">
          <defs>
            <filter id="shadow">
              <feDropShadow dx="0" dy="1" stdDeviation="1" flood-opacity="0.2"/>
            </filter>
          </defs>

          <!-- Contrast issues -->
          <g id="contrast-layer">
            <rect x="{x}" y="{y}" width="{w}" height="{h}"
                  fill="none" stroke="#ef4444" stroke-width="2"/>
            <rect x="{x}" y="{y-18}" width="40" height="14"
                  fill="#ef4444" rx="2" filter="url(#shadow)"/>
            <text x="{x+4}" y="{y-7}" fill="white"
                  font-size="9" font-family="system-ui">3.2:1</text>
          </g>

          <!-- Touch targets -->
          <g id="touch-layer">
            <!-- 44px ghost for small targets -->
            <rect x="{cx-22}" y="{cy-22}" width="44" height="44"
                  fill="none" stroke="#94a3b8" stroke-dasharray="2,2"/>
          </g>
        </svg>
        ```

        ### Output Structure

        ```text
        .preview/accessibility/
        ├── {screen}-contrast.png       # Screenshot + contrast overlay
        ├── {screen}-contrast.svg       # Just the overlay
        ├── {screen}-touch-targets.png
        ├── {screen}-touch-targets.svg
        ├── {screen}-focus.png
        ├── {screen}-focus.svg
        ├── {screen}-aria.png
        ├── {screen}-aria.svg
        ├── {screen}-combined.png       # All overlays together
        ├── issues.json                 # Machine-readable issues
        └── report.html                 # Interactive report
        ```

        ### Interactive Report

        Generate HTML report with layer toggles:
        - Buttons to show/hide each overlay type
        - Summary cards showing issue counts
        - Clickable issues that highlight on screenshot
        - Export options (PNG, PDF)

        See `templates/shared/a11y-overlay-styles.md` for full HTML template.

        ### Accessibility Score Calculation

        ```
        a11y_score = (
          contrast_score +      # 0-6 points
          touch_target_score +  # 0-5 points
          focus_score +         # 0-4 points
          aria_score +          # 0-3 points
          motion_score          # 0-2 points
        )
        # Max: 20 points
        ```

    - role: state-matrix-generator
      role_group: FRONTEND
      parallel: true
      depends_on: [component-previewer]
      priority: 8
      prompt: |
        ## State Matrix Generator

        ### Your Role
        Generate preview pages showing all component states simultaneously.
        Create comprehensive visual testing surfaces for design QA.

        ### Skip Condition
        Skip if --skip-state-matrix flag is set or no components found.

        ### Matrix Layout Concept

        For each component, create a grid showing all combinations:

        ```text
        ┌─────────────────────────────────────────────────────────────┐
        │ Button Component - All States                                │
        ├─────────┬─────────┬─────────┬─────────┬─────────┬──────────┤
        │ Default │ Hover   │ Active  │ Focus   │Disabled │ Loading  │
        ├─────────┼─────────┼─────────┼─────────┼─────────┼──────────┤
        │Primary  │ [btn]   │ [btn]   │ [btn]   │ [btn]   │ [btn]    │
        │Secondary│ [btn]   │ [btn]   │ [btn]   │ [btn]   │ [btn]    │
        │Ghost    │ [btn]   │ [btn]   │ [btn]   │ [btn]   │ [btn]    │
        │Danger   │ [btn]   │ [btn]   │ [btn]   │ [btn]   │ [btn]    │
        ├─────────┴─────────┴─────────┴─────────┴─────────┴──────────┤
        │ Size Variants: sm | md | lg | xl                            │
        └─────────────────────────────────────────────────────────────┘
        ```

        ### Process

        1. **Parse Component Spec from design.md**
           Extract:
           - Component name
           - Variants (primary, secondary, ghost, etc.)
           - States (default, hover, active, focus, disabled, loading)
           - Sizes (sm, md, lg, xl)
           - Props that affect appearance

        2. **Generate State-Forcing CSS**
           Create CSS classes that force each state:

           ```css
           /* Force hover state */
           .force-hover:hover,
           .force-hover.--force-state {
             background: var(--color-primary-hover);
             /* ... hover styles */
           }

           /* Force active state */
           .force-active:active,
           .force-active.--force-state {
             background: var(--color-primary-active);
           }

           /* Force focus state */
           .force-focus:focus,
           .force-focus.--force-state {
             outline: 2px solid var(--color-focus);
             outline-offset: 2px;
           }

           /* Force disabled state */
           .force-disabled {
             opacity: 0.5;
             cursor: not-allowed;
             pointer-events: none;
           }

           /* Force loading state */
           .force-loading::after {
             content: "";
             /* spinner animation */
           }
           ```

        3. **Generate Matrix HTML**
           Create responsive grid layout:

           ```html
           <div class="state-matrix">
             <header class="matrix-header">
               <h1>{Component} - State Matrix</h1>
               <div class="controls">
                 <label><input type="checkbox" id="dark-mode"> Dark Mode</label>
                 <select id="size-filter">
                   <option value="all">All Sizes</option>
                   <option value="sm">Small</option>
                   <option value="md">Medium</option>
                   <option value="lg">Large</option>
                 </select>
               </div>
             </header>

             <table class="matrix-table">
               <thead>
                 <tr>
                   <th>Variant</th>
                   <th>Default</th>
                   <th>Hover</th>
                   <th>Active</th>
                   <th>Focus</th>
                   <th>Disabled</th>
                   <th>Loading</th>
                 </tr>
               </thead>
               <tbody>
                 <tr data-variant="primary">
                   <td>Primary</td>
                   <td><Button variant="primary" /></td>
                   <td><Button variant="primary" class="force-hover --force-state" /></td>
                   <!-- ... -->
                 </tr>
               </tbody>
             </table>

             <section class="size-variants">
               <h2>Size Variants</h2>
               <div class="size-row">
                 <Button size="sm">Small</Button>
                 <Button size="md">Medium</Button>
                 <Button size="lg">Large</Button>
                 <Button size="xl">Extra Large</Button>
               </div>
             </section>
           </div>
           ```

        4. **Add Interactive Controls**
           - Toggle between light/dark mode
           - Filter by size
           - Highlight specific states
           - Copy component code

        ### Output Structure

        ```text
        .preview/components/{name}/
        ├── matrix.html           # Full state matrix
        ├── matrix-screenshot.png # Screenshot of matrix
        ├── matrix.css            # State-forcing styles
        ├── states/
        │   ├── default.html      # Individual state pages
        │   ├── hover.html
        │   ├── active.html
        │   ├── focus.html
        │   ├── disabled.html
        │   └── loading.html
        └── variants/
            ├── primary.html      # Individual variant pages
            ├── secondary.html
            └── ...
        ```

        ### Interaction Score Calculation

        Based on state coverage:
        ```
        required_states = [default, hover, active, focus, disabled]
        optional_states = [loading, error, success]

        coverage = implemented_states / required_states
        interaction_score = coverage × 10  # Max 10 points
        ```

    - role: visual-regression-validator
      role_group: TESTING
      parallel: false
      depends_on: [screenshot-capturer]
      priority: 4
      prompt: |
        ## Visual Regression Validator

        ### Your Role
        Compare new screenshots against baseline for unexpected changes.
        Detect visual drift and prevent design regressions.

        ### Skip Condition
        Skip if --skip-regression flag is set or no baseline exists.

        ### Reference Document
        Read `templates/shared/visual-regression.md` for comparison algorithms.

        ### Process

        1. **Check for Baseline**
           ```bash
           if [ ! -d ".preview/baseline" ]; then
             echo "No baseline found. Creating initial baseline..."
             mkdir -p .preview/baseline
             cp .preview/screenshots/*.png .preview/baseline/
             echo "Baseline created. Run again to compare."
             exit 0
           fi
           ```

        2. **Compare Screenshots**
           For each current screenshot, find matching baseline:

           ```javascript
           async function compareScreenshots(currentPath, baselinePath) {
             const current = await loadImage(currentPath);
             const baseline = await loadImage(baselinePath);

             // Check dimensions
             if (current.width !== baseline.width ||
                 current.height !== baseline.height) {
               return {
                 match: false,
                 error: 'DIMENSION_MISMATCH',
                 current: { width: current.width, height: current.height },
                 baseline: { width: baseline.width, height: baseline.height }
               };
             }

             // Pixel comparison with threshold
             const threshold = 0.1;  // Color threshold
             let diffPixels = 0;
             const totalPixels = current.width * current.height;
             const diffData = new Uint8ClampedArray(totalPixels * 4);

             for (let i = 0; i < current.data.length; i += 4) {
               const colorDiff = colorDelta(
                 current.data.slice(i, i + 4),
                 baseline.data.slice(i, i + 4)
               );

               if (colorDiff > threshold) {
                 diffPixels++;
                 // Mark as different (magenta)
                 diffData[i] = 255;
                 diffData[i + 1] = 0;
                 diffData[i + 2] = 255;
                 diffData[i + 3] = 255;
               } else {
                 // Fade unchanged pixels
                 diffData[i] = current.data[i] * 0.3;
                 diffData[i + 1] = current.data[i + 1] * 0.3;
                 diffData[i + 2] = current.data[i + 2] * 0.3;
                 diffData[i + 3] = 255;
               }
             }

             const diffPercentage = (diffPixels / totalPixels) * 100;

             return {
               match: diffPercentage < 1,
               diffPixels,
               totalPixels,
               diffPercentage: diffPercentage.toFixed(2),
               diffImageData: diffData
             };
           }
           ```

        3. **Classify Changes**
           Based on diff percentage and region analysis:

           | Classification | Threshold | Action |
           |----------------|-----------|--------|
           | IDENTICAL | < 0.1% | Auto-pass |
           | RENDERING_VARIATION | 0.1-1% | Auto-pass (anti-aliasing, fonts) |
           | MINOR_CHANGE | 1-5% | Review recommended |
           | SIGNIFICANT_CHANGE | 5-20% | Block, require approval |
           | MAJOR_CHANGE | > 20% | Block, likely regression |

        4. **Generate Diff Images**
           Create visual diff for each changed screenshot:
           - Side-by-side: [Baseline] | [Current] | [Diff]
           - Overlay: Slider comparison
           - Highlighted: Bounding boxes around changes

        5. **Determine Overall Status**
           ```javascript
           function determineStatus(results) {
             const blocked = results.filter(r =>
               r.classification === 'SIGNIFICANT_CHANGE' ||
               r.classification === 'MAJOR_CHANGE'
             );

             if (blocked.length > 0) {
               return {
                 status: 'BLOCKED',
                 message: `${blocked.length} screenshots require approval`,
                 blockedScreenshots: blocked
               };
             }

             const warnings = results.filter(r =>
               r.classification === 'MINOR_CHANGE'
             );

             if (warnings.length > 0) {
               return {
                 status: 'WARNING',
                 message: `${warnings.length} screenshots have minor changes`,
                 warnings
               };
             }

             return {
               status: 'PASS',
               message: 'No visual regression detected'
             };
           }
           ```

        ### Output Structure

        ```text
        .preview/regression/
        ├── summary.md            # Overview of all changes
        ├── report.html           # Interactive comparison viewer
        ├── {screen}/
        │   ├── baseline.png      # Original baseline
        │   ├── current.png       # Current screenshot
        │   ├── diff.png          # Highlighted differences
        │   ├── side-by-side.png  # Three-way comparison
        │   └── analysis.json     # Detailed analysis
        └── approve.sh            # Script to accept changes
        ```

        ### Approval Script

        Generate shell script to accept changes as new baseline:
        ```bash
        #!/bin/bash
        # approve.sh - Accept current screenshots as new baseline

        echo "Updating baseline with current screenshots..."

        for screen in dashboard login settings; do
          if [ -f ".preview/regression/$screen/current.png" ]; then
            cp ".preview/regression/$screen/current.png" ".preview/baseline/$screen.png"
            echo "✓ Updated: $screen"
          fi
        done

        rm -rf .preview/regression
        echo "Baseline updated. Run preview again to verify."
        ```

        ### Thresholds (Configurable)

        ```yaml
        regression_thresholds:
          auto_pass: 1          # < 1% = auto approve
          review: 5             # 1-5% = flag for review
          block: 5              # > 5% = block and require approval
        ```

    - role: fidelity-scorer
      role_group: REVIEW
      parallel: true
      depends_on: [mockup-quality-analyzer, token-compliance-validator, accessibility-overlay-generator]
      priority: 3
      model_override: sonnet
      prompt: |
        ## Fidelity Scorer

        ### Your Role
        Calculate final Mockup Quality Score (MQS) from all validation results.
        You are the aggregator that produces the final quality verdict.

        ### Skip Condition
        Skip if --skip-mqs flag is set.

        ### Reference Document
        Read `templates/shared/mqs-rubric.md` for complete scoring rubric.

        ### MQS Formula

        ```
        MQS = (
          visual_fidelity_score × 0.25 +     # 0-25 points
          token_compliance_score × 0.20 +     # 0-20 points
          accessibility_score × 0.20 +        # 0-20 points
          responsiveness_score × 0.15 +       # 0-15 points
          interaction_score × 0.10 +          # 0-10 points
          polish_score × 0.10                 # 0-10 points
        )
        ```

        ### Input Sources

        Collect scores from other validators:

        ```yaml
        input_files:
          mockup-quality-analyzer:
            file: .preview/reports/mqs-analysis.md
            provides:
              - visual_fidelity_score
              - polish_score

          token-compliance-validator:
            file: .preview/reports/token-compliance.md
            provides:
              - token_compliance_score
              - violation_list

          accessibility-overlay-generator:
            file: .preview/accessibility/issues.json
            provides:
              - contrast_score
              - touch_target_score
              - focus_score
              - aria_score

          touch-target-validator:
            file: .preview/reports/touch-targets.md
            provides:
              - touch_target_details

          state-matrix-generator:
            file: .preview/components/*/matrix.html
            provides:
              - interaction_score
              - state_coverage

          screenshot-capturer:
            files: .preview/screenshots/
            provides:
              - responsiveness_score (compare across viewports)
        ```

        ### Score Extraction

        ```javascript
        async function collectScores() {
          const scores = {};

          // Visual Fidelity (from mockup-quality-analyzer)
          const mqsAnalysis = await readMarkdown('.preview/reports/mqs-analysis.md');
          scores.visual_fidelity = extractScore(mqsAnalysis, 'Visual Fidelity Score');

          // Token Compliance
          const tokenReport = await readMarkdown('.preview/reports/token-compliance.md');
          scores.token_compliance = extractScore(tokenReport, 'Score:');

          // Accessibility (aggregate from overlay generator)
          const a11yIssues = await readJSON('.preview/accessibility/issues.json');
          scores.accessibility = calculateA11yScore(a11yIssues);

          // Responsiveness (compare viewport screenshots)
          scores.responsiveness = await calculateResponsivenessScore();

          // Interaction (from state matrix coverage)
          scores.interaction = await calculateInteractionScore();

          // Polish (from mockup-quality-analyzer)
          scores.polish = extractScore(mqsAnalysis, 'Polish Score');

          return scores;
        }
        ```

        ### Responsiveness Calculation

        Compare screenshots across viewports:
        ```javascript
        function calculateResponsivenessScore() {
          const viewports = ['mobile', 'tablet', 'desktop'];
          let score = 15;  // Start with max

          for (const viewport of viewports) {
            const screenshots = glob(`.preview/screenshots/*-${viewport}.png`);

            for (const screenshot of screenshots) {
              // Check for layout issues
              const issues = analyzeLayoutForViewport(screenshot, viewport);

              if (issues.horizontalScroll) score -= 3;
              if (issues.overlappingElements) score -= 2;
              if (issues.textTooSmall) score -= 2;
              if (issues.touchTargetsTooSmall) score -= 2;
            }
          }

          return Math.max(0, score);
        }
        ```

        ### Quality Gates

        ```yaml
        gates:
          production_ready:
            threshold: 80
            message: "MQS ≥ 80: Production Ready ✓"
            action: proceed

          needs_polish:
            threshold: 60
            message: "MQS 60-79: Needs Polish"
            action: warn

          major_issues:
            threshold: 40
            message: "MQS 40-59: Major Issues"
            action: block

          regenerate:
            threshold: 0
            message: "MQS < 40: Regenerate"
            action: fail
        ```

        ### Output Report

        Generate `.preview/reports/mqs-report.md`:

        ```markdown
        # Mockup Quality Report

        **Generated**: {timestamp}
        **Feature**: {feature_name}
        **Screens Analyzed**: {count}

        ## Overall Score: {score}/100 ({status})

        ┌────────────────────┬───────┬────────┬─────────────────────┐
        │ Dimension          │ Score │ Weight │ Status              │
        ├────────────────────┼───────┼────────┼─────────────────────┤
        │ Visual Fidelity    │ {vf}  │ 25%    │ {vf_status}         │
        │ Token Compliance   │ {tc}  │ 20%    │ {tc_status}         │
        │ Accessibility      │ {a11y}│ 20%    │ {a11y_status}       │
        │ Responsiveness     │ {resp}│ 15%    │ {resp_status}       │
        │ Interaction Design │ {int} │ 10%    │ {int_status}        │
        │ Polish             │ {pol} │ 10%    │ {pol_status}        │
        ├────────────────────┼───────┼────────┼─────────────────────┤
        │ **TOTAL**          │ **{t}**│100%   │ {overall_status}    │
        └────────────────────┴───────┴────────┴─────────────────────┘

        ## Top Issues

        1. **{issue_1}** ({dimension}, -{points} pts)
           - Location: {file}:{line}
           - Fix: {suggestion}

        2. **{issue_2}** ({dimension}, -{points} pts)
           - Location: {file}:{line}
           - Fix: {suggestion}

        3. **{issue_3}** ({dimension}, -{points} pts)
           - Location: {file}:{line}
           - Fix: {suggestion}

        ## Auto-Fixable Issues

        | Issue | Location | Auto-Fix |
        |-------|----------|----------|
        | Hardcoded color | button.css:12 | → var(--color-primary) |
        | Touch target 32px | nav.css:45 | → min-height: 44px |
        | Missing hover | card.css:78 | → Add :hover rule |

        ## Quality Gate: {PASSED/FAILED}

        {gate_message}

        ---

        **Run `speckit preview --auto-improve` to automatically fix issues.**
        ```

        Also generate `.preview/reports/mqs-score.json` for CI integration.

    - role: mockup-improver
      role_group: GENERATION
      parallel: false
      depends_on: [fidelity-scorer]
      priority: 2
      prompt: |
        ## Mockup Improver

        ### Your Role
        Automatically fix common quality issues when MQS < 80.
        You are the auto-fix agent that improves mockup quality.

        ### Skip Condition
        Skip if --skip-auto-improve flag is set or MQS ≥ 80.

        ### Activation Condition

        ```javascript
        const mqsReport = await readJSON('.preview/reports/mqs-score.json');

        if (mqsReport.score >= 80) {
          console.log('MQS ≥ 80, skipping auto-improvement');
          return;
        }

        console.log(`MQS ${mqsReport.score} < 80, starting improvement loop`);
        ```

        ### Auto-Fix Categories

        #### 1. Token Replacement
        Replace hardcoded values with design tokens:

        ```javascript
        async function fixTokenViolations() {
          const violations = await readJSON('.preview/reports/token-violations.json');

          for (const violation of violations) {
            if (violation.autoFixable) {
              const { file, line, found, suggested } = violation;

              // Read file
              let content = await readFile(file);

              // Replace value
              content = content.replace(found, suggested);

              // Write back
              await writeFile(file, content);

              console.log(`Fixed: ${file}:${line} - ${found} → ${suggested}`);
            }
          }
        }
        ```

        #### 2. Accessibility Fixes
        Add missing accessibility features:

        ```javascript
        async function fixAccessibilityIssues() {
          const issues = await readJSON('.preview/accessibility/issues.json');

          for (const issue of issues) {
            switch (issue.type) {
              case 'touch-target-small':
                // Add min-height/min-width
                injectCSS(issue.selector, {
                  'min-height': '44px',
                  'min-width': '44px'
                });
                break;

              case 'missing-focus':
                // Add focus-visible styles
                injectCSS(`${issue.selector}:focus-visible`, {
                  'outline': '2px solid var(--color-focus)',
                  'outline-offset': '2px'
                });
                break;

              case 'low-contrast':
                // Suggest darker/lighter color
                // (requires manual review)
                break;
            }
          }
        }
        ```

        #### 3. Consistency Fixes
        Normalize styling across components:

        ```javascript
        async function fixConsistencyIssues() {
          // Normalize button padding
          const buttons = await findAll('.preview/**/*.css', /\.btn-/);
          const paddingValues = extractPaddingValues(buttons);

          if (paddingValues.length > 1) {
            const mostCommon = mode(paddingValues);
            for (const button of buttons) {
              if (button.padding !== mostCommon) {
                replaceValue(button.file, button.padding, mostCommon);
              }
            }
          }

          // Normalize border radii
          // Normalize icon sizes
          // etc.
        }
        ```

        #### 4. Polish Enhancements
        Add missing polish details:

        ```javascript
        async function addPolishEnhancements() {
          // Add missing hover states
          const interactiveElements = await findAll('.preview/**/*.css',
            /button|a\[href\]|input|select/);

          for (const element of interactiveElements) {
            if (!hasHoverState(element)) {
              injectHoverState(element, {
                'opacity': '0.9',
                'transform': 'translateY(-1px)'
              });
            }
          }

          // Add transitions
          const animatableElements = await findAll('.preview/**/*.css',
            /background|color|opacity|transform/);

          for (const element of animatableElements) {
            if (!hasTransition(element)) {
              injectCSS(element.selector, {
                'transition': 'all 0.15s ease'
              });
            }
          }
        }
        ```

        ### Improvement Loop

        Run up to 3 improvement cycles:

        ```javascript
        const MAX_ATTEMPTS = 3;
        let attempt = 0;
        let currentMQS = await getMQS();

        while (currentMQS < 80 && attempt < MAX_ATTEMPTS) {
          attempt++;
          console.log(`Improvement attempt ${attempt}/${MAX_ATTEMPTS}`);

          // Apply fixes
          await fixTokenViolations();
          await fixAccessibilityIssues();
          await fixConsistencyIssues();
          await addPolishEnhancements();

          // Re-capture screenshots
          await captureScreenshots();

          // Re-calculate MQS
          currentMQS = await recalculateMQS();

          console.log(`MQS after attempt ${attempt}: ${currentMQS}`);

          if (currentMQS >= 80) {
            console.log('✓ MQS threshold reached!');
            break;
          }
        }

        if (currentMQS < 80) {
          console.log('⚠ Could not reach MQS 80 after 3 attempts');
          console.log('Manual intervention required');
        }
        ```

        ### Output

        Generate improvement report:

        ```markdown
        ## Mockup Improvement Report

        **Initial MQS**: {initial_score}
        **Final MQS**: {final_score}
        **Improvement**: +{delta} points
        **Attempts**: {attempts}

        ### Fixes Applied

        | Category | Count | Impact |
        |----------|-------|--------|
        | Token Replacement | {n} | +{pts} pts |
        | Accessibility | {n} | +{pts} pts |
        | Consistency | {n} | +{pts} pts |
        | Polish | {n} | +{pts} pts |

        ### Before/After Comparison

        | Screen | Before | After |
        |--------|--------|-------|
        | Dashboard | ![](before/dashboard.png) | ![](after/dashboard.png) |
        | Login | ![](before/login.png) | ![](after/login.png) |

        ### Remaining Issues (Manual Fix Required)

        1. {issue_description} - {file}:{line}
        2. {issue_description} - {file}:{line}

        ### Recommendation

        {recommendation based on final MQS}
        ```

        Save before/after screenshots for comparison.

    # Wave Final: Reporting & Benchmarking
    - role: benchmark-reporter
      role_group: REPORTING
      parallel: false
      depends_on: [mockup-improver, quality-validator, perceptual-diff-validator]
      priority: 1
      model_override: haiku
      prompt: |
        ## Benchmark Reporter (v0.4.0)

        ### Your Role
        Aggregate all quality metrics into comprehensive benchmark dashboard.
        Provide trend analysis, competitive comparison, and actionable recommendations.

        ### Data Sources

        Collect metrics from all validation reports:
        1. **DQS Report**: `.preview/reports/dqs-total.md`
        2. **MQS Report**: `.preview/reports/mqs-score.json`
        3. **Token Compliance**: `.preview/reports/token-violations.json`
        4. **Touch Targets**: `.preview/accessibility/touch-targets.json`
        5. **Visual Regression**: `.preview/reports/visual-regression.md`
        6. **Lighthouse A11y**: `.preview/accessibility/lighthouse.json`
        7. **AutoFix Log**: `.preview/reports/autofix-log.md`

        ### Metric Aggregation

        ```javascript
        async function aggregateMetrics() {
          const dqs = await readDQSReport('.preview/reports/dqs-total.md');
          const mqs = await readJSON('.preview/reports/mqs-score.json');
          const tokens = await readJSON('.preview/reports/token-violations.json');
          const touchTargets = await readJSON('.preview/accessibility/touch-targets.json');
          const visualReg = await readMarkdown('.preview/reports/visual-regression.md');
          const lighthouse = await readJSON('.preview/accessibility/lighthouse.json');
          const autofix = await readMarkdown('.preview/reports/autofix-log.md');

          return {
            dqs: {
              total: dqs.total,
              visual_design: dqs.dimensions.visual_design,
              accessibility: dqs.dimensions.accessibility,
              components: dqs.dimensions.components,
              responsiveness: dqs.dimensions.responsiveness,
              token_compliance: dqs.dimensions.token_compliance,
              code_quality: dqs.dimensions.code_quality
            },
            mqs: {
              total: mqs.score,
              fidelity: mqs.fidelity,
              tokens: mqs.tokens,
              accessibility: mqs.accessibility,
              consistency: mqs.consistency,
              polish: mqs.polish
            },
            token_compliance: {
              violations: tokens.length,
              auto_fixed: tokens.filter(t => t.autoFixed).length,
              percentage: ((1 - tokens.length / totalElements) * 100).toFixed(1)
            },
            touch_targets: {
              total: touchTargets.length,
              passing: touchTargets.filter(t => t.width >= 44 && t.height >= 44).length,
              percentage: (touchTargets.filter(t => t.width >= 44 && t.height >= 44).length / touchTargets.length * 100).toFixed(1)
            },
            visual_regression: {
              ssim: parseFloat(visualReg.match(/SSIM: ([\d.]+)/)?.[1] || 0),
              phash: parseInt(visualReg.match(/pHash: (\d+) bits/)?.[1] || 0),
              status: visualReg.includes('IDENTICAL') ? 'pass' : 'warning'
            },
            lighthouse_a11y: {
              score: lighthouse.categories.accessibility.score * 100
            },
            autofix: {
              issues_detected: parseInt(autofix.match(/Issues Detected \((\d+)\)/)?.[1] || 0),
              fixes_applied: parseInt(autofix.match(/Fixes Applied \((\d+)\)/)?.[1] || 0),
              resolution_rate: 0
            }
          };
        }
        ```

        ### Benchmark Dashboard Generation

        Create `.preview/reports/benchmark-dashboard.html`:

        ```html
        <!DOCTYPE html>
        <html>
        <head>
          <title>Design Quality Benchmark Dashboard</title>
          <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
          <style>
            body {
              font-family: Inter, sans-serif;
              max-width: 1400px;
              margin: 0 auto;
              padding: 40px;
              background: #f9fafb;
            }
            .dashboard {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
              gap: 24px;
              margin-bottom: 40px;
            }
            .metric-card {
              background: white;
              padding: 24px;
              border-radius: 12px;
              box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .metric-value {
              font-size: 48px;
              font-weight: 700;
              margin: 16px 0;
            }
            .metric-label {
              font-size: 14px;
              color: #6b7280;
              text-transform: uppercase;
              letter-spacing: 0.05em;
            }
            .status-pass { color: #10b981; }
            .status-warn { color: #f59e0b; }
            .status-fail { color: #ef4444; }
            .radar-container {
              background: white;
              padding: 32px;
              border-radius: 12px;
              box-shadow: 0 1px 3px rgba(0,0,0,0.1);
              margin-bottom: 40px;
            }
            .trend-chart {
              background: white;
              padding: 32px;
              border-radius: 12px;
              box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .comparison-table {
              background: white;
              padding: 32px;
              border-radius: 12px;
              box-shadow: 0 1px 3px rgba(0,0,0,0.1);
              margin-top: 40px;
            }
            table {
              width: 100%;
              border-collapse: collapse;
            }
            th, td {
              text-align: left;
              padding: 12px;
              border-bottom: 1px solid #e5e7eb;
            }
            th {
              font-weight: 600;
              background: #f9fafb;
            }
          </style>
        </head>
        <body>
          <h1>Design Quality Benchmark Dashboard</h1>
          <p>Generated: {timestamp}</p>

          <div class="dashboard">
            <div class="metric-card">
              <div class="metric-label">DQS Total</div>
              <div class="metric-value status-{dqs_status}">{dqs_total}/100</div>
              <div>Target: 85+</div>
            </div>

            <div class="metric-card">
              <div class="metric-label">MQS Total</div>
              <div class="metric-value status-{mqs_status}">{mqs_total}/100</div>
              <div>Target: 80+</div>
            </div>

            <div class="metric-card">
              <div class="metric-label">Token Compliance</div>
              <div class="metric-value status-{token_status}">{token_percentage}%</div>
              <div>Target: 98%</div>
            </div>

            <div class="metric-card">
              <div class="metric-label">Touch Targets</div>
              <div class="metric-value status-{touch_status}">{touch_percentage}%</div>
              <div>Target: 100%</div>
            </div>

            <div class="metric-card">
              <div class="metric-label">Visual Regression</div>
              <div class="metric-value status-{visual_status}">{visual_ssim}</div>
              <div>SSIM Score (Target: ≥0.95)</div>
            </div>

            <div class="metric-card">
              <div class="metric-label">Lighthouse A11y</div>
              <div class="metric-value status-{lighthouse_status}">{lighthouse_score}</div>
              <div>Target: 90+</div>
            </div>

            <div class="metric-card">
              <div class="metric-label">AutoFix Resolution</div>
              <div class="metric-value status-{autofix_status}">{autofix_rate}%</div>
              <div>{autofix_fixed}/{autofix_total} issues</div>
            </div>

            <div class="metric-card">
              <div class="metric-label">First-Pass Success</div>
              <div class="metric-value status-{firstpass_status}">{firstpass_rate}%</div>
              <div>Target: 85%</div>
            </div>
          </div>

          <div class="radar-container">
            <h2>DQS Dimensions Radar</h2>
            <canvas id="radarChart"></canvas>
          </div>

          <div class="trend-chart">
            <h2>Quality Trend (Last 5 Generations)</h2>
            <canvas id="trendChart"></canvas>
          </div>

          <div class="comparison-table">
            <h2>Industry Benchmarks</h2>
            <table>
              <thead>
                <tr>
                  <th>Tool</th>
                  <th>DQS</th>
                  <th>Speed</th>
                  <th>Code Quality</th>
                  <th>A11y</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Spec Kit v0.4.0</strong></td>
                  <td class="status-{speckit_dqs_status}">{speckit_dqs}</td>
                  <td>{speckit_speed}</td>
                  <td>{speckit_code}</td>
                  <td>{speckit_a11y}%</td>
                </tr>
                <tr>
                  <td>Galileo AI</td>
                  <td>75</td>
                  <td>Fast</td>
                  <td>Medium</td>
                  <td>70%</td>
                </tr>
                <tr>
                  <td>v0.dev</td>
                  <td>80</td>
                  <td>Very Fast</td>
                  <td>High</td>
                  <td>85%</td>
                </tr>
                <tr>
                  <td>Builder.io</td>
                  <td>85</td>
                  <td>Medium</td>
                  <td>Very High</td>
                  <td>90%</td>
                </tr>
              </tbody>
            </table>
          </div>

          <script>
            // Radar Chart
            const radarCtx = document.getElementById('radarChart').getContext('2d');
            new Chart(radarCtx, {
              type: 'radar',
              data: {
                labels: ['Visual Design', 'Accessibility', 'Components', 'Responsiveness', 'Token Compliance', 'Code Quality'],
                datasets: [{
                  label: 'Current',
                  data: [{dqs_dimensions}],
                  backgroundColor: 'rgba(94, 106, 210, 0.2)',
                  borderColor: 'rgba(94, 106, 210, 1)',
                  pointBackgroundColor: 'rgba(94, 106, 210, 1)'
                }, {
                  label: 'Target',
                  data: [85, 85, 85, 85, 85, 85],
                  backgroundColor: 'rgba(16, 185, 129, 0.1)',
                  borderColor: 'rgba(16, 185, 129, 0.5)',
                  borderDash: [5, 5]
                }]
              },
              options: {
                scales: {
                  r: {
                    beginAtZero: true,
                    max: 100
                  }
                }
              }
            });

            // Trend Chart
            const trendCtx = document.getElementById('trendChart').getContext('2d');
            new Chart(trendCtx, {
              type: 'line',
              data: {
                labels: {trend_labels},
                datasets: [{
                  label: 'DQS',
                  data: {trend_dqs},
                  borderColor: 'rgba(94, 106, 210, 1)',
                  backgroundColor: 'rgba(94, 106, 210, 0.1)',
                  tension: 0.4
                }, {
                  label: 'MQS',
                  data: {trend_mqs},
                  borderColor: 'rgba(99, 91, 255, 1)',
                  backgroundColor: 'rgba(99, 91, 255, 0.1)',
                  tension: 0.4
                }]
              },
              options: {
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100
                  }
                },
                plugins: {
                  annotation: {
                    annotations: {
                      targetLine: {
                        type: 'line',
                        yMin: 85,
                        yMax: 85,
                        borderColor: 'rgba(16, 185, 129, 0.5)',
                        borderWidth: 2,
                        borderDash: [5, 5]
                      }
                    }
                  }
                }
              }
            });
          </script>
        </body>
        </html>
        ```

        ### Trend Analysis

        Load historical data from `.preview/reports/history/`:
        - Compare last 5 generations
        - Calculate improvement rate
        - Identify regressions

        ```javascript
        function analyzeTrends() {
          const history = loadHistory('.preview/reports/history/');
          const recent = history.slice(-5);

          return {
            dqs_trend: calculateTrend(recent.map(r => r.dqs)),
            mqs_trend: calculateTrend(recent.map(r => r.mqs)),
            improvement_rate: ((recent[4].dqs - recent[0].dqs) / 5).toFixed(1),
            regressions: findRegressions(recent)
          };
        }
        ```

        ### Actionable Recommendations

        Based on aggregated metrics, provide specific recommendations:

        ```markdown
        ## Recommendations

        ### Critical (DQS < 70)
        1. **Token Compliance**: {violation_count} hardcoded values detected
           - Run AutoFix: `/speckit.preview --autofix`
           - Review: `.preview/reports/token-violations.json`

        2. **Accessibility**: {a11y_issues} WCAG violations
           - Fix touch targets: {small_targets} buttons < 44×44px
           - Add ARIA labels: {missing_labels} interactive elements

        ### Improvements (DQS 70-84)
        1. **Visual Consistency**: {consistency_score}/25
           - Normalize button padding across components
           - Standardize border radius values

        2. **Responsiveness**: {responsive_score}/20
           - Test on mobile (375×812)
           - Fix overflow issues on tablet

        ### Optimization (DQS ≥ 85)
        - Consider variable fonts for performance (+15KB savings)
        - Enable glassmorphism for modern aesthetic
        - Add micro-interactions for polish
        ```

        ### Output

        Generate comprehensive report:
        1. **HTML Dashboard**: `.preview/reports/benchmark-dashboard.html`
        2. **JSON Metrics**: `.preview/reports/benchmark-metrics.json`
        3. **Markdown Summary**: `.preview/reports/benchmark-summary.md`
        4. **CSV Export**: `.preview/reports/benchmark-export.csv`

        Open dashboard in browser if `preview_config.auto_open: true`.

component_styling:
  default_library: "shadcn/ui"
  registry: "templates/shared/shadcn-registry.md"
  patterns:
    imports: "@/components/ui/{component}"
    variants: "class-variance-authority (cva)"
    utilities: "cn() from @/lib/utils"
    dark_mode: "Tailwind dark: class strategy"
    accessibility: "Radix UI primitives"
skills:
  - name: shadcn-registry
    trigger: "When generating any UI component"
    usage: "Read templates/shared/shadcn-registry.md for component patterns and imports"
  - name: wireframe-preview
    trigger: "When converting ASCII wireframes to visual HTML"
    usage: "Read templates/skills/wireframe-preview.md for conversion rules"
  - name: component-codegen
    trigger: "When generating React/Vue components from specs"
    usage: "Read templates/skills/component-codegen.md for generation templates"
  - name: v0-generation
    trigger: "When using v0.dev for component generation"
    usage: "Read templates/shared/v0-integration.md for API and prompts (generates shadcn/ui style)"
  - name: visual-regression
    trigger: "When capturing screenshots for baseline"
    usage: "Read templates/shared/visual-regression.md for Playwright setup"
preview_config:
  port: 3456
  output_dir: ".preview"
  screenshot_dir: ".preview/screenshots"
  auto_open: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

This command generates **interactive visual previews** from design specifications, enabling design validation without a human designer. It:

1. **Converts wireframes**: Transforms ASCII wireframes to visual HTML/React
2. **Generates components**: Creates production-ready components via v0.dev
3. **Captures screenshots**: Takes Playwright screenshots for all states/viewports
4. **Validates quality**: Runs Design Quality Score (DQS) checks
5. **Creates Storybook**: Auto-generates Storybook stories for components

**When to use**:
- After `/speckit.design` to visualize the design
- Before `/speckit.implement` to validate design decisions
- During design iteration to see changes
- For design review without Figma access

## Preview Types

| Type | Input | Output | Use Case |
|------|-------|--------|----------|
| Wireframe | ASCII wireframe in design.md | Visual HTML page | Quick layout validation |
| Component | Component spec in design.md | Interactive React component | State/variant testing |
| Flow | Screen flow in design.md | Multi-page navigation demo | User journey validation |
| Animation | Motion spec in design.md | Animated preview | Timing/easing review |
| Mockup | Stitch-generated mockups | Gallery with side-by-side comparison | High-fidelity visual validation |

## Outline

### 0. Preview Mode Detection (Adaptive Model Selection)

```text
# Detect preview mode from design.md content and CLI flags

IF adaptive_model.enabled = true AND --preview-mode flag not present:

  READ design.md → DESIGN_CONTENT

  # Analyze content for mode signals
  STATIC_SIGNALS = count_matches(DESIGN_CONTENT, adaptive_model.detection_signals.static)
  INTERACTIVE_SIGNALS = count_matches(DESIGN_CONTENT, adaptive_model.detection_signals.interactive)
  ANIMATED_SIGNALS = count_matches(DESIGN_CONTENT, adaptive_model.detection_signals.animated)

  # Determine mode (priority: animated > interactive > static)
  IF ANIMATED_SIGNALS >= 2:
    PREVIEW_MODE = "animated_preview"
  ELIF INTERACTIVE_SIGNALS >= 3:
    PREVIEW_MODE = "interactive_preview"
  ELSE:
    PREVIEW_MODE = "static_mockup"

  # Apply adaptive routing
  MODE_CONFIG = adaptive_model.mode_routing[PREVIEW_MODE]
  ORCHESTRATOR_MODEL = MODE_CONFIG.orchestrator
  THINKING_BUDGET = MODE_CONFIG.thinking_budget

  APPLY subagent_overrides from adaptive_model.subagent_overrides[PREVIEW_MODE]

  DISPLAY:
  ┌─────────────────────────────────────────┐
  │ Preview Mode: {PREVIEW_MODE}            │
  ├─────────────────────────────────────────┤
  │ Description: {MODE_CONFIG.description}  │
  │ Model:       {ORCHESTRATOR_MODEL}       │
  │ Opus cost:   $0.50                      │
  │ Selected:    ${SELECTED_COST}           │
  │ Savings:     {SAVINGS}%                 │
  └─────────────────────────────────────────┘

  REPORT: "Detected preview mode: {PREVIEW_MODE}"
  REPORT: "Using {ORCHESTRATOR_MODEL} for cost optimization"

ELSE IF --preview-mode flag present:
  PREVIEW_MODE = flag_value
  USE corresponding mode_routing configuration

ELSE:
  PREVIEW_MODE = "full"  # Default opus for all
  USE default model: opus
```

### 1. Load Configuration

```text
READ constitution.md:
  - design_system.preset → Load tokens
  - design_system.framework → Target framework
  - language → Artifact language

READ design.md:
  - Visual language → Color/typography tokens
  - Component specifications → Components to generate
  - Screen flows → Pages to preview
  - Motion specifications → Animations to include

DETERMINE preview_scope:
  IF user_input specifies component:
    scope = "component:{component_name}"
  ELIF user_input specifies screen:
    scope = "screen:{screen_name}"
  ELIF user_input specifies flow:
    scope = "flow:{flow_name}"
  ELSE:
    scope = "all"
```

### 1. Wireframe to Visual Conversion

```text
FOR EACH wireframe IN design.md:

  1. Parse ASCII wireframe structure:
     - Identify layout regions (header, sidebar, main, footer)
     - Extract component placeholders
     - Detect hierarchy (nesting levels)

  2. Map to HTML structure:
     ```
     +----------------------------------+    →    <header>
     |  [Header - Navigation context]   |    →      <nav>...</nav>
     +----------------------------------+    →    </header>
     |  [Sidebar]  |  [Main Content]    |    →    <div class="layout">
     |             |                    |    →      <aside>...</aside>
     +-------------+--------------------+    →      <main>...</main>
     ```

  3. Apply design tokens:
     - Background: var(--background)
     - Text: var(--foreground)
     - Spacing: var(--spacing-X)
     - Border radius: var(--radius-X)

  4. Generate HTML file:
     OUTPUT: .preview/wireframes/{screen_name}.html

  5. Include responsive meta + CSS variables
```

### 2. Component Preview Generation

```text
FOR EACH component IN design.md Component Specifications:

  1. Extract component definition:
     - States: default, hover, active, focus, disabled, loading, error
     - Variants: primary, secondary, ghost, etc.
     - Sizes: sm, md, lg
     - Props: documented properties

  2. Determine generation method:
     IF v0_api_available AND component.complexity == "high":
       method = "v0.dev"
       Read templates/shared/v0-integration.md
     ELSE:
       method = "template"
       Read templates/skills/component-codegen.md

  2.5. Apply shadcn/ui styling (DEFAULT):
     # All generated components use shadcn/ui patterns
     Read templates/shared/shadcn-registry.md
     styling_config = {
       import_base: "@/components/ui/",
       variant_system: "cva",  # class-variance-authority
       utility_merge: "cn()",  # clsx + tailwind-merge
       dark_mode: "class",     # Tailwind dark: prefix
       css_variables: true,    # Use CSS custom properties
       accessibility: "radix"  # Radix UI primitives
     }

     # Map component to shadcn/ui equivalent
     IF component.type IN shadcn_registry:
       base_component = shadcn_registry[component.type]
       LOG "📦 Using shadcn/ui base: {base_component}"

  3. Generate component code:
     v0_prompt = build_v0_prompt(component, design_tokens, styling_config)
     # v0.dev generates shadcn/ui style by default
     code = generate_component(method, v0_prompt)

  4. Create preview wrapper:
     - Import component
     - Render all states in grid
     - Render all variants
     - Add state toggle controls

  5. Output files:
     .preview/components/{component_name}/
     ├── {component_name}.tsx          # Component code
     ├── {component_name}.stories.tsx  # Storybook stories
     └── preview.html                  # Standalone preview
```

### 3. Flow Preview Generation

```text
FOR EACH flow IN design.md Screen Flows:

  1. Parse flow diagram (Mermaid):
     ```mermaid
     graph LR
       A[Welcome] --> B[Profile]
       B --> C[Preferences]
     ```

  2. Generate page for each node:
     - Use wireframe conversion for layout
     - Add navigation buttons for edges
     - Include transition animations

  3. Create flow runner:
     - Entry point: first node
     - Navigation: click to traverse edges
     - State persistence: maintain form data across screens

  4. Output:
     .preview/flows/{flow_name}/
     ├── index.html      # Flow entry
     ├── {screen_1}.html
     ├── {screen_2}.html
     └── flow.json       # Navigation config
```

### 4. Animation Preview

```text
FOR EACH animation IN design.md Motion Specifications:

  1. Parse animation spec:
     - Duration, easing, delay
     - Keyframes
     - Trigger (click, hover, load)

  2. Generate CSS keyframes:
     @keyframes {animation_name} { ... }

  3. Create demo element:
     - Element with animation applied
     - Play/pause control
     - Speed control (0.25x, 0.5x, 1x, 2x)
     - Frame-by-frame stepping

  4. Output:
     .preview/animations/{animation_name}.html
```

### 4.5. Stitch Mockup Gallery

```text
IF EXISTS(.preview/stitch-mockups/):

  1. Scan mockup directory:
     mockups = []
     FOR EACH feature_dir IN .preview/stitch-mockups/*/:
       FOR EACH screen_dir IN feature_dir/*/:
         mockup = {
           feature: feature_dir.name,
           screen: screen_dir.name,
           html: screen_dir/stitch-output.html,
           css: screen_dir/stitch-output.css,
           desktop: screen_dir/screenshot-desktop.png,
           mobile: screen_dir/screenshot-mobile.png,
           figma: screen_dir/figma-clipboard.json,
           prompt: screen_dir/prompt.txt
         }
         mockups.append(mockup)

  2. Generate mockup comparison pages:
     FOR EACH mockup IN mockups:

       # Find corresponding wireframe
       wireframe = find_wireframe(mockup.feature, mockup.screen)

       # Create side-by-side comparison page
       comparison_page = """
       <div class="mockup-comparison">
         <div class="comparison-header">
           <h2>{mockup.screen}</h2>
           <span class="feature-badge">{mockup.feature}</span>
         </div>

         <div class="comparison-grid">
           <div class="wireframe-panel">
             <h3>Wireframe</h3>
             <iframe src="{wireframe.html}"></iframe>
           </div>

           <div class="mockup-panel">
             <h3>Visual Mockup</h3>
             <iframe src="{mockup.html}"></iframe>
           </div>
         </div>

         <div class="mockup-assets">
           <a href="{mockup.desktop}" download>Desktop PNG</a>
           <a href="{mockup.mobile}" download>Mobile PNG</a>
           <button onclick="copyFigma('{mockup.figma}')">Copy to Figma</button>
           <a href="{mockup.html}" target="_blank">Open Full Screen</a>
         </div>

         <details class="prompt-details">
           <summary>Generation Prompt</summary>
           <pre>{read(mockup.prompt)}</pre>
         </details>
       </div>
       """

       OUTPUT: .preview/mockup-comparisons/{feature}/{screen}.html

  3. Generate mockup gallery index:
     gallery_index = """
     <h1>Visual Mockups Gallery</h1>

     <div class="gallery-stats">
       <span>Total Mockups: {mockups.length}</span>
       <span>Features: {unique_features.length}</span>
     </div>

     <div class="gallery-filters">
       <select id="feature-filter">
         <option value="all">All Features</option>
         {FOR feature IN unique_features: <option>{feature}</option>}
       </select>
       <button onclick="toggleView('grid')">Grid</button>
       <button onclick="toggleView('list')">List</button>
     </div>

     <div class="mockup-grid">
       {FOR mockup IN mockups:
         <div class="mockup-card" data-feature="{mockup.feature}">
           <img src="{mockup.desktop}" alt="{mockup.screen}">
           <div class="card-info">
             <h3>{mockup.screen}</h3>
             <span class="feature">{mockup.feature}</span>
           </div>
           <div class="card-actions">
             <a href="mockup-comparisons/{mockup.feature}/{mockup.screen}.html">
               Compare
             </a>
           </div>
         </div>
       }
     </div>
     """

     OUTPUT: .preview/stitch-mockups/gallery.html

  4. Include in main preview index:
     ADD link to .preview/stitch-mockups/gallery.html
     ADD mockup count to stats
```

### 5. Screenshot Capture

```text
FUNCTION capture_screenshots():

  viewports = [
    { name: "mobile", width: 375, height: 812 },
    { name: "tablet", width: 768, height: 1024 },
    { name: "desktop", width: 1440, height: 900 }
  ]

  themes = ["light", "dark"]  # If dark mode configured

  FOR EACH preview_file IN .preview/:
    FOR EACH viewport IN viewports:
      FOR EACH theme IN themes:

        1. Launch Playwright browser
        2. Set viewport size
        3. Set color scheme (prefers-color-scheme)
        4. Navigate to preview file
        5. Wait for animations to complete
        6. Capture screenshot

        OUTPUT: .preview/screenshots/{name}_{viewport}_{theme}.png

  FOR EACH component IN .preview/components/:
    FOR EACH state IN component.states:

      1. Navigate to component preview
      2. Trigger state (hover, focus, etc.)
      3. Capture screenshot

      OUTPUT: .preview/screenshots/{component}_{state}.png

  RETURN screenshot_manifest
```

### 6. Design Quality Score (DQS) Validation

```text
FUNCTION validate_dqs(previews, screenshots):

  score = 0
  issues = []

  # Visual Quality (40 points)
  FOR EACH screenshot IN screenshots:

    # Contrast check (via Claude Vision)
    contrast_result = vision_check(screenshot, "contrast_ratios")
    IF contrast_result.all_pass:
      score += 3
    ELSE:
      issues.append(f"Contrast issue: {contrast_result.failures}")

    # Typography hierarchy
    typography_result = vision_check(screenshot, "typography_hierarchy")
    score += typography_result.score  # 0-2

    # Spacing consistency
    spacing_result = vision_check(screenshot, "spacing_consistency")
    score += spacing_result.score  # 0-2

  # Accessibility (30 points)
  FOR EACH component IN components:

    # ARIA check
    IF component.has_aria_labels:
      score += 3
    ELSE:
      issues.append(f"{component.name}: Missing ARIA labels")

    # Keyboard check
    IF component.keyboard_navigable:
      score += 2

    # Focus indicator
    IF component.visible_focus:
      score += 2

  # Consistency (20 points)
  token_usage = check_css_for_tokens(previews)
  score += token_usage.score  # 0-10

  pattern_adherence = check_component_patterns(components)
  score += pattern_adherence.score  # 0-10

  # Implementation (10 points)
  typescript_check = lint_typescript(components)
  score += typescript_check.score  # 0-5

  code_quality = format_check(components)
  score += code_quality.score  # 0-5

  RETURN DQSResult(
    score=score,
    grade=calculate_grade(score),
    issues=issues,
    passed=score >= 80
  )
```

### 7. Storybook Generation

```text
IF storybook_enabled:

  FOR EACH component IN .preview/components/:

    story_template = """
    import type { Meta, StoryObj } from '@storybook/react'
    import { {ComponentName} } from './{component_name}'

    const meta: Meta<typeof {ComponentName}> = {
      title: 'Components/{ComponentName}',
      component: {ComponentName},
      parameters: {
        layout: 'centered',
      },
      tags: ['autodocs'],
    }

    export default meta
    type Story = StoryObj<typeof meta>

    export const Default: Story = {
      args: {
        {default_props}
      },
    }

    // Generate story for each variant
    {variant_stories}

    // Generate story for each state
    {state_stories}
    """

    OUTPUT: .preview/components/{component_name}/{component_name}.stories.tsx

  # Generate Storybook config if not exists
  IF NOT exists(.storybook/):
    generate_storybook_config()
```

### 8. Preview Server

```text
FUNCTION start_preview_server():

  1. Check if port 3456 available
     IF not available:
       port = find_available_port(3456, 3500)

  2. Start simple HTTP server:
     - Serve .preview/ directory
     - Enable hot reload for file changes
     - CORS enabled for local development

  3. Generate index page:
     .preview/index.html with:
     - Links to all wireframes
     - Links to all components
     - Links to all flows
     - Links to all animations
     - Links to Stitch mockups gallery (if exists)
     - DQS score badge
     - Screenshot gallery
     - Mockup comparison quick access (if mockups exist)

  4. Open browser (if auto_open enabled):
     open http://localhost:{port}

  RETURN server_url
```

## Validation Gates

Before completing, verify:

- [ ] All wireframes converted to HTML
- [ ] All components have preview files
- [ ] All component states captured in screenshots
- [ ] Screenshots taken for all viewports
- [ ] Stitch mockups gallery generated (if mockups exist)
- [ ] Mockup comparison pages created (if mockups exist)
- [ ] DQS score calculated
- [ ] Storybook stories generated (if enabled)
- [ ] Preview server accessible

## Output

After completion:

```text
## Preview Generated ✓

**Output Directory**: .preview/

### Files Generated

| Type | Count | Location |
|------|-------|----------|
| Wireframes | {N} | .preview/wireframes/ |
| Components | {N} | .preview/components/ |
| Flows | {N} | .preview/flows/ |
| Animations | {N} | .preview/animations/ |
| Mockups | {N} | .preview/stitch-mockups/ |
| Screenshots | {N} | .preview/screenshots/ |
| Stories | {N} | .preview/components/*/*.stories.tsx |

### Design Quality Score

| Category | Score | Max |
|----------|-------|-----|
| Visual Quality | {X} | 40 |
| Accessibility | {X} | 30 |
| Consistency | {X} | 20 |
| Implementation | {X} | 10 |
| **Total** | **{X}** | **100** |

**Grade**: {A/B/C/D/F}
**Status**: {Production Ready / Needs Work / Not Ready}

### Issues Found

{list of DQS issues if any}

### Preview Server

🌐 **URL**: http://localhost:{port}

- Wireframes: http://localhost:{port}/wireframes/
- Components: http://localhost:{port}/components/
- Flows: http://localhost:{port}/flows/
- Mockups: http://localhost:{port}/stitch-mockups/gallery.html
- Screenshots: http://localhost:{port}/screenshots/

### Recommended Next Steps

{IF score >= 80}
  - Run `/speckit.implement` to build the feature
  - Screenshots available as visual regression baseline
{ELSE}
  - Address DQS issues listed above
  - Run `/speckit.design` to refine design
  - Re-run `/speckit.preview` after fixes
{ENDIF}
```

## CLI API

### Presets

```bash
# Default: Full preview with quality, gallery, frames
speckit preview

# Quick iteration (skip quality, gallery, deploy)
speckit preview --quick

# CI/CD mode (headless, baseline check, strict gates)
speckit preview --ci

# Stakeholder review package (deploy, all devices)
speckit preview --review
```

### Core Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--component <name>` | Preview specific component | `--component Button` |
| `--screen <name>` | Preview specific screen | `--screen Dashboard` |
| `--device <id>` | Target device(s) | `--device iphone-15-pro` or `--device mobile` or `--device all` |
| `--theme <mode>` | Color theme | `--theme dark` |
| `--output <dir>` | Custom output directory | `--output ./preview` |
| `--port <num>` | Server port | `--port 4000` |
| `--deploy <platform>` | Deploy for sharing | `--deploy vercel` or `--deploy firebase` |
| `--password <secret>` | Password protect deployment | `--password review2026` |
| `--gate <score>` | Minimum MQS threshold | `--gate 80` (default) |
| `--skip <features>` | Skip specific features | `--skip quality,gallery` |
| `--only <features>` | Run only specific features | `--only storybook` |
| `--baseline <action>` | Baseline management | `--baseline update` or `--baseline check` |

### Alternative/Variant Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--alternative <N>` | Preview specific alternative from concept.md | `--alternative 2` |
| `--all-alternatives` | Generate preview gallery for ALL alternatives | `--all-alternatives` |
| `--variant <name>` | Preview specific variant | `--variant BALANCED` |
| `--all-variants` | Generate previews for all scope variants | `--all-variants` |
| `--compare` | Generate side-by-side comparison view | `--compare` |

### Feature Keywords

Use with `--skip` and `--only` flags:

| Keyword | What It Controls |
|---------|------------------|
| `quality` | MQS scoring, token check, a11y overlays, auto-improve |
| `gallery` | Multi-device comparison gallery |
| `frames` | Device bezels, notches, status bars |
| `gestures` | Touch gesture simulation |
| `deploy` | Shareable preview deployment |
| `storybook` | Component storybook generation |
| `mockups` | Stitch/v0 mockup gallery |
| `screenshots` | Screenshot capture |
| `regression` | Visual regression testing |
| `states` | Component state matrix |

### Usage Examples

```bash
# Full preview (default)
speckit preview

# Quick local iteration
speckit preview --quick

# Preview specific component
speckit preview --component Button

# Preview on specific device with frames
speckit preview --device iphone-15-pro

# Multi-device preview
speckit preview --device mobile,tablet

# CI pipeline with strict quality gate
speckit preview --ci --gate 85

# Stakeholder review with deploy
speckit preview --review

# Skip quality validation (faster)
speckit preview --skip quality

# Skip gallery and frames
speckit preview --skip gallery,frames

# Only generate storybook
speckit preview --only storybook

# Deploy with password protection
speckit preview --deploy vercel --password review2026

# Update visual regression baseline
speckit preview --baseline update

# Check against baseline (CI mode)
speckit preview --baseline check

# Dark mode only
speckit preview --theme dark

# Preview all concept alternatives
speckit preview --all-alternatives

# Preview specific alternative
speckit preview --alternative 2

# Preview with side-by-side comparison
speckit preview --all-alternatives --compare

# Preview specific variant
speckit preview --variant BALANCED

# Preview all variants
speckit preview --all-variants
```

### Preset Equivalents

| Preset | Equivalent Flags |
|--------|------------------|
| `--quick` | `--skip quality,gallery,deploy,frames` |
| `--ci` | `--no-open --baseline check --gate 80 --skip deploy` |
| `--review` | `--deploy --device all --gate 80` |

## Example

**User Input**: "Preview the onboarding wizard components"

**Process**:
1. Load design.md for onboarding feature
2. Find components: WizardStepper, OnboardingCard, StepIndicator
3. Generate each component via v0.dev
4. Create preview pages with all states
5. Capture screenshots (mobile, tablet, desktop × light, dark)
6. Calculate DQS score
7. Generate Storybook stories
8. Start preview server

**Output**:

```text
## Preview Generated ✓

### Files Generated

| Type | Count | Location |
|------|-------|----------|
| Wireframes | 5 | .preview/wireframes/ |
| Components | 3 | .preview/components/ |
| Screenshots | 36 | .preview/screenshots/ |
| Stories | 3 | .preview/components/*/*.stories.tsx |

### Design Quality Score

| Category | Score | Max |
|----------|-------|-----|
| Visual Quality | 38 | 40 |
| Accessibility | 28 | 30 |
| Consistency | 18 | 20 |
| Implementation | 9 | 10 |
| **Total** | **93** | **100** |

**Grade**: A
**Status**: Production Ready ✓

### Preview Server

🌐 **URL**: http://localhost:3456

Components:
- WizardStepper: http://localhost:3456/components/wizard-stepper/
- OnboardingCard: http://localhost:3456/components/onboarding-card/
- StepIndicator: http://localhost:3456/components/step-indicator/

### Recommended Next Steps

- Run `/speckit.implement` to build the feature
- Screenshots available as visual regression baseline at .preview/screenshots/
```

---

## Alternative Preview Generation

{{include: shared/alternative-parser.md}}

### When to Use

Use alternative/variant preview when:
- User runs `/speckit.preview --all-alternatives` or `/speckit.preview --alternative N`
- User runs `/speckit.preview --all-variants` or `/speckit.preview --variant NAME`
- User wants to compare visual designs across concept alternatives
- Stakeholder review requires seeing multiple product directions

### Prerequisites

1. **concept.md** must exist with:
   - Product Alternatives section (`### Alternative [N]:`) for `--alternative`/`--all-alternatives`
   - Concept Variants section (`### Variant: MINIMAL/BALANCED/AMBITIOUS`) for `--variant`/`--all-variants`

2. **Design artifacts** must exist in `specs/app-design/alternatives/` or `specs/app-design/variants/`
   - Run `/speckit.design --concept --all-alternatives` first if missing

### Output Structure

```text
.preview/
├── alternatives/
│   ├── index.html              # Gallery with alternative selector
│   ├── comparison.html         # Side-by-side comparison (if --compare)
│   ├── alt-1-conventional/
│   │   ├── wireframes/
│   │   ├── components/
│   │   ├── framed/
│   │   │   ├── iphone-15-pro.html
│   │   │   └── desktop.html
│   │   └── screenshots/
│   ├── alt-2-disruptive/
│   │   └── ...
│   └── alt-N-{strategy}/
│       └── ...
└── variants/
    ├── index.html              # Variant gallery
    ├── comparison.html         # Scope comparison
    ├── MINIMAL/
    │   └── ...
    ├── BALANCED/
    │   └── ...
    └── AMBITIOUS/
        └── ...
```

### Alternative Preview Workflow

```text
IF --all-alternatives:
  1. CHECK prerequisites:
     - concept.md exists with Product Alternatives section
     - Design artifacts exist in specs/app-design/alternatives/

     IF design artifacts missing:
       ERROR "No alternative designs found. Run /speckit.design --concept --all-alternatives first."

  2. PARSE alternatives from concept.md:
     alternatives = parse_alternatives(read_file("specs/concept.md"))

     FOR each alt in alternatives:
       alt_dir = "specs/app-design/alternatives/alt-{alt.number}-{slugify(alt.strategy_type)}/"

       IF NOT exists(alt_dir):
         WARN "Design for alternative {alt.number} not found, skipping"
         CONTINUE

       output_dir = ".preview/alternatives/alt-{alt.number}-{slugify(alt.strategy_type)}/"

       3. LOAD design artifacts:
          design_system = read_file(alt_dir + "design-system.md")
          features = glob(alt_dir + "features/*.md")
          screens = glob(alt_dir + "screens/*.md")

       4. GENERATE previews with alternative-specific tokens:
          # Apply design tokens from alternative's design-system.md
          FOR each screen in screens:
            generate_wireframe_preview(screen, design_system, output_dir + "wireframes/")

          FOR each feature in features:
            generate_component_previews(feature, design_system, output_dir + "components/")

          # Generate device frames
          generate_device_frames(output_dir + "wireframes/", output_dir + "framed/")

          # Capture screenshots
          capture_screenshots(output_dir + "framed/", output_dir + "screenshots/")

  5. GENERATE gallery index:
     gallery_html = generate_alternative_gallery(alternatives, {
       title: "Alternative Comparison Gallery",
       features: [
         "alternative_selector",    # Dropdown to switch alternatives
         "device_selector",         # Device frame picker
         "score_badges",            # Show score/40 per alternative
         "strategy_labels"          # Conventional/Disruptive/etc
       ]
     })
     write_file(".preview/alternatives/index.html", gallery_html)

  6. IF --compare:
     comparison_html = generate_side_by_side_comparison(alternatives, {
       layout: "horizontal_scroll",  # or "grid" for 2x2
       sync_scroll: true,            # Synchronized scrolling
       highlight_differences: true,  # Visual diff overlay
       include_scores: true
     })
     write_file(".preview/alternatives/comparison.html", comparison_html)

IF --alternative N:
  # Similar to above but for single alternative
  alt = parse_alternatives(concept_content).find(a => a.number == N)
  IF NOT alt:
    ERROR "Alternative {N} not found. Available alternatives: 1-{max}"

  # Generate preview for this alternative only
  generate_alternative_preview(alt)

IF --all-variants:
  1. CHECK prerequisites:
     - concept.md exists with Concept Variants section
     - Design artifacts exist in specs/app-design/variants/

  2. PARSE variants: ["MINIMAL", "BALANCED", "AMBITIOUS"]

     FOR each variant in variants:
       variant_dir = "specs/app-design/variants/{variant}/"
       output_dir = ".preview/variants/{variant}/"

       # Load and generate similar to alternatives
       generate_variant_preview(variant, variant_dir, output_dir)

  3. GENERATE variant gallery and comparison:
     - Show feature count per variant
     - Show timeline/effort per variant
     - Show risk level badges

IF --variant NAME:
  # Single variant preview
  validate NAME in ["MINIMAL", "BALANCED", "AMBITIOUS"]
  generate_variant_preview(NAME)
```

### Gallery Index Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name} - Alternative Gallery</title>
  <style>
    :root {
      --bg: #0f172a;
      --fg: #f8fafc;
      --border: #334155;
      --primary: {primary_color};
    }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: var(--bg);
      color: var(--fg);
    }
    .header {
      padding: 24px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .controls {
      display: flex;
      gap: 16px;
    }
    select {
      padding: 8px 16px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--fg);
      font-size: 14px;
    }
    .gallery {
      display: flex;
      gap: 24px;
      padding: 24px;
      overflow-x: auto;
      scroll-snap-type: x mandatory;
    }
    .alt-card {
      flex: 0 0 400px;
      scroll-snap-align: start;
      background: rgba(255,255,255,0.05);
      border-radius: 16px;
      overflow: hidden;
    }
    .alt-header {
      padding: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
    }
    .strategy-badge {
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
    }
    .strategy-badge.conventional { background: #3b82f6; }
    .strategy-badge.disruptive { background: #f59e0b; }
    .strategy-badge.premium { background: #8b5cf6; }
    .strategy-badge.minimal { background: #22c55e; }
    .strategy-badge.platform { background: #ec4899; }
    .score {
      font-size: 24px;
      font-weight: 700;
    }
    .score span { color: #64748b; font-size: 14px; }
    .preview-frame {
      padding: 16px;
    }
    .preview-frame iframe {
      width: 100%;
      height: 600px;
      border: none;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>Alternative Gallery</h1>
    <div class="controls">
      <select id="device-select">
        <option value="iphone-15-pro">iPhone 15 Pro</option>
        <option value="pixel-8">Pixel 8</option>
        <option value="desktop">Desktop</option>
      </select>
      <select id="theme-select">
        <option value="light">Light Mode</option>
        <option value="dark">Dark Mode</option>
      </select>
    </div>
  </div>

  <div class="gallery" id="gallery">
    <!-- Generated per alternative -->
    {{#each alternatives}}
    <div class="alt-card">
      <div class="alt-header">
        <div>
          <h3>Alternative {{number}}</h3>
          <span class="strategy-badge {{strategy_class}}">{{strategy_type}}</span>
        </div>
        <div class="score">{{score}}<span>/40</span></div>
      </div>
      <div class="preview-frame">
        <iframe src="./alt-{{number}}-{{strategy_slug}}/framed/{{device}}.html"></iframe>
      </div>
    </div>
    {{/each}}
  </div>

  <script>
    const gallery = document.getElementById('gallery');
    const deviceSelect = document.getElementById('device-select');
    const themeSelect = document.getElementById('theme-select');

    deviceSelect.addEventListener('change', updatePreviews);
    themeSelect.addEventListener('change', updatePreviews);

    function updatePreviews() {
      const device = deviceSelect.value;
      const theme = themeSelect.value;
      document.querySelectorAll('.preview-frame iframe').forEach((iframe, i) => {
        const altNum = i + 1;
        iframe.src = `./alt-${altNum}-${alternatives[i].slug}/framed/${device}.html?theme=${theme}`;
      });
    }
  </script>
</body>
</html>
```

### Side-by-Side Comparison Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name} - Alternative Comparison</title>
  <style>
    :root {
      --bg: #0f172a;
      --fg: #f8fafc;
      --border: #334155;
    }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--fg);
    }
    .comparison-header {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      z-index: 100;
      background: var(--bg);
      border-bottom: 1px solid var(--border);
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
    }
    .comparison-grid {
      display: grid;
      grid-template-columns: repeat({{alt_count}}, 1fr);
      gap: 1px;
      background: var(--border);
      margin-top: 60px;
    }
    .comparison-column {
      background: var(--bg);
      min-height: 100vh;
    }
    .column-header {
      position: sticky;
      top: 60px;
      background: var(--bg);
      padding: 16px;
      border-bottom: 1px solid var(--border);
      z-index: 50;
    }
    .sync-scroll {
      overflow-y: auto;
      max-height: calc(100vh - 120px);
    }
    .sync-scroll.synced {
      overflow: hidden;
    }
    .diff-highlight {
      position: absolute;
      background: rgba(239, 68, 68, 0.2);
      border: 2px solid #ef4444;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <div class="comparison-header">
    <h1>Side-by-Side Comparison</h1>
    <label>
      <input type="checkbox" id="sync-scroll" checked> Sync Scroll
    </label>
  </div>

  <div class="comparison-grid">
    {{#each alternatives}}
    <div class="comparison-column">
      <div class="column-header">
        <h3>Alt {{number}}: {{name}}</h3>
        <span>{{strategy_type}} • {{score}}/40</span>
      </div>
      <div class="sync-scroll synced" data-alt="{{number}}">
        <iframe src="./alt-{{number}}-{{strategy_slug}}/framed/{{device}}.html"
                style="width: 100%; height: 800px; border: none;"></iframe>
      </div>
    </div>
    {{/each}}
  </div>

  <script>
    const syncCheckbox = document.getElementById('sync-scroll');
    const scrollContainers = document.querySelectorAll('.sync-scroll');

    syncCheckbox.addEventListener('change', (e) => {
      scrollContainers.forEach(el => {
        el.classList.toggle('synced', e.target.checked);
      });
    });

    // Synchronized scrolling
    scrollContainers.forEach(container => {
      container.addEventListener('scroll', (e) => {
        if (!syncCheckbox.checked) return;
        const scrollTop = e.target.scrollTop;
        scrollContainers.forEach(other => {
          if (other !== e.target) {
            other.scrollTop = scrollTop;
          }
        });
      });
    });
  </script>
</body>
</html>
```

### Completion Summary

When alternative preview generation completes, output:

```text
## Alternative Preview Generated ✓

### Alternatives Processed

| Alt | Strategy | Score | Screens | Components | Status |
|-----|----------|-------|---------|------------|--------|
| 1 | Conventional | 32/40 | 5 | 12 | ✓ |
| 2 | Disruptive | 28/40 | 7 | 15 | ✓ |
| 3 | Premium | 35/40 | 6 | 18 | ✓ |

### Files Generated

| Type | Count | Location |
|------|-------|----------|
| Wireframes | 18 | .preview/alternatives/alt-*/wireframes/ |
| Components | 45 | .preview/alternatives/alt-*/components/ |
| Device Frames | 54 | .preview/alternatives/alt-*/framed/ |
| Screenshots | 162 | .preview/alternatives/alt-*/screenshots/ |
| Gallery | 1 | .preview/alternatives/index.html |
| Comparison | 1 | .preview/alternatives/comparison.html |

### Gallery URL

🌐 **http://localhost:3456/alternatives/**

- **Gallery View**: http://localhost:3456/alternatives/index.html
- **Side-by-Side**: http://localhost:3456/alternatives/comparison.html
- **Alt 1**: http://localhost:3456/alternatives/alt-1-conventional/
- **Alt 2**: http://localhost:3456/alternatives/alt-2-disruptive/
- **Alt 3**: http://localhost:3456/alternatives/alt-3-premium/

### Recommended Next Steps

- Review alternatives in gallery to select preferred direction
- Run `/speckit.design --alternative N` to refine chosen alternative
- Run `/speckit.specify` to create detailed spec for selected approach
```

---

## Integration with Vision Validation

The DQS validation uses Claude Vision to analyze screenshots:

```text
VISION_CHECKS:

  contrast_ratios:
    prompt: |
      Analyze this UI screenshot for color contrast issues.
      Check text against backgrounds.
      Report any elements with contrast ratio < 4.5:1.
      Return: { pass: boolean, issues: string[] }

  typography_hierarchy:
    prompt: |
      Analyze the visual hierarchy of text in this screenshot.
      Check if headings are visually distinct from body text.
      Check if font sizes follow logical progression.
      Return: { score: 0-2, feedback: string }

  spacing_consistency:
    prompt: |
      Analyze spacing in this UI screenshot.
      Check if spacing follows a consistent system.
      Identify any irregular gaps or crowded areas.
      Return: { score: 0-2, feedback: string }

  touch_targets:
    prompt: |
      Analyze interactive elements in this mobile screenshot.
      Check if buttons/links appear to be at least 44x44px.
      Identify any elements that look too small to tap.
      Return: { pass: boolean, issues: string[] }
```

## Dependencies

For full functionality, the preview system requires:

```json
{
  "devDependencies": {
    "playwright": "^1.40.0",
    "@storybook/react": "^7.6.0",
    "vite": "^5.0.0"
  }
}
```

If dependencies are missing, the command will:
1. Warn about missing capabilities
2. Skip screenshot capture if Playwright missing
3. Skip Storybook if @storybook/react missing
4. Still generate HTML previews (no dependencies needed)

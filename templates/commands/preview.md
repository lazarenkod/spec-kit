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
  model: opus
  reasoning_mode: extended
  thinking_budget: 16000
  cache_hierarchy: full
  orchestration:
    max_parallel: 3
    fail_fast: true
    wave_overlap:
      enabled: true
      overlap_threshold: 0.80
  subagents:
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
        Capture Playwright screenshots for all previews.
        Use viewports: mobile (375x812), tablet (768x1024), desktop (1440x900).
        Capture both light and dark themes if configured.
        For components, capture each state (hover, focus, disabled, etc.).
        Output to .preview/screenshots/.

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

skills:
  - name: wireframe-preview
    trigger: "When converting ASCII wireframes to visual HTML"
    usage: "Read templates/skills/wireframe-preview.md for conversion rules"
  - name: component-codegen
    trigger: "When generating React/Vue components from specs"
    usage: "Read templates/skills/component-codegen.md for generation templates"
  - name: v0-generation
    trigger: "When using v0.dev for component generation"
    usage: "Read templates/shared/v0-integration.md for API and prompts"
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

### 0. Load Configuration

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

  3. Generate component code:
     v0_prompt = build_v0_prompt(component, design_tokens)
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

## CLI Flags

```bash
# Preview specific component
speckit preview --component Button

# Preview specific screen
speckit preview --screen Dashboard

# Skip screenshot capture (faster)
speckit preview --no-screenshots

# Skip DQS validation
speckit preview --no-validation

# Generate Storybook only
speckit preview --storybook-only

# Specify output directory
speckit preview --output ./my-preview

# Specify port
speckit preview --port 4000

# Don't auto-open browser
speckit preview --no-open

# Dark mode only
speckit preview --theme dark

# Specific viewport only
speckit preview --viewport mobile

# Serve Stitch mockups gallery only
speckit preview --mockups

# Serve mockups with comparison view
speckit preview --mockups --compare

# Filter mockups by feature
speckit preview --mockups --feature onboarding

# === Device-Specific Preview (NEW) ===

# Preview on specific device
speckit preview --device iphone-14-pro
speckit preview --device pixel-8

# Preview on multiple devices
speckit preview --device iphone-14-pro,pixel-8,ipad-pro

# Preview on device category (all devices in category)
speckit preview --devices mobile          # All mobile devices
speckit preview --devices tablet          # All tablets
speckit preview --devices desktop         # All desktop devices
speckit preview --devices all             # Every device in registry

# Add device frames (bezels, status bar, notch)
speckit preview --framed
speckit preview --device iphone-14-pro --framed

# Show safe area debug overlay
speckit preview --framed --debug

# === Touch & Gestures (NEW) ===

# Enable gesture simulator (tap, swipe, pinch, etc.)
speckit preview --gestures
speckit preview --device mobile --gestures

# Disable gestures (for desktop-only previews)
speckit preview --no-gestures

# === Touch Target Validation (NEW) ===

# Run touch target validation
speckit preview --validate-touch-targets

# Skip touch target validation
speckit preview --no-touch-validation

# Set custom minimum touch target size (default: 44px)
speckit preview --min-touch-target 48

# === Multi-Device Gallery (NEW) ===

# Generate device comparison gallery
speckit preview --gallery

# Gallery with synchronized scrolling
speckit preview --gallery --sync-scroll

# Gallery with responsive breakpoint slider
speckit preview --gallery --responsive

# Skip gallery generation
speckit preview --no-gallery

# === Preview Deployment (NEW) ===

# Deploy preview for sharing
speckit preview --deploy
speckit preview --deploy firebase
speckit preview --deploy vercel
speckit preview --deploy cloudflare
speckit preview --deploy surge

# Deploy with password protection
speckit preview --deploy --password secret123

# Set deployment expiration (default: 7d)
speckit preview --deploy --expires 14d

# Skip deployment
speckit preview --no-deploy

# === Orientation (NEW) ===

# Generate both orientations
speckit preview --orientation both

# Portrait only (default for mobile)
speckit preview --orientation portrait

# Landscape only
speckit preview --orientation landscape

# === Combined Examples ===

# Full mobile-focused preview with frames and gestures
speckit preview --device iphone-14-pro --framed --gestures

# Multi-device comparison with deployment
speckit preview --devices mobile --gallery --deploy firebase

# Quick local preview without extras
speckit preview --no-framed --no-gestures --no-gallery

# Complete stakeholder review package
speckit preview --devices all --framed --gallery --deploy --password review2026
```

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

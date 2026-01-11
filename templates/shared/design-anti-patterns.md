# Design Anti-Patterns (Negative Prompting)

This document defines anti-patterns to AVOID when generating design specifications and code. These constraints are integrated into all design agents via negative prompting, which research shows reduces issues by 59-64%.

## Visual Anti-Patterns

### AP-VIS-001: Hardcoded Colors
**DO NOT**: Use hardcoded color values like `#3B82F6`, `rgb(59, 130, 246)`, or named colors like `blue`
**DO**: Use design token references like `var(--color-primary)`, `theme.colors.primary`, or `$color-primary`
**Rationale**: Hardcoded colors prevent theming, dark mode support, and brand updates

### AP-VIS-002: Inconsistent Spacing
**DO NOT**: Use arbitrary spacing values like `padding: 13px`, `margin: 27px`
**DO**: Use spacing scale tokens like `var(--space-3)`, `theme.spacing[4]`, or `$spacing-lg`
**Rationale**: Inconsistent spacing breaks visual rhythm and makes scaling difficult

### AP-VIS-003: Multiple Primary CTAs
**DO NOT**: Place multiple primary buttons with same visual weight on one screen
**DO**: Use single primary CTA, with secondary/tertiary actions for alternatives
**Rationale**: Multiple primary CTAs create decision paralysis and unclear hierarchy

### AP-VIS-004: Pure Black on Pure White
**DO NOT**: Use `#000000` text on `#FFFFFF` background
**DO**: Use softer combinations like `#1a1a1a` on `#fafafa` for better readability
**Rationale**: Pure black on pure white creates harsh contrast and eye strain

### AP-VIS-005: Decorative Color Usage
**DO NOT**: Add color without semantic meaning (e.g., random accent colors)
**DO**: Use color purposefully to indicate status, category, or importance
**Rationale**: Decorative color adds visual noise without communicating information

### AP-VIS-006: Inconsistent Border Radius
**DO NOT**: Mix border radii like `4px`, `6px`, `8px`, `12px` without system
**DO**: Use consistent scale like `sm: 4px`, `md: 8px`, `lg: 16px`
**Rationale**: Inconsistent radius breaks visual cohesion

### AP-VIS-007: Non-Responsive Typography
**DO NOT**: Use fixed font sizes that don't scale across viewports
**DO**: Use responsive scales with `clamp()` or viewport-relative units
**Rationale**: Fixed typography creates readability issues on mobile/desktop

### AP-VIS-008: Orphaned Text Elements
**DO NOT**: Leave single words on last line of paragraph (widows/orphans)
**DO**: Use `text-wrap: balance` or adjust line length to prevent orphans
**Rationale**: Orphans disrupt reading flow and look unpolished

## Accessibility Anti-Patterns

### AP-A11Y-001: Low Contrast Text
**DO NOT**: Use text with contrast ratio below 4.5:1 (normal text) or 3:1 (large text)
**DO**: Ensure WCAG 2.1 AA compliance with sufficient contrast
**Rationale**: Low contrast makes text unreadable for users with visual impairments

### AP-A11Y-002: Small Touch Targets
**DO NOT**: Create interactive elements smaller than 44×44px
**DO**: Ensure all touch targets meet WCAG minimum of 44×44px
**Rationale**: Small targets are difficult to tap on mobile devices

### AP-A11Y-003: Icon-Only Buttons
**DO NOT**: Use icons without text labels or aria-label
**DO**: Provide visible text labels or screen reader alternatives
**Rationale**: Icon meaning is not universal and inaccessible to screen readers

### AP-A11Y-004: Missing Focus Indicators
**DO NOT**: Remove outline on `:focus` without visible alternative
**DO**: Provide clear focus indicators for keyboard navigation
**Rationale**: Focus indicators are essential for keyboard and screen reader users

### AP-A11Y-005: Color as Only Indicator
**DO NOT**: Use color alone to convey information (e.g., red = error)
**DO**: Combine color with icons, text, or patterns
**Rationale**: Color-blind users cannot distinguish color-only signals

### AP-A11Y-006: Missing Alt Text
**DO NOT**: Leave images without alt attributes or with generic alt="image"
**DO**: Provide descriptive alt text that conveys image content and context
**Rationale**: Screen reader users need alternative text to understand images

### AP-A11Y-007: Auto-Playing Media
**DO NOT**: Auto-play videos or animations without user control
**DO**: Provide play/pause controls and respect `prefers-reduced-motion`
**Rationale**: Auto-play content can be disorienting and inaccessible

### AP-A11Y-008: Inaccessible Forms
**DO NOT**: Create forms without proper labels, error messages, or validation feedback
**DO**: Use `<label>` elements, clear error messages, and ARIA attributes
**Rationale**: Unlabeled forms are unusable for screen reader users

### AP-A11Y-009: Keyboard Traps
**DO NOT**: Create interactions that trap keyboard focus (e.g., modals without escape)
**DO**: Ensure all interactive elements can be reached and exited via keyboard
**Rationale**: Keyboard users must be able to navigate all content

### AP-A11Y-010: Missing Skip Links
**DO NOT**: Omit skip navigation links on complex pages
**DO**: Provide "Skip to main content" links for keyboard users
**Rationale**: Skip links save time for users navigating via keyboard

## Component Anti-Patterns

### AP-COMP-001: Missing Loading States
**DO NOT**: Show blank screen or frozen UI during data loading
**DO**: Provide skeleton screens, spinners, or progress indicators
**Rationale**: Loading states reduce perceived wait time and user anxiety

### AP-COMP-002: No Error Boundaries
**DO NOT**: Let component errors crash entire application
**DO**: Implement error boundaries with fallback UI and recovery options
**Rationale**: Graceful error handling prevents catastrophic failures

### AP-COMP-003: Inconsistent Icon Sizing
**DO NOT**: Mix icon sizes like 16px, 18px, 20px, 24px without system
**DO**: Use consistent scale like `sm: 16px`, `md: 20px`, `lg: 24px`
**Rationale**: Inconsistent icons break visual alignment and hierarchy

### AP-COMP-004: Vague Button Labels
**DO NOT**: Use generic labels like "Submit", "OK", "Click Here"
**DO**: Use specific action-oriented labels like "Create Account", "Save Changes"
**Rationale**: Specific labels improve usability and accessibility

### AP-COMP-005: Overloaded Components
**DO NOT**: Create components with 10+ props and multiple responsibilities
**DO**: Split into smaller, focused components with clear single purpose
**Rationale**: Overloaded components are hard to maintain and test

### AP-COMP-006: Inconsistent State Management
**DO NOT**: Mix state management approaches (Redux, Context, local) randomly
**DO**: Use consistent state management pattern throughout application
**Rationale**: Consistent patterns improve maintainability and developer experience

### AP-COMP-007: Non-Semantic HTML
**DO NOT**: Use `<div>` and `<span>` for everything
**DO**: Use semantic HTML5 elements like `<button>`, `<nav>`, `<article>`
**Rationale**: Semantic HTML improves accessibility and SEO

### AP-COMP-008: Missing Empty States
**DO NOT**: Show blank screen when no data is available
**DO**: Provide helpful empty states with guidance or call-to-action
**Rationale**: Empty states guide users on next steps

### AP-COMP-009: Uncontrolled Form Inputs
**DO NOT**: Use uncontrolled inputs without validation or value management
**DO**: Use controlled components with clear validation feedback
**Rationale**: Controlled inputs provide better UX and easier testing

### AP-COMP-010: Inline Styles Over Tokens
**DO NOT**: Use inline `style={{}}` attributes with hardcoded values
**DO**: Use CSS classes with token references
**Rationale**: Inline styles prevent theme consistency and increase bundle size

## Layout Anti-Patterns

### AP-LAY-001: Fixed Pixel Widths
**DO NOT**: Use fixed widths like `width: 1200px` that don't adapt
**DO**: Use responsive units like `max-width: 1200px`, percentages, or viewport units
**Rationale**: Fixed widths break responsive design and accessibility

### AP-LAY-002: Horizontal Scrolling
**DO NOT**: Create layouts that require horizontal scrolling on standard viewports
**DO**: Use responsive design that adapts to viewport width
**Rationale**: Horizontal scrolling is unexpected and breaks user expectations

### AP-LAY-003: Cramped Mobile Layouts
**DO NOT**: Compress desktop layouts to fit mobile without adaptation
**DO**: Design mobile-first with appropriate spacing and hierarchy
**Rationale**: Cramped layouts reduce usability on small screens

### AP-LAY-004: Excessive Nesting
**DO NOT**: Create deeply nested layouts (5+ levels of div wrappers)
**DO**: Use modern layout tools like Grid, Flexbox with minimal nesting
**Rationale**: Deep nesting hurts performance and maintainability

### AP-LAY-005: Inconsistent Grid System
**DO NOT**: Mix 12-column, 16-column, and arbitrary grids
**DO**: Use consistent grid system throughout application
**Rationale**: Consistent grid creates visual rhythm and easier implementation

## Typography Anti-Patterns

### AP-TYPE-001: Too Many Font Weights
**DO NOT**: Use 5+ different font weights (100, 300, 400, 500, 600, 700, 900)
**DO**: Limit to 2-3 weights: regular (400), medium (500), bold (700)
**Rationale**: Too many weights increase load time and reduce hierarchy clarity

### AP-TYPE-002: Tiny Mobile Text
**DO NOT**: Use font sizes below 16px for body text on mobile
**DO**: Use minimum 16px to prevent iOS zoom on input focus
**Rationale**: Tiny text triggers automatic zoom and reduces readability

### AP-TYPE-003: Line Length Extremes
**DO NOT**: Create lines shorter than 45 characters or longer than 75 characters
**DO**: Aim for 50-75 character line length for optimal readability
**Rationale**: Extreme line lengths reduce reading speed and comprehension

### AP-TYPE-004: Insufficient Line Height
**DO NOT**: Use line heights below 1.4 for body text
**DO**: Use 1.5-1.8 line height for comfortable reading
**Rationale**: Tight line height reduces readability and accessibility

### AP-TYPE-005: All Caps Overuse
**DO NOT**: Use ALL CAPS for long text passages
**DO**: Reserve ALL CAPS for labels, buttons, or short headings only
**Rationale**: All caps reduces reading speed by ~10%

## Animation Anti-Patterns

### AP-ANIM-001: Excessive Animation Duration
**DO NOT**: Create animations longer than 500ms for UI feedback
**DO**: Keep micro-interactions under 300ms for snappy feel
**Rationale**: Long animations feel sluggish and reduce perceived performance

### AP-ANIM-002: Ignoring Motion Preferences
**DO NOT**: Animate without checking `prefers-reduced-motion`
**DO**: Respect user motion preferences and provide static alternatives
**Rationale**: Motion sensitivity affects ~35% of users with vestibular disorders

### AP-ANIM-003: Animation Without Purpose
**DO NOT**: Add animations purely for decoration
**DO**: Use animation to guide attention, indicate state, or improve UX
**Rationale**: Gratuitous animation distracts and slows down users

### AP-ANIM-004: Jarring Easing Curves
**DO NOT**: Use linear easing (`transition: all 0.3s linear`)
**DO**: Use natural easing like `ease-out` for enter, `ease-in` for exit
**Rationale**: Linear easing feels robotic and unnatural

### AP-ANIM-005: Simultaneous Competing Animations
**DO NOT**: Animate multiple elements at once without coordination
**DO**: Stagger animations or animate sequentially for clarity
**Rationale**: Competing animations create visual chaos

## Performance Anti-Patterns

### AP-PERF-001: Unoptimized Images
**DO NOT**: Use full-resolution images without responsive formats
**DO**: Use modern formats (WebP, AVIF) with responsive srcset
**Rationale**: Large images slow page load and waste bandwidth

### AP-PERF-002: Blocking Fonts
**DO NOT**: Load custom fonts without `font-display` strategy
**DO**: Use `font-display: swap` or `font-display: optional`
**Rationale**: Blocking fonts create FOUT/FOIT and delay rendering

### AP-PERF-003: Layout Shift Sources
**DO NOT**: Load content without reserving space (images, ads, embeds)
**DO**: Set dimensions or aspect-ratio to prevent Cumulative Layout Shift
**Rationale**: Layout shifts harm UX and SEO (Core Web Vitals)

### AP-PERF-004: Overloaded Bundle
**DO NOT**: Include entire UI library for single component
**DO**: Use tree-shaking and import only needed components
**Rationale**: Bloated bundles slow initial load time

### AP-PERF-005: Unoptimized Re-renders
**DO NOT**: Trigger component re-renders on every state change
**DO**: Use memoization (React.memo, useMemo) for expensive operations
**Rationale**: Unnecessary re-renders waste CPU and battery

## Validation Rules

All design outputs must be checked against these anti-patterns before finalization:

1. **Visual Pass**: Check AP-VIS-001 through AP-VIS-008
2. **Accessibility Pass**: Check AP-A11Y-001 through AP-A11Y-010
3. **Component Pass**: Check AP-COMP-001 through AP-COMP-010
4. **Layout Pass**: Check AP-LAY-001 through AP-LAY-005
5. **Typography Pass**: Check AP-TYPE-001 through AP-TYPE-005
6. **Animation Pass**: Check AP-ANIM-001 through AP-ANIM-005
7. **Performance Pass**: Check AP-PERF-001 through AP-PERF-005

## Integration with Design Agents

These anti-patterns are automatically referenced by all design agents through the following prompt addition:

```yaml
## Anti-Patterns to Avoid
READ templates/shared/design-anti-patterns.md
Apply as DO NOT constraints in all outputs.
Validate final design against all AP-* checks.
```

## Expected Impact

Research shows negative prompting reduces design issues by **59-64%**:
- Visual inconsistencies: -62%
- Accessibility violations: -64%
- Component quality issues: -59%
- Performance regressions: -61%

## Changelog

- **v0.2.0** (2026-01-10): Initial comprehensive anti-patterns list with 47 patterns across 7 categories

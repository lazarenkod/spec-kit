# WCAG 2.1 AA Accessibility Requirements

## Overview

WCAG 2.1 Level AA is the internationally recognized standard for web accessibility, required by most accessibility laws including ADA (US), EAA (EU), and AODA (Canada). Meeting AA compliance ensures your product is usable by people with visual, auditory, motor, and cognitive disabilities.

**The Four Principles (POUR):**
- **Perceivable** - Information must be presentable in ways users can perceive
- **Operable** - Interface components must be operable by all users
- **Understandable** - Information and UI operation must be understandable
- **Robust** - Content must be robust enough for diverse assistive technologies

---

## Color Contrast Requirements

### Text Contrast Ratios

| Text Type | Minimum Ratio | Examples |
|-----------|---------------|----------|
| Normal text (<18px) | **4.5:1** | Body copy, labels, captions |
| Large text (≥18px or ≥14px bold) | **3:1** | Headings, buttons |
| Incidental/decorative text | No requirement | Disabled states, logos |

### UI Component Contrast

| Element | Minimum Ratio | Notes |
|---------|---------------|-------|
| Form inputs (borders) | **3:1** | Against background |
| Icons (functional) | **3:1** | When conveying information |
| Focus indicators | **3:1** | Against adjacent colors |
| Graphical objects | **3:1** | Charts, infographics |

### Recommended Contrast Checker Tools

- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Stark (Figma plugin)**: Real-time contrast checking in design tools
- **axe DevTools**: Browser extension for automated testing
- **Colour Contrast Analyser (CCA)**: Desktop application for precise measurement

### CSS Example: Accessible Color Palette

```css
:root {
  /* Primary colors with AA-compliant text combinations */
  --color-text-primary: #1a1a1a;      /* 12.6:1 on white */
  --color-text-secondary: #595959;    /* 7.0:1 on white */
  --color-text-muted: #767676;        /* 4.5:1 on white (minimum) */

  /* Interactive colors */
  --color-link: #0056b3;              /* 4.5:1 on white */
  --color-link-hover: #003d80;        /* 7.3:1 on white */

  /* Status colors */
  --color-error: #c41e3a;             /* 4.5:1 on white */
  --color-success: #0a7a3e;           /* 4.5:1 on white */
}
```

---

## Touch Target Requirements

### Minimum Size Requirements

| Requirement | Size | WCAG Criterion |
|-------------|------|----------------|
| Minimum touch target | **44×44px** | 2.5.5 Target Size |
| Inline links (exception) | Natural text size | Must have adequate spacing |
| Spacing between targets | **8px minimum** | Prevents accidental activation |

### CSS Example: Touch Targets

```css
/* Button with minimum touch target */
.btn {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 24px;
}

/* Icon button with adequate target size */
.btn-icon {
  width: 44px;
  height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Checkbox/radio with expanded hit area */
.form-check-input {
  width: 20px;
  height: 20px;
  position: relative;
}

.form-check-input::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 44px;
  height: 44px;
}
```

---

## Focus Indicators

### Requirements

- Focus must be **visible** on all interactive elements
- Focus indicator must have **3:1 contrast** against adjacent colors
- Focus should not be **suppressed** (`outline: none` without replacement)
- Focus order must follow **logical reading sequence**

### CSS Example: Accessible Focus Styles

```css
/* Base focus style - never remove without replacement */
:focus {
  outline: 2px solid var(--color-focus, #0056b3);
  outline-offset: 2px;
}

/* Enhanced focus for keyboard users only */
:focus:not(:focus-visible) {
  outline: none;
}

:focus-visible {
  outline: 3px solid var(--color-focus, #0056b3);
  outline-offset: 2px;
  border-radius: 2px;
}

/* High contrast focus for dark backgrounds */
.dark-section :focus-visible {
  outline-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.5);
}

/* Focus within for composite components */
.card:focus-within {
  box-shadow: 0 0 0 3px var(--color-focus);
}
```

---

## Screen Reader Support

### Semantic HTML Requirements

| Element | Use Case | Avoid |
|---------|----------|-------|
| `<button>` | Clickable actions | `<div onclick>` |
| `<a href>` | Navigation links | `<span onclick>` |
| `<nav>` | Navigation regions | `<div class="nav">` |
| `<main>` | Primary content | Unmarked content |
| `<article>` | Self-contained content | Generic divs |
| `<h1>`-`<h6>` | Content hierarchy | Styled paragraphs |
| `<ul>`, `<ol>` | Lists of items | Line-break separated items |
| `<table>` | Tabular data | Layout purposes |

### ARIA Labels for Custom Components

```html
<!-- Custom button -->
<div role="button" tabindex="0" aria-label="Close dialog">
  <svg aria-hidden="true">...</svg>
</div>

<!-- Icon-only button -->
<button aria-label="Search">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>

<!-- Loading state -->
<button aria-busy="true" aria-label="Submitting form">
  <span class="spinner" aria-hidden="true"></span>
  Submitting...
</button>

<!-- Expandable section -->
<button aria-expanded="false" aria-controls="panel-1">
  Show details
</button>
<div id="panel-1" hidden>...</div>

<!-- Live region for dynamic updates -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  <!-- Announce changes to screen readers -->
</div>
```

### Image Alt Text Requirements

| Image Type | Alt Text Approach |
|------------|-------------------|
| Informative | Describe content and purpose |
| Decorative | Use `alt=""` (empty) |
| Functional (links/buttons) | Describe action/destination |
| Complex (charts/graphs) | Provide detailed description or link to text alternative |
| Text in images | Include all visible text |

```html
<!-- Informative image -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2 2024">

<!-- Decorative image -->
<img src="decorative-border.png" alt="" role="presentation">

<!-- Functional image -->
<a href="/home">
  <img src="logo.png" alt="Acme Corp - Return to homepage">
</a>
```

---

## Reduced Motion

### Implementation Requirements

Users with vestibular disorders can be triggered by animations. Respect the `prefers-reduced-motion` media query.

```css
/* Default: include animations */
.animated-element {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

/* Reduced motion: minimize or remove animations */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  /* Alternative: instant state changes */
  .animated-element {
    transition: none;
  }
}
```

### JavaScript Detection

```javascript
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (prefersReducedMotion) {
  // Disable autoplay videos, carousels, parallax effects
  // Use instant transitions instead of animations
}
```

---

## Keyboard Navigation

### Tab Order Requirements

- Follow **visual and logical reading order**
- No **keyboard traps** (users can navigate away from any element)
- Skip navigation link for repetitive content
- `tabindex="0"` for custom interactive elements
- `tabindex="-1"` for programmatic focus only
- **Never use** `tabindex` values greater than 0

### Focus Trap for Modals

```javascript
// Focus trap implementation for dialogs
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey && document.activeElement === firstFocusable) {
      e.preventDefault();
      lastFocusable.focus();
    } else if (!e.shiftKey && document.activeElement === lastFocusable) {
      e.preventDefault();
      firstFocusable.focus();
    }
  });

  // Focus first element when modal opens
  firstFocusable.focus();
}
```

### Escape Key Behavior

Modals, dropdowns, and overlays must close on Escape key:

```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeModal();
    // Return focus to trigger element
    triggerElement.focus();
  }
});
```

### Skip Link Implementation

```html
<body>
  <a href="#main-content" class="skip-link">
    Skip to main content
  </a>
  <nav>...</nav>
  <main id="main-content" tabindex="-1">
    ...
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px 16px;
  background: var(--color-primary);
  color: white;
  z-index: 1000;
}

.skip-link:focus {
  top: 0;
}
```

---

## Quick Validation Checklist

### Perceivable

- [ ] Text has minimum 4.5:1 contrast (3:1 for large text)
- [ ] UI components have 3:1 contrast against backgrounds
- [ ] Color is not the only means of conveying information
- [ ] All images have appropriate alt text
- [ ] Video has captions; audio has transcripts
- [ ] Content is readable at 200% zoom
- [ ] Text spacing can be adjusted without loss of content

### Operable

- [ ] All functionality available via keyboard
- [ ] No keyboard traps exist
- [ ] Focus indicators are visible (3:1 contrast)
- [ ] Touch targets are minimum 44×44px
- [ ] Users can pause, stop, or hide moving content
- [ ] No content flashes more than 3 times per second
- [ ] Skip navigation link is provided
- [ ] Page titles are descriptive and unique

### Understandable

- [ ] Page language is declared (`<html lang="en">`)
- [ ] Form labels are associated with inputs
- [ ] Error messages identify the field and describe the error
- [ ] Instructions don't rely solely on sensory characteristics
- [ ] Navigation is consistent across pages
- [ ] Form validation provides suggestions for correction

### Robust

- [ ] HTML validates without significant errors
- [ ] ARIA is used correctly (valid roles, states, properties)
- [ ] Custom components have appropriate roles and states
- [ ] Status messages use `aria-live` regions
- [ ] Name, role, and value are programmatically determinable

---

## Testing Tools Reference

| Tool | Purpose | URL |
|------|---------|-----|
| axe DevTools | Automated testing | Browser extension |
| WAVE | Visual accessibility feedback | wave.webaim.org |
| Lighthouse | Performance + accessibility audit | Built into Chrome |
| NVDA | Screen reader testing (Windows) | nvaccess.org |
| VoiceOver | Screen reader testing (macOS/iOS) | Built into Apple devices |
| Keyboard | Manual tab-through testing | Native |

---

*Reference: [WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21/) | [WebAIM](https://webaim.org/)*

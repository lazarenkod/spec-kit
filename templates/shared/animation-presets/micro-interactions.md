# Micro-Interaction Animation Presets

Ready-to-use animation specifications for common UI micro-interactions. Copy these directly into your design.md or use as reference.

## Button Interactions

### Button Press

```yaml
name: button-press
trigger: mousedown / touchstart
purpose: Provide tactile feedback on interaction

animation:
  duration: 100ms
  easing: ease-out
  properties:
    transform: scale(0.98)

reset:
  trigger: mouseup / touchend
  duration: 150ms
  easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)  # spring
  properties:
    transform: scale(1)
```

**CSS Implementation**:
```css
.button {
  transition: transform 150ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.button:active {
  transform: scale(0.98);
  transition-duration: 100ms;
  transition-timing-function: ease-out;
}
```

**Framer Motion**:
```tsx
<motion.button
  whileTap={{ scale: 0.98 }}
  transition={{ duration: 0.1 }}
>
  Click me
</motion.button>
```

### Button Hover Lift

```yaml
name: button-hover-lift
trigger: mouseenter
purpose: Indicate interactivity

animation:
  duration: 200ms
  easing: ease-out
  properties:
    transform: translateY(-2px)
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15)

reset:
  trigger: mouseleave
  duration: 200ms
  easing: ease-out
  properties:
    transform: translateY(0)
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)
```

**CSS Implementation**:
```css
.button {
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

### Button Loading Spinner

```yaml
name: button-loading
trigger: loading state
purpose: Show action in progress

animation:
  - target: text
    properties:
      opacity: 0
    duration: 100ms

  - target: spinner
    properties:
      opacity: 1
      animation: spin 1s linear infinite

keyframes:
  spin:
    from: { transform: rotate(0deg) }
    to: { transform: rotate(360deg) }
```

**CSS Implementation**:
```css
.button-loading .button-text {
  opacity: 0;
  transition: opacity 100ms ease-out;
}

.button-loading .button-spinner {
  position: absolute;
  opacity: 1;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .button-loading .button-spinner {
    animation: none;
  }
}
```

---

## Form Interactions

### Input Focus

```yaml
name: input-focus
trigger: focus
purpose: Highlight active input

animation:
  duration: 150ms
  easing: ease-out
  properties:
    border-color: var(--ring)
    box-shadow: 0 0 0 2px var(--ring)
    outline: none
```

**CSS Implementation**:
```css
.input {
  transition: border-color 150ms ease-out, box-shadow 150ms ease-out;
  border: 1px solid var(--border);
}

.input:focus {
  border-color: var(--ring);
  box-shadow: 0 0 0 2px var(--ring);
  outline: none;
}

.input:focus-visible {
  /* Same styles for keyboard focus */
  border-color: var(--ring);
  box-shadow: 0 0 0 2px var(--ring);
}
```

### Input Error Shake

```yaml
name: input-error-shake
trigger: validation error
purpose: Draw attention to error

animation:
  duration: 300ms
  easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
  keyframes:
    0%: { transform: translateX(0) }
    20%: { transform: translateX(-8px) }
    40%: { transform: translateX(8px) }
    60%: { transform: translateX(-4px) }
    80%: { transform: translateX(4px) }
    100%: { transform: translateX(0) }

concurrent:
  - property: border-color
    value: var(--destructive)
    duration: 150ms
```

**CSS Implementation**:
```css
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-8px); }
  40% { transform: translateX(8px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}

.input-error {
  animation: shake 300ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border-color: var(--destructive);
}

@media (prefers-reduced-motion: reduce) {
  .input-error {
    animation: none;
    /* Just show red border */
  }
}
```

### Checkbox Toggle

```yaml
name: checkbox-toggle
trigger: click / change
purpose: Confirm state change

animation:
  - target: box
    duration: 150ms
    easing: ease-out
    properties:
      background-color: var(--primary)
      border-color: var(--primary)

  - target: checkmark
    duration: 200ms
    delay: 50ms
    easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
    properties:
      stroke-dashoffset: 0
      transform: scale(1)

initial:
  checkmark:
    stroke-dashoffset: 24  # Full length of path
    transform: scale(0.8)
```

**CSS Implementation**:
```css
.checkbox-box {
  transition: background-color 150ms ease-out, border-color 150ms ease-out;
}

.checkbox:checked + .checkbox-box {
  background-color: var(--primary);
  border-color: var(--primary);
}

.checkbox-checkmark {
  stroke-dasharray: 24;
  stroke-dashoffset: 24;
  transform: scale(0.8);
  transition: stroke-dashoffset 200ms cubic-bezier(0.175, 0.885, 0.32, 1.275) 50ms,
              transform 200ms cubic-bezier(0.175, 0.885, 0.32, 1.275) 50ms;
}

.checkbox:checked + .checkbox-box .checkbox-checkmark {
  stroke-dashoffset: 0;
  transform: scale(1);
}
```

### Switch Toggle

```yaml
name: switch-toggle
trigger: click / change
purpose: Confirm on/off state

animation:
  - target: track
    duration: 200ms
    easing: ease-in-out
    properties:
      background-color: var(--primary)  # when on
      # or var(--muted) when off

  - target: thumb
    duration: 200ms
    easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
    properties:
      transform: translateX(20px)  # when on
      # or translateX(0) when off
```

**CSS Implementation**:
```css
.switch-track {
  transition: background-color 200ms ease-in-out;
  background-color: var(--muted);
}

.switch-thumb {
  transition: transform 200ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform: translateX(0);
}

.switch:checked + .switch-track {
  background-color: var(--primary);
}

.switch:checked + .switch-track .switch-thumb {
  transform: translateX(20px);
}
```

---

## Feedback Interactions

### Ripple Effect

```yaml
name: ripple
trigger: click
purpose: Material-style touch feedback

animation:
  duration: 500ms
  easing: ease-out
  keyframes:
    0%:
      transform: scale(0)
      opacity: 0.5
    100%:
      transform: scale(2.5)
      opacity: 0
```

**CSS Implementation**:
```css
.ripple-container {
  position: relative;
  overflow: hidden;
}

.ripple {
  position: absolute;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.3;
  transform: scale(0);
  animation: ripple 500ms ease-out forwards;
  pointer-events: none;
}

@keyframes ripple {
  to {
    transform: scale(2.5);
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ripple {
    animation: none;
    opacity: 0;
  }
}
```

**JavaScript** (to position ripple):
```typescript
function createRipple(event: MouseEvent) {
  const button = event.currentTarget as HTMLElement;
  const ripple = document.createElement('span');
  const rect = button.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);

  ripple.style.width = ripple.style.height = size + 'px';
  ripple.style.left = event.clientX - rect.left - size / 2 + 'px';
  ripple.style.top = event.clientY - rect.top - size / 2 + 'px';
  ripple.classList.add('ripple');

  button.appendChild(ripple);
  ripple.addEventListener('animationend', () => ripple.remove());
}
```

### Tooltip Show

```yaml
name: tooltip-show
trigger: mouseenter / focus
purpose: Show contextual information

animation:
  duration: 150ms
  delay: 300ms  # Wait before showing
  easing: ease-out
  properties:
    opacity: 1
    transform: translateY(0)

initial:
  opacity: 0
  transform: translateY(4px)
```

**CSS Implementation**:
```css
.tooltip {
  opacity: 0;
  transform: translateY(4px);
  transition: opacity 150ms ease-out, transform 150ms ease-out;
  transition-delay: 0ms;
  pointer-events: none;
}

.trigger:hover + .tooltip,
.trigger:focus + .tooltip {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 300ms;
}
```

### Badge Pulse

```yaml
name: badge-pulse
trigger: new notification
purpose: Draw attention to new items

animation:
  duration: 2000ms
  easing: ease-in-out
  iteration: 3
  keyframes:
    0%, 100%:
      transform: scale(1)
      box-shadow: 0 0 0 0 rgba(var(--destructive), 0.4)
    50%:
      transform: scale(1.05)
      box-shadow: 0 0 0 8px rgba(var(--destructive), 0)
```

**CSS Implementation**:
```css
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 8px rgba(239, 68, 68, 0);
  }
}

.badge-new {
  animation: pulse 2s ease-in-out 3;
}

@media (prefers-reduced-motion: reduce) {
  .badge-new {
    animation: none;
    /* Just show static badge */
  }
}
```

---

## Card Interactions

### Card Hover

```yaml
name: card-hover
trigger: mouseenter
purpose: Indicate card is interactive

animation:
  duration: 200ms
  easing: ease-out
  properties:
    transform: translateY(-4px)
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15)
```

**CSS Implementation**:
```css
.card {
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

@media (prefers-reduced-motion: reduce) {
  .card:hover {
    transform: none;
    /* Just show shadow change */
  }
}
```

### Card Selection

```yaml
name: card-selection
trigger: click
purpose: Show card is selected

animation:
  duration: 200ms
  easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
  properties:
    transform: scale(1.02)
    border-color: var(--primary)
    box-shadow: 0 0 0 2px var(--primary)
```

**CSS Implementation**:
```css
.card {
  transition: transform 200ms cubic-bezier(0.175, 0.885, 0.32, 1.275),
              border-color 200ms ease-out,
              box-shadow 200ms ease-out;
}

.card[aria-selected="true"],
.card.selected {
  transform: scale(1.02);
  border-color: var(--primary);
  box-shadow: 0 0 0 2px var(--primary);
}
```

---

## Menu Interactions

### Dropdown Open

```yaml
name: dropdown-open
trigger: click / enter
purpose: Reveal menu options

animation:
  duration: 200ms
  easing: ease-out
  properties:
    opacity: 1
    transform: translateY(0) scale(1)
  transform-origin: top

initial:
  opacity: 0
  transform: translateY(-8px) scale(0.95)
```

**CSS Implementation**:
```css
.dropdown-menu {
  opacity: 0;
  transform: translateY(-8px) scale(0.95);
  transform-origin: top;
  transition: opacity 200ms ease-out, transform 200ms ease-out;
  pointer-events: none;
}

.dropdown-menu[data-state="open"] {
  opacity: 1;
  transform: translateY(0) scale(1);
  pointer-events: auto;
}
```

**Framer Motion**:
```tsx
<AnimatePresence>
  {isOpen && (
    <motion.div
      initial={{ opacity: 0, y: -8, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -8, scale: 0.95 }}
      transition={{ duration: 0.2, ease: [0, 0, 0.2, 1] }}
    >
      {/* Menu content */}
    </motion.div>
  )}
</AnimatePresence>
```

### Menu Item Hover

```yaml
name: menu-item-hover
trigger: mouseenter / focus
purpose: Highlight focused item

animation:
  duration: 100ms
  easing: ease-out
  properties:
    background-color: var(--accent)
```

**CSS Implementation**:
```css
.menu-item {
  transition: background-color 100ms ease-out;
}

.menu-item:hover,
.menu-item:focus {
  background-color: var(--accent);
}
```

---

## Accessibility Notes

### Reduced Motion

All presets include `prefers-reduced-motion` alternatives:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Focus Indicators

Always maintain visible focus:

```css
/* Never hide focus for keyboard users */
:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}

/* Can hide for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

### Touch Targets

Minimum 44×44px for all interactive elements:

```css
.button,
.checkbox,
.radio,
.switch {
  min-width: 44px;
  min-height: 44px;
}
```

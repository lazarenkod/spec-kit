# Page Transition Animation Presets

Ready-to-use animation specifications for page and route transitions. These presets work with React Router, Next.js, and other routing solutions.

## Basic Transitions

### Fade

```yaml
name: fade
use_case: Default route transition, subtle navigation
duration: 200ms
easing: ease-out

enter:
  initial: { opacity: 0 }
  animate: { opacity: 1 }

exit:
  initial: { opacity: 1 }
  animate: { opacity: 0 }
```

**CSS Implementation**:
```css
.page-enter {
  opacity: 0;
}

.page-enter-active {
  opacity: 1;
  transition: opacity 200ms ease-out;
}

.page-exit {
  opacity: 1;
}

.page-exit-active {
  opacity: 0;
  transition: opacity 200ms ease-out;
}
```

**Framer Motion**:
```tsx
const fadeVariants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
}

<motion.div
  variants={fadeVariants}
  initial="initial"
  animate="animate"
  exit="exit"
  transition={{ duration: 0.2, ease: [0, 0, 0.2, 1] }}
>
  {children}
</motion.div>
```

### Fade Slide Up

```yaml
name: fade-slide-up
use_case: Content appearing from bottom, modal-like feel
duration: 250ms
easing: ease-out

enter:
  initial:
    opacity: 0
    transform: translateY(16px)
  animate:
    opacity: 1
    transform: translateY(0)

exit:
  initial:
    opacity: 1
    transform: translateY(0)
  animate:
    opacity: 0
    transform: translateY(-8px)
```

**CSS Implementation**:
```css
.page-enter {
  opacity: 0;
  transform: translateY(16px);
}

.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 250ms ease-out, transform 250ms ease-out;
}

.page-exit {
  opacity: 1;
  transform: translateY(0);
}

.page-exit-active {
  opacity: 0;
  transform: translateY(-8px);
  transition: opacity 200ms ease-in, transform 200ms ease-in;
}
```

**Framer Motion**:
```tsx
const fadeSlideUpVariants = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
}

<motion.div
  variants={fadeSlideUpVariants}
  initial="initial"
  animate="animate"
  exit="exit"
  transition={{ duration: 0.25, ease: [0, 0, 0.2, 1] }}
>
  {children}
</motion.div>
```

### Fade Scale

```yaml
name: fade-scale
use_case: Emphasizing new content, zoom-in feel
duration: 250ms
easing: ease-out

enter:
  initial:
    opacity: 0
    transform: scale(0.96)
  animate:
    opacity: 1
    transform: scale(1)

exit:
  initial:
    opacity: 1
    transform: scale(1)
  animate:
    opacity: 0
    transform: scale(1.02)
```

**Framer Motion**:
```tsx
const fadeScaleVariants = {
  initial: { opacity: 0, scale: 0.96 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 1.02 },
}
```

---

## Directional Transitions

### Slide Horizontal

```yaml
name: slide-horizontal
use_case: Wizard steps, pagination, directional navigation
duration: 300ms
easing: ease-in-out

# Direction determined by navigation
forward:
  enter: { transform: translateX(100%) }
  exit: { transform: translateX(-100%) }

backward:
  enter: { transform: translateX(-100%) }
  exit: { transform: translateX(100%) }
```

**CSS Implementation** (forward):
```css
.page-enter {
  transform: translateX(100%);
}

.page-enter-active {
  transform: translateX(0);
  transition: transform 300ms ease-in-out;
}

.page-exit {
  transform: translateX(0);
}

.page-exit-active {
  transform: translateX(-100%);
  transition: transform 300ms ease-in-out;
}
```

**Framer Motion with direction**:
```tsx
const slideVariants = {
  enter: (direction: number) => ({
    x: direction > 0 ? '100%' : '-100%',
    opacity: 0,
  }),
  center: {
    x: 0,
    opacity: 1,
  },
  exit: (direction: number) => ({
    x: direction > 0 ? '-100%' : '100%',
    opacity: 0,
  }),
}

<AnimatePresence mode="wait" custom={direction}>
  <motion.div
    key={currentPage}
    custom={direction}
    variants={slideVariants}
    initial="enter"
    animate="center"
    exit="exit"
    transition={{ duration: 0.3, ease: 'easeInOut' }}
  >
    {children}
  </motion.div>
</AnimatePresence>
```

### Slide Vertical

```yaml
name: slide-vertical
use_case: Bottom sheets, expandable sections
duration: 300ms
easing: ease-out

enter:
  initial:
    transform: translateY(100%)
  animate:
    transform: translateY(0)

exit:
  initial:
    transform: translateY(0)
  animate:
    transform: translateY(100%)
```

**CSS Implementation**:
```css
.sheet-enter {
  transform: translateY(100%);
}

.sheet-enter-active {
  transform: translateY(0);
  transition: transform 300ms ease-out;
}

.sheet-exit {
  transform: translateY(0);
}

.sheet-exit-active {
  transform: translateY(100%);
  transition: transform 300ms ease-in;
}
```

---

## Modal & Overlay Transitions

### Modal Fade Scale

```yaml
name: modal-fade-scale
use_case: Dialogs, modal windows
duration: 200ms
easing: ease-out

backdrop:
  enter: { opacity: 0 → 1 }
  exit: { opacity: 1 → 0 }
  duration: 200ms

content:
  enter:
    initial:
      opacity: 0
      transform: scale(0.95)
    animate:
      opacity: 1
      transform: scale(1)
  exit:
    initial:
      opacity: 1
      transform: scale(1)
    animate:
      opacity: 0
      transform: scale(0.95)
```

**CSS Implementation**:
```css
/* Backdrop */
.modal-backdrop {
  opacity: 0;
  transition: opacity 200ms ease-out;
}

.modal-backdrop[data-state="open"] {
  opacity: 1;
}

/* Content */
.modal-content {
  opacity: 0;
  transform: scale(0.95);
  transition: opacity 200ms ease-out, transform 200ms ease-out;
}

.modal-content[data-state="open"] {
  opacity: 1;
  transform: scale(1);
}
```

**Framer Motion**:
```tsx
<AnimatePresence>
  {isOpen && (
    <>
      <motion.div
        className="backdrop"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.2 }}
      />
      <motion.div
        className="modal"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        transition={{ duration: 0.2, ease: [0, 0, 0.2, 1] }}
      >
        {children}
      </motion.div>
    </>
  )}
</AnimatePresence>
```

### Drawer Slide

```yaml
name: drawer-slide
use_case: Side navigation, panels
duration: 300ms
easing: ease-out

# Right drawer
right:
  enter:
    initial: { transform: translateX(100%) }
    animate: { transform: translateX(0) }
  exit:
    initial: { transform: translateX(0) }
    animate: { transform: translateX(100%) }

# Left drawer
left:
  enter:
    initial: { transform: translateX(-100%) }
    animate: { transform: translateX(0) }
  exit:
    initial: { transform: translateX(0) }
    animate: { transform: translateX(-100%) }

backdrop:
  duration: 200ms
```

**CSS Implementation** (right drawer):
```css
.drawer-right {
  transform: translateX(100%);
  transition: transform 300ms ease-out;
}

.drawer-right[data-state="open"] {
  transform: translateX(0);
}
```

---

## Staggered Transitions

### List Stagger

```yaml
name: list-stagger
use_case: List items appearing sequentially
base_duration: 200ms
stagger_delay: 50ms
easing: ease-out

item:
  initial:
    opacity: 0
    transform: translateY(8px)
  animate:
    opacity: 1
    transform: translateY(0)
```

**Framer Motion**:
```tsx
const containerVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.05,
    },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 8 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.2, ease: [0, 0, 0.2, 1] },
  },
}

<motion.ul variants={containerVariants} initial="hidden" animate="visible">
  {items.map((item) => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.content}
    </motion.li>
  ))}
</motion.ul>
```

### Grid Stagger

```yaml
name: grid-stagger
use_case: Dashboard cards, gallery items
base_duration: 200ms
stagger_delay: 30ms
easing: ease-out

# Can animate row by row or all at once
strategy: row-by-row  # or cascade
items_per_row: 3
```

**Framer Motion**:
```tsx
const gridVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.03,
      delayChildren: 0.1,
    },
  },
}

const cardVariants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.2 },
  },
}
```

---

## Shared Element Transitions

### Expand from Element

```yaml
name: expand-from-element
use_case: Card to detail page, thumbnail to full view
duration: 400ms
easing: cubic-bezier(0.4, 0, 0.2, 1)

# Requires knowing source element bounds
animation:
  - phase: expand
    from: source_element_bounds
    to: full_screen_bounds
    properties:
      - width
      - height
      - x
      - y
      - border-radius
```

**Framer Motion (layout animations)**:
```tsx
// Card in list
<motion.div layoutId={`card-${id}`}>
  <motion.img layoutId={`image-${id}`} src={image} />
  <motion.h2 layoutId={`title-${id}`}>{title}</motion.h2>
</motion.div>

// Full page view
<motion.div layoutId={`card-${id}`}>
  <motion.img layoutId={`image-${id}`} src={image} />
  <motion.h2 layoutId={`title-${id}`}>{title}</motion.h2>
  <p>{fullDescription}</p>
</motion.div>
```

---

## Special Transitions

### Cross-Fade

```yaml
name: cross-fade
use_case: Image galleries, content swap
duration: 300ms
easing: ease-in-out

# Both pages visible during transition
strategy: cross-fade
```

**CSS Implementation**:
```css
.page-container {
  position: relative;
}

.page {
  position: absolute;
  inset: 0;
}

.page-enter {
  opacity: 0;
}

.page-enter-active {
  opacity: 1;
  transition: opacity 300ms ease-in-out;
}

.page-exit {
  opacity: 1;
}

.page-exit-active {
  opacity: 0;
  transition: opacity 300ms ease-in-out;
}
```

### Blur Transition

```yaml
name: blur-transition
use_case: Premium feel, focus shift
duration: 300ms
easing: ease-out

enter:
  initial:
    opacity: 0
    filter: blur(8px)
  animate:
    opacity: 1
    filter: blur(0)

exit:
  initial:
    opacity: 1
    filter: blur(0)
  animate:
    opacity: 0
    filter: blur(8px)
```

**CSS Implementation**:
```css
.page-enter {
  opacity: 0;
  filter: blur(8px);
}

.page-enter-active {
  opacity: 1;
  filter: blur(0);
  transition: opacity 300ms ease-out, filter 300ms ease-out;
}

.page-exit {
  opacity: 1;
  filter: blur(0);
}

.page-exit-active {
  opacity: 0;
  filter: blur(8px);
  transition: opacity 300ms ease-out, filter 300ms ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .page-enter,
  .page-exit {
    filter: none;
  }
}
```

---

## Framework Integration

### Next.js App Router

```tsx
// app/template.tsx
'use client'

import { motion } from 'framer-motion'

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: [0, 0, 0.2, 1] }}
    >
      {children}
    </motion.div>
  )
}
```

### React Router v6

```tsx
import { AnimatePresence, motion } from 'framer-motion'
import { useLocation, Routes } from 'react-router-dom'

function AnimatedRoutes() {
  const location = useLocation()

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.2 }}
      >
        <Routes location={location}>
          {/* Routes here */}
        </Routes>
      </motion.div>
    </AnimatePresence>
  )
}
```

### View Transitions API (Native)

```typescript
// For browsers supporting View Transitions API
async function navigate(href: string) {
  if (!document.startViewTransition) {
    window.location.href = href
    return
  }

  const transition = document.startViewTransition(async () => {
    // Update DOM
    await loadNewPage(href)
  })

  await transition.finished
}
```

```css
/* View Transition CSS */
::view-transition-old(root) {
  animation: fade-out 200ms ease-out;
}

::view-transition-new(root) {
  animation: fade-in 200ms ease-out;
}

@keyframes fade-out {
  to { opacity: 0; }
}

@keyframes fade-in {
  from { opacity: 0; }
}
```

---

## Accessibility Considerations

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  .page-enter,
  .page-exit,
  .page-enter-active,
  .page-exit-active {
    transition: none;
    animation: none;
    transform: none;
    opacity: 1;
  }
}
```

### Focus Management

```typescript
// After page transition completes
useEffect(() => {
  // Find main heading or content
  const mainHeading = document.querySelector('h1')
  const mainContent = document.querySelector('main')

  if (mainHeading) {
    mainHeading.focus()
  } else if (mainContent) {
    mainContent.focus()
  }
}, [location.pathname])
```

### Announce Page Changes

```tsx
// Live region for screen readers
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
  className="sr-only"
>
  {`Navigated to ${pageTitle}`}
</div>
```

# Loading State Animation Presets

Ready-to-use animation specifications for loading indicators, skeleton screens, progress bars, and content loading patterns.

## Skeleton Screens

### Basic Skeleton

```yaml
name: skeleton-shimmer
use_case: Content placeholders, data loading
animation_type: continuous
duration: 1500ms
easing: linear
iteration: infinite

keyframes:
  0%:
    background-position: -200% 0
  100%:
    background-position: 200% 0

gradient:
  direction: 90deg
  colors:
    - var(--muted) 0%
    - var(--muted-foreground) 50%
    - var(--muted) 100%
  size: 200% 100%
```

**CSS Implementation**:
```css
.skeleton {
  background: linear-gradient(
    90deg,
    hsl(var(--muted)) 0%,
    hsl(var(--muted-foreground) / 0.1) 50%,
    hsl(var(--muted)) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite linear;
  border-radius: var(--radius);
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
    background: hsl(var(--muted));
  }
}
```

**React Component**:
```tsx
interface SkeletonProps {
  className?: string
  width?: string | number
  height?: string | number
}

function Skeleton({ className, width, height }: SkeletonProps) {
  return (
    <div
      className={cn("skeleton", className)}
      style={{ width, height }}
      aria-hidden="true"
    />
  )
}

// Usage
<Skeleton width="100%" height={20} />
<Skeleton width={200} height={16} />
```

### Pulse Skeleton

```yaml
name: skeleton-pulse
use_case: Alternative to shimmer, simpler animation
animation_type: continuous
duration: 2000ms
easing: ease-in-out
iteration: infinite

keyframes:
  0%, 100%:
    opacity: 1
  50%:
    opacity: 0.5
```

**CSS Implementation**:
```css
.skeleton-pulse {
  background: hsl(var(--muted));
  animation: pulse 2s ease-in-out infinite;
  border-radius: var(--radius);
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-pulse {
    animation: none;
    opacity: 0.7;
  }
}
```

### Skeleton Patterns

```yaml
# Common skeleton layouts

card_skeleton:
  - type: rectangle
    width: 100%
    height: 200px
    purpose: image placeholder

  - type: rectangle
    width: 60%
    height: 24px
    margin_top: 16px
    purpose: title

  - type: rectangle
    width: 100%
    height: 16px
    margin_top: 8px
    purpose: description line 1

  - type: rectangle
    width: 80%
    height: 16px
    margin_top: 4px
    purpose: description line 2

table_row_skeleton:
  - type: circle
    width: 40px
    height: 40px
    purpose: avatar

  - type: rectangle
    width: 120px
    height: 16px
    purpose: name

  - type: rectangle
    width: 180px
    height: 16px
    purpose: email

  - type: rectangle
    width: 80px
    height: 16px
    purpose: status
```

**React Implementation**:
```tsx
function CardSkeleton() {
  return (
    <div className="card">
      <Skeleton className="w-full h-[200px]" />
      <div className="p-4">
        <Skeleton className="w-3/5 h-6" />
        <Skeleton className="w-full h-4 mt-2" />
        <Skeleton className="w-4/5 h-4 mt-1" />
      </div>
    </div>
  )
}

function TableRowSkeleton() {
  return (
    <tr>
      <td><Skeleton className="w-10 h-10 rounded-full" /></td>
      <td><Skeleton className="w-[120px] h-4" /></td>
      <td><Skeleton className="w-[180px] h-4" /></td>
      <td><Skeleton className="w-[80px] h-4" /></td>
    </tr>
  )
}
```

---

## Spinners

### Simple Spinner

```yaml
name: spinner
use_case: Button loading, small indicators
animation_type: continuous
duration: 1000ms
easing: linear
iteration: infinite

keyframes:
  from:
    transform: rotate(0deg)
  to:
    transform: rotate(360deg)
```

**CSS Implementation**:
```css
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid hsl(var(--muted));
  border-top-color: hsl(var(--primary));
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Size variants */
.spinner-sm {
  width: 16px;
  height: 16px;
  border-width: 2px;
}

.spinner-lg {
  width: 32px;
  height: 32px;
  border-width: 3px;
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation: none;
    border-top-color: hsl(var(--muted-foreground));
    /* Show static partial ring */
  }
}
```

**React Component**:
```tsx
interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

function Spinner({ size = 'md', className }: SpinnerProps) {
  return (
    <div
      className={cn('spinner', `spinner-${size}`, className)}
      role="status"
      aria-label="Loading"
    >
      <span className="sr-only">Loading...</span>
    </div>
  )
}
```

### Dots Spinner

```yaml
name: dots-spinner
use_case: Modern alternative to circular spinner
animation_type: staggered
duration: 1400ms
easing: ease-in-out
iteration: infinite

dots: 3
stagger: 160ms

keyframes:
  0%, 80%, 100%:
    transform: scale(0)
    opacity: 0.5
  40%:
    transform: scale(1)
    opacity: 1
```

**CSS Implementation**:
```css
.dots-spinner {
  display: flex;
  gap: 4px;
}

.dots-spinner .dot {
  width: 8px;
  height: 8px;
  background: hsl(var(--primary));
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite both;
}

.dots-spinner .dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dots-spinner .dot:nth-child(2) {
  animation-delay: -0.16s;
}

.dots-spinner .dot:nth-child(3) {
  animation-delay: 0s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

@media (prefers-reduced-motion: reduce) {
  .dots-spinner .dot {
    animation: none;
    opacity: 0.7;
  }
}
```

### Icon Spinner (Lucide)

```tsx
import { Loader2 } from 'lucide-react'

function IconSpinner({ className }: { className?: string }) {
  return (
    <Loader2
      className={cn('animate-spin', className)}
      aria-hidden="true"
    />
  )
}
```

```css
.animate-spin {
  animation: spin 1s linear infinite;
}
```

---

## Progress Indicators

### Determinate Progress Bar

```yaml
name: progress-bar
use_case: File uploads, known-length operations
animation_type: value-based
easing: ease-out
duration: 300ms  # For value changes

bar:
  height: 4px
  background: var(--muted)
  border_radius: 2px

fill:
  background: var(--primary)
  transition: width 300ms ease-out
```

**CSS Implementation**:
```css
.progress {
  width: 100%;
  height: 4px;
  background: hsl(var(--muted));
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: hsl(var(--primary));
  transition: width 300ms ease-out;
}
```

**React Component**:
```tsx
interface ProgressProps {
  value: number  // 0-100
  className?: string
}

function Progress({ value, className }: ProgressProps) {
  return (
    <div
      className={cn('progress', className)}
      role="progressbar"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      <div
        className="progress-fill"
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  )
}
```

### Indeterminate Progress Bar

```yaml
name: progress-indeterminate
use_case: Unknown duration operations
animation_type: continuous
duration: 1500ms
easing: ease-in-out
iteration: infinite

keyframes:
  0%:
    transform: translateX(-100%)
  100%:
    transform: translateX(400%)
```

**CSS Implementation**:
```css
.progress-indeterminate {
  width: 100%;
  height: 4px;
  background: hsl(var(--muted));
  border-radius: 2px;
  overflow: hidden;
}

.progress-indeterminate::after {
  content: '';
  display: block;
  width: 30%;
  height: 100%;
  background: hsl(var(--primary));
  border-radius: 2px;
  animation: indeterminate 1.5s ease-in-out infinite;
}

@keyframes indeterminate {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(400%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .progress-indeterminate::after {
    animation: none;
    width: 100%;
    opacity: 0.5;
  }
}
```

### Circular Progress

```yaml
name: circular-progress
use_case: Percentage completion, stats
animation_type: value-based

circle:
  stroke_width: 4px
  radius: 40px
  background_stroke: var(--muted)
  fill_stroke: var(--primary)

calculation:
  circumference: 2 * π * radius
  stroke_dasharray: circumference
  stroke_dashoffset: circumference * (1 - value/100)
```

**SVG Implementation**:
```tsx
interface CircularProgressProps {
  value: number  // 0-100
  size?: number
  strokeWidth?: number
}

function CircularProgress({
  value,
  size = 80,
  strokeWidth = 4,
}: CircularProgressProps) {
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference * (1 - value / 100)

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      role="progressbar"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      {/* Background circle */}
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke="hsl(var(--muted))"
        strokeWidth={strokeWidth}
      />
      {/* Progress circle */}
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke="hsl(var(--primary))"
        strokeWidth={strokeWidth}
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        style={{ transition: 'stroke-dashoffset 300ms ease-out' }}
      />
    </svg>
  )
}
```

---

## Content Loading Patterns

### Lazy Load Fade In

```yaml
name: lazy-fade-in
use_case: Images, heavy content after load
trigger: content loaded
duration: 300ms
easing: ease-out

initial:
  opacity: 0

animate:
  opacity: 1
```

**CSS Implementation**:
```css
.lazy-load {
  opacity: 0;
  transition: opacity 300ms ease-out;
}

.lazy-load.loaded {
  opacity: 1;
}
```

**React Hook**:
```tsx
function useLazyLoad<T extends HTMLElement>(ref: React.RefObject<T>) {
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    if (!ref.current) return

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsLoaded(true)
          observer.disconnect()
        }
      },
      { threshold: 0.1 }
    )

    observer.observe(ref.current)
    return () => observer.disconnect()
  }, [ref])

  return isLoaded
}
```

### Image Placeholder to Full

```yaml
name: image-placeholder
use_case: Image loading with blur placeholder
phases:
  - phase: placeholder
    filter: blur(20px)
    transform: scale(1.1)

  - phase: loaded
    filter: blur(0)
    transform: scale(1)
    duration: 500ms
    easing: ease-out
```

**CSS Implementation**:
```css
.image-container {
  overflow: hidden;
}

.image-placeholder {
  filter: blur(20px);
  transform: scale(1.1);
  transition: filter 500ms ease-out, transform 500ms ease-out;
}

.image-placeholder.loaded {
  filter: blur(0);
  transform: scale(1);
}
```

**React Component**:
```tsx
function BlurImage({ src, alt, placeholder }: {
  src: string
  alt: string
  placeholder: string  // Low-res or blur hash
}) {
  const [isLoaded, setIsLoaded] = useState(false)

  return (
    <div className="image-container">
      <img
        src={isLoaded ? src : placeholder}
        alt={alt}
        className={cn('image-placeholder', isLoaded && 'loaded')}
        onLoad={() => setIsLoaded(true)}
      />
      {!isLoaded && (
        <img
          src={src}
          alt=""
          style={{ display: 'none' }}
          onLoad={() => setIsLoaded(true)}
        />
      )}
    </div>
  )
}
```

---

## Button Loading States

### Button with Spinner

```yaml
name: button-loading
use_case: Form submissions, async actions
transition:
  text:
    opacity: 0
    duration: 100ms

  spinner:
    opacity: 1
    delay: 50ms

min_width: preserve  # Prevent layout shift
```

**React Component**:
```tsx
interface ButtonProps {
  loading?: boolean
  children: React.ReactNode
}

function Button({ loading, children, ...props }: ButtonProps) {
  return (
    <button
      {...props}
      disabled={loading || props.disabled}
      className={cn('button', loading && 'button-loading')}
    >
      <span className={cn('button-text', loading && 'opacity-0')}>
        {children}
      </span>
      {loading && (
        <span className="button-spinner">
          <Spinner size="sm" />
        </span>
      )}
    </button>
  )
}
```

```css
.button {
  position: relative;
  min-width: 100px;  /* Prevent shrinking */
}

.button-text {
  transition: opacity 100ms ease-out;
}

.button-loading .button-text {
  opacity: 0;
}

.button-spinner {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Button with Progress

```yaml
name: button-progress
use_case: File uploads, multi-step operations
animation:
  fill_direction: left-to-right
  background: linear-gradient overlay
```

**React Component**:
```tsx
function ProgressButton({
  progress,
  children,
}: {
  progress: number | null  // null = not loading
  children: React.ReactNode
}) {
  return (
    <button
      className="progress-button"
      disabled={progress !== null}
      style={{
        '--progress': progress !== null ? `${progress}%` : '0%',
      } as React.CSSProperties}
    >
      {progress !== null && (
        <span className="progress-fill" />
      )}
      <span className="button-text">
        {progress !== null ? `${Math.round(progress)}%` : children}
      </span>
    </button>
  )
}
```

```css
.progress-button {
  position: relative;
  overflow: hidden;
}

.progress-fill {
  position: absolute;
  inset: 0;
  width: var(--progress);
  background: hsl(var(--primary) / 0.2);
  transition: width 150ms ease-out;
}

.progress-button .button-text {
  position: relative;
  z-index: 1;
}
```

---

## Accessibility

### Screen Reader Announcements

```tsx
// Live region for loading state
function LoadingAnnouncement({ isLoading }: { isLoading: boolean }) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {isLoading ? 'Loading...' : 'Content loaded'}
    </div>
  )
}
```

### Reduced Motion Alternatives

```css
@media (prefers-reduced-motion: reduce) {
  /* Spinners: show static indicator */
  .spinner,
  .dots-spinner .dot {
    animation: none;
  }

  /* Progress: instant transitions */
  .progress-fill {
    transition: none;
  }

  /* Skeletons: solid color, no animation */
  .skeleton {
    animation: none;
    background: hsl(var(--muted));
  }
}
```

### ARIA Attributes

```tsx
// Progress bar
<div
  role="progressbar"
  aria-valuenow={value}
  aria-valuemin={0}
  aria-valuemax={100}
  aria-label="Loading progress"
/>

// Indeterminate
<div
  role="progressbar"
  aria-label="Loading"
  aria-busy="true"
/>

// Spinner
<div
  role="status"
  aria-label="Loading"
>
  <span className="sr-only">Loading...</span>
</div>
```

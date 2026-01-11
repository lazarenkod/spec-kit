# Button Examples (Few-Shot)

High-quality button implementations demonstrating best practices for accessibility, token usage, and interaction design.

## Example 1: Primary Action Button

### Specification
- **Purpose**: Primary call-to-action for critical user actions
- **States**: Default, hover, active, focus, disabled, loading
- **Accessibility**: ARIA label, keyboard navigation, 44×44px minimum touch target
- **Variants**: Default (md), small (sm), large (lg)

### Code
```tsx
import { ButtonHTMLAttributes, ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface PrimaryButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export function PrimaryButton({
  children,
  size = 'md',
  isLoading = false,
  disabled,
  className,
  ...props
}: PrimaryButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        'inline-flex items-center justify-center',
        'font-medium rounded-md transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',

        // Token-based colors
        'bg-primary text-primary-foreground',
        'hover:bg-primary/90',
        'focus-visible:ring-primary',

        // Token-based sizing
        size === 'sm' && 'h-9 px-3 text-sm',  // 36px height
        size === 'md' && 'h-11 px-4 text-base', // 44px height (WCAG)
        size === 'lg' && 'h-12 px-6 text-lg',   // 48px height

        // Disabled state
        'disabled:opacity-50 disabled:pointer-events-none',

        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && (
        <svg
          className="mr-2 h-4 w-4 animate-spin"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      {children}
    </button>
  );
}
```

### Why This Works
- **Token Usage**: Uses `bg-primary`, `text-primary-foreground` instead of hardcoded colors (prevents AP-VIS-001)
- **Touch Targets**: Default size is 44px height (WCAG 2.1 AAA compliant, prevents AP-A11Y-002)
- **Focus Indicators**: Clear ring on focus-visible (prevents AP-A11Y-004)
- **Loading State**: Visual feedback with spinner (prevents AP-COMP-001)
- **Semantic HTML**: Uses `<button>` element (prevents AP-COMP-007)
- **Transition**: Smooth color transition on hover (prevents AP-ANIM-004)

---

## Example 2: Secondary/Outline Button

### Specification
- **Purpose**: Secondary actions, less visual weight than primary
- **States**: Default, hover, active, focus, disabled
- **Style**: Border outline, transparent background
- **Accessibility**: Same standards as primary

### Code
```tsx
export function SecondaryButton({
  children,
  size = 'md',
  className,
  ...props
}: PrimaryButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center',
        'font-medium rounded-md transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',

        // Outline style with tokens
        'border-2 border-primary bg-transparent text-primary',
        'hover:bg-primary/10',
        'focus-visible:ring-primary',

        size === 'sm' && 'h-9 px-3 text-sm',
        size === 'md' && 'h-11 px-4 text-base',
        size === 'lg' && 'h-12 px-6 text-lg',

        'disabled:opacity-50 disabled:pointer-events-none',

        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
```

### Why This Works
- **Visual Hierarchy**: Lower visual weight than primary (prevents AP-VIS-003)
- **Token Consistency**: Uses same color tokens with different application
- **Hover Feedback**: Subtle background on hover (prevents AP-ANIM-003)
- **Border Width**: 2px border ensures visibility at 4.5:1 contrast (WCAG AA)

---

## Example 3: Icon Button

### Specification
- **Purpose**: Actions with icon-only representation
- **States**: Default, hover, active, focus, disabled
- **Accessibility**: **CRITICAL** - Must have aria-label (prevents AP-A11Y-003)
- **Size**: Square 44×44px minimum

### Code
```tsx
import { LucideIcon } from 'lucide-react';

interface IconButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  icon: LucideIcon;
  label: string;  // Required for accessibility
  size?: 'sm' | 'md' | 'lg';
}

export function IconButton({
  icon: Icon,
  label,
  size = 'md',
  className,
  ...props
}: IconButtonProps) {
  return (
    <button
      aria-label={label}  // CRITICAL: Screen reader support
      title={label}       // Tooltip on hover
      className={cn(
        'inline-flex items-center justify-center',
        'rounded-md transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',

        'bg-transparent text-foreground',
        'hover:bg-accent hover:text-accent-foreground',
        'focus-visible:ring-primary',

        // Square dimensions for touch targets
        size === 'sm' && 'h-9 w-9',   // 36px
        size === 'md' && 'h-11 w-11', // 44px (WCAG)
        size === 'lg' && 'h-12 w-12', // 48px

        'disabled:opacity-50 disabled:pointer-events-none',

        className
      )}
      {...props}
    >
      <Icon className={cn(
        size === 'sm' && 'h-4 w-4',
        size === 'md' && 'h-5 w-5',
        size === 'lg' && 'h-6 w-6'
      )} />
      <span className="sr-only">{label}</span>
    </button>
  );
}
```

### Why This Works
- **Accessibility**: `aria-label` + `sr-only` span provides screen reader support (prevents AP-A11Y-003)
- **Touch Target**: 44×44px square ensures mobile usability (prevents AP-A11Y-002)
- **Visual Feedback**: Hover state with background color (prevents missing feedback)
- **Icon Sizing**: Consistent icon scale relative to button size (prevents AP-COMP-003)

---

## Example 4: Button with Icon + Text

### Specification
- **Purpose**: Action with both icon and label for clarity
- **States**: Default, hover, active, focus, disabled, loading
- **Layout**: Icon on left, text on right with proper spacing
- **Accessibility**: Text provides context, icon enhances recognition

### Code
```tsx
interface IconTextButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  icon: LucideIcon;
  children: ReactNode;
  iconPosition?: 'left' | 'right';
  size?: 'sm' | 'md' | 'lg';
}

export function IconTextButton({
  icon: Icon,
  children,
  iconPosition = 'left',
  size = 'md',
  className,
  ...props
}: IconTextButtonProps) {
  const iconSize = size === 'sm' ? 'h-4 w-4' : size === 'md' ? 'h-5 w-5' : 'h-6 w-6';
  const iconSpacing = iconPosition === 'left' ? 'mr-2' : 'ml-2';

  return (
    <button
      className={cn(
        'inline-flex items-center justify-center',
        'font-medium rounded-md transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',

        'bg-primary text-primary-foreground',
        'hover:bg-primary/90',
        'focus-visible:ring-primary',

        size === 'sm' && 'h-9 px-3 text-sm',
        size === 'md' && 'h-11 px-4 text-base',
        size === 'lg' && 'h-12 px-6 text-lg',

        'disabled:opacity-50 disabled:pointer-events-none',

        className
      )}
      {...props}
    >
      {iconPosition === 'left' && <Icon className={cn(iconSize, iconSpacing)} />}
      {children}
      {iconPosition === 'right' && <Icon className={cn(iconSize, iconSpacing)} />}
    </button>
  );
}
```

### Why This Works
- **Clarity**: Text + icon provides redundant communication (accessibility best practice)
- **Spacing**: Token-based spacing (mr-2 = 8px) creates visual rhythm (prevents AP-VIS-002)
- **Flexibility**: Icon position configurable without duplicating code
- **Consistency**: Same color and sizing tokens as other buttons

---

## Example 5: Destructive Action Button

### Specification
- **Purpose**: Dangerous actions (delete, remove, cancel)
- **States**: Default, hover, active, focus, disabled
- **Color**: Red/destructive semantic color
- **Pattern**: Often paired with confirmation dialog

### Code
```tsx
export function DestructiveButton({
  children,
  size = 'md',
  className,
  ...props
}: PrimaryButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center',
        'font-medium rounded-md transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',

        // Destructive semantic color (token-based)
        'bg-destructive text-destructive-foreground',
        'hover:bg-destructive/90',
        'focus-visible:ring-destructive',

        size === 'sm' && 'h-9 px-3 text-sm',
        size === 'md' && 'h-11 px-4 text-base',
        size === 'lg' && 'h-12 px-6 text-lg',

        'disabled:opacity-50 disabled:pointer-events-none',

        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
```

### Why This Works
- **Semantic Color**: Uses `destructive` token instead of hardcoded red (prevents AP-VIS-001, AP-VIS-005)
- **Contrast**: Destructive colors pre-validated for WCAG compliance (prevents AP-A11Y-001)
- **Action Clarity**: Color + text label = clear communication (prevents AP-COMP-004)
- **Hover Feedback**: Slight darkening on hover provides confidence (prevents missing feedback)

---

## Usage Guidelines

### When to Use Each Variant
- **Primary**: Single most important action per screen (max 1-2)
- **Secondary**: Alternative actions, less emphasis
- **Icon**: Space-constrained UI, toolbar actions
- **Icon + Text**: When icon alone isn't clear enough
- **Destructive**: Delete, remove, or irreversible actions

### Common Anti-Patterns to Avoid
- ❌ Multiple primary buttons (AP-VIS-003)
- ❌ Icon buttons without aria-label (AP-A11Y-003)
- ❌ Hardcoded colors like `bg-blue-500` (AP-VIS-001)
- ❌ Buttons smaller than 44×44px (AP-A11Y-002)
- ❌ Missing hover/focus states (AP-A11Y-004)
- ❌ Using `<div onClick>` instead of `<button>` (AP-COMP-007)

### Accessibility Checklist
- ✓ Minimum 44×44px touch target
- ✓ 4.5:1 color contrast ratio (WCAG AA)
- ✓ Visible focus indicator
- ✓ Keyboard navigable (Tab, Enter, Space)
- ✓ Aria-label for icon-only buttons
- ✓ Disabled state prevents interaction
- ✓ Loading state prevents double-submit

---

## Integration with Design Tokens

All button examples use semantic tokens:

```css
/* Token definitions (example) */
:root {
  --primary: 220 90% 56%;           /* hsl values */
  --primary-foreground: 0 0% 100%;
  --destructive: 0 84% 60%;
  --destructive-foreground: 0 0% 100%;
  --accent: 220 14% 96%;
  --accent-foreground: 220 9% 46%;
}
```

This enables:
- Theme switching (light/dark)
- Brand customization without code changes
- Automatic contrast compliance
- Consistent visual language

---

**Version:** v0.2.0
**Last Updated:** 2026-01-10

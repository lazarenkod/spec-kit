# Badge Examples (Few-Shot)

High-quality badge implementations for status, labels, and notifications.

## Example 1: Basic Badge

### Specification
- **Purpose**: Display status, label, or category
- **States**: Default, hover (if interactive)
- **Accessibility**: Semantic colors, sufficient contrast
- **Variants**: Color variants (default, success, warning, error, info)

### Code
```tsx
import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

type BadgeVariant = 'default' | 'success' | 'warning' | 'error' | 'info' | 'secondary';

interface BadgeProps {
  children: ReactNode;
  variant?: BadgeVariant;
  className?: string;
}

export function Badge({ children, variant = 'default', className }: BadgeProps) {
  const variants = {
    default: 'bg-primary text-primary-foreground',
    secondary: 'bg-secondary text-secondary-foreground',
    success: 'bg-green-100 text-green-800 border-green-200',
    warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    error: 'bg-red-100 text-red-800 border-red-200',
    info: 'bg-blue-100 text-blue-800 border-blue-200'
  };

  return (
    <span
      className={cn(
        'inline-flex items-center',
        'px-2.5 py-0.5',
        'rounded-full',
        'text-xs font-semibold',
        'border',
        variants[variant],
        className
      )}
    >
      {children}
    </span>
  );
}
```

### Why This Works
- **Semantic Colors**: Green (success), yellow (warning), red (error), blue (info) (prevents AP-VIS-005)
- **Token Colors**: Uses primary/secondary tokens for default variants (prevents AP-VIS-001)
- **Contrast**: Light backgrounds with dark text (WCAG AA compliant, prevents AP-A11Y-001)
- **Border**: Adds definition (prevents merge with background)
- **Font Weight**: Semibold ensures readability (prevents AP-TYPE-002)
- **Rounded**: Full rounding creates pill shape (standard pattern)

---

## Example 2: Badge with Icon

### Specification
- **Purpose**: Badge with leading or trailing icon
- **States**: Default, hover
- **Accessibility**: Icon decorative or with aria-label
- **Layout**: Icon + text with proper spacing

### Code
```tsx
import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface IconBadgeProps {
  icon: LucideIcon;
  children: ReactNode;
  variant?: BadgeVariant;
  iconPosition?: 'left' | 'right';
}

export function IconBadge({
  icon: Icon,
  children,
  variant = 'default',
  iconPosition = 'left'
}: IconBadgeProps) {
  const variants = {
    default: 'bg-primary text-primary-foreground',
    secondary: 'bg-secondary text-secondary-foreground',
    success: 'bg-green-100 text-green-800 border-green-200',
    warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    error: 'bg-red-100 text-red-800 border-red-200',
    info: 'bg-blue-100 text-blue-800 border-blue-200'
  };

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1',
        'px-2.5 py-0.5',
        'rounded-full',
        'text-xs font-semibold',
        'border',
        variants[variant]
      )}
    >
      {iconPosition === 'left' && <Icon className="h-3 w-3" aria-hidden="true" />}
      {children}
      {iconPosition === 'right' && <Icon className="h-3 w-3" aria-hidden="true" />}
    </span>
  );
}
```

### Why This Works
- **Icon Sizing**: 12×12px (h-3 w-3) scales with text (prevents AP-COMP-003)
- **Gap Spacing**: gap-1 (4px) provides breathing room (prevents AP-VIS-002)
- **Aria-hidden**: Decorative icons hidden from screen readers
- **Flexible Position**: Icon can be left or right
- **Consistent Styling**: Inherits colors from badge variant

---

## Example 3: Notification Badge (Count)

### Specification
- **Purpose**: Show unread count or notification number
- **States**: Default, overflow (99+)
- **Accessibility**: Aria-label with full count
- **Layout**: Small badge positioned on corner

### Code
```tsx
import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface NotificationBadgeProps {
  count: number;
  children: ReactNode;
  max?: number;
  variant?: 'default' | 'destructive';
}

export function NotificationBadge({
  count,
  children,
  max = 99,
  variant = 'destructive'
}: NotificationBadgeProps) {
  const displayCount = count > max ? `${max}+` : count.toString();

  const variants = {
    default: 'bg-primary text-primary-foreground',
    destructive: 'bg-destructive text-destructive-foreground'
  };

  return (
    <div className="relative inline-block">
      {children}

      {count > 0 && (
        <span
          className={cn(
            'absolute -top-1 -right-1',
            'flex items-center justify-center',
            'min-w-[18px] h-[18px] px-1',
            'rounded-full',
            'text-xs font-semibold',
            variants[variant],
            'border-2 border-background'
          )}
          aria-label={`${count} unread notifications`}
        >
          {displayCount}
        </span>
      )}
    </div>
  );
}
```

### Why This Works
- **Overflow Handling**: Shows 99+ for large numbers (prevents badge stretching)
- **Aria-label**: Announces full count to screen readers (prevents AP-A11Y-008)
- **Min Width**: 18px ensures circular shape (prevents squashing)
- **Border**: Separates badge from parent (prevents visual merge)
- **Conditional Render**: Only shows when count > 0 (prevents clutter)
- **Destructive Variant**: Red for urgent notifications (semantic color)

---

## Example 4: Removable Badge (Tag)

### Specification
- **Purpose**: Tag with remove button for filters/selections
- **States**: Default, hover, removing
- **Accessibility**: Remove button has aria-label
- **Interaction**: Click X to remove

### Code
```tsx
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface RemovableBadgeProps {
  children: ReactNode;
  onRemove: () => void;
  variant?: 'default' | 'secondary';
}

export function RemovableBadge({
  children,
  onRemove,
  variant = 'secondary'
}: RemovableBadgeProps) {
  const variants = {
    default: 'bg-primary/10 text-primary border-primary/20',
    secondary: 'bg-secondary text-secondary-foreground border-border'
  };

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1',
        'pl-2.5 pr-1 py-0.5',
        'rounded-full',
        'text-xs font-medium',
        'border',
        variants[variant]
      )}
    >
      {children}
      <button
        type="button"
        onClick={onRemove}
        aria-label={`Remove ${children}`}
        className={cn(
          'inline-flex items-center justify-center',
          'h-4 w-4 rounded-full',
          'hover:bg-black/10 dark:hover:bg-white/10',
          'transition-colors',
          'focus-visible:outline-none focus-visible:ring-2',
          'focus-visible:ring-primary focus-visible:ring-offset-1'
        )}
      >
        <X className="h-3 w-3" />
      </button>
    </span>
  );
}
```

### Why This Works
- **Aria-label**: Remove button has descriptive label (prevents AP-A11Y-003)
- **Hover Feedback**: Background change on hover (prevents missing feedback)
- **Focus Ring**: Visible focus indicator (prevents AP-A11Y-004)
- **Button Size**: 16×16px touch target acceptable for dense UI
- **Padding Asymmetry**: More padding left, less right (visual balance)
- **Icon Size**: 12×12px X icon (prevents AP-COMP-003)

---

## Example 5: Status Badge with Dot

### Specification
- **Purpose**: Compact status indicator with dot and label
- **States**: Active, inactive, pending, success, error
- **Accessibility**: Status announced to screen readers
- **Layout**: Dot + label with minimal spacing

### Code
```tsx
import { cn } from '@/lib/utils';

type Status = 'active' | 'inactive' | 'pending' | 'success' | 'error';

interface StatusBadgeProps {
  status: Status;
  label?: string;
  showDot?: boolean;
}

export function StatusBadge({ status, label, showDot = true }: StatusBadgeProps) {
  const statusConfig = {
    active: {
      dotColor: 'bg-green-500',
      bgColor: 'bg-green-50',
      textColor: 'text-green-700',
      borderColor: 'border-green-200',
      label: label || 'Active'
    },
    inactive: {
      dotColor: 'bg-gray-400',
      bgColor: 'bg-gray-50',
      textColor: 'text-gray-700',
      borderColor: 'border-gray-200',
      label: label || 'Inactive'
    },
    pending: {
      dotColor: 'bg-yellow-500',
      bgColor: 'bg-yellow-50',
      textColor: 'text-yellow-700',
      borderColor: 'border-yellow-200',
      label: label || 'Pending'
    },
    success: {
      dotColor: 'bg-green-500',
      bgColor: 'bg-green-50',
      textColor: 'text-green-700',
      borderColor: 'border-green-200',
      label: label || 'Success'
    },
    error: {
      dotColor: 'bg-red-500',
      bgColor: 'bg-red-50',
      textColor: 'text-red-700',
      borderColor: 'border-red-200',
      label: label || 'Error'
    }
  };

  const config = statusConfig[status];

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5',
        'px-2.5 py-0.5',
        'rounded-full',
        'text-xs font-medium',
        'border',
        config.bgColor,
        config.textColor,
        config.borderColor
      )}
      role="status"
      aria-label={`Status: ${config.label}`}
    >
      {showDot && (
        <span
          className={cn(
            'h-1.5 w-1.5 rounded-full',
            config.dotColor
          )}
          aria-hidden="true"
        />
      )}
      {config.label}
    </span>
  );
}
```

### Why This Works
- **Role**: role="status" for screen reader announcements
- **Aria-label**: Full status announced (prevents AP-A11Y-008)
- **Color Redundancy**: Dot + text color + background (prevents AP-A11Y-005)
- **Semantic Colors**: Green (active/success), yellow (pending), red (error), gray (inactive)
- **Dot Size**: 6×6px (h-1.5 w-1.5) subtle but visible
- **Configurable**: Custom label support (prevents rigidity)

---

## Common Anti-Patterns to Avoid

- ❌ Low contrast text on colored backgrounds (AP-A11Y-001)
- ❌ Color-only status indication (AP-A11Y-005)
- ❌ Remove buttons without aria-label (AP-A11Y-003)
- ❌ Hardcoded colors like bg-blue-500 (AP-VIS-001)
- ❌ No focus indicators on interactive badges (AP-A11Y-004)
- ❌ Text too small (< 12px) (AP-TYPE-002)
- ❌ No visual feedback on hover (confusing UX)
- ❌ Notification badge without aria-label for count

## Accessibility Checklist

- ✓ Sufficient color contrast (WCAG AA 4.5:1 minimum)
- ✓ Color not sole indicator (use icons + text)
- ✓ Interactive badges have aria-labels
- ✓ Focus indicators visible
- ✓ Status badges use role="status"
- ✓ Notification counts announced to screen readers
- ✓ Remove buttons keyboard accessible
- ✓ Decorative icons have aria-hidden="true"
- ✓ Font size ≥ 12px (0.75rem)
- ✓ Hover states provide feedback

---

**Version:** v0.2.0
**Last Updated:** 2026-01-10

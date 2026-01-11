# Card Examples (Few-Shot)

High-quality card component implementations for content containers.

## Example 1: Basic Content Card

### Specification
- **Purpose**: Container for related content with optional header/footer
- **States**: Default, hover (if interactive), focus (if clickable)
- **Accessibility**: Semantic landmarks, heading hierarchy
- **Layout**: Flexible padding, rounded corners, subtle shadow

### Code
```tsx
import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface CardProps {
  children: ReactNode;
  className?: string;
}

export function Card({ children, className }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-lg border border-border bg-card text-card-foreground',
        'shadow-sm',  // Token-based shadow
        className
      )}
    >
      {children}
    </div>
  );
}

export function CardHeader({ children, className }: CardProps) {
  return (
    <div className={cn('flex flex-col space-y-1.5 p-6', className)}>
      {children}
    </div>
  );
}

export function CardTitle({ children, className }: CardProps) {
  return (
    <h3 className={cn('text-2xl font-semibold leading-none tracking-tight', className)}>
      {children}
    </h3>
  );
}

export function CardDescription({ children, className }: CardProps) {
  return (
    <p className={cn('text-sm text-muted-foreground', className)}>
      {children}
    </p>
  );
}

export function CardContent({ children, className }: CardProps) {
  return <div className={cn('p-6 pt-0', className)}>{children}</div>;
}

export function CardFooter({ children, className }: CardProps) {
  return (
    <div className={cn('flex items-center p-6 pt-0', className)}>
      {children}
    </div>
  );
}
```

### Why This Works
- **Token Colors**: Uses `bg-card`, `text-card-foreground`, `border-border` (prevents AP-VIS-001)
- **Composability**: Separate components for header/content/footer (prevents AP-COMP-005)
- **Semantic HTML**: Uses proper heading tags (prevents AP-COMP-007)
- **Spacing Scale**: Token-based padding (p-6 = 24px) (prevents AP-VIS-002)

---

## Example 2: Interactive/Clickable Card

### Specification
- **Purpose**: Card that acts as a clickable link/button
- **States**: Default, hover, focus, active
- **Accessibility**: Entire card clickable, keyboard accessible
- **UX**: Clear hover feedback, pointer cursor

### Code
```tsx
import Link from 'next/link';

interface InteractiveCardProps {
  href: string;
  title: string;
  description: string;
  icon?: ReactNode;
}

export function InteractiveCard({
  href,
  title,
  description,
  icon
}: InteractiveCardProps) {
  return (
    <Link
      href={href}
      className={cn(
        'group block rounded-lg border border-border',
        'bg-card text-card-foreground shadow-sm',
        'transition-all duration-200',
        'hover:shadow-md hover:border-primary/50',
        'focus-visible:outline-none focus-visible:ring-2',
        'focus-visible:ring-primary focus-visible:ring-offset-2'
      )}
    >
      <div className="p-6">
        {icon && (
          <div className="mb-4 text-primary">
            {icon}
          </div>
        )}
        <h3 className="mb-2 text-xl font-semibold group-hover:text-primary transition-colors">
          {title}
        </h3>
        <p className="text-sm text-muted-foreground">
          {description}
        </p>
      </div>
    </Link>
  );
}
```

### Why This Works
- **Semantic Link**: Uses `<Link>` for proper navigation (prevents AP-COMP-007)
- **Focus Indicator**: Ring on keyboard focus (prevents AP-A11Y-004)
- **Hover Feedback**: Shadow elevation + border color change (prevents missing feedback)
- **Group Hover**: Coordinated hover effects with `group` class
- **Transition**: Smooth 200ms animation (prevents AP-ANIM-004)

---

## Example 3: Card with Image

### Specification
- **Purpose**: Card with prominent image/thumbnail
- **States**: Default, hover, loading
- **Accessibility**: Alt text required, aspect ratio preserved
- **Layout**: Image at top, content below

### Code
```tsx
import Image from 'next/image';

interface ImageCardProps {
  title: string;
  description: string;
  imageSrc: string;
  imageAlt: string;
  href?: string;
}

export function ImageCard({
  title,
  description,
  imageSrc,
  imageAlt,
  href
}: ImageCardProps) {
  const content = (
    <>
      <div className="relative aspect-video w-full overflow-hidden rounded-t-lg bg-muted">
        <Image
          src={imageSrc}
          alt={imageAlt}
          fill
          className="object-cover transition-transform duration-300 group-hover:scale-105"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
      </div>
      <div className="p-6">
        <h3 className="mb-2 text-lg font-semibold">{title}</h3>
        <p className="text-sm text-muted-foreground line-clamp-2">
          {description}
        </p>
      </div>
    </>
  );

  const className = cn(
    'group overflow-hidden rounded-lg border border-border',
    'bg-card shadow-sm transition-shadow',
    href && 'hover:shadow-md cursor-pointer'
  );

  return href ? (
    <Link href={href} className={className}>
      {content}
    </Link>
  ) : (
    <div className={className}>{content}</div>
  );
}
```

### Why This Works
- **Image Optimization**: Uses Next.js Image with proper sizes (prevents AP-PERF-001)
- **Aspect Ratio**: `aspect-video` prevents layout shift (prevents AP-PERF-003)
- **Alt Text**: Required prop enforces accessibility (prevents AP-A11Y-006)
- **Hover Effect**: Subtle scale on image (prevents AP-ANIM-003)
- **Line Clamp**: Truncates long descriptions (prevents layout breaking)

---

## Example 4: Stats/Metric Card

### Specification
- **Purpose**: Display key metrics/statistics
- **States**: Default, loading
- **Accessibility**: Clear hierarchy, screen reader friendly
- **Layout**: Value emphasized, label secondary

### Code
```tsx
import { LucideIcon } from 'lucide-react';

interface StatsCardProps {
  title: string;
  value: string | number;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
  icon?: LucideIcon;
  trend?: ReactNode;
}

export function StatsCard({
  title,
  value,
  change,
  changeType = 'neutral',
  icon: Icon,
  trend
}: StatsCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold">{value}</div>
        {change && (
          <p
            className={cn(
              'text-xs flex items-center gap-1 mt-1',
              changeType === 'positive' && 'text-green-600',
              changeType === 'negative' && 'text-red-600',
              changeType === 'neutral' && 'text-muted-foreground'
            )}
          >
            {trend}
            <span>{change}</span>
          </p>
        )}
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- **Visual Hierarchy**: Large value, smaller label (prevents confusion)
- **Semantic Color**: Green/red for positive/negative (prevents AP-A11Y-005)
- **Icon Context**: Optional icon provides visual categorization
- **Trend Indicator**: Arrow/icon + text for redundancy (accessibility)

---

## Example 5: Action Card with Buttons

### Specification
- **Purpose**: Card with call-to-action buttons
- **States**: Default, loading
- **Accessibility**: Clear action hierarchy
- **Layout**: Content + button footer

### Code
```tsx
interface ActionCardProps {
  title: string;
  description: string;
  primaryAction: { label: string; onClick: () => void };
  secondaryAction?: { label: string; onClick: () => void };
  isLoading?: boolean;
}

export function ActionCard({
  title,
  description,
  primaryAction,
  secondaryAction,
  isLoading
}: ActionCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardFooter className="flex gap-2 justify-end">
        {secondaryAction && (
          <SecondaryButton
            onClick={secondaryAction.onClick}
            disabled={isLoading}
          >
            {secondaryAction.label}
          </SecondaryButton>
        )}
        <PrimaryButton
          onClick={primaryAction.onClick}
          isLoading={isLoading}
        >
          {primaryAction.label}
        </PrimaryButton>
      </CardFooter>
    </Card>
  );
}
```

### Why This Works
- **Action Hierarchy**: Primary on right, secondary on left (Western UX convention)
- **Loading State**: Disables interactions during async operations (prevents AP-COMP-001)
- **Button Reuse**: Leverages existing button components (prevents duplication)
- **Gap Spacing**: Token-based gap-2 (8px) between buttons (prevents AP-VIS-002)

---

## Common Anti-Patterns

- ❌ Hardcoded shadows like `shadow-[0_2px_4px_rgba(0,0,0,0.1)]` (AP-VIS-001)
- ❌ Inconsistent border radius across cards (AP-VIS-006)
- ❌ Clickable cards without focus indicators (AP-A11Y-004)
- ❌ Images without alt text (AP-A11Y-006)
- ❌ Cards with too many actions (>3 buttons) (AP-COMP-005)

## Accessibility Checklist

- ✓ Interactive cards are keyboard accessible
- ✓ Images have descriptive alt text
- ✓ Heading hierarchy (h2 → h3 → h4)
- ✓ Focus indicators visible
- ✓ Color not sole indicator of change (use icons + text)
- ✓ Touch targets ≥ 44×44px for mobile

---

**Version:** v0.2.0
**Last Updated:** 2026-01-10

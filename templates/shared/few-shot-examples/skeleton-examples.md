# Skeleton Examples (Few-Shot)

## Example 1: Card Skeleton Loader

### Specification
- Purpose: Show loading placeholders for card content
- States: Loading animation (pulse), content loaded
- Accessibility: ARIA live region announces loading state

### Code
```tsx
import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent, CardHeader } from '@/components/ui/card';

export function CardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-3 w-1/2 mt-2" />
      </CardHeader>
      <CardContent className="space-y-2">
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-3 w-4/5" />
      </CardContent>
    </Card>
  );
}

// Usage with actual content
export function CardWithLoading({ isLoading }: { isLoading: boolean }) {
  if (isLoading) {
    return <CardSkeleton />;
  }

  return (
    <Card>
      <CardHeader>
        <h3 className="font-semibold">Article Title</h3>
        <p className="text-sm text-muted-foreground">Published 2 days ago</p>
      </CardHeader>
      <CardContent>
        <p className="text-sm">
          This is the actual article content that appears after loading...
        </p>
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Skeleton matches actual content layout
- Varying widths (3/4, 1/2) create realistic effect
- Pulse animation shows activity
- Smooth transition when content loads
- Same card structure for consistency

---

## Example 2: Table Skeleton with Rows

### Specification
- Purpose: Loading placeholder for data tables
- States: Loading multiple rows, partial data loaded
- Accessibility: Screen reader announces table is loading

### Code
```tsx
import { Skeleton } from '@/components/ui/skeleton';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead><Skeleton className="h-4 w-24" /></TableHead>
          <TableHead><Skeleton className="h-4 w-32" /></TableHead>
          <TableHead><Skeleton className="h-4 w-20" /></TableHead>
          <TableHead><Skeleton className="h-4 w-16" /></TableHead>
        </TableRow>
      </TableHeader>
      <TableBody role="status" aria-label="Loading">
        {Array.from({ length: rows }).map((_, i) => (
          <TableRow key={i}>
            <TableCell><Skeleton className="h-4 w-24" /></TableCell>
            <TableCell><Skeleton className="h-4 w-32" /></TableCell>
            <TableCell><Skeleton className="h-4 w-20" /></TableCell>
            <TableCell><Skeleton className="h-4 w-16" /></TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
```

### Why This Works
- Configurable row count
- Skeleton headers match column structure
- Consistent widths per column
- ARIA role="status" for accessibility
- Array.from for clean row generation

---

## Example 3: Profile Skeleton with Avatar

### Specification
- Purpose: Loading state for user profiles
- States: Loading avatar + text content
- Accessibility: Descriptive loading label

### Code
```tsx
import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent } from '@/components/ui/card';

export function ProfileSkeleton() {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-start gap-4">
          {/* Avatar skeleton */}
          <Skeleton className="h-16 w-16 rounded-full flex-shrink-0" />

          {/* Content skeleton */}
          <div className="flex-1 space-y-2">
            <Skeleton className="h-5 w-32" />
            <Skeleton className="h-4 w-48" />
            <div className="flex gap-4 mt-4">
              <div className="space-y-1">
                <Skeleton className="h-6 w-12" />
                <Skeleton className="h-3 w-16" />
              </div>
              <div className="space-y-1">
                <Skeleton className="h-6 w-12" />
                <Skeleton className="h-3 w-16" />
              </div>
              <div className="space-y-1">
                <Skeleton className="h-6 w-12" />
                <Skeleton className="h-3 w-16" />
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Circular skeleton for avatar
- Flex layout matches actual profile
- Stats section with multiple columns
- Consistent spacing with actual content
- Realistic content hierarchy

---

## Example 4: Dashboard Grid Skeleton

### Specification
- Purpose: Loading multiple dashboard cards at once
- States: Loading all cards simultaneously
- Accessibility: Each card announces loading independently

### Code
```tsx
import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent, CardHeader } from '@/components/ui/card';

function MetricCardSkeleton() {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-4 w-4 rounded" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-7 w-20 mb-1" />
        <Skeleton className="h-3 w-32" />
      </CardContent>
    </Card>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="space-y-6" role="status" aria-label="Loading dashboard">
      {/* Metrics grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricCardSkeleton />
        <MetricCardSkeleton />
        <MetricCardSkeleton />
        <MetricCardSkeleton />
      </div>

      {/* Chart sections */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <Skeleton className="h-5 w-32" />
            <Skeleton className="h-3 w-48 mt-1" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-64 w-full" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <Skeleton className="h-5 w-32" />
            <Skeleton className="h-3 w-48 mt-1" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-64 w-full" />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
```

### Why This Works
- Reusable MetricCardSkeleton component
- Grid layout matches actual dashboard
- Different skeleton shapes (cards, charts)
- Responsive grid breaks
- Single loading announcement for whole dashboard

---

## Example 5: List with Avatar Skeleton

### Specification
- Purpose: Loading state for lists with avatars (messages, users, etc.)
- States: Loading multiple list items
- Accessibility: List role with loading items

### Code
```tsx
import { Skeleton } from '@/components/ui/skeleton';

function ListItemSkeleton() {
  return (
    <div className="flex items-start gap-3 p-3">
      <Skeleton className="h-10 w-10 rounded-full flex-shrink-0" />
      <div className="flex-1 space-y-2">
        <div className="flex items-center justify-between">
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-3 w-16" />
        </div>
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-3 w-3/4" />
      </div>
    </div>
  );
}

export function ListSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div
      className="divide-y divide-border"
      role="list"
      aria-label="Loading items"
    >
      {Array.from({ length: count }).map((_, i) => (
        <ListItemSkeleton key={i} />
      ))}
    </div>
  );
}

// Advanced: Staggered loading animation
export function StaggeredListSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div className="divide-y divide-border" role="list">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          style={{
            animation: `fadeIn 0.5s ease-in-out ${i * 0.1}s both`,
          }}
        >
          <ListItemSkeleton />
        </div>
      ))}
    </div>
  );
}

// Add to global CSS:
// @keyframes fadeIn {
//   from { opacity: 0; transform: translateY(10px); }
//   to { opacity: 1; transform: translateY(0); }
// }
```

### Why This Works
- Consistent item structure
- Configurable item count
- Avatar + text layout common pattern
- Optional staggered animation for polish
- Dividers match actual list styling
- Each item announces as loading

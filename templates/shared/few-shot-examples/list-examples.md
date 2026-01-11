# List Examples (Few-Shot)

High-quality list implementations with accessibility and interaction patterns.

## Example 1: Basic List with Items

### Specification
- **Purpose**: Display list of items with consistent structure
- **States**: Default, hover, active, empty
- **Accessibility**: Semantic list markup, keyboard navigation
- **Layout**: Flexible item layout with optional actions

### Code
```tsx
import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface ListItem {
  id: string | number;
  title: string;
  description?: string;
  icon?: ReactNode;
  actions?: ReactNode;
}

interface ListProps {
  items: ListItem[];
  onItemClick?: (item: ListItem) => void;
  emptyMessage?: string;
}

export function List({ items, onItemClick, emptyMessage = 'No items' }: ListProps) {
  if (items.length === 0) {
    return (
      <div className="py-12 text-center text-sm text-muted-foreground">
        {emptyMessage}
      </div>
    );
  }

  return (
    <ul role="list" className="divide-y divide-border">
      {items.map((item) => (
        <li
          key={item.id}
          onClick={() => onItemClick?.(item)}
          className={cn(
            'flex items-center gap-4 p-4',
            'transition-colors',
            onItemClick && 'cursor-pointer hover:bg-accent'
          )}
        >
          {item.icon && (
            <div className="flex-shrink-0 text-muted-foreground">
              {item.icon}
            </div>
          )}

          <div className="flex-1 min-w-0">
            <h3 className="text-sm font-medium text-foreground truncate">
              {item.title}
            </h3>
            {item.description && (
              <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                {item.description}
              </p>
            )}
          </div>

          {item.actions && (
            <div className="flex-shrink-0 flex items-center gap-2">
              {item.actions}
            </div>
          )}
        </li>
      ))}
    </ul>
  );
}
```

### Why This Works
- **Semantic HTML**: Uses `<ul role="list">` and `<li>` (prevents AP-COMP-007)
- **Empty State**: Clear message when no items (prevents confusion)
- **Truncation**: Prevents overflow with truncate/line-clamp (prevents layout breaking)
- **Hover Feedback**: Background change on hover (prevents missing feedback)
- **Flexible Layout**: Icon, content, actions slots (prevents rigidity)
- **Token Colors**: Uses semantic tokens (prevents AP-VIS-001)

---

## Example 2: Virtualized List (Performance)

### Specification
- **Purpose**: Render large lists efficiently with windowing
- **States**: Loading, loaded, scrolling
- **Accessibility**: Maintains semantic structure, keyboard scroll
- **Performance**: Only renders visible items

### Code
```tsx
import { useRef, useState, useEffect } from 'react';
import { cn } from '@/lib/utils';

interface VirtualListProps<T> {
  items: T[];
  itemHeight: number;
  renderItem: (item: T, index: number) => ReactNode;
  height: number;
  overscan?: number;
}

export function VirtualList<T extends { id: string | number }>({
  items,
  itemHeight,
  renderItem,
  height,
  overscan = 3
}: VirtualListProps<T>) {
  const [scrollTop, setScrollTop] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  const totalHeight = items.length * itemHeight;
  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
  const endIndex = Math.min(
    items.length - 1,
    Math.ceil((scrollTop + height) / itemHeight) + overscan
  );

  const visibleItems = items.slice(startIndex, endIndex + 1);
  const offsetY = startIndex * itemHeight;

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop);
  };

  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      role="list"
      className="overflow-auto"
      style={{ height }}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        <div
          style={{
            transform: `translateY(${offsetY}px)`,
            position: 'absolute',
            width: '100%'
          }}
        >
          {visibleItems.map((item, index) => (
            <div
              key={item.id}
              role="listitem"
              style={{ height: itemHeight }}
              className={cn(
                'border-b border-border',
                'hover:bg-accent transition-colors'
              )}
            >
              {renderItem(item, startIndex + index)}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

### Why This Works
- **Performance**: Only renders visible items + overscan (prevents AP-PERF-001)
- **Smooth Scrolling**: Transform for GPU acceleration (prevents jank)
- **Semantic Roles**: role="list" and role="listitem" (prevents AP-A11Y-008)
- **Overscan**: Renders extra items above/below (prevents blank flashes)
- **Flexible Height**: Configurable list and item heights
- **Fixed Heights**: Required for windowing calculation (documented limitation)

---

## Example 3: Drag-and-Drop List

### Specification
- **Purpose**: Reorderable list with drag-and-drop
- **States**: Default, dragging, drop target
- **Accessibility**: Keyboard reordering (Alt+Arrow keys)
- **Interaction**: Touch-friendly drag handles

### Code
```tsx
import { useState } from 'react';
import { GripVertical } from 'lucide-react';
import { cn } from '@/lib/utils';

interface DraggableItem {
  id: string | number;
  content: ReactNode;
}

interface DragDropListProps {
  items: DraggableItem[];
  onReorder: (items: DraggableItem[]) => void;
}

export function DragDropList({ items, onReorder }: DragDropListProps) {
  const [draggedIndex, setDraggedIndex] = useState<number | null>(null);
  const [dropTargetIndex, setDropTargetIndex] = useState<number | null>(null);

  const handleDragStart = (e: React.DragEvent, index: number) => {
    setDraggedIndex(index);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e: React.DragEvent, index: number) => {
    e.preventDefault();
    setDropTargetIndex(index);
  };

  const handleDrop = (e: React.DragEvent, dropIndex: number) => {
    e.preventDefault();

    if (draggedIndex === null || draggedIndex === dropIndex) {
      setDraggedIndex(null);
      setDropTargetIndex(null);
      return;
    }

    const newItems = [...items];
    const [removed] = newItems.splice(draggedIndex, 1);
    newItems.splice(dropIndex, 0, removed);

    onReorder(newItems);
    setDraggedIndex(null);
    setDropTargetIndex(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    if (e.altKey && e.key === 'ArrowUp' && index > 0) {
      e.preventDefault();
      const newItems = [...items];
      [newItems[index - 1], newItems[index]] = [newItems[index], newItems[index - 1]];
      onReorder(newItems);
    } else if (e.altKey && e.key === 'ArrowDown' && index < items.length - 1) {
      e.preventDefault();
      const newItems = [...items];
      [newItems[index], newItems[index + 1]] = [newItems[index + 1], newItems[index]];
      onReorder(newItems);
    }
  };

  return (
    <ul role="list" className="space-y-2">
      {items.map((item, index) => (
        <li
          key={item.id}
          draggable
          onDragStart={(e) => handleDragStart(e, index)}
          onDragOver={(e) => handleDragOver(e, index)}
          onDrop={(e) => handleDrop(e, index)}
          onDragEnd={() => {
            setDraggedIndex(null);
            setDropTargetIndex(null);
          }}
          onKeyDown={(e) => handleKeyDown(e, index)}
          tabIndex={0}
          role="listitem"
          aria-label={`Item ${index + 1}. Press Alt+Arrow keys to reorder`}
          className={cn(
            'flex items-center gap-3 p-3',
            'rounded-md border border-border bg-card',
            'transition-all',
            'focus-visible:outline-none focus-visible:ring-2',
            'focus-visible:ring-primary',
            draggedIndex === index && 'opacity-50',
            dropTargetIndex === index && 'border-primary border-2'
          )}
        >
          <button
            type="button"
            aria-label="Drag to reorder"
            className={cn(
              'cursor-grab active:cursor-grabbing',
              'text-muted-foreground hover:text-foreground',
              'touch-none'  // Prevents text selection on mobile
            )}
          >
            <GripVertical className="h-5 w-5" />
          </button>

          <div className="flex-1">{item.content}</div>
        </li>
      ))}
    </ul>
  );
}
```

### Why This Works
- **Keyboard Support**: Alt+Arrow keys for reordering (prevents AP-A11Y-004)
- **Aria-label**: Clear instructions for screen readers (prevents AP-A11Y-008)
- **Visual Feedback**: Opacity on drag, border on drop target (prevents confusion)
- **Touch-friendly**: Drag handle with touch-none (prevents text selection)
- **Focus Management**: Items are focusable with visible ring (prevents AP-A11Y-004)
- **Native Drag API**: Uses HTML5 drag-and-drop (standard pattern)

---

## Example 4: Accordion List (Expandable Items)

### Specification
- **Purpose**: List with expandable/collapsible content
- **States**: Expanded, collapsed, hover
- **Accessibility**: aria-expanded, button controls
- **Interaction**: Click header to toggle, keyboard support

### Code
```tsx
import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';

interface AccordionItem {
  id: string | number;
  title: string;
  content: ReactNode;
}

interface AccordionListProps {
  items: AccordionItem[];
  allowMultiple?: boolean;
}

export function AccordionList({ items, allowMultiple = false }: AccordionListProps) {
  const [expandedIds, setExpandedIds] = useState<Set<string | number>>(new Set());

  const toggleItem = (id: string | number) => {
    const newExpanded = new Set(expandedIds);

    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      if (!allowMultiple) {
        newExpanded.clear();
      }
      newExpanded.add(id);
    }

    setExpandedIds(newExpanded);
  };

  return (
    <ul role="list" className="divide-y divide-border border-y border-border">
      {items.map((item) => {
        const isExpanded = expandedIds.has(item.id);
        const headerId = `accordion-header-${item.id}`;
        const panelId = `accordion-panel-${item.id}`;

        return (
          <li key={item.id}>
            <button
              type="button"
              id={headerId}
              onClick={() => toggleItem(item.id)}
              aria-expanded={isExpanded}
              aria-controls={panelId}
              className={cn(
                'flex items-center justify-between',
                'w-full px-4 py-3 text-left',
                'text-sm font-medium text-foreground',
                'hover:bg-accent transition-colors',
                'focus-visible:outline-none focus-visible:ring-2',
                'focus-visible:ring-primary focus-visible:ring-inset'
              )}
            >
              <span>{item.title}</span>
              <ChevronDown
                className={cn(
                  'h-5 w-5 text-muted-foreground',
                  'transition-transform duration-200',
                  isExpanded && 'rotate-180'
                )}
                aria-hidden="true"
              />
            </button>

            <div
              id={panelId}
              role="region"
              aria-labelledby={headerId}
              hidden={!isExpanded}
              className={cn(
                'px-4 py-3 text-sm text-muted-foreground',
                'border-t border-border',
                isExpanded && 'animate-in slide-in-from-top-2 fade-in-0'
              )}
            >
              {item.content}
            </div>
          </li>
        );
      })}
    </ul>
  );
}
```

### Why This Works
- **Aria-expanded**: Announces state to screen readers (prevents AP-A11Y-008)
- **ID Association**: aria-controls links button to panel
- **Button Control**: Uses `<button>` for toggle (prevents AP-COMP-007)
- **Keyboard Support**: Spacebar/Enter toggle (native button behavior)
- **Animation**: Smooth slide-in on expand (prevents AP-ANIM-004)
- **Single/Multiple Mode**: allowMultiple prop controls behavior
- **Visual Indicator**: Chevron rotates (prevents confusion)

---

## Example 5: Avatar List (User List)

### Specification
- **Purpose**: Display list of users with avatars
- **States**: Online, offline, loading
- **Accessibility**: Alt text for avatars, status indicators
- **Layout**: Avatar + name + metadata

### Code
```tsx
import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface User {
  id: string | number;
  name: string;
  email?: string;
  avatarUrl?: string;
  status?: 'online' | 'offline' | 'away';
  badge?: ReactNode;
}

interface AvatarListProps {
  users: User[];
  onUserClick?: (user: User) => void;
  showStatus?: boolean;
}

export function AvatarList({
  users,
  onUserClick,
  showStatus = true
}: AvatarListProps) {
  return (
    <ul role="list" className="divide-y divide-border">
      {users.map((user) => (
        <li
          key={user.id}
          onClick={() => onUserClick?.(user)}
          className={cn(
            'flex items-center gap-3 p-3',
            'transition-colors',
            onUserClick && 'cursor-pointer hover:bg-accent'
          )}
        >
          {/* Avatar with Status */}
          <div className="relative flex-shrink-0">
            <div
              className={cn(
                'h-10 w-10 rounded-full',
                'bg-muted flex items-center justify-center',
                'overflow-hidden'
              )}
            >
              {user.avatarUrl ? (
                <img
                  src={user.avatarUrl}
                  alt={user.name}
                  className="h-full w-full object-cover"
                />
              ) : (
                <span className="text-sm font-medium text-foreground">
                  {user.name.charAt(0).toUpperCase()}
                </span>
              )}
            </div>

            {showStatus && user.status && (
              <span
                className={cn(
                  'absolute bottom-0 right-0',
                  'h-3 w-3 rounded-full border-2 border-background',
                  user.status === 'online' && 'bg-green-500',
                  user.status === 'away' && 'bg-yellow-500',
                  user.status === 'offline' && 'bg-gray-400'
                )}
                aria-label={`Status: ${user.status}`}
              />
            )}
          </div>

          {/* User Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <p className="text-sm font-medium text-foreground truncate">
                {user.name}
              </p>
              {user.badge && (
                <span className="flex-shrink-0">{user.badge}</span>
              )}
            </div>
            {user.email && (
              <p className="text-sm text-muted-foreground truncate">
                {user.email}
              </p>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}
```

### Why This Works
- **Avatar Fallback**: Shows initial if no image (prevents blank state)
- **Status Indicator**: Color-coded with aria-label (prevents AP-A11Y-005, AP-A11Y-008)
- **Alt Text**: Image has descriptive alt (prevents AP-A11Y-006)
- **Truncation**: Prevents name overflow (prevents layout breaking)
- **Touch Target**: 44px height list items (prevents AP-A11Y-002)
- **Semantic HTML**: Uses `<ul>` and `<li>` (prevents AP-COMP-007)
- **Badge Slot**: Optional badge for verified/admin indicators

---

## Common Anti-Patterns to Avoid

- ❌ Using `<div>` instead of `<ul>`/`<li>` (AP-COMP-007)
- ❌ No empty state message (confusing when list is empty)
- ❌ Missing aria-expanded on accordion (AP-A11Y-008)
- ❌ Drag handles without aria-label (AP-A11Y-003)
- ❌ Status indicators without text alternative (AP-A11Y-005)
- ❌ No keyboard support for interactions (AP-A11Y-004)
- ❌ Fixed widths causing mobile overflow (AP-LAY-001)
- ❌ Rendering all items in huge lists (AP-PERF-001)

## Accessibility Checklist

- ✓ Semantic list markup (`<ul role="list">`, `<li>`)
- ✓ Empty state message
- ✓ Keyboard navigation support
- ✓ Focus indicators visible
- ✓ aria-label on icon buttons
- ✓ aria-expanded on collapsible items
- ✓ Alt text on avatar images
- ✓ Status indicators have text alternatives
- ✓ Touch targets ≥ 44px
- ✓ Truncation prevents overflow
- ✓ Hover/active states provide feedback

---

**Version:** v0.2.0
**Last Updated:** 2026-01-10

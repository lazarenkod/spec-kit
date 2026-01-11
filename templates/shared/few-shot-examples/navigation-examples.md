# Navigation Examples (Few-Shot)

High-quality navigation implementations with accessibility and responsive design.

## Example 1: Horizontal Navigation Bar

### Specification
- **Purpose**: Primary site navigation with logo and links
- **States**: Default, hover, active (current page), mobile collapsed
- **Accessibility**: Keyboard navigation, aria-current for active link
- **Layout**: Logo left, links center/right, mobile hamburger menu

### Code
```tsx
import { useState } from 'react';
import Link from 'next/link';
import { Menu, X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface NavItem {
  label: string;
  href: string;
}

interface NavBarProps {
  logo: ReactNode;
  items: NavItem[];
  currentPath: string;
}

export function NavBar({ logo, items, currentPath }: NavBarProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-background border-b border-border">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link href="/" className="flex items-center">
              {logo}
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex md:items-center md:space-x-1">
            {items.map((item) => {
              const isCurrent = currentPath === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  aria-current={isCurrent ? 'page' : undefined}
                  className={cn(
                    'rounded-md px-3 py-2 text-sm font-medium',
                    'transition-colors',
                    'focus-visible:outline-none focus-visible:ring-2',
                    'focus-visible:ring-primary focus-visible:ring-offset-2',
                    isCurrent
                      ? 'bg-primary text-primary-foreground'
                      : 'text-foreground hover:bg-accent hover:text-accent-foreground'
                  )}
                >
                  {item.label}
                </Link>
              );
            })}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              type="button"
              onClick={() => setIsOpen(!isOpen)}
              aria-expanded={isOpen}
              aria-label="Toggle navigation menu"
              className={cn(
                'inline-flex items-center justify-center',
                'h-10 w-10 rounded-md',
                'text-foreground hover:bg-accent',
                'focus-visible:outline-none focus-visible:ring-2',
                'focus-visible:ring-primary'
              )}
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden">
          <div className="space-y-1 px-2 pb-3 pt-2">
            {items.map((item) => {
              const isCurrent = currentPath === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  aria-current={isCurrent ? 'page' : undefined}
                  onClick={() => setIsOpen(false)}
                  className={cn(
                    'block rounded-md px-3 py-2 text-base font-medium',
                    isCurrent
                      ? 'bg-primary text-primary-foreground'
                      : 'text-foreground hover:bg-accent'
                  )}
                >
                  {item.label}
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </nav>
  );
}
```

### Why This Works
- **Aria-current**: Marks active page for screen readers (prevents AP-A11Y-008)
- **Touch Targets**: 44px height buttons for mobile (prevents AP-A11Y-002)
- **Focus Indicators**: Visible ring on keyboard focus (prevents AP-A11Y-004)
- **Token Colors**: Uses semantic tokens (prevents AP-VIS-001)
- **Responsive**: Mobile hamburger menu below md breakpoint

---

## Example 2: Breadcrumb Navigation

### Specification
- **Purpose**: Show current location in site hierarchy
- **States**: Default, hover, collapsed for mobile
- **Accessibility**: aria-label, aria-current for current page
- **Layout**: Home icon → Parent → Child with separators

### Code
```tsx
import Link from 'next/link';
import { ChevronRight, Home } from 'lucide-react';
import { cn } from '@/lib/utils';

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
}

export function Breadcrumb({ items }: BreadcrumbProps) {
  return (
    <nav aria-label="Breadcrumb" className="flex">
      <ol className="flex items-center space-x-2">
        <li>
          <Link
            href="/"
            className={cn(
              'inline-flex items-center text-sm font-medium',
              'text-muted-foreground hover:text-foreground',
              'transition-colors',
              'focus-visible:outline-none focus-visible:ring-2',
              'focus-visible:ring-primary focus-visible:rounded'
            )}
          >
            <Home className="h-4 w-4" />
            <span className="sr-only">Home</span>
          </Link>
        </li>

        {items.map((item, index) => {
          const isLast = index === items.length - 1;
          return (
            <li key={index} className="flex items-center space-x-2">
              <ChevronRight className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
              {item.href && !isLast ? (
                <Link
                  href={item.href}
                  className={cn(
                    'text-sm font-medium text-muted-foreground',
                    'hover:text-foreground transition-colors',
                    'focus-visible:outline-none focus-visible:ring-2',
                    'focus-visible:ring-primary focus-visible:rounded'
                  )}
                >
                  {item.label}
                </Link>
              ) : (
                <span
                  className="text-sm font-medium text-foreground"
                  aria-current={isLast ? 'page' : undefined}
                >
                  {item.label}
                </span>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
```

### Why This Works
- **Semantic HTML**: Uses `<nav>`, `<ol>`, `<li>` (prevents AP-COMP-007)
- **Aria-label**: Clear navigation purpose (prevents AP-A11Y-008)
- **Icon Context**: Home icon with sr-only text (prevents AP-A11Y-003)
- **Current Page**: aria-current on last item (accessibility best practice)
- **Separators**: Decorative chevrons with aria-hidden

---

## Example 3: Tab Navigation

### Specification
- **Purpose**: Switch between related content panels
- **States**: Default, hover, active, focus, disabled
- **Accessibility**: role="tablist", aria-selected, keyboard navigation
- **Layout**: Horizontal tabs with active indicator

### Code
```tsx
import { useState, useId } from 'react';
import { cn } from '@/lib/utils';

interface Tab {
  id: string;
  label: string;
  content: ReactNode;
  disabled?: boolean;
}

interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
}

export function Tabs({ tabs, defaultTab }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0].id);
  const tabsId = useId();

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    if (e.key === 'ArrowRight') {
      e.preventDefault();
      const nextIndex = (index + 1) % tabs.length;
      setActiveTab(tabs[nextIndex].id);
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      const prevIndex = (index - 1 + tabs.length) % tabs.length;
      setActiveTab(tabs[prevIndex].id);
    }
  };

  return (
    <div>
      {/* Tab List */}
      <div
        role="tablist"
        aria-label="Content tabs"
        className="border-b border-border"
      >
        <div className="flex space-x-1">
          {tabs.map((tab, index) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                role="tab"
                id={`${tabsId}-tab-${tab.id}`}
                aria-controls={`${tabsId}-panel-${tab.id}`}
                aria-selected={isActive}
                disabled={tab.disabled}
                onClick={() => setActiveTab(tab.id)}
                onKeyDown={(e) => handleKeyDown(e, index)}
                tabIndex={isActive ? 0 : -1}
                className={cn(
                  'inline-flex items-center justify-center',
                  'px-4 py-2 text-sm font-medium',
                  'border-b-2 transition-colors',
                  'focus-visible:outline-none focus-visible:ring-2',
                  'focus-visible:ring-primary focus-visible:ring-offset-2',
                  isActive
                    ? 'border-primary text-primary'
                    : 'border-transparent text-muted-foreground hover:text-foreground hover:border-border',
                  'disabled:opacity-50 disabled:cursor-not-allowed'
                )}
              >
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Panels */}
      {tabs.map((tab) => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`${tabsId}-panel-${tab.id}`}
          aria-labelledby={`${tabsId}-tab-${tab.id}`}
          hidden={activeTab !== tab.id}
          className="py-4"
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

### Why This Works
- **ARIA Roles**: role="tablist/tab/tabpanel" for screen readers
- **Keyboard Navigation**: Arrow keys move between tabs (ARIA Authoring Practices)
- **Tab Index Management**: Only active tab is focusable (prevents tab traps)
- **ID Association**: aria-controls links tabs to panels
- **Visual Indicator**: Border-bottom on active tab (prevents confusion)

---

## Example 4: Sidebar Navigation

### Specification
- **Purpose**: Vertical navigation for app layouts
- **States**: Default, hover, active, collapsed, expanded
- **Accessibility**: Semantic nav, current page indication
- **Layout**: Collapsible with icon-only mode

### Code
```tsx
import { useState } from 'react';
import Link from 'next/link';
import { LucideIcon, ChevronLeft } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SidebarItem {
  label: string;
  href: string;
  icon: LucideIcon;
}

interface SidebarProps {
  items: SidebarItem[];
  currentPath: string;
}

export function Sidebar({ items, currentPath }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        'flex flex-col border-r border-border bg-card',
        'transition-all duration-300',
        isCollapsed ? 'w-16' : 'w-64'
      )}
    >
      {/* Collapse Toggle */}
      <div className="flex h-16 items-center justify-end px-4 border-b border-border">
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          className={cn(
            'h-8 w-8 rounded-md',
            'inline-flex items-center justify-center',
            'text-muted-foreground hover:bg-accent hover:text-foreground',
            'focus-visible:outline-none focus-visible:ring-2',
            'focus-visible:ring-primary'
          )}
        >
          <ChevronLeft
            className={cn(
              'h-5 w-5 transition-transform',
              isCollapsed && 'rotate-180'
            )}
          />
        </button>
      </div>

      {/* Navigation Items */}
      <nav className="flex-1 space-y-1 p-2">
        {items.map((item) => {
          const isCurrent = currentPath === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              aria-current={isCurrent ? 'page' : undefined}
              title={isCollapsed ? item.label : undefined}
              className={cn(
                'flex items-center gap-3 rounded-md px-3 py-2',
                'text-sm font-medium transition-colors',
                'focus-visible:outline-none focus-visible:ring-2',
                'focus-visible:ring-primary focus-visible:ring-offset-2',
                isCurrent
                  ? 'bg-primary text-primary-foreground'
                  : 'text-foreground hover:bg-accent hover:text-accent-foreground'
              )}
            >
              <Icon className="h-5 w-5 flex-shrink-0" />
              {!isCollapsed && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
```

### Why This Works
- **Collapsed State**: Icon-only mode with title tooltips (space-efficient)
- **Transition**: Smooth width animation (prevents AP-ANIM-004)
- **Touch Targets**: 44px height links (prevents AP-A11Y-002)
- **Icon Context**: Icons always visible, labels optional (prevents AP-A11Y-003)
- **Aria-current**: Marks active page (prevents AP-A11Y-008)

---

## Example 5: Mobile Bottom Navigation

### Specification
- **Purpose**: Primary navigation for mobile apps
- **States**: Default, active, badge notification
- **Accessibility**: Icons with labels, aria-label
- **Layout**: Fixed bottom bar with 3-5 items

### Code
```tsx
import Link from 'next/link';
import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface NavItem {
  label: string;
  href: string;
  icon: LucideIcon;
  badge?: number;
}

interface BottomNavProps {
  items: NavItem[];
  currentPath: string;
}

export function BottomNav({ items, currentPath }: BottomNavProps) {
  return (
    <nav
      className={cn(
        'fixed bottom-0 left-0 right-0 z-50',
        'border-t border-border bg-background',
        'md:hidden'  // Only on mobile
      )}
      aria-label="Primary navigation"
    >
      <div className="flex items-center justify-around h-16">
        {items.map((item) => {
          const isCurrent = currentPath === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              aria-current={isCurrent ? 'page' : undefined}
              aria-label={item.label}
              className={cn(
                'flex flex-col items-center justify-center',
                'min-w-[64px] h-full px-2',
                'transition-colors',
                'focus-visible:outline-none focus-visible:ring-2',
                'focus-visible:ring-primary focus-visible:ring-inset',
                isCurrent
                  ? 'text-primary'
                  : 'text-muted-foreground active:text-foreground'
              )}
            >
              <div className="relative">
                <Icon className="h-6 w-6" />
                {item.badge !== undefined && item.badge > 0 && (
                  <span
                    className={cn(
                      'absolute -top-1 -right-1',
                      'flex items-center justify-center',
                      'min-w-[18px] h-[18px] px-1',
                      'rounded-full',
                      'bg-destructive text-destructive-foreground',
                      'text-xs font-semibold'
                    )}
                    aria-label={`${item.badge} notifications`}
                  >
                    {item.badge > 99 ? '99+' : item.badge}
                  </span>
                )}
              </div>
              <span className="mt-1 text-xs font-medium">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
```

### Why This Works
- **Fixed Position**: Always accessible at screen bottom (mobile UX pattern)
- **Touch Targets**: 64px wide items (exceeds 44px minimum, prevents AP-A11Y-002)
- **Badge Notifications**: Clear visual indicator with aria-label
- **Icon + Label**: Redundant communication (prevents AP-A11Y-003)
- **Active State**: Color change for current page (prevents confusion)

---

## Common Anti-Patterns to Avoid

- ❌ Navigation without aria-current on active items (AP-A11Y-008)
- ❌ Icon-only navigation without labels or tooltips (AP-A11Y-003)
- ❌ Tabs without proper ARIA roles (role="tablist", etc.)
- ❌ Mobile menu button without aria-expanded (AP-A11Y-008)
- ❌ Keyboard navigation not supported (arrow keys in tabs)
- ❌ Touch targets smaller than 44px (AP-A11Y-002)
- ❌ Hardcoded colors instead of tokens (AP-VIS-001)

## Accessibility Checklist

- ✓ Semantic HTML (`<nav>`, `<ol>`, `<li>`)
- ✓ aria-current="page" on active links
- ✓ aria-label on navigation regions
- ✓ Keyboard navigable (Tab, Arrow keys for tabs)
- ✓ Focus indicators visible (ring on focus-visible)
- ✓ Touch targets ≥ 44×44px
- ✓ Icon buttons have aria-label
- ✓ Mobile menu has aria-expanded state
- ✓ Tab navigation uses proper roles and properties

---

**Version:** v0.2.0
**Last Updated:** 2026-01-10

# Table Examples (Few-Shot)

High-quality data table implementations with sorting, pagination, and accessibility.

## Example 1: Basic Data Table

### Specification
- **Purpose**: Display tabular data with semantic markup
- **States**: Default, hover, selected row
- **Accessibility**: Proper table structure, th scope, caption
- **Layout**: Responsive with horizontal scroll

### Code
```tsx
import { cn } from '@/lib/utils';

interface Column<T> {
  key: keyof T;
  header: string;
  render?: (value: T[keyof T], row: T) => ReactNode;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  caption?: string;
  onRowClick?: (row: T) => void;
}

export function Table<T extends { id: string | number }>({
  columns,
  data,
  caption,
  onRowClick
}: TableProps<T>) {
  return (
    <div className="w-full overflow-x-auto">
      <table className="w-full border-collapse">
        {caption && (
          <caption className="mb-4 text-left text-sm font-medium text-foreground">
            {caption}
          </caption>
        )}

        <thead>
          <tr className="border-b border-border">
            {columns.map((column) => (
              <th
                key={String(column.key)}
                scope="col"
                className={cn(
                  'px-4 py-3 text-left text-sm font-semibold',
                  'text-foreground bg-muted/50'
                )}
              >
                {column.header}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map((row) => (
            <tr
              key={row.id}
              onClick={() => onRowClick?.(row)}
              className={cn(
                'border-b border-border',
                'transition-colors',
                onRowClick && 'cursor-pointer hover:bg-muted/50'
              )}
            >
              {columns.map((column) => (
                <td
                  key={String(column.key)}
                  className="px-4 py-3 text-sm text-foreground"
                >
                  {column.render
                    ? column.render(row[column.key], row)
                    : String(row[column.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {data.length === 0 && (
        <div className="py-8 text-center text-sm text-muted-foreground">
          No data available
        </div>
      )}
    </div>
  );
}
```

### Why This Works
- **Semantic HTML**: Proper `<table>`, `<thead>`, `<tbody>`, `<th>`, `<td>` (prevents AP-COMP-007)
- **Scope Attribute**: `scope="col"` for screen readers (prevents AP-A11Y-008)
- **Caption**: Optional table caption for context
- **Responsive**: Horizontal scroll on mobile (prevents AP-LAY-003)
- **Empty State**: Clear message when no data (prevents confusion)
- **Hover State**: Visual feedback on hover (if clickable)

---

## Example 2: Sortable Table

### Specification
- **Purpose**: Table with sortable columns
- **States**: Default, ascending, descending, hover
- **Accessibility**: aria-sort, button for sort control
- **Interaction**: Click column header to sort

### Code
```tsx
import { useState } from 'react';
import { ArrowUp, ArrowDown, ArrowUpDown } from 'lucide-react';
import { cn } from '@/lib/utils';

type SortDirection = 'asc' | 'desc' | null;

interface SortableColumn<T> {
  key: keyof T;
  header: string;
  sortable?: boolean;
  render?: (value: T[keyof T], row: T) => ReactNode;
}

interface SortableTableProps<T> {
  columns: SortableColumn<T>[];
  data: T[];
}

export function SortableTable<T extends { id: string | number }>({
  columns,
  data
}: SortableTableProps<T>) {
  const [sortKey, setSortKey] = useState<keyof T | null>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>(null);

  const handleSort = (key: keyof T) => {
    if (sortKey === key) {
      // Cycle: null → asc → desc → null
      if (sortDirection === null) {
        setSortDirection('asc');
      } else if (sortDirection === 'asc') {
        setSortDirection('desc');
      } else {
        setSortDirection(null);
        setSortKey(null);
      }
    } else {
      setSortKey(key);
      setSortDirection('asc');
    }
  };

  const sortedData = [...data].sort((a, b) => {
    if (!sortKey || !sortDirection) return 0;

    const aValue = a[sortKey];
    const bValue = b[sortKey];

    if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
    return 0;
  });

  const getSortIcon = (columnKey: keyof T) => {
    if (sortKey !== columnKey) {
      return <ArrowUpDown className="h-4 w-4 opacity-50" />;
    }
    if (sortDirection === 'asc') {
      return <ArrowUp className="h-4 w-4" />;
    }
    return <ArrowDown className="h-4 w-4" />;
  };

  return (
    <div className="w-full overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b border-border">
            {columns.map((column) => (
              <th
                key={String(column.key)}
                scope="col"
                aria-sort={
                  sortKey === column.key
                    ? sortDirection === 'asc'
                      ? 'ascending'
                      : 'descending'
                    : undefined
                }
                className="px-4 py-3 text-left bg-muted/50"
              >
                {column.sortable !== false ? (
                  <button
                    type="button"
                    onClick={() => handleSort(column.key)}
                    className={cn(
                      'inline-flex items-center gap-2',
                      'text-sm font-semibold text-foreground',
                      'hover:text-primary transition-colors',
                      'focus-visible:outline-none focus-visible:ring-2',
                      'focus-visible:ring-primary focus-visible:rounded'
                    )}
                  >
                    {column.header}
                    {getSortIcon(column.key)}
                  </button>
                ) : (
                  <span className="text-sm font-semibold text-foreground">
                    {column.header}
                  </span>
                )}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {sortedData.map((row) => (
            <tr
              key={row.id}
              className="border-b border-border hover:bg-muted/50 transition-colors"
            >
              {columns.map((column) => (
                <td
                  key={String(column.key)}
                  className="px-4 py-3 text-sm text-foreground"
                >
                  {column.render
                    ? column.render(row[column.key], row)
                    : String(row[column.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### Why This Works
- **Aria-sort**: Announces sort state to screen readers (prevents AP-A11Y-008)
- **Button Control**: Sortable headers use `<button>` (prevents AP-COMP-007)
- **Visual Indicator**: Arrow icons show sort direction (prevents confusion)
- **Tri-state Sort**: null → asc → desc → null cycle (standard pattern)
- **Focus Indicator**: Visible ring on keyboard focus (prevents AP-A11Y-004)
- **Hover Feedback**: Color change on hover (prevents missing feedback)

---

## Example 3: Table with Pagination

### Specification
- **Purpose**: Table with client-side pagination
- **States**: Current page, total pages, per-page options
- **Accessibility**: Page navigation with aria-labels
- **Interaction**: Previous/Next buttons, page numbers

### Code
```tsx
import { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';

interface PaginatedTableProps<T> {
  columns: Column<T>[];
  data: T[];
  pageSize?: number;
}

export function PaginatedTable<T extends { id: string | number }>({
  columns,
  data,
  pageSize = 10
}: PaginatedTableProps<T>) {
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(data.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  const currentData = data.slice(startIndex, endIndex);

  const goToPage = (page: number) => {
    setCurrentPage(Math.max(1, Math.min(page, totalPages)));
  };

  return (
    <div className="space-y-4">
      {/* Table */}
      <div className="w-full overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-border">
              {columns.map((column) => (
                <th
                  key={String(column.key)}
                  scope="col"
                  className="px-4 py-3 text-left text-sm font-semibold text-foreground bg-muted/50"
                >
                  {column.header}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {currentData.map((row) => (
              <tr
                key={row.id}
                className="border-b border-border hover:bg-muted/50 transition-colors"
              >
                {columns.map((column) => (
                  <td
                    key={String(column.key)}
                    className="px-4 py-3 text-sm text-foreground"
                  >
                    {column.render
                      ? column.render(row[column.key], row)
                      : String(row[column.key])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination Controls */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          Showing {startIndex + 1} to {Math.min(endIndex, data.length)} of{' '}
          {data.length} results
        </p>

        <nav aria-label="Pagination" className="flex items-center gap-1">
          <button
            type="button"
            onClick={() => goToPage(currentPage - 1)}
            disabled={currentPage === 1}
            aria-label="Go to previous page"
            className={cn(
              'inline-flex items-center justify-center',
              'h-9 w-9 rounded-md',
              'text-sm font-medium',
              'border border-input bg-background',
              'hover:bg-accent hover:text-accent-foreground',
              'focus-visible:outline-none focus-visible:ring-2',
              'focus-visible:ring-primary',
              'disabled:opacity-50 disabled:pointer-events-none'
            )}
          >
            <ChevronLeft className="h-4 w-4" />
          </button>

          {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => {
            const isCurrent = page === currentPage;
            return (
              <button
                key={page}
                type="button"
                onClick={() => goToPage(page)}
                aria-label={`Go to page ${page}`}
                aria-current={isCurrent ? 'page' : undefined}
                className={cn(
                  'inline-flex items-center justify-center',
                  'h-9 w-9 rounded-md',
                  'text-sm font-medium',
                  'focus-visible:outline-none focus-visible:ring-2',
                  'focus-visible:ring-primary',
                  isCurrent
                    ? 'bg-primary text-primary-foreground'
                    : 'border border-input bg-background hover:bg-accent hover:text-accent-foreground'
                )}
              >
                {page}
              </button>
            );
          })}

          <button
            type="button"
            onClick={() => goToPage(currentPage + 1)}
            disabled={currentPage === totalPages}
            aria-label="Go to next page"
            className={cn(
              'inline-flex items-center justify-center',
              'h-9 w-9 rounded-md',
              'text-sm font-medium',
              'border border-input bg-background',
              'hover:bg-accent hover:text-accent-foreground',
              'focus-visible:outline-none focus-visible:ring-2',
              'focus-visible:ring-primary',
              'disabled:opacity-50 disabled:pointer-events-none'
            )}
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </nav>
      </div>
    </div>
  );
}
```

### Why This Works
- **Results Summary**: Shows current range (prevents confusion)
- **Aria-labels**: Clear labels for navigation buttons (prevents AP-A11Y-003)
- **Aria-current**: Marks current page (prevents AP-A11Y-008)
- **Disabled State**: Previous/Next disabled at boundaries (prevents invalid actions)
- **Touch Targets**: 36×36px buttons (acceptable for dense UI)
- **Token Colors**: Uses semantic tokens (prevents AP-VIS-001)

---

## Example 4: Table with Row Selection

### Specification
- **Purpose**: Table with checkbox selection
- **States**: None selected, some selected, all selected
- **Accessibility**: Select all checkbox, individual checkboxes
- **Interaction**: Click row to select, checkbox for bulk actions

### Code
```tsx
import { useState } from 'react';
import { cn } from '@/lib/utils';

interface SelectableTableProps<T> {
  columns: Column<T>[];
  data: T[];
  onSelectionChange?: (selectedIds: Set<string | number>) => void;
}

export function SelectableTable<T extends { id: string | number }>({
  columns,
  data,
  onSelectionChange
}: SelectableTableProps<T>) {
  const [selectedIds, setSelectedIds] = useState<Set<string | number>>(new Set());

  const allIds = data.map((row) => row.id);
  const isAllSelected = allIds.length > 0 && allIds.every((id) => selectedIds.has(id));
  const isSomeSelected = allIds.some((id) => selectedIds.has(id)) && !isAllSelected;

  const toggleAll = () => {
    if (isAllSelected) {
      setSelectedIds(new Set());
      onSelectionChange?.(new Set());
    } else {
      const newSelection = new Set(allIds);
      setSelectedIds(newSelection);
      onSelectionChange?.(newSelection);
    }
  };

  const toggleRow = (id: string | number) => {
    const newSelection = new Set(selectedIds);
    if (newSelection.has(id)) {
      newSelection.delete(id);
    } else {
      newSelection.add(id);
    }
    setSelectedIds(newSelection);
    onSelectionChange?.(newSelection);
  };

  return (
    <div className="w-full overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b border-border">
            <th scope="col" className="w-12 px-4 py-3 bg-muted/50">
              <input
                type="checkbox"
                checked={isAllSelected}
                ref={(el) => {
                  if (el) el.indeterminate = isSomeSelected;
                }}
                onChange={toggleAll}
                aria-label="Select all rows"
                className={cn(
                  'h-4 w-4 rounded',
                  'border-2 border-input',
                  'text-primary',
                  'focus:ring-2 focus:ring-primary focus:ring-offset-2'
                )}
              />
            </th>
            {columns.map((column) => (
              <th
                key={String(column.key)}
                scope="col"
                className="px-4 py-3 text-left text-sm font-semibold text-foreground bg-muted/50"
              >
                {column.header}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map((row) => {
            const isSelected = selectedIds.has(row.id);
            return (
              <tr
                key={row.id}
                onClick={() => toggleRow(row.id)}
                className={cn(
                  'border-b border-border cursor-pointer',
                  'transition-colors',
                  isSelected ? 'bg-accent' : 'hover:bg-muted/50'
                )}
              >
                <td className="w-12 px-4 py-3">
                  <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={() => toggleRow(row.id)}
                    aria-label={`Select row ${row.id}`}
                    onClick={(e) => e.stopPropagation()}
                    className={cn(
                      'h-4 w-4 rounded',
                      'border-2 border-input',
                      'text-primary',
                      'focus:ring-2 focus:ring-primary focus:ring-offset-2'
                    )}
                  />
                </td>
                {columns.map((column) => (
                  <td
                    key={String(column.key)}
                    className="px-4 py-3 text-sm text-foreground"
                  >
                    {column.render
                      ? column.render(row[column.key], row)
                      : String(row[column.key])}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>

      {selectedIds.size > 0 && (
        <div className="mt-4 text-sm text-foreground">
          {selectedIds.size} row(s) selected
        </div>
      )}
    </div>
  );
}
```

### Why This Works
- **Indeterminate State**: Shows partial selection (standard pattern)
- **Aria-labels**: Checkboxes have clear labels (prevents AP-A11Y-008)
- **Row Click**: Entire row clickable for selection (better UX)
- **Visual Feedback**: Selected rows have background color (prevents confusion)
- **Selection Count**: Shows number of selected rows (transparency)
- **Focus Rings**: Visible on checkboxes (prevents AP-A11Y-004)

---

## Example 5: Responsive Data Table (Card View on Mobile)

### Specification
- **Purpose**: Table that adapts to mobile as cards
- **States**: Table view (desktop), card view (mobile)
- **Accessibility**: Maintains semantic structure in both views
- **Layout**: Breakpoint-based responsive design

### Code
```tsx
import { cn } from '@/lib/utils';

interface ResponsiveTableProps<T> {
  columns: Column<T>[];
  data: T[];
}

export function ResponsiveTable<T extends { id: string | number }>({
  columns,
  data
}: ResponsiveTableProps<T>) {
  return (
    <>
      {/* Desktop Table View */}
      <div className="hidden md:block w-full overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-border">
              {columns.map((column) => (
                <th
                  key={String(column.key)}
                  scope="col"
                  className="px-4 py-3 text-left text-sm font-semibold text-foreground bg-muted/50"
                >
                  {column.header}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {data.map((row) => (
              <tr
                key={row.id}
                className="border-b border-border hover:bg-muted/50 transition-colors"
              >
                {columns.map((column) => (
                  <td
                    key={String(column.key)}
                    className="px-4 py-3 text-sm text-foreground"
                  >
                    {column.render
                      ? column.render(row[column.key], row)
                      : String(row[column.key])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile Card View */}
      <div className="md:hidden space-y-4">
        {data.map((row) => (
          <div
            key={row.id}
            className={cn(
              'rounded-lg border border-border',
              'bg-card p-4 space-y-3',
              'shadow-sm'
            )}
          >
            {columns.map((column) => (
              <div key={String(column.key)} className="flex justify-between">
                <dt className="text-sm font-medium text-muted-foreground">
                  {column.header}
                </dt>
                <dd className="text-sm font-medium text-foreground text-right">
                  {column.render
                    ? column.render(row[column.key], row)
                    : String(row[column.key])}
                </dd>
              </div>
            ))}
          </div>
        ))}
      </div>
    </>
  );
}
```

### Why This Works
- **Breakpoint Strategy**: md: breakpoint switches views (prevents AP-LAY-003)
- **Semantic Cards**: Uses dl/dt/dd for key-value pairs (prevents AP-COMP-007)
- **No Horizontal Scroll on Mobile**: Cards stack vertically (better UX)
- **Touch-Friendly**: Card padding provides touch targets (prevents AP-A11Y-002)
- **Visual Hierarchy**: Bold headers, aligned values (prevents confusion)

---

## Common Anti-Patterns to Avoid

- ❌ Using `<div>` instead of `<table>` (AP-COMP-007)
- ❌ Missing `scope` attribute on `<th>` (AP-A11Y-008)
- ❌ Sortable headers without aria-sort (AP-A11Y-008)
- ❌ Pagination without aria-labels (AP-A11Y-003)
- ❌ Checkboxes without labels (AP-A11Y-008)
- ❌ No empty state message (confusing UX)
- ❌ Fixed width tables on mobile (AP-LAY-001)
- ❌ No hover feedback on interactive rows

## Accessibility Checklist

- ✓ Semantic table elements (`<table>`, `<thead>`, `<tbody>`, `<th>`, `<td>`)
- ✓ `scope="col"` on column headers
- ✓ `<caption>` for table description
- ✓ aria-sort on sortable columns
- ✓ aria-label on action buttons
- ✓ aria-current on current page
- ✓ Checkboxes have associated labels
- ✓ Focus indicators visible
- ✓ Responsive design (horizontal scroll or card view)
- ✓ Empty state handling

---

**Version:** v0.2.0
**Last Updated:** 2026-01-10

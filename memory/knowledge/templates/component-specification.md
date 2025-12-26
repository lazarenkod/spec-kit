# Component Specification Template

> **Purpose**: Define design system component requirements, API, behavior, and accessibility.
> **When to Use**: Before implementing a new shared UI component.
> **Audience**: Designers, developers, consumers of the design system.

---

## Component Metadata

| Field | Value |
|-------|-------|
| **Component Name** | [ComponentName] |
| **Category** | [Atom | Molecule | Organism | Template] |
| **Status** | [Draft | In Review | Stable | Deprecated] |
| **Version** | [X.Y.Z] (semver) |
| **Owner** | [Design System Team / Name] |
| **Created** | [YYYY-MM-DD] |
| **Last Updated** | [YYYY-MM-DD] |
| **Figma Link** | [Link to Figma component] |
| **Storybook Link** | [Link to Storybook] |

---

## 1. Overview

### Description
[1-2 sentences describing what this component is and its primary purpose]

### When to Use
- ✅ [Use case 1]
- ✅ [Use case 2]
- ✅ [Use case 3]

### When NOT to Use
- ❌ [Anti-use case 1] → Use [Alternative] instead
- ❌ [Anti-use case 2] → Use [Alternative] instead

### Related Components
| Component | Relationship |
|-----------|--------------|
| [Component A] | Parent / Contains this |
| [Component B] | Sibling / Often used together |
| [Component C] | Alternative for [use case] |

---

## 2. Anatomy

### Visual Structure

```
┌─────────────────────────────────────────────┐
│ ┌─────────┐                      ┌────────┐ │
│ │  Icon   │  Label Text          │ Action │ │
│ │ (slot)  │  Helper text         │ (slot) │ │
│ └─────────┘                      └────────┘ │
│                                             │
│  [Content Area / Children]                  │
│                                             │
└─────────────────────────────────────────────┘
     └── Container (padding, border, bg)
```

### Slots / Composition Points

| Slot | Required | Type | Description |
|------|----------|------|-------------|
| `children` | Yes | ReactNode | Main content area |
| `icon` | No | ReactNode | Leading icon or graphic |
| `action` | No | ReactNode | Trailing action (button, icon) |

### Sub-Components (if compound)

| Sub-Component | Purpose | Required |
|---------------|---------|----------|
| `Component.Header` | Header section | No |
| `Component.Body` | Main content | Yes |
| `Component.Footer` | Footer with actions | No |

---

## 3. Props / API

### Core Props

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'ghost'` | `'primary'` | No | Visual variant |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | No | Component size |
| `disabled` | `boolean` | `false` | No | Disable interaction |
| `loading` | `boolean` | `false` | No | Show loading state |
| `children` | `ReactNode` | - | Yes | Content |

### Event Props

| Prop | Type | Description |
|------|------|-------------|
| `onClick` | `(event: MouseEvent) => void` | Click handler |
| `onFocus` | `(event: FocusEvent) => void` | Focus handler |
| `onBlur` | `(event: FocusEvent) => void` | Blur handler |

### Accessibility Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `aria-label` | `string` | - | Accessible label (required if no visible text) |
| `aria-describedby` | `string` | - | ID of descriptive element |
| `role` | `string` | `'button'` | ARIA role (if non-semantic element) |

### Styling Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | - | Additional CSS classes |
| `style` | `CSSProperties` | - | Inline styles (discouraged) |
| `data-testid` | `string` | - | Test automation selector |

---

## 4. Variants

### Visual Variants

| Variant | Use Case | Visual |
|---------|----------|--------|
| `primary` | Primary actions, CTAs | Solid background, brand color |
| `secondary` | Secondary actions | Outlined, neutral |
| `ghost` | Tertiary, in dense UIs | No background, text only |
| `danger` | Destructive actions | Red/warning color |

### Size Variants

| Size | Height | Padding | Font Size | Icon Size | Use Case |
|------|--------|---------|-----------|-----------|----------|
| `sm` | 32px | 8px 12px | 14px | 16px | Dense UIs, tables |
| `md` | 40px | 12px 16px | 16px | 20px | Default, forms |
| `lg` | 48px | 16px 24px | 18px | 24px | Hero sections, mobile |

### State Variations

| State | Description | Visual Changes |
|-------|-------------|----------------|
| Default | Normal state | Base styles |
| Hover | Mouse over | Background lightens/darkens |
| Focus | Keyboard focus | Focus ring visible |
| Active | Being clicked | Slightly pressed effect |
| Disabled | Non-interactive | Reduced opacity, no pointer |
| Loading | Async operation | Spinner, disabled interactions |

---

## 5. Behavior

### Interactions

| Trigger | Behavior |
|---------|----------|
| Click | [What happens on click] |
| Enter/Space key | [Same as click] |
| Escape | [If applicable, close/cancel] |
| Tab | [Focus management] |

### State Management

**Internal State**:
| State | Type | Description |
|-------|------|-------------|
| `isHovered` | boolean | Tracks hover for styling |
| `isFocused` | boolean | Tracks focus for styling |

**Controlled vs Uncontrolled**:
```tsx
// Uncontrolled (internal state)
<Component defaultValue="initial" />

// Controlled (external state)
<Component value={value} onChange={setValue} />
```

### Loading Behavior
- Shows spinner in place of [icon/content]
- Disables interactions while loading
- Maintains original dimensions (no layout shift)

### Error Handling
- Invalid props: [Console warning in dev]
- Missing required children: [Render nothing / placeholder]

---

## 6. Design Tokens

### Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `component-padding-x` | `var(--space-4)` | Horizontal padding |
| `component-padding-y` | `var(--space-3)` | Vertical padding |
| `component-gap` | `var(--space-2)` | Gap between internal elements |

### Colors

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| `component-bg` | `var(--color-primary-500)` | `var(--color-primary-400)` | Background |
| `component-bg-hover` | `var(--color-primary-600)` | `var(--color-primary-300)` | Hover state |
| `component-text` | `var(--color-white)` | `var(--color-white)` | Text color |
| `component-border` | `transparent` | `transparent` | Border |

### Typography

| Token | Value | Usage |
|-------|-------|-------|
| `component-font-size` | `var(--text-md)` | Label text |
| `component-font-weight` | `var(--font-medium)` | Label weight |
| `component-line-height` | `var(--leading-normal)` | Label line height |

### Effects

| Token | Value | Usage |
|-------|-------|-------|
| `component-shadow` | `var(--shadow-sm)` | Box shadow |
| `component-radius` | `var(--radius-md)` | Border radius |
| `component-transition` | `150ms ease-in-out` | State transitions |

---

## 7. Accessibility

### ARIA Requirements

| Requirement | Implementation |
|-------------|----------------|
| Role | `role="button"` (if not using `<button>`) |
| Label | `aria-label` or visible text content |
| State | `aria-disabled="true"` when disabled |
| Loading | `aria-busy="true"` when loading |

### Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Focus the component |
| `Enter` | Activate (same as click) |
| `Space` | Activate (same as click) |
| `Escape` | [If applicable] Close/cancel |

### Focus Management
- Focus ring visible on keyboard focus (not mouse)
- Focus ring: 2px offset, brand color
- Focus trapped in [if modal/popover]

### Screen Reader Behavior
```
[Icon: decorative, hidden] "Label text, button"
[Loading state] "Label text, button, loading"
[Disabled state] "Label text, button, dimmed"
```

### Color Contrast
| Foreground | Background | Ratio | WCAG Level |
|------------|------------|-------|------------|
| Text on primary | Primary bg | 4.5:1+ | AA |
| Text on secondary | Secondary bg | 4.5:1+ | AA |
| Focus ring | Any background | 3:1+ | AA |

### Motion
- Respects `prefers-reduced-motion`
- Essential animations only when reduced motion

---

## 8. Responsive Behavior

### Breakpoint Adaptations

| Breakpoint | Changes |
|------------|---------|
| Mobile (< 640px) | Full width, larger touch target |
| Tablet (640-1024px) | Standard sizing |
| Desktop (> 1024px) | Standard sizing |

### Touch Targets
- Minimum touch target: 44x44px
- Adequate spacing between adjacent targets

### Overflow Handling
- Text truncation: [ellipsis / wrap / hidden]
- Container overflow: [scroll / visible / clip]

---

## 9. Usage Examples

### Basic Usage

```tsx
import { Component } from '@design-system/react';

<Component variant="primary" size="md">
  Click me
</Component>
```

### With Icon

```tsx
<Component icon={<PlusIcon />}>
  Add item
</Component>
```

### Loading State

```tsx
<Component loading>
  Saving...
</Component>
```

### Compound Components

```tsx
<Component.Root>
  <Component.Header>
    <Component.Title>Title</Component.Title>
  </Component.Header>
  <Component.Body>
    Content goes here
  </Component.Body>
  <Component.Footer>
    <Component.Action>Save</Component.Action>
  </Component.Footer>
</Component.Root>
```

### Controlled Usage

```tsx
const [isOpen, setIsOpen] = useState(false);

<Component
  open={isOpen}
  onOpenChange={setIsOpen}
>
  Controlled content
</Component>
```

---

## 10. Do's and Don'ts

### Do ✅

```tsx
// ✅ Use semantic variant for context
<Button variant="danger">Delete account</Button>

// ✅ Provide accessible label when icon-only
<Button aria-label="Close dialog"><CloseIcon /></Button>

// ✅ Use composition for flexibility
<Card>
  <Card.Header>...</Card.Header>
  <Card.Body>...</Card.Body>
</Card>
```

### Don't ❌

```tsx
// ❌ Don't override core styles inline
<Button style={{ backgroundColor: 'red' }}>Bad</Button>

// ❌ Don't use for navigation (use Link)
<Button onClick={() => router.push('/page')}>Go</Button>

// ❌ Don't nest interactive elements
<Button><a href="#">Nested link</a></Button>

// ❌ Don't disable without explanation
<Button disabled>Submit</Button>  // Why disabled?
// ✅ Better: Show validation error
```

---

## 11. Testing

### Unit Test Cases

| Test Case | Expected Behavior |
|-----------|-------------------|
| Renders with default props | Component visible, default variant/size |
| Renders all variants | Each variant has correct styling |
| Click handler fires | onClick called with event |
| Disabled state | No onClick, aria-disabled, visual change |
| Loading state | Spinner visible, interactions disabled |
| Keyboard activation | Enter/Space trigger onClick |

### Accessibility Tests

```tsx
// axe-core integration
it('has no accessibility violations', async () => {
  const { container } = render(<Component>Test</Component>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

// Focus management
it('is focusable', () => {
  render(<Component>Test</Component>);
  userEvent.tab();
  expect(screen.getByRole('button')).toHaveFocus();
});
```

### Visual Regression Tests
- [ ] Default state
- [ ] Hover state
- [ ] Focus state
- [ ] Active state
- [ ] Disabled state
- [ ] Loading state
- [ ] All variants
- [ ] All sizes
- [ ] Dark mode
- [ ] RTL layout

---

## 12. Migration Guide

### From Previous Version

**v1.x → v2.x**

| Change | v1.x | v2.x | Codemod |
|--------|------|------|---------|
| Prop rename | `type` | `variant` | Available |
| API change | `onClick` | `onPress` | Available |
| Removal | `fluid` prop | Use `className="w-full"` | Manual |

```bash
# Run codemod
npx @design-system/codemod component-v2 ./src
```

### Breaking Changes
- `type` prop renamed to `variant`
- `fluid` prop removed (use className)
- Minimum React version: 18

---

## 13. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2024-01-15 | Added `loading` prop |
| 2.0.0 | 2024-01-01 | Breaking: renamed `type` to `variant` |
| 1.2.0 | 2023-12-01 | Added `ghost` variant |
| 1.1.0 | 2023-11-15 | Added `size` prop |
| 1.0.0 | 2023-11-01 | Initial release |

---

## Appendix

### A. Figma Component Structure

```
Component/
├── .Base (hidden)
├── Primary/
│   ├── Small
│   ├── Medium
│   └── Large
├── Secondary/
│   ├── Small
│   ├── Medium
│   └── Large
└── Ghost/
    ├── Small
    ├── Medium
    └── Large
```

### B. CSS Custom Properties

```css
.component {
  /* Spacing */
  --component-padding-x: var(--space-4);
  --component-padding-y: var(--space-3);

  /* Colors */
  --component-bg: var(--color-primary-500);
  --component-text: var(--color-white);

  /* Typography */
  --component-font-size: var(--text-md);

  /* Effects */
  --component-radius: var(--radius-md);
  --component-transition: 150ms ease-in-out;
}
```

### C. Implementation Checklist

- [ ] Props interface defined
- [ ] All variants implemented
- [ ] All sizes implemented
- [ ] States (hover, focus, active, disabled)
- [ ] Loading state
- [ ] Keyboard navigation
- [ ] ARIA attributes
- [ ] Screen reader testing
- [ ] Color contrast verification
- [ ] Reduced motion support
- [ ] RTL support
- [ ] Unit tests
- [ ] Accessibility tests
- [ ] Visual regression tests
- [ ] Storybook documentation
- [ ] Migration guide (if updating)

---

# Component Spec Quality Checklist

## Design
- [ ] Anatomy diagram provided
- [ ] All variants documented
- [ ] Design tokens specified
- [ ] Figma link included

## API
- [ ] All props documented with types
- [ ] Defaults specified
- [ ] Event handlers documented
- [ ] Compound component API (if applicable)

## Accessibility
- [ ] ARIA requirements listed
- [ ] Keyboard navigation documented
- [ ] Focus management specified
- [ ] Color contrast verified
- [ ] Screen reader behavior documented

## Developer Experience
- [ ] Usage examples provided
- [ ] Do's and Don'ts clear
- [ ] Migration guide (for updates)
- [ ] Test cases listed

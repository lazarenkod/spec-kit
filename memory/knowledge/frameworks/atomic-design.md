# Atomic Design Methodology Guide

## Overview

Atomic Design is a methodology for creating design systems, introduced by Brad Frost in 2013. It provides a mental model for thinking about UI design in a hierarchical, systematic way — from the smallest elements to complete pages.

**Core Idea**: UI components can be broken down into five distinct levels, like chemistry's atoms combining to form molecules and organisms.

## The Five Levels

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   Level 1          Level 2          Level 3          Level 4          │
│   ATOMS            MOLECULES        ORGANISMS        TEMPLATES         │
│                                                                         │
│   ● Button         ┌────────────┐   ┌─────────────┐  ┌─────────────┐   │
│   ● Input          │ 🔍 Search  │   │   HEADER    │  │ ░░░░░░░░░░░ │   │
│   ● Label          └────────────┘   │ Logo Nav    │  │ ░░░ ░░░░░░ │   │
│   ● Icon                            └─────────────┘  │ ░░░░░░░░░░░ │   │
│   ● Color          Search Field     Header           │ ░░░ ░░░░░░ │   │
│                    = Icon + Input   = Logo + Nav     └─────────────┘   │
│                                     + Search         Layout Structure   │
│                                                                         │
│   Level 5                                                               │
│   PAGES                                                                 │
│   ┌─────────────┐                                                       │
│   │ ACME Corp   │  ← Real content                                       │
│   │ Welcome!    │  ← Real data                                          │
│   │ Products... │  ← Live state                                         │
│   └─────────────┘                                                       │
│   Home Page                                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Level 1: Atoms

**Definition**: The basic building blocks of UI — HTML elements that can't be broken down further without losing meaning.

**Characteristics**:
- Standalone, no dependencies on other components
- Foundational UI elements
- Often map directly to HTML elements

**Examples**:
| Atom | HTML Element | Purpose |
|------|--------------|---------|
| Button | `<button>` | Trigger actions |
| Input | `<input>` | Accept user input |
| Label | `<label>` | Describe form fields |
| Icon | `<svg>` | Visual indicator |
| Image | `<img>` | Visual content |
| Heading | `<h1>`-`<h6>` | Section titles |
| Paragraph | `<p>` | Body text |
| Link | `<a>` | Navigation |

**Atom Specification Template**:
```markdown
## Atom: Button

### Variants
| Variant | Use Case |
|---------|----------|
| Primary | Main actions |
| Secondary | Alternative actions |
| Ghost | Subtle actions |
| Danger | Destructive actions |

### Sizes
- Small (32px height)
- Medium (40px height)
- Large (48px height)

### States
- Default
- Hover
- Active
- Focused
- Disabled
- Loading

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | string | 'primary' | Visual style |
| size | string | 'medium' | Size variant |
| disabled | boolean | false | Disabled state |
```

---

## Level 2: Molecules

**Definition**: Simple groups of atoms functioning together as a unit.

**Characteristics**:
- Combine atoms into functional groups
- Have a single responsibility
- Reusable across contexts

**Examples**:
| Molecule | Atoms Combined | Purpose |
|----------|----------------|---------|
| Search Field | Input + Button + Icon | User search |
| Form Field | Label + Input + Helper text | Data entry |
| Card Header | Avatar + Name + Timestamp | User info |
| Navigation Item | Icon + Label | Menu item |
| Badge | Text + Background | Status indicator |

**Molecule Example: Search Field**
```text
┌─────────────────────────────────────────────────┐
│ 🔍  │  Search products...          │  [Search] │
│ Icon│       Input                  │   Button  │
└─────────────────────────────────────────────────┘
       └──────────── Molecule ───────────────┘
```

**Molecule Specification Template**:
```markdown
## Molecule: Search Field

### Composition
- Icon (atom) — Search indicator
- Input (atom) — Text entry
- Button (atom) — Submit action

### Variants
| Variant | Description |
|---------|-------------|
| Default | Full search field |
| Compact | Icon-only, expands on focus |
| Inline | No button, submits on Enter |

### Props
| Prop | Type | Description |
|------|------|-------------|
| placeholder | string | Input placeholder |
| onSearch | function | Search callback |
| loading | boolean | Show loading state |

### Behavior
- Focus on input highlights field
- Enter key triggers search
- Clear button appears when text present
```

---

## Level 3: Organisms

**Definition**: Complex UI components composed of molecules and/or atoms, forming distinct sections of an interface.

**Characteristics**:
- Self-contained, meaningful sections
- Can function independently
- Often map to content sections

**Examples**:
| Organism | Components | Purpose |
|----------|------------|---------|
| Header | Logo + Navigation + Search + User Menu | Site navigation |
| Product Card | Image + Title + Price + Actions | Product display |
| Comment | Avatar + Author + Content + Actions | User comment |
| Footer | Links + Logo + Social + Legal | Site footer |
| Sidebar | Navigation + User Info + Actions | Dashboard nav |

**Organism Example: Header**
```text
┌─────────────────────────────────────────────────────────────────────┐
│  ┌──────┐    ┌─────────────────────────┐   ┌────────────────────┐   │
│  │ Logo │    │  Products  About  Blog  │   │ 🔍 Search...   ●   │   │
│  └──────┘    └─────────────────────────┘   └────────────────────┘   │
│   Atom              Navigation               Search   Avatar        │
│                     (Molecule)               (Molecule) (Atom)      │
│                                                                     │
│  └────────────────────── HEADER ORGANISM ─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**Organism Specification Template**:
```markdown
## Organism: Header

### Composition
- Logo (atom)
- Navigation (molecule)
- Search Field (molecule)
- User Menu (molecule)

### Variants
| Variant | Description |
|---------|-------------|
| Default | Full header with all components |
| Minimal | Logo + hamburger menu |
| Transparent | Overlay on hero images |

### Responsive Behavior
| Breakpoint | Behavior |
|------------|----------|
| Desktop (>1024px) | Full horizontal layout |
| Tablet (768-1024px) | Condensed nav, search in menu |
| Mobile (<768px) | Hamburger menu, search hidden |

### States
- Default (not scrolled)
- Scrolled (sticky, condensed)
- Menu open (mobile)
```

---

## Level 4: Templates

**Definition**: Page-level layouts that place organisms and molecules in a content structure — the skeleton of a page.

**Characteristics**:
- Define page structure and layout
- Use placeholder content
- Focus on layout, not content
- Reusable across pages

**Examples**:
| Template | Structure | Pages Using It |
|----------|-----------|----------------|
| Dashboard Layout | Header + Sidebar + Content | Dashboard, Settings |
| Marketing Layout | Header + Hero + Content + Footer | Home, About, Pricing |
| Auth Layout | Centered card | Login, Register, Reset |
| Article Layout | Header + Content + Related | Blog posts, Docs |

**Template Example: Dashboard**
```text
┌─────────────────────────────────────────────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░ HEADER ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
├──────────────┬──────────────────────────────────────────────────────┤
│              │                                                      │
│   ░░░░░░░░   │   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│   SIDEBAR    │                                                      │
│   ░░░░░░░░   │   ░░░░░░░░░░░░ MAIN CONTENT ░░░░░░░░░░░░░░░░░░░░░   │
│   ░░░░░░░░   │                                                      │
│   ░░░░░░░░   │   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│   ░░░░░░░░   │                                                      │
│              │                                                      │
└──────────────┴──────────────────────────────────────────────────────┘
```

**Template Specification**:
```markdown
## Template: Dashboard Layout

### Grid Structure
- Header: Full width, fixed height (64px)
- Sidebar: 240px width, collapsible to 64px
- Content: Flexible, scrollable

### Slots
| Slot | Expected Content |
|------|------------------|
| header | Header organism |
| sidebar | Sidebar organism |
| content | Page-specific content |

### Responsive Behavior
| Breakpoint | Sidebar | Content |
|------------|---------|---------|
| Desktop | Visible, 240px | Full |
| Tablet | Collapsed, 64px | Full |
| Mobile | Hidden, overlay | Full |
```

---

## Level 5: Pages

**Definition**: Specific instances of templates with real content — what users actually see.

**Characteristics**:
- Templates populated with real data
- Handle dynamic content and states
- Test edge cases and variations
- Final output for users

**Examples**:
| Page | Template | Real Content |
|------|----------|--------------|
| Home | Marketing | Company headline, CTA |
| User Dashboard | Dashboard | User's actual data |
| Product Details | Product | Specific product info |
| Empty State | Dashboard | No data state |

**Page Variations to Test**:
| Variation | Purpose |
|-----------|---------|
| Default | Normal content, happy path |
| Empty State | No data yet |
| Error State | Something went wrong |
| Loading State | Content loading |
| Maximum Content | Long text, many items |
| Minimum Content | Sparse data |
| Localized | Different language |
| Authenticated | Logged in user |
| Guest | Not logged in |

---

## Implementation Guide

### Folder Structure

```text
src/
├── atoms/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   ├── Button.stories.tsx
│   │   └── Button.module.css
│   ├── Input/
│   ├── Icon/
│   └── ...
├── molecules/
│   ├── SearchField/
│   ├── FormField/
│   └── ...
├── organisms/
│   ├── Header/
│   ├── ProductCard/
│   └── ...
├── templates/
│   ├── DashboardLayout/
│   ├── MarketingLayout/
│   └── ...
└── pages/
    ├── Home/
    ├── Dashboard/
    └── ...
```

### Component Documentation

Each component should include:
1. **Props documentation** — API reference
2. **Storybook stories** — Visual examples
3. **Usage examples** — Code snippets
4. **Accessibility notes** — A11y considerations
5. **Design tokens** — Styling variables

### Naming Conventions

| Level | Naming Pattern | Example |
|-------|----------------|---------|
| Atom | Simple noun | `Button`, `Input`, `Icon` |
| Molecule | Noun phrase | `SearchField`, `FormGroup` |
| Organism | Section name | `Header`, `ProductCard` |
| Template | Layout + Layout | `DashboardLayout`, `AuthLayout` |
| Page | Page name | `HomePage`, `SettingsPage` |

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Component soup | Too many small atoms | Consolidate related atoms |
| Mega-organisms | Organisms too large | Split into smaller organisms |
| Template confusion | Templates have real content | Keep templates content-agnostic |
| Skip levels | Jump from atoms to organisms | Include molecules for reusability |
| Rigid hierarchy | Everything must fit exactly | Allow flexibility in classification |
| Over-atomization | Button variants as atoms | Use props for variants |

---

## Relationship to Design Tokens

```text
Design Tokens                    Atomic Design
(the ingredients)                (the recipes)

┌─────────────────┐              ┌─────────────────┐
│ Colors          │              │ Atoms           │
│ Typography      │──────────────│ (use tokens)    │
│ Spacing         │              │                 │
│ Shadows         │              │ Molecules       │
│ Border radius   │              │ (compose atoms) │
└─────────────────┘              │                 │
                                 │ Organisms       │
                                 │ (compose all)   │
                                 └─────────────────┘
```

**Integration**:
- Atoms consume design tokens directly
- Molecules inherit tokens through atoms
- Organisms assemble the whole

---

## Atomic Design + Storybook

### Story Organization

```text
Components/
├── Atoms/
│   ├── Button
│   ├── Input
│   └── Icon
├── Molecules/
│   ├── SearchField
│   └── FormField
├── Organisms/
│   ├── Header
│   └── Footer
├── Templates/
│   └── DashboardLayout
└── Pages/
    └── Dashboard
```

### Story Template

```tsx
// Button.stories.tsx
import { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Atoms/Button',
  component: Button,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Click me',
  },
};

export const AllVariants: Story = {
  render: () => (
    <>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
    </>
  ),
};
```

---

## Resources

- **Book**: "Atomic Design" by Brad Frost (free online)
- **Website**: [atomicdesign.bradfrost.com](https://atomicdesign.bradfrost.com)
- **Pattern Lab**: Tool for building atomic design systems
- **Storybook**: Component documentation and development

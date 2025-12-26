# Design Systems Anti-Patterns Database

## Overview

This database catalogs common design system anti-patterns that undermine consistency, scalability, and developer experience. Each anti-pattern includes detection methods, consequences, root causes, and remediation strategies.

**Usage**: Reference during design system audits, component library reviews, and design-dev handoff.

---

## DS-001: Component Soup

### Description
Creating too many fine-grained components that are too small to be useful, leading to composition overhead and inconsistent usage.

### Detection Signals
- 500+ components in library
- Components for single-use cases
- Same UI achieved with different component combinations
- "Which component do I use?" confusion
- Nested imports 5+ levels deep

### Component Proliferation
```text
OVER-ATOMIZED:
<Typography>
  <Text>
    <Paragraph>
      <Body>
        <Content>Hello</Content>
      </Body>
    </Paragraph>
  </Text>
</Typography>

RIGHT-SIZED:
<Text variant="body">Hello</Text>
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Atomic design misapplied | "Everything must be an atom" |
| Premature abstraction | "We might need this separately" |
| Reuse obsession | "Don't repeat anything" |
| Designer-developer gap | Each variant becomes component |
| No governance | Anyone can add components |

### Consequences
| Impact | Description |
|--------|-------------|
| Discovery overwhelm | Can't find right component |
| Inconsistent composition | Same UI, different approach |
| Maintenance burden | Many small components to update |
| Performance | Many small bundles to load |
| Onboarding difficulty | Too much to learn |

### Remediation

**Component Right-Sizing**:
```text
ASK BEFORE CREATING:
1. Will this be used 3+ times?
2. Does it encapsulate meaningful behavior?
3. Can an existing component's prop do this?
4. Is this composition vs component confusion?

CONSOLIDATE WHEN:
- Component has single consumer
- Component is always used with specific parent
- Props would simplify multiple components
```

**Variant vs Component Decision**:
```text
COMPONENT:
├── Different DOM structure
├── Different behavior
├── Different state management
└── Semantically distinct

VARIANT (use props):
├── Different styling
├── Different sizes
├── Different colors
└── Same core behavior

EXAMPLE:
Button (component)
├── variant="primary" (prop)
├── variant="secondary" (prop)
├── size="small" (prop)
└── size="large" (prop)

NOT:
PrimaryButton, SecondaryButton,
SmallButton, LargeButton (❌ component per variant)
```

### Prevention Checklist
- [ ] Component governance process exists
- [ ] New components require 3+ use cases
- [ ] Props preferred over new components
- [ ] Regular component audit/consolidation

---

## DS-002: Prop Explosion

### Description
Components with too many props (20+) that are hard to understand, use, and maintain. The opposite of component soup — too much in one component.

### Detection Signals
- Component has 30+ props
- TypeScript interface spans multiple screens
- "What does this prop do?" common question
- Boolean prop combinations create invalid states
- Documentation is overwhelming

### Prop Explosion Example
```typescript
// ❌ TOO MANY PROPS
<Card
  title="..."
  titleSize="large"
  titleColor="#333"
  titleBold={true}
  titleUnderline={false}
  subtitle="..."
  subtitleSize="medium"
  body="..."
  bodyAlign="left"
  image="..."
  imagePosition="top"
  imageSize="cover"
  imageBorder={true}
  cta="..."
  ctaVariant="primary"
  ctaOnClick={() => {}}
  border={true}
  borderColor="#ccc"
  borderRadius={8}
  shadow="medium"
  padding="large"
  ... // 15 more props
/>
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Configurability obsession | "Make it flexible" |
| Fear of breaking changes | "Add prop, don't change" |
| Single component bias | "One card to rule them all" |
| No composition | Props over children |
| Kitchen sink | Avoid "too many components" |

### Remediation

**Compound Component Pattern**:
```tsx
// ✅ COMPOUND COMPONENTS
<Card variant="featured">
  <Card.Image src="..." position="top" />
  <Card.Header>
    <Card.Title>Title</Card.Title>
    <Card.Subtitle>Subtitle</Card.Subtitle>
  </Card.Header>
  <Card.Body>Content...</Card.Body>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card>
```

**Prop Grouping Pattern**:
```tsx
// Instead of individual props:
<Component
  titleText="..."
  titleSize="lg"
  titleColor="primary"
/>

// Use grouped object props:
<Component
  title={{
    text: "...",
    size: "lg",
    color: "primary"
  }}
/>

// Or composition:
<Component>
  <Component.Title size="lg" color="primary">
    ...
  </Component.Title>
</Component>
```

**Prop Limit Guidelines**:
| Prop Count | Status | Action |
|------------|--------|--------|
| 1-10 | Healthy | Normal |
| 11-15 | Warning | Consider refactoring |
| 16-20 | Problem | Split or use composition |
| 20+ | Critical | Refactor required |

### Prevention Checklist
- [ ] Props count monitored per component
- [ ] Compound components for complex UI
- [ ] Composition over configuration
- [ ] Prop grouping for related options

---

## DS-003: Missing Design Tokens

### Description
Hardcoding values instead of using design tokens. Inconsistent spacing, colors, and typography that can't be updated globally.

### Detection Signals
- `color: #3B82F6` instead of `color: var(--color-primary)`
- `padding: 16px` instead of `padding: var(--spacing-4)`
- Multiple "almost the same" colors
- Theme changes require find-replace
- "What blue should I use?" confusion

### Token Debt
```css
/* ❌ HARDCODED VALUES */
.card {
  background: #ffffff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  color: #333333;
}

/* ✅ TOKENIZED */
.card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--spacing-4);
  box-shadow: var(--shadow-sm);
  color: var(--color-text-primary);
}
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| No token system | Tokens not established |
| Token discovery | "What token should I use?" |
| Speed | "Faster to hardcode" |
| Enforcement gap | No linting for tokens |
| Designer-dev gap | Design uses different values |

### Remediation

**Token Hierarchy**:
```text
LEVEL 1: PRIMITIVE TOKENS (raw values)
--color-blue-500: #3B82F6;
--spacing-4: 16px;
--font-size-lg: 18px;

LEVEL 2: SEMANTIC TOKENS (purpose)
--color-primary: var(--color-blue-500);
--spacing-component-padding: var(--spacing-4);
--font-size-heading: var(--font-size-lg);

LEVEL 3: COMPONENT TOKENS (specific use)
--button-background: var(--color-primary);
--card-padding: var(--spacing-component-padding);
--heading-size: var(--font-size-heading);
```

**Token Adoption Strategy**:
```text
Phase 1: Define primitive tokens
         └── Colors, spacing, typography scale

Phase 2: Create semantic tokens
         └── Map primitives to purposes

Phase 3: Audit existing code
         └── Find hardcoded values

Phase 4: Migrate to tokens
         └── Replace hardcoded with tokens

Phase 5: Enforce with linting
         └── Block hardcoded values in PRs
```

**Token Enforcement**:
```javascript
// Stylelint rule
{
  "rules": {
    "color-no-hex": true,
    "declaration-property-value-disallowed-list": {
      "padding": ["/^\\d/"],
      "margin": ["/^\\d/"],
      "font-size": ["/^\\d/"]
    }
  }
}
```

### Prevention Checklist
- [ ] Token system documented
- [ ] Semantic tokens cover all use cases
- [ ] Linting enforces token usage
- [ ] Figma tokens sync with code

---

## DS-004: Inconsistent API

### Description
Component APIs that are inconsistent across the system. Same concept, different prop names. Same prop, different behavior.

### Detection Signals
- `onClick` vs `onPress` vs `handleClick`
- `variant` vs `type` vs `kind`
- `size="sm"` vs `size="small"` vs `small={true}`
- Boolean props sometimes inverted
- Different default values

### API Inconsistency Examples
```tsx
// ❌ INCONSISTENT
<Button size="sm" />
<Input size="small" />
<Card sizing="compact" />

<Button onClick={() => {}} />
<Link onPress={() => {}} />
<IconButton handleClick={() => {}} />

<Button disabled />
<Input isDisabled />
<Select enabled={false} />
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| No API guidelines | Each developer decides |
| Multiple authors | Different people, different styles |
| Evolution | API changed over time |
| Framework mixing | React vs Angular conventions |
| Copy-paste | From different sources |

### Remediation

**API Naming Conventions**:
```text
STANDARD PROPS (always use these names):
├── Events: onClick, onChange, onFocus, onBlur
├── State: disabled, loading, selected, expanded
├── Content: children, label, title, description
├── Styling: className, style, variant, size
├── Layout: width, height, fullWidth

SIZE SCALE:
├── xs, sm, md, lg, xl (not small, medium, large)

VARIANTS:
├── primary, secondary, tertiary, ghost, danger

BOOLEAN PROPS:
├── Positive form: disabled, loading, selected
├── Not: isDisabled, notEnabled, active={false}
```

**Component API Template**:
```typescript
// Standard component interface
interface ComponentProps {
  // Content
  children?: React.ReactNode;
  label?: string;

  // Variants
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';

  // State
  disabled?: boolean;
  loading?: boolean;

  // Events
  onClick?: () => void;
  onChange?: (value: T) => void;

  // Styling
  className?: string;
  style?: React.CSSProperties;

  // Accessibility
  'aria-label'?: string;
}
```

**API Audit Template**:
```markdown
## Component: [Name]

### Events
| Prop | Standard | Status |
|------|----------|--------|
| onClick | onClick | ✅ |
| onPress | onClick | ❌ Rename |

### Variants
| Prop | Standard | Status |
|------|----------|--------|
| type="primary" | variant="primary" | ❌ Rename |

### Sizes
| Prop | Standard | Status |
|------|----------|--------|
| size="small" | size="sm" | ❌ Rename |
```

### Prevention Checklist
- [ ] API conventions documented
- [ ] New components follow conventions
- [ ] API review in PR process
- [ ] Regular API consistency audit

---

## DS-005: No Accessibility Built-In

### Description
Components that don't include accessibility features by default, requiring consumers to add accessibility manually (which they won't).

### Detection Signals
- Components without ARIA attributes
- No keyboard navigation support
- Focus management missing
- Screen reader testing never done
- "Add your own aria-label" in docs

### Accessibility Gaps
```tsx
// ❌ INACCESSIBLE COMPONENT
<div className="modal" onClick={onClose}>
  <div className="modal-content">
    {children}
  </div>
</div>

// ✅ ACCESSIBLE COMPONENT
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby={titleId}
  aria-describedby={descriptionId}
  onKeyDown={(e) => e.key === 'Escape' && onClose()}
>
  <FocusTrap>
    <div className="modal-content">
      {children}
    </div>
  </FocusTrap>
</div>
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Knowledge gap | "Don't know accessibility" |
| Time pressure | "Add it later" |
| Testing gap | No screen reader testing |
| Invisible problem | "Works for me" |
| Bolt-on mindset | A11y as afterthought |

### Remediation

**Accessible Component Checklist**:
```text
KEYBOARD NAVIGATION:
☐ All interactive elements focusable
☐ Focus visible indicator
☐ Tab order logical
☐ Keyboard shortcuts work (Enter, Space, Escape)
☐ Arrow key navigation where expected

ARIA ATTRIBUTES:
☐ role attribute correct
☐ aria-label or aria-labelledby
☐ aria-describedby for descriptions
☐ aria-expanded, aria-selected for state
☐ aria-live for dynamic content

FOCUS MANAGEMENT:
☐ Focus trapped in modals
☐ Focus returned on close
☐ No focus loss on state changes
☐ Skip links for navigation

SCREEN READER:
☐ Tested with VoiceOver/NVDA
☐ Meaningful announcements
☐ Hidden decorative elements
☐ Logical reading order
```

**Accessible Component Patterns**:
```tsx
// Modal Pattern
function Modal({ isOpen, onClose, title, children }) {
  const titleId = useId();
  const descId = useId();

  useEffect(() => {
    if (isOpen) {
      // Return focus on close
      const previouslyFocused = document.activeElement;
      return () => previouslyFocused?.focus();
    }
  }, [isOpen]);

  return (
    <Portal>
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={descId}
      >
        <FocusTrap active={isOpen}>
          <h2 id={titleId}>{title}</h2>
          <div id={descId}>{children}</div>
          <button onClick={onClose}>Close</button>
        </FocusTrap>
      </div>
    </Portal>
  );
}
```

### Prevention Checklist
- [ ] A11y requirements in component specs
- [ ] Keyboard testing in component DoD
- [ ] Screen reader testing regular
- [ ] Automated a11y testing in CI

---

## DS-006: Documentation Debt

### Description
Component library with poor or missing documentation. Developers can't figure out how to use components, leading to misuse and workarounds.

### Detection Signals
- "How do I use this component?" in Slack
- Storybook has default stories only
- No prop documentation
- Copy-paste from other code vs docs
- Undocumented edge cases

### Documentation Gaps
```text
MINIMUM VIABLE DOCS:
├── What: Component description
├── When: Use cases
├── How: Code examples
├── Props: API reference
└── Accessibility: A11y notes

MISSING:
├── Edge cases
├── Composition patterns
├── Do/Don't examples
├── Migration guides
├── Playground/sandbox
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Time pressure | "Ship component, doc later" |
| Not valued | "Code is self-documenting" |
| Skill gap | "Don't know how to doc well" |
| No process | Docs not in DoD |
| Stale docs | Docs not updated with code |

### Remediation

**Component Documentation Template**:
```markdown
## Button

### Description
Triggers actions when clicked. Use for primary, secondary,
and destructive actions.

### When to Use
- ✅ Form submissions
- ✅ Navigation (with link styling)
- ✅ Triggering actions
- ❌ Links (use Link component)
- ❌ Toggle states (use Toggle)

### Examples

#### Basic Usage
```jsx
<Button>Click me</Button>
```

#### Variants
```jsx
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="danger">Delete</Button>
```

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | string | "primary" | Visual style |
| size | string | "md" | Button size |
| disabled | boolean | false | Disabled state |
| loading | boolean | false | Loading state |

### Accessibility
- Uses `<button>` element
- Supports keyboard activation (Enter, Space)
- Disabled state announced
- Loading state announced via aria-busy
```

**Storybook Structure**:
```text
STORIES:
├── Default.stories.tsx (basic example)
├── Variants.stories.tsx (all variants)
├── Sizes.stories.tsx (all sizes)
├── States.stories.tsx (loading, disabled)
├── Composition.stories.tsx (with icons, groups)
└── Playground.stories.tsx (interactive controls)

DOCS:
├── MDX documentation
├── Do/Don't examples
├── Accessibility notes
└── Migration guide (if breaking changes)
```

### Prevention Checklist
- [ ] Documentation in Definition of Done
- [ ] Docs reviewed with component
- [ ] Storybook stories required
- [ ] Doc updates with code changes

---

## DS-007: Breaking Changes Without Migration

### Description
Introducing breaking changes to components without version control, migration guides, or deprecation periods. Consumers break unexpectedly.

### Detection Signals
- "Component stopped working after update"
- No semantic versioning
- No deprecation warnings
- No migration guides
- All updates are major updates

### Breaking Change Impact
```text
BREAKING CHANGE WITHOUT WARNING:
v1.0.0: <Button type="primary">
v2.0.0: <Button variant="primary">  // Prop renamed!

RESULT:
- 50 consumers break
- No warning given
- Emergency rollback or mass update
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| No versioning | "It's internal" |
| Speed pressure | "Just push it" |
| Communication gap | "Didn't know it was breaking" |
| No deprecation | No warning system |
| Monorepo trap | "Everyone updates together" |

### Remediation

**Semantic Versioning for Components**:
```text
MAJOR (1.0.0 → 2.0.0):
├── Breaking prop changes
├── Removed props
├── Changed default behavior
└── Renamed/removed components

MINOR (1.0.0 → 1.1.0):
├── New components
├── New props (optional)
├── New variants
└── Backward-compatible features

PATCH (1.0.0 → 1.0.1):
├── Bug fixes
├── Performance improvements
├── Documentation updates
└── No API changes
```

**Deprecation Strategy**:
```typescript
// Step 1: Add deprecation warning (minor version)
/** @deprecated Use `variant` instead. Will be removed in v3.0 */
type?: 'primary' | 'secondary';
variant?: 'primary' | 'secondary';

// In component:
if (props.type) {
  console.warn(
    'Button: `type` prop is deprecated. Use `variant` instead.'
  );
  // Map old prop to new for backward compatibility
  props.variant = props.variant ?? props.type;
}

// Step 2: Remove in major version
// Remove `type` prop, only `variant` remains
```

**Migration Guide Template**:
```markdown
## Migrating from v2 to v3

### Breaking Changes

#### Button: `type` prop renamed to `variant`

**Before (v2):**
```jsx
<Button type="primary">Click</Button>
```

**After (v3):**
```jsx
<Button variant="primary">Click</Button>
```

**Codemod:**
```bash
npx design-system-codemods button-type-to-variant src/
```

### Deprecation Removals
The following deprecated props have been removed:
- `Button.type` → Use `Button.variant`
- `Input.onTextChange` → Use `Input.onChange`
```

### Prevention Checklist
- [ ] Semantic versioning enforced
- [ ] Breaking changes require major version
- [ ] Deprecation warnings before removal
- [ ] Migration guides for major versions
- [ ] Codemods for common migrations

---

## DS-008: Style Leakage

### Description
Component styles leaking into global scope or being overridden by global styles. Styles work in isolation but break in context.

### Detection Signals
- "Component looks different in my app"
- Global CSS affecting component
- Component CSS affecting siblings
- Specificity wars (!!important)
- "Works in Storybook, not in app"

### Style Collision
```css
/* Global style */
button {
  background: red;
}

/* Component (leaked into) */
.my-button {
  background: blue; /* Overridden by global! */
}

/* Global (leaked from component) */
.card p {
  margin: 0; /* Affects ALL paragraphs in cards! */
}
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Global CSS | "We use vanilla CSS" |
| Low specificity | Component styles lose |
| Element selectors | "p {}" affects everything |
| No encapsulation | CSS has no native scoping |
| Third-party CSS | Libraries inject globals |

### Remediation

**Style Encapsulation Options**:
```text
OPTION 1: CSS Modules
.button {
  background: blue;
}
→ Compiles to: .button_abc123

OPTION 2: CSS-in-JS (Styled Components, Emotion)
const Button = styled.button`
  background: blue;
`;
→ Scoped to component

OPTION 3: BEM Convention
.card__title--highlighted {
  color: blue;
}
→ Low collision risk

OPTION 4: Shadow DOM (Web Components)
<custom-button>
  #shadow-root
    <button>Click</button>
  </shadow-root>
</custom-button>
→ True encapsulation
```

**CSS Reset Strategy**:
```css
/* Component reset - prevent inheritance */
.design-system-button {
  /* Reset ALL properties that could be inherited */
  all: initial;
  /* Then set intentional styles */
  font-family: var(--font-family);
  color: var(--color-text);
  /* ... */
}
```

**Specificity Management**:
```css
/* ❌ TOO WEAK */
button { }  /* 0,0,1 - easily overridden */

/* ❌ TOO STRONG */
#app button.btn.primary { }  /* 1,3,1 - hard to override */

/* ✅ JUST RIGHT */
.ds-button { }  /* 0,1,0 - component prefix */
.ds-button--primary { }  /* 0,2,0 - modifier */
```

### Prevention Checklist
- [ ] Style encapsulation method chosen
- [ ] No element selectors in components
- [ ] Component prefix for classes
- [ ] Reset inherited properties
- [ ] Testing in context, not just Storybook

---

## DS-009: Not Composable

### Description
Components that can't be combined or extended. Rigid, monolithic components that don't work well together.

### Detection Signals
- "I can't put X inside Y"
- No children prop support
- No slot/render prop patterns
- Wrapper components to hack composition
- "Component doesn't support this layout"

### Composition Failures
```tsx
// ❌ NOT COMPOSABLE
<Card
  title="Title"
  body="Body text"
  footer="Footer"
  cta="Click me"
  onCtaClick={() => {}}
/>
// Can't add icon to title, custom footer, etc.

// ✅ COMPOSABLE
<Card>
  <Card.Header>
    <Icon name="star" />
    <Card.Title>Title</Card.Title>
  </Card.Header>
  <Card.Body>Any content here</Card.Body>
  <Card.Footer>
    <CustomFooter />
  </Card.Footer>
</Card>
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Props over children | "Configure everything via props" |
| Rigid structure | "All cards look like this" |
| Control obsession | "Don't let consumers break it" |
| Complexity fear | "Composition is hard" |
| Use case blindness | "Didn't think of that" |

### Remediation

**Composition Patterns**:
```tsx
// 1. CHILDREN PATTERN
<Alert variant="warning">
  <AlertIcon />
  <AlertText>Custom message with <Link>link</Link></AlertText>
  <AlertDismiss />
</Alert>

// 2. COMPOUND COMPONENTS
<Select>
  <Select.Trigger>Choose...</Select.Trigger>
  <Select.Content>
    <Select.Group>
      <Select.Label>Fruits</Select.Label>
      <Select.Item value="apple">Apple</Select.Item>
      <Select.Item value="banana">Banana</Select.Item>
    </Select.Group>
  </Select.Content>
</Select>

// 3. RENDER PROPS
<DataTable
  data={items}
  renderRow={(item) => (
    <tr>
      <td>{item.name}</td>
      <td><CustomAction item={item} /></td>
    </tr>
  )}
/>

// 4. SLOT PATTERN
<Modal>
  <Modal.Header slot="header">Title</Modal.Header>
  <Modal.Body slot="body">Content</Modal.Body>
  <Modal.Footer slot="footer">
    <Button>Cancel</Button>
    <Button>Confirm</Button>
  </Modal.Footer>
</Modal>
```

**Headless Component Pattern**:
```tsx
// Headless: behavior without styling
function useToggle(initialState = false) {
  const [on, setOn] = useState(initialState);
  return {
    on,
    toggle: () => setOn(!on),
    buttonProps: {
      'aria-pressed': on,
      onClick: () => setOn(!on),
    },
  };
}

// Consumer adds their own styling
function MyToggle() {
  const { on, buttonProps } = useToggle();
  return (
    <button {...buttonProps} className={on ? 'active' : ''}>
      {on ? 'ON' : 'OFF'}
    </button>
  );
}
```

### Prevention Checklist
- [ ] Components accept children
- [ ] Compound component pattern for complex UI
- [ ] Render props for customization
- [ ] Slots for structured content
- [ ] Headless hooks for ultimate flexibility

---

## DS-010: No Multi-Theme Support

### Description
Design system hard-coded for single theme. Can't support dark mode, high contrast, or brand variations without major refactoring.

### Detection Signals
- Light mode only
- Hardcoded color values
- "Dark mode would require rewrite"
- No brand customization
- Theme switching requires refresh

### Theme Debt
```css
/* ❌ SINGLE THEME */
.card {
  background: #ffffff;
  color: #333333;
  border: 1px solid #e0e0e0;
}

/* ✅ THEMEABLE */
.card {
  background: var(--color-surface);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

/* Theme definitions */
:root {
  --color-surface: #ffffff;
  --color-text-primary: #333333;
}

[data-theme="dark"] {
  --color-surface: #1a1a1a;
  --color-text-primary: #f0f0f0;
}
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Not planned | "Dark mode wasn't in scope" |
| Token gaps | Not all values tokenized |
| Hardcoded values | Tokens not enforced |
| Architecture gap | No theme context |
| Color naming | "blue" vs "primary" |

### Remediation

**Theme Architecture**:
```text
THEME TOKENS:
├── Primitive tokens (color palette)
│   ├── --color-gray-100 ... --color-gray-900
│   ├── --color-blue-100 ... --color-blue-900
│   └── etc.
│
├── Semantic tokens (intent)
│   ├── --color-background
│   ├── --color-text-primary
│   ├── --color-border
│   └── --color-action
│
└── Theme mapping
    ├── Light: --color-background: var(--color-gray-100)
    └── Dark: --color-background: var(--color-gray-900)
```

**Theme Provider Pattern**:
```tsx
// Context provider
const ThemeProvider = ({ theme, children }) => {
  return (
    <div data-theme={theme} className="theme-root">
      <ThemeContext.Provider value={theme}>
        {children}
      </ThemeContext.Provider>
    </div>
  );
};

// Usage
<ThemeProvider theme={userPrefersMode}>
  <App />
</ThemeProvider>

// Component reads from context/CSS variables
function Card() {
  // Automatically themed via CSS variables
  return <div className="card">...</div>;
}
```

**Multi-Theme Testing**:
```text
EVERY COMPONENT TESTED IN:
├── Light mode
├── Dark mode
├── High contrast mode
├── Reduced motion
└── Each brand theme (if multi-brand)

STORYBOOK GLOBALS:
├── Theme switcher in toolbar
├── All stories visible in all themes
└── Chromatic captures all themes
```

### Prevention Checklist
- [ ] All colors via semantic tokens
- [ ] Theme context established
- [ ] Dark mode tested from start
- [ ] Storybook theme switcher
- [ ] High contrast mode supported

---

## Quick Reference: Anti-Pattern Detection Matrix

| Anti-Pattern | Quick Detection | Immediate Action |
|--------------|-----------------|------------------|
| DS-001: Component Soup | 500+ components | Consolidate, use props |
| DS-002: Prop Explosion | 30+ props | Compound components |
| DS-003: Missing Tokens | Hardcoded values | Token audit |
| DS-004: Inconsistent API | Same concept, different names | API conventions |
| DS-005: No A11y | No ARIA, no keyboard | A11y audit |
| DS-006: Doc Debt | "How do I use this?" | Documentation blitz |
| DS-007: Breaking Changes | "It broke after update" | Semver + migration |
| DS-008: Style Leakage | "Looks different in app" | CSS modules/isolation |
| DS-009: Not Composable | "Can't put X in Y" | Children/slots pattern |
| DS-010: No Multi-Theme | Light mode only | Token-based theming |

## Design System Audit Questions

1. "How many components do we have?" → DS-001
2. "What's the average props per component?" → DS-002
3. "How many hardcoded colors are there?" → DS-003
4. "Are prop names consistent?" → DS-004
5. "Can I use this with a screen reader?" → DS-005
6. "Where's the documentation?" → DS-006
7. "How do we handle breaking changes?" → DS-007
8. "Do components work in any context?" → DS-008
9. "Can I customize this layout?" → DS-009
10. "Does dark mode work?" → DS-010

## Resources

- **Books**: "Atomic Design" (Frost), "Design Systems" (Suarez)
- **Tools**: Storybook, Chromatic, axe-core
- **Examples**: Radix UI, Chakra UI, Primer

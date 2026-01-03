# Storybook Generation Skill

Skill for generating CSF 3.0 Storybook stories from component specifications in design.md.

## Trigger Conditions

Use this skill when:
- Component specifications are defined in design.md
- Need to generate interactive component documentation
- Want visual testing and playground for components
- Preparing component library for design review

## Prerequisites

```yaml
required_files:
  - design.md (with component specifications)
  - constitution.md (for design tokens and framework)

optional_files:
  - .storybook/preview.ts (existing Storybook config)
  - components/ (existing component implementations)
```

## CSF 3.0 Format

Component Story Format 3.0 provides:
- Type-safe story definitions with `satisfies Meta<typeof Component>`
- Autodocs for automatic documentation generation
- Args and argTypes for interactive controls
- Play functions for interaction testing

## Generation Pipeline

### 1. Load Component Specs

```text
FUNCTION load_component_specs():
  design = read("design.md")
  components = extract_component_specs(design)
  RETURN components

FUNCTION extract_component_specs(design):
  FOR section IN extract_all_sections(design, "### Component:"):
    YIELD {
      name: extract_component_name(section),
      props: parse_props_table(section),
      variants: parse_variants_table(section),
      states: parse_states(section),
      accessibility: parse_a11y_requirements(section)
    }
```

### 2. Generate Meta Configuration

```text
FUNCTION generate_meta(component):
  RETURN f"""
import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ {component.name} }} from './{component.name}';

const meta = {{
  title: 'Components/{component.name}',
  component: {component.name},
  tags: ['autodocs'],
  argTypes: {{{generate_arg_types(component)}}},
  args: {{{generate_default_args(component)}}},
}} satisfies Meta<typeof {component.name}>;

export default meta;
type Story = StoryObj<typeof meta>;
"""
```

### 3. Generate Variant Stories

```text
FUNCTION generate_variant_stories(component):
  FOR variant IN component.variants:
    YIELD f"""
export const {pascal_case(variant.name)}: Story = {{
  args: {{ variant: '{variant.name}' }},
}};
"""
```

### 4. Generate State Stories

```text
FUNCTION generate_state_stories(component):
  IF "disabled" IN component.states:
    YIELD "export const Disabled: Story = { args: { disabled: true } };"
  IF "loading" IN component.states:
    YIELD "export const Loading: Story = { args: { loading: true } };"
  IF "error" IN component.states:
    YIELD "export const Error: Story = { args: { error: true } };"
```

### 5. Generate Play Functions

```text
FUNCTION generate_play_function(interaction_type):
  IF interaction_type == "click":
    RETURN """
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const element = canvas.getByRole('button');
    await expect(element).toBeEnabled();
    await userEvent.click(element);
  },"""
  ELIF interaction_type == "form":
    RETURN """
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const input = canvas.getByRole('textbox');
    await userEvent.type(input, 'Test value');
    await expect(input).toHaveValue('Test value');
  },"""
```

## Template: Button Story

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent, expect } from '@storybook/test';
import { Button } from './Button';

const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['default', 'destructive', 'outline', 'ghost'],
    },
    size: {
      control: { type: 'select' },
      options: ['default', 'sm', 'lg', 'icon'],
    },
    disabled: { control: 'boolean' },
    loading: { control: 'boolean' },
  },
  args: { variant: 'default', size: 'default', children: 'Button' },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = { args: { children: 'Click me' } };

export const Destructive: Story = { args: { variant: 'destructive', children: 'Delete' } };

export const Disabled: Story = { args: { disabled: true, children: 'Disabled' } };

export const Loading: Story = { args: { loading: true, children: 'Loading...' } };

export const ClickInteraction: Story = {
  args: { children: 'Click me' },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');
    await expect(button).toBeEnabled();
    await userEvent.click(button);
  },
};

export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button variant="default">Default</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
    </div>
  ),
};
```

## Template: Form Story

```typescript
// LoginForm.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent, expect, waitFor } from '@storybook/test';
import { LoginForm } from './LoginForm';

const meta = {
  title: 'Components/Forms/LoginForm',
  component: LoginForm,
  tags: ['autodocs'],
  argTypes: {
    onSubmit: { action: 'submitted' },
    loading: { control: 'boolean' },
    error: { control: 'text' },
  },
} satisfies Meta<typeof LoginForm>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const WithError: Story = { args: { error: 'Invalid credentials' } };

export const FormSubmission: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.type(canvas.getByLabelText(/email/i), 'user@example.com');
    await userEvent.type(canvas.getByLabelText(/password/i), 'password123');
    await userEvent.click(canvas.getByRole('button', { name: /sign in/i }));
  },
};
```

## Template: Modal Story

```typescript
// Modal.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent, expect } from '@storybook/test';
import { Modal, ModalTrigger, ModalContent } from './Modal';
import { Button } from '../Button';

const meta = {
  title: 'Components/Overlays/Modal',
  component: Modal,
  tags: ['autodocs'],
} satisfies Meta<typeof Modal>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Modal>
      <ModalTrigger asChild><Button>Open Modal</Button></ModalTrigger>
      <ModalContent>
        <h2>Modal Title</h2>
        <p>Modal content goes here.</p>
      </ModalContent>
    </Modal>
  ),
};

export const InteractionTest: Story = {
  render: () => (
    <Modal>
      <ModalTrigger asChild><Button>Open</Button></ModalTrigger>
      <ModalContent><p>Test content</p></ModalContent>
    </Modal>
  ),
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole('button'));
    await expect(canvas.getByRole('dialog')).toBeInTheDocument();
    await userEvent.keyboard('{Escape}');
  },
};
```

## Commands

### `/storybook generate [component]`

Generate a story file for a specific component.

```text
COMMAND generate:
  ARGS: component (component name from design.md)
  OUTPUT: {ComponentName}.stories.tsx
  EXAMPLE: /storybook generate Button
```

### `/storybook generate-all`

Generate stories for all components in design.md.

```text
COMMAND generate-all:
  OUTPUT: Story files for all components
  EXAMPLE: /storybook generate-all
```

### `/storybook preview`

Launch Storybook development server.

```text
COMMAND preview:
  EXAMPLE: /storybook preview
  # Opens http://localhost:6006
```

## Integration with /speckit.design

```text
INTEGRATION_FLOW:
  1. /speckit.design generates design.md with component specs
  2. /storybook generate reads specs and creates stories
  3. Stories include: argTypes from props, variants, states, play functions
  4. /speckit.preview can render stories for visual validation
```

## Integration with /speckit.preview

```text
PREVIEW_INTEGRATION:
  1. Generate stories with /storybook generate-all
  2. Run /speckit.preview to build static Storybook
  3. Capture screenshots and generate visual comparison report
```

## Storybook Configuration

```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react';
import '../src/styles/globals.css';

const preview: Preview = {
  parameters: {
    controls: { matchers: { color: /(background|color)$/i, date: /Date$/i } },
    a11y: { element: '#storybook-root' },
    viewport: {
      viewports: {
        mobile: { name: 'Mobile', styles: { width: '375px', height: '667px' } },
        tablet: { name: 'Tablet', styles: { width: '768px', height: '1024px' } },
        desktop: { name: 'Desktop', styles: { width: '1280px', height: '800px' } },
      },
    },
  },
};

export default preview;
```

## Required Dependencies

```json
{
  "devDependencies": {
    "@storybook/react": "^8.0.0",
    "@storybook/react-vite": "^8.0.0",
    "@storybook/addon-essentials": "^8.0.0",
    "@storybook/addon-interactions": "^8.0.0",
    "@storybook/addon-a11y": "^8.0.0",
    "@storybook/test": "^8.0.0"
  }
}
```

# Stitch Prompt Templates

> Prompt templates for generating high-fidelity UI mockups from ASCII wireframes using Google Stitch.

## Overview

This module provides structured templates for converting ASCII wireframes and design specifications into prompts that Google Stitch (Gemini 2.5 Pro/Flash) can effectively process to generate professional UI designs.

## Prompt Structure

### Base Template

```text
TEMPLATE: base_prompt

Create a {screen_type} screen for {app_name}.

## Layout
{layout_description}

## Components
{component_list}

## Style
- Primary color: {primary_color}
- Secondary color: {secondary_color}
- Background: {background_color}
- Font: {font_family}
- Theme: {theme}
- Border radius: {border_radius}
- Shadows: {shadow_style}

## Content
{content_description}

## Constraints
{constraints}

Mood: {mood}
```

---

## Screen Type Templates

### Authentication Screens

#### Login Screen

```text
TEMPLATE: screen_login

Create a modern login screen for {app_name}.

## Layout
- Centered card on gradient or image background
- Logo at top of card
- Form fields vertically stacked
- Primary action button full-width
- Secondary links below (forgot password, sign up)

## Components
- Logo: {logo_description}
- Email input: Text field with label "Email" and placeholder "you@example.com"
- Password input: Password field with show/hide toggle, label "Password"
- Remember me: Checkbox with label "Remember me"
- Login button: Primary button with text "{login_cta}"
- Forgot password: Text link, right-aligned
- Sign up link: Text "Don't have an account? Sign up" below button
- Social login: {social_providers} buttons (optional)

## Style
- Primary color: {primary_color}
- Card background: white with subtle shadow
- Border radius: {border_radius} for card, smaller for inputs
- Input style: Outlined with focus ring
- Font: {font_family}
- Theme: {theme}

## Content
- Headline: "{headline}" (optional, above form)
- Subtext: "{subtext}" (optional)

## Constraints
- Mobile-responsive: Stack all elements vertically
- Accessibility: Visible focus states, form labels
- Security: No password hints in placeholder

Mood: {mood}, professional, trustworthy
```

#### Registration Screen

```text
TEMPLATE: screen_register

Create a registration/sign-up screen for {app_name}.

## Layout
- Centered card or split-screen (form + illustration)
- Logo at top
- Multi-field form with logical grouping
- Terms checkbox above submit button
- Progress indicator if multi-step (optional)

## Components
- Logo: {logo_description}
- Name fields: First name, Last name (side by side on desktop)
- Email input: Text field with validation indicator
- Password input: With strength meter
- Confirm password: Must match indicator
- Terms checkbox: "I agree to Terms of Service and Privacy Policy" with links
- Sign up button: Primary button with text "{signup_cta}"
- Login link: "Already have an account? Sign in"
- Social signup: {social_providers} buttons (optional)

## Style
- Primary color: {primary_color}
- Progress indicator: Steps or bar showing current position
- Validation: Green checkmark for valid, red for errors
- Password strength: Gradient bar (red → yellow → green)
- Border radius: {border_radius}
- Font: {font_family}

## Content
- Headline: "{headline}"
- Value proposition: Brief benefit statement (optional)

## Constraints
- Field validation: Real-time feedback
- Mobile: Single column, adequate touch targets
- Password requirements: Visible list that checks off as met

Mood: {mood}, welcoming, encouraging
```

#### Password Reset

```text
TEMPLATE: screen_password_reset

Create a password reset screen for {app_name}.

## Layout
- Centered card, minimal design
- Single focus: email input OR new password fields

## Components
For request step:
- Back link: "← Back to login"
- Headline: "Reset your password"
- Description: "Enter your email and we'll send you a reset link"
- Email input: Text field
- Submit button: "Send reset link"

For reset step:
- Headline: "Create new password"
- New password: With strength meter
- Confirm password: With match indicator
- Submit button: "Reset password"

## Style
- Minimal, focused design
- Primary color: {primary_color}
- Success state: Green confirmation with checkmark icon
- Font: {font_family}

Mood: helpful, reassuring
```

---

### Dashboard Screens

#### Main Dashboard

```text
TEMPLATE: screen_dashboard

Create a main dashboard screen for {app_name}.

## Layout
{layout_variant}

Variant A (Sidebar):
- Fixed sidebar navigation on left (240px)
- Top bar with search, notifications, user menu
- Main content area with card-based widgets

Variant B (Top Nav):
- Top navigation bar with logo, menu items, actions
- Full-width content below
- Card grid layout

## Components
- Navigation: {nav_items}
- Search: Global search input in header
- Notifications: Bell icon with badge counter
- User menu: Avatar dropdown with profile, settings, logout
- Stats cards: {stat_cards}
- Charts: {chart_types}
- Recent activity: List with timestamps
- Quick actions: {quick_actions}

## Style
- Primary color: {primary_color}
- Card style: White background, subtle shadow, {border_radius} radius
- Stat cards: Large number, small label, optional trend indicator
- Charts: Use primary color palette
- Active nav item: Background highlight or left border
- Font: {font_family}
- Theme: {theme}

## Content
- Welcome message: "Welcome back, {user_name}" or similar
- Date range selector: For filtering data (optional)

## Constraints
- Responsive: Sidebar collapses to hamburger on mobile
- Data loading: Skeleton placeholders for async data
- Empty state: Friendly message when no data

Mood: {mood}, organized, data-rich
```

#### Analytics Dashboard

```text
TEMPLATE: screen_analytics

Create an analytics dashboard for {app_name}.

## Layout
- Top section: Key metrics in horizontal cards
- Middle section: Primary chart (large, 60% width) + secondary chart (40%)
- Bottom section: Data table with filters

## Components
- Metric cards: {metrics} - each with value, label, trend (↑↓), sparkline
- Date range picker: Preset ranges + custom date selection
- Primary chart: {chart_type} showing {primary_data}
- Secondary chart: {secondary_chart_type} showing {secondary_data}
- Data table: Sortable columns, pagination, export button
- Filters: Dropdown filters for {filter_options}

## Style
- Metric cards: Consistent height, icon on left
- Trend indicators: Green for positive, red for negative
- Charts: Consistent color palette from design system
- Table: Alternating row colors, hover highlight
- Font: {font_family}, tabular numbers for data

## Constraints
- Performance: Lazy load charts below fold
- Export: CSV/PDF export options
- Mobile: Stack charts vertically, horizontal scroll for table

Mood: data-driven, professional, insightful
```

---

### Form Screens

#### Create/Edit Form

```text
TEMPLATE: screen_form

Create a {form_purpose} form for {app_name}.

## Layout
- Form header with title and close/back action
- Form body with grouped sections
- Sticky footer with actions (on long forms)

## Components
- Header: Title "{form_title}", close button
- Sections: {form_sections} - each with heading and fields
- Fields: {field_list}
- Required indicator: Asterisk or "(required)" label
- Help text: Below fields where needed
- Validation messages: Inline, below fields
- Primary action: "{submit_cta}" button
- Secondary action: "Cancel" or "Save as draft"
- Destructive action: "Delete" (edit mode only, with confirmation)

## Style
- Section spacing: Clear visual separation between groups
- Field layout: Single column or two-column where logical
- Labels: Above fields, not floating
- Required: Red asterisk
- Errors: Red text with icon, red border on field
- Border radius: {border_radius}
- Font: {font_family}

## Constraints
- Autosave: Draft saved indicator (optional)
- Unsaved changes: Warn before navigation away
- Long forms: Progress indicator or step breakdown
- Mobile: Single column, large touch targets

Mood: {mood}, efficient, guided
```

#### Multi-Step Wizard

```text
TEMPLATE: screen_wizard

Create a multi-step wizard for {wizard_purpose} in {app_name}.

## Layout
- Progress indicator at top (steps or progress bar)
- Current step content in center
- Navigation buttons at bottom

## Components
- Progress: Step indicators with labels, current/completed/pending states
- Step content: {steps}
- Back button: "← Back" (hidden on first step)
- Next button: "Continue" or "Next step"
- Finish button: "Complete" or "{completion_cta}" (last step)
- Step indicator: "Step {n} of {total}"

## Style
- Progress steps: Numbered circles, connected line
- Completed: Primary color fill with checkmark
- Current: Primary color outline, bold label
- Pending: Gray outline
- Transitions: Slide animation between steps
- Font: {font_family}

## Constraints
- Validation: Validate current step before proceeding
- State preservation: Keep data when going back
- Exit: "Save and exit" option to preserve progress
- Mobile: Horizontal scroll or simplified progress indicator

Mood: guided, progressive, encouraging
```

---

### List Screens

#### Data Table

```text
TEMPLATE: screen_table

Create a data table screen for {table_purpose} in {app_name}.

## Layout
- Page header with title and primary action
- Filter bar with search and filters
- Table with pagination
- Empty state when no results

## Components
- Header: Title "{page_title}", primary button "{add_cta}"
- Search: Search input with icon
- Filters: {filter_options} as dropdowns or chips
- Table columns: {columns}
- Row actions: {row_actions} (icons or overflow menu)
- Bulk actions: Checkbox select, bulk action bar
- Pagination: Page numbers or "Load more"
- Empty state: Illustration + message + CTA

## Style
- Table: Clean lines, alternating rows optional
- Header row: Bold, sortable indicators (↑↓)
- Row hover: Subtle highlight
- Actions: Icon buttons or "..." overflow menu
- Pagination: Clear current page indicator
- Font: {font_family}

## Constraints
- Sorting: Click column header to sort
- Column resize: Draggable borders (optional)
- Mobile: Horizontal scroll or card view
- Performance: Virtual scroll for large datasets

Mood: {mood}, organized, efficient
```

#### Card Grid

```text
TEMPLATE: screen_card_grid

Create a card grid screen for {content_type} in {app_name}.

## Layout
- Page header with title, view toggle, add button
- Filter/sort bar
- Responsive card grid
- Load more or pagination

## Components
- Header: Title "{page_title}", grid/list toggle, "{add_cta}" button
- Sort: Dropdown with sort options
- Cards: {card_content}
- Card image: Thumbnail or placeholder
- Card title: Main identifier
- Card metadata: {card_metadata}
- Card actions: {card_actions}
- Empty state: Illustration + message + CTA

## Style
- Grid: Auto-fill with min 280px cards
- Cards: Consistent height, image aspect ratio {aspect_ratio}
- Hover: Subtle lift shadow or border
- Selected: Primary color border
- Border radius: {border_radius}
- Font: {font_family}

## Constraints
- Responsive: 4 cols → 3 → 2 → 1 on smaller screens
- Lazy loading: Images load as scrolled into view
- Mobile: Consider swipeable cards

Mood: {mood}, browsable, visual
```

---

### Detail Screens

#### Item Detail

```text
TEMPLATE: screen_detail

Create a detail view screen for {item_type} in {app_name}.

## Layout
- Header with title, status, primary actions
- Tabs or sections for organizing content
- Main content area with metadata and details
- Related items sidebar or section

## Components
- Header: Back button, title "{item_title}", status badge, action buttons
- Actions: "{primary_action}", "{secondary_action}", overflow menu
- Tabs: {tab_names} (if using tabs)
- Info section: Key-value pairs for metadata
- Content section: {content_description}
- Related items: {related_content}
- Activity/history: Timeline of changes

## Style
- Status badge: Color-coded by state
- Metadata: Two-column grid or definition list
- Sections: Clear headings, adequate spacing
- Timeline: Vertical line with event nodes
- Border radius: {border_radius}
- Font: {font_family}

## Constraints
- Scrolling: Sticky header on scroll (optional)
- Loading: Skeleton for async content
- Mobile: Tabs become accordion or full-width sections
- Actions: FAB on mobile for primary action

Mood: {mood}, informative, comprehensive
```

---

### Settings Screens

#### Settings Page

```text
TEMPLATE: screen_settings

Create a settings page for {app_name}.

## Layout
- Sidebar navigation with setting categories (desktop)
- Content area with setting sections
- Mobile: Full-width list → detail pattern

## Components
- Categories: {setting_categories}
- Section header: Category title with description
- Toggle settings: Switch + label + description
- Select settings: Label + dropdown
- Input settings: Label + text input + save button
- Danger zone: Red-bordered section for destructive actions

## Style
- Sidebar: Vertical nav with icons and labels
- Active category: Highlight or left border
- Toggles: Clear on/off states
- Inputs: Inline edit with save/cancel
- Danger zone: Red accent, warning icon
- Border radius: {border_radius}
- Font: {font_family}

## Constraints
- Auto-save: Toggle changes save immediately
- Confirmation: Destructive actions require confirmation
- Mobile: Stack navigation and content
- Discoverability: Search within settings (optional)

Mood: organized, controllable, safe
```

---

### Specialized Screens

#### Empty State

```text
TEMPLATE: screen_empty

Create an empty state for {context} in {app_name}.

## Layout
- Centered content
- Illustration above text
- CTA button below

## Components
- Illustration: {illustration_style} related to {context}
- Headline: "{empty_headline}"
- Description: "{empty_description}"
- Primary CTA: "{empty_cta}" button
- Secondary action: Link or small button (optional)

## Style
- Illustration: 200-300px, muted colors or line art
- Headline: Large, bold
- Description: Smaller, muted color
- CTA: Primary button style
- Spacing: Generous whitespace
- Font: {font_family}

Mood: helpful, encouraging, not discouraging
```

#### Error State

```text
TEMPLATE: screen_error

Create an error state screen for {error_type} in {app_name}.

## Components
For 404:
- Illustration: Lost or confused theme
- Headline: "Page not found"
- Description: "The page you're looking for doesn't exist or has been moved."
- CTA: "Go home" or "Go back"

For 500:
- Illustration: Broken or error theme
- Headline: "Something went wrong"
- Description: "We're working on fixing this. Please try again later."
- CTA: "Refresh" or "Go home"
- Support link: "Contact support"

For offline:
- Illustration: Disconnected theme
- Headline: "You're offline"
- Description: "Check your connection and try again."
- CTA: "Retry"

## Style
- Illustration: Friendly, not alarming
- Colors: Muted, avoid harsh red
- Font: {font_family}

Mood: apologetic, helpful, reassuring
```

---

## Component Prompt Fragments

### Buttons

```text
FRAGMENT: button_primary
Primary button: {text}, full-width or auto-width, {color} background, white text, {radius} radius, hover darkens

FRAGMENT: button_secondary
Secondary button: {text}, outlined style, {color} border and text, transparent background, hover fills

FRAGMENT: button_ghost
Ghost button: {text}, no border, {color} text only, hover shows subtle background

FRAGMENT: button_destructive
Destructive button: {text}, red background or outlined red, for dangerous actions

FRAGMENT: button_icon
Icon button: {icon} icon, circular or rounded square, {size}px, tooltip on hover
```

### Inputs

```text
FRAGMENT: input_text
Text input: Label "{label}", placeholder "{placeholder}", {width} width, outlined style

FRAGMENT: input_password
Password input: Label "{label}", show/hide toggle icon, strength indicator below

FRAGMENT: input_select
Select dropdown: Label "{label}", options: {options}, placeholder "{placeholder}"

FRAGMENT: input_checkbox
Checkbox: Label "{label}", {checked} state, {color} when checked

FRAGMENT: input_radio
Radio group: Label "{group_label}", options: {options}, {selected} selected

FRAGMENT: input_textarea
Textarea: Label "{label}", {rows} rows, placeholder "{placeholder}", character count
```

### Cards

```text
FRAGMENT: card_basic
Card: White background, {radius} radius, subtle shadow, {padding} padding

FRAGMENT: card_interactive
Interactive card: Hover effect (lift or border), click entire card, cursor pointer

FRAGMENT: card_image
Image card: {aspect_ratio} image at top, title and description below, actions at bottom
```

### Navigation

```text
FRAGMENT: nav_sidebar
Sidebar nav: {width}px width, vertical list of items, icons + labels, collapse to icons on mobile

FRAGMENT: nav_topbar
Top navigation: Logo left, nav items center or right, user menu far right

FRAGMENT: nav_tabs
Tab navigation: Horizontal tabs, underline or pill style active indicator

FRAGMENT: nav_breadcrumb
Breadcrumbs: Path separated by /, current page non-clickable, chevron separators
```

---

## Style Modifiers

### Color Schemes

```text
MODIFIER: color_scheme_light
Light theme: White/gray backgrounds, dark text, subtle shadows, high contrast

MODIFIER: color_scheme_dark
Dark theme: Dark gray backgrounds (#1a1a1a to #2d2d2d), light text, softer shadows, glowing accents

MODIFIER: color_scheme_system
System theme: Respect user's OS preference, provide manual toggle
```

### Visual Styles

```text
MODIFIER: style_minimal
Minimal style: Clean lines, lots of whitespace, subtle interactions, no unnecessary decoration

MODIFIER: style_glassmorphism
Glassmorphism: Translucent backgrounds with blur, subtle borders, depth through transparency

MODIFIER: style_neumorphism
Neumorphism: Soft shadows both inset and outset, same-color variations, tactile feel

MODIFIER: style_gradient
Gradient accents: Gradient buttons, gradient headers, gradient decorative elements

MODIFIER: style_brutalist
Brutalist: Bold borders, high contrast, unconventional layouts, stark typography
```

### Density

```text
MODIFIER: density_comfortable
Comfortable density: Generous padding and margins, larger touch targets, relaxed spacing

MODIFIER: density_compact
Compact density: Reduced padding, tighter spacing, more content visible, smaller text

MODIFIER: density_spacious
Spacious density: Extra whitespace, breathing room, fewer elements per view
```

---

## Persona-Based Customization

### Busy Professional

```text
PERSONA_MODIFIER: busy_professional
Optimize for quick scanning and one-tap actions:
- Glanceable information hierarchy
- Prominent quick actions
- Minimal steps to complete tasks
- Status indicators visible at first glance
- Recent items and shortcuts prominent
- Mobile-first touch targets (48px minimum)
- Swipe gestures where appropriate
```

### Power User

```text
PERSONA_MODIFIER: power_user
Optimize for efficiency and density:
- Dense information display
- Keyboard shortcut hints
- Advanced filters visible
- Bulk actions available
- Customizable layout
- Command palette / quick search
- Tabs for multitasking
```

### First-Time User

```text
PERSONA_MODIFIER: first_time_user
Optimize for learning and guidance:
- Progressive disclosure
- Tooltips and hints
- Onboarding overlays
- Empty states with clear CTAs
- Simplified initial view
- "Learn more" links
- Success celebrations
```

### Casual User

```text
PERSONA_MODIFIER: casual_user
Optimize for simplicity and delight:
- Clean, uncluttered interface
- Clear primary action per screen
- Friendly, conversational copy
- Visual feedback and micro-animations
- Forgiving error handling
- Obvious navigation
```

---

## Prompt Assembly Algorithm

```text
FUNCTION assemble_stitch_prompt(wireframe, design_context, persona):

  1. SELECT base template:
     screen_type = detect_screen_type(wireframe)
     template = TEMPLATES["screen_" + screen_type] OR TEMPLATES.base_prompt

  2. FILL template variables:
     - app_name: design_context.brand_name
     - primary_color: design_context.colors.primary
     - secondary_color: design_context.colors.secondary
     - background_color: design_context.colors.background
     - font_family: design_context.typography.font_family
     - theme: design_context.theme
     - border_radius: design_context.border_radius
     - mood: design_context.style.join(", ")

  3. EXTRACT layout from wireframe:
     layout = analyze_wireframe_layout(wireframe.ascii_content)
     INSERT layout.description

  4. LIST components from wireframe:
     components = extract_components(wireframe.ascii_content)
     FOR each component:
       fragment = FRAGMENTS[component.type]
       filled_fragment = fill_fragment(fragment, component.props)
       APPEND to component_list

  5. ADD style modifiers:
     IF design_context.theme == "dark":
       APPEND MODIFIER.color_scheme_dark
     IF design_context.style.includes("minimal"):
       APPEND MODIFIER.style_minimal
     # ... etc

  6. ADD persona customization:
     IF persona:
       APPEND PERSONA_MODIFIER[persona.type]

  7. ADD constraints from context:
     IF design_context.responsive_priority == "mobile":
       APPEND "Mobile-first design, touch-friendly"
     IF design_context.accessibility_level == "AAA":
       APPEND "WCAG AAA compliance, high contrast"

  8. VALIDATE prompt:
     - Check length < 4000 chars (Stitch limit)
     - Ensure no conflicting instructions
     - Remove redundant descriptions

  9. RETURN assembled prompt
```

---

## Screen Type Detection

```text
FUNCTION detect_screen_type(wireframe):

  ascii = wireframe.ascii_content.toLowerCase()
  context = wireframe.context.toLowerCase()

  patterns = {
    login: ["login", "sign in", "email.*password", "remember me"],
    register: ["sign up", "register", "create account", "join"],
    password_reset: ["reset password", "forgot password", "recover"],
    dashboard: ["dashboard", "overview", "summary", "stats", "metrics"],
    analytics: ["analytics", "chart", "graph", "report", "trend"],
    form: ["form", "create", "edit", "add new", "save.*cancel"],
    wizard: ["step.*of", "next.*back", "progress", "wizard"],
    table: ["table", "list", "rows", "columns", "sort", "filter"],
    card_grid: ["grid", "cards", "tiles", "gallery"],
    detail: ["detail", "view", "profile", "info", "tabs"],
    settings: ["settings", "preferences", "configuration", "options"],
    empty: ["empty", "no.*found", "get started"],
    error: ["error", "404", "500", "not found", "went wrong"]
  }

  FOR each type, keywords IN patterns:
    IF any keyword MATCHES ascii OR context:
      RETURN type

  RETURN "generic"
```

---

## Prompt Optimization Tips

### Do's

```text
✅ Be specific about layout ("sidebar on left", "header at top")
✅ Include exact colors (#3B82F6, not "blue")
✅ Specify component states (hover, active, disabled)
✅ Mention responsive behavior
✅ Include content examples where helpful
✅ Use consistent terminology
✅ Keep prompts under 4000 characters
```

### Don'ts

```text
❌ Don't use vague terms ("nice", "good-looking")
❌ Don't include code snippets
❌ Don't request animations (static output only)
❌ Don't ask for multiple screens in one prompt
❌ Don't include implementation details
❌ Don't use conflicting style instructions
❌ Don't exceed token limits
```

---

## Integration with Stitch

```text
USAGE:

1. Load this module in stitch_generate_prompt()
2. Call assemble_stitch_prompt() with:
   - wireframe: Extracted ASCII wireframe
   - design_context: Colors, fonts, style from design-system.md
   - persona: Primary persona for this screen/journey
3. Save prompt to prompts-cache for retry/manual mode
4. Send to Stitch via browser automation
```

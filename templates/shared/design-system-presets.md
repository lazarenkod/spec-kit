# Design System Presets

Pre-configured design system tokens for popular UI frameworks. Use these presets by setting `preset` in your constitution.md.

## Usage

In `memory/constitution.md`, set the preset name:

```yaml
design_system:
  preset: "shadcn/ui"  # Loads all tokens from this file
  # Override specific values as needed:
  theme:
    colors:
      primary: "#custom-color"  # Overrides preset's primary
```

---

## shadcn/ui Preset

Based on shadcn/ui default theme with CSS variables.

```yaml
# preset: "shadcn/ui"
design_system:
  framework: "shadcn/ui"

  theme:
    colors:
      # Light mode defaults
      background: "#FFFFFF"
      foreground: "#0F172A"
      card: "#FFFFFF"
      card-foreground: "#0F172A"
      popover: "#FFFFFF"
      popover-foreground: "#0F172A"
      primary: "#0F172A"
      primary-foreground: "#F8FAFC"
      secondary: "#F1F5F9"
      secondary-foreground: "#0F172A"
      muted: "#F1F5F9"
      muted-foreground: "#64748B"
      accent: "#F1F5F9"
      accent-foreground: "#0F172A"
      destructive: "#EF4444"
      destructive-foreground: "#F8FAFC"
      border: "#E2E8F0"
      input: "#E2E8F0"
      ring: "#0F172A"

      # Dark mode variants (if supporting dark mode)
      # Prefix with "dark-" for dark mode tokens
      dark-background: "#0F172A"
      dark-foreground: "#F8FAFC"
      dark-card: "#0F172A"
      dark-primary: "#F8FAFC"
      dark-primary-foreground: "#0F172A"

    typography:
      font_family: "Inter, system-ui, -apple-system, sans-serif"
      font_family_mono: "JetBrains Mono, Fira Code, monospace"
      scale:
        xs: "0.75rem"      # 12px
        sm: "0.875rem"     # 14px
        base: "1rem"       # 16px
        lg: "1.125rem"     # 18px
        xl: "1.25rem"      # 20px
        2xl: "1.5rem"      # 24px
        3xl: "1.875rem"    # 30px
        4xl: "2.25rem"     # 36px
      line_heights:
        tight: "1.25"
        normal: "1.5"
        relaxed: "1.75"
      font_weights:
        normal: "400"
        medium: "500"
        semibold: "600"
        bold: "700"

    spacing:
      unit: "4px"
      scale:
        0: "0"
        1: "0.25rem"       # 4px
        2: "0.5rem"        # 8px
        3: "0.75rem"       # 12px
        4: "1rem"          # 16px
        5: "1.25rem"       # 20px
        6: "1.5rem"        # 24px
        8: "2rem"          # 32px
        10: "2.5rem"       # 40px
        12: "3rem"         # 48px

    radii:
      none: "0"
      sm: "calc(0.5rem - 4px)"   # ~4px
      md: "calc(0.5rem - 2px)"   # ~6px
      lg: "0.5rem"               # 8px
      xl: "0.75rem"              # 12px
      2xl: "1rem"                # 16px
      full: "9999px"

    shadows:
      sm: "0 1px 2px 0 rgb(0 0 0 / 0.05)"
      md: "0 4px 6px -1px rgb(0 0 0 / 0.1)"
      lg: "0 10px 15px -3px rgb(0 0 0 / 0.1)"

  component_library_url: "https://ui.shadcn.com/docs"
  enforcement_level: "warn"

  # Component mapping for DSS-001 detection
  components:
    button: "@/components/ui/button"
    input: "@/components/ui/input"
    select: "@/components/ui/select"
    checkbox: "@/components/ui/checkbox"
    dialog: "@/components/ui/dialog"
    dropdown-menu: "@/components/ui/dropdown-menu"
    card: "@/components/ui/card"
    tabs: "@/components/ui/tabs"
    toast: "@/components/ui/toast"
    form: "@/components/ui/form"
```

---

## MUI (Material UI) Preset

Based on Material UI v5 default theme.

```yaml
# preset: "mui"
design_system:
  framework: "mui"

  theme:
    colors:
      # Primary palette
      primary: "#1976D2"
      primary-light: "#42A5F5"
      primary-dark: "#1565C0"
      primary-contrast: "#FFFFFF"

      # Secondary palette
      secondary: "#9C27B0"
      secondary-light: "#BA68C8"
      secondary-dark: "#7B1FA2"
      secondary-contrast: "#FFFFFF"

      # Semantic colors
      error: "#D32F2F"
      error-light: "#EF5350"
      error-dark: "#C62828"
      warning: "#ED6C02"
      warning-light: "#FF9800"
      warning-dark: "#E65100"
      info: "#0288D1"
      info-light: "#03A9F4"
      info-dark: "#01579B"
      success: "#2E7D32"
      success-light: "#4CAF50"
      success-dark: "#1B5E20"

      # Background
      background: "#FFFFFF"
      background-paper: "#FFFFFF"
      background-default: "#FAFAFA"

      # Text
      text-primary: "rgba(0, 0, 0, 0.87)"
      text-secondary: "rgba(0, 0, 0, 0.6)"
      text-disabled: "rgba(0, 0, 0, 0.38)"

      # Actions
      action-active: "rgba(0, 0, 0, 0.54)"
      action-hover: "rgba(0, 0, 0, 0.04)"
      action-selected: "rgba(0, 0, 0, 0.08)"
      action-disabled: "rgba(0, 0, 0, 0.26)"

      # Divider
      divider: "rgba(0, 0, 0, 0.12)"

    typography:
      font_family: "Roboto, Helvetica, Arial, sans-serif"
      font_family_mono: "Roboto Mono, monospace"
      scale:
        # MUI uses specific variant names
        h1: "6rem"         # 96px
        h2: "3.75rem"      # 60px
        h3: "3rem"         # 48px
        h4: "2.125rem"     # 34px
        h5: "1.5rem"       # 24px
        h6: "1.25rem"      # 20px
        subtitle1: "1rem"  # 16px
        subtitle2: "0.875rem"  # 14px
        body1: "1rem"      # 16px
        body2: "0.875rem"  # 14px
        button: "0.875rem" # 14px
        caption: "0.75rem" # 12px
        overline: "0.75rem" # 12px
      font_weights:
        light: "300"
        regular: "400"
        medium: "500"
        bold: "700"

    spacing:
      unit: "8px"          # MUI uses 8px base
      scale:
        0: "0"
        1: "8px"
        2: "16px"
        3: "24px"
        4: "32px"
        5: "40px"
        6: "48px"

    radii:
      none: "0"
      sm: "4px"
      md: "4px"            # MUI default
      lg: "8px"
      xl: "16px"
      full: "9999px"

    shadows:
      # MUI has 25 elevation levels (0-24)
      0: "none"
      1: "0px 2px 1px -1px rgba(0,0,0,0.2)"
      2: "0px 3px 1px -2px rgba(0,0,0,0.2)"
      4: "0px 2px 4px -1px rgba(0,0,0,0.2)"
      8: "0px 5px 5px -3px rgba(0,0,0,0.2)"
      16: "0px 8px 10px -5px rgba(0,0,0,0.2)"
      24: "0px 11px 15px -7px rgba(0,0,0,0.2)"

  component_library_url: "https://mui.com/material-ui/getting-started/"
  enforcement_level: "warn"

  # Component mapping for DSS-001 detection
  components:
    button: "@mui/material/Button"
    text-field: "@mui/material/TextField"
    select: "@mui/material/Select"
    checkbox: "@mui/material/Checkbox"
    dialog: "@mui/material/Dialog"
    menu: "@mui/material/Menu"
    card: "@mui/material/Card"
    tabs: "@mui/material/Tabs"
    snackbar: "@mui/material/Snackbar"
    autocomplete: "@mui/material/Autocomplete"
```

---

## Tailwind CSS Preset

Based on Tailwind CSS v3 default configuration.

```yaml
# preset: "tailwind"
design_system:
  framework: "tailwind"

  theme:
    colors:
      # Tailwind default palette (subset - key colors only)
      # Full palette at https://tailwindcss.com/docs/customizing-colors

      # Slate (neutral gray)
      slate-50: "#F8FAFC"
      slate-100: "#F1F5F9"
      slate-200: "#E2E8F0"
      slate-300: "#CBD5E1"
      slate-400: "#94A3B8"
      slate-500: "#64748B"
      slate-600: "#475569"
      slate-700: "#334155"
      slate-800: "#1E293B"
      slate-900: "#0F172A"
      slate-950: "#020617"

      # Blue (primary)
      blue-50: "#EFF6FF"
      blue-100: "#DBEAFE"
      blue-500: "#3B82F6"
      blue-600: "#2563EB"
      blue-700: "#1D4ED8"

      # Green (success)
      green-50: "#F0FDF4"
      green-500: "#22C55E"
      green-600: "#16A34A"
      green-700: "#15803D"

      # Red (error/destructive)
      red-50: "#FEF2F2"
      red-500: "#EF4444"
      red-600: "#DC2626"
      red-700: "#B91C1C"

      # Yellow (warning)
      yellow-50: "#FEFCE8"
      yellow-500: "#EAB308"
      yellow-600: "#CA8A04"

      # Semantic mapping
      primary: "#3B82F6"      # blue-500
      secondary: "#64748B"    # slate-500
      background: "#FFFFFF"
      foreground: "#0F172A"   # slate-900
      muted: "#F1F5F9"        # slate-100
      destructive: "#EF4444"  # red-500
      success: "#22C55E"      # green-500
      warning: "#EAB308"      # yellow-500

    typography:
      font_family: "ui-sans-serif, system-ui, -apple-system, sans-serif"
      font_family_mono: "ui-monospace, SFMono-Regular, monospace"
      font_family_serif: "ui-serif, Georgia, serif"
      scale:
        xs: "0.75rem"      # 12px
        sm: "0.875rem"     # 14px
        base: "1rem"       # 16px
        lg: "1.125rem"     # 18px
        xl: "1.25rem"      # 20px
        2xl: "1.5rem"      # 24px
        3xl: "1.875rem"    # 30px
        4xl: "2.25rem"     # 36px
        5xl: "3rem"        # 48px
        6xl: "3.75rem"     # 60px
        7xl: "4.5rem"      # 72px
        8xl: "6rem"        # 96px
        9xl: "8rem"        # 128px
      font_weights:
        thin: "100"
        extralight: "200"
        light: "300"
        normal: "400"
        medium: "500"
        semibold: "600"
        bold: "700"
        extrabold: "800"
        black: "900"
      line_heights:
        none: "1"
        tight: "1.25"
        snug: "1.375"
        normal: "1.5"
        relaxed: "1.625"
        loose: "2"

    spacing:
      unit: "4px"           # Tailwind uses 4px base
      scale:
        0: "0"
        px: "1px"
        0.5: "0.125rem"     # 2px
        1: "0.25rem"        # 4px
        2: "0.5rem"         # 8px
        3: "0.75rem"        # 12px
        4: "1rem"           # 16px
        5: "1.25rem"        # 20px
        6: "1.5rem"         # 24px
        8: "2rem"           # 32px
        10: "2.5rem"        # 40px
        12: "3rem"          # 48px
        16: "4rem"          # 64px
        20: "5rem"          # 80px
        24: "6rem"          # 96px

    radii:
      none: "0"
      sm: "0.125rem"       # 2px
      md: "0.25rem"        # 4px (default)
      lg: "0.5rem"         # 8px
      xl: "0.75rem"        # 12px
      2xl: "1rem"          # 16px
      3xl: "1.5rem"        # 24px
      full: "9999px"

    shadows:
      sm: "0 1px 2px 0 rgb(0 0 0 / 0.05)"
      md: "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)"
      lg: "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
      xl: "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
      2xl: "0 25px 50px -12px rgb(0 0 0 / 0.25)"

  component_library_url: "https://tailwindcss.com/docs"
  enforcement_level: "warn"

  # For Tailwind, DSS-001 focuses on utility class usage
  # No component mapping - check for Tailwind utility patterns instead
  utility_patterns:
    colors: "bg-|text-|border-|ring-|fill-|stroke-"
    typography: "text-|font-|leading-|tracking-"
    spacing: "p-|m-|gap-|space-"
```

---

## Vuetify Preset

Based on Vuetify v3 default theme.

```yaml
# preset: "vuetify"
design_system:
  framework: "vuetify"

  theme:
    colors:
      # Vuetify theme colors
      primary: "#1867C0"
      secondary: "#5CBBF6"
      accent: "#82B1FF"
      error: "#FF5252"
      info: "#2196F3"
      success: "#4CAF50"
      warning: "#FB8C00"

      # Surface colors
      background: "#FFFFFF"
      surface: "#FFFFFF"
      surface-variant: "#424242"

      # Text colors
      on-primary: "#FFFFFF"
      on-secondary: "#000000"
      on-surface: "#000000"
      on-background: "#000000"

    typography:
      font_family: "Roboto, sans-serif"
      font_family_mono: "Roboto Mono, monospace"
      scale:
        # Vuetify typography scale
        h1: "6rem"
        h2: "3.75rem"
        h3: "3rem"
        h4: "2.125rem"
        h5: "1.5rem"
        h6: "1.25rem"
        subtitle-1: "1rem"
        subtitle-2: "0.875rem"
        body-1: "1rem"
        body-2: "0.875rem"
        button: "0.875rem"
        caption: "0.75rem"
        overline: "0.75rem"

    spacing:
      unit: "4px"
      # Vuetify uses multiples of 4px

    radii:
      none: "0"
      sm: "4px"
      md: "4px"
      lg: "8px"
      xl: "24px"
      pill: "9999px"

  component_library_url: "https://vuetifyjs.com/en/components/all/"
  enforcement_level: "warn"

  components:
    button: "v-btn"
    text-field: "v-text-field"
    select: "v-select"
    checkbox: "v-checkbox"
    dialog: "v-dialog"
    menu: "v-menu"
    card: "v-card"
    tabs: "v-tabs"
    snackbar: "v-snackbar"
    autocomplete: "v-autocomplete"
```

---

## Bootstrap Preset

Based on Bootstrap v5 default variables.

```yaml
# preset: "bootstrap"
design_system:
  framework: "bootstrap"

  theme:
    colors:
      # Bootstrap theme colors
      primary: "#0D6EFD"
      secondary: "#6C757D"
      success: "#198754"
      info: "#0DCAF0"
      warning: "#FFC107"
      danger: "#DC3545"
      light: "#F8F9FA"
      dark: "#212529"

      # Grays
      white: "#FFFFFF"
      gray-100: "#F8F9FA"
      gray-200: "#E9ECEF"
      gray-300: "#DEE2E6"
      gray-400: "#CED4DA"
      gray-500: "#ADB5BD"
      gray-600: "#6C757D"
      gray-700: "#495057"
      gray-800: "#343A40"
      gray-900: "#212529"
      black: "#000000"

      # Semantic
      background: "#FFFFFF"
      body-bg: "#FFFFFF"
      body-color: "#212529"
      border-color: "#DEE2E6"

    typography:
      font_family: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
      font_family_mono: "SFMono-Regular, Menlo, Monaco, monospace"
      scale:
        # Bootstrap font sizes
        1: "2.5rem"        # 40px (h1)
        2: "2rem"          # 32px (h2)
        3: "1.75rem"       # 28px (h3)
        4: "1.5rem"        # 24px (h4)
        5: "1.25rem"       # 20px (h5)
        6: "1rem"          # 16px (h6)
        base: "1rem"       # 16px
        sm: "0.875rem"     # 14px
        lg: "1.25rem"      # 20px
      font_weights:
        lighter: "lighter"
        light: "300"
        normal: "400"
        semibold: "600"
        bold: "700"
        bolder: "bolder"

    spacing:
      unit: "4px"          # Bootstrap $spacer / 4
      scale:
        0: "0"
        1: "0.25rem"       # 4px
        2: "0.5rem"        # 8px
        3: "1rem"          # 16px
        4: "1.5rem"        # 24px
        5: "3rem"          # 48px

    radii:
      none: "0"
      sm: "0.25rem"        # 4px
      md: "0.375rem"       # 6px (default)
      lg: "0.5rem"         # 8px
      xl: "1rem"           # 16px
      pill: "50rem"

  component_library_url: "https://getbootstrap.com/docs/5.3/components/"
  enforcement_level: "warn"

  components:
    button: "btn"
    input: "form-control"
    select: "form-select"
    checkbox: "form-check-input"
    modal: "modal"
    dropdown: "dropdown"
    card: "card"
    nav-tabs: "nav-tabs"
    toast: "toast"
```

---

## Creating Custom Presets

To create a custom preset for your organization:

1. Copy the structure from any preset above
2. Replace token values with your brand guidelines
3. Save as `design-system-presets.custom.md` in your project
4. Reference with `preset: "custom"` in constitution.md

### Example: Custom Brand Preset

```yaml
# preset: "acme-brand"
design_system:
  framework: "acme-components"

  theme:
    colors:
      # ACME Corp brand colors
      primary: "#FF6B00"       # ACME Orange
      secondary: "#1A1A1A"     # ACME Dark
      accent: "#00D4AA"        # ACME Teal
      background: "#FFFFFF"
      foreground: "#1A1A1A"
      # ... additional brand tokens

  component_library_url: "https://design.acme.com/components"
  enforcement_level: "strict"  # ACME requires strict compliance

  components:
    button: "@acme/ui/Button"
    # ... additional component mappings
```

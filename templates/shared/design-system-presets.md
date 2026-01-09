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

## shadcn/ui Preset (DEFAULT)

**Primary choice for all React/Next.js projects.** Based on shadcn/ui default theme with CSS variables.

See `templates/shared/shadcn-registry.md` for complete component reference.

```yaml
# preset: "shadcn/ui"
design_system:
  framework: "shadcn/ui"
  is_default: true  # Auto-applied unless --library flag overrides

  theme:
    colors:
      # Core semantic colors (HSL values for CSS variables)
      background: "0 0% 100%"           # --background
      foreground: "222.2 84% 4.9%"      # --foreground
      card: "0 0% 100%"                 # --card
      card-foreground: "222.2 84% 4.9%" # --card-foreground
      popover: "0 0% 100%"              # --popover
      popover-foreground: "222.2 84% 4.9%"
      primary: "222.2 47.4% 11.2%"      # --primary
      primary-foreground: "210 40% 98%"
      secondary: "210 40% 96.1%"        # --secondary
      secondary-foreground: "222.2 47.4% 11.2%"
      muted: "210 40% 96.1%"            # --muted
      muted-foreground: "215.4 16.3% 46.9%"
      accent: "210 40% 96.1%"           # --accent
      accent-foreground: "222.2 47.4% 11.2%"
      destructive: "0 84.2% 60.2%"      # --destructive
      destructive-foreground: "210 40% 98%"
      border: "214.3 31.8% 91.4%"       # --border
      input: "214.3 31.8% 91.4%"        # --input
      ring: "222.2 84% 4.9%"            # --ring
      radius: "0.5rem"                  # --radius

      # Chart colors (for Recharts integration)
      chart-1: "12 76% 61%"             # --chart-1 (orange)
      chart-2: "173 58% 39%"            # --chart-2 (teal)
      chart-3: "197 37% 24%"            # --chart-3 (dark blue)
      chart-4: "43 74% 66%"             # --chart-4 (yellow)
      chart-5: "27 87% 67%"             # --chart-5 (peach)

      # Sidebar colors (for sidebar component)
      sidebar-background: "0 0% 98%"    # --sidebar-background
      sidebar-foreground: "240 5.3% 26.1%"
      sidebar-primary: "240 5.9% 10%"
      sidebar-primary-foreground: "0 0% 98%"
      sidebar-accent: "240 4.8% 95.9%"
      sidebar-accent-foreground: "240 5.9% 10%"
      sidebar-border: "220 13% 91%"
      sidebar-ring: "217.2 91.2% 59.8%"

      # Dark mode variants
      dark:
        background: "222.2 84% 4.9%"
        foreground: "210 40% 98%"
        card: "222.2 84% 4.9%"
        card-foreground: "210 40% 98%"
        popover: "222.2 84% 4.9%"
        popover-foreground: "210 40% 98%"
        primary: "210 40% 98%"
        primary-foreground: "222.2 47.4% 11.2%"
        secondary: "217.2 32.6% 17.5%"
        secondary-foreground: "210 40% 98%"
        muted: "217.2 32.6% 17.5%"
        muted-foreground: "215 20.2% 65.1%"
        accent: "217.2 32.6% 17.5%"
        accent-foreground: "210 40% 98%"
        destructive: "0 62.8% 30.6%"
        destructive-foreground: "210 40% 98%"
        border: "217.2 32.6% 17.5%"
        input: "217.2 32.6% 17.5%"
        ring: "212.7 26.8% 83.9%"
        # Dark chart colors
        chart-1: "220 70% 50%"
        chart-2: "160 60% 45%"
        chart-3: "30 80% 55%"
        chart-4: "280 65% 60%"
        chart-5: "340 75% 55%"
        # Dark sidebar
        sidebar-background: "240 5.9% 10%"
        sidebar-foreground: "240 4.8% 95.9%"
        sidebar-primary: "224.3 76.3% 48%"
        sidebar-primary-foreground: "0 0% 100%"
        sidebar-accent: "240 3.7% 15.9%"
        sidebar-accent-foreground: "240 4.8% 95.9%"
        sidebar-border: "240 3.7% 15.9%"
        sidebar-ring: "217.2 91.2% 59.8%"

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
        5xl: "3rem"        # 48px
      line_heights:
        none: "1"
        tight: "1.25"
        snug: "1.375"
        normal: "1.5"
        relaxed: "1.625"
        loose: "2"
      font_weights:
        normal: "400"
        medium: "500"
        semibold: "600"
        bold: "700"
        extrabold: "800"
      tracking:
        tighter: "-0.05em"
        tight: "-0.025em"
        normal: "0em"
        wide: "0.025em"
        wider: "0.05em"
        widest: "0.1em"

    spacing:
      unit: "4px"
      scale:
        0: "0"
        px: "1px"
        0.5: "0.125rem"    # 2px
        1: "0.25rem"       # 4px
        1.5: "0.375rem"    # 6px
        2: "0.5rem"        # 8px
        2.5: "0.625rem"    # 10px
        3: "0.75rem"       # 12px
        3.5: "0.875rem"    # 14px
        4: "1rem"          # 16px
        5: "1.25rem"       # 20px
        6: "1.5rem"        # 24px
        7: "1.75rem"       # 28px
        8: "2rem"          # 32px
        9: "2.25rem"       # 36px
        10: "2.5rem"       # 40px
        11: "2.75rem"      # 44px
        12: "3rem"         # 48px
        14: "3.5rem"       # 56px
        16: "4rem"         # 64px
        20: "5rem"         # 80px
        24: "6rem"         # 96px
        28: "7rem"         # 112px
        32: "8rem"         # 128px

    radii:
      none: "0"
      sm: "calc(var(--radius) - 4px)"   # ~4px
      md: "calc(var(--radius) - 2px)"   # ~6px
      lg: "var(--radius)"               # 8px (default)
      xl: "calc(var(--radius) + 4px)"   # 12px
      2xl: "calc(var(--radius) + 8px)"  # 16px
      3xl: "calc(var(--radius) + 16px)" # 24px
      full: "9999px"

    shadows:
      sm: "0 1px 2px 0 rgb(0 0 0 / 0.05)"
      md: "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)"
      lg: "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
      xl: "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
      2xl: "0 25px 50px -12px rgb(0 0 0 / 0.25)"
      inner: "inset 0 2px 4px 0 rgb(0 0 0 / 0.05)"

    # Motion tokens for animations
    motion:
      duration:
        instant: "0ms"
        fast: "100ms"
        normal: "200ms"
        slow: "300ms"
        deliberate: "500ms"
      easing:
        ease-out: "cubic-bezier(0, 0, 0.2, 1)"
        ease-in: "cubic-bezier(0.4, 0, 1, 1)"
        ease-in-out: "cubic-bezier(0.4, 0, 0.2, 1)"
        spring: "cubic-bezier(0.175, 0.885, 0.32, 1.275)"
      keyframes:
        # Radix UI animation keyframes
        accordion-down: "{ from { height: 0 } to { height: var(--radix-accordion-content-height) } }"
        accordion-up: "{ from { height: var(--radix-accordion-content-height) } to { height: 0 } }"
        collapsible-down: "{ from { height: 0 } to { height: var(--radix-collapsible-content-height) } }"
        collapsible-up: "{ from { height: var(--radix-collapsible-content-height) } to { height: 0 } }"
        # Fade animations
        fade-in: "{ from { opacity: 0 } to { opacity: 1 } }"
        fade-out: "{ from { opacity: 1 } to { opacity: 0 } }"
        # Slide animations
        slide-in-from-top: "{ from { transform: translateY(-100%) } to { transform: translateY(0) } }"
        slide-in-from-bottom: "{ from { transform: translateY(100%) } to { transform: translateY(0) } }"
        slide-in-from-left: "{ from { transform: translateX(-100%) } to { transform: translateX(0) } }"
        slide-in-from-right: "{ from { transform: translateX(100%) } to { transform: translateX(0) } }"
        slide-out-to-top: "{ from { transform: translateY(0) } to { transform: translateY(-100%) } }"
        slide-out-to-bottom: "{ from { transform: translateY(0) } to { transform: translateY(100%) } }"
        slide-out-to-left: "{ from { transform: translateX(0) } to { transform: translateX(-100%) } }"
        slide-out-to-right: "{ from { transform: translateX(0) } to { transform: translateX(100%) } }"
        # Scale animations
        scale-in: "{ from { transform: scale(0.95); opacity: 0 } to { transform: scale(1); opacity: 1 } }"
        scale-out: "{ from { transform: scale(1); opacity: 1 } to { transform: scale(0.95); opacity: 0 } }"
        # Spin
        spin: "{ from { transform: rotate(0deg) } to { transform: rotate(360deg) } }"

  component_library_url: "https://ui.shadcn.com/docs"
  component_registry: "templates/shared/shadcn-registry.md"
  enforcement_level: "warn"

  # Dependencies for shadcn/ui
  dependencies:
    core:
      - "tailwindcss"
      - "tailwind-merge"
      - "clsx"
      - "class-variance-authority"
    optional:
      - "@radix-ui/react-accordion"
      - "@radix-ui/react-alert-dialog"
      - "@radix-ui/react-aspect-ratio"
      - "@radix-ui/react-avatar"
      - "@radix-ui/react-checkbox"
      - "@radix-ui/react-collapsible"
      - "@radix-ui/react-context-menu"
      - "@radix-ui/react-dialog"
      - "@radix-ui/react-dropdown-menu"
      - "@radix-ui/react-hover-card"
      - "@radix-ui/react-label"
      - "@radix-ui/react-menubar"
      - "@radix-ui/react-navigation-menu"
      - "@radix-ui/react-popover"
      - "@radix-ui/react-progress"
      - "@radix-ui/react-radio-group"
      - "@radix-ui/react-scroll-area"
      - "@radix-ui/react-select"
      - "@radix-ui/react-separator"
      - "@radix-ui/react-slider"
      - "@radix-ui/react-switch"
      - "@radix-ui/react-tabs"
      - "@radix-ui/react-toast"
      - "@radix-ui/react-toggle"
      - "@radix-ui/react-toggle-group"
      - "@radix-ui/react-tooltip"
      - "cmdk"
      - "embla-carousel-react"
      - "input-otp"
      - "react-day-picker"
      - "react-hook-form"
      - "@hookform/resolvers"
      - "zod"
      - "recharts"
      - "sonner"
      - "vaul"
      - "@tanstack/react-table"
      - "react-resizable-panels"

  # Component mapping for DSS-001 detection (expanded)
  components:
    # Form components
    button: "@/components/ui/button"
    input: "@/components/ui/input"
    textarea: "@/components/ui/textarea"
    select: "@/components/ui/select"
    checkbox: "@/components/ui/checkbox"
    radio-group: "@/components/ui/radio-group"
    switch: "@/components/ui/switch"
    slider: "@/components/ui/slider"
    toggle: "@/components/ui/toggle"
    toggle-group: "@/components/ui/toggle-group"
    input-otp: "@/components/ui/input-otp"
    label: "@/components/ui/label"
    form: "@/components/ui/form"
    # Display components
    card: "@/components/ui/card"
    badge: "@/components/ui/badge"
    alert: "@/components/ui/alert"
    avatar: "@/components/ui/avatar"
    skeleton: "@/components/ui/skeleton"
    separator: "@/components/ui/separator"
    aspect-ratio: "@/components/ui/aspect-ratio"
    scroll-area: "@/components/ui/scroll-area"
    resizable: "@/components/ui/resizable"
    collapsible: "@/components/ui/collapsible"
    # Navigation components
    breadcrumb: "@/components/ui/breadcrumb"
    pagination: "@/components/ui/pagination"
    menubar: "@/components/ui/menubar"
    navigation-menu: "@/components/ui/navigation-menu"
    dropdown-menu: "@/components/ui/dropdown-menu"
    context-menu: "@/components/ui/context-menu"
    tabs: "@/components/ui/tabs"
    sidebar: "@/components/ui/sidebar"
    # Overlay components
    dialog: "@/components/ui/dialog"
    alert-dialog: "@/components/ui/alert-dialog"
    drawer: "@/components/ui/drawer"
    sheet: "@/components/ui/sheet"
    popover: "@/components/ui/popover"
    hover-card: "@/components/ui/hover-card"
    tooltip: "@/components/ui/tooltip"
    command: "@/components/ui/command"
    # Data components
    table: "@/components/ui/table"
    data-table: "@/components/ui/data-table"
    carousel: "@/components/ui/carousel"
    calendar: "@/components/ui/calendar"
    progress: "@/components/ui/progress"
    chart: "@/components/ui/chart"
    # Feedback components
    toast: "@/components/ui/toast"
    sonner: "@/components/ui/sonner"
    # Utility components
    accordion: "@/components/ui/accordion"
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

    # Motion tokens (MUI transitions)
    motion:
      duration:
        shortest: "150ms"
        shorter: "200ms"
        short: "250ms"
        standard: "300ms"
        complex: "375ms"
        enteringScreen: "225ms"
        leavingScreen: "195ms"
      easing:
        easeInOut: "cubic-bezier(0.4, 0, 0.2, 1)"
        easeOut: "cubic-bezier(0.0, 0, 0.2, 1)"
        easeIn: "cubic-bezier(0.4, 0, 1, 1)"
        sharp: "cubic-bezier(0.4, 0, 0.6, 1)"
      # MUI uses transition helpers, not raw keyframes
      transitions:
        create: "all {duration} {easing}"
        getAutoHeightDuration: "min({height} / 36 * 10, 300)ms"

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

    # Motion tokens (Tailwind animation utilities)
    motion:
      duration:
        75: "75ms"
        100: "100ms"
        150: "150ms"
        200: "200ms"
        300: "300ms"
        500: "500ms"
        700: "700ms"
        1000: "1000ms"
      easing:
        linear: "linear"
        in: "cubic-bezier(0.4, 0, 1, 1)"
        out: "cubic-bezier(0, 0, 0.2, 1)"
        in-out: "cubic-bezier(0.4, 0, 0.2, 1)"
      keyframes:
        spin: "{ to { transform: rotate(360deg) } }"
        ping: "{ 75%, 100% { transform: scale(2); opacity: 0 } }"
        pulse: "{ 50% { opacity: 0.5 } }"
        bounce: "{ 0%, 100% { transform: translateY(-25%); animation-timing-function: cubic-bezier(0.8, 0, 1, 1) } 50% { transform: none; animation-timing-function: cubic-bezier(0, 0, 0.2, 1) } }"
      animation:
        spin: "spin 1s linear infinite"
        ping: "ping 1s cubic-bezier(0, 0, 0.2, 1) infinite"
        pulse: "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite"
        bounce: "bounce 1s infinite"

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

    # Motion tokens (Vuetify transitions)
    motion:
      duration:
        fast: "150ms"
        normal: "250ms"
        slow: "350ms"
      easing:
        standard: "cubic-bezier(0.4, 0, 0.2, 1)"
        decelerate: "cubic-bezier(0.0, 0, 0.2, 1)"
        accelerate: "cubic-bezier(0.4, 0, 1, 1)"
      transitions:
        # Vuetify built-in transition names
        fade: "v-fade-transition"
        scale: "v-scale-transition"
        slide-x: "v-slide-x-transition"
        slide-x-reverse: "v-slide-x-reverse-transition"
        slide-y: "v-slide-y-transition"
        slide-y-reverse: "v-slide-y-reverse-transition"
        scroll-x: "v-scroll-x-transition"
        scroll-y: "v-scroll-y-transition"
        expand: "v-expand-transition"

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

    # Motion tokens (Bootstrap transitions)
    motion:
      duration:
        base: "150ms"       # $transition-base
        fade: "150ms"       # $transition-fade
        collapse: "350ms"   # $transition-collapse
      easing:
        base: "ease-in-out"
        collapse: "ease"
      transitions:
        # Bootstrap CSS transition values
        base: "all 0.15s ease-in-out"
        fade: "opacity 0.15s linear"
        collapse: "height 0.35s ease"
        transform: "transform 0.15s ease-in-out"
      keyframes:
        # Bootstrap keyframe animations
        spinner-border: "{ to { transform: rotate(360deg) } }"
        spinner-grow: "{ 0% { transform: scale(0) } 50% { opacity: 1; transform: none } }"
        placeholder-glow: "{ 50% { opacity: 0.2 } }"
        placeholder-wave: "{ 100% { mask-position: -200% 0% } }"

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

    motion:
      # ACME brand motion values
      duration:
        instant: "0ms"
        fast: "120ms"          # Slightly snappier than default
        normal: "200ms"
        slow: "350ms"
        dramatic: "600ms"      # For hero transitions
      easing:
        # ACME custom easing curves
        ease-out: "cubic-bezier(0.22, 1, 0.36, 1)"   # Smooth deceleration
        ease-in: "cubic-bezier(0.64, 0, 0.78, 0)"   # Gradual acceleration
        spring: "cubic-bezier(0.34, 1.56, 0.64, 1)" # Bouncy ACME feel
        bounce: "cubic-bezier(0.68, -0.55, 0.27, 1.55)"
      keyframes:
        acme-pop: "{ 0% { transform: scale(0.9); opacity: 0 } 70% { transform: scale(1.05) } 100% { transform: scale(1); opacity: 1 } }"
        acme-slide-up: "{ from { transform: translateY(20px); opacity: 0 } to { transform: translateY(0); opacity: 1 } }"

  component_library_url: "https://design.acme.com/components"
  enforcement_level: "strict"  # ACME requires strict compliance

  components:
    button: "@acme/ui/Button"
    # ... additional component mappings
```

---

## Motion Token Reference

All presets include standardized motion tokens for consistency across animation generation:

| Category | Purpose | Typical Values |
|----------|---------|---------------|
| `duration` | Animation timing | instant (0ms), fast (100-150ms), normal (200-300ms), slow (350-500ms) |
| `easing` | Acceleration curves | ease-out, ease-in, ease-in-out, spring, bounce |
| `keyframes` | Reusable animations | fade-in, slide-up, scale-in, spin, pulse |
| `transitions` | Combined shorthand | "all 200ms ease-out" |

### Reduced Motion Support

All motion tokens should have `prefers-reduced-motion` alternatives:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

See `templates/shared/animation-presets/` for detailed animation implementations with reduced-motion alternatives.

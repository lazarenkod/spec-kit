# Component Library Recommendations Guide

This document provides context for AI agents automatically recommending component libraries based on detected UI framework.

## Overview

Component Library Recommendations automates the selection of appropriate UI component libraries (shadcn/ui, MUI, Vuetify, etc.) based on the project's UI framework (React, Vue, Angular, Svelte). This reduces decision fatigue and ensures design system consistency from project inception.

### Integration Points

- **`/speckit.design`**: Step 0.75 auto-detects framework and recommends libraries
- **`constitution.md`**: Stores recommended preset after user confirmation
- **`design-system-presets.md`**: Contains preset tokens for each library

### Workflow

```text
1. User runs /speckit.design
2. Step 0.75: Check if design_system.framework is "none"
3. Parse spec.md → Framework Requirements table
4. Parse constitution.md → Technology Constraints → UI Framework
5. Apply recommendation algorithm
6. Present recommendation to user
7. If confirmed → apply preset to constitution.md
8. Continue with design.md generation
```

---

## Framework → Library Mapping

### Primary Recommendations

| UI Framework | Primary Library | Preset Key | Reasoning |
|--------------|-----------------|------------|-----------|
| React + TypeScript | shadcn/ui | `shadcn/ui` | Accessible, zero runtime, copy-paste ownership, full TS support |
| React (JS) | MUI (Material UI) | `mui` | Comprehensive, enterprise-proven, strong community |
| Vue.js 3 | Vuetify 3 | `vuetify` | Material Design, excellent TypeScript support, rich components |
| Angular | Angular Material | `angular-material` | Official library, tight framework integration, accessibility built-in |
| Svelte / SvelteKit | Skeleton UI | `skeleton-ui` | Svelte-native, Tailwind-based, lightweight |

### Alternative Recommendations

| UI Framework | Alternative 1 | Alternative 2 | Alternative 3 |
|--------------|---------------|---------------|---------------|
| React + TS | MUI | Radix UI | Headless UI |
| React (JS) | shadcn/ui | Chakra UI | Bootstrap React |
| Vue.js 3 | PrimeVue | Quasar | Bootstrap Vue |
| Angular | PrimeNG | ng-bootstrap | Taiga UI |
| Svelte | Svelte Material UI | Carbon Svelte | - |

### Tailwind CSS Note

Tailwind CSS is a utility-first CSS framework, not a component library. When detected:
- Recommend `tailwind` preset for token-based styling
- Suggest pairing with headless component library (Headless UI, Radix)
- shadcn/ui is Tailwind-based, so recommend it for React + Tailwind

---

## Detection Algorithm

### Step 1: Parse Framework Requirements from spec.md

```text
FUNCTION detect_from_spec(spec_content):

  # Look for Framework Requirements table
  table = find_table_section(spec_content, "Framework Requirements")

  IF table NOT found:
    RETURN null

  # Parse table rows for UI framework indicators
  FOR row IN table.rows:
    framework = row["Framework"].lower()

    IF "react" IN framework:
      IF "typescript" IN framework OR "tsx" IN spec_content:
        RETURN "react-ts"
      RETURN "react"

    IF "next" IN framework OR "nextjs" IN framework:
      RETURN "react-ts"  # Next.js implies React + TS

    IF "vue" IN framework OR "nuxt" IN framework:
      RETURN "vue"

    IF "angular" IN framework:
      RETURN "angular"

    IF "svelte" IN framework OR "sveltekit" IN framework:
      RETURN "svelte"

  RETURN null
```

### Step 2: Parse Technology Constraints from constitution.md

```text
FUNCTION detect_from_constitution(constitution_content):

  # Look for Technology Constraints table
  table = find_table_section(constitution_content, "Technology Constraints")

  IF table NOT found:
    RETURN null

  # Find UI Framework row
  ui_framework_row = find_row(table, "UI Framework")

  IF ui_framework_row:
    value = ui_framework_row["Decision"].lower()

    IF "react" IN value:
      IF "typescript" IN value OR "ts" IN value:
        RETURN "react-ts"
      RETURN "react"

    IF "vue" IN value:
      RETURN "vue"

    IF "angular" IN value:
      RETURN "angular"

    IF "svelte" IN value:
      RETURN "svelte"

    IF "none" IN value OR value == "-" OR value == "[none]":
      RETURN "none"

  RETURN null
```

### Step 3: Combine Detection Results

```text
FUNCTION detect_ui_framework(spec_content, constitution_content):

  # Priority: constitution.md > spec.md
  # (constitution is project-level config, more authoritative)

  from_constitution = detect_from_constitution(constitution_content)
  from_spec = detect_from_spec(spec_content)

  IF from_constitution == "none":
    RETURN "none"  # Explicitly no UI framework

  IF from_constitution != null:
    RETURN from_constitution

  IF from_spec != null:
    RETURN from_spec

  RETURN "unknown"
```

---

## Recommendation Logic

### Core Algorithm

```text
FUNCTION recommend_library(ui_framework, domain, wcag_level, project_type):

  # 1. Base recommendations by framework
  SWITCH ui_framework:

    CASE "react-ts":
      primary = "shadcn/ui"
      alternatives = ["mui", "radix-ui", "headless-ui"]
      reasoning = "Modern headless components with full TypeScript support, accessibility-first, zero runtime overhead"

    CASE "react":
      primary = "mui"
      alternatives = ["shadcn/ui", "chakra-ui", "bootstrap"]
      reasoning = "Comprehensive component library with strong community, enterprise-ready, good docs"

    CASE "vue":
      primary = "vuetify"
      alternatives = ["primevue", "quasar", "bootstrap-vue"]
      reasoning = "Material Design for Vue with excellent TypeScript support and rich component set"

    CASE "angular":
      primary = "angular-material"
      alternatives = ["primeng", "ng-bootstrap", "taiga-ui"]
      reasoning = "Official Angular component library with tight framework integration and built-in a11y"

    CASE "svelte":
      primary = "skeleton-ui"
      alternatives = ["svelte-material-ui", "carbon-svelte"]
      reasoning = "Svelte-native design system built on Tailwind, lightweight and performant"

    CASE "none":
      RETURN {
        skip: true,
        message: "No UI framework detected - backend-only project or manual selection required"
      }

    DEFAULT:
      RETURN {
        skip: true,
        message: "Unknown UI framework - please set UI Framework in Technology Constraints"
      }

  # 2. Apply domain modifiers
  IF domain != null:
    recommendations = apply_domain_modifier(primary, alternatives, domain)
    primary = recommendations.primary
    alternatives = recommendations.alternatives

  # 3. Apply WCAG modifiers
  IF wcag_level == "AAA":
    filter_accessible_first([primary] + alternatives)

  # 4. Apply project type modifiers
  IF project_type == "mvp" OR project_type == "prototype":
    # Prefer simpler setup
    IF "tailwind" NOT IN alternatives:
      alternatives.append("tailwind")

  RETURN {
    primary: primary,
    alternatives: alternatives,
    preset_key: get_preset_key(primary),
    reasoning: reasoning,
    skip: false
  }
```

### Domain Modifiers

```text
FUNCTION apply_domain_modifier(primary, alternatives, domain):

  SWITCH domain:

    CASE "uxq":
      # B2C, rich UX, delight-focused
      # Prefer libraries with animation support, rich interactions
      prefer_order = ["shadcn/ui", "mui", "vuetify", "chakra-ui"]

    CASE "saas":
      # B2B, productivity, data-dense UIs
      # Prefer libraries with tables, forms, dashboards
      prefer_order = ["mui", "angular-material", "primevue", "primeng"]

    CASE "fintech":
      # Compliance-heavy, accessibility critical
      # Prefer mature, well-audited libraries
      prefer_order = ["mui", "angular-material", "shadcn/ui"]

    CASE "healthcare":
      # HIPAA considerations, accessibility mandatory
      # Prefer libraries with strong a11y track record
      prefer_order = ["angular-material", "mui", "shadcn/ui"]

    CASE "e-commerce":
      # Conversion-focused, mobile-first
      # Prefer responsive, performant libraries
      prefer_order = ["shadcn/ui", "chakra-ui", "tailwind"]

    DEFAULT:
      RETURN { primary: primary, alternatives: alternatives }

  # Reorder based on domain preference
  IF primary IN prefer_order:
    new_primary = prefer_order[0] IF prefer_order[0] IN ([primary] + alternatives) ELSE primary
  ELSE:
    new_primary = primary

  RETURN { primary: new_primary, alternatives: alternatives }
```

### WCAG Level Modifiers

```text
FUNCTION filter_accessible_first(libraries):

  # Libraries with strong accessibility track record
  # Based on a11y audit scores, VPAT availability, community feedback

  a11y_tier_1 = ["angular-material", "shadcn/ui", "mui", "radix-ui"]
  a11y_tier_2 = ["vuetify", "chakra-ui", "headless-ui"]
  a11y_tier_3 = ["bootstrap", "skeleton-ui", "tailwind"]

  # For AAA compliance, prefer tier 1
  filtered = []
  FOR lib IN libraries:
    IF lib IN a11y_tier_1:
      filtered.insert(0, lib)
    ELIF lib IN a11y_tier_2:
      filtered.append(lib)
    # Tier 3 excluded for AAA requirements

  RETURN filtered IF filtered.length > 0 ELSE libraries
```

---

## Preset Application Flow

### Step 1: Match Recommendation to Preset

```text
FUNCTION get_preset_key(library_name):

  preset_mapping = {
    "shadcn/ui": "shadcn/ui",
    "mui": "mui",
    "vuetify": "vuetify",
    "angular-material": "angular-material",
    "skeleton-ui": "skeleton-ui",
    "tailwind": "tailwind",
    "bootstrap": "bootstrap",
    "chakra-ui": "mui",        # Similar tokens to MUI
    "radix-ui": "shadcn/ui",   # shadcn is built on Radix
    "headless-ui": "tailwind"  # Pairs with Tailwind tokens
  }

  RETURN preset_mapping.get(library_name, "none")
```

### Step 2: Load Preset Tokens

```text
FUNCTION load_preset(preset_key):

  # Read templates/shared/design-system-presets.md
  presets_content = read_file("templates/shared/design-system-presets.md")

  # Parse YAML block for specified preset
  preset_yaml = extract_yaml_block(presets_content, preset_key)

  IF preset_yaml == null:
    RETURN { error: "Preset not found: " + preset_key }

  RETURN preset_yaml
```

### Step 3: Generate Constitution Update

```text
FUNCTION generate_constitution_diff(current_design_system, new_preset):

  # Generate diff showing what will change
  diff = {
    framework: {
      old: current_design_system.framework,
      new: new_preset.framework
    },
    theme: {
      colors: compare_objects(
        current_design_system.theme.colors,
        new_preset.theme.colors
      ),
      typography: compare_objects(
        current_design_system.theme.typography,
        new_preset.theme.typography
      )
    },
    component_library_url: {
      old: current_design_system.component_library_url,
      new: new_preset.component_library_url
    }
  }

  RETURN diff
```

### Step 4: Apply After Confirmation

```text
FUNCTION apply_preset(constitution_path, preset_key):

  # 1. Load preset tokens
  preset = load_preset(preset_key)

  # 2. Read current constitution
  constitution = read_file(constitution_path)

  # 3. Replace design_system YAML block
  updated_constitution = replace_yaml_block(
    constitution,
    "design_system",
    preset
  )

  # 4. Write updated constitution
  write_file(constitution_path, updated_constitution)

  RETURN { success: true, preset_applied: preset_key }
```

---

## Output Format

### Recommendation Summary

When presenting recommendations to the user:

```markdown
## Component Library Recommendation

**Detected Framework**: React 18 with TypeScript
**Source**: spec.md → Framework Requirements table

### Primary Recommendation: shadcn/ui

**Reasoning**: Modern headless components with full TypeScript support, accessibility-first, zero runtime overhead

**Preset Available**: Yes (`shadcn/ui` in design-system-presets.md)

### Alternatives

| Library | Pros | Cons |
|---------|------|------|
| MUI | Comprehensive, enterprise-ready | Larger bundle, Material Design only |
| Radix UI | Headless, unstyled primitives | Requires more styling work |
| Headless UI | Tailwind-native, lightweight | Fewer components |

### Apply Preset?

To apply the shadcn/ui preset to your constitution.md:
- Framework: `shadcn/ui`
- Primary color: `#18181B` (zinc-950)
- Component URL: https://ui.shadcn.com/docs/components

[Apply Preset] [Choose Alternative] [Skip]
```

### Skip Message

When no recommendation can be made:

```markdown
## Component Library Recommendation

**Status**: Skipped

**Reason**: [one of:]
- No UI framework detected in spec.md or constitution.md
- UI Framework explicitly set to "None" in Technology Constraints
- Design system framework already configured (not "none")
- Backend-only project detected

**To enable recommendations**:
1. Add UI Framework to Technology Constraints in constitution.md
2. Or add Framework Requirements to spec.md with React/Vue/Angular/Svelte
```

---

## Skip Conditions

Component Library Recommendations are skipped when:

1. **Already Configured**: `design_system.framework` in constitution.md is not `"none"`
2. **Explicitly Disabled**: UI Framework in Technology Constraints is `"None"`
3. **No UI Framework**: Neither spec.md nor constitution.md specify a UI framework
4. **Backend Project**: No frontend-related entries in Framework Requirements
5. **Flag Passed**: `--no-recommendation` flag passed to `/speckit.design`

When skipped, Step 0.75 in design.md outputs "Skipped: [reason]" and continues to Step 1.

---

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| Wrong framework detected | Ambiguous spec.md entries | Explicitly set UI Framework in constitution.md Technology Constraints |
| Preset not found | Library not in presets | Add custom preset to design-system-presets.md or use closest match |
| Recommendation ignored | User declined or skipped | Manually set design_system.framework in constitution.md |
| TypeScript not detected | Missing tsx/ts indicators | Add "TypeScript" to Framework Requirements or use `react-ts` explicitly |
| Domain modifier wrong | Domain layer not loaded | Set Domain Layer in constitution.md header |

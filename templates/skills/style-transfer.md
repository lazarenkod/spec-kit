# Style Transfer Skill

## Purpose

Migrate design specifications from one aesthetic preset to another while preserving functional requirements. Automates the tedious process of remapping design tokens, updating component specifications, and maintaining visual consistency during a rebrand or design system migration.

## When to Use

- **Rebranding**: Company rebrand requires new visual identity
- **Design System Migration**: Moving from one design language to another (e.g., Material → Tailwind UI)
- **Aesthetic Exploration**: Testing different visual styles on the same feature
- **Multi-Brand Products**: Adapt a feature for different brand variants

## Supported Transfers

All pairwise combinations of the 9 aesthetic presets:
- **linear** → stripe, vercel, notion, apple, airbnb, github, slack, figma
- **stripe** → linear, vercel, notion, apple, airbnb, github, slack, figma
- **vercel** → linear, stripe, notion, apple, airbnb, github, slack, figma
- (and so on for all 36 combinations)

## Prerequisites

- Existing `design.md` with source aesthetic preset tokens
- Target aesthetic preset defined in `templates/shared/design-aesthetic-presets.md`
- No uncommitted changes (style transfer modifies design.md)

---

## Style Transfer Pipeline

### FUNCTION style_transfer_pipeline(source_preset, target_preset)

#### Step 1: Extract Current Tokens

```text
FUNCTION extract_current_tokens(design_md_path):
  """Extract all design tokens from current design.md"""

  design_content = READ design_md_path

  # Parse color tokens
  colors = EXTRACT_SECTION(design_content, "## Colors")
  parsed_colors = {
    "primary": PARSE_COLOR(colors, "primary"),
    "secondary": PARSE_COLOR(colors, "secondary"),
    "accent": PARSE_COLOR(colors, "accent"),
    "background": PARSE_COLOR(colors, "background"),
    "foreground": PARSE_COLOR(colors, "foreground"),
    "muted": PARSE_COLOR(colors, "muted"),
    "border": PARSE_COLOR(colors, "border"),
    "success": PARSE_COLOR(colors, "success"),
    "warning": PARSE_COLOR(colors, "warning"),
    "error": PARSE_COLOR(colors, "error"),
  }

  # Parse typography tokens
  typography = EXTRACT_SECTION(design_content, "## Typography")
  parsed_typography = {
    "font_family": PARSE_FONT(typography, "font-family"),
    "font_sizes": PARSE_SCALE(typography, "font-size"),
    "font_weights": PARSE_SCALE(typography, "font-weight"),
    "line_heights": PARSE_SCALE(typography, "line-height"),
    "letter_spacing": PARSE_SCALE(typography, "letter-spacing"),
  }

  # Parse spacing tokens
  spacing = EXTRACT_SECTION(design_content, "## Spacing")
  parsed_spacing = PARSE_SCALE(spacing, "spacing")

  # Parse component tokens
  components = EXTRACT_SECTION(design_content, "## Components")
  parsed_components = {
    "border_radius": PARSE_COMPONENT_TOKEN(components, "border-radius"),
    "border_width": PARSE_COMPONENT_TOKEN(components, "border-width"),
    "shadow": PARSE_COMPONENT_TOKEN(components, "shadow"),
  }

  RETURN {
    "colors": parsed_colors,
    "typography": parsed_typography,
    "spacing": parsed_spacing,
    "components": parsed_components,
  }
```

#### Step 2: Load Preset Definitions

```text
FUNCTION load_preset_definitions(source_preset, target_preset):
  """Load token definitions for source and target presets"""

  presets_file = "templates/shared/design-aesthetic-presets.md"
  presets_content = READ presets_file

  # Extract source preset tokens
  source_section = EXTRACT_PRESET_SECTION(presets_content, source_preset)
  source_tokens = PARSE_PRESET_TOKENS(source_section)

  # Extract target preset tokens
  target_section = EXTRACT_PRESET_SECTION(presets_content, target_preset)
  target_tokens = PARSE_PRESET_TOKENS(target_section)

  RETURN {
    "source": source_tokens,
    "target": target_tokens,
  }
```

#### Step 3: Build Transformation Matrix

```text
FUNCTION build_transformation_matrix(current_tokens, preset_definitions):
  """Create mapping from current tokens to target tokens"""

  source_tokens = preset_definitions.source
  target_tokens = preset_definitions.target

  # Map colors
  color_mapping = {}
  FOR EACH color_name, current_value IN current_tokens.colors:
    # Find closest match in source preset
    source_match = FIND_CLOSEST_COLOR(current_value, source_tokens.colors)

    # Map to corresponding target token
    target_value = target_tokens.colors[source_match.name]

    color_mapping[color_name] = {
      "current": current_value,
      "source_preset_match": source_match.name,
      "target_value": target_value,
      "change_type": CLASSIFY_CHANGE(current_value, target_value),
    }

  # Map typography
  typography_mapping = {
    "font_family": {
      "current": current_tokens.typography.font_family,
      "target": target_tokens.typography.font_family,
      "change_type": "font_change" IF different ELSE "no_change",
    },
    "font_sizes": MAP_SCALE(
      current_tokens.typography.font_sizes,
      target_tokens.typography.font_sizes
    ),
    "font_weights": MAP_SCALE(
      current_tokens.typography.font_weights,
      target_tokens.typography.font_weights
    ),
  }

  # Map spacing
  spacing_mapping = MAP_SCALE(
    current_tokens.spacing,
    target_tokens.spacing
  )

  # Map component tokens
  component_mapping = {
    "border_radius": {
      "current": current_tokens.components.border_radius,
      "target": target_tokens.components.border_radius,
      "change_type": CLASSIFY_RADIUS_CHANGE(
        current_tokens.components.border_radius,
        target_tokens.components.border_radius
      ),
    },
    "shadow": {
      "current": current_tokens.components.shadow,
      "target": target_tokens.components.shadow,
      "change_type": "shadow_change",
    },
  }

  RETURN {
    "colors": color_mapping,
    "typography": typography_mapping,
    "spacing": spacing_mapping,
    "components": component_mapping,
  }
```

#### Step 4: Generate Diff Report

```text
FUNCTION generate_diff_report(transformation_matrix, source_preset, target_preset):
  """Create human-readable diff showing all changes"""

  report = f"""
# Style Transfer Diff Report

## Transfer Details
- Source Preset: {source_preset}
- Target Preset: {target_preset}
- Generated: {TIMESTAMP()}

---

## Color Changes

"""

  FOR EACH color_name, mapping IN transformation_matrix.colors:
    change_icon = "🔄" IF mapping.change_type != "no_change" ELSE "✓"

    report += f"""
### {color_name}
{change_icon} **Change Type**: {mapping.change_type}
- **Current**: {mapping.current}
- **Source Match**: {mapping.source_preset_match}
- **Target**: {mapping.target_value}

"""

  report += """
---

## Typography Changes

"""

  # Font family change
  IF transformation_matrix.typography.font_family.change_type == "font_change":
    report += f"""
### Font Family
🔄 **Font Change**
- **Current**: {transformation_matrix.typography.font_family.current}
- **Target**: {transformation_matrix.typography.font_family.target}

"""

  # Font size scale changes
  report += """
### Font Size Scale
"""
  FOR EACH size_name, mapping IN transformation_matrix.typography.font_sizes:
    report += f"- **{size_name}**: {mapping.current} → {mapping.target}\n"

  report += """
---

## Spacing Changes

"""
  FOR EACH spacing_name, mapping IN transformation_matrix.spacing:
    report += f"- **{spacing_name}**: {mapping.current} → {mapping.target}\n"

  report += """
---

## Component Token Changes

"""

  # Border radius
  report += f"""
### Border Radius
{mapping.change_type}
- **Current**: {transformation_matrix.components.border_radius.current}
- **Target**: {transformation_matrix.components.border_radius.target}

"""

  # Shadow
  report += f"""
### Shadow/Elevation
- **Current**: {transformation_matrix.components.shadow.current}
- **Target**: {transformation_matrix.components.shadow.target}

"""

  report += """
---

## Summary

"""

  # Count changes
  color_changes = COUNT(transformation_matrix.colors WHERE change_type != "no_change")
  typography_changes = COUNT_TYPOGRAPHY_CHANGES(transformation_matrix.typography)
  component_changes = COUNT_COMPONENT_CHANGES(transformation_matrix.components)

  total_changes = color_changes + typography_changes + component_changes

  report += f"""
- **Total Changes**: {total_changes}
- **Color Changes**: {color_changes}
- **Typography Changes**: {typography_changes}
- **Component Changes**: {component_changes}

## Impact Assessment

"""

  # Assess impact
  IF total_changes > 20:
    report += "⚠️ **HIGH IMPACT**: Significant visual changes expected. Review carefully.\n"
  ELIF total_changes > 10:
    report += "⚠️ **MODERATE IMPACT**: Noticeable visual changes.\n"
  ELSE:
    report += "✓ **LOW IMPACT**: Minor visual adjustments.\n"

  RETURN report
```

#### Step 5: User Confirmation

```text
FUNCTION request_user_confirmation(diff_report):
  """Show diff and ask for user approval"""

  # Write diff to file
  diff_path = ".speckit/style-transfer-diff.md"
  WRITE diff_path, diff_report

  # Display to user
  PRINT """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Style Transfer Preview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A diff report has been generated at:
  {diff_path}

Review the changes and confirm to proceed.

"""

  PRINT diff_report

  response = PROMPT_USER("""
Do you want to apply these changes? (yes/no)
> """)

  IF response.lower() IN ["yes", "y"]:
    RETURN true
  ELSE:
    PRINT "Style transfer cancelled. No changes made."
    RETURN false
```

#### Step 6: Apply Transformation

```text
FUNCTION apply_transformation(transformation_matrix, design_md_path):
  """Apply token changes to design.md"""

  design_content = READ design_md_path

  # Create backup
  backup_path = f"{design_md_path}.backup.{TIMESTAMP()}"
  WRITE backup_path, design_content
  PRINT f"Backup created at: {backup_path}"

  # Apply color changes
  FOR EACH color_name, mapping IN transformation_matrix.colors:
    design_content = REPLACE_TOKEN(
      design_content,
      section="Colors",
      token_name=color_name,
      old_value=mapping.current,
      new_value=mapping.target_value
    )

  # Apply typography changes
  design_content = REPLACE_TOKEN(
    design_content,
    section="Typography",
    token_name="font-family",
    old_value=transformation_matrix.typography.font_family.current,
    new_value=transformation_matrix.typography.font_family.target
  )

  FOR EACH size_name, mapping IN transformation_matrix.typography.font_sizes:
    design_content = REPLACE_TOKEN(
      design_content,
      section="Typography",
      token_name=size_name,
      old_value=mapping.current,
      new_value=mapping.target
    )

  # Apply spacing changes
  FOR EACH spacing_name, mapping IN transformation_matrix.spacing:
    design_content = REPLACE_TOKEN(
      design_content,
      section="Spacing",
      token_name=spacing_name,
      old_value=mapping.current,
      new_value=mapping.target
    )

  # Apply component token changes
  design_content = REPLACE_TOKEN(
    design_content,
    section="Components",
    token_name="border-radius",
    old_value=transformation_matrix.components.border_radius.current,
    new_value=transformation_matrix.components.border_radius.target
  )

  design_content = REPLACE_TOKEN(
    design_content,
    section="Components",
    token_name="shadow",
    old_value=transformation_matrix.components.shadow.current,
    new_value=transformation_matrix.components.shadow.target
  )

  # Update aesthetic preset reference
  design_content = UPDATE_METADATA(
    design_content,
    key="aesthetic_preset",
    value=target_preset
  )

  # Write updated design.md
  WRITE design_md_path, design_content

  PRINT f"✓ Style transfer complete. Changes applied to {design_md_path}"
  PRINT f"✓ Backup available at: {backup_path}"
```

#### Step 7: Validation & Preview

```text
FUNCTION validate_and_preview(design_md_path, target_preset):
  """Validate token compliance and generate preview"""

  # Run token compliance validator
  PRINT "Running token compliance validator..."
  validation_result = RUN_VALIDATOR("token-compliance", design_md_path)

  IF validation_result.passed:
    PRINT "✓ Token compliance validation passed"
  ELSE:
    PRINT "⚠️ Token compliance issues detected:"
    FOR EACH issue IN validation_result.issues:
      PRINT f"  - {issue.message}"

  # Offer to generate preview
  response = PROMPT_USER("""
Generate preview with new aesthetic preset? (yes/no)
> """)

  IF response.lower() IN ["yes", "y"]:
    PRINT "Generating preview..."
    RUN_COMMAND("/speckit.preview")
```

---

## Example: Linear → Stripe Transfer

### Input (design.md with Linear preset)

```yaml
aesthetic_preset: linear

colors:
  primary: "#5E6AD2"      # Linear blue
  background: "#FFFFFF"
  foreground: "#000000"
  border: "#E5E7EB"

typography:
  font_family: "Inter, system-ui, sans-serif"
  font_size_base: "16px"

components:
  border_radius: "8px"
  shadow: "0 1px 3px rgba(0,0,0,0.1)"
```

### Transformation Matrix

```json
{
  "colors": {
    "primary": {
      "current": "#5E6AD2",
      "source_preset_match": "linear.primary",
      "target_value": "#635BFF",
      "change_type": "hue_shift"
    },
    "background": {
      "current": "#FFFFFF",
      "target_value": "#FFFFFF",
      "change_type": "no_change"
    }
  },
  "typography": {
    "font_family": {
      "current": "Inter",
      "target": "Inter",
      "change_type": "no_change"
    }
  },
  "components": {
    "border_radius": {
      "current": "8px",
      "target": "6px",
      "change_type": "radius_decrease"
    }
  }
}
```

### Output (design.md with Stripe preset)

```yaml
aesthetic_preset: stripe

colors:
  primary: "#635BFF"      # Stripe purple
  background: "#FFFFFF"
  foreground: "#000000"
  border: "#E5E7EB"

typography:
  font_family: "Inter, system-ui, sans-serif"
  font_size_base: "16px"

components:
  border_radius: "6px"
  shadow: "0 1px 3px rgba(0,0,0,0.1)"
```

---

## Helper Functions

### FUNCTION FIND_CLOSEST_COLOR(target_color, preset_colors)
```text
"""Find closest matching color in preset using perceptual distance"""

target_lab = CONVERT_TO_LAB(target_color)
min_distance = INFINITY
closest_match = null

FOR EACH name, preset_color IN preset_colors:
  preset_lab = CONVERT_TO_LAB(preset_color)
  distance = DELTA_E(target_lab, preset_lab)  # CIE Delta E 2000

  IF distance < min_distance:
    min_distance = distance
    closest_match = { name: name, color: preset_color, distance: distance }

RETURN closest_match
```

### FUNCTION CLASSIFY_CHANGE(current, target)
```text
"""Classify the type of color change"""

current_hsl = CONVERT_TO_HSL(current)
target_hsl = CONVERT_TO_HSL(target)

hue_diff = ABS(current_hsl.h - target_hsl.h)
sat_diff = ABS(current_hsl.s - target_hsl.s)
light_diff = ABS(current_hsl.l - target_hsl.l)

IF hue_diff < 10 AND sat_diff < 0.1 AND light_diff < 0.1:
  RETURN "no_change"
ELIF hue_diff > 30:
  RETURN "hue_shift"
ELIF sat_diff > 0.2:
  RETURN "saturation_change"
ELIF light_diff > 0.2:
  RETURN "lightness_change"
ELSE:
  RETURN "minor_adjustment"
```

---

## Usage

### CLI Command (if integrated)
```bash
# Basic transfer
/speckit.style-transfer --from linear --to stripe

# With auto-confirm (skip diff review)
/speckit.style-transfer --from vercel --to notion --yes

# Dry run (generate diff only, don't apply)
/speckit.style-transfer --from apple --to airbnb --dry-run
```

### Manual Invocation
```text
SWITCH to persona: product-designer-agent
READ templates/skills/style-transfer.md

RUN style_transfer_pipeline(
  source_preset="linear",
  target_preset="stripe",
  design_md_path=".speckit/design.md"
)
```

---

## Error Handling

### Missing Tokens
```text
IF current_tokens missing required tokens:
  PRINT "⚠️ Warning: Some tokens not found in current design.md"
  PRINT "Missing tokens will use target preset defaults"

  FOR EACH missing_token:
    PRINT f"  - {missing_token}: will use {target_tokens[missing_token]}"
```

### Unsupported Preset
```text
IF source_preset NOT IN supported_presets:
  ERROR "Unsupported source preset: {source_preset}"
  PRINT "Supported presets: linear, stripe, vercel, notion, apple, airbnb, github, slack, figma"
  EXIT 1

IF target_preset NOT IN supported_presets:
  ERROR "Unsupported target preset: {target_preset}"
  EXIT 1
```

### Backup Failure
```text
TRY:
  WRITE backup_path, design_content
CATCH IOError:
  ERROR "Failed to create backup. Aborting style transfer."
  EXIT 1
```

---

## Expected Results

- **Execution Time**: 5-10 seconds for token extraction + mapping
- **User Review Time**: 2-5 minutes for diff review
- **Application Time**: <1 second for token replacement
- **Accuracy**: 95%+ token mapping accuracy using perceptual color distance
- **Safety**: Automatic backup before any changes
- **Reversibility**: Can revert using backup or reverse transfer

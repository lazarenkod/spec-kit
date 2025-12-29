# Wireframe Preview Skill

Skill for converting ASCII wireframes from design.md into visual HTML previews.

## Trigger Conditions

Use this skill when:
- design.md contains ASCII wireframes
- Need to visualize layout structure
- Converting text-based wireframes to HTML
- Generating responsive layout previews

## Prerequisites

```yaml
required_files:
  - design.md (with ASCII wireframes)
  - constitution.md (for design tokens)
```

## ASCII Wireframe Patterns

### Layout Detection

```text
PATTERNS:

  # Full-width section
  +----------------------------------+
  |           Content                |
  +----------------------------------+

  # Two-column split
  +-------------+--------------------+
  |  Sidebar    |   Main Content     |
  +-------------+--------------------+

  # Three-column
  +--------+------------+--------+
  |  Left  |   Center   | Right  |
  +--------+------------+--------+

  # Header + content + footer
  +----------------------------------+
  |            Header                |
  +----------------------------------+
  |            Content               |
  +----------------------------------+
  |            Footer                |
  +----------------------------------+

  # Grid items
  +-------+ +-------+ +-------+
  | Card  | | Card  | | Card  |
  +-------+ +-------+ +-------+

  # Nested content
  +----------------------------------+
  |  +----------------------------+  |
  |  |       Nested Box           |  |
  |  +----------------------------+  |
  +----------------------------------+
```

### Component Placeholders

```text
COMPONENT_PATTERNS:

  [Button]           → <button> element
  [Input]            → <input type="text">
  [Search...]        → <input type="search" placeholder="Search...">
  [Dropdown ▼]       → <select> element
  [✓ Checkbox]       → <input type="checkbox" checked>
  [○ Radio]          → <input type="radio">
  [Avatar]           → <div class="avatar">
  [Image]            → <img> placeholder
  [Icon: home]       → <svg> icon
  [Logo]             → <div class="logo">
  [Nav: Home|About]  → <nav> with links
  [...loading...]    → <div class="skeleton">
  [● ● ●]            → Pagination dots
  [< Prev] [Next >]  → Pagination buttons
```

### Content Placeholders

```text
CONTENT_PATTERNS:

  # Title text (all caps or Title Case)
  PAGE TITLE          → <h1>
  Section Title       → <h2>
  Subsection          → <h3>

  # Body text
  Lorem ipsum...      → <p> with placeholder text
  ---                 → <hr> divider
  • Item              → <li> in <ul>
  1. Item             → <li> in <ol>

  # Labels
  Label:              → <label>
  *Required           → Required field indicator
```

## Parsing Pipeline

### 1. Extract Wireframes from design.md

```text
FUNCTION extract_wireframes(design_md):

  wireframes = []

  # Find wireframe sections (code blocks with ASCII art)
  code_blocks = extract_code_blocks(design_md, language="")

  FOR block IN code_blocks:
    IF looks_like_wireframe(block):
      # Get preceding header for name
      name = get_preceding_header(block)
      wireframes.append({
        name: name,
        content: block,
        context: get_surrounding_context(block)
      })

  # Also check for indented wireframes
  indented_sections = extract_indented_blocks(design_md)

  FOR section IN indented_sections:
    IF looks_like_wireframe(section):
      wireframes.append({
        name: infer_name(section),
        content: section,
        context: ""
      })

  RETURN wireframes


FUNCTION looks_like_wireframe(text):

  # Check for box-drawing characters
  box_chars = ['+', '-', '|', '─', '│', '┌', '┐', '└', '┘', '├', '┤']

  char_count = sum(1 FOR c IN text IF c IN box_chars)

  # If more than 10% are box characters, likely wireframe
  IF char_count / len(text) > 0.1:
    RETURN true

  # Check for bracket placeholders
  IF "[" IN text AND "]" IN text:
    brackets = count_brackets(text)
    IF brackets > 2:
      RETURN true

  RETURN false
```

### 2. Parse Wireframe Structure

```text
FUNCTION parse_wireframe(wireframe_text):

  lines = wireframe_text.split("\n")

  # Identify structure
  structure = {
    type: null,      # "single", "columns", "grid", "nested"
    regions: [],     # Named regions
    components: [],  # Component placeholders
    layout: null     # CSS grid/flex specification
  }

  # Detect column splits
  column_lines = find_column_separators(lines)

  IF column_lines:
    structure.type = "columns"
    structure.regions = parse_columns(lines, column_lines)
  ELSE:
    # Check for grid pattern
    IF looks_like_grid(lines):
      structure.type = "grid"
      structure.regions = parse_grid(lines)
    ELSE:
      structure.type = "single"
      structure.regions = [parse_single_region(lines)]

  # Extract components from all regions
  FOR region IN structure.regions:
    components = extract_components(region.content)
    structure.components.extend(components)

  RETURN structure


FUNCTION find_column_separators(lines):

  # Find vertical bars that span multiple lines
  separators = []

  FOR col IN range(max_line_length(lines)):
    is_separator = true
    separator_positions = []

    FOR line IN lines:
      IF col < len(line):
        char = line[col]
        IF char == '|' OR char == '│':
          separator_positions.append(line_number)
        ELIF char NOT IN [' ', '+', '-']:
          is_separator = false
          BREAK

    IF is_separator AND len(separator_positions) > 2:
      separators.append(col)

  RETURN separators


FUNCTION parse_columns(lines, separators):

  columns = []
  prev_sep = 0

  FOR sep IN separators:
    column_content = extract_column_content(lines, prev_sep, sep)

    IF column_content.strip():
      columns.append({
        name: infer_region_name(column_content),
        content: column_content,
        width: sep - prev_sep
      })

    prev_sep = sep + 1

  # Last column
  last_content = extract_column_content(lines, prev_sep, -1)
  IF last_content.strip():
    columns.append({
      name: infer_region_name(last_content),
      content: last_content,
      width: "auto"
    })

  RETURN columns


FUNCTION infer_region_name(content):

  # Check for explicit region label
  label_patterns = [
    r'\[(\w+)\s*-\s*.*\]',  # [Header - Navigation]
    r'\[(\w+)\]',           # [Sidebar]
    r'^(\w+):',             # Header:
  ]

  FOR pattern IN label_patterns:
    match = regex_search(pattern, content)
    IF match:
      RETURN match.group(1).lower()

  # Infer from position and content
  IF "nav" IN content.lower() OR "menu" IN content.lower():
    RETURN "nav"
  IF "header" IN content.lower() OR "logo" IN content.lower():
    RETURN "header"
  IF "footer" IN content.lower() OR "copyright" IN content.lower():
    RETURN "footer"
  IF "sidebar" IN content.lower():
    RETURN "sidebar"

  RETURN "content"
```

### 3. Extract Components

```text
FUNCTION extract_components(region_content):

  components = []

  # Find bracketed placeholders
  bracket_pattern = r'\[([^\]]+)\]'
  matches = regex_find_all(bracket_pattern, region_content)

  FOR match IN matches:
    component = parse_component_placeholder(match)
    components.append(component)

  RETURN components


FUNCTION parse_component_placeholder(placeholder):

  text = placeholder.strip()

  # Button patterns
  IF text.startswith("Button") OR text.endswith("Button"):
    RETURN {
      type: "button",
      label: extract_label(text),
      variant: infer_variant(text)
    }

  # Input patterns
  IF "..." IN text OR text.startswith("Input") OR text.startswith("Search"):
    RETURN {
      type: "input",
      placeholder: text.replace("...", "").strip(),
      input_type: "search" IF "search" IN text.lower() ELSE "text"
    }

  # Dropdown
  IF "▼" IN text OR text.startswith("Dropdown") OR text.startswith("Select"):
    RETURN {
      type: "select",
      label: text.replace("▼", "").strip()
    }

  # Checkbox
  IF "✓" IN text OR "☑" IN text OR text.startswith("Checkbox"):
    RETURN {
      type: "checkbox",
      label: text.replace("✓", "").replace("☑", "").strip(),
      checked: "✓" IN text OR "☑" IN text
    }

  # Radio
  IF "○" IN text OR "●" IN text OR text.startswith("Radio"):
    RETURN {
      type: "radio",
      label: text.replace("○", "").replace("●", "").strip(),
      checked: "●" IN text
    }

  # Image/Avatar
  IF text IN ["Image", "Avatar", "Photo", "Picture"]:
    RETURN {
      type: "image",
      variant: text.lower()
    }

  # Icon
  IF text.startswith("Icon:"):
    icon_name = text.replace("Icon:", "").strip()
    RETURN {
      type: "icon",
      name: icon_name
    }

  # Navigation
  IF text.startswith("Nav:"):
    items = text.replace("Nav:", "").split("|")
    RETURN {
      type: "nav",
      items: [i.strip() FOR i IN items]
    }

  # Loading state
  IF "loading" IN text.lower() OR text == "...":
    RETURN {
      type: "skeleton",
      shape: "text"
    }

  # Default: treat as text/label
  RETURN {
    type: "text",
    content: text
  }
```

### 4. Generate HTML

```text
FUNCTION generate_html(structure, tokens):

  html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
{css_reset}
{css_variables}
{layout_css}
{component_css}
  </style>
</head>
<body>
  <div class="wireframe-container">
{body_content}
  </div>
</body>
</html>
"""

  # Generate CSS variables from tokens
  css_variables = generate_css_variables(tokens)

  # Generate layout CSS
  layout_css = generate_layout_css(structure)

  # Generate component CSS
  component_css = generate_component_css(structure.components)

  # Generate body content
  body_content = generate_body_content(structure)

  html = html.replace("{title}", structure.name OR "Wireframe Preview")
  html = html.replace("{css_reset}", CSS_RESET)
  html = html.replace("{css_variables}", css_variables)
  html = html.replace("{layout_css}", layout_css)
  html = html.replace("{component_css}", component_css)
  html = html.replace("{body_content}", body_content)

  RETURN html


FUNCTION generate_css_variables(tokens):

  css = ":root {\n"

  # Colors
  IF tokens.colors:
    FOR name, value IN tokens.colors:
      css += f"  --{name}: {value};\n"

  # Spacing
  css += f"  --spacing-unit: {tokens.spacing.unit OR '4px'};\n"

  # Typography
  IF tokens.typography:
    css += f"  --font-family: {tokens.typography.font_family};\n"
    css += f"  --font-size-base: {tokens.typography.scale.base};\n"

  # Radii
  IF tokens.radii:
    FOR name, value IN tokens.radii:
      css += f"  --radius-{name}: {value};\n"

  css += "}\n"

  RETURN css


FUNCTION generate_layout_css(structure):

  IF structure.type == "columns":
    # Calculate column widths
    total_width = sum(r.width FOR r IN structure.regions IF r.width != "auto")
    column_widths = []

    FOR region IN structure.regions:
      IF region.width == "auto":
        column_widths.append("1fr")
      ELSE:
        fraction = region.width / total_width
        column_widths.append(f"{fraction:.2f}fr")

    css = f"""
.wireframe-container {{
  display: grid;
  grid-template-columns: {' '.join(column_widths)};
  min-height: 100vh;
  gap: var(--spacing-unit);
}}
"""

  ELIF structure.type == "grid":
    css = """
.wireframe-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: calc(var(--spacing-unit) * 4);
  padding: calc(var(--spacing-unit) * 4);
}
"""

  ELSE:
    css = """
.wireframe-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
"""

  # Add region-specific styles
  FOR i, region IN enumerate(structure.regions):
    region_class = f".region-{region.name OR i}"
    css += f"""
{region_class} {{
  padding: calc(var(--spacing-unit) * 4);
  background: var(--background);
  border: 1px dashed var(--border);
}}
"""

  RETURN css


FUNCTION generate_body_content(structure):

  content = ""

  FOR i, region IN enumerate(structure.regions):
    region_class = f"region-{region.name OR i}"

    content += f'  <section class="{region_class}">\n'

    # Add region label
    IF region.name:
      content += f'    <div class="region-label">{region.name}</div>\n'

    # Render components
    FOR component IN extract_components(region.content):
      component_html = render_component(component)
      content += f'    {component_html}\n'

    content += '  </section>\n'

  RETURN content


FUNCTION render_component(component):

  IF component.type == "button":
    variant_class = f"btn-{component.variant}" IF component.variant ELSE ""
    RETURN f'<button class="btn {variant_class}">{component.label OR "Button"}</button>'

  IF component.type == "input":
    RETURN f'<input type="{component.input_type}" placeholder="{component.placeholder}" class="input">'

  IF component.type == "select":
    RETURN f'''<select class="select">
      <option>{component.label OR "Select..."}</option>
    </select>'''

  IF component.type == "checkbox":
    checked = "checked" IF component.checked ELSE ""
    RETURN f'''<label class="checkbox">
      <input type="checkbox" {checked}>
      <span>{component.label OR "Checkbox"}</span>
    </label>'''

  IF component.type == "radio":
    checked = "checked" IF component.checked ELSE ""
    RETURN f'''<label class="radio">
      <input type="radio" {checked}>
      <span>{component.label OR "Radio"}</span>
    </label>'''

  IF component.type == "image":
    IF component.variant == "avatar":
      RETURN '<div class="avatar"></div>'
    RETURN '<div class="image-placeholder"></div>'

  IF component.type == "icon":
    RETURN f'<span class="icon" data-icon="{component.name}">⬡</span>'

  IF component.type == "nav":
    items = "".join(f'<a href="#">{item}</a>' FOR item IN component.items)
    RETURN f'<nav class="nav">{items}</nav>'

  IF component.type == "skeleton":
    RETURN '<div class="skeleton"></div>'

  IF component.type == "text":
    RETURN f'<span class="text">{component.content}</span>'

  RETURN f'<!-- Unknown component: {component.type} -->'
```

### 5. Generate Component CSS

```text
FUNCTION generate_component_css(components):

  css = """
/* Component Styles */

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: calc(var(--spacing-unit) * 2) calc(var(--spacing-unit) * 4);
  font-size: var(--font-size-base);
  font-weight: 500;
  border-radius: var(--radius-md);
  border: none;
  background: var(--primary);
  color: var(--primary-foreground);
  cursor: pointer;
}

.btn-secondary {
  background: var(--secondary);
  color: var(--secondary-foreground);
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--foreground);
}

.input {
  width: 100%;
  padding: calc(var(--spacing-unit) * 2) calc(var(--spacing-unit) * 3);
  font-size: var(--font-size-base);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  background: var(--background);
}

.select {
  width: 100%;
  padding: calc(var(--spacing-unit) * 2) calc(var(--spacing-unit) * 3);
  font-size: var(--font-size-base);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  background: var(--background);
}

.checkbox, .radio {
  display: flex;
  align-items: center;
  gap: calc(var(--spacing-unit) * 2);
  cursor: pointer;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--muted);
}

.image-placeholder {
  width: 100%;
  height: 200px;
  background: var(--muted);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder::after {
  content: '🖼️';
  font-size: 2rem;
  opacity: 0.5;
}

.icon {
  font-size: 1.25rem;
}

.nav {
  display: flex;
  gap: calc(var(--spacing-unit) * 4);
}

.nav a {
  color: var(--foreground);
  text-decoration: none;
}

.nav a:hover {
  color: var(--primary);
}

.skeleton {
  height: 1em;
  background: linear-gradient(
    90deg,
    var(--muted) 25%,
    var(--muted-foreground) 50%,
    var(--muted) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.region-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted-foreground);
  margin-bottom: calc(var(--spacing-unit) * 2);
}

.text {
  color: var(--foreground);
}
"""

  RETURN css
```

## Complete Pipeline

```text
FUNCTION wireframe_preview_pipeline(wireframe_name = null):

  # 1. Load context
  design_md = read("design.md")
  constitution = read("constitution.md")
  tokens = extract_design_tokens(constitution)

  # 2. Extract wireframes
  all_wireframes = extract_wireframes(design_md)

  IF wireframe_name:
    wireframes = [w FOR w IN all_wireframes IF w.name == wireframe_name]
  ELSE:
    wireframes = all_wireframes

  IF NOT wireframes:
    LOG "No wireframes found in design.md"
    RETURN null

  # 3. Generate previews
  results = []

  FOR wireframe IN wireframes:
    # Parse structure
    structure = parse_wireframe(wireframe.content)
    structure.name = wireframe.name

    # Generate HTML
    html = generate_html(structure, tokens)

    # Save file
    output_path = f".preview/wireframes/{kebab_case(wireframe.name)}.html"
    write(output_path, html)

    results.append({
      name: wireframe.name,
      file: output_path,
      regions: len(structure.regions),
      components: len(structure.components)
    })

  # 4. Generate index
  index_html = generate_wireframe_index(results)
  write(".preview/wireframes/index.html", index_html)

  RETURN {
    wireframes: results,
    index: ".preview/wireframes/index.html"
  }


FUNCTION generate_wireframe_index(wireframes):

  html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Wireframe Index</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      padding: 2rem;
      max-width: 800px;
      margin: 0 auto;
    }
    h1 { margin-bottom: 2rem; }
    .wireframe-list {
      display: grid;
      gap: 1rem;
    }
    .wireframe-card {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: #f5f5f5;
      border-radius: 8px;
    }
    .wireframe-card a {
      color: #3b82f6;
      text-decoration: none;
      font-weight: 500;
    }
    .wireframe-card a:hover {
      text-decoration: underline;
    }
    .stats {
      color: #666;
      font-size: 0.875rem;
    }
  </style>
</head>
<body>
  <h1>Wireframe Previews</h1>
  <div class="wireframe-list">
"""

  FOR wf IN wireframes:
    html += f'''
    <div class="wireframe-card">
      <a href="{kebab_case(wf.name)}.html">{wf.name}</a>
      <span class="stats">{wf.regions} regions, {wf.components} components</span>
    </div>
'''

  html += """
  </div>
</body>
</html>
"""

  RETURN html
```

## CSS Reset

```text
CSS_RESET = """
*, *::before, *::after {
  box-sizing: border-box;
}

* {
  margin: 0;
}

body {
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  font-family: var(--font-family, system-ui, sans-serif);
  background: var(--background, #ffffff);
  color: var(--foreground, #1a1a1a);
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}

input, button, textarea, select {
  font: inherit;
}
"""
```

## Usage Example

```text
# Convert all wireframes from design.md

result = wireframe_preview_pipeline()

# Output:
{
  wireframes: [
    {
      name: "Dashboard",
      file: ".preview/wireframes/dashboard.html",
      regions: 3,
      components: 12
    },
    {
      name: "Profile Page",
      file: ".preview/wireframes/profile-page.html",
      regions: 2,
      components: 8
    }
  ],
  index: ".preview/wireframes/index.html"
}

# Previews available at:
# http://localhost:3456/wireframes/
```

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| component-codegen | Wireframe components → full components |
| v0-generation | Complex wireframe regions → v0 generation |
| motion-generation | Add animations to wireframe elements |

## Responsive Handling

Wireframes are generated with responsive breakpoints:

```css
/* Mobile-first breakpoints */
@media (max-width: 640px) {
  .wireframe-container {
    grid-template-columns: 1fr !important;
  }

  .region-sidebar {
    order: 2;
  }
}

@media (min-width: 1024px) {
  /* Desktop enhancements */
}
```

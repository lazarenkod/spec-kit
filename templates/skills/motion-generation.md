# Motion Generation Skill

Skill for generating animation code from motion specifications in design.md.

## Trigger Conditions

Use this skill when:
- design.md contains motion specifications
- Component requires animations (hover, transitions, loading)
- Page transitions need implementation
- Micro-interactions are specified

## Prerequisites

```yaml
required_files:
  - design.md (with motion specifications)
  - constitution.md (for animation tokens)

optional_files:
  - templates/shared/animation-presets/*.md
```

## Animation Token System

### Default Tokens

```text
DEFAULT_ANIMATION_TOKENS:

  duration:
    instant: "0ms"
    fast: "100ms"
    normal: "200ms"
    slow: "300ms"
    deliberate: "500ms"
    dramatic: "800ms"

  easing:
    linear: "linear"
    ease-out: "cubic-bezier(0, 0, 0.2, 1)"
    ease-in: "cubic-bezier(0.4, 0, 1, 1)"
    ease-in-out: "cubic-bezier(0.4, 0, 0.2, 1)"
    spring: "cubic-bezier(0.175, 0.885, 0.32, 1.275)"
    bounce: "cubic-bezier(0.68, -0.55, 0.265, 1.55)"

  distance:
    xs: "4px"
    sm: "8px"
    md: "16px"
    lg: "24px"
    xl: "48px"

FUNCTION load_animation_tokens(constitution):
  IF constitution.design_system.animation:
    RETURN merge(DEFAULT_ANIMATION_TOKENS, constitution.design_system.animation)
  RETURN DEFAULT_ANIMATION_TOKENS
```

## Generation Pipeline

### 1. Parse Motion Specifications

```text
FUNCTION parse_motion_specs(design_md):

  specs = []

  # Find motion system section
  motion_section = extract_section(design_md, "## Motion System")

  IF motion_section:
    # Parse global tokens
    tokens = parse_yaml_block(motion_section, "Animation Tokens")

    # Parse component animations
    component_anims = extract_all_sections(motion_section, "### ")

    FOR section IN component_anims:
      spec = {
        name: section.title,
        trigger: extract_field(section, "Trigger"),
        duration: extract_field(section, "Duration"),
        easing: extract_field(section, "Easing"),
        properties: extract_list(section, "Properties"),
        keyframes: parse_keyframes(section),
        states: extract_states(section)
      }
      specs.append(spec)

  # Also check component specs for inline animations
  component_sections = extract_all_sections(design_md, "### Component:")

  FOR component IN component_sections:
    IF "animation" IN component.content.lower():
      inline_anims = parse_inline_animations(component)
      specs.extend(inline_anims)

  RETURN specs
```

### 2. Classify Animation Type

```text
FUNCTION classify_animation(spec):

  trigger = spec.trigger.lower()

  IF "hover" IN trigger OR "mouseenter" IN trigger:
    RETURN "hover"
  ELIF "click" IN trigger OR "tap" IN trigger:
    RETURN "click"
  ELIF "focus" IN trigger:
    RETURN "focus"
  ELIF "load" IN trigger OR "mount" IN trigger:
    RETURN "mount"
  ELIF "exit" IN trigger OR "unmount" IN trigger:
    RETURN "unmount"
  ELIF "scroll" IN trigger:
    RETURN "scroll"
  ELIF "state" IN trigger:
    RETURN "state-change"
  ELSE:
    RETURN "custom"
```

### 3. Generate CSS Animation

```text
FUNCTION generate_css_animation(spec, tokens):

  animation_type = classify_animation(spec)

  # Resolve token values
  duration = resolve_token(spec.duration, tokens.duration)
  easing = resolve_token(spec.easing, tokens.easing)

  css = ""

  # Generate keyframes if specified
  IF spec.keyframes:
    css += generate_keyframes(spec.name, spec.keyframes)
    css += "\n\n"

  # Generate class-based animation
  IF animation_type == "hover":
    css += generate_hover_animation(spec, duration, easing)

  ELIF animation_type == "click":
    css += generate_click_animation(spec, duration, easing)

  ELIF animation_type == "focus":
    css += generate_focus_animation(spec, duration, easing)

  ELIF animation_type == "mount":
    css += generate_mount_animation(spec, duration, easing)

  ELSE:
    css += generate_custom_animation(spec, duration, easing)

  # Add reduced motion variant
  css += generate_reduced_motion(spec)

  RETURN css


FUNCTION generate_keyframes(name, keyframes):

  css = f"@keyframes {kebab_case(name)} {{\n"

  FOR frame IN keyframes:
    css += f"  {frame.percent}% {{\n"
    FOR prop, value IN frame.properties:
      css += f"    {prop}: {value};\n"
    css += "  }\n"

  css += "}"

  RETURN css


FUNCTION generate_hover_animation(spec, duration, easing):

  base_class = kebab_case(spec.name)

  css = f"""
.{base_class} {{
  transition: {build_transition_string(spec.properties, duration, easing)};
}}

.{base_class}:hover {{
{build_property_values(spec.states.hover)}
}}
"""

  RETURN css


FUNCTION generate_mount_animation(spec, duration, easing):

  base_class = kebab_case(spec.name)

  css = f"""
.{base_class} {{
  animation: {base_class} {duration} {easing} forwards;
}}

.{base_class}-exit {{
  animation: {base_class}-exit {duration} {easing} forwards;
}}
"""

  RETURN css


FUNCTION generate_reduced_motion(spec):

  base_class = kebab_case(spec.name)

  css = f"""

@media (prefers-reduced-motion: reduce) {{
  .{base_class} {{
    animation: none;
    transition: none;
  }}
}}
"""

  RETURN css
```

### 4. Generate Framer Motion Code

```text
FUNCTION generate_framer_motion(spec, tokens):

  duration = resolve_token(spec.duration, tokens.duration)
  easing = resolve_token(spec.easing, tokens.easing)

  # Convert easing to Framer format
  framer_easing = convert_easing_to_framer(easing)

  # Build variants object
  variants = {}

  IF spec.states:
    FOR state_name, state_props IN spec.states:
      variants[state_name] = convert_to_framer_variant(state_props)

  # Generate component code
  component_name = pascal_case(spec.name)

  code = f"""
import {{ motion }} from 'framer-motion'

const {camel_case(spec.name)}Variants = {{
{format_variants(variants)}
}}

export function {component_name}({{ children, ...props }}) {{
  return (
    <motion.div
      variants={{{camel_case(spec.name)}Variants}}
      initial="{spec.initial_state OR 'initial'}"
      animate="{spec.animate_state OR 'animate'}"
      exit="{spec.exit_state OR 'exit'}"
      transition={{{{
        duration: {parse_duration_to_seconds(duration)},
        ease: {framer_easing},
      }}}}
      {{...props}}
    >
      {{children}}
    </motion.div>
  )
}}
"""

  RETURN code


FUNCTION convert_easing_to_framer(css_easing):

  # Map CSS easing to Framer Motion format
  easing_map = {
    "ease-out": "[0, 0, 0.2, 1]",
    "ease-in": "[0.4, 0, 1, 1]",
    "ease-in-out": "[0.4, 0, 0.2, 1]",
    "linear": "linear",
  }

  # Check if it's a cubic-bezier
  IF css_easing.startswith("cubic-bezier"):
    values = extract_bezier_values(css_easing)
    RETURN f"[{values}]"

  RETURN easing_map.get(css_easing, "[0, 0, 0.2, 1]")


FUNCTION convert_to_framer_variant(css_props):

  framer_props = {}

  FOR prop, value IN css_props:
    IF prop == "transform":
      # Parse transform into individual properties
      transforms = parse_transform(value)
      framer_props.update(transforms)
    ELIF prop == "opacity":
      framer_props["opacity"] = float(value)
    ELIF prop == "scale":
      framer_props["scale"] = float(value)
    ELSE:
      framer_props[prop] = value

  RETURN framer_props


FUNCTION parse_transform(transform_string):

  result = {}

  IF "translateX" IN transform_string:
    value = extract_value(transform_string, "translateX")
    result["x"] = value

  IF "translateY" IN transform_string:
    value = extract_value(transform_string, "translateY")
    result["y"] = value

  IF "scale" IN transform_string:
    value = extract_value(transform_string, "scale")
    result["scale"] = float(value)

  IF "rotate" IN transform_string:
    value = extract_value(transform_string, "rotate")
    result["rotate"] = parse_rotation(value)

  RETURN result
```

### 5. Generate Tailwind Animation

```text
FUNCTION generate_tailwind_animation(spec, tokens):

  # Build animation for tailwind.config.js
  duration = resolve_token(spec.duration, tokens.duration)
  easing_name = spec.easing OR "ease-out"

  config_addition = f"""
// Add to tailwind.config.js → theme.extend.animation
'{kebab_case(spec.name)}': '{kebab_case(spec.name)} {duration} {easing_name}',

// Add to tailwind.config.js → theme.extend.keyframes
'{kebab_case(spec.name)}': {{
{format_tailwind_keyframes(spec.keyframes)}
}},
"""

  # Generate utility class usage
  usage = f"""
// Usage in JSX:
<div className="animate-{kebab_case(spec.name)}">
  Content
</div>

// With Tailwind arbitrary values:
<div className="animate-[{kebab_case(spec.name)}_{duration}_{easing_name}]">
  Content
</div>
"""

  RETURN {
    config: config_addition,
    usage: usage
  }


FUNCTION format_tailwind_keyframes(keyframes):

  lines = []

  FOR frame IN keyframes:
    percent = f"'{frame.percent}%'"
    props = []
    FOR prop, value IN frame.properties:
      props.append(f"    {prop}: '{value}'")
    lines.append(f"  {percent}: {{\n{chr(10).join(props)}\n  }},")

  RETURN "\n".join(lines)
```

### 6. Match Animation Preset

```text
FUNCTION match_preset(spec):

  # Load available presets
  presets = load_animation_presets()

  # Find matching preset
  FOR preset IN presets:
    IF preset.name == spec.name:
      RETURN preset
    IF preset.use_case AND spec.purpose IN preset.use_case:
      RETURN preset

  # Try fuzzy match
  FOR preset IN presets:
    similarity = calculate_similarity(spec, preset)
    IF similarity > 0.8:
      RETURN preset

  RETURN null


FUNCTION load_animation_presets():

  presets = []

  preset_files = [
    "templates/shared/animation-presets/micro-interactions.md",
    "templates/shared/animation-presets/page-transitions.md",
    "templates/shared/animation-presets/loading-states.md",
  ]

  FOR file IN preset_files:
    IF exists(file):
      content = read(file)
      file_presets = parse_preset_file(content)
      presets.extend(file_presets)

  RETURN presets


FUNCTION use_preset(preset, spec):

  # Customize preset with spec overrides
  customized = preset.copy()

  IF spec.duration:
    customized.duration = spec.duration
  IF spec.easing:
    customized.easing = spec.easing
  IF spec.properties:
    customized.properties = spec.properties

  RETURN customized
```

## Complete Pipeline

```text
FUNCTION motion_generation_pipeline(component_name = null):

  # 1. Load context
  design_md = read("design.md")
  constitution = read("constitution.md")
  tokens = load_animation_tokens(constitution)

  # 2. Parse motion specs
  all_specs = parse_motion_specs(design_md)

  IF component_name:
    # Filter to specific component
    specs = [s FOR s IN all_specs IF s.component == component_name]
  ELSE:
    specs = all_specs

  IF NOT specs:
    LOG "No motion specifications found"
    RETURN null

  # 3. Generate animations
  results = []

  FOR spec IN specs:

    # Check for preset match
    preset = match_preset(spec)
    IF preset:
      LOG f"Using preset '{preset.name}' for {spec.name}"
      spec = use_preset(preset, spec)

    # Generate outputs
    css = generate_css_animation(spec, tokens)
    framer = generate_framer_motion(spec, tokens)
    tailwind = generate_tailwind_animation(spec, tokens)

    results.append({
      name: spec.name,
      css: css,
      framer_motion: framer,
      tailwind: tailwind,
      preset_used: preset.name IF preset ELSE null
    })

  # 4. Output files
  output_dir = ".preview/animations"
  mkdir_p(output_dir)

  # Consolidated CSS file
  all_css = "\n\n".join([r.css FOR r IN results])
  write(f"{output_dir}/animations.css", all_css)

  # Individual Framer Motion components
  FOR result IN results:
    write(f"{output_dir}/{kebab_case(result.name)}.tsx", result.framer_motion)

  # Tailwind config additions
  tailwind_config = "// Add these to your tailwind.config.js\n\n"
  FOR result IN results:
    tailwind_config += result.tailwind.config + "\n"
  write(f"{output_dir}/tailwind-additions.js", tailwind_config)

  # Generate preview page
  preview_html = generate_animation_preview_page(results)
  write(f"{output_dir}/preview.html", preview_html)

  RETURN {
    animations: results,
    files: {
      css: f"{output_dir}/animations.css",
      tailwind: f"{output_dir}/tailwind-additions.js",
      preview: f"{output_dir}/preview.html"
    }
  }
```

### Animation Preview Page

```text
FUNCTION generate_animation_preview_page(animations):

  html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Animation Preview</title>
  <link rel="stylesheet" href="animations.css">
  <style>
    body {
      font-family: system-ui, sans-serif;
      padding: 2rem;
      background: #f5f5f5;
    }
    .preview-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 2rem;
    }
    .preview-card {
      background: white;
      border-radius: 8px;
      padding: 1.5rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .preview-card h3 {
      margin: 0 0 1rem;
      font-size: 1rem;
    }
    .demo-area {
      height: 100px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f0f0f0;
      border-radius: 4px;
      margin-bottom: 1rem;
    }
    .demo-element {
      width: 60px;
      height: 60px;
      background: #3b82f6;
      border-radius: 8px;
    }
    .controls {
      display: flex;
      gap: 0.5rem;
    }
    .controls button {
      padding: 0.5rem 1rem;
      border: none;
      border-radius: 4px;
      background: #e5e7eb;
      cursor: pointer;
    }
    .controls button:hover {
      background: #d1d5db;
    }
    .speed-control {
      margin-top: 0.5rem;
    }
  </style>
</head>
<body>
  <h1>Animation Preview</h1>
  <p>Hover, click, or use controls to preview animations</p>

  <div class="preview-grid">
"""

  FOR anim IN animations:
    html += f"""
    <div class="preview-card">
      <h3>{anim.name}</h3>
      <div class="demo-area">
        <div class="demo-element {kebab_case(anim.name)}" id="demo-{kebab_case(anim.name)}"></div>
      </div>
      <div class="controls">
        <button onclick="replay('{kebab_case(anim.name)}')">Replay</button>
        <button onclick="togglePause('{kebab_case(anim.name)}')">Pause/Play</button>
      </div>
      <div class="speed-control">
        <label>Speed: <select onchange="setSpeed('{kebab_case(anim.name)}', this.value)">
          <option value="0.25">0.25x</option>
          <option value="0.5">0.5x</option>
          <option value="1" selected>1x</option>
          <option value="2">2x</option>
        </select></label>
      </div>
    </div>
"""

  html += """
  </div>

  <script>
    function replay(id) {
      const el = document.getElementById('demo-' + id);
      el.style.animation = 'none';
      el.offsetHeight; // Trigger reflow
      el.style.animation = null;
    }

    function togglePause(id) {
      const el = document.getElementById('demo-' + id);
      const state = el.style.animationPlayState;
      el.style.animationPlayState = state === 'paused' ? 'running' : 'paused';
    }

    function setSpeed(id, speed) {
      const el = document.getElementById('demo-' + id);
      el.style.animationDuration = (parseFloat(getComputedStyle(el).animationDuration) / speed) + 's';
    }
  </script>
</body>
</html>
"""

  RETURN html
```

## Usage Example

```text
# Generate all animations from design.md

result = motion_generation_pipeline()

# Output:
{
  animations: [
    {
      name: "button-hover",
      css: "/* CSS code */",
      framer_motion: "/* Framer Motion component */",
      tailwind: { config: "/* Tailwind config */", usage: "/* Usage */"}
    },
    ...
  ],
  files: {
    css: ".preview/animations/animations.css",
    tailwind: ".preview/animations/tailwind-additions.js",
    preview: ".preview/animations/preview.html"
  }
}

# Preview available at:
# http://localhost:3456/animations/preview.html
```

## Integration Points

| Command | Usage |
|---------|-------|
| `/speckit.design` | Motion Designer Agent calls this skill |
| `/speckit.preview` | Includes animation previews |
| `/speckit.implement` | Uses generated CSS/Framer code |

## Accessibility Compliance

All generated animations include:

1. **`prefers-reduced-motion` queries** - Disable/reduce animations
2. **Pause controls** - User can stop animations
3. **No autoplay for decorative** - Only functional animations autoplay
4. **Duration limits** - Max 5 seconds for loops

# AI Mockup Generation Skill

Skill for generating high-fidelity visual mockups using Midjourney and DALL-E 3.

## Overview

**Version:** v0.3.0
**Last Updated:** 2026-01-10

This skill provides automated visual mockup generation using state-of-the-art AI image generation models:
- **DALL-E 3**: 95% text accuracy for UI mockups with readable text
- **Midjourney v7**: Highest visual fidelity for hero images and marketing visuals

## Trigger Conditions

Use this skill when:
- Generating visual mockups from design specifications
- Creating hero images for landing pages
- Producing marketing visuals with brand consistency
- Need high-fidelity mockups before component implementation
- Design.md contains screen specifications but lacks visual references

## Prerequisites

```yaml
required_files:
  - design.md (with screen specifications)
  - constitution.md (for design tokens and aesthetic preset)

optional_files:
  - .speckit/cache/mockups/ (mockup cache)

required_environment:
  - OPENAI_API_KEY (for DALL-E 3)
  - MIDJOURNEY_API_KEY (for Midjourney v7, if using API)
```

## Model Selection

### DALL-E 3 (Recommended for UI)

**Best For:**
- Mobile app screens with readable text
- Desktop interfaces with labels and buttons
- Form layouts with input fields
- Dashboard designs with data visualization
- Any UI requiring accurate text rendering

**Strengths:**
- 95% text accuracy (readable labels, buttons, inputs)
- Precise control over layout and composition
- Consistent with design tokens
- Fast generation (20-30 seconds)

**Limitations:**
- Lower artistic fidelity than Midjourney
- Limited to square/portrait/landscape ratios
- Max resolution: 1024×1792px (portrait)

### Midjourney v7 (Recommended for Marketing)

**Best For:**
- Hero images and landing page headers
- Marketing illustrations
- Brand storytelling visuals
- Abstract concepts and metaphors
- High-fidelity artistic compositions

**Strengths:**
- Highest visual fidelity and artistic quality
- Photorealistic rendering
- Advanced lighting and composition
- Wide aspect ratio support

**Limitations:**
- Text rendering unreliable (use for decoration only)
- Requires Discord bot or API access
- Slower generation (60-90 seconds with retries)

## Execution Flow

### 1. Load Design Context

```text
FUNCTION load_design_context():

  # Load design system
  constitution = read("constitution.md")
  tokens = extract_design_tokens(constitution)
  aesthetic = constitution.design_system.aesthetic_preset OR "vercel"

  # Load screen specs
  design = read("design.md")
  screens = extract_screen_specs(design)

  RETURN {
    tokens: tokens,
    aesthetic: aesthetic,
    screens: screens,
    app_type: constitution.project.app_type,
    brand_identity: constitution.brand
  }
```

### 2. Select Model Based on Screen Type

```text
FUNCTION select_model(screen):

  # Decision tree
  IF screen.contains_ui_elements AND screen.has_readable_text:
    RETURN "dalle3"  # UI with text requires DALL-E 3

  IF screen.type IN ["hero", "banner", "marketing", "illustration"]:
    RETURN "midjourney"  # Marketing visuals use Midjourney

  IF screen.type IN ["dashboard", "form", "table", "list"]:
    RETURN "dalle3"  # Data-heavy UIs use DALL-E 3

  IF screen.complexity == "high" AND screen.artistic_quality == "critical":
    RETURN "midjourney"  # High-fidelity visuals use Midjourney

  # Default to DALL-E 3 for UI
  RETURN "dalle3"
```

### 3. Build DALL-E 3 Prompt

```text
FUNCTION build_dalle3_prompt(screen, tokens, aesthetic):

  # Base prompt structure
  prompt = f"""
Create a {screen.device} {screen.type} UI mockup in {aesthetic} style.

## Screen Purpose
{screen.purpose}

## Layout Structure
{screen.layout.description}

## Design Tokens
Colors:
  - Primary: {tokens.colors.primary}
  - Background: {tokens.colors.background}
  - Foreground: {tokens.colors.foreground}

Typography:
  - Font: {tokens.typography.font_family}
  - Base Size: {tokens.typography.scale.base}

Spacing: {tokens.spacing.unit} scale

## UI Elements
{build_ui_elements_list(screen.elements)}

## Text Content (Must Be Readable)
{extract_text_content(screen)}

## Style Guidelines
- {aesthetic} aesthetic (reference: {get_aesthetic_keywords(aesthetic)})
- Modern 2026 design trends
- Clean, minimal, professional
- High contrast for accessibility

## Requirements
- All text must be legible and match specified content
- Use design token colors exactly
- Follow {screen.device} conventions (iOS/Android/Web)
- Include proper spacing and hierarchy
- Realistic data (not placeholder)

Negative prompts: generic, low-fidelity, placeholder text, blurry, clip-art
"""

  RETURN prompt


FUNCTION build_ui_elements_list(elements):
  result = ""
  FOR element IN elements:
    result += f"- {element.type}: {element.label}"
    IF element.props:
      result += f" ({format_props(element.props)})"
    result += "\n"
  RETURN result


FUNCTION extract_text_content(screen):
  """Extract all text that should appear in mockup"""
  content = []

  # Navigation
  IF screen.navigation:
    content.append(f"Navigation: {', '.join(screen.navigation.items)}")

  # Headings
  FOR heading IN screen.headings:
    content.append(f"Heading: '{heading.text}'")

  # Buttons
  FOR button IN screen.buttons:
    content.append(f"Button: '{button.label}'")

  # Form labels
  FOR field IN screen.form_fields:
    content.append(f"Label: '{field.label}'")
    IF field.placeholder:
      content.append(f"Placeholder: '{field.placeholder}'")

  # Body text (truncated)
  IF screen.body_text:
    truncated = screen.body_text[:200] + "..."
    content.append(f"Body: '{truncated}'")

  RETURN "\n".join(content)
```

### 4. Build Midjourney Prompt

```text
FUNCTION build_midjourney_prompt(screen, tokens, aesthetic):

  # Midjourney-specific prompt structure
  prompt = f"""
{screen.concept_description}, {aesthetic} style, {screen.mood} atmosphere

## Visual Style
- Aesthetic: {aesthetic} ({get_aesthetic_keywords(aesthetic)})
- Colors: {tokens.colors.primary}, {tokens.colors.accent}
- Mood: {screen.mood}
- Lighting: {screen.lighting OR "soft, natural"}

## Composition
- Layout: {screen.composition}
- Focal Point: {screen.focal_point}
- Aspect Ratio: {screen.aspect_ratio OR "16:9"}

## Quality Settings
- Style: raw
- Version: 6.1
- Stylize: 500
- Quality: 2

negative prompts: text, labels, buttons, UI elements, generic stock photo, low quality
"""

  # Format for Midjourney API
  formatted = prompt.replace("\n", " ").strip()

  # Add parameters
  formatted += f" --ar {screen.aspect_ratio OR '16:9'}"
  formatted += " --style raw --stylize 500 --quality 2 --v 6.1"

  RETURN formatted


FUNCTION get_aesthetic_keywords(aesthetic):
  """Map aesthetic presets to visual keywords"""

  keywords = {
    "linear": "clean minimal purple gradient geometric",
    "stripe": "professional indigo blue gradient sophisticated",
    "vercel": "brutalist black sharp modern high-contrast",
    "notion": "warm beige soft-shadows friendly approachable",
    "apple": "premium glossy blue frosted-glass elegant",
    "airbnb": "vibrant pink warm-coral welcoming travel",
    "github": "developer blue monospace technical clean",
    "slack": "playful purple colorful friendly messaging",
    "figma": "creative purple gradient design-tools modern"
  }

  RETURN keywords.get(aesthetic, "modern clean professional")
```

### 5. Generate with DALL-E 3

```text
FUNCTION generate_dalle3(prompt, screen):

  # API call
  response = openai.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size=get_size(screen.device),  # "1024x1024", "1024x1792", "1792x1024"
    quality="hd",
    n=1
  )

  image_url = response.data[0].url

  # Download image
  image_data = http_get(image_url)

  # Save locally
  output_path = f".preview/mockups/{screen.name}-dalle3.png"
  write_binary(output_path, image_data)

  # Extract revised prompt (DALL-E 3 auto-revises)
  revised_prompt = response.data[0].revised_prompt

  RETURN {
    path: output_path,
    url: image_url,
    revised_prompt: revised_prompt,
    model: "dall-e-3",
    size: get_size(screen.device)
  }


FUNCTION get_size(device):
  sizes = {
    "mobile": "1024x1792",    # Portrait
    "tablet": "1024x1024",     # Square
    "desktop": "1792x1024"     # Landscape
  }
  RETURN sizes.get(device, "1024x1024")
```

### 6. Generate with Midjourney

```text
FUNCTION generate_midjourney(prompt, screen):

  # Two modes: API (preferred) or Discord bot
  IF midjourney_api_available():
    RETURN generate_midjourney_api(prompt, screen)
  ELSE:
    RETURN generate_midjourney_manual(prompt, screen)


FUNCTION generate_midjourney_api(prompt, screen):
  """Using Midjourney API (future availability)"""

  # API call (hypothetical endpoint)
  response = http_post("https://api.midjourney.com/v1/imagine", {
    headers: {
      "Authorization": f"Bearer {env.MIDJOURNEY_API_KEY}",
      "Content-Type": "application/json"
    },
    body: {
      "prompt": prompt,
      "webhook_url": f"{env.CALLBACK_URL}/midjourney"
    }
  })

  job_id = response.id

  # Poll for completion (async)
  WHILE true:
    status = http_get(f"https://api.midjourney.com/v1/jobs/{job_id}")

    IF status.status == "completed":
      BREAK
    ELSE IF status.status == "failed":
      ERROR "Midjourney generation failed"

    sleep(5000)  # Poll every 5 seconds

  # Download result
  image_data = http_get(status.image_url)
  output_path = f".preview/mockups/{screen.name}-midjourney.png"
  write_binary(output_path, image_data)

  RETURN {
    path: output_path,
    url: status.image_url,
    prompt: prompt,
    model: "midjourney-v7",
    job_id: job_id
  }


FUNCTION generate_midjourney_manual(prompt, screen):
  """Manual Discord bot workflow"""

  formatted_prompt = format_for_manual_entry(prompt)

  DISPLAY """
  ┌─────────────────────────────────────────────────────────────┐
  │ Midjourney Generation Required                               │
  └─────────────────────────────────────────────────────────────┘

  Please use Midjourney Discord bot to generate this image:

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {formatted_prompt}
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Steps:
  1. Go to Midjourney Discord server
  2. Use /imagine command with prompt above
  3. Wait for 4 variations to generate
  4. Select best variation (U1, U2, U3, or U4)
  5. Download upscaled image
  6. Save to: .preview/mockups/{screen.name}-midjourney.png

  Press Enter when image is saved...
  """

  wait_for_user_input()

  # Verify file exists
  output_path = f".preview/mockups/{screen.name}-midjourney.png"
  IF NOT exists(output_path):
    ERROR "Image not found. Please save to {output_path}"

  RETURN {
    path: output_path,
    prompt: prompt,
    model: "midjourney-v7-manual"
  }
```

### 7. Post-Process and Validate

```text
FUNCTION post_process_mockup(mockup, screen):

  # Load image
  image = load_image(mockup.path)

  # Validate dimensions
  IF image.width < 800 OR image.height < 600:
    WARN f"Low resolution: {image.width}x{image.height}"

  # Check if image contains expected elements (basic validation)
  validation = {
    "resolution": f"{image.width}x{image.height}",
    "file_size": get_file_size(mockup.path),
    "aspect_ratio": round(image.width / image.height, 2)
  }

  # Generate thumbnail
  thumbnail_path = mockup.path.replace(".png", "-thumb.png")
  create_thumbnail(image, thumbnail_path, max_size=400)

  # Add to mockup metadata
  mockup.thumbnail = thumbnail_path
  mockup.validation = validation

  RETURN mockup
```

### 8. Cache Result

```text
FUNCTION cache_mockup(mockup, screen, tokens):

  cache_key = hash(screen.spec + tokens + mockup.model)
  cache_dir = f".speckit/cache/mockups/{screen.name}"

  mkdir_p(cache_dir)

  # Copy image to cache
  copy_file(mockup.path, f"{cache_dir}/mockup.png")
  IF mockup.thumbnail:
    copy_file(mockup.thumbnail, f"{cache_dir}/thumbnail.png")

  # Write metadata
  metadata = {
    "generated_at": now(),
    "screen": screen.name,
    "model": mockup.model,
    "prompt": mockup.prompt,
    "validation": mockup.validation,
    "cache_key": cache_key
  }

  write_json(f"{cache_dir}/metadata.json", metadata)

  LOG f"Cached mockup for {screen.name}"
```

### 9. Generate Gallery HTML

```text
FUNCTION generate_mockup_gallery(mockups):

  html = """
<!DOCTYPE html>
<html>
<head>
  <title>AI Mockups Gallery</title>
  <style>
    body { font-family: -apple-system, system-ui; padding: 40px; background: #f5f5f5; }
    .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 24px; }
    .card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .card img { width: 100%; border-radius: 8px; margin-bottom: 16px; }
    .card h3 { margin: 0 0 8px 0; }
    .card .meta { color: #666; font-size: 14px; }
    .card .model { display: inline-block; padding: 4px 12px; background: #e3e3e3; border-radius: 4px; font-size: 12px; margin-top: 8px; }
  </style>
</head>
<body>
  <h1>AI-Generated Mockups</h1>
  <p>Generated: {now()}</p>
  <div class="gallery">
"""

  FOR mockup IN mockups:
    html += f"""
    <div class="card">
      <img src="{mockup.path}" alt="{mockup.screen}" />
      <h3>{mockup.screen}</h3>
      <div class="meta">
        <div>Resolution: {mockup.validation.resolution}</div>
        <div>File Size: {mockup.validation.file_size}</div>
        <span class="model">{mockup.model}</span>
      </div>
    </div>
"""

  html += """
  </div>
</body>
</html>
"""

  write(f".preview/mockups/gallery.html", html)
  LOG "Gallery generated at .preview/mockups/gallery.html"
```

## Complete Pipeline

```text
FUNCTION ai_mockup_generation_pipeline(screen_name):

  # 1. Load context
  context = load_design_context()
  screen = find_screen(context.screens, screen_name)

  IF NOT screen:
    ERROR f"Screen '{screen_name}' not found in design.md"

  # 2. Check cache
  cached = check_mockup_cache(screen, context.tokens)
  IF cached:
    RETURN cached

  # 3. Select model
  model = select_model(screen)
  LOG f"Selected model: {model} for screen '{screen.name}'"

  # 4. Build prompt
  IF model == "dalle3":
    prompt = build_dalle3_prompt(screen, context.tokens, context.aesthetic)
  ELSE:
    prompt = build_midjourney_prompt(screen, context.tokens, context.aesthetic)

  LOG f"Generated prompt ({len(prompt)} chars)"

  # 5. Generate mockup
  IF model == "dalle3":
    mockup = generate_dalle3(prompt, screen)
  ELSE:
    mockup = generate_midjourney(prompt, screen)

  # 6. Post-process
  mockup = post_process_mockup(mockup, screen)

  # 7. Cache
  cache_mockup(mockup, screen, context.tokens)

  # 8. Return
  RETURN {
    mockup: mockup,
    screen: screen.name,
    model: model,
    validation: mockup.validation
  }


FUNCTION generate_all_mockups():
  """Generate mockups for all screens in design.md"""

  context = load_design_context()
  mockups = []

  FOR screen IN context.screens:
    LOG f"Generating mockup for {screen.name}..."

    TRY:
      mockup = ai_mockup_generation_pipeline(screen.name)
      mockups.append(mockup)
      LOG f"✓ {screen.name} complete"
    CATCH error:
      WARN f"✗ {screen.name} failed: {error}"
      CONTINUE

  # Generate gallery
  generate_mockup_gallery(mockups)

  RETURN mockups
```

## Integration with Preview Command

Add as Wave 6 subagent in `templates/commands/preview.md`:

```yaml
- role: ai-mockup-generator
  role_group: GENERATION
  priority: 25
  model_override: opus
  prompt: |
    Generate AI mockups for screens using ai-mockup-generation skill.

    ## Execution
    CALL ai_mockup_generation_pipeline() for each screen in design.md

    ## Model Selection
    - UI screens with text → DALL-E 3
    - Hero/marketing visuals → Midjourney v7

    ## Output
    - .preview/mockups/{screen}-dalle3.png OR {screen}-midjourney.png
    - .preview/mockups/gallery.html (overview)

    ## Validation
    - Check resolution >= 800x600
    - Verify file exists
    - Generate thumbnails
```

## Configuration

```yaml
# constitution.md
ai_mockup_generation:
  enabled: true
  default_model: "dalle3"  # or "midjourney"
  cache:
    enabled: true
    ttl_hours: 168  # 7 days
  dalle3:
    quality: "hd"
    sizes:
      mobile: "1024x1792"
      tablet: "1024x1024"
      desktop: "1792x1024"
  midjourney:
    version: "6.1"
    style: "raw"
    stylize: 500
    quality: 2
    mode: "api"  # or "manual"
```

## Error Handling

```text
ERROR_HANDLERS:

  api_rate_limit:
    message: "API rate limit exceeded"
    action: "Wait 60 seconds and retry"
    retry: true
    max_retries: 3

  invalid_prompt:
    message: "Prompt rejected by content policy"
    action: "Revise prompt to remove policy violations"
    retry: false

  generation_timeout:
    message: "Generation timed out (>120s)"
    action: "Retry with shorter prompt"
    retry: true
    max_retries: 2

  low_quality_result:
    message: "Generated image quality below threshold"
    action: "Regenerate with revised prompt"
    retry: true
    max_retries: 1
```

## Usage Examples

```text
# Single screen mockup
RESULT = ai_mockup_generation_pipeline("LoginScreen")
# Output: .preview/mockups/LoginScreen-dalle3.png

# All screens
RESULTS = generate_all_mockups()
# Output: .preview/mockups/gallery.html

# Hero image only
screen = { name: "Hero", type: "hero", mood: "inspiring", ... }
mockup = generate_midjourney(build_midjourney_prompt(screen, tokens, "linear"))
# Output: .preview/mockups/Hero-midjourney.png
```

## Expected Results

### DALL-E 3 Output
- **Resolution**: 1024×1024 to 1792×1024
- **Text Accuracy**: 95% readable labels, buttons, inputs
- **Generation Time**: 20-30 seconds
- **Cost**: ~$0.04-0.08 per image

### Midjourney Output
- **Resolution**: Up to 2048×2048 (varies by aspect ratio)
- **Visual Fidelity**: Photorealistic, high artistic quality
- **Generation Time**: 60-90 seconds (with retries)
- **Cost**: ~$0.10 per image (Fast mode)

---

**Version:** v0.3.0
**Status:** Implementation Ready
**Dependencies**: OpenAI API (DALL-E 3), Midjourney API/Discord (optional)

# Figma Import Guide

This document provides context for AI agents performing Figma design token and component extraction via the `/speckit.design` command.

## Authentication

Set `FIGMA_ACCESS_TOKEN` environment variable with a Personal Access Token from Figma settings:

1. Go to Figma → Settings → Personal Access Tokens
2. Generate a new token with read access
3. Export as environment variable:
   ```bash
   export FIGMA_ACCESS_TOKEN="figd_xxxxx"
   ```

## Figma URL Formats

The Design System field in `spec.md` accepts these URL patterns:

| Format | Pattern | Example |
|--------|---------|---------|
| File URL | `https://www.figma.com/file/{file_key}/{file_name}` | `https://www.figma.com/file/abc123/MyDesign` |
| Design URL | `https://www.figma.com/design/{file_key}/{file_name}` | `https://www.figma.com/design/abc123/MyDesign` |
| With node | `...?node-id={node_id}` | `...?node-id=0%3A1` |

**File Key Extraction**: Parse the `{file_key}` segment from the URL path.

## Figma API Endpoints

### Get File Styles

```http
GET /v1/files/{file_key}/styles
Authorization: Bearer {FIGMA_ACCESS_TOKEN}
```

Returns all published styles (colors, text, effects).

### Get File

```http
GET /v1/files/{file_key}
Authorization: Bearer {FIGMA_ACCESS_TOKEN}
```

Returns full document tree including components.

### Get File Components

```http
GET /v1/files/{file_key}/components
Authorization: Bearer {FIGMA_ACCESS_TOKEN}
```

Returns component metadata and descriptions.

## Extraction Mapping

### Design Tokens

| Figma Element | API Path | Spec-Kit Target | Notes |
|---------------|----------|-----------------|-------|
| Color Styles | `styles[type=FILL]` | design.md → Color Palette | Semantic names preserved |
| Text Styles | `styles[type=TEXT]` | design.md → Typography Scale | Font family, size, weight, line-height |
| Effect Styles | `styles[type=EFFECT]` | design.md → Shadow System | Drop shadows, inner shadows, blurs |
| Grid Styles | `styles[type=GRID]` | design.md → Spacing System | Column/row/grid layouts |

### Color Extraction

```text
Figma Style:
  name: "Primary/500"
  style_type: "FILL"
  description: "Main brand color for CTAs"

→ design.md Color Palette:
  | Token | CSS Variable | Light Value | Usage |
  | Primary | --color-primary | {extracted hex} | Main brand color for CTAs |
```

**Color Naming Convention**:
- `Primary/500` → `--color-primary`
- `Gray/100` → `--color-gray-100`
- `Status/Success` → `--color-success`

### Typography Extraction

```text
Figma Style:
  name: "Heading/H1"
  style_type: "TEXT"
  fontFamily: "Inter"
  fontSize: 36
  fontWeight: 700
  lineHeightPx: 43.2

→ design.md Typography Scale:
  | Level | CSS Variable | Size (rem) | Weight | Line Height |
  | H1 | --text-h1 | 2.25rem | 700 | 1.2 |
```

### Effect Extraction

```text
Figma Style:
  name: "Shadow/Medium"
  style_type: "EFFECT"
  effects: [{
    type: "DROP_SHADOW",
    offset: { x: 0, y: 4 },
    radius: 6,
    color: { r: 0, g: 0, b: 0, a: 0.1 }
  }]

→ design.md Shadow System:
  | Token | CSS Variable | Value |
  | Medium | --shadow-md | 0 4px 6px rgba(0,0,0,0.1) |
```

### Component Extraction

| Figma Element | API Path | Spec-Kit Target | Notes |
|---------------|----------|-----------------|-------|
| Components | `components[]` | design.md → Component Specifications | Props from variants |
| Component Sets | `componentSets[]` | Component variant matrix | States mapping |
| Component Descriptions | `description` | Component Purpose field | Preserved verbatim |

**Variant Mapping**:
```text
Figma Component Set: "Button"
  Variants:
    - Size=sm, State=default
    - Size=sm, State=hover
    - Size=md, State=default
    - Size=md, State=hover

→ design.md Component Specifications:
  ### Button

  **Variants**:
  | Variant | Size | State |
  | SM Default | 32px | Default |
  | SM Hover | 32px | Hover |
  | MD Default | 40px | Default |
  | MD Hover | 40px | Hover |
```

## Conflict Resolution

When importing into an existing `design.md`:

| Scenario | Behavior |
|----------|----------|
| Existing manual entries | PRESERVE (don't overwrite) |
| Figma-imported entries (marked `<!-- figma-sync -->`) | UPDATE with new values |
| New Figma styles not in design.md | APPEND to appropriate table |
| Deleted Figma styles | KEEP in design.md (warn user) |

### Sync Markers

Figma-imported entries include HTML comments for re-import:

```markdown
| Primary | --color-primary | #2563EB | CTAs | <!-- figma-sync:style_id -->
```

On re-import, only entries with `figma-sync` markers are updated.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| 403 Forbidden | Invalid or expired token | Regenerate FIGMA_ACCESS_TOKEN |
| 404 Not Found | Invalid file key or deleted file | Verify Figma URL in spec.md |
| Rate Limited | Too many requests | Wait and retry with backoff |
| No styles found | File has no published styles | Publish styles in Figma first |

## Validation Rules

Before writing to `design.md`, validate:

1. **Color values**: Must be valid hex (#RRGGBB or #RRGGBBAA)
2. **Font sizes**: Convert px to rem (base 16px)
3. **Line heights**: Convert px to unitless ratio
4. **Shadow values**: Format as CSS box-shadow syntax
5. **Token names**: Convert to kebab-case CSS variable names

## Import Report Format

After successful import, generate:

```text
FIGMA_IMPORT_REPORT:
  File: {file_name} ({file_key})
  Imported: {timestamp}

  Tokens:
    - Colors: {count} extracted
    - Typography: {count} extracted
    - Effects: {count} extracted

  Components:
    - {count} components extracted
    - {count} variants mapped

  Conflicts:
    - {list of skipped manual entries}

  Warnings:
    - {list of unpublished styles}
```

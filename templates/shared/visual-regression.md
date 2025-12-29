# Visual Regression Testing

Automated visual testing system for detecting unintended UI changes between design iterations and implementation.

## Overview

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    VISUAL REGRESSION TESTING                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐                          ┌──────────────┐             │
│  │   Baseline   │                          │   Current    │             │
│  │  Screenshot  │                          │  Screenshot  │             │
│  └──────┬───────┘                          └──────┬───────┘             │
│         │                                         │                      │
│         └────────────────┬────────────────────────┘                      │
│                          │                                               │
│                          ▼                                               │
│                   ┌──────────────┐                                       │
│                   │   Pixel      │                                       │
│                   │   Comparison │                                       │
│                   └──────┬───────┘                                       │
│                          │                                               │
│         ┌────────────────┼────────────────┐                             │
│         │                │                │                              │
│         ▼                ▼                ▼                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                     │
│  │    Pass      │ │    Diff      │ │    Fail      │                     │
│  │  < 0.1%      │ │  0.1% - 5%   │ │   > 5%       │                     │
│  └──────────────┘ └──────────────┘ └──────────────┘                     │
│                          │                │                              │
│                          ▼                ▼                              │
│                   ┌──────────────┐ ┌──────────────┐                     │
│                   │  Diff Image  │ │   Report     │                     │
│                   │  Generation  │ │  Generation  │                     │
│                   └──────────────┘ └──────────────┘                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Concepts

### Baselines

Baselines are the reference screenshots that current screenshots are compared against.

```text
.visual-regression/
├── baselines/
│   ├── components/
│   │   ├── button/
│   │   │   ├── default.desktop.png
│   │   │   ├── default.mobile.png
│   │   │   ├── hover.desktop.png
│   │   │   └── disabled.desktop.png
│   │   └── card/
│   │       └── ...
│   ├── wireframes/
│   │   ├── dashboard.desktop.png
│   │   └── dashboard.mobile.png
│   └── flows/
│       └── onboarding/
│           ├── step-1.png
│           └── step-2.png
├── current/
│   └── ... (same structure)
├── diffs/
│   └── ... (same structure)
└── config.json
```

### Comparison Modes

| Mode | Use Case | Algorithm |
|------|----------|-----------|
| `pixel` | Exact match required | Pixel-by-pixel diff |
| `perceptual` | Minor rendering differences OK | SSIM/DSSIM |
| `layout` | Content may change, layout matters | Structural comparison |
| `anti-alias` | Ignore font rendering differences | Anti-aliasing tolerance |

## Pipeline Functions

### Initialize Baseline

```text
FUNCTION initialize_baselines():

  baseline_dir = ".visual-regression/baselines"
  mkdir_p(baseline_dir)

  # Collect all screenshots from preview
  screenshots = glob(".preview/**/screenshots/*.png")

  FOR screenshot IN screenshots:
    # Determine baseline path
    relative_path = screenshot.replace(".preview/", "")
    baseline_path = f"{baseline_dir}/{relative_path}"

    # Copy to baselines
    mkdir_p(dirname(baseline_path))
    copy(screenshot, baseline_path)

    LOG f"Baseline created: {baseline_path}"

  # Write metadata
  metadata = {
    created_at: now(),
    screenshot_count: len(screenshots),
    config: load_vr_config()
  }
  write_json(f"{baseline_dir}/metadata.json", metadata)

  LOG f"Initialized {len(screenshots)} baselines"
```

### Run Comparison

```text
FUNCTION run_visual_regression(options):

  config = load_vr_config()
  baseline_dir = ".visual-regression/baselines"
  current_dir = ".visual-regression/current"
  diff_dir = ".visual-regression/diffs"

  # Ensure directories exist
  mkdir_p(current_dir)
  mkdir_p(diff_dir)

  # Collect current screenshots
  current_screenshots = glob(".preview/**/screenshots/*.png")

  results = []

  FOR screenshot IN current_screenshots:

    # Determine paths
    relative_path = screenshot.replace(".preview/", "")
    baseline_path = f"{baseline_dir}/{relative_path}"
    current_path = f"{current_dir}/{relative_path}"
    diff_path = f"{diff_dir}/{relative_path}"

    # Copy current screenshot
    mkdir_p(dirname(current_path))
    copy(screenshot, current_path)

    # Check if baseline exists
    IF NOT exists(baseline_path):
      results.append({
        path: relative_path,
        status: "new",
        message: "No baseline found"
      })
      CONTINUE

    # Run comparison
    comparison = compare_images(
      baseline_path,
      current_path,
      options.mode OR config.mode OR "pixel"
    )

    # Determine status
    threshold = get_threshold(relative_path, config)

    IF comparison.diff_percentage < threshold.pass:
      status = "pass"
    ELIF comparison.diff_percentage < threshold.warn:
      status = "warn"
    ELSE:
      status = "fail"

    # Generate diff image if not pass
    IF status != "pass":
      mkdir_p(dirname(diff_path))
      generate_diff_image(
        baseline_path,
        current_path,
        diff_path,
        highlight_color: config.highlight_color OR "#ff00ff"
      )

    results.append({
      path: relative_path,
      status: status,
      diff_percentage: comparison.diff_percentage,
      diff_pixels: comparison.diff_pixels,
      total_pixels: comparison.total_pixels,
      baseline: baseline_path,
      current: current_path,
      diff: diff_path IF status != "pass" ELSE null
    })

  # Generate report
  report = generate_vr_report(results, config)

  RETURN report
```

### Image Comparison

```text
FUNCTION compare_images(baseline_path, current_path, mode):

  baseline = load_image(baseline_path)
  current = load_image(current_path)

  # Check dimensions
  IF baseline.dimensions != current.dimensions:
    RETURN {
      diff_percentage: 100,
      diff_pixels: max(baseline.pixels, current.pixels),
      total_pixels: max(baseline.pixels, current.pixels),
      dimension_mismatch: true
    }

  IF mode == "pixel":
    RETURN pixel_compare(baseline, current)
  ELIF mode == "perceptual":
    RETURN perceptual_compare(baseline, current)
  ELIF mode == "layout":
    RETURN layout_compare(baseline, current)
  ELIF mode == "anti-alias":
    RETURN antialias_compare(baseline, current)


FUNCTION pixel_compare(baseline, current):

  diff_pixels = 0
  total_pixels = baseline.width * baseline.height

  FOR x IN range(baseline.width):
    FOR y IN range(baseline.height):
      baseline_pixel = baseline.get_pixel(x, y)
      current_pixel = current.get_pixel(x, y)

      IF baseline_pixel != current_pixel:
        diff_pixels += 1

  RETURN {
    diff_percentage: (diff_pixels / total_pixels) * 100,
    diff_pixels: diff_pixels,
    total_pixels: total_pixels
  }


FUNCTION perceptual_compare(baseline, current):

  # Use SSIM (Structural Similarity Index)
  ssim_score = calculate_ssim(baseline, current)

  # Convert to diff percentage (1.0 = identical, 0.0 = completely different)
  diff_percentage = (1 - ssim_score) * 100

  RETURN {
    diff_percentage: diff_percentage,
    ssim_score: ssim_score,
    total_pixels: baseline.width * baseline.height
  }


FUNCTION antialias_compare(baseline, current):

  diff_pixels = 0
  total_pixels = baseline.width * baseline.height
  tolerance = 16  # Color channel tolerance for anti-aliasing

  FOR x IN range(baseline.width):
    FOR y IN range(baseline.height):
      baseline_pixel = baseline.get_pixel(x, y)
      current_pixel = current.get_pixel(x, y)

      # Check if within tolerance
      color_diff = max(
        abs(baseline_pixel.r - current_pixel.r),
        abs(baseline_pixel.g - current_pixel.g),
        abs(baseline_pixel.b - current_pixel.b)
      )

      IF color_diff > tolerance:
        # Check if this is an edge pixel (anti-aliasing)
        IF NOT is_edge_pixel(baseline, x, y) AND NOT is_edge_pixel(current, x, y):
          diff_pixels += 1

  RETURN {
    diff_percentage: (diff_pixels / total_pixels) * 100,
    diff_pixels: diff_pixels,
    total_pixels: total_pixels
  }
```

### Diff Image Generation

```text
FUNCTION generate_diff_image(baseline_path, current_path, output_path, options):

  baseline = load_image(baseline_path)
  current = load_image(current_path)

  # Create diff image canvas
  width = max(baseline.width, current.width)
  height = max(baseline.height, current.height)

  diff_image = create_image(width, height)

  FOR x IN range(width):
    FOR y IN range(height):

      # Handle dimension mismatches
      IF x >= baseline.width OR y >= baseline.height:
        diff_image.set_pixel(x, y, options.missing_color OR "#00ff00")
        CONTINUE
      IF x >= current.width OR y >= current.height:
        diff_image.set_pixel(x, y, options.missing_color OR "#00ff00")
        CONTINUE

      baseline_pixel = baseline.get_pixel(x, y)
      current_pixel = current.get_pixel(x, y)

      IF baseline_pixel != current_pixel:
        # Highlight difference
        diff_image.set_pixel(x, y, options.highlight_color OR "#ff00ff")
      ELSE:
        # Fade unchanged pixels
        faded = fade_pixel(baseline_pixel, 0.3)
        diff_image.set_pixel(x, y, faded)

  save_image(diff_image, output_path)


FUNCTION generate_side_by_side(baseline_path, current_path, diff_path, output_path):

  baseline = load_image(baseline_path)
  current = load_image(current_path)
  diff = load_image(diff_path)

  # Create composite image
  total_width = baseline.width + current.width + diff.width + 40  # 20px gaps
  height = max(baseline.height, current.height, diff.height) + 60  # Labels

  composite = create_image(total_width, height, background: "#ffffff")

  # Draw labels
  draw_text(composite, "Baseline", 10, 10)
  draw_text(composite, "Current", baseline.width + 30, 10)
  draw_text(composite, "Diff", baseline.width + current.width + 50, 10)

  # Draw images
  composite.paste(baseline, 10, 40)
  composite.paste(current, baseline.width + 30, 40)
  composite.paste(diff, baseline.width + current.width + 50, 40)

  save_image(composite, output_path)
```

## Threshold Configuration

```text
FUNCTION get_threshold(path, config):

  # Check for path-specific threshold
  FOR pattern, threshold IN config.thresholds:
    IF glob_match(pattern, path):
      RETURN threshold

  # Default thresholds
  RETURN {
    pass: 0.1,   # < 0.1% difference = pass
    warn: 1.0,   # 0.1% - 1% = warning
    fail: 5.0    # > 5% = fail
  }
```

### Configuration File

```json
{
  "mode": "pixel",
  "highlight_color": "#ff00ff",
  "missing_color": "#00ff00",
  "thresholds": {
    "default": {
      "pass": 0.1,
      "warn": 1.0,
      "fail": 5.0
    },
    "components/button/*": {
      "pass": 0.05,
      "warn": 0.5,
      "fail": 2.0
    },
    "wireframes/*": {
      "pass": 0.5,
      "warn": 2.0,
      "fail": 10.0
    },
    "animations/*": {
      "pass": 5.0,
      "warn": 10.0,
      "fail": 20.0
    }
  },
  "ignore_patterns": [
    "**/timestamp*",
    "**/dynamic-content*"
  ],
  "viewports": {
    "mobile": { "width": 375, "height": 667 },
    "tablet": { "width": 768, "height": 1024 },
    "desktop": { "width": 1280, "height": 800 }
  }
}
```

## Report Generation

```text
FUNCTION generate_vr_report(results, config):

  # Calculate statistics
  stats = {
    total: len(results),
    passed: count(results, status == "pass"),
    warned: count(results, status == "warn"),
    failed: count(results, status == "fail"),
    new: count(results, status == "new")
  }

  # Group by status
  grouped = {
    failed: filter(results, status == "fail"),
    warned: filter(results, status == "warn"),
    new: filter(results, status == "new"),
    passed: filter(results, status == "pass")
  }

  # Generate HTML report
  html_report = generate_html_report(stats, grouped)
  write(".visual-regression/report.html", html_report)

  # Generate JSON report
  json_report = {
    timestamp: now(),
    stats: stats,
    results: results,
    config: config
  }
  write_json(".visual-regression/report.json", json_report)

  # Generate Markdown summary
  md_summary = generate_markdown_summary(stats, grouped)
  write(".visual-regression/summary.md", md_summary)

  RETURN {
    html: ".visual-regression/report.html",
    json: ".visual-regression/report.json",
    markdown: ".visual-regression/summary.md",
    stats: stats
  }


FUNCTION generate_html_report(stats, grouped):

  html = f"""
<!DOCTYPE html>
<html>
<head>
  <title>Visual Regression Report</title>
  <style>
    body {{ font-family: system-ui, sans-serif; padding: 2rem; }}
    .stats {{ display: flex; gap: 1rem; margin-bottom: 2rem; }}
    .stat {{ padding: 1rem; border-radius: 8px; text-align: center; }}
    .stat.pass {{ background: #d1fae5; }}
    .stat.warn {{ background: #fef3c7; }}
    .stat.fail {{ background: #fee2e2; }}
    .stat.new {{ background: #dbeafe; }}
    .stat-value {{ font-size: 2rem; font-weight: bold; }}
    .result {{ margin: 1rem 0; padding: 1rem; border: 1px solid #e5e7eb; border-radius: 8px; }}
    .result.fail {{ border-color: #ef4444; }}
    .result.warn {{ border-color: #f59e0b; }}
    .images {{ display: flex; gap: 1rem; margin-top: 1rem; }}
    .images img {{ max-width: 300px; border: 1px solid #e5e7eb; }}
    .diff-percentage {{ font-weight: bold; }}
    .diff-percentage.high {{ color: #ef4444; }}
    .diff-percentage.medium {{ color: #f59e0b; }}
    .diff-percentage.low {{ color: #10b981; }}
  </style>
</head>
<body>
  <h1>Visual Regression Report</h1>
  <p>Generated: {now()}</p>

  <div class="stats">
    <div class="stat pass">
      <div class="stat-value">{stats.passed}</div>
      <div>Passed</div>
    </div>
    <div class="stat warn">
      <div class="stat-value">{stats.warned}</div>
      <div>Warnings</div>
    </div>
    <div class="stat fail">
      <div class="stat-value">{stats.failed}</div>
      <div>Failed</div>
    </div>
    <div class="stat new">
      <div class="stat-value">{stats.new}</div>
      <div>New</div>
    </div>
  </div>

  {generate_result_sections(grouped)}

</body>
</html>
"""

  RETURN html


FUNCTION generate_markdown_summary(stats, grouped):

  md = f"""
# Visual Regression Summary

| Status | Count |
|--------|-------|
| ✅ Passed | {stats.passed} |
| ⚠️ Warnings | {stats.warned} |
| ❌ Failed | {stats.failed} |
| 🆕 New | {stats.new} |

## Failed Tests

"""

  FOR result IN grouped.failed:
    md += f"- **{result.path}**: {result.diff_percentage:.2f}% difference\n"

  md += "\n## Warnings\n\n"

  FOR result IN grouped.warned:
    md += f"- **{result.path}**: {result.diff_percentage:.2f}% difference\n"

  md += "\n## New Screenshots\n\n"

  FOR result IN grouped.new:
    md += f"- {result.path}\n"

  RETURN md
```

## Baseline Management

```text
FUNCTION update_baselines(paths):

  baseline_dir = ".visual-regression/baselines"
  current_dir = ".visual-regression/current"

  updated = []

  FOR path IN paths:
    current_path = f"{current_dir}/{path}"
    baseline_path = f"{baseline_dir}/{path}"

    IF NOT exists(current_path):
      WARN f"Current screenshot not found: {path}"
      CONTINUE

    # Backup old baseline
    IF exists(baseline_path):
      backup_path = f"{baseline_dir}/.backup/{path}.{timestamp()}"
      mkdir_p(dirname(backup_path))
      copy(baseline_path, backup_path)

    # Update baseline
    mkdir_p(dirname(baseline_path))
    copy(current_path, baseline_path)

    updated.append(path)
    LOG f"Updated baseline: {path}"

  # Update metadata
  metadata = read_json(f"{baseline_dir}/metadata.json")
  metadata.last_updated = now()
  metadata.updated_screenshots = updated
  write_json(f"{baseline_dir}/metadata.json", metadata)

  RETURN updated


FUNCTION approve_new_baselines():

  report = read_json(".visual-regression/report.json")
  new_screenshots = [r.path FOR r IN report.results WHERE r.status == "new"]

  IF len(new_screenshots) == 0:
    LOG "No new screenshots to approve"
    RETURN []

  RETURN update_baselines(new_screenshots)


FUNCTION approve_all_changes():

  report = read_json(".visual-regression/report.json")
  changed = [r.path FOR r IN report.results WHERE r.status IN ["fail", "warn", "new"]]

  IF len(changed) == 0:
    LOG "No changes to approve"
    RETURN []

  RETURN update_baselines(changed)
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/visual-regression.yml
name: Visual Regression

on:
  pull_request:
    paths:
      - 'design.md'
      - 'templates/**'
      - '.preview/**'

jobs:
  visual-regression:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Playwright
        run: npx playwright install chromium

      - name: Generate previews
        run: speckit preview --screenshots

      - name: Run visual regression
        run: speckit vr run

      - name: Upload report
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: visual-regression-report
          path: .visual-regression/

      - name: Comment on PR
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const summary = fs.readFileSync('.visual-regression/summary.md', 'utf8');

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: summary
            });
```

### GitLab CI Pipeline

```yaml
# .gitlab-ci.yml
visual-regression:
  stage: test
  image: mcr.microsoft.com/playwright:v1.40.0

  script:
    - npm ci
    - speckit preview --screenshots
    - speckit vr run

  artifacts:
    when: on_failure
    paths:
      - .visual-regression/
    reports:
      junit: .visual-regression/report.xml

  rules:
    - changes:
        - design.md
        - templates/**
        - .preview/**
```

## CLI Commands

```bash
# Initialize baselines from current previews
speckit vr init

# Run visual regression tests
speckit vr run

# Run with specific mode
speckit vr run --mode perceptual

# Update specific baselines
speckit vr update components/button/default.desktop.png

# Approve all new baselines
speckit vr approve --new

# Approve all changes
speckit vr approve --all

# Generate report only (no comparison)
speckit vr report

# Open HTML report in browser
speckit vr open

# Clean up diff images
speckit vr clean

# Show diff for specific test
speckit vr diff components/button/hover.desktop.png
```

## Integration with Preview Pipeline

```text
FUNCTION run_preview_with_vr():

  # Generate previews
  preview_result = run_preview_pipeline()

  # Check if baselines exist
  IF NOT exists(".visual-regression/baselines"):
    LOG "No baselines found. Run 'speckit vr init' to create baselines."
    RETURN preview_result

  # Run visual regression
  vr_result = run_visual_regression({
    mode: get_config("visual_regression.mode", "pixel")
  })

  # Check results
  IF vr_result.stats.failed > 0:
    WARN f"Visual regression failed: {vr_result.stats.failed} differences detected"
    DISPLAY "See .visual-regression/report.html for details"

  RETURN {
    preview: preview_result,
    visual_regression: vr_result
  }
```

## Best Practices

### 1. Stable Baselines

```text
✅ DO:
- Use consistent viewport sizes
- Wait for fonts and images to load
- Disable animations during capture
- Use fixed timestamps/dates

❌ DON'T:
- Capture with animations running
- Include dynamic content without masking
- Use different browser versions
- Capture before page is fully loaded
```

### 2. Threshold Tuning

```text
Component Type    | Pass  | Warn  | Fail
------------------|-------|-------|------
Buttons/Icons     | 0.05% | 0.5%  | 2%
Cards/Containers  | 0.1%  | 1%    | 5%
Text-heavy        | 0.5%  | 2%    | 10%
Wireframes        | 1%    | 5%    | 15%
Animations        | 5%    | 10%   | 25%
```

### 3. Ignore Patterns

```json
{
  "ignore_regions": [
    { "selector": "[data-testid='timestamp']" },
    { "selector": ".dynamic-avatar" },
    { "area": { "x": 0, "y": 0, "width": 100, "height": 50 } }
  ]
}
```

### 4. Review Workflow

```text
1. CI fails with visual regression
2. Developer reviews report.html
3. If intentional change:
   - Run: speckit vr approve <path>
   - Commit updated baseline
4. If unintentional change:
   - Fix the code
   - Re-run tests
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| All tests failing | Viewport size changed | Update config and re-init |
| Font rendering differences | System fonts vary | Use web fonts only |
| Anti-aliasing differences | Browser version | Pin browser version |
| Random failures | Animations not disabled | Add animation wait |
| Large diff percentages | Layout shift | Wait for networkidle |

## Configuration Reference

```yaml
# constitution.md
design_system:
  visual_regression:
    enabled: true
    mode: "pixel"  # pixel, perceptual, layout, anti-alias

    thresholds:
      default:
        pass: 0.1
        warn: 1.0
        fail: 5.0

    viewports:
      - name: mobile
        width: 375
        height: 667
      - name: desktop
        width: 1280
        height: 800

    capture:
      wait_for_fonts: true
      wait_for_images: true
      disable_animations: true
      network_idle_timeout: 2000

    reporting:
      html: true
      json: true
      markdown: true
      junit: true  # For CI integration

    ci:
      fail_on_new: false  # Fail if new screenshots detected
      fail_on_missing: true  # Fail if baseline missing
      auto_approve_new: false  # Auto-approve new baselines
```

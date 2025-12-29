# Vision Turbo Mode

## Purpose

Enable parallel browser screenshot capture across multiple viewports to dramatically reduce vision validation time.

## Performance Impact

| Mode | Time | Savings |
|------|------|---------|
| Sequential (current) | 120-240s | baseline |
| Turbo (parallel) | 35-50s | 75-80% |

## Configuration

```yaml
vision_turbo:
  enabled: true
  skip_flag: "--no-turbo"
  max_parallel_contexts: 3
  fallback_on_error: sequential
```

## Parallel Execution Algorithm

```text
PARALLEL_VISION_CHECK(url, viewports, states):

  # 1. Pre-allocate browser contexts (warm up)
  contexts = []
  FOR viewport IN viewports:
    ctx = browser.new_context({
      viewport: {width: viewport.width, height: viewport.height},
      device_scale_factor: 2  # Retina quality
    })
    contexts.append({viewport: viewport.name, ctx: ctx})

  # 2. Build capture tasks (all permutations)
  capture_tasks = []
  FOR EACH ctx_info IN contexts:
    FOR EACH state IN states:
      capture_tasks.append({
        viewport: ctx_info.viewport,
        state: state,
        ctx: ctx_info.ctx,
        url: url
      })

  # 3. Execute captures in parallel (batch by viewport)
  results = []
  FOR EACH viewport_group IN group_by_viewport(capture_tasks):
    # Within same viewport: run states sequentially (same context)
    # Across viewports: run in parallel (different contexts)
    batch_results = await parallel_execute([
      capture_single(task) FOR task IN viewport_group
    ])
    results.extend(batch_results)

  # 4. Close contexts
  FOR ctx_info IN contexts:
    await ctx_info.ctx.close()

  RETURN results


FUNCTION capture_single(task):
  page = await task.ctx.new_page()
  await page.goto(task.url)

  # Trigger state (mock API, click buttons, etc.)
  await trigger_ui_state(page, task.state)

  # Wait for stability
  await page.wait_for_load_state('networkidle')

  # Capture
  filename = f"screenshots/{task.viewport}_{task.state}.png"
  await page.screenshot({path: filename, full_page: false})

  await page.close()
  RETURN {
    viewport: task.viewport,
    state: task.state,
    file: filename
  }
```

## State Triggering

```text
TRIGGER_UI_STATE(page, state):
  SWITCH state:
    CASE "default":
      # No action needed, initial render
      PASS

    CASE "loading":
      # Intercept API calls to delay response
      await page.route("**/api/**", route => route.fulfill({
        status: 200,
        body: null,
        headers: {"X-Delay": "5000"}
      }))
      await page.reload()

    CASE "error":
      # Force API error
      await page.route("**/api/**", route => route.fulfill({
        status: 500,
        body: JSON.stringify({error: "Simulated error"})
      }))
      await page.reload()

    CASE "empty":
      # Return empty data
      await page.route("**/api/**", route => route.fulfill({
        status: 200,
        body: JSON.stringify({data: []})
      }))
      await page.reload()

    CASE "success":
      # Return success with mock data
      await page.route("**/api/**", route => route.fulfill({
        status: 200,
        body: JSON.stringify({success: true, data: mock_data()})
      }))
      await page.reload()
```

## Fallback Mode

If parallel mode fails (browser crash, memory issues):

```text
FALLBACK_SEQUENTIAL(url, viewports, states):
  LOG "⚠️ Vision turbo failed, falling back to sequential mode"

  # Use progressive timeout for warm cache
  results = []
  first_capture = true

  FOR viewport IN viewports:
    ctx = browser.new_context(viewport)

    FOR state IN states:
      timeout = first_capture ? 30000 : 15000  # Warm cache: shorter timeout
      first_capture = false

      result = await capture_with_timeout(ctx, url, state, timeout)
      results.append(result)

    await ctx.close()

  RETURN results
```

## Memory Management

```text
MEMORY_OPTIMIZATION:
  # Limit concurrent screenshots to prevent OOM
  max_concurrent = min(os.cpu_count(), 3)

  # Clear screenshot buffer after analysis
  FOR EACH screenshot IN completed_screenshots:
    analyze_result = await vision_analyze(screenshot)
    os.remove(screenshot.path)  # Free disk space immediately

  # Garbage collect between viewport batches
  gc.collect()
```

## Integration with implement.md

Add to `vision_validation` section:

```yaml
vision_validation:
  enabled: true
  turbo_mode:
    enabled: true
    skip_flag: "--no-turbo"
    max_parallel: 3
    fallback: sequential
  # ... rest of config
```

Reference in Step 1.7:
```text
Read `templates/shared/implement/vision-turbo.md` and apply parallel capture.
```

## Output Format

```text
👁️ Vision Turbo Mode
├── Mode: PARALLEL (3 contexts)
├── Viewports: mobile, tablet, desktop
├── States per viewport: 5 (default, loading, error, empty, success)
├── Total captures: 15
├── Capture time: 42s (vs ~180s sequential)
├── Speedup: 4.3x
└── Status: SUCCESS

Screenshots:
├── mobile_default.png ✓
├── mobile_loading.png ✓
...
```

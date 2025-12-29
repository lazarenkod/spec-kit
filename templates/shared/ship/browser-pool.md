# Browser Pool Management

## Purpose

Pre-warm and reuse browser instances for E2E tests to eliminate cold start overhead and reduce test execution time through efficient resource pooling.

## Performance Impact

| Mode | Time per test | Savings |
|------|---------------|---------|
| Cold start | 3-5s | baseline |
| Warm pool acquire | 200-500ms | 90-95% |
| Context reuse | 50-100ms | 98% |

## Configuration

```yaml
optimization:
  verify:
    browser_pool:
      enabled: true
      skip_flag: "--no-browser-pool"
      min_size: 2                # Minimum warm browsers
      max_size: 8                # Maximum concurrent browsers
      idle_timeout: 60           # seconds before recycling idle browser
      recycle_after: 10          # recycle browser after N tests
      pre_warm_on_deploy: true   # Start warming at 80% deploy
      browsers:
        - chromium               # Primary browser
        - firefox                # Optional secondary
```

## Pool Architecture

```text
BROWSER_POOL_STATE:
  available: []        # Ready to use
  in_use: []           # Currently running tests
  warming: []          # Being initialized
  recycling: []        # Being cleaned up


POOL_METRICS:
  total_acquires: 0
  cache_hits: 0
  cache_misses: 0
  avg_acquire_time_ms: 0
  avg_warm_time_ms: 0
```

## Pool Initialization

```text
FUNCTION initialize_browser_pool(config):
  LOG "🌐 Initializing Browser Pool"

  pool = BrowserPool(
    min_size=config.min_size,
    max_size=config.max_size,
    idle_timeout=config.idle_timeout,
    recycle_after=config.recycle_after
  )

  # Pre-warm minimum browsers
  warm_futures = []
  FOR i IN range(config.min_size):
    future = async_create_browser(config.browsers[0])
    warm_futures.append(future)

  # Wait for all browsers to warm
  FOR future IN warm_futures:
    browser = await future
    pool.available.append(BrowserInstance(
      browser=browser,
      created_at=now(),
      test_count=0,
      browser_type=config.browsers[0]
    ))

  LOG f"✓ Pool initialized with {len(pool.available)} browsers"
  RETURN pool


FUNCTION async_create_browser(browser_type):
  # Launch browser in background
  IF browser_type == "chromium":
    browser = await playwright.chromium.launch(
      headless=true,
      args=["--disable-gpu", "--no-sandbox"]
    )
  ELIF browser_type == "firefox":
    browser = await playwright.firefox.launch(headless=true)
  ELIF browser_type == "webkit":
    browser = await playwright.webkit.launch(headless=true)

  RETURN browser
```

## Acquire / Release Pattern

```text
FUNCTION acquire_browser(pool, test_requirements=None):
  start_time = now()
  POOL_METRICS.total_acquires += 1

  # 1. Try to get from available pool
  IF pool.available:
    instance = select_best_instance(pool.available, test_requirements)
    IF instance:
      pool.available.remove(instance)
      pool.in_use.append(instance)

      acquire_time = now() - start_time
      POOL_METRICS.cache_hits += 1
      POOL_METRICS.avg_acquire_time_ms = update_avg(
        POOL_METRICS.avg_acquire_time_ms,
        acquire_time * 1000
      )

      LOG f"✓ Acquired browser from pool ({acquire_time*1000:.0f}ms)"
      RETURN prepare_context(instance)

  # 2. Pool empty - check if can create new
  IF len(pool.in_use) + len(pool.warming) < pool.max_size:
    POOL_METRICS.cache_misses += 1
    LOG "Creating new browser (pool exhausted)"

    instance = await create_new_instance(pool)
    pool.in_use.append(instance)

    acquire_time = now() - start_time
    LOG f"✓ Created new browser ({acquire_time*1000:.0f}ms)"
    RETURN prepare_context(instance)

  # 3. Pool at max capacity - wait for available
  LOG "Pool at capacity, waiting for available browser..."
  instance = await wait_for_available(pool, timeout=30)

  IF instance IS None:
    RAISE TimeoutError("No browser available within timeout")

  pool.in_use.append(instance)
  RETURN prepare_context(instance)


FUNCTION release_browser(pool, instance, context):
  # 1. Clean up context (fast)
  await context.clear_cookies()
  await context.clear_permissions()

  # 2. Check if needs recycling
  instance.test_count += 1

  IF instance.test_count >= pool.recycle_after:
    LOG f"Recycling browser after {instance.test_count} tests"
    pool.in_use.remove(instance)
    pool.recycling.append(instance)
    schedule_recycle(pool, instance)
    RETURN

  # 3. Check if browser healthy
  IF NOT await is_browser_healthy(instance):
    LOG "Browser unhealthy, recycling"
    pool.in_use.remove(instance)
    schedule_recycle(pool, instance)
    RETURN

  # 4. Return to pool
  pool.in_use.remove(instance)
  pool.available.append(instance)
  LOG "Browser returned to pool"


FUNCTION prepare_context(instance):
  # Create fresh context with clean state
  context = await instance.browser.new_context(
    viewport={"width": 1280, "height": 720},
    ignore_https_errors=true
  )

  # Enable tracing for debugging (optional)
  IF DEBUG_MODE:
    await context.tracing.start(screenshots=true, snapshots=true)

  RETURN context
```

## Pre-warming Strategy

```text
FUNCTION pre_warm_on_deploy_progress(pool, progress_percent):
  # Start warming browsers when deploy is 80% complete
  IF progress_percent < 80:
    RETURN

  IF pool.pre_warm_triggered:
    RETURN

  pool.pre_warm_triggered = true
  LOG "🔥 Pre-warming browser pool (deploy at 80%)"

  # Calculate how many to warm
  target_warm = pool.min_size
  current_warm = len(pool.available) + len(pool.warming)
  need_to_warm = target_warm - current_warm

  IF need_to_warm <= 0:
    RETURN

  # Warm in background
  FOR i IN range(need_to_warm):
    schedule_background_warm(pool)


FUNCTION schedule_background_warm(pool):
  async_task = async_create_browser(pool.default_browser)
  pool.warming.append(async_task)

  WHEN async_task.complete:
    browser = async_task.result()
    instance = BrowserInstance(
      browser=browser,
      created_at=now(),
      test_count=0
    )
    pool.warming.remove(async_task)
    pool.available.append(instance)
    LOG f"✓ Background warm complete ({len(pool.available)} available)"
```

## Idle Management

```text
FUNCTION start_idle_monitor(pool):
  # Run every 10 seconds
  SCHEDULE_EVERY(10_seconds):
    check_idle_browsers(pool)


FUNCTION check_idle_browsers(pool):
  now_time = now()
  browsers_to_close = []

  FOR instance IN pool.available:
    idle_time = now_time - instance.last_used_at

    IF idle_time > pool.idle_timeout:
      # Keep minimum browsers warm
      IF len(pool.available) - len(browsers_to_close) <= pool.min_size:
        CONTINUE

      browsers_to_close.append(instance)

  FOR instance IN browsers_to_close:
    pool.available.remove(instance)
    LOG f"Closing idle browser (idle for {idle_time}s)"
    schedule_close(instance)


FUNCTION schedule_close(instance):
  TRY:
    await instance.browser.close()
  EXCEPT:
    PASS  # Browser may already be closed
```

## Health Checking

```text
FUNCTION is_browser_healthy(instance):
  TRY:
    # Quick health check - try to create/close context
    context = await instance.browser.new_context()
    page = await context.new_page()

    # Simple navigation test
    await page.goto("about:blank", timeout=5000)
    await page.close()
    await context.close()

    RETURN true

  EXCEPT:
    RETURN false


FUNCTION schedule_recycle(pool, instance):
  async_task:
    TRY:
      await instance.browser.close()
    EXCEPT:
      PASS

    pool.recycling.remove(instance)

    # Create replacement if below min_size
    IF len(pool.available) < pool.min_size:
      new_instance = await create_new_instance(pool)
      pool.available.append(new_instance)
      LOG "✓ Replacement browser created"
```

## Multi-Browser Support

```text
FUNCTION select_best_instance(available, requirements):
  # Filter by browser type if specified
  IF requirements AND requirements.browser_type:
    matching = [i FOR i IN available IF i.browser_type == requirements.browser_type]
    IF matching:
      # Prefer least-used browser
      RETURN min(matching, key=lambda x: x.test_count)

  # Default: prefer least-used of any type
  IF available:
    RETURN min(available, key=lambda x: x.test_count)

  RETURN None


FUNCTION ensure_browser_type_available(pool, browser_type):
  # Check if we have this browser type warming or available
  available_types = [i.browser_type FOR i IN pool.available]
  warming_types = [t.browser_type FOR t IN pool.warming IF hasattr(t, 'browser_type')]

  IF browser_type NOT IN available_types + warming_types:
    LOG f"Creating {browser_type} browser (not in pool)"
    schedule_background_warm(pool, browser_type=browser_type)
```

## Integration with ship.md

```text
# At verify phase preparation:
Read `templates/shared/ship/browser-pool.md` and apply.

# Initialize pool early (during deploy):
ON_DEPLOY_PROGRESS(80%):
  browser_pool = initialize_browser_pool(config)
  pre_warm_on_deploy_progress(browser_pool, 80)

# In tests:
INSTEAD OF:
  browser = playwright.chromium.launch()
  page = browser.new_page()
  # ... test ...
  browser.close()

USE:
  context = acquire_browser(browser_pool)
  page = context.new_page()
  # ... test ...
  release_browser(browser_pool, instance, context)
```

## Output Format

```text
🌐 Browser Pool
├── Configuration:
│   ├── Min size: 2
│   ├── Max size: 8
│   ├── Idle timeout: 60s
│   └── Recycle after: 10 tests
├── Pre-warm:
│   ├── Triggered at: Deploy 80%
│   ├── Warm time: 1.2s
│   └── Browsers ready: 2
├── Usage:
│   ├── Total acquires: 28
│   ├── Cache hits: 26 (93%)
│   ├── Cache misses: 2
│   ├── Avg acquire time: 180ms
│   └── Avg cold start: 3.2s
├── Current State:
│   ├── Available: 3
│   ├── In use: 1
│   └── Recycling: 0
└── Time saved: ~78s (vs cold starts)
```

## CLI Flags

```bash
# Disable browser pool
speckit ship --no-browser-pool

# Override pool size
speckit ship --browser-pool-size=4

# Use specific browser
speckit ship --browser=firefox

# Disable pre-warming
speckit ship --no-pre-warm
```

## Playwright Integration Example

```javascript
// test-setup.js
const { browserPool } = require('@speckit/browser-pool');

let poolContext;

beforeAll(async () => {
  poolContext = await browserPool.acquire();
});

afterAll(async () => {
  await browserPool.release(poolContext);
});

beforeEach(async () => {
  // Clear state between tests (fast)
  await poolContext.clearCookies();
  await poolContext.clearPermissions();
});
```

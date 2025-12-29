# Parallel Test Execution

## Purpose

Execute tests in parallel with intelligent grouping, resource management, and fast-fail strategies to reduce verification time by 65-75%.

## Performance Impact

| Mode | Time | Savings |
|------|------|---------|
| Sequential tests | 60-90s | baseline |
| Parallel tests | 15-30s | 65-75% |
| With caching | 5-15s | 80-90% |

## Configuration

```yaml
optimization:
  verify:
    parallel_tests: true
    skip_flag: "--sequential-tests"
    max_workers: 4               # Max parallel test processes
    fast_fail: true              # Stop on first critical failure
    group_strategy: "type"       # type | file | smart
    timeout_per_test: 30         # seconds
    retry_flaky: 1               # Retry count for flaky tests
```

## Test Grouping Strategy

```text
TEST_GROUPS:
  smoke:
    priority: 1              # Run first
    parallel: true
    max_workers: 4
    fast_fail: true          # Stop all if smoke fails
    timeout: 30s

  acceptance:
    priority: 2
    parallel: true
    max_workers: 2           # More resource intensive
    fast_fail: false
    timeout: 60s

  security:
    priority: 3
    parallel: false          # Sequential for auth state
    fast_fail: true
    timeout: 120s

  performance:
    priority: 4
    parallel: true
    max_workers: 8           # Many small tests
    fast_fail: false
    timeout: 300s


FUNCTION group_tests(test_files):
  groups = {
    smoke: [],
    acceptance: [],
    security: [],
    performance: []
  }

  FOR test_file IN test_files:
    group = detect_test_group(test_file)
    groups[group].append(test_file)

  RETURN groups


FUNCTION detect_test_group(test_file):
  # By filename pattern
  IF "smoke" IN test_file.lower():
    RETURN "smoke"
  IF "security" IN test_file.lower() OR "auth" IN test_file.lower():
    RETURN "security"
  IF "perf" IN test_file.lower() OR "performance" IN test_file.lower():
    RETURN "performance"

  # By directory
  IF "/smoke/" IN test_file:
    RETURN "smoke"
  IF "/e2e/" IN test_file OR "/acceptance/" IN test_file:
    RETURN "acceptance"

  # Default
  RETURN "acceptance"
```

## Parallel Execution Engine

```text
FUNCTION parallel_test_executor(test_group, config):
  IF NOT config.parallel:
    # Sequential execution
    RETURN sequential_run(test_group.tests)

  # Create worker pool
  pool = WorkerPool(max_workers=config.max_workers)
  results = []
  failed_critical = false

  # Submit all tests to pool
  futures = []
  FOR test IN test_group.tests:
    future = pool.submit(run_single_test, test, config.timeout)
    futures.append((test, future))

  # Collect results with fast-fail check
  FOR test, future IN futures:
    IF failed_critical AND config.fast_fail:
      future.cancel()
      results.append(TestResult(test, status="cancelled"))
      CONTINUE

    TRY:
      result = future.result(timeout=config.timeout)
      results.append(result)

      IF result.failed AND config.fast_fail:
        failed_critical = true
        LOG f"✗ Fast-fail triggered by {test.name}"

    EXCEPT TimeoutError:
      results.append(TestResult(test, status="timeout"))
      IF config.fast_fail:
        failed_critical = true

  pool.shutdown()
  RETURN results


FUNCTION run_single_test(test, timeout):
  start_time = now()

  TRY:
    result = execute_test(test, timeout)
    duration = now() - start_time

    RETURN TestResult(
      test=test,
      status="passed" IF result.exit_code == 0 ELSE "failed",
      duration=duration,
      output=result.output
    )

  EXCEPT Exception AS e:
    RETURN TestResult(
      test=test,
      status="error",
      error=str(e)
    )
```

## Smart Test Ordering

```text
FUNCTION order_tests_smart(tests):
  # Prioritize tests by:
  # 1. Historical failure rate (run failing tests first)
  # 2. Historical duration (run slow tests first for better parallelization)
  # 3. File modification time (recently changed first)

  test_metrics = load_test_metrics()

  scored_tests = []
  FOR test IN tests:
    metrics = test_metrics.get(test.name, {})

    score = 0
    # Higher score = run earlier

    # Failure rate: prioritize historically failing tests
    failure_rate = metrics.get("failure_rate", 0)
    score += failure_rate * 100

    # Duration: prioritize slow tests (better parallelization)
    avg_duration = metrics.get("avg_duration", 10)
    score += avg_duration * 2

    # Recency: prioritize recently modified
    IF test.file IN recently_modified_files():
      score += 50

    scored_tests.append((score, test))

  # Sort by score descending
  scored_tests.sort(key=lambda x: -x[0])

  RETURN [test FOR score, test IN scored_tests]
```

## Flaky Test Handling

```text
FLAKY_TEST_REGISTRY = ".speckit/metrics/flaky-tests.json"

FUNCTION handle_flaky_test(test, initial_result, retry_count):
  IF initial_result.passed:
    RETURN initial_result

  IF NOT is_flaky(test):
    RETURN initial_result

  LOG f"⚠ Retrying flaky test: {test.name}"

  FOR attempt IN range(1, retry_count + 1):
    result = run_single_test(test, test.timeout * 1.5)  # Extended timeout for retry

    IF result.passed:
      LOG f"✓ Flaky test passed on retry {attempt}"
      record_flaky_result(test, "passed_on_retry", attempt)
      RETURN result

  LOG f"✗ Flaky test failed after {retry_count} retries"
  record_flaky_result(test, "failed_after_retries", retry_count)
  RETURN initial_result


FUNCTION is_flaky(test):
  registry = json.load(FLAKY_TEST_REGISTRY) IF exists(FLAKY_TEST_REGISTRY) ELSE {}
  test_record = registry.get(test.name)

  IF NOT test_record:
    RETURN false

  # Consider flaky if > 10% failure rate with > 5 runs
  IF test_record.total_runs > 5:
    failure_rate = test_record.failures / test_record.total_runs
    IF 0.1 < failure_rate < 0.5:  # Between 10-50% failure
      RETURN true

  RETURN false


FUNCTION record_flaky_result(test, outcome, attempts):
  registry = json.load(FLAKY_TEST_REGISTRY) IF exists(FLAKY_TEST_REGISTRY) ELSE {}

  IF test.name NOT IN registry:
    registry[test.name] = {
      total_runs: 0,
      failures: 0,
      retries_needed: 0
    }

  registry[test.name].total_runs += 1
  IF outcome == "failed_after_retries":
    registry[test.name].failures += 1
  IF outcome == "passed_on_retry":
    registry[test.name].retries_needed += 1

  json.dump(FLAKY_TEST_REGISTRY, registry)
```

## Resource Management

```text
RESOURCE_LIMITS:
  max_memory_per_worker: "2G"
  max_cpu_per_worker: 2
  shared_resources:
    database: 1              # Only 1 test can use DB at a time
    browser: 4               # Up to 4 browser instances


FUNCTION allocate_resources(test, available_resources):
  required = test.resource_requirements

  # Check if resources available
  FOR resource, count IN required:
    IF available_resources[resource] < count:
      RETURN None  # Can't run yet

  # Allocate resources
  FOR resource, count IN required:
    available_resources[resource] -= count

  RETURN ResourceAllocation(test, required)


FUNCTION release_resources(allocation, available_resources):
  FOR resource, count IN allocation.required:
    available_resources[resource] += count
```

## Orchestrated Execution

```text
FUNCTION orchestrated_test_execution(test_files, config):
  LOG "🧪 Parallel Test Execution"

  # 1. Group tests
  groups = group_tests(test_files)

  # 2. Order by priority
  ordered_groups = sorted(groups.items(), key=lambda x: TEST_GROUPS[x[0]].priority)

  all_results = []
  critical_failure = false

  FOR group_name, tests IN ordered_groups:
    IF critical_failure AND TEST_GROUPS[group_name].priority > 1:
      LOG f"⏭ Skipping {group_name} due to critical failure"
      CONTINUE

    group_config = TEST_GROUPS[group_name]
    LOG f"\n📋 Running {group_name} tests ({len(tests)} tests, workers={group_config.max_workers})"

    # Smart ordering within group
    ordered_tests = order_tests_smart(tests)

    # Execute
    results = parallel_test_executor(
      TestGroup(name=group_name, tests=ordered_tests),
      group_config
    )

    # Handle flaky tests
    FOR result IN results:
      IF result.failed:
        result = handle_flaky_test(result.test, result, config.retry_flaky)

    all_results.extend(results)

    # Check for critical failures
    failures = [r FOR r IN results IF r.failed]
    IF failures AND group_config.fast_fail:
      critical_failure = true
      LOG f"✗ {len(failures)} failures in {group_name} - fast-fail triggered"

  RETURN TestSummary(all_results)
```

## Integration with ship.md

```text
# At verify phase start:
Read `templates/shared/ship/test-parallel.md` and apply.

# Replace standard test run:
INSTEAD OF:
  npm test
  # or
  pytest tests/

USE:
  summary = orchestrated_test_execution(test_files, config)
```

## Output Format

```text
🧪 Parallel Test Execution
├── Test Discovery:
│   ├── smoke: 5 tests
│   ├── acceptance: 12 tests
│   ├── security: 3 tests
│   └── performance: 8 tests
│
├── 📋 smoke (workers=4, fast-fail=true)
│   ├── ✓ test_homepage_loads (0.8s)
│   ├── ✓ test_api_health (0.3s)
│   ├── ✓ test_auth_endpoint (1.2s)
│   ├── ✓ test_db_connection (0.5s)
│   └── ✓ test_cache_ping (0.2s)
│   └── Duration: 1.5s (parallel)
│
├── 📋 acceptance (workers=2)
│   ├── ✓ test_user_login (2.1s)
│   ├── ✓ test_create_order (3.4s)
│   ├── ⚠ test_payment_flow (4.2s, retry 1)
│   └── ... 9 more passed
│   └── Duration: 8.3s (parallel)
│
├── 📋 security (sequential)
│   ├── ✓ test_xss_protection (1.8s)
│   ├── ✓ test_csrf_tokens (1.2s)
│   └── ✓ test_sql_injection (2.1s)
│   └── Duration: 5.1s
│
├── Summary:
│   ├── Total: 28 tests
│   ├── Passed: 27
│   ├── Failed: 0
│   ├── Flaky (retried): 1
│   └── Duration: 14.9s (vs ~75s sequential)
│
└── Result: SUCCESS ✓
```

## CLI Flags

```bash
# Run specific group only
speckit ship --tests=smoke

# Override worker count
speckit ship --parallel-tests=8

# Disable fast-fail
speckit ship --no-fast-fail

# Run all tests sequentially
speckit ship --sequential-tests

# Skip flaky test retries
speckit ship --no-retry-flaky
```

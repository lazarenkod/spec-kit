# Incremental Test Selection

## Purpose

Execute only tests affected by code changes through intelligent code-to-test mapping, reducing test execution time by 70-85% while maintaining confidence in change coverage.

## Performance Impact

| Mode | Time | Coverage |
|------|------|----------|
| Full test suite | 60-120s | 100% |
| Incremental selection | 10-30s | Changed code only |
| With caching | 5-15s | Skip unchanged |

## Configuration

```yaml
optimization:
  verify:
    incremental_tests:
      enabled: true
      skip_flag: "--full-tests"
      mapping_strategy: coverage    # coverage | static | hybrid
      fallback_to_full: true        # Run full suite if mapping fails
      mapping_cache_ttl: 86400      # 24 hours
      min_coverage_threshold: 0.8   # Require 80% mapping coverage
```

## Test Mapping Strategies

### Coverage-Based Mapping

```text
COVERAGE_MAPPING:
  description: "Build map from actual test coverage data"
  accuracy: HIGH
  setup_cost: MEDIUM
  maintenance: AUTO

  FUNCTION build_coverage_map():
    # Run tests with coverage instrumentation
    coverage_data = run_tests_with_coverage()

    # Build source-to-test map
    source_to_tests = {}

    FOR test_file, coverage IN coverage_data:
      FOR source_file, lines IN coverage.covered_files:
        IF source_file NOT IN source_to_tests:
          source_to_tests[source_file] = set()
        source_to_tests[source_file].add(test_file)

    save_mapping(source_to_tests, ".speckit/test-mapping/coverage-map.json")
    RETURN source_to_tests


  FUNCTION update_coverage_map(changed_files, existing_map):
    # Only re-run tests for changed files to update their coverage
    affected_tests = set()

    FOR file IN changed_files:
      IF file IN existing_map:
        affected_tests.update(existing_map[file])

    # Run affected tests with coverage
    new_coverage = run_tests_with_coverage(affected_tests)

    # Update map
    FOR test_file, coverage IN new_coverage:
      FOR source_file, lines IN coverage.covered_files:
        existing_map[source_file].add(test_file)

    save_mapping(existing_map, ".speckit/test-mapping/coverage-map.json")
    RETURN existing_map
```

### Static Analysis Mapping

```text
STATIC_MAPPING:
  description: "Build map from import/dependency analysis"
  accuracy: MEDIUM
  setup_cost: LOW
  maintenance: AUTO

  FUNCTION build_static_map():
    source_to_tests = {}

    # Analyze test files for imports
    test_files = glob("tests/**/*.{ts,js,py,go}")

    FOR test_file IN test_files:
      imports = extract_imports(test_file)

      FOR import_path IN imports:
        source_file = resolve_import_path(import_path)
        IF source_file:
          IF source_file NOT IN source_to_tests:
            source_to_tests[source_file] = set()
          source_to_tests[source_file].add(test_file)

    save_mapping(source_to_tests, ".speckit/test-mapping/static-map.json")
    RETURN source_to_tests


  FUNCTION extract_imports(test_file):
    content = read_file(test_file)
    imports = []

    # Language-specific import patterns
    patterns = {
      ".ts": [r'import .* from ["\'](.+)["\']', r'require\(["\'](.+)["\']\)'],
      ".js": [r'import .* from ["\'](.+)["\']', r'require\(["\'](.+)["\']\)'],
      ".py": [r'from (\S+) import', r'import (\S+)'],
      ".go": [r'import "(.+)"', r'"(.+)"']
    }

    ext = get_extension(test_file)
    FOR pattern IN patterns.get(ext, []):
      matches = regex.findall(pattern, content)
      imports.extend(matches)

    RETURN imports
```

### Hybrid Mapping

```text
HYBRID_MAPPING:
  description: "Combine coverage and static analysis"
  accuracy: HIGHEST
  setup_cost: MEDIUM
  maintenance: AUTO

  FUNCTION build_hybrid_map():
    # Start with static map (fast, always available)
    static_map = build_static_map()

    # Enhance with coverage data if available
    coverage_map = load_coverage_map() IF exists(".speckit/test-mapping/coverage-map.json") ELSE {}

    # Merge maps
    hybrid_map = {}

    # Union of both maps
    all_sources = set(static_map.keys()) | set(coverage_map.keys())

    FOR source IN all_sources:
      static_tests = static_map.get(source, set())
      coverage_tests = coverage_map.get(source, set())
      hybrid_map[source] = static_tests | coverage_tests

    # Add confidence scores
    FOR source, tests IN hybrid_map:
      FOR test IN tests:
        in_static = test IN static_map.get(source, set())
        in_coverage = test IN coverage_map.get(source, set())

        confidence = 0.0
        IF in_static AND in_coverage:
          confidence = 1.0
        ELIF in_coverage:
          confidence = 0.9
        ELIF in_static:
          confidence = 0.7

        hybrid_map[source][test] = {"test": test, "confidence": confidence}

    save_mapping(hybrid_map, ".speckit/test-mapping/hybrid-map.json")
    RETURN hybrid_map
```

## Change Detection

```text
FUNCTION detect_changed_files(since=None):
  IF since IS None:
    # Default: changes since last successful test run
    since = read_file(".speckit/state/last-test-commit") OR "HEAD~1"

  # Get changed files
  result = run(f"git diff --name-only {since} HEAD")
  changed_files = result.stdout.strip().split("\n")

  # Categorize changes
  categorized = {
    source: [],
    tests: [],
    config: [],
    infra: [],
    docs: []
  }

  FOR file IN changed_files:
    IF file.startswith("tests/") OR file.endswith(".test.ts") OR file.endswith("_test.go"):
      categorized.tests.append(file)
    ELIF file.startswith("infra/") OR file.endswith(".tf"):
      categorized.infra.append(file)
    ELIF file.endswith(".md") OR file.startswith("docs/"):
      categorized.docs.append(file)
    ELIF file IN ["package.json", "go.mod", "pyproject.toml", "Cargo.toml"]:
      categorized.config.append(file)
    ELSE:
      categorized.source.append(file)

  RETURN categorized


FUNCTION should_run_full_suite(categorized_changes):
  # Run full suite if config files changed
  IF categorized_changes.config:
    LOG "Config files changed, running full suite"
    RETURN True

  # Run full suite if test infrastructure changed
  test_infra_files = ["jest.config.js", "pytest.ini", "conftest.py", "setup.ts"]
  IF any(f IN categorized_changes.tests FOR f IN test_infra_files):
    LOG "Test infrastructure changed, running full suite"
    RETURN True

  RETURN False
```

## Test Selection Algorithm

```text
FUNCTION select_affected_tests(changed_files, test_map):
  affected_tests = set()
  unmapped_files = []

  FOR file IN changed_files:
    IF file IN test_map:
      tests = test_map[file]
      affected_tests.update(tests)
      LOG f"  {file} → {len(tests)} tests"
    ELSE:
      unmapped_files.append(file)
      LOG f"  {file} → (unmapped)"

  # Handle unmapped files
  IF unmapped_files:
    coverage_ratio = (len(changed_files) - len(unmapped_files)) / len(changed_files)

    IF coverage_ratio < config.min_coverage_threshold:
      LOG f"⚠ Low mapping coverage ({coverage_ratio:.0%}), falling back to related tests"
      related = find_related_tests(unmapped_files)
      affected_tests.update(related)

  # Add tests that were directly changed
  FOR file IN changed_files:
    IF is_test_file(file):
      affected_tests.add(file)

  # Deduplicate and sort
  affected_tests = sorted(set(affected_tests))

  LOG f"\nSelected {len(affected_tests)} tests for {len(changed_files)} changed files"
  RETURN affected_tests


FUNCTION find_related_tests(unmapped_files):
  related_tests = set()

  FOR file IN unmapped_files:
    # Try to find tests with similar names
    base_name = get_base_name(file)
    potential_tests = [
      f"tests/{base_name}.test.ts",
      f"tests/{base_name}_test.py",
      f"tests/{base_name}_test.go",
      f"tests/test_{base_name}.py",
      f"__tests__/{base_name}.test.js"
    ]

    FOR test_path IN potential_tests:
      IF exists(test_path):
        related_tests.add(test_path)

    # Try to find tests in same directory
    dir_path = get_directory(file)
    test_dir = dir_path.replace("src/", "tests/")
    IF exists(test_dir):
      related_tests.update(glob(f"{test_dir}/*.test.*"))

  RETURN related_tests
```

## Test Ordering

```text
FUNCTION order_selected_tests(tests, test_metrics):
  scored_tests = []

  FOR test IN tests:
    metrics = test_metrics.get(test, {})

    score = 0

    # Priority 1: Recent failures (run first to fail fast)
    IF metrics.get("last_failed"):
      days_since_fail = (now() - metrics.last_failed).days
      IF days_since_fail < 7:
        score += 100 - (days_since_fail * 10)

    # Priority 2: Flaky tests (run early to catch issues)
    flakiness = metrics.get("flakiness_score", 0)
    IF flakiness > 0.1:
      score += 50

    # Priority 3: Fast tests (run first for quick feedback)
    avg_duration = metrics.get("avg_duration", 10)
    IF avg_duration < 1:
      score += 30
    ELIF avg_duration < 5:
      score += 20
    ELIF avg_duration < 10:
      score += 10

    # Priority 4: High-value tests (cover critical paths)
    IF metrics.get("critical_path"):
      score += 40

    scored_tests.append((score, test))

  # Sort by score (highest first)
  scored_tests.sort(key=lambda x: -x[0])

  RETURN [test FOR score, test IN scored_tests]
```

## Mapping Maintenance

```text
MAPPING_MAINTENANCE:
  # Automatic map updates

  ON_TEST_RUN:
    IF coverage_enabled:
      update_coverage_map(ran_tests, new_coverage)

  ON_NEW_FILE:
    # Add to static map immediately
    imports = extract_imports(new_file) IF is_test_file(new_file) ELSE []
    update_static_map(new_file, imports)

  ON_FILE_RENAME:
    # Update both old and new paths
    update_mapping_paths(old_path, new_path)

  ON_FILE_DELETE:
    remove_from_mapping(deleted_path)

  SCHEDULED(weekly):
    # Full rebuild for accuracy
    rebuild_coverage_map()
    rebuild_static_map()
    merge_to_hybrid()


FUNCTION validate_mapping_accuracy():
  # Sample validation: run selected tests and check coverage
  changed = sample_changed_files(10)
  selected = select_affected_tests(changed, test_map)

  # Run selected tests with coverage
  coverage = run_tests_with_coverage(selected)

  # Check if changed files are actually covered
  covered_files = extract_covered_files(coverage)
  accuracy = len(set(changed) & covered_files) / len(changed)

  IF accuracy < 0.9:
    LOG f"⚠ Mapping accuracy low ({accuracy:.0%}), triggering rebuild"
    schedule_mapping_rebuild()

  RETURN accuracy
```

## Incremental Execution Flow

```text
FUNCTION incremental_test_execution(config):
  LOG "🔍 Incremental Test Selection"

  # 1. Detect changes
  changes = detect_changed_files()
  LOG f"Changed files: {len(changes.source)} source, {len(changes.tests)} tests"

  # 2. Check if full suite needed
  IF should_run_full_suite(changes):
    RETURN run_full_test_suite()

  # 3. Skip if only docs changed
  IF changes.docs AND NOT (changes.source OR changes.tests):
    LOG "Only documentation changed, skipping tests"
    RETURN TestResult(skipped=True, reason="docs_only")

  # 4. Load test mapping
  test_map = load_test_mapping(config.mapping_strategy)

  IF NOT test_map:
    LOG "No test mapping available, building..."
    test_map = build_test_mapping(config.mapping_strategy)

  # 5. Select affected tests
  affected = select_affected_tests(changes.source + changes.tests, test_map)

  IF NOT affected:
    LOG "No tests affected by changes"
    IF config.run_smoke_on_no_affected:
      LOG "Running smoke tests as fallback"
      RETURN run_smoke_tests()
    RETURN TestResult(skipped=True, reason="no_affected")

  # 6. Order tests for optimal execution
  test_metrics = load_test_metrics()
  ordered_tests = order_selected_tests(affected, test_metrics)

  # 7. Execute
  LOG f"\n📋 Running {len(ordered_tests)} selected tests"
  results = run_tests(ordered_tests)

  # 8. Update metrics
  update_test_metrics(results)

  # 9. Save last test commit
  save_last_test_commit(get_current_commit())

  RETURN results
```

## Integration with ship.md

```text
# At verify phase:
Read `templates/shared/ship/incremental-tests.md` and apply.

# Replace standard test execution:
INSTEAD OF:
  npm test
  # or
  pytest

USE:
  results = incremental_test_execution(config)
  IF results.skipped:
    LOG f"Tests skipped: {results.reason}"
  ELIF results.failed:
    FAIL_SHIP("Tests failed")
```

## Output Format

```text
🔍 Incremental Test Selection
├── Change Detection:
│   ├── Since: abc123 (last successful)
│   ├── Source files: 5
│   ├── Test files: 1
│   └── Config files: 0
├── Test Mapping:
│   ├── Strategy: hybrid
│   ├── Map coverage: 94%
│   └── Last updated: 2h ago
├── Selection:
│   ├── src/auth/login.ts → 3 tests
│   ├── src/auth/session.ts → 2 tests
│   ├── src/api/users.ts → 4 tests
│   ├── tests/auth.test.ts → (directly changed)
│   └── Total: 9 tests (vs 127 in full suite)
├── Execution:
│   ├── auth.test.ts: ✓ 4/4 passed (1.2s)
│   ├── session.test.ts: ✓ 2/2 passed (0.8s)
│   ├── users.test.ts: ✓ 4/4 passed (1.5s)
│   └── api-integration.test.ts: ✓ 3/3 passed (2.1s)
├── Summary:
│   ├── Tests run: 13
│   ├── Passed: 13
│   ├── Failed: 0
│   └── Duration: 5.6s (vs ~45s full suite)
└── Result: SUCCESS ✓
```

## CLI Flags

```bash
# Run full test suite
speckit ship --full-tests

# Use specific mapping strategy
speckit ship --test-mapping=coverage

# Rebuild test mapping
speckit ship --rebuild-test-map

# Show affected tests without running
speckit ship --show-affected-tests

# Include tests for specific files
speckit ship --test-files=src/auth/*.ts
```

## Language-Specific Implementations

```text
LANGUAGE_CONFIGS:

  typescript:
    test_patterns: ["**/*.test.ts", "**/*.spec.ts", "__tests__/**/*.ts"]
    import_pattern: r'import .* from ["\'](.+)["\']'
    coverage_tool: "nyc"
    test_runner: "jest"

  python:
    test_patterns: ["tests/**/test_*.py", "tests/**/*_test.py"]
    import_pattern: r'from (\S+) import|import (\S+)'
    coverage_tool: "coverage"
    test_runner: "pytest"

  go:
    test_patterns: ["**/*_test.go"]
    import_pattern: r'import "(.+)"'
    coverage_tool: "go test -cover"
    test_runner: "go test"

  rust:
    test_patterns: ["**/tests/*.rs", "**/*_test.rs"]
    import_pattern: r'use (\S+)::'
    coverage_tool: "cargo tarpaulin"
    test_runner: "cargo test"


FUNCTION get_language_config():
  # Detect from project files
  IF exists("package.json"):
    RETURN LANGUAGE_CONFIGS.typescript
  IF exists("pyproject.toml") OR exists("setup.py"):
    RETURN LANGUAGE_CONFIGS.python
  IF exists("go.mod"):
    RETURN LANGUAGE_CONFIGS.go
  IF exists("Cargo.toml"):
    RETURN LANGUAGE_CONFIGS.rust

  RETURN LANGUAGE_CONFIGS.typescript  # Default
```

## Test Mapping Storage

```text
MAPPING_STORAGE:
  directory: ".speckit/test-mapping/"
  files:
    coverage_map: "coverage-map.json"
    static_map: "static-map.json"
    hybrid_map: "hybrid-map.json"
    test_metrics: "test-metrics.json"

  # Example coverage-map.json:
  {
    "src/auth/login.ts": [
      "tests/auth/login.test.ts",
      "tests/integration/auth.test.ts"
    ],
    "src/api/users.ts": [
      "tests/api/users.test.ts",
      "tests/e2e/user-flow.test.ts"
    ]
  }

  # Example test-metrics.json:
  {
    "tests/auth/login.test.ts": {
      "avg_duration": 1.2,
      "last_run": "2024-01-15T10:30:00Z",
      "last_failed": null,
      "flakiness_score": 0.02,
      "critical_path": true,
      "run_count": 234
    }
  }
```

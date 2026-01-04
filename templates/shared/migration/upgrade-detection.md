# Version Upgrade Detection

Detect outdated dependencies, fetch breaking changes, analyze codebase impact, and generate ordered upgrade paths with validation tests.

## Supported Ecosystems

| Ecosystem | Version Files | Lock Files |
|-----------|--------------|------------|
| Node.js | `package.json`, `.nvmrc`, `.node-version` | `package-lock.json`, `yarn.lock` |
| Python | `requirements.txt`, `pyproject.toml` | `poetry.lock`, `Pipfile.lock` |
| Go | `go.mod` | `go.sum` |
| Rust | `Cargo.toml` | `Cargo.lock` |
| Database | `docker-compose.yml`, `*.tf` | PostgreSQL, MySQL, Redis |

## VERSION_DETECTION

```text
FUNCTION detect_versions():
  versions = {}
  IF exists(package.json): versions.nodejs = {runtime: read(".nvmrc"), deps: pkg.dependencies}
  IF exists(pyproject.toml): versions.python = {runtime: requires-python, deps: dependencies}
  IF exists(go.mod): versions.go = {runtime: gomod.go, deps: gomod.require}
  IF exists(Cargo.toml): versions.rust = {edition: package.edition, deps: dependencies}
  versions.databases = detect_from_docker_compose_or_terraform()
  RETURN versions
```

## BREAKING_CHANGE_FETCH

```text
SOURCES = {npm: "registry.npmjs.org", pypi: "pypi.org", go: "proxy.golang.org", crates: "crates.io"}

FUNCTION fetch_breaking_changes(package, current, target):
  changelog = fetch_changelog(package)
  breaking = []
  FOR version IN versions_between(current, target):
    IF matches_pattern(changelog[version], BREAKING_PATTERNS):
      breaking.append({id: generate_id("UPG"), version, changes, migration_guide})
  RETURN breaking

BREAKING_PATTERNS = [/BREAKING/, /removed|deprecated|renamed/, /migration required/]
```

## IMPACT_ANALYSIS

```text
FUNCTION analyze_impact(breaking_changes, codebase):
  FOR change IN breaking_changes:
    affected = grep(codebase, change.affected_apis)
    YIELD {
      upgrade_id: change.id, package: change.package,
      from: change.current, to: change.target,
      affected_files: affected, severity: calculate_severity(len(affected)),
      effort: estimate_effort(affected)
    }

SEVERITY = {CRITICAL: ">20 files", HIGH: "10-20", MEDIUM: "5-10", LOW: "<5", NONE: "0"}
```

## UPGRADE_PATH_GENERATION

```text
FUNCTION generate_upgrade_path(impact_report):
  dep_graph = build_dependency_graph(impact_report)
  ordered = topological_sort(dep_graph)

  FOR idx, upgrade IN enumerate(ordered):
    YIELD {
      id: f"UPG-{idx+1:03d}",
      package: upgrade.package,
      from: upgrade.current, to: upgrade.target,
      depends_on: [u.id FOR u IN upgrade.blockers],
      affected_files: len(upgrade.affected),
      effort: upgrade.effort, validation_required: upgrade.has_breaking
    }

OUTPUT_FORMAT:
| UPG-001 | typescript | 4.9 | 5.3 | - | ~2h |
| UPG-002 | react | 17.0 | 18.2 | UPG-001 | ~8h |
```

## VALIDATION_TESTS

```text
FUNCTION generate_validation_tests(upgrade_path):
  FOR upgrade IN upgrade_path:
    test_suite = {id: f"{upgrade.id}-VAL", cases: []}

    # API compatibility
    FOR api IN upgrade.affected_apis:
      test_suite.cases.append({name: f"API {api} works", type: "compatibility"})

    # Regression tests
    FOR file IN upgrade.affected_files:
      test_suite.cases.append({name: f"No regression in {file}", type: "regression"})

    # Smoke test
    test_suite.cases.append({name: "App starts", type: "smoke"})
    YIELD test_suite

VALIDATION_CHECKLIST:
- [ ] Backup lock file
- [ ] Run baseline tests
- [ ] Apply upgrade: {package} {from} → {to}
- [ ] Run validation tests
- [ ] Rollback plan: restore lock + reinstall
```

## Integration

```text
Read `templates/shared/migration/upgrade-detection.md` and apply.

versions = detect_versions()
IF outdated := check_for_updates(versions):
  breaking = fetch_breaking_changes(outdated)
  impact = analyze_impact(breaking, codebase)
  path = generate_upgrade_path(impact)
  tests = generate_validation_tests(path)
  OUTPUT upgrade_report(path, tests)
```

## Output Format

```text
Upgrade Detection Report

Current Versions:
├── Node.js: 18.17.0 → 20.10.0 available
├── react: 17.0.2 → 18.2.0 (BREAKING)
└── postgres: 14.9 → 16.1 available

Upgrade Path:
├── UPG-001: typescript 4.9→5.3 [0 deps] ~2h
├── UPG-002: react 17.0→18.2 [UPG-001] ~8h
└── UPG-003: postgres 14→16 [0 deps] ~4h

Impact: 3 breaking | 24 files | ~15h effort | 12 tests
```

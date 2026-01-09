# Gate Check Implementations

## Purpose

Provide simplified check implementations for inline quality gates. Each pass (A-Z) has two variants:

1. **Simplified Check** (default for inline gates) - Fast (~1-5s), returns pass/fail with count
2. **Full Pass** (for `/speckit.analyze`) - Complete (~10-30s), returns detailed findings

## Check Function Interface

```text
CHECK_RESULT = {
  status: PASS | FAIL | WARN,
  count: number,           # Issues found
  threshold: number,       # Acceptable threshold
  details: string,         # Human-readable summary
  locations: [{            # Specific issue locations (optional)
    file: string,
    line: number,
    text: string
  }]
}
```

---

## Pass B: Ambiguity Detection

Detects vague terms and placeholders that need clarification.

### Simplified Check

```text
SIMPLIFIED_CHECK_B(artifact):

  # Vague terms without measurable criteria
  VAGUE_TERMS = [
    "fast", "quickly", "responsive",
    "secure", "robust", "reliable",
    "scalable", "performant", "efficient",
    "user-friendly", "intuitive", "easy",
    "appropriate", "suitable", "reasonable",
    "as needed", "if necessary", "when required",
    "etc", "and so on", "and more"
  ]

  # Placeholder markers
  PLACEHOLDERS = [
    "TODO", "TBD", "FIXME", "XXX", "???",
    "<placeholder>", "[TBD]", "[TODO]",
    "NEEDS CLARIFICATION", "to be determined"
  ]

  # Count matches (case-insensitive)
  vague_count = 0
  FOR term IN VAGUE_TERMS:
    vague_count += COUNT_MATCHES(artifact, term, case_insensitive=true)

  placeholder_count = 0
  FOR marker IN PLACEHOLDERS:
    placeholder_count += COUNT_MATCHES(artifact, marker, case_insensitive=true)

  total = vague_count + placeholder_count

  RETURN {
    status: IF total <= threshold THEN PASS ELSE FAIL,
    count: total,
    threshold: 5,  # Default threshold
    details: "{vague_count} vague terms, {placeholder_count} placeholders"
  }
```

### Full Pass

See `/speckit.analyze` Pass B for complete implementation with:
- Classification of ambiguity types
- Specific line locations
- Suggested rewrites
- Severity scoring per ambiguity

---

## Pass D: Constitution Alignment

Validates artifact against project constitution principles.

### Simplified Check

```text
SIMPLIFIED_CHECK_D(artifact, constitution):

  # Load constitution if not provided
  IF constitution IS NULL:
    constitution = READ("memory/constitution.md")
    IF constitution IS NULL:
      RETURN {status: PASS, count: 0, details: "No constitution found"}

  # Extract MUST principles (non-negotiable)
  MUST_PRINCIPLES = []
  FOR line IN constitution.lines:
    IF line MATCHES "MUST" OR line MATCHES "SHALL":
      principle = EXTRACT_PRINCIPLE(line)
      MUST_PRINCIPLES.push(principle)

  # Quick conflict detection
  violations = []
  FOR principle IN MUST_PRINCIPLES:
    # Check for direct contradictions
    IF CONFLICTS_WITH(artifact, principle):
      violations.push({
        principle_id: principle.id,
        principle_text: principle.text,
        conflict_location: FIND_CONFLICT(artifact, principle)
      })

  RETURN {
    status: IF violations.length == 0 THEN PASS ELSE FAIL,
    count: violations.length,
    threshold: 0,  # Zero tolerance for constitution violations
    details: IF violations.length > 0
      THEN "Conflicts: " + violations.map(v => v.principle_id).join(", ")
      ELSE "No constitution violations"
  }

CONFLICTS_WITH(artifact, principle):
  # Pattern-based conflict detection
  IF principle.type == "SECURITY":
    # Check for security anti-patterns
    RETURN CONTAINS_SECURITY_ANTIPATTERN(artifact, principle.pattern)
  ELIF principle.type == "TESTING":
    # Check for testing coverage conflicts
    RETURN MISSING_TEST_REQUIREMENT(artifact, principle.threshold)
  ELIF principle.type == "ARCHITECTURE":
    # Check for architectural conflicts
    RETURN VIOLATES_PATTERN(artifact, principle.pattern)
  ELSE:
    # Generic keyword conflict detection
    RETURN KEYWORD_CONFLICT(artifact, principle.keywords)
```

---

## Pass F: Inconsistency Detection

Detects terminology drift between spec and plan.

### Simplified Check

```text
SIMPLIFIED_CHECK_F(spec, plan):

  # Extract key technical terms from spec
  spec_terms = EXTRACT_KEY_TERMS(spec)
  # Terms: component names, API endpoints, data models, etc.

  # Extract key technical terms from plan
  plan_terms = EXTRACT_KEY_TERMS(plan)

  # Find drift: terms that appear different
  inconsistencies = []

  FOR spec_term IN spec_terms:
    # Check for similar but not identical terms in plan
    similar = FIND_SIMILAR(spec_term, plan_terms, threshold=0.8)
    IF similar AND similar != spec_term:
      inconsistencies.push({
        spec_term: spec_term,
        plan_term: similar,
        similarity: CALCULATE_SIMILARITY(spec_term, similar)
      })

  # Check for terms in plan not in spec
  FOR plan_term IN plan_terms:
    IF plan_term NOT IN spec_terms:
      # Check if it's a derived term
      IF NOT IS_DERIVED_TERM(plan_term, spec_terms):
        inconsistencies.push({
          type: "undefined_in_spec",
          plan_term: plan_term
        })

  RETURN {
    status: IF inconsistencies.length == 0 THEN PASS ELSE WARN,
    count: inconsistencies.length,
    threshold: 0,
    details: IF inconsistencies.length > 0
      THEN "{inconsistencies.length} terminology inconsistencies"
      ELSE "Terminology consistent"
  }

EXTRACT_KEY_TERMS(artifact):
  terms = []
  # Extract from headers
  terms += EXTRACT_HEADERS(artifact)
  # Extract code identifiers (PascalCase, camelCase, snake_case)
  terms += EXTRACT_IDENTIFIERS(artifact)
  # Extract API endpoints
  terms += EXTRACT_ENDPOINTS(artifact)
  # Extract data model names
  terms += EXTRACT_MODELS(artifact)
  RETURN UNIQUE(terms)
```

---

## Pass G: Dependency Graph Validation

Detects circular dependencies in task graph.

### Simplified Check

```text
SIMPLIFIED_CHECK_G(tasks):

  # Build dependency graph from tasks.md
  graph = {}
  FOR task IN tasks:
    task_id = EXTRACT_ID(task)  # e.g., T001
    deps = EXTRACT_DEPS(task)   # e.g., [DEP:T000]
    graph[task_id] = deps

  # Topological sort to detect cycles
  visited = {}
  rec_stack = {}
  cycle_found = false
  cycle_path = []

  FUNCTION detect_cycle(node):
    visited[node] = true
    rec_stack[node] = true

    FOR dep IN graph[node]:
      IF NOT visited[dep]:
        IF detect_cycle(dep):
          cycle_path.unshift(dep)
          RETURN true
      ELIF rec_stack[dep]:
        cycle_path = [dep, node]
        RETURN true

    rec_stack[node] = false
    RETURN false

  FOR node IN graph.keys:
    IF NOT visited[node]:
      IF detect_cycle(node):
        cycle_found = true
        BREAK

  RETURN {
    status: IF NOT cycle_found THEN PASS ELSE FAIL,
    count: IF cycle_found THEN 1 ELSE 0,
    threshold: 0,
    details: IF cycle_found
      THEN "Circular dependency: " + cycle_path.join(" → ")
      ELSE "No circular dependencies"
  }
```

---

## Pass H: Traceability Validation

Validates FR coverage by implementation tasks.

### Simplified Check

```text
SIMPLIFIED_CHECK_H(spec, tasks):

  # Extract FR IDs from spec.md
  fr_ids = []
  FOR line IN spec.lines:
    IF line MATCHES /FR-\d{3}/:
      fr_ids.push(EXTRACT_MATCH(line, /FR-\d{3}/))
  fr_ids = UNIQUE(fr_ids)

  # Extract FR markers from tasks.md
  covered_frs = []
  FOR task IN tasks:
    markers = EXTRACT_FR_MARKERS(task)  # [FR:FR-001,FR-002]
    covered_frs += markers
  covered_frs = UNIQUE(covered_frs)

  # Find uncovered FRs
  uncovered = []
  FOR fr IN fr_ids:
    IF fr NOT IN covered_frs:
      uncovered.push(fr)

  RETURN {
    status: IF uncovered.length == 0 THEN PASS ELSE FAIL,
    count: uncovered.length,
    threshold: 0,
    details: IF uncovered.length > 0
      THEN "Uncovered FRs: " + uncovered.join(", ")
      ELSE "All FRs covered ({fr_ids.length} total)"
  }
```

---

## Pass J: RTM (Requirements Traceability Matrix) Validation

Validates completeness of traceability matrix.

### Simplified Check

```text
SIMPLIFIED_CHECK_J(spec, plan, tasks):

  # Build expected traceability chains
  # FR → Plan Section → Task
  issues = []

  # Extract all requirement IDs
  fr_ids = EXTRACT_IDS(spec, /FR-\d{3}/)
  as_ids = EXTRACT_IDS(spec, /AS-\d+[A-Z]?/)

  # Check FR → Task coverage
  FOR fr IN fr_ids:
    task_refs = FIND_REFS(tasks, fr)
    IF task_refs.length == 0:
      issues.push({type: "fr_no_task", id: fr})

  # Check AS → Test task coverage
  FOR as IN as_ids:
    test_refs = FIND_TEST_REFS(tasks, as)
    IF test_refs.length == 0:
      issues.push({type: "as_no_test", id: as})

  RETURN {
    status: IF issues.length == 0 THEN PASS ELSE WARN,
    count: issues.length,
    threshold: 0,
    details: IF issues.length > 0
      THEN "{issues.length} traceability gaps"
      ELSE "RTM complete"
  }
```

---

## Pass R: Build Verification

Verifies build succeeds.

### Simplified Check

```text
SIMPLIFIED_CHECK_R(project):

  # Detect project type and build command
  build_cmd = DETECT_BUILD_COMMAND(project)

  IF build_cmd IS NULL:
    RETURN {status: WARN, count: 0, details: "No build command detected"}

  # Run build
  result = EXECUTE(build_cmd, timeout=120000)

  IF result.exit_code == 0:
    RETURN {
      status: PASS,
      count: 0,
      threshold: 0,
      details: "Build succeeded"
    }
  ELSE:
    # Extract error count
    error_count = COUNT_MATCHES(result.stderr, /error/i)
    RETURN {
      status: FAIL,
      count: error_count,
      threshold: 0,
      details: "Build failed ({error_count} errors)"
    }

DETECT_BUILD_COMMAND(project):
  IF EXISTS("package.json"):
    pkg = READ_JSON("package.json")
    IF pkg.scripts.build:
      RETURN "npm run build"
    ELIF pkg.scripts.compile:
      RETURN "npm run compile"
  ELIF EXISTS("Cargo.toml"):
    RETURN "cargo build"
  ELIF EXISTS("go.mod"):
    RETURN "go build ./..."
  ELIF EXISTS("pyproject.toml"):
    RETURN "python -m build"
  ELIF EXISTS("pom.xml"):
    RETURN "mvn compile"
  ELIF EXISTS("build.gradle") OR EXISTS("build.gradle.kts"):
    RETURN "./gradlew build"
  RETURN NULL
```

---

## Pass S: Test Verification

Verifies tests pass.

### Simplified Check

```text
SIMPLIFIED_CHECK_S(project):

  # Detect project type and test command
  test_cmd = DETECT_TEST_COMMAND(project)

  IF test_cmd IS NULL:
    RETURN {status: WARN, count: 0, details: "No test command detected"}

  # Run tests
  result = EXECUTE(test_cmd, timeout=300000)

  # Parse test results
  passed = EXTRACT_PASSED_COUNT(result.stdout)
  failed = EXTRACT_FAILED_COUNT(result.stdout)
  total = passed + failed

  IF result.exit_code == 0:
    RETURN {
      status: PASS,
      count: 0,
      threshold: 0,
      details: "{passed}/{total} tests passed"
    }
  ELSE:
    RETURN {
      status: FAIL,
      count: failed,
      threshold: 0,
      details: "{failed}/{total} tests failed"
    }

DETECT_TEST_COMMAND(project):
  IF EXISTS("package.json"):
    pkg = READ_JSON("package.json")
    IF pkg.scripts.test:
      RETURN "npm test"
  ELIF EXISTS("Cargo.toml"):
    RETURN "cargo test"
  ELIF EXISTS("go.mod"):
    RETURN "go test ./..."
  ELIF EXISTS("pyproject.toml") OR EXISTS("pytest.ini"):
    RETURN "pytest"
  ELIF EXISTS("pom.xml"):
    RETURN "mvn test"
  ELIF EXISTS("build.gradle") OR EXISTS("build.gradle.kts"):
    RETURN "./gradlew test"
  RETURN NULL
```

---

## Pass T: Coverage Verification

Verifies test coverage meets threshold.

### Simplified Check

```text
SIMPLIFIED_CHECK_T(project, threshold=80):

  # Detect coverage command
  coverage_cmd = DETECT_COVERAGE_COMMAND(project)

  IF coverage_cmd IS NULL:
    RETURN {status: WARN, count: 0, details: "No coverage tool detected"}

  # Run coverage
  result = EXECUTE(coverage_cmd, timeout=300000)

  # Parse coverage percentage
  coverage = EXTRACT_COVERAGE_PERCENT(result.stdout)

  IF coverage IS NULL:
    RETURN {status: WARN, count: 0, details: "Could not parse coverage"}

  IF coverage >= threshold:
    RETURN {
      status: PASS,
      count: coverage,
      threshold: threshold,
      details: "{coverage}% coverage (threshold: {threshold}%)"
    }
  ELSE:
    RETURN {
      status: FAIL,
      count: coverage,
      threshold: threshold,
      details: "{coverage}% coverage (below {threshold}% threshold)"
    }

DETECT_COVERAGE_COMMAND(project):
  IF EXISTS("package.json"):
    pkg = READ_JSON("package.json")
    IF pkg.scripts["test:coverage"]:
      RETURN "npm run test:coverage"
    ELIF pkg.scripts.coverage:
      RETURN "npm run coverage"
    ELIF EXISTS("jest.config.js") OR EXISTS("jest.config.ts"):
      RETURN "npx jest --coverage"
    ELIF EXISTS("vitest.config.js") OR EXISTS("vitest.config.ts"):
      RETURN "npx vitest run --coverage"
  ELIF EXISTS("Cargo.toml"):
    RETURN "cargo tarpaulin --out Json"
  ELIF EXISTS("go.mod"):
    RETURN "go test -cover ./..."
  ELIF EXISTS("pyproject.toml") OR EXISTS("pytest.ini"):
    RETURN "pytest --cov"
  RETURN NULL
```

---

## Pass U: Lint Verification

Verifies lint passes with zero errors.

### Simplified Check

```text
SIMPLIFIED_CHECK_U(project):

  # Detect lint command
  lint_cmd = DETECT_LINT_COMMAND(project)

  IF lint_cmd IS NULL:
    RETURN {status: WARN, count: 0, details: "No linter detected"}

  # Run linter
  result = EXECUTE(lint_cmd, timeout=60000)

  # Parse lint results
  error_count = COUNT_MATCHES(result.stdout + result.stderr, /error/i)
  warning_count = COUNT_MATCHES(result.stdout + result.stderr, /warning/i)

  IF result.exit_code == 0 AND error_count == 0:
    RETURN {
      status: PASS,
      count: 0,
      threshold: 0,
      details: "Lint clean ({warning_count} warnings)"
    }
  ELSE:
    RETURN {
      status: FAIL,
      count: error_count,
      threshold: 0,
      details: "{error_count} errors, {warning_count} warnings"
    }

DETECT_LINT_COMMAND(project):
  IF EXISTS("package.json"):
    pkg = READ_JSON("package.json")
    IF pkg.scripts.lint:
      RETURN "npm run lint"
    ELIF EXISTS(".eslintrc") OR EXISTS(".eslintrc.js") OR EXISTS("eslint.config.js"):
      RETURN "npx eslint ."
  ELIF EXISTS("Cargo.toml"):
    RETURN "cargo clippy"
  ELIF EXISTS("go.mod"):
    RETURN "golangci-lint run"
  ELIF EXISTS("pyproject.toml"):
    RETURN "ruff check ."
  RETURN NULL
```

---

## Quality Gate References

For gates that reference QG-xxx IDs, delegate to quality gate definitions.

### QG-001: SQS Threshold

```text
CHECK_QG_001(feature_dir):
  # Calculate SQS from spec artifacts
  spec = READ(feature_dir + "/spec.md")
  plan = READ(feature_dir + "/plan.md")
  tasks = READ(feature_dir + "/tasks.md")

  # SQS = (FR_Coverage×0.3 + AS_Coverage×0.3 + Traceability×0.2 + Constitution×0.2) × 100
  fr_coverage = CALCULATE_FR_COVERAGE(spec, tasks)
  as_coverage = CALCULATE_AS_COVERAGE(spec, tasks)
  traceability = CALCULATE_TRACEABILITY_SCORE(spec, plan, tasks)
  constitution = CALCULATE_CONSTITUTION_SCORE(spec, plan)

  sqs = (fr_coverage * 0.3 + as_coverage * 0.3 + traceability * 0.2 + constitution * 0.2) * 100

  RETURN {
    status: IF sqs >= 80 THEN PASS ELSE FAIL,
    count: ROUND(sqs),
    threshold: 80,
    details: "SQS: {sqs}/100 (FR:{fr_coverage*100}%, AS:{as_coverage*100}%)"
  }
```

### QG-STAGING-001: Staging Ready

```text
CHECK_QG_STAGING_001():
  # Check Docker services health
  compose_file = FIND_COMPOSE_FILE()

  IF compose_file IS NULL:
    RETURN {status: WARN, count: 0, details: "No docker-compose found"}

  # Check if services are running
  result = EXECUTE("docker compose ps --format json", timeout=10000)

  IF result.exit_code != 0:
    RETURN {status: FAIL, count: 1, details: "Docker Compose not running"}

  services = PARSE_JSON(result.stdout)
  unhealthy = []

  FOR service IN services:
    IF service.Health != "healthy" AND service.State != "running":
      unhealthy.push(service.Name)

  IF unhealthy.length > 0:
    RETURN {
      status: FAIL,
      count: unhealthy.length,
      threshold: 0,
      details: "Unhealthy: " + unhealthy.join(", ")
    }

  RETURN {status: PASS, count: 0, details: "All staging services healthy"}
```

### QG-TEST-001: AS Test Coverage

```text
CHECK_QG_TEST_001(spec, tasks):
  # Extract AS IDs from spec
  as_ids = EXTRACT_IDS(spec, /AS-\d+[A-Z]?/)

  # Extract TEST markers from tasks
  test_markers = []
  FOR task IN tasks:
    IF task CONTAINS "[TEST:":
      markers = EXTRACT_TEST_MARKERS(task)
      test_markers += markers

  # Check coverage
  uncovered = []
  FOR as IN as_ids:
    IF as NOT IN test_markers:
      uncovered.push(as)

  coverage_pct = (as_ids.length - uncovered.length) / as_ids.length * 100

  RETURN {
    status: IF uncovered.length == 0 THEN PASS ELSE FAIL,
    count: uncovered.length,
    threshold: 0,
    details: "{coverage_pct}% AS test coverage ({uncovered.length} uncovered)"
  }
```

---

## Usage in Commands

Commands execute checks via the inline gates framework:

```text
# In specify.md, before handoff to plan.md:

### Inline Quality Gates

Read `templates/shared/validation/inline-gates.md` and execute:

```text
gates_config = this.inline_gates
artifact = generated spec.md
cli_flags = parse_arguments($ARGUMENTS)

result = EXECUTE_INLINE_GATES(artifact, gates_config, cli_flags)

IF result.status == "BLOCKED":
  STOP  # Do not proceed to handoff
```
```

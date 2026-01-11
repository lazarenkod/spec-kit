# Drift Detection Framework

## Purpose

Detect when code implementation diverges from specification (spec-code drift) through bidirectional analysis.

## Why This Matters

| Without Drift Detection | With Drift Detection |
|------------------------|---------------------|
| Manual fixes go undocumented | Automatic tracking of spec-code mismatches |
| Specifications become stale | Proactive staleness alerts |
| Undocumented APIs proliferate | Reverse drift detection (code → spec) |
| Missing implementations go unnoticed | Forward drift detection (spec → code) |

## Drift Types

### Forward Drift (Spec → Code)

**Definition**: Requirements in spec.md that are NOT implemented in code

**Detection Algorithm**:
```text
DETECT_FORWARD_DRIFT(spec, codebase):
  # Extract all requirement IDs from spec.md
  spec_frs = EXTRACT_FRS(spec)
  spec_ass = EXTRACT_ASS(spec)
  spec_nfrs = EXTRACT_NFRS(spec)

  # Scan codebase for @speckit annotations
  code_annotations = PARSE_ANNOTATIONS(codebase)

  drift_items = []

  FOR fr IN spec_frs:
    IF fr.id NOT IN code_annotations.FR:
      drift = {
        id: "DRIFT-{N}",
        type: "forward_drift",
        subtype: "unimplemented_requirement",
        severity: "HIGH",
        requirement: fr.id,
        description: fr.description,
        expected_location: INFER_LOCATION(fr),
        recommendation: "Implement {fr.id} or move to Out of Scope"
      }
      drift_items.append(drift)

  FOR as IN spec_ass:
    IF as.id NOT IN code_annotations.AS AND as.id NOT IN test_files:
      drift = {
        id: "DRIFT-{N}",
        type: "forward_drift",
        subtype: "missing_test",
        severity: "MEDIUM",
        scenario: as.id,
        description: as.description,
        recommendation: "Add test file with [TEST:{as.id}] marker"
      }
      drift_items.append(drift)

  RETURN drift_items
```

**Examples**:
- FR-007 defined in spec but no implementation found
- AS-3B has no corresponding test file
- NFR-PERF-001 performance target not validated

---

### Reverse Drift (Code → Spec)

**Definition**: Code implementations that are NOT documented in spec.md

**Detection Algorithm**:
```text
DETECT_REVERSE_DRIFT(spec, codebase):
  # Extract spec requirements
  spec_frs = EXTRACT_FRS(spec)

  # Analyze codebase for public APIs
  code_apis = EXTRACT_PUBLIC_APIS(codebase)

  drift_items = []

  FOR api IN code_apis:
    # Check if API has @speckit:FR: annotation
    IF api.annotations.FR:
      # Check if annotated FR exists in spec
      IF api.annotations.FR NOT IN spec_frs:
        drift = {
          id: "DRIFT-{N}",
          type: "reverse_drift",
          subtype: "orphan_annotation",
          severity: "HIGH",
          location: "{api.file}:{api.line}",
          signature: api.signature,
          annotation: api.annotations.FR,
          recommendation: "Add {api.annotations.FR} to spec.md or remove annotation"
        }
        drift_items.append(drift)
    ELSE:
      # Public API without annotation
      IF NOT api.marked_internal:
        drift = {
          id: "DRIFT-{N}",
          type: "reverse_drift",
          subtype: "undocumented_api",
          severity: "HIGH" IF api.is_public_route ELSE "MEDIUM",
          location: "{api.file}:{api.line}",
          signature: api.signature,
          recommendation: "Add @speckit:FR:FR-xxx or mark @internal"
        }
        drift_items.append(drift)

  RETURN drift_items
```

**Examples**:
- POST /api/v1/users/:id/archive exists but not in spec
- Public function exportToCSV() without @speckit annotation
- Test file tests/integration/sms.test.ts but no AS-xxx in spec

---

### Behavioral Drift

**Definition**: Implementation behavior differs from spec expectations

**Detection Patterns**:
```text
DETECT_BEHAVIORAL_DRIFT(spec, tests, impl):
  drift_items = []

  # Example: Expected vs actual HTTP status codes
  spec_status = EXTRACT_EXPECTED_STATUS(spec, endpoint)
  impl_status = EXTRACT_ACTUAL_STATUS(impl, endpoint)

  IF spec_status != impl_status:
    drift = {
      id: "DRIFT-{N}",
      type: "behavioral_drift",
      subtype: "status_mismatch",
      severity: "HIGH",
      endpoint: endpoint,
      expected: spec_status,
      actual: impl_status,
      recommendation: "Update impl to return {spec_status} or revise spec"
    }
    drift_items.append(drift)

  # Example: Expected vs actual validation rules
  spec_rules = EXTRACT_VALIDATION_RULES(spec, field)
  impl_rules = EXTRACT_ACTUAL_VALIDATION(impl, field)

  IF spec_rules != impl_rules:
    drift = {
      id: "DRIFT-{N}",
      type: "behavioral_drift",
      subtype: "validation_mismatch",
      severity: "MEDIUM",
      field: field,
      expected: spec_rules,
      actual: impl_rules
    }
    drift_items.append(drift)

  RETURN drift_items
```

**Examples**:
- Spec says "return 401 on invalid token", impl returns 403
- Spec requires email validation, impl allows any string
- Spec limits max length to 100, impl enforces 50

---

## Severity Levels

```text
SEVERITY_CLASSIFICATION:

  CRITICAL:
    description: "Breaking changes risk - immediate action required"
    examples:
      - Public API removed from spec but exists in code
      - Security requirement (NFR-SEC-xxx) not implemented
      - Data loss risk (no validation where spec requires it)
    action: "Block deployment, fix immediately"

  HIGH:
    description: "Missing functionality or undocumented changes"
    examples:
      - FR-xxx in spec but no implementation
      - Public API without @speckit annotation
      - Test missing for AS-xxx
    action: "Fix before merge"

  MEDIUM:
    description: "Behavioral drift or inconsistencies"
    examples:
      - HTTP status code differs from spec
      - Validation rules mismatch
      - Partial implementation (some fields missing)
    action: "Review and address"

  LOW:
    description: "Documentation drift - informational"
    examples:
      - Outdated code comments
      - Deprecated @internal function still in code
      - Test coverage below target but passing
    action: "Informational - address when convenient"
```

---

## Detection Patterns by Language

### TypeScript

```text
UNDOCUMENTED_API_PATTERNS = [
  # Express routes
  r"router\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]",

  # NestJS decorators
  r"@(Get|Post|Put|Delete|Patch)\(['\"]([^'\"]*)['\"]?\)",

  # Exported functions (public API)
  r"export\s+(async\s+)?function\s+([A-Z]\w+)",

  # Exported classes (public API)
  r"export\s+class\s+([A-Z]\w+)"
]

VALIDATION_PATTERNS = [
  # Zod schemas
  r"z\.(string|number|boolean|array|object)\(\)",
  r"\.(email|url|uuid|min|max)\(\d*\)",

  # Joi schemas
  r"Joi\.(string|number|boolean)\(\)",

  # Class-validator decorators
  r"@(IsEmail|IsString|IsNumber|Min|Max|Length)"
]

INTERNAL_MARKERS = [
  r"@internal",
  r"\/\*\*.*@internal.*\*\/",
  r"\/\/ @internal"
]
```

### Python

```text
UNDOCUMENTED_API_PATTERNS = [
  # FastAPI routes
  r"@app\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]",

  # Flask routes
  r"@app\.route\(['\"]([^'\"]+)['\"].*methods=\[['\"]([A-Z]+)['\"]",

  # Django views
  r"def\s+(\w+)\(request[,\)].*\):",

  # Public functions (not starting with _)
  r"def\s+([a-z][a-z0-9_]*)\([^)]*\)(?!.*:$)"  # Not _ prefix
]

VALIDATION_PATTERNS = [
  # Pydantic models
  r"(\w+):\s*(str|int|bool|float|EmailStr|UUID)",
  r"Field\(.*min_length=(\d+)",
  r"Field\(.*max_length=(\d+)",

  # Django validators
  r"validators=\[(MinLength|MaxLength|EmailValidator)"
]
```

### Go

```text
UNDOCUMENTED_API_PATTERNS = [
  # Gin routes
  r"router\.(GET|POST|PUT|DELETE|PATCH)\(['\"]([^'\"]+)['\"]",

  # Chi routes
  r"r\.(Get|Post|Put|Delete|Patch)\(['\"]([^'\"]+)['\"]",

  # Exported functions (capitalized)
  r"func\s+([A-Z]\w+)\("
]

VALIDATION_PATTERNS = [
  # Validator package
  r"validate:\"(required|email|min=\d+|max=\d+)\"",

  # Custom validation
  r"if\s+.*==\s*\"\"\s*\{.*return\s+.*error"
]
```

### Java/Kotlin

```text
UNDOCUMENTED_API_PATTERNS = [
  # Spring annotations
  r"@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)\(['\"]([^'\"]*)['\"]?\)",

  # JAX-RS annotations
  r"@(GET|POST|PUT|DELETE)\s+@Path\(['\"]([^'\"]+)['\"]",

  # Public methods
  r"public\s+\w+\s+([a-z]\w+)\("
]

VALIDATION_PATTERNS = [
  # JSR-303/Bean Validation
  r"@(NotNull|NotEmpty|Email|Size|Min|Max|Pattern)",

  # Hibernate Validator
  r"@(Length|Range|CreditCardNumber)"
]
```

---

## Drift Metrics

```yaml
# Extension to .artifact-registry.yaml
drift_metrics:
  last_checked: "{ISO_DATE}"
  forward_drift:
    unimplemented_frs: 3
    missing_tests: 5
    total: 8
  reverse_drift:
    undocumented_apis: 7
    orphan_annotations: 2
    total: 9
  behavioral_drift:
    status_mismatches: 2
    validation_mismatches: 3
    total: 5
  by_severity:
    critical: 0
    high: 10
    medium: 8
    low: 4
  coverage_stats:
    fr_to_code: 85%  # FRs with @speckit:FR: in code
    code_to_spec: 72%  # Public APIs with FR in spec
```

---

## Drift Report Template

```markdown
# Drift Detection Report

**Feature**: {FEATURE_ID}-{feature_name}
**Generated**: {ISO_DATE}
**Analysis Scope**:
- **Languages**: {languages}
- **Files Analyzed**: {file_count}
- **Public APIs Found**: {api_count}

## Summary

| Category | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| Forward Drift | {N} | {N} | {N} | {N} | {N} |
| Reverse Drift | {N} | {N} | {N} | {N} | {N} |
| Behavioral Drift | {N} | {N} | {N} | {N} | {N} |
| **Total** | **{N}** | **{N}** | **{N}** | **{N}** | **{N}** |

**Overall Status**: {✅ PASS | ⚠️ REVIEW | 🔴 FAIL}

**Quality Gate**: {QG-DRIFT-001}
- FR → Code coverage: {X}% (threshold: >= 80%)
- Critical issues: {N} (threshold: == 0)
- High issues: {N} (threshold: < 5)

---

## Drift Items

### DRIFT-001: Undocumented API Endpoint (HIGH)

**Type**: reverse_drift → undocumented_api
**Severity**: HIGH
**Location**: `src/api/users.ts:42-58`

**API Signature**:
```typescript
POST /api/v1/users/:id/archive
```

**Current State**:
- ✅ Implementation exists
- ❌ Not in spec.md FR list
- ❌ No @speckit:FR: annotation
- ❌ No @internal marker

**Recommendation**: Add AS-xxx scenario to spec.md or mark as @internal

**Auto-fix Available**: ✅ Yes
```typescript
// Suggested annotation:
// @speckit:FR:FR-009 User archival endpoint
```

**Auto-fix Command**:
```bash
# Preview changes
/speckit.drift-detect --fix DRIFT-001 --preview

# Apply fix
/speckit.drift-detect --fix DRIFT-001 --apply
```

---

### DRIFT-002: Unimplemented Requirement (HIGH)

**Type**: forward_drift → unimplemented_requirement
**Severity**: HIGH
**Requirement**: FR-007
**Description**: "User password reset via email link"

**Current State**:
- ✅ Defined in spec.md §3.2
- ❌ No implementation found in codebase
- ❌ No @speckit:FR:FR-007 annotation
- ❌ Expected location: `src/auth/` (inferred)

**Recommendation**: Implement FR-007 or move to "Out of Scope" section

**Auto-fix Available**: ❌ No (requires implementation)

---

### DRIFT-003: Missing Test Coverage (MEDIUM)

**Type**: forward_drift → missing_test
**Severity**: MEDIUM
**Scenario**: AS-5C
**Description**: "Given user navigates to dashboard, When authenticated, Then shows welcome message"

**Current State**:
- ✅ Defined in spec.md
- ❌ No test file found
- ❌ No [TEST:AS-5C] marker in test files

**Recommendation**: Create test file tests/e2e/dashboard.test.ts with [TEST:AS-5C]

**Auto-fix Available**: ✅ Yes (scaffold test)
```typescript
// tests/e2e/dashboard.test.ts
// [TEST:AS-5C]
describe('Dashboard welcome message', () => {
  it('shows welcome when authenticated', () => {
    // TODO: Implement test
  });
});
```

---

## Next Actions

**Immediate** (Critical):
- None ✅

**High Priority** (before merge):
1. Fix DRIFT-001: Add @speckit:FR:FR-009 to archiveUser endpoint
2. Fix DRIFT-002: Implement FR-007 or update spec scope
3. Fix DRIFT-004 to DRIFT-007: (similar items)

**Medium Priority** (review):
1. DRIFT-003: Add test for AS-5C
2. DRIFT-008 to DRIFT-012: (similar items)

**Low Priority** (informational):
- DRIFT-013 to DRIFT-016: Update code comments

---

## Drift Trends

| Metric | Current | Previous | Trend |
|--------|---------|----------|-------|
| Total Drift | 16 | 22 | ⬇️ -6 (good) |
| Critical | 0 | 1 | ⬇️ -1 (fixed) |
| High | 10 | 15 | ⬇️ -5 (improving) |
| FR → Code Coverage | 85% | 78% | ⬆️ +7% (improving) |

**Insight**: Drift reduced by 27% since last check (2026-01-08)

---

## Recommendations

1. **Auto-fix Safe Items**: Run `/speckit.drift-detect --auto-fix --severity=LOW,MEDIUM` to automatically add annotations and scaffold tests

2. **Review Workflow**: Address HIGH items before next `/speckit.implement` run

3. **Prevention**: Add pre-commit hook to run drift detection:
   ```bash
   # .git/hooks/pre-commit
   /speckit.analyze --profile drift --severity HIGH,CRITICAL
   ```

4. **Continuous Monitoring**: Schedule weekly drift checks:
   ```bash
   # .github/workflows/drift-check.yml
   - name: Drift Check
     run: /speckit.analyze --profile drift
   ```
```

---

## Integration Points

### In /speckit.analyze (Pass AA)

```text
Read `templates/shared/drift/drift-detection.md`

drift_items = []

# Forward drift
forward = DETECT_FORWARD_DRIFT(spec, codebase)
drift_items.extend(forward)

# Reverse drift
reverse = DETECT_REVERSE_DRIFT(spec, codebase)
drift_items.extend(reverse)

# Generate report
WRITE(drift-report.md, drift_items)

# Update registry
UPDATE_DRIFT_METRICS(registry, drift_items)
```

### In /speckit.reverse-engineer

```text
Read `templates/shared/drift/drift-detection.md`

# After extraction
extracted_frs = EXTRACT_FROM_CODE(codebase)
canonical_frs = EXTRACT_FRS(spec.md)

# Detect drift
drift = DIFF(extracted_frs, canonical_frs)

# Report as part of extraction results
WRITE(reverse-engineered/drift-report.md, drift)
```

---

## Auto-fix Strategy

**Safe Auto-fixes** (no user confirmation):
- Add @speckit:FR: annotation to functions with clear FR mapping
- Add [TEST:AS-xxx] markers to test files with AS in name
- Add @internal marker to private utility functions

**Preview-required Auto-fixes** (user confirmation):
- Scaffold test files for missing AS coverage
- Add new FR-xxx to spec.md for undocumented APIs
- Update spec.md to mark FRs as "Out of Scope"

**Manual-only Fixes** (no automation):
- Implement missing FR-xxx functionality
- Fix behavioral drift (status codes, validation)
- Refactor code to match spec architecture

```text
AUTO_FIX_WORKFLOW:

  IF drift.type == "undocumented_api" AND has_clear_intent(api):
    # Safe: Add annotation
    suggestion = GENERATE_ANNOTATION(api)
    APPLY_FIX(api.file, api.line, suggestion)

  ELIF drift.type == "missing_test" AND has_test_template(as):
    # Preview: Scaffold test
    test_scaffold = GENERATE_TEST_SCAFFOLD(as)
    SHOW_PREVIEW(test_scaffold)
    IF user_confirms:
      WRITE(test_file, test_scaffold)

  ELIF drift.type == "unimplemented_requirement":
    # Manual: Cannot auto-implement
    OUTPUT: "Manual implementation required for {fr.id}"
```

---

## Performance Considerations

**Optimization Strategies**:

1. **Incremental Analysis**: Only analyze changed files
   ```text
   git diff --name-only HEAD~1 | grep "\.(ts|py|go|java|kt)$"
   ```

2. **Parallel Processing**: Analyze each language in parallel
   ```text
   LAUNCH 4 Task agents:
     - typescript-analyzer
     - python-analyzer
     - go-analyzer
     - java-analyzer
   ```

3. **Caching**: Cache parsed symbols per file
   ```text
   IF file_checksum == cached_checksum:
     symbols = LOAD_FROM_CACHE(file)
   ELSE:
     symbols = PARSE_FILE(file)
     CACHE(file, symbols, checksum)
   ```

4. **Scope Limiting**: Respect user-provided scope
   ```bash
   /speckit.analyze --profile drift --scope "src/api/**/*.ts"
   ```

**Performance Targets**:
- Small project (< 20 files): < 30 seconds
- Medium project (20-100 files): < 2 minutes
- Large project (100-500 files): < 5 minutes

---

## Backward Compatibility

**For projects without drift detection**:

```text
IF NOT exists(drift-report.md):
  # First run - baseline
  OUTPUT: "Establishing drift baseline..."
  OUTPUT: "Found {N} drift items (normal for first run)"
  OUTPUT: "Future runs will track trends"

IF NOT exists(.artifact-registry.yaml):
  # Registry not initialized
  OUTPUT: "Note: Artifact registry not initialized"
  OUTPUT: "Run any /speckit.* command to enable full drift tracking"
```

**Migration from manual fixes**:

```text
# Scan for existing manual annotations
existing = SEARCH_FOR_PATTERN("@speckit:FR:", codebase)

IF len(existing) == 0:
  OUTPUT: "No @speckit annotations found"
  OUTPUT: "Run /speckit.reverse-engineer to bootstrap annotations"
ELSE:
  OUTPUT: "Found {len(existing)} existing annotations"
  OUTPUT: "Validating against spec.md..."
```

# Drift Detection System Validation Checklist

**Version**: 0.4.0
**Date**: 2026-01-11
**Purpose**: Manual validation checklist for Pass AA (Drift Detection) and `/speckit.reverse-engineer` features

---

## Test Fixture Overview

### TypeScript Fixture
**Location**: `.test-fixtures/typescript-drift-test/`
**Language**: TypeScript (Node.js)
**Framework**: Jest (tests)

**Intentional Drift Scenarios**:
- ✅ Forward drift: FR-002 (password reset) in spec but not implemented
- ✅ Reverse drift: `deleteUser()` function implemented but not in spec
- ✅ Behavioral drift: `updateUser()` only updates name, not email (spec requires both)
- ✅ Correct alignment: `createUser()` properly aligned

### Python Fixture
**Location**: `.test-fixtures/python-drift-test/`
**Language**: Python (FastAPI)
**Framework**: pytest

**Intentional Drift Scenarios**:
- ✅ Forward drift: FR-002 (product search) in spec but not implemented
- ✅ Reverse drift: Two endpoints not in spec:
  - `GET /api/products/{id}/inventory`
  - `POST /api/products/bulk-import`
- ✅ Behavioral drift: `update_product()` only updates price, ignores stock
- ✅ Correct alignment: `create_product()` and `delete_product()` properly aligned

---

## Validation Phase 1: Drift Detection (Pass AA)

### Test 1: TypeScript Fixture - Forward Drift Detection

**Objective**: Verify that unimplemented requirements are detected

**Steps**:
1. Navigate to TypeScript fixture:
   ```bash
   cd /Users/dmitry.lazarenko/Documents/projects/spec-kit/.test-fixtures/typescript-drift-test
   ```

2. Run drift detection:
   ```bash
   /speckit.analyze --profile drift
   ```

3. Verify `drift-report.md` is generated

4. Check for expected drift items:

**Expected Results**:

```markdown
## Summary

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 0 | ✅ None |
| HIGH | 2 | ⚠️ Action Required |
| MEDIUM | 1 | 📋 Review |
| LOW | 0 | ℹ️ Informational |

## Drift Items

### DRIFT-001: Unimplemented Requirement (HIGH)

**Type**: forward_drift (Spec → Code)
**Requirement**: FR-002: "User Password Reset"
**Expected Location**: `src/auth/` (inferred) or `src/api.ts`

**Current State**:
- ✅ Defined in spec.md (lines 30-42)
- ❌ No implementation found
- ❌ No @speckit:FR:FR-002 annotation in codebase

### DRIFT-002: Undocumented API (HIGH)

**Type**: reverse_drift (Code → Spec)
**Location**: `src/api.ts:77-89`
**API Signature**: `deleteUser(userId: string): Promise<void>`

**Current State**:
- ✅ Implementation exists
- ❌ Not in spec.md FR list
- ❌ No @speckit:FR: annotation

### DRIFT-003: Behavioral Drift (MEDIUM)

**Type**: behavioral_drift
**Requirement**: FR-003: "User Update"
**Location**: `src/api.ts:55-69`

**Spec Says**: "Update user profile information (name and email)"
**Implementation Does**: Only updates name, ignores email updates

**Evidence**:
- Spec line 47: "Update user profile information (name and email)"
- Code line 62-64: Only `if (updates.name)` check, no email handling
```

**Coverage Metrics**:
- FR → Code: 66% (2/3 FRs implemented: FR-001 ✅, FR-002 ❌, FR-003 ⚠️)
- Code → Spec: 50% (2/4 public APIs documented: createUser ✅, updateUser ✅, deleteUser ❌, archiveInactiveUsers N/A)

**Validation Checklist**:
- [ ] drift-report.md exists
- [ ] Detected DRIFT-001 (FR-002 unimplemented) with HIGH severity
- [ ] Detected DRIFT-002 (deleteUser undocumented) with HIGH severity
- [ ] Detected DRIFT-003 (updateUser behavioral drift) with MEDIUM severity
- [ ] Did NOT flag createUser (correct alignment)
- [ ] Did NOT flag archiveInactiveUsers (marked @internal)
- [ ] Coverage metrics calculated correctly
- [ ] Traceability matrix included

---

### Test 2: Python Fixture - Forward Drift Detection

**Objective**: Verify drift detection on Python/FastAPI code

**Steps**:
1. Navigate to Python fixture:
   ```bash
   cd /Users/dmitry.lazarenko/Documents/projects/spec-kit/.test-fixtures/python-drift-test
   ```

2. Run drift detection:
   ```bash
   /speckit.analyze --profile drift --language python
   ```

3. Verify `drift-report.md` is generated

**Expected Results**:

```markdown
## Summary

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 0 | ✅ None |
| HIGH | 3 | ⚠️ Action Required |
| MEDIUM | 1 | 📋 Review |
| LOW | 0 | ℹ️ Informational |

## Drift Items

### DRIFT-001: Unimplemented Requirement (HIGH)

**Type**: forward_drift (Spec → Code)
**Requirement**: FR-002: "Product Search"
**Expected Location**: `src/api.py` (inferred)

**Current State**:
- ✅ Defined in spec.md (lines 30-44)
- ❌ No implementation found
- ❌ No @speckit:FR:FR-002 annotation

### DRIFT-002: Undocumented API (HIGH)

**Type**: reverse_drift (Code → Spec)
**Location**: `src/api.py:110-128`
**API Signature**: `GET /api/products/{product_id}/inventory`

**Current State**:
- ✅ Implementation exists
- ❌ Not in spec.md FR list
- ❌ No @speckit:FR: annotation
- ✅ Has test coverage

### DRIFT-003: Undocumented API (HIGH)

**Type**: reverse_drift (Code → Spec)
**Location**: `src/api.py:131-152`
**API Signature**: `POST /api/products/bulk-import`

**Current State**:
- ✅ Implementation exists
- ❌ Not in spec.md FR list
- ❌ No @speckit:FR: annotation
- ✅ Has test coverage

### DRIFT-004: Behavioral Drift (MEDIUM)

**Type**: behavioral_drift
**Requirement**: FR-003: "Product Update"
**Location**: `src/api.py:57-76`

**Spec Says**: "Update product information including price and stock levels"
**Implementation Does**: Only updates price, ignores stock/name/description

**Evidence**:
- Spec line 47: "Update product information including price and stock levels"
- Code line 62-70: Only `if updates.price:` check, no stock handling
```

**Coverage Metrics**:
- FR → Code: 75% (3/4 FRs implemented: FR-001 ✅, FR-002 ❌, FR-003 ⚠️, FR-004 ✅)
- Code → Spec: 60% (3/5 public APIs documented)

**Validation Checklist**:
- [ ] drift-report.md exists
- [ ] Detected DRIFT-001 (FR-002 unimplemented) with HIGH severity
- [ ] Detected DRIFT-002 (inventory endpoint undocumented) with HIGH severity
- [ ] Detected DRIFT-003 (bulk-import undocumented) with HIGH severity
- [ ] Detected DRIFT-004 (update_product behavioral drift) with MEDIUM severity
- [ ] Did NOT flag create_product (correct alignment)
- [ ] Did NOT flag delete_product (correct alignment)
- [ ] Did NOT flag archive_discontinued_products (marked @internal)
- [ ] Coverage metrics calculated correctly
- [ ] FastAPI decorators recognized (@app.post, @app.patch, etc.)

---

## Validation Phase 2: Reverse-Engineering

### Test 3: TypeScript Fixture - Requirement Extraction

**Objective**: Verify that requirements can be extracted from TypeScript code

**Steps**:
1. Navigate to TypeScript fixture:
   ```bash
   cd /Users/dmitry.lazarenko/Documents/projects/spec-kit/.test-fixtures/typescript-drift-test
   ```

2. Run reverse-engineering:
   ```bash
   /speckit.reverse-engineer --scope "src/**/*.ts" --exclude "*.test.ts" --language typescript
   ```

3. Verify `reverse-engineered/` directory is created

**Expected Output Structure**:
```
reverse-engineered/
├── .extraction-manifest.yaml
├── extracted-spec.md
├── drift-report.md
└── extraction-log.md
```

**Expected `.extraction-manifest.yaml`**:
```yaml
version: "1.0"
extracted_at: "2026-01-11T..."
extracted_by: "/speckit.reverse-engineer"
scan_scope:
  patterns: ["src/**/*.ts"]
  exclude: ["*.test.ts"]

baseline:
  spec_version: "1.0"
  spec_checksum: "sha256:..."

extraction_results:
  discovered_files: 1  # src/api.ts
  analyzed_symbols: 4  # createUser, updateUser, deleteUser, archiveInactiveUsers
  extracted_requirements:
    total: 3  # Excluding @internal function
    by_confidence:
      explicit: 2      # FR-001 (createUser), FR-003 (updateUser)
      high: 1          # deleteUser (inferred)
      medium: 0
      low: 0
  extracted_scenarios: 2  # From test file analysis

drift_summary:
  spec_to_code:
    missing_in_code: 1     # FR-002
  code_to_spec:
    missing_in_spec: 1     # deleteUser

confidence_stats:
  average: 0.85
  median: 0.90
  min: 0.70
  max: 0.95
```

**Expected `extracted-spec.md` Content**:

```markdown
### FR-001: User Creation

**Description**: Create a new user account with email and name
**Confidence**: 0.95 (EXPLICIT)

**Evidence**:
- Annotation: @speckit:FR:FR-001 (src/api.ts:20)
- Test coverage: AS-1A, AS-1B (src/api.test.ts:10-45)
- Implementation: src/api.ts:22-46

**Input**: UserData { email: string, name: string }
**Output**: User { id: string, email: string, name: string, createdAt: Date }

---

### FR-003: User Profile Update

**Description**: Update user profile information
**Confidence**: 0.80 (HIGH)

**Evidence**:
- Annotation: @speckit:FR:FR-003 (src/api.ts:48)
- Test coverage: AS-3A (src/api.test.ts:50-60)
- Implementation: src/api.ts:48-69
- ⚠️ Behavioral drift detected: Only updates name, not email

**Input**: userId: string, updates: Partial<UserData>
**Output**: Updated User object

---

### FR-NEW-1: User Account Deletion

**Description**: Permanently delete a user account
**Confidence**: 0.70 (HIGH - inferred from code)

**Evidence**:
- No annotation (inferred from implementation)
- Test coverage: Tests exist (src/api.test.ts:70-82)
- Implementation: src/api.ts:77-89
- Clear naming and documentation

**Input**: userId: string
**Output**: void

**Note**: This requirement was extracted from code but is not in canonical spec.md
```

**Validation Checklist**:
- [ ] reverse-engineered/ directory created
- [ ] .extraction-manifest.yaml exists with correct structure
- [ ] extracted-spec.md exists
- [ ] Extracted FR-001 with confidence 0.95 (EXPLICIT - has annotation)
- [ ] Extracted FR-003 with confidence 0.80 (HIGH - has annotation but drift)
- [ ] Extracted FR-NEW-1 (deleteUser) with confidence 0.70 (HIGH - inferred)
- [ ] Did NOT extract archiveInactiveUsers (marked @internal)
- [ ] Average confidence >= 0.70
- [ ] drift-report.md shows comparison with canonical spec
- [ ] extraction-log.md contains agent reasoning trace

---

### Test 4: Python Fixture - Requirement Extraction

**Objective**: Verify extraction from Python/FastAPI code

**Steps**:
1. Navigate to Python fixture:
   ```bash
   cd /Users/dmitry.lazarenko/Documents/projects/spec-kit/.test-fixtures/python-drift-test
   ```

2. Run reverse-engineering:
   ```bash
   /speckit.reverse-engineer --scope "src/**/*.py" --exclude "tests/*" --language python
   ```

**Expected `.extraction-manifest.yaml`**:
```yaml
extraction_results:
  discovered_files: 1  # src/api.py
  analyzed_symbols: 5  # create, update, delete, inventory, bulk-import
  extracted_requirements:
    total: 5
    by_confidence:
      explicit: 3      # FR-001, FR-003, FR-004 (have annotations)
      high: 2          # inventory, bulk-import (inferred)
      medium: 0
      low: 0

confidence_stats:
  average: 0.83
  median: 0.85
  min: 0.70
  max: 0.95
```

**Expected `extracted-spec.md` Requirements**:
- FR-001: Product Creation (confidence: 0.95)
- FR-003: Product Update (confidence: 0.75 - has drift)
- FR-004: Product Deletion (confidence: 0.90)
- FR-NEW-1: Product Inventory Retrieval (confidence: 0.75)
- FR-NEW-2: Bulk Product Import (confidence: 0.70)

**Validation Checklist**:
- [ ] Extracted all 5 public endpoints
- [ ] Recognized FastAPI decorators (@app.post, @app.get, etc.)
- [ ] Extracted route patterns correctly
- [ ] Did NOT extract archive_discontinued_products (@internal)
- [ ] Average confidence >= 0.70
- [ ] Behavioral drift in FR-003 flagged
- [ ] Type hints from Pydantic models captured

---

## Validation Phase 3: Cross-Language Consistency

### Test 5: Language-Agnostic Pattern Detection

**Objective**: Verify that common patterns are detected across languages

**Validation Checklist**:

**Annotation Recognition**:
- [ ] TypeScript: `// @speckit:FR:FR-001` recognized
- [ ] TypeScript: `// @speckit:AS:AS-1A` recognized
- [ ] TypeScript: `// @internal` recognized
- [ ] Python: `# @speckit:FR:FR-001` recognized
- [ ] Python: `# @internal` recognized

**Test Scenario Patterns**:
- [ ] TypeScript: `[TEST:AS-1A]` in comments recognized
- [ ] Python: `[TEST:AS-1A]` in docstrings recognized
- [ ] Test file patterns: `*.test.ts`, `*.spec.ts`, `test_*.py` recognized

**API Patterns**:
- [ ] TypeScript: `export async function` recognized as public API
- [ ] TypeScript: Functions starting with `_` ignored
- [ ] Python: FastAPI route decorators recognized
- [ ] Python: Functions starting with `_` ignored
- [ ] Python: `@internal` marker respected

**Framework Detection**:
- [ ] TypeScript: Jest test framework detected
- [ ] Python: FastAPI framework detected
- [ ] Python: pytest framework detected

---

## Validation Phase 4: Quality Gates

### Test 6: Quality Gate Validation

**Objective**: Verify that quality gates fire correctly

**Steps**:
1. Run drift detection on TypeScript fixture
2. Check if gates would block based on thresholds

**Expected Gate Results**:

**QG-DRIFT-001: No Critical Drift**
- Status: ✅ PASS
- Reason: 0 critical items detected

**QG-DRIFT-002: High Drift Limit**
- TypeScript: ⚠️ PASS (2 HIGH items <= 5 threshold)
- Python: ⚠️ PASS (3 HIGH items <= 5 threshold)

**QG-DRIFT-003: FR → Code Coverage**
- TypeScript: ❌ FAIL (66% < 80% threshold)
- Python: ❌ FAIL (75% < 80% threshold)

**QG-DRIFT-004: Code → Spec Coverage**
- TypeScript: ❌ FAIL (50% < 70% threshold)
- Python: ❌ FAIL (60% < 70% threshold)

**Validation Checklist**:
- [ ] QG-DRIFT-001 calculated correctly (0 critical = PASS)
- [ ] QG-DRIFT-002 calculated correctly (count <= 5 = PASS)
- [ ] QG-DRIFT-003 calculated correctly (FR coverage percentage)
- [ ] QG-DRIFT-004 calculated correctly (Code coverage percentage)
- [ ] Gate failures clearly communicated in report
- [ ] Recommendations provided for failing gates

---

## Validation Phase 5: Performance & Edge Cases

### Test 7: Performance Benchmarks

**Objective**: Verify acceptable performance on small fixtures

**Validation Checklist**:
- [ ] TypeScript drift detection completes in < 30 seconds
- [ ] Python drift detection completes in < 30 seconds
- [ ] TypeScript reverse-engineering completes in < 2 minutes
- [ ] Python reverse-engineering completes in < 2 minutes
- [ ] Memory usage remains reasonable (< 1GB)

### Test 8: Edge Cases

**Objective**: Test handling of edge cases

**Test Cases**:

1. **Empty spec.md**:
   - Expected: All code flagged as reverse drift
   - Severity: HIGH for public APIs

2. **Empty codebase**:
   - Expected: All FRs flagged as forward drift
   - Severity: HIGH

3. **No annotations**:
   - Expected: Lower confidence scores (0.70-0.80 range)
   - Should still infer from patterns

4. **Ambiguous naming**:
   - Example: `function process(data)` with no context
   - Expected: Lower confidence (0.50-0.60)
   - Flagged for manual review

5. **Multiple files per FR**:
   - Expected: All files listed in drift report
   - Traceability maintained across files

**Validation Checklist**:
- [ ] Edge cases handled gracefully (no crashes)
- [ ] Clear error messages for problematic cases
- [ ] Hallucination detection prevents false positives
- [ ] Low-confidence items flagged for review

---

## Validation Phase 6: Hallucination Detection

### Test 9: Hallucination Prevention

**Objective**: Verify LLM doesn't invent requirements

**Test Cases**:

1. **Generic function names**:
   - `function doStuff()` → Should have LOW confidence (<0.50)
   - Should be flagged as "speculative"

2. **No supporting evidence**:
   - No tests, no clear naming, no docs → LOW confidence
   - Should require manual review

3. **Contradictory evidence**:
   - Code suggests one thing, tests suggest another
   - Should flag as "inconsistent" with MEDIUM confidence

**Validation Checklist**:
- [ ] Confidence scores reflect evidence quality
- [ ] Low-confidence items clearly marked
- [ ] Speculative requirements flagged for review
- [ ] Contradictions detected and reported
- [ ] Hallucination rate < 5% (manual review required)

---

## Final Validation Summary

### Overall Checklist

**Drift Detection**:
- [ ] Forward drift detected (spec without code)
- [ ] Reverse drift detected (code without spec)
- [ ] Behavioral drift detected (logic mismatch)
- [ ] Correct alignment not flagged
- [ ] Internal functions ignored (@internal)
- [ ] Coverage metrics calculated

**Reverse-Engineering**:
- [ ] Requirements extracted from code
- [ ] Confidence scoring accurate
- [ ] Annotations recognized
- [ ] Test coverage analyzed
- [ ] Manifest generated correctly
- [ ] Drift comparison with canonical spec

**Quality Gates**:
- [ ] All 4 drift gates implemented
- [ ] Thresholds calculated correctly
- [ ] Pass/fail determination accurate
- [ ] Recommendations provided

**Cross-Language**:
- [ ] TypeScript patterns recognized
- [ ] Python patterns recognized
- [ ] Framework-specific detection works
- [ ] Consistent behavior across languages

**Performance**:
- [ ] Acceptable execution time
- [ ] Reasonable memory usage
- [ ] No crashes on edge cases

**Documentation**:
- [ ] Clear report format
- [ ] Actionable recommendations
- [ ] Traceability maintained
- [ ] User-friendly output

---

## Notes for Testers

1. **Manual Review Required**: Some validation items require human judgment (e.g., semantic drift detection quality)

2. **Expected Failures**: The test fixtures are DESIGNED to fail quality gates - this is correct behavior

3. **Confidence Calibration**: Confidence scores may need tuning based on real-world usage

4. **Language Expansion**: If adding Go or Java support, create similar test fixtures

5. **Iteration**: This is v0.4.0 - expect to iterate based on dogfooding results

---

**Validation Performed By**: __________________
**Date**: __________________
**Version Tested**: __________________
**Result**: ☐ PASS  ☐ FAIL (see notes)
**Notes**:

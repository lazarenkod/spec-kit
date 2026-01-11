# TypeScript Drift Test Fixture

Test fixture for validating spec-code drift detection and reverse-engineering capabilities.

## Intentional Drift Scenarios

### 1. Forward Drift (Spec → Code)

**FR-002: User Password Reset**
- ✅ Defined in `spec.md`
- ❌ NOT implemented in `src/api.ts`
- ❌ No `@speckit:FR:FR-002` annotation

**Expected Detection**: DRIFT-001 "Unimplemented requirement FR-002" (HIGH)

### 2. Reverse Drift (Code → Spec)

**deleteUser() function**
- ❌ NOT in `spec.md`
- ✅ Implemented in `src/api.ts:61-76`
- ❌ No FR mapping

**Expected Detection**: DRIFT-002 "Undocumented API deleteUser" (HIGH)

### 3. Behavioral Drift

**FR-003: User Update**
- ✅ Spec says: "Update user profile information (name **and email**)"
- ⚠️ Code only updates **name**, ignores email updates (`src/api.ts:48-62`)
- ✅ Has `@speckit:FR:FR-003` annotation

**Expected Detection**: DRIFT-003 "Behavioral drift: implementation differs from spec" (MEDIUM)

### 4. Correct Alignment ✅

**FR-001: User Creation**
- ✅ Defined in `spec.md`
- ✅ Implemented in `src/api.ts:22-45`
- ✅ Has `@speckit:FR:FR-001` annotation
- ✅ Test coverage: AS-1A, AS-1B

**Expected Detection**: No drift

## Testing Instructions

### Run Drift Detection

```bash
cd /Users/dmitry.lazarenko/Documents/projects/spec-kit/.test-fixtures/typescript-drift-test
/speckit.analyze --profile drift
```

**Expected Output**: `drift-report.md` with:
- 1 HIGH forward drift (FR-002 unimplemented)
- 1 HIGH reverse drift (deleteUser undocumented)
- 1 MEDIUM behavioral drift (updateUser logic mismatch)
- Coverage: FR → Code: 66% (2/3 FRs), Code → Spec: 50% (2/4 public APIs)

### Run Reverse-Engineering

```bash
cd /Users/dmitry.lazarenko/Documents/projects/spec-kit/.test-fixtures/typescript-drift-test
/speckit.reverse-engineer --scope "src/**/*.ts" --exclude "*.test.ts"
```

**Expected Output**: `reverse-engineered/extracted-spec.md` with:
- FR-001: User Creation (confidence: 0.95 - has annotation + tests)
- FR-003: User Update (confidence: 0.80 - has annotation, behavior drift flagged)
- FR-NEW-1: User Deletion (confidence: 0.70 - inferred from code, no tests)

## Project Structure

```
typescript-drift-test/
├── spec.md                 # Canonical specification (3 FRs)
├── src/
│   ├── api.ts             # Implementation (4 public functions)
│   └── api.test.ts        # Tests (covers FR-001, FR-003, deleteUser)
├── package.json
└── README.md              # This file
```

## Confidence Scoring Examples

| Function | Annotation | Tests | Naming | Docs | Confidence |
|----------|-----------|-------|--------|------|------------|
| createUser | ✅ FR-001 | ✅ AS-1A, AS-1B | ✅ Clear | ✅ JSDoc | 0.95 (EXPLICIT) |
| updateUser | ✅ FR-003 | ⚠️ Partial | ✅ Clear | ✅ JSDoc | 0.80 (HIGH) |
| deleteUser | ❌ None | ✅ Yes | ✅ Clear | ✅ JSDoc | 0.70 (HIGH) |
| archiveInactiveUsers | ✅ @internal | ❌ None | ⚠️ Internal | ✅ JSDoc | N/A (internal) |

## Expected Traceability Matrix

| FR ID | Description | Implementation | Test Coverage | Status |
|-------|-------------|----------------|---------------|--------|
| FR-001 | User Creation | src/api.ts:22 | ✅ AS-1A, AS-1B | ✅ Aligned |
| FR-002 | Password Reset | ❌ NOT FOUND | ❌ None | ❌ Forward Drift |
| FR-003 | User Update | src/api.ts:48 | ⚠️ AS-3A (partial) | ⚠️ Behavioral Drift |
| N/A | User Deletion | src/api.ts:61 | ✅ Tests exist | ❌ Reverse Drift |

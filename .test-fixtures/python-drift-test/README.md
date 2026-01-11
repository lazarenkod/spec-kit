# Python Drift Test Fixture

Test fixture for validating spec-code drift detection and reverse-engineering capabilities on Python/FastAPI projects.

## Intentional Drift Scenarios

### 1. Forward Drift (Spec → Code)

**FR-002: Product Search**
- ✅ Defined in `spec.md`
- ❌ NOT implemented in `src/api.py`
- ❌ No `@speckit:FR:FR-002` annotation
- ❌ No API endpoint

**Expected Detection**: DRIFT-001 "Unimplemented requirement FR-002" (HIGH)

### 2. Reverse Drift (Code → Spec)

**Two undocumented endpoints:**

**A) GET /api/products/{id}/inventory endpoint**
- ❌ NOT in `spec.md`
- ✅ Implemented in `src/api.py:110-128`
- ❌ No FR mapping
- ✅ Has tests

**Expected Detection**: DRIFT-002 "Undocumented API get_product_inventory" (HIGH)

**B) POST /api/products/bulk-import endpoint**
- ❌ NOT in `spec.md`
- ✅ Implemented in `src/api.py:131-152`
- ❌ No FR mapping
- ✅ Has tests

**Expected Detection**: DRIFT-003 "Undocumented API bulk_import_products" (HIGH)

### 3. Behavioral Drift

**FR-003: Product Update**
- ✅ Spec says: "Update product information including **price and stock levels**"
- ⚠️ Code only updates **price**, ignores stock/name/description updates (`src/api.py:57-76`)
- ✅ Has `@speckit:FR:FR-003` annotation
- ✅ Has audit log for price changes

**Expected Detection**: DRIFT-004 "Behavioral drift: implementation differs from spec" (MEDIUM)

### 4. Correct Alignment ✅

**FR-001: Product Creation**
- ✅ Defined in `spec.md`
- ✅ Implemented in `src/api.py:38-55`
- ✅ Has `@speckit:FR:FR-001` annotation
- ✅ Test coverage: AS-1A, AS-1B
- ✅ All validations match spec

**FR-004: Product Deletion**
- ✅ Defined in `spec.md`
- ✅ Implemented in `src/api.py:79-96`
- ✅ Has `@speckit:FR:FR-004` annotation
- ✅ Test coverage: AS-4A
- ✅ Soft delete behavior matches spec

**Expected Detection**: No drift

## Testing Instructions

### Run Drift Detection

```bash
cd /Users/dmitry.lazarenko/Documents/projects/spec-kit/.test-fixtures/python-drift-test
/speckit.analyze --profile drift
```

**Expected Output**: `drift-report.md` with:
- 1 HIGH forward drift (FR-002 unimplemented)
- 2 HIGH reverse drift (inventory endpoint, bulk-import endpoint)
- 1 MEDIUM behavioral drift (update_product logic mismatch)
- Coverage: FR → Code: 75% (3/4 FRs), Code → Spec: 60% (3/5 public APIs)

### Run Reverse-Engineering

```bash
cd /Users/dmitry.lazarenko/Documents/projects/spec-kit/.test-fixtures/python-drift-test
/speckit.reverse-engineer --scope "src/**/*.py" --exclude "tests/*" --language python
```

**Expected Output**: `reverse-engineered/extracted-spec.md` with:
- FR-001: Product Creation (confidence: 0.95 - has annotation + tests)
- FR-003: Product Update (confidence: 0.75 - has annotation, behavior drift flagged)
- FR-004: Product Deletion (confidence: 0.90 - has annotation + tests)
- FR-NEW-1: Product Inventory Retrieval (confidence: 0.75 - inferred from code + tests)
- FR-NEW-2: Bulk Product Import (confidence: 0.70 - inferred from code + tests)

## Project Structure

```
python-drift-test/
├── spec.md                 # Canonical specification (4 FRs)
├── src/
│   └── api.py              # FastAPI implementation (5 public endpoints)
├── tests/
│   └── test_api.py         # Tests (covers FR-001, FR-003, FR-004, inventory, bulk-import)
├── requirements.txt
└── README.md               # This file
```

## Confidence Scoring Examples

| Endpoint | Annotation | Tests | Naming | Docs | Confidence |
|----------|-----------|-------|--------|------|------------|
| create_product | ✅ FR-001 | ✅ AS-1A, AS-1B | ✅ Clear | ✅ Docstring | 0.95 (EXPLICIT) |
| update_product | ✅ FR-003 | ⚠️ Partial | ✅ Clear | ✅ Docstring | 0.75 (HIGH) |
| delete_product | ✅ FR-004 | ✅ AS-4A | ✅ Clear | ✅ Docstring | 0.90 (EXPLICIT) |
| get_product_inventory | ❌ None | ✅ Yes | ✅ Clear | ✅ Docstring | 0.75 (HIGH) |
| bulk_import_products | ❌ None | ✅ Yes | ✅ Clear | ✅ Docstring | 0.70 (HIGH) |
| archive_discontinued_products | ✅ @internal | ❌ None | ⚠️ Internal | ✅ Docstring | N/A (internal) |

## Expected Traceability Matrix

| FR ID | Description | Implementation | Test Coverage | Status |
|-------|-------------|----------------|---------------|--------|
| FR-001 | Product Creation | src/api.py:38 | ✅ AS-1A, AS-1B | ✅ Aligned |
| FR-002 | Product Search | ❌ NOT FOUND | ❌ None | ❌ Forward Drift |
| FR-003 | Product Update | src/api.py:57 | ⚠️ AS-3A (partial) | ⚠️ Behavioral Drift |
| FR-004 | Product Deletion | src/api.py:79 | ✅ AS-4A | ✅ Aligned |
| N/A | Product Inventory | src/api.py:110 | ✅ Tests exist | ❌ Reverse Drift |
| N/A | Bulk Import | src/api.py:131 | ✅ Tests exist | ❌ Reverse Drift |

## FastAPI-Specific Detection Patterns

The drift detection should recognize FastAPI decorators:
- `@app.post()` → POST endpoint
- `@app.get()` → GET endpoint
- `@app.patch()` → PATCH endpoint
- `@app.delete()` → DELETE endpoint

Route patterns:
- `/api/products` → Public API
- `/api/products/{product_id}` → Single resource API
- `/api/products/bulk-import` → Batch operation API

## Language-Specific Features

**Python patterns to detect:**
- Pydantic models for validation (ProductData, Product)
- FastAPI route decorators for API endpoints
- `async def` functions for async operations
- Type hints for parameters and return values
- Docstrings for function documentation
- `@internal` marker for internal functions

**Expected extraction quality:**
- Average confidence: 0.80+ (due to strong typing and decorators)
- Hallucination rate: <5% (FastAPI decorators provide clear intent)
- FR inference accuracy: 85%+ (route paths and docstrings are descriptive)

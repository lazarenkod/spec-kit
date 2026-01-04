# Property Quality Score (PQS) Rubric

**Version**: 1.0
**Purpose**: Measure property-based testing quality for `/speckit.properties`

---

## Score Calculation

```
PQS = (
  Requirement_Coverage × 0.30 +
  Type_Diversity × 0.20 +
  Generator_Quality × 0.20 +
  Shrunk_Examples × 0.15 +
  EARS_Alignment × 0.15
) × 100
```

**Thresholds**:
- ≥80: Excellent - Ready for production
- 70-79: Good - Minor improvements suggested
- 60-69: Acceptable - Review recommended
- <60: Insufficient - Block merge

---

## Dimension 1: Requirement Coverage (30%)

| Score | Criteria |
|-------|----------|
| 100 | All FR/AS/EC have corresponding properties |
| 80 | ≥90% coverage, all P0/P1 requirements covered |
| 60 | ≥80% coverage, all P0 requirements covered |
| 40 | ≥70% coverage |
| 20 | ≥50% coverage |
| 0 | <50% coverage |

**Measurement**: `covered_requirements / total_requirements × 100`

---

## Dimension 2: Type Diversity (20%)

| Score | Criteria |
|-------|----------|
| 100 | All 6 property types used appropriately |
| 80 | 5 types, including inverse + invariant |
| 60 | 4 types, including inverse |
| 40 | 3 types |
| 20 | 2 types |
| 0 | Only 1 type or inappropriate type selection |

**Property Types**:
1. Inverse (round-trip)
2. Idempotent (repeated application)
3. Invariant (always holds)
4. Boundary (edge cases)
5. Commutative (order-independent)
6. Model-based (state machine)

---

## Dimension 3: Generator Quality (20%)

| Score | Criteria |
|-------|----------|
| 100 | Custom generators for all entities, security generators included |
| 80 | Custom generators for main entities, boundary generators |
| 60 | Mix of custom and built-in generators |
| 40 | Mostly built-in generators with some customization |
| 20 | Only built-in generators |
| 0 | Inadequate generators, poor coverage |

**Quality Indicators**:
- Entity-specific generators (User, Order, etc.)
- Boundary value generators (empty, max, min)
- Security payload generators (SQL injection, XSS)
- Relationship-aware generators (foreign keys valid)

---

## Dimension 4: Shrunk Examples (15%)

| Score | Criteria |
|-------|----------|
| 100 | ≥5 shrunk examples per property, documented with dates |
| 80 | 3-4 shrunk examples per property |
| 60 | 1-2 shrunk examples per property |
| 40 | Some shrunk examples, inconsistent |
| 20 | Few shrunk examples |
| 0 | No shrunk examples preserved |

**Shrunk Example Quality**:
- Minimal reproduction case
- Date/iteration recorded
- Root cause annotated
- Regression prevention verified

---

## Dimension 5: EARS Alignment (15%)

| Score | Criteria |
|-------|----------|
| 100 | All properties traceable to EARS forms, no ambiguity |
| 80 | ≥90% EARS alignment, minor ambiguities resolved |
| 60 | ≥80% EARS alignment |
| 40 | ≥70% EARS alignment, some informal properties |
| 20 | ≥50% EARS alignment |
| 0 | <50% or no EARS transformation |

**EARS Types**:
- Ubiquitous: "System SHALL..."
- Event-driven: "WHEN trigger THEN action"
- State-driven: "WHILE state THEN action"
- Unwanted: "IF condition THEN prevent"
- Option: "WHERE condition THEN option"

---

## Example Scoring

### Feature: User Registration

| Dimension | Raw Score | Weight | Weighted |
|-----------|-----------|--------|----------|
| Requirement Coverage | 85 | 0.30 | 25.5 |
| Type Diversity | 80 | 0.20 | 16.0 |
| Generator Quality | 90 | 0.20 | 18.0 |
| Shrunk Examples | 60 | 0.15 | 9.0 |
| EARS Alignment | 75 | 0.15 | 11.25 |
| **TOTAL PQS** | | | **79.75** |

**Assessment**: Good (70-79) - Minor improvements suggested

**Recommendations**:
1. Add more shrunk examples (currently 2 per property)
2. Improve EARS transformation for EC-003, EC-004
3. Consider adding model-based tests for registration workflow

---

## Integration with Quality Gates

| PQS Range | Gate Status | Action |
|-----------|-------------|--------|
| ≥80 | VG-PQS PASS | Proceed to merge |
| 70-79 | VG-PQS WARN | Review suggestions, optional fixes |
| 60-69 | VG-PQS FAIL | Required improvements before merge |
| <60 | VG-PQS BLOCK | Block merge, major rework needed |

---

## Automated Calculation

The `/speckit.properties` command calculates PQS automatically:

```bash
/speckit.properties --dry-run  # Shows PQS without generating code
/speckit.properties --profile full  # Full PQS calculation
```

Output includes:
- Overall PQS score
- Per-dimension breakdown
- Specific improvement recommendations
- Comparison to previous runs

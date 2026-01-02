# Specification Quality Scorer

> Multi-dimensional specification quality scoring using G-Eval framework. Import this module in spec-quality-scorer subagent.

## Purpose

Provide objective, repeatable spec quality measurement before implementation:
1. **Predictive Quality**: Correlate spec score with implementation success
2. **Actionable Feedback**: Dimension-specific improvement suggestions
3. **Quality Gate**: Block low-quality specs from proceeding to implementation
4. **Trend Tracking**: Monitor spec quality improvement over time

Research basis: G-Eval framework (LLM-as-a-judge, 2025) achieves 0.85+ correlation with human expert ratings.

---

## Data Structures

```text
QualityDimension = {
  name: string,                        # "Clarity", "Completeness", etc.
  score: float,                        # 0.0 to 1.0
  weight: float,                       # Contribution to overall (sum = 1.0)
  explanation: string,                 # Human-readable score justification
  improvement_suggestions: List[string] # Actionable improvements
}

SpecQualityScore = {
  overall_score: float,                # 0-100 scale
  dimensions: List[QualityDimension],  # All 5 dimension scores
  pass_threshold: float,               # 70.0 (Grade C)
  grade: "A" | "B" | "C" | "D" | "F",  # Letter grade
  recommendation: string,              # Action guidance
  passed: boolean                      # overall_score >= pass_threshold
}
```

---

## Dimension Weights

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Clarity | 25% | Ambiguous specs cause 30% of code generation errors |
| Completeness | 25% | Missing requirements cause 40% of rework |
| Testability | 20% | Untestable specs cannot be validated |
| Consistency | 15% | Contradictions cause implementation deadlocks |
| Traceability | 15% | Poor traceability breaks audit trails |

```text
DIMENSION_WEIGHTS = {
  clarity: 0.25,
  completeness: 0.25,
  testability: 0.20,
  consistency: 0.15,
  traceability: 0.15
}
```

---

## Grade Scale

| Grade | Score Range | Description | Action |
|-------|-------------|-------------|--------|
| **A** | 90-100 | Excellent — Ship with confidence | Proceed to implementation |
| **B** | 80-89 | Good — Minor improvements recommended | Proceed with optional improvements |
| **C** | 70-79 | Acceptable — Address suggestions | Proceed after addressing key issues |
| **D** | 60-69 | Below Standard — Significant gaps | Revise before implementation |
| **F** | < 60 | Failing — Major revision required | Block until major revision |

**Pass Threshold**: 70.0 (Grade C or higher required)

---

## G-Eval Rubrics

### Clarity Rubric

```text
CLARITY_RUBRIC = {
  excellent: "All requirements use precise, measurable language. No vague terms. Technical specifications are unambiguous. Every actor clearly identified.",
  good: "Most requirements are precise. 1-2 minor vague terms that don't affect implementation. Actors mostly clear.",
  acceptable: "Requirements are generally understandable. Some vague terms present. May need 1-2 clarification questions.",
  below_standard: "Multiple vague terms. Several requirements open to interpretation. Implementation would require significant clarification.",
  poor: "Requirements are mostly vague or subjective. Cannot implement without extensive clarification."
}
```

### Completeness Rubric

```text
COMPLETENESS_RUBRIC = {
  excellent: "All functional areas covered. Error handling complete. Edge cases addressed. Non-functional requirements specified.",
  good: "Core functionality complete. Most error handling present. Minor gaps in edge cases.",
  acceptable: "Main requirements present. Some gaps in error handling or edge cases. Can implement core flow.",
  below_standard: "Missing several requirements. Error handling incomplete. Major gaps need addressing.",
  poor: "Fundamental requirements missing. Cannot implement primary use case."
}
```

### Testability Rubric

```text
TESTABILITY_RUBRIC = {
  excellent: "Every requirement has measurable acceptance criteria. All scenarios testable. Clear pass/fail conditions.",
  good: "Most requirements testable. 1-2 scenarios lack specific criteria. Generally measurable.",
  acceptable: "Core requirements testable. Some scenarios need clearer criteria. Can write basic tests.",
  below_standard: "Many requirements lack testable criteria. Unclear what constitutes success.",
  poor: "Requirements cannot be objectively tested. No measurable criteria."
}
```

### Consistency Rubric

```text
CONSISTENCY_RUBRIC = {
  excellent: "No contradictions. Terminology consistent throughout. Constraints align. Behavior unified.",
  good: "No logical contradictions. Minor terminology variations. Constraints compatible.",
  acceptable: "No critical contradictions. Some terminology inconsistency. Minor conflicts resolvable.",
  below_standard: "Contains contradictions that affect implementation. Inconsistent terminology causes confusion.",
  poor: "Multiple contradictions. Cannot implement without resolving conflicts."
}
```

### Traceability Rubric

```text
TRACEABILITY_RUBRIC = {
  excellent: "100% FR→AS→EC coverage. All links bidirectional. Orphan detection complete.",
  good: "90%+ coverage. Most links present. Minor gaps in traceability.",
  acceptable: "75%+ coverage. Core requirements traceable. Some orphan scenarios.",
  below_standard: "50-74% coverage. Many requirements not linked to scenarios.",
  poor: "< 50% coverage. Traceability largely missing."
}
```

---

## Main Algorithm

```text
SCORE_SPECIFICATION(spec, context = {}):

  # Evaluate each dimension
  clarity = EVALUATE_CLARITY(spec)
  completeness = EVALUATE_COMPLETENESS(spec, context.completeness_results)
  testability = EVALUATE_TESTABILITY(spec)
  consistency = EVALUATE_CONSISTENCY(spec)
  traceability = EVALUATE_TRACEABILITY(spec)

  dimensions = [clarity, completeness, testability, consistency, traceability]

  # Calculate weighted overall score
  overall_score = 0.0
  FOR dim IN dimensions:
    overall_score += dim.score × dim.weight × 100

  # Assign grade
  grade = ASSIGN_GRADE(overall_score)

  # Generate recommendation
  recommendation = GENERATE_RECOMMENDATION(overall_score, grade, dimensions)

  RETURN SpecQualityScore(
    overall_score: ROUND(overall_score, 1),
    dimensions: dimensions,
    pass_threshold: 70.0,
    grade: grade,
    recommendation: recommendation,
    passed: overall_score >= 70.0
  )
```

---

## Dimension Evaluation Algorithms

### EVALUATE_CLARITY

```text
EVALUATE_CLARITY(spec):
  requirements = spec.functional_requirements

  # ===== Automated Component (60%) =====
  # Import ambiguity detection
  LOAD DETECT_AMBIGUITIES from "templates/shared/quality/ambiguity-patterns.md"

  ambiguities = DETECT_AMBIGUITIES(requirements, spec.glossary OR {})

  # Count by severity
  critical_count = COUNT(ambiguities WHERE severity == "CRITICAL")
  high_count = COUNT(ambiguities WHERE severity == "HIGH")
  medium_count = COUNT(ambiguities WHERE severity == "MEDIUM")

  # Severity-weighted penalty: CRITICAL=0.15, HIGH=0.08, MEDIUM=0.03
  ambiguity_penalty = (critical_count × 0.15) + (high_count × 0.08) + (medium_count × 0.03)
  automated_score = MAX(0.0, 1.0 - ambiguity_penalty)

  # ===== LLM Component (40%) =====
  llm_result = LLM_GEVAL_RUBRIC("clarity", requirements, CLARITY_RUBRIC)
  llm_score = llm_result.score  # 0.0 to 1.0

  # ===== Combine =====
  final_score = (automated_score × 0.6) + (llm_score × 0.4)

  # Generate suggestions
  suggestions = []
  IF len(ambiguities) > 0:
    suggestions.append("Resolve {len(ambiguities)} ambiguities via /speckit.clarify")
  IF critical_count > 0:
    suggestions.append("Address {critical_count} CRITICAL ambiguities immediately")
  IF llm_score < 0.7:
    suggestions.append("Improve technical precision of requirements language")
  FOR neg_example IN llm_result.negative_examples[:2]:
    suggestions.append("Improve: {neg_example}")

  RETURN QualityDimension(
    name: "Clarity",
    score: final_score,
    weight: 0.25,
    explanation: "Ambiguities: {len(ambiguities)} ({critical_count} critical, {high_count} high). LLM clarity: {llm_score:.2f}",
    improvement_suggestions: suggestions[:3]
  )
```

### EVALUATE_COMPLETENESS

```text
EVALUATE_COMPLETENESS(spec, completeness_results = null):

  # ===== Automated Component (60%) =====
  # Use completeness-checker results if available
  IF completeness_results IS NOT null:
    gaps = completeness_results.gaps
  ELSE:
    LOAD COMPLETENESS_CATEGORIES from "templates/shared/quality/completeness-checklist.md"
    gaps = DETECT_COMPLETENESS_GAPS(spec, COMPLETENESS_CATEGORIES)

  # Severity-weighted gap penalty
  critical_gaps = COUNT(gaps WHERE severity == "CRITICAL")
  high_gaps = COUNT(gaps WHERE severity == "HIGH")
  medium_gaps = COUNT(gaps WHERE severity == "MEDIUM")

  # CRITICAL=0.20, HIGH=0.10, MEDIUM=0.05
  gap_penalty = (critical_gaps × 0.20) + (high_gaps × 0.10) + (medium_gaps × 0.05)
  automated_score = MAX(0.0, 1.0 - gap_penalty)

  # ===== LLM Component (40%) =====
  llm_result = LLM_GEVAL_RUBRIC("completeness", spec.functional_requirements, COMPLETENESS_RUBRIC)
  llm_score = llm_result.score

  # ===== Combine =====
  final_score = (automated_score × 0.6) + (llm_score × 0.4)

  # Generate suggestions
  suggestions = []
  IF critical_gaps > 0:
    suggestions.append("Address {critical_gaps} CRITICAL completeness gaps")
  IF high_gaps > 0:
    suggestions.append("Fill {high_gaps} HIGH-priority missing sections")
  FOR gap IN gaps[:2]:
    suggestions.append("Add: {gap.category} - {gap.description}")

  RETURN QualityDimension(
    name: "Completeness",
    score: final_score,
    weight: 0.25,
    explanation: "{len(gaps)} gaps ({critical_gaps} critical, {high_gaps} high, {medium_gaps} medium)",
    improvement_suggestions: suggestions[:3]
  )
```

### EVALUATE_TESTABILITY

```text
EVALUATE_TESTABILITY(spec):

  scenarios = spec.acceptance_scenarios OR []
  requirements = spec.functional_requirements

  # ===== Automated Component (60%) =====

  # 1. Testable scenario ratio (40%)
  testable_scenarios = []
  FOR scenario IN scenarios:
    IF HAS_MEASURABLE_CRITERIA(scenario):
      testable_scenarios.append(scenario)

  testable_ratio = len(testable_scenarios) / MAX(1, len(scenarios))

  # 2. FR→AS traceability (20%)
  linked_frs = SET()
  FOR scenario IN scenarios:
    linked_frs.update(EXTRACT_FR_REFERENCES(scenario))

  traceability_ratio = len(linked_frs) / MAX(1, len(requirements))

  automated_score = (testable_ratio × 0.67) + (traceability_ratio × 0.33)

  # ===== LLM Component (40%) =====
  llm_result = LLM_GEVAL_RUBRIC("testability", requirements, TESTABILITY_RUBRIC)
  llm_score = llm_result.score

  # ===== Combine =====
  final_score = (automated_score × 0.6) + (llm_score × 0.4)

  # Generate suggestions
  suggestions = []
  untestable_count = len(scenarios) - len(testable_scenarios)
  IF untestable_count > 0:
    suggestions.append("Add measurable criteria to {untestable_count} scenarios")

  unlinked_frs = len(requirements) - len(linked_frs)
  IF unlinked_frs > 0:
    suggestions.append("Link {unlinked_frs} requirements to acceptance scenarios")

  IF llm_score < 0.7:
    suggestions.append("Define clearer pass/fail conditions for tests")

  RETURN QualityDimension(
    name: "Testability",
    score: final_score,
    weight: 0.20,
    explanation: "Testable scenarios: {PERCENT(testable_ratio)}%, FR→AS coverage: {PERCENT(traceability_ratio)}%",
    improvement_suggestions: suggestions[:3]
  )

HAS_MEASURABLE_CRITERIA(scenario):
  # Check for quantifiable expectations
  text = scenario.expected_outcome OR scenario.then_clause

  # Look for measurable patterns
  has_number = REGEX_MATCH(text, r'\d+')  # Contains numbers
  has_comparison = REGEX_MATCH(text, r'(less than|greater than|within|equals|exactly|at least|at most)')
  has_status = REGEX_MATCH(text, r'(status|code|response)\s*[:=]?\s*\d+')
  has_boolean = REGEX_MATCH(text, r'(returns|displays|shows|contains|includes|is)\s+(true|false|visible|hidden)')

  RETURN has_number OR has_comparison OR has_status OR has_boolean
```

### EVALUATE_CONSISTENCY

```text
EVALUATE_CONSISTENCY(spec):

  requirements = spec.functional_requirements

  # ===== LLM Contradiction Detection (100% LLM for this dimension) =====

  prompt = """You are an expert requirements analyst detecting CONTRADICTIONS.

REQUIREMENTS:
{FORMAT_NUMBERED(requirements)}

GLOSSARY:
{spec.glossary OR "No glossary provided"}

TASK: Find requirements that contradict each other.

CONTRADICTION TYPES:
1. **Logical**: A says X, B says NOT X
2. **Semantic**: Same term used with different meanings
3. **Constraint**: Conflicting limits (e.g., "max 100" vs "minimum 150")
4. **Behavioral**: Same trigger, different outcomes
5. **Temporal**: Conflicting timing requirements

For each contradiction found:
- Identify both requirements by ID (FR-XXX)
- Explain the conflict
- Rate severity: CRITICAL (blocks implementation) / HIGH (causes errors) / MEDIUM (causes confusion)

OUTPUT FORMAT (strict JSON):
{
  "contradictions": [
    {
      "requirement_a": "FR-001",
      "requirement_b": "FR-005",
      "type": "constraint",
      "explanation": "FR-001 requires max 100ms, FR-005 requires at least 150ms processing",
      "severity": "CRITICAL"
    }
  ],
  "score": 4,
  "reasoning": "Found 1 critical contradiction in constraints..."
}

If NO contradictions found, return empty array and score 5."""

  response = LLM_CALL(prompt, temperature=0.2)
  result = PARSE_JSON(response)

  contradictions = result.contradictions
  llm_score = result.score / 5.0

  # Calculate penalty from contradictions
  critical_count = COUNT(contradictions WHERE severity == "CRITICAL")
  high_count = COUNT(contradictions WHERE severity == "HIGH")
  medium_count = COUNT(contradictions WHERE severity == "MEDIUM")

  # CRITICAL=0.25, HIGH=0.15, MEDIUM=0.05
  contradiction_penalty = (critical_count × 0.25) + (high_count × 0.15) + (medium_count × 0.05)
  penalty_score = MAX(0.0, 1.0 - contradiction_penalty)

  # Combine LLM score with penalty (equal weight)
  final_score = (llm_score × 0.5) + (penalty_score × 0.5)

  # Generate suggestions
  suggestions = []
  IF critical_count > 0:
    suggestions.append("BLOCKER: Resolve {critical_count} critical contradictions before implementation")
  FOR contradiction IN contradictions[:2]:
    suggestions.append("Resolve conflict: {contradiction.requirement_a} vs {contradiction.requirement_b}")

  RETURN QualityDimension(
    name: "Consistency",
    score: final_score,
    weight: 0.15,
    explanation: "{len(contradictions)} contradictions ({critical_count} critical, {high_count} high)",
    improvement_suggestions: suggestions[:3]
  )
```

### EVALUATE_TRACEABILITY

```text
EVALUATE_TRACEABILITY(spec):

  requirements = spec.functional_requirements
  scenarios = spec.acceptance_scenarios OR []
  edge_cases = spec.edge_cases OR []

  # ===== Automated Component (70%) =====

  # 1. FR→AS coverage (40%)
  frs_with_scenarios = SET()
  FOR scenario IN scenarios:
    refs = EXTRACT_FR_REFERENCES(scenario)
    frs_with_scenarios.update(refs)

  fr_as_coverage = len(frs_with_scenarios) / MAX(1, len(requirements))

  # 2. FR→EC coverage (30%)
  frs_with_edge_cases = SET()
  FOR edge_case IN edge_cases:
    refs = EXTRACT_FR_REFERENCES(edge_case)
    frs_with_edge_cases.update(refs)

  fr_ec_coverage = len(frs_with_edge_cases) / MAX(1, len(requirements))

  # Weighted automated score
  automated_score = (fr_as_coverage × 0.6) + (fr_ec_coverage × 0.4)

  # ===== LLM Component (30%) =====
  llm_result = LLM_GEVAL_RUBRIC("traceability", requirements, TRACEABILITY_RUBRIC)
  llm_score = llm_result.score

  # ===== Combine =====
  final_score = (automated_score × 0.7) + (llm_score × 0.3)

  # Identify orphans
  orphan_frs = []
  FOR i, req IN ENUMERATE(requirements):
    fr_id = "FR-{i+1:03d}"
    IF fr_id NOT IN frs_with_scenarios AND fr_id NOT IN frs_with_edge_cases:
      orphan_frs.append(fr_id)

  # Generate suggestions
  suggestions = []
  IF len(orphan_frs) > 0:
    suggestions.append("Add scenarios for orphan requirements: {', '.join(orphan_frs[:5])}")
  IF fr_as_coverage < 0.9:
    suggestions.append("Improve FR→AS coverage from {PERCENT(fr_as_coverage)}% to 90%+")
  IF fr_ec_coverage < 0.5:
    suggestions.append("Add edge cases for more requirements (currently {PERCENT(fr_ec_coverage)}%)")

  RETURN QualityDimension(
    name: "Traceability",
    score: final_score,
    weight: 0.15,
    explanation: "FR→AS: {PERCENT(fr_as_coverage)}%, FR→EC: {PERCENT(fr_ec_coverage)}%, Orphans: {len(orphan_frs)}",
    improvement_suggestions: suggestions[:3]
  )

EXTRACT_FR_REFERENCES(text_or_object):
  text = STRINGIFY(text_or_object)
  # Match FR-001, FR-002, etc.
  matches = REGEX_FINDALL(text, r'FR-\d{3}')
  RETURN SET(matches)
```

---

## LLM G-Eval Framework

```text
LLM_GEVAL_RUBRIC(dimension, requirements, rubric):

  prompt = """You are an expert requirements analyst evaluating {dimension.upper()}.

REQUIREMENTS TO EVALUATE:
{FORMAT_NUMBERED(requirements)}

EVALUATION CRITERIA (G-Eval rubric for {dimension}):
- **5 points (Excellent)**: {rubric.excellent}
- **4 points (Good)**: {rubric.good}
- **3 points (Acceptable)**: {rubric.acceptable}
- **2 points (Below Standard)**: {rubric.below_standard}
- **1 point (Poor)**: {rubric.poor}

TASK:
1. Carefully assess these requirements against the {dimension} rubric
2. Provide an integer score from 1-5
3. Justify your score with specific examples from the requirements
4. List positive examples (requirements that score well)
5. List negative examples (requirements that need improvement)

OUTPUT FORMAT (strict JSON):
{
  "score": 4,
  "reasoning": "Overall the requirements demonstrate good {dimension} because... However, some areas could improve...",
  "positive_examples": ["FR-001: Clearly specifies 200ms response time", "FR-003: Uses precise terminology"],
  "negative_examples": ["FR-005: Uses vague term 'quickly'", "FR-008: Actor unclear"]
}"""

  response = LLM_CALL(prompt, temperature=0.2)
  result = PARSE_JSON(response)

  RETURN {
    score: result.score / 5.0,  # Normalize to 0-1
    reasoning: result.reasoning,
    positive_examples: result.positive_examples OR [],
    negative_examples: result.negative_examples OR []
  }
```

---

## Grade Assignment

```text
ASSIGN_GRADE(overall_score):
  IF overall_score >= 90.0: RETURN "A"
  IF overall_score >= 80.0: RETURN "B"
  IF overall_score >= 70.0: RETURN "C"
  IF overall_score >= 60.0: RETURN "D"
  RETURN "F"
```

---

## Recommendation Generation

```text
GENERATE_RECOMMENDATION(overall_score, grade, dimensions):

  # Sort dimensions by score (lowest first)
  sorted_dims = SORT(dimensions, BY: dim.score, ORDER: ASC)
  lowest_dim = sorted_dims[0]
  second_lowest = sorted_dims[1] IF len(sorted_dims) > 1 ELSE null

  # Check for critical issues
  has_critical = ANY(dim.score < 0.50 FOR dim IN dimensions)
  consistency_dim = FIND(dimensions WHERE name == "Consistency")
  has_contradictions = consistency_dim AND "critical" IN consistency_dim.explanation.lower()

  # Generate recommendation based on grade
  SWITCH grade:
    CASE "A":
      base = "Excellent specification quality. Ship with confidence."
      IF lowest_dim.score < 0.85:
        base += " Optional: Minor {lowest_dim.name.lower()} improvements available."
      RETURN base

    CASE "B":
      RETURN "Good specification quality. Minor improvements recommended in {lowest_dim.name.lower()}. Proceed to implementation."

    CASE "C":
      RETURN "Acceptable quality. Address {lowest_dim.name.lower()} issues before implementation. Run /speckit.clarify for improvements."

    CASE "D":
      RETURN "Below standard. Significant gaps in {lowest_dim.name.lower()} and {second_lowest.name.lower() IF second_lowest ELSE 'other areas'}. Revise specification before proceeding."

    CASE "F":
      IF has_contradictions:
        RETURN "BLOCKED: Critical contradictions detected. Resolve conflicts before any implementation. Major revision required."
      ELIF has_critical:
        RETURN "BLOCKED: Critical quality failures in {lowest_dim.name.lower()}. Major revision required before implementation."
      ELSE:
        RETURN "Failing quality. Major revision required across multiple dimensions. Do not proceed to implementation."
```

---

## Helper Functions

```text
FORMAT_NUMBERED(requirements):
  lines = []
  FOR i, req IN ENUMERATE(requirements):
    lines.append("FR-{i+1:03d}: {req}")
  RETURN JOIN(lines, "\n")

PERCENT(ratio):
  RETURN ROUND(ratio × 100, 0)

STRINGIFY(obj):
  IF IS_STRING(obj): RETURN obj
  IF IS_DICT(obj): RETURN JSON_STRINGIFY(obj)
  RETURN STR(obj)
```

---

## Integration Points

| System | Integration |
|--------|-------------|
| `ambiguity-patterns.md` | Clarity automated scoring |
| `completeness-checklist.md` | Completeness gap detection |
| `completeness-checker` subagent | Provides pre-calculated gaps |
| `spec-template.md` | Quality Score output section |
| `checkpoints.md` | CP-SPEC-04 trigger |
| `criteria-spec.md` | SR-SPEC-19/20/21 validation |

---

## Quality Gates

| Gate | Criteria | Effect |
|------|----------|--------|
| SR-SPEC-19 | Overall score >= 70 | HIGH severity if failed |
| SR-SPEC-20 | All dimensions >= 0.50 | MEDIUM severity if failed |
| SR-SPEC-21 | No CRITICAL contradictions | CRITICAL severity if failed |

---

## Output Format

```markdown
### Specification Quality Score

**Overall Score**: XX.X / 100 (Grade: X)
**Status**: ✅ PASSED | ❌ FAILED
**Recommendation**: [Generated recommendation]

| Dimension | Score | Weight | Explanation |
|-----------|-------|--------|-------------|
| Clarity | X.XX | 25% | Ambiguities: N (X critical). LLM: X.XX |
| Completeness | X.XX | 25% | N gaps (X critical, Y high) |
| Testability | X.XX | 20% | Testable: X%, FR→AS: Y% |
| Consistency | X.XX | 15% | N contradictions (X critical) |
| Traceability | X.XX | 15% | FR→AS: X%, FR→EC: Y%, Orphans: N |

**Improvement Suggestions**:
1. [Highest priority suggestion from lowest-scoring dimension]
2. [Second suggestion]
3. [Third suggestion]
```

---

## Execution Flow

```text
EXECUTE_QUALITY_SCORING(spec, context):

  # 1. Validate input
  IF NOT spec.functional_requirements:
    RETURN ERROR("No functional requirements found")

  # 2. Score specification
  quality_score = SCORE_SPECIFICATION(spec, context)

  # 3. Format output
  output = FORMAT_QUALITY_SCORE(quality_score)

  # 4. Return result
  RETURN {
    score: quality_score,
    output: output,
    passed: quality_score.passed,
    gates: {
      SR_SPEC_19: quality_score.overall_score >= 70,
      SR_SPEC_20: ALL(dim.score >= 0.50 FOR dim IN quality_score.dimensions),
      SR_SPEC_21: NOT HAS_CRITICAL_CONTRADICTIONS(quality_score)
    }
  }

HAS_CRITICAL_CONTRADICTIONS(quality_score):
  consistency = FIND(quality_score.dimensions WHERE name == "Consistency")
  IF consistency:
    RETURN "critical" IN consistency.explanation.lower() AND "0 critical" NOT IN consistency.explanation.lower()
  RETURN false
```

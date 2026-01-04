# PGS (Property-Generated Solver) Protocol

This document defines the PGS iterative protocol for property-based testing refinement, based on research showing 23-37% pass@1 improvements over traditional TDD.

## Overview

PGS breaks the "cycle of self-deception" where tests share flaws with code by using collaborative agents that:
1. Generate properties independently from implementation
2. Execute tests to find counterexamples
3. Analyze failures to classify root cause
4. Iteratively refine properties OR flag implementation bugs

---

## PGS Architecture

### Agent Wave Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                                │
│  - Manages iteration cycles                                      │
│  - Detects deception patterns                                    │
│  - Enforces max_iterations                                       │
│  - Aggregates quality metrics                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  WAVE 1-3: Standard extraction and generation (see properties.md)│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  WAVE 4: TEST EXECUTION                                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ test-executor                                               │ │
│  │                                                             │ │
│  │ 1. Run generated property tests                             │ │
│  │ 2. Capture counterexamples                                  │ │
│  │ 3. Shrink to minimal failing cases                          │ │
│  │ 4. Record shrunk examples                                   │ │
│  │ 5. Trigger WAVE 5 if failures found                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (if counterexamples found)
┌─────────────────────────────────────────────────────────────────┐
│  WAVE 5: PGS ITERATION                                           │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ counterexample-analyzer                                     │ │
│  │                                                             │ │
│  │ Classify each counterexample:                               │ │
│  │ - PROPERTY_TOO_STRICT: Property needs relaxation            │ │
│  │ - IMPLEMENTATION_BUG: Code needs fixing                     │ │
│  │ - SPEC_AMBIGUITY: Specification is unclear                  │ │
│  │ - GENERATOR_ISSUE: Generator producing invalid inputs       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│                              ▼                                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐              │
│  │ property-    │ │ impl-        │ │ spec-        │              │
│  │ refiner      │ │ suggester    │ │ flagger      │              │
│  │              │ │              │ │              │              │
│  │ Relax prop   │ │ Suggest fix  │ │ Generate     │              │
│  │ Add assume   │ │ for impl bug │ │ clarify Q    │              │
│  │ Fix generator│ │              │ │              │              │
│  └──────────────┘ └──────────────┘ └──────────────┘              │
│                              │                                    │
│                              ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ deception-detector                                          │ │
│  │                                                             │ │
│  │ Check for deception patterns:                               │ │
│  │ - Property oscillation (A→B→A)                              │ │
│  │ - Persistent counterexample                                 │ │
│  │ - Coverage stagnation                                       │ │
│  │ - Agent conflict                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              (Loop back to WAVE 4 if iteration < max)
```

---

## Iteration Protocol

### Main Loop

```python
def pgs_iteration_loop(properties, max_iterations=5):
    """
    PGS main iteration loop.
    """
    iteration = 0
    iteration_history = []

    while iteration < max_iterations:
        iteration += 1

        # Step 1: Execute property tests
        results = execute_property_tests(properties)

        # Step 2: Check for success
        if results.all_passed:
            return PGSResult(
                status="SUCCESS",
                iterations=iteration,
                properties=properties,
                shrunk_examples=results.shrunk_examples
            )

        # Step 3: Analyze counterexamples
        classifications = []
        for counterexample in results.counterexamples:
            classification = analyze_counterexample(counterexample)
            classifications.append(classification)

        # Step 4: Apply resolutions
        resolutions = []
        for classification in classifications:
            resolution = apply_resolution(classification, properties)
            resolutions.append(resolution)

        # Step 5: Check for deception
        iteration_history.append({
            "iteration": iteration,
            "properties": snapshot(properties),
            "counterexamples": results.counterexamples,
            "classifications": classifications,
            "resolutions": resolutions
        })

        deception = detect_deception(iteration_history)
        if deception.detected:
            return PGSResult(
                status="ESCALATE",
                reason=deception.reason,
                iterations=iteration,
                properties=properties,
                unresolved=results.counterexamples
            )

        # Step 6: Update properties
        properties = apply_property_updates(properties, resolutions)

    # Max iterations reached
    return PGSResult(
        status="MAX_ITERATIONS",
        iterations=iteration,
        properties=properties,
        unresolved=[r for r in classifications if not r.resolved]
    )
```

---

## Counterexample Classification

### Classification Categories

| Category | Description | Resolution |
|----------|-------------|------------|
| **PROPERTY_TOO_STRICT** | Property is correct but too strict | Relax property with preconditions |
| **IMPLEMENTATION_BUG** | Property is correct, code is wrong | Flag for fix, block iteration |
| **SPEC_AMBIGUITY** | Specification is unclear | Generate clarify question |
| **GENERATOR_ISSUE** | Generator produces invalid inputs | Fix generator constraints |

### Classification Algorithm

```python
def analyze_counterexample(counterexample):
    """
    Classify a counterexample to determine resolution strategy.
    """
    property = counterexample.property
    value = counterexample.shrunk_value
    error = counterexample.error

    # Check if value is valid according to spec constraints
    if not is_valid_domain_value(value, property.entity):
        return Classification(
            type="GENERATOR_ISSUE",
            confidence=0.95,
            reason=f"Value {value} violates domain constraints",
            resolution="Add filter to generator"
        )

    # Check if property has implicit preconditions
    if has_implicit_preconditions(property, value):
        return Classification(
            type="PROPERTY_TOO_STRICT",
            confidence=0.85,
            reason=f"Property assumes precondition not stated",
            resolution="Add assume() clause"
        )

    # Check if spec is ambiguous about this case
    if is_spec_ambiguous(property, value):
        return Classification(
            type="SPEC_AMBIGUITY",
            confidence=0.80,
            reason=f"Spec doesn't clearly define behavior for {value}",
            resolution="Generate clarify question"
        )

    # Default: likely implementation bug
    return Classification(
        type="IMPLEMENTATION_BUG",
        confidence=0.75,
        reason=f"Property seems correct, implementation fails for {value}",
        resolution="Flag for implementation fix"
    )
```

### Confidence Factors

```yaml
classification_confidence:
  GENERATOR_ISSUE:
    high_confidence:
      - "Value outside declared constraints"
      - "Type mismatch with entity definition"
    medium_confidence:
      - "Edge case not in spec"

  PROPERTY_TOO_STRICT:
    high_confidence:
      - "Similar property succeeded with assume()"
      - "Related spec has explicit exception"
    medium_confidence:
      - "Common pattern for precondition"

  SPEC_AMBIGUITY:
    high_confidence:
      - "Multiple interpretations possible"
      - "No explicit edge case coverage"
    medium_confidence:
      - "Vague terms in original requirement"

  IMPLEMENTATION_BUG:
    high_confidence:
      - "Clear spec, clear property, code fails"
      - "Regression from previous passing tests"
    medium_confidence:
      - "Default classification"
```

---

## Resolution Strategies

### PROPERTY_TOO_STRICT Resolution

```python
def refine_strict_property(property, counterexample):
    """
    Relax an overly strict property.
    """
    strategies = []

    # Strategy 1: Add assume() clause
    if can_add_precondition(property, counterexample):
        new_precondition = infer_precondition(counterexample)
        strategies.append({
            "type": "add_assume",
            "before": property.formula,
            "after": f"assume({new_precondition}); {property.formula}",
            "code_change": f"assume({new_precondition})"
        })

    # Strategy 2: Narrow generator scope
    if can_narrow_generator(property, counterexample):
        new_filter = infer_filter(counterexample)
        strategies.append({
            "type": "narrow_generator",
            "before": property.generators.valid,
            "after": f"{property.generators.valid}.filter({new_filter})"
        })

    # Strategy 3: Split into multiple properties
    if should_split(property, counterexample):
        strategies.append({
            "type": "split_property",
            "original": property.id,
            "new_properties": split_property(property, counterexample)
        })

    return select_best_strategy(strategies)
```

### GENERATOR_ISSUE Resolution

```python
def fix_generator(property, counterexample):
    """
    Fix generator that produces invalid inputs.
    """
    value = counterexample.shrunk_value
    violation = find_constraint_violation(value, property.entity)

    if violation.type == "format":
        # Add format constraint
        return {
            "type": "add_format_filter",
            "generator": property.generators.valid,
            "filter": f"filter(lambda x: matches_format(x, '{violation.expected}'))"
        }

    elif violation.type == "range":
        # Adjust range bounds
        return {
            "type": "adjust_bounds",
            "generator": property.generators.valid,
            "min": violation.valid_min,
            "max": violation.valid_max
        }

    elif violation.type == "relationship":
        # Add relationship constraint
        return {
            "type": "add_relationship_filter",
            "generator": property.generators.valid,
            "constraint": violation.relationship_rule
        }

    return None
```

### SPEC_AMBIGUITY Resolution

```python
def flag_spec_ambiguity(property, counterexample):
    """
    Generate clarification question for spec ambiguity.
    """
    return {
        "type": "clarify_question",
        "property_id": property.id,
        "counterexample": counterexample.shrunk_value,
        "question": generate_clarify_question(property, counterexample),
        "interpretations": suggest_interpretations(property, counterexample),
        "affects_artifacts": property.source.artifacts,
        "block_until_resolved": True
    }

def generate_clarify_question(property, counterexample):
    """
    Generate a specific clarification question.
    """
    template = """
    Property {property_id} failed for input: {value}

    The specification doesn't clearly define behavior for this case.

    Question: {question}

    Possible interpretations:
    {interpretations}

    Please clarify which interpretation is correct, or provide the expected behavior.
    """

    return template.format(
        property_id=property.id,
        value=counterexample.shrunk_value,
        question=infer_question(property, counterexample),
        interpretations="\n".join(suggest_interpretations(property, counterexample))
    )
```

### IMPLEMENTATION_BUG Resolution

```python
def flag_implementation_bug(property, counterexample):
    """
    Flag implementation bug - blocks further PGS iterations.
    """
    return {
        "type": "implementation_bug",
        "property_id": property.id,
        "counterexample": counterexample.shrunk_value,
        "expected": property.expected_behavior(counterexample.shrunk_value),
        "actual": counterexample.actual_result,
        "suggested_fix": suggest_implementation_fix(property, counterexample),
        "trace": property.source.artifacts,
        "severity": "CRITICAL",
        "block_pgs": True,
        "action_required": "Fix implementation before continuing PGS"
    }
```

---

## Anti-Deception Mechanism

### Deception Patterns

| Pattern | Description | Detection | Action |
|---------|-------------|-----------|--------|
| **Oscillation** | Property changes A→B→A | Track formula history | Escalate |
| **Persistent** | Same counterexample repeats | Track shrunk values | Different strategy |
| **Stagnation** | No coverage improvement | Track coverage metrics | Suggest new approach |
| **Conflict** | Agents disagree | Compare agent outputs | Arbitration |

### Detection Algorithm

```python
def detect_deception(iteration_history):
    """
    Detect deception patterns in PGS iteration history.
    """
    deceptions = []

    # Pattern 1: Property oscillation
    for prop_id in get_all_property_ids(iteration_history):
        formulas = get_formula_history(prop_id, iteration_history)
        if has_oscillation(formulas):
            deceptions.append(Deception(
                type="OSCILLATION",
                severity="HIGH",
                property_id=prop_id,
                pattern=formulas,
                message=f"Property {prop_id} oscillating: {formulas}"
            ))

    # Pattern 2: Persistent counterexample
    counterexample_counts = count_counterexamples(iteration_history)
    for value, count in counterexample_counts.items():
        if count >= 2:
            deceptions.append(Deception(
                type="PERSISTENT_COUNTEREXAMPLE",
                severity="MEDIUM",
                value=value,
                count=count,
                message=f"Counterexample {value} persists across {count} iterations"
            ))

    # Pattern 3: Coverage stagnation
    coverage_history = get_coverage_history(iteration_history)
    if len(coverage_history) >= 3:
        recent = coverage_history[-3:]
        if all(c == recent[0] for c in recent):
            deceptions.append(Deception(
                type="STAGNATION",
                severity="MEDIUM",
                coverage=recent[0],
                iterations=3,
                message=f"Coverage stagnant at {recent[0]}% for 3 iterations"
            ))

    # Pattern 4: Agent conflict
    for iteration in iteration_history:
        conflicts = find_agent_conflicts(iteration)
        for conflict in conflicts:
            deceptions.append(Deception(
                type="AGENT_CONFLICT",
                severity="HIGH",
                agents=conflict.agents,
                property_id=conflict.property_id,
                message=f"Agents {conflict.agents} disagree on {conflict.property_id}"
            ))

    return DeceptionResult(
        detected=len(deceptions) > 0,
        deceptions=deceptions,
        should_escalate=any(d.severity == "HIGH" for d in deceptions)
    )

def has_oscillation(formulas):
    """
    Check if formula sequence shows A→B→A pattern.
    """
    if len(formulas) < 3:
        return False

    for i in range(len(formulas) - 2):
        if formulas[i] == formulas[i + 2] and formulas[i] != formulas[i + 1]:
            return True

    return False
```

### Escalation Protocol

```python
def handle_deception(deception):
    """
    Handle detected deception pattern.
    """
    if deception.type == "OSCILLATION":
        return {
            "action": "ESCALATE_TO_HUMAN",
            "message": f"Property {deception.property_id} is oscillating. Manual review required.",
            "options": [
                "Choose one of the alternating formulas",
                "Rewrite property from scratch",
                "Mark spec as ambiguous and run /speckit.clarify"
            ]
        }

    elif deception.type == "PERSISTENT_COUNTEREXAMPLE":
        return {
            "action": "TRY_ALTERNATIVE",
            "message": f"Counterexample {deception.value} persists. Trying alternative resolution.",
            "alternative_strategies": [
                "Split property into multiple specific cases",
                "Reclassify as SPEC_AMBIGUITY",
                "Add explicit edge case to spec"
            ]
        }

    elif deception.type == "STAGNATION":
        return {
            "action": "SUGGEST_NEW_APPROACH",
            "message": f"Coverage stagnant at {deception.coverage}%.",
            "suggestions": [
                "Add different property types (model-based, commutative)",
                "Review uncovered requirements manually",
                "Consider if remaining requirements are untestable"
            ]
        }

    elif deception.type == "AGENT_CONFLICT":
        return {
            "action": "REQUEST_ARBITRATION",
            "message": f"Agents disagree on {deception.property_id}.",
            "conflicting_outputs": deception.agents,
            "arbitration_options": [
                "Use most conservative interpretation",
                "Escalate to human",
                "Run both versions and compare"
            ]
        }
```

---

## Quality Metrics

### PGS-Specific Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Iterations to Success** | Number of iterations to resolve all | < 5 |
| **Resolution Rate** | % of counterexamples resolved per iteration | > 50% |
| **Deception Rate** | % of iterations with deception detected | < 10% |
| **Escalation Rate** | % of runs requiring human intervention | < 5% |
| **Coverage Delta** | Coverage improvement per iteration | > 5% |

### Success Criteria

```yaml
pgs_success_criteria:
  excellent:
    iterations: <= 2
    resolution_rate: >= 80%
    final_coverage: >= 95%
    deception_rate: 0%

  good:
    iterations: <= 4
    resolution_rate: >= 60%
    final_coverage: >= 85%
    deception_rate: < 10%

  acceptable:
    iterations: <= 5
    resolution_rate: >= 50%
    final_coverage: >= 80%
    deception_rate: < 20%

  needs_improvement:
    iterations: > 5
    resolution_rate: < 50%
    final_coverage: < 80%
    action: "Review spec and properties manually"
```

---

## Integration with Spec-Kit

### Entry Point

```bash
/speckit.properties --profile pgs --iterations 5
```

### Output Artifacts

1. **properties.md** - Updated with refined properties
2. **pgs-report.md** - PGS iteration details
3. **clarify-questions.md** - Questions for /speckit.clarify
4. **implementation-bugs.md** - Flagged bugs for developers

### Handoff to Other Commands

```yaml
handoffs:
  - condition: "SPEC_AMBIGUITY found"
    target: speckit.clarify
    payload: "clarify-questions.md"

  - condition: "IMPLEMENTATION_BUG found"
    target: speckit.implement
    payload: "implementation-bugs.md"
    block: true

  - condition: "SUCCESS"
    target: speckit.implement
    payload: "properties.md"
```

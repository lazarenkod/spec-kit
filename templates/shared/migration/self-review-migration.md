# Self-Review Criteria: Migration Plans (SR-MIG)

Reference: `templates/shared/self-review/framework.md`

## Criteria Table

| ID | Criterion | Severity | Check |
|----|-----------|----------|-------|
| SR-MIG-01 | All modules analyzed for coupling | CRITICAL | Coupling analysis covers all src directories |
| SR-MIG-02 | Each phase has rollback plan | CRITICAL | Every MIG-xxx includes rollback steps |
| SR-MIG-03 | Risk mitigation for HIGH/CRITICAL risks | CRITICAL | All L×I >= 12 risks have mitigations |
| SR-MIG-04 | Success metrics defined | HIGH | Each phase has measurable success criteria |
| SR-MIG-05 | Duration estimates present | HIGH | All phases have time estimates |
| SR-MIG-06 | Dependencies mapped | HIGH | External dependencies verified |
| SR-MIG-07 | Mermaid diagram valid | MEDIUM | Diagram renders correctly |
| SR-MIG-08 | Phase sequencing correct | HIGH | Dependencies respected in phase order |
| SR-MIG-09 | No circular dependencies | CRITICAL | Migration phases don't create cycles |
| SR-MIG-10 | Data migration addressed | HIGH | Data migration strategy for stateful services |
| SR-MIG-11 | Compatibility checks done | HIGH | Breaking changes identified and addressed |
| SR-MIG-12 | Cost estimation present | MEDIUM | Cost comparison for cloud migrations |
| SR-MIG-13 | Timeline realistic | MEDIUM | Total duration within reasonable bounds |
| SR-MIG-14 | Validation plan exists | HIGH | Each phase has validation criteria |
| SR-MIG-15 | No placeholders | HIGH | No TODO, TBD, or [NEEDS RESEARCH] markers |

## Severity Levels

```text
SEVERITY_LEVELS = {
  CRITICAL: { weight: 10, auto_fail: true },
  HIGH:     { weight: 5,  warn_threshold: 2 },
  MEDIUM:   { weight: 2,  warn_threshold: 4 },
  LOW:      { weight: 1 }
}
```

## Verdict Logic

```text
CALCULATE_VERDICT(results):
  critical_fails = count(WHERE severity = CRITICAL AND status = FAIL)
  high_fails = count(WHERE severity = HIGH AND status = FAIL)
  medium_fails = count(WHERE severity = MEDIUM AND status = FAIL)

  IF critical_fails > 0:
    RETURN FAIL, "CRITICAL issues must be resolved"
  ELIF high_fails >= 2:
    RETURN WARN, "{high_fails} HIGH severity issues"
  ELIF medium_fails >= 4:
    RETURN WARN, "{medium_fails} MEDIUM severity issues"
  ELSE:
    score = 100 * (1 - failed_weight / total_weight)
    IF score >= 80: RETURN PASS
    ELSE: RETURN WARN
```

## Self-Correction Loop

```text
MAX_ITERATIONS = 3

FOR iteration IN 1..MAX_ITERATIONS:
  results = RUN_CHECKS(migration_plan, SR-MIG-01..15)
  verdict = CALCULATE_VERDICT(results)

  IF verdict == PASS:
    OUTPUT "Self-Review PASSED (iteration {iteration}/3)"
    BREAK
  ELIF iteration < MAX_ITERATIONS:
    fixable = filter(results, auto_fixable = true AND status = FAIL)
    APPLY_FIXES(migration_plan, fixable)
  ELSE:
    IF verdict == FAIL:
      OUTPUT "Self-Review FAILED after 3 iterations"
      ASK_USER "Proceed anyway? (Not recommended)"
    ELSE:
      OUTPUT "Self-Review completed with warnings"
```

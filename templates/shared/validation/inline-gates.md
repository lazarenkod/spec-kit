# Inline Quality Gates Framework

## Purpose

Enable quality gate validation directly within commands, eliminating the need to invoke `/speckit.analyze` for routine checks. Gates run automatically before handoffs, catching issues early with minimal latency.

## Why Inline Gates?

| External Analyze Call | Inline Gates |
|----------------------|--------------|
| ~10-30s latency | ~1-5s latency |
| Full profile execution | Targeted simplified checks |
| External tool invocation | Inline execution |
| Full findings report | Pass/fail with counts |
| Complex async flow | Simple synchronous flow |

## Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                    COMMAND EXECUTION FLOW                        │
├────────────────┬───────────────┬───────────────┬────────────────┤
│   Generate     │   Self-Review │   Inline      │   Handoff      │
│   Artifact     │   Checkpoint  │   Gates       │   Transition   │
│                │               │               │                │
│  spec.md       │  SR-SPEC-*    │  IG-SPEC-*    │  → /plan       │
│                │  (streaming)  │  (blocking)   │                │
└────────────────┴───────────────┴───────────────┴────────────────┘

INLINE GATES run AFTER artifact is complete, BEFORE handoff.
They validate cross-artifact consistency and quality thresholds.
```

## Inline Gate Definition Format

```yaml
inline_gates:
  enabled: true
  skip_flag: "--skip-gates"        # CLI flag to bypass all gates
  strict_flag: "--strict-gates"    # CLI flag to treat warnings as errors
  full_flag: "--full-gates"        # CLI flag for full pass instead of simplified
  mode: progressive                # progressive | strict | fast
  on_failure: block                # block | warn | continue
  gates:
    - id: IG-{CMD}-{NNN}           # Unique gate identifier
      name: "Human-readable name"   # Display name
      pass: A-Z                     # Reference to analyze.md pass (optional)
      checks: [SR-xxx-yy, ...]      # Self-review criteria (optional)
      ref: QG-xxx                   # Reference to quality gate ID (optional)
      tier: 1 | 2 | 3               # Validation tier (1=blocking, 2=errors block, 3=warn)
      threshold: number             # Acceptable count/score threshold
      severity: CRITICAL | HIGH | MEDIUM | LOW
      message: "Failure message"    # Displayed when gate fails
      auto_fix: command | false     # Command to auto-remediate (optional)
```

## Gate Severity Behavior

| Severity | Default Behavior | With `--strict-gates` |
|----------|-----------------|----------------------|
| CRITICAL | Block handoff | Block handoff |
| HIGH | Warn, allow continue | Block handoff |
| MEDIUM | Warn, continue | Warn, allow continue |
| LOW | Log, continue | Warn, continue |

## Execution Algorithm

```text
EXECUTE_INLINE_GATES(artifact, gates_config, cli_flags):

  # Check skip flag
  IF "--skip-gates" IN cli_flags:
    OUTPUT "⏭️ Inline gates skipped (--skip-gates)"
    RETURN {status: "SKIPPED", gates: []}

  gates = gates_config.gates
  results = []
  blocked = false
  strict_mode = "--strict-gates" IN cli_flags
  full_mode = "--full-gates" IN cli_flags

  OUTPUT "### Inline Quality Gates"
  OUTPUT ""

  # Execute each gate
  FOR gate IN gates:

    # Run check (simplified or full)
    IF full_mode AND gate.pass:
      result = RUN_FULL_PASS(gate.pass, artifact)
    ELIF gate.pass:
      result = RUN_SIMPLIFIED_CHECK(gate.pass, artifact)
    ELIF gate.checks:
      result = RUN_CRITERIA_CHECK(gate.checks, artifact)
    ELIF gate.ref:
      result = RUN_QUALITY_GATE_CHECK(gate.ref, artifact)

    # Determine status based on threshold
    IF result.count <= gate.threshold:
      result.status = "PASS"
    ELIF gate.severity == "CRITICAL":
      result.status = "FAIL"
      blocked = true
    ELIF gate.severity == "HIGH" AND strict_mode:
      result.status = "FAIL"
      blocked = true
    ELIF gate.severity == "HIGH":
      result.status = "WARN"
    ELIF gate.severity == "MEDIUM":
      result.status = "WARN"
    ELSE:
      result.status = "INFO"

    results.push({gate: gate, result: result})

    # Early exit on CRITICAL failure
    IF result.status == "FAIL" AND gate.severity == "CRITICAL":
      OUTPUT_GATE_TABLE(results)
      OUTPUT_FAILURE_DETAILS(gate, result)
      RETURN {status: "BLOCKED", gate: gate.id, results: results}

  # Output results table
  OUTPUT_GATE_TABLE(results)

  # Determine overall verdict
  fail_count = COUNT(results WHERE status == "FAIL")
  warn_count = COUNT(results WHERE status == "WARN")
  pass_count = COUNT(results WHERE status == "PASS")

  IF blocked OR fail_count > 0:
    OUTPUT ""
    OUTPUT "**Result**: BLOCKED"
    OUTPUT ""
    OUTPUT "Fix issues before proceeding:"
    FOR r IN results WHERE r.result.status == "FAIL":
      OUTPUT "- {r.gate.id}: {r.gate.message}"
      IF r.result.details:
        OUTPUT "  {r.result.details}"
      IF r.gate.auto_fix:
        OUTPUT "  Auto-fix: Run `{r.gate.auto_fix}`"
    OUTPUT ""
    OUTPUT "Use `--skip-gates` to bypass (not recommended)."

    RETURN {status: "BLOCKED", results: results}

  ELIF warn_count > 0:
    OUTPUT ""
    OUTPUT "**Result**: PASS with {warn_count} warning(s)"
    OUTPUT ""
    OUTPUT "Proceeding to handoff..."

    RETURN {status: "WARN", results: results}

  ELSE:
    OUTPUT ""
    OUTPUT "**Result**: PASS ({pass_count}/{pass_count} gates passed)"
    OUTPUT ""
    OUTPUT "Proceeding to handoff..."

    RETURN {status: "PASS", results: results}
```

## Output Format

### Gate Results Table

```text
| Gate | Status | Details |
|------|--------|---------|
| IG-SPEC-001: Constitution Alignment | PASS | 0 violations |
| IG-SPEC-002: Ambiguity Detection | WARN | 3 vague terms (threshold: 5) |
| IG-SPEC-003: FR-AS Coverage | PASS | 100% coverage |
| IG-SPEC-004: Implementation Details | PASS | 0 leaks detected |

**Result**: PASS with 1 warning(s)

Proceeding to handoff...
```

### Blocked Output

```text
| Gate | Status | Details |
|------|--------|---------|
| IG-SPEC-001: Constitution Alignment | FAIL | 2 violations |
| IG-SPEC-002: Ambiguity Detection | - | (skipped - prior failure) |

**Result**: BLOCKED

Fix issues before proceeding:
- IG-SPEC-001: Spec violates project constitution
  FR-003 conflicts with SEC-001: "Must not store plaintext passwords"
  FR-005 conflicts with QUA-001: "Must have 80%+ test coverage"

Use `--skip-gates` to bypass (not recommended).
```

## Command-Specific Gates

### /speckit.specify

```yaml
inline_gates:
  enabled: true
  skip_flag: "--skip-gates"
  strict_flag: "--strict-gates"
  mode: progressive
  on_failure: block
  gates:
    - id: IG-SPEC-001
      name: "Constitution Alignment"
      pass: D
      tier: 2
      threshold: 0
      severity: CRITICAL
      message: "Spec violates project constitution"
    - id: IG-SPEC-002
      name: "Ambiguity Detection"
      pass: B
      tier: 2
      threshold: 5
      severity: HIGH
      message: "Too many vague terms without measurable criteria"
      auto_fix: speckit.clarify
    - id: IG-SPEC-003
      name: "FR-AS Coverage"
      checks: [SR-SPEC-03, SR-SPEC-04]
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Functional requirements missing acceptance scenarios"
    - id: IG-SPEC-004
      name: "Implementation Details"
      checks: [SR-SPEC-02]
      tier: 2
      threshold: 0
      severity: MEDIUM
      message: "Spec contains implementation details (should be in plan)"
```

### /speckit.plan

```yaml
inline_gates:
  enabled: true
  skip_flag: "--skip-gates"
  strict_flag: "--strict-gates"
  mode: progressive
  on_failure: block
  gates:
    - id: IG-PLAN-001
      name: "Constitution Alignment"
      pass: D
      tier: 2
      threshold: 0
      severity: CRITICAL
      message: "Plan violates project constitution"
    - id: IG-PLAN-002
      name: "Tech Consistency"
      pass: F
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Terminology inconsistent between spec and plan"
    - id: IG-PLAN-003
      name: "Spec Alignment"
      checks: [SR-PLAN-07]
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Plan references undefined spec elements"
    - id: IG-PLAN-004
      name: "Dependencies Verified"
      checks: [SR-PLAN-03, SR-PLAN-04]
      tier: 2
      threshold: 0
      severity: MEDIUM
      message: "External dependencies not verified"
```

### /speckit.tasks

```yaml
inline_gates:
  enabled: true
  skip_flag: "--skip-gates"
  strict_flag: "--strict-gates"
  mode: progressive
  on_failure: block
  gates:
    - id: IG-TASK-001
      name: "Dependency Graph Valid"
      pass: G
      tier: 1
      threshold: 0
      severity: CRITICAL
      message: "Circular dependencies detected in task graph"
    - id: IG-TASK-002
      name: "FR Coverage"
      pass: H
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Functional requirements without implementation tasks"
    - id: IG-TASK-003
      name: "RTM Validity"
      pass: J
      tier: 2
      threshold: 0
      severity: MEDIUM
      message: "Requirements Traceability Matrix inconsistent"
    - id: IG-TASK-004
      name: "Test Coverage"
      ref: QG-TEST-001
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Acceptance scenarios missing test tasks"
```

### /speckit.implement

```yaml
inline_gates:
  enabled: true
  skip_flag: "--skip-gates"
  strict_flag: "--strict-gates"
  mode: progressive
  on_failure: block

  # Pre-implementation gates (run before Wave 1)
  pre_gates:
    - id: IG-IMPL-001
      name: "Staging Ready"
      ref: QG-STAGING-001
      tier: 1
      threshold: 0
      severity: CRITICAL
      message: "Staging environment not healthy"
    - id: IG-IMPL-002
      name: "SQS Threshold"
      ref: QG-001
      tier: 3
      threshold: 80
      severity: CRITICAL
      message: "SQS below 80 threshold - improve spec quality first"

  # Post-implementation gates (run after Wave 4)
  post_gates:
    - id: IG-IMPL-101
      name: "Build Success"
      pass: R
      tier: 1
      threshold: 0
      severity: CRITICAL
      message: "Build failed"
    - id: IG-IMPL-102
      name: "Tests Pass"
      pass: S
      tier: 2
      threshold: 0
      severity: CRITICAL
      message: "Tests failing"
    - id: IG-IMPL-103
      name: "Coverage Threshold"
      pass: T
      ref: QG-004
      tier: 2
      threshold: 80
      severity: HIGH
      message: "Test coverage below 80%"
    - id: IG-IMPL-104
      name: "Lint Clean"
      pass: U
      ref: QG-006
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Lint errors present"
```

## Integration with Checkpoints

Inline gates complement streaming checkpoints:

```text
ARTIFACT LIFECYCLE:

  GENERATE                   VALIDATE                    TRANSITION
  ────────                   ────────                    ──────────
  Section 1
     │
     ▼ CP-*-01 (streaming)
  Section 2
     │
     ▼ CP-*-02 (streaming)
     ...
  Section N
     │
     ▼ CP-*-Final
                             INLINE GATES (blocking)
                             IG-*-001...004
                                                        → HANDOFF
```

**Checkpoints**: Catch issues during generation (streaming, non-blocking)
**Inline Gates**: Validate before handoff (synchronous, blocking)

## Integration with Self-Review

Inline gates can reference self-review criteria:

```yaml
gates:
  - id: IG-SPEC-003
    name: "FR-AS Coverage"
    checks: [SR-SPEC-03, SR-SPEC-04]  # Uses self-review check functions
    tier: 2
    threshold: 0
    severity: HIGH
```

The check function returns:
- `count`: Number of issues found
- `details`: Human-readable description
- `locations`: Specific artifact locations with issues

## Performance Expectations

| Mode | Latency | Use Case |
|------|---------|----------|
| Fast (simplified) | 1-5s | Default for all commands |
| Full (--full-gates) | 10-30s | Thorough validation before milestone |
| Skip (--skip-gates) | 0s | Development/debugging only |

## CLI Flag Reference

| Flag | Effect |
|------|--------|
| `--skip-gates` | Bypass all inline gates (not recommended) |
| `--strict-gates` | Treat HIGH severity as blocking (same as CRITICAL) |
| `--full-gates` | Run full pass instead of simplified check |

## When to Use /speckit.analyze Instead

Inline gates handle routine validation. Use `/speckit.analyze` for:

- **Full Audit**: Comprehensive pre-milestone analysis (`--profile full`)
- **QA Verification**: Post-implementation quality assurance (`--profile qa`)
- **Quality Dashboard**: Unified metrics view (`--profile quality_dashboard`)
- **Troubleshooting**: Investigating specific quality issues
- **Reports**: Generating detailed findings for stakeholders

```text
WORKFLOW RECOMMENDATION:

  /speckit.specify ──[IG-SPEC-*]──► /speckit.plan ──[IG-PLAN-*]──►
  /speckit.tasks ──[IG-TASK-*]──► /speckit.implement ──[IG-IMPL-*]──►

  MILESTONE? ──► /speckit.analyze --profile full (comprehensive audit)

  POST-IMPL? ──► /speckit.analyze --profile qa (QA verification)
```

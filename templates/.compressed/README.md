# Compressed Context Templates - Reference System

## Overview

This directory contains the reference notation system for compressed command templates (`.COMPRESSED.md` variants). References reduce token usage by 60% while maintaining semantic equivalence with full templates.

## Reference Notation

Compressed templates use `[REF:XXX-NNN]` notation to reference shared patterns:

| Reference | Description | Source |
|-----------|-------------|--------|
| `[REF:INIT-001]` | Standard initialization (language, complexity, brownfield) | `refs/init-modules.yaml` |
| `[REF:SR-001]` | Self-Review Framework (3 iterations, verdict logic) | `refs/self-review.yaml` |
| `[REF:VG-001]` | Validation Gate: SRS threshold | `refs/validation-gates.yaml` |
| `[REF:VG-002]` | Validation Gate: CQS threshold | `refs/validation-gates.yaml` |
| `[REF:VG-003]` | Validation Gate: Checklist complete | `refs/validation-gates.yaml` |
| `[REF:QI-001]` | Quality imports (anti-slop + reader-testing) | `refs/quality-checks.yaml` |
| `[REF:AS-001]` | Anti-Slop checks | `refs/quality-checks.yaml` |
| `[REF:CP-001]` | Checkpoint execution algorithm | `refs/checkpoints.yaml` |

## How References Work

When an AI agent encounters `[REF:XXX-NNN]`, it should:

1. **Recognize** the reference as a pointer to a defined pattern
2. **Expand** by loading the corresponding YAML definition from `refs/`
3. **Apply** the pattern logic as if it were inline

### Example Expansion

Template contains:
```markdown
## Init [REF:INIT-001]
→ ARTIFACT_LANGUAGE, COMPLEXITY_TIER, BROWNFIELD_MODE
```

Agent expands to execute:
1. Read `/memory/constitution.md` → extract language setting
2. Run complexity scoring algorithm → COMPLEXITY_TIER, COMPLEXITY_SCORE
3. Run brownfield detection → BROWNFIELD_MODE, BROWNFIELD_CONFIDENCE

## File Structure

```
.compressed/
├── README.md                    # This file
└── refs/
    ├── init-modules.yaml        # Initialization patterns
    ├── self-review.yaml         # Self-review framework
    ├── validation-gates.yaml    # Quality gates
    ├── quality-checks.yaml      # Anti-slop, reader-testing
    └── output-schemas.yaml      # Common output structures
```

## Token Savings

| Component | Full Template | Compressed | Savings |
|-----------|---------------|------------|---------|
| Init modules | ~500 lines | 3 lines + ref | 95% |
| Self-review | ~100 lines | 5 lines + ref | 95% |
| Validation gates | ~50 lines | 2 lines + ref | 96% |
| Examples | ~200 lines | 0 (removed) | 100% |
| **Total per template** | ~1,000 lines | ~350 lines | 65% |

## Usage

Compressed templates are selected via:
- `--fast` flag in CLI commands
- Direct reference to `.COMPRESSED.md` files

## Compatibility

- Full templates (`.md`) remain the default for maximum clarity
- Compressed templates (`.COMPRESSED.md`) are semantically equivalent
- Both produce identical artifact outputs
- Quality scores (SRS, CQS, DQS) should not regress

# Spec Kit Excellence: Quick Reference Guide

> **5-минутные чек-листы для world-class качества**

---

## /speckit.specify - Specification Excellence

### Pre-Generation Checklist
- [ ] User pain point quantified ($ lost, time wasted, NPS impact)
- [ ] Business metrics defined (revenue, conversion, retention)
- [ ] Technical constraints documented
- [ ] Alternatives evaluated (at least 3)

### SQS Quick Score (Target: ≥80/100)

| Category | Points | Check |
|----------|--------|-------|
| **Clarity (25)** | | |
| SHALL/SHOULD/MAY used | 5 | [ ] |
| No vague terms ("fast", "easy") | 5 | [ ] |
| All numbers specific | 5 | [ ] |
| Success measurable | 5 | [ ] |
| Failures defined | 5 | [ ] |
| **Completeness (25)** | | |
| FRs documented | 5 | [ ] |
| NFRs specified | 5 | [ ] |
| Edge cases listed | 5 | [ ] |
| Dependencies mapped | 5 | [ ] |
| Security covered | 5 | [ ] |
| **Testability (25)** | | |
| Each FR has AC | 5 | [ ] |
| Scenarios concrete | 5 | [ ] |
| Performance metrics | 5 | [ ] |
| Error conditions | 5 | [ ] |
| Integration points | 5 | [ ] |
| **Traceability (15)** | | |
| Unique IDs | 3 | [ ] |
| Concept cross-refs | 3 | [ ] |
| Feature dependencies | 3 | [ ] |
| FR→AC→Test chain | 3 | [ ] |
| No orphans | 3 | [ ] |
| **No Ambiguity (10)** | | |
| No hedge words | 2 | [ ] |
| Terms defined | 2 | [ ] |
| Clarifications resolved | 2 | [ ] |
| Scope explicit | 2 | [ ] |
| Assumptions documented | 2 | [ ] |

**Total**: ___/100

### Anti-Patterns to Avoid

| ❌ Bad | ✅ Good |
|--------|---------|
| "System should be fast" | "API responds in <200ms p95" |
| "User-friendly interface" | "Task completion in ≤3 clicks" |
| "Secure authentication" | "OAuth 2.0 + MFA with AES-256" |
| "Handle errors gracefully" | "Retry 3x with exponential backoff, then show error #123" |
| "Scalable architecture" | "Horizontal scaling to 10K concurrent users" |

### Evidence Requirements (P0/P1 Features)

| Evidence Tier | Quality | Required For |
|---------------|---------|--------------|
| **Tier 1** | Primary research, direct measurements | All P0 |
| **Tier 2** | Industry benchmarks, studies | All P1 |
| **Tier 3** | Assumptions (FLAG!) | Needs validation |

---

## /speckit.plan - Planning Excellence

### Pre-Mortem Template (Mandatory)

```markdown
## Pre-Mortem: Why We Failed

**Scenario 1: Technical**
- Failed because: [specific failure]
- Warning signs: [what we ignored]
- Prevention: [concrete action]

**Scenario 2: Adoption**
- Failed because: [specific failure]
- Warning signs: [what we ignored]
- Prevention: [concrete action]

**Scenario 3: Business**
- Failed because: [specific failure]
- Warning signs: [what we ignored]
- Prevention: [concrete action]
```

### Brainstorm-Curate Template

```markdown
## Decision: [Name]

### Options
| Option | Pros | Cons |
|--------|------|------|
| A: [Name] | +... | -... |
| B: [Name] | +... | -... |
| C: [Name] | +... | -... |

### Evaluation (1-10)
| Criteria | Weight | A | B | C |
|----------|--------|---|---|---|
| User Value | 25% | _ | _ | _ |
| Feasibility | 25% | _ | _ | _ |
| Differentiation | 20% | _ | _ | _ |
| Cost | 15% | _ | _ | _ |
| Risk | 15% | _ | _ | _ |

**Decision**: [Option] because [reasoning]
```

### RACI Quick Check

| Rule | Check |
|------|-------|
| Every task has exactly 1 Accountable | [ ] |
| Responsible assigned to all tasks | [ ] |
| Consulted are actually needed | [ ] |
| Informed list is complete | [ ] |

### Plan Completeness

- [ ] All [NEEDS CLARIFICATION] resolved
- [ ] Technical Context 100% filled (no placeholders)
- [ ] Dependencies verified with documentation links
- [ ] Phases have clear success criteria
- [ ] Pre-Mortem completed
- [ ] Major decisions have Brainstorm-Curate

---

## /speckit.tasks - Task Excellence

### INVEST Compliance (Every Task)

| Criteria | Question | Check |
|----------|----------|-------|
| **I**ndependent | Can start without other tasks? | [ ] |
| **N**egotiable | Can adjust details during impl? | [ ] |
| **V**aluable | Delivers measurable value? | [ ] |
| **E**stimable | Can estimate effort? | [ ] |
| **S**mall | Completable in 1-3 days? | [ ] |
| **T**estable | Has clear acceptance criteria? | [ ] |

### Effort Estimation Guide

| Size | Hours | Complexity | When to Use |
|------|-------|------------|-------------|
| XS | 1-2h | Trivial | Config, copy changes |
| S | 2-4h | Simple | Single function, basic endpoint |
| M | 4-8h | Moderate | New component, integration |
| L | 8-16h | Complex | New service, major refactor |
| XL | 16-32h | Very complex | Architecture change |
| XXL | 32h+ | Epic | **SPLIT THIS TASK!** |

### Epic Splitting Patterns

1. **Workflow Steps**: Split by user journey stage
2. **Business Rules**: Split by scenario/variation
3. **Simple → Complex**: Hardcoded → Configurable → Dynamic
4. **CRUD**: Create, Read, Update, Delete separately
5. **Layers**: DB → API → UI → Tests
6. **Data**: By field type (text, date, file)
7. **Spike + Impl**: Research then build
8. **Core + Hardening**: Function → Errors → Logging

### Definition of Done Templates

**Implementation Task**:
- [ ] Code written, self-reviewed
- [ ] Tests ≥80% coverage
- [ ] Lint/type checks pass
- [ ] @speckit annotations added
- [ ] PR approved, merged

**Test Task**:
- [ ] Scenario implemented
- [ ] Passes consistently (not flaky)
- [ ] Edge cases covered

**Design Task**:
- [ ] Peer reviewed
- [ ] Handoff complete
- [ ] Tokens exported

---

## /speckit.implement - Quality Gates

### Profile Selection

| Profile | Use When | Gates |
|---------|----------|-------|
| **MVP** | Early stage, fast iteration | Test 60%, Type 80%, Lint 0 critical |
| **Standard** | Production features | Test 80%, Type 95%, Lint 0, A11y A |
| **Strict** | Enterprise, regulated | Test 90%, Type 99%, Lint 0, A11y AA |

### Traceability Verification

- [ ] Every FR has implementation task
- [ ] Every testable AS has test task
- [ ] Every source file has @speckit annotation
- [ ] All referenced IDs exist in spec

### Rollout Phases

| Phase | Audience | Duration | Rollback Trigger |
|-------|----------|----------|------------------|
| Internal | 0.1% | 3 days | Error >1% |
| Beta | 5% | 4 days | NPS drop >10 |
| Limited | 25% | 7 days | Ticket spike 3x |
| Full GA | 100% | Ongoing | Incident process |

---

## /speckit.design - Design Excellence

### Component Spec Must-Haves

| Section | Required For | Check |
|---------|--------------|-------|
| Purpose | All | [ ] |
| Anatomy diagram | Complex components | [ ] |
| Variants | All with variations | [ ] |
| All 7 states | Interactive components | [ ] |
| Sizes | Scalable components | [ ] |
| Spacing rules | All | [ ] |
| Motion specs | Animated components | [ ] |
| Responsive | Adaptive components | [ ] |
| Accessibility | All | [ ] |
| Code reference | All | [ ] |

### Component States Checklist

- [ ] Default
- [ ] Hover
- [ ] Focus (keyboard)
- [ ] Active/Pressed
- [ ] Disabled
- [ ] Loading
- [ ] Error

### Motion Design Tokens

| Purpose | Duration | Easing |
|---------|----------|--------|
| Micro-interaction | 100ms | ease-out |
| Standard transition | 200ms | ease-in-out |
| Complex animation | 300-500ms | ease-out |
| Continuous | ∞ | linear |

### Handoff Checklist

- [ ] Figma components named correctly
- [ ] Auto-layout applied
- [ ] Dev mode annotations complete
- [ ] Design tokens exported (colors, typography, spacing)
- [ ] Icons exported as SVG
- [ ] Storybook stories created
- [ ] Accessibility requirements documented

---

## Universal Quality Checks

### Anti-Slop Scanner

Search for and replace:

| Find | Replace With |
|------|--------------|
| "fast" | "[specific time: <Xms]" |
| "secure" | "[specific standard: OWASP Top 10]" |
| "scalable" | "[specific capacity: X users]" |
| "might", "may", "could" | "[definitive statement]" |
| "best practices" | "[name the specific practice]" |
| "user-friendly" | "[specific UX metric]" |
| "robust" | "[specific failure scenarios]" |

### Quality Dashboard Template

```markdown
## Quality Status

| Phase | Score | Target | Status |
|-------|-------|--------|--------|
| Spec (SQS) | __/100 | ≥80 | [ ] |
| Plan Complete | __% | ≥90% | [ ] |
| Tasks INVEST | __% | ≥95% | [ ] |
| Impl Gates | __/__ | All pass | [ ] |
| Design Ready | __% | ≥85% | [ ] |

**Overall**: [Ready / Needs Work / Blocked]
```

---

## Quick Commands

```bash
# Run full quality check
/speckit.analyze --profile quality_gates

# Check specific phase
/speckit.analyze --profile spec_validate
/speckit.analyze --profile plan_validate
/speckit.analyze --profile tasks_validate

# Generate SQS score
/speckit.analyze --profile sqs
```

---

## Red Flags to Escalate

| Signal | Action |
|--------|--------|
| SQS < 60 | Block implementation, major rework |
| >5 [NEEDS CLARIFICATION] | Run /speckit.clarify first |
| No Pre-Mortem | Block planning sign-off |
| XXL tasks | Force split before approval |
| Tier 3 evidence on P0 | Validate before development |
| Missing DoD | Define before task start |
| No rollout plan | Block release approval |

---

*Quick Reference v1.0 | 2026-01-03*

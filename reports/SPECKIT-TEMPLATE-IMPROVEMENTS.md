# Spec Kit Template Improvements

> **Конкретные изменения для внедрения в шаблоны**

---

## 1. spec-template.md Improvements

### Добавить секцию SQS Checklist

```markdown
<!-- ADD AFTER FEATURE METADATA -->

## Specification Quality Score (SQS)

### Pre-Handoff Quality Gate

| Category | Score | Max |
|----------|-------|-----|
| Requirements Clarity | __ | 25 |
| Completeness | __ | 25 |
| Testability | __ | 25 |
| Traceability | __ | 15 |
| Ambiguity Absence | __ | 10 |
| **Total** | __ | **100** |

**Threshold**: ≥80 for production features
**Status**: [ ] Pass / [ ] Needs Revision
```

### Добавить секцию Evidence Tracking

```markdown
<!-- ADD AFTER USER SCENARIOS -->

## Evidence Tracking

| Requirement ID | Claim | Evidence Source | Tier | Status |
|----------------|-------|-----------------|------|--------|
| FR-001 | [claim] | [source/link] | T1/T2/T3 | ✅/⚠️ |
| FR-002 | [claim] | [source/link] | T1/T2/T3 | ✅/⚠️ |

### Evidence Tier Legend
- **T1**: Primary research, direct measurements (required for P0)
- **T2**: Industry benchmarks, peer-reviewed studies (acceptable for P1)
- **T3**: Assumptions, analogies (flag for validation before implementation)

### Weak Evidence Actions
<!-- List T3 items that need validation before development -->
```

### Добавить секцию Success Metrics

```markdown
<!-- ADD AFTER PROBLEM STATEMENT -->

## Success Metrics

### North Star Impact
- **Primary NSM**: [metric name]
- **Baseline**: [current value]
- **Target**: [expected value after launch]
- **Measurement**: [how we'll track]

### AARRR Funnel Impact
| Stage | Metric | Current | Target | How Feature Helps |
|-------|--------|---------|--------|-------------------|
| Acquisition | [metric] | X% | Y% | [description] |
| Activation | [metric] | X% | Y% | [description] |
| Retention | [metric] | X% | Y% | [description] |
| Referral | [metric] | X% | Y% | [description] |
| Revenue | [metric] | $X | $Y | [description] |

### Guardrail Metrics
<!-- Metrics that should NOT degrade -->
- [Metric 1]: Must remain above [threshold]
- [Metric 2]: Must remain above [threshold]
```

### Добавить секцию Experimentation

```markdown
<!-- ADD AT END OF SPEC -->

## Experimentation Plan

### Hypothesis
**If** we [change/add feature],
**then** [metric] will [increase/decrease] by [X%],
**because** [reasoning based on evidence].

### Test Design
- **Primary Metric**: [specific metric]
- **Secondary Metrics**: [list]
- **Counter Metrics**: [what could go wrong]
- **Sample Size**: [calculated for 95% confidence, 80% power]
- **Duration**: [minimum X weeks]

### Success Criteria
- [ ] p < 0.05 (statistical significance)
- [ ] Practical significance > [X%]
- [ ] No degradation in counter metrics

### Rollout Plan
| Phase | Audience | Duration | Go/No-Go |
|-------|----------|----------|----------|
| Internal | 0.1% | 3 days | Error rate <1% |
| Beta | 5% | 7 days | NPS stable |
| Limited | 25% | 7 days | Metrics improved |
| Full | 100% | - | All gates pass |
```

---

## 2. plan-template.md Improvements

### Добавить секцию Pre-Mortem

```markdown
<!-- ADD AFTER SUMMARY -->

## Pre-Mortem Analysis

> "Imagine it's 6 months from now. The feature launch failed completely. What happened?"

### Failure Scenario 1: Technical Failure
- **What went wrong**: [specific technical failure]
- **Warning signs we missed**: [early indicators we ignored]
- **Prevention measures**: [concrete actions to add to plan]
- **Owner**: [who monitors this risk]

### Failure Scenario 2: User Adoption Failure
- **What went wrong**: [why users didn't adopt]
- **Warning signs we missed**: [user feedback we ignored]
- **Prevention measures**: [validation steps to add]
- **Owner**: [who monitors this risk]

### Failure Scenario 3: Business Impact Failure
- **What went wrong**: [negative business outcome]
- **Warning signs we missed**: [business signals we ignored]
- **Prevention measures**: [business validation steps]
- **Owner**: [who monitors this risk]

### Risk Mitigation Actions
<!-- Add to project plan -->
| Risk | Probability | Impact | Mitigation Action | Owner | Deadline |
|------|-------------|--------|-------------------|-------|----------|
| [Risk 1] | H/M/L | H/M/L | [action] | [name] | [date] |
| [Risk 2] | H/M/L | H/M/L | [action] | [name] | [date] |
```

### Добавить секцию Architecture Decision Records

```markdown
<!-- ADD IN ARCHITECTURE SECTION -->

## Architecture Decisions (Brainstorm-Curate)

### Decision 1: [Decision Name]

#### Context
[Why this decision needs to be made now]

#### Options Evaluated

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A: [Name] | [Brief description] | +[Pro 1]<br>+[Pro 2] | -[Con 1]<br>-[Con 2] |
| B: [Name] | [Brief description] | +[Pro 1]<br>+[Pro 2] | -[Con 1]<br>-[Con 2] |
| C: [Name] | [Brief description] | +[Pro 1]<br>+[Pro 2] | -[Con 1]<br>-[Con 2] |

#### Evaluation Matrix

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| User Value | 25% | _/10 | _/10 | _/10 |
| Feasibility | 25% | _/10 | _/10 | _/10 |
| Differentiation | 20% | _/10 | _/10 | _/10 |
| Cost | 15% | _/10 | _/10 | _/10 |
| Risk | 15% | _/10 | _/10 | _/10 |
| **Weighted Score** | 100% | _/10 | _/10 | _/10 |

#### Decision
**Chosen**: Option [X]

**Rationale**: [Why this option best satisfies our criteria]

**Trade-offs Accepted**: [What we're giving up by not choosing alternatives]

**Reversibility**: [How hard to change if wrong? High/Medium/Low]
```

### Добавить секцию RACI Matrix

```markdown
<!-- ADD AFTER DEPENDENCY REGISTRY -->

## RACI Matrix

| Task/Deliverable | Responsible | Accountable | Consulted | Informed |
|------------------|-------------|-------------|-----------|----------|
| Specification approval | PM | VP Product | Engineering, UX | All |
| Architecture design | Tech Lead | CTO | Senior Engineers | PM, QA |
| API contracts | Backend Lead | Tech Lead | Frontend, External | PM |
| UI implementation | Frontend Lead | Tech Lead | UX, Backend | PM |
| Testing strategy | QA Lead | Tech Lead | Engineering | PM |
| Security review | Security | CISO | Engineering | All |
| Documentation | Tech Writer | PM | Engineering | All |
| Go/No-Go decision | PM | VP Product | All | Company |

### RACI Rules
- Exactly ONE Accountable per row
- Multiple Responsible is OK (but assign lead)
- Consulted should actually be consulted before decisions
- Informed should be kept up to date proactively
```

### Добавить секцию Rollout Strategy

```markdown
<!-- ADD AT END OF PLAN -->

## Rollout Strategy

### Phase 1: Internal Validation
- **Audience**: Engineering team, internal stakeholders (0.1%)
- **Duration**: 3 days
- **Feature Flag**: `feature_[name]_internal`
- **Success Criteria**:
  - [ ] No P0/P1 bugs discovered
  - [ ] Performance within targets
  - [ ] No security vulnerabilities
- **Rollback Trigger**: Error rate >1% OR critical bug

### Phase 2: Beta Testing
- **Audience**: Opted-in beta users (5%)
- **Duration**: 7 days
- **Feature Flag**: `feature_[name]_beta`
- **Success Criteria**:
  - [ ] User feedback positive (NPS stable or improved)
  - [ ] Adoption rate on track
  - [ ] Support ticket volume acceptable
- **Rollback Trigger**: NPS drops >10 points OR adoption <20%

### Phase 3: Limited Release
- **Audience**: Random sample (25%)
- **Duration**: 7 days
- **Feature Flag**: `feature_[name]_limited`
- **Success Criteria**:
  - [ ] Business metrics improving
  - [ ] No unexpected side effects
  - [ ] Scale performance verified
- **Rollback Trigger**: Ticket spike >3x baseline OR metrics regression

### Phase 4: General Availability
- **Audience**: All users (100%)
- **Feature Flag**: Remove flag (cleanup)
- **Success Criteria**:
  - [ ] All success metrics on target
  - [ ] Documentation complete
  - [ ] Support team trained

### Rollback Procedure
1. Set feature flag to OFF (immediate)
2. Notify on-call engineer and PM
3. Create incident ticket
4. Communicate to affected users
5. Begin root cause analysis
6. Document learnings
```

---

## 3. tasks-template.md Improvements

### Добавить INVEST Validation

```markdown
<!-- ADD AT TOP OF TASKS FILE -->

## Task Quality Validation

### INVEST Compliance Summary

| Task ID | I | N | V | E | S | T | Status |
|---------|---|---|---|---|---|---|--------|
| T001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Ready |
| T002 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Ready |
| ... | | | | | | | |

### INVEST Criteria
- **I**ndependent: Task can be started without waiting for other tasks
- **N**egotiable: Implementation details can be adjusted
- **V**aluable: Delivers measurable value to user or business
- **E**stimable: Effort can be reasonably estimated
- **S**mall: Completable in 1-3 days (4-16 hours)
- **T**estable: Clear acceptance criteria exist

### Failed Tasks → Required Actions
<!-- List tasks failing INVEST with remediation -->
```

### Добавить Effort Estimation

```markdown
<!-- ADD AFTER EACH TASK -->

## Effort Summary

### Size Guide
| Size | Hours | Complexity | Criteria |
|------|-------|------------|----------|
| XS | 1-2h | Trivial | Config change, copy update |
| S | 2-4h | Simple | Single function, basic endpoint |
| M | 4-8h | Moderate | New component, integration |
| L | 8-16h | Complex | New service, major refactor |
| XL | 16-32h | Very complex | Architecture change |
| XXL | 32h+ | Epic | **MUST SPLIT!** |

### Task Estimates

| Phase | Task ID | Description | Size | Hours | Confidence |
|-------|---------|-------------|------|-------|------------|
| Setup | T001 | [desc] | S | 3h | High |
| Foundation | T002 | [desc] | M | 6h | Medium |
| ... | | | | | |

### Totals
| Category | Hours | Buffer (20%) | Total |
|----------|-------|--------------|-------|
| P1 Tasks | X | +20% | Y |
| P2 Tasks | X | +20% | Y |
| **Total** | X | | **Y hours** |

**Estimated Duration**: [Y / 6h per day] = Z productive days
```

### Добавить Definition of Done

```markdown
<!-- ADD AT END OF TASKS FILE -->

## Definition of Done

### For Implementation Tasks [FR:xxx]
Every implementation task is complete when:
- [ ] Code written and self-reviewed
- [ ] Unit tests written with ≥80% coverage
- [ ] Integration tests for external dependencies
- [ ] Code passes lint checks (0 errors)
- [ ] Code passes type checks (≥95% coverage)
- [ ] @speckit annotations added linking to requirements
- [ ] Pull request created and approved by peer
- [ ] Code merged to main branch
- [ ] Task marked complete in tasks.md

### For Test Tasks [TEST:xxx]
Every test task is complete when:
- [ ] Test scenario implemented per acceptance criteria
- [ ] Test passes consistently (no flaky failures)
- [ ] Edge cases from spec are covered
- [ ] Test documented in test plan
- [ ] Test added to CI pipeline

### For Design Tasks [VR:xxx / IR:xxx]
Every design task is complete when:
- [ ] Design reviewed by peer designer
- [ ] Developer handoff meeting completed
- [ ] Components specified in Figma with all states
- [ ] Design tokens exported (colors, typography, spacing)
- [ ] Storybook story created

### For Documentation Tasks [APIDOC:xxx]
Every documentation task is complete when:
- [ ] API documented with request/response examples
- [ ] README updated with new feature
- [ ] RUNNING.md updated if setup changed
- [ ] CHANGELOG.md entry added
- [ ] Migration guide written (if breaking changes)

### For Migration Tasks [MIG:xxx]
Every migration task is complete when:
- [ ] Migration script written and tested
- [ ] Rollback script written and tested
- [ ] Data validation passed
- [ ] Zero-downtime deployment verified
- [ ] Monitoring alerts configured
```

---

## 4. Quality Profiles for implement.md

### Добавить профили качества

```markdown
<!-- ADD TO IMPLEMENT COMMAND -->

## Quality Gate Profiles

Select profile at project start (in constitution.md):

### Profile: MVP
**Use for**: Early-stage products, rapid prototyping, internal tools

| Gate | Threshold | Blocking |
|------|-----------|----------|
| QG-001: Build Success | Pass | ✅ Yes |
| QG-002: Test Coverage | ≥60% | ✅ Yes |
| QG-003: Type Coverage | ≥80% | ✅ Yes |
| QG-004: Lint Errors | 0 critical, ≤5 warnings | ✅ Yes |
| QG-005: Security Scan | 0 critical | ✅ Yes |
| QG-006: Accessibility | WCAG 2.1 A | ⚠️ Warning |
| QG-007: Performance | LCP <4s | ⚠️ Warning |
| QG-008: Documentation | README exists | ⚠️ Warning |

### Profile: Standard
**Use for**: Most production features, B2B/B2C products

| Gate | Threshold | Blocking |
|------|-----------|----------|
| QG-001: Build Success | Pass | ✅ Yes |
| QG-002: Test Coverage | ≥80% | ✅ Yes |
| QG-003: Type Coverage | ≥95% | ✅ Yes |
| QG-004: Lint Errors | 0 | ✅ Yes |
| QG-005: Security Scan | 0 critical, 0 high | ✅ Yes |
| QG-006: Accessibility | WCAG 2.1 A | ✅ Yes |
| QG-007: Performance | LCP <2.5s | ⚠️ Warning |
| QG-008: Documentation | 80% public API | ✅ Yes |

### Profile: Strict
**Use for**: Enterprise, financial, healthcare, regulated industries

| Gate | Threshold | Blocking |
|------|-----------|----------|
| QG-001: Build Success | Pass | ✅ Yes |
| QG-002: Test Coverage | ≥90% | ✅ Yes |
| QG-003: Type Coverage | ≥99% | ✅ Yes |
| QG-004: Lint Errors | 0 | ✅ Yes |
| QG-005: Security Scan | 0 critical/high/medium | ✅ Yes |
| QG-006: Accessibility | WCAG 2.1 AA | ✅ Yes |
| QG-007: Performance | LCP <1.5s, Lighthouse ≥80 | ✅ Yes |
| QG-008: Documentation | 100% public API | ✅ Yes |
| QG-009: Penetration Test | Pass | ✅ Yes |
| QG-010: Audit Log | Complete | ✅ Yes |

### Profile Override Rules
- Profile is set in `constitution.md` at project initialization
- Cannot be changed mid-feature without PM approval
- Individual gates can be waived with documented exception
- Exception requires: Justification + Owner + Remediation plan + Deadline
```

---

## 5. design-template.md Improvements

### Добавить Component Specification Template

```markdown
<!-- STANDARD COMPONENT SPEC FORMAT -->

## Component: [Component Name]

### 1. Purpose
[One sentence: when to use this component and why]

### 2. Anatomy
```
┌──────────────────────────────────────┐
│ [Label]                              │
│ ┌────────────────────────────────┐   │
│ │ [Input/Content area]           │   │
│ └────────────────────────────────┘   │
│ [Helper text / Error message]        │
└──────────────────────────────────────┘
```

### 3. Variants
| Variant | Use Case | Visual Treatment |
|---------|----------|------------------|
| Primary | Main CTAs | Solid fill, brand color |
| Secondary | Alternative actions | Outline, border |
| Ghost | Tertiary actions | No border, text only |
| Danger | Destructive actions | Red/warning color |

### 4. States (All 7 Required)
| State | Visual | Cursor | Interaction |
|-------|--------|--------|-------------|
| Default | [desc] | pointer | Awaiting input |
| Hover | [desc] | pointer | Mouse over |
| Focus | [desc] | text | Keyboard focus (ring) |
| Active | [desc] | pointer | During click |
| Disabled | [desc] | not-allowed | Not interactive |
| Loading | [desc] | wait | Async operation |
| Error | [desc] | pointer | Validation failed |

### 5. Sizes
| Size | Height | Font | Padding | Use Case |
|------|--------|------|---------|----------|
| Small | 32px | 14px | 8px 12px | Dense UIs, tables |
| Medium | 40px | 16px | 12px 16px | Default, forms |
| Large | 48px | 18px | 16px 24px | Hero, mobile-first |

### 6. Spacing & Layout
- **Internal Padding**: [top right bottom left]
- **Icon Spacing**: [gap between icon and text]
- **Margin Recommendations**: [typical surrounding space]
- **Alignment**: [left/center/right, when each]

### 7. Motion Specifications
| Animation | Duration | Easing | Trigger |
|-----------|----------|--------|---------|
| Hover transition | 150ms | ease-out | Mouse enter/leave |
| Focus ring appear | 100ms | ease-in | Keyboard focus |
| Active press | 50ms | ease-in | Mouse down |
| Loading spinner | 1000ms | linear, infinite | Loading state |

### 8. Responsive Behavior
| Breakpoint | Behavior |
|------------|----------|
| Mobile (<768px) | Full width, stacked layout |
| Tablet (768-1024px) | Flexible width, min 200px |
| Desktop (>1024px) | Fixed or percentage width |

### 9. Accessibility Requirements
- **ARIA Role**: [button/link/etc.]
- **Keyboard Navigation**:
  - Tab: Focus component
  - Enter/Space: Activate
  - Escape: Cancel (if applicable)
- **Screen Reader**: [announcement pattern]
- **Color Contrast**: ≥4.5:1 (AA) for text, ≥3:1 for UI

### 10. Code Reference
```tsx
// React usage example
<Button
  variant="primary"
  size="medium"
  disabled={false}
  loading={false}
  onClick={handleClick}
>
  Button Text
</Button>
```

- **Figma**: [link to component]
- **Storybook**: [link to story]
- **Design Tokens**: [link to token file]
```

### Добавить Motion Design System

```markdown
<!-- ADD TO DESIGN TEMPLATE -->

## Motion Design System

### Motion Principles
1. **Purposeful**: Every animation serves a UX goal (feedback, guide, delight)
2. **Responsive**: Immediate acknowledgment of user input (<100ms)
3. **Natural**: Physics-based, familiar motion patterns
4. **Consistent**: Same patterns used throughout the application

### Duration Tokens
| Token | Value | Use Case |
|-------|-------|----------|
| `--motion-instant` | 0ms | Immediate state change |
| `--motion-fast` | 100ms | Micro-interactions (hover, click) |
| `--motion-normal` | 200ms | Standard transitions |
| `--motion-slow` | 300ms | Complex transitions |
| `--motion-deliberate` | 500ms | Emphasis, reveal, modal |

### Easing Tokens
| Token | CSS Value | Use Case |
|-------|-----------|----------|
| `--ease-out` | cubic-bezier(0, 0, 0.2, 1) | Element entering view |
| `--ease-in` | cubic-bezier(0.4, 0, 1, 1) | Element leaving view |
| `--ease-in-out` | cubic-bezier(0.4, 0, 0.2, 1) | Element moving/transforming |
| `--ease-linear` | linear | Continuous animation (spinner) |

### Standard Patterns

#### Page Transitions
```css
.page-enter {
  opacity: 0;
  transform: translateY(16px);
}
.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 200ms ease-out, transform 200ms ease-out;
}
.page-exit-active {
  opacity: 0;
  transition: opacity 150ms ease-in;
}
```

#### Modal/Dialog
```css
.modal-backdrop {
  transition: opacity 200ms ease-out;
}
.modal-content {
  transition: opacity 200ms ease-out, transform 200ms ease-out;
  transform: scale(0.95);
}
.modal-content.open {
  transform: scale(1);
}
```

#### Toast/Notification
```css
.toast-enter {
  transform: translateX(100%);
}
.toast-enter-active {
  transform: translateX(0);
  transition: transform 300ms ease-out;
}
```

### Accessibility
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
```

### Добавить Developer Handoff Checklist

```markdown
<!-- ADD AT END OF DESIGN SPEC -->

## Developer Handoff Checklist

### Pre-Handoff (Designer)
- [ ] All components use correct naming convention (PascalCase)
- [ ] Auto-layout applied to all components
- [ ] All variants named correctly (Property=Value format)
- [ ] All 7 states documented for interactive components
- [ ] Responsive constraints set correctly
- [ ] Dev mode annotations complete
- [ ] Design tokens linked (not hardcoded values)

### Assets Export
- [ ] Icons exported as SVG (optimized, no unnecessary groups)
- [ ] Images at 1x and 2x resolution
- [ ] Illustrations in vector format (SVG preferred)
- [ ] Favicons generated (16, 32, 180, 192, 512px)

### Token Export
- [ ] Colors exported (CSS variables + JSON)
- [ ] Typography scale exported
- [ ] Spacing scale exported (4px grid)
- [ ] Border radius scale exported
- [ ] Shadow tokens exported
- [ ] Motion tokens exported (duration, easing)

### Documentation
- [ ] Component specs complete (purpose, anatomy, states, etc.)
- [ ] Usage guidelines written (do/don't examples)
- [ ] Accessibility requirements documented
- [ ] Responsive behavior documented
- [ ] Motion specifications included

### Code Integration
- [ ] Figma component names match code components
- [ ] Props/variants align with implementation
- [ ] Storybook stories created for all components
- [ ] Visual regression tests set up

### Handoff Meeting
- [ ] Walk through designs with developer (10 min)
- [ ] Clarify edge cases and questions (10 min)
- [ ] Review accessibility requirements (5 min)
- [ ] Agree on implementation timeline (5 min)
- [ ] Q&A (10 min)

### Post-Handoff
- [ ] Designer available for questions during implementation
- [ ] Design review scheduled before merge
- [ ] Storybook review completed
- [ ] Visual QA passed
```

---

## Implementation Priority

### Week 1-2: Critical Foundations
1. Add SQS Checklist to spec-template.md
2. Add Pre-Mortem to plan-template.md
3. Add INVEST Validation to tasks-template.md
4. Add Quality Gate Profiles to implement.md

### Week 3-4: Excellence Patterns
1. Add Brainstorm-Curate to plan-template.md
2. Add Effort Estimation to tasks-template.md
3. Add Definition of Done to tasks-template.md
4. Add Rollout Strategy to plan-template.md

### Week 5-6: Design & Integration
1. Add Component Spec Template
2. Add Motion Design System
3. Add Developer Handoff Checklist
4. Add Evidence Tracking to spec-template.md

### Week 7-8: Growth & Metrics
1. Add Success Metrics to spec-template.md
2. Add Experimentation Plan
3. Add RACI Matrix
4. Final integration testing

---

*Template Improvements v1.0 | 2026-01-03*

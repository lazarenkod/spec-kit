# Wave-by-Wave Design Strategy

Quality bars and design focus areas for each wave of concept design generation.

## Wave Model Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│  Wave 1: Foundation                                             │
│  ───────────────────                                            │
│  Core infrastructure, auth, navigation, FTUE                    │
│  Quality Bar: 95%+ | Zero compromises                           │
├─────────────────────────────────────────────────────────────────┤
│  Wave 2: Experience                                             │
│  ──────────────────                                             │
│  Primary user flows, key features, differentiators              │
│  Quality Bar: 90%+ | Polish matters                             │
├─────────────────────────────────────────────────────────────────┤
│  Wave 3+: Business                                              │
│  ───────────────────                                            │
│  Secondary features, admin, integrations, analytics             │
│  Quality Bar: 85%+ | Functional first                           │
└─────────────────────────────────────────────────────────────────┘
```

## Wave 1: Foundation Features

### Scope

Features from concept.md `execution_order.wave_1`:
- Authentication & authorization
- Core navigation structure
- First-time user experience (FTUE)
- Error handling patterns
- Basic layouts

### Design Quality Bar

| Criterion | Target | Rationale |
|-----------|--------|-----------|
| Wireframe Completeness | 100% | Every screen fully specified |
| State Coverage | 100% | All states (loading, error, empty, success) |
| Accessibility | WCAG AAA | Foundation sets a11y standard |
| Responsive Design | All breakpoints | Mobile, tablet, desktop |
| Animation Specs | Complete | Transitions between all states |
| Component Reusability | High | These become the design system |

### Design Focus

```text
1. DESIGN SYSTEM ALIGNMENT
   - Every component matches design-system.md tokens
   - No one-off colors, spacings, or typography
   - Establish component variants (primary, secondary, ghost, etc.)

2. ACCESSIBILITY FOUNDATION
   - Screen reader testing for all flows
   - Keyboard navigation complete
   - Focus management documented
   - Color contrast verified

3. ERROR HANDLING PATTERNS
   - Consistent error message format
   - Recovery paths for all errors
   - Graceful degradation defined

4. NAVIGATION PATTERNS
   - Information architecture locked
   - Route structure finalized
   - Deep linking support
```

### Output Requirements

| Artifact | Required | Notes |
|----------|----------|-------|
| Foundation designs | All 7 | AUTH, ERROR, LAYOUT, NAV, FTUE, FEEDBACK, ADMIN |
| Navigation map | Complete | Sitemap + route table |
| Journey flows | All core | At minimum J000 (golden path) |
| Motion system | Complete | Animation tokens + patterns |
| Component inventory | Complete | Master list with categories |

### Checkpoint Before Wave 2

```text
□ App-DQS >= 90 for Wave 1 artifacts
□ All UX foundations have design coverage
□ Golden path journey fully designed
□ Design system tokens locked (no changes after this)
□ Component inventory established
□ Accessibility audit passed
```

---

## Wave 2: Experience Features

### Scope

Features from concept.md `execution_order.wave_2`:
- Primary user workflows
- Differentiating features
- Core value propositions
- Main dashboard/home experience

### Design Quality Bar

| Criterion | Target | Rationale |
|-----------|--------|-----------|
| Wireframe Completeness | 95% | Main screens fully specified |
| State Coverage | 90% | Critical states, defer edge cases |
| Accessibility | WCAG AA | Maintain accessibility standard |
| Responsive Design | Mobile + Desktop | Tablet can use desktop layout |
| Animation Specs | Key transitions | Focus on user-facing animations |
| Component Reusability | Medium | Feature-specific components OK |

### Design Focus

```text
1. USER EXPERIENCE POLISH
   - Delight moments (micro-interactions, celebrations)
   - Loading state quality (skeletons, optimistic UI)
   - Empty states with personality

2. FEATURE DIFFERENTIATION
   - Unique interactions that set app apart
   - Brand expression through design
   - Innovative patterns where appropriate

3. FLOW OPTIMIZATION
   - Minimize steps in critical paths
   - Smart defaults reduce input
   - Progressive disclosure for complexity

4. CROSS-FEATURE CONSISTENCY
   - Patterns from Wave 1 applied consistently
   - New patterns documented for reuse
   - No regression on design system
```

### Output Requirements

| Artifact | Required | Notes |
|----------|----------|-------|
| Feature designs | All Wave 2 | Per concept execution_order |
| Additional journeys | As defined | J001, J002, etc. |
| Shared components | As needed | New components added to inventory |

### Checkpoint Before Wave 3

```text
□ App-DQS >= 85 for Wave 2 artifacts
□ All Wave 2 features have design coverage
□ Primary user journeys designed
□ No design system token changes (use existing)
□ Component inventory updated
```

---

## Wave 3+: Business Features

### Scope

Features from concept.md `execution_order.wave_3` and beyond:
- Admin interfaces
- Settings & configuration
- Integrations
- Analytics & reporting
- Edge case features

### Design Quality Bar

| Criterion | Target | Rationale |
|-----------|--------|-----------|
| Wireframe Completeness | 85% | Main flows, defer variations |
| State Coverage | 80% | Happy path + key errors |
| Accessibility | WCAG AA | Maintain standard, not exceed |
| Responsive Design | Desktop primary | Admin often desktop-focused |
| Animation Specs | Minimal | Functional transitions only |
| Component Reusability | High | Use existing components |

### Design Focus

```text
1. FUNCTIONAL COMPLETENESS
   - Cover all required functionality
   - Clear user paths, no dead ends
   - Basic error handling

2. CONSISTENCY OVER INNOVATION
   - Reuse Wave 1/2 patterns
   - No new component variants
   - Standard layouts

3. EFFICIENCY
   - Dense information display OK
   - Power user optimizations
   - Keyboard-first for admin tasks

4. TECHNICAL FEASIBILITY
   - Simple implementation patterns
   - Standard UI libraries sufficient
   - No complex animations
```

### Output Requirements

| Artifact | Required | Notes |
|----------|----------|-------|
| Feature designs | All Wave 3+ | May be less detailed |
| Journey additions | Edge cases | Error recovery, admin flows |
| Component updates | Minimal | Document but don't over-specify |

### Final Checkpoint

```text
□ App-DQS >= 80 overall
□ All concept features have design coverage
□ All journeys have design coverage
□ All UX foundations covered
□ Traceability matrix complete (100%)
□ Component inventory finalized
```

---

## Quality Gates Summary

| Wave | Min DQS | Focus | Iteration Limit |
|------|---------|-------|-----------------|
| 1 | 90 | Foundation excellence | Until passed |
| 2 | 85 | Experience polish | 2 iterations |
| 3+ | 80 | Functional completeness | 1 iteration |

## Re-Running Waves

```text
IF App-DQS < threshold after wave:

  Wave 1: MUST iterate until 90+
    - Foundation quality non-negotiable
    - Block Wave 2 until passed

  Wave 2: MAY iterate once
    - Address critical gaps
    - Accept minor polish gaps
    - Document tech debt

  Wave 3+: ACCEPT and document
    - Log gaps in index.md
    - Plan post-launch improvements
    - Move forward
```

## Integration Commands

```bash
# Design Wave 1 (Foundation)
/speckit.design --concept

# Design Wave 2 (Experience)
/speckit.design --concept --wave 2

# Design Wave 3+ (Business)
/speckit.design --concept --wave 3

# Design all waves (small concepts only)
/speckit.design --concept --all
```

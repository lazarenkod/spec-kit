# Application Design Overview

> Generated from concept.md using `/speckit.design --concept`

## Metadata

| Property | Value |
|----------|-------|
| **Concept** | {concept_name} |
| **CQS Score** | {cqs_score} |
| **App-DQS** | {app_dqs_score} |
| **Generated** | {timestamp} |
| **Current Wave** | {current_wave} of {total_waves} |

---

## Design Artifacts

| Category | Artifact | Status | DQS | Link |
|----------|----------|--------|-----|------|
| **Foundation** | Design System | {status} | {score} | [design-system.md](design-system.md) |
| **Foundation** | Navigation | {status} | {score} | [navigation.md](navigation.md) |
| **UX Foundations** | Auth Flows | {status} | {score} | [foundations/auth-design.md](foundations/auth-design.md) |
| **UX Foundations** | Error Handling | {status} | {score} | [foundations/error-design.md](foundations/error-design.md) |
| **UX Foundations** | Layouts | {status} | {score} | [foundations/layout-design.md](foundations/layout-design.md) |
| **UX Foundations** | Navigation | {status} | {score} | [foundations/nav-design.md](foundations/nav-design.md) |
| **UX Foundations** | FTUE | {status} | {score} | [foundations/ftue-design.md](foundations/ftue-design.md) |
| **UX Foundations** | Feedback | {status} | {score} | [foundations/feedback-design.md](foundations/feedback-design.md) |
| **UX Foundations** | Admin | {status} | {score} | [foundations/admin-design.md](foundations/admin-design.md) |
| **Journeys** | Golden Path | {status} | {score} | [journeys/J000-golden-path.md](journeys/J000-golden-path.md) |
| **Wave 1** | {feature_count} features | {status} | {score} | [waves/wave-1/](waves/wave-1/) |
| **Wave 2** | {feature_count} features | {status} | {score} | [waves/wave-2/](waves/wave-2/) |
| **Wave 3+** | {feature_count} features | {status} | {score} | [waves/wave-3/](waves/wave-3/) |
| **Motion** | Animation System | {status} | {score} | [motion/](motion/) |
| **Components** | Inventory | {status} | {score} | [components/inventory.md](components/inventory.md) |

---

## Traceability Matrix

### Features → Design Artifacts

| Concept ID | Name | Wave | Design Artifact | Coverage |
|------------|------|------|-----------------|----------|
| EPIC-001.F01 | {feature_name} | 1 | [waves/wave-1/EPIC-001.F01-design.md](waves/wave-1/EPIC-001.F01-design.md) | {coverage}% |
| EPIC-001.F02 | {feature_name} | 1 | [waves/wave-1/EPIC-001.F02-design.md](waves/wave-1/EPIC-001.F02-design.md) | {coverage}% |
<!-- Add more features as generated -->

### Journeys → Design Artifacts

| Journey ID | Name | Steps | Design Artifact | Coverage |
|------------|------|-------|-----------------|----------|
| J000 | Golden Path | {step_count} | [journeys/J000-golden-path.md](journeys/J000-golden-path.md) | {coverage}% |
<!-- Add more journeys as generated -->

### UX Foundations → Design Artifacts

| Foundation | Scenarios | Design Artifact | Coverage |
|------------|-----------|-----------------|----------|
| AUTH | UXF-AUTH-001, UXF-AUTH-002, ... | [foundations/auth-design.md](foundations/auth-design.md) | {coverage}% |
| ERROR | UXF-ERR-001, UXF-ERR-002, ... | [foundations/error-design.md](foundations/error-design.md) | {coverage}% |
| LAYOUT | UXF-LAYOUT-001, ... | [foundations/layout-design.md](foundations/layout-design.md) | {coverage}% |
| NAV | UXF-NAV-001, ... | [foundations/nav-design.md](foundations/nav-design.md) | {coverage}% |
| FTUE | UXF-FTUE-001, ... | [foundations/ftue-design.md](foundations/ftue-design.md) | {coverage}% |
| FEEDBACK | UXF-FEED-001, ... | [foundations/feedback-design.md](foundations/feedback-design.md) | {coverage}% |
| ADMIN | UXF-ADMIN-001, ... | [foundations/admin-design.md](foundations/admin-design.md) | {coverage}% |

---

## App-DQS Breakdown

```text
App-DQS = {app_dqs_score}/100

Components:
  Design System:     {design_system_score}/100 × 0.15 = {weighted_ds}
  Foundations:       {foundations_score}/100 × 0.20 = {weighted_f}
  Journeys:          {journeys_score}/100 × 0.20 = {weighted_j}
  Features:          {features_score}/100 × 0.30 = {weighted_feat}
  Traceability:      {trace_score}/100 × 0.15 = {weighted_t}
  ─────────────────────────────────────────────────
  Total:             {app_dqs_score}/100
```

### Quality Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| 90-100 | Production ready, comprehensive design |
| 80-89 | High quality, minor gaps acceptable |
| 70-79 | Good foundation, some areas need refinement |
| 60-69 | Usable but requires iteration |
| < 60 | Incomplete, not recommended for implementation |

---

## Coverage Gaps

<!-- List any missing design artifacts or incomplete traceability -->

| Gap Type | Missing | Impact | Recommendation |
|----------|---------|--------|----------------|
<!-- Example: | Journey | J003 | Medium | Run /speckit.design --concept to complete | -->

---

## Next Steps

- [ ] **Review**: Open individual design files for detailed specs
- [ ] **Preview**: Run `/speckit.preview` to generate interactive HTML preview
- [ ] **Iterate**: Address coverage gaps if App-DQS < 80
- [ ] **Continue**: Run `/speckit.design --concept --wave {next_wave}` for next wave
- [ ] **Plan**: Run `/speckit.plan` to create technical implementation plan
- [ ] **Implement**: Run `/speckit.tasks` to generate development tasks

---

## Generation Log

| Phase | Duration | Artifacts | Notes |
|-------|----------|-----------|-------|
| Validation | {time} | - | CQS: {cqs_score} |
| Design System | {time} | 1 | {notes} |
| Foundations | {time} | 7 | {notes} |
| Navigation | {time} | 1 | {notes} |
| Journeys | {time} | {count} | {notes} |
| Wave {N} Features | {time} | {count} | {notes} |
| Motion System | {time} | 2 | {notes} |
| Component Inventory | {time} | 1 | {notes} |
| **Total** | **{total_time}** | **{total_count}** | |

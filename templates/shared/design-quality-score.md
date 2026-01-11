# Design Quality Score (DQS) v2.0

## Purpose

Quantify design specification quality across visual, UX, and brand dimensions to ensure production-ready designs.

## Version History

- **v2.0** (2026-01-11): Added 7 UX/brand dimensions (Q15-Q24), expanded from 5 to 12 total dimensions
- **v1.0** (2025-10-15): Initial release with 5 baseline dimensions (visual tokens, components, accessibility)

---

## Formula

```
DQS = Σ(dimension_score × weight) × 100

where:
  dimension_score = 0-1 (0% to 100% of dimension potential)
  weight = dimension_weight (sum of all weights = 1.0)
  DQS = 0-100 (final quality score)
```

---

## Dimensions (12 total, 100 points)

### Baseline Dimensions (45 points, 45% weight)

#### 1. Token Completeness (10 points, 10% weight)

**Evaluation Criteria**:
- Color tokens: primary, secondary, accent, semantic (success, error, warning, info) → 2.5 pts
- Typography tokens: font families, sizes, weights, line heights → 2.5 pts
- Spacing tokens: scale from xs to 3xl (at least 8 steps) → 2.5 pts
- Motion tokens: durations, easing functions → 2.5 pts

**Scoring**:
- All 4 categories complete → 10 pts
- 3 categories complete → 7.5 pts
- 2 categories complete → 5 pts
- 1 category complete → 2.5 pts
- 0 categories complete → 0 pts

**Pass Threshold**: >= 7.5 pts (75%)

---

#### 2. Component Documentation (8 points, 8% weight)

**Evaluation Criteria**:
- Storybook stories for all components → 2 pts
- Props documentation with types and descriptions → 2 pts
- Usage examples and code snippets → 2 pts
- Accessibility notes (ARIA, keyboard support) → 2 pts

**Scoring**:
- All 4 categories complete → 8 pts
- 3 categories complete → 6 pts
- 2 categories complete → 4 pts
- 1 category complete → 2 pts
- 0 categories complete → 0 pts

**Pass Threshold**: >= 6 pts (75%)

---

#### 3. Accessibility Compliance (12 points, 12% weight)

**Evaluation Criteria**:
- WCAG color contrast compliance (4.5:1 text, 3:1 UI) → 3 pts
- ARIA patterns documented for interactive components → 3 pts
- Keyboard navigation specified (tab order, focus states) → 3 pts
- Screen reader annotations (labels, descriptions, live regions) → 3 pts

**Scoring**:
- All 4 categories complete → 12 pts
- 3 categories complete → 9 pts
- 2 categories complete → 6 pts
- 1 category complete → 3 pts
- 0 categories complete → 0 pts

**Pass Threshold**: >= 9 pts (75%)

---

#### 4. Consistency (10 points, 10% weight)

**Evaluation Criteria**:
- All colors use design tokens (no hardcoded hex values) → 2.5 pts
- Typography follows token system (no inline font-size) → 2.5 pts
- Spacing uses token scale (no hardcoded margins/padding) → 2.5 pts
- Component variants follow naming convention → 2.5 pts

**Scoring**:
- All 4 categories complete → 10 pts
- 3 categories complete → 7.5 pts
- 2 categories complete → 5 pts
- 1 category complete → 2.5 pts
- 0 categories complete → 0 pts

**Pass Threshold**: >= 7.5 pts (75%)

---

#### 5. Figma Export Quality (5 points, 5% weight)

**Evaluation Criteria**:
- Token export compatibility (Figma Tokens plugin format) → 1.25 pts
- Layer naming consistency (component/variant naming) → 1.25 pts
- Component variant structure (props-based variants) → 1.25 pts
- Style guide completeness (cover page, usage docs) → 1.25 pts

**Scoring**:
- All 4 categories complete → 5 pts
- 3 categories complete → 3.75 pts
- 2 categories complete → 2.5 pts
- 1 category complete → 1.25 pts
- 0 categories complete → 0 pts

**Pass Threshold**: >= 3.75 pts (75%)

---

### UX Quality Dimensions (35 points, 35% weight) — NEW v0.6.2

#### 6. Usability Testing Plan (15 points, 15% weight)

**Evaluation** (based on `constitution.md design_system.ux_quality.usability_target`):

| Target Level | Requirements | Score |
|--------------|-------------|-------|
| **best-in-class** | A/B testing plan, user testing (10+ participants), task completion metrics (>= 90%), SUS score tracking, iterative testing cycles | 15 pts |
| **competitive** | User testing (5+ participants), task completion metrics (>= 80%), basic analytics tracking | 10 pts |
| **acceptable** | Metrics tracking only (GA/PostHog), no formal user testing | 5 pts |
| **low** | No usability testing plan | 0 pts |

**Pass Threshold**: >= 10 pts (67%) for competitive/best-in-class projects

---

#### 7. User Flow Documentation (15 points, 15% weight)

**Evaluation** (based on `constitution.md design_system.ux_quality.flow_complexity`):

**Base Score** (all complexity levels):
- Flow diagrams present (Mermaid or visual) → 5 pts
- Navigation system documented → 5 pts
- Information architecture defined → 5 pts

**Complexity Requirements** (minimum score for pass):

| Complexity | Requirements | Pass Threshold |
|------------|-------------|----------------|
| **very-complex** | All flows documented, multi-role IA, deep navigation (3+ levels) | 15 pts (100%) |
| **complex** | Main flows documented, standard IA, 2-level navigation | 12 pts (80%) |
| **moderate** | Core flows documented, simple IA, 1-level navigation | 8 pts (53%) |
| **simple** | Linear flow documented, minimal IA | 5 pts (33%) |

**Scoring**:
- All 3 categories complete → 15 pts
- 2 categories complete → 10 pts
- 1 category complete → 5 pts
- 0 categories complete → 0 pts

---

#### 8. Accessibility Empowerment (10 points, 10% weight)

**Evaluation** (based on `constitution.md design_system.ux_quality.design_a11y_level`):

| A11y Level | Requirements | Score |
|------------|-------------|-------|
| **inclusive** | User testing with disabled users, innovative a11y patterns (beyond WCAG), disability-led design process | 10 pts |
| **proactive** | Exceeds WCAG AA (e.g., 7:1 contrast), inclusive design patterns (progressive enhancement, multimodal input) | 8 pts |
| **compliance-plus** | WCAG AA compliance + design best practices (focus indicators, error prevention) | 6 pts |
| **compliance-only** | Minimum WCAG level from constitution (no additional patterns) | 4 pts |

**Pass Threshold**: >= 6 pts (60%)

---

#### 9. Error Handling UX (5 points, 5% weight)

**Evaluation** (based on `constitution.md design_system.ux_quality.error_prevention`):

| Strategy | Requirements | Score |
|----------|-------------|-------|
| **proactive** | Inline validation, auto-correct suggestions, smart defaults, confirmation dialogs for destructive actions | 5 pts |
| **reactive** | Clear error messages, easy recovery paths, helpful guidance, context preservation | 3 pts |
| **minimal** | Basic error messages, standard browser validation | 1 pt |

**Pass Threshold**: >= 3 pts (60%)

---

#### 10. Responsive Design Completeness (5 points, 5% weight)

**Evaluation** (if `app_type == web-application` in constitution):

**Criteria**:
- Breakpoint system defined (mobile, tablet, desktop) → 2 pts
- Responsive patterns documented (reflow, stack, hide) → 2 pts
- Mobile/tablet/desktop variants specified → 1 pt

**Scoring**:
- All 3 criteria met → 5 pts
- 2 criteria met → 3 pts
- 1 criterion met → 1 pt
- 0 criteria met → 0 pts

**Conditional Scoring**:
- IF `app_type != web-application`: Auto-award 5 pts (N/A)

**Pass Threshold**: >= 3 pts (60%)

---

### Brand Dimensions (5 points, 5% weight) — NEW v0.6.2

#### 11. Brand Consistency (3 points, 3% weight)

**Evaluation** (based on `constitution.md design_system.brand_audience`):

**Criteria**:
- Visual style aligned with `brand_archetype` (innovator: bold, trusted-advisor: conservative, friend: warm, performer: vibrant, minimalist: clean) → 1 pt
- Microcopy follows `tone_of_voice` (formal/professional/conversational/playful/technical examples provided) → 1 pt
- Emotional design patterns match `emotional_goal` (confidence: predictable, delight: playful, empowerment: powerful, calm: gentle, excitement: dynamic) → 1 pt

**Scoring**:
- All 3 criteria met → 3 pts
- 2 criteria met → 2 pts
- 1 criterion met → 1 pt
- 0 criteria met → 0 pts

**Pass Threshold**: >= 2 pts (67%)

---

#### 12. Inclusive Design (2 points, 2% weight)

**Evaluation** (based on `constitution.md design_system.brand_audience.demographics_priority`):

**Scoring**: 0.5 pts per demographic addressed:

| Demographic | Patterns Required | Score |
|-------------|------------------|-------|
| **age-diversity** | Senior-friendly patterns (large touch targets, high contrast), child-safe content (age-appropriate language, parental controls) | 0.5 pt |
| **global-audience** | i18n-ready (externalized strings, date/number formats), RTL support, cultural sensitivity (neutral imagery, inclusive language) | 0.5 pt |
| **neurodiversity** | Cognitive accessibility (simple language, clear instructions), ADHD-friendly (reduced clutter, focus modes), autism-friendly (predictable patterns, no sudden changes) | 0.5 pt |
| **low-bandwidth** | Optimized assets (WebP, lazy loading, image compression), progressive loading (skeleton screens), offline support (service workers) | 0.5 pt |

**Conditional Scoring**:
- IF `demographics_priority == []`: Auto-award 2 pts (N/A)

**Pass Threshold**: >= 1 pt (50%)

---

## Scoring Thresholds

| DQS Range | Quality Level | Action | Gate Status |
|-----------|---------------|--------|-------------|
| 90-100 | Excellent | Production-ready, exemplary quality | PASS |
| 80-89 | Good | Production-ready with minor improvements | PASS |
| 70-79 | Acceptable | Meets minimum threshold (QG-DQS-001), address gaps | PASS |
| 60-69 | Needs Work | Significant gaps, remediation required | FAIL |
| 0-59 | Poor | Major quality issues, full rework recommended | FAIL |

**Quality Gate**: QG-DQS-001 requires **DQS >= 70**

---

## Dimension Weight Summary

| Dimension | Weight | Category |
|-----------|--------|----------|
| Token Completeness | 10% | Baseline |
| Component Documentation | 8% | Baseline |
| Accessibility Compliance | 12% | Baseline |
| Consistency | 10% | Baseline |
| Figma Export Quality | 5% | Baseline |
| **Usability Testing Plan** | **15%** | **UX Quality** |
| **User Flow Documentation** | **15%** | **UX Quality** |
| **Accessibility Empowerment** | **10%** | **UX Quality** |
| **Error Handling UX** | **5%** | **UX Quality** |
| **Responsive Completeness** | **5%** | **UX Quality** |
| **Brand Consistency** | **3%** | **Brand** |
| **Inclusive Design** | **2%** | **Brand** |
| **Total** | **100%** | — |

---

## Example Scoring

### Example 1: Enterprise SaaS (Best-in-class UX)

**Constitution Settings**:
- `usability_target: best-in-class`
- `flow_complexity: complex`
- `design_a11y_level: proactive`
- `error_prevention: proactive`
- `responsive_strategy: platform-optimized`
- `brand_archetype: trusted-advisor`
- `demographics_priority: [global-audience, age-diversity]`

**Scores**:
1. Token Completeness: 10/10 (100%)
2. Component Docs: 8/8 (100%)
3. Accessibility Compliance: 12/12 (100%)
4. Consistency: 10/10 (100%)
5. Figma Export: 5/5 (100%)
6. Usability Testing: 15/15 (best-in-class plan)
7. Flow Documentation: 12/15 (complex IA documented)
8. A11y Empowerment: 8/10 (proactive level)
9. Error Handling: 5/5 (proactive strategy)
10. Responsive: 5/5 (platform-optimized)
11. Brand Consistency: 3/3 (trusted-advisor style)
12. Inclusive Design: 1/2 (2 demographics)

**DQS**: (10 + 8 + 12 + 10 + 5 + 15 + 12 + 8 + 5 + 5 + 3 + 1) = **94/100** ✅ EXCELLENT

---

### Example 2: Mobile Game (Playful Brand, Simple UX)

**Constitution Settings**:
- `usability_target: competitive`
- `flow_complexity: simple`
- `design_a11y_level: compliance-only`
- `error_prevention: reactive`
- `responsive_strategy: N/A` (mobile-only)
- `brand_archetype: performer`
- `demographics_priority: [age-diversity]`

**Scores**:
1. Token Completeness: 7.5/10 (3 categories)
2. Component Docs: 6/8 (3 categories)
3. Accessibility Compliance: 6/12 (basic WCAG)
4. Consistency: 10/10 (token-based)
5. Figma Export: 3.75/5 (3 categories)
6. Usability Testing: 10/15 (competitive plan)
7. Flow Documentation: 5/15 (simple linear flow)
8. A11y Empowerment: 4/10 (compliance-only)
9. Error Handling: 3/5 (reactive strategy)
10. Responsive: 5/5 (N/A, mobile-only)
11. Brand Consistency: 3/3 (performer archetype)
12. Inclusive Design: 0.5/2 (1 demographic)

**DQS**: (7.5 + 6 + 6 + 10 + 3.75 + 10 + 5 + 4 + 3 + 5 + 3 + 0.5) = **63.75/100** ❌ NEEDS WORK

**Remediation**: Improve accessibility (dimension 3, 8), add usability testing (dimension 6), document flows (dimension 7)

---

### Example 3: Developer Tool (Technical Audience, Expert UX)

**Constitution Settings**:
- `usability_target: best-in-class`
- `flow_complexity: moderate`
- `design_a11y_level: compliance-plus`
- `error_prevention: proactive`
- `responsive_strategy: desktop-first`
- `brand_archetype: innovator`
- `tone_of_voice: technical`
- `demographics_priority: [low-bandwidth]`

**Scores**:
1. Token Completeness: 10/10 (100%)
2. Component Docs: 8/8 (100%)
3. Accessibility Compliance: 12/12 (100%)
4. Consistency: 10/10 (100%)
5. Figma Export: 5/5 (100%)
6. Usability Testing: 15/15 (best-in-class plan)
7. Flow Documentation: 8/15 (moderate IA)
8. A11y Empowerment: 6/10 (compliance-plus)
9. Error Handling: 5/5 (proactive strategy)
10. Responsive: 5/5 (desktop-first documented)
11. Brand Consistency: 3/3 (innovator archetype)
12. Inclusive Design: 0.5/2 (1 demographic)

**DQS**: (10 + 8 + 12 + 10 + 5 + 15 + 8 + 6 + 5 + 5 + 3 + 0.5) = **87.5/100** ✅ GOOD

---

## Remediation Guidelines

### DQS < 70 (FAIL)

**Immediate Actions**:
1. Identify dimensions with score < 60% (failing dimensions)
2. Prioritize by weight (fix Usability Testing, Flow Docs, Accessibility first)
3. Create remediation tasks for each failing dimension
4. Re-validate after fixes

**Common Remediation Steps**:
- **Token Completeness**: Generate missing tokens from design questionnaire answers
- **Component Docs**: Add Storybook stories with props tables
- **Accessibility**: Run WCAG audit, add ARIA labels, test with screen readers
- **Consistency**: Refactor hardcoded values to use design tokens
- **Usability Testing**: Create test plan with scenarios, recruit participants
- **Flow Documentation**: Create Mermaid diagrams for user journeys
- **A11y Empowerment**: Add inclusive design patterns, test with disabled users
- **Error Handling**: Add inline validation, improve error messages
- **Brand Consistency**: Align visual style with brand archetype, update microcopy tone

---

## Integration with Design Command

The Design Quality Validator agent (`design-quality-validator` role in `/speckit.design`) automatically calculates DQS v2.0 during design spec validation.

**Validation Trigger**: Wave 5 (Quality Validation) in design command orchestration

**Output Format**:
```markdown
## Design Quality Score (DQS v2.0)

**Overall Score**: 87.5/100 ✅ GOOD

### Dimension Breakdown

| Dimension | Score | Weight | Weighted | Status |
|-----------|-------|--------|----------|--------|
| Token Completeness | 10/10 | 10% | 10.0 | ✅ PASS |
| Component Documentation | 8/8 | 8% | 8.0 | ✅ PASS |
| Accessibility Compliance | 12/12 | 12% | 12.0 | ✅ PASS |
| Consistency | 10/10 | 10% | 10.0 | ✅ PASS |
| Figma Export Quality | 5/5 | 5% | 5.0 | ✅ PASS |
| Usability Testing Plan | 15/15 | 15% | 15.0 | ✅ PASS |
| User Flow Documentation | 8/15 | 15% | 8.0 | ⚠️ PASS |
| Accessibility Empowerment | 6/10 | 10% | 6.0 | ✅ PASS |
| Error Handling UX | 5/5 | 5% | 5.0 | ✅ PASS |
| Responsive Completeness | 5/5 | 5% | 5.0 | ✅ PASS |
| Brand Consistency | 3/3 | 3% | 3.0 | ✅ PASS |
| Inclusive Design | 0.5/2 | 2% | 0.5 | ⚠️ PASS |

**Quality Gate**: QG-DQS-001 ✅ PASS (>= 70)

### Recommendations

1. **Flow Documentation** (8/15): Add complex navigation patterns for multi-level IA
2. **Inclusive Design** (0.5/2): Add patterns for global-audience demographic
```

---

## Changelog

### v2.0 (2026-01-11)

**Added**:
- 7 new dimensions: Usability Testing Plan, User Flow Documentation, Accessibility Empowerment, Error Handling UX, Responsive Completeness, Brand Consistency, Inclusive Design
- Constitution integration: Read UX quality settings from `design_system.ux_quality`
- Constitution integration: Read brand/audience settings from `design_system.brand_audience`
- Conditional scoring: Responsive dimension auto-awards 5pts for non-Web apps
- Conditional scoring: Inclusive Design auto-awards 2pts if no demographics specified

**Changed**:
- Total dimensions: 5 → 12
- Weight rebalancing: Baseline dimensions reduced from 100% to 45%, added UX Quality (35%) and Brand (5%)
- Pass threshold: Maintained at DQS >= 70 (QG-DQS-001)

**Removed**:
- None (backward compatible with v1.0 scoring)

### v1.0 (2025-10-15)

- Initial release with 5 baseline dimensions

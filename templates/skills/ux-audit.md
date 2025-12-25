---
description: Audit a specification for UXQ domain compliance and user experience quality
---

## User Input

```text
$ARGUMENTS
```

## Purpose

This skill audits a feature specification against UXQ (User Experience Quality) domain principles. It identifies gaps in user-centered design documentation and provides actionable recommendations.

## Prerequisites

- `specs/[feature]/spec.md` must exist
- UXQ domain should be active in `memory/constitution.domain.md`

## Execution Steps

### 1. Load Specification

Read the target spec file:
- If argument provided: use that path
- Otherwise: find most recent spec in `specs/`

### 2. UXQ Principle Checklist

Validate against each UXQ principle:

#### UXQ-001: Mental Model Alignment (MUST)
```text
CHECK:
- [ ] "User Mental Model" section exists
- [ ] User vocabulary used (not technical jargon)
- [ ] Workflows match user expectations

VIOLATIONS:
- Technical terms in user-facing descriptions
- Database/API names exposed to users
- Developer-centric error messages
```

#### UXQ-003: Friction Justification (MUST)
```text
CHECK:
- [ ] "Friction Points" table exists
- [ ] Every FP-xxx has Justification column filled
- [ ] Every FP-xxx has Mitigation strategy

VIOLATIONS:
- Unjustified confirmation dialogs
- Unnecessary steps without rationale
- Missing mitigation strategies
```

#### UXQ-005: Error Empathy (MUST)
```text
CHECK:
- [ ] Error scenarios include user perspective
- [ ] Errors explain what user can do next
- [ ] No system-centric error messages

VIOLATIONS:
- "500 Internal Server Error" without explanation
- Technical stack traces exposed
- No recovery guidance
```

#### UXQ-006: FTUE Documentation (MUST)
```text
CHECK:
- [ ] "First-Time User Experience" section exists
- [ ] Empty states documented
- [ ] Progressive disclosure described
- [ ] First meaningful action defined

VIOLATIONS:
- No FTUE section
- Generic "getting started" without specifics
- No empty state handling
```

#### UXQ-008: JTBD Tracing (MUST)
```text
CHECK:
- [ ] "Jobs to Be Done" table exists
- [ ] Each JTBD uses "When/I want/So I can" format
- [ ] Every FR traces to at least one JTBD

VIOLATIONS:
- FR without user value connection
- Missing JTBD table
- Vague job statements
```

#### UXQ-010: Accessibility as Empowerment (MUST)
```text
CHECK:
- [ ] Accessibility section exists
- [ ] WCAG conformance level specified
- [ ] Framed as empowerment, not compliance
- [ ] Specific assistive tech mentioned

VIOLATIONS:
- "WCAG compliant" without specifics
- Accessibility as afterthought
- No empowerment framing
```

### 3. SHOULD Principles (Advisory)

#### UXQ-002: Emotional Journey
- Check for emotional annotations in user journeys
- Suggest adding frustration/delight markers

#### UXQ-004: Delight Moments
- Check for success state celebrations
- Suggest delight opportunities

#### UXQ-007: Context Awareness
- Check multi-device considerations
- Suggest mobile/desktop adaptations

#### UXQ-009: Persona Integration
- Check persona references in features
- Suggest persona-specific prioritization

### 4. Generate Audit Report

Output format:

```markdown
# UXQ Audit Report

**Spec**: [SPEC_PATH]
**Date**: [DATE]
**Domain**: UXQ (User Experience Quality)

## Compliance Summary

| Principle | Level | Status | Issues |
|-----------|-------|--------|--------|
| UXQ-001 Mental Model | MUST | ✅/❌ | [count] |
| UXQ-003 Friction | MUST | ✅/❌ | [count] |
| UXQ-005 Error Empathy | MUST | ✅/❌ | [count] |
| UXQ-006 FTUE | MUST | ✅/❌ | [count] |
| UXQ-008 JTBD | MUST | ✅/❌ | [count] |
| UXQ-010 A11y | MUST | ✅/❌ | [count] |

**MUST Compliance**: X/6 passing
**Overall Score**: X%

## Critical Issues (MUST violations)

### [PRINCIPLE]: [Issue Title]
- **Location**: [section/line]
- **Problem**: [description]
- **Fix**: [recommendation]

## Recommendations (SHOULD improvements)

### [PRINCIPLE]: [Suggestion]
- **Benefit**: [why this matters]
- **Example**: [how to implement]

## Next Steps

1. Fix all MUST violations before proceeding
2. Consider SHOULD improvements for better UX
3. Run `/speckit.analyze` for full validation
```

## Output

- Audit report displayed inline
- Optionally save to `specs/[feature]/uxq-audit.md`
- List of actionable fixes

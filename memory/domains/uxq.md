# Domain Extension: User Experience Quality (Layer 1)

**Extends**: constitution.base.md v1.0
**Context**: Product design, UX, User research, Human-centered design
**Typical Projects**: B2C applications, dashboards, onboarding flows, forms, consumer products

---

## Key Concepts

- **Mental Model**: User's internal representation of how a system works
- **JTBD (Jobs to Be Done)**: The progress a user is trying to make in a given circumstance
- **Friction**: Any obstacle that slows user progress toward their goal
- **Delight Moment**: An unexpected positive experience that exceeds expectations
- **FTUE (First-Time User Experience)**: The initial interaction sequence for new users
- **A11y (Accessibility)**: Design enabling use by people with diverse abilities

---

## Strengthened Principles

These base principles are elevated for UX-focused projects:

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| ERR-001 | MUST (handle gracefully) | MUST (user-centric) | Errors MUST explain what happened AND what to do next |
| DOC-002 | SHOULD | MUST | User-facing documentation is not optional |
| CMP-004 | SHOULD | MUST | Accessibility is a feature, not a checkbox |

---

## Additional Principles

### UXQ-001: Mental Model Alignment

**Level**: MUST
**Applies to**: All user-facing features

Features MUST align with user mental models. Terminology MUST match user vocabulary, not internal jargon. Workflows MUST follow user expectations, not system architecture.

**Validation**: Review feature against documented user mental models
**Violations**: HIGH - User confusion, increased support burden

---

### UXQ-002: Emotional Journey Mapping

**Level**: SHOULD
**Applies to**: Core user journeys

Key user journeys SHOULD document emotional states at each step. Negative emotions (frustration, anxiety, confusion) SHOULD trigger design review. Transition points SHOULD be analyzed for emotional impact.

**Validation**: Check for emotional annotations in user journey documentation
**Violations**: MEDIUM - Missed optimization opportunities

---

### UXQ-003: Friction Justification

**Level**: MUST
**Applies to**: All points of user friction

Every friction point MUST be explicitly justified. Friction without justification MUST be eliminated. Justified friction MUST document: (1) why it exists, (2) what value it provides, (3) how it's minimized.

**Validation**: Audit friction points for documented justifications
**Violations**: HIGH - Unnecessary user burden, abandonment risk

---

### UXQ-004: Delight Moments

**Level**: SHOULD
**Applies to**: Success states and milestones

Success states SHOULD include delight opportunities. Milestones SHOULD be celebrated appropriately. Positive feedback SHOULD reinforce desired behaviors.

**Validation**: Review success flows for delight elements
**Violations**: LOW - Missed engagement opportunity

---

### UXQ-005: Error Empathy

**Level**: MUST
**Applies to**: All error states

Error messages MUST be written from user perspective, not system perspective. Errors MUST explain: (1) what went wrong in user terms, (2) why it matters to the user, (3) what the user can do next. Technical details MUST be secondary or hidden.

**Validation**: Review error messages for user empathy
**Violations**: HIGH - User frustration, support escalation

---

### UXQ-006: First-Time User Experience

**Level**: MUST
**Applies to**: All user-facing features

FTUE MUST be documented separately from repeat-use flows. First-time users MUST receive appropriate guidance. Progressive disclosure MUST prevent overwhelm. Empty states MUST guide toward first meaningful action.

**Validation**: Verify FTUE section exists and describes onboarding
**Violations**: HIGH - New user abandonment

---

### UXQ-007: Context Awareness

**Level**: SHOULD
**Applies to**: Multi-device, multi-context features

Features SHOULD adapt to user context (device, time, location, state). Mobile-first features SHOULD consider touch, connectivity, and interruption. Desktop features SHOULD leverage larger screens and precision input.

**Validation**: Review context-specific behaviors documented
**Violations**: MEDIUM - Suboptimal experience in specific contexts

---

### UXQ-008: Jobs-to-Be-Done Tracing

**Level**: MUST
**Applies to**: All functional requirements

Each functional requirement MUST trace to a user JTBD. Features without clear JTBD MUST be questioned. JTBD statements MUST follow format: "When [situation], I want to [motivation], so I can [outcome]."

**Validation**: Check FR traceability to JTBD statements
**Violations**: HIGH - Feature may not deliver user value

---

### UXQ-009: Persona Integration

**Level**: SHOULD
**Applies to**: Feature specifications

Features SHOULD reference specific personas. Different personas MAY have different feature priorities. Persona conflicts SHOULD be explicitly resolved.

**Validation**: Check persona references in feature specs
**Violations**: MEDIUM - Generic design, missed optimization

---

### UXQ-010: Accessibility as Empowerment

**Level**: MUST
**Applies to**: All user interfaces

Accessibility MUST be framed as expanding user capabilities, not compliance. A11y requirements MUST be specific (WCAG level, screen reader support, keyboard navigation). Accessible alternatives MUST provide equivalent experience, not degraded fallback.

**Validation**: Review accessibility section for empowerment framing
**Violations**: HIGH - Exclusionary design, legal risk

---

## Summary

| Type | Count |
|------|-------|
| Strengthened from base | 3 |
| New MUST principles | 6 |
| New SHOULD principles | 4 |
| **Total additional requirements** | **13** |

---

## Usage

To apply this domain extension:

```bash
cp memory/domains/uxq.md memory/constitution.domain.md
```

Then customize `memory/constitution.md` for project-specific overrides.

### When to Use

Apply UXQ domain when:
- Building consumer-facing (B2C) products
- Developing dashboards or data visualization tools
- Creating onboarding or wizard flows
- Designing form-heavy applications
- Working on products where UX is a key differentiator

### Combining with Other Domains

UXQ can be combined with other domains:
- **UXQ + SaaS**: Multi-tenant apps with consumer-grade UX
- **UXQ + Healthcare**: Patient-facing health applications
- **UXQ + E-commerce**: Shopping experiences

When combining, the stricter principle level applies.

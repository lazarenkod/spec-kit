# Technology Radar Template

> **Purpose**: Track and communicate technology adoption decisions across the organization.
> **When to Use**: Quarterly review of technology landscape and strategic direction.
> **Inspiration**: Based on ThoughtWorks Technology Radar methodology.

---

## Radar Metadata

| Field | Value |
|-------|-------|
| **Organization** | [Company Name] |
| **Radar Version** | [YYYY-QX, e.g., 2024-Q1] |
| **Owner** | [CTO / Architecture Team] |
| **Last Updated** | [YYYY-MM-DD] |
| **Review Cadence** | [Quarterly] |

---

## Radar Visualization

```
                         ADOPT
                           │
              ┌────────────┼────────────┐
             ╱              │              ╲
            ╱    TRIAL      │      TRIAL    ╲
           ╱                │                ╲
          ╱    ┌────────────┼────────────┐    ╲
         ╱    ╱              │              ╲    ╲
        ╱    ╱     ASSESS    │    ASSESS     ╲    ╲
       ╱    ╱                │                ╲    ╲
      ╱    ╱    ┌────────────┼────────────┐    ╲    ╲
     ╱    ╱    ╱              │              ╲    ╲    ╲
    ╱    ╱    ╱      HOLD     │     HOLD      ╲    ╲    ╲
   ╱    ╱    ╱                │                ╲    ╲    ╲
   ─────────────────────────────────────────────────────────
   │ Techniques │ Tools │ Platforms │ Languages │ Frameworks│
```

---

## Ring Definitions

| Ring | Definition | Action | Risk Level |
|------|------------|--------|------------|
| **ADOPT** | Proven, recommended for broad use | Use by default for new projects | Low |
| **TRIAL** | Worth pursuing, understood tradeoffs | Use in non-critical projects, build expertise | Medium |
| **ASSESS** | Worth exploring, not yet proven | Research, proof-of-concept only | Medium-High |
| **HOLD** | Proceed with caution, issues identified | Do not start new work, plan migration | Variable |

---

## Quadrants

| Quadrant | Description |
|----------|-------------|
| **Techniques** | Processes, methodologies, practices |
| **Tools** | Development tools, IDEs, automation |
| **Platforms** | Infrastructure, cloud, databases |
| **Languages & Frameworks** | Programming languages, major frameworks |

---

## Current Radar

### Techniques

#### ADOPT ✅
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Technique 1] | [Brief description] | [YYYY-QX] | [Why we adopt this] |
| [Technique 2] | [Brief description] | [YYYY-QX] | [Why we adopt this] |

#### TRIAL 🔵
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Technique 3] | [Brief description] | [YYYY-QX] | [What we're learning] |

#### ASSESS 🟡
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Technique 4] | [Brief description] | [YYYY-QX] | [Why assessing] |

#### HOLD 🔴
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Technique 5] | [Brief description] | [YYYY-QX] | [Why on hold] |

---

### Tools

#### ADOPT ✅
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Tool 1] | [Brief description] | [YYYY-QX] | [Why we adopt this] |

#### TRIAL 🔵
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Tool 2] | [Brief description] | [YYYY-QX] | [What we're learning] |

#### ASSESS 🟡
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Tool 3] | [Brief description] | [YYYY-QX] | [Why assessing] |

#### HOLD 🔴
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Tool 4] | [Brief description] | [YYYY-QX] | [Why on hold] |

---

### Platforms

#### ADOPT ✅
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Platform 1] | [Brief description] | [YYYY-QX] | [Why we adopt this] |

#### TRIAL 🔵
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Platform 2] | [Brief description] | [YYYY-QX] | [What we're learning] |

#### ASSESS 🟡
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Platform 3] | [Brief description] | [YYYY-QX] | [Why assessing] |

#### HOLD 🔴
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Platform 4] | [Brief description] | [YYYY-QX] | [Why on hold] |

---

### Languages & Frameworks

#### ADOPT ✅
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Lang/Framework 1] | [Brief description] | [YYYY-QX] | [Why we adopt this] |

#### TRIAL 🔵
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Lang/Framework 2] | [Brief description] | [YYYY-QX] | [What we're learning] |

#### ASSESS 🟡
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Lang/Framework 3] | [Brief description] | [YYYY-QX] | [Why assessing] |

#### HOLD 🔴
| Technology | Description | Since | Notes |
|------------|-------------|-------|-------|
| [Lang/Framework 4] | [Brief description] | [YYYY-QX] | [Why on hold] |

---

## Detailed Blips

### [Technology Name]

**Ring**: [ADOPT | TRIAL | ASSESS | HOLD]

**Quadrant**: [Techniques | Tools | Platforms | Languages & Frameworks]

**Status Change**: [New | Moved In | Moved Out | No Change]

**Previous Ring**: [If changed, what was it before]

#### Summary
[2-3 sentence summary of what this technology is and why it matters]

#### Our Experience
[What we've learned from using/evaluating this technology]

#### Strengths
- ✅ [Strength 1]
- ✅ [Strength 2]
- ✅ [Strength 3]

#### Weaknesses/Risks
- ⚠️ [Weakness 1]
- ⚠️ [Weakness 2]

#### Use Cases
- ✅ **Good for**: [Use case 1], [Use case 2]
- ❌ **Not for**: [Anti use case 1], [Anti use case 2]

#### Alternatives Considered
| Alternative | Why Not Chosen |
|-------------|----------------|
| [Alternative 1] | [Reason] |
| [Alternative 2] | [Reason] |

#### Resources
- [Link to internal documentation]
- [Link to getting started guide]
- [Link to proof of concept]

---

## Movement Summary

### Changes This Quarter

| Technology | Previous | Current | Reason |
|------------|----------|---------|--------|
| [Tech 1] | TRIAL | ADOPT | [Why promoted] |
| [Tech 2] | ASSESS | TRIAL | [Why promoted] |
| [Tech 3] | ADOPT | HOLD | [Why demoted] |
| [Tech 4] | - | ASSESS | [Why added] |

### New Additions

| Technology | Ring | Quadrant | Rationale |
|------------|------|----------|-----------|
| [Tech 1] | [Ring] | [Quadrant] | [Why added to radar] |
| [Tech 2] | [Ring] | [Quadrant] | [Why added to radar] |

### Removals

| Technology | Last Ring | Quadrant | Reason for Removal |
|------------|-----------|----------|-------------------|
| [Tech 1] | [Ring] | [Quadrant] | [Why removed - deprecated, superseded, etc.] |

---

## Strategic Themes

### Theme 1: [Theme Name, e.g., "Cloud-Native by Default"]

**Description**: [What this theme means for technology choices]

**Related Technologies**:
- [Technology in ADOPT that supports this]
- [Technology in TRIAL that supports this]

**Anti-Patterns to Avoid**:
- [Technology in HOLD that conflicts with this]

---

### Theme 2: [Theme Name, e.g., "Developer Experience First"]

**Description**: [What this theme means for technology choices]

**Related Technologies**:
- [Technology in ADOPT that supports this]
- [Technology in TRIAL that supports this]

---

## Decision Framework

### How to Use This Radar

#### Starting a New Project

1. **Check ADOPT ring first**: Use these technologies by default
2. **Consider TRIAL for non-critical components**: Build expertise
3. **Avoid HOLD technologies**: Don't introduce new dependencies
4. **Get approval for ASSESS**: Proof of concept only

#### Proposing New Technology

```
┌─────────────────────────────────────────────────┐
│  1. Is there an ADOPT option that works?        │
│     YES → Use it                                │
│     NO  → Continue                              │
├─────────────────────────────────────────────────┤
│  2. Is there a TRIAL option that fits?          │
│     YES → Consider it, discuss with team        │
│     NO  → Continue                              │
├─────────────────────────────────────────────────┤
│  3. Submit for ASSESS consideration:            │
│     - Problem statement                         │
│     - Why current options don't work            │
│     - Proof of concept plan                     │
│     - Team capacity to evaluate                 │
├─────────────────────────────────────────────────┤
│  4. Architecture review approves/rejects        │
└─────────────────────────────────────────────────┘
```

#### Moving Technologies Between Rings

| From | To | Requirements |
|------|----|-------------|
| ASSESS | TRIAL | PoC completed, identified use case, team capacity |
| TRIAL | ADOPT | Production use, positive outcomes, documented patterns |
| Any | HOLD | Identified issues, migration path documented |

---

## Evaluation Criteria

### Criteria for Ring Placement

| Criterion | ADOPT | TRIAL | ASSESS | HOLD |
|-----------|-------|-------|--------|------|
| Production experience | Extensive | Some | None | N/A |
| Team expertise | Deep | Growing | Learning | N/A |
| Ecosystem maturity | Mature | Maturing | Emerging | Declining |
| Vendor/community support | Strong | Good | Uncertain | Weak |
| Security posture | Verified | Under review | Unknown | Concerns |
| Total cost | Understood | Estimated | Unknown | High |

### Technology Assessment Template

When proposing a new technology for the radar, answer:

1. **Problem**: What problem does this solve?
2. **Alternatives**: What existing options did we consider?
3. **Differentiation**: Why is this better than alternatives?
4. **Experience**: Do we have experience with it?
5. **Risk**: What are the risks of adoption?
6. **Investment**: What's the cost to adopt (time, money, learning)?
7. **Exit Strategy**: How would we migrate away if needed?

---

## Governance

### Radar Review Process

**Frequency**: Quarterly

**Participants**:
- CTO/VP Engineering
- Architecture Team
- Tech Leads
- Security Representative

**Agenda**:
1. Review technologies that moved (promotions/demotions)
2. Discuss new technologies proposed
3. Review HOLD technologies for migration progress
4. Update strategic themes

### Submission Process

1. **Anyone can propose** a technology for consideration
2. **Submit via**: [Submission form/channel]
3. **Include**: Problem, use case, initial evaluation
4. **Review**: Architecture team evaluates monthly
5. **Decision**: Announced in quarterly radar update

---

## Migration Tracking

### Technologies on HOLD

| Technology | HOLD Since | Migration Target | Progress | Owner |
|------------|------------|------------------|----------|-------|
| [Tech 1] | [YYYY-QX] | [Replacement] | [XX%] | [Team] |
| [Tech 2] | [YYYY-QX] | [Replacement] | [XX%] | [Team] |

### Migration Milestones

**[Technology Being Replaced]** → **[Replacement Technology]**

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Replacement selected | [Date] | ✅ Complete |
| Migration guide created | [Date] | ✅ Complete |
| First service migrated | [Date] | 🔄 In Progress |
| 50% services migrated | [Date] | ⏳ Planned |
| 100% services migrated | [Date] | ⏳ Planned |
| Old technology deprecated | [Date] | ⏳ Planned |

---

## Appendix

### Historical Radar Versions

| Version | Date | Major Changes |
|---------|------|---------------|
| [YYYY-Q4] | [Date] | [Summary of key changes] |
| [YYYY-Q3] | [Date] | [Summary of key changes] |
| [YYYY-Q2] | [Date] | [Summary of key changes] |
| [YYYY-Q1] | [Date] | [Summary of key changes] |

### Resources

- [Link to interactive radar visualization]
- [Link to submission form]
- [Link to full evaluation criteria]
- [Link to ThoughtWorks Radar for inspiration]

---

# Tech Radar Quality Checklist

## Completeness
- [ ] All four rings populated (ADOPT, TRIAL, ASSESS, HOLD)
- [ ] All four quadrants covered
- [ ] Movement summary shows changes
- [ ] Strategic themes align with business goals

## Clarity
- [ ] Each blip has clear rationale
- [ ] HOLD technologies have migration plans
- [ ] Decision framework is documented
- [ ] Team knows how to propose new technologies

## Actionability
- [ ] ADOPT ring guides default choices
- [ ] TRIAL technologies have owners
- [ ] ASSESS technologies have PoC plans
- [ ] HOLD technologies have exit timelines

## Currency
- [ ] Reviewed within last quarter
- [ ] Reflects actual organizational usage
- [ ] Includes emerging relevant technologies
- [ ] Removes obsolete entries

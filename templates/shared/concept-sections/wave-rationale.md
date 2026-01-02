# Wave Rationale

> **Purpose**: Explain WHY features are grouped in each wave and what dependency chains determined the order. Eliminates confusion about "why can't we build X first?".

## Integration Notes

- **Depends on**: Feature Hierarchy, Cross-Feature Dependencies, selection-rationale.md
- **Feeds into**: Execution Order section, Implementation Planning
- **CQS Impact**: Transparency component — Wave rationale criterion (20 points)

---

## Wave Rationale Framework

### Wave Purpose Definitions

| Wave | Purpose | Typical Contents | Exit Criteria |
|:----:|---------|------------------|---------------|
| **Wave 1** | Foundation Layer | Auth, Core Data, Layout, Infrastructure | Can create authenticated user session |
| **Wave 2** | Experience Layer | Navigation, Onboarding, Feedback, Admin basics | Golden Path testable end-to-end |
| **Wave 3** | Business Value | Core features delivering primary JTBD | User can achieve primary goal |
| **Wave 4+** | Enhancement & Expansion | Secondary JTBD, new segments, platform features | Incremental value delivery |

### Wave Assignment Criteria

Features are assigned to waves based on:

1. **Technical Dependencies**: What must exist for this feature to work?
2. **Logical Coherence**: Does this feature form a complete capability with others in the wave?
3. **User Journey Enablement**: Which wave must complete before user can accomplish goal?
4. **Risk Sequencing**: Are higher-risk features in later waves (validate foundations first)?

---

## Template: Wave Rationale Section

```markdown
## Execution Order

<!--
  This section explains not just WHEN features are built (wave assignment)
  but WHY they're grouped together and what drives the sequencing.
-->

### Wave 1: Foundation Layer

| Feature ID | Name | Priority | Status | Blocks |
|------------|------|----------|--------|--------|
| [EPIC-001.F01] | [Feature] | P1a | [ ] | [What it blocks] |
| [EPIC-001.F02] | [Feature] | P1a | [ ] | [What it blocks] |

**Wave 1 Completion Gate**: [Specific capability that must exist]

#### Wave 1 Rationale

**Why these features are grouped together**:
- [Technical dependency explanation — e.g., "All require database schema to exist"]
- [Logical coherence — e.g., "Together enable basic user session"]
- [Risk rationale — e.g., "Validates core technical assumptions early"]

**What blocks Wave 2**:
- [ ] [Specific capability — e.g., "User can authenticate"]
- [ ] [API/Data requirement — e.g., "User entity exists in database"]
- [ ] [Infrastructure — e.g., "Error handling framework operational"]

**Alternative groupings considered**:

| Alternative | Why Not Chosen |
|-------------|----------------|
| [Split auth and user mgmt into separate waves] | [Would create integration risk — auth depends on user entity] |
| [Move navigation to Wave 1] | [Navigation useless without content to navigate to] |

**Dependencies from this wave**:
```text
EPIC-001.F01 (User Registration)
    ↓ creates user entity
EPIC-001.F02 (Authentication)
    ↓ requires user entity, enables
ALL Wave 2+ features (require auth session)
```

---

### Wave 2: Experience Layer

| Feature ID | Name | Priority | Status | Blocks |
|------------|------|----------|--------|--------|
| [EPIC-001.F03] | [Feature] | P1b | [ ] | [What it blocks] |

**Wave 2 Completion Gate**: Golden Path must be testable.

#### Wave 2 Rationale

**Why these features are grouped together**:
- [All require Wave 1 foundation (auth, layout) to function]
- [Together enable minimum viable user experience]
- [Form logical set: user can navigate, get feedback, start journey]

**What blocks Wave 3**:
- [ ] [User must be able to complete basic journey]
- [ ] [Feedback mechanisms must exist for iteration]
- [ ] [Admin must be able to configure core settings]

**Dependency chain visualization**:
```text
Wave 1 (Foundation) → Wave 2 (Experience) → Wave 3 (Business Value)
     ↓                      ↓                      ↓
 Auth exists         User can navigate      User achieves goal
 Data schema         Gets feedback          Primary JTBD fulfilled
 Layout shell        Onboarding complete    Differentiation visible
```

---

### Wave 3+: Business Features

| Feature ID | Name | Priority | Wave | Depends On | Status |
|------------|------|----------|------|------------|--------|
| [EPIC-002.F01] | [Feature] | P1a | 3 | [Dependencies] | [ ] |
| [EPIC-002.F02] | [Feature] | P1b | 3 | [Dependencies] | [ ] |
| [EPIC-003.F01] | [Feature] | P2a | 4 | [Dependencies] | [ ] |

#### Wave 3+ Rationale

**Why Wave 3 features wait**:
- [Require Golden Path to be testable first]
- [Business value depends on user activation (Wave 2)]
- [Need feedback from Wave 2 to validate assumptions]

**Wave 3 vs Wave 4 distinction**:

| Wave | Theme | Why This Order |
|:----:|-------|----------------|
| 3 | Core business value | Directly addresses primary functional JTBD |
| 4 | Enhancement | Builds on Wave 3 data/patterns, addresses secondary JTBD |
| 5+ | Expansion | New personas, markets, platforms |

**Features deliberately pushed to later waves**:

| Feature | Could Be Earlier? | Why Delayed |
|---------|:-----------------:|-------------|
| [Feature X] | Yes | [Risk reduction — validate Wave 3 first] |
| [Feature Y] | No | [Hard dependency on Wave 3 data] |
| [Feature Z] | Yes | [Resource constraint — team capacity] |

**Wave 4+ triggers** (when to start next wave):
- [ ] Wave 3 features stable (no critical bugs)
- [ ] Core metrics trending positive (validation)
- [ ] User feedback confirms direction
- [ ] Resources available

```

---

## Validation Checklist

Before finalizing Wave Rationale:

- [ ] Every wave has "Why grouped together" explanation
- [ ] Every wave has "What blocks next wave" checklist
- [ ] At least one alternative grouping documented per major wave
- [ ] Dependency chain visualized (text or mermaid)
- [ ] Wave 3 vs Wave 4 distinction explained
- [ ] "Could be earlier" analysis for delayed features
- [ ] Wave completion gates are specific and verifiable

---

## Common Wave Rationale Patterns

### Pattern 1: Foundation-First

```text
Wave 1: Authentication + Core Entities + Error Handling
Rationale: "Nothing works without identity and data foundation"

Wave 2: Navigation + Feedback + Basic Admin
Rationale: "User needs to move around and see results"

Wave 3: Primary Business Features
Rationale: "Now user can accomplish their goal"
```

### Pattern 2: Risk-Ordered

```text
Wave 1: Highest technical risk features
Rationale: "Validate feasibility before building dependent features"

Wave 2: Medium risk features that depend on Wave 1 validation
Rationale: "Wave 1 proved approach works"

Wave 3: Lower risk features (proven patterns)
Rationale: "Foundation stable, can execute confidently"
```

### Pattern 3: User Journey-Ordered

```text
Wave 1: Features for journey steps 1-2 (arrive, orient)
Wave 2: Features for journey steps 3-4 (engage, act)
Wave 3: Features for journey steps 5-6 (achieve, return)
```

---

## Integration with Other Sections

### Feature Hierarchy Enhancement

Each feature in Feature Hierarchy gains wave assignment:

```markdown
#### Feature: [EPIC-001.F01] User Registration

**Description**: [Description]
**Priority**: P1a
**Wave**: 1 (Foundation)
**Wave Rationale**: Required for all authenticated features
```

### Cross-Feature Dependencies

Wave Rationale should align with dependency matrix:

```markdown
| Feature | Depends On | Wave | Rationale |
|---------|------------|:----:|-----------|
| F01 | - | 1 | Foundation |
| F02 | F01 | 1 | Same wave (tightly coupled) |
| F03 | F01, F02 | 2 | Experience layer |
```

### CQS Scoring Integration

Wave Rationale contributes to Transparency component:

| Criterion | Points | Check |
|-----------|:------:|-------|
| Wave rationale for each wave | 20 | All waves have "Why grouped" explanation |
| Alternative groupings documented | 10 | At least 1 per major wave |
| Dependency chain visualized | 10 | Text or mermaid diagram present |

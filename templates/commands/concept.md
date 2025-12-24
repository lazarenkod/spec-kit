---
description: Capture complete service concept before detailed specification. Creates hierarchical feature breakdown with full traceability. Use BEFORE /speckit.specify for large projects (50+ requirements).
handoffs:
  - label: Create Specification
    agent: speckit.specify
    prompt: Generate detailed specification from concept for stories
    send: true
  - label: Validate Concept
    agent: speckit.analyze
    prompt: Check concept completeness and consistency
claude_code:
  reasoning_mode: extended
  thinking_budget: 10000
  plan_mode_trigger: true
  subagents:
    - role: market-researcher
      trigger: "when exploring competitors, market trends, or user pain points"
      prompt: "Research market landscape for {DOMAIN}: competitors, trends, user complaints"
    - role: design-researcher
      trigger: "when exploring UI patterns or user experience approaches"
      prompt: "Research UI/UX patterns and best practices for {DOMAIN}"
scripts:
  sh: scripts/bash/create-concept.sh --json "{ARGS}"
  ps: scripts/powershell/create-concept.ps1 -Json "{ARGS}"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

This command captures the **complete vision and scope** of a service/product BEFORE breaking it into detailed specifications. It prevents idea loss by:

1. Structuring all features in an Epic > Feature > Story hierarchy
2. Mapping user journeys across features
3. Tracking cross-feature dependencies
4. Preserving all ideas (even unvalidated ones) in a backlog

**When to use**:
- Starting a new project from scratch
- Large scope (50+ requirements expected)
- Multiple interconnected features
- When you need to preserve the full vision before detailing

## Outline

1. **Initialize concept document**:
   - Run script `{SCRIPT}` to create `specs/concept.md`
   - The script creates the file from `templates/concept-template.md`
   - If `specs/concept.md` already exists, the script returns its path (no overwrite)

2. **Mode Detection** (determine Discovery vs Capture mode):

   Analyze user input for discovery signals:

   **Discovery Mode triggers** (any match activates):
   - Vague descriptors: "something like", "maybe", "возможно", "не знаю точно", "типа"
   - Open questions: "what if", "should I", "как лучше", "что если"
   - Competitor mentions without differentiation: "like Trello but...", "как X только лучше"
   - Single-sentence descriptions without specific features
   - Uncertainty markers: "I think", "probably", "наверное"

   **Capture Mode triggers** (skip to step 5):
   - Structured feature lists with 3+ items
   - Specific user personas mentioned by name/role
   - Concrete metrics or KPIs stated
   - Clear differentiation articulated
   - Technical requirements specified

   ```text
   IF Discovery Mode triggered:
     → Execute Phase 0a, 0b, 0c (steps 3-4)
   ELSE IF Capture Mode triggered:
     → Skip to step 5 (Extract Vision)
   ELSE (ambiguous):
     → Ask user: "Would you like to brainstorm and research first, or do you have a clear concept ready?"
   ```

3. **Phase 0: Discovery Mode** (if triggered):

   ### Phase 0a: Problem Discovery (Brainstorming)

   **Goal**: Help user articulate the real problem before jumping to solutions.

   **Interactive questioning flow** (ask sequentially, adapt based on answers):

   1. **Root Problem Question**:
      "What specific frustration or inefficiency triggered this idea?"
      - Listen for: pain points, workarounds, failed alternatives
      - If answer is vague, probe deeper: "Can you describe a specific moment when this was frustrating?"

   2. **Scale Question**:
      "How many people/companies face this problem? How often does it occur?"
      - Listen for: market size signals, frequency, severity

   3. **Current Solutions Question**:
      "How do people solve this today? What's wrong with those approaches?"
      - Listen for: competitor gaps, differentiation opportunities

   4. **Stakes Question**:
      "What happens if this problem remains unsolved? What's the cost?"
      - Listen for: urgency, willingness to pay, business impact

   5. **Vision Question**:
      "Describe the ideal outcome if this were perfectly solved."
      - Listen for: success criteria, feature hints, user delight moments

   **Output**: Document answers in "Problem Discovery" section of concept.md

   ### Phase 0b: Market & User Research

   **Goal**: Validate problem with external data using web search.

   **Research actions** (use WebSearch tool proactively):

   1. **Competitor Analysis**:
      - Search: "[problem domain] software solutions 2025"
      - Search: "alternatives to [mentioned competitor]"
      - Search: "[competitor name] reviews complaints"
      - Extract: feature comparisons, pricing, user complaints, gaps

   2. **Market Trends**:
      - Search: "[industry/domain] software trends 2025"
      - Search: "[problem] market size TAM"
      - Extract: growth signals, emerging needs, investment activity

   3. **User Pain Points**:
      - Search: "[target user role] workflow challenges"
      - Search: "[domain] frustrations reddit OR hackernews"
      - Extract: unmet needs, feature requests, workaround patterns

   **Output**:
   - Populate "Market Research" section in concept.md
   - Create competitor comparison table
   - Document market gaps and opportunities
   - Include source links for reference

   ### Phase 0c: Solution Ideation

   **Goal**: Generate feature ideas based on discovered problems and market gaps.

   **Structured brainstorming**:

   1. **Value Proposition Canvas**:
      - Pain relievers: Which discovered pains can we address?
      - Gain creators: What new value can we provide?
      - Differentiators: What do competitors miss that we can nail?

   2. **"What If" Scenarios** (generate 5-10):
      - "What if users could [action] without [current friction]?"
      - "What if [competitor feature] worked with [missing integration]?"
      - "What if [manual process] was fully automated?"
      - "What if [expert task] was accessible to [non-experts]?"

   3. **Feature Candidates**:
      - Group "What If" scenarios into potential features
      - Rate each: Impact (High/Medium/Low) × Effort (High/Medium/Low)
      - Mark high-impact, reasonable-effort ideas as winners

   **Output**:
   - Populate "Solution Ideation" section
   - Feed winning ideas into Feature Hierarchy (step 6)
   - Move lower-priority ideas to Ideas Backlog

4. **Transition: Discovery → Structure** (if Discovery Mode was used):

   **Synthesis step** before proceeding to structured capture:

   1. **Summarize discoveries** to user:
      - "Top problems validated: [list]"
      - "Key market gaps identified: [list]"
      - "Winning feature candidates: [list]"

   2. **Synthesize vision statement**:
      "Based on our discovery, here's the emerging concept:
      [draft vision statement combining problem + solution + differentiation]"

   3. **User confirmation**:
      "Does this capture your intent? Any adjustments before we structure the full concept?"

   4. After confirmation, proceed to step 5.

5. **Extract Vision and Business Context** from user input:

   Parse the user description to identify:
   - **Vision Statement**: What is this? Who is it for? What problem does it solve?
   - **Problem Space**: Specific pain points being addressed
   - **Target Users**: Personas with their goals and current frustrations
   - **Success Metrics**: Business KPIs with target values

   For each element:
   - If clearly stated in input: Extract directly
   - If implied: Infer from context and document as assumption
   - If unclear: Use reasonable industry defaults (or use Discovery findings if available)

6. **Build Feature Hierarchy**:

   Analyze the user description to identify capabilities and organize them:

   ```text
   FOR EACH capability mentioned:
     1. Classify as Epic (large area) or Feature (specific functionality)
     2. If capability is too large for single Feature:
        - Create Epic containing multiple Features
     3. Break each Feature into user-facing Stories
     4. Assign hierarchical IDs: EPIC-NNN.FNN.SNN
     5. Assign initial priority based on:
        - Explicitly stated priority from user
        - Dependency order (foundations first)
        - User value (core journey enablers higher)
   ```

   **ID Format Rules**:
   - Epic: `EPIC-001`, `EPIC-002`, etc.
   - Feature: `EPIC-001.F01`, `EPIC-001.F02`, etc.
   - Story: `EPIC-001.F01.S01`, `EPIC-001.F01.S02`, etc.

   **Priority Format**:
   - `P1a`, `P1b`, `P1c`: MVP critical path (ordered sequence)
   - `P2a`, `P2b`: Important but post-MVP
   - `P3`: Nice-to-have, future enhancements

7. **Map User Journeys**:

   Identify end-to-end flows that cross features:

   ```text
   FOR EACH user persona:
     1. Identify primary goal they want to achieve
     2. Map the steps to achieve that goal
     3. Link each step to Feature IDs
     4. Document edge cases per journey
     5. Note where journeys share features (integration points)
   ```

8. **Document Cross-Feature Dependencies**:

   Build dependency matrix:

   ```text
   FOR EACH Feature:
     1. Identify: What must be built BEFORE this feature?
     2. Identify: What does this feature BLOCK?
     3. Note integration points and shared entities
   ```

   Generate Mermaid diagram for visual representation.

9. **Capture Ideas Backlog**:

   **CRITICAL**: No idea should be lost. For each idea that doesn't fit current scope:

   ```markdown
   - [ ] [Idea] - Status: not started
   - [?] [Idea] - Status: needs validation (unclear value/feasibility)
   - [>] [Idea] - Status: deferred to future phase
   - [x] [Idea] - Status: rejected with reason
   ```

   Categories:
   - Potential future Epics
   - Feature enhancement ideas
   - Technical explorations
   - Rejected ideas (preserve rationale)

10. **Initialize Traceability Skeleton**:

   Create empty traceability matrix for each Story:

   | Concept ID | Spec Created | Spec Requirements | Tasks | Tests | Status |
   |------------|--------------|-------------------|-------|-------|--------|
   | [ID] | [ ] | - | - | - | Not started |

   This will be populated by subsequent commands (`/speckit.specify`, `/speckit.tasks`).

11. **Write concept.md** to `specs/concept.md` using template structure.

## Validation Gates

Before completing, verify:

**Core Gates (always required)**:
- [ ] Vision statement is concrete (no vague words like "better", "improved")
- [ ] At least 2 user personas defined with specific goals
- [ ] At least 1 user journey per primary persona
- [ ] All Epics have at least one Feature
- [ ] All Features have at least one Story
- [ ] All Features have unique IDs following the format
- [ ] Dependencies form a DAG (no circular dependencies)
- [ ] Ideas backlog section is populated (even if "No additional ideas")
- [ ] Glossary includes all domain-specific terms

**Discovery Mode Gates** (if Discovery Mode was used):
- [ ] Problem statement refined from initial vague input
- [ ] At least 1 competitor analyzed with strengths/weaknesses
- [ ] At least 3 "What If" scenarios explored
- [ ] Market research sources documented
- [ ] User confirmed synthesized vision before structured capture
- [ ] Discovery findings connected to Feature Hierarchy (winning ideas became features)

## Quality Guidelines

### Hierarchy Best Practices

**Epic Granularity**:
- Too broad: "Core Platform" (meaningless)
- Too narrow: "User Login" (this is a Feature)
- Good: "User Management", "Payment Processing", "Analytics"

**Feature Granularity**:
- Too broad: "Authentication" (could be multiple features)
- Too narrow: "Validate Email Format" (this is implementation detail)
- Good: "User Registration", "Social Login", "Password Reset"

**Story Granularity**:
- Too broad: "User can manage their account" (vague)
- Good: "As a user, I want to update my email address so that I receive notifications at my current address"

### Dependency Mapping

Identify dependencies for:
- Data entities (shared models)
- UI components (shared layouts)
- Business logic (shared services)
- External integrations (API contracts)

### Ideas Backlog

**Do capture**:
- Half-formed ideas
- "What if..." scenarios
- Competitive feature ideas
- User-requested enhancements
- Technical debt considerations

**Don't discard**:
- Ideas that seem "obvious" (document them)
- Ideas that seem "too hard" (mark as needs-validation)
- Ideas outside current scope (mark as deferred)

## Output

After completion:

1. `specs/concept.md` with complete hierarchy
2. Report summary:
   - N Epics, M Features, K Stories captured
   - L Ideas in backlog
   - Dependency graph validated: Yes/No
3. Recommended next steps:
   - Stories ready for specification (P1a priority)
   - Example: `/speckit.specify EPIC-001.F01.S01, EPIC-001.F01.S02`

## Example

**User Input**: "I want to build a task management app where teams can create projects, assign tasks, track time, and generate reports"

**Resulting Hierarchy**:

```text
EPIC-001: User Management (P1)
  F01: Registration (P1a)
    S01: User registers with email
    S02: User verifies email
  F02: Team Management (P1b)
    S01: User creates team
    S02: User invites members

EPIC-002: Project Management (P1)
  F01: Project CRUD (P1a)
    S01: User creates project
    S02: User archives project
  F02: Task Management (P1a)
    S01: User creates task
    S02: User assigns task
    S03: User sets deadline

EPIC-003: Time Tracking (P2)
  F01: Time Entry (P2a)
    S01: User logs time
    S02: User edits time entry

EPIC-004: Reporting (P2)
  F01: Basic Reports (P2b)
    S01: User generates time report

Ideas Backlog:
- [ ] Recurring tasks - potential EPIC-002.F03
- [?] AI task suggestions - needs validation
- [>] Mobile app - deferred to v2.0
```

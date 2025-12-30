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
  model: opus
  reasoning_mode: extended
  thinking_budget: 10000
  plan_mode_trigger: true
skills:
  - name: market-research
    trigger: "Phase 0b: Market & User Research"
    usage: "Read templates/skills/market-research.md for comprehensive competitor and market analysis"
  - name: ux-audit
    trigger: "When validating concept for UX quality"
    usage: "Read templates/skills/ux-audit.md to validate UXQ compliance before specification"
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

0. **Load project language setting**:

   Read `/memory/constitution.md` and extract the `language` value from the Project Settings table.

   ```text
   IF Project Settings section exists AND language row found:
     ARTIFACT_LANGUAGE = extracted value (e.g., "ru", "en", "de")
   ELSE:
     ARTIFACT_LANGUAGE = "en" (default)

   Apply language rules from templates/shared/language-context.md:
   - Generate all prose content in ARTIFACT_LANGUAGE
   - Keep IDs (EPIC-001, F01, S01), technical terms, and code in English
   ```

   Report: "Generating concept in {LANGUAGE_NAME} ({ARTIFACT_LANGUAGE})..."

1. **Initialize concept document**:
   - Run script `{SCRIPT}` to create `specs/concept.md`
   - The script creates the file from `templates/concept-template.md`
   - If `specs/concept.md` already exists, the script returns its path (no overwrite)

2. **Mode Detection** (determine Discovery vs Capture vs Validation mode):

   Analyze user input and existing artifacts for mode signals:

   **Discovery Mode triggers** (any match activates):
   - Vague descriptors: "something like", "maybe", "возможно", "не знаю точно", "типа"
   - Open questions: "what if", "should I", "как лучше", "что если"
   - Competitor mentions without differentiation: "like Trello but...", "как X только лучше"
   - Single-sentence descriptions without specific features
   - Uncertainty markers: "I think", "probably", "наверное"
   - Words related to product vision: "product vision", "product strategy", "product concept"

   **Capture Mode triggers** (skip to step 5):
   - Structured feature lists with 3+ items
   - Specific user personas mentioned by name/role
   - Concrete metrics or KPIs stated
   - Clear differentiation articulated
   - Technical requirements specified

   **Validation Mode triggers** (NEW - for existing concepts needing enhancement):
   - `specs/concept.md` already exists
   - User explicitly asks to "validate", "improve", or "enhance" concept
   - Concept exists but missing key sections:
     - No "Market Opportunity" section (TAM/SAM/SOM missing)
     - No "Risk Assessment" section
     - No "Technical Discovery" section
     - CQS < 60 (if calculable)

   ```text
   IF specs/concept.md exists:
     CHECK for missing sections (Market/Risk/Technical/CQS)
     IF missing sections found OR user asks to validate:
       → Validation Mode: Focus on adding missing sections
       → Ask: "Your concept has features but is missing [market validation/risk assessment/technical hints].
              Would you like to add these now to improve concept quality? (y/n)"
   ELSE IF Discovery Mode triggered:
     → Execute Phase 0a, 0b, 0c (steps 3-4)
   ELSE IF Capture Mode triggered:
     → Skip to step 5 (Extract Vision)
   ELSE (ambiguous):
     → Ask user: "Would you like to brainstorm and research first, or do you have a clear concept ready?"
   ```

2b. **Project Type Detection**:

   Analyze codebase to determine project type and required UX foundations.

   ```text
   INDICATORS = {
     "Web SPA": package.json with React/Vue/Angular/Svelte,
     "Web SSR": package.json with Next.js/Nuxt/SvelteKit,
     "Mobile": ios/ or android/ directories,
     "CLI": --help flag, cli.py, argparse, commander.js,
     "API": openapi.yaml, swagger.json, api/ directory,
     "Desktop": Electron, Tauri indicators,
     "Service": Dockerfile only, no UI
   }

   FOR EACH indicator in INDICATORS:
     IF indicator matches codebase:
       PROJECT_TYPE = indicator.type
       BREAK (use first match by priority)

   # Load required foundations from catalog
   READ memory/knowledge/frameworks/ux-foundations.md
   REQUIRED_FOUNDATIONS = lookup by PROJECT_TYPE

   Report: "Detected project type: {PROJECT_TYPE}"
   Report: "Required UX foundations: {REQUIRED_FOUNDATIONS}"
   ```

   **Project Type Priority** (when multiple match):
   1. Mobile (if ios/ or android/)
   2. Web SSR (if SSR framework)
   3. Web SPA (if SPA framework)
   4. Desktop (if Electron/Tauri)
   5. CLI (if CLI indicators)
   6. API (if OpenAPI/swagger)
   7. Service (fallback)

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

   **Goal**: Validate problem with external data and quantify market opportunity.

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

   4. **Market Sizing (TAM/SAM/SOM)** — NEW:
      - Search: "[industry] market size 2025 report"
      - Search: "[target segment] number of companies/users"
      - Search: "[competitor] pricing revenue"

      Calculate and document:
      ```markdown
      ## Market Opportunity

      ### TAM/SAM/SOM Analysis
      | Metric | Value | Calculation | Source |
      |--------|-------|-------------|--------|
      | **TAM** | $[X]B | [Total market if everyone bought] | [Source] |
      | **SAM** | $[X]M | TAM × [segment/geo filters] | [Source] |
      | **SOM** | $[X]M | SAM × [realistic capture in Y yrs] | [Assumptions] |

      ### Market Validation Signals
      - [ ] Problem validated by customer research
      - [ ] Competitors exist (market is real)
      - [ ] Budget exists (people pay for alternatives)
      - [ ] Timing is right (enabling trends)
      ```

   5. **Competitive Positioning Matrix** — NEW:
      Build comparison against top 3-5 competitors:
      ```markdown
      | Capability | Us | Competitor A | Competitor B | Gap |
      |------------|:--:|:------------:|:------------:|-----|
      | [Feature 1] | ✓+ | ✓ | ✗ | Differentiation |
      | [Feature 2] | ✓ | ✓ | ✓ | Table stakes |
      ```
      Legend: ✓+ = Better, ✓ = Parity, ✗ = Missing

   **Output**:
   - Populate "Market Opportunity" section in concept.md (NEW)
   - Create TAM/SAM/SOM table with sources
   - Create competitive positioning matrix
   - Document market gaps and opportunities
   - Include source links for reference

   **Reference template**: `templates/shared/concept-sections/market-framework.md`

   ### Phase 0b-2: Multi-Perspective Problem Analysis (NEW)

   **Goal**: Validate problem from multiple stakeholder angles to prevent blind spots.

   **Quality Import**:
   ```text
   IMPORT: templates/shared/quality/brainstorm-curate.md
   APPLY brainstorm-curate to solution approaches in Phase 0c
   ```

   **Perspectives to explore** (for each, document findings):

   1. **End User Perspective**:
      - What's their emotional state when facing this problem?
      - What workarounds have they tried? (list specific behaviors)
      - What would "perfect" look like to them? (ideal outcome)
      - Search: "[user role] workflow frustrations 2025"
      - Search: "[problem] user complaints reddit"

   2. **Business Perspective**:
      - What's the revenue/cost impact of the problem?
      - Who pays for solutions today? (budget holder ≠ user)
      - What's the buying process? (self-serve vs sales-led)
      - Search: "[domain] software ROI case study"
      - Search: "[problem] business impact statistics"

   3. **Technical Perspective**:
      - Why hasn't this been solved before? (historical blockers)
      - What technical barriers exist? (integration challenges)
      - What recent tech enables new solutions? (AI, APIs, platforms)
      - Search: "[problem domain] API integrations 2025"
      - Search: "[technology] breakthrough [domain]"

   4. **Competitive Perspective**:
      - Who else is working on this? (startups, incumbents)
      - What's their approach? (positioning, features)
      - What gaps remain? (underserved segments, missing features)
      - Search: "[competitor] roadmap announcements"
      - Search: "[domain] startup funding 2025"

   **Output**:
   ```markdown
   ## Problem Validation Matrix

   | Perspective | Key Finding | Confidence | Source |
   |-------------|-------------|:----------:|--------|
   | End User | [insight] | High/Med/Low | [source] |
   | Business | [insight] | High/Med/Low | [source] |
   | Technical | [insight] | High/Med/Low | [source] |
   | Competitive | [insight] | High/Med/Low | [source] |

   ### Validated Problem Statement
   [Refined problem statement incorporating all perspectives]

   ### Blind Spots Identified
   - [area needing more research]
   - [assumption to validate with users]
   ```

   **Minimum requirement**: At least 3 of 4 perspectives explored with High/Med confidence.

   ### Phase 0c: Solution Ideation (Enhanced)

   **Goal**: Generate feature ideas based on discovered problems and market gaps.

   **Quality Import**:
   ```text
   IMPORT: templates/shared/quality/brainstorm-curate.md
   IMPORT: templates/shared/quality/anti-slop.md

   APPLY brainstorm-curate to each major feature area
   APPLY anti-slop rules to all prose content
   ```

   **Structured brainstorming** (using Brainstorm-Curate Protocol):

   FOR EACH major problem/gap identified in Phase 0b-2:

   1. **BRAINSTORM Phase** (no evaluation yet):
      Generate 3-5 genuinely different solution approaches:

      - **Option 1 (Conventional)**: What would competitors/industry do?
      - **Option 2 (Minimal)**: Simplest possible solution (80/20)
      - **Option 3 (Unconventional)**: What if we did the opposite?
      - **Option 4 (Premium)**: Best-in-class, no constraints
      - **Option 5 (Lazy/Clever)**: What shortcut might actually work?

      Use unconventional prompts:
      - "What would [innovative company] do here?"
      - "What if we had zero budget? Unlimited budget?"
      - "What would make users say 'wow, that's clever'?"

   2. **CURATE Phase** (evaluate and select):
      For each solution option, score against:

      | Criterion | Weight | Description |
      |-----------|:------:|-------------|
      | User Delight | 3x | How delighted would users be? (0-10) |
      | Time to Value | 3x | How quickly do users see benefit? (0-10) |
      | Feasibility | 2x | Can our team build this? (0-10) |
      | Differentiation | 2x | Does this set us apart? (0-10) |

      Calculate weighted score. Select highest-scoring approach.

   3. **HYBRID Check**:
      Before committing, ask: "Can we combine the best parts of multiple options?"
      - Example: Option 1's UX + Option 3's architecture

   4. **Document Decision**:
      ```markdown
      ### Solution: [Feature Area]

      **Recommendation**: [Chosen approach name]

      **Why this approach**:
      - [Specific reason tied to user needs]
      - [Specific reason tied to differentiation]

      **Alternatives considered**:
      - Option X: [Why not — specific disqualifier]
      - Option Y: [Why not — specific disqualifier]

      **Reversibility**: [High/Medium/Low] — [what's locked in vs changeable]
      ```

   **Legacy compatibility** (enhanced, not replaced):

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
      - Apply Brainstorm-Curate for non-trivial features
      - Rate each: Impact (High/Medium/Low) × Effort (High/Medium/Low)
      - Mark high-impact, reasonable-effort ideas as winners

   **Output**:
   - Populate "Solution Ideation" section with decision reasoning
   - Document alternatives considered (why not)
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

   4. After confirmation, proceed to Clarification Gate.

4b. **Clarification Gate** (NEW — before proceeding to Capture):

   **Goal**: Ensure sufficient clarity before writing concept. Prevents wasted effort on vague inputs.

   **Quality Import**:
   ```text
   IMPORT: templates/shared/quality/anti-slop.md
   APPLY specificity checks to all answers
   ```

   **Clarity Checklist** (must pass before proceeding):

   ```text
   CLARITY_CHECK = {
     target_user: {
       check: "Is target user specific? (persona ≠ 'users')",
       pass_examples: ["Marketing Manager at 50-200 employee B2B SaaS", "Solo indie hackers"],
       fail_examples: ["users", "businesses", "people who need X"]
     },
     core_problem: {
       check: "Is core problem specific? (not generic 'improve efficiency')",
       pass_examples: ["Spend 4+ hours/week copying data between tools", "Can't find relevant docs in 50K+ file repos"],
       fail_examples: ["inefficient processes", "need better workflow", "improve productivity"]
     },
     differentiation: {
       check: "Is differentiation articulated? (not 'better than competitors')",
       pass_examples: ["Only tool with native Figma integration", "10x faster via local-first architecture"],
       fail_examples: ["better UX", "more features", "easier to use"]
     },
     success_measurable: {
       check: "Is success measurable? (has concrete metrics)",
       pass_examples: ["Reduce time-to-first-report from 2 hours to 10 minutes", "Achieve 40% weekly active usage"],
       fail_examples: ["users are happy", "adoption increases", "efficiency improves"]
     }
   }

   FAILED_CHECKS = []
   FOR EACH check IN CLARITY_CHECK:
     IF check fails:
       FAILED_CHECKS.append(check)
   ```

   **If any check fails**, ask clarifying questions BEFORE proceeding:

   ```text
   MAX_QUESTIONS_PER_ROUND = 3  # Avoid overwhelming user

   CLARIFYING_QUESTION_TEMPLATES = {
     target_user: [
       "You mentioned '[vague term]' — can you be more specific?",
       "What's their job title? Company size? Industry?",
       "What does a typical day look like for this person?"
     ],
     core_problem: [
       "The problem is '[vague description]' — which specific process?",
       "What's the cost of this problem? (time/money/frustration)",
       "How do they solve this today? What's wrong with that approach?"
     ],
     differentiation: [
       "How is this different from [competitor]?",
       "What's the one thing competitors do wrong that you'll fix?",
       "Why would someone switch from their current solution?"
     ],
     success_measurable: [
       "How would you measure if this succeeds?",
       "What number would need to change for this to be worth it?",
       "What would users be able to do that they can't do today?"
     ]
   }

   # Select up to 3 most critical questions
   FOR i IN range(min(3, len(FAILED_CHECKS))):
     ASK question from CLARIFYING_QUESTION_TEMPLATES[FAILED_CHECKS[i]]

   WAIT for answers before proceeding
   UPDATE concept with clarified information
   RE-RUN clarity check
   ```

   **Gate Decision**:
   - **PASS (all checks green)**: Proceed to step 5 (Extract Vision)
   - **PARTIAL (1-2 checks fail)**: Ask clarifying questions, then proceed
   - **FAIL (3+ checks fail)**: Return to Discovery Mode (Phase 0a)

   **Output**: Document clarifications in "Assumptions & Clarifications" section.

5. **Extract Vision and Business Context** from user input:

   Parse the user description to identify:
   - **Vision Statement**: What is this? Who is it for? What problem does it solve?
   - **Problem Space**: Specific pain points being addressed
   - **Target Users**: Personas with Jobs-to-be-Done (JTBD)
   - **Success Metrics**: Business KPIs validated against SMART criteria

   For each element:
   - If clearly stated in input: Extract directly
   - If implied: Infer from context and document as assumption
   - If unclear: Use reasonable industry defaults (or use Discovery findings if available)

5a. **Deep Persona Framework (JTBD-Enhanced)** — NEW:

   For each identified persona, capture Jobs-to-be-Done:

   ```markdown
   ### Persona: [Name] — [Role]

   #### Demographics
   - **Segment**: [B2B SMB / B2B Enterprise / B2C Consumer / B2C Prosumer]
   - **Tech Comfort**: [Low / Medium / High]
   - **Frequency of Use**: [Daily / Weekly / Monthly / One-time]

   #### Jobs-to-be-Done
   | Job Type | When I... | I want to... | So I can... |
   |----------|-----------|--------------|-------------|
   | Functional | [situation] | [action] | [outcome] |
   | Emotional | [situation] | [feel] | [state] |
   | Social | [situation] | [appear] | [perception] |

   #### Willingness to Pay
   - **Current spend on alternatives**: $[X]/mo
   - **Pain severity**: [1-10]
   - **Switching cost tolerance**: [Low/Med/High]

   #### Success Criteria
   - **Must have**: [non-negotiable outcomes]
   - **Nice to have**: [delighters]
   - **Deal breaker**: [instant churn triggers]
   ```

   **Minimum requirement**: At least 2 personas with JTBD defined.

   **Reference template**: `templates/shared/concept-sections/persona-jtbd.md`

5aa. **Success Metrics Framework (SMART + OKRs)** — NEW:

   Validate all success metrics against SMART criteria:

   ```markdown
   ## Success Metrics

   ### North Star Metric
   **[Metric Name]**: [Definition]
   - **Why this metric?**: [connects user value to business value]
   - **Leading indicators**: [predictive metrics]
   - **Lagging indicators**: [outcome metrics]

   ### Metric Quality Validation
   | Metric | S | M | A | R | T | Score |
   |--------|:-:|:-:|:-:|:-:|:-:|:-----:|
   | [metric] | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | X/5 |

   **Legend**: S=Specific, M=Measurable, A=Achievable, R=Relevant, T=Time-bound

   ### OKR Structure (if applicable)
   **Objective**: [qualitative goal]
   - **KR1**: [quantitative result] — [baseline → target]
   - **KR2**: [quantitative result] — [baseline → target]
   ```

   **Validation rule**: Metrics with score < 4/5 should be refined before specification.

   **Reference template**: `templates/shared/concept-sections/metrics-smart.md`

5b. **Extract UX Foundation Layer**:

   Generate foundation features based on detected project type.

   ```text
   # Load foundation scenarios from catalog
   READ memory/knowledge/frameworks/ux-foundations.md

   FOR EACH foundation in REQUIRED_FOUNDATIONS:
     1. Load scenario definitions (UXF-xxx IDs)
     2. Generate corresponding Epic/Feature/Story entries:
        - AUTH → EPIC-001 User Access
          - F01 Registration (UXF-AUTH-001, UXF-AUTH-002)
          - F02 Session Management (UXF-AUTH-003, UXF-AUTH-004)
        - ERROR → Infrastructure layer (cross-cutting)
        - LAYOUT → Infrastructure layer (cross-cutting)
        - NAV → Feature in EPIC-001 or separate EPIC
        - FTUE → EPIC for Onboarding
        - FEEDBACK → Infrastructure layer (cross-cutting)

     3. Assign Wave:
        - Wave 1: AUTH, LAYOUT, ERROR (core infrastructure)
        - Wave 2: NAV, FTUE, FEEDBACK (user experience)

     4. Auto-set priority:
        - Wave 1 foundations → P1a (always highest priority)
        - Wave 2 foundations → P1b

     5. Mark in "UX Foundation Layer" section of concept.md
   ```

   **Output**:
   - Populate "UX Foundation Layer" section with detected foundations
   - Generate foundation Epic/Features/Stories BEFORE user-defined features
   - Set up "Foundation Scenarios" mapping table

5c. **Risk Assessment Matrix** — NEW:

   Identify and document execution risks before detailed planning:

   ```markdown
   ## Risk Assessment

   ### Execution Risks
   | Risk | Likelihood | Impact | L×I | Mitigation | Contingency |
   |------|:----------:|:------:|:---:|------------|-------------|
   | [Risk 1] | [1-5] | [1-5] | [X] | [Proactive action] | [If it happens...] |
   | [Risk 2] | [1-5] | [1-5] | [X] | [Proactive action] | [If it happens...] |
   | [Risk 3] | [1-5] | [1-5] | [X] | [Proactive action] | [If it happens...] |

   ### Dependency Failure Scenarios
   | Dependency | If unavailable... | Fallback | Cost of fallback |
   |------------|-------------------|----------|------------------|
   | [service/API] | [impact] | [alternative] | [effort/time] |

   ### Pivot Criteria
   - **Pivot if**: [condition 1], [condition 2]
   - **Pivot to**: [alternative direction]
   - **Kill if**: [condition that proves thesis invalid]
   ```

   **Risk scoring**: Likelihood × Impact. Address risks with score ≥ 12 first.

   **Minimum requirement**: At least 3 risks with mitigations documented.

   **Reference template**: `templates/shared/concept-sections/risk-matrix.md`

5d. **Technical Discovery Hints** — NEW:

   Surface architectural considerations early to reduce surprises during planning:

   ```markdown
   ## Technical Discovery

   ### Domain Entities (Sketch)
   | Entity | Key Attributes | Relationships | Persistence |
   |--------|----------------|---------------|-------------|
   | User | id, email, role | → Account, → Sessions | PostgreSQL |
   | [Entity] | [attrs] | [relations] | [store] |

   ### API Surface Estimation
   | Domain | Operations | Auth Required | External Integration |
   |--------|------------|:-------------:|---------------------|
   | Users | CRUD + search | ✓ | SSO providers |
   | [Domain] | [ops] | ✓/✗ | [integrations] |

   ### Integration Complexity
   | External System | Protocol | Complexity | Risk |
   |-----------------|----------|:----------:|------|
   | [system] | REST/GraphQL | Low/Med/High | [notes] |

   ### Constitution Principle Conflicts
   | Feature | Principle | Conflict | Resolution |
   |---------|-----------|----------|------------|
   | [feature] | [ID] | [what conflicts] | [how to resolve] |
   ```

   **Purpose**: Identify potential blockers and architectural decisions before specification.

   **Reference template**: `templates/shared/concept-sections/technical-hints.md`

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

7b. **Scenario Completeness Validation**:

   Validate each non-foundation story has complete context.

   ```text
   COMPLETENESS_CHECKS = {
     "Entry Point": "How does user navigate here?",
     "Auth Context": "GUEST | AUTHENTICATED | ADMIN?",
     "Error Handling": "What if the action fails?",
     "Exit Point": "Where does user go after success?"
   }

   FOR EACH story in Feature Hierarchy:
     IF story.wave >= 3:  # Non-foundation story
       FOR EACH check in COMPLETENESS_CHECKS:
         IF check not documented:
           WARN: "Story {story.id} missing: {check}"

   # Generate completeness table
   | Story ID | Entry Point | Auth | Error | Exit | Complete? |
   |----------|-------------|------|-------|------|-----------|
   | EPIC-002.F01.S01 | Nav menu | AUTH | Shows error toast | Returns to list | ✓ |
   | EPIC-002.F01.S02 | Direct link | AUTH | ? | ? | ⚠ INCOMPLETE |
   ```

   **Output**:
   - List of incomplete stories with missing fields
   - Recommendation: "Complete scenario context before specification"

7c. **Generate Golden Path**:

   Create J000 journey that validates Wave 1-2 completion.

   ```text
   GOLDEN_PATH_TEMPLATE = [
     "[Guest] Views home page → LAYOUT",
     "[Guest] Clicks Sign Up → NAV",
     "[Guest] Registers account → AUTH",
     "[User] Completes onboarding → FTUE",
     "[User] Performs first action → First P1a feature",
     "[User] Sees confirmation → FEEDBACK"
   ]

   FOR EACH step in GOLDEN_PATH_TEMPLATE:
     1. Find matching feature in hierarchy
     2. Link to Feature ID
     3. Note Wave number
     4. Set status = [ ] (pending)

   ADD to "Execution Order" section as "Golden Path"
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

8b. **Foundation Layer Detection (Pattern-Based)**:

   Identify user-defined features that ARE foundations (even if not from catalog).

   ```text
   FOUNDATION_PATTERNS = {
     "AUTH": ["auth*", "login*", "signin*", "signup*", "register*", "session*", "oauth*", "sso*"],
     "USER_MGMT": ["user*", "account*", "profile*", "permission*", "role*", "member*"],
     "CORE_DATA": ["schema*", "database*", "migration*", "model*", "entity*"],
     "INFRASTRUCTURE": ["config*", "env*", "logging*", "error*", "monitoring*"],
     "NAV": ["nav*", "route*", "router*", "menu*", "sidebar*"],
     "LAYOUT": ["layout*", "shell*", "frame*", "container*", "header*", "footer*"]
   }

   FOR EACH feature in Feature Hierarchy:
     feature_name_lower = lowercase(feature.name)

     FOR EACH (foundation_type, patterns) in FOUNDATION_PATTERNS:
       FOR EACH pattern in patterns:
         IF feature_name_lower MATCHES pattern (glob-style):
           MARK feature.is_foundation = true
           MARK feature.foundation_type = foundation_type

           # Auto-assign Wave based on foundation type
           IF foundation_type in ["AUTH", "USER_MGMT", "CORE_DATA", "INFRASTRUCTURE", "LAYOUT"]:
             SET feature.wave = 1
             IF feature.priority > "P1a":
               WARN: "Elevating {feature.id} to P1a (foundation)"
               SET feature.priority = "P1a"
           ELSE IF foundation_type in ["NAV"]:
             SET feature.wave = 2
             IF feature.priority > "P1b":
               SET feature.priority = "P1b"

           BREAK  # First match wins
   ```

   **Output**:
   - List of detected foundation features with their types
   - Wave assignments for all foundations
   - Priority elevation warnings (if any)

8c. **Populate Execution Order**:

   Organize all features into Waves in the concept.md template.

   ```text
   WAVE_1_FEATURES = filter(features, wave == 1)
   WAVE_2_FEATURES = filter(features, wave == 2)
   WAVE_3_PLUS = filter(features, wave >= 3)

   FOR EACH feature in WAVE_1_FEATURES:
     ADD to "Wave 1: Foundation Layer" table

   FOR EACH feature in WAVE_2_FEATURES:
     ADD to "Wave 2: Experience Layer" table

   FOR EACH feature in WAVE_3_PLUS:
     ADD to "Wave 3+: Business Features" table

   # Calculate what each feature blocks
   FOR EACH feature:
     feature.blocks = find_features_that_depend_on(feature.id)
   ```

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

---

## Self-Review Phase (MANDATORY)

**Before declaring concept.md complete, you MUST perform self-review.**

This ensures the concept hierarchy is valid, complete, and ready for specification.

### Step 1: Re-read Generated Artifact

Read the concept file you created:
- `specs/concept.md`

Parse to extract hierarchy and validate structure.

### Step 2: Quality Criteria

| ID | Criterion | Check | Severity |
|----|-----------|-------|----------|
| SR-CONCEPT-01 | Vision Concrete | No vague words ("better", "improved", "enhanced") | CRITICAL |
| SR-CONCEPT-02 | Personas Defined | At least 2 user personas with specific goals | CRITICAL |
| SR-CONCEPT-03 | Hierarchy Valid | All IDs follow EPIC-NNN.FNN.SNN format | CRITICAL |
| SR-CONCEPT-04 | Epics Have Features | Every Epic has ≥1 Feature | HIGH |
| SR-CONCEPT-05 | Features Have Stories | Every Feature has ≥1 Story | HIGH |
| SR-CONCEPT-06 | IDs Unique | No duplicate EPIC/Feature/Story IDs | CRITICAL |
| SR-CONCEPT-07 | Dependencies Acyclic | No circular dependencies in DAG | CRITICAL |
| SR-CONCEPT-08 | Journeys Mapped | At least 1 journey per primary persona | HIGH |
| SR-CONCEPT-09 | Backlog Populated | Ideas Backlog section exists (even if empty note) | MEDIUM |
| SR-CONCEPT-10 | Glossary Present | Domain-specific terms defined | MEDIUM |
| SR-CONCEPT-11 | Foundation Detected | UX Foundation Layer populated with detected type | CRITICAL |
| SR-CONCEPT-12 | Foundations are P1a | All Wave 1 foundations have P1a priority | HIGH |
| SR-CONCEPT-13 | Execution Order Valid | Wave assignments complete, no Wave 3 without Wave 1-2 | HIGH |
| SR-CONCEPT-14 | Golden Path Exists | J000 journey defined covering Wave 1-2 features | CRITICAL |
| SR-CONCEPT-15 | No Orphan Features | All features assigned to a Wave | MEDIUM |
| SR-CONCEPT-16 | Market Opportunity | TAM/SAM/SOM analysis present with sources | HIGH |
| SR-CONCEPT-17 | JTBD Personas | Personas include Jobs-to-be-Done | HIGH |
| SR-CONCEPT-18 | SMART Metrics | Success metrics validated against SMART criteria | HIGH |
| SR-CONCEPT-19 | Risk Assessment | ≥3 risks documented with mitigations | MEDIUM |
| SR-CONCEPT-20 | Technical Hints | Domain entities or API surface estimated | MEDIUM |
| SR-CONCEPT-21 | CQS Calculated | Concept Quality Score computed and displayed | HIGH |
| SR-CONCEPT-22 | CQS Quality Gate | CQS ≥ 60 for specification readiness | HIGH |

### Step 3: Hierarchy Validation

Verify hierarchy structure:

```text
EPICS = {}
FEATURES = {}
STORIES = {}

FOR EACH line matching EPIC-NNN pattern:
  Validate format: EPIC-NNN
  Check uniqueness
  EPICS[id] = entry

FOR EACH line matching EPIC-NNN.FNN pattern:
  Validate parent EPIC exists
  Check uniqueness
  FEATURES[id] = entry

FOR EACH line matching EPIC-NNN.FNN.SNN pattern:
  Validate parent Feature exists
  Check uniqueness
  STORIES[id] = entry

# Validate completeness
FOR EACH epic in EPICS:
  IF no features reference this epic:
    ERROR: "Epic {id} has no features"

FOR EACH feature in FEATURES:
  IF no stories reference this feature:
    ERROR: "Feature {id} has no stories"
```

### Step 3b: Foundation & Wave Validation

Verify UX Foundation Layer and Execution Order:

```text
# SR-CONCEPT-11: Foundation Detected
IF "UX Foundation Layer" section is empty OR PROJECT_TYPE not set:
  ERROR: "Foundation layer not populated"

# SR-CONCEPT-12: Foundations are P1a
FOR EACH feature WHERE wave == 1:
  IF feature.priority != "P1a":
    ERROR: "Wave 1 feature {id} must be P1a, found {priority}"

# SR-CONCEPT-13: Execution Order Valid
WAVE_1_COUNT = count(features WHERE wave == 1)
WAVE_2_COUNT = count(features WHERE wave == 2)
WAVE_3_COUNT = count(features WHERE wave >= 3)

IF WAVE_3_COUNT > 0 AND WAVE_1_COUNT == 0:
  ERROR: "Wave 3 features exist but no Wave 1 foundations"

IF WAVE_3_COUNT > 0 AND WAVE_2_COUNT == 0:
  WARN: "Wave 3 features exist but no Wave 2 experience layer"

# SR-CONCEPT-14: Golden Path Exists
IF "Golden Path" section is empty OR J000 not defined:
  ERROR: "Golden Path (J000) not defined"

GOLDEN_PATH_FEATURES = extract features from J000
FOR EACH feature in GOLDEN_PATH_FEATURES:
  IF feature not in FEATURES:
    ERROR: "Golden Path references undefined feature: {id}"

# SR-CONCEPT-15: No Orphan Features
FOR EACH feature in FEATURES:
  IF feature.wave is undefined:
    WARN: "Feature {id} not assigned to any Wave"
```

### Step 3c: CQS Calculation — NEW

Calculate Concept Quality Score from 6 components:

```text
# Component Scoring (see templates/shared/concept-sections/cqs-score.md for full criteria)

MARKET_SCORE = 0
IF "TAM/SAM/SOM" section present with values: MARKET_SCORE += 55
IF "Competitive Positioning Matrix" present: MARKET_SCORE += 25
IF "Market Validation Signals" checklist present: MARKET_SCORE += 20

PERSONA_SCORE = 0
IF count(personas) >= 2: PERSONA_SCORE += 30
IF personas have JTBD tables: PERSONA_SCORE += 40
IF "Willingness to Pay" documented: PERSONA_SCORE += 15
IF "Success Criteria" documented: PERSONA_SCORE += 15

METRICS_SCORE = 0
IF "North Star Metric" identified: METRICS_SCORE += 40
IF SMART validation table present: METRICS_SCORE += 40
IF leading/lagging indicators defined: METRICS_SCORE += 20

FEATURES_SCORE = 0
IF Epic/Feature/Story hierarchy valid: FEATURES_SCORE += 40
IF Wave assignments complete: FEATURES_SCORE += 30
IF Golden Path (J000) defined: FEATURES_SCORE += 30

RISK_SCORE = 0
IF count(risks) >= 3: RISK_SCORE += 40
IF mitigations documented: RISK_SCORE += 30
IF pivot criteria defined: RISK_SCORE += 30

TECH_SCORE = 0
IF "Domain Entities" sketched: TECH_SCORE += 40
IF "API Surface Estimation" present: TECH_SCORE += 30
IF "Constitution Principle Conflicts" reviewed: TECH_SCORE += 30

# Calculate weighted CQS
CQS = (MARKET_SCORE × 0.25) + (PERSONA_SCORE × 0.20) + (METRICS_SCORE × 0.15) +
      (FEATURES_SCORE × 0.20) + (RISK_SCORE × 0.10) + (TECH_SCORE × 0.10)

# SR-CONCEPT-21: CQS Calculated
STORE CQS for report output

# SR-CONCEPT-22: CQS Quality Gate
IF CQS < 60:
  WARN: "CQS {CQS}/100 — Concept not ready for specification"
  WARN: "Low scoring components: [list components < 60]"
ELSE IF CQS < 80:
  INFO: "CQS {CQS}/100 — Proceed with caution, flag gaps during specification"
ELSE:
  INFO: "CQS {CQS}/100 — Concept ready for specification"
```

### Step 4: Dependency Validation

Check for circular dependencies:

```text
BUILD directed graph from dependency declarations:
  - Feature A depends on Feature B → edge B → A

RUN topological sort:
  IF cycle detected:
    Extract cycle path
    ERROR: "Circular dependency: {path}"

VALIDATE cross-Epic dependencies are documented
```

### Step 5: Verdict

- **PASS**: All CRITICAL/HIGH criteria pass, hierarchy valid → proceed to handoff
- **FAIL**: Any CRITICAL issue → self-correct (max 3 iterations)
  - Duplicate IDs → renumber
  - Missing hierarchy levels → add
  - Circular dependencies → break cycle
- **WARN**: Only MEDIUM issues → show warnings, proceed

### Step 6: Self-Correction Loop

```text
IF issues found AND iteration < 3:
  1. Fix each issue:
     - Renumber duplicate IDs
     - Add missing Features/Stories
     - Break circular dependencies
     - Add Ideas Backlog section
     - Populate Glossary
  2. Re-run self-review from Step 1
  3. Report: "Self-review iteration {N}: Fixed {issues}, re-validating..."

IF still failing after 3 iterations:
  - STOP and report to user
  - List hierarchy validation failures
  - Do NOT proceed to handoff
```

### Step 7: Self-Review Report

After passing self-review, output:

```text
## Self-Review Complete ✓

**Artifact**: specs/concept.md
**Iterations**: {N}

### Hierarchy Summary

| Level | Count | Status |
|-------|-------|--------|
| Epics | {N} | ✓ All have Features |
| Features | {N} | ✓ All have Stories |
| Stories | {N} | ✓ All IDs unique |

### Validation Results

| Check | Result |
|-------|--------|
| Vision | ✓ Concrete (no vague terms) |
| Personas | ✓ {N} defined |
| ID Format | ✓ All valid |
| Dependencies | ✓ DAG valid (no cycles) |
| User Journeys | ✓ {N} journeys mapped |
| Ideas Backlog | ✓ {N} ideas captured |

### Foundation Layer

| Check | Result |
|-------|--------|
| Project Type | ✓ {PROJECT_TYPE} detected |
| Foundations | ✓ {N} required, {N} defined |
| Golden Path | ✓ J000 defined with {N} steps |

### Wave Distribution

| Wave | Features | Status |
|------|----------|--------|
| Wave 1 (Foundation) | {N} | ✓ All P1a |
| Wave 2 (Experience) | {N} | ✓ All P1b |
| Wave 3+ (Business) | {N} | Ready after Wave 1-2 |

### Priority Distribution

| Priority | Stories |
|----------|---------|
| P1a | {N} |
| P1b | {N} |
| P2 | {N} |
| P3 | {N} |

### Concept Quality Score (CQS) — NEW

**Formula**: CQS = (Market × 0.25 + Persona × 0.20 + Metrics × 0.15 + Features × 0.20 + Risk × 0.10 + Technical × 0.10) × 100

| Component | Score | Weight | Weighted |
|-----------|:-----:|:------:|:--------:|
| Market Validation | {MARKET_SCORE}/100 | 0.25 | {WEIGHTED} |
| Persona Depth | {PERSONA_SCORE}/100 | 0.20 | {WEIGHTED} |
| Metrics Quality | {METRICS_SCORE}/100 | 0.15 | {WEIGHTED} |
| Feature Completeness | {FEATURES_SCORE}/100 | 0.20 | {WEIGHTED} |
| Risk Assessment | {RISK_SCORE}/100 | 0.10 | {WEIGHTED} |
| Technical Hints | {TECH_SCORE}/100 | 0.10 | {WEIGHTED} |
| **CQS Total** | | | **{CQS}/100** |

**Quality Gate**: {CQS_STATUS}
- CQS ≥ 80: ✅ Ready for specification with high confidence
- CQS 60-79: ⚠️ Proceed with caution — flag gaps during specification
- CQS < 60: ⛔ Not ready — complete discovery before specification

**Reference**: `templates/shared/concept-sections/cqs-score.md`

### Ready for Specification

Concept capture complete.

**Recommended order** (Wave-based):
1. Start with Wave 1 foundations: `/speckit.specify EPIC-001.F01.S01`
2. Then Wave 2 experience: (after Wave 1 complete)
3. Then Wave 3+ business features: (after Golden Path testable)

**Golden Path status**: [ ] Not yet testable (requires Wave 1-2 completion)
```

---
description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
auto_invocation:
  enabled: true
  triggers:
    - source: speckit.analyze
      profile: spec_validate
      gates:
        - ambiguity_count
        - constitution_alignment
      inject: extracted_questions
    - source: speckit.specify
      trigger: pre_handoff_action_failure
      inject: extracted_questions_from_validation
  behavior:
    skip_coverage_scan: true
    use_injected_questions: true
    max_questions: 5
    post_clarification: re_validate
scripts:
   sh: scripts/bash/check-prerequisites.sh --json --paths-only
   ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
claude_code:
  model: sonnet
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 4000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 8000
        max_parallel: 3
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 16000
        max_parallel: 6
        batch_delay: 1500
        wave_overlap_threshold: 0.65
  cache_hierarchy: full
  orchestration:
    max_parallel: 6
    fail_fast: true
    wave_overlap:
      enabled: true
      overlap_threshold: 0.65
  operation_batching:
    enabled: true
    skip_flag: "--sequential"
    framework: templates/shared/operation-batching.md
    strategies:
      context_reads: true    # Batch context file reads
      searches: true         # Batch gap search queries
      prefetch: true         # Speculative parallel load
    gap_search_batch:
      enabled: true
      queries:
        - "Search spec.md for vague terms and ambiguities"
        - "Search plan.md for undefined references"
        - "Search tasks.md for missing details"
  subagents:
    # Wave 1: Ambiguity Detection (Enhanced with pattern-based detection)
    - role: ambiguity-detector
      role_group: ANALYSIS
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Detect ambiguities in the specification using multi-pass analysis.

        Read: `templates/shared/quality/ambiguity-patterns.md` for detection patterns.

        ## PASS 1: Heuristic Pattern Matching (Fast)

        FOR requirement IN functional_requirements:

          # 1a. Vague Term Detection
          Check against VAGUE_TERM_PATTERNS:
          - Performance: "fast", "slow", "quickly", "responsive", "real-time"
          - Quality/UX: "user-friendly", "intuitive", "simple", "easy", "clean"
          - Security: "secure", "safe", "protected", "robust", "reliable"
          - Quantity: "some", "many", "few", "several", "multiple", "various"
          - Frequency: "often", "rarely", "occasionally", "sometimes"
          - Size: "large", "small", "big", "minimal", "significant"
          - Time: "soon", "later", "eventually", "immediately", "recently"

          # 1b. Missing Quantity Detection
          Check for triggers WITHOUT explicit values:
          - Retention: "retain", "store", "keep" → How long?
          - Rate limits: "limit", "throttle", "quota" → What limit?
          - Pagination: "list", "show", "display" → How many per page?
          - Timeout: "timeout", "expire", "wait" → What duration?
          - Max length: "text", "input", "field" → Character limit?

          # 1c. Unclear Actor Detection
          - Generic system: "the system", "it", "this"
          - Generic user: "user", "the user" (which type?)
          - Passive voice: "is displayed", "will be sent", "should be validated"

          # 1d. Conditional Gap Detection
          - "if X" without "else" or "otherwise" behavior

          # 1e. Incomplete List Detection
          - "etc.", "...", "and more", "such as", "including", "like"

        ## PASS 2: LLM Metacognitive Analysis (Deep)

        Apply this metacognitive prompt for each requirement:
        "What CANNOT I understand clearly from this requirement?"

        For each ambiguity found:
        - Generate at least 2 different valid interpretations
        - Explain implementation impact of each interpretation
        - Flag if interpretations lead to DIFFERENT implementations

        ## PASS 3: Cross-Requirement Consistency

        Check for contradictions or inconsistencies:
        - Conflicting constraints between requirements
        - Terminology inconsistencies (same concept, different names)
        - Logical impossibilities ("offline-only" + "real-time sync")

        ## OUTPUT FORMAT

        ambiguities: [
          {
            requirement_id: "FR-XXX",
            ambiguity_type: "VAGUE_TERM|MISSING_QUANTITY|UNCLEAR_ACTOR|CONDITIONAL_GAP|INCOMPLETE_LIST|UNDEFINED_TERM",
            ambiguous_text: "the specific text",
            explanation: "why this is ambiguous",
            interpretations: ["interpretation 1", "interpretation 2"],
            implementation_impact: "how this affects implementation",
            clarification_question: "targeted question to resolve",
            severity: "CRITICAL|HIGH|MEDIUM|LOW"
          }
        ]

        coverage_map: {
          functional_scope: "Clear|Partial|Missing",
          domain_data_model: "Clear|Partial|Missing",
          interaction_ux: "Clear|Partial|Missing",
          non_functional: "Clear|Partial|Missing",
          integration_deps: "Clear|Partial|Missing",
          edge_cases: "Clear|Partial|Missing",
          constraints: "Clear|Partial|Missing",
          terminology: "Clear|Partial|Missing"
        }

        Prioritize by (Impact * Uncertainty) heuristic.
        Output: ambiguities list + coverage map with candidate questions.

    # Wave 2: Question Generation (after detection)
    - role: question-generator
      role_group: ANALYSIS
      parallel: true
      depends_on: [ambiguity-detector]
      priority: 20
      model_override: sonnet
      prompt: |
        Generate up to 5 targeted clarification questions.
        Each question must be multiple-choice (2-5 options) or short-answer.
        Prioritize by (Impact * Uncertainty) heuristic.
        Ensure category coverage balance.
        Add recommended option with reasoning for each.
        Output: formatted question queue ready for user interaction.

    # Wave 3: Spec Update (after user answers)
    - role: spec-updater
      role_group: DOCS
      parallel: true
      depends_on: [question-generator]
      priority: 30
      model_override: sonnet
      prompt: |
        Integrate clarifications into spec.md after user answers.
        Create/update ## Clarifications section with session date.
        Apply answers to appropriate sections: Functional, Data Model, etc.
        Replace obsolete statements, normalize terminology.
        Perform self-review: verify integration, check contradictions.
        Output: updated spec with clarifications applied.
flags:
  max_model: "--max-model <opus|sonnet|haiku>"  # Override model cap
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Goal: Detect and reduce ambiguity or missing decision points in the active feature specification and record the clarifications directly in the spec file.

Note: This clarification workflow is expected to run (and be completed) BEFORE invoking `/speckit.plan`. If the user explicitly states they are skipping clarification (e.g., exploratory spike), you may proceed, but must warn that downstream rework risk increases.

Execution steps:

1. Run `{SCRIPT}` from repo root **once** (combined `--json --paths-only` mode / `-Json -PathsOnly`). Parse minimal JSON payload fields:
   - `FEATURE_DIR`
   - `FEATURE_SPEC`
   - (Optionally capture `IMPL_PLAN`, `TASKS` for future chained flows.)
   - If JSON parsing fails, abort and instruct user to re-run `/speckit.specify` or verify feature branch environment.
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. Load the current spec file. Perform a structured ambiguity & coverage scan using this taxonomy. For each category, mark status: Clear / Partial / Missing. Produce an internal coverage map used for prioritization (do not output raw map unless no questions will be asked).

   Functional Scope & Behavior:
   - Core user goals & success criteria
   - Explicit out-of-scope declarations
   - User roles / personas differentiation

   Domain & Data Model:
   - Entities, attributes, relationships
   - Identity & uniqueness rules
   - Lifecycle/state transitions
   - Data volume / scale assumptions

   Interaction & UX Flow:
   - Critical user journeys / sequences
   - Error/empty/loading states
   - Accessibility or localization notes

   Non-Functional Quality Attributes:
   - Performance (latency, throughput targets)
   - Scalability (horizontal/vertical, limits)
   - Reliability & availability (uptime, recovery expectations)
   - Observability (logging, metrics, tracing signals)
   - Security & privacy (authN/Z, data protection, threat assumptions)
   - Compliance / regulatory constraints (if any)

   Integration & External Dependencies:
   - External services/APIs and failure modes
   - Data import/export formats
   - Protocol/versioning assumptions

   Edge Cases & Failure Handling:
   - Negative scenarios
   - Rate limiting / throttling
   - Conflict resolution (e.g., concurrent edits)

   Constraints & Tradeoffs:
   - Technical constraints (language, storage, hosting)
   - Explicit tradeoffs or rejected alternatives

   Terminology & Consistency:
   - Canonical glossary terms
   - Avoided synonyms / deprecated terms

   Completion Signals:
   - Acceptance criteria testability
   - Measurable Definition of Done style indicators

   Misc / Placeholders:
   - TODO markers / unresolved decisions
   - Ambiguous adjectives ("robust", "intuitive") lacking quantification

   For each category with Partial or Missing status, add a candidate question opportunity unless:
   - Clarification would not materially change implementation or validation strategy
   - Information is better deferred to planning phase (note internally)

3. Generate (internally) a prioritized queue of candidate clarification questions (maximum 5). Do NOT output them all at once. Apply these constraints:
    - Maximum of 10 total questions across the whole session.
    - Each question must be answerable with EITHER:
       - A short multiple‑choice selection (2–5 distinct, mutually exclusive options), OR
       - A one-word / short‑phrase answer (explicitly constrain: "Answer in <=5 words").
    - Only include questions whose answers materially impact architecture, data modeling, task decomposition, test design, UX behavior, operational readiness, or compliance validation.
    - Ensure category coverage balance: attempt to cover the highest impact unresolved categories first; avoid asking two low-impact questions when a single high-impact area (e.g., security posture) is unresolved.
    - Exclude questions already answered, trivial stylistic preferences, or plan-level execution details (unless blocking correctness).
    - Favor clarifications that reduce downstream rework risk or prevent misaligned acceptance tests.
    - If more than 5 categories remain unresolved, select the top 5 by (Impact * Uncertainty) heuristic.

4. Sequential questioning loop (interactive):
    - Present EXACTLY ONE question at a time.
    - For multiple‑choice questions:
       - **Analyze all options** and determine the **most suitable option** based on:
          - Best practices for the project type
          - Common patterns in similar implementations
          - Risk reduction (security, performance, maintainability)
          - Alignment with any explicit project goals or constraints visible in the spec
       - Present your **recommended option prominently** at the top with clear reasoning (1-2 sentences explaining why this is the best choice).
       - Format as: `**Recommended:** Option [X] - <reasoning>`
       - Then render all options as a Markdown table:

       | Option | Description |
       |--------|-------------|
       | A | <Option A description> |
       | B | <Option B description> |
       | C | <Option C description> (add D/E as needed up to 5) |
       | Short | Provide a different short answer (<=5 words) (Include only if free-form alternative is appropriate) |

       - After the table, add: `You can reply with the option letter (e.g., "A"), accept the recommendation by saying "yes" or "recommended", or provide your own short answer.`
    - For short‑answer style (no meaningful discrete options):
       - Provide your **suggested answer** based on best practices and context.
       - Format as: `**Suggested:** <your proposed answer> - <brief reasoning>`
       - Then output: `Format: Short answer (<=5 words). You can accept the suggestion by saying "yes" or "suggested", or provide your own answer.`
    - After the user answers:
       - If the user replies with "yes", "recommended", or "suggested", use your previously stated recommendation/suggestion as the answer.
       - Otherwise, validate the answer maps to one option or fits the <=5 word constraint.
       - If ambiguous, ask for a quick disambiguation (count still belongs to same question; do not advance).
       - Once satisfactory, record it in working memory (do not yet write to disk) and move to the next queued question.
    - Stop asking further questions when:
       - All critical ambiguities resolved early (remaining queued items become unnecessary), OR
       - User signals completion ("done", "good", "no more"), OR
       - You reach 5 asked questions.
    - Never reveal future queued questions in advance.
    - If no valid questions exist at start, immediately report no critical ambiguities.

5. Integration after EACH accepted answer (incremental update approach):
    - Maintain in-memory representation of the spec (loaded once at start) plus the raw file contents.
    - For the first integrated answer in this session:
       - Ensure a `## Clarifications` section exists (create it just after the highest-level contextual/overview section per the spec template if missing).
       - Under it, create (if not present) a `### Session YYYY-MM-DD` subheading for today.
    - Append a bullet line immediately after acceptance: `- Q: <question> → A: <final answer>`.
    - Then immediately apply the clarification to the most appropriate section(s):
       - Functional ambiguity → Update or add a bullet in Functional Requirements.
       - User interaction / actor distinction → Update User Stories or Actors subsection (if present) with clarified role, constraint, or scenario.
       - Data shape / entities → Update Data Model (add fields, types, relationships) preserving ordering; note added constraints succinctly.
       - Non-functional constraint → Add/modify measurable criteria in Non-Functional / Quality Attributes section (convert vague adjective to metric or explicit target).
       - Edge case / negative flow → Add a new bullet under Edge Cases / Error Handling (or create such subsection if template provides placeholder for it).
       - Terminology conflict → Normalize term across spec; retain original only if necessary by adding `(formerly referred to as "X")` once.
    - If the clarification invalidates an earlier ambiguous statement, replace that statement instead of duplicating; leave no obsolete contradictory text.
    - Save the spec file AFTER each integration to minimize risk of context loss (atomic overwrite).
    - Preserve formatting: do not reorder unrelated sections; keep heading hierarchy intact.
    - Keep each inserted clarification minimal and testable (avoid narrative drift).

6. Validation (performed after EACH write plus final pass):
   - Clarifications session contains exactly one bullet per accepted answer (no duplicates).
   - Total asked (accepted) questions ≤ 5.
   - Updated sections contain no lingering vague placeholders the new answer was meant to resolve.
   - No contradictory earlier statement remains (scan for now-invalid alternative choices removed).
   - Markdown structure valid; only allowed new headings: `## Clarifications`, `### Session YYYY-MM-DD`.
   - Terminology consistency: same canonical term used across all updated sections.

7. Write the updated spec back to `FEATURE_SPEC`.

8. Report completion (after questioning loop ends or early termination):
   - Number of questions asked & answered.
   - Path to updated spec.
   - Sections touched (list names).
   - Coverage summary table listing each taxonomy category with Status: Resolved (was Partial/Missing and addressed), Deferred (exceeds question quota or better suited for planning), Clear (already sufficient), Outstanding (still Partial/Missing but low impact).
   - If any Outstanding or Deferred remain, recommend whether to proceed to `/speckit.plan` or run `/speckit.clarify` again later post-plan.
   - Suggested next command.

Behavior rules:

- If no meaningful ambiguities found (or all potential questions would be low-impact), respond: "No critical ambiguities detected worth formal clarification." and suggest proceeding.
- If spec file missing, instruct user to run `/speckit.specify` first (do not create a new spec here).
- Never exceed 5 total asked questions (clarification retries for a single question do not count as new questions).
- Avoid speculative tech stack questions unless the absence blocks functional clarity.
- Respect user early termination signals ("stop", "done", "proceed").
- If no questions asked due to full coverage, output a compact coverage summary (all categories Clear) then suggest advancing.
- If quota reached with unresolved high-impact categories remaining, explicitly flag them under Deferred with rationale.

Context for prioritization: {ARGS}

---

## Self-Review Phase (MANDATORY)

**Before declaring clarification complete, you MUST perform self-review.**

This ensures all clarifications are properly integrated and the spec is ready for planning.

### Step 1: Re-read Updated Spec

Read the spec file you modified:
- `FEATURE_SPEC` (path from script output)

Parse to verify clarification integration.

### Step 2: Quality Criteria

| ID | Criterion | Check | Severity |
|----|-----------|-------|----------|
| SR-CLAR-01 | Clarifications Logged | Session entry exists under ## Clarifications | CRITICAL |
| SR-CLAR-02 | Answers Recorded | Each Q&A pair is documented | CRITICAL |
| SR-CLAR-03 | Spec Sections Updated | Clarifications applied to appropriate sections | HIGH |
| SR-CLAR-04 | No Contradictions | Updated text doesn't conflict with existing | HIGH |
| SR-CLAR-05 | Markers Resolved | No [NEEDS CLARIFICATION] for answered questions | HIGH |
| SR-CLAR-06 | Terms Normalized | Same canonical term used throughout | MEDIUM |
| SR-CLAR-07 | Markdown Valid | Structure and headings intact | MEDIUM |
| SR-CLAR-08 | Coverage Balanced | High-impact categories addressed first | MEDIUM |

### Step 3: Integration Verification

For each clarification recorded, verify:

```text
FOR EACH clarification in ## Clarifications > ### Session YYYY-MM-DD:
  1. Extract Q&A pair
  2. Find target section where answer was integrated
  3. Verify answer text appears in target section
  4. Check no conflicting text remains in spec
  5. Confirm terminology is consistent with glossary (if exists)

IF clarification not found in any section:
  ERROR: "Clarification for '{question}' not integrated into spec"
  Add to issues
```

### Step 4: Contradiction Scan

Check for conflicting statements:

```text
FOR EACH updated section:
  Scan for opposing statements about same topic
  Examples of contradictions:
  - "Users must authenticate" vs "No login required"
  - "Maximum 5 items" vs "No limit on items"
  - "Real-time updates" vs "Batch processing only"

IF contradiction found:
  ERROR: "Contradiction in {section}: {statement1} vs {statement2}"
```

### Step 5: Verdict

- **PASS**: All clarifications logged, integrated, no contradictions → report completion
- **FAIL**: Missing integration or contradiction → self-correct (max 3 iterations)
- **WARN**: Minor issues (formatting, optional sections) → show warnings, proceed

### Step 6: Self-Correction Loop

```text
IF issues found AND iteration < 3:
  1. Fix each issue:
     - Add missing clarification entries
     - Integrate answers into correct sections
     - Remove contradictory statements
     - Normalize terminology
  2. Save spec file
  3. Re-run self-review from Step 1
  4. Report: "Self-review iteration {N}: Fixed {issues}, re-validating..."

IF still failing after 3 iterations:
  - STOP and report to user
  - List unresolved integration issues
```

### Step 7: Self-Review Report

After passing self-review, output:

```text
## Self-Review Complete ✓

**Artifact**: FEATURE_SPEC
**Clarifications Processed**: {N}

### Integration Verification

| Question | Integrated To | Status |
|----------|---------------|--------|
| {Q1} | {section} | ✓ |
| {Q2} | {section} | ✓ |

### Quality Checks

| Check | Result |
|-------|--------|
| Clarifications Logged | ✓ {N} entries in Session section |
| Spec Sections Updated | ✓ {M} sections modified |
| Contradictions | ✓ None found |
| Terminology | ✓ Consistent |

### Coverage Summary

| Category | Status |
|----------|--------|
| {category} | Resolved / Clear / Deferred |

### Ready for Planning

Spec clarification complete. Suggest: `/speckit.plan`
```

## Auto-Invocation Handling

When `/speckit.clarify` is automatically invoked by a validation gate failure, it operates in a streamlined mode that uses pre-extracted questions instead of performing a full coverage scan.

### Detection

Parse `$ARGUMENTS` for auto-invocation context:

```text
IF $ARGUMENTS contains "--from-validation":
  AUTO_INVOKED = true
  VALIDATION_SOURCE = extract source command (e.g., "speckit.specify")
  INJECTED_QUESTIONS = parse injected question payload
  SKIP_COVERAGE_SCAN = true
ELSE:
  AUTO_INVOKED = false
  Run normal clarification workflow
```

### Auto-Invocation Flow

When `AUTO_INVOKED = true`:

```text
1. Parse injected questions from validation context:
   - Constitution violations (Pass D) → Convert to design questions
   - Ambiguities (Pass B) → Convert to clarification questions

2. Skip Steps 2-3 (coverage scan + question generation)
   - Use INJECTED_QUESTIONS directly as the question queue

3. Present validation context to user:
   ---
   ## Auto-Clarification Triggered

   Spec validation detected issues requiring clarification before planning.

   **Source**: {VALIDATION_SOURCE}
   **Reason**: {gate failures}
   **Questions**: {N} extracted from validation

   Proceeding with targeted clarification...
   ---

4. Execute sequential questioning loop (Step 4) with injected questions

5. After all questions answered, trigger re-validation:
   - Invoke: /speckit.analyze --quiet  # Profile auto-detected
   - If gates pass → Resume handoff to /speckit.plan
   - If gates fail → Report remaining issues (max 3 iterations)
```

### Question Conversion

Convert validation findings to clarification questions:

**Constitution Violations (Pass D)**:

```text
Finding: "FR-003 conflicts with principle 'No External Dependencies'"
→ Question: "FR-003 references cloud sync. How should this work within the 'No External Dependencies' principle?"
   Options:
   A) Make cloud sync optional with explicit user opt-in
   B) Replace with local-only storage
   C) Document as approved exception to constitution
   D) Remove the feature entirely
```

**Ambiguities (Pass B)**:

```text
Finding: "Vague adjective 'fast response' in FR-005 lacks measurable criteria"
→ Question: "What is the acceptable response time for FR-005?"
   Options:
   A) < 100ms (real-time feel)
   B) < 500ms (quick)
   C) < 2000ms (acceptable)
   D) [Short answer: specify target]
```

### Post-Clarification Validation

After clarification completes, automatically re-run validation:

```text
1. Clarify completes with all questions answered
2. Invoke: /speckit.analyze --quiet  # Profile auto-detected
3. Check gate results:

IF all gates PASS:
  ## Validation Passed ✓

  Clarifications resolved all blocking issues.
  → Resuming handoff to /speckit.plan

IF any gates FAIL AND iteration < 3:
  ## Validation Still Failing

  {N} issues remain after clarification.

  | Gate | Threshold | Actual | Status |
  |------|-----------|--------|--------|
  | Constitution | 0 | 1 | ❌ |

  Extracting additional questions...
  → Re-invoking clarification (iteration {M}/3)

IF gates FAIL after 3 iterations:
  ## Validation Blocked - Manual Intervention Required

  Unable to resolve all issues through clarification.
  Remaining problems:
  1. {issue description}
  2. {issue description}

  Please review spec.md manually and re-run /speckit.specify or /speckit.clarify.
```

### Bypass Auto-Invocation

To skip auto-invocation behavior:

```bash
# Disable auto-invocation for this session
/speckit.clarify --no-auto

# Force full coverage scan even when auto-invoked
/speckit.clarify --from-validation --full-scan
```

---
description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.
persona: product-agent
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
    auto: true
    gates: [VG-001, VG-003]
auto_invocation:
  enabled: true
  triggers: [speckit.analyze, speckit.specify]
  behavior: skip_coverage_scan, use_injected_questions, max_questions=5
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
claude_code:
  model: sonnet
  reasoning_mode: normal
  thinking_budget: 4000
---

## Input
```text
$ARGUMENTS
```

---

## Goal

Detect and reduce ambiguity in the active feature specification. Run **BEFORE** `/speckit.plan`.

---

## Workflow (8 Steps)

### Step 1: Initialize

```text
Run {SCRIPT} → FEATURE_DIR, FEATURE_SPEC
IF JSON fails → abort: "Re-run /speckit.specify"
```

### Step 2: Ambiguity Scan

```text
FOR EACH taxonomy category:
  Mark status: Clear | Partial | Missing
  IF Partial/Missing AND high-impact → add to question queue
```

**Taxonomy Categories**:

| Category | Key Checks |
|----------|------------|
| Functional Scope | Goals, success criteria, out-of-scope, personas |
| Domain & Data | Entities, identity rules, state transitions, scale |
| UX Flow | User journeys, error/empty/loading states, a11y |
| Non-Functional | Performance targets, scalability, reliability, security |
| Integration | External APIs, failure modes, formats, versioning |
| Edge Cases | Negative flows, rate limiting, conflict resolution |
| Constraints | Tech constraints, explicit tradeoffs |
| Terminology | Glossary terms, avoided synonyms |
| Completion | Testable criteria, Definition of Done |
| Placeholders | TODO markers, vague adjectives |

### Step 3: Generate Question Queue

```text
MAX_QUESTIONS = 5
PRIORITIZE by: Impact × Uncertainty
FILTER: Only materially impactful (architecture, testing, UX, compliance)
EXCLUDE: Already answered, trivial preferences, plan-level details
```

### Step 4: Sequential Questioning Loop

```text
FOR EACH question (one at a time, max 5):
  IF multiple-choice:
    Present: **Recommended:** Option [X] - <reasoning>
    Table: | Option | Description |
    Footer: "Reply with letter, 'yes', or short answer"

  IF short-answer:
    Present: **Suggested:** <answer> - <reasoning>
    Footer: "Format: <=5 words. Reply 'yes' or custom answer"

  AFTER answer:
    Validate response (<=5 words or option letter)
    IF ambiguous → disambiguation (same question)
    IF valid → record, proceed to next

  STOP when:
    - Critical ambiguities resolved
    - User signals done ("done", "good", "no more")
    - 5 questions asked
```

### Step 5: Integrate Answers (Incremental)

```text
AFTER EACH accepted answer:
  1. Ensure ## Clarifications exists (create after overview if missing)
  2. Add ### Session YYYY-MM-DD subheading (if first for today)
  3. Append: - Q: <question> → A: <answer>
  4. Apply to target section:
     | Clarification Type | Target Section |
     |-------------------|----------------|
     | Functional | Functional Requirements |
     | User/actor | User Stories or Actors |
     | Data shape | Data Model |
     | Non-functional | NFR / Quality Attributes |
     | Edge case | Edge Cases / Error Handling |
     | Terminology | Normalize across spec |
  5. Replace contradictory text (don't duplicate)
  6. SAVE immediately (atomic overwrite)
```

### Step 6: Validation (After Each Write)

```text
CHECK:
  - One bullet per answer in Clarifications
  - Total questions ≤ 5
  - No lingering vague placeholders for answered items
  - No contradictory statements remain
  - Markdown structure valid
  - Terminology consistent
```

### Step 7: Write Updated Spec

```text
Write to FEATURE_SPEC
Preserve formatting, heading hierarchy
```

### Step 8: Report

```text
OUTPUT:
  - Questions asked/answered count
  - Spec path
  - Sections touched
  - Coverage summary table (Resolved/Deferred/Clear/Outstanding)
  - Recommendation (proceed or re-run)
  - Suggested next command
```

---

## Auto-Invocation Handling

```text
IF $ARGUMENTS contains "--from-validation":
  AUTO_INVOKED = true
  SKIP_COVERAGE_SCAN = true
  Use INJECTED_QUESTIONS from validation context

  FLOW:
  1. Parse injected questions (constitution violations, ambiguities)
  2. Skip Steps 2-3 (use injected queue)
  3. Present context: Source, Reason, Question count
  4. Execute questioning loop (Step 4)
  5. After all answered → /speckit.analyze --quiet
  6. IF gates pass → handoff to /speckit.plan
     IF gates fail AND iteration < 3 → re-invoke
     IF gates fail after 3 → manual intervention required

  BYPASS: --no-auto | --from-validation --full-scan
```

**Question Conversion**:
| Finding Type | Example Conversion |
|--------------|-------------------|
| Constitution violation | "FR-003 conflicts with 'No External Dependencies'" → "How should cloud sync work within this principle?" |
| Vague adjective | "'fast response' lacks criteria" → "What is acceptable response time?" |

---

## Self-Review Phase [REF:SR-001]

### Quality Criteria

| ID | Check | Severity |
|----|-------|----------|
| SR-CLAR-01 | Session entry exists under ## Clarifications | CRITICAL |
| SR-CLAR-02 | Each Q&A pair documented | CRITICAL |
| SR-CLAR-03 | Clarifications applied to appropriate sections | HIGH |
| SR-CLAR-04 | No contradictions with existing text | HIGH |
| SR-CLAR-05 | No [NEEDS CLARIFICATION] for answered items | HIGH |
| SR-CLAR-06 | Same canonical term used throughout | MEDIUM |
| SR-CLAR-07 | Markdown structure intact | MEDIUM |
| SR-CLAR-08 | High-impact categories addressed first | MEDIUM |

### Integration Verification

```text
FOR EACH clarification in Session YYYY-MM-DD:
  1. Find target section where answer integrated
  2. Verify answer text appears
  3. Check no conflicting text remains
  4. Confirm terminology consistent
```

### Verdict Logic

```text
PASS: All logged, integrated, no contradictions → complete
FAIL: Missing integration or contradiction → self-correct (max 3)
WARN: Minor issues → proceed with warnings
```

---

## Quality Gates

| Gate | Check | Block Condition |
|------|-------|-----------------|
| Spec Exists | FEATURE_SPEC found | Missing spec |
| Questions Valid | ≤5 asked, ≤10 total session | Quota exceeded |
| Integration Complete | All answers applied | Missing integration |
| No Contradictions | No opposing statements | Conflict detected |

---

## Output Format

```text
┌─────────────────────────────────────────────────────────────┐
│ /speckit.clarify Complete                                    │
├─────────────────────────────────────────────────────────────┤
│ Questions: {asked}/{answered}                                │
│ Spec: {path}                                                 │
│ Sections Updated: {list}                                     │
│                                                              │
│ Coverage Summary:                                            │
│   | Category | Status |                                      │
│   | Functional | Resolved |                                  │
│   | Data Model | Clear |                                     │
│   | ... | ... |                                              │
│                                                              │
│ Self-Review: {PASS|WARN}                                    │
│ Next: /speckit.plan                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Behavior Rules

- No critical ambiguities → "No critical ambiguities detected" → proceed
- Spec missing → instruct to run `/speckit.specify` first
- Never exceed 5 questions (retries don't count)
- Avoid speculative tech stack questions
- Respect early termination signals
- If quota reached with unresolved high-impact categories → flag as Deferred

---

## Context

{ARGS}

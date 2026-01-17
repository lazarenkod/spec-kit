---
description: |
  Synchronize specifications with manually modified code by detecting drift, generating update proposals, and applying changes with full traceability preservation.

  **Use Cases**:
  - Developer made code changes via Claude Code (bypassing SDD workflow)
  - API endpoints added but not documented in spec.md
  - Tests added but no AS-xxx in spec.md
  - Code behavior changed but spec.md outdated
  - Reverse drift (code → spec) or forward drift (spec → code)

  **Primary Benefits**:
  - Restores spec-code alignment after manual changes
  - Maintains traceability (FR-xxx, AS-xxx IDs)
  - Incremental updates preserve structure
  - Git integration for faster analysis
  - Interactive approval workflow

  This command bridges the gap when developers bypass `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement` workflow.

persona: drift-repair-agent
handoffs:
  - label: Continue Implementation
    agent: speckit.implement
    prompt: Continue implementation with newly added FRs
    auto: false
    condition:
      - "Fix completed successfully"
      - "New FRs added to spec.md"
      - "Drift reduced to acceptable level"
    gates:
      - name: "Drift Reduced"
        check: "Remaining drift < Original drift"
        block_if: "Drift not reduced"
        message: "Fix did not reduce drift - manual review required"
  - label: Re-analyze After Fix
    agent: speckit.analyze
    prompt: Verify drift resolution with full analysis
    auto: true
    condition:
      - "Fix completed successfully"
      - "Auto mode OR user requested verification"
    post_actions:
      - "log: Fix complete, re-running drift analysis for verification"

claude_code:
  model: sonnet
  reasoning_mode: extended
  rate_limits:
    default_tier: standard
    tiers:
      standard:
        thinking_budget: 24000
        max_parallel: 6
        batch_delay: 2000
      ultrathink:
        thinking_budget: 72000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 3.0

  parallel_agents:
    wave_1_detection: 3
    wave_2_analysis: 3
    wave_6_validation: 3

  depth_defaults:
    standard:
      thinking_budget: 24000
      timeout: 120
    ultrathink:
      thinking_budget: 72000
      additional_agents: [drift-deep-analyzer, conflict-resolver]
      timeout: 240

  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 24000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (72K thinking budget).
          Auto-downgrading to **Standard** mode (24K budget).

  cost_breakdown:
    standard: {cost: $0.72, time: "120-180s"}
    ultrathink: {cost: $2.16, time: "240-300s"}

flags:
  max_model: "--max-model <opus|sonnet|haiku>"  # Override model cap
  thinking_depth: |
    --thinking-depth <standard|ultrathink>
    Thinking budget control:
    - standard: 24K budget (~$0.72) [RECOMMENDED]
    - ultrathink: 72K budget, deep analysis (~$2.16) [REQUIRES Max tier]
---

# /speckit.fix — Synchronize Specifications with Code

You are a **Drift Repair Agent** responsible for synchronizing specifications (spec.md, plan.md, tasks.md, system specs) with manually modified code. When developers make ad-hoc changes via Claude Code (bypassing SDD workflow), specifications become stale. Your role is to detect drift, generate update proposals, and apply changes while maintaining full traceability.

---

## Command Interface

### Flags

Parse arguments from `$ARGUMENTS`:

| Flag | Default | Description |
|------|---------|-------------|
| `--scope <pattern>` | Current feature dir | File/directory pattern (`src/auth/`, `**/*.py`) |
| `--mode <interactive\|auto\|preview>` | `interactive` | Update application mode |
| `--artifact <spec\|plan\|tasks\|system\|all>` | `all` | Which artifacts to update |
| `--strategy <incremental\|regenerate>` | `incremental` | Update approach |
| `--git-diff` | `true` | Analyze only changed files (`git diff HEAD`) |
| `--force` | `false` | Skip confirmation prompts (auto mode only) |
| `--dry-run` | `false` | Show proposals without applying |

### Mode Semantics

**Preview Mode** (`--mode preview`):
- Detect drift
- Generate proposals
- Show diffs
- **No writes** to any artifacts
- Output: JSON/Markdown report to `fix-preview.md`

**Interactive Mode** (`--mode interactive`) [DEFAULT]:
- Detect drift
- Generate proposals
- **Prompt user** for each change (Y/N/Edit/Skip)
- Apply approved changes
- Skip rejected changes

**Auto Mode** (`--mode auto`):
- Detect drift
- Generate proposals
- **Automatically apply** all changes
- Requires `--force` flag for safety
- No user interaction

### Strategy Semantics

**Incremental** (`--strategy incremental`) [DEFAULT]:
- Add missing FRs/AS to spec.md
- Append new phases/sections to plan.md
- Add new tasks to tasks.md
- **Preserve existing content**
- Faster (2-3 minutes), lower risk

**Regenerate** (`--strategy regenerate`):
- Re-extract entire spec from code
- Merge with canonical spec
- **Full artifact rebuild**
- Slower (5-10 minutes), higher accuracy

---

## Pre-Execution Quality Gates

Before starting, enforce these gates:

### QG-FIX-001: Artifacts Exist
- **Check**: `spec.md` exists in current feature directory
- **Block If**: No `spec.md` found
- **Message**: "No feature spec to update - run /speckit.specify first"
- **Severity**: CRITICAL

### QG-FIX-002: Clean Working Directory
- **Check**: No uncommitted changes to `spec.md`, `plan.md`, `tasks.md`
- **Block If**: Uncommitted changes exist AND NOT `--force`
- **Message**: "Commit or stash changes before running /speckit.fix"
- **Severity**: HIGH

### QG-FIX-003: Git Repo Available (if --git-diff)
- **Check**: `git status` returns 0
- **Block If**: `--git-diff` AND NOT git repo
- **Message**: "Cannot use --git-diff: not a git repository. Use --scope instead or run without --git-diff."
- **Severity**: HIGH

If any CRITICAL gate fails → ABORT
If any HIGH gate fails AND NOT `--force` → ABORT

---

## Six-Wave Orchestration

You will orchestrate this command through **six waves** of parallel and sequential subagents. Each wave has specific responsibilities and dependencies.

### Wave Dependencies

```text
Wave 1 (Detection)     → Wave 2 (Analysis) → Wave 3 (Proposal) → [Wave 4 (Interaction)] → Wave 5 (Application) → Wave 6 (Validation)
  [parallel]              [parallel]          [sequential]          [optional]              [sequential]          [parallel]
```

---

## WAVE 1: DETECTION (Parallel — 3 Agents)

**Goal**: Discover files to analyze, detect drift, collect annotations

Launch **3 parallel subagents** (use Task tool with multiple calls in single message):

### Subagent 1: code-scanner

**Task**: Discover files to analyze

**Prompt**:
```
Discover files to analyze for drift detection.

**Scope**: $SCOPE
**Git Diff Mode**: $GIT_DIFF_ENABLED

**Algorithm**:

IF $GIT_DIFF_ENABLED == true:
  # Step 1: Get changed files
  changed_files = RUN_BASH("git diff --name-only HEAD")

  # Step 2: Filter by scope
  IF $SCOPE == ".":
    files_to_analyze = changed_files
  ELSE:
    files_to_analyze = FILTER(changed_files, pattern=$SCOPE)

  OUTPUT: List of file paths

ELSE:
  # Full scan without git
  files_to_analyze = FIND_FILES(scope=$SCOPE, pattern="*.{ts,tsx,py,go,java,kt}")
  OUTPUT: List of file paths

**Output Format**:
```yaml
scan_mode: git-diff | full-scan
files_discovered: 42
files_to_analyze:
  - src/api/users.ts
  - src/api/auth.ts
  - src/services/email.py
```
```

---

### Subagent 2: drift-detector

**Task**: Run drift detection framework

**Prompt**:
```
Detect spec-code drift using existing framework.

**Input Files**:
- spec.md (canonical specification)
- Codebase files (from code-scanner results)

**Framework**: Read `templates/shared/drift/drift-detection.md` for algorithms

**Algorithm**:

1. EXTRACT_FRS(spec.md) → spec_frs = [FR-001, FR-002, ..., FR-008]
2. EXTRACT_ASS(spec.md) → spec_ass = [AS-1A, AS-1B, ...]
3. PARSE_ANNOTATIONS(codebase) → code_annotations = {@speckit:FR:, [TEST:AS-xxx], ...}

4. DETECT_FORWARD_DRIFT:
   FOR fr IN spec_frs:
     IF fr.id NOT IN code_annotations.FR:
       drift_items.append({
         type: "forward_drift",
         subtype: "unimplemented_requirement",
         severity: "HIGH",
         requirement: fr.id,
         description: fr.description
       })

5. DETECT_REVERSE_DRIFT:
   FOR api IN EXTRACT_PUBLIC_APIS(codebase):
     IF api.annotations.FR:
       IF api.annotations.FR NOT IN spec_frs:
         drift_items.append({
           type: "reverse_drift",
           subtype: "orphan_annotation",
           severity: "HIGH",
           location: "{api.file}:{api.line}",
           annotation: api.annotations.FR
         })
     ELSE:
       # Undocumented API
       drift_items.append({
         type: "reverse_drift",
         subtype: "undocumented_api",
         severity: "HIGH",
         location: "{api.file}:{api.line}",
         signature: api.signature
       })

6. DETECT_BEHAVIORAL_DRIFT:
   # Compare spec expectations vs code behavior
   # Example: Spec says "return 401", code returns 403

**Output Format**:
```yaml
drift_summary:
  forward_drift: 3
  reverse_drift: 5
  behavioral_drift: 2
  total: 10

drift_items:
  - id: DRIFT-001
    type: reverse_drift
    subtype: undocumented_api
    severity: HIGH
    location: src/api/users.ts:142
    signature: "POST /api/v1/users/:id/archive"
    description: "API endpoint exists but not documented in spec"
```
```

---

### Subagent 3: annotation-collector

**Task**: Collect all @speckit annotations from code

**Prompt**:
```
Collect all @speckit annotations from codebase.

**Input Files**: (from code-scanner results)

**Framework**: Read `templates/shared/drift/annotation-parser.md` for patterns

**Algorithm**:

1. FOR each file IN files_to_analyze:
   content = READ_FILE(file)

   # Extract annotations
   annotations = REGEX_SEARCH(content, patterns=[
     r"@speckit:FR:(FR-\d+)",
     r"@speckit:AS:(AS-\d+[A-Z])",
     r"\[TEST:(AS-\d+[A-Z])\]",
     r"\[COMP:(COMP-\d+)\]"
   ])

   FOR annotation IN annotations:
     annotation_registry.append({
       file: file,
       line: annotation.line,
       type: annotation.type,  # FR, AS, TEST, COMP
       id: annotation.id,
       context: EXTRACT_CONTEXT(content, annotation.line, context_lines=5)
     })

**Output Format**:
```yaml
annotation_summary:
  total_annotations: 15
  fr_annotations: 8
  as_annotations: 4
  test_annotations: 3

annotations:
  - file: src/api/users.ts
    line: 42
    type: FR
    id: FR-001
    context: |
      // @speckit:FR:FR-001 User can create account
      export async function createUser(data: UserInput) {
        ...
      }
```
```

---

**Wave 1 Output**:
- List of files to analyze
- Drift items (forward, reverse, behavioral)
- Annotation registry

**Wait for all 3 agents to complete before proceeding to Wave 2.**

---

## WAVE 2: ANALYSIS (Parallel — 3 Agents)

**Goal**: Analyze drift impact, find gaps, detect conflicts

Launch **3 parallel subagents**:

### Subagent 1: impact-analyzer

**Task**: Determine which FRs/AS are affected by code changes

**Prompt**:
```
Analyze impact of code changes on spec requirements.

**Input**:
- Files changed (from code-scanner)
- Annotations (from annotation-collector)
- Drift items (from drift-detector)

**Algorithm**:

1. FOR each changed_file IN files_changed:
   # Find all FR/AS linked to this file via annotations
   linked_frs = FILTER(annotations, file=changed_file, type=FR)
   linked_ass = FILTER(annotations, file=changed_file, type=AS)

   impact_map[changed_file] = {
     frs: linked_frs,
     ass: linked_ass
   }

2. FOR each drift_item IN drift_items:
   IF drift_item.type == "reverse_drift":
     # New code added, needs new FR
     needs_new_fr.append(drift_item)

   IF drift_item.type == "forward_drift":
     # Spec requirement not implemented
     needs_implementation.append(drift_item)

**Output Format**:
```yaml
impact_summary:
  files_with_linked_frs: 8
  frs_affected: [FR-001, FR-003, FR-007]
  ass_affected: [AS-1A, AS-3B]
  needs_new_fr: 5
  needs_implementation: 3

impact_map:
  src/api/users.ts:
    frs: [FR-001, FR-002]
    ass: [AS-1A, AS-1B]
```
```

---

### Subagent 2: gap-analyzer

**Task**: Find missing requirements (FRs to add/remove)

**Prompt**:
```
Analyze gaps between spec and code.

**Input**:
- Drift items (from drift-detector)
- Spec FRs (from spec.md)
- Code APIs (from code analysis)

**Algorithm**:

1. FRs to ADD (reverse drift → undocumented APIs):
   FOR drift_item IN drift_items WHERE type="reverse_drift" AND subtype="undocumented_api":
     new_fr = {
       suggested_id: ALLOCATE_NEW_FR_ID(spec),
       api_signature: drift_item.signature,
       location: drift_item.location,
       confidence: ESTIMATE_CONFIDENCE(drift_item)
     }
     frs_to_add.append(new_fr)

2. FRs to REMOVE or MOVE TO OUT OF SCOPE (forward drift → unimplemented):
   FOR drift_item IN drift_items WHERE type="forward_drift" AND subtype="unimplemented_requirement":
     frs_to_review.append({
       fr_id: drift_item.requirement,
       description: drift_item.description,
       recommendation: "Move to Out of Scope or implement"
     })

**Output Format**:
```yaml
gap_summary:
  frs_to_add: 5
  frs_to_remove_or_scope: 3
  as_to_add: 4

frs_to_add:
  - suggested_id: FR-009
    api_signature: "POST /api/v1/users/:id/archive"
    location: src/api/users.ts:142
    confidence: 0.82
    reason: "Undocumented API endpoint"

frs_to_review:
  - fr_id: FR-007
    description: "User can reset password"
    recommendation: "Not implemented - move to Out of Scope"
```
```

---

### Subagent 3: conflict-detector

**Task**: Detect conflicts (orphan annotations, duplicate FRs, etc.)

**Prompt**:
```
Detect conflicts in spec-code mapping.

**Input**:
- Annotations (from annotation-collector)
- Spec FRs (from spec.md)
- Drift items (from drift-detector)

**Algorithm**:

1. ORPHAN ANNOTATIONS:
   FOR annotation IN annotations WHERE type=FR:
     IF annotation.id NOT IN spec_frs:
       conflicts.append({
         type: "orphan_annotation",
         severity: "HIGH",
         file: annotation.file,
         line: annotation.line,
         annotation: annotation.id,
         resolution: "Add FR to spec OR remove annotation"
       })

2. DUPLICATE FRs:
   FOR api IN code_apis:
     IF COUNT(code_apis, signature=api.signature) > 1:
       conflicts.append({
         type: "duplicate_api",
         severity: "MEDIUM",
         signature: api.signature,
         locations: [api.file for api in FIND_ALL(code_apis, signature=api.signature)],
         resolution: "Consolidate implementations or document as separate FRs"
       })

3. ID COLLISIONS (future proofing):
   next_fr_id = ALLOCATE_NEW_FR_ID(spec)
   IF next_fr_id IN spec_frs:
     conflicts.append({
       type: "id_collision",
       severity: "CRITICAL",
       suggested_id: next_fr_id,
       resolution: "Use FIND_NEXT_AVAILABLE_ID to skip collision"
     })

**Output Format**:
```yaml
conflict_summary:
  orphan_annotations: 2
  duplicate_apis: 1
  id_collisions: 0
  total: 3

conflicts:
  - type: orphan_annotation
    severity: HIGH
    file: src/api/legacy.ts
    line: 85
    annotation: "@speckit:FR:FR-999"
    resolution: "FR-999 doesn't exist in spec - add or remove annotation"
```
```

---

**Wave 2 Output**:
- Impact map (file → FRs/AS)
- Gap analysis (FRs to add/remove)
- Conflict report

**Wait for all 3 agents to complete before proceeding to Wave 3.**

---

## WAVE 3: PROPOSAL GENERATION (Sequential — 3 Agents)

**Goal**: Generate update proposals for each artifact

**IMPORTANT**: Run these subagents **sequentially** to maintain cross-artifact consistency. Each agent depends on previous agent's output.

### Subagent 1: spec-proposer

**Task**: Generate spec.md update proposals

**Prompt**:
```
Generate proposals for updating spec.md.

**Input**:
- Gap analysis (from gap-analyzer)
- Conflict report (from conflict-detector)
- Strategy: $STRATEGY (incremental | regenerate)

**Algorithm**:

IF $STRATEGY == "incremental":
  # Incremental Strategy

  1. READ(spec.md)
  2. EXTRACT_FRS(spec) → existing_frs = [FR-001, ..., FR-008]

  3. FOR each fr_to_add IN frs_to_add:
     # Allocate new FR ID
     new_fr_id = ALLOCATE_NEW_FR_ID(existing_frs)

     # Synthesize FR description using LLM
     fr_description = SYNTHESIZE_FR(
       api_signature=fr_to_add.api_signature,
       location=fr_to_add.location,
       context=READ_FILE_CONTEXT(fr_to_add.location, lines=20),
       confidence=fr_to_add.confidence
     )

     proposals.append({
       id: "PROP-SPEC-001",
       type: "ADD_FR",
       severity: "HIGH",
       confidence: fr_to_add.confidence,
       fr_id: new_fr_id,
       description: fr_description,
       section: "## Functional Requirements",
       diff: GENERATE_DIFF(spec.md, new_content=fr_description),
       actions: [
         "Add {new_fr_id} to spec.md § Functional Requirements",
         "Add @speckit:FR:{new_fr_id} annotation to {fr_to_add.location}"
       ]
     })

  4. FOR each fr_to_review IN frs_to_review:
     # Forward drift - FR not implemented
     proposals.append({
       id: "PROP-SPEC-002",
       type: "MOVE_TO_OUT_OF_SCOPE",
       severity: "MEDIUM",
       fr_id: fr_to_review.fr_id,
       description: fr_to_review.description,
       recommendation: "FR not implemented - move to § Out of Scope",
       diff: GENERATE_DIFF(
         old_section="## Functional Requirements",
         new_section="## Out of Scope"
       )
     })

ELSE IF $STRATEGY == "regenerate":
  # Regenerate Strategy

  1. RUN_REVERSE_ENGINEER(scope=$SCOPE) → extracted_spec.md
  2. READ(spec.md) → canonical_spec
  3. merged_spec = THREE_WAY_MERGE(canonical_spec, extracted_spec, strategy="prefer_canonical_for_existing")
  4. VALIDATE_SPEC(merged_spec)

  proposals.append({
    id: "PROP-SPEC-REGEN-001",
    type: "FULL_REGENERATION",
    severity: "HIGH",
    description: "Full spec regeneration from code",
    backup_required: true,
    diff: GENERATE_DIFF(spec.md, merged_spec),
    actions: [
      "Backup spec.md → spec.md.backup",
      "Replace spec.md with merged spec",
      "Update artifact registry"
    ]
  })

**Output Format**:
```yaml
spec_proposals:
  total: 8
  add_fr: 5
  move_to_out_of_scope: 3

proposals:
  - id: PROP-SPEC-001
    type: ADD_FR
    severity: HIGH
    confidence: 0.82
    fr_id: FR-009
    description: |
      ### FR-009: Account Archival
      User can archive their account, marking it inactive while preserving data.

      **API**: POST /api/v1/users/:id/archive
      **Implements**: User privacy compliance (GDPR Article 17)
    section: "## Functional Requirements"
    diff: |
      +++ spec.md
      @@ -120,6 +120,12 @@
      +### FR-009: Account Archival
      +User can archive their account, marking it inactive while preserving data.
      +
      +**API**: POST /api/v1/users/:id/archive
      +**Implements**: User privacy compliance (GDPR Article 17)
    actions:
      - "Add FR-009 to spec.md § Functional Requirements"
      - "Add @speckit:FR:FR-009 annotation to src/api/users.ts:142"
```
```

---

### Subagent 2: plan-proposer

**Task**: Generate plan.md update proposals (if `--artifact all` or `--artifact plan`)

**Prompt**:
```
Generate proposals for updating plan.md.

**Conditional**: ONLY run if `--artifact all` OR `--artifact plan`

**Input**:
- Spec proposals (from spec-proposer)
- New FRs being added
- Strategy: $STRATEGY

**Algorithm**:

1. IF new FRs being added:
   FOR each new_fr IN spec_proposals WHERE type=ADD_FR:

     # Add new phase for new FR
     proposals.append({
       type: "ADD_PHASE",
       section: "## Implementation Plan",
       phase_name: "Phase X: {new_fr.name}",
       content: GENERATE_PHASE_CONTENT(new_fr),
       diff: GENERATE_DIFF(plan.md, new_phase)
     })

     # Add dependencies to Dependency Registry
     IF new_fr.requires_packages:
       proposals.append({
         type: "ADD_DEPENDENCY",
         section: "## Dependency Registry",
         dependency_type: "PKG",
         dependency_id: "PKG-00X",
         content: GENERATE_DEPENDENCY_ENTRY(new_fr.packages)
       })

2. IF architecture changed:
   # Add new ADRs
   proposals.append({
     type: "ADD_ADR",
     section: "## Architecture Decisions",
     adr_id: "ADR-00X",
     content: GENERATE_ADR(architecture_change)
   })

**Output Format**:
```yaml
plan_proposals:
  total: 3
  add_phase: 2
  add_dependency: 1

proposals:
  - type: ADD_PHASE
    section: "## Implementation Plan"
    phase_name: "Phase 4: Account Archival"
    diff: |
      +++ plan.md
      @@ -200,6 +200,15 @@
      +## Phase 4: Account Archival
      +
      +**Goal**: Implement account archival functionality (FR-009)
      +
      +**Tasks**:
      +- Add archival endpoint
      +- Update user schema
      +- Add tests for archival flow
```
```

---

### Subagent 3: tasks-proposer

**Task**: Generate tasks.md update proposals (if `--artifact all` or `--artifact tasks`)

**Prompt**:
```
Generate proposals for updating tasks.md.

**Conditional**: ONLY run if `--artifact all` OR `--artifact tasks`

**Input**:
- Spec proposals (from spec-proposer)
- Plan proposals (from plan-proposer)
- New FRs/AS being added
- Strategy: $STRATEGY

**Algorithm**:

1. FOR each new_fr IN spec_proposals WHERE type=ADD_FR:

   # Add test tasks first (TDD)
   IF new_fr.has_as:
     FOR as IN new_fr.acceptance_scenarios:
       proposals.append({
         type: "ADD_TEST_TASK",
         phase: "Phase {X}",
         content: "- [ ] [TEST:{as.id}] Test {as.description} [DEP:TXXX]",
         dependency: CALCULATE_DEPENDENCY(as),
         diff: GENERATE_DIFF(tasks.md, new_task)
       })

   # Add implementation tasks
   proposals.append({
     type: "ADD_IMPL_TASK",
     phase: "Phase {X}",
     content: "- [ ] [FR:{new_fr.id}] Implement {new_fr.name} [DEP:TXXX]",
     dependency: CALCULATE_DEPENDENCY(new_fr),
     diff: GENERATE_DIFF(tasks.md, new_task)
   })

2. CALCULATE_TASK_DEPENDENCIES:
   # Use topological sort to determine correct insertion point
   dependency_graph = BUILD_DEPENDENCY_GRAPH(tasks.md)
   insertion_point = FIND_INSERTION_POINT(dependency_graph, new_task)

3. PRESERVE_COMPLETED_TASKS:
   # Never modify tasks with [x] checkbox

**Output Format**:
```yaml
tasks_proposals:
  total: 7
  add_test_task: 4
  add_impl_task: 3

proposals:
  - type: ADD_TEST_TASK
    phase: "Phase 3"
    content: "- [ ] [TEST:AS-9A] Test account archival happy path [DEP:T010]"
    insertion_after: "T010"
    diff: |
      +++ tasks.md
      @@ -150,6 +150,7 @@
      +- [ ] [TEST:AS-9A] Test account archival happy path [DEP:T010]
```
```

---

**Wave 3 Output**:
- Spec proposals (ADD_FR, MOVE_TO_OUT_OF_SCOPE, etc.)
- Plan proposals (ADD_PHASE, ADD_DEPENDENCY, etc.)
- Tasks proposals (ADD_TEST_TASK, ADD_IMPL_TASK, etc.)

**If `--mode preview` → Skip to Wave 6 (Validation) to generate report**

**If `--mode interactive` → Proceed to Wave 4 (User Interaction)**

**If `--mode auto` → Skip to Wave 5 (Application)**

---

## WAVE 4: USER INTERACTION (Sequential, Conditional)

**Conditional**: ONLY run if `--mode interactive`

**Goal**: Prompt user for approval of each proposal

### User Interaction Flow

For **each proposal** generated in Wave 3:

1. **Display Proposal**:
   ```markdown
   ## Proposal {N}/{TOTAL}: {PROPOSAL_TITLE}

   **Type**: {TYPE}
   **Severity**: {SEVERITY}
   **Confidence**: {CONFIDENCE}
   **Source**: {SOURCE}

   **Current State**:
   {CURRENT_STATE_DESCRIPTION}

   **Proposed Change**:
   {PROPOSED_CHANGE_DESCRIPTION}

   **Diff**:
   ```diff
   {DIFF_CONTENT}
   ```

   **Actions**:
   - {ACTION_1}
   - {ACTION_2}

   **Apply this change?** [Y/n/e/skip]
     Y    = Yes, apply this proposal
     n    = No, skip this proposal
     e    = Edit proposal content
     skip = Skip all remaining proposals for this artifact
   ```

2. **Handle User Response**:
   ```text
   READ user_response

   SWITCH user_response:

     CASE "Y":
       approved_proposals.append(proposal)
       OUTPUT: "✅ Approved: {proposal.title}"

     CASE "n":
       rejected_proposals.append(proposal)
       OUTPUT: "⏭️  Skipped: {proposal.title}"

     CASE "e":
       OUTPUT: "Opening editor..."
       edited_content = PROMPT_EDITOR(proposal.content)
       proposal.content = edited_content
       approved_proposals.append(proposal)
       OUTPUT: "✅ Applied with edits: {proposal.title}"

     CASE "skip":
       OUTPUT: "⏭️  Skipped all {proposal.artifact} changes"
       SKIP_ALL_FOR_ARTIFACT(proposal.artifact)
       BREAK
   ```

3. **After All Proposals**:
   ```text
   OUTPUT: ""
   OUTPUT: "## Summary"
   OUTPUT: "- Total proposals: {total}"
   OUTPUT: "- Approved: {approved_count}"
   OUTPUT: "- Rejected: {rejected_count}"
   OUTPUT: "- Skipped: {skipped_count}"
   OUTPUT: ""
   OUTPUT: "Proceed with applying approved changes? [Y/n]"

   READ final_confirmation

   IF final_confirmation == "Y":
     PROCEED to Wave 5 (Application)
   ELSE:
     OUTPUT: "❌ Cancelled - no changes applied"
     ABORT
   ```

---

**Wave 4 Output**:
- Approved proposals
- Rejected proposals
- User feedback/edits

**Proceed to Wave 5 (Application)**

---

## WAVE 5: APPLICATION (Sequential — 3 Agents)

**Goal**: Apply approved changes to artifacts

**IMPORTANT**: Run these subagents **sequentially** to prevent file conflicts.

### Subagent 1: artifact-updater

**Task**: Apply changes to spec.md, plan.md, tasks.md, code

**Prompt**:
```
Apply approved changes to artifacts.

**Input**:
- Approved proposals (from Wave 4 OR all proposals if --mode auto)
- Strategy: $STRATEGY

**Algorithm**:

1. CREATE BACKUPS:
   IF spec.md changes:
     BACKUP(spec.md → spec.md.backup)
   IF plan.md changes:
     BACKUP(plan.md → plan.md.backup)
   IF tasks.md changes:
     BACKUP(tasks.md → tasks.md.backup)

2. APPLY SPEC CHANGES:
   FOR proposal IN approved_proposals WHERE artifact=spec:

     IF proposal.type == "ADD_FR":
       # Append new FR to § Functional Requirements
       spec_content = READ(spec.md)
       fr_section_end = FIND_SECTION_END(spec_content, "## Functional Requirements")
       INSERT_AT(spec.md, fr_section_end, proposal.description)

       # Add annotation to code
       code_file = proposal.actions.code_file
       code_line = proposal.actions.code_line
       annotation = f"// @speckit:FR:{proposal.fr_id}"
       INSERT_LINE_BEFORE(code_file, code_line, annotation)

     ELSE IF proposal.type == "MOVE_TO_OUT_OF_SCOPE":
       # Move FR from § Functional Requirements to § Out of Scope
       MOVE_SECTION(spec.md,
         from="## Functional Requirements",
         to="## Out of Scope",
         content=proposal.fr_id
       )

     ELSE IF proposal.type == "FULL_REGENERATION":
       # Replace entire spec.md
       WRITE(spec.md, proposal.merged_spec)

3. APPLY PLAN CHANGES:
   FOR proposal IN approved_proposals WHERE artifact=plan:

     IF proposal.type == "ADD_PHASE":
       plan_content = READ(plan.md)
       impl_section_end = FIND_SECTION_END(plan_content, "## Implementation Plan")
       INSERT_AT(plan.md, impl_section_end, proposal.content)

     ELSE IF proposal.type == "ADD_DEPENDENCY":
       INSERT_AT(plan.md, "## Dependency Registry", proposal.content)

4. APPLY TASKS CHANGES:
   FOR proposal IN approved_proposals WHERE artifact=tasks:

     IF proposal.type == "ADD_TEST_TASK":
       # Find correct insertion point based on dependencies
       insertion_point = FIND_INSERTION_POINT(tasks.md, proposal.dependency)
       INSERT_AT(tasks.md, insertion_point, proposal.content)

     ELSE IF proposal.type == "ADD_IMPL_TASK":
       insertion_point = FIND_INSERTION_POINT(tasks.md, proposal.dependency)
       INSERT_AT(tasks.md, insertion_point, proposal.content)

5. VALIDATE CHANGES:
   # Check FR IDs unique
   spec_frs = EXTRACT_FRS(spec.md)
   IF len(spec_frs) != len(set(spec_frs)):
     ERROR: "Duplicate FR IDs detected"
     ROLLBACK_FROM_BACKUP()
     ABORT

   # Check AS IDs follow convention
   spec_ass = EXTRACT_ASS(spec.md)
   FOR as IN spec_ass:
     IF NOT VALIDATE_AS_ID(as.id):
       ERROR: "Invalid AS ID: {as.id}"
       ROLLBACK_FROM_BACKUP()
       ABORT

**Output Format**:
```yaml
application_summary:
  spec_changes: 5
  plan_changes: 2
  tasks_changes: 7
  code_annotations_added: 5
  errors: 0

modified_files:
  - spec.md
  - plan.md
  - tasks.md
  - src/api/users.ts
  - src/api/auth.ts
```
```

---

### Subagent 2: registry-updater

**Task**: Update `.artifact-registry.yaml`

**Prompt**:
```
Update artifact registry after applying changes.

**Input**:
- Modified files (from artifact-updater)
- Drift items (original from Wave 1)
- Remaining drift (after fixes)

**Algorithm**:

1. RECALCULATE CHECKSUMS:
   IF spec.md modified:
     spec_checksum = CALCULATE_SHA256(READ(spec.md), normalize=true)
     registry.spec.checksum = spec_checksum

   IF plan.md modified:
     plan_checksum = CALCULATE_SHA256(READ(plan.md), normalize=true)
     registry.plan.checksum = plan_checksum

   IF tasks.md modified:
     tasks_checksum = CALCULATE_SHA256(READ(tasks.md), normalize=true)
     registry.tasks.checksum = tasks_checksum

2. INCREMENT VERSIONS:
   # Determine version bump type
   FOR file IN modified_files:
     IF file == "spec.md":
       IF structural_changes:
         # Major: New sections added
         registry.spec.version = BUMP_MAJOR(registry.spec.version)
       ELSE IF new_frs_added:
         # Minor: New FRs added
         registry.spec.version = BUMP_MINOR(registry.spec.version)
       ELSE:
         # Patch: Existing FRs modified
         registry.spec.version = BUMP_PATCH(registry.spec.version)

3. UPDATE DRIFT METRICS:
   registry.drift_metrics.forward_drift.unimplemented_frs = REMAINING_FORWARD_DRIFT_COUNT
   registry.drift_metrics.reverse_drift.undocumented_apis = REMAINING_REVERSE_DRIFT_COUNT
   registry.drift_metrics.behavioral_drift_count = REMAINING_BEHAVIORAL_DRIFT_COUNT

4. UPDATE COVERAGE STATS:
   total_frs = COUNT(EXTRACT_FRS(spec.md))
   annotated_frs = COUNT(code_annotations WHERE type=FR)
   registry.coverage_stats.fr_to_code_percentage = (annotated_frs / total_frs) * 100

   total_apis = COUNT(EXTRACT_PUBLIC_APIS(codebase))
   documented_apis = COUNT(spec_frs WHERE has_api_reference)
   registry.coverage_stats.code_to_spec_percentage = (documented_apis / total_apis) * 100

5. WRITE REGISTRY:
   WRITE(.artifact-registry.yaml, registry)

**Output Format**:
```yaml
registry_updated:
  spec_version: 1.2.0 → 1.3.0
  plan_version: 1.1.0 → 1.2.0
  tasks_version: 1.0.0 → 1.1.0

  drift_metrics:
    forward_drift: 3 → 0
    reverse_drift: 5 → 0
    behavioral_drift: 2 → 2

  coverage_stats:
    fr_to_code_percentage: 75% → 95%
    code_to_spec_percentage: 60% → 85%
```
```

---

### Subagent 3: system-spec-updater

**Task**: Update system specs (if merged feature affected)

**Prompt**:
```
Update system specs if feature already merged.

**Conditional**: ONLY run if feature has `.merged` marker file

**Input**:
- Approved proposals (spec changes)
- New FRs added
- Current feature ID

**Algorithm**:

1. CHECK IF MERGED:
   IF NOT EXISTS(.merged):
     OUTPUT: "Feature not merged yet - skipping system spec update"
     RETURN

2. READ MERGE METADATA:
   merge_metadata = READ(.merged)
   system_specs_affected = merge_metadata.system_specs_updated

3. FOR each system_spec IN system_specs_affected:

   # Read current system spec
   system_spec_content = READ(system_spec)

   # Append to § Spec History
   new_version = BUMP_VERSION(system_spec.current_version, relationship=EXTENDS)
   new_history_row = f"""
   | {new_version} | {FEATURE_ID} | EXTENDS | {TODAY} | @user | {SUMMARIZE_CHANGES(new_frs)} |
   """
   APPEND_TO_SECTION(system_spec, "## Spec History", new_history_row)

   # Update § Current Behavior
   FOR new_fr IN new_frs:
     behavior_entry = GENERATE_BEHAVIOR_ENTRY(new_fr)
     APPEND_TO_SECTION(system_spec, "## Current Behavior", behavior_entry)

   # Update § API Contract (if new endpoints)
   IF new_fr.has_api:
     api_entry = GENERATE_API_ENTRY(new_fr.api)
     APPEND_TO_SECTION(system_spec, "## API Contract", api_entry)

4. WRITE UPDATED SYSTEM SPECS:
   FOR system_spec IN updated_system_specs:
     WRITE(system_spec, updated_content)

**Output Format**:
```yaml
system_spec_updates:
  total_updated: 2

  updated_specs:
    - path: system/auth/login.md
      old_version: 1.1
      new_version: 1.2
      changes: "Added account archival flow"

    - path: system/user/profile.md
      old_version: 1.0
      new_version: 1.1
      changes: "Added archival status field"
```
```

---

**Wave 5 Output**:
- Modified files (spec.md, plan.md, tasks.md, code)
- Updated registry (.artifact-registry.yaml)
- Updated system specs (if applicable)

**Proceed to Wave 6 (Validation)**

---

## WAVE 6: VALIDATION (Parallel — 3 Agents)

**Goal**: Validate that fixes resolved drift and maintained integrity

Launch **3 parallel subagents** for final validation:

### Subagent 1: drift-validator

**Task**: Re-run drift detection to verify reduction

**Prompt**:
```
Validate that drift was reduced after applying fixes.

**Input**:
- Original drift count (from Wave 1)
- Modified files (from Wave 5)

**Algorithm**:

1. RE-RUN DRIFT DETECTION:
   # Use same algorithm from Wave 1, Subagent 2
   new_drift_items = DETECT_FORWARD_DRIFT() + DETECT_REVERSE_DRIFT() + DETECT_BEHAVIORAL_DRIFT()

2. COMPARE:
   drift_reduction = original_drift_count - len(new_drift_items)

   IF drift_reduction <= 0:
     VALIDATION_FAILED: "Drift not reduced"
     OUTPUT: "❌ Drift count: {original_drift_count} → {len(new_drift_items)}"
     RETURN FAILURE

   ELSE:
     OUTPUT: "✅ Drift reduced: {original_drift_count} → {len(new_drift_items)} ({drift_reduction} items fixed)"
     RETURN SUCCESS

**Output Format**:
```yaml
drift_validation:
  status: SUCCESS | FAILURE
  original_drift: 10
  remaining_drift: 2
  drift_reduced: 8
  reduction_percentage: 80%

  remaining_items:
    - type: behavioral_drift
      description: "Spec says 401, code returns 403"
```
```

---

### Subagent 2: traceability-validator

**Task**: Validate FR/AS IDs are correct

**Prompt**:
```
Validate traceability IDs after updates.

**Input**:
- Updated spec.md
- Updated tasks.md
- Code annotations

**Algorithm**:

1. VALIDATE FR IDs:
   spec_frs = EXTRACT_FRS(spec.md)

   # Check unique
   IF len(spec_frs) != len(set(spec_frs)):
     VALIDATION_FAILED: "Duplicate FR IDs detected"
     duplicates = FIND_DUPLICATES(spec_frs)
     OUTPUT: "❌ Duplicate FRs: {duplicates}"
     RETURN FAILURE

   # Check sequential (warn only, not blocking)
   gaps = FIND_GAPS(spec_frs)
   IF gaps:
     OUTPUT: "⚠️  FR ID gaps detected: {gaps} (non-blocking)"

2. VALIDATE AS IDs:
   spec_ass = EXTRACT_ASS(spec.md)

   FOR as IN spec_ass:
     # Check convention: AS-{FR_NUM}{LETTER}
     IF NOT MATCHES_CONVENTION(as.id):
       VALIDATION_FAILED: "Invalid AS ID: {as.id}"
       OUTPUT: "❌ AS ID doesn't follow convention: {as.id}"
       RETURN FAILURE

3. VALIDATE ANNOTATIONS:
   code_annotations = PARSE_ANNOTATIONS(codebase)

   FOR annotation IN code_annotations WHERE type=FR:
     IF annotation.id NOT IN spec_frs:
       VALIDATION_FAILED: "Orphan annotation: {annotation.id}"
       OUTPUT: "❌ Annotation references non-existent FR: {annotation.id} at {annotation.file}:{annotation.line}"
       RETURN FAILURE

4. IF all validations pass:
   OUTPUT: "✅ Traceability validation passed"
   RETURN SUCCESS

**Output Format**:
```yaml
traceability_validation:
  status: SUCCESS | FAILURE
  fr_ids_unique: true
  fr_ids_sequential: false (gaps: [FR-005, FR-007])
  as_ids_valid: true
  annotations_valid: true
  orphan_annotations: 0
```
```

---

### Subagent 3: cross-reference-validator

**Task**: Validate cross-references between artifacts

**Prompt**:
```
Validate cross-references between spec, plan, tasks.

**Input**:
- Updated spec.md
- Updated plan.md
- Updated tasks.md

**Algorithm**:

1. VALIDATE TASKS → SPEC REFERENCES:
   tasks_content = READ(tasks.md)
   task_fr_refs = EXTRACT_MARKERS(tasks_content, pattern=r"\[FR:(FR-\d+)\]")
   spec_frs = EXTRACT_FRS(spec.md)

   FOR fr_ref IN task_fr_refs:
     IF fr_ref NOT IN spec_frs:
       VALIDATION_FAILED: "Task references non-existent FR: {fr_ref}"
       RETURN FAILURE

2. VALIDATE TASKS → AS REFERENCES:
   task_as_refs = EXTRACT_MARKERS(tasks_content, pattern=r"\[TEST:(AS-\d+[A-Z])\]")
   spec_ass = EXTRACT_ASS(spec.md)

   FOR as_ref IN task_as_refs:
     IF as_ref NOT IN spec_ass:
       VALIDATION_FAILED: "Task references non-existent AS: {as_ref}"
       RETURN FAILURE

3. VALIDATE TASK DEPENDENCIES:
   task_deps = EXTRACT_MARKERS(tasks_content, pattern=r"\[DEP:(T\d+(?:,T\d+)*)\]")
   all_task_ids = EXTRACT_ALL_TASK_IDS(tasks_content)

   FOR dep IN task_deps:
     FOR task_id IN SPLIT(dep, ","):
       IF task_id NOT IN all_task_ids:
         VALIDATION_FAILED: "Task dependency references non-existent task: {task_id}"
         RETURN FAILURE

4. IF all validations pass:
   OUTPUT: "✅ Cross-reference validation passed"
   RETURN SUCCESS

**Output Format**:
```yaml
cross_reference_validation:
  status: SUCCESS | FAILURE
  tasks_to_spec_valid: true
  tasks_to_as_valid: true
  task_dependencies_valid: true
  invalid_references: []
```
```

---

**Wave 6 Output**:
- Drift validation report (SUCCESS/FAILURE)
- Traceability validation report (SUCCESS/FAILURE)
- Cross-reference validation report (SUCCESS/FAILURE)

---

## Post-Execution: Rollback or Success

### If ANY Validation Failed (Wave 6)

```text
IF drift_validation.status == FAILURE OR
   traceability_validation.status == FAILURE OR
   cross_reference_validation.status == FAILURE:

   OUTPUT: "❌ Validation failed after applying changes"
   OUTPUT: "Rolling back..."

   # Restore from backups
   IF EXISTS(spec.md.backup):
     RESTORE(spec.md.backup → spec.md)
     OUTPUT: "✅ Restored spec.md from backup"

   IF EXISTS(plan.md.backup):
     RESTORE(plan.md.backup → plan.md)
     OUTPUT: "✅ Restored plan.md from backup"

   IF EXISTS(tasks.md.backup):
     RESTORE(tasks.md.backup → tasks.md)
     OUTPUT: "✅ Restored tasks.md from backup"

   # Save session state for debugging
   session_state = {
     original_drift: Wave1.drift_items,
     proposals: Wave3.all_proposals,
     approved: Wave4.approved_proposals,
     validation_errors: Wave6.all_errors
   }
   WRITE(.fix-session.yaml, session_state)

   OUTPUT: "✅ Rolled back to original state"
   OUTPUT: "Session state saved to .fix-session.yaml"
   OUTPUT: "Manual resolution required"

   ABORT
```

### If ALL Validations Passed

```text
OUTPUT: ""
OUTPUT: "## ✅ Fix Completed Successfully"
OUTPUT: ""
OUTPUT: "### Summary"
OUTPUT: "- Drift reduced: {original_drift} → {remaining_drift} ({drift_reduction} items fixed)"
OUTPUT: "- Spec changes: {spec_changes_count}"
OUTPUT: "- Plan changes: {plan_changes_count}"
OUTPUT: "- Tasks changes: {tasks_changes_count}"
OUTPUT: "- Annotations added: {annotations_added_count}"
OUTPUT: ""
OUTPUT: "### Modified Files"
FOR file IN modified_files:
  OUTPUT: "- {file}"
OUTPUT: ""
OUTPUT: "### Registry Updates"
OUTPUT: "- Spec version: {old_spec_version} → {new_spec_version}"
OUTPUT: "- FR-to-code coverage: {old_fr_coverage}% → {new_fr_coverage}%"
OUTPUT: "- Code-to-spec coverage: {old_code_coverage}% → {new_code_coverage}%"
OUTPUT: ""
OUTPUT: "### Next Steps"
IF remaining_drift > 0:
  OUTPUT: "- {remaining_drift} drift items remain (behavioral drift requires manual review)"
  OUTPUT: "- Run /speckit.analyze --profile drift for details"
ELSE:
  OUTPUT: "- ✅ All drift resolved"
  OUTPUT: "- Run /speckit.implement to continue with newly added FRs"
OUTPUT: ""

# Cleanup backups if validation passed
DELETE(spec.md.backup)
DELETE(plan.md.backup)
DELETE(tasks.md.backup)
```

---

## Post-Execution Quality Gates

After successful completion, enforce these gates before handoffs:

### QG-FIX-101: Drift Reduction
- **Check**: `remaining_drift < original_drift`
- **Block If**: Drift not reduced
- **Message**: "Fix did not reduce drift - review proposals"
- **Severity**: HIGH

### QG-FIX-102: Traceability Valid
- **Check**: All FR IDs unique AND AS IDs follow convention
- **Block If**: Duplicate or invalid IDs
- **Message**: "ID collision or invalid format detected"
- **Severity**: CRITICAL

### QG-FIX-103: Registry Updated
- **Check**: `.artifact-registry.yaml` checksums match files
- **Block If**: Checksum mismatch
- **Message**: "Registry update failed - artifact integrity at risk"
- **Severity**: CRITICAL

### QG-FIX-104: Validation Passed
- **Check**: All 3 validators returned SUCCESS
- **Block If**: Any validator returned FAILURE
- **Message**: "Post-fix validation failed - already rolled back"
- **Severity**: CRITICAL

If any CRITICAL gate fails → Block handoffs
If any HIGH gate fails → Warn but allow handoffs

---

## Special Cases & Edge Cases

### Edge Case 1: ID Collision

**Scenario**: User manually added FR-009, then `/speckit.fix` tries to add FR-009

**Detection**:
```text
new_fr_id = ALLOCATE_NEW_FR_ID(spec)
IF new_fr_id IN existing_frs:
  # Collision detected
  next_available = FIND_NEXT_AVAILABLE_ID(existing_frs, start=new_fr_id)
  WARNING: "ID {new_fr_id} already exists, using {next_available}"
  new_fr_id = next_available
```

---

### Edge Case 2: Orphan Annotations

**Scenario**: Code has `@speckit:FR:FR-999` but FR-999 doesn't exist in spec

**Resolution** (in Wave 3, spec-proposer):
```text
FOR conflict IN conflicts WHERE type="orphan_annotation":

  IF --mode auto:
    # Auto-fix: Remove orphan annotation
    proposals.append({
      type: "REMOVE_ANNOTATION",
      file: conflict.file,
      line: conflict.line,
      annotation: conflict.annotation
    })

  ELSE:
    # Interactive: Ask user
    proposals.append({
      type: "ORPHAN_ANNOTATION_RESOLUTION",
      severity: "MEDIUM",
      file: conflict.file,
      annotation: conflict.annotation,
      options: [
        {label: "Add FR-999 to spec", action: "ADD_PLACEHOLDER_FR"},
        {label: "Remove annotation", action: "REMOVE_ANNOTATION"}
      ]
    })
```

---

### Edge Case 3: Concurrent Modification

**Scenario**: User edits spec.md while `/speckit.fix` is running

**Detection** (before Wave 5):
```text
BEFORE_WAVE_1:
  original_spec_checksum = CALCULATE_CHECKSUM(spec.md)
  original_plan_checksum = CALCULATE_CHECKSUM(plan.md)
  original_tasks_checksum = CALCULATE_CHECKSUM(tasks.md)

BEFORE_WAVE_5:
  current_spec_checksum = CALCULATE_CHECKSUM(spec.md)
  current_plan_checksum = CALCULATE_CHECKSUM(plan.md)
  current_tasks_checksum = CALCULATE_CHECKSUM(tasks.md)

  IF current_spec_checksum != original_spec_checksum:
    ERROR: "spec.md modified during fix session - aborting"
    OUTPUT: "Save session state to .fix-session.yaml for recovery"
    SAVE_SESSION_STATE(.fix-session.yaml)
    ABORT

  IF current_plan_checksum != original_plan_checksum:
    ERROR: "plan.md modified during fix session - aborting"
    ABORT

  IF current_tasks_checksum != original_tasks_checksum:
    ERROR: "tasks.md modified during fix session - aborting"
    ABORT
```

---

### Edge Case 4: Behavioral Drift (Code ≠ Spec)

**Scenario**: Spec says "return 401", code returns 403

**Policy**: **Code is truth** (update spec to match code)

**Resolution** (in Wave 3, spec-proposer):
```text
FOR drift_item IN drift_items WHERE type="behavioral_drift":

  # Generate proposal to update spec
  proposals.append({
    type: "UPDATE_FR_DESCRIPTION",
    fr_id: drift_item.fr_id,
    severity: "MEDIUM",
    old_description: drift_item.spec_expectation,
    new_description: drift_item.code_behavior,
    rationale: "Code behavior differs from spec - updating spec to match reality",
    diff: GENERATE_DIFF(old, new)
  })

  IF --mode interactive:
    # Allow user to override policy
    OUTPUT: "⚠️  Behavioral Drift Detected"
    OUTPUT: "- FR-{drift_item.fr_id}: {drift_item.description}"
    OUTPUT: "- Spec expects: {drift_item.spec_expectation}"
    OUTPUT: "- Code implements: {drift_item.code_behavior}"
    OUTPUT: "- Location: {drift_item.location}"
    OUTPUT: ""
    OUTPUT: "Policy: Code is truth (will update spec)"
    OUTPUT: "Override? [spec/code/skip]"
    OUTPUT: "  spec = Update spec to match code (recommended)"
    OUTPUT: "  code = Manual code change required (you fix code)"
    OUTPUT: "  skip = Skip this drift item"

    READ user_response

    IF user_response == "code":
      OUTPUT: "Manual code change required: Update {drift_item.location}"
      SKIP(proposal)
```

---

## Output Files

### If `--mode preview`

Generate `fix-preview.md`:
```markdown
# Fix Preview Report

**Generated**: {TIMESTAMP}
**Scope**: {SCOPE}
**Strategy**: {STRATEGY}
**Drift Items**: {DRIFT_COUNT}

## Summary

- Total proposals: {TOTAL}
- Spec proposals: {SPEC_COUNT}
- Plan proposals: {PLAN_COUNT}
- Tasks proposals: {TASKS_COUNT}

## Proposals

### PROP-SPEC-001: Add FR-009 - Account Archival

**Type**: ADD_FR
**Severity**: HIGH
**Confidence**: 0.82

**Proposed Change**:
<FR-009 content>

**Diff**:
```diff
<diff content>
```

---

(Repeat for all proposals)
```

---

### If `--mode interactive` or `--mode auto`

Generate `.fix-summary.md`:
```markdown
# Fix Summary

**Executed**: {TIMESTAMP}
**Mode**: {MODE}
**Strategy**: {STRATEGY}
**Status**: SUCCESS | FAILURE

## Drift Reduction

- Original drift: {ORIGINAL_DRIFT}
- Remaining drift: {REMAINING_DRIFT}
- Items fixed: {DRIFT_REDUCTION}

## Changes Applied

### spec.md
- FRs added: {FR_COUNT}
- FRs moved to Out of Scope: {MOVED_COUNT}

### plan.md
- Phases added: {PHASE_COUNT}
- Dependencies added: {DEP_COUNT}

### tasks.md
- Test tasks added: {TEST_TASK_COUNT}
- Implementation tasks added: {IMPL_TASK_COUNT}

## Modified Files

- spec.md (version {OLD_VER} → {NEW_VER})
- plan.md (version {OLD_VER} → {NEW_VER})
- tasks.md (version {OLD_VER} → {NEW_VER})
- src/api/users.ts (annotation added)

## Coverage Metrics

- FR-to-code coverage: {OLD_FR_COV}% → {NEW_FR_COV}%
- Code-to-spec coverage: {OLD_CODE_COV}% → {NEW_CODE_COV}%

## Next Steps

{NEXT_STEPS}
```

---

## Integration with Existing Commands

### From `/speckit.analyze`

**Handoff**: After drift detection, suggest `/speckit.fix`

```yaml
handoffs:
  - label: Fix Drift
    agent: speckit.fix
    prompt: Synchronize specifications with code
    auto: false
    condition:
      - "Drift items detected (forward, reverse, or behavioral)"
      - "User wants to resolve drift"
```

---

### From `/speckit.reverse-engineer`

**Handoff**: After extraction, apply with regenerate strategy

```yaml
handoffs:
  - label: Apply Extracted Spec
    agent: speckit.fix
    prompt: Apply extracted spec with regenerate strategy
    auto: false
    condition:
      - "Extraction completed successfully"
      - "User wants to merge extracted spec into canonical spec"
```

---

### To `/speckit.implement`

**Handoff**: After successful fix, continue implementation

```yaml
handoffs:
  - label: Continue Implementation
    agent: speckit.implement
    prompt: Implement newly added FRs
    auto: false
    condition:
      - "Fix completed successfully"
      - "New FRs added to spec.md"
      - "User wants to implement new requirements"
```

---

## Session State Recovery

If command aborts due to concurrent modification or other errors, save session state:

**.fix-session.yaml**:
```yaml
session_id: fix-2026-01-11-14-30-42
started_at: 2026-01-11T14:30:42Z
aborted_at: 2026-01-11T14:35:18Z
abort_reason: "Concurrent modification detected in spec.md"

context:
  mode: interactive
  strategy: incremental
  scope: "src/**/*.ts"
  git_diff: true

original_drift:
  forward: 3
  reverse: 5
  behavioral: 2
  total: 10

proposals_generated:
  spec: 8
  plan: 2
  tasks: 7
  total: 17

approved_proposals:
  - PROP-SPEC-001
  - PROP-SPEC-002
  - PROP-TASKS-001

rejected_proposals:
  - PROP-SPEC-005

validation_errors:
  - "spec.md checksum mismatch: expected abc123, got def456"

recovery_instructions: |
  1. Review .fix-session.yaml
  2. Commit or stash changes to spec.md
  3. Re-run /speckit.fix with same flags
  4. System will detect session file and offer to resume
```

---

## Final Output Example

### Success Case

```text
## ✅ Fix Completed Successfully

### Summary
- Drift reduced: 10 → 2 (8 items fixed)
- Spec changes: 5 FRs added, 3 FRs moved to Out of Scope
- Plan changes: 2 phases added
- Tasks changes: 7 tasks added (4 tests, 3 implementation)
- Annotations added: 5

### Modified Files
- spec.md (version 1.2.0 → 1.3.0)
- plan.md (version 1.1.0 → 1.2.0)
- tasks.md (version 1.0.0 → 1.1.0)
- src/api/users.ts
- src/api/auth.ts

### Registry Updates
- Spec version: 1.2.0 → 1.3.0
- FR-to-code coverage: 75% → 95%
- Code-to-spec coverage: 60% → 85%

### Next Steps
- 2 drift items remain (behavioral drift requires manual review)
- Run /speckit.analyze --profile drift for details
- Run /speckit.implement to continue with newly added FRs

Fix summary saved to .fix-summary.md
```

---

### Failure Case (Validation Failed)

```text
❌ Validation failed after applying changes
Rolling back...

✅ Restored spec.md from backup
✅ Restored plan.md from backup
✅ Restored tasks.md from backup

✅ Rolled back to original state
Session state saved to .fix-session.yaml
Manual resolution required

Validation errors:
- Cross-reference validation: Task T045 references non-existent FR-012
- Traceability validation: Duplicate FR ID: FR-009

Please resolve these issues manually and re-run /speckit.fix
```

---

## Command Completion

After Wave 6 completes successfully:

1. Output success summary
2. Save `.fix-summary.md`
3. Cleanup backups
4. Trigger handoffs (if applicable)
5. Exit with status code 0

If any validation fails:
1. Output failure message
2. Rollback from backups
3. Save `.fix-session.yaml`
4. Exit with status code 1

---

**End of /speckit.fix command template**

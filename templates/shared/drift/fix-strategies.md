# Fix Strategies — Update Algorithms for Spec-Code Synchronization

## Purpose

This document defines algorithms for updating artifacts (spec.md, plan.md, tasks.md, system specs) after detecting spec-code drift. Two primary strategies are supported:

1. **Incremental Strategy** (default) — Add missing requirements, preserve structure
2. **Regenerate Strategy** — Full extraction and merge, higher accuracy

---

## Strategy Comparison

| Aspect | Incremental | Regenerate |
|--------|-------------|------------|
| **Speed** | Fast (2-3 min) | Slow (5-10 min) |
| **Risk** | Low | Medium |
| **Preserves Structure** | Yes | Partial |
| **Fixes Behavioral Drift** | No | Yes |
| **User Edits** | Preserved | May be overwritten |
| **Accuracy** | Good | Excellent |
| **Use Case** | Quick fixes, minor drift | Major refactor, stale specs |

---

## Incremental Strategy (Default)

### Philosophy

**"Add missing, preserve existing, never rewrite unnecessarily"**

- Append new FRs/AS to existing sections
- Preserve manual edits
- Maintain existing ID sequences
- Fast and safe

---

### Algorithm 1: Incremental spec.md Updates

```text
INCREMENTAL_UPDATE_SPEC(spec, drift_items, gap_analysis):

  # Step 1: Read current spec
  spec_content = READ(spec.md)
  existing_frs = EXTRACT_FRS(spec_content)
  existing_ass = EXTRACT_ASS(spec_content)

  # Step 2: Allocate new FR IDs
  max_fr_id = MAX(fr.id_number for fr in existing_frs)  # FR-008 → 8
  next_fr_id_number = max_fr_id + 1  # 9

  # Step 3: Process reverse drift (undocumented APIs → new FRs)
  new_frs = []

  FOR drift_item IN drift_items WHERE type="reverse_drift" AND subtype="undocumented_api":

    # Allocate FR ID
    new_fr_id = f"FR-{next_fr_id_number:03d}"  # FR-009
    next_fr_id_number += 1

    # Synthesize FR description using LLM
    fr_description = SYNTHESIZE_FR(
      api_signature=drift_item.signature,
      location=drift_item.location,
      context=READ_FILE_CONTEXT(drift_item.location, lines=20),
      docstring=EXTRACT_DOCSTRING(drift_item.location),
      confidence=drift_item.confidence
    )

    # Create FR entry
    new_fr_entry = f"""
### {new_fr_id}: {fr_description.title}

{fr_description.description}

**API**: {drift_item.signature}
**Location**: {drift_item.location}
**Traceability**: [IMPL:{drift_item.location}]

"""

    new_frs.append({
      id: new_fr_id,
      content: new_fr_entry,
      annotation_target: drift_item.location
    })

  # Step 4: Insert new FRs into spec.md
  fr_section_end = FIND_SECTION_END(spec_content, "## Functional Requirements")

  FOR new_fr IN new_frs:
    INSERT_AT(spec.md, fr_section_end, new_fr.content)

  # Step 5: Add annotations to code
  FOR new_fr IN new_frs:
    code_file = new_fr.annotation_target.file
    code_line = new_fr.annotation_target.line
    annotation = f"// @speckit:FR:{new_fr.id}"
    INSERT_LINE_BEFORE(code_file, code_line, annotation)

  # Step 6: Process forward drift (unimplemented FRs → move to Out of Scope)
  FOR drift_item IN drift_items WHERE type="forward_drift" AND subtype="unimplemented_requirement":

    # Prompt user (if interactive mode)
    IF --mode interactive:
      OUTPUT: "FR-{drift_item.requirement} not implemented. Move to Out of Scope? [y/N]"
      READ user_response

      IF user_response == "y":
        MOVE_FR_TO_OUT_OF_SCOPE(spec.md, drift_item.requirement)

  # Step 7: Update artifact registry
  UPDATE_REGISTRY(spec.md, version=BUMP_MINOR, checksum=CALCULATE_SHA256(spec.md))

  RETURN new_frs
```

---

### Algorithm 2: Incremental plan.md Updates

```text
INCREMENTAL_UPDATE_PLAN(plan, new_frs):

  # Step 1: Read current plan
  plan_content = READ(plan.md)

  # Step 2: For each new FR, add implementation phase
  FOR new_fr IN new_frs:

    # Generate phase content
    phase_content = GENERATE_PHASE(
      fr_id=new_fr.id,
      fr_title=new_fr.title,
      fr_description=new_fr.description,
      api_signature=new_fr.api_signature
    )

    # Example phase content:
    # ## Phase X: Account Archival (FR-009)
    #
    # **Goal**: Implement account archival functionality
    #
    # **Tasks**:
    # - Add archival endpoint
    # - Update user schema
    # - Add tests for archival flow
    #
    # **Dependencies**:
    # - User service (Phase 2)
    # - Database migrations (Phase 1)

    # Insert phase into Implementation Plan
    impl_section_end = FIND_SECTION_END(plan_content, "## Implementation Plan")
    INSERT_AT(plan.md, impl_section_end, phase_content)

  # Step 3: Add dependencies to Dependency Registry (if applicable)
  FOR new_fr IN new_frs:

    IF new_fr.requires_packages:
      # Extract package dependencies from code
      packages = EXTRACT_PACKAGE_DEPENDENCIES(new_fr.location)

      FOR package IN packages:
        IF package NOT IN plan.dependency_registry:
          # Allocate PKG ID
          next_pkg_id = ALLOCATE_PKG_ID(plan)

          # Add to registry
          pkg_entry = f"""
#### PKG-{next_pkg_id}: {package.name}

- **Version**: {package.version} (locked)
- **Docs**: {package.docs_url}
- **Purpose**: {package.purpose}
- **Key APIs**: {package.key_apis}
"""
          INSERT_AT(plan.md, "## Dependency Registry § Package Dependencies", pkg_entry)

  # Step 4: Update artifact registry
  UPDATE_REGISTRY(plan.md, version=BUMP_MINOR, checksum=CALCULATE_SHA256(plan.md))
```

---

### Algorithm 3: Incremental tasks.md Updates

```text
INCREMENTAL_UPDATE_TASKS(tasks, new_frs, new_ass):

  # Step 1: Read current tasks
  tasks_content = READ(tasks.md)
  existing_tasks = EXTRACT_ALL_TASKS(tasks_content)
  dependency_graph = BUILD_DEPENDENCY_GRAPH(existing_tasks)

  # Step 2: Allocate new task IDs
  max_task_id = MAX(task.id_number for task in existing_tasks)  # T045 → 45
  next_task_id_number = max_task_id + 1  # 46

  # Step 3: Add test tasks for new AS (TDD — tests first)
  test_tasks = []

  FOR new_as IN new_ass:
    test_task_id = f"T{next_task_id_number:03d}"  # T046
    next_task_id_number += 1

    # Determine dependencies (tests depend on test setup)
    test_setup_tasks = FIND_TASKS(existing_tasks, marker="[TEST-SETUP]")
    dependencies = [task.id for task in test_setup_tasks]

    test_task_content = f"""- [ ] [TEST:{new_as.id}] Test {new_as.description} [DEP:{",".join(dependencies)}]"""

    test_tasks.append({
      id: test_task_id,
      content: test_task_content,
      dependencies: dependencies,
      phase: DETERMINE_PHASE(new_as.priority)  # P1a → Phase 3
    })

  # Step 4: Add implementation tasks for new FRs
  impl_tasks = []

  FOR new_fr IN new_frs:
    impl_task_id = f"T{next_task_id_number:03d}"  # T047
    next_task_id_number += 1

    # Implementation depends on its tests (TDD)
    test_task_for_fr = FIND_TASK(test_tasks, fr_id=new_fr.id)
    dependencies = [test_task_for_fr.id] if test_task_for_fr else []

    impl_task_content = f"""- [ ] [FR:{new_fr.id}] Implement {new_fr.title} [DEP:{",".join(dependencies)}]"""

    impl_tasks.append({
      id: impl_task_id,
      content: impl_task_content,
      dependencies: dependencies,
      phase: DETERMINE_PHASE(new_fr.priority)
    })

  # Step 5: Insert tasks at correct phases
  all_new_tasks = test_tasks + impl_tasks

  FOR task IN all_new_tasks:
    # Find correct insertion point within phase
    phase_section = FIND_SECTION(tasks_content, task.phase)
    insertion_point = FIND_INSERTION_POINT(phase_section, task.dependencies)
    INSERT_AT(tasks.md, insertion_point, task.content)

  # Step 6: Update dependency graph diagram
  REGENERATE_DEPENDENCY_GRAPH(tasks.md)

  # Step 7: Update Requirements Traceability Matrix (RTM)
  REGENERATE_RTM(tasks.md)

  # Step 8: Update Acceptance Scenario Coverage table
  REGENERATE_AS_COVERAGE(tasks.md)

  # Step 9: Update artifact registry
  UPDATE_REGISTRY(tasks.md, version=BUMP_MINOR, checksum=CALCULATE_SHA256(tasks.md))
```

---

### Algorithm 4: Incremental system-spec Updates (Append-Only)

```text
INCREMENTAL_UPDATE_SYSTEM_SPEC(system_spec, new_frs, feature_id):

  # Conditional: Only run if feature already merged
  IF NOT EXISTS(.merged):
    RETURN  # Feature not merged, skip system spec update

  # Step 1: Read merge metadata
  merge_metadata = READ(.merged)
  system_specs_affected = merge_metadata.system_specs_updated

  # Step 2: For each affected system spec
  FOR system_spec_path IN system_specs_affected:

    system_spec_content = READ(system_spec_path)
    current_version = EXTRACT_VERSION(system_spec_content)

    # Step 3: Determine version bump (always EXTENDS for incremental)
    new_version = BUMP_MINOR(current_version)  # 1.1 → 1.2

    # Step 4: Append to § Spec History (append-only)
    history_entry = f"""
| {new_version} | {feature_id} | EXTENDS | {TODAY} | @user | {SUMMARIZE_CHANGES(new_frs)} |
"""
    APPEND_TO_SECTION(system_spec_path, "## Spec History", history_entry)

    # Step 5: Update § Current Behavior
    FOR new_fr IN new_frs:
      behavior_entry = f"""
### {new_fr.id}: {new_fr.title}

{new_fr.description}

**Introduced**: Version {new_version} (Feature {feature_id})
"""
      APPEND_TO_SECTION(system_spec_path, "## Current Behavior", behavior_entry)

    # Step 6: Update § API Contract (if new endpoints)
    FOR new_fr IN new_frs WHERE has_api_endpoint:
      api_entry = f"""
#### {new_fr.api_signature}

**Version**: {new_version}+
**Stability**: Stable
**Auth**: {new_fr.auth_requirement}
**Rate Limit**: {new_fr.rate_limit}

**Request**:
{new_fr.api_request_schema}

**Response**:
{new_fr.api_response_schema}
"""
      APPEND_TO_SECTION(system_spec_path, "## API Contract", api_entry)

  # Step 7: Write updated system specs
  FOR system_spec_path IN system_specs_affected:
    WRITE(system_spec_path, updated_content)
```

---

## Regenerate Strategy

### Philosophy

**"Extract from code, merge with canonical, validate comprehensively"**

- Full spec extraction via LLM
- Three-way merge (canonical + extracted → merged)
- Preserve manual edits in canonical spec
- Fix behavioral drift
- Slower but more accurate

---

### Algorithm 5: Regenerate spec.md Updates

```text
REGENERATE_UPDATE_SPEC(spec, scope):

  # Step 1: Run reverse-engineer to extract full spec from code
  extracted_spec = RUN_REVERSE_ENGINEER(
    scope=scope,
    output="reverse-engineered/extracted-spec.md"
  )

  # Step 2: Read canonical spec
  canonical_spec = READ(spec.md)

  # Step 3: Three-way merge
  merged_spec = THREE_WAY_MERGE(
    canonical=canonical_spec,
    extracted=extracted_spec,
    strategy="prefer_canonical_for_existing"
  )

  # Merge strategy:
  # - For FRs that exist in BOTH → Use canonical version (preserve manual edits)
  # - For FRs that exist ONLY in extracted → Add to canonical (new requirements)
  # - For FRs that exist ONLY in canonical → Keep (may be out of scope)
  # - For AS that exist in BOTH → Use canonical version
  # - For AS that exist ONLY in extracted → Add to canonical

  # Step 4: Validate merged spec
  validation_result = VALIDATE_SPEC(merged_spec)

  IF validation_result.status == FAILURE:
    OUTPUT: "❌ Merged spec validation failed"
    OUTPUT: validation_result.errors
    OUTPUT: "Manual review required"
    OUTPUT: "Canonical spec: spec.md"
    OUTPUT: "Extracted spec: reverse-engineered/extracted-spec.md"
    OUTPUT: "Merge attempt saved: reverse-engineered/merged-spec.md.failed"
    WRITE("reverse-engineered/merged-spec.md.failed", merged_spec)
    ABORT

  # Step 5: Backup canonical spec
  BACKUP(spec.md → spec.md.backup)

  # Step 6: Replace spec.md with merged spec
  WRITE(spec.md, merged_spec)

  # Step 7: Update artifact registry
  UPDATE_REGISTRY(spec.md, version=BUMP_MAJOR, checksum=CALCULATE_SHA256(spec.md))

  # Step 8: Add annotations to code for new FRs
  new_frs = FIND_NEW_FRS(canonical_spec, merged_spec)

  FOR new_fr IN new_frs:
    IF new_fr.has_code_location:
      annotation = f"// @speckit:FR:{new_fr.id}"
      INSERT_LINE_BEFORE(new_fr.location.file, new_fr.location.line, annotation)

  RETURN merged_spec
```

---

### Algorithm 6: Three-Way Merge Logic

```text
THREE_WAY_MERGE(canonical, extracted, strategy):

  # Step 1: Extract FRs from both specs
  canonical_frs = EXTRACT_FRS(canonical)
  extracted_frs = EXTRACT_FRS(extracted)

  # Step 2: Build FR mapping (by content similarity, not ID)
  fr_mapping = BUILD_FR_MAPPING(canonical_frs, extracted_frs)

  # Mapping algorithm:
  # - For each extracted FR, find most similar canonical FR using LLM
  # - Similarity threshold: 0.70 (below this = new FR)
  # - Example: extracted FR "User can archive account" → canonical FR-009 (0.95 similarity)

  # Step 3: Merge FRs
  merged_frs = []

  FOR extracted_fr IN extracted_frs:

    IF extracted_fr IN fr_mapping:
      # FR exists in canonical (similar content found)
      canonical_fr = fr_mapping[extracted_fr].canonical_fr
      similarity = fr_mapping[extracted_fr].similarity

      IF strategy == "prefer_canonical_for_existing":
        # Use canonical version (preserves manual edits)
        merged_frs.append(canonical_fr)

      ELSE IF strategy == "prefer_extracted_for_existing":
        # Use extracted version (reflects current code)
        merged_frs.append(extracted_fr)

      ELSE IF strategy == "merge_descriptions":
        # Merge descriptions (canonical + extracted insights)
        merged_fr = {
          id: canonical_fr.id,
          title: canonical_fr.title,
          description: MERGE_DESCRIPTIONS(canonical_fr.description, extracted_fr.description),
          api: extracted_fr.api,  # Always use extracted API (reflects code)
          traceability: canonical_fr.traceability  # Preserve canonical traceability
        }
        merged_frs.append(merged_fr)

    ELSE:
      # FR only in extracted (new requirement from code)
      # Allocate new FR ID
      new_fr_id = ALLOCATE_NEW_FR_ID(merged_frs)
      extracted_fr.id = new_fr_id
      merged_frs.append(extracted_fr)

  # Step 4: Add canonical-only FRs (not in extracted)
  FOR canonical_fr IN canonical_frs:
    IF canonical_fr NOT IN fr_mapping.values():
      # FR only in canonical (may be out of scope or not yet implemented)
      merged_frs.append(canonical_fr)

  # Step 5: Rebuild spec.md with merged FRs
  merged_spec = REBUILD_SPEC(
    template=canonical,  # Preserve structure from canonical
    frs=merged_frs,
    ass=MERGE_ASS(canonical, extracted),  # Same logic for AS
    sections=PRESERVE_SECTIONS(canonical)  # Preserve non-FR sections
  )

  RETURN merged_spec
```

---

## Traceability Preservation

### FR ID Allocation

```text
ALLOCATE_NEW_FR_ID(existing_frs):

  # Extract FR numbers
  fr_numbers = [PARSE_FR_NUMBER(fr.id) for fr in existing_frs]
  # Example: [1, 2, 3, 5, 7, 8] (note gaps at 4 and 6)

  # Find max
  max_fr_number = MAX(fr_numbers)  # 8

  # Increment
  next_fr_number = max_fr_number + 1  # 9

  # Format
  next_fr_id = f"FR-{next_fr_number:03d}"  # FR-009

  RETURN next_fr_id
```

**Constraints**:
- Never reuse deleted IDs
- Sequential allocation (gaps allowed, warn only)
- Unique within spec.md

---

### AS ID Allocation

```text
ALLOCATE_NEW_AS_ID(spec, fr_id):

  # Extract FR number
  fr_number = PARSE_FR_NUMBER(fr_id)  # FR-009 → 9

  # Find all AS for this FR
  related_ass = EXTRACT_ASS(spec) WHERE as.fr_number == fr_number

  IF len(related_ass) == 0:
    # First AS for this FR
    next_as_id = f"AS-{fr_number}A"  # AS-9A

  ELSE:
    # Find last letter
    last_as_id = related_ass[-1].id  # AS-9B
    last_letter = last_as_id[-1]  # "B"

    # Increment letter
    next_letter = INCREMENT_LETTER(last_letter)  # "C"
    next_as_id = f"AS-{fr_number}{next_letter}"  # AS-9C

  RETURN next_as_id
```

**Convention**: `AS-{FR_NUM}{LETTER}`
- Example: FR-009 → AS-9A, AS-9B, AS-9C

---

## Proposal Generation

### Proposal Structure

```yaml
proposal:
  id: PROP-SPEC-001
  type: ADD_FR | UPDATE_FR | MOVE_TO_OUT_OF_SCOPE | REMOVE_FR | FULL_REGENERATION
  artifact: spec | plan | tasks | system
  severity: CRITICAL | HIGH | MEDIUM | LOW
  confidence: 0.0 - 1.0

  # Current state
  current_state:
    description: "API endpoint exists but not documented"
    location: src/api/users.ts:142
    signature: "POST /api/v1/users/:id/archive"

  # Proposed change
  proposed_change:
    action: "Add FR-009 to spec.md"
    fr_id: FR-009
    title: "Account Archival"
    description: |
      User can archive their account, marking it inactive while preserving data.

      **API**: POST /api/v1/users/:id/archive
      **Implements**: User privacy compliance (GDPR Article 17)

  # Diff
  diff: |
    +++ spec.md
    @@ -120,6 +120,12 @@
    +### FR-009: Account Archival
    +User can archive their account, marking it inactive while preserving data.
    +
    +**API**: POST /api/v1/users/:id/archive
    +**Implements**: User privacy compliance (GDPR Article 17)

  # Actions to apply
  actions:
    - "Add FR-009 to spec.md § Functional Requirements"
    - "Add @speckit:FR:FR-009 annotation to src/api/users.ts:142"

  # User response (filled during interactive mode)
  user_response: null  # Y | n | e | skip
```

---

### Confidence Scoring

```text
ESTIMATE_CONFIDENCE(drift_item):

  confidence = 0.0

  # Factor 1: Has @speckit annotation (0.50)
  IF drift_item.has_annotation:
    confidence += 0.50

  # Factor 2: Has test coverage (0.20, or 0.10 if partial)
  IF drift_item.has_tests:
    confidence += 0.20
  ELSE IF drift_item.has_partial_tests:
    confidence += 0.10

  # Factor 3: Naming clarity (LLM evaluated, 0.0-0.15)
  naming_clarity = EVALUATE_NAMING_CLARITY(drift_item.signature)
  confidence += 0.15 * naming_clarity

  # Factor 4: Has docstring (0.10, or 0.05 if inline comments)
  IF drift_item.has_docstring:
    confidence += 0.10
  ELSE IF drift_item.has_inline_comments:
    confidence += 0.05

  # Factor 5: Matches known pattern (0.05)
  IF drift_item.matches_pattern:
    confidence += 0.05

  RETURN MIN(confidence, 1.0)
```

**Interpretation**:
- **0.90 - 1.00**: Very high confidence (explicit annotation + tests + docstring)
- **0.70 - 0.89**: High confidence (tests + good naming)
- **0.50 - 0.69**: Medium confidence (annotation only or tests only)
- **0.30 - 0.49**: Low confidence (inferred from code structure)
- **0.00 - 0.29**: Very low confidence (likely hallucination)

---

## Helper Functions

### FIND_SECTION_END

```text
FIND_SECTION_END(content, section_name):

  # Find section start
  section_start_line = FIND_LINE(content, pattern=f"^{section_name}$")

  # Find next section (start with ##)
  next_section_line = FIND_LINE(content, pattern="^## ", start=section_start_line + 1)

  # Section end is line before next section
  section_end_line = next_section_line - 1

  RETURN section_end_line
```

---

### INSERT_AT

```text
INSERT_AT(file_path, line_number, content):

  file_content = READ(file_path)
  lines = SPLIT(file_content, "\n")

  # Insert content at line_number
  lines.insert(line_number, content)

  # Write back
  WRITE(file_path, JOIN(lines, "\n"))
```

---

### MOVE_SECTION

```text
MOVE_SECTION(file_path, from_section, to_section, content_id):

  file_content = READ(file_path)

  # Extract content from source section
  content = EXTRACT_CONTENT(file_content, from_section, content_id)

  # Remove from source section
  file_content = REMOVE_CONTENT(file_content, from_section, content_id)

  # Insert into target section
  to_section_end = FIND_SECTION_END(file_content, to_section)
  file_content = INSERT_AT_LINE(file_content, to_section_end, content)

  # Write back
  WRITE(file_path, file_content)
```

---

### FIND_INSERTION_POINT

```text
FIND_INSERTION_POINT(tasks_content, task_dependencies):

  # Algorithm: Find the last task that this task depends on
  dependency_tasks = FIND_TASKS(tasks_content, ids=task_dependencies)

  IF len(dependency_tasks) == 0:
    # No dependencies, insert at beginning of phase
    RETURN FIND_PHASE_START(tasks_content)

  ELSE:
    # Find max line number of dependency tasks
    max_line = MAX(task.line_number for task in dependency_tasks)

    # Insert after max line
    RETURN max_line + 1
```

---

## Behavioral Drift Handling

### Policy

**Code is truth** — When spec and code behavior diverge, update spec to match code.

### Algorithm

```text
HANDLE_BEHAVIORAL_DRIFT(drift_item, mode):

  # Example: Spec says "return 401", code returns 403

  IF mode == "auto":
    # Auto-fix: Update spec to match code
    proposal = {
      type: "UPDATE_FR_DESCRIPTION",
      fr_id: drift_item.fr_id,
      old_description: drift_item.spec_expectation,
      new_description: drift_item.code_behavior,
      rationale: "Code behavior differs from spec - updating spec to match reality"
    }
    RETURN proposal

  ELSE IF mode == "interactive":
    # Prompt user
    OUTPUT: "⚠️  Behavioral Drift Detected"
    OUTPUT: "- FR-{drift_item.fr_id}: {drift_item.description}"
    OUTPUT: "- Spec expects: {drift_item.spec_expectation}"
    OUTPUT: "- Code implements: {drift_item.code_behavior}"
    OUTPUT: "- Location: {drift_item.location}"
    OUTPUT: ""
    OUTPUT: "Policy: Code is truth (will update spec)"
    OUTPUT: "Override? [spec/code/skip]"

    READ user_response

    IF user_response == "spec":
      # Update spec
      proposal = {
        type: "UPDATE_FR_DESCRIPTION",
        fr_id: drift_item.fr_id,
        old_description: drift_item.spec_expectation,
        new_description: drift_item.code_behavior
      }
      RETURN proposal

    ELSE IF user_response == "code":
      # User will fix code manually
      OUTPUT: "Manual code change required: Update {drift_item.location}"
      RETURN null

    ELSE:
      # Skip
      RETURN null
```

---

## Validation After Application

### Post-Fix Validation Checklist

```yaml
post_fix_validation:
  - name: "FR IDs Unique"
    check: "len(frs) == len(set(frs))"
    severity: CRITICAL

  - name: "FR IDs Sequential"
    check: "No collisions (gaps allowed)"
    severity: LOW (warn only)

  - name: "AS IDs Follow Convention"
    check: "AS-{FR_NUM}{LETTER}"
    severity: CRITICAL

  - name: "Annotations Valid"
    check: "All @speckit:FR: reference existing FRs"
    severity: HIGH

  - name: "Cross-References Valid"
    check: "All [FR:FR-xxx] in tasks.md reference existing FRs"
    severity: HIGH

  - name: "Checksums Match"
    check: ".artifact-registry.yaml checksums == file checksums"
    severity: CRITICAL

  - name: "Drift Reduced"
    check: "remaining_drift < original_drift"
    severity: HIGH
```

---

## Rollback Procedure

### When to Rollback

- Any CRITICAL validation failed
- Checksum mismatch after changes
- User aborted during interactive mode
- Concurrent modification detected

### Rollback Algorithm

```text
ROLLBACK_FROM_BACKUP():

  OUTPUT: "❌ Rolling back changes..."

  # Restore from backups
  IF EXISTS(spec.md.backup):
    RESTORE(spec.md.backup → spec.md)
    DELETE(spec.md.backup)
    OUTPUT: "✅ Restored spec.md"

  IF EXISTS(plan.md.backup):
    RESTORE(plan.md.backup → plan.md)
    DELETE(plan.md.backup)
    OUTPUT: "✅ Restored plan.md"

  IF EXISTS(tasks.md.backup):
    RESTORE(tasks.md.backup → tasks.md)
    DELETE(tasks.md.backup)
    OUTPUT: "✅ Restored tasks.md"

  # Revert code annotations (if applied)
  IF code_annotations_added:
    FOR annotation IN code_annotations_added:
      REMOVE_LINE(annotation.file, annotation.line)
    OUTPUT: "✅ Reverted code annotations"

  # Save session state for debugging
  session_state = {
    timestamp: NOW(),
    rollback_reason: "Validation failed",
    validation_errors: validation_errors,
    proposals_generated: proposals,
    proposals_approved: approved_proposals
  }
  WRITE(.fix-session.yaml, session_state)

  OUTPUT: "✅ Rollback complete"
  OUTPUT: "Session state saved to .fix-session.yaml"
```

---

## Performance Optimization

### Caching

```text
# Cache extracted spec for 15 minutes (avoid re-running reverse-engineer)
IF --strategy regenerate:
  cache_key = f"extracted-spec-{CHECKSUM(scope)}"
  cached_spec = GET_FROM_CACHE(cache_key)

  IF cached_spec AND cache_age < 900:  # 15 minutes
    extracted_spec = cached_spec
  ELSE:
    extracted_spec = RUN_REVERSE_ENGINEER(scope)
    SET_CACHE(cache_key, extracted_spec, ttl=900)
```

### Parallel Annotation Addition

```text
# Add annotations in parallel to speed up
FOR batch IN BATCH(new_frs, batch_size=10):
  PARALLEL_FOR fr IN batch:
    ADD_ANNOTATION_TO_CODE(fr.location, fr.id)
```

---

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `Duplicate FR ID` | ID collision during allocation | Use FIND_NEXT_AVAILABLE_ID to skip |
| `Invalid AS ID` | AS ID doesn't follow convention | Regenerate with correct format |
| `Orphan annotation` | Code has @speckit:FR:FR-999 but FR-999 doesn't exist | Add FR-999 to spec OR remove annotation |
| `Checksum mismatch` | File modified during fix session | Abort, save session state, prompt user to re-run |
| `Validation failed` | Post-fix validation detected issues | Rollback, save session state, manual review |

---

**End of fix-strategies.md**

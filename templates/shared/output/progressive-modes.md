# Progressive Output Modes

## Purpose

Adapt output verbosity based on complexity tier and user preferences. Provides summary-first pattern with expandable details, reducing cognitive load while preserving full information access.

## Why This Matters

| Fixed Output | Progressive Output |
|--------------|-------------------|
| Same verbosity for all features | Adapts to complexity |
| Wall of text for simple features | Concise summaries when appropriate |
| Missing details for complex features | Full depth when needed |
| No clear next actions | Always shows next step |

## Output Modes

```text
OUTPUT_MODES = {
  COMPACT: {
    description: "Minimal output for TRIVIAL/SIMPLE features",
    sections: "summary + essentials only",
    details: "collapsed by default",
    use_when: "complexity_tier IN [TRIVIAL, SIMPLE]"
  },
  STANDARD: {
    description: "Balanced output with collapsible sections",
    sections: "all sections visible",
    details: "verbose sections collapsed",
    use_when: "complexity_tier == MODERATE OR user_default"
  },
  DETAILED: {
    description: "Full verbose output for complex features",
    sections: "all sections expanded",
    details: "all details visible",
    use_when: "complexity_tier == COMPLEX OR --verbose flag"
  }
}
```

## Mode Selection Algorithm

```text
SELECT_OUTPUT_MODE(complexity_tier, user_flags):

  # User override takes precedence
  IF "--compact" IN user_flags:
    RETURN COMPACT
  IF "--verbose" IN user_flags:
    RETURN DETAILED

  # Complexity-based default
  SWITCH complexity_tier:
    CASE TRIVIAL:
      RETURN COMPACT
    CASE SIMPLE:
      RETURN COMPACT
    CASE MODERATE:
      RETURN STANDARD
    CASE COMPLEX:
      RETURN DETAILED

  # Fallback
  RETURN STANDARD
```

## Summary-First Pattern

All commands MUST output a Quick Summary before detailed content:

```markdown
# {Command} Complete

## Quick Summary

| Aspect | Value |
|--------|-------|
| **Feature** | {name} |
| **Complexity** | {TIER} ({score}/100) |
| **Key Metrics** | {primary_metrics} |
| **Tokens** | {METRICS_STATE.total_tokens_in + METRICS_STATE.total_tokens_out:,} |
| **Cost** | ${METRICS_STATE.total_cost:.4f} |
| **Status** | {status_badge} |
| **Next Step** | `/speckit.{next}` |

{IF mode != COMPACT}
---
{full_artifact_content}
{END}

{IF mode == COMPACT}
<details>
<summary>📄 View Full {Artifact}</summary>

{full_artifact_content}

</details>
{END}
```

## Command-Specific Templates

### specify.md Quick Summary

```markdown
## Quick Summary

| Aspect | Value |
|--------|-------|
| **Feature** | {feature_name} |
| **Complexity** | {TIER} ({score}/100) |
| **User Stories** | {story_count} stories |
| **Requirements** | {fr_count} functional, {nfr_count} non-functional |
| **Scenarios** | {as_count} acceptance scenarios |
| **Tokens** | {total_tokens:,} |
| **Cost** | ${total_cost:.4f} |
| **Status** | ✅ Ready for Planning |
| **Next Step** | `/speckit.plan` |

### Key Requirements

{top_3_requirements_summary}

### Scope Boundaries

- **In**: {in_scope_summary}
- **Out**: {out_scope_summary}
```

### plan.md Quick Summary

```markdown
## Quick Summary

| Aspect | Value |
|--------|-------|
| **Feature** | {feature_name} |
| **Complexity** | {TIER} ({score}/100) |
| **Phases** | {phase_count} implementation phases |
| **Dependencies** | {dep_count} external, {internal_count} internal |
| **Estimated Scope** | {file_count} files to modify |
| **Tokens** | {total_tokens:,} |
| **Cost** | ${total_cost:.4f} |
| **Status** | ✅ Ready for Tasks |
| **Next Step** | `/speckit.tasks` |

### Implementation Phases

{phase_list_with_file_counts}

### Key Dependencies

{top_3_dependencies}
```

### tasks.md Quick Summary

```markdown
## Quick Summary

| Aspect | Value |
|--------|-------|
| **Feature** | {feature_name} |
| **Complexity** | {TIER} ({score}/100) |
| **Total Tasks** | {task_count} tasks |
| **By Story** | {story_task_breakdown} |
| **Parallel Ops** | {parallel_count} can run in parallel |
| **FR Coverage** | {fr_covered}/{fr_total} ({fr_pct}%) |
| **Tokens** | {total_tokens:,} |
| **Cost** | ${total_cost:.4f} |
| **Status** | ✅ Ready for Implementation |
| **Next Step** | `/speckit.implement` |

### Task Distribution

| Story | Tasks | Priority |
|-------|-------|----------|
{story_task_table}

### MVP Scope (Story 1)

{story_1_tasks_summary}
```

## Collapsible Sections

Use HTML details/summary for verbose content in COMPACT/STANDARD modes:

```markdown
<details>
<summary>📋 Full Requirements List ({fr_count} items)</summary>

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | ... | MUST |
| FR-002 | ... | SHOULD |
...

</details>

<details>
<summary>🧪 All Acceptance Scenarios ({as_count} items)</summary>

### AS-1A: {scenario_name}
...

</details>

<details>
<summary>🔧 Technical Details</summary>

### Dependencies
...

### File Changes
...

</details>
```

## Status Badges

```text
STATUS_BADGES = {
  ready_for_next: "✅ Ready for {next_command}",
  warnings: "⚠️ Ready with {count} warnings",
  blocked: "❌ Blocked: {reason}",
  stale: "🔄 Stale: needs refresh"
}

DETERMINE_STATUS(self_review_result, staleness):

  IF staleness.any_stale:
    RETURN STATUS_BADGES.stale.format(...)

  IF self_review_result.verdict == "FAIL":
    RETURN STATUS_BADGES.blocked.format(reason=self_review_result.reason)

  IF self_review_result.verdict == "WARN":
    count = len(self_review_result.warnings)
    RETURN STATUS_BADGES.warnings.format(count=count)

  RETURN STATUS_BADGES.ready_for_next.format(next_command=NEXT_COMMAND)
```

## Next Step Determination

```text
NEXT_COMMAND_MAP = {
  concept: "specify",
  specify: "plan",
  plan: "tasks",
  tasks: "implement"
}

DETERMINE_NEXT_STEP(current_command, self_review_result, staleness):

  # Check for blockers
  IF self_review_result.verdict == "FAIL":
    RETURN "Fix issues above, then re-run /speckit.{current}"

  IF staleness.any_upstream_stale:
    upstream = staleness.stale_upstream[0]
    RETURN "Refresh /speckit.{upstream} first (stale)"

  # Normal flow
  next_cmd = NEXT_COMMAND_MAP[current_command]
  RETURN "/speckit.{next_cmd}"
```

## Progressive Detail Levels

### Level 1: One-Liner (for logs, notifications)

```text
[specify] Feature "user-auth" complete: 3 stories, 8 FRs, 12 ASs → /speckit.plan
```

### Level 2: Quick Summary (default visible)

```markdown
## Quick Summary
| Feature | user-auth (MODERATE) |
| Requirements | 8 FRs, 3 NFRs |
| Status | ✅ Ready |
| Next | /speckit.plan |
```

### Level 3: Full Summary (STANDARD mode)

```markdown
## Quick Summary
{level_2_content}

### Key Requirements
{top_requirements}

### Scope
{scope_summary}

<details><summary>Full Specification</summary>
{complete_spec}
</details>
```

### Level 4: Complete Output (DETAILED mode)

```markdown
## Quick Summary
{level_2_content}

---

{complete_specification_all_sections_expanded}

---

## Self-Review Report
{full_self_review}

## Registry Update
{registry_changes}
```

## Integration

### In Command Templates

Add to end of each command:

```markdown
## Output Phase

Read `templates/shared/output/progressive-modes.md` and apply:

1. Determine output mode:
   - MODE = SELECT_OUTPUT_MODE(COMPLEXITY_TIER, user_flags)

2. Generate Quick Summary:
   - Use command-specific template
   - Include status badge
   - Include next step
   - Include tokens and cost from METRICS_STATE

3. Format full content:
   - IF MODE == COMPACT: wrap in <details>
   - IF MODE == STANDARD: use collapsible sections for verbose parts
   - IF MODE == DETAILED: show all expanded

4. Output in order:
   - Quick Summary (always visible)
   - Full content (formatted per mode)
   - Self-review report (if applicable)
   - **Token Statistics table** (always visible, from orchestration-instructions.md)
```

### Token Statistics Integration

**ALWAYS emit token statistics at command completion:**

```text
IMPORT: templates/shared/orchestration-instructions.md#emit_final_token_summary

AT command_complete:
  emit_final_token_summary()  # Displays per-model breakdown table
```

The token statistics table displays:
- Per-model breakdown (opus, sonnet, haiku)
- Input/output tokens per model
- Cost per model
- Total tokens and total cost
- Duration and cost/minute

### User Overrides

```text
# Force compact output
/speckit.specify --compact "Add login feature"

# Force detailed output
/speckit.plan --verbose

# Set default in constitution.md
| Setting | Value |
|---------|-------|
| Output Mode | STANDARD |
```

## Backward Compatibility

- Default mode is STANDARD (matches current behavior)
- `--legacy` flag outputs raw artifact without summary wrapper
- All content is still generated, just presentation changes

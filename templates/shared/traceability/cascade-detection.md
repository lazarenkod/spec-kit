# Cascade Update Detection

## Purpose

Detect when changes to upstream artifacts require downstream artifacts to be refreshed. Provides intelligent diff analysis to determine impact severity and recommended actions.

## Why This Matters

| Without Cascade Detection | With Cascade Detection |
|---------------------------|------------------------|
| Stale artifacts silently drift | Proactive staleness alerts |
| Manual tracking of dependencies | Automatic dependency graph |
| "Works on my machine" issues | Consistent artifact state |
| Breaking changes go unnoticed | Impact analysis before proceed |

## Artifact Dependency Graph

```text
                    ┌─────────────┐
                    │ concept.md  │
                    │   (root)    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  spec.md    │
                    │ (parent:    │
                    │  concept)   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  plan.md    │
                    │ (parent:    │
                    │  spec)      │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  tasks.md   │
                    │ (parents:   │
                    │  plan,spec) │
                    └─────────────┘
```

## Change Classification

### Impact Levels

```text
IMPACT_LEVELS = {
  BREAKING: {
    severity: "critical",
    requires_refresh: true,
    block_downstream: true,
    description: "Structural changes that invalidate downstream artifacts"
  },
  SIGNIFICANT: {
    severity: "high",
    requires_refresh: true,
    block_downstream: false,
    description: "Content changes that may affect downstream artifacts"
  },
  MINOR: {
    severity: "medium",
    requires_refresh: false,
    block_downstream: false,
    description: "Cosmetic changes, typos, formatting"
  },
  METADATA: {
    severity: "low",
    requires_refresh: false,
    block_downstream: false,
    description: "Comments, timestamps, non-functional changes"
  }
}
```

### Change Detection Rules

```text
DETECT_CHANGE_IMPACT(old_artifact, new_artifact, artifact_type):

  changes = DIFF(old_artifact, new_artifact)

  # Classify each change
  FOR change IN changes:
    change.impact = CLASSIFY_CHANGE(change, artifact_type)

  # Return highest impact
  RETURN max(changes, key=impact.severity)
```

### Classification by Artifact Type

```text
SPEC_CHANGE_CLASSIFICATION:

  BREAKING:
    - FR-xxx removed entirely
    - AS-xxx removed entirely
    - User story removed
    - Non-functional requirement fundamentally changed

  SIGNIFICANT:
    - New FR-xxx added
    - New AS-xxx added
    - FR description significantly changed (>30% diff)
    - Acceptance criteria modified
    - Out of Scope item moved to In Scope

  MINOR:
    - FR description refined (<30% diff)
    - Typos fixed
    - Formatting changes
    - Section reordering (same content)

  METADATA:
    - Comments added/removed
    - Last Updated timestamp changed
    - Version number changed (without content change)
```

```text
PLAN_CHANGE_CLASSIFICATION:

  BREAKING:
    - Implementation phase removed
    - Critical dependency removed
    - Architecture pattern fundamentally changed

  SIGNIFICANT:
    - New phase added
    - New dependency added
    - File path changed significantly
    - Implementation approach changed

  MINOR:
    - Phase description refined
    - Minor dependency version change
    - Code example updated

  METADATA:
    - Comments, timestamps
```

```text
TASKS_CHANGE_CLASSIFICATION:

  BREAKING:
    - Task removed that was in_progress or completed
    - Dependency chain broken

  SIGNIFICANT:
    - New task added
    - Task description significantly changed
    - Priority changed
    - Dependencies modified

  MINOR:
    - Task description refined
    - Story assignment changed
    - File path updated

  METADATA:
    - Status changes (pending → completed)
    - Timestamps
```

## Cascade Propagation Algorithm

```text
PROPAGATE_CASCADE(changed_artifact, impact, registry):

  affected = []

  SWITCH changed_artifact:

    CASE "concept":
      IF impact >= SIGNIFICANT:
        affected.append({
          artifact: "spec",
          reason: "concept.md changed with {impact} impact",
          action: "Review spec.md alignment, consider /speckit.specify --refresh"
        })
        # Cascade continues
        affected.extend(PROPAGATE_CASCADE("spec", SIGNIFICANT, registry))

    CASE "spec":
      IF impact >= SIGNIFICANT:
        affected.append({
          artifact: "plan",
          reason: "spec.md changed with {impact} impact",
          action: "Review plan.md, may need /speckit.plan --refresh"
        })
        affected.append({
          artifact: "tasks",
          reason: "spec.md changed - tasks may have stale FR/AS references",
          action: "Verify task FR coverage, consider /speckit.tasks --refresh"
        })

      IF impact == BREAKING:
        # Mark all downstream as requiring refresh
        FOR artifact IN ["plan", "tasks"]:
          affected.find(artifact).requires_refresh = true
          affected.find(artifact).block_downstream = true

    CASE "plan":
      IF impact >= SIGNIFICANT:
        affected.append({
          artifact: "tasks",
          reason: "plan.md changed with {impact} impact",
          action: "Review tasks.md alignment, may need /speckit.tasks --refresh"
        })

  RETURN affected
```

## On-Change Hook Integration

```text
ON_ARTIFACT_SAVE(artifact_type, artifact_path):

  registry = READ_REGISTRY()

  # Get previous checksum
  old_checksum = registry.artifacts[artifact_type].checksum
  new_checksum = CALCULATE_CHECKSUM(artifact_path)

  IF old_checksum == new_checksum:
    RETURN  # No change

  # Detect impact
  old_content = CACHE.get(artifact_type + "_content")
  new_content = READ(artifact_path)
  impact = DETECT_CHANGE_IMPACT(old_content, new_content, artifact_type)

  # Propagate cascade
  affected = PROPAGATE_CASCADE(artifact_type, impact, registry)

  # Update registry staleness
  FOR affected_artifact IN affected:
    registry.staleness[affected_artifact.artifact + "_stale"] = true
    registry.staleness.reasons.append(affected_artifact)

  # Update registry
  UPDATE_REGISTRY(artifact_type, artifact_path, ...)

  # Report if significant
  IF len(affected) > 0:
    OUTPUT: "## Cascade Update Detected"
    OUTPUT: ""
    OUTPUT: "**Changed**: {artifact_type}.md ({impact} impact)"
    OUTPUT: ""
    OUTPUT: "**Affected Artifacts**:"
    FOR a IN affected:
      OUTPUT: "- **{a.artifact}**: {a.reason}"
      OUTPUT: "  - Action: {a.action}"
```

## Smart Refresh Recommendations

```text
RECOMMEND_REFRESH_STRATEGY(registry):

  stale_artifacts = [a FOR a IN registry.staleness IF a.stale]

  IF len(stale_artifacts) == 0:
    OUTPUT: "All artifacts are current."
    RETURN

  # Determine optimal refresh order
  refresh_order = TOPOLOGICAL_SORT(stale_artifacts, by_dependency)

  OUTPUT: "## Recommended Refresh Sequence"
  OUTPUT: ""

  FOR i, artifact IN enumerate(refresh_order):
    reason = registry.staleness.reasons.find(artifact)
    OUTPUT: "{i+1}. `/speckit.{artifact}` - {reason.reason}"

  OUTPUT: ""
  OUTPUT: "**Tip**: Run in sequence to maintain consistency."

  # Check if batch refresh is possible
  IF all_independent(stale_artifacts):
    OUTPUT: ""
    OUTPUT: "**Alternative**: All stale artifacts are independent."
    OUTPUT: "You can refresh in any order or parallel."
```

## Diff Visualization

```text
GENERATE_CHANGE_SUMMARY(old_artifact, new_artifact, artifact_type):

  changes = DIFF(old_artifact, new_artifact)

  summary = {
    added: [],
    modified: [],
    removed: [],
    impact: NONE
  }

  FOR change IN changes:
    IF change.type == ADD:
      summary.added.append(change.item)
    ELIF change.type == MODIFY:
      summary.modified.append({
        item: change.item,
        before: change.old_value[:50],
        after: change.new_value[:50]
      })
    ELIF change.type == REMOVE:
      summary.removed.append(change.item)

    # Track highest impact
    item_impact = CLASSIFY_CHANGE(change, artifact_type)
    IF item_impact > summary.impact:
      summary.impact = item_impact

  RETURN summary
```

## Change Summary Report

```markdown
## Change Summary: spec.md

**Impact Level**: SIGNIFICANT
**Changed By**: Manual edit / /speckit.specify
**Timestamp**: {ISO_DATE}

### Added
- FR-009: New authentication requirement
- AS-9A: New acceptance scenario

### Modified
- FR-003: Updated description (clarified scope)
- AS-3B: Modified expected behavior

### Removed
- (none)

### Cascade Impact

| Downstream | Status | Action Required |
|------------|--------|-----------------|
| plan.md | ⚠️ Review | New FR-009 may need implementation phase |
| tasks.md | ⚠️ Stale | Missing tasks for FR-009 |

**Recommendation**: Run `/speckit.plan` then `/speckit.tasks` to refresh.
```

## Integration Points

### In /speckit.analyze

```text
# At start of analysis
Read `templates/shared/traceability/cascade-detection.md`
Read `templates/shared/traceability/artifact-registry.md`

registry = READ_REGISTRY()
staleness = CHECK_STALENESS(registry)

IF staleness.reasons.length > 0:
  OUTPUT: "## Staleness Detected"
  RECOMMEND_REFRESH_STRATEGY(registry)
```

### In /speckit.specify (on refresh)

```text
IF --refresh flag:
  old_spec = READ(FEATURE_DIR/spec.md)
  # ... generate new spec ...
  new_spec = generated_content

  impact = DETECT_CHANGE_IMPACT(old_spec, new_spec, "spec")
  affected = PROPAGATE_CASCADE("spec", impact, registry)

  IF len(affected) > 0:
    OUTPUT: GENERATE_CHANGE_SUMMARY(old_spec, new_spec, "spec")
```

## Backward Compatibility

```text
IF NOT exists(FEATURE_DIR/.artifact-registry.yaml):
  # Cascade detection works in degraded mode
  OUTPUT: "Note: Artifact registry not initialized."
  OUTPUT: "Run any /speckit.* command to enable cascade detection."

  # Still provide basic staleness check via file timestamps
  spec_mtime = mtime(FEATURE_DIR/spec.md)
  plan_mtime = mtime(FEATURE_DIR/plan.md)
  tasks_mtime = mtime(FEATURE_DIR/tasks.md)

  IF plan_mtime < spec_mtime:
    OUTPUT: "⚠️ plan.md older than spec.md - may be stale"
  IF tasks_mtime < plan_mtime:
    OUTPUT: "⚠️ tasks.md older than plan.md - may be stale"
```

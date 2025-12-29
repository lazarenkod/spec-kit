# Artifact Version Registry

## Purpose

Track artifact versions and parent relationships to enable bi-directional traceability. Detects when downstream artifacts need refresh due to upstream changes.

## Why This Matters

| Without Registry | With Registry |
|------------------|---------------|
| Manual tracking of artifact relationships | Automatic parent-child tracking |
| Stale artifacts go unnoticed | Proactive staleness detection |
| No version history | Version lineage preserved |
| Inconsistent cross-references | Validated traceability |

## Registry Location

```text
REGISTRY_FILE = FEATURE_DIR/.artifact-registry.yaml
```

## Registry Schema

```yaml
# .artifact-registry.yaml
version: "1.0"
feature_id: "{FEATURE_ID}"
feature_name: "{feature_name}"
created_at: "{ISO_DATE}"
last_updated: "{ISO_DATE}"

artifacts:
  concept:
    exists: true | false
    version: "1.0"
    checksum: "sha256:..."
    updated_at: "{ISO_DATE}"
    updated_by: "/speckit.concept"

  spec:
    exists: true | false
    version: "1.0"
    checksum: "sha256:..."
    updated_at: "{ISO_DATE}"
    updated_by: "/speckit.specify"
    parent_concept_version: "1.0" | null
    fr_count: 8
    as_count: 12

  plan:
    exists: true | false
    version: "1.0"
    checksum: "sha256:..."
    updated_at: "{ISO_DATE}"
    updated_by: "/speckit.plan"
    parent_spec_version: "1.0"
    phase_count: 4

  tasks:
    exists: true | false
    version: "1.0"
    checksum: "sha256:..."
    updated_at: "{ISO_DATE}"
    updated_by: "/speckit.tasks"
    parent_plan_version: "1.0"
    parent_spec_version: "1.0"
    task_count: 25
    fr_coverage:
      covered: 8
      total: 8
      percentage: 100
    as_coverage:
      covered: 10
      total: 12
      percentage: 83

staleness:
  spec_stale: false
  plan_stale: false
  tasks_stale: false
  reasons: []
```

## Checksum Calculation

```text
CALCULATE_CHECKSUM(artifact_path):
  1. Read file content
  2. Normalize whitespace (trim trailing, normalize line endings)
  3. Remove metadata comments (lines starting with <!-- registry: -->)
  4. Calculate SHA-256 hash
  5. Return first 16 characters of hex digest

  RETURN "sha256:{hash_prefix}"
```

## Version Increment Rules

```text
DETERMINE_VERSION_INCREMENT(old_artifact, new_artifact):

  # Major: Breaking changes
  IF structure_changed(old, new):  # sections added/removed
    RETURN increment_major(old.version)

  # Minor: Content additions
  IF content_added(old, new):  # new FRs, new tasks
    RETURN increment_minor(old.version)

  # Patch: Content modifications
  IF content_modified(old, new):  # edits to existing items
    RETURN increment_patch(old.version)

  # No change
  RETURN old.version

VERSION_FORMAT = "MAJOR.MINOR"  # e.g., "1.0", "1.1", "2.0"
```

## Registry Operations

### Initialize Registry

```text
INIT_REGISTRY(feature_dir, feature_id, feature_name):

  registry = {
    version: "1.0",
    feature_id: feature_id,
    feature_name: feature_name,
    created_at: NOW(),
    last_updated: NOW(),
    artifacts: {
      concept: {exists: false},
      spec: {exists: false},
      plan: {exists: false},
      tasks: {exists: false}
    },
    staleness: {
      spec_stale: false,
      plan_stale: false,
      tasks_stale: false,
      reasons: []
    }
  }

  WRITE_YAML(FEATURE_DIR/.artifact-registry.yaml, registry)
  RETURN registry
```

### Update Registry on Artifact Change

```text
UPDATE_REGISTRY(artifact_type, artifact_path, parent_versions):

  registry = READ_YAML(FEATURE_DIR/.artifact-registry.yaml)

  # Calculate new checksum
  new_checksum = CALCULATE_CHECKSUM(artifact_path)

  # Determine version
  IF registry.artifacts[artifact_type].exists:
    old_checksum = registry.artifacts[artifact_type].checksum
    IF new_checksum != old_checksum:
      new_version = DETERMINE_VERSION_INCREMENT(old, new)
    ELSE:
      new_version = registry.artifacts[artifact_type].version
  ELSE:
    new_version = "1.0"

  # Update artifact entry
  registry.artifacts[artifact_type] = {
    exists: true,
    version: new_version,
    checksum: new_checksum,
    updated_at: NOW(),
    updated_by: "/speckit.{artifact_type}",
    ...parent_versions,
    ...extract_metrics(artifact_path)
  }

  # Check for cascade staleness
  CHECK_CASCADE_STALENESS(registry)

  registry.last_updated = NOW()
  WRITE_YAML(FEATURE_DIR/.artifact-registry.yaml, registry)

  RETURN registry
```

### Check Staleness

```text
CHECK_STALENESS(registry):

  staleness = {
    spec_stale: false,
    plan_stale: false,
    tasks_stale: false,
    reasons: []
  }

  # Spec staleness (if concept changed)
  IF registry.artifacts.concept.exists AND registry.artifacts.spec.exists:
    IF registry.artifacts.spec.parent_concept_version != registry.artifacts.concept.version:
      staleness.spec_stale = true
      staleness.reasons.append({
        artifact: "spec",
        reason: "concept.md updated to v{concept.version}, spec built against v{spec.parent_concept_version}",
        action: "Re-run /speckit.specify"
      })

  # Plan staleness (if spec changed)
  IF registry.artifacts.spec.exists AND registry.artifacts.plan.exists:
    IF registry.artifacts.plan.parent_spec_version != registry.artifacts.spec.version:
      staleness.plan_stale = true
      staleness.reasons.append({
        artifact: "plan",
        reason: "spec.md updated to v{spec.version}, plan built against v{plan.parent_spec_version}",
        action: "Re-run /speckit.plan"
      })

  # Tasks staleness (if plan or spec changed)
  IF registry.artifacts.plan.exists AND registry.artifacts.tasks.exists:
    IF registry.artifacts.tasks.parent_plan_version != registry.artifacts.plan.version:
      staleness.tasks_stale = true
      staleness.reasons.append({
        artifact: "tasks",
        reason: "plan.md updated to v{plan.version}, tasks built against v{tasks.parent_plan_version}",
        action: "Re-run /speckit.tasks"
      })

    IF registry.artifacts.tasks.parent_spec_version != registry.artifacts.spec.version:
      staleness.tasks_stale = true
      staleness.reasons.append({
        artifact: "tasks",
        reason: "spec.md updated to v{spec.version}, tasks built against v{tasks.parent_spec_version}",
        action: "Re-run /speckit.tasks"
      })

  registry.staleness = staleness
  RETURN staleness
```

## Integration with Commands

### In specify.md

```text
# After generating spec.md
Read `templates/shared/traceability/artifact-registry.md` and apply:

UPDATE_REGISTRY("spec", "FEATURE_DIR/spec.md", {
  parent_concept_version: registry.artifacts.concept.version OR null
})
```

### In plan.md

```text
# After generating plan.md
Read `templates/shared/traceability/artifact-registry.md` and apply:

UPDATE_REGISTRY("plan", "FEATURE_DIR/plan.md", {
  parent_spec_version: registry.artifacts.spec.version
})
```

### In tasks.md

```text
# After generating tasks.md
Read `templates/shared/traceability/artifact-registry.md` and apply:

UPDATE_REGISTRY("tasks", "FEATURE_DIR/tasks.md", {
  parent_plan_version: registry.artifacts.plan.version,
  parent_spec_version: registry.artifacts.spec.version
})
```

### In analyze.md

```text
# Check for staleness
Read `templates/shared/traceability/artifact-registry.md` and apply:

staleness = CHECK_STALENESS(registry)

IF staleness.reasons.length > 0:
  OUTPUT: "## Staleness Warnings"
  FOR reason IN staleness.reasons:
    OUTPUT: "- **{reason.artifact}**: {reason.reason}"
    OUTPUT: "  Action: {reason.action}"
```

## Staleness Report Format

```markdown
## Artifact Staleness Check

| Artifact | Version | Parent Version | Status |
|----------|---------|----------------|--------|
| concept.md | 1.2 | - | Current |
| spec.md | 1.0 | concept v1.0 | ⚠️ STALE |
| plan.md | 1.0 | spec v1.0 | Current |
| tasks.md | 1.1 | plan v1.0, spec v1.0 | ⚠️ STALE |

### Recommended Actions

1. **spec.md** is stale: concept.md updated (v1.0 → v1.2)
   - Run `/speckit.specify` to refresh

2. **tasks.md** is stale: spec.md parent version mismatch
   - Run `/speckit.tasks` after spec refresh
```

## Registry Lifecycle

```text
┌─────────────────────────────────────────────────────────────┐
│                    REGISTRY LIFECYCLE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  /speckit.specify                                            │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────┐    Creates/Updates    ┌─────────────────┐  │
│  │  spec.md    │ ──────────────────────▶│  .artifact-     │  │
│  │  generated  │                        │  registry.yaml  │  │
│  └─────────────┘                        └────────┬────────┘  │
│                                                  │           │
│  /speckit.plan                                   │           │
│       │                                          │           │
│       ▼                                          ▼           │
│  ┌─────────────┐    Updates with        ┌─────────────────┐  │
│  │  plan.md    │ ──parent_spec_version──▶│  Registry now   │  │
│  │  generated  │                        │  tracks both    │  │
│  └─────────────┘                        └────────┬────────┘  │
│                                                  │           │
│  /speckit.tasks                                  │           │
│       │                                          │           │
│       ▼                                          ▼           │
│  ┌─────────────┐    Updates with        ┌─────────────────┐  │
│  │  tasks.md   │ ──parent versions──────▶│  Full lineage   │  │
│  │  generated  │                        │  tracked        │  │
│  └─────────────┘                        └────────┬────────┘  │
│                                                  │           │
│  spec.md edited manually                         │           │
│       │                                          │           │
│       ▼                                          ▼           │
│  ┌─────────────┐    Checksum change     ┌─────────────────┐  │
│  │  Checksum   │ ──triggers staleness───▶│  plan_stale:    │  │
│  │  differs    │    detection           │  true           │  │
│  └─────────────┘                        │  tasks_stale:   │  │
│                                         │  true           │  │
│                                         └─────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Backward Compatibility

For existing projects without registry:

```text
IF NOT exists(FEATURE_DIR/.artifact-registry.yaml):
  # Initialize registry from existing artifacts
  registry = INIT_REGISTRY(feature_dir, feature_id, feature_name)

  FOR artifact_type IN [concept, spec, plan, tasks]:
    artifact_path = FEATURE_DIR/{artifact_type}.md
    IF exists(artifact_path):
      registry.artifacts[artifact_type] = {
        exists: true,
        version: "1.0",  # Assume v1.0 for existing
        checksum: CALCULATE_CHECKSUM(artifact_path),
        updated_at: file_mtime(artifact_path),
        updated_by: "migration"
      }

  WRITE_YAML(REGISTRY_FILE, registry)
  OUTPUT: "Initialized artifact registry from existing files"
```

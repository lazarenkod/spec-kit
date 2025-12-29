# Workspace Detection

## Purpose

Automatically detect whether a project is part of a multi-repository workspace. Uses confidence-weighted detection for accurate classification and provides workspace context for cross-repository feature references.

## Why This Matters

| Mode | Impact on Specification |
|------|------------------------|
| **Single-Repo** | Local feature references, no cross-repo sections |
| **Workspace** | Include Cross-Repository Dependencies, use `repo-alias:feature-id` format |

## Detection Algorithm

### Step 1: Collect Signals

Evaluate each signal and accumulate confidence score:

```text
WORKSPACE_SCORE = 0
WORKSPACE_SIGNALS = []

# Signal 1: Workspace Marker File (weight: 50 - definitive)
IF exists(.speckit-workspace) in current or parent directories:
  WORKSPACE_SCORE += 50
  WORKSPACE_ROOT = directory containing .speckit-workspace
  WORKSPACE_CONFIG = parse YAML from .speckit-workspace
  WORKSPACE_SIGNALS.append({signal: "workspace_marker", weight: 50, definitive: true})

# Signal 2: Multiple Git Remotes (weight: 20)
git_remotes = run: git remote -v | grep -E "(fetch|push)" | wc -l
IF git_remotes > 2:
  WORKSPACE_SCORE += 20
  WORKSPACE_SIGNALS.append({signal: "multiple_remotes", weight: 20, value: git_remotes})

# Signal 3: Monorepo Structure (weight: 25)
has_packages = exists(packages/) OR exists(apps/) OR exists(services/) OR exists(libs/)
subproject_count = count directories with own package.json/go.mod/Cargo.toml
IF has_packages AND subproject_count >= 2:
  WORKSPACE_SCORE += 25
  WORKSPACE_SIGNALS.append({signal: "monorepo_structure", weight: 25, count: subproject_count})

# Signal 4: Workspace Config Files (weight: 20)
has_workspace_config = exists(pnpm-workspace.yaml) OR
                       exists(lerna.json) OR
                       exists(nx.json) OR
                       exists(rush.json) OR
                       (exists(package.json) AND package.json contains "workspaces")
IF has_workspace_config:
  WORKSPACE_SCORE += 20
  WORKSPACE_SIGNALS.append({signal: "workspace_config", weight: 20})

# Signal 5: Cross-Repo References in Existing Specs (weight: 15)
IF exists(specs/) AND any spec contains pattern "repo-alias:feature-id":
  WORKSPACE_SCORE += 15
  WORKSPACE_SIGNALS.append({signal: "cross_repo_refs", weight: 15})

# Signal 6: User Intent Keywords (weight: 10)
workspace_keywords = [
  "workspace", "monorepo", "multi-repo", "cross-repo",
  "multiple services", "microservices", "shared libraries"
]
IF any(keyword in user_input for keyword in workspace_keywords):
  WORKSPACE_SCORE += 10
  WORKSPACE_SIGNALS.append({signal: "intent_keywords", weight: 10})
```

### Step 2: Calculate Confidence

```text
WORKSPACE_CONFIDENCE = WORKSPACE_SCORE / 140  # Max possible score

# Normalize to percentage
CONFIDENCE_PERCENT = round(WORKSPACE_CONFIDENCE * 100)
```

### Step 3: Make Decision

```text
IF WORKSPACE_CONFIDENCE >= 0.5:
  WORKSPACE_MODE = true
  DECISION_REASON = "High confidence ({CONFIDENCE_PERCENT}%): " + top 2 signals

ELIF WORKSPACE_CONFIDENCE >= 0.2:
  # Ambiguous - ask user
  ASK_USER: "This project appears to be part of a workspace (confidence: {CONFIDENCE_PERCENT}%).
             Detected: {signals_list}
             Enable workspace mode? (Adds Cross-Repository Dependencies section)"

  IF user_confirms:
    WORKSPACE_MODE = true
  ELSE:
    WORKSPACE_MODE = false

ELSE:
  WORKSPACE_MODE = false
  DECISION_REASON = "Low confidence ({CONFIDENCE_PERCENT}%): Treating as single-repo"
```

### Step 4: Load Workspace Context

```text
IF WORKSPACE_MODE = true AND exists(WORKSPACE_CONFIG):

  # Extract repository mapping
  CURRENT_REPO_ALIAS = find current directory in workspace repos
  AVAILABLE_REPOS = list all repos from workspace config

  # Load cross-dependencies
  CROSS_DEPENDENCIES = parse cross_dependencies section from config

  # Build context object
  WORKSPACE_CONTEXT = {
    root: WORKSPACE_ROOT,
    current_repo: CURRENT_REPO_ALIAS,
    repos: AVAILABLE_REPOS,
    dependencies: CROSS_DEPENDENCIES
  }

ELSE:
  WORKSPACE_CONTEXT = null
```

### Step 5: Report Detection

```text
IF WORKSPACE_MODE:
  OUTPUT: "Workspace mode enabled (confidence: {CONFIDENCE_PERCENT}%)"
  OUTPUT: "Signals: {signals_summary}"
  OUTPUT: "Current repo: {CURRENT_REPO_ALIAS}"
  OUTPUT: "Available repos: {AVAILABLE_REPOS}"
ELSE:
  OUTPUT: "Single-repo mode (confidence: {100 - CONFIDENCE_PERCENT}%)"
```

## Workspace Config Format

The `.speckit-workspace` file uses YAML format:

```yaml
# .speckit-workspace
name: "my-product"
repos:
  frontend:
    path: ../frontend-app
    type: application
    stack: react
  backend:
    path: ../backend-api
    type: service
    stack: python
  shared:
    path: ../shared-libs
    type: library
    stack: typescript

cross_dependencies:
  - from: frontend
    to: backend
    type: api
    description: "Frontend consumes backend REST API"
  - from: frontend
    to: shared
    type: library
    description: "Frontend uses shared UI components"
```

## Impact on Commands

### When WORKSPACE_MODE = true

**In specify.md**:
- Include "Cross-Repository Dependencies" section
- Use `repo-alias:feature-id` format for all cross-repo references
- Suggest dependencies based on repository roles

**In plan.md**:
- Add workspace coordination section
- Include cross-repo API contracts
- Plan for shared library updates

**In tasks.md**:
- Add cross-repo task dependencies
- Include [CROSS:repo-alias] markers
- Add coordination checkpoints

### When WORKSPACE_MODE = false

**In specify.md**:
- Skip "Cross-Repository Dependencies" section
- All feature references are local (just feature-id)

**In plan.md**:
- Standard single-repo planning
- No cross-repo considerations

**In tasks.md**:
- Standard task structure
- No cross-repo markers

## Override Flags

```text
--workspace       # Force workspace mode
--single-repo     # Force single-repo mode
--detect          # Run detection and report (default)
```

## Usage in Commands

Add to command's early steps:

```markdown
## Step N: Detect Workspace Mode

Read `templates/shared/core/workspace-detection.md` and apply.

IF WORKSPACE_MODE = true:
  Set INCLUDE_CROSS_REPO = true
  Load WORKSPACE_CONTEXT
ELSE:
  Set INCLUDE_CROSS_REPO = false
```

## Confidence Thresholds Summary

| Score Range | Confidence | Decision |
|-------------|------------|----------|
| 0-27 | 0-19% | Single-repo (auto) |
| 28-69 | 20-49% | Ask user |
| 70-140 | 50-100% | Workspace (auto) |

## Caching Hint

Detection results can be cached for the session:
- Key: working directory + .speckit-workspace checksum (if exists)
- Value: `{mode: WORKSPACE_MODE, confidence: CONFIDENCE_PERCENT, context: WORKSPACE_CONTEXT}`
- TTL: Until workspace config changes

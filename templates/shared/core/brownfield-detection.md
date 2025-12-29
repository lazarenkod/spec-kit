# Brownfield Detection

## Purpose

Automatically detect whether a project is "brownfield" (modifying existing code) or "greenfield" (new codebase). Uses confidence-weighted multi-signal detection for accurate classification.

## Why This Matters

| Mode | Impact on Specification |
|------|------------------------|
| **Greenfield** | Focus on new requirements, skip change analysis |
| **Brownfield** | Include Change Specification, baseline analysis, regression considerations |

## Detection Algorithm

### Step 1: Collect Signals

Evaluate each signal and accumulate confidence score:

```text
BROWNFIELD_SCORE = 0
BROWNFIELD_SIGNALS = []

# Signal 1: Git History (weight: 30)
git_commits = run: git log --oneline | wc -l
IF git_commits > 50:
  BROWNFIELD_SCORE += 30
  BROWNFIELD_SIGNALS.append({signal: "git_history", weight: 30, value: git_commits})

# Signal 2: Codebase Structure (weight: 25)
has_src = exists(src/) OR exists(backend/) OR exists(frontend/) OR exists(app/)
file_count = count files matching *.py, *.ts, *.js, *.go, *.rs, *.java
IF has_src AND file_count > 20:
  BROWNFIELD_SCORE += 25
  BROWNFIELD_SIGNALS.append({signal: "codebase_exists", weight: 25, files: file_count})

# Signal 3: Baseline Exists (weight: 35 - definitive)
IF exists(FEATURE_DIR/baseline.md):
  BROWNFIELD_SCORE += 35
  BROWNFIELD_SIGNALS.append({signal: "baseline_exists", weight: 35, definitive: true})

# Signal 4: Package Manager Config (weight: 15)
has_deps = exists(package.json) OR exists(requirements.txt) OR exists(go.mod) OR
           exists(Cargo.toml) OR exists(pom.xml) OR exists(build.gradle)
IF has_deps:
  BROWNFIELD_SCORE += 15
  BROWNFIELD_SIGNALS.append({signal: "package_manager", weight: 15})

# Signal 5: User Intent Keywords (weight: 10)
brownfield_keywords = [
  "existing", "modify", "extend", "refactor", "migrate", "upgrade",
  "fix", "improve", "current system", "legacy", "brownfield",
  "already have", "existing code", "our current"
]
IF any(keyword in user_input for keyword in brownfield_keywords):
  BROWNFIELD_SCORE += 10
  BROWNFIELD_SIGNALS.append({signal: "intent_keywords", weight: 10})

# Signal 6: Database/Migration Files (weight: 10)
has_migrations = exists(migrations/) OR exists(db/migrate/) OR exists(alembic/)
IF has_migrations:
  BROWNFIELD_SCORE += 10
  BROWNFIELD_SIGNALS.append({signal: "migrations_exist", weight: 10})
```

### Step 2: Calculate Confidence

```text
BROWNFIELD_CONFIDENCE = BROWNFIELD_SCORE / 125  # Max possible score

# Normalize to percentage
CONFIDENCE_PERCENT = round(BROWNFIELD_CONFIDENCE * 100)
```

### Step 3: Make Decision

```text
IF BROWNFIELD_CONFIDENCE >= 0.6:
  BROWNFIELD_MODE = true
  DECISION_REASON = "High confidence ({CONFIDENCE_PERCENT}%): " + top 2 signals

ELIF BROWNFIELD_CONFIDENCE >= 0.3:
  # Ambiguous - ask user
  ASK_USER: "This project appears partially established (confidence: {CONFIDENCE_PERCENT}%).
             Detected: {signals_list}
             Treat as brownfield project? (Adds Change Specification section)"

  IF user_confirms:
    BROWNFIELD_MODE = true
  ELSE:
    BROWNFIELD_MODE = false

ELSE:
  BROWNFIELD_MODE = false
  DECISION_REASON = "Low confidence ({CONFIDENCE_PERCENT}%): Treating as greenfield"
```

### Step 4: Report Detection

```text
IF BROWNFIELD_MODE:
  OUTPUT: "Brownfield mode enabled (confidence: {CONFIDENCE_PERCENT}%)"
  OUTPUT: "Signals: {signals_summary}"
ELSE:
  OUTPUT: "Greenfield mode (confidence: {100 - CONFIDENCE_PERCENT}%)"
```

## Impact on Commands

### When BROWNFIELD_MODE = true

**In specify.md**:
- Include "Change Specification" section
- If baseline.md exists, auto-populate current state
- Add CB-xxx (Current Behavior) markers
- Include regression considerations

**In plan.md**:
- Add migration strategy section
- Consider backward compatibility
- Plan for rollback scenarios

**In tasks.md**:
- Add [CHG:CHG-001] markers for changes
- Include regression test tasks [REG:PB-001]
- Add [ROLLBACK:MIG-001] tasks if needed

### When BROWNFIELD_MODE = false

**In specify.md**:
- Skip "Change Specification" section entirely
- No CB-xxx markers
- Focus on new feature requirements

**In plan.md**:
- Standard architecture planning
- No migration considerations

**In tasks.md**:
- Standard task structure
- No regression/rollback markers

## Override Flags

```text
--brownfield    # Force brownfield mode
--greenfield    # Force greenfield mode
--detect        # Run detection and report (default)
```

## Usage in Commands

Add to command's early steps:

```markdown
## Step N: Detect Brownfield Mode

Read `templates/shared/core/brownfield-detection.md` and apply.

IF BROWNFIELD_MODE = true:
  Set INCLUDE_CHANGE_SPEC = true
  Load baseline.md if exists
ELSE:
  Set INCLUDE_CHANGE_SPEC = false
```

## Confidence Thresholds Summary

| Score Range | Confidence | Decision |
|-------------|------------|----------|
| 0-37 | 0-29% | Greenfield (auto) |
| 38-74 | 30-59% | Ask user |
| 75-125 | 60-100% | Brownfield (auto) |

## Caching Hint

Detection results can be cached for the session:
- Key: working directory + git HEAD
- Value: `{mode: BROWNFIELD_MODE, confidence: CONFIDENCE_PERCENT, signals: [...]}`
- TTL: Until git state changes

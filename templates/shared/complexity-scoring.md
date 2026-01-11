# Complexity Scoring

## Purpose

Automatically assess feature complexity to adapt workflow behavior. Higher complexity features require more rigorous specification phases, while simpler features can use streamlined workflows.

## Why This Matters

| Complexity Tier | Workflow Impact |
|-----------------|-----------------|
| **TRIVIAL** | Minimal workflow, 3 sections, skip CQS |
| **SIMPLE** | Standard workflow, 5-6 sections |
| **MODERATE** | Enhanced workflow, full sections, CQS >= 60 |
| **COMPLEX** | Full workflow + concept.md required, CQS >= 80 |

## Complexity Tiers

```text
COMPLEXITY_TIERS = {
  TRIVIAL:  0-25   # Quick fix, single component, obvious solution
  SIMPLE:   26-50  # Standard feature, few components, clear requirements
  MODERATE: 51-75  # Multi-component feature, some uncertainty
  COMPLEX:  76-100 # System-wide change, high uncertainty, concept required
}
```

## Scoring Algorithm

### Step 1: Collect Scoring Signals

```text
COMPLEXITY_SCORE = 0
COMPLEXITY_SIGNALS = []

# ─────────────────────────────────────────────────
# Signal Category 1: SCOPE (0-25 points)
# ─────────────────────────────────────────────────

scope_keywords_high = ["system-wide", "platform", "architecture", "infrastructure"]
scope_keywords_medium = ["multiple", "several", "various", "cross-functional"]
scope_keywords_low = ["single", "simple", "quick", "minor"]

IF any(kw in user_input.lower() for kw in scope_keywords_high):
  SCOPE_SCORE = 25
  COMPLEXITY_SIGNALS.append({category: "scope", level: "high", score: 25})
ELIF any(kw in user_input.lower() for kw in scope_keywords_medium):
  SCOPE_SCORE = 15
  COMPLEXITY_SIGNALS.append({category: "scope", level: "medium", score: 15})
ELIF any(kw in user_input.lower() for kw in scope_keywords_low):
  SCOPE_SCORE = 5
  COMPLEXITY_SIGNALS.append({category: "scope", level: "low", score: 5})
ELSE:
  SCOPE_SCORE = 10  # Default
  COMPLEXITY_SIGNALS.append({category: "scope", level: "default", score: 10})

COMPLEXITY_SCORE += SCOPE_SCORE

# ─────────────────────────────────────────────────
# Signal Category 2: STAKEHOLDERS (0-20 points)
# ─────────────────────────────────────────────────

# Count distinct user types/roles mentioned
user_types = extract_user_types(user_input)
# Examples: "admin", "user", "customer", "merchant", "operator"

IF len(user_types) >= 3:
  STAKEHOLDER_SCORE = 20
ELIF len(user_types) == 2:
  STAKEHOLDER_SCORE = 12
ELSE:
  STAKEHOLDER_SCORE = 5

COMPLEXITY_SIGNALS.append({category: "stakeholders", count: len(user_types), score: STAKEHOLDER_SCORE})
COMPLEXITY_SCORE += STAKEHOLDER_SCORE

# ─────────────────────────────────────────────────
# Signal Category 3: TECHNICAL COMPLEXITY (0-25 points)
# ─────────────────────────────────────────────────

tech_complex_high = [
  "real-time", "distributed", "ML", "machine learning", "AI",
  "blockchain", "cryptography", "streaming", "event sourcing",
  "kotlin multiplatform", "kmp", "kmm", "cross-platform"
]
tech_complex_medium = [
  "async", "queue", "cache", "search", "analytics",
  "notification", "scheduled", "batch", "import", "export",
  "flutter", "react native", "react-native", "expo"
]
tech_complex_low = [
  "CRUD", "form", "page", "list", "table", "dashboard"
]

high_matches = count_matches(user_input, tech_complex_high)
medium_matches = count_matches(user_input, tech_complex_medium)
low_matches = count_matches(user_input, tech_complex_low)

TECH_SCORE = min(25, high_matches * 10 + medium_matches * 5 + low_matches * 2)
COMPLEXITY_SIGNALS.append({category: "tech_complexity", high: high_matches, medium: medium_matches, score: TECH_SCORE})
COMPLEXITY_SCORE += TECH_SCORE

# ─────────────────────────────────────────────────
# Signal Category 4: INTEGRATION (0-15 points)
# ─────────────────────────────────────────────────

integration_keywords = [
  "API", "third-party", "webhook", "integration",
  "external", "partner", "OAuth", "SSO", "payment gateway"
]

integration_matches = count_matches(user_input, integration_keywords)

IF integration_matches >= 3:
  INTEGRATION_SCORE = 15
ELIF integration_matches >= 1:
  INTEGRATION_SCORE = 8
ELSE:
  INTEGRATION_SCORE = 0

COMPLEXITY_SIGNALS.append({category: "integration", matches: integration_matches, score: INTEGRATION_SCORE})
COMPLEXITY_SCORE += INTEGRATION_SCORE

# ─────────────────────────────────────────────────
# Signal Category 4.5: CROSS-PLATFORM (0-15 points)
# ─────────────────────────────────────────────────

# Detect cross-platform frameworks that add significant complexity
cross_platform_keywords = {
  "kmp": ["kotlin multiplatform", "kmp", "kmm", "iosMain", "androidMain", "shared module"],
  "flutter": ["flutter", "dart", "pubspec.yaml"],
  "react_native": ["react native", "react-native", "expo"]
}

PLATFORM_DETECTED = null
for platform, keywords in cross_platform_keywords:
  IF any(kw in user_input.lower() for kw in keywords):
    PLATFORM_DETECTED = platform
    break

IF PLATFORM_DETECTED == "kmp":
  PLATFORM_SCORE = 15  # KMP has highest complexity (iOS interop, framework export)
ELIF PLATFORM_DETECTED == "flutter":
  PLATFORM_SCORE = 10  # Flutter moderate complexity
ELIF PLATFORM_DETECTED == "react_native":
  PLATFORM_SCORE = 10  # RN moderate complexity
ELSE:
  PLATFORM_SCORE = 0

IF PLATFORM_SCORE > 0:
  COMPLEXITY_SIGNALS.append({category: "cross_platform", platform: PLATFORM_DETECTED, score: PLATFORM_SCORE})
  COMPLEXITY_SCORE += PLATFORM_SCORE

# ─────────────────────────────────────────────────
# Signal Category 5: CODEBASE CONTEXT (0-15 points)
# ─────────────────────────────────────────────────

# Only applies to brownfield projects
IF BROWNFIELD_MODE = true:
  commit_count = run: git log --oneline | wc -l
  existing_specs = count files in specs/features/

  IF commit_count > 500 OR existing_specs > 20:
    CODEBASE_SCORE = 15
  ELIF commit_count > 200 OR existing_specs > 10:
    CODEBASE_SCORE = 10
  ELIF commit_count > 50 OR existing_specs > 5:
    CODEBASE_SCORE = 5
  ELSE:
    CODEBASE_SCORE = 0

  COMPLEXITY_SIGNALS.append({category: "codebase", commits: commit_count, specs: existing_specs, score: CODEBASE_SCORE})
  COMPLEXITY_SCORE += CODEBASE_SCORE
```

### Step 2: Determine Tier

```text
IF COMPLEXITY_SCORE <= 25:
  COMPLEXITY_TIER = "TRIVIAL"
ELIF COMPLEXITY_SCORE <= 50:
  COMPLEXITY_TIER = "SIMPLE"
ELIF COMPLEXITY_SCORE <= 70:
  COMPLEXITY_TIER = "MODERATE"
ELSE:
  COMPLEXITY_TIER = "COMPLEX"  # 71+ (changed from 76+ for Plan Mode v0.4.0)
```

### Step 3: Report Assessment

```text
OUTPUT: "Complexity Assessment: {COMPLEXITY_TIER} ({COMPLEXITY_SCORE}/100)"
OUTPUT: "Signals:"
FOR signal IN COMPLEXITY_SIGNALS:
  OUTPUT: "  - {signal.category}: {signal.score} pts"
```

## Tier-Specific Workflow Adaptations

### TRIVIAL (0-25)

**specify.md**:
- Include only: Goal, Requirements (FR only), Basic Scenarios
- Skip: User Stories, NFR, Data Contracts, Out of Scope
- Self-review: 3 criteria only (SR-SPEC-01, 02, 03)

**plan.md**:
- Auto-fill tech context from codebase analysis
- Skip: Research phase, Multiple approaches
- Include: Single implementation approach

**tasks.md**:
- Compact task list (max 5 tasks)
- Skip: RTM, Rollback tasks
- Simple T001, T002... format

### SIMPLE (26-50)

**specify.md**:
- Include: Goal, Requirements, User Stories, Scenarios
- Skip: Data Contracts (unless API feature)
- Self-review: 6 criteria

**plan.md**:
- Standard workflow
- Single approach with brief alternatives

**tasks.md**:
- Standard task breakdown
- Include RTM if FR count > 3

### MODERATE (51-75)

**specify.md**:
- Full sections
- Require CQS >= 60 for concept (if exists)
- Self-review: 10 criteria

**plan.md**:
- Full workflow
- Include research.md for unknowns
- Multiple approaches comparison

**tasks.md**:
- Full task breakdown with RTM
- Include regression considerations
- Add [CRITICAL] markers for risky tasks

### COMPLEX (76-100)

**specify.md**:
- Require concept.md to exist first
- Require CQS >= 80
- Full sections + Change Specification
- Self-review: Full 10 criteria + concept alignment

**plan.md**:
- Full workflow with all phases
- Require technical spike for unknowns
- Include rollback plan

**tasks.md**:
- Full breakdown with dependency graph
- Include [CRITICAL], [RISK], [ROLLBACK] markers
- Add milestone checkpoints

## CQS Requirements by Tier

| Tier | CQS Requirement | Concept Required |
|------|-----------------|------------------|
| TRIVIAL | Not applicable | No |
| SIMPLE | Not applicable | No |
| MODERATE | CQS >= 60 (if concept exists) | Recommended |
| COMPLEX | CQS >= 80 | Required |

## Override Flags

```text
--complexity=trivial   # Force TRIVIAL tier
--complexity=simple    # Force SIMPLE tier
--complexity=moderate  # Force MODERATE tier
--complexity=complex   # Force COMPLEX tier
--complexity=auto      # Run detection (default)
```

## Usage in Commands

Add to command's early steps:

```markdown
## Step N: Assess Complexity

Read `templates/shared/complexity-scoring.md` and apply.

Store COMPLEXITY_TIER and COMPLEXITY_SCORE for workflow adaptation.

ADAPT sections based on COMPLEXITY_TIER guidelines.
```

## Scoring Adjustment Hints

The scoring can be refined over time based on actual outcomes:

```text
CALIBRATION_HINTS:
- If simple-looking feature takes > 2 weeks: +15 to similar patterns
- If complex-rated feature finishes in < 1 week: -10 to similar patterns
- Track tier→actual-effort ratio to improve accuracy

FEEDBACK_LOOP:
- After /speckit.merge, prompt: "How accurate was the complexity assessment?"
- Store calibration data in FEATURE_DIR/.complexity-feedback.yaml
```

## Caching Hint

Assessment can be cached for the session:
- Key: user_input hash + BROWNFIELD_MODE + codebase stats
- Value: `{tier: COMPLEXITY_TIER, score: COMPLEXITY_SCORE, signals: [...]}`
- TTL: Until user input changes

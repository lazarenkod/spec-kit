# Plan Mode Triggers

> **Version**: 1.0.0
> **Purpose**: Auto-enable logic, keyword detection, graceful fallbacks

## Overview

Plan Mode can be triggered in 4 ways (priority order):
1. **Explicit flag** — `--depth-level <0-3>`, `--plan-mode`, `--no-plan-mode`
2. **Keyword detection** — Keywords in user input upgrade depth by +1
3. **Complexity-based** — Default depth level based on complexity tier and command
4. **Manual** — User explicitly requests Plan Mode in conversation

---

## Trigger Priority

### Priority 1: Explicit Flags (Highest)

```python
# Priority 1a: --depth-level flag
if "--depth-level" in flags:
    level = parse_int(flags["--depth-level"])
    if not 0 <= level <= 3:
        raise ValueError(f"--depth-level must be 0-3, got {level}")
    return level, f"explicit flag (--depth-level {level})"

# Priority 1b: Backward compat flags
if "--plan-mode" in flags:
    return 3, "explicit flag (--plan-mode → depth 3)"

if "--no-plan-mode" in flags:
    return 0, "explicit flag (--no-plan-mode → depth 0)"
```

**Effect:** Overrides all other triggers

---

### Priority 2: Keyword Detection

```python
KEYWORD_TRIGGERS = [
    # Architecture keywords
    "distributed",
    "microservices",
    "multi-service",
    "event-driven",
    "service-mesh",
    "multi-region",

    # Complexity keywords
    "migration",
    "data-intensive",
    "real-time",
    "streaming",
    "high-throughput",

    # Risk keywords
    "security-critical",
    "compliance",
    "GDPR",
    "HIPAA",
    "financial",

    # Scale keywords
    "high-availability",
    "fault-tolerant",
    "disaster-recovery",
    "geo-distributed",
    "multi-tenant"
]

def detect_keyword_triggers(user_input, default_level):
    """
    Scan user input for keywords that upgrade depth level.

    Returns:
        (upgraded_level, matched_keyword) or (default_level, None)
    """
    normalized_input = user_input.lower()

    for keyword in KEYWORD_TRIGGERS:
        if keyword in normalized_input:
            upgraded_level = min(default_level + 1, 3)  # Cap at level 3
            if upgraded_level > default_level:
                return upgraded_level, keyword

    return default_level, None
```

**Effect:** Upgrades default depth by +1 level (max 3)

**Examples:**

```text
Input: "Build a simple REST API"
→ No keywords, uses default depth for complexity tier

Input: "Build a distributed REST API with microservices"
→ Keywords: "distributed", "microservices"
→ Upgrades from default (e.g., 1 → 2)

Input: "Migrate legacy monolith to event-driven architecture"
→ Keywords: "migration", "event-driven"
→ Upgrades from default (e.g., 2 → 3)
```

---

### Priority 3: Complexity-Based Defaults

```python
COMMAND_DEPTH_DEFAULTS = {
    "speckit.plan": {
        "TRIVIAL": 0,   # 0-25
        "SIMPLE": 0,    # 26-50
        "MODERATE": 1,  # 51-70
        "COMPLEX": 2    # 71+
    },
    "speckit.specify": {
        "TRIVIAL": 0,
        "SIMPLE": 0,
        "MODERATE": 1,
        "COMPLEX": 2
    },
    "speckit.tasks": {
        "TRIVIAL": 0,
        "SIMPLE": 0,
        "MODERATE": 0,  # Stay at standard
        "COMPLEX": 1    # Lite only
    },
    "speckit.concept": {
        "TRIVIAL": 0,
        "SIMPLE": 1,    # Exploration even for simple
        "MODERATE": 2,
        "COMPLEX": 3    # Full depth
    },
    "speckit.implement": {
        "TRIVIAL": 0,
        "SIMPLE": 0,
        "MODERATE": 0,  # Minimize overhead
        "COMPLEX": 1
    }
}

def get_default_depth(command, complexity_tier):
    """
    Get default depth level for command and complexity tier.
    """
    if command not in COMMAND_DEPTH_DEFAULTS:
        # Unknown command, use conservative defaults
        return {"TRIVIAL": 0, "SIMPLE": 0, "MODERATE": 0, "COMPLEX": 1}[complexity_tier]

    return COMMAND_DEPTH_DEFAULTS[command][complexity_tier]
```

**Rationale:**
- **/speckit.concept**: Aggressive depth (even L1 for SIMPLE) because concept benefits from exploration
- **/speckit.tasks**: Conservative depth (L0 for MODERATE) because tasks is fast
- **/speckit.plan, /speckit.specify**: Balanced depth (L1 for MODERATE, L2 for COMPLEX)
- **/speckit.implement**: Minimal depth (L1 max) because implement is long

---

### Priority 4: Manual Request

If user explicitly says "use Plan Mode" or "run exploration" in conversation, treat as `--plan-mode` flag.

**Detection:**

```python
def detect_manual_request(user_message):
    """
    Check if user manually requested Plan Mode in conversation.
    """
    patterns = [
        r"use plan mode",
        r"enable plan mode",
        r"run exploration",
        r"do research first",
        r"analyze alternatives",
        r"depth level [123]"
    ]

    normalized = user_message.lower()
    for pattern in patterns:
        if re.search(pattern, normalized):
            return True

    return False
```

---

## Complexity Threshold Changes

### Old Thresholds (v0.3.x)

```python
IF score <= 25:     tier = "TRIVIAL"
ELIF score <= 50:   tier = "SIMPLE"
ELIF score <= 75:   tier = "MODERATE"  # 51-75
ELSE:               tier = "COMPLEX"   # 76+
```

### New Thresholds (v0.4.0)

```python
IF score <= 25:     tier = "TRIVIAL"
ELIF score <= 50:   tier = "SIMPLE"
ELIF score <= 70:   tier = "MODERATE"  # 51-70 (changed from 75)
ELSE:               tier = "COMPLEX"   # 71+ (changed from 76)
```

**Rationale:** Plan Mode auto-enables at complexity ≥ 71 per user requirement. Lowering threshold from 76 to 71 means more features trigger Plan Mode.

**Impact:**
- Features with scores 71-75: Previously MODERATE (no Plan Mode), now COMPLEX (auto Plan Mode at depth 2)
- ~5% more features will auto-enable Plan Mode

---

## Graceful Fallbacks

### Exploration Phase Failure

```python
def handle_exploration_failure(error, feature_dir):
    """
    If exploration phase fails, fall back to standard mode.
    """
    LOG f"⚠️ Exploration phase failed: {error}"
    LOG "Falling back to Standard mode (depth 0)"

    # Remove partial research.md if it exists
    research_path = f"{feature_dir}/research.md"
    if os.path.exists(research_path):
        os.remove(research_path)
        LOG f"Removed partial {research_path}"

    # Return None → standard mode will be used
    return None
```

**Triggers:**
- Agent timeout (45s or 60s exceeded)
- Agent error (tool failure, API error)
- research.md write failure

**Effect:** Workflow continues without Plan Mode enhancements

---

### Review Phase Failure (Non-Critical)

```python
def handle_review_failure_noncritical(pass_name, error):
    """
    Log warning for non-critical review failures, continue workflow.
    """
    LOG f"⚠️ Review pass '{pass_name}' failed: {error}"
    LOG "Continuing (non-critical pass)"

    # Continue to next pass or finalize
```

**Triggers:**
- completeness_check failure (HIGH severity)
- edge_case_detection failure (HIGH severity)
- testability_audit failure (MEDIUM severity)

**Effect:** Workflow continues, but user is warned

---

### Review Phase Failure (Critical)

```python
def handle_review_failure_critical(pass_name, violations):
    """
    Block workflow on constitution violations.
    """
    LOG f"❌ Review pass '{pass_name}' FAILED (CRITICAL)"
    LOG "Violations found:"

    for v in violations:
        LOG f"  - {v.severity}: {v.description}"
        LOG f"    Location: {v.location}"
        LOG f"    Fix: {v.remediation}"

    raise QualityGateViolation(
        gate_id="PM-004",
        message=f"Constitution violations detected",
        violations=violations
    )
```

**Triggers:**
- constitution_alignment FAIL with CRITICAL violations

**Effect:** Workflow stops, user must fix violations

---

## Edge Cases

### Case 1: Missing spec.md (Complexity Calculation)

**Problem:** Complexity tier calculation requires spec.md, but it doesn't exist yet (e.g., first run of /speckit.specify)

**Solution:**

```python
def calculate_complexity_tier_safe(spec_path):
    """
    Calculate complexity tier, default to MODERATE if spec doesn't exist.
    """
    if not os.path.exists(spec_path):
        LOG "spec.md not found, defaulting to MODERATE complexity"
        return "MODERATE"

    # Normal calculation
    return calculate_complexity_tier(spec_path)
```

**Effect:** First run of /speckit.specify uses MODERATE defaults (depth 1 for plan/specify)

---

### Case 2: Conflicting Flags

**Problem:** User provides both `--plan-mode` and `--no-plan-mode`

**Solution:**

```python
if "--plan-mode" in flags and "--no-plan-mode" in flags:
    raise ValueError("Conflicting flags: --plan-mode and --no-plan-mode cannot both be set")
```

**Effect:** Error raised, user must choose one

---

### Case 3: Keyword Triggers on TRIVIAL Features

**Problem:** User says "Build a distributed system" but it's actually TRIVIAL (score 15)

**Solution:**

```python
# Keyword upgrade: TRIVIAL (default 0) → +1 → Lite (1)
# Still only uses Lite mode (2 agents, 90s), not Moderate/Full
upgraded_level = min(default_level + 1, 3)
```

**Effect:** Keywords upgrade by +1 only, capped at 3. TRIVIAL with keyword → depth 1 (reasonable).

---

### Case 4: Multiple Keywords Match

**Problem:** User input has 3 keywords: "distributed", "microservices", "real-time"

**Solution:**

```python
# Only upgrade once, even if multiple keywords match
for keyword in KEYWORD_TRIGGERS:
    if keyword in normalized_input:
        upgraded_level = min(default_level + 1, 3)
        return upgraded_level, keyword  # Return on first match
```

**Effect:** Upgrade by +1 total (not +3), return first matched keyword for logging

---

## Testing Triggers

### Test Matrix

| Scenario | Complexity | Flags | Keywords | Expected Depth | Reason |
|----------|------------|-------|----------|----------------|--------|
| T1 | TRIVIAL (20) | None | None | 0 | Default for TRIVIAL |
| T2 | SIMPLE (40) | None | None | 0 | Default for SIMPLE |
| T3 | MODERATE (65) | None | None | 1 | Default for plan/specify |
| T4 | COMPLEX (80) | None | None | 2 | Default for plan/specify |
| T5 | MODERATE (65) | `--plan-mode` | None | 3 | Flag overrides default |
| T6 | COMPLEX (80) | `--no-plan-mode` | None | 0 | Flag overrides default |
| T7 | MODERATE (65) | None | "distributed" | 2 | Keyword upgrade 1→2 |
| T8 | TRIVIAL (20) | None | "microservices" | 1 | Keyword upgrade 0→1 |
| T9 | COMPLEX (80) | None | "real-time" | 3 | Keyword upgrade 2→3 |
| T10 | COMPLEX (80) | `--depth-level 1` | "distributed" | 1 | Flag overrides keyword |

### Validation Commands

```bash
# T7: Keyword upgrade on MODERATE
/speckit.plan
# Input: "Design API for distributed system"
# Expected: "🔍 Depth Level 2 (Moderate): ENABLED (keyword 'distributed' upgraded from 1)"

# T10: Flag overrides keyword
/speckit.specify --depth-level 1
# Input: "Implement microservices architecture"
# Expected: "🔍 Depth Level 1 (Lite): ENABLED (explicit flag --depth-level 1)"
```

---

## References

- Framework: `templates/shared/plan-mode/framework.md`
- Complexity Scoring: `templates/shared/complexity-scoring.md`
- Command Configs: `templates/commands/*.md` (plan_mode section)

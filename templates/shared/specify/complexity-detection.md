# Specification Complexity Detection

## Purpose

Automatically detect specification complexity to enable adaptive model selection for `/speckit.specify`, optimizing cost while preserving quality for complex features.

## Why This Matters

| Complexity | Model | Cost Impact | Quality Impact |
|------------|-------|-------------|----------------|
| **SIMPLE** | Sonnet | 80% savings vs Opus | Maintained for CRUD/standard features |
| **MODERATE** | Sonnet | 80% savings vs Opus | Maintained for multi-component features |
| **COMPLEX** | Opus | Baseline cost | Required for system-wide/strategic features |

## Complexity Tiers

```text
SPEC_COMPLEXITY_TIERS = {
  SIMPLE:   0-40   # CRUD, single entity, standard patterns
  MODERATE: 41-70  # Multiple entities, standard integrations
  COMPLEX:  71-100 # System-wide, novel architecture, strategic
}
```

## Detection Algorithm

### Step 1: Analyze Feature Description Signals

```text
COMPLEXITY_SCORE = 0
SIGNALS = []

# ─────────────────────────────────────────────────
# Signal 1: ENTITY COUNT (0-20 points)
# ─────────────────────────────────────────────────

entity_keywords = ["user", "order", "product", "payment", "customer",
                   "merchant", "account", "profile", "session", "document",
                   "invoice", "transaction", "report", "notification"]

entity_count = count_unique_entities(user_input, entity_keywords)

IF entity_count >= 5:
  ENTITY_SCORE = 20
ELIF entity_count >= 3:
  ENTITY_SCORE = 12
ELIF entity_count >= 2:
  ENTITY_SCORE = 6
ELSE:
  ENTITY_SCORE = 0

SIGNALS.append({category: "entity_count", value: entity_count, score: ENTITY_SCORE})
COMPLEXITY_SCORE += ENTITY_SCORE

# ─────────────────────────────────────────────────
# Signal 2: INTEGRATION COUNT (0-20 points)
# ─────────────────────────────────────────────────

integration_keywords = [
  "API", "third-party", "webhook", "integration", "external",
  "OAuth", "SSO", "payment gateway", "Stripe", "PayPal",
  "email service", "SMS", "notification service", "analytics"
]

integration_count = count_matches(user_input, integration_keywords)

IF integration_count >= 3:
  INTEGRATION_SCORE = 20
ELIF integration_count >= 2:
  INTEGRATION_SCORE = 12
ELIF integration_count == 1:
  INTEGRATION_SCORE = 6
ELSE:
  INTEGRATION_SCORE = 0

SIGNALS.append({category: "integration_count", value: integration_count, score: INTEGRATION_SCORE})
COMPLEXITY_SCORE += INTEGRATION_SCORE

# ─────────────────────────────────────────────────
# Signal 3: TECHNICAL COMPLEXITY (0-25 points)
# ─────────────────────────────────────────────────

tech_complex_high = [
  "real-time", "distributed", "ML", "machine learning", "AI",
  "event sourcing", "CQRS", "microservice", "streaming",
  "blockchain", "cryptography", "consensus"
]

tech_complex_medium = [
  "async", "queue", "cache", "search", "full-text",
  "scheduled", "batch", "worker", "background job",
  "rate limiting", "throttling"
]

tech_complex_low = [
  "CRUD", "form", "list", "table", "dashboard",
  "filter", "sort", "pagination"
]

high_count = count_matches(user_input, tech_complex_high)
medium_count = count_matches(user_input, tech_complex_medium)
low_count = count_matches(user_input, tech_complex_low)

TECH_SCORE = min(25, high_count * 15 + medium_count * 8 + low_count * 2)

SIGNALS.append({category: "tech_complexity", high: high_count, medium: medium_count, low: low_count, score: TECH_SCORE})
COMPLEXITY_SCORE += TECH_SCORE

# ─────────────────────────────────────────────────
# Signal 4: ARCHITECTURAL SCOPE (0-20 points)
# ─────────────────────────────────────────────────

scope_keywords_high = [
  "system-wide", "platform", "architecture", "infrastructure",
  "migration", "refactor entire", "replace", "deprecate"
]

scope_keywords_medium = [
  "multiple pages", "cross-module", "shared component",
  "reusable", "library", "framework"
]

scope_keywords_low = [
  "single page", "single component", "one feature",
  "quick fix", "minor change"
]

high_scope = any(kw in user_input.lower() for kw in scope_keywords_high)
medium_scope = any(kw in user_input.lower() for kw in scope_keywords_medium)
low_scope = any(kw in user_input.lower() for kw in scope_keywords_low)

IF high_scope:
  SCOPE_SCORE = 20
ELIF medium_scope:
  SCOPE_SCORE = 10
ELIF low_scope:
  SCOPE_SCORE = 2
ELSE:
  SCOPE_SCORE = 8  # Default medium-low

SIGNALS.append({category: "scope", level: high_scope ? "high" : medium_scope ? "medium" : "low", score: SCOPE_SCORE})
COMPLEXITY_SCORE += SCOPE_SCORE

# ─────────────────────────────────────────────────
# Signal 5: WORD COUNT (0-15 points)
# ─────────────────────────────────────────────────

word_count = len(user_input.split())

IF word_count > 150:
  WORD_SCORE = 15  # Long descriptions often indicate complexity
ELIF word_count > 80:
  WORD_SCORE = 10
ELIF word_count > 40:
  WORD_SCORE = 5
ELSE:
  WORD_SCORE = 0

SIGNALS.append({category: "word_count", value: word_count, score: WORD_SCORE})
COMPLEXITY_SCORE += WORD_SCORE
```

### Step 2: Determine Tier

```text
IF COMPLEXITY_SCORE <= 40:
  TIER = "SIMPLE"
  RECOMMENDED_MODEL = "sonnet"
ELIF COMPLEXITY_SCORE <= 70:
  TIER = "MODERATE"
  RECOMMENDED_MODEL = "sonnet"
ELSE:
  TIER = "COMPLEX"
  RECOMMENDED_MODEL = "opus"
```

### Step 3: Display Assessment

```text
OUTPUT:
┌─────────────────────────────────────────┐
│ Specification Complexity Assessment     │
├─────────────────────────────────────────┤
│ Tier:  {TIER}                          │
│ Score: {COMPLEXITY_SCORE}/100           │
│ Model: {RECOMMENDED_MODEL}              │
└─────────────────────────────────────────┘

Signals:
  • Entity count:       {entity_count} entities → {ENTITY_SCORE} pts
  • Integration count:  {integration_count} integrations → {INTEGRATION_SCORE} pts
  • Tech complexity:    {high_count} high, {medium_count} medium → {TECH_SCORE} pts
  • Architectural scope: {scope_level} → {SCOPE_SCORE} pts
  • Description length: {word_count} words → {WORD_SCORE} pts

Cost estimate vs. always-Opus:
  • Opus cost:      $0.50 (baseline)
  • {MODEL} cost:   ${COST}
  • Savings:        {SAVINGS}%
```

## Model Selection Rules for Specify

```yaml
model_selection:
  SIMPLE:
    orchestrator: sonnet
    subagents:
      brownfield-detector: haiku
      workspace-detector: haiku
      concept-loader: haiku
      spec-writer: sonnet
      validator: sonnet

  MODERATE:
    orchestrator: sonnet
    subagents:
      brownfield-detector: haiku
      workspace-detector: haiku
      concept-loader: sonnet
      spec-writer: sonnet
      validator: sonnet

  COMPLEX:
    orchestrator: opus
    subagents:
      brownfield-detector: haiku
      workspace-detector: haiku
      concept-loader: sonnet
      spec-writer: opus
      validator: opus
```

## Examples

### Example 1: SIMPLE (Score: 25)

```text
INPUT: "Add a logout button to the user dashboard"

Analysis:
  • Entities: 1 (user) → 0 pts
  • Integrations: 0 → 0 pts
  • Tech: 0 high, 0 medium, 0 low → 0 pts
  • Scope: single component → 2 pts
  • Word count: 8 words → 0 pts

TIER: SIMPLE (25/100)
MODEL: sonnet
SAVINGS: 80% vs Opus
```

### Example 2: MODERATE (Score: 55)

```text
INPUT: "Build a product catalog with search, filters, and pagination. Support admin CRUD for products."

Analysis:
  • Entities: 2 (product, admin) → 6 pts
  • Integrations: 0 → 0 pts
  • Tech: 0 high, 0 medium, 5 low (CRUD, search, filter, pagination) → 10 pts
  • Scope: multiple pages → 10 pts
  • Word count: 15 words → 0 pts

TIER: MODERATE (26/100)
MODEL: sonnet
SAVINGS: 80% vs Opus

NOTE: Score adjusted to 55 due to feature scope
```

### Example 3: COMPLEX (Score: 85)

```text
INPUT: "Design a real-time collaborative document editing system with operational transformation, conflict resolution, WebSocket streaming, user presence indicators, version history, and integration with Google Drive and Dropbox for import/export."

Analysis:
  • Entities: 3 (document, user, version) → 12 pts
  • Integrations: 2 (Google Drive, Dropbox) → 12 pts
  • Tech: 2 high (real-time, streaming), 1 medium (async) → 38 pts
  • Scope: system-wide → 20 pts
  • Word count: 30 words → 5 pts

TIER: COMPLEX (87/100)
MODEL: opus
SAVINGS: 0% (requires full reasoning capacity)
```

## Override Flags

```bash
/speckit.specify --model=haiku     # Force haiku (use with caution)
/speckit.specify --model=sonnet    # Force sonnet
/speckit.specify --model=opus      # Force opus (disable adaptive)
/speckit.specify --auto-model      # Enable adaptive (default)
```

## Integration with `/speckit.specify`

Add to specify.md workflow:

```markdown
## Step 0: Complexity Detection (Pre-orchestration)

1. Read templates/shared/specify/complexity-detection.md
2. Run detection algorithm on user input
3. Determine TIER and RECOMMENDED_MODEL
4. Display assessment to user
5. Override orchestrator model and subagent models based on tier
6. Store TIER in feature metadata for future commands
```

## Quality Preservation

**Critical safeguard**: Even with SIMPLE/MODERATE tiers using Sonnet:

- ✅ Validation gates still apply (Constitution Alignment, Ambiguity Gate)
- ✅ SQS scoring unchanged (threshold: 80)
- ✅ Auto-remediation triggers if validation fails
- ✅ Handoff to `/speckit.clarify` if ambiguity detected

**Quality is NOT compromised** - only orchestration model is adapted.

## Calibration Data

Track actual complexity outcomes to refine scoring:

```yaml
# .speckit/complexity-calibration.yaml
features:
  - id: "001-login"
    predicted_tier: SIMPLE
    predicted_score: 35
    actual_tier: SIMPLE  # Based on implementation time
    model_used: sonnet
    quality_score: 85  # SQS
    feedback: "Accurate - straightforward CRUD"

  - id: "002-realtime-chat"
    predicted_tier: MODERATE
    predicted_score: 55
    actual_tier: COMPLEX  # Took longer than expected
    model_used: sonnet
    quality_score: 72  # Needed rework
    feedback: "Underestimated - should have been COMPLEX"
```

## Cost Tracking

Display estimated savings:

```text
┌─────────────────────────────────────────┐
│ Model Selection: sonnet (MODERATE)     │
├─────────────────────────────────────────┤
│ Estimated cost:    $0.10                │
│ Opus baseline:     $0.50                │
│ Savings:           $0.40 (80%)          │
│ Expected time:     30-60s               │
└─────────────────────────────────────────┘
```

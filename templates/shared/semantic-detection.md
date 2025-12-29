# Semantic Detection

## Purpose

Replace simple keyword matching with confidence-scored semantic analysis for detecting user intent, feature types, and required workflow actions. Provides more accurate classification with explicit confidence levels.

## Why This Matters

| Approach | Problem | Solution |
|----------|---------|----------|
| **Keyword Matching** | "add login" triggers ADD but "additional info for login" also triggers ADD | Semantic context analysis |
| **Hard Rules** | Misses synonyms and variations | Confidence-weighted scoring |
| **Binary Decisions** | No uncertainty handling | Thresholds with user confirmation |

## Core Concepts

### Confidence Thresholds

```text
CONFIDENCE_THRESHOLDS = {
  HIGH:   0.80  # Proceed automatically
  MEDIUM: 0.50  # Ask user to confirm
  LOW:    0.30  # Ask user explicitly
  NONE:   0.00  # No match detected
}
```

### Intent Classification Engine

```text
CLASSIFY_INTENT(user_input):

  1. TOKENIZE: Split input into words, normalize case
  2. EXTRACT_ENTITIES: Identify nouns (features, components, systems)
  3. EXTRACT_ACTIONS: Identify verbs (add, modify, fix, remove)
  4. CONTEXT_ANALYSIS: Check surrounding words for disambiguation
  5. CODEBASE_CROSS_REF: Match entities against existing code/specs
  6. CALCULATE_CONFIDENCE: Score based on signal strength
```

## Intent Detection Patterns

### Pattern 1: Feature Intent (ADD / MODIFY / REMOVE)

```text
FEATURE_INTENT_SIGNALS:

ADD_SIGNALS (confidence weights):
  - "add", "create", "implement", "build", "new": 0.8 base
  - "want to have", "need to support": 0.7
  - No existing feature with same name: +0.2
  - Context: subject is NEW entity: +0.15

MODIFY_SIGNALS:
  - "modify", "change", "update", "improve", "enhance": 0.8 base
  - "existing", "current", "our current": +0.2
  - Feature exists in manifest: +0.3 (definitive boost)

REMOVE_SIGNALS:
  - "remove", "delete", "deprecate", "disable": 0.8 base
  - "no longer need", "get rid of": 0.7
  - Feature exists in codebase: +0.2

DISAMBIGUATION:
  - "add additional info" → NOT ADD (additional is adjective)
  - "add new login" → ADD (new is adjective modifying login)
  - "modify the add button" → MODIFY (add is noun, part of UI element name)
```

### Pattern 2: Change Type Detection

```text
CHANGE_TYPE_SIGNALS:

ENHANCEMENT:
  - "add feature", "new capability", "extend functionality": 0.9
  - "want users to be able to": 0.8

BUGFIX:
  - "fix", "bug", "issue", "broken", "doesn't work": 0.9
  - "should work but", "expected to": 0.7

REFACTOR:
  - "refactor", "restructure", "reorganize", "clean up": 0.9
  - "improve code", "better architecture": 0.7

MIGRATION:
  - "migrate", "upgrade", "move from X to Y": 0.9
  - "switch from", "replace X with Y": 0.8

PERFORMANCE:
  - "optimize", "performance", "speed up", "faster": 0.9
  - "slow", "takes too long", "timeout": 0.7

SECURITY:
  - "security", "vulnerability", "CVE", "exploit": 0.9
  - "authentication", "authorization", "encrypt": 0.6 (lower - could be feature)
```

### Pattern 3: Scope Detection

```text
SCOPE_SIGNALS:

SINGLE_COMPONENT:
  - Mentions 1 specific file/class/function: 0.8
  - "the X component", "just the Y": 0.7

MULTI_COMPONENT:
  - Mentions 2-4 components: 0.8
  - "and", "also", "as well as": +0.1 per occurrence

SYSTEM_WIDE:
  - "across the system", "everywhere", "all services": 0.9
  - "platform", "infrastructure", "architecture": 0.8
  - Mentions > 4 components: 0.7
```

## Detection Algorithm

### Step 1: Parse User Input

```text
PARSED_INPUT = {
  raw: user_input,
  tokens: tokenize(user_input),
  entities: extract_nouns(user_input),
  actions: extract_verbs(user_input),
  adjectives: extract_adjectives(user_input),
  context_phrases: extract_phrases(user_input)
}
```

### Step 2: Score Each Intent Category

```text
INTENT_SCORES = {}

FOR category IN [ADD, MODIFY, REMOVE]:
  score = 0.0
  evidence = []

  FOR signal IN FEATURE_INTENT_SIGNALS[category]:
    IF signal.matches(PARSED_INPUT):
      score += signal.weight
      evidence.append({signal: signal.name, weight: signal.weight})

  # Apply disambiguation rules
  score = apply_disambiguation(score, PARSED_INPUT, category)

  # Cross-reference with codebase
  IF category == MODIFY AND feature_exists_in_manifest(PARSED_INPUT.entities):
    score += 0.3
    evidence.append({signal: "manifest_match", weight: 0.3})

  # Normalize score (cap at 1.0)
  INTENT_SCORES[category] = {
    confidence: min(1.0, score),
    evidence: evidence
  }
```

### Step 3: Select Best Match

```text
BEST_INTENT = max(INTENT_SCORES, key=lambda x: x.confidence)
BEST_CONFIDENCE = INTENT_SCORES[BEST_INTENT].confidence
EVIDENCE = INTENT_SCORES[BEST_INTENT].evidence
```

### Step 4: Make Decision

```text
IF BEST_CONFIDENCE >= 0.80:
  # High confidence - proceed automatically
  DETECTED_INTENT = BEST_INTENT
  DECISION_MODE = "AUTO"
  LOG: "Detected intent: {BEST_INTENT} (confidence: {BEST_CONFIDENCE:.0%})"

ELIF BEST_CONFIDENCE >= 0.50:
  # Medium confidence - ask user to confirm
  ASK_USER: "Detected: {BEST_INTENT} feature (confidence: {BEST_CONFIDENCE:.0%})
             Evidence: {EVIDENCE}
             Is this correct?"

  IF user_confirms:
    DETECTED_INTENT = BEST_INTENT
  ELSE:
    ASK_USER: "What type of change is this? (add/modify/remove)"
    DETECTED_INTENT = user_response

  DECISION_MODE = "CONFIRMED"

ELIF BEST_CONFIDENCE >= 0.30:
  # Low confidence - present options
  sorted_intents = sort(INTENT_SCORES, by=confidence, desc=True)

  ASK_USER: "Multiple interpretations possible:
             1. {sorted_intents[0].intent} ({sorted_intents[0].confidence:.0%})
             2. {sorted_intents[1].intent} ({sorted_intents[1].confidence:.0%})
             Which best describes your intent?"

  DETECTED_INTENT = user_selection
  DECISION_MODE = "USER_SELECTED"

ELSE:
  # No clear match - ask explicitly
  ASK_USER: "Could not determine intent from description.
             What type of change is this? (add/modify/remove/other)"

  DETECTED_INTENT = user_response
  DECISION_MODE = "USER_PROVIDED"
```

### Step 5: Report Detection

```text
DETECTION_RESULT = {
  intent: DETECTED_INTENT,
  confidence: BEST_CONFIDENCE,
  decision_mode: DECISION_MODE,
  evidence: EVIDENCE,
  alternatives: filter(INTENT_SCORES, confidence > 0.30)
}

OUTPUT: "Intent: {DETECTED_INTENT} ({DECISION_MODE})"
IF DECISION_MODE != "AUTO":
  OUTPUT: "Evidence: {EVIDENCE}"
```

## Entity Extraction

### Extracting Feature Names

```text
EXTRACT_FEATURE_NAME(user_input):

  # Pattern 1: Explicit feature mention
  patterns = [
    r"(?:add|create|implement|build)\s+(?:a\s+)?(.+?)\s+(?:feature|functionality)",
    r"(?:feature|for)\s+(.+)",
    r"(.+?)\s+(?:system|module|component)"
  ]

  FOR pattern IN patterns:
    match = regex_match(pattern, user_input)
    IF match:
      candidate = match.group(1)
      confidence = 0.8
      RETURN {name: candidate, confidence: confidence}

  # Pattern 2: Extract main noun phrase
  entities = PARSED_INPUT.entities
  IF entities:
    # Filter out generic nouns
    generic = ["user", "system", "feature", "thing", "stuff"]
    specific_entities = filter(entities, not_in=generic)
    IF specific_entities:
      RETURN {name: specific_entities[0], confidence: 0.6}

  # No clear feature name
  RETURN {name: null, confidence: 0.0}
```

## Usage in Commands

Add to command's early steps:

```markdown
## Step N: Semantic Intent Detection

Read `templates/shared/semantic-detection.md` and apply.

1. Parse user input
2. Score intent categories
3. Make decision based on confidence thresholds
4. Store DETECTED_INTENT and DETECTION_RESULT for use in generation
```

## Caching Hint

Detection results can be cached for the session:
- Key: user_input hash
- Value: `{intent: DETECTED_INTENT, confidence: BEST_CONFIDENCE, feature_name: ...}`
- TTL: Until user input changes

## Fallback Behavior

If semantic detection fails or times out:

1. Fall back to simple keyword matching
2. Log warning: "Semantic detection unavailable, using keyword matching"
3. Apply higher user confirmation threshold (always ask if confidence < 0.9)

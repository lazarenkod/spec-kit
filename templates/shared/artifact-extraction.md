# Artifact Extraction Layer

## Purpose

Extract and cache structured data from artifacts to minimize token consumption.
Pass extracted structures to subagents instead of full file contents.

**Problem**: Commands load full artifacts (50-200KB each) multiple times, causing context window compaction.

**Solution**: Extract only needed fields (2-5KB) and cache for session reuse.

## Performance Impact

| Approach | Context Size | Compactions |
|----------|--------------|-------------|
| Full artifacts (3 subagents × 100KB) | ~300KB per wave | 2-3 |
| Extracted data (3 subagents × 5KB) | ~15KB per wave | 0 |
| **Reduction** | **95%** | **100%** |

---

## Configuration

```yaml
artifact_extraction:
  enabled: true
  skip_flag: "--full-context"

  spec_fields:
    - fr_list           # FR-001, FR-002, ...
    - as_list           # AS-1A, AS-1B, ...
    - ec_list           # EC-001, EC-002, ...
    - sc_list           # SC-001, SC-002, ...
    - story_priorities  # {US1: P1a, US2: P1b, ...}
    - component_registry
    - fr_summaries      # [{id: FR-001, summary: "..."}, ...]
    - as_summaries      # [{id: AS-1A, name: "..."}, ...]

  plan_fields:
    - tech_stack
    - dependencies
    - phases
    - adr_decisions
```

---

## EXTRACT_SPEC Algorithm

```text
FUNCTION EXTRACT_SPEC(spec_path):
  """
  Extract structured data from spec.md.
  Returns cached result if already parsed in session.
  """

  CACHE_KEY = "spec_extracted:" + spec_path

  IF CACHE_KEY IN SESSION_CACHE:
    LOG "📦 Using cached spec extraction"
    RETURN SESSION_CACHE[CACHE_KEY]

  spec_content = READ(spec_path)
  original_size = len(spec_content)

  extracted = {
    # ===== Traceability IDs (~1-2KB instead of 50-200KB) =====

    fr_list: EXTRACT_PATTERN(spec_content, r"FR-\d{3}"),
    # → ["FR-001", "FR-002", "FR-003", ...]

    as_list: EXTRACT_PATTERN(spec_content, r"AS-\d+[A-Z]"),
    # → ["AS-1A", "AS-1B", "AS-2A", ...]

    ec_list: EXTRACT_PATTERN(spec_content, r"EC-\d{3}"),
    # → ["EC-001", "EC-002", ...]

    sc_list: EXTRACT_PATTERN(spec_content, r"SC-\d{3}"),
    # → ["SC-001", "SC-002", ...]

    # ===== Story Priorities (~500B) =====

    story_priorities: EXTRACT_STORY_PRIORITIES(spec_content),
    # → {"US1": "P1a", "US2": "P1b", "US3": "P2a", ...}

    # ===== Component Registry (~2-5KB, for UI features) =====

    component_registry: EXTRACT_SECTION(spec_content, "UI Component Registry"),
    # → Raw markdown table or empty string

    screen_registry: EXTRACT_SECTION(spec_content, "Screen Registry"),
    # → Raw markdown table or empty string

    # ===== FR Summaries (~5KB) =====

    fr_summaries: EXTRACT_FR_SUMMARIES(spec_content),
    # → [{id: "FR-001", summary: "System MUST validate..."}, ...]

    # ===== AS Summaries (~3KB) =====

    as_summaries: EXTRACT_AS_SUMMARIES(spec_content),
    # → [{id: "AS-1A", name: "**Happy Path Login**"}, ...]

    # ===== NFRs (~2KB) =====

    nfr_list: EXTRACT_PATTERN(spec_content, r"NFR-\d{3}"),
    # → ["NFR-001", "NFR-002", ...]

    # ===== Metadata =====

    _source_path: spec_path,
    _original_size_kb: round(original_size / 1024, 1),
    _extracted_at: NOW()
  }

  extracted_size = estimate_size(extracted)

  SESSION_CACHE[CACHE_KEY] = extracted

  LOG "📊 Extracted spec data:"
  LOG "├── FRs: {len(extracted.fr_list)}"
  LOG "├── ASs: {len(extracted.as_list)}"
  LOG "├── ECs: {len(extracted.ec_list)}"
  LOG "└── Size: {extracted._original_size_kb}KB → {extracted_size}KB ({reduction}% reduction)"

  RETURN extracted
```

---

## EXTRACT_PLAN Algorithm

```text
FUNCTION EXTRACT_PLAN(plan_path):
  """
  Extract tech stack and structure from plan.md.
  Returns cached result if already parsed in session.
  """

  CACHE_KEY = "plan_extracted:" + plan_path

  IF CACHE_KEY IN SESSION_CACHE:
    LOG "📦 Using cached plan extraction"
    RETURN SESSION_CACHE[CACHE_KEY]

  plan_content = READ(plan_path)
  original_size = len(plan_content)

  extracted = {
    # ===== Technical Context (~1-2KB) =====

    tech_stack: EXTRACT_SECTION(plan_content, "Technical Context"),
    # → Markdown section content

    # ===== Dependencies (~2KB) =====

    dependencies: EXTRACT_SECTION(plan_content, "Dependency Registry"),
    # → Markdown table or section

    # ===== Phase Structure (~1KB) =====

    phases: EXTRACT_HEADERS(plan_content, level=3),
    # → ["Phase 0: Setup", "Phase 1: Core", "Phase 2: Integration", ...]

    # ===== ADR Summaries (~2KB) =====

    adr_decisions: EXTRACT_ADR_TITLES(plan_content),
    # → ["ADR-001: Use PostgreSQL", "ADR-002: REST over GraphQL", ...]

    # ===== NFR Targets (~1KB) =====

    nfr_targets: EXTRACT_SECTION(plan_content, "NFR Definition"),
    # → Performance targets, SLA definitions

    # ===== RTM Preview (~1KB) =====

    rtm_summary: EXTRACT_SECTION(plan_content, "Requirements Traceability Matrix"),
    # → RTM table for reference

    # ===== Metadata =====

    _source_path: plan_path,
    _original_size_kb: round(original_size / 1024, 1),
    _extracted_at: NOW()
  }

  extracted_size = estimate_size(extracted)

  SESSION_CACHE[CACHE_KEY] = extracted

  LOG "📊 Extracted plan data:"
  LOG "├── Phases: {len(extracted.phases)}"
  LOG "├── ADRs: {len(extracted.adr_decisions)}"
  LOG "└── Size: {extracted._original_size_kb}KB → {extracted_size}KB"

  RETURN extracted
```

---

## EXTRACT_CONCEPT Algorithm

```text
FUNCTION EXTRACT_CONCEPT(concept_path):
  """
  Extract traceability and structure from concept.md.
  Returns cached result if already parsed in session.
  """

  CACHE_KEY = "concept_extracted:" + concept_path

  IF CACHE_KEY IN SESSION_CACHE:
    LOG "📦 Using cached concept extraction"
    RETURN SESSION_CACHE[CACHE_KEY]

  IF NOT exists(concept_path):
    RETURN null

  concept_content = READ(concept_path)

  extracted = {
    # ===== Feature Hierarchy (~2KB) =====

    epic_ids: EXTRACT_PATTERN(concept_content, r"EPIC-\d{3}"),
    feature_ids: EXTRACT_PATTERN(concept_content, r"F\d{2}"),
    story_ids: EXTRACT_PATTERN(concept_content, r"S\d{2}"),

    # ===== User Journeys (~1KB) =====

    journey_ids: EXTRACT_PATTERN(concept_content, r"J\d{3}"),

    # ===== Traceability Skeleton (~2KB) =====

    traceability_skeleton: EXTRACT_SECTION(concept_content, "Traceability Skeleton"),

    # ===== Metadata =====

    _source_path: concept_path,
    _extracted_at: NOW()
  }

  SESSION_CACHE[CACHE_KEY] = extracted

  RETURN extracted
```

---

## Helper Functions

### EXTRACT_SECTION

```text
FUNCTION EXTRACT_SECTION(content, header):
  """
  Extract content between header and next same-level header.
  Supports ## and ### headers.
  """

  # Try ## header first
  pattern = rf"## {header}\s*\n(.*?)(?=\n## |\Z)"
  match = regex.search(pattern, content, DOTALL)

  IF match:
    RETURN match.group(1).strip()

  # Try ### header
  pattern = rf"### {header}\s*\n(.*?)(?=\n### |\n## |\Z)"
  match = regex.search(pattern, content, DOTALL)

  IF match:
    RETURN match.group(1).strip()

  RETURN ""
```

### EXTRACT_PATTERN

```text
FUNCTION EXTRACT_PATTERN(content, pattern):
  """
  Extract all unique matches of a pattern, preserving order.
  """

  matches = regex.findall(pattern, content)
  seen = set()
  unique = []

  FOR match IN matches:
    IF match NOT IN seen:
      seen.add(match)
      unique.append(match)

  RETURN unique
```

### EXTRACT_FR_SUMMARIES

```text
FUNCTION EXTRACT_FR_SUMMARIES(content):
  """
  Extract FR ID + first sentence only.
  """

  frs = []

  # Pattern: FR-001: System MUST do something.
  # Or: | FR-001 | System MUST do something | ...
  patterns = [
    r"(FR-\d{3})[:\s]+([^.\n]+\.)",           # Prose format
    r"\|\s*(FR-\d{3})\s*\|\s*([^|]+?)\s*\|"   # Table format
  ]

  FOR pattern IN patterns:
    FOR match IN regex.findall(pattern, content):
      fr_id = match[0]
      summary = match[1].strip()[:200]  # Limit to 200 chars

      # Avoid duplicates
      IF NOT any(fr.id == fr_id FOR fr IN frs):
        frs.append({
          id: fr_id,
          summary: summary
        })

  RETURN frs
```

### EXTRACT_AS_SUMMARIES

```text
FUNCTION EXTRACT_AS_SUMMARIES(content):
  """
  Extract AS ID + scenario name only.
  """

  scenarios = []

  # Pattern: AS-1A: **Happy Path Login**
  # Or: ### AS-1A: Happy Path
  patterns = [
    r"(AS-\d+[A-Z])[:\s]+\*\*([^*]+)\*\*",    # Bold name
    r"###?\s*(AS-\d+[A-Z])[:\s]+([^\n]+)"     # Header format
  ]

  FOR pattern IN patterns:
    FOR match IN regex.findall(pattern, content):
      as_id = match[0]
      name = match[1].strip()[:100]  # Limit to 100 chars

      IF NOT any(s.id == as_id FOR s IN scenarios):
        scenarios.append({
          id: as_id,
          name: name
        })

  RETURN scenarios
```

### EXTRACT_STORY_PRIORITIES

```text
FUNCTION EXTRACT_STORY_PRIORITIES(content):
  """
  Extract user story priorities from spec.md.
  """

  priorities = {}

  # Pattern: | US1 | P1a | ... or | User Story 1 | P1a |
  # Or: **US1** (P1a): ...
  patterns = [
    r"\|\s*(?:US)?(\d+)\s*\|\s*(P\d+[a-z]?)\s*\|",
    r"\*\*US(\d+)\*\*\s*\((P\d+[a-z]?)\)"
  ]

  FOR pattern IN patterns:
    FOR match IN regex.findall(pattern, content):
      us_num = match[0]
      priority = match[1]
      priorities[f"US{us_num}"] = priority

  RETURN priorities
```

### EXTRACT_HEADERS

```text
FUNCTION EXTRACT_HEADERS(content, level=3):
  """
  Extract all headers of specified level.
  """

  prefix = "#" * level
  pattern = rf"^{prefix}\s+(.+)$"

  headers = []
  FOR match IN regex.findall(pattern, content, MULTILINE):
    headers.append(match.strip())

  RETURN headers
```

### EXTRACT_ADR_TITLES

```text
FUNCTION EXTRACT_ADR_TITLES(content):
  """
  Extract ADR titles from plan.md.
  """

  adrs = []

  # Pattern: ### ADR-001: Decision Title
  # Or: **ADR-001**: Decision Title
  patterns = [
    r"###?\s*(ADR-\d{3})[:\s]+([^\n]+)",
    r"\*\*(ADR-\d{3})\*\*[:\s]+([^\n]+)"
  ]

  FOR pattern IN patterns:
    FOR match IN regex.findall(pattern, content):
      adr_id = match[0]
      title = match[1].strip()[:100]
      adrs.append(f"{adr_id}: {title}")

  RETURN adrs
```

---

## Usage in Commands

### In Prefetch Phase

```text
## Step 0: Prefetch and Extract

IF artifact_extraction.enabled AND NOT "--full-context" IN ARGS:

  # 1. Load files (parallel, as before)
  PREFETCH_BATCH(
    paths=[constitution, templates, spec.md, plan.md],
    optional_paths=[concept.md]
  )

  # 2. Extract structured data (NEW)
  SPEC_DATA = EXTRACT_SPEC(FEATURE_DIR/spec.md)
  PLAN_DATA = EXTRACT_PLAN(FEATURE_DIR/plan.md)
  CONCEPT_DATA = EXTRACT_CONCEPT(specs/concept.md)  # May be null

  PRINT "📊 Artifact extraction complete:"
  PRINT "├── spec: {len(SPEC_DATA.fr_list)} FRs, {len(SPEC_DATA.as_list)} ASs"
  PRINT "├── plan: {len(PLAN_DATA.phases)} phases, {len(PLAN_DATA.adr_decisions)} ADRs"
  PRINT "└── Context reduction: ~{original_total}KB → ~{extracted_total}KB"

ELSE:
  # Legacy: load full files
  PREFETCH_BATCH(...)
  LOG "⚠️ Full context mode: using complete artifacts"
```

### In Subagent Prompts

```text
# BEFORE (high token consumption):
subagents:
  - role: fr-mapper
    prompt: |
      Map functional requirements to tasks.

      Full spec.md:
      {SPEC_CONTENT}  # 50-200KB

      Full plan.md:
      {PLAN_CONTENT}  # 30-100KB

# AFTER (optimized):
subagents:
  - role: fr-mapper
    context_injection: extracted
    prompt: |
      Map functional requirements to tasks.

      FR List ({len(SPEC_DATA.fr_list)} items):
      {format_list(SPEC_DATA.fr_summaries)}

      Tech Stack:
      {PLAN_DATA.tech_stack}

      Dependencies:
      {PLAN_DATA.dependencies}
```

### In Self-Review (Avoid Re-read)

```text
## Self-Review Step 1: Parse Generated Tasks

# Use in-memory content if available (NEW)
IF GENERATED_ARTIFACT_CONTENT exists:
  artifact_content = GENERATED_ARTIFACT_CONTENT
  LOG "📦 Using in-memory content (saved {file_size}KB read)"
ELSE:
  artifact_content = READ(ARTIFACT_PATH)

# Continue with parsing...
```

---

## Skip Flag

```text
IF "--full-context" IN ARGS:
  LOG "⚠️ Artifact extraction DISABLED (full context mode)"
  LOG "   Using complete file contents for maximum fidelity"
  SKIP extraction, load full files as before
```

Use `--full-context` when:
- Debugging extraction issues
- Complex features where summaries may lose context
- First run on a new project to verify extraction patterns

---

## Caching Behavior

```text
SESSION_CACHE = {}  # Persists for entire command session

# Cache keys:
# - "spec_extracted:{path}" → SPEC_DATA
# - "plan_extracted:{path}" → PLAN_DATA
# - "concept_extracted:{path}" → CONCEPT_DATA

# Benefits:
# - Extract once, use multiple times
# - Subagents share cached data
# - Self-review uses cached extraction
```

---

## Error Handling

```text
EXTRACTION_ERROR_STRATEGY:

  # Pattern extraction failure
  IF extraction returns empty AND expected non-empty:
    LOG "⚠️ Extraction returned empty for {field}"
    LOG "   Pattern may not match this spec format"

    IF "--strict-extraction" IN ARGS:
      ERROR: "Extraction failed for required field {field}"
    ELSE:
      CONTINUE with empty value

  # Section not found
  IF EXTRACT_SECTION returns empty:
    LOG "ℹ️ Section '{header}' not found in {file}"
    RETURN ""  # Empty is valid, section may not exist

  # File read failure
  IF READ fails:
    ERROR: "Cannot read {path}: {error}"
    ABORT extraction
```

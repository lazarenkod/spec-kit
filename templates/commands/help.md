---
description: Display help documentation for any speckit command, including flags, examples, and handoffs
handoffs: []
scripts:
  sh: echo "Displaying command help from COMMANDS_GUIDE.md"
  ps: Write-Host "Displaying command help from COMMANDS_GUIDE.md"
flags:
  - name: --thinking-depth
    type: choice
    choices: [standard, ultrathink]
    default: standard
    description: |
      Thinking budget control:
      - standard: 2K budget, fast help display (~$0.03) [RECOMMENDED]
      - ultrathink: 8K budget, detailed examples (~$0.12)
claude_code:
  model: haiku
  reasoning_mode: basic

  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 2000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 4000
        max_parallel: 3
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 2000
        max_parallel: 6
        batch_delay: 1500
        wave_overlap_threshold: 0.65
      ultrathink:
        thinking_budget: 8000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 4.0

  depth_defaults:
    standard:
      thinking_budget: 2000
      timeout: 30
    ultrathink:
      thinking_budget: 8000
      additional_analysis: [example-generator, command-suggester]
      timeout: 60

  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 2000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (8K thinking budget).
          Auto-downgrading to **Standard** mode (2K budget).

  cost_breakdown:
    standard: {cost: $0.03, time: "15-30s"}
    ultrathink: {cost: $0.12, time: "30-60s"}
---

## Input
```text
$ARGUMENTS
```

---

## Purpose

Display comprehensive help documentation for any speckit command, including:
- Command description and purpose
- Required and optional flags with descriptions
- Usage examples
- Handoff commands (next steps in workflow)
- Model and thinking budget information

**Target Audience**: Developers using speckit commands manually

**Source**: `docs/COMMANDS_GUIDE.md` (single source of truth)

---

## Instructions

### Step 1: Parse Command Name

Extract the command name from `$ARGUMENTS`:
- Accept both "concept" and "speckit.concept" formats
- Normalize to "speckit.concept" format for searching
- If empty/missing, display list of all available commands

### Step 2: Read COMMANDS_GUIDE.md

Use the Read tool to load `docs/COMMANDS_GUIDE.md`.

### Step 3: Find Command Section

Search for the command section using pattern:
```
### \d+[a-z]?\. `/speckit\.<command-name>` {#speckit<commandname>}
```

For example, for "games.progression", search for:
```
### 2d. `/speckit.games.progression` {#speckitgamesprogression}
```

Use Grep tool with pattern if Read returns too much content.

### Step 4: Extract Help Content

Parse the command section and extract:

1. **Description** (after `**Назначение:**`)
   - Extract text until next bold section
   - Wrap at 80 characters for readability

2. **Model Info** (after `**Модель:**`)
   - Extract model name and thinking budget
   - Format: `Model: opus (thinking_budget: 120000)`

3. **Flags** (after `**Флаги:**`)
   - Extract each flag line starting with `- \``
   - Parse pattern: `- \`--flag-name <values>\` — Description`
   - Identify REQUIRED flags (marked with "REQUIRED" in description)
   - Identify optional flags with defaults (marked with "default:" in description)
   - Preserve choice values (e.g., `<match3|idle|shooter>`)

4. **Examples** (after `**Пример использования:**` or `**Примеры:**`)
   - Extract code block with example commands
   - Include comments if present

5. **Handoffs** (after `**Handoffs:**`)
   - Extract lines starting with `- →`
   - Format: `→ /speckit.next-command — Description`

### Step 5: Format Help Text

Format the extracted content into this structure:

```
/speckit.<command-name>

DESCRIPTION:
  <description text, wrapped at 80 chars>

MODEL:
  <model-name> (thinking_budget: <budget>)

USAGE:
  /speckit.<command-name> <required-flags> [OPTIONS]

REQUIRED FLAGS:
  --flag-name <choices>
      Description text
      (Multiple required flags if present)

OPTIONS:
  --optional-flag <choices>
      Description text (default: <value>)

  --another-flag
      Description text

EXAMPLES:
  <example commands from documentation>

HANDOFFS:
  → /speckit.next — Description
  → /speckit.other — Description

---
For full documentation, see: docs/COMMANDS_GUIDE.md#speckit<commandname>
```

**Formatting Rules**:
- Maximum line width: 80 characters
- Indent descriptions under flags by 6 spaces
- Keep flag syntax consistent (preserve `<>` for choices)
- Preserve Russian text from COMMANDS_GUIDE.md (don't translate)
- Use em-dash (—) for handoffs, not hyphen (-)

### Step 6: Display Help

Output the formatted help text directly (no markdown code blocks).

---

## Error Handling

### If Command Not Found

If the command section is not found in COMMANDS_GUIDE.md:

1. Display error message:
   ```
   ❌ Command '/speckit.<command-name>' not found in documentation.
   ```

2. List all available commands:
   - Use Grep to extract all command headers from COMMANDS_GUIDE.md
   - Pattern: `### \d+[a-z]?\. \`/speckit\.([a-z.-]+)\``
   - Display as numbered list

3. Suggest closest match (optional):
   - Use fuzzy matching on command names
   - Suggest top 3 similar commands

**Example Error Output**:
```
❌ Command '/speckit.game-progression' not found in documentation.

Available commands:
  1. /speckit.constitution
  2. /speckit.concept
  3. /speckit.games.concept
  4. /speckit.games.mechanics
  5. /speckit.games.progression
  ... (show first 20)

Did you mean: /speckit.games.progression?

For full list, see: docs/COMMANDS_GUIDE.md
```

### If Missing Sections

If a command section lacks certain subsections:
- **No flags**: Omit "REQUIRED FLAGS" and "OPTIONS" sections
- **No examples**: Omit "EXAMPLES" section
- **No handoffs**: Omit "HANDOFFS" section
- Always include: DESCRIPTION, MODEL, USAGE

---

## Example Output

For `/speckit.help games.progression`:

```
/speckit.games.progression

DESCRIPTION:
  Design comprehensive game progression with 200+ levels, difficulty curves,
  unlock gates, meta-progression systems (prestige, skill trees, account
  leveling, ascension), and Flow Channel validation. Ensures smooth difficulty
  scaling, optimal player engagement, and long-term retention through
  mathematically validated progression design.

MODEL:
  opus (thinking_budget: 120000)

USAGE:
  /speckit.games.progression --genre <genre> [OPTIONS]

REQUIRED FLAGS:
  --genre <match3|idle|shooter|arcade|puzzle|runner|platformer>
      Game genre (REQUIRED)

OPTIONS:
  --level-count <50|100|200|500|infinite>
      Target level count (default: 200)

  --difficulty-model <linear|exponential|logarithmic|s-curve>
      Difficulty scaling model (default: exponential)

  --meta-depth <basic|standard|deep>
      Meta-progression depth (default: deep)

  --flow-validation <true|false>
      Enable Flow Channel validation (default: true)

  --skip-gates
      Skip quality gates validation (not recommended)

EXAMPLES:
  # Standard 200-level progression for match-3 with deep meta-progression
  /speckit.games.progression --genre match3 --level-count 200 --meta-depth deep

  # Idle game with infinite progression and exponential scaling
  /speckit.games.progression --genre idle --level-count infinite

  # Quick 50-level arcade game with basic progression
  /speckit.games.progression --genre arcade --level-count 50 --meta-depth basic

HANDOFFS:
  → /speckit.implement — Handoff progression specs for implementation
  → /speckit.games.virality — Use progression data for K-factor optimization

---
For full documentation, see: docs/COMMANDS_GUIDE.md#speckitgamesprogression
```

---

## Notes

- Response time: <5 seconds typical (haiku model is fast)
- Cost: ~$0.01 per help invocation
- No changes to the requested command itself (help is read-only)
- Help content is always up-to-date (reads from COMMANDS_GUIDE.md on each invocation)

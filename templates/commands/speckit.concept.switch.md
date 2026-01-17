---
name: "Switch Concept Variant"
description: "Switch to a different concept alternative"
usage: "/speckit.concept.switch [1-5]"
flags:
  - name: --thinking-depth
    type: choice
    choices: [minimal, quick, standard, thorough]
    default: minimal
    description: |
      Thinking budget (Claude Code Max tier):
      - minimal: 4K budget, ~30s (~$0.06)
      - quick: 8K budget, ~60s (~$0.12)
      - standard: 16K budget, ~90s (~$0.24)
      - thorough: 32K budget, ~120s (~$0.48)

      Free tier: 25% budgets | Pro tier: 50-67% budgets
claude_code:
  model: haiku

  rate_limits:
    default_tier: max
    tiers:
      free:
        minimal: 1000    # 25% of 4K
        quick: 2000      # 25% of 8K
        standard: 4000   # 25% of 16K
        thorough: 8000   # 25% of 32K
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90

      pro:
        minimal: 2000    # 50% of 4K
        quick: 4000      # 50% of 8K
        standard: 10720  # 67% of 16K
        thorough: 21440  # 67% of 32K
        max_parallel: 3
        batch_delay: 4000
        wave_overlap_threshold: 0.80

      max:
        minimal: 4000
        quick: 8000
        standard: 16000
        thorough: 32000
        max_parallel: 6
        batch_delay: 1500
        wave_overlap_threshold: 0.65

  depth_defaults:
    minimal:
      thinking_budget: 4000
      timeout: 30

    quick:
      thinking_budget: 8000
      timeout: 60

    standard:
      thinking_budget: 16000
      timeout: 90

    thorough:
      thinking_budget: 32000
      timeout: 120

  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier == 'free' AND requested_depth == 'thorough'"
        fallback_depth: "standard"
        fallback_thinking: 16000
        warning_message: |
          ⚠️ **Thorough mode requires Pro tier or higher**.
          Auto-downgrading to **Standard** mode (16K budget).

      - condition: "user_tier == 'free' AND requested_depth == 'standard'"
        fallback_depth: "quick"
        fallback_thinking: 8000
        warning_message: |
          ⚠️ **Standard mode requires Pro tier**.
          Auto-downgrading to **Quick** mode (8K budget).

  cost_breakdown:
    minimal: {cost: $0.06, time: "30s"}
    quick: {cost: $0.12, time: "60s"}
    standard: {cost: $0.24, time: "90s"}
    thorough: {cost: $0.48, time: "120s"}
---

# /speckit.concept.switch

## Purpose

Switch `specs/concept.md` to a different product alternative after autonomous generation.

## Usage

```bash
/speckit.concept.switch [1-5]
```

**Arguments**:
- `[1-5]`: Alternative number (1=Conventional, 2=Minimal, 3=Disruptive, 4=Premium, 5=Platform)

**Example**:
```bash
# Switch to platform variant
/speckit.concept.switch 5
```

---

## Execution Flow

### Step 1: Parse Arguments

```python
import sys

if len(sys.argv) < 2:
    print("Usage: /speckit.concept.switch [1-5]")
    sys.exit(1)

try:
    alt_num = int(sys.argv[1])
    if alt_num < 1 or alt_num > 5:
        raise ValueError
except ValueError:
    print("Error: Alternative must be 1-5")
    sys.exit(1)
```

### Step 2: Validate Alternative Exists

```python
alt_file = f"specs/alternatives/0{alt_num}-*.md"
matches = glob.glob(alt_file)

if not matches:
    print(f"Error: Alternative {alt_num} not found.")
    print("Run /speckit.concept first to generate alternatives.")
    sys.exit(1)

alt_path = matches[0]
alt_name = Path(alt_path).stem.split('-', 1)[1]  # Extract name
```

### Step 3: Read Alternative Content

```python
with open(alt_path, 'r') as f:
    alt_content = f.read()

# Extract CQS score from content
cqs_match = re.search(r'CQS Score\*\*: (\d+)/100', alt_content)
cqs_score = cqs_match.group(1) if cqs_match else "N/A"
```

### Step 4: Read Current Selection

```python
with open('specs/concept.md', 'r') as f:
    current_content = f.read()

# Extract current alternative number
current_match = re.search(r'Alternative (\d+):', current_content)
current_num = current_match.group(1) if current_match else "?"
```

### Step 5: Update concept.md

```python
# Add selection banner
banner = f"""
# Concept: {project_name}

> **Selected Alternative**: {alt_num} - {alt_name.title()} (CQS: {cqs_score}/100)
> **Switched from**: Alternative {current_num}
> **Date**: {datetime.now().strftime('%Y-%m-%d')}

---

"""

# Write new content
with open('specs/concept.md', 'w') as f:
    f.write(banner + alt_content)
```

### Step 6: Update Comparison File

```python
# Update specs/concept-alternatives.md
with open('specs/concept-alternatives.md', 'r') as f:
    comparison = f.read()

# Replace "Auto-Selected" section
new_section = f"""
## Selected Concept

**Alternative {alt_num}: {alt_name.title()}** (CQS: {cqs_score}/100)

**Selection Method**: Manual (switched by user from Alternative {current_num})
**Switched Date**: {datetime.now().strftime('%Y-%m-%d')}
"""

comparison = re.sub(
    r'## (Auto-)?Selected Concept.*?---',
    new_section + '\n---',
    comparison,
    flags=re.DOTALL
)

with open('specs/concept-alternatives.md', 'w') as f:
    f.write(comparison)
```

### Step 7: Display Confirmation

```python
print(f"""
✅ Switched to Alternative {alt_num}: {alt_name.title()}

📊 Previous: Alternative {current_num}
   Current: Alternative {alt_num} - {alt_name.title()} (CQS: {cqs_score}/100)

📄 Updated Files:
   - specs/concept.md
   - specs/concept-alternatives.md

💡 All alternatives preserved in specs/alternatives/

Next steps:
   - Review: cat specs/concept.md
   - Specify feature: /speckit.specify EPIC-001
   - Switch again: /speckit.concept.switch [1-5]
""")
```

---

## Error Handling

| Error | Message | Exit Code |
|-------|---------|-----------|
| No arguments | `Usage: /speckit.concept.switch [1-5]` | 1 |
| Invalid number | `Error: Alternative must be 1-5` | 1 |
| File not found | `Error: Alternative {N} not found. Run /speckit.concept first.` | 1 |
| Read error | `Error: Could not read {file}: {error}` | 1 |

---

## Integration with Downstream Commands

After switching, downstream commands work normally:
- `/speckit.specify` - Uses `specs/concept.md` (now switched variant)
- `/speckit.plan` - Reads from `specs/concept.md`
- `/speckit.tasks` - Reads from `specs/concept.md`

**No conflicts** - All commands use `specs/concept.md` as source of truth.

# Alternative Parser

## Purpose

Parse concept alternatives and variants from `concept.md` for design and preview generation.

---

## Data Structures

### Product Alternative

```yaml
Alternative:
  number: 1-5                    # Alternative number
  name: "string"                 # Alternative name
  strategy_type: enum            # Conventional/Minimal/Disruptive/Premium/Platform
  vision: "string"               # 1-2 sentence vision
  core_features: ["EPIC-xxx"]    # 5-7 core epics
  pros: ["string"]               # List of pros
  cons: ["string"]               # List of cons
  effort: enum                   # S/M/L/XL
  technical_risk: enum           # Low/Medium/High
  time_to_mvp: "X weeks"         # Timeline
  score: number                  # Total score /40
  score_breakdown:
    problem_solution_fit: number # /12
    market_differentiation: number # /10
    feasibility: number          # /10
    time_to_market: number       # /8
```

### Concept Variant

```yaml
Variant:
  name: enum                     # MINIMAL/BALANCED/AMBITIOUS
  philosophy: "string"           # Short description
  features: ["EPIC-xxx.Fxx"]     # Included feature IDs
  timeline: "X weeks"            # Time to MVP
  team_size: "X FTEs"            # Team requirement
  risk_level: enum               # Low/Medium/High
  included_priorities: ["P1", "P2"]  # Which priorities included
```

---

## Parsing Logic

### Parse Alternatives from concept.md

```text
FUNCTION parse_alternatives(concept_content):
  alternatives = []

  # Find all alternative sections
  REGEX = /### Alternative \[(\d+)\]: (.+?) — (.+?)$/gm

  FOR each match in concept_content:
    alt = {
      number: match[1],
      name: match[2],
      vision: match[3]
    }

    # Extract section content until next ### or ##
    section_content = extract_section(match.end, next_header)

    # Parse strategy type
    strategy_match = section_content.match(/Strategy Type:\s*(\w+)/)
    alt.strategy_type = strategy_match[1]

    # Parse core features
    features_section = extract_between("Core Features:", next_field)
    alt.core_features = parse_list(features_section)

    # Parse pros/cons
    alt.pros = parse_list(extract_between("Pros:", "Cons:"))
    alt.cons = parse_list(extract_between("Cons:", next_field))

    # Parse metrics
    alt.effort = extract_value("Effort:")
    alt.technical_risk = extract_value("Technical Risk:")
    alt.time_to_mvp = extract_value("Time to MVP:")

    # Parse score
    score_match = section_content.match(/Total:\s*(\d+)\/40/)
    alt.score = int(score_match[1])

    alternatives.push(alt)

  RETURN alternatives
```

### Parse Variants from concept.md

```text
FUNCTION parse_variants(concept_content):
  variants = []

  # Find all variant sections
  REGEX = /### Variant: (MINIMAL|BALANCED|AMBITIOUS)$/gm

  FOR each match in concept_content:
    variant = {
      name: match[1]
    }

    section_content = extract_section(match.end, next_header)

    # Parse philosophy
    phil_match = section_content.match(/Philosophy:\s*(.+)$/)
    variant.philosophy = phil_match[1]

    # Parse included features table
    features_table = extract_table("Included Features")
    variant.features = parse_feature_ids(features_table)

    # Parse metrics
    variant.timeline = extract_value("Timeline:")
    variant.team_size = extract_value("Team:")
    variant.risk_level = extract_value("Risk:")

    variants.push(variant)

  RETURN variants
```

### Check if Alternatives Exist

```text
FUNCTION has_alternatives(concept_content):
  RETURN concept_content.includes("### Alternative [")

FUNCTION has_variants(concept_content):
  RETURN concept_content.includes("### Variant: MINIMAL")
```

---

## Usage in Commands

### In design.md

```text
IF --all-alternatives:
  concept_path = find_concept_md()  # specs/concept.md or ./concept.md
  concept_content = read_file(concept_path)

  IF NOT has_alternatives(concept_content):
    ERROR "No alternatives found in concept.md. Run /speckit.concept first."

  alternatives = parse_alternatives(concept_content)

  FOR each alt in alternatives:
    output_dir = "specs/app-design/alternatives/alt-{alt.number}-{slugify(alt.strategy_type)}/"
    generate_design_for_alternative(alt, output_dir)

  generate_comparison_matrix(alternatives, "specs/app-design/alternatives/comparison.md")

IF --alternative N:
  alternatives = parse_alternatives(concept_content)
  alt = alternatives.find(a => a.number == N)

  IF NOT alt:
    ERROR "Alternative {N} not found. Available: 1-{alternatives.length}"

  generate_design_for_alternative(alt, output_dir)
```

### In preview.md

```text
IF --all-alternatives:
  # Check if designs exist for alternatives
  alt_designs = glob("specs/app-design/alternatives/alt-*/")

  IF alt_designs.empty:
    ERROR "No alternative designs found. Run /speckit.design --concept --all-alternatives first."

  FOR each alt_dir in alt_designs:
    generate_preview_for_alternative(alt_dir)

  generate_gallery_index("alternatives")
```

---

## Output Directory Naming

### Alternative Design Directories

```text
Pattern: alt-{N}-{strategy_slug}/
Examples:
  alt-1-conventional/
  alt-2-minimal/
  alt-3-disruptive/
  alt-4-premium/
  alt-5-platform/
```

### Variant Design Directories

```text
Pattern: {variant_name}/
Examples:
  MINIMAL/
  BALANCED/
  AMBITIOUS/
```

---

## Comparison Matrix Generation

### For Alternatives

```markdown
# Alternative Comparison

| Dimension | Alt 1: Conventional | Alt 2: Disruptive | Alt 3: Premium |
|-----------|:-------------------:|:-----------------:|:--------------:|
| **Strategy** | Standard approach | Contrarian | Best-in-class |
| **Score** | 32/40 | 28/40 | 35/40 |
| **Effort** | M | L | XL |
| **Risk** | Low | High | Medium |
| **MVP Time** | 8 weeks | 12 weeks | 16 weeks |
| **Core Features** | 5 | 7 | 9 |

## Feature Matrix

| Feature | Alt 1 | Alt 2 | Alt 3 |
|---------|:-----:|:-----:|:-----:|
| EPIC-001 User Auth | ✓ | ✓ | ✓ |
| EPIC-002 Dashboard | ✓ | | ✓ |
| EPIC-003 Analytics | | ✓ | ✓ |
| EPIC-004 Integrations | | | ✓ |
```

### For Variants

```markdown
# Variant Comparison

| Dimension | MINIMAL | BALANCED | AMBITIOUS |
|-----------|:-------:|:--------:|:---------:|
| **Philosophy** | Ship fast | Core + diff | Full vision |
| **Features** | 8 | 14 | 22 |
| **Timeline** | 4 weeks | 8 weeks | 14 weeks |
| **Risk** | Low | Medium | High |
| **Coverage** | P1 only | P1 + P2 | P1 + P2 + P3 |
```

---

## Error Handling

| Error | Message | Recovery |
|-------|---------|----------|
| No concept.md | "concept.md not found. Run /speckit.concept first." | Run concept command |
| No alternatives | "No alternatives found in concept.md. Ensure Product Alternatives section exists." | Check concept structure |
| Invalid alt number | "Alternative {N} not found. Available alternatives: 1-{max}" | Use valid number |
| No alt designs | "No alternative designs found. Run /speckit.design --concept --all-alternatives" | Run design first |

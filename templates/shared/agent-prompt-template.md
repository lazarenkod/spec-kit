# Agent Prompt Template

**Purpose**: Single source of truth for repetitive agent prompt structure in concept.md, eliminating 8,000+ tokens of duplication.

## Base Template Structure

```yaml
- role: {{ROLE_NAME}}
  role_group: RESEARCH
  parallel: true
  depends_on: []
  priority: 10
  model_override: {{MODEL}}
  thinking_budget: {{THINKING_BUDGET}}
  reasoning_mode: extended
  role_description: "{{ROLE_DESCRIPTION}}"
  prompt: |
    ## Context
    Project: {{PROJECT_ROOT}}
    User Input: {{ARGUMENTS}}

    ## Your Role
    {{ROLE_INTRO}}

    ## Task
    {{TASK_DESCRIPTION}}

    {{FRAMEWORK_APPLICATION}}

    ## Output Requirements
    {{OUTPUT_REQUIREMENTS}}
```

## Agent Configurations

### market-researcher
- **Role**: Strategic Market Analyst & Co-Founder
- **Framework**: Porter's 5 Forces, Market Sizing, Blue Ocean Reconnaissance
- **Output**: Market dynamics, TAM/SAM/SOM with evidence, timing triggers
- **Model**: Opus | **Thinking**: 120K
- **Key Content**: Lines 114-157 (44 lines)

### competitive-analyst
- **Role**: Strategic Competitive Intelligence Analyst
- **Framework**: Blue Ocean Canvas (ERRC Grid), Competitor Feature Matrix, Pricing Analysis
- **Output**: ERRC Grid, competitor strengths/weaknesses, pricing gaps, unit economics
- **Model**: Opus | **Thinking**: 120K
- **Key Content**: Lines 158-200 (43 lines)

### persona-designer
- **Role**: Strategic Persona & JTBD Researcher
- **Framework**: Jobs-to-Be-Done, Persona Segmentation, Willingness-to-Pay Analysis
- **Output**: 2-4 persona cards, JTBD, WTP analysis with evidence
- **Model**: Opus | **Thinking**: 120K
- **Key Content**: Lines 200-244 (45 lines)

### standards-researcher
- **Role**: Compliance & Standards Researcher
- **Framework**: Domain-specific compliance mapping, regulatory checklists
- **Output**: Standards requirements, compliance checklists, authoritative evidence
- **Model**: Opus | **Thinking**: 120K
- **Key Content**: Lines 246-276 (31 lines)

### academic-researcher
- **Role**: Academic & Best Practices Researcher
- **Framework**: Peer-reviewed papers, industry whitepapers, research synthesis
- **Output**: Validated best practices, peer-reviewed evidence, architectural patterns
- **Model**: Opus | **Thinking**: 120K
- **Key Content**: Lines 277-300+ (24+ lines)

## Token Optimization Strategies

1. **Replace Full Prompts with References**:
   - Instead of embedding 500-600 word prompts in frontmatter
   - Use: `prompt_ref: market-research` → load from `templates/shared/agent-prompts/market-research.md`
   - Save: ~8,000 tokens

2. **Standardized Structure**:
   - All agents follow same pattern: Context → Role → Task → Framework → Output
   - Reduces cognitive overhead for maintenance
   - Easier to validate prompt quality

3. **Reuse Across Commands**:
   - Market-researcher prompt used in: concept.md, validate-concept.md, discover.md
   - Competitive-analyst prompt used in: concept.md, validate-concept.md, baseline.md
   - Reduces duplication across multiple command templates

## Implementation Plan

### Phase 1: Extract Core Prompts (Current)
Create individual prompt files in `templates/shared/agent-prompts/`:
- `market-researcher.md`
- `competitive-analyst.md`
- `persona-designer.md`
- `standards-researcher.md`
- `academic-researcher.md`

### Phase 2: Update concept.md
Replace inline YAML agent configs with:
```yaml
subagents:
  - role: market-researcher
    includes_from: templates/shared/agent-prompts/market-researcher.md
    # ... minimal overrides
```

### Phase 3: Consolidate Across Commands
Use same prompt files in:
- `/speckit.concept`
- `/speckit.games-concept`
- `/speckit.validate-concept`
- `/speckit.discover`
- Other commands needing market research

## Expected Savings

- **concept.md**: 8,000 tokens (agent prompt duplication)
- **concept.md**: 2,000 tokens (CQS formula duplication)
- **games-concept.md**: 3,000-4,000 tokens (game-specific agent consolidation)
- **design.md**: 4,000+ tokens (anti-patterns duplication)
- **Total Phase 1**: ~15,000 tokens saved immediately
- **Total Across All Commands**: ~30,000+ tokens

## Notes

- This template ensures all concept research agents follow consistent structure
- Reduces maintenance burden when updating agent instructions
- Enables prompt versioning (`market-researcher-v1.0.md`, `market-researcher-v1.1.md`)
- Easier to A/B test different agent prompts

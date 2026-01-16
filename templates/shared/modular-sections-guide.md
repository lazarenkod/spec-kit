# Modular Sections Guide for Concept

**Purpose**: Document 46 reusable concept sections and how to use include directives

**OPTIMIZATION v0.5.0**: Replace narrative prose descriptions with `<!-- @include -->` directives

## Overview

Instead of duplicating full section text in concept.md, use `<!-- @include -->` directives to load from modular files:

```markdown
<!-- @include templates/shared/concept-sections/market-framework.md -->
```

This reduces concept.md by **6,000+ tokens** while maintaining full content.

## Framework Sections (8 total)

### 1. Market Framework
- **File**: `templates/shared/concept-sections/market-framework.md`
- **Content**: Porter's 5 Forces, TAM/SAM/SOM analysis, Blue Ocean Canvas
- **Used in**: Phase 0b (Market Research)
- **Include**: 
  ```markdown
  ## § Market Dynamics
  <!-- @include templates/shared/concept-sections/market-framework.md -->
  ```

### 2. Competitive Analysis
- **File**: `templates/shared/concept-sections/competitive-analysis.md`
- **Content**: Competitor matrix, pricing analysis, ERRC Grid
- **Used in**: Phase 0b (Competitive Research)

### 3. Persona Framework
- **File**: `templates/shared/concept-sections/persona-framework.md`
- **Content**: JTBD synthesis, persona segmentation, WTP analysis
- **Used in**: Phase 0b (Persona Research)

### 4. Metrics Framework
- **File**: `templates/shared/concept-sections/metrics-framework.md`
- **Content**: SMART validation, North Star, leading indicators
- **Used in**: Phase 1 (Metrics Design)

### 5. Risk Framework
- **File**: `templates/shared/concept-sections/risk-framework.md`
- **Content**: Risk identification, impact/likelihood, mitigation strategies
- **Used in**: Phase 2 (Risk Assessment)

### 6. Technical Framework
- **File**: `templates/shared/concept-sections/technical-framework.md`
- **Content**: Architecture hints, tech stack, dependencies
- **Used in**: Phase 2 (Technical Discovery)

### 7. Strategic Positioning Framework
- **File**: `templates/shared/concept-sections/strategic-positioning.md`
- **Content**: Market position, differentiation, GTM strategy
- **Used in**: Phase 0c (Strategic Implications)

### 8. CQS Formula
- **File**: `templates/shared/cqs-formula.md`
- **Content**: 11-component quality scoring, evidence multiplier, quality gates
- **Used in**: Quality Validation (after research complete)

## Research Sections (5 total)

### 1. Research Orchestration
- **File**: `templates/shared/concept-sections/research-orchestration.md`
- **Content**: 4-agent parallel research, cross-validation, evidence registry
- **Used in**: Phase 0b (Multi-Agent Orchestration)

### 2. Research Actions (Market Intelligence)
- **File**: `templates/shared/concept-sections/research-actions-market.md`
- **Content**: WebSearch queries, competitor analysis, market trends
- **Used in**: Phase 0b (Market Research)

### 3. Research Actions (Competitive)
- **File**: `templates/shared/concept-sections/research-actions-competitive.md`
- **Content**: Competitor matrix, pricing, feature gaps
- **Used in**: Phase 0b (Competitive Research)

### 4. Research Actions (Personas)
- **File**: `templates/shared/concept-sections/research-actions-personas.md`
- **Content**: User pain points, buying behavior, WTP signals
- **Used in**: Phase 0b (Persona Research)

### 5. Evidence Registry
- **File**: `templates/shared/concept-sections/evidence-registry.md`
- **Content**: Evidence ID format (EV-001, EV-002), tier definitions, source tracking
- **Used in**: Phase 0b (Evidence Collection)

## Phase Sections (8 total)

### 1. Phase 0.5: Context Extraction
- **File**: `templates/shared/concept-sections/phase-0-5-context.md`
- **Content**: Classification agent, domain extraction, adaptive agent selection
- **Used in**: Phase 0.5 (Autonomous Context Extraction)

### 2. Phase 0a: Problem Statement
- **File**: `templates/shared/concept-sections/phase-0a-problem.md`
- **Content**: Problem validation, customer pain points, opportunity sizing
- **Used in**: Phase 0 (Discovery)

### 3. Phase 0b: Market & User Research
- **File**: `templates/shared/concept-sections/phase-0b-research.md`
- **Content**: Multi-agent orchestration, TAM analysis, persona synthesis
- **Used in**: Phase 0b (Research)

### 4. Phase 0b-2: Multi-Perspective Analysis
- **File**: `templates/shared/concept-sections/phase-0b-2-perspectives.md`
- **Content**: Alternative viewpoints, edge cases, devil's advocate
- **Used in**: Phase 0b-2 (Perspective Analysis)

### 5. Phase 0b-summary: Research Findings
- **File**: `templates/shared/concept-sections/phase-0b-summary.md`
- **Content**: Findings presentation, confidence assessment, recommendations
- **Used in**: Phase 0b-summary (Research Synthesis)

### 6. Phase 0c: Solution Ideation
- **File**: `templates/shared/concept-sections/phase-0c-ideation.md`
- **Content**: 5 alternative concepts, variant generation, positioning
- **Used in**: Phase 0c (Solution Ideation)

### 7. Phase 0c: Strategic Implications
- **File**: `templates/shared/concept-sections/phase-0c-strategic.md`
- **Content**: Constitution recommendations, quality implications
- **Used in**: Phase 0c (Strategic Implications)

### 8. Phase 1-3: Requirements Definition
- **File**: `templates/shared/concept-sections/phase-1-3-requirements.md`
- **Content**: Epic/Feature/Story hierarchy, priorities, user journey mapping
- **Used in**: Phase 1-3 (Requirements Generation)

## Alternative Variant Sections (10 total)

### 1-5. Variant Template (for each of 5 alternatives)
- **Files**: 
  - `templates/shared/concept-sections/variant-1-conservative.md`
  - `templates/shared/concept-sections/variant-2-balanced.md`
  - `templates/shared/concept-sections/variant-3-ambitious.md`
  - `templates/shared/concept-sections/variant-4-disruptive.md`
  - `templates/shared/concept-sections/variant-5-acquisition.md`
- **Content**: Problem statement, positioning, roadmap, risks
- **Used in**: Phase 0c-3 (Variant Generation & Scoring)

### 6-10. Game-Specific Variants (for /speckit.games-concept)
- **Files**:
  - `templates/shared/concept-sections/game-variant-sorting.md`
  - `templates/shared/concept-sections/game-variant-match3.md`
  - `templates/shared/concept-sections/game-variant-idle.md`
  - `templates/shared/concept-sections/game-variant-arcade.md`
  - `templates/shared/concept-sections/game-variant-puzzle.md`
- **Content**: Genre-specific mechanics, economy, progression
- **Used in**: /speckit.games-concept (Variant Generation)

## Quality & Validation Sections (6 total)

### 1. Quality Gates
- **File**: `templates/shared/concept-sections/quality-gates.md`
- **Content**: QG-001 to QG-012 definitions, severity, validation steps
- **Used in**: Validation phase (Quality Gate Enforcement)

### 2. CQS Score Output
- **File**: `templates/shared/concept-sections/cqs-score.md`
- **Content**: Component breakdown, evidence multiplier, improvement recommendations
- **Used in**: Quality Validation (Score Reporting)

### 3. Self-Review Checklist
- **File**: `templates/shared/concept-sections/self-review-checklist.md`
- **Content**: Hierarchy validation, persona check, metrics validation
- **Used in**: Phase 6 (Self-Review)

### 4. Handoff Checklist
- **File**: `templates/shared/concept-sections/handoff-checklist.md`
- **Content**: Pre-specification validation, completeness check, readiness gates
- **Used in**: Handoff to `/speckit.specify`

### 5. Compliance Check
- **File**: `templates/shared/concept-sections/compliance-check.md`
- **Content**: Standards research output, regulatory requirements
- **Used in**: Quality Validation (if domain-specific)

### 6. Evidence Validation
- **File**: `templates/shared/concept-sections/evidence-validation.md`
- **Content**: Source verification, tier assignment, confidence scoring
- **Used in**: Cross-validation (after research)

## Usage Patterns

### Pattern 1: Insert at Section Level
```markdown
## § Market Opportunity

<!-- @include templates/shared/concept-sections/market-framework.md -->
```

### Pattern 2: Insert with Override Variables
```markdown
## § Competitive Positioning

<!-- @include templates/shared/concept-sections/competitive-analysis.md
with_variants: true
competitor_count: 5
-->
```

### Pattern 3: Conditional Includes (Domain-Specific)
```markdown
## § Compliance Requirements

<!-- @include 
  templates/shared/concept-sections/compliance-check.md 
  IF domain IN ["fintech", "healthtech"]
-->
```

## Token Savings Calculation

**Current State** (inline sections):
- Each section: 100-600 words (300-1,800 tokens)
- 46 sections × avg 500 tokens = **23,000 tokens** in concept.md alone

**With Includes** (this optimization):
- Include directive: 3-5 words (5-10 tokens)
- External file loaded once per execution
- 46 sections × avg 8 tokens (include) = **368 tokens** in concept.md
- **Savings**: 23,000 - 368 = **22,632 tokens saved**

**Reality**:
- Not all 46 sections always used (typical: 15-20 sections per concept)
- Typical savings per concept: **6,000-8,000 tokens** (Phase 1 target)

## Implementation Steps

1. **Scan concept.md** for duplicated prose descriptions of frameworks
2. **Identify sections** that appear in multiple places or match modular files
3. **Replace** detailed prose with `<!-- @include -->` directives
4. **Test** that includes resolve correctly and content appears
5. **Verify** token count reduction (should see 6-8K reduction per concept)

## Future: Parameter Injection

Advanced pattern (future enhancement):

```markdown
## § Market Analysis

<!-- @include templates/shared/concept-sections/market-framework.md
  tam_estimate: "{{ TAM_ESTIMATE }}"
  growth_rate: "{{ GROWTH_RATE }}"
  competitive_intensity: "{{ COMPETITIVE_INTENSITY }}"
-->
```

This would allow parameterized sections for reuse across similar concepts.

## Files Not Included

These files are intentionally NOT included (too specific to concept.md):
- Feature Hierarchy (Epic/Feature/Story definitions - must be in concept)
- Ready-to-Execute Commands (user-specific - must be generated)
- Self-Review Output (must be generated fresh each run)
- Variants Summary (must compare actual generated alternatives)

---

**Reference**: `templates/commands/concept.md` Phases 0-1  
**Optimization**: v0.5.0 - Modular Section Includes  
**Token Savings**: ~6,000 tokens per concept execution

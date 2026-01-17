---
description: Re-validate an existing concept against current market conditions. Runs research agents to detect changes in market, competitors, and trends. Generates diff report and CQS delta. Use periodically (monthly/quarterly) to keep concept fresh.
persona: concept-validator
flags:
  - name: --thinking-depth
    type: choice
    choices: [minimal, quick, standard, thorough, deep, expert, ultrathink]
    default: standard
    description: |
      Thinking budget per agent (Category B - Core Workflow):
      - minimal: 8K budget, core agents, 45s (~$0.12)
      - quick: 16K budget, core agents, 60s (~$0.24)
      - standard: 32K budget, full workflow, 120s (~$0.48) [RECOMMENDED]
      - thorough: 48K budget, extended validation, 180s (~$0.72)
      - deep: 80K budget, deep analysis, 300s (~$1.20)
      - expert: 120K budget, expert review, 480s (~$1.80)
      - ultrathink: 200K budget, comprehensive validation, 720s (~$3.00)
handoffs:
  - label: Update Concept
    agent: speckit.concept
    prompt: Incorporate validation findings into concept.md
    auto: false
    condition:
      - "Validation found significant changes (HIGH impact)"
      - "CQS delta > -10 points"
  - label: View Full Report
    agent: none
    prompt: Review the detailed validation report
    auto: true
    condition:
      - "Validation completed successfully"
claude_code:
  model: sonnet
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        minimal: 2000      # 25% of 8K
        quick: 4000        # 25% of 16K
        standard: 8000     # 25% of 32K
        thorough: 12000    # 25% of 48K
        deep: 26400        # 33% of 80K
        expert: 39600      # 33% of 120K
        ultrathink: 66000  # 33% of 200K
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
        timeout_minutes: 10
        retry_on_failure: 1
      pro:
        minimal: 4000      # 50% of 8K
        quick: 8000        # 50% of 16K
        standard: 21440    # 67% of 32K
        thorough: 32160    # 67% of 48K
        deep: 60000        # 75% of 80K
        expert: 99600      # 83% of 120K
        ultrathink: 160000 # 80% of 200K
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
        timeout_minutes: 15
        retry_on_failure: 2
      max:
        minimal: 8000      # 100%
        quick: 16000       # 100%
        standard: 32000    # 100%
        thorough: 48000    # 100%
        deep: 80000        # 100%
        expert: 120000     # 100%
        ultrathink: 200000 # 100%
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
        timeout_minutes: 30
        retry_on_failure: 3
  depth_defaults:
    minimal:
      thinking_budget: 8000
      skip_agents: [optional-validators, alternative-analyzer]
      timeout: 45
    quick:
      thinking_budget: 16000
      skip_agents: [optional-validators]
      timeout: 60
    standard:
      thinking_budget: 32000
      skip_agents: []
      timeout: 120
    thorough:
      thinking_budget: 48000
      additional_agents: [deep-analyzers]
      timeout: 180
    deep:
      thinking_budget: 80000
      additional_agents: [deep-analyzers, edge-case-analyzer]
      timeout: 300
    expert:
      thinking_budget: 120000
      additional_agents: [deep-analyzers, edge-case-analyzer, security-auditor]
      timeout: 480
    ultrathink:
      thinking_budget: 200000
      additional_agents: [deep-analyzers, edge-case-analyzer, security-auditor, performance-auditor]
      timeout: 720
  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier == 'free' AND requested_depth IN ['deep', 'expert', 'ultrathink']"
        fallback_depth: "thorough"
        fallback_thinking: 12000
        warning_message: |
          ⚠️ **Deep/Expert/Ultrathink modes require Pro or Max tier**.
          Auto-downgrading to **Thorough** mode (12K budget on Free tier).
      - condition: "user_tier == 'pro' AND requested_depth == 'ultrathink'"
        fallback_depth: "expert"
        fallback_thinking: 99600
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (200K thinking budget).
          Auto-downgrading to **Expert** mode (99.6K budget on Pro tier).
      - condition: "user_tier == 'pro' AND requested_depth == 'expert'"
        fallback_depth: "expert"
        fallback_thinking: 99600
        warning_message: |
          ℹ️ **Expert mode on Pro tier** (99.6K budget, 83% of full 120K).
      - condition: "user_tier == 'free' AND requested_depth == 'thorough'"
        fallback_depth: "thorough"
        fallback_thinking: 12000
        warning_message: |
          ℹ️ **Thorough mode on Free tier** (12K budget, 25% of full 48K).
  cost_breakdown:
    minimal: {cost: $0.12, time: "45-60s"}
    quick: {cost: $0.24, time: "60-90s"}
    standard: {cost: $0.48, time: "120-180s"}
    thorough: {cost: $0.72, time: "180-240s"}
    deep: {cost: $1.20, time: "300-360s"}
    expert: {cost: $1.80, time: "480-540s"}
    ultrathink: {cost: $3.00, time: "720-900s"}
  cache_hierarchy: full
  orchestration:
    max_parallel: 6
    timeout_minutes: 30
  subagents:
    - role: market-validator
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 9
      trigger: "when re-validating market sizing and trends"
      prompt: |
        Compare current market data with existing concept.md:
        1. Re-calculate TAM/SAM/SOM with fresh sources
        2. Identify new growth signals or slowdowns
        3. Check regulatory changes
        Output: market_delta_report

    - role: competitive-validator
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 9
      trigger: "when monitoring competitive landscape changes"
      prompt: |
        Detect competitor changes since last validation:
        1. New entrants in the space
        2. Pricing changes from existing competitors
        3. Feature announcements / roadmap shifts
        4. Funding events or acquisitions
        Output: competitive_delta_report

    - role: trend-validator
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 9
      trigger: "when validating trend assumptions"
      prompt: |
        Validate trend assumptions from concept.md:
        1. Check if enabling trends are still valid
        2. Identify new emerging trends
        3. Assess timing window changes
        Output: trend_delta_report

    - role: synthesis-agent
      role_group: SYNTHESIS
      parallel: false
      depends_on: [market-validator, competitive-validator, trend-validator]
      priority: 10
      trigger: "when synthesizing all validation reports"
      prompt: |
        Synthesize validation findings:
        1. Calculate overall CQS delta
        2. Generate unified diff report
        3. Recommend actions based on impact severity
        Output: validation_synthesis
flags:
  max_model: "--max-model <opus|sonnet|haiku>"  # Override model cap
---

# `/speckit.validate-concept` — Continuous Concept Validation

## Purpose

Re-validate an existing concept against current market conditions to:
- Detect market shifts that may invalidate assumptions
- Monitor competitive landscape changes
- Update evidence freshness scores
- Track CQS drift over time

## When to Use

| Scenario | Frequency | Trigger |
|----------|-----------|---------|
| Active development | Monthly | Before each major release |
| Paused project | Quarterly | Before resuming work |
| Market volatility | Weekly | News of competitor moves |
| Investor update | On-demand | Before fundraising |

---

## User Input

```markdown
## Validation Request

**Concept to validate**: [path to concept.md, default: .spec/concept.md]

**Focus areas** (optional):
- [ ] Market sizing (TAM/SAM/SOM)
- [ ] Competitive landscape
- [ ] Trend analysis
- [ ] All of the above (default)

**Last validation date**: [date from concept.md metadata, or "Never"]

**Specific concerns** (optional):
[Any specific areas to investigate, e.g., "Competitor X announced new feature"]
```

---

## Outline

### Phase 1: Load Existing Concept (1-2 min)

1. **Read current concept.md**:
   - Extract TAM/SAM/SOM values
   - Extract competitor list and positioning
   - Extract trend assumptions
   - Extract CQS score and evidence registry

2. **Identify validation baseline**:
   - Last validation date
   - Evidence age (calculate staleness)
   - Key assumptions to re-test

### Phase 2: Parallel Re-Validation (10-15 min)

Launch 3 research agents in parallel:

#### Market Validator

```yaml
market_validator:
  inputs:
    - existing_tam: from concept.md
    - existing_sam: from concept.md
    - existing_som: from concept.md
  tasks:
    - Re-calculate TAM with fresh 2025 sources
    - Check for market growth/decline signals
    - Identify regulatory changes
  outputs:
    - new_tam: calculated value
    - tam_delta: percentage change
    - new_sources: [list of fresh sources]
    - market_alerts: [significant changes]
```

#### Competitive Validator

```yaml
competitive_validator:
  inputs:
    - existing_competitors: from concept.md
    - existing_positioning: from concept.md
  tasks:
    - Search for new entrants
    - Check pricing changes
    - Monitor feature announcements
    - Track funding/M&A events
  outputs:
    - new_competitors: [list]
    - pricing_changes: [list]
    - feature_announcements: [list]
    - competitive_alerts: [significant changes]
```

#### Trend Validator

```yaml
trend_validator:
  inputs:
    - existing_trends: from concept.md
    - timing_assumptions: from concept.md
  tasks:
    - Validate enabling trends still active
    - Identify new emerging trends
    - Assess timing window changes
  outputs:
    - trend_status: [validated/invalidated]
    - new_trends: [list]
    - timing_assessment: [on_track/accelerated/delayed]
    - trend_alerts: [significant changes]
```

### Phase 3: Synthesis & Diff Generation (3-5 min)

1. **Calculate CQS Delta**:
   ```
   CQS_delta = CQS_new - CQS_original

   Impact Classification:
   - CRITICAL: delta < -20 points
   - HIGH: delta < -10 points
   - MEDIUM: delta < -5 points
   - LOW: delta >= -5 points
   ```

2. **Generate Diff Report**:
   ```markdown
   ## Validation Diff Report

   ### Summary
   | Metric | Original | Current | Delta | Impact |
   |--------|:--------:|:-------:|:-----:|:------:|
   | TAM | $50B | $55B | +10% | LOW |
   | Competitors | 5 | 7 | +2 | MEDIUM |
   | CQS | 82 | 78 | -4 | LOW |

   ### Detailed Changes
   [Per-category breakdown]
   ```

3. **Generate Recommendations**:
   - If CRITICAL: "Stop and re-validate concept"
   - If HIGH: "Update affected sections before proceeding"
   - If MEDIUM: "Note changes, continue with caution"
   - If LOW: "Concept remains valid"

### Phase 4: Output Generation

Create `concept-validation-{date}.md`:

```markdown
# Concept Validation Report

**Validated**: {date}
**Original Concept**: {concept_date}
**Days Since Creation**: {days}

## Executive Summary

**Validation Status**: [VALID / NEEDS_UPDATE / INVALID]
**CQS Delta**: {delta} points ({impact} impact)
**Recommendation**: {action}

## Market Changes

### TAM/SAM/SOM Delta
| Metric | Original | Current | Delta | Sources |
|--------|:--------:|:-------:|:-----:|---------|
| TAM | {old} | {new} | {%} | [links] |
| SAM | {old} | {new} | {%} | [links] |
| SOM | {old} | {new} | {%} | [links] |

### New Market Signals
- {signal_1}
- {signal_2}

## Competitive Changes

### New Entrants
| Competitor | Type | Threat Level | Notes |
|------------|------|:------------:|-------|
| {name} | {direct/indirect} | {H/M/L} | {notes} |

### Pricing Changes
| Competitor | Old Price | New Price | Impact |
|------------|:---------:|:---------:|:------:|
| {name} | {old} | {new} | {impact} |

### Feature Announcements
- {competitor}: {announcement} ({date})

## Trend Changes

### Validated Trends
- ✅ {trend_1}: Still active
- ⚠️ {trend_2}: Weakening
- ❌ {trend_3}: No longer relevant

### New Trends
- {new_trend_1}: {impact}

### Timing Assessment
- Original window: {original}
- Current assessment: {current}
- Status: [ON_TRACK / ACCELERATED / DELAYED]

## Evidence Freshness

| Component | Avg Evidence Age | Freshness Score |
|-----------|:----------------:|:---------------:|
| Market | {days} days | {score}/100 |
| Competitive | {days} days | {score}/100 |
| Personas | {days} days | {score}/100 |
| Trends | {days} days | {score}/100 |

## Recommended Actions

### Immediate (if CRITICAL/HIGH)
1. {action_1}
2. {action_2}

### Before Next Sprint (if MEDIUM)
1. {action_1}

### Monitor (if LOW)
- {item_to_watch}

## Validation History

| Date | CQS | Delta | Status | Key Changes |
|------|:---:|:-----:|:------:|-------------|
| {date_1} | {cqs} | — | Initial | — |
| {date_2} | {cqs} | {delta} | {status} | {changes} |
| {today} | {cqs} | {delta} | {status} | {changes} |
```

---

## Self-Review Criteria

Before completing validation, verify:

| ID | Criterion | Check | Severity |
|----|-----------|-------|----------|
| SR-VAL-01 | All validators completed | 3/3 agents returned | CRITICAL |
| SR-VAL-02 | Fresh sources used | Evidence <30 days old | HIGH |
| SR-VAL-03 | Diff calculated | CQS delta computed | HIGH |
| SR-VAL-04 | Recommendations provided | Actions listed per impact | MEDIUM |
| SR-VAL-05 | History updated | Validation logged | MEDIUM |

---

## Integration with Workflow

```
                    ┌─────────────────────┐
                    │  /speckit.concept   │
                    │  (Initial creation) │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Development      │
                    │    (Weeks/Months)   │
                    └──────────┬──────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────┐
│                /speckit.validate-concept                  │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ Market   │  │Competit. │  │  Trend   │               │
│  │ Validator│  │ Validator│  │ Validator│               │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘               │
│       └─────────────┼─────────────┘                     │
│                     ▼                                    │
│              ┌────────────┐                             │
│              │ Synthesis  │                             │
│              └──────┬─────┘                             │
│                     │                                    │
│         ┌───────────┴───────────┐                       │
│         ▼                       ▼                       │
│   concept-validation-     [Update concept.md           │
│   {date}.md               if needed]                   │
└──────────────────────────────────────────────────────────┘
```

---

## Cost Estimation

| Agent | Model | Avg Tokens | Est. Cost |
|-------|-------|:----------:|:---------:|
| market-validator | sonnet-4.5 | 10,000 | $0.10 |
| competitive-validator | sonnet-4.5 | 8,000 | $0.08 |
| trend-validator | sonnet-4.5 | 6,000 | $0.06 |
| synthesis-agent | sonnet-4.5 | 5,000 | $0.05 |
| **Total per validation** | | | **~$0.30-0.40** |

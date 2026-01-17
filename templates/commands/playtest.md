---
name: playtest
description: |
  Structured playtesting workflow for mobile games.
  Manages internal, external, and friends-family playtests with standardized metrics collection,
  session recording, and actionable insights generation.

version: 1.0.0
persona: ux-researcher-agent
model: opus
thinking_budget: 24000

skills:
  - user-research
  - session-analysis
  - metrics-collection
  - qualitative-synthesis

flags:
  - name: --thinking-depth
    type: choice
    choices: [quick, standard, thorough, deep, expert, ultrathink]
    default: standard
    description: |
      Research depth and thinking budget per agent:
      - quick: 16K budget, 5 core agents, 90s timeout (~$0.32)
      - standard: 32K budget, 9 agents, 180s timeout (~$1.15) [RECOMMENDED]
      - thorough: 64K budget, 12 agents, 240s timeout (~$2.30)
      - deep: 96K budget, 15 agents, 300s timeout (~$3.46)
      - expert: 120K budget, 18 agents, 360s timeout (~$4.32)
      - ultrathink: 192K budget, 18 agents, 480s timeout (~$6.91) [EXPERT MODE]
  - name: --max-model
    type: string
    default: null
    description: "--max-model <opus|sonnet|haiku> - Override model cap"

inputs:
  playtest_type:
    type: enum
    options: [internal, friends_family, closed_beta, open_beta, focus_group]
    required: true
    description: Type of playtest session
  build_version:
    type: string
    required: true
    description: Game build version being tested
  target_participants:
    type: integer
    default: 10
    description: Number of participants to recruit
  focus_areas:
    type: array
    items: [ftue, core_loop, monetization, ux, difficulty, retention, social]
    default: [ftue, core_loop]
    description: Specific areas to focus testing on

outputs:
  - docs/playtest/playtest-plan.md                    # Test plan
  - docs/playtest/sessions/session-{{N}}.md           # Individual session notes
  - docs/playtest/playtest-report.md                  # Aggregated report
  - docs/playtest/metrics.json                        # Quantitative metrics
  - docs/playtest/action-items.md                     # Prioritized action items
  - docs/playtest/clips/                              # Session recording clips (references)

quality_gates:
  - name: QG-PLAYTEST-001
    description: Minimum Sample Size
    condition: "participants >= 5 for internal, >= 10 for external"
    threshold: "≥ minimum for playtest type"
    severity: HIGH
  - name: QG-PLAYTEST-002
    description: NPS Score
    condition: "Net Promoter Score calculated and reported"
    threshold: "NPS measured"
    severity: MEDIUM
  - name: QG-PLAYTEST-003
    description: Critical Issues Identified
    condition: "No P0 blockers remain unaddressed"
    threshold: "0 unresolved P0s"
    severity: CRITICAL
  - name: QG-PLAYTEST-004
    description: Comprehension Rate
    condition: "FTUE comprehension >= 80%"
    threshold: "≥ 80% understand core mechanics"
    severity: HIGH

pre_gates:
  - name: QG-PLAYTEST-000
    description: Playable build exists
    condition: "Build version {{build_version}} is deployable"
    severity: CRITICAL

inline_gates:
  enabled: true
  gates:
    - id: IG-PLAYTEST-001
      name: Session Recording
      check: "All sessions have recording consent and are captured"
      severity: MEDIUM
    - id: IG-PLAYTEST-002
      name: Demographic Coverage
      check: "Participants match target audience demographics"
      severity: HIGH
    - id: IG-PLAYTEST-003
      name: Task Completion Tracking
      check: "All focus area tasks have completion rates"
      severity: HIGH

handoffs:
  - label: Update GDD
    agent: speckit.gdd
    auto: false
    condition:
      - "Critical UX issues found"
      - "Core loop changes recommended"
    prompt: "Update GDD sections based on playtest findings"
  - label: Create Bug Tasks
    agent: speckit.tasks
    auto: true
    condition:
      - "P0 or P1 bugs identified"
    gates:
      - name: "QG-PLAYTEST-003"
        check: "All P0 blockers have tasks"
  - label: Iterate Design
    agent: speckit.specify
    auto: false
    condition:
      - "Major design changes recommended"
  - label: Next Playtest
    agent: speckit.playtest
    auto: false
    condition:
      - "Iteration complete"
      - "New build ready"

claude_code:
  model: opus
  reasoning_mode: extended
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 4000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
        timeout_per_agent: 180000
        retry_on_failure: 1
      pro:
        thinking_budget: 8000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
        timeout_per_agent: 300000
        retry_on_failure: 2
      max:
        thinking_budget: 32000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
        timeout_per_agent: 900000
        retry_on_failure: 3
      ultrathink:
        thinking_budget: 96000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 6.0
  depth_defaults:
    quick:
      thinking_budget: 16000
      skip_agents: [optional-synthesizers]
      timeout: 90
    standard:
      thinking_budget: 32000
      skip_agents: []
      timeout: 180
    ultrathink:
      thinking_budget: 96000
      additional_agents: [deep-session-analyzer, pattern-detector]
      timeout: 300
  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 32000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (96K thinking budget).
          Auto-downgrading to **Standard** mode (32K budget).
  cost_breakdown:
    quick: {cost: $0.12, time: "90-120s"}
    standard: {cost: $0.24, time: "180-240s"}
    ultrathink: {cost: $0.72, time: "300-360s"}
  cache_control:
    system_prompt: ephemeral
    constitution: ephemeral
    templates: ephemeral
    artifacts: ephemeral
    ttl: session
  cache_hierarchy: full
  orchestration:
    max_parallel: 5
    conflict_resolution: queue
    timeout_per_agent: 600000
    retry_on_failure: 2
  operation_batching:
    enabled: true
    skip_flag: "--sequential"
    framework: templates/shared/operation-batching.md

  subagents:
    # Wave 1: Planning (parallel)
    - role: playtest-planner
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: opus
      prompt: |
        Create comprehensive playtest plan (docs/playtest/playtest-plan.md).

        Based on inputs (playtest_type, focus_areas, target_participants):

        1. **Objectives Definition**:
           - Primary objectives (2-3 key questions to answer)
           - Secondary objectives (nice-to-have insights)
           - Success criteria with measurable thresholds

        2. **Participant Recruitment**:
           - Screening criteria (match target audience)
           - Recruitment channels per playtest type:
             - Internal: Slack, team members
             - Friends & Family: Personal networks
             - Closed Beta: Discord, early access signups
             - Open Beta: App Store TestFlight, Google Play Beta

        3. **Session Structure**:
           - Pre-session: Consent, demographics survey
           - Play session: Structured tasks + free play
           - Post-session: Interview questions, NPS survey

        4. **Focus Area Tasks**:
           FOR EACH focus_area in inputs:
             - Define 3-5 specific tasks to observe
             - Set completion criteria
             - Define success metrics

        5. **Metrics Collection**:
           - Quantitative: Task completion rates, time-to-complete, errors
           - Qualitative: Think-aloud observations, emotional reactions
           - Surveys: NPS, CSAT, comprehension check

        6. **Logistics**:
           - Session duration (30-60 min recommended)
           - Recording setup (screen + face + audio)
           - Incentives (if applicable)

        Reference: Nielsen's 5-user rule for usability, 10-15 for quant insights

        Output: docs/playtest/playtest-plan.md

    - role: survey-designer
      role_group: RESEARCH
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Create playtest surveys and interview guides.

        Generate artifacts:

        1. **Pre-Session Survey** (docs/playtest/templates/pre-survey.md):
           - Demographics (age, gender, region)
           - Gaming habits (hours/week, favorite genres)
           - Mobile game experience
           - Familiarity with game type

        2. **Post-Session Survey** (docs/playtest/templates/post-survey.md):
           - NPS question (0-10 recommend)
           - Comprehension check (what was the goal?)
           - Difficulty rating (1-5 scale)
           - Enjoyment rating (1-5 scale)
           - Open-ended: Best part? Worst part?
           - Would you play again? (Yes/No/Maybe)

        3. **Interview Guide** (docs/playtest/templates/interview-guide.md):
           - Opening: "Tell me about your experience"
           - Probing: "What did you think when X happened?"
           - Pain points: "What frustrated you?"
           - Suggestions: "What would make it better?"
           - Closing: "Anything else?"

        4. **Observation Checklist** (docs/playtest/templates/observation-checklist.md):
           - FTUE completion steps
           - First error occurrence
           - Confusion indicators (pause, repeated taps, wrong path)
           - Emotional reactions (frustration, delight, boredom)
           - Session end behavior (quit voluntarily, asked to continue)

    # Wave 2: Session Execution (sequential per session)
    - role: session-facilitator
      role_group: RESEARCH
      parallel: false
      depends_on: [playtest-planner, survey-designer]
      priority: 20
      model_override: sonnet
      prompt: |
        Guide playtest session execution and note-taking.

        For EACH session:

        1. **Pre-Session Setup**:
           - Verify recording is working
           - Confirm participant consent
           - Administer pre-survey
           - Brief participant (think-aloud protocol)

        2. **During Session**:
           - Timestamp key events
           - Note think-aloud comments verbatim
           - Track task completion (pass/fail/partial)
           - Mark confusion points
           - Note emotional reactions

        3. **Post-Session**:
           - Administer post-survey
           - Conduct interview (5-10 min)
           - Thank participant
           - Export recording

        4. **Session Documentation**:
           Create docs/playtest/sessions/session-{{N}}.md with:
           - Participant ID (anonymized)
           - Demographics summary
           - Task completion table
           - Key observations (timestamped)
           - Verbatim quotes (3-5 best)
           - NPS score
           - Severity ratings for issues found

        Template for session notes provided in next section.

    # Wave 3: Analysis (parallel after all sessions)
    - role: metrics-analyst
      role_group: ANALYSIS
      parallel: true
      depends_on: [session-facilitator]
      priority: 30
      model_override: opus
      prompt: |
        Aggregate and analyze quantitative playtest metrics.

        Generate docs/playtest/metrics.json and metrics section of report.

        1. **Task Completion Metrics**:
           FOR EACH focus_area:
             - Calculate completion rate (% passed)
             - Calculate average time-to-complete
             - Identify failure patterns

        2. **NPS Calculation**:
           - Promoters (9-10): count
           - Passives (7-8): count
           - Detractors (0-6): count
           - NPS = % Promoters - % Detractors

        3. **Comprehension Analysis**:
           - % correctly identified game goal
           - % understood core mechanic
           - % knew how to progress

        4. **Engagement Signals**:
           - Average session length
           - % asked to continue after allotted time
           - % expressed desire to play again

        5. **Issue Severity Distribution**:
           - P0 (Blocker): count
           - P1 (Major): count
           - P2 (Minor): count
           - P3 (Polish): count

        6. **Statistical Confidence**:
           - Sample size: N
           - Confidence level for each metric
           - Note if N too small for significance

        Output: docs/playtest/metrics.json

    - role: qualitative-synthesizer
      role_group: ANALYSIS
      parallel: true
      depends_on: [session-facilitator]
      priority: 30
      model_override: opus
      prompt: |
        Synthesize qualitative insights from playtest sessions.

        Analyze all session notes and generate:

        1. **Theme Extraction**:
           - Group similar observations into themes
           - Rank themes by frequency (mentioned by N participants)
           - Identify consensus vs outlier opinions

        2. **Pain Point Prioritization**:
           | Pain Point | Frequency | Severity | Impact | Priority |
           |------------|-----------|----------|--------|----------|
           | [Issue] | N/{{total}} | P0-P3 | High/Med/Low | 1-N |

        3. **Verbatim Quote Collection**:
           - Best 10-15 quotes representing key insights
           - Attribute to participant ID (anonymized)
           - Tag by theme/issue

        4. **Behavioral Patterns**:
           - Common successful strategies
           - Common failure patterns
           - Unexpected player behaviors

        5. **Emotional Journey Map**:
           ```
           Session Timeline → [Start] --- [Mid] --- [End]
           Emotional State  →  😐  →  😊  →  😤  →  😊
           ```

        6. **Comparative Analysis** (if multiple playtest rounds):
           - What improved since last round?
           - What regressed?
           - New issues introduced?

    # Wave 4: Reporting (depends on analysis)
    - role: report-generator
      role_group: REPORTING
      parallel: true
      depends_on: [metrics-analyst, qualitative-synthesizer]
      priority: 40
      model_override: opus
      prompt: |
        Generate comprehensive playtest report (docs/playtest/playtest-report.md).

        Structure:

        ## Executive Summary
        - Build version tested
        - Participants: N
        - NPS: X
        - Top 3 insights
        - GO / NO-GO recommendation

        ## Methodology
        - Playtest type
        - Recruitment criteria
        - Session structure
        - Metrics collected

        ## Quantitative Results
        - Task completion rates (by focus area)
        - NPS breakdown
        - Comprehension scores
        - Issue distribution

        ## Qualitative Insights
        - Top themes with evidence
        - Pain point analysis
        - Verbatim quotes

        ## Issue Log
        | ID | Description | Severity | Frequency | Recommendation |
        |----|-------------|----------|-----------|----------------|

        ## Recommendations
        ### P0: Fix Before Launch
        ### P1: Fix in Next Sprint
        ### P2: Backlog
        ### P3: Nice to Have

        ## Next Steps
        - Recommended changes
        - Next playtest scope
        - Timeline

        ## Appendix
        - Session summaries
        - Raw data references
        - Recording links

    - role: action-item-generator
      role_group: REPORTING
      parallel: true
      depends_on: [metrics-analyst, qualitative-synthesizer]
      priority: 40
      model_override: sonnet
      prompt: |
        Generate prioritized action items (docs/playtest/action-items.md).

        Create actionable tasks from playtest findings:

        ## P0: Blockers (Fix Immediately)
        - [ ] TASK-{{N}}: [Issue] - [Recommendation]
          - Evidence: [Quote/Metric]
          - Affected: N participants
          - Owner: [Suggested owner]

        ## P1: Major Issues (Fix Before Soft Launch)
        - [ ] TASK-{{N}}: [Issue] - [Recommendation]

        ## P2: Minor Issues (Fix Before Global)
        - [ ] TASK-{{N}}: [Issue] - [Recommendation]

        ## P3: Polish (Post-Launch)
        - [ ] TASK-{{N}}: [Issue] - [Recommendation]

        ## Design Reconsiderations
        - [ ] Review [Feature] based on feedback
        - [ ] A/B test [Element]

        ## Next Playtest Recommendations
        - Scope: [What to test next]
        - Target N: [Sample size]
        - When: [After which fixes]

        Ensure traceability:
        - Link tasks to spec requirements (FR-xxx, AS-xxx) if applicable
        - Tag with focus area (FTUE, core_loop, etc.)

flags:
  plan_only: "--plan-only"                       # Generate plan without executing
  analyze: "--analyze <session-dir>"             # Analyze existing sessions
  compare: "--compare <previous-report>"         # Compare to previous playtest
  export_jira: "--export-jira"                   # Export issues to JIRA format
  export_linear: "--export-linear"               # Export issues to Linear format
  skip_recording: "--skip-recording"             # Skip recording requirements
  max_model: "--max-model <opus|sonnet|haiku>"   # Override model cap
---

# /speckit.playtest - Playtesting Workflow

## Purpose

The `/speckit.playtest` command provides a structured framework for conducting, analyzing, and acting on playtest sessions. It ensures:

1. **Consistent methodology** across all playtest rounds
2. **Comprehensive metrics collection** (NPS, comprehension, engagement)
3. **Actionable insights** with prioritized recommendations
4. **Traceability** from findings to fixes

## When to Use

- **Pre-Alpha**: Internal team playtest for core loop validation
- **Alpha**: Friends & family playtest for initial feedback
- **Beta**: Closed/open beta for scaled testing
- **Pre-Launch**: Focus group testing for final polish
- **Post-Launch**: Ongoing playtests for new features

## Playtest Types

| Type | Participants | Purpose | Duration |
|------|--------------|---------|----------|
| **Internal** | 5-10 (team) | Find obvious issues | 30 min |
| **Friends & Family** | 10-20 | Honest feedback | 45 min |
| **Closed Beta** | 50-500 | Scale testing | Ongoing |
| **Open Beta** | 1000+ | Stress test, metrics | Ongoing |
| **Focus Group** | 6-12 | Deep qualitative | 60-90 min |

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      /speckit.playtest                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WAVE 1: Planning (parallel)                                    │
│  ├── Playtest Planner → playtest-plan.md                        │
│  └── Survey Designer → templates/*.md                           │
│                                                                  │
│  WAVE 2: Execution (sequential per session)                     │
│  └── Session Facilitator → sessions/session-N.md                │
│                                                                  │
│  WAVE 3: Analysis (parallel)                                    │
│  ├── Metrics Analyst → metrics.json                             │
│  └── Qualitative Synthesizer → themes, quotes                   │
│                                                                  │
│  WAVE 4: Reporting (parallel)                                   │
│  ├── Report Generator → playtest-report.md                      │
│  └── Action Item Generator → action-items.md                    │
│                                                                  │
│  HANDOFFS:                                                      │
│  ├── P0/P1 issues → /speckit.tasks                              │
│  ├── UX changes → /speckit.gdd                                  │
│  └── Next round → /speckit.playtest                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Execution Steps

### Step 1: Generate Playtest Plan

```text
INPUT: playtest_type, build_version, target_participants, focus_areas

CREATE docs/playtest/playtest-plan.md:
  - Objectives (primary, secondary)
  - Participant criteria
  - Session structure
  - Focus area tasks
  - Metrics to collect
  - Logistics (duration, recording, incentives)
```

### Step 2: Create Survey & Interview Templates

```text
CREATE docs/playtest/templates/:
  - pre-survey.md (demographics, gaming habits)
  - post-survey.md (NPS, ratings, open-ended)
  - interview-guide.md (probing questions)
  - observation-checklist.md (what to watch for)
```

### Step 3: Execute Sessions

```text
FOR EACH participant:
  1. Pre-session setup
  2. Administer pre-survey
  3. Play session with observation
  4. Administer post-survey
  5. Conduct interview
  6. Document in sessions/session-N.md
```

### Step 4: Analyze Results

```text
PARALLEL:
  - Aggregate quantitative metrics → metrics.json
  - Synthesize qualitative themes
  - Extract key quotes
  - Calculate NPS
```

### Step 5: Generate Reports

```text
PARALLEL:
  - Create playtest-report.md (full report)
  - Create action-items.md (prioritized tasks)
```

## Key Metrics

### Net Promoter Score (NPS)

**Question**: "On a scale of 0-10, how likely are you to recommend this game to a friend?"

```
NPS = % Promoters (9-10) - % Detractors (0-6)
```

| NPS Range | Interpretation |
|-----------|----------------|
| 50+ | Excellent |
| 30-50 | Good |
| 0-30 | Needs improvement |
| <0 | Critical issues |

**Industry Benchmarks**:
- Supercell games: NPS 60-70
- Top 100 mobile games: NPS 30-50
- Average mobile game: NPS 10-20

### Comprehension Rate

**Question**: "In your own words, what is the goal of this game?"

```
Comprehension = % participants who correctly identify core goal
```

| Rate | Interpretation |
|------|----------------|
| 90%+ | Excellent FTUE |
| 80-90% | Good, minor tweaks |
| 60-80% | FTUE needs work |
| <60% | Major FTUE overhaul |

### Task Completion Rate

```
Completion Rate = (Successful completions / Total attempts) × 100
```

Track per focus area:
- FTUE: Complete tutorial steps
- Core Loop: Complete 3 rounds
- Monetization: Navigate to shop
- Social: Add a friend

### Engagement Signals

| Signal | Positive | Negative |
|--------|----------|----------|
| Session length | Extended play | Early quit |
| Return intent | "When can I play again?" | "I've seen enough" |
| Exploration | Discovered hidden features | Stuck on main path |
| Emotional | Laughed, cheered | Sighed, complained |

## Session Note Template

```markdown
# Session {{N}}: {{PARTICIPANT_ID}}

## Metadata

| Field | Value |
|-------|-------|
| Date | {{DATE}} |
| Duration | {{DURATION}} min |
| Build | {{BUILD_VERSION}} |
| Playtest Type | {{TYPE}} |

## Participant Profile

- **Age**: {{AGE_RANGE}}
- **Gender**: {{GENDER}}
- **Gaming Experience**: {{EXPERIENCE}}
- **Device**: {{DEVICE}}

## Task Completion

| Task | Status | Time | Notes |
|------|--------|------|-------|
| Complete FTUE | ✅/❌/⚠️ | Xs | |
| Win first match | ✅/❌/⚠️ | Xs | |
| Navigate to shop | ✅/❌/⚠️ | Xs | |
| Understand progression | ✅/❌/⚠️ | Xs | |

## Key Observations

### [HH:MM:SS] {{EVENT_TITLE}}
- **Observation**: {{WHAT_HAPPENED}}
- **Reaction**: {{PARTICIPANT_REACTION}}
- **Severity**: P0/P1/P2/P3

### [HH:MM:SS] {{EVENT_TITLE}}
...

## Verbatim Quotes

> "{{QUOTE_1}}" ({{CONTEXT}})

> "{{QUOTE_2}}" ({{CONTEXT}})

## Survey Results

- **NPS**: {{SCORE}}/10
- **Difficulty**: {{SCORE}}/5
- **Enjoyment**: {{SCORE}}/5
- **Would Play Again**: Yes/No/Maybe

## Interview Highlights

**Best Part**: {{RESPONSE}}

**Worst Part**: {{RESPONSE}}

**Suggestions**: {{RESPONSE}}

## Issues Found

| ID | Description | Severity | Timestamp |
|----|-------------|----------|-----------|
| ISSUE-1 | | P0/P1/P2/P3 | HH:MM:SS |
| ISSUE-2 | | P0/P1/P2/P3 | HH:MM:SS |

## Session Recording

- **File**: {{RECORDING_PATH}}
- **Key Clips**:
  - [HH:MM:SS - HH:MM:SS]: {{DESCRIPTION}}
  - [HH:MM:SS - HH:MM:SS]: {{DESCRIPTION}}
```

## Playtest Report Template

```markdown
# Playtest Report: {{BUILD_VERSION}}

**Report Date**: {{DATE}}
**Playtest Type**: {{TYPE}}
**Participants**: {{N}}

---

## Executive Summary

### Key Findings

1. **{{FINDING_1}}**: {{DESCRIPTION}}
2. **{{FINDING_2}}**: {{DESCRIPTION}}
3. **{{FINDING_3}}**: {{DESCRIPTION}}

### Metrics Snapshot

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| NPS | {{NPS}} | ≥30 | ✅/⚠️/❌ |
| FTUE Completion | {{%}}% | ≥90% | ✅/⚠️/❌ |
| Core Loop Comprehension | {{%}}% | ≥80% | ✅/⚠️/❌ |
| Would Play Again | {{%}}% | ≥70% | ✅/⚠️/❌ |

### Recommendation

**{{GO / NO-GO / ITERATE}}**: {{RATIONALE}}

---

## Detailed Results

### NPS Analysis

```
Promoters (9-10): {{N}} ({{%}}%)
Passives (7-8):   {{N}} ({{%}}%)
Detractors (0-6): {{N}} ({{%}}%)
═══════════════════════════════
NPS Score:        {{NPS}}
```

**Comparison to Previous**:
- Previous NPS: {{PREV_NPS}}
- Change: {{DELTA}} ({{INTERPRETATION}})

### Task Completion Rates

| Focus Area | Task | Completion | Avg Time | Issues |
|------------|------|------------|----------|--------|
| FTUE | Complete tutorial | {{%}}% | {{T}}s | {{N}} |
| Core Loop | Win first round | {{%}}% | {{T}}s | {{N}} |
| Monetization | Find shop | {{%}}% | {{T}}s | {{N}} |
| Social | Add friend | {{%}}% | {{T}}s | {{N}} |

### Qualitative Themes

#### Theme 1: {{THEME_NAME}} ({{N}}/{{TOTAL}} participants)

**Description**: {{DESCRIPTION}}

**Evidence**:
> "{{QUOTE}}" — P{{N}}

**Recommendation**: {{RECOMMENDATION}}

#### Theme 2: {{THEME_NAME}} ({{N}}/{{TOTAL}} participants)
...

---

## Issue Log

### P0: Blockers ({{COUNT}})

| ID | Issue | Frequency | Recommendation |
|----|-------|-----------|----------------|
| P0-1 | {{ISSUE}} | {{N}}/{{TOTAL}} | {{REC}} |

### P1: Major ({{COUNT}})

| ID | Issue | Frequency | Recommendation |
|----|-------|-----------|----------------|
| P1-1 | {{ISSUE}} | {{N}}/{{TOTAL}} | {{REC}} |

### P2: Minor ({{COUNT}})
...

### P3: Polish ({{COUNT}})
...

---

## Recommendations

### Immediate Actions (Before Next Build)

1. **{{ACTION_1}}**: {{DETAILS}}
2. **{{ACTION_2}}**: {{DETAILS}}

### Next Playtest Scope

- **Focus**: {{FOCUS_AREAS}}
- **Target N**: {{PARTICIPANT_COUNT}}
- **Build Requirements**: {{REQUIREMENTS}}
- **Timeline**: After {{MILESTONE}}

---

## Appendix

### A. Participant Demographics

| ID | Age | Gender | Experience | Device |
|----|-----|--------|------------|--------|
| P1 | ... | ... | ... | ... |

### B. Session Recordings

| Session | Recording | Key Timestamps |
|---------|-----------|----------------|
| Session 1 | [Link] | 00:05 FTUE, 02:30 Bug |

### C. Raw Survey Data

See `docs/playtest/metrics.json`
```

## Quality Gates

### QG-PLAYTEST-001: Minimum Sample Size

| Playtest Type | Minimum N | Rationale |
|---------------|-----------|-----------|
| Internal | 5 | Find obvious issues |
| Friends & Family | 10 | Directional insights |
| Closed Beta | 30 | Statistical significance |
| Focus Group | 6 | Qualitative depth |

### QG-PLAYTEST-002: NPS Measurement

- NPS question MUST be asked in every session
- NPS MUST be calculated and reported
- NPS trend SHOULD be tracked across playtests

### QG-PLAYTEST-003: No Unresolved P0s

- All P0 (blocker) issues MUST have:
  - Clear description
  - Reproduction steps
  - Assigned owner or action item
  - Target fix date

### QG-PLAYTEST-004: Comprehension Gate

- Comprehension rate < 80% → FTUE needs revision
- Comprehension rate < 60% → BLOCK soft launch

## Industry Benchmarks

### Retention Expectations Post-Playtest

| Playtest Result | Expected D1 | Action |
|-----------------|-------------|--------|
| NPS 50+, Comp 90%+ | 40%+ | Proceed to soft launch |
| NPS 30-50, Comp 80-90% | 30-40% | Minor iteration |
| NPS 10-30, Comp 60-80% | 20-30% | Major iteration |
| NPS <10, Comp <60% | <20% | Fundamental redesign |

### Sample Sizes for Confidence

| Confidence Level | Sample Size | Error Margin |
|------------------|-------------|--------------|
| Directional | 5-10 | ±20-30% |
| Indicative | 20-30 | ±10-15% |
| Confident | 50-100 | ±5-10% |
| Statistical | 200+ | ±3-5% |

## Example Output

```
/speckit.playtest --playtest_type=friends_family --build_version=0.3.2 --target_participants=15 --focus_areas=[ftue,core_loop]

✅ Wave 1: Planning
   ├── Generated playtest-plan.md
   └── Created survey templates

📋 Playtest Plan Summary:
   - Type: Friends & Family
   - Target: 15 participants
   - Focus: FTUE, Core Loop
   - Duration: 45 min/session

✅ Wave 2: Session Execution
   ├── Session 1/15: P001 (completed)
   ├── Session 2/15: P002 (completed)
   ...
   └── Session 15/15: P015 (completed)

✅ Wave 3: Analysis
   ├── Calculated metrics
   └── Synthesized themes

📊 Key Metrics:
   - NPS: 42 (Good)
   - FTUE Completion: 87%
   - Core Loop Comprehension: 93%
   - Would Play Again: 80%

✅ Wave 4: Reporting
   ├── Generated playtest-report.md
   └── Generated action-items.md

⚠️ Issues Found:
   - P0: 1 (Blocker)
   - P1: 3 (Major)
   - P2: 5 (Minor)
   - P3: 2 (Polish)

🔗 Handoffs:
   → /speckit.tasks (Create bug tasks for P0/P1)
   → /speckit.gdd --update (UX flow revision recommended)
```

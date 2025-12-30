# Brainstorm-Curate Protocol

> Generate multiple options before committing to one approach. Prevents premature convergence and ensures considered decisions.

## Purpose

When facing non-trivial decisions, follow a two-phase process:
1. **Brainstorm**: Generate 3-5 genuinely different options (no evaluation)
2. **Curate**: Evaluate against criteria, select and document reasoning

This prevents:
- Anchoring on the first idea
- Missing better alternatives
- Decisions without documented reasoning
- "We chose X" without explaining "why not Y"

---

## When to Apply

```text
APPLY_BRAINSTORM_CURATE = [
  # Architecture Decisions
  "database selection",
  "caching strategy",
  "authentication approach",
  "deployment architecture",
  "API design pattern",
  "state management",
  "message queue selection",

  # Product Decisions
  "feature prioritization",
  "user flow design",
  "monetization model",
  "pricing strategy",
  "go-to-market approach",

  # Technical Trade-offs
  "build vs buy",
  "library/framework selection",
  "data model design",
  "integration approach",

  # UX Decisions
  "navigation structure",
  "onboarding flow",
  "error handling UX",
  "notification strategy"
]

SKIP_WHEN = [
  "Decision is trivial (single obvious answer)",
  "User already specified the approach explicitly",
  "Time constraint explicitly stated by user",
  "Following established project patterns (no deviation needed)",
  "Industry standard with no real alternatives"
]
```

---

## Phase 1: Brainstorm

### Rules

```text
BRAINSTORM_RULES = [
  "Generate 3-5 distinct options (minimum 3, prefer 5)",
  "Each option must be GENUINELY different (not variations)",
  "Include at least one 'conventional' option (industry standard)",
  "Include at least one 'unconventional' option (what-if challenge)",
  "Include at least one 'minimal' option (simplest possible)",
  "NO EVALUATION during brainstorming — just generate",
  "Capture ALL ideas, even seemingly crazy ones",
  "Don't dismiss options prematurely"
]
```

### Output Format

```text
### Brainstorm: [Decision Point]

**Decision**: [What are we deciding?]
**Context**: [Why does this decision matter?]
**Constraints**: [What limits our options?]

---

**Option 1: [Descriptive Name]** (Conventional)
- Approach: [2-3 sentence description]
- Example: [How would this look in our system?]
- Pro: [Primary advantage]
- Con: [Primary disadvantage]

**Option 2: [Descriptive Name]** (Unconventional)
- Approach: [2-3 sentence description]
- Example: [How would this look in our system?]
- Pro: [Primary advantage]
- Con: [Primary disadvantage]

**Option 3: [Descriptive Name]** (Minimal)
- Approach: [2-3 sentence description]
- Example: [How would this look in our system?]
- Pro: [Primary advantage]
- Con: [Primary disadvantage]

[Option 4, 5 if applicable...]
```

### Unconventional Option Prompts

To generate truly different options, ask:

```text
UNCONVENTIONAL_PROMPTS = [
  "What if we did the opposite of the conventional approach?",
  "What would [innovative company] do here?",
  "What if we had zero budget/unlimited budget?",
  "What if we had to ship in 1 day vs 1 year?",
  "What would a total beginner try?",
  "What's the 'lazy' solution that might actually work?",
  "What if we ignored the constraint that seems fixed?",
  "What would make users say 'wow, that's clever'?"
]
```

---

## Phase 2: Curate

### Evaluation Criteria

```text
EVALUATION_DIMENSIONS = {
  # Product Value
  user_delight: "How delighted would users be? (0-10)",
  time_to_value: "How quickly do users see benefit? (0-10)",

  # Technical
  feasibility: "Can our team build this? (0-10)",
  maintainability: "How easy to maintain long-term? (0-10)",
  scalability: "Will it scale to 10x load? (0-10)",

  # Business
  differentiation: "Does this set us apart? (0-10)",
  cost_efficiency: "Resource cost vs value? (0-10)",
  risk_level: "Execution risk? (10=low risk, 0=high risk)"
}

# Weight by project priorities:
# - Startup MVP: user_delight (3x), time_to_value (3x), feasibility (2x)
# - Enterprise: maintainability (3x), scalability (2x), risk_level (2x)
# - Scale-up: scalability (3x), cost_efficiency (2x), differentiation (2x)
```

### Scoring Matrix

```text
### Evaluation Matrix

| Criterion | Weight | Opt 1 | Opt 2 | Opt 3 | Opt 4 | Opt 5 |
|-----------|--------|-------|-------|-------|-------|-------|
| User Delight | 3x | 7 | 9 | 5 | 8 | 6 |
| Time to Value | 3x | 6 | 4 | 9 | 5 | 7 |
| Feasibility | 2x | 9 | 6 | 8 | 7 | 8 |
| Maintainability | 1x | 8 | 5 | 7 | 6 | 7 |
| **Weighted Score** | | **54** | **52** | **58** | **50** | **54** |
```

### Hybrid Identification

Before final selection, check for hybrid possibilities:

```text
HYBRID_CHECK:
  "Can we combine the best parts of multiple options?"

  Example:
  - Option 1 has best user experience
  - Option 3 has simplest implementation
  - Hybrid: Use Option 3's architecture with Option 1's UX layer

  Document hybrid as Option N+1 if viable, then include in evaluation.
```

### Output Format

```text
### Recommendation: [Chosen Option Name]

**Weighted Score**: [X] (highest among options)

**Why this approach:**
1. [Specific reason tied to project goals]
2. [Specific reason tied to constraints]
3. [Specific reason tied to team capabilities]

**Key trade-offs accepted:**
- Accepting: [what we give up]
- Because: [why it's acceptable in our context]

**Why not alternatives:**
- **Option X**: [Specific disqualifier]
- **Option Y**: [Specific disqualifier]
- **Option Z**: [Specific disqualifier]

**Reversibility:**
- Reversible: Yes/No/Partially
- If partially: [What's locked in, what can change]
- Pivot cost: [Low/Medium/High]

**Implementation note:**
[Any specific guidance for executing this approach]
```

---

## Examples

### Example 1: Database Selection

```text
### Brainstorm: Database for User Analytics

**Decision**: Which database to use for storing and querying user analytics events
**Context**: Need to store 1M events/day, query for dashboards and reports
**Constraints**: Team knows PostgreSQL well, budget < $500/month

---

**Option 1: PostgreSQL with TimescaleDB** (Conventional)
- Approach: Use familiar PostgreSQL with time-series extension
- Example: Store events in hypertable, use continuous aggregates for dashboards
- Pro: Team knows it, single database to manage
- Con: May struggle at very high write volumes

**Option 2: ClickHouse** (High Performance)
- Approach: Purpose-built OLAP database for analytics
- Example: Column-oriented storage, 100x faster analytical queries
- Pro: Best-in-class performance for analytics workloads
- Con: Team has zero experience, new operational burden

**Option 3: BigQuery** (Managed)
- Approach: Serverless data warehouse, pay per query
- Example: Batch load events daily, run SQL for dashboards
- Pro: Zero ops burden, scales infinitely
- Con: Not real-time, costs can spike unpredictably

**Option 4: Keep in Main PostgreSQL** (Minimal)
- Approach: Just add events table to existing database
- Example: Simple INSERT, query with regular SQL
- Pro: No new infrastructure
- Con: Will degrade main database performance

**Option 5: Event Store + Materialized Views** (Unconventional)
- Approach: Append-only event log with pre-computed views
- Example: Write to Kafka, materialize into Postgres views nightly
- Pro: Decouples write from read, flexible reprocessing
- Con: Complex architecture for team size
```

```text
### Recommendation: PostgreSQL with TimescaleDB

**Weighted Score**: 62 (highest)

**Why this approach:**
1. Team expertise: 2 devs have 5+ years PostgreSQL experience, zero learning curve
2. Single stack: No additional database to monitor/maintain/pay for
3. Proven at scale: TimescaleDB handles 1M inserts/day easily, headroom to 10M

**Key trade-offs accepted:**
- Accepting: Not the absolute fastest query performance
- Because: Our dashboards need 2-second response, not 200ms. Timescale delivers <500ms.

**Why not alternatives:**
- **ClickHouse**: Team size (3) can't absorb operational complexity
- **BigQuery**: Real-time dashboard requirement disqualifies batch approach
- **Keep in main DB**: Performance impact on core product unacceptable
- **Event Store + Views**: Over-engineered for current scale

**Reversibility:**
- Reversible: Partially
- Lock-in: TimescaleDB schema differs from standard PostgreSQL
- Pivot cost: Medium (would need data migration to switch)

**Implementation note:**
Start with single hypertable, partition by week. Add continuous aggregates
for top 5 dashboard queries. Revisit when hitting 5M events/day.
```

### Example 2: User Onboarding Flow

```text
### Brainstorm: New User Onboarding

**Decision**: How to onboard new users to the analytics dashboard
**Context**: Current signup → blank dashboard → 80% drop-off in first session
**Constraints**: Must work for technical and non-technical users

---

**Option 1: Guided Tour** (Conventional)
- Approach: Step-by-step tooltip walkthrough of key features
- Pro: Users see all features, familiar pattern
- Con: Most users skip, doesn't show value

**Option 2: Sample Data** (Value-First)
- Approach: Pre-populate with realistic demo data
- Pro: Users see value immediately, explore naturally
- Con: Extra click to clear demo data

**Option 3: Template Selection** (Personalized)
- Approach: Ask use case, show pre-configured dashboard
- Pro: Immediately relevant to user's goals
- Con: Adds friction before value

**Option 4: Video Welcome** (Minimal)
- Approach: 60-second video explanation, then let them explore
- Pro: Low dev effort, personal touch
- Con: Passive, doesn't drive action

**Option 5: Competitive Import** (Unconventional)
- Approach: Import from Mixpanel/Amplitude, show same data in our UI
- Pro: Zero setup, immediate comparison with their tool
- Con: Complex integrations, limited initial reach
```

---

## Integration

### In Concept Phase

```text
IMPORT: templates/shared/quality/brainstorm-curate.md

FOR EACH major feature area identified:
  IF feature has multiple valid approaches:
    APPLY brainstorm_curate_protocol
    DOCUMENT in concept.md under "Solution Architecture"
```

### In Plan Phase

```text
IMPORT: templates/shared/quality/brainstorm-curate.md

FOR architecture_decision IN [database, caching, auth, deployment]:
  IF decision is non-trivial:
    APPLY brainstorm_curate_protocol
    DOCUMENT chosen approach with reasoning in plan.md
```

### In Design Phase

```text
IMPORT: templates/shared/quality/brainstorm-curate.md

FOR ux_decision IN [navigation, onboarding, error_handling]:
  IF multiple valid patterns exist:
    APPLY brainstorm_curate_protocol
    DOCUMENT in wireframes/design-decisions.md
```

---

## Quick Reference

```text
BRAINSTORM PHASE:
□ Generate 3-5 options
□ Include 1 conventional option
□ Include 1 unconventional option
□ Include 1 minimal option
□ NO evaluation yet

CURATE PHASE:
□ Score against weighted criteria
□ Check for hybrid possibilities
□ Select highest score
□ Document "why this" reasoning
□ Document "why not others" reasoning
□ Note reversibility and pivot cost
```

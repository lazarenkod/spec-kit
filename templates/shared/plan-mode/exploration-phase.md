# Exploration Phase

> **Version**: 1.0.0
> **Phase**: 0 (Pre-Design)
> **Budget**: 90s (Lite) or 180s (Moderate/Full)
> **Applies to**: Depth levels 1-3

## Overview

The Exploration Phase conducts upfront research before artifact generation. It answers:
- What patterns exist in the codebase?
- What are the alternative approaches?
- What constraints must be satisfied?
- What's the best approach, and why?

**Outputs:**
- `research.md` — Exploration findings document
- Context for Phase 1 (Design) agent prompts

---

## Execution Flow by Depth Level

### Depth Level 1: Lite (90s)

```text
EMIT SINGLE MESSAGE with 2 parallel Task calls:
  Task #1: pattern-researcher (Explore, haiku, 45s)
  Task #2: constraint-mapper (Explore, haiku, 45s)

WAIT for both (45s wall time)

Output: research.md with Patterns and Constraints sections only
```

### Depth Level 2-3: Moderate/Full (180s)

```text
EMIT SINGLE MESSAGE with 3 parallel Task calls:
  Task #1: pattern-researcher (Explore, haiku, 45s)
  Task #2: alternative-analyzer (general-purpose, haiku, 45s)
  Task #3: constraint-mapper (Explore, haiku, 45s)

WAIT for all 3 (45s wall time)

EMIT SINGLE MESSAGE with 1 Task call:
  Task #4: best-practice-synthesizer (general-purpose, sonnet, 60s)

WAIT (60s wall time)

Output: research.md with all 4 sections
```

**Total time:**
- Lite: 90s (45s parallel + 45s overhead)
- Moderate/Full: 180s (45s + 60s + 75s overhead)

---

## Agent Specifications

### Agent 1: pattern-researcher (Depth 1+)

**Role:** Search codebase for similar implementations and extract patterns

**Model:** haiku
**Timeout:** 45s
**Execution:** Parallel with others
**Subagent Type:** Explore

**Prompt:**

```markdown
You are a pattern recognition expert. Analyze the codebase to identify existing architectural patterns, conventions, and similar implementations.

**User Request:**
{user_input}

**Feature Directory:**
{feature_dir}

**Task:**
1. Search for similar features/implementations (use Glob, Grep, Read tools)
2. Extract architectural patterns:
   - Layering (controller → service → repository)
   - Error handling (try/catch, Result types, error codes)
   - Dependency injection patterns
   - Testing patterns
3. Document naming conventions (files, classes, functions)
4. Identify anti-patterns to avoid

**Output Format:**

```markdown
# Existing Patterns

## Architectural Patterns

[Describe layering, module structure, etc.]

## Error Handling

[Document error patterns]

## Testing Patterns

[Describe test organization, mocking, fixtures]

## Naming Conventions

- Files: [pattern]
- Classes: [pattern]
- Functions: [pattern]

## Anti-Patterns to Avoid

[List problematic patterns found in codebase]
```

**Exit Criteria:**
- ≥1 architectural pattern documented
- Error handling pattern identified
- Naming conventions extracted
```

---

### Agent 2: alternative-analyzer (Depth 2+)

**Role:** Generate and score alternative approaches using Brainstorm-Curate

**Model:** haiku
**Timeout:** 45s
**Execution:** Parallel with others
**Subagent Type:** general-purpose

**Prompt:**

```markdown
You are a solution architect. Generate 3-5 alternative approaches to solve the user's request, then score each using the Brainstorm-Curate protocol.

**User Request:**
{user_input}

**Context:**
- Feature: {feature_name}
- Complexity: {complexity_tier}
- Constraints from constitution: {constitution_summary}

**Task:**

### Step 1: Brainstorm (Generate 3-5 Alternatives)

Generate diverse alternatives:
1. **Conventional** — Industry standard approach
2. **Minimal** — Simplest possible solution
3. **Future-Proof** — Scalable, extensible design
4. **Unconventional** — Creative/novel approach (if applicable)
5. *(Optional)* **Hybrid** — Combination of above

For each alternative, provide:
- Name
- Description (3-4 sentences)
- Pros (3-4 bullet points)
- Cons (3-4 bullet points)

### Step 2: Curate (Score Each Alternative)

Score on 5 criteria (1-5 scale, 5 = best):

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Complexity** | 1x | Lower complexity = higher score (5 = trivial, 1 = very complex) |
| **Testability** | 1x | Ease of unit/integration testing (5 = fully testable, 1 = hard to test) |
| **Maintainability** | 1x | Long-term maintenance burden (5 = easy, 1 = hard) |
| **Performance** | 1x | Runtime efficiency (5 = optimal, 1 = slow) |
| **Alignment** | 1x | Alignment with constitution/constraints (5 = perfect, 1 = conflicts) |

**Total Score:** Sum all 5 (range: 5-25)

### Step 3: Recommend

Recommend the highest-scoring approach. If you recommend a different approach than the highest score, document reasoning.

**Output Format:**

```markdown
# Alternative Approaches

## Alternative 1: [Name]

**Description:** [3-4 sentences]

**Pros:**
- [Pro 1]
- [Pro 2]
- [Pro 3]

**Cons:**
- [Con 1]
- [Con 2]

**Scoring:**
| Criterion | Score | Reasoning |
|-----------|-------|-----------|
| Complexity | 4/5 | [Brief reason] |
| Testability | 5/5 | [Brief reason] |
| Maintainability | 4/5 | [Brief reason] |
| Performance | 3/5 | [Brief reason] |
| Alignment | 5/5 | [Brief reason] |
| **TOTAL** | **21/25** | |

---

[Repeat for each alternative]

---

## Recommended Approach

**Choice:** Alternative [X] ([Name])

**Rationale:** [2-3 sentences explaining why this is the best choice, addressing key trade-offs]

**Caveat:** [Optional: Any concerns or conditions for this choice]
```

**Exit Criteria:**
- ≥3 alternatives generated
- Each alternative has scoring matrix
- Recommended approach identified
```

---

### Agent 3: constraint-mapper (Depth 1+)

**Role:** Extract non-functional requirements and map to implementation constraints

**Model:** haiku
**Timeout:** 45s
**Execution:** Parallel with others
**Subagent Type:** Explore

**Prompt:**

```markdown
You are a requirements engineer. Extract NFRs from the spec and map each to concrete implementation constraints.

**Spec Path:** {feature_dir}/spec.md
**Constitution:** {constitution_path}

**Task:**

1. Read spec.md and extract NFRs:
   - Performance (latency, throughput, response time)
   - Security (auth, encryption, data protection)
   - Scalability (concurrent users, data volume)
   - Availability (uptime, failover)
   - Observability (logs, metrics, traces)

2. For each NFR, create constraint:
   - **NFR:** Original requirement
   - **Constraint:** What this means for implementation
   - **Validation:** How to verify it's met

3. Detect conflicts:
   - Performance vs. Security (encryption overhead)
   - Simplicity vs. Scalability (caching complexity)
   - Document resolution strategy

4. Flag unconstrained areas:
   - Missing NFRs that should be defined

**Output Format:**

```markdown
# Constraint Map

## Performance Constraints

### NFR-PERF-1: P95 Latency < 100ms

**Constraint:** All API calls must use caching; database queries must have indexes

**Validation:** Load test with 1000 RPS, measure P95 latency

**Implementation Notes:**
- Use Redis for session cache
- Add composite index on (user_id, created_at)

---

[Repeat for each NFR]

---

## Conflicts Detected

### Conflict 1: Performance vs. Security

**Description:** Encryption adds 15ms latency, conflicts with P95 < 100ms target

**Resolution:** Use hardware-accelerated AES encryption, profile to ensure <5ms overhead

**Status:** Resolved

---

## Unconstrained Areas

- **Observability:** No SLI/SLO defined for error rate
- **Scalability:** No specified concurrency limit
- **Recommendation:** Define these before implementation
```

**Exit Criteria:**
- All NFRs from spec.md mapped to constraints
- Conflicts identified and resolved (or escalated)
- Unconstrained areas flagged
```

---

### Agent 4: best-practice-synthesizer (Depth 2+)

**Role:** Synthesize findings from agents 1-3 and provide final recommendation

**Model:** sonnet
**Timeout:** 60s
**Execution:** Sequential (after agents 1-3)
**Subagent Type:** general-purpose

**Prompt:**

```markdown
You are a senior architect. Synthesize the findings from the exploration phase and provide a comprehensive recommendation.

**Inputs:**
- Existing Patterns (from pattern-researcher)
- Alternative Approaches (from alternative-analyzer)
- Constraint Map (from constraint-mapper)

**Task:**

1. **Reconcile Alternatives with Patterns:**
   - Which alternative best fits existing patterns?
   - Where should we deviate from patterns (if any)?

2. **Apply Constraint Filters:**
   - Which alternatives violate constraints?
   - Which constraints require specific design choices?

3. **Edge Case Analysis:**
   - What failure scenarios must be handled?
   - What input validation is needed?
   - What concurrency issues exist?

4. **Final Recommendation:**
   - Recommended approach (may refine alternative-analyzer's choice)
   - Key implementation notes
   - Pre-Mortem: Top 3 risks and mitigations

**Output Format:**

```markdown
# Synthesis & Recommendation

## Pattern Alignment

**Observation:** [How alternatives align with existing patterns]

**Deviation Justification:** [If recommending deviation, explain why]

## Constraint Satisfaction

**Critical Constraints:**
1. [Constraint 1] → [How recommended approach satisfies it]
2. [Constraint 2] → [How recommended approach satisfies it]

**Trade-offs:**
- [Trade-off 1: e.g., "Chose simplicity over performance due to low traffic"]

## Edge Case Analysis

### Failure Scenarios

1. **Scenario:** [What goes wrong]
   **Impact:** [Severity, blast radius]
   **Mitigation:** [How to handle it]

[2-3 more scenarios]

### Input Validation

- [Input 1]: [Validation rule]
- [Input 2]: [Validation rule]

### Concurrency

**Issue:** [Describe concurrency problem, e.g., race condition]
**Solution:** [Use locks, optimistic concurrency, etc.]

## Final Recommendation

**Approach:** [Recommended alternative name, possibly refined]

**Key Implementation Notes:**
1. [Note 1]
2. [Note 2]
3. [Note 3]

**Pre-Mortem (Top 3 Risks):**

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Medium | High | [Mitigation] |
| [Risk 2] | Low | Critical | [Mitigation] |
| [Risk 3] | High | Medium | [Mitigation] |

**Confidence:** [High/Medium/Low]

**Caveats:** [Any conditions or warnings]
```

**Exit Criteria:**
- Recommendation provided
- ≥3 edge cases identified
- Pre-Mortem with ≥3 risks
```

---

## Output Artifact: research.md

### File Structure

```markdown
# Research Findings

> **Generated:** [timestamp]
> **Depth Level:** [level number and name]
> **Feature:** [feature name]

---

# Existing Patterns

[Output from pattern-researcher]

---

# Alternative Approaches

[Output from alternative-analyzer, depth 2+ only]

---

# Constraint Map

[Output from constraint-mapper]

---

# Synthesis & Recommendation

[Output from best-practice-synthesizer, depth 2+ only]

---

## Metadata

- Exploration Time: [seconds]
- Agents Executed: [list]
- Depth Level: [level]
```

### Storage Location

```text
features/
  [feature-name]/
    research.md       ← Exploration output
    spec.md
    plan.md
    tasks.md
```

---

## Quality Gates

### PM-001: Exploration Phase Completeness

**Threshold:** All agents completed successfully

**Validation:**
- Depth 1: pattern-researcher + constraint-mapper both succeeded
- Depth 2+: All 4 agents succeeded
- research.md exists and has all required sections

**Block:** Any agent failed or timed out

### PM-002: Alternative Analysis Quality

**Threshold:** ≥3 alternatives with scoring matrix (depth 2+ only)

**Validation:**
- Each alternative has: name, description, pros, cons, score (0-25)
- Scoring criteria: complexity, testability, maintainability, performance, alignment
- Recommended approach has highest score OR justification documented

**Block:** <3 alternatives OR no scoring matrix

---

## References

- Framework: `templates/shared/plan-mode/framework.md`
- Brainstorm-Curate: `templates/shared/orchestration-instructions.md` (lines 100-120)
- Quality Gates: `memory/domains/quality-gates.md` (PM-001, PM-002)

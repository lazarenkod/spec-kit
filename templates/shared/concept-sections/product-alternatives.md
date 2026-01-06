# Product Alternatives

> **Purpose**: Generate 3-5 fundamentally different product visions solving the same problem. Ensures exploration of design space before committing to one approach.

## Integration Notes

- **Depends on**: Phase 0a-0c (Problem Discovery, Market Research, Solution Ideation)
- **Feeds into**: Vision Statement, Feature Hierarchy
- **CQS Impact**: Strategic Clarity component (30/100 points)
- **Phase**: Phase 0d (Discovery Mode)

---

## Alternative Generation Strategies

When generating product alternatives, apply these 5 strategic lenses to the same core problem:

### 1. Conventional Approach
**Philosophy**: Industry standard, proven patterns
**Question**: "What do successful competitors do?"
**Characteristics**:
- Follows established market patterns
- Lower risk, faster time to market
- Competitive parity baseline
- Clear benchmarks available

### 2. Minimal Approach
**Philosophy**: Simplest 80/20 solution
**Question**: "What's the absolute minimum that solves the core problem?"
**Characteristics**:
- Focuses on one primary JTBD
- Maximum speed to market
- Lowest technical complexity
- Fast hypothesis validation

### 3. Disruptive Approach
**Philosophy**: Opposite/contrarian thinking
**Question**: "What if we did the exact opposite of competitors?"
**Characteristics**:
- Challenges industry assumptions
- High differentiation potential
- Higher risk, higher reward
- Novel user experience

### 4. Premium Approach
**Philosophy**: Best-in-class, no constraints
**Question**: "What if budget and time were unlimited?"
**Characteristics**:
- Maximum feature completeness
- Best-in-class UX and performance
- High technical complexity
- Premium positioning

### 5. Platform Approach
**Philosophy**: Ecosystem and network effects
**Question**: "How can we enable third parties to extend this?"
**Characteristics**:
- API-first architecture
- Marketplace or plugin system
- Network effects strategy
- Longer-term value capture

---

## Scoring Criteria

Each alternative is scored on 4 dimensions (40 points total):

| Criterion | Weight | Points | Evaluation Question |
|-----------|:------:|:------:|---------------------|
| **Problem-Solution Fit** | 30% | 12 | How directly does this solve the core problem? |
| **Market Differentiation** | 25% | 10 | How different is this from existing solutions? |
| **Feasibility** | 25% | 10 | Can we actually build this with our resources? |
| **Time to Market** | 20% | 8 | How quickly can we ship an MVP? |
| **TOTAL** | 100% | **40** | Overall score |

### Scoring Guidelines

**Problem-Solution Fit (12 points)**:
- 10-12: Directly solves primary JTBD with clear value proposition
- 7-9: Solves problem but requires user behavior change
- 4-6: Partial solution, leaves gaps
- 0-3: Tangential or unclear fit

**Market Differentiation (10 points)**:
- 9-10: Unique approach, no direct competitors
- 6-8: Clear differentiation from competitors
- 3-5: Similar to competitors with minor differences
- 0-2: Commoditized, no differentiation

**Feasibility (10 points)**:
- 9-10: Proven tech stack, clear implementation path
- 6-8: Some technical unknowns, manageable risk
- 3-5: Significant technical challenges, requires R&D
- 0-2: High risk, unproven approach

**Time to Market (8 points)**:
- 7-8: Can ship MVP in < 8 weeks
- 5-6: Can ship MVP in 8-16 weeks
- 3-4: Requires 16-24 weeks
- 0-2: > 24 weeks to MVP

---

## Template Structure

Use this template for EACH alternative:

```markdown
### Alternative [N]: [Strategy Name] — [One-line Vision]

**Strategy Type**: [Conventional/Minimal/Disruptive/Premium/Platform]

**Vision**: [1-2 sentence product vision that captures the unique approach]

**Core Features** (5-7 epics):
1. **[Epic Name]**: [1 sentence description]
2. **[Epic Name]**: [1 sentence description]
3. **[Epic Name]**: [1 sentence description]
4. **[Epic Name]**: [1 sentence description]
5. **[Epic Name]**: [1 sentence description]

**Value Proposition**: [User benefit statement — what makes this compelling?]

**Differentiation**: [How this differs from competitors — what's unique?]

**Pros**:
- ✅ [Advantage 1]
- ✅ [Advantage 2]
- ✅ [Advantage 3]

**Cons**:
- ❌ [Drawback 1]
- ❌ [Drawback 2]
- ❌ [Drawback 3]

**Effort Estimate**: [S/M/L/XL]
**Technical Risk**: [Low/Medium/High]
**Time to MVP**: [X weeks]

**Scoring**:
- Problem-Solution Fit: [X]/12
- Market Differentiation: [X]/10
- Feasibility: [X]/10
- Time to Market: [X]/8
- **TOTAL SCORE**: **[X]/40**

**Best For**: [When would you choose this alternative?]
```

---

## Comparison Matrix Template

After documenting all alternatives, create a comparison matrix:

```markdown
## Alternative Comparison Matrix

| Criterion | Alt 1: [Name] | Alt 2: [Name] | Alt 3: [Name] | Alt 4: [Name] | Alt 5: [Name] |
|-----------|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| **Strategy Type** | [Type] | [Type] | [Type] | [Type] | [Type] |
| **Problem Fit** (12pts) | X/12 | X/12 | X/12 | X/12 | X/12 |
| **Differentiation** (10pts) | X/10 | X/10 | X/10 | X/10 | X/10 |
| **Feasibility** (10pts) | X/10 | X/10 | X/10 | X/10 | X/10 |
| **Time to Market** (8pts) | X/8 | X/8 | X/8 | X/8 | X/8 |
| **TOTAL SCORE** | **X/40** | **X/40** | **X/40** | **X/40** | **X/40** |
| **Effort** | S/M/L/XL | S/M/L/XL | S/M/L/XL | S/M/L/XL | S/M/L/XL |
| **Risk** | Low/Med/High | Low/Med/High | Low/Med/High | Low/Med/High | Low/Med/High |
| **MVP Timeline** | X weeks | X weeks | X weeks | X weeks | X weeks |

### Quick Summary

**Highest Score**: Alternative [N] — [Name] ([X]/40)
**Fastest to Market**: Alternative [N] — [Name] ([X] weeks)
**Lowest Risk**: Alternative [N] — [Name] ([Risk level])
**Most Differentiated**: Alternative [N] — [Name] ([X]/10 differentiation score)
```

---

## Brainstorm-Curate Integration

Product Alternatives generation uses the **Brainstorm-Curate Protocol** from `templates/shared/quality/brainstorm-curate.md`:

### BRAINSTORM Phase (Divergent Thinking)

For EACH strategy type (Conventional/Minimal/Disruptive/Premium/Platform):

1. **Suspend Judgment**: No evaluation during generation
2. **Provocative Prompts**: Use unconventional questions:
   - "What would [Innovative Company] do here?"
   - "What if we had zero budget? Unlimited budget?"
   - "What would make users say 'wow, that's clever'?"
   - "What's the laziest solution that might work?"
   - "What if the opposite of best practices is actually better?"
3. **Concrete Details**: Don't just say "do X differently" — specify exactly how
4. **Evidence Links**: Ground each alternative in research from Phase 0a-0c

### CURATE Phase (Convergent Thinking)

After generating 5 alternatives:

1. **Score Each**: Apply 4-criterion scoring framework
2. **Identify Hybrids**: Can we combine best parts of multiple alternatives?
3. **Document Trade-offs**: Make pros/cons explicit
4. **Recommendation**: Which alternative(s) merit deeper exploration?

---

## Validation Checklist

Before finalizing Product Alternatives section:

- [ ] At least 3 alternatives documented (5 preferred)
- [ ] All 5 strategy types explored (Conventional, Minimal, Disruptive, Premium, Platform)
- [ ] Each alternative has unique vision statement
- [ ] Each alternative lists 5-7 concrete features/epics
- [ ] Scoring is evidence-based (references Phase 0a-0c findings)
- [ ] Comparison matrix complete with all scores
- [ ] Pros/cons are specific (not generic)
- [ ] Best-for guidance is actionable (not vague)
- [ ] At least one alternative scores ≥30/40

---

## Example: Team Collaboration Tool

```markdown
### Alternative 1: Conventional — Slack-Style Chat Platform

**Strategy Type**: Conventional

**Vision**: A real-time messaging platform with channels, threads, and integrations that brings team communication into one place.

**Core Features** (7 epics):
1. **Real-time messaging**: Instant messaging with typing indicators, read receipts
2. **Channels & DMs**: Organized conversations by topic, private messaging
3. **Threaded replies**: Keep discussions organized without cluttering main channel
4. **File sharing**: Drag-and-drop file uploads with previews
5. **Search**: Full-text search across messages and files
6. **Integrations**: Connect with GitHub, Jira, Google Drive, etc.
7. **Notifications**: Configurable alerts for mentions, DMs, keywords

**Value Proposition**: Reduces email overload and scattered conversations by centralizing team communication in one searchable, organized platform.

**Differentiation**: Enterprise-grade security and compliance (SOC 2, GDPR), on-premise deployment option.

**Pros**:
- ✅ Proven product-market fit (Slack validates demand)
- ✅ Clear monetization path (per-user pricing)
- ✅ Users already understand the paradigm

**Cons**:
- ❌ Highly competitive market (Slack, Teams, Discord)
- ❌ Requires network effects to be valuable
- ❌ "Chat overload" problem well-documented

**Effort Estimate**: L (12-16 weeks for MVP)
**Technical Risk**: Low (proven architecture patterns)
**Time to MVP**: 14 weeks

**Scoring**:
- Problem-Solution Fit: 10/12 (solves communication fragmentation)
- Market Differentiation: 4/10 (crowded market, enterprise focus helps)
- Feasibility: 9/10 (proven tech, WebSockets + React)
- Time to Market: 6/8 (14 weeks is competitive)
- **TOTAL SCORE**: **29/40**

**Best For**: Teams already using chat tools but needing better security/compliance.

---

### Alternative 2: Minimal — Async Voice Notes

**Strategy Type**: Minimal

**Vision**: Async voice messaging for teams — like walkie-talkie meets podcast. Record thoughts, teammates listen when convenient.

**Core Features** (5 epics):
1. **Voice recording**: One-tap record, auto-transcription
2. **Playback controls**: 1.5x speed, skip silence, bookmarks
3. **Topics**: Organize voice notes by project/topic
4. **Reactions**: Quick emoji reactions without creating notification noise
5. **Transcripts**: Searchable text, accessibility, skimmable

**Value Proposition**: Eliminates meeting fatigue and timezone challenges. Think async, communicate naturally.

**Differentiation**: Voice-first async (no meetings, no real-time pressure), automatic transcription makes it searchable.

**Pros**:
- ✅ Extremely simple to build (MVP in 4-6 weeks)
- ✅ Solves remote/async-first team pain
- ✅ Novel approach (not another chat app)

**Cons**:
- ❌ Unproven concept (no major player)
- ❌ User behavior change required
- ❌ Limited network effects

**Effort Estimate**: S (4-6 weeks for MVP)
**Technical Risk**: Medium (transcription API dependency)
**Time to MVP**: 5 weeks

**Scoring**:
- Problem-Solution Fit: 8/12 (solves async communication but misses real-time needs)
- Market Differentiation: 9/10 (very novel approach)
- Feasibility: 8/10 (transcription API risk)
- Time to Market: 8/8 (very fast to MVP)
- **TOTAL SCORE**: **33/40**

**Best For**: Remote-first teams, distributed timezones, "deep work" culture.

---

### Alternative 3: Disruptive — No-Communication Tool

**Strategy Type**: Disruptive

**Vision**: Eliminate unnecessary communication by making work self-documenting. Teams collaborate through transparent work streams, not messages.

**Core Features** (6 epics):
1. **Activity streams**: Every action auto-logged (commits, tickets, docs)
2. **Smart digest**: AI summarizes daily activity, highlights blockers
3. **Read-only by default**: Can't message unless you've read context
4. **Decision log**: All decisions auto-extracted from commits/PRs
5. **Auto-standups**: AI generates standup from activity, no meetings
6. **Transparency score**: Gamify how well you document your work

**Value Proposition**: Stop interrupting each other. Stay aligned through radical transparency and self-documenting work.

**Differentiation**: Anti-communication stance (opposite of Slack), AI-first summarization, forces good documentation habits.

**Pros**:
- ✅ Extremely differentiated (contrarian bet)
- ✅ Solves "too much communication" problem
- ✅ Forces async-first culture

**Cons**:
- ❌ Requires major behavior change
- ❌ May not work for all team types
- ❌ "AI summarization" is unproven at scale

**Effort Estimate**: XL (20-24 weeks for MVP)
**Technical Risk**: High (AI summarization quality critical)
**Time to MVP**: 22 weeks

**Scoring**:
- Problem-Solution Fit: 7/12 (solves overcommunication but may miss edge cases)
- Market Differentiation: 10/10 (unique, contrarian)
- Feasibility: 5/10 (AI quality is hard to guarantee)
- Time to Market: 2/8 (long timeline)
- **TOTAL SCORE**: **24/40**

**Best For**: Engineering teams with strong documentation culture, "no meetings" philosophy.

---

[Alternatives 4 and 5 would follow similar format...]
```

---

## Integration with Concept.md

### In Executive Summary

After generating and selecting an alternative, update Executive Summary:

```markdown
### Our Approach
[2-3 sentences describing selected alternative approach]

**Selected Alternative**: [Alternative Name] — scored [X]/40 in alternatives analysis.
See "Product Alternatives" section for complete comparison of 5 approaches considered.
```

### In Vision Statement

Use selected alternative's vision statement as starting point:

```markdown
## Vision Statement

[Selected alternative's vision, expanded with context]

**Selection Rationale**:
We considered 5 alternative approaches (Conventional, Minimal, Disruptive, Premium, Platform) and selected [Alternative Name] because:
1. [Reason 1: e.g., "Best problem-solution fit for primary persona"]
2. [Reason 2: e.g., "Optimal balance of differentiation and feasibility"]
3. [Reason 3: e.g., "Fastest path to validating core hypothesis"]
```

### In Feature Hierarchy

Expand selected alternative's epics into full feature hierarchy:

```markdown
## Feature Hierarchy

<!--
  Features derived from Alternative [N]: [Name]
  See Product Alternatives section for alternatives considered
-->

[Detailed feature breakdown based on selected alternative's 5-7 epics]
```

---

## CQS Scoring Integration

Product Alternatives contributes to **Strategic Clarity** component of CQS-E:

| Criterion | Points | Check |
|-----------|:------:|-------|
| Product Alternatives generated | 30 | ≥3 alternatives documented |
| All 5 strategy types explored | +5 bonus | Conventional, Minimal, Disruptive, Premium, Platform |
| Selection rationale documented | +5 bonus | Clear "why this alternative" explanation |

**Scoring Logic**:

```python
PRODUCT_ALTERNATIVES_SCORE = 0

# Base score
ALTERNATIVES_COUNT = count("Alternative [0-9]+:")
SELECTED = check("Selected Alternative:")

if ALTERNATIVES_COUNT >= 5 and SELECTED:
    PRODUCT_ALTERNATIVES_SCORE += 30
elif ALTERNATIVES_COUNT >= 3 and SELECTED:
    PRODUCT_ALTERNATIVES_SCORE += 25
elif ALTERNATIVES_COUNT >= 3:
    PRODUCT_ALTERNATIVES_SCORE += 15
else:
    PRODUCT_ALTERNATIVES_SCORE += 0

# Bonus: All strategy types
STRATEGY_TYPES = count_unique("Strategy Type: (Conventional|Minimal|Disruptive|Premium|Platform)")
if STRATEGY_TYPES >= 5:
    PRODUCT_ALTERNATIVES_SCORE += 5

# Bonus: Selection rationale
if check("Selection Rationale:") and len(rationale_bullets) >= 3:
    PRODUCT_ALTERNATIVES_SCORE += 5

# Maximum: 40 points (caps at 30 for CQS component)
PRODUCT_ALTERNATIVES_SCORE = min(PRODUCT_ALTERNATIVES_SCORE, 30)
```

---

## Common Pitfalls

### ❌ Avoid: Scope Variations Disguised as Alternatives

**Wrong**:
- Alternative 1: Minimal Chat (just messaging)
- Alternative 2: Full Chat (messaging + calls + screen sharing)
- Alternative 3: Enterprise Chat (Full Chat + SSO + compliance)

**Why Wrong**: These are scope levels (MINIMAL/BALANCED/AMBITIOUS) of the SAME product vision, not fundamentally different approaches.

**Right**:
- Alternative 1: Real-time Chat (Slack approach)
- Alternative 2: Async Voice Notes (novel approach)
- Alternative 3: No-Communication Tool (contrarian approach)

### ❌ Avoid: Generic/Vague Alternatives

**Wrong**: "Alternative 1: A platform that helps teams collaborate better"

**Right**: "Alternative 1: Slack-Style Chat — Real-time messaging with channels, threads, and integrations"

### ❌ Avoid: Unevaluated Brainstorming

**Wrong**: Just listing 5 ideas without scoring, pros/cons, or trade-offs.

**Right**: Each alternative scored on 4 criteria, pros/cons listed, best-for guidance provided.

---

## Output Files

### Primary: specs/concept.md

Contains "Product Alternatives" section with:
- Selected alternative summary
- Selection rationale
- Reference to full analysis

### Supporting: specs/concept-alternatives.md

Separate file with:
- All 5 alternatives in full detail
- Comparison matrix
- Scoring breakdown
- Decision log (how selection was made)

**Cleanup**: After concept finalized, `concept-alternatives.md` can be archived or deleted.

---

## References

- `templates/shared/quality/brainstorm-curate.md` — Brainstorm-Curate Protocol
- `templates/shared/concept-sections/concept-variants.md` — Scope Variants (different from Product Alternatives)
- `templates/shared/concept-sections/selection-rationale.md` — Per-feature selection reasoning

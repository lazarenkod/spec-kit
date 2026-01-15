# World-Class Improvements for /speckit.concept

**Дата**: 2026-01-01
**Агент**: product-manager
**Цель**: Поднять качество concept outputs до уровня Amazon, Google, Stripe, OpenAI

---

## Executive Summary

Текущая имплементация `/speckit.concept` **уже очень сильна** в:
- Hierarchical feature breakdown (Epic/Feature/Story)
- TAM/SAM/SOM market sizing
- JTBD-enhanced personas
- Risk assessment & CQS scoring
- Technical discovery hints

**Gaps vs world-class product strategy**:
1. **Отсутствует narrative structure** — документ читается как checklist, а не как compelling story
2. **Слабая strategic positioning** — нет Blue Ocean Canvas, Porter's 5 Forces, Business Model Canvas
3. **Нет decision-making frameworks** — отсутствуют trade-off frameworks и decision logs
4. **Недостаточная stakeholder segmentation** — один документ для всех аудиторий
5. **Слабая validation rigor** — нет structured assumption testing и hypothesis tracking

---

## 1. Strategic Depth: Missing Frameworks

### 1.1 Amazon Working Backwards (PR/FAQ)

**Что не хватает**: Concept начинается с features, а не с customer experience

**Предложение**: Добавить **PR/FAQ section** в начало concept.md

```markdown
## Press Release (Draft — Launch Day Vision)

**FOR IMMEDIATE RELEASE**

### [Product Name]: [One-line value proposition]

**[DATE]** — [Company] today announced [Product], [what it does for whom].

**Problem Statement**:
[Target customer] struggle with [specific problem]. Current solutions like [competitors] fall short because [gap].

**Solution**:
[Product] solves this by [unique approach]. Unlike [alternatives], we [differentiation].

**Customer Quote** (imagined):
"[Name], [Title] at [Company], said: '[Impact on their workflow/business]'"

**How to Get Started**:
[Simplest onboarding path]

**Pricing** (indicative):
[Pricing model sketch]

---

## Frequently Asked Questions (Internal)

### Customer Questions
1. **Q: Why is this better than [competitor]?**
   A: [Specific differentiation]

2. **Q: How long does it take to see value?**
   A: [Time to first value]

3. **Q: What if [common objection]?**
   A: [Objection handling]

### Internal Questions
1. **Q: What's the business case?**
   A: [Revenue model, market size, strategic fit]

2. **Q: Why now?**
   A: [Market timing, competitive window, enabling technology]

3. **Q: What could go wrong?**
   A: [Top 3 risks and mitigations]

4. **Q: What are we NOT building?**
   A: [Out of scope — prevents feature creep]
```

**Impact**: Forces clarity on customer value BEFORE feature lists. Aligns team around outcome, not output.

**Placement**: After Problem Discovery (Phase 0a), before Feature Hierarchy (step 6).

**Sources**:
- [Amazon Working Backwards PR/FAQ](https://www.productplan.com/glossary/working-backward-amazon-method/)
- [Amazon PR/FAQ Guide 2025](https://www.landpmjob.com/amazon-working-backwards-prfaq)

---

### 1.2 Blue Ocean Strategy Canvas

**Что не хватает**: Competitive Positioning Matrix сравнивает features, но не показывает **strategic differentiation**

**Предложение**: Добавить **Blue Ocean Strategy Canvas** в Market Opportunity section

```markdown
## Blue Ocean Strategy Canvas

**Purpose**: Visualize competitive factors and identify differentiation opportunities

### Strategy Canvas

| Competing Factor | Importance (1-10) | Industry Avg | Competitor A | Us (Target) | Action |
|------------------|:-----------------:|:------------:|:------------:|:-----------:|--------|
| [Factor 1] | 8 | 7 | 9 | 3 | **REDUCE** — over-served |
| [Factor 2] | 9 | 5 | 6 | 2 | **ELIMINATE** — not valued |
| [Factor 3] | 10 | 4 | 4 | 9 | **RAISE** — differentiation |
| [Factor 4] | 7 | 0 | 0 | 8 | **CREATE** — new value curve |

### Four Actions Framework (ERRC Grid)

| Eliminate | Reduce | Raise | Create |
|-----------|--------|-------|--------|
| [Factors to eliminate] | [Factors to reduce below industry] | [Factors to raise above industry] | [New factors industry never offered] |

**Example** (Wine industry — Yellow Tail):
- **Eliminate**: Aging complexity, prestige terminology, marketing mystique
- **Reduce**: Price, wine complexity, vineyard range
- **Raise**: Retail store involvement, approachability
- **Create**: Easy drinking, fun/adventure brand, easy selection

### Our Value Curve

**Hypothesis**: By [eliminating X] and [creating Y], we create uncontested market space in [segment].

**Validation plan**:
1. Survey [N] target users on factor importance
2. Benchmark competitors on each factor
3. Test prototype with [reduce/eliminate] factors removed
4. Measure willingness-to-pay for [create] factors
```

**Impact**:
- Reveals **strategic positioning**, not just feature parity
- Identifies "blue ocean" opportunities (uncontested market space)
- Guides product decisions: what NOT to build is as important as what to build

**Sources**:
- [Blue Ocean Strategy Canvas](https://www.blueoceanstrategy.com/tools/strategy-canvas/)
- [ERRC Grid Framework](https://quantive.com/resources/articles/blue-ocean-strategy)

---

### 1.3 Porter's 5 Forces (Market Dynamics)

**Что не хватает**: Market sizing есть, но нет **structural analysis of competition**

**Предложение**: Добавить **Porter's 5 Forces** для understanding market attractiveness

```markdown
## Market Dynamics (Porter's 5 Forces)

### 1. Threat of New Entrants
| Factor | Assessment | Barriers to Entry |
|--------|:----------:|-------------------|
| Capital requirements | Low/Med/High | [Cost to start competing product] |
| Technology barriers | Low/Med/High | [Proprietary tech, patents, expertise] |
| Network effects | Low/Med/High | [Do we get stronger with more users?] |
| Regulatory barriers | Low/Med/High | [Compliance, licensing] |
| Brand loyalty | Low/Med/High | [Switching costs for customers] |

**Verdict**: Threat is **[Low/Medium/High]** because [reasoning]

### 2. Bargaining Power of Suppliers
- **Key suppliers**: [Dependencies on platforms, APIs, data providers]
- **Switching cost**: [How hard to replace supplier]
- **Concentration**: [Few suppliers or many alternatives?]
- **Verdict**: Power is **[Low/Medium/High]**

### 3. Bargaining Power of Buyers
- **Buyer concentration**: [Few large customers or many small?]
- **Price sensitivity**: [How much do they care about price?]
- **Switching costs**: [Hard to switch to competitor?]
- **Verdict**: Power is **[Low/Medium/High]**

### 4. Threat of Substitutes
| Substitute | How it solves problem | Our advantage vs substitute |
|------------|----------------------|----------------------------|
| [Alternative 1] | [Approach] | [Why we're better] |
| [Alternative 2] | [Approach] | [Why we're better] |
| Do nothing | [Status quo workaround] | [Cost of inaction] |

**Verdict**: Threat is **[Low/Medium/High]**

### 5. Competitive Rivalry
- **Market growth rate**: [Growing/Flat/Declining]
- **Number of competitors**: [Few/Many]
- **Differentiation**: [Commoditized/Differentiated]
- **Exit barriers**: [Hard to leave market?]
- **Verdict**: Rivalry is **[Low/Medium/High]**

### Overall Market Attractiveness

**Score**: [X/5 forces favorable]

**Conclusion**: This market is [Attractive/Neutral/Unattractive] because [summary]. Our moat will be [what makes us defensible].
```

**Impact**:
- Reveals **structural profitability** of market (not just size)
- Identifies where to build moats (network effects, switching costs, brand)
- Informs pricing power and long-term sustainability

---

### 1.4 Business Model Canvas

**Что не хватает**: Revenue model buried in metrics. No clear view of **how business works end-to-end**.

**Предложение**: Добавить **Business Model Canvas** visualization

```markdown
## Business Model Canvas

| Key Partners | Key Activities | Value Propositions | Customer Relationships | Customer Segments |
|--------------|----------------|-------------------|----------------------|-------------------|
| [Who we rely on] | [What we do] | [What we offer] | [How we interact] | [Who we serve] |
| • [Partner 1] | • [Activity 1] | **For [Segment A]**: | • [Relationship type] | **Primary**: |
| • [Partner 2] | • [Activity 2] | [Value prop] | • [Acquisition] | [Segment details] |
| | | | • [Retention] | **Secondary**: |
| **Key Resources** | | **Channels** | | [Segment details] |
| [What we need] | | [How we reach them] | | |
| • [Resource 1] | | • [Channel 1] | | |
| • [Resource 2] | | • [Channel 2] | | |

| Cost Structure | Revenue Streams |
|----------------|-----------------|
| **Fixed costs**: | **Revenue model**: |
| • [Cost 1] | • [Stream 1]: [pricing model] |
| • [Cost 2] | • [Stream 2]: [pricing model] |
| **Variable costs**: | **Unit economics**: |
| • [Cost per unit] | • LTV: $[X] |
| **Burn rate**: $[X]/mo | • CAC: $[X] |
| | • LTV/CAC: [ratio] |

### Unit Economics Deep Dive

| Metric | Value | Notes |
|--------|-------|-------|
| **CAC** (Customer Acquisition Cost) | $[X] | [Channel breakdown] |
| **LTV** (Lifetime Value) | $[X] | [Retention assumption] |
| **LTV/CAC ratio** | [X]:1 | Target: ≥3:1 |
| **Payback period** | [X] months | Target: ≤12 months |
| **Gross margin** | [X]% | [COGS breakdown] |
```

**Impact**:
- Holistic view of business model (not just product)
- Forces thinking about distribution, not just features
- Reveals economic viability early

---

## 2. Narrative Quality: Story Structure

### 2.1 Problem: Concept reads like a checklist

**Текущая структура**:
```
1. Vision Statement
2. Market Opportunity
3. Personas
4. Features
5. Risks
```

**World-class structure** (storytelling arc):
```
1. The World Today (Problem Space)
   ↓
2. What's Broken (Gap Analysis)
   ↓
3. The Future We're Building (Vision)
   ↓
4. Why Now (Market Timing)
   ↓
5. How We Win (Strategy)
   ↓
6. What Success Looks Like (Outcomes)
   ↓
7. The Plan (Roadmap)
```

**Предложение**: Добавить **narrative scaffolding** в concept template

```markdown
## Part 1: The World Today

### Current State
[Target customer] currently solve [problem] by [workaround]. This results in [pain points]:
- [Pain 1]: [Specific example with numbers]
- [Pain 2]: [Specific example with numbers]
- [Pain 3]: [Specific example with numbers]

**Example scenario**:
> "[Persona name], a [role] at [company type], spends [X hours/week] doing [manual task] because [no good solution]. This costs them [money/time/opportunity]."

### What's Broken
Existing solutions ([competitor A], [competitor B]) fail because:
1. **[Gap 1]**: [Specific shortcoming]
2. **[Gap 2]**: [Specific shortcoming]
3. **[Gap 3]**: [Specific shortcoming]

**Market gap**: [X]% of [target segment] are underserved by current solutions ([source])

---

## Part 2: The Future We're Building

### Vision (3-5 years out)
In [year], [target customer] will [new behavior enabled by product]. Instead of [old way], they'll [new way], resulting in [outcome].

**Transformation**:
- **From**: [Current painful state]
- **To**: [Desired future state]
- **Unlock**: [New possibilities not currently feasible]

### Why Now
This is possible now (but wasn't 2 years ago) because:
1. **[Enabling trend 1]**: [Technology/regulation/culture shift]
2. **[Enabling trend 2]**: [Technology/regulation/culture shift]
3. **[Market readiness]**: [Evidence customers are ready]

**Timing window**: We have [X months/years] before [competitors catch up / market saturates].

---

## Part 3: How We Win

### Strategic Moats
We will be defensible because:
1. **[Moat 1]**: [Network effects / Data advantage / Brand / Switching costs]
2. **[Moat 2]**: [How this compounds over time]
3. **[Moat 3]**: [What makes us hard to copy]

**Competitive positioning**:
- vs [Competitor A]: We win on [dimension] because [reason]
- vs [Competitor B]: We win on [dimension] because [reason]
- vs Do Nothing: We win because [cost of inaction > cost of switching]

### Go-to-Market Strategy
- **Beachhead**: [Specific segment to dominate first]
- **Why this beachhead**: [Underserved, accessible, reference-able]
- **Expansion path**: [Beachhead] → [Adjacent segment 1] → [Adjacent segment 2] → [Mass market]

---

## Part 4: What Success Looks Like

### Year 1 Outcomes
- [Outcome 1]: [Measurable result]
- [Outcome 2]: [Measurable result]
- [Outcome 3]: [Measurable result]

### Year 3 Vision
- [Outcome 1]: [Measurable result]
- [Outcome 2]: [Measurable result]
- [Market position]: [Where we stand in market]
```

**Impact**:
- Concept becomes **persuasive** (tells a story, not lists facts)
- Stakeholders can see the vision, not just the features
- Builds excitement and alignment

**Sources**:
- [Product Narrative Storytelling](https://wynter.com/post/narrative-strategy)
- [Executive Presentation Best Practices](https://www.storydoc.com/blog/presentation-storytelling-examples)

---

### 2.2 Add "Why This Matters" context to every section

**Предложение**: Each section should answer **"So what?"**

**Before**:
```markdown
## TAM/SAM/SOM
| TAM | $5B |
| SAM | $500M |
| SOM | $50M |
```

**After**:
```markdown
## TAM/SAM/SOM

**Why this matters**: We need $50M ARR to reach profitability. Our SOM of $50M in Year 3 assumes 10% market capture, which is achievable because [evidence].

| Metric | Value | Calculation | So What? |
|--------|-------|-------------|----------|
| TAM | $5B | [Method] | Large enough to support multiple $1B companies |
| SAM | $500M | [Filters] | Focused segment with high willingness-to-pay |
| SOM | $50M | [Realistic capture] | Achievable with [X] enterprise customers at $[Y] ACV |
```

**Impact**: Every metric connects to **business outcomes**, not just academic sizing.

---

## 3. Decision Frameworks: Trade-offs & Choices

### 3.1 Stripe-style Decision Logs

**Что не хватает**: Concept captures decisions but not **why we chose X over Y**

**Предложение**: Добавить **Decision Log** section

```markdown
## Strategic Decisions

**Purpose**: Document key product decisions and rationale for future reference

| Decision | Options Considered | Choice | Rationale | Reversibility | Date |
|----------|-------------------|--------|-----------|:-------------:|------|
| Pricing model | Usage-based vs Flat-rate vs Freemium | **Flat-rate** | Lower complexity for SMB segment, easier to forecast | Medium (pricing can change) | [Date] |
| Market segment | SMB vs Enterprise vs Prosumer | **SMB** | Faster sales cycle, self-serve motion, larger TAM | Low (defines product DNA) | [Date] |
| Tech stack | [Option A] vs [Option B] | **[Choice]** | [Why] | High (can migrate) | [Date] |
| MVP scope | [Ambitious] vs [Minimal] | **[Choice]** | [Why] | High (can add later) | [Date] |

### Decision-Making Principles

When faced with trade-offs, we prioritize:
1. **[Principle 1]**: [What we optimize for] > [What we sacrifice]
2. **[Principle 2]**: [Example trade-off and resolution]
3. **[Principle 3]**: [Example trade-off and resolution]

**Example**:
- **Speed vs Perfection**: Ship fast, iterate based on feedback (AWS "2-way door" decisions)
- **Simplicity vs Power**: Default to simple, add power for advanced users only
- **Self-serve vs Sales-led**: Optimize for self-serve, offer white-glove for enterprise

### "What We're NOT Building" (Anti-Scope Creep)

Explicitly out of scope for this concept:
- [ ] [Feature/idea] — Why: [Reason], When: [Future phase if ever]
- [ ] [Feature/idea] — Why: [Reason], When: [Future phase if ever]
- [ ] [Feature/idea] — Why: [Reason], When: [Future phase if ever]

**Impact**: Prevents scope creep. "No" is as important as "yes".
```

**Impact**:
- Creates **institutional memory** of why decisions were made
- Enables learning from past decisions (Stripe practice)
- Prevents re-litigating settled decisions

**Sources**:
- [Stripe Decision Logs](https://www.blitzllama.com/blog/stripe-product-management-practices)

---

### 3.2 Trade-off Frameworks (Explicit)

**Предложение**: Формализовать **how we make hard choices**

```markdown
## Trade-off Resolution Framework

### When features conflict, apply this hierarchy:

| Priority | Principle | Example |
|:--------:|-----------|---------|
| 1 | **User value** | If feature A helps more users than feature B → choose A |
| 2 | **Strategic alignment** | If feature aligns with North Star → prioritize |
| 3 | **Defensibility** | If feature creates moat (network effects, data) → prioritize |
| 4 | **Time to value** | If feature can ship in 1/3 the time with 80% value → ship faster |

### Build vs Buy vs Partner

| Criteria | Build | Buy | Partner |
|----------|:-----:|:---:|:-------:|
| Core differentiation | ✓ | ✗ | ✗ |
| Table stakes | ✗ | ✓ | ✓ |
| High integration complexity | ✓ | ✗ | ~ |
| Fast time to market | ✗ | ✓ | ✓ |
| Long-term control needed | ✓ | ~ | ✗ |

**Example decisions**:
- **Auth system**: Buy (not differentiation, high complexity) → Use Auth0/Clerk
- **Core algorithm**: Build (key IP, competitive advantage)
- **Payment processing**: Partner (regulated, table stakes) → Use Stripe

### Feature Prioritization Matrix

| Feature | User Impact | Business Impact | Effort | Reversibility | PRIORITY |
|---------|:-----------:|:---------------:|:------:|:-------------:|:--------:|
| [Feature 1] | High (8/10) | High ($500K ARR) | Low (2 weeks) | High | **P0** |
| [Feature 2] | Med (5/10) | Low ($50K ARR) | High (3 months) | Low | **P2** |

**Formula**: Priority = (User Impact × Business Impact) / (Effort × (1 - Reversibility))
```

**Impact**: Consistent decision-making across team. No debates without framework.

---

## 4. Validation Rigor: Assumption Testing

### 4.1 OpenAI-style Hypothesis Tracking

**Что не хватает**: Risks identified, but **assumptions not explicitly tested**

**Предложение**: Добавить **Hypothesis Testing Log**

```markdown
## Hypothesis Testing Log

**Purpose**: Track key assumptions and validate before building

| Hypothesis | Type | Test Method | Success Criteria | Status | Result |
|------------|------|-------------|------------------|:------:|--------|
| Users will pay $X/mo for [value] | Pricing | Landing page test | 10% conversion | 🟡 Testing | [Result] |
| [Persona] has [problem] daily | Problem | User interviews | 8/10 say "very painful" | ✅ Validated | 9/10 confirmed |
| [Feature] reduces time by 50% | Solution | Prototype test | Users complete task in <5min | 🔴 Failed | Only 20% improvement |
| Market size is $500M | Market | TAM analysis | Multiple sources confirm | ✅ Validated | Gartner: $480M |
| We can acquire users for <$100 | GTM | Ad campaign test | CAC < $100 on paid channels | 🟡 Testing | [Result] |

**Legend**: ✅ Validated | 🟡 Testing | 🔴 Failed | ⚪ Not tested

### Riskiest Assumptions (Validate First)

1. **[Assumption 1]**: [What we're betting on]
   - **Why risky**: [What happens if wrong]
   - **Test plan**: [How to validate cheaply]
   - **Success criteria**: [What proves it true]
   - **Timeline**: Test by [date]

2. **[Assumption 2]**: [What we're betting on]
   - **Why risky**: [What happens if wrong]
   - **Test plan**: [How to validate cheaply]
   - **Success criteria**: [What proves it true]
   - **Timeline**: Test by [date]

### Validation Milestones

Before proceeding to Wave 1 implementation, we must validate:
- [ ] **Problem severity**: [X] users confirm pain level ≥8/10
- [ ] **Willingness to pay**: [X] users commit to pilot at $[Y]/mo
- [ ] **Technical feasibility**: Prototype proves [key tech risk] solvable
- [ ] **Market timing**: [Evidence] confirms market is ready now

**Kill criteria**: If [assumption X] fails validation, we pivot to [alternative] or kill project.
```

**Impact**:
- Forces **explicit testing** of assumptions (not just documenting them)
- Reduces risk of building wrong thing
- Creates data-driven validation culture (OpenAI practice)

**Sources**:
- [OpenAI Product-Market Fit Framework](https://www.thevccorner.com/p/ai-product-market-fit-framework-openai)
- [Hypothesis Testing for Products](https://www.productcompass.pm/p/openai-how-to-build-ai-product-strategy)

---

### 4.2 Pre-Mortem Analysis

**Предложение**: Before building, imagine **"It's 12 months from now. The product failed. Why?"**

```markdown
## Pre-Mortem Analysis

**Exercise**: Imagine it's [date 12 months from now]. The product launched but failed. What went wrong?

### Failure Scenarios

| Scenario | Likelihood | If this happens... | Prevention |
|----------|:----------:|-------------------|------------|
| Users don't adopt (activation < 20%) | Medium | [Impact] | [What we'll do to prevent] |
| Competitors copy us in 6 months | High | [Impact] | [Moat strategy] |
| Key integration partner shuts down API | Low | [Impact] | [Backup plan] |
| We can't acquire users profitably (CAC > LTV) | Medium | [Impact] | [Channel diversification] |
| Product is too complex (NPS < 30) | High | [Impact] | [UX simplification] |

### Most Likely Failure Mode

**What's most likely to kill this**: [Scenario]

**Why we think this**: [Evidence from similar products]

**How we'll prevent it**:
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Early warning signals**:
- If [metric] < [threshold] at [time] → trigger mitigation plan
- If [behavior] observed → pivot to [alternative]
```

**Impact**: Surfaces blind spots. Forces proactive risk mitigation.

---

## 5. Stakeholder Communication: Multi-Audience Concept

### 5.1 Problem: One document for all audiences

**Текущая ситуация**: CEO, engineers, designers, investors read same concept.md

**World-class practice**: **Tailor narrative to audience**

**Предложение**: Добавить **Executive Summary variants**

```markdown
## Executive Summary (Multi-Audience)

### For CEO / Leadership (Strategic)
**In 3 sentences**:
We're building [product] for [target customer] who currently [struggle with X]. Unlike [competitors], we [unique approach] which will capture $[X] of a $[Y] market. Success = [North Star metric] reaching [target] by [date].

**Strategic fit**: [How this aligns with company vision]

**Ask**: [What you need from leadership - budget, resources, decisions]

---

### For Engineering (Technical)
**In 3 sentences**:
We're building [product] that requires [tech stack]. Core technical challenge is [problem] which we'll solve with [approach]. MVP scope is [X features] targeting [launch date].

**Technical risks**: [Top 3 with mitigations]

**Architecture hints**: [Key entities, API surface, integrations]

---

### For Design (Experience)
**In 3 sentences**:
We're designing for [persona] who needs to [job to be done] in [context]. Key UX challenge is [problem] which we'll solve by [approach]. Success = [user can achieve X in <Y time with Z satisfaction].

**Design principles**: [Constraints and priorities]

**UX Foundations**: [Required patterns from catalog]

---

### For Investors (Financial)
**In 3 sentences**:
We're targeting $[X]M market with [business model] at [price point]. Unit economics: LTV $[X], CAC $[Y], ratio [Z]:1. Path to $[X]M ARR in [Y] years via [go-to-market strategy].

**Financial projections**: [Revenue, burn, breakeven timeline]

**Use of funds**: [How investment will be deployed]

---

### For Marketing (Positioning)
**In 3 sentences**:
We're positioning against [competitors] with differentiation on [dimension]. Target message: "[Headline]". Key channels: [acquisition strategy].

**Competitive messaging**: [How to win vs each competitor]

**Launch strategy**: [Timing, channels, partnerships]
```

**Impact**:
- Each stakeholder gets **relevant context** quickly
- No need to read entire 50-page concept to understand their part
- Speeds up alignment and decision-making

---

### 5.2 Visual Strategy Summary (One-Pager)

**Предложение**: Concept должен генерировать **visual one-pager** для executive review

```markdown
## Strategy Canvas (Visual Summary)

```
┌─────────────────────────────────────────────────────────────────┐
│  [PRODUCT NAME] — Strategy Overview                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROBLEM                          SOLUTION                      │
│  ┌──────────────────┐            ┌──────────────────┐          │
│  │ [Target user]    │            │ [Our approach]   │          │
│  │ spends [X hrs]   │    ───►    │ reduces to [Y]   │          │
│  │ on [manual task] │            │ via [automation] │          │
│  └──────────────────┘            └──────────────────┘          │
│                                                                 │
│  MARKET                           BUSINESS MODEL               │
│  • TAM: $5B                       • Pricing: $X/mo             │
│  • SAM: $500M                     • LTV/CAC: 4:1               │
│  • SOM: $50M (Yr 3)               • Breakeven: 18mo           │
│                                                                 │
│  COMPETITION                      MOAT                         │
│  vs [Competitor A]: Win on [X]    • Network effects           │
│  vs [Competitor B]: Win on [Y]    • Data advantage            │
│  vs Do Nothing: [Cost of inaction]• Switching costs           │
│                                                                 │
│  ROADMAP                          SUCCESS METRICS              │
│  Wave 1: [Foundation] (Q1)        North Star: [Metric]        │
│  Wave 2: [Experience] (Q2)        Target: [X] by [Date]       │
│  Wave 3: [Growth] (Q3-Q4)         PMF signal: [Indicator]     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Impact**:
- Leadership can grasp strategy in 60 seconds
- Single slide for all-hands presentations
- Easy to share with board/investors

---

## 6. Implementation Priorities

### Phase 1: Quick Wins (1-2 weeks)
1. ✅ Add **PR/FAQ section** (Amazon Working Backwards)
2. ✅ Add **Decision Log** table
3. ✅ Add **"What We're NOT Building"** section
4. ✅ Add **Hypothesis Testing Log**

### Phase 2: Moderate Effort (2-4 weeks)
5. ✅ Add **Blue Ocean Strategy Canvas**
6. ✅ Add **Business Model Canvas**
7. ✅ Restructure concept with **narrative arc** (story structure)
8. ✅ Add **Multi-Audience Executive Summaries**

### Phase 3: Advanced (4-8 weeks)
9. ✅ Add **Porter's 5 Forces** analysis
10. ✅ Add **Pre-Mortem Analysis**
11. ✅ Generate **Visual Strategy One-Pager**
12. ✅ Create **Trade-off Resolution Framework**

---

## 7. Measurement of Success

### How to know improvements worked:

| Metric | Before | After (Target) | Measurement |
|--------|:------:|:--------------:|-------------|
| **Concept Quality Score (CQS)** | 60-80 avg | 85+ avg | Existing CQS calculation |
| **Time to stakeholder alignment** | [X days] | <50% reduction | Days from concept → approval |
| **Strategic clarity** | Qualitative | 8/10+ on survey | Stakeholder survey: "I understand the strategy" |
| **Decision-making speed** | [X decisions/week] | 2x faster | Track decisions logged |
| **Pivot rate** | [X]% projects pivot | <50% reduction | % of concepts that fail validation |

### Qualitative Signals

- ✅ Stakeholders can articulate strategy without reading full concept
- ✅ Fewer "Why are we building this?" questions
- ✅ Faster executive approvals
- ✅ Engineers understand user context before implementation
- ✅ Design has clear principles to guide decisions

---

## 8. Comparison: Before vs After

### Before (Current State)
```
Concept Document:
├── Vision Statement (generic)
├── Market Opportunity (TAM/SAM/SOM)
├── Personas (demographics)
├── Feature Hierarchy (Epic/Feature/Story)
├── Risk Assessment
└── CQS Score

Strengths: Comprehensive, structured
Weaknesses: Reads like checklist, no story, hard to scan
```

### After (World-Class)
```
Concept Document:
├── PR/FAQ (Customer narrative, launch vision)
├── The World Today (Problem space with examples)
├── What's Broken (Gap analysis)
├── The Future We're Building (Vision with transformation)
├── Why Now (Market timing)
├── Strategic Positioning
│   ├── Blue Ocean Canvas (Differentiation strategy)
│   ├── Porter's 5 Forces (Market dynamics)
│   └── Business Model Canvas (How business works)
├── How We Win
│   ├── Moats & Defensibility
│   ├── Go-to-Market Strategy
│   └── Competitive Positioning
├── Decision Log (Why we chose X over Y)
├── Hypothesis Testing (Assumption validation)
├── Pre-Mortem (Failure scenarios)
├── Feature Hierarchy (What we build)
├── Multi-Audience Summaries (CEO/Eng/Design/Investors)
└── Visual Strategy One-Pager

Strengths: Compelling story, strategic depth, actionable decisions
Weaknesses: Longer (but scannable with multi-audience summaries)
```

---

## 9. Specific Template Updates

### Update to `templates/commands/concept.md`

**Add new steps**:

```yaml
# After step 4 (Discovery → Structure transition):

4c. **Generate PR/FAQ** (Amazon Working Backwards):
   - Write press release as if product launched
   - Draft customer FAQ (objections, comparisons)
   - Draft internal FAQ (business case, risks, scope)
   - Place at beginning of concept (before features)

# After step 5a (JTBD Personas):

5aa-2. **Strategic Positioning Frameworks**:
   1. Blue Ocean Strategy Canvas (ERRC Grid)
   2. Porter's 5 Forces (Market dynamics)
   3. Business Model Canvas (Revenue model)

# After step 5c (Risk Assessment):

5c-2. **Pre-Mortem Analysis**:
   - Imagine project failed in 12 months
   - List failure scenarios with likelihood
   - Document prevention strategies
   - Identify early warning signals

# After step 8 (Dependencies):

8d. **Decision Log**:
   - Document strategic decisions made
   - Record options considered and why chosen
   - Mark reversibility of each decision
   - Add "What We're NOT Building" section

8e. **Hypothesis Testing Log**:
   - List riskiest assumptions
   - Define validation tests
   - Set success criteria
   - Track validation status

# After step 11 (Write concept.md):

11b. **Generate Multi-Audience Summaries**:
   - Executive summary for CEO (strategic)
   - Executive summary for Engineering (technical)
   - Executive summary for Design (experience)
   - Executive summary for Investors (financial)
   - Executive summary for Marketing (positioning)

11c. **Generate Visual Strategy One-Pager**:
   - ASCII art strategy canvas
   - Problem → Solution → Market → Moat
   - One-slide format for presentations
```

---

## 10. New Shared Templates

### Create new templates in `templates/shared/concept-sections/`:

1. **`pr-faq-amazon.md`** — Amazon Working Backwards template
2. **`blue-ocean-canvas.md`** — Strategy Canvas & ERRC Grid
3. **`porters-five-forces.md`** — Market dynamics analysis
4. **`business-model-canvas.md`** — Revenue model visualization
5. **`decision-log.md`** — Stripe-style decision tracking
6. **`hypothesis-testing.md`** — OpenAI-style assumption validation
7. **`pre-mortem-analysis.md`** — Failure scenario planning
8. **`multi-audience-summary.md`** — Stakeholder-specific summaries
9. **`visual-strategy-onepager.md`** — Executive presentation format

---

## 11. Sources & References

### Amazon Product Strategy
- [Amazon Working Backwards PR/FAQ](https://www.productplan.com/glossary/working-backward-amazon-method/)
- [Amazon PR/FAQ Guide 2025](https://www.landpmjob.com/amazon-working-backwards-prfaq)
- [Working Backwards Process](https://productstrategy.co/working-backwards-the-amazon-prfaq-for-product-innovation/)

### Stripe Product Strategy
- [Stripe GPTN Framework](https://www.aakashg.com/stripe-modern-product-rocket/)
- [What Makes Stripe Great](https://www.blitzllama.com/blog/stripe-product-management-practices)
- [Stripe Decision Logs](https://www.blitzllama.com/blog/stripe-product-management-practices)

### OpenAI Product Strategy
- [OpenAI Product-Market Fit Framework](https://www.thevccorner.com/p/ai-product-market-fit-framework-openai)
- [AI Product Strategy Framework](https://www.productcompass.pm/p/openai-how-to-build-ai-product-strategy)
- [OpenAI Iterative Deployment](https://www.lomitpatel.com/articles/openai-product-strategy/)

### Strategic Frameworks
- [Blue Ocean Strategy Canvas](https://www.blueoceanstrategy.com/tools/strategy-canvas/)
- [Blue Ocean ERRC Grid](https://quantive.com/resources/articles/blue-ocean-strategy)
- [Porter's 5 Forces](https://en.wikipedia.org/wiki/Porter%27s_five_forces_analysis)

### Narrative & Storytelling
- [Product Narrative Strategy](https://wynter.com/post/narrative-strategy)
- [Executive Presentation Storytelling](https://www.storydoc.com/blog/presentation-storytelling-examples)
- [Strategic Storytelling Techniques](https://24slides.com/presentbetter/7-essential-storytelling-techniques-for-your-business-presentation)

---

## 12. Recommended Reading for Team

### Books
- **"Working Backwards"** by Colin Bryar & Bill Carr (Amazon practices)
- **"Blue Ocean Strategy"** by W. Chan Kim & Renée Mauborgne
- **"Inspired"** by Marty Cagan (Silicon Valley Product Group)
- **"The Lean Product Playbook"** by Dan Olsen

### Articles
- Amazon's 6-Page Narrative Memo structure
- Stripe's Operating Principles
- Netflix's Context, Not Control culture doc
- Airbnb's 11-Star Experience framework

---

## Conclusion

Текущая имплементация `/speckit.concept` **уже сильна** в structured hierarchy и validation rigor (CQS).

Эти улучшения поднимут её до **world-class level** через:
1. **Strategic depth** — Blue Ocean, Porter's 5 Forces, Business Model Canvas
2. **Narrative quality** — PR/FAQ, story arc, multi-audience summaries
3. **Decision frameworks** — Decision logs, trade-off resolution, hypothesis testing
4. **Validation rigor** — Pre-mortem, assumption tracking, kill criteria
5. **Stakeholder communication** — Visual one-pagers, audience-specific summaries

**Impact**: Concepts становятся **compelling strategic documents**, а не просто feature checklists. Alignment ускоряется, decisions становятся evidence-based, pivots происходят раньше (когда они дешевле).

**Next Steps**: Prioritize Phase 1 quick wins (PR/FAQ, Decision Log, Hypothesis Testing) → validate with pilot project → roll out Phase 2-3 improvements.

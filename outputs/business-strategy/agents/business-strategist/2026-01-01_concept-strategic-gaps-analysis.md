# Strategic Gap Analysis: /speckit.concept vs Fortune 500 Strategy Standards

**Analyst**: Business Strategist Agent
**Date**: 2026-01-01
**Context**: Upgrade `/speckit.concept` command to match Amazon, Microsoft, Google, Oracle corporate strategy standards
**Current State**: TAM/SAM/SOM, competitive matrix, basic risk assessment, technical hints

---

## Executive Summary

Текущая реализация `/speckit.concept` — это **хороший product management фреймворк**, но ему не хватает **корпоративной стратегической глубины** для инвестиционных решений Board/CEO-уровня.

**Критический разрыв**: Инструмент фокусируется на "что построить", а не на "почему это правильный стратегический выбор СЕЙЧАС для достижения N-year vision с учётом портфеля альтернатив".

**Рекомендация**: Добавить 5 недостающих стратегических слоёв (см. ниже), не отказываясь от текущей product-ориентированной базы.

---

## 1. Strategic Planning Gaps: Missing Fortune 500 Frameworks

### 1.1 Three Horizons Framework (McKinsey/Google/Microsoft)

**Что есть**: Концепт описывает одну идею целиком.
**Что НЕ хватает**: Портфельное мышление — куда эта идея вписывается в стратегический портфель компании?

```markdown
## Strategic Horizon Classification

| Dimension | Horizon 1 (Defend) | Horizon 2 (Extend) | Horizon 3 (Create) |
|-----------|-------------------|-------------------|-------------------|
| **This Concept** | [✓/✗] | [✓/✗] | [✓/✗] |
| Timeframe | 0-12 months | 1-3 years | 3-5 years |
| Revenue Impact | Protect existing $[X]M | Grow into $[Y]M | Create new $[Z]M |
| Risk Tolerance | Low | Medium | High |
| Success Criteria | [Defend market share] | [Enter adjacent] | [Build new category] |
| Portfolio Balance | [% of R&D budget] | [% of R&D budget] | [% of R&D budget] |

### Portfolio Context
- **H1 projects competing for resources**: [List]
- **H2 projects competing for resources**: [List]
- **H3 projects competing for resources**: [List]
- **Strategic rationale for THIS horizon**: [Why now, why this vs alternatives]
```

**Пример Amazon**: Amazon Go (H3 2016) → Prime Air (H3) vs Alexa Skills expansion (H2) vs AWS feature parity (H1). Каждый проект явно классифицирован, метрики отличаются, риски управляются по-разному.

**Пример Microsoft**: Cloud-первая стратегия Надели (H1: Azure core, H2: Industry Clouds, H3: OpenAI partnership). Концепты без привязки к горизонту не получают funding.

---

### 1.2 MOALS/OSM (Amazon Operating Model)

**Что есть**: Success Metrics с SMART-валидацией.
**Что НЕ хватает**: Связка метрик с операционной моделью и ресурсной моделью.

```markdown
## Operating Model Canvas (Amazon MOALS)

### Mechanisms (How Work Gets Done)
| Process | Owner | Frequency | Dependency | Automate? |
|---------|-------|-----------|------------|-----------|
| [Weekly business review] | [Role] | Weekly | [Systems] | ✓/✗ |
| [Launch readiness review] | [Role] | Per launch | [Checklist] | ✓/✗ |
| [Risk escalation] | [Role] | On trigger | [Alert system] | ✓/✗ |

### Outputs (What Gets Produced)
- **North Star Output**: [Customer gets X in Y seconds]
- **Leading Outputs**: [Weekly actives, NPS, feature adoption]
- **Artifact Outputs**: [Weekly metrics doc, monthly QBR deck]

### Actions (Decisions Made Regularly)
| Decision Type | Owner | Frequency | Kill Criteria |
|--------------|-------|-----------|---------------|
| Go/No-Go on Wave 2 | [PM] | After Wave 1 | [Adoption < X%] |
| Pivot to Plan B | [CEO] | Monthly review | [CAC > $X, LTV < $Y] |
| Resource reallocation | [VP] | Quarterly | [Velocity < X story points] |

### Learning (How We Improve)
- **Experimentation cadence**: [X A/B tests per week]
- **Failure review**: [Post-mortem after each Wave]
- **Metric evolution**: [How metrics change as we learn]

### Systems (Technical Infrastructure)
- **Data systems**: [Analytics stack for metric tracking]
- **Alerting systems**: [Threshold monitoring for pivot triggers]
- **Feedback loops**: [User research → Feature backlog]
```

**Пример Oracle**: Каждый major product concept документирует "Operating Rhythm" — как будет происходить Weekly Business Review (WBR), что смотрят, кто принимает решения, когда pivot.

**Пример Google**: OKR не просто метрики, а часть Operating Model — check-in frequency, scoring process, re-allocation triggers.

---

### 1.3 Working Backwards (Amazon PRFAQ) vs Product Vision

**Что есть**: Vision Statement + Problem Space.
**Что НЕ хватает**: Документ, написанный **из будущего**, описывающий успех как уже случившийся.

```markdown
## PRFAQ (Press Release + FAQ) — Working Backwards Document

### Press Release (Written from Launch Day)

**[CITY], [LAUNCH DATE] — [COMPANY] today announced [PRODUCT]...**

[Customer quote]: "Before [product], I [pain]. Now I [gain]."

**Key capabilities**:
- [Capability 1] — [Customer benefit]
- [Capability 2] — [Customer benefit]

**Availability**: [Pricing, launch date, how to access]

---

### FAQ (Anticipated Questions)

#### External FAQ (Customer/Press)
**Q: How is this different from [competitor]?**
A: [Differentiation with customer-visible proof]

**Q: What does this cost?**
A: [Pricing with value justification]

**Q: When can I use it?**
A: [Rollout plan with early access details]

#### Internal FAQ (Exec/Board)
**Q: Why now? Why not 6 months ago or 6 months later?**
A: [Market timing, enabling tech, competitive window]

**Q: What's the business model?**
A: [Unit economics, payback period, scaling path]

**Q: What could kill this?**
A: [Risks that would invalidate thesis + mitigations]

**Q: What resources are required?**
A: [Team size, budget, timeline, opportunity cost]

**Q: What's the exit criteria if it fails?**
A: [Kill criteria with financial thresholds]
```

**Amazon standard**: Каждый концепт > $1M investment начинается с 6-page PRFAQ. Если не можешь написать убедительный customer quote из будущего — не понимаешь customer problem достаточно глубоко.

---

### 1.4 Jobs-to-be-Done (JTBD) Integration с Willingness-to-Pay

**Что есть**: JTBD framework per persona, WTP assessment.
**Что НЕ хватает**: Калибровка WTP к фактическим расходам, связка с unit economics.

```markdown
## Value-Based Pricing Framework (Linked to JTBD)

### Persona WTP Calibration
| Persona | Current Spend | Pain Severity | Alt Solutions | Our WTP Estimate | Confidence |
|---------|--------------|--------------|---------------|------------------|------------|
| Marketing Mgr | $500/mo (3 tools) | 8/10 | Manual work 10h/mo | $300/mo | High |
| CTO | $2000/mo | 6/10 | Build in-house | $800/mo | Medium |

### Unit Economics per Persona
| Persona | CAC | LTV (3yr) | Payback | Gross Margin | NRR Target |
|---------|-----|-----------|---------|--------------|------------|
| Marketing Mgr | $200 | $10,800 | 0.7mo | 85% | 120% |
| CTO | $800 | $28,800 | 1.2mo | 90% | 110% |

### Value Metric Selection
**Our value metric**: [Per seat / Per usage / Per outcome]
**Why this metric**: [Aligns with customer perception of value]
**Pricing tiers**:
- **Starter** ($X/mo): [JTBD coverage: functional only]
- **Professional** ($Y/mo): [JTBD coverage: + emotional (status, ease)]
- **Enterprise** ($Z/mo): [JTBD coverage: + social (compliance, team)]

### Pricing Confidence
- [ ] Validated with ≥5 customers per segment
- [ ] Tested with Van Westendorp PSM (Price Sensitivity Meter)
- [ ] Competitive pricing benchmarked
- [ ] Anchoring strategy defined (vs alternatives)
```

**Google Cloud standard**: Каждый product concept включает "Customer Economic Model" — сколько клиент тратит сейчас, сколько сэкономит/заработает с нашим продуктом, какой payback period приемлем для категории buyer.

---

### 1.5 Ecosystem & Partnership Strategy (Oracle/Microsoft Partner Motion)

**Что есть**: Integration Complexity table.
**Что НЕ хватает**: Стратегия партнёрской экосистемы как драйвера роста.

```markdown
## Ecosystem Strategy Canvas

### Partner Categories
| Category | Strategic Role | Examples | Value Exchange |
|----------|---------------|----------|----------------|
| **Tech Partners** | Enable core capability | [AWS, Stripe] | [We pay fees, get infrastructure] |
| **Distribution Partners** | Reach new segments | [Consultancies] | [Revenue share, co-marketing] |
| **ISV Partners** | Extend platform | [App developers] | [Marketplace fees, data access] |
| **Co-Sell Partners** | Joint GTM | [Microsoft CSP] | [Lead sharing, deal reg] |

### Marketplace Strategy (if applicable)
- **Target marketplaces**: [AWS Marketplace, Azure Marketplace, Salesforce AppExchange]
- **Listing strategy**: [BYOL / Consumption-based / SaaS contract]
- **Marketplace economics**: [Revenue share: X%, benefits: Co-sell, procurement ease]

### Integration Roadmap
| Partner | Integration Type | Wave | Strategic Value | Effort | Priority |
|---------|-----------------|------|-----------------|--------|----------|
| Salesforce | Native embed | Wave 2 | TAM expansion | High | P1 |
| Slack | OAuth + Webhook | Wave 3 | Engagement +30% | Low | P2 |

### Partner Incentives
- **For Tech Partners**: [API volume, brand association]
- **For Channel Partners**: [Margin: X%, MDF budget, training]
- **For ISVs**: [API access, rev share, co-marketing]
```

**Oracle standard**: Каждый Cloud product concept включает "Partner GTM Strategy" — без channel partners большинство enterprise-продуктов не взлетят. Документ описывает partner economics, enablement plan, conflict resolution.

**Microsoft example**: Azure Industry Clouds построены вокруг ISV ecosystems. Концепты без ecosystem strategy не утверждаются.

---

## 2. Investment-Grade Analysis: What VCs/Boards Expect

### 2.1 Investment Thesis (One-Pager for Board)

**Что есть**: Market Opportunity (TAM/SAM/SOM).
**Что НЕ хватает**: **Инвестиционное обоснование** — почему ЭТОТ проект лучше альтернативных вложений капитала.

```markdown
## Investment Thesis (Board-Ready)

### The Opportunity
**Market inefficiency**: [What's broken in the market that creates value capture opportunity]
**Enabling factors**: [Tech/regulatory/behavioral shifts that make NOW the right time]
**Market structure**: [$[X]B TAM growing at Y% CAGR, fragmented/winner-take-all]

### Our Advantage
**Moat type**: [Network effects / Switching costs / Data moat / Brand]
**Moat strength timeline**: [Years until competitors replicate]
**Defensibility proof**: [Why this is hard to copy]

### Financial Case
| Metric | Year 1 | Year 2 | Year 3 | Assumptions |
|--------|--------|--------|--------|-------------|
| Revenue | $[X]M | $[Y]M | $[Z]M | [Growth rate: X%] |
| Gross Margin | [%] | [%] | [%] | [Scaling effects] |
| EBITDA | $[X]M | $[Y]M | $[Z]M | [Breakeven: Month X] |
| CAC | $[X] | $[Y] | $[Z] | [Improving via: ...] |
| LTV/CAC | [X]× | [Y]× | [Z]× | [Target: >3×] |
| Payback | [X]mo | [Y]mo | [Z]mo | [Target: <12mo] |

### Capital Required vs Returns
- **Investment ask**: $[X]M over [Y] months
- **Use of funds**: [50% eng, 30% GTM, 20% ops]
- **Expected return**: $[Z]M ARR by Year 3 → [X]× multiple
- **Opportunity cost**: [Comparison with alternative investments]

### Exit Scenarios
| Scenario | Probability | Outcome | Timeline |
|----------|:----------:|---------|----------|
| **Base case** | 50% | $[X]M ARR, strategic exit | 3-4 years |
| **Upside case** | 30% | $[Y]M ARR, IPO path | 4-5 years |
| **Downside case** | 20% | Acquihire or shutdown | 2 years |

### Risk-Adjusted NPV
**Discount rate**: [X]% (reflecting risk profile)
**NPV**: $[X]M
**IRR**: [Y]%
**Comparison**: [Industry benchmark IRR for this risk tier]
```

**Amazon standard**: Каждый major bet (> $10M) представляется как "S-Team paper" с финансовым моделированием на 3-5 лет, NPV, сравнением с альтернативными проектами в портфеле.

**VC standard (a16z, Sequoia)**: Seed/Series A memos включают Total Addressable Outcome (TAO) — сколько можно вернуть на вложенный доллар в разных сценариях.

---

### 2.2 Sensitivity Analysis & Scenario Planning

**Что есть**: Risk matrix (Likelihood × Impact).
**Что НЕ хватает**: Количественная оценка влияния рисков на финансы, стресс-тесты.

```markdown
## Financial Sensitivity Analysis

### Key Assumptions Sensitivity
| Variable | Base Case | Downside (-20%) | Upside (+20%) | ARR Impact (Y3) |
|----------|-----------|-----------------|---------------|-----------------|
| Conversion rate | 10% | 8% | 12% | $[X]M → $[Y]M |
| ARPU | $100/mo | $80/mo | $120/mo | $[X]M → $[Y]M |
| Churn rate | 5%/mo | 6%/mo | 4%/mo | $[X]M → $[Y]M |
| CAC | $200 | $240 | $160 | Payback: [X]mo → [Y]mo |

### Break-Even Scenarios
| Scenario | Revenue Req. | CAC Ceiling | Churn Ceiling | Timeline to BEP |
|----------|-------------|-------------|---------------|-----------------|
| **Optimistic** | $[X]M/mo | $[Y] | [Z]% | Month 18 |
| **Base** | $[X]M/mo | $[Y] | [Z]% | Month 24 |
| **Pessimistic** | $[X]M/mo | $[Y] | [Z]% | Month 36 |

### Monte Carlo Simulation (if applicable)
- **Variables modeled**: [Conversion, churn, ARPU, CAC]
- **Distribution**: [Normal / Log-normal / Custom]
- **Outcome**: [90% confidence: ARR between $[X]M and $[Y]M]
```

**Google Ventures standard**: Спринты включают "Assumptions Mapping" — какие предположения должны быть верны для успеха, как их валидировать дёшево, что случится если они неверны.

---

### 2.3 Strategic Options Analysis (Real Options Valuation)

**Что есть**: Один концепт, одна линейная стратегия.
**Что НЕ хватает**: Опционное мышление — какие будущие опции создаёт этот проект?

```markdown
## Strategic Options Created by This Concept

### Option 1: Platform Play
**Trigger**: If adoption > [X] users by Month 12
**Value**: Opens $[Y]M marketplace/ecosystem opportunity
**Investment to exercise**: $[Z]M (API platform development)
**Decision point**: Month 12 review
**Option value**: [Black-Scholes estimate if quantifiable]

### Option 2: Adjacent Vertical Expansion
**Trigger**: If NPS > 50 in beachhead segment
**Value**: 3× TAM expansion into [adjacent industry]
**Investment to exercise**: $[Z]M (vertical customization)
**Decision point**: Month 18 review

### Option 3: Enterprise Tier Launch
**Trigger**: If ≥5 customers request SSO/SAML
**Value**: ARPU uplift from $[X] to $[Y] (5× increase)
**Investment to exercise**: $[Z]M (enterprise features)
**Decision point**: On-demand (customer-driven)

### Option 4: Acquihire Exit
**Trigger**: If core tech valuable but GTM not scaling
**Value**: $[X]M based on team size/tech IP
**Investment to exercise**: $0 (exit)
**Decision point**: Month 24 if growth < [threshold]

### Options Portfolio Value
**Total embedded options value**: $[X]M (NPV of exercisable options)
**Optionality premium**: [X]% of base case valuation
```

**Amazon standard**: "One-way doors vs two-way doors". Two-way door decisions делаются быстро (reversible). One-way doors требуют анализа long-term optionality.

**Microsoft example**: GitHub acquisition ($7.5B) оценивалась не только по текущей выручке, но по опциям: developer data, AI training data, enterprise upsell, cloud migration catalyst.

---

## 3. Scenario Planning: Handling Uncertainty

### 3.1 Future Scenarios Framework (Shell Method)

**Что есть**: Single baseline forecast.
**Что НЕ хватает**: Multiple plausible futures с разными стратегиями для каждого.

```markdown
## Scenario Planning Matrix (2×2 Framework)

### Critical Uncertainties (Axes)
- **Axis 1 (Horizontal)**: [Market adoption speed — Fast vs Slow]
- **Axis 2 (Vertical)**: [Competitive intensity — High vs Low]

### Four Scenarios

#### Scenario A: "Land Grab" (Fast Adoption, Low Competition)
- **Probability**: 15%
- **Market dynamics**: [Viral growth, network effects kick in]
- **Our strategy**: Maximize growth, sacrifice margins, land grab
- **Metrics to track**: [User growth rate, viral coefficient]
- **Trigger signals**: [Week-over-week growth > X%]

#### Scenario B: "Red Ocean" (Fast Adoption, High Competition)
- **Probability**: 35%
- **Market dynamics**: [Category validated, many entrants, price war]
- **Our strategy**: Differentiate aggressively, build moat fast
- **Metrics to track**: [Competitive win rate, feature parity gaps]
- **Trigger signals**: [New funded competitor every month]

#### Scenario C: "Marathon" (Slow Adoption, Low Competition)
- **Probability**: 30%
- **Market dynamics**: [Education required, patient capital]
- **Our strategy**: Efficiency focus, extend runway, strategic partnerships
- **Metrics to track**: [CAC payback, burn multiple]
- **Trigger signals**: [Conversion rates < X%, long sales cycles]

#### Scenario D: "Graveyard" (Slow Adoption, High Competition)
- **Probability**: 20%
- **Market dynamics**: [Market not ready, too many players chasing small pie]
- **Our strategy**: Pivot or exit, cut losses
- **Metrics to track**: [Market share shrinkage, funding runway]
- **Trigger signals**: [Churn > X%, negative word-of-mouth]

### Early Warning Indicators (Next 6 Months)
| Indicator | Scenario A | Scenario B | Scenario C | Scenario D |
|-----------|-----------|-----------|-----------|-----------|
| Weekly active users | [Threshold] | [Threshold] | [Threshold] | [Threshold] |
| Competitor count | [Threshold] | [Threshold] | [Threshold] | [Threshold] |
| Media mentions | [Threshold] | [Threshold] | [Threshold] | [Threshold] |

### Scenario Review Cadence
- **Monthly**: Track leading indicators, update probabilities
- **Quarterly**: Reassess scenario fit, adjust strategy if needed
- **Annually**: Rebuild scenarios with new uncertainties
```

**Shell Oil standard**: Стратегии разрабатываются для 3-4 plausible futures (не forecasts), каждая с early warning signals. Это то, как Shell предсказал нефтяной кризис 1973.

**Microsoft example**: Cloud strategy строилась на сценариях "AWS dominates" vs "Multi-cloud wins" vs "Hybrid wins" — разные сценарии требовали разных продуктовых инвестиций.

---

### 3.2 Pre-Mortem Analysis

**Что есть**: Risk assessment (что может пойти не так).
**Что НЕ хватает**: **Pre-mortem** — представь, что проект FAILED, опиши почему.

```markdown
## Pre-Mortem Exercise (Failure Analysis)

### Setup
**Date**: [Today]
**Imagined failure date**: [18 months from now]
**Prompt**: "It's [date]. This project is dead. What killed it?"

### Failure Scenarios (Ranked by Likelihood)

#### Failure #1: "Market Didn't Exist" (35% probability)
**What happened**: We built great product, but pain not severe enough for users to switch
**Root causes**:
- TAM calculation was top-down, not validated bottom-up
- Users had cheap workarounds we didn't discover
- Buying process too complex (legal/procurement blockers)

**Could we have known earlier?**:
- [ ] Tested willingness-to-pay with real contracts (not surveys)
- [ ] Tracked conversion from trial → paid (not just signups)
- [ ] Interviewed churned users within 7 days

**Prevention now**:
- Add "paid pilot" requirement before Wave 2 investment
- Set kill threshold: If conversion < X% after 100 trials, pivot

#### Failure #2: "Competitor Crushed Us" (25% probability)
**What happened**: Incumbent launched similar feature, free
**Root causes**:
- Underestimated how easy our feature is to replicate
- No proprietary data/network effect moat
- Incumbent had distribution advantage (bundling)

**Could we have known earlier?**:
- [ ] War-gamed competitor response (what would WE do if competitor?)
- [ ] Analyzed their strategic incentives to compete
- [ ] Built relationship moats (integrations, partnerships) early

**Prevention now**:
- Prioritize integration partnerships in Wave 1 (lock-in)
- Build data moat feature (proprietary dataset from usage)

#### Failure #3: "Execution Death March" (20% probability)
**What happened**: Took 2× longer than planned, team burned out, ran out of money
**Root causes**:
- Wave 1 foundations harder than estimated (technical debt)
- Scope creep from early customers ("just one more feature")
- Key engineer left, knowledge loss

**Could we have known earlier?**:
- [ ] Time-boxed Wave 1 with hard scope freeze
- [ ] Tracked velocity vs plan weekly (not just at milestones)
- [ ] Built redundancy for critical skills

**Prevention now**:
- Set Wave 1 deadline with 30% buffer
- Document all architectural decisions (reduce bus factor)

### Aggregate Pre-Mortem Insights
**Most likely failure mode**: [Market risk]
**Mitigation priority**: [Add validation experiments in Wave 1]
**Kill criteria update**: [If conversion < X%, kill before Wave 2]
```

**Google standard**: Pre-mortems перед major launches. Команду просят представить failure и описать причины — выявляет blind spots лучше, чем "что может пойти не так?".

---

## 4. Strategic Alternatives: Presenting Options with Trade-offs

### 4.1 Strategic Alternatives Canvas (Not Just "This Concept")

**Что есть**: Один концепт.
**Что НЕ хватает**: Сравнение этого концепта с **альтернативными стратегическими направлениями** (включая "do nothing").

```markdown
## Strategic Alternatives Analysis

### Alternative 1: This Concept (Primary)
**Description**: [As defined in current concept.md]
**Strategic intent**: [Horizon X, Y% of portfolio]
**Investment**: $[X]M over [Y] months
**Expected return**: $[Z]M ARR by Year 3
**Risk profile**: [High/Medium/Low]
**Key assumption**: [If wrong, project fails]

### Alternative 2: Build Smaller MVP (Conservative)
**Description**: [Same vision, but only Wave 1 + 1 key Wave 2 feature]
**Strategic intent**: Test market with minimal investment
**Investment**: $[X]M over [Y] months (50% of Alt 1)
**Expected return**: $[Z]M ARR by Year 3 (60% of Alt 1)
**Risk profile**: Lower risk, lower upside
**Key assumption**: Market validates quickly enough
**Trade-off**: Slower time-to-market, risk competitor moves first

### Alternative 3: Partner Instead of Build
**Description**: White-label existing solution, brand as ours
**Strategic intent**: Test distribution before investing in product
**Investment**: $[X]M (80% lower CAPEX, higher OPEX)
**Expected return**: $[Z]M ARR (worse margins, faster launch)
**Risk profile**: Low product risk, high partner dependency risk
**Key assumption**: Partner relationship stable
**Trade-off**: Give up product IP, vendor lock-in, margin compression

### Alternative 4: Do Nothing (Baseline)
**Description**: Continue current trajectory, don't build this
**Strategic intent**: Preserve capital for other opportunities
**Investment**: $0
**Expected return**: $0 direct, but [X]% growth in core business
**Risk profile**: Zero project risk, opportunity cost risk
**Key assumption**: Market window doesn't close
**Trade-off**: Competitor captures market, future entry harder

### Decision Matrix

| Criterion | Weight | Alt 1 (This) | Alt 2 (MVP) | Alt 3 (Partner) | Alt 4 (Nothing) |
|-----------|:------:|:------------:|:-----------:|:---------------:|:---------------:|
| **Strategic fit** | 25% | 9 | 7 | 5 | 3 |
| **Financial return** | 20% | 8 | 6 | 5 | 2 |
| **Risk** (inverse) | 15% | 5 | 7 | 6 | 9 |
| **Speed to market** | 15% | 6 | 8 | 9 | 0 |
| **Defensibility** | 10% | 9 | 7 | 3 | 0 |
| **Team capability** | 10% | 7 | 8 | 9 | 10 |
| **Optionality** | 5% | 9 | 6 | 4 | 2 |
| **Weighted Score** | | **7.35** | **6.95** | **5.75** | **3.15** |

### Recommendation
**Primary recommendation**: Alternative 1 (This Concept)
**Rationale**: [Highest strategic fit and optionality value, acceptable risk]
**Hedge**: De-risk with Alternative 2 approach for first 6 months (smaller Wave 1), then re-evaluate
**Re-evaluation trigger**: If [metric] < [threshold] by Month 6, pivot to Alt 3 or 4
```

**BCG standard**: Strategy papers всегда включают "Path Not Taken" — альтернативные стратегии с trade-offs. Это заставляет эксплицитно выбирать, а не дефолтить на "первую идею".

**Amazon standard**: "Type 1 decisions" (one-way doors) требуют comparison with alternatives. "Disagree and commit" возможен только если альтернативы явно рассмотрены.

---

### 4.2 Build vs Buy vs Partner Decision Framework

**Что есть**: Описание того, что строим.
**Что НЕ хватает**: Обоснование **почему строим сами**, а не покупаем/партнёримся.

```markdown
## Build vs Buy vs Partner Analysis

### Build (This Concept)
**Pros**:
- [ ] Full control over roadmap and customer experience
- [ ] Proprietary IP and competitive differentiation
- [ ] Margins not eroded by vendor fees

**Cons**:
- [ ] High upfront CAPEX ($[X]M)
- [ ] Longer time-to-market ([X] months)
- [ ] Execution risk (team, tech, timeline)

**Total cost (3yr)**: $[X]M CAPEX + $[Y]M OPEX = $[Z]M
**Defensibility**: High (own IP)

### Buy (Acquire Existing Solution)
**Candidates**: [Startup A ($[X]M valuation), Startup B ($[Y]M valuation)]

**Pros**:
- [ ] Instant market entry (0-3 months)
- [ ] Proven product-market fit (if choosing right target)
- [ ] Acquire team and customer base

**Cons**:
- [ ] High upfront cost ($[X]M acquisition)
- [ ] Integration complexity (tech debt, culture)
- [ ] Overpay risk (valuation bubble)

**Total cost (3yr)**: $[X]M acquisition + $[Y]M integration = $[Z]M
**Defensibility**: Medium (acquirable by others too)

### Partner (White-Label / Resell)
**Candidates**: [Platform A (rev share: X%), Platform B (license: $Y/mo)]

**Pros**:
- [ ] Fastest time-to-market (1-2 months)
- [ ] Low upfront cost ($[X]K)
- [ ] Low execution risk (vendor handles product)

**Cons**:
- [ ] Vendor lock-in and dependency risk
- [ ] Margin compression (give [X]% to partner)
- [ ] Limited differentiation (same as vendor's other partners)

**Total cost (3yr)**: $[X]K setup + $[Y]M rev share = $[Z]M
**Defensibility**: Low (partner can go direct)

### Decision Scorecard

| Factor | Build | Buy | Partner | Winner |
|--------|:-----:|:---:|:-------:|--------|
| Strategic control | ✓+ | ✓ | ✗ | Build |
| Time to market | ✗ | ✓ | ✓+ | Partner |
| Upfront cost | ✗ | ✗✗ | ✓+ | Partner |
| Long-term margin | ✓+ | ✓ | ✗ | Build |
| Defensibility | ✓+ | ✓ | ✗ | Build |
| **Total** | **3 wins** | **1 win** | **2 wins** | **Build** |

### Recommendation
**Choice**: Build (this concept)
**Why**: Strategic control and defensibility outweigh time/cost trade-offs
**Hedge**: If acquisition target becomes available at <$[X]M, re-evaluate Buy option
**Validation gate**: After 6mo, if build velocity < [X]% of plan, re-evaluate Partner option
```

**Microsoft standard**: Cloud acquisitions (GitHub, Nuance, etc.) всегда документируют "Why buy vs build?" — часто строят параллельно (hedge) и оценивают через 6-12 мес.

---

## 5. Execution Readiness: Signals for Investment

### 5.1 Investment Readiness Scorecard (Y Combinator / Sequoia Style)

**Что есть**: CQS (Concept Quality Score) для внутренней валидации.
**Что НЕ хватает**: **Investor-grade readiness** — что нужно для external funding или internal capital allocation.

```markdown
## Investment Readiness Scorecard

### Market Validation (30 points)
| Criterion | Score | Evidence |
|-----------|:-----:|----------|
| **Problem validated** | /10 | [X customer interviews confirm pain > 8/10] |
| **Solution validated** | /10 | [Prototype tested with Y users, NPS > Z] |
| **Market sized** | /10 | [TAM/SAM/SOM with bottom-up validation] |
| **Subtotal** | /30 | |

### Team Readiness (20 points)
| Criterion | Score | Evidence |
|-----------|:-----:|----------|
| **Domain expertise** | /7 | [Founder/PM has X years in industry] |
| **Technical capability** | /7 | [CTO has built similar systems] |
| **GTM experience** | /6 | [VP Sales has X ARR experience] |
| **Subtotal** | /20 | |

### Traction (20 points)
| Criterion | Score | Evidence |
|-----------|:-----:|----------|
| **Early revenue** | /7 | [$X MRR or $Y pilot contracts] |
| **User engagement** | /7 | [DAU/MAU ratio > X%, retention > Y%] |
| **Growth rate** | /6 | [Month-over-month growth > X%] |
| **Subtotal** | /20 | |

### Competitive Position (15 points)
| Criterion | Score | Evidence |
|-----------|:-----:|----------|
| **Differentiation** | /7 | [Clear moat: network effects/data/brand] |
| **Defensibility** | /8 | [X years until competitors replicate] |
| **Subtotal** | /15 | |

### Economics (15 points)
| Criterion | Score | Evidence |
|-----------|:-----:|----------|
| **Unit economics** | /7 | [LTV/CAC > 3×, payback < 12mo] |
| **Margin structure** | /8 | [Gross margin > X%, path to Y% EBITDA] |
| **Subtotal** | /15 | |

### Total Investment Readiness Score: /100

### Funding Thresholds
- **80-100**: Ready for Series A ($[X]M+), strong institutional interest
- **60-79**: Ready for Seed ($[Y]M), angel/pre-seed funds
- **40-59**: Not ready, need more validation (friends & family only)
- **<40**: Concept stage, grant/accelerator funding only

### Current Status: [Score]/100 — [Funding stage readiness]

### Gaps to Close for Next Stage
1. [Gap 1]: [Action to close gap] — [Timeline]
2. [Gap 2]: [Action to close gap] — [Timeline]
```

**Y Combinator standard**: Batch applications оцениваются по Founder/Market/Product/Traction. Concept без traction принимается только если founder exceptionally strong.

**Sequoia standard**: "Why now?" slide обязателен — market timing и enabling factors должны быть articulated.

---

### 5.2 Execution Confidence Matrix

**Что есть**: Wave-based execution plan.
**Что НЕ хватает**: **Confidence levels** по каждой критической зависимости.

```markdown
## Execution Confidence Assessment

### Critical Path Analysis
| Wave | Dependency | Confidence | Evidence | Mitigation if Low |
|------|-----------|:----------:|----------|-------------------|
| Wave 1 | Team can hire [role] | 🟢 High | [Pipeline: X candidates] | [Contractor backup] |
| Wave 1 | AWS API stable | 🟢 High | [Used in prod for Y years] | [Fallback to Z] |
| Wave 2 | Users adopt feature X | 🟡 Medium | [Prototype NPS: 40/100] | [A/B test, pivot if <30] |
| Wave 2 | Integration with [platform] | 🔴 Low | [No API docs, beta only] | [Manual workaround Wave 2] |

### Confidence Definitions
- 🟢 **High (80-100%)**: Validated, low risk, fallback exists
- 🟡 **Medium (50-79%)**: Unvalidated but reasonable, can mitigate
- 🔴 **Low (<50%)**: High risk, no clear mitigation, could block project

### Red Flag Dependencies (Confidence < 50%)
1. **[Dependency name]**:
   - **Risk**: [What happens if this fails]
   - **Mitigation**: [Plan A, Plan B]
   - **Validation plan**: [How to de-risk in next 30 days]
   - **Kill criteria**: [If still low confidence by Month X, pivot]

### Execution Readiness Verdict
- **Green flags**: [X/Y critical dependencies high confidence]
- **Yellow flags**: [X/Y medium confidence — acceptable]
- **Red flags**: [X/Y low confidence — BLOCK until resolved]

**Recommendation**:
- [ ] ✅ Proceed immediately (all greens)
- [ ] ⚠️ Proceed with caution (some yellows, no reds)
- [ ] ⛔ Do not proceed (reds present, must de-risk first)
```

**Google standard**: Project approval требует "Confidence levels" по каждой критической hypothesis. Low-confidence hypotheses требуют validation experiments перед greenlight.

---

### 5.3 Capital Allocation Framework (Portfolio View)

**Что есть**: Investment ask для этого проекта.
**Что НЕ хватает**: **Портфельный контекст** — как этот проект конкурирует с другими за капитал.

```markdown
## Capital Allocation Portfolio Context

### Current Portfolio (Competing Projects)
| Project | Horizon | Investment | Expected Return | IRR | Risk | Status |
|---------|---------|-----------|-----------------|-----|------|--------|
| **This Concept** | H2 | $[X]M | $[Y]M ARR (Y3) | [Z]% | Med | Proposed |
| Project Alpha | H1 | $[X]M | $[Y]M ARR (Y3) | [Z]% | Low | Approved |
| Project Beta | H2 | $[X]M | $[Y]M ARR (Y3) | [Z]% | High | Under review |
| Project Gamma | H3 | $[X]M | $[Y]M ARR (Y3) | [Z]% | High | Proposed |

### Portfolio Balance (Current)
| Horizon | % of Budget | Target % | Delta |
|---------|------------|----------|-------|
| H1 (Defend) | 60% | 60% | ✓ On target |
| H2 (Extend) | 25% | 30% | ⚠️ Under-allocated |
| H3 (Create) | 15% | 10% | ⚠️ Over-allocated |

### Portfolio Balance (After This Project)
| Horizon | % of Budget | Target % | Delta |
|---------|------------|----------|-------|
| H1 (Defend) | 55% | 60% | ⚠️ Slightly under |
| H2 (Extend) | 35% | 30% | ✓ Better balance |
| H3 (Create) | 10% | 10% | ✓ On target |

### Strategic Rationale for Allocation
**Why fund THIS vs alternatives**:
- [ ] Fills H2 gap in portfolio (extend strategy under-allocated)
- [ ] Higher IRR than Project Beta (X% vs Y%)
- [ ] Lower risk than Project Gamma (Medium vs High)
- [ ] Enables future optionality (Platform play in Year 2)

### Opportunity Cost
**If we fund this**, we CANNOT fund:
- Project Delta ($[X]M, IRR [Y]%, Risk [Low/Med/High])
- **Comparison**: [Why THIS is better use of capital]

### Capital Efficiency
| Metric | This Concept | Portfolio Avg | Best in Portfolio |
|--------|-------------|--------------|-------------------|
| IRR | [X]% | [Y]% | [Z]% |
| Payback (months) | [X] | [Y] | [Z] |
| Risk-adjusted return | [X] | [Y] | [Z] |
| Capital efficiency | $[X] invested per $1 ARR | [Y] | [Z] |
```

**Amazon standard**: S-Team reviews всегда включают portfolio view — как этот bet соотносится с другими bets в том же Horizon, какой trade-off делается.

**Microsoft example**: Satya Nadella's "mobile-first, cloud-first" strategy означала явное **re-allocation** капитала из Windows/Office (H1) в Azure/M365 (H2) и AI (H3).

---

## Summary: Priority Gaps to Close

### TIER 1 (Critical for Board-Level Credibility)
1. **Investment Thesis One-Pager**: Почему ЭТОТ проект — лучший use of capital vs alternatives
2. **Strategic Alternatives Canvas**: Сравнение Build vs Buy vs Partner vs Do Nothing
3. **Financial Sensitivity Analysis**: Стресс-тесты assumptions, break-even scenarios
4. **Three Horizons Classification**: Где этот проект в portfolio (H1/H2/H3)
5. **Pre-Mortem Analysis**: Представь failure, опиши причины

### TIER 2 (High Value, Differentiating)
6. **PRFAQ (Working Backwards)**: Press release из будущего + FAQs
7. **Scenario Planning (2×2 Matrix)**: 4 plausible futures с разными стратегиями
8. **Strategic Options Valuation**: Какие future options создаёт проект
9. **Execution Confidence Matrix**: Red/Yellow/Green flags для critical dependencies
10. **Capital Allocation Portfolio View**: Как конкурирует с другими проектами

### TIER 3 (Nice-to-Have, Corporate Strategy Polish)
11. **MOALS/OSM Operating Model**: Mechanisms, Outputs, Actions, Learning, Systems
12. **Ecosystem Strategy Canvas**: Partner categories, marketplace strategy
13. **Value-Based Pricing (linked to JTBD)**: Unit economics per persona
14. **Investment Readiness Scorecard**: YC/Sequoia-style funding readiness

---

## Recommended Next Steps

### 1. Prototype Enhanced Template
Создать **расширенную версию** `concept-template.md` с секциями:
- Strategic Horizon Classification (Tier 1, #4)
- Investment Thesis (Tier 1, #1)
- Strategic Alternatives (Tier 1, #2)
- Financial Scenarios (Tier 1, #3)
- Pre-Mortem (Tier 1, #5)

### 2. Update `/speckit.concept` Command Flow
Добавить **новые фазы**:
- **Phase 0d: Strategic Context** — classify horizon, identify portfolio alternatives
- **Phase 5e: Investment Case** — build financial model, sensitivity, NPV
- **Phase 5f: Strategic Alternatives** — build vs buy vs partner vs do nothing
- **Phase 9b: Pre-Mortem** — imagine failure, extract mitigations

### 3. Add "Board Mode" Flag
```bash
/speckit.concept --mode=board
```
Режим для board-ready concepts (полный набор Tier 1 frameworks).

### 4. Create Reference Examples
Документировать **примеры из реальных стратегий**:
- Amazon PRFAQ example (Kindle, AWS)
- Microsoft Horizon classification (Windows/Azure/OpenAI)
- Google OKR cascade (company → product → team)
- Oracle partner economics model

---

## Conclusion

Текущий `/speckit.concept` — сильный **product management** инструмент. Чтобы стать **corporate strategy** инструментом уровня Fortune 500, нужно добавить **инвестиционное мышление**:

1. **Не "что строим"**, а **"почему это правильный стратегический выбор vs alternatives"**
2. **Не один план**, а **portfolio of scenarios с hedge strategies**
3. **Не разовый документ**, а **живая стратегия с review triggers**

Добавление 5 Tier 1 frameworks превратит spec-kit из "dev tool" в **strategic planning platform** для CEO/Board-level decision making.

---

**Файл сохранён**: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/outputs/business-strategy/agents/business-strategist/2026-01-01_concept-strategic-gaps-analysis.md`

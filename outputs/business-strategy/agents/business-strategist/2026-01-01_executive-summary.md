# Executive Summary: Strategic Gaps in /speckit.concept

**Date**: 2026-01-01
**Analyst**: Business Strategist Agent
**Purpose**: Upgrade `/speckit.concept` to Fortune 500 corporate strategy standards

---

## Ключевая проблема

`/speckit.concept` отвечает на вопрос **"ЧТО строим?"**, но не отвечает на вопрос **"ПОЧЕМУ это правильный стратегический выбор СЕЙЧАС?"**

Это отличный product management tool, но не corporate strategy framework для Board/CEO-level решений.

---

## 5 критических разрывов (Tier 1 Priority)

### 1. Investment Thesis (Amazon/Sequoia Standard)
**Чего НЕ хватает**: Обоснование, почему ЭТОТ проект — лучший use of capital vs alternatives.

**Что добавить**:
- NPV/IRR расчёт с discount rate
- Сравнение с альтернативными инвестициями в портфеле
- Expected return scenarios (base/upside/downside)
- Exit scenarios с probability weighting

**Пример Amazon**: S-Team papers включают 3-year P&L projection + сравнение с другими bets.

---

### 2. Strategic Alternatives (BCG/McKinsey Standard)
**Чего НЕ хватает**: Анализ Build vs Buy vs Partner vs Do Nothing.

**Что добавить**:
- Decision matrix: 4 alternatives с weighted scoring
- Trade-offs явно articulated (time vs cost vs control)
- Recommendation с rationale
- Hedge strategy (de-risk через smaller MVP, затем scale)

**Пример Microsoft**: GitHub acquisition ($7.5B) документировала "Why buy vs build?" с 5 alternatives.

---

### 3. Financial Sensitivity Analysis (VC Standard)
**Чего НЕ хватает**: Стресс-тесты key assumptions (conversion, churn, CAC, ARPU).

**Что добавить**:
- Sensitivity table: ±20% на key variables → impact on ARR/payback
- Break-even scenarios (optimistic/base/pessimistic)
- Monte Carlo simulation для confidence intervals
- Kill criteria с financial thresholds

**Пример a16z**: Seed memos включают "If conversion drops to X%, payback extends to Y months — still acceptable?"

---

### 4. Three Horizons Portfolio Classification (Google/McKinsey)
**Чего НЕ хватает**: Где этот проект в strategic portfolio (H1 Defend / H2 Extend / H3 Create)?

**Что добавить**:
- Horizon classification (timeframe, risk, return expectations)
- Portfolio balance view (% of R&D budget per horizon)
- Competing projects в том же Horizon
- Strategic rationale для allocation vs alternatives

**Пример Google**: OKRs cascade down from company H1/H2/H3 strategy. Проекты без Horizon-alignment не получают headcount.

---

### 5. Pre-Mortem Analysis (Google Ventures)
**Чего НЕ хватает**: Imagine project FAILED — describe why.

**Что добавить**:
- Top 3-5 failure scenarios с probability
- Root causes для каждого failure
- "Could we have known earlier?" validation tests
- Prevention actions NOW (de-risk before it's too late)

**Пример Google**: Pre-mortems перед major launches выявляют blind spots лучше, чем "what could go wrong?".

---

## Tier 2 Frameworks (High Value)

6. **PRFAQ (Amazon Working Backwards)**: Press release из будущего + customer quote + FAQs
7. **Scenario Planning (Shell 2×2 Matrix)**: 4 plausible futures с different strategies
8. **Strategic Options Valuation**: Real options created by this project (platform, adjacencies)
9. **Execution Confidence Matrix**: Red/Yellow/Green flags для critical dependencies
10. **Capital Allocation Portfolio View**: How this competes for capital vs other projects

---

## Tier 3 Frameworks (Nice-to-Have)

11. **MOALS/OSM Operating Model**: Mechanisms → Outputs → Actions → Learning → Systems
12. **Ecosystem Strategy**: Partner categories, marketplace economics, co-sell motion
13. **Value-Based Pricing (JTBD-linked)**: WTP calibration → unit economics per persona
14. **Investment Readiness Scorecard**: YC/Sequoia-style funding readiness (0-100 points)

---

## Рекомендация

### Quick Win (1-2 weeks)
Добавить **5 Tier 1 секций** в `concept-template.md`:
1. Investment Thesis (one-pager для Board)
2. Strategic Alternatives (Build vs Buy vs Partner vs Nothing)
3. Financial Scenarios (base/upside/downside с sensitivity)
4. Horizon Classification (H1/H2/H3 + portfolio context)
5. Pre-Mortem (top 3 failure scenarios + prevention)

### Medium-Term (1 month)
Добавить **Tier 2 frameworks** как опциональные секции (флаг `--mode=board`).

### Long-Term Vision
Превратить spec-kit из **dev tool** в **strategic planning platform** для CEO/Board:
- Автоматический NPV/IRR калькулятор
- Scenario modeling с Monte Carlo
- Portfolio dashboard (all concepts across Horizons)
- Decision log с review triggers

---

## Что это даст?

**Для продакт-команд**:
- Концепты, которые проходят Board review с первого раза
- Явные kill criteria (не тратим время на зомби-проекты)
- Alignment со стратегией компании

**Для CEO/Board**:
- Investment-grade documentation для capital allocation
- Сравнимость проектов (не "каждый красив по-своему")
- Confidence в execution readiness

**Для spec-kit как продукта**:
- Переход из "developer tool" в "executive tool"
- Differentiation: единственный spec tool с board-level strategy frameworks
- Upsell path: Free (basic concept) → Pro (board mode) → Enterprise (portfolio dashboard)

---

## Next Actions

1. **Review**: Обсудить Tier 1 frameworks с командой (priority / scope)
2. **Prototype**: Создать enhanced `concept-template-board.md` с Tier 1 секциями
3. **Validate**: Протестировать на реальном концепте (например, spec-kit roadmap)
4. **Document**: Создать examples из реальных стратегий (Amazon PRFAQ, Microsoft Horizon)
5. **Ship**: Выкатить как `/speckit.concept --mode=board` (beta)

---

**Полный анализ**: `2026-01-01_concept-strategic-gaps-analysis.md` (17 страниц, 50+ frameworks)

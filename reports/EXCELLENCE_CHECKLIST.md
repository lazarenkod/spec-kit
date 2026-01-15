# Excellence Checklist: Быстрая проверка качества артефактов

**Дата**: 2026-01-03
**Назначение**: Краткий чек-лист для валидации спецификаций, планов и задач

---

## 📋 Specification (PRD) Checklist

### ✅ Must-Have (Блокеры релиза)

- [ ] **Problem Statement**: Формулировка боли клиента (НЕ "отсутствует функция X")
- [ ] **User Personas + JTBD**: "Когда [ситуация], я хочу [мотивация], чтобы [результат]"
- [ ] **Success Metrics (HEART)**:
  - [ ] North Star Metric определена
  - [ ] 2-4 Input Metrics с текущими/целевыми значениями
  - [ ] Измеримые KPI с дедлайнами
- [ ] **Acceptance Criteria**: 2-5 testable criteria на каждую функцию
- [ ] **Edge Cases**: 5-10 сценариев обработки ошибок
- [ ] **Non-Functional Requirements**: Performance, Security, Scalability, Availability
- [ ] **Out of Scope**: Четко указано, что НЕ включено

### ⚠️ Common Anti-Patterns (Избегать)

- ❌ Vagueness: "Продукт должен быть простым" → ✅ "Онбординг завершается за < 5 мин"
- ❌ Solutions Without Problems: Начинать с "Нужна функция X" → ✅ "Проблема: Пользователи..."
- ❌ No Metrics: Нет KPI для оценки успеха → ✅ HEART framework + North Star
- ❌ Ignoring Edge Cases: Только happy path → ✅ Error handling section
- ❌ Static Document: Написали и забыли → ✅ Версионирование + change log

### 🌟 Excellence Indicators

- [ ] **Amazon Working Backwards**: Есть пресс-релиз для клиентов
- [ ] **Airbnb 11-Star**: Определен 7-9★ опыт (не только 5★)
- [ ] **Validated with Users**: Prototype testing с ≥5 пользователями
- [ ] **Living Document**: Change log показывает регулярные обновления

---

## 🗺️ Implementation Plan Checklist

### ✅ Must-Have

- [ ] **Architecture (RFC-style)**:
  - [ ] High-level design diagram
  - [ ] API contracts (OpenAPI/Swagger)
  - [ ] Database schema changes
  - [ ] Alternatives considered (почему rejected)
- [ ] **RACI Matrix**: Для каждой ключевой задачи ровно 1 Accountable
- [ ] **Dependency Map**: Internal + external dependencies + blockers
- [ ] **Pre-Mortem Analysis**:
  - [ ] Топ 5-10 failure modes идентифицированы
  - [ ] Risk Score = Impact × Likelihood
  - [ ] Mitigation strategy для топ-3 рисков
- [ ] **Rollout Plan**:
  - [ ] Phasing: Internal Beta → Canary (5%) → Gradual (25% → 50% → 100%)
  - [ ] Rollback criteria (error rate, latency thresholds)

### ⚠️ Common Anti-Patterns

- ❌ Over-Optimistic Estimates: Нет buffer → ✅ Добавить 20-30%
- ❌ No Risk Mitigation: Риски без планов → ✅ Action plan + Owner для каждого
- ❌ Unclear Ownership: Несколько Accountable → ✅ RACI: ровно 1 A
- ❌ Ignoring Dependencies: Нет dependency map → ✅ Critical path analysis
- ❌ Big Bang Release: Все сразу 100% → ✅ Gradual rollout

### 🌟 Excellence Indicators

- [ ] **McKinsey Value vs Complexity Matrix**: Приоритизация Quick Wins
- [ ] **Critical Path**: Определена longest dependency chain
- [ ] **Pre-Mortem Completed**: С участием cross-functional team
- [ ] **Feature Flags**: Готовы для gradual rollout

---

## ✅ Task Breakdown Checklist

### ✅ Must-Have (INVEST Criteria)

Каждая user story проходит INVEST:

- [ ] **I - Independent**: Можно разработать независимо от других историй
- [ ] **N - Negotiable**: Без технических деталей, оставляет пространство команде
- [ ] **V - Valuable**: Приносит ценность пользователю (не "Refactor DB layer")
- [ ] **E - Estimable**: Команда может оценить (достаточно деталей)
- [ ] **S - Small**: Завершается за 1 итерацию (≤13 story points)
- [ ] **T - Testable**: 2-5 acceptance criteria определяют "done"

### ✅ Definition of Done (Universal для команды)

- [ ] **Code Quality**:
  - [ ] Code review ≥1 approval
  - [ ] Linting passing
  - [ ] No code smells (SonarQube)
- [ ] **Testing**:
  - [ ] Unit tests ≥80% coverage
  - [ ] Integration tests passing
  - [ ] QA sign-off (no P0/P1 bugs)
- [ ] **Security**: Security scan passed (0 critical CVEs)
- [ ] **Documentation**: API docs updated
- [ ] **Deployment**: Feature flag + rollback plan

### ⚠️ Common Anti-Patterns

- ❌ Too Large: Story > 1 sprint → ✅ Разбить epic (8 splitting patterns)
- ❌ Vague AC: "Должно работать хорошо" → ✅ "Response time < 200ms при 1000 RPS"
- ❌ Dependent Stories: Story A блокирует Story B → ✅ Независимость через splitting
- ❌ No DoD: Команда не знает "done" → ✅ Universal DoD checklist

### 🌟 Excellence Indicators

- [ ] **8 Epic Splitting Patterns**: Workflow steps, business rules, simple vs complex
- [ ] **Spotify Independence**: Transparent code, self-service, minimal dependencies
- [ ] **Acceptance Criteria Format**: "Given [context] When [action] Then [outcome]"
- [ ] **Estimation Calibrated**: Velocity tracking показывает точность

---

## 🚀 Implementation Checklist

### ✅ Quality Gates (Automated)

**Pre-Commit:**
- [ ] Linting passing
- [ ] No secrets in code

**Pull Request:**
- [ ] ≥1 peer review approval
- [ ] Code coverage ≥80% (no decrease)
- [ ] Static analysis passing (SonarQube)
- [ ] Security scan: 0 critical CVEs

**Build:**
- [ ] Unit tests: 100% pass rate
- [ ] Build time < 15 min

**Staging:**
- [ ] E2E tests passing
- [ ] Load test: handles 2x expected traffic
- [ ] API response time p95 < 300ms

**Production:**
- [ ] Gradual rollout: 5% → 25% → 50% → 100%
- [ ] Error rate < 0.1% (auto-rollback if exceeds)
- [ ] Monitoring & alerting active

### ⚠️ Common Anti-Patterns

- ❌ No Code Review: Код в main без review → ✅ Обязательный ≥1 approval
- ❌ Low Test Coverage: < 50% → ✅ Quality gate: ≥80%
- ❌ Skipping Quality Gates: "Срочно, пропустим" → ✅ Автоматизация: нельзя обойти
- ❌ Big Bang Release: 100% users сразу → ✅ Gradual rollout
- ❌ No Monitoring: Нет alerts → ✅ Alerts на error rate, latency, availability

### 🌟 Excellence Indicators

- [ ] **RFC Process**: Design doc для architectural changes
- [ ] **DORA Metrics**: Tracking deployment frequency, lead time, change failure rate, MTTR
- [ ] **Tech Debt Budget**: 15-25% capacity каждого спринта
- [ ] **Automated Quality Gates**: Интегрированы в CI/CD pipeline

---

## 📊 DORA Metrics Targets

| Metric | Elite | Target | Current |
|--------|-------|--------|---------|
| **Deployment Frequency** | Multiple/day | Weekly | [TBD] |
| **Lead Time for Changes** | < 1 hour | < 1 week | [TBD] |
| **Change Failure Rate** | 0-1% | < 5% | [TBD] |
| **Mean Time to Recovery** | < 1 hour | < 1 day | [TBD] |

---

## 🎯 Prioritization Quick Reference

### BCG Matrix (Portfolio)
- **Stars**: High share + High growth → Invest
- **Cash Cows**: High share + Low growth → Harvest
- **Question Marks**: Low share + High growth → Evaluate
- **Dogs**: Low share + Low growth → Divest

### Value vs Complexity (Features)
- **Quick Wins**: High value + Low effort → Do first
- **Strategic**: High value + High effort → Plan carefully
- **Fill-Ins**: Low value + Low effort → If capacity
- **Time Sinks**: Low value + High effort → Avoid

### Tech Debt Quadrant
- **Critical**: High impact + Low effort → Do now
- **Strategic**: High impact + High effort → Plan Q
- **Monitor**: Low impact + Low effort → Watch
- **Avoid**: Low impact + High effort → Low priority

---

## 🔍 Pre-Mortem Template (5 минут)

**Сценарий**: "Проект провалился. Почему?"

**Топ 5 Failure Modes:**
1. [Failure mode 1]
2. [Failure mode 2]
3. [Failure mode 3]
4. [Failure mode 4]
5. [Failure mode 5]

**Для каждого:**
- Impact (1-5): [?]
- Likelihood (1-5): [?]
- Risk Score = Impact × Likelihood
- Mitigation: [Action plan]
- Owner: [Person]

---

## 📝 Epic Splitting Cheat Sheet

**8 Patterns:**

1. **Workflow Steps**: Multi-step process → Separate stories per step
2. **Business Rules**: Different scenarios → Different stories
3. **Simple vs Complex**: Basic first → Advanced later
4. **Major Effort**: Simple version → Defer complexity
5. **Data Variations**: Different data types → Different stories
6. **Acceptance Criteria**: One AC → One story
7. **CRUD Operations**: Create, Read, Update, Delete → Separate stories
8. **Spike**: Research → Separate time-boxed story

**Example:**
- Epic: "User can complete checkout"
  - Story 1: Add items to cart
  - Story 2: Enter shipping info
  - Story 3: Enter payment info
  - Story 4: Receive confirmation

---

## 🛡️ Rollback Checklist

**Before Production Deploy:**
- [ ] Feature flag configured (can disable in 30 seconds)
- [ ] Database migration rollback script tested
- [ ] Monitoring thresholds set:
  - [ ] Error rate > 1% → Auto-rollback
  - [ ] API latency p95 > 500ms → Alert
  - [ ] User complaints > 10/hour → Investigate
- [ ] On-call engineer assigned
- [ ] Runbook updated (troubleshooting steps)

---

## 🎓 Quick References

### HEART Framework
- **H**appiness: NPS, CSAT
- **E**ngagement: DAU/MAU, sessions
- **A**doption: Activation rate
- **R**etention: Cohort analysis
- **T**ask Success: Completion rate

### RACI
- **R**esponsible: Does the work
- **A**ccountable: Answers for result (only 1!)
- **C**onsulted: Provides input
- **I**nformed: Kept updated

### INVEST
- **I**ndependent
- **N**egotiable
- **V**aluable
- **E**stimable
- **S**mall
- **T**estable

---

## ✅ Final Validation

**Before approving any artifact, ask:**

1. ✅ **Clarity**: Может ли новый член команды понять цель за 5 минут?
2. ✅ **Measurability**: Есть ли четкие метрики успеха с целевыми значениями?
3. ✅ **Actionability**: Может ли команда начать работу без дополнительных вопросов?
4. ✅ **Risk Awareness**: Идентифицированы ли топ-3 риска с митигацией?
5. ✅ **User Focus**: Ясно ли, какую ценность это приносит пользователю?

**Если хотя бы 1 из 5 = "Нет" → Артефакт требует доработки.**

---

## 📚 Быстрые ссылки

- [Полное исследование](/SPECIFICATION_EXCELLENCE_RESEARCH.md)
- [Amazon Working Backwards](https://www.hustlebadger.com/what-do-product-teams-do/amazon-working-backwards-process/)
- [Google HEART Framework](https://www.heartframework.com/)
- [DORA Metrics](https://linearb.io/blog/dora-metrics)
- [INVEST Criteria](https://www.leanwisdom.com/blog/crafting-high-quality-user-stories-with-the-invest-criteria-in-safe/)

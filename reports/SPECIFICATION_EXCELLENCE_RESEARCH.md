# Исследование: Мировые практики создания спецификаций, планов и задач

**Дата**: 2026-01-03
**Агент**: product-manager
**Цель**: Исследовать передовые практики от Google, Amazon, Stripe, Airbnb, McKinsey, BCG, FAANG для интеграции в Spec Kit

---

## Оглавление

1. [Specification Excellence: PRD Best Practices](#1-specification-excellence-prd-best-practices)
2. [Planning Excellence: Implementation Plans](#2-planning-excellence-implementation-plans)
3. [Task Breakdown Excellence](#3-task-breakdown-excellence)
4. [Implementation Excellence](#4-implementation-excellence)
5. [Anti-Patterns to Avoid](#5-anti-patterns-to-avoid)
6. [Интеграционные рекомендации для Spec Kit](#6-интеграционные-рекомендации-для-spec-kit)

---

## 1. Specification Excellence: PRD Best Practices

### 1.1 Amazon Working Backwards (Press Release + FAQ)

**Метод**: Начинать с пресс-релиза и FAQ *до* написания кода.

**Структура PR:**
```markdown
# [COMPANY] ANNOUNCES [SERVICE/TECHNOLOGY/TOOL] TO ENABLE [CUSTOMER SEGMENT] TO [BENEFIT STATEMENT]

**Подзаголовок**: Переформулирует решение с дополнительными деталями
**Дата**: Предполагаемая дата запуска
**Вводный абзац**: Описание решения, целевой аудитории и преимуществ

## Проблема
Какую проблему это решает? (Избегать формулировки "отсутствует функция X")

## Решение
Как продукт решает проблему?

## Цитата руководства
Почему мы увлечены этим?

## Как начать работу
С чего начинается путь клиента?

## Цитата клиента
Отзыв раннего пользователя (воображаемый)

## Призыв к действию
Следующие шаги
```

**Структура FAQ:**
- Внешний FAQ (для клиентов): Вопросы о функциональности, ценообразовании, поддержке
- Внутренний FAQ (для команды): Технические вопросы, зависимости, бизнес-метрики

**Почему это работает:**
- Заставляет фокусироваться на ценности для клиента, а не на конкурентах или технических возможностях
- Выявляет проблемы *до* разработки, когда изменения дешевы
- Создает выравнивание команды вокруг единого видения

**Источники:**
- [Amazon Working Backwards Template](https://www.hustlebadger.com/what-do-product-teams-do/amazon-working-backwards-process/)
- [Working Backwards: The Amazon PR/FAQ](https://productstrategy.co/working-backwards-the-amazon-prfaq-for-product-innovation/)
- [Working Backwards Official Resources](https://workingbackwards.com/resources/working-backwards-pr-faq/)

---

### 1.2 Google HEART Framework (Metrics Definition)

**Фреймворк**: 5 категорий метрик для измерения UX качества.

**HEART = Happiness + Engagement + Adoption + Retention + Task Success**

| Категория | Определение | Пример метрик |
|-----------|-------------|---------------|
| **Happiness** | Удовлетворенность пользователей | NPS, CSAT, опросы настроений |
| **Engagement** | Уровень использования продукта | Время в приложении, кол-во сессий, кол-во действий |
| **Adoption** | Как продукт привлекает новых пользователей | Скорость онбординга, активация первой функции |
| **Retention** | Удержание пользователей | Day 1/7/30 retention, churn rate |
| **Task Success** | Эффективность выполнения задач | Task completion rate, время выполнения, error rate |

**GSM Process (Goals → Signals → Metrics):**

1. **Goals**: Для каждой категории HEART определите цель
   - Пример: "Улучшить скорость онбординга новых пользователей" (Adoption)

2. **Signals**: Качественное поведение пользователя, связанное с целью
   - Действия: "Пользователь завершает настройку профиля"
   - Чувства: "Пользователь чувствует, что онбординг простой"

3. **Metrics**: Количественные метрики для измерения сигналов
   - % пользователей, завершивших онбординг за первые 24 часа
   - Средний NPS-скор после онбординга

**Best Practices:**
- Не все проекты требуют всех 5 метрик — выбирайте 1-2 наиболее релевантные
- Избегайте "интересных статистик" — только метрики, влияющие на решения
- Используйте HEART на уровне функций, а не микровзаимодействий или всего продуктового семейства

**Интеграция с OKR:**
- HEART goals → OKR Objectives
- HEART metrics → Key Results
- Пример OKR:
  - Objective: "Improve daily sign-ups by 25% by May 1"
  - KR1: Adoption rate +25% (HEART: Adoption)
  - KR2: Time-to-first-value < 5 min (HEART: Task Success)

**Источники:**
- [How to Use Google's HEART Framework](https://www.productplan.com/learn/heart-framework-product-decisions/)
- [HEART Framework for Software UX](https://amplitude.com/blog/heart-framework-software-ux)
- [Google HEART Framework Official](https://www.heartframework.com/)

---

### 1.3 Stripe/Airbnb Design Frameworks

**Airbnb: 11-Star Experience Framework**

Метод мышления для выхода за пределы инкрементальных улучшений:

| Звезды | Опыт |
|--------|------|
| 1★ | Худший возможный опыт (сайт не загружается) |
| 3★ | Базовая функциональность (можно забронировать комнату) |
| 5★ | Ожидаемый отличный опыт (простой букинг, хорошие фото, отзывы) |
| 7★ | Удивительный опыт (консьерж звонит для подтверждения, предлагает активности) |
| 9★ | Магический опыт (лимузин из аэропорта, персонализированный номер) |
| 11★ | Невозможный опыт (частный самолет, персональный шеф-повар, вилла на острове) |

**Процесс:**
1. Представьте 11-звездочный опыт (невозможный, но идеальный)
2. Работайте в обратном направлении к осуществимому 7-9★ опыту
3. Определите минимальный 5★ опыт (MVP)
4. Убедитесь, что 3★ базовые потребности покрыты

**Stripe: Writing Culture & Context Sharing**

- **Контекст, а не контроль**: Делитесь стратегией, метриками, ограничениями; команды принимают тактические решения
- **DRI (Directly Responsible Individual)**: Каждая инициатива имеет ОДНОГО ответственного человека (не "мы", только "я")
- **High Alignment, Loosely Coupled**: Четкие цели, автономное исполнение

**Источники:**
- [How Great Design Was Key to Airbnb's Success](https://passionates.com/how-great-design-key-to-airbnbs-massive-success/)
- [Building Beautiful Products with Stripe's Head of Design](https://www.lennysnewsletter.com/p/building-beautiful-products-with)
- [Managing Your PM Career](https://maven.com/shreyas-doshi/product-management-career)

---

### 1.4 Критические секции мирового класса PRD

**Базовые секции (обязательные):**

1. **Problem Statement** (Формулировка проблемы)
   - НЕ "отсутствует функция X"
   - Глубокое понимание боли, неэффективности, неудовлетворенных потребностей
   - Проверка: Читатель должен согласиться "да, это проблема стоит решения"

2. **User Personas & Jobs-to-be-Done**
   - Формат: "Когда [ситуация], я хочу [мотивация], чтобы [ожидаемый результат]"
   - Не демографические данные — контекст и мотивация
   - Пример: "Когда я работаю удаленно, я хочу чувствовать связь с командой, чтобы поддерживать отношения и эффективно сотрудничать"

3. **Success Metrics** (Метрики успеха)
   - North Star Metric: единая метрика, представляющая ценность для клиента
   - Input Metrics: драйверы North Star (2-5 метрик)
   - Измеримые KPI с целевыми значениями
   - Пример: "Increase DAU from 100K to 500K by Q2" (не "улучшить вовлеченность")

4. **MVP Definition & Phasing**
   - P0 (Must-have): Минимально жизнеспособная функциональность для принятия
   - P1 (Important): Важные, но не критичные для запуска
   - P2 (Nice-to-have): Функции для будущих итераций
   - Каждая фаза связана с целями обучения

5. **User Journeys & Edge Cases**
   - Идеальный путь (happy path)
   - Альтернативные потоки
   - Обработка ошибок и неожиданного поведения
   - Граничные случаи: "Что если пользователь..."

6. **Non-Functional Requirements**
   - Производительность: время отклика, пропускная способность
   - Безопасность: аутентификация, авторизация, шифрование
   - Масштабируемость: ожидаемый рост пользователей
   - Доступность (Accessibility): WCAG compliance, screen readers
   - Соответствие (Compliance): GDPR, HIPAA, SOC2

7. **Dependencies & Risks**
   - Технические зависимости (API, инфраструктура, сторонние сервисы)
   - Кросс-функциональные зависимости (дизайн, маркетинг, продажи)
   - Идентифицированные риски с планами митигации

**Продвинутые секции (для сложных проектов):**

8. **Competitive Analysis**
   - Как конкуренты решают эту проблему?
   - Наши дифференциаторы и уникальная ценность
   - Feature comparison table

9. **Go-to-Market Strategy**
   - Целевые сегменты и позиционирование
   - Каналы запуска и маркетинговые кампании
   - Ценообразование и упаковка

10. **Change History & Living Document Status**
    - Версионирование (v1.0, v1.1, etc.)
    - Кто изменил, когда, почему
    - Статус: Draft → Review → Approved → In Progress → Delivered

**Источники:**
- [12 Real PRD Examples from Top Tech Companies](https://pmprompt.com/blog/prd-examples)
- [PRD Document Template 2025](https://www.kuse.ai/blog/insight/prd-document-template-in-2025-how-to-write-effective-product-requirements)
- [How to Write a PRD: Complete Guide](https://www.perforce.com/blog/alm/how-write-product-requirements-document-prd)

---

## 2. Planning Excellence: Implementation Plans

### 2.1 McKinsey/BCG Strategic Planning Frameworks

**BCG Growth-Share Matrix (Portfolio Prioritization):**

| Квадрант | Характеристики | Стратегия |
|----------|----------------|-----------|
| **Stars** | Высокая доля рынка + Высокий рост | Инвестировать для поддержания роста |
| **Cash Cows** | Высокая доля рынка + Низкий рост | Собирать стабильную прибыль, минимальные инвестиции |
| **Question Marks** | Низкая доля рынка + Высокий рост | Тщательно оценить: инвестировать или дивестировать |
| **Dogs** | Низкая доля рынка + Низкий рост | Дивестировать или прекратить |

**McKinsey 7S Framework (Organizational Alignment):**

7 внутренних элементов организации, которые должны быть выровнены:
- **Strategy**: Долгосрочный план
- **Structure**: Организационная структура
- **Systems**: Процессы и процедуры
- **Shared Values**: Корпоративные ценности
- **Skills**: Компетенции команды
- **Style**: Лидерский стиль
- **Staff**: Люди и культура

**GE-McKinsey Matrix (Business Unit Evaluation):**

Оценка бизнес-единиц по двум осям:
- Ось X: Industry Attractiveness (Привлекательность индустрии)
- Ось Y: Business Strength (Сила бизнеса)

9 квадрантов → приоритизация инвестиций

**Value vs Complexity Matrix (Feature Prioritization):**

```
          HIGH VALUE
              │
    STRATEGIC │ QUICK WINS
    (plan)    │ (do first)
──────────────┼──────────────
    TIME      │ FILL-INS
    SINKS     │ (if capacity)
    (avoid)   │
              │
          LOW VALUE

    LOW         HIGH
    COMPLEXITY  COMPLEXITY
```

**Источники:**
- [MBB Frameworks Bundle](https://www.eloquens.com/tool/vqPVi0dJ/strategy/mbb-mckinsey-bain-bcg-frameworks/mbb-mckinsey-bcg-bain-models-and-frameworks-bundle)
- [Strategic Planning Models Guide](https://www.bobstanke.com/blog/strategic-planning-models)
- [BCG Matrix Strategic Framework](https://quantive.com/resources/articles/bcg-matrix)

---

### 2.2 RACI Matrix (Responsibility Assignment)

**RACI = Responsible, Accountable, Consulted, Informed**

| Role | Definition | Example |
|------|------------|---------|
| **R - Responsible** | Человек, выполняющий работу | Engineer implementing feature |
| **A - Accountable** | Человек, отвечающий за конечный результат (ТОЛЬКО ОДИН) | Product Manager |
| **C - Consulted** | Люди, дающие input до выполнения работы | Design team, Security team |
| **I - Informed** | Люди, информируемые о прогрессе/решениях | Marketing, Support, Sales |

**Правила:**
- Каждая задача имеет **как минимум один R**
- Каждая задача имеет **ровно одно A** (не больше!)
- Ограничить количество C и I — избыток замедляет
- Согласовать RACI с заинтересованными сторонами в начале проекта

**Пример RACI для Feature Launch:**

| Task | PM | Eng Lead | Designer | Marketing | Support |
|------|----|----|---------|-----------|---------|
| Define requirements | A | C | C | I | I |
| Create mockups | C | I | A/R | I | I |
| Implement feature | A | R | C | I | I |
| Write release notes | R | C | I | A | C |
| Launch campaign | C | I | I | A/R | C |
| Monitor metrics | A/R | C | I | I | I |

**Best Practices:**
- Создавать в начале проекта с участием команды
- Регулярно пересматривать при изменении scope
- Документировать изменения
- Использовать как reference для разрешения конфликтов

**Источники:**
- [RACI Matrix Guide](https://project-management.com/understanding-responsibility-assignment-matrix-raci-matrix/)
- [RACI Chart: What is it & How to Use](https://www.atlassian.com/work-management/project-management/raci-chart)
- [The RACI Matrix: Your Blueprint for Project Success](https://www.cio.com/article/287088/project-management-how-to-design-a-successful-raci-project-plan.html)

---

### 2.3 Dependency Mapping & Critical Path Method (CPM)

**Dependency Mapping:**

Визуализация зависимостей между задачами, ресурсами и вехами.

**4 типа зависимостей:**

1. **Finish-to-Start (FS)**: Задача B начинается после завершения задачи A
   - Пример: "Design mockups" → "Implement UI"

2. **Start-to-Start (SS)**: Задача B начинается одновременно с задачей A
   - Пример: "Backend API development" || "Frontend development"

3. **Finish-to-Finish (FF)**: Задача B завершается одновременно с задачей A
   - Пример: "QA testing" заканчивается вместе с "Documentation"

4. **Start-to-Finish (SF)**: Задача B завершается, когда задача A начинается (редко)

**Critical Path Method (CPM):**

Алгоритм для определения самой длинной цепочки зависимых задач от старта до финиша.

**Процесс:**
1. Перечислить все задачи
2. Определить длительность каждой задачи
3. Определить зависимости
4. Построить сетевую диаграмму
5. Вычислить критический путь (самая длинная последовательность)
6. Определить float (запас времени для некритических задач)

**Пример:**

```
Task A (5d) → Task B (3d) → Task D (4d) = 12 days (Critical Path)
Task A (5d) → Task C (2d) → Task D (4d) = 11 days (имеет 1 день float)
```

**Benefits для планирования:**
- Определяет минимальное время завершения проекта
- Выявляет задачи, которые нельзя задерживать (критические)
- Помогает в распределении ресурсов (приоритет критическим задачам)
- Облегчает управление рисками (фокус на критические зависимости)

**Best Practices:**
- Создать dependency log/matrix во время планирования
- Регулярно обновлять при изменении зависимостей
- Документировать блокеры и планы разблокировки
- Использовать для оценки влияния задержек

**Источники:**
- [What is Dependency Mapping?](https://miro.com/project-management/what-is-dependency-mapping/)
- [Dependency Mapping in Project Management](https://creately.com/guides/dependency-mapping/)
- [Critical Path Method Explained](https://www.officetimeline.com/project-management/critical-path)

---

### 2.4 Pre-Mortem Analysis (Risk Mitigation)

**Метод**: Представить, что проект провалился, и работать в обратном направлении, чтобы определить причины.

**Процесс:**

1. **Setup** (после планирования, до начала разработки)
   - Соберите кросс-функциональную команду (разработка, дизайн, продукт, QA)
   - Временной горизонт: "Проект провалился через [6 месяцев/1 год]"

2. **Individual Brainstorm** (10 минут)
   - Каждый участник молча записывает 3-5 причин провала
   - Поощрять честность и креативность (безопасная среда)

3. **Group Discussion** (30 минут)
   - Каждый делится своими сценариями провала
   - Группировать похожие сценарии
   - Голосовать за наиболее вероятные/критические риски

4. **Prioritization** (15 минут)
   - Оценить каждый риск по Impact x Likelihood
   - Топ 5-10 рисков выбрать для митигации

5. **Mitigation Planning** (45 минут)
   - Для каждого риска:
     - Action Plan: как предотвратить риск
     - Contingency Plan: что делать, если риск реализуется
     - Owner: кто ответственный за митигацию
     - Timeline: когда проверить/пересмотреть

**Пример Pre-Mortem Worksheet:**

| Failure Scenario | Impact (1-5) | Likelihood (1-5) | Risk Score | Mitigation Strategy | Owner | Deadline |
|------------------|--------------|------------------|------------|---------------------|-------|----------|
| API третьей стороны недоступна | 5 | 3 | 15 | Разработать fallback механизм, контракт SLA | Eng Lead | Sprint 2 |
| Пользователи не понимают новый UI | 4 | 4 | 16 | Usability testing с 10 пользователями до запуска | Designer | Sprint 3 |
| Производительность деградирует при scale | 5 | 2 | 10 | Load testing с 10x ожидаемого трафика | DevOps | Sprint 4 |

**Benefits:**
- Выявляет слепые зоны (оптимизм bias)
- Снижает overconfidence и groupthink
- Улучшает прогнозирование (исследование Harvard: +30% точность)
- Проактивное управление рисками вместо реактивного

**Источники:**
- [How to Identify Project Risks Early with Pre-Mortem](https://seriousplaybusiness.com/project-pre-mortem-risk-identification/)
- [Pre-Mortem Analysis Guide](https://www.myfinanceprocess.com/pre-mortem-analysis/)
- [How to Conduct a Project Premortem](https://asana.com/resources/premortem)

---

## 3. Task Breakdown Excellence

### 3.1 INVEST Criteria for User Stories

**INVEST = Independent, Negotiable, Valuable, Estimable, Small, Testable**

| Критерий | Определение | Как проверить |
|----------|-------------|---------------|
| **I - Independent** | История не зависит от других историй | Можно разрабатывать и деплоить независимо |
| **N - Negotiable** | Детали реализации обсуждаемы | Описание без технических решений, оставляет пространство для команды |
| **V - Valuable** | Приносит ценность пользователю или бизнесу | Ясно сформулирована ценность: "чтобы я мог [результат]" |
| **E - Estimable** | Команда может оценить сложность | Достаточно деталей для оценки в story points/hours |
| **S - Small** | Завершается за 1 итерацию (1-2 недели) | Если больше → разбить на меньшие истории |
| **T - Testable** | Четкие критерии приемки | 2-5 acceptance criteria определяют "done" |

**User Story Template:**

```
As a [type of user]
I want [specific feature/functionality]
So that [specific benefit or outcome]

Acceptance Criteria:
1. [Specific testable condition]
2. [Specific testable condition]
3. [Specific testable condition]

Definition of Done:
- [ ] Code reviewed and approved
- [ ] Unit tests written and passing (≥80% coverage)
- [ ] Integration tests passing
- [ ] Manual QA completed
- [ ] Documentation updated
- [ ] No critical/blocker bugs
```

**Пример хорошей истории:**

```
As a mobile app user
I want to receive push notifications when someone mentions me in a comment
So that I can respond quickly and stay engaged with conversations

Acceptance Criteria:
1. When another user @mentions my username in a comment, I receive a push notification within 30 seconds
2. The notification includes the commenter's name and first 50 characters of the comment
3. Tapping the notification opens the app to the relevant comment thread
4. Users can disable mention notifications in Settings > Notifications

Definition of Done:
- [ ] Backend event system triggers notification on @mention
- [ ] Push notification delivered via Firebase Cloud Messaging (iOS & Android)
- [ ] Deep link opens correct comment thread
- [ ] Settings toggle implemented and tested
- [ ] Unit tests: 85% coverage
- [ ] Manual testing on iOS 17+ and Android 13+
- [ ] No P0/P1 bugs
```

**Источники:**
- [INVEST Criteria in SAFe](https://www.leanwisdom.com/blog/crafting-high-quality-user-stories-with-the-invest-criteria-in-safe/)
- [Top Tips For Breaking Down Epics/Features](https://www.scrum.org/forum/scrum-forum/40837/top-tips-breaking-down-epicsfeatures-user-stories)

---

### 3.2 Epic Splitting Techniques

**8 проверенных паттернов для разбиения больших историй:**

**1. Workflow Steps (Шаги процесса)**
- Разбить многошаговый процесс на отдельные истории для каждого шага
- Пример Epic: "User can complete checkout"
  - Story 1: User can add items to cart
  - Story 2: User can enter shipping information
  - Story 3: User can enter payment information
  - Story 4: User receives order confirmation

**2. Business Rules (Бизнес-правила)**
- Разные сценарии → разные истории
- Пример Epic: "Apply discount codes"
  - Story 1: Percentage-based discounts (10% off)
  - Story 2: Fixed amount discounts ($20 off)
  - Story 3: Free shipping codes
  - Story 4: BOGO (Buy One Get One) offers

**3. Simple vs Complex (Простое vs сложное)**
- Сначала базовая функциональность, потом продвинутая
- Пример Epic: "Search functionality"
  - Story 1: Basic keyword search
  - Story 2: Filters (category, price range)
  - Story 3: Advanced search with Boolean operators
  - Story 4: Search suggestions and autocomplete

**4. Major Effort (Главное усилие)**
- Начать с простой версии, отложить сложность на потом
- Пример Epic: "User profile customization"
  - Story 1: User can upload profile picture
  - Story 2: User can edit bio text (plain text)
  - Story 3: User can add social media links
  - Story 4: Rich text editor for bio (formatting, emojis)

**5. Data Variations (Варианты данных)**
- Разные типы данных → разные истории
- Пример Epic: "Import data from external sources"
  - Story 1: Import from CSV files
  - Story 2: Import from Excel files
  - Story 3: Import from Google Sheets
  - Story 4: Import from API (REST)

**6. Acceptance Criteria (Критерии приемки)**
- Один критерий приемки → одна история
- Пример Epic: "User authentication"
  - AC1 → Story 1: User can sign up with email/password
  - AC2 → Story 2: User can log in with email/password
  - AC3 → Story 3: User can reset forgotten password
  - AC4 → Story 4: User can enable two-factor authentication

**7. CRUD Operations (Create, Read, Update, Delete)**
- Разделить по операциям
- Пример Epic: "Manage team members"
  - Story 1: Admin can add new team members (Create)
  - Story 2: Admin can view list of team members (Read)
  - Story 3: Admin can edit team member roles (Update)
  - Story 4: Admin can remove team members (Delete)

**8. Spike (Исследование)**
- Выделить исследовательскую работу в отдельную историю
- Пример Epic: "Integrate AI chatbot"
  - Story 1 (Spike): Research and evaluate 3 AI chatbot APIs (timeboxed 3 days)
  - Story 2: Implement selected chatbot API
  - Story 3: Train chatbot with FAQ data
  - Story 4: Deploy chatbot to production

**Best Practices:**
- Разбивайте только на столько, сколько нужно для следующего спринта (не вперед на год)
- Каждая разбитая история должна соответствовать INVEST
- Приоритет приносящим ценность историям (не техническим задачам)
- Лимит: 2-5 acceptance criteria на историю (если больше → разбить)

**Источники:**
- [Splitting Epics and User Stories](https://premieragile.com/splitting-epics-and-user-stories/)
- [Two Examples of Splitting Epics](https://www.mountaingoatsoftware.com/blog/two-examples-of-splitting-epics)
- [Practice: Decomposing Features into Stories](https://www.pmi.org/disciplined-agile/team-lead/practice-decomposing-features-into-stories)

---

### 3.3 Spotify/Netflix Task Independence (Dependency Management)

**Spotify's Squad Model & Dependency Reduction:**

**Принцип**: "Squad всегда может двигаться независимо от других squad, даже при наличии зависимостей."

**Стратегии для обеспечения независимости:**

**1. Transparent Code Model**
- Весь код доступен всем разработчикам
- Если Squad A блокирует Squad B → Squad B может сделать изменения сам
- Ownership без блокировки: "ты владеешь, но не блокируешь"

**2. Self-Service Infrastructure**
- Команды создают собственные сервисы без зависимости от Platform team
- Golden Paths: визарды для быстрого старта проектов
  - Backend services
  - Application features
  - Data pipelines
  - ML projects
  - Web apps
- Документация best practices для каждого типа проекта

**3. Alliance (для управления зависимостями между Tribes)**
- 3+ tribes (300+ человек) работают над взаимосвязанными задачами
- Регулярные синхронизации между tribes для управления зависимостями
- Снижение bottlenecks через координацию

**4. Microservices Architecture (Netflix/Spotify pattern)**
- Каждый сервис разрабатывается, тестируется и деплоится независимо
- Изменения в Service A не ломают Service B
- Команды владеют всем lifecycle своего сервиса

**Netflix Dependency Management:**

**1. Small Cross-Functional Teams**
- 1 PM + 4-6 Engineers + 1 Designer + 1 Data Scientist
- Команда владеет всеми зависимостями внутри
- Минимизация внешних dependencies

**2. Context, Not Control**
- Менеджеры дают стратегический контекст
- Команды принимают решения самостоятельно
- Автономия в исполнении

**3. Internal Tools for Self-Service**
- Developers управляют deployments самостоятельно
- Мониторинг систем без зависимости от других команд
- Тестирование кода с минимальными dependencies

**Практические рекомендации для Task Breakdown:**

- **Design for Independence**: При разбиении задач минимизировать cross-team dependencies
- **API Contracts Early**: Определить API интерфейсы до начала разработки
- **Mock/Stub External Dependencies**: Использовать моки для внешних зависимостей
- **Feature Flags**: Деплоить незавершенные функции за флагами, чтобы не блокировать release

**Источники:**
- [How Spotify Improved Developer Productivity](https://engineering.atspotify.com/2020/08/how-we-improved-developer-productivity-for-our-devops-teams)
- [7 Main Elements of Spotify Tribe Engineering Model](https://dworkz.com/article/7-main-elements-of-spotifys-tribe-engineering-model-in-2025/)
- [What Methodology Does Netflix Use?](https://www.designgurus.io/answers/detail/what-methodology-does-netflix-use)

---

### 3.4 Definition of Done (DoD) vs Acceptance Criteria

**Definition of Done (DoD):**
- Универсальный стандарт для **всех** user stories в проекте/команде
- Определяет, когда product increment готов к релизу
- Создается командой разработки с участием PO, QA, других stakeholders

**Acceptance Criteria (AC):**
- Специфичны для **конкретной** user story
- Определяют функциональные требования: что должна делать эта история
- Создаются Product Owner или командой

**Оба должны быть выполнены для завершения истории.**

**Пример Definition of Done (универсальный для команды):**

```markdown
# Definition of Done

## Code Quality
- [ ] Code reviewed and approved by at least 1 senior engineer
- [ ] No code smells or critical SonarQube issues
- [ ] Follows team coding standards (linting rules passing)
- [ ] No commented-out code or debug statements

## Testing
- [ ] Unit tests written with ≥80% code coverage
- [ ] Integration tests passing (if applicable)
- [ ] Manual testing completed by developer
- [ ] QA testing completed and signed off
- [ ] No P0 (blocker) or P1 (critical) bugs

## Security & Performance
- [ ] Security scan passed (no critical vulnerabilities)
- [ ] Performance benchmarks met (e.g., API response < 200ms)
- [ ] No sensitive data logged or exposed

## Documentation
- [ ] API documentation updated (Swagger/OpenAPI)
- [ ] README updated with new features/changes
- [ ] User-facing documentation updated (if applicable)

## Deployment
- [ ] Feature flag implemented (if needed)
- [ ] Database migrations tested and backward compatible
- [ ] Deployed to staging environment
- [ ] Smoke tests passing in staging
- [ ] Rollback plan documented

## Stakeholder Sign-off
- [ ] Product Owner accepts the story
- [ ] Design review completed (if UI changes)
```

**Пример Acceptance Criteria (специфично для одной истории):**

```markdown
User Story: As a user, I want to filter products by price range so that I can find items within my budget.

Acceptance Criteria:
1. Price range filter displays min and max price inputs
2. Entering min price (e.g., $50) shows only products ≥$50
3. Entering max price (e.g., $200) shows only products ≤$200
4. Entering both min and max shows products within range
5. Invalid inputs (non-numeric) show error message
6. Filter updates results in real-time without page reload
7. Filter state persists when navigating to product detail and back
```

**Best Practices:**
- **DoD**: Пересматривать каждый квартал, обновлять при изменении стандартов команды
- **AC**: 2-5 критериев на историю (если больше → разбить историю)
- **Testability**: Каждый AC должен быть однозначно проверяемым (не "улучшить UX")
- **Ownership**: DoD создается командой; AC создается PO с участием команды

**Источники:**
- [Definition of Done vs Acceptance Criteria](https://www.visual-paradigm.com/scrum/definition-of-done-vs-acceptance-criteria/)
- [What is the Definition of Done in Agile?](https://www.atlassian.com/agile/project-management/definition-of-done)
- [5 Steps to Find Your Definition of Done](https://plan.io/blog/definition-of-done/)

---

## 4. Implementation Excellence

### 4.1 Engineering RFC (Request for Comments) Process

**Что такое RFC:**
- Документ для планирования архитектуры до написания кода
- Уточняет предположения и распространяет планы заранее
- Используется Google, Facebook, Amazon, Uber, Stripe

**Когда писать RFC:**

- ✅ Строите что-то с нуля (новый endpoint, компонент, система, библиотека)
- ✅ Изменения влияют на несколько систем или команд
- ✅ Определяете контракт/интерфейс между клиентами или системами
- ✅ Добавляете новую зависимость
- ✅ Добавляете/заменяете язык или инструмент в стеке
- ❌ Простые багфиксы или рефакторинг внутри одной системы

**Структура RFC (на основе HashiCorp template):**

```markdown
# RFC: [Title]

**Author**: [Name]
**Date**: [YYYY-MM-DD]
**Status**: Draft | Review | Approved | Rejected | Implemented

## Overview (1-2 параграфа)
Краткое описание цели RFC без погружения в детали "почему/как".

## Background (2-3 параграфа до 1 страницы)
- Контекст проблемы: почему эти изменения необходимы?
- Ссылки на связанные документы, issues, PRDs
- Исторический контекст (что пробовали раньше, почему не сработало)
- Цель: новый сотрудник должен понять полный контекст

## Goals & Non-Goals
### Goals
- [Что мы хотим достичь]
- [Что мы хотим достичь]

### Non-Goals (важно!)
- [Что явно НЕ в scope]
- [Что явно НЕ в scope]

## Proposal (Основная секция)
### High-Level Design
- Архитектурная диаграмма
- Основные компоненты и их взаимодействие
- Data flow

### Detailed Design
- API changes (internal & external)
- Database schema changes
- New dependencies
- Configuration changes

### Implementation Plan
1. Phase 1: [Description] - [Timeline]
2. Phase 2: [Description] - [Timeline]
3. Phase 3: [Description] - [Timeline]

## Alternatives Considered
### Alternative 1: [Name]
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

### Alternative 2: [Name]
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

## Risks & Mitigation
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| [Risk description] | High/Med/Low | High/Med/Low | [How to mitigate] |

## Testing Plan
- Unit tests: [Coverage target, key scenarios]
- Integration tests: [What integrations to test]
- Load/Performance tests: [Benchmarks to meet]
- Rollback plan: [How to revert if issues]

## Rollout Plan
- [ ] Feature flag strategy
- [ ] Gradual rollout (% of users)
- [ ] Monitoring & alerting
- [ ] Rollback criteria

## Success Metrics
- [Metric 1]: [Current value] → [Target value]
- [Metric 2]: [Current value] → [Target value]

## Open Questions
1. [Question that needs resolution before proceeding]
2. [Question that needs resolution before proceeding]

## Appendix
- [Links to related RFCs, PRDs, design docs]
- [Prototypes, POCs, benchmarks]
```

**Uber RFC Best Practices:**

- **Lightweight templates** для изменений в рамках команды
- **Heavyweight templates** для изменений масштаба организации
- **Searchable repository** всех RFC с четко отмеченными approvers
- **Integration с task systems** (JIRA, Phabricator) для tracking approval

**Процесс Review:**

1. **Draft** (1-2 дня): Автор пишет RFC
2. **Peer Review** (3-5 дней): Команда комментирует, задает вопросы
3. **Revision** (1-2 дня): Автор обновляет на основе feedback
4. **Approval** (1 день): Tech Lead / Architect одобряет
5. **Implementation** (weeks): Команда реализует согласно RFC

**Источники:**
- [Software Engineering RFC and Design Doc Examples](https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design)
- [Companies Using RFCs or Design Docs](https://blog.pragmaticengineer.com/rfcs-and-design-docs/)
- [HashiCorp RFC Template](https://works.hashicorp.com/articles/rfc-template)

---

### 4.2 Quality Gates & Testing Strategy

**Software Quality Gate:**
Автоматизированный checkpoint в SDLC, который проверяет, соответствует ли код заранее определенным критериям.

**Key Quality Metrics & Thresholds:**

| Quality Gate | Metric | Threshold | Tool |
|--------------|--------|-----------|------|
| **Code Coverage** | % code covered by tests | ≥80% | Jest, pytest, JaCoCo |
| **Code Quality** | Code smells, tech debt | ≤5 critical issues | SonarQube |
| **Security** | Vulnerabilities | 0 critical, ≤3 high | Snyk, OWASP Dependency-Check |
| **Performance** | API response time | ≤300ms (p95) | JMeter, k6, Gatling |
| **Defect Density** | Bugs per 1000 LOC | ≤1.0 | Bug tracking system |
| **Build Success** | % successful builds | ≥95% | CI/CD platform |

**Quality Gates по фазам SDLC:**

### 1. Code Commit Quality Gate
- [ ] Linting rules passing (ESLint, Pylint, etc.)
- [ ] Code formatted (Prettier, Black, gofmt)
- [ ] Pre-commit hooks passing
- [ ] No secrets/credentials in code (GitGuardian)

### 2. Pull Request Quality Gate
- [ ] ≥1 peer review approval
- [ ] All review comments resolved
- [ ] Code coverage ≥80% (no decrease from baseline)
- [ ] Static analysis passing (SonarQube quality gate)
- [ ] Security scan passing (0 critical vulnerabilities)
- [ ] Unit tests passing
- [ ] No merge conflicts

### 3. Build Quality Gate
- [ ] Compilation successful
- [ ] Unit tests passing (100% pass rate)
- [ ] Integration tests passing
- [ ] Docker image build successful
- [ ] Build time < 15 min (if slower → optimize)

### 4. Staging Deployment Quality Gate
- [ ] Smoke tests passing
- [ ] E2E tests passing
- [ ] Performance tests meeting benchmarks
- [ ] Load tests: system handles 2x expected traffic
- [ ] Database migrations successful
- [ ] No regressions in key user flows

### 5. Production Deployment Quality Gate
- [ ] Gradual rollout (canary: 5% → 25% → 100%)
- [ ] Error rate < 0.1% (rollback if exceeds)
- [ ] Response time within SLA
- [ ] No spike in user-reported issues
- [ ] Monitoring & alerting active
- [ ] Rollback plan tested

**Testing Pyramid Strategy:**

```
           /\
          /  \        E2E Tests (10%)
         /    \       - Critical user journeys
        /------\      - Slow, brittle, expensive
       /        \
      /          \    Integration Tests (20%)
     /            \   - API contracts, database
    /--------------\  - Service interactions
   /                \
  /                  \ Unit Tests (70%)
 /____________________\ - Fast, isolated, cheap
                        - Business logic, utilities
```

**DORA Metrics (Engineering Excellence):**

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| **Deployment Frequency** | Multiple/day | Weekly-Monthly | Monthly-6mo | 6mo+ |
| **Lead Time for Changes** | < 1 hour | 1 day - 1 week | 1 week - 1 month | 1-6 months |
| **Change Failure Rate** | 0-1% | 1-5% | 5-15% | > 15% |
| **Mean Time to Recovery** | < 1 hour | < 1 day | 1 day - 1 week | > 1 week |

**Best Practices:**
- Реалистичные пороги (100% coverage фрустрирует команду)
- Вовлечение разработчиков в определение gates (избежать сопротивления)
- Интеграция в CI/CD pipeline для автоматизации
- Мониторинг трендов (не только pass/fail)

**Источники:**
- [Software Quality Gates: What They Are & Why They Matter](https://testrigor.com/blog/software-quality-gates/)
- [Quality Gates and Test Orchestration Strategy](https://lesia-topol.medium.com/quality-gates-and-test-orchestration-strategy-in-one-slide-f55c183118ac)
- [What Are DORA Metrics?](https://linearb.io/blog/dora-metrics)

---

### 4.3 Technical Debt Tracking & Management

**Определение Technical Debt:**
Стоимость будущей доработки, вызванной выбором быстрого решения сейчас вместо лучшего подхода, который требует больше времени.

**4 типа Technical Debt (по Martin Fowler):**

1. **Reckless & Deliberate**: "У нас нет времени на дизайн" (худший)
2. **Reckless & Inadvertent**: "Что такое layered architecture?" (незнание)
3. **Prudent & Deliberate**: "Мы должны поставить сейчас, разберемся с последствиями позже" (осознанный trade-off)
4. **Prudent & Inadvertent**: "Теперь мы знаем, как надо было делать" (обучение)

**Framework для отслеживания Tech Debt:**

### Tech Debt Register (реестр долга)

| ID | Description | Type | Impact | Effort | Risk Score | Owner | Status |
|----|-------------|------|--------|--------|------------|-------|--------|
| TD-001 | Legacy authentication system (no MFA) | Security | High | 3 weeks | 15 | Security team | Planned Q2 |
| TD-002 | Monolithic database (scaling bottleneck) | Architecture | High | 8 weeks | 12 | Platform team | In Progress |
| TD-003 | No unit tests for payment module | Testing | Medium | 2 weeks | 8 | Payments team | Backlog |

**Risk Score = Impact (1-5) × Likelihood of causing issue (1-5)**

### Metrics для отслеживания Tech Debt

**Code Quality Metrics:**
- Code coverage: текущий % → целевой %
- Code smells: количество issues по SonarQube
- Cyclomatic complexity: сложность функций/методов
- Code duplication: % дублированного кода

**Productivity Metrics:**
- Time to fix bugs: среднее время на багфикс
- Build time: время сборки проекта
- Deployment frequency: как часто деплоим (DORA metric)
- Developer satisfaction: опросы команды (1-10)

**Business Impact Metrics:**
- Feature velocity: скорость доставки новых функций
- Incident frequency: количество production incidents
- Customer-reported bugs: количество багов от пользователей

### Приоритизация Tech Debt

**Tech Debt Quadrant (Value vs Effort):**

```
     HIGH BUSINESS IMPACT
            │
  CRITICAL  │  QUICK WINS
  (plan Q)  │  (do now)
────────────┼────────────────
  MONITOR   │  AVOID
  (watch)   │  (low priority)
            │
     LOW BUSINESS IMPACT

  LOW EFFORT    HIGH EFFORT
```

**Tech Debt Budget:**
- Резервировать 15-25% capacity каждого спринта на tech debt
- Правило "20% time": 1 день в неделю на улучшения качества кода
- "Boy Scout Rule": оставляй код чище, чем нашел

**Preventing Tech Debt:**
- Architecture Decision Records (ADR): документировать архитектурные решения
- Code review checklist: проверка на потенциальный debt
- Definition of Done включает "no new tech debt"
- Refactoring time в estimation

**Источники:**
- [How to Track Technical Debt](https://www.codeant.ai/blogs/track-technical-debt)
- [Beyond DORA Metrics: Engineering Excellence](https://www.thoughtworks.com/en-us/insights/podcasts/technology-podcasts/beyond-dora-metrics-measuring-engineering-excellence)
- [What Are DORA Metrics?](https://devdynamics.ai/blog/what-are-dora-metrics/)

---

## 5. Anti-Patterns to Avoid

### 5.1 PRD Anti-Patterns

| Anti-Pattern | Проблема | Как избежать |
|--------------|----------|--------------|
| **Vagueness & Ambiguity** | "Продукт должен быть простым в использовании" | Используйте конкретные, измеримые формулировки: "Новый пользователь завершает онбординг за < 5 минут" |
| **Writing to Check a Box** | PRD создается "потому что надо", а не для помощи команде | Начинайте с проблемы пользователя, не с шаблона документа |
| **Skipping Stakeholder Input** | Заполнили PRD без консультации с дизайном/маркетингом/разработкой | Проводите PRD review встречи с представителями всех функций |
| **Too Much Detail** | 50-страничный PRD, который никто не читает | Фокус на "что" и "почему", не на "как"; детали в отдельных tech specs |
| **Too Little Detail** | Пробелы → команда делает разные предположения | 5-10 страниц с четкими acceptance criteria и user journeys |
| **Static Document** | PRD не обновляется при изменении требований | Версионирование + change log; PRD — living document |
| **No Success Metrics** | Нет KPI для оценки успеха после запуска | ВСЕГДА определяйте North Star metric + 2-4 supporting metrics |
| **Ignoring Edge Cases** | Фокус только на happy path | Секция "Error Handling & Edge Cases" с 5-10 сценариями |
| **Feature Overload** | Слишком много функций → scope creep | Приоритизация: P0 (must-have), P1 (important), P2 (nice-to-have) |
| **Solutions Without Problems** | Переход к решениям без понимания проблемы | Начинайте с Problem Statement, валидируйте с пользователями |
| **Cumulative Interpretation Errors** | Цепочка неправильных интерпретаций: автор → разработчик → тестировщик | Peer review + walkthrough meeting с командой |
| **Overconfidence Without Validation** | Уверенность в PRD без тестирования с пользователями | Prototype testing с 5-10 пользователями до начала разработки |

**Источники:**
- [Top 10 Mistakes to Avoid When Writing a PRD](https://www.scopilot.ai/top-10-mistakes-to-avoid-when-writing-a-product-requirements-document/)
- [How to Write an Effective PRD](https://www.jamasoftware.com/requirements-management-guide/writing-requirements/how-to-write-an-effective-product-requirements-document/)
- [The Problem with PRDs](https://helixdesign.com/tangents/the-problem-with-product-requirements-documents/)

---

### 5.2 Planning Anti-Patterns

| Anti-Pattern | Проблема | Как избежать |
|--------------|----------|--------------|
| **Over-Optimistic Estimates** | Планирование fallacy: недооценка времени | Используйте pre-mortem analysis; добавьте 20-30% buffer |
| **Ignoring Dependencies** | Не идентифицированы блокеры между задачами | Создайте dependency map + critical path analysis |
| **No Risk Mitigation** | Риски идентифицированы, но нет планов митигации | Для топ-5 рисков: action plan + contingency plan + owner |
| **Single Point of Failure** | Один человек владеет критическим знанием | Bus factor ≥ 2: минимум 2 человека знают каждую систему |
| **Unclear Ownership** | Нет ответственных за задачи (RACI matrix отсутствует) | RACI для каждой ключевой задачи: ровно 1 Accountable |
| **No Phasing Strategy** | Попытка запустить все функции сразу | MVP → Phase 1 → Phase 2; четкие критерии для каждой фазы |
| **Scope Creep** | Требования меняются без переоценки timeline/ресурсов | Change control process: каждое изменение → impact assessment |
| **Waterfall Planning in Agile** | Детальный план на год вперед в быстро меняющемся проекте | Rolling wave planning: детально 1-2 спринта, high-level 1 квартал |

---

### 5.3 Task Breakdown Anti-Patterns

| Anti-Pattern | Проблема | Как избежать |
|--------------|----------|--------------|
| **Too Large Stories** | Истории занимают > 1 спринта | Если estimation > 13 story points → разбить epic |
| **Too Small Stories** | Микрозадачи создают overhead | Минимальный размер: приносит ценность пользователю |
| **Technical Tasks as Stories** | "Refactor database layer" как user story | Технические задачи — enablers, не stories; связать с user value |
| **Dependent Stories** | История A не может начаться без истории B | Используйте epic splitting techniques для независимости |
| **Vague Acceptance Criteria** | "Должно работать хорошо" | Конкретные, testable criteria: "Response time < 200ms при 1000 RPS" |
| **Missing Definition of Done** | Команда не знает, когда история "готова" | DoD определен для команды + AC для каждой истории |
| **No Testability** | AC не поддаются проверке | Каждый AC формулируется как: "Given [context] When [action] Then [outcome]" |

---

### 5.4 Implementation Anti-Patterns

| Anti-Pattern | Проблема | Как избежать |
|--------------|----------|--------------|
| **No Code Review** | Код попадает в main без peer review | Обязательный ≥1 approval для merge |
| **Low Test Coverage** | < 50% code coverage → bugs в production | Quality gate: ≥80% coverage |
| **Skipping Quality Gates** | "Срочно, пропустим тесты" | Автоматизация gates в CI/CD: нельзя обойти |
| **No Performance Testing** | Производительность проверяется только в production | Load testing на staging с 2x ожидаемого трафика |
| **No Rollback Plan** | Деплой без способа откатить изменения | Feature flags + database migration rollback scripts |
| **Big Bang Releases** | Все функции деплоятся сразу в 100% пользователей | Gradual rollout: 5% → 25% → 50% → 100% |
| **Tech Debt Ignored** | "Исправим потом" (но никогда не исправляют) | Tech debt budget: 15-25% capacity каждого спринта |
| **No Monitoring** | Нет алертов на критические метрики | Алерты на: error rate, latency, availability |

---

## 6. Интеграционные рекомендации для Spec Kit

### 6.1 Улучшения для spec-template.md

**Добавить секции:**

#### 1. Amazon-Style Problem Statement
```markdown
## Problem Statement (Customer Pain Points)

### What customer problem are we solving?
[Avoid: "We don't have feature X"]
[Instead: Deep understanding of pain, inefficiency, unmet need]

### Why is this problem worth solving now?
- Market timing / competitive pressure
- Customer feedback / churn reason
- Strategic alignment with company vision

### Press Release (Working Backwards)
**[COMPANY] ANNOUNCES [PRODUCT] TO ENABLE [CUSTOMERS] TO [BENEFIT]**

[1-2 paragraphs describing the solution from customer perspective]
```

#### 2. HEART Metrics Framework
```markdown
## Success Metrics (HEART Framework)

| Metric Category | Goal | Signal | Metric | Current | Target | Deadline |
|-----------------|------|--------|--------|---------|--------|----------|
| **Happiness** | Improve user satisfaction | Users report product is "easy to use" | NPS | 30 | 50 | Q2 2026 |
| **Engagement** | Increase product usage | Users return daily | DAU/MAU ratio | 25% | 40% | Q2 2026 |
| **Adoption** | Faster onboarding | Users complete setup quickly | % users activated in 24h | 60% | 85% | Q2 2026 |
| **Retention** | Reduce churn | Users continue using product | Day 30 retention | 40% | 60% | Q3 2026 |
| **Task Success** | Efficient workflows | Users complete tasks without errors | Task completion rate | 75% | 95% | Q2 2026 |

**North Star Metric**: [Single metric representing customer value]
**Input Metrics**: [2-4 metrics driving North Star]
```

#### 3. Non-Functional Requirements
```markdown
## Non-Functional Requirements

### Performance
- API response time: p50 < 100ms, p95 < 300ms, p99 < 1s
- Page load time: < 2s on 3G connection
- Throughput: support 10,000 requests/second

### Security
- Authentication: OAuth 2.0 + MFA for admin accounts
- Authorization: Role-based access control (RBAC)
- Data encryption: TLS 1.3 in transit, AES-256 at rest
- Compliance: GDPR, SOC2 Type II

### Scalability
- Horizontal scaling: auto-scale to handle 10x traffic spikes
- Database: support 100M records without performance degradation
- Geographic distribution: multi-region deployment (US, EU, APAC)

### Availability
- SLA: 99.9% uptime (max 43 minutes downtime/month)
- Recovery Time Objective (RTO): < 1 hour
- Recovery Point Objective (RPO): < 15 minutes

### Accessibility
- WCAG 2.1 Level AA compliance
- Screen reader support (NVDA, JAWS, VoiceOver)
- Keyboard navigation for all functionality
```

#### 4. Edge Cases & Error Handling
```markdown
## Edge Cases & Error Handling

| Scenario | Expected Behavior |
|----------|-------------------|
| User enters invalid email format | Show inline error: "Please enter a valid email address" |
| API third-party service is down | Fallback to cached data + notify user "Some features temporarily unavailable" |
| File upload > 10MB | Reject with error: "File size must be < 10MB" |
| Concurrent edits by 2 users | Last write wins + notify first user "Document was updated by [User]" |
| Payment processing fails | Retry 3 times with exponential backoff → show user-friendly error |
```

#### 5. Out of Scope (Critical!)
```markdown
## Out of Scope (Non-Goals)

**Explicitly NOT included in this release:**
- Mobile app support (planned for Q3)
- Integration with Salesforce (future consideration)
- Real-time collaboration features (separate project)
- Admin analytics dashboard (Phase 2)

**Why these are out of scope:**
- Prioritizing core user value first (80/20 rule)
- Resource constraints / timeline
- Awaiting technical dependencies
```

---

### 6.2 Улучшения для plan-template.md

**Добавить секции:**

#### 1. RFC-Style Architecture Section
```markdown
## Technical Architecture (RFC)

### High-Level Design
[Architecture diagram: components, data flow, integrations]

### Components
- **Frontend**: React 18 + TypeScript, Vite bundler
- **Backend**: Node.js 20 + Express, TypeScript
- **Database**: PostgreSQL 15 (primary), Redis 7 (cache)
- **Infrastructure**: AWS ECS Fargate, RDS, ElastiCache

### API Design
**New Endpoints:**
- `POST /api/v2/products/filter` - Filter products by criteria
- `GET /api/v2/products/:id/recommendations` - Get product recommendations

**Changes to Existing Endpoints:**
- `GET /api/v1/products` - Add `?price_min=X&price_max=Y` query params

### Database Schema Changes
```sql
-- New table for price history
CREATE TABLE price_history (
  id SERIAL PRIMARY KEY,
  product_id INTEGER REFERENCES products(id),
  price DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast price range queries
CREATE INDEX idx_products_price ON products(price);
```

### Third-Party Dependencies
- **New**: Stripe API v2023-10-16 (payment processing)
- **Updated**: SendGrid API v3 → v4 (email notifications)

### Alternatives Considered
#### Alternative 1: Client-side filtering
- **Pros**: Simpler backend, faster initial development
- **Cons**: Poor performance with large datasets, no server-side caching
- **Rejected because**: Scalability concerns (100K+ products)
```

#### 2. Pre-Mortem Risk Analysis
```markdown
## Pre-Mortem Risk Analysis

**Scenario: "This project failed spectacularly. Why?"**

| Failure Mode | Impact (1-5) | Likelihood (1-5) | Risk Score | Mitigation Strategy | Owner |
|--------------|--------------|------------------|------------|---------------------|-------|
| Stripe API rate limits exceeded during peak | 5 | 3 | 15 | Implement request queuing + circuit breaker pattern | Backend Lead |
| Database query performance degrades at scale | 5 | 4 | 20 | Load testing with 10x data + query optimization | DBA |
| Third-party email service outage | 3 | 3 | 9 | Implement retry logic + fallback to backup provider | DevOps |
| Users don't understand new filtering UI | 4 | 4 | 16 | Usability testing with 10 users before launch | Product Designer |
| Team underestimates complexity (timeline slip) | 4 | 4 | 16 | Add 30% buffer to estimates + weekly check-ins | Project Manager |

**Top 3 Risks (Score ≥15):**
1. **Database performance**: Weekly load testing starting Sprint 2
2. **Stripe rate limits**: Implement queuing in Sprint 1 (before integration)
3. **Timeline slip**: Bi-weekly velocity tracking + scope adjustment if needed
```

#### 3. RACI Matrix
```markdown
## Responsibility Assignment (RACI)

| Task | PM | Eng Lead | Backend Dev | Frontend Dev | Designer | QA | DevOps |
|------|----|----|---------|---------|----------|----|----|
| Define requirements | **A** | C | C | C | C | I | I |
| API design | C | **A** | **R** | C | I | I | I |
| Database schema | C | **A** | **R** | I | I | I | C |
| UI mockups | C | I | I | C | **A/R** | I | I |
| Frontend implementation | C | C | I | **A/R** | C | I | I |
| Backend implementation | C | **A** | **R** | I | I | I | C |
| Write tests | C | C | **R** | **R** | I | **A** | I |
| Deploy to staging | I | C | I | I | I | C | **A/R** |
| Production deployment | A | C | I | I | I | C | **R** |
| Monitor post-launch | **A** | C | C | C | I | C | **R** |

**Legend**: R = Responsible, A = Accountable, C = Consulted, I = Informed
```

#### 4. Dependency Map & Critical Path
```markdown
## Dependencies & Critical Path

### Internal Dependencies
- [ ] **Design team**: Mockups needed by Sprint 1, Day 3 (blocks frontend dev)
- [ ] **Platform team**: Redis cluster provisioning by Sprint 1, Day 5 (blocks caching implementation)
- [ ] **Security team**: Security review approval before production deploy

### External Dependencies
- [ ] **Stripe**: API key & webhook setup (lead time: 2-3 days)
- [ ] **AWS**: Increase RDS instance size quota (lead time: 1 week)

### Critical Path (Longest dependency chain)
```
Requirements (3d) → Design Mockups (5d) → Frontend Dev (10d) → Integration Testing (3d) → Production Deploy (1d)
= 22 days total
```

**Non-critical tasks (have float):**
- Backend API development can start in parallel with frontend
- Documentation can be written throughout sprints
```

#### 5. Rollout Strategy
```markdown
## Rollout Strategy

### Phase 1: Internal Beta (Week 1)
- [ ] Deploy to staging with feature flag `price_filter_enabled: false`
- [ ] Enable for internal employees only (10 users)
- [ ] Collect feedback via Slack channel #price-filter-beta

### Phase 2: Canary Release (Week 2)
- [ ] Enable for 5% of production users
- [ ] Monitor error rate (rollback if > 1%), latency (rollback if p95 > 500ms)
- [ ] A/B test: measure engagement vs control group

### Phase 3: Gradual Rollout (Week 3-4)
- [ ] 25% of users (if metrics healthy)
- [ ] 50% of users (if no degradation)
- [ ] 100% of users (final rollout)

### Rollback Plan
- Feature flag toggle: disable in 30 seconds via LaunchDarkly
- Database migration rollback script: `migrations/rollback_price_filter.sql`
- Monitoring thresholds:
  - Error rate > 1% → auto-rollback
  - API latency p95 > 500ms → alert team
  - User complaints > 10 in 1 hour → investigate
```

---

### 6.3 Улучшения для tasks-template.md

**Добавить секции:**

#### 1. INVEST Compliance Check
```markdown
## User Stories (INVEST Criteria)

### Story 1: Price Range Filter UI
**As a** shopper
**I want** to filter products by price range
**So that** I can find items within my budget

**INVEST Check:**
- ✅ **Independent**: Can be developed without other stories
- ✅ **Negotiable**: Implementation details (slider vs input fields) flexible
- ✅ **Valuable**: Directly helps users find affordable products
- ✅ **Estimable**: Team estimates 5 story points
- ✅ **Small**: Can complete in 1 sprint
- ✅ **Testable**: Clear acceptance criteria below

**Acceptance Criteria:**
1. ✅ User sees min/max price input fields on product listing page
2. ✅ Entering min price filters to show only products ≥ min price
3. ✅ Entering max price filters to show only products ≤ max price
4. ✅ Entering both filters to show products within range
5. ✅ Invalid inputs show error: "Please enter a valid price"

**Estimation**: 5 story points
**Priority**: P0 (Must-have for MVP)
```

#### 2. Definition of Done (Universal)
```markdown
## Definition of Done (Applies to ALL Tasks)

### Code Quality
- [ ] Code reviewed by ≥1 senior engineer
- [ ] No SonarQube critical issues
- [ ] Linting rules passing (ESLint/Prettier)
- [ ] No commented-out code or debug logs

### Testing
- [ ] Unit tests written (≥80% coverage)
- [ ] Integration tests passing
- [ ] Manual testing completed by developer
- [ ] QA sign-off (no P0/P1 bugs)

### Security & Performance
- [ ] Security scan passed (Snyk/OWASP)
- [ ] Performance benchmarks met (API < 300ms p95)
- [ ] No secrets in code (GitGuardian check)

### Documentation
- [ ] API docs updated (Swagger/OpenAPI)
- [ ] README updated if needed
- [ ] Inline code comments for complex logic

### Deployment
- [ ] Feature flag implemented (if applicable)
- [ ] Database migrations backward compatible
- [ ] Deployed to staging + smoke tests passed
- [ ] Rollback plan documented

### Sign-off
- [ ] Product Owner accepts story
- [ ] Design review (if UI changes)
```

#### 3. Task Breakdown with Dependencies
```markdown
## Task Breakdown

### Sprint 1: Foundation & Backend (Weeks 1-2)

#### Task 1.1: Database Schema Updates
**Owner**: Backend Developer
**Estimation**: 1 day
**Dependencies**: None
**Blocks**: Task 1.2, 1.3

**Subtasks:**
- [ ] Create `price_history` table
- [ ] Add index `idx_products_price` for fast queries
- [ ] Write migration script + rollback script
- [ ] Test migration on staging database

**DoD Checklist:**
- [ ] Migration runs successfully on staging
- [ ] Rollback tested
- [ ] Database load test: queries < 50ms with 1M records

---

#### Task 1.2: Price Filter API Endpoint
**Owner**: Backend Developer
**Estimation**: 3 days
**Dependencies**: Task 1.1 (database schema)
**Blocks**: Task 2.1 (frontend integration)

**Subtasks:**
- [ ] Implement `GET /api/v2/products?price_min=X&price_max=Y`
- [ ] Add input validation (price must be positive number)
- [ ] Write unit tests (≥80% coverage)
- [ ] Write integration tests (test with real database)
- [ ] API documentation (Swagger)

**DoD Checklist:**
- [ ] API returns correct filtered results
- [ ] Performance: response < 200ms with 100K products
- [ ] Error handling: returns 400 for invalid inputs
- [ ] Unit tests: 85% coverage
- [ ] Swagger docs updated

---

### Sprint 2: Frontend & Integration (Weeks 3-4)

#### Task 2.1: Price Filter UI Component
**Owner**: Frontend Developer
**Estimation**: 3 days
**Dependencies**: Task 1.2 (API endpoint ready)
**Blocks**: Task 2.3 (E2E tests)

**Subtasks:**
- [ ] Create PriceFilter React component (TypeScript)
- [ ] Add min/max price input fields with validation
- [ ] Integrate with backend API (`/api/v2/products`)
- [ ] Handle loading states and errors
- [ ] Write unit tests (React Testing Library)

**DoD Checklist:**
- [ ] Component renders on product listing page
- [ ] Real-time filtering as user types
- [ ] Error messages for invalid inputs
- [ ] Unit tests: 90% coverage
- [ ] Accessibility: keyboard navigation works
```

#### 4. Dependency Visualization
```markdown
## Dependency Graph

```
Sprint 1:
Task 1.1 (DB Schema) → Task 1.2 (API) → Task 2.1 (Frontend UI)
                         ↓
                    Task 1.3 (Cache) → Task 2.2 (Performance)
                         ↓
Sprint 2:
Task 2.1 (Frontend) + Task 2.2 (Performance) → Task 2.3 (E2E Tests) → Task 3.1 (Deploy)
                                                                           ↓
Sprint 3:
                                                                    Task 3.2 (Monitor)
```

**Critical Path**: 1.1 → 1.2 → 2.1 → 2.3 → 3.1 (total: 12 days)
**Float**: Task 1.3 has 2 days float (can delay without impacting deadline)
```

---

### 6.4 Новый Template: quality-gates-template.md

```markdown
# Quality Gates Checklist

## Pre-Development Gates

### Requirements Completeness
- [ ] Problem statement clearly defined (customer pain point)
- [ ] Success metrics identified (HEART framework)
- [ ] User stories meet INVEST criteria
- [ ] Acceptance criteria testable and specific
- [ ] Non-functional requirements defined (performance, security)
- [ ] Edge cases documented
- [ ] Out-of-scope items explicitly listed

### Architecture & Design
- [ ] RFC/Design doc reviewed and approved
- [ ] Architecture diagram created
- [ ] Database schema reviewed (if applicable)
- [ ] API contracts defined (OpenAPI/Swagger)
- [ ] Third-party dependencies identified
- [ ] Alternatives considered and documented
- [ ] Pre-mortem risk analysis completed

---

## Development Gates

### Code Commit Quality Gate
- [ ] Linting rules passing (no errors)
- [ ] Code formatted (Prettier/Black/gofmt)
- [ ] Pre-commit hooks passing
- [ ] No secrets/credentials in code

### Pull Request Quality Gate
- [ ] ≥1 peer review approval
- [ ] All review comments addressed
- [ ] Code coverage ≥80% (no decrease from baseline)
- [ ] Static analysis passing (SonarQube quality gate)
- [ ] Security scan: 0 critical vulnerabilities
- [ ] Unit tests: 100% passing
- [ ] No merge conflicts

### Build Quality Gate
- [ ] Compilation successful
- [ ] Unit tests: 100% pass rate
- [ ] Integration tests: passing
- [ ] Docker image builds successfully
- [ ] Build time < 15 minutes

---

## Testing Gates

### Functional Testing
- [ ] All acceptance criteria validated
- [ ] User flows tested end-to-end
- [ ] Error handling tested (invalid inputs, timeouts)
- [ ] Edge cases covered
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Mobile responsive testing (if applicable)

### Performance Testing
- [ ] Load testing: handles 2x expected traffic
- [ ] API response time: p95 < 300ms
- [ ] Page load time: < 2s on 3G
- [ ] Database queries optimized (< 50ms)
- [ ] No memory leaks (profiling completed)

### Security Testing
- [ ] OWASP Top 10 vulnerabilities checked
- [ ] Dependency scan: no critical CVEs
- [ ] Authentication/authorization tested
- [ ] SQL injection / XSS tests passed
- [ ] Secrets management verified (no hardcoded keys)

---

## Deployment Gates

### Staging Deployment
- [ ] Smoke tests passing
- [ ] E2E tests passing
- [ ] Database migrations successful
- [ ] No regressions in key user flows
- [ ] Rollback plan tested

### Production Deployment
- [ ] Feature flag configured (gradual rollout)
- [ ] Monitoring & alerting set up
- [ ] Error rate < 0.1% (rollback if exceeds)
- [ ] Response time within SLA
- [ ] Rollback tested and ready
- [ ] On-call engineer assigned

### Gradual Rollout Checklist
- [ ] Phase 1: 5% of users (monitor 24h)
- [ ] Phase 2: 25% of users (monitor 24h)
- [ ] Phase 3: 50% of users (monitor 24h)
- [ ] Phase 4: 100% of users

**Rollback Criteria:**
- Error rate > 1%
- API latency p95 > 500ms
- User complaints > 10/hour

---

## Post-Launch Gates

### Monitoring & Success Metrics
- [ ] North Star metric tracked (dashboard set up)
- [ ] HEART metrics monitored:
  - [ ] Happiness (NPS/CSAT)
  - [ ] Engagement (DAU/MAU)
  - [ ] Adoption (activation rate)
  - [ ] Retention (cohort analysis)
  - [ ] Task Success (completion rate)
- [ ] Error logs reviewed daily (first week)
- [ ] Performance metrics within targets
- [ ] No critical bugs reported

### Documentation & Knowledge Transfer
- [ ] API documentation updated
- [ ] User-facing documentation updated
- [ ] Internal runbook created (troubleshooting)
- [ ] Team demo/training completed
- [ ] Post-mortem scheduled (2 weeks post-launch)

---

## DORA Metrics Tracking

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **Deployment Frequency** | Weekly | [TBD] | 🟢/🟡/🔴 |
| **Lead Time for Changes** | < 1 week | [TBD] | 🟢/🟡/🔴 |
| **Change Failure Rate** | < 5% | [TBD] | 🟢/🟡/🔴 |
| **Mean Time to Recovery** | < 1 hour | [TBD] | 🟢/🟡/🔴 |
```

---

### 6.5 Новый Template: tech-debt-register-template.md

```markdown
# Technical Debt Register

**Project**: [Project Name]
**Last Updated**: [Date]
**Owner**: [Engineering Lead]

---

## Current Tech Debt Inventory

| ID | Description | Type | Impact | Effort | Risk Score | Owner | Status | Target Date |
|----|-------------|------|--------|--------|------------|-------|--------|-------------|
| TD-001 | No unit tests for authentication module | Testing | High (5) | 2 weeks | 15 | Security Team | Planned | Q2 2026 |
| TD-002 | Monolithic database (scaling bottleneck) | Architecture | High (5) | 8 weeks | 12 | Platform Team | In Progress | Q3 2026 |
| TD-003 | Legacy jQuery code in admin panel | Maintenance | Medium (3) | 3 weeks | 9 | Frontend Team | Backlog | Q4 2026 |
| TD-004 | Hardcoded configuration values | DevOps | Low (2) | 1 week | 4 | DevOps Team | Backlog | 2027 |

**Risk Score = Impact (1-5) × Likelihood of causing issue (1-5)**

---

## Tech Debt Types

- **Code Quality**: Code smells, duplication, complex functions
- **Testing**: Missing tests, low coverage
- **Architecture**: Monoliths, tight coupling, poor scalability
- **Security**: Unpatched vulnerabilities, outdated dependencies
- **DevOps**: Manual processes, lack of automation
- **Documentation**: Missing/outdated docs
- **Performance**: Slow queries, N+1 problems, memory leaks

---

## Metrics Dashboard

### Code Quality Metrics
- **Code Coverage**: 65% → Target: 80% (by Q3 2026)
- **SonarQube Issues**: 45 critical → Target: < 10
- **Cyclomatic Complexity**: Avg 8.2 → Target: < 5
- **Code Duplication**: 12% → Target: < 5%

### Productivity Metrics
- **Build Time**: 18 minutes → Target: < 10 minutes
- **Deployment Frequency**: Bi-weekly → Target: Daily (DORA Elite)
- **Mean Time to Fix Bug**: 3 days → Target: 1 day
- **Developer Satisfaction**: 6.5/10 → Target: 8/10

### Business Impact Metrics
- **Feature Velocity**: 3 features/month → Target: 5 features/month
- **Production Incidents**: 8/month → Target: < 2/month
- **Customer-Reported Bugs**: 15/month → Target: < 5/month

---

## Prioritization Matrix

```
     HIGH BUSINESS IMPACT
            │
  CRITICAL  │  QUICK WINS
  (TD-001)  │  (TD-004)
────────────┼────────────────
  MONITOR   │  AVOID
  (TD-003)  │
            │
     LOW BUSINESS IMPACT

  LOW EFFORT    HIGH EFFORT
```

---

## Tech Debt Budget

**Quarterly Allocation:**
- **Q1 2026**: 20% sprint capacity (1 day/week)
- **Q2 2026**: 25% sprint capacity (targeting TD-001, TD-002)
- **Q3 2026**: 15% sprint capacity (maintenance mode)

**Boy Scout Rule**: Leave code cleaner than you found it (every commit)

---

## Prevention Strategies

- [ ] Architecture Decision Records (ADR) for all major decisions
- [ ] Code review checklist includes "Does this add tech debt?"
- [ ] Definition of Done includes "No new tech debt introduced"
- [ ] Refactoring time included in story estimates
- [ ] Monthly tech debt review meeting

---

## Recent Debt Resolved

| ID | Description | Resolved Date | Outcome |
|----|-------------|---------------|---------|
| TD-005 | Migrated from MongoDB to PostgreSQL | 2025-12-15 | Performance improved 40%, query complexity reduced |
| TD-006 | Upgraded Node.js 14 → 20 | 2025-11-20 | Security vulnerabilities eliminated, build time -30% |
```

---

## Резюме

Это исследование охватывает:

1. **Specification Excellence**:
   - Amazon Working Backwards (PR/FAQ)
   - Google HEART Framework
   - Airbnb 11-Star Experience
   - Stripe Context & DRI
   - Critical PRD sections от топ-компаний

2. **Planning Excellence**:
   - McKinsey/BCG frameworks (BCG Matrix, 7S, GE-McKinsey)
   - RACI Matrix для ownership
   - Dependency Mapping & Critical Path
   - Pre-Mortem Analysis для risk mitigation

3. **Task Breakdown Excellence**:
   - INVEST criteria для user stories
   - 8 паттернов для epic splitting
   - Spotify/Netflix dependency management
   - Definition of Done vs Acceptance Criteria

4. **Implementation Excellence**:
   - Engineering RFC process (Google, Uber, Stripe)
   - Quality Gates & Testing Strategy
   - DORA metrics для engineering excellence
   - Technical Debt tracking frameworks

5. **Anti-Patterns**: 13+ анти-паттернов с решениями

6. **Интеграция в Spec Kit**: Конкретные улучшения для всех templates

---

## Источники

### Specification Excellence
- [12 Real PRD Examples from Top Tech Companies](https://pmprompt.com/blog/prd-examples)
- [Amazon Working Backwards Template](https://www.hustlebadger.com/what-do-product-teams-do/amazon-working-backwards-process/)
- [Working Backwards: The Amazon PR/FAQ](https://productstrategy.co/working-backwards-the-amazon-prfaq-for-product-innovation/)
- [How to Use Google's HEART Framework](https://www.productplan.com/learn/heart-framework-product-decisions/)
- [HEART Framework for Software UX](https://amplitude.com/blog/heart-framework-software-ux)
- [How Great Design Was Key to Airbnb's Success](https://passionates.com/how-great-design-key-to-airbnbs-massive-success/)
- [Building Beautiful Products with Stripe](https://www.lennysnewsletter.com/p/building-beautiful-products-with)

### Planning Excellence
- [MBB Frameworks Bundle](https://www.eloquens.com/tool/vqPVi0dJ/strategy/mbb-mckinsey-bain-bcg-frameworks/mbb-mckinsey-bcg-bain-models-and-frameworks-bundle)
- [RACI Matrix Guide](https://project-management.com/understanding-responsibility-assignment-matrix-raci-matrix/)
- [RACI Chart: What is it & How to Use](https://www.atlassian.com/work-management/project-management/raci-chart)
- [What is Dependency Mapping?](https://miro.com/project-management/what-is-dependency-mapping/)
- [How to Identify Project Risks with Pre-Mortem](https://seriousplaybusiness.com/project-pre-mortem-risk-identification/)

### Task Breakdown Excellence
- [INVEST Criteria in SAFe](https://www.leanwisdom.com/blog/crafting-high-quality-user-stories-with-the-invest-criteria-in-safe/)
- [Splitting Epics and User Stories](https://premieragile.com/splitting-epics-and-user-stories/)
- [Definition of Done vs Acceptance Criteria](https://www.visual-paradigm.com/scrum/definition-of-done-vs-acceptance-criteria/)
- [How Spotify Improved Developer Productivity](https://engineering.atspotify.com/2020/08/how-we-improved-developer-productivity-for-our-devops-teams)

### Implementation Excellence
- [Software Engineering RFC Examples](https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design)
- [Companies Using RFCs](https://blog.pragmaticengineer.com/rfcs-and-design-docs/)
- [Software Quality Gates](https://testrigor.com/blog/software-quality-gates/)
- [What Are DORA Metrics?](https://linearb.io/blog/dora-metrics)
- [How to Track Technical Debt](https://www.codeant.ai/blogs/track-technical-debt)

### Anti-Patterns
- [Top 10 PRD Mistakes to Avoid](https://www.scopilot.ai/top-10-mistakes-to-avoid-when-writing-a-product-requirements-document/)
- [How to Write an Effective PRD](https://www.jamasoftware.com/requirements-management-guide/writing-requirements/how-to-write-an-effective-product-requirements-document/)

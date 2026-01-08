# Spec-Kit Commands Guide

Полное руководство по всем командам Spec-Kit: последовательность выполнения, флаги и аргументы.

## Содержание

- [Основной Workflow](#основной-workflow)
- [Детальное описание команд](#детальное-описание-команд)
- [Вспомогательные команды](#вспомогательные-команды)
- [Специальные режимы](#специальные-режимы)

---

## Основной Workflow

### Greenfield проекты (новые проекты)

```mermaid
graph TD
    A[/speckit.constitution] --> B{Размер проекта}
    B -->|50+ требований| C[/speckit.concept]
    B -->|<50 требований| D[/speckit.specify]
    C --> E[/speckit.validate-concept]
    E --> D
    D --> F[/speckit.clarify]
    F --> G[/speckit.design]
    G --> H[/speckit.plan]
    H --> I[/speckit.tasks]
    I --> J[/speckit.staging]
    J --> K[/speckit.analyze]
    K --> L[/speckit.implement]
    L --> M[/speckit.merge]
```

### Brownfield проекты (существующие кодовые базы)

```mermaid
graph TD
    A[/speckit.constitution] --> B[/speckit.baseline]
    B --> C[/speckit.specify]
    C --> D[/speckit.plan]
    D --> E[/speckit.tasks]
    E --> F[/speckit.staging]
    F --> G[/speckit.implement]
    G --> H[/speckit.merge]
```

---

## Детальное описание команд

### 1. `/speckit.constitution`

**Назначение:** Создание или обновление проектной конституции с интерактивным опросником

**Аргументы:**
```bash
/speckit.constitution                    # Интерактивный режим (3 вопроса)
/speckit.constitution set domain fintech # Установка домена
/speckit.constitution set language ru    # Установка языка
/speckit.constitution --merge            # Показать объединённую конституцию
```

**Интерактивный режим (если без аргументов):**

При запуске без аргументов, команда задаёт 3 вопроса:

1. **Тип приложения**: Web / Mobile / API / CLI / Desktop / Other
2. **Домен**: SaaS / E-commerce / Fintech / Healthcare / Gaming / General
3. **Язык артефактов**: English (en) / Russian (ru) / Other

На основе ответов:
- Применяются соответствующие принципы (WEB, API, SEC, etc.)
- Копируется доменный файл в `constitution.domain.md`
- Устанавливается язык в Project Settings

**Когда использовать:**
- ✅ Сразу после `specify init` (первая команда)
- ✅ При изменении архитектурных принципов
- ✅ При добавлении новых стандартов качества
- ✅ При смене домена проекта

**Примеры:**
```bash
# Интерактивный режим - AI задаёт 3 вопроса
/speckit.constitution

# Прямая установка домена
/speckit.constitution set domain fintech

# Усиление принципа
/speckit.constitution strengthen QUA-001 to MUST with 95% coverage

# Добавление принципа
/speckit.constitution add principle: all API responses must include request-id header
```

**Выходные файлы:**
- `memory/constitution.md` - проектная конституция (Layer 2)
- `memory/constitution.base.md` - базовые принципы (Layer 0, read-only)
- `memory/constitution.domain.md` - доменные принципы (Layer 1, опционально)

**Модель:** `opus` (высшее качество для архитектурных решений)

---

### 2. `/speckit.concept`

**Назначение:** Захват полного концепта продукта перед детальной спецификацией (для крупных проектов)

**Аргументы:**
```bash
/speckit.concept <free-text-product-description>
```

**Параметры:**
- `<free-text-product-description>` - описание продукта, рынка, целей

**Флаги:** Нет

**Когда использовать:**
- ✅ Проекты с 50+ требованиями
- ✅ Новые продукты (требуется market research)
- ✅ Нужна Epic → Feature → Story иерархия
- ⛔ Малые фичи (<50 требований) - используйте `/speckit.specify`

**Что генерируется:**
- **Core Sections** (CQS ≥60): Базовая информация
- **Strategic Sections** (CQS ≥80): Market research, конкуренты
- **Advanced Sections** (CQS ≥90): Риски, pivot критерии

**Пример:**
```bash
/speckit.concept Build a SaaS platform for team collaboration with real-time editing, targeting remote teams of 10-50 people. Key differentiator: AI-powered task prioritization.
```

**Выходные файлы:**
- `specs/concept.md` - полный концепт продукта
- Включает: TAM/SAM/SOM, конкурентный анализ, JTBD personas, Wave Planning, **Ready-to-Execute Commands**

**Модель:** `opus`

**Новое в v0.0.81:**
Автоматически генерирует готовые команды `/speckit.specify` в 4 вариантах:
1. **По волнам (RECOMMENDED)** - Wave 1, Wave 2, Wave 3+
2. **По эпикам** - EPIC-001, EPIC-002...
3. **По приоритетам** - P1a, P1b, P2, P3
4. **Весь концепт целиком** - все stories в одной команде

---

### 3. `/speckit.validate-concept`

**Назначение:** Повторная валидация существующего концепта против текущих рыночных условий

**Аргументы:**
```bash
/speckit.validate-concept
```

**Параметры:** Нет (использует существующий `specs/concept.md`)

**Флаги:** Нет

**Когда использовать:**
- ✅ Ежемесячно/ежеквартально для проверки актуальности
- ✅ После значительных рыночных событий
- ✅ Перед major pivot решениями

**Что проверяется:**
- Изменения в TAM/SAM/SOM
- Новые конкуренты / изменения в ценообразовании
- Тренды и сигналы роста
- Регуляторные изменения

**Выходные файлы:**
- `specs/concept-validation-{date}.md` - отчет с diff и CQS delta

**Модель:** `sonnet`

---

### 4. `/speckit.specify`

**Назначение:** Создание детальной спецификации фичи (что и почему, не как)

**Аргументы:**
```bash
# Standalone режим (новая фича)
/speckit.specify <feature-description>

# Concept-driven режим (из концепта)
/speckit.specify EPIC-001.F01.S01, EPIC-001.F01.S02
```

**Параметры:**
- `<feature-description>` - описание фичи на естественном языке
- `EPIC-XXX.FXX.SXX` - Story IDs из концепта (через запятую)

**Флаги:**
- `--init` - создать feature directory без генерации spec
- `--skip-validate` - пропустить pre-handoff validation

**Когда использовать:**
- ✅ После `/speckit.concept` (concept-driven)
- ✅ Для standalone фич (<50 требований)
- ✅ После `/speckit.baseline` (brownfield)

**Пример:**
```bash
# Standalone
/speckit.specify Add user authentication with OAuth2 and JWT tokens

# Из концепта (Wave 1 Foundation)
/speckit.specify EPIC-001.F01.S01, EPIC-001.F01.S02, EPIC-001.F02.S01
```

**Выходные файлы:**
- `specs/NNN-feature-name/spec.md` - спецификация фичи
- Включает: FR-xxx (functional requirements), NFR-xxx (non-functional), AS-xxx (acceptance scenarios)

**Модель:** `opus`

**Quality Gates:**
- SQS ≥ 80 для перехода к планированию

---

### 5. `/speckit.clarify`

**Назначение:** Выявление недостаточно специфицированных областей через целевые вопросы

**Аргументы:**
```bash
/speckit.clarify
```

**Параметры:** Нет (использует текущий `spec.md`)

**Флаги:** Нет

**Когда использовать:**
- ✅ Автоматически вызывается при SQS < 80
- ✅ Много `[NEEDS CLARIFICATION]` маркеров в spec
- ✅ Обнаружены ambiguities в `/speckit.analyze`

**Режимы работы:**
1. **Heuristic Pattern Matching** - быстрое выявление vague terms
2. **LLM Metacognitive Analysis** - глубокий анализ
3. **Cross-Requirement Consistency** - проверка противоречий

**Что обнаруживает:**
- Vague terms: "fast", "secure", "user-friendly"
- Missing quantities: retention без указания срока
- Unclear actors: "the system" без уточнения
- Conditional gaps: "if X" без "else"

**Выходные файлы:**
- Обновленный `specs/NNN-feature/spec.md` с clarifications

**Модель:** `sonnet`

---

### 6. `/speckit.design`

**Назначение:** Создание визуальных спецификаций и дизайн-систем

**Аргументы:**
```bash
# Feature design режим (из spec)
/speckit.design

# Design system режим
/speckit.design --design-system

# Concept design режим (весь app из концепта)
/speckit.design --concept

# Mockup generation режим
/speckit.design --mockup
```

**Флаги:**
- `--design-system` - генерация полной design system
- `--concept` - дизайн всего app из concept.md
- `--wave N` - дизайн конкретной волны (с --concept)
- `--all` - дизайн всех волн сразу (с --concept)
- `--mockup` - генерация high-fidelity mockups через Google Stitch
- `--screens "screen1,screen2"` - retry для конкретных экранов (с --mockup)
- `--promo` - генерация promo материалов

**Когда использовать:**
- ✅ После `/speckit.specify` для UI-heavy фич
- ✅ Standalone для design system bootstrapping
- ✅ После concept для app-wide дизайна

**Агенты:**
- `ux-designer-agent` - user flows, wireframes, interactions
- `product-designer-agent` - visual language, code generation
- `motion-designer-agent` - animation system
- `promo-designer-agent` - landing pages (с --promo)

**Выходные файлы:**
- `specs/NNN-feature/design.md` - design specs
- `specs/app-design/` - для concept design режима
- `.preview/stitch-mockups/` - для mockup режима

**Модель:** `opus`

---

### 7. `/speckit.plan`

**Назначение:** Создание технического плана реализации (как)

**Аргументы:**
```bash
/speckit.plan
```

**Параметры:** Нет (использует текущий `spec.md`)

**Флаги:**
- `--skip-validate` - пропустить pre-handoff validation
- `--fast` - быстрая валидация (Tier 1-2 только)

**Когда использовать:**
- ✅ После `/speckit.specify` (автоматически через handoff)
- ✅ SQS ≥ 80
- ✅ Все `[NEEDS CLARIFICATION]` разрешены

**Режимы валидации:**
- **Progressive validation** - 4-tier система (см. `templates/shared/validation/checkpoints.md`)
- **Early exit** при confidence ≥ 0.95

**Выходные файлы:**
- `specs/NNN-feature/plan.md` - implementation plan
- `specs/NNN-feature/research.md` - Phase 0 research findings
- `specs/NNN-feature/adrs/ADR-XXX.md` - Architecture Decision Records

**Модель:** `opus`

**Quality Gates:**
- Constitution Alignment Gate (CRITICAL)
- Tech Consistency Gate (HIGH)

---

### 8. `/speckit.tasks`

**Назначение:** Генерация actionable, dependency-ordered task breakdown

**Аргументы:**
```bash
/speckit.tasks
```

**Параметры:** Нет (использует `plan.md`)

**Флаги:** Нет

**Когда использовать:**
- ✅ После `/speckit.plan` (автоматически через handoff)
- ✅ План заполнен (все фазы описаны)
- ✅ `research.md` существует (Phase 0 complete)

**Выходные файлы:**
- `specs/NNN-feature/tasks.md` - task breakdown с зависимостями
- Включает: [DEP:TASK-XXX] для dependency graph

**Модель:** `sonnet`

**Quality Gates:**
- Circular Dependencies Gate (CRITICAL) - блокирует при циклах
- FR Coverage Gate (HIGH) - все FR должны иметь tasks

---

### 9. `/speckit.staging`

**Назначение:** Provision Docker Compose staging environment ПЕРЕД имплементацией для TDD workflow

**Аргументы:**
```bash
/speckit.staging [flags]
```

**Параметры:** Нет (автоматически определяет сервисы из spec/tasks)

**Флаги:**
- `--services <list>` - override сервисов (postgres,redis,playwright). Comma-separated
- `--skip-playwright` - пропустить Playwright контейнер (для unit-test-only фич)
- `--reset` - пересоздать все сервисы (down + up)
- `--status` - показать текущий статус без изменений
- `--down` - остановить все staging сервисы

**Когда использовать:**
- ✅ После `/speckit.tasks` (автоматически через handoff)
- ✅ ПЕРЕД `/speckit.implement` для TDD
- ✅ Тесты требуют PostgreSQL, Redis или Playwright
- ⛔ НЕ для production деплоя (используйте `/speckit.ship`)

**Сервисы по умолчанию:**
| Сервис | Image | Port | Healthcheck |
|--------|-------|------|-------------|
| PostgreSQL | postgres:16-alpine | 5433 | pg_isready |
| Redis | redis:7-alpine | 6380 | redis-cli ping |
| Playwright | mcr.microsoft.com/playwright:v1.40.0 | - | npx playwright --version |

**Пример:**
```bash
# Полный staging
/speckit.staging

# Только PostgreSQL и Redis (без Playwright)
/speckit.staging --skip-playwright

# Проверить статус
/speckit.staging --status

# Остановить
/speckit.staging --down
```

**Выходные файлы:**
- `.speckit/staging/docker-compose.yaml` - Docker Compose конфигурация
- `.speckit/staging/test-config.env` - переменные окружения для тестов
- `.speckit/state/staging/staging-status.json` - состояние сервисов

**Модель:** `haiku` (быстрый provisioning)

**Quality Gates:**
- **QG-STAGING-001**: All services healthy (CRITICAL)

**Отличие от `/speckit.ship`:**
| Аспект | `/speckit.staging` | `/speckit.ship` |
|--------|-------------------|-----------------|
| **Когда** | ПЕРЕД имплементацией | ПОСЛЕ имплементации |
| **Цель** | Тестовая инфра для TDD | Cloud деплой |
| **Сервисы** | Docker Compose локально | Terraform + K8s |
| **Порты** | 5433, 6380 (не конфликтуют) | По infra.yaml |

---

### 10. `/speckit.analyze`

**Назначение:** Cross-artifact consistency, traceability, QA verification

**Аргументы:**
```bash
# Автоматическое определение профиля
/speckit.analyze

# Явное указание профиля
/speckit.analyze --profile <profile-name>
```

**Профили валидации:**
- `spec_validate` - проверка spec.md
- `plan_validate` - проверка plan.md
- `tasks_validate` - проверка tasks.md
- `qa_mode` - post-implementation QA
- `concept_validate` - проверка concept.md

**Флаги:**
- `--profile <name>` - явное указание профиля валидации
- `--quiet` - тихий режим (минимальный вывод)
- `--skip-validate` - пропустить валидацию

**Когда использовать:**
- ✅ Перед переходом между фазами (автоматически через pre_handoff_action)
- ✅ После `/speckit.implement` (QA mode)
- ✅ Для проверки consistency вручную

**Quality Gates (QG-001 to QG-012):**
- **QG-001**: Constitution Alignment
- **QG-002**: Spec Completeness
- **QG-003**: Plan Consistency
- **QG-004**: Test Coverage ≥ 80%
- **QG-005**: Type Coverage ≥ 95%
- **QG-006**: Lint Cleanliness (0 errors)
- **QG-007**: Performance Baseline (Lighthouse ≥ 90)
- **QG-008**: Accessibility Compliance (WCAG 2.1 AA)
- **QG-009**: Documentation Coverage (100% public APIs)

**Выходные файлы:**
- `specs/NNN-feature/analysis/analysis-report-{timestamp}.md`
- `specs/NNN-feature/analysis/qa-report-{timestamp}.md` (в QA mode)

**Модель:** `sonnet`

---

### 11. `/speckit.implement`

**Назначение:** Выполнение TDD implementation plan с самопроверкой

**Аргументы:**
```bash
/speckit.implement
```

**Параметры:** Нет (использует `tasks.md`)

**Флаги:**
- `--skip-pre-gates` - пропустить pre-implementation gates

**Когда использовать:**
- ✅ После `/speckit.tasks` (автоматически через handoff)
- ✅ Все P1 tasks определены
- ✅ Нет circular dependencies
- ✅ SQS ≥ 80

**Pre-Gates (прогрессивная валидация):**
- **Tier 1 (SYNTAX)**: tasks.md exists, plan.md exists
- **Tier 2 (SEMANTIC)**: No CRITICAL issues
- **Tier 3 (LOGIC)**: Traceability complete
- **Tier 4 (QUALITY)**: Constitution compliance

**Выходные файлы:**
- Исходный код (по tasks.md)
- `specs/NNN-feature/RUNNING.md` - как запустить
- `README.md` - документация

**Модель:** `opus`

**Автоматические handoffs:**
- → `/speckit.analyze --profile qa_mode` после завершения

**Quality Gates (Post-Implement):**
- **QG-004**: Test Coverage ≥ 80%
- **QG-005**: Type Coverage ≥ 95%
- **QG-006**: Lint Cleanliness
- **QG-007**: Performance Baseline
- **QG-008**: Accessibility Compliance
- **QG-009**: Documentation Coverage

---

### 12. `/speckit.merge`

**Назначение:** Финализация фичи и обновление system specs после PR merge

**Аргументы:**
```bash
/speckit.merge
```

**Параметры:** Нет (использует текущую фичу)

**Флаги:** Нет

**Когда использовать:**
- ✅ PR merged в main
- ✅ QA verification passed
- ✅ Готовность к обновлению system specs

**Что делает:**
1. Validates feature spec completeness
2. Updates system specs в `specs/system/`
3. Creates `.merged` file с метаданными
4. Updates feature registry в `specs/features/.manifest.md`

**Выходные файлы:**
- `specs/NNN-feature/.merged` - merge metadata
- `specs/system/*.md` - обновленные system specs
- `specs/features/.manifest.md` - обновленный registry

**Модель:** `sonnet`

---

## Вспомогательные команды

### `/speckit.baseline`

**Назначение:** Захват текущего состояния для brownfield спецификаций

**Аргументы:**
```bash
/speckit.baseline <scope>
```

**Параметры:**
- `<scope>` - file paths, modules, или keywords для захвата

**Когда использовать:**
- ✅ Brownfield проекты (изменение существующего кода)
- ✅ Перед модификацией legacy компонентов

**Выходные файлы:**
- `specs/NNN-feature/baseline.md` - текущее поведение (CB-xxx)

**Модель:** `sonnet`

---

### `/speckit.checklist`

**Назначение:** Генерация custom checklist для валидации качества требований

**Аргументы:**
```bash
/speckit.checklist <domain-requirements>
```

**Параметры:**
- `<domain-requirements>` - описание домена (security, UX, performance и т.д.)

**Когда использовать:**
- ✅ Для domain-specific валидации (security, a11y, UX)
- ✅ "Unit tests для requirements writing"

**Что проверяет:**
- ✅ Completeness - все ли requirements определены
- ✅ Clarity - количественно ли определено "prominent display"
- ✅ Consistency - консистентны ли hover states
- ✅ Coverage - определены ли accessibility requirements

**⛔ НЕ проверяет:**
- ❌ Работает ли код (это не verification)
- ❌ Корректность реализации

**Выходные файлы:**
- `specs/NNN-feature/checklists/{domain}.md`

**Модель:** `sonnet`

---

### `/speckit.list`

**Назначение:** Список всех фич в проекте с их статусами

**Аргументы:**
```bash
/speckit.list [flags]
```

**Флаги:**
- `--verbose` - детальная информация
- `--json` - JSON формат вывода
- `--tree` - древовидная структура
- `--evolution` - эволюция фич (lineage)

**Когда использовать:**
- ✅ Для просмотра всех фич проекта
- ✅ Проверить активную фичу
- ✅ Понять статус development lifecycle

**Модель:** `haiku` (быстрый lookup)

---

### `/speckit.switch`

**Назначение:** Переключение на другую фичу для продолжения работы

**Аргументы:**
```bash
/speckit.switch <feature-id-or-name>
```

**Параметры:**
- `<feature-id-or-name>` - ID фичи (001) или имя

**Когда использовать:**
- ✅ Переключение между фичами
- ✅ Возврат к недоработанной фиче

**Что делает:**
- Updates `.speckit/active` file
- Опционально: `git checkout` соответствующей ветки

**Модель:** `haiku`

---

### `/speckit.extend`

**Назначение:** Расширение merged фичи новыми capabilities

**Аргументы:**
```bash
/speckit.extend <parent-feature> <description>
```

**Параметры:**
- `<parent-feature>` - ID родительской фичи
- `<description>` - описание расширения

**Когда использовать:**
- ✅ Добавление capabilities к merged фиче
- ✅ Сохранение Feature Lineage

**Что делает:**
- Создает новую фичу с Feature Lineage
- Загружает контекст из parent spec
- Предзаполняет систему constraints

**Модель:** `sonnet`

---

### `/speckit.taskstoissues`

**Назначение:** Конвертация tasks.md в GitHub Issues

**Аргументы:**
```bash
/speckit.taskstoissues
```

**Параметры:** Нет (использует `tasks.md`)

**Флаги:** Нет

**Когда использовать:**
- ✅ После генерации tasks.md
- ✅ Работа через GitHub Issues

**Требования:**
- GitHub MCP server настроен
- `tasks.md` существует

**Модель:** `sonnet`

---

### `/speckit.preview`

**Назначение:** Генерация интерактивных preview из design specs

**Аргументы:**
```bash
/speckit.preview
```

**Параметры:** Нет (использует `design.md`)

**Флаги:** Нет

**Когда использовать:**
- ✅ После `/speckit.design`
- ✅ Визуализация wireframes → HTML
- ✅ Component previews

**Выходные файлы:**
- `.preview/wireframes/` - HTML из ASCII wireframes
- `.preview/components/` - component previews
- `.preview/screenshots/` - captured screenshots

**Модель:** `opus`

---

## Специальные режимы

### `/speckit.discover`

**Назначение:** Customer discovery для валидации problem-solution fit

**Аргументы:**
```bash
/speckit.discover --problem "<hypothesis>" --persona "<target>" --method <interviews|survey|landing_page|all>
```

**Флаги:**
- `--problem` - problem hypothesis
- `--persona` - target persona
- `--method` - validation method

**Когда использовать:**
- ✅ Перед `/speckit.concept` для новых продуктов
- ✅ Validation required

**Выходные файлы:**
- `docs/discover/hypothesis.md`
- `docs/discover/interview-guide.md` - Mom Test скрипт
- `docs/discover/analysis.md`
- `docs/discover/decision.md` - Go/No-Go

**Quality Gates:**
- `minimum_interviews`: ≥10 interviews OR ≥50 survey responses OR ≥5% landing conversion
- `signal_strength`: avg_problem_severity ≥3.5

**Модель:** `opus`

---

### `/speckit.migrate`

**Назначение:** Планирование и выполнение spec-driven миграций

**Аргументы:**
```bash
/speckit.migrate <migration-description>
```

**Параметры:**
- `<migration-description>` - описание миграции (architecture, version, cloud)

**Когда использовать:**
- ✅ Monolith → Microservices
- ✅ Version upgrades (Python 2 → 3)
- ✅ Cloud migrations (AWS → GCP)

**Выходные файлы:**
- `specs/NNN-migration/migration-plan.md` - с MIG-xxx фазами
- Включает: Strangler Fig strategy, rollback strategies

**Модель:** `opus`

---

### `/speckit.properties`

**Назначение:** Генерация property-based tests через EARS transformation

**Аргументы:**
```bash
/speckit.properties [language-targets]
```

**Параметры:**
- `[language-targets]` - языки для генерации (Python, TypeScript и т.д.)

**Когда использовать:**
- ✅ После `/speckit.specify`
- ✅ Comprehensive edge case discovery

**Что генерирует:**
- PROP-xxx properties из AS/EC/FR/NFR
- PGS (Property-Generated Solver) тесты

**Выходные файлы:**
- `specs/NNN-feature/properties.md`

**Quality Gates:**
- PQS (Property Quality Score) ≥ 80

**Модель:** `sonnet`

---

## Дополнительные команды (не рассмотренные)

### `/speckit.integrate`

**Назначение:** Integration и deployment planning

**Флаги:**
- Зависит от типа интеграции (CI/CD, third-party APIs)

---

### `/speckit.launch`

**Назначение:** Launch preparation и go-to-market

**Флаги:**
- `--prepare-press-kit`
- `--outreach`

---

### `/speckit.monitor`

**Назначение:** Setup monitoring и observability

**Флаги:**
- Telemetry destination configuration

---

### `/speckit.ship`

**Назначение:** Provision infrastructure и deploy

**Флаги:**
- Cloud provider selection
- Environment targets

---

## Quick Reference

### По фазе проекта

| Фаза | Команда | Обязательна |
|------|---------|-------------|
| **Setup** | `/speckit.constitution` | ✅ |
| **Discovery** | `/speckit.discover` | ⚪ (для новых продуктов) |
| **Concept** | `/speckit.concept` | ⚪ (50+ requirements) |
| **Validation** | `/speckit.validate-concept` | ⚪ (периодически) |
| **Brownfield** | `/speckit.baseline` | ⚪ (существующий код) |
| **Specification** | `/speckit.specify` | ✅ |
| **Clarification** | `/speckit.clarify` | ⚪ (автоматически при SQS<80) |
| **Design** | `/speckit.design` | ⚪ (UI-heavy фичи) |
| **Planning** | `/speckit.plan` | ✅ |
| **Tasks** | `/speckit.tasks` | ✅ |
| **Staging** | `/speckit.staging` | ✅ (TDD инфраструктура) |
| **Analysis** | `/speckit.analyze` | ✅ (автоматически) |
| **Implementation** | `/speckit.implement` | ✅ |
| **Finalization** | `/speckit.merge` | ✅ |

### По назначению

| Назначение | Команды |
|------------|---------|
| **Setup & Principles** | `constitution` |
| **Strategic Planning** | `concept`, `validate-concept`, `discover` |
| **Requirements** | `specify`, `clarify`, `baseline` |
| **Design** | `design`, `preview` |
| **Planning** | `plan`, `tasks` |
| **TDD Infrastructure** | `staging` |
| **Quality** | `analyze`, `checklist`, `properties` |
| **Implementation** | `implement` |
| **Project Management** | `list`, `switch`, `extend`, `taskstoissues` |
| **Deployment** | `integrate`, `launch`, `monitor`, `ship` |
| **Special** | `migrate`, `merge` |

### Модели по умолчанию

| Команда | Модель | Reasoning Budget |
|---------|--------|------------------|
| `constitution` | `opus` | 16000 |
| `concept` | `opus` | 16000 |
| `validate-concept` | `sonnet` | 12000 |
| `specify` | `opus` | 16000 |
| `clarify` | `sonnet` | 16000 |
| `design` | `opus` | 16000 |
| `plan` | `opus` | 16000 |
| `tasks` | `sonnet` | 8000 |
| `staging` | `haiku` | 4000 |
| `analyze` | `sonnet` | 16000 |
| `implement` | `opus` | 16000 |
| `list` | `haiku` | 4000 |
| `switch` | `haiku` | 4000 |
| `preview` | `opus` | 16000 |

---

## Troubleshooting

### SQS < 80 (Specification Quality Score низкий)

**Решение:**
1. Запустить `/speckit.clarify` для уточнения ambiguities
2. Проверить FR coverage (все ли functional requirements покрыты)
3. Проверить AS coverage (все ли requirements имеют acceptance scenarios)

### Circular Dependencies в tasks.md

**Решение:**
1. `/speckit.analyze` покажет циклы
2. Пересмотреть dependency graph
3. Регенерировать `/speckit.tasks`

### Pre-handoff validation блокирует переход

**Решение:**
1. Посмотреть failing gate в output
2. Исправить указанную проблему
3. Использовать `--skip-validate` для bypass (не рекомендуется)

---

## Версия документа

**Версия:** 1.1.0 (совместим с Spec-Kit v0.0.86)
**Дата:** 2026-01-07
**Автор:** Auto-generated from command templates

### Изменения в 1.1.0

- Добавлена команда `/speckit.staging` для TDD workflow
- Обновлены workflow диаграммы (staging между tasks и analyze)
- Добавлен раздел "TDD Infrastructure" в Quick Reference

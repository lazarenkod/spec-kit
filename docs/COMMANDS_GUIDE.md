# Spec-Kit Commands Guide

<!-- AUTO-GENERATED - DO NOT EDIT MANUALLY -->
<!-- Generated at: 2026-01-09 14:02:55 -->
<!-- Source: templates/commands/*.md -->

Полное руководство по командам Spec Kit для Spec-Driven Development.

---

## Содержание

- [1. /speckit.constitution](#speckitconstitution)
- [2. /speckit.concept](#speckitconcept)
- [3. /speckit.validate-concept](#speckitvalidate-concept)
- [4. /speckit.specify](#speckitspecify)
- [5. /speckit.clarify](#speckitclarify)
- [6. /speckit.design](#speckitdesign)
- [7. /speckit.plan](#speckitplan)
- [8. /speckit.tasks](#speckittasks)
- [9. /speckit.taskstoissues](#speckittaskstoissues)
- [10. /speckit.staging](#speckitstaging)
- [11. /speckit.analyze](#speckitanalyze)
- [12. /speckit.implement](#speckitimplement)
- [13. /speckit.preview](#speckitpreview)
- [14. /speckit.list](#speckitlist)
- [15. /speckit.switch](#speckitswitch)
- [16. /speckit.extend](#speckitextend)
- [17. /speckit.merge](#speckitmerge)
- [18. /speckit.baseline](#speckitbaseline)
- [19. /speckit.checklist](#speckitchecklist)
- [20. /speckit.discover](#speckitdiscover)
- [21. /speckit.integrate](#speckitintegrate)
- [22. /speckit.monitor](#speckitmonitor)
- [23. /speckit.launch](#speckitlaunch)
- [24. /speckit.ship](#speckitship)
- [25. /speckit.concept-variants](#speckitconcept-variants)
- [26. /speckit.migrate](#speckitmigrate)
- [27. /speckit.properties](#speckitproperties)
- [28. /speckit.mobile](#speckitmobile)

---

## Основной Workflow

```mermaid
graph LR
    A[constitution] --> B[concept]
    B --> C[specify]
    C --> D[plan]
    D --> E[tasks]
    E --> F[staging]
    F --> G[implement]
    G --> H[analyze]
```

---

## Детальное описание команд

### 1. `/speckit.constitution` {#speckitconstitution}

**Назначение:** Create or update the project constitution with layered architecture support (base → domain → project layers).

**Модель:** `opus` (thinking_budget: 16000)

**Handoffs:**

- → `/speckit.specify`
- → `/speckit.analyze`

---

### 2. `/speckit.concept` {#speckitconcept}

**Назначение:** Capture complete service concept before detailed specification. Creates hierarchical feature breakdown with full traceability. Use BEFORE /speckit.specify for large projects (50+ requirements).

**Модель:** `opus` (thinking_budget: 16000)

**Domain Immersion (v0.0.120):**

Автоматическое погружение в предметную область с помощью 9 research agents:

- **Wave 1 (Research, 7 agents)**: market-researcher, competitive-analyst, persona-designer, standards-researcher (PCI-DSS, GDPR, HIPAA), academic-researcher (papers, whitepapers), community-intelligence (Stack Overflow, GitHub), trend-analyst
- **Wave 2 (Synthesis, 2 agents)**: glossary-builder (авто-генерация терминологии), constraints-analyzer (технические ограничения)

**Knowledge Base Generation:**
- `memory/knowledge/glossaries/{domain}.md` — автоматический глоссарий
- `memory/knowledge/best-practices/by-domain/{domain}.md` — проверенные паттерны
- `memory/knowledge/standards/compliance/{standard}.md` — чек-листы соответствия
- `memory/knowledge/constraints/platforms/{tech}.md` — технические ограничения

**Evidence Tier Enhancement:**
- **AUTHORITATIVE** (35 points) — RFC, ISO standards, PCI-DSS, GDPR, vendor API docs (<90 days)

**Handoffs:**

- → `/speckit.specify`
- → `/speckit.analyze`

---

### 3. `/speckit.validate-concept` {#speckitvalidate-concept}

**Назначение:** Re-validate an existing concept against current market conditions. Runs research agents to detect changes in market, competitors, and trends. Generates diff report and CQS delta. Use periodically (monthly/quarterly) to keep concept fresh.

**Модель:** `sonnet` (thinking_budget: 12000)

**Persona:** `concept-validator`

**Handoffs:**

- → `/speckit.concept`
- → `/none`

---

### 4. `/speckit.specify` {#speckitspecify}

**Назначение:** Create or update the feature specification from a natural language feature description. Supports both standalone features and concept-derived specifications with full traceability.

**Модель:** `opus` (thinking_budget: 16000)

**Persona:** `product-agent`

**Domain Context Loading (v0.0.120):**

Автоматическая загрузка контекста предметной области через **domain-context-loader agent**:

- **Auto-Link Glossary Terms**: Автоматическая подстановка определений при первом упоминании терминов
- **Auto-Generate Compliance NFRs**: Автоматическая генерация NFR для соответствия стандартам на основе ключевых слов:
  - "store credit card" → `NFR-SEC-PCI-001` (PCI-DSS Req 3.4)
  - "patient data" → `NFR-SEC-HIPAA-001` (HIPAA Privacy Rule)
  - "EU users" → `NFR-SEC-GDPR-001` (GDPR Art. 17)
- **Best Practices References**: Автоматическое добавление ссылок на best practices в Technical Context
- **Known Constraints**: Документирование известных технических ограничений

**Acceptance Criteria Format (v0.0.121):**

Автоматическая генерация исполняемых критериев приемки в формате Gherkin:

- **Gherkin Format**: Сценарии совместимы с BDD-фреймворками (Cucumber, Behave, SpecFlow, Pytest-BDD)
  - **Feature blocks**: Группировка связанных сценариев по user story
  - **Data tables**: Структурированные тела запросов для POST/PUT/PATCH операций
  - **Multiple assertions**: Статус ответа, поля, тайминг, изменения состояния (Then/And)
  - **Specific values**: Конкретные тестовые данные (например, `user "test@example.com"`) вместо заполнителей
  - **Entity-specific patterns**: Готовые паттерны для Auth, CRUD, File Upload, Search, Payment
  - **Scenario IDs**: AS-xxx сохранены для трассировки в tasks.md
  - **Classification tags**: [HAPPY_PATH], [ERROR_PATH], [BOUNDARY], [SECURITY], [ALT_PATH]
  - **Confidence scores**: 0.0-1.0 оценка важности сценария (≥0.90 = критично для MVP)

- **Visual Acceptance Criteria (YAML)**: Для UI-фич автоматически генерируется визуальная спецификация
  - **Elements**: Все UI-компоненты с свойствами (visible, type, placeholder, validation)
  - **States**: loading, error, success, empty, disabled с изменениями элементов
  - **Responsive**: mobile (<640px), tablet (640-1024px), desktop (>1024px) с адаптацией layout/spacing
  - **Accessibility**: ARIA-метки, роли, навигация с клавиатуры, live regions
  - **Interactions**: Триггеры, валидация, действия, ожидаемое время отклика
  - **Performance**: Целевые показатели времени для каждого взаимодействия

**Примеры** доступны в:
- `templates/shared/examples/gherkin-api-example.md` — API с Payment Processing (8 сценариев)
- `templates/shared/examples/gherkin-ui-example.md` — UI с Product Search (10 сценариев + Visual YAML)

**Агенты**:
- **acceptance-criteria-generator**: STEP 5.5 конвертирует таблицы в Gherkin
- **visual-acceptance-generator** (NEW): Генерирует Visual YAML для UI-фич

**Флаги:**

- `--model` — Override model selection
- `--skip-gates` — Bypass inline quality gates
- `--strict-gates` — Treat HIGH severity as blocking
- `--full-gates` — Run full validation passes
- `--sequential` — Disable operation batching (execute operations sequentially)

**Inline Quality Gates:**

| Gate ID | Name | Severity | Pass |
|---------|------|----------|------|
| IG-SPEC-001 | Constitution Alignment | CRITICAL | D |
| IG-SPEC-002 | Ambiguity Detection | HIGH | B |
| IG-SPEC-003 | FR-AS Coverage | HIGH | - |
| IG-SPEC-004 | Implementation Details | MEDIUM | - |

**Quality Gates:**

- Spec Quality Gate

**Handoffs:**

- → `/speckit.plan`
- → `/speckit.clarify`
- → `/speckit.analyze` (for full audit)

**Выходные файлы:**

- `spec.md`
- `Checklists/requirements.md`

---

### 5. `/speckit.clarify` {#speckitclarify}

**Назначение:** Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.

**Модель:** `sonnet` (thinking_budget: 16000)

**Флаги:**

- `--sequential` — Disable operation batching (execute gap searches sequentially)

**Handoffs:**

- → `/speckit.plan`

---

### 6. `/speckit.design` {#speckitdesign}

**Назначение:** Create visual specifications and complete design systems from brand inputs. Orchestrates UX, Product, and Motion Designer agents. Supports design system generation, component library presets, Storybook auto-generation, and Figma token export. Use AFTER /speckit.specify for UI-heavy features OR standalone for design system bootstrapping.

**Модель:** `opus` (thinking_budget: 16000)

**Persona:** `ux-designer-agent`

**Флаги:**

- `--quick` — or `--defaults` flag passed
- `--alternative` — — Generate design for specific alternative (1-5)
- `--all-alternatives` — — Generate designs for ALL alternatives from concept.md
- `--variant` — — Generate design for variant (MINIMAL/BALANCED/AMBITIOUS)
- `--all-variants` — — Generate designs for all 3 scope variants
- `--compare` — — Generate visual comparison matrix alongside designs
- `--viewports` — `"desktop,tablet,mobile"`
- `--no-webp` — `false`
- `--no-optimize` — `false`
- `--interactive` — `true`
- `--parallel` — `true`
- `--max-parallel` — `3`
- `--batch-delay` — `5000`
- `--no-parallel` — -
- `--incremental` — `true`
- `--force` — `false`
- `--reuse-session` — `true`
- `--no-reuse-session` — -
- `--audit-selectors` — `false`
- `--dry-run` — `false`
- `--debug` — `false`
- `--log-level` — `info`
- `--retry-max` — `2`
- `--retry-backoff` — `exponential`
- `--allow-manual-intervention` — `false`
- `--gallery-mode` — `basic`
- `--no-gallery` — `false`
- `--all` — `false`
- `--screens` — -
- `--manual` — `false`
- `--reauth` — `false`
- `--no-figma` — `false`
- `--sequential` — Disable operation batching (execute context reads sequentially)

**Handoffs:**

- → `/speckit.preview`
- → `/speckit.plan`
- → `/speckit.tasks`
- → `/speckit.analyze`
- → `/speckit.analyze`
- → `/speckit.design-promo`
- → `/speckit.preview`
- → `/speckit.design`
- → `/speckit.plan`
- → `/speckit.design`
- → `/speckit.preview`
- → `/speckit.design`
- → `/speckit.design`

**Выходные файлы:**

- `design-system/tokens.json`
- `design-system/README.md`
- `design-tokens/figma-tokens.json`
- `themes.json`
- `metadata.json`
- ... и ещё 1

---

### 7. `/speckit.plan` {#speckitplan}

**Назначение:** Execute the implementation planning workflow using the plan template to generate design artifacts.

**Модель:** `opus` (thinking_budget: 16000)

**Persona:** `architect-agent`

**Требует:** handoffs/specify-to-plan.md

**Domain-Aware Planning (v0.0.120):**

Автоматическая загрузка знаний предметной области перед принятием архитектурных решений:

- **Phase 0.1: Best Practices Loading** — загрузка проверенных паттернов перед генерацией ADR
  - Инъекция best practices в research.md с цитированием источников
  - Пример: "Idempotency Keys for Payments (Stripe Best Practice [AUTHORITATIVE])"
- **Phase 0.2: Constraints Loading** — валидация NFR против технических ограничений
  - Проверка соответствия требованиям лимитам платформ (rate limits, quotas, timeouts)
  - Авто-генерация constraint-driven NFRs
  - Флаги нарушений ДО начала реализации
- **Phase 0.3: Standards Verification** — верификация архитектуры против официальных стандартов
  - Маппинг compliance requirements на implementation
  - Генерация Compliance Traceability Matrix
  - Создание задач верификации соответствия

**Флаги:**

- `--skip-gates` — Bypass inline quality gates
- `--strict-gates` — Treat HIGH severity as blocking
- `--full-gates` — Run full validation passes
- `--sequential` — Disable operation batching (execute research sequentially)

**Inline Quality Gates:**

| Gate ID | Name | Severity | Pass |
|---------|------|----------|------|
| IG-PLAN-001 | Constitution Alignment | CRITICAL | D |
| IG-PLAN-002 | Tech Consistency | HIGH | F |
| IG-PLAN-003 | Spec Alignment | HIGH | V |
| IG-PLAN-004 | Dependencies Verified | MEDIUM | - |

**Quality Gates:**

- Plan Completeness Gate

**Handoffs:**

- → `/speckit.tasks`
- → `/speckit.checklist`
- → `/speckit.specify`
- → `/speckit.analyze` (for full audit)

---

### 8. `/speckit.tasks` {#speckittasks}

**Назначение:** Generate an actionable, dependency-ordered tasks.md with full traceability to spec requirements and acceptance scenarios.

**Модель:** `sonnet` (thinking_budget: 8000)

**Persona:** `decomposer-agent`

**Требует:** handoffs/plan-to-tasks.md

**Флаги:**

- `--skip-gates` — Bypass inline quality gates
- `--strict-gates` — Treat HIGH severity as blocking
- `--full-gates` — Run full validation passes
- `--sequential` — Disable operation batching (execute mappers sequentially)

**Inline Quality Gates:**

| Gate ID | Name | Severity | Pass |
|---------|------|----------|------|
| IG-TASK-001 | Dependency Graph Valid | CRITICAL | G |
| IG-TASK-002 | FR Coverage | HIGH | H |
| IG-TASK-003 | RTM Validity | MEDIUM | J |
| IG-TASK-004 | Test Coverage | HIGH | QG-TEST-001 |

**Quality Gates:**

- Tasks Generated Gate
- Tasks Ready Gate
- Dependency Validity Gate

**Handoffs:**

- → `/speckit.implement`
- → `/speckit.tasks`
- → `/speckit.analyze` (for full audit)

---

### 9. `/speckit.taskstoissues` {#speckittaskstoissues}

**Назначение:** Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts.

**Модель:** `haiku` (thinking_budget: 8000)

---

### 10. `/speckit.staging` {#speckitstaging}

**Назначение:** Provision Docker Compose staging environment before implementation

**Модель:** `haiku` (thinking_budget: 4000)

**Persona:** `devops-agent`

**Требует:** tasks.md

**Флаги:**

- `--services` — Override default services (postgres,redis,playwright). Comma-separated.
- `--skip-playwright` — Skip Playwright container (useful for unit-test-only features)
- `--reset` — Tear down and recreate all services
- `--status` — Show current staging status without changes
- `--down` — Stop all staging services

**Pre-Gates:**

- Tasks Exist Gate
- Docker Available Gate

**Quality Gates:**

- Staging Ready Gate

**Handoffs:**

- → `/speckit.implement`

**Выходные файлы:**

- `.speckit/staging/docker-compose.yaml`
- `.speckit/staging/test-config.env`

---

### 11. `/speckit.analyze` {#speckitanalyze}

**Назначение:** Full cross-artifact analysis and comprehensive QA verification. Primary use cases: comprehensive audits before major milestones (`--profile full`), post-implementation QA verification (`--profile qa`), generating audit reports (`--json`).

> **Note:** Since v0.0.109, inline quality gates are embedded in `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`. Use `/speckit.analyze` for full audits only. Profiles `spec_validate`, `plan_validate`, `tasks_validate` are deprecated for inline use.

**Модель:** `sonnet` (thinking_budget: 16000)

**Persona:** `qa-agent`

**Флаги:**

- `--profile` — Select validation profile: `full` (all passes), `qa` (post-implementation), `quick` (critical only)
- `--quiet` — Suppress non-essential output (only gates + result)
- `--strict` — Lower thresholds (e.g., ambiguity < 3 instead of 5)
- `--json` — Output as JSON for programmatic consumption

**Quality Gates:**

- No Critical Issues Gate
- Dependency Graph Valid Gate
- SQS Quality Gate
- QA Issues Exist Gate
- QA Pass Gate

**Handoffs:**

- → `/speckit.specify`
- → `/speckit.plan`
- → `/speckit.tasks`
- → `/speckit.implement`

---

### 12. `/speckit.implement` {#speckitimplement}

**Назначение:** Execute the implementation plan, generate documentation (RUNNING.md, README.md), and validate with self-review. Enforces inline quality gates for pre-implementation checks and post-implementation validation.

**Модель:** `opus` (thinking_budget: 16000)

**Persona:** `developer-agent`

**Требует:** handoffs/tasks-to-implement.md

**Флаги:**

- `--skip-gates` — Bypass all inline quality gates
- `--skip-pre-gates` — Skip only pre-implementation gates
- `--strict-gates` — Treat HIGH severity as blocking
- `--fast` — Fast mode - run only Tier 1-2 validation
- `--sequential-tasks` — Disable task batching (execute tasks one-by-one)
- `--sequential-waves` — Disable wave overlap optimization

**Task Batching (v0.0.110):**

Tasks are grouped by dependency level and executed as parallel Task tool calls:
- Independent tasks → single message with 4-8 parallel Task calls
- 60-75% time savings vs sequential execution
- Skip with `--sequential-tasks` flag

**Pre-Implementation Inline Gates:**

| Gate ID | Name | Severity | Ref |
|---------|------|----------|-----|
| IG-IMPL-001 | Staging Ready | CRITICAL | QG-STAGING-001 |
| IG-IMPL-002 | SQS Threshold | CRITICAL | QG-001 |
| IG-IMPL-003 | Tasks Exist | CRITICAL | - |
| IG-IMPL-004 | Required Artifacts | CRITICAL | - |
| IG-IMPL-005 | Properties Available | MEDIUM | - |

**Post-Implementation Inline Gates:**

| Gate ID | Name | Severity | Pass |
|---------|------|----------|------|
| IG-IMPL-101 | Build Success | CRITICAL | R |
| IG-IMPL-102 | Tests Pass | CRITICAL | S |
| IG-IMPL-103 | Coverage >= 80% | HIGH | T |
| IG-IMPL-104 | Lint Clean | HIGH | U |

**Quality Gates:**

- Implementation Complete Gate
- Build Artifacts Gate
- QG-004: Test Coverage Gate
- QG-005: Type Coverage Gate
- QG-006: Lint Gate

**Handoffs:**

- → `/speckit.analyze` (for full QA audit)
- → `/speckit.implement`
- → `/speckit.tasks`
- → `/speckit.specify`

---

### 13. `/speckit.preview` {#speckitpreview}

**Назначение:** Generate interactive previews from design specifications. Converts wireframes to visual HTML, generates component previews, captures screenshots, and runs design quality validation.

**Модель:** `opus` (thinking_budget: 16000)

**Persona:** `product-designer-agent`

**Флаги:**

- `--all-alternatives` — Generate preview gallery for ALL alternatives
- `--all-variants` — Generate previews for all scope variants
- `--compare` — Generate side-by-side comparison view
- `--quick` — `--skip quality,gallery,deploy,frames`
- `--ci` — `--no-open --baseline check --gate 80 --skip deploy`
- `--review` — `--deploy --device all --gate 80`
- `--preview-mode` — Override model selection

**Handoffs:**

- → `/speckit.implement`
- → `/speckit.design`
- → `/speckit.design-generate`

---

### 14. `/speckit.list` {#speckitlist}

**Назначение:** List all features in the project with their current status. Shows feature registry from manifest and indicates which feature is currently active.

**Модель:** `haiku` (thinking_budget: 4000)

**Флаги:**

- `--json` — Output in JSON format
- `--tree` — Show feature evolution tree (parent-child relationships)

**Handoffs:**

- → `/speckit.switch`
- → `/speckit.specify`

---

### 15. `/speckit.switch` {#speckitswitch}

**Назначение:** Switch to a different feature to continue working on it. Updates the active feature state and optionally checks out the corresponding git branch.

**Модель:** `haiku` (thinking_budget: 4000)

**Флаги:**

- `--json` — Output in JSON format
- `--repair` — Regenerate manifest from directory structure
- `--no-git` — Skip git branch checkout

**Handoffs:**

- → `/speckit.specify`
- → `/speckit.plan`
- → `/speckit.tasks`
- → `/speckit.implement`

---

### 16. `/speckit.extend` {#speckitextend}

**Назначение:** Extend a merged feature with new capabilities. Creates a new feature branch with Feature Lineage pre-populated, loading context from the parent feature and its system specs.

**Модель:** `sonnet` (thinking_budget: 8000)

**Quality Gates:**

- Extension Valid Gate

**Handoffs:**

- → `/speckit.specify`
- → `/speckit.view`
- → `/speckit.analyze`

**Выходные файлы:**

- `spec.md`

---

### 17. `/speckit.merge` {#speckitmerge}

**Назначение:** Finalize feature and update system specs after PR merge. Converts feature requirements into living system documentation.

**Модель:** `sonnet` (thinking_budget: 16000)

**Handoffs:**

- → `/speckit.analyze`
- → `/speckit.specify`

---

### 18. `/speckit.baseline` {#speckitbaseline}

**Назначение:** Capture current state of system components for brownfield specifications. Generates baseline.md documenting existing behaviors, code structure, and dependencies.

**Модель:** `sonnet` (thinking_budget: 16000)

**Pre-Gates:**

- Feature Directory Gate
- Scope Definition Gate

**Quality Gates:**

- Baseline Completeness Gate
- Code Location Validity Gate
- Baseline Exists Gate

**Handoffs:**

- → `/speckit.specify`
- → `/speckit.plan`

**Выходные файлы:**

- `FEATURE_DIR/baseline.md`

---

### 19. `/speckit.checklist` {#speckitchecklist}

**Назначение:** Generate a custom checklist for the current feature based on user requirements.

**Модель:** `sonnet` (thinking_budget: 8000)

---

### 20. `/speckit.discover` {#speckitdiscover}

**Назначение:** Validate problem-solution fit before building through customer discovery

**Модель:** `opus` (thinking_budget: 16000)

**Persona:** `product-agent`

**Handoffs:**

- → `/speckit.concept`
- → `/speckit.discover`

**Выходные файлы:**

- `docs/discover/hypothesis.md`
- `docs/discover/interview-guide.md`
- `docs/discover/scoring-template.md`
- `docs/discover/analysis.md`
- `docs/discover/decision.md`
- ... и ещё 5

---

### 21. `/speckit.integrate` {#speckitintegrate}

**Назначение:** Quick integration with common third-party services

**Модель:** `sonnet` (thinking_budget: 16000)

**Persona:** `developer-agent`

**Handoffs:**

- → `/speckit.implement`

---

### 22. `/speckit.monitor` {#speckitmonitor}

**Назначение:** Set up production observability with OpenTelemetry, dashboards, and alerting

**Модель:** `sonnet` (thinking_budget: 16000)

**Persona:** `devops-agent`

**Handoffs:**

- → `/speckit.monitor`
- → `/speckit.launch`

**Выходные файлы:**

- `docs/monitor.md`
- `infra/observability/docker-compose.yml`

---

### 23. `/speckit.launch` {#speckitlaunch}

**Назначение:** Automate product launch and go-to-market activities

**Модель:** `sonnet` (thinking_budget: 16000)

**Persona:** `marketing-agent`

**Handoffs:**

- → `/speckit.ship`
- → `/speckit.monitor`
- → `/speckit.implement`

**Выходные файлы:**

- `docs/launch/launch-plan.md`
- `docs/launch/readiness-report.md`
- `docs/launch/social-content.md`
- `docs/launch/email-templates.md`
- `docs/launch/growth-playbook.md`
- ... и ещё 2

---

### 24. `/speckit.ship` {#speckitship}

**Назначение:** Provision infrastructure, deploy application, and verify running system in one command

**Модель:** `sonnet` (thinking_budget: 16000)

**Persona:** `devops-agent`

**Флаги:**

- `--env` — Target environment (local, staging, production). Default: staging
- `--only` — Run only specific stage (infra, deploy, verify). Default: all
- `--destroy` — Tear down infrastructure and deployment
- `--dry-run` — Show plan without executing
- `--cloud` — Override cloud provider (vk, yandex, gcp)
- `--skip-verify` — Skip verification stage
- `--turbo` — Enable maximum parallelism and skip optional checks
- `--safe` — Use sequential execution with full validation
- `--skip-provision` — Skip provision if fingerprint unchanged
- `--force-deploy` — Force deploy even if version unchanged
- `--force-provision` — Force provision even if fingerprint unchanged
- `--full-e2e` — Run full E2E suite instead of contract tests
- `--full-tests` — Run full test suite instead of incremental
- `--auto-rollback` — Automatically rollback on verification failure
- `--no-rollback` — Disable automatic rollback prompts
- `--sequential-phases` — Disable wave overlap optimization
- `--no-browser-pool` — Disable browser pool pre-warming
- `--no-fingerprint` — Disable fingerprint-based skip logic
- `--no-test-cache` — Ignore cached test results

**Pre-Gates:**

- Implementation Exists Gate
- Ship Config Exists Gate

**Quality Gates:**

- Verification Issues Exist Gate
- Deployment Success Gate

**Handoffs:**

- → `/speckit.implement`
- → `/speckit.specify`
- → `/speckit.analyze`

**Выходные файлы:**

- `/infra-outputs.json`
- `FEATURE_DIR/verify-results.md`

---

### 25. `/speckit.concept-variants` {#speckitconcept-variants}

**Назначение:** Generate MINIMAL/BALANCED/AMBITIOUS scope variants for existing concept

**Модель:** `sonnet` (thinking_budget: 8000)

---

### 26. `/speckit.migrate` {#speckitmigrate}

**Назначение:** Plan and execute spec-driven modernization between architectures, versions, and cloud providers

**Модель:** `opus` (thinking_budget: 32000)

**Persona:** `architect-agent`

**Флаги:**

- `--from` — Source architecture to migrate from (monolith, legacy, etc.)
- `--upgrade` — Target version/runtime to upgrade to (node18, postgres16, python312, etc.)
- `--to-cloud` — Target cloud provider (aws, gcp, azure, vk-cloud)
- `--scope` — Limit analysis to specific paths (default: entire codebase)
- `--output` — Output verbosity (minimal, standard, detailed). Default: standard
- `--dry-run` — Show migration plan without generating files

**Pre-Gates:**

- Codebase Exists Gate
- Migration Type Gate

**Quality Gates:**

- Migration Plan Complete Gate
- Risk Mitigation Gate
- Migration Plan Exists Gate

**Handoffs:**

- → `/speckit.plan`
- → `/speckit.tasks`

**Выходные файлы:**

- `baseline.md`

---

### 27. `/speckit.properties` {#speckitproperties}

**Назначение:** Extract properties from spec artifacts and generate property-based tests with EARS transformation. Creates PROP-xxx traced to AS/EC/FR/NFR for comprehensive edge case discovery via PGS (Property-Generated Solver) methodology.

**Модель:** `sonnet` (thinking_budget: 16000)

**Persona:** `qa-agent`

**Требует:** specs/[feature]/spec.md

**Quality Gates:**

- Property Quality Gate
- Property Coverage Gate

**Handoffs:**

- → `/speckit.implement`
- → `/speckit.specify`
- → `/speckit.analyze`

---

### 28. `/speckit.mobile` {#speckitmobile}

**Назначение:** Orchestrate mobile development with specialized agents. Activates platform-specific expertise (KMP/Flutter/React Native), calculates Mobile Quality Score (MQS), and ensures production-ready mobile applications.

**Модель:** `sonnet` (thinking_budget: high)

**Persona:** `mobile-developer-agent`

**Режимы:**

| Mode | Trigger | Purpose |
|------|---------|---------|
| `auto` | Platform detected via platform-detection.md | Automatically select platform and apply expertise |
| `kmp` | `--platform kmp` OR `shared/build.gradle.kts` exists | Apply KMP-specific patterns and validation |
| `flutter` | `--platform flutter` OR `pubspec.yaml` exists | Apply Flutter-specific patterns and validation |
| `react_native` | `--platform react-native` OR `metro.config.js` exists | Apply React Native-specific patterns and validation |

**Skills:**

- `mobile-architecture` — Cross-platform architecture decisions
- `mobile-performance` — Performance optimization
- `mobile-testing` — Testing strategy
- `kmp-expert` — KMP-specific patterns (conditional)
- `flutter-expert` — Flutter-specific patterns (conditional)
- `react-native-expert` — React Native-specific patterns (conditional)

**Флаги:**

- `--platform <kmp|flutter|react-native|native>` — Override auto-detection
- `--skip-mqs` — Skip MQS calculation (not recommended)
- `--mqs-threshold <N>` — Override default 75 threshold

**Mobile Quality Score (MQS):**

| Dimension | Points | Criteria |
|-----------|--------|----------|
| Architecture | 25 | Layer separation, DI, state management |
| Performance | 20 | Cold start <2s, 60 FPS, memory <150MB |
| Platform Parity | 20 | Feature/UX consistency across platforms |
| Testing | 20 | Unit 80%, binding 100%, E2E critical paths |
| Accessibility | 15 | A11y labels, screen reader, touch targets |
| **Total** | **100** | **Threshold: ≥75** |

**Pre-Gates:**

- QG-MOBILE-001: Platform successfully detected
- QG-MOBILE-002: Required dependencies present

**Quality Gates:**

- QG-MQS-001: Architecture score ≥ 20/25
- QG-MQS-002: Performance score ≥ 15/20
- QG-MQS-003: Platform parity ≥ 15/20
- QG-MQS-004: Testing coverage ≥ 15/20 (CRITICAL)
- QG-MQS-005: Accessibility ≥ 10/15
- QG-MQS: Total MQS ≥ 75/100 (CRITICAL)

**Handoffs:**

- → `/speckit.plan` — Create technical plan with mobile architecture decisions
- → `/speckit.tasks` — Generate tasks with platform-specific and binding test tasks
- → `/speckit.implement` — Execute implementation with mobile patterns
- → `/speckit.analyze` — Validate MQS and binding coverage

**Выходные файлы:**

- `memory/mqs-report.md` — Detailed quality breakdown
- `memory/mobile-architecture.md` — Architecture decisions
- `memory/mobile-improvements.md` — Recommended fixes
- `memory/binding-coverage.md` — ViewModel test mapping

---

## Quick Reference

### Команды по категориям

| Категория | Команды |
|-----------|---------|
| Foundation | `/speckit.constitution` |
| Discovery | `/speckit.concept`, `/speckit.validate-concept`, `/speckit.discover` |
| Specification | `/speckit.specify`, `/speckit.clarify`, `/speckit.design` |
| Planning | `/speckit.plan`, `/speckit.tasks`, `/speckit.taskstoissues` |
| Implementation | `/speckit.staging`, `/speckit.implement`, `/speckit.preview` |
| Quality | `/speckit.analyze`, `/speckit.checklist` |
| Navigation | `/speckit.list`, `/speckit.switch`, `/speckit.extend`, `/speckit.merge` |
| Mobile | `/speckit.mobile` |
| Operations | `/speckit.baseline`, `/speckit.integrate`, `/speckit.monitor`, `/speckit.launch`, `/speckit.ship` |

### Флаги команд

| Команда | Флаг | Описание |
|---------|------|----------|
| `/speckit.specify` | `--model` | Override model selection |
| `/speckit.design` | `--quick` | or \`--defaults\` flag passed |
| `/speckit.design` | `--alternative` | — Generate design for specific alternative (1-5) |
| `/speckit.design` | `--all-alternatives` | — Generate designs for ALL alternatives from conce... |
| `/speckit.design` | `--variant` | — Generate design for variant (MINIMAL/BALANCED/AM... |
| `/speckit.design` | `--all-variants` | — Generate designs for all 3 scope variants |
| `/speckit.design` | `--compare` | — Generate visual comparison matrix alongside desi... |
| `/speckit.design` | `--viewports` | \`"desktop,tablet,mobile"\` |
| `/speckit.design` | `--no-webp` | \`false\` |
| `/speckit.design` | `--no-optimize` | \`false\` |
| `/speckit.design` | `--interactive` | \`true\` |
| `/speckit.design` | `--parallel` | \`true\` |
| `/speckit.design` | `--max-parallel` | \`3\` |
| `/speckit.design` | `--batch-delay` | \`5000\` |
| `/speckit.design` | `--no-parallel` | - |
| `/speckit.design` | `--incremental` | \`true\` |
| `/speckit.design` | `--force` | \`false\` |
| `/speckit.design` | `--reuse-session` | \`true\` |
| `/speckit.design` | `--no-reuse-session` | - |
| `/speckit.design` | `--audit-selectors` | \`false\` |
| `/speckit.design` | `--dry-run` | \`false\` |
| `/speckit.design` | `--debug` | \`false\` |
| `/speckit.design` | `--log-level` | \`info\` |
| `/speckit.design` | `--retry-max` | \`2\` |
| `/speckit.design` | `--retry-backoff` | \`exponential\` |
| `/speckit.design` | `--allow-manual-intervention` | \`false\` |
| `/speckit.design` | `--gallery-mode` | \`basic\` |
| `/speckit.design` | `--no-gallery` | \`false\` |
| `/speckit.design` | `--all` | \`false\` |
| `/speckit.design` | `--screens` | - |
| `/speckit.design` | `--manual` | \`false\` |
| `/speckit.design` | `--reauth` | \`false\` |
| `/speckit.design` | `--no-figma` | \`false\` |
| `/speckit.staging` | `--services` | Override default services (postgres,redis,playwrig... |
| `/speckit.staging` | `--skip-playwright` | Skip Playwright container (useful for unit-test-on... |
| `/speckit.staging` | `--reset` | Tear down and recreate all services |
| `/speckit.staging` | `--status` | Show current staging status without changes |
| `/speckit.staging` | `--down` | Stop all staging services |
| `/speckit.analyze` | `--profile` | override remains available for power users |
| `/speckit.analyze` | `--quiet` | Suppress non-essential output (only gates + result... |
| `/speckit.analyze` | `--strict` | Lower thresholds (e.g., ambiguity < 3 instead of 5... |
| `/speckit.analyze` | `--json` | Output as JSON for programmatic consumption |
| `/speckit.implement` | `--skip-pre-gates` | Skip pre-implementation gates |
| `/speckit.implement` | `--fast` | Fast mode - run only Tier 1-2 validation |
| `/speckit.preview` | `--all-alternatives` | Generate preview gallery for ALL alternatives |
| `/speckit.preview` | `--all-variants` | Generate previews for all scope variants |
| `/speckit.preview` | `--compare` | Generate side-by-side comparison view |
| `/speckit.preview` | `--quick` | \`--skip quality,gallery,deploy,frames\` |
| `/speckit.preview` | `--ci` | \`--no-open --baseline check --gate 80 --skip depl... |
| `/speckit.preview` | `--review` | \`--deploy --device all --gate 80\` |
| `/speckit.preview` | `--preview-mode` | Override model selection |
| `/speckit.list` | `--json` | Output in JSON format |
| `/speckit.list` | `--tree` | Show feature evolution tree (parent-child relation... |
| `/speckit.switch` | `--json` | Output in JSON format |
| `/speckit.switch` | `--repair` | Regenerate manifest from directory structure |
| `/speckit.switch` | `--no-git` | Skip git branch checkout |
| `/speckit.ship` | `--env` | Target environment (local, staging, production). D... |
| `/speckit.ship` | `--only` | Run only specific stage (infra, deploy, verify). D... |
| `/speckit.ship` | `--destroy` | Tear down infrastructure and deployment |
| `/speckit.ship` | `--dry-run` | Show plan without executing |
| `/speckit.ship` | `--cloud` | Override cloud provider (vk, yandex, gcp) |
| `/speckit.ship` | `--skip-verify` | Skip verification stage |
| `/speckit.ship` | `--turbo` | Enable maximum parallelism and skip optional check... |
| `/speckit.ship` | `--safe` | Use sequential execution with full validation |
| `/speckit.ship` | `--skip-provision` | Skip provision if fingerprint unchanged |
| `/speckit.ship` | `--force-deploy` | Force deploy even if version unchanged |
| `/speckit.ship` | `--force-provision` | Force provision even if fingerprint unchanged |
| `/speckit.ship` | `--full-e2e` | Run full E2E suite instead of contract tests |
| `/speckit.ship` | `--full-tests` | Run full test suite instead of incremental |
| `/speckit.ship` | `--auto-rollback` | Automatically rollback on verification failure |
| `/speckit.ship` | `--no-rollback` | Disable automatic rollback prompts |
| `/speckit.ship` | `--sequential-phases` | Disable wave overlap optimization |
| `/speckit.ship` | `--no-browser-pool` | Disable browser pool pre-warming |
| `/speckit.ship` | `--no-fingerprint` | Disable fingerprint-based skip logic |
| `/speckit.ship` | `--no-test-cache` | Ignore cached test results |
| `/speckit.migrate` | `--from` | Source architecture to migrate from (monolith, leg... |
| `/speckit.migrate` | `--upgrade` | Target version/runtime to upgrade to (node18, post... |
| `/speckit.migrate` | `--to-cloud` | Target cloud provider (aws, gcp, azure, vk-cloud) |
| `/speckit.migrate` | `--scope` | Limit analysis to specific paths (default: entire ... |
| `/speckit.migrate` | `--output` | Output verbosity (minimal, standard, detailed). De... |
| `/speckit.migrate` | `--dry-run` | Show migration plan without generating files |
| `/speckit.mobile` | `--platform` | Override auto-detection (kmp, flutter, react-native, native) |
| `/speckit.mobile` | `--skip-mqs` | Skip MQS calculation (not recommended) |
| `/speckit.mobile` | `--mqs-threshold` | Override default 75 threshold |

---

## Версия документа

**Версия:** 0.0.120
**Дата генерации:** 2026-01-10
**Автор:** Auto-generated from command templates

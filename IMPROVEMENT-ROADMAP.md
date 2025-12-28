# Spec Kit: Roadmap к Автономной Генерации Приложений

> Комплексный анализ текущего состояния, конкурентного ландшафта и стратегии развития для достижения скорости и качества уровня Lovable

**Дата**: 2025-12-27
**Версия**: 1.0

---

## Executive Summary

Spec Kit — мощный фреймворк для Spec-Driven Development с сильными основами: структурированные спецификации, трассируемость требований и интеграция с AI-агентами. Однако для достижения уровня автономности конкурентов (Lovable, Bolt.new, Replit Agent) требуются стратегические улучшения.

### Ключевые метрики текущего состояния vs целевые

| Метрика | Сейчас | Цель (6 мес) | Lovable/Bolt |
|---------|--------|--------------|--------------|
| Zero-Touch Deployment | ~30% | 70% | 85%+ |
| Время до MVP | 2+ часа | 30 мин | 5-15 мин |
| Self-Healing Rate | ~10% | 70% | 80%+ |
| Cost per Feature | ~$44 | $25 | $5-15 |

---

## Часть 1: Конкурентный Ландшафт

### 1.1 Lovable.dev

**Официальный сайт**: [lovable.dev](https://lovable.dev/)

**Ключевые преимущества**:
- **20x быстрее традиционного кодинга**: функциональные прототипы за минуты
- **Full-stack генерация**: React frontend + Supabase backend + auth + database автоматически
- **Figma интеграция**: импорт дизайнов через Builder.io
- **Chat Mode (Lovable 2.0)**: структурированный development agent
- **Agent Mode**: автономный debugging и исправление ошибок

**Слабости**:
- Требует базовых навыков кодинга для сложных кастомизаций
- Ограниченные бесплатные лимиты (5 сообщений/день)
- [Уязвимости безопасности](https://medium.com/firebird-technologies/honest-review-of-lovable-from-an-ai-engineer-38e49f7069fb): 170 из 1,645 приложений имели проблемы с доступом к данным

**Ценовая модель**: Message-based (не токены), $20/месяц Pro план

**Источники**: [UI Bakery Review](https://uibakery.io/blog/what-is-lovable-ai), [Trickle Review](https://trickle.so/blog/lovable-ai-review), [Lovable Docs](https://docs.lovable.dev/)

---

### 1.2 Bolt.new (StackBlitz)

**Официальный сайт**: [bolt.new](https://bolt.new/)

**Ключевые преимущества**:
- **Browser-native development**: WebContainers, нет локальной установки
- **Full-stack в одном процессе**: React + Node.js + PostgreSQL + Prisma
- **Интеграции**: Stripe, Supabase, Firebase из коробки
- **Мгновенный deploy**: Vercel, Netlify в один клик
- **1M+ AI-сгенерированных сайтов** через Netlify (март 2025)
- **Claude Agent**: выбор Claude 4.5 моделей для генерации

**Август 2025 апдейт**: Подписка теперь включает hosting, domains, databases, serverless, auth, SEO, payments, analytics — переход к "build + run + scale" платформе

**Слабости**:
- Проблемы со сложными приложениями: "significant manual intervention for debugging"
- npm support и multi-model agent routing в experimental фазе

**Источники**: [Bolt GitHub](https://github.com/stackblitz/bolt.new), [Refine Review](https://refine.dev/blog/bolt-new-ai/), [DronaHQ Review](https://www.dronahq.com/bolt-ai-review/)

---

### 1.3 Vercel v0

**Официальный сайт**: [v0.app](https://v0.app/)

**Ключевые преимущества**:
- **Text-to-UI специализация**: React + Tailwind + shadcn/ui
- **AutoFix post-processor**: автоматическое исправление ошибок при генерации
- **Platform API**: headless app builder для интеграции в другие продукты
- **512K контекст** (v0-1.5-lg): огромный контекст для сложных проектов
- **Итеративное уточнение**: "add dark mode" → regenerate

**Слабости**:
- **Только React**: другие фреймворки не поддерживаются
- Проблемы с GitHub sync и zip exports
- Credit-based pricing вызывает frustration

**Источники**: [Skywork Review](https://skywork.ai/blog/vercel-v0-dev-review-2025-ai-ui-react-tailwind/), [Trickle Review](https://trickle.so/blog/vercel-v0-review), [Vercel Blog](https://vercel.com/blog/build-your-own-ai-app-builder-with-the-v0-platform-api)

---

### 1.4 Replit Agent 3

**Официальный сайт**: [replit.com/products/agent](https://replit.com/products/agent)

**Ключевые преимущества**:
- **Extended autonomous builds**: минимальный надзор
- **App Testing**: self-validation через browser testing
- **Agents & Automations**: создание своих autonomous систем
- **Built-in everything**: Auth, Database, Hosting, Monitoring
- **Rokt кейс**: 135 internal apps за 24 часа

**Proprietary testing**: 3x быстрее и 10x дешевле чем Computer Use Models

**Слабости**:
- Медленнее конкурентов (Agent 3 slow)
- Дорого для масштабных проектов

**Источники**: [Replit Agent Docs](https://docs.replit.com/replitai/agent), [HostAdvice Review](https://hostadvice.com/ai-app-builders/replit-review/)

---

### 1.5 Cursor AI IDE

**Официальный сайт**: [cursor.com](https://cursor.com/)

**Ключевые преимущества**:
- **8 параллельных агентов** (Cursor 2.0)
- **Composer model**: mixture-of-experts, обученный через RL в реальных codebase
- **Browser tool**: агенты тестируют web apps, делают скриншоты
- **Voice mode**: голосовое управление агентами
- **Best solution judging**: автоматический выбор лучшего результата из параллельных запусков

**Cursor vs Copilot**: "Cursor's Agent mode aims to *execute tasks*, not just generate code"

**Источники**: [Cursor Features](https://cursor.com/features), [Skywork Review](https://skywork.ai/blog/cursor-ai-review-2025-agent-refactors-privacy/), [Nearform Comparison](https://nearform.com/digital-community/battle-of-the-ai-agents/)

---

### 1.6 Сравнительная Матрица

| Возможность | Spec Kit | Lovable | Bolt.new | v0 | Replit | Cursor |
|-------------|----------|---------|----------|-----|--------|--------|
| **Full-stack генерация** | ✅ (через templates) | ✅ Native | ✅ Native | ❌ UI only | ✅ Native | ✅ Via agents |
| **Figma import** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Self-healing/debugging** | ⚠️ Manual | ✅ Agent Mode | ⚠️ Limited | ✅ AutoFix | ✅ Browser testing | ✅ Auto-judge |
| **Spec-first подход** | ✅ Core feature | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Трассируемость** | ✅ FR→AS→Tasks | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Wave-based ordering** | ✅ UX Foundations | ❌ | ❌ | ❌ | ❌ | ❌ |
| **One-click deploy** | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Время до MVP** | 2+ часа | 5-15 мин | 10-30 мин | 15-60 мин | 30-60 мин | 1-2 часа |
| **Стоимость** | API costs | $20/мес | $20/мес | $20/мес | $25/мес | $20/мес |

---

## Часть 2: Vibe Coding и Тренды 2025

### 2.1 Что такое Vibe Coding

> **Vibe coding** — практика разработки ПО, где AI генерирует код из natural language prompts. Термин введён Andrej Karpathy в начале 2025 и стал "Word of the Year" Collins Dictionary.

**Ключевые характеристики**:
- Разработчик направляет AI через диалог, а не пишет код
- AI планирует, генерирует, отлаживает автономно
- Фокус на intent, не на implementation

**Статистика**:
- 84% разработчиков используют или планируют AI tools
- 25% Y Combinator W25 batch имели 95% AI-generated codebases
- 40% рост продуктивности в surveyed teams

**Источники**: [The New Stack](https://thenewstack.io/ai-engineering-trends-in-2025-agents-mcp-and-vibe-coding/), [Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding), [Google Cloud](https://cloud.google.com/discover/what-is-vibe-coding)

---

### 2.2 Эволюция к Context Engineering

> "2025 has seen a significant shift from vibes-based approach to **context engineering** — systematic approach for managing how AI systems process context."

**Что это значит для Spec Kit**:
- Spec-first подход уже реализует context engineering через structure specs
- Трассируемость (FR→AS→Tasks) = structured context
- Wave-based ordering = prioritized context injection

**Spec Kit преимущество**: Уже практикует context engineering, пока конкуренты переходят от "vibes"

---

### 2.3 Проблемы Vibe Coding

**"Vibe Coding Hangover"** (Fast Company, сентябрь 2025):
- Senior engineers сталкиваются с "development hell" при работе с AI-кодом
- Код компилируется, но имеет subtle logic errors
- 60% quality gains для seniors, но только 22% уверенность в shipping

**Безопасность**:
- Databricks AI Red Team: critical vulnerabilities (arbitrary code execution, memory corruption)
- Lovable: 170/1,645 apps имели data access issues

**Spec Kit возможность**: Валидация качества через /speckit.analyze решает "hangover" проблему

---

## Часть 3: Gap Analysis — Текущие Узкие Места

### 3.1 Human-in-the-Loop Bottlenecks

| Фаза | Bottleneck | Impact | Root Cause |
|------|------------|--------|------------|
| **Specification** | /speckit.clarify требует manual Q&A cycles | Дни вместо часов | Нет автоматической ambiguity detection |
| **Plan Validation** | Manual review перед tasks | Over-engineering risks | Constitution не enforced programmatically |
| **Implementation** | Self-review 3-iteration limit | User override bypasses quality | Нет auto-remediation |
| **QA** | Reactive validation | Issues discovered late | UXQ validation post-spec, не proactive |

### 3.2 Quality Consistency Issues

| Issue | Evidence | Impact |
|-------|----------|--------|
| **UX Variance** | UXQ validated post-spec | Friction points discovered late |
| **Missing Tests** | [NO-TEST:] allowed with minimal justification | AS without automated tests |
| **Annotation Gaps** | @speckit added post-implementation | Traceability discovered in QA |
| **API Hallucinations** | Verification is pre-flight only | AI can hallucinate between verify and implement |

### 3.3 AI Capability Limitations

| Limitation | Current State | Competitor State |
|------------|---------------|------------------|
| **Model Routing** | Single agent for all phases | Cursor: 8 parallel agents, auto-judging |
| **Vision Validation** | None | Lovable/Replit: browser testing, screenshots |
| **Self-Healing** | 3 manual iterations | Bolt: AutoFix, Replit: 3x faster testing |
| **Design Import** | None | Lovable: Figma via Builder.io |

---

## Часть 4: Стратегия Улучшений

### 4.1 Proactive Validation Pipeline

**Текущий поток**:
```
specify → clarify → plan → tasks → implement → analyze (QA)
```

**Улучшенный поток**:
```
specify → [auto-analyze] → clarify (только если issues) → plan → [auto-analyze] → tasks → implement → [continuous-analyze]
```

**Реализация**:
- Gate conditions перед каждой фазой
- Spec MUST pass ambiguity detection (< 5 findings)
- Constitution alignment = 100%
- Auto-invoke clarify с specific questions при failures

### 4.2 Self-Healing Implementation Loop

**Текущий**:
```
Self-review → Manual fix → Re-review (3x max) → User override
```

**Улучшенный**:
```
Self-review → Auto-fix common issues → Re-review → Human escalation (rare)
```

**Auto-fixable Issues**:
- Missing @speckit annotations → Insert from task markers
- TODO/FIXME comments → Convert to GitHub issues
- Lint warnings → Auto-formatter
- Missing .env.example → Generate from code scanning

### 4.3 Intelligent Model Routing

| Phase | Model | Reasoning |
|-------|-------|-----------|
| /speckit.constitution | **Opus 4.5** | High reasoning, rare |
| /speckit.concept | **Opus 4.5** | Complex planning |
| /speckit.specify | **Opus 4.5** | Creative synthesis |
| /speckit.clarify | **Sonnet 4.5** | Iterative, balanced |
| /speckit.plan | **Opus 4.5** | Architecture reasoning |
| /speckit.tasks | **Sonnet 4.5** | Structured output |
| /speckit.implement (setup) | **Haiku 4** | Templates, boilerplate |
| /speckit.implement (core) | **Opus 4.5** | Business logic |
| /speckit.implement (tests) | **Sonnet 4.5** | Structured, repetitive |
| Self-review auto-fix | **Haiku 4** | Syntax-only |

**Экономия**: 40-60% снижение costs без degradation качества

---

## Часть 5: Техническая Архитектура

### 5.1 RAG Integration

**Зачем**: Prevent API hallucinations, ensure code follows best practices

**Реализация**:
```python
class ComponentVectorStore:
    """Vector database for retrievable code patterns"""

    def __init__(self, persist_directory: str = ".speckit/cache/vectors"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection("component_patterns")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def retrieve_patterns(self, query: str, tech_filter: List[str], top_k: int = 5):
        """Retrieve relevant patterns via semantic search"""
        # ...returns ComponentPattern objects with proven code examples
```

**Рекомендуемая DB**: ChromaDB (embedded, local-first) → Qdrant Cloud (production)

### 5.2 Multi-Agent Orchestration

**Текущее**: Sequential single agent
**Целевое**: Parallel agents с dependency resolution

```python
class AgentOrchestrator:
    """Coordinate multiple AI agents working in parallel"""

    async def execute_workflow(self, tasks: List[AgentTask]):
        while self.task_queue or self.in_progress:
            ready_tasks = self._get_ready_tasks()  # Dependencies met
            role_groups = self._group_by_role(ready_tasks)  # Avoid conflicts

            await asyncio.gather(*[
                self._execute_task(task, self.agents[task.role])
                for task in self._select_parallel_tasks(role_groups)
            ])
```

**Agent Roles**:
- FRONTEND: UI components, styles
- BACKEND: APIs, business logic
- TESTING: Test generation, execution
- INFRASTRUCTURE: Build, deploy, config
- REVIEW: Code quality, security

### 5.3 Self-Healing Engine

```python
class SelfHealingEngine:
    """Automatically fix common build and test errors"""

    async def build_until_works(self, project_path: str) -> bool:
        for iteration in range(1, self.max_iterations + 1):
            build_result = await self._run_build(project_path)

            if build_result.success:
                return True

            errors = self._parse_build_errors(build_result.stderr)
            fixes_applied = await self._apply_auto_fixes(errors)

            if not fixes_applied:
                return False  # No auto-fixes available

        return False  # Max iterations reached
```

**Error Pattern Library**:
- TypeScript: Missing import → Auto-add import
- ESLint: Unused variable → Remove or prefix with _
- React: Missing key prop → Add key={index}
- Python: Missing type hint → Infer from context

### 5.4 Design Tool Integration

**Figma Import**:
```python
class FigmaToCodeGenerator:
    async def import_design(self, figma_file_key: str) -> Dict:
        figma_data = await self.client.get_file(figma_file_key)

        design_tokens = self._extract_design_tokens(figma_data)  # Colors, typography
        components = self._extract_components(figma_data)  # Buttons, forms

        return {
            "design_tokens": design_tokens,
            "components": components,
            "spec": self._generate_design_spec(design_tokens, components)
        }
```

**OpenAPI Generation**:
- Parse FR-xxx requirements
- Generate endpoints автоматически
- Write to contracts/api.yaml

---

## Часть 6: UX Quality Automation

### 6.1 Vision-Powered UX Validation

**Workflow**:
1. /speckit.implement completes Wave 1-2
2. Capture screenshots (Playwright MCP)
3. Feed to Claude 4.5 Opus (vision)
4. System prompt: UXQ principles + Nielsen Heuristics
5. Generate UX Audit Report
6. If CRITICAL → block deployment

**Example Vision Prompt**:
```
Evaluate authentication page against UXQ principles:
- UXQ-001: Match user mental model (no jargon)
- UXQ-003: All friction must be justified
- UXQ-006: FTUE clear guidance

Output violations as JSON with severity and suggestions.
```

### 6.2 Design System Enforcement

**Injection in Constitution**:
```yaml
design_system:
  framework: "shadcn/ui"
  theme:
    primary: "#3B82F6"
    secondary: "#10B981"
    typography: "Inter"
  component_library_url: "https://ui.shadcn.com/docs"
```

**Enforcement**:
- Always use library components before custom
- Validate colors against theme tokens
- Check typography consistency via vision

### 6.3 Component Library Recommendations

| Tech Stack | Library | Reasoning |
|------------|---------|-----------|
| React + TS | **shadcn/ui** | Accessible, no runtime overhead |
| React | **MUI** | Comprehensive, enterprise-ready |
| Vue.js | **Vuetify** | Material Design, TS support |
| Angular | **Angular Material** | Official, tight integration |
| Svelte | **Skeleton UI** | Svelte-native, Tailwind-based |

---

## Часть 7: Metrics & Success Criteria

### 7.1 Generation Quality Score (SQS)

```
SQS = (
  FR_Coverage × 0.3 +           # % FRs with tasks
  AS_Coverage × 0.3 +           # % AS with tests
  Traceability_Score × 0.2 +    # % code with @speckit
  Constitution_Compliance × 0.2 # % principles followed
) × 100
```

**Targets**:
- MVP (Wave 1-2): SQS ≥ 80%
- Full Feature: SQS ≥ 90%
- Production-Ready: SQS = 100%

### 7.2 Velocity Metrics

| Metric | Current | Target | Lovable Benchmark |
|--------|---------|--------|-------------------|
| Time to First Working Code | ~30 min | < 10 min | ~5 min |
| Time to MVP | 2+ hours | < 30 min | ~15 min |
| Human Intervention Rate | ~70% | < 30% | ~15% |
| Auto-Fix Success Rate | ~10% | > 70% | ~80% |

### 7.3 Cost Metrics

**Current Estimated (50 FRs, 200 tasks)**:

| Phase | Model | Tokens | Cost |
|-------|-------|--------|------|
| Constitution | Opus | 25K | $0.68 |
| Concept | Opus | 70K | $2.25 |
| Specify | Opus | 130K | $3.75 |
| Clarify | Sonnet | 95K | $0.47 |
| Plan | Opus | 160K | $4.80 |
| Tasks | Sonnet | 200K | $1.20 |
| Implement | Opus/Sonnet | 1.5M | $22 |
| QA | Sonnet | 350K | $1.65 |
| **Total** | | ~2.5M | **~$37** |

**Target with Optimizations**: $20-25 (32-46% reduction)

---

## Часть 8: Implementation Roadmap

### Phase 1: Foundation (Месяцы 1-2)

**Цель**: Reduce human-in-the-loop by 40%

**Deliverables**:
1. Proactive validation gates
2. Auto-clarification agent
3. Self-healing for annotations
4. Model routing (Opus/Sonnet/Haiku)
5. Cost tracking

**Metrics**:
- ZTD: 30% → 50%
- QGPR: 40% → 60%
- Cost: $37 → $30

---

### Phase 2: Autonomy (Месяцы 3-4)

**Цель**: Achieve Level 3 autonomy (70% ZTD)

**Deliverables**:
1. Vision-powered UX validation
2. API docs context injection
3. Auto-debug loop (3 iterations)
4. UXQ domain as default
5. Design system enforcement

**Metrics**:
- ZTD: 50% → 70%
- SHSR: 20% → 60%
- Hallucination Rate: 15% → 5%

---

### Phase 3: Scale (Месяцы 5-6)

**Цель**: Production-ready autonomous generation

**Deliverables**:
1. Multi-repo workspace orchestration
2. One-command generation (`specify generate`)
3. Auto-deployment (Vercel, AWS, Docker)
4. Monitoring integration (Sentry, DataDog)
5. Quality metrics dashboard

**Metrics**:
- ZTD: 70% → 85%
- Time to MVP: 30 min → 15 min
- QGPR: 60% → 80%

---

## Часть 9: Unique Value Proposition

### 9.1 Что Spec Kit Делает Лучше Конкурентов

| Capability | Spec Kit Advantage | Competitor Gap |
|------------|-------------------|----------------|
| **Spec-first development** | Структурированные требования до кода | Lovable/Bolt: Code-first, specs implicit |
| **Трассируемость** | FR → AS → Tasks → Code → Tests | Конкуренты: Нет traceability |
| **Wave-based UX** | Foundations первыми (AUTH, NAV, ERROR) | Конкуренты: Random order |
| **Quality gates** | 26+ validation passes | Конкуренты: Basic linting |
| **Context engineering** | Structured specs = optimized context | Конкуренты: Raw prompts |
| **Enterprise-ready** | Constitution, ADRs, audit trail | Конкуренты: Startup-focused |

### 9.2 Как Достичь Скорости Lovable

**Gap Analysis**:
- Lovable: 5-15 min to MVP
- Spec Kit: 2+ hours to MVP

**Причина разрыва**:
1. Lovable генерирует код напрямую (no spec phase)
2. Lovable имеет pre-built Supabase integration
3. Lovable использует browser-based preview (instant feedback)

**Стратегия закрытия разрыва**:

1. **"Quick Mode"** для простых приложений:
   ```bash
   specify quick "Task management app with auth"
   # → Skips formal spec, generates MVP directly
   # → Uses sensible defaults from UX Foundations
   ```

2. **Pre-configured integrations**:
   - Supabase, Firebase, Clerk templates
   - One-command setup: `specify init --backend supabase`

3. **Browser preview** (через Playwright MCP):
   - Live preview during implementation
   - Hot reload для instant feedback

4. **Parallel Wave execution**:
   - Wave 1 + Wave 2 параллельно (где нет dependencies)
   - Reduces time from sequential to parallel

**Projected Time with Improvements**:
- Current: 2+ hours
- After Phase 1: 45 min
- After Phase 2: 20 min
- After Phase 3: ~10 min (approaching Lovable)

---

## Часть 10: Immediate Action Items

### High Priority (This Week)

1. **Implement model routing** в AGENT_CONFIG
   - Add model_preference to command YAML
   - Route Haiku for boilerplate, Opus for reasoning

2. **Add pre-gates to /speckit.plan**
   - Ambiguity detection (< 5 findings to pass)
   - Constitution alignment check

3. **Create annotation auto-fix**
   - Parse task markers
   - Insert @speckit comments automatically

### Medium Priority (This Month)

4. **Integrate ChromaDB** для component patterns
   - Index shadcn/ui, MUI component examples
   - Semantic search during implementation

5. **Vision UX validation** prototype
   - Playwright screenshot capture
   - Claude vision evaluation

6. **Design system detection**
   - Auto-detect from package.json
   - Inject tokens into implementation context

### Low Priority (Next Quarter)

7. **Figma import** integration
8. **One-command generation** (`specify generate`)
9. **Auto-deployment** pipeline
10. **Quality metrics dashboard**

---

## Заключение

Spec Kit уже реализует **context engineering**, который индустрия только начинает осваивать после "vibe coding hangover". Это стратегическое преимущество.

Для достижения скорости Lovable/Bolt нужно:
1. **Proactive validation** вместо reactive
2. **Self-healing** вместо manual fixes
3. **Intelligent routing** вместо one-model-fits-all
4. **Parallel agents** вместо sequential
5. **Pre-built integrations** вместо from-scratch

При реализации roadmap за 6 месяцев Spec Kit может достичь:
- **70% Zero-Touch Deployment**
- **10-15 мин Time to MVP** (vs 2+ часов сейчас)
- **$20-25 Cost per Feature** (vs $37 сейчас)

**Главное преимущество**: Spec Kit создаёт **production-quality, auditable, maintainable** код с полной трассируемостью — то, чего не дают "vibe coding" tools.

---

## Источники

### Competitors
- [Lovable.dev](https://lovable.dev/) | [Docs](https://docs.lovable.dev/)
- [Bolt.new](https://bolt.new/) | [GitHub](https://github.com/stackblitz/bolt.new)
- [Vercel v0](https://v0.app/) | [Blog](https://vercel.com/blog)
- [Replit Agent](https://replit.com/products/agent) | [Docs](https://docs.replit.com/replitai/agent)
- [Cursor](https://cursor.com/) | [Features](https://cursor.com/features)

### Research & Trends
- [The New Stack: AI Trends 2025](https://thenewstack.io/ai-engineering-trends-in-2025-agents-mcp-and-vibe-coding/)
- [Martin Fowler: Pushing AI Autonomy](https://martinfowler.com/articles/pushing-ai-autonomy.html)
- [Qodo: State of AI Code Quality](https://www.qodo.ai/reports/state-of-ai-code-quality/)
- [Google Cloud: What is Vibe Coding](https://cloud.google.com/discover/what-is-vibe-coding)
- [Microsoft: Vibe Coding and AI](https://news.microsoft.com/source/features/ai/vibe-coding-and-other-ways-ai-is-changing-who-can-build-apps-and-how/)

### Reviews
- [UI Bakery: Lovable Review](https://uibakery.io/blog/what-is-lovable-ai)
- [Skywork: Cursor Review](https://skywork.ai/blog/cursor-ai-review-2025-agent-refactors-privacy/)
- [Refine: Bolt.new Review](https://refine.dev/blog/bolt-new-ai/)
- [Medium: Lovable Honest Review](https://medium.com/firebird-technologies/honest-review-of-lovable-from-an-ai-engineer-38e49f7069fb)

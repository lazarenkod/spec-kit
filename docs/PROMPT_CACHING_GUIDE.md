# Prompt Caching Guide — Claude API Token Optimization

**Версия**: 1.0.0
**Дата**: 2026-01-13
**Применимо к**: Claude API (Anthropic API), Claude Code CLI

---

## 🎯 Что такое Prompt Caching?

**Prompt Caching** — встроенная функция Claude API, которая автоматически кеширует повторяющиеся части промпта для экономии токенов и денег.

### Ключевые преимущества

| Метрика | Без кеширования | С кешированием | Экономия |
|---------|----------------|----------------|----------|
| **Стоимость** | 100% | **10%** | 90% на кеш-хитах |
| **Скорость** | Baseline | До 3x быстрее | Мгновенная загрузка кеша |
| **Токены** | 50,000 input | 5,000 input | 45,000 токенов сэкономлено |

**Пример расчёта** для Sonnet 4.5:
```
Без кеша: 50,000 tokens × $3/MTok = $0.15 per request
С кешем:  5,000 tokens × $3/MTok + 45,000 tokens × $0.30/MTok = $0.015 + $0.0135 = $0.0285 per request
Экономия: $0.15 - $0.0285 = $0.1215 (81% дешевле!)
```

---

## 🔧 Как работает Prompt Caching

### Архитектура

```
┌─────────────────────────────────────────────┐
│           Ваш API запрос                    │
├─────────────────────────────────────────────┤
│  System Prompt (10K tokens) ← КЕШИРУЕТСЯ   │
│  Context (30K tokens)       ← КЕШИРУЕТСЯ   │
│  User Query (100 tokens)    ← НЕ КЕШИРУЕТСЯ│
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│         Claude API Cache Layer              │
│  • Проверка cache_control breakpoints      │
│  • Загрузка кешированных блоков (0.1ms)    │
│  • Обработка только некешированной части   │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│              Response                        │
│  • 45,000 tokens: cache read ($0.0135)      │
│  • 5,000 tokens: regular input ($0.015)     │
│  • Total: $0.0285 вместо $0.15              │
└─────────────────────────────────────────────┘
```

### Механизм кеширования

1. **Маркировка кеш-блоков** — используется `cache_control: {"type": "ephemeral"}`
2. **Автоматическое кеширование** — Claude API создаёт кеш-ключ на основе содержимого
3. **5-минутный TTL** — кеш живёт 5 минут с момента последнего использования
4. **Минимум 1024 токена** — блоки меньше 1024 токенов не кешируются (не выгодно)
5. **Максимум 4 breakpoint** — можно пометить до 4 кеш-блоков в одном запросе

---

## 📝 Синтаксис и примеры

### Базовый пример (Python SDK)

```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an AI assistant specialized in Python development...",
        },
        {
            "type": "text",
            "text": "Here is the entire codebase:\n\n" + codebase_content,
            "cache_control": {"type": "ephemeral"}  # ← КЕШИРУЕТСЯ!
        }
    ],
    messages=[
        {"role": "user", "content": "What does the main() function do?"}
    ]
)

print(f"Input tokens: {response.usage.input_tokens}")
print(f"Cache creation tokens: {response.usage.cache_creation_input_tokens}")  # Первый запрос
print(f"Cache read tokens: {response.usage.cache_read_input_tokens}")          # Последующие запросы
```

**Вывод (первый запрос)**:
```
Input tokens: 5000
Cache creation tokens: 45000  # Кеш создан
Cache read tokens: 0
```

**Вывод (второй запрос через 30 секунд)**:
```
Input tokens: 5000
Cache creation tokens: 0
Cache read tokens: 45000      # Кеш прочитан (90% дешевле!)
```

---

### Множественные кеш-блоки (Multi-breakpoint)

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are a Python expert...",
        },
        {
            "type": "text",
            "text": f"Project README:\n\n{readme_content}",
            "cache_control": {"type": "ephemeral"}  # Breakpoint 1
        },
        {
            "type": "text",
            "text": f"Full codebase:\n\n{codebase_content}",
            "cache_control": {"type": "ephemeral"}  # Breakpoint 2
        },
        {
            "type": "text",
            "text": f"Test suite:\n\n{test_content}",
            "cache_control": {"type": "ephemeral"}  # Breakpoint 3
        }
    ],
    messages=[
        {"role": "user", "content": "Review the test coverage"}
    ]
)
```

**Преимущества**: Если изменился только `test_content`, кеш для `readme_content` и `codebase_content` всё ещё валиден!

---

### Кеширование в messages (диалоговый контекст)

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Here is a large document to analyze:\n\n" + large_document,
                    "cache_control": {"type": "ephemeral"}  # ← Кешируем user message
                }
            ]
        },
        {
            "role": "assistant",
            "content": "I'll analyze this document..."
        },
        {
            "role": "user",
            "content": "Now tell me about section 3"
        }
    ]
)
```

**Use case**: Длинный диалог, где большой документ загружен один раз, а затем пользователь задаёт несколько вопросов.

---

## 🚀 Интеграция с Claude Code

### Автоматическое кеширование в Claude Code

**Claude Code CLI уже использует prompt caching автоматически!** Вам не нужно ничего настраивать.

#### Что кешируется по умолчанию:

1. **System prompt** — инструкции из `CLAUDE.md` (глобальные и проектные)
2. **Tool definitions** — определения всех доступных инструментов (Read, Edit, Bash, etc.)
3. **Codebase context** — содержимое файлов, прочитанных ранее в сессии
4. **MCP tool definitions** — определения инструментов из MCP серверов

#### Пример сессии:

**Запрос 1**: "Read src/specify_cli/__init__.py and explain the CLI structure"
```
Input tokens: 2,000 (query + новые файлы)
Cache creation: 15,000 (system + tools + codebase)
```

**Запрос 2** (через 1 минуту): "Now add a new command called 'validate'"
```
Input tokens: 1,500 (query)
Cache read: 15,000 (system + tools + codebase)  # 90% дешевле!
```

**Запрос 3** (через 10 минут, кеш истёк):
```
Input tokens: 2,000
Cache creation: 15,000  # Кеш пересоздан (TTL истёк)
```

---

### Ручное управление кешированием (Advanced)

Если вы используете Claude API напрямую в своём коде (не через Claude Code):

```python
# spec-kit пример: кеширование спецификации для /speckit.implement
import anthropic

client = anthropic.Anthropic()

spec_content = open("memory/spec.md").read()  # 10K tokens
plan_content = open("memory/plan.md").read()  # 8K tokens

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    system=[
        {
            "type": "text",
            "text": "You are implementing a feature based on a specification and plan."
        },
        {
            "type": "text",
            "text": f"# Specification\n\n{spec_content}",
            "cache_control": {"type": "ephemeral"}  # Кешируем spec
        },
        {
            "type": "text",
            "text": f"# Implementation Plan\n\n{plan_content}",
            "cache_control": {"type": "ephemeral"}  # Кешируем plan
        }
    ],
    messages=[
        {"role": "user", "content": "Implement task TASK-003: Add input validation"}
    ]
)

# Последующие запросы для других задач будут использовать кеш spec + plan
```

**Экономия**: Если вы реализуете 10 задач подряд, spec и plan читаются из кеша 9 раз (экономия ~150K токенов за сессию!)

---

## 💰 Стоимость кеширования

### Тарифы (2026-01-13)

| Модель | Input | Cache Write | Cache Read | Output |
|--------|-------|-------------|------------|--------|
| **Sonnet 4.5** | $3.00/MTok | $3.75/MTok | **$0.30/MTok** | $15/MTok |
| **Haiku 4** | $0.80/MTok | $1.00/MTok | **$0.08/MTok** | $4/MTok |
| **Opus 4.5** | $15/MTok | $18.75/MTok | **$1.50/MTok** | $75/MTok |

### Расчёт окупаемости

**Вопрос**: Когда кеш окупается?

**Формула**:
```
Cost(cache write) = tokens × $3.75/MTok
Cost(cache read)  = tokens × $0.30/MTok
Cost(no cache)    = tokens × $3.00/MTok

Окупается после N запросов, где:
N = cache_write_cost / (no_cache_cost - cache_read_cost)
N = ($3.75/MTok) / ($3.00/MTok - $0.30/MTok)
N = 1.39 запросов
```

**Вывод**: Кеш окупается уже после **2-го запроса**! Всё, что после — чистая экономия.

---

### Примеры экономии

#### Пример 1: Разработка с Claude Code (10 запросов в сессии)

**Без кеша**:
```
10 requests × 50,000 tokens × $3/MTok = $1.50
```

**С кешем** (9 cache hits):
```
Request 1: 50,000 tokens × $3.75/MTok (cache write) = $0.1875
Requests 2-10: 9 × (5,000 × $3/MTok + 45,000 × $0.30/MTok) = 9 × $0.15 = $1.35
Total: $0.1875 + $0.15 = $0.3375 (first request) + $0.135 (each subsequent) × 9 = $1.41

Wait, let me recalculate properly:
Request 1 (cache write): 5K normal + 45K write = $0.015 + $0.16875 = $0.18375
Requests 2-10 (cache hit): 9 × (5K normal + 45K read) = 9 × ($0.015 + $0.0135) = 9 × $0.0285 = $0.2565
Total: $0.18375 + $0.2565 = $0.44025

Savings: $1.50 - $0.44025 = $1.05975 (70% экономия)
```

#### Пример 2: Реализация spec-kit фичи (20 задач)

**Spec + Plan = 50K tokens, query = 2K tokens**

**Без кеша**:
```
20 requests × 52,000 tokens × $3/MTok = $3.12
```

**С кешем** (4 cache refreshes, 5 запросов per cache):
```
Cache writes: 4 × 50K × $3.75/MTok = $0.75
Cache reads: 16 × 50K × $0.30/MTok = $0.24
Normal input: 20 × 2K × $3/MTok = $0.12
Total: $0.75 + $0.24 + $0.12 = $1.11

Savings: $3.12 - $1.11 = $2.01 (64% экономия)
```

---

## ⚙️ Best Practices

### 1. Размещение cache_control в конце блоков

**❌ Неправильно**:
```python
system=[
    {
        "type": "text",
        "text": small_instruction,
        "cache_control": {"type": "ephemeral"}  # Только 100 tokens, не окупится
    },
    {
        "type": "text",
        "text": large_codebase  # 30K tokens, НЕ кешируется
    }
]
```

**✅ Правильно**:
```python
system=[
    {
        "type": "text",
        "text": small_instruction  # 100 tokens
    },
    {
        "type": "text",
        "text": large_codebase,
        "cache_control": {"type": "ephemeral"}  # Кешируется всё до этой точки (30.1K tokens)
    }
]
```

**Правило**: `cache_control` применяется ко **всему контенту до breakpoint**, не только к текущему блоку.

---

### 2. Минимальный размер кеш-блока

**Минимум**: 1024 tokens

**Почему**: Cache write стоит дороже обычного input ($3.75 vs $3.00). Для окупаемости нужно минимум 2 запроса.

**Пример расчёта**:
```
1024 tokens:
- Cache write: $0.00384
- Cache read:  $0.000307
- No cache:    $0.00307

Break-even: $0.00384 / ($0.00307 - $0.000307) = 1.39 requests

Вывод: Окупается после 2-го запроса ✅
```

**512 tokens** (не рекомендуется):
```
- Cache write: $0.00192
- Cache read:  $0.000154
- No cache:    $0.001536

Break-even: $0.00192 / ($0.001536 - $0.000154) = 1.39 requests

Но API не кеширует блоки < 1024 tokens, так что это теоретический расчёт.
```

---

### 3. Группировка стабильного контента

**Организуйте промпт от стабильного к изменчивому**:

```python
system=[
    # Слой 1: Почти никогда не меняется (кешировать!)
    {"type": "text", "text": "Base instructions..."},
    {"type": "text", "text": constitution_content, "cache_control": {"type": "ephemeral"}},

    # Слой 2: Меняется редко (кешировать!)
    {"type": "text", "text": project_spec_content, "cache_control": {"type": "ephemeral"}},

    # Слой 3: Меняется часто (НЕ кешировать)
    {"type": "text", "text": f"Current task: {task_description}"}  # Без cache_control
]
```

**Эффект**: Если меняется только `task_description`, слои 1 и 2 остаются в кеше.

---

### 4. Использование в multi-turn диалогах

**Для чат-ботов и интерактивных приложений**:

```python
conversation_history = []

# Turn 1
conversation_history.append({
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": large_document,
            "cache_control": {"type": "ephemeral"}  # Кешируем документ
        }
    ]
})

response1 = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=conversation_history
)

conversation_history.append({
    "role": "assistant",
    "content": response1.content[0].text
})

# Turn 2 - документ уже в кеше
conversation_history.append({
    "role": "user",
    "content": "Summarize section 3"
})

response2 = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=conversation_history  # large_document read from cache
)
```

**Use case**: Анализ длинных документов, code review, многоступенчатая отладка.

---

### 5. Мониторинг cache hit rate

**Проверяйте метрики**:

```python
usage = response.usage

print(f"Input tokens: {usage.input_tokens}")
print(f"Cache creation: {usage.cache_creation_input_tokens}")
print(f"Cache reads: {usage.cache_read_input_tokens}")

cache_hit_rate = usage.cache_read_input_tokens / (
    usage.input_tokens + usage.cache_read_input_tokens
) if usage.cache_read_input_tokens > 0 else 0

print(f"Cache hit rate: {cache_hit_rate:.1%}")
```

**Целевой показатель**: > 70% cache hit rate для активных сессий.

---

## 📊 Диагностика и оптимизация

### Проблема 1: Низкий cache hit rate (< 30%)

**Причины**:
- TTL истекает (5 минут между запросами)
- Контент постоянно меняется
- Кеш-блоки слишком маленькие (< 1024 tokens)

**Решение**:
```python
# Если запросы редкие (> 5 min), переструктурируйте:
# Вместо кеширования всего контекста, кешируйте только базовые инструкции

system=[
    {
        "type": "text",
        "text": base_instructions,  # Стабильно
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": dynamic_context  # Не кешируется
    }
]
```

---

### Проблема 2: Высокая стоимость cache write

**Симптомы**: Cache creation tokens > 100K per request

**Причины**:
- Слишком большой кеш-блок
- Контент меняется каждый раз (кеш не переиспользуется)

**Решение**:
```python
# Разбейте на несколько кеш-блоков с разной частотой изменения
system=[
    {
        "type": "text",
        "text": stable_large_content,  # 50K tokens, меняется редко
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": semi_stable_content,  # 30K tokens, меняется иногда
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": dynamic_small_content  # 5K tokens, меняется часто (НЕ кешируется)
    }
]
```

---

### Проблема 3: Cache invalidation

**Симптомы**: Кеш часто инвалидируется (cache reads = 0)

**Причины**:
- Изменение кешируемого контента (даже 1 символ = новый кеш)
- Изменение порядка блоков
- Изменение `cache_control` breakpoints

**Решение**:
```python
# Используйте content-addressed hashing для версионирования
import hashlib

content_hash = hashlib.sha256(codebase_content.encode()).hexdigest()[:8]

system=[
    {
        "type": "text",
        "text": f"Codebase version: {content_hash}\n\n{codebase_content}",
        "cache_control": {"type": "ephemeral"}
    }
]

# Если content_hash не меняется, кеш остаётся валидным
```

---

## 🔍 Интеграция с spec-kit

### Use Case 1: /speckit.implement с кешированием

```python
# В templates/commands/speckit.implement.md добавьте:
# (псевдокод для иллюстрации, реальная интеграция через Claude Code API)

def implement_feature_with_caching():
    spec = read_file("memory/spec.md")
    plan = read_file("memory/plan.md")
    tasks = read_file("memory/tasks.md")
    constitution = read_file("memory/constitution.md")

    # Создаём кешируемый контекст
    system_context = [
        {
            "type": "text",
            "text": "You are implementing a feature using TDD..."
        },
        {
            "type": "text",
            "text": f"# Constitution\n\n{constitution}",
            "cache_control": {"type": "ephemeral"}  # Стабильно
        },
        {
            "type": "text",
            "text": f"# Specification\n\n{spec}",
            "cache_control": {"type": "ephemeral"}  # Стабильно
        },
        {
            "type": "text",
            "text": f"# Plan\n\n{plan}",
            "cache_control": {"type": "ephemeral"}  # Стабильно
        },
        {
            "type": "text",
            "text": f"# Tasks\n\n{tasks}"  # НЕ кешируется (часто меняется при выполнении)
        }
    ]

    # Выполняем все задачи с переиспользованием кеша
    for task in parse_tasks(tasks):
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            system=system_context,
            messages=[
                {"role": "user", "content": f"Implement {task.id}: {task.description}"}
            ]
        )

        # Constitution, spec, plan читаются из кеша!
        print(f"Cache reads: {response.usage.cache_read_input_tokens}")
```

**Экономия**: Для 20 задач — ~$2 за всю реализацию вместо ~$4 (50% дешевле).

---

### Use Case 2: /speckit.clarify iterations

```python
# Многократные уточнения спецификации
def clarify_spec_with_caching():
    original_spec = read_file("memory/spec.md")

    for clarification_round in range(5):
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            system=[
                {
                    "type": "text",
                    "text": "You are clarifying ambiguous requirements...",
                },
                {
                    "type": "text",
                    "text": f"# Original Spec\n\n{original_spec}",
                    "cache_control": {"type": "ephemeral"}  # Кешируется
                }
            ],
            messages=[
                {"role": "user", "content": f"Clarification round {clarification_round}..."}
            ]
        )

        # Original spec читается из кеша в rounds 2-5
```

---

### Use Case 3: Batch task execution

```python
# spec-kit batch mode для параллельных задач
import asyncio

async def execute_tasks_parallel_with_cache():
    spec = read_file("memory/spec.md")
    plan = read_file("memory/plan.md")

    # Все задачи используют один и тот же кеш
    tasks = [
        {"id": "TASK-001", "desc": "Setup test framework"},
        {"id": "TASK-002", "desc": "Implement validation"},
        {"id": "TASK-003", "desc": "Add error handling"}
    ]

    async def execute_task(task):
        response = await client.messages.create_async(
            model="claude-sonnet-4-5-20250929",
            system=[
                {"type": "text", "text": "You are implementing..."},
                {"type": "text", "text": f"# Spec\n{spec}", "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": f"# Plan\n{plan}", "cache_control": {"type": "ephemeral"}}
            ],
            messages=[{"role": "user", "content": f"Implement {task['id']}"}]
        )
        return response

    # Параллельное выполнение с общим кешем
    results = await asyncio.gather(*[execute_task(t) for t in tasks])

    # Все 3 задачи используют кеш spec + plan (огромная экономия!)
```

---

## 🛠️ Инструменты и мониторинг

### 1. Claude API Dashboard

**URL**: https://console.anthropic.com/settings/usage

**Метрики**:
- Input tokens (regular)
- Cache creation tokens
- Cache read tokens
- Total cost breakdown

**Как использовать**:
1. Откройте dashboard после сессии Claude Code
2. Проверьте соотношение cache reads / total input
3. Целевой показатель: > 60% cache read tokens

---

### 2. Логирование cache stats

**В вашем коде (Python)**:

```python
import json
from datetime import datetime

def log_cache_stats(response, request_id):
    stats = {
        "timestamp": datetime.now().isoformat(),
        "request_id": request_id,
        "input_tokens": response.usage.input_tokens,
        "cache_creation": response.usage.cache_creation_input_tokens,
        "cache_reads": response.usage.cache_read_input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cache_hit_rate": (
            response.usage.cache_read_input_tokens /
            (response.usage.input_tokens + response.usage.cache_read_input_tokens)
            if response.usage.cache_read_input_tokens > 0 else 0
        )
    }

    with open("cache_stats.jsonl", "a") as f:
        f.write(json.dumps(stats) + "\n")
```

**Анализ логов**:
```bash
# Средний cache hit rate за сессию
cat cache_stats.jsonl | jq -s 'map(.cache_hit_rate) | add / length'

# Общая экономия токенов
cat cache_stats.jsonl | jq -s 'map(.cache_reads) | add'

# Топ-3 запроса с наибольшей экономией
cat cache_stats.jsonl | jq -s 'sort_by(-.cache_reads) | .[0:3]'
```

---

### 3. MCP Optimizer интеграция

**mcp-optimizer может анализировать cache usage!**

```bash
# Запустите optimizer на вашем проекте
cd /tmp/mcp-optimizer
source .venv/bin/activate
python -m mcp_optimizer analyze --project /path/to/spec-kit

# Optimizer покажет:
# - Рекомендации по cache_control placement
# - Оптимальный размер кеш-блоков
# - Прогноз экономии токенов
```

---

## 📚 Дополнительные ресурсы

### Официальная документация

- **Prompt Caching API Docs**: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- **Pricing**: https://www.anthropic.com/pricing
- **Usage Dashboard**: https://console.anthropic.com/settings/usage
- **API Reference**: https://docs.anthropic.com/en/api/messages

### Примеры кода

- **Anthropic Cookbook**: https://github.com/anthropics/anthropic-cookbook/tree/main/skills/caching
- **Python SDK**: https://github.com/anthropics/anthropic-sdk-python
- **TypeScript SDK**: https://github.com/anthropics/anthropic-sdk-typescript

### Альтернативные стратегии

Если prompt caching не подходит (запросы редкие, контент уникальный):

1. **Semantic Chunking** — разбивайте большие документы на смысловые чанки
2. **RAG (Retrieval-Augmented Generation)** — используйте vector DB (Pinecone) для поиска релевантных частей
3. **Prompt Compression** — используйте `llmlingua` для сжатия промптов
4. **Dynamic Context** — загружайте только необходимый контекст для каждого запроса

---

## ✅ Чеклист внедрения

- [ ] **Измерить baseline** — запустите 10 запросов без кеширования, посчитайте стоимость
- [ ] **Идентифицировать стабильный контент** — что не меняется между запросами?
- [ ] **Добавить cache_control** — пометьте стабильные блоки (минимум 1024 tokens)
- [ ] **Тестировать TTL** — убедитесь, что запросы укладываются в 5-минутное окно
- [ ] **Мониторить cache hit rate** — целевой показатель > 60%
- [ ] **Оптимизировать breakpoints** — используйте до 4 кеш-блоков для разных слоёв стабильности
- [ ] **Логировать метрики** — собирайте cache stats для анализа
- [ ] **Рассчитать ROI** — сравните стоимость до и после (ожидаемая экономия: 50-70%)

---

## 🎯 Итоговые рекомендации

### Для Claude Code пользователей:

✅ **Prompt caching уже работает автоматически** — ничего настраивать не нужно
✅ **Держите сессии активными** — делайте запросы каждые 2-3 минуты для сохранения кеша
✅ **Используйте MCP token optimization servers** — meta-mcp + modular-mcp + memory
✅ **Мониторьте usage в dashboard** — https://console.anthropic.com

### Для spec-kit workflows:

✅ **Кешируйте constitution, spec, plan** — они стабильны в течение всей реализации
✅ **НЕ кешируйте tasks.md** — часто обновляется при выполнении задач
✅ **Используйте batch mode** — все параллельные задачи используют общий кеш
✅ **Логируйте экономию** — добавьте cache stats в CHANGELOG.md

### Для API интеграций:

✅ **Минимум 1024 tokens на кеш-блок**
✅ **До 4 breakpoints** для разных слоёв стабильности
✅ **5-минутный TTL** — планируйте запросы соответственно
✅ **Мониторинг cache hit rate** — целевой показатель > 60%

---

**Версия документа**: 1.0.0
**Дата создания**: 2026-01-13
**Автор**: Claude Sonnet 4.5 (spec-kit documentation assistant)
**Следующее обновление**: При изменении API pricing или функций кеширования

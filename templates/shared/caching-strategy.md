# Anthropic Prompt Caching Strategy [REF:PC-001]

This module documents the API-level prompt caching strategy using Anthropic's native `cache_control` directive.

---

## Overview

**Prompt Caching** allows marking content for reuse across API calls within a session:
- Reduces input tokens by **80-90%** on repeated calls
- Provides **50-70% faster** inference times
- Automatically managed by Anthropic API

---

## Cache Control Directive

```yaml
# In command frontmatter
claude_code:
  cache_control:
    system_prompt: ephemeral    # Cache command instructions
    constitution: ephemeral      # Cache project principles
    templates: ephemeral         # Cache loaded template content
    artifacts: ephemeral         # Cache spec/plan/tasks content
    ttl: session                 # session | 3600 | permanent
```

---

## Cacheable Content Types

### 1. Always Cached (High Reuse)

| Content | Cache Key | TTL | Invalidation |
|---------|-----------|-----|--------------|
| System prompt | command-name | session | Never |
| Constitution | `constitution.md:mtime` | session | File change |
| Shared modules | `module-path:mtime` | session | File change |

### 2. Session Cached (Medium Reuse)

| Content | Cache Key | TTL | Invalidation |
|---------|-----------|-----|--------------|
| Spec artifact | `spec.md:mtime` | session | File change |
| Plan artifact | `plan.md:mtime` | session | File change |
| Tasks artifact | `tasks.md:mtime` | session | File change |
| Concept | `concept.md:mtime` | session | File change |

### 3. Never Cached

| Content | Reason |
|---------|--------|
| User input | Dynamic, changes every call |
| File paths | May resolve differently |
| Git status | Changes between calls |

---

## API Integration Pattern

```python
# Anthropic API call with caching
messages = [{
    "role": "user",
    "content": [{
        "type": "text",
        "text": cached_context,
        "cache_control": {"type": "ephemeral"}
    }, {
        "type": "text",
        "text": user_input
        # No cache_control = always fresh
    }]
}]

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=messages,
    system=[{
        "type": "text",
        "text": system_prompt,
        "cache_control": {"type": "ephemeral"}
    }]
)
```

---

## Per-Subagent Caching

Subagents can inherit or override parent cache settings:

```yaml
subagents:
  - role: brownfield-detector
    model_override: haiku
    cache_control:
      enabled: true              # Use caching
      type: ephemeral            # Cache type
      share_with_parent: true    # Inherit parent's cached context
      additional_cache:          # Extra content to cache
        - baseline.md
```

---

## Content Markers

Mark stable sections in template body for explicit caching hints:

```markdown
## System Context [CACHE:ephemeral]

This section contains stable project context.
```

### Marker Syntax

| Marker | Meaning |
|--------|---------|
| `[CACHE:ephemeral]` | Cache for session duration |
| `[CACHE:permanent]` | Cache indefinitely (rare) |
| `[NO-CACHE]` | Never cache this section |

---

## Cache Hierarchy Integration

Prompt caching works with the existing cache layers:

```
┌─────────────────────────────────────────────────┐
│ L0: Prompt Cache (Anthropic API)                │  ← NEW
│  • System prompts, constitution                 │
│  • TTL: Session (managed by API)                │
│  • Savings: 80-90% input tokens                 │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ L1: In-Memory (Command scope)                   │
│  • File contents, glob results                  │
│  • TTL: Command lifetime                        │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ L2: Session Cache                               │
│  • LLM responses, computed results              │
│  • TTL: 30 minutes                              │
└─────────────────────────────────────────────────┘
```

---

## Expected Performance

| Scenario | Without Caching | With Caching | Improvement |
|----------|-----------------|--------------|-------------|
| First call | 5000 tokens | 5000 tokens | - |
| Repeat call | 5000 tokens | 500-1000 tokens | 80-90% |
| Workflow (4 cmds) | 20000 tokens | 6000 tokens | 70% |

---

## Best Practices

1. **Cache stable content first**: Constitution, system prompts, templates
2. **Order matters**: Place cached content before fresh content in messages
3. **Avoid over-caching**: Dynamic content should remain fresh
4. **Monitor cache hits**: Check API response headers for cache utilization
5. **Invalidate on change**: Use file mtime in cache keys

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No cache hits | Content too different | Increase similarity threshold |
| Stale responses | File changed after cache | Include mtime in cache key |
| High token count | Cache not applied | Verify `cache_control` in request |

---

## References

- [Anthropic Prompt Caching Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- `templates/shared/core/parallel-loading.md` - File-level caching
- `SPEC-KIT-ACCELERATION-STRATEGIES.md` section 3.3

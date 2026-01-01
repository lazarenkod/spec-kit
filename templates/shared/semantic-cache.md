# Semantic Caching

## Purpose

Enable query-level caching using semantic similarity matching. When a user submits a query that is semantically similar to a previous query (even with different wording), the cached result can be returned instantly.

**Example**: "Create user auth" and "Build login functionality" → 0.97 similarity → cache hit

---

## How It Works

### Embedding-Based Similarity

```text
SEMANTIC_CACHE_FLOW:
  1. User submits query: "Build login functionality"
  2. NORMALIZE query → remove stopwords, stem terms
  3. ENCODE normalized query → 384-dim embedding vector
  4. COMPARE against cached embeddings using cosine similarity
  5. IF max_similarity >= 0.95:
       RETURN cached_result
       LOG: "Semantic cache hit: matched '{original}' (similarity: 0.97)"
     ELSE:
       GENERATE new result
       STORE(query, embedding, result) in cache
```

### Encoder Selection

| Encoder | Dimensions | Speed | Accuracy | Use Case |
|---------|-----------|-------|----------|----------|
| all-MiniLM-L6-v2 | 384 | 5ms | 0.95 | **Recommended** - fast, good quality |
| all-mpnet-base-v2 | 768 | 15ms | 0.98 | High accuracy requirements |
| text-embedding-3-small | 1536 | API | 0.96 | External API fallback |

**Default**: `all-MiniLM-L6-v2` — optimal balance of speed and accuracy for command queries.

---

## Configuration

### Frontmatter Directive

Add `semantic_cache` to the `claude_code` block in command templates:

```yaml
claude_code:
  model: opus
  cache_control:
    system_prompt: ephemeral
    constitution: ephemeral
    ttl: session
  semantic_cache:
    enabled: true
    encoder: all-MiniLM-L6-v2
    similarity_threshold: 0.95
    cache_scope: session
    cacheable_fields:
      - user_input
      - feature_description
    max_entries: 1000
    ttl: 3600
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | true | Enable/disable semantic caching |
| `encoder` | string | all-MiniLM-L6-v2 | Embedding model to use |
| `similarity_threshold` | float | 0.95 | Minimum similarity for cache hit |
| `cache_scope` | enum | session | session, project, or global |
| `cacheable_fields` | array | [user_input] | Fields to include in cache key |
| `max_entries` | integer | 1000 | Maximum cached entries |
| `ttl` | integer | 3600 | Time-to-live in seconds |

### Compact Format (COMPRESSED templates)

```yaml
semantic_cache: {enabled: true, encoder: all-MiniLM-L6-v2, threshold: 0.95, scope: session}
```

---

## Query Normalization

Before encoding, normalize queries to improve matching:

### Intent Synonyms

```yaml
normalization:
  intent_synonyms:
    create: ["add", "implement", "build", "new", "make", "generate"]
    modify: ["update", "enhance", "improve", "fix", "change", "edit"]
    remove: ["delete", "deprecate", "drop", "eliminate"]
    analyze: ["review", "check", "validate", "audit", "inspect"]
```

### Feature Synonyms

```yaml
normalization:
  feature_synonyms:
    auth: ["authentication", "login", "sign-in", "user auth", "authorization"]
    database: ["persistence", "data store", "db", "storage"]
    api: ["endpoint", "route", "REST", "interface"]
    ui: ["frontend", "interface", "view", "component"]
```

### Normalization Algorithm

```text
FUNCTION normalize_query(query: str) -> str:
  # Step 1: Lowercase
  query = query.lower()

  # Step 2: Replace intent synonyms
  FOR intent, synonyms IN intent_synonyms:
    FOR synonym IN synonyms:
      query = query.replace(synonym, intent)

  # Step 3: Replace feature synonyms
  FOR feature, synonyms IN feature_synonyms:
    FOR synonym IN synonyms:
      query = query.replace(synonym, feature)

  # Step 4: Remove stopwords
  query = remove_stopwords(query)

  RETURN query
```

---

## Similarity Thresholds

### Threshold Interpretation

| Similarity | Confidence | Action |
|------------|------------|--------|
| ≥ 0.95 | High | Auto-use cached result |
| 0.85 - 0.94 | Medium | Confirm with user before using |
| < 0.85 | Low | Generate fresh result |

### Threshold Tuning by Command

```yaml
# High-stakes commands need higher threshold
specify:
  similarity_threshold: 0.95

# Fast-iteration commands can use lower threshold
implement:
  similarity_threshold: 0.90

# Validation commands need exact matches
analyze:
  similarity_threshold: 0.98
```

---

## Cache Scope

### Session Scope (Default)

```text
SCOPE: session
- Cache persists for current Claude Code session
- Cleared on session end
- Storage: In-memory
- Best for: Iterative development within one feature
```

### Project Scope

```text
SCOPE: project
- Cache persists across sessions for this project
- Storage: `.speckit/cache/semantic.db`
- Invalidated on: Git commit that changes specs/
- Best for: Team collaboration, repeated queries
```

### Global Scope

```text
SCOPE: global
- Cache persists across all projects
- Storage: `~/.speckit/semantic-cache/`
- TTL: 7 days
- Best for: Common patterns (CRUD, auth, etc.)
```

---

## Cache Key Generation

### Single-Field Key

```text
cache_key = hash(normalize(user_input))
embedding = encode(normalize(user_input))
```

### Multi-Field Key

```text
cacheable_fields: [user_input, feature_description, project_type]

cache_key = hash(
  normalize(user_input) +
  normalize(feature_description) +
  project_type
)
embedding = encode(concatenated_normalized_text)
```

---

## Example Matches

| Query A | Query B | Similarity | Match? |
|---------|---------|------------|--------|
| "Create user authentication" | "Build login functionality" | 0.97 | ✅ Hit |
| "Add API endpoint for products" | "Implement REST route for products" | 0.94 | ✅ Hit |
| "Fix bug in login form" | "Repair authentication UI" | 0.91 | ⚠️ Confirm |
| "Create payment system" | "Build user profile page" | 0.45 | ❌ Miss |
| "Specify user dashboard" | "Specify admin dashboard" | 0.78 | ❌ Miss |

---

## Cache Storage

### In-Memory Structure (Session Scope)

```text
SEMANTIC_CACHE = {
  entries: [
    {
      normalized_query: "create auth feature",
      embedding: [0.12, -0.34, ...],  # 384-dim vector
      result_hash: "sha256:abc123...",
      result_path: "specs/auth/spec.md",
      created_at: timestamp,
      hit_count: 3
    },
    ...
  ],
  embeddings_matrix: [[...], [...]],  # Stacked for batch similarity
  max_entries: 1000,
  ttl: 3600
}
```

### Disk Structure (Project/Global Scope)

```text
.speckit/cache/semantic.db (SQLite)
├── queries         # normalized_query, embedding_blob, created_at
├── results         # result_hash, result_path, content_preview
└── metadata        # hit_count, last_accessed, ttl
```

---

## Integration with Cache Hierarchy

Semantic cache integrates as Layer 1 in the cache hierarchy:

```text
CACHE_HIERARCHY:
  L0: Prompt Cache (Anthropic API)
      ↳ 80-90% input token reduction
      ↳ Caches: system prompts, constitution, templates

  L1: Semantic Cache (Embeddings)     ← THIS MODULE
      ↳ 10-100x faster for similar queries
      ↳ Caches: user queries → generated artifacts

  L2: File Cache (In-Memory)
      ↳ 60-70% hit rate
      ↳ Caches: file contents, glob results

  L3: Session Cache
      ↳ Response-level caching
      ↳ Caches: LLM responses, API results
```

### Lookup Order

```text
FUNCTION cached_generate(query: str) -> Result:
  # L1: Check semantic cache first
  semantic_result = semantic_cache.get(query)
  IF semantic_result AND semantic_result.similarity >= threshold:
    RETURN semantic_result.cached_artifact

  # L0: Use prompt caching for generation
  result = generate_with_prompt_cache(query)

  # L1: Store in semantic cache
  semantic_cache.put(query, result)

  RETURN result
```

---

## Performance Metrics

### Tracking

```text
SEMANTIC_CACHE_METRICS:
  hit_rate: 45%              # Queries matched semantically
  miss_rate: 55%             # Fresh generations required
  avg_similarity: 0.93       # Average match confidence
  cache_latency: 12ms        # Embedding + matching time
  savings_per_hit: 5-10 min  # Time saved per cache hit
```

### Reporting Format

```text
┌─────────────────────────────────────────┐
│ Semantic Cache Stats                     │
├─────────────────────────────────────────┤
│ Hit Rate: 45% (18/40 queries)           │
│ Avg Similarity: 0.93                     │
│ Cache Latency: 12ms                      │
│ Time Saved: ~90 minutes                  │
├─────────────────────────────────────────┤
│ Recent Hit:                              │
│   Query: "user authentication"           │
│   Matched: "login system" (0.97)        │
│   Saved: 5 min                          │
└─────────────────────────────────────────┘
```

---

## Error Handling

### Cache Miss Graceful Degradation

```text
IF semantic_cache.unavailable:
  LOG_WARNING: "Semantic cache unavailable, generating fresh"
  SKIP semantic lookup
  PROCEED with normal generation
  DO NOT fail command
```

### Stale Cache Detection

```text
IF result.source_files_changed:
  INVALIDATE cached_entry
  LOG: "Cache invalidated: source files modified since caching"
  REGENERATE result
```

---

## Best Practices

1. **Threshold Selection**: Start with 0.95, lower to 0.90 if too few hits
2. **Scope Selection**: Use `session` for dev, `project` for team workflows
3. **Cache Warming**: Pre-populate cache with common query patterns
4. **Monitoring**: Track hit rates, adjust thresholds based on false positives
5. **Invalidation**: Clear cache when spec templates change significantly

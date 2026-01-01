# Six-Level Cache Hierarchy [REF:CH-001]

This module defines the complete cache hierarchy for Spec Kit commands, enabling 20-30% latency reduction through intelligent multi-level caching.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ L0: Prompt Cache (Anthropic API)                            │  v0.0.61
│  • System prompts, constitution                             │
│  • TTL: Session (managed by API)                            │
│  • Savings: 80-90% input tokens                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ L1: Semantic Cache (Embeddings)                             │  v0.0.62
│  • Query similarity matching                                │
│  • TTL: Session/1 hour                                      │
│  • Savings: 10-100x for similar queries                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ L2: In-Memory Cache (Command scope)                         │
│  • File contents, glob results, parsed YAML                 │
│  • TTL: Command lifetime (2-5 min)                          │
│  • Size: 50-100MB RAM                                       │
│  • Hit rate: 60-70% (saves 10-50ms per hit)                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ L3: Session Cache (RAM)                                     │
│  • LLM responses, API results, computed values              │
│  • TTL: 30 minutes                                          │
│  • Size: 200-500MB RAM                                      │
│  • Hit rate: 30-40% (saves 2-5s per hit)                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ L4: Project Cache (Disk)                                    │  v0.0.63
│  • Compiled templates, analyses, constitution hash          │
│  • TTL: Git commit SHA (invalidate on commit)               │
│  • Size: 10-50MB disk                                       │
│  • Path: .speckit/cache/                                    │
│  • Hit rate: 20-30% (saves 500ms-2s per hit)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ L5: Global Cache (Disk)                                     │  v0.0.63
│  • Context7 docs, common templates, library info            │
│  • TTL: 7 days                                              │
│  • Size: 100-200MB disk                                     │
│  • Path: ~/.speckit/cache/                                  │
│  • Hit rate: 40-50% (saves 1-3s per hit)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Level Specifications

### L0: Prompt Cache (Anthropic API)

**Purpose**: Token reduction for repeated system content

```yaml
l0_prompt:
  scope: api_call
  storage: anthropic_managed
  contents:
    - system_prompt
    - constitution
    - template_content
    - artifacts
  ttl: session
  invalidation: api_managed
  savings: 80-90% input tokens
```

**Key Pattern**: Managed by Anthropic API via `cache_control: ephemeral`

**Reference**: `templates/shared/caching-strategy.md`

---

### L1: Semantic Cache (Embeddings)

**Purpose**: Query-level similarity matching for expensive operations

```yaml
l1_semantic:
  scope: session | project | global
  storage: RAM + disk
  contents:
    - user_queries
    - feature_descriptions
    - clarification_responses
  encoder: all-MiniLM-L6-v2
  similarity_threshold: 0.95
  ttl: 3600  # 1 hour
  invalidation: ttl_expiry | manual
  savings: 10-100x for similar queries
```

**Key Pattern**: `{scope}:{encoder}:{query_hash}`

**Reference**: `templates/shared/semantic-cache.md`

---

### L2: In-Memory Cache (Command Scope)

**Purpose**: Fast access to file contents during command execution

```yaml
l2_memory:
  scope: command
  storage: RAM
  contents:
    - file_contents
    - glob_results
    - parsed_yaml
    - frontmatter_data
  ttl: 300  # 5 minutes (command lifetime)
  max_size: 100MB
  hit_rate: 60-70%
  savings: 10-50ms per hit
  invalidation: command_end | file_mtime
```

**Key Pattern**: `{file_path}:{mtime}`

**Cacheable Content**:
| Content Type | Cache Key | TTL | Size Limit |
|--------------|-----------|-----|------------|
| File reads | `file:{path}:{mtime}` | command | 10MB/file |
| Glob results | `glob:{pattern}:{dir}` | command | 1000 entries |
| YAML parsing | `yaml:{path}:{mtime}` | command | 1MB |
| Frontmatter | `fm:{path}:{mtime}` | command | 100KB |

---

### L3: Session Cache (RAM)

**Purpose**: Persist expensive computations across commands

```yaml
l3_session:
  scope: session
  storage: RAM
  contents:
    - llm_responses
    - api_results
    - computed_values
    - spec_analyses
  ttl: 1800  # 30 minutes
  max_size: 500MB
  hit_rate: 30-40%
  savings: 2-5s per hit
  invalidation: session_end | ttl_expiry
```

**Key Pattern**: `{session_id}:{operation}:{input_hash}`

**Cacheable Content**:
| Content Type | Cache Key | TTL | Size Limit |
|--------------|-----------|-----|------------|
| LLM response | `llm:{prompt_hash}:{model}` | 30 min | 100KB |
| API call | `api:{endpoint}:{params_hash}` | 30 min | 1MB |
| Computed | `calc:{operation}:{input_hash}` | 30 min | 10MB |
| Analysis | `analysis:{artifact}:{mtime}` | 30 min | 5MB |

---

### L4: Project Cache (Disk) [NEW]

**Purpose**: Cross-session caching within a project

```yaml
l4_project:
  scope: project
  storage: disk
  path: .speckit/cache/
  contents:
    - compiled_templates
    - analyses
    - constitution_hash
    - dependency_graphs
    - cqs_scores
    - dqs_scores
  ttl: git_commit_sha  # Invalidate on new commit
  max_size: 50MB
  hit_rate: 20-30%
  savings: 500ms-2s per hit
  invalidation: git_commit | file_change | manual
```

**Key Pattern**: `{project_root}:{content_type}:{git_sha}`

**Directory Structure**:
```
.speckit/cache/
├── templates/              # Compiled command templates
│   ├── specify.cache      # Cached template (gzipped)
│   └── concept.cache
├── analyses/               # Spec analysis results
│   ├── spec-001.json      # CQS/DQS scores
│   └── concept-001.json
├── constitution/           # Constitution derivatives
│   └── hash.json          # Constitution hash + parsed rules
├── dependencies/           # Dependency graphs
│   └── dag.json           # Feature dependency DAG
└── manifest.json          # Cache manifest with git SHA
```

**Manifest Format**:
```json
{
  "version": "1.0",
  "git_sha": "abc123",
  "created_at": "2025-01-01T00:00:00Z",
  "entries": {
    "templates/specify.cache": {
      "source": "templates/commands/specify.md",
      "mtime": 1704067200,
      "size": 15234
    }
  }
}
```

**Invalidation Rules**:
| Trigger | Action |
|---------|--------|
| New git commit | Clear all caches |
| File mtime change | Clear affected cache |
| Manual `--clear-cache` | Clear all caches |
| TTL expiry (30 days) | Clear stale entries |

---

### L5: Global Cache (Disk) [NEW]

**Purpose**: Cross-project caching for shared resources

```yaml
l5_global:
  scope: global
  storage: disk
  path: ~/.speckit/cache/
  contents:
    - context7_docs
    - common_templates
    - library_info
    - npm_package_info
    - github_api_responses
  ttl: 604800  # 7 days
  max_size: 200MB
  hit_rate: 40-50%
  savings: 1-3s per hit
  invalidation: ttl_expiry | manual_clear | version_change
```

**Key Pattern**: `{content_type}:{identifier}:{version}:{hash}`

**Directory Structure**:
```
~/.speckit/cache/
├── context7/              # Library documentation
│   ├── react-19.json     # Cached Context7 results
│   └── typescript-5.json
├── templates/             # Global template cache
│   └── shared/           # Common shared modules
├── npm/                   # npm package metadata
│   └── package-info.json
├── github/                # GitHub API cache
│   └── repos/
└── manifest.json         # Global cache manifest
```

**Manifest Format**:
```json
{
  "version": "1.0",
  "speckit_version": "0.0.63",
  "created_at": "2025-01-01T00:00:00Z",
  "size_mb": 45.2,
  "entries": {
    "context7/react-19.json": {
      "library_id": "/facebook/react",
      "version": "19.0.0",
      "fetched_at": "2025-01-01T00:00:00Z",
      "ttl": 604800,
      "size": 1024567
    }
  }
}
```

**Invalidation Rules**:
| Trigger | Action |
|---------|--------|
| TTL expiry (7 days) | Clear specific entry |
| Manual `--clear-global-cache` | Clear all global caches |
| Spec Kit version change | Clear incompatible caches |
| Size limit exceeded | LRU eviction |

---

## Cache Lookup Algorithm

```text
CACHE_LOOKUP(key, content_type):

  # 1. Check L2 (in-memory, command scope)
  IF L2.has(key):
    L2.update_access_time(key)
    RETURN L2.get(key)

  # 2. Check L3 (session RAM)
  IF L3.has(key) AND NOT L3.expired(key):
    L3.update_access_time(key)
    L2.set(key, L3.get(key))  # Promote to L2
    RETURN L3.get(key)

  # 3. Check L4 (project disk)
  IF L4.valid_for_commit(current_git_sha):
    IF L4.has(key):
      value = L4.load(key)
      L3.set(key, value)  # Promote to L3
      L2.set(key, value)  # Promote to L2
      RETURN value

  # 4. Check L5 (global disk)
  IF L5.has(key) AND NOT L5.expired(key):
    value = L5.load(key)
    L4.set(key, value)  # Promote to L4 (if project-relevant)
    L3.set(key, value)  # Promote to L3
    L2.set(key, value)  # Promote to L2
    RETURN value

  # 5. Cache miss - fetch and store
  value = FETCH(key, content_type)
  STORE_AT_APPROPRIATE_LEVEL(key, value, content_type)
  RETURN value


STORE_AT_APPROPRIATE_LEVEL(key, value, content_type):

  MATCH content_type:
    CASE "file_content", "glob_result", "yaml":
      L2.set(key, value)

    CASE "llm_response", "api_result", "analysis":
      L3.set(key, value)

    CASE "template", "constitution", "dependency_graph":
      L4.set(key, value)
      L3.set(key, value)

    CASE "context7_doc", "npm_info", "github_api":
      L5.set(key, value)
      L3.set(key, value)
```

---

## Frontmatter Configuration

### Full Format

```yaml
claude_code:
  cache_hierarchy:
    l2_memory:
      enabled: true
      ttl: 300
      max_size: 100MB
    l3_session:
      enabled: true
      ttl: 1800
      max_size: 500MB
    l4_project:
      enabled: true
      path: .speckit/cache
      invalidation: git_sha
      max_size: 50MB
    l5_global:
      enabled: true
      path: ~/.speckit/cache
      ttl: 604800
      max_size: 200MB
```

### Compressed Format

```yaml
cache_hierarchy: {l2: true, l3: true, l4: {path: .speckit/cache}, l5: {path: ~/.speckit/cache}}
```

### Minimal Format (defaults)

```yaml
cache_hierarchy: full
```

---

## Performance Impact

| Level | Hit Rate | Time Saved | Use Case |
|-------|----------|------------|----------|
| L0 | 90%+ | 2-3s | Repeated prompts |
| L1 | 40-50% | 5-60s | Similar queries |
| L2 | 60-70% | 10-50ms | File re-reads |
| L3 | 30-40% | 2-5s | Repeated operations |
| L4 | 20-30% | 500ms-2s | Cross-session |
| L5 | 40-50% | 1-3s | Library docs |
| **Total** | | | **20-30% latency reduction** |

### Cumulative Impact

```text
Typical /speckit.specify workflow:

Without caching:
  Read constitution:     200ms
  Parse templates:       100ms
  Load Context7 docs:    2000ms
  LLM inference:         30000ms
  Total:                 32300ms

With full cache hierarchy:
  L4 hit - constitution: 10ms  (saved 190ms)
  L2 hit - templates:    5ms   (saved 95ms)
  L5 hit - Context7:     50ms  (saved 1950ms)
  L0 hit - prompt cache: 25000ms (saved 5000ms)
  Total:                 25065ms

Improvement: 22% faster
```

---

## Cache Management Commands

### Clear Caches

```bash
# Clear project cache
specify cache clear --project

# Clear global cache
specify cache clear --global

# Clear all caches
specify cache clear --all

# Clear specific entry
specify cache clear --key "context7/react-19.json"
```

### Cache Statistics

```bash
# Show cache stats
specify cache stats

# Output:
# ┌─────────────────────────────────────────┐
# │ Cache Statistics                        │
# ├─────────────────────────────────────────┤
# │ L4 (Project):  23.5 MB / 50 MB (47%)    │
# │   Entries: 45                           │
# │   Hit rate: 28%                         │
# │                                         │
# │ L5 (Global):  89.2 MB / 200 MB (45%)    │
# │   Entries: 234                          │
# │   Hit rate: 52%                         │
# └─────────────────────────────────────────┘
```

### Warm Cache

```bash
# Pre-populate project cache
specify cache warm --project

# Pre-populate global cache for common libraries
specify cache warm --global --libraries react,typescript,nextjs
```

---

## Best Practices

### 1. Cache-Aware Template Design

```yaml
# Mark stable content for aggressive caching
claude_code:
  cache_control:
    system_prompt: ephemeral    # L0
    constitution: ephemeral     # L0
  cache_hierarchy:
    l4_project:
      enabled: true
      contents:
        - compiled_template
        - constitution_hash
```

### 2. Invalidation Strategy

| Content Type | Invalidation Trigger | Level |
|--------------|---------------------|-------|
| File content | mtime change | L2 |
| LLM response | prompt change | L3 |
| Template | git commit | L4 |
| Library docs | 7-day TTL | L5 |

### 3. Size Management

```yaml
# Eviction policy (LRU)
cache_hierarchy:
  l4_project:
    max_size: 50MB
    eviction: lru
    min_entries: 10  # Keep at least 10 entries
```

### 4. Debug Cache Behavior

```yaml
# Enable cache debugging
claude_code:
  cache_hierarchy:
    debug: true  # Log cache hits/misses
```

---

## Gitignore Integration

Add to project `.gitignore`:

```gitignore
# Spec Kit project cache
.speckit/cache/
```

Global cache is in `~/.speckit/cache/` (outside project).

---

## References

- `templates/shared/caching-strategy.md` - L0 Prompt caching
- `templates/shared/semantic-cache.md` - L1 Semantic caching
- `SPEC-KIT-ACCELERATION-STRATEGIES.md` - Section 3.1

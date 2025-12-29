# API Verification Batching

## Purpose

Batch Context7/WebFetch calls to reduce network latency and improve API documentation verification speed.

## Performance Impact

| Mode | Time | Savings |
|------|------|---------|
| Sequential | 25-40s | baseline |
| Batched | 8-12s | 70% |

## Configuration

```yaml
api_batch:
  enabled: true
  skip_flag: "--no-batch-verify"
  max_batch_size: 5
  cache_ttl: 3600  # 1 hour
  cache_file: ".cache/api-verification.yaml"
```

## Batch Verification Algorithm

```text
BATCH_API_VERIFICATION(tasks):

  # 1. Extract all unique dependencies from tasks
  dependencies = {}
  FOR task IN tasks:
    IF task.has_marker("[DEP:xxx]"):
      dep_id = extract_dep_id(task)
      IF dep_id NOT IN dependencies:
        dependencies[dep_id] = {
          id: dep_id,
          tasks: [task.id],
          docs_url: lookup_in_dependency_registry(dep_id)
        }
      ELSE:
        dependencies[dep_id].tasks.append(task.id)

    IF task.has_marker("[APIDOC:url]"):
      url = extract_apidoc_url(task)
      IF url NOT IN dependencies:
        dependencies[url] = {
          id: url,
          tasks: [task.id],
          docs_url: url
        }
      ELSE:
        dependencies[url].tasks.append(task.id)

  # 2. Check session cache first
  cached = load_cache(cache_file)
  uncached = []

  FOR dep IN dependencies.values():
    cache_entry = cached.get(dep.id)
    IF cache_entry AND cache_entry.expires_at > now():
      dep.verified = cache_entry.verified
      dep.cached = true
    ELSE:
      uncached.append(dep)

  # 3. Batch fetch uncached dependencies
  IF uncached.length > 0:
    batches = chunk(uncached, max_batch_size)

    FOR batch IN batches:
      # Parallel fetch within batch
      results = await parallel_fetch([
        verify_single_dep(dep) FOR dep IN batch
      ])

      # Update cache
      FOR result IN results:
        save_to_cache(cache_file, result.id, {
          verified: result.verified,
          docs_url: result.docs_url,
          methods: result.methods,
          expires_at: now() + cache_ttl
        })

  # 4. Return consolidated results
  RETURN dependencies


FUNCTION verify_single_dep(dep):
  IF context7_available():
    # Use Context7 MCP for library docs
    library_id = await context7.resolve_library_id(dep.id)
    IF library_id:
      docs = await context7.get_library_docs(library_id, topic="API reference")
      RETURN {
        id: dep.id,
        verified: true,
        docs_url: library_id,
        methods: extract_methods(docs)
      }

  # Fallback to WebFetch
  IF dep.docs_url:
    content = await web_fetch(dep.docs_url)
    IF content.status == 200:
      RETURN {
        id: dep.id,
        verified: true,
        docs_url: dep.docs_url,
        methods: extract_methods_from_html(content.body)
      }

  RETURN {
    id: dep.id,
    verified: false,
    error: "Documentation not found"
  }
```

## Cache Structure

```yaml
# FEATURE_DIR/.cache/api-verification.yaml
version: "1.0"
created_at: "2025-12-29T10:30:00Z"
entries:
  "react-query@5.x":
    verified: true
    docs_url: "/tanstack/query"
    methods:
      - name: "useQuery"
        signature: "useQuery(options: QueryOptions)"
        verified: true
      - name: "useMutation"
        signature: "useMutation(options: MutationOptions)"
        verified: true
    checked_at: "2025-12-29T10:30:00Z"
    expires_at: "2025-12-29T11:30:00Z"

  "zod@3.x":
    verified: true
    docs_url: "/colinhacks/zod"
    methods:
      - name: "z.object"
        signature: "z.object(shape: ZodRawShape)"
        verified: true
    checked_at: "2025-12-29T10:30:00Z"
    expires_at: "2025-12-29T11:30:00Z"

  "stripe-api":
    verified: true
    docs_url: "https://stripe.com/docs/api"
    methods:
      - name: "charges.create"
        signature: "stripe.charges.create(params)"
        verified: true
        deprecation_notice: "Use PaymentIntents instead"
    checked_at: "2025-12-29T10:30:00Z"
    expires_at: "2025-12-29T11:30:00Z"
```

## Method Verification

```text
VERIFY_METHOD_USAGE(dep, method_name, expected_params):
  cached_method = dep.methods.find(m => m.name == method_name)

  IF NOT cached_method:
    # Not in cache, need to fetch
    RETURN {verified: false, reason: "Method not found in docs"}

  IF cached_method.deprecation_notice:
    RETURN {
      verified: true,
      warning: f"Deprecated: {cached_method.deprecation_notice}"
    }

  # Verify parameters match
  IF expected_params:
    signature_params = parse_signature(cached_method.signature)
    FOR param IN expected_params:
      IF param NOT IN signature_params:
        RETURN {
          verified: false,
          reason: f"Parameter '{param}' not found in {method_name} signature"
        }

  RETURN {verified: true}
```

## Cache Invalidation

```text
INVALIDATE_CACHE(trigger):
  SWITCH trigger:
    CASE "dependency_update":
      # When plan.md Dependency Registry changes
      checksum = hash(read_file("plan.md"))
      IF checksum != cached.plan_checksum:
        clear_cache()
        cached.plan_checksum = checksum

    CASE "ttl_expired":
      # Automatic on read
      FOR entry IN cached.entries:
        IF entry.expires_at < now():
          delete_entry(entry.id)

    CASE "manual":
      # User runs --clear-api-cache
      clear_cache()
```

## Integration with implement.md

Reference in Step 3.5:

```text
Read `templates/shared/implement/api-batch.md` and apply batch verification.

INSTEAD OF:
  FOR EACH task with [DEP:]:
    verify_api(task)  # Sequential, slow

USE:
  dependencies = BATCH_API_VERIFICATION(all_tasks)  # Parallel, cached
  FOR task IN tasks:
    dep = dependencies[task.dep_id]
    IF NOT dep.verified:
      BLOCK task
```

## Output Format

```text
📡 API Verification (Batch Mode)
├── Dependencies found: 8
├── Cache hits: 5 (62%)
├── Cache misses: 3
├── Batch fetches: 1 (batch of 3)
├── Total time: 9.2s (vs ~35s sequential)
└── Status: SUCCESS

Verification Results:
├── react-query@5.x: ✓ Verified (cached)
│   ├── useQuery: ✓ Valid
│   └── useMutation: ✓ Valid
├── zod@3.x: ✓ Verified (cached)
├── stripe-api: ✓ Verified (fetched)
│   ├── charges.create: ⚠️ Deprecated - use PaymentIntents
│   └── paymentIntents.create: ✓ Valid
└── custom-api: ✓ Verified (fetched)
```

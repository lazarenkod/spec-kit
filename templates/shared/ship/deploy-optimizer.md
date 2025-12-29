# Deploy Optimizer

## Purpose

Accelerate deployment through Docker layer intelligence, Helm template caching, adaptive timeouts, and version-based skip logic to reduce deploy time by 70-85%.

## Performance Impact

| Mode | Time | Savings |
|------|------|---------|
| Default deploy | 2-5 min | baseline |
| With optimizer | 30s-2 min | 70-85% |
| Version cache hit | 5-10s | 95%+ |

## Configuration

```yaml
optimization:
  deploy:
    enabled: true
    skip_flag: "--no-deploy-optimize"
    docker_cache: true           # Use BuildKit cache
    helm_template_cache: true    # Cache rendered templates
    adaptive_timeout: true       # Dynamic rollout timeout
    parallel_deployments: true   # Deploy multiple services in parallel
    version_skip: true           # Skip if same version deployed
```

## Docker Layer Intelligence

```text
DOCKER_CACHE_CONFIG:
  registry: "${REGISTRY}/cache"
  cache_mode: "max"              # max | min | inline
  build_args:
    BUILDKIT_INLINE_CACHE: "1"


FUNCTION optimized_docker_build(dockerfile, context, tag):
  # 1. Check source fingerprint
  source_hash = calculate_source_hash(context)
  cached_hash = read_cache("docker-source-hash")

  IF source_hash == cached_hash:
    LOG f"✓ Source unchanged, checking registry for {tag}"
    IF image_exists_in_registry(tag):
      LOG "✓ Using existing image"
      RETURN tag

  # 2. Pre-warm base images
  base_images = extract_base_images(dockerfile)
  parallel_pull(base_images)

  # 3. Build with cache
  cache_from = f"{DOCKER_CACHE_CONFIG.registry}:cache"

  build_cmd = f"""
    docker buildx build \
      --cache-from=type=registry,ref={cache_from} \
      --cache-to=type=registry,ref={cache_from},mode=max \
      --build-arg BUILDKIT_INLINE_CACHE=1 \
      -t {tag} \
      -f {dockerfile} \
      {context}
  """

  start_time = now()
  run(build_cmd)
  build_time = now() - start_time

  # 4. Save fingerprint
  save_cache("docker-source-hash", source_hash)

  LOG f"Build completed in {build_time}s"
  RETURN tag


FUNCTION calculate_source_hash(context):
  hash = sha256()

  # Hash source files (excluding node_modules, .git, etc)
  FOR file IN glob(f"{context}/**/*"):
    IF should_include_in_hash(file):
      hash.update(read_file(file))

  # Include dependency lock files
  FOR lockfile IN ["package-lock.json", "yarn.lock", "pnpm-lock.yaml", "go.sum", "Cargo.lock"]:
    IF exists(f"{context}/{lockfile}"):
      hash.update(read_file(f"{context}/{lockfile}"))

  RETURN hash.hexdigest()


FUNCTION should_include_in_hash(file):
  EXCLUDE_PATTERNS = [
    "node_modules/",
    ".git/",
    "__pycache__/",
    "*.pyc",
    ".env*",
    "dist/",
    "build/",
    "*.log"
  ]

  FOR pattern IN EXCLUDE_PATTERNS:
    IF fnmatch(file, pattern):
      RETURN false

  RETURN true
```

## Helm Template Caching

```text
HELM_CACHE_DIR = ".speckit/cache/helm/"

FUNCTION cached_helm_upgrade(release, chart, values, namespace):
  # 1. Calculate template hash
  template_hash = calculate_helm_hash(chart, values)
  cache_key = f"{release}-{namespace}-{template_hash[:16]}"
  cached_manifest = f"{HELM_CACHE_DIR}/{cache_key}.yaml"

  # 2. Check cache
  IF exists(cached_manifest):
    manifest_age = now() - mtime(cached_manifest)
    IF manifest_age < HELM_CACHE_TTL:
      LOG f"✓ Using cached Helm templates ({cache_key})"
      # Apply cached manifest directly (faster than helm upgrade)
      kubectl apply -f $cached_manifest -n $namespace
      RETURN SUCCESS

  # 3. Render and cache templates
  LOG "Rendering Helm templates..."
  helm template $release $chart -f $values -n $namespace > $cached_manifest

  # 4. Run upgrade
  RETURN run_helm_upgrade(release, chart, values, namespace)


FUNCTION calculate_helm_hash(chart, values):
  hash = sha256()

  # Hash chart files
  FOR file IN glob(f"{chart}/**/*"):
    hash.update(read_file(file))

  # Hash values
  hash.update(read_file(values))

  # Include chart version
  chart_yaml = yaml.load(f"{chart}/Chart.yaml")
  hash.update(chart_yaml.version)

  RETURN hash.hexdigest()
```

## Adaptive Timeout

```text
TIMEOUT_CONFIG:
  min_timeout: 30           # seconds
  max_timeout: 300          # 5 minutes
  per_pod_factor: 10        # seconds per pod
  per_mb_image_factor: 0.5  # seconds per MB of image


FUNCTION calculate_adaptive_timeout(deployment_spec):
  # Base timeout
  timeout = TIMEOUT_CONFIG.min_timeout

  # Factor in replica count
  replicas = deployment_spec.replicas OR 1
  timeout += replicas * TIMEOUT_CONFIG.per_pod_factor

  # Factor in image size (if available)
  image_size_mb = get_image_size_mb(deployment_spec.image)
  IF image_size_mb:
    timeout += image_size_mb * TIMEOUT_CONFIG.per_mb_image_factor

  # Factor in historical startup time
  historical_avg = get_historical_startup_time(deployment_spec.name)
  IF historical_avg:
    timeout = max(timeout, historical_avg * 1.5)

  # Apply bounds
  timeout = clamp(timeout, TIMEOUT_CONFIG.min_timeout, TIMEOUT_CONFIG.max_timeout)

  LOG f"Calculated timeout: {timeout}s (replicas={replicas}, image={image_size_mb}MB)"
  RETURN timeout


FUNCTION get_historical_startup_time(deployment_name):
  history_file = f".speckit/metrics/{deployment_name}-startup.json"
  IF NOT exists(history_file):
    RETURN None

  history = json.load(history_file)
  IF len(history.times) < 3:
    RETURN None

  # Use p90 of recent startup times
  recent = history.times[-10:]
  RETURN percentile(recent, 90)


FUNCTION record_startup_time(deployment_name, duration):
  history_file = f".speckit/metrics/{deployment_name}-startup.json"
  history = json.load(history_file) IF exists(history_file) ELSE {times: []}
  history.times.append(duration)
  history.times = history.times[-100:]  # Keep last 100
  json.dump(history_file, history)
```

## Version-Based Skip

```text
VERSION_CACHE = ".speckit/state/{ENV}/deployed-versions.json"

FUNCTION should_skip_deploy(service_name, new_version):
  IF NOT exists(VERSION_CACHE):
    RETURN false

  versions = json.load(VERSION_CACHE)
  deployed_version = versions.get(service_name)

  IF deployed_version == new_version:
    LOG f"✓ {service_name} already at version {new_version}"
    RETURN true

  LOG f"Version change: {deployed_version} → {new_version}"
  RETURN false


FUNCTION update_deployed_version(service_name, version):
  versions = json.load(VERSION_CACHE) IF exists(VERSION_CACHE) ELSE {}
  versions[service_name] = version
  versions["_updated_at"] = now().isoformat()
  json.dump(VERSION_CACHE, versions)
```

## Parallel Deployments

```text
FUNCTION parallel_deploy(deployments):
  # Group deployments by dependency
  independent = []
  dependent = {}

  FOR deploy IN deployments:
    IF deploy.depends_on IS EMPTY:
      independent.append(deploy)
    ELSE:
      FOR dep IN deploy.depends_on:
        IF dep NOT IN dependent:
          dependent[dep] = []
        dependent[dep].append(deploy)

  # Deploy independent services in parallel
  LOG f"Deploying {len(independent)} independent services in parallel"
  results = parallel_execute([
    deploy_service(d) FOR d IN independent
  ])

  # Check for failures
  failed = [r FOR r IN results IF r.failed]
  IF failed:
    RETURN FAILURE(failed)

  # Deploy dependent services
  FOR completed_service IN [r.name FOR r IN results IF r.success]:
    IF completed_service IN dependent:
      next_batch = dependent[completed_service]
      LOG f"Deploying {len(next_batch)} services depending on {completed_service}"
      parallel_execute([deploy_service(d) FOR d IN next_batch])

  RETURN SUCCESS
```

## Health Check Optimization

```text
HEALTH_CHECK_CONFIG:
  initial_delay: 2          # seconds
  max_delay: 30             # seconds
  multiplier: 1.5           # exponential backoff
  max_attempts: 10
  circuit_breaker_threshold: 3


FUNCTION smart_health_check(endpoint):
  delay = HEALTH_CHECK_CONFIG.initial_delay
  consecutive_failures = 0

  FOR attempt IN range(1, HEALTH_CHECK_CONFIG.max_attempts + 1):
    result = check_health(endpoint)

    IF result.healthy:
      LOG f"✓ Health check passed (attempt {attempt})"
      RETURN SUCCESS

    consecutive_failures += 1

    # Circuit breaker
    IF consecutive_failures >= HEALTH_CHECK_CONFIG.circuit_breaker_threshold:
      LOG f"✗ Circuit breaker triggered after {consecutive_failures} failures"
      RETURN FAILURE("Service unhealthy - circuit breaker triggered")

    # Exponential backoff
    sleep(delay)
    delay = min(delay * HEALTH_CHECK_CONFIG.multiplier, HEALTH_CHECK_CONFIG.max_delay)
    LOG f"Health check failed, retrying in {delay}s (attempt {attempt}/{HEALTH_CHECK_CONFIG.max_attempts})"

  RETURN FAILURE(f"Health check failed after {HEALTH_CHECK_CONFIG.max_attempts} attempts")


FUNCTION parallel_health_checks(endpoints):
  # Run all health checks in parallel
  results = parallel_execute([
    smart_health_check(ep) FOR ep IN endpoints
  ])

  failed = [r FOR r IN results IF r.failed]
  IF failed:
    RETURN FAILURE(failed)

  RETURN SUCCESS
```

## Optimized Deploy Flow

```text
FUNCTION optimized_deploy(services, environment):
  LOG "🚀 Deploy Optimizer"

  # 1. Version check
  services_to_deploy = []
  FOR service IN services:
    IF should_skip_deploy(service.name, service.version):
      LOG f"✓ Skipping {service.name} (version unchanged)"
    ELSE:
      services_to_deploy.append(service)

  IF len(services_to_deploy) == 0:
    LOG "✓ All services up to date, nothing to deploy"
    RETURN SUCCESS

  # 2. Build images with cache
  FOR service IN services_to_deploy:
    optimized_docker_build(
      service.dockerfile,
      service.context,
      service.image_tag
    )

  # 3. Calculate adaptive timeouts
  FOR service IN services_to_deploy:
    service.timeout = calculate_adaptive_timeout(service)

  # 4. Deploy in parallel where possible
  result = parallel_deploy(services_to_deploy)

  IF result.failed:
    RETURN result

  # 5. Health checks
  endpoints = [s.health_endpoint FOR s IN services_to_deploy]
  health_result = parallel_health_checks(endpoints)

  IF health_result.failed:
    RETURN health_result

  # 6. Update version cache
  FOR service IN services_to_deploy:
    update_deployed_version(service.name, service.version)

  RETURN SUCCESS
```

## Integration with ship.md

```text
# At deploy phase start:
Read `templates/shared/ship/deploy-optimizer.md` and apply.

# Replace standard deploy:
INSTEAD OF:
  docker build ...
  docker push ...
  helm upgrade --wait --timeout=5m

USE:
  result = optimized_deploy(services, environment)
```

## Output Format

```text
🚀 Deploy Optimizer
├── Version Check:
│   ├── api-server: v1.2.3 → v1.2.4 (DEPLOY)
│   ├── worker: v1.2.3 (SKIP - unchanged)
│   └── web-app: v1.2.3 → v1.2.4 (DEPLOY)
├── Docker Build:
│   ├── api-server: 12.3s (cache hit: 85%)
│   └── web-app: 8.7s (cache hit: 92%)
├── Helm Deploy:
│   ├── api-server: timeout=45s, parallel
│   └── web-app: timeout=30s, parallel
├── Health Checks:
│   ├── api-server: ✓ 2.1s (attempt 1)
│   └── web-app: ✓ 3.4s (attempt 2, backoff)
├── Timing:
│   ├── Build: 21.0s
│   ├── Deploy: 48.2s
│   └── Health: 5.5s
└── Total: 74.7s (vs ~240s baseline)
```

## CLI Flags

```bash
# Skip version check
speckit ship --force-deploy

# Override timeout
speckit ship --deploy-timeout=120

# Disable parallel deployments
speckit ship --sequential-deploy

# Skip Docker cache
speckit ship --no-docker-cache
```

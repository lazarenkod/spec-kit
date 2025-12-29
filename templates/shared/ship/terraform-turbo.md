# Terraform Turbo Mode

## Purpose

Optimize Terraform operations through provider caching, parallelism tuning, fingerprint-based skip logic, and state optimization to reduce provision time by 60-70%.

## Performance Impact

| Mode | Time | Savings |
|------|------|---------|
| Default Terraform | 5-15 min | baseline |
| With Turbo Mode | 2-5 min | 60-70% |
| Fingerprint cache hit | 5-10s | 95%+ |

## Configuration

```yaml
optimization:
  terraform:
    enabled: true
    skip_flag: "--no-tf-turbo"
    parallelism: auto          # auto | 10 | 20 | 30
    provider_cache: true       # Cache providers across sessions
    fingerprint_skip: true     # Skip if inputs unchanged
    targeted_plan: true        # Use -target for known changes
    state_cache_ttl: 300       # 5 minutes
```

## Provider Cache

```text
PROVIDER_CACHE_DIR = ~/.speckit/terraform-cache/providers/

FUNCTION initialize_provider_cache():
  IF NOT exists(PROVIDER_CACHE_DIR):
    mkdir -p $PROVIDER_CACHE_DIR

  # Configure Terraform to use shared plugin cache
  export TF_PLUGIN_CACHE_DIR=$PROVIDER_CACHE_DIR

  LOG "Provider cache initialized at $PROVIDER_CACHE_DIR"


FUNCTION cache_provider_check(required_providers):
  cached = []
  missing = []

  FOR provider IN required_providers:
    cache_path = "$PROVIDER_CACHE_DIR/${provider.namespace}/${provider.name}/${provider.version}"
    IF exists(cache_path):
      cached.append(provider)
      LOG f"✓ Provider {provider.name} v{provider.version} (cached)"
    ELSE:
      missing.append(provider)
      LOG f"↓ Provider {provider.name} v{provider.version} (downloading)"

  RETURN {cached, missing}
```

## Parallelism Tuning

```text
FUNCTION calculate_optimal_parallelism(resource_count):
  # Based on benchmarks, optimal parallelism scales with resource count
  # but has diminishing returns above 30

  IF resource_count < 10:
    RETURN 10  # Default for small configs
  ELIF resource_count < 50:
    RETURN 20  # Medium configs
  ELIF resource_count < 100:
    RETURN 30  # Large configs
  ELSE:
    RETURN 30  # Cap at 30 (diminishing returns beyond)


FUNCTION count_resources():
  # Quick resource count from terraform state or plan
  result = run("terraform state list 2>/dev/null | wc -l")
  IF result.exit_code == 0:
    RETURN int(result.stdout.strip())

  # Fallback: count resource blocks in .tf files
  result = run("grep -r 'resource \"' *.tf | wc -l")
  RETURN int(result.stdout.strip())


FUNCTION apply_with_parallelism():
  resource_count = count_resources()
  parallelism = calculate_optimal_parallelism(resource_count)

  LOG f"Resources: {resource_count}, Parallelism: {parallelism}"

  terraform apply -parallelism=$parallelism -auto-approve
```

## Fingerprint-Based Skip

```text
FINGERPRINT_INPUTS = [
  "infra.yaml",
  "terraform/*.tf",
  "terraform/*.tfvars",
  "terraform/modules/**/*.tf"
]

FINGERPRINT_CACHE = ".speckit/state/{ENV}/terraform-fingerprint.sha256"
OUTPUTS_CACHE = ".speckit/state/{ENV}/terraform-outputs.json"


FUNCTION calculate_fingerprint():
  content_hash = sha256()

  FOR pattern IN FINGERPRINT_INPUTS:
    FOR file IN glob(pattern):
      content_hash.update(read_file(file))

  # Include terraform version
  tf_version = run("terraform version -json").stdout
  content_hash.update(tf_version)

  RETURN content_hash.hexdigest()


FUNCTION should_skip_provision():
  current_fingerprint = calculate_fingerprint()

  IF NOT exists(FINGERPRINT_CACHE):
    LOG "No fingerprint cache, will provision"
    RETURN false, None

  cached_fingerprint = read_file(FINGERPRINT_CACHE)

  IF current_fingerprint == cached_fingerprint:
    IF exists(OUTPUTS_CACHE):
      outputs = json.load(OUTPUTS_CACHE)
      LOG f"✓ Infrastructure unchanged (fingerprint: {current_fingerprint[:8]}...)"
      RETURN true, outputs
    ELSE:
      LOG "Fingerprint match but outputs missing, will provision"
      RETURN false, None

  LOG f"Infrastructure changed (old: {cached_fingerprint[:8]}... → new: {current_fingerprint[:8]}...)"
  RETURN false, None


FUNCTION save_provision_state(outputs):
  fingerprint = calculate_fingerprint()
  write_file(FINGERPRINT_CACHE, fingerprint)
  json.dump(OUTPUTS_CACHE, outputs)
  LOG f"Provision state saved (fingerprint: {fingerprint[:8]}...)"
```

## Targeted Plan

```text
FUNCTION detect_changed_resources():
  # Get files changed since last successful provision
  last_provision_commit = read_file(".speckit/state/{ENV}/last-provision-commit")
  changed_files = git diff --name-only $last_provision_commit HEAD -- terraform/

  changed_resources = set()

  FOR file IN changed_files:
    # Parse file to find resource definitions
    content = read_file(file)
    FOR match IN regex.findall(r'resource "(\w+)" "(\w+)"', content):
      resource_type, resource_name = match
      changed_resources.add(f"{resource_type}.{resource_name}")

  RETURN list(changed_resources)


FUNCTION plan_with_targets(changed_resources):
  IF len(changed_resources) == 0:
    LOG "No specific resources changed, running full plan"
    RETURN terraform plan

  IF len(changed_resources) > 10:
    LOG f"Too many changed resources ({len(changed_resources)}), running full plan"
    RETURN terraform plan

  targets = " ".join([f"-target={r}" FOR r IN changed_resources])
  LOG f"Running targeted plan for {len(changed_resources)} resources"
  RETURN terraform plan $targets
```

## State Optimization

```text
STATE_CACHE = ".speckit/state/{ENV}/"

FUNCTION optimize_state_operations():
  # 1. Local state snapshot for faster reads
  IF NOT exists(STATE_CACHE + "terraform.tfstate.cache"):
    terraform state pull > $STATE_CACHE/terraform.tfstate.cache

  # 2. Skip drift detection on recent apply
  last_apply = read_file(STATE_CACHE + "last_apply.timestamp")
  IF (now() - last_apply) < 5_minutes:
    LOG "Recent apply detected, skipping drift check"
    export TF_SKIP_REMOTE_STATE_DRIFT_CHECK=1

  # 3. Use cached outputs when possible
  IF exists(STATE_CACHE + "outputs.json"):
    age = now() - mtime(STATE_CACHE + "outputs.json")
    IF age < STATE_CACHE_TTL:
      LOG f"Using cached outputs (age: {age}s)"
      RETURN json.load(STATE_CACHE + "outputs.json")

  RETURN None


FUNCTION refresh_state_cache():
  # Update local cache after successful operation
  terraform state pull > $STATE_CACHE/terraform.tfstate.cache
  terraform output -json > $STATE_CACHE/outputs.json
  write_file(STATE_CACHE + "last_apply.timestamp", now())
```

## Optimized Provision Flow

```text
FUNCTION terraform_turbo_provision(environment):
  LOG "🚀 Terraform Turbo Mode"

  # 1. Initialize provider cache
  initialize_provider_cache()

  # 2. Check fingerprint
  skip, cached_outputs = should_skip_provision()
  IF skip:
    LOG f"✓ Skipping provision (cached)"
    RETURN cached_outputs

  # 3. Check state optimization
  cached = optimize_state_operations()
  IF cached AND NOT force_refresh:
    RETURN cached

  # 4. Run terraform init (with cached providers)
  init_start = now()
  terraform init -reconfigure
  LOG f"Init completed in {now() - init_start}s"

  # 5. Calculate parallelism
  parallelism = calculate_optimal_parallelism(count_resources())

  # 6. Detect if targeted plan is possible
  changed = detect_changed_resources()
  IF len(changed) > 0 AND len(changed) <= 10:
    targets = " ".join([f"-target={r}" FOR r IN changed])
    plan_cmd = f"terraform plan {targets} -out=tfplan"
  ELSE:
    plan_cmd = "terraform plan -out=tfplan"

  # 7. Run plan
  plan_start = now()
  run(plan_cmd)
  LOG f"Plan completed in {now() - plan_start}s"

  # 8. Apply with optimized parallelism
  apply_start = now()
  terraform apply -parallelism=$parallelism -auto-approve tfplan
  LOG f"Apply completed in {now() - apply_start}s"

  # 9. Cache results
  outputs = terraform output -json
  save_provision_state(outputs)
  refresh_state_cache()

  RETURN outputs
```

## Integration with ship.md

```text
# At provision phase start:
Read `templates/shared/ship/terraform-turbo.md` and apply.

# Replace standard provision:
INSTEAD OF:
  terraform init
  terraform plan
  terraform apply

USE:
  outputs = terraform_turbo_provision(environment)
```

## Output Format

```text
🚀 Terraform Turbo Mode
├── Provider Cache: ~/.speckit/terraform-cache/providers/
│   ├── hashicorp/aws/5.0.0: ✓ cached
│   ├── hashicorp/kubernetes/2.23.0: ✓ cached
│   └── hashicorp/random/3.5.1: ↓ downloading
├── Fingerprint Check:
│   ├── Current: a1b2c3d4...
│   ├── Cached: a1b2c3d4...
│   └── Status: MATCH (skipping provision)
└── Result: Using cached outputs (5.2s)

# Or when provision runs:
🚀 Terraform Turbo Mode
├── Provider Cache: 3/3 providers cached
├── Fingerprint: CHANGED (e5f6g7h8... → i9j0k1l2...)
├── Resources: 47, Parallelism: 20
├── Plan: 3 resources targeted
│   ├── aws_instance.web
│   ├── aws_security_group.web
│   └── aws_lb_target_group.web
├── Timing:
│   ├── Init: 2.1s (cached providers)
│   ├── Plan: 8.3s (targeted)
│   └── Apply: 45.2s (parallelism=20)
└── Total: 55.6s (vs ~180s baseline)
```

## CLI Flags

```bash
# Skip fingerprint optimization
speckit ship --no-fingerprint

# Force full provision (ignore cache)
speckit ship --force-provision

# Override parallelism
speckit ship --tf-parallelism=30

# Disable provider cache
speckit ship --no-provider-cache
```

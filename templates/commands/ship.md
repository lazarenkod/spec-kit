---
description: Provision infrastructure, deploy application, and verify running system in one command
persona: devops-agent
optimization_modules:
  - templates/shared/ship/terraform-turbo.md
  - templates/shared/ship/deploy-optimizer.md
  - templates/shared/ship/test-parallel.md
  - templates/shared/ship/browser-pool.md
  - templates/shared/ship/dependency-dag.md
  - templates/shared/ship/contract-testing.md
  - templates/shared/ship/incremental-tests.md
  - templates/shared/ship/smart-rollback.md
handoff:
  requires: null  # Can run independently if infra.yaml exists
  template: templates/handoff-template.md
handoffs:
  - label: Fix Verification Issues
    agent: speckit.implement
    prompt: |
      Address issues identified in verify-results.md:
      - Fix failing acceptance scenarios
      - Resolve performance issues
      - Address security findings
    auto: false
    condition:
      - "verify-results.md shows FAILED scenarios"
      - "Verification Verdict == FAIL"
    gates:
      - name: "Verification Issues Exist Gate"
        check: "At least one AS-xxx has status FAIL"
        block_if: "All scenarios PASS"
        message: "No verification issues to fix"
  - label: Update Spec with Results
    agent: speckit.specify
    prompt: Update spec.md with verification results and production learnings
    auto: false
    condition:
      - "Verification completed successfully"
      - "New requirements discovered during deployment"
  - label: Analyze Results
    agent: speckit.analyze
    prompt: |
      Run QA verification on deployed system:
      - Verify all AS-xxx scenarios from spec.md
      - Check production health metrics
      - Generate deployment verification report
    auto: true
    condition:
      - "All stages (provision, deploy, verify) completed"
      - "--only verify was not specified"
    gates:
      - name: "Deployment Success Gate"
        check: "deploy stage completed without errors"
        block_if: "deploy stage failed"
        message: "Fix deployment issues before running analysis"
    post_actions:
      - "log: Ship complete, running post-deployment analysis"
pre_gates:
  - name: "Implementation Exists Gate"
    check: "Source code exists to deploy"
    block_if: "No source files found"
    message: "Run /speckit.implement first to create application code"
  - name: "Ship Config Exists Gate"
    check: "infra.yaml OR deploy.yaml exists in FEATURE_DIR or PROJECT_ROOT"
    block_if: "No ship configuration found"
    message: "Create infra.yaml and/or deploy.yaml to define deployment"
scripts:
  sh: scripts/bash/ship.sh
  ps: scripts/powershell/ship.ps1
claude_code:
  model: sonnet
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 6000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
        timeout_per_agent: 180000
        retry_on_failure: 1
      pro:
        thinking_budget: 12000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
        timeout_per_agent: 300000
        retry_on_failure: 2
      max:
        thinking_budget: 24000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
        timeout_per_agent: 900000
        retry_on_failure: 3
  cache_hierarchy: full
  orchestration:
    max_parallel: 8
    conflict_resolution: queue
    timeout_per_agent: 900000
    retry_on_failure: 3
    role_isolation: true
    wave_overlap:
      enabled: true
      threshold: 0.65
  subagents:
    # Wave 1: Infrastructure Setup (parallel)
    - role: infra-provisioner
      role_group: INFRA
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Provision cloud infrastructure for deployment.

        Read `templates/shared/ship/terraform-turbo.md` for optimization strategies.

        Tasks:
        1. Load infra.yaml configuration
        2. Check fingerprint cache for skip eligibility
        3. Generate/update Terraform configuration
        4. Run terraform init and plan
        5. Apply infrastructure changes (if not --dry-run)
        6. Extract outputs for deploy stage

        Apply optimizations:
        - Provider caching
        - Parallelism tuning
        - Fingerprint-based skip

        Output:
        - INFRA_OUTPUTS with database_host, redis_host, k8s_endpoint, etc.
        - Updated .speckit/state/{ENV}/infra-outputs.json
        - Fingerprint cache update

    - role: config-validator
      role_group: INFRA
      parallel: true
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        Validate deployment configuration before provisioning.

        Check:
        - infra.yaml syntax and required fields
        - deploy.yaml syntax and required fields
        - Environment variables are defined
        - Secrets references are valid
        - Resource limits are specified
        - Helm values files exist

        Output:
        - CONFIG_VALID: true/false
        - List of validation errors (if any)
        - Suggested fixes for common issues

    # Wave 2: Deployment (depends on infrastructure)
    - role: deployment-executor
      role_group: BACKEND
      parallel: true
      depends_on: [infra-provisioner, config-validator]
      priority: 20
      model_override: sonnet
      prompt: |
        Execute application deployment to target environment.

        Read `templates/shared/ship/deploy-optimizer.md` for optimization strategies.

        Using INFRA_OUTPUTS from provisioning:

        1. Check if deployment needed (version comparison)
        2. Build and push container image
        3. Deploy with Helm to Kubernetes
        4. Wait for rollout completion
        5. Save deployed version state

        Apply optimizations:
        - Docker layer intelligence
        - Helm template caching
        - Adaptive timeouts

        Output:
        - DEPLOY_SUCCESS: true/false
        - BASE_URL for verification
        - Deployed version details
        - Namespace and pod status

    # Wave 3: Verification (depends on deployment)
    - role: health-checker
      role_group: TESTING
      parallel: true
      depends_on: [deployment-executor]
      priority: 30
      model_override: haiku
      prompt: |
        Verify basic health of deployed application.

        Run quick health checks:
        - HTTP health endpoint (/health)
        - Database connectivity
        - Redis connectivity (if applicable)
        - Basic API endpoint responses

        Output:
        - HEALTH_STATUS: healthy/degraded/unhealthy
        - Individual check results
        - Latency metrics for each check
        - Recommendations if degraded

    - role: smoke-tester
      role_group: TESTING
      parallel: true
      depends_on: [deployment-executor]
      priority: 30
      model_override: sonnet
      prompt: |
        Execute smoke and acceptance tests on deployed application.

        Read optimization modules:
        - `templates/shared/ship/test-parallel.md`
        - `templates/shared/ship/browser-pool.md`
        - `templates/shared/ship/contract-testing.md`
        - `templates/shared/ship/incremental-tests.md`

        Using BASE_URL from deployment:

        1. Run smoke tests (parallel)
        2. Run acceptance tests linked to AS-xxx
        3. Generate verify-results.md
        4. Create snapshot on success (for rollback)
        5. Handle failures per smart-rollback.md

        Apply optimizations:
        - Browser pool pre-warming
        - Incremental test selection
        - Test result caching
        - Contract vs E2E strategy

        Output:
        - FEATURE_DIR/verify-results.md
        - Test summary with pass/fail counts
        - Snapshot ID (if successful)
        - Rollback recommendation (if failed)
flags:
  max_model: "--max-model <opus|sonnet|haiku>"  # Override model cap
---

## User Input

```text
$ARGUMENTS
```

Parse arguments for:
- `--env <environment>`: Target environment (local, staging, production). Default: staging
- `--only <stage>`: Run only specific stage (infra, deploy, verify). Default: all
- `--destroy`: Tear down infrastructure and deployment
- `--dry-run`: Show plan without executing
- `--cloud <provider>`: Override cloud provider (vk, yandex, gcp)
- `--skip-verify`: Skip verification stage

**Optimization flags** (see optimization modules for details):
- `--turbo`: Enable maximum parallelism and skip optional checks
- `--safe`: Use sequential execution with full validation
- `--skip-provision`: Skip provision if fingerprint unchanged
- `--force-deploy`: Force deploy even if version unchanged
- `--force-provision`: Force provision even if fingerprint unchanged
- `--full-e2e`: Run full E2E suite instead of contract tests
- `--full-tests`: Run full test suite instead of incremental
- `--parallel-tests=N`: Control test parallelism (default: 4)
- `--auto-rollback`: Automatically rollback on verification failure
- `--no-rollback`: Disable automatic rollback prompts
- `--sequential-phases`: Disable wave overlap optimization
- `--no-browser-pool`: Disable browser pool pre-warming
- `--no-fingerprint`: Disable fingerprint-based skip logic
- `--no-test-cache`: Ignore cached test results

## Optimization Integration

**Read and apply optimization modules at the start of execution:**

```text
# Load optimization modules (if not using --safe flag)
IF NOT --safe:
  Read `templates/shared/ship/terraform-turbo.md` and apply.
  Read `templates/shared/ship/deploy-optimizer.md` and apply.
  Read `templates/shared/ship/test-parallel.md` and apply.
  Read `templates/shared/ship/browser-pool.md` and apply.
  Read `templates/shared/ship/dependency-dag.md` and apply.
  Read `templates/shared/ship/contract-testing.md` and apply.
  Read `templates/shared/ship/incremental-tests.md` and apply.
  Read `templates/shared/ship/smart-rollback.md` and apply.
```

**Wave Overlap Execution** (enabled by default, disable with `--sequential-phases`):

```text
WAVE_OVERLAP_CONFIG:
  enabled: true
  threshold: 0.80  # Start next phase preparation at 80% completion

# Instead of strict sequential:
#   provision_complete → deploy_start → deploy_complete → verify_start

# Use speculative execution:
#   provision_start
#   AT 80% provision_complete → deploy_prepare (pull images, warm cache)
#   provision_complete → deploy_start
#   AT 80% deploy_complete → verify_prepare (warm browser pool)
#   deploy_complete → verify_start

FUNCTION wave_overlap_execution():
  provision_task = async_start_provision()

  # At 80% provision, start deploy preparation
  ON provision_task.progress >= 80%:
    async_prepare_deploy()  # Pull images, warm Docker cache

  # Wait for provision to complete
  provision_result = await provision_task

  # Start deploy immediately (preparation already done)
  deploy_task = async_start_deploy(provision_result.outputs)

  # At 80% deploy, start verify preparation
  ON deploy_task.progress >= 80%:
    async_prepare_verify()  # Warm browser pool, prepare test data

  # Wait for deploy
  deploy_result = await deploy_task

  # Start verify immediately (preparation already done)
  verify_result = run_verify()

  RETURN ship_result(provision_result, deploy_result, verify_result)
```

**Expected Performance Impact:**

| Scenario | Without Optimization | With Optimization | Savings |
|----------|---------------------|-------------------|---------|
| Clean deploy (staging) | 12 min | 5 min | 58% |
| Small code change | 8 min | 45s | 91% |
| Infra-only change | 10 min | 3 min | 70% |
| Test re-run | 90s | 20s | 78% |
| Rollback | 5 min | 90s | 70% |

## Outline

### Phase 0: Setup and Context Loading

1. Run `{SCRIPT} --json` from repo root and parse:
   - `FEATURE_DIR`: Current feature directory
   - `PROJECT_ROOT`: Repository root
   - `ENV`: Target environment from --env or default
   - `CLOUD`: Cloud provider from infra.yaml or --cloud

2. Load ship configuration:
   - **REQUIRED**: Read infra.yaml (infrastructure spec)
   - **REQUIRED**: Read deploy.yaml (deployment spec)
   - **IF EXISTS**: Read verify.yaml (verification spec)
   - **IF EXISTS**: Read spec.md for AS-xxx acceptance scenarios

3. Load state files from `.speckit/state/{ENV}/`:
   - `infra-state.json`: Terraform state reference and outputs
   - `deployed-version.json`: Currently deployed git SHA
   - `last-verify.json`: Last verification results

4. Detect current git SHA and branch:
   ```bash
   GIT_SHA=$(git rev-parse HEAD)
   GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
   FEATURE_SLUG=$(echo "$GIT_BRANCH" | sed 's/[^a-zA-Z0-9]/-/g' | tr '[:upper:]' '[:lower:]')
   ```

### Phase 1: PROVISION (Infrastructure)

**Optimization:** Apply `templates/shared/ship/terraform-turbo.md` for provider caching, parallelism tuning, and fingerprint-based skip.

**Skip conditions:**
- `--only deploy` or `--only verify` specified
- `--env local` (uses docker-compose, no cloud infra)
- Fingerprint unchanged AND `--force-provision` not specified (see terraform-turbo.md)

**Execution:**

1. **Fingerprint-based skip check** (if optimizations enabled):
   ```text
   fingerprint = calculate_fingerprint(infra.yaml, terraform/*.tf, variables.tfvars)
   IF fingerprint == cached_fingerprint AND NOT --force-provision:
     LOG "✓ Infrastructure unchanged (fingerprint: {fingerprint[:8]}...)"
     RETURN cached_outputs
   ```

2. **Check if infrastructure exists:**
   ```
   IF .speckit/state/{ENV}/infra-state.json exists:
     terraform_state = read(infra-state.json)

     # Check for drift
     drift_check = terraform plan -detailed-exitcode

     IF drift_check.exit_code == 0:
       log("Infrastructure up-to-date, skipping provision")
       outputs = terraform output -json
       GOTO Phase 2
     ELSE IF drift_check.exit_code == 2:
       log("Drift detected, reconciling...")
       # Continue to apply
   ```

2. **Generate Terraform configuration from infra.yaml:**
   ```
   FOR EACH resource in infra.yaml.environments[ENV].resources:
     - Map resource.ref (INFRA-xxx) to Terraform module
     - Apply resource.vars as module variables
     - Use cloud-specific modules (vk-cloud/, yandex/, gcp/)
   ```

3. **Initialize and apply Terraform:**
   ```bash
   cd .speckit/terraform/{ENV}

   terraform init \
     -backend-config="bucket=${PROJECT}-tfstate" \
     -backend-config="key=${ENV}/terraform.tfstate" \
     -backend-config="endpoint=${BACKEND_ENDPOINT}"

   terraform plan -out=tfplan

   # Show plan summary to user
   echo "Infrastructure changes:"
   terraform show -no-color tfplan | head -50

   # Apply if not --dry-run
   IF not DRY_RUN:
     terraform apply -auto-approve tfplan

     # Save state reference
     terraform output -json > .speckit/state/{ENV}/infra-outputs.json
     echo '{"state_file": "s3://${PROJECT}-tfstate/${ENV}/terraform.tfstate"}' > .speckit/state/{ENV}/infra-state.json
   ```

4. **Extract outputs for deploy stage:**
   ```
   INFRA_OUTPUTS = {
     database_host: terraform output -raw database_host,
     database_port: terraform output -raw database_port,
     redis_host: terraform output -raw redis_host,
     s3_bucket: terraform output -raw s3_bucket,
     k8s_endpoint: terraform output -raw kubernetes_endpoint
   }
   ```

### Phase 2: DEPLOY (Application)

**Optimization:** Apply `templates/shared/ship/deploy-optimizer.md` for Docker layer intelligence, Helm template caching, and adaptive timeouts.

**Skip conditions:**
- `--only infra` or `--only verify` specified
- `--destroy` specified
- Version unchanged AND `--force-deploy` not specified (see deploy-optimizer.md)

**For --env local:**

1. **Generate docker-compose.yml from deploy.yaml:**
   ```yaml
   version: '3.8'
   services:
     # From infra.yaml local resources
     postgres:
       image: postgres:16
       ports: ["5432:5432"]
       environment:
         POSTGRES_DB: app_dev

     # From deploy.yaml local services
     app:
       build: ./backend
       ports: ["8080:8080"]
       depends_on: [postgres]
       environment:
         DATABASE_URL: postgres://postgres@postgres:5432/app_dev
   ```

2. **Run docker-compose:**
   ```bash
   docker-compose -f .speckit/local/docker-compose.yml up -d

   # Save state
   docker-compose ps --format json > .speckit/state/local/docker-state.json
   ```

**For --env staging/production:**

1. **Check if deployment is needed:**
   ```
   deployed_version = read(.speckit/state/{ENV}/deployed-version.json)

   IF deployed_version.git_sha == GIT_SHA:
     log("Version already deployed, skipping")
     GOTO Phase 3
   ```

2. **Build and push container image:**
   ```bash
   IMAGE_TAG="${REGISTRY}/${PROJECT}/app:${GIT_SHA}"

   docker build -t $IMAGE_TAG .
   docker push $IMAGE_TAG
   ```

3. **Deploy with Helm:**
   ```bash
   NAMESPACE="staging-${FEATURE_SLUG}"  # or "production"

   # Create namespace if not exists
   kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

   # Deploy with Helm
   helm upgrade --install app ./helm/app \
     --namespace $NAMESPACE \
     --values helm/values/base.yaml \
     --values helm/values/${ENV}.yaml \
     --set image.tag=${GIT_SHA} \
     --set image.repository=${REGISTRY}/${PROJECT}/app \
     --set ingress.host=${FEATURE_SLUG}.${ENV}.example.com \
     --set database.host=${INFRA_OUTPUTS.database_host} \
     --set redis.host=${INFRA_OUTPUTS.redis_host} \
     --wait --timeout=5m

   # Save deployed version
   echo '{"git_sha": "${GIT_SHA}", "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)", "namespace": "${NAMESPACE}"}' \
     > .speckit/state/{ENV}/deployed-version.json
   ```

4. **Wait for rollout:**
   ```bash
   kubectl rollout status deployment/app -n $NAMESPACE --timeout=5m
   ```

### Phase 3: VERIFY (Running System)

**Optimization:** Apply the following modules for faster verification:
- `templates/shared/ship/test-parallel.md` for parallel test execution
- `templates/shared/ship/browser-pool.md` for browser pool management
- `templates/shared/ship/contract-testing.md` for contract vs E2E strategy
- `templates/shared/ship/incremental-tests.md` for affected-test selection

**Skip conditions:**
- `--skip-verify` specified
- `--only infra` or `--only deploy` specified
- `--destroy` specified

**Pre-execution (during deploy phase at 80% completion):**
```text
# Browser pool pre-warming (see browser-pool.md)
IF NOT --no-browser-pool:
  async_warm_browser_pool(size=4)

# Test data preparation
IF has_test_fixtures:
  async_prepare_test_fixtures()
```

**Execution:**

1. **Determine base URL:**
   ```
   IF ENV == "local":
     BASE_URL = "http://localhost:8080"
   ELSE:
     BASE_URL = "https://${FEATURE_SLUG}.${ENV}.example.com"
   ```

2. **Select test strategy** (see contract-testing.md and incremental-tests.md):
   ```text
   # Determine if full E2E or contract-based testing
   IF --full-e2e:
     test_strategy = "full_e2e"
   ELSE:
     test_strategy = decide_test_strategy()  # From contract-testing.md
     # Returns: "contract" | "e2e" | "hybrid" based on triggers

   # Determine affected tests (incremental selection)
   IF --full-tests:
     tests_to_run = all_tests
   ELSE:
     changed_files = git diff --name-only HEAD~1
     tests_to_run = select_affected_tests(changed_files)  # From incremental-tests.md

     IF tests_to_run.empty:
       LOG "No tests affected by changes, running smoke only"
       tests_to_run = smoke_tests_only
   ```

3. **Run smoke tests (always first, parallel if enabled):**
   ```text
   # Parallel smoke tests (see test-parallel.md)
   smoke_checks = verify.yaml.checks.smoke
   max_workers = --parallel-tests OR 4

   results = parallel_execute(smoke_checks, max_workers, FUNCTION(check):
     result = http_request(check.url, check.method or "GET")

     IF check.expect.status and result.status != check.expect.status:
       RETURN FAIL("expected ${check.expect.status}, got ${result.status}")

     IF check.expect.body.contains and not result.body.contains(check.expect.body.contains):
       RETURN FAIL("body missing '${check.expect.body.contains}'")

     RETURN PASS
   )

   # Fast-fail on smoke failure
   IF any(results.failed):
     LOG "❌ Smoke tests failed, aborting verification"
     TRIGGER_ROLLBACK_PROMPT()  # See smart-rollback.md
     EXIT_FAIL
   ```

4. **Run acceptance tests (linked to AS-xxx):**
   ```text
   results = []
   browser_pool = get_warmed_browser_pool()  # From browser-pool.md pre-warming

   # Filter to affected tests only (incremental selection)
   acceptance_checks = verify.yaml.checks.acceptance
   IF tests_to_run != all_tests:
     acceptance_checks = filter(acceptance_checks, c => c.ref IN tests_to_run)

   # Check test cache (see incremental-tests.md)
   FOR EACH check IN acceptance_checks:
     IF NOT --no-test-cache:
       cache_key = hash(check.script, check.ref, GIT_SHA, ENV)
       cached_result = test_cache.get(cache_key)
       IF cached_result AND cached_result.passed:
         LOG f"✓ {check.ref} (cached)"
         results.append(cached_result)
         CONTINUE

     start_time = now()

     # Execute based on test strategy
     IF test_strategy == "contract" AND check.type == "api":
       # Use contract verification instead of full API test (see contract-testing.md)
       result = verify_api_contract(check.contract_ref)
     ELSE IF check.type == "playwright":
       # Use browser from pool (see browser-pool.md)
       browser_context = browser_pool.acquire()
       result = run_playwright(check.script, browser_context)
       browser_pool.release(browser_context)
     ELSE IF check.type == "api":
       result = run_api_test(check.script)
     ELSE IF check.type == "manual":
       result = prompt_user("Verify: ${check.description}")

     duration = now() - start_time

     test_result = {
       ref: check.ref,
       status: result.passed ? "PASS" : "FAIL",
       duration: duration,
       error: result.error or null
     }
     results.append(test_result)

     # Cache successful results
     IF result.passed AND NOT --no-test-cache:
       test_cache.set(cache_key, test_result, TTL=3600)
   ```

5. **Generate verify-results.md:**
   ```markdown
   # Verification Results

   **Environment**: ${ENV}
   **Timestamp**: ${TIMESTAMP}
   **Git SHA**: ${GIT_SHA}
   **Base URL**: ${BASE_URL}

   ## Summary

   | Category | Total | Passed | Failed |
   |----------|-------|--------|--------|
   | Smoke    | 3     | 3      | 0      |
   | Acceptance | 5   | 4      | 1      |
   | Security | 2     | 2      | 0      |

   **Verdict**: ${all_passed ? "PASS" : "FAIL"}

   ## Detailed Results

   | Scenario | Status | Duration | Error |
   |----------|--------|----------|-------|
   | AS-1A    | PASS   | 1.2s     | -     |
   | AS-1B    | FAIL   | 30.0s    | Timeout connecting to API |
   | AS-2A    | PASS   | 0.8s     | -     |

   ## Failed Scenarios

   ### AS-1B: User can login with valid credentials

   **Error**: Timeout connecting to API after 30s
   **Suggested Action**: Check API pod logs, verify database connectivity
   ```

6. **Update spec.md verification status:**
   ```
   FOR EACH result in results:
     IF result.status == "FAIL":
       # Add verification status to AS-xxx in spec.md
       update_spec_md(result.ref, {
         verification_status: "FAILED",
         last_error: result.error,
         environment: ENV,
         timestamp: TIMESTAMP
       })
   ```

7. **Save verification state:**
   ```bash
   echo '${JSON.stringify(results)}' > .speckit/state/{ENV}/last-verify.json
   ```

8. **Create snapshot on success** (see smart-rollback.md):
   ```text
   IF all_results_passed:
     # Create deployment snapshot for rollback capability
     snapshot = create_snapshot(ENV, {
       version: GIT_SHA,
       infra_state: terraform_state_snapshot(),
       deploy_config: helm_values_snapshot(),
       verification_passed: true
     })
     LOG f"✓ Snapshot created: {snapshot.id}"
     maintain_snapshots(max_count=5)  # Keep last 5 successful snapshots
   ```

9. **Handle verification failure** (see smart-rollback.md):
   ```text
   IF any_results_failed:
     failure_severity = classify_failure(failed_results)
     # CRITICAL: security, data integrity → auto-rollback
     # HIGH: core functionality → prompt rollback
     # MEDIUM: non-critical → warning only
     # LOW: performance → log only

     IF failure_severity == "CRITICAL" OR --auto-rollback:
       LOG "❌ Critical failure detected, initiating rollback"
       last_good_snapshot = get_last_successful_snapshot(ENV)
       IF last_good_snapshot:
         rollback_to(last_good_snapshot)
       ELSE:
         LOG "⚠ No previous snapshot available for rollback"
         EXIT_FAIL

     ELSE IF failure_severity == "HIGH":
       IF NOT --no-rollback:
         response = prompt("Rollback to previous version? (y/n)")
         IF response == "y":
           rollback_to(get_last_successful_snapshot(ENV))
       EXIT_FAIL

     ELSE:
       LOG f"⚠ Verification issues detected (severity: {failure_severity})"
       LOG "Review verify-results.md for details"
   ```

### Phase 4: DESTROY (Teardown)

**Only if `--destroy` specified**

1. **Confirm destruction:**
   ```
   prompt("Are you sure you want to destroy ${ENV} environment? (type 'yes' to confirm)")
   IF response != "yes":
     abort()
   ```

2. **Delete Kubernetes resources:**
   ```bash
   helm uninstall app -n staging-${FEATURE_SLUG}
   kubectl delete namespace staging-${FEATURE_SLUG}
   ```

3. **Destroy Terraform resources (if not shared):**
   ```bash
   # Only destroy feature-specific resources
   # Shared infrastructure (DB, cache) is NOT destroyed
   cd .speckit/terraform/{ENV}
   terraform destroy -auto-approve -target=module.feature_specific
   ```

4. **Clean up state files:**
   ```bash
   rm -f .speckit/state/{ENV}/deployed-version.json
   # Keep infra-state.json if shared infrastructure
   ```

### Phase 5: ROLLBACK (Recovery)

**Only if rollback triggered by verification failure or explicit `--rollback` flag**

**Optimization:** Apply `templates/shared/ship/smart-rollback.md` for intelligent rollback strategies.

1. **Determine rollback type:**
   ```text
   # Automatic determination based on what failed
   IF only_app_failed:
     rollback_type = "app_only"      # Fast: just redeploy previous version
   ELSE IF infra_changed:
     rollback_type = "full"          # Restore infra + app
   ELSE:
     rollback_type = "partial"       # Selective component rollback
   ```

2. **Execute rollback:**
   ```text
   snapshot = get_rollback_target(ENV)

   IF rollback_type == "app_only":
     # Fast rollback using previous image
     helm rollback app -n $NAMESPACE
     OR
     kubectl set image deployment/app app=${snapshot.image_tag}

   ELSE IF rollback_type == "full":
     # Full state restoration
     terraform_restore(snapshot.infra_state)
     helm_restore(snapshot.deploy_config)

   ELSE IF rollback_type == "partial":
     # Selective restoration
     FOR component IN failed_components:
       restore_component(component, snapshot)
   ```

3. **Verify rollback:**
   ```text
   # Run smoke tests to confirm rollback success
   rollback_verify = run_smoke_tests_only()

   IF rollback_verify.passed:
     LOG "✓ Rollback successful, system restored to {snapshot.version}"
   ELSE:
     LOG "❌ Rollback verification failed!"
     ALERT("Manual intervention required for {ENV}")
   ```

4. **Update state:**
   ```bash
   echo '{"git_sha": "${snapshot.version}", "rollback_from": "${GIT_SHA}", "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"}' \
     > .speckit/state/{ENV}/deployed-version.json
   ```

---

## Output Summary

After all phases complete, output a summary:

```markdown
## Ship Complete

**Environment**: staging
**Git SHA**: abc1234
**Namespace**: staging-feature-001

### Stages

| Stage | Status | Duration | Optimization |
|-------|--------|----------|--------------|
| Provision | SKIPPED (fingerprint match) | 0s | Saved ~5 min |
| Deploy | SUCCESS | 45s | Cache hit |
| Verify | SUCCESS | 12s | 8/12 tests cached |

**Total Time**: 57s (vs ~8 min without optimizations)

### Optimizations Applied

| Optimization | Impact |
|-------------|--------|
| Fingerprint skip (provision) | -5 min |
| Docker layer cache | -60s |
| Browser pool pre-warm | -12s |
| Incremental test selection | -45s |
| Test result caching | -30s |
| Contract tests (vs E2E) | -40s |

### Endpoints

- **Application**: https://feature-001.staging.example.com
- **Health**: https://feature-001.staging.example.com/health

### Verification

- Smoke tests: 3/3 passed (parallel, 2.1s)
- Acceptance tests: 5/5 passed (3 cached, 2 executed)
- Contract tests: 8/8 verified (replaced 4 E2E tests)
- Security scans: 2/2 passed

### Snapshot

- **Snapshot ID**: snap-abc1234-20240115
- **Rollback available**: Yes (5 snapshots retained)

**Verdict**: READY FOR REVIEW
```

---

## Self-Review

Before completing, verify:

1. **State Consistency**:
   - [ ] `.speckit/state/{ENV}/` files are up-to-date
   - [ ] Terraform state reference is valid
   - [ ] Deployed version matches current git SHA
   - [ ] Fingerprint cache updated (if provision ran)
   - [ ] Snapshot created (if verification passed)

2. **Verification Coverage**:
   - [ ] All smoke tests passed
   - [ ] Critical AS-xxx scenarios verified
   - [ ] Results linked back to spec.md
   - [ ] Test cache updated with new results

3. **Optimization Resources**:
   - [ ] Browser pool released/cleaned up
   - [ ] Docker build cache pruned (if over threshold)
   - [ ] Test cache pruned (entries over TTL)

4. **Cleanup**:
   - [ ] No orphaned resources
   - [ ] Temporary files removed
   - [ ] Namespace lifecycle documented

5. **Rollback Readiness**:
   - [ ] Snapshot exists for current deployment
   - [ ] Previous snapshot(s) available for rollback
   - [ ] Rollback procedures documented

**If any check fails, report the issue and suggest remediation steps.**

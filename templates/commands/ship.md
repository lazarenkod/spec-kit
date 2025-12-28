---
description: Provision infrastructure, deploy application, and verify running system in one command
persona: devops-agent
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

**Skip conditions:**
- `--only deploy` or `--only verify` specified
- `--env local` (uses docker-compose, no cloud infra)

**Execution:**

1. **Check if infrastructure exists:**
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

**Skip conditions:**
- `--only infra` or `--only verify` specified
- `--destroy` specified

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

**Skip conditions:**
- `--skip-verify` specified
- `--only infra` or `--only deploy` specified
- `--destroy` specified

**Execution:**

1. **Determine base URL:**
   ```
   IF ENV == "local":
     BASE_URL = "http://localhost:8080"
   ELSE:
     BASE_URL = "https://${FEATURE_SLUG}.${ENV}.example.com"
   ```

2. **Run smoke tests (always first):**
   ```
   FOR EACH check in verify.yaml.checks.smoke:
     result = http_request(check.url, check.method or "GET")

     IF check.expect.status and result.status != check.expect.status:
       FAIL("Smoke test failed: expected ${check.expect.status}, got ${result.status}")

     IF check.expect.body.contains and not result.body.contains(check.expect.body.contains):
       FAIL("Smoke test failed: body missing '${check.expect.body.contains}'")

     log("Smoke: ${check.name} PASSED")
   ```

3. **Run acceptance tests (linked to AS-xxx):**
   ```
   results = []

   FOR EACH check in verify.yaml.checks.acceptance:
     start_time = now()

     IF check.type == "playwright":
       result = run_playwright(check.script)
     ELSE IF check.type == "api":
       result = run_api_test(check.script)
     ELSE IF check.type == "manual":
       result = prompt_user("Verify: ${check.description}")

     duration = now() - start_time

     results.append({
       ref: check.ref,
       status: result.passed ? "PASS" : "FAIL",
       duration: duration,
       error: result.error or null
     })
   ```

4. **Generate verify-results.md:**
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

5. **Update spec.md verification status:**
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

6. **Save verification state:**
   ```bash
   echo '${JSON.stringify(results)}' > .speckit/state/{ENV}/last-verify.json
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

---

## Output Summary

After all phases complete, output a summary:

```markdown
## Ship Complete

**Environment**: staging
**Git SHA**: abc1234
**Namespace**: staging-feature-001

### Stages

| Stage | Status | Duration |
|-------|--------|----------|
| Provision | SKIPPED (no changes) | 0s |
| Deploy | SUCCESS | 45s |
| Verify | SUCCESS | 12s |

### Endpoints

- **Application**: https://feature-001.staging.example.com
- **Health**: https://feature-001.staging.example.com/health

### Verification

- Smoke tests: 3/3 passed
- Acceptance tests: 5/5 passed
- Security scans: 2/2 passed

**Verdict**: READY FOR REVIEW
```

---

## Self-Review

Before completing, verify:

1. **State Consistency**:
   - [ ] `.speckit/state/{ENV}/` files are up-to-date
   - [ ] Terraform state reference is valid
   - [ ] Deployed version matches current git SHA

2. **Verification Coverage**:
   - [ ] All smoke tests passed
   - [ ] Critical AS-xxx scenarios verified
   - [ ] Results linked back to spec.md

3. **Cleanup**:
   - [ ] No orphaned resources
   - [ ] Temporary files removed
   - [ ] Namespace lifecycle documented

**If any check fails, report the issue and suggest remediation steps.**

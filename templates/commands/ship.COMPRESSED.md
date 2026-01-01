---
description: Provision infrastructure, deploy application, and verify running system in one command
persona: devops-agent
handoffs:
  - label: Fix Verification Issues
    agent: speckit.implement
    auto: false
    condition: ["verify-results.md shows FAILED scenarios"]
  - label: Analyze Results
    agent: speckit.analyze
    auto: true
    condition: ["All stages completed"]
scripts:
  sh: scripts/bash/ship.sh
  ps: scripts/powershell/ship.ps1
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 6000
  cache_hierarchy: full
---

## Input
```text
$ARGUMENTS
```

---

## Arguments

| Flag | Description | Default |
|------|-------------|---------|
| `--env <environment>` | Target: local, staging, production | staging |
| `--only <stage>` | Run only: infra, deploy, verify | all |
| `--destroy` | Tear down infrastructure | false |
| `--dry-run` | Show plan without executing | false |
| `--cloud <provider>` | Override: vk, yandex, gcp | from infra.yaml |
| `--skip-verify` | Skip verification stage | false |

**Optimization Flags**:
| Flag | Effect |
|------|--------|
| `--turbo` | Max parallelism, skip optional checks |
| `--safe` | Sequential execution, full validation |
| `--skip-provision` | Skip if fingerprint unchanged |
| `--force-deploy` | Force deploy even if version unchanged |
| `--full-e2e` | Full E2E instead of contract tests |
| `--full-tests` | Full suite instead of incremental |
| `--auto-rollback` | Auto-rollback on verification failure |

---

## Wave Overlap Execution

```text
DEFAULT: Speculative execution at 80% completion threshold

provision_start
  AT 80% → deploy_prepare (pull images, warm cache)
provision_complete → deploy_start
  AT 80% → verify_prepare (warm browser pool)
deploy_complete → verify_start
```

| Scenario | Without Opt | With Opt | Savings |
|----------|-------------|----------|---------|
| Clean deploy (staging) | 12 min | 5 min | 58% |
| Small code change | 8 min | 45s | 91% |
| Test re-run | 90s | 20s | 78% |
| Rollback | 5 min | 90s | 70% |

---

## Workflow (5 Phases)

### Phase 0: Setup

```text
1. Run {SCRIPT} --json → FEATURE_DIR, PROJECT_ROOT, ENV, CLOUD
2. Load configs: infra.yaml (REQUIRED), deploy.yaml (REQUIRED), verify.yaml (optional)
3. Load state from .speckit/state/{ENV}/
4. Detect GIT_SHA, GIT_BRANCH, FEATURE_SLUG
```

### Phase 1: PROVISION (Infrastructure)

**Skip If**: `--only deploy|verify`, `--env local`, fingerprint unchanged

```text
1. Fingerprint check: hash(infra.yaml, terraform/*.tf) vs cached
   IF match AND NOT --force-provision → return cached_outputs

2. Check drift: terraform plan -detailed-exitcode
   EXIT_CODE 0 → skip, 2 → apply

3. Generate Terraform from infra.yaml.environments[ENV].resources
   - Map resource.ref (INFRA-xxx) to modules

4. Apply Terraform:
   terraform init -backend-config="..."
   terraform plan -out=tfplan
   IF NOT --dry-run: terraform apply -auto-approve tfplan

5. Extract outputs: database_host, redis_host, k8s_endpoint, etc.
```

### Phase 2: DEPLOY (Application)

**Skip If**: `--only infra|verify`, `--destroy`, version unchanged

**Local** (`--env local`):
```text
Generate docker-compose.yml from deploy.yaml
docker-compose up -d
Save state to .speckit/state/local/docker-state.json
```

**Staging/Production**:
```text
1. Check version: IF deployed_sha == GIT_SHA → skip

2. Build and push:
   docker build -t ${REGISTRY}/${PROJECT}/app:${GIT_SHA} .
   docker push

3. Deploy with Helm:
   NAMESPACE="staging-${FEATURE_SLUG}" or "production"
   helm upgrade --install app ./helm/app \
     --namespace $NAMESPACE \
     --values helm/values/{ENV}.yaml \
     --set image.tag=${GIT_SHA} \
     --wait --timeout=5m

4. Save deployed version to .speckit/state/{ENV}/deployed-version.json
```

### Phase 3: VERIFY (Running System)

**Skip If**: `--skip-verify`, `--only infra|deploy`, `--destroy`

```text
1. Determine BASE_URL:
   local → http://localhost:8080
   else → https://${FEATURE_SLUG}.${ENV}.example.com

2. Select test strategy:
   --full-e2e → full_e2e
   else → decide_test_strategy() → contract | e2e | hybrid

3. Incremental test selection:
   --full-tests → all_tests
   else → select_affected_tests(git diff --name-only HEAD~1)

4. Run smoke tests (parallel, fast-fail):
   IF any_failed → TRIGGER_ROLLBACK_PROMPT, EXIT_FAIL

5. Run acceptance tests:
   FOR EACH check in verify.yaml.checks.acceptance:
     - Check cache (skip if cached + passed)
     - Execute: contract | playwright | api | manual
     - Cache successful results (TTL=3600)

6. Generate verify-results.md:
   - Environment, timestamp, git SHA
   - Summary table: Category | Total | Passed | Failed
   - Detailed results with duration and errors
   - Verdict: PASS | FAIL

7. Create snapshot on success:
   snapshot = {version, infra_state, deploy_config}
   maintain_snapshots(max_count=5)

8. Handle failure (see Rollback Severity):
   CRITICAL → auto-rollback
   HIGH → prompt rollback
   MEDIUM → warning only
   LOW → log only
```

### Phase 4: DESTROY (Teardown)

**Only If**: `--destroy` specified

```text
1. Confirm: prompt("type 'yes' to confirm")
2. helm uninstall app -n $NAMESPACE
3. kubectl delete namespace $NAMESPACE
4. terraform destroy -target=module.feature_specific (NOT shared infra)
5. Clean up state files (keep infra-state.json if shared)
```

### Phase 5: ROLLBACK (Recovery)

**Triggered By**: Verification failure or `--rollback` flag

| Rollback Type | When | Action |
|---------------|------|--------|
| app_only | Only app failed | `helm rollback` or set previous image |
| full | Infra changed | Restore infra state + deploy config |
| partial | Selective | Restore failed components only |

```text
1. Determine type based on what failed
2. Execute rollback from snapshot
3. Run smoke tests to verify rollback
4. Update deployed-version.json with rollback info
```

**Rollback Severity Classification**:
| Severity | Triggers | Action |
|----------|----------|--------|
| CRITICAL | Security, data integrity | Auto-rollback |
| HIGH | Core functionality | Prompt rollback |
| MEDIUM | Non-critical | Warning only |
| LOW | Performance | Log only |

---

## Self-Review Phase [REF:SR-001]

### Quality Criteria

| ID | Check | Severity |
|----|-------|----------|
| SR-SHIP-01 | `.speckit/state/{ENV}/` files up-to-date | CRITICAL |
| SR-SHIP-02 | Terraform state reference valid | CRITICAL |
| SR-SHIP-03 | Deployed version matches GIT_SHA | HIGH |
| SR-SHIP-04 | Fingerprint cache updated | MEDIUM |
| SR-SHIP-05 | All smoke tests passed | CRITICAL |
| SR-SHIP-06 | Critical AS-xxx verified | HIGH |
| SR-SHIP-07 | Results linked to spec.md | MEDIUM |
| SR-SHIP-08 | Test cache updated | LOW |
| SR-SHIP-09 | Browser pool released | MEDIUM |
| SR-SHIP-10 | Snapshot exists for deployment | HIGH |
| SR-SHIP-11 | Rollback procedures documented | MEDIUM |

---

## Quality Gates

| Gate | Check | Block Condition |
|------|-------|-----------------|
| Implementation Exists | Source code exists | No source files found |
| Ship Config Exists | infra.yaml OR deploy.yaml exists | No configuration |
| Deployment Success | Deploy stage completed | Deploy failed |
| Verification Passed | All critical tests pass | Critical failures |

---

## Output Format

```text
┌─────────────────────────────────────────────────────────────┐
│ /speckit.ship Complete                                       │
├─────────────────────────────────────────────────────────────┤
│ Environment: {ENV}                                           │
│ Git SHA: {sha}                                               │
│ Namespace: {namespace}                                       │
│                                                              │
│ Stages:                                                      │
│   Provision: {status} ({duration}) {optimization}            │
│   Deploy: {status} ({duration}) {optimization}               │
│   Verify: {status} ({duration}) {optimization}               │
│                                                              │
│ Total Time: {time} (vs {baseline} without optimizations)    │
│                                                              │
│ Verification:                                                │
│   Smoke: {pass}/{total}  Acceptance: {pass}/{total}         │
│   Cached: {count}  Contract: {count}                         │
│                                                              │
│ Snapshot: {id} (Rollback available: {yes|no})               │
│ Verdict: {READY FOR REVIEW | FAILED | ROLLED BACK}          │
└─────────────────────────────────────────────────────────────┘
```

---

## Context

{ARGS}

# Smart Rollback Strategy

## Purpose

Implement intelligent rollback capabilities with snapshot management, partial rollback support, and automatic recovery decisions based on failure severity and component criticality.

## Performance Impact

| Rollback Type | Time | Data Loss Risk |
|---------------|------|----------------|
| Full rollback | 3-5 min | Low |
| Partial rollback | 1-2 min | Very Low |
| Instant rollback | 10-30s | None |

## Configuration

```yaml
optimization:
  rollback:
    enabled: true
    skip_flag: "--no-auto-rollback"
    auto_on_failure: false        # Prompt user by default
    snapshot_count: 5             # Keep last 5 snapshots
    partial_enabled: true         # Allow component-level rollback
    instant_rollback: true        # Use blue-green when available
    preserve_data_migrations: true
```

## Snapshot Management

```text
SNAPSHOT_STRUCTURE:
  directory: ".speckit/snapshots/{ENV}/"
  files:
    - snapshot-{timestamp}.json     # Full state
    - terraform-{timestamp}.tfstate # Infra state
    - helm-{timestamp}.yaml         # Deploy values
    - config-{timestamp}.json       # App config

  metadata:
    - version
    - git_sha
    - timestamp
    - components_deployed
    - verification_status
    - rollback_safe              # Can we safely rollback to this?


FUNCTION create_snapshot(environment, deployment_result):
  timestamp = now().isoformat()

  snapshot = {
    id: f"snapshot-{timestamp}",
    environment: environment,
    timestamp: timestamp,
    version: deployment_result.version,
    git_sha: get_current_commit(),

    # Component states
    components: {},

    # Infrastructure state
    terraform_state: None,

    # Verification status
    verification: {
      smoke: deployment_result.smoke_passed,
      acceptance: deployment_result.acceptance_passed,
      security: deployment_result.security_passed,
      performance: deployment_result.performance_passed
    },

    # Metadata
    rollback_safe: True,
    created_by: get_current_user(),
    notes: []
  }

  # Capture component states
  FOR component IN deployment_result.components:
    snapshot.components[component.name] = {
      version: component.version,
      image: component.image,
      replicas: component.replicas,
      config_hash: component.config_hash,
      healthy: component.healthy
    }

  # Capture Terraform state
  IF terraform_managed():
    snapshot.terraform_state = terraform_state_snapshot()

  # Capture Helm values
  IF helm_managed():
    snapshot.helm_values = helm_values_snapshot()

  # Save snapshot
  save_snapshot(snapshot)

  # Maintain snapshot count
  cleanup_old_snapshots(max_count=config.snapshot_count)

  LOG f"✓ Snapshot created: {snapshot.id}"
  RETURN snapshot


FUNCTION save_snapshot(snapshot):
  dir = f".speckit/snapshots/{snapshot.environment}/"
  mkdir -p $dir

  # Save main snapshot
  json.dump(f"{dir}/{snapshot.id}.json", snapshot)

  # Save terraform state separately (large file)
  IF snapshot.terraform_state:
    write_file(f"{dir}/terraform-{snapshot.timestamp}.tfstate", snapshot.terraform_state)

  # Update latest pointer
  json.dump(f"{dir}/latest.json", {
    snapshot_id: snapshot.id,
    version: snapshot.version,
    timestamp: snapshot.timestamp
  })


FUNCTION cleanup_old_snapshots(max_count):
  snapshots = list_snapshots()
  IF len(snapshots) <= max_count:
    RETURN

  # Sort by timestamp (oldest first)
  snapshots.sort(key=lambda s: s.timestamp)

  # Remove oldest
  to_remove = snapshots[:-max_count]
  FOR snapshot IN to_remove:
    remove_snapshot(snapshot.id)
    LOG f"Removed old snapshot: {snapshot.id}"
```

## Rollback Decision Engine

```text
ROLLBACK_DECISION_MATRIX:

  FAILURE_SEVERITY:
    CRITICAL:
      - smoke_tests_failed
      - health_check_failed
      - security_vulnerability_detected
      action: IMMEDIATE_ROLLBACK

    HIGH:
      - acceptance_tests_failed
      - error_rate_spike
      - latency_degradation
      action: PROMPT_ROLLBACK

    MEDIUM:
      - performance_regression
      - non_critical_test_failed
      action: LOG_WARNING

    LOW:
      - cosmetic_issues
      - documentation_mismatch
      action: LOG_INFO


FUNCTION decide_rollback_action(failure_context):
  severity = classify_failure_severity(failure_context)
  component = failure_context.failed_component

  LOG f"Failure detected: {failure_context.type} (severity: {severity})"

  # Check auto-rollback setting
  IF config.auto_on_failure AND severity IN [CRITICAL, HIGH]:
    LOG "Auto-rollback enabled, initiating rollback"
    RETURN RollbackDecision(
      action="rollback",
      type="automatic",
      target=determine_rollback_target(component, severity)
    )

  # Check if partial rollback is possible
  IF config.partial_enabled AND can_partial_rollback(component):
    LOG f"Partial rollback available for {component}"
    RETURN RollbackDecision(
      action="prompt",
      options=["full_rollback", "partial_rollback", "skip"],
      recommended="partial_rollback",
      target=component
    )

  # Default: prompt user
  RETURN RollbackDecision(
    action="prompt",
    options=["rollback", "skip", "investigate"],
    recommended="rollback" IF severity == CRITICAL ELSE "investigate"
  )


FUNCTION classify_failure_severity(context):
  # Check test failures
  IF context.smoke_failed:
    RETURN CRITICAL

  IF context.security_failed:
    RETURN CRITICAL

  IF context.health_check_failed:
    RETURN CRITICAL

  IF context.acceptance_failed:
    RETURN HIGH

  IF context.performance_failed:
    RETURN MEDIUM

  RETURN LOW


FUNCTION determine_rollback_target(component, severity):
  IF severity == CRITICAL:
    # Critical failures require full rollback
    RETURN RollbackTarget(type="full", components="all")

  IF component IN ["app", "gateway"]:
    # Core components affect everything
    RETURN RollbackTarget(type="full", components="all")

  # Isolated component
  RETURN RollbackTarget(type="partial", components=[component])
```

## Full Rollback

```text
FUNCTION full_rollback(environment, target_snapshot=None):
  LOG "🔄 Initiating full rollback"

  # 1. Get target snapshot
  IF target_snapshot IS None:
    target_snapshot = get_last_successful_snapshot(environment)

  IF target_snapshot IS None:
    RAISE RollbackError("No successful snapshot available")

  LOG f"Rolling back to: {target_snapshot.id} (v{target_snapshot.version})"

  # 2. Pre-rollback checks
  pre_checks = perform_pre_rollback_checks(target_snapshot)
  IF NOT pre_checks.passed:
    LOG f"⚠ Pre-rollback checks failed: {pre_checks.errors}"
    IF NOT force:
      RAISE RollbackError(pre_checks.errors)

  # 3. Rollback infrastructure (if needed)
  IF target_snapshot.terraform_state:
    LOG "Rolling back Terraform state..."
    rollback_terraform(target_snapshot.terraform_state)

  # 4. Rollback deployments
  FOR component_name, component_state IN target_snapshot.components:
    LOG f"Rolling back {component_name} to {component_state.version}..."
    rollback_component(component_name, component_state)

  # 5. Wait for stability
  LOG "Waiting for services to stabilize..."
  wait_for_healthy(timeout=120)

  # 6. Verify rollback
  LOG "Verifying rollback..."
  verification = run_smoke_tests()

  IF NOT verification.passed:
    LOG "⚠ Rollback verification failed!"
    RETURN RollbackResult(success=False, verification=verification)

  # 7. Update state
  update_deployed_version(environment, target_snapshot.version)

  LOG f"✓ Rollback complete to {target_snapshot.version}"
  RETURN RollbackResult(success=True, snapshot=target_snapshot)


FUNCTION rollback_terraform(state_snapshot):
  # Write state to file
  write_file("terraform.tfstate.rollback", state_snapshot)

  # Import state
  terraform state push terraform.tfstate.rollback

  # Apply to ensure consistency
  terraform apply -auto-approve -refresh-only


FUNCTION rollback_component(name, state):
  IF helm_managed():
    # Rollback via Helm
    helm rollback $name --version={state.helm_revision}
  ELSE:
    # Direct kubectl rollback
    kubectl set image deployment/$name \
      $name={state.image}

    kubectl scale deployment/$name \
      --replicas={state.replicas}

  # Wait for rollout
  kubectl rollout status deployment/$name --timeout=120s
```

## Partial Rollback

```text
FUNCTION partial_rollback(environment, component, target_snapshot=None):
  LOG f"🔄 Initiating partial rollback for {component}"

  # 1. Validate partial rollback is safe
  IF NOT can_partial_rollback(component):
    LOG f"⚠ Partial rollback not safe for {component}, dependencies may break"
    RAISE RollbackError(f"Cannot partially rollback {component}")

  # 2. Get target state
  IF target_snapshot IS None:
    target_snapshot = get_last_successful_snapshot(environment)

  component_state = target_snapshot.components.get(component)
  IF NOT component_state:
    RAISE RollbackError(f"Component {component} not found in snapshot")

  # 3. Rollback only this component
  LOG f"Rolling back {component}: {current_version} → {component_state.version}"
  rollback_component(component, component_state)

  # 4. Check compatibility with other components
  compatibility = check_component_compatibility(component, component_state.version)
  IF NOT compatibility.ok:
    LOG f"⚠ Compatibility issues: {compatibility.warnings}"

  # 5. Verify affected endpoints
  affected_tests = get_component_tests(component)
  verification = run_tests(affected_tests)

  IF NOT verification.passed:
    LOG "⚠ Partial rollback verification failed"
    RETURN PartialRollbackResult(
      success=False,
      component=component,
      verification=verification,
      suggestion="Consider full rollback"
    )

  LOG f"✓ Partial rollback complete for {component}"
  RETURN PartialRollbackResult(success=True, component=component)


FUNCTION can_partial_rollback(component):
  # Check if component can be rolled back independently

  # Core components cannot be partially rolled back
  core_components = ["app", "gateway", "database"]
  IF component IN core_components:
    RETURN False

  # Check for breaking API changes
  current_version = get_deployed_version(component)
  previous_version = get_previous_version(component)

  IF has_breaking_changes(component, previous_version, current_version):
    RETURN False

  # Check dependencies
  dependents = get_component_dependents(component)
  FOR dependent IN dependents:
    IF NOT is_backward_compatible(component, dependent):
      RETURN False

  RETURN True
```

## Instant Rollback (Blue-Green)

```text
INSTANT_ROLLBACK:
  description: "Zero-downtime rollback using traffic switching"
  requirements:
    - Blue-green or canary deployment
    - Load balancer with traffic splitting
    - Both versions running simultaneously

  FUNCTION instant_rollback(environment):
    LOG "⚡ Initiating instant rollback"

    # Check if blue-green is available
    IF NOT blue_green_enabled():
      LOG "Blue-green not available, falling back to standard rollback"
      RETURN full_rollback(environment)

    # Get current traffic state
    current = get_traffic_state()
    LOG f"Current: {current.active_version} (100% traffic)"

    # Switch traffic to previous version
    previous_version = current.inactive_version
    IF NOT is_healthy(previous_version):
      RAISE RollbackError(f"Previous version {previous_version} not healthy")

    # Execute traffic switch
    LOG f"Switching traffic: {current.active_version} → {previous_version}"
    switch_traffic(
      from_version=current.active_version,
      to_version=previous_version,
      strategy="instant"  # or "gradual"
    )

    # Verify switch
    new_state = get_traffic_state()
    IF new_state.active_version != previous_version:
      RAISE RollbackError("Traffic switch failed")

    LOG f"✓ Instant rollback complete ({elapsed}ms)"
    RETURN InstantRollbackResult(
      success=True,
      previous_version=current.active_version,
      current_version=previous_version,
      switch_time=elapsed
    )


  FUNCTION switch_traffic(from_version, to_version, strategy):
    IF strategy == "instant":
      # 100% switch immediately
      update_load_balancer(to_version, weight=100)
      update_load_balancer(from_version, weight=0)

    ELIF strategy == "gradual":
      # Gradual shift over 30 seconds
      FOR weight IN [25, 50, 75, 100]:
        update_load_balancer(to_version, weight=weight)
        update_load_balancer(from_version, weight=100-weight)
        sleep(10)
        IF NOT health_check_passing(to_version):
          # Abort and restore
          update_load_balancer(from_version, weight=100)
          RAISE RollbackError("Health check failed during gradual switch")
```

## Data Migration Safety

```text
DATA_MIGRATION_SAFETY:

  FUNCTION check_migration_rollback_safety(current_version, target_version):
    # Get migrations between versions
    migrations = get_migrations_between(target_version, current_version)

    safety = {
      safe: True,
      warnings: [],
      blockers: []
    }

    FOR migration IN migrations:
      # Check if migration is reversible
      IF NOT migration.has_down_migration:
        safety.blockers.append(f"Migration {migration.id} has no down migration")
        safety.safe = False

      # Check for destructive operations
      IF migration.is_destructive:
        safety.blockers.append(f"Migration {migration.id} is destructive")
        safety.safe = False

      # Check for data loss
      IF migration.may_lose_data:
        safety.warnings.append(f"Migration {migration.id} may cause data loss")

    RETURN safety


  FUNCTION rollback_with_migrations(environment, target_snapshot):
    # Check migration safety first
    safety = check_migration_rollback_safety(
      current_version=get_deployed_version(environment),
      target_version=target_snapshot.version
    )

    IF NOT safety.safe:
      LOG "⚠ Migration rollback blocked:"
      FOR blocker IN safety.blockers:
        LOG f"  - {blocker}"
      RAISE RollbackError("Cannot rollback due to migration safety")

    IF safety.warnings:
      LOG "⚠ Migration rollback warnings:"
      FOR warning IN safety.warnings:
        LOG f"  - {warning}"

      IF NOT config.preserve_data_migrations:
        LOG "Proceeding despite warnings (preserve_data_migrations=false)"
      ELSE:
        RAISE RollbackError("Migration warnings with preserve_data_migrations=true")

    # Execute migration rollback
    LOG "Rolling back database migrations..."
    run_migration_down(target_version)

    # Then rollback application
    RETURN full_rollback(environment, target_snapshot)
```

## Integration with ship.md

```text
# At the end of ship execution:
Read `templates/shared/ship/smart-rollback.md` and apply.

# After successful deploy:
IF deployment_successful:
  create_snapshot(environment, deployment_result)

# On failure:
IF verification_failed:
  decision = decide_rollback_action(failure_context)

  IF decision.action == "rollback":
    IF decision.type == "partial":
      result = partial_rollback(environment, decision.target)
    ELSE:
      result = full_rollback(environment)

    IF NOT result.success:
      ALERT_TEAM("Rollback failed, manual intervention required")
```

## Output Format

```text
🔄 Smart Rollback
├── Trigger: smoke_tests_failed
├── Severity: CRITICAL
├── Decision: automatic_rollback
├── Target Snapshot:
│   ├── ID: snapshot-2024-01-15T10:30:00
│   ├── Version: v1.2.3
│   ├── Age: 2h 15m
│   └── Verification: ✓ all passed
├── Pre-checks:
│   ├── Migration safety: ✓ safe
│   ├── State consistency: ✓ ok
│   └── Dependencies: ✓ compatible
├── Rollback Execution:
│   ├── Infrastructure: skipped (unchanged)
│   ├── api-server: v1.2.4 → v1.2.3 (32s)
│   ├── worker: v1.2.4 → v1.2.3 (28s)
│   └── Total: 60s
├── Verification:
│   ├── Health checks: ✓ passing
│   ├── Smoke tests: ✓ 5/5 passed
│   └── Duration: 12s
├── Timing:
│   ├── Decision: 0.5s
│   ├── Pre-checks: 3.2s
│   ├── Rollback: 60s
│   └── Verification: 12s
└── Result: ROLLBACK SUCCESS ✓
```

## CLI Flags

```bash
# Enable auto-rollback
speckit ship --auto-rollback

# Disable all rollback
speckit ship --no-rollback

# Rollback to specific snapshot
speckit ship --rollback-to=snapshot-2024-01-15

# List available snapshots
speckit ship --list-snapshots

# Force rollback (ignore warnings)
speckit ship --force-rollback

# Partial rollback specific component
speckit ship --rollback-component=worker
```

## Rollback Alerts

```text
ALERT_CONFIGURATION:

  ON_ROLLBACK_INITIATED:
    channels: [slack, pagerduty]
    message: |
      🔄 Rollback initiated in {environment}
      Reason: {failure_reason}
      Target: {target_version}
      Triggered by: {trigger}

  ON_ROLLBACK_COMPLETE:
    channels: [slack]
    message: |
      ✓ Rollback complete in {environment}
      Version: {new_version}
      Duration: {duration}
      Verification: {verification_status}

  ON_ROLLBACK_FAILED:
    channels: [slack, pagerduty]
    severity: critical
    message: |
      ⚠️ ROLLBACK FAILED in {environment}
      Error: {error}
      Manual intervention required
      Runbook: {runbook_url}


FUNCTION send_rollback_alert(event_type, context):
  config = ALERT_CONFIGURATION[event_type]

  FOR channel IN config.channels:
    message = format_message(config.message, context)
    send_to_channel(channel, message, severity=config.severity)
```

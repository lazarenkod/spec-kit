# DAG-based Dependency Management

## Purpose

Implement intelligent dependency resolution using a Directed Acyclic Graph (DAG) to enable parallel execution, lazy loading, and minimal provisioning based on actual requirements.

## Performance Impact

| Mode | Time | Savings |
|------|------|---------|
| Full provision | 5-15 min | baseline |
| DAG-optimized | 2-5 min | 60-70% |
| Lazy resolution | 30s-2 min | 85-95% |

## Configuration

```yaml
optimization:
  dependencies:
    enabled: true
    skip_flag: "--eager-deps"
    resolution: lazy          # eager | lazy | on-demand
    skip_optional: true
    parallel_resolution: true
    max_parallel: 4
    soft_dep_timeout: 30      # seconds before using fallback
```

## DAG Structure

```text
NODE_TYPES:
  INFRA:
    - database
    - cache
    - storage
    - networking
    - secrets
    - monitoring

  DEPLOY:
    - app
    - worker
    - scheduler
    - gateway

  VERIFY:
    - smoke
    - acceptance
    - security
    - performance


EDGE_TYPES:
  HARD:
    description: "Must complete before dependent starts"
    behavior: BLOCK_UNTIL_COMPLETE
    on_failure: FAIL_DEPENDENT

  SOFT:
    description: "Should complete, but can proceed with fallback"
    behavior: WAIT_WITH_TIMEOUT
    timeout: 30s
    on_timeout: USE_FALLBACK
    on_failure: USE_FALLBACK

  OPTIONAL:
    description: "Nice to have, skip if slow or unavailable"
    behavior: BEST_EFFORT
    timeout: 10s
    on_timeout: SKIP
    on_failure: SKIP

  LAZY:
    description: "Resolve only when accessed"
    behavior: DEFER_UNTIL_ACCESS
    on_failure: FAIL_ON_ACCESS
```

## DAG Definition

```text
DEFAULT_DEPENDENCY_DAG = {
  nodes: {
    # Infrastructure nodes
    networking: {type: INFRA, provision_time: "30s"},
    database: {type: INFRA, provision_time: "60-120s"},
    cache: {type: INFRA, provision_time: "30s"},
    storage: {type: INFRA, provision_time: "45s"},
    secrets: {type: INFRA, provision_time: "10s"},
    monitoring: {type: INFRA, provision_time: "30s"},

    # Deploy nodes
    app: {type: DEPLOY, deploy_time: "60-120s"},
    worker: {type: DEPLOY, deploy_time: "60s"},
    scheduler: {type: DEPLOY, deploy_time: "30s"},
    gateway: {type: DEPLOY, deploy_time: "30s"},

    # Verify nodes
    smoke: {type: VERIFY, run_time: "10-30s"},
    acceptance: {type: VERIFY, run_time: "30-60s"},
    security: {type: VERIFY, run_time: "30-60s"},
    performance: {type: VERIFY, run_time: "60-180s"}
  },

  edges: [
    # Infrastructure dependencies
    {from: networking, to: database, type: HARD},
    {from: networking, to: cache, type: HARD},
    {from: secrets, to: database, type: HARD},
    {from: secrets, to: app, type: HARD},

    # Deploy dependencies
    {from: database, to: app, type: HARD},
    {from: cache, to: app, type: SOFT, fallback: "local_cache"},
    {from: storage, to: app, type: SOFT, fallback: "local_storage"},
    {from: monitoring, to: app, type: OPTIONAL},

    {from: app, to: worker, type: HARD},
    {from: app, to: scheduler, type: HARD},
    {from: app, to: gateway, type: HARD},

    # Verify dependencies
    {from: app, to: smoke, type: HARD},
    {from: smoke, to: acceptance, type: HARD},
    {from: acceptance, to: security, type: SOFT},
    {from: acceptance, to: performance, type: LAZY}
  ]
}
```

## DAG Construction

```text
FUNCTION build_dependency_dag(config, environment):
  dag = DirectedAcyclicGraph()

  # 1. Load base DAG
  base_dag = load_yaml("ship.yaml").dependencies.dag OR DEFAULT_DEPENDENCY_DAG

  # 2. Add nodes
  FOR node_name, node_config IN base_dag.nodes:
    dag.add_node(DependencyNode(
      name=node_name,
      type=node_config.type,
      config=node_config
    ))

  # 3. Add edges
  FOR edge IN base_dag.edges:
    dag.add_edge(DependencyEdge(
      source=edge.from,
      target=edge.to,
      type=edge.type,
      fallback=edge.fallback IF exists ELSE None,
      timeout=edge.timeout IF exists ELSE default_timeout(edge.type)
    ))

  # 4. Validate DAG (no cycles)
  IF dag.has_cycle():
    cycles = dag.find_cycles()
    RAISE ConfigError(f"Dependency cycle detected: {cycles}")

  # 5. Apply environment overrides
  env_overrides = config.environments[environment].dependency_overrides
  IF env_overrides:
    apply_overrides(dag, env_overrides)

  LOG f"DAG built: {len(dag.nodes)} nodes, {len(dag.edges)} edges"
  RETURN dag


FUNCTION apply_overrides(dag, overrides):
  FOR override IN overrides:
    IF override.action == "skip":
      dag.mark_skipped(override.node)
    ELIF override.action == "promote":
      # Change SOFT/OPTIONAL to HARD
      dag.change_edge_type(override.from, override.to, HARD)
    ELIF override.action == "demote":
      # Change HARD to SOFT/OPTIONAL
      dag.change_edge_type(override.from, override.to, override.new_type)
```

## Topological Execution

```text
FUNCTION execute_dag(dag, target_node=None):
  # 1. Determine execution scope
  IF target_node:
    # Only execute nodes required for target
    required_nodes = dag.ancestors(target_node) + [target_node]
  ELSE:
    required_nodes = dag.all_nodes()

  # 2. Topological sort for execution order
  execution_order = dag.topological_sort(required_nodes)

  # 3. Group by level for parallel execution
  levels = dag.group_by_level(execution_order)
  LOG f"Execution plan: {len(levels)} levels"

  # 4. Execute level by level
  results = {}
  FOR level_idx, level_nodes IN enumerate(levels):
    LOG f"Level {level_idx + 1}: {[n.name FOR n IN level_nodes]}"

    # Filter out skipped nodes
    active_nodes = [n FOR n IN level_nodes IF NOT n.skipped]

    # Execute level in parallel
    level_results = parallel_execute_level(active_nodes, dag, results)
    results.update(level_results)

    # Check for failures
    failures = [r FOR r IN level_results.values() IF r.failed AND r.edge_type == HARD]
    IF failures:
      LOG f"✗ Hard dependency failed: {[f.node FOR f IN failures]}"
      RETURN ExecutionResult(success=False, results=results, failures=failures)

  RETURN ExecutionResult(success=True, results=results)


FUNCTION parallel_execute_level(nodes, dag, previous_results):
  futures = {}

  FOR node IN nodes:
    # Check if dependencies satisfied
    deps_satisfied, fallbacks_used = check_dependencies(node, dag, previous_results)

    IF NOT deps_satisfied:
      futures[node.name] = DeferredResult(status="blocked")
      CONTINUE

    # Execute node
    future = async_execute_node(node, fallbacks_used)
    futures[node.name] = future

  # Wait for all
  results = {}
  FOR node_name, future IN futures:
    IF isinstance(future, DeferredResult):
      results[node_name] = future
    ELSE:
      results[node_name] = await future

  RETURN results
```

## Lazy Resolution

```text
LAZY_RESOLUTION_STATE = {
  resolved: {},      # Already resolved dependencies
  pending: {},       # Currently resolving
  deferred: set()    # Marked for lazy resolution
}


FUNCTION resolve_lazy(dependency_name):
  # Check if already resolved
  IF dependency_name IN LAZY_RESOLUTION_STATE.resolved:
    RETURN LAZY_RESOLUTION_STATE.resolved[dependency_name]

  # Check if currently resolving (prevent cycles)
  IF dependency_name IN LAZY_RESOLUTION_STATE.pending:
    LOG f"Waiting for {dependency_name} (already resolving)"
    RETURN await LAZY_RESOLUTION_STATE.pending[dependency_name]

  # Start resolution
  LOG f"Lazy resolving: {dependency_name}"
  promise = async_resolve(dependency_name)
  LAZY_RESOLUTION_STATE.pending[dependency_name] = promise

  TRY:
    result = await promise
    LAZY_RESOLUTION_STATE.resolved[dependency_name] = result
    RETURN result
  FINALLY:
    del LAZY_RESOLUTION_STATE.pending[dependency_name]


FUNCTION async_resolve(dependency_name):
  node = dag.get_node(dependency_name)

  # First resolve this node's dependencies
  FOR dep IN dag.get_dependencies(node):
    IF dep.edge_type == LAZY:
      await resolve_lazy(dep.source.name)
    ELIF dep.source.name NOT IN LAZY_RESOLUTION_STATE.resolved:
      # Hard/Soft dep not resolved - this shouldn't happen
      RAISE DependencyError(f"Non-lazy dependency {dep.source.name} not resolved")

  # Execute node
  result = await execute_node(node)
  RETURN result
```

## Environment-Specific DAG

```text
ENVIRONMENT_DAG_PROFILES = {

  local: {
    skip_nodes: [monitoring, performance],
    demote_edges: [
      {from: database, to: app, new_type: SOFT, fallback: "docker_postgres"},
      {from: cache, to: app, new_type: SOFT, fallback: "docker_redis"}
    ],
    max_parallel: 2
  },

  staging: {
    skip_nodes: [performance],
    demote_edges: [
      {from: monitoring, to: app, new_type: OPTIONAL}
    ],
    max_parallel: 4
  },

  production: {
    promote_edges: [
      {from: cache, to: app, new_type: HARD},  # Cache required in prod
      {from: monitoring, to: app, new_type: HARD}  # Monitoring required
    ],
    max_parallel: 4,
    require_all_hard: true
  }
}


FUNCTION get_environment_dag(base_dag, environment):
  profile = ENVIRONMENT_DAG_PROFILES.get(environment, {})

  dag = copy(base_dag)

  # Skip nodes
  FOR node_name IN profile.skip_nodes:
    dag.mark_skipped(node_name)
    LOG f"Skipping {node_name} for {environment}"

  # Demote edges
  FOR demote IN profile.demote_edges:
    dag.change_edge_type(demote.from, demote.to, demote.new_type)
    IF demote.fallback:
      dag.set_fallback(demote.from, demote.to, demote.fallback)
    LOG f"Demoted {demote.from} → {demote.to} to {demote.new_type}"

  # Promote edges
  FOR promote IN profile.promote_edges:
    dag.change_edge_type(promote.from, promote.to, promote.new_type)
    LOG f"Promoted {promote.from} → {promote.to} to {promote.new_type}"

  RETURN dag
```

## Change Impact Analysis

```text
FUNCTION analyze_change_impact(changed_files, dag):
  impact = {
    affected_nodes: set(),
    skip_provision: False,
    skip_deploy: False,
    minimal_path: []
  }

  # Map files to nodes
  FILE_TO_NODE_MAP = {
    "infra/*.tf": ["networking", "database", "cache", "storage"],
    "infra/monitoring/*": ["monitoring"],
    "src/**": ["app"],
    "workers/**": ["worker"],
    "helm/**": ["app", "worker", "scheduler", "gateway"],
    "tests/smoke/**": ["smoke"],
    "tests/e2e/**": ["acceptance"],
    "tests/security/**": ["security"],
    "tests/perf/**": ["performance"]
  }

  # Find affected nodes
  FOR file IN changed_files:
    FOR pattern, nodes IN FILE_TO_NODE_MAP:
      IF fnmatch(file, pattern):
        impact.affected_nodes.update(nodes)

  # Calculate transitive impact
  FOR node IN list(impact.affected_nodes):
    dependents = dag.descendants(node)
    impact.affected_nodes.update(dependents)

  # Determine skip flags
  infra_nodes = {"networking", "database", "cache", "storage", "secrets", "monitoring"}
  deploy_nodes = {"app", "worker", "scheduler", "gateway"}

  impact.skip_provision = impact.affected_nodes.isdisjoint(infra_nodes)
  impact.skip_deploy = impact.affected_nodes.isdisjoint(deploy_nodes)

  # Calculate minimal execution path
  IF impact.affected_nodes:
    impact.minimal_path = dag.minimal_subgraph(impact.affected_nodes)

  LOG f"Impact analysis: {len(impact.affected_nodes)} nodes affected"
  LOG f"Skip provision: {impact.skip_provision}, Skip deploy: {impact.skip_deploy}"

  RETURN impact
```

## Fallback Resolution

```text
FALLBACK_REGISTRY = {
  local_cache: {
    type: "docker",
    image: "redis:7-alpine",
    startup_time: "5s",
    config: {port: 6379}
  },
  local_storage: {
    type: "local_fs",
    path: "/tmp/speckit-storage",
    startup_time: "instant"
  },
  docker_postgres: {
    type: "docker",
    image: "postgres:16-alpine",
    startup_time: "10s",
    config: {port: 5432, user: "dev", password: "dev"}
  }
}


FUNCTION resolve_fallback(fallback_name, original_node):
  fallback_config = FALLBACK_REGISTRY.get(fallback_name)

  IF NOT fallback_config:
    RAISE ConfigError(f"Unknown fallback: {fallback_name}")

  LOG f"Using fallback {fallback_name} for {original_node.name}"

  IF fallback_config.type == "docker":
    RETURN start_docker_fallback(fallback_config)
  ELIF fallback_config.type == "local_fs":
    RETURN setup_local_fs(fallback_config)
  ELIF fallback_config.type == "mock":
    RETURN create_mock(fallback_config)

  RAISE ConfigError(f"Unknown fallback type: {fallback_config.type}")


FUNCTION start_docker_fallback(config):
  container_name = f"speckit-fallback-{config.image.split(':')[0]}"

  # Check if already running
  IF docker_container_running(container_name):
    LOG f"Fallback container {container_name} already running"
    RETURN get_container_connection(container_name)

  # Start container
  LOG f"Starting fallback: {config.image}"
  docker run -d --name $container_name \
    -p $config.config.port:$config.config.port \
    $config.image

  # Wait for ready
  wait_for_ready(container_name, config.startup_time)

  RETURN get_container_connection(container_name)
```

## Integration with ship.md

```text
# At ship phase start:
Read `templates/shared/ship/dependency-dag.md` and apply.

# Build and execute DAG:
dag = build_dependency_dag(config, environment)
env_dag = get_environment_dag(dag, environment)

# Check for changes
IF git_changes_available:
  impact = analyze_change_impact(changed_files, env_dag)
  IF impact.skip_provision:
    LOG "No infra changes, skipping provision"
  IF impact.skip_deploy:
    LOG "No deploy changes, skipping deploy"

# Execute
result = execute_dag(env_dag, target_node="verify")
```

## Output Format

```text
🔗 Dependency DAG Execution
├── Environment: staging
├── Profile Applied:
│   ├── Skipped: performance
│   └── Demoted: monitoring → app (OPTIONAL)
├── Impact Analysis:
│   ├── Changed files: 3
│   ├── Affected nodes: app, smoke, acceptance
│   ├── Skip provision: true
│   └── Skip deploy: false
├── Execution Plan:
│   ├── Level 1: [secrets] (1 node)
│   ├── Level 2: [app] (1 node)
│   ├── Level 3: [smoke] (1 node)
│   └── Level 4: [acceptance] (1 node)
├── Execution:
│   ├── secrets: ✓ cached (0.1s)
│   ├── cache: ✓ fallback:local_cache (2.1s)
│   ├── app: ✓ deployed (45.2s)
│   ├── smoke: ✓ passed (8.3s)
│   └── acceptance: ✓ passed (22.1s)
├── Timing:
│   ├── Analysis: 0.3s
│   ├── Execution: 77.8s
│   └── Saved: ~180s (vs full DAG)
└── Result: SUCCESS ✓
```

## CLI Flags

```bash
# Force eager resolution (no lazy)
speckit ship --eager-deps

# Skip optional dependencies
speckit ship --skip-optional

# Target specific node only
speckit ship --target=smoke

# Show DAG visualization
speckit ship --show-dag

# Dry run (show plan only)
speckit ship --dag-dry-run
```

## DAG Visualization

```text
FUNCTION visualize_dag(dag, highlight_path=None):
  # ASCII visualization
  output = []
  levels = dag.group_by_level()

  FOR level_idx, nodes IN enumerate(levels):
    level_str = f"L{level_idx}: "
    node_strs = []

    FOR node IN nodes:
      status = "✓" IF node.resolved ELSE "○" IF node.pending ELSE "·"
      highlight = "*" IF node IN highlight_path ELSE ""
      node_strs.append(f"{highlight}{status}{node.name}")

    level_str += " | ".join(node_strs)
    output.append(level_str)

  # Show edges
  output.append("\nEdges:")
  FOR edge IN dag.edges:
    type_symbol = {
      HARD: "──▶",
      SOFT: "- -▶",
      OPTIONAL: "···▶",
      LAZY: "~~~▶"
    }[edge.type]
    output.append(f"  {edge.source.name} {type_symbol} {edge.target.name}")

  RETURN "\n".join(output)


# Example output:
# L0: ✓networking | ✓secrets
# L1: ✓database | ✓cache | ·storage
# L2: *✓app
# L3: *✓smoke | ○worker | ○scheduler
# L4: *○acceptance
#
# Edges:
#   networking ──▶ database
#   database ──▶ app
#   cache - -▶ app
#   app ──▶ smoke
#   smoke ──▶ acceptance
```

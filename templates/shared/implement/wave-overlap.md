# Wave Overlap Execution

## Purpose

Enable speculative execution of next wave tasks when critical dependencies in current wave are satisfied, reducing idle time between waves.

## Performance Impact

| Mode | Time | Savings |
|------|------|---------|
| Sequential waves | 220-340s | baseline |
| Overlapped waves | 160-250s | 25-30% |

## Configuration

```yaml
wave_overlap:
  enabled: true
  skip_flag: "--sequential-waves"
  overlap_threshold: 0.80  # Start next wave at 80% completion
  critical_deps_only: true  # Only wait for critical path deps
```

## Wave Structure Analysis

```text
ANALYZE_WAVE_STRUCTURE(subagents):

  # Group subagents by wave (based on depends_on chains)
  waves = {
    1: [],  # INFRA: project-scaffolder, dependency-installer
    2: [],  # CORE: data-layer, ui-foundation, api-builder, ui-feature
    3: [],  # TESTING: unit-test, integration-test
    4: []   # REVIEW: code-reviewer, documentation
  }

  FOR agent IN subagents:
    wave = determine_wave(agent)
    waves[wave].append(agent)

  # Build dependency graph
  graph = DirectedGraph()
  FOR agent IN subagents:
    graph.add_node(agent.role)
    FOR dep IN agent.depends_on:
      graph.add_edge(dep, agent.role)

  # Identify critical path
  critical_path = graph.longest_path()

  RETURN {waves, graph, critical_path}


FUNCTION determine_wave(agent):
  IF agent.role_group == "INFRA":
    RETURN 1
  ELIF agent.role_group IN ["BACKEND", "FRONTEND"]:
    RETURN 2
  ELIF agent.role_group == "TESTING":
    RETURN 3
  ELIF agent.role_group IN ["REVIEW", "DOCS"]:
    RETURN 4
```

## Overlap Execution Algorithm

```text
OVERLAPPED_WAVE_EXECUTION(waves, graph, tasks):

  completed = set()
  in_progress = set()
  results = {}

  # Start Wave 1 immediately
  FOR agent IN waves[1]:
    in_progress.add(agent.role)
    spawn_agent(agent)

  WHILE NOT all_waves_complete(waves, completed):
    # Check for completions
    FOR role IN in_progress.copy():
      IF agent_completed(role):
        in_progress.remove(role)
        completed.add(role)
        results[role] = get_agent_result(role)

    # Check if we can start next wave agents
    FOR wave_num IN [2, 3, 4]:
      FOR agent IN waves[wave_num]:
        IF agent.role IN completed OR agent.role IN in_progress:
          CONTINUE

        IF can_start_early(agent, completed, graph):
          in_progress.add(agent.role)
          spawn_agent(agent)
          LOG f"🚀 Early start: {agent.role} (deps satisfied)"

    # Small delay to prevent busy-waiting
    sleep(100ms)

  RETURN results


FUNCTION can_start_early(agent, completed, graph):
  # Get this agent's dependencies
  deps = graph.predecessors(agent.role)

  IF agent.role_group == "TESTING":
    # Testing can start when primary implementation done
    # Don't need to wait for ALL backend/frontend
    required_deps = filter_critical_deps(deps, agent)
    RETURN all(d IN completed FOR d IN required_deps)

  IF agent.role_group == "REVIEW":
    # Review can start when testing >= 80% complete
    testing_agents = [a FOR a IN deps IF a.role_group == "TESTING"]
    completed_testing = [a FOR a IN testing_agents IF a IN completed]
    RETURN len(completed_testing) / len(testing_agents) >= 0.8

  # Default: all deps must be complete
  RETURN all(d IN completed FOR d IN deps)


FUNCTION filter_critical_deps(deps, agent):
  # Return only the critical dependencies for this agent
  critical = []

  IF agent.role == "unit-test-generator":
    # Needs: data-layer, api-builder
    # Doesn't need: ui-foundation, ui-feature
    critical = ["data-layer-builder", "api-builder"]

  ELIF agent.role == "integration-test-generator":
    # Needs: api-builder, ui-feature
    # Doesn't need: complete ui-feature (can test partial)
    critical = ["api-builder"]  # ui-feature is nice-to-have

  RETURN [d FOR d IN deps IF d IN critical]
```

## Wave-Specific Start Conditions

```text
WAVE_START_CONDITIONS = {
  wave_2: {
    # Can start when Wave 1 core infra done
    conditions: [
      "project-scaffolder DONE",
      "dependency-installer DONE"
    ],
    can_skip_waiting_for: [
      # If any Wave 1 agent is slow, don't block
    ]
  },

  wave_3: {
    # Can start when core implementation available
    conditions: [
      "data-layer-builder DONE",       # For unit tests
      "api-builder DONE OR >= 80%"     # For integration tests
    ],
    can_skip_waiting_for: [
      "ui-foundation-builder",  # Tests can run without UI
      "ui-feature-builder"      # Can test API independently
    ]
  },

  wave_4: {
    # Can start when enough to review
    conditions: [
      "ANY testing agent DONE"  # Start review on completed code
    ],
    can_skip_waiting_for: [
      "integration-test-generator"  # Review code while e2e runs
    ]
  }
}
```

## Progress Tracking

```text
TRACK_WAVE_PROGRESS():

  progress = {
    wave_1: {total: 2, done: 2, pct: 100},
    wave_2: {total: 4, done: 3, pct: 75},
    wave_3: {total: 2, done: 0, pct: 0, started_early: true},
    wave_4: {total: 2, done: 0, pct: 0}
  }

  OUTPUT:
  ```text
  🌊 Wave Progress (Overlap Mode)
  ├── Wave 1 [INFRA]:    ████████████████████ 100% (2/2) ✓
  ├── Wave 2 [CORE]:     ███████████████░░░░░  75% (3/4)
  │   └── ui-feature-builder: IN_PROGRESS
  ├── Wave 3 [TESTING]:  ░░░░░░░░░░░░░░░░░░░░   0% (0/2) 🚀 EARLY START
  │   ├── unit-test-generator: WAITING (deps: api-builder)
  │   └── integration-test-generator: STARTED (overlap enabled)
  └── Wave 4 [REVIEW]:   ░░░░░░░░░░░░░░░░░░░░   0% (0/2)

  Overlap Savings: ~45s estimated
  ```
```

## Conflict Resolution

```text
HANDLE_WAVE_CONFLICTS():

  # Same-file conflict: queue
  IF agent_A.file_set INTERSECTS agent_B.file_set:
    IF agent_A.wave < agent_B.wave:
      queue_agent(agent_B)  # Lower wave has priority
    ELSE:
      # Same wave: use role_group isolation
      IF agent_A.role_group != agent_B.role_group:
        # Different groups can proceed
        PASS
      ELSE:
        # Same group: queue lower priority
        queue_lower_priority(agent_A, agent_B)

  # Resource conflict (memory/CPU)
  IF current_parallel_count >= max_parallel:
    queue_agent(newest_agent)
```

## Integration with implement.md

Add to `orchestration` section:

```yaml
orchestration:
  max_parallel: 3
  conflict_resolution: queue
  wave_overlap:
    enabled: true
    skip_flag: "--sequential-waves"
    overlap_threshold: 0.80
```

Reference in Step 7:

```text
Read `templates/shared/implement/wave-overlap.md` and apply overlap execution.

Execute implementation with wave overlap:
1. Start Wave 1 agents
2. When Wave 1 >= 80% OR critical deps done, start Wave 2
3. When Wave 2 has data-layer/api done, start unit tests
4. When any tests done, start code review on completed code
```

## Output Format

```text
🌊 Wave Overlap Execution Summary
├── Total agents: 10
├── Waves: 4
├── Overlap events: 3
│   ├── Wave 3 started 45s early (api-builder done)
│   ├── integration-test started with partial ui-feature
│   └── code-reviewer started while e2e running
├── Sequential time (estimated): 340s
├── Actual time: 248s
└── Time saved: 92s (27%)
```

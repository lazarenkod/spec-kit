---
description: Set up production observability with OpenTelemetry, dashboards, and alerting
persona: devops-agent
skills: [observability-setup]
inputs:
  service_name: { type: string, required: true }
  stack: { type: enum, options: [node, python, go, java, dotnet], required: false }
  observability_backend: { type: enum, options: [self-hosted, grafana-cloud, datadog, new-relic], default: self-hosted }
outputs:
  - docs/monitor.md
  - src/lib/telemetry.{ts,py,go}
  - infra/observability/docker-compose.yml
  - infra/observability/grafana/dashboards/
  - docs/runbooks/
handoffs:
  - label: Configure Alerts
    agent: speckit.monitor
    condition: alerts_not_configured
  - label: Prepare Launch
    agent: speckit.launch
    condition: observability_complete
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 4000
---

## Input
```text
$ARGUMENTS
```

---

## Purpose

Set up production-grade observability using OpenTelemetry: distributed tracing, metrics, logs, dashboards, alerting.

**When to use**: After deploying a service, before launch, when troubleshooting production.

---

## Workflow (6 Steps)

### Step 1: Detect Stack

```yaml
detection:
  runtime: [auto-detect from package.json, requirements.txt, go.mod]
  framework: [Express, FastAPI, Gin, Spring]
  database: [PostgreSQL, MySQL, MongoDB]
  cache: [Redis, Memcached]
  message_queue: [RabbitMQ, Kafka, SQS]

instrumentation_libraries:
  node: [@opentelemetry/sdk-node, @opentelemetry/auto-instrumentations-node]
  python: [opentelemetry-sdk, opentelemetry-instrumentation]
  go: [go.opentelemetry.io/otel, go.opentelemetry.io/contrib/instrumentation]
```

### Step 2: Generate Instrumentation

```text
Load observability-setup skill → generate:
  1. Telemetry SDK initialization (language-specific)
  2. Auto-instrumentation (HTTP, database, cache)
  3. Custom span/metric helpers
```

### Step 3: Deploy Observability Stack

```text
Generate docker-compose.yml or K8s manifests:
  - OpenTelemetry Collector (receive, process, export)
  - Jaeger/Tempo (traces)
  - Prometheus (metrics)
  - Loki (logs)
  - Grafana (visualization)
  - Alertmanager (notifications)
```

### Step 4: Configure Dashboards

| Dashboard | Purpose |
|-----------|---------|
| Service Overview | Golden signals for all services |
| Service Deep Dive | Detailed metrics per service |
| SLO Dashboard | Error budget tracking |
| Infrastructure | Node/container health |
| Database | Query performance, connections |

### Step 5: Configure Alerting

```yaml
alert_categories:
  golden_signals: [HighLatencyP95, CriticalLatencyP99, HighErrorRate, CriticalErrorRate, TrafficDropped, NoTraffic]
  resources: [HighCPUUsage, HighMemoryUsage, DiskSpaceLow]
  database: [ConnectionPoolExhausted, SlowQueries, ReplicationLag]
  slo: [ErrorBudgetBurn, ErrorBudgetExhausted]
  application: [QueueBacklog, CacheHitRateLow, ExternalAPIErrors]

slo_definition:
  availability: { target: 99.9%, window: 30d, indicator: "1 - (errors/total)" }
  latency: { target: 95%, threshold: 500ms, window: 30d }

error_budget:
  monthly: "0.1% of requests can fail"
  burn_rate_alerts: ["1h burn > 14.4x → warning", "6h burn > 6x → critical"]
```

### Step 6: Generate Runbooks & Verify

```text
FOR EACH critical alert:
  Generate runbook: summary, impact, diagnosis steps, resolution, escalation

VERIFICATION:
  - [ ] Service starts without telemetry errors
  - [ ] Traces appear in Jaeger within 30s
  - [ ] Metrics appear in Prometheus
  - [ ] Logs appear in Loki
  - [ ] Dashboard panels show data
  - [ ] Test alert fires and reaches notification channel
```

---

## Quality Gates

| Gate | Condition | Severity |
|------|-----------|----------|
| Telemetry Working | traces AND metrics received | Error |
| Dashboards Created | >= 3 dashboards | Warning |
| Alerts Configured | >= 5 alert rules | Warning |
| Runbooks Written | runbook per critical alert | Warning |
| SLOs Defined | >= 1 SLO with budget | Info |

---

## Output: monitor.md

```markdown
# Monitoring Configuration: {{service_name}}

## Overview
| Component | Technology | Endpoint |
|-----------|------------|----------|
| Traces | Jaeger | http://localhost:16686 |
| Metrics | Prometheus | http://localhost:9090 |
| Logs | Loki | http://localhost:3100 |
| Dashboards | Grafana | http://localhost:3000 |
| Alerts | Alertmanager | http://localhost:9093 |

## Instrumentation
- SDK: src/lib/telemetry.{ts|py|go}
- Auto-instrumented: HTTP, Database, Cache, Framework

## Custom Metrics
| Metric | Type | Description |
|--------|------|-------------|
| {{service}}_requests_total | Counter | Total HTTP requests |
| {{service}}_request_duration_seconds | Histogram | Request latency |
| {{service}}_errors_total | Counter | Total errors |

## Dashboards
| Dashboard | Purpose | Link |
|-----------|---------|------|
| Overview | Golden signals | [Open](http://localhost:3000/d/overview) |
| Deep Dive | Detailed metrics | [Open](http://localhost:3000/d/{{service}}) |
| SLO | Error budget | [Open](http://localhost:3000/d/slo) |

## Alerting
| Alert | Severity | Threshold | Runbook |
|-------|----------|-----------|---------|
| HighErrorRate | Warning | > 1% for 5m | [Link](docs/runbooks/high-error-rate.md) |
| CriticalErrorRate | Critical | > 5% for 2m | [Link](docs/runbooks/high-error-rate.md) |
| HighLatencyP95 | Warning | > 1s for 5m | [Link](docs/runbooks/high-latency.md) |

## SLOs
| SLO | Target | Current | Budget Remaining |
|-----|--------|---------|------------------|
| Availability | 99.9% | 99.95% | 80% |
| Latency (p95 < 500ms) | 95% | 97% | 100% |

## On-Call Escalation
1. Primary: @oncall-primary (PagerDuty)
2. Secondary: @oncall-secondary (after 15 min)
3. Engineering Lead: @eng-lead (after 30 min)
```

---

## Integration Points

| Command | Integration |
|---------|-------------|
| `/speckit.ship` | Triggers monitor setup post-deployment |
| `/speckit.launch` | Ensures monitoring before launch |
| `/speckit.implement` | Adds telemetry instrumentation |

---

## Anti-Patterns

- Deploying without monitoring configured
- Alert fatigue from too many low-priority alerts
- Dashboards with too many panels
- Missing distributed tracing correlation
- Outdated runbooks
- Not testing alerting notification paths
- High-cardinality metrics without cost awareness

---

## Output Format

```text
┌─────────────────────────────────────────────────────────────┐
│ /speckit.monitor Complete                                    │
├─────────────────────────────────────────────────────────────┤
│ Service: {service_name}                                      │
│ Stack: {detected_stack}                                      │
│ Backend: {observability_backend}                             │
│                                                              │
│ Generated:                                                   │
│   ✓ Telemetry SDK    ✓ OTEL Collector    ✓ Dashboards (5)   │
│   ✓ Alert Rules (8)  ✓ Runbooks (5)      ✓ SLO Config       │
│                                                              │
│ Verification:                                                │
│   Telemetry: ✓  Dashboards: ✓  Alerts: ✓                    │
│                                                              │
│ Endpoints:                                                   │
│   Grafana: http://localhost:3000                            │
│   Jaeger: http://localhost:16686                            │
│                                                              │
│ Next: /speckit.launch                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Context

{ARGS}

---
name: monitor
description: Set up production observability with OpenTelemetry, dashboards, and alerting
version: 1.0.0
persona: devops-agent
skills:
  - observability-setup
inputs:
  service_name:
    type: string
    required: true
    description: Name of the service to monitor
  stack:
    type: enum
    options: [node, python, go, java, dotnet]
    required: false
    description: Technology stack (auto-detected if not specified)
  observability_backend:
    type: enum
    options: [self-hosted, grafana-cloud, datadog, new-relic]
    default: self-hosted
    description: Where to send telemetry data
outputs:
  - docs/monitor.md
  - src/lib/telemetry.{ts,py,go}
  - infra/observability/docker-compose.yml
  - infra/observability/grafana/dashboards/
  - infra/observability/rules/
  - docs/runbooks/
quality_gates:
  - name: telemetry_working
    condition: "traces_received AND metrics_received"
    severity: error
  - name: dashboards_created
    condition: "dashboard_count >= 3"
    severity: warning
  - name: alerts_configured
    condition: "alert_rules_count >= 5"
    severity: warning
handoffs:
  - label: Configure Alerts
    agent: speckit.monitor
    condition: "alerts_not_configured"
  - label: Prepare Launch
    agent: speckit.launch
    condition: "observability_complete"
---

# /speckit.monitor

## Purpose

Set up production-grade observability for your services using the OpenTelemetry standard. This command configures distributed tracing, metrics collection, log aggregation, dashboards, and alerting following industry best practices.

## When to Use

- **After** deploying a service to production
- When you need visibility into service behavior
- When troubleshooting production issues
- Before launching to ensure monitoring is in place

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      /speckit.monitor                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. DETECT                                                       │
│     └── Identify technology stack and dependencies               │
│                                                                  │
│  2. INSTRUMENT                                                   │
│     ├── Generate OpenTelemetry SDK configuration                 │
│     ├── Add auto-instrumentation for frameworks                  │
│     └── Create custom span/metric helpers                        │
│                                                                  │
│  3. DEPLOY STACK                                                 │
│     ├── OpenTelemetry Collector                                  │
│     ├── Jaeger (traces) / Tempo                                  │
│     ├── Prometheus (metrics)                                     │
│     ├── Loki (logs)                                              │
│     └── Grafana (visualization)                                  │
│                                                                  │
│  4. CONFIGURE                                                    │
│     ├── Import dashboard templates                               │
│     ├── Set up alerting rules                                    │
│     └── Define SLOs and error budgets                            │
│                                                                  │
│  5. DOCUMENT                                                     │
│     ├── Generate runbooks for each alert                         │
│     └── Create on-call playbook                                  │
│                                                                  │
│  6. VERIFY                                                       │
│     ├── Test telemetry pipeline end-to-end                       │
│     ├── Verify dashboards populate correctly                     │
│     └── Test alert notification path                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Observability Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│   │  API    │  │  Web    │  │ Worker  │  │  Queue  │           │
│   │ Service │  │   App   │  │ Service │  │Consumer │           │
│   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘           │
│        │            │            │            │                 │
│        └────────────┴────────────┴────────────┘                 │
│                           │                                      │
│                   OpenTelemetry SDK                              │
│              (auto-instrumentation + custom spans)               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Collection Layer                              │
│                                                                  │
│   ┌─────────────────────────────────────────────┐               │
│   │           OpenTelemetry Collector           │               │
│   │   (receive, process, export)                │               │
│   └─────────────────────┬───────────────────────┘               │
│                         │                                        │
│         ┌───────────────┼───────────────┐                       │
│         ▼               ▼               ▼                       │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐                   │
│   │  Traces  │   │  Metrics │   │   Logs   │                   │
│   │  (Jaeger)│   │(Prometheus)│ │  (Loki)  │                   │
│   └────┬─────┘   └────┬─────┘   └────┬─────┘                   │
│        │              │              │                          │
└────────┴──────────────┴──────────────┴──────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Visualization Layer                            │
│                                                                  │
│   ┌─────────────────────────────────────────────┐               │
│   │                  Grafana                     │               │
│   │   ┌─────────┐ ┌─────────┐ ┌─────────┐      │               │
│   │   │Overview │ │ Service │ │  SLO    │      │               │
│   │   │Dashboard│ │Dashboard│ │Dashboard│      │               │
│   │   └─────────┘ └─────────┘ └─────────┘      │               │
│   └─────────────────────────────────────────────┘               │
│                                                                  │
│   ┌─────────────────────────────────────────────┐               │
│   │              Alertmanager                    │               │
│   │   → Slack, PagerDuty, Email, Webhook        │               │
│   └─────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

## Command Execution

### Step 1: Detect Stack

```yaml
detection:
  runtime: "[auto-detect from package.json, requirements.txt, go.mod, etc.]"
  framework: "[Express, FastAPI, Gin, Spring, etc.]"
  database: "[PostgreSQL, MySQL, MongoDB, etc.]"
  cache: "[Redis, Memcached, etc.]"
  message_queue: "[RabbitMQ, Kafka, SQS, etc.]"

instrumentation_libraries:
  node:
    - "@opentelemetry/sdk-node"
    - "@opentelemetry/auto-instrumentations-node"
    - "@opentelemetry/exporter-trace-otlp-http"
    - "@opentelemetry/exporter-metrics-otlp-http"

  python:
    - "opentelemetry-sdk"
    - "opentelemetry-instrumentation"
    - "opentelemetry-exporter-otlp"

  go:
    - "go.opentelemetry.io/otel"
    - "go.opentelemetry.io/otel/sdk"
    - "go.opentelemetry.io/contrib/instrumentation"
```

### Step 2: Generate Instrumentation

Load `observability-setup` skill to generate:

1. **Telemetry SDK initialization** - Language-specific setup
2. **Auto-instrumentation** - HTTP, database, cache, etc.
3. **Custom helpers** - For adding business logic spans/metrics

### Step 3: Deploy Observability Stack

Generate Docker Compose or Kubernetes manifests:

```bash
# Self-hosted (Docker Compose)
docker-compose -f infra/observability/docker-compose.yml up -d

# Kubernetes
kubectl apply -f infra/observability/k8s/
```

### Step 4: Configure Dashboards

Generate Grafana dashboards:

| Dashboard | Purpose |
|-----------|---------|
| Service Overview | Golden signals for all services |
| Service Deep Dive | Detailed metrics per service |
| SLO Dashboard | Error budget tracking |
| Infrastructure | Node/container health |
| Database | Query performance, connections |

### Step 5: Configure Alerting

Generate alerting rules based on templates:

```yaml
alert_categories:
  golden_signals:
    - HighLatencyP95
    - CriticalLatencyP99
    - HighErrorRate
    - CriticalErrorRate
    - TrafficDropped
    - NoTraffic
    - HighCPUUsage
    - HighMemoryUsage
    - DiskSpaceLow

  database:
    - DatabaseConnectionPoolExhausted
    - DatabaseSlowQueries
    - DatabaseReplicationLag

  slo:
    - SLOErrorBudgetBurn
    - SLOErrorBudgetExhausted

  application:
    - QueueBacklog
    - CacheHitRateLow
    - ExternalAPIErrors
```

### Step 6: Define SLOs

```yaml
slo_definition:
  availability:
    target: 99.9%
    window: 30d
    indicator: "1 - (error_requests / total_requests)"

  latency:
    target: 95%
    threshold: 500ms
    window: 30d
    indicator: "requests_under_threshold / total_requests"

error_budget:
  monthly_budget: "0.1% of requests can fail"
  burn_rate_alerts:
    - "1h burn > 14.4x triggers warning"
    - "6h burn > 6x triggers critical"
```

### Step 7: Generate Runbooks

Create runbook for each alert with:
- Summary of what triggered the alert
- Impact assessment
- Diagnosis steps with specific commands
- Resolution options
- Escalation paths
- Post-incident checklist

### Step 8: Verify Setup

```yaml
verification_checklist:
  telemetry:
    - [ ] "Service starts without telemetry errors"
    - [ ] "Traces appear in Jaeger within 30 seconds"
    - [ ] "Metrics appear in Prometheus"
    - [ ] "Logs appear in Loki"

  dashboards:
    - [ ] "Service Overview dashboard loads"
    - [ ] "All panels show data (no 'No Data')"
    - [ ] "Drill-down links work"

  alerting:
    - [ ] "Test alert fires correctly"
    - [ ] "Alert reaches Slack/PagerDuty"
    - [ ] "Runbook link accessible"

  documentation:
    - [ ] "monitor.md generated"
    - [ ] "Runbooks for all alerts"
    - [ ] "On-call playbook complete"
```

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

### SDK Setup
```
src/lib/telemetry.ts (or .py/.go)
```

### Auto-instrumented
- HTTP requests (inbound and outbound)
- Database queries ({{database}})
- Cache operations ({{cache}})
- Framework-specific ({{framework}})

### Custom Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `{{service}}_requests_total` | Counter | Total HTTP requests |
| `{{service}}_request_duration_seconds` | Histogram | Request latency |
| `{{service}}_errors_total` | Counter | Total errors |

## Dashboards

| Dashboard | Purpose | Link |
|-----------|---------|------|
| Service Overview | Golden signals | [Open](http://localhost:3000/d/overview) |
| {{service}} Deep Dive | Detailed metrics | [Open](http://localhost:3000/d/{{service}}) |
| SLO Dashboard | Error budget | [Open](http://localhost:3000/d/slo) |

## Alerting

### Active Rules
| Alert | Severity | Threshold | Runbook |
|-------|----------|-----------|---------|
| HighErrorRate | Warning | > 1% for 5m | [Link](docs/runbooks/high-error-rate.md) |
| CriticalErrorRate | Critical | > 5% for 2m | [Link](docs/runbooks/high-error-rate.md) |
| HighLatencyP95 | Warning | > 1s for 5m | [Link](docs/runbooks/high-latency.md) |

### Notification Channels
- Slack: #alerts
- PagerDuty: [Configured]
- Email: [Configured]

## SLOs

| SLO | Target | Current | Budget Remaining |
|-----|--------|---------|------------------|
| Availability | 99.9% | 99.95% | 80% |
| Latency (p95 < 500ms) | 95% | 97% | 100% |

## On-Call

### Escalation Path
1. Primary: @oncall-primary (PagerDuty)
2. Secondary: @oncall-secondary (after 15 min)
3. Engineering Lead: @eng-lead (after 30 min)

### Quick Links
- [Grafana](http://localhost:3000)
- [Jaeger](http://localhost:16686)
- [Runbooks](docs/runbooks/)
- [PagerDuty](https://pagerduty.com/...)

---
Generated by /speckit.monitor
Last updated: {{date}}
```

## Integration Points

| Command | Integration |
|---------|-------------|
| `/speckit.ship` | Triggers monitor setup post-deployment |
| `/speckit.launch` | Ensures monitoring before launch |
| `/speckit.implement` | Adds telemetry instrumentation |

## Quality Gates

| Gate | Condition | Severity |
|------|-----------|----------|
| Telemetry Working | traces AND metrics received | Error |
| Dashboards Created | >= 3 dashboards | Warning |
| Alerts Configured | >= 5 alert rules | Warning |
| Runbooks Written | runbook per critical alert | Warning |
| SLOs Defined | >= 1 SLO with budget | Info |

## Anti-Patterns

- Deploying without monitoring configured
- Alert fatigue from too many low-priority alerts
- Dashboards with too many panels to be useful
- Missing distributed tracing correlation
- Runbooks that are out of date
- Not testing alerting notification paths
- Ignoring cost implications of high-cardinality metrics

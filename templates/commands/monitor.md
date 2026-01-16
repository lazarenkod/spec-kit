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
claude_code:
  model: sonnet
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 4000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 8000
        max_parallel: 3
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 24000
        max_parallel: 6
        batch_delay: 1500
        wave_overlap_threshold: 0.65
      ultrathink:
        thinking_budget: 96000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 4.0
  depth_defaults:
    standard:
      thinking_budget: 24000
      timeout: 120
    ultrathink:
      thinking_budget: 96000
      additional_agents: [deep-analyzers, security-auditor]
      timeout: 240
  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 24000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (96K thinking budget).
          Auto-downgrading to **Standard** mode (24K budget).
  cost_breakdown:
    standard: {cost: $0.72, time: "120-180s"}
    ultrathink: {cost: $2.88, time: "240-360s"}
  cache_hierarchy: full
  orchestration:
    max_parallel: 6
    fail_fast: true
    wave_overlap:
      enabled: true
      overlap_threshold: 0.65
  subagents:
    # Wave 1: Configuration (parallel)
    - role: telemetry-configurer
      role_group: INFRA
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Set up OpenTelemetry instrumentation for the service.
        Detect technology stack from package.json/requirements.txt/go.mod.
        Generate SDK initialization code for traces, metrics, logs.
        Configure auto-instrumentation for detected frameworks.
        Create custom span/metric helpers for business logic.
        Output: src/lib/telemetry.{ts,py,go}.

    - role: alert-designer
      role_group: INFRA
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Design alerting rules based on golden signals and SLOs.
        Create alerts for: high latency, error rate, traffic drops.
        Add database-specific alerts: connection pool, slow queries.
        Define SLO-based alerts: error budget burn rate.
        Generate runbooks for each alert with diagnosis steps.
        Output: infra/observability/rules/, docs/runbooks/.

    # Wave 2: Dashboard Generation (after config)
    - role: dashboard-generator
      role_group: DOCS
      parallel: true
      depends_on: [telemetry-configurer, alert-designer]
      priority: 20
      model_override: haiku
      prompt: |
        Generate Grafana dashboards for observability.
        Create: Service Overview, Service Deep Dive, SLO Dashboard.
        Include Infrastructure and Database panels.
        Configure data sources for Prometheus, Loki, Jaeger.
        Output: infra/observability/grafana/dashboards/.
flags:
  - name: --thinking-depth
    type: choice
    choices: [standard, ultrathink]
    default: standard
    description: |
      Thinking budget control:
      - standard: 24K budget, standard analysis (~$0.72) [RECOMMENDED]
      - ultrathink: 96K budget, deep analysis (~$2.88)
  - name: --max-model
    type: choice
    choices: [opus, sonnet, haiku]
    description: Override model cap
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

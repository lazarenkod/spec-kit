# Alerting Rules

## Purpose

Define alerting rules for production monitoring, including severity levels, escalation paths, and alert fatigue prevention strategies.

## Alert Severity Framework

### Severity Levels

```yaml
severity_levels:
  critical:
    description: "Service down, data loss imminent, security breach"
    response_time: "5 minutes"
    notification_channels:
      - pagerduty
      - slack_oncall
      - sms
    auto_escalate_after: "15 minutes"
    examples:
      - "All API endpoints returning 5xx"
      - "Database connection pool exhausted"
      - "Memory usage > 95%"
      - "Security breach detected"
      - "Data corruption detected"

  warning:
    description: "Degraded performance, approaching limits"
    response_time: "30 minutes"
    notification_channels:
      - slack_alerts
    auto_escalate_after: "2 hours"
    examples:
      - "p95 latency > 2x normal"
      - "Error rate > 1%"
      - "Disk usage > 80%"
      - "Certificate expiring in 7 days"

  info:
    description: "Notable events, deployment notifications"
    response_time: "Business hours"
    notification_channels:
      - slack_info
    auto_escalate_after: null
    examples:
      - "Deployment completed"
      - "Backup completed"
      - "Certificate expiring in 30 days"
      - "New user signup milestone"
```

## Golden Signals Alerts

### Latency Alerts

```yaml
# prometheus/rules/latency.yml
groups:
  - name: latency
    rules:
      - alert: HighLatencyP95
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p95 latency on {{ $labels.service }}"
          description: "p95 latency is {{ $value }}s (threshold: 1s)"
          runbook: "docs/runbooks/high-latency.md"

      - alert: CriticalLatencyP99
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 5
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Critical p99 latency on {{ $labels.service }}"
          description: "p99 latency is {{ $value }}s (threshold: 5s)"
          runbook: "docs/runbooks/high-latency.md"
```

### Error Rate Alerts

```yaml
# prometheus/rules/errors.yml
groups:
  - name: errors
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service)
          > 0.01
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook: "docs/runbooks/high-error-rate.md"

      - alert: CriticalErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service)
          > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Critical error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook: "docs/runbooks/high-error-rate.md"
```

### Traffic Alerts

```yaml
# prometheus/rules/traffic.yml
groups:
  - name: traffic
    rules:
      - alert: TrafficDropped
        expr: |
          sum(rate(http_requests_total[5m])) by (service)
          <
          sum(rate(http_requests_total[5m] offset 1h)) by (service) * 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Traffic dropped >50% on {{ $labels.service }}"
          description: "Current traffic is significantly lower than 1 hour ago"
          runbook: "docs/runbooks/traffic-anomaly.md"

      - alert: NoTraffic
        expr: |
          sum(rate(http_requests_total[5m])) by (service) == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "No traffic on {{ $labels.service }}"
          description: "Service is receiving zero requests"
          runbook: "docs/runbooks/no-traffic.md"
```

### Saturation Alerts

```yaml
# prometheus/rules/saturation.yml
groups:
  - name: saturation
    rules:
      - alert: HighCPUUsage
        expr: |
          100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value | humanize }}%"
          runbook: "docs/runbooks/high-cpu.md"

      - alert: HighMemoryUsage
        expr: |
          (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | humanize }}%"
          runbook: "docs/runbooks/high-memory.md"

      - alert: CriticalMemoryUsage
        expr: |
          (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 95
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Critical memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | humanize }}%"
          runbook: "docs/runbooks/high-memory.md"

      - alert: DiskSpaceLow
        expr: |
          (1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100 > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Disk usage is {{ $value | humanize }}%"
          runbook: "docs/runbooks/low-disk.md"
```

## Database Alerts

```yaml
# prometheus/rules/database.yml
groups:
  - name: database
    rules:
      - alert: DatabaseConnectionPoolExhausted
        expr: |
          pg_stat_activity_count / pg_settings_max_connections > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Database connection pool near exhaustion"
          description: "{{ $value | humanizePercentage }} of connections in use"
          runbook: "docs/runbooks/db-connections.md"

      - alert: DatabaseSlowQueries
        expr: |
          rate(pg_stat_statements_seconds_total[5m])
          / rate(pg_stat_statements_calls_total[5m]) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow database queries detected"
          description: "Average query time is {{ $value }}s"
          runbook: "docs/runbooks/slow-queries.md"

      - alert: DatabaseReplicationLag
        expr: |
          pg_replication_lag_seconds > 30
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Database replication lag detected"
          description: "Replication lag is {{ $value }}s"
          runbook: "docs/runbooks/replication-lag.md"
```

## Application-Specific Alerts

```yaml
# prometheus/rules/application.yml
groups:
  - name: application
    rules:
      - alert: QueueBacklog
        expr: |
          queue_messages_total - queue_messages_processed_total > 1000
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Queue backlog growing on {{ $labels.queue }}"
          description: "{{ $value }} messages pending"
          runbook: "docs/runbooks/queue-backlog.md"

      - alert: CacheHitRateLow
        expr: |
          rate(cache_hits_total[5m])
          / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m])) < 0.8
        for: 15m
        labels:
          severity: info
        annotations:
          summary: "Low cache hit rate"
          description: "Cache hit rate is {{ $value | humanizePercentage }}"

      - alert: ExternalAPIErrors
        expr: |
          sum(rate(external_api_errors_total[5m])) by (api) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "External API {{ $labels.api }} returning errors"
          description: "Error rate: {{ $value }}/s"
          runbook: "docs/runbooks/external-api.md"
```

## SLO-Based Alerts

```yaml
# prometheus/rules/slo.yml
groups:
  - name: slo
    rules:
      # Error budget burn rate alerts
      - alert: SLOErrorBudgetBurn
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[1h]))
            / sum(rate(http_requests_total[1h]))
          ) > (1 - 0.999) * 14.4
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "SLO error budget burning fast"
          description: "At current rate, monthly error budget exhausted in 5 days"

      - alert: SLOErrorBudgetExhausted
        expr: |
          (
            sum(increase(http_requests_total{status=~"5.."}[30d]))
            / sum(increase(http_requests_total[30d]))
          ) > (1 - 0.999)
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "SLO error budget exhausted"
          description: "Monthly 99.9% availability SLO breached"
```

## Alertmanager Configuration

```yaml
# alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: '${SLACK_WEBHOOK_URL}'

route:
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'default'

  routes:
    - match:
        severity: critical
      receiver: 'critical'
      continue: true

    - match:
        severity: warning
      receiver: 'warning'

    - match:
        severity: info
      receiver: 'info'

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts'
        send_resolved: true

  - name: 'critical'
    pagerduty_configs:
      - service_key: '${PAGERDUTY_SERVICE_KEY}'
    slack_configs:
      - channel: '#alerts-critical'
        send_resolved: true

  - name: 'warning'
    slack_configs:
      - channel: '#alerts'
        send_resolved: true

  - name: 'info'
    slack_configs:
      - channel: '#alerts-info'
        send_resolved: false

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'service']
```

## Alert Fatigue Prevention

```yaml
best_practices:
  noise_reduction:
    - "Set appropriate 'for' durations to avoid flapping"
    - "Use inhibit rules to suppress redundant alerts"
    - "Group related alerts together"
    - "Route low-priority alerts to info channels"

  actionable_alerts:
    - "Every alert must have a runbook link"
    - "Alert description should include current value and threshold"
    - "Include enough context to start investigation immediately"

  review_cadence:
    weekly:
      - "Review alert volume and noise"
      - "Tune thresholds based on false positives"
    monthly:
      - "Audit runbooks for accuracy"
      - "Review on-call burden distribution"
    quarterly:
      - "Review SLOs and adjust alert thresholds"
      - "Retire alerts that never fire"

  metrics_to_track:
    - alert_count_by_severity_per_week
    - mean_time_to_acknowledge
    - mean_time_to_resolve
    - false_positive_rate
    - alerts_per_oncall_shift
```

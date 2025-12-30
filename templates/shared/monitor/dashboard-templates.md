# Dashboard Templates

## Purpose

Provide Grafana dashboard templates for monitoring production services, including overview dashboards, service-specific views, and SLO tracking.

## Dashboard Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│                    Executive Dashboard                   │
│  (SLOs, Business Metrics, High-Level Health)            │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Service    │  │  Service    │  │Infrastructure│
│  Overview   │  │  Deep Dive  │  │  Overview    │
│  Dashboard  │  │  Dashboard  │  │  Dashboard   │
└─────────────┘  └─────────────┘  └─────────────┘
```

## 1. Service Overview Dashboard

**Purpose**: Single-pane-of-glass view of all services' health

```json
{
  "dashboard": {
    "title": "Service Overview",
    "tags": ["overview", "golden-signals"],
    "refresh": "30s",
    "panels": [
      {
        "title": "Service Health Matrix",
        "type": "stat",
        "gridPos": { "x": 0, "y": 0, "w": 24, "h": 4 },
        "targets": [
          {
            "expr": "up{job=~\"$service\"}",
            "legendFormat": "{{ service }}"
          }
        ],
        "options": {
          "colorMode": "background",
          "graphMode": "none",
          "orientation": "horizontal"
        }
      },
      {
        "title": "Request Rate",
        "type": "timeseries",
        "gridPos": { "x": 0, "y": 4, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{ service }}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "timeseries",
        "gridPos": { "x": 12, "y": 4, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (service) / sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{ service }}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "thresholds": {
              "mode": "absolute",
              "steps": [
                { "color": "green", "value": null },
                { "color": "yellow", "value": 0.01 },
                { "color": "red", "value": 0.05 }
              ]
            }
          }
        }
      },
      {
        "title": "Latency (p95)",
        "type": "timeseries",
        "gridPos": { "x": 0, "y": 12, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
            "legendFormat": "{{ service }}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "s"
          }
        }
      },
      {
        "title": "Resource Utilization",
        "type": "timeseries",
        "gridPos": { "x": 12, "y": 12, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "avg(container_memory_usage_bytes / container_spec_memory_limit_bytes) by (service)",
            "legendFormat": "Memory: {{ service }}"
          },
          {
            "expr": "avg(rate(container_cpu_usage_seconds_total[5m]) / container_spec_cpu_quota * container_spec_cpu_period) by (service)",
            "legendFormat": "CPU: {{ service }}"
          }
        ]
      }
    ]
  }
}
```

## 2. Service Deep Dive Dashboard

**Purpose**: Detailed view of a single service with drill-down capability

```json
{
  "dashboard": {
    "title": "Service Deep Dive: $service",
    "templating": {
      "list": [
        {
          "name": "service",
          "type": "query",
          "query": "label_values(http_requests_total, service)"
        }
      ]
    },
    "panels": [
      {
        "title": "Golden Signals",
        "type": "row",
        "gridPos": { "x": 0, "y": 0, "w": 24, "h": 1 }
      },
      {
        "title": "Request Rate",
        "type": "stat",
        "gridPos": { "x": 0, "y": 1, "w": 6, "h": 4 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{service=\"$service\"}[5m]))"
          }
        ],
        "options": { "graphMode": "area" }
      },
      {
        "title": "Error Rate",
        "type": "stat",
        "gridPos": { "x": 6, "y": 1, "w": 6, "h": 4 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{service=\"$service\",status=~\"5..\"}[5m])) / sum(rate(http_requests_total{service=\"$service\"}[5m]))"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "thresholds": {
              "steps": [
                { "color": "green", "value": null },
                { "color": "red", "value": 0.01 }
              ]
            }
          }
        }
      },
      {
        "title": "Latency (p50/p95/p99)",
        "type": "stat",
        "gridPos": { "x": 12, "y": 1, "w": 6, "h": 4 },
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service=\"$service\"}[5m])) by (le))"
          }
        ],
        "fieldConfig": { "defaults": { "unit": "s" } }
      },
      {
        "title": "Saturation",
        "type": "gauge",
        "gridPos": { "x": 18, "y": 1, "w": 6, "h": 4 },
        "targets": [
          {
            "expr": "avg(container_memory_usage_bytes{service=\"$service\"} / container_spec_memory_limit_bytes)"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "max": 1,
            "thresholds": {
              "steps": [
                { "color": "green", "value": null },
                { "color": "yellow", "value": 0.7 },
                { "color": "red", "value": 0.9 }
              ]
            }
          }
        }
      },
      {
        "title": "Request Rate by Endpoint",
        "type": "timeseries",
        "gridPos": { "x": 0, "y": 5, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{service=\"$service\"}[5m])) by (endpoint)",
            "legendFormat": "{{ endpoint }}"
          }
        ]
      },
      {
        "title": "Error Rate by Endpoint",
        "type": "timeseries",
        "gridPos": { "x": 12, "y": 5, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{service=\"$service\",status=~\"5..\"}[5m])) by (endpoint) / sum(rate(http_requests_total{service=\"$service\"}[5m])) by (endpoint)",
            "legendFormat": "{{ endpoint }}"
          }
        ]
      },
      {
        "title": "Latency Heatmap",
        "type": "heatmap",
        "gridPos": { "x": 0, "y": 13, "w": 24, "h": 8 },
        "targets": [
          {
            "expr": "sum(rate(http_request_duration_seconds_bucket{service=\"$service\"}[5m])) by (le)",
            "format": "heatmap"
          }
        ]
      },
      {
        "title": "Dependencies",
        "type": "row",
        "gridPos": { "x": 0, "y": 21, "w": 24, "h": 1 }
      },
      {
        "title": "Database Query Duration",
        "type": "timeseries",
        "gridPos": { "x": 0, "y": 22, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(db_query_duration_seconds_bucket{service=\"$service\"}[5m])) by (le, operation))",
            "legendFormat": "{{ operation }}"
          }
        ]
      },
      {
        "title": "External API Latency",
        "type": "timeseries",
        "gridPos": { "x": 12, "y": 22, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(external_api_duration_seconds_bucket{service=\"$service\"}[5m])) by (le, api))",
            "legendFormat": "{{ api }}"
          }
        ]
      }
    ]
  }
}
```

## 3. SLO Dashboard

**Purpose**: Track SLO compliance and error budget consumption

```json
{
  "dashboard": {
    "title": "SLO Dashboard",
    "panels": [
      {
        "title": "SLO Status",
        "type": "stat",
        "gridPos": { "x": 0, "y": 0, "w": 24, "h": 4 },
        "targets": [
          {
            "expr": "1 - (sum(increase(http_requests_total{status=~\"5..\"}[30d])) / sum(increase(http_requests_total[30d])))",
            "legendFormat": "Availability (30d)"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "decimals": 3,
            "thresholds": {
              "steps": [
                { "color": "red", "value": null },
                { "color": "yellow", "value": 0.999 },
                { "color": "green", "value": 0.9995 }
              ]
            }
          }
        }
      },
      {
        "title": "Error Budget Remaining",
        "type": "gauge",
        "gridPos": { "x": 0, "y": 4, "w": 8, "h": 8 },
        "targets": [
          {
            "expr": "1 - ((sum(increase(http_requests_total{status=~\"5..\"}[30d])) / sum(increase(http_requests_total[30d]))) / (1 - 0.999))"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "min": 0,
            "max": 1,
            "thresholds": {
              "steps": [
                { "color": "red", "value": null },
                { "color": "yellow", "value": 0.25 },
                { "color": "green", "value": 0.5 }
              ]
            }
          }
        }
      },
      {
        "title": "Error Budget Burn Rate",
        "type": "timeseries",
        "gridPos": { "x": 8, "y": 4, "w": 16, "h": 8 },
        "targets": [
          {
            "expr": "(sum(rate(http_requests_total{status=~\"5..\"}[1h])) / sum(rate(http_requests_total[1h]))) / (1 - 0.999)",
            "legendFormat": "Burn Rate (1 = budget for period)"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "custom": {
              "thresholdsStyle": { "mode": "line" }
            },
            "thresholds": {
              "steps": [
                { "color": "green", "value": null },
                { "color": "red", "value": 1 }
              ]
            }
          }
        }
      },
      {
        "title": "Availability Over Time",
        "type": "timeseries",
        "gridPos": { "x": 0, "y": 12, "w": 24, "h": 8 },
        "targets": [
          {
            "expr": "1 - (sum(rate(http_requests_total{status=~\"5..\"}[1h])) / sum(rate(http_requests_total[1h])))",
            "legendFormat": "Availability (1h rolling)"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "min": 0.99,
            "max": 1,
            "custom": {
              "thresholdsStyle": { "mode": "line" }
            },
            "thresholds": {
              "steps": [
                { "color": "red", "value": null },
                { "color": "green", "value": 0.999 }
              ]
            }
          }
        }
      }
    ]
  }
}
```

## 4. Infrastructure Dashboard

**Purpose**: Monitor underlying infrastructure health

```json
{
  "dashboard": {
    "title": "Infrastructure Overview",
    "panels": [
      {
        "title": "Node Health",
        "type": "stat",
        "targets": [{ "expr": "count(up{job=\"node-exporter\"} == 1)" }]
      },
      {
        "title": "CPU Usage by Node",
        "type": "timeseries",
        "targets": [
          {
            "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "{{ instance }}"
          }
        ]
      },
      {
        "title": "Memory Usage by Node",
        "type": "timeseries",
        "targets": [
          {
            "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
            "legendFormat": "{{ instance }}"
          }
        ]
      },
      {
        "title": "Disk Usage by Node",
        "type": "timeseries",
        "targets": [
          {
            "expr": "(1 - (node_filesystem_avail_bytes{mountpoint=\"/\"} / node_filesystem_size_bytes{mountpoint=\"/\"})) * 100",
            "legendFormat": "{{ instance }}"
          }
        ]
      },
      {
        "title": "Network I/O",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(node_network_receive_bytes_total[5m])",
            "legendFormat": "{{ instance }} RX"
          },
          {
            "expr": "rate(node_network_transmit_bytes_total[5m])",
            "legendFormat": "{{ instance }} TX"
          }
        ]
      }
    ]
  }
}
```

## 5. Database Dashboard

**Purpose**: Monitor database performance and health

```yaml
panels:
  - title: "Connection Pool"
    queries:
      - "pg_stat_activity_count"
      - "pg_settings_max_connections"

  - title: "Query Performance"
    queries:
      - "rate(pg_stat_statements_seconds_total[5m]) / rate(pg_stat_statements_calls_total[5m])"

  - title: "Cache Hit Ratio"
    queries:
      - "pg_stat_database_blks_hit / (pg_stat_database_blks_hit + pg_stat_database_blks_read)"

  - title: "Replication Lag"
    queries:
      - "pg_replication_lag_seconds"

  - title: "Table Sizes"
    queries:
      - "pg_total_relation_size_bytes"

  - title: "Index Usage"
    queries:
      - "pg_stat_user_indexes_idx_scan"
```

## Dashboard Best Practices

```yaml
design_principles:
  visual_hierarchy:
    - "Most critical metrics at the top"
    - "Use stat panels for current values"
    - "Use timeseries for trends"
    - "Use heatmaps for distributions"

  actionable:
    - "Every panel should answer a specific question"
    - "Include thresholds that indicate when action is needed"
    - "Link to runbooks for problem areas"

  performance:
    - "Limit to 15-20 panels per dashboard"
    - "Use appropriate time ranges (not too long)"
    - "Avoid expensive queries on overview dashboards"

  consistency:
    - "Use consistent color coding across dashboards"
    - "Green = good, Yellow = warning, Red = critical"
    - "Use same units and formatting"

panel_types:
  stat: "Current value, trend indicator"
  gauge: "Progress toward threshold"
  timeseries: "Historical trends"
  heatmap: "Distribution over time"
  table: "Detailed breakdown"
  logs: "Log search integration"
```

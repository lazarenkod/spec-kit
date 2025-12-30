# Observability Setup Skill

## Purpose

Configure production observability stack including OpenTelemetry instrumentation, metrics collection, distributed tracing, logging, dashboards, and alerting.

## Trigger

- User deploys a service to production
- User wants to set up monitoring
- User needs to troubleshoot production issues
- After `/speckit.ship` completes

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `service_name` | Yes | Name of the service to instrument |
| `stack` | Yes | Technology stack (node, python, go, java) |
| `deployment` | No | Deployment target (kubernetes, docker, serverless) |
| `observability_backend` | No | Where to send telemetry (grafana-cloud, self-hosted, datadog) |

## Skill Execution

### Step 1: Detect Stack and Dependencies

```yaml
stack_detection:
  runtime: "{{detected_runtime}}"
  framework: "{{detected_framework}}"
  database: "{{detected_database}}"
  cache: "{{detected_cache}}"
  message_queue: "{{detected_mq}}"

instrumentation_needed:
  auto:
    - http
    - "{{framework}}"
    - "{{database}}"
    - "{{cache}}"
  manual:
    - business_logic_spans
    - custom_metrics
```

### Step 2: Generate OpenTelemetry Instrumentation

#### Node.js

```typescript
// src/lib/telemetry.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const resource = new Resource({
  [SemanticResourceAttributes.SERVICE_NAME]: '{{service_name}}',
  [SemanticResourceAttributes.SERVICE_VERSION]: process.env.npm_package_version,
  [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV,
});

const sdk = new NodeSDK({
  resource,
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT + '/v1/traces',
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT + '/v1/metrics',
    }),
    exportIntervalMillis: 60000,
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-fs': { enabled: false },
    }),
  ],
});

sdk.start();

process.on('SIGTERM', () => {
  sdk.shutdown()
    .then(() => console.log('Telemetry shutdown complete'))
    .catch((err) => console.error('Telemetry shutdown error', err))
    .finally(() => process.exit(0));
});

export { sdk };
```

#### Python

```python
# src/telemetry.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.instrumentation.auto_instrumentation import sitecustomize
import os

resource = Resource(attributes={
    SERVICE_NAME: "{{service_name}}",
    SERVICE_VERSION: os.getenv("APP_VERSION", "0.0.0"),
    "deployment.environment": os.getenv("ENVIRONMENT", "development"),
})

# Traces
tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") + "/v1/traces"
    ))
)
trace.set_tracer_provider(tracer_provider)

# Metrics
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") + "/v1/metrics"
    ),
    export_interval_millis=60000,
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
```

### Step 3: Generate Docker Compose Observability Stack

```yaml
# infra/observability/docker-compose.yml
version: '3.8'

services:
  # OpenTelemetry Collector
  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
      - "8888:8888"   # Prometheus metrics
    depends_on:
      - jaeger
      - prometheus

  # Traces
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "14268:14268"  # Collector HTTP
    environment:
      - COLLECTOR_OTLP_ENABLED=true

  # Metrics
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"

  # Logs
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml
    volumes:
      - loki_data:/loki

  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
      - ./promtail-config.yml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml

  # Visualization
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    depends_on:
      - prometheus
      - loki
      - jaeger

  # Alerting
  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml

volumes:
  prometheus_data:
  loki_data:
  grafana_data:
```

### Step 4: Generate OTel Collector Config

```yaml
# infra/observability/otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

  memory_limiter:
    check_interval: 1s
    limit_mib: 512

  resource:
    attributes:
      - key: service.instance.id
        from_attribute: host.name
        action: insert

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

  prometheus:
    endpoint: "0.0.0.0:8889"
    namespace: "{{service_name}}"

  loki:
    endpoint: http://loki:3100/loki/api/v1/push
    labels:
      attributes:
        service.name: "service"
        level: "level"

  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [jaeger, logging]

    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheus]

    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [loki]
```

### Step 5: Generate Dashboards

Reference `templates/shared/monitor/dashboard-templates.md` to generate:

1. **Service Overview Dashboard** - Golden signals for all services
2. **Service Deep Dive Dashboard** - Detailed view per service
3. **SLO Dashboard** - Error budget tracking
4. **Infrastructure Dashboard** - Node/container health

### Step 6: Generate Alerting Rules

Reference `templates/shared/monitor/alerting-rules.md` to generate:

1. **Golden signal alerts** - Latency, errors, traffic, saturation
2. **Database alerts** - Connections, slow queries, replication
3. **SLO alerts** - Error budget burn rate
4. **Infrastructure alerts** - CPU, memory, disk

### Step 7: Generate Runbooks

Reference `templates/shared/monitor/runbooks.md` to generate runbooks for each alert.

### Step 8: Output Verification Checklist

```yaml
verification:
  instrumentation:
    - [ ] Telemetry SDK initializes without errors
    - [ ] Traces appear in Jaeger
    - [ ] Metrics appear in Prometheus
    - [ ] Logs appear in Loki

  dashboards:
    - [ ] All dashboards load without errors
    - [ ] Metrics populate correctly
    - [ ] Links between dashboards work

  alerting:
    - [ ] Test alert fires correctly
    - [ ] Alert reaches notification channel
    - [ ] Runbook link is accessible

  slo:
    - [ ] SLO targets defined
    - [ ] Error budget tracking works
    - [ ] Burn rate alerts configured
```

## Output Format

```yaml
observability_package:
  files:
    - path: "src/lib/telemetry.ts"
      content: "[OpenTelemetry SDK setup]"
    - path: "infra/observability/docker-compose.yml"
      content: "[Full observability stack]"
    - path: "infra/observability/prometheus.yml"
      content: "[Prometheus config]"
    - path: "infra/observability/alertmanager.yml"
      content: "[Alertmanager config]"
    - path: "infra/observability/rules/*.yml"
      content: "[Alert rules]"
    - path: "infra/observability/grafana/dashboards/*.json"
      content: "[Dashboard JSONs]"
    - path: "docs/runbooks/*.md"
      content: "[Runbook for each alert]"

  env_vars:
    - OTEL_EXPORTER_OTLP_ENDPOINT
    - OTEL_SERVICE_NAME

  verification:
    commands:
      - "docker-compose -f infra/observability/docker-compose.yml up -d"
      - "curl http://localhost:16686"  # Jaeger UI
      - "curl http://localhost:9090"   # Prometheus UI
      - "curl http://localhost:3000"   # Grafana UI
```

## Integration

This skill is used by:
- `/speckit.monitor` - Main observability workflow
- `/speckit.ship` - Post-deployment verification

References:
- `templates/shared/monitor/alerting-rules.md`
- `templates/shared/monitor/dashboard-templates.md`
- `templates/shared/monitor/runbooks.md`
- `templates/personas/devops-agent.md`

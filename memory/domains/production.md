# Domain Extension: Production Readiness (Layer 1)

**Extends**: constitution.base.md v1.0
**Regulatory Context**: SOC 2, ISO 27001, GDPR (operational requirements), SLA compliance
**Typical Projects**: SaaS, APIs, microservices, any production workload
**Philosophy**: "If it's not observable, it's not production-ready"

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Observability** | Ability to understand system state from external outputs (logs, metrics, traces) |
| **OpenTelemetry** | CNCF standard for vendor-neutral instrumentation (traces, metrics, logs) |
| **Trace Context** | W3C standard for distributed trace propagation (traceId, spanId) |
| **Health Probes** | Kubernetes-style liveness and readiness endpoints |
| **Graceful Shutdown** | Clean termination handling SIGTERM with connection draining |
| **Self-Hosted Stack** | Observability infrastructure under your control (GlitchTip, Prometheus, Jaeger) |

---

## Open Source Stack (No Paid APIs)

| Category | Paid Alternative | Open Source Choice | Rationale |
|----------|------------------|-------------------|-----------|
| Error Tracking | Sentry ($29+/mo) | **GlitchTip** | Sentry-compatible API, drop-in replacement |
| Analytics | PostHog ($0-450/mo) | **Umami** | Privacy-first, GDPR compliant, lightweight |
| Metrics | Datadog ($15/host) | **VictoriaMetrics + Grafana** | Prometheus-compatible, 10x more efficient storage |
| Tracing | Honeycomb ($100+/mo) | **Jaeger v2** | OpenTelemetry-native, CNCF graduated |
| Logs | Splunk ($150+/GB) | **Loki + Grafana** | Label-indexed, cost-effective |
| Logging Library | - | **Pino** (Node) / **structlog** (Python) | 5-10x faster, JSON native |
| Instrumentation | - | **OpenTelemetry** | CNCF standard, vendor-neutral |

---

## Strengthened Principles

These principles from `constitution.base.md` are elevated or enhanced for production:

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| OBS-001 | MUST | MUST (with trace context) | All logs must include traceId/spanId |
| OBS-002 | MUST | MUST (with GlitchTip) | Error tracking via open-source stack |
| OBS-003 | SHOULD | MUST | Health endpoints mandatory in production |
| OBS-004 | SHOULD | MUST | Metrics mandatory for SLA compliance |
| SEC-001 | MUST | MUST (with rotation) | Secrets must have rotation policy |
| TFA-001 | MUST | MUST (with validation) | Config validated at startup |

---

## Additional Principles

### PRD-001: OpenTelemetry-First Architecture

**Level**: MUST
**Applies to**: All production services

All observability instrumentation MUST use OpenTelemetry SDK. No proprietary vendor SDKs.

**Implementation**:
```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-grpc';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter(),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter(),
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

**Validation**: All imports resolve to `@opentelemetry/*` packages
**Violations**: HIGH - Vendor lock-in, migration cost

---

### PRD-002: Structured Logging with Correlation

**Level**: MUST
**Applies to**: All logging output

Logs MUST be JSON-formatted and include trace context (traceId, spanId, service, version).

**Implementation**:
```typescript
import pino from 'pino';
import { trace } from '@opentelemetry/api';

const logger = pino({
  formatters: {
    level: (label) => ({ level: label }),
  },
  mixin() {
    const span = trace.getActiveSpan();
    return {
      traceId: span?.spanContext().traceId,
      spanId: span?.spanContext().spanId,
      service: process.env.SERVICE_NAME,
      version: process.env.SERVICE_VERSION,
    };
  }
});
```

**Python equivalent**:
```python
import structlog
from opentelemetry import trace

def add_trace_context(logger, method_name, event_dict):
    span = trace.get_current_span()
    if span:
        ctx = span.get_span_context()
        event_dict['trace_id'] = format(ctx.trace_id, '032x')
        event_dict['span_id'] = format(ctx.span_id, '016x')
    return event_dict

structlog.configure(processors=[add_trace_context, structlog.processors.JSONRenderer()])
```

**Validation**: `grep -r "console.log" src/` returns 0 matches in production code
**Violations**: HIGH - Debugging impossible without correlation

---

### PRD-003: Health Endpoints

**Level**: MUST
**Applies to**: All HTTP services

Services MUST expose `/health` (liveness) and `/ready` (readiness) endpoints.

**Implementation**:
```typescript
// /health - basic liveness (returns 200 if process running)
app.get('/health', (req, res) => res.json({ status: 'ok', timestamp: new Date().toISOString() }));

// /ready - readiness with dependency checks
app.get('/ready', async (req, res) => {
  const checks = await Promise.allSettled([
    checkDatabase(),
    checkCache(),
    checkExternalAPIs(),
  ]);

  const results = checks.map((check, i) => ({
    name: ['database', 'cache', 'external'][i],
    healthy: check.status === 'fulfilled' && check.value,
    latency: check.status === 'fulfilled' ? check.value.latency : null,
  }));

  const healthy = results.every(r => r.healthy);
  res.status(healthy ? 200 : 503).json({
    status: healthy ? 'ready' : 'degraded',
    checks: results
  });
});
```

**Validation**: `curl /health` returns 200, `curl /ready` returns dependency status
**Violations**: CRITICAL - Kubernetes cannot manage service lifecycle

---

### PRD-004: Prometheus Metrics Export

**Level**: MUST
**Applies to**: All production services

Services MUST export metrics in Prometheus format at `/metrics` endpoint.

**Required Metrics**:
- `http_request_duration_seconds` (histogram by method, path, status)
- `http_requests_total` (counter by status, method, path)
- `process_cpu_seconds_total`
- `process_resident_memory_bytes`
- `nodejs_heap_size_bytes` / language-specific runtime metrics
- Custom business metrics (e.g., `orders_processed_total`)

**Implementation**:
```typescript
import { PrometheusExporter } from '@opentelemetry/exporter-prometheus';

const exporter = new PrometheusExporter({ port: 9464 });
// Or use express-prom-bundle for Express apps
```

**Validation**: `curl /metrics` returns valid Prometheus format
**Violations**: HIGH - No visibility into service health

---

### PRD-005: Graceful Shutdown

**Level**: MUST
**Applies to**: All services

Services MUST handle SIGTERM gracefully:
1. Stop accepting new requests immediately
2. Complete in-flight requests (30s timeout)
3. Close database connections
4. Flush telemetry buffers
5. Exit with code 0

**Implementation**:
```typescript
let isShuttingDown = false;

process.on('SIGTERM', async () => {
  if (isShuttingDown) return;
  isShuttingDown = true;

  logger.info('SIGTERM received, starting graceful shutdown');

  // Stop accepting new connections
  server.close(async () => {
    logger.info('HTTP server closed');

    // Cleanup in order
    await Promise.allSettled([
      db.disconnect(),
      redis.quit(),
      sdk.shutdown(), // OpenTelemetry flush
    ]);

    logger.info('Cleanup complete, exiting');
    process.exit(0);
  });

  // Force exit after timeout
  setTimeout(() => {
    logger.error('Graceful shutdown timeout, forcing exit');
    process.exit(1);
  }, 30000);
});
```

**Validation**: `kill -TERM <pid>` completes without data loss
**Violations**: CRITICAL - Data loss, zombie connections, deployment failures

---

### PRD-006: Error Tracking with Context

**Level**: MUST
**Applies to**: All error handling

Exceptions MUST be recorded to span and sent to error tracking service (GlitchTip) with context.

**Implementation**:
```typescript
import * as Sentry from "@sentry/node"; // Works with GlitchTip
import { trace, SpanStatusCode } from '@opentelemetry/api';

// Initialize with GlitchTip DSN
Sentry.init({
  dsn: process.env.GLITCHTIP_DSN, // e.g., https://key@glitchtip.example.com/1
  environment: process.env.NODE_ENV,
  release: process.env.SERVICE_VERSION,
});

// Error handling wrapper
async function withErrorTracking<T>(
  operation: () => Promise<T>,
  context: Record<string, unknown>
): Promise<T> {
  const span = trace.getActiveSpan();
  try {
    return await operation();
  } catch (error) {
    span?.recordException(error);
    span?.setStatus({ code: SpanStatusCode.ERROR, message: error.message });

    Sentry.captureException(error, {
      extra: context,
      tags: { traceId: span?.spanContext().traceId },
    });

    throw error;
  }
}
```

**Validation**: Errors appear in GlitchTip with stack trace and context
**Violations**: HIGH - Silent failures in production

---

### PRD-007: Distributed Tracing

**Level**: MUST
**Applies to**: All inter-service communication

All HTTP/gRPC calls MUST propagate trace context using W3C Trace Context format.

**Implementation**: Auto-instrumentation via `@opentelemetry/auto-instrumentations-node` handles:
- HTTP client/server (fetch, axios, express, fastify)
- Database clients (pg, mysql, mongodb, redis)
- Message queues (amqp, kafka)
- gRPC

**Manual propagation** (if needed):
```typescript
import { propagation, context } from '@opentelemetry/api';

// Inject into outgoing request
const headers = {};
propagation.inject(context.active(), headers);
await fetch(url, { headers });

// Extract from incoming request
const ctx = propagation.extract(context.active(), req.headers);
context.with(ctx, () => handleRequest(req, res));
```

**Validation**: Jaeger shows complete trace across services
**Violations**: HIGH - Cannot debug distributed systems

---

### PRD-008: Configuration Validation

**Level**: MUST
**Applies to**: Application startup

All required configuration MUST be validated at startup. Missing or invalid config = fail fast with clear error.

**Implementation**:
```typescript
import { z } from 'zod';

const envSchema = z.object({
  // Required
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  SERVICE_NAME: z.string().min(1),
  SERVICE_VERSION: z.string().default('unknown'),

  // Observability
  OTEL_EXPORTER_OTLP_ENDPOINT: z.string().url(),
  GLITCHTIP_DSN: z.string().url().optional(),

  // Environment
  NODE_ENV: z.enum(['development', 'staging', 'production']).default('development'),
  PORT: z.coerce.number().default(3000),
});

// Parse at startup - throws with detailed error if invalid
export const env = envSchema.parse(process.env);
```

**Python equivalent**:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    service_name: str
    otel_exporter_otlp_endpoint: str

settings = Settings()  # Validates on import
```

**Validation**: App fails to start with clear error if config missing
**Violations**: CRITICAL - Runtime failures from missing config

---

### PRD-009: Self-Hosted Observability

**Level**: SHOULD
**Applies to**: Data governance requirements

Observability data SHOULD be stored self-hosted for data sovereignty and cost control.

**Stack**:
- **GlitchTip**: Error tracking (Sentry-compatible)
- **VictoriaMetrics**: Metrics storage (Prometheus-compatible, 10x more efficient)
- **Jaeger v2**: Distributed tracing
- **Loki**: Log aggregation
- **Grafana**: Unified dashboards
- **Umami**: Privacy-first analytics

**Architecture**:
```
App → OpenTelemetry Collector → Jaeger (traces)
                             → VictoriaMetrics (metrics)
                             → Loki (logs)
                                     ↓
                                 Grafana (visualization)
```

**Validation**: No external SaaS observability endpoints in config
**Violations**: MEDIUM - Data leaves infrastructure, ongoing costs

---

### PRD-010: Dashboard as Code

**Level**: SHOULD
**Applies to**: Grafana dashboards

Dashboards SHOULD be defined as code (JSON/YAML) and version-controlled.

**Implementation**:
```yaml
# grafana/provisioning/dashboards/dashboard.yml
apiVersion: 1
providers:
  - name: 'default'
    folder: ''
    type: file
    options:
      path: /etc/grafana/provisioning/dashboards
```

**Directory structure**:
```
observability/
├── docker-compose.yml
├── otel-collector-config.yml
├── prometheus/
│   └── prometheus.yml
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── datasources.yml
│       └── dashboards/
│           ├── dashboard.yml
│           └── service-overview.json
└── alertmanager/
    └── alertmanager.yml
```

**Validation**: Dashboards auto-load on container start
**Violations**: LOW - Dashboard drift, manual recreation needed

---

## Architecture Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                        Application                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Pino Logger  │  │ OTel Traces  │  │ OTel Metrics │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼─────────────────┼─────────────────┼───────────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              OpenTelemetry Collector (central hub)               │
│  receivers: otlp (gRPC:4317, HTTP:4318)                         │
│  exporters: jaeger, prometheus, loki                            │
└─────────┬─────────────────┬─────────────────┬───────────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
    ┌─────────┐       ┌───────────┐     ┌─────────┐
    │  Loki   │       │  Jaeger   │     │Prometheus│
    │ (logs)  │       │ (traces)  │     │(metrics) │
    └────┬────┘       └─────┬─────┘     └────┬─────┘
         │                  │                │
         └──────────────────┼────────────────┘
                            ▼
                    ┌───────────────┐
                    │   Grafana     │ ← Unified dashboards
                    │  (visualize)  │
                    └───────────────┘

    ┌─────────────┐              ┌─────────────┐
    │  GlitchTip  │ ← Errors     │   Umami     │ ← Analytics
    │ (Sentry API)│              │  (privacy)  │
    └─────────────┘              └─────────────┘
```

---

## Performance Thresholds

| Metric | Target | SLA-Critical |
|--------|--------|--------------|
| Error Rate | < 0.1% | < 1% |
| P99 Latency | < 500ms | < 2s |
| Health Check Latency | < 50ms | < 200ms |
| Metrics Scrape | < 100ms | < 500ms |
| Log Shipping Lag | < 5s | < 30s |
| Trace Sampling | 100% errors, 10% success | 100% errors |

---

## Summary

| Type | Count |
|------|-------|
| Strengthened from base | 6 |
| New MUST principles | 8 |
| New SHOULD principles | 2 |
| **Total additional requirements** | **16** |

---

## When to Use

Apply this domain extension when:
- Deploying to production environments
- Operating services with SLA commitments
- Building microservices architectures
- Requiring SOC 2 / ISO 27001 compliance
- Managing infrastructure costs (self-hosted vs SaaS)

---

## Combining with Other Domains

| Combined With | Notes |
|---------------|-------|
| **SaaS** | Multi-tenant: add tenant_id to all observability context |
| **Mobile** | Backend APIs: production domain for server, mobile domain for client |
| **Gaming** | Game servers: add PRD metrics for player sessions, matchmaking |
| **E-Commerce** | Shopping: add business metrics (cart, checkout, revenue) |
| **FinTech** | Financial: extend with audit logging and PCI compliance |

---

## Usage

```bash
# Activate production domain
cp memory/domains/production.md memory/constitution.domain.md

# Or combine with other domains
cat memory/domains/saas.md memory/domains/production.md > memory/constitution.domain.md
```

Then customize `constitution.domain.md` for your specific deployment, adjusting thresholds and tool choices as needed.

---

## Related Templates

- `templates/shared/observability-stack.md` - Docker Compose for full self-hosted stack
- `templates/shared/otel-integration.md` - Language-specific OpenTelemetry setup guides

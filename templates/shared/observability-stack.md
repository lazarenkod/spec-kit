# Open Source Observability Stack

**Related Domain**: `memory/domains/production.md`
**Philosophy**: Self-hosted, vendor-neutral, cost-effective observability

This template provides a complete Docker Compose stack for production-grade observability without paid SaaS dependencies.

---

## Stack Overview

| Component | Purpose | Port | URL |
|-----------|---------|------|-----|
| OpenTelemetry Collector | Central telemetry hub | 4317 (gRPC), 4318 (HTTP) | - |
| Jaeger | Distributed tracing | 16686 | <http://localhost:16686> |
| VictoriaMetrics | Metrics storage | 8428 | <http://localhost:8428> |
| Grafana | Dashboards | 3001 | <http://localhost:3001> |
| Loki | Log aggregation | 3100 | - |
| GlitchTip | Error tracking | 8000 | <http://localhost:8000> |
| Umami | Privacy-first web analytics | 3002 | <http://localhost:3002> |
| PostHog | Product analytics (self-hosted) | 8001 | <http://localhost:8001> |
| PostgreSQL | Database for GlitchTip/Umami/PostHog | 5432 | - |
| Redis | Cache for GlitchTip/PostHog | 6379 | - |

---

## Quick Start

```bash
# Create observability directory
mkdir -p observability && cd observability

# Copy files from this template
# Then start the stack
docker compose up -d

# Access dashboards
open http://localhost:3001  # Grafana (admin/admin)
open http://localhost:16686 # Jaeger
open http://localhost:8000  # GlitchTip
open http://localhost:3002  # Umami
open http://localhost:8001  # PostHog (if enabled)
```

---

## Analytics Services

### Web Analytics (Umami)
- **Purpose**: Privacy-first web analytics for page views, sessions, traffic sources
- **Port**: 3002 (http://localhost:3002)
- **Default Credentials**: admin / umami
- **Included**: Always (if analytics_enabled == true)

### Product Analytics (PostHog)
- **Purpose**: User behavior tracking, event funnels, session recording
- **Port**: 8001 (http://localhost:8001)
- **Included**: Only if analytics_provider == "posthog" (self-hosted)
- **Cloud Alternative**: Use PostHog Cloud (app.posthog.com) - no Docker service needed

### Product Analytics (Mixpanel / Amplitude)
- **Purpose**: User behavior tracking, funnels, cohorts
- **Included**: No Docker service - cloud-only providers
- **Setup**: Add API key to environment variables, use SDK

---

## docker-compose.yml

```yaml
version: '3.8'

services:
  # ============================================
  # OpenTelemetry Collector - Central Hub
  # ============================================
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.92.0
    container_name: otel-collector
    command: ["--config=/etc/otel-collector-config.yml"]
    volumes:
      - ./otel-collector-config.yml:/etc/otel-collector-config.yml:ro
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
      - "8888:8888"   # Prometheus metrics (self)
    depends_on:
      - jaeger
      - loki
    networks:
      - observability
    restart: unless-stopped

  # ============================================
  # Jaeger - Distributed Tracing
  # ============================================
  jaeger:
    image: jaegertracing/all-in-one:1.53
    container_name: jaeger
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    ports:
      - "16686:16686" # UI
      - "14268:14268" # HTTP collector
      - "14250:14250" # gRPC collector
    networks:
      - observability
    restart: unless-stopped

  # ============================================
  # VictoriaMetrics - Metrics Storage
  # Prometheus-compatible, 10x more efficient
  # ============================================
  victoriametrics:
    image: victoriametrics/victoria-metrics:v1.96.0
    container_name: victoriametrics
    command:
      - '--storageDataPath=/victoria-metrics-data'
      - '--httpListenAddr=:8428'
      - '--retentionPeriod=90d'
      - '--search.latencyOffset=0s'
    volumes:
      - victoriametrics_data:/victoria-metrics-data
    ports:
      - "8428:8428"
    networks:
      - observability
    restart: unless-stopped

  # ============================================
  # Loki - Log Aggregation
  # ============================================
  loki:
    image: grafana/loki:2.9.3
    container_name: loki
    command: -config.file=/etc/loki/loki-config.yml
    volumes:
      - ./loki/loki-config.yml:/etc/loki/loki-config.yml:ro
      - loki_data:/loki
    ports:
      - "3100:3100"
    networks:
      - observability
    restart: unless-stopped

  # ============================================
  # Grafana - Unified Dashboards
  # ============================================
  grafana:
    image: grafana/grafana:10.2.3
    container_name: grafana
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - grafana_data:/var/lib/grafana
    ports:
      - "3001:3000"
    depends_on:
      - victoriametrics
      - loki
      - jaeger
    networks:
      - observability
    restart: unless-stopped

  # ============================================
  # GlitchTip - Error Tracking (Sentry-compatible)
  # ============================================
  glitchtip-postgres:
    image: postgres:15-alpine
    container_name: glitchtip-postgres
    environment:
      POSTGRES_DB: glitchtip
      POSTGRES_USER: glitchtip
      POSTGRES_PASSWORD: glitchtip_secret
    volumes:
      - glitchtip_postgres_data:/var/lib/postgresql/data
    networks:
      - observability
    restart: unless-stopped

  glitchtip-redis:
    image: redis:7-alpine
    container_name: glitchtip-redis
    networks:
      - observability
    restart: unless-stopped

  glitchtip-web:
    image: glitchtip/glitchtip:v4.0
    container_name: glitchtip-web
    environment:
      DATABASE_URL: postgres://glitchtip:glitchtip_secret@glitchtip-postgres:5432/glitchtip
      REDIS_URL: redis://glitchtip-redis:6379/0
      SECRET_KEY: ${GLITCHTIP_SECRET_KEY:-change-me-in-production}
      PORT: 8000
      EMAIL_URL: ${EMAIL_URL:-consolemail://}
      GLITCHTIP_DOMAIN: ${GLITCHTIP_DOMAIN:-http://localhost:8000}
      DEFAULT_FROM_EMAIL: ${DEFAULT_FROM_EMAIL:-noreply@localhost}
      CELERY_WORKER_AUTOSCALE: "1,3"
      ENABLE_OPEN_USER_REGISTRATION: "True"
    ports:
      - "8000:8000"
    depends_on:
      - glitchtip-postgres
      - glitchtip-redis
    networks:
      - observability
    restart: unless-stopped

  glitchtip-worker:
    image: glitchtip/glitchtip:v4.0
    container_name: glitchtip-worker
    command: ./bin/run-celery-with-beat.sh
    environment:
      DATABASE_URL: postgres://glitchtip:glitchtip_secret@glitchtip-postgres:5432/glitchtip
      REDIS_URL: redis://glitchtip-redis:6379/0
      SECRET_KEY: ${GLITCHTIP_SECRET_KEY:-change-me-in-production}
    depends_on:
      - glitchtip-postgres
      - glitchtip-redis
    networks:
      - observability
    restart: unless-stopped

  # ============================================
  # Umami - Privacy-First Analytics
  # ============================================
  umami-postgres:
    image: postgres:15-alpine
    container_name: umami-postgres
    environment:
      POSTGRES_DB: umami
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: umami_secret
    volumes:
      - umami_postgres_data:/var/lib/postgresql/data
    networks:
      - observability
    restart: unless-stopped

  umami:
    image: ghcr.io/umami-software/umami:postgresql-v2.10.1
    container_name: umami
    environment:
      DATABASE_URL: postgres://umami:umami_secret@umami-postgres:5432/umami
      DATABASE_TYPE: postgresql
      APP_SECRET: ${UMAMI_APP_SECRET:-change-me-in-production}
    ports:
      - "3002:3000"
    depends_on:
      - umami-postgres
    networks:
      - observability
    restart: unless-stopped

  # ============================================
  # PostHog - Product Analytics (Self-Hosted)
  # CONDITION: Include this service only if:
  #   - analytics_enabled == true (from constitution)
  #   - "product" in analytics_types
  #   - analytics_provider == "posthog"
  # ============================================
  posthog-postgres:
    image: postgres:15-alpine
    container_name: posthog-postgres
    environment:
      POSTGRES_DB: posthog
      POSTGRES_USER: posthog
      POSTGRES_PASSWORD: posthog_secret
    volumes:
      - posthog_postgres_data:/var/lib/postgresql/data
    networks:
      - observability
    restart: unless-stopped

  posthog-redis:
    image: redis:7-alpine
    container_name: posthog-redis
    networks:
      - observability
    restart: unless-stopped

  posthog:
    image: posthog/posthog:latest
    container_name: posthog
    environment:
      - DATABASE_URL=postgres://posthog:posthog_secret@posthog-postgres:5432/posthog
      - REDIS_URL=redis://posthog-redis:6379/
      - SECRET_KEY=${POSTHOG_SECRET_KEY:-random-secret-key-change-in-production}
      - IS_BEHIND_PROXY=true
      - DISABLE_SECURE_SSL_REDIRECT=true
    ports:
      - "8001:8000"
    depends_on:
      - posthog-postgres
      - posthog-redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/_health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
    networks:
      - observability
    restart: unless-stopped
    volumes:
      - posthog-data:/var/lib/posthog

  posthog-worker:
    image: posthog/posthog:latest
    container_name: posthog-worker
    command: ["./bin/docker-worker"]
    environment:
      - DATABASE_URL=postgres://posthog:posthog_secret@posthog-postgres:5432/posthog
      - REDIS_URL=redis://posthog-redis:6379/
      - SECRET_KEY=${POSTHOG_SECRET_KEY:-random-secret-key-change-in-production}
    depends_on:
      - posthog-postgres
      - posthog-redis
    networks:
      - observability
    restart: unless-stopped

networks:
  observability:
    driver: bridge

volumes:
  victoriametrics_data:
  loki_data:
  grafana_data:
  glitchtip_postgres_data:
  umami_postgres_data:
  posthog_postgres_data:
  posthog-data:
```

---

## Configuration Files

### otel-collector-config.yml

```yaml
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
    limit_mib: 1000
    spike_limit_mib: 200

  resource:
    attributes:
      - key: deployment.environment
        value: ${OTEL_RESOURCE_ATTRIBUTES_ENVIRONMENT:-development}
        action: upsert

exporters:
  # Traces to Jaeger
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true

  # Metrics to VictoriaMetrics (Prometheus-compatible)
  prometheusremotewrite:
    endpoint: http://victoriametrics:8428/api/v1/write

  # Logs to Loki
  loki:
    endpoint: http://loki:3100/loki/api/v1/push
    labels:
      resource:
        service.name: "service_name"
        service.version: "service_version"
      attributes:
        level: ""
        trace_id: ""

  # Debug output (development only)
  debug:
    verbosity: detailed

extensions:
  health_check:
    endpoint: 0.0.0.0:13133

service:
  extensions: [health_check]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp/jaeger]

    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheusremotewrite]

    logs:
      receivers: [otlp]
      processors: [memory_limiter, resource, batch]
      exporters: [loki]
```

---

### VictoriaMetrics Configuration

VictoriaMetrics is configured via command-line flags in docker-compose.yml.
For scraping (optional), use vmagent:

```yaml
# Optional: vmagent for active scraping (if not using OTel push)
# Add to docker-compose.yml if you need Prometheus-style scraping

# vmagent:
#   image: victoriametrics/vmagent:v1.96.0
#   container_name: vmagent
#   command:
#     - '--promscrape.config=/etc/vmagent/scrape.yml'
#     - '--remoteWrite.url=http://victoriametrics:8428/api/v1/write'
#   volumes:
#     - ./vmagent/scrape.yml:/etc/vmagent/scrape.yml:ro
#   networks:
#     - observability
```

**Note**: With OpenTelemetry Collector, metrics are pushed directly to VictoriaMetrics.
vmagent is only needed if you also need to scrape Prometheus endpoints.

---

### loki/loki-config.yml

```yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  instance_addr: 127.0.0.1
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

query_range:
  results_cache:
    cache:
      embedded_cache:
        enabled: true
        max_size_mb: 100

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

ruler:
  alertmanager_url: http://localhost:9093

limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h
  ingestion_rate_mb: 16
  ingestion_burst_size_mb: 24

analytics:
  reporting_enabled: false
```

---

### grafana/provisioning/datasources/datasources.yml

```yaml
apiVersion: 1

datasources:
  - name: VictoriaMetrics
    type: prometheus
    access: proxy
    url: http://victoriametrics:8428
    isDefault: true
    editable: false

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: false
    jsonData:
      derivedFields:
        - name: TraceID
          matcherRegex: '"traceId":"(\w+)"'
          url: '$${__value.raw}'
          datasourceUid: jaeger
          urlDisplayLabel: View Trace

  - name: Jaeger
    type: jaeger
    access: proxy
    url: http://jaeger:16686
    uid: jaeger
    editable: false
```

---

### grafana/provisioning/dashboards/dashboard.yml

```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    folderUid: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 30
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
```

---

## Environment Variables

Create a `.env` file for production:

```bash
# GlitchTip
GLITCHTIP_SECRET_KEY=your-secret-key-here-min-32-chars
GLITCHTIP_DOMAIN=https://errors.yourdomain.com
EMAIL_URL=smtp://user:password@smtp.example.com:587
DEFAULT_FROM_EMAIL=errors@yourdomain.com

# Umami
UMAMI_APP_SECRET=your-umami-secret-here

# PostHog (self-hosted only)
POSTHOG_SECRET_KEY=your-posthog-secret-key-change-in-production

# OpenTelemetry
OTEL_RESOURCE_ATTRIBUTES_ENVIRONMENT=production
```

---

## Application Integration

### Required Environment Variables

```bash
# Service identification
SERVICE_NAME=my-api
SERVICE_VERSION=1.0.0

# OpenTelemetry
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_SERVICE_NAME=${SERVICE_NAME}

# GlitchTip DSN (get from GlitchTip after setup)
GLITCHTIP_DSN=http://key@glitchtip-web:8000/1

# Logging
LOG_LEVEL=info
```

### Connecting Your Application

```yaml
# Add to your application's docker-compose.yml
services:
  my-api:
    environment:
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
      - GLITCHTIP_DSN=http://key@glitchtip-web:8000/1
    networks:
      - observability  # Same network as observability stack
```

---

## Health Checks

Verify the stack is running:

```bash
# All services
docker compose ps

# Jaeger UI
curl -s http://localhost:16686/api/services | jq

# VictoriaMetrics
curl -s http://localhost:8428/-/healthy

# Loki
curl -s http://localhost:3100/ready

# Grafana
curl -s http://localhost:3001/api/health

# GlitchTip
curl -s http://localhost:8000/health/

# Umami
curl -s http://localhost:3002/api/heartbeat

# PostHog
curl -s http://localhost:8001/_health
```

---

## Production Considerations

### Resource Requirements

| Component | CPU | Memory | Storage |
|-----------|-----|--------|---------|
| OTel Collector | 0.5 | 1GB | - |
| Jaeger | 0.5 | 1GB | 10GB/week |
| VictoriaMetrics | 0.25 | 512MB | 5GB/month |
| Loki | 0.5 | 1GB | 5GB/week |
| Grafana | 0.25 | 256MB | 100MB |
| GlitchTip | 0.5 | 1GB | 5GB/month |
| Umami | 0.25 | 256MB | 1GB/month |
| PostHog | 0.5 | 1GB | 10GB/month |
| **Total** | **3.5 vCPU** | **~6.5GB** | **~50GB/month** |

### Recommended VPS

- **Development**: 2 vCPU, 4GB RAM, 50GB SSD (~$20/mo)
- **Production**: 4 vCPU, 8GB RAM, 100GB SSD (~$40/mo)

### Security Checklist

- [ ] Change all default passwords
- [ ] Enable HTTPS (use nginx/traefik as reverse proxy)
- [ ] Restrict network access to observability ports
- [ ] Set up authentication for Grafana, GlitchTip, Umami, PostHog
- [ ] Configure backup for PostgreSQL volumes (includes PostHog data)
- [ ] Set resource limits in Docker Compose

---

## Scaling

For high-volume production:

1. **Jaeger**: Use Jaeger with Elasticsearch/Cassandra backend
2. **VictoriaMetrics**: Use VictoriaMetrics Cluster for horizontal scaling
3. **Loki**: Use S3/GCS backend with multiple ingesters
4. **OTel Collector**: Run multiple instances with load balancer

---

## Related

- Domain: `memory/domains/production.md`
- Integration guide: `templates/shared/otel-integration.md`

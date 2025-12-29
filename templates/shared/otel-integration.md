# OpenTelemetry Integration Guide

**Related Domain**: `memory/domains/production.md`
**Related Stack**: `templates/shared/observability-stack.md`

This guide provides copy-paste integrations for OpenTelemetry with Pino logging across Node.js, Python, and Go.

---

## Node.js / TypeScript

### Installation

```bash
# Core OpenTelemetry
npm install @opentelemetry/sdk-node \
            @opentelemetry/auto-instrumentations-node \
            @opentelemetry/exporter-trace-otlp-grpc \
            @opentelemetry/exporter-metrics-otlp-grpc \
            @opentelemetry/sdk-metrics \
            @opentelemetry/api

# Logging
npm install pino pino-pretty

# Error tracking (Sentry SDK works with GlitchTip)
npm install @sentry/node

# Config validation
npm install zod
```

### File: `src/instrumentation.ts`

```typescript
// Must be imported FIRST before any other imports
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-grpc';
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { Resource } from '@opentelemetry/resources';
import {
  SEMRESATTRS_SERVICE_NAME,
  SEMRESATTRS_SERVICE_VERSION,
  SEMRESATTRS_DEPLOYMENT_ENVIRONMENT,
} from '@opentelemetry/semantic-conventions';

const resource = new Resource({
  [SEMRESATTRS_SERVICE_NAME]: process.env.SERVICE_NAME || 'unknown-service',
  [SEMRESATTRS_SERVICE_VERSION]: process.env.SERVICE_VERSION || '0.0.0',
  [SEMRESATTRS_DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV || 'development',
});

const sdk = new NodeSDK({
  resource,
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4317',
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4317',
    }),
    exportIntervalMillis: 15000,
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      // Disable noisy instrumentations
      '@opentelemetry/instrumentation-fs': { enabled: false },
      '@opentelemetry/instrumentation-dns': { enabled: false },
    }),
  ],
});

sdk.start();

// Graceful shutdown
process.on('SIGTERM', async () => {
  try {
    await sdk.shutdown();
    console.log('OpenTelemetry SDK shut down successfully');
  } catch (error) {
    console.error('Error shutting down OpenTelemetry SDK', error);
  }
});

export { sdk };
```

### File: `src/logger.ts`

```typescript
import pino from 'pino';
import { trace, context } from '@opentelemetry/api';

const isDevelopment = process.env.NODE_ENV !== 'production';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',

  // Pretty print in development
  transport: isDevelopment
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,

  // JSON formatting
  formatters: {
    level: (label) => ({ level: label }),
    bindings: () => ({}), // Remove pid, hostname
  },

  // Add trace context to every log
  mixin() {
    const span = trace.getActiveSpan();
    if (!span) return {};

    const spanContext = span.spanContext();
    return {
      traceId: spanContext.traceId,
      spanId: spanContext.spanId,
      service: process.env.SERVICE_NAME,
      version: process.env.SERVICE_VERSION,
    };
  },

  // Timestamp in ISO format
  timestamp: pino.stdTimeFunctions.isoTime,
});

// Child logger with request context
export function createRequestLogger(requestId: string, userId?: string) {
  return logger.child({ requestId, userId });
}

export default logger;
```

### File: `src/errors.ts`

```typescript
import * as Sentry from '@sentry/node';
import { trace, SpanStatusCode } from '@opentelemetry/api';
import logger from './logger';

// Initialize Sentry/GlitchTip
Sentry.init({
  dsn: process.env.GLITCHTIP_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.SERVICE_VERSION,
  // Don't send in development unless explicitly enabled
  enabled: process.env.NODE_ENV === 'production' || !!process.env.GLITCHTIP_DSN,
});

export interface ErrorContext {
  userId?: string;
  requestId?: string;
  action?: string;
  [key: string]: unknown;
}

export function captureError(error: Error, context: ErrorContext = {}): void {
  const span = trace.getActiveSpan();

  // Record to span
  if (span) {
    span.recordException(error);
    span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
  }

  // Log error
  logger.error({
    err: error,
    ...context,
    traceId: span?.spanContext().traceId,
  }, error.message);

  // Send to GlitchTip
  Sentry.captureException(error, {
    extra: context,
    tags: {
      traceId: span?.spanContext().traceId,
      ...context.action && { action: context.action },
    },
  });
}

// Wrapper for async operations
export async function withErrorTracking<T>(
  operation: () => Promise<T>,
  context: ErrorContext
): Promise<T> {
  try {
    return await operation();
  } catch (error) {
    captureError(error as Error, context);
    throw error;
  }
}
```

### File: `src/config.ts`

```typescript
import { z } from 'zod';

const envSchema = z.object({
  // Service identity
  SERVICE_NAME: z.string().min(1).default('my-service'),
  SERVICE_VERSION: z.string().default('0.0.0'),
  NODE_ENV: z.enum(['development', 'staging', 'production']).default('development'),

  // Server
  PORT: z.coerce.number().default(3000),
  HOST: z.string().default('0.0.0.0'),

  // Database
  DATABASE_URL: z.string().url(),

  // Redis (optional)
  REDIS_URL: z.string().url().optional(),

  // OpenTelemetry
  OTEL_EXPORTER_OTLP_ENDPOINT: z.string().url().default('http://localhost:4317'),

  // Error tracking
  GLITCHTIP_DSN: z.string().url().optional(),

  // Logging
  LOG_LEVEL: z.enum(['trace', 'debug', 'info', 'warn', 'error', 'fatal']).default('info'),
});

// Parse and validate - throws on startup if invalid
export const env = envSchema.parse(process.env);

// Type for autocomplete
export type Env = z.infer<typeof envSchema>;
```

### File: `src/health.ts`

```typescript
import { FastifyInstance } from 'fastify';
import { PrismaClient } from '@prisma/client'; // or your DB client
import { Redis } from 'ioredis'; // if using Redis

interface HealthCheck {
  name: string;
  healthy: boolean;
  latency?: number;
  error?: string;
}

async function checkDatabase(prisma: PrismaClient): Promise<HealthCheck> {
  const start = Date.now();
  try {
    await prisma.$queryRaw`SELECT 1`;
    return { name: 'database', healthy: true, latency: Date.now() - start };
  } catch (error) {
    return { name: 'database', healthy: false, error: (error as Error).message };
  }
}

async function checkRedis(redis: Redis | undefined): Promise<HealthCheck> {
  if (!redis) return { name: 'redis', healthy: true }; // Skip if not configured
  const start = Date.now();
  try {
    await redis.ping();
    return { name: 'redis', healthy: true, latency: Date.now() - start };
  } catch (error) {
    return { name: 'redis', healthy: false, error: (error as Error).message };
  }
}

export function registerHealthRoutes(
  app: FastifyInstance,
  deps: { prisma: PrismaClient; redis?: Redis }
) {
  // Liveness - returns 200 if process is running
  app.get('/health', async () => ({
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: process.env.SERVICE_VERSION,
  }));

  // Readiness - checks all dependencies
  app.get('/ready', async (request, reply) => {
    const checks = await Promise.all([
      checkDatabase(deps.prisma),
      checkRedis(deps.redis),
    ]);

    const healthy = checks.every((c) => c.healthy);
    const status = healthy ? 'ready' : 'degraded';

    reply.status(healthy ? 200 : 503).send({
      status,
      timestamp: new Date().toISOString(),
      checks,
    });
  });
}
```

### File: `src/index.ts`

```typescript
// MUST be first import
import './instrumentation';

import Fastify from 'fastify';
import { env } from './config';
import logger from './logger';
import { registerHealthRoutes } from './health';
import { PrismaClient } from '@prisma/client';

const app = Fastify({ logger: false }); // Use custom Pino logger
const prisma = new PrismaClient();

// Health routes
registerHealthRoutes(app, { prisma });

// Your routes here
app.get('/', async () => ({ message: 'Hello World' }));

// Graceful shutdown
let isShuttingDown = false;

async function shutdown() {
  if (isShuttingDown) return;
  isShuttingDown = true;

  logger.info('Shutting down gracefully...');

  // Stop accepting new connections
  await app.close();

  // Cleanup
  await prisma.$disconnect();

  logger.info('Shutdown complete');
  process.exit(0);
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

// Start server
app.listen({ port: env.PORT, host: env.HOST }, (err) => {
  if (err) {
    logger.error(err);
    process.exit(1);
  }
  logger.info({ port: env.PORT }, 'Server started');
});
```

### package.json scripts

```json
{
  "scripts": {
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "typecheck": "tsc --noEmit"
  }
}
```

---

## Python (FastAPI)

### Installation

```bash
pip install opentelemetry-distro \
            opentelemetry-exporter-otlp \
            opentelemetry-instrumentation-fastapi \
            opentelemetry-instrumentation-sqlalchemy \
            opentelemetry-instrumentation-redis \
            opentelemetry-instrumentation-httpx \
            structlog \
            sentry-sdk \
            pydantic-settings
```

### File: `app/instrumentation.py`

```python
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

def setup_telemetry():
    resource = Resource.create({
        SERVICE_NAME: os.getenv("SERVICE_NAME", "unknown-service"),
        SERVICE_VERSION: os.getenv("SERVICE_VERSION", "0.0.0"),
        "deployment.environment": os.getenv("ENVIRONMENT", "development"),
    })

    provider = TracerProvider(resource=resource)

    exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"),
        insecure=True,
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)

    # Auto-instrument
    SQLAlchemyInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()

def instrument_app(app):
    FastAPIInstrumentor.instrument_app(app)
```

### File: `app/logger.py`

```python
import os
import structlog
from opentelemetry import trace

def add_trace_context(logger, method_name, event_dict):
    """Add OpenTelemetry trace context to every log."""
    span = trace.get_current_span()
    if span and span.get_span_context().is_valid:
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")

    event_dict["service"] = os.getenv("SERVICE_NAME", "unknown")
    event_dict["version"] = os.getenv("SERVICE_VERSION", "0.0.0")
    return event_dict

def setup_logging():
    processors = [
        structlog.contextvars.merge_contextvars,
        add_trace_context,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if os.getenv("ENVIRONMENT") == "development":
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            int(os.getenv("LOG_LEVEL", "20"))  # INFO = 20
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

def get_logger():
    return structlog.get_logger()
```

### File: `app/errors.py`

```python
import sentry_sdk
from opentelemetry import trace
from opentelemetry.trace import StatusCode
from app.logger import get_logger

logger = get_logger()

def setup_sentry():
    import os
    dsn = os.getenv("GLITCHTIP_DSN")
    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            environment=os.getenv("ENVIRONMENT", "development"),
            release=os.getenv("SERVICE_VERSION"),
            traces_sample_rate=0.0,  # We use OpenTelemetry for traces
        )

def capture_error(error: Exception, context: dict = None):
    """Capture error to span, logs, and GlitchTip."""
    span = trace.get_current_span()

    # Record to span
    if span:
        span.record_exception(error)
        span.set_status(StatusCode.ERROR, str(error))

    # Log
    logger.error(
        str(error),
        exc_info=error,
        **context or {},
    )

    # Send to GlitchTip
    sentry_sdk.capture_exception(error)
```

### File: `app/config.py`

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Service identity
    service_name: str = "my-service"
    service_version: str = "0.0.0"
    environment: str = "development"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str

    # Redis
    redis_url: str | None = None

    # OpenTelemetry
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"

    # Error tracking
    glitchtip_dsn: str | None = None

    # Logging
    log_level: int = 20  # INFO

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### File: `app/health.py`

```python
from fastapi import APIRouter, Response
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import time

router = APIRouter()

async def check_database(session: AsyncSession) -> dict:
    start = time.time()
    try:
        await session.execute(text("SELECT 1"))
        return {"name": "database", "healthy": True, "latency": time.time() - start}
    except Exception as e:
        return {"name": "database", "healthy": False, "error": str(e)}

@router.get("/health")
async def health():
    return {
        "status": "ok",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

@router.get("/ready")
async def ready(response: Response, session: AsyncSession):
    checks = [await check_database(session)]
    healthy = all(c["healthy"] for c in checks)

    if not healthy:
        response.status_code = 503

    return {
        "status": "ready" if healthy else "degraded",
        "checks": checks,
    }
```

### File: `app/main.py`

```python
import os
import signal
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.instrumentation import setup_telemetry, instrument_app
from app.logger import setup_logging, get_logger
from app.errors import setup_sentry
from app.config import get_settings
from app.health import router as health_router

# Setup before anything else
setup_telemetry()
setup_logging()
setup_sentry()

logger = get_logger()
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up", service=settings.service_name)
    yield
    logger.info("Shutting down")

app = FastAPI(lifespan=lifespan)
instrument_app(app)

app.include_router(health_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Graceful shutdown
def handle_sigterm(*args):
    logger.info("SIGTERM received")
    raise SystemExit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
```

---

## Go

### Installation

```bash
go get go.opentelemetry.io/otel
go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc
go get go.opentelemetry.io/otel/sdk/trace
go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp
go get github.com/rs/zerolog
go get github.com/getsentry/sentry-go
```

### File: `internal/telemetry/telemetry.go`

```go
package telemetry

import (
    "context"
    "os"
    "time"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/propagation"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
)

func Setup(ctx context.Context) (func(context.Context) error, error) {
    res, err := resource.New(ctx,
        resource.WithAttributes(
            semconv.ServiceName(os.Getenv("SERVICE_NAME")),
            semconv.ServiceVersion(os.Getenv("SERVICE_VERSION")),
            semconv.DeploymentEnvironment(os.Getenv("ENVIRONMENT")),
        ),
    )
    if err != nil {
        return nil, err
    }

    endpoint := os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint == "" {
        endpoint = "localhost:4317"
    }

    exporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint(endpoint),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(res),
    )

    otel.SetTracerProvider(tp)
    otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
        propagation.TraceContext{},
        propagation.Baggage{},
    ))

    return tp.Shutdown, nil
}
```

### File: `internal/logger/logger.go`

```go
package logger

import (
    "os"
    "time"

    "github.com/rs/zerolog"
    "go.opentelemetry.io/otel/trace"
)

var log zerolog.Logger

func Init() {
    zerolog.TimeFieldFormat = time.RFC3339

    output := zerolog.ConsoleWriter{Out: os.Stdout}
    if os.Getenv("ENVIRONMENT") == "production" {
        log = zerolog.New(os.Stdout).With().Timestamp().Logger()
    } else {
        log = zerolog.New(output).With().Timestamp().Logger()
    }

    log = log.With().
        Str("service", os.Getenv("SERVICE_NAME")).
        Str("version", os.Getenv("SERVICE_VERSION")).
        Logger()
}

// WithSpan adds trace context to logger
func WithSpan(span trace.Span) zerolog.Logger {
    if span == nil {
        return log
    }
    ctx := span.SpanContext()
    return log.With().
        Str("traceId", ctx.TraceID().String()).
        Str("spanId", ctx.SpanID().String()).
        Logger()
}

func Get() zerolog.Logger {
    return log
}
```

### File: `internal/health/health.go`

```go
package health

import (
    "context"
    "database/sql"
    "encoding/json"
    "net/http"
    "time"
)

type HealthCheck struct {
    Name    string  `json:"name"`
    Healthy bool    `json:"healthy"`
    Latency float64 `json:"latency,omitempty"`
    Error   string  `json:"error,omitempty"`
}

type HealthHandler struct {
    db *sql.DB
}

func NewHandler(db *sql.DB) *HealthHandler {
    return &HealthHandler{db: db}
}

func (h *HealthHandler) Health(w http.ResponseWriter, r *http.Request) {
    json.NewEncoder(w).Encode(map[string]interface{}{
        "status":    "ok",
        "timestamp": time.Now().UTC().Format(time.RFC3339),
    })
}

func (h *HealthHandler) Ready(w http.ResponseWriter, r *http.Request) {
    checks := []HealthCheck{h.checkDatabase(r.Context())}

    healthy := true
    for _, c := range checks {
        if !c.Healthy {
            healthy = false
            break
        }
    }

    status := "ready"
    if !healthy {
        status = "degraded"
        w.WriteHeader(http.StatusServiceUnavailable)
    }

    json.NewEncoder(w).Encode(map[string]interface{}{
        "status": status,
        "checks": checks,
    })
}

func (h *HealthHandler) checkDatabase(ctx context.Context) HealthCheck {
    start := time.Now()
    err := h.db.PingContext(ctx)
    latency := time.Since(start).Seconds()

    if err != nil {
        return HealthCheck{Name: "database", Healthy: false, Error: err.Error()}
    }
    return HealthCheck{Name: "database", Healthy: true, Latency: latency}
}
```

---

## Environment Variables

All languages use the same environment variables:

```bash
# Service identity
SERVICE_NAME=my-service
SERVICE_VERSION=1.0.0
ENVIRONMENT=production

# Server
PORT=3000
HOST=0.0.0.0

# Database
DATABASE_URL=postgres://user:pass@localhost:5432/db

# OpenTelemetry
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317

# Error tracking (GlitchTip)
GLITCHTIP_DSN=http://key@glitchtip:8000/1

# Logging
LOG_LEVEL=info
```

---

## Validation Checklist

After integration, verify:

- [ ] `curl /health` returns 200 with JSON
- [ ] `curl /ready` returns 200 with dependency checks
- [ ] Logs are JSON-formatted with traceId/spanId
- [ ] Traces appear in Jaeger UI
- [ ] Errors appear in GlitchTip with trace context
- [ ] No `console.log` / `print` statements in production code
- [ ] App fails to start if required config is missing
- [ ] Graceful shutdown completes without errors

---

## Related

- Domain: `memory/domains/production.md`
- Stack: `templates/shared/observability-stack.md`

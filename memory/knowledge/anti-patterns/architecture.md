# Architecture Anti-Patterns Database

## Overview

This database catalogs common software architecture anti-patterns that lead to unmaintainable, unscalable, and unreliable systems. Each anti-pattern includes detection methods, root causes, consequences, and remediation strategies.

**Usage**: Reference during architecture reviews, ADR discussions, and system design sessions.

---

## ARCH-001: Big Ball of Mud

### Description
A system with no discernible architecture — a haphazardly structured, sprawling, sloppy, duct-tape-and-baling-wire, spaghetti-code jungle. The most common architecture pattern in practice.

### Detection Signals
- No clear module boundaries
- Any component can call any other component
- Changing one thing breaks unrelated things
- No one understands the full system
- "Tribal knowledge" required to navigate code
- Inconsistent naming conventions
- Multiple ways to do the same thing

### Metrics
| Metric | Warning Level | Critical Level |
|--------|---------------|----------------|
| Cyclomatic complexity | >20 per function | >50 per function |
| Coupling between modules | >5 dependencies | >10 dependencies |
| Change failure rate | >30% | >50% |
| Time to onboard dev | >2 weeks | >1 month |

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Throwaway code that stuck | MVP never refactored |
| Piecemeal growth | No architectural vision |
| Developer turnover | Knowledge loss |
| Time pressure | "We'll fix it later" |
| No architecture ownership | No one responsible |

### Remediation

**Strangler Fig Approach**:
```text
Phase 1: Identify Seams
├── Map current system
├── Find natural boundaries
└── Identify highest-pain areas

Phase 2: Extract Module
├── Define clear interface
├── Create new implementation
├── Route traffic through facade
└── Migrate incrementally

Phase 3: Strangle Old Code
├── Monitor new implementation
├── Gradually shift traffic
├── Deprecate old paths
└── Delete dead code
```

**Bounded Context Discovery**:
```text
1. Event Storming Workshop
   ├── Map domain events
   ├── Identify aggregates
   └── Find context boundaries

2. Context Mapping
   ├── Upstream/downstream relationships
   ├── Shared kernels
   └── Anti-corruption layers

3. Module Extraction Priority
   ├── Business criticality × Change frequency
   └── Start with highest score
```

### Prevention
- Architecture Decision Records (ADRs) for major changes
- Regular architecture reviews
- Clear module ownership
- Fitness functions for architecture compliance

---

## ARCH-002: Distributed Monolith

### Description
A system that has the complexity of microservices but the coupling of a monolith. The worst of both worlds — network overhead plus tight coupling.

### Detection Signals
- Deploying service A requires deploying service B
- Shared database between "independent" services
- Synchronous calls between all services
- Single point of failure takes down everything
- "Microservices" but one Git repo
- All services deployed together

### Distributed Monolith Smell Test
```text
Ask: "Can Service A be deployed independently?"
├── No → Distributed Monolith
├── Yes, but we never do → Distributed Monolith
└── Yes, and we regularly do → True Microservices
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Cargo cult microservices | "Everyone else is doing it" |
| Shared database | "It's easier" |
| Synchronous everything | RPC feels familiar |
| No clear boundaries | Split by layer, not domain |
| Lack of async patterns | Don't know how |

### Consequences
| Impact | Description |
|--------|-------------|
| Worse than monolith | Network overhead without benefit |
| Cascading failures | One service down = all down |
| Deployment nightmare | Coordinate all services |
| Testing complexity | Integration testing explosion |
| Performance | N+1 network calls |

### Remediation

**True Service Independence**:
```text
Each service MUST have:
├── Own database (no sharing)
├── Own deployment pipeline
├── Own on-call rotation
├── Async communication (prefer events)
└── Graceful degradation (works if others down)
```

**Event-Driven Decoupling**:
```text
BEFORE (Coupled):
Order Service ──sync call──► Inventory ──sync──► Shipping
      │                          │                  │
      └──────── If any fails, all fail ─────────────┘

AFTER (Decoupled):
Order Service ──publish──► Event Bus
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
               Inventory  Shipping   Billing
               (async)    (async)    (async)
```

**Database-per-Service Pattern**:
```text
❌ SHARED DATABASE:
Service A ───┐
             ├──► Shared DB ───► Tight coupling
Service B ───┘

✅ DATABASE-PER-SERVICE:
Service A ──► DB A ──► Own schema, own lifecycle
Service B ──► DB B ──► Independent scaling
                  │
            Event sync for shared data
```

### Prevention
- Clear bounded contexts before splitting
- API contracts before implementation
- Async by default, sync when necessary
- Each service independently deployable

---

## ARCH-003: Golden Hammer

### Description
Applying a familiar tool or pattern to every problem, regardless of fit. "When all you have is a hammer, everything looks like a nail."

### Detection Signals
- "We use [X] for everything"
- Same database for OLTP and OLAP
- One language for all services
- Microservices for simple CRUD app
- Kubernetes for 3-developer startup
- GraphQL for internal service-to-service

### Common Golden Hammers
| Hammer | Misuse Example |
|--------|----------------|
| Microservices | 5-person team, MVP stage |
| Kubernetes | 3 services, could use simple VMs |
| MongoDB | Financial data needing transactions |
| GraphQL | Internal APIs between services |
| Redis | Primary database |
| React | Static content site |

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Expertise bias | "I know this well" |
| Résumé-driven dev | "Want to learn X" |
| Vendor lock-in | "We're an X shop" |
| Fear of unknown | New tools are risky |
| Past success | "It worked before" |

### Remediation

**Technology Selection Matrix**:
```text
For each problem, evaluate:

1. PROBLEM CHARACTERISTICS
   ├── Data model (relational vs document)
   ├── Scale requirements (now and 2 years)
   ├── Consistency needs (ACID vs eventual)
   ├── Query patterns (complex joins vs simple lookups)
   └── Team expertise

2. SOLUTION OPTIONS (minimum 3)
   ├── Option A: [Technology]
   │   ├── Pros: [...]
   │   ├── Cons: [...]
   │   └── Fit score: X/10
   └── Compare objectively

3. DECISION CRITERIA
   ├── Technical fit (primary)
   ├── Team capability
   ├── Operational complexity
   ├── Total cost of ownership
   └── Migration path
```

**Right Tool Guidelines**:
| Problem | Consider |
|---------|----------|
| Simple CRUD | Monolith, PostgreSQL |
| High write throughput | Cassandra, ScyllaDB |
| Complex relationships | PostgreSQL, Neo4j |
| Document flexibility | MongoDB, PostgreSQL (JSONB) |
| Caching | Redis, Memcached |
| Search | Elasticsearch, OpenSearch |
| Message queue | RabbitMQ, Kafka (scale) |
| Static site | Hugo, 11ty (not React) |

### Prevention
- ADRs with alternatives considered
- "Why not X?" section in design docs
- Proof of concept for new tech
- Technology radar with governance

---

## ARCH-004: Premature Optimization

### Description
Optimizing for scale, performance, or complexity before there's evidence it's needed. Building for millions when you have hundreds.

### Detection Signals
- "We need to scale to 10 million users"
- Complex caching before measuring
- Microservices for first version
- Sharding database with 1GB of data
- CQRS for simple CRUD
- Event sourcing for blog

### Optimization Timing
```text
Premature                    Appropriate
    │                             │
    ▼                             ▼
No users ────────────────────────► Bottleneck measured
No metrics ──────────────────────► Data proves need
Guessing ────────────────────────► Profiling guides
Architecture phase ──────────────► After MVP validates
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Fear of success | "What if we go viral?" |
| Enterprise habits | Team from big company |
| Résumé building | "Want to use X" |
| Vendor influence | "You'll need this" |
| Avoiding hard choices | Complexity is easier |

### Remediation

**Right-Sizing Framework**:
```text
Stage 1: Validate (0-100 users)
├── SQLite, single server OK
├── Sync operations OK
├── Simplest possible architecture
└── Measure before optimizing

Stage 2: Scale (100-10K users)
├── PostgreSQL, proper hosting
├── Add caching where measured
├── Async for slow operations
└── Still probably monolith

Stage 3: Optimize (10K-100K users)
├── Read replicas
├── CDN for static
├── Queue for background jobs
└── Maybe extract one service

Stage 4: Distribute (100K+ users)
├── Database sharding if needed
├── Service extraction where bounded
├── Edge computing
└── Full observability
```

**Performance Budget**:
```text
Instead of optimizing everything, set budgets:

Page Load: < 3 seconds
API Response: < 200ms (P95)
Database Query: < 50ms

Optimize ONLY when budget exceeded.
Measure → Budget violated? → Optimize specific bottleneck
```

### Prevention
- "Do we have a problem?" before "What's the solution?"
- Measure before optimizing
- Simple solution first, complexity later
- Performance budgets as guardrails

---

## ARCH-005: Shared Database Integration

### Description
Multiple applications sharing a database as an integration mechanism. One app writes, others read — creating invisible coupling.

### Detection Signals
- Multiple apps connect to same database
- "We just read from their tables"
- No API, just SQL queries
- Schema changes break multiple apps
- Unclear data ownership
- Stored procedures as business logic

### Coupling Diagram
```text
ANTI-PATTERN: Shared Database
                    ┌─────────────┐
     App A ─────────┤             │
                    │  Shared     │
     App B ─────────┤  Database   │
                    │             │
     App C ─────────┤             │
                    └─────────────┘
Any schema change affects all apps.
No contract. No versioning. Maximum coupling.
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Speed | "Faster than building API" |
| Simplicity | "Just a SELECT" |
| Historical | "It's always been this way" |
| No ownership | "Database is shared resource" |
| SQL expertise | "We know SQL well" |

### Consequences
| Impact | Description |
|--------|-------------|
| Schema lock-in | Can't change without breaking others |
| Data ownership unclear | Who's responsible for integrity? |
| Performance coupling | One app's queries affect others |
| Technology lock-in | All apps use same database |
| Testing nightmare | Can't test in isolation |

### Remediation

**API-First Integration**:
```text
PATTERN: Service with API

     App A ────►  ┌─────────────┐
                  │   App B     │
     App C ────►  │   (Owner)   │
                  │     ↓       │
                  │  Database   │
                  └─────────────┘

App B owns the data. Exposes API.
Schema changes don't affect consumers.
Clear contract. Version control.
```

**Change Data Capture Pattern**:
```text
For read-heavy integration:

Primary Service ──► Database ──► CDC ──► Event Stream
                                              │
                              ┌───────────────┼───────────────┐
                              ▼               ▼               ▼
                         Consumer A      Consumer B      Consumer C
                         (own copy)      (own copy)      (own copy)

Each consumer has own copy.
Eventually consistent but decoupled.
```

**Migration Strategy**:
```text
Phase 1: Identify all consumers
         └── Query logs, connection pools

Phase 2: Create API for data access
         └── App B becomes data owner

Phase 3: Migrate consumers to API
         └── One by one, measure latency

Phase 4: Restrict database access
         └── Only owner can connect

Phase 5: Evolve schema freely
         └── API contract, not schema
```

### Prevention
- Data ownership defined upfront
- API-first integration policy
- No direct database access across teams
- Event-driven for cross-service data

---

## ARCH-006: Synchronous Chain

### Description
Long chains of synchronous service calls where each service waits for the next. Latency accumulates, availability multiplies down.

### Detection Signals
- Request timeout after 30+ seconds
- One slow service blocks everything
- P99 latency >> P50 latency
- Cascading failures common
- Circuit breakers constantly open

### Latency Accumulation
```text
Synchronous Chain:
User → A (50ms) → B (100ms) → C (200ms) → D (150ms)
                                                │
Total latency: 500ms                            │
Availability: 99% × 99% × 99% × 99% = 96.1%    ←┘

If any service slow, all slow.
If any service down, all down.
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| RPC familiarity | "It's like function calls" |
| Async complexity | "Async is hard" |
| Transaction mindset | "Need immediate consistency" |
| Request-response habit | REST = sync in mindset |

### Remediation

**Async by Default Pattern**:
```text
BEFORE (Sync Chain):
POST /order → Create → Validate → Charge → Ship → Response
                                                    │
Total: 2 seconds                                    │
User waits for everything                          ←┘

AFTER (Async):
POST /order → Accept → Return 202 Accepted (50ms)
       │
       └──► Event: OrderCreated
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   Validation   Payment     Notification
   (async)      (async)     (async)
       │            │
       └────────────┴──► Event: OrderComplete
                              │
                         User notified
```

**Saga Pattern for Distributed Transactions**:
```text
Choreography (Event-driven):
Order Created ──► Payment Charged ──► Inventory Reserved ──► Shipping Created
      │                 │                    │                     │
      └─────────────────┴────────────────────┴─────────────────────┘
              Each service reacts to events. No orchestrator.

Orchestration:
      ┌─────────────────────────────────────────┐
      │           Order Saga Orchestrator       │
      └───────────────────┬─────────────────────┘
          │               │                │
          ▼               ▼                ▼
       Payment       Inventory         Shipping
          │               │                │
          └───────────────┴────────────────┘
              Orchestrator controls flow.
```

**Circuit Breaker**:
```text
Closed ──(failures > threshold)──► Open
  ↑                                   │
  │                            (timeout)
  │                                   │
  └───(success)───── Half-Open ◄─────┘

When downstream slow/failing:
- Open circuit
- Fail fast
- Fallback response
- Recover gracefully
```

### Prevention
- Default to async, sync when required
- Circuit breakers on all external calls
- Timeout budgets per request
- Retry with exponential backoff

---

## ARCH-007: Missing Observability

### Description
Production systems without adequate logging, metrics, tracing, or alerting. "Flying blind" — problems discovered by users, not monitoring.

### Detection Signals
- "Check the logs" requires SSH
- No dashboards for service health
- No distributed tracing
- Alerts based on user complaints
- Post-mortem: "We need better monitoring"
- Debug by adding print statements

### Observability Gaps
| Gap | Consequence |
|-----|-------------|
| No metrics | Don't know if system is healthy |
| No tracing | Can't debug distributed requests |
| No structured logs | Grep-based debugging |
| No alerting | Users find problems first |
| No runbooks | Reinvent debugging each time |

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Feature pressure | "Ship features, not tooling" |
| Complexity | "Observability is hard" |
| Cost | "Infrastructure is expensive" |
| Ops split | "That's the ops team's job" |
| Works on my machine | "It's fine in dev" |

### Remediation

**Observability Stack**:
```text
THREE PILLARS:

1. METRICS (What is happening?)
   ├── RED: Rate, Errors, Duration (services)
   ├── USE: Utilization, Saturation, Errors (resources)
   └── Business: Orders/min, Revenue, Conversions

2. LOGS (Why did it happen?)
   ├── Structured JSON (not plain text)
   ├── Correlation IDs (trace requests)
   └── Contextual data (user ID, request ID)

3. TRACES (Where did it happen?)
   ├── Distributed request tracing
   ├── Span timing breakdown
   └── Cross-service visualization
```

**SLO-Based Alerting**:
```text
INSTEAD OF:
Alert when CPU > 80%
Alert when error count > 10

USE SLOs:
Service: Order API
SLO: 99.9% of requests complete in < 500ms

Error Budget: 0.1% (43 minutes/month downtime OK)

Alert when:
- Error budget burn rate > 10x (page now)
- Error budget burn rate > 2x (ticket)
- Error budget < 20% remaining (review)
```

**Minimum Viable Observability**:
```text
DAY 1:
├── Structured logging with correlation IDs
├── Health check endpoint
└── Basic uptime monitoring

WEEK 1:
├── RED metrics for each service
├── Dashboard with key graphs
└── PagerDuty/Opsgenie integration

MONTH 1:
├── Distributed tracing
├── SLO definitions
├── Error budget tracking
└── Runbooks for common alerts
```

### Prevention
- Observability as non-functional requirement
- SLOs defined before launch
- Dashboards part of definition of done
- Runbooks accompany new features

---

## ARCH-008: Hardcoded Configuration

### Description
Configuration baked into code rather than externalized. Environment-specific values, secrets, and feature flags compiled into artifacts.

### Detection Signals
- Different builds for staging vs prod
- Secrets in Git history
- Environment variables set in Dockerfile
- Feature flags require deployment
- Config changes need code review

### Configuration Layers
```text
HARDCODED (Bad):
if (env == "prod") {
    dbHost = "prod-db.internal";
    apiKey = "sk_live_abc123";
}

EXTERNALIZED (Good):
dbHost = config.get("DB_HOST");
apiKey = secretManager.get("API_KEY");
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Speed | "It's just one value" |
| Simplicity | "No config infrastructure" |
| Lack of tooling | "We don't have secret manager" |
| Single environment | "We only have prod" |
| Copy-paste | "It works in another project" |

### Remediation

**12-Factor Configuration**:
```text
ENVIRONMENT VARIABLES (runtime config):
DATABASE_URL=postgres://...
REDIS_URL=redis://...
LOG_LEVEL=info

SECRETS (sensitive, encrypted):
API_KEY → Secret Manager
DB_PASSWORD → Secret Manager
TLS_CERT → Secret Manager

FEATURE FLAGS (dynamic):
ENABLE_NEW_CHECKOUT → LaunchDarkly / Unleash
ROLLOUT_PERCENTAGE → Remote config
```

**Configuration Hierarchy**:
```text
1. Defaults (in code) ─────────► Fallback values
2. Config files ───────────────► Environment-specific
3. Environment variables ──────► Override at deploy
4. Secret manager ─────────────► Sensitive data
5. Remote config ──────────────► Dynamic changes
```

**Secret Management Pattern**:
```text
❌ NEVER:
secrets.json committed to Git
.env files with real secrets
API keys in CI/CD logs

✅ ALWAYS:
Secret manager (Vault, AWS Secrets Manager)
Environment injection at runtime
Secret rotation automated
Audit logs for access
```

### Prevention
- No secrets in code (git-secrets hook)
- Config validation at startup
- Environment parity (same config structure)
- Feature flags externalized

---

## ARCH-009: Insufficient Fault Isolation

### Description
System where failures cascade — one component failure brings down unrelated components. No bulkheads, no circuit breakers, no graceful degradation.

### Detection Signals
- One service down = entire system down
- No fallback behavior
- Timeout = retry forever
- Memory leak in one service affects others
- "We had to restart everything"

### Failure Propagation
```text
WITHOUT ISOLATION:
Service A (OOM) ──► Shared Thread Pool ──► Service B (blocked)
                                                    │
                            ┌───────────────────────┘
                            ▼
                     Load Balancer ──► All instances affected
                            │
                            └──► User: "Site is down"

WITH ISOLATION:
Service A (OOM) ──► Bulkhead ──► Only Service A affected
                       │
                       └──► Circuit Breaker ──► Fallback response
                                                       │
                                    User: "Some features unavailable"
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Shared resources | Thread pools, connections, memory |
| No timeouts | Wait forever for response |
| No circuit breakers | Keep calling failing service |
| Monolithic deployment | All eggs in one basket |
| Optimistic assumptions | "It won't fail" |

### Remediation

**Bulkhead Pattern**:
```text
Separate resources by criticality:

CRITICAL PATH (checkout):
├── Dedicated thread pool
├── Dedicated database connections
├── Isolated from non-critical

STANDARD PATH (browse):
├── Shared thread pool
├── Shared connections
├── Graceful degradation OK

NON-CRITICAL (recommendations):
├── Best-effort
├── Fallback to cached/empty
├── Can fail without affecting core
```

**Graceful Degradation Pattern**:
```text
Level 0: Full functionality
         └── All services healthy

Level 1: Partial degradation
         └── Recommendations unavailable
         └── Search uses cache

Level 2: Core only
         └── Checkout works
         └── Browse works
         └── Everything else off

Level 3: Read only
         └── View products
         └── No mutations

Level 4: Maintenance mode
         └── Static page
```

**Chaos Engineering Practice**:
```text
Regular failure injection:
1. Random service termination
2. Network partition simulation
3. Dependency latency injection
4. Resource exhaustion

Validate:
- System degrades gracefully
- Core paths remain functional
- Recovery is automatic
- Alerts fire correctly
```

### Prevention
- Design for failure from start
- Circuit breakers on all external calls
- Bulkheads for resource isolation
- Regular chaos testing
- Graceful degradation as requirement

---

## ARCH-010: Security as Afterthought

### Description
Security added at the end of development rather than designed in. Bolt-on security that leaves fundamental vulnerabilities.

### Detection Signals
- Security review only before launch
- No threat modeling
- "We'll add auth later"
- Secrets in plain text
- No input validation
- Trust all internal traffic

### Security Debt Accumulation
```text
Phase 1: "MVP doesn't need security"
Phase 2: "We'll add it next sprint"
Phase 3: "Too much to refactor now"
Phase 4: "Breach happened"
Phase 5: "Rewrite with security in mind"
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Speed pressure | "Ship first, secure later" |
| Security expertise gap | "We're not security experts" |
| Invisible problem | "Haven't been breached yet" |
| Cost perception | "Security slows us down" |
| User-facing focus | Features visible, security invisible |

### Remediation

**Security by Design Principles**:
```text
1. DEFENSE IN DEPTH
   └── Multiple layers, each independently secure

2. LEAST PRIVILEGE
   └── Minimum access needed for function

3. FAIL SECURE
   └── Errors deny access, not grant

4. ZERO TRUST
   └── Verify everything, trust nothing

5. SEPARATION OF CONCERNS
   └── Auth, authz, audit as separate concerns
```

**Threat Modeling (STRIDE)**:
```text
For each component, analyze:

S - Spoofing: Can attacker impersonate?
T - Tampering: Can attacker modify data?
R - Repudiation: Can attacker deny actions?
I - Info Disclosure: Can attacker access data?
D - Denial of Service: Can attacker disrupt?
E - Elevation: Can attacker gain privileges?
```

**Security Checklist**:
```text
AUTHENTICATION:
☐ Strong password policy enforced
☐ MFA available/required
☐ Session timeout configured
☐ JWT/token expiration short

AUTHORIZATION:
☐ RBAC/ABAC implemented
☐ Principle of least privilege
☐ Authz checks at every layer
☐ No client-side only checks

DATA PROTECTION:
☐ Encryption at rest
☐ Encryption in transit
☐ Sensitive data identified
☐ PII handling documented

INPUT VALIDATION:
☐ All inputs validated
☐ SQL injection prevented
☐ XSS prevented
☐ CSRF tokens used

SECRETS:
☐ Secret manager used
☐ No secrets in code
☐ Rotation automated
☐ Access audited
```

### Prevention
- Threat modeling in design phase
- Security review in PR checklist
- Dependency scanning automated
- Penetration testing regular
- Security training for developers

---

## Quick Reference: Anti-Pattern Detection Matrix

| Anti-Pattern | Quick Detection | Immediate Action |
|--------------|-----------------|------------------|
| ARCH-001: Ball of Mud | No clear boundaries | Identify seams, extract module |
| ARCH-002: Distributed Monolith | Deploy together | Database per service, async |
| ARCH-003: Golden Hammer | "We use X for everything" | ADR with alternatives |
| ARCH-004: Premature Optimization | "Scale to millions" | Size for current stage |
| ARCH-005: Shared Database | Multiple apps, one DB | API-first integration |
| ARCH-006: Sync Chain | Timeout cascade | Async by default |
| ARCH-007: Missing Observability | "Check the logs" | Add metrics, tracing |
| ARCH-008: Hardcoded Config | Different builds per env | Externalize config |
| ARCH-009: No Fault Isolation | One service down = all | Bulkheads, circuit breakers |
| ARCH-010: Security Afterthought | "Add auth later" | Threat model now |

## Architecture Review Prompts

Use these during architecture reviews:

1. "What happens when this service is down?"
2. "Where are the single points of failure?"
3. "Who owns this data?"
4. "How do we deploy this independently?"
5. "What's the blast radius of a failure here?"
6. "How do we know if this is healthy?"
7. "What's the security threat model?"
8. "What would we do differently with 10x traffic?"
9. "How long would it take a new developer to understand this?"
10. "What's the migration path if we're wrong?"

## Resources

- **Books**: "Building Microservices" (Newman), "Release It!" (Nygard)
- **Patterns**: microservices.io, Martin Fowler's patterns
- **Tools**: Architecture Decision Records, C4 Model

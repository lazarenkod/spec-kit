# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Strategic Narrative (Working Backwards)

<!--
  PURPOSE: Define the customer experience BEFORE building. Working Backwards methodology.
  Import from concept.md PR/FAQ section if available, otherwise generate.

  Reference: templates/shared/concept-sections/pr-faq.md
  Quality Gate: IG-PLAN-005 (Strategic Narrative Present)
-->

### Press Release Summary

**Product/Feature**: [Feature name from spec]
**Target Customer**: [Specific customer segment from personas]
**Quantified Value Proposition**: [Measurable benefit, e.g., "Reduces X by Y%" or "Saves Z hours/week"]

#### Key Pain Points Addressed

1. [Pain with numbers: "Users waste X hours per week on..."]
2. [Pain with numbers: "Current solution costs $X per month..."]
3. [Qualitative frustration: "Users are frustrated by..."]

#### Differentiators vs Alternatives

| Alternative | Our Advantage | Quantified Improvement |
|-------------|---------------|------------------------|
| [Status quo / manual process] | [What we do differently] | [X% faster/cheaper/easier] |
| [Competitor A] | [Our unique value] | [Specific metric] |
| [Competitor B] | [Our unique value] | [Specific metric] |

### MVP Scope Statement

**What We're Building (v1)**:
1. [Must-have feature 1]: [Why essential for launch - ties to pain point]
2. [Must-have feature 2]: [Why essential for launch]
3. [Must-have feature 3]: [Why essential for launch]

**What We're NOT Building (v1)**:
- [Excluded feature 1]: [Why excluded, when to revisit]
- [Excluded feature 2]: [Alternative users should use instead]
- [Excluded feature 3]: [Future phase consideration]

**Time to Value**:
- **Day 1**: [Immediate benefit user gets after first use]
- **Week 1**: [Early wins and habits formed]
- **Month 1**: [Full value realization and retention trigger]

### Go/No-Go Criteria

| Criterion | Threshold | Current Status | Owner |
|-----------|-----------|----------------|-------|
| Technical feasibility validated | All blockers resolved | [Status] | [Name] |
| Core dependencies available | PKG/API verified | [Status] | [Name] |
| Team capacity confirmed | Sprint allocated | [Status] | [Name] |

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

### Non-Functional Requirements (NFRs)

<!--
  PURPOSE: Define measurable performance, reliability, and observability targets.
  Each NFR MUST have: metric, target, measurement method, and linked ADR.

  Quality Gate: IG-PLAN-007 (NFR Definition) - CRITICAL
  Self-Review: SR-PLAN-17 (P95/P99 defined), SR-PLAN-18 (Availability justified)
  Reference NFR IDs in tasks: [NFR:NFR-PERF-001]
-->

#### Performance Requirements (NFR-PERF-xxx)

| ID | Metric | P50 | P95 | P99 | P99.9 | Measurement | Linked ADR |
|----|--------|-----|-----|-----|-------|-------------|------------|
| NFR-PERF-001 | API Response Time | <50ms | <200ms | <500ms | <1000ms | OTel traces, load test | ADR-xxx |
| NFR-PERF-002 | Database Query Time | <10ms | <50ms | <100ms | <200ms | Slow query log | ADR-xxx |
| NFR-PERF-003 | Throughput | - | - | - | [X RPS] | Load test | ADR-xxx |

**Load Profile**:
- **Peak Concurrent Users**: [X users simultaneously active]
- **Request Rate at Peak**: [X requests/second]
- **Data Volume**: [X records in DB, X GB storage]
- **Growth Rate**: [X% monthly growth expected]

#### Reliability Requirements (NFR-REL-xxx)

| ID | Metric | Target | Error Budget | Measurement | Linked ADR |
|----|--------|--------|--------------|-------------|------------|
| NFR-REL-001 | Availability | 99.9% | 43.8 min/month | Uptime monitor | ADR-xxx |
| NFR-REL-002 | MTTR | <15 min | - | Incident log | ADR-xxx |
| NFR-REL-003 | MTBF | >30 days | - | Incident log | ADR-xxx |

**Availability Target Justification**:
- **99.9% (Three 9s)**: [Standard web app - 43.8 min/month downtime allowed]
- **Why not 99.95%**: [Cost/complexity not justified for this use case]
- **Why not 99.99%**: [Mission-critical not required, would need geo-redundancy]

#### Observability Requirements (NFR-OBS-xxx)

| ID | Requirement | Target | Implementation | Status |
|----|-------------|--------|----------------|--------|
| NFR-OBS-001 | Trace Coverage | 100% API endpoints | OTel auto-instrumentation | Planned |
| NFR-OBS-002 | Log Correlation | Trace ID in all logs | Structured logging | Planned |
| NFR-OBS-003 | Metric Cardinality | <10K unique series | Label constraints | Planned |
| NFR-OBS-004 | Alert Coverage | All NFR-PERF metrics | Grafana/PagerDuty | Planned |

#### Security Requirements (NFR-SEC-xxx)

| ID | Requirement | Standard | Implementation | Status |
|----|-------------|----------|----------------|--------|
| NFR-SEC-001 | Authentication | [OAuth2/JWT/Session] | [Implementation] | Planned |
| NFR-SEC-002 | Data Encryption | TLS 1.3 in transit, AES-256 at rest | [Implementation] | Planned |
| NFR-SEC-003 | Input Validation | OWASP Top 10 | [Implementation] | Planned |

### Design System *(for UI features)*

<!--
  Include this section if the feature has significant user interface.
  Skip for API-only, CLI, or backend features.
  Reference design.md for detailed visual specifications.
-->

**Component Library**: [Radix UI, Headless UI, shadcn/ui, custom, or N/A]
**Styling Approach**: [Tailwind CSS, CSS Modules, styled-components, or NEEDS CLARIFICATION]
**Design Tokens**: [CSS variables, JSON tokens, theme file location]
**Icon System**: [Lucide, Heroicons, Phosphor, custom SVG, or NEEDS CLARIFICATION]
**Animation Library**: [Framer Motion, CSS transitions, GSAP, or none]
**Accessibility Target**: [WCAG 2.1 A, AA, or AAA]
**Design Reference**: [design.md location, Figma link, or "To be created"]

### Dependency Registry

<!--
  CRITICAL: This section is the single source of truth for all dependencies.
  AI agents MUST verify method signatures and API calls against these docs.

  Populated by Phase 0.5 (API Verification) of /speckit.plan command.
  Use Context7 MCP tool to fetch and verify documentation.

  Reference format in tasks: [DEP:PKG-001], [DEP:API-001], [DEP:FW-001]
-->

#### Package Dependencies (PKG-xxx)

| ID | Package | Locked Version | Documentation URL | Key APIs Used |
|----|---------|----------------|-------------------|---------------|
| PKG-001 | [name] | [exact version] | [docs URL] | [method1(), method2()] |

**Version Lock Rationale**: [why specific versions are locked]

#### External API Dependencies (API-xxx)

| ID | Provider | API Version | Base URL | Docs | Rate Limits | Auth |
|----|----------|-------------|----------|------|-------------|------|
| API-001 | [e.g., Stripe] | [e.g., 2024-12-18] | [base URL] | [docs] | [limits] | [method] |

#### Framework Dependencies (FW-xxx)

| ID | Framework | Version | Docs | Breaking Changes Since |
|----|-----------|---------|------|------------------------|
| FW-001 | [name] | [version] | [docs URL] | [list major breaking changes] |

#### Infrastructure Dependencies (INFRA-xxx)

<!--
  Infrastructure requirements from spec.md Infrastructure Requirements section.
  These define cloud resources needed for deployment.
  Referenced by /speckit.ship for provisioning via Terraform.

  Types: database, cache, queue, storage, compute, network, secret
  Provisioned by: provision.sh using infra.yaml configuration
-->

| ID | Type | Service | Config | Environments | Status |
|----|------|---------|--------|--------------|--------|
| INFRA-001 | database | [e.g., PostgreSQL 16] | [size/config] | [staging, production] | [Existing/New] |
| INFRA-002 | cache | [e.g., Redis 7] | [size/config] | [all] | [Existing/New] |

**Provisioning Strategy**:
- `Existing`: Infrastructure already exists in environment, reuse
- `New`: Must be provisioned by /speckit.ship before deployment
- Infrastructure is shared across features in the same environment

**Generated Artifacts**:
- `infra.yaml` - Terraform configuration for provisioning
- `deploy.yaml` - Helm/docker-compose configuration for deployment
- `verify.yaml` - Health check and acceptance test configuration

#### Platform Dependencies (PLATFORM-xxx)

<!--
  Cross-platform framework requirements from constitution.platform.md.
  Auto-detected by /speckit.plan using templates/shared/platform-detection.md.
  Skip this section if Project Type is not Mobile + API.

  Types: kmp, flutter, react_native
  Integration tasks auto-injected by /speckit.tasks into Phase 2 (Foundational)
-->

| ID | Platform | Version | Constitution | Integration Checklist | Status |
|----|----------|---------|--------------|----------------------|--------|
| PLATFORM-001 | [kmp/flutter/react_native] | [e.g., Kotlin 1.9, Flutter 3.16] | [platforms/kmp.md] | [kmp-integration-checklist.md] | [Detected/Manual] |

**Platform Build Commands**:
- KMP iOS: `./gradlew :shared:linkDebugFrameworkIosArm64`
- KMP Android: `./gradlew :androidApp:assembleDebug`
- Flutter: `flutter build ios/apk --debug`
- React Native: `npx react-native run-ios/android`

**Platform Integration Validation**:
- [ ] Framework builds successfully for both platforms
- [ ] DI configuration exports factory functions for iOS
- [ ] Platform-specific implementations complete (expect/actual)
- [ ] Verification tasks pass (QG-PLATFORM-001 to QG-PLATFORM-003)

**Note**: Platform integration tasks are automatically injected into tasks.md Phase 2 (Foundational) by `/speckit.tasks`. See `templates/shared/platforms/{platform}-integration-checklist.md` for details.

### API Method Reference

<!--
  Document specific methods/endpoints that will be used in implementation.
  This prevents AI agents from hallucinating non-existent APIs.
  Use Context7 to fetch current method signatures.
-->

| Dependency | Method/Endpoint | Signature/Parameters | Docs Section |
|------------|-----------------|---------------------|--------------|
| PKG-001 | [method()] | [params and return type] | [docs anchor] |
| API-001 | POST /endpoint | [request/response schema] | [docs anchor] |

### API Contracts

<!--
  Auto-generated by /speckit.plan Step 4.5 if openapi_generation.enabled.
  Contains OpenAPI specs for this feature's API surface.
  Skip generation with --no-contracts flag.
-->

| Contract | Path | Source FRs | Status |
|----------|------|------------|--------|
| Main API | `contracts/api.yaml` | [FR-xxx, FR-yyy] | [GENERATED / MANUAL / N/A] |

#### Generated Endpoints

<!-- Populated from FR-xxx requirements with API keywords -->

| Method | Path | Operation ID | Source FR | Description |
|--------|------|--------------|-----------|-------------|
| POST | /api/v1/{resource} | create{Resource} | FR-xxx | [FR description] |
| GET | /api/v1/{resource}/{id} | get{Resource} | FR-yyy | [FR description] |

## Architecture Decisions

<!--
  PURPOSE: Document all significant architectural decisions with traceability to requirements.

  Auto-generated by Phase 0 of /speckit.plan command using brainstorm-curate protocol.

  FORMAT:
  - Lightweight ADR inline in plan.md (always)
  - Full ADR file in specs/[feature]/adrs/ when:
    - ≥2 alternatives were compared
    - Decision has High impact (affects multiple components)
    - Non-trivial trade-offs exist

  Full ADR template: memory/knowledge/templates/adr-template.md
  Reference format in tasks: [ADR:ADR-001], [ADR:ADR-002]
-->

### ADR-001: [Decision Title]

**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-xxx
**Impact**: High | Medium | Low
**Linked Requirements**: FR-xxx, NFR-xxx
**Decision Date**: YYYY-MM-DD

**Decision**:
[One clear sentence describing what was decided]

**Context**:
[2-3 sentences: What problem does this solve? What constraints exist?]

**Rationale**:
[2-4 sentences: Why this approach? What makes it the best option?]

#### Brainstorm-Curate Evidence

<!--
  REQUIRED for non-trivial decisions (database, caching, auth, deployment, framework).
  Quality Gate: IG-PLAN-009 (Brainstorm-Curate Enforcement)
  Self-Review: SR-PLAN-21 (applied), SR-PLAN-22 (visible)

  Reference: templates/shared/quality/brainstorm-curate.md
-->

**Protocol Applied**: Yes | No (trivial decision)
**Options Generated**: [3-5]

| Criterion | Weight | Opt 1: [Name] | Opt 2: [Name] | Opt 3: [Name] | Opt 4: [Name] | Opt 5: [Name] |
|-----------|:------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| Team Expertise | 3x | [0-10] | [0-10] | [0-10] | [0-10] | [0-10] |
| Maintenance Cost | 2x | [0-10] | [0-10] | [0-10] | [0-10] | [0-10] |
| Scalability | 2x | [0-10] | [0-10] | [0-10] | [0-10] | [0-10] |
| Time to Implement | 1x | [0-10] | [0-10] | [0-10] | [0-10] | [0-10] |
| **Weighted Score** | | **[X]** | **[X]** | **[X]** | **[X]** | **[X]** |

**Selected**: Option [N]: [Name] (highest weighted score)

**Why Not Others**:
- **Option 1**: [Specific disqualifier - not vague]
- **Option 2**: [Specific disqualifier - not vague]
- **Option 3**: [Specific disqualifier - not vague]

**Reversibility**: [Yes/Partially/No] — Pivot cost: [Low/Medium/High]

**Trade-offs Accepted**:
- ✅ **Pros**: [Key benefits of chosen option]
- ❌ **Cons**: [Key drawbacks we accept]
- ⚠️ **Risks**: [What could go wrong and mitigation]

**Implementation Notes**:
[Specific guidance for developers implementing this decision]

**Full ADR**: [specs/[feature]/adrs/ADR-001-slug.md](adrs/ADR-001-slug.md) *(if complex decision)*

---

<!-- Repeat ADR template for ADR-002, ADR-003, etc. -->

### Architecture Decisions Summary

| ADR | Title | Status | Impact | Requirements | Full Doc |
|-----|-------|--------|--------|--------------|----------|
| ADR-001 | [Title] | Accepted | High | FR-xxx, NFR-xxx | [ADR-001](adrs/ADR-001-slug.md) |

**Decision Patterns Applied**:
- [Pattern]: Used in ADR-xxx, ADR-yyy

**Requirement Coverage**:
- Performance (NFR-PERF-xxx): ADR-001, ADR-003
- Security (NFR-SEC-xxx): ADR-002
- Scalability (NFR-REL-xxx): ADR-004

## Pre-Mortem Analysis

<!--
  PURPOSE: Identify preventable failure scenarios BEFORE they happen.
  Establish early warning systems and kill criteria.

  Quality Gate: IG-PLAN-006 (Pre-Mortem Coverage)
  Self-Review: SR-PLAN-15 (3+ scenarios), SR-PLAN-16 (Tech+Integration), SR-PLAN-27 (kill criteria)
  Reference: templates/shared/concept-sections/pre-mortem.md
-->

### Failure Scenarios Summary

| ID | Failure Mode | Category | Probability | Impact | Risk Score | Status |
|:--:|--------------|:--------:|:-----------:|:------:|:----------:|:------:|
| FAIL-001 | [e.g., Database bottleneck under load] | Technical | H/M/L | C/M/L | [1-9] | Monitoring |
| FAIL-002 | [e.g., Third-party API becomes unavailable] | External | H/M/L | C/M/L | [1-9] | Mitigating |
| FAIL-003 | [e.g., Integration complexity underestimated] | Integration | H/M/L | C/M/L | [1-9] | Monitoring |

**Risk Score** = Probability (H:3, M:2, L:1) × Impact (C:3, M:2, L:1)
**Category Coverage**: ☑ Technical ☑ Integration ☐ Team/Resource ☑ External

### FAIL-001: [Failure Mode Name]

**Description**: [What could go wrong and why it matters]

**Early Warning Signs**:
- [ ] [Metric threshold: "Latency P99 > 500ms in staging"]
- [ ] [Pattern: "More than 3 retry attempts per request"]
- [ ] [Dependency signal: "Upstream service degraded"]

**Prevention Strategy**:
| Action | Owner | Due Date | Status |
|--------|:-----:|:--------:|:------:|
| [Preventive measure 1] | [Role] | [Date] | Not Started |
| [Preventive measure 2] | [Role] | [Date] | Not Started |

**Contingency Plan**: [What to do if this failure occurs]

**Kill Criteria**:
```
IF [specific metric] < [threshold] BY [date]:
  THEN [pivot/redesign/escalate to stakeholder]
```

### FAIL-002: [Failure Mode Name]

*[Repeat structure for each failure scenario]*

### FAIL-003: [Failure Mode Name]

*[Repeat structure for each failure scenario]*

## Requirements Traceability Matrix

<!--
  PURPOSE: Bidirectional tracing from requirements to implementation.
  Ensures every FR has implementation and every implementation traces to FR.

  Quality Gate: IG-PLAN-008 (RTM Coverage)
  Self-Review: SR-PLAN-19 (FR Coverage ≥90%), SR-PLAN-20 (No orphans)
  Populated by /speckit.plan, validated by /speckit.analyze Pass J.
-->

### FR Coverage Matrix

| FR-ID | Requirement Summary | ADR-xxx | TASK-xxx (planned) | TEST-xxx (expected) | Status |
|-------|---------------------|---------|--------------------|--------------------|:------:|
| FR-001 | [Brief description] | ADR-001, ADR-003 | T-001, T-002 | TBD | ✓ Covered |
| FR-002 | [Brief description] | ADR-002 | T-003, T-004 | TBD | ✓ Covered |
| FR-003 | [Brief description] | - | T-005 | TBD | ⚠ No ADR |

**FR Coverage**: {covered}/{total} ({percentage}%) — Target: ≥90%

### NFR Coverage Matrix

| NFR-ID | Requirement | ADR-xxx | Monitoring | Alert | Status |
|--------|-------------|---------|------------|-------|:------:|
| NFR-PERF-001 | API P99 <500ms | ADR-004 | [Dashboard] | ALERT-001 | ✓ Planned |
| NFR-REL-001 | 99.9% Availability | ADR-005 | [SLO Dashboard] | ALERT-002 | ✓ Planned |
| NFR-OBS-001 | Trace Coverage | - | [OTel] | - | ✓ Planned |

**NFR Coverage**: {covered}/{total} ({percentage}%)

### Traceability Gaps

<!--
  Auto-populated by self-review. Empty table = no gaps detected.
-->

| Gap Type | Item | Issue | Resolution |
|----------|------|-------|------------|
| Orphan FR | FR-xxx | No ADR or Task reference | Create task in /speckit.tasks |
| Orphan ADR | ADR-xxx | No FR linkage | Link to FR or document as internal |
| Missing Test | FR-xxx | No expected test coverage | Add test task |

### Impact Analysis

<!--
  What happens if upstream spec changes?
-->

| If This Changes... | These Are Affected... | Action Required |
|--------------------|----------------------|-----------------|
| FR-001 scope | ADR-001, TASK-001-003 | Re-evaluate architecture |
| NFR-PERF-001 target | ADR-004, monitoring config | Update thresholds |
| External API version | PKG-002, TASK-010 | Migration required |

## Observability & Monitoring Plan

<!--
  PURPOSE: Define SLIs, SLOs, dashboards, and alerts BEFORE implementation.
  Ensures observability is planned, not retrofitted.

  Quality Gate: IG-PLAN-010 (Observability Defined)
  Self-Review: SR-PLAN-23 (SLI/SLO defined), SR-PLAN-24 (Alerts have runbooks)
  Reference: templates/shared/observability-stack.md
-->

### Service Level Indicators (SLIs)

| SLI ID | Name | Definition | Good Event | Valid Event |
|--------|------|------------|------------|-------------|
| SLI-001 | Request Latency | P99 response time | response_time < 500ms | All HTTP 2xx/4xx |
| SLI-002 | Availability | Successful responses | status_code < 500 | All HTTP requests |
| SLI-003 | Error Rate | Failed requests ratio | status_code >= 500 | All HTTP requests |

### Service Level Objectives (SLOs)

| SLO ID | SLI | Target | Window | Error Budget | Alert Threshold |
|--------|-----|--------|--------|--------------|-----------------|
| SLO-001 | SLI-001 | 99.5% < 500ms | 30 days | 0.5% (3.6 hrs) | 50% budget consumed |
| SLO-002 | SLI-002 | 99.9% success | 30 days | 0.1% (43.8 min) | 50% budget consumed |
| SLO-003 | SLI-003 | <0.1% errors | 30 days | 0.1% | 80% budget consumed |

### Dashboard Specifications

| Dashboard | Purpose | Key Panels | Refresh | Audience |
|-----------|---------|------------|---------|----------|
| Overview | Health at a glance | SLO status, error rate, latency P50/P99 | 30s | On-call, leadership |
| Performance | Deep dive metrics | Latency histogram, throughput, saturation | 10s | Developers |
| Business | Feature adoption | DAU, feature usage, conversion funnel | 5m | Product, leadership |
| Dependency | External health | API latency, error rates, rate limits | 30s | On-call |

### Alert Definitions

| Alert ID | Condition | Severity | Runbook | Notification |
|----------|-----------|:--------:|---------|--------------|
| ALERT-001 | P99 latency > 1000ms for 5m | WARNING | [runbooks/latency.md] | #alerts-warning |
| ALERT-002 | Error rate > 1% for 5m | CRITICAL | [runbooks/errors.md] | #alerts-critical + PagerDuty |
| ALERT-003 | SLO budget < 20% remaining | WARNING | [runbooks/slo-budget.md] | #alerts-warning |
| ALERT-004 | Database connections > 80% | WARNING | [runbooks/database.md] | #alerts-warning |

### Runbook Index

| Runbook | Triggers | Owner | Last Reviewed |
|---------|----------|-------|---------------|
| [runbooks/latency.md] | ALERT-001 | [Team] | [Date] |
| [runbooks/errors.md] | ALERT-002 | [Team] | [Date] |
| [runbooks/slo-budget.md] | ALERT-003 | [Team] | [Date] |
| [runbooks/database.md] | ALERT-004 | [Team] | [Date] |

## Scalability Strategy

<!--
  PURPOSE: Define capacity baseline, scaling thresholds, and bottleneck analysis.
  Ensures the system can grow without architectural rewrites.

  Quality Gate: IG-PLAN-011 (Scalability Planned)
  Self-Review: SR-PLAN-25 (Capacity baseline), SR-PLAN-26 (Scaling triggers)
-->

### Capacity Baseline

| Resource | Current Capacity | 6mo Projected | 12mo Projected | Scaling Strategy |
|----------|------------------|---------------|----------------|------------------|
| API Servers | [2 instances] | [4 instances] | [8 instances] | Horizontal (auto-scale) |
| Database | [1 primary] | [1 primary + 1 replica] | [1 primary + 2 replicas] | Vertical → Read replicas |
| Cache | [1GB Redis] | [2GB Redis] | [4GB Redis Cluster] | Vertical → Cluster |
| Queue Workers | [N/A] | [2 workers] | [4 workers] | Horizontal |
| Storage | [10GB] | [50GB] | [200GB] | Auto-expand |

### Scaling Triggers

| Metric | Warning Threshold | Scale Threshold | Scale Action | Cooldown |
|--------|-------------------|-----------------|--------------|----------|
| CPU Utilization | >60% avg (5m) | >80% avg (5m) | Add instance | 5m |
| Memory Utilization | >70% | >85% | Add instance | 5m |
| Request Queue Depth | >100 | >500 | Add instance | 3m |
| DB Connections | >60% pool | >80% pool | Increase pool / Add replica | 10m |
| Cache Hit Ratio | <80% | <60% | Increase cache size | 15m |

### Bottleneck Analysis

| Component | Current Limit | Risk Level | Mitigation | When to Implement |
|-----------|---------------|:----------:|------------|-------------------|
| Database Writes | ~500 QPS | High | Connection pooling, write batching | Before 10K users |
| External API | 100 req/min (rate limited) | High | Caching, request batching | Immediately |
| Single Region | N/A | Medium | Multi-region deployment | Before 50K users |
| Synchronous Processing | ~200 req/s | Medium | Async job queue | Before 20K users |

### Growth Milestones

| Milestone | Users | Traffic | Architecture Changes Required |
|-----------|-------|---------|-------------------------------|
| Launch | 100 | 10 RPS | None (current architecture sufficient) |
| Early Adoption | 1,000 | 100 RPS | Add auto-scaling, implement caching |
| Growth | 10,000 | 1,000 RPS | Add read replicas, CDN for static assets |
| Scale | 100,000 | 10,000 RPS | Database sharding, microservices extraction |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── design.md            # UI specs (/speckit.design command - for UI features)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── adrs/                # Architecture Decision Records (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   │   └── ui/           # Design system primitives (Button, Input, etc.)
│   ├── styles/
│   │   └── tokens.css    # Design tokens (colors, spacing, typography)
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

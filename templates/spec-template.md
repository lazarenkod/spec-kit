# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Status**: Draft
**Input**: User description: "$ARGUMENTS"

## Concept Reference *(if applicable)*

<!--
  If this spec was created from a concept.md, reference the source here.
  This enables traceability from high-level concept to detailed specification.
-->

**Source Concept**: [Link to specs/concept.md or "N/A" if created without concept]
**Concept IDs Covered**: [EPIC-001.F01.S01, EPIC-001.F01.S02, ... or "N/A"]

## Feature Lineage *(for modifications of merged features)*

<!--
  INCLUDE THIS SECTION ONLY when this feature extends/modifies an already-merged feature.
  Leave empty or delete for completely new features (greenfield).

  This section establishes traceability between features:
  - Parent features that this feature extends
  - Relationship type (how this feature relates to parent)
  - System specs affected by both parent and this feature

  Use /speckit.extend to auto-populate this section.
-->

**Extends Feature(s)**:

| Parent Feature | Relationship | System Specs Affected |
|----------------|--------------|----------------------|
| <!-- e.g., [001-login](../001-login/spec.md) --> | <!-- EXTENDS/REFINES/FIXES/DEPRECATES --> | <!-- e.g., system/auth/login.md --> |

**Relationship Types**:
- `EXTENDS`: Adds new capability to parent feature's functionality
- `REFINES`: Improves or modifies parent feature's behavior
- `FIXES`: Corrects issues or bugs in parent feature
- `DEPRECATES`: Replaces functionality from parent feature

**Context from Parent**:

<!--
  If extending a merged feature, summarize relevant context:
  - Key design decisions from parent that must be respected
  - Constraints that carry over to this feature
  - Integration points with parent's implementation
  - Business rules inherited from parent
-->

[Summarize inherited context here, or "N/A" for new features]

---

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Priority Format (use sub-priorities for large projects):
  - P1a, P1b, P1c: MVP critical path (ordered sequence)
  - P2a, P2b: Important but can be added post-MVP
  - P3: Nice-to-have, future enhancements

  For smaller projects, simple P1, P2, P3 is sufficient.

  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1a)

[Describe this user journey in plain language]

**Concept Reference**: [EPIC-001.F01.S01 or "N/A"]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

<!--
  IMPORTANT: Each scenario has a unique ID (AS-NNN) for traceability.
  These IDs will be referenced in tasks.md to ensure test coverage.
  Format: AS-[story number][scenario letter], e.g., AS-1A, AS-1B, AS-2A

  "Classification" column (auto-assigned by acceptance-criteria-generator):
  - HAPPY_PATH = Primary success flow, expected user journey
  - ALT_PATH = Alternate valid paths, secondary success flows
  - ERROR_PATH = Failure scenarios, validation errors, exceptions
  - BOUNDARY = Min/max values, empty states, edge conditions
  - SECURITY = Authentication, authorization, injection prevention

  "Requires Test" column:
  - YES = Automated test REQUIRED in tasks.md (enforced by Pass W in /speckit.analyze)
  - NO = No automated test needed (e.g., UI-only, manual validation)
  If YES but no test is feasible, use [NO-TEST:AS-xxx] with justification in tasks.md.
-->

| ID | Classification | Given | When | Then | Requires Test |
|----|----------------|-------|------|------|---------------|
| AS-1A | HAPPY_PATH | [initial state] | [action] | [expected outcome] | YES |
| AS-1B | ERROR_PATH | [initial state] | [action] | [expected outcome] | YES |

---

### User Story 2 - [Brief Title] (Priority: P1b)

[Describe this user journey in plain language]

**Concept Reference**: [EPIC-001.F01.S02 or "N/A"]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

| ID | Classification | Given | When | Then | Requires Test |
|----|----------------|-------|------|------|---------------|
| AS-2A | HAPPY_PATH | [initial state] | [action] | [expected outcome] | YES |

---

### User Story 3 - [Brief Title] (Priority: P2a)

[Describe this user journey in plain language]

**Concept Reference**: [EPIC-001.F02.S01 or "N/A"]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

| ID | Classification | Given | When | Then | Requires Test |
|----|----------------|-------|------|------|---------------|
| AS-3A | ALT_PATH | [initial state] | [action] | [expected outcome] | NO |

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.

  Edge cases should have IDs for traceability (EC-NNN format).

  Columns:
  - Severity: CRITICAL | HIGH | MEDIUM | LOW
    - CRITICAL = Security-related, data-integrity, or system-breaking (test REQUIRED)
    - HIGH = Important validation or business logic (test strongly recommended)
    - MEDIUM = Quality improvement (test recommended)
    - LOW = Minor edge case (test optional)
  - Category: security | validation | boundary | concurrency | integration | performance

  Auto-generated edge cases from entity-type heuristics and security patterns
  will have confidence scores (0.60-0.95) noted in comments.
-->

| ID | Condition | Expected Behavior | Severity | Category |
|----|-----------|-------------------|----------|----------|
| EC-001 | [boundary condition] | [expected behavior] | MEDIUM | boundary |
| EC-002 | [security: auth bypass attempt] | [expected behavior] | CRITICAL | security |
| EC-003 | [validation: invalid email format] | [validation error with message] | HIGH | validation |

### Edge Case Coverage Summary

<!--
  This summary is auto-populated by edge-case-detector subagent.
  It tracks coverage across entity types and security categories.
-->

| Category | Count | Triggers Detected | Coverage Status |
|----------|-------|-------------------|-----------------|
| Security | N | [auth, input, etc.] | ✅ Covered / ⚠️ Partial |
| Validation | N | [entity types found] | ✅ Covered / ⚠️ Partial |
| Boundary | N | - | ✅ Covered / ⚠️ Partial |
| Concurrency | N | - | ✅ Covered / ⚠️ Partial |

**Completeness Score**: X.XX / 1.00 (threshold: >= 0.80)

**Gaps Identified**:
- [Any missing coverage noted by edge-case-detector]

### Property-Based Testing Hints

> Auto-generated hints for `/speckit.properties`. Manual additions welcome.

| ID | Type | Derived From | Formula | Generator Hint | Priority |
|----|------|--------------|---------|----------------|----------|
| PROP-001 | inverse | AS-1A | `delete(create(x)) == not_exists(x)` | valid_{{entity}} | P1 |
| PROP-002 | idempotent | FR-xxx | `normalize(normalize(x)) == normalize(x)` | boundary_string | P2 |
| PROP-003 | invariant | NFR-xxx | `len(result) <= MAX_SIZE` | any_input | P1 |
| PROP-004 | boundary | EC-xxx | `validate(invalid) throws ValidationError` | invalid_{{field}} | P1 |

#### Property Type Reference

- **inverse**: Round-trip operations (create/delete, encode/decode, serialize/deserialize)
- **idempotent**: Repeated application yields same result (save, normalize, format)
- **invariant**: Conditions that always hold (size limits, type constraints)
- **boundary**: Edge case behavior (empty, null, max values)
- **commutative**: Order-independent operations (set union, addition)
- **model**: State machine conformance (workflow transitions)

### Completeness Analysis

<!--
  This section is auto-populated by completeness-checker subagent.
  It validates spec completeness across multiple dimensions.
  See templates/shared/quality/completeness-checklist.md for details.
-->

| Category | Status | Details |
|----------|--------|---------|
| Error Handling | ✅/⚠️/❌ | X error scenarios for Y happy paths |
| Security | ✅/⚠️/❌ | Auth/Input/Data protection coverage |
| Performance | ✅/⚠️/❌ | Latency/throughput requirements defined |
| Observability | ✅/⚠️/❌ | Logging/metrics/alerting requirements |
| Accessibility | ✅/⚠️/❌ | WCAG compliance (UI features only) |
| Prerequisites | ✅/⚠️/❌ | Technical dependencies documented |

**Completeness Score**: X.XX / 1.00 (threshold: >= 0.75)

**Status Legend**:
- ✅ Covered: Category requirements fully specified
- ⚠️ Partial: Some requirements missing or incomplete
- ❌ Missing: Critical requirements not addressed

**Gaps Requiring Attention**:
- [Any missing requirements identified by completeness-checker]

### Specification Quality Score

<!--
  This section is auto-populated by spec-quality-scorer subagent.
  It provides multi-dimensional quality assessment using G-Eval framework.
  See templates/shared/quality/spec-quality-scorer.md for details.

  Grade Scale:
  - A (90-100): Excellent — Ship with confidence
  - B (80-89): Good — Minor improvements recommended
  - C (70-79): Acceptable — Address suggestions before implementation
  - D (60-69): Below Standard — Significant gaps, needs work
  - F (< 60): Failing — Major revision required

  Pass Threshold: 70.0 (Grade C or higher)
-->

**Overall Score**: XX.X / 100 (Grade: X)
**Status**: ✅ PASSED | ❌ FAILED
**Recommendation**: [Ship with confidence | Minor improvements | Address suggestions | Needs revision | Major revision required]

| Dimension | Score | Weight | Explanation |
|-----------|-------|--------|-------------|
| Clarity | X.XX | 25% | Ambiguities: N (X critical, Y high). LLM clarity: X.XX |
| Completeness | X.XX | 25% | N gaps (X critical, Y high, Z medium) |
| Testability | X.XX | 20% | Testable: X%, FR→AS traceability: Y% |
| Consistency | X.XX | 15% | N contradictions (X critical, Y high) |
| Traceability | X.XX | 15% | FR→AS: X%, FR→EC: Y%, Orphans: N |

**Quality Gates**:
- SR-SPEC-19 (Overall >= 70): ✅/❌
- SR-SPEC-20 (All dimensions >= 0.50): ✅/❌
- SR-SPEC-21 (No CRITICAL contradictions): ✅/❌

**Improvement Suggestions**:
1. [Highest priority suggestion from lowest-scoring dimension]
2. [Second priority suggestion]
3. [Third priority suggestion]

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.

  Each requirement has a unique ID (FR-NNN) that will be referenced in tasks.md
  to ensure implementation coverage.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
  - *Acceptance Scenarios*: AS-1A, AS-1B

- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]
  - *Acceptance Scenarios*: AS-1A

- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
  - *Acceptance Scenarios*: AS-2A

- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
  - *Acceptance Scenarios*: AS-3A

- **FR-005**: System MUST [behavior, e.g., "log all security events"]
  - *Acceptance Scenarios*: [list relevant AS-IDs]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Non-Functional Requirements *(mandatory)*

<!--
  NFRs define HOW the system should perform, not WHAT it does.
  Every spec MUST include at least 3 NFRs covering:
  - Performance (NFR-PERF-xxx)
  - Security (NFR-SEC-xxx)
  - Reliability (NFR-REL-xxx)

  Additional categories (use as needed):
  - Scalability (NFR-SCAL-xxx)
  - Observability (NFR-OBS-xxx)
  - Accessibility (NFR-A11Y-xxx)
  - Compliance (NFR-CMP-xxx)
  - Maintainability (NFR-MNT-xxx)

  NFR ID Format: NFR-[CATEGORY]-[NUMBER]
  Each NFR should have:
  - Quantified metric (not "fast" but "<200ms p95")
  - Measurement method
  - Acceptance threshold
-->

#### Performance Requirements

- **NFR-PERF-001**: API response time MUST be <[X]ms p95 under normal load
  - *Measurement*: APM/Load testing
  - *Threshold*: p95 < [X]ms, p99 < [Y]ms
  - *Acceptance Scenarios*: AS-NFR-001

- **NFR-PERF-002**: System MUST handle [X] concurrent users without degradation
  - *Measurement*: Load testing with [tool]
  - *Threshold*: [X] users with <5% error rate
  - *Acceptance Scenarios*: AS-NFR-002

#### Security Requirements

- **NFR-SEC-001**: All data in transit MUST use TLS 1.3
  - *Measurement*: SSL Labs scan
  - *Threshold*: Grade A+
  - *Acceptance Scenarios*: AS-NFR-003

- **NFR-SEC-002**: Authentication tokens MUST expire within [X] hours
  - *Measurement*: Security audit
  - *Threshold*: Token TTL ≤ [X]h, refresh token ≤ [Y]d
  - *Acceptance Scenarios*: AS-NFR-004

#### Reliability Requirements

- **NFR-REL-001**: System availability MUST be ≥[X]% ([N] nines)
  - *Measurement*: Uptime monitoring
  - *Threshold*: Monthly uptime ≥ [X]%
  - *Acceptance Scenarios*: AS-NFR-005

- **NFR-REL-002**: System MUST recover from failures within [RTO]
  - *Measurement*: Chaos engineering / DR drill
  - *Threshold*: RTO ≤ [X] minutes
  - *Acceptance Scenarios*: AS-NFR-006

#### [Optional: Additional NFR Categories]

<!--
  Add sections as needed:
  - Scalability: horizontal/vertical scaling requirements
  - Observability: logging, metrics, tracing requirements
  - Accessibility: WCAG compliance level
  - Compliance: regulatory requirements (GDPR, SOC2, etc.)
  - Maintainability: code coverage, documentation requirements
-->

### NFR Acceptance Scenarios

<!--
  NFRs need acceptance scenarios just like FRs.
  These scenarios are typically validated through:
  - Load testing
  - Security scanning
  - Chaos engineering
  - Compliance audits
-->

| ID | NFR | Given | When | Then | Validation Method |
|----|-----|-------|------|------|-------------------|
| AS-NFR-001 | NFR-PERF-001 | System under normal load | API request sent | Response in <[X]ms p95 | Load test |
| AS-NFR-002 | NFR-PERF-002 | [X] concurrent users | All users perform actions | Error rate <5% | Load test |
| AS-NFR-003 | NFR-SEC-001 | HTTPS connection attempted | TLS handshake | TLS 1.3, Grade A+ | SSL Labs |
| AS-NFR-004 | NFR-SEC-002 | Valid auth token issued | [X] hours elapsed | Token expired | Security audit |
| AS-NFR-005 | NFR-REL-001 | System running for 30 days | Uptime calculated | Availability ≥[X]% | Monitoring |
| AS-NFR-006 | NFR-REL-002 | System component failed | Recovery initiated | Service restored within RTO | DR drill |

### Visual & Interaction Requirements *(for UI features)*

<!--
  Include this section if the feature has significant user interface.
  Skip for API-only, CLI, or backend features.

  These requirements are technology-agnostic but UI-specific.
  They will be detailed further in design.md if /speckit.design is run.
-->

**VR-001**: [Visual requirement with measurable criteria]
- Example: "Primary action buttons MUST have minimum touch target of 44x44px"
- *Acceptance Scenarios*: [AS-IDs that involve this visual element]

**VR-002**: [Visual requirement]
- Example: "Form validation errors MUST appear inline below the field"
- *Acceptance Scenarios*: [AS-IDs]

**IR-001**: [Interaction requirement with timing]
- Example: "System MUST show loading indicator within 100ms of action"
- *Acceptance Scenarios*: [AS-IDs]

**IR-002**: [Interaction requirement]
- Example: "Modal dialogs MUST be dismissible via Escape key and outside click"
- *Acceptance Scenarios*: [AS-IDs]

### Design Constraints *(for UI features)*

<!--
  Constraints that will guide /speckit.design decisions.
-->

- **Design System**: [Existing system to follow / New system to create / N/A]
  <!-- Figma: paste URL like https://www.figma.com/file/{file_key}/... for auto-import -->
  <!-- Storybook: paste URL for component reference -->
  <!-- Tokens: path to design-tokens.json for local tokens -->
- **Accessibility Level**: WCAG 2.1 [A / AA / AAA]
- **Responsive Breakpoints**: [mobile-first / desktop-first / specific breakpoints]
- **Browser Support**: [matrix, e.g., "Last 2 versions of Chrome, Firefox, Safari, Edge"]
- **Device Support**: [desktop / tablet / mobile / all]

### UI Acceptance Scenarios *(for UI features)*

<!--
  Additional acceptance scenarios specific to visual and interaction behavior.
  These complement the main Acceptance Scenarios in User Stories.
  UI scenarios typically have "Requires Test = NO" unless E2E testing is available.
-->

| ID | Given | When | Then | Requires Test |
|----|-------|------|------|---------------|
| AS-UI-001 | User is on mobile device | User taps submit button | Button shows loading spinner within 100ms | NO |
| AS-UI-002 | User is filling form | User leaves required field empty | Field shows red border and error message | NO |
| AS-UI-003 | Modal is open | User presses Escape | Modal closes with fade animation | NO |

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]
---

## Non-Functional Requirements *(mandatory)*

<!--
  ACTION REQUIRED: Define performance, security, and compliance requirements.
  These are critical for architectural decisions and must be specified upfront.
  Reference: memory/domains/security.md for Security by Design principles.
-->

### Performance Requirements

| Endpoint/Operation | p99 Target | Critical Threshold | Notes |
|--------------------|------------|-------------------|-------|
| GET /api/v1/[resource] | < 200ms | < 500ms | Public read |
| POST /api/v1/[resource] | < 1s | < 2s | Transactional write |
| Background job [name] | < 30s | < 60s | Async processing |

**Throughput Requirements**:
- Peak RPS: [expected requests per second]
- Concurrent users: [expected concurrent users]

### Security Requirements

<!--
  Apply Security by Design principles (SBD-001 to SBD-005).
  Use STRIDE threat modeling for critical features.
  Reference: templates/shared/security/threat-model-template.md
-->

| Requirement ID | Description | Auth Required | Roles | Data Classification |
|----------------|-------------|---------------|-------|---------------------|
| SEC-[FEATURE]-001 | [Operation description] | Yes/No | [Roles] | [Classification] |
| SEC-[FEATURE]-002 | [Operation description] | Yes/No | [Roles] | [Classification] |

**Data Classification Legend** (per security.md):
- **Public**: No restrictions
- **Internal**: Company internal only
- **Confidential**: Business-sensitive (PII, financial)
- **Restricted**: Highly sensitive (credentials, keys)

**OWASP Considerations** (check applicable):
- [ ] A01: Broken Access Control - [mitigation approach]
- [ ] A02: Cryptographic Failures - [mitigation approach]
- [ ] A03: Injection - [mitigation approach]
- [ ] A07: Authentication Failures - [mitigation approach]

### Compliance Requirements

- [ ] **PII Handling**: [describe what PII is collected, how it's protected]
- [ ] **Audit Logging**: [what events must be logged, retention period]
- [ ] **Data Retention**: [retention period, deletion policy]
- [ ] **GDPR/CCPA**: [applicable regulations, consent requirements]
- [ ] **Industry Standards**: [PCI-DSS, HIPAA, SOC2 if applicable]

---

## Events *(for event-driven features)*

<!--
  INCLUDE THIS SECTION when feature produces or consumes async events.
  Document event schemas, producers, consumers for event-driven architecture.

  Skip for:
  - Synchronous-only features
  - Features not participating in event bus
-->

### Events Produced

| Event Name | Schema | Trigger | Consumers |
|------------|--------|---------|-----------|
| [Feature]Created | [Avro/JSON Schema link] | [When triggered] | [consumer-services] |
| [Feature]Updated | [Schema link] | [When triggered] | [consumer-services] |

### Events Consumed

| Event Name | Schema | Producer | Handler |
|------------|--------|----------|---------|
| [Dependency]Completed | [Schema link] | [producer-service] | [Handler.method()] |

### Event Schema Example

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "[EventName]",
  "type": "object",
  "required": ["id", "timestamp", "payload"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object" }
  }
}
```

---

## Technical Dependencies *(for features with external integrations)*

<!--
  IMPORTANT: Document all external dependencies that AI agents must reference.
  This prevents hallucination of non-existent APIs and ensures version compatibility.

  Types:
  - NPM/PyPI packages with specific versions
  - External REST APIs (Stripe, AWS, Firebase, etc.)
  - Frameworks with version-specific features

  For each dependency, provide:
  - Version constraints
  - Official documentation URL
  - Key methods/endpoints to be used

  Skip this section if feature has no external integrations.
-->

### Package Dependencies

| ID | Package | Version | Documentation URL | Purpose |
|----|---------|---------|-------------------|---------|
| PKG-001 | [package-name] | ^X.Y.Z | [official docs URL] | [why needed] |

### External API Dependencies

| ID | API | Version | Base URL | Documentation | Auth Method |
|----|-----|---------|----------|---------------|-------------|
| API-001 | [API name] | v1 | [base endpoint] | [docs URL] | [OAuth2/API Key/etc.] |

### Framework Requirements

<!--
  NOTE: UI frameworks listed here (React, Vue, Angular, Svelte, Next.js, Nuxt, SvelteKit)
  will trigger automatic component library recommendations when running /speckit.design.
  See templates/shared/library-recommendations.md for framework → library mapping.

  Example: "React 18 + TypeScript" → recommends shadcn/ui
           "Vue.js 3" → recommends Vuetify
           "Angular 17" → recommends Angular Material
-->

| ID | Framework | Version | Documentation | Critical Features Used |
|----|-----------|---------|---------------|------------------------|
| FW-001 | [framework] | ^X.Y.Z | [docs URL] | [feature1, feature2] |

### Deprecated API Warnings

<!--
  List any APIs/methods that are deprecated but might be suggested by AI agents
  based on older training data. This prevents hallucination of outdated patterns.
-->

| Deprecated | Replacement | Since Version | Migration Docs |
|------------|-------------|---------------|----------------|
| [old method/API] | [new method/API] | [version] | [migration URL] |

## Infrastructure Requirements *(for features requiring infrastructure)*

<!--
  INCLUDE THIS SECTION when the feature requires cloud infrastructure beyond
  what exists in the current deployment. This enables /speckit.ship to
  provision and deploy the feature autonomously.

  Infrastructure is tied to ENVIRONMENTS, not features - meaning multiple
  features share the same database, cache, etc. in a given environment.

  Skip this section for:
  - Features that work with existing infrastructure
  - Frontend-only features
  - CLI tools that run locally

  Run /speckit.ship to provision, deploy, and verify the feature.
-->

### Required Services

<!--
  List all infrastructure services needed for this feature.
  These will be translated to infra.yaml and provisioned via Terraform.

  Types: database, cache, queue, storage, compute, network, secret
  Config should specify requirements without implementation details.
-->

| ID | Type | Service | Config | Environments | Notes |
|----|------|---------|--------|--------------|-------|
| INFRA-001 | database | PostgreSQL 16 | 2vCPU, 4GB RAM, 50GB SSD | staging, production | Primary data store |
| INFRA-002 | cache | Redis 7 | 1GB, single node | all | Session/cache storage |
| INFRA-003 | storage | S3-compatible | 10GB, versioned | all | File uploads |

### Environment Configuration

<!--
  Define environment-specific variations.
  Local environment uses docker-compose; staging/production use Terraform.
-->

**Local (docker-compose)**:
- All services run as containers
- Data persists in Docker volumes
- No external network access required

**Staging**:
- Uses managed cloud services
- Feature isolation via namespaces
- Shared database with feature-specific schemas

**Production**:
- High-availability configuration
- Multi-AZ deployment where applicable
- Automated backups enabled

### Connection Requirements

<!--
  Document how the application connects to infrastructure.
  These become environment variables in deploy.yaml.
-->

| Environment Variable | Source | Example |
|---------------------|--------|---------|
| DATABASE_URL | INFRA-001 | `postgres://user:pass@host:5432/db` |
| REDIS_URL | INFRA-002 | `redis://host:6379` |
| S3_ENDPOINT | INFRA-003 | `https://s3.cloud.example.com` |
| S3_BUCKET | INFRA-003 | `feature-uploads` |

### Verification Endpoints

<!--
  Define health check endpoints for /speckit.ship verification.
  These are used by verify.yaml to confirm successful deployment.
-->

| Endpoint | Expected Status | Purpose |
|----------|-----------------|---------|
| `/health` | 200 | Basic application health |
| `/ready` | 200 | Dependencies connected |
| `/api/v1` | 200 | API is responding |

---

## Cross-Repository Dependencies *(for multi-repo workspaces)*

<!--
  INCLUDE THIS SECTION when this feature depends on or is depended upon by
  features in other repositories within the workspace.

  Use format: repo-alias:feature-id (e.g., api:002-payment-api, web:005-checkout)

  Skip this section for:
  - Single-repository projects
  - Features with no cross-repo dependencies

  Run `specify workspace list` to see available repository aliases.
-->

### Dependencies on Other Repositories

<!--
  List features in other repos that THIS feature depends on.
  These should be implemented/available before this feature can be completed.
-->

| This Feature | Depends On | Dependency Type | Reason |
|--------------|------------|-----------------|--------|
| [current-repo:XXX-this-feature] | [other-repo:XXX-feature] | REQUIRES | [Why this dependency exists] |

### Features Depending on This

<!--
  List features in other repos that depend on THIS feature.
  Useful for understanding impact and prioritization.
-->

| External Feature | Dependency Type | Notes |
|------------------|-----------------|-------|
| [other-repo:XXX-feature] | REQUIRES | [How they depend on this feature] |

### Dependency Types Reference

| Type | Description |
|------|-------------|
| REQUIRES | Hard dependency - target must be implemented first |
| BLOCKS | This feature blocks the target from completion |
| EXTENDS | Extends functionality of the target feature |
| IMPLEMENTS | Implements a contract/interface defined by target |
| USES | Soft dependency - uses target but doesn't strictly require it |

---

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]

---

## User Experience Quality *(UXQ domain)*

<!--
  INCLUDE THIS SECTION when UXQ domain is applied (memory/constitution.domain.md = uxq.md).
  These sections ensure product thinking and user empathy are documented alongside technical requirements.

  Skip this section for:
  - API-only features without user-facing components
  - CLI tools (unless targeting non-technical users)
  - Internal/backend services

  See memory/domains/uxq.md for principle definitions.
-->

### Jobs to Be Done

<!--
  Document the user jobs this feature helps accomplish.
  Format: "When [situation], I want to [motivation], so I can [outcome]."
  Each FR should trace to at least one JTBD.
-->

| ID | Job Statement | Related FRs | Priority |
|----|---------------|-------------|----------|
| JTBD-001 | When [situation], I want to [motivation], so I can [outcome] | FR-001, FR-002 | P1a |
| JTBD-002 | When [situation], I want to [motivation], so I can [outcome] | FR-003 | P1b |

### User Mental Model

<!--
  Document how users think about this feature's domain.
  This prevents building features that work correctly but feel wrong.

  Include:
  - Key concepts users already understand
  - Terminology users expect (vs. internal jargon)
  - Analogies users draw to familiar systems
  - Assumptions users bring to the interaction
-->

**Domain Understanding**:
- Users expect [concept] to work like [familiar analogy]
- Users call this "[user term]" not "[internal term]"
- Users assume [common assumption]

**Terminology Mapping**:

| User Term | System Term | Notes |
|-----------|-------------|-------|
| [what users say] | [what system calls it] | [when to use which] |

### First-Time User Experience (FTUE)

<!--
  Document the initial interaction for new users.
  New users have different needs than power users - document both.

  UXQ-006 requires FTUE to be documented separately from repeat-use flows.
-->

**Entry Point**: [How do first-time users discover/access this feature?]

**Initial State**:
- [What do first-time users see?]
- [Empty state handling]

**Guidance Approach**:
- [ ] Onboarding wizard / tutorial
- [ ] Contextual hints / tooltips
- [ ] Sample data / templates
- [ ] None needed (self-explanatory)

**First Meaningful Action**: [What action should new users take first? Why?]

**Success Moment**: [How do users know they've succeeded? What feedback do they get?]

### Friction Points

<!--
  CRITICAL: Every friction point MUST be justified (UXQ-003).
  Unjustified friction = design debt = user abandonment.

  Friction types:
  - SECURITY: Required for protection (auth, confirmation)
  - LEGAL: Required by regulations (consent, terms)
  - DATA QUALITY: Required for system integrity (validation)
  - INTENTIONAL: Slows users down deliberately (prevent mistakes)
  - TECHNICAL: Limitation we can't easily remove (performance)
-->

| ID | Friction Point | Type | Justification | Mitigation |
|----|----------------|------|---------------|------------|
| FP-001 | [what slows user down] | SECURITY | [why necessary] | [how we minimize impact] |
| FP-002 | [what slows user down] | DATA QUALITY | [why necessary] | [how we minimize impact] |

**Unjustified Friction** (must be eliminated):
- [ ] None identified
- [ ] [Friction] - Removal planned in [task/PR]

### Delight Opportunities

<!--
  Document opportunities to exceed user expectations (UXQ-004).
  Delight moments build loyalty and differentiate the product.

  Types:
  - CELEBRATION: Acknowledge user achievements
  - ANTICIPATION: Predict user needs before they ask
  - RECOVERY: Turn failures into positive experiences
  - EASTER EGG: Unexpected pleasant surprises
-->

| ID | Moment | Type | Implementation Idea | Priority |
|----|--------|------|---------------------|----------|
| DM-001 | [when user achieves X] | CELEBRATION | [confetti, message, badge] | SHOULD |
| DM-002 | [when system prevents error] | ANTICIPATION | [smart defaults, autofill] | SHOULD |

### Emotional Journey

<!--
  Map expected emotional states at key points (UXQ-002).
  Helps identify where to add support/delight and reduce friction.

  Emotions: Curious → Confused → Frustrated → Anxious → Relieved → Satisfied → Delighted
-->

| Journey Step | Expected Emotion | Design Response |
|--------------|------------------|-----------------|
| [discovery/entry] | [emotion] | [how we support this] |
| [first action] | [emotion] | [how we support this] |
| [challenge/friction] | [emotion] | [how we support this] |
| [success/completion] | [emotion] | [how we support this] |

### Accessibility as Empowerment

<!--
  Frame accessibility as expanding capabilities, not just compliance (UXQ-010).
  Document specific ways this feature empowers diverse users.
-->

**Target Level**: WCAG 2.1 [A / AA / AAA]

**Empowerment Goals**:
- Users with [ability difference] can [achieve outcome] because [how we enable it]
- Users in [challenging context] can [achieve outcome] because [how we enable it]

**Specific Accommodations**:

| User Need | How We Accommodate | Why It Matters |
|-----------|-------------------|----------------|
| Screen reader users | [specific approach] | [user outcome] |
| Keyboard-only users | [specific approach] | [user outcome] |
| Low vision users | [specific approach] | [user outcome] |
| Users with motor differences | [specific approach] | [user outcome] |

---

## Traceability Summary *(auto-generated)*

<!--
  This section summarizes the traceability relationships for this spec.
  It will be populated/validated by /speckit.analyze.
-->

### Functional Requirements

| Requirement | Acceptance Scenarios | Edge Cases | Status |
|-------------|---------------------|------------|--------|
| FR-001 | AS-1A, AS-1B | EC-001 | Defined |
| FR-002 | AS-1A | - | Defined |
| FR-003 | AS-2A | EC-002 | Defined |

### Visual & Interaction Requirements *(for UI features)*

| Requirement | Acceptance Scenarios | Design Spec | Status |
|-------------|---------------------|-------------|--------|
| VR-001 | AS-UI-001 | design.md | Defined |
| VR-002 | AS-UI-002 | design.md | Defined |
| IR-001 | AS-UI-001 | design.md | Defined |
| IR-002 | AS-UI-003 | design.md | Defined |

---

## Test Strategy

<!--
  Documents the overall testing approach for this feature.
  Validated by Pass W in /speckit.analyze.
-->

### Coverage Summary

| Category | Total | Requires Test | Coverage Target |
|----------|-------|---------------|-----------------|
| Acceptance Scenarios (AS) | 4 | 3 | 100% of YES |
| UI Acceptance Scenarios (AS-UI) | 3 | 0 | N/A (manual) |
| Edge Cases (EC) | 3 | 2 (CRITICAL/HIGH) | 100% of CRITICAL, 80% of HIGH |

### Test Types Required

- [ ] **Unit Tests**: For FR with pure logic (validation, calculations)
- [ ] **Integration Tests**: For FR with external dependencies (API, DB)
- [ ] **E2E Tests**: For critical user journeys (AS with Requires Test = YES)

### Untestable Scenarios

<!--
  List scenarios marked "Requires Test = NO" with justification.
  Use this to communicate to /speckit.tasks what [NO-TEST:] markers are valid.
-->

| Scenario | Justification |
|----------|---------------|
| AS-3A | [e.g., "UI-only behavior, validated by visual review"] |
| AS-UI-* | UI scenarios validated through design review and manual QA |

### Test Infrastructure Requirements

<!--
  Document any prerequisites for test execution.
  This informs /speckit.plan Phase 0.5 verification.
-->

- **Test Framework**: [e.g., Jest, pytest, vitest]
- **Mock Requirements**: [e.g., "Mock external payment API"]
- **Fixtures Required**: [e.g., "User fixtures with various roles"]
- **Environment Variables**: [e.g., "TEST_API_KEY required"]

---

## System Spec Impact *(mandatory for merge)*

<!--
  IMPORTANT: This section defines how this feature affects system specifications.
  It is used by /speckit.merge to update living documentation after PR merge.

  System specs live in specs/system/ and represent CURRENT system behavior.
  Feature specs (this file) represent HISTORICAL requirements.
-->

### Creates

<!-- New system specs this feature introduces (will be created by /speckit.merge) -->

| System Spec | Domain | Description |
|-------------|--------|-------------|
| `system/[domain]/[name].md` | [domain] | [What this new system spec documents] |

### Updates

<!-- Existing system specs this feature modifies (will be updated by /speckit.merge) -->

| System Spec | Changes | Breaking? |
|-------------|---------|-----------|
| `system/[domain]/[name].md` | [What behavior changes] | No |

### Breaking Changes

<!--
  Any changes that break existing behavior or API contracts.
  Requires migration plan and version bump.
-->

| System Spec | Breaking Change | Migration Path |
|-------------|-----------------|----------------|
| `system/[domain]/[name].md` | [What breaks] | [How clients should adapt] |

### No Impact

<!--
  Check this if the feature doesn't affect any system specs.
  This is rare - most features should create or update at least one system spec.
-->

- [ ] This feature is internal refactoring with no external behavior change
- [ ] This feature only adds tests/documentation without behavior change

---

## Change Specification *(brownfield only)*

<!--
  INCLUDE THIS SECTION ONLY FOR BROWNFIELD PROJECTS

  Brownfield = modifying existing codebase (existing system, existing code, existing behavior)
  Greenfield = new project from scratch (skip this entire section)

  This section implements Change-Based Architecture where you specify:
  - WHAT EXISTS (Current State)
  - WHAT CHANGES (Delta)
  - WHAT REMAINS (Preserved Behaviors)

  Delete this section entirely for greenfield projects.
-->

**Change Type**: [ Enhancement | Refactor | Migration | Bugfix | Performance | Security ]

<!--
  Enhancement: Adding new capability to existing system
  Refactor: Restructuring without changing external behavior
  Migration: Moving from one technology/pattern to another
  Bugfix: Correcting incorrect behavior
  Performance: Optimizing existing functionality
  Security: Addressing security vulnerabilities
-->

### Current State Analysis

<!--
  Document the CURRENT system behavior before proposing changes.
  Reference baseline.md if generated by /speckit.baseline.
  Each CB-xxx ID enables traceability from current behavior to change requests.
-->

**Baseline Reference**: [`FEATURE_DIR/baseline.md`] *(if generated by /speckit.baseline)*

| ID | Component | Current Behavior | System Spec Reference | Code Location |
|----|-----------|------------------|----------------------|---------------|
| CB-001 | [component name] | [what it does now] | [`system/xxx.md`] | `src/path/file.py:42` |
| CB-002 | [component name] | [what it does now] | [`system/xxx.md`] | `src/path/file.py:128` |

### Current Limitations

<!--
  Why does the current state need to change?
  Each CL-xxx links a limitation to a change request.
-->

| ID | Limitation | Impact | Affected CB |
|----|------------|--------|-------------|
| CL-001 | [what's wrong or missing] | [business/user impact] | CB-001 |
| CL-002 | [what's wrong or missing] | [business/user impact] | CB-001, CB-002 |

### Change Delta

<!--
  The heart of Change-Based Architecture: explicit delta specification.
  Each CHG-xxx is a discrete change request with clear scope.

  Delta Types:
  - ADD: New capability that doesn't exist today
  - MODIFY: Change existing behavior (preserves interface)
  - REPLACE: Swap implementation (may change interface)
  - REMOVE: Delete existing capability
  - DEPRECATE: Mark for future removal (not immediate)
-->

| ID | Delta Type | What Changes | From (CB) | To (Desired) | Impact Scope |
|----|------------|--------------|-----------|--------------|--------------|
| CHG-001 | ADD | [new capability] | N/A | [desired behavior] | [affected components] |
| CHG-002 | MODIFY | [changed behavior] | CB-001 | [new behavior] | [affected components] |
| CHG-003 | REPLACE | [swapped implementation] | CB-002 | [new implementation] | [affected components] |
| CHG-004 | REMOVE | [deprecated feature] | CB-003 | N/A | [affected components] |

### Delta Requirements

<!--
  Map each change request (CHG-xxx) to functional requirements (FR-xxx).
  This creates traceability: CL → CHG → FR → Tasks
-->

| CHG ID | Addresses Limitation | Functional Requirements | Priority |
|--------|---------------------|------------------------|----------|
| CHG-001 | CL-001 | FR-001, FR-002 | P1a |
| CHG-002 | CL-002 | FR-003 | P1b |
| CHG-003 | CL-001, CL-002 | FR-004, FR-005 | P2a |

### Preserved Behaviors

<!--
  CRITICAL: Document behaviors that MUST NOT change.
  These become regression test requirements.
  Each PB-xxx links to current behavior and gets explicit test coverage.
-->

| ID | Behavior | Current Implementation (CB) | Reason for Preservation | Regression Test Required |
|----|----------|----------------------------|------------------------|--------------------------|
| PB-001 | [behavior that must remain] | CB-001 | [why it cannot change] | Yes |
| PB-002 | [behavior that must remain] | CB-002 | [backward compatibility] | Yes |

### Migration Plan *(for Migration change type)*

<!--
  Include this subsection ONLY for Migration change type.
  Defines the transition strategy from current to desired state.
-->

**Migration Strategy**: [ Big Bang | Parallel Run | Strangler Fig | Feature Flag ]

| ID | Migration Phase | Description | Duration | Rollback Plan |
|----|-----------------|-------------|----------|---------------|
| MIG-001 | [phase name] | [what happens] | [estimated time] | [how to rollback] |
| MIG-002 | [phase name] | [what happens] | [estimated time] | [how to rollback] |

**Dual-Mode Period**: [duration where old and new systems coexist]

**Deprecation Timeline**:

| Deprecated Component | Deprecation Date | Removal Date | Migration Path |
|---------------------|------------------|--------------|----------------|
| [component] | [date] | [date] | [how users migrate] |

### Rollback Criteria

<!--
  Define conditions that trigger rollback to current state.
-->

| Metric | Threshold | Action |
|--------|-----------|--------|
| Error rate | > X% | Rollback CHG-001 |
| Response time | > Xms p99 | Rollback CHG-002 |
| [custom metric] | [threshold] | [action] |

---

## Change Traceability Summary *(brownfield only)*

<!--
  Auto-generated by /speckit.analyze for brownfield specs.
  Shows the complete traceability chain:
  Current Behavior (CB) → Limitation (CL) → Change (CHG) → Requirement (FR) → Task → Test
-->

### Change Chain

| Limitation | Change | Requirements | Tasks | Tests | Status |
|------------|--------|--------------|-------|-------|--------|
| CL-001 | CHG-001 | FR-001, FR-002 | T012, T014 | T020 | Defined |
| CL-002 | CHG-002, CHG-003 | FR-003, FR-004 | T015, T016 | T021 | Defined |

### Preserved Behavior Coverage

| PB ID | Behavior | Regression Test | Status |
|-------|----------|-----------------|--------|
| PB-001 | [description] | T030 | ❌ Not covered |
| PB-002 | [description] | T031 | ✅ Covered |

### Migration Task Coverage *(if applicable)*

| MIG ID | Phase | Implementation Tasks | Rollback Tasks | Status |
|--------|-------|---------------------|----------------|--------|
| MIG-001 | [phase] | T040, T041 | T045 | ❌ Not started |
| MIG-002 | [phase] | T042 | T046 | ❌ Not started |

---

## Quality Checklist (SQS Self-Assessment) *(optional)*

<!--
  Optional self-assessment section to verify specification quality before implementation.
  Complete this checklist to estimate your SQS (Specification Quality Score).

  Target: SQS ≥ 80 (Ready for Implementation)

  Full rubric: templates/shared/quality/sqs-rubric.md
  Run `/speckit.analyze --profile sqs` for automated assessment.
-->

### Clarity (25 points)

| ID | Checkpoint | Score | Notes |
|----|------------|-------|-------|
| CL-01 | RFC 2119 Keywords (SHALL/SHOULD/MAY) used consistently | __/5 | |
| CL-02 | No vague terms ("fast", "easy", "user-friendly", "robust") | __/5 | |
| CL-03 | Specific numbers for all quantities, limits, thresholds | __/5 | |
| CL-04 | Measurable success criteria with specific targets | __/5 | |
| CL-05 | Failure scenarios explicitly defined with expected behavior | __/5 | |
| **Subtotal** | | **__/25** | |

### Completeness (25 points)

| ID | Checkpoint | Score | Notes |
|----|------------|-------|-------|
| CM-01 | All functional requirements documented (FR-XXX) | __/5 | |
| CM-02 | Non-functional requirements specified (performance, security) | __/5 | |
| CM-03 | Edge cases listed (boundaries, empty states, limits) | __/5 | |
| CM-04 | Dependencies mapped (external services, libraries, APIs) | __/5 | |
| CM-05 | Security requirements covered (auth, data protection) | __/5 | |
| **Subtotal** | | **__/25** | |

### Testability (25 points)

| ID | Checkpoint | Score | Notes |
|----|------------|-------|-------|
| TS-01 | Each FR has acceptance criteria (AS-XXX) | __/5 | |
| TS-02 | Scenarios are concrete (Given/When/Then with specific values) | __/5 | |
| TS-03 | Performance metrics defined (response times, throughput) | __/5 | |
| TS-04 | Error conditions covered with expected behavior | __/5 | |
| TS-05 | Integration points specified (API contracts, data formats) | __/5 | |
| **Subtotal** | | **__/25** | |

### Traceability (15 points)

| ID | Checkpoint | Score | Notes |
|----|------------|-------|-------|
| TR-01 | Unique IDs assigned to all requirements (FR, NFR, AS) | __/3 | |
| TR-02 | Concept cross-references (links to personas, goals, metrics) | __/3 | |
| TR-03 | Feature dependencies documented | __/3 | |
| TR-04 | FR → AC → Test chain established | __/3 | |
| TR-05 | No orphan requirements (all FRs have tasks, all ACs have tests) | __/3 | |
| **Subtotal** | | **__/15** | |

### No Ambiguity (10 points)

| ID | Checkpoint | Score | Notes |
|----|------------|-------|-------|
| AM-01 | No hedge words ("might", "could", "possibly", "maybe") | __/2 | |
| AM-02 | Domain terms defined in glossary | __/2 | |
| AM-03 | All [NEEDS CLARIFICATION] markers resolved | __/2 | |
| AM-04 | Scope explicit (in-scope and out-of-scope listed) | __/2 | |
| AM-05 | Assumptions documented | __/2 | |
| **Subtotal** | | **__/10** | |

### SQS Summary

```
Clarity:      __/25
Completeness: __/25
Testability:  __/25
Traceability: __/15
No Ambiguity: __/10
─────────────────
TOTAL SQS:    __/100
```

**Status**: [ ] Ready (≥80) | [ ] Needs Work (60-79) | [ ] Block (<60)

**Next Steps**:
- If SQS < 80: Run `/speckit.clarify` to address gaps
- If SQS ≥ 80: Proceed to `/speckit.plan`

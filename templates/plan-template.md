# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

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
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

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

**Alternatives Considered**:
- **Option A**: [Brief description] — Rejected because [reason]
- **Option B**: [Chosen] — Selected because [reason]

**Trade-offs**:
- ✅ **Pros**: [Key benefits]
- ❌ **Cons**: [Key drawbacks/compromises]
- ⚠️ **Risks**: [What could go wrong?]

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

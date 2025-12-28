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

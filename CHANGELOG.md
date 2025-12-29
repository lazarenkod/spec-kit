# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to the Specify CLI and templates are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.46] - 2025-12-29

### Added

- **Radical Ship Optimization — 50-70% Faster Deployments** — Transform `/speckit.ship` with intelligent caching, parallelization, and incremental execution
  - **New Shared Modules** (`templates/shared/ship/`):
    - `terraform-turbo.md`: Provider caching, parallelism tuning (10-30 workers), fingerprint-based skip, targeted plan
    - `deploy-optimizer.md`: Docker layer intelligence, Helm template caching, adaptive timeouts, version-based skip
    - `test-parallel.md`: Parallel test execution with worker pools, test grouping by type (smoke/acceptance/security/performance)
    - `browser-pool.md`: Browser pre-warming at 80% deploy, context reuse, idle management, pool lifecycle
    - `dependency-dag.md`: DAG-based dependency resolution, lazy loading, node/edge types (HARD/SOFT/OPTIONAL/LAZY)
    - `contract-testing.md`: Contract vs E2E strategy, Pact/OpenAPI support, E2E trigger conditions
    - `incremental-tests.md`: Code-to-test mapping, affected-only execution, coverage-based/static analysis strategies
    - `smart-rollback.md`: Snapshot management, partial/instant rollback, failure severity classification
  - **Wave Overlap Execution** — Speculative phase execution at 80% completion threshold:
    - At 80% provision → start deploy preparation (pull images, warm cache)
    - At 80% deploy → start verify preparation (warm browser pool)
    - Expected 25-30% time savings from overlap alone
  - **New CLI Flags** (14 optimization controls):
    - `--turbo`: Maximum parallelism, skip optional checks
    - `--skip-provision`: Skip if fingerprint unchanged
    - `--force-deploy` / `--force-provision`: Override skip logic
    - `--full-e2e` / `--full-tests`: Force complete test suites
    - `--auto-rollback` / `--no-rollback`: Rollback behavior control
    - `--sequential-phases`: Disable wave overlap
    - `--no-browser-pool` / `--no-fingerprint` / `--no-test-cache`: Disable specific optimizations
  - **Phase 5: ROLLBACK** — New recovery phase with intelligent rollback strategies:
    - Rollback type detection: app_only, full, partial
    - Snapshot-based restoration with verification
    - Severity-based decision engine (CRITICAL/HIGH/MEDIUM/LOW)
  - **Enhanced Output Summary** with optimization metrics:
    - Stage-by-stage optimization impact (e.g., "Saved ~5 min")
    - Optimization breakdown table
    - Snapshot status and rollback availability
  - **Expected Performance Impact**:
    - Clean deploy: 12 min → 5 min (58% faster)
    - Small code change: 8 min → 45s (91% faster)
    - Infra-only change: 10 min → 3 min (70% faster)
    - Test re-run: 90s → 20s (78% faster)
    - Rollback: 5 min → 90s (70% faster)

---

## [0.0.45] - 2025-12-29

### Added

- **DRY Architecture with Shared Modules** — Eliminate ~480 lines of duplication across command templates
  - **Core Modules** (`templates/shared/core/`):
    - `language-loading.md`: Unified language detection from constitution.md
    - `manifest-update.md`: Centralized manifest status transitions with validation
    - `brownfield-detection.md`: Confidence-weighted project type detection (6 signals, thresholds at 60%/30%)
    - `workspace-detection.md`: Multi-repo workspace detection for monorepos
  - **Adaptive Intelligence** (`templates/shared/`):
    - `complexity-scoring.md`: 4-tier system (TRIVIAL/SIMPLE/MODERATE/COMPLEX) with 5 scoring categories
    - `semantic-detection.md`: Intent classification (ADD/MODIFY/REMOVE) with confidence thresholds
  - **Quality & Speed** (`templates/shared/`):
    - `self-review/framework.md`: Unified self-review with severity levels (CRITICAL/HIGH/MEDIUM/LOW), verdict logic, 3-iteration loop
    - `validation/checkpoints.md`: Streaming validation during generation with early-fail on CRITICAL issues
  - **Bi-directional Traceability** (`templates/shared/traceability/`):
    - `artifact-registry.md`: YAML-based version tracking (`.artifact-registry.yaml`) with checksums and parent versions
    - `cascade-detection.md`: Change impact analysis with BREAKING/SIGNIFICANT/MINOR/METADATA classification
  - **Progressive Output** (`templates/shared/output/`):
    - `progressive-modes.md`: COMPACT/STANDARD/DETAILED output modes based on complexity tier

- **Performance Optimizations for `/speckit.implement`** — 50-65% faster execution through parallelization, caching, and adaptive behavior
  - **New Shared Modules** (`templates/shared/implement/`):
    - `vision-turbo.md`: Parallel browser contexts for simultaneous viewport capture (75-80% savings)
    - `api-batch.md`: Batched Context7/WebFetch calls with session caching (70% savings)
    - `wave-overlap.md`: Speculative wave execution at 80% completion threshold (25-30% savings)
    - `build-optimizer.md`: Pre-compiled regex patterns for 8 languages (50% savings)
    - `model-selection.md`: Complexity-based haiku/sonnet/opus selection (60-90% cost savings)
  - **Integrated Optimizations in implement.md**:
    - `turbo_mode` config for parallel vision validation (3 browser contexts)
    - `wave_overlap` config for speculative wave start
    - `model_selection` config for complexity-adaptive model routing
    - `precompile_patterns` and `smart_retry` for build error handling
    - File read caching strategy with mtime invalidation (85% savings)
  - **Expected Impact** (MODERATE complexity feature):
    - Sequential time: 400s → Optimized: ~180s (55% faster)
    - Cost: $18.50 → ~$6.20 (66% savings with adaptive models)
  - **Backward Compatibility** via skip flags:
    - `--no-turbo`: Disable parallel vision
    - `--sequential-waves`: Classic wave execution
    - `--no-adaptive-model`: Force opus for all agents
    - `--no-batch-verify`: Sequential API verification
    - `--no-build-fix`: Disable build error auto-fixing

- **Summary-First Pattern** — All commands now output Quick Summary before detailed content
  - Feature name, complexity tier, key metrics at a glance
  - Status badges (✅ Ready, ⚠️ Warnings, ❌ Blocked, 🔄 Stale)
  - Clear next step recommendation
  - Collapsible details for verbose content in COMPACT mode

- **Artifact Version Registry** — Automatic version and lineage tracking
  - Parent version tracking (spec → plan → tasks chain)
  - SHA-256 checksum calculation for change detection
  - Staleness detection when upstream artifacts change
  - Cascade update recommendations

### Changed

- **`/speckit.specify`** updated with shared modules:
  - Uses `complexity-scoring.md` for adaptive workflow
  - Uses `semantic-detection.md` for intent classification
  - Uses `self-review/framework.md` for quality gates
  - Added Output Phase with progressive modes and registry update

- **`/speckit.plan`** updated with shared modules:
  - Uses `language-loading.md`, `complexity-scoring.md`, `brownfield-detection.md`
  - Uses `manifest-update.md` for status transitions
  - Uses `self-review/framework.md` with tier-adaptive criteria
  - Added Output Phase with Quick Summary template

- **`/speckit.tasks`** updated with shared modules:
  - Uses shared core modules for initialization
  - Uses `validation/checkpoints.md` for streaming validation
  - Uses `self-review/framework.md` with complexity-adaptive criteria
  - Added Output Phase with traceability chain visualization

### Technical Details

- **Complexity Tiers** adapt workflow depth:
  - TRIVIAL (0-25): Minimal workflow, 3 self-review criteria
  - SIMPLE (26-50): Standard workflow, 6 criteria
  - MODERATE (51-75): Full workflow, all 10 criteria, CQS ≥ 60
  - COMPLEX (76-100): Full + concept validation, CQS ≥ 80

- **Streaming Validation** catches issues early:
  - Checkpoints after each major section
  - Early-fail on CRITICAL issues (don't wait until end)
  - Parallel validation groups for performance (~33% faster)

- **Backward Compatibility** preserved:
  - Existing artifacts work unchanged
  - Registry auto-initializes on first command run
  - `--legacy` flag for raw output
  - Graceful degradation if modules not found

---

## [0.0.44] - 2025-12-29

### Added

- **Enhanced Concept Phase — Strategic Product Discovery** — Transform `/speckit.concept` from feature capture into market validation
  - **Philosophy**: "Validate before you build, quantify before you commit"
  - **New Modular Templates** (`templates/shared/concept-sections/`):
    - `market-framework.md`: TAM/SAM/SOM market sizing + competitive positioning matrix + market validation signals
    - `persona-jtbd.md`: Deep persona framework with Jobs-to-be-Done (functional, emotional, social jobs) + willingness-to-pay assessment
    - `metrics-smart.md`: SMART validation (Specific, Measurable, Achievable, Relevant, Time-bound) + OKR structure + metrics by wave
    - `risk-matrix.md`: Execution risks with L×I scoring + dependency failure scenarios + pivot criteria + kill criteria
    - `technical-hints.md`: Domain entities sketch + API surface estimation + integration complexity + constitution conflicts
    - `cqs-score.md`: Concept Quality Score calculation with weighted components and quality gate thresholds
  - **Concept Quality Score (CQS)** — New quality gate analogous to SQS for specifications:
    - Formula: `CQS = (Market × 0.25 + Persona × 0.20 + Metrics × 0.15 + Features × 0.20 + Risk × 0.10 + Technical × 0.10) × 100`
    - Quality Gate: CQS ≥ 80 (ready), 60-79 (caution), < 60 (not ready)
    - Component scoring criteria for each dimension with detailed checklists
  - **Validation Mode** — Third mode for existing concepts needing market/risk validation:
    - Triggered when `specs/concept.md` exists but CQS components incomplete
    - Gap-focused workflow: "Your concept has features but lacks market validation. Let's add that."
  - **6 Enhancement Layers** in `/speckit.concept`:
    - Layer 1: Market Opportunity Framework (TAM/SAM/SOM, competitive matrix)
    - Layer 2: Deep Persona Framework (JTBD-enhanced personas)
    - Layer 3: Success Metrics Framework (SMART validation + OKRs)
    - Layer 4: Risk & Contingency Planning (risk matrix, pivot/kill criteria)
    - Layer 5: Technical Discovery Hints (domain entities, API surface)
    - Layer 6: CQS calculation in self-review
  - **New Self-Review Criteria** (SR-CONCEPT-16 through SR-CONCEPT-22):
    - SR-CONCEPT-16: TAM/SAM/SOM calculated with sources (HIGH)
    - SR-CONCEPT-17: ≥2 personas with JTBD defined (HIGH)
    - SR-CONCEPT-18: North Star metric identified (HIGH)
    - SR-CONCEPT-19: All metrics pass SMART validation (MEDIUM)
    - SR-CONCEPT-20: ≥3 risks with mitigations documented (MEDIUM)
    - SR-CONCEPT-21: Pivot criteria defined (MEDIUM)
    - SR-CONCEPT-22: Domain entities sketched (LOW)

### Changed

- **`/speckit.specify` enhanced with CQS Quality Gate**:
  - Validates CQS before specification if `specs/concept.md` exists
  - CQS ≥ 80: INFO and proceed with high confidence
  - CQS 60-79: WARN and ask confirmation to proceed
  - CQS < 60: ERROR and recommend running `/speckit.concept` first
  - Allows override with explicit user confirmation

- **Updated CLAUDE.md workflow documentation**:
  - `/speckit.concept` now documented as Step 2 in SDD workflow
  - Added explanation of Concept Phase features and CQS quality gate
  - Philosophy: "Capture complete product vision before detailed specifications"

---

## [0.0.43] - 2025-12-28

### Added

- **Metrics & Success Criteria (7)** — Comprehensive metrics framework for Spec-Driven Development
  - **Spec Quality Score (SQS)** (`templates/shared/metrics-framework.md`):
    - Aggregate 0-100 quality score from weighted components
    - Formula: `SQS = (FR_Coverage × 0.3 + AS_Coverage × 0.3 + Traceability × 0.2 + Constitution_Compliance × 0.2) × 100`
    - Quality levels: Below MVP (<80), MVP Ready (80-89), Full Feature (90-99), Production Ready (100)
    - Quality gate: SQS >= 80 required before `/speckit.implement`
  - **Velocity Metrics** (VEL-001 to VEL-004):
    - Time to First Working Code: < 10 min target (~5 min lovable)
    - Time to MVP: < 30 min target (~15 min lovable)
    - Human Intervention Rate: < 30% target (~15% lovable)
    - Auto-Fix Success Rate: > 70% target (~80% lovable)
  - **Cost Metrics**:
    - Per-phase token and cost tracking
    - Model pricing: Opus ($0.015/$0.075/1K), Sonnet ($0.003/$0.015/1K), Haiku ($0.00025/$0.00125/1K)
    - Target: $37 current → $20-25 optimized
    - Cache efficiency tracking (write/read rates)
  - **Integration Points**:
    - `/speckit.analyze`: SQS calculation after Pass Z with component breakdown
    - `/speckit.implement`: Velocity and Cost metrics in Self-Review Report
    - Quality gates: Pre-implement (SQS >= 80), Post-implement (intervention < 50%), Cost alert (< 150%)
  - **Metrics Report Template** (`templates/metrics-report-template.md`):
    - Executive summary with all metric categories
    - Detailed component analysis for each SQS factor
    - Timeline breakdown and intervention analysis
    - Cost by phase with model efficiency tracking
    - Trend data support for cross-session comparison
    - Recommendations engine based on metric gaps

- **Mobile Applications Domain** (`memory/domains/mobile.md`) — Constitution extension for mobile app development
  - Platform context: App Store Guidelines (Apple), Play Store Policies (Google), GDPR, COPPA
  - Strengthened base principles: PERF-001, SEC-002, ERR-001, API-003 elevated to MUST
  - New principles (MOB-001 to MOB-008):
    - MOB-001: Offline Capability (MUST) — core features work without network
    - MOB-002: Platform Compliance (MUST) — Apple HIG / Material Design adherence
    - MOB-003: Battery Efficiency (MUST) — minimize background processing
    - MOB-004: Responsive Touch (MUST) — < 100ms touch feedback
    - MOB-005: Secure Storage (MUST) — Keychain/Keystore for credentials
    - MOB-006: Deep Linking (SHOULD) — Universal Links / App Links support
    - MOB-007: Accessibility (MUST) — VoiceOver/TalkBack support
    - MOB-008: Graceful Updates (SHOULD) — forced update mechanism
  - Platform-specific tables for iOS and Android requirements
  - Performance thresholds: cold start < 2s, touch response < 100ms, 60fps target

- **Gaming Domain** (`memory/domains/gaming.md`) — Constitution extension for game development
  - Platform context: PEGI/ESRB ratings, COPPA, loot box regulations, platform TOS (Sony TRC, Microsoft TCR)
  - Strengthened base principles: PERF-001, PERF-002, LOG-001, SEC-003 elevated to MUST
  - New principles (GAM-001 to GAM-009):
    - GAM-001: Frame Rate Stability (MUST) — maintain 30/60/120 FPS target
    - GAM-002: Input Latency (MUST) — < 50ms input-to-response
    - GAM-003: State Persistence (MUST) — reliable progress saving
    - GAM-004: Fair Monetization (MUST) — clear pricing, no deceptive patterns
    - GAM-005: Age-Appropriate Content (MUST) — accurate age ratings
    - GAM-006: Multiplayer Integrity (MUST) — anti-cheat, server-authoritative state
    - GAM-007: Network Resilience (MUST) — graceful disconnect handling
    - GAM-008: Asset Loading (SHOULD) — async loading with progress
    - GAM-009: Platform Certification (MUST) — TRC/TCR/Lotcheck compliance
  - Game type considerations: real-time multiplayer, turn-based, live service
  - Performance thresholds by platform: mobile, PC, console

- **Production-First Templates (5.2)** — Constitution domain and self-hosted observability stack
  - **Production Domain** (`memory/domains/production.md`):
    - Philosophy: "If it's not observable, it's not production-ready"
    - Strengthened base principles: OBS-003, OBS-004 elevated to MUST; OBS-001/002 enhanced with trace context
    - New principles (PRD-001 to PRD-010):
      - PRD-001: OpenTelemetry-First Architecture (MUST) — vendor-neutral instrumentation
      - PRD-002: Structured Logging with Correlation (MUST) — JSON logs with traceId/spanId
      - PRD-003: Health Endpoints (MUST) — `/health` and `/ready` endpoints
      - PRD-004: Prometheus Metrics Export (MUST) — `/metrics` endpoint
      - PRD-005: Graceful Shutdown (MUST) — SIGTERM handling with connection draining
      - PRD-006: Error Tracking with Context (MUST) — exceptions to span and GlitchTip
      - PRD-007: Distributed Tracing (MUST) — W3C Trace Context propagation
      - PRD-008: Configuration Validation (MUST) — fail fast on startup
      - PRD-009: Self-Hosted Observability (SHOULD) — data sovereignty
      - PRD-010: Dashboard as Code (SHOULD) — Grafana provisioning
  - **Open Source Stack** (no paid SaaS dependencies):
    - GlitchTip (replaces Sentry) — Sentry-compatible error tracking
    - VictoriaMetrics (replaces Datadog/Prometheus) — 10x more efficient storage
    - Jaeger v2 — OpenTelemetry-native distributed tracing
    - Loki + Grafana — log aggregation and unified dashboards
    - Umami (replaces PostHog) — privacy-first analytics
    - Pino/structlog — high-performance structured logging
  - **Observability Stack Template** (`templates/shared/observability-stack.md`):
    - Complete Docker Compose for full stack
    - OpenTelemetry Collector configuration
    - VictoriaMetrics with 90-day retention
    - Grafana datasource provisioning
    - Resource requirements: ~2.5 vCPU, ~5.5GB RAM
    - Cost savings: $0/mo vs $200-600/mo for SaaS equivalents
  - **OpenTelemetry Integration Guide** (`templates/shared/otel-integration.md`):
    - Node.js/TypeScript setup with Pino
    - Python setup with structlog
    - Go setup with zerolog
    - Health endpoint patterns
    - Graceful shutdown implementations
    - Configuration validation with Zod/Pydantic
  - **Template-Based Initialization** (`specify init --template`):
    - CLI `--template` / `-t` flag for production-ready project scaffolding
    - 8 production templates with pre-configured technology stacks:
      - `production-saas`: Full-stack SaaS with auth, payments, observability
      - `production-api`: REST/GraphQL API backend with observability
      - `mobile-app`: iOS/Android with offline support and analytics
      - `gaming`: Real-time game with multiplayer and anti-cheat
      - `fintech`: Regulated financial services (PCI-DSS, SOC2)
      - `healthcare`: HIPAA/GDPR-compliant health application
      - `e-commerce`: Online store with payments and inventory
      - `minimal`: Empty template for advanced users (default)
    - Interactive template discovery with arrow-key selection and rich descriptions
    - `REQUIREMENTS_CHECKLIST.md` auto-generation with:
      - Stack configuration table with constitution principle mappings
      - Functional requirements checklist (domain-specific)
      - Non-functional requirements checklist (quality attributes)
      - Activated constitution principles summary
      - Next steps workflow guidance
    - Template YAML schema (`templates/stacks/`) with:
      - Domain activation (automatically includes relevant domain files)
      - Category-based stack options with constitution principle mappings
      - Framework alternatives with URLs and descriptions
      - Functional and non-functional requirement checklists
    - Philosophy: "Don't make me think about what I might forget"

- **Quality Gates (5.3)** — Constitution domain extension for quality thresholds at workflow transitions
  - **Quality Gates Domain** (`memory/domains/quality-gates.md`):
    - Philosophy: "Quality is not a phase, it's a gate at every transition"
    - 12 QG-XXX principles across three checkpoint phases
    - Strengthened base principles: QUA-001, QUA-003, QUA-004, TST-001, SEC-001 elevated
  - **Pre-Implement Gates** (QG-001 to QG-003):
    - QG-001: SQS Quality Gate (MUST) — Spec Quality Score >= 80 before implementation
    - QG-002: Security Scan Pass (MUST) — 0 critical/high vulnerabilities
    - QG-003: Dependency Freshness (SHOULD) — no deps > 2 major versions behind
  - **Post-Implement Gates** (QG-004 to QG-009):
    - QG-004: Test Coverage (MUST) — >= 80% line coverage
    - QG-005: Type Coverage (MUST) — >= 95% type annotations
    - QG-006: Lint Cleanliness (MUST) — 0 errors, < 10 warnings
    - QG-007: Performance Baseline (SHOULD) — Lighthouse >= 90
    - QG-008: Accessibility Compliance (SHOULD) — WCAG 2.1 AA
    - QG-009: Documentation Coverage (SHOULD) — 100% public APIs documented
  - **Pre-Deploy Gates** (QG-010 to QG-012):
    - QG-010: All Tests Pass (MUST) — 100% test pass rate
    - QG-011: No Debug Artifacts (MUST) — no console.log/debugger statements
    - QG-012: Environment Documentation (MUST) — all env vars in .env.example
  - **CI/CD Templates** (`templates/shared/ci-templates.md`):
    - GitHub Actions workflow with all 12 quality gates
    - GitLab CI pipeline equivalent
    - Pre-commit hooks for local gate validation
    - Lighthouse CI, axe-core, and type-coverage configurations
    - Environment coverage check script
  - **Command Integration**:
    - `/speckit.analyze --profile sqs` — SQS validation (QG-001)
    - `/speckit.analyze --profile quality_gates` — full quality gate validation
    - `/speckit.analyze --profile pre_deploy` — pre-deployment gates (QG-010 to QG-012)
    - `/speckit.implement` — pre-gates for SQS >= 80, post-gates for coverage/lint

### Changed

- **Auto-Context Profile Detection** — `/speckit.analyze` now auto-detects validation profile from context
  - **Caller-based detection**: Automatically selects profile based on invoking command
    - From `/speckit.specify` or `/speckit.clarify` → `spec_validate`
    - From `/speckit.plan` → `plan_validate`
    - From `/speckit.tasks` → `tasks_validate`
    - From `/speckit.implement` → `sqs` (pre) or `quality_gates` (post)
  - **Artifact-based fallback**: If no caller context, detects from project artifacts
    - `*.impl.md` or `src/` changes → `quality_gates`
    - `*.tasks.md` exists → `tasks_validate`
    - `*.plan.md` exists → `plan_validate`
    - `*.spec.md` exists → `spec_validate`
  - **Simplified command invocations** (no explicit `--profile` needed):
    - Before: `/speckit.analyze --profile spec_validate --quiet`
    - After: `/speckit.analyze --quiet`
  - **Backward compatible**: `--profile <name>` override still works for power users
  - Philosophy: "Convention over Configuration" — tool understands context automatically

---

## [0.0.42] - 2025-12-28

### Added

- **Component Library Recommendations (6.3)** — Auto-recommend UI component libraries based on detected framework
  - **Framework Detection** in `/speckit.design` Step 0.75:
    - Parses spec.md Framework Requirements table for React, Vue, Angular, Svelte
    - Reads constitution.md Technology Constraints for UI Framework field
    - Detects TypeScript usage for refined recommendations
  - **Library Mapping** (`templates/shared/library-recommendations.md`):
    - React + TypeScript → shadcn/ui (primary), MUI, Radix UI (alternatives)
    - React (JS) → MUI (primary), shadcn/ui, Chakra UI (alternatives)
    - Vue.js → Vuetify (primary), PrimeVue, Quasar (alternatives)
    - Angular → Angular Material (primary), PrimeNG, ng-bootstrap (alternatives)
    - Svelte → Skeleton UI (primary), Svelte Material UI (alternatives)
  - **Domain Modifiers**:
    - UXQ domain → prefer rich UX libraries (shadcn/ui, MUI)
    - SaaS domain → prefer data-dense libraries (MUI, Angular Material)
    - Fintech domain → prefer mature, audited libraries (MUI, Angular Material)
    - Healthcare domain → prefer accessible-first libraries (Angular Material, MUI)
  - **WCAG Level Modifiers**:
    - AAA compliance → filter to tier-1 accessible libraries (Angular Material, shadcn/ui, MUI)
  - **Preset Application**:
    - Auto-applies matching preset from design-system-presets.md on user confirmation
    - Shows preset preview (framework, primary color, font family, component URL)
    - User can choose alternatives or skip
  - **Configuration Updates**:
    - New UI Framework field in constitution.md Technology Constraints table
    - New `library_recommendation:` frontmatter in design.md with `--no-recommendation` skip flag
  - **Template Updates**:
    - spec-template.md Framework Requirements section with library recommendation note
    - design.md Step 0.75 with complete auto-discovery algorithm

---

## [0.0.41] - 2025-12-28

### Added

- **Design System Enforcement (6.2)** — Validate UI code against design tokens and component libraries
  - **New DSS Principles** in `constitution.base.md`:
    - DSS-001: Use Library Components First (SHOULD) — prefer configured library components over custom
    - DSS-002: Color Token Compliance (MUST) — all colors must reference design tokens
    - DSS-003: Typography Consistency (SHOULD) — use typography tokens for text styling
  - **Design System Configuration** in `constitution.md`:
    - `design_system:` YAML block for framework, theme tokens, and enforcement level
    - Supported frameworks: shadcn/ui, MUI, Vuetify, Angular Material, Tailwind, Bootstrap
    - Enforcement levels: `strict` (blocks deployment), `warn` (reports violations), `off` (disabled)
    - Theme tokens: colors, typography scale, spacing units, border radii
  - **Framework Presets** (`templates/shared/design-system-presets.md`):
    - Pre-configured tokens for shadcn/ui, MUI, Tailwind CSS
    - Includes color palettes, typography scales, and component library URLs
    - Easily extendable preset system
  - **Code Analysis** via Pass Z in `/speckit.analyze`:
    - DSS-002: Scan for hardcoded hex/RGB/HSL colors (excludes *.config.*, tokens.*)
    - DSS-001: Detect custom components when library equivalent exists
    - DSS-003: Find hardcoded font-family/font-size values
    - Token coverage analysis with utilization metrics
    - Severity mapping based on enforcement level
  - **Vision Validation Integration** (`templates/shared/vision-validation.md`):
    - Design System Vision Prompt for visual token compliance
    - Color comparison with 5% RGB Euclidean distance tolerance
    - Typography and component consistency checks
    - Integrated into UX Audit Report output
  - **Implementation Enforcement** (`templates/commands/implement.md`):
    - Step 3.6: Design System Context Loading (parse config, load presets)
    - New self-review criteria: SR-IMPL-18 (colors), SR-IMPL-19 (components), SR-IMPL-20 (typography)
    - Auto-fix rules: AF-006 (hex→CSS variable), AF-007 (custom→library), AF-008 (font-size→token)
  - **Report Enhancements**:
    - Design System Status section in analysis report
    - Token utilization metrics (colors, typography, spacing, radii)
    - DSS principle compliance table with issue counts
  - **New Severity Entries**:
    - CRITICAL: Hardcoded color in strict mode (DSS-002)
    - HIGH: Hardcoded color in warn mode, unknown preset, custom component (strict)
    - MEDIUM: Custom component (warn), hardcoded typography (warn)
    - LOW: Low token utilization, invalid color format in config

---

## [0.0.40] - 2025-12-28

### Added

- **Vision-Powered UX Validation (6.1)** — Automated visual UX auditing in `/speckit.implement`
  - **Screenshot Capture** via Playwright MCP:
    - Multi-viewport capture: mobile (375px), tablet (768px), desktop (1440px)
    - Multi-state coverage: default, loading, error, empty, success
    - Triggered for tasks with `[VR:VR-xxx]` markers or `role_group = FRONTEND`
  - **Vision Analysis** via Claude Opus:
    - Validates against UXQ principles (UXQ-001, 003, 005, 006, 010)
    - Validates against Nielsen Heuristics (H1, H2, H4, H6, H8)
    - Detects UX anti-patterns (modal overload, cognitive overload, mobile neglect)
    - Outputs structured JSON with severity-classified violations
  - **UX Audit Report** generation (`specs/{feature}/ux-audit.md`):
    - Executive summary with overall UX score (0-100)
    - Critical/High/Medium/Low issue breakdown
    - Per-screen analysis with suggestions
    - Screenshot gallery with coverage matrix
  - **Deployment Gate**:
    - CRITICAL violations block deployment (`SR-IMPL-15`)
    - Skip with `--no-vision` flag
  - **New YAML Configuration** (`vision_validation:` section):
    - `enabled: true` for feature toggle
    - `skip_flag: "--no-vision"` for opt-out
    - Configurable viewports, states, severity threshold
  - **New Quality Criteria** (SR-IMPL-14 through SR-IMPL-17):
    - SR-IMPL-14: UI renders across viewports (HIGH)
    - SR-IMPL-15: No CRITICAL UX violations (CRITICAL)
    - SR-IMPL-16: Loading/error/empty states implemented (HIGH)
    - SR-IMPL-17: Visual accessibility checks pass (HIGH)
  - **New Templates**:
    - `templates/shared/vision-validation.md`: Screenshot strategy, vision prompts, severity classification
    - `templates/ux-audit-template.md`: UX Audit Report template with scoring rubric
  - **Integration Points**:
    - Step 1.7 in Self-Review Phase (after Self-Healing, before Re-read Files)
    - References existing `memory/domains/uxq.md`, `memory/knowledge/frameworks/nielsen-heuristics.md`, `memory/knowledge/anti-patterns/ux.md`

---

## [0.0.39] - 2025-12-28

### Added

- **Design Tool Integration (5.4)** — Figma import and OpenAPI generation
  - **Figma Import** in `/speckit.design`:
    - New `figma_import:` YAML configuration section
    - Step 0.5: Auto-extract design tokens (colors, typography, shadows, spacing)
    - Auto-extract component specifications with variant mapping
    - Non-destructive merge into design.md (preserves manual entries)
    - `<!-- figma-sync -->` markers for re-import updates
    - Skip with `--no-figma` flag
    - Environment: `FIGMA_ACCESS_TOKEN` for API authentication
  - **OpenAPI Generation** in `/speckit.plan`:
    - New `openapi_generation:` YAML configuration section
    - Step 4.5: Parse FR-xxx for API-related requirements
    - Generate `contracts/api.yaml` in OpenAPI 3.0.3 format
    - FR-to-endpoint mapping rules (create→POST, get→GET, etc.)
    - Schema inference from FR descriptions
    - Validate endpoint coverage against spec requirements
    - Skip with `--no-contracts` flag
  - **Template Updates**:
    - `spec-template.md`: Enhanced Design System field with Figma/Storybook/Tokens URL comments
    - `plan-template.md`: Added API Contracts section with Generated Endpoints table
    - `design-template.md`: Added Import Metadata section for tracking Figma sync status
  - **New Shared Context Files**:
    - `templates/shared/figma-import.md`: Figma API mapping, token extraction rules, conflict resolution
    - `templates/shared/openapi-generation.md`: FR-to-endpoint mapping, schema inference, validation rules

---

## [0.0.38] - 2025-12-28

### Added

- **Proactive Validation Pipeline** — Auto-validation gates before phase transitions
  - `pre_handoff_action` in `/speckit.specify` and `/speckit.plan` command templates
  - Constitution Alignment Gate (Pass D): blocks on any constitution violations
  - Ambiguity Gate (Pass B): warns if >5 ambiguous findings
  - Tech Consistency Gate (Pass F): blocks on terminology inconsistencies
  - Auto-invokes `/speckit.clarify` with extracted questions on gate failures
  - Compact validation output format for quick scanning

- **Self-Healing Implementation Loop** — Auto-fix common issues during self-review
  - `auto_fix_rules` section in `/speckit.implement` template
  - 5 auto-fix rules:
    - AF-001: Missing @speckit annotations → insert from task markers
    - AF-002: TODO/FIXME/HACK comments → convert to `.speckit/issues.md`
    - AF-003: Lint warnings → run project auto-formatter (eslint/prettier/black/gofmt)
    - AF-004: Missing .env.example → generate from code scanning
    - AF-005: Debug statements → remove console.log/print
  - Max 3 auto-fix iterations before human escalation
  - Skip with `--no-auto-fix` flag

- **Post-Implementation Workflow Rule** — Added to CLAUDE.md
  - Automatic CHANGELOG.md updates after completing features
  - Version bump reminder for CLI changes
  - Ensures traceability across sessions

- **Intelligent Model Routing** — Cost optimization through model selection per command
  - Added `model:` field to `claude_code:` YAML sections across all 11 command templates
  - **Opus** for high-reasoning tasks: `/speckit.constitution`, `/speckit.concept`, `/speckit.specify`, `/speckit.plan`, `/speckit.design`
  - **Sonnet** for balanced tasks: `/speckit.clarify`, `/speckit.tasks`, `/speckit.analyze`, `/speckit.baseline`, `/speckit.merge`
  - **Haiku** for simple/repetitive tasks: setup phase, self-review phase
  - **Phase-aware routing for `/speckit.implement`**:
    - `setup` phase → Haiku (boilerplate, deps, config files)
    - `core` phase → Opus (business logic, services, models)
    - `tests` phase → Sonnet (test generation)
    - `self_review` phase → Haiku (auto-fix, formatting)
  - Expected cost reduction: 40-60%

- **Multi-Agent Orchestration** — Parallel subagent execution with dependency resolution
  - New `orchestration:` YAML section in `claude_code:` config
    - `max_parallel`: Max concurrent agents (default: 1)
    - `role_isolation`: One agent per role_group at a time (default: false)
    - `conflict_resolution`: queue | abort | merge
    - `timeout_per_agent`: Timeout in ms
    - `retry_on_failure`: Retry count
  - Extended subagent attributes:
    - `role_group`: FRONTEND | BACKEND | TESTING | INFRA | REVIEW | DOCS
    - `parallel`: Can run in parallel (default: false)
    - `depends_on`: List of role dependencies
    - `priority`: 1-10, higher runs first
    - `model_override`: Override model for specific agent
  - **Commands updated**:
    - `/speckit.implement`: 10 subagents in 4 waves (scaffolder → builders → testers → reviewers)
    - `/speckit.plan`: 2 parallel research agents
    - `/speckit.analyze`: 4 validation agents with dependency chain
    - `/speckit.tasks`: 3 mapping agents (dependency → FR → AS)
    - `/speckit.merge`: Extended with role_group attributes
  - Wave-based execution prevents file conflicts between FRONTEND/BACKEND/TESTING agents

- **Self-Healing Engine: Build Error Auto-Fixes** — Automatic compilation error recovery
  - New `build_error_patterns:` YAML section with language-specific patterns
  - **11 Build Fix rules** (BF-001 to BF-011):
    - BF-001: Missing import/module → Auto-add import (TS/Py/Go/Rust/Kt/Java)
    - BF-002: Unused variable → Prefix with `_` (TS/ESLint/Go/Rust/Kt/Java)
    - BF-003: Type mismatch → Add annotation or cast (TS/Kt/Java)
    - BF-004: Missing key prop → Add `key={index}` (React)
    - BF-005: Conditional hook call → Move hook to top (React)
    - BF-006: Undefined name/symbol → Add import or define (Python/Java)
    - BF-007: Missing companion object → Add `companion object {}` (Kotlin)
    - BF-008: Suspend outside coroutine → Wrap in coroutine scope (Kotlin)
    - BF-009: Missing @Composable → Add annotation (Compose)
    - BF-010: Modifier wrong position → Reorder to first optional (Compose)
    - BF-011: Static context error → Add instance or make static (Java)
  - **Step 0.5: Build-Until-Works Loop** in self-review phase
    - Iterative build → parse stderr → apply fixes → retry
    - Max 3 attempts before human escalation
    - Skip with `--no-build-fix` flag
  - Languages supported: TypeScript, React, Python, Go, Rust, ESLint, Kotlin, Kotlin Compose, Java
  - Target: 70% build errors auto-fixed (vs ~10% before)

---

## [0.0.37] - 2025-12-27

### Added

- **Wave-Based Ordering for UX Foundations**
  - Execution order system ensuring prerequisites are built before business features
  - **Wave 1 (Core Infrastructure)**: AUTH, ERROR, LAYOUT, CONFIG, HEALTH — blocks all other features
  - **Wave 2 (User Experience)**: NAV, FTUE, FEEDBACK, HELP, ADMIN — enables testable user journeys
  - **Wave 3+ (Business Features)**: All product-specific functionality
  - Auto-detection of required foundations based on project type (Web SPA, Mobile, API, CLI, etc.)
  - Golden Path generation: minimum viable user journey exercising all Wave 1-2 foundations

- **ADMIN Foundation (Wave 2)**
  - Administrative interface for all projects with AUTH
  - 6 scenarios: Admin dashboard, user list, user edit, role management, audit log, access denial
  - Pattern detection: `admin*`, `dashboard*`, `backoffice*`, `management*`, `panel*`, `console*`
  - Default Epic mapping: Dashboard → User Management → Role Management → Audit Log

- **Auto-Changelog in `/speckit.implement`**
  - Changelog automatically updated after each user story passes DoD validation
  - Entry format includes story ID, acceptance scenarios, and FR traceability
  - Skip conditions for infrastructure/internal stories (`[NO-CHANGELOG]` marker)

### Fixed

- **`/speckit.implement` Task Completion**: Now mandatory marks tasks as completed immediately after finishing each one

---

## [0.0.36] - 2025-12-27

### Added

- **Autonomous Infrastructure & Deployment: `/speckit.ship`** — Full pipeline from spec to running system
  - New slash command with provision → deploy → verify workflow
  - Supports `--env local|staging|production`, `--only infra|deploy|verify`, `--destroy`, `--dry-run`
  - Multi-cloud support: VK Cloud, Yandex Cloud, Google Cloud Platform
  - Idempotent provisioning with Terraform drift detection
  - State management in `.speckit/state/{env}/` prevents infrastructure recreation

- **New Templates**:
  - `templates/infra-template.yaml` — Infrastructure specification (Terraform config)
  - `templates/deploy-template.yaml` — Deployment specification (Helm/docker-compose)
  - `templates/verify-template.yaml` — Verification specification (tests + security scans)
  - `templates/commands/ship.md` — Slash command definition for AI agents

- **New Deployment Scripts** (`scripts/bash/`):
  - `ship.sh` — Main orchestrator (provision → deploy → verify)
  - `provision.sh` — Terraform wrapper with drift detection and S3 backend
  - `deploy.sh` — Helm/docker-compose deployment with namespace management
  - `verify.sh` — Health checks, acceptance tests, and results generation

- **Infrastructure Requirements section in `spec-template.md`**:
  - Required Services table (INFRA-xxx IDs)
  - Environment Configuration (local/staging/production)
  - Connection Requirements (environment variables)
  - Verification Endpoints (health checks)

- **INFRA-xxx dependency type in `plan-template.md`**:
  - Infrastructure Dependencies table in Dependency Registry
  - Provisioning Strategy (Existing/New)
  - Generated Artifacts reference (infra.yaml, deploy.yaml, verify.yaml)

- **Verification Feedback Loop**:
  - `verify-results.md` generated after deployment
  - Automatic update of `spec.md` with verification status
  - Traceability: AS-xxx acceptance scenarios → verify.yaml → results

---

## [0.0.35] - 2025-12-26

### Added

- **Multi-Repository Workspace Support**
  - Cross-repository feature dependencies via `specify workspace` commands
  - Repository aliases for referencing features across repos (e.g., `api:002-payment-api`)
  - Dependency types: REQUIRES, BLOCKS, EXTENDS, IMPLEMENTS, USES
  - Cross-Repository Dependencies section in spec-template.md

- **Agent Skills Enhancement**
  - Improved skill definitions and handoff mechanisms
  - Better context preservation between agent phases

---

## [0.0.34] - 2025-12-25

### Added

- **Language Setting for Generated Artifacts**
  - All generated artifacts (specs, plans, tasks) now support configurable language
  - Consistent language across the entire workflow

- **Inline Agents Support**
  - Agents can be defined inline within commands
  - Reduces need for separate persona files for simple agents

- **User Experience Quality (UXQ) Domain**
  - New domain extension for UX-focused projects
  - 10 UXQ principles (Jobs to Be Done, Friction Justification, Delight Moments, etc.)
  - UXQ section in spec-template.md with:
    - Jobs to Be Done table
    - User Mental Model documentation
    - First-Time User Experience (FTUE) section
    - Friction Points table with justification requirements
    - Delight Opportunities table
    - Emotional Journey mapping
    - Accessibility as Empowerment section

- **Self-Testing Capabilities**
  - Enhanced automated test generation and validation
  - Better integration with test frameworks

---

## [0.0.33] - 2025-12-24

### Added

- **Multi-Agent Orchestration Architecture** (BMAD-Method inspired)
  - Multi-agent orchestrator pattern: specialized agents per workflow phase
  - Phase-specific agent personas for specialized context retention
  - Handoff documents for explicit context transfer between phases
  - Solves "single-agent bottleneck" problem where one agent loses context between phases

- **New Agent Personas** (`templates/personas/`):
  - `product-agent.md`: Requirements engineering, user value focus
  - `architect-agent.md`: Technical design, trade-off analysis
  - `decomposer-agent.md`: Task breakdown, dependency management
  - `developer-agent.md`: Implementation, testing, security
  - `qa-agent.md`: Validation, compliance, quality gates

- **Handoff Template** (`templates/handoff-template.md`):
  - Key Decisions Made table with rationale and alternatives
  - Constraints for Next Phase section
  - Risks Identified table with severity and mitigation
  - Open Questions checklist
  - Context for Next Agent section

- **Orchestration Scripts**:
  - `scripts/bash/orchestrate-handoff.sh`: Generate, load, validate handoffs
  - `scripts/powershell/orchestrate-handoff.ps1`: PowerShell variant

### Changed

- **All main workflow commands enhanced with persona and handoff support**:
  - `specify.md`: Product Agent persona, generates specify-to-plan handoff
  - `plan.md`: Architect Agent persona, loads specify handoff, generates plan-to-tasks handoff
  - `tasks.md`: Decomposer Agent persona, loads plan handoff, generates tasks-to-implement handoff
  - `implement.md`: Developer Agent persona, loads tasks handoff
  - `analyze.md`: QA Agent persona integration

- **New frontmatter fields in command templates**:
  - `persona:` — Links command to agent persona for specialized context
  - `handoff.generates:` — Specifies handoff document this phase creates
  - `handoff.requires:` — Specifies handoff document this phase needs
  - `handoff.template:` — Reference to handoff template

### Fixed

- **Markdown linter compliance**: Fixed 371 linter errors
  - Added language specifiers to all fenced code blocks (MD040)
  - Configured markdownlint rules for template-heavy project
  - Disabled overly strict formatting rules (MD001, MD007, MD026, MD029, MD046, MD053)

---

## [0.0.32] - 2025-12-24

### Added

- **QA Phase in Workflow** (BMAD-Method inspired)
  - Post-implementation QA verification via `/speckit.analyze` QA mode
  - Automatic transition from `/speckit.implement` to QA when P1 tasks complete
  - QA Loop for iterative fixes until all checks pass

- **New QA validation categories in `/speckit.analyze`**:
  - **Category R — Build Validation**: Build system detection, build check, lint check, type check
  - **Category S — Test Execution Validation**: Test discovery, test runner, execution, coverage check
  - **Category T — Performance Baseline Validation**: NFR extraction, performance regression detection
  - **Category U — Security Validation**: Dependency audit, secret detection, OWASP quick checks

- **QA Verification Report format**:
  - Build & test status table with pass/fail indicators
  - Coverage metrics vs. threshold comparison
  - Security audit summary with vulnerability counts
  - QA Verdict: PASS / CONCERNS / FAIL based on issue severity

- **QA handoffs in `/speckit.implement`**:
  - `QA Verification` (auto: true) — Triggers `/speckit.analyze` QA mode after implementation
  - `Fix QA Issues` (auto: false) — Returns to implement to address failures
  - QA Loop visualization in Automation Behavior section

### Changed

- **`/speckit.analyze` now supports two modes**:
  - Pre-Implementation mode (default): Categories A-Q for spec artifact validation
  - QA mode (post-implementation): Categories A-Q + R-U for full verification
  - Mode detection based on tasks.md completion status

- **`/speckit.implement` auto-transitions to QA**:
  - No longer terminal phase — flows to QA verification
  - Implementation Complete Gate validates P1 tasks before QA
  - Build Artifacts Gate ensures implementation exists

- **Updated severity assignments**:
  - CRITICAL: Build failed, Tests failed, Critical vulnerabilities, Secrets in code
  - HIGH: Lint errors, Type errors, Coverage below threshold, High vulnerabilities
  - MEDIUM: No test files, Lint warnings, Performance regression, Resource limits
  - LOW: Build warnings, No baseline measurement

### Documentation

- New "Analysis Modes" section in `/speckit.analyze`
- New "QA Loop" section in `/speckit.implement` with ASCII flow diagram
- QA Handoffs table showing auto vs. manual transitions

---

## [0.0.31] - 2025-12-23

### Added

- **Automation Hooks: Enhanced Handoffs with Quality Gates** (AWS Kiro-inspired)
  - Declarative automation rules via enhanced handoffs in command frontmatter
  - Quality gates that can block phase transitions until conditions are met
  - Pre-execution gates for validating prerequisites before command runs
  - Auto-transitions between phases when conditions pass and gates allow
  - Post-actions for logging and audit trails

- **New frontmatter fields for automation**:
  - `auto: true|false` — Enable automatic transition to next phase
  - `condition:` — List of conditions required for auto-transition
  - `gates:` — Quality gates with `check`, `block_if`, and `message` fields
  - `pre_gates:` — Pre-execution gates validated before command starts
  - `post_actions:` — Actions to execute after successful transition

- **Quality Gates per phase**:
  - `/speckit.specify`: Spec Quality Gate (no unresolved [NEEDS CLARIFICATION])
  - `/speckit.plan`: Plan Completeness Gate (all sections filled, architecture defined)
  - `/speckit.tasks`: Tasks Ready Gate, Dependency Validity Gate (no circular deps)
  - `/speckit.analyze`: No Critical Issues Gate, Dependency Graph Valid Gate
  - `/speckit.implement`: Tasks Exist Gate, Required Artifacts Gate, No Critical Issues Gate
  - `/speckit.baseline`: Feature Directory Gate, Scope Definition Gate, Baseline Completeness Gate

### Changed

- **All main workflow commands enhanced with automation behavior**:
  - `specify.md`: Auto-transition to plan when spec valid, gate blocks if clarifications remain
  - `plan.md`: Auto-transition to tasks when plan complete, gate blocks if empty sections
  - `tasks.md`: Auto-transition to implement when tasks valid, gates block on circular deps
  - `analyze.md`: Auto-transition to implement only if CRITICAL == 0
  - `implement.md`: Pre-gates validate artifacts exist before execution starts
  - `baseline.md`: Pre-gates and transition gates for brownfield workflow

- **New "Automation Behavior" section in each command**:
  - Documents auto-transitions, quality gates, gate behavior, and manual overrides
  - Provides tables showing conditions, gates, and blocking behavior
  - Explains what happens when gates block vs pass

### Documentation

- Each command now includes detailed Automation Behavior section explaining:
  - Auto-Transitions table with conditions and gates
  - Quality Gates table with check/block_if/message
  - Gate Behavior section for pass/block scenarios
  - Manual Overrides section for user control

---

## [0.0.30] - 2025-12-23

### Added

- **Brownfield Support: Change-Based Architecture** (OpenSpec-inspired)
  - Full support for specifying changes to existing codebases
  - Current State → Delta → Desired State pattern for brownfield projects

- **New `/speckit.baseline` command**: Capture current system state for brownfield specs
  - Analyzes code structure, behaviors, and dependencies within defined scope
  - Generates `baseline.md` with CB-xxx (Current Behavior) IDs
  - Documents API contracts, performance baselines, and dependency graphs
  - Identifies potential limitations that may drive changes
  - Produces machine-readable baseline for `/speckit.specify` integration

- **New ID types for brownfield traceability**:
  - `CB-xxx` — Current Behavior (documented in baseline.md)
  - `CL-xxx` — Current Limitation (drives change requests)
  - `CHG-xxx` — Change Request with Delta Types (ADD/MODIFY/REPLACE/REMOVE/DEPRECATE)
  - `PB-xxx` — Preserved Behavior (must remain unchanged, requires regression tests)
  - `MIG-xxx` — Migration Phase (for Migration change type)

- **New task markers for brownfield projects** (in tasks-template.md):
  - `[CHG:CHG-xxx]` — Links task to change request
  - `[MIG:MIG-xxx]` — Migration phase implementation
  - `[REG:PB-xxx]` — Regression test for preserved behavior
  - `[ROLLBACK:MIG-xxx]` — Rollback procedure for migration phase

- **Change Specification section in spec-template.md** (brownfield only):
  - Change Type classification (Enhancement, Refactor, Migration, Bugfix, Performance, Security)
  - Current State Analysis table with CB-xxx references
  - Current Limitations table (CL-xxx)
  - Change Delta table with explicit delta types
  - Delta-to-Requirement mapping (CHG → FR traceability)
  - Preserved Behaviors table with regression test requirements
  - Migration Plan section (for Migration change type)
  - Rollback Criteria with thresholds and actions
  - Change Traceability Summary (CB → CL → CHG → FR → Task → Test)

- **Migration Foundation Phase (Phase 2c)** in tasks-template.md:
  - Regression test tasks for preserved behaviors
  - Migration infrastructure tasks (feature flags, dual-mode operation)
  - Rollback procedure tasks
  - Change baseline documentation tasks
  - Blocks change implementation until regression protection is in place

### Changed

- **`/speckit.specify` enhanced with brownfield detection**:
  - Auto-detects brownfield projects (git history, directory structure, keywords)
  - Prompts for brownfield mode when signals detected
  - Integrates with baseline.md when available
  - Generates Change Specification section for brownfield projects
  - Reports brownfield status in completion summary

- **`/speckit.analyze` enhanced with brownfield validation**:
  - Category P: Brownfield Consistency Validation
    - Current state completeness (CB-xxx validation)
    - Limitation-to-change linkage (CL → CHG)
    - Delta-to-requirement mapping (CHG → FR)
    - Preserved behavior coverage (PB-xxx with [REG:] tasks)
  - Category Q: Migration Validation (for Migration change type)
    - Migration plan presence and completeness
    - Phase coverage with implementation and rollback tasks
    - Dual-mode period and deprecation timeline validation
    - Rollback criteria completeness
  - New severity levels for brownfield issues (CRITICAL, HIGH, MEDIUM, LOW)
  - Brownfield Status section in analysis report
  - Change Traceability Chain visualization
  - Migration Status summary with phase coverage

- **Updated `tasks-template.md`**:
  - Phase Dependencies include Migration Foundation (Phase 2c)
  - Change Traceability Matrix section for brownfield projects
  - Migration Phase Coverage table
  - Preserved Behavior Coverage table
  - Code Traceability Convention includes CHG and PB types
  - Notes section includes brownfield markers and best practices

---

## [0.0.29] - 2025-12-23

### Added

- **Bidirectional Spec ↔ Code Traceability** (AWS Kiro-inspired)
  - `@speckit:<TYPE>:<ID>` annotation convention for source code
  - Types: FR (Functional Requirement), AS (Acceptance Scenario), EC (Edge Case), VR/IR (Visual/Interaction)
  - Universal format works across Python, TypeScript, Go, Rust, Java, Kotlin, C/C++, etc.

- **Auto-generation in `/speckit.implement`**:
  - Agent automatically adds `@speckit` annotations when implementing tasks with [FR:], [TEST:], [EC:], [VR:], [IR:] markers
  - Annotation placement guidelines for functions, classes, components, and tests
  - Traceability verification step after each phase (Step 10)
  - Self-correction for missing annotations before proceeding to next phase

- **Code Traceability Validation in `/speckit.analyze`**:
  - Section N: Forward traceability (Spec → Code) - validates FRs have code annotations
  - Section N: Backward traceability (Code → Spec) - detects orphan annotations
  - Section N: Task-to-code consistency - verifies tasks match annotations
  - Section N: Test coverage validation - validates AS scenarios have test annotations
  - Section O: Annotation freshness detection - identifies stale/orphan annotations
  - Traceability Matrix in analysis report with coverage percentages

### Changed

- Enhanced `/speckit.implement` with annotation placement guidelines and language-specific examples
- Enhanced `/speckit.analyze` with code scanning capabilities for `src/`, `tests/`, and related directories
- Updated `tasks-template.md` with Code Traceability Convention reference section
- Updated severity assignments to include code traceability issues (HIGH: orphan annotations, MEDIUM: coverage gaps)

---

## [0.0.28] - 2025-12-23

### Added

- **Living Specs: Two-Folder Architecture** for maintaining current system documentation alongside historical feature specs
  - `specs/features/` — Historical feature specs (frozen after merge)
  - `specs/system/` — Living system specs (evolves with codebase)
  - Feature specs capture point-in-time requirements; system specs reflect current behavior

- **New `/speckit.merge` command**: Finalize features and update system specs after PR merge
  - Creates new system specs defined in "System Spec Impact → Creates"
  - Updates existing system specs defined in "System Spec Impact → Updates"
  - Archives feature spec by adding `.merged` JSON marker
  - Validates cross-references and dependency integrity
  - Generates detailed merge report
  - Supports `--maintain` mode for documentation corrections without new features
  - Supports `--impact` mode for pre-change impact analysis

- **New `system-spec-template.md`**: Template for living system specifications
  - Sections: Overview, Current Behavior, API Contract, Business Rules
  - Dependencies and Dependents tables for impact tracking
  - Spec History with append-only versioning linked to features
  - Test Coverage matrix for validation

- **System Spec Impact section in `spec-template.md`** (mandatory for merge)
  - Creates table: New system specs this feature introduces
  - Updates table: Existing system specs this feature modifies
  - Breaking Changes table: Migration paths for breaking behavior
  - No Impact checkboxes: For internal refactoring or test-only changes

### Changed

- **`/speckit.analyze` enhanced with system spec validation**:
  - Category K: System Spec Impact validation (incomplete sections, orphaned updates)
  - Category L: System Spec Integrity (missing history, broken dependencies)
  - Category M: Impact Analysis (unreviewed dependents, breaking changes)
  - New System Spec Status section in report output

- **`create-new-feature` scripts updated for two-folder architecture**:
  - Feature directories now created in `specs/features/` instead of `specs/`
  - Both bash and PowerShell scripts automatically create `specs/system/` directory
  - Branch numbering now checks `specs/features/` for existing specs

---

## [0.0.27] - 2025-12-23

### Fixed

- **Feature branch numbering collision bug**: Fixed bash script regex that only matched exactly 3-digit prefixes (`001-`, `012-`), missing branches like `1-feature`, `12-feature`, or `1234-feature`
  - Changed `^[0-9]\{3\}-` to `^[0-9]+-` (one or more digits)
  - Added double-check collision detection: `is_branch_number_taken()` and `is_spec_number_taken()` functions
  - If a number is already taken (edge case), script now increments until finding a free number
  - Applied same fixes to both `create-new-feature.sh` and `create-new-feature.ps1`

### Added

- **Layered Constitution Architecture**: 3-layer inheritance system for enterprise principles
  - **Layer 0** (`constitution.base.md`): 42 enterprise principles across 8 domains (READ-ONLY)
  - **Layer 1** (`constitution.domain.md`): Domain-specific extensions (fintech, healthcare, e-commerce, saas)
  - **Layer 2** (`constitution.md`): Project-specific overrides and additions
  - Inheritance rules: Higher layers can STRENGTHEN (SHOULD→MUST) but NEVER weaken (MUST→SHOULD)

- **Enterprise Base Principles** (`memory/constitution.base.md`) - 42 principles across 8 domains:
  - SEC (Security): 8 principles - secrets management, input validation, output encoding, dependency security, authentication, least privilege, RBAC authorization, SQL injection prevention
  - OBS (Observability): 4 principles - structured logging, error tracking, health endpoints, performance metrics
  - ERR (Error Exposure): 3 principles - no stack traces in production, generic user-facing errors, correlation ID in all errors
  - QUA (Quality): 7 principles - unit test coverage, integration testing, code review, documentation, tech debt tracking, code style enforcement, API integration tests
  - REL (Reliability): 6 principles - error handling, graceful degradation, idempotency, transaction boundaries, retry policies, optimistic locking
  - API (API Design): 6 principles - versioning, backwards compatibility, rate limiting, error responses, OpenAPI specification, pagination
  - PRF (Performance): 4 principles - response time SLA, resource limits, query optimization, caching strategy
  - CMP (Compliance): 4 principles - audit logging, data retention, privacy by design, accessibility

- **Domain Extension Templates** (`memory/domains/`):
  - `fintech.md`: FIN-001 to FIN-006 (Transaction Atomicity, Audit Immutability, Dual Control, Regulatory Reporting, Reconciliation, Money Precision)
  - `healthcare.md`: HIP-001 to HIP-006 (PHI Encryption, Access Logging, Minimum Necessary, Patient Rights, Breach Notification, BAA Tracking)
  - `e-commerce.md`: ECM-001 to ECM-007 (PCI Compliance, Inventory Consistency, Cart Persistence, Order Immutability, Price Consistency, Fraud Prevention, SEO Friendliness)
  - `saas.md`: SAS-001 to SAS-008 (Tenant Isolation, Usage Metering, Provisioning, Configuration, Data Residency, Offboarding, Service Level Tiers, Noisy Neighbor Prevention)

### Changed

- `/speckit.constitution` command now supports layered operations:
  - `set domain [name]`: Activate domain-specific principles
  - `add principle`: Add project-specific principles (PRJ-xxx)
  - `strengthen [ID]`: Strengthen base/domain principles (SHOULD→MUST)
  - `--merge`: Generate effective constitution view with all layers merged
- `memory/constitution.md` is now a project layer template with:
  - Strengthened Principles table for overriding base/domain principles
  - Project-Specific Principles section (PRJ-xxx format)
  - Technology Constraints table
  - Exceptions table with expiration dates and remediation plans

---

## [0.0.26] - 2025-12-23

### Added

- **New `/speckit.design` command**: Create visual specifications for UI-heavy features
  - Visual Language: Design tokens (colors, typography, spacing, shadows, icons)
  - Component Specifications: States, variants, accessibility, responsive behavior
  - Screen Flows: User interface sequences with Mermaid diagrams
  - Interaction Specifications: Animations, transitions, gestures with timing values
  - Accessibility Checklist: WCAG 2.1 validation (A/AA/AAA levels)
  - Design Tokens Export: Ready-to-use CSS variables

- **New `design-template.md`**: Complete template for design specifications
  - Semantic color tokens with light/dark mode and contrast ratios
  - Typography scale with rem/px values and line heights
  - 4px-based spacing system (--space-1 through --space-16)
  - Component anatomy diagrams and state definitions
  - Screen layout wireframes with component mapping
  - Responsive breakpoint definitions (mobile/tablet/desktop/wide)

- **Visual & Interaction Requirements in `spec-template.md`**:
  - VR-xxx markers for Visual Requirements (e.g., "Primary buttons MUST have 44x44px touch target")
  - IR-xxx markers for Interaction Requirements (e.g., "Loading indicator MUST appear within 100ms")
  - Design Constraints section for UI features
  - UI Acceptance Scenarios table (AS-UI-xxx)

- **Design System section in `plan-template.md`**:
  - Component Library selection (Radix UI, Headless UI, shadcn/ui)
  - Styling Approach (Tailwind CSS, CSS Modules, styled-components)
  - Icon System configuration
  - Animation Library choice
  - Accessibility Target level

- **Phase 2b: Design Foundation in `tasks-template.md`**:
  - Design Token Tasks: CSS variables setup
  - Component Foundation Tasks: Button, Input, layout primitives
  - Accessibility Foundation Tasks: Focus management, skip links
  - Animation Foundation Tasks: Transition presets, reduced-motion support
  - VR/IR requirement markers for UI task traceability

- **Claude Code integration via frontmatter**:
  - `claude_code.reasoning_mode`: extended/standard/none
  - `claude_code.thinking_budget`: Token allocation for reasoning
  - `claude_code.plan_mode_trigger`: Signal for plan mode activation
  - `claude_code.subagents`: Specialized agent delegation
    - market-researcher: Competitor and trend analysis
    - design-researcher: UI/UX patterns research
    - code-explorer: Codebase validation
    - architecture-specialist: Technology evaluation

### Changed

- `/speckit.concept` now includes Claude Code frontmatter with extended thinking and subagents
- `/speckit.analyze` now includes Claude Code frontmatter with extended thinking (12k budget)
- `/speckit.plan` now includes Claude Code frontmatter with architecture-specialist subagent
- `/speckit.design` workflow integrates with existing spec → plan → tasks pipeline

---

## [0.0.25] - 2025-12-23

### Added

- **Discovery Mode for `/speckit.concept`**: Active brainstorming and research capabilities
  - Mode Detection: Automatically detects vague input and offers discovery workflow
  - Phase 0a: Problem Discovery with 5 targeted brainstorming questions
  - Phase 0b: Market Research using web search (competitors, trends, user pain points)
  - Phase 0c: Solution Ideation with "What If" scenarios and Impact/Effort rating
  - Transition synthesis: Summarizes findings before structured capture
  - New "Discovery & Research" section in concept-template.md

### Changed

- `/speckit.concept` now supports two modes:
  - **Discovery Mode**: For vague or exploratory input (runs brainstorm + research phases)
  - **Capture Mode**: For users with clear vision (existing workflow, unchanged)
- Updated Validation Gates with Discovery Mode checklist
- Renumbered outline steps to accommodate new discovery phases

---

## [0.0.24] - 2025-12-23

### Added

- **New `/speckit.concept` command**: Capture complete project vision before detailed specifications
  - Feature Hierarchy with hierarchical IDs: EPIC-NNN → Feature (Fxx) → Story (Sxx)
  - User Journeys with cross-feature mapping
  - Cross-Feature Dependencies matrix
  - Ideas Backlog to prevent concept loss
  - Traceability Skeleton for spec tracking

- **Enhanced traceability system** with new ID formats:
  - Acceptance Scenario IDs: `AS-[story][letter]` (e.g., AS-1A, AS-1B, AS-2A)
  - Functional Requirement IDs: `FR-NNN` (e.g., FR-001, FR-002)
  - Edge Case IDs: `EC-NNN` (e.g., EC-001, EC-002)
  - Sub-priorities: P1a, P1b, P1c (MVP critical path) instead of simple P1, P2, P3

- **Task dependency and traceability markers**:
  - `[DEP:T001,T002]` - Explicit task dependencies with cycle detection
  - `[FR:FR-001]` - Links tasks to Functional Requirements
  - `[TEST:AS-1A]` - Links test tasks to Acceptance Scenarios
  - Mermaid-based Dependency Graph visualization
  - Requirements Traceability Matrix (RTM)
  - Coverage Summary with gap identification

- **Enhanced `/speckit.analyze` command**:
  - Dependency Graph Validation (cycle detection, orphan references, phase order)
  - Traceability Validation (FR → Tasks, AS → Tests chains)
  - Concept Coverage validation (if concept.md exists)
  - RTM accuracy validation
  - New severity categories for traceability issues
  - Detailed metrics and coverage percentages

### Changed

- `/speckit.specify` now supports Concept Integration:
  - Reads `specs/concept.md` if present
  - Maps Concept IDs to specifications
  - Generates tabular Acceptance Scenarios with IDs
  - Supports both standalone and concept-derived workflows

- `/speckit.tasks` now generates:
  - Dependency markers based on file/component relationships
  - FR/AS links for full traceability
  - Mermaid dependency graph
  - RTM and Coverage Summary sections
  - Validation for circular dependencies

- Updated README with new workflow steps and command descriptions

## [0.0.23] - 2025-12-23

### Fixed

- `constitution.md` is now preserved automatically during `specify init --here --force` upgrades. Previously, this file was overwritten with the default template, erasing user customizations.

## [0.0.22] - 2025-11-07

- Support for VS Code/Copilot agents, and moving away from prompts to proper agents with hand-offs.
- Move to use `AGENTS.md` for Copilot workloads, since it's already supported out-of-the-box.
- Adds support for the version command. ([#486](https://github.com/github/spec-kit/issues/486))
- Fixes potential bug with the `create-new-feature.ps1` script that ignores existing feature branches when determining next feature number ([#975](https://github.com/github/spec-kit/issues/975))
- Add graceful fallback and logging for GitHub API rate-limiting during template fetch ([#970](https://github.com/github/spec-kit/issues/970))

## [0.0.21] - 2025-10-21

- Fixes [#975](https://github.com/github/spec-kit/issues/975) (thank you [@fgalarraga](https://github.com/fgalarraga)).
- Adds support for Amp CLI.
- Adds support for VS Code hand-offs and moves prompts to be full-fledged chat modes.
- Adds support for `version` command (addresses [#811](https://github.com/github/spec-kit/issues/811) and [#486](https://github.com/github/spec-kit/issues/486), thank you [@mcasalaina](https://github.com/mcasalaina) and [@dentity007](https://github.com/dentity007)).
- Adds support for rendering the rate limit errors from the CLI when encountered ([#970](https://github.com/github/spec-kit/issues/970), thank you [@psmman](https://github.com/psmman)).

## [0.0.20] - 2025-10-14

### Added

- **Intelligent Branch Naming**: `create-new-feature` scripts now support `--short-name` parameter for custom branch names
  - When `--short-name` provided: Uses the custom name directly (cleaned and formatted)
  - When omitted: Automatically generates meaningful names using stop word filtering and length-based filtering
  - Filters out common stop words (I, want, to, the, for, etc.)
  - Removes words shorter than 3 characters (unless they're uppercase acronyms)
  - Takes 3-4 most meaningful words from the description
  - **Enforces GitHub's 244-byte branch name limit** with automatic truncation and warnings
  - Examples:
    - "I want to create user authentication" → `001-create-user-authentication`
    - "Implement OAuth2 integration for API" → `001-implement-oauth2-integration-api`
    - "Fix payment processing bug" → `001-fix-payment-processing`
    - Very long descriptions are automatically truncated at word boundaries to stay within limits
  - Designed for AI agents to provide semantic short names while maintaining standalone usability

### Changed

- Enhanced help documentation for `create-new-feature.sh` and `create-new-feature.ps1` scripts with examples
- Branch names now validated against GitHub's 244-byte limit with automatic truncation if needed

## [0.0.19] - 2025-10-10

### Added

- Support for CodeBuddy (thank you to [@lispking](https://github.com/lispking) for the contribution).
- You can now see Git-sourced errors in the Specify CLI.

### Changed

- Fixed the path to the constitution in `plan.md` (thank you to [@lyzno1](https://github.com/lyzno1) for spotting).
- Fixed backslash escapes in generated TOML files for Gemini (thank you to [@hsin19](https://github.com/hsin19) for the contribution).
- Implementation command now ensures that the correct ignore files are added (thank you to [@sigent-amazon](https://github.com/sigent-amazon) for the contribution).

## [0.0.18] - 2025-10-06

### Added

- Support for using `.` as a shorthand for current directory in `specify init .` command, equivalent to `--here` flag but more intuitive for users.
- Use the `/speckit.` command prefix to easily discover Spec Kit-related commands.
- Refactor the prompts and templates to simplify their capabilities and how they are tracked. No more polluting things with tests when they are not needed.
- Ensure that tasks are created per user story (simplifies testing and validation).
- Add support for Visual Studio Code prompt shortcuts and automatic script execution.

### Changed

- All command files now prefixed with `speckit.` (e.g., `speckit.specify.md`, `speckit.plan.md`) for better discoverability and differentiation in IDE/CLI command palettes and file explorers

## [0.0.17] - 2025-09-22

### Added

- New `/clarify` command template to surface up to 5 targeted clarification questions for an existing spec and persist answers into a Clarifications section in the spec.
- New `/analyze` command template providing a non-destructive cross-artifact discrepancy and alignment report (spec, clarifications, plan, tasks, constitution) inserted after `/tasks` and before `/implement`.
  - Note: Constitution rules are explicitly treated as non-negotiable; any conflict is a CRITICAL finding requiring artifact remediation, not weakening of principles.

## [0.0.16] - 2025-09-22

### Added

- `--force` flag for `init` command to bypass confirmation when using `--here` in a non-empty directory and proceed with merging/overwriting files.

## [0.0.15] - 2025-09-21

### Added

- Support for Roo Code.

## [0.0.14] - 2025-09-21

### Changed

- Error messages are now shown consistently.

## [0.0.13] - 2025-09-21

### Added

- Support for Kilo Code. Thank you [@shahrukhkhan489](https://github.com/shahrukhkhan489) with [#394](https://github.com/github/spec-kit/pull/394).
- Support for Auggie CLI. Thank you [@hungthai1401](https://github.com/hungthai1401) with [#137](https://github.com/github/spec-kit/pull/137).
- Agent folder security notice displayed after project provisioning completion, warning users that some agents may store credentials or auth tokens in their agent folders and recommending adding relevant folders to `.gitignore` to prevent accidental credential leakage.

### Changed

- Warning displayed to ensure that folks are aware that they might need to add their agent folder to `.gitignore`.
- Cleaned up the `check` command output.

## [0.0.12] - 2025-09-21

### Changed

- Added additional context for OpenAI Codex users - they need to set an additional environment variable, as described in [#417](https://github.com/github/spec-kit/issues/417).

## [0.0.11] - 2025-09-20

### Added

- Codex CLI support (thank you [@honjo-hiroaki-gtt](https://github.com/honjo-hiroaki-gtt) for the contribution in [#14](https://github.com/github/spec-kit/pull/14))
- Codex-aware context update tooling (Bash and PowerShell) so feature plans refresh `AGENTS.md` alongside existing assistants without manual edits.

## [0.0.10] - 2025-09-20

### Fixed

- Addressed [#378](https://github.com/github/spec-kit/issues/378) where a GitHub token may be attached to the request when it was empty.

## [0.0.9] - 2025-09-19

### Changed

- Improved agent selector UI with cyan highlighting for agent keys and gray parentheses for full names

## [0.0.8] - 2025-09-19

### Added

- Windsurf IDE support as additional AI assistant option (thank you [@raedkit](https://github.com/raedkit) for the work in [#151](https://github.com/github/spec-kit/pull/151))
- GitHub token support for API requests to handle corporate environments and rate limiting (contributed by [@zryfish](https://github.com/@zryfish) in [#243](https://github.com/github/spec-kit/pull/243))

### Changed

- Updated README with Windsurf examples and GitHub token usage
- Enhanced release workflow to include Windsurf templates

## [0.0.7] - 2025-09-18

### Changed

- Updated command instructions in the CLI.
- Cleaned up the code to not render agent-specific information when it's generic.

## [0.0.6] - 2025-09-17

### Added

- opencode support as additional AI assistant option

## [0.0.5] - 2025-09-17

### Added

- Qwen Code support as additional AI assistant option

## [0.0.4] - 2025-09-14

### Added

- SOCKS proxy support for corporate environments via `httpx[socks]` dependency

### Fixed

N/A

### Changed

N/A

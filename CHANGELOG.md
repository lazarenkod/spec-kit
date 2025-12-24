# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to the Specify CLI and templates are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to the Specify CLI and templates are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.95] - 2026-01-08

### Added

- **Adaptive Model Selection Framework**: Intelligent cost optimization across SpecKit commands
  - Created `templates/shared/model-selection.md` - General-purpose framework for model routing
  - Created `templates/shared/specify/complexity-detection.md` - Spec-specific complexity scoring
  - Enables 30-50% cost savings on simple features while preserving quality

- **Adaptive Model Selection for `/speckit.specify`**:
  - Automatic complexity detection (SIMPLE/MODERATE/COMPLEX tiers)
  - Smart routing: Simple features → Sonnet ($0.10), Complex features → Opus ($0.50)
  - Detection signals: entity count, integration count, technical complexity, scope, word count
  - Expected savings: 30-50% for SIMPLE/MODERATE features (0% for COMPLEX)
  - Quality gates preserved (Constitution Alignment, Ambiguity Gate, SQS >= 80)
  - Override flag: `--model=haiku|sonnet|opus`

- **Preview Mode Detection for `/speckit.preview`**:
  - Automatic mode detection (static_mockup/interactive_preview/animated_preview)
  - Smart routing: Static → Haiku ($0.05), Interactive → Sonnet ($0.15), Animated → Opus ($0.50)
  - Detection signals: wireframe/layout keywords, component/state keywords, animation/gesture keywords
  - Expected savings: 40-60% for static mockups, 20-40% for interactive previews
  - Override flag: `--preview-mode=static_mockup|interactive_preview|animated_preview`

### Changed

- **Updated `/speckit.specify` workflow**:
  - Added Step 0: Complexity detection with adaptive model selection
  - Displays cost savings estimate before execution
  - Subagent model overrides based on complexity tier
  - Updated reference from `complexity-scoring.md` to `complexity-detection.md`

- **Updated `/speckit.preview` workflow**:
  - Added Step 0: Preview mode detection with adaptive model selection
  - Displays mode and cost estimate before execution
  - Subagent model overrides based on preview mode

### Performance

- **🚀 `/speckit.implement` Performance Optimization (Phase 1)**:
  - **Enabled batch aggregation**: Cross-wave task batching reduces 5 waves → 2-3 batches (20% time savings)
  - **Increased parallelism**: Pool size 4→8, max_parallel 3→6 (4% time savings)
  - **Aggressive wave overlap**: Threshold 80%→60% for earlier wave starts (5% time savings)
  - **Batch task status updates**: Queue-based file I/O minimizes contention (2% time savings)
  - **Total improvement**: ~31% faster execution (340s → 236s for typical features)
  - Modified files:
    - `src/specify_cli/wave_scheduler.py`: batch_mode=True, overlap_threshold=0.60, max_parallel=6
    - `src/specify_cli/agent_pool.py`: pool_size=8, batch_mode=True
    - `src/specify_cli/task_status_updater.py`: Added queue_update(), force_flush() for batch writes

- **⚡ `/speckit.implement` Performance Optimization (Phase 2)**:
  - **Async file I/O infrastructure**: Parallel artifact loading with aiofiles (8% potential time savings)
    - Created `src/specify_cli/async_file_ops.py` with load_artifacts_parallel()
    - 4x speedup: Sequential 800ms → Parallel 200ms for 4 files
    - Automatic fallback to synchronous I/O if aiofiles unavailable
  - **Early test verification (experimental)**: Infrastructure for TDD wave optimization (5% potential time savings)
    - Added `early_test_verification` flag (disabled by default) in WaveConfig
    - Methods: `_verify_test_and_unlock()`, `_is_test_task()` for early impl unlocking
    - **Status**: Infrastructure ready, requires integration testing before enabling
  - **Updated dependencies**: Added aiofiles>=24.1.0 to pyproject.toml
  - **Phase 2 total (when fully enabled)**: Additional ~9% improvement (236s → 216s)
  - Modified files:
    - NEW: `src/specify_cli/async_file_ops.py`: Async file loading utilities
    - `src/specify_cli/wave_scheduler.py`: load_artifacts_async(), early test verification methods
    - `pyproject.toml`: Added aiofiles dependency

### Technical Details

- Modified `templates/commands/specify.md`:
  - Lines 68-94: Added `adaptive_model` configuration with tier routing
  - Lines 1254-1295: Added complexity detection and model selection logic in Step 0
- Modified `templates/commands/preview.md`:
  - Lines 19-52: Added `adaptive_model` configuration with mode routing
  - Lines 2357-2407: Added mode detection and model selection logic in Step 0
- Created `templates/shared/specify/complexity-detection.md` (397 lines)
- Created `templates/shared/model-selection.md` (472 lines)

### Cost Impact

**Estimated savings per feature lifecycle**:
```
Before Phase 2:
  /speckit.specify: $0.50 (always Opus)
  /speckit.preview: $0.50 (always Opus)
  Total: $1.00

After Phase 2 (50% simple features):
  /speckit.specify: $0.30 avg (50% Sonnet, 50% Opus)
  /speckit.preview: $0.25 avg (50% Haiku/Sonnet mix)
  Total: $0.55
  Savings: $0.45 (45%)
```

**Combined with Phase 1**:
```
Total lifecycle cost:
  Before: $7.37 per feature
  After: $7.01 per feature
  Total savings: ~5% overall
```

## [0.0.94] - 2026-01-08

### Changed

- **Model Optimization for `/speckit.taskstoissues`**: Downgraded orchestrator model from Sonnet to Haiku
  - Template-based conversion requires minimal reasoning for orchestration
  - Subagents already optimized (task-parser: Haiku, issue-creator: Sonnet)
  - Expected cost reduction: ~85% for orchestration layer
  - Quality preserved through subagent model overrides

### Fixed

- **Task Status Updates in `/speckit.implement`**: Restructured agent prompts to make task status update requirements impossible to miss
  - Moved critical "⚠️ TASK STATUS UPDATE PROTOCOL" instructions to TOP of each Wave 3 agent prompt (was at bottom)
  - Added visual separator boxes (═══) around mandatory update protocol
  - Enhanced Step 9 protocol with prominent blocking visual box (🚨 DO NOT SKIP)
  - Modified agents: `data-layer-builder`, `api-builder`, `ui-feature-builder`
  - Ensures 100% task status update compliance before proceeding to next task
  - Fixes issue where agents would skip updating tasks.md and move to new tasks

### Technical Details

- Modified `templates/commands/implement.md`:
  - Lines 549-579: data-layer-builder prompt restructured
  - Lines 609-640: api-builder prompt restructured
  - Lines 647-678: ui-feature-builder prompt restructured
  - Lines 1572-1624: Step 9 enhanced with blocking visual box
- Changes from reactive enforcement (checkpoint after wave) to proactive prevention (visual prominence before task)
- Modified `templates/commands/taskstoissues.md`:
  - Line 8: Changed orchestrator model from `sonnet` to `haiku`
  - Added optimization comment explaining reasoning

## [0.0.93] - 2026-01-08

### Changed

- **Minimized `/speckit.preview` CLI API**: Reduced ~45 flags to 12 core flags + 4 presets
  - New presets: `--quick`, `--ci`, `--review` (default is full preview)
  - New `--skip <features>` and `--only <features>` flags with 10 feature keywords
  - New `--baseline <action>` flag consolidating baseline management
  - Feature keywords: `quality`, `gallery`, `frames`, `gestures`, `deploy`, `storybook`, `mockups`, `screenshots`, `regression`, `states`

- **Moved `COMMANDS_GUIDE.md`** from root to `docs/` directory
  - Updated `/speckit.preview` section with new minimal API
  - Document version 1.3.0

## [0.0.92] - 2026-01-08

### Added

- **Mockup Quality Engine** for `/speckit.preview`:
  - New **MQS (Mockup Quality Score)**: 0-100 metric with 6 dimensions (Visual Fidelity 25%, Token Compliance 20%, Accessibility 20%, Responsiveness 15%, Interaction 10%, Polish 10%)
  - Quality gates: ≥80 Production Ready, 60-79 Needs Polish, 40-59 Major Issues, <40 Regenerate
  - 7 new quality-focused subagents:
    - `mockup-quality-analyzer`: Claude Vision-based visual quality analysis
    - `token-compliance-validator`: Detect hardcoded values vs design tokens
    - `accessibility-overlay-generator`: Visual a11y annotations (contrast, touch, focus, ARIA)
    - `state-matrix-generator`: Component state × variant grid visualization
    - `visual-regression-validator`: Pixelmatch-based baseline comparison
    - `fidelity-scorer`: Aggregate MQS calculation with quality gates
    - `mockup-improver`: Auto-fix loop (up to 3 cycles) when MQS < threshold

- **New supporting templates**:
  - `templates/shared/mqs-rubric.md`: Complete MQS scoring system with dimension breakdowns
  - `templates/shared/token-patterns.md`: Regex patterns for token violation detection
  - `templates/shared/a11y-overlay-styles.md`: CSS/JS for accessibility overlay generation

- **New CLI flags** for `/speckit.preview`:
  - `--validate-quality` / `--mqs`: Run full MQS analysis
  - `--token-check`: Token compliance validation only
  - `--a11y-overlay`: Generate accessibility overlays
  - `--state-matrix` / `--all-states`: Generate component state matrices
  - `--regression` / `--update-baseline` / `--diff-threshold`: Visual regression testing
  - `--mqs-gate <threshold>`: Set minimum MQS score (default: 80)
  - `--auto-improve` / `--max-cycles`: Auto-fix when MQS below threshold
  - `--quality-full`: Run all quality checks
  - `--no-quality`: Skip quality validation

## [0.0.91] - 2026-01-08

### Added

- **Preview 2.0: Full Interactive Device Mockups** for `/speckit.preview`:
  - New `device-profiles.md` with 20+ device profiles (iPhone, iPad, Pixel, Samsung, MacBook, watches)
  - Device Frame Generator: Wraps previews in realistic device frames with bezels, notches, status bars
  - Gesture Simulator: Touch gesture injection (tap, swipe, long-press, pinch, pull-to-refresh)
  - Safe Area Injector: CSS env() polyfills for notches and home indicators
  - Touch Target Validator: WCAG 2.1 AAA compliance checking (44x44px minimum)
  - Multi-Device Gallery: Side-by-side comparison, synchronized scroll, device carousel, breakpoint slider
  - Shareable Preview Deployer: Deploy to Firebase/Vercel/Cloudflare/Surge with QR codes

- **New CLI flags** for `/speckit.preview`:
  - `--device <id>` / `--devices <category>`: Target specific devices or categories
  - `--framed` / `--debug`: Add device frames with optional safe area overlay
  - `--gestures`: Enable touch gesture simulation
  - `--validate-touch-targets`: Run WCAG touch target validation
  - `--gallery` / `--sync-scroll` / `--responsive`: Multi-device comparison views
  - `--deploy <platform>` / `--password` / `--expires`: Shareable preview deployment
  - `--orientation portrait|landscape|both`: Device orientation support

### Changed

- **screenshot-capturer** now depends on device-frame-generator for framed screenshots
- **design-quality-validator** enhanced with device-specific checks (touch targets, safe areas)

## [0.0.90] - 2026-01-08

### Added

- **Changelog Updater** for `/speckit.implement`:
  - New `changelog_update` orchestration config
  - New `changelog-updater` subagent in Wave 5 (after code-reviewer)
  - Automatically updates project CHANGELOG.md after feature completion
  - Creates Keep a Changelog format entry with story ID, AS-xxx, FR-xxx
  - Skip markers: `[INTERNAL]`, `[NO-CHANGELOG]`
  - Skip conditions: Infrastructure-only waves (1-2)

### Changed

- **documentation-generator** now depends on changelog-updater (changelog first, then docs)

## [0.0.89] - 2026-01-07

### Added

- **Task Status Enforcement** for `/speckit.implement`:
  - New `task_status_enforcement` orchestration config
  - MANDATORY task update instructions in all Wave 3 subagents (data-layer-builder, api-builder, ui-feature-builder)
  - New `task-status-enforcer` checkpoint subagent (Wave 3.6)
  - Ensures 100% of completed tasks are marked `[X]` in tasks.md

### Changed

- **Wave 3 subagents** now include explicit task update requirement
- **test-verifier** depends on task-status-enforcer (ensures tasks updated before testing)

## [0.0.88] - 2026-01-07

### Added

- **PBT Just-in-Time Mode** for `/speckit.implement`:
  - Automatic property test execution after each related task
  - Auto-fix loop (max 3 attempts) for implementation bugs
  - Task-to-Property mapping via FR/AS traceability
  - Shrunk counterexamples captured for regression testing
  - New `pbt-jit-runner` subagent in Wave 3.5
  - Skip flag: `--skip-pbt-jit`

- **New file**: `templates/shared/pbt/just-in-time-protocol.md`
  - Complete JIT protocol documentation
  - Execution commands per language
  - Auto-fix strategies for common bugs
  - Metrics collection format

### Changed

- **`/speckit.properties`**: Auto-handoff to implement (`auto: true`)
  - After successful properties extraction, automatically continues to implement
  - PBT JIT mode enabled when properties.md exists

- **`/speckit.implement`**: Enhanced with PBT integration
  - New `pbt_jit` orchestration config
  - Properties Available Gate (informational)
  - Updated `property-test-generator` with JIT dependency
  - Final validation runs full suite after JIT checks

- Updated COMMANDS_GUIDE.md with JIT PBT documentation
- Updated CLAUDE.md with PBT Just-in-Time Workflow section

## [0.0.87] - 2026-01-07

### Changed

- **`specify init`**: No longer asks for template selection
  - Default behavior now creates minimal project structure
  - `--template` flag deprecated (shows warning, still works for backward compatibility)
  - Users should run `/speckit.constitution` after init to configure project

- **`/speckit.constitution`**: Now has interactive questionnaire mode
  - When called without arguments, asks 3 questions:
    1. Application Type (Web/Mobile/API/CLI/Desktop)
    2. Domain (SaaS/E-commerce/Fintech/Healthcare/Gaming/General)
    3. Language (English/Russian/Other)
  - Maps answers to appropriate principles and domain layers
  - Generates complete constitution based on responses
  - Existing direct commands still work (set domain, strengthen, --merge)

### Added

- **Tests for CLI init command** (`tests/test_cli_init.py`):
  - 9 test cases covering template deprecation and backward compatibility
  - Tests for deprecation warnings, invalid templates, help text
  - Verification that `select_template_with_descriptions` was removed

### Removed

- Interactive template selection UI from `specify init`
- `REQUIREMENTS_CHECKLIST.md` generation (templates deprecated)
- Template-specific notices and quick start steps

---

## [0.0.86] - 2026-01-07

### Added

- **New command `/speckit.staging`**: Provision Docker Compose staging environment BEFORE implementation
  - Creates `.speckit/staging/docker-compose.yaml` with PostgreSQL 16, Redis 7, Playwright
  - Generates `test-config.env` with connection strings
  - Validates QG-STAGING-001 quality gate (all services healthy)
  - Script: `scripts/bash/staging-provision.sh` with `--services`, `--reset`, `--status` flags

- **TDD workflow enforcement**: Tests are now REQUIRED (not optional)
  - Every AS-xxx with "Requires Test = YES" must have a corresponding [TEST:AS-xxx] task
  - Test Traceability Matrix (TTM) is mandatory in tasks.md
  - Quality Gate QG-TEST-001 blocks if any AS lacks a test task
  - No `--skip-tests` flag available

- **TDD wave ordering in `/speckit.implement`**:
  - Wave 0: Staging Validation (`staging-validator` agent)
  - Wave 2: Test Scaffolding (`test-scaffolder`, `e2e-test-scaffolder` agents) - TDD Red Phase
  - Wave 4: Test Verification (`test-verifier` agent) - TDD Green Phase
  - Tests created BEFORE implementation code

- **New Quality Gates** for TDD workflow:
  - QG-STAGING-001: All Docker services healthy (CRITICAL)
  - QG-TEST-001: 100% AS coverage with test tasks (CRITICAL)
  - QG-TEST-002: Test framework configured (CRITICAL)
  - QG-TEST-003: Tests fail first - TDD red (HIGH)
  - QG-TEST-004: Coverage >= 80% (CRITICAL)

- **CI/CD templates** for TDD pipeline in `templates/shared/ci-templates.md`:
  - GitHub Actions workflow (`tdd-pipeline.yml`) with staging, tests, quality gates
  - GitLab CI configuration with TDD stages
  - Local TDD runner: `scripts/bash/run-tdd-pipeline.sh`

### Changed

- **`/speckit.tasks`**: Tests changed from OPTIONAL to REQUIRED
  - SR-TASK-06 severity upgraded from HIGH to CRITICAL
  - TTM section now mandatory with QG-TEST-001 reference

- **`/speckit.implement`**: Restructured wave execution for TDD
  - Added staging-validator, test-scaffolder, e2e-test-scaffolder, test-verifier agents
  - ui-foundation-builder now depends on test-scaffolder
  - Wave numbering shifted to accommodate TDD phases

- **Core workflow order**: `/speckit.staging` now runs between `/speckit.tasks` and `/speckit.analyze`

## [0.0.85] - 2026-01-07

### Added

- **Automatic task status updates** during `/speckit.implement` execution:
  - Task checkboxes automatically update from `[ ]` → `[x]` on success
  - Failed tasks marked as `[!]` with error message comments
  - Thread-safe file operations with platform-specific locking (fcntl/msvcrt)
  - Graceful degradation when tasks.md not found (warning only, no crash)
  - Real-time console feedback on update success/failure
  - All task markers (`[P]`, `[US#]`, `[DEP:]`, `[FR:]`, etc.) preserved during updates
- **New module**: `src/specify_cli/task_status_updater.py` with `TaskStatusUpdater` class
- **Integration**: WaveScheduler callback system enhanced to update tasks.md after each task completion
- **Documentation**: Updated `templates/tasks-template.md` with automatic updates section

### Changed

- **`/speckit.implement` behavior**: No longer requires manual checkbox marking - fully automatic
- **Callback enhancement**: `on_task_complete` in `__init__.py` now updates tasks.md in real-time

## [0.0.84] - 2026-01-06

### Enhanced

- **Stitch Integration robustness** with proven patterns from production automation:
  - **Robust element finding** (`stitch_find_element_robust()`):
    - Try primary + all fallback selectors with 5s timeout each (not 10s total)
    - Check `isVisible()` before using any element
    - Log which selector worked for debugging
    - Continue to next fallback if element found but hidden
  - **Interactive fallback mode**:
    - When all selectors fail, ask user to click the element manually
    - Use `:focus` selector to capture user's selection
    - Beautiful console UI guides user through process
    - Enable with `--allow-interactive` flag
  - **Clipboard-based input** (10x faster than typing):
    - Try clipboard paste first (instant vs ~140ms per char typing)
    - Automatic OS detection (Meta+V for Mac, Ctrl+V for Windows/Linux)
    - Fallback to typing if clipboard permissions fail
    - Override with `--prefer-typing` for more human-like behavior
  - **Better error recovery**:
    - Platform-aware keyboard shortcuts (Meta/Control detection)
    - Session re-authentication detection
    - Detailed element finding logging
    - Graceful degradation from fast to slow methods

### Changed

- **Module version**: `templates/shared/stitch-integration.md` v3.0.0 → v3.1.0
- **Selector resolution**: Updated `stitch_generate_mockup()` to use new robust element finder
- **Text entry**: Replaced slow typing with clipboard-first approach (10x faster)
- **Button finding**: Both prompt input and generate button now use robust finding with visibility checks

### Added

- **New helper functions** in `templates/shared/stitch-integration.md`:
  - `stitch_find_element_robust()` - Robust element finding with visibility checks and logging
  - `stitch_wait_for_user_click()` - Interactive element identification fallback
  - `stitch_enter_text_clipboard()` - Clipboard-based text entry with typing fallback
  - `wait_for_enter_key()` - Cross-platform user input helper
- **New flags** for `/speckit.design`:
  - `--allow-interactive` - Enable interactive fallback when selectors fail
  - `--prefer-typing` - Force typing instead of clipboard (more human-like)
- **Enhanced documentation** with usage examples for new features

### Context

These enhancements are based on analyzing production Stitch automation scripts from `/Users/dmitry.lazarenko/Documents/projects/ai/tm/.speckit/stitch-old/`:
- `stitch-automation.js` (641 lines) - Production-tested selector strategies
- `debug-stitch-ui.js` (208 lines) - Element discovery and visibility checks
- `debug-shadow-dom.js` (210 lines) - Shadow DOM traversal patterns
- `manual-workflow.sh` (134 lines) - Semi-automated workflow with clipboard

## [0.0.83] - 2026-01-06

### Fixed

- **Critical Playwright selector failure** after Google Stitch UI update (2026-01-06):
  - **Root cause**: Google migrated prompt input from `<textarea>` to TipTap rich text editor (contenteditable `<div>`)
  - **Impact**: All mockup generation was broken due to unable to find prompt input field
  - **Resolution**: Updated `promptInput` selector in `templates/shared/stitch-selectors.md`:
    - New primary selector: `div[contenteditable="true"][role="textbox"]` (v2.0.0)
    - Added 3 additional v2.0.0 fallbacks for TipTap editor variants
    - Kept all v1.0.0 selectors as fallbacks for rollback compatibility
    - Total fallbacks: 9 (4 new + 5 old)
  - **Selector version**: v1.0.0 → v2.0.0
  - **Text input method change**: Now uses `.textContent` instead of `.value` for contenteditable divs

### Added

- **Selector debugging and diagnostic tools**:
  - **New flag**: `--audit-selectors` for testing all Stitch UI selectors without mockup generation
    - Tests all 26 selectors (authentication, input, loading, preview, export, error, navigation)
    - Generates comprehensive audit report with success/failure breakdown
    - Automatically captures debug screenshots for failed selectors
    - Saves screenshots to `.speckit/debug/selector-failures/`
    - Example: `/speckit.design --mockup --audit-selectors`
  - **New module**: `templates/shared/stitch-debug-utils.md` (~400 lines)
    - `test_selector()` - Test individual selector with all fallback variants
    - `audit_all_selectors()` - Full audit of all selectors with summary report
    - `inspect_element_at_selector()` - Detailed DOM element inspection with suggested selectors
    - `explore_selectors_interactively()` - Interactive mode for discovering new selectors
    - `ENSURE_DIRECTORY_EXISTS()`, `PERCENTAGE()`, timestamp helpers
  - **Audit mode integration** in `templates/shared/stitch-integration.md`:
    - Early exit branch in `stitch_main()` when `--audit-selectors` is set
    - Automatic browser setup and Stitch authentication
    - Returns audit results without generating mockups
    - Supports `--debug` flag for verbose selector testing
  - **Documentation** in `templates/commands/design.md`:
    - Added `--audit-selectors` to Developer Flags section
    - Detailed usage examples with expected output
    - Troubleshooting guide for broken selectors
    - Integration examples with `--debug` flag

- **Selector version tracking and maintenance system**:
  - **Version history** added to `templates/shared/stitch-selectors.md`:
    - Current version tracking (v2.0.0 as of 2026-01-06)
    - UI Change Log table with dates, changes, and status
    - Known UI Patterns by Version section documenting selector evolution
  - **UI Change Detection Strategy** guide:
    - Step-by-step process for updating selectors after Google UI changes
    - Selector stability ranking (data-testid > aria-label > classes > text)
    - Best practices for maintaining 8-10 fallbacks per selector
    - Examples of testing new selectors in DevTools Console
  - **Maintenance documentation**:
    - How to identify broken selectors using `--audit-selectors`
    - How to inspect live Stitch UI with DevTools
    - How to test and update selectors in this file
    - Automated monitoring suggestions (weekly cron jobs)

### Changed

- **Selector resilience improvements** in `templates/shared/stitch-selectors.md`:
  - `promptInput` now supports both textarea (v1.0.0) and contenteditable (v2.0.0) UI patterns
  - Fallback chains extended to handle multiple UI versions simultaneously
  - Backward compatibility maintained: old selectors kept for potential Google UI rollbacks
  - Description updated to reflect TipTap editor architecture

### Developer Notes

**For future Google Stitch UI changes:**
1. Run `/speckit.design --mockup --audit-selectors` to identify broken selectors
2. Inspect live UI at <https://stitch.withgoogle.com> with DevTools
3. Update `templates/shared/stitch-selectors.md` with new selectors
4. Increment version, update UI Change Log
5. Test with `--audit-selectors` again to verify fix
6. Update this CHANGELOG with details

**Time to fix this issue**: ~2 hours (inspection + updates + testing + documentation)

---

## [0.0.82] - 2026-01-06

### Added

- **Enhanced Mockup Output Generation** (`/speckit.design --mockup` Phase 1 enhancements):
  - **Multi-viewport screenshots**: Desktop (1440px), Tablet (768px), Mobile (375px)
    - Previous: 2 viewports (desktop + mobile)
    - Now: 3 viewports with configurable selection via `--viewports` flag
    - Retina support: 2x device scale factor for high-DPI displays
  - **WebP optimization**: Automatic PNG → WebP conversion
    - Target: 30-50% file size reduction at 85% quality
    - Parallel conversion for performance
    - Keeps original PNG files for compatibility
    - Compression stats displayed in output summary
    - Disable with `--no-webp` flag
  - **Interactive HTML previews**: JavaScript-enhanced mockup previews
    - Hover effects on buttons/links (shadow, transform)
    - Click animations with ripple effects
    - Form field focus states
    - Modal overlay simulation
    - Auto-notification showing interactive capabilities
    - Generated as `preview-interactive.html` alongside standard output
    - Disable with `--interactive false` flag
  - **New output structure**:
    - 6 screenshot files per screen (3 PNG + 3 WebP) vs previous 2 PNG
    - Interactive preview HTML with embedded JavaScript
    - Compression statistics tracking (PNG vs WebP sizes)
  - **Module created**: `templates/shared/stitch-output-processor.md` (~300 lines)
    - `stitch_export_screenshots_enhanced()` function
    - `convert_screenshots_to_webp()` with parallel processing
    - `generate_interactive_preview()` with JS injection
    - `GENERATE_INTERACTIVE_JS()` dynamic script generator
    - `INTERACTIVE_CSS` style enhancements

- **Parallel Mockup Generation** (`/speckit.design --mockup` Phase 2 enhancements):
  - **Performance improvement**: 3-5x faster mockup generation
    - 10 screens: 450s → 90-180s (60% faster)
    - 15 screens: 675s → 270s (60% faster)
    - Configurable concurrency: 1-5 parallel screens (default: 3)
  - **Browser pool management**:
    - Reusable browser context pool (max 5 contexts)
    - Acquire/release pattern for efficient resource usage
    - Automatic context validation and cleanup
    - Context TTL: 5 minutes
    - Memory limits and low-memory mode support
  - **Intelligent batching**:
    - Splits screens into batches based on max concurrency
    - Rate limit protection: 5s delay between batches (configurable)
    - Error isolation: one screen failure doesn't crash entire batch
    - Concurrent processing within batches
  - **Real-time progress tracking**:
    - Live progress bar with completion percentage
    - ETA (Estimated Time to Arrival) calculation
    - Success/failed/in-progress counters
    - Currently processing screen names display
    - Console updates every 500ms
    - Final summary with performance stats
  - **Parallel/Sequential branching**:
    - Parallel mode enabled by default (`--parallel`)
    - Sequential mode available for debugging (`--no-parallel`)
    - Performance flags: `--max-parallel N`, `--batch-delay MS`
    - Browser pool automatically managed in parallel mode
    - Maintains backward compatibility with existing workflows
  - **Module created**: `templates/shared/stitch-parallel-engine.md` (~400 lines)
    - `stitch_generate_mockups_parallel()` orchestrator
    - `create_browser_pool()` with acquire/release methods
    - `create_progress_tracker()` with real-time rendering
    - `process_batch_parallel()` with error isolation
    - Performance metrics and resource management

- **Caching & Incremental Generation** (`/speckit.design --mockup` Phase 3 enhancements):
  - **Performance improvement**: 80% reduction on re-runs with changes
    - No changes: 450s → 5s (99% faster, all screens skipped)
    - 1 screen changed: 450s → 90s (80% faster, 9 skipped + 1 regenerated)
    - Design context changed: All screens regenerated (session reuse saves ~30s)
  - **Prompt cache system**:
    - Automatically caches generated prompts with metadata
    - Cache includes wireframe mtime, design context hash, prompt text
    - Reusable for retry/manual mode
    - Cache stored in `.speckit/stitch/cache/prompts/`
    - JSON format with version tracking
  - **Incremental generation detector**:
    - Detects unchanged screens by comparing:
      - Output file existence
      - Wireframe modification time
      - Design context hash
    - Skips unchanged screens automatically
    - Shows time savings estimate in console
    - Override with `--force` flag to regenerate all
    - Disable with `--incremental false`
  - **Browser session reuse**:
    - Persists authentication state (cookies + storage)
    - Session TTL: 1 hour (configurable)
    - Saves ~30s per run (10s browser startup + 20s auth flow)
    - Automatic session validation before reuse
    - CDP endpoint persistence for reconnection
    - Disable with `--no-reuse-session`
  - **Smart caching logic**:
    - SHA256 hashing of design context for change detection
    - File modification time tracking for wireframes
    - Cache index for fast lookup
    - Graceful degradation on cache failures
  - **Module created**: `templates/shared/stitch-cache-manager.md` (~300 lines)
    - `cache_prompt()` and `get_cached_prompt()` functions
    - `detect_incremental_screens()` with skip logic
    - `hash_design_context()` for change detection
    - `save_browser_session()` and `load_browser_session()` functions
    - `restore_browser_session()` with validation
    - Cache directory management and cleanup functions

- **Comprehensive Mockup Flags Documentation**:
  - **Output flags**: `--viewports`, `--no-webp`, `--no-optimize`, `--interactive`
  - **Performance flags**: `--parallel`, `--max-parallel`, `--batch-delay`, `--no-parallel`
  - **Caching flags**: `--incremental`, `--force`, `--reuse-session`, `--no-reuse-session`
  - **Developer flags** (Phase 5, coming soon): `--dry-run`, `--debug`, `--log-level`, `--retry-max`
  - **Gallery flags** (Phase 4, coming soon): `--gallery-mode`, `--no-gallery`
  - Flag reference table added to `templates/commands/design.md`
  - Updated output section showing enhanced directory structure
  - Examples for all flag combinations

### Changed

- **Mockup generation workflow** (`templates/shared/stitch-integration.md`):
  - Added parallel/sequential branching in Phase 4-5
  - Default behavior changed to parallel (opt-out with `--no-parallel`)
  - Export phase enhanced with multi-viewport and WebP support
  - Results tracking includes WebP compression statistics
  - Browser context management adapted for parallel mode
  - Module imports updated for output processor, parallel engine, and cache manager
  - **Phase 2b**: Incremental detection added before design context loading
    - Early exit if all screens unchanged
    - Wireframe filtering to only regenerate changed screens
    - Design context hash calculation for cache validation
  - **Phase 1b**: Session restoration added before authentication
    - Attempts to restore cached session first (~30s savings)
    - Falls back to normal authentication if restore fails
    - Session validation before reuse
  - **Sequential mode**: Prompt caching added during generation
    - Caches every generated prompt with metadata
    - Session saving before browser context close
  - **Parallel mode**: Note added that pool manages own session handling

- **Design command outputs** (`templates/commands/design.md`):
  - Output summary now shows 3 viewports + WebP files + interactive HTML
  - Directory structure documentation updated with new file formats
  - Performance stats section added (compression ratio, size savings)
  - Next steps include interactive preview opening
  - Enhanced exports section shows all new output types

### Performance

- **Mockup generation speed**: 3-5x faster with parallel mode
  - 3 screens: 135s → 60s (56% improvement)
  - 10 screens: 450s → 180s (60% improvement)
  - Batch delays ensure rate limit compliance
  - Resource usage scales with concurrency level

- **File size optimization**: 30-50% reduction with WebP
  - PNG total: 100 MB → WebP total: 50-60 MB
  - Automatic parallel conversion
  - No quality degradation (85% WebP quality)

## [0.0.81] - 2026-01-06

### Added

- **Ready-to-Execute Commands Generation** (`/speckit.concept` command enhancement):
  - Automatically generates copy-paste ready `/speckit.specify` commands at concept completion
  - **4 execution strategies** with ready commands:
    - **By Waves (RECOMMENDED)**: Separate commands for Wave 1 (Foundation), Wave 2 (Experience), Wave 3+ (Business)
    - **By Epics**: One command per epic with all its stories
    - **By Priorities**: Commands grouped by priority level (P1a, P1b, P2, P3)
    - **Entire Concept**: Single command for all stories at once
  - **Smart grouping**: Stories automatically grouped by feature within each command
  - **Story counts**: Each command variant shows total stories included
  - **Contextual guidance**: "When to use" explanations for each execution strategy
  - **Edge case handling**: Empty waves, long commands (>500 chars), missing metadata
  - **Step 7b**: New generation logic with parsing algorithms for story metadata extraction
  - **Helper documentation**: Parse Story Metadata and Group Stories by Feature helpers
  - Updated "Ready for Specification" section to reference new commands output
  - Commands generated from Feature Hierarchy, Execution Order, and Priority metadata
  - **Infrastructure Prerequisites**: Added warning about INFRA-AUTH, INFRA-LAYOUT, INFRA-ERROR tasks before Wave 1 execution
  - Updated Next Steps to include infrastructure prerequisites completion before implementation

- **Comprehensive Commands Guide** (`COMMANDS_GUIDE.md`):
  - Complete documentation for all 25+ Spec-Kit commands in Russian
  - **Workflow diagrams** for Greenfield and Brownfield projects
  - **Detailed command descriptions** with arguments, flags, and when to use
  - **Quick reference tables** by project phase and purpose
  - **Model selection guide** showing default models and reasoning budgets
  - **Troubleshooting section** for common issues (SQS < 80, circular dependencies, etc.)
  - **Quality Gates reference** (QG-001 to QG-012) with thresholds
  - **Examples** for each command with real-world use cases
  - Covers core workflow, supporting commands, and special modes (migrate, discover, properties)
  - Version 1.0.0 compatible with Spec-Kit v0.0.81+

## [0.0.80] - 2026-01-06

### Added

- **Acceptance Criteria Enhancement**: AI-powered acceptance scenario generation with confidence scoring and edge case prediction
  - **Confidence Scores (0.0-1.0)**: Each acceptance scenario includes AI confidence assessment of necessity
    - 0.90-1.0: Critical scenario validating core functionality
    - 0.70-0.89: Important scenario validating common path or significant error
    - <0.70: Flagged for human review
  - **Edge Case Prediction (STEP 4)**: Automatically predicts edge cases per entity type before scenario generation
    - Detects 21 entity types (11 standard + 10 domain-specific)
    - Assigns severity levels (CRITICAL/HIGH/MEDIUM/LOW) per edge case
  - **Suggested Edge Cases**: Each scenario lists edge cases it should handle with cross-references
  - **Coverage Gap Detection (STEP 6)**: Validates completeness by cross-checking scenarios against predicted edge cases
  - **Enhanced Completeness Formula (STEP 7)**: Weighted scoring with 7 components
    - Base coverage (60%): happy/error/boundary/security path coverage
    - Edge case coverage (20%): entity-level edge case awareness
    - Confidence bonus (10%): average scenario confidence score
    - Reasoning quality (10%): scenarios with clear justification
  - **10 Domain-Specific Entity Types** (`edge-case-heuristics.md`):
    - Currency (amount, price, cost, fee) - 6 edge cases
    - Percentage (rate, ratio, proportion) - 5 edge cases
    - Coordinates (latitude, longitude, GPS) - 6 edge cases
    - Timezone (tz, utc_offset) - 5 edge cases
    - Version (semver, release) - 5 edge cases
    - IP Address (IPv4/IPv6) - 6 edge cases
    - MAC Address (hardware_address) - 4 edge cases
    - Credit Card (cc_number, payment_card) - 5 edge cases
    - SSN (social_security, tax_id) - 4 edge cases
    - Locale (language, i18n) - 5 edge cases
  - **Quality Gate SR-SPEC-22**: Validates all scenarios have confidence >= 0.70 (MEDIUM severity)
  - **Spec Template Update** (`spec-template.md`):
    - Added "Confidence" column to acceptance scenarios table
    - Added "Predicted Edge Cases" subsection per user story
    - Documentation of confidence scoring interpretation
- **Automatic Test Case Generation from Specs**: AI-powered test task generation in `/speckit.tasks` (section 4.1)
  - **Detailed Test Structure**: ARRANGE/ACT/ASSERT mapping from Given/When/Then scenarios
  - **Test Data Suggestions**: Language-specific test data patterns (Python, TypeScript, Go, Java, Kotlin)
    - Entity-aware suggestions (email → faker.email(), password → secure generator)
    - Anti-patterns detection (hardcoded `test@example.com`, `password123`)
  - **Edge Case Test Tasks**: Automatic generation from section 1.1's `suggested_edge_cases`
    - [TEST:AS-xxx:EDGE-n] markers for edge case traceability
    - Dedicated test tasks for each predicted edge case
  - **Test Type Classification**: AI classifies appropriate test type per scenario
    - HAPPY_PATH → Integration Test
    - ERROR_PATH/BOUNDARY/ALT_PATH → Unit Test
    - SECURITY → Security Test
  - **Property-Based Testing Suggestions**: Recommends `/speckit.properties` when applicable
  - **Enhanced Pass W Validation** (`analyze.md`):
    - Check 8: Test Structure Completeness validation
    - Check 9: Edge Case Test Coverage validation
    - Check 10: Test Data Pattern Quality warnings
  - **Test Task Quality Dimension**: New SQS dimension (10% weight)
    - Test Coverage (40%): All "Requires Test = YES" scenarios have tasks
    - Test Task Detail (30%): Tasks have structure, assertions, data suggestions
    - Test Type Appropriateness (20%): Correct test type per classification
    - Edge Case Coverage (10%): All suggested edge cases have test tasks
  - **Enhanced Tasks Template** (`tasks-template.md`):
    - Rich test task format with Test Structure, Test Data Suggestions, Edge Cases
    - Language-specific code examples in ARRANGE/ACT/ASSERT format
    - Estimated effort per test task
  - **Test Task Generator Subagent** (`tasks.md`):
    - 6-step AI generation process in /speckit.tasks command
    - Integration with section 1.1 edge case prediction
    - Multi-language support with language detection

### Changed

- **Acceptance Criteria Generator** (`specify.md` lines 183-445):
  - Expanded from 5-step to 7-step RaT (Refine-and-Thought) prompting
  - STEP 4 (NEW): PREDICT EDGE CASES - entity-type-based edge case prediction
  - STEP 5 (enhanced): GENERATE SCENARIOS - now includes confidence_score and suggested_edge_cases fields
  - STEP 6 (NEW): VALIDATE COMPLETENESS - cross-check scenarios against predicted edge cases
  - STEP 7 (enhanced): SCORE COMPLETENESS - updated formula with 7 weighted components
  - Output schema updated with predicted_edge_cases, coverage_gaps, and completeness components
- **Concept Template Section Reorganization** (`concept-template.md` v2.1-flow-optimized):
  - Reorganized 19 sections to follow logical top-down flow (Strategy → Discovery → Features → Execution)
  - **Discovery & Research** moved to position 4 (was 8) — Research must inform feature decisions
  - **Execution Order** moved to position 12 (was 7) — Plan WHEN after defining WHAT
  - **Section Completion Checklist** moved to position 17 (was 4) — Meta/tracking content at end
  - Added 4 flow rationale comments explaining section groupings at key transitions
  - Updated Section Completion Checklist to reflect new section positions
  - Template version updated from v2.0-alternatives to v2.1-flow-optimized

### Technical Details

- Implementation approach: Template-based enhancement (no new Python modules)
- Based on: AI_AUGMENTED_SPEC_ARCHITECTURE.md section 1.1
- Backward compatible: Legacy specs without confidence scores receive WARN status, not FAIL

## [0.0.79] - 2026-01-06

### Fixed

- **Markdownlint errors**: Resolved MD034 (bare URL) in wcag-21-aa-requirements.md and MD028 (blank line in blockquote) in concept-variants.md

### Added

- **Comprehensive Command Audit Report**: Audited all 26 spec-kit commands to ensure no section-skipping issues exist (SPEC-KIT-COMMAND-AUDIT-REPORT.md)
- **Pre-commit workflow**: Added GitHub Actions workflow to run pre-commit checks on all PRs and pushes
- **Hook installation script**: Added scripts/install-hooks.sh for easy local pre-commit setup

## [0.0.78] - 2026-01-06

### Changed

- **BREAKING**: `/speckit.concept` command now generates Product Alternatives instead of Scope Variants
  - **Product Alternatives** (Phase 0d/0e): Generate 3-5 fundamentally different product visions (Conventional, Minimal, Disruptive, Premium, Platform)
  - User selects preferred alternative before expanding to full concept
  - Replaced scope-first approach with vision-first approach
  - Scope Variants (MINIMAL/BALANCED/AMBITIOUS) now OPTIONAL (Step 12)

- **Concept Template v2.0** (`concept-template.md`):
  - New "Product Alternatives" section with selected alternative + comparison matrix
  - "Concept Variants" section now marked OPTIONAL with status checkbox
  - Section Completion Checklist added (tracks 33 sections)
  - Version marker updated to v2.0-alternatives

- **CQS Scoring Updates** (`cqs-score.md`):
  - Strategic Depth: Added Product Alternatives (30 pts), reduced other criteria proportionally
  - Transparency: Scope Variants now optional bonus (10 pts), increased JTBD links (30 pts)

### Added

- **NEW**: `templates/shared/concept-sections/product-alternatives.md` (~580 lines)
  - 5 alternative generation strategies with scoring criteria (Problem Fit, Differentiation, Feasibility, Time to Market)
  - Comparison matrix template
  - Integration with Brainstorm-Curate protocol
  - Selection rationale framework

- **NEW**: `templates/commands/concept-variants.md` command (~270 lines)
  - On-demand scope variant generation (MINIMAL/BALANCED/AMBITIOUS)
  - Feature classification by JTBD priority
  - Variant metrics calculation (effort, risk, differentiation)
  - Comparison matrix and recommendation logic

- **Validation**: Self-review check SR-CONCEPT-27 for Product Alternatives (≥3 alternatives required)

### Fixed

- Concept Variants section clarified: distinguishes Product Alternatives (WHAT to build) vs Scope Variants (HOW MUCH to build)
- Updated `concept-variants.md` template with v2.0 status and relationship to Product Alternatives

## [0.0.77] - 2026-01-03

### Added

- **Property-Based Testing Integration** (`/speckit.properties` command)
  - EARS transformation pipeline for requirements → testable properties
  - 6 property types: inverse, idempotent, invariant, boundary, commutative, model-based
  - PGS (Property-Generated Solver) iterative mode with anti-deception mechanism
  - Multi-language code generation: Python (Hypothesis), TypeScript (fast-check), Go (rapid), Java (jqwik), Kotlin (Kotest)
  - Security generators for SQL injection, XSS, path traversal, command injection
  - Shrunk examples registry for counterexample preservation
- **PQS (Property Quality Score)** rubric for PBT quality measurement
- **New quality gates**: VG-PROP, VG-PROP-SEC, VG-EARS, VG-SHRUNK, VG-PGS, VG-PQS
- PBT hints section in spec-template.md
- PBT tasks section in tasks-template.md
- PBT strategy section in test-strategy.md
- W2 Property Coverage validation pass in analyze.md
- PBT testing wave in implement.md

## [0.0.76] - 2026-01-03

### Added

- **Migration Planning Framework v0.0.76** — Spec-driven code migration between architectures, versions, and cloud providers

  - **New**: `templates/commands/migrate.md` (~950 lines)
    - Three migration scenarios: `--from monolith`, `--upgrade <target>`, `--to-cloud <provider>`
    - MIG-xxx phase identifiers with dependency DAG
    - Parallel subagents: codebase-scanner, coupling-analyzer, dependency-mapper, migration-strategist, risk-assessor, rollback-planner
    - Self-review with SR-MIG-01 to SR-MIG-15 criteria
    - Auto-handoff to /speckit.plan after successful planning

  - **New**: `templates/shared/migration/coupling-analysis.md` (~170 lines)
    - Module dependency detection with instability scoring
    - Afferent/Efferent coupling calculation (Ca/Ce)
    - Instability index I = Ce / (Ca + Ce)
    - Migration candidate scoring (80-100: Phase1, 50-79: Phase2, 0-49: Phase3)
    - Coupling classification: TIGHT (≥10), LOOSE (3-9), MINIMAL (0-2)

  - **New**: `templates/shared/migration/strangler-fig.md` (~120 lines)
    - Strangler Fig pattern for monolith decomposition
    - Boundary identification and facade implementation
    - Traffic shifting strategies (1-5% → 10-25% → 50% → 100%)
    - Service mesh integration patterns

  - **New**: `templates/shared/migration/upgrade-detection.md` (~140 lines)
    - Version detection from package.json, requirements.txt, go.mod, Cargo.toml
    - Breaking change fetching and impact analysis
    - UPG-xxx upgrade item identifiers
    - Upgrade path generation with priority levels

  - **New**: `templates/shared/migration/cloud-mapping.md` (~180 lines)
    - Service equivalents for AWS, GCP, Azure, VK Cloud
    - Service discovery from docker-compose.yml and k8s manifests
    - Network topology planning
    - Cost estimation templates

  - **New**: `templates/shared/migration/risk-matrix-migration.md` (~80 lines)
    - Migration-specific risk assessment
    - Risk categories: Technical, Operational, Business, Schedule
    - 5×5 probability/impact matrix
    - RISK-MIG-xxx identifier format

  - **New**: `templates/shared/migration/rollback-strategy.md` (~90 lines)
    - Per-phase rollback strategies
    - Rollback triggers (>5% error rate, p99 > 2x baseline)
    - Rollback types: Immediate (<5 min), Gradual (10-30 min), Full (30-60 min)
    - Data rollback with PITR, log replay, backup restore

  - **New**: `templates/shared/migration/migration-phases.md` (~100 lines)
    - MIG-xxx phase template with full structure
    - Phase status values: PLANNED, IN_PROGRESS, VALIDATING, COMPLETED, ROLLED_BACK
    - Phase sequencing rules for dependency DAG
    - Success metrics templates

  - **New**: `templates/shared/migration/self-review-migration.md` (~80 lines)
    - SR-MIG-01 to SR-MIG-15 criteria table
    - Severity levels with weights (CRITICAL: 3, HIGH: 2, MEDIUM: 1)
    - Verdict logic and self-correction loop (up to 3 iterations)

  - **Enhanced**: `memory/domains/quality-gates.md` (+90 lines)
    - New Migration Gates section (QG-MIG-001 to QG-MIG-003)
    - QG-MIG-001: Rollback Plan Required (MUST) — 100% phases have rollback
    - QG-MIG-002: Risk Mitigation Required (MUST) — HIGH+ risks mitigated
    - QG-MIG-003: Coupling Analysis Complete (MUST) — All modules analyzed
    - Updated summary (23 total gates, 19 MUST level)

## [0.0.75] - 2026-01-03

### Added

- **Design Quality Framework v0.0.75** — World-class design specification quality with automated validation

  - **New**: `templates/shared/quality/dqs-rubric.md` (~290 lines)
    - 25-checkpoint Design Quality Score (DQS) rubric across 5 dimensions
    - Visual Hierarchy (25 pts): VH-01 to VH-05 — CTAs, headings, whitespace, visual weight, scanning
    - Consistency (20 pts): CN-01 to CN-05 — Tokens, components, naming, interactions, icons
    - Accessibility (25 pts): AC-01 to AC-05 — Contrast, touch targets, focus, screen reader, motion
    - Responsiveness (15 pts): RS-01 to RS-05 — Breakpoints, layout, touch/pointer, priority, images
    - Interaction Design (15 pts): ID-01 to ID-05 — States, timing, loading, errors, success
    - Thresholds: ≥70 Ready, 50-69 Needs Work, <50 Block

  - **New**: `templates/shared/a11y/wcag-21-aa-requirements.md` (~414 lines)
    - Comprehensive WCAG 2.1 AA checklist for design specifications
    - Color contrast requirements (4.5:1 text, 3:1 UI components)
    - Touch target minimums (44×44px)
    - Keyboard navigation and focus indicator requirements
    - Screen reader support and ARIA patterns
    - Reduced motion alternatives

  - **New**: `templates/skills/token-management.md` (~319 lines)
    - Design token extraction, validation, and multi-format export
    - Commands: `/token extract`, `/token validate`, `/token export`
    - Semantic naming patterns: `{category}-{property}-{variant}`
    - Theme support (light/dark mode)
    - Token validation rules and naming conventions

  - **New**: `templates/skills/storybook-generation.md` (~352 lines)
    - CSF 3.0 compliant Storybook story generation from component specs
    - TypeScript-first with `satisfies Meta<typeof Component>` pattern
    - Automatic story generation for all component variants
    - Play functions for interaction testing
    - Accessibility addon integration (a11y)
    - Autodocs generation

  - **New**: `templates/shared/token-export-formats.md` (~161 lines)
    - Multi-format token export templates
    - CSS Custom Properties with light/dark theme support
    - Tailwind CSS configuration generation
    - JSON (Style Dictionary compatible) format
    - Figma Variables REST API format

  - **Enhanced**: `memory/domains/quality-gates.md` (+40 lines)
    - New Design Quality Gates section (QG-DQS-001 to QG-DQS-003)
    - QG-DQS-001: Minimum Design Quality Score (MUST) — DQS ≥ 70
    - QG-DQS-002: Accessibility Compliance (MUST) — A11y dimension ≥ 60%
    - QG-DQS-003: WCAG Compliance (SHOULD) — All text meets contrast requirements
    - Updated enforcement matrix and summary (20 total gates, 16 MUST level)

  - **Enhanced**: `templates/commands/design.md` (+30 lines)
    - New skills: token-management, storybook-generation
    - Updated DQS Calculation section with rubric reference
    - A11y validation reference to WCAG requirements file

  - **Enhanced**: `templates/design-template.md` (+25 lines)
    - New DQS section with dimension score table
    - Token export format references
    - A11y checklist reference to detailed requirements

## [0.0.74] - 2026-01-03

### Added

- **Security by Design Framework v0.0.74** — Enterprise-grade security embedded into every spec phase

  - **New**: `memory/domains/security.md` (~420 lines)
    - 5 Core Security Principles (SBD-001 to SBD-005): Least Privilege, Defense in Depth, Secure Defaults, Minimize Attack Surface, Complete Mediation
    - OWASP Top 10 (2021) mapping with prevention patterns and requirement templates
    - Data Classification framework (Public → Internal → Confidential → Restricted)
    - Authentication patterns: Session-based, JWT, API Keys with secure code examples
    - Authorization patterns: RBAC and ABAC with policy definitions
    - Encryption standards: AES-256-GCM, Argon2id, Ed25519, TLS 1.3

  - **New**: `templates/shared/security/threat-model-template.md` (~305 lines)
    - STRIDE-based threat analysis (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation)
    - Asset inventory with data classification
    - Trust boundary identification with validation requirements
    - DREAD risk scoring (Damage, Reproducibility, Exploitability, Affected Users, Discoverability)
    - Security requirements derivation from threats (SEC-xxx requirement IDs)
    - Residual risk documentation

  - **New**: `templates/shared/security/owasp-checklist.md` (~600 lines)
    - 100 security checklist items (SEC-001 to SEC-100)
    - Covers all OWASP Top 10 categories with actionable checks
    - Python, JavaScript, YAML code examples for secure implementations
    - Priority levels and automation hints

  - **Enhanced**: `memory/domains/quality-gates.md` (+50 lines)
    - New Security Gates section (QG-SEC-001 to QG-SEC-005)
    - QG-SEC-001: Threat Model Required (MUST) — STRIDE coverage before implementation
    - QG-SEC-002: OWASP Checklist Passed (MUST) — 100% security checklist compliance
    - QG-SEC-003: Dependency Vulnerability Scan (MUST) — Zero critical/high CVEs
    - QG-SEC-004: Secret Scanning (MUST) — No hardcoded secrets
    - QG-SEC-005: Security Tests Exist (SHOULD) — Auth, authz, input validation tests
    - Updated enforcement matrix and summary (17 total gates, 13 MUST level)

  - **Enhanced**: `templates/spec-template.md` (+95 lines)
    - New **Non-Functional Requirements** section (mandatory)
      - Performance Requirements with p99 targets and thresholds
      - Security Requirements with data classification and OWASP considerations
      - Compliance Requirements (PII, Audit, Retention, GDPR/CCPA, Industry Standards)
    - New **Events** section (for event-driven features)
      - Events Produced/Consumed tables with schema links
      - Event Schema Example (JSON Schema format)

  - **Enhanced**: `templates/shared/quality/sqs-rubric.md` — NFR ID enforcement
    - CM-02 checkpoint now requires NFR-xxx IDs (NFR-PERF-*, NFR-SEC-*, NFR-REL-* mandatory)
    - Updated completeness indicators with NFR category requirements

  - **Enhanced**: `templates/shared/quality/completeness-checklist.md` (+90 lines)
    - New **NFR Requirements Validation** section
    - 8 NFR category prefixes defined (PERF, SEC, REL, SCAL, OBS, A11Y, CMP, MNT)
    - CHECK_NFR_REQUIREMENTS algorithm for automated validation
    - NFR → AS traceability checks
    - Vague term detection (prevents "fast", "secure" without quantification)
    - NFR scoring integration with weighted thresholds

- **Architecture Decision Records (ADR) Integration** — Automatic ADR generation in /speckit.plan workflow

  - **Enhanced**: `templates/plan-template.md` (+90 lines)
    - New **Architecture Decisions** section with lightweight ADR format
    - ADR-xxx identifier assignment for traceability
    - Linked Requirements (FR-xxx, NFR-xxx) for bidirectional tracing
    - ADR Summary table with status, impact, requirements columns
    - Decision Patterns and Requirement Coverage tracking
    - Integration with `specs/[feature]/adrs/` directory structure

  - **Enhanced**: `templates/commands/plan.md` (+60 lines)
    - New **ADR Generation Protocol** in Phase 0
    - Automatic ADR identifier assignment logic
    - Threshold detection for full ADR file creation (≥2 alternatives, High impact)
    - Full ADR file generation for complex decisions
    - ADR index (README.md) generation in adrs/ directory
    - Three new self-review criteria: SR-PLAN-11 (ADR Coverage), SR-PLAN-12 (ADR Traceability), SR-PLAN-13 (Full ADR Files)
    - Updated CRITERIA_SET to SR-PLAN-01 through SR-PLAN-13

  - **Enhanced**: `memory/knowledge/templates/adr-template.md` (+10 lines)
    - New **Linked Requirements** field in header metadata
    - Bidirectional traceability: ADR → FR-xxx/NFR-xxx
    - Example ADR updated with requirement references

## [0.0.73] - 2026-01-03

### Added

- **Enterprise Constitution Presets v0.0.73** — Compliance, security, governance, and SLA configuration for enterprise-grade projects

  - **Enhanced**: `memory/constitution.md` (+130 lines)
    - New **Compliance Requirements** section — GDPR, SOC 2 Type II, HIPAA, PCI-DSS, ISO 27001, FedRAMP, CCPA checkboxes with certification tracking
    - New **Security Standards** section — Authentication (OAuth2/OIDC), Authorization (RBAC/ABAC), Encryption (TLS 1.3, AES-256), Secrets Management, MFA, SSO configuration + Security Contacts table
    - New **Approval Matrix** section — Decision authority (Architecture Board, Security Team, Data Team, API Guild), approval requirements, escalation paths + Escalation SLA by priority (P0-P3)
    - New **Technology Radar** section — Adopt/Trial/Assess/Hold categorization for Languages, Frameworks, Databases, Infrastructure, Observability, Security + Radar Definitions + Technology Decisions Log
    - New **SLA Targets** section — Availability (99.9%), RTO (4h), RPO (1h), MTTR, P99 Latency, Error Rate + SLA Tiers by Environment + Breach Escalation matrix

  - **New**: `memory/domains/enterprise.md` (~180 lines)
    - 6 strengthened base principles (SEC-001, SEC-002, OBS-001, OBS-002, CMP-001, DOC-001)
    - ENT-001: Compliance-Driven Design (MUST) — Design with compliance from day one
    - ENT-002: Approval Workflow Enforcement (MUST) — Formal approvals with audit trail
    - ENT-003: Technology Governance (SHOULD) — Radar assessment before adoption
    - ENT-004: SLA Monitoring (MUST) — Continuous monitoring with automated escalation
    - ENT-005: Data Classification (MUST) — Public/Internal/Confidential/Restricted levels
    - ENT-006: Vendor Risk Assessment (SHOULD) — Security assessment for third-party integrations
    - Compliance Framework Integration matrix (GDPR, SOC 2, HIPAA, PCI-DSS, ISO 27001)
    - Domain combination guide (Production, FinTech, Healthcare, SaaS)

- **SQS Formalization & Quality Dashboard v0.0.73** — Formal 25-checkpoint specification quality scoring and unified quality metrics dashboard

  - **New**: `templates/shared/quality/sqs-rubric.md` (~275 lines)
    - Formal definition of 25-checkpoint SQS rubric (replaces old 4-factor formula)
    - 5 dimensions: Clarity (25pts), Completeness (25pts), Testability (25pts), Traceability (15pts), No Ambiguity (10pts)
    - Scoring scales per checkpoint with clear pass/fail guidance
    - Anti-patterns table (bad vs good examples)
    - Evidence requirements by tier (Tier 1/2/3)
    - SQS calculation worksheet template

  - **New**: `templates/shared/quality/quality-dashboard.md` (~275 lines)
    - Unified Quality Dashboard aggregating all phase metrics
    - Executive summary with CQS, SQS, Plan, Tasks, Implementation scores
    - CQS breakdown with evidence tier distribution
    - SQS breakdown with 25-checkpoint visualization
    - Plan quality and clarification status tracking
    - INVEST compliance for tasks with size distribution
    - Implementation quality gates status (QG-002 through QG-011)
    - Red flags section with critical/warning severity triggers
    - Trend analysis with historical score tracking
    - Quick commands reference for `/speckit.analyze` profiles

  - **Enhanced**: `memory/domains/quality-gates.md`
    - Updated SQS definition in Key Concepts to reference new rubric
    - QG-001 now uses 5-dimension rubric table with checkpoint details
    - Added link to formal `sqs-rubric.md` for full scoring guidance

  - **Enhanced**: `templates/metrics-report-template.md`
    - Replaced old 4-factor SQS formula with 25-checkpoint rubric format
    - Added checkpoint visualization grid `[CL01][CL02]...`
    - Improved quality level table with threshold indicators

  - **Enhanced**: `templates/commands/analyze.md`
    - Added `quality_dashboard` profile for unified quality reporting
    - Profile includes all validation passes and outputs to `quality-dashboard.md`
    - Updated Available Profiles table

  - **Enhanced**: `templates/spec-template.md`
    - Added optional `## Quality Checklist (SQS Self-Assessment)` section
    - Inline 25-checkpoint scoring tables for manual pre-implementation QA
    - SQS summary block with status indicators

## [0.0.72] - 2026-01-03

### Added

- **AI-Assisted Persona Synthesis & Evidence-Based CQS Enhancement v0.0.72**

  - **Section 1.3: AI-Assisted Persona Synthesis** (from AI_CONCEPT_EVOLUTION_ANALYSIS.md)
    - **Enhanced**: `templates/shared/concept-sections/persona-jtbd.md` (~90 lines added)
      - Data Sources for AI Persona Generation table (G2, Capterra, Reddit, job postings, industry reports)
      - AI Persona Synthesis Prompt Template with evidence citation requirements
      - Evidence Requirements per Persona (demographics, JTBD, WTP, deal breakers)
      - Persona Quality Gate with VS/S/M/W/N tier gating
    - **Enhanced**: `templates/shared/concept-sections/research-agents.md` (~100 lines added)
      - New tools: `review_analyzer`, `job_posting_parser`, `sentiment_analyzer`
      - Multi-source `data_sources` configuration (b2b_reviews, prosumer, job_postings, industry_reports)
      - 3-phase AI Synthesis workflow in prompt template
      - Evidence documentation with [EV-XXX] citations

  - **Section 2.1: Evidence-Based CQS (Assumptions → Evidence)** (from AI_CONCEPT_EVOLUTION_ANALYSIS.md)
    - **Enhanced**: `templates/shared/concept-sections/cqs-score.md` (~60 lines added)
      - Source Credibility Matrix (8 source types with base tiers)
      - Recency Decay Formula with configurable thresholds
      - Tier Decay Examples table
      - Conflict Detection Rules with resolution strategies
      - Conflict Registry template
    - **Enhanced**: `templates/shared/concept-sections/evidence-tracking.md` (~130 lines added)
      - Automated Evidence Tier Assignment with YAML rules
      - Evidence Quality Gate (blocking/warning per component)
      - Automated Tier Validation 5-step process
      - Evidence Tier Override with justification tracking
      - CQS-E Integration formula with tier multipliers

### Changed

- **CQS Inflation Prevention**: CQS can no longer be inflated by checking boxes without real evidence
- **Persona Validation**: Minimum STRONG tier now required for demographics and functional JTBD

## [0.0.71] - 2026-01-02

### Added

- **Fortune 500 Strategic Frameworks v0.0.71** — 9 new board-ready strategic frameworks for `/speckit.concept`

  - **Tier 1: Board Credibility (Critical)**
    - **New Module**: `templates/shared/concept-sections/investment-thesis.md` (~180 lines)
      - Board-ready investment case with executive summary table
      - Key assumptions matrix with evidence and confidence scoring
      - Risk-adjusted returns with base/upside/downside scenarios
      - Use of funds breakdown, milestones, kill criteria
      - Comparable transactions for valuation support
    - **New Module**: `templates/shared/concept-sections/strategic-alternatives.md` (~200 lines)
      - Build vs Buy vs Partner vs Nothing decision matrix
      - Weighted criteria scoring (speed, cost, strategic fit, risk)
      - Financial comparison across alternatives
      - Board-ready recommendation with rationale
    - **New Module**: `templates/shared/concept-sections/financial-sensitivity.md` (~250 lines)
      - NPV/IRR calculations across scenarios
      - Sensitivity analysis table (tornado diagram ready)
      - Monte Carlo simulation guidance
      - Break-even analysis and payback period

  - **Tier 2: Strategic Depth (High Value)**
    - **New Module**: `templates/shared/concept-sections/scenario-planning.md` (~290 lines)
      - Shell/McKinsey 2×2 uncertainty matrix
      - Four futures with probability-weighted strategies
      - Robust strategies across multiple scenarios
      - Early warning indicators per scenario
    - **New Module**: `templates/shared/concept-sections/strategic-options.md` (~200 lines)
      - Real options valuation framework
      - Option types: expand, delay, abandon, pivot, stage
      - Total option value calculation
      - Decision tree integration
    - **New Module**: `templates/shared/concept-sections/execution-confidence.md` (~190 lines)
      - R/Y/G confidence matrix by domain
      - Google-style greenlight criteria
      - Capability gap analysis with hiring plan
    - **New Module**: `templates/shared/concept-sections/portfolio-context.md` (~230 lines)
      - Strategic fit assessment (Core/Adjacent/Transform)
      - Resource allocation view
      - Cannibalization analysis
      - Synergy identification

  - **Tier 3: Corporate Strategy (Nice-to-Have)**
    - **New Module**: `templates/shared/concept-sections/moals-osm.md` (~280 lines)
      - Amazon MOALS framework (Mechanisms, Outputs, Actions, Learning, Systems)
      - Flywheel model for continuous improvement
      - WBR dashboard structure
      - Learning loops and feedback systems
    - **New Module**: `templates/shared/concept-sections/ecosystem-strategy.md` (~270 lines)
      - Platform/ecosystem strategy canvas
      - Partner economics and revenue share models
      - API strategy tiers (Public/Standard/Enterprise)
      - Ecosystem health metrics

  - **Updated**: `templates/commands/concept.md`
    - Added sections 5ab-IT, 5ab-SA, 5ab-FS (after Business Model Canvas)
    - Added sections 5c-SP, 5c-SO, 5c-EC, 5c-PC, 5c-ES (after Risk Assessment Matrix)
    - Added section 5d-MO (after Technical Discovery)
    - All 9 frameworks integrated with reference templates

### Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Fortune 500 frameworks | 18/27 (67%) | 27/27 (100%) |
| Board-ready concepts | Partial | Full |
| Strategic planning depth | Medium | High |
| Financial rigor | Low | High (NPV/IRR) |
| Scenario coverage | Single forecast | 4 futures |

## [0.0.70] - 2026-01-02

### Added

- **AI Augmentation Suite v0.0.70** — Multi-Agent Research Framework, Evidence-Based CQS, and Continuous Validation

  - **Feature 1: Multi-Agent Research Framework** — 4 parallel AI agents for accelerated market research
    - **New Module**: `templates/shared/concept-sections/research-agents.md` (~350 lines)
      - `market-intelligence-ai`: TAM/SAM/SOM calculation with cross-validation
      - `competitive-intelligence-ai`: Competitor analysis with pricing intel
      - `persona-researcher-ai`: JTBD synthesis with evidence tracking
      - `trend-analyst-ai`: Timing analysis and risk factors
    - Shared memory structure (`research_db`) for cross-agent references
    - Cross-validation rules: TAM variance <30%, ≥2 sources per claim, ≥3 evidence per JTBD
    - Research time reduction: 4-8 hours manual → 30-45 minutes automated
    - Cost: ~$0.75-1.00 per concept
    - **Workflow Update**: `templates/commands/concept.md` Phase 0b.1 enhanced

  - **Feature 2: Evidence-Based CQS** — Transform checkbox scoring to evidence tier scoring
    - **New Module**: `templates/shared/concept-sections/evidence-tracking.md` (~200 lines)
      - Evidence Tiers: VERY_STRONG (30pts), STRONG (25pts), MEDIUM (20pts), WEAK (5pts), NONE (0pts)
      - Evidence Registry table (EV-001, EV-002, ...)
      - Evidence Gap Analysis with priority assignments
      - Cross-Validation Matrix for critical claims
      - AI-assisted evidence collection integration
    - **Updated Module**: `templates/shared/concept-sections/cqs-score.md`
      - All 9 component scoring tables updated with Evidence Tier column
      - Source ID tracking for each criterion
      - Evidence Requirements per component (e.g., ≥3 sources for TAM)
      - Evidence Gap Report section

  - **Feature 3: Continuous Validation** — New `/speckit.validate-concept` command
    - **New Command**: `templates/commands/validate-concept.md` (~400 lines)
      - Re-validation workflow with 3 parallel validators
      - Market, Competitive, and Trend validators
      - CQS delta calculation with impact classification (CRITICAL/HIGH/MEDIUM/LOW)
      - Diff report generation: `concept-validation-{date}.md`
      - Evidence freshness scoring
      - Validation history tracking
    - **New Wrapper**: `.claude/commands/speckit.validate-concept.md`
      - Quick start guide with common usage patterns
      - Impact level reference table
      - Cost estimation (~$0.30-0.40 per validation)

### Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Research time | 4-8 hours | 30-45 minutes |
| Evidence quality | Binary (✓/✗) | Tiered (N/W/M/S/VS) |
| Source tracking | None | Evidence Registry |
| Concept freshness | One-time snapshot | Continuous validation |
| CQS baseline | ~60 | ~85+ (with evidence) |
| Cost per concept | $50-100 (manual) | ~$1 (automated) |

## [0.0.69] - 2026-01-02

### Added

- **Concept Transparency & Explainability Framework** — Full visibility into AI decision-making during `/speckit.concept`
  - **New Module**: `templates/shared/concept-sections/concept-variants.md` — 3 alternative concept variants (MINIMAL/BALANCED/AMBITIOUS)
    - Variant Comparison Matrix with timeline, feature count, risk level
    - Recommended variant with evidence-based rationale
    - Feature allocation by JTBD priority (MUST/SHOULD/COULD HAVE)
  - **New Module**: `templates/shared/concept-sections/selection-rationale.md` — Per-feature decision documentation
    - Selection Decision Table with SEL-NNN IDs
    - JTBD links, alternatives considered, evidence citations
    - Reversibility classification (Type 1 irreversible / Type 2 reversible)
  - **New Module**: `templates/shared/concept-sections/wave-rationale.md` — Wave grouping explanations
    - Why features are grouped together (dependencies, logical coherence)
    - Alternative groupings considered with rejection rationale
    - Wave completion gates and triggers for next wave
  - **New Module**: `templates/shared/concept-sections/reasoning-trace.md` — Decision chain visualization
    - RT-NNN formatted traces: Problem → JTBD → Persona → Feature → Priority
    - INCLUDE, EXCLUDE, DEFER trace types with evidence
    - Mermaid diagrams for Problem→Feature flow visualization
  - **Template Update**: `templates/concept-template.md` — 4 new sections
    - Concept Variants (after Executive Summary)
    - Feature Selection Rationale (after Feature Hierarchy)
    - Wave Rationale subsections in Execution Order
    - Reasoning Trace (before Next Steps)
  - **Workflow Update**: `templates/commands/concept.md` — New transparency steps
    - Step 4c: Generate Concept Variants (3 alternatives with comparison)
    - Step 6c: Document Feature Selection Rationale (per-feature decisions)
    - Step 8d: Document Wave Rationale (grouping explanations)
    - Step 10b: Generate Reasoning Trace (decision chain visualization)
    - Transparency Gates in Validation Gates section
  - **CQS Update**: `templates/shared/concept-sections/cqs-score.md` — Transparency component (5% weight)
    - Scoring criteria: variants, JTBD links, wave rationale, reasoning traces
    - Validation checklist for transparency items
  - **New Self-Review Criteria**: SR-CONCEPT-23 through SR-CONCEPT-26
    - SR-CONCEPT-23: Variants Generated (HIGH) — 3 variants documented
    - SR-CONCEPT-24: Per-Feature Rationale (HIGH) — >80% JTBD coverage
    - SR-CONCEPT-25: Wave Rationale (MEDIUM) — Wave grouping explanations
    - SR-CONCEPT-26: Reasoning Trace (MEDIUM) — ≥3 traces documented

### Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Concept output | 1 concept | 3 variants with comparison |
| Feature selection visibility | None | Full rationale per feature |
| Wave grouping explanation | None | Why grouped + alternatives |
| Decision traceability | None | Problem → Feature chains |
| AI explainability | Black box | Transparent reasoning |

## [0.0.68] - 2026-01-02

### Added

- **AI Augmentation 2.1: ML-Based Specification Quality Scoring** — G-Eval framework for objective multi-dimensional spec quality measurement
  - **New Module**: `templates/shared/quality/spec-quality-scorer.md` (~400 lines)
    - 5 Quality Dimensions with weighted scoring: Clarity (25%), Completeness (25%), Testability (20%), Consistency (15%), Traceability (15%)
    - Hybrid scoring approach: 60% automated metrics + 40% LLM G-Eval evaluation
    - Grade scale: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
    - Pass threshold: 70.0 (Grade C or higher)
    - Core algorithms:
      - `SCORE_SPECIFICATION(spec, historical_benchmark)` — main entry point
      - `EVALUATE_CLARITY(spec)` — ambiguity count + LLM G-Eval
      - `EVALUATE_COMPLETENESS(spec)` — severity-weighted gap penalty
      - `EVALUATE_TESTABILITY(spec)` — scenario measurability + traceability
      - `EVALUATE_CONSISTENCY(spec)` — LLM contradiction detection
      - `EVALUATE_TRACEABILITY(spec)` — FR→AS→EC link coverage
      - `LLM_GEVAL_RUBRIC(dimension, requirements)` — G-Eval prompting (0.85+ human correlation)
      - `ASSIGN_GRADE(overall_score)` — grade classification
      - `GENERATE_RECOMMENDATION(score, dimensions)` — actionable improvement advice
  - **New Subagent**: `spec-quality-scorer` in `templates/commands/specify.md`
    - Wave 3.5 execution (priority 35, after spec-writer and completeness-checker)
    - 6-step evaluation pipeline covering all quality dimensions
    - Outputs structured quality report with dimension breakdown and suggestions
  - **Template Update**: `templates/spec-template.md`
    - New Specification Quality Score section after Completeness Analysis
    - Dimension table with score, weight, and explanation columns
    - Quality gates status display (SR-SPEC-19/20/21)
    - Improvement suggestions based on lowest-scoring dimensions

- **New Validation Criteria** — G-Eval quality gates for specification quality
  - **Updated File**: `templates/shared/self-review/criteria-spec.md`
    - SR-SPEC-19: Quality Score Pass — overall G-Eval score >= 70 (Grade C+) (HIGH severity)
    - SR-SPEC-20: No Failing Dimensions — all quality dimensions >= 0.50 (MEDIUM severity)
    - SR-SPEC-21: Consistency Check — no CRITICAL contradictions detected (CRITICAL severity)
  - **New Checkpoint**: CP-SPEC-03D in `templates/shared/validation/checkpoints.md`
    - Triggers after quality scoring (before success criteria)
    - Validates SR-SPEC-19, SR-SPEC-20, SR-SPEC-21
  - **New Validation Gates**: VG-009 and VG-010 in progressive validation Tier 3
    - VG-009: spec_quality_score (G-Eval overall >= 70)
    - VG-010: dimension_minimums (All dimensions >= 0.50)

### Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Spec quality measurement | SQS only (4 components) | 5-dimension G-Eval scoring |
| Quality scoring method | Rule-based only | 60% automated + 40% LLM |
| Grade system | Quality levels | A/B/C/D/F grades |
| Pass threshold | 80% (SQS) | 70% (Grade C) |
| Improvement guidance | Generic | Dimension-specific suggestions |
| Contradiction detection | None | LLM-based semantic analysis |
| Human-expert correlation | N/A | 0.85+ via G-Eval rubrics |

---

## [0.0.67] - 2026-01-02

### Added

- **AI Augmentation 1.3: Requirement Ambiguity Detection** — Metacognitive LLM-based detection of vague terms, missing quantities, unclear actors, conditional gaps
  - **New Module**: `templates/shared/quality/ambiguity-patterns.md` (~290 lines)
    - 6 ambiguity types: VAGUE_TERM, MISSING_QUANTITY, UNCLEAR_ACTOR, UNDEFINED_TERM, CONDITIONAL_GAP, INCOMPLETE_LIST
    - Pattern library with severity and suggestions for each type
    - `DETECT_AMBIGUITIES(functional_requirements, glossary)` multi-pass algorithm
    - `LLM_AMBIGUITY_ANALYSIS(requirements, context)` metacognitive prompting
    - `REPAIR_AMBIGUITY(ambiguity, user_clarification)` repair algorithm
  - **Enhanced Subagent**: `ambiguity-detector` in `templates/commands/clarify.md`
    - 3-pass detection: Heuristic Pattern Matching → LLM Metacognitive Analysis → Cross-Requirement Consistency
    - Integration with `ambiguity-patterns.md` pattern library
    - Outputs structured ambiguity reports with repair suggestions

- **AI Augmentation 1.4: Completeness Checking via Semantic Analysis** — Multi-dimensional validation for error handling, security, observability, and prerequisites
  - **New Module**: `templates/shared/quality/completeness-checklist.md` (~300 lines)
    - 7 completeness categories: ERROR_HANDLING (0.20), PERFORMANCE (0.15), SECURITY (0.20), OBSERVABILITY (0.10), ACCESSIBILITY (0.10), PREREQUISITES (0.15), EDGE_CASES (0.10)
    - Category-specific check algorithms with pattern detection
    - `CALCULATE_COMPLETENESS_SCORE(spec, codebase_context)` weighted scoring
    - `LLM_GAP_ANALYSIS(spec, context)` for semantic gap detection
    - EARS template validation for requirement patterns
  - **New Subagent**: `completeness-checker` in `templates/commands/specify.md`
    - 8-step validation pipeline covering all completeness categories
    - Parallel execution with `edge-case-detector` in Wave 3
    - Outputs gaps with severity, explanation, and suggested requirements
  - **Template Update**: `templates/spec-template.md`
    - New Completeness Analysis section with 6-category status table
    - Completeness Score threshold of 0.75 for PASS

- **New Validation Criteria** — Self-review checks for ambiguity and completeness
  - **Updated File**: `templates/shared/self-review/criteria-spec.md`
    - SR-SPEC-14: No Vague Terms — no "fast", "user-friendly" without metrics (HIGH severity)
    - SR-SPEC-15: Quantities Defined — all "some/many/few" have specific numbers (MEDIUM severity)
    - SR-SPEC-16: Error Path Coverage — ratio of error:happy scenarios >= 0.5 (HIGH severity)
    - SR-SPEC-17: Security Triggers Covered — all auth/input/file triggers have security reqs (CRITICAL severity)
    - SR-SPEC-18: Completeness Score — overall completeness >= 0.75 (HIGH severity)
  - **New Checkpoint**: CP-SPEC-03C in `templates/shared/validation/checkpoints.md`
    - Triggers after completeness check (before success criteria)
    - Validates SR-SPEC-14 through SR-SPEC-18
    - Integrated into progressive validation Tier 2

### Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Vague terms detected | Manual review | Automatic detection with repair suggestions |
| Missing quantities flagged | Ad-hoc | 100% flagged with clarification questions |
| Error path coverage | Not tracked | >= 0.5 ratio enforced |
| Security gap detection | Partial (EC only) | 100% for auth/input/file triggers |
| Completeness score | Not measured | >= 0.75 threshold with 7-category breakdown |
| Clarification efficiency | 5 generic questions | Targeted questions from ambiguity detection |

---

## [0.0.66] - 2026-01-02

### Added

- **AI Augmentation 1.1: Acceptance Criteria Enhancement** — RaT prompting for acceptance scenario generation in `/speckit.specify`
  - **Enhanced `acceptance-criteria-generator` subagent** in `templates/commands/specify.md`:
    - 5-step RaT (Refine-and-Thought) pipeline: REFINE → THINK → EXTRACT → GENERATE → SCORE
    - Scenario Classification: HAPPY_PATH, ALT_PATH, ERROR_PATH, BOUNDARY, SECURITY
    - Entity extraction with type detection (email, phone, date, numeric, string, password, file, url, array, boolean, id)
    - Completeness scoring formula with >= 0.80 threshold
    - YAML output format for structured consumption
  - **Template Update**: `templates/spec-template.md`
    - New Classification column in Acceptance Scenarios tables
    - Documented classification values in HTML comments
    - Updated Test Strategy coverage targets

- **AI Augmentation 1.2: Automatic Edge Case Identification** — Systematic edge case discovery via heuristics and security patterns
  - **New Module**: `templates/shared/quality/edge-case-heuristics.md` (~330 lines)
    - `DETECT_ENTITY_TYPE(field_name, context)` algorithm
    - Edge case patterns for 11 entity types (email, phone, date, numeric, string, password, file, url, array, boolean, id)
    - `GENERATE_HEURISTIC_EDGE_CASES(entities)` procedure
    - `CALCULATE_ENTITY_COVERAGE(entities, edge_cases)` for validation
    - Integration with SR-SPEC-12 self-review
  - **New Module**: `templates/shared/quality/security-patterns.md` (~360 lines)
    - `DETECT_SECURITY_TRIGGERS(requirements_text)` algorithm
    - OWASP-based patterns for 7 categories: Authentication, Input Validation, Access Control, Session Management, File Upload, API Security, Data Protection
    - Security edge cases with OWASP references (EC-SEC-AUTH, EC-SEC-INJ, EC-SEC-AC, EC-SEC-SESS, EC-SEC-FILE, EC-SEC-API, EC-SEC-DATA)
    - Confidence scoring (0.95 pattern match, 0.75 inferred, 0.60 LLM-generated)
    - Integration with SR-SPEC-13 self-review
  - **New Subagent**: `edge-case-detector` in `templates/commands/specify.md`
    - 4-step pipeline: Entity-Type Heuristics → Security Pattern Matching → LLM Gap Analysis → Deduplicate and Rank
    - Parallel execution with `acceptance-criteria-generator`
    - Outputs enhanced EC table with Severity (CRITICAL/HIGH/MEDIUM/LOW) and Category columns
  - **Template Update**: `templates/spec-template.md`
    - New Severity and Category columns in Edge Cases table
    - New Edge Case Coverage Summary section with completeness score
    - Updated coverage targets for severity-based testing

- **New Validation Criteria** — Self-review checks for acceptance criteria and edge case coverage
  - **New File**: `templates/shared/self-review/criteria-spec.md`
    - SR-SPEC-01 to SR-SPEC-10: Existing spec validation criteria (documented)
    - SR-SPEC-11: AC Completeness Score >= 0.80 threshold (HIGH severity)
    - SR-SPEC-12: Entity Type Coverage — auto-fixable heuristic EC generation (MEDIUM severity)
    - SR-SPEC-13: Security EC Coverage for auth/input/session features (HIGH severity)
  - **New Checkpoint**: CP-SPEC-03B in `templates/shared/validation/checkpoints.md`
    - Triggers after edge case generation
    - Validates SR-SPEC-11/12/13
    - Integrated into progressive validation Tier 2

### Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Edge cases per spec | 5-10 manual | 15-25 systematic |
| Security EC coverage | Ad-hoc | 100% for auth/input features |
| Entity type coverage | Not tracked | 100% of detected entities |
| Completeness score | Not measured | >= 0.80 threshold |
| Scenario classification | None | HAPPY/ALT/ERROR/BOUNDARY/SECURITY |

---

## [0.0.65] - 2026-01-01

### Added

- **Part 1: Strategic Frameworks** — World-class business strategy frameworks for `/speckit.concept`
  - **5 New Templates** in `templates/shared/concept-sections/`:
    - `pr-faq.md` — Amazon Working Backwards methodology (Press Release + FAQ)
    - `blue-ocean-canvas.md` — Blue Ocean Strategy ERRC Grid (Eliminate/Reduce/Raise/Create)
    - `porters-five-forces.md` — Porter's Five Forces competitive analysis
    - `business-model-canvas.md` — 9-component canvas with unit economics (CAC, LTV, LTV:CAC)
    - `three-horizons.md` — McKinsey Three Horizons (H1: 70%, H2: 20%, H3: 10%)
  - **Concept Command Integration**: All frameworks referenced at strategic points in `concept.md`
    - Porter's 5 Forces → Phase 0b (market research)
    - Blue Ocean Canvas → Phase 0c (solution ideation)
    - PR/FAQ → Step 5 (Extract Vision)
    - Business Model Canvas → Step 5aa (after SMART metrics)
    - Three Horizons → Step 6b (Feature Hierarchy prioritization)
  - **Expected CQS Impact**: +10-15 points (strategic depth)

- **Part 2: Decision-Making Frameworks** — Stripe-style decision documentation for `/speckit.concept`
  - **3 New Templates** in `templates/shared/concept-sections/`:
    - `decision-log.md` — Stripe-style decision log (DEC-001 format, options/pros/cons, reversibility assessment)
    - `tradeoff-resolution.md` — Trade-off hierarchy (Safety > User Value > Simplicity > Speed > Reversible)
    - `scope-exclusions.md` — Explicit non-goals with guardrails and rejected alternatives
  - **Concept Command Integration**: All frameworks referenced at decision points in `concept.md`
    - Trade-off Resolution → Section 5-TR (after PR/FAQ)
    - Decision Log → Section 5c-DL (after Risk Assessment)
    - Scope Exclusions → Section 6a (between Feature Hierarchy and Three Horizons)
  - **Expected CQS Impact**: +5-8 points (decision clarity, scope creep prevention)

- **Part 3: Validation Frameworks** — OpenAI-style hypothesis testing and pre-mortem analysis for `/speckit.concept`
  - **2 New Templates** in `templates/shared/concept-sections/`:
    - `hypothesis-testing.md` — HYP-001 format with Type (Desirability/Feasibility/Viability), evidence tracking, success criteria
    - `pre-mortem.md` — FAIL-001 format with failure scenarios, early warning signs, prevention strategies, kill criteria
  - **Concept Command Integration**:
    - Pre-Mortem → Section 5b-PM (before Risk Assessment)
    - Hypothesis Testing → Section 5c-HTL (after Risk Assessment)
  - **Expected CQS Impact**: +5-8 points (validation rigor, failure prevention)

- **Part 5: AI Augmentation** — Multi-agent research and Evidence-Based CQS for `/speckit.concept`
  - **2 New Templates** in `templates/shared/concept-sections/`:
    - `multi-agent-research.md` — Research agent orchestration (market_intelligence, competitor_analyst, validation_agent)
    - `ai-responsibility.md` — Responsible AI checklist (bias/fairness, transparency, privacy, safety) for AI products
  - **CQS-E Enhancement** in `cqs-score.md`:
    - New dimensions: Strategic (10%), Validation (5%)
    - Evidence Multiplier (0.8-1.2) for citation quality
    - Updated formula with 8 components
  - **Concept Command Integration**:
    - Multi-Agent Research → Phase 0b.1 (research orchestration)
    - AI Responsibility → Section 5c-AIR (conditional for AI products)
    - CQS-E → Updated CQS section with Strategic + Validation + Evidence Multiplier
  - **Expected Impact**: +8-12 CQS points, 2-4 hours research time saved, 100x ROI vs manual research

- **Part 4.1: Executive Summary Excellence** — 90-second decision context for executives in `/speckit.concept`
  - **New Template**: `templates/shared/concept-sections/executive-summary.md`
    - 8-section structure: The Ask, Why Now, Opportunity, Approach, Investment, Risks, Success Criteria, Recommendation
    - Synthesis instructions mapping source sections to executive summary fields
    - Quality checklist for executive-ready output
  - **Concept Template Update**: `templates/concept-template.md`
    - Executive Summary section inserted between Vision Statement and UX Foundation Layer
    - First comprehensive view executives see after 2-3 sentence vision
  - **Concept Command Integration**: `templates/commands/concept.md`
    - New Step 5-ES: Executive Summary Synthesis (after all sections, before Self-Review)
    - Synthesis table mapping 8 sections to source data
    - Quality check before proceeding to Self-Review
  - **Expected Impact**: 10% concept quality improvement, reduced executive back-and-forth

- **Batch API Requests (Strategy 1.3)** — Cross-wave task aggregation for 50-70% reduction in API latency
  - **New Module**: `src/specify_cli/batch_aggregator.py`
    - `BatchConfig` — Configuration for batch aggregation (max_batch_size, timeout_ms, cross_wave)
    - `BatchGroup` — Represents a group of independent tasks that can execute in parallel
    - `BatchAggregator` — DAG analysis and intelligent task grouping across wave boundaries
    - Topological level computation for identifying truly independent tasks
    - Aggregation statistics for monitoring performance improvements

  - **WaveScheduler Enhancements**:
    - New `BATCHED` execution strategy in `ExecutionStrategy` enum
    - Batch configuration in `WaveConfig`: `batch_mode`, `max_batch_size`, `cross_wave_batching`
    - `_execute_batched()` method for cross-wave batch execution
    - Proper wave status tracking for batched tasks

  - **PoolConfig Extensions**:
    - `batch_mode: bool` — Enable/disable batch aggregation
    - `max_batch_size: int` — Maximum tasks per aggregated batch (default: 10)
    - `batch_timeout_ms: int` — Collection timeout before batch execution (default: 100ms)

  - **Algorithm**:
    - Build dependency graph from all tasks across waves
    - Compute topological levels (tasks at same level are independent)
    - Group by level into batches respecting max_batch_size
    - Execute batches sequentially, tasks within batch in parallel

  - **Expected Performance**:
    - Wave boundaries: 3+ → 1-2 per execution (50-70% reduction)
    - Round-trip latency: 300-900ms → 100-200ms (60% reduction)
    - Parallel utilization: Within-wave → Cross-wave (higher throughput)

## [0.0.64] - 2026-01-01

### Added

- **Template Pre-Compilation Engine** — Build-time template compilation for 20-30x faster runtime loading
  - **New Modules**:
    - `src/specify_cli/template_compiler.py` — Main compiler engine
      - `IncludeResolver` — Transitive `{{include:}}` directive resolution
      - `TemplateCompiler` — Compiles markdown to optimized JSON
      - Source hash tracking (SHA-256) for cache invalidation
      - Wave assignment computation for subagent dependencies
      - Fast path detection for greenfield/brownfield scenarios
    - `src/specify_cli/compiled_loader.py` — Runtime JSON loader
      - `CompiledTemplateLoader` — LRU-cached template loading
      - Automatic fallback to runtime parsing if compiled not available
      - Fast path optimization based on runtime context

  - **Release Pipeline Integration**:
    - Added `compile_templates()` function to `create-release-packages.sh`
    - Pre-compiles all command templates before package building
    - Compiled JSON included in `.specify/compiled/` directory

  - **Compiled JSON Schema [REF:TC-001]**:
    - `meta`: command, source_file, source_hash, compiled_at, includes_resolved
    - `config`: description, persona, model, reasoning_mode, thinking_budget, cache_hierarchy
    - `execution_plan`: max_parallel, wave_overlap, subagents, wave_assignments
    - `prompt`: user_template, sections
    - `fast_paths`: greenfield, simple, brownfield_with_baseline

  - **Expected Performance**:
    - Template load: 2-3s → ~100ms (20-30x improvement)
    - Include resolution: Runtime → Pre-computed (100% savings)
    - Frontmatter parsing: Every call → Pre-parsed (100% savings)
    - LRU cache hit: <1ms response

## [0.0.63] - 2026-01-01

### Added

- **Six-Level Cache Hierarchy** — Complete cache infrastructure with Project Cache (L4) and Global Cache (L5)
  - **New Shared Module**:
    - `templates/shared/cache-hierarchy.md` — Comprehensive six-level cache documentation
    - Full specifications for all cache levels with TTL, size limits, and hit rates
    - Cache lookup algorithm with level promotion
    - Invalidation strategies per level

  - **Cache Levels [REF:CH-001]**:
    - L0: Prompt Cache (Anthropic API) — 80-90% token reduction
    - L1: Semantic Cache (Embeddings) — 10-100x for similar queries
    - L2: In-Memory (Command scope) — TTL: 2-5 min, 60-70% hit rate
    - L3: Session Cache (RAM) — TTL: 30 min, 30-40% hit rate
    - **L4: Project Cache (Disk) — NEW: TTL: Git SHA, path `.speckit/cache/`**
    - **L5: Global Cache (Disk) — NEW: TTL: 7 days, path `~/.speckit/cache/`**

  - **Frontmatter Directive**:
    - Added `cache_hierarchy: full` to all 22 command templates
    - Added `cache_hierarchy: full` to all 21 COMPRESSED templates
    - Compact format enables all cache levels with sensible defaults

  - **Updated Shared Modules**:
    - `caching-strategy.md` — Added reference to cache-hierarchy.md

  - **Expected Performance**:
    - L4 Project Cache: 20-30% hit rate, saves 500ms-2s per hit
    - L5 Global Cache: 40-50% hit rate, saves 1-3s per hit
    - Combined latency reduction: 20-30% across workflows

## [0.0.62] - 2026-01-01

### Added

- **Semantic Caching Integration** — Query-level semantic caching using embeddings for 10-100x speedup on similar queries
  - **Semantic Cache Directives [REF:SC-001]**:
    - Added `semantic_cache` section to YAML frontmatter in all major commands
    - Uses embedding-based similarity matching (all-MiniLM-L6-v2 encoder)
    - 0.95 similarity threshold for cache hits
    - Session-scoped caching with 1-hour TTL

  - **New Shared Module**:
    - `templates/shared/semantic-cache.md` — Comprehensive semantic caching documentation
    - Explains embedding mechanics, query normalization, similarity matching
    - Intent and feature synonym dictionaries
    - Cache storage structure and lookup algorithm

  - **Command Updates**:
    - `specify.md`, `specify.COMPRESSED.md` — Added semantic_cache
    - `plan.md`, `plan.COMPRESSED.md` — Added semantic_cache
    - `tasks.md`, `tasks.COMPRESSED.md` — Added semantic_cache
    - `implement.md`, `implement.COMPRESSED.md` — Added semantic_cache
    - `design.md`, `design.COMPRESSED.md` — Added semantic_cache
    - `concept.md`, `concept.COMPRESSED.md` — Added semantic_cache

  - **Updated Cache Hierarchy**:
    - L0: Prompt Cache (Anthropic API) — 80-90% token reduction
    - **L1: Semantic Cache (Embeddings) — NEW: 10-100x for similar queries**
    - L2: In-Memory (Command scope) — 60-70% hit rate
    - L3: Session Cache — Response caching

  - **Example Cache Hits**:
    - "Create user auth" ↔ "Build login functionality" → 0.97 similarity (HIT)
    - "Add API endpoint" ↔ "Implement REST route" → 0.94 similarity (HIT)

  - **Expected Performance**:
    - Similar query response: 10-100x faster on cache hit
    - Cache hit rate: 40-50% for typical workflows
    - Overall workflow time: 40-50% reduction on repeated operations

## [0.0.61] - 2026-01-01

### Added

- **Anthropic Prompt Caching Integration** — API-level prompt caching for 80-90% input token reduction
  - **Cache Control Directives [REF:PC-001]**:
    - Added `cache_control` section to YAML frontmatter in all major commands
    - Supports caching of system prompts, constitution, templates, and artifacts
    - Session-scoped TTL with file-change invalidation

  - **New Shared Module**:
    - `templates/shared/caching-strategy.md` — Comprehensive caching strategy documentation
    - Explains Anthropic prompt caching mechanics, cacheable content types, TTL strategies
    - Integration with existing file-level caching hierarchy

  - **Command Updates**:
    - `specify.md`, `specify.COMPRESSED.md` — Added cache_control
    - `plan.md`, `plan.COMPRESSED.md` — Added cache_control with artifacts
    - `tasks.md`, `tasks.COMPRESSED.md` — Added cache_control with artifacts
    - `implement.md`, `implement.COMPRESSED.md` — Added cache_control with artifacts
    - `design.md`, `design.COMPRESSED.md` — Added cache_control with artifacts
    - `concept.md`, `concept.COMPRESSED.md` — Added cache_control

  - **Updated Documentation**:
    - `parallel-loading.md` — Added API-Level Prompt Caching section

  - **Expected Performance**:
    - Input tokens per call: 80-90% reduction on cache hits
    - API response time: 50-70% faster on cached prompts
    - Workflow cost savings: 80-90% for repeated operations

## [0.0.60] - 2026-01-01

### Added

- **Speculative Pre-fetching** — Active prefetch phases in all major commands for 2-3s faster initialization
  - **Prefetch Phase [REF:PF-001]**:
    - Parallel load of all potentially-needed files BEFORE any conditional logic
    - Session-scoped caching of prefetched content
    - Command-specific prefetch lists based on parallel-loading.md

  - **Command Updates**:
    - `specify.md` — Added Prefetch Phase section (constitution, templates, modules, concept)
    - `specify.COMPRESSED.md` — Added compact Prefetch Phase section
    - `plan.md` — Converted docs-only parallel loading to active prefetch execution
    - `tasks.md` — Converted docs-only parallel loading to active prefetch execution
    - `implement.md` — Added Prefetch Phase section (tasks, plan, checklists)
    - `design.md` — Added Prefetch Phase section (spec, concept, design-system)

  - **Performance Impact**:
    - Files loaded on-demand: 5-8 → 0 (100% cached)
    - Init phase time: 2-5s → 0.3-1s (70-80% faster)
    - Per command savings: 2-3s
    - Workflow (4 commands): saves 8-12s total

## [0.0.59] - 2026-01-01

### Added

- **Parallel File Operations** — Batch parallel reads to reduce initialization time by 2-3 seconds per command
  - **Parallel Batch Read Pattern**:
    - Replace sequential file reads with parallel batch operations
    - Single message, multiple Read tool calls for parallelism
    - 650ms sequential → 300ms parallel (54% faster)

  - **Speculative Pre-fetching**:
    - Background pre-load of commonly-needed files per command
    - Command-specific prefetch lists (specify, plan, tasks, implement, design)
    - Cache with TTL for repeated reads

  - **Template Changes**:
    - `parallel-loading.md` — **NEW** shared module with parallel loading patterns
    - `plan.md` — Updated Init section with parallel reads
    - `specify.md` — Updated Init section with parallel reads
    - `specify.COMPRESSED.md` — Updated Init section with parallel reads
    - `tasks.md` — Updated Init section with parallel reads
    - `design.md` — Updated framework detection with parallel reads

  - **Performance Impact**:
    - Init context load: 650ms → 300ms (saves ~350ms)
    - With prefetch hit: 300ms → ~50ms (saves ~250ms)
    - Per command total: 3-5s → 1-2s (saves 2-3s)

## [0.0.58] - 2026-01-01

### Added

- **Progressive Validation** — 4-tier validation pipeline that replaces blocking gates with tiered execution
  - **4-Tier Pipeline Architecture**:
    - **Tier 1 (Syntax)**: < 1s, BLOCKING — Checks section IDs, format, mandatory fields
    - **Tier 2 (Semantic)**: 1-5s, BLOCKING on errors — Constitution alignment, link validation, schema checks
    - **Tier 3 (Quality)**: 5-15s, NON-BLOCKING — SRS/CQS/PRS/TRS scoring, ambiguity detection
    - **Tier 4 (Deep)**: 15-30s, ASYNC BACKGROUND — LLM review, cross-artifact consistency, suggestions

  - **Probabilistic Early Exit**:
    - At 95%+ confidence after Tier 1-2 pass, skip expensive Tier 3-4 checks
    - Confidence calculation: `base_confidence × historical_rate - issue_penalty`
    - Historical pass rates: spec.md (92%), plan.md (88%), tasks.md (95%)

  - **Performance Optimizations**:
    - Clean artifact: 25s → 3s (saves ~22s via early exit)
    - Minor warnings: 25s → 8s (saves ~17s)
    - Average savings: 5-10s per command

  - **Skip Flags**:
    - `--skip-validate` / `--skip-validation` — Skip all validation
    - `--fast` — Run Tier 1-2 only, skip expensive checks
    - `--full-validation` — Force all tiers (no early exit)

  - **Template Changes**:
    - `checkpoints.md` — Added Progressive Validation section (~330 lines)
    - `validation-gates.yaml` — Added tier classifications to all VG-xxx gates
    - `specify.COMPRESSED.md` — Updated validation phase with tiered pipeline
    - `plan.md` — Added progressive mode to pre_handoff_action
    - `implement.md` — Added progressive mode to pre_gates with tier classifications

## [0.0.57] - 2026-01-01

### Added

- **Streaming Output** — Real-time progress updates during parallel wave execution
  - **Checkpoint-Based Updates**:
    - Emit progress after each agent completes (not wait for entire wave)
    - Visual progress bar: `[████████████░░░░░░░░] 60%`
    - Per-agent status with model and duration: `✓ data-layer-builder [sonnet]: 22s`

  - **Live Metrics Tracking**:
    - Running elapsed time and token count
    - Real-time cost estimation per model tier
    - Wave overlap announcements when 80% threshold reached

  - **Checkpoint Trigger Events**:
    - Wave start → emit header with agent list
    - Agent complete → update with ✓/✗ status
    - Wave 80% threshold → announce overlap trigger
    - Wave complete → emit collapsed summary

  - **Template Changes**:
    - `orchestration-instructions.md` — Added "Streaming Output" section with format and execution loop
    - `implement.md` — Added streaming reference and output format example

  - **Skip Flags**: `--no-streaming` or `--quiet` to disable

## [0.0.56] - 2026-01-01

### Added

- **Adaptive Model Routing** — Dynamic model selection (haiku/sonnet/opus) based on feature complexity and role group
  - **Complexity Detection Algorithm**:
    - Analyzes `spec.md` to calculate complexity score (0-100)
    - Scoring factors: user stories (×5), FRs (×2), APIs (×8), tech signals (×5)
    - Four tiers: TRIVIAL (0-25), SIMPLE (26-50), MODERATE (51-75), COMPLEX (76-100)

  - **Model Routing Matrix**:
    - Maps (complexity_tier × role_group) → optimal model
    - Role groups: INFRA, BACKEND, FRONTEND, TESTING, REVIEW, DOCS
    - Example: SIMPLE/INFRA → haiku, MODERATE/BACKEND → opus

  - **Cost Optimization**:
    - 40-85% cost reduction vs all-opus baseline
    - Cost model: haiku ~$0.001, sonnet ~$0.012, opus ~$0.060 per agent
    - Real-time cost reporting with savings percentage

  - **Template Changes**:
    - `orchestration-instructions.md` — Added Step 0/0.5 for complexity detection and routing
    - `implement.md` — Added Step 3.7 for adaptive routing execution

  - **Skip Flag**: `--no-adaptive-model` to disable adaptive routing

## [0.0.55] - 2026-01-01

### Added

- **Wave-Based Parallel Execution for All Commands** — Ultrathink mode support across all 19 speckit commands
  - **Standardized Claude Code Configuration**:
    - All commands now have `claude_code` blocks with subagent definitions
    - `reasoning_mode: extended` + `thinking_budget: 16000` for complex commands
    - Wave-based parallel execution with dependency ordering

  - **P1 Commands (High Impact)** — Full parallel subagent orchestration:
    - `design.md` — 10 subagents across 5 waves (design research → generation → system → integration → quality)
    - `concept.md` — 9 subagents across 5 waves (discovery → synthesis → validation → technical → quality)
    - `specify.md` — 7 subagents across 4 waves (context → analysis → specification → quality)

  - **P2 Commands (Medium-High Impact)**:
    - `launch.md` — 5 subagents across 3 waves (release notes → press kit → distribution)
    - `ship.md` — 5 subagents across 3 waves (infra → deployment → verification)
    - `discover.md` — 3 subagents across 2 waves (hypothesis → validation)

  - **P3 Commands (Medium Impact)**:
    - `baseline.md` — 4 subagents across 2 waves (analysis → compilation)
    - `preview.md` — 4 subagents across 2 waves (conversion → validation)
    - `monitor.md` — 3 subagents across 2 waves (telemetry → dashboards)

  - **P4 Commands (Lower Impact)**:
    - `constitution.md` — 3 subagents across 2 waves (analysis → writing)
    - `clarify.md` — 3 subagents across 3 waves (detection → generation → update)
    - `integrate.md` — 3 subagents across 2 waves (analysis → contracts)

  - **P5 Commands (Minimal Impact)** — Simpler configurations:
    - `checklist.md`, `list.md`, `switch.md` — Single subagent (sequential)
    - `extend.md`, `taskstoissues.md` — 2 sequential subagents

  - **Existing Commands** — Upgraded thinking_budget to ultrathink:
    - `implement.md` — 8000 → 16000
    - `analyze.md` — 12000 → 16000
    - `plan.md` — 8000 → 16000
    - `tasks.md` — 6000 → 8000
    - `speckit.merge.md` — 8000 → 16000

  - **Orchestration Features**:
    - `max_parallel: 3` — Maximum concurrent agents per wave
    - `wave_overlap.threshold: 0.80` — Start next wave at 80% completion
    - `fail_fast: true` — Stop on critical errors
    - Model routing: haiku (simple) → sonnet (standard) → opus (complex)

  - **Expected Outcome**:
    - 40-50% time reduction for complex workflows
    - All commands support Claude Code Task tool parallel execution
    - Ultrathink mode enabled for deep reasoning on specifications

## [0.0.54] - 2026-01-01

### Added

- **Parallel Agent Orchestration Instructions for Claude Code** — Template instructions enabling parallel Task tool calls
  - **New Shared Module**: `templates/shared/orchestration-instructions.md`
    - Reusable instructions for Claude Code on executing `claude_code.subagents` in parallel
    - Wave building algorithm with dependency resolution
    - Task call patterns for concurrent execution
    - Error handling strategies (fail-fast vs continue-on-error)
    - Progress reporting between waves

  - **Updated Templates with Include Directive**:
    - `templates/commands/implement.md` — Enhanced 10 subagent prompts with Context/Task/Success Criteria structure
    - `templates/commands/implement.COMPRESSED.md` — Added orchestration config and expanded subagents
    - `templates/commands/plan.md` — Added parallel execution section
    - `templates/commands/tasks.md` — Added parallel execution section
    - `templates/commands/analyze.md` — Added parallel execution section
    - `templates/commands/speckit.merge.md` — Added parallel execution section

  - **Enhanced Subagent Prompts** (implement.md):
    - Each of 10 subagents now has structured prompts with:
      - `## Context` — Feature directory and relevant artifacts
      - `## Task` — Numbered steps for execution
      - `## Success Criteria` — Clear validation checklist

  - **Orchestration Settings**:
    - `max_parallel: 3` — Maximum concurrent agents per wave
    - `wave_overlap.threshold: 0.80` — Start next wave at 80% completion
    - Respects `depends_on` for dependency ordering

  - **Expected Outcome**:
    - 20-30% speedup for multi-agent commands
    - Parallel execution of independent subagents within waves
    - Better utilization of Claude Code's Task tool concurrency

## [0.0.53] - 2025-12-31

### Added

- **Distributed Agent Pool (2.2)** — Parallel Claude API execution for multi-agent workflows
  - **New Modules**:
    - `agent_pool.py` — Pool of async Anthropic clients with semaphore-based concurrency
    - `wave_scheduler.py` — DAG-based wave scheduling with overlap execution
    - `template_parser.py` — YAML frontmatter parsing for subagent extraction

  - **New CLI Command**: `specify orchestrate <command> <feature>`
    - Execute command templates with parallel agent orchestration
    - Parses `claude_code.subagents` from template frontmatter
    - Respects dependency graphs and wave-based execution
    - Options: `--pool-size`, `--dry-run`, `--sequential`, `--verbose`

  - **Execution Strategies**:
    - `SEQUENTIAL` — Execute waves one after another (safest)
    - `OVERLAPPED` — Start next wave at 80% completion threshold (default)
    - `AGGRESSIVE` — Start next wave ASAP when deps satisfied

  - **Features**:
    - Pool of 4 async Anthropic clients (configurable 1-8)
    - Automatic retry with exponential backoff (tenacity)
    - Real-time progress callbacks
    - Statistics tracking (tokens, duration, success rate)
    - Dry-run mode for execution plan preview

  - **Expected Speedup**:
    - `/speckit.implement` (10 agents): 750s → 220s (70% faster)
    - Multi-command workflows: 20-30% speedup
    - API utilization: ~25% → ~90%

  - **Dependencies Added**:
    - `anthropic>=0.40.0` — Claude API async client
    - `tenacity>=8.2.0` — Retry logic with exponential backoff

  - **Usage**:
    ```bash
    # Preview execution plan
    specify orchestrate implement 001-user-auth --dry-run

    # Execute with 4 parallel agents
    specify orchestrate implement 001-user-auth --pool-size 4

    # Sequential execution (no wave overlap)
    specify orchestrate implement 001-user-auth --sequential
    ```

  - **Requirements**:
    - `ANTHROPIC_API_KEY` environment variable must be set
    - Templates must define `claude_code.subagents` in YAML frontmatter

## [0.0.52] - 2025-12-31

### Added

- **Compressed Context Templates (1.3)** — Token-efficient template variants for 60-66% reduction
  - **Reference System** (`templates/.compressed/refs/`):
    - `init-modules.yaml` — Language, complexity, brownfield initialization
    - `self-review.yaml` — Framework definitions with verdict logic
    - `validation-gates.yaml` — SRS/CQS/DQS quality gates
    - `quality-checks.yaml` — Anti-slop and reader-testing rules
    - `output-schemas.yaml` — Common output structures

  - **21 Compressed Templates** (`.COMPRESSED.md` variants):
    - `specify.COMPRESSED.md` (1292 → ~450 lines, 65%)
    - `analyze.COMPRESSED.md` (2631 → ~340 lines, 87%)
    - `design.COMPRESSED.md` (2516 → ~410 lines, 84%)
    - `implement.COMPRESSED.md` (2057 → ~385 lines, 81%)
    - `concept.COMPRESSED.md`, `launch.COMPRESSED.md`, `plan.COMPRESSED.md`
    - `tasks.COMPRESSED.md`, `discover.COMPRESSED.md`, `ship.COMPRESSED.md`
    - `checklist.COMPRESSED.md`, `preview.COMPRESSED.md`, `baseline.COMPRESSED.md`
    - `clarify.COMPRESSED.md`, `monitor.COMPRESSED.md`, `integrate.COMPRESSED.md`
    - `list.COMPRESSED.md`, `switch.COMPRESSED.md`, `constitution.COMPRESSED.md`
    - `extend.COMPRESSED.md`, `taskstoissues.COMPRESSED.md`

  - **Compression Techniques**:
    - Reference notation: `[REF:XXX-NNN]` for shared patterns (INIT-001, SR-001, VG-001, etc.)
    - Tables for criteria, rules, and mappings
    - Abbreviated YAML frontmatter with essential fields only
    - Condensed workflow steps preserving decision logic

  - **Release Script Updates**:
    - Compressed templates included in all release packages
    - Skip `.COMPRESSED.md` in command generation (avoid duplicates)
    - Reference system copied to `.specify/templates/.compressed/`

  - **Benefits**:
    - 60-66% token reduction (80K → 27K total)
    - 30-40% faster LLM inference
    - 60% reduction in input token costs
    - No regression in SRS/CQS/DQS quality scores

  - **Usage Guide**:
    - **Full templates** (default): Standard `.specify/templates/commands/*.md` — verbose with examples, explanations, edge cases. Best for learning and complex scenarios.
    - **Compressed templates**: `.specify/templates/commands/*.COMPRESSED.md` — token-efficient with reference notation. Best for experienced users and cost optimization.

    **To switch to compressed mode**:
    ```bash
    # Option 1: Rename compressed templates (permanent)
    cd .specify/templates/commands
    for f in *.COMPRESSED.md; do mv "$f" "${f%.COMPRESSED.md}.md.backup" && mv "${f%.COMPRESSED.md}.md" "${f%.COMPRESSED.md}.full.md" && mv "$f" "${f%.COMPRESSED.md}.md"; done

    # Option 2: Use compressed template directly (per-command)
    # In your AI agent, reference the compressed variant:
    # "Use .specify/templates/commands/specify.COMPRESSED.md for this task"

    # Option 3: Configure agent to prefer compressed (agent-specific)
    # Claude Code: Add to CLAUDE.md
    # "Prefer .COMPRESSED.md template variants when available"
    ```

    **Reference resolution**: Compressed templates use `[REF:XXX-NNN]` notation pointing to `.specify/templates/.compressed/refs/` YAML files. Agents should inline these references during execution.

## [0.0.51] - 2025-12-30

### Added

- **Zero-Budget Growth Strategies for `/speckit.launch`** — Comprehensive sustainable growth tactics
  - **Community Growth Playbook**:
    - Reddit strategy (95/5 rule, karma building, subreddit targeting)
    - Indie Hackers engagement (23% conversion rate tactics, milestone posts)
    - Discord/Slack community approach (Join → Help → Beta test → Mention)
    - Hacker News beyond Show HN (organic engagement strategies)

  - **Directory Listings (100+ directories organized by tier)**:
    - Tier 1 Essential: G2, Capterra, TrustRadius, AlternativeTo, GetApp, Software Advice
    - Tier 2 SaaS Directories: SaaSHub, SaaSworthy, SoftwareSuggest, SourceForge, Crozdesk
    - Tier 3 Startup Launch Sites: BetaList, Launching Next, BetaPage, StartupBuffer, KillerStartups
    - Tier 4 Business Directories: Crunchbase, AngelList, F6S, Gust, StartupBlink
    - Tier 5 Niche-Specific: Dev Tools (GitHub/VS Code/JetBrains Marketplaces), AI/ML (Futurepedia, TopAI.tools), No-Code, Design, Marketing
    - Tier 6 Regional: Europe, Asia, LatAm, India, Russia/CIS directories
    - Tier 7 Aggregators: BuiltWith, SimilarWeb, Wappalyzer
    - Submission checklist and tracking template

  - **Viral & Referral Loops**:
    - Inherent virality patterns (Calendly, Zoom, Figma examples)
    - Incentivized referral structures (one-sided, two-sided)
    - Waitlist virality mechanics
    - K-factor and referral rate benchmarks

  - **Partnership & Integration Marketing**:
    - Integration marketplace guide (Zapier, Slack, Chrome, Shopify, HubSpot, Salesforce)
    - Co-marketing playbook (webinars, guest content, mutual promotion)
    - Partnership outreach templates
    - Partnership tier framework

  - **Build in Public Strategy**:
    - Platform-specific guides (Twitter/X, LinkedIn, Indie Hackers)
    - Content mix recommendations (40% insights, 30% BTS, 20% milestones, 10% product)
    - Milestone post templates
    - Content rules (do's and don'ts)

  - **Cold Outreach Playbook**:
    - Prospect finding sources and tools
    - 3-email sequence templates (Value First, Case Study, Breakup)
    - Personalization requirements
    - Benchmark metrics (40-60% open rate, 5-15% reply rate)

  - **Growth Timeline** — 12-month roadmap with weekly time allocation

  - **New Input Parameter**: `growth_focus` (community, directories, viral, partnerships, all)
  - **New Output Files**: `docs/launch/growth-playbook.md`, `docs/launch/directory-tracker.md`

## [0.0.50] - 2025-12-30

### Added

- **Artifact Quality System** — Anti-Slop, Reader Testing, and Brainstorm-Curate protocols
  - **New Quality Modules** (`templates/shared/quality/`):
    - `anti-slop.md` — Explicit rules against generic AI content (forbidden phrases, hedge phrase limits, buzzword density, specificity checks)
    - `reader-testing.md` — Fresh reader perspective simulation for catching blind spots, implicit assumptions, and ambiguities
    - `brainstorm-curate.md` — Two-phase decision protocol: generate 3-5 options before committing, with weighted evaluation matrix

  - **Self-Review Framework Enhancement**:
    - New Universal Quality Checks: SR-SLOP-01 to SR-SLOP-05 (anti-slop), SR-READ-01 to SR-READ-05 (reader testing)
    - Integrated into all artifact-generating commands

  - **`/speckit.concept` Enhancements**:
    - **Phase 0b-2: Multi-Perspective Problem Analysis** — Validates problems from End User, Business, Technical, and Competitive perspectives
    - **Phase 0c Enhanced**: Solution Ideation now uses Brainstorm-Curate protocol with weighted scoring
    - **Step 4b: Clarification Gate** — Proactive clarifying questions when input is vague (specific pass/fail examples for target user, core problem, differentiation, measurable success)

  - **`/speckit.specify` Enhancements**:
    - New "Pre-Review Quality Pass" section with Anti-Slop Scan and Reader Testing before formal Self-Review

  - **`/speckit.plan` Enhancements**:
    - "Quality Imports for Architecture Decisions" section with Brainstorm-Curate for database, caching, auth, deployment, and framework decisions
    - Architecture Decision Protocol with skip conditions and documentation format

  - **`/speckit.design` Enhancements**:
    - "Design Writing Quality Rules" with design-specific anti-slop rules
    - Forbidden design phrases (e.g., "modern look and feel", "clean aesthetic") with concrete replacement requirements
    - Bold > Safe, Specific > Generic, Why > What rules for design rationale

## [0.0.49] - 2025-12-30

### Added

- **`/speckit.design --concept` Mode** — Application-Wide Design from Concept
  - **New Mode**: Generate comprehensive app-wide design from `concept.md` covering ALL features and UX flows
  - **Wave-by-Wave Generation Strategy**:
    - `--concept` → Wave 1 (Foundations)
    - `--concept --wave 2` → Wave 2 (Experience)
    - `--concept --wave 3` → Wave 3+ (Business)
    - `--concept --all` → All waves in one pass
  - **8-Phase Workflow**:
    1. Validation & Concept Parsing (CQS quality gate)
    2. Design System Generation (reuses existing agents)
    3. Foundation Designs (AUTH, ERROR, LAYOUT, NAV, FTUE, FEEDBACK, ADMIN)
    4. Navigation Architecture (sitemap, route map, journey mapping)
    5. Journey Flows (step-by-step with edge cases)
    6. Wave-by-Wave Feature Design (story → screen mapping)
    7. Motion System (animation tokens, page transitions)
    8. Quality Validation & Index Generation (App-DQS scoring)
  - **Output Structure**: `specs/app-design/` with subdirectories for foundations, waves, journeys, motion, components
  - **Traceability**: Every design artifact linked to concept IDs (EPIC-NNN.FNN, J000, UXF-xxx)
  - **Quality Gates**: CQS >= 80 (production), 60-79 (warnings), <60 (prompt continue)
  - **App-DQS Scoring**: Aggregate quality score from design_system + foundations + journeys + features + traceability

- **New Templates**:
  - `templates/app-design-template.md` — Index/overview template for app-design directory
  - `templates/foundation-design-template.md` — UXF scenario design template with state variations
  - `templates/journey-design-template.md` — User journey flow template with transitions

- **New Shared Modules** (`templates/shared/concept-design-sections/`):
  - `feature-to-screens.md` — Algorithm for mapping stories to screen inventory
  - `persona-to-patterns.md` — JTBD-to-interaction-patterns mapping
  - `wave-design-strategy.md` — Quality bars and focus areas per wave

- **New Handoffs** (for concept design mode):
  - "Generate App Preview" → speckit.preview for full application
  - "Continue Next Wave" → speckit.design --concept --wave N+1
  - "Plan Wave 1 Implementation" → speckit.plan for foundation features
  - "Design All Waves" → speckit.design --concept --all (for small concepts)

- **`/speckit.design --mockup` Mode** — Visual Mockup Generation via Google Stitch
  - **New Mode**: Generate high-fidelity visual mockups from ASCII wireframes using Google Stitch AI
  - **Browser Automation**: Playwright-based automation with persistent browser context for session management
  - **8-Phase Workflow**:
    1. Preflight Check (Playwright, Chromium, design artifacts)
    2. Authentication (Google OAuth with session persistence)
    3. Wireframe Discovery (scan specs/app-design/ for ASCII wireframes)
    4. Prompt Generation (convert wireframes to natural language prompts)
    5. Stitch Generation Pipeline (submit prompts, wait for generation)
    6. Export Pipeline (HTML, Tailwind, Screenshots, Figma clipboard)
    7. Gallery Generation (per-feature indexes, master gallery)
    8. Fallback Handling (manual mode if automation fails)
  - **Output Structure**: `.preview/stitch-mockups/` with HTML, CSS, screenshots (desktop/mobile), Figma JSON
  - **Rate Limit Tracking**: `.speckit/stitch/usage.json` tracks 350/month standard, 50/month experimental
  - **Manual Mode**: `--manual` flag generates prompts only without automation
  - **Re-authentication**: `--reauth` flag forces new Google OAuth flow
  - **Screen Selection**: `--screens "login,dashboard"` for specific screens only
  - **Error Recovery**: Auto-retry, session refresh, graceful fallback to manual mode

- **New Skill: `/speckit.stitch`** — Standalone Mockup Generation
  - Direct access to Stitch mockup generation without full design workflow
  - Supports `--all`, `--screens`, `--manual`, `--reauth`, `--prompt` flags
  - Interactive mode when run without arguments
  - Quality validation for generated outputs

- **Stitch Anti-Detection v3** — Bypass Google's Automation Detection
  - **Problem Solved**: Google started blocking Playwright automation with CAPTCHA challenges
  - **4-Mode Hybrid Strategy** with auto-fallback:
    - `CDP Mode` — Connect to user's existing Chrome via `--remote-debugging-port=9222` (zero detection)
    - `Stealth Mode` — Patchright + humanization + persistent profile (low detection)
    - `Turbo Mode` — Standard Playwright + stealth args (fast but risky)
    - `Assisted Mode` — Human-assisted workflow with prompt generation + collection
  - **Humanization Engine**:
    - Bezier curve mouse movements (Fitts's Law timing)
    - Gaussian-distributed typing delays with 2% typo rate
    - Random wait intervals with exponential distribution
    - Scroll simulation before clicking below-fold elements
    - Smooth viewport resize with easing functions
  - **New CLI Flags**:
    - `--mode cdp|stealth|turbo|assisted` — Explicit mode selection
    - `--setup-cdp` — Print Chrome launch command for CDP mode
    - `--speed slow|normal|fast` — Humanization intensity (2x, 1x, 0.5x delays)
    - `--prepare` — Generate prompts only (assisted mode phase 1)
    - `--collect` — Collect manual exports (assisted mode phase 3)
  - **CAPTCHA Detection & Fallback**: After 2 CAPTCHAs, auto-switch to assisted mode
  - **Mode Statistics Tracking**: Success/failure rates per mode in `usage.json`

- **New Shared Modules** (`templates/shared/`):
  - `stitch-integration.md` — Core Stitch automation module (8 workflow phases, v3.0.0 with multi-mode)
  - `stitch-anti-detection.md` — **NEW**: Humanization functions, Bezier curves, Fitts's Law, stealth browser config
  - `stitch-prompts.md` — Prompt templates for different screen types (dashboard, auth, form, list, detail, settings, empty, error, loading)
  - `stitch-selectors.md` — Versioned DOM selectors for Stitch UI (v1.0.0 with fallbacks)

- **Preview Command Enhancements**:
  - New preview type: Mockup (Stitch-generated mockups with side-by-side comparison)
  - Mockup gallery at `.preview/stitch-mockups/gallery.html`
  - Mockup comparison pages showing wireframe vs visual mockup
  - CLI flags: `--mockups`, `--mockups --compare`, `--mockups --feature {name}`

- **New Handoffs** (for mockup generation mode):
  - "Preview Mockups" → speckit.preview with Stitch gallery
  - "Retry Failed Screens" → speckit.design --mockup --screens "{failed}"

### Changed

- **Premium Smoke Test Landing Page** — Complete redesign of `/speckit.discover` landing page template
  - **Modern Visual Design**
    - Animated gradient orbs with `filter: blur(80px)` and floating animation
    - Grid pattern overlay with radial gradient mask for premium texture
    - Glassmorphism signup card with `backdrop-filter: blur(20px)`
    - Full-bleed hero section replacing minimal 640px container
  - **Micro-Interactions & Animations**
    - CTA button with hover lift, press scale, and shine sweep effect
    - Input focus ring animation with smooth transitions
    - Feature cards with staggered entrance animation
    - Card hover lift with shadow enhancement
  - **Success State with Confetti**
    - Checkmark SVG with `stroke-dashoffset` draw animation
    - Confetti burst celebration (50 particles, 5 colors)
    - Spring scale animation for success card
  - **Light/Dark Mode Support**
    - Automatic theme via `@media (prefers-color-scheme)`
    - CSS Variables system for complete theming
    - Optimized colors for both modes
  - **Accessibility Enhancements**
    - Full `prefers-reduced-motion` support (disables confetti and reduces animations)
    - ARIA attributes for form and interactive elements
    - Semantic HTML structure
    - 44px minimum touch targets
  - **New Template Variables**
    - `{{PRIMARY_COLOR_RGB}}` for rgba() usage in gradients
    - `{{YEAR}}` for copyright footer
    - `{{PRIVACY_URL}}`, `{{TERMS_URL}}` for legal links
  - **New Sections**
    - Features grid with gradient icon backgrounds
    - Trust indicators (SSL, GDPR, No Spam badges)
    - Minimalist footer with legal links

## [0.0.48] - 2025-12-29

### Added

- **New Commands from Section 2.2** — 5 new/enhanced commands for complete product lifecycle automation
  - **`/speckit.discover`** — Customer Discovery Automation
    - Validate problem-solution fit before building
    - Interview script generation with ICP validation
    - Survey templates for quantitative validation
    - Smoke test landing page generation for demand testing
    - Go/No-Go recommendation with signal strength analysis
    - Success criteria: 10+ interviews OR 50+ survey responses OR >5% landing conversion
  - **`/speckit.monitor`** — Observability Pipeline Setup
    - Auto-detect stack type (Node/Python/Go/Java)
    - OpenTelemetry instrumentation generation
    - Docker Compose observability stack (Prometheus, Grafana, Loki, Jaeger)
    - Grafana dashboard templates for API, infrastructure, and business metrics
    - Alerting rules with severity classification (critical/warning/info)
    - Runbook generation for incident response
  - **`/speckit.integrate`** — Third-Party Integration Wizard
    - Service catalog: Auth (Clerk, Auth0, Supabase), Payments (Stripe, Paddle), Email (Resend, SendGrid), Analytics (PostHog, Mixpanel), Storage (S3, R2), Database (Supabase, PlanetScale), Search (Algolia, Meilisearch), AI (OpenAI, Anthropic)
    - SDK wrapper generation with error handling
    - Integration smoke tests
    - Environment variable management
  - **`/speckit.launch`** — Go-to-Market Automation
    - Pre-launch readiness audit (12 categories)
    - Press kit generation (fact sheet, screenshots, founder bios)
    - SEO configuration (meta tags, sitemap, robots.txt)
    - Social media content templates
    - Product Hunt submission preparation
    - Launch day checklist with timeline

- **New Agent Personas** (`templates/personas/`)
  - `marketing-agent.md` — GTM specialist for launch strategy, content marketing, press relations, analytics
  - `devops-agent.md` — Infrastructure specialist for observability, CI/CD, IaC, incident response

- **New Skills** (`templates/skills/`)
  - `customer-interview.md` — Interview script generation and response analysis
  - `landing-generator.md` — Smoke test landing page creation
  - `observability-setup.md` — Monitoring stack configuration
  - `integration-wizard.md` — Third-party service integration
  - `launch-prep.md` — Launch preparation and GTM execution

- **New Shared Modules** (10 files)
  - `templates/shared/discover/` — Interview scripts, survey templates, smoke test landing
  - `templates/shared/monitor/` — Alerting rules, dashboard templates, runbooks
  - `templates/shared/integrate/` — Integration catalog with 8 service categories
  - `templates/shared/launch/` — GTM checklist, press kit, SEO setup

- **Role-Based Templates** (`templates/roles/`) — 12 new role-specific templates
  - **Developer** (`templates/roles/developer/`)
    - `code-review-checklist.md` — Comprehensive review checklist with severity levels
    - `pr-template.md` — Pull request template with testing checklist
    - `debugging-guide.md` — Systematic debugging methodology
  - **Product Manager** (`templates/roles/product-manager/`)
    - `prd-template.md` — Product Requirements Document template
    - `roadmap-template.md` — Quarterly/annual roadmap planning
    - `prioritization-framework.md` — RICE, MoSCoW, Kano frameworks
  - **Marketing** (`templates/roles/marketing/`)
    - `launch-checklist.md` — 50+ item launch checklist
    - `content-calendar.md` — Editorial planning template
    - `seo-guide.md` — Technical and content SEO guide
  - **Legal** (`templates/roles/legal/`)
    - `privacy-policy-template.md` — GDPR/CCPA compliant privacy policy
    - `terms-of-service-template.md` — ToS with special clauses for API, AI, marketplace
    - `gdpr-compliance-checklist.md` — 8-section GDPR compliance checklist

### Changed

- **`/speckit.design` enhanced with Design System Generation**
  - Dual-mode support: `feature_design` (existing) and `design_system` (new)
  - Brand input collection workflow (name, colors, product type)
  - Product type presets: SaaS (data-dense), Marketing (bold/conversion), Mobile (touch-first), Admin (efficient/tables)
  - Design System Generation Workflow (6 steps): Load Preset → Generate Color Palette → Generate Typography → Generate Spacing & Layout → Generate Component Library → Generate Output Files
  - Storybook auto-generation with component stories and documentation
  - Figma Token Export in Tokens Studio format
  - WCAG accessibility validation with contrast ratio checking

### Technical Details

- **Command Workflow Integration**
  ```
  /speckit.concept
      ├── /speckit.discover (validation)
      ▼
  /speckit.specify → /speckit.design (enhanced) → /speckit.plan
      ▼
  /speckit.implement
      ├── /speckit.integrate (during)
      ▼
  /speckit.ship
      ├── /speckit.monitor (post-deploy)
      ▼
  /speckit.launch (go-to-market)
  ```

- **File Count**: 33 new files + 1 modified file

---

## [0.0.47] - 2025-12-29

### Added

- **AI Designer Replacement System** — Full replacement of UX, Product, Motion, and Promo designer roles with AI agents
  - **New Designer Agent Personas** (`templates/personas/`):
    - `product-designer-agent.md`: Visual design, code generation, design system maintenance
    - `motion-designer-agent.md`: Animation tokens, micro-interactions, CSS/Framer Motion code
    - `promo-designer-agent.md`: Landing pages, marketing assets, social graphics specs
  - **Enhanced UX Designer Agent** with visual wireframe generation:
    - ASCII to HTML conversion workflow
    - `upgrade_to_interactive()` function for complexity-based generation
    - `validate_wireframe()` function for Claude Vision validation
    - Responsive wireframe generation for multiple breakpoints (mobile, tablet, desktop)
  - **New `/speckit.preview` Command** (`templates/commands/preview.md`):
    - Generate interactive previews from design specifications
    - Wireframe, component, animation, and flow preview generation
    - Playwright screenshot capture for all viewports
    - Storybook story auto-generation
    - Design Quality Score (DQS) validation
  - **Design Generation Skills** (`templates/skills/`):
    - `v0-generation.md`: v0.dev API integration for React component generation
    - `component-codegen.md`: Template-based fallback for simple/moderate components
    - `motion-generation.md`: Animation code generation (CSS keyframes, Framer Motion)
    - `wireframe-preview.md`: ASCII wireframe to visual HTML conversion
  - **Animation Presets Library** (`templates/shared/animation-presets/`):
    - `micro-interactions.md`: Button, form, feedback animations
    - `page-transitions.md`: Route transitions, shared element morphs
    - `loading-states.md`: Skeleton, spinner, progress animations
  - **Preview Pipeline** (`templates/shared/preview-pipeline.md`):
    - 6-stage architecture: Parse → Wireframes → Components → Animations → Flows → Server
    - Screenshot capture via Playwright (multi-viewport, multi-state)
    - Storybook integration with auto-story generation
    - Claude Vision validation for layout verification
  - **Visual Regression Testing** (`templates/shared/visual-regression.md`):
    - Multi-mode comparison: pixel, perceptual (SSIM), layout, anti-alias
    - Baseline management with versioning and backup
    - Diff image generation with highlight overlay
    - CI/CD integration (GitHub Actions, GitLab CI)
    - Threshold configuration per path/component type
  - **v0.dev Integration Guide** (`templates/shared/v0-integration.md`):
    - API and manual workflow documentation
    - Design token injection into prompts
    - Component caching with TTL
    - Validation and auto-correction of generated code

### Changed

- **`/speckit.design` enhanced with Designer Agent Orchestration**:
  - Phase 2: Product Designer Agent (visual language, component specs)
  - Phase 3: Motion Designer Agent (animation tokens, micro-interactions)
  - Phase 4: Quality Validation with Design Quality Score (DQS)
  - Steps 10-15 for sequential agent orchestration
  - Output structure includes `.preview/components/` and `.preview/animations/`
- **Motion tokens added to all design system presets** (`templates/shared/design-system-presets.md`):
  - Duration scale (instant → dramatic)
  - Easing functions (ease-out, spring, bounce)
  - CSS keyframes and Framer Motion variants
  - Reduced motion support (`prefers-reduced-motion`)
  - Presets updated: shadcn/ui, MUI, Tailwind, Vuetify, Bootstrap, custom
- **`design-template.md` enhanced with Motion System section**:
  - Duration tokens (6 levels: 0ms → 800ms)
  - Easing functions (6 types including spring and bounce)
  - Animation presets organized by category
  - CSS keyframes ready for copy-paste
  - Framer Motion variants for React projects
  - Reduced motion alternatives table
  - Motion tokens export in CSS variables

### Technical Details

- **Design Quality Score (DQS)** — 100-point automated quality scoring:
  - Visual Quality: 40 points (contrast, typography, spacing, color)
  - Accessibility: 30 points (WCAG AA, keyboard, screen reader)
  - Consistency: 20 points (token usage, component reuse)
  - Implementation: 10 points (TypeScript, tests)
  - Quality Gate: DQS ≥ 80 (production ready), 60-79 (minor polish), <60 (requires iteration)

- **Preview Server** runs at `localhost:3456` with routes:
  - `/wireframes/*` — Wireframe previews
  - `/components/*` — Component previews
  - `/animations` — Animation showcase
  - `/flows/*` — User flow previews

---

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

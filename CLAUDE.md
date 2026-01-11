# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spec Kit** is a toolkit for Spec-Driven Development (SDD) - a methodology where specifications drive code generation rather than the reverse. The main deliverable is the **Specify CLI** (`specify`), a Python CLI tool that bootstraps projects with templates, scripts, and AI agent integrations.

## Agent Execution Strategy

**CRITICAL**: Always execute tasks using parallel agents by default.

### Default Behavior

When performing any task that involves multiple operations:
1. **ALWAYS launch multiple Task agents in a single message** when operations are independent
2. Use `subagent_type=Explore` for all codebase searches
3. Use `subagent_type=general-purpose` for complex multi-step tasks
4. Set `run_in_background: true` for long-running operations

### Parallel Execution Patterns

| Task Type | Approach |
|-----------|----------|
| Code search | Launch 3-5 `Explore` agents for different patterns |
| File reads | Batch multiple Read calls in single message |
| Research | Launch multiple `general-purpose` agents |
| Code review | Launch security, quality, style agents simultaneously |
| Implementation | Plan agent + Explore agents in parallel |

### Examples

```
✅ CORRECT: Single message with multiple agents
- Task #1: "Search for authentication patterns"
- Task #2: "Search for authorization patterns"
- Task #3: "Search for session management"

❌ WRONG: Sequential one-by-one execution
- Task #1 → wait → Task #2 → wait → Task #3
```

### Model Selection for Agents

- `haiku` — Simple searches, quick lookups (fastest, cheapest)
- `sonnet` — Standard analysis, code review (default)
- `opus` — Complex architecture, critical decisions (highest quality)

## Common Commands

### Development

```bash
# Run CLI directly from source (fastest feedback)
python -m src.specify_cli --help
python -m src.specify_cli init demo-project --ai claude --ignore-agent-tools

# Editable install with uv
uv venv && source .venv/bin/activate
uv pip install -e .
specify --help

# Local uvx run
uvx --from . specify init demo --ai copilot --ignore-agent-tools

# Build wheel
uv build
```

### Testing Template Changes Locally

```bash
# Generate release packages locally
./.github/workflows/scripts/create-release-packages.sh v1.0.0

# Copy to test project
cp -r .genreleases/sdd-copilot-package-sh/. <path-to-test-project>/
```

### Quick Validation

```bash
# Verify module imports correctly
python -c "import specify_cli; print('Import OK')"

# Verify dependencies
uv sync
uv run specify --help
```

## Architecture

### Directory Structure

```text
spec-kit/
├── src/specify_cli/__init__.py  # Main CLI implementation (single-file CLI)
├── templates/                    # Templates copied to initialized projects
│   ├── commands/                 # Slash command templates for AI agents
│   ├── spec-template.md          # Feature specification template
│   ├── plan-template.md          # Implementation plan template
│   └── tasks-template.md         # Task breakdown template
├── scripts/                      # Scripts bundled with projects
│   ├── bash/                     # Shell scripts (.sh)
│   └── powershell/               # PowerShell scripts (.ps1)
├── memory/constitution.md        # Constitution template for project principles
└── docs/                         # Documentation site content
```

### Key Architectural Decisions

1. **Single-file CLI**: The entire CLI lives in `src/specify_cli/__init__.py` for simplicity and single-artifact distribution

2. **Agent Configuration**: `AGENT_CONFIG` dict in `__init__.py` is the single source of truth for all supported AI agents. Keys must match actual CLI tool names (e.g., `cursor-agent` not `cursor`)

3. **Template-based Generation**: The CLI downloads pre-packaged release assets from GitHub rather than generating files dynamically

4. **Script Variants**: Both Bash (`.sh`) and PowerShell (`.ps1`) variants are maintained for cross-platform support

### Adding a New AI Agent

When adding support for a new agent:

1. Add entry to `AGENT_CONFIG` in `src/specify_cli/__init__.py` - use actual CLI tool name as key
2. Update `--ai` help text in the `init()` command
3. Update README.md Supported Agents table
4. Update release scripts in `.github/workflows/scripts/`
5. Update agent context scripts in `scripts/bash/` and `scripts/powershell/`

See `AGENTS.md` for detailed integration guide.

## Version Management

- CLI version: `pyproject.toml` → `project.version`
- Any changes to `__init__.py` or any template require version bump in `pyproject.toml` and `CHANGELOG.md` entry
- Release assets are auto-generated via GitHub Actions on tag push

## Spec-Driven Development Workflow

The toolkit implements a workflow where AI agents use slash commands.

### Core Workflow (Primary Commands)

| Phase | Command | Description |
|-------|---------|-------------|
| 1. Foundation | `/speckit.constitution` | Interactive setup: app type, domain, language → generates constitution |
| 2. Discovery | `/speckit.concept` | Strategic product discovery & validation (50+ requirements) |
| 3. Validation | `/speckit.validate-concept` | Re-validate concept against current market conditions |
| 4. Specification | `/speckit.specify` | Create feature specification (what & why, not how) |
| 5. Clarification | `/speckit.clarify` | Clarify ambiguous requirements (optional) |
| 6. Planning | `/speckit.plan` | Create technical implementation plan |
| 7. Task Breakdown | `/speckit.tasks` | Generate actionable task breakdown (tests REQUIRED) |
| 8. Staging | `/speckit.staging` | Provision Docker Compose staging environment |
| 9. Quality Check | `/speckit.analyze` | Cross-artifact consistency check (optional) |
| 10. Implementation | `/speckit.implement` | Execute TDD implementation (tests first, then code) |

### TDD Workflow

The toolkit enforces Test-Driven Development with these key features:

1. **Tests are REQUIRED**: Every acceptance scenario (AS-xxx) must have a corresponding test task
2. **Staging before implementation**: `/speckit.staging` provisions local Docker services (PostgreSQL, Redis, Playwright)
3. **TDD wave ordering in `/speckit.implement`**:
   - Wave 0: Staging Validation (QG-STAGING-001)
   - Wave 1: Infrastructure setup
   - Wave 2: Test Scaffolding (TDD Red - failing tests first)
   - Wave 3: Core Implementation (TDD Green - make tests pass)
   - Wave 3.5: **PBT JIT Validation** (if properties.md exists)
   - Wave 4: Test Verification
   - Wave 5: Polish

### PBT Just-in-Time Workflow

When `/speckit.properties` is run before implementation, PBT tests execute incrementally:

1. **Auto-handoff**: After properties extraction, automatically continues to `/speckit.implement`
2. **JIT validation**: After each task that maps to PROP-xxx, run corresponding property test
3. **Auto-fix loop**: On failure, attempt up to 3 automatic fixes
4. **Traceability**: PROP-xxx → FR-xxx/AS-xxx → TASK-xxx mapping
5. **Final validation**: Full property suite runs in Wave 4 after all JIT checks

**Skip JIT mode**: `--skip-pbt-jit` flag on implement command

### Inline Quality Gates

Commands now have built-in quality gates that run automatically before handoffs:

| Command | Inline Gates | Passes Used | Severity |
|---------|--------------|-------------|----------|
| `/speckit.specify` | IG-SPEC-001..004 | B, D | CRITICAL, HIGH |
| `/speckit.plan` | IG-PLAN-001..004 | D, F | CRITICAL, HIGH |
| `/speckit.tasks` | IG-TASK-001..004 | G, H, J | CRITICAL, HIGH |
| `/speckit.implement` | IG-IMPL-001..104 | R, S, T, U | CRITICAL, HIGH |

**Gate Flags**:
- `--skip-gates` — Bypass all inline quality gates (not recommended)
- `--strict-gates` — Treat HIGH severity as blocking (same as CRITICAL)
- `--full-gates` — Run full validation pass instead of simplified check

**When to Use /speckit.analyze**:
- Full audit before major milestones (`--profile full`)
- Post-implementation QA verification (`--profile qa`)
- Comprehensive quality dashboard
- Troubleshooting quality issues

### Quality Gates (TDD)

| Gate | Phase | Purpose |
|------|-------|---------|
| QG-STAGING-001 | Pre-Implement | All Docker services healthy |
| QG-TEST-001 | Pre-Implement | 100% AS coverage with test tasks |
| QG-TEST-002 | Pre-Implement | Test framework configured |
| QG-TEST-003 | Wave 2 | Tests fail first (TDD red) |
| QG-TEST-004 | Post-Story | Coverage >= 80% |

### Task Batching (v0.0.110)

`/speckit.implement` now groups independent tasks into batches and executes them as parallel Task tool calls in a **single message**:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| API round-trips | N (per task) | N/4-8 | 4-8x fewer |
| Execution time | ~10 min | ~2-3 min | 60-75% faster |
| Parallelism | 1 task | 4-8 tasks | 4-8x |

**Algorithm**:
1. Parse tasks.md → build dependency graph
2. Compute topological levels (tasks at same level are independent)
3. Group by file conflicts (same-file → separate batches)
4. Execute each batch as parallel Task calls

**Skip**: `--sequential-tasks` flag

### CI/CD Integration

TDD pipeline templates available in `templates/shared/ci-templates.md`:
- **GitHub Actions**: `.github/workflows/tdd-pipeline.yml`
- **GitLab CI**: `.gitlab-ci.yml` with TDD stages
- **Local runner**: `scripts/bash/run-tdd-pipeline.sh`

### Supporting Commands

| Command | Description |
|---------|-------------|
| `/speckit.baseline` | Capture current state for brownfield projects |
| `/speckit.checklist` | Generate custom checklist for current feature |
| `/speckit.design` | Create visual specifications and design systems |
| `/speckit.discover` | Run discovery experiments and validation |
| `/speckit.extend` | Extend a merged feature with new capabilities |
| `/speckit.integrate` | Integration and deployment planning |
| `/speckit.launch` | Launch preparation and go-to-market |
| `/speckit.list` | List all features with current status |
| `/speckit.merge` | Finalize feature and update system specs after PR merge |
| `/speckit.monitor` | Set up monitoring and observability |
| `/speckit.preview` | Generate interactive previews from design specs |
| `/speckit.ship` | Provision infrastructure and deploy |
| `/speckit.switch` | Switch to a different feature branch |
| `/speckit.taskstoissues` | Convert tasks to GitHub issues |

### Quality Scores

| Score | Full Name | Purpose |
|-------|-----------|---------|
| **CQS** | Concept Quality Score | Quality gate for concept readiness (0-120, threshold ≥80) |
| **SQS** | Specification Quality Score | Quality gate for spec readiness (0-100, threshold ≥80) |

**Concept Phase**: For larger projects, the concept phase captures complete product vision with:
- TAM/SAM/SOM market sizing and competitive positioning
- JTBD-enhanced personas with willingness-to-pay analysis
- SMART-validated success metrics with North Star metric
- Risk assessment matrix with pivot criteria
- Technical discovery hints (domain entities, API surface)

Templates in `templates/commands/` define these slash command behaviors.
Modular concept sections in `templates/shared/concept-sections/` provide reusable frameworks.

## Post-Implementation Workflow

After completing any feature or significant change, ALWAYS:

1. **Update CHANGELOG.md**:
   - Determine current version from top entry
   - If today's date differs from latest entry → create new version (increment patch)
   - If same date → append to existing entry
   - Format: `## [X.Y.Z] - YYYY-MM-DD` with `### Added/Changed/Fixed` subsections

2. **Version bump** (if CLI code changed):
   - Update `pyproject.toml` → `project.version`
   - Keep in sync with CHANGELOG version

3. **Summary**: Report completed changes to user

This ensures traceability and prevents changelog updates from being forgotten.

## COMMANDS_GUIDE.md Maintenance

After any changes to `templates/commands/*.md`, update `docs/COMMANDS_GUIDE.md`:

### When to Update

- New command template created
- Existing command flags changed
- Command description or handoffs modified
- Quality gates added/removed

### Update Process

1. **Scan changed command templates**:
   - Read YAML frontmatter for: description, persona, model, thinking_budget, handoffs, pre_gates, gates
   - Extract CLI flags from markdown content (patterns: `--flag-name`, CLI tables, Parse arguments sections)

2. **Update COMMANDS_GUIDE.md sections**:
   - **Table of Contents**: Ensure new commands are listed in workflow order
   - **Command section**: Update or add section with format:
     ```markdown
     ### N. `/speckit.COMMAND` {#speckitcommand}

     **Назначение:** [description from frontmatter]

     **Модель:** [model] (thinking_budget: [value])

     **Флаги:**
     - `--flag` — description

     **Handoffs:**
     - → `/speckit.next-command`
     ```
   - **Quick Reference tables**: Update flags table if flags changed

3. **Update footer**:
   - Version from pyproject.toml
   - Generation timestamp (current date/time)

### Workflow Order (for TOC)

constitution → concept → validate-concept → specify → clarify → design → plan → tasks → taskstoissues → staging → analyze → implement → preview → list → switch → extend → merge → baseline → checklist → discover → integrate → monitor → launch → ship → concept-variants → migrate → properties

### Skip Updates When

- Only `.COMPRESSED.md` files changed
- Changes are only to non-command templates (shared/, etc.)

## ARCHITECTURE.md Maintenance

After any changes to core architectural components, update `ARCHITECTURE.md`:

### When to Update

Automatically update ARCHITECTURE.md when changes occur in:

**CLI Layer (Section 3):**
- `src/specify_cli/__init__.py` — CLI entry point, AGENT_CONFIG, commands
- `src/specify_cli/wave_scheduler.py` — DAG execution
- `src/specify_cli/agent_pool.py` — Concurrent API
- `src/specify_cli/batch_aggregator.py` — Cross-wave optimization
- `src/specify_cli/*.py` — Any other CLI modules

**Template System (Section 4):**
- `templates/commands/*.md` — New commands added or modified
- `templates/shared/concept-sections/*.md` — New modular sections
- `templates/shared/quality/*.md` — Quality gate definitions
- `templates/shared/traceability/*.md` — Traceability system changes

**Scripts & Automation (Section 6):**
- `scripts/bash/*.sh` — Bash script changes
- `scripts/powershell/*.ps1` — PowerShell script changes
- `memory/constitution.base.md` — Base constitution updated
- `memory/domains/*.md` — Domain-specific knowledge

**CI/CD & Release (Section 7):**
- `.github/workflows/*.yml` — GitHub Actions workflow changes
- `.github/workflows/scripts/*.sh` — Release scripts modified

**Configuration:**
- `pyproject.toml` — Version bumped, dependencies changed
- `AGENT_CONFIG` changes in `__init__.py` — New agents added/removed

### Update Process

#### 1. Detect Affected Sections

Map changed files to document sections using the Section Mapping Table below.

#### 2. Update Section Content

For each affected section:

**Section 3.3 (AGENT_CONFIG):**
- Scan `__init__.py` for AGENT_CONFIG dictionary (~line 185)
- Extract: agent name, folder, requires_cli
- Regenerate agent table:
  ```markdown
  | Agent | Folder | Requires CLI | Install URL |
  |-------|--------|--------------|-------------|
  | claude | .claude/ | Yes | https://... |
  ```
- Update agent count in text (currently 17 agents)

**Section 4.1 (Slash Commands):**
- Count files in `templates/commands/`
- Update command count (currently "50+ commands")
- Regenerate command list if new commands added

**Section 4.2 (Modular Sections):**
- Count files in `templates/shared/concept-sections/`
- Update section count (currently "36 секций")
- Update categorization if new categories added

**Section 5.2 (Quality Gates):**
- Parse `memory/domains/quality-gates.md`
- Extract QG-001 through QG-012, QG-TEST-001..004, QG-DRIFT-001..004, PM-001..006
- Update QG tables with: ID, Name, Threshold, Phase

**Section 6.2 (Key Scripts):**
- List all `.sh` files in `scripts/bash/`
- For each script, extract:
  - Purpose (from header comment)
  - Key functions (grep for function definitions)
  - Usage examples (from comments)
- Update script descriptions

**Section 7.1 (CI/CD Pipeline):**
- List all `.yml` files in `.github/workflows/`
- For each workflow:
  - Parse `name:` field
  - Parse `on:` triggers
  - Parse `jobs:` (job names)
- Update workflow descriptions

**Section 8.2 (Wave Scheduler Algorithm):**
- Parse `wave_scheduler.py` for:
  - DAG building algorithm
  - Topological sort implementation
  - File conflict detection logic
- Update algorithm description if implementation changed

**Section 11.1 (Glossary):**
- Add new terms when new concepts introduced
- Update existing term definitions if behavior changed

**Section 11.2 (File Path Reference):**
- Add new critical files to tables
- Update line counts if files significantly changed (±20%)
- Add new categories if new components added

**Section 11.3 (Changelog Highlights):**
- Parse `CHANGELOG.md` for latest 5 versions
- Extract highlights from `## [X.Y.Z]` sections
- Update version timeline table

#### 3. Update Meta Information

**Header Comment:**
```markdown
<!-- AUTO-GENERATED SECTIONS - DO NOT EDIT MANUALLY -->
<!-- Generated at: YYYY-MM-DD HH:MM:SS -->
<!-- Version: 0.4.0 (from pyproject.toml) -->
<!-- Sources: src/specify_cli/*.py, templates/**/*.md, scripts/**/* -->
```

**Footer:**
```markdown
**Документ версия**: 0.4.0
**Последнее обновление**: 2026-01-11
**Сгенерировано**: Автоматически из кодовой базы spec-kit
```

#### 4. Verification

After updating, verify:
- [ ] All section counts accurate (agents, commands, sections, scripts)
- [ ] Version numbers synchronized with `pyproject.toml`
- [ ] Timestamp updated to current date/time
- [ ] Code snippets valid (check syntax)
- [ ] Cross-references not broken (links between sections work)
- [ ] File paths absolute and correct
- [ ] Tables properly formatted

### Section Mapping Table

| File Pattern | Document Section | What to Update |
|--------------|------------------|----------------|
| `src/specify_cli/__init__.py` (AGENT_CONFIG) | 3.3 | Agent table, agent count |
| `src/specify_cli/__init__.py` (commands) | 3.5 | CLI commands list |
| `src/specify_cli/wave_scheduler.py` | 8.2 | DAG algorithm description |
| `src/specify_cli/agent_pool.py` | 8.3 | Concurrent API details |
| `src/specify_cli/batch_aggregator.py` | 8.4 | Cross-wave optimization |
| `templates/commands/*.md` (new file) | 4.1, 11.2 | Command count, file reference |
| `templates/commands/*.md` (YAML change) | 4.1 | Update frontmatter schema examples |
| `templates/shared/concept-sections/*.md` | 4.2 | Section count, categorization |
| `templates/shared/quality/*.md` | 5.1-5.5 | Quality rubrics, scoring |
| `templates/shared/traceability/*.md` | 5.4 | Traceability system description |
| `scripts/bash/*.sh` (new script) | 6.2, 11.2 | Add script description, file reference |
| `scripts/powershell/*.ps1` (new script) | 6.2, 11.2 | Add script description, file reference |
| `memory/domains/quality-gates.md` | 5.2, 5.3 | Update QG registry tables |
| `memory/constitution.base.md` | 6.3 | Layer 0 principles |
| `.github/workflows/*.yml` | 7.1 | CI/CD pipeline descriptions |
| `pyproject.toml` (version) | Footer, 11.3 | Version number, changelog |
| `CHANGELOG.md` | 11.3 | Changelog highlights table |

### Skip Updates When

**Do NOT update ARCHITECTURE.md if changes only in:**
- `*.COMPRESSED.md` files
- `templates/stacks/*.yaml` (tech stack configs)
- `templates/personas/*.md` (persona definitions)
- `templates/skills/*.md` (skill definitions)
- `docs/` directory (except if adding new architectural patterns)
- `.vscode/`, `.idea/` (IDE configs)
- Test files (`*_test.py`, `*_test.go`, `tests/`)
- README.md, CONTRIBUTING.md (non-architectural docs)

**Only update if:**
- Changes affect architecture (new modules, new patterns)
- New AI agents added/removed in AGENT_CONFIG
- Core algorithms changed (wave scheduling, batching, DAG)
- New Quality Gates added (QG-xxx, IG-xxx)
- New workflow commands added (handoffs, phases)
- Major version bump (0.x.0 → 0.y.0 or x.0.0 → y.0.0)

### Update Frequency

- **After minor changes**: Update affected sections only
- **After major features**: Full review of Sections 1-9
- **Before releases**: Full review + verification checklist
- **Version bumps**: Always update footer + Section 11.3

### Examples

**Example 1: New AI Agent Added**
```
Files changed: src/specify_cli/__init__.py (AGENT_CONFIG)
Affected sections: 3.3, 10.4, 11.1 (glossary if needed)
Action:
1. Update agent table in Section 3.3
2. Update agent count (16 → 17)
3. Update "ПОЧЕМУ 16 агентов?" → "ПОЧЕМУ 17 агентов?" in Section 10.4
4. Update AGENT_CONFIG code snippet if structure changed
```

**Example 2: New Slash Command**
```
Files changed: templates/commands/new-command.md
Affected sections: 4.1, 11.2
Action:
1. Update command count in Section 4.1 (50+ → 51+)
2. Add file to File Path Reference table in Section 11.2
3. If major command, add example to Section 4.1.3
```

**Example 3: Quality Gate Changes**
```
Files changed: memory/domains/quality-gates.md
Affected sections: 5.2, 5.3, 11.1
Action:
1. Re-parse quality-gates.md for new QG definitions
2. Update QG registry tables in Section 5.2
3. Update inline gates table in Section 5.2 if IG-* added
4. Add new gate IDs to glossary if they introduce new concepts
```

**Example 4: Version Bump to 0.5.0**
```
Files changed: pyproject.toml, CHANGELOG.md
Affected sections: Footer, 11.3
Action:
1. Update footer version (0.4.0 → 0.5.0)
2. Update footer timestamp
3. Add 0.5.0 to changelog highlights in Section 11.3
4. Update version timeline table
```

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

### Quality Gates (TDD)

| Gate | Phase | Purpose |
|------|-------|---------|
| QG-STAGING-001 | Pre-Implement | All Docker services healthy |
| QG-TEST-001 | Pre-Implement | 100% AS coverage with test tasks |
| QG-TEST-002 | Pre-Implement | Test framework configured |
| QG-TEST-003 | Wave 2 | Tests fail first (TDD red) |
| QG-TEST-004 | Post-Story | Coverage >= 80% |

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

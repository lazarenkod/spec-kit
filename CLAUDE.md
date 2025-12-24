# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spec Kit** is a toolkit for Spec-Driven Development (SDD) - a methodology where specifications drive code generation rather than the reverse. The main deliverable is the **Specify CLI** (`specify`), a Python CLI tool that bootstraps projects with templates, scripts, and AI agent integrations.

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
- Any changes to `__init__.py` require version bump in `pyproject.toml` and `CHANGELOG.md` entry
- Release assets are auto-generated via GitHub Actions on tag push

## Spec-Driven Development Workflow

The toolkit implements a workflow where AI agents use slash commands:

1. `/speckit.constitution` - Establish project principles
2. `/speckit.specify` - Create feature specification (what & why, not how)
3. `/speckit.clarify` - Clarify ambiguous requirements (optional)
4. `/speckit.plan` - Create technical implementation plan
5. `/speckit.tasks` - Generate actionable task breakdown
6. `/speckit.analyze` - Cross-artifact consistency check (optional)
7. `/speckit.implement` - Execute implementation

Templates in `templates/commands/` define these slash command behaviors.

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
#     "pyyaml",
# ]
# ///
"""
Specify CLI - Setup tool for Specify projects

Usage:
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init .
    uvx specify-cli.py init --here

Or install globally:
    uv tool install --from specify-cli.py specify-cli
    specify init <project-name>
    specify init .
    specify init --here
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import shlex
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

import yaml

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# Task status updater
from .task_status_updater import TaskStatusUpdater, TaskUpdate

# For cross-platform keyboard input
import readchar
import ssl
import truststore
from datetime import datetime, timezone

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)

def _github_token(cli_token: str | None = None) -> str | None:
    """Return sanitized GitHub token (cli arg takes precedence) or None."""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None

def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}

def _parse_rate_limit_headers(headers: httpx.Headers) -> dict:
    """Extract and parse GitHub rate-limit headers."""
    info = {}
    
    # Standard GitHub rate-limit headers
    if "X-RateLimit-Limit" in headers:
        info["limit"] = headers.get("X-RateLimit-Limit")
    if "X-RateLimit-Remaining" in headers:
        info["remaining"] = headers.get("X-RateLimit-Remaining")
    if "X-RateLimit-Reset" in headers:
        reset_epoch = int(headers.get("X-RateLimit-Reset", "0"))
        if reset_epoch:
            reset_time = datetime.fromtimestamp(reset_epoch, tz=timezone.utc)
            info["reset_epoch"] = reset_epoch
            info["reset_time"] = reset_time
            info["reset_local"] = reset_time.astimezone()
    
    # Retry-After header (seconds or HTTP-date)
    if "Retry-After" in headers:
        retry_after = headers.get("Retry-After")
        try:
            info["retry_after_seconds"] = int(retry_after)
        except ValueError:
            # HTTP-date format - not implemented, just store as string
            info["retry_after"] = retry_after
    
    return info

def _format_rate_limit_error(status_code: int, headers: httpx.Headers, url: str) -> str:
    """Format a user-friendly error message with rate-limit information."""
    rate_info = _parse_rate_limit_headers(headers)
    
    lines = [f"GitHub API returned status {status_code} for {url}"]
    lines.append("")
    
    if rate_info:
        lines.append("[bold]Rate Limit Information:[/bold]")
        if "limit" in rate_info:
            lines.append(f"  • Rate Limit: {rate_info['limit']} requests/hour")
        if "remaining" in rate_info:
            lines.append(f"  • Remaining: {rate_info['remaining']}")
        if "reset_local" in rate_info:
            reset_str = rate_info["reset_local"].strftime("%Y-%m-%d %H:%M:%S %Z")
            lines.append(f"  • Resets at: {reset_str}")
        if "retry_after_seconds" in rate_info:
            lines.append(f"  • Retry after: {rate_info['retry_after_seconds']} seconds")
        lines.append("")
    
    # Add troubleshooting guidance
    lines.append("[bold]Troubleshooting Tips:[/bold]")
    lines.append("  • If you're on a shared CI or corporate environment, you may be rate-limited.")
    lines.append("  • Consider using a GitHub token via --github-token or the GH_TOKEN/GITHUB_TOKEN")
    lines.append("    environment variable to increase rate limits.")
    lines.append("  • Authenticated requests have a limit of 5,000/hour vs 60/hour for unauthenticated.")
    
    return "\n".join(lines)

# Agent configuration with name, folder, install URL, and CLI tool requirement
AGENT_CONFIG = {
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "install_url": None,  # IDE-based, no CLI check needed
        "requires_cli": False,
    },
    "claude": {
        "name": "Claude Code",
        "folder": ".claude/",
        "install_url": "https://docs.anthropic.com/en/docs/claude-code/setup",
        "requires_cli": True,
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini/",
        "install_url": "https://github.com/google-gemini/gemini-cli",
        "requires_cli": True,
    },
    "cursor-agent": {
        "name": "Cursor",
        "folder": ".cursor/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen/",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex/",
        "install_url": "https://github.com/openai/codex",
        "requires_cli": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "folder": ".windsurf/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "kilocode": {
        "name": "Kilo Code",
        "folder": ".kilocode/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "auggie": {
        "name": "Auggie CLI",
        "folder": ".augment/",
        "install_url": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
        "requires_cli": True,
    },
    "codebuddy": {
        "name": "CodeBuddy",
        "folder": ".codebuddy/",
        "install_url": "https://www.codebuddy.ai/cli",
        "requires_cli": True,
    },
    "qoder": {
        "name": "Qoder CLI",
        "folder": ".qoder/",
        "install_url": "https://qoder.com/cli",
        "requires_cli": True,
    },
    "roo": {
        "name": "Roo Code",
        "folder": ".roo/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "q": {
        "name": "Amazon Q Developer CLI",
        "folder": ".amazonq/",
        "install_url": "https://aws.amazon.com/developer/learning/q-developer-cli/",
        "requires_cli": True,
    },
    "amp": {
        "name": "Amp",
        "folder": ".agents/",
        "install_url": "https://ampcode.com/manual#install",
        "requires_cli": True,
    },
    "shai": {
        "name": "SHAI",
        "folder": ".shai/",
        "install_url": "https://github.com/ovh/shai",
        "requires_cli": True,
    },
    "bob": {
        "name": "IBM Bob",
        "folder": ".bob/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
}

SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}

# Production-First Templates
TEMPLATE_CHOICES = {
    "production-saas": "Full-stack SaaS with auth, payments, observability",
    "production-api": "REST/GraphQL API backend with observability",
    "mobile-app": "iOS/Android app with offline support and analytics",
    "gaming": "Real-time game with multiplayer and anti-cheat",
    "fintech": "Regulated financial services (PCI-DSS, SOC2)",
    "healthcare": "HIPAA/GDPR-compliant health application",
    "e-commerce": "Online store with payments and inventory",
    "minimal": "Empty template - configure everything yourself",
}

CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"

# Workspace configuration
WORKSPACE_CONFIG_FILE = ".speckit-workspace"
WORKSPACE_LINKS_DIR = ".speckit/links/repos"
WORKSPACE_CACHE_DIR = ".speckit/cache"
WORKSPACE_VERSION = "1.0"

# Link strategy constants
LINK_STRATEGY_AUTO = "auto"
LINK_STRATEGY_SYMLINK = "symlink"
LINK_STRATEGY_JUNCTION = "junction"  # Windows directory symlinks
LINK_STRATEGY_PATH_REF = "path_ref"  # Fallback for restricted environments

# Repository role types
REPO_ROLES = ["backend", "frontend", "mobile", "shared", "infrastructure", "docs", "other"]


@dataclass
class RepoConfig:
    """Configuration for a single repository in a workspace."""
    path: str
    alias: Optional[str] = None
    role: str = "other"
    domain: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for YAML serialization."""
        result = {"path": self.path}
        if self.alias:
            result["alias"] = self.alias
        if self.role and self.role != "other":
            result["role"] = self.role
        if self.domain:
            result["domain"] = self.domain
        return result

    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> "RepoConfig":
        """Create from dictionary (YAML data)."""
        if isinstance(data, str):
            # Simple format: just a path
            return cls(path=data, alias=name)
        return cls(
            path=data.get("path", ""),
            alias=data.get("alias", name),
            role=data.get("role", "other"),
            domain=data.get("domain"),
        )


@dataclass
class CrossDependency:
    """Cross-repository dependency."""
    source: str  # Format: "repo-alias:feature-id"
    target: str  # Format: "repo-alias:feature-id"
    dep_type: str = "REQUIRES"  # REQUIRES, BLOCKS, EXTENDS, IMPLEMENTS

    def to_dict(self) -> Dict[str, str]:
        return {
            "source": self.source,
            "target": self.target,
            "type": self.dep_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "CrossDependency":
        return cls(
            source=data.get("source", ""),
            target=data.get("target", ""),
            dep_type=data.get("type", "REQUIRES"),
        )


@dataclass
class WorkspaceConfig:
    """Workspace configuration stored in .speckit-workspace."""
    name: str
    version: str = WORKSPACE_VERSION
    link_strategy: str = LINK_STRATEGY_AUTO
    repositories: Dict[str, RepoConfig] = field(default_factory=dict)
    cross_dependencies: List[CrossDependency] = field(default_factory=list)

    def to_yaml(self) -> str:
        """Serialize to YAML string."""
        data = {
            "version": self.version,
            "name": self.name,
            "link_strategy": self.link_strategy,
            "repositories": {
                name: repo.to_dict()
                for name, repo in self.repositories.items()
            },
        }
        if self.cross_dependencies:
            data["cross_dependencies"] = [
                dep.to_dict() for dep in self.cross_dependencies
            ]
        return yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "WorkspaceConfig":
        """Parse from YAML string."""
        data = yaml.safe_load(yaml_str)
        if not data:
            raise ValueError("Empty or invalid YAML")

        repos = {}
        for name, repo_data in data.get("repositories", {}).items():
            repos[name] = RepoConfig.from_dict(name, repo_data)

        deps = []
        for dep_data in data.get("cross_dependencies", []):
            deps.append(CrossDependency.from_dict(dep_data))

        return cls(
            name=data.get("name", ""),
            version=data.get("version", WORKSPACE_VERSION),
            link_strategy=data.get("link_strategy", LINK_STRATEGY_AUTO),
            repositories=repos,
            cross_dependencies=deps,
        )

    def save(self, workspace_root: Path) -> None:
        """Save configuration to workspace root."""
        config_path = workspace_root / WORKSPACE_CONFIG_FILE
        config_path.write_text(self.to_yaml(), encoding="utf-8")

    @classmethod
    def load(cls, workspace_root: Path) -> "WorkspaceConfig":
        """Load configuration from workspace root."""
        config_path = workspace_root / WORKSPACE_CONFIG_FILE
        if not config_path.exists():
            raise FileNotFoundError(f"No workspace config found at {config_path}")
        return cls.from_yaml(config_path.read_text(encoding="utf-8"))


def find_workspace_root(start_path: Path = None) -> Optional[Path]:
    """Find the workspace root by searching upward for .speckit-workspace file.

    Args:
        start_path: Path to start searching from (defaults to cwd)

    Returns:
        Path to workspace root, or None if not found
    """
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()

    # Search upward until we hit the root
    while current != current.parent:
        config_file = current / WORKSPACE_CONFIG_FILE
        if config_file.exists():
            return current
        current = current.parent

    # Check root as well
    config_file = current / WORKSPACE_CONFIG_FILE
    if config_file.exists():
        return current

    return None


def detect_link_strategy() -> str:
    """Auto-detect the best link strategy for the current platform.

    Returns:
        One of: symlink, junction, path_ref
    """
    # Check environment variable override
    env_strategy = os.environ.get("SPECKIT_LINK_STRATEGY", "").lower()
    if env_strategy in [LINK_STRATEGY_SYMLINK, LINK_STRATEGY_JUNCTION, LINK_STRATEGY_PATH_REF]:
        return env_strategy

    if os.name == "nt":
        # Windows: try junction first, fall back to path_ref
        # Junctions don't require admin privileges on modern Windows
        try:
            # Test if we can create junctions
            test_dir = Path(tempfile.gettempdir()) / f".speckit_junction_test_{os.getpid()}"
            target_dir = Path(tempfile.gettempdir())

            # Clean up any existing test
            if test_dir.exists():
                test_dir.unlink()

            # Try to create a junction
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(test_dir), str(target_dir)],
                check=True,
                capture_output=True,
            )

            # Clean up
            if test_dir.exists():
                test_dir.unlink()

            return LINK_STRATEGY_JUNCTION
        except Exception:
            return LINK_STRATEGY_PATH_REF
    else:
        # Unix: symlinks are the default
        try:
            # Test if we can create symlinks
            test_link = Path(tempfile.gettempdir()) / f".speckit_symlink_test_{os.getpid()}"
            target = Path(tempfile.gettempdir())

            if test_link.exists() or test_link.is_symlink():
                test_link.unlink()

            test_link.symlink_to(target)
            test_link.unlink()

            return LINK_STRATEGY_SYMLINK
        except Exception:
            return LINK_STRATEGY_PATH_REF


def resolve_link_strategy(strategy: str) -> str:
    """Resolve 'auto' to actual strategy, or validate explicit strategy."""
    if strategy == LINK_STRATEGY_AUTO:
        return detect_link_strategy()
    if strategy not in [LINK_STRATEGY_SYMLINK, LINK_STRATEGY_JUNCTION, LINK_STRATEGY_PATH_REF]:
        raise ValueError(f"Invalid link strategy: {strategy}")
    return strategy


BANNER = """
███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝ 
╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝  
███████║██║     ███████╗╚██████╗██║██║        ██║   
╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝   
"""

TAGLINE = "GitHub Spec Kit - Spec-Driven Development Toolkit"
class StepTracker:
    """Track and render hierarchical steps without emojis, similar to Claude Code tree output.
    Supports live auto-refresh via an attached refresh callback.
    """
    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return

        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree

def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()

    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return 'up'
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return 'down'

    if key == readchar.key.ENTER:
        return 'enter'

    if key == readchar.key.ESC:
        return 'escape'

    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key

def select_with_arrows(options: dict, prompt_text: str = "Select an option", default_key: str = None) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.
    
    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with
        
    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == 'up':
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == 'down':
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == 'enter':
                        selected_key = option_keys[selected_index]
                        break
                    elif key == 'escape':
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    return selected_key


def load_stack_template(template_name: str, templates_path: Path = None) -> Optional[Dict[str, Any]]:
    """
    Load a stack template YAML file.

    Args:
        template_name: Name of the template (e.g., 'production-saas')
        templates_path: Path to templates directory (defaults to bundled templates)

    Returns:
        Parsed YAML content or None if not found
    """
    if templates_path is None:
        # Look for templates in the package resources
        templates_path = Path(__file__).parent.parent.parent / "templates" / "stacks"

    template_file = templates_path / f"{template_name}.yaml"
    if not template_file.exists():
        return None

    try:
        with open(template_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def generate_requirements_checklist(
    project_path: Path,
    template_name: str,
    template_data: Dict[str, Any],
    stack_selections: Dict[str, str] = None
) -> Path:
    """
    Generate REQUIREMENTS_CHECKLIST.md from template data.

    Args:
        project_path: Path to project directory
        template_name: Name of the template
        template_data: Parsed template YAML data
        stack_selections: User's selections for each category (optional)

    Returns:
        Path to generated checklist file
    """
    checklist_path = project_path / "REQUIREMENTS_CHECKLIST.md"

    # Build stack table
    stack_lines = ["| Category | Selected | Constitution Principles |", "|----------|----------|------------------------|"]

    if stack_selections and template_data.get("categories"):
        for category, selected in stack_selections.items():
            category_data = template_data.get("categories", {}).get(category, {})
            options = category_data.get("options", [])

            # Find selected option's constitution principles
            principles = []
            for opt in options:
                if opt.get("name") == selected:
                    principles = opt.get("constitution", [])
                    break

            principles_str = ", ".join(principles) if principles else "-"
            stack_lines.append(f"| {category.title()} | {selected} | {principles_str} |")
    else:
        stack_lines.append(f"| - | Using {template_name} defaults | See template |")

    stack_table = "\n".join(stack_lines)

    # Build functional checklist
    functional_items = template_data.get("checklist", {}).get("functional", [])
    functional_checklist = "\n".join([f"- [ ] {item}" for item in functional_items]) if functional_items else "- [ ] Define core requirements"

    # Build non-functional checklist
    non_functional_items = template_data.get("checklist", {}).get("non_functional", [])
    non_functional_checklist = "\n".join([f"- [ ] {item}" for item in non_functional_items]) if non_functional_items else "- [ ] Define quality attributes"

    # Build constitution principles list
    all_principles = set()
    if stack_selections and template_data.get("categories"):
        for category, selected in stack_selections.items():
            category_data = template_data.get("categories", {}).get(category, {})
            for opt in category_data.get("options", []):
                if opt.get("name") == selected:
                    all_principles.update(opt.get("constitution", []))

    principles_list = "\n".join([f"- {p}" for p in sorted(all_principles)]) if all_principles else "- (Select stack options to activate principles)"

    # Build domain files list
    domains = template_data.get("domains", [])
    domain_files = "\n".join([f"- `memory/domains/{d}.md`" for d in domains]) if domains else "- No domain files activated"

    # Get current date
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Generate the checklist content
    content = f"""# Requirements Checklist

Generated by Spec Kit for **{template_data.get('name', template_name)}** template.

> **Philosophy**: "Don't make me think about what I might forget"
>
> This checklist surfaces critical requirements you might overlook when starting a project.
> Review each item and mark as done or explicitly skipped.

---

## Stack Configuration

{stack_table}

---

## Functional Requirements

Define these in your feature specifications (`spec.md`):

{functional_checklist}

---

## Non-Functional Requirements

Configure these in your constitution (`constitution.md`) or clarify during `/speckit.clarify`:

{non_functional_checklist}

---

## Constitution Principles Activated

The following constitution principles are automatically active based on your stack choices:

{principles_list}

---

## Domain Files Activated

Based on your template, these domain files will be composed into your constitution:

{domain_files}

---

## Next Steps

1. **Review this checklist** — Mark items as done or explicitly skipped
2. **Run `/speckit.constitution`** — Configure project principles
3. **Run `/speckit.specify`** — Create your first feature specification
4. **Follow the SDD workflow**: specify → clarify → plan → tasks → implement

---

## Template Info

- **Template**: {template_name}
- **Generated**: {current_date}
- **Framework**: {template_data.get('framework', {}).get('primary', 'Not specified')}

---

*This file is generated once during `specify init`. You can modify it freely.*
"""

    checklist_path.write_text(content, encoding="utf-8")
    return checklist_path


console = Console()

class BannerGroup(TyperGroup):
    """Custom group that shows banner before help and workflow after."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)
        # Show workflow after help (compact version)
        console.print()
        show_workflow(compact=True)


app = typer.Typer(
    name="specify",
    help="Setup tool for Specify spec-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)

def show_banner():
    """Display the ASCII art banner."""
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


def show_workflow(compact: bool = False):
    """Display available commands and recommended workflow.

    Args:
        compact: If True, show a more compact version for --help
    """
    # Core Workflow Commands
    core_table = Table(show_header=True, header_style="bold cyan", box=None, padding=(0, 2))
    core_table.add_column("Command", style="cyan", no_wrap=True)
    core_table.add_column("Description")

    core_commands = [
        ("/speckit.constitution", "Define project principles and constraints"),
        ("/speckit.specify", "Create a feature specification (what & why)"),
        ("/speckit.clarify", "Resolve ambiguities in the specification"),
        ("/speckit.plan", "Create technical implementation plan"),
        ("/speckit.tasks", "Generate actionable task breakdown"),
        ("/speckit.implement", "Execute the implementation"),
    ]

    for cmd, desc in core_commands:
        core_table.add_row(cmd, desc)

    console.print(Panel(core_table, title="[bold]Core Workflow[/bold]", border_style="cyan", padding=(1, 2)))

    if not compact:
        # Workflow Diagram
        workflow_text = """
[dim]Recommended order:[/dim]

  [cyan]1. CONSTITUTION[/cyan]  →  Define project rules & principles
        ↓
  [cyan]2. SPECIFY[/cyan]      →  Describe what you want (not how)
        ↓
  [cyan]3. CLARIFY[/cyan]       →  Resolve any ambiguities
        ↓
  [cyan]4. PLAN[/cyan]          →  Define tech stack & architecture
        ↓
  [cyan]5. TASKS[/cyan]         →  Break down into actionable items
        ↓
  [cyan]6. IMPLEMENT[/cyan]     →  Let the AI build it
"""
        console.print(Panel(workflow_text.strip(), title="[bold]Workflow[/bold]", border_style="green", padding=(1, 2)))

    # Extended Commands
    extended_table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
    extended_table.add_column("Command", style="cyan", no_wrap=True)
    extended_table.add_column("Description")
    extended_table.add_column("When to Use", style="dim")

    extended_commands = [
        ("/speckit.concept", "Capture complete service concept", "Large projects (50+ requirements)"),
        ("/speckit.design", "Create visual specs & design system", "UI-heavy features"),
        ("/speckit.baseline", "Capture current system state", "Brownfield projects"),
        ("/speckit.analyze", "Cross-artifact consistency check", "Before implementation"),
        ("/speckit.checklist", "Validate spec completeness", "After planning"),
    ]

    for cmd, desc, when in extended_commands:
        extended_table.add_row(cmd, desc, when)

    console.print(Panel(extended_table, title="[bold]Extended Commands[/bold]", border_style="yellow", padding=(1, 2)))

    # Feature Management
    mgmt_table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
    mgmt_table.add_column("Command", style="cyan", no_wrap=True)
    mgmt_table.add_column("Description")

    mgmt_commands = [
        ("/speckit.list", "List all specifications in the project"),
        ("/speckit.switch", "Switch to a different specification"),
        ("/speckit.extend", "Extend a merged feature with new capabilities"),
        ("/speckit.merge", "Finalize feature after PR merge"),
        ("/speckit.taskstoissues", "Convert tasks into GitHub issues"),
    ]

    for cmd, desc in mgmt_commands:
        mgmt_table.add_row(cmd, desc)

    console.print(Panel(mgmt_table, title="[bold]Feature Management[/bold]", border_style="magenta", padding=(1, 2)))

    # Infrastructure & Deployment
    infra_table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
    infra_table.add_column("Command", style="cyan", no_wrap=True)
    infra_table.add_column("Description")

    infra_commands = [
        ("/speckit.ship", "Provision infrastructure, deploy, and verify"),
    ]

    for cmd, desc in infra_commands:
        infra_table.add_row(cmd, desc)

    console.print(Panel(infra_table, title="[bold]Infrastructure & Deployment[/bold]", border_style="blue", padding=(1, 2)))

@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'specify --help' for usage information[/dim]"))
        console.print()

def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None

def check_tool(tool: str, tracker: StepTracker = None) -> bool:
    """Check if a tool is installed. Optionally update tracker.
    
    Args:
        tool: Name of the tool to check
        tracker: Optional StepTracker to update with results
        
    Returns:
        True if tool is found, False otherwise
    """
    # Special handling for Claude CLI after `claude migrate-installer`
    # See: https://github.com/github/spec-kit/issues/123
    # The migrate-installer command REMOVES the original executable from PATH
    # and creates an alias at ~/.claude/local/claude instead
    # This path should be prioritized over other claude executables in PATH
    if tool == "claude":
        if CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
            if tracker:
                tracker.complete(tool, "available")
            return True
    
    found = shutil.which(tool) is not None
    
    if tracker:
        if found:
            tracker.complete(tool, "available")
        else:
            tracker.error(tool, "not found")
    
    return found

def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()
    
    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git_repo(project_path: Path, quiet: bool = False) -> Tuple[bool, Optional[str]]:
    """Initialize a git repository in the specified path.
    
    Args:
        project_path: Path to initialize git repository in
        quiet: if True suppress console output (tracker handles status)
    
    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Specify template"], check=True, capture_output=True, text=True)
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True, None

    except subprocess.CalledProcessError as e:
        error_msg = f"Command: {' '.join(e.cmd)}\nExit code: {e.returncode}"
        if e.stderr:
            error_msg += f"\nError: {e.stderr.strip()}"
        elif e.stdout:
            error_msg += f"\nOutput: {e.stdout.strip()}"
        
        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False, error_msg
    finally:
        os.chdir(original_cwd)

def handle_vscode_settings(sub_item, dest_file, rel_path, verbose=False, tracker=None) -> None:
    """Handle merging or copying of .vscode/settings.json files."""
    def log(message, color="green"):
        if verbose and not tracker:
            console.print(f"[{color}]{message}[/] {rel_path}")

    try:
        with open(sub_item, 'r', encoding='utf-8') as f:
            new_settings = json.load(f)

        if dest_file.exists():
            merged = merge_json_files(dest_file, new_settings, verbose=verbose and not tracker)
            with open(dest_file, 'w', encoding='utf-8') as f:
                json.dump(merged, f, indent=4)
                f.write('\n')
            log("Merged:", "green")
        else:
            shutil.copy2(sub_item, dest_file)
            log("Copied (no existing settings.json):", "blue")

    except Exception as e:
        log(f"Warning: Could not merge, copying instead: {e}", "yellow")
        shutil.copy2(sub_item, dest_file)

def merge_json_files(existing_path: Path, new_content: dict, verbose: bool = False) -> dict:
    """Merge new JSON content into existing JSON file.

    Performs a deep merge where:
    - New keys are added
    - Existing keys are preserved unless overwritten by new content
    - Nested dictionaries are merged recursively
    - Lists and other values are replaced (not merged)

    Args:
        existing_path: Path to existing JSON file
        new_content: New JSON content to merge in
        verbose: Whether to print merge details

    Returns:
        Merged JSON content as dict
    """
    try:
        with open(existing_path, 'r', encoding='utf-8') as f:
            existing_content = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, just use new content
        return new_content

    def deep_merge(base: dict, update: dict) -> dict:
        """Recursively merge update dict into base dict."""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                result[key] = deep_merge(result[key], value)
            else:
                # Add new key or replace existing value
                result[key] = value
        return result

    merged = deep_merge(existing_content, new_content)

    if verbose:
        console.print(f"[cyan]Merged JSON file:[/cyan] {existing_path.name}")

    return merged

def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None, repo: str = None) -> Tuple[Path, dict]:
    # Default to official repo, but allow custom fork via --repo parameter
    if repo:
        parts = repo.split("/")
        if len(parts) != 2:
            raise ValueError(f"Invalid repo format '{repo}'. Expected 'owner/repo-name'")
        repo_owner, repo_name = parts
    else:
        repo_owner = "github"
        repo_name = "spec-kit"
    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = client.get(
            api_url,
            timeout=30,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        )
        status = response.status_code
        if status != 200:
            # Format detailed error message with rate-limit info
            error_msg = _format_rate_limit_error(status, response.headers, api_url)
            if debug:
                error_msg += f"\n\n[dim]Response body (truncated 500):[/dim]\n{response.text[:500]}"
            raise RuntimeError(error_msg)
        try:
            release_data = response.json()
        except ValueError as je:
            raise RuntimeError(f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}")
    except Exception as e:
        console.print(f"[red]Error fetching release information[/red]")
        console.print(Panel(str(e), title="Fetch Error", border_style="red"))
        raise typer.Exit(1)

    assets = release_data.get("assets", [])
    pattern = f"spec-kit-template-{ai_assistant}-{script_type}"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]

    asset = matching_assets[0] if matching_assets else None

    if asset is None:
        console.print(f"[red]No matching release asset found[/red] for [bold]{ai_assistant}[/bold] (expected pattern: [bold]{pattern}[/bold])")
        asset_names = [a.get('name', '?') for a in assets]
        console.print(Panel("\n".join(asset_names) or "(no assets)", title="Available Assets", border_style="yellow"))
        raise typer.Exit(1)

    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]

    if verbose:
        console.print(f"[cyan]Found template:[/cyan] {filename}")
        console.print(f"[cyan]Size:[/cyan] {file_size:,} bytes")
        console.print(f"[cyan]Release:[/cyan] {release_data['tag_name']}")

    zip_path = download_dir / filename
    if verbose:
        console.print(f"[cyan]Downloading template...[/cyan]")

    try:
        with client.stream(
            "GET",
            download_url,
            timeout=60,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                # Handle rate-limiting on download as well
                error_msg = _format_rate_limit_error(response.status_code, response.headers, download_url)
                if debug:
                    error_msg += f"\n\n[dim]Response body (truncated 400):[/dim]\n{response.text[:400]}"
                raise RuntimeError(error_msg)
            total_size = int(response.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f:
                if total_size == 0:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            console=console,
                        ) as progress:
                            task = progress.add_task("Downloading...", total=total_size)
                            downloaded = 0
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress.update(task, completed=downloaded)
                    else:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
    except Exception as e:
        console.print(f"[red]Error downloading template[/red]")
        detail = str(e)
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(detail, title="Download Error", border_style="red"))
        raise typer.Exit(1)
    if verbose:
        console.print(f"Downloaded: {filename}")
    metadata = {
        "filename": filename,
        "size": file_size,
        "release": release_data["tag_name"],
        "asset_url": download_url
    }
    return zip_path, metadata

def download_and_extract_template(project_path: Path, ai_assistant: str, script_type: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None, client: httpx.Client = None, debug: bool = False, github_token: str = None, repo: str = None) -> Path:
    """Download the latest release and extract it to create a new project.
    Returns project_path. Uses tracker if provided (with keys: fetch, download, extract, cleanup)
    """
    current_dir = Path.cwd()

    if tracker:
        tracker.start("fetch", "contacting GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            ai_assistant,
            current_dir,
            script_type=script_type,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None),
            client=client,
            debug=debug,
            github_token=github_token,
            repo=repo
        )
        if tracker:
            tracker.complete("fetch", f"release {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "Download template")
            tracker.complete("download", meta['filename'])
    except Exception as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]Error downloading template:[/red] {e}")
        raise

    if tracker:
        tracker.add("extract", "Extract template")
        tracker.start("extract")
    elif verbose:
        console.print("Extracting template...")

    try:
        if not is_current_dir:
            project_path.mkdir(parents=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} entries")
            elif verbose:
                console.print(f"[cyan]ZIP contains {len(zip_contents)} items[/cyan]")

            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    zip_ref.extractall(temp_path)

                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]")

                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "Flatten nested directory")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print(f"[cyan]Found nested directory structure[/cyan]")

                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]Merging directory:[/yellow] {item.name}")
                                for sub_item in item.rglob('*'):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        # Special handling for .vscode/settings.json - merge instead of overwrite
                                        if dest_file.name == "settings.json" and dest_file.parent.name == ".vscode":
                                            handle_vscode_settings(sub_item, dest_file, rel_path, verbose, tracker)
                                        # Skip constitution.md if it already exists (preserve user customizations)
                                        elif dest_file.name == "constitution.md" and dest_file.exists():
                                            if verbose and not tracker:
                                                console.print(f"[yellow]Preserving existing:[/yellow] {rel_path}")
                                        else:
                                            shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]Overwriting file:[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print(f"[cyan]Template files merged into current directory[/cyan]")
            else:
                zip_ref.extractall(project_path)

                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")

                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"

                    shutil.move(str(nested_dir), str(temp_move_dir))

                    project_path.rmdir()

                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "Flatten nested directory")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print(f"[cyan]Flattened nested directory structure[/cyan]")

    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]Error extracting template:[/red] {e}")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))

        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "Remove temporary archive")

        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"Cleaned up: {zip_path.name}")

    return project_path


def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Ensure POSIX .sh scripts under .specify/scripts (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / ".specify" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: list[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:
                continue
            st = script.stat(); mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400: new_mode |= 0o100
            if mode & 0o040: new_mode |= 0o010
            if mode & 0o004: new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]")
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")

@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here, or use '.' for current directory)"),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, copilot, cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, codebuddy, amp, shai, q, bob, or qoder "),
    template: str = typer.Option(None, "--template", "-t", help="[DEPRECATED] Use /speckit.constitution instead. Templates: production-saas, production-api, mobile-app, gaming, fintech, healthcare, e-commerce, minimal"),
    script_type: str = typer.Option(None, "--script", help="Script type to use: sh or ps"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
    force: bool = typer.Option(False, "--force", help="Force merge/overwrite when using --here (skip confirmation)"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"),
    debug: bool = typer.Option(False, "--debug", help="Show verbose diagnostic output for network and extraction failures"),
    github_token: str = typer.Option(None, "--github-token", help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)"),
    repo: str = typer.Option(None, "--repo", help="Custom GitHub repo to download templates from (format: 'owner/repo-name', e.g., 'myuser/spec-kit')"),
    language: str = typer.Option(None, "--language", "-l", help="Project language for artifacts: en, ru, de, fr, es, zh, ja, ko, pt, it, pl, uk, ar, hi"),
):
    """
    Initialize a new Specify project with minimal template.

    This command will:
    1. Check that required tools are installed (git is optional)
    2. Download the minimal template from GitHub
    3. Extract the template to a new project directory or current directory
    4. Initialize a fresh git repository (if not --no-git and no existing repo)

    After initialization, run /speckit.constitution to configure your project
    with interactive questions about app type, domain, and language.

    Examples:
        specify init my-project
        specify init my-project --ai claude
        specify init my-project --ai copilot --no-git
        specify init --ignore-agent-tools my-project
        specify init . --ai claude         # Initialize in current directory
        specify init --here --ai claude    # Alternative syntax for current directory
        specify init --here --force        # Skip confirmation when current directory not empty
        specify init my-project --ai claude --repo "myuser/spec-kit"  # Use custom fork
        specify init my-project --ai claude --language ru  # Set initial language
        specify init my-project -l de      # Short form for language

    Deprecated:
        --template is deprecated. Use /speckit.constitution after init instead.
    """

    show_banner()

    # Validate language if provided
    VALID_LANGUAGES = {
        "en": "English",
        "ru": "Russian",
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "pt": "Portuguese",
        "it": "Italian",
        "pl": "Polish",
        "uk": "Ukrainian",
        "ar": "Arabic",
        "hi": "Hindi",
    }

    if language and language not in VALID_LANGUAGES:
        console.print(f"[red]Error:[/red] Invalid language '[cyan]{language}[/cyan]'")
        console.print(f"Valid options: {', '.join(VALID_LANGUAGES.keys())}")
        raise typer.Exit(1)

    # Validate template if provided
    if template and template not in TEMPLATE_CHOICES:
        console.print(f"[red]Error:[/red] Invalid template '[cyan]{template}[/cyan]'")
        console.print(f"Valid options: {', '.join(TEMPLATE_CHOICES.keys())}")
        raise typer.Exit(1)

    # Template selection: default to minimal, --template is deprecated
    selected_template = template if template else "minimal"
    if template and template != "minimal":
        console.print(f"[yellow]⚠ Warning:[/yellow] --template is deprecated. Use /speckit.constitution after init to configure your project.")
        console.print(f"[dim]Template '{template}' will be applied for backward compatibility.[/dim]")

    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic

    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag")
        raise typer.Exit(1)

    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
            if force:
                console.print("[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]")
            else:
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        if project_path.exists():
            error_panel = Panel(
                f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                "Please choose a different project name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    current_dir = Path.cwd()

    setup_lines = [
        "[cyan]Specify Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]

    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")

    if repo:
        setup_lines.append(f"{'Template Repo':<15} [yellow]{repo}[/yellow]")

    if language:
        lang_name = VALID_LANGUAGES.get(language, language)
        setup_lines.append(f"{'Language':<15} [magenta]{lang_name}[/magenta] ({language})")

    if selected_template and selected_template != "minimal":
        template_desc = TEMPLATE_CHOICES.get(selected_template, selected_template)
        setup_lines.append(f"{'Template':<15} [green]{selected_template}[/green]")
        setup_lines.append(f"{'             ':<15} [dim]{template_desc}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git")
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    if ai_assistant:
        if ai_assistant not in AGENT_CONFIG:
            console.print(f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. Choose from: {', '.join(AGENT_CONFIG.keys())}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Create options dict for selection (agent_key: display_name)
        ai_choices = {key: config["name"] for key, config in AGENT_CONFIG.items()}
        selected_ai = select_with_arrows(
            ai_choices, 
            "Choose your AI assistant:", 
            "copilot"
        )

    if not ignore_agent_tools:
        agent_config = AGENT_CONFIG.get(selected_ai)
        if agent_config and agent_config["requires_cli"]:
            install_url = agent_config["install_url"]
            if not check_tool(selected_ai):
                error_panel = Panel(
                    f"[cyan]{selected_ai}[/cyan] not found\n"
                    f"Install from: [cyan]{install_url}[/cyan]\n"
                    f"{agent_config['name']} is required to continue with this project type.\n\n"
                    "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
                    title="[red]Agent Detection Error[/red]",
                    border_style="red",
                    padding=(1, 2)
                )
                console.print()
                console.print(error_panel)
                raise typer.Exit(1)

    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_script = script_type
    else:
        default_script = "ps" if os.name == "nt" else "sh"

        if sys.stdin.isatty():
            selected_script = select_with_arrows(SCRIPT_TYPE_CHOICES, "Choose script type (or press Enter)", default_script)
        else:
            selected_script = default_script

    console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
    console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")
    if selected_template != "minimal":
        console.print(f"[cyan]Selected template:[/cyan] {selected_template}")

    tracker = StepTracker("Initialize Specify Project")

    sys._specify_tracker_active = True

    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "Select AI assistant")
    tracker.complete("ai-select", f"{selected_ai}")
    tracker.add("script-select", "Select script type")
    tracker.complete("script-select", selected_script)
    tracker_steps = [
        ("fetch", "Fetch latest release"),
        ("download", "Download template"),
        ("extract", "Extract template"),
        ("zip-list", "Archive contents"),
        ("extracted-summary", "Extraction summary"),
        ("chmod", "Ensure scripts executable"),
        ("cleanup", "Cleanup"),
    ]
    # Add checklist step only for non-minimal templates
    if selected_template != "minimal":
        tracker_steps.append(("checklist", "Generate requirements checklist"))
    tracker_steps.extend([
        ("git", "Initialize git repository"),
        ("final", "Finalize")
    ])
    for key, label in tracker_steps:
        tracker.add(key, label)

    # Track git error message outside Live context so it persists
    git_error_message = None

    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            verify = not skip_tls
            local_ssl_context = ssl_context if verify else False
            local_client = httpx.Client(verify=local_ssl_context)

            download_and_extract_template(project_path, selected_ai, selected_script, here, verbose=False, tracker=tracker, client=local_client, debug=debug, github_token=github_token, repo=repo)

            ensure_executable_scripts(project_path, tracker=tracker)

            # Update constitution.md with language setting if specified
            if language:
                constitution_path = project_path / "memory" / "constitution.md"
                if constitution_path.exists():
                    try:
                        content = constitution_path.read_text(encoding="utf-8")
                        # Replace default language value in Project Settings table
                        # Pattern: | **language** | `en` | -> | **language** | `ru` |
                        pattern = r'(\| \*\*language\*\* \| `)en(` \|)'
                        replacement = rf'\g<1>{language}\g<2>'
                        updated_content = re.sub(pattern, replacement, content)
                        constitution_path.write_text(updated_content, encoding="utf-8")
                    except Exception:
                        pass  # Silently ignore if update fails

            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    success, error_msg = init_git_repo(project_path, quiet=True)
                    if success:
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                        git_error_message = error_msg
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            pass

    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")
    
    # Show git error details if initialization failed
    if git_error_message:
        console.print()
        git_error_panel = Panel(
            f"[yellow]Warning:[/yellow] Git repository initialization failed\n\n"
            f"{git_error_message}\n\n"
            f"[dim]You can initialize git manually later with:[/dim]\n"
            f"[cyan]cd {project_path if not here else '.'}[/cyan]\n"
            f"[cyan]git init[/cyan]\n"
            f"[cyan]git add .[/cyan]\n"
            f"[cyan]git commit -m \"Initial commit\"[/cyan]",
            title="[red]Git Initialization Failed[/red]",
            border_style="red",
            padding=(1, 2)
        )
        console.print(git_error_panel)

    # Agent folder security notice
    agent_config = AGENT_CONFIG.get(selected_ai)
    if agent_config:
        agent_folder = agent_config["folder"]
        security_notice = Panel(
            f"Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\n"
            f"Consider adding [cyan]{agent_folder}[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
            title="[yellow]Agent Folder Security[/yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print()
        console.print(security_notice)

    # Quick start instructions
    quick_start_lines = []
    if not here:
        quick_start_lines.append(f"[bold]1.[/bold] Go to the project folder: [cyan]cd {project_name}[/cyan]")
        step_num = 2
    else:
        quick_start_lines.append("[bold]1.[/bold] You're already in the project directory!")
        step_num = 2

    # Add Codex-specific setup step if needed
    if selected_ai == "codex":
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":  # Windows
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:  # Unix-like systems
            cmd = f"export CODEX_HOME={quoted_path}"

        quick_start_lines.append(f"[bold]{step_num}.[/bold] Set [cyan]CODEX_HOME[/cyan] environment variable: [cyan]{cmd}[/cyan]")
        step_num += 1

    quick_start_lines.append(f"[bold]{step_num}.[/bold] Start using slash commands with your AI agent")

    quick_start_panel = Panel("\n".join(quick_start_lines), title="[bold]Quick Start[/bold]", border_style="green", padding=(1, 2))
    console.print()
    console.print(quick_start_panel)

    # Show full workflow with all available commands
    console.print()
    show_workflow()

@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    tracker.add("git", "Git version control")
    git_ok = check_tool("git", tracker=tracker)

    agent_results = {}
    for agent_key, agent_config in AGENT_CONFIG.items():
        agent_name = agent_config["name"]
        requires_cli = agent_config["requires_cli"]

        tracker.add(agent_key, agent_name)

        if requires_cli:
            agent_results[agent_key] = check_tool(agent_key, tracker=tracker)
        else:
            # IDE-based agent - skip CLI check and mark as optional
            tracker.skip(agent_key, "IDE-based, no CLI check")
            agent_results[agent_key] = False  # Don't count IDE agents as "found"

    # Check VS Code variants (not in agent config)
    tracker.add("code", "Visual Studio Code")
    code_ok = check_tool("code", tracker=tracker)

    tracker.add("code-insiders", "Visual Studio Code Insiders")
    code_insiders_ok = check_tool("code-insiders", tracker=tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Specify CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")

    if not any(agent_results.values()):
        console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")

@app.command()
def version():
    """Display version and system information."""
    import platform
    import importlib.metadata
    
    show_banner()
    
    # Get CLI version from package metadata
    cli_version = "unknown"
    try:
        cli_version = importlib.metadata.version("specify-cli")
    except Exception:
        # Fallback: try reading from pyproject.toml if running from source
        try:
            import tomllib
            pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    cli_version = data.get("project", {}).get("version", "unknown")
        except Exception:
            pass
    
    # Fetch latest template release version
    repo_owner = "github"
    repo_name = "spec-kit"
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    template_version = "unknown"
    release_date = "unknown"
    
    try:
        response = client.get(
            api_url,
            timeout=10,
            follow_redirects=True,
            headers=_github_auth_headers(),
        )
        if response.status_code == 200:
            release_data = response.json()
            template_version = release_data.get("tag_name", "unknown")
            # Remove 'v' prefix if present
            if template_version.startswith("v"):
                template_version = template_version[1:]
            release_date = release_data.get("published_at", "unknown")
            if release_date != "unknown":
                # Format the date nicely
                try:
                    dt = datetime.fromisoformat(release_date.replace('Z', '+00:00'))
                    release_date = dt.strftime("%Y-%m-%d")
                except Exception:
                    pass
    except Exception:
        pass

    info_table = Table(show_header=False, box=None, padding=(0, 2))
    info_table.add_column("Key", style="cyan", justify="right")
    info_table.add_column("Value", style="white")

    info_table.add_row("CLI Version", cli_version)
    info_table.add_row("Template Version", template_version)
    info_table.add_row("Released", release_date)
    info_table.add_row("", "")
    info_table.add_row("Python", platform.python_version())
    info_table.add_row("Platform", platform.system())
    info_table.add_row("Architecture", platform.machine())
    info_table.add_row("OS Version", platform.version())

    panel = Panel(
        info_table,
        title="[bold cyan]Specify CLI Information[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    )

    console.print(panel)
    console.print()

# =============================================================================
# Workspace Commands - Multi-Repository Support
# =============================================================================

workspace_app = typer.Typer(
    name="workspace",
    help="Manage multi-repository workspaces for Spec-Driven Development",
    add_completion=False,
)


@workspace_app.command("create")
def workspace_create(
    name: str = typer.Option(None, "--name", "-n", help="Name for the workspace"),
    link_strategy: str = typer.Option(
        LINK_STRATEGY_AUTO,
        "--link-strategy", "-s",
        help=f"Link strategy: {LINK_STRATEGY_AUTO}, {LINK_STRATEGY_SYMLINK}, {LINK_STRATEGY_JUNCTION}, or {LINK_STRATEGY_PATH_REF}",
    ),
):
    """
    Create a new multi-repository workspace in the current directory.

    A workspace coordinates multiple git repositories for cross-repo
    spec-driven development. It creates a .speckit-workspace configuration
    file and a .speckit/ directory for links and cache.

    Examples:
        specify workspace create --name my-platform
        specify workspace create -n ecommerce
        specify workspace create --name myapp --link-strategy symlink
    """
    workspace_root = Path.cwd()
    config_file = workspace_root / WORKSPACE_CONFIG_FILE

    # Check if workspace already exists
    if config_file.exists():
        console.print(f"[red]Error:[/red] Workspace already exists at {workspace_root}")
        console.print(f"[dim]Config file: {config_file}[/dim]")
        raise typer.Exit(1)

    # Interactive name prompt if not provided
    if not name:
        suggested_name = workspace_root.name
        name = typer.prompt("Workspace name", default=suggested_name)

    # Resolve link strategy
    try:
        resolved_strategy = resolve_link_strategy(link_strategy)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    # Create workspace config
    config = WorkspaceConfig(
        name=name,
        version=WORKSPACE_VERSION,
        link_strategy=link_strategy,  # Store original (may be 'auto')
    )

    # Create .speckit directory structure
    speckit_dir = workspace_root / ".speckit"
    links_dir = workspace_root / WORKSPACE_LINKS_DIR
    cache_dir = workspace_root / WORKSPACE_CACHE_DIR

    try:
        speckit_dir.mkdir(exist_ok=True)
        links_dir.mkdir(parents=True, exist_ok=True)
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Save config
        config.save(workspace_root)

        console.print()
        console.print(f"[bold green]✓[/bold green] Workspace '[cyan]{name}[/cyan]' created successfully!")
        console.print()
        console.print("[dim]Created:[/dim]")
        console.print(f"  • {WORKSPACE_CONFIG_FILE}")
        console.print(f"  • {WORKSPACE_LINKS_DIR}/")
        console.print(f"  • {WORKSPACE_CACHE_DIR}/")
        console.print()
        console.print(f"[dim]Link strategy:[/dim] {resolved_strategy}" +
                      (" (auto-detected)" if link_strategy == LINK_STRATEGY_AUTO else ""))

        # Quick start for workspace
        workspace_steps = [
            "[bold]1.[/bold] Add repositories to your workspace:",
            "   [cyan]specify workspace add ./repo-path --alias myrepo --role backend[/cyan]",
            "",
            "[bold]2.[/bold] List and verify repositories:",
            "   [cyan]specify workspace list[/cyan]",
            "",
            "[bold]3.[/bold] Initialize spec-driven development in each repository:",
            "   [cyan]cd ./repo-path && specify init --here --ai <agent>[/cyan]",
        ]
        console.print()
        console.print(Panel("\n".join(workspace_steps), title="[bold]Quick Start[/bold]", border_style="green", padding=(1, 2)))

        # Show full workflow with all available commands
        console.print()
        show_workflow()

    except Exception as e:
        console.print(f"[red]Error creating workspace:[/red] {e}")
        raise typer.Exit(1)


@workspace_app.command("add")
def workspace_add(
    path: str = typer.Argument(..., help="Path to the repository to add"),
    alias: str = typer.Option(None, "--alias", "-a", help="Alias for the repository (defaults to directory name)"),
    role: str = typer.Option("other", "--role", "-r", help=f"Repository role: {', '.join(REPO_ROLES)}"),
    domain: str = typer.Option(None, "--domain", "-d", help="Business domain (e.g., payments, auth)"),
):
    """
    Add a repository to the current workspace.

    The repository path can be relative or absolute. A symbolic link
    (or equivalent based on link strategy) will be created in the
    .speckit/links/repos/ directory.

    Examples:
        specify workspace add ./backend-api --alias api --role backend
        specify workspace add ../frontend-web --alias web --role frontend
        specify workspace add /path/to/repo --alias mobile --role mobile --domain commerce
    """
    # Find workspace root
    workspace_root = find_workspace_root()
    if not workspace_root:
        console.print("[red]Error:[/red] Not inside a workspace.")
        console.print("[dim]Run 'specify workspace create' to create a workspace.[/dim]")
        raise typer.Exit(1)

    # Resolve repository path
    repo_path = Path(path).resolve()
    if not repo_path.exists():
        console.print(f"[red]Error:[/red] Repository path does not exist: {repo_path}")
        raise typer.Exit(1)

    if not repo_path.is_dir():
        console.print(f"[red]Error:[/red] Path is not a directory: {repo_path}")
        raise typer.Exit(1)

    # Check if it's a git repo
    git_dir = repo_path / ".git"
    if not git_dir.exists():
        console.print(f"[yellow]Warning:[/yellow] {repo_path} is not a git repository")

    # Default alias to directory name
    if not alias:
        alias = repo_path.name

    # Validate role
    if role not in REPO_ROLES:
        console.print(f"[red]Error:[/red] Invalid role '{role}'")
        console.print(f"[dim]Valid roles: {', '.join(REPO_ROLES)}[/dim]")
        raise typer.Exit(1)

    # Load workspace config
    try:
        config = WorkspaceConfig.load(workspace_root)
    except Exception as e:
        console.print(f"[red]Error loading workspace config:[/red] {e}")
        raise typer.Exit(1)

    # Check if alias already exists
    if alias in config.repositories:
        console.print(f"[red]Error:[/red] Repository with alias '{alias}' already exists")
        console.print(f"[dim]Current path: {config.repositories[alias].path}[/dim]")
        raise typer.Exit(1)

    # Create relative path from workspace root
    try:
        relative_path = repo_path.relative_to(workspace_root)
        path_str = f"./{relative_path}"
    except ValueError:
        # Path is outside workspace, use absolute
        path_str = str(repo_path)

    # Add repository to config
    repo_config = RepoConfig(
        path=path_str,
        alias=alias,
        role=role,
        domain=domain,
    )
    config.repositories[alias] = repo_config

    # Create link based on strategy
    resolved_strategy = resolve_link_strategy(config.link_strategy)
    links_dir = workspace_root / WORKSPACE_LINKS_DIR
    link_path = links_dir / alias

    try:
        # Remove existing link if present
        if link_path.exists() or link_path.is_symlink():
            if link_path.is_symlink() or (os.name == "nt" and link_path.is_dir()):
                if os.name == "nt":
                    # Windows: might be a junction
                    os.rmdir(str(link_path))
                else:
                    link_path.unlink()
            else:
                shutil.rmtree(link_path)

        # Create link based on strategy
        if resolved_strategy == LINK_STRATEGY_SYMLINK:
            link_path.symlink_to(repo_path, target_is_directory=True)
        elif resolved_strategy == LINK_STRATEGY_JUNCTION:
            # Windows junction
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link_path), str(repo_path)],
                check=True,
                capture_output=True,
            )
        elif resolved_strategy == LINK_STRATEGY_PATH_REF:
            # Create a .path file with the absolute path
            path_ref_file = links_dir / f"{alias}.path"
            path_ref_file.write_text(str(repo_path), encoding="utf-8")

        # Save updated config
        config.save(workspace_root)

        console.print()
        console.print(f"[bold green]✓[/bold green] Added repository '[cyan]{alias}[/cyan]' to workspace")
        console.print()
        console.print(f"  [dim]Path:[/dim]   {path_str}")
        console.print(f"  [dim]Role:[/dim]   {role}")
        if domain:
            console.print(f"  [dim]Domain:[/dim] {domain}")
        console.print(f"  [dim]Link:[/dim]   {resolved_strategy}")
        console.print()

    except Exception as e:
        console.print(f"[red]Error adding repository:[/red] {e}")
        raise typer.Exit(1)


@workspace_app.command("remove")
def workspace_remove(
    alias: str = typer.Argument(..., help="Alias of the repository to remove"),
    keep_link: bool = typer.Option(False, "--keep-link", help="Keep the symlink/junction (only remove from config)"),
):
    """
    Remove a repository from the current workspace.

    This removes the repository from the workspace configuration and
    deletes the link in .speckit/links/repos/. The actual repository
    files are NOT deleted.

    Examples:
        specify workspace remove api
        specify workspace remove web --keep-link
    """
    # Find workspace root
    workspace_root = find_workspace_root()
    if not workspace_root:
        console.print("[red]Error:[/red] Not inside a workspace.")
        raise typer.Exit(1)

    # Load workspace config
    try:
        config = WorkspaceConfig.load(workspace_root)
    except Exception as e:
        console.print(f"[red]Error loading workspace config:[/red] {e}")
        raise typer.Exit(1)

    # Check if alias exists
    if alias not in config.repositories:
        console.print(f"[red]Error:[/red] No repository with alias '{alias}' found")
        console.print("[dim]Run 'specify workspace list' to see available repositories[/dim]")
        raise typer.Exit(1)

    # Get repo info before removing
    repo = config.repositories[alias]

    # Remove from config
    del config.repositories[alias]

    # Remove cross-dependencies involving this repo
    config.cross_dependencies = [
        dep for dep in config.cross_dependencies
        if not (dep.source.startswith(f"{alias}:") or dep.target.startswith(f"{alias}:"))
    ]

    # Remove link unless --keep-link
    links_dir = workspace_root / WORKSPACE_LINKS_DIR
    link_path = links_dir / alias
    path_ref_file = links_dir / f"{alias}.path"

    if not keep_link:
        try:
            if link_path.exists() or link_path.is_symlink():
                if link_path.is_symlink() or (os.name == "nt" and link_path.is_dir()):
                    if os.name == "nt":
                        os.rmdir(str(link_path))
                    else:
                        link_path.unlink()
            if path_ref_file.exists():
                path_ref_file.unlink()
        except Exception as e:
            console.print(f"[yellow]Warning:[/yellow] Could not remove link: {e}")

    # Save updated config
    try:
        config.save(workspace_root)
    except Exception as e:
        console.print(f"[red]Error saving config:[/red] {e}")
        raise typer.Exit(1)

    console.print()
    console.print(f"[bold green]✓[/bold green] Removed repository '[cyan]{alias}[/cyan]' from workspace")
    console.print(f"  [dim]Was at:[/dim] {repo.path}")
    if keep_link:
        console.print(f"  [dim]Link kept at:[/dim] {link_path}")
    console.print()


@workspace_app.command("list")
def workspace_list(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information"),
):
    """
    List all repositories in the current workspace.

    Shows repository aliases, paths, roles, and link status.
    Use --verbose for additional details including domains and
    cross-dependencies.

    Examples:
        specify workspace list
        specify workspace list --verbose
    """
    # Find workspace root
    workspace_root = find_workspace_root()
    if not workspace_root:
        console.print("[red]Error:[/red] Not inside a workspace.")
        console.print("[dim]Run 'specify workspace create' to create a workspace.[/dim]")
        raise typer.Exit(1)

    # Load workspace config
    try:
        config = WorkspaceConfig.load(workspace_root)
    except Exception as e:
        console.print(f"[red]Error loading workspace config:[/red] {e}")
        raise typer.Exit(1)

    console.print()
    console.print(f"[bold cyan]Workspace:[/bold cyan] {config.name}")
    console.print(f"[dim]Location:[/dim] {workspace_root}")
    console.print(f"[dim]Link strategy:[/dim] {config.link_strategy}")
    console.print()

    if not config.repositories:
        console.print("[dim]No repositories added yet.[/dim]")
        console.print("[dim]Run 'specify workspace add <path>' to add a repository.[/dim]")
        return

    # Create table for repositories
    table = Table(title="Repositories", show_header=True, header_style="bold")
    table.add_column("Alias", style="cyan")
    table.add_column("Role", style="green")
    table.add_column("Path")
    table.add_column("Status")

    if verbose:
        table.add_column("Domain", style="dim")

    links_dir = workspace_root / WORKSPACE_LINKS_DIR

    for alias, repo in config.repositories.items():
        # Resolve path and check existence
        if repo.path.startswith("./") or repo.path.startswith("../"):
            resolved_path = (workspace_root / repo.path).resolve()
        else:
            resolved_path = Path(repo.path)

        # Check link status
        link_path = links_dir / alias
        path_ref = links_dir / f"{alias}.path"

        if link_path.exists() or link_path.is_symlink():
            status = "[green]linked[/green]"
        elif path_ref.exists():
            status = "[blue]path-ref[/blue]"
        elif resolved_path.exists():
            status = "[yellow]unlinked[/yellow]"
        else:
            status = "[red]missing[/red]"

        row = [alias, repo.role, repo.path, status]
        if verbose:
            row.append(repo.domain or "-")

        table.add_row(*row)

    console.print(table)

    # Show cross-dependencies in verbose mode
    if verbose and config.cross_dependencies:
        console.print()
        deps_table = Table(title="Cross-Repository Dependencies", show_header=True, header_style="bold")
        deps_table.add_column("Source", style="cyan")
        deps_table.add_column("Type", style="yellow")
        deps_table.add_column("Target", style="green")

        for dep in config.cross_dependencies:
            deps_table.add_row(dep.source, dep.dep_type, dep.target)

        console.print(deps_table)

    console.print()


@workspace_app.command("sync")
def workspace_sync(
    force: bool = typer.Option(False, "--force", "-f", help="Force re-creation of all links"),
):
    """
    Synchronize workspace links with the configuration.

    This command ensures that all repositories in the workspace
    configuration have corresponding links in .speckit/links/repos/.
    Use --force to recreate all links.

    Examples:
        specify workspace sync
        specify workspace sync --force
    """
    # Find workspace root
    workspace_root = find_workspace_root()
    if not workspace_root:
        console.print("[red]Error:[/red] Not inside a workspace.")
        raise typer.Exit(1)

    # Load workspace config
    try:
        config = WorkspaceConfig.load(workspace_root)
    except Exception as e:
        console.print(f"[red]Error loading workspace config:[/red] {e}")
        raise typer.Exit(1)

    resolved_strategy = resolve_link_strategy(config.link_strategy)
    links_dir = workspace_root / WORKSPACE_LINKS_DIR
    links_dir.mkdir(parents=True, exist_ok=True)

    console.print()
    console.print(f"[bold cyan]Syncing workspace:[/bold cyan] {config.name}")
    console.print(f"[dim]Strategy:[/dim] {resolved_strategy}")
    console.print()

    synced = 0
    skipped = 0
    errors = 0

    for alias, repo in config.repositories.items():
        # Resolve repo path
        if repo.path.startswith("./") or repo.path.startswith("../"):
            repo_path = (workspace_root / repo.path).resolve()
        else:
            repo_path = Path(repo.path)

        link_path = links_dir / alias
        path_ref = links_dir / f"{alias}.path"

        # Check if repo exists
        if not repo_path.exists():
            console.print(f"  [red]✗[/red] {alias}: repository not found at {repo_path}")
            errors += 1
            continue

        # Check if link already exists and is valid
        if not force:
            if resolved_strategy == LINK_STRATEGY_PATH_REF:
                if path_ref.exists():
                    existing_path = path_ref.read_text(encoding="utf-8").strip()
                    if existing_path == str(repo_path):
                        console.print(f"  [dim]○[/dim] {alias}: already synced")
                        skipped += 1
                        continue
            elif link_path.exists() or link_path.is_symlink():
                try:
                    if link_path.resolve() == repo_path:
                        console.print(f"  [dim]○[/dim] {alias}: already synced")
                        skipped += 1
                        continue
                except Exception:
                    pass  # Link is broken, will recreate

        # Create or recreate link
        try:
            # Remove existing link/path-ref
            if link_path.exists() or link_path.is_symlink():
                if link_path.is_symlink() or (os.name == "nt" and link_path.is_dir()):
                    if os.name == "nt":
                        os.rmdir(str(link_path))
                    else:
                        link_path.unlink()
            if path_ref.exists():
                path_ref.unlink()

            # Create new link
            if resolved_strategy == LINK_STRATEGY_SYMLINK:
                link_path.symlink_to(repo_path, target_is_directory=True)
            elif resolved_strategy == LINK_STRATEGY_JUNCTION:
                subprocess.run(
                    ["cmd", "/c", "mklink", "/J", str(link_path), str(repo_path)],
                    check=True,
                    capture_output=True,
                )
            elif resolved_strategy == LINK_STRATEGY_PATH_REF:
                path_ref.write_text(str(repo_path), encoding="utf-8")

            console.print(f"  [green]✓[/green] {alias}: synced")
            synced += 1

        except Exception as e:
            console.print(f"  [red]✗[/red] {alias}: {e}")
            errors += 1

    # Generate unified manifest cache
    cache_dir = workspace_root / WORKSPACE_CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "workspace": config.name,
        "version": config.version,
        "repositories": {
            alias: {
                "path": repo.path,
                "role": repo.role,
                "domain": repo.domain,
            }
            for alias, repo in config.repositories.items()
        },
        "cross_dependencies": [dep.to_dict() for dep in config.cross_dependencies],
    }

    manifest_path = cache_dir / "unified-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    console.print()
    console.print(f"[bold]Summary:[/bold] {synced} synced, {skipped} skipped, {errors} errors")
    console.print(f"[dim]Manifest updated:[/dim] {manifest_path.relative_to(workspace_root)}")
    console.print()


# Register workspace commands with main app
app.add_typer(workspace_app, name="workspace")


# =============================================================================
# ORCHESTRATE COMMAND - Parallel Agent Execution
# =============================================================================

@app.command()
def orchestrate(
    command: str = typer.Argument(
        ...,
        help="Command template to orchestrate (e.g., 'implement', 'plan')"
    ),
    feature: str = typer.Argument(
        ...,
        help="Feature directory (e.g., '001-user-auth')"
    ),
    pool_size: int = typer.Option(
        4,
        "--pool-size", "-p",
        help="Number of parallel agents (1-8)",
        min=1,
        max=8,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show execution plan without running agents"
    ),
    sequential: bool = typer.Option(
        False,
        "--sequential",
        help="Disable wave overlap (run waves one at a time)"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Show detailed progress and agent outputs"
    ),
):
    """
    Execute a speckit command with parallel agent orchestration.

    This command parses subagent definitions from command templates and
    executes them in parallel using the Anthropic API, respecting dependencies
    and wave-based scheduling.

    Requires ANTHROPIC_API_KEY environment variable to be set.

    Examples:

        specify orchestrate implement 001-user-auth

        specify orchestrate implement 001-user-auth --pool-size 4

        specify orchestrate implement 001-user-auth --dry-run

        specify orchestrate plan 002-payments --sequential
    """
    import asyncio

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and not dry_run:
        console.print("[bold red]Error:[/bold red] ANTHROPIC_API_KEY environment variable is required")
        console.print("[dim]Set it with: export ANTHROPIC_API_KEY=your-key-here[/dim]")
        raise typer.Exit(1)

    # Find template
    template_candidates = [
        Path(".specify/templates/commands") / f"{command}.md",
        Path(".specify/templates/commands") / f"speckit.{command}.md",
        Path("templates/commands") / f"{command}.md",
    ]

    template_path = None
    for candidate in template_candidates:
        if candidate.exists():
            template_path = candidate
            break

    if template_path is None:
        console.print(f"[bold red]Error:[/bold red] Template not found for command: {command}")
        console.print("[dim]Searched:[/dim]")
        for c in template_candidates:
            console.print(f"  - {c}")
        raise typer.Exit(1)

    console.print(f"[bold]Orchestrate:[/bold] {command}")
    console.print(f"[dim]Template:[/dim] {template_path}")
    console.print(f"[dim]Feature:[/dim] {feature}")
    console.print()

    # Import orchestration modules
    try:
        from .template_parser import parse_subagents_from_template, get_wave_config_from_template
        from .agent_pool import DistributedAgentPool
        from .wave_scheduler import WaveScheduler, WaveConfig, ExecutionStrategy
    except ImportError as e:
        console.print(f"[bold red]Error:[/bold red] Failed to import orchestration modules: {e}")
        console.print("[dim]Ensure anthropic and tenacity are installed: pip install anthropic tenacity[/dim]")
        raise typer.Exit(1)

    # Parse template
    try:
        tasks = parse_subagents_from_template(template_path, feature)
        wave_config = get_wave_config_from_template(template_path)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to parse template: {e}")
        raise typer.Exit(1)

    if not tasks:
        console.print("[bold yellow]Warning:[/bold yellow] No parallel subagents found in template")
        console.print("[dim]This command template may not support parallel execution[/dim]")
        raise typer.Exit(0)

    # Override config with CLI options
    wave_config.max_parallel = pool_size
    if sequential:
        wave_config.strategy = ExecutionStrategy.SEQUENTIAL
        wave_config.overlap_enabled = False

    # Show execution plan
    console.print(f"[bold cyan]Execution Plan[/bold cyan] ({len(tasks)} agents)")
    console.print()

    # Build waves for display
    pool = DistributedAgentPool(pool_size=pool_size) if not dry_run else None
    scheduler = WaveScheduler(pool, wave_config) if pool else WaveScheduler(None, wave_config)

    try:
        waves = scheduler.build_waves(tasks)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

    # Display waves
    wave_table = Table(show_header=True, header_style="bold cyan", box=None)
    wave_table.add_column("Wave", style="cyan", width=8)
    wave_table.add_column("Agents", style="white")
    wave_table.add_column("Model", style="dim")

    for wave in waves:
        agent_names = ", ".join(t.name for t in wave.tasks)
        models = set(t.model.split("-")[1] if "-" in t.model else t.model for t in wave.tasks)
        wave_table.add_row(f"{wave.index + 1}", agent_names, "/".join(models))

    console.print(wave_table)
    console.print()

    if dry_run:
        console.print("[bold yellow]Dry run mode[/bold yellow] - no agents executed")
        console.print()
        console.print("[dim]Strategy:[/dim]", wave_config.strategy.value)
        console.print("[dim]Pool size:[/dim]", pool_size)
        console.print("[dim]Overlap:[/dim]", "enabled" if wave_config.overlap_enabled else "disabled")
        if wave_config.overlap_enabled:
            console.print("[dim]Threshold:[/dim]", f"{wave_config.overlap_threshold:.0%}")
        return

    # Execute
    console.print("[bold]Executing agents...[/bold]")
    console.print()

    # Initialize task status updater
    tasks_md_path = None
    cwd = Path.cwd()

    # Strategy 1: Look in specs/[feature]/ directory structure
    spec_dirs = list(cwd.glob("specs/*/tasks.md"))
    if spec_dirs:
        tasks_md_path = spec_dirs[0]
    else:
        # Strategy 2: Look in current directory
        if (cwd / "tasks.md").exists():
            tasks_md_path = cwd / "tasks.md"

    # Initialize updater if found
    task_updater = TaskStatusUpdater(str(tasks_md_path)) if tasks_md_path else None

    if not task_updater:
        console.print("[yellow]Warning:[/yellow] tasks.md not found. Task status updates disabled.")
        console.print()

    async def run_orchestration():
        # Set up progress tracking
        completed_count = 0
        total_count = len(tasks)

        def on_task_complete(name: str, result):
            nonlocal completed_count
            completed_count += 1
            status = "[green]OK[/green]" if result.success else "[red]FAIL[/red]"
            duration = f"{result.duration_ms}ms"
            tokens = f"{result.tokens_in + result.tokens_out} tokens"
            console.print(f"  [{completed_count}/{total_count}] {name}: {status} ({duration}, {tokens})")

            if verbose and result.output:
                # Show first 200 chars of output
                preview = result.output[:200] + "..." if len(result.output) > 200 else result.output
                console.print(f"    [dim]{preview}[/dim]")

            # Automatically update tasks.md
            if task_updater:
                try:
                    # Read file to find task ID mapping
                    with open(task_updater.tasks_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    task_id = task_updater.find_task_id_from_name(name, content)

                    if task_id:
                        task_update = TaskUpdate(
                            task_id=task_id,
                            task_name=name,
                            success=result.success,
                            error_message=result.error if not result.success else None,
                            duration_ms=result.duration_ms
                        )

                        success, error = task_updater.update_task_status(task_update)

                        if success:
                            checkbox = "[x]" if result.success else "[!]"
                            console.print(f"    [dim]Updated tasks.md: {task_id} → {checkbox}[/dim]")
                        else:
                            console.print(f"    [yellow]Warning:[/yellow] Could not update tasks.md: {error}")
                    else:
                        if verbose:
                            console.print(f"    [dim]Could not map '{name}' to task ID in tasks.md[/dim]")
                except Exception as e:
                    # Don't crash execution if update fails
                    console.print(f"    [yellow]Warning:[/yellow] Task update failed: {e}")

        def on_wave_complete(wave):
            if verbose:
                console.print(f"  [dim]Wave {wave.index + 1} complete: {len(wave.completed)} succeeded, {len(wave.failed)} failed[/dim]")

        scheduler.on_task_complete(on_task_complete)
        scheduler.on_wave_complete(on_wave_complete)

        try:
            results = await scheduler.execute_all(tasks)
            return results
        finally:
            if pool:
                await pool.close()

    try:
        results = asyncio.run(run_orchestration())
    except RuntimeError as e:
        console.print(f"[bold red]Execution failed:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        raise typer.Exit(1)

    # Summary
    console.print()
    success_count = sum(1 for r in results.values() if r.success)
    fail_count = len(results) - success_count
    total_duration = sum(r.duration_ms for r in results.values())
    total_tokens = sum(r.tokens_in + r.tokens_out for r in results.values())

    if fail_count == 0:
        console.print(f"[bold green]Completed {success_count} agents[/bold green] in {total_duration}ms ({total_tokens} tokens)")
    else:
        console.print(f"[bold yellow]Completed {success_count} agents, {fail_count} failed[/bold yellow] in {total_duration}ms")
        for name, result in results.items():
            if not result.success:
                console.print(f"  [red]FAILED:[/red] {name}: {result.error}")


def main():
    app()

if __name__ == "__main__":
    main()


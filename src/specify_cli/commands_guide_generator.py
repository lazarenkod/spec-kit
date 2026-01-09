"""
Auto-generator for COMMANDS_GUIDE.md documentation.

This module scans command templates from templates/commands/*.md,
extracts metadata from YAML frontmatter and flag definitions from content,
and generates a comprehensive COMMANDS_GUIDE.md documentation file.

Usage:
    python -m specify_cli.commands_guide_generator

Or from code:
    from specify_cli.commands_guide_generator import generate_commands_guide
    generate_commands_guide()
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class CommandFlag:
    """Represents a CLI flag for a command."""
    name: str           # --autonomous
    alias: Optional[str] = None  # --auto
    description: str = ""
    default: Optional[str] = None

    def __str__(self) -> str:
        if self.alias:
            return f"`{self.name}` / `{self.alias}`"
        return f"`{self.name}`"


@dataclass
class CommandMetadata:
    """Parsed metadata from a command template."""
    name: str                    # implement
    description: str             # Description from frontmatter
    model: str = "sonnet"        # opus/sonnet/haiku
    thinking_budget: int = 8000
    flags: List[CommandFlag] = field(default_factory=list)
    arguments: List[str] = field(default_factory=list)
    handoffs: List[str] = field(default_factory=list)
    pre_gates: List[str] = field(default_factory=list)
    quality_gates: List[str] = field(default_factory=list)
    output_files: List[str] = field(default_factory=list)
    persona: Optional[str] = None
    requires: List[str] = field(default_factory=list)


def parse_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """
    Extract YAML frontmatter from template content.

    Args:
        content: Full template file content

    Returns:
        Parsed YAML dict or None if no frontmatter found
    """
    if not content.startswith("---"):
        return None

    lines = content.split("\n")
    end_idx = None

    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None

    frontmatter_text = "\n".join(lines[1:end_idx])

    try:
        return yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return None


def extract_flags_from_content(content: str) -> List[CommandFlag]:
    """
    Extract flags from markdown content using multiple patterns.

    Patterns:
    1. "Parse arguments for:" lists with `--flag` items
    2. CLI Flags tables: | `--flag` | description |
    3. Inline `--flag` mentions with descriptions
    4. pre_gates skip_flag and fast_flag references

    Args:
        content: Markdown content after frontmatter

    Returns:
        List of extracted CommandFlag objects
    """
    flags: List[CommandFlag] = []
    seen_flags: set = set()

    # Pattern 1: Parse arguments for sections
    # Example: - `--services <list>`: Override default services
    parse_args_pattern = r'-\s*`(--[\w-]+(?:\s+<[\w-]+>)?)`[:\s]*([^\n]+)'
    for match in re.finditer(parse_args_pattern, content):
        flag_full = match.group(1).strip()
        description = match.group(2).strip()

        # Extract just the flag name (without <arg>)
        flag_name = re.match(r'(--[\w-]+)', flag_full)
        if flag_name:
            name = flag_name.group(1)
            if name not in seen_flags:
                flags.append(CommandFlag(
                    name=name,
                    description=description
                ))
                seen_flags.add(name)

    # Pattern 2: CLI Flags table
    # Example: | `--autonomous` | Run without user prompts |
    table_pattern = r'\|\s*`(--[\w-]+)`\s*\|\s*([^|]+)\s*\|'
    for match in re.finditer(table_pattern, content):
        name = match.group(1).strip()
        description = match.group(2).strip()
        if name not in seen_flags:
            flags.append(CommandFlag(
                name=name,
                description=description
            ))
            seen_flags.add(name)

    # Pattern 3: Inline flag definitions
    # Example: `--skip-pre-gates` - skip pre-implementation gates
    inline_pattern = r'`(--[\w-]+)`\s*[-–:]\s*([^`\n]+?)(?=\n|$|`)'
    for match in re.finditer(inline_pattern, content):
        name = match.group(1).strip()
        description = match.group(2).strip()
        if name not in seen_flags and len(description) > 5:
            flags.append(CommandFlag(
                name=name,
                description=description
            ))
            seen_flags.add(name)

    return flags


def extract_flags_from_frontmatter(frontmatter: Dict[str, Any]) -> List[CommandFlag]:
    """
    Extract flags defined in YAML frontmatter.

    Looks for:
    - autonomous_mode.flag / autonomous_mode.alias
    - pre_gates.skip_flag / pre_gates.fast_flag
    - Any other explicit flag definitions

    Args:
        frontmatter: Parsed YAML frontmatter dict

    Returns:
        List of CommandFlag objects
    """
    flags: List[CommandFlag] = []
    seen_flags: set = set()

    # autonomous_mode config
    auto_mode = frontmatter.get("autonomous_mode", {})
    if auto_mode and isinstance(auto_mode, dict):
        flag = auto_mode.get("flag")
        if flag and flag not in seen_flags:
            flags.append(CommandFlag(
                name=flag,
                alias=auto_mode.get("alias"),
                description=auto_mode.get("description", "Run autonomously without user prompts")
            ))
            seen_flags.add(flag)

    # pre_gates flags
    pre_gates = frontmatter.get("pre_gates", {})
    if pre_gates and isinstance(pre_gates, dict):
        skip_flag = pre_gates.get("skip_flag")
        if skip_flag and skip_flag not in seen_flags:
            flags.append(CommandFlag(
                name=skip_flag,
                description="Skip pre-implementation gates"
            ))
            seen_flags.add(skip_flag)

        fast_flag = pre_gates.get("fast_flag")
        if fast_flag and fast_flag not in seen_flags:
            flags.append(CommandFlag(
                name=fast_flag,
                description="Fast mode - run only Tier 1-2 validation"
            ))
            seen_flags.add(fast_flag)

    # execution_mode overrides
    exec_mode = frontmatter.get("execution_mode", {})
    if exec_mode and isinstance(exec_mode, dict):
        override_flag = exec_mode.get("override_flag")
        if override_flag and override_flag not in seen_flags:
            flags.append(CommandFlag(
                name=override_flag,
                description="Override execution mode"
            ))
            seen_flags.add(override_flag)

    # claude_code adaptive model override flag
    claude_code = frontmatter.get("claude_code", {})
    adaptive = claude_code.get("adaptive_model", {})
    if adaptive and isinstance(adaptive, dict):
        override_flag = adaptive.get("override_flag")
        if override_flag and override_flag not in seen_flags:
            flags.append(CommandFlag(
                name=override_flag,
                description="Override model selection"
            ))
            seen_flags.add(override_flag)

    return flags


def extract_handoffs(frontmatter: Dict[str, Any]) -> List[str]:
    """Extract handoff target commands from frontmatter."""
    handoffs = frontmatter.get("handoffs", [])
    if not handoffs:
        return []

    targets = []
    for h in handoffs:
        if isinstance(h, dict):
            agent = h.get("agent", "")
            if agent:
                targets.append(agent)
    return targets


def extract_gates(frontmatter: Dict[str, Any]) -> tuple[List[str], List[str]]:
    """Extract pre_gates and quality_gates names from frontmatter."""
    pre_gates: List[str] = []
    quality_gates: List[str] = []

    # Pre-gates
    pg = frontmatter.get("pre_gates", {})
    if isinstance(pg, dict):
        gates = pg.get("gates", [])
        for gate in gates:
            if isinstance(gate, dict):
                name = gate.get("name", "")
                if name:
                    pre_gates.append(name)
    elif isinstance(pg, list):
        for gate in pg:
            if isinstance(gate, dict):
                name = gate.get("name", "")
                if name:
                    pre_gates.append(name)

    # Quality gates from handoffs
    handoffs = frontmatter.get("handoffs", [])
    for h in handoffs:
        if isinstance(h, dict):
            gates = h.get("gates", [])
            for gate in gates:
                if isinstance(gate, dict):
                    name = gate.get("name", "")
                    if name:
                        quality_gates.append(name)

    return pre_gates, quality_gates


def extract_output_files(content: str) -> List[str]:
    """Extract output file patterns from content."""
    outputs: List[str] = []
    seen: set = set()

    # Pattern: Output/Outputs: lists
    output_pattern = r'(?:Output|Outputs|Generates):\s*\n((?:\s*-[^\n]+\n?)+)'
    for match in re.finditer(output_pattern, content, re.IGNORECASE):
        block = match.group(1)
        for line in block.split('\n'):
            line = line.strip().lstrip('- ')
            # Extract file paths
            file_match = re.search(r'[.\w/-]+\.(md|yaml|yml|json|env|txt)', line)
            if file_match:
                path = file_match.group(0)
                if path not in seen:
                    outputs.append(path)
                    seen.add(path)

    return outputs


def parse_command_template(path: Path) -> CommandMetadata:
    """
    Parse a command template and extract all metadata.

    Args:
        path: Path to the template .md file

    Returns:
        CommandMetadata with extracted information
    """
    content = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(content)

    if frontmatter is None:
        frontmatter = {}

    # Extract command name from filename
    name = path.stem
    if name.endswith(".COMPRESSED"):
        name = name.replace(".COMPRESSED", "")
    # Strip speckit. prefix if present (e.g., speckit.merge.md -> merge)
    if name.startswith("speckit."):
        name = name[8:]

    # Basic metadata
    description = frontmatter.get("description", "")
    persona = frontmatter.get("persona")

    # Claude Code settings
    claude_code = frontmatter.get("claude_code", {})
    model = claude_code.get("model", "sonnet")
    thinking_budget = claude_code.get("thinking_budget", 8000)

    # Extract flags from both sources
    flags_from_content = extract_flags_from_content(content)
    flags_from_frontmatter = extract_flags_from_frontmatter(frontmatter)

    # Merge flags (frontmatter takes precedence)
    flags_dict = {f.name: f for f in flags_from_content}
    for f in flags_from_frontmatter:
        flags_dict[f.name] = f

    # Handoffs
    handoffs = extract_handoffs(frontmatter)

    # Gates
    pre_gates, quality_gates = extract_gates(frontmatter)

    # Output files
    output_files = extract_output_files(content)

    # Requirements
    requires: List[str] = []
    handoff_config = frontmatter.get("handoff", {})
    if isinstance(handoff_config, dict):
        req = handoff_config.get("requires")
        if req:
            requires.append(req)

    return CommandMetadata(
        name=name,
        description=description,
        model=model,
        thinking_budget=thinking_budget,
        flags=list(flags_dict.values()),
        handoffs=handoffs,
        pre_gates=pre_gates,
        quality_gates=quality_gates,
        output_files=output_files,
        persona=persona,
        requires=requires,
    )


def generate_commands_guide(
    commands: List[CommandMetadata],
    version: str = "1.5.0"
) -> str:
    """
    Generate COMMANDS_GUIDE.md content from command metadata.

    Args:
        commands: List of parsed CommandMetadata
        version: Documentation version

    Returns:
        Generated markdown content
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Sort commands by workflow order
    workflow_order = [
        "constitution", "concept", "validate-concept", "specify", "clarify",
        "design", "plan", "tasks", "taskstoissues", "staging", "analyze",
        "implement", "preview", "list", "switch", "extend", "merge",
        "baseline", "checklist", "discover", "integrate", "monitor", "launch", "ship",
        "concept-variants", "migrate", "properties"  # Additional/specialized commands
    ]

    def sort_key(cmd: CommandMetadata) -> int:
        try:
            return workflow_order.index(cmd.name)
        except ValueError:
            return 999

    commands = sorted(commands, key=sort_key)

    lines = [
        "# Spec-Kit Commands Guide",
        "",
        "<!-- AUTO-GENERATED - DO NOT EDIT MANUALLY -->",
        f"<!-- Generated at: {now} -->",
        "<!-- Source: templates/commands/*.md -->",
        "",
        "Полное руководство по командам Spec Kit для Spec-Driven Development.",
        "",
        "---",
        "",
        "## Содержание",
        "",
    ]

    # Generate TOC
    for i, cmd in enumerate(commands, 1):
        lines.append(f"- [{i}. /speckit.{cmd.name}](#speckit{cmd.name})")

    lines.extend([
        "",
        "---",
        "",
        "## Основной Workflow",
        "",
        "```mermaid",
        "graph LR",
        "    A[constitution] --> B[concept]",
        "    B --> C[specify]",
        "    C --> D[plan]",
        "    D --> E[tasks]",
        "    E --> F[staging]",
        "    F --> G[implement]",
        "    G --> H[analyze]",
        "```",
        "",
        "---",
        "",
        "## Детальное описание команд",
        "",
    ])

    # Generate command sections
    for i, cmd in enumerate(commands, 1):
        anchor = f"speckit{cmd.name}"
        lines.extend([
            f"### {i}. `/speckit.{cmd.name}` {{#{anchor}}}",
            "",
            f"**Назначение:** {cmd.description}",
            "",
            f"**Модель:** `{cmd.model}` (thinking_budget: {cmd.thinking_budget})",
            "",
        ])

        if cmd.persona:
            lines.append(f"**Persona:** `{cmd.persona}`")
            lines.append("")

        if cmd.requires:
            lines.append(f"**Требует:** {', '.join(cmd.requires)}")
            lines.append("")

        # Flags (only include flags with descriptions)
        flags_with_desc = [f for f in cmd.flags if f.description.strip()]
        if flags_with_desc:
            lines.append("**Флаги:**")
            lines.append("")
            for flag in flags_with_desc:
                if flag.alias:
                    lines.append(f"- `{flag.name}` / `{flag.alias}` — {flag.description.strip()}")
                else:
                    lines.append(f"- `{flag.name}` — {flag.description.strip()}")
            lines.append("")

        # Pre-gates
        if cmd.pre_gates:
            lines.append("**Pre-Gates:**")
            lines.append("")
            for gate in cmd.pre_gates[:5]:  # Limit to 5
                lines.append(f"- {gate}")
            if len(cmd.pre_gates) > 5:
                lines.append(f"- ... и ещё {len(cmd.pre_gates) - 5}")
            lines.append("")

        # Quality gates
        if cmd.quality_gates:
            lines.append("**Quality Gates:**")
            lines.append("")
            for gate in cmd.quality_gates[:5]:
                lines.append(f"- {gate}")
            if len(cmd.quality_gates) > 5:
                lines.append(f"- ... и ещё {len(cmd.quality_gates) - 5}")
            lines.append("")

        # Handoffs
        if cmd.handoffs:
            lines.append("**Handoffs:**")
            lines.append("")
            for h in cmd.handoffs:
                lines.append(f"- → `/{h}`")
            lines.append("")

        # Output files
        if cmd.output_files:
            lines.append("**Выходные файлы:**")
            lines.append("")
            for f in cmd.output_files[:5]:
                lines.append(f"- `{f}`")
            if len(cmd.output_files) > 5:
                lines.append(f"- ... и ещё {len(cmd.output_files) - 5}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Quick reference table
    lines.extend([
        "## Quick Reference",
        "",
        "### Команды по категориям",
        "",
        "| Категория | Команды |",
        "|-----------|---------|",
        "| Foundation | `/speckit.constitution` |",
        "| Discovery | `/speckit.concept`, `/speckit.validate-concept`, `/speckit.discover` |",
        "| Specification | `/speckit.specify`, `/speckit.clarify`, `/speckit.design` |",
        "| Planning | `/speckit.plan`, `/speckit.tasks`, `/speckit.taskstoissues` |",
        "| Implementation | `/speckit.staging`, `/speckit.implement`, `/speckit.preview` |",
        "| Quality | `/speckit.analyze`, `/speckit.checklist` |",
        "| Navigation | `/speckit.list`, `/speckit.switch`, `/speckit.extend`, `/speckit.merge` |",
        "| Operations | `/speckit.baseline`, `/speckit.integrate`, `/speckit.monitor`, `/speckit.launch`, `/speckit.ship` |",
        "",
    ])

    # Flags quick reference (only flags with descriptions)
    all_flags = []
    for cmd in commands:
        for flag in cmd.flags:
            if flag.description.strip():
                all_flags.append((cmd.name, flag))

    if all_flags:
        lines.extend([
            "### Флаги команд",
            "",
            "| Команда | Флаг | Описание |",
            "|---------|------|----------|",
        ])
        for cmd_name, flag in all_flags:
            flag_str = f"`{flag.name}`"
            if flag.alias:
                flag_str += f" / `{flag.alias}`"
            desc = flag.description.strip()
            # Escape markdown characters in table cell to prevent nesting issues
            desc = desc.replace('`', '\\`').replace('|', '\\|')
            desc_truncated = f"{desc[:50]}..." if len(desc) > 50 else desc
            lines.append(f"| `/speckit.{cmd_name}` | {flag_str} | {desc_truncated} |")
        lines.append("")

    # Version info
    lines.extend([
        "---",
        "",
        "## Версия документа",
        "",
        f"**Версия:** {version}",
        f"**Дата генерации:** {now}",
        "**Автор:** Auto-generated from command templates",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    """
    CLI entrypoint for generating COMMANDS_GUIDE.md.

    Scans templates/commands/*.md and generates docs/COMMANDS_GUIDE.md
    """
    # Find project root (look for pyproject.toml)
    cwd = Path.cwd()
    project_root = cwd

    for parent in [cwd] + list(cwd.parents):
        if (parent / "pyproject.toml").exists():
            project_root = parent
            break

    templates_dir = project_root / "templates" / "commands"
    output_path = project_root / "docs" / "COMMANDS_GUIDE.md"

    if not templates_dir.exists():
        print(f"ERROR: Templates directory not found: {templates_dir}")
        return

    # Parse all command templates
    commands: List[CommandMetadata] = []
    template_count = 0

    for template_path in templates_dir.glob("*.md"):
        # Skip compressed templates
        if ".COMPRESSED" in template_path.name:
            continue

        template_count += 1
        try:
            cmd = parse_command_template(template_path)
            commands.append(cmd)
            print(f"  ✓ Parsed: {cmd.name} ({len(cmd.flags)} flags)")
        except Exception as e:
            print(f"  ✗ Failed to parse {template_path.name}: {e}")

    print(f"\nParsed {len(commands)}/{template_count} templates")

    # Get version from pyproject.toml
    version = "1.5.0"
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text()
        match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if match:
            version = match.group(1)

    # Generate guide
    guide_content = generate_commands_guide(commands, version)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write output
    output_path.write_text(guide_content, encoding="utf-8")
    print(f"\n✓ Generated: {output_path}")
    print(f"  - {len(commands)} commands documented")
    print(f"  - {sum(len(c.flags) for c in commands)} total flags")


if __name__ == "__main__":
    main()

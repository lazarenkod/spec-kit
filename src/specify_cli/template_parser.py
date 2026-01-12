"""
Template Parser for extracting subagent definitions from command templates.

This module parses YAML frontmatter from Spec Kit command templates and
extracts agent task definitions, orchestration settings, and dependency graphs.

Template Structure:
    ```yaml
    ---
    description: Command description
    claude_code:
      model: opus
      orchestration:
        max_parallel: 3
        wave_overlap:
          enabled: true
          overlap_threshold: 0.80
      subagents:
        - role: analyzer
          role_group: ANALYSIS
          parallel: true
          depends_on: []
          priority: 10
          prompt: "Analyze the code..."
          model_override: sonnet
    ---
    # Template content...
    ```

Usage:
    tasks = parse_subagents_from_template(
        template_path=Path(".specify/templates/commands/implement.md"),
        feature="001-user-auth"
    )
    # Returns list of AgentTask objects ready for execution
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .agent_pool import AgentTask, ModelTier
from .wave_scheduler import WaveConfig, ExecutionStrategy


# Model name mapping from template shorthand to full model ID
MODEL_MAP: Dict[str, str] = {
    "opus": ModelTier.OPUS.value,
    "sonnet": ModelTier.SONNET.value,
    "haiku": ModelTier.HAIKU.value,
    "claude-opus-4-5-20251101": ModelTier.OPUS.value,
    "claude-sonnet-4-5-20250929": ModelTier.SONNET.value,
    "claude-3-5-haiku-20241022": ModelTier.HAIKU.value,
}

# Model tier hierarchy (for cap enforcement)
MODEL_TIERS: Dict[str, int] = {
    "opus": 3,
    "sonnet": 2,
    "haiku": 1,
    "claude-opus-4-5-20251101": 3,
    "claude-sonnet-4-5-20250929": 2,
    "claude-3-5-haiku-20241022": 1,
}

# Reverse mapping: tier → model shorthand
TIER_TO_MODEL: Dict[int, str] = {
    3: "opus",
    2: "sonnet",
    1: "haiku",
}


@dataclass
class TemplateConfig:
    """
    Parsed configuration from a template.

    Attributes:
        description: Template description
        default_model: Default model for agents
        wave_config: Configuration for wave execution
        subagents: List of subagent definitions
        phases: Named execution phases with model overrides
        raw_frontmatter: Original parsed YAML frontmatter
    """
    description: str
    default_model: str
    wave_config: WaveConfig
    subagents: List[Dict[str, Any]]
    phases: Dict[str, Dict[str, Any]]
    raw_frontmatter: Dict[str, Any]


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

    # Find the closing ---
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


def parse_template_config(template_path: Path) -> TemplateConfig:
    """
    Parse a template file and extract configuration.

    Args:
        template_path: Path to the template .md file

    Returns:
        TemplateConfig with parsed settings

    Raises:
        FileNotFoundError: If template doesn't exist
        ValueError: If template has invalid structure
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    content = template_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(content)

    if frontmatter is None:
        raise ValueError(f"No valid YAML frontmatter in: {template_path}")

    # Extract claude_code configuration
    claude_code = frontmatter.get("claude_code", {})

    # Default model
    default_model = MODEL_MAP.get(
        claude_code.get("model", "sonnet"),
        ModelTier.SONNET.value
    )

    # Orchestration settings
    orchestration = claude_code.get("orchestration", {})
    wave_overlap = orchestration.get("wave_overlap", {})

    wave_config = WaveConfig(
        max_parallel=orchestration.get("max_parallel", 3),
        overlap_enabled=wave_overlap.get("enabled", True),
        overlap_threshold=wave_overlap.get("overlap_threshold", 0.80),
        strategy=(
            ExecutionStrategy.OVERLAPPED
            if wave_overlap.get("enabled", True)
            else ExecutionStrategy.SEQUENTIAL
        ),
        fail_fast=True,
        timeout_per_task_ms=orchestration.get("timeout_per_agent"),
    )

    # Subagents
    subagents = claude_code.get("subagents", [])

    # Phases (for phase-specific model overrides)
    phases = claude_code.get("phases", {})

    return TemplateConfig(
        description=frontmatter.get("description", ""),
        default_model=default_model,
        wave_config=wave_config,
        subagents=subagents,
        phases=phases,
        raw_frontmatter=frontmatter,
    )


def read_max_model_from_constitution(project_root: Path) -> Optional[str]:
    """
    Read max_model setting from constitution.md.

    Args:
        project_root: Path to project root directory

    Returns:
        max_model value ("opus", "sonnet", "haiku") or None if not set
    """
    constitution_path = project_root / "memory" / "constitution.md"

    if not constitution_path.exists():
        return None

    try:
        content = constitution_path.read_text(encoding="utf-8")

        # Search for: | **max_model** | `VALUE` | ... |
        # Pattern: | **max_model** | `(opus|sonnet|haiku|none)` |
        pattern = r'\|\s*\*\*max_model\*\*\s*\|\s*`([^`]+)`\s*\|'
        match = re.search(pattern, content)

        if match:
            value = match.group(1).strip()
            if value in ["opus", "sonnet", "haiku"]:
                return value
            elif value == "none":
                return None

        return None
    except Exception:
        # Silent fallback if constitution read fails
        return None


def resolve_model(
    model_override: Optional[str],
    default_model: str,
    max_model: Optional[str] = None
) -> str:
    """
    Resolve a model name to full model ID, applying model cap if set.

    Args:
        model_override: Optional model shorthand (e.g., "haiku")
        default_model: Default model to use if no override
        max_model: Optional maximum model tier ("opus", "sonnet", "haiku")

    Returns:
        Full model ID string (potentially downgraded)
    """
    # Determine requested model
    requested_model = model_override if model_override else default_model

    # Resolve shorthand to full ID
    resolved_model = MODEL_MAP.get(requested_model, requested_model)

    # Apply model cap if set
    if max_model:
        requested_tier = MODEL_TIERS.get(resolved_model, MODEL_TIERS.get(requested_model, 0))
        max_tier = MODEL_TIERS.get(max_model, 0)

        if requested_tier > max_tier and max_tier > 0:
            # Downgrade: return model at max_tier
            downgraded_model = TIER_TO_MODEL.get(max_tier, requested_model)
            return MODEL_MAP.get(downgraded_model, downgraded_model)

    return resolved_model


def build_prompt_with_context(
    base_prompt: str,
    feature: str,
    context: Optional[Dict[str, Any]] = None
) -> str:
    """
    Build a complete prompt with feature context.

    Args:
        base_prompt: The base prompt from template
        feature: Feature identifier (e.g., "001-user-auth")
        context: Additional context to inject

    Returns:
        Complete prompt string
    """
    prompt_parts = [
        f"Feature: {feature}",
        "",
        base_prompt,
    ]

    if context:
        prompt_parts.append("")
        prompt_parts.append("Additional Context:")
        for key, value in context.items():
            prompt_parts.append(f"  {key}: {value}")

    return "\n".join(prompt_parts)


def parse_subagents_from_template(
    template_path: Path,
    feature: str,
    context: Optional[Dict[str, Any]] = None,
    filter_parallel: bool = True,
) -> List[AgentTask]:
    """
    Extract subagent definitions from template YAML frontmatter.

    Parses the template's claude_code.subagents section and converts
    each subagent definition into an AgentTask ready for execution.

    Args:
        template_path: Path to the template .md file
        feature: Feature identifier for prompt context
        context: Additional context to inject into prompts
        filter_parallel: If True, only return agents marked parallel=true

    Returns:
        List of AgentTask objects

    Example:
        ```python
        tasks = parse_subagents_from_template(
            Path(".specify/templates/commands/implement.md"),
            feature="001-user-auth",
            context={"spec_path": "specs/features/001-user-auth/spec.md"}
        )
        ```
    """
    config = parse_template_config(template_path)

    # Read model cap from constitution (project root = current working directory)
    max_model = read_max_model_from_constitution(Path.cwd())

    tasks: List[AgentTask] = []

    for agent_def in config.subagents:
        # Skip non-parallel agents if filtering
        if filter_parallel and not agent_def.get("parallel", True):
            continue

        # Resolve model
        model = resolve_model(
            agent_def.get("model_override"),
            config.default_model,
            max_model
        )

        # Build prompt with context
        base_prompt = agent_def.get("prompt", f"Execute {agent_def.get('role', 'unknown')}")
        prompt = build_prompt_with_context(base_prompt, feature, context)

        # Extract dependencies
        depends_on = agent_def.get("depends_on", [])
        if depends_on is None:
            depends_on = []

        task = AgentTask(
            name=agent_def.get("role", f"agent-{len(tasks)}"),
            prompt=prompt,
            model=model,
            depends_on=depends_on,
            priority=agent_def.get("priority", 5),
            role_group=agent_def.get("role_group", "DEFAULT"),
            metadata={
                "trigger": agent_def.get("trigger"),
                "template": str(template_path),
                "feature": feature,
            }
        )

        tasks.append(task)

    return tasks


def get_wave_config_from_template(template_path: Path) -> WaveConfig:
    """
    Extract WaveConfig from template.

    Convenience function to get just the wave configuration.

    Args:
        template_path: Path to template file

    Returns:
        WaveConfig with template settings
    """
    config = parse_template_config(template_path)
    return config.wave_config


def list_available_templates(
    templates_dir: Path,
    with_subagents_only: bool = True
) -> List[Path]:
    """
    List available command templates.

    Args:
        templates_dir: Directory containing templates
        with_subagents_only: If True, only return templates with subagents

    Returns:
        List of template paths
    """
    if not templates_dir.exists():
        return []

    templates = list(templates_dir.glob("*.md"))

    if not with_subagents_only:
        return templates

    # Filter to those with subagents
    result = []
    for path in templates:
        try:
            config = parse_template_config(path)
            if config.subagents:
                result.append(path)
        except (ValueError, FileNotFoundError):
            continue

    return result


def generate_dependency_graph(tasks: List[AgentTask]) -> str:
    """
    Generate a Mermaid dependency graph for visualization.

    Args:
        tasks: List of tasks with dependencies

    Returns:
        Mermaid graph definition string
    """
    lines = ["graph TD"]

    # Create nodes
    for task in tasks:
        label = f"{task.name}[{task.name}]"
        lines.append(f"    {label}")

    # Create edges
    for task in tasks:
        for dep in task.depends_on:
            lines.append(f"    {dep} --> {task.name}")

    return "\n".join(lines)

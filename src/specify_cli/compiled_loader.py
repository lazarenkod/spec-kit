"""
Runtime Loader for Pre-Compiled Templates.

Provides fast loading of pre-compiled JSON templates with LRU caching.
Falls back to runtime parsing if compiled version is unavailable.

Usage:
    loader = CompiledTemplateLoader()
    template = loader.load("specify")

    # With fast path optimization
    template = loader.load_with_fast_path("specify", {"mode": "greenfield"})

Performance:
    Compiled JSON load: ~5-10ms
    With LRU cache hit: <1ms
    Fallback parsing: 50-100ms
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from .template_parser import parse_template_config, TemplateConfig


class CompiledTemplateLoader:
    """
    Runtime loader for pre-compiled templates.

    Provides fast access to pre-compiled template JSON with LRU caching.
    Automatically falls back to runtime parsing when compiled version
    is unavailable or outdated.
    """

    def __init__(
        self,
        compiled_dir: Optional[Path] = None,
        templates_dir: Optional[Path] = None,
        cache_size: int = 50,
    ):
        """
        Initialize the loader.

        Args:
            compiled_dir: Path to compiled/ directory with JSON files
            templates_dir: Path to templates/commands/ for fallback
            cache_size: Maximum number of templates to cache in memory
        """
        self.compiled_dir = compiled_dir or Path("compiled")
        self.templates_dir = templates_dir or Path("templates/commands")

        # Configure cache
        self._load_cached = lru_cache(maxsize=cache_size)(self._load_impl)

    def load(self, command: str) -> Optional[Dict[str, Any]]:
        """
        Load a compiled template by command name.

        Tries compiled JSON first, falls back to runtime parsing.

        Args:
            command: Template command name (e.g., "specify", "implement")

        Returns:
            Compiled template dict or None if not found
        """
        return self._load_cached(command)

    def _load_impl(self, command: str) -> Optional[Dict[str, Any]]:
        """Internal implementation of load (cached)."""
        # Try compiled version first
        compiled_path = self.compiled_dir / f"{command}.json"
        if compiled_path.exists():
            try:
                content = compiled_path.read_text(encoding="utf-8")
                return json.loads(content)
            except (json.JSONDecodeError, OSError):
                pass

        # Fallback to runtime parsing
        template_path = self.templates_dir / f"{command}.md"
        if template_path.exists():
            return self._parse_template_to_dict(template_path)

        return None

    def _parse_template_to_dict(self, template_path: Path) -> Dict[str, Any]:
        """
        Parse template at runtime and convert to compiled format.

        Used as fallback when compiled JSON is not available.
        """
        config = parse_template_config(template_path)

        # Read body
        content = template_path.read_text(encoding="utf-8")
        body = self._get_template_body(content)

        return {
            "version": "1.0",
            "meta": {
                "command": template_path.stem,
                "source_file": str(template_path),
                "source_hash": "runtime",
                "compiled_at": None,
                "compiler_version": "runtime",
                "includes_resolved": [],
            },
            "config": {
                "description": config.description,
                "model": config.default_model,
            },
            "execution_plan": {
                "max_parallel": config.wave_config.max_parallel,
                "wave_overlap": {
                    "enabled": config.wave_config.overlap_enabled,
                    "threshold": config.wave_config.overlap_threshold,
                },
            },
            "prompt": {
                "user_template": body,
            },
            "handoffs": config.raw_frontmatter.get("handoffs", []),
            "scripts": config.raw_frontmatter.get("scripts", {}),
        }

    def _get_template_body(self, content: str) -> str:
        """Extract template body (everything after frontmatter)."""
        if not content.startswith("---"):
            return content

        lines = content.split("\n")

        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                return "\n".join(lines[i + 1:]).strip()

        return content

    def load_with_fast_path(
        self,
        command: str,
        runtime_context: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Load template and apply fast path optimizations.

        Fast paths allow skipping certain processing steps based on
        runtime context (e.g., greenfield vs brownfield mode).

        Args:
            command: Template command name
            runtime_context: Runtime context for optimization decisions
                - mode: "greenfield" or "brownfield"
                - has_baseline: Whether baseline.md exists
                - complexity: "simple" or "complex"

        Returns:
            Template dict with fast_path_applied field
        """
        template = self.load(command)
        if template is None:
            return None

        # Apply fast paths based on context
        fast_paths = template.get("fast_paths", {})
        applied_optimizations: List[str] = []

        mode = runtime_context.get("mode")
        has_baseline = runtime_context.get("has_baseline", False)

        # Greenfield fast path
        if mode == "greenfield" and "greenfield" in fast_paths:
            applied_optimizations.append("greenfield")
            template["_skip_steps"] = fast_paths["greenfield"].get("skip_steps", [])

        # Brownfield with baseline
        if mode == "brownfield" and has_baseline and "brownfield_with_baseline" in fast_paths:
            applied_optimizations.append("brownfield_with_baseline")
            template["_skip_steps"] = fast_paths["brownfield_with_baseline"].get("skip_steps", [])

        # Simple template fast path
        if runtime_context.get("complexity") == "simple" and "simple" in fast_paths:
            applied_optimizations.append("simple")
            skip_steps = template.get("_skip_steps", [])
            skip_steps.extend(fast_paths["simple"].get("skip_steps", []))
            template["_skip_steps"] = list(set(skip_steps))

        template["_fast_path_applied"] = applied_optimizations

        return template

    def get_config(self, command: str) -> Optional[Dict[str, Any]]:
        """
        Get just the config section of a template.

        Convenience method for quick access to template configuration.

        Args:
            command: Template command name

        Returns:
            Config dict or None if template not found
        """
        template = self.load(command)
        if template:
            return template.get("config")
        return None

    def get_execution_plan(self, command: str) -> Optional[Dict[str, Any]]:
        """
        Get the execution plan section of a template.

        Args:
            command: Template command name

        Returns:
            Execution plan dict or None if template not found
        """
        template = self.load(command)
        if template:
            return template.get("execution_plan")
        return None

    def list_compiled(self) -> List[str]:
        """
        List all available compiled templates.

        Returns:
            List of command names
        """
        if not self.compiled_dir.exists():
            return []

        return sorted(
            p.stem for p in self.compiled_dir.glob("*.json")
        )

    def is_compiled(self, command: str) -> bool:
        """
        Check if a template has a compiled version.

        Args:
            command: Template command name

        Returns:
            True if compiled JSON exists
        """
        compiled_path = self.compiled_dir / f"{command}.json"
        return compiled_path.exists()

    def get_source_hash(self, command: str) -> Optional[str]:
        """
        Get the source hash of a compiled template.

        Useful for cache invalidation checks.

        Args:
            command: Template command name

        Returns:
            Source hash string or None if not compiled
        """
        template = self.load(command)
        if template:
            meta = template.get("meta", {})
            return meta.get("source_hash")
        return None

    def clear_cache(self) -> None:
        """Clear the LRU cache."""
        self._load_cached.cache_clear()

    def cache_info(self) -> Dict[str, int]:
        """
        Get cache statistics.

        Returns:
            Dict with hits, misses, maxsize, currsize
        """
        info = self._load_cached.cache_info()
        return {
            "hits": info.hits,
            "misses": info.misses,
            "maxsize": info.maxsize,
            "currsize": info.currsize,
        }


# Global loader instance for convenience
_default_loader: Optional[CompiledTemplateLoader] = None


def get_loader() -> CompiledTemplateLoader:
    """
    Get the default loader instance.

    Creates a new loader on first call, reuses on subsequent calls.

    Returns:
        CompiledTemplateLoader instance
    """
    global _default_loader
    if _default_loader is None:
        _default_loader = CompiledTemplateLoader()
    return _default_loader


def load_template(command: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to load a template.

    Uses the default loader instance.

    Args:
        command: Template command name

    Returns:
        Compiled template dict or None
    """
    return get_loader().load(command)

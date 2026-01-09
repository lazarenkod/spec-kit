"""
Async file operations for parallel loading of feature artifacts.

This module provides async file I/O functions to load multiple files
in parallel, reducing total I/O latency for feature bootstrapping.

Performance:
    Sequential: 4 files × 200ms = 800ms
    Parallel:   1 × 200ms = 200ms (4x speedup)
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict, List, Optional

try:
    import aiofiles
    AIOFILES_AVAILABLE = True
except ImportError:
    AIOFILES_AVAILABLE = False


async def load_artifacts_parallel(
    feature_dir: Path,
    filenames: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    Load multiple feature artifacts in parallel.

    Args:
        feature_dir: Directory containing feature files
        filenames: List of filenames to load. Defaults to standard artifacts.

    Returns:
        Dictionary mapping filename to content (empty string if file doesn't exist)

    Example:
        ```python
        artifacts = await load_artifacts_parallel(Path("features/auth"))
        spec_content = artifacts["spec.md"]
        plan_content = artifacts["plan.md"]
        ```
    """
    if not AIOFILES_AVAILABLE:
        # Fallback to synchronous loading
        return _load_artifacts_sync(feature_dir, filenames)

    if filenames is None:
        filenames = [
            "spec.md",
            "plan.md",
            "tasks.md",
            "constitution.md",
            "concept.md",
            "baseline.md",
        ]

    paths = [feature_dir / filename for filename in filenames]

    async def read_one(path: Path, filename: str) -> tuple[str, str]:
        """Read a single file asynchronously."""
        if not path.exists():
            return (filename, "")

        try:
            async with aiofiles.open(path, 'r', encoding='utf-8') as f:
                content = await f.read()
            return (filename, content)
        except Exception as e:
            # Return empty string on error (file may be locked, etc.)
            return (filename, f"# ERROR: {str(e)}")

    # Launch all reads in parallel
    tasks = [read_one(path, filename) for path, filename in zip(paths, filenames)]
    results = await asyncio.gather(*tasks)

    return dict(results)


def _load_artifacts_sync(
    feature_dir: Path,
    filenames: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    Synchronous fallback for loading artifacts.

    Used when aiofiles is not available.
    """
    if filenames is None:
        filenames = [
            "spec.md",
            "plan.md",
            "tasks.md",
            "constitution.md",
            "concept.md",
            "baseline.md",
        ]

    artifacts = {}
    for filename in filenames:
        path = feature_dir / filename
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    artifacts[filename] = f.read()
            except Exception as e:
                artifacts[filename] = f"# ERROR: {str(e)}"
        else:
            artifacts[filename] = ""

    return artifacts


async def load_file_async(file_path: Path) -> str:
    """
    Load a single file asynchronously.

    Args:
        file_path: Path to file to load

    Returns:
        File content or empty string if file doesn't exist

    Example:
        ```python
        spec = await load_file_async(Path("features/auth/spec.md"))
        ```
    """
    if not AIOFILES_AVAILABLE:
        # Fallback to synchronous
        if not file_path.exists():
            return ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return ""

    if not file_path.exists():
        return ""

    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        return content
    except Exception:
        return ""


async def write_file_async(file_path: Path, content: str) -> bool:
    """
    Write a file asynchronously.

    Args:
        file_path: Path to file to write
        content: Content to write

    Returns:
        True if successful, False otherwise

    Example:
        ```python
        success = await write_file_async(
            Path("features/auth/spec.md"),
            spec_content
        )
        ```
    """
    if not AIOFILES_AVAILABLE:
        # Fallback to synchronous
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False

    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)
        return True
    except Exception:
        return False


async def load_template_async(template_path: Path) -> str:
    """
    Load a template file asynchronously.

    Convenience wrapper around load_file_async for template files.

    Args:
        template_path: Path to template file

    Returns:
        Template content or empty string if file doesn't exist
    """
    return await load_file_async(template_path)


def is_async_available() -> bool:
    """
    Check if async file operations are available.

    Returns:
        True if aiofiles is installed, False otherwise
    """
    return AIOFILES_AVAILABLE

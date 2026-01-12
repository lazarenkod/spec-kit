"""
Unit tests for template_parser module, focusing on model cap functionality.
"""

import tempfile
from pathlib import Path

import pytest

from src.specify_cli.template_parser import (
    MODEL_MAP,
    MODEL_TIERS,
    TIER_TO_MODEL,
    read_max_model_from_constitution,
    resolve_model,
)


class TestModelTierMappings:
    """Test model tier dictionaries are correctly defined."""

    def test_model_tiers_include_all_models(self):
        """All models in MODEL_MAP should have tier mappings."""
        for model in MODEL_MAP.values():
            assert model in MODEL_TIERS, f"Model {model} missing from MODEL_TIERS"

    def test_tier_to_model_completeness(self):
        """TIER_TO_MODEL should have entries for tiers 1, 2, 3."""
        assert TIER_TO_MODEL[1] == "haiku"
        assert TIER_TO_MODEL[2] == "sonnet"
        assert TIER_TO_MODEL[3] == "opus"

    def test_tier_hierarchy(self):
        """Opus (3) > Sonnet (2) > Haiku (1)."""
        opus_tier = MODEL_TIERS["opus"]
        sonnet_tier = MODEL_TIERS["sonnet"]
        haiku_tier = MODEL_TIERS["haiku"]

        assert opus_tier > sonnet_tier > haiku_tier
        assert opus_tier == 3
        assert sonnet_tier == 2
        assert haiku_tier == 1


class TestResolveModelNoCap:
    """Test resolve_model function without model cap (baseline behavior)."""

    def test_resolve_model_no_cap_opus(self):
        """Default behavior: no cap, opus works normally."""
        result = resolve_model(None, "opus", max_model=None)
        assert result == "claude-opus-4-5-20251101"

    def test_resolve_model_no_cap_sonnet(self):
        """Default behavior: no cap, sonnet works normally."""
        result = resolve_model(None, "sonnet", max_model=None)
        assert result == "claude-sonnet-4-5-20250929"

    def test_resolve_model_no_cap_haiku(self):
        """Default behavior: no cap, haiku works normally."""
        result = resolve_model(None, "haiku", max_model=None)
        assert result == "claude-3-5-haiku-20241022"

    def test_resolve_model_with_override_no_cap(self):
        """Model override works without cap."""
        result = resolve_model("haiku", "opus", max_model=None)
        assert result == "claude-3-5-haiku-20241022"


class TestResolveModelWithCapSonnet:
    """Test resolve_model with max_model=sonnet."""

    def test_cap_sonnet_downgrades_opus(self):
        """Cap at sonnet: opus → sonnet."""
        result = resolve_model(None, "opus", max_model="sonnet")
        assert result == "claude-sonnet-4-5-20250929"

    def test_cap_sonnet_preserves_sonnet(self):
        """Cap at sonnet: sonnet unchanged."""
        result = resolve_model(None, "sonnet", max_model="sonnet")
        assert result == "claude-sonnet-4-5-20250929"

    def test_cap_sonnet_preserves_haiku(self):
        """Cap at sonnet: haiku unchanged."""
        result = resolve_model(None, "haiku", max_model="sonnet")
        assert result == "claude-3-5-haiku-20241022"

    def test_cap_sonnet_with_opus_override(self):
        """Cap at sonnet: opus override → sonnet."""
        result = resolve_model("opus", "haiku", max_model="sonnet")
        assert result == "claude-sonnet-4-5-20250929"


class TestResolveModelWithCapHaiku:
    """Test resolve_model with max_model=haiku."""

    def test_cap_haiku_downgrades_opus(self):
        """Cap at haiku: opus → haiku."""
        result = resolve_model(None, "opus", max_model="haiku")
        assert result == "claude-3-5-haiku-20241022"

    def test_cap_haiku_downgrades_sonnet(self):
        """Cap at haiku: sonnet → haiku."""
        result = resolve_model(None, "sonnet", max_model="haiku")
        assert result == "claude-3-5-haiku-20241022"

    def test_cap_haiku_preserves_haiku(self):
        """Cap at haiku: haiku unchanged."""
        result = resolve_model(None, "haiku", max_model="haiku")
        assert result == "claude-3-5-haiku-20241022"


class TestResolveModelWithCapOpus:
    """Test resolve_model with max_model=opus (should be no-op)."""

    def test_cap_opus_preserves_opus(self):
        """Cap at opus: opus unchanged."""
        result = resolve_model(None, "opus", max_model="opus")
        assert result == "claude-opus-4-5-20251101"

    def test_cap_opus_preserves_sonnet(self):
        """Cap at opus: sonnet unchanged."""
        result = resolve_model(None, "sonnet", max_model="opus")
        assert result == "claude-sonnet-4-5-20250929"

    def test_cap_opus_preserves_haiku(self):
        """Cap at opus: haiku unchanged."""
        result = resolve_model(None, "haiku", max_model="opus")
        assert result == "claude-3-5-haiku-20241022"


class TestReadMaxModelFromConstitution:
    """Test reading max_model setting from constitution.md."""

    def test_missing_constitution_returns_none(self):
        """Missing constitution → None (no cap)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            result = read_max_model_from_constitution(project_root)
            assert result is None

    def test_constitution_without_max_model_returns_none(self):
        """Constitution without max_model → None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            memory_dir = project_root / "memory"
            memory_dir.mkdir()

            constitution = memory_dir / "constitution.md"
            constitution.write_text(
                """
## Project Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **language** | `en` | Primary language |
| **date_format** | `ISO` | Date format |
"""
            )

            result = read_max_model_from_constitution(project_root)
            assert result is None

    def test_constitution_with_max_model_none(self):
        """max_model: none → None (no cap)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            memory_dir = project_root / "memory"
            memory_dir.mkdir()

            constitution = memory_dir / "constitution.md"
            constitution.write_text(
                """
## Project Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **language** | `en` | Primary language |
| **max_model** | `none` | Maximum model tier |
"""
            )

            result = read_max_model_from_constitution(project_root)
            assert result is None

    def test_constitution_with_max_model_sonnet(self):
        """max_model: sonnet → 'sonnet'."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            memory_dir = project_root / "memory"
            memory_dir.mkdir()

            constitution = memory_dir / "constitution.md"
            constitution.write_text(
                """
## Project Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **language** | `en` | Primary language |
| **max_model** | `sonnet` | Maximum model tier |
"""
            )

            result = read_max_model_from_constitution(project_root)
            assert result == "sonnet"

    def test_constitution_with_max_model_haiku(self):
        """max_model: haiku → 'haiku'."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            memory_dir = project_root / "memory"
            memory_dir.mkdir()

            constitution = memory_dir / "constitution.md"
            constitution.write_text(
                """
## Project Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **max_model** | `haiku` | Maximum model tier |
"""
            )

            result = read_max_model_from_constitution(project_root)
            assert result == "haiku"

    def test_constitution_with_max_model_opus(self):
        """max_model: opus → 'opus'."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            memory_dir = project_root / "memory"
            memory_dir.mkdir()

            constitution = memory_dir / "constitution.md"
            constitution.write_text(
                """
## Project Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **max_model** | `opus` | Maximum model tier |
"""
            )

            result = read_max_model_from_constitution(project_root)
            assert result == "opus"

    def test_constitution_with_invalid_value(self):
        """max_model: invalid → None (graceful fallback)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            memory_dir = project_root / "memory"
            memory_dir.mkdir()

            constitution = memory_dir / "constitution.md"
            constitution.write_text(
                """
## Project Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **max_model** | `invalid-value` | Maximum model tier |
"""
            )

            result = read_max_model_from_constitution(project_root)
            assert result is None


class TestIntegration:
    """Integration tests combining constitution reading and model resolution."""

    def test_end_to_end_cap_at_sonnet(self):
        """Full workflow: constitution with max_model=sonnet."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            memory_dir = project_root / "memory"
            memory_dir.mkdir()

            constitution = memory_dir / "constitution.md"
            constitution.write_text(
                """
## Project Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **max_model** | `sonnet` | Maximum model tier |
"""
            )

            # Read cap
            max_model = read_max_model_from_constitution(project_root)
            assert max_model == "sonnet"

            # Apply cap
            opus_result = resolve_model(None, "opus", max_model)
            sonnet_result = resolve_model(None, "sonnet", max_model)
            haiku_result = resolve_model(None, "haiku", max_model)

            assert opus_result == "claude-sonnet-4-5-20250929"  # downgraded
            assert sonnet_result == "claude-sonnet-4-5-20250929"  # unchanged
            assert haiku_result == "claude-3-5-haiku-20241022"  # unchanged

    def test_end_to_end_no_cap(self):
        """Full workflow: constitution with max_model=none."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            memory_dir = project_root / "memory"
            memory_dir.mkdir()

            constitution = memory_dir / "constitution.md"
            constitution.write_text(
                """
## Project Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **max_model** | `none` | Maximum model tier |
"""
            )

            # Read cap
            max_model = read_max_model_from_constitution(project_root)
            assert max_model is None

            # No cap applied
            opus_result = resolve_model(None, "opus", max_model)
            assert opus_result == "claude-opus-4-5-20251101"  # unchanged

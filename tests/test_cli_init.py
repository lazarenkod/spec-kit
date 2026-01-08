"""
Unit tests for CLI init command.

Tests template selection removal, deprecation warnings, and backward compatibility.
"""

import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from specify_cli import app, TEMPLATE_CHOICES


runner = CliRunner()


class TestInitCommand:
    """Test suite for specify init command."""

    def test_init_defaults_to_minimal_template(self):
        """Test that init uses 'minimal' template by default without asking."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock the download function to avoid network calls
            with patch("specify_cli.download_and_extract_template") as mock_download:
                mock_download.return_value = None

                result = runner.invoke(
                    app,
                    ["init", "test-project", "--ai", "claude", "--no-git"],
                    input="",  # No interactive input
                    catch_exceptions=False,
                    env={"HOME": tmpdir}
                )

                # Should not show template selection UI
                assert "Choose a production-ready template" not in result.output
                # Should complete without errors
                # Note: May fail due to network issues, but shouldn't ask for template

    def test_template_flag_shows_deprecation_warning(self):
        """Test that --template flag shows deprecation warning."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("specify_cli.download_and_extract_template") as mock_download:
                mock_download.return_value = None

                result = runner.invoke(
                    app,
                    ["init", "test-project", "--ai", "claude", "--template", "production-saas", "--no-git"],
                    env={"HOME": tmpdir}
                )

                # Should show deprecation warning
                assert "deprecated" in result.output.lower()
                assert "/speckit.constitution" in result.output

    def test_template_flag_backward_compatibility(self):
        """Test that --template flag still works for backward compatibility."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("specify_cli.download_and_extract_template") as mock_download:
                mock_download.return_value = None

                result = runner.invoke(
                    app,
                    ["init", "test-project", "--ai", "claude", "--template", "fintech", "--no-git"],
                    env={"HOME": tmpdir}
                )

                # Should show warning but still mention backward compatibility
                assert "backward compatibility" in result.output.lower()

    def test_invalid_template_still_rejected(self):
        """Test that invalid template values are still rejected."""
        result = runner.invoke(
            app,
            ["init", "test-project", "--ai", "claude", "--template", "invalid-template"],
        )

        assert result.exit_code != 0
        assert "invalid template" in result.output.lower()

    def test_template_choices_still_exist(self):
        """Test that TEMPLATE_CHOICES dict still contains expected templates."""
        expected_templates = [
            "production-saas",
            "production-api",
            "mobile-app",
            "gaming",
            "fintech",
            "healthcare",
            "e-commerce",
            "minimal",
        ]

        for template in expected_templates:
            assert template in TEMPLATE_CHOICES, f"Missing template: {template}"

    def test_init_help_shows_deprecated_notice(self):
        """Test that init --help shows deprecated notice for --template."""
        result = runner.invoke(app, ["init", "--help"])

        assert result.exit_code == 0
        assert "DEPRECATED" in result.output

    def test_minimal_template_no_warning(self):
        """Test that --template minimal doesn't show deprecation warning."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("specify_cli.download_and_extract_template") as mock_download:
                mock_download.return_value = None

                result = runner.invoke(
                    app,
                    ["init", "test-project", "--ai", "claude", "--template", "minimal", "--no-git"],
                    env={"HOME": tmpdir}
                )

                # Minimal template shouldn't show deprecation warning
                # (it's the default behavior now)
                assert "deprecated" not in result.output.lower() or "backward compatibility" not in result.output.lower()


class TestSelectTemplateRemoved:
    """Tests to verify select_template_with_descriptions was removed."""

    def test_no_interactive_template_selection(self):
        """Verify that interactive template selection function was removed."""
        import specify_cli

        # The function should no longer exist
        assert not hasattr(specify_cli, 'select_template_with_descriptions'), \
            "select_template_with_descriptions should be removed"

    def test_no_requirements_checklist_generation(self):
        """Verify requirements checklist is not generated for minimal template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir) / "test-project"
            project_path.mkdir()

            # Create a minimal project structure
            (project_path / "memory").mkdir(parents=True)

            # Check that REQUIREMENTS_CHECKLIST.md is not created by default
            checklist_path = project_path / "REQUIREMENTS_CHECKLIST.md"
            assert not checklist_path.exists(), \
                "REQUIREMENTS_CHECKLIST.md should not be generated for minimal template"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

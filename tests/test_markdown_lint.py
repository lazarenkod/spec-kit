"""
Markdown linting tests.

Validates all markdown files in the project to prevent CI failures.
Runs markdownlint-cli2 and fails if any errors are found in tracked files.
"""

import subprocess
import os
from pathlib import Path

import pytest


# Get project root
PROJECT_ROOT = Path(__file__).parent.parent


def get_tracked_markdown_files() -> list[str]:
    """Get list of markdown files tracked by git."""
    result = subprocess.run(
        ["git", "ls-files", "*.md", "**/*.md"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []

    files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
    return files


def run_markdownlint(files: list[str] | None = None) -> tuple[int, str, str]:
    """
    Run markdownlint-cli2 on specified files or all tracked markdown files.

    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    cmd = ["npx", "markdownlint-cli2"]

    if files:
        cmd.extend(files)
    else:
        cmd.extend(["**/*.md", "!.genreleases/", "!node_modules/", "!.venv/"])

    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    return result.returncode, result.stdout, result.stderr


class TestMarkdownLint:
    """Test suite for markdown validation."""

    def test_templates_valid(self):
        """Test that all template markdown files pass linting."""
        template_files = list(PROJECT_ROOT.glob("templates/**/*.md"))

        if not template_files:
            pytest.skip("No template markdown files found")

        relative_files = [str(f.relative_to(PROJECT_ROOT)) for f in template_files]
        exit_code, stdout, stderr = run_markdownlint(relative_files)

        # Combine output for error message
        output = stdout + stderr

        assert exit_code == 0, f"Markdown lint errors in templates:\n{output}"

    def test_memory_files_valid(self):
        """Test that memory markdown files pass linting."""
        memory_files = list(PROJECT_ROOT.glob("memory/**/*.md"))

        if not memory_files:
            pytest.skip("No memory markdown files found")

        relative_files = [str(f.relative_to(PROJECT_ROOT)) for f in memory_files]
        exit_code, stdout, stderr = run_markdownlint(relative_files)

        output = stdout + stderr
        assert exit_code == 0, f"Markdown lint errors in memory:\n{output}"

    def test_docs_valid(self):
        """Test that documentation files pass linting."""
        docs_files = list(PROJECT_ROOT.glob("docs/**/*.md"))

        if not docs_files:
            pytest.skip("No docs markdown files found")

        relative_files = [str(f.relative_to(PROJECT_ROOT)) for f in docs_files]
        exit_code, stdout, stderr = run_markdownlint(relative_files)

        output = stdout + stderr
        assert exit_code == 0, f"Markdown lint errors in docs:\n{output}"

    def test_root_markdown_valid(self):
        """Test that root-level tracked markdown files pass linting."""
        # Only test files tracked by git in root
        tracked = get_tracked_markdown_files()
        root_files = [f for f in tracked if "/" not in f and f.endswith(".md")]

        if not root_files:
            pytest.skip("No root markdown files tracked")

        exit_code, stdout, stderr = run_markdownlint(root_files)

        output = stdout + stderr
        assert exit_code == 0, f"Markdown lint errors in root files:\n{output}"

    def test_claude_commands_valid(self):
        """Test that .claude/commands markdown files pass linting."""
        command_files = list(PROJECT_ROOT.glob(".claude/commands/**/*.md"))

        if not command_files:
            pytest.skip("No .claude/commands markdown files found")

        relative_files = [str(f.relative_to(PROJECT_ROOT)) for f in command_files]
        exit_code, stdout, stderr = run_markdownlint(relative_files)

        output = stdout + stderr
        assert exit_code == 0, f"Markdown lint errors in .claude/commands:\n{output}"

    def test_critical_files_valid(self):
        """Test that critical project files pass linting."""
        critical_files = [
            "README.md",
            "CHANGELOG.md",
            "CLAUDE.md",
            "COMMANDS_GUIDE.md",
            "AGENTS.md",
        ]

        existing_files = [f for f in critical_files if (PROJECT_ROOT / f).exists()]

        if not existing_files:
            pytest.skip("No critical markdown files found")

        exit_code, stdout, stderr = run_markdownlint(existing_files)

        output = stdout + stderr
        assert exit_code == 0, f"Markdown lint errors in critical files:\n{output}"


class TestMarkdownStructure:
    """Test markdown file structure requirements."""

    def test_templates_have_frontmatter(self):
        """Test that command templates have valid YAML frontmatter."""
        command_templates = list(PROJECT_ROOT.glob("templates/commands/*.md"))

        errors = []
        for template in command_templates:
            content = template.read_text(encoding="utf-8")

            # Check for frontmatter
            if not content.startswith("---"):
                errors.append(f"{template.name}: Missing frontmatter (should start with ---)")
                continue

            # Check frontmatter is closed
            parts = content.split("---", 2)
            if len(parts) < 3:
                errors.append(f"{template.name}: Frontmatter not closed (missing second ---)")

        assert not errors, "Template frontmatter errors:\n" + "\n".join(errors)

    def test_no_trailing_whitespace_in_core_templates(self):
        """Test that core template files don't have excessive trailing whitespace."""
        # Only check core templates
        core_templates = [
            "templates/spec-template.md",
            "templates/plan-template.md",
            "templates/tasks-template.md",
        ]

        errors = []
        for template_path in core_templates:
            template = PROJECT_ROOT / template_path
            if not template.exists():
                continue

            content = template.read_text(encoding="utf-8")

            for i, line in enumerate(content.split("\n"), 1):
                # Allow trailing spaces for markdown line breaks (2 spaces)
                stripped = line.rstrip()
                trailing = len(line) - len(stripped)

                # Only flag 3+ trailing spaces (1-2 may be intentional)
                if trailing > 2:
                    errors.append(f"{template.name}:{i}: {trailing} trailing spaces")

        assert not errors, f"Trailing whitespace issues:\n" + "\n".join(errors)

    def test_code_spans_no_excessive_spaces(self):
        """Test that code spans don't have excessive leading/trailing spaces.

        Note: This is a simplified check. Full MD038 validation is done by markdownlint.
        We only flag egregious cases (3+ spaces) that would definitely fail CI.
        Patterns like ` / ` or ` | ` are intentional separators in templates.
        """
        import re

        # Only check core templates to limit false positives
        core_templates = [
            "templates/spec-template.md",
            "templates/plan-template.md",
            "templates/tasks-template.md",
        ]

        errors = []
        # Only flag code spans with 3+ leading or trailing spaces (definitely wrong)
        pattern = re.compile(r'`\s{3,}[^`]+`|`[^`]+\s{3,}`')

        for template_path in core_templates:
            template = PROJECT_ROOT / template_path
            if not template.exists():
                continue

            content = template.read_text(encoding="utf-8")

            for i, line in enumerate(content.split("\n"), 1):
                matches = pattern.findall(line)
                for match in matches:
                    errors.append(f"{template.name}:{i}: Excessive spaces in code span: {match[:50]}")

        assert not errors, "Code span space errors (MD038):\n" + "\n".join(errors[:20])


class TestMarkdownLinks:
    """Test markdown link validity."""

    def test_no_broken_internal_links_in_core_templates(self):
        """Test that core template files have valid internal links."""
        import re

        # Only check core templates, not design templates (which reference generated files)
        core_templates = [
            "templates/spec-template.md",
            "templates/plan-template.md",
            "templates/tasks-template.md",
            "templates/concept-template.md",
        ]

        errors = []
        # Pattern for markdown links: [text](path)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        for template_path in core_templates:
            template = PROJECT_ROOT / template_path
            if not template.exists():
                continue

            content = template.read_text(encoding="utf-8")
            template_dir = template.parent

            for match in link_pattern.finditer(content):
                link_text, link_path = match.groups()

                # Skip external links
                if link_path.startswith(("http://", "https://", "mailto:", "#")):
                    continue

                # Skip template variables and placeholders
                if "$" in link_path or "{" in link_path or "[" in link_path:
                    continue

                # Skip relative references to generated files and template placeholders
                if link_path.startswith(("specs/", "design/", "journeys/", "waves/", "adrs/", "../")):
                    continue

                # Skip placeholder patterns (like 001-login)
                if "/001-" in link_path or link_path.startswith("001-"):
                    continue

                # Remove anchor
                file_path = link_path.split("#")[0]

                if not file_path:
                    continue

                # Resolve relative path
                if file_path.startswith("/"):
                    target = PROJECT_ROOT / file_path.lstrip("/")
                else:
                    target = template_dir / file_path

                if not target.exists():
                    errors.append(f"{template.name}: Broken link [{link_text}]({link_path})")

        assert not errors, f"Broken internal links:\n" + "\n".join(errors)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

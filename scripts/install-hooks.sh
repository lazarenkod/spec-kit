#!/bin/bash
# Install pre-commit hooks for spec-kit development

set -e

echo "🔧 Installing pre-commit hooks..."

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit
fi

# Install the git hooks
pre-commit install

echo "✅ Pre-commit hooks installed successfully!"
echo ""
echo "Hooks configured:"
echo "  - Markdownlint (catches MD034, MD028, etc.)"
echo "  - Trailing whitespace"
echo "  - End-of-file fixer"
echo "  - YAML syntax check"
echo "  - Large file prevention"
echo "  - Merge conflict detection"
echo "  - Direct commit to main prevention"
echo ""
echo "💡 To run manually: pre-commit run --all-files"

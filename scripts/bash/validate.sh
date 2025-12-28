#!/bin/bash
# Validate all project files before commit/push
# Usage: ./scripts/bash/validate.sh

set -e

echo "=== Spec Kit Validation ==="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# 1. Markdown Linting
echo -n "Checking Markdown files... "
if command -v npx &> /dev/null; then
    if npx markdownlint-cli2 "**/*.md" 2>/dev/null; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}FAILED${NC}"
        echo "Run: npx markdownlint-cli2 \"**/*.md\" for details"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${YELLOW}SKIPPED${NC} (npx not found)"
fi

# 2. Python syntax check
echo -n "Checking Python syntax... "
if python3 -m py_compile src/specify_cli/__init__.py 2>/dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 3. Python imports
echo -n "Checking Python imports... "
if python3 -c "import specify_cli" 2>/dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}SKIPPED${NC} (not installed)"
fi

# 4. Template structure
echo -n "Checking template structure... "
REQUIRED_TEMPLATES=(
    "templates/commands/implement.md"
    "templates/commands/concept.md"
    "templates/commands/specify.md"
    "templates/spec-template.md"
)
MISSING=0
for tmpl in "${REQUIRED_TEMPLATES[@]}"; do
    if [ ! -f "$tmpl" ]; then
        echo -e "\n  Missing: $tmpl"
        MISSING=$((MISSING + 1))
    fi
done
if [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC} ($MISSING missing)"
    ERRORS=$((ERRORS + 1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}=== All checks passed ===${NC}"
    exit 0
else
    echo -e "${RED}=== $ERRORS check(s) failed ===${NC}"
    exit 1
fi

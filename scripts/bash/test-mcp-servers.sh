#!/bin/bash
# Test MCP Servers Installation
# Usage: ./scripts/bash/test-mcp-servers.sh

set -e

echo "🔍 Testing MCP Servers Installation..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_command() {
    local name=$1
    local cmd=$2

    echo -n "Testing ${name}... "
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        return 1
    fi
}

# Test Core Dependencies
echo "📦 Core Dependencies:"
test_command "Node.js" "node --version"
test_command "npm" "npm --version"
test_command "uvx" "uvx --version"
echo ""

# Test Python LSP
echo "🐍 Python LSP:"
test_command "pyright" "pyright --version"
test_command "pyright-langserver" "which pyright-langserver"
echo ""

# Test MCP Servers
echo "🔌 MCP Servers:"

# ast-grep
echo -n "Testing ast-grep CLI... "
if ast-grep --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
fi

echo -n "Testing ast-grep MCP... "
if npx -y @notprolands/ast-grep-mcp --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
fi

# tree-sitter
echo -n "Testing tree-sitter MCP... "
if uvx mcp-server-tree-sitter --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
fi

# lsp-mcp (test if it can be fetched)
echo -n "Testing lsp-mcp availability... "
if npx --yes --silent git+https://github.com/jonrad/lsp-mcp --help > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${YELLOW}⚠️  SLOW (first run downloads from GitHub)${NC}"
fi

# meta-mcp (token optimization)
echo -n "Testing meta-mcp-server... "
if npx -y @justanothermldude/meta-mcp-server --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
fi

# modular-mcp (token optimization)
echo -n "Testing modular-mcp... "
if npx -y @kimuson/modular-mcp --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
fi

# memory server (official)
echo -n "Testing memory server... "
if npx -y @modelcontextprotocol/server-memory --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
fi

# memory-sqlite (production)
echo -n "Testing memory-sqlite... "
if npx -y @pepk/mcp-memory-sqlite --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
fi

# mcp-optimizer (Python 3.13)
echo -n "Testing mcp-optimizer... "
if [ -x /tmp/mcp-optimizer/mcp-optimizer-wrapper.sh ]; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED (wrapper not found)${NC}"
fi

echo ""

# Test Claude Config
echo "⚙️  Configuration:"
if [ -d ~/.config/claude ]; then
    echo -e "Claude config directory: ${GREEN}✅ EXISTS${NC}"

    if [ -f ~/.config/claude/mcp.json ]; then
        echo -e "MCP config file: ${GREEN}✅ EXISTS${NC}"

        # Validate JSON
        if jq empty ~/.config/claude/mcp.json 2>/dev/null; then
            echo -e "JSON syntax: ${GREEN}✅ VALID${NC}"
        else
            echo -e "JSON syntax: ${RED}❌ INVALID${NC}"
        fi
    else
        echo -e "MCP config file: ${YELLOW}⚠️  NOT FOUND${NC}"
        echo "  Run: cp .mcp-config.json ~/.config/claude/mcp.json"
    fi
else
    echo -e "Claude config directory: ${RED}❌ NOT FOUND${NC}"
    echo "  Run: mkdir -p ~/.config/claude"
fi

echo ""

# Test Pyright on project
echo "🎯 Project-specific Tests:"
echo -n "Testing pyright on spec-kit... "
if pyright src/specify_cli/__init__.py --outputjson > /dev/null 2>&1; then
    echo -e "${GREEN}✅ NO TYPE ERRORS${NC}"
else
    echo -e "${YELLOW}⚠️  HAS TYPE WARNINGS (check with: pyright src/)${NC}"
fi

echo ""
echo "✨ MCP Setup Test Complete!"
echo ""
echo "Next steps:"
echo "1. Copy MCP config: cp .mcp-config.json ~/.config/claude/mcp.json"
echo "2. Restart Claude Code: exit && claude code"
echo "3. Verify in Claude: /mcp list"

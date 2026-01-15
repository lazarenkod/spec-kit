# MCP Setup Guide for spec-kit

This guide explains how to configure Model Context Protocol (MCP) servers for enhanced Claude Code functionality in the spec-kit project.

## 📦 Installed MCP Servers

### Core (Already Active)

1. **Serena** — Semantic code editing and navigation
   - Symbol-level refactoring
   - Memory management for project context
   - Status: ✅ Active

2. **Pinecone** — Vector database for semantic search
   - Embedding storage and retrieval
   - Semantic code search
   - Status: ✅ Active

### Recommended (New)

3. **LSP Bridge** (`lsp-mcp`) — Language Server Protocol integration
   - Real-time diagnostics and type checking
   - Go-to-definition, find references
   - Auto-imports and quick fixes
   - Status: 🟡 Ready to install

4. **Tree-sitter** (`mcp-server-tree-sitter`) — AST parsing
   - Structural code analysis
   - Syntax-aware queries
   - Parse tree caching
   - Status: 🟡 Ready to install

5. **ast-grep** (`ast-grep-mcp`) — Pattern-based code search
   - Syntax-aware search and replace
   - YAML rule testing
   - AST visualization
   - Status: 🟡 Ready to install

### Optional

6. **GitHub MCP** — GitHub integration
   - PR creation and review
   - Issue management
   - Automated workflows
   - Status: ⚪ Disabled (requires GITHUB_TOKEN)

7. **PostgreSQL MCP** — Database integration
   - SQL query execution
   - Schema inspection
   - Data analysis
   - Status: ⚪ Disabled (requires DATABASE_URL)

---

## 🚀 Quick Start

### Step 1: Install Pyright LSP (Native Claude Code Plugin)

**Recommended**: Use Claude Code's native LSP support (v2.0.74+):

```bash
# In Claude Code CLI session
/plugin install pyright@claude-code-lsps
```

This gives you:
- ✅ Real-time Python type checking
- ✅ Auto-imports
- ✅ Go-to-definition (50ms response time)
- ✅ Diagnostics and quick fixes

**Alternative**: Use MCP LSP Bridge (see Step 3).

### Step 2: Verify Pyright Configuration

The project already has `pyrightconfig.json` configured:

```json
{
  "include": ["src"],
  "pythonVersion": "3.11",
  "typeCheckingMode": "basic",
  "venvPath": ".",
  "venv": ".venv"
}
```

Test Pyright:
```bash
# Activate venv
source .venv/bin/activate

# Run pyright manually
pyright src/specify_cli/__init__.py
```

### Step 3: Install MCP Servers

**Option A: Copy configuration to Claude Code config**

```bash
# Copy MCP config to Claude Code directory
cp .mcp-config.json ~/.config/claude/mcp.json

# Or merge with existing config
cat .mcp-config.json >> ~/.config/claude/mcp.json
```

**Option B: Use project-local MCP config**

```bash
# Set environment variable
export CLAUDE_MCP_CONFIG="$PWD/.mcp-config.json"

# Run Claude Code
claude code
```

### Step 4: Install Required Dependencies

**For LSP Bridge** (if not using native plugin):
```bash
npm install -g pyright typescript-language-server gopls
cargo install rust-analyzer
```

**For Tree-sitter MCP**:
```bash
# Install via uvx (Python package manager)
uvx install mcp-server-tree-sitter

# Or via pip
pip install mcp-server-tree-sitter
```

**For ast-grep MCP**:
```bash
# Installs automatically via npx (no pre-install needed)
npx -y @ast-grep/ast-grep-mcp --version
```

### Step 5: Restart Claude Code

```bash
# Exit current session
exit

# Start new session
claude code
```

### Step 6: Verify MCP Tools

In Claude Code session:
```bash
# List available MCP servers
/mcp list

# Check LSP status
/plugin list

# Test Pyright
<ask Claude to check types in src/specify_cli/__init__.py>
```

---

## 🔧 Configuration Details

### LSP Bridge Configuration

**Supported Languages**:
- Python → Pyright
- TypeScript/JavaScript → typescript-language-server
- Go → gopls
- Rust → rust-analyzer

**Environment Variables**:
```json
{
  "LSP_LANGUAGES": "python=pyright,typescript=typescript-language-server"
}
```

### Tree-sitter Configuration

**Supported Languages** (40+):
Python, TypeScript, JavaScript, Go, Rust, Java, C, C++, C#, Ruby, PHP, Bash, YAML, JSON, Markdown, HTML, CSS, SQL, and more.

**Features**:
- Parse tree caching
- Incremental parsing
- Query language (S-expressions)
- Multi-file analysis

### ast-grep Configuration

**Features**:
- Pattern-based search (more precise than regex)
- YAML rule engine
- AST visualization
- Batch transformations

**Example Query**:
```yaml
# Find all @app.command() decorators
id: find-cli-commands
language: python
rule:
  pattern: |
    @app.command()
    def $FUNC_NAME(): ...
```

---

## 📊 Performance Comparison

| Operation | Before (text search) | After (LSP/Tree-sitter) | Improvement |
|-----------|---------------------|------------------------|-------------|
| Go-to-definition | 45 seconds | 50 ms | **900x faster** |
| Find references | 30 seconds | 100 ms | **300x faster** |
| Type checking | Manual | Real-time | ∞ |
| Structural search | Regex (brittle) | AST (precise) | Qualitative |

---

## 🎯 Use Cases for spec-kit

### 1. Type Safety
**Tool**: Pyright LSP (native plugin)
```python
# Claude detects type errors before running code
AGENT_CONFIG: dict[str, AgentInfo] = {
    "claude": AgentInfo(folder=".claude", requires_cli=True),
    "windsurf": "invalid"  # ❌ Error: Expected AgentInfo, got str
}
```

### 2. Symbol Navigation
**Tool**: LSP Bridge or Serena
```python
# Find all references to AGENT_CONFIG
/lsp find-references src/specify_cli/__init__.py:185
```

### 3. Pattern Search
**Tool**: ast-grep MCP
```bash
# Find all Typer command definitions
ast-grep --pattern '@app.command() def $NAME(): ...'
```

### 4. Structural Analysis
**Tool**: Tree-sitter MCP
```python
# Get all function signatures in __init__.py
treesitter_query("src/specify_cli/__init__.py", "(function_definition name: (_) parameters: (_))")
```

### 5. Template Validation
**Tool**: Tree-sitter (Markdown grammar)
```python
# Find all H2 headings in spec-template.md
treesitter_query("templates/spec-template.md", "(atx_heading (atx_h2_marker) (heading_content))")
```

---

## 🐛 Troubleshooting

### "No LSP server available"

**Cause**: LSP server not installed or not in PATH.

**Fix**:
```bash
# Check if pyright is installed
which pyright

# Install if missing
npm install -g pyright

# Restart Claude Code
```

### "MCP server failed to start"

**Cause**: Missing dependencies or incorrect config.

**Fix**:
```bash
# Check MCP server logs
tail -f ~/.claude/logs/mcp.log

# Test MCP server manually
npx -y @ast-grep/ast-grep-mcp --version
```

### "Tree-sitter parse errors"

**Cause**: Unsupported language or syntax errors in file.

**Fix**:
```bash
# Check supported languages
tree-sitter list

# Install missing grammar
npm install tree-sitter-python
```

---

## 📚 References

### Official Documentation

- **LSP Bridge**: [jonrad/lsp-mcp](https://github.com/jonrad/lsp-mcp)
- **Tree-sitter MCP**: [wrale/mcp-server-tree-sitter](https://github.com/wrale/mcp-server-tree-sitter)
- **ast-grep MCP**: [ast-grep/ast-grep-mcp](https://github.com/ast-grep/ast-grep-mcp)
- **Claude Code LSP Guide**: [AI Free API - Claude Code LSP](https://www.aifreeapi.com/en/posts/claude-code-lsp)
- **MCP Specification**: [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25)

### Community Resources

- **Awesome MCP Servers**: [mcpservers.org](https://mcpservers.org/)
- **PulseMCP**: [pulsemcp.com](https://www.pulsemcp.com/)
- **MCP Registry**: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

### Alternative Implementations

- **mcpls** (bug-ops): Universal MCP-LSP bridge - [github.com/bug-ops/mcpls](https://github.com/bug-ops/mcpls)
- **cclsp** (ktnyt): Claude Code LSP integration - [github.com/ktnyt/cclsp](https://github.com/ktnyt/cclsp)
- **mcp-language-server** (isaacphi): Semantic tools via LSP - [github.com/isaacphi/mcp-language-server](https://github.com/isaacphi/mcp-language-server)

---

## 🎓 Advanced Topics

### Custom LSP Configurations

For spec-kit-specific needs, you can create custom LSP wrappers:

```python
# scripts/python/lsp_wrapper.py
import asyncio
from lsp_mcp import LSPServer

async def main():
    server = LSPServer(
        language="python",
        command=["pyright-langserver", "--stdio"],
        root_path="/Users/dmitry.lazarenko/Documents/projects/spec-kit",
        config={
            "python.analysis.typeCheckingMode": "basic",
            "python.analysis.autoImportCompletions": True
        }
    )
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())
```

### Tree-sitter Custom Queries

**Find all Quality Gates in templates**:
```scheme
; templates/commands/*.md
(heading
  (atx_heading
    (atx_h3_marker)
    (heading_content) @title
    (#match? @title "QG-[0-9]{3}")))
```

**Find all AGENT_CONFIG accesses**:
```scheme
; src/specify_cli/*.py
(subscript
  value: (identifier) @var
  (#eq? @var "AGENT_CONFIG")
  subscript: (string) @agent)
```

### ast-grep Rules for spec-kit

**Validate all Typer commands have description**:
```yaml
# .ast-grep/rules/typer-commands.yml
id: require-command-description
language: python
rule:
  pattern: |
    @app.command()
    def $FUNC($PARAMS):
      $$$BODY
  not:
    has:
      kind: string
message: "Typer command must have docstring"
severity: warning
```

---

**Document Version**: 1.0.0
**Last Updated**: 2026-01-13
**Compatible with**: Claude Code v2.0.74+, MCP Spec 2025-11-25

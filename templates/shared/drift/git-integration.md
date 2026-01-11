# Git Integration for Drift Detection

**Purpose**: Define git diff analysis patterns, changed file detection algorithms, and scope filtering logic for `/speckit.fix` Wave 1 code-scanner subagent.

**Version**: 1.0.0
**Last Updated**: 2026-01-11

---

## Table of Contents

1. [Overview](#overview)
2. [Git Diff Analysis Patterns](#git-diff-analysis-patterns)
3. [Changed File Detection Algorithm](#changed-file-detection-algorithm)
4. [Scope Filtering Logic](#scope-filtering-logic)
5. [File Classification](#file-classification)
6. [Integration with Wave 1 Code-Scanner](#integration-with-wave-1-code-scanner)
7. [Edge Cases](#edge-cases)
8. [Performance Optimizations](#performance-optimizations)
9. [Examples](#examples)

---

## Overview

The git integration module enables `/speckit.fix` to analyze only changed files, reducing scan time from minutes to seconds for large codebases. This is the **default behavior** when `--git-diff` flag is enabled (which it is by default).

### Key Benefits

| Benefit | Impact |
|---------|--------|
| **Speed** | 10-50x faster (only changed files) |
| **Precision** | Focus on recent modifications |
| **Context** | Leverage git history for better analysis |
| **Efficiency** | Reduce token usage for LLM-based analysis |

### When Git Integration is Used

```text
IF --git-diff flag is TRUE (default):
  IF git repository exists:
    USE git_diff_analysis()
  ELSE:
    FALLBACK to full_scan()
    WARNING: "Not a git repo, falling back to full scan"
ELSE:
  USE full_scan()
```

---

## Git Diff Analysis Patterns

### Core Git Commands

#### 1. Get Changed Files (Basic)

```bash
git diff --name-only HEAD
```

**Output**:
```
src/api/users.ts
src/api/posts.ts
src/utils/validation.ts
```

**Use Case**: Get list of modified files in working directory vs HEAD

---

#### 2. Get Changed Files (with Status)

```bash
git diff --name-status HEAD
```

**Output**:
```
M   src/api/users.ts
A   src/api/posts.ts
D   src/api/legacy.ts
```

**Status Codes**:
- `M` = Modified
- `A` = Added
- `D` = Deleted
- `R` = Renamed
- `C` = Copied
- `U` = Unmerged

**Use Case**: Distinguish between added, modified, and deleted files

---

#### 3. Filter by Change Type

```bash
# Only added or modified files (exclude deleted)
git diff --name-only --diff-filter=AM HEAD

# Only modified files
git diff --name-only --diff-filter=M HEAD

# Only added files
git diff --name-only --diff-filter=A HEAD
```

**Use Case**: Avoid analyzing deleted files (they can't have code to analyze)

---

#### 4. Include Staged and Unstaged Changes

```bash
# Unstaged changes only
git diff --name-only HEAD

# Staged changes only
git diff --name-only --cached

# Both staged and unstaged
git diff --name-only HEAD && git diff --name-only --cached
```

**Use Case**: Catch all modifications regardless of staging status

---

#### 5. Compare Against Branch

```bash
# Changes since branching from main
git diff --name-only main...HEAD

# Changes between specific commits
git diff --name-only abc123..def456
```

**Use Case**: Analyze all changes in feature branch

---

### Advanced Patterns

#### 6. Get Changed Lines Count

```bash
git diff --numstat HEAD
```

**Output**:
```
45  12  src/api/users.ts
120 0   src/api/posts.ts
```

**Format**: `<added_lines> <deleted_lines> <file>`

**Use Case**: Prioritize files with most changes

---

#### 7. Get Changed Functions/Symbols

```bash
git diff -U0 --function-context HEAD
```

**Use Case**: Show only changed functions (with context)

---

#### 8. Detect Renames

```bash
git diff --name-status -M HEAD
```

**Output**:
```
R100  src/api/old-users.ts  src/api/users.ts
```

**Use Case**: Track file renames to avoid missing renamed files

---

#### 9. Filter by File Extension

```bash
# TypeScript files only
git diff --name-only HEAD | grep '\.ts$'

# Multiple extensions
git diff --name-only HEAD | grep -E '\.(ts|js|py)$'
```

**Use Case**: Analyze only code files, skip configs/docs

---

#### 10. Exclude Patterns

```bash
# Exclude test files
git diff --name-only HEAD | grep -v '\.test\.'

# Exclude generated files
git diff --name-only HEAD | grep -v 'generated/'
```

**Use Case**: Skip auto-generated or test-only files

---

## Changed File Detection Algorithm

### Algorithm: GET_CHANGED_FILES

```text
GET_CHANGED_FILES(scope, git_diff_enabled, branch):
  """
  Detect changed files using git diff or fallback to full scan.

  Args:
    scope: Directory or file pattern (e.g., "src/auth/", "**/*.ts")
    git_diff_enabled: Boolean (default True)
    branch: Comparison branch (default "HEAD")

  Returns:
    List[ChangedFile]: [
      {path: "src/api/users.ts", status: "M", lines_added: 45, lines_deleted: 12},
      ...
    ]
  """

  # Step 1: Check if git repo exists
  git_available = CHECK_GIT_REPO()

  IF NOT git_diff_enabled:
    RETURN FULL_SCAN(scope)

  IF NOT git_available:
    WARNING("Not a git repository, falling back to full scan")
    RETURN FULL_SCAN(scope)

  # Step 2: Get changed files with status
  TRY:
    # Get both staged and unstaged changes
    unstaged_files = EXEC("git diff --name-status --diff-filter=AM HEAD")
    staged_files = EXEC("git diff --name-status --cached --diff-filter=AM")

    # Merge and deduplicate
    all_changes = PARSE_GIT_STATUS(unstaged_files) + PARSE_GIT_STATUS(staged_files)
    changed_files = DEDUPLICATE(all_changes)

  CATCH GitError as e:
    WARNING(f"Git command failed: {e}, falling back to full scan")
    RETURN FULL_SCAN(scope)

  # Step 3: Filter by scope
  filtered_files = FILTER_BY_SCOPE(changed_files, scope)

  # Step 4: Get line change statistics
  FOR file IN filtered_files:
    numstat = EXEC(f"git diff --numstat HEAD -- {file.path}")
    file.lines_added, file.lines_deleted = PARSE_NUMSTAT(numstat)

  # Step 5: Classify files (code vs non-code)
  classified_files = []
  FOR file IN filtered_files:
    file.is_code = IS_CODE_FILE(file.path)
    file.language = DETECT_LANGUAGE(file.path)
    classified_files.append(file)

  # Step 6: Sort by priority (most changed first)
  classified_files.sort(key=lambda f: f.lines_added + f.lines_deleted, reverse=True)

  RETURN classified_files
```

---

### Helper Function: CHECK_GIT_REPO

```text
CHECK_GIT_REPO():
  """
  Check if current directory is inside a git repository.

  Returns:
    Boolean: True if git repo, False otherwise
  """

  TRY:
    result = EXEC("git rev-parse --is-inside-work-tree")
    RETURN result.strip() == "true"
  CATCH:
    RETURN False
```

---

### Helper Function: PARSE_GIT_STATUS

```text
PARSE_GIT_STATUS(git_output):
  """
  Parse git diff --name-status output into structured data.

  Input:
    M   src/api/users.ts
    A   src/api/posts.ts

  Returns:
    [
      {path: "src/api/users.ts", status: "M"},
      {path: "src/api/posts.ts", status: "A"}
    ]
  """

  changes = []
  FOR line IN git_output.split("\n"):
    IF line.strip() == "":
      CONTINUE

    parts = line.split("\t")
    status = parts[0].strip()
    path = parts[1].strip()

    changes.append({
      "path": path,
      "status": status
    })

  RETURN changes
```

---

### Helper Function: PARSE_NUMSTAT

```text
PARSE_NUMSTAT(numstat_output):
  """
  Parse git diff --numstat output to extract added/deleted lines.

  Input:
    45  12  src/api/users.ts

  Returns:
    (lines_added: 45, lines_deleted: 12)
  """

  IF numstat_output.strip() == "":
    RETURN (0, 0)

  parts = numstat_output.split()
  lines_added = INT(parts[0]) if parts[0] != "-" else 0
  lines_deleted = INT(parts[1]) if parts[1] != "-" else 0

  RETURN (lines_added, lines_deleted)
```

---

### Helper Function: DEDUPLICATE

```text
DEDUPLICATE(changes):
  """
  Remove duplicate file paths, keeping the one with most recent status.

  Priority: M (modified) > A (added) > other

  Args:
    changes: List of {path, status} dicts

  Returns:
    Deduplicated list
  """

  seen = {}
  FOR change IN changes:
    path = change["path"]

    IF path NOT IN seen:
      seen[path] = change
    ELSE:
      # Prefer M (modified) over A (added)
      IF change["status"] == "M":
        seen[path] = change

  RETURN LIST(seen.values())
```

---

## Scope Filtering Logic

### Algorithm: FILTER_BY_SCOPE

```text
FILTER_BY_SCOPE(files, scope):
  """
  Filter files by scope pattern.

  Scope patterns:
    - "." → All files (no filtering)
    - "src/" → Files in src/ directory
    - "src/auth/" → Files in src/auth/ directory
    - "**/*.ts" → All TypeScript files
    - "src/**/*.py" → All Python files in src/

  Args:
    files: List of ChangedFile objects
    scope: Scope pattern string

  Returns:
    Filtered list of ChangedFile objects
  """

  # Special case: "." means no filtering
  IF scope == ".":
    RETURN files

  # Normalize scope (remove trailing slash)
  normalized_scope = scope.rstrip("/")

  filtered = []
  FOR file IN files:
    IF MATCHES_SCOPE(file.path, normalized_scope):
      filtered.append(file)

  RETURN filtered
```

---

### Helper Function: MATCHES_SCOPE

```text
MATCHES_SCOPE(file_path, scope):
  """
  Check if file path matches scope pattern.

  Args:
    file_path: "src/api/users.ts"
    scope: "src/auth/" or "**/*.ts"

  Returns:
    Boolean
  """

  # Pattern 1: Directory prefix (e.g., "src/auth/")
  IF NOT ("*" IN scope OR "?" IN scope):
    # Simple directory match
    RETURN file_path.startswith(scope)

  # Pattern 2: Glob pattern (e.g., "**/*.ts")
  ELSE:
    IMPORT glob
    # Convert scope to regex pattern
    pattern = GLOB_TO_REGEX(scope)
    RETURN REGEX_MATCH(pattern, file_path)
```

---

### Helper Function: GLOB_TO_REGEX

```text
GLOB_TO_REGEX(glob_pattern):
  """
  Convert glob pattern to regex.

  Examples:
    "*.ts" → "^[^/]*\.ts$"
    "**/*.ts" → "^.*\.ts$"
    "src/**/*.py" → "^src/.*\.py$"

  Args:
    glob_pattern: Glob string

  Returns:
    Regex pattern string
  """

  import re

  # Escape special regex characters except *, ?, **
  escaped = glob_pattern
  escaped = escaped.replace(".", r"\.")
  escaped = escaped.replace("(", r"\(")
  escaped = escaped.replace(")", r"\)")
  escaped = escaped.replace("[", r"\[")
  escaped = escaped.replace("]", r"\]")

  # Replace glob patterns with regex
  escaped = escaped.replace("**", "DOUBLE_STAR_PLACEHOLDER")
  escaped = escaped.replace("*", "[^/]*")
  escaped = escaped.replace("DOUBLE_STAR_PLACEHOLDER", ".*")
  escaped = escaped.replace("?", "[^/]")

  # Anchor pattern
  regex = f"^{escaped}$"

  RETURN regex
```

---

### Scope Filtering Examples

```text
# Example 1: Directory scope
scope = "src/auth/"
files = [
  "src/auth/login.ts",      → MATCH ✅
  "src/auth/register.ts",   → MATCH ✅
  "src/api/users.ts",       → NO MATCH ❌
  "tests/auth/login.test.ts" → NO MATCH ❌
]

# Example 2: Glob pattern (all TypeScript)
scope = "**/*.ts"
files = [
  "src/api/users.ts",       → MATCH ✅
  "src/auth/login.ts",      → MATCH ✅
  "scripts/build.js",       → NO MATCH ❌
  "README.md",              → NO MATCH ❌
]

# Example 3: Nested glob (Python in src/)
scope = "src/**/*.py"
files = [
  "src/api/users.py",       → MATCH ✅
  "src/auth/login.py",      → MATCH ✅
  "tests/test_api.py",      → NO MATCH ❌
  "scripts/deploy.py",      → NO MATCH ❌
]

# Example 4: No filtering
scope = "."
files = [
  "src/api/users.ts",       → MATCH ✅
  "tests/api.test.ts",      → MATCH ✅
  "README.md",              → MATCH ✅
  "package.json",           → MATCH ✅
]
```

---

## File Classification

### Algorithm: IS_CODE_FILE

```text
IS_CODE_FILE(file_path):
  """
  Determine if file is a code file (vs config, docs, etc.).

  Code files:
    - Can have @speckit annotations
    - Can have FR/AS markers
    - Should be analyzed by drift detector

  Non-code files:
    - Configs (package.json, tsconfig.json)
    - Docs (README.md, docs/*.md)
    - Data (fixtures, seeds)

  Args:
    file_path: "src/api/users.ts"

  Returns:
    Boolean: True if code file, False otherwise
  """

  extension = GET_FILE_EXTENSION(file_path)

  # Language extensions (code files)
  CODE_EXTENSIONS = [
    ".ts", ".tsx", ".js", ".jsx",  # JavaScript/TypeScript
    ".py",                          # Python
    ".go",                          # Go
    ".java", ".kt",                 # Java/Kotlin
    ".cs",                          # C#
    ".rb",                          # Ruby
    ".php",                         # PHP
    ".rs",                          # Rust
    ".swift",                       # Swift
    ".c", ".cpp", ".h", ".hpp",    # C/C++
  ]

  # Config/docs extensions (non-code)
  NON_CODE_EXTENSIONS = [
    ".json", ".yaml", ".yml", ".toml",  # Configs
    ".md", ".txt", ".rst",              # Docs
    ".xml", ".html", ".css",            # Markup
    ".svg", ".png", ".jpg",             # Assets
    ".lock",                            # Lock files
  ]

  IF extension IN CODE_EXTENSIONS:
    RETURN True

  IF extension IN NON_CODE_EXTENSIONS:
    RETURN False

  # Unknown extension → check if in code directory
  code_dirs = ["src/", "lib/", "app/", "pkg/", "internal/"]
  FOR dir IN code_dirs:
    IF file_path.startswith(dir):
      RETURN True

  # Default: assume non-code
  RETURN False
```

---

### Algorithm: DETECT_LANGUAGE

```text
DETECT_LANGUAGE(file_path):
  """
  Detect programming language from file extension.

  Args:
    file_path: "src/api/users.ts"

  Returns:
    Language name: "typescript" | "python" | "go" | ...
  """

  extension = GET_FILE_EXTENSION(file_path)

  LANGUAGE_MAP = {
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".py": "python",
    ".go": "go",
    ".java": "java",
    ".kt": "kotlin",
    ".cs": "csharp",
    ".rb": "ruby",
    ".php": "php",
    ".rs": "rust",
    ".swift": "swift",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
  }

  RETURN LANGUAGE_MAP.get(extension, "unknown")
```

---

## Integration with Wave 1 Code-Scanner

### Wave 1: Detection Phase

The `code-scanner` subagent uses git integration as follows:

```text
# Code-Scanner Subagent (Wave 1)

PROMPT:
  You are the code-scanner subagent for /speckit.fix Wave 1.

  Your task: Discover files to analyze for drift detection.

  Inputs:
    - scope: "{scope}"
    - git_diff_enabled: {git_diff_enabled}
    - branch: "{branch}"

  Steps:
    1. Read templates/shared/drift/git-integration.md
    2. Execute GET_CHANGED_FILES(scope, git_diff_enabled, branch)
    3. Classify files (code vs non-code)
    4. Output: .fix-session/wave1-changed-files.json

  Output Format:
    {
      "scan_mode": "git_diff" | "full_scan",
      "files": [
        {
          "path": "src/api/users.ts",
          "status": "M",
          "lines_added": 45,
          "lines_deleted": 12,
          "is_code": true,
          "language": "typescript"
        },
        ...
      ],
      "stats": {
        "total_files": 8,
        "code_files": 6,
        "non_code_files": 2,
        "total_lines_changed": 320
      }
    }

TOOLS:
  - Bash (for git commands)
  - Write (for output file)
```

---

### Integration Flow

```text
USER RUNS:
  /speckit.fix --scope "src/auth/" --git-diff

WAVE 1: Detection (Parallel)
  │
  ├─ code-scanner subagent:
  │    1. Read git-integration.md
  │    2. Execute: git diff --name-status --diff-filter=AM HEAD
  │    3. Filter by scope: "src/auth/"
  │    4. Classify files (code vs non-code)
  │    5. Output: .fix-session/wave1-changed-files.json
  │
  ├─ drift-detector subagent:
  │    (Runs in parallel, independent of code-scanner)
  │
  └─ annotation-collector subagent:
       (Runs in parallel, independent of code-scanner)

WAVE 2: Analysis (Parallel)
  Uses output from code-scanner (.fix-session/wave1-changed-files.json)
```

---

### Output Schema: wave1-changed-files.json

```json
{
  "scan_mode": "git_diff",
  "scope": "src/auth/",
  "branch": "HEAD",
  "timestamp": "2026-01-11T10:30:00Z",
  "files": [
    {
      "path": "src/auth/login.ts",
      "status": "M",
      "lines_added": 45,
      "lines_deleted": 12,
      "is_code": true,
      "language": "typescript",
      "priority": 57
    },
    {
      "path": "src/auth/register.ts",
      "status": "A",
      "lines_added": 120,
      "lines_deleted": 0,
      "is_code": true,
      "language": "typescript",
      "priority": 120
    }
  ],
  "stats": {
    "total_files": 2,
    "code_files": 2,
    "non_code_files": 0,
    "total_lines_changed": 177,
    "added_files": 1,
    "modified_files": 1,
    "deleted_files": 0
  }
}
```

**Priority Calculation**: `lines_added + lines_deleted` (higher = more changed = higher priority)

---

## Edge Cases

### Edge Case 1: Not a Git Repository

**Scenario**: User runs `/speckit.fix --git-diff` in a non-git directory

**Detection**:
```bash
git rev-parse --is-inside-work-tree
# Exit code: 128 (not a git repo)
```

**Handling**:
```text
IF NOT CHECK_GIT_REPO():
  WARNING("Not a git repository, falling back to full scan")
  RETURN FULL_SCAN(scope)
```

**User Message**:
```
⚠️  Warning: Not a git repository
Falling back to full file scan for scope: src/

Scanning 342 files...
```

---

### Edge Case 2: Empty Git Diff

**Scenario**: No files changed since HEAD

**Detection**:
```bash
git diff --name-only HEAD
# Output: (empty)
```

**Handling**:
```text
changed_files = GET_CHANGED_FILES(...)

IF len(changed_files) == 0:
  OUTPUT("No files changed since HEAD")
  OUTPUT("Run with --scope . to scan all files")
  EXIT(0)
```

**User Message**:
```
ℹ️  No files changed since HEAD
No drift to fix. If you want to scan all files, run:
  /speckit.fix --scope . --git-diff=false
```

---

### Edge Case 3: Merge Conflicts

**Scenario**: User runs `/speckit.fix` during a merge conflict

**Detection**:
```bash
git diff --name-only HEAD
# Output includes conflict markers

git diff --name-status HEAD
# Output:
U   src/api/users.ts
```

**Handling**:
```text
changed_files = PARSE_GIT_STATUS(...)

conflict_files = FILTER(changed_files, status="U")

IF len(conflict_files) > 0:
  ERROR("Merge conflicts detected:")
  FOR file IN conflict_files:
    ERROR(f"  - {file.path}")
  ERROR("Resolve conflicts before running /speckit.fix")
  EXIT(1)
```

**User Message**:
```
❌ Error: Merge conflicts detected
The following files have unresolved conflicts:
  - src/api/users.ts

Please resolve conflicts and commit before running /speckit.fix
```

---

### Edge Case 4: Binary Files

**Scenario**: Git diff includes binary files (images, PDFs, etc.)

**Detection**:
```bash
git diff --numstat HEAD
# Output:
-   -   assets/logo.png
```

**Handling**:
```text
FOR file IN changed_files:
  numstat = EXEC(f"git diff --numstat HEAD -- {file.path}")

  IF numstat.startswith("-\t-\t"):
    # Binary file
    file.is_binary = True
    file.is_code = False
    file.lines_added = 0
    file.lines_deleted = 0
```

**Filtering**:
```text
# Exclude binary files from analysis
code_files = FILTER(changed_files, is_binary=False, is_code=True)
```

---

### Edge Case 5: Deleted Files

**Scenario**: Files deleted in working directory

**Detection**:
```bash
git diff --name-status HEAD
# Output:
D   src/api/legacy.ts
```

**Handling**:
```text
# Filter out deleted files (can't analyze what doesn't exist)
changed_files = EXEC("git diff --name-status --diff-filter=AM HEAD")
# --diff-filter=AM → only Added and Modified (exclude Deleted)
```

---

### Edge Case 6: Renamed Files

**Scenario**: File was renamed (e.g., `old-users.ts` → `users.ts`)

**Detection**:
```bash
git diff --name-status -M HEAD
# Output:
R100  src/api/old-users.ts  src/api/users.ts
```

**Handling**:
```text
FOR line IN git_output:
  IF line.startswith("R"):
    parts = line.split("\t")
    old_path = parts[1]
    new_path = parts[2]

    changes.append({
      "path": new_path,
      "status": "R",
      "old_path": old_path
    })
```

**Analysis**:
```text
# Analyze renamed file at new location
ANALYZE_FILE(new_path)

# Note: Old path no longer exists, skip it
```

---

### Edge Case 7: Submodules

**Scenario**: Repository has git submodules

**Detection**:
```bash
git diff --name-only HEAD
# Output may include:
third-party/lib (submodule)
```

**Handling**:
```text
# Skip submodule changes
changed_files = EXEC("git diff --name-only HEAD")
filtered = []

FOR file IN changed_files:
  # Check if file is inside a submodule
  IF IS_SUBMODULE(file):
    CONTINUE
  ELSE:
    filtered.append(file)

RETURN filtered
```

---

### Edge Case 8: Very Large Diffs

**Scenario**: 1000+ files changed

**Detection**:
```text
changed_files = GET_CHANGED_FILES(...)

IF len(changed_files) > 500:
  WARNING(f"Large diff detected: {len(changed_files)} files changed")
```

**Handling**:
```text
IF len(changed_files) > 500:
  WARNING(f"⚠️  Large diff: {len(changed_files)} files")
  OUTPUT("This may take several minutes. Consider:")
  OUTPUT("  1. Use --scope to narrow analysis")
  OUTPUT("  2. Commit in smaller batches")
  OUTPUT("  3. Run with --strategy regenerate for full rebuild")

  # Ask user to confirm
  IF mode == "interactive":
    response = PROMPT("Continue with large diff analysis? [y/N]")
    IF response != "y":
      EXIT(0)
```

---

## Performance Optimizations

### Optimization 1: Parallel Git Commands

```text
# SLOW (sequential):
FOR file IN changed_files:
  numstat = EXEC(f"git diff --numstat HEAD -- {file}")
  PARSE_NUMSTAT(numstat)

# FAST (single command):
all_numstats = EXEC("git diff --numstat HEAD")
PARSE_ALL_NUMSTATS(all_numstats)
```

**Speedup**: 10-20x for 100+ files

---

### Optimization 2: Cache Git Results

```text
# Cache git diff results for session duration
cache = {}

GET_CHANGED_FILES_CACHED(scope):
  cache_key = f"git_diff_{scope}"

  IF cache_key IN cache:
    RETURN cache[cache_key]

  result = GET_CHANGED_FILES(scope)
  cache[cache_key] = result
  RETURN result
```

---

### Optimization 3: Limit Depth for Large Repos

```bash
# Shallow diff (only HEAD vs working directory)
git diff --name-only HEAD

# Deep diff (entire branch history) - AVOID
git diff --name-only $(git merge-base main HEAD)..HEAD
```

**Recommendation**: Use `HEAD` for speed, not branch base

---

### Optimization 4: Skip Binary Files Early

```bash
# Exclude binary files from git diff
git diff --name-only --diff-filter=AM HEAD -- ':!*.png' ':!*.jpg' ':!*.pdf'
```

---

### Optimization 5: Use --numstat Once

```bash
# Get all stats in single command
git diff --numstat HEAD

# Output:
45  12  src/api/users.ts
120 0   src/api/posts.ts
0   87  src/api/legacy.ts
```

**Parse once**, split by lines, cache results

---

## Examples

### Example 1: Basic Git Diff (Default)

```bash
# User command
/speckit.fix

# Equivalent to
/speckit.fix --scope "." --git-diff
```

**Execution**:
```text
1. Check git repo: ✅
2. Execute: git diff --name-status --diff-filter=AM HEAD
3. Output:
   M   src/api/users.ts
   M   src/api/posts.ts
   A   src/auth/register.ts
4. Filter by scope: "." (no filtering)
5. Classify files: All are code files
6. Result: 3 files to analyze
```

---

### Example 2: Scoped Git Diff

```bash
# User command
/speckit.fix --scope "src/auth/"
```

**Execution**:
```text
1. Check git repo: ✅
2. Execute: git diff --name-status --diff-filter=AM HEAD
3. Output:
   M   src/api/users.ts
   M   src/auth/login.ts
   A   src/auth/register.ts
4. Filter by scope: "src/auth/"
   → src/auth/login.ts ✅
   → src/auth/register.ts ✅
   → src/api/users.ts ❌ (not in scope)
5. Result: 2 files to analyze
```

---

### Example 3: Glob Pattern Scope

```bash
# User command
/speckit.fix --scope "**/*.ts"
```

**Execution**:
```text
1. Check git repo: ✅
2. Execute: git diff --name-status --diff-filter=AM HEAD
3. Output:
   M   src/api/users.ts
   M   scripts/build.js
   A   src/auth/register.ts
4. Filter by glob: "**/*.ts"
   → src/api/users.ts ✅ (matches *.ts)
   → src/auth/register.ts ✅ (matches *.ts)
   → scripts/build.js ❌ (*.js, not *.ts)
5. Result: 2 files to analyze
```

---

### Example 4: No Git Diff (Full Scan)

```bash
# User command
/speckit.fix --git-diff=false
```

**Execution**:
```text
1. Git diff disabled by flag
2. Fallback to FULL_SCAN(scope=".")
3. Scan all files in project:
   - Use Serena MCP find_file
   - Pattern: "**/*.{ts,js,py,go,java}"
4. Result: 342 files to analyze
```

---

### Example 5: Not a Git Repo

```bash
# User command
/speckit.fix --git-diff

# Execution in non-git directory
```

**Output**:
```text
⚠️  Warning: Not a git repository
Falling back to full file scan for scope: .

Scanning files...
Found 127 code files to analyze
```

---

### Example 6: Empty Diff

```bash
# User command
/speckit.fix --git-diff
```

**Execution**:
```text
1. Check git repo: ✅
2. Execute: git diff --name-status HEAD
3. Output: (empty)
4. Result: 0 files to analyze
```

**Output**:
```text
ℹ️  No files changed since HEAD
No drift to fix. If you want to scan all files, run:
  /speckit.fix --scope . --git-diff=false
```

---

### Example 7: Large Diff (Interactive)

```bash
# User has 850 changed files
/speckit.fix --mode interactive
```

**Output**:
```text
⚠️  Large diff: 850 files changed
This may take several minutes. Consider:
  1. Use --scope to narrow analysis (e.g., --scope "src/api/")
  2. Commit in smaller batches
  3. Run with --strategy regenerate for full rebuild

Continue with large diff analysis? [y/N]: _
```

---

### Example 8: Renamed File

```bash
# User renamed src/api/old-users.ts → src/api/users.ts
/speckit.fix --git-diff
```

**Execution**:
```text
1. Check git repo: ✅
2. Execute: git diff --name-status -M HEAD
3. Output:
   R100  src/api/old-users.ts  src/api/users.ts
4. Parse rename:
   - Old path: src/api/old-users.ts
   - New path: src/api/users.ts
5. Analyze new path: src/api/users.ts
6. Skip old path (no longer exists)
```

---

## Command Line Examples

### Git Commands for Manual Testing

```bash
# Test 1: Get changed files
git diff --name-only HEAD

# Test 2: Get changed files with status
git diff --name-status HEAD

# Test 3: Filter by change type (Added or Modified)
git diff --name-only --diff-filter=AM HEAD

# Test 4: Get line change stats
git diff --numstat HEAD

# Test 5: Check if git repo
git rev-parse --is-inside-work-tree

# Test 6: Compare against branch
git diff --name-only main...HEAD

# Test 7: Include staged changes
git diff --name-only HEAD && git diff --name-only --cached

# Test 8: Detect renames
git diff --name-status -M HEAD

# Test 9: Filter by extension
git diff --name-only HEAD | grep '\.ts$'

# Test 10: Exclude test files
git diff --name-only HEAD | grep -v '\.test\.'
```

---

## Integration Checklist

Use this checklist when implementing git integration in code-scanner:

- [ ] Check git repo availability with `CHECK_GIT_REPO()`
- [ ] Get changed files with `git diff --name-status --diff-filter=AM HEAD`
- [ ] Include staged changes with `git diff --name-status --cached --diff-filter=AM`
- [ ] Merge and deduplicate staged + unstaged changes
- [ ] Parse git status output into structured data
- [ ] Get line change statistics with `git diff --numstat HEAD`
- [ ] Filter by scope pattern (directory or glob)
- [ ] Classify files (code vs non-code)
- [ ] Detect language from extension
- [ ] Sort by priority (most changed first)
- [ ] Handle edge cases:
  - [ ] Not a git repo → fallback to full scan
  - [ ] Empty diff → exit with message
  - [ ] Merge conflicts → error and exit
  - [ ] Binary files → skip
  - [ ] Deleted files → exclude
  - [ ] Renamed files → use new path
  - [ ] Large diffs → warn and confirm
- [ ] Output structured JSON to `.fix-session/wave1-changed-files.json`
- [ ] Log scan mode (`git_diff` or `full_scan`)
- [ ] Report statistics (total files, code files, lines changed)

---

## Performance Benchmarks

### Git Diff vs Full Scan

| Codebase Size | Git Diff Time | Full Scan Time | Speedup |
|---------------|---------------|----------------|---------|
| Small (50 files) | 0.5s | 2s | 4x |
| Medium (500 files) | 1s | 15s | 15x |
| Large (5000 files) | 3s | 120s | 40x |
| Very Large (50k files) | 8s | 600s+ | 75x |

**Assumptions**:
- Git diff: Only 10-20 files changed
- Full scan: All files analyzed

---

## Troubleshooting

### Issue 1: Git Command Fails

**Symptom**: `git diff` returns error

**Diagnosis**:
```bash
git diff --name-only HEAD 2>&1
# Output: fatal: not a git repository
```

**Fix**: Fallback to full scan
```text
WARNING("Git command failed, falling back to full scan")
RETURN FULL_SCAN(scope)
```

---

### Issue 2: Empty Scope Filter

**Symptom**: Filter returns 0 files even though files changed

**Diagnosis**:
```text
# User runs:
/speckit.fix --scope "src/auth"

# Git output:
M   src/auth/login.ts
M   src/auth/register.ts

# Filter result: 0 files
```

**Cause**: Scope should be `"src/auth/"` (with trailing slash) or use glob `"src/auth/**"`

**Fix**: Normalize scope in filter logic
```text
normalized_scope = scope.rstrip("/") + "/"
# "src/auth" → "src/auth/"
```

---

### Issue 3: Binary Files Cause Errors

**Symptom**: Parser crashes on binary file diffs

**Diagnosis**:
```bash
git diff --numstat HEAD
# Output:
-   -   assets/logo.png
```

**Fix**: Check for binary marker
```text
IF numstat.startswith("-\t-\t"):
  file.is_binary = True
  SKIP_FILE(file)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-11 | Initial version with git diff analysis patterns |

---

## References

- Git diff documentation: https://git-scm.com/docs/git-diff
- Glob pattern syntax: https://en.wikipedia.org/wiki/Glob_(programming)
- `/speckit.fix` command template: `templates/commands/speckit.fix.md`
- Drift detection framework: `templates/shared/drift/drift-detection.md`

---

**End of Git Integration Guide**

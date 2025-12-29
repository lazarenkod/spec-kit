# Build Optimizer

## Purpose

Pre-compile build error patterns and optimize the build-until-works loop for faster iteration cycles.

## Performance Impact

| Mode | Time | Savings |
|------|------|---------|
| Runtime pattern matching | 15-45s | baseline |
| Pre-compiled patterns | 10-20s | 50% |

## Configuration

```yaml
build_optimizer:
  enabled: true
  skip_flag: "--no-build-fix"
  max_attempts: 3
  precompile_patterns: true
  smart_retry: true
```

## Pre-compiled Pattern Registry

```text
# Initialize at session start, not per-build
COMPILED_PATTERNS = None

FUNCTION initialize_build_optimizer():
  global COMPILED_PATTERNS

  IF COMPILED_PATTERNS IS NOT None:
    RETURN  # Already initialized

  COMPILED_PATTERNS = {
    "typescript": [
      {
        pattern: re.compile(r"Cannot find module '([^']+)'"),
        rule: "BF-001",
        action: "add_import",
        extract: lambda m: {"module": m.group(1)}
      },
      {
        pattern: re.compile(r"'([^']+)' is declared but its value is never read"),
        rule: "BF-002",
        action: "prefix_unused",
        extract: lambda m: {"variable": m.group(1)}
      },
      {
        pattern: re.compile(r"Property '([^']+)' does not exist on type"),
        rule: "BF-003",
        action: "add_type_annotation",
        extract: lambda m: {"property": m.group(1)}
      },
      {
        pattern: re.compile(r"TS(\d+):"),
        rule: "BF-GENERIC",
        action: "log_ts_error",
        extract: lambda m: {"error_code": m.group(1)}
      }
    ],

    "react": [
      {
        pattern: re.compile(r'Each child in a list should have a unique "key" prop'),
        rule: "BF-004",
        action: "add_key_prop",
        extract: lambda m: {}
      },
      {
        pattern: re.compile(r"React Hook ([^\s]+) is called conditionally"),
        rule: "BF-005",
        action: "move_hook_to_top",
        extract: lambda m: {"hook": m.group(1)}
      }
    ],

    "python": [
      {
        pattern: re.compile(r"ModuleNotFoundError: No module named '([^']+)'"),
        rule: "BF-001",
        action: "add_import",
        extract: lambda m: {"module": m.group(1)}
      },
      {
        pattern: re.compile(r"NameError: name '([^']+)' is not defined"),
        rule: "BF-006",
        action: "add_import_or_define",
        extract: lambda m: {"name": m.group(1)}
      },
      {
        pattern: re.compile(r"IndentationError:"),
        rule: "BF-INDENT",
        action: "fix_indentation",
        extract: lambda m: {}
      }
    ],

    "go": [
      {
        pattern: re.compile(r'undefined: ([^\s]+)'),
        rule: "BF-001",
        action: "add_import",
        extract: lambda m: {"identifier": m.group(1)}
      },
      {
        pattern: re.compile(r"([^\s]+) declared but not used"),
        rule: "BF-002",
        action: "prefix_unused",
        extract: lambda m: {"variable": m.group(1)}
      }
    ],

    "rust": [
      {
        pattern: re.compile(r"cannot find .+ `([^`]+)` in this scope"),
        rule: "BF-001",
        action: "add_use_statement",
        extract: lambda m: {"item": m.group(1)}
      },
      {
        pattern: re.compile(r"unused variable: `([^`]+)`"),
        rule: "BF-002",
        action: "prefix_unused",
        extract: lambda m: {"variable": m.group(1)}
      }
    ],

    "kotlin": [
      {
        pattern: re.compile(r"Unresolved reference: ([^\s]+)"),
        rule: "BF-001",
        action: "add_import",
        extract: lambda m: {"reference": m.group(1)}
      },
      {
        pattern: re.compile(r"Variable '([^']+)' is never used"),
        rule: "BF-002",
        action: "prefix_unused",
        extract: lambda m: {"variable": m.group(1)}
      },
      {
        pattern: re.compile(r"Classifier '([^']+)' does not have a companion object"),
        rule: "BF-007",
        action: "add_companion_object",
        extract: lambda m: {"class_name": m.group(1)}
      },
      {
        pattern: re.compile(r"'([^']+)' is a suspend function"),
        rule: "BF-008",
        action: "wrap_in_coroutine_scope",
        extract: lambda m: {"function": m.group(1)}
      }
    ],

    "java": [
      {
        pattern: re.compile(r"cannot find symbol.*symbol:\s*class ([^\s]+)"),
        rule: "BF-001",
        action: "add_import",
        extract: lambda m: {"class_name": m.group(1)}
      },
      {
        pattern: re.compile(r"variable ([^\s]+) is never used"),
        rule: "BF-002",
        action: "prefix_unused",
        extract: lambda m: {"variable": m.group(1)}
      },
      {
        pattern: re.compile(r"package ([^\s]+) does not exist"),
        rule: "BF-001",
        action: "add_import",
        extract: lambda m: {"package": m.group(1)}
      }
    ],

    "eslint": [
      {
        pattern: re.compile(r"'([^']+)' is defined but never used"),
        rule: "BF-002",
        action: "prefix_unused",
        extract: lambda m: {"variable": m.group(1)}
      }
    ]
  }

  LOG f"✓ Build optimizer initialized: {sum(len(v) for v in COMPILED_PATTERNS.values())} patterns pre-compiled"
```

## Fast Pattern Matching

```text
FUNCTION fast_match_errors(build_output, detected_language):
  # Ensure patterns are initialized
  initialize_build_optimizer()

  matches = []
  lines = build_output.split('\n')

  # Get relevant pattern sets
  pattern_sets = []
  IF detected_language IN COMPILED_PATTERNS:
    pattern_sets.append((detected_language, COMPILED_PATTERNS[detected_language]))

  # Always check eslint patterns for JS/TS projects
  IF detected_language IN ["typescript", "javascript"]:
    pattern_sets.append(("eslint", COMPILED_PATTERNS.get("eslint", [])))
    pattern_sets.append(("react", COMPILED_PATTERNS.get("react", [])))

  # Match against all relevant patterns
  FOR line IN lines:
    FOR lang, patterns IN pattern_sets:
      FOR p IN patterns:
        match = p.pattern.search(line)
        IF match:
          matches.append({
            line: line,
            rule: p.rule,
            action: p.action,
            data: p.extract(match),
            language: lang
          })
          BREAK  # One match per line

  RETURN matches
```

## Smart Retry Strategy

```text
SMART_RETRY_STRATEGY = {
  iteration_1: {
    timeout: 30000,      # 30s - first build may be cold
    fix_scope: "targeted",  # Only fix exact matches
    aggressive_mode: false
  },
  iteration_2: {
    timeout: 20000,      # 20s - cache is warm
    fix_scope: "expanded",  # Fix related issues
    aggressive_mode: false
  },
  iteration_3: {
    timeout: 15000,      # 15s - final attempt
    fix_scope: "full",      # Try all possible fixes
    aggressive_mode: true   # Allow speculative fixes
  }
}

FUNCTION get_retry_config(iteration):
  key = f"iteration_{min(iteration, 3)}"
  RETURN SMART_RETRY_STRATEGY[key]
```

## Build Command Detection

```text
FUNCTION detect_build_command():
  # Cache build command for session
  IF SESSION_CACHE.has("build_cmd"):
    RETURN SESSION_CACHE.get("build_cmd")

  cmd = None
  lang = None

  IF exists("package.json"):
    pkg = json.load("package.json")
    IF "build" IN pkg.get("scripts", {}):
      cmd = detect_package_manager() + " run build"
    ELSE:
      cmd = detect_package_manager() + " run tsc"  # Fallback to tsc
    lang = "typescript" IF exists("tsconfig.json") ELSE "javascript"

  ELIF exists("Cargo.toml"):
    cmd = "cargo build"
    lang = "rust"

  ELIF exists("go.mod"):
    cmd = "go build ./..."
    lang = "go"

  ELIF exists("pyproject.toml"):
    cmd = "python -m py_compile $(find . -name '*.py' | head -20)"
    lang = "python"

  ELIF exists("build.gradle") OR exists("build.gradle.kts"):
    cmd = "./gradlew build -x test"
    lang = "kotlin" IF exists("*.kt") ELSE "java"

  ELIF exists("pom.xml"):
    cmd = "mvn compile -q"
    lang = "java"

  SESSION_CACHE.set("build_cmd", cmd)
  SESSION_CACHE.set("build_lang", lang)

  RETURN cmd, lang
```

## Optimized Build Loop

```text
FUNCTION optimized_build_loop():
  initialize_build_optimizer()

  build_cmd, lang = detect_build_command()

  FOR iteration IN range(1, MAX_ATTEMPTS + 1):
    config = get_retry_config(iteration)

    # Run build with timeout
    start_time = now()
    result = run_with_timeout(build_cmd, config.timeout)
    build_time = now() - start_time

    IF result.exit_code == 0:
      LOG f"✅ Build successful on attempt {iteration} ({build_time}ms)"
      RETURN SUCCESS

    # Fast pattern matching
    match_start = now()
    errors = fast_match_errors(result.stderr, lang)
    match_time = now() - match_start

    LOG f"Pattern matching: {len(errors)} errors in {match_time}ms"

    # Apply fixes based on scope
    fixes_applied = 0
    FOR error IN errors:
      IF config.fix_scope == "targeted":
        IF apply_targeted_fix(error):
          fixes_applied++
      ELIF config.fix_scope == "expanded":
        IF apply_expanded_fix(error):
          fixes_applied++
      ELIF config.fix_scope == "full":
        IF apply_full_fix(error, aggressive=config.aggressive_mode):
          fixes_applied++

    IF fixes_applied == 0:
      LOG f"⚠️ No auto-fixes available for {len(errors)} errors"
      IF iteration == MAX_ATTEMPTS:
        RETURN BLOCKED
      CONTINUE

    LOG f"🔧 Applied {fixes_applied} fixes, retrying..."

  RETURN BLOCKED
```

## Integration with implement.md

Reference in Step 0.5 (Build-Until-Works Loop):

```text
Read `templates/shared/implement/build-optimizer.md` and apply.

# At session start
initialize_build_optimizer()

# In build loop
result = optimized_build_loop()
```

## Output Format

```text
🔨 Build Optimizer
├── Patterns pre-compiled: 47
├── Build command: npm run build
├── Language: typescript
├── Attempt 1/3
│   ├── Build time: 2.3s
│   ├── Exit code: 1 (5 errors)
│   ├── Pattern matching: 8ms
│   ├── Matches found: 4
│   └── Fixes applied: 4
│       ├── BF-001: Added import for 'lodash'
│       ├── BF-002: Prefixed '_unused' in types.ts:45
│       ├── BF-004: Added key={item.id} in List.tsx
│       └── BF-004: Added key={index} in Grid.tsx
├── Attempt 2/3
│   ├── Build time: 1.8s (cache warm)
│   ├── Exit code: 0
│   └── Build: SUCCESS ✅
└── Total time: 4.1s (vs ~15s without optimizer)
```

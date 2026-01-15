# Implementation Plan: Project-Level Model Cap Feature

**Feature**: Hard model cap enforcement from `memory/constitution.md`  
**Date**: 2026-01-11  
**Status**: Design Complete

---

## Executive Summary

This plan implements a project-level model cap system where users can set `max_model: sonnet` in `memory/constitution.md` to automatically downgrade opus → sonnet for all commands. The feature is opt-in (opus works normally by default) and provides transparent cost control without breaking existing functionality.

### Key Design Decisions

1. **Schema Location**: Add `max_model` to "Project Settings" table in constitution.md (lines 38-46)
2. **Loading Point**: Parse constitution during template config loading in `template_parser.py`
3. **Application Point**: Apply cap in `resolve_model()` function before model ID resolution
4. **User Feedback**: Silent downgrade with optional verbose logging (CLI flag)
5. **Backward Compatibility**: Feature is fully opt-in; missing `max_model` = no cap

---

## Architecture Overview

### Model Resolution Flow (Current → Enhanced)

```
┌─────────────────────────────────────────────────────────────────┐
│                     CURRENT FLOW                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Load command template (e.g., concept.md)                    │
│  2. Parse YAML frontmatter → extract "model: opus"              │
│  3. resolve_model(override=None, default="opus")                │
│  4. MODEL_MAP lookup → "claude-opus-4-5-20251101"               │
│  5. Create AgentTask with resolved model                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     ENHANCED FLOW (with cap)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Load command template (e.g., concept.md)                    │
│  2. Parse YAML frontmatter → extract "model: opus"              │
│  3. Load constitution.md → parse max_model setting              │
│  4. resolve_model(override=None, default="opus", cap="sonnet")  │
│  5. Apply downgrade logic: opus → sonnet (if capped)            │
│  6. MODEL_MAP lookup → "claude-sonnet-4-5-20250929"             │
│  7. Create AgentTask with capped model                          │
│  8. (Optional) Log downgrade event                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | File | Responsibility |
|-----------|------|----------------|
| **Constitution Schema** | `memory/constitution.md` | Define max_model setting |
| **Constitution Parser** | `src/specify_cli/template_parser.py` | Load and parse max_model from constitution |
| **Model Resolver** | `src/specify_cli/template_parser.py` | Apply downgrade logic |
| **CLI Integration** | `src/specify_cli/__init__.py` | Pass verbose flag to parser |

---

## Detailed Implementation

### 1. Constitution Schema Update

**File**: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/memory/constitution.md`

**Location**: Lines 38-46 (Project Settings table)

**Change**: Add new row to settings table

```markdown
| Setting | Value | Description |
|---------|-------|-------------|
| **language** | `en` | Primary language for generated artifacts. Options: `en` (English), `ru` (Russian), ... |
| **date_format** | `ISO` | Date format in documents. Options: `ISO` (2024-01-15), `US` (01/15/2024), `EU` (15.01.2024) |
| **measurements** | `metric` | Unit system. Options: `metric`, `imperial` |
| **max_model** | `none` | Maximum Claude model tier allowed. Options: `opus` (unrestricted), `sonnet` (cap at Sonnet), `haiku` (cap at Haiku), `none` (same as opus). When set, automatically downgrades higher-tier models to stay within budget. |
```

**Default Value**: `none` (meaning no cap, opus works normally)

**Alternative Syntax** (YAML block in constitution):

```yaml
# Project Configuration
project_settings:
  language: en
  date_format: ISO
  measurements: metric
  max_model: sonnet  # opus | sonnet | haiku | none
```

**Recommendation**: Use Markdown table format (simpler, consistent with existing style).

---

### 2. Constitution Parser Implementation

**File**: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/src/specify_cli/template_parser.py`

#### 2.1 Add Constitution Loading Function

**Insert after line 59** (after MODEL_MAP definition):

```python
# Model tier hierarchy for cap enforcement
MODEL_TIER_HIERARCHY = {
    "opus": 3,
    "sonnet": 2,
    "haiku": 1,
}


def load_constitution_settings(project_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load project settings from constitution.md.
    
    Searches for constitution.md in:
    1. {project_root}/memory/constitution.md
    2. ./memory/constitution.md (if project_root is None)
    3. Returns empty dict if not found
    
    Args:
        project_root: Optional project root path
    
    Returns:
        Dict with settings like {"max_model": "sonnet", "language": "en"}
    """
    if project_root is None:
        project_root = Path.cwd()
    
    constitution_path = project_root / "memory" / "constitution.md"
    
    if not constitution_path.exists():
        return {}
    
    try:
        content = constitution_path.read_text(encoding="utf-8")
        return parse_constitution_settings(content)
    except Exception:
        return {}  # Fail silently, don't block execution


def parse_constitution_settings(content: str) -> Dict[str, Any]:
    """
    Parse Project Settings table from constitution.md.
    
    Looks for markdown table with format:
    | **max_model** | `sonnet` | ...
    
    Args:
        content: Full constitution.md content
    
    Returns:
        Dict of settings
    """
    settings = {}
    
    # Find Project Settings section
    lines = content.split("\n")
    in_settings_section = False
    
    for line in lines:
        # Detect section start
        if "## Project Settings" in line:
            in_settings_section = True
            continue
        
        # Detect section end (next ## heading)
        if in_settings_section and line.startswith("## ") and "Project Settings" not in line:
            break
        
        # Parse table rows
        if in_settings_section and "|" in line:
            # Match: | **max_model** | `sonnet` | ...
            match = re.match(r'\|\s*\*\*(\w+)\*\*\s*\|\s*`([^`]+)`\s*\|', line)
            if match:
                key, value = match.groups()
                settings[key] = value.strip()
    
    return settings
```

**Why this approach?**
- Robust: Works even if table format varies slightly
- Fast: Regex-based parsing, no YAML parsing overhead
- Fail-safe: Returns empty dict on any error (doesn't block CLI)

---

#### 2.2 Enhance `resolve_model()` Function

**File**: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/src/specify_cli/template_parser.py`

**Replace function at lines 181-198**:

```python
def resolve_model(
    model_override: Optional[str],
    default_model: str,
    max_model: Optional[str] = None,
    verbose: bool = False,
) -> Tuple[str, bool]:
    """
    Resolve a model name to full model ID with optional cap enforcement.
    
    Model downgrade logic:
    - If max_model is set and resolved model exceeds cap → downgrade
    - Hierarchy: opus (3) > sonnet (2) > haiku (1)
    - Example: requested=opus, cap=sonnet → returns sonnet
    
    Args:
        model_override: Optional model shorthand (e.g., "haiku")
        default_model: Default model to use if no override
        max_model: Optional cap (e.g., "sonnet")
        verbose: If True, log downgrade events to stderr
    
    Returns:
        Tuple of (resolved_model_id, was_downgraded)
    """
    # Step 1: Resolve requested model
    requested = model_override if model_override else default_model
    
    # Step 2: Convert to tier name (opus/sonnet/haiku)
    requested_tier = _extract_tier_from_model(requested)
    
    # Step 3: Apply cap if set
    was_downgraded = False
    final_tier = requested_tier
    
    if max_model and max_model != "none":
        cap_tier = max_model  # Already in tier format
        
        if MODEL_TIER_HIERARCHY.get(requested_tier, 0) > MODEL_TIER_HIERARCHY.get(cap_tier, 0):
            final_tier = cap_tier
            was_downgraded = True
            
            if verbose:
                import sys
                print(
                    f"[Model Cap] Downgraded {requested_tier} → {final_tier} "
                    f"(max_model={cap_tier} in constitution.md)",
                    file=sys.stderr
                )
    
    # Step 4: Lookup final model ID
    return MODEL_MAP.get(final_tier, default_model), was_downgraded


def _extract_tier_from_model(model: str) -> str:
    """
    Extract tier name (opus/sonnet/haiku) from model string.
    
    Handles both shorthand ("opus") and full IDs ("claude-opus-4-5-20251101").
    
    Args:
        model: Model string
    
    Returns:
        Tier name (defaults to "sonnet" if unknown)
    """
    model_lower = model.lower()
    
    if "opus" in model_lower:
        return "opus"
    elif "sonnet" in model_lower:
        return "sonnet"
    elif "haiku" in model_lower:
        return "haiku"
    else:
        # Default to sonnet for unknown models
        return "sonnet"
```

**Key Changes**:
1. Added `max_model` and `verbose` parameters
2. Returns tuple `(model_id, was_downgraded)` instead of just string
3. Implements tier hierarchy comparison
4. Logs downgrade events when verbose=True

---

#### 2.3 Update `parse_subagents_from_template()`

**File**: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/src/specify_cli/template_parser.py`

**Modify function at lines 232-302**:

```python
def parse_subagents_from_template(
    template_path: Path,
    feature: str,
    context: Optional[Dict[str, Any]] = None,
    filter_parallel: bool = True,
    project_root: Optional[Path] = None,
    verbose: bool = False,
) -> List[AgentTask]:
    """
    Extract subagent definitions from template YAML frontmatter.
    
    ... (existing docstring)
    
    New Args:
        project_root: Project root for loading constitution.md
        verbose: Enable verbose logging for model cap events
    """
    config = parse_template_config(template_path)
    
    # Load constitution settings
    constitution = load_constitution_settings(project_root)
    max_model = constitution.get("max_model", "none")
    
    tasks: List[AgentTask] = []
    downgrade_count = 0

    for agent_def in config.subagents:
        # Skip non-parallel agents if filtering
        if filter_parallel and not agent_def.get("parallel", True):
            continue

        # Resolve model WITH cap enforcement
        model, was_downgraded = resolve_model(
            agent_def.get("model_override"),
            config.default_model,
            max_model=max_model,
            verbose=verbose,
        )
        
        if was_downgraded:
            downgrade_count += 1

        # Build prompt with context
        base_prompt = agent_def.get("prompt", f"Execute {agent_def.get('role', 'unknown')}")
        prompt = build_prompt_with_context(base_prompt, feature, context)

        # Extract dependencies
        depends_on = agent_def.get("depends_on", [])
        if depends_on is None:
            depends_on = []

        task = AgentTask(
            name=agent_def.get("role", f"agent-{len(tasks)}"),
            prompt=prompt,
            model=model,
            depends_on=depends_on,
            priority=agent_def.get("priority", 5),
            role_group=agent_def.get("role_group", "DEFAULT"),
            metadata={
                "trigger": agent_def.get("trigger"),
                "template": str(template_path),
                "feature": feature,
                "was_downgraded": was_downgraded,
            }
        )

        tasks.append(task)
    
    # Summary logging
    if verbose and downgrade_count > 0:
        import sys
        print(
            f"[Model Cap Summary] {downgrade_count}/{len(tasks)} agents downgraded "
            f"(max_model={max_model})",
            file=sys.stderr
        )

    return tasks
```

**Key Changes**:
1. Added `project_root` and `verbose` parameters
2. Load constitution settings before processing agents
3. Pass `max_model` to `resolve_model()`
4. Track downgrade statistics in task metadata
5. Print summary when downgrades occur

---

#### 2.4 Update `parse_template_config()`

**File**: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/src/specify_cli/template_parser.py`

**Modify function at lines 116-178**:

```python
def parse_template_config(
    template_path: Path,
    project_root: Optional[Path] = None,
    max_model: Optional[str] = None,
) -> TemplateConfig:
    """
    Parse a template file and extract configuration.
    
    ... (existing docstring)
    
    New Args:
        project_root: Project root for loading constitution.md
        max_model: Optional model cap override (CLI takes precedence)
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    content = template_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(content)

    if frontmatter is None:
        raise ValueError(f"No valid YAML frontmatter in: {template_path}")

    # Extract claude_code configuration
    claude_code = frontmatter.get("claude_code", {})

    # Load constitution settings if not overridden
    if max_model is None and project_root:
        constitution = load_constitution_settings(project_root)
        max_model = constitution.get("max_model", "none")

    # Default model with cap enforcement
    template_model = claude_code.get("model", "sonnet")
    resolved_model, _ = resolve_model(
        model_override=None,
        default_model=MODEL_MAP.get(template_model, ModelTier.SONNET.value),
        max_model=max_model,
        verbose=False,  # Silent at this stage
    )
    default_model = resolved_model

    # ... (rest of function unchanged)
```

**Why modify this?**  
Ensures model cap is applied when loading template config, not just when creating tasks.

---

### 3. CLI Integration

**File**: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/src/specify_cli/__init__.py`

#### 3.1 Add Global `--model-cap` Flag

**Insert after line 2600** (near `@app.command("orchestrate")` definition):

```python
@app.command("orchestrate")
def orchestrate(
    template: str = typer.Argument(..., help="Command template name (e.g., 'specify', 'implement')"),
    feature: str = typer.Argument(..., help="Feature identifier"),
    pool_size: int = typer.Option(4, "--pool-size", "-p", help="Number of parallel agents"),
    sequential: bool = typer.Option(False, "--sequential", help="Disable wave overlap (run sequentially)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show execution plan without running"),
    model_cap: Optional[str] = typer.Option(None, "--model-cap", help="Override max_model from constitution (opus/sonnet/haiku)"),
    verbose_cap: bool = typer.Option(False, "--verbose-cap", help="Log model downgrade events"),
):
    """
    Execute a command template with parallel agent orchestration.
    
    ... (existing docstring)
    """
```

#### 3.2 Pass Parameters to Parser

**Modify around line 2664**:

```python
    # Parse template
    try:
        project_root = Path.cwd()  # Detect project root
        tasks = parse_subagents_from_template(
            template_path,
            feature,
            project_root=project_root,
            verbose=verbose_cap,
        )
        
        # Load constitution for config parsing
        constitution = load_constitution_settings(project_root)
        effective_cap = model_cap if model_cap else constitution.get("max_model", "none")
        
        wave_config = get_wave_config_from_template(template_path)
        
        # Show cap info if active
        if effective_cap and effective_cap != "none":
            source = "CLI flag" if model_cap else "constitution.md"
            console.print(f"[yellow]Model Cap Active:[/yellow] {effective_cap} (from {source})")
            console.print()
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to parse template: {e}")
        raise typer.Exit(1)
```

---

### 4. Downgrade Logic Specification

#### Model Tier Hierarchy

```python
MODEL_TIER_HIERARCHY = {
    "opus": 3,      # Highest tier
    "sonnet": 2,    # Mid tier
    "haiku": 1,     # Lowest tier
}
```

#### Downgrade Rules Matrix

| Requested Model | Max Model Cap | Final Model | Downgraded? |
|-----------------|---------------|-------------|-------------|
| opus | none | opus | No |
| opus | opus | opus | No |
| opus | sonnet | sonnet | Yes |
| opus | haiku | haiku | Yes |
| sonnet | opus | sonnet | No |
| sonnet | sonnet | sonnet | No |
| sonnet | haiku | haiku | Yes |
| haiku | opus | haiku | No |
| haiku | sonnet | haiku | No |
| haiku | haiku | haiku | No |

#### Special Cases

1. **Subagent Override**: If subagent has `model_override: haiku`, it's NOT downgraded (already below cap)
2. **Missing Constitution**: If `memory/constitution.md` doesn't exist → no cap (opus works)
3. **Invalid Cap Value**: If `max_model: invalid` → ignore, treat as "none"
4. **CLI Override**: `--model-cap sonnet` takes precedence over constitution.md

---

### 5. Edge Cases & Error Handling

| Scenario | Behavior | Rationale |
|----------|----------|-----------|
| **Constitution not found** | No cap applied (silent) | Don't break new/incomplete projects |
| **Invalid max_model value** | Ignore, log warning | Fail-safe: better to allow opus than block |
| **Template has no model** | Apply cap to default (sonnet) | Consistent behavior |
| **Subagent already < cap** | No downgrade | Don't upgrade lower models |
| **Constitution parse error** | No cap applied (silent) | Don't block CLI on malformed config |
| **CLI `--model-cap` conflict** | CLI wins | User intent takes precedence |
| **Multiple constitutions** | Use closest to CWD | Standard file resolution |

#### Error Handling Strategy

```python
def load_constitution_settings(project_root: Optional[Path] = None) -> Dict[str, Any]:
    """Always returns dict, never raises exceptions."""
    try:
        # ... parsing logic
        return settings
    except FileNotFoundError:
        return {}  # No constitution = no cap
    except Exception as e:
        # Log to stderr if verbose, but don't block
        import sys
        print(f"[Warning] Failed to parse constitution.md: {e}", file=sys.stderr)
        return {}
```

---

### 6. User Experience

#### Silent Mode (Default)

```bash
$ specify orchestrate specify feature-123
# No output about model cap unless downgrade occurs
```

#### Verbose Mode

```bash
$ specify orchestrate specify feature-123 --verbose-cap

Model Cap Active: sonnet (from constitution.md)

[Model Cap] Downgraded opus → sonnet (max_model=sonnet in constitution.md)
[Model Cap] Downgraded opus → sonnet (max_model=sonnet in constitution.md)
[Model Cap Summary] 2/5 agents downgraded (max_model=sonnet)

Execution Plan (5 agents)
...
```

#### CLI Override

```bash
$ specify orchestrate specify feature-123 --model-cap haiku --verbose-cap

Model Cap Active: haiku (from CLI flag)

[Model Cap] Downgraded opus → haiku (max_model=haiku in constitution.md)
[Model Cap] Downgraded sonnet → haiku (max_model=haiku in constitution.md)
[Model Cap Summary] 4/5 agents downgraded (max_model=haiku)
```

---

### 7. Testing Strategy

#### Unit Tests

**New file**: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/tests/test_model_cap.py`

```python
import pytest
from pathlib import Path
from specify_cli.template_parser import (
    parse_constitution_settings,
    resolve_model,
    MODEL_TIER_HIERARCHY,
)


def test_parse_constitution_settings_valid():
    """Test parsing valid constitution with max_model."""
    content = """
## Project Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **language** | `en` | ... |
| **max_model** | `sonnet` | ... |
"""
    settings = parse_constitution_settings(content)
    assert settings["max_model"] == "sonnet"
    assert settings["language"] == "en"


def test_parse_constitution_settings_missing():
    """Test parsing constitution without max_model."""
    content = """
## Project Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **language** | `ru` | ... |
"""
    settings = parse_constitution_settings(content)
    assert settings.get("max_model") is None
    assert settings["language"] == "ru"


def test_resolve_model_no_cap():
    """Test model resolution without cap."""
    model, downgraded = resolve_model(
        model_override=None,
        default_model="claude-opus-4-5-20251101",
        max_model=None,
    )
    assert "opus" in model
    assert not downgraded


def test_resolve_model_with_cap_opus_to_sonnet():
    """Test opus → sonnet downgrade."""
    model, downgraded = resolve_model(
        model_override=None,
        default_model="claude-opus-4-5-20251101",
        max_model="sonnet",
    )
    assert "sonnet" in model
    assert downgraded


def test_resolve_model_with_cap_already_below():
    """Test no downgrade when already below cap."""
    model, downgraded = resolve_model(
        model_override="haiku",
        default_model="claude-sonnet-4-5-20250929",
        max_model="sonnet",
    )
    assert "haiku" in model
    assert not downgraded


def test_resolve_model_cap_hierarchy():
    """Test tier hierarchy enforcement."""
    # opus > sonnet
    assert MODEL_TIER_HIERARCHY["opus"] > MODEL_TIER_HIERARCHY["sonnet"]
    
    # sonnet > haiku
    assert MODEL_TIER_HIERARCHY["sonnet"] > MODEL_TIER_HIERARCHY["haiku"]


def test_resolve_model_invalid_cap():
    """Test handling of invalid cap value."""
    model, downgraded = resolve_model(
        model_override=None,
        default_model="claude-opus-4-5-20251101",
        max_model="invalid_tier",
    )
    # Should not downgrade (invalid cap = no cap)
    assert "opus" in model
    assert not downgraded
```

#### Integration Tests

```python
def test_parse_subagents_with_cap(tmp_path):
    """Test full subagent parsing with model cap."""
    # Create mock constitution
    constitution = tmp_path / "memory" / "constitution.md"
    constitution.parent.mkdir(parents=True)
    constitution.write_text("""
## Project Settings

| **max_model** | `sonnet` |
""")
    
    # Create mock template
    template = tmp_path / "templates" / "commands" / "test.md"
    template.parent.mkdir(parents=True)
    template.write_text("""
---
claude_code:
  model: opus
  subagents:
    - role: analyzer
      parallel: true
---
Test template
""")
    
    # Parse with cap
    tasks = parse_subagents_from_template(
        template,
        "test-feature",
        project_root=tmp_path,
    )
    
    # Verify downgrade
    assert len(tasks) == 1
    assert "sonnet" in tasks[0].model
    assert tasks[0].metadata["was_downgraded"] is True
```

#### Manual Testing Checklist

- [ ] Constitution with `max_model: sonnet` → opus commands use sonnet
- [ ] Constitution with `max_model: haiku` → opus+sonnet commands use haiku
- [ ] Constitution with `max_model: none` → opus commands use opus
- [ ] Missing constitution → opus commands use opus
- [ ] CLI `--model-cap haiku` overrides constitution
- [ ] Verbose mode shows downgrade logs
- [ ] Silent mode shows no logs
- [ ] Subagent with `model_override: haiku` not affected by cap
- [ ] Malformed constitution doesn't break CLI
- [ ] Cost tracking reflects downgraded model

---

### 8. Backward Compatibility

#### Guarantee

> **Zero Breaking Changes**: All existing projects without `max_model` setting continue to work identically.

#### Compatibility Matrix

| Project State | Constitution | Behavior |
|---------------|--------------|----------|
| **Legacy** | No constitution.md | Opus works normally (no change) |
| **Legacy** | constitution.md without max_model | Opus works normally (no change) |
| **New** | constitution.md with `max_model: none` | Opus works normally (explicit) |
| **Capped** | constitution.md with `max_model: sonnet` | Opus → Sonnet (opt-in) |

#### Migration Path

Users can adopt gradually:

1. **Phase 1**: Continue using opus (no changes)
2. **Phase 2**: Add `max_model: sonnet` to constitution.md
3. **Phase 3**: Test with `--verbose-cap` flag
4. **Phase 4**: Remove flag, run with silent cap

---

### 9. Quality Gates Impact

#### SQS (Specification Quality Score)

**No Impact**: Model cap doesn't affect spec quality validation logic.

#### CQS (Concept Quality Score)

**Potential Impact**: If concept generation uses opus by default, capping to sonnet may reduce quality slightly.

**Mitigation**:
- Make CQS threshold configurable per model tier
- Document recommended caps: `max_model: sonnet` (safe), `max_model: haiku` (not recommended for concept)

---

### 10. Future Enhancements (Out of Scope)

These are NOT included in initial implementation:

1. **Per-command caps**: Different caps for different commands
   ```yaml
   max_model:
     default: sonnet
     concept: opus  # Allow opus for concept only
   ```

2. **Budget tracking**: Track cumulative cost and stop when limit reached
   ```yaml
   budget:
     max_cost_usd: 10.00
     reset: daily
   ```

3. **Dynamic caps**: Adjust cap based on time of day / urgency
   ```yaml
   max_model:
     business_hours: haiku
     after_hours: opus
   ```

4. **Cap notifications**: Slack/email when cap prevents opus usage

---

## Implementation Checklist

### Phase 1: Schema & Parsing (Week 1)

- [ ] Update constitution.md template with max_model setting
- [ ] Implement `parse_constitution_settings()` function
- [ ] Implement `load_constitution_settings()` function
- [ ] Add unit tests for parsing logic
- [ ] Document schema in constitution.md comments

### Phase 2: Model Resolution (Week 1)

- [ ] Add `MODEL_TIER_HIERARCHY` constant
- [ ] Implement `_extract_tier_from_model()` helper
- [ ] Update `resolve_model()` with cap logic
- [ ] Add unit tests for downgrade logic
- [ ] Test edge cases (invalid caps, missing files)

### Phase 3: Integration (Week 2)

- [ ] Update `parse_subagents_from_template()` signature
- [ ] Update `parse_template_config()` signature
- [ ] Add `--model-cap` and `--verbose-cap` CLI flags
- [ ] Pass parameters through call chain
- [ ] Add integration tests

### Phase 4: User Experience (Week 2)

- [ ] Implement verbose logging
- [ ] Add downgrade summary output
- [ ] Update CLI help text
- [ ] Test silent mode (default)
- [ ] Test verbose mode

### Phase 5: Documentation (Week 3)

- [ ] Update README.md with model cap feature
- [ ] Add CHANGELOG.md entry
- [ ] Update docs/COMMANDS_GUIDE.md
- [ ] Add migration guide for existing users
- [ ] Document quality gate impacts

### Phase 6: Testing & Validation (Week 3)

- [ ] Run full test suite
- [ ] Manual testing with real projects
- [ ] Performance testing (cap overhead < 5ms)
- [ ] Cost validation (downgraded models used)
- [ ] Backward compatibility testing

---

## Critical Files for Implementation

1. **`/Users/dmitry.lazarenko/Documents/projects/spec-kit/src/specify_cli/template_parser.py`**  
   - Core logic: Constitution loading, model resolution, downgrade rules
   - Lines to modify: 59 (add constants), 181-198 (resolve_model), 232-302 (parse_subagents)

2. **`/Users/dmitry.lazarenko/Documents/projects/spec-kit/memory/constitution.md`**  
   - Schema definition: Add max_model to Project Settings table
   - Lines to modify: 38-46 (add new row)

3. **`/Users/dmitry.lazarenko/Documents/projects/spec-kit/src/specify_cli/__init__.py`**  
   - CLI integration: Add flags, pass parameters to parser
   - Lines to modify: ~2600 (add CLI flags), ~2664 (pass to parser)

4. **`/Users/dmitry.lazarenko/Documents/projects/spec-kit/src/specify_cli/agent_pool.py`**  
   - Cost tracking: Ensure downgraded model costs are tracked correctly
   - Lines to check: 59-73 (model_id_to_tier, calculate_cost)

5. **`/Users/dmitry.lazarenko/Documents/projects/spec-kit/tests/test_model_cap.py`** (NEW)  
   - Test coverage: Unit + integration tests for model cap feature
   - To create: Full test suite as documented above

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Constitution parse errors break CLI** | HIGH | LOW | Fail-safe: return empty dict on any error |
| **Model cap bypassed in some paths** | MEDIUM | MEDIUM | Audit all model resolution call sites |
| **Users unaware of downgrade** | LOW | HIGH | Add verbose mode, document in CLI help |
| **Quality degradation with sonnet cap** | MEDIUM | MEDIUM | Document recommended caps per command |
| **Performance overhead** | LOW | LOW | Cache constitution parsing (LRU) |

---

## Success Metrics

1. **Backward Compatibility**: 100% of existing projects work without changes
2. **Performance**: Constitution loading overhead < 5ms (cached)
3. **Adoption**: Feature documented, easy to enable/disable
4. **Cost Savings**: Measurable reduction in API costs when cap is enabled
5. **User Satisfaction**: No complaints about breaking changes

---

## Flowchart: Model Resolution with Cap

```
┌─────────────────────────────────────────────────────────────┐
│                      START                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Load command template (e.g., concept.md)                   │
│  Extract: model=opus (from YAML frontmatter)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Check CLI flag: --model-cap?                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ┌────┴────┐
                    │         │
                  Yes        No
                    │         │
                    ▼         ▼
      ┌──────────────────┐   ┌──────────────────────┐
      │ Use CLI cap      │   │ Load constitution.md │
      │ max_model=CLI    │   │ Parse max_model      │
      └────────┬─────────┘   └──────────┬───────────┘
               │                         │
               │                         ▼
               │             ┌──────────────────────┐
               │             │ max_model found?     │
               │             └─────┬────────┬───────┘
               │                   │        │
               │                  Yes      No
               │                   │        │
               │                   ▼        ▼
               │         ┌──────────────┐  ┌────────────┐
               │         │ Use it       │  │ Use "none" │
               │         └──────┬───────┘  └──────┬─────┘
               │                │                  │
               └────────────────┴──────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│  Resolve model tier:                                        │
│  requested_tier = extract_tier("opus") → "opus"             │
│  cap_tier = max_model → "sonnet"                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Compare tiers:                                             │
│  TIER_HIERARCHY["opus"] (3) > TIER_HIERARCHY["sonnet"] (2)? │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ┌────┴────┐
                    │         │
                  Yes        No
                    │         │
                    ▼         ▼
      ┌──────────────────┐   ┌──────────────────┐
      │ DOWNGRADE        │   │ Keep requested   │
      │ final="sonnet"   │   │ final="opus"     │
      │ downgraded=True  │   │ downgraded=False │
      └────────┬─────────┘   └──────────┬───────┘
               │                         │
               │                         ▼
               │             ┌──────────────────────┐
               │             │ verbose mode?        │
               │             └─────┬────────┬───────┘
               │                   │        │
               └───────────────────┤       Yes
                                  No        │
                                   │        ▼
                                   │  ┌──────────────────┐
                                   │  │ Log to stderr:   │
                                   │  │ "Downgraded      │
                                   │  │  opus → sonnet"  │
                                   │  └────────┬─────────┘
                                   │           │
                                   └───────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Lookup MODEL_MAP:                                          │
│  final_tier="sonnet" → "claude-sonnet-4-5-20250929"         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Return: (model_id, was_downgraded)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Create AgentTask with resolved model                       │
│  metadata["was_downgraded"] = True                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      END                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Code Diff Summary

### Files Changed: 3
### Files Created: 1 (test file)
### Lines Added: ~250
### Lines Modified: ~50

**Estimated Implementation Time**: 2-3 weeks (including testing)

---

**Plan Status**: ✅ Complete and ready for implementation

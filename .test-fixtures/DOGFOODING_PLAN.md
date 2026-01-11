# Dogfooding Plan: Drift Detection on Spec Kit

**Version**: 0.4.0
**Purpose**: Test drift detection and reverse-engineering features on the Spec Kit project itself

---

## Rationale

Testing the drift detection system on Spec Kit itself ("eating our own dog food") provides:
1. **Real-world validation**: Complex codebase with mixed Python/Markdown/Bash
2. **Meta-testing**: Can we extract specs from our own templates?
3. **Quality assurance**: Detect any drift in our own implementation
4. **User experience**: Experience the feature as end-users would

---

## Test Scenario 1: Drift Detection on Command Templates

### Objective
Verify that command templates align with their documentation in COMMANDS_GUIDE.md

### Setup
```bash
cd /Users/dmitry.lazarenko/Documents/projects/spec-kit
```

### Test Case 1A: Analyze Command Template vs Documentation

**Hypothesis**: The `/speckit.analyze` template might have drift from COMMANDS_GUIDE.md documentation

**Steps**:
1. Run drift detection treating COMMANDS_GUIDE.md as "spec":
   ```bash
   /speckit.analyze --profile drift --scope "templates/commands/*.md" --spec-source "docs/COMMANDS_GUIDE.md"
   ```

**Expected Findings**:
- Check if all documented flags in COMMANDS_GUIDE.md exist in command templates
- Check if all command frontmatter handoffs match documentation
- Identify any undocumented commands or flags

**Success Criteria**:
- [ ] All commands documented
- [ ] All flags documented
- [ ] Handoff chains accurate
- [ ] No critical drift

---

### Test Case 1B: Quality Gates vs Implementation

**Hypothesis**: Quality gate definitions (quality-gates.md) might have drift from actual gate usage in commands

**Steps**:
1. Extract all gate IDs from `memory/domains/quality-gates.md`
2. Search for gate references in `templates/commands/*.md`
3. Identify:
   - Gates defined but never used (dead gates)
   - Gates used but not defined (missing definitions)

**Expected Findings**:
```markdown
## Drift Report

### DRIFT-001: Unused Quality Gate (LOW)
**Gate**: QG-XYZ-001 defined in quality-gates.md but never referenced

### DRIFT-002: Undocumented Quality Gate (HIGH)
**Gate**: QG-ABC-002 used in implement.md but not defined in quality-gates.md
```

**Success Criteria**:
- [ ] All used gates have definitions
- [ ] Dead gates identified (for potential removal)
- [ ] Gate thresholds consistent across usages

---

## Test Scenario 2: Reverse-Engineering CLI Commands

### Objective
Extract implicit "requirements" from the CLI implementation itself

### Test Case 2A: Extract Requirements from CLI Code

**Steps**:
1. Run reverse-engineering on Python CLI:
   ```bash
   cd /Users/dmitry.lazarenko/Documents/projects/spec-kit
   /speckit.reverse-engineer --scope "src/specify_cli/__init__.py" --language python
   ```

**Expected Output**:
```markdown
# Extracted Specification

### FR-001: Project Initialization
**Description**: Initialize a new project with SDD templates
**Confidence**: 0.85 (HIGH - inferred from `init()` function)

**Evidence**:
- Function: `init()` in src/specify_cli/__init__.py:150-300
- CLI command: `specify init <project_name>`
- Flags: --ai, --template, --ignore-agent-tools

**Input**: project_name: str, ai: str, template: str
**Output**: Initialized project directory

---

### FR-002: Agent Context Injection
**Description**: Inject context about agent tools into project
**Confidence**: 0.75 (HIGH - inferred from agent configuration)

**Evidence**:
- AGENT_CONFIG dict (line 50-120)
- Script generation logic (line 400-500)

---

### FR-NEW-1: GitHub Package Download
**Description**: Download pre-packaged release assets from GitHub
**Confidence**: 0.80 (HIGH)

**Evidence**:
- Function: download logic scattered across init()
- External API call patterns detected
```

**Success Criteria**:
- [ ] Extracted 5-10 implicit requirements
- [ ] Average confidence >= 0.70
- [ ] Identified core CLI capabilities
- [ ] No hallucinations (manual review)

---

### Test Case 2B: Template Structure Reverse-Engineering

**Hypothesis**: Can we infer the "schema" of command templates from multiple examples?

**Steps**:
1. Analyze all command templates:
   ```bash
   /speckit.reverse-engineer --scope "templates/commands/*.md" --min-confidence 0.60
   ```

2. Look for common patterns:
   - YAML frontmatter structure
   - Persona patterns
   - Handoff patterns
   - Gate patterns

**Expected Findings**:
```markdown
### PATTERN-001: Command Template Structure
**Confidence**: 0.90 (EXPLICIT - consistent across 30 files)

**Schema Extracted**:
- description: string (always present)
- persona: string (optional)
- model: "sonnet" | "haiku" | "opus"
- handoffs: array of {label, agent, prompt, auto, gates}
- pre_gates: array of {name, check}
- gates: array of {name, check}
```

**Success Criteria**:
- [ ] Schema extraction accurate
- [ ] Inconsistencies flagged
- [ ] Template quality patterns identified

---

## Test Scenario 3: Script Consistency Analysis

### Objective
Verify bash and PowerShell scripts have feature parity

### Test Case 3A: Cross-Platform Drift Detection

**Hypothesis**: Bash and PowerShell versions of scripts might have drifted

**Steps**:
1. Compare bash vs PowerShell implementations:
   ```bash
   # Create temporary "spec" from bash script behavior
   /speckit.reverse-engineer --scope "scripts/bash/*.sh" --output-dir temp-bash-spec

   # Check if PowerShell implements same features
   /speckit.analyze --profile drift --scope "scripts/powershell/*.ps1" --spec-source "temp-bash-spec/extracted-spec.md"
   ```

**Expected Findings**:
- Identify flags present in bash but missing in PowerShell
- Identify validation logic differences
- Identify error handling inconsistencies

**Success Criteria**:
- [ ] Feature parity >= 95%
- [ ] No critical behavioral drift
- [ ] Error messages consistent

---

## Test Scenario 4: Documentation Drift

### Objective
Verify documentation matches implementation

### Test Case 4A: CHANGELOG.md Completeness

**Hypothesis**: Recent changes might not be documented in CHANGELOG

**Steps**:
1. Extract all features from git commits since last release:
   ```bash
   git log v0.3.0..HEAD --oneline
   ```

2. Compare with CHANGELOG.md entries
3. Flag missing changelog entries

**Expected Findings**:
```markdown
### DRIFT-001: Undocumented Feature (MEDIUM)
**Commit**: d210b51 "fix: remove GitHub Pages auto-enablement from workflow"
**Status**: ✅ Documented in CHANGELOG

### DRIFT-002: Undocumented Feature (HIGH)
**Commit**: abc1234 "feat: add new quality gate"
**Status**: ❌ NOT in CHANGELOG
```

**Success Criteria**:
- [ ] All features documented
- [ ] Version numbers consistent
- [ ] Dates accurate

---

### Test Case 4B: README vs COMMANDS_GUIDE Consistency

**Steps**:
1. Extract command list from README.md
2. Compare with COMMANDS_GUIDE.md table of contents
3. Identify mismatches

**Expected Findings**:
- Commands in README but not in COMMANDS_GUIDE (or vice versa)
- Description mismatches
- Missing documentation

**Success Criteria**:
- [ ] Command lists match
- [ ] Descriptions consistent
- [ ] No orphaned documentation

---

## Test Scenario 5: Agent Configuration Validation

### Objective
Verify AGENT_CONFIG consistency with documentation and scripts

### Test Case 5A: Agent Support Matrix

**Steps**:
1. Extract agent list from AGENT_CONFIG in `__init__.py`
2. Compare with:
   - README.md "Supported Agents" table
   - bash scripts (get-agent-context.sh)
   - PowerShell scripts (Get-AgentContext.ps1)

**Expected Findings**:
```markdown
## Agent Support Consistency

| Agent | AGENT_CONFIG | README | Bash | PowerShell | Status |
|-------|--------------|--------|------|------------|--------|
| claude | ✅ | ✅ | ✅ | ✅ | ✅ Aligned |
| cursor-agent | ✅ | ✅ | ✅ | ✅ | ✅ Aligned |
| copilot | ✅ | ✅ | ✅ | ✅ | ✅ Aligned |
| cline | ✅ | ✅ | ✅ | ❌ | ⚠️ Drift |
```

**Success Criteria**:
- [ ] All agents documented everywhere
- [ ] Tool names consistent
- [ ] No orphaned agents

---

## Test Scenario 6: Metadata Consistency

### Objective
Verify version numbers and dates are consistent across project

### Test Case 6A: Version Audit

**Files to Check**:
- `pyproject.toml` → `project.version`
- `CHANGELOG.md` → top entry `## [X.Y.Z]`
- `COMMANDS_GUIDE.md` → footer version
- `__init__.py` → `__version__` (if exists)

**Expected Result**:
All should show `0.4.0`

**Validation**:
```bash
# Extract versions
grep "version = " pyproject.toml
grep "## \[" CHANGELOG.md | head -1
grep "Версия:" docs/COMMANDS_GUIDE.md
```

**Success Criteria**:
- [ ] All versions match
- [ ] No stale version references

---

### Test Case 6B: Date Consistency

**Check**:
- CHANGELOG.md top entry date
- Git commit date for latest changes
- Documentation "Last updated" dates

**Expected**: Dates within 1 day of each other

**Success Criteria**:
- [ ] Dates consistent
- [ ] No stale timestamps

---

## Test Scenario 7: Template Completeness

### Objective
Verify all templates are included in release packages

### Test Case 7A: Release Package Audit

**Steps**:
1. Run release package generation:
   ```bash
   ./.github/workflows/scripts/create-release-packages.sh v0.4.0
   ```

2. Check each package for required files:
   - All templates/*.md files
   - All scripts/bash/*.sh files
   - All scripts/powershell/*.ps1 files
   - memory/constitution.md

**Expected**:
```
Checking sdd-claude-package-bash.tar.gz...
✅ All templates present (30/30)
✅ All bash scripts present (15/15)
✅ memory/constitution.md present

Checking sdd-copilot-package-ps.tar.gz...
✅ All templates present (15/15)
✅ All PowerShell scripts present (15/15)
❌ Missing: memory/constitution.md
```

**Success Criteria**:
- [ ] No missing files in any package
- [ ] Agent-specific filtering works correctly
- [ ] Package sizes reasonable

---

## Test Scenario 8: Cross-Reference Validation

### Objective
Verify internal cross-references are valid

### Test Case 8A: Handoff Chain Validation

**Steps**:
1. Extract all handoffs from command templates
2. Verify target commands exist
3. Build handoff graph

**Expected Findings**:
```markdown
## Handoff Graph

/speckit.constitution
  ↓ (auto=false)
/speckit.concept
  ↓ (auto=false)
/speckit.validate-concept
  ↓ (auto=false)
/speckit.specify
  ↓ (auto=true)
/speckit.plan
  ↓ (auto=true)
/speckit.tasks
  ...

## Broken Handoffs

### DRIFT-001: Broken Handoff (CRITICAL)
**From**: /speckit.implement
**To**: /speckit.nonexistent
**Line**: templates/commands/implement.md:250
```

**Success Criteria**:
- [ ] All handoff targets exist
- [ ] No circular handoffs (unless intentional)
- [ ] Auto-handoff chains make sense

---

## Test Scenario 9: Error Message Quality

### Objective
Verify error messages are helpful and consistent

### Test Case 9A: CLI Error Message Audit

**Steps**:
1. Extract all `raise` statements and error prints from `__init__.py`
2. Check for:
   - Clear error messages
   - Actionable guidance
   - Consistent formatting

**Expected Findings**:
```python
# Good
raise ValueError("Project name cannot be empty. Provide a valid project name.")

# Bad (if found)
raise ValueError("Invalid input")  # Too vague
```

**Success Criteria**:
- [ ] All errors have clear messages
- [ ] All errors suggest fixes
- [ ] No generic error messages

---

## Summary: Dogfooding Metrics

### Expected Results

| Scenario | Expected Drift Items | Severity | Action |
|----------|---------------------|----------|--------|
| Command vs Docs | 0-2 | LOW-MEDIUM | Update docs |
| Quality Gates | 0-3 | LOW-MEDIUM | Clean up unused |
| Agent Config | 0-1 | MEDIUM-HIGH | Fix inconsistency |
| Script Parity | 0-5 | MEDIUM | Sync features |
| Documentation | 0-3 | LOW-MEDIUM | Update docs |
| Versions | 0 | CRITICAL | Must be consistent |
| Templates | 0 | CRITICAL | Must be complete |
| Handoffs | 0-1 | HIGH | Fix broken links |
| Error Messages | 0-5 | LOW | Improve clarity |

### Overall Success Criteria

- [ ] **Zero CRITICAL drift items**
- [ ] **< 5 HIGH drift items**
- [ ] **< 10 MEDIUM drift items**
- [ ] **Average confidence on extractions >= 0.75**
- [ ] **No crashes during execution**
- [ ] **All tests complete in < 10 minutes total**

---

## Post-Dogfooding Actions

1. **Document findings** in `DOGFOODING_RESULTS.md`
2. **Fix critical drift** immediately
3. **Prioritize high drift** for pre-release fixes
4. **Log medium/low drift** for future iterations
5. **Update validation checklist** based on learnings
6. **Calibrate confidence scoring** if needed
7. **Improve error messages** based on UX

---

## Notes

- This dogfooding plan is intentionally comprehensive - not all tests need to be run for every release
- Focus on critical scenarios (versions, templates, handoffs) for v0.4.0 release
- Use medium/low priority scenarios for continuous improvement
- Document any unexpected findings for future investigation

---

**Prepared by**: Claude Sonnet 4.5
**Date**: 2026-01-11
**Version**: 0.4.0

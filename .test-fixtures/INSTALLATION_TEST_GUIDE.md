# Installation Testing Guide - v0.4.0

**Purpose**: Verify that v0.4.0 release packages install correctly and drift detection features work as expected

---

## Pre-Testing Checklist

- [ ] Release packages generated in `.genreleases/` directory
- [ ] 68 package files present (34 agents × 2 script types)
- [ ] Package naming: `spec-kit-template-{agent}-{sh|ps}-v0.4.0.zip`
- [ ] File sizes reasonable (750-850 KB range)

---

## Test Environment Setup

### Option 1: Local Directory Test (Recommended)

```bash
# Create test directory
mkdir -p /tmp/spec-kit-test-v0.4.0
cd /tmp/spec-kit-test-v0.4.0

# Copy a test package (claude-sh for this example)
cp /Users/dmitry.lazarenko/Documents/projects/spec-kit/.genreleases/spec-kit-template-claude-sh-v0.4.0.zip .

# Extract package
unzip spec-kit-template-claude-sh-v0.4.0.zip

# Verify contents
ls -la .claude/commands/ | grep reverse
ls -la .specify/scripts/bash/ | grep reverse
ls -la .specify/memory/domains/ | grep quality-gates
```

**Expected Results**:
```
-rw-r--r-- speckit.reverse-engineer.md
-rwxr-xr-x reverse-engineer.sh
-rw-r--r-- quality-gates.md
```

### Option 2: Fresh Git Repository Test

```bash
# Create a new project
mkdir -p ~/test-projects/drift-test-project
cd ~/test-projects/drift-test-project
git init

# Install Spec Kit via Python CLI (if available)
specify init drift-test-project --ai claude --ignore-agent-tools

# Or manually extract package
unzip /path/to/spec-kit-template-claude-sh-v0.4.0.zip
```

---

## Test Case 1: Package Contents Verification

### Step 1: Verify Command Templates

**Expected Files**:
```bash
.claude/commands/speckit.analyze.md         # Should be ~124KB (includes Pass AA)
.claude/commands/speckit.reverse-engineer.md # Should be ~29KB (new command)
```

**Validation**:
```bash
# Check file exists and size
ls -lh .claude/commands/speckit.reverse-engineer.md

# Check for key content markers
grep "4-Wave Extraction Algorithm" .claude/commands/speckit.reverse-engineer.md
grep "Pass AA: Drift Detection" .claude/commands/speckit.analyze.md
```

**Expected Output**:
- Both grep commands return matches
- File sizes match expected ranges

### Step 2: Verify Scripts

**Expected Files**:
```bash
.specify/scripts/bash/reverse-engineer.sh      # Should be ~6.5KB
.specify/scripts/powershell/reverse-engineer.ps1 # Should be ~5KB (if ps package)
```

**Validation**:
```bash
# Check script exists and is executable
ls -la .specify/scripts/bash/reverse-engineer.sh | grep "x"

# Check script content
head -10 .specify/scripts/bash/reverse-engineer.sh

# Expected first line:
#!/usr/bin/env bash
```

### Step 3: Verify Quality Gates

**Expected File**:
```bash
.specify/memory/domains/quality-gates.md  # Should be ~60KB (includes 4 new drift gates)
```

**Validation**:
```bash
# Check for new quality gates
grep "QG-DRIFT-001" .specify/memory/domains/quality-gates.md
grep "QG-DRIFT-002" .specify/memory/domains/quality-gates.md
grep "QG-DRIFT-003" .specify/memory/domains/quality-gates.md
grep "QG-DRIFT-004" .specify/memory/domains/quality-gates.md

# Count total gates
grep -c "^### QG-" .specify/memory/domains/quality-gates.md
# Expected: 48 (44 original + 4 new drift gates)
```

**Expected Output**:
- All 4 drift gates found
- Total gate count is 48

---

## Test Case 2: Functional Testing with Test Fixtures

### Step 1: Copy Test Fixture

```bash
# From Spec Kit repo
cp -r /Users/dmitry.lazarenko/Documents/projects/spec-kit/.test-fixtures/typescript-drift-test ./
cd typescript-drift-test
```

### Step 2: Verify Command Availability

**For Claude Code users**:
```bash
# Check if command is recognized
claude-code --help | grep reverse-engineer

# Or in chat, type:
/speckit.reverse-engineer --help
```

**For other AI agents** (Cursor, Copilot, etc.):
- Check if `/speckit.reverse-engineer` appears in slash command autocomplete
- Verify command description matches documentation

### Step 3: Run Drift Detection

**Execute**:
```bash
# In AI agent chat or via CLI
/speckit.analyze --profile drift
```

**Expected Output**:
- `drift-report.md` file created
- Report contains 3 drift items:
  - DRIFT-001: FR-002 unimplemented (HIGH)
  - DRIFT-002: deleteUser undocumented (HIGH)
  - DRIFT-003: updateUser behavioral drift (MEDIUM)
- Coverage metrics calculated:
  - FR → Code: 66%
  - Code → Spec: 50%

**Validation**:
```bash
# Check report exists
test -f drift-report.md && echo "✅ Report created" || echo "❌ Report missing"

# Check for expected drift items
grep "DRIFT-001" drift-report.md
grep "DRIFT-002" drift-report.md
grep "DRIFT-003" drift-report.md

# Check coverage metrics
grep "66%" drift-report.md  # FR → Code
grep "50%" drift-report.md  # Code → Spec
```

### Step 4: Run Reverse-Engineering

**Execute**:
```bash
# In AI agent chat or via CLI
/speckit.reverse-engineer --scope "src/**/*.ts" --exclude "*.test.ts" --language typescript
```

**Expected Output**:
- `reverse-engineered/` directory created with 4 files:
  - `.extraction-manifest.yaml`
  - `extracted-spec.md`
  - `drift-report.md`
  - `extraction-log.md`
- Extracted 3 requirements:
  - FR-001: User Creation (confidence: 0.95)
  - FR-003: User Update (confidence: 0.80)
  - FR-NEW-1: User Deletion (confidence: 0.70)
- Average confidence >= 0.75

**Validation**:
```bash
# Check directory created
test -d reverse-engineered && echo "✅ Directory created" || echo "❌ Directory missing"

# Check manifest
test -f reverse-engineered/.extraction-manifest.yaml && echo "✅ Manifest exists"

# Check extracted spec
grep "FR-001" reverse-engineered/extracted-spec.md
grep "FR-003" reverse-engineered/extracted-spec.md
grep "FR-NEW-1" reverse-engineered/extracted-spec.md

# Validate manifest structure
grep "extracted_at:" reverse-engineered/.extraction-manifest.yaml
grep "confidence_stats:" reverse-engineered/.extraction-manifest.yaml
```

---

## Test Case 3: Python Fixture Testing

### Step 1: Copy Python Fixture

```bash
cd /tmp/spec-kit-test-v0.4.0
cp -r /Users/dmitry.lazarenko/Documents/projects/spec-kit/.test-fixtures/python-drift-test ./
cd python-drift-test
```

### Step 2: Run Drift Detection

**Execute**:
```bash
/speckit.analyze --profile drift --language python
```

**Expected Output**:
- 4 drift items detected:
  - DRIFT-001: FR-002 unimplemented (HIGH)
  - DRIFT-002: inventory endpoint undocumented (HIGH)
  - DRIFT-003: bulk-import undocumented (HIGH)
  - DRIFT-004: update_product behavioral drift (MEDIUM)
- Coverage: FR → Code: 75%, Code → Spec: 60%

### Step 3: Run Reverse-Engineering

**Execute**:
```bash
/speckit.reverse-engineer --scope "src/**/*.py" --exclude "tests/*" --language python
```

**Expected Output**:
- 5 requirements extracted (FR-001, FR-003, FR-004, FR-NEW-1, FR-NEW-2)
- Average confidence >= 0.75
- FastAPI decorators recognized

---

## Test Case 4: Cross-Platform Testing (PowerShell)

**For Windows or PowerShell users**:

### Step 1: Extract PowerShell Package

```powershell
# Windows PowerShell
Expand-Archive spec-kit-template-claude-ps-v0.4.0.zip -DestinationPath .
```

### Step 2: Verify PowerShell Script

```powershell
# Check script exists
Test-Path .specify/scripts/powershell/reverse-engineer.ps1

# Check script is valid PowerShell
Get-Command .specify/scripts/powershell/reverse-engineer.ps1

# Try running with -Help flag
.specify/scripts/powershell/reverse-engineer.ps1 -Help
```

**Expected Output**:
- Script found
- Help text displays usage information
- No syntax errors

---

## Test Case 5: Quality Gate Integration

### Step 1: Verify Gate Definitions

**Execute**:
```bash
cd typescript-drift-test

# Check if gates are documented
grep -A 10 "QG-DRIFT-001" ../.specify/memory/domains/quality-gates.md
```

**Expected Output**:
- Gate definition includes:
  - Level: MUST or SHOULD
  - Threshold: Clear numeric value
  - Validation command
  - Pass criteria
  - Examples

### Step 2: Test Gate Validation

**Execute** (in AI agent):
```bash
# Run analyze with gate checking
/speckit.analyze --profile drift --check-gates
```

**Expected Behavior**:
- Gates QG-DRIFT-001 to QG-DRIFT-004 evaluated
- Pass/fail status reported
- Failing gates provide recommendations

---

## Test Case 6: Error Handling

### Test 6A: Missing --scope Parameter

**Execute**:
```bash
/speckit.reverse-engineer --language typescript
# (intentionally omitting --scope)
```

**Expected Behavior**:
- Clear error message: "Missing required argument: --scope"
- Suggestion: "Run with --help for usage information"
- No crash, clean exit

### Test 6B: Non-existent Directory

**Execute**:
```bash
/speckit.analyze --profile drift --scope "nonexistent/**/*.ts"
```

**Expected Behavior**:
- Clear error: "Directory not found: nonexistent"
- Graceful handling, no stack trace

### Test 6C: Empty Codebase

**Execute**:
```bash
mkdir empty-project && cd empty-project
echo "## Spec" > spec.md
/speckit.analyze --profile drift
```

**Expected Behavior**:
- Report generated
- All FRs (if any) flagged as forward drift
- No crashes

---

## Test Case 7: Documentation Accuracy

### Step 1: Verify COMMANDS_GUIDE.md Accuracy

**Check**:
1. Open `.specify/docs/COMMANDS_GUIDE.md` (if present) or online docs
2. Find `/speckit.reverse-engineer` section
3. Verify all flags documented:
   - `--scope` (required)
   - `--exclude` (optional)
   - `--min-confidence` (optional)
   - `--language` (optional)
   - `--output-dir` (optional)
   - `--merge-mode` (optional)

**Validation**:
- All flags in script match documentation
- Examples are accurate
- Output format described correctly

---

## Test Case 8: Version Consistency

### Step 1: Check Version References

**Execute**:
```bash
# Check package version
echo "Package version: v0.4.0"

# Check quality-gates.md version references
grep "v0.4.0" .specify/memory/domains/quality-gates.md

# Check if any old version numbers remain
grep -r "v0.3" .specify/ .claude/
# Expected: No matches (all should be v0.4.0)
```

---

## Success Criteria

### Must Pass (Blocking)

- [✅] All 68 packages extract without errors
- [✅] Command templates include Pass AA and reverse-engineer
- [✅] Scripts are executable and have correct permissions
- [✅] Quality gates (QG-DRIFT-001 to 004) are defined
- [✅] Test fixtures run without crashes
- [✅] Drift detection produces expected output
- [✅] Reverse-engineering produces expected output
- [✅] Error handling is graceful
- [✅] Version references consistent (v0.4.0)

### Should Pass (High Priority)

- [ ] Documentation matches implementation
- [ ] Cross-platform (bash + PowerShell) parity
- [ ] All test fixtures pass validation
- [ ] Quality gates integrate correctly
- [ ] Performance acceptable (< 5 min on fixtures)

### Nice to Have (Medium Priority)

- [ ] Confidence scores calibrated well
- [ ] False positive rate < 10%
- [ ] User-friendly error messages
- [ ] Clear recommendations in reports

---

## Known Issues (v0.4.0)

### Non-Blocking Issues

1. **Shared templates not in packages**: The `templates/shared/drift/` directory is not copied to release packages. This is intentional - shared templates are embedded in command templates.

2. **cp errors during package generation**: macOS shows "illegal option --" warnings during packaging. These are non-fatal and don't affect package contents.

3. **No pre-compiled templates**: Template compilation step shows warning but continues. Compression still works via .COMPRESSED.md files.

4. **Performance not benchmarked**: No empirical performance data yet. Based on design, should be < 5 min for medium projects.

5. **Go/Java untested**: Test fixtures only exist for TypeScript and Python. Go and Java support is implemented but not validated.

---

## Troubleshooting

### Issue: Command not recognized

**Symptoms**: `/speckit.reverse-engineer` shows "command not found"

**Resolution**:
1. Verify package extracted correctly
2. Check `.claude/commands/speckit.reverse-engineer.md` exists
3. Restart AI agent to reload commands
4. Check agent configuration supports custom commands

### Issue: Script permission denied

**Symptoms**: `./reverse-engineer.sh: Permission denied`

**Resolution**:
```bash
chmod +x .specify/scripts/bash/reverse-engineer.sh
```

### Issue: No drift-report.md generated

**Symptoms**: Command runs but no output file

**Resolution**:
1. Check command output for errors
2. Verify you're in a directory with spec.md
3. Check agent has write permissions
4. Try with `--debug` flag (if available)

### Issue: Low confidence scores

**Symptoms**: All extracted requirements have confidence < 0.50

**Resolution**:
- Add `@speckit:FR:` annotations to code
- Add tests with `[TEST:AS-xxx]` markers
- Improve function/variable naming clarity
- Add docstrings/comments

---

## Post-Testing Actions

### If All Tests Pass ✅

1. **Tag release**:
   ```bash
   cd /Users/dmitry.lazarenko/Documents/projects/spec-kit
   git tag v0.4.0
   git push origin v0.4.0
   ```

2. **Upload packages** to GitHub Releases (via CI/CD)

3. **Announce release**:
   - Update README.md with v0.4.0 features
   - Post announcement (if applicable)
   - Update documentation site

4. **Monitor for issues**:
   - Watch GitHub issues
   - Track user feedback
   - Monitor performance reports

### If Tests Fail ❌

1. **Document failures** in issue tracker
2. **Determine severity**:
   - CRITICAL: Blocks release → Fix immediately
   - HIGH: Impacts usability → Fix before wide release
   - MEDIUM/LOW: Can address in v0.4.1

3. **Fix and re-test**:
   - Make fixes in source
   - Re-generate packages
   - Re-run full test suite

4. **Update version if needed**:
   - If fixes are substantial, bump to v0.4.1
   - Update CHANGELOG.md

---

## Testing Log Template

```markdown
## Installation Testing - v0.4.0

**Tester**: __________________
**Date**: __________________
**Environment**: macOS / Windows / Linux
**AI Agent**: claude / cursor / copilot / other

### Test Results

| Test Case | Status | Notes |
|-----------|--------|-------|
| TC1: Package Contents | ☐ Pass ☐ Fail | |
| TC2: TypeScript Fixture | ☐ Pass ☐ Fail | |
| TC3: Python Fixture | ☐ Pass ☐ Fail | |
| TC4: PowerShell | ☐ Pass ☐ Fail | |
| TC5: Quality Gates | ☐ Pass ☐ Fail | |
| TC6: Error Handling | ☐ Pass ☐ Fail | |
| TC7: Documentation | ☐ Pass ☐ Fail | |
| TC8: Version Consistency | ☐ Pass ☐ Fail | |

### Issues Found

1. **Issue**:
   - **Severity**: CRITICAL / HIGH / MEDIUM / LOW
   - **Description**:
   - **Steps to Reproduce**:
   - **Expected**:
   - **Actual**:

### Overall Assessment

☐ APPROVE FOR RELEASE
☐ CONDITIONAL APPROVAL (minor fixes needed)
☐ REJECT (critical issues found)

**Notes**:
```

---

**Guide Version**: 1.0
**Created**: 2026-01-11
**For Release**: v0.4.0

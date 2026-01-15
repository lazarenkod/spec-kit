# Architecture Design: Spec-Code Drift Detection & Reverse-Engineering

**Date**: 2026-01-11  
**Status**: Draft  
**Phase**: Planning  

---

## Executive Summary

This design integrates two complementary features into Spec Kit:

1. **Spec-Code Drift Detection** - Extends `/speckit.analyze` with Pass AA to detect when code diverges from spec requirements
2. **Reverse-Engineering** - New `/speckit.reverse-engineer` command to extract specifications from existing code

Both features leverage:
- **Existing infrastructure**: Artifact registry, cascade detection, quality gates
- **LLM-powered analysis**: Using Claude Code Task agents via Serena MCP tools
- **Multi-language support**: TypeScript, Python, Go, Java/Kotlin
- **Semi-automated workflow**: Preview → user confirmation → apply

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DRIFT DETECTION ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      │
│  │   spec.md    │      │   plan.md    │      │   tasks.md   │      │
│  │  FR-xxx      │      │   ADR-xxx    │      │  T001, T002  │      │
│  │  AS-xxx      │      │   PKG-xxx    │      │  [FR:FR-xxx] │      │
│  └──────┬───────┘      └──────┬───────┘      └──────┬───────┘      │
│         │                     │                     │               │
│         └─────────────────────┴─────────────────────┘               │
│                               │                                     │
│                               ▼                                     │
│                    ┌─────────────────────┐                          │
│                    │  Pass AA: Drift     │                          │
│                    │  Detection Engine   │                          │
│                    └──────────┬──────────┘                          │
│                               │                                     │
│              ┌────────────────┼────────────────┐                    │
│              │                │                │                    │
│              ▼                ▼                ▼                    │
│    ┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐        │
│    │ Code Analyzer   │ │ Annotation  │ │ Diff Comparator │        │
│    │ (Multi-lang)    │ │ Parser      │ │ (Spec ↔ Code)   │        │
│    └─────────────────┘ └─────────────┘ └─────────────────┘        │
│              │                │                │                    │
│              └────────────────┼────────────────┘                    │
│                               ▼                                     │
│                    ┌─────────────────────┐                          │
│                    │  drift-report.md    │                          │
│                    │  DRIFT-xxx items    │                          │
│                    │  Severity: CRITICAL │                          │
│                    │           HIGH      │                          │
│                    │           MEDIUM    │                          │
│                    │           LOW       │                          │
│                    └─────────────────────┘                          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                REVERSE-ENGINEERING ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                       Codebase                               │   │
│  │  src/auth/login.ts, src/users/repository.ts, ...            │   │
│  └──────────────────────┬───────────────────────────────────────┘   │
│                         │                                           │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │  /speckit.reverse-  │                                │
│              │  engineer (command) │                                │
│              └──────────┬──────────┘                                │
│                         │                                           │
│         ┌───────────────┼───────────────┐                           │
│         │               │               │                           │
│         ▼               ▼               ▼                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                   │
│  │ Serena MCP  │ │  LLM Agent  │ │ Annotation  │                   │
│  │ Code Tools  │ │  Extractor  │ │  Parser     │                   │
│  │ (find_sym)  │ │ (FR/AS/NFR) │ │ (@speckit)  │                   │
│  └─────────────┘ └─────────────┘ └─────────────┘                   │
│         │               │               │                           │
│         └───────────────┼───────────────┘                           │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │ reverse-engineered/ │                                │
│              │  directory          │                                │
│              └──────────┬──────────┘                                │
│                         │                                           │
│              ┌──────────┴──────────┐                                │
│              │                     │                                │
│              ▼                     ▼                                │
│   ┌───────────────────┐  ┌──────────────────┐                      │
│   │ extracted-spec.md │  │ drift-report.md  │                      │
│   │  FR-xxx, AS-xxx   │  │  DRIFT-xxx items │                      │
│   │  (from code)      │  │  (vs spec.md)    │                      │
│   └───────────────────┘  └──────────────────┘                      │
│              │                     │                                │
│              └──────────┬──────────┘                                │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │ .extraction-        │                                │
│              │ manifest.yaml       │                                │
│              │ (metadata)          │                                │
│              └─────────────────────┘                                │
│                         │                                           │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │  User Review &      │                                │
│              │  Confirmation       │                                │
│              └──────────┬──────────┘                                │
│                         │                                           │
│                    [approve]                                        │
│                         │                                           │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │  /speckit.specify   │                                │
│              │  (merge/update)     │                                │
│              └─────────────────────┘                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ADR-001: Drift Detection Integration Strategy

**Context**: Extend `/speckit.analyze` vs create new command

**Decision**: Extend `/speckit.analyze` with new Pass AA

**Rationale**:
- Analyze already has 26 detection passes (A-Z in use except AA)
- Existing profile system (`--profile drift`) for targeted execution
- Already integrated with quality gates and artifact registry
- Consistent with user mental model (analyze = validation)

**Alternatives Considered**:
1. **New command** `/speckit.drift` - Rejected: adds cognitive overhead, duplicates infra
2. **Inline in implement** - Rejected: too late in workflow, should catch drift earlier

**Consequences**:
- ✅ Reuses existing infrastructure
- ✅ Natural fit for QA verification (`--profile qa` includes drift)
- ⚠️ Must extend analyze.md detection passes section (currently at ~3000 lines)

---

## ADR-002: Code Analysis Approach (LLM vs AST)

**Context**: Balance between accuracy (LLM) and speed (AST-only)

**Decision**: Hybrid approach - AST for structure, LLM for semantic analysis

**Rationale**:
- AST (via Serena MCP) provides fast, reliable structure extraction
- LLM (via Task agents) understands business logic and intent
- Best of both worlds: speed where possible, intelligence where needed

**Implementation**:
```
PHASE 1: AST Extraction (Fast - Serena MCP tools)
  - find_symbol: Extract all functions, classes, methods
  - search_for_pattern: Find @speckit annotations
  - get_symbols_overview: High-level structure

PHASE 2: LLM Analysis (Slow - Task agents)
  - Semantic analysis of extracted symbols
  - Business logic inference from code patterns
  - Requirements extraction from naming/comments
```

**Tradeoffs**:
| Approach | Accuracy | Speed | Cost | Code Coverage |
|----------|----------|-------|------|---------------|
| AST-only | 60% | Fast | Low | 100% |
| LLM-only | 95% | Slow | High | Limited by context |
| Hybrid | 85% | Medium | Medium | 100% |

**Alternatives Considered**:
1. **AST-only** - Rejected: misses semantic drift (renamed functions with same signature)
2. **LLM-only** - Rejected: too slow for large codebases, context limits

---

## ADR-003: Drift Granularity (File vs Function vs Line)

**Context**: What level of granularity to report drift at

**Decision**: Function/method level with line-level details on demand

**Rationale**:
- Function level = actionable units (can fix one function at a time)
- Line level = too noisy (every typo fix triggers drift)
- File level = too coarse (hides which specific API changed)

**Drift Item Format**:
```markdown
### DRIFT-001: Undocumented API Endpoint (HIGH)

**Spec Coverage**: ❌ Not documented
**Code Location**: `src/api/routes/users.ts:42-58`
**Function Signature**: `POST /api/v1/users/:id/archive`
**Detected By**: Code Analyzer (undocumented_api pattern)

**Current Implementation**:
```typescript
router.post('/users/:id/archive', async (req, res) => {
  // 17 lines of implementation
});
```

**Recommendation**: Add AS-xxx scenario or mark as internal-only
**Auto-Fix Available**: ❌ Requires manual spec update
```

**Alternatives Considered**:
1. **Line-level** - Rejected: too noisy (100s of items)
2. **Component-level** - Rejected: too coarse for APIs

---

## ADR-004: Reverse-Engineering Output Format

**Context**: Where to place extracted specifications

**Decision**: Separate `reverse-engineered/` directory with merge workflow

**Rationale**:
- Keeps extracted content isolated from canonical spec.md
- User reviews before merging (semi-automated workflow)
- Enables diff comparison (extracted vs canonical)
- Non-destructive (can discard if quality is poor)

**Directory Structure**:
```
specs/{feature}/
├── spec.md                    # Canonical specification
├── plan.md
├── tasks.md
├── .artifact-registry.yaml
└── reverse-engineered/        # NEW
    ├── .extraction-manifest.yaml
    ├── extracted-spec.md      # Extracted from code
    ├── drift-report.md        # Diff vs spec.md
    └── extraction-log.md      # Agent reasoning trace
```

**Alternatives Considered**:
1. **Direct spec.md update** - Rejected: destructive, no undo
2. **Comments in spec.md** - Rejected: pollutes canonical doc
3. **Git branch** - Rejected: overkill, not discoverable

---

## ADR-005: Language Support Strategy

**Context**: Prioritize which languages to support first

**Decision**: TypeScript/JavaScript → Python → Go → Java/Kotlin

**Rationale**:
- TypeScript = most common in Spec Kit target audience (web/fullstack)
- Python = second most common (ML/backend)
- Go = growing backend ecosystem
- Java/Kotlin = enterprise legacy codebases (brownfield)

**Language-Specific Patterns**:

### TypeScript/JavaScript
```typescript
// Pattern: Express/Fastify route handlers
router.post('/api/v1/resource', (req, res) => {})
→ Extract as: FR-xxx: System MUST support POST /api/v1/resource

// Pattern: Zod/Yup validation schemas
const schema = z.object({ email: z.string().email() })
→ Extract as: AS-xxx validation scenario

// Pattern: Test files (*.test.ts, *.spec.ts)
it('should return 404 for missing user', () => {})
→ Extract as: AS-xxx error scenario
```

### Python
```python
# Pattern: FastAPI/Flask route decorators
@app.post("/api/v1/resource")
→ Extract as: FR-xxx

# Pattern: Pydantic models
class User(BaseModel):
    email: EmailStr
→ Extract as: Entity + validation rules

# Pattern: Pytest tests
def test_should_reject_invalid_email():
→ Extract as: AS-xxx
```

### Go
```go
// Pattern: HTTP handler registration
http.HandleFunc("/api/v1/resource", handler)
→ Extract as: FR-xxx

// Pattern: Struct tags
type User struct {
    Email string `json:"email" validate:"required,email"`
}
→ Extract as: Entity + validation

// Pattern: Table-driven tests
{name: "invalid email", want: error}
→ Extract as: AS-xxx
```

### Java/Kotlin
```java
// Pattern: Spring @RestController
@PostMapping("/api/v1/resource")
→ Extract as: FR-xxx

// Pattern: Jakarta Bean Validation
@Email @NotNull
→ Extract as: Validation rules

// Pattern: JUnit @Test
@Test void shouldRejectInvalidEmail()
→ Extract as: AS-xxx
```

---

## File Changes

### 1. Extend `/speckit.analyze` command

**File**: `templates/commands/analyze.md`

**Changes**:
```yaml
# Add new detection pass at line ~2600 (after Pass Y)

## Detection Passes

### Pass AA: Spec-Code Drift Detection

**Purpose**: Detect drift between specification requirements and implementation code

**Severity Levels**:
- CRITICAL: Implemented API not in spec (breaking change risk)
- HIGH: Spec requirement not implemented (missing functionality)
- MEDIUM: Implementation diverges from spec (behavioral drift)
- LOW: Documentation drift (comments outdated)

**Detection Algorithm**:

```text
DRIFT_DETECTION_ALGORITHM:

STEP 1: Load Artifacts
  spec = READ(FEATURE_DIR/spec.md)
  plan = READ(FEATURE_DIR/plan.md)
  tasks = READ(FEATURE_DIR/tasks.md)
  registry = READ_REGISTRY()

STEP 2: Extract Spec Requirements
  spec_frs = EXTRACT_FRS(spec)          # FR-001, FR-002, ...
  spec_ass = EXTRACT_ASS(spec)          # AS-1A, AS-1B, ...
  spec_apis = EXTRACT_API_SPECS(spec)   # Endpoints from plan
  spec_nfrs = EXTRACT_NFRS(spec)        # Performance, security

STEP 3: Analyze Codebase (Parallel Task Agents)
  LAUNCH Task agents in parallel:
    - typescript-analyzer → TypeScript/JavaScript files
    - python-analyzer → Python files
    - go-analyzer → Go files
    - java-analyzer → Java/Kotlin files
  
  EACH agent uses Serena MCP tools:
    - find_symbol: Extract public APIs
    - search_for_pattern: Find @speckit annotations
    - get_symbols_overview: Get structure

  AGGREGATE results into code_inventory:
    - implemented_apis[]
    - annotated_frs[]      # Functions with @speckit:FR:
    - annotated_tests[]    # Tests with [TEST:AS-xxx]
    - undocumented_apis[]  # Public without @speckit

STEP 4: Compare (Diff Comparator)
  drift_items = []

  # Forward drift: Spec → Code
  FOR fr IN spec_frs:
    IF fr NOT IN annotated_frs:
      drift_items.append({
        id: "DRIFT-{N}",
        type: "unimplemented_requirement",
        severity: HIGH,
        fr_id: fr.id,
        description: "FR-{id} specified but not implemented"
      })

  FOR api IN spec_apis:
    IF api NOT IN implemented_apis:
      drift_items.append({
        id: "DRIFT-{N}",
        type: "missing_api",
        severity: CRITICAL,
        api: api.signature,
        description: "API {signature} in spec but not in code"
      })

  # Reverse drift: Code → Spec
  FOR api IN undocumented_apis:
    IF api.visibility == "public":
      drift_items.append({
        id: "DRIFT-{N}",
        type: "undocumented_api",
        severity: HIGH,
        api: api.signature,
        code_location: api.file_path,
        description: "Public API {signature} not documented in spec"
      })

  # Test coverage drift
  FOR as IN spec_ass WHERE as.requires_test == YES:
    IF as NOT IN annotated_tests:
      drift_items.append({
        id: "DRIFT-{N}",
        type: "missing_test",
        severity: MEDIUM,
        as_id: as.id,
        description: "AS-{id} requires test but no [TEST:AS-{id}] found"
      })

STEP 5: Generate Report
  WRITE(FEATURE_DIR/drift-report.md, {
    summary: {
      total_items: drift_items.length,
      critical: count(severity=CRITICAL),
      high: count(severity=HIGH),
      medium: count(severity=MEDIUM),
      low: count(severity=LOW)
    },
    items: drift_items,
    recommendations: GENERATE_REMEDIATION_PLAN(drift_items)
  })

STEP 6: Update Artifact Registry
  registry.artifacts.drift_report = {
    exists: true,
    version: "1.0",
    checksum: CALCULATE_CHECKSUM(drift-report.md),
    updated_at: NOW(),
    item_count: drift_items.length
  }
  UPDATE_REGISTRY(registry)
```

**Agents**:
```yaml
subagents:
  - role: typescript-drift-detector
    role_group: DRIFT_ANALYSIS
    parallel: true
    depends_on: []
    priority: 10
    trigger: "when analyzing TypeScript/JavaScript code for drift"
    prompt: |
      Analyze TypeScript/JavaScript codebase for spec-code drift.
      
      Use Serena MCP tools:
      1. find_symbol: Extract all exported functions, classes, methods
      2. search_for_pattern: Find @speckit:FR: and [TEST:AS-xxx] annotations
      3. get_symbols_overview: Get high-level structure
      
      Compare against spec.md FR-xxx and AS-xxx requirements.
      Report drift items with severity levels.

  - role: python-drift-detector
    role_group: DRIFT_ANALYSIS
    parallel: true
    depends_on: []
    priority: 10
    trigger: "when analyzing Python code for drift"
    prompt: |
      Analyze Python codebase for spec-code drift.
      
      Use Serena MCP tools for FastAPI/Flask/Django patterns.
      Extract route decorators, Pydantic models, pytest tests.
      Compare against spec requirements.

  - role: drift-report-compiler
    role_group: REPORTING
    parallel: false
    depends_on: [typescript-drift-detector, python-drift-detector, go-drift-detector, java-drift-detector]
    priority: 20
    prompt: |
      Compile drift-report.md from all language-specific drift items.
      
      Aggregate results, deduplicate, prioritize by severity.
      Generate actionable recommendations.
```

**Output Format**:
```markdown
# Drift Detection Report

**Feature**: {feature_name}
**Generated**: {ISO_DATE}
**Profile**: Pass AA (Drift Detection)

## Summary

| Severity | Count | Action Required |
|----------|-------|-----------------|
| CRITICAL | 2 | Immediate fix |
| HIGH | 5 | Fix before merge |
| MEDIUM | 8 | Review recommended |
| LOW | 12 | Informational |

**Overall Verdict**: ⚠️ DRIFT DETECTED (7 blocking issues)

## Drift Items

### DRIFT-001: Undocumented API Endpoint (CRITICAL)

**Type**: undocumented_api
**Location**: `src/api/routes/users.ts:42-58`
**API Signature**: `POST /api/v1/users/:id/archive`

**Current Implementation**:
```typescript
router.post('/users/:id/archive', async (req, res) => {
  const { id } = req.params;
  const user = await User.findById(id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  user.archived = true;
  await user.save();
  return res.json({ success: true });
});
```

**Drift Analysis**:
- ❌ No FR-xxx in spec.md covers this endpoint
- ❌ No AS-xxx acceptance scenario
- ❌ No @speckit:FR: annotation in code

**Recommendation**:
1. Add to spec.md:
   ```markdown
   - **FR-012**: System MUST support archiving users
     - *Acceptance Scenarios*: AS-12A
   ```
2. Add acceptance scenario:
   ```gherkin
   Scenario: AS-12A - Archive user successfully
     Given user "john@example.com" exists
     When I POST /api/v1/users/{id}/archive
     Then response status is 200
     And user.archived is true
   ```
3. Annotate code:
   ```typescript
   // @speckit:FR:FR-012 Archive user endpoint
   router.post('/users/:id/archive', async (req, res) => {
   ```

**Auto-Fix**: ❌ Requires manual spec update

---

### DRIFT-002: Unimplemented Requirement (HIGH)

**Type**: unimplemented_requirement
**FR ID**: FR-007
**Spec Location**: `spec.md:245`

**Requirement**:
> FR-007: System MUST validate email addresses using RFC 5322 standard

**Current Implementation**:
- ❌ No code found with @speckit:FR:FR-007
- ❌ No validation function detected

**Recommendation**:
1. Implement validation (Phase 2 of tasks.md)
2. Add annotation:
   ```typescript
   // @speckit:FR:FR-007 RFC 5322 email validation
   function validateEmail(email: string): boolean {
     return RFC5322_REGEX.test(email);
   }
   ```

**Auto-Fix**: ❌ Requires implementation

---

## Recommendations

### Immediate Actions (CRITICAL)
1. Document DRIFT-001 undocumented API in spec.md
2. Remove or mark as internal-only if not intended for public use

### Before Merge (HIGH)
1. Implement DRIFT-002 (FR-007) email validation
2. Review 3 other unimplemented FRs

### Review Recommended (MEDIUM)
1. Add [TEST:AS-xxx] annotations to existing tests (8 items)
2. Update stale inline comments (4 items)

## Traceability Impact

**Current Coverage**:
- FR → Code: 15/20 (75%) ⚠️ Below 80% threshold
- AS → Test: 22/28 (79%) ⚠️ Below 80% threshold

**Post-Fix Coverage** (estimated):
- FR → Code: 19/20 (95%) ✅
- AS → Test: 26/28 (93%) ✅
```
```

**Integration with Quality Gates**:
```yaml
# Add new quality gate in memory/domains/quality-gates.md

### QG-DRIFT-001: Spec-Code Alignment

**Level**: MUST (for production deployments)
**Applies to**: Post-implementation QA
**Phase**: Pre-merge

Code implementation MUST align with specification requirements.

**Threshold**: FR → Code coverage >= 80%

**Validation**:
```bash
/speckit.analyze --profile drift
# Pass AA runs drift detection
```

**Violations**: HIGH - Implementation deviates from spec
```

---

### 2. Create `/speckit.reverse-engineer` command

**File**: `templates/commands/reverse-engineer.md` (NEW)

**Content**:
```yaml
---
description: |
  Extract specifications from existing code using LLM-powered analysis.
  Creates reverse-engineered/ directory with extracted-spec.md and drift-report.md.
  
  Use Cases:
  - Brownfield projects with missing documentation
  - Legacy codebases needing spec generation
  - Validation that implementation matches business intent
  - Knowledge transfer (code → readable spec)

persona: documentation-agent
handoffs:
  - label: Review Extracted Spec
    agent: speckit.specify
    prompt: |
      Review extracted-spec.md and merge relevant sections into canonical spec.md.
      
      User should review reverse-engineered/ content first.
      Cherry-pick valid requirements, discard hallucinations.
    auto: false
    condition:
      - "extracted-spec.md generated successfully"
      - "User reviewed and approved extraction quality"
    gates:
      - name: "Extraction Quality Gate"
        check: "Extracted spec has >= 5 FR-xxx items"
        block_if: "< 5 requirements extracted"
        message: "Extraction yielded too few requirements - verify scope is correct"
      - name: "Hallucination Check Gate"
        check: "LLM confidence >= 0.70 for extracted items"
        block_if: "Average confidence < 0.70"
        message: "Low confidence extraction - may contain hallucinations"
    post_actions:
      - "log: Extraction complete, awaiting user review"

  - label: Update Spec from Extraction
    agent: speckit.specify
    prompt: |
      Merge approved items from extracted-spec.md into spec.md.
      User has reviewed and selected specific FR-xxx/AS-xxx to merge.
    auto: false
    condition:
      - "User selected specific items to merge"
      - "Quality check passed"

pre_gates:
  - name: "Feature Directory Gate"
    check: "FEATURE_DIR exists"
    block_if: "FEATURE_DIR missing"
    message: "Create feature directory first with /speckit.specify --init"
    
  - name: "Scope Definition Gate"
    check: "User provided scope (file paths, modules, or glob patterns)"
    block_if: "No scope defined"
    message: "Specify scope for reverse engineering (e.g., 'src/auth/**/*.ts')"

  - name: "No Existing Extraction Gate"
    check: "reverse-engineered/ directory does not exist"
    block_if: "reverse-engineered/ already exists"
    message: "Previous extraction exists - use --force to overwrite or review existing content"

claude_code:
  model: sonnet
  reasoning_mode: extended
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 8000
        max_parallel: 2
        batch_delay: 8000
      pro:
        thinking_budget: 16000
        max_parallel: 4
        batch_delay: 4000
      max:
        thinking_budget: 32000
        max_parallel: 8
        batch_delay: 1500
  cache_hierarchy: full
  orchestration:
    max_parallel: 8
    role_isolation: true
    wave_overlap:
      enabled: true
      threshold: 0.70
  subagents:
    # Wave 1: Code Discovery (parallel)
    - role: code-discoverer
      role_group: DISCOVERY
      parallel: true
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        Discover all code files in SCOPE using Serena MCP tools.
        
        1. Use find_file with glob patterns from SCOPE
        2. Filter by language (TypeScript, Python, Go, Java)
        3. Exclude test files (save for later wave)
        4. Output: List of discovered files grouped by type

    - role: annotation-extractor
      role_group: DISCOVERY
      parallel: true
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        Extract existing @speckit annotations from code.
        
        Use search_for_pattern to find:
        - @speckit:FR:FR-xxx
        - [TEST:AS-xxx]
        - [FR:FR-xxx] in comments
        
        Output: Map of file → annotations

    # Wave 2: Structure Analysis (parallel, depends on Wave 1)
    - role: api-extractor
      role_group: ANALYSIS
      parallel: true
      depends_on: [code-discoverer]
      priority: 20
      model_override: sonnet
      prompt: |
        Extract public APIs from discovered code files.
        
        For each file:
        1. Use find_symbol to extract exported functions/classes
        2. Use get_symbols_overview for structure
        3. Identify HTTP routes, GraphQL resolvers, gRPC services
        4. Extract signatures, parameters, return types
        
        Output: API inventory with signatures

    - role: entity-extractor
      role_group: ANALYSIS
      parallel: true
      depends_on: [code-discoverer]
      priority: 20
      model_override: sonnet
      prompt: |
        Extract domain entities and data models.
        
        Find:
        - TypeScript interfaces, types, classes
        - Python Pydantic/dataclass models
        - Go structs with json tags
        - Java/Kotlin entity classes
        
        Output: Entity registry with fields and validation rules

    - role: test-analyzer
      role_group: ANALYSIS
      parallel: true
      depends_on: [code-discoverer]
      priority: 20
      model_override: sonnet
      prompt: |
        Analyze test files to extract acceptance scenarios.
        
        Parse test descriptions:
        - Jest/Vitest: it('should...', () => {})
        - Pytest: def test_should_...():
        - Go: func TestShould...(t *testing.T)
        - JUnit: @Test void shouldDoSomething()
        
        Convert to AS-xxx scenarios with Given/When/Then

    # Wave 3: LLM Synthesis (depends on Wave 2)
    - role: requirement-synthesizer
      role_group: SYNTHESIS
      parallel: false
      depends_on: [api-extractor, entity-extractor, annotation-extractor]
      priority: 30
      model_override: opus  # Use Opus for complex reasoning
      prompt: |
        Synthesize functional requirements from code analysis.
        
        Input: API inventory, entity registry, annotations
        
        For each API/entity:
        1. Infer business intent from naming and structure
        2. Extract validation rules from code
        3. Identify CRUD operations
        4. Detect security requirements (auth checks)
        5. Infer NFRs from implementation patterns
        
        Output: FR-xxx items with confidence scores (0.0-1.0)
        
        Confidence scoring:
        - 0.90-1.0: Has @speckit annotation (explicit)
        - 0.70-0.89: Clear naming + tests (high confidence)
        - 0.50-0.69: Inferred from patterns (medium confidence)
        - <0.50: Speculative (flag for review)

    - role: scenario-synthesizer
      role_group: SYNTHESIS
      parallel: false
      depends_on: [test-analyzer, api-extractor]
      priority: 30
      model_override: opus
      prompt: |
        Synthesize acceptance scenarios from tests and API contracts.
        
        For each test case:
        1. Convert to Gherkin format (Given/When/Then)
        2. Extract expected inputs/outputs
        3. Identify error scenarios
        4. Map to FR-xxx requirements
        
        Output: AS-xxx scenarios with FR mappings and confidence

    # Wave 4: Report Generation (depends on Wave 3)
    - role: spec-compiler
      role_group: REPORTING
      parallel: false
      depends_on: [requirement-synthesizer, scenario-synthesizer]
      priority: 40
      model_override: sonnet
      prompt: |
        Compile extracted-spec.md from synthesized requirements.
        
        Follow spec-template.md structure:
        1. User Scenarios (from AS-xxx)
        2. Requirements (FR-xxx with confidence)
        3. Edge Cases (from error tests)
        4. NFRs (inferred from patterns)
        5. Traceability (FR → AS mapping)
        
        Flag low-confidence items for review.

    - role: drift-comparator
      role_group: REPORTING
      parallel: true
      depends_on: [spec-compiler]
      priority: 40
      model_override: sonnet
      prompt: |
        Compare extracted-spec.md with canonical spec.md (if exists).
        
        Generate drift-report.md showing:
        1. Requirements in code but not in spec (additions)
        2. Requirements in spec but not in code (gaps)
        3. Conflicting definitions (mismatches)
        
        Use same DRIFT-xxx format as Pass AA.

    - role: manifest-generator
      role_group: REPORTING
      parallel: false
      depends_on: [spec-compiler, drift-comparator]
      priority: 50
      model_override: haiku
      prompt: |
        Generate .extraction-manifest.yaml with metadata.
        
        Include:
        - Extraction timestamp
        - Scope (files analyzed)
        - Confidence summary
        - Agent reasoning trace
        - Quality metrics

scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

## Goal

Extract specifications from existing code using LLM-powered analysis. This command:

1. **Analyzes codebase** in specified scope (file paths, modules, globs)
2. **Extracts requirements** (FR-xxx) from APIs, entities, tests
3. **Synthesizes scenarios** (AS-xxx) from test cases
4. **Generates specifications** in `reverse-engineered/` directory
5. **Compares with canonical spec** (if exists) and reports drift

## Output Structure

```
specs/{feature}/
└── reverse-engineered/
    ├── .extraction-manifest.yaml  # Metadata
    ├── extracted-spec.md          # Synthesized spec from code
    ├── drift-report.md            # Diff vs spec.md (if exists)
    └── extraction-log.md          # Agent reasoning trace
```

## Operating Constraints

**STRICTLY NON-DESTRUCTIVE**: Do NOT modify any existing files. All output goes to `reverse-engineered/` directory.

**User Review Required**: Extracted specifications may contain:
- Hallucinations (inferred requirements not actually implemented)
- Low-confidence items (< 0.70 confidence score)
- Missing context (code without comments is ambiguous)

User MUST review `extracted-spec.md` before merging into `spec.md`.

## Extraction Algorithm

```text
REVERSE_ENGINEER_ALGORITHM:

STEP 1: Parse Scope
  IF $ARGUMENTS contains file paths:
    SCOPE_FILES = explicit file list
  ELIF $ARGUMENTS contains glob patterns:
    SCOPE_FILES = GLOB(patterns)
  ELIF $ARGUMENTS contains module names:
    SCOPE_FILES = DISCOVER_MODULE_FILES(modules)
  ELSE:
    ERROR: "No scope defined - specify files, globs, or modules"

STEP 2: Discover Code (code-discoverer agent)
  discovered_files = FIND_FILES(SCOPE_FILES)
  GROUP by language:
    typescript_files[]
    python_files[]
    go_files[]
    java_files[]
  EXCLUDE test files (defer to Wave 2)

STEP 3: Extract Structure (Parallel - Wave 2)
  LAUNCH Task agents in parallel:
    - api-extractor → Extract public APIs
    - entity-extractor → Extract domain entities
    - annotation-extractor → Find @speckit annotations
  
  AGGREGATE results:
    api_inventory = {
      endpoint: "/api/v1/users",
      method: "POST",
      signature: "createUser(data: CreateUserDto): Promise<User>",
      file: "src/api/users.ts:42",
      annotations: ["@speckit:FR:FR-003"]
    }[]
    
    entity_inventory = {
      name: "User",
      fields: {email: "string", password: "string"},
      validations: {email: "RFC5322", password: "min:8"}
    }[]

STEP 4: Analyze Tests (test-analyzer agent)
  test_files = FIND_TEST_FILES(SCOPE_FILES)
  FOR test_file IN test_files:
    test_cases = PARSE_TEST_CASES(test_file)
    FOR test IN test_cases:
      as_item = CONVERT_TO_GHERKIN(test)
      as_item.confidence = ESTIMATE_CONFIDENCE(test)

STEP 5: Synthesize Requirements (LLM - Opus)
  frs = []
  FOR api IN api_inventory:
    IF api.annotations:
      # Explicit FR reference
      fr = api.annotations.FR_ID
      fr.confidence = 1.0
    ELSE:
      # Infer from naming and structure
      fr = LLM_INFER_FR(api, entity_inventory, test_cases)
      fr.confidence = 0.50 to 0.89
    frs.append(fr)

STEP 6: Synthesize Scenarios (LLM - Opus)
  ass = []
  FOR test IN test_cases:
    as_item = LLM_CONVERT_TO_AS(test)
    as_item.linked_fr = FIND_FR_MATCH(as_item, frs)
    ass.append(as_item)

STEP 7: Compile Spec (spec-compiler agent)
  extracted_spec = RENDER_TEMPLATE("spec-template.md", {
    frs: frs,
    ass: ass,
    entities: entity_inventory,
    confidence_summary: {
      high: count(frs, confidence >= 0.90),
      medium: count(frs, 0.70 <= confidence < 0.90),
      low: count(frs, confidence < 0.70)
    }
  })
  
  WRITE(reverse-engineered/extracted-spec.md, extracted_spec)

STEP 8: Compare with Canonical (drift-comparator agent)
  IF exists(FEATURE_DIR/spec.md):
    canonical_spec = READ(FEATURE_DIR/spec.md)
    canonical_frs = EXTRACT_FRS(canonical_spec)
    
    drift_items = []
    
    # Code → Spec (additions)
    FOR fr IN frs:
      IF fr NOT IN canonical_frs:
        drift_items.append({
          type: "new_in_code",
          severity: HIGH,
          fr: fr,
          description: "FR-{id} implemented in code but not in spec"
        })
    
    # Spec → Code (gaps)
    FOR canonical_fr IN canonical_frs:
      IF canonical_fr NOT IN frs:
        drift_items.append({
          type: "missing_in_code",
          severity: CRITICAL,
          fr: canonical_fr,
          description: "FR-{id} in spec but not implemented"
        })
    
    WRITE(reverse-engineered/drift-report.md, drift_items)

STEP 9: Generate Manifest (manifest-generator agent)
  manifest = {
    version: "1.0",
    extracted_at: NOW(),
    scope: SCOPE_FILES,
    files_analyzed: discovered_files.length,
    confidence_summary: {
      high: count(frs, confidence >= 0.90),
      medium: count(frs, 0.70 <= confidence < 0.90),
      low: count(frs, confidence < 0.70),
      average: mean(frs.confidence)
    },
    extraction_quality: CALCULATE_QUALITY(frs, ass),
    agents_used: [list of agent names],
    reasoning_trace: extraction_log
  }
  
  WRITE(reverse-engineered/.extraction-manifest.yaml, manifest)

STEP 10: Output Summary
  OUTPUT: """
  ## Reverse-Engineering Complete
  
  **Extracted**: {frs.length} requirements, {ass.length} scenarios
  **Confidence**: {manifest.confidence_summary}
  **Quality**: {manifest.extraction_quality}/100
  
  **Review Required**:
  - {count low confidence items} low-confidence items need validation
  - {count potential hallucinations} items may be hallucinations
  
  **Next Steps**:
  1. Review `reverse-engineered/extracted-spec.md`
  2. Verify accuracy of extracted requirements
  3. Run `/speckit.specify` to merge approved items
  """
```

## Confidence Scoring

```text
CONFIDENCE_LEVELS = {
  EXPLICIT: {
    range: [0.90, 1.00],
    trigger: "@speckit:FR: annotation present",
    meaning: "Requirement explicitly documented in code"
  },
  HIGH: {
    range: [0.70, 0.89],
    trigger: "Clear naming + tests + patterns",
    meaning: "Strong evidence from multiple sources"
  },
  MEDIUM: {
    range: [0.50, 0.69],
    trigger: "Inferred from patterns only",
    meaning: "Likely correct but needs validation"
  },
  LOW: {
    range: [0.00, 0.49],
    trigger: "Speculative inference",
    meaning: "May be hallucination - requires review"
  }
}

CALCULATE_ITEM_CONFIDENCE(item, context):
  score = 0.0
  
  # Evidence from annotations
  IF item.has_annotation:
    score += 0.50
  
  # Evidence from tests
  IF item.has_test_coverage:
    score += 0.20
  
  # Evidence from naming
  IF item.name_clarity_score > 0.80:
    score += 0.15
  
  # Evidence from documentation
  IF item.has_comment OR item.has_docstring:
    score += 0.10
  
  # Evidence from patterns
  IF item.follows_common_pattern:
    score += 0.05
  
  RETURN min(score, 1.0)
```

## Hallucination Detection

```text
DETECT_HALLUCINATIONS(extracted_frs, code_inventory):

  hallucination_flags = []
  
  FOR fr IN extracted_frs:
    IF fr.confidence < 0.50:
      hallucination_flags.append({
        fr_id: fr.id,
        reason: "Low confidence score",
        severity: MEDIUM
      })
    
    IF NOT fr.has_code_evidence:
      hallucination_flags.append({
        fr_id: fr.id,
        reason: "No code evidence found",
        severity: HIGH
      })
    
    IF fr.description contains ["should", "might", "could"]:
      hallucination_flags.append({
        fr_id: fr.id,
        reason: "Speculative language in description",
        severity: LOW
      })
  
  RETURN hallucination_flags
```

## Example Output

### extracted-spec.md

```markdown
# Feature Specification: User Management (Extracted from Code)

**Extracted**: 2026-01-11
**Scope**: src/users/**/*.ts
**Confidence**: 82% average (15 high, 8 medium, 2 low)

⚠️ **Review Required**: This specification was reverse-engineered from code.
Verify accuracy before using for implementation planning.

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST allow users to create accounts [Confidence: 0.95]
  - *Evidence*: POST /api/v1/users endpoint, createUser() function, tests present
  - *Acceptance Scenarios*: AS-1A, AS-1B
  - *Code Location*: `src/api/users.ts:42`

- **FR-002**: System MUST validate email addresses [Confidence: 0.88]
  - *Evidence*: validateEmail() function, Zod schema, tests present
  - *Acceptance Scenarios*: AS-2A
  - *Code Location*: `src/validators/email.ts:12`

- **FR-003**: System MUST hash passwords before storage [Confidence: 0.92]
  - *Evidence*: bcrypt.hash() calls, security pattern detected
  - *Acceptance Scenarios*: AS-3A
  - *Code Location*: `src/auth/password.ts:28`

⚠️ **FR-004**: System MAY support OAuth login [Confidence: 0.45]
  - *Evidence*: Commented-out OAuth code, no tests
  - *Status*: **LOW CONFIDENCE** - May be hallucination or planned feature
  - *Code Location*: `src/auth/oauth.ts:5` (commented out)
  - *Action Required*: **Manual review** - Verify if intended or remove

---

## Acceptance Scenarios

### User Story 1 - User Registration (Priority: P1)

#### Acceptance Criteria (Gherkin)

```gherkin
Scenario: AS-1A - Create user with valid data [HAPPY_PATH] [Confidence: 0.95]
  Given no user with email "john@example.com" exists
  When I POST /api/v1/users with:
    | email | john@example.com |
    | password | SecurePass123 |
  Then response status is 201
  And response contains "id"
  And password is hashed in database

# Extracted from: src/api/users.test.ts:15
# Test: 'should create user with valid data'
```

---

## Quality Metrics

**Extraction Quality Score**: 78/100

| Dimension | Score | Details |
|-----------|-------|---------|
| Code Coverage | 85% | 17/20 files analyzed |
| Annotation Coverage | 40% | 6/15 FRs had explicit @speckit |
| Test Coverage | 90% | 18/20 tests converted to AS |
| Confidence | 82% | 15 high, 8 medium, 2 low |
| Hallucination Risk | 15% | 2 low-confidence items flagged |

**Review Checklist**:
- [ ] Verify FR-004 (low confidence)
- [ ] Verify FR-007 (no test coverage)
- [ ] Check AS-4A (inferred from incomplete test)
```

### .extraction-manifest.yaml

```yaml
version: "1.0"
extracted_at: "2026-01-11T10:30:00Z"
scope:
  patterns:
    - "src/users/**/*.ts"
    - "src/auth/**/*.ts"
  files_analyzed: 20
  files_excluded: 8  # test files

confidence_summary:
  high: 15         # >= 0.90
  medium: 8        # 0.70-0.89
  low: 2           # < 0.70
  average: 0.82

extraction_quality:
  score: 78
  dimensions:
    code_coverage: 85
    annotation_coverage: 40
    test_coverage: 90
    confidence: 82
    hallucination_risk: 15

requirements:
  total: 25
  with_code_evidence: 23
  with_test_coverage: 18
  with_annotations: 6

scenarios:
  total: 20
  converted_from_tests: 18
  inferred_from_code: 2

agents_used:
  - code-discoverer
  - api-extractor
  - entity-extractor
  - annotation-extractor
  - test-analyzer
  - requirement-synthesizer
  - scenario-synthesizer
  - spec-compiler
  - drift-comparator

reasoning_trace_file: "extraction-log.md"
```
```

**File**: `scripts/bash/reverse-engineer.sh` (NEW)

```bash
#!/bin/bash
# Reverse-engineer specifications from code

FEATURE_DIR="${1:-.}"
SCOPE="${2:-src/**/*}"

# Prerequisites check
if [ ! -d "$FEATURE_DIR" ]; then
  echo "Error: Feature directory not found: $FEATURE_DIR"
  exit 1
fi

# Create output directory
mkdir -p "$FEATURE_DIR/reverse-engineered"

# Run reverse-engineer command
echo "Reverse-engineering from scope: $SCOPE"
echo "Output will be in: $FEATURE_DIR/reverse-engineered/"
```

**File**: `scripts/powershell/reverse-engineer.ps1` (NEW)

```powershell
# PowerShell version (similar to bash)
param(
    [string]$FeatureDir = ".",
    [string]$Scope = "src/**/*"
)

if (!(Test-Path $FeatureDir)) {
    Write-Error "Feature directory not found: $FeatureDir"
    exit 1
}

New-Item -ItemType Directory -Force -Path "$FeatureDir/reverse-engineered"
Write-Host "Reverse-engineering from scope: $Scope"
```

---

### 3. Shared Infrastructure Templates

**File**: `templates/shared/drift/drift-detection.md` (NEW)

```markdown
# Drift Detection Framework

## Purpose

Detect and report drift between specification requirements and code implementation.

## Drift Types

| Type | Description | Severity | Direction |
|------|-------------|----------|-----------|
| undocumented_api | Public API not in spec | HIGH | Code → Spec |
| unimplemented_requirement | FR in spec not in code | CRITICAL | Spec → Code |
| missing_test | AS requires test but none exists | MEDIUM | Spec → Code |
| behavioral_drift | Implementation diverges from spec | HIGH | Bidirectional |
| documentation_drift | Comments/docs outdated | LOW | N/A |
| annotation_missing | Code lacks @speckit markers | MEDIUM | Code → Spec |

## Detection Patterns

### TypeScript/JavaScript

```text
UNDOCUMENTED_API_PATTERNS = [
  "router.(get|post|put|delete)\\(",        # Express routes
  "@(Get|Post|Put|Delete)\\(",              # NestJS decorators
  "app.(get|post|put|delete)\\(",           # Fastify routes
  "export (async )?function [A-Z]",         # Exported functions
  "export class [A-Z].*\\{.*public"         # Exported classes with public methods
]

VALIDATION_PATTERNS = [
  "z\\.(string|number|boolean|object)\\(", # Zod schemas
  "\\.email\\(\\)",                         # Email validation
  "\\.min\\(\\d+\\)",                       # Min length/value
  "yup\\.(string|number|object)"            # Yup schemas
]

TEST_PATTERNS = [
  "it\\(['\"]should",                       # Jest/Vitest
  "describe\\(['\"]",                       # Test suites
  "test\\(['\"]"                            # Test cases
]
```

### Python

```text
UNDOCUMENTED_API_PATTERNS = [
  "@app\\.(get|post|put|delete)\\(",        # FastAPI routes
  "@bp\\.route\\(",                         # Flask blueprints
  "def (get|post|put|delete)_\\w+\\(",     # Django views
]

VALIDATION_PATTERNS = [
  "class \\w+\\(BaseModel\\)",              # Pydantic models
  "Field\\(.*validate",                     # Pydantic validators
  "@validator",                             # Pydantic validator decorators
]

TEST_PATTERNS = [
  "def test_\\w+",                          # Pytest
  "def test_should_",                       # Pytest BDD-style
  "@pytest\\.mark",                         # Pytest markers
]
```

## Severity Calculation

```text
CALCULATE_SEVERITY(drift_item):
  
  IF drift_item.type == "unimplemented_requirement":
    IF drift_item.fr.priority == "P1":
      RETURN CRITICAL
    ELSE:
      RETURN HIGH
  
  IF drift_item.type == "undocumented_api":
    IF drift_item.api.visibility == "public":
      RETURN HIGH
    ELSE:
      RETURN MEDIUM
  
  IF drift_item.type == "missing_test":
    IF drift_item.as.requires_test == YES:
      RETURN MEDIUM
    ELSE:
      RETURN LOW
  
  IF drift_item.type == "behavioral_drift":
    IF drift_item.impact == "breaking":
      RETURN CRITICAL
    ELIF drift_item.impact == "significant":
      RETURN HIGH
    ELSE:
      RETURN MEDIUM
  
  RETURN LOW  # Default
```
```

**File**: `templates/shared/drift/code-analyzers.md` (NEW)

```markdown
# Language-Specific Code Analyzers

## TypeScript Analyzer

```text
ANALYZE_TYPESCRIPT(file_path):
  
  # Use Serena MCP tools
  symbols = find_symbol(name_path_pattern="*", relative_path=file_path)
  
  apis = []
  FOR symbol IN symbols:
    IF symbol.kind == FUNCTION OR symbol.kind == METHOD:
      IF symbol.visibility == "export":
        api = {
          signature: EXTRACT_SIGNATURE(symbol),
          file: file_path,
          line: symbol.location.start_line,
          annotations: EXTRACT_ANNOTATIONS(symbol.body)
        }
        apis.append(api)
  
  RETURN apis
```

## Python Analyzer

```text
ANALYZE_PYTHON(file_path):
  
  symbols = find_symbol(name_path_pattern="*", relative_path=file_path)
  
  apis = []
  FOR symbol IN symbols:
    IF symbol.kind == FUNCTION:
      # Check for FastAPI/Flask decorators
      decorators = EXTRACT_DECORATORS(symbol)
      IF decorators contains ["@app", "@router", "@bp.route"]:
        api = {
          signature: EXTRACT_SIGNATURE(symbol),
          route: EXTRACT_ROUTE(decorators),
          method: EXTRACT_METHOD(decorators),
          file: file_path,
          line: symbol.location.start_line
        }
        apis.append(api)
  
  RETURN apis
```
```

**File**: `templates/shared/drift/annotation-parser.md` (NEW)

```markdown
# Annotation Parser

## Purpose

Extract @speckit annotations from code comments.

## Supported Annotations

```text
ANNOTATION_PATTERNS = {
  "FR": r"@speckit:FR:(FR-\d+)",        # Functional requirement
  "TEST": r"\[TEST:(AS-\w+)\]",         # Test marker
  "COMP": r"\[COMP:(COMP-\d+)\]",       # Component marker
  "VR": r"\[VR:(VR-\d+)\]",             # Visual requirement
  "NFR": r"@speckit:NFR:(NFR-\w+-\d+)"  # Non-functional requirement
}
```

## Parsing Algorithm

```text
PARSE_ANNOTATIONS(file_content):
  
  annotations = []
  
  lines = file_content.split("\n")
  FOR i, line IN enumerate(lines):
    FOR annotation_type, pattern IN ANNOTATION_PATTERNS.items():
      matches = REGEX_FIND_ALL(pattern, line)
      FOR match IN matches:
        annotation = {
          type: annotation_type,
          id: match.group(1),
          line: i + 1,
          context: lines[i-1:i+3]  # 1 line before, 2 after
        }
        annotations.append(annotation)
  
  RETURN annotations
```
```

---

### 4. Update Documentation

**File**: `docs/COMMANDS_GUIDE.md`

Add new sections:

```markdown
### 9.5. `/speckit.analyze --profile drift` {#speckitanalyzedrift}

**Назначение:** Detect spec-code drift (Pass AA)

**Модель:** sonnet (thinking_budget: 24000)

**Флаги:**
- `--profile drift` — Run only Pass AA (drift detection)
- `--language <lang>` — Analyze specific language (ts/py/go/java)
- `--scope <path>` — Limit scope to specific directory

**Output:** drift-report.md in feature directory

**Handoffs:**
- → `/speckit.specify` (if spec needs update)
- → `/speckit.implement` (if code needs fixes)

---

### 18. `/speckit.reverse-engineer` {#speckitreverseengineer}

**Назначение:** Extract specifications from existing code

**Модель:** opus (thinking_budget: 32000)

**Флаги:**
- `--scope <path>` — Glob pattern for files to analyze
- `--force` — Overwrite existing extraction
- `--confidence-threshold <N>` — Minimum confidence (default: 0.70)
- `--skip-tests` — Don't analyze test files

**Output:** reverse-engineered/ directory with extracted-spec.md

**Handoffs:**
- → `/speckit.specify` (review and merge extraction)

**Workflow:**
1. Run reverse-engineer with scope
2. Review extracted-spec.md in reverse-engineered/
3. Cherry-pick valid requirements
4. Run /speckit.specify to merge into canonical spec
```

**File**: `CHANGELOG.md`

Add entry for new version:

```markdown
## [X.Y.Z] - 2026-01-XX

### Added
- **Spec-Code Drift Detection**: New Pass AA in `/speckit.analyze` detects when code diverges from spec (DRIFT-xxx items)
- **Reverse-Engineering**: New `/speckit.reverse-engineer` command extracts specs from existing code
- **Multi-language support**: TypeScript, Python, Go, Java/Kotlin code analysis
- **Quality Gate QG-DRIFT-001**: FR → Code coverage >= 80% gate
- **Drift report format**: drift-report.md with DRIFT-xxx items and severity levels
- **Extraction manifest**: .extraction-manifest.yaml tracks reverse-engineering metadata
- **Confidence scoring**: 0.0-1.0 confidence for extracted requirements
- **Hallucination detection**: Flags low-confidence items for manual review

### Changed
- Extended `templates/commands/analyze.md` with Pass AA (drift detection)
- Updated artifact registry schema to track drift reports
- Enhanced code analysis infrastructure with language-specific patterns

### Templates Added
- `templates/commands/reverse-engineer.md` - Reverse-engineering command
- `templates/shared/drift/drift-detection.md` - Drift detection framework
- `templates/shared/drift/code-analyzers.md` - Language-specific analyzers
- `templates/shared/drift/annotation-parser.md` - @speckit annotation parser
- `scripts/bash/reverse-engineer.sh` - Bash helper script
- `scripts/powershell/reverse-engineer.ps1` - PowerShell helper script
```

---

## Implementation Phases

### Wave 1: Foundation (Drift Detection Infrastructure)

**Duration**: 3-5 days  
**Priority**: P1

**Tasks**:
1. **T001**: Create `templates/shared/drift/drift-detection.md`
   - Define drift types, severity levels
   - Document detection patterns
   - [FR:ADR-001] Integration with analyze.md

2. **T002**: Create `templates/shared/drift/code-analyzers.md`
   - TypeScript analyzer with Serena MCP integration
   - Python analyzer
   - Go analyzer
   - Java/Kotlin analyzer
   - [FR:ADR-002] Hybrid AST+LLM approach

3. **T003**: Create `templates/shared/drift/annotation-parser.md`
   - @speckit:FR:, [TEST:AS-xxx], [COMP:COMP-xxx] patterns
   - Multi-language comment extraction
   - [FR:ADR-002]

4. **T004**: Update `.artifact-registry.yaml` schema
   - Add `drift_report` artifact type
   - Track drift item counts
   - Extend CASCADE_STALENESS logic
   - [FR:ADR-001]

**Dependencies**: None (foundation work)

**Validation**:
- All templates follow existing conventions
- Schema changes backward compatible
- Patterns tested against sample codebases

---

### Wave 2: Pass AA Implementation

**Duration**: 5-7 days  
**Priority**: P1

**Tasks**:
5. **T005**: Extend `templates/commands/analyze.md` with Pass AA
   - Add detection pass section (after Pass Y at ~line 2600)
   - Define DRIFT_DETECTION_ALGORITHM pseudocode
   - Add subagents: typescript-drift-detector, python-drift-detector, etc.
   - Add drift-report-compiler subagent
   - [FR:ADR-001]

6. **T006**: Create drift report output template
   - drift-report.md format with DRIFT-xxx items
   - Severity breakdown table
   - Actionable recommendations section
   - Traceability impact metrics
   - [FR:ADR-003] Function-level granularity

7. **T007**: Integrate with quality gates
   - Add QG-DRIFT-001 in `memory/domains/quality-gates.md`
   - Define FR → Code coverage threshold (80%)
   - Add to `--profile qa` validation
   - [FR:ADR-001]

8. **T008**: Add `--profile drift` support
   - Configure Pass AA execution
   - Set timeout (300s default)
   - Output mode: detailed
   - [FR:ADR-001]

**Dependencies**: Wave 1 (T001-T004)

**Validation**:
- Test Pass AA on sample TypeScript project
- Verify DRIFT-xxx items are actionable
- Confirm quality gate integration

---

### Wave 3: Reverse-Engineering Command

**Duration**: 7-10 days  
**Priority**: P1

**Tasks**:
9. **T009**: Create `templates/commands/reverse-engineer.md`
   - Command structure (YAML frontmatter)
   - Handoffs to /speckit.specify
   - Pre-gates (scope definition, directory check)
   - [FR:ADR-004] reverse-engineered/ directory

10. **T010**: Implement REVERSE_ENGINEER_ALGORITHM
    - 10-step algorithm pseudocode
    - Wave 1: Discovery (code-discoverer, annotation-extractor)
    - Wave 2: Structure (api-extractor, entity-extractor, test-analyzer)
    - Wave 3: Synthesis (requirement-synthesizer, scenario-synthesizer)
    - Wave 4: Reporting (spec-compiler, drift-comparator, manifest-generator)
    - [FR:ADR-002] Hybrid AST+LLM

11. **T011**: Create extraction templates
    - extracted-spec.md format (follows spec-template.md)
    - .extraction-manifest.yaml schema
    - extraction-log.md for reasoning trace
    - [FR:ADR-004]

12. **T012**: Implement confidence scoring
    - CALCULATE_ITEM_CONFIDENCE algorithm
    - 0.90-1.0: Explicit (has @speckit annotation)
    - 0.70-0.89: High (naming + tests + patterns)
    - 0.50-0.69: Medium (patterns only)
    - <0.50: Low (speculative, requires review)
    - [FR:ADR-003]

13. **T013**: Implement hallucination detection
    - DETECT_HALLUCINATIONS algorithm
    - Flag low-confidence items
    - Check for code evidence
    - Detect speculative language
    - [FR:ADR-003]

**Dependencies**: Wave 2 (T005-T008) for shared infrastructure

**Validation**:
- Extract spec from sample TypeScript project
- Verify confidence scores are reasonable
- Test hallucination detection accuracy

---

### Wave 4: Helper Scripts & Documentation

**Duration**: 2-3 days  
**Priority**: P2

**Tasks**:
14. **T014**: Create `scripts/bash/reverse-engineer.sh`
    - Prerequisites check
    - Directory creation
    - Scope validation
    - [FR:ADR-004]

15. **T015**: Create `scripts/powershell/reverse-engineer.ps1`
    - PowerShell equivalent
    - Windows compatibility
    - [FR:ADR-004]

16. **T016**: Update `docs/COMMANDS_GUIDE.md`
    - Section 9.5: /speckit.analyze --profile drift
    - Section 18: /speckit.reverse-engineer
    - Add workflow examples
    - Document flags
    - [FR:Documentation]

17. **T017**: Update `CHANGELOG.md`
    - Add entry for version X.Y.Z
    - List all new features
    - Document breaking changes (none expected)
    - [FR:Documentation]

**Dependencies**: Wave 3 (T009-T013)

**Validation**:
- Scripts work on macOS, Linux, Windows
- Documentation is clear and complete
- Examples are accurate

---

### Wave 5: Testing & Polish

**Duration**: 3-5 days  
**Priority**: P1

**Tasks**:
18. **T018**: Create test fixtures
    - Sample TypeScript project with drift
    - Sample Python project for reverse-engineering
    - Expected drift-report.md outputs
    - Expected extracted-spec.md outputs
    - [TEST:Integration]

19. **T019**: Manual testing
    - Run Pass AA on Spec Kit itself (dogfooding)
    - Run reverse-engineer on existing project
    - Verify output quality
    - Test edge cases (empty scope, no annotations)
    - [TEST:Manual]

20. **T020**: Performance optimization
    - Profile Pass AA execution time
    - Optimize Serena MCP tool usage
    - Add caching for repeated analyses
    - [NFR:Performance]

21. **T021**: Error handling
    - Graceful failure for unsupported languages
    - Timeout handling for large codebases
    - User-friendly error messages
    - [FR:Reliability]

22. **T022**: Self-review
    - Run /speckit.analyze on this plan
    - Verify traceability (all ADR → Tasks)
    - Check quality metrics
    - [QA:Self-Review]

**Dependencies**: Wave 4 (T014-T017)

**Validation**:
- All tests pass
- Performance acceptable (<5 min for medium project)
- Error messages are helpful

---

## Quality Gates

### QG-DRIFT-001: Spec-Code Alignment

**Level**: MUST (for production)  
**Threshold**: FR → Code coverage >= 80%  
**Validation**: `/speckit.analyze --profile drift`  
**Severity**: HIGH  

**Pass Criteria**:
- At least 80% of spec FR-xxx have @speckit:FR: in code
- No CRITICAL drift items
- < 5 HIGH drift items

**Fail Actions**:
- Block merge until drift resolved
- Require spec update or code annotation
- Document exceptions in drift-report.md

---

### QG-EXTRACT-001: Extraction Quality

**Level**: SHOULD (for reverse-engineering)  
**Threshold**: Average confidence >= 0.70  
**Validation**: Check .extraction-manifest.yaml  
**Severity**: MEDIUM  

**Pass Criteria**:
- Average confidence >= 0.70
- < 20% low-confidence items
- < 5 hallucination flags

**Fail Actions**:
- Warn user about low quality
- Recommend narrower scope
- Suggest adding @speckit annotations first

---

## Testing Strategy

### Unit Tests
- Annotation parser on sample code snippets
- Confidence scoring algorithm
- Severity calculation logic
- Drift item deduplication

### Integration Tests
- Pass AA on sample TypeScript project
- Reverse-engineer on sample Python project
- Full workflow: extract → review → merge

### E2E Tests
- Dogfooding: Run on Spec Kit itself
- Brownfield test: Extract spec from legacy project
- Validation: Compare extracted vs manual spec

### Performance Tests
- Pass AA on large codebase (>1000 files)
- Target: <5 minutes for medium project
- Parallel agent execution optimization

---

## Migration Path

### For Existing Projects

#### Without @speckit annotations

**Before**:
```typescript
// src/api/users.ts
export async function createUser(data: CreateUserDto) {
  // Implementation
}
```

**Migration Step 1**: Run drift detection
```bash
/speckit.analyze --profile drift
# Output: DRIFT-001: Undocumented API createUser (HIGH)
```

**Migration Step 2**: Add annotations
```typescript
// @speckit:FR:FR-003 User registration API
export async function createUser(data: CreateUserDto) {
  // Implementation
}
```

**Migration Step 3**: Re-validate
```bash
/speckit.analyze --profile drift
# Output: No drift detected, FR → Code coverage: 100%
```

---

#### With Missing Spec

**Scenario**: Legacy codebase, no spec.md

**Migration Step 1**: Run reverse-engineering
```bash
/speckit.reverse-engineer --scope "src/users/**/*.ts"
# Output: reverse-engineered/extracted-spec.md
```

**Migration Step 2**: Review extraction
- Check confidence scores
- Verify extracted FR-xxx match business intent
- Flag hallucinations for removal

**Migration Step 3**: Create canonical spec
```bash
# Manually copy verified FRs to spec.md
# Or use /speckit.specify with extraction as input
```

**Migration Step 4**: Add annotations
```typescript
// @speckit:FR:FR-001 (from extracted-spec.md)
export async function createUser(data: CreateUserDto) {
```

---

### Backward Compatibility

**Guarantees**:
- ✅ Existing specs without drift detection still work
- ✅ Artifact registry schema is backward compatible
- ✅ New Pass AA is opt-in (via `--profile drift`)
- ✅ No breaking changes to existing commands

**Opt-In Flags**:
- Use `--profile qa` to include drift in post-implement QA
- Use `--profile drift` for standalone drift detection
- Default analyze behavior unchanged (no drift check)

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LLM hallucinations in extraction | HIGH | MEDIUM | Confidence scoring, manual review, hallucination detection |
| Performance issues on large codebases | MEDIUM | HIGH | Parallel agents, caching, scope limits |
| Serena MCP tool limitations | MEDIUM | MEDIUM | Fallback to AST-only mode, error handling |
| Language-specific edge cases | HIGH | LOW | Iterative pattern refinement, community feedback |

### Process Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Users trust low-confidence extraction | MEDIUM | HIGH | Prominent warnings, confidence thresholds, gating |
| Drift reports too noisy | MEDIUM | MEDIUM | Severity levels, filtering, actionable recommendations |
| Adoption friction (annotation overhead) | MEDIUM | LOW | Tooling support, auto-annotation suggestions |

---

## Success Metrics

### Quantitative

1. **Drift Detection Accuracy**: >= 90%
   - True positives: Correctly identified drift
   - False positives: < 10% of reported items

2. **Extraction Quality**: >= 75% average confidence
   - High confidence (>= 0.90): >= 50%
   - Low confidence (< 0.50): < 20%

3. **Performance**: < 5 minutes for medium project
   - Medium project: 50 files, 5000 LOC
   - Large project: 500 files, 50000 LOC (< 30 min)

4. **Coverage**: >= 80% FR → Code after annotation
   - Baseline: Measure current projects
   - Target: 80% within 1 month of adoption

### Qualitative

1. **User Satisfaction**: >= 4/5 stars
   - Survey: "How helpful was drift detection?"
   - Feedback: "How accurate was reverse-engineering?"

2. **Adoption Rate**: >= 50% of active projects
   - Track `/speckit.analyze --profile drift` usage
   - Track `/speckit.reverse-engineer` invocations

3. **Documentation Quality**: Zero critical gaps
   - All commands documented in COMMANDS_GUIDE.md
   - All patterns documented in templates/shared/drift/

---

## Critical Files for Implementation

Based on this design, the 5 most critical files are:

### 1. `templates/commands/analyze.md`
**Reason**: Core drift detection logic (Pass AA)  
**Changes**: Add ~500 lines for Pass AA detection algorithm, subagents, output format  
**Complexity**: HIGH - Extends existing 3000-line file with new detection pass  
**Dependencies**: Must integrate with existing Pass Y (code-spec drift baseline)

### 2. `templates/commands/reverse-engineer.md`
**Reason**: Entirely new command for spec extraction  
**Changes**: Create ~800-line new command file from scratch  
**Complexity**: HIGH - Most complex new command with 9 subagents across 4 waves  
**Dependencies**: Requires Serena MCP tools, Task agent orchestration

### 3. `templates/shared/drift/drift-detection.md`
**Reason**: Shared framework for both features  
**Changes**: Create ~400-line new template defining drift types, patterns, algorithms  
**Complexity**: MEDIUM - Foundation for both drift detection and reverse-engineering  
**Dependencies**: None - standalone framework

### 4. `templates/shared/drift/code-analyzers.md`
**Reason**: Language-specific analysis patterns  
**Changes**: Create ~600-line new template with TypeScript, Python, Go, Java patterns  
**Complexity**: HIGH - Must handle 4 languages with different syntax, tooling  
**Dependencies**: Serena MCP tools (find_symbol, search_for_pattern, get_symbols_overview)

### 5. `memory/domains/quality-gates.md`
**Reason**: New quality gate QG-DRIFT-001  
**Changes**: Add ~150 lines for QG-DRIFT-001 definition, validation, enforcement  
**Complexity**: MEDIUM - Extends existing quality gate system  
**Dependencies**: Pass AA must provide data for gate validation

---

## Appendix: Example Workflows

### Workflow 1: Post-Implementation Drift Check

```bash
# After implementing feature
cd specs/042-user-management/

# Run QA validation (includes drift check)
/speckit.analyze --profile qa

# Output: drift-report.md
# DRIFT-001: Undocumented API POST /api/v1/users/:id/archive (CRITICAL)
# DRIFT-002: FR-007 not implemented (HIGH)

# Fix drift
# 1. Add undocumented API to spec.md
# 2. Implement FR-007
# 3. Re-validate

/speckit.analyze --profile drift
# Output: No drift detected ✅
```

### Workflow 2: Reverse-Engineering Legacy Project

```bash
# Start with existing codebase, no spec
cd my-legacy-project/
specify init feature brownfield-users --ai claude

# Run reverse-engineering
cd specs/brownfield-users/
/speckit.reverse-engineer --scope "src/users/**/*.ts"

# Review extraction
cat reverse-engineered/extracted-spec.md
# 15 FRs extracted (confidence: 0.82 avg)
# 2 low-confidence items flagged for review

# Manually review and approve
# Edit extracted-spec.md to remove hallucinations

# Merge into canonical spec
/speckit.specify --merge-from reverse-engineered/extracted-spec.md

# Add annotations to code
# @speckit:FR:FR-001
# @speckit:FR:FR-002

# Validate alignment
/speckit.analyze --profile drift
# Output: FR → Code coverage: 95% ✅
```

### Workflow 3: Continuous Drift Monitoring

```bash
# In CI/CD pipeline (.github/workflows/drift-check.yml)

name: Spec-Code Drift Check

on:
  pull_request:
    branches: [main]

jobs:
  drift-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Drift Detection
        run: |
          /speckit.analyze --profile drift
      
      - name: Check Drift Report
        run: |
          if grep -q "CRITICAL\|HIGH" specs/*/drift-report.md; then
            echo "Drift detected - blocking PR"
            exit 1
          fi
      
      - name: Upload Drift Report
        uses: actions/upload-artifact@v3
        with:
          name: drift-report
          path: specs/*/drift-report.md
```

---

**End of Architecture Design**

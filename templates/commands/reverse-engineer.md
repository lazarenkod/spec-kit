---
description: |
  Extract specifications from existing codebase using LLM-powered analysis.
  Creates reverse-engineered/ directory with extracted-spec.md for review.

  **Use Cases**:
  - Legacy codebases without documentation
  - Brownfield projects needing spec baseline
  - Post-implementation validation (compare extracted vs canonical spec)
  - Documentation generation from code

  **Output**: Isolated reverse-engineered/ directory containing:
  - extracted-spec.md (LLM-synthesized spec following spec-template.md)
  - drift-report.md (comparison with canonical spec.md if exists)
  - .extraction-manifest.yaml (metadata, confidence scores, coverage stats)
  - extraction-log.md (agent reasoning trace for debugging)

persona: documentation-agent

handoffs:
  - label: Review Extracted Spec
    agent: speckit.specify
    prompt: Review extracted-spec.md and merge verified FRs into canonical spec.md
    auto: false
    condition:
      - "Extraction completed successfully"
      - "Average confidence >= 0.70"
    gates:
      - name: "Extraction Quality Gate"
        check: "Extracted spec has >= 5 FR-xxx"
        block_if: "Extracted FRs < 5"
        message: "Extraction produced too few requirements - verify scan scope"
      - name: "Hallucination Check Gate"
        check: "Average confidence >= 0.70"
        block_if: "Average confidence < 0.70"
        message: "Low confidence scores suggest hallucinations - manual review required"
      - name: "Extraction Completeness Gate"
        check: "Discovered APIs > 0 AND Analyzed symbols > 0"
        block_if: "No APIs or symbols discovered"
        message: "Extraction found no code to analyze - check scan scope and language support"
    post_actions:
      - "log: Extraction complete with {extracted_frs} FRs (avg confidence: {avg_confidence})"
  - label: Apply Extracted Spec
    agent: speckit.fix
    prompt: Apply extracted spec using regenerate strategy to merge into canonical spec.md
    auto: false
    condition:
      - "Extraction completed successfully"
      - "User wants to apply extracted spec to canonical artifacts"
    post_actions:
      - "log: Consider running /speckit.fix --strategy regenerate to merge extracted spec"

pre_gates:
  - name: "Scope Definition Gate"
    check: "User provided scan scope (--scope flag or interactive prompt)"
    block_if: "No scope defined"
    message: "Scan scope required - specify file patterns (e.g., src/**/*.ts)"
  - name: "No Existing Extraction Gate"
    check: "reverse-engineered/ directory does not exist"
    block_if: "reverse-engineered/ exists"
    message: "Existing extraction found - delete reverse-engineered/ or use --force to overwrite"
  - name: "Code Exists Gate"
    check: "At least one code directory exists (src/, app/, lib/)"
    block_if: "No code directories found"
    message: "No code to analyze - verify working directory"

claude_code:
  model: sonnet
  reasoning_mode: extended

  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 2000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 4000
        max_parallel: 3
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 2000
        max_parallel: 6
        batch_delay: 1500
        wave_overlap_threshold: 0.65
      ultrathink:
        thinking_budget: 8000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 4.0

  depth_defaults:
    standard:
      thinking_budget: 2000
      timeout: 30
    ultrathink:
      thinking_budget: 8000
      additional_analysis: [confidence-validator, hallucination-detector]
      timeout: 60

  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 2000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (8K thinking budget).
          Auto-downgrading to **Standard** mode (2K budget).

  cost_breakdown:
    standard: {cost: $0.03, time: "15-30s"}
    ultrathink: {cost: $0.12, time: "30-60s"}

  orchestration:
    max_parallel: 8
    wave_overlap:
      enabled: true
      threshold: 0.75
    retry:
      max_attempts: 2
      backoff: exponential

  subagents:
    # ====================================================================
    # WAVE 1: DISCOVERY (Parallel - Priority 10)
    # ====================================================================
    - role: code-discoverer
      priority: 10
      model: haiku
      description: "Discover files in scan scope using Serena list_dir, find_file"
      depends_on: []
      tools: [list_dir, find_file, search_for_pattern]
      prompt: |
        Discover all files matching scan scope patterns.

        INPUT:
        - scan_scope.patterns: {patterns}
        - scan_scope.exclude: {exclude}

        ALGORITHM:
        1. Expand glob patterns to file list
        2. Apply exclusions (node_modules/, dist/, etc.)
        3. Group by language (TypeScript, Python, Go, Java/Kotlin)
        4. Identify framework (Express, FastAPI, Spring, etc.)

        OUTPUT:
        discovered_files = {
          typescript: [file1.ts, file2.tsx, ...],
          python: [file1.py, file2.py, ...],
          go: [file1.go, file2.go, ...],
          java: [file1.java, file2.kt, ...]
        }
        detected_frameworks = ["express", "react"]

    - role: annotation-extractor
      priority: 10
      model: haiku
      description: "Extract existing @speckit annotations using search_for_pattern"
      depends_on: []
      tools: [search_for_pattern]
      prompt: |
        Extract all existing @speckit annotations from codebase.

        Read `templates/shared/drift/annotation-parser.md`

        PATTERNS:
        - @speckit:FR:(FR-\d+)
        - @speckit:AS:(AS-\w+)
        - [TEST:(AS-\w+)]
        - [COMP:(COMP-\d+)]
        - @internal

        OUTPUT:
        existing_annotations = {
          FR: [{id: "FR-001", file: "src/api.ts", line: 42}, ...],
          AS: [{id: "AS-1A", file: "tests/auth.test.ts", line: 15}, ...],
          COMP: [...],
          TEST: [...],
          INTERNAL: [{file: "src/utils.ts", line: 99}, ...]
        }

    # ====================================================================
    # WAVE 2: STRUCTURE ANALYSIS (Parallel - Priority 20)
    # ====================================================================
    - role: api-extractor
      priority: 20
      model: sonnet
      description: "Extract public APIs using Serena find_symbol"
      depends_on: [code-discoverer]
      tools: [find_symbol, read_file]
      prompt: |
        Extract public API endpoints and exported functions.

        Read `templates/shared/drift/code-analyzers.md`

        INPUT: discovered_files from code-discoverer

        ALGORITHM (per language):

        TypeScript:
          symbols = find_symbol("*", file, include_kinds=[12, 6])  # Function, Method
          FOR symbol IN symbols:
            IF "export" IN symbol.body:
              api = {
                type: DETECT_API_TYPE(symbol),  # REST_API, FUNCTION, CLASS_METHOD
                signature: PARSE_SIGNATURE(symbol),
                visibility: "public",
                file: file,
                line: symbol.line,
                annotations: EXTRACT_LOCAL_ANNOTATIONS(symbol.body),
                framework: DETECT_FRAMEWORK(symbol)  # Express, NestJS, Next.js
              }
              apis.append(api)

        Python:
          # FastAPI: @app.(get|post|put|delete)
          # Flask: @app.route
          # Django: HttpRequest views

        Go:
          # Exported = capitalized first letter
          # Gin, Echo, Chi routers

        Java/Kotlin:
          # Spring: @GetMapping, @PostMapping
          # JAX-RS: @GET, @POST, @Path

        OUTPUT:
        apis = [
          {
            type: "REST_API",
            method: "POST",
            endpoint: "/api/v1/users",
            signature: "async function createUser(data: UserData)",
            file: "src/api/users.ts",
            line: 42,
            annotations: {FR: ["FR-001"]},
            framework: "express"
          },
          ...
        ]

    - role: entity-extractor
      priority: 20
      model: sonnet
      description: "Extract domain entities (classes, models, interfaces)"
      depends_on: [code-discoverer]
      tools: [find_symbol, read_file]
      prompt: |
        Extract domain entities representing business concepts.

        INPUT: discovered_files from code-discoverer

        ALGORITHM:
        symbols = find_symbol("*", file, include_kinds=[5, 4])  # Class, Interface

        FOR symbol IN symbols:
          entity = {
            name: symbol.name,
            type: symbol.kind,  # class, interface, type, model
            properties: PARSE_PROPERTIES(symbol.body),
            methods: PARSE_METHODS(symbol.body),
            file: file,
            line: symbol.line,
            annotations: EXTRACT_LOCAL_ANNOTATIONS(symbol.body)
          }

          # Infer entity purpose from naming
          IF symbol.name.endswith("Request") OR symbol.name.endswith("DTO"):
            entity.purpose = "data_transfer"
          ELIF symbol.name.endswith("Model") OR symbol.name.endswith("Entity"):
            entity.purpose = "domain_model"
          ELIF symbol.name.endswith("Service"):
            entity.purpose = "business_logic"

          entities.append(entity)

        OUTPUT:
        entities = [
          {
            name: "User",
            type: "interface",
            properties: ["id: string", "email: string", "password: string"],
            methods: [],
            file: "src/models/user.ts",
            line: 15,
            purpose: "domain_model"
          },
          ...
        ]

    - role: test-analyzer
      priority: 20
      model: sonnet
      description: "Parse test files to extract acceptance scenarios"
      depends_on: [code-discoverer]
      tools: [read_file, search_for_pattern]
      prompt: |
        Analyze test files to extract acceptance scenarios.

        INPUT: discovered_files.tests (*.test.*, *.spec.*)

        ALGORITHM:
        FOR test_file IN test_files:
          content = read_file(test_file)

          # Extract test structure
          test_suites = PARSE_TEST_SUITES(content)  # describe(), test(), it()

          FOR suite IN test_suites:
            FOR test_case IN suite.tests:
              scenario = {
                id: INFER_AS_ID(test_case.name),  # "should create user" → AS-xxx
                description: test_case.name,
                file: test_file,
                line: test_case.line,
                assertions: EXTRACT_ASSERTIONS(test_case.body),
                confidence: CALCULATE_TEST_CONFIDENCE(test_case)
              }

              # Convert to Gherkin if possible
              gherkin = CONVERT_TO_GHERKIN(test_case)
              scenario.gherkin = gherkin

              scenarios.append(scenario)

        OUTPUT:
        scenarios = [
          {
            id: "AS-1A",
            description: "should create user with valid data",
            file: "tests/auth.test.ts",
            line: 42,
            gherkin: {
              given: "valid user data",
              when: "POST /api/v1/users",
              then: "returns 201 with user object"
            },
            confidence: 0.85
          },
          ...
        ]

    # ====================================================================
    # WAVE 3: LLM SYNTHESIS (Sequential - Priority 30)
    # ====================================================================
    - role: requirement-synthesizer
      priority: 30
      model: sonnet
      description: "Synthesize FR-xxx from APIs and entities with confidence scoring"
      depends_on: [api-extractor, entity-extractor, annotation-extractor]
      tools: []
      prompt: |
        Synthesize functional requirements from discovered code patterns.

        Read `templates/shared/drift/drift-detection.md`

        INPUT:
        - apis from api-extractor
        - entities from entity-extractor
        - existing_annotations from annotation-extractor

        ALGORITHM:
        extracted_frs = []

        # Priority 1: Explicit annotations (highest confidence)
        FOR annotation IN existing_annotations.FR:
          IF annotation.id NOT IN extracted_frs:
            fr = {
              id: annotation.id,
              description: INFER_FROM_CODE_CONTEXT(annotation),
              source: "explicit_annotation",
              confidence: 0.95,
              file: annotation.file,
              line: annotation.line
            }
            extracted_frs.append(fr)

        # Priority 2: Public APIs with clear intent
        FOR api IN apis:
          IF api.annotations.FR:
            CONTINUE  # Already covered by explicit annotations

          # Infer business intent from API signature
          intent = INFER_BUSINESS_INTENT(
            signature=api.signature,
            endpoint=api.endpoint,
            method=api.method,
            naming=api.name,
            context=api.file
          )

          fr = {
            id: GENERATE_FR_ID(extracted_frs),  # FR-001, FR-002, ...
            description: intent,
            source: "api_inference",
            confidence: CALCULATE_CONFIDENCE(api),
            file: api.file,
            line: api.line,
            api_signature: api.signature
          }

          extracted_frs.append(fr)

        # Priority 3: Domain entities suggesting CRUD operations
        FOR entity IN entities:
          IF entity.purpose == "domain_model":
            # Infer CRUD requirements
            crud_frs = INFER_CRUD_REQUIREMENTS(entity)
            FOR crud_fr IN crud_frs:
              IF NOT EXISTS_SIMILAR_FR(extracted_frs, crud_fr):
                crud_fr.source = "entity_inference"
                crud_fr.confidence = 0.65
                extracted_frs.append(crud_fr)

        OUTPUT:
        extracted_frs = [
          {
            id: "FR-001",
            description: "User can create an account with email and password",
            source: "api_inference",
            confidence: 0.82,
            file: "src/api/auth.ts",
            line: 42,
            api_signature: "async function register(data: RegisterRequest)"
          },
          ...
        ]

        # CONFIDENCE SCORING FORMULA:
        # score = 0.0
        # + 0.50 if has_@speckit_annotation
        # + 0.20 if has_test_coverage (0.10 if partial)
        # + 0.15 * naming_clarity (LLM evaluated 0.0-1.0)
        # + 0.10 if has_docstring (0.05 if inline comments)
        # + 0.05 if matches_known_pattern (REST CRUD, auth, etc.)
        # RETURN min(score, 1.0)

    - role: scenario-synthesizer
      priority: 30
      model: sonnet
      description: "Convert test cases to Gherkin AS-xxx scenarios"
      depends_on: [test-analyzer, requirement-synthesizer]
      tools: []
      prompt: |
        Convert test cases to acceptance scenarios in Gherkin format.

        INPUT:
        - scenarios from test-analyzer
        - extracted_frs from requirement-synthesizer

        ALGORITHM:
        extracted_ass = []

        FOR scenario IN scenarios:
          # Map scenario to FR
          mapped_fr = FIND_RELATED_FR(scenario, extracted_frs)

          # Convert to Gherkin
          as = {
            id: scenario.id OR GENERATE_AS_ID(extracted_ass),
            fr_ids: [mapped_fr.id] IF mapped_fr ELSE [],
            title: scenario.description,
            gherkin: scenario.gherkin OR SYNTHESIZE_GHERKIN(scenario),
            confidence: scenario.confidence,
            source: "test_conversion",
            file: scenario.file,
            line: scenario.line
          }

          extracted_ass.append(as)

        OUTPUT:
        extracted_ass = [
          {
            id: "AS-1A",
            fr_ids: ["FR-001"],
            title: "User registration with valid data",
            gherkin: {
              given: "valid user registration data (email, password)",
              when: "user submits registration form",
              then: "account is created and confirmation email sent"
            },
            confidence: 0.85,
            source: "test_conversion",
            file: "tests/auth.test.ts",
            line: 42
          },
          ...
        ]

    # ====================================================================
    # WAVE 4: REPORTING (Sequential - Priority 40)
    # ====================================================================
    - role: spec-compiler
      priority: 40
      model: sonnet
      description: "Compile extracted-spec.md following spec-template.md"
      depends_on: [requirement-synthesizer, scenario-synthesizer]
      tools: [read_file]
      prompt: |
        Compile extracted requirements into spec-template.md format.

        INPUT:
        - extracted_frs from requirement-synthesizer
        - extracted_ass from scenario-synthesizer

        ALGORITHM:
        1. Read `templates/spec-template.md` for structure
        2. Populate template sections:
           - Feature Description: Synthesize from top FRs
           - User Stories: Group FRs by user goal
           - Functional Requirements: Insert extracted FRs with confidence annotations
           - Acceptance Scenarios: Insert extracted AS with Gherkin
        3. Add confidence metadata to each FR/AS as comment
        4. Flag low-confidence items (< 0.70) for review

        OUTPUT:
        extracted_spec_content = """
        # Feature Specification: {feature_name}

        **Status**: EXTRACTED (reverse-engineered)
        **Extraction Date**: {ISO_DATE}
        **Average Confidence**: {avg_confidence}

        ## Feature Description

        {synthesized_description}

        ## User Stories

        {synthesized_stories}

        ## Functional Requirements

        ### FR-001: User Registration
        <!-- Confidence: 0.82 | Source: api_inference | File: src/api/auth.ts:42 -->
        User can create an account with email and password.

        **API**: `async function register(data: RegisterRequest)`

        ...

        ## Acceptance Scenarios

        ### AS-1A: User registration with valid data
        <!-- Confidence: 0.85 | Source: test_conversion | File: tests/auth.test.ts:42 -->

        **Given** valid user registration data (email, password)
        **When** user submits registration form
        **Then** account is created and confirmation email sent

        **Mapped FRs**: FR-001

        ...
        """

        WRITE(reverse-engineered/extracted-spec.md, extracted_spec_content)

    - role: drift-comparator
      priority: 40
      model: sonnet
      description: "Compare extracted spec with canonical spec.md if exists"
      depends_on: [spec-compiler]
      tools: [read_file]
      prompt: |
        Compare extracted-spec.md with canonical spec.md (if exists).

        INPUT:
        - extracted_spec_content from spec-compiler
        - canonical_spec_content (if exists)

        ALGORITHM:
        IF NOT exists(spec.md):
          drift_report = {
            mode: "no_canonical",
            message: "No canonical spec.md - extracted spec is baseline"
          }
          RETURN drift_report

        canonical_spec = READ(spec.md)

        # Compare requirements
        canonical_frs = EXTRACT_FRS(canonical_spec)
        extracted_frs = EXTRACT_FRS(extracted_spec)

        drift = {
          only_in_canonical: [],
          only_in_extracted: [],
          common: [],
          semantic_differences: []
        }

        FOR fr IN canonical_frs:
          match = FIND_SIMILAR_FR(fr, extracted_frs, threshold=0.80)
          IF NOT match:
            drift.only_in_canonical.append(fr)
          ELSE:
            semantic_diff = LLM_COMPARE_SEMANTICS(fr, match)
            IF semantic_diff.score < 0.90:
              drift.semantic_differences.append({
                canonical: fr,
                extracted: match,
                diff: semantic_diff
              })
            drift.common.append({canonical: fr, extracted: match})

        FOR fr IN extracted_frs:
          IF fr NOT IN drift.common AND fr NOT IN drift.semantic_differences:
            drift.only_in_extracted.append(fr)

        OUTPUT:
        drift_report = {
          mode: "comparison",
          canonical_frs: canonical_frs.length,
          extracted_frs: extracted_frs.length,
          common: drift.common.length,
          only_in_canonical: drift.only_in_canonical,
          only_in_extracted: drift.only_in_extracted,
          semantic_differences: drift.semantic_differences
        }

        WRITE(reverse-engineered/drift-report.md, RENDER_DRIFT_REPORT(drift))

    - role: manifest-generator
      priority: 50
      model: haiku
      description: "Generate .extraction-manifest.yaml with metadata"
      depends_on: [spec-compiler, drift-comparator]
      tools: []
      prompt: |
        Generate extraction manifest with metadata and statistics.

        INPUT:
        - All wave outputs
        - extracted_spec_content
        - drift_report

        ALGORITHM:
        manifest = {
          version: "1.0",
          extracted_at: NOW(),
          extracted_by: "/speckit.reverse-engineer",
          scan_scope: {
            patterns: scan_scope.patterns,
            exclude: scan_scope.exclude
          },
          baseline: {
            spec_version: canonical_spec.version IF exists ELSE null,
            spec_checksum: CHECKSUM(spec.md) IF exists ELSE null
          },
          extraction_results: {
            discovered_files: discovered_files.length,
            analyzed_symbols: total_symbols,
            extracted_requirements: {
              total: extracted_frs.length,
              by_confidence: {
                explicit: COUNT(extracted_frs, confidence >= 0.90),
                high: COUNT(extracted_frs, confidence >= 0.70 AND < 0.90),
                medium: COUNT(extracted_frs, confidence >= 0.50 AND < 0.70),
                low: COUNT(extracted_frs, confidence < 0.50)
              }
            },
            extracted_scenarios: extracted_ass.length
          },
          drift_summary: {
            spec_to_code: {
              missing_in_code: drift.only_in_canonical.length
            },
            code_to_spec: {
              missing_in_spec: drift.only_in_extracted.length
            }
          },
          confidence_stats: {
            average: AVG(fr.confidence for fr in extracted_frs),
            median: MEDIAN(fr.confidence for fr in extracted_frs),
            min: MIN(fr.confidence for fr in extracted_frs),
            max: MAX(fr.confidence for fr in extracted_frs)
          }
        }

        WRITE_YAML(reverse-engineered/.extraction-manifest.yaml, manifest)

flags:
  - name: --thinking-depth
    type: choice
    choices: [standard, ultrathink]
    default: standard
    description: |
      Thinking budget control:
      - standard: 2K budget, fast extraction (~$0.03) [RECOMMENDED]
      - ultrathink: 8K budget, deep analysis (~$0.12)
  max_model: "--max-model <opus|sonnet|haiku>"  # Override model cap
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

## Parallel Execution

{{include: shared/orchestration-instructions.md}}

Execute subagents defined in `claude_code.subagents` using parallel Task calls per wave.
Wave 1 and Wave 2 agents run in parallel within their wave.
Wave 3 and Wave 4 agents run sequentially (LLM synthesis requires context).

---

## Goal

Extract specifications from existing codebase through 4-wave analysis:
1. **Discovery**: Find code files and existing annotations
2. **Structure Analysis**: Extract APIs, entities, and tests
3. **LLM Synthesis**: Infer business requirements and scenarios
4. **Reporting**: Compile spec, compare with canonical, generate manifest

Output is isolated in `reverse-engineered/` directory for manual review before merging.

---

## Algorithm

### 0. Parse Arguments and Initialize

```text
PARSE_ARGUMENTS:
  --scope: Scan scope patterns (required)
    Example: "src/**/*.ts" OR "src/,tests/" OR "**/*.py"
  --exclude: Additional exclusions (optional)
    Default: node_modules/, dist/, build/, __pycache__/, venv/, .git/
  --language: Override language detection (optional)
    Values: typescript, python, go, java, kotlin
  --force: Overwrite existing reverse-engineered/ directory
  --confidence-threshold: Minimum confidence for inclusion (default: 0.50)

IF NOT --scope:
  PROMPT user: "Enter scan scope (e.g., src/**/*.ts): "

IF exists(reverse-engineered/) AND NOT --force:
  ERROR: "Existing extraction found - use --force to overwrite"

MKDIR reverse-engineered/
```

### 1. Execute Wave 1: Discovery (Parallel)

```text
Launch in parallel:
  Task #1: code-discoverer agent
  Task #2: annotation-extractor agent

WAIT for both to complete

discovered_files = Task #1 output
existing_annotations = Task #2 output

IF discovered_files.length == 0:
  ERROR: "No files found in scan scope - verify patterns"
```

### 2. Execute Wave 2: Structure Analysis (Parallel)

```text
Launch in parallel:
  Task #3: api-extractor agent (input: discovered_files)
  Task #4: entity-extractor agent (input: discovered_files)
  Task #5: test-analyzer agent (input: discovered_files)

WAIT for all to complete

apis = Task #3 output
entities = Task #4 output
scenarios = Task #5 output
```

### 3. Execute Wave 3: LLM Synthesis (Sequential)

```text
Task #6: requirement-synthesizer agent
  INPUT: apis, entities, existing_annotations
  OUTPUT: extracted_frs

Task #7: scenario-synthesizer agent
  INPUT: scenarios, extracted_frs
  OUTPUT: extracted_ass
```

### 4. Execute Wave 4: Reporting (Sequential)

```text
Task #8: spec-compiler agent
  INPUT: extracted_frs, extracted_ass
  OUTPUT: extracted-spec.md

Task #9: drift-comparator agent
  INPUT: extracted-spec.md, canonical spec.md (if exists)
  OUTPUT: drift-report.md

Task #10: manifest-generator agent
  INPUT: all wave outputs
  OUTPUT: .extraction-manifest.yaml
```

### 5. Generate Extraction Summary

```text
manifest = READ_YAML(reverse-engineered/.extraction-manifest.yaml)

OUTPUT: "## Reverse-Engineering Complete"
OUTPUT: ""
OUTPUT: "**Extracted**: {manifest.extraction_results.extracted_requirements.total} FRs, {manifest.extraction_results.extracted_scenarios} AS"
OUTPUT: "**Average Confidence**: {manifest.confidence_stats.average}"
OUTPUT: "**Scan Scope**: {manifest.scan_scope.patterns}"
OUTPUT: ""
OUTPUT: "| Confidence | Count | Percentage |"
OUTPUT: "|------------|-------|------------|"
OUTPUT: "| Explicit (0.90-1.00) | {manifest.extraction_results.extracted_requirements.by_confidence.explicit} | {%} |"
OUTPUT: "| High (0.70-0.89) | {manifest.extraction_results.extracted_requirements.by_confidence.high} | {%} |"
OUTPUT: "| Medium (0.50-0.69) | {manifest.extraction_results.extracted_requirements.by_confidence.medium} | {%} |"
OUTPUT: "| Low (0.00-0.49) | {manifest.extraction_results.extracted_requirements.by_confidence.low} | {%} |"
OUTPUT: ""

IF exists(spec.md):
  drift = READ(reverse-engineered/drift-report.md)
  OUTPUT: "**Drift Summary**:"
  OUTPUT: "- Only in canonical spec: {drift.only_in_canonical.length}"
  OUTPUT: "- Only in extracted spec: {drift.only_in_extracted.length}"
  OUTPUT: "- Common (verified): {drift.common.length}"
  OUTPUT: ""

OUTPUT: "**Output Directory**: reverse-engineered/"
OUTPUT: "- extracted-spec.md (review and merge verified FRs)"
OUTPUT: "- drift-report.md (comparison with canonical spec)"
OUTPUT: "- .extraction-manifest.yaml (metadata and confidence scores)"
OUTPUT: ""
OUTPUT: "**Next Steps**:"
OUTPUT: "1. Review extracted-spec.md for hallucinations"
OUTPUT: "2. Verify low-confidence items (< 0.70)"
OUTPUT: "3. Run /speckit.specify to merge verified FRs into canonical spec"
```

---

## Hallucination Detection

```text
DETECT_HALLUCINATIONS(extracted_frs):
  hallucinations = []

  FOR fr IN extracted_frs:
    IF fr.confidence < 0.50:
      hallucinations.append({
        fr: fr.id,
        reason: "Very low confidence - likely speculative",
        severity: "HIGH"
      })

    IF fr.source == "entity_inference" AND NOT HAS_SUPPORTING_CODE(fr):
      hallucinations.append({
        fr: fr.id,
        reason: "Inferred from entity but no actual usage found",
        severity: "MEDIUM"
      })

    # Check for over-specific details
    IF CONTAINS_NUMERIC_DETAILS(fr.description):
      hallucinations.append({
        fr: fr.id,
        reason: "Contains specific numbers not found in code",
        severity: "MEDIUM"
      })

    # Check for business logic assumptions
    IF CONTAINS_BUSINESS_RULES(fr.description) AND fr.confidence < 0.80:
      hallucinations.append({
        fr: fr.id,
        reason: "Business rule inferred without explicit code support",
        severity: "LOW"
      })

  IF hallucinations.length > 0:
    OUTPUT: "## Hallucination Warnings"
    FOR h IN hallucinations:
      OUTPUT: "- **{h.fr}** [{h.severity}]: {h.reason}"

  RETURN hallucinations
```

---

## Confidence Scoring Algorithm

```text
CALCULATE_CONFIDENCE(item):
  score = 0.0

  # 1. Explicit annotation (highest confidence)
  IF has_@speckit_annotation(item):
    score += 0.50

  # 2. Test coverage
  IF has_test_coverage(item):
    score += 0.20
  ELIF has_partial_test_coverage(item):
    score += 0.10

  # 3. Naming clarity (LLM evaluated)
  naming_clarity = LLM_EVAL_CLARITY(item.name, item.signature)
  score += naming_clarity * 0.15  # 0.0-0.15

  # 4. Documentation
  IF has_docstring(item):
    score += 0.10
  ELIF has_inline_comments(item):
    score += 0.05

  # 5. Pattern recognition
  IF matches_known_pattern(item):  # REST CRUD, auth flow, etc.
    score += 0.05

  RETURN min(score, 1.0)

EXAMPLES:
- Explicit @speckit:FR:FR-001 with tests and docs: 0.50 + 0.20 + 0.10 + 0.10 = 0.90 ✅
- Public API with clear naming, partial tests: 0.15 + 0.10 + 0.05 = 0.30 + pattern = 0.75 ✅
- Inferred CRUD from entity, no tests: 0.08 + 0.05 = 0.13 ❌ (likely hallucination)
```

---

## Operating Principles

### Quality Over Quantity

- Flag low-confidence FRs (< 0.70) for mandatory manual review
- Do not hallucinate business rules not evident in code
- Prefer under-extraction to over-extraction (precision > recall)

### Traceability

- Every extracted FR links to source code location
- Confidence score transparent in extracted-spec.md comments
- Extraction manifest provides full audit trail

### Isolation

- Output to reverse-engineered/ directory (not mixed with canonical spec)
- Prevents hallucinations from polluting canonical spec
- User controls merge process

---

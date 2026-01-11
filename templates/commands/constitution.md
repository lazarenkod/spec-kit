---
description: Create or update the project constitution with layered architecture support (base → domain → project layers).
handoffs:
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
  - label: Analyze Compliance
    agent: speckit.analyze
    prompt: Check artifacts for constitution compliance
scripts:
  sh: echo "Constitution management - no prerequisites required"
  ps: Write-Host "Constitution management - no prerequisites required"
claude_code:
  model: opus
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 8000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 16000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 32000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
  cache_hierarchy: full
  orchestration:
    max_parallel: 8
    fail_fast: true
    wave_overlap:
      enabled: true
      overlap_threshold: 0.65
  subagents:
    # Wave 0: Interactive Questionnaire (if no input)
    - role: questionnaire-agent
      role_group: DISCOVERY
      parallel: false
      depends_on: []
      priority: 5
      model_override: haiku
      prompt: |
        Check if $ARGUMENTS is empty or whitespace-only.
        If empty, ask user 3 questions using AskUserQuestion tool:
        1. Application type (Web/Mobile/API/CLI/Desktop/Other)
        2. Domain (SaaS/E-commerce/Fintech/Healthcare/Gaming/General/Other)
        3. Language (English/Russian/Other)
        Return structured answers for constitution generation.
        If $ARGUMENTS is NOT empty, skip and pass through to analysis.

    # Wave 1: Analysis (parallel, after questionnaire)
    - role: layer-analyzer
      role_group: ANALYSIS
      parallel: true
      depends_on: [questionnaire-agent]
      priority: 10
      model_override: haiku
      prompt: |
        Analyze existing constitution layers.
        Read /memory/constitution.base.md (always exists).
        Check if /memory/constitution.domain.md exists and identify domain.
        Read /memory/constitution.md (project layer).
        Report layer status and identify placeholder tokens.
        Output: layer analysis summary.

    - role: principle-extractor
      role_group: ANALYSIS
      parallel: true
      depends_on: [questionnaire-agent]
      priority: 10
      model_override: sonnet
      prompt: |
        Extract principles from repo context if user input incomplete.
        Scan README, docs/, prior constitution versions.
        Identify applicable domain from project type.
        Collect values for [ALL_CAPS_IDENTIFIER] placeholders.
        Suggest principle strengthenings based on project needs.
        Output: extracted values and recommendations.

    # Wave 2: Constitution Writing (after analysis)
    - role: constitution-writer
      role_group: DOCS
      parallel: true
      depends_on: [layer-analyzer, principle-extractor]
      priority: 20
      model_override: sonnet
      prompt: |
        Write or update constitution based on analysis.
        Apply inheritance rules: higher layers cannot weaken MUST.
        Fill placeholder tokens with extracted values.
        Handle domain selection, principle strengthening, or merge view.
        Validate: no unexplained brackets, version updated.
        Generate sync impact report as HTML comment.
        Output: updated /memory/constitution.md.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

## Phase 0: Interactive Questionnaire (if no arguments)

**IMPORTANT**: If `$ARGUMENTS` is empty or whitespace-only, you MUST ask the user 3 questions
to determine the project context before proceeding. Use the `AskUserQuestion` tool.

### Question 1: Application Type

Ask: "What type of application are you building?"

| Option | Description | Resulting Principles |
|--------|-------------|---------------------|
| Web Application | SPA, SSR, static site | DSS-001-003, SEC-001-008, WEB-001-004 |
| Mobile Application | iOS, Android, cross-platform | mobile.md principles, SEC, offline-first |
| API/Backend Service | REST, GraphQL, gRPC | API-001-006, SEC, REL-001-003 |
| CLI Tool | Command-line utility | CLI-001-003, minimal security |
| Desktop Application | Electron, native | DSS + SEC + desktop-specific |
| Other | (user describes) | Derive from description |

### Question 2: Domain

Ask: "What domain does your project belong to?"

| Option | Description | Domain File | Key Principles |
|--------|-------------|-------------|----------------|
| SaaS | Multi-tenant B2B platform | saas.md | Multi-tenancy, auth, billing, tenant isolation |
| E-commerce | Online store, marketplace | e-commerce.md | PCI-DSS, inventory, checkout, payments |
| Fintech | Payments, banking, trading | fintech.md | SOC2, audit trail, transaction safety |
| Healthcare | Patient data, HIPAA | healthcare.md | HIPAA, PHI protection, consent management |
| Gaming (PC/Console) | PC/console games, high-end | gaming.md | Frame rate, netcode, platform cert (TRC/TCR) |
| Gaming (Mobile) | Mobile games, F2P, casual | gaming.md + mobile.md | Battery, offline, app size, retention, IAP |
| General/Minimal | No specific domain | (none) | Base layer only |
| Other | (user describes) | Derive from description |

### Question 3: Language

Ask: "What language should be used for specifications and documentation?"

| Option | Code | Effect |
|--------|------|--------|
| English | `en` | All artifacts in English (default) |
| Russian | `ru` | All prose content in Russian |
| Other | (user specifies) | Validate against supported languages list |

### Question 2.5: Game Genre (if Gaming (Mobile) selected)

**Condition**: Only ask if Question 2 answer is "Gaming (Mobile)"

Ask: "What genre of mobile game are you building?"

| Option | Description | Session Length | D1/D7/D30 Targets | Monetization Model |
|--------|-------------|---------------|-------------------|-------------------|
| Hyper-casual | One-thumb, instant play | 3-5 min | 40% / 20% / 8% | Ads (rewarded video) |
| Casual | Puzzle, match-3, merge | 10-15 min | 45% / 25% / 12% | Hybrid (IAP + ads) |
| Mid-core | Strategy, RPG, card battler | 20-30 min | 55% / 35% / 18% | F2P + IAP (gacha, battle pass) |
| Core | MOBA, BR, FPS, MMORPG | 45-60 min | 65% / 45% / 25% | F2P + cosmetic IAP |
| Other | (user describes) | TBD | TBD | TBD |

**Auto-Tuning**: Genre selection auto-tunes:
- Performance targets (hyper-casual: 120fps, core: 60fps)
- Retention expectations (D1/D7/D30 benchmarks)
- Monetization defaults (ads vs IAP mix)
- Session design (short bursts vs long sessions)

**Stack Template**: Recommend `mobile-game.yaml` stack template
**Concept Sections**: Auto-include all 6 game-specific sections (economy, monetization, live ops, retention, genre, psychology)

### Question 4: Cross-Platform Framework (if Mobile selected)

**Condition**: Only ask if Question 1 answer is "Mobile Application"

Ask: "Are you using a cross-platform framework?"

| Option | Platform File | Integration Checklist | Key Principles |
|--------|---------------|----------------------|----------------|
| Kotlin Multiplatform (KMP) | `platforms/kmp.md` | `kmp-integration-checklist.md` | KMP-001 to KMP-008 |
| Flutter | `platforms/flutter.md` | `flutter-integration-checklist.md` | FLT-001 to FLT-008 |
| React Native | `platforms/react-native.md` | `rn-integration-checklist.md` | RN-001 to RN-009 |
| Native Only (no cross-platform) | (none) | Platform-specific native tasks | iOS/Android native principles |

**Platform Detection**: If `$ARGUMENTS` or codebase already indicates a platform, SKIP this question.
Use `templates/shared/platform-detection.md` algorithm to auto-detect from:
- build.gradle.kts (KMP)
- pubspec.yaml (Flutter)
- package.json with react-native (React Native)

### After Collecting Answers

1. **Map App Type → Principles**: Apply relevant principle sets based on application type
2. **Map Domain → Domain Layer**: Copy appropriate domain file to `constitution.domain.md`
3. **Map Platform → Platform Layer**: If mobile + cross-platform, copy platform file to `constitution.platform.md`
4. **Set Language**: Update Project Settings table with language preference
5. **Generate Constitution**: Merge all layers and generate complete constitution

**Example Flow (Web)**:
```text
User runs: /speckit.constitution
(No arguments provided)

AI asks Question 1 → User selects "Web Application"
AI asks Question 2 → User selects "SaaS"
AI asks Question 3 → User selects "Russian"
(Question 4 skipped - not mobile)

AI then:
1. Copies memory/domains/saas.md → memory/constitution.domain.md
2. Adds WEB-001-004 principles to project layer
3. Sets language = "ru" in Project Settings
4. Generates complete constitution with SYNC REPORT
```

**Example Flow (Mobile + KMP)**:
```text
User runs: /speckit.constitution
(No arguments provided)

AI asks Question 1 → User selects "Mobile Application"
AI asks Question 2 → User selects "General/Minimal"
AI asks Question 3 → User selects "English"
AI asks Question 4 → User selects "Kotlin Multiplatform (KMP)"

AI then:
1. Copies memory/platforms/kmp.md → memory/constitution.platform.md
2. Adds KMP-001-008 principles to project layer
3. Sets language = "en" in Project Settings
4. Generates complete constitution with SYNC REPORT
5. Integration tasks will be auto-injected by /speckit.tasks
```

---

## Layered Constitution Architecture

The constitution uses a 4-layer inheritance model:

```text
Layer 0: /memory/constitution.base.md ───── Enterprise defaults (READ-ONLY)
    ↓ inherits
Layer 1: /memory/constitution.domain.md ─── Domain-specific (fintech, healthcare, etc.)
    ↓ inherits
Layer 2: /memory/constitution.platform.md ─ Platform-specific (KMP, Flutter, RN)
    ↓ inherits
Layer 3: /memory/constitution.md ─────────── Project overrides
```

**Inheritance Rules**:
- Higher layers INHERIT all principles from lower layers
- Higher layers can STRENGTHEN (SHOULD → MUST) but NEVER weaken (MUST → SHOULD)
- Higher layers can ADD new principles
- Higher layers can REFINE parameters (e.g., coverage 80% → 90%)

**Layer Applicability**:
- Layer 0 (base): Always applies
- Layer 1 (domain): Applies when business domain selected
- Layer 2 (platform): Applies when cross-platform framework selected (mobile only)
- Layer 3 (project): Always applies, contains project-specific overrides

## Available Domains

| Domain | File | Use Cases |
|--------|------|-----------|
| fintech | `domains/fintech.md` | Payments, trading, banking, investment |
| healthcare | `domains/healthcare.md` | EHR, patient portals, HIPAA-regulated |
| e-commerce | `domains/e-commerce.md` | Online stores, marketplaces, checkout |
| saas | `domains/saas.md` | Multi-tenant B2B platforms |
| uxq | `domains/uxq.md` | B2C apps, dashboards, onboarding, forms, consumer products |

**Domain Combinations**: Domains can be combined for hybrid contexts:
- `uxq + saas` → Multi-tenant apps with consumer-grade UX
- `uxq + healthcare` → Patient-facing health applications
- `uxq + e-commerce` → Shopping experiences with delight moments

When combining domains, copy both to `constitution.domain.md` and merge principles (stricter level wins).

## Available Platforms

| Platform | File | Use Cases | Integration Checklist |
|----------|------|-----------|----------------------|
| kmp | `platforms/kmp.md` | Kotlin Multiplatform iOS+Android | `kmp-integration-checklist.md` |
| flutter | `platforms/flutter.md` | Flutter iOS+Android+Web | `flutter-integration-checklist.md` |
| react-native | `platforms/react-native.md` | React Native iOS+Android | `rn-integration-checklist.md` |

**Platform Detection**: Platforms can be auto-detected from codebase:
- `build.gradle.kts` with `kotlin("multiplatform")` → KMP
- `pubspec.yaml` with `flutter:` → Flutter
- `package.json` with `react-native` dependency → React Native

See `templates/shared/platform-detection.md` for full detection algorithm.

**Platform + Domain Combinations**: Platform layer combines with domain layer:
- `kmp + fintech` → KMP app with financial security requirements
- `flutter + healthcare` → Flutter app with HIPAA compliance
- `react-native + e-commerce` → RN app with PCI-DSS requirements

## Execution Flow

### 0. Check for Interactive Mode

**FIRST**, check if `$ARGUMENTS` is empty or whitespace-only:
- If **empty** → Execute Phase 0 (ask 3-4 questions via AskUserQuestion)
- If **not empty** → Skip to step 1 and parse the input

### 1. Determine Operation Mode

Parse user input (from `$ARGUMENTS` or Phase 0 questionnaire results):

| User Says | Operation |
|-----------|-----------|
| (empty input) | Interactive questionnaire (Phase 0) |
| "set domain fintech" | Select domain layer |
| "add principle" / "strengthen" | Modify project layer |
| "set language ru" / "язык русский" | Configure artifact language |
| "--merge" / "show effective" | Generate merged view |
| (other text) | Interactive edit of project layer |

### 2. Load Existing Layers

Load available constitution layers:

```text
1. Read /memory/constitution.base.md (always exists)
2. Check if /memory/constitution.domain.md exists
   - If yes, read and identify domain
   - If no, note that no domain is selected
3. Read /memory/constitution.md (project layer)
```

### 3a. Domain Selection (if requested)

If user requests domain selection:

1. Validate domain exists in `/memory/domains/[domain].md`
2. Copy domain file to `/memory/constitution.domain.md`
3. Update project constitution header: `Domain Layer: [domain]`
4. Report domain principles added/strengthened

### 3b. Project Layer Edit (default)

If editing project layer:

1. Identify placeholder tokens `[ALL_CAPS_IDENTIFIER]`
2. Collect/derive values:
   - From user input if supplied
   - From repo context (README, docs, prior versions)
   - Dates: ISO format YYYY-MM-DD
3. Ensure overrides follow inheritance rules:
   - Cannot weaken base/domain MUST principles
   - Can strengthen SHOULD → MUST
   - Can add PRJ-xxx project principles

### 3c. Merge View (if --merge)

If generating merged view:

```text
FOR EACH principle in base:
  IF domain overrides it:
    Use domain version
  IF project overrides it:
    Use project version
  ELSE:
    Use base version

ADD domain-specific principles
ADD project-specific principles

OUTPUT merged constitution
```

### 3d. Project Settings (if "set language" or similar)

If configuring project settings:

1. Locate the **Project Settings** table in `/memory/constitution.md`
2. Update the requested setting:

   | Setting | Valid Values | Default |
   |---------|--------------|---------|
   | language | `en`, `ru`, `de`, `fr`, `es`, `zh`, `ja`, `ko`, `pt`, `it`, `pl`, `uk`, `ar`, `hi` | `en` |
   | date_format | `ISO`, `US`, `EU` | `ISO` |
   | measurements | `metric`, `imperial` | `metric` |

3. Report: "Project setting updated: language = ru"

**Language affects all artifact generation commands** (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.design`, `/speckit.concept`).

See `templates/shared/language-context.md` for language behavior details:
- All prose content generated in configured language
- IDs, technical terms, and code remain in English

### 4. Validation

Before finalizing:

- [ ] No unexplained bracket tokens remain
- [ ] No MUST → SHOULD weakening (violation = ERROR)
- [ ] Version updated if changes made
- [ ] Dates in ISO format

**Version Semantics**:
- MAJOR: Principle removal or incompatible redefinition
- MINOR: New principle or significant expansion
- PATCH: Clarifications, parameter tweaks

### 5. Consistency Propagation

Check dependent templates for alignment:

| File | Check |
|------|-------|
| `/templates/plan-template.md` | Constitution Check section aligns |
| `/templates/spec-template.md` | Requirements don't conflict with principles |
| `/templates/tasks-template.md` | Task types reflect principle domains |

### 6. Output

**Sync Impact Report** (as HTML comment in constitution):

```html
<!--
SYNC REPORT - [DATE]
Version: [OLD] → [NEW]
Domain: [DOMAIN or none]

Modified Principles:
- [ID]: [CHANGE]

Added Principles:
- [ID]: [NAME]

Templates Checked:
✅ plan-template.md
✅ spec-template.md
⚠ tasks-template.md (manual review needed)

Follow-up TODOs:
- [ITEM]
-->
```

**User Summary**:
- New version and bump rationale
- Domain status (active/none)
- Files flagged for manual follow-up
- Suggested commit message

## Examples

### Example 1: Select Domain

**Input**: "set domain fintech"

**Actions**:
1. Copy `/memory/domains/fintech.md` → `/memory/constitution.domain.md`
2. Update `/memory/constitution.md` header
3. Report: "Activated fintech domain. 6 principles strengthened, 6 domain principles added."

### Example 2: Strengthen Principle

**Input**: "strengthen QUA-001 to MUST with 95% coverage because we're building critical infrastructure"

**Actions**:
1. Add to Strengthened Principles table in constitution.md
2. Validate: base QUA-001 is SHOULD (can strengthen)
3. Version bump: MINOR (principle strength change)

### Example 3: Add Project Principle

**Input**: "add principle: all API responses must include request-id header for debugging"

**Actions**:
1. Create PRJ-001: Request ID Header
2. Set level: MUST
3. Add validation and violation severity
4. Version bump: MINOR (new principle)

### Example 4: View Effective Constitution

**Input**: "--merge"

**Actions**:
1. Merge all layers
2. Output complete effective constitution
3. Show principle count by domain and level

## Formatting Requirements

- Use Markdown headings exactly as in template
- Lines < 100 chars where practical
- Single blank line between sections
- No trailing whitespace
- Principle IDs: [DOMAIN]-[NNN] (e.g., SEC-001, PRJ-002)

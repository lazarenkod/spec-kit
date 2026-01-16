---
description: Orchestrate mobile development with specialized agents. Activates platform-specific expertise (KMP/Flutter/React Native), calculates Mobile Quality Score (MQS), and ensures production-ready mobile applications.
persona: mobile-developer-agent
model: opus
thinking_budget: 24000

flags:
  - name: --thinking-depth
    type: choice
    choices: [quick, standard, ultrathink]
    default: standard
    description: |
      Thinking budget per agent:
      - quick: 16K budget, core mobile setup, 90s (~$0.12)
      - standard: 32K budget, full platform analysis, 180s (~$0.24) [RECOMMENDED]
      - ultrathink: 96K budget, deep platform expertise, 300s (~$0.72)
  - name: --max-model
    type: string
    default: null
    description: "--max-model <opus|sonnet|haiku> - Override model cap"

modes:
  auto:
    trigger: "Platform detected via platform-detection.md (default)"
    purpose: "Automatically select platform and apply expertise"
  kmp:
    trigger: "--platform kmp OR shared/build.gradle.kts exists"
    purpose: "Apply KMP-specific patterns and validation"
    skill: kmp-expert
  flutter:
    trigger: "--platform flutter OR pubspec.yaml exists"
    purpose: "Apply Flutter-specific patterns and validation"
    skill: flutter-expert
  react_native:
    trigger: "--platform react-native OR metro.config.js exists"
    purpose: "Apply React Native-specific patterns and validation"
    skill: react-native-expert
orchestration:
  agents:
    - mobile-developer-agent     # Core mobile expertise
  skills:
    - mobile-architecture        # Cross-platform architecture decisions
    - mobile-performance         # Performance optimization
    - mobile-testing             # Testing strategy
  conditional_skills:
    - skill: kmp-expert
      when: "platform == kmp"
    - skill: flutter-expert
      when: "platform == flutter"
    - skill: react-native-expert
      when: "platform == react-native"
  flow: sequential
pre_gates:
  - QG-MOBILE-001: Platform successfully detected
  - QG-MOBILE-002: Required dependencies present
gates:
  - QG-MQS: Mobile Quality Score ≥ 75
handoffs:
  - label: Create Implementation Plan
    agent: speckit.plan
    prompt: Create technical plan with mobile architecture decisions
  - label: Generate Tasks
    agent: speckit.tasks
    prompt: Generate tasks with platform-specific and binding test tasks
  - label: Implement
    agent: speckit.implement
    prompt: Execute implementation with mobile patterns
    send: true
  - label: Analyze Quality
    agent: speckit.analyze
    prompt: Validate MQS and binding coverage
claude_code:
  model: opus
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 4000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
        timeout_per_agent: 180000
        retry_on_failure: 1
      pro:
        thinking_budget: 8000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
        timeout_per_agent: 300000
        retry_on_failure: 2
      max:
        thinking_budget: 32000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
        timeout_per_agent: 900000
        retry_on_failure: 3
      ultrathink:
        thinking_budget: 96000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 6.0
  depth_defaults:
    quick:
      thinking_budget: 16000
      skip_agents: [optional-synthesizers]
      timeout: 90
    standard:
      thinking_budget: 32000
      skip_agents: []
      timeout: 180
    ultrathink:
      thinking_budget: 96000
      additional_agents: [platform-deepdive, binding-expert]
      timeout: 300
  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 32000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (96K thinking budget).
          Auto-downgrading to **Standard** mode (32K budget).
  cost_breakdown:
    quick: {cost: $0.12, time: "90-120s"}
    standard: {cost: $0.24, time: "180-240s"}
    ultrathink: {cost: $0.72, time: "300-360s"}
  cache_control:
    system_prompt: ephemeral
    constitution: ephemeral
    templates: ephemeral
    artifacts: ephemeral
    ttl: session
  cache_hierarchy: full
  orchestration:
    max_parallel: 8
    role_isolation: false
  operation_batching:
    enabled: true
    skip_flag: "--sequential"
    framework: templates/shared/operation-batching.md
---

# Mobile Development Orchestrator

## Overview

This command orchestrates mobile development by:
1. Detecting the mobile platform (KMP, Flutter, React Native, Native)
2. Loading platform-specific expertise and skills
3. Applying architecture best practices
4. Validating Mobile Quality Score (MQS)

## User Input

$ARGUMENTS

Parse arguments:
- `--platform <kmp|flutter|react-native|native>`: Override auto-detection
- `--skip-mqs`: Skip MQS calculation (not recommended)
- `--mqs-threshold <N>`: Override default 75 threshold

## Execution Workflow

### Phase 1: Platform Detection

```text
DETECT platform:
  IF shared/build.gradle.kts exists AND contains "kotlin(\"multiplatform\")":
    PLATFORM = "kmp"
    LOAD skill: kmp-expert

  ELSE IF pubspec.yaml exists AND contains "flutter":
    PLATFORM = "flutter"
    LOAD skill: flutter-expert

  ELSE IF package.json exists AND contains "react-native":
    PLATFORM = "react-native"
    LOAD skill: react-native-expert

  ELSE IF *.xcodeproj exists AND no shared code:
    PLATFORM = "ios-native"

  ELSE IF android/app/build.gradle exists AND no shared code:
    PLATFORM = "android-native"

  ELSE:
    FAIL "Unable to detect mobile platform. Use --platform flag."

OUTPUT:
  📱 Platform Detected: {PLATFORM}
  📦 Skills Loaded: {skills}
```

### Phase 2: Architecture Analysis

```text
LOAD skill: mobile-architecture

ANALYZE project:
  1. Layer Separation
     - Check for presentation/domain/data layers
     - Verify dependency direction (inward)
     - Report violations

  2. Dependency Injection
     - Detect DI framework (Koin, GetIt, Hilt, etc.)
     - Verify all dependencies registered
     - Check lifecycle scoping

  3. State Management
     - Detect pattern (ViewModel, BLoC, Redux, etc.)
     - Verify unidirectional data flow
     - Check for anti-patterns

  4. Offline-First
     - Check for local cache implementation
     - Verify sync strategy
     - Report missing offline support

OUTPUT architecture_score (0-25):
  | Component        | Score | Max | Notes |
  |------------------|-------|-----|-------|
  | Layer separation | X     | 8   | ...   |
  | DI configuration | X     | 7   | ...   |
  | Shared code %    | X     | 5   | ...   |
  | State management | X     | 5   | ...   |
```

### Phase 3: Performance Assessment

```text
LOAD skill: mobile-performance

ASSESS performance metrics:
  1. Startup Time
     - Check for lazy initialization
     - Identify blocking operations
     - Estimate cold start time

  2. Rendering
     - Check list virtualization
     - Identify potential jank sources
     - Review image handling

  3. Memory
     - Check for common leaks
     - Review caching strategy
     - Estimate peak usage

  4. Battery
     - Check for polling patterns
     - Review background tasks
     - Identify battery drains

OUTPUT performance_score (0-20):
  | Metric         | Score | Max | Notes |
  |----------------|-------|-----|-------|
  | Startup time   | X     | 6   | ...   |
  | Frame rate     | X     | 6   | ...   |
  | Memory usage   | X     | 4   | ...   |
  | Battery impact | X     | 4   | ...   |
```

### Phase 4: Platform Parity Check

```text
FOR cross-platform projects (KMP, Flutter, RN):
  COMPARE features across platforms:
    - List features per platform
    - Identify platform-specific gaps
    - Check UX consistency

  CHECK platform conventions:
    - iOS: Human Interface Guidelines
    - Android: Material Design
    - Report violations

OUTPUT parity_score (0-20):
  | Aspect          | Score | Max | Notes |
  |-----------------|-------|-----|-------|
  | Feature parity  | X     | 10  | ...   |
  | UX adaptation   | X     | 5   | ...   |
  | Platform bugs   | X     | 5   | ...   |
```

### Phase 5: Testing Validation

```text
LOAD skill: mobile-testing

VALIDATE test coverage:
  1. Unit Tests
     - Measure coverage percentage
     - Identify untested ViewModels
     - Check test quality

  2. Binding Tests (for cross-platform)
     **Agent**: test-generator-agent
     **Skill**: binding-test-generator
     **Purpose**: Automated generation and validation of platform binding tests

     - FOR EACH ViewModel/Controller/Store:
         - Check iOS wrapper tests exist
         - Check Android tests exist
         - Verify 100% method coverage (QG-BIND-001)
         - Validate no stub methods (QG-BIND-004)
         - Check all observable properties tested (QG-BIND-002)

     **Validation Commands**:
     ```bash
     # QG-BIND-004: No stub methods in generated tests
     grep -r "// TODO: Implement" ios/Tests/*BindingTests.swift && FAIL
     grep -r "fatalError(" ios/Tests/ && FAIL
     grep -r "throw NotImplementedError" android/app/src/test/*BindingTest.kt && FAIL
     ```

     **Templates Used**:
     - templates/test-templates/ios-binding-test.swift.template
     - templates/test-templates/android-binding-test.kt.template

     **Reference**: See templates/skills/binding-test-generator.md for patterns

  3. E2E Tests
     - Check critical paths covered
     - Verify Maestro/Detox flows exist
     - Review test reliability

OUTPUT testing_score (0-20):
  | Type           | Score | Max | Notes |
  |----------------|-------|-----|-------|
  | Unit coverage  | X     | 8   | X%    |
  | Binding tests  | X     | 6   | X% (QG-BIND-001/004) |
  | E2E coverage   | X     | 6   | X paths |
```

### Phase 6: Automated Performance Profiling

```text
AGENT: performance-profiler-agent
SKILL: native-profiling

AUTOMATED profiling with native platform tools:
  **Tier 1 (Ideal)**: Full automation with native tools
  **Tier 2 (Fallback)**: CLI-based automation
  **Tier 3 (Manual)**: Provide manual profiling instructions

  1. iOS Profiling (if iOS platform detected)
     a. Cold Start Measurement (QG-PERF-001)
        - Launch app with xcrun xctrace (App Launch template)
        - Parse trace for didFinishLaunching time
        - Threshold: < 2000ms
        - Auto-fail if ≥ 2000ms

     b. Frame Rate Measurement (QG-PERF-002)
        - Profile with Game Performance template
        - Extract 95th percentile frame time
        - Threshold: ≤ 16.67ms (60 FPS)
        - Auto-fail if < 60 FPS at p95

     c. Memory Profiling (QG-PERF-003, QG-PERF-004)
        - Profile with Allocations template
        - Track peak memory usage
        - Detect leaked allocations
        - Thresholds: < 150MB, 0 leaks

  2. Android Profiling (if Android platform detected)
     a. Cold Start Measurement (QG-PERF-001)
        - adb shell am start -W
        - Parse TotalTime from output
        - Threshold: < 1500ms
        - Auto-fail if ≥ 1500ms

     b. Frame Rate Measurement (QG-PERF-002)
        - adb shell dumpsys gfxinfo
        - Extract 95th percentile frame time
        - Threshold: ≤ 16.67ms (60 FPS)
        - Auto-fail if < 60 FPS at p95

     c. Memory Profiling (QG-PERF-003)
        - adb shell dumpsys meminfo
        - Sample every 5 seconds
        - Track peak PSS value
        - Threshold: < 150MB

  3. Unity Profiling (if Unity project detected)
     - Use UnityProfilerExporter.cs (API mode)
     - OR parse Editor.log (fallback mode)
     - Extract: FPS, GC alloc, draw calls, memory

  4. Battery Impact (QG-PERF-005)
     - Optional: Requires physical device + 60+ minutes
     - Estimate drain rate (%/hour)
     - Threshold: < 5%/hour
     - Skip if not feasible

SCRIPTS USED:
  - scripts/bash/mobile-profile.sh (iOS/Android on macOS/Linux)
  - scripts/bash/unity-profiler-export.sh (Unity projects)
  - scripts/powershell/Mobile-Profile.ps1 (Android on Windows)

OUTPUT: reports/performance-report.md, reports/performance-metrics.json
  {
    "cold_start_ms": 1234,
    "fps_p95": 58,
    "memory_peak_mb": 142,
    "leaked_allocations": 0,
    "battery_drain_percent": 4.2,
    "quality_gates": {
      "QG-PERF-001": "PASS|FAIL",
      "QG-PERF-002": "PASS|FAIL",
      "QG-PERF-003": "PASS|FAIL",
      "QG-PERF-004": "PASS|FAIL",
      "QG-PERF-005": "PASS|SKIP"
    },
    "performance_score": 17
  }

INTEGRATION with MQS:
  - Automated profiling score overrides Phase 3 static assessment
  - If automated profiling available → use runtime metrics (0-20 points)
  - If automated profiling unavailable → fallback to static assessment
  - Priority: Runtime metrics > Static code analysis

REFERENCE: templates/skills/native-profiling.md for detailed patterns
```

### Phase 7: Accessibility Check

```text
CHECK accessibility:
  1. Labels
     - iOS: accessibilityLabel present
     - Android: contentDescription present
     - Flutter: Semantics widgets used

  2. Screen Reader
     - Navigation order logical
     - All interactive elements reachable
     - Announcements meaningful

  3. Touch Targets
     - Minimum 44pt (iOS) / 48dp (Android)
     - Sufficient spacing between targets

OUTPUT accessibility_score (0-15):
  | Check           | Score | Max | Notes |
  |-----------------|-------|-----|-------|
  | A11y labels     | X     | 5   | ...   |
  | Screen reader   | X     | 5   | ...   |
  | Touch targets   | X     | 5   | ...   |
```

### Phase 8: MQS Calculation

```text
CALCULATE Mobile Quality Score:

  MQS = architecture_score     # 0-25
      + performance_score      # 0-20
      + parity_score          # 0-20
      + testing_score         # 0-20
      + accessibility_score   # 0-15
                              # Total: 0-100

IF MQS < 75:
  STATUS = "⚠️ Below Threshold"
  GENERATE improvement recommendations
  BLOCK release (unless --skip-mqs)
ELSE IF MQS < 90:
  STATUS = "✅ Production Ready (Minor Polish)"
ELSE:
  STATUS = "🌟 Excellent"

OUTPUT:
  ┌─────────────────────────────────────────────────────────────┐
  │                   MOBILE QUALITY SCORE                       │
  ├─────────────────────────────────────────────────────────────┤
  │  Architecture    ████████████████████░░░░░  20/25           │
  │  Performance     ████████████████░░░░░░░░░  16/20           │
  │  Platform Parity ████████████████████░░░░░  18/20           │
  │  Testing         ████████████████████░░░░░  18/20           │
  │  Accessibility   ████████████░░░░░░░░░░░░░  12/15           │
  ├─────────────────────────────────────────────────────────────┤
  │  TOTAL                                       84/100  ✅     │
  └─────────────────────────────────────────────────────────────┘
```

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| MQS Report | `memory/mqs-report.md` | Detailed quality breakdown |
| Architecture ADR | `memory/mobile-architecture.md` | Architecture decisions |
| Improvement Plan | `memory/mobile-improvements.md` | Recommended fixes |
| Binding Coverage | `memory/binding-coverage.md` | ViewModel test mapping |

## Quality Gates

| Gate ID | Purpose | Threshold | Blocks |
|---------|---------|-----------|--------|
| QG-MOBILE-001 | Platform detected | PASS/FAIL | Workflow |
| QG-MOBILE-002 | Dependencies present | PASS/FAIL | Workflow |
| QG-MQS-001 | Architecture score | ≥ 20/25 | Release |
| QG-MQS-002 | Performance score | ≥ 15/20 | Release |
| QG-MQS-003 | Platform parity | ≥ 15/20 | Release |
| QG-MQS-004 | Testing coverage | ≥ 15/20 | Release |
| QG-MQS-005 | Accessibility | ≥ 10/15 | Release |
| QG-MQS | Total MQS | ≥ 75/100 | Store submission |

## Integration with Other Commands

### Before `/speckit.plan`

```text
RUN /speckit.mobile to:
1. Detect platform and load expertise
2. Generate architecture recommendations
3. Create preliminary MQS baseline

THEN /speckit.plan receives:
- Platform-specific architecture patterns
- DI framework recommendations
- Offline-first strategy (if applicable)
```

### Before `/speckit.tasks`

```text
RUN /speckit.mobile to:
1. Identify platform-specific task requirements
2. Generate binding test task list
3. Create E2E test task list

THEN /speckit.tasks injects:
- Phase 2e-BINDING tasks (for KMP)
- Platform integration tasks
- MQS validation tasks
```

### After `/speckit.implement`

```text
RUN /speckit.mobile --validate to:
1. Re-calculate MQS with implemented code
2. Verify all binding tests pass
3. Confirm no TODO stubs remain

BLOCKS release if MQS < 75
```

## Example Output

```text
📱 Mobile Development Analysis

Platform: Kotlin Multiplatform (KMP)
Skills: kmp-expert, mobile-architecture, mobile-performance, mobile-testing

🏗️ Architecture Analysis (22/25)
   ✅ Clean layer separation (presentation/domain/data)
   ✅ Koin DI configured for both platforms
   ✅ Shared code ratio: 82% (target: ≥70%)
   ⚠️ Missing offline-first for annotations feature
   Action: Add local cache for annotations in ReaderRepository

⚡ Performance Analysis (17/20)
   ✅ Cold start: ~1.8s iOS, ~2.1s Android
   ✅ Scroll FPS: 60 FPS both platforms
   ✅ Memory peak: 120MB (target: <150MB)
   ⚠️ Android cold start slightly above 2s
   Action: Lazy-load Koin modules, defer analytics init

🔗 Platform Parity (18/20)
   ✅ All 12 features available on both platforms
   ✅ Material Design on Android, HIG on iOS
   ⚠️ 2 minor UX differences in settings flow
   Action: Align settings screen navigation pattern

🧪 Testing Coverage (18/20)
   ✅ Unit test coverage: 85% (target: ≥80%)
   ✅ Binding tests: 100% (15/15 methods tested)
   ✅ No TODO stubs in platform wrappers
   ⚠️ E2E: 4/6 critical paths covered
   Action: Add Maestro flows for search and sync

♿ Accessibility (13/15)
   ✅ All interactive elements have a11y labels
   ✅ VoiceOver navigation tested
   ⚠️ 3 buttons below 44pt touch target
   Action: Increase nav button touch targets

┌─────────────────────────────────────────────────────────────┐
│                   MOBILE QUALITY SCORE                       │
│                                                              │
│  Architecture    ██████████████████████░░░  22/25           │
│  Performance     █████████████████░░░░░░░░  17/20           │
│  Platform Parity ██████████████████░░░░░░░  18/20           │
│  Testing         ██████████████████░░░░░░░  18/20           │
│  Accessibility   █████████████░░░░░░░░░░░░  13/15           │
├─────────────────────────────────────────────────────────────┤
│  TOTAL                                      88/100  ✅      │
│  Status: Production Ready (Minor Polish)                    │
└─────────────────────────────────────────────────────────────┘

📋 Recommendations (Priority Order):
1. [HIGH] Add offline cache for annotations
2. [MEDIUM] Optimize Android startup with lazy Koin
3. [MEDIUM] Add remaining E2E Maestro flows
4. [LOW] Increase touch targets for nav buttons

Ready for: /speckit.implement → /speckit.analyze → Release
```

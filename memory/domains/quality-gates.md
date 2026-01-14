# Domain Extension: Quality Gates (Layer 1)

**Extends**: constitution.base.md v1.0
**Regulatory Context**: CI/CD pipelines, code quality standards, deployment safety
**Typical Projects**: All production software requiring automated quality enforcement
**Philosophy**: "Quality is not a phase, it's a gate at every transition"

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Quality Gate** | A checkpoint that must pass before workflow proceeds to next phase |
| **Pre-Implement Gate** | Validates spec/plan quality before code generation begins |
| **Post-Implement Gate** | Validates code quality after implementation completes |
| **Pre-Deploy Gate** | Validates production readiness before deployment |
| **SQS** | Spec Quality Score (0-100) measuring specification quality via 25-checkpoint rubric across 5 dimensions (Clarity, Completeness, Testability, Traceability, No Ambiguity). See [sqs-rubric.md](../../templates/shared/quality/sqs-rubric.md) |
| **DQS** | Design Quality Score (0-100) measuring design specification quality via 25-checkpoint rubric across 5 dimensions (Visual Hierarchy, Consistency, Accessibility, Responsiveness, Interaction Design). See [dqs-rubric.md](../../templates/shared/quality/dqs-rubric.md) |
| **AQS** | Art Quality Score (0-120) measuring game art pipeline quality via 30-checkpoint rubric across 6 dimensions (Visual Style, Asset Completeness, Animation Polish, VFX Believability, Audio Fidelity, Performance Budget). Threshold: ≥90 for world-class. See [aqs-rubric.md](../../templates/shared/quality/aqs-rubric.md) |
| **Coverage** | Percentage of code exercised by tests (line, branch, path) |
| **Type Coverage** | Percentage of code with static type annotations |

---

## Gate Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRE-IMPLEMENT GATES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ QG-001: SQS  │  │ QG-002: Sec  │  │ QG-003: Deps │          │
│  │   >= 80      │  │  Scan Pass   │  │  No Critical │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    /speckit.implement
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    POST-IMPLEMENT GATES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ QG-004: Test │  │ QG-005: Type │  │ QG-006: Lint │          │
│  │ Coverage 80% │  │ Coverage 95% │  │  Zero Errors │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ QG-007: Perf │  │ QG-008: A11y │  │ QG-009: Docs │          │
│  │ Lighthouse 90│  │  WCAG 2.1 AA │  │ API Documented│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                      Pre-Deploy Check
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     PRE-DEPLOY GATES                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ QG-010: All  │  │ QG-011: No   │  │ QG-012: Env  │          │
│  │ Tests Pass   │  │ Console Logs │  │Vars Documented│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Strengthened Principles

These principles from `constitution.base.md` are elevated for quality-gated projects:

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| QUA-001 | SHOULD (unit) | MUST (80%+) | Coverage gate requires enforcement |
| QUA-003 | MUST | MUST (blocking) | Code review MUST block non-compliant PRs |
| QUA-004 | SHOULD | MUST | Formatter/linter MUST run in CI |
| TST-001 | SHOULD | MUST | Tests MUST map to acceptance scenarios |
| SEC-001 | MUST | MUST (scanned) | Secrets MUST be detected via automated scanning |

---

## Design Quality Gates (QG-DQS-xxx)

> **Design Quality Score (DQS)** gates ensure design specifications meet quality standards before implementation.
> See `templates/shared/quality/dqs-rubric.md` for full rubric.

### QG-DQS-001: Minimum Design Quality Score

**Level**: MUST (for UI-heavy features)
**Applies to**: All `/speckit.implement` invocations with design.md artifacts

Design implementation MUST NOT begin until Design Quality Score (DQS) reaches minimum threshold.

**Threshold**: DQS >= 70

**DQS Rubric v1.0** (25 checkpoints across 5 dimensions):

| Dimension | Points | Key Checkpoints |
|-----------|--------|-----------------|
| **Visual Hierarchy** | 25 | Clear CTAs, heading levels, white space, visual weight, content scanning |
| **Consistency** | 20 | Token usage, component reuse, naming conventions, interaction patterns, icon system |
| **Accessibility** | 25 | Color contrast, touch targets, focus indicators, screen reader support, reduced motion |
| **Responsiveness** | 15 | Breakpoints, layout adaptation, touch vs pointer, content priority, image optimization |
| **Interaction Design** | 15 | State definitions, animation timing, loading states, error handling, success feedback |

**Formula**: `DQS = VisualHierarchy + Consistency + Accessibility + Responsiveness + InteractionDesign`

**Full Rubric**: See [templates/shared/quality/dqs-rubric.md](../../templates/shared/quality/dqs-rubric.md)

**Validation**:
```bash
/speckit.analyze --profile dqs
# Output: DQS: 85/100 (Visual: 22, Consist: 18, A11y: 23, Resp: 12, Interact: 10)
```

**Thresholds**:
- **≥70**: Ready for implementation
- **50-69**: Needs improvement (iterate on design)
- **<50**: Major rework required (block implementation)

**Violations**: HIGH - Design not ready, implementation will have UX issues

---

### QG-DQS-002: Accessibility Compliance

**Level**: MUST
**Applies to**: All UI features

Design MUST pass accessibility dimension with minimum score.

**Threshold**: Accessibility dimension >= 60% (15/25 points)

**Key Checks**:
- Color contrast ratios (4.5:1 text, 3:1 UI)
- Touch targets (44×44px minimum)
- Focus indicators defined
- Screen reader support documented
- Reduced motion alternatives

**Validation**:
```bash
/speckit.analyze --profile dqs --dimension accessibility
```

**Violations**: CRITICAL - Accessibility barriers for users

---

### QG-DQS-003: WCAG Compliance

**Level**: MUST
**Applies to**: All public-facing web applications

Design MUST have zero WCAG 2.1 AA violations in color contrast.

**Threshold**: All text colors meet WCAG 2.1 AA contrast requirements

**Validation**:
- Normal text: >= 4.5:1 contrast ratio
- Large text (18px+ or 14px+ bold): >= 3:1 contrast ratio
- UI components: >= 3:1 contrast ratio

**Violations**: CRITICAL - Legal compliance risk, accessibility barriers

---

## Test-First Development Gates (QG-STAGING-xxx, QG-TEST-xxx)

> **Test-First Development** gates ensure staging infrastructure is ready and tests exist before implementation.
> Tests MUST exist and FAIL before code is written (TDD).

### QG-STAGING-001: Staging Environment Ready

**Level**: MUST
**Applies to**: All `/speckit.implement` invocations
**Phase**: Pre-Implement

Local staging environment MUST be provisioned and healthy before implementation begins.

**Threshold**: All staging services pass health checks

**Validation**:
```bash
docker-compose -f .speckit/staging/docker-compose.yaml ps --format json
# All services must show "running" and "healthy"
```

**Required Services**:
| Service | Health Check | Required |
|---------|-------------|----------|
| test-db (postgres) | `pg_isready` | YES |
| test-redis | `redis-cli ping` | YES |
| playwright | Container running | For E2E features |

**Violations**: CRITICAL - Cannot run tests without infrastructure

---

### QG-TEST-001: Test Completeness

**Level**: MUST
**Applies to**: All `/speckit.tasks` outputs
**Phase**: Pre-Implement

Every Acceptance Scenario (AS-xxx) marked "Requires Test = YES" MUST have a corresponding test task.

**Threshold**: 100% coverage of required test scenarios

**Validation**:
```bash
/speckit.analyze --profile test-completeness
# Parses tasks.md TTM, compares against spec.md AS list
```

**Formula**:
```
Test Completeness = (AS with [TEST:] markers) / (AS with "Requires Test = YES") × 100
```

**Thresholds**:
- **100%**: Ready for implementation
- **<100%**: BLOCK - Add missing test tasks

**Violations**: CRITICAL - Untested acceptance scenarios

---

### QG-TEST-002: Test Infrastructure Ready

**Level**: MUST
**Applies to**: All `/speckit.implement` invocations
**Phase**: Pre-Implement

Test framework MUST be configured and executable before implementation begins.

**Threshold**: Test command runs successfully (even with 0 tests)

**Validation by Language**:

| Language | Package File | Test Command | Config File |
|----------|-------------|--------------|-------------|
| TypeScript | package.json | `npm test` | jest.config.js / vitest.config.ts |
| Python | pyproject.toml | `pytest` | pytest.ini / pyproject.toml |
| Go | go.mod | `go test ./...` | - |

**Implementation**:
```bash
# Node.js
npm test -- --passWithNoTests --coverage

# Python
pytest --collect-only || pytest --co

# Go
go test ./... -count=0
```

**Violations**: CRITICAL - Cannot verify implementation without test infrastructure

**Enforcement**:

QG-TEST-002 is now enforced as a CRITICAL pre-gate in `/speckit.implement`:

**Pre-Implementation (Wave 0)**:
- Added as `IG-IMPL-005` in pre_gates section
- Severity: CRITICAL (blocking)
- Auto-remediation: Enabled by default

**Auto-Remediation Flow**:
When QG-TEST-002 fails:
1. Automatically invokes `framework-installer` agent (3-minute timeout)
2. Detects platform and required frameworks from:
   - tasks.md ("Test Framework:" markers)
   - constitution.md (language, platform, tech_stack)
   - Project structure (existing configs, dependencies)
   - Best practice defaults (registry-based)
3. Installs missing frameworks using Test Framework Registry
4. Re-validates QG-TEST-002
5. If still failing → blocks Wave 2 with manual remediation steps

**Skip Auto-Remediation**:
```bash
/speckit.implement --no-auto-framework
```

**Supported Frameworks** (via Test Framework Registry):
- **Unit/Integration**: Jest, Vitest, pytest, Go test, cargo test, JUnit5, TestNG, RSpec, xUnit, NUnit, Mocha, unittest
- **E2E Web**: Playwright, Cypress, Selenium, Puppeteer, WebdriverIO
- **E2E Mobile**: Maestro, XCUITest, Espresso, Detox, Flutter test, Appium, XCTest
- **E2E Desktop**: Tauri test, Spectron, WebdriverIO Electron
- **API Testing**: Supertest, REST Assured, Newman, requests-mock, httptest
- **Performance**: k6, Artillery, Locust, JMeter
- **Visual Regression**: Percy, Chromatic, BackstopJS, Playwright Visual
- **Contract Testing**: Pact, Spring Cloud Contract

**Manual Validation** (if auto-remediation disabled):
```bash
# Node.js
npm test -- --passWithNoTests

# Python
pytest --collect-only

# iOS
xcodebuild test -scheme YourAppTests -destination 'platform=iOS Simulator,name=iPhone 15 Pro' -dry-run

# Android
./gradlew testDebugUnitTest --dry-run

# Go
go test ./... -count=0

# Rust
cargo test --no-run
```

**Platform-Specific Notes**:
- **XCUITest**: Requires macOS + Xcode (cannot auto-install, manual setup via App Store)
- **Espresso**: Requires Android SDK + `$ANDROID_HOME` environment variable
- **Flutter test**: Requires Flutter SDK installed
- **Built-in frameworks** (no installation): go-test, cargo-test, unittest, httptest, XCTest

---

### QG-TEST-003: TDD Red-Green Verification

**Level**: MUST
**Applies to**: Wave 2 (Test Scaffolding) completion
**Phase**: During-Implement

All test tasks MUST have tests that FAIL initially (Red phase of TDD).

**Threshold**: 100% of new tests fail on first run (before implementation)

**Validation**:
```bash
# Run tests expecting failures
npm test -- --passWithNoTests=false
# Expected: All tests fail

# After implementation
npm test
# Expected: All tests pass
```

**Rationale**: Confirms tests are actually testing new functionality, not passing trivially.

**Violations**: HIGH - Tests may not be testing real behavior

---

### QG-TEST-004: Per-Story Test Coverage

**Level**: MUST
**Applies to**: Each story phase completion
**Phase**: Post-Story

Code coverage MUST meet minimum threshold after each story implementation.

**Threshold**: >= 80% line coverage for new code

**Validation**:
```bash
# Jest
jest --coverage --coverageThreshold='{"global":{"lines":80}}'

# Pytest
pytest --cov=src --cov-fail-under=80

# Go
go test -coverprofile=coverage.out && go tool cover -func=coverage.out
```

**Per-Story Tracking**:
| Story | Files Changed | Coverage Before | Coverage After | Delta |
|-------|--------------|-----------------|----------------|-------|
| US1 | 5 | N/A | 85% | +85% |
| US2 | 3 | 85% | 82% | -3% |

**Violations**: CRITICAL if < 70%, HIGH if 70-80%

---

## Mobile Testing Gates (QG-MOB-xxx)

> **Mobile Testing** gates ensure mobile apps are tested on real emulators/simulators.
> Tests MUST run on both Android and iOS for cross-platform frameworks.

### QG-MOB-001: Mobile Staging Ready

**Level**: MUST
**Applies to**: All mobile features (Flutter, React Native, KMP, native iOS/Android)
**Phase**: Pre-Implement

Mobile staging environment MUST be provisioned with working emulator/simulator.

**Threshold**: All mobile staging services pass health checks

**Validation**:
```bash
# Android emulator (Docker)
docker exec speckit-android-emulator adb devices | grep -q "emulator"

# iOS simulator (macOS only)
xcrun simctl list devices | grep -q "Booted"
```

**Required Services**:
| Service | Health Check | Required |
|---------|-------------|----------|
| android-emulator | `adb devices` | YES (Android/cross-platform) |
| ios-simulator | `xcrun simctl list` | YES (iOS/cross-platform, macOS only) |
| appium-server | HTTP 4723 | OPTIONAL (native automation) |

**Platform-Specific Requirements**:
| Platform | Android | iOS |
|----------|---------|-----|
| Flutter | Required | Required (macOS) or Skipped (Linux/Windows) |
| React Native | Required | Required (macOS) or Skipped |
| KMP | Required | Required (macOS) or Skipped |
| Native Android | Required | N/A |
| Native iOS | N/A | Required (macOS only) |

**Violations**: CRITICAL - Cannot run mobile tests without emulator/simulator

---

### QG-MOB-002: Mobile Test Coverage

**Level**: MUST
**Applies to**: All mobile features
**Phase**: Post-Implement

Mobile test coverage MUST meet minimum threshold.

**Threshold**: >= 70% line coverage for mobile-specific code

**Validation by Framework**:
| Framework | Command | Coverage Format |
|-----------|---------|-----------------|
| Flutter | `flutter test --coverage` | lcov |
| React Native | `jest --coverage` (unit) + Detox | istanbul |
| Native iOS | `xcodebuild ... -enableCodeCoverage YES` | xccov |
| Native Android | `./gradlew jacocoTestReport` | jacoco |

**Coverage Calculation**:
```bash
# Flutter
flutter test --coverage
lcov --summary coverage/lcov.info | grep "lines" | awk '{print $2}'

# React Native
jest --coverage --coverageReporters=text-summary

# iOS (after xcodebuild test)
xcrun xccov view --report result.xcresult

# Android
./gradlew jacocoTestReport
# Parse build/reports/jacoco/test/html/index.html
```

**Thresholds**:
- **≥70%**: Ready for merge
- **50-69%**: Needs improvement (add more tests)
- **<50%**: BLOCK - Insufficient coverage

**Violations**: HIGH - Insufficient mobile test coverage

---

### QG-MOB-003: Cross-Platform Verification

**Level**: MUST
**Applies to**: Flutter, React Native, KMP features
**Phase**: Post-Implement

Cross-platform apps MUST pass tests on BOTH Android AND iOS.

**Threshold**: 100% test pass rate on both platforms

**Validation**:
```bash
# Flutter
flutter test integration_test/ -d <android_emulator>
flutter test integration_test/ -d <ios_simulator>

# React Native (Detox)
detox test --configuration android.emu.debug
detox test --configuration ios.sim.debug

# React Native (Maestro)
maestro test .maestro/ --device android
maestro test .maestro/ --device ios

# KMP
./gradlew connectedAndroidTest        # Android
xcodebuild test -scheme iosApp       # iOS
```

**Skip Conditions**:
- Single-platform native apps (Swift-only or Kotlin-only)
- Platform-specific feature (e.g., Android widget, iOS Today Extension)
- No macOS available for iOS tests (skip with WARNING, not FAIL)

**Platform Matrix**:
| Framework | Android | iOS (macOS) | iOS (Linux/Windows) |
|-----------|---------|-------------|---------------------|
| Flutter | MUST pass | MUST pass | SKIP with warning |
| React Native | MUST pass | MUST pass | SKIP with warning |
| KMP | MUST pass | MUST pass | SKIP with warning |

**Violations**: CRITICAL - Cross-platform apps must work on both platforms

---

### QG-MOB-004: Device Profile Validation

**Level**: SHOULD
**Applies to**: All mobile features
**Phase**: Post-Implement

App SHOULD be tested on representative device profiles.

**Threshold**: Tests pass on at least one device from each category

**Device Categories**:
| Category | Examples | Min Test |
|----------|----------|----------|
| Small phone | iPhone SE, Pixel 4a | 1 device |
| Large phone | iPhone 15 Pro Max, Pixel 8 Pro | 1 device |
| Tablet | iPad, Pixel Tablet | 1 device (if tablet support specified) |

**Reference**: `templates/shared/device-profiles.md`

**Validation**:
```bash
# Test on multiple device profiles
flutter test integration_test/ -d "iPhone SE"
flutter test integration_test/ -d "iPhone 15 Pro Max"
flutter test integration_test/ -d "iPad Pro"
```

**Performance Thresholds** (from `memory/domains/mobile.md`):
| Metric | MUST | Lovable |
|--------|------|---------|
| Cold start | < 2s | < 1s |
| Warm start | < 500ms | < 200ms |
| Touch response | < 100ms | < 50ms |
| Animations | 60fps | 120fps (ProMotion) |
| Battery drain | < 5%/hour | < 2%/hour |
| App size (iOS) | < 200MB | < 100MB |
| App size (Android) | < 150MB | < 75MB |

**Violations**: MEDIUM - May have device-specific issues

---

### Mobile Gate Enforcement Matrix

| Gate ID | Phase | Level | Threshold | Validation | Severity |
|---------|-------|-------|-----------|------------|----------|
| QG-MOB-001 | Pre-Implement | MUST | Emulators healthy | Health check | CRITICAL |
| QG-MOB-002 | Post-Implement | MUST | >= 70% coverage | Coverage report | HIGH |
| QG-MOB-003 | Post-Implement | MUST | 100% both platforms | Test pass rate | CRITICAL |
| QG-MOB-004 | Post-Implement | SHOULD | Device categories | Multi-device tests | MEDIUM |
| QG-BIND-001 | Post-Implement | MUST | 100% method coverage | Binding test coverage | CRITICAL |
| QG-BIND-002 | Post-Implement | MUST | 100% observables tested | Observable test coverage | CRITICAL |
| QG-BIND-003 | Post-Implement | MUST | 0 TODO/stub comments | Code pattern scan | HIGH |
| QG-BIND-004 | Post-Implement | MUST | 0 stub methods | Generated test validation | HIGH |
| QG-PARITY-001 | Post-Implement / Pre-Release | MUST | ≥ 95% feature parity | Feature parity analysis | CRITICAL |
| QG-PARITY-002 | Post-Implement / Pre-Release | MUST | ≥ 80% UX adaptation | UX adaptation scoring | HIGH |
| QG-PARITY-003 | Post-Implement / Pre-Release | MUST | 0 platform regressions | Regression detection | CRITICAL |

---

## Platform Binding Test Gates (QG-BIND-xxx)

> **Platform Binding Test Gates** ensure cross-platform apps have comprehensive binding tests.
> Prevents "wrapper bugs" - shared code works but platform wrappers have stubs/TODOs.
> **Agent**: test-generator-agent (persona) with binding-test-generator (skill)

### QG-BIND-001: 100% ViewModel Method Coverage

**Level**: MUST
**Applies to**: KMP, Flutter, React Native features
**Phase**: Post-Implement (Wave 2 - Test Scaffolding)

All public methods in shared ViewModels/Controllers MUST have platform binding tests.

**Threshold**: 100% of public methods tested on both iOS and Android

**Validation**:
```bash
# Generate binding coverage report
.speckit/binding-coverage.json

# Check method coverage
jq '.coverage.methodsCovered / .coverage.methodsTotal * 100' .speckit/binding-coverage.json
# Expected: 100%
```

**What to Test**:
- iOS: XCTest wrapper tests that mock ViewModel and verify iOS wrapper calls Kotlin/Dart code
- Android: JUnit/Mockito tests that verify Android wrapper calls shared code
- Every `fun methodName()` → test that verifies platform calls it

**Generated Files**:
- iOS: `ios/Tests/*BindingTests.swift` (using `ios-binding-test.swift.template`)
- Android: `android/app/src/test/*BindingTest.kt` (using `android-binding-test.kt.template`)

**Violations**: CRITICAL - Missing binding tests = undetected wrapper bugs

---

### QG-BIND-002: 100% Observable Property Coverage

**Level**: MUST
**Applies to**: KMP, Flutter, React Native features
**Phase**: Post-Implement (Wave 2 - Test Scaffolding)

All observable properties (StateFlow, Flow, LiveData, etc.) MUST be observed in platform UI tests.

**Threshold**: 100% of StateFlow/Flow/LiveData properties tested

**Validation**:
```bash
# Check from binding coverage report
jq '.coverage.stateFlowsCovered / .coverage.stateFlowsTotal * 100' .speckit/binding-coverage.json
# Expected: 100%
```

**What to Test**:
- iOS: Test `.sink`/`.assign`/Combine publisher receives state updates from Kotlin StateFlow
- Android: Test `.collectAsState()`/`.observe()` receives state updates
- Verify UI re-renders on state change

**Example**:
```swift
// iOS test for StateFlow observation
func test_currentPage_observesStateFlow() {
    let expectation = expectation(description: "StateFlow observed")
    viewModel.currentPage.sink { page in
        XCTAssertEqual(page, 5)
        expectation.fulfill()
    }
    wait(for: [expectation], timeout: 1.0)
}
```

**Violations**: CRITICAL - Missing observable tests = undetected state sync bugs

---

### QG-BIND-003: Zero TODO/Stub Comments in Platform Code

**Level**: MUST
**Applies to**: All cross-platform features
**Phase**: Post-Implement (Wave 3 - Core Implementation)

Platform binding code MUST NOT contain TODO/FIXME/stub comments.

**Threshold**: 0 TODO/FIXME/stub patterns found

**Validation**:
```bash
# Scan for stub patterns
grep -r "// TODO" ios/App/ android/app/src/main/
grep -r "// FIXME" ios/App/ android/app/src/main/
grep -r "fatalError(\"not implemented\")" ios/App/
grep -r "throw NotImplementedError()" android/app/src/main/

# Expected: No matches (exit code 1 from grep = good)
```

**Violations**: HIGH - Incomplete platform code = crashes, broken features

---

### QG-BIND-004: No Stub Methods in Generated Binding Tests

**Level**: MUST
**Applies to**: All cross-platform features with binding tests
**Phase**: Post-Implement (Wave 2 - Test Scaffolding)

Generated binding tests MUST be fully implemented with no stub methods or TODO comments.

**Threshold**: 0 stub methods, 0 TODO comments in generated tests

**Validation**:
```bash
# Scan generated test files for stubs
grep -r "// TODO: Implement" ios/Tests/*BindingTests.swift && exit 1
grep -r "fatalError(" ios/Tests/*BindingTests.swift && exit 1
grep -r "throw NotImplementedError" android/app/src/test/*BindingTest.kt && exit 1

# All commands should exit with code 1 (no matches) for gate to pass
```

**Why This Matters**:
- Generated tests with stubs = false sense of security
- Automated test generation MUST produce complete, runnable tests
- Prevents "TDD theater" - tests exist but don't actually test anything

**Generation Process**:
1. `test-generator-agent` analyzes ViewModel method signatures
2. Uses `binding-test-generator` skill patterns (4 patterns: void, value, Flow, suspend)
3. Generates complete tests using templates:
   - `templates/test-templates/ios-binding-test.swift.template`
   - `templates/test-templates/android-binding-test.kt.template`
4. QG-BIND-004 validates no stubs remain

**Violations**: HIGH - Stub tests provide no value, waste CI/CD resources

**Reference**: See `templates/skills/binding-test-generator.md` for comprehensive patterns

---

## Cross-Platform Parity Gates (QG-PARITY-xxx)

> **Platform Parity Quality Gates** ensure cross-platform mobile applications (KMP, Flutter, React Native) maintain feature consistency, appropriate UX adaptations, and zero platform-specific regressions across iOS and Android implementations.

### QG-PARITY-001: Feature Parity ≥ 95%

**Level**: MUST (for cross-platform mobile apps)
**Applies to**: All cross-platform projects (KMP, Flutter, React Native)
**Phase**: Post-Implement (Wave 4) OR Pre-Release

Cross-platform applications MUST have ≥95% of features available on both iOS and Android platforms.

**Threshold**: Feature Parity Score ≥ 95%

**Formula**:
```
Feature Parity Score = (Common Features / Total Unique Features) × 100%

Where:
- Common Features = Features implemented on both iOS and Android
- Total Unique Features = Common + iOS-only + Android-only
```

**Validation**:
```bash
# Run parity validation
specify analyze --profile parity

# Check parity score
parity_score=$(jq '.parity_score' reports/parity-score.json)
if [ "$parity_score" -ge 95 ]; then
    echo "QG-PARITY-001: PASS ($parity_score%)"
    exit 0
else
    echo "QG-PARITY-001: FAIL ($parity_score% < 95% threshold)"
    jq '.ios_only_features' reports/parity-score.json
    jq '.android_only_features' reports/parity-score.json
    exit 1
fi
```

**Feature Detection**:

iOS:
```bash
# Detect ViewControllers
grep -r "class.*ViewController.*UIViewController" ios/ --include="*.swift" | \
  sed -E 's/.*class ([A-Za-z0-9]+)ViewController.*/\1/' | sort -u

# Detect SwiftUI Views
grep -r "struct.*View.*View" ios/ --include="*.swift" | \
  sed -E 's/.*struct ([A-Za-z0-9]+)View.*/\1/' | sort -u
```

Android:
```bash
# Detect Activities
grep -r "class.*Activity.*AppCompatActivity" android/ --include="*.kt" | \
  sed -E 's/.*class ([A-Za-z0-9]+)Activity.*/\1/' | sort -u

# Detect Fragments/Composables
grep -r "class.*Fragment.*Fragment" android/ --include="*.kt" | \
  sed -E 's/.*class ([A-Za-z0-9]+)Fragment.*/\1/' | sort -u
```

**Why This Matters**:
- Users expect feature parity across platforms
- Missing features on one platform lead to user churn
- Platform-specific limitations should be rare (<5%)
- Feature gaps indicate incomplete implementations

**Acceptable Exceptions** (<5% allowed):
- Platform-exclusive features (e.g., iOS HealthKit, Android NFC)
- Platform-specific APIs with no equivalent (document in `platform-differences.md`)

**Violations**: CRITICAL - Feature missing on one platform

**Integration**:
- **Persona**: `parity-validator-agent`
- **Skill**: `platform-parity`
- **Command**: `/speckit.analyze --profile parity`
- **MQS Impact**: Contributes 10/20 points to Platform Parity component

**Reference**: See `templates/skills/platform-parity.md` for feature detection algorithms

---

### QG-PARITY-002: UX Adaptation Score ≥ 80%

**Level**: MUST (for cross-platform mobile apps)
**Applies to**: All cross-platform projects (KMP, Flutter, React Native)
**Phase**: Post-Implement (Wave 4) OR Pre-Release

Cross-platform applications MUST correctly adapt UX patterns to each platform's guidelines (≥80% adaptation quality).

**Threshold**: UX Adaptation Score ≥ 80%

**Formula**:
```
UX Adaptation Score = Average(iOS Screen Scores, Android Screen Scores)

Per-Screen Score (0-100):
- Navigation patterns: 20pt
- Primary action placement: 20pt
- Modal/dialog presentation: 15pt
- List interactions: 15pt
- Haptic feedback: 10pt
- Share functionality: 10pt
- Search UI: 10pt
```

**Validation**:
```bash
# Run parity validation
specify analyze --profile parity

# Check adaptation score
adaptation_score=$(jq '.adaptation_score' reports/parity-score.json)
if [ "$adaptation_score" -ge 80 ]; then
    echo "QG-PARITY-002: PASS ($adaptation_score%)"
    exit 0
else
    echo "QG-PARITY-002: FAIL ($adaptation_score% < 80% threshold)"
    jq '.adaptation_issues' reports/parity-score.json
    exit 1
fi
```

**iOS Platform Patterns (Expected)**:
- ✅ UINavigationController with back button (top-left)
- ✅ UITabBarController at bottom
- ✅ Sheet presentation with swipe-to-dismiss
- ✅ Swipe actions on list items (leading/trailing)
- ✅ UIFeedbackGenerator for haptics
- ✅ UIActivityViewController for sharing
- ✅ UISearchController in navigation bar

**Android Platform Patterns (Expected)**:
- ✅ Jetpack Navigation with back gesture
- ✅ BottomNavigationView or NavigationBar
- ✅ FloatingActionButton for primary action
- ✅ Material Snackbar for feedback
- ✅ Material motion transitions
- ✅ Intent.ACTION_SEND for sharing
- ✅ SearchView in ActionBar/Toolbar

**Why This Matters**:
- Platform-appropriate UX feels native and intuitive
- Wrong patterns confuse users (e.g., iOS back button on Android)
- Platform guidelines exist for good UX reasons
- "Cross-platform" ≠ "identical UI" - adapt, don't copy

**Common Anti-Patterns** (AUTO-FAIL):
- ❌ iOS-style back button (←) on Android
- ❌ Android FAB on iOS
- ❌ Custom dialogs instead of platform share sheets
- ❌ Identical navigation on both platforms

**Violations**: HIGH - Wrong platform patterns applied

**Integration**:
- **Persona**: `parity-validator-agent`
- **Skill**: `platform-parity`
- **Command**: `/speckit.analyze --profile parity`
- **MQS Impact**: Contributes 6/20 points to Platform Parity component

**Reference**: See `templates/skills/platform-parity.md` for UX adaptation scoring algorithm

---

### QG-PARITY-003: Zero Platform-Specific Regressions

**Level**: MUST (for cross-platform mobile apps)
**Applies to**: All cross-platform projects (KMP, Flutter, React Native)
**Phase**: Post-Implement (Wave 4) OR Pre-Release

Cross-platform applications MUST have ZERO platform-specific crashes or regressions (bugs that only occur on one platform).

**Threshold**: 0 platform-specific regressions

**Validation**:
```bash
# Run parity validation
specify analyze --profile parity

# Check regression count
regression_count=$(jq '.regression_count' reports/parity-score.json)
if [ "$regression_count" -eq 0 ]; then
    echo "QG-PARITY-003: PASS (0 regressions)"
    exit 0
else
    echo "QG-PARITY-003: FAIL ($regression_count regressions detected)"
    jq '.ios_only_crashes' reports/parity-score.json
    jq '.android_only_crashes' reports/parity-score.json
    jq '.performance_disparities' reports/parity-score.json
    exit 1
fi
```

**Detection Methods**:

**1. Platform-Specific Crashes**:
```bash
# iOS crash logs
grep -r "Exception Type:" ios/CrashLogs/ --include="*.crash"

# Android crash logs
grep -r "FATAL EXCEPTION" android/CrashLogs/
```

**2. Synchronization Issues**:
- Compare offline-first implementation (iOS vs Android)
- Verify data sync logic is identical
- Check conflict resolution consistency

**3. Performance Disparities** (>30% difference):
```python
def is_performance_regression(ios_metric, android_metric):
    avg = (ios_metric + android_metric) / 2
    disparity = abs(ios_metric - android_metric) / avg * 100
    return disparity > 30  # Flag if >30% difference
```

**Why This Matters**:
- Platform-specific bugs indicate incorrect bindings or platform code
- Shared logic (ViewModels) should produce identical behavior
- Performance disparities suggest platform-specific optimizations missing
- Synchronization issues lead to data inconsistencies

**Common Regression Sources**:
- ❌ iOS wrapper doesn't null-check parameters
- ❌ Android wrapper missing error handling
- ❌ Platform-specific state management bugs
- ❌ Different async/await patterns on iOS vs Android
- ❌ Performance issues (cold start, FPS, memory)

**Performance Thresholds** (flag if disparity >30%):
- Cold start: iOS vs Android
- Scroll FPS: iOS 60 FPS vs Android FPS
- Memory usage: iOS peak vs Android peak

**Violations**: CRITICAL - Platform-specific bugs detected

**Integration**:
- **Persona**: `parity-validator-agent`
- **Skill**: `platform-parity`
- **Command**: `/speckit.analyze --profile parity`
- **MQS Impact**: Contributes 4/20 points to Platform Parity component

**Reference**: See `templates/skills/platform-parity.md` for regression detection algorithms

---

## Performance Profiling Gates (QG-PERF-xxx)

> **Performance Profiling Quality Gates** ensure mobile apps meet performance targets through automated profiling with native platform tools.
> Uses runtime metrics (cold start, FPS, memory, battery) to validate app performance.
> **Agent**: performance-profiler-agent (persona) with native-profiling (skill)

### QG-PERF-001: Cold Start < 2000ms (iOS) / < 1500ms (Android)

**Level**: MUST (for mobile apps)
**Applies to**: iOS, Android, KMP, Flutter, React Native, Unity
**Phase**: Post-Implement (Wave 6 - Performance Validation) OR Pre-Release

Mobile applications MUST launch in under 2000ms (iOS) or 1500ms (Android) from cold start to first frame.

**Threshold**: iOS < 2000ms, Android < 1500ms

**Validation**:
```bash
# iOS profiling
scripts/bash/mobile-profile.sh ios \
  --device "iPhone 15 Pro" \
  --bundle-id "com.example.app" \
  --output reports/

# Android profiling
scripts/bash/mobile-profile.sh android \
  --package "com.example.app" \
  --output reports/

# Check cold start time
cold_start=$(jq '.cold_start.total_ms' reports/performance-metrics.json)
threshold=$(jq -r '.cold_start.threshold_ms' reports/performance-metrics.json)

if [ "$cold_start" -lt "$threshold" ]; then
    echo "QG-PERF-001: PASS ($cold_start ms < $threshold ms)"
    exit 0
else
    echo "QG-PERF-001: FAIL ($cold_start ms >= $threshold ms)"
    exit 1
fi
```

**iOS Profiling**:
```bash
# Launch app with Time Profiler
xcrun xctrace record \
  --template "App Launch" \
  --device "${DEVICE_ID}" \
  --launch "${BUNDLE_ID}" \
  --output cold-start.trace \
  --time-limit 10s

# Parse launch time
xcrun xctrace export \
  --input cold-start.trace \
  --xpath '/trace-toc/run[@number="1"]/data/table[@schema="time-profile"]' \
  --output cold-start.xml
```

**Android Profiling**:
```bash
# Force stop and launch
adb shell am force-stop "${PACKAGE_NAME}"
adb shell am start -W -n "${PACKAGE_NAME}/.MainActivity" | \
  grep "TotalTime:" | awk '{print $2}'
```

**Why This Matters**: Cold start time is the first impression. Apps taking >2s to launch lead to user drop-off.

**Optimization Tips**:
- Defer non-critical initialization (analytics, remote config)
- Use lazy loading for heavy resources
- Minimize dependencies loaded at startup
- Profile startup with Xcode Instruments / Android Profiler

**Reference**: See `templates/skills/native-profiling.md` for iOS/Android profiling patterns

---

### QG-PERF-002: 60 FPS (95th Percentile Frame Time ≤ 16.67ms)

**Level**: MUST (for mobile apps)
**Applies to**: iOS, Android, KMP, Flutter, React Native, Unity
**Phase**: Post-Implement (Wave 6) OR Pre-Release

Mobile applications MUST maintain 60 FPS (16.67ms per frame) at the 95th percentile during normal usage.

**Threshold**: 95th percentile frame time ≤ 16.67ms (60 FPS)

**Validation**:
```bash
# iOS profiling
xcrun xctrace record \
  --template "Game Performance" \
  --device "${DEVICE_ID}" \
  --attach "${BUNDLE_ID}" \
  --output fps-profile.trace \
  --time-limit 30s

# Android profiling
adb shell dumpsys gfxinfo "${PACKAGE_NAME}" reset
sleep 30
adb shell dumpsys gfxinfo "${PACKAGE_NAME}" > gfxinfo.txt

# Check FPS
fps_p95=$(jq '.frame_rate.p95_fps' reports/performance-metrics.json)

if (( $(echo "$fps_p95 >= 60" | bc -l) )); then
    echo "QG-PERF-002: PASS ($fps_p95 FPS)"
    exit 0
else
    echo "QG-PERF-002: FAIL ($fps_p95 FPS < 60 FPS)"
    exit 1
fi
```

**Why This Matters**: Frame drops (jank) create a poor user experience. 60 FPS is the minimum for smooth animations and scrolling.

**Common Causes of Jank**:
- Heavy computations on main thread
- Excessive draw calls (target: <500)
- Large texture uploads
- Inefficient list rendering (not virtualized)

**Reference**: See `templates/skills/native-profiling.md` for FPS profiling patterns

---

### QG-PERF-003: Memory Peak < 150MB

**Level**: MUST (for mobile apps)
**Applies to**: iOS, Android, KMP, Flutter, React Native, Unity
**Phase**: Post-Implement (Wave 6) OR Pre-Release

Mobile applications MUST NOT exceed 150MB peak memory usage (excluding system overhead) during normal operation.

**Threshold**: Peak memory < 150MB

**Validation**:
```bash
# iOS profiling
xcrun xctrace record \
  --template "Allocations" \
  --device "${DEVICE_ID}" \
  --attach "${BUNDLE_ID}" \
  --output memory-profile.trace \
  --time-limit 300s

# Android profiling (sample every 5 seconds for 5 minutes)
for i in {1..60}; do
  adb shell dumpsys meminfo "${PACKAGE_NAME}" | grep "TOTAL PSS" | awk '{print $2}'
  sleep 5
done

# Check peak memory
memory_peak=$(jq '.memory.peak_mb' reports/performance-metrics.json)

if [ "$memory_peak" -lt 150 ]; then
    echo "QG-PERF-003: PASS ($memory_peak MB < 150 MB)"
    exit 0
else
    echo "QG-PERF-003: FAIL ($memory_peak MB >= 150 MB)"
    exit 1
fi
```

**Why This Matters**: High memory usage causes OS to terminate background apps (iOS) or trigger OOM killer (Android).

**Optimization Tips**:
- Implement image caching with memory limits (e.g., LRU cache with 50MB max)
- Use pagination for large lists
- Release resources when backgrounded
- Avoid loading entire datasets into memory

**Reference**: See `templates/skills/native-profiling.md` for memory profiling patterns

---

### QG-PERF-004: Zero Memory Leaks

**Level**: MUST (for mobile apps)
**Applies to**: iOS, Android, KMP, Flutter, React Native, Unity
**Phase**: Post-Implement (Wave 6) OR Pre-Release

Mobile applications MUST have ZERO memory leaks after 5-minute profiling session.

**Threshold**: 0 leaked allocations

**Validation**:
```bash
# iOS profiling (Leaks template)
xcrun xctrace record \
  --template "Leaks" \
  --device "${DEVICE_ID}" \
  --attach "${BUNDLE_ID}" \
  --output memory-leaks.trace \
  --time-limit 300s

# Parse leaked allocations
xcrun xctrace export \
  --input memory-leaks.trace \
  --xpath '//row[column[@name="leaked"]="true"]' \
  --output leaks.xml

# Check leak count
leaked_allocs=$(jq '.memory.leaked_allocations' reports/performance-metrics.json)

if [ "$leaked_allocs" -eq 0 ]; then
    echo "QG-PERF-004: PASS (0 leaked allocations)"
    exit 0
else
    echo "QG-PERF-004: FAIL ($leaked_allocs leaked allocations)"
    jq '.memory.leaked_allocations_list' reports/performance-metrics.json
    exit 1
fi
```

**Why This Matters**: Memory leaks cause app crashes and degrade performance over time.

**Common Leak Sources**:
- Retain cycles (iOS Swift/Obj-C)
- Missing unsubscribe (RxJava, Combine, Kotlin Flow)
- Static references to Views/Activities
- Timers not invalidated

**Reference**: See `templates/skills/native-profiling.md` for leak detection patterns

---

### QG-PERF-005: Battery Drain < 5%/hour

**Level**: SHOULD (for mobile apps)
**Applies to**: iOS, Android, KMP, Flutter, React Native
**Phase**: Pre-Release (optional, requires 60+ minute profiling)

Mobile applications SHOULD consume less than 5% battery per hour during moderate usage.

**Threshold**: < 5% battery drain per hour

**Validation**:
```bash
# iOS profiling (requires physical device + idevice_battery tool)
initial_battery=$(idevice_battery -u "${DEVICE_ID}" | grep "Capacity:" | awk '{print $2}')
xcrun simctl launch "${DEVICE_ID}" "${BUNDLE_ID}"
sleep 3600  # 1 hour
final_battery=$(idevice_battery -u "${DEVICE_ID}" | grep "Capacity:" | awk '{print $2}')

battery_drain=$((initial_battery - final_battery))

if [ "$battery_drain" -lt 5 ]; then
    echo "QG-PERF-005: PASS ($battery_drain% < 5%/hour)"
    exit 0
else
    echo "QG-PERF-005: FAIL ($battery_drain% >= 5%/hour)"
    exit 1
fi
```

**Why This Matters**: Battery drain is a top complaint in app store reviews.

**Common Battery Drains**:
- Excessive network polling (use push notifications instead)
- GPS location services running in background
- CPU-intensive background tasks
- Excessive animations

**Note**: Battery profiling requires physical device and extended time (60+ minutes). Can be skipped for rapid iteration, but MUST be validated before release.

**Reference**: See `templates/skills/native-profiling.md` for battery profiling patterns

---

### Performance Gate Summary (Mobile Apps)

**Integration**:
- **Agent**: performance-profiler-agent
- **Skill**: `native-profiling`
- **Command**: `/speckit.mobile` Phase 6 OR `/speckit.analyze --profile performance`
- **MQS Impact**: Contributes 17-20/20 points to Performance component

**Automated Profiling Scripts**:
- `scripts/bash/mobile-profile.sh` — iOS/Android profiling wrapper
- `scripts/bash/unity-profiler-export.sh` — Unity profiler exporter
- `scripts/powershell/Mobile-Profile.ps1` — Windows Android profiling

**Tool Tiers**:
- **Tier 1 (Ideal)**: Full automation with native tools (Xcode Instruments, Android Profiler)
- **Tier 2 (Fallback)**: CLI-based automation (xcrun xctrace, adb shell dumpsys)
- **Tier 3 (Manual)**: Provide manual profiling instructions

**Reference**: See `templates/skills/native-profiling.md` for comprehensive profiling patterns

---

## Game Economy Balance Gates (QG-ECONOMY-xxx)

> **Game Economy Balance Gates** ensure F2P game economies are fair, balanced, and free from pay-to-win mechanics.
> Uses Monte Carlo simulation to validate wealth distribution, inflation, F2P progression, and competitive balance.

**Integration**:
- **Agent**: game-economist-agent
- **Skill**: economy-simulation
- **Command**: `/speckit.analyze --profile game-economy`
- **Applicable**: `is_game_project AND has_economy_design`
- **Platforms**: Unity, Godot, native game engines

### QG-ECONOMY-001: Gini Coefficient < 0.6

**Level**: MUST (for F2P games with virtual economies)
**Phase**: Post-economy-simulation
**Severity**: HIGH
**Description**: Wealth inequality across player population must be within acceptable bounds (Gini coefficient < 0.6)

**Threshold**: Gini coefficient < 0.6 (moderate inequality acceptable in F2P games)

**Check**:
```bash
# Via /speckit.analyze
specify analyze --profile game-economy

# Check Gini in report
cat reports/economy-simulation-report.md | grep "Gini Coefficient"
# Expected: "Gini Coefficient: 0.52 ✅ PASS"

# Or check JSON metrics
gini=$(jq '.gini_coefficient.value' reports/economy-metrics.json)
if (( $(echo "$gini < 0.6" | bc -l) )); then
    echo "QG-ECONOMY-001: PASS (Gini = $gini)"
else
    echo "QG-ECONOMY-001: FAIL (Gini = $gini, threshold < 0.6)"
fi
```

**Rationale**:
- Gini = 0 → perfect equality (unrealistic, kills monetization)
- Gini < 0.6 → moderate inequality (whales have more, but F2P can progress)
- Gini > 0.6 → high inequality (F2P feel powerless, churn increases)
- Gini = 1 → perfect inequality (one player has everything, broken economy)

**Example Pass**:
```
Gini Coefficient: 0.52 ✅

Wealth Distribution (Day 90):
- F2P median: 4,500 gems
- Whale median: 450,000 gems
- Whale/F2P ratio: 100x (acceptable within Gini < 0.6)

Interpretation: Moderate wealth inequality. Whales have significantly more resources, but F2P players can still progress meaningfully.
```

**Example Fail**:
```
Gini Coefficient: 0.82 ❌ (threshold < 0.6)

Issue: Extreme wealth inequality
Root Cause: F2P earn rate too low (10 gems/day vs whale 10,000/day)

Recommendation: Increase F2P gem earn rate from 10 to 50 gems/day
Expected Impact: Reduce Gini from 0.82 to ~0.55
```

---

### QG-ECONOMY-002: Inflation < 10% per Month

**Level**: SHOULD (becomes MUST for games with >6 month retention targets)
**Phase**: Post-economy-simulation
**Severity**: MEDIUM
**Description**: Currency value decay over time must be within acceptable bounds (< 10% per month)

**Threshold**: Inflation rate < 10% per month

**Check**:
```bash
# Via /speckit.analyze
specify analyze --profile game-economy

# Check inflation in report
cat reports/economy-simulation-report.md | grep "Inflation Rate"
# Expected: "Inflation Rate: 8.3%/month ✅ PASS"

# Or check JSON metrics
inflation=$(jq '.inflation_rate.value' reports/economy-metrics.json)
if (( $(echo "$inflation < 10" | bc -l) )); then
    echo "QG-ECONOMY-002: PASS (Inflation = $inflation%)"
else
    echo "QG-ECONOMY-002: FAIL (Inflation = $inflation%, threshold < 10%)"
fi
```

**Rationale**:
- Inflation < 5% → Very stable economy (risk: not enough pressure to spend)
- Inflation 5-10% → Healthy economy (players feel progress, some urgency)
- Inflation > 10% → High inflation (player frustration, "treadmill" feeling)
- Inflation > 20% → Hyperinflation (game feels broken, mass churn)

**Calculation**:
```
Inflation = (Week4_Cost - Week1_Cost) / Week1_Cost * 100%

Where:
- Week1_Cost = Average upgrade cost at day 7
- Week4_Cost = Average upgrade cost at day 28
```

**Example Pass**:
```
Inflation Rate: 8.3%/month ✅

Calculation:
- Week 1 average upgrade cost: 10,000 gold
- Week 4 average upgrade cost: 10,830 gold
- Inflation: (10,830 - 10,000) / 10,000 = 8.3%

Interpretation: Currency value is stable. Incremental power creep is within acceptable bounds.
```

**Example Fail**:
```
Inflation Rate: 15.2%/month ❌ (threshold < 10%)

Issue: Excessive currency inflation
Root Cause: Upgrade costs scale exponentially (cost = base * 2^level)

Recommendation: Switch to linear scaling (cost = base * (1 + level * 0.1))
Expected Impact: Reduce inflation from 15.2% to ~7.5%
```

---

### QG-ECONOMY-003: F2P Milestones Reachable

**Level**: MUST (for all F2P games)
**Phase**: Post-economy-simulation
**Severity**: CRITICAL
**Description**: All major progression milestones must be reachable by F2P players within reasonable time budgets

**Threshold**: 100% of milestones reachable by F2P within time budgets

**Time Budget Guidelines**:
- **Early game** (Level 1-10): < 14 days
- **Mid game** (Level 11-30): < 60 days
- **Late game** (Level 31+): < 180 days

**Check**:
```bash
# Via /speckit.analyze
specify analyze --profile game-economy

# Check milestone reachability in report
cat reports/economy-simulation-report.md | grep -A10 "F2P Milestone Reachability"

# Expected output:
# | Milestone | Time Budget | Median F2P Time | Status |
# | Level 10  | 7 days      | 6.2 days       | ✅ PASS |
# | Unlock Raid | 30 days  | 28.5 days      | ✅ PASS |

# Or check JSON metrics
jq '.f2p_milestones' reports/economy-metrics.json
```

**Rationale**:
- F2P path to all content = fair, ethical monetization
- No F2P path = hard paywall = unethical, regulatory risk
- Unreasonable time budgets (e.g., 1 year for mid-game) = soft paywall = unethical

**Example Pass**:
```
F2P Milestone Reachability: ✅ PASS

| Milestone | Time Budget | Median F2P Time | Status |
|-----------|-------------|-----------------|--------|
| Level 10  | 7 days      | 6.2 days       | ✅ PASS |
| Unlock Raid | 30 days  | 28.5 days      | ✅ PASS |
| Level 30  | 45 days     | 42.1 days      | ✅ PASS |

Interpretation: All milestones reachable by F2P within reasonable time. No hard paywalls detected.
```

**Example Fail**:
```
F2P Milestone Reachability: ❌ FAIL

| Milestone | Time Budget | Median F2P Time | Status |
|-----------|-------------|-----------------|--------|
| Level 10  | 7 days      | 6.2 days       | ✅ PASS |
| Unlock Raid | 30 days  | 58.3 days      | ❌ FAIL |

Issue: "Unlock Raid" milestone unreachable within time budget
Root Cause: Power requirement (2000) too high for F2P progression rate

Recommendation: Reduce power requirement from 2000 to 1500, OR increase F2P gem earn rate
Expected Impact: F2P median time reduced to ~28 days
```

---

### QG-ECONOMY-004: No Pay-to-Win in PvP

**Level**: MUST (for games with competitive PvP modes)
**Phase**: Post-economy-simulation
**Severity**: CRITICAL
**Description**: Whale players must not have overwhelming power advantage in PvP modes. Skill should remain a significant factor.

**Threshold**: Whale power gap < 2.0x compared to F2P at same time investment

**Check**:
```bash
# Via /speckit.analyze
specify analyze --profile game-economy

# Check P2W analysis in report
cat reports/economy-simulation-report.md | grep -A10 "Pay-to-Win Analysis"

# Expected output:
# PvP Power Gap (30-day comparison):
# - F2P median power: 2,500
# - Whale median power: 4,800
# - Power gap ratio: 1.92x ✅ PASS

# Or check JSON metrics
power_gap=$(jq '.p2w_analysis.power_gap_30d' reports/economy-metrics.json)
if (( $(echo "$power_gap < 2.0" | bc -l) )); then
    echo "QG-ECONOMY-004: PASS (Power gap = ${power_gap}x)"
else
    echo "QG-ECONOMY-004: FAIL (Power gap = ${power_gap}x, threshold < 2.0x)"
fi
```

**Rationale**:
- Power gap < 1.5x → Very balanced (whales have minimal advantage)
- Power gap 1.5-2.0x → Acceptable balance (skill matters, whales have edge)
- Power gap > 2.0x → Pay-to-win (whales dominate, F2P can't compete)
- Power gap > 5.0x → Extreme P2W (broken competitive balance)

**Additional Checks**:
1. **Exclusive PvP Content**: No PvP-critical features locked behind paywall
2. **Skill Factor**: At least 30% of PvP outcome determined by player skill
3. **Matchmaking**: Power-based brackets to prevent mismatches

**Example Pass**:
```
Pay-to-Win Analysis: ✅ PASS

PvP Power Gap (30-day comparison):
- F2P median power: 2,500
- Whale median power: 4,800
- Power gap ratio: 1.92x ✅ (< 2.0x threshold)

Skill Factor: 30% (player skill can overcome 30% power disadvantage)

Exclusive Content Check:
- ✅ All PvP modes accessible to F2P
- ✅ No PvP-critical items locked behind paywall
- ✅ Matchmaking uses power brackets (±20%)

Interpretation: Whales have an advantage, but not overwhelming. Skilled F2P players can compete in same power bracket.
```

**Example Fail**:
```
Pay-to-Win Analysis: ❌ FAIL

PvP Power Gap (30-day comparison):
- F2P median power: 2,500
- Whale median power: 12,000
- Power gap ratio: 4.8x ❌ (threshold < 2.0x)

Exclusive Content Issues:
- ❌ Best character (SSR tier) only obtainable via $99.99 pack
- ❌ PvP power scaling is exponential (favors whales excessively)

Root Cause:
1. Exclusive characters locked behind paywall
2. Exponential power scaling amplifies spending advantage

Recommendations:
1. Make all characters earnable (F2P path with 60-90 day grind)
2. Switch from exponential to linear power scaling
3. Increase skill factor from 20% to 40%

Expected Impact: Reduce power gap from 4.8x to ~1.8x
```

---

### Quality Gate Summary (Game Economy)

| Gate ID | Description | Level | Severity | Threshold |
|---------|-------------|-------|----------|-----------|
| QG-ECONOMY-001 | Gini Coefficient | MUST | HIGH | < 0.6 |
| QG-ECONOMY-002 | Inflation Rate | SHOULD | MEDIUM | < 10%/month |
| QG-ECONOMY-003 | F2P Milestones | MUST | CRITICAL | 100% reachable |
| QG-ECONOMY-004 | No P2W in PvP | MUST | CRITICAL | Power gap < 2.0x |

**Integration with /speckit.analyze**:
```bash
# Run economy validation
specify analyze --profile game-economy

# Output artifacts:
# - reports/economy-simulation-report.md (human-readable)
# - reports/economy-metrics.json (machine-readable)

# Check all gates
grep "QG-ECONOMY-" reports/economy-simulation-report.md

# Expected output:
# QG-ECONOMY-001: PASS (Gini = 0.52)
# QG-ECONOMY-002: PASS (Inflation = 8.3%)
# QG-ECONOMY-003: PASS (All milestones reachable)
# QG-ECONOMY-004: PASS (Power gap = 1.92x)
```

**Economic Health Score**:
```
Score = (Gate Passes / Total Gates) * 100 + Bonuses

Bonuses:
- Gini < 0.5: +5 (very balanced)
- Inflation < 5%: +5 (very stable)
- F2P can reach endgame: +5 (excellent retention)
- No P2W detected: +5 (ethical monetization)

Max Score: 120/100 (with all bonuses)
Target Score: ≥ 80/100
```

**Monte Carlo Simulation Parameters**:
- **Simulations**: 10,000 per archetype (F2P, dolphin, whale)
- **Duration**: 90 days (early to mid-game focus)
- **Archetypes**: F2P ($0/month), dolphin ($25/month), whale ($500/month)
- **Variance**: ±20% daily earnings to model real player behavior

**Reference**: See `templates/skills/economy-simulation.md` for comprehensive simulation framework

---

## Component Integration Gates (QG-COMP-xxx)

> **Component Integration Quality Gates** ensure UI components are not just created but actually integrated into all target screens.
> Prevents "orphan components" - components that exist but are never used in navigation.

### QG-COMP-001: Component Registration

**Level**: MUST (for UI features with Component Registry)
**Applies to**: All `/speckit.tasks` outputs for features with UI Component Registry
**Phase**: Pre-Implement

Every component creation task in Phase 2b MUST have a `[COMP:COMP-xxx]` marker linking to Component Registry.

**Threshold**: 100% of Phase 2b component tasks have [COMP:] markers

**Validation**:
```bash
# Parse tasks.md Phase 2b, extract component creation tasks
# Verify each has [COMP:COMP-xxx] marker
# Verify COMP-xxx exists in spec.md Component Registry
```

**Implementation**:
```
FOR EACH task IN Phase_2b_tasks:
  IF task.description contains "Create.*Component" OR ".*View" OR ".*Button":
    IF NOT task.markers contains "[COMP:COMP-xxx]":
      ERROR: "Component task missing [COMP:] marker: {task}"
    IF NOT Component_Registry contains task.COMP_id:
      ERROR: "COMP-{id} not found in Component Registry"
```

**Violations**: HIGH - Component not traceable to spec

---

### QG-COMP-002: Wire Task Coverage

**Level**: MUST (for UI features with Component Registry)
**Applies to**: All `/speckit.tasks` outputs for features with UI Component Registry
**Phase**: Pre-Implement

Every (Component, Target Screen) pair from Component Registry MUST have a corresponding wire task.

**Threshold**: 100% of (Component, Target Screen) pairs have [WIRE:] tasks

**Validation**:
```bash
/speckit.analyze --profile component-coverage
# Output: CSIM coverage: X/Y pairs have wire tasks (Z%)
```

**Implementation**:
```
FOR EACH comp IN Component_Registry:
  FOR EACH screen_id IN comp.Target_Screens:
    FIND task with marker "[WIRE:{comp.id}→{screen_id}]"
    IF NOT FOUND:
      ERROR: "Missing wire task: {comp.id} → {screen_id}"
      ERROR: "Add: - [ ] TXXX [WIRE:{comp.id}→{screen_id}] Wire {comp.name} into {screen.name}"
```

**CSIM Matrix Validation**:
```
CSIM_PAIRS = Component_Registry × Screen_Registry (via Target_Screens)
WIRE_TASKS = tasks with [WIRE:*] markers
COVERAGE = len(WIRE_TASKS) / len(CSIM_PAIRS) × 100

IF COVERAGE < 100%:
  BLOCK: "CSIM coverage {COVERAGE}% < 100%. Missing wire tasks for:"
  FOR EACH missing_pair:
    OUTPUT: "  - {comp.name} → {screen.name}"
```

**Violations**: CRITICAL - Components will not appear in navigation screens

---

### QG-COMP-003: Screen Component Completeness

**Level**: MUST (for UI features with Screen Registry)
**Applies to**: All `/speckit.tasks` outputs for features with Screen Registry
**Phase**: Pre-Implement

Every screen MUST have wire tasks for ALL its Required Components (from Screen Registry).

**Threshold**: 100% of screens have wire tasks for all Required Components

**Validation**:
```bash
/speckit.analyze --profile screen-completeness
# Output: Screen coverage: X/Y screens fully wired (Z%)
```

**Implementation**:
```
FOR EACH screen IN Screen_Registry:
  FOR EACH comp_id IN screen.Required_Components:
    FIND task with marker "[WIRE:{comp_id}→{screen.id}]"
    IF NOT FOUND:
      ERROR: "{screen.name} missing wire task for {comp_id}"
```

**Violations**: CRITICAL - Screen will show placeholders instead of components

---

### QG-COMP-004: No Orphan Components (Post-Implement)

**Level**: MUST (for UI features)
**Applies to**: `/speckit.analyze` QA mode after implementation
**Phase**: Post-Implement

Every completed wire task MUST result in actual component usage in the screen file.

**Threshold**: 100% of completed [WIRE:] tasks have import AND usage in screen

**Validation**:
```bash
/speckit.analyze --profile qa --check orphan-components
# Output: Orphan detection: X/Y wire tasks verified (Z%)
```

**Implementation** (code-level validation):
```
FOR EACH wire_task WHERE status = "[x]":
  comp_file = resolve from [COMP:{comp_id}] task
  screen_file = resolve from [SCREEN:{screen_id}] task

  # Check import
  SCAN screen_file for import of comp_file
  IF NOT FOUND:
    CRITICAL: "Missing import: {comp_name} not imported in {screen_file}"

  # Check usage
  SCAN screen_file for usage of component (function call, JSX tag, Compose call)
  IF NOT FOUND:
    CRITICAL: "Orphan component: {comp_name} imported but not used in {screen_file}"

  # Check for placeholders
  SCAN screen_file for placeholder patterns:
    - Text("...placeholder...")
    - Text("{screen_name}")  # e.g., Text("Settings")
    - TODO:, FIXME: in render body
    - EmptyView(), Spacer() where component should be
  IF FOUND:
    WARNING: "Placeholder detected in {screen_file}: {pattern}"
```

**Violations**: CRITICAL - Tasks marked complete but integration not done

---

## Plan Mode Gates (PM-xxx)

> **Plan Mode Quality Gates** ensure exploration and review phases meet quality standards when Plan Mode is enabled (depth levels 1-3).

### PM-001: Exploration Phase Completeness

**Level**: MUST (blocking)
**Phase**: Phase 0 (Exploration)
**Applies to**: All commands with depth level ≥ 1

All exploration agents must complete successfully with valid outputs.

**Threshold**: 100% of required agents completed with valid outputs

**Required Agents by Depth Level**:
- **Depth 1 (Lite)**: pattern-researcher, constraint-mapper
- **Depth 2-3 (Moderate/Full)**: pattern-researcher, alternative-analyzer, constraint-mapper, best-practice-synthesizer

**Validation**:
```python
def validate_exploration_completeness(depth_level, research_md):
    required_agents = {
        1: ["pattern-researcher", "constraint-mapper"],
        2: ["pattern-researcher", "alternative-analyzer", "constraint-mapper", "best-practice-synthesizer"],
        3: ["pattern-researcher", "alternative-analyzer", "constraint-mapper", "best-practice-synthesizer"]
    }

    agents = required_agents[depth_level]

    # Check pattern-researcher
    IF NOT research_md.has_section("Existing Patterns"):
        FAIL: "pattern-researcher did not complete"
    IF research_md.get_pattern_count() < 1:
        FAIL: "pattern-researcher found no patterns"

    # Check constraint-mapper (depth 1+)
    IF depth_level >= 1:
        IF NOT research_md.has_section("Constraint Map"):
            FAIL: "constraint-mapper did not complete"
        nfrs_mapped = research_md.get_nfr_count()
        IF nfrs_mapped == 0:
            WARN: "No NFRs mapped (feature may have no NFRs)"

    # Check alternative-analyzer (depth 2+)
    IF depth_level >= 2:
        IF NOT research_md.has_section("Alternative Approaches"):
            FAIL: "alternative-analyzer did not complete"
        alternatives = research_md.get_alternatives()
        IF len(alternatives) < 3:
            FAIL: "alternative-analyzer generated < 3 alternatives"

    # Check best-practice-synthesizer (depth 2+)
    IF depth_level >= 2:
        IF NOT research_md.has_section("Synthesis & Recommendation"):
            FAIL: "best-practice-synthesizer did not complete"
        IF NOT research_md.has_recommendation():
            FAIL: "No recommendation provided"

    RETURN "PM-001: PASS"
```

**Severity**: CRITICAL

**Violations**:
- CRITICAL: Any required agent failed or timed out
- CRITICAL: Missing required sections in research.md
- WARNING: 0 patterns found (may indicate empty codebase)

**Graceful Fallback**: On failure, log warning and fall back to standard mode (depth 0)

---

### PM-002: Alternative Analysis Quality

**Level**: MUST (blocking)
**Phase**: Phase 0 (Exploration)
**Applies to**: Commands with depth level ≥ 2

Alternative approaches must include ≥3 options with complete scoring matrix.

**Threshold**: ≥3 alternatives with 5-dimensional scores

**Validation**:
```python
def validate_alternative_quality(research_md):
    alternatives = research_md.get_alternatives()

    IF len(alternatives) < 3:
        FAIL: "Only {len(alternatives)} alternatives generated (minimum: 3)"

    # Check each alternative has required fields
    FOR EACH alt IN alternatives:
        REQUIRE: alt.name
        REQUIRE: alt.description
        REQUIRE: alt.pros (list, ≥1 item)
        REQUIRE: alt.cons (list, ≥1 item)
        REQUIRE: alt.score (dict with 5 keys)

        # Validate scoring dimensions
        required_dimensions = ["complexity", "testability", "maintainability", "performance", "alignment"]
        FOR EACH dim IN required_dimensions:
            IF dim NOT IN alt.score:
                FAIL: "Alternative '{alt.name}' missing score dimension: {dim}"
            IF NOT (1 <= alt.score[dim] <= 5):
                FAIL: "Alternative '{alt.name}' score '{dim}' out of range [1-5]: {alt.score[dim]}"

        # Calculate aggregate score (0-25)
        alt.aggregate_score = sum(alt.score.values())

    # Check recommendation
    recommended = research_md.get_recommended_approach()
    IF NOT recommended:
        FAIL: "No recommended approach specified"

    # Validate recommendation is highest-scoring OR has justification
    highest_score = max([alt.aggregate_score for alt in alternatives])
    IF recommended.aggregate_score < highest_score:
        IF NOT recommended.justification:
            WARN: "Recommended approach not highest-scoring and no justification provided"

    RETURN "PM-002: PASS"
```

**Severity**: CRITICAL

**Violations**:
- CRITICAL: < 3 alternatives generated
- CRITICAL: Missing scoring dimensions
- CRITICAL: Scores out of valid range [1-5]
- WARNING: Recommended approach not highest-scoring without justification

---

### PM-003: Constraint Conflict Resolution

**Level**: SHOULD (non-blocking)
**Phase**: Phase 0 (Exploration)
**Applies to**: Commands with depth level ≥ 1

All NFR conflicts must be detected and resolved.

**Threshold**: 0 unresolved CRITICAL conflicts

**Validation**:
```python
def validate_constraint_conflicts(research_md):
    constraint_map = research_md.get_constraint_map()

    # Check if conflicts section exists
    IF NOT constraint_map.has_section("Conflicts Detected"):
        # No conflicts detected is acceptable
        RETURN "PM-003: PASS (no conflicts detected)"

    conflicts = constraint_map.get_conflicts()

    FOR EACH conflict IN conflicts:
        REQUIRE: conflict.severity IN ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        REQUIRE: conflict.description
        REQUIRE: conflict.nfr_a
        REQUIRE: conflict.nfr_b

        # Check resolution
        IF conflict.severity == "CRITICAL":
            IF NOT conflict.resolution:
                FAIL: "CRITICAL conflict unresolved: {conflict.description}"
            IF NOT conflict.resolution_rationale:
                WARN: "CRITICAL conflict resolution lacks rationale"

        ELIF conflict.severity == "HIGH":
            IF NOT conflict.resolution:
                WARN: "HIGH severity conflict unresolved: {conflict.description}"

    RETURN "PM-003: PASS"
```

**Severity**:
- CRITICAL for unresolved CRITICAL conflicts
- WARNING for unresolved HIGH conflicts

**Violations**:
- CRITICAL: Unresolved CRITICAL conflicts block implementation
- WARNING: Unresolved HIGH conflicts may cause issues

---

### PM-004: Review Pass Compliance

**Level**: MUST (blocking)
**Phase**: Phase 2 (Review)
**Applies to**: Commands with depth level ≥ 2

All review passes must complete with 0 CRITICAL failures.

**Threshold**: 0 CRITICAL failures across all review passes

**Review Passes by Depth Level**:
- **Depth 2 (Moderate)**: constitution_alignment only
- **Depth 3 (Full)**: constitution_alignment, completeness_check, edge_case_detection, testability_audit

**Validation**:
```python
def validate_review_compliance(depth_level, review_results):
    required_passes = {
        2: ["constitution_alignment"],
        3: ["constitution_alignment", "completeness_check", "edge_case_detection", "testability_audit"]
    }

    passes = required_passes[depth_level]

    FOR EACH pass_name IN passes:
        result = review_results.get_pass_result(pass_name)

        IF NOT result:
            FAIL: "Review pass '{pass_name}' did not complete"

        IF result.status == "FAIL" AND result.severity == "CRITICAL":
            FAIL: "CRITICAL failure in {pass_name}: {result.violations}"

        ELIF result.status == "FAIL" AND result.severity == "HIGH":
            WARN: "HIGH severity failure in {pass_name}: {result.violations}"

    RETURN "PM-004: PASS"
```

**Pass Definitions**:

1. **constitution_alignment** (CRITICAL)
   - All tech stack choices in `constitution.allowed_stack`
   - No security anti-patterns (hardcoded secrets, SQL injection)
   - Dependencies in `constitution.approved_dependencies`

2. **completeness_check** (HIGH)
   - FR coverage ≥ 90% (all FRs addressed in plan/spec)
   - NFR coverage ≥ 90% (all NFRs have measurable criteria)
   - All AS-xxx scenarios have test strategy

3. **edge_case_detection** (HIGH)
   - Pre-Mortem has ≥ 3 failure scenarios
   - Each API call has error handling strategy
   - Data validation for all user inputs

4. **testability_audit** (MEDIUM)
   - Each FR has measurable acceptance criteria
   - Each NFR has measurement method
   - Test doubles/mocks strategy defined for external deps
   - Observability: SLIs, SLOs, alerts defined

**Severity**:
- CRITICAL for constitution_alignment failures
- HIGH for completeness_check and edge_case_detection failures
- MEDIUM for testability_audit failures

**Violations**:
- CRITICAL: Constitution violations block workflow
- HIGH: Completeness/edge case failures log warnings
- MEDIUM: Testability issues log warnings

**Block Behavior**: Only CRITICAL failures block workflow

---

### PM-005: Edge Case Coverage

**Level**: SHOULD (non-blocking)
**Phase**: Phase 2 (Review)
**Applies to**: Commands with depth level ≥ 3

Pre-Mortem section must identify ≥3 edge cases/failure scenarios.

**Threshold**: ≥3 edge cases identified

**Validation**:
```python
def validate_edge_case_coverage(review_results, complexity_tier):
    edge_case_result = review_results.get_pass_result("edge_case_detection")

    IF NOT edge_case_result:
        # Pass not run (depth level < 3)
        RETURN "PM-005: SKIP (not applicable)"

    # Extract edge cases from Pre-Mortem section
    edge_cases = extract_edge_cases_from_pre_mortem(spec_md, plan_md)

    IF len(edge_cases) < 3:
        IF complexity_tier == "COMPLEX":
            FAIL: "Only {len(edge_cases)} edge cases identified (minimum: 3 for COMPLEX features)"
        ELSE:
            WARN: "Only {len(edge_cases)} edge cases identified (recommended: 3+)"

    # Validate edge case quality
    FOR EACH case IN edge_cases:
        REQUIRE: case.description
        REQUIRE: case.impact IN ["HIGH", "MEDIUM", "LOW"]
        REQUIRE: case.mitigation

        IF NOT case.mitigation:
            WARN: "Edge case '{case.description}' lacks mitigation strategy"

    # Check coverage types
    technical_cases = [c for c in edge_cases if c.type == "technical"]
    integration_cases = [c for c in edge_cases if c.type == "integration"]

    IF len(technical_cases) == 0:
        WARN: "No technical edge cases identified"
    IF len(integration_cases) == 0:
        WARN: "No integration edge cases identified"

    RETURN "PM-005: PASS"
```

**Severity**:
- CRITICAL if 0 edge cases AND complexity tier = COMPLEX
- WARNING if < 3 edge cases

**Violations**:
- CRITICAL: No edge cases for COMPLEX features blocks workflow
- WARNING: < 3 edge cases logged but not blocking

---

### PM-006: Quality Score Threshold

**Level**: MUST (blocking)
**Phase**: Phase 3 (Finalize)
**Applies to**: Commands with depth level ≥ 2

Aggregate quality score must meet minimum threshold.

**Threshold**: ≥80 for COMPLEX features, ≥70 for MODERATE features

**Quality Score by Command**:
- `/speckit.plan`: PQS (Plan Quality Score, 0-100)
- `/speckit.specify`: SQS (Spec Quality Score, 0-100)
- `/speckit.concept`: CQS (Concept Quality Score, 0-120)

**Validation**:
```python
def validate_quality_score(command, complexity_tier, quality_score):
    # Determine threshold based on complexity
    thresholds = {
        "TRIVIAL": 60,
        "SIMPLE": 65,
        "MODERATE": 70,
        "COMPLEX": 80
    }

    threshold = thresholds[complexity_tier]

    # Get score name
    score_names = {
        "speckit.plan": "PQS",
        "speckit.specify": "SQS",
        "speckit.concept": "CQS"
    }
    score_name = score_names.get(command, "Quality Score")

    IF quality_score < threshold:
        IF complexity_tier == "COMPLEX":
            FAIL: "{score_name} = {quality_score} < {threshold} (COMPLEX threshold)"
        ELSE:
            WARN: "{score_name} = {quality_score} < {threshold} ({complexity_tier} threshold)"

    RETURN "PM-006: PASS ({score_name} = {quality_score})"
```

**Severity**:
- CRITICAL if score < threshold AND complexity tier = COMPLEX
- WARNING if score < threshold AND complexity tier ≠ COMPLEX

**Violations**:
- CRITICAL: Below-threshold score for COMPLEX features blocks workflow
- WARNING: Below-threshold score for other features logged

**Score Calculation**: See respective command templates (plan.md, specify.md, concept.md) for scoring rubrics

---

## UI Testing Gates (QG-UI-xxx)

> **UI Testing Quality Gates** ensure 100% coverage of UI acceptance scenarios with E2E tests and validate that UI tests pass with self-healing auto-fix loops.

### QG-UI-001: UI Test Coverage

**Level**: MUST (blocking)
**Applies to**: All `/speckit.tasks` outputs for features with UI components
**Phase**: Pre-Implement (tasks.md validation)

Every acceptance scenario (AS-xxx) with UI components MUST have a corresponding E2E test task.

**Threshold**: 100% of AS-xxx with UI components have [E2E-TEST:AS-xxx] or [UI-TEST:AS-xxx] markers

**Validation**:
```bash
/speckit.analyze --profile ui-test-coverage
```

**Formula**: `(AS with [E2E-TEST:] markers) / (AS with "Requires UI Test = YES") × 100`

**Implementation**:
```
# Step 1: Parse spec.md for AS-xxx with UI keywords
UI_AS = detect_ui_acceptance_scenarios(spec_md)

# Step 2: Parse tasks.md for E2E test tasks
E2E_TASKS = extract_tasks_with_markers(tasks_md, "[E2E-TEST:", "[UI-TEST:")

# Step 3: Calculate coverage
FOR EACH as_id IN UI_AS:
  IF NOT EXISTS task WHERE task.markers CONTAINS "[E2E-TEST:{as_id}]":
    ERROR: "Missing E2E test for UI scenario: {as_id}"

coverage = (len(E2E_TASKS) / len(UI_AS)) × 100
IF coverage < 100:
  FAIL QG-UI-001
```

**Severity**: CRITICAL

**Violations**: CRITICAL - UI scenarios not covered by E2E tests

---

### QG-UI-002: All UI Tests Pass

**Level**: MUST
**Applies to**: All `/speckit.implement` executions
**Phase**: Post-Implement (Wave 4)

All UI E2E tests MUST pass after auto-fix attempts (2 attempts for basic mode, 3 for advanced mode).

**Threshold**: 100% of UI tests pass (after auto-fix loop)

**Validation**:
```bash
# Playwright (Web/Electron)
npm test -- --testPathPattern=e2e

# XCUITest (iOS)
xcodebuild test -scheme UITests -destination 'platform=iOS Simulator,name=iPhone 15 Pro'

# Espresso (Android)
./gradlew connectedAndroidTest

# Maestro (Cross-platform mobile)
maestro test .maestro/
```

**Implementation**:
```python
# In Wave 4 of /speckit.implement
ui_test_results = []

FOR EACH test_task IN ui_test_tasks:
  result = await _verify_ui_test_and_heal(
    test_task=test_task,
    mode=ui_autofix_config.mode  # "basic" or "advanced"
  )
  ui_test_results.append(result)

passed = [r for r in ui_test_results if r.success]
failed = [r for r in ui_test_results if not r.success]

IF len(failed) > 0:
  FAIL QG-UI-002 with details:
    - Total tests: len(ui_test_results)
    - Passed: len(passed)
    - Failed: len(failed)
    - Failed tests: [f.test_file for f in failed]
```

**Severity**: CRITICAL

**Violations**: CRITICAL - UI tests failing block feature completion

---

### QG-UI-003: No Hardcoded Waits

**Level**: SHOULD
**Applies to**: All UI test code
**Phase**: Post-Implement (code analysis)

UI tests MUST NOT use hardcoded waits (sleep, delay, setTimeout). Use explicit waits (waitFor, waitForSelector) instead.

**Threshold**: 0 hardcoded waits in test code

**Validation**: Regex scan for hardcoded wait patterns

**Patterns** (language-specific):
```yaml
javascript/typescript:
  - "setTimeout\\("
  - "setInterval\\("
  - "\\.sleep\\("
  - "await page\\.waitForTimeout\\("  # Playwright discouraged pattern

python:
  - "time\\.sleep\\("
  - "sleep\\("

swift:
  - "Thread\\.sleep\\("
  - "usleep\\("

kotlin/java:
  - "Thread\\.sleep\\("
  - "SystemClock\\.sleep\\("
```

**Implementation**:
```bash
# Scan all test files for hardcoded waits
rg "(setTimeout|sleep|waitForTimeout)" tests/e2e/ --type js --type ts
rg "time\.sleep" tests/e2e/ --type py
rg "Thread\.sleep" tests/ --type swift --type kotlin --type java

IF matches_found > 0:
  WARN QG-UI-003 with locations
```

**Severity**: HIGH

**Violations**: HIGH - Hardcoded waits cause flaky tests

**Remediation**:
```typescript
// ❌ Bad
await page.waitForTimeout(2000);
await page.click('button');

// ✅ Good
await page.waitForSelector('button[data-testid="submit"]', { state: 'visible' });
await page.click('button[data-testid="submit"]');
```

---

### UI Testing Gates Summary

| Gate ID | Phase | Level | Threshold | Validation | Severity |
|---------|-------|-------|-----------|------------|----------|
| QG-UI-001 | Pre-Implement | MUST | 100% UI AS with E2E tasks | [E2E-TEST:] check | CRITICAL |
| QG-UI-002 | Post-Implement | MUST | 100% UI tests pass | Test execution | CRITICAL |
| QG-UI-003 | Post-Implement | SHOULD | 0 hardcoded waits | Regex scan | HIGH |

---

### Component Integration Gates Summary

| Gate ID | Phase | Level | Threshold | Validation | Violation |
|---------|-------|-------|-----------|------------|-----------|
| QG-COMP-001 | Pre-Implement | MUST | 100% markers | [COMP:] check | HIGH |
| QG-COMP-002 | Pre-Implement | MUST | 100% pairs | CSIM coverage | CRITICAL |
| QG-COMP-003 | Pre-Implement | MUST | 100% screens | Screen completeness | CRITICAL |
| QG-COMP-004 | Post-Implement | MUST | 100% wired | Orphan detection | CRITICAL |

---

## Pre-Implement Gates

### QG-001: Minimum Spec Quality Score

**Level**: MUST
**Applies to**: All `/speckit.implement` invocations

Implementation MUST NOT begin until Spec Quality Score (SQS) reaches minimum threshold.

**Threshold**: SQS >= 80

**SQS Rubric v2.0** (25 checkpoints across 5 dimensions):

| Dimension | Points | Key Checkpoints |
|-----------|--------|-----------------|
| **Clarity** | 25 | RFC 2119 keywords, no vague terms, specific numbers, measurable success, defined failures |
| **Completeness** | 25 | FRs documented, NFRs specified, edge cases, dependencies, security |
| **Testability** | 25 | Each FR has AC, concrete scenarios, performance metrics, error conditions, integration points |
| **Traceability** | 15 | Unique IDs, concept cross-refs, feature dependencies, FR→AC→Test chain, no orphans |
| **No Ambiguity** | 10 | No hedge words, terms defined, clarifications resolved, scope explicit, assumptions documented |

**Formula**: `SQS = Clarity + Completeness + Testability + Traceability + NoAmbiguity`

**Full Rubric**: See [templates/shared/quality/sqs-rubric.md](../../templates/shared/quality/sqs-rubric.md)

**Validation**:
```bash
/speckit.analyze --profile sqs
# Output: SQS: 85/100 (Clarity: 22, Complete: 23, Test: 20, Trace: 12, Ambig: 8)
```

**Thresholds**:
- **≥80**: Ready for implementation
- **60-79**: Needs improvement (run `/speckit.clarify`)
- **<60**: Major rework required (block implementation)

**Violations**: CRITICAL - Spec not ready, implementation will fail or drift

---

### QG-002: Security Scan Pass

**Level**: MUST
**Applies to**: All projects with dependencies

All dependencies MUST pass security vulnerability scan with no critical or high severity issues.

**Threshold**: 0 critical/high vulnerabilities

**Implementation**:
```bash
# Node.js
npm audit --audit-level=high

# Python
pip-audit --strict

# Go
govulncheck ./...
```

**Validation**: Exit code 0 from security scanner
**Violations**: CRITICAL - Known vulnerabilities before implementation

---

### QG-003: Dependency Freshness

**Level**: SHOULD
**Applies to**: All projects with external dependencies

Dependencies SHOULD NOT be more than 2 major versions behind current stable release.

**Threshold**: No critical dependencies > 2 major versions behind

**Implementation**:
```bash
# Node.js
npx npm-check-updates

# Python
pip list --outdated

# Check for critical deps only (React, Express, Django, etc.)
```

**Validation**: Review output for major version gaps
**Violations**: HIGH - Technical debt, missing security patches

---

## Post-Implement Gates

### QG-004: Test Coverage

**Level**: MUST
**Applies to**: All production code

Code MUST have minimum test coverage threshold enforced in CI.

**Threshold**: >= 80% line coverage

**Implementation**:
```bash
# Jest (Node.js)
jest --coverage --coverageThreshold='{"global":{"lines":80}}'

# Pytest (Python)
pytest --cov=src --cov-fail-under=80

# Go
go test -coverprofile=coverage.out && go tool cover -func=coverage.out
```

**Coverage Report Parsing**:
```typescript
// Parse lcov or coverage-summary.json
const coverage = JSON.parse(fs.readFileSync('coverage/coverage-summary.json'));
if (coverage.total.lines.pct < 80) {
  throw new Error(`Coverage ${coverage.total.lines.pct}% below 80% threshold`);
}
```

**Validation**: Coverage report shows >= 80%
**Violations**: CRITICAL - Untested code paths may contain bugs

---

### QG-005: Type Coverage

**Level**: MUST
**Applies to**: TypeScript, Python with type hints

Code MUST have static type annotations covering specified threshold.

**Threshold**: >= 95% type coverage

**Implementation**:
```bash
# TypeScript
npx type-coverage --at-least 95

# Python (mypy)
mypy src/ --strict --ignore-missing-imports

# Python (pyright)
pyright --verifytypes src
```

**Validation**: Type coverage tool reports >= 95%
**Violations**: HIGH - Runtime type errors risk

---

### QG-006: Lint Cleanliness

**Level**: MUST
**Applies to**: All source code

Code MUST pass linting with zero errors and minimal warnings.

**Threshold**: 0 errors, < 10 warnings

**Implementation**:
```bash
# TypeScript/JavaScript
eslint src/ --max-warnings 10

# Python
ruff check src/ --fix

# Go
golangci-lint run
```

**Validation**: Linter exit code 0 with warning count < 10
**Violations**: HIGH - Code quality issues, inconsistent style

---

### QG-007: Performance Baseline

**Level**: SHOULD
**Applies to**: User-facing web applications

Web applications SHOULD meet Lighthouse performance score threshold.

**Threshold**: Lighthouse Performance >= 90

**Implementation**:
```bash
# Lighthouse CI
lighthouse http://localhost:3000 --only-categories=performance --output=json

# Parse result
jq '.categories.performance.score * 100' lighthouse-report.json
```

**Metrics Checked**:
- First Contentful Paint < 1.8s
- Largest Contentful Paint < 2.5s
- Total Blocking Time < 200ms
- Cumulative Layout Shift < 0.1

**Validation**: Lighthouse performance score >= 90
**Violations**: MEDIUM - Poor user experience, SEO impact

---

### QG-008: Accessibility Compliance

**Level**: SHOULD
**Applies to**: User-facing web applications

Web applications SHOULD meet WCAG 2.1 Level AA accessibility standards.

**Threshold**: Zero WCAG 2.1 AA violations

**Implementation**:
```bash
# axe-core via CLI
npx @axe-core/cli http://localhost:3000

# Lighthouse accessibility
lighthouse http://localhost:3000 --only-categories=accessibility

# Playwright with axe
await expect(page).toHaveNoViolations();
```

**Key Checks**:
- Color contrast ratios
- Keyboard navigation
- Screen reader compatibility
- Focus management
- Alt text for images

**Validation**: axe-core or Lighthouse reports 0 violations
**Violations**: MEDIUM - Accessibility barriers for users

---

### QG-009: Documentation Coverage

**Level**: SHOULD
**Applies to**: Public APIs and library code

All public APIs SHOULD have documentation coverage.

**Threshold**: 100% of public exports documented

**Implementation**:
```bash
# TypeScript (TypeDoc)
typedoc --validation.notDocumented

# Python (pydocstyle)
pydocstyle src/ --convention=google

# JSDoc coverage
npx jsdoc-coverage src/
```

**Documentation Requirements**:
- Function/method descriptions
- Parameter types and descriptions
- Return value documentation
- Usage examples for complex APIs

**Validation**: Documentation coverage tool reports 100% public API coverage
**Violations**: LOW - Maintainability and onboarding impact

---

## Verification Gates (QG-VERIFY-xxx)

> **Post-Implementation Verification** gates ensure complete validation across all layers after implementation.
> See `templates/commands/verify.md` for the `/speckit.verify` command.

### QG-VERIFY-001: Acceptance Criteria Coverage

**Level**: MUST
**Applies to**: All features with acceptance scenarios
**Phase**: Post-Implement

Every AS-xxx scenario from spec.md MUST have a corresponding test task with [TEST:AS-xxx] marker.

**Threshold**: 100% coverage of acceptance scenarios with tests

**Validation**:
```bash
/speckit.verify
# OR manually:
# Parse spec.md for AS-xxx scenarios
# Parse tasks.md for [TEST:AS-xxx] markers
# Coverage = (scenarios with tests) / (total scenarios) × 100
```

**Formula**:
```
AS Test Coverage = (AS with [TEST:] markers) / (Total AS scenarios) × 100
```

**Violations**: CRITICAL - Untested acceptance scenarios
**Remediation**: Create test tasks for missing scenarios: {{missing_scenarios}}

---

### QG-VERIFY-002: Acceptance Criteria Pass Rate

**Level**: MUST
**Applies to**: All features with test scenarios
**Phase**: Post-Implement

At least 90% of acceptance criteria tests MUST pass.

**Threshold**: >= 90% test pass rate

**Validation**:
```bash
/speckit.verify
# Runs all tests marked with [TEST:AS-xxx]
# Calculates: (passing tests) / (total tests) × 100
```

**Thresholds**:
- **≥90%**: Ready to proceed
- **80-89%**: Warning - fix remaining issues
- **<80%**: BLOCK - too many failures

**Violations**: CRITICAL - Only {{pass_rate}}% of AC tests passing (threshold: 90%)
**Remediation**: Fix failing tests: {{failing_scenarios}}

---

### QG-VERIFY-003: API Contract Compliance

**Level**: HIGH
**Applies to**: Features with API endpoints
**Phase**: Post-Implement

All API endpoints MUST match spec.md contract definitions.

**Threshold**: 100% contract compliance (no undocumented drift)

**Validation**:
```bash
/speckit.verify
# Parses Gherkin "When I [METHOD] [ENDPOINT]" steps
# Tests actual API against expected request/response schemas
# Detects: missing fields, extra fields, type mismatches, status code diffs
```

**Contract Checks**:
- Request schema matches spec
- Response schema matches spec
- Status codes match spec
- No undocumented fields in responses

**Violations**: HIGH - {{drift_count}} API endpoints have contract drift
**Remediation**: Update spec or fix implementation for: {{drifted_endpoints}}

---

### QG-VERIFY-004: Visual Regression Threshold

**Level**: HIGH
**Applies to**: UI features with Visual YAML specifications
**Phase**: Post-Implement

Visual diff between baseline and current screenshots MUST be < 5% for all screens.

**Threshold**: >= 95% screens pass (< 5% visual diff)

**Validation**:
```bash
/speckit.verify
# Uses Playwright for screenshots
# Uses pixelmatch for pixel comparison
# Generates diff images with highlights
```

**Diff Thresholds**:
- **0-1%**: PASS (negligible diff)
- **1-5%**: WARN (minor drift, may be acceptable)
- **>5%**: FAIL (significant visual change)

**Violations**: HIGH - {{fail_count}} screens have >5% visual diff
**Remediation**: Review visual diffs: {{failed_screens}}

**Update Baselines**:
```bash
# After intentional UI changes
/speckit.verify --baseline
```

---

### QG-VERIFY-005: Behavior Verification

**Level**: MUST
**Applies to**: All features with user flows
**Phase**: Post-Implement

All user flows from spec.md MUST work end-to-end as specified.

**Threshold**: 100% behavior correctness

**Validation**:
```bash
/speckit.verify
# Runs E2E tests for multi-step scenarios
# Verifies: navigation, state persistence, cross-page flows
```

**Behavior Checks**:
- Redirects work as expected
- State persists across pages
- Multi-step flows complete successfully
- Error handling works correctly

**Violations**: CRITICAL - {{fail_count}} behaviors not working as specified
**Remediation**: Fix behaviors: {{failed_behaviors}}

---

### QG-VERIFY-006: NFR Compliance

**Level**: MEDIUM
**Applies to**: Features with non-functional requirements
**Phase**: Post-Implement

At least 80% of non-functional requirements (NFRs) MUST be met.

**Threshold**: >= 80% NFR compliance

**Validation**:
```bash
/speckit.verify
# Runs Lighthouse for performance
# Runs axe-core for accessibility
# Checks bundle size, test coverage, security scan
```

**NFR Categories**:
- **Performance**: Lighthouse score >= 90, LCP < 2.5s, bundle size targets
- **Accessibility**: WCAG 2.1 AA compliance, axe-core scan clean
- **Security**: No critical/high vulnerabilities, secret scanning clean
- **Coverage**: >= 80% test coverage

**Thresholds**:
- **≥80%**: Ready to proceed
- **60-79%**: Warning - optimization recommended
- **<60%**: BLOCK - significant NFR failures

**Violations**: MEDIUM - {{fail_count}} NFRs not met
**Remediation**: Optimize: {{failed_nfrs}}

---

### Verification Gate Summary

| Gate ID | Phase | Level | Threshold | Validation | Severity |
|---------|-------|-------|-----------|------------|----------|
| QG-VERIFY-001 | Post-Implement | MUST | 100% coverage | AS test markers | CRITICAL |
| QG-VERIFY-002 | Post-Implement | MUST | >= 90% pass | Test results | CRITICAL |
| QG-VERIFY-003 | Post-Implement | HIGH | 100% compliance | API contract check | HIGH |
| QG-VERIFY-004 | Post-Implement | HIGH | >= 95% pass | Visual diff | HIGH |
| QG-VERIFY-005 | Post-Implement | MUST | 100% correct | E2E behavior | CRITICAL |
| QG-VERIFY-006 | Post-Implement | MEDIUM | >= 80% met | NFR checks | MEDIUM |

---

## Pre-Deploy Gates

### QG-010: All Tests Pass

**Level**: MUST
**Applies to**: All deployments

Deployment MUST NOT proceed if any test fails.

**Threshold**: 100% test pass rate

**Implementation**:
```bash
# Run full test suite
npm test
pytest
go test ./...

# Check exit code
if [ $? -ne 0 ]; then
  echo "Tests failed - blocking deployment"
  exit 1
fi
```

**Test Categories**:
- Unit tests
- Integration tests
- E2E tests (if applicable)
- Contract tests (if applicable)

**Validation**: Test runner exit code 0
**Violations**: CRITICAL - Broken functionality will reach production

---

### QG-011: No Debug Artifacts

**Level**: MUST
**Applies to**: Production builds

Production code MUST NOT contain debug statements or development artifacts.

**Threshold**: 0 debug artifacts found

**Forbidden Patterns**:
```bash
# JavaScript/TypeScript
console.log
console.debug
console.warn (review case-by-case)
debugger
alert(

# Python
print(  # in non-CLI code
pdb.set_trace()
breakpoint()
import pdb

# General
TODO
FIXME
HACK
XXX
```

**Implementation**:
```bash
# Check for debug statements
grep -rn "console\.log\|debugger" src/ --include="*.ts" --include="*.tsx"

# Check for development markers
grep -rn "TODO\|FIXME\|HACK\|XXX" src/
```

**Validation**: grep returns no matches
**Violations**: HIGH - Information leakage, unfinished code in production

---

### QG-012: Environment Documentation

**Level**: MUST
**Applies to**: All deployable applications

All required environment variables MUST be documented in `.env.example`.

**Threshold**: 100% env var documentation coverage

**Implementation**:
```bash
#!/bin/bash
# scripts/check-env-coverage.sh

# Find all env var references in code
CODE_ENVS=$(grep -roh "process\.env\.\w\+" src/ | sort -u | sed 's/process\.env\.//')

# Find documented env vars
DOC_ENVS=$(grep -oh "^\w\+=" .env.example | sed 's/=//' | sort -u)

# Find undocumented
UNDOC=$(comm -23 <(echo "$CODE_ENVS") <(echo "$DOC_ENVS"))

if [ -n "$UNDOC" ]; then
  echo "Undocumented environment variables:"
  echo "$UNDOC"
  exit 1
fi
```

**Documentation Format** (`.env.example`):
```bash
# Database connection (required)
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Redis cache (optional, defaults to in-memory)
REDIS_URL=

# Feature flags
FEATURE_NEW_UI=false
```

**Validation**: All runtime env vars present in .env.example
**Violations**: HIGH - Deployment failures, configuration drift

---

## Mobile Game Quality Gates (QG-GAME-xxx)

Эти гейты активны только когда `constitution.domain.md` содержит `gaming.md + mobile.md` (мобильные игры).

### QG-GAME-001: Frame Rate Stability

**Level**: MUST
**Threshold**: 60 FPS ±5 on iPhone 11 (2019) / Galaxy S10 (2019)
**Phase**: Post-Implementation (Wave 4)

**Description**: Игра должна поддерживать стабильные 60 FPS на mid-tier устройствах (iPhone 11, Galaxy S10). Frame time budget: 16.67ms.

**Validation**:
- **Unity Profiler**: CPU time <14ms, GPU time <14ms per frame
- **Xcode Instruments**: Game Performance template, 10-minute continuous gameplay
- **Android GPU Inspector**: Frame time histogram, 95th percentile <18ms
- **Automated**: CI runs profiler on device farm, fails if <55 FPS

**Metrics**:
- Avg FPS: ≥58
- 1% low FPS: ≥50
- Frame drops (>20ms): <1% of frames

**Violations**: HIGH - Poor FPS = negative reviews, refunds

**References**: GAM-001 (Frame Rate Stability)

---

### QG-GAME-002: Battery Efficiency

**Level**: MUST
**Threshold**: ≤5% battery drain per hour of active gameplay
**Phase**: Pre-Deployment (Wave 5)

**Description**: Игра не должна быстро разряжать батарею. Target: <5% в час активной игры.

**Validation**:
- **Xcode Energy Log**: Run 1-hour gameplay session, measure battery delta
- **Android Battery Historian**: Upload bugreport, check power consumption
- **Formula**: `Battery Drain % = (Start % - End %) / (Minutes Played / 60)`
- **Device**: Test on real devices (not simulator/emulator)

**Metrics**:
- Battery drain: ≤5%/hour
- CPU usage: <30% avg
- GPU usage: <50% avg (60 FPS target allows 50% headroom for battery)

**Common Issues**:
- Polling instead of push (WebSocket vs HTTP polling)
- Rendering off-screen objects
- High GC pressure (memory allocations)

**Violations**: MEDIUM - Negative reviews ("drains battery"), user uninstalls

**References**: MOB-003 (Battery Efficiency)

---

### QG-GAME-003: App Size Compliance

**Level**: MUST
**Threshold**: IPA/AAB <150MB before App Thinning
**Phase**: Pre-Deployment (Wave 5)

**Description**: Initial download size должен быть <150MB (iOS cellular limit). Android Play Store рекомендация: <150MB для AAB.

**Validation**:
- **Build Report**: Unity Build Report, Xcode Archive Organizer
- **Command**: `ls -lh build/Game.ipa` (iOS), `ls -lh build/Game.aab` (Android)
- **Asset Profiler**: Identify largest assets (textures, audio)

**Optimization Strategies**:
- Texture compression (ASTC for mobile)
- Audio compression (Vorbis, AAC)
- On-Demand Resources (iOS) / Play Asset Delivery (Android)
- Code stripping (remove unused code)

**Metrics**:
- iOS IPA: <150MB (before App Thinning, after typically <100MB)
- Android AAB: <150MB (Play Store generates optimized APKs per device)

**Violations**: MEDIUM - Won't download over cellular, limits installs

**References**: MOB-002 (Platform Compliance), gaming.md line 243 (mobile app size <150MB)

---

### QG-GAME-004: Input Latency

**Level**: MUST
**Threshold**: <80ms touch-to-visual for mobile games
**Phase**: Post-Implementation (Wave 4)

**Description**: Input latency (touch → visual response) должен быть <80ms для mobile games. Action games: <50ms ideal, casual: <100ms acceptable.

**Validation**:
- **High-Speed Camera**: Record 240fps video, count frames from touch to visual change
- **Formula**: `Latency (ms) = (Frame Count / 240) * 1000`
- **Automated**: WALT Latency Timer (hardware tool)

**Common Sources of Latency**:
- Input polling at end of frame (should be start of frame)
- Render pipeline latency (V-Sync, triple buffering)
- Main thread blocking (UI, physics on main thread)

**Genre Targets**:
- Hyper-casual: <80ms (acceptable)
- Casual: <100ms (acceptable)
- Mid-core: <70ms (good)
- Core (competitive): <50ms (must)

**Violations**: HIGH - Poor game feel, "laggy" complaints, competitive disadvantage

**References**: GAM-002 (Input Latency), gaming.md line 242 (mobile <80ms)

---

### QG-GAME-005: Monetization Ethics

**Level**: MUST (if IAP or ads present)
**Checklist**: All items must pass
**Phase**: Pre-Deployment (Wave 5)

**Description**: Monetization должна соответствовать этическим стандартам и региональным законам (loot box disclosure, no dark patterns).

**Checklist**:
- [ ] **Transparent Pricing**: Real currency prices shown alongside virtual currency (e.g., "500 Gems ($4.99)")
- [ ] **Loot Box Disclosure**: Drop rates disclosed (required by Apple/Google) if gacha/loot boxes present
- [ ] **No Pay-to-Win in PvP**: Competitive modes don't allow direct power purchase
- [ ] **Spending Limits**: Daily/weekly spending caps or parental controls implemented
- [ ] **Regional Compliance**:
  - Belgium/Netherlands: No loot boxes (banned)
  - Japan: Kompu gacha banned, drop rates disclosed
  - EU: GDPR compliance, no data from <16 without parental consent
  - US: COPPA compliance, no data from <13 without parental consent
- [ ] **Ad Frequency Cap**: Max 1 interstitial per 5 minutes, rewarded video unlimited (user-initiated)
- [ ] **No Dark Patterns**:
  - No hidden costs (show real prices)
  - No fake countdown timers (timers must be real)
  - No confirm-shaming ("No thanks, I don't want free stuff")
  - No forced continuity (trials clearly marked, easy cancellation)

**Validation**:
- **Policy Review**: Manual checklist against App Store + Play Store guidelines
- **Regional Testing**: Test in Belgium (loot boxes disabled), Japan (drop rates shown)
- **Ethics Review**: "Would you let your child play this monetization model?"

**Violations**: CRITICAL - Store removal, legal action, player backlash, PR crisis

**References**: GAM-004 (Fair Monetization), gaming.md lines 93-108

---

## Quality Gate Summary (Mobile Games)

| Gate ID | Threshold | Severity | Phase | Validation Method |
|---------|-----------|----------|-------|-------------------|
| QG-GAME-001 | 60 FPS ±5 | HIGH | Post-Impl (Wave 4) | Unity Profiler, Instruments |
| QG-GAME-002 | ≤5%/hour battery | MEDIUM | Pre-Deploy (Wave 5) | Energy Log, Battery Historian |
| QG-GAME-003 | <150MB | MEDIUM | Pre-Deploy (Wave 5) | Build report, ls -lh |
| QG-GAME-004 | <80ms latency | HIGH | Post-Impl (Wave 4) | High-speed camera (240fps) |
| QG-GAME-005 | All checklist ✅ | CRITICAL | Pre-Deploy (Wave 5) | Manual policy review |

**When Active**: Only when `domains: [gaming, mobile]` present in constitution

**Enforcement**: `/speckit.implement` runs QG-GAME-001, 004 in Wave 4; QG-GAME-002, 003, 005 in Wave 5

**Skip**: `--skip-gates` flag bypasses (not recommended for production)

---

## Game Progression Quality Gates (QG-PROGRESSION-xxx)

> **Progression Design Quality** gates ensure game progression specifications (levels, difficulty curves, unlock gates, meta-progression) meet player engagement and retention standards.
> **Active**: Only when `/speckit.games.progression` command is executed
> **Applied by**: validator-exporter-agent (Phase 5) during progression design

These gates validate that game progression design follows best practices from Flow Theory (Csikszentmihalyi) and game economy principles.

### QG-PROGRESSION-001: Difficulty Slope Compliance

**Level**: CRITICAL
**Threshold**: 0.8 ≤ slope ≤ 1.2 between all adjacent levels
**Phase**: POST (during progression design validation)
**Severity**: CRITICAL

All adjacent level difficulty ratios MUST fall within valid range to ensure smooth player progression without frustration spikes or boredom drops.

**Formula**:
```python
slope = difficulty(level + 1) / difficulty(level)
valid_slope = 0.8 <= slope <= 1.2
```

**Interpretation**:
- **slope < 0.8**: Difficulty drops (regression, bad UX)
- **slope 0.8-1.0**: Plateau (acceptable for resting phases)
- **slope = 1.0**: Perfect continuity (ideal)
- **slope 1.0-1.2**: Smooth increase (optimal challenge growth)
- **slope > 1.2**: Sudden spike (frustration risk)

**Validation**:
```bash
# validator-exporter-agent calculates slopes during Phase 5
# Check all 199 slopes (for 200 levels)
slopes_in_range=$(jq '.validation.difficulty_slope.in_range_count' specs/games/progression.md)
total_slopes=$(jq '.validation.difficulty_slope.total_slopes' specs/games/progression.md)

if [ "$slopes_in_range" -eq "$total_slopes" ]; then
    echo "QG-PROGRESSION-001: PASS (100% slopes within 0.8-1.2)"
else
    violations=$((total_slopes - slopes_in_range))
    echo "QG-PROGRESSION-001: FAIL ($violations slopes outside range)"
    exit 1
fi
```

**Fixing Violations**:
1. Identify problematic levels (slopes > 1.2 or < 0.8)
2. Adjust difficulty formula parameters (base_difficulty, growth_rate)
3. Re-run `/speckit.games.progression` with adjusted parameters
4. Validate again until 100% compliance

**Related Gates**: QG-PROGRESSION-002 (Flow Channel must also be satisfied)

---

### QG-PROGRESSION-002: Flow Channel Compliance

**Level**: HIGH
**Threshold**: ≥95% of levels within Flow Channel (Challenge ≈ Skill ± 20%)
**Phase**: POST (during progression design validation)
**Severity**: HIGH

Player challenge MUST match player skill growth to maintain optimal engagement (Flow state). Levels outside the Flow Channel cause boredom (too easy) or anxiety (too hard).

**Flow Theory (Mihaly Csikszentmihalyi)**:
- **Flow Zone**: Challenge ≈ Skill ± 20% (optimal engagement)
- **Boredom Zone**: Challenge < Skill - 20% (disengagement)
- **Anxiety Zone**: Challenge > Skill + 20% (frustration)

**Formula**:
```python
skill = base_skill + (level * skill_growth_rate)
boredom_threshold = skill - (skill * 0.20)
anxiety_threshold = skill + (skill * 0.20)

in_flow = boredom_threshold <= difficulty <= anxiety_threshold
```

**Validation**:
```bash
# validator-exporter-agent calculates Flow Channel status for each level
flow_count=$(jq '.validation.flow_channel.in_flow_count' specs/games/progression.md)
total_levels=$(jq '.metadata.level_count' specs/games/progression.md)
flow_percentage=$(echo "scale=1; $flow_count * 100 / $total_levels" | bc)

if (( $(echo "$flow_percentage >= 95" | bc -l) )); then
    echo "QG-PROGRESSION-002: PASS ($flow_percentage% in Flow)"
else
    echo "QG-PROGRESSION-002: FAIL ($flow_percentage% < 95% threshold)"
    exit 1
fi
```

**Fixing Violations**:
1. **Boredom Zone levels**: Increase difficulty (adjust growth rate upward)
2. **Anxiety Zone levels**: Decrease difficulty (adjust growth rate downward)
3. **Skill growth model**: Adjust player skill growth rate to match challenge curve
4. Re-run `/speckit.games.progression` with adjusted parameters

**Related Gates**: QG-PROGRESSION-001 (Slope must also be smooth)

---

### QG-PROGRESSION-003: Level Count Minimum

**Level**: HIGH
**Threshold**: ≥ target level count (default: 200 for mid-core, 50 for hyper-casual)
**Phase**: POST (during progression design validation)
**Severity**: HIGH

Game MUST have sufficient content to meet genre expectations and retention targets.

**Genre Targets**:
| Genre | Minimum Levels | Rationale |
|-------|----------------|-----------|
| **Hyper-casual** | 50 | Short session, quick progression |
| **Casual** | 100 | Medium session, moderate progression |
| **Mid-core** | 200 | Long session, deep progression |
| **Hardcore** | 500+ | Very long session, competitive progression |
| **Idle** | Infinite | Endless progression with prestige |

**Validation**:
```bash
# Check level count matches target
actual_levels=$(jq '.metadata.level_count' specs/games/progression.md)
target_levels=$(jq '.metadata.target_level_count' specs/games/progression.md)

if [ "$actual_levels" -ge "$target_levels" ]; then
    echo "QG-PROGRESSION-003: PASS ($actual_levels ≥ $target_levels)"
else
    echo "QG-PROGRESSION-003: FAIL ($actual_levels < $target_levels)"
    exit 1
fi
```

**Fixing Violations**:
- Re-run `/speckit.games.progression` with increased `--level-count` flag

**Related Gates**: QG-PROGRESSION-004 (Unlock pacing must match level count)

---

### QG-PROGRESSION-004: Unlock Gate Pacing

**Level**: MEDIUM
**Threshold**: New mechanic/power-up/feature every 5-15 levels (≤5% gaps exceed 15)
**Phase**: POST (during progression design validation)
**Severity**: MEDIUM

New content MUST unlock at regular intervals to maintain player interest and prevent monotony.

**Pacing Guidelines**:
- **Wave 1 (Tutorial)**: Dense unlocks (every 2-3 levels) — rapid learning
- **Wave 2 (Core)**: Moderate unlocks (every 5-10 levels) — complexity introduction
- **Wave 3 (Mid)**: Slower unlocks (every 10-15 levels) — mastery phase
- **Wave 4 (Meta)**: Sparse unlocks (every 15-20 levels) — long-term systems
- **Wave 5 (Endgame)**: Very sparse unlocks (every 20-25 levels) — mastery rewards

**Validation**:
```bash
# Check gap distribution (unlock-schedule.md)
gaps_too_large=$(jq '.validation.unlock_gaps.gaps_exceeding_15' specs/games/unlock-schedule.md)
total_gaps=$(jq '.validation.unlock_gaps.total_gaps' specs/games/unlock-schedule.md)
gap_percentage=$(echo "scale=1; $gaps_too_large * 100 / $total_gaps" | bc)

if (( $(echo "$gap_percentage <= 5" | bc -l) )); then
    echo "QG-PROGRESSION-004: PASS ($gap_percentage% large gaps < 5% threshold)"
else
    echo "QG-PROGRESSION-004: FAIL ($gap_percentage% ≥ 5% threshold)"
    echo "Gaps exceeding 15 levels: $gaps_too_large/$total_gaps"
    exit 1
fi
```

**Fixing Violations**:
1. Identify gaps > 15 levels in unlock-schedule.md
2. Add intermediate unlocks at recommended levels
3. Re-run `/speckit.games.progression` with updated unlock schedule

**Related Gates**: QG-PROGRESSION-003 (Level count must be sufficient for pacing)

---

### QG-PROGRESSION-005: Meta-Progression Depth

**Level**: HIGH (if `--meta-depth` flag ≥ standard)
**Threshold**: Systems implemented match `--meta-depth` flag setting
**Phase**: POST (during progression design validation)
**Severity**: HIGH

Meta-progression systems MUST meet the specified depth level to ensure long-term retention and engagement.

**Depth Levels**:
| Level | Required Systems | Min Spec Lines | Retention Target |
|-------|------------------|----------------|------------------|
| **basic** | Prestige only | ~500 lines | D30: 10-15% |
| **standard** | Prestige + (Skill Tree OR Account Leveling) | ~1000 lines | D30: 20-30% |
| **deep** | Prestige + Skill Tree + Account Leveling + Ascension | ~1500 lines | D30: 30-40% |

**Validation**:
```bash
# Check meta-progression.md for required systems
target_depth=$(jq -r '.metadata.meta_depth' specs/games/progression.md)
has_prestige=$(grep -q "## 1. Prestige System" specs/games/meta-progression.md && echo "true" || echo "false")
has_skill_tree=$(grep -q "## 2. Skill Tree" specs/games/meta-progression.md && echo "true" || echo "false")
has_account_leveling=$(grep -q "## 3. Account Leveling" specs/games/meta-progression.md && echo "true" || echo "false")
has_ascension=$(grep -q "## 4. Ascension Mechanics" specs/games/meta-progression.md && echo "true" || echo "false")

case "$target_depth" in
    "basic")
        if [ "$has_prestige" = "true" ]; then
            echo "QG-PROGRESSION-005: PASS (basic: prestige present)"
        else
            echo "QG-PROGRESSION-005: FAIL (basic: prestige missing)"
            exit 1
        fi
        ;;
    "standard")
        if [ "$has_prestige" = "true" ] && ([ "$has_skill_tree" = "true" ] || [ "$has_account_leveling" = "true" ]); then
            echo "QG-PROGRESSION-005: PASS (standard: prestige + skill/account)"
        else
            echo "QG-PROGRESSION-005: FAIL (standard: missing systems)"
            exit 1
        fi
        ;;
    "deep")
        if [ "$has_prestige" = "true" ] && [ "$has_skill_tree" = "true" ] && [ "$has_account_leveling" = "true" ] && [ "$has_ascension" = "true" ]; then
            echo "QG-PROGRESSION-005: PASS (deep: all systems present)"
        else
            echo "QG-PROGRESSION-005: FAIL (deep: missing systems)"
            exit 1
        fi
        ;;
esac
```

**Fixing Violations**:
- Re-run `/speckit.games.progression` with correct `--meta-depth` flag
- Ensure meta-progression-agent completes all required sections

**Related Gates**: QG-PROGRESSION-003 (Sufficient levels for meta-progression unlocks)

---

### Summary: Game Progression Quality Gates Registry

| Gate ID | Threshold | Severity | Phase | Validation Method |
|---------|-----------|----------|-------|-------------------|
| QG-PROGRESSION-001 | 0.8-1.2 slope | CRITICAL | POST | Slope calculation |
| QG-PROGRESSION-002 | ≥95% in Flow | HIGH | POST | Flow Channel check |
| QG-PROGRESSION-003 | ≥ target count | HIGH | POST | Level count check |
| QG-PROGRESSION-004 | ≤5% gaps >15 | MEDIUM | POST | Unlock gap analysis |
| QG-PROGRESSION-005 | Match depth | HIGH | POST | Meta-system presence |

**When Active**: Only when `/speckit.games.progression` command is executed

**Enforcement**: All gates run automatically in Phase 5 by validator-exporter-agent

**Skip**: `--skip-gates` flag bypasses (not recommended for production)

**Integration with Other Gates**:
- QG-GAME-001 (Frame Rate) ← progression affects performance (more levels = more assets)
- QG-ART-001 (Art Quality) ← progression unlocks require art assets
- CQS (Concept Quality) ← progression design follows from concept requirements

---

## Game Art Pipeline Quality Gates (QG-ART-xxx)

> **Art Quality Score (AQS)** gates ensure game art specifications meet world-class standards before asset production begins.
> See `templates/shared/quality/aqs-rubric.md` for full 120-point rubric.
> **Active**: Only when `/speckit.design --game-art-pipeline` is executed

### QG-ART-001: Minimum Art Quality Score

**Level**: CRITICAL
**Threshold**: AQS ≥ 90/120 (75% of maximum, world-class tier)
**Phase**: Pre-Production (before asset creation begins)

Art pipeline MUST NOT begin asset production until Art Quality Score (AQS) reaches minimum threshold.

**AQS Rubric v1.0** (30 checkpoints across 6 dimensions):

| Dimension | Max Points | Key Checkpoints |
|-----------|------------|-----------------|
| **Visual Style** | 25 | Style guide, visual language, benchmarks, emotional tone, mobile adaptation |
| **Asset Completeness** | 25 | Catalog size (≥200), character coverage (≥20), environment coverage (≥10), UI library (≥100), variants/priority |
| **Animation Polish** | 20 | Frame rates, timing/easing, state machines, juiciness, ASMR integration |
| **VFX Believability** | 20 | Particle specs, screen effects, feedback hierarchy, performance budget (≤150), blend modes |
| **Audio Fidelity** | 15 | Material sounds (≥8), latency (<50ms), music integration, ASMR quality, spatial audio |
| **Performance Budget** | 15 | Texture memory (≤256MB), audio memory (≤64MB), polygon budget, draw calls (≤100), resolution tiers |

**Validation**:
```bash
# Calculate AQS from art pipeline output files
/speckit.analyze --profile aqs

# Check AQS score
aqs_score=$(jq '.aqs.total' reports/aqs-score.json)
if [ "$aqs_score" -ge 90 ]; then
    echo "QG-ART-001: PASS (AQS=$aqs_score/120)"
    exit 0
else
    echo "QG-ART-001: FAIL (AQS=$aqs_score/120 < 90 threshold)"
    jq '.aqs.dimensions' reports/aqs-score.json
    exit 1
fi
```

**Thresholds**:
- **≥95**: World-Class (AAA-quality production ready)
- **90-94**: Excellent (production ready with minor polish) ✅
- **80-89**: Good (address flagged dimensions)
- **70-79**: Needs Improvement (substantial rework required)
- **<70**: Not Ready (block production, major revision needed)

**Violations**: CRITICAL - Art production begins with subpar specifications

**Integration**:
- **Command**: `/speckit.design --game-art-pipeline`
- **Output Files**: `specs/games/art-spec.md`, `asset-catalog.md`, `animation-library.md`, `audio-requirements.md`
- **Handoff**: → `/speckit.tasks` (generate asset production tasks)

**Reference**: See `templates/shared/quality/aqs-rubric.md` for complete 30-checkpoint scoring system

---

### QG-ART-002: Asset Catalog Completeness

**Level**: HIGH
**Threshold**: ≥200 assets cataloged with unique IDs and technical specifications
**Phase**: Pre-Production

Asset catalog MUST contain minimum 200 assets across 6 categories with complete technical specs.

**Category Minimums**:
- **CHAR-xxx**: ≥20 character assets (player, enemies, NPCs)
- **ENV-xxx**: ≥10 environment assets (zones, tilesets, props)
- **PROP-xxx**: ≥20 prop assets (interactive, collectibles)
- **UI-xxx**: ≥100 UI elements (buttons, icons, panels)
- **VFX-xxx**: ≥20 VFX assets (combo, clear, explosion, ambient)
- **SFX-xxx**: ≥30 audio assets (UI sounds, gameplay, ambience)

**Validation**:
```bash
# Count assets in catalog
asset_count=$(grep -c "^[A-Z]+-[0-9]+" specs/games/asset-catalog.md)
if [ "$asset_count" -ge 200 ]; then
    echo "QG-ART-002: PASS ($asset_count assets ≥ 200)"
    exit 0
else
    echo "QG-ART-002: FAIL ($asset_count assets < 200 threshold)"
    exit 1
fi

# Verify category minimums
grep "^CHAR-" specs/games/asset-catalog.md | wc -l  # ≥20
grep "^UI-" specs/games/asset-catalog.md | wc -l    # ≥100
```

**Each Asset Must Include**:
- Unique ID (e.g., CHAR-001, UI-042)
- Name and description
- Type/category
- Technical specs (poly count, texture resolution, format)
- Priority (P0=MVP, P1=Soft Launch, P2=Full Launch)
- Status (pending, in-progress, complete)

**Violations**: HIGH - Incomplete asset planning leads to scope creep

**Integration**:
- **Agent**: asset-cataloger-agent
- **Output**: `specs/games/asset-catalog.md`

---

### QG-ART-003: Performance Budget Compliance

**Level**: CRITICAL
**Threshold**: Texture ≤256MB, Audio ≤64MB, Particles ≤150/frame
**Phase**: Pre-Production (budgets documented) + Post-Production (actual validation)

Art specifications MUST document performance budgets and final assets MUST comply with mobile platform constraints.

**Performance Budgets**:
| Resource | Mobile Target | Validation Method |
|----------|---------------|-------------------|
| Texture Memory | ≤256MB total | `find . -name "*.png" -o -name "*.jpg" \| xargs du -ch` |
| Audio Memory | ≤64MB total | `find . -name "*.ogg" -o -name "*.mp3" \| xargs du -ch` |
| Particles On-Screen | ≤150 simultaneous | Profiler measurement (combo 80, clear 60, UI 20, ambient 30) |
| Polygon Count | Characters ≤5K, Props ≤2K, Envs ≤10K/zone | Unity Asset Post-Processor |
| Draw Calls | ≤100 per frame | Frame Debugger |
| Resolution Tiers | @1x (512px), @2x (1024px), @3x (2048px) | Asset variants documented |

**Validation**:
```bash
# Check texture memory budget
texture_mb=$(find specs/games -name "*.png" -o -name "*.jpg" | xargs du -ch | tail -1 | awk '{print $1}')
if [ "$texture_mb" -le 256 ]; then
    echo "QG-ART-003: Texture memory PASS ($texture_mb MB ≤ 256MB)"
else
    echo "QG-ART-003: Texture memory FAIL ($texture_mb MB > 256MB)"
    exit 1
fi

# Check audio memory budget
audio_mb=$(find specs/games -name "*.ogg" -o -name "*.mp3" | xargs du -ch | tail -1 | awk '{print $1}')
if [ "$audio_mb" -le 64 ]; then
    echo "QG-ART-003: Audio memory PASS ($audio_mb MB ≤ 64MB)"
else
    echo "QG-ART-003: Audio memory FAIL ($audio_mb MB > 64MB)"
    exit 1
fi
```

**Platform Targets**:
- **High-end** (iPhone 14+): @3x textures, 150 particles, 60fps
- **Mid-tier** (iPhone 11-13): @2x textures, 100 particles, 60fps
- **Low-end** (iPhone X): @1x textures, 50 particles, 30fps

**Violations**: CRITICAL - Performance issues on target devices, negative reviews

**Integration**:
- **Agents**: visual-style-agent, vfx-designer-agent
- **Output**: Performance budgets in all art specification files

---

### QG-ART-004: Audio Latency Requirement

**Level**: HIGH
**Threshold**: <50ms from input to sound (UI: <20ms, Gameplay: <30ms)
**Phase**: Post-Production (manual validation with high-speed camera)

Audio latency MUST be <50ms total for ASMR-quality game feel. Critical for player satisfaction.

**Latency Targets by Category**:
| Sound Category | Max Latency | Priority | Test Method |
|----------------|-------------|----------|-------------|
| UI Tap | <20ms | CRITICAL | High-speed camera (240fps) |
| Gameplay Action | <30ms | HIGH | High-speed camera (240fps) |
| Feedback | <50ms | HIGH | Audio profiler |
| Music/Ambience | <100-200ms | MEDIUM | Acceptable streaming latency |

**Validation**:
```bash
# Manual validation with high-speed camera
# 1. Record UI button tap at 240fps
# 2. Count frames from touch to sound waveform visible
# 3. Calculate: Latency (ms) = (Frame Count / 240) * 1000

# Example: 4 frames = (4/240)*1000 = 16.7ms ✅ PASS (UI <20ms)
# Example: 8 frames = (8/240)*1000 = 33.3ms ❌ FAIL (UI >20ms)

# Automated profiler check (approximate)
/speckit.analyze --profile audio-latency
```

**ASMR Quality Requirements**:
- **Tactile**: Material-specific sounds (wood, metal, glass, stone, fabric, liquid, organic, magical)
- **Proximity**: High-fidelity recordings, binaural if possible
- **Precision**: Timing synchronized with animations (<50ms budget)
- **Satisfaction**: ASMR rating ≥4/5 for feedback sounds

**Optimization Strategies**:
- Preload critical sounds (UI, gameplay actions)
- Use uncompressed formats for UI sounds (<20ms)
- Streaming for music/ambience (acceptable latency)
- Low-latency audio codec for gameplay

**Violations**: HIGH - Poor game feel, "laggy" audio, dissatisfying interactions

**Integration**:
- **Agent**: audio-designer-agent
- **Output**: `specs/games/audio-requirements.md` with latency specs

**Reference**: Similar to QG-GAME-004 (Input Latency), but focused on audio feedback

---

### QG-ART-005: Visual Style Consistency

**Level**: HIGH
**Threshold**: 100% style guide compliance (colors, typography, icons)
**Phase**: Post-Production (visual audit after asset creation)

All assets MUST adhere to visual style guide specifications (color palette, typography, icon system).

**Consistency Checklist**:
- [ ] **Color Palette**: All assets use defined colors (no custom hex values)
- [ ] **Typography**: Font stack consistent across UI (title, body, numeric fonts)
- [ ] **Icon System**: Single icon library, consistent sizing (24px, 32px, 48px)
- [ ] **Art Style**: Unified visual language (no mixing realistic + cartoony)
- [ ] **Rendering Style**: Consistent shading model, outline style, shadows

**Validation**:
```bash
# Manual visual audit
# 1. Review all assets against art-spec.md color palette
# 2. Check typography consistency (no rogue fonts)
# 3. Verify icon system (single library, no mixed styles)

# Automated color palette check (if CSS/design tokens available)
grep -r "#[0-9a-fA-F]\{6\}" src/ | grep -v "design-tokens.css"
# Expected: 0 matches (all colors use tokens)

# Consistency score from analyze command
/speckit.analyze --profile aqs | jq '.aqs.dimensions.visual_style.consistency'
```

**Anti-Patterns** (AUTO-FAIL):
- ❌ Custom hex colors outside style guide
- ❌ Multiple icon libraries mixed (Material + FontAwesome)
- ❌ Inconsistent visual style (realistic characters, cartoony UI)
- ❌ Typography chaos (5+ different fonts)

**Violations**: HIGH - Unprofessional appearance, lack of visual cohesion

**Integration**:
- **Agent**: visual-style-agent
- **Output**: `specs/games/art-spec.md` with style guide

---

### QG-ART-006: Animation Frame Rate Compliance

**Level**: MEDIUM (SHOULD level)
**Threshold**: UI 60fps, Gameplay 30fps, Background 15-20fps
**Phase**: Post-Production (animation profiler)

Animations SHOULD meet frame rate targets for smooth playback and performance optimization.

**Frame Rate Standards**:
| Animation Category | Target FPS | Use Case | Battery Mode |
|-------------------|------------|----------|--------------|
| UI Animations | 60fps | Buttons, transitions, HUD | 60fps (no reduction) |
| Gameplay Animations | 30fps | Characters, enemies, actions | 30fps → 20fps |
| Background Animations | 15-20fps | Ambient effects, parallax | 15-20fps → 10fps |
| VFX (Particles) | 30-60fps | Explosions, combos, clears | 60fps → 30fps |

**Validation**:
```bash
# Unity Animation Profiler
# 1. Select animated asset
# 2. Check Animation Clip properties
# 3. Verify Sample Rate (FPS)

# Expected: UI animations at 60 samples/second
#           Gameplay animations at 30 samples/second

# Automated check (if animation metadata accessible)
/speckit.analyze --profile aqs | jq '.aqs.dimensions.animation_polish.frame_rate'
```

**Performance Benefits**:
- UI at 60fps: Smooth, responsive (required for good UX)
- Gameplay at 30fps: 50% less animation data, battery savings
- Background at 15-20fps: Minimal performance impact

**Violations**: MEDIUM (SHOULD level) - Not blocking, but degrades polish

**Integration**:
- **Agent**: animation-designer-agent
- **Output**: `specs/games/animation-library.md` with frame rate specs

---

## Quality Gate Summary (Game Art Pipeline)

| Gate ID | Threshold | Severity | Phase | Validation Method |
|---------|-----------|----------|-------|-------------------|
| QG-ART-001 | AQS ≥ 90/120 | CRITICAL | Pre-Production | `/speckit.analyze --profile aqs` |
| QG-ART-002 | ≥200 assets | HIGH | Pre-Production | `grep -c "^[A-Z]+-[0-9]+"` |
| QG-ART-003 | Texture ≤256MB, Audio ≤64MB, Particles ≤150 | CRITICAL | Pre-Production + Post-Production | `du -ch`, profiler |
| QG-ART-004 | Audio <50ms | HIGH | Post-Production | High-speed camera (240fps) |
| QG-ART-005 | 100% style consistency | HIGH | Post-Production | Manual visual audit |
| QG-ART-006 | UI 60fps, Gameplay 30fps | MEDIUM | Post-Production | Animation profiler |

**When Active**: Only when `/speckit.design --game-art-pipeline` is executed

**Enforcement**: Pre-production gates (QG-ART-001, 002, 003) MUST pass before `/speckit.tasks` handoff

**Skip**: `--skip-gates` flag bypasses (not recommended for production)

**Integration with Other Gates**:
- QG-ART-003 (Performance) ← relates to QG-GAME-001 (Frame Rate), QG-GAME-002 (Battery)
- QG-ART-004 (Audio Latency) ← relates to QG-GAME-004 (Input Latency)
- AQS ← complements CQS-Game (concept quality) and DQS (design quality)

---

## Security Gates (QG-SEC-xxx)

> **Security by Design** gates ensure security is embedded throughout the development lifecycle.
> See `memory/domains/security.md` for full Security by Design framework.

### QG-SEC-001: Threat Model Required

**Level**: MUST (for Confidential+ data classification)
**Applies to**: Features handling Confidential or Restricted data

A threat model MUST be completed before implementation begins for features handling sensitive data.

**Threshold**: `threat-model.md` exists with all STRIDE categories addressed

**Implementation**:
```bash
# Check threat model exists
ls .speckit/threat-model.md

# Validate STRIDE coverage
grep -c "### 4\.[1-6]" .speckit/threat-model.md  # Should return 6
```

**Validation**: Threat model file exists with complete STRIDE analysis
**Violations**: CRITICAL - Unknown security risks will reach production

---

### QG-SEC-002: OWASP Top 10 Addressed

**Level**: MUST
**Applies to**: All web applications and APIs

All applicable OWASP Top 10 vulnerabilities MUST have documented mitigations.

**Threshold**: Security checklist 100% complete for applicable items

**Implementation**:
```bash
# Check OWASP checklist completion
grep -c "\[x\]" .speckit/security-checklist.md
grep -c "\[ \]" .speckit/security-checklist.md  # Should be 0
```

**Validation**: All applicable OWASP checklist items marked complete
**Violations**: CRITICAL - Known vulnerability patterns not addressed

---

### QG-SEC-003: Dependency Scan Clean

**Level**: MUST
**Applies to**: All projects with dependencies

All dependencies MUST pass security vulnerability scan with no critical or high severity issues.

**Threshold**: 0 critical/high vulnerabilities

**Implementation**:
```bash
# Node.js
npm audit --audit-level=high

# Python
pip-audit --strict

# Go
govulncheck ./...

# Multi-language
snyk test --severity-threshold=high
```

**Validation**: Security scanner exit code 0
**Violations**: CRITICAL - Known vulnerable dependencies

---

### QG-SEC-004: Secret Scanning

**Level**: MUST
**Applies to**: All repositories

Codebase MUST NOT contain hardcoded secrets, API keys, or credentials.

**Threshold**: 0 secrets found in codebase

**Implementation**:
```bash
# Gitleaks
gitleaks detect --source . --verbose

# TruffleHog
trufflehog filesystem --directory=. --only-verified

# GitHub (if using)
gh secret scanning alerts list
```

**Validation**: Secret scanner reports 0 findings
**Violations**: CRITICAL - Credentials exposed in version control

---

### QG-SEC-005: Security Testing

**Level**: SHOULD
**Applies to**: Features with authentication or authorization

Security-critical flows SHOULD have dedicated security tests.

**Threshold**: Auth/authz tests exist and pass

**Implementation**:
```bash
# Check for security tests
find tests/ -name "*auth*" -o -name "*security*" | wc -l

# Run security-focused tests
npm test -- --grep "security\|auth"
pytest -k "security or auth"
```

**Coverage Requirements**:
- Authentication flows (login, logout, session)
- Authorization checks (role-based access)
- Input validation (injection prevention)
- Rate limiting behavior

**Validation**: Security tests exist and pass
**Violations**: MEDIUM - Untested security controls

---

## Gate Enforcement Matrix

| Gate | Phase | Level | Threshold | Validation Command | Severity |
|------|-------|-------|-----------|-------------------|----------|
| QG-COMP-001 | Pre-Implement | MUST | 100% markers | `/speckit.analyze --profile component-coverage` | HIGH |
| QG-COMP-002 | Pre-Implement | MUST | 100% pairs | `/speckit.analyze --profile component-coverage` | CRITICAL |
| QG-COMP-003 | Pre-Implement | MUST | 100% screens | `/speckit.analyze --profile screen-completeness` | CRITICAL |
| QG-COMP-004 | Post-Implement | MUST | 100% wired | `/speckit.analyze --profile qa --check orphan-components` | CRITICAL |
| QG-DQS-001 | Pre-Implement | MUST | DQS >= 70 | `/speckit.analyze --profile dqs` | HIGH |
| QG-DQS-002 | Pre-Implement | MUST | A11y >= 60% | `/speckit.analyze --profile dqs --dimension accessibility` | CRITICAL |
| QG-DQS-003 | Pre-Implement | MUST | WCAG AA | Contrast ratio validation | CRITICAL |
| QG-001 | Pre-Implement | MUST | SQS >= 80 | `/speckit.analyze --profile sqs` | CRITICAL |
| QG-002 | Pre-Implement | MUST | 0 critical | `npm audit --audit-level=high` | CRITICAL |
| QG-003 | Pre-Implement | SHOULD | < 2 major | `npx npm-check-updates` | HIGH |
| QG-004 | Post-Implement | MUST | >= 80% | `jest --coverage` | CRITICAL |
| QG-005 | Post-Implement | MUST | >= 95% | `npx type-coverage` | HIGH |
| QG-006 | Post-Implement | MUST | 0 errors | `npm run lint` | HIGH |
| QG-007 | Post-Implement | SHOULD | >= 90 | `lighthouse` | MEDIUM |
| QG-008 | Post-Implement | SHOULD | WCAG AA | `axe-core` | MEDIUM |
| QG-009 | Post-Implement | SHOULD | 100% public | TypeDoc coverage | LOW |
| QG-VERIFY-001 | Post-Implement | MUST | 100% coverage | `/speckit.verify` | CRITICAL |
| QG-VERIFY-002 | Post-Implement | MUST | >= 90% pass | `/speckit.verify` | CRITICAL |
| QG-VERIFY-003 | Post-Implement | HIGH | 100% compliance | `/speckit.verify` | HIGH |
| QG-VERIFY-004 | Post-Implement | HIGH | >= 95% pass | `/speckit.verify` | HIGH |
| QG-VERIFY-005 | Post-Implement | MUST | 100% correct | `/speckit.verify` | CRITICAL |
| QG-VERIFY-006 | Post-Implement | MEDIUM | >= 80% met | `/speckit.verify` | MEDIUM |
| QG-010 | Pre-Deploy | MUST | 100% pass | `npm test` | CRITICAL |
| QG-011 | Pre-Deploy | MUST | 0 found | grep patterns | HIGH |
| QG-012 | Pre-Deploy | MUST | 100% | env coverage script | HIGH |
| QG-GAME-001 | Post-Implement | MUST | 60 FPS ±5 | Unity Profiler / Instruments | HIGH |
| QG-GAME-002 | Pre-Deploy | MUST | ≤5%/hour | Energy Log / Battery Historian | MEDIUM |
| QG-GAME-003 | Pre-Deploy | MUST | <150MB | Build report / ls -lh | MEDIUM |
| QG-GAME-004 | Post-Implement | MUST | <80ms | High-speed camera (240fps) | HIGH |
| QG-GAME-005 | Pre-Deploy | MUST | All ✅ | Policy review checklist | CRITICAL |
| QG-PROGRESSION-001 | POST | MUST | 0.8-1.2 slope | Slope calculation | CRITICAL |
| QG-PROGRESSION-002 | POST | MUST | ≥95% in Flow | Flow Channel check | HIGH |
| QG-PROGRESSION-003 | POST | MUST | ≥ target count | Level count check | HIGH |
| QG-PROGRESSION-004 | POST | MUST | ≤5% gaps >15 | Unlock gap analysis | MEDIUM |
| QG-PROGRESSION-005 | POST | MUST | Match depth | Meta-system presence | HIGH |
| QG-SEC-001 | Pre-Implement | MUST | threat-model.md | STRIDE coverage check | CRITICAL |
| QG-SEC-002 | Pre-Implement | MUST | 100% checklist | OWASP checklist | CRITICAL |
| QG-SEC-003 | Pre-Deploy | MUST | 0 critical/high | `npm audit` / `pip-audit` | CRITICAL |
| QG-SEC-004 | Pre-Deploy | MUST | 0 secrets | `gitleaks` / `trufflehog` | CRITICAL |
| QG-SEC-005 | Post-Implement | SHOULD | tests exist | security test grep | MEDIUM |

---

## Migration Gates (QG-MIG-xxx)

> **Migration Quality Gates** ensure migration plans are safe and reversible before execution.
> See `templates/commands/migrate.md` for migration planning command.

### QG-MIG-001: Rollback Plan Required

**Level**: MUST
**Applies to**: All `/speckit.migrate` generated plans

Every migration phase (MIG-xxx) MUST have a documented rollback strategy.

**Threshold**: 100% of MIG-xxx phases have rollback procedures

**Validation**:
```bash
/speckit.analyze --profile migration
# Validates: Each MIG-xxx has rollback_strategy defined
```

**Rollback Types**:
| Type | Duration | Use Case |
|------|----------|----------|
| IMMEDIATE | < 5 min | Config changes, feature flags |
| GRADUAL | 10-30 min | Traffic shifting, API versioning |
| FULL | 30-60 min | Data migrations, schema changes |

**Violations**: CRITICAL - Migration without rollback is unrecoverable

---

### QG-MIG-002: Risk Mitigation Required

**Level**: MUST
**Applies to**: All migration plans with HIGH or CRITICAL risks

All HIGH (score ≥ 10) and CRITICAL (score ≥ 15) risks MUST have documented mitigations.

**Threshold**: 100% of HIGH+ risks have mitigation strategies

**Risk Score Calculation**: `probability (1-5) × impact (1-5)`

**Severity Levels**:
| Score | Severity | Mitigation Required |
|-------|----------|---------------------|
| 15-25 | CRITICAL | MUST (blocks planning) |
| 10-14 | HIGH | MUST (blocks planning) |
| 5-9 | MEDIUM | SHOULD |
| 1-4 | LOW | Optional |

**Validation**:
```bash
/speckit.analyze --profile migration-risks
# Validates: All RISK-MIG-xxx with score >= 10 have mitigation field
```

**Violations**: CRITICAL - High-risk migration without mitigation

---

### QG-MIG-003: Coupling Analysis Complete

**Level**: MUST
**Applies to**: All `--from monolith` migrations

Coupling analysis MUST be completed before phase planning for monolith decomposition.

**Threshold**: All modules analyzed with instability index calculated

**Required Metrics**:
- Afferent coupling (Ca) - modules that depend on this
- Efferent coupling (Ce) - modules this depends on
- Instability index I = Ce / (Ca + Ce)
- Coupling classification (TIGHT ≥ 10, LOOSE 3-9, MINIMAL 0-2)

**Validation**:
```bash
/speckit.analyze --profile coupling
# Output: N modules analyzed, M% classified as TIGHT
```

**Violations**: HIGH - Extraction order undefined, risk of cascading failures

---

### Migration Gate Summary

| Gate ID | Phase | Level | Threshold | Validation | Violation |
|---------|-------|-------|-----------|------------|-----------|
| QG-MIG-001 | Pre-Plan | MUST | 100% phases | rollback check | CRITICAL |
| QG-MIG-002 | Pre-Plan | MUST | HIGH+ mitigated | risk check | CRITICAL |
| QG-MIG-003 | Pre-Plan | MUST | all modules | coupling check | HIGH |

---

## Drift Detection Gates

| Gate ID | Name | Threshold | Severity | Description |
|---------|------|-----------|----------|-------------|
| QG-DRIFT-001 | No Critical Drift | 0 critical items | CRITICAL | No critical spec-code misalignment detected |
| QG-DRIFT-002 | High Drift Limit | ≤ 5 high items | HIGH | High-severity drift within acceptable range |
| QG-DRIFT-003 | FR → Code Coverage | ≥ 80% | HIGH | Functional requirements have implementation |
| QG-DRIFT-004 | Code → Spec Coverage | ≥ 70% | HIGH | Public APIs documented in spec |

### QG-DRIFT-001: No Critical Drift

**Level**: MUST (production blocking)
**Applies to**: Post-Implement, Pre-Merge

Ensures no critical spec-code misalignment exists. Critical drift includes:
- Public APIs removed from spec but still exist in code (breaking change risk)
- Security requirements in spec with no implementation
- Backwards-incompatible changes not reflected in spec

**Threshold**: 0 critical drift items

**Validation**:
```bash
/speckit.analyze --profile drift
# Output: drift-report.md with severity breakdown
```

**Violations**: CRITICAL - Blocks merge/deploy until resolved

---

### QG-DRIFT-002: High Drift Limit

**Level**: SHOULD (warning threshold)
**Applies to**: Post-Implement, Pre-Merge

Limits high-severity drift items to manageable number. High drift includes:
- Unimplemented requirements (spec → code gap)
- Undocumented APIs (code → spec gap)
- Missing test coverage for acceptance scenarios

**Threshold**: ≤ 5 high-severity drift items

**Validation**:
```bash
/speckit.analyze --profile drift
# Output: "High drift: 3/5 (60%)" in drift-report.md
```

**Violations**: HIGH - Review recommended, not blocking

---

### QG-DRIFT-003: FR → Code Coverage

**Level**: MUST (for production)
**Applies to**: Post-Implement

Ensures at least 80% of functional requirements have implementation. Measures forward traceability (spec drives code).

**Threshold**: ≥ 80% of FR-xxx have @speckit:FR: annotations in codebase

**Validation**:
```bash
/speckit.analyze --profile drift
# Output: "FR → Code Coverage: 85% (17/20 FRs)"
```

**Auto-Remediation**: Suggest adding @speckit:FR: annotations to implementations

**Violations**:
- CRITICAL: < 50% coverage (major spec-code divergence)
- HIGH: 50-79% coverage (below target, improvement needed)

---

### QG-DRIFT-004: Code → Spec Coverage

**Level**: SHOULD (documentation quality)
**Applies to**: Post-Implement

Ensures at least 70% of public APIs are documented in spec. Measures reverse traceability (code reflects in spec).

**Threshold**: ≥ 70% of public APIs have corresponding FR-xxx in spec.md

**Validation**:
```bash
/speckit.analyze --profile drift
# Output: "Code → Spec Coverage: 75% (15/20 APIs)"
```

**Auto-Remediation**:
- Run `/speckit.reverse-engineer` to extract missing specs
- Add FR-xxx entries to spec.md
- Mark internal APIs with @internal comment

**Violations**: HIGH - Public APIs lack documentation (technical debt)

---

### Drift Gate Summary

| Gate ID | Phase | Level | Threshold | Validation | Violation |
|---------|-------|-------|-----------|------------|-----------|
| QG-DRIFT-001 | Post-Implement | MUST | 0 critical | drift profile | CRITICAL |
| QG-DRIFT-002 | Post-Implement | SHOULD | ≤ 5 high | drift profile | HIGH |
| QG-DRIFT-003 | Post-Implement | MUST | ≥ 80% FR→Code | drift profile | HIGH/CRITICAL |
| QG-DRIFT-004 | Post-Implement | SHOULD | ≥ 70% Code→Spec | drift profile | HIGH |

---

## Property-Based Testing Gates

| Gate ID | Name | Threshold | Severity | Description |
|---------|------|-----------|----------|-------------|
| VG-PROP | Property Coverage | ≥80% | CRITICAL | FR/AS requirements covered by properties |
| VG-PROP-SEC | Security Property Coverage | ≥95% | CRITICAL | EC-SEC-* covered by security properties |
| VG-PROP-BOUND | Boundary Property Coverage | ≥90% | HIGH | EC-* edge cases covered |
| VG-EARS | EARS Transformation | ≥85% | HIGH | Requirements in EARS canonical form |
| VG-SHRUNK | Shrunk Examples | ≥3 per property | MEDIUM | Minimal counterexamples preserved |
| VG-PGS | PGS Resolution | 100% | CRITICAL | All PGS iterations resolved |
| VG-PQS | Property Quality Score | ≥70 | HIGH | Overall PBT quality metric |

### PQS Calculation

```
PQS = (
  Requirement_Coverage × 0.30 +
  Type_Diversity × 0.20 +
  Generator_Quality × 0.20 +
  Shrunk_Examples × 0.15 +
  EARS_Alignment × 0.15
) × 100
```

### Gate Enforcement

- **VG-PROP < 80%**: Block merge, require property addition
- **VG-PROP-SEC < 95%**: Block merge, security review required
- **VG-PGS < 100%**: Block merge, resolve counterexamples first
- **VG-PQS < 70**: Warning, suggest improvements

---

## Summary

| Type | Count |
|------|-------|
| Component Integration Gates | 4 |
| Design Quality Gates | 3 |
| Test-First Development Gates | 4 |
| Mobile Testing Gates | 4 |
| Pre-Implement Gates | 5 |
| Post-Implement Gates | 7 |
| Verification Gates | 6 |
| Pre-Deploy Gates | 5 |
| Mobile Game Quality Gates | 5 |
| Game Art Pipeline Quality Gates | 6 |
| Security Gates | 5 |
| Migration Gates | 3 |
| Drift Detection Gates | 4 |
| Property-Based Testing Gates | 7 |
| **Total QG Principles** | **63** |
| MUST level | 46 |
| SHOULD level | 8 |

---

## When to Use

Apply this domain extension when:
- Building production software with CI/CD pipelines
- Requiring automated quality enforcement
- Working in teams with code review requirements
- Deploying to environments with quality SLAs
- Following DevOps/SRE best practices

---

## Combining with Other Domains

| Combined With | Notes |
|---------------|-------|
| **Production** | Recommended - adds observability on top of quality gates |
| **SaaS** | Multi-tenant: gates apply per-tenant deployment |
| **FinTech** | Strengthen coverage to 90%, add compliance gates |
| **Healthcare** | Add HIPAA-specific security scanning gates |
| **E-Commerce** | Add PCI DSS compliance gates for payment code |

---

## Usage

```bash
# Activate quality gates domain
cp memory/domains/quality-gates.md memory/constitution.domain.md

# Or combine with other domains
cat memory/domains/production.md memory/domains/quality-gates.md > memory/constitution.domain.md

# Run gate validation
/speckit.analyze --profile quality-gates
```

---

## Related Templates

- `templates/shared/ci-templates.md` - GitHub Actions/GitLab CI workflows with gates
- `templates/shared/metrics-framework.md` - SQS calculation and quality metrics
- `templates/commands/analyze.md` - Quality gate validation command

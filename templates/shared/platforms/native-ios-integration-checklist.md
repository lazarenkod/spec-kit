# Native iOS Integration Checklist

**Platform**: Native iOS (Swift/SwiftUI/UIKit)
**Constitution**: `memory/platforms/ios.md`
**Auto-injected by**: `/speckit.tasks` Step 5.5

## Purpose

This checklist defines MANDATORY platform integration tasks that are automatically injected into Phase 2 (Foundational) when native iOS is detected. These tasks block all story implementation tasks.

## Task Format

Tasks use the format: `T-IOS-{AREA}-{NNN}`
- **AREA**: `CFG` | `BLD` | `TST` | `VER`
- **NNN**: Sequential number within area

## Detection

Native iOS is detected when:
- `*.xcodeproj` or `*.xcworkspace` exists
- AND `pubspec.yaml` does NOT exist (not Flutter)
- AND `package.json` does NOT contain "react-native"

## Mandatory Tasks

### Configuration Tasks [CFG]

```markdown
- [ ] T-IOS-CFG-001 [CRITICAL] [PLATFORM:ios_native] Verify Xcode environment
  - Command: xcodebuild -version
  - Check: Xcode 15.0+ installed
  - Check: Command line tools configured
  - Output: Xcode version info

- [ ] T-IOS-CFG-002 [CRITICAL] [PLATFORM:ios_native] [DEP:T-IOS-CFG-001] Configure project settings
  - Open: *.xcodeproj or *.xcworkspace
  - Set: Development Team
  - Set: Bundle Identifier
  - Set: Deployment Target (iOS 15.0+)
  - Verify: No signing errors

- [ ] T-IOS-CFG-003 [HIGH] [PLATFORM:ios_native] [DEP:T-IOS-CFG-002] Configure Info.plist
  - File: Info.plist
  - Add required keys based on features:
    - NSCameraUsageDescription (camera)
    - NSPhotoLibraryUsageDescription (photos)
    - NSLocationWhenInUseUsageDescription (location)
    - NSMicrophoneUsageDescription (audio)
  - Verify: No missing required keys

- [ ] T-IOS-CFG-004 [HIGH] [PLATFORM:ios_native] [DEP:T-IOS-CFG-001] Install CocoaPods/SPM dependencies
  - IF Podfile exists:
    - cd ios && pod install
    - Open .xcworkspace (not .xcodeproj)
  - IF Package.swift or SPM used:
    - Xcode → File → Packages → Resolve
  - Verify: Dependencies resolved
```

### Build Tasks [BLD]

```markdown
- [ ] T-IOS-BLD-001 [CRITICAL] [PLATFORM:ios_native] [DEP:T-IOS-CFG-004] Build debug configuration
  - Command: xcodebuild -scheme Runner -configuration Debug -sdk iphonesimulator build
  - Or: Xcode → Product → Build
  - Check: Build succeeds
  - Output: Build log

- [ ] T-IOS-BLD-002 [HIGH] [PLATFORM:ios_native] [DEP:T-IOS-BLD-001] Configure release build
  - Set: Archive scheme settings
  - Set: Code signing for distribution
  - Configure: App Store Connect API key (optional)
  - Verify: Release build compiles
```

### Testing Tasks [TST]

```markdown
- [ ] T-IOS-TST-001 [CRITICAL] [PLATFORM:ios_native] [DEP:T-IOS-BLD-001] Create XCUITest target
  - IF UITests target not exists:
    - Xcode → File → New → Target → UI Testing Bundle
  - Verify: UITests target added to scheme
  - Template: templates/shared/mobile-test-templates/xcuitest-template.md

- [ ] T-IOS-TST-002 [CRITICAL] [PLATFORM:ios_native] [DEP:T-IOS-TST-001] Scaffold UI tests for AS-xxx
  - Map: Each AS-xxx from spec.md to test method
  - Add: @speckit:AS-xxx comments
  - Create: FeatureUITests.swift with test methods
  - Create: Screen objects in Screens/ directory
  - Verify: All AS-xxx covered with test scaffolds
  - QG-MOB-001: Test scaffolds created

- [ ] T-IOS-TST-003 [HIGH] [PLATFORM:ios_native] [DEP:T-IOS-TST-002] Add accessibility identifiers
  - For each testable element:
    - SwiftUI: .accessibilityIdentifier("id")
    - UIKit: element.accessibilityIdentifier = "id"
  - Verify: Test selectors find elements

- [ ] T-IOS-TST-004 [HIGH] [PLATFORM:ios_native] [DEP:T-IOS-TST-003] Run UI tests on Simulator
  - Prerequisite: iOS Simulator running (iPhone 15 Pro)
  - Command: xcodebuild test -scheme Runner -destination 'platform=iOS Simulator,name=iPhone 15 Pro'
  - Check: Tests execute (may fail in TDD Red phase)
  - Output: Test execution log
  - QG-MOB-003: Cross-platform verified (iOS only)

- [ ] T-IOS-TST-005 [MEDIUM] [PLATFORM:ios_native] [DEP:T-IOS-TST-004] Generate coverage report
  - Command: xcodebuild test -enableCodeCoverage YES ...
  - Tool: xcrun xccov view --report Build/Logs/Test/*.xcresult
  - Check: Coverage >= 70% (QG-MOB-002 threshold)
  - Output: Coverage summary
```

### Verification Tasks [VER]

```markdown
- [ ] T-IOS-VER-001 [CRITICAL] [PLATFORM:ios_native] [DEP:T-IOS-BLD-001] Run app on Simulator
  - Command: xcodebuild -scheme Runner -destination 'platform=iOS Simulator,name=iPhone 15 Pro' run
  - Or: Xcode → Run
  - Verify: App launches without crash
  - Output: Screenshot of running app

- [ ] T-IOS-VER-002 [HIGH] [PLATFORM:ios_native] [DEP:T-IOS-VER-001] Test on multiple device sizes
  - Run on: iPhone SE (small)
  - Run on: iPhone 15 Pro (standard)
  - Run on: iPhone 15 Pro Max (large)
  - Run on: iPad (if universal)
  - Verify: Layout adapts correctly
```

## Dependency Graph

```text
T-IOS-CFG-001 ──→ T-IOS-CFG-002 ──→ T-IOS-CFG-003
       │
       └──→ T-IOS-CFG-004 ──→ T-IOS-BLD-001 ──→ T-IOS-BLD-002
                                     │
                                     ├──→ T-IOS-VER-001 ──→ T-IOS-VER-002
                                     │
                                     └──→ T-IOS-TST-001 ──→ T-IOS-TST-002 ──→ T-IOS-TST-003
                                                                                    │
                                                                                    ↓
                                                                            T-IOS-TST-004
                                                                                    │
                                                                                    ↓
                                                                            T-IOS-TST-005
```

## Injection Rules

When `/speckit.tasks` detects `PLATFORM_DETECTED = "ios_native"`:

1. Load this checklist
2. Parse all tasks from `### Mandatory Tasks` sections
3. Add `[PLATFORM:ios_native]` marker to all tasks
4. Insert into Phase 2 (Foundational)
5. Add implicit dependency: All Phase 3+ tasks depend on T-IOS-VER-001

## Quality Gate Integration

| Gate ID | Task | Blocks |
|---------|------|--------|
| QG-IOS-001 | T-IOS-BLD-001 | Phase 3 start |
| QG-IOS-002 | T-IOS-VER-001 | Story tasks |
| QG-MOB-001 | T-IOS-TST-002 | Wave 3 implementation |
| QG-MOB-002 | T-IOS-TST-005 | Feature completion |
| QG-MOB-003 | T-IOS-TST-004 | Platform verification |

## macOS Requirement

**CRITICAL**: Native iOS development requires macOS.

If running on non-macOS:
- All T-IOS-* tasks are SKIPPED with warning
- Log: "iOS native tasks skipped - requires macOS"
- Feature may proceed with Android-only if applicable

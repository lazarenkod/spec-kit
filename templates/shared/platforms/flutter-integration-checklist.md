# Flutter Integration Checklist

**Platform**: Flutter
**Constitution**: `memory/platforms/flutter.md`
**Auto-injected by**: `/speckit.tasks` Step 5.5

## Purpose

This checklist defines MANDATORY platform integration tasks that are automatically injected into Phase 2 (Foundational) when Flutter is detected. These tasks block all story implementation tasks.

## Task Format

Tasks use the format: `T-FLT-{AREA}-{NNN}`
- **AREA**: `IOS` | `AND` | `VER` | `CFG`
- **NNN**: Sequential number within area

## Mandatory Tasks

### Configuration Tasks [CFG]

```markdown
- [ ] T-FLT-CFG-001 [CRITICAL] [PLATFORM:flutter] Verify Flutter SDK and dependencies
  - Command: flutter doctor -v
  - Check: All required components installed
  - Check: Xcode and Android SDK configured
  - Output: flutter doctor output with no errors

- [ ] T-FLT-CFG-002 [HIGH] [PLATFORM:flutter] Configure pubspec.yaml with required dependencies
  - File: pubspec.yaml
  - Verify: SDK constraint is >=3.0.0 <4.0.0
  - Add: Required dependencies for the feature
  - Run: flutter pub get
  - Verify: No dependency conflicts

- [ ] T-FLT-CFG-003 [HIGH] [PLATFORM:flutter] Configure analysis_options.yaml
  - File: analysis_options.yaml
  - Add: flutter_lints or very_good_analysis
  - Run: flutter analyze
  - Verify: No analysis errors
```

### iOS Integration Tasks [IOS]

```markdown
- [ ] T-FLT-IOS-001 [CRITICAL] [PLATFORM:flutter] [DEP:T-FLT-CFG-001] Configure iOS deployment target
  - File: ios/Podfile
  - Set: platform :ios, '12.0' (minimum)
  - Add post_install script for deployment target
  - Verify: Podfile syntax valid

- [ ] T-FLT-IOS-002 [CRITICAL] [PLATFORM:flutter] [DEP:T-FLT-IOS-001] Install CocoaPods dependencies
  - Commands:
    ```bash
    cd ios
    pod repo update
    pod install
    ```
  - Verify: Pods installed without errors
  - Output: Podfile.lock updated

- [ ] T-FLT-IOS-003 [HIGH] [PLATFORM:flutter] [DEP:T-FLT-IOS-002] Configure Xcode signing
  - Open: ios/Runner.xcworkspace
  - Target → Signing & Capabilities
  - Set: Team, Bundle Identifier
  - Set: Provisioning Profile (auto or manual)
  - Verify: Signing certificate valid

- [ ] T-FLT-IOS-004 [HIGH] [PLATFORM:flutter] [DEP:T-FLT-IOS-003] Configure Info.plist permissions
  - File: ios/Runner/Info.plist
  - Add required keys based on features:
    - NSCameraUsageDescription (camera)
    - NSPhotoLibraryUsageDescription (photos)
    - NSLocationWhenInUseUsageDescription (location)
    - NSMicrophoneUsageDescription (audio)
  - Verify: No missing required keys for used features
```

### Android Integration Tasks [AND]

```markdown
- [ ] T-FLT-AND-001 [CRITICAL] [PLATFORM:flutter] [DEP:T-FLT-CFG-001] Configure Android SDK versions
  - File: android/app/build.gradle
  - Set:
    ```groovy
    android {
        compileSdk 34
        defaultConfig {
            minSdk 21
            targetSdk 34
        }
    }
    ```
  - Verify: Gradle sync succeeds

- [ ] T-FLT-AND-002 [HIGH] [PLATFORM:flutter] [DEP:T-FLT-AND-001] Configure ProGuard rules
  - File: android/app/proguard-rules.pro
  - Add rules for:
    - Flutter engine
    - Firebase (if used)
    - Other native libraries
  - File: android/app/build.gradle
  - Enable minification for release:
    ```groovy
    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
    ```
  - Verify: Release build succeeds with ProGuard

- [ ] T-FLT-AND-003 [HIGH] [PLATFORM:flutter] [DEP:T-FLT-AND-001] Configure AndroidManifest.xml
  - File: android/app/src/main/AndroidManifest.xml
  - Add required permissions based on features:
    - android.permission.INTERNET
    - android.permission.CAMERA (camera)
    - android.permission.ACCESS_FINE_LOCATION (location)
    - android.permission.READ_EXTERNAL_STORAGE (files)
  - Verify: No missing permissions for used features
```

### Verification Tasks [VER]

```markdown
- [ ] T-FLT-VER-001 [CRITICAL] [PLATFORM:flutter] [DEP:T-FLT-CFG-003] Verify flutter doctor passes
  - Command: flutter doctor
  - Check: No issues in output
  - Check: All platforms show checkmarks
  - Output: flutter doctor output

- [ ] T-FLT-VER-002 [CRITICAL] [PLATFORM:flutter] [DEP:T-FLT-IOS-004] Verify iOS debug build
  - Command: flutter build ios --debug
  - Check: Build succeeds without errors
  - Check: App bundle created
  - Output: Build log

- [ ] T-FLT-VER-003 [CRITICAL] [PLATFORM:flutter] [DEP:T-FLT-AND-003] Verify Android debug build
  - Command: flutter build apk --debug
  - Check: APK created successfully
  - Check: File: build/app/outputs/flutter-apk/app-debug.apk
  - Output: Build log

- [ ] T-FLT-VER-004 [HIGH] [PLATFORM:flutter] [DEP:T-FLT-VER-002,T-FLT-VER-003] Run app on both platforms
  - iOS: flutter run -d ios (or simulator)
  - Android: flutter run -d android (or emulator)
  - Verify: App launches without crash
  - Verify: Hot reload works
  - Output: Screenshots of running app
```

### Mobile Testing Tasks [TST]

```markdown
- [ ] T-FLT-TST-001 [CRITICAL] [PLATFORM:flutter] [DEP:T-FLT-VER-004] Configure integration test dependencies
  - File: pubspec.yaml
  - Add dev_dependencies:
    ```yaml
    dev_dependencies:
      integration_test:
        sdk: flutter
      flutter_test:
        sdk: flutter
    ```
  - Run: flutter pub get
  - Verify: Dependencies resolved

- [ ] T-FLT-TST-002 [CRITICAL] [PLATFORM:flutter] [DEP:T-FLT-TST-001] Create integration_test directory structure
  - Create: integration_test/
  - Create: integration_test/app_test.dart
  - Create: test_driver/integration_test.dart
  - Template: templates/shared/mobile-test-templates/flutter-test-template.md
  - Verify: Directory structure correct

- [ ] T-FLT-TST-003 [HIGH] [PLATFORM:flutter] [DEP:T-FLT-TST-002] Scaffold integration tests for AS-xxx
  - Map: Each AS-xxx from spec.md to test case
  - Add: @speckit:AS-xxx annotations
  - Add: testWidgets() for each acceptance scenario
  - Verify: All AS-xxx covered with test scaffolds
  - QG-MOB-001: Test scaffolds created

- [ ] T-FLT-TST-004 [HIGH] [PLATFORM:flutter] [DEP:T-FLT-TST-003] Run tests on Android emulator
  - Prerequisite: Android emulator running (speckit-android-emulator)
  - Command: flutter test integration_test/ --device-id=emulator-5554
  - Check: Tests execute (may fail in TDD Red phase)
  - Output: Test execution log

- [ ] T-FLT-TST-005 [HIGH] [PLATFORM:flutter] [DEP:T-FLT-TST-003] Run tests on iOS Simulator (macOS only)
  - Prerequisite: iOS Simulator running (iPhone 15 Pro)
  - Skip: If not on macOS (log warning)
  - Command: flutter test integration_test/
  - Check: Tests execute (may fail in TDD Red phase)
  - Output: Test execution log
  - QG-MOB-003: Cross-platform verified

- [ ] T-FLT-TST-006 [MEDIUM] [PLATFORM:flutter] [DEP:T-FLT-TST-004,T-FLT-TST-005] Generate coverage report
  - Command: flutter test integration_test/ --coverage
  - File: coverage/lcov.info
  - Check: Coverage >= 70% (QG-MOB-002 threshold)
  - Output: Coverage summary
```

## Dependency Graph

```text
T-FLT-CFG-001 ──┬──→ T-FLT-CFG-002 ──→ T-FLT-CFG-003 ──→ T-FLT-VER-001
               │
               ├──→ T-FLT-IOS-001 ──→ T-FLT-IOS-002 ──→ T-FLT-IOS-003 ──→ T-FLT-IOS-004 ──→ T-FLT-VER-002
               │
               └──→ T-FLT-AND-001 ──→ T-FLT-AND-002 ──→ T-FLT-AND-003 ──→ T-FLT-VER-003
                                                                                   │
                                                                                   ↓
                                                                           T-FLT-VER-004
                                                                                   │
                                                                                   ↓
                                                                           T-FLT-TST-001
                                                                                   │
                                                                                   ↓
                                                                           T-FLT-TST-002
                                                                                   │
                                                                                   ↓
                                                                           T-FLT-TST-003
                                                                               ┌───┴───┐
                                                                               ↓       ↓
                                                                       T-FLT-TST-004  T-FLT-TST-005
                                                                               └───┬───┘
                                                                                   ↓
                                                                           T-FLT-TST-006
```

## Injection Rules

When `/speckit.tasks` detects `PLATFORM_DETECTED = "flutter"`:

1. Load this checklist
2. Parse all tasks from `### Mandatory Tasks` sections
3. Add `[PLATFORM:flutter]` marker to all tasks
4. Insert into Phase 2 (Foundational)
5. Add implicit dependency: All Phase 3+ tasks depend on T-FLT-VER-004

## Quality Gate Integration

| Gate ID | Task | Blocks |
|---------|------|--------|
| QG-FLT-001 | T-FLT-VER-001 | Phase 3 start |
| QG-FLT-002 | T-FLT-VER-002 | iOS story tasks |
| QG-FLT-003 | T-FLT-VER-003 | Android story tasks |
| QG-MOB-001 | T-FLT-TST-003 | Wave 3 implementation |
| QG-MOB-002 | T-FLT-TST-006 | Feature completion |
| QG-MOB-003 | T-FLT-TST-005 | Cross-platform release |

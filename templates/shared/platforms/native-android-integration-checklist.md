# Native Android Integration Checklist

**Platform**: Native Android (Kotlin/Java)
**Constitution**: `memory/platforms/android.md`
**Auto-injected by**: `/speckit.tasks` Step 5.5

## Purpose

This checklist defines MANDATORY platform integration tasks that are automatically injected into Phase 2 (Foundational) when native Android is detected. These tasks block all story implementation tasks.

## Task Format

Tasks use the format: `T-AND-{AREA}-{NNN}`
- **AREA**: `CFG` | `BLD` | `TST` | `VER`
- **NNN**: Sequential number within area

## Detection

Native Android is detected when:
- `app/build.gradle` or `app/build.gradle.kts` exists
- AND `pubspec.yaml` does NOT exist (not Flutter)
- AND `package.json` does NOT contain "react-native"
- AND `build.gradle.kts` does NOT contain `kotlin("multiplatform")` (not KMP)

## Mandatory Tasks

### Configuration Tasks [CFG]

```markdown
- [ ] T-AND-CFG-001 [CRITICAL] [PLATFORM:android_native] Verify Android SDK environment
  - Check: ANDROID_HOME environment variable set
  - Check: SDK Platform 34 installed
  - Check: Build Tools installed
  - Command: sdkmanager --list
  - Output: SDK configuration

- [ ] T-AND-CFG-002 [CRITICAL] [PLATFORM:android_native] [DEP:T-AND-CFG-001] Configure project Gradle
  - File: build.gradle.kts (project level)
  - Set: Kotlin version (1.9+)
  - Set: Gradle plugin versions
  - Verify: Gradle sync succeeds

- [ ] T-AND-CFG-003 [CRITICAL] [PLATFORM:android_native] [DEP:T-AND-CFG-002] Configure app Gradle
  - File: app/build.gradle.kts
  - Set:
    ```kotlin
    android {
        compileSdk = 34
        defaultConfig {
            minSdk = 24
            targetSdk = 34
        }
    }
    ```
  - Verify: Gradle sync succeeds

- [ ] T-AND-CFG-004 [HIGH] [PLATFORM:android_native] [DEP:T-AND-CFG-003] Configure AndroidManifest.xml
  - File: app/src/main/AndroidManifest.xml
  - Add required permissions:
    - android.permission.INTERNET
    - android.permission.CAMERA (camera)
    - android.permission.ACCESS_FINE_LOCATION (location)
  - Verify: No missing permissions for used features

- [ ] T-AND-CFG-005 [HIGH] [PLATFORM:android_native] [DEP:T-AND-CFG-003] Configure ProGuard/R8
  - File: app/proguard-rules.pro
  - Add rules for libraries
  - File: app/build.gradle.kts
  - Enable:
    ```kotlin
    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    ```
  - Verify: Release build with minification succeeds
```

### Build Tasks [BLD]

```markdown
- [ ] T-AND-BLD-001 [CRITICAL] [PLATFORM:android_native] [DEP:T-AND-CFG-004] Build debug APK
  - Command: ./gradlew assembleDebug
  - Check: APK created at app/build/outputs/apk/debug/
  - Output: Build log

- [ ] T-AND-BLD-002 [HIGH] [PLATFORM:android_native] [DEP:T-AND-BLD-001] Configure signing
  - Create: keystore file for release
  - File: app/build.gradle.kts
  - Add signing config:
    ```kotlin
    signingConfigs {
        create("release") {
            storeFile = file("keystore.jks")
            storePassword = System.getenv("STORE_PASSWORD")
            keyAlias = System.getenv("KEY_ALIAS")
            keyPassword = System.getenv("KEY_PASSWORD")
        }
    }
    ```
  - Verify: Release build signs correctly

- [ ] T-AND-BLD-003 [HIGH] [PLATFORM:android_native] [DEP:T-AND-BLD-002] Build release APK/AAB
  - Command: ./gradlew assembleRelease
  - Or: ./gradlew bundleRelease (for AAB)
  - Check: Signed output created
  - Output: Build log
```

### Testing Tasks [TST]

```markdown
- [ ] T-AND-TST-001 [CRITICAL] [PLATFORM:android_native] [DEP:T-AND-BLD-001] Configure Espresso dependencies
  - File: app/build.gradle.kts
  - Add:
    ```kotlin
    dependencies {
        androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
        androidTestImplementation("androidx.test.espresso:espresso-contrib:3.5.1")
        androidTestImplementation("androidx.test.ext:junit:1.1.5")
        androidTestImplementation("androidx.test:runner:1.5.2")
        androidTestImplementation("androidx.test:rules:1.5.0")
    }
    android {
        defaultConfig {
            testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        }
        testOptions {
            animationsDisabled = true
        }
    }
    ```
  - Run: ./gradlew build
  - Verify: Dependencies resolved
  - Template: templates/shared/mobile-test-templates/espresso-template.md

- [ ] T-AND-TST-002 [CRITICAL] [PLATFORM:android_native] [DEP:T-AND-TST-001] Scaffold Espresso tests for AS-xxx
  - Create: app/src/androidTest/java/com/example/app/
  - Map: Each AS-xxx from spec.md to test method
  - Add: @speckit:AS-xxx comments
  - Create: FeatureTest.kt with test methods
  - Create: Screen objects in screens/ package
  - Verify: All AS-xxx covered with test scaffolds
  - QG-MOB-001: Test scaffolds created

- [ ] T-AND-TST-003 [HIGH] [PLATFORM:android_native] [DEP:T-AND-TST-002] Add view IDs for testing
  - For each testable element:
    - XML: android:id="@+id/element_id"
    - Compose: Modifier.testTag("element_id")
  - Verify: Test selectors find elements

- [ ] T-AND-TST-004 [HIGH] [PLATFORM:android_native] [DEP:T-AND-TST-003] Run Espresso tests on emulator
  - Prerequisite: Android emulator running (speckit-android-emulator)
  - Command: ./gradlew connectedAndroidTest
  - Check: Tests execute (may fail in TDD Red phase)
  - Output: Test execution log
  - QG-MOB-003: Cross-platform verified (Android only)

- [ ] T-AND-TST-005 [MEDIUM] [PLATFORM:android_native] [DEP:T-AND-TST-004] Generate coverage report
  - Command: ./gradlew createDebugCoverageReport
  - File: app/build/reports/coverage/androidTest/debug/
  - Check: Coverage >= 70% (QG-MOB-002 threshold)
  - Output: Coverage summary
```

### Verification Tasks [VER]

```markdown
- [ ] T-AND-VER-001 [CRITICAL] [PLATFORM:android_native] [DEP:T-AND-BLD-001] Run app on emulator
  - Prerequisite: Android emulator running
  - Command: adb install app/build/outputs/apk/debug/app-debug.apk
  - Command: adb shell am start -n com.example.app/.MainActivity
  - Verify: App launches without crash
  - Output: Screenshot of running app

- [ ] T-AND-VER-002 [HIGH] [PLATFORM:android_native] [DEP:T-AND-VER-001] Test on multiple screen sizes
  - Run on: Small phone (360dp width)
  - Run on: Standard phone (411dp width)
  - Run on: Large phone/Tablet (600dp+ width)
  - Verify: Layout adapts correctly
```

## Dependency Graph

```text
T-AND-CFG-001 ──→ T-AND-CFG-002 ──→ T-AND-CFG-003 ──→ T-AND-CFG-004 ──→ T-AND-CFG-005
                                            │
                                            ↓
                                    T-AND-BLD-001 ──→ T-AND-BLD-002 ──→ T-AND-BLD-003
                                            │
                                            ├──→ T-AND-VER-001 ──→ T-AND-VER-002
                                            │
                                            └──→ T-AND-TST-001 ──→ T-AND-TST-002 ──→ T-AND-TST-003
                                                                                           │
                                                                                           ↓
                                                                                   T-AND-TST-004
                                                                                           │
                                                                                           ↓
                                                                                   T-AND-TST-005
```

## Injection Rules

When `/speckit.tasks` detects `PLATFORM_DETECTED = "android_native"`:

1. Load this checklist
2. Parse all tasks from `### Mandatory Tasks` sections
3. Add `[PLATFORM:android_native]` marker to all tasks
4. Insert into Phase 2 (Foundational)
5. Add implicit dependency: All Phase 3+ tasks depend on T-AND-VER-001

## Quality Gate Integration

| Gate ID | Task | Blocks |
|---------|------|--------|
| QG-AND-001 | T-AND-BLD-001 | Phase 3 start |
| QG-AND-002 | T-AND-VER-001 | Story tasks |
| QG-MOB-001 | T-AND-TST-002 | Wave 3 implementation |
| QG-MOB-002 | T-AND-TST-005 | Feature completion |
| QG-MOB-003 | T-AND-TST-004 | Platform verification |

## Docker Android Emulator

For CI/CD and staging environments, use Docker-based Android emulator:

```yaml
# .speckit/staging/docker-compose.yaml
android-emulator:
  image: budtmo/docker-android:emulator_12.0
  container_name: speckit-android-emulator
  privileged: true
  ports:
    - "5554:5554"
    - "5555:5555"
    - "6080:6080"
  environment:
    EMULATOR_DEVICE: "pixel_6"
    WEB_VNC: "true"
```

Access VNC at `http://localhost:6080` for visual debugging.

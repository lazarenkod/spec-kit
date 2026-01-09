# React Native Integration Checklist

**Platform**: React Native
**Constitution**: `memory/platforms/react-native.md`
**Auto-injected by**: `/speckit.tasks` Step 5.5

## Purpose

This checklist defines MANDATORY platform integration tasks that are automatically injected into Phase 2 (Foundational) when React Native is detected. These tasks block all story implementation tasks.

## Task Format

Tasks use the format: `T-RN-{AREA}-{NNN}`
- **AREA**: `IOS` | `AND` | `VER` | `CFG` | `NAT`
- **NNN**: Sequential number within area

## Mandatory Tasks

### Configuration Tasks [CFG]

```markdown
- [ ] T-RN-CFG-001 [CRITICAL] [PLATFORM:react_native] Verify React Native environment
  - Command: npx react-native doctor
  - Check: All required components installed
  - Check: Node.js, Watchman, Xcode, Android SDK
  - Output: Doctor output with no errors

- [ ] T-RN-CFG-002 [CRITICAL] [PLATFORM:react_native] Install npm dependencies
  - Command: npm install (or yarn)
  - Check: No peer dependency warnings
  - Check: package-lock.json updated
  - Output: Install log

- [ ] T-RN-CFG-003 [HIGH] [PLATFORM:react_native] Configure TypeScript
  - File: tsconfig.json
  - Set: strict: true
  - Set: noImplicitAny: true
  - Run: npx tsc --noEmit
  - Verify: No TypeScript errors

- [ ] T-RN-CFG-004 [HIGH] [PLATFORM:react_native] Configure Metro bundler
  - File: metro.config.js
  - Extend default config properly
  - Add custom transformers if needed (SVG, etc.)
  - Verify: Metro starts without errors
```

### iOS Integration Tasks [IOS]

```markdown
- [ ] T-RN-IOS-001 [CRITICAL] [PLATFORM:react_native] [DEP:T-RN-CFG-002] Install CocoaPods dependencies
  - Commands:
    ```bash
    cd ios
    bundle install  # If using Gemfile
    bundle exec pod install
    ```
  - Verify: Pods installed without errors
  - Output: Podfile.lock updated

- [ ] T-RN-IOS-002 [CRITICAL] [PLATFORM:react_native] [DEP:T-RN-IOS-001] Configure Xcode project
  - Open: ios/{AppName}.xcworkspace
  - Target → Signing & Capabilities
  - Set: Team, Bundle Identifier
  - Set: Development Team
  - Verify: No signing errors

- [ ] T-RN-IOS-003 [HIGH] [PLATFORM:react_native] [DEP:T-RN-IOS-002] Configure Info.plist
  - File: ios/{AppName}/Info.plist
  - Add required keys:
    - NSCameraUsageDescription (camera)
    - NSPhotoLibraryUsageDescription (photos)
    - NSLocationWhenInUseUsageDescription (location)
    - NSAppTransportSecurity (if needed)
  - Verify: No missing required keys

- [ ] T-RN-IOS-004 [HIGH] [PLATFORM:react_native] [DEP:T-RN-IOS-001] Link native modules
  - Command: npx pod-install (auto-linking)
  - Check: All native modules linked
  - File: ios/Podfile - verify no manual links needed
  - Verify: No "module not found" errors
```

### Android Integration Tasks [AND]

```markdown
- [ ] T-RN-AND-001 [CRITICAL] [PLATFORM:react_native] [DEP:T-RN-CFG-002] Configure Gradle properties
  - File: android/gradle.properties
  - Set:
    ```properties
    # New Architecture (RN 0.71+)
    newArchEnabled=true

    # Hermes engine
    hermesEnabled=true

    # Performance
    org.gradle.jvmargs=-Xmx4g
    org.gradle.parallel=true
    ```
  - Verify: Gradle sync succeeds

- [ ] T-RN-AND-002 [HIGH] [PLATFORM:react_native] [DEP:T-RN-AND-001] Configure signing
  - Create: keystore file for release
  - File: android/app/build.gradle
  - Add:
    ```groovy
    signingConfigs {
        release {
            storeFile file(MYAPP_RELEASE_STORE_FILE)
            storePassword MYAPP_RELEASE_STORE_PASSWORD
            keyAlias MYAPP_RELEASE_KEY_ALIAS
            keyPassword MYAPP_RELEASE_KEY_PASSWORD
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
    ```
  - File: android/gradle.properties - add credentials (or use env vars)
  - Verify: Release build signs correctly

- [ ] T-RN-AND-003 [HIGH] [PLATFORM:react_native] [DEP:T-RN-AND-001] Configure permissions
  - File: android/app/src/main/AndroidManifest.xml
  - Add required permissions:
    ```xml
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    ```
  - Verify: No runtime permission crashes
```

### Native Module Tasks [NAT]

```markdown
- [ ] T-RN-NAT-001 [HIGH] [PLATFORM:react_native] [DEP:T-RN-CFG-004] Configure react-native.config.js
  - File: react-native.config.js
  - Configure:
    - Project paths
    - Asset sources
    - Native module dependencies
  - Verify: Native modules resolve correctly

- [ ] T-RN-NAT-002 [MEDIUM] [PLATFORM:react_native] [DEP:T-RN-NAT-001] Verify native module linking
  - Run: npx react-native config
  - Check: All dependencies listed
  - Check: No "unlinked" warnings
  - Output: Config output
```

### Verification Tasks [VER]

```markdown
- [ ] T-RN-VER-001 [CRITICAL] [PLATFORM:react_native] [DEP:T-RN-CFG-003] Verify TypeScript compiles
  - Command: npx tsc --noEmit
  - Check: No type errors
  - Output: Compiler output

- [ ] T-RN-VER-002 [CRITICAL] [PLATFORM:react_native] [DEP:T-RN-IOS-004] Verify iOS build
  - Command: npx react-native run-ios --mode Debug
  - Or: Open Xcode → Build
  - Check: Build succeeds
  - Check: App launches on simulator
  - Output: Build log

- [ ] T-RN-VER-003 [CRITICAL] [PLATFORM:react_native] [DEP:T-RN-AND-003] Verify Android build
  - Command: npx react-native run-android
  - Or: ./gradlew :app:assembleDebug
  - Check: APK created
  - Check: App launches on emulator
  - Output: Build log

- [ ] T-RN-VER-004 [HIGH] [PLATFORM:react_native] [DEP:T-RN-VER-002,T-RN-VER-003] Run on both platforms
  - iOS: Run on simulator or device
  - Android: Run on emulator or device
  - Check: App launches without crash
  - Check: Metro bundler serves JS
  - Check: Hot reload works
  - Output: Screenshots of running app
```

## Dependency Graph

```text
T-RN-CFG-001 ──→ T-RN-CFG-002 ──┬──→ T-RN-CFG-003 ──→ T-RN-CFG-004 ──→ T-RN-VER-001
                               │                              │
                               │                              └──→ T-RN-NAT-001 ──→ T-RN-NAT-002
                               │
                               ├──→ T-RN-IOS-001 ──→ T-RN-IOS-002 ──→ T-RN-IOS-003
                               │          │
                               │          └──→ T-RN-IOS-004 ──→ T-RN-VER-002
                               │
                               └──→ T-RN-AND-001 ──→ T-RN-AND-002 ──→ T-RN-AND-003 ──→ T-RN-VER-003
                                                                                            │
                                                                                            ↓
                                                                                    T-RN-VER-004
```

## Injection Rules

When `/speckit.tasks` detects `PLATFORM_DETECTED = "react_native"`:

1. Load this checklist
2. Parse all tasks from `### Mandatory Tasks` sections
3. Add `[PLATFORM:react_native]` marker to all tasks
4. Insert into Phase 2 (Foundational)
5. Add implicit dependency: All Phase 3+ tasks depend on T-RN-VER-004

## Quality Gate Integration

| Gate ID | Task | Blocks |
|---------|------|--------|
| QG-RN-001 | T-RN-VER-001 | Phase 3 start |
| QG-RN-002 | T-RN-VER-002 | iOS story tasks |
| QG-RN-003 | T-RN-VER-003 | Android story tasks |

## Expo Variant

If Expo is detected (expo in package.json), use simplified checklist:

```markdown
- [ ] T-RN-EXPO-001 [CRITICAL] [PLATFORM:react_native:expo] Verify Expo environment
  - Command: npx expo doctor
  - Check: No critical issues

- [ ] T-RN-EXPO-002 [CRITICAL] [PLATFORM:react_native:expo] Configure app.json
  - Set: name, slug, version
  - Set: ios.bundleIdentifier
  - Set: android.package
  - Set: Required permissions

- [ ] T-RN-EXPO-003 [HIGH] [PLATFORM:react_native:expo] Run Expo build
  - Command: npx expo run:ios / npx expo run:android
  - Or: eas build --profile development
  - Verify: Build succeeds
```

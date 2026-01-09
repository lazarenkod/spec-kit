# KMP Integration Checklist

**Platform**: Kotlin Multiplatform (KMP)
**Constitution**: `memory/platforms/kmp.md`
**Auto-injected by**: `/speckit.tasks` Step 5.5

## Purpose

This checklist defines MANDATORY platform integration tasks that are automatically injected into Phase 2 (Foundational) when KMP is detected. These tasks block all story implementation tasks.

## Task Format

Tasks use the format: `T-KMP-{AREA}-{NNN}`
- **AREA**: `IOS` | `AND` | `VER` | `CFG`
- **NNN**: Sequential number within area

## Mandatory Tasks

### Configuration Tasks [CFG]

```markdown
- [ ] T-KMP-CFG-001 [CRITICAL] [PLATFORM:kmp] Configure shared/build.gradle.kts with multiplatform targets
  - File: shared/build.gradle.kts
  - Add kotlin("multiplatform") plugin
  - Configure targets: jvm(), androidTarget(), iosX64(), iosArm64(), iosSimulatorArm64()
  - Verify: Gradle sync succeeds

- [ ] T-KMP-CFG-002 [CRITICAL] [PLATFORM:kmp] Configure iOS framework export in build.gradle.kts
  - File: shared/build.gradle.kts
  - Add framework binary configuration:
    ```kotlin
    listOf(iosX64(), iosArm64(), iosSimulatorArm64()).forEach {
        it.binaries.framework {
            baseName = "shared"
            isStatic = true
        }
    }
    ```
  - Verify: ./gradlew :shared:linkDebugFrameworkIosArm64 succeeds

- [ ] T-KMP-CFG-003 [HIGH] [PLATFORM:kmp] Configure gradle.properties for KMP
  - File: gradle.properties
  - Add:
    ```properties
    kotlin.mpp.enableCInteropCommonization=true
    kotlin.native.binary.memoryModel=experimental
    ```
  - Verify: Gradle sync succeeds
```

### iOS Integration Tasks [IOS]

```markdown
- [ ] T-KMP-IOS-001 [CRITICAL] [PLATFORM:kmp] [DEP:T-KMP-CFG-002] Build iOS framework
  - Command: ./gradlew :shared:linkDebugFrameworkIosArm64
  - Verify: shared/build/bin/iosArm64/debugFramework/shared.framework exists
  - Output: Framework binary ready for Xcode

- [ ] T-KMP-IOS-002 [CRITICAL] [PLATFORM:kmp] [DEP:T-KMP-IOS-001] Add framework to Xcode project
  - Open: iosApp/iosApp.xcodeproj (or .xcworkspace)
  - Target → General → Frameworks, Libraries, and Embedded Content
  - Add: shared.framework
  - Set: "Embed & Sign"
  - Verify: Xcode recognizes framework

- [ ] T-KMP-IOS-003 [CRITICAL] [PLATFORM:kmp] [DEP:T-KMP-IOS-002] Configure Framework Search Paths
  - Xcode → Target → Build Settings → Framework Search Paths
  - Add for Debug: $(SRCROOT)/../shared/build/bin/iosArm64/debugFramework
  - Add for Release: $(SRCROOT)/../shared/build/bin/iosArm64/releaseFramework
  - Verify: Build succeeds without "framework not found" errors

- [ ] T-KMP-IOS-004 [HIGH] [PLATFORM:kmp] [DEP:T-KMP-IOS-003] Create Koin iOS initializer
  - File: shared/src/iosMain/kotlin/di/KoinIOS.kt
  - Content:
    ```kotlin
    object KoinApplication {
        val shared = initKoin()
        val koin get() = shared.koin
    }

    fun initKoin(): KoinApplication = startKoin {
        modules(sharedModule)
    }
    ```
  - Verify: KoinApplication accessible from Swift

- [ ] T-KMP-IOS-005 [HIGH] [PLATFORM:kmp] [DEP:T-KMP-IOS-004] Export ViewModels for iOS consumption
  - File: shared/src/iosMain/kotlin/presentation/ViewModelWrappers.kt
  - Create wrapper classes with @ObjCName annotations
  - Provide factory functions for each ViewModel
  - Example:
    ```kotlin
    @ObjCName("LibraryViewModelWrapper")
    class LibraryViewModelWrapper {
        private val viewModel: LibraryViewModel = KoinApplication.koin.get()
        // Expose state and methods
    }
    ```
  - Verify: ViewModels accessible from Swift

- [ ] T-KMP-IOS-006 [HIGH] [PLATFORM:kmp] [DEP:T-KMP-IOS-005] Create StateFlow wrappers for iOS
  - File: shared/src/iosMain/kotlin/util/FlowWrapper.kt
  - Create Closeable wrapper for StateFlow observation
  - Enable Swift to collect Kotlin flows
  - Verify: Flows can be observed from SwiftUI
```

### Android Integration Tasks [AND]

```markdown
- [ ] T-KMP-AND-001 [CRITICAL] [PLATFORM:kmp] Configure androidApp/build.gradle.kts
  - File: androidApp/build.gradle.kts
  - Add: implementation(project(":shared"))
  - Configure android block with proper SDK versions
  - Verify: Gradle sync succeeds

- [ ] T-KMP-AND-002 [HIGH] [PLATFORM:kmp] [DEP:T-KMP-AND-001] Initialize Koin in Android Application
  - File: androidApp/src/main/kotlin/.../App.kt
  - Add:
    ```kotlin
    class App : Application() {
        override fun onCreate() {
            super.onCreate()
            startKoin {
                androidContext(this@App)
                modules(sharedModule)
            }
        }
    }
    ```
  - Register in AndroidManifest.xml
  - Verify: Koin injection works in Activities/Fragments
```

### Verification Tasks [VER]

```markdown
- [ ] T-KMP-VER-001 [CRITICAL] [PLATFORM:kmp] [DEP:T-KMP-IOS-006] Verify iOS framework builds without errors
  - Run: ./gradlew :shared:linkDebugFrameworkIosArm64 --info
  - Check: No compilation errors
  - Check: Framework size reasonable (< 50MB for empty)
  - Output: Build log without errors

- [ ] T-KMP-VER-002 [CRITICAL] [PLATFORM:kmp] [DEP:T-KMP-AND-002] Verify Android app compiles with shared module
  - Run: ./gradlew :androidApp:assembleDebug
  - Check: APK created successfully
  - Check: shared module classes accessible
  - Output: Build log without errors

- [ ] T-KMP-VER-003 [HIGH] [PLATFORM:kmp] [DEP:T-KMP-VER-001,T-KMP-VER-002] Run basic UI test on both platforms
  - iOS: Xcode → Run on Simulator
  - Android: ./gradlew :androidApp:installDebug
  - Verify: App launches without crash
  - Verify: Koin DI provides dependencies
  - Output: Screenshots of running app on both platforms
```

## Dependency Graph

```text
T-KMP-CFG-001 ──┬──→ T-KMP-CFG-002 ──→ T-KMP-IOS-001 ──→ T-KMP-IOS-002 ──→ T-KMP-IOS-003
               │                                                             ↓
               │                                                    T-KMP-IOS-004
               │                                                             ↓
               │                                                    T-KMP-IOS-005
               │                                                             ↓
               │                                                    T-KMP-IOS-006
               │                                                             ↓
               └──→ T-KMP-CFG-003 ──→ T-KMP-AND-001 ──→ T-KMP-AND-002 ──→ T-KMP-VER-001
                                                                             ↓
                                                                     T-KMP-VER-002
                                                                             ↓
                                                                     T-KMP-VER-003
```

## Injection Rules

When `/speckit.tasks` detects `PLATFORM_DETECTED = "kmp"`:

1. Load this checklist
2. Parse all tasks from `### Mandatory Tasks` sections
3. Assign task IDs starting from T001 if no existing tasks, or after last task ID
4. Add `[PLATFORM:kmp]` marker to all tasks
5. Insert into Phase 2 (Foundational)
6. Add implicit dependency: All Phase 3+ tasks depend on T-KMP-VER-003

## Quality Gate Integration

| Gate ID | Task | Blocks |
|---------|------|--------|
| QG-KMP-001 | T-KMP-CFG-002 | Phase 3 start |
| QG-KMP-002 | T-KMP-VER-001 | iOS story tasks |
| QG-KMP-003 | T-KMP-VER-002 | Android story tasks |

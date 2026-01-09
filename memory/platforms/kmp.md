# Kotlin Multiplatform Platform Constitution

**Inherits from**: `constitution.base.md` → `constitution.domain.md` (if applicable)

## Overview

Kotlin Multiplatform (KMP) enables sharing business logic across iOS, Android, and other platforms while using native UI. This constitution defines mandatory principles for KMP projects.

## Platform Principles

### KMP-001: Shared Module Structure [MUST]

The shared module MUST follow the standard KMP source set structure:

```text
shared/
├── build.gradle.kts
└── src/
    ├── commonMain/kotlin/     # Platform-agnostic code
    │   ├── domain/            # Business logic, use cases
    │   ├── data/              # Repository interfaces, models
    │   └── presentation/      # ViewModels (if using MVVM)
    ├── commonTest/kotlin/     # Shared tests
    ├── androidMain/kotlin/    # Android-specific implementations
    ├── androidTest/kotlin/    # Android-specific tests
    ├── iosMain/kotlin/        # iOS-specific implementations
    └── iosTest/kotlin/        # iOS-specific tests
```

**Rationale**: Consistent structure enables predictable navigation and clear separation of platform-specific code.

### KMP-002: Framework Export [MUST]

iOS framework MUST be explicitly configured in `shared/build.gradle.kts`:

```kotlin
kotlin {
    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "shared"
            isStatic = true // or false depending on needs
        }
    }
}
```

**Rationale**: Without explicit framework configuration, iOS cannot consume the shared module.

### KMP-003: DI Configuration [MUST]

Dependency injection MUST be configured to work across platforms:

**Common Module** (`commonMain`):
```kotlin
// Module definition
val sharedModule = module {
    singleOf(::BookRepository)
    factoryOf(::LibraryViewModel)
}

// Start function for iOS
fun initKoin(): KoinApplication {
    return startKoin {
        modules(sharedModule)
    }
}
```

**iOS Entry Point** (`iosMain`):
```kotlin
object KoinApplication {
    val shared = initKoin()
    val koin get() = shared.koin
}
```

**Rationale**: iOS cannot use Kotlin constructors directly; factory functions provide access.

### KMP-004: Build System [MUST]

Build system requirements:
- Gradle wrapper version: 8.0+
- Kotlin version: 1.9.0+ (for stable iOS interop)
- Android Gradle Plugin: 8.0+

**gradle.properties**:
```properties
kotlin.mpp.enableCInteropCommonization=true
kotlin.native.binary.memoryModel=experimental
```

**Rationale**: Older versions have significant iOS interop issues and memory model problems.

### KMP-005: Expect/Actual Pattern [MUST]

Platform-specific implementations MUST use expect/actual pattern:

```kotlin
// commonMain
expect class PlatformContext

expect fun getPlatformName(): String

// androidMain
actual class PlatformContext(val context: Context)

actual fun getPlatformName(): String = "Android"

// iosMain
actual class PlatformContext

actual fun getPlatformName(): String = "iOS"
```

**Rationale**: Type-safe platform abstraction prevents runtime errors.

### KMP-006: iOS Interop Annotations [SHOULD]

iOS-facing APIs SHOULD use appropriate annotations:

```kotlin
@ObjCName("LibraryViewModelWrapper")
class LibraryViewModelWrapper(private val viewModel: LibraryViewModel) {
    // Wrapper for iOS consumption
}

@OptIn(ExperimentalObjCName::class)
@ObjCName("BookModel")
data class Book(
    val id: String,
    val title: String
)
```

**Rationale**: Clean Objective-C names improve Swift interop experience.

### KMP-007: Coroutines on iOS [MUST]

Coroutines on iOS MUST be handled with proper dispatchers:

```kotlin
// commonMain
expect val ioDispatcher: CoroutineDispatcher

// androidMain
actual val ioDispatcher: CoroutineDispatcher = Dispatchers.IO

// iosMain
actual val ioDispatcher: CoroutineDispatcher = Dispatchers.Default
```

**Rationale**: iOS doesn't have Dispatchers.IO; using Default prevents runtime crashes.

### KMP-008: State Flow Export [MUST]

StateFlow MUST be wrapped for iOS consumption:

```kotlin
// In iosMain
class FlowWrapper<T>(private val flow: StateFlow<T>) {
    fun collect(onEach: (T) -> Unit, onCompletion: (Throwable?) -> Unit): Closeable {
        val job = CoroutineScope(Dispatchers.Main).launch {
            flow.collect { onEach(it) }
        }
        return object : Closeable {
            override fun close() { job.cancel() }
        }
    }
}
```

**Rationale**: Swift cannot directly observe Kotlin StateFlow; wrappers enable reactive UI.

## Integration Requirements

### iOS Framework Integration

1. **Build Command**: `./gradlew :shared:linkDebugFrameworkIosArm64`
2. **Framework Location**: `shared/build/bin/iosArm64/debugFramework/shared.framework`
3. **Xcode Setup**:
   - Add framework to "Frameworks, Libraries, and Embedded Content"
   - Set "Embed & Sign"
   - Add Framework Search Path: `$(SRCROOT)/../shared/build/bin/iosArm64/debugFramework`

### Android Integration

1. **Dependency**: `implementation(project(":shared"))`
2. **Koin Setup**: Initialize in Application class
3. **ProGuard**: Add rules for Koin and Kotlin reflection

## Quality Gates

| Gate ID | Check | Severity |
|---------|-------|----------|
| QG-KMP-001 | shared/build.gradle.kts has iOS targets | CRITICAL |
| QG-KMP-002 | Framework builds without errors | CRITICAL |
| QG-KMP-003 | Koin modules export iOS factories | HIGH |
| QG-KMP-004 | expect/actual declarations complete | HIGH |
| QG-KMP-005 | No Dispatchers.IO in iosMain | HIGH |

## Testing Strategy

### Shared Tests (commonTest)

- Unit tests for business logic
- Repository interface tests with fakes
- ViewModel tests with TestDispatcher

### Platform Tests

- **androidTest**: Integration tests with real Android context
- **iosTest**: Integration tests with iOS-specific implementations

## Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| iOS build fails | Missing Xcode | Install Xcode Command Line Tools |
| Framework not found | Wrong search path | Verify Framework Search Paths in Xcode |
| Koin crash on iOS | Direct constructor use | Use factory functions via KoinApplication |
| Memory leak on iOS | Improper Flow collection | Use Closeable wrapper pattern |
| Main thread crash | Wrong dispatcher | Use Dispatchers.Main for UI updates |

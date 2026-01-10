---
description: Kotlin Multiplatform expertise for shared code architecture and platform integration
---

## User Input
$ARGUMENTS

## Purpose

Provides deep KMP expertise for architecting shared Kotlin modules that work seamlessly across iOS and Android. This skill covers shared module structure, ViewModel patterns, iOS framework export, and platform-specific integration patterns.

## When to Use

- Platform detected as `kmp` (via `platform-detection.md`)
- Project has `shared/` directory with `build.gradle.kts`
- Project has both `iosApp/` and `androidApp/` directories
- Files contain `commonMain`, `iosMain`, `androidMain` source sets

## Quality Gates

| Gate ID | Purpose | Threshold |
|---------|---------|-----------|
| QG-KMP-001 | Framework export configured | PASS/FAIL |
| QG-KMP-002 | iOS framework builds | PASS/FAIL |
| QG-KMP-003 | Android integration works | PASS/FAIL |
| QG-BIND-001 | ViewModel binding coverage | 100% |
| QG-BIND-002 | StateFlow observation coverage | 100% |
| QG-BIND-003 | No platform stubs | 0 violations |

## Execution Steps

### 1. Validate Project Structure

```text
VERIFY structure:
  shared/
  ├── build.gradle.kts           # Multiplatform configuration
  └── src/
      ├── commonMain/kotlin/     # Shared code (MUST have most logic)
      │   ├── domain/            # Entities, use cases
      │   ├── data/              # Repositories, data sources
      │   └── presentation/      # ViewModels, UI state
      ├── iosMain/kotlin/        # iOS-specific implementations
      │   ├── di/                # Koin iOS initializer
      │   └── util/              # Flow wrappers for Swift
      └── androidMain/kotlin/    # Android-specific implementations

IF structure missing:
  RECOMMEND: Create missing directories
  PROVIDE: Scaffolding commands
```

### 2. Configure Gradle Build

```kotlin
// shared/build.gradle.kts - REQUIRED configuration
plugins {
    kotlin("multiplatform")
    id("com.android.library")
}

kotlin {
    // Targets
    androidTarget {
        compilations.all {
            kotlinOptions {
                jvmTarget = "17"
            }
        }
    }

    // iOS targets with framework export
    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach {
        it.binaries.framework {
            baseName = "shared"
            isStatic = true
        }
    }

    sourceSets {
        commonMain.dependencies {
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
            implementation("io.insert-koin:koin-core:3.5.0")
        }
        androidMain.dependencies {
            implementation("io.insert-koin:koin-android:3.5.0")
        }
        iosMain.dependencies {
            // iOS-specific dependencies
        }
    }
}
```

### 3. ViewModel Pattern for KMP

```kotlin
// commonMain - Shared ViewModel base
abstract class ViewModel {
    protected val viewModelScope = CoroutineScope(
        SupervisorJob() + Dispatchers.Main.immediate
    )

    open fun onCleared() {
        viewModelScope.cancel()
    }
}

// commonMain - Feature ViewModel
class LibraryViewModel(
    private val repository: BookRepository
) : ViewModel() {

    private val _state = MutableStateFlow(LibraryState())
    val state: StateFlow<LibraryState> = _state.asStateFlow()

    fun loadBooks() {
        viewModelScope.launch {
            _state.update { it.copy(loading = true) }
            repository.getBooks()
                .onSuccess { books ->
                    _state.update { it.copy(books = books, loading = false) }
                }
                .onFailure { error ->
                    _state.update { it.copy(error = error.message, loading = false) }
                }
        }
    }

    fun addBook(book: Book) {
        viewModelScope.launch {
            repository.addBook(book)
            loadBooks() // Refresh
        }
    }
}

data class LibraryState(
    val books: List<Book> = emptyList(),
    val loading: Boolean = false,
    val error: String? = null
)
```

### 4. iOS Export Pattern

```kotlin
// iosMain/kotlin/di/KoinIOS.kt
object KoinApplication {
    val shared = initKoin()
    val koin get() = shared.koin
}

fun initKoin(): KoinApplication = startKoin {
    modules(sharedModule)
}

// iosMain/kotlin/util/CommonFlow.kt
class CommonFlow<T>(private val origin: Flow<T>) : Flow<T> by origin {
    fun watch(block: (T) -> Unit): Closeable {
        val job = CoroutineScope(Dispatchers.Main).launch {
            collect { block(it) }
        }
        return object : Closeable {
            override fun close() {
                job.cancel()
            }
        }
    }
}

fun <T> Flow<T>.asCommonFlow(): CommonFlow<T> = CommonFlow(this)

// iosMain/kotlin/presentation/ViewModelWrappers.kt
@ObjCName("LibraryViewModelWrapper")
class LibraryViewModelWrapper {
    private val viewModel: LibraryViewModel = KoinApplication.koin.get()

    val state: CommonFlow<LibraryState> = viewModel.state.asCommonFlow()

    fun loadBooks() = viewModel.loadBooks()

    fun addBook(title: String, author: String) {
        viewModel.addBook(Book(title = title, author = author))
    }

    fun onCleared() = viewModel.onCleared()
}
```

### 5. Swift Integration Pattern

```swift
// iosApp/Sources/ViewModels/LibraryViewModel.swift
import shared
import SwiftUI
import Combine

@MainActor
class LibraryViewModelObserver: ObservableObject {
    private let wrapper = LibraryViewModelWrapper()
    private var stateWatcher: Closeable?

    @Published var state: LibraryState = LibraryState(
        books: [],
        loading: false,
        error: nil
    )

    init() {
        stateWatcher = wrapper.state.watch { [weak self] newState in
            Task { @MainActor in
                self?.state = newState
            }
        }
    }

    func loadBooks() {
        wrapper.loadBooks()
    }

    func addBook(title: String, author: String) {
        wrapper.addBook(title: title, author: author)
    }

    deinit {
        stateWatcher?.close()
        wrapper.onCleared()
    }
}

// iosApp/Sources/Views/LibraryView.swift
struct LibraryView: View {
    @StateObject private var viewModel = LibraryViewModelObserver()

    var body: some View {
        NavigationView {
            Group {
                if viewModel.state.loading {
                    ProgressView()
                } else if let error = viewModel.state.error {
                    Text(error)
                } else {
                    List(viewModel.state.books, id: \.id) { book in
                        BookRow(book: book)
                    }
                }
            }
            .navigationTitle("Library")
        }
        .onAppear {
            viewModel.loadBooks()
        }
    }
}
```

### 6. Android Integration Pattern

```kotlin
// androidApp/src/main/kotlin/App.kt
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@App)
            modules(sharedModule)
        }
    }
}

// androidApp/src/main/kotlin/ui/LibraryScreen.kt
@Composable
fun LibraryScreen(viewModel: LibraryViewModel = koinViewModel()) {
    val state by viewModel.state.collectAsState()

    Scaffold(
        topBar = { TopAppBar(title = { Text("Library") }) }
    ) { padding ->
        Box(modifier = Modifier.padding(padding)) {
            when {
                state.loading -> CircularProgressIndicator()
                state.error != null -> Text(state.error!!)
                else -> LazyColumn {
                    items(state.books) { book ->
                        BookRow(book)
                    }
                }
            }
        }
    }

    LaunchedEffect(Unit) {
        viewModel.loadBooks()
    }
}
```

## Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Swift sees mangled names | Missing @ObjCName | Add @ObjCName to all iOS-exposed classes |
| Flow doesn't update UI | Swift can't observe StateFlow | Use CommonFlow wrapper with Closeable |
| Memory leak on iOS | StateFlow observer not closed | Call close() in deinit |
| Framework not found | Missing Framework Search Paths | Add paths in Xcode Build Settings |
| Coroutine scope leak | Not tied to lifecycle | Cancel scope in onCleared() |
| expect/actual mismatch | Missing platform implementation | Verify all expect have actual |

## Verification Commands

```bash
# Build iOS framework
./gradlew :shared:linkDebugFrameworkIosArm64

# Build Android library
./gradlew :shared:assembleDebug

# Run shared tests
./gradlew :shared:allTests

# Check iOS integration
xcodebuild -project iosApp/iosApp.xcodeproj -scheme iosApp -sdk iphonesimulator build

# Check Android integration
./gradlew :androidApp:assembleDebug
```

## Output

This skill produces:
- Validated KMP project structure
- Correctly configured build.gradle.kts
- ViewModel with StateFlow patterns
- iOS wrapper classes with @ObjCName
- CommonFlow for Swift consumption
- Platform-specific DI initialization
- Binding test recommendations

## Integration with Spec Kit

- **`/speckit.plan`**: Recommends KMP architecture when multiplatform detected
- **`/speckit.tasks`**: Injects KMP-specific tasks (Phase 2e-BINDING)
- **`/speckit.implement`**: Uses KMP patterns for implementation
- **`/speckit.analyze`**: Validates QG-BIND-001/002/003 gates

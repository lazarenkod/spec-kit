---
description: Comprehensive mobile testing strategy including binding tests, E2E, and platform-specific testing
---

## User Input
$ARGUMENTS

## Purpose

Provides testing strategy guidance for mobile applications. Covers the test pyramid, binding tests for cross-platform projects, E2E testing with Maestro/Detox, and platform-specific testing patterns.

## When to Use

- During `/speckit.tasks` to generate test tasks
- During `/speckit.implement` Wave 2 (Test Scaffolding)
- During `/speckit.analyze` for test coverage validation
- When implementing TDD for mobile features

## Test Pyramid for Mobile

```text
              ┌──────────────┐
              │     E2E      │  10% - Critical user journeys
              │   (Maestro)  │  Device/Simulator tests
              ├──────────────┤
             ╱│  Integration │╲  20% - API, Database, Platform
            ╱ │    Tests     │ ╲  MockWebServer, platform mocks
           ╱  ├──────────────┤  ╲
          ╱   │    Unit      │   ╲  70% - Business logic
         ╱    │    Tests     │    ╲  Fast, isolated, no device
        ───────┴──────────────┴───────

SPECIAL FOR CROSS-PLATFORM:
        ┌──────────────────┐
        │  Binding Tests   │  Platform UI ↔ Shared Code
        │  (100% required) │  Verifies no TODO/stubs
        └──────────────────┘
```

## Execution Steps

### 1. Unit Testing

```text
UNIT TEST SCOPE:
- ViewModels / BLoCs
- Use Cases
- Repositories (with mocks)
- Utilities and helpers
- Data transformations

REQUIREMENTS:
- No device/emulator needed
- No network calls (mocked)
- No database (in-memory or mocked)
- Fast execution (< 1ms per test)

COVERAGE THRESHOLD: ≥ 80%
```

#### KMP Unit Tests

```kotlin
// shared/src/commonTest/kotlin/presentation/LibraryViewModelTest.kt
class LibraryViewModelTest {
    private lateinit var viewModel: LibraryViewModel
    private val mockRepository = mockk<BookRepository>()

    @BeforeTest
    fun setup() {
        viewModel = LibraryViewModel(mockRepository)
    }

    @Test
    fun `loadBooks updates state with books on success`() = runTest {
        // Given
        val books = listOf(Book(id = "1", title = "Test", author = "Author"))
        coEvery { mockRepository.getBooks() } returns Result.success(books)

        // When
        viewModel.loadBooks()

        // Then
        val state = viewModel.state.value
        assertEquals(books, state.books)
        assertFalse(state.loading)
        assertNull(state.error)
    }

    @Test
    fun `loadBooks updates state with error on failure`() = runTest {
        // Given
        coEvery { mockRepository.getBooks() } returns Result.failure(Exception("Network error"))

        // When
        viewModel.loadBooks()

        // Then
        val state = viewModel.state.value
        assertTrue(state.books.isEmpty())
        assertFalse(state.loading)
        assertEquals("Network error", state.error)
    }
}
```

#### Flutter Unit Tests

```dart
// test/features/library/presentation/bloc/library_bloc_test.dart
void main() {
  late LibraryBloc bloc;
  late MockBookRepository mockRepository;

  setUp(() {
    mockRepository = MockBookRepository();
    bloc = LibraryBloc(mockRepository);
  });

  tearDown(() => bloc.close());

  group('LoadBooks', () {
    blocTest<LibraryBloc, LibraryState>(
      'emits [loading, loaded] when successful',
      build: () {
        when(() => mockRepository.getBooks())
            .thenAnswer((_) async => [testBook]);
        return bloc;
      },
      act: (bloc) => bloc.add(const LibraryEvent.loadBooks()),
      expect: () => [
        const LibraryState.loading(),
        LibraryState.loaded([testBook]),
      ],
    );
  });
}
```

### 2. Binding Tests (Cross-Platform Critical)

```text
PURPOSE:
Verify that platform UI (SwiftUI/Compose) correctly calls shared ViewModels.
Catches bugs where unit tests pass but UI has TODO/stub implementations.

COVERAGE REQUIREMENT: 100% of ViewModel public methods

GENERATES TASKS:
FOR EACH ViewModel in shared/src/commonMain/**/*ViewModel.kt:
  FOR EACH public method:
    - [ ] T### [BINDING-TEST:{ViewModel}:{method}] Verify binding
```

#### iOS Binding Tests

```swift
// iosApp/iosAppTests/binding/LibraryViewModelBindingTests.swift
import XCTest
@testable import iosApp
@testable import shared

final class LibraryViewModelBindingTests: XCTestCase {
    private var mockViewModel: MockLibraryViewModel!
    private var wrapper: LibraryViewModelWrapper!

    override func setUp() {
        super.setUp()
        mockViewModel = MockLibraryViewModel()
        wrapper = LibraryViewModelWrapper(viewModel: mockViewModel)
    }

    func test_loadBooks_callsViewModel() {
        // When
        wrapper.loadBooks()

        // Then
        XCTAssertTrue(mockViewModel.loadBooksCalled)
    }

    func test_addBook_passesCorrectParameters() {
        // When
        wrapper.addBook(title: "Test", author: "Author")

        // Then
        XCTAssertTrue(mockViewModel.addBookCalled)
        XCTAssertEqual(mockViewModel.lastBookTitle, "Test")
        XCTAssertEqual(mockViewModel.lastBookAuthor, "Author")
    }

    func test_state_observesChanges() {
        // Given
        let expectation = expectation(description: "State updated")
        var receivedState: LibraryState?

        let watcher = wrapper.state.watch { state in
            receivedState = state
            expectation.fulfill()
        }

        // When
        mockViewModel.emitState(LibraryState(books: [testBook], loading: false, error: nil))

        // Then
        wait(for: [expectation], timeout: 1.0)
        XCTAssertEqual(receivedState?.books.count, 1)

        watcher.close()
    }
}

// Mock implementation
class MockLibraryViewModel: LibraryViewModelProtocol {
    var loadBooksCalled = false
    var addBookCalled = false
    var lastBookTitle: String?
    var lastBookAuthor: String?

    private let stateSubject = CurrentValueSubject<LibraryState, Never>(
        LibraryState(books: [], loading: false, error: nil)
    )

    func loadBooks() {
        loadBooksCalled = true
    }

    func addBook(title: String, author: String) {
        addBookCalled = true
        lastBookTitle = title
        lastBookAuthor = author
    }

    func emitState(_ state: LibraryState) {
        stateSubject.send(state)
    }
}
```

#### Android Binding Tests

```kotlin
// androidApp/src/androidTest/kotlin/binding/LibraryViewModelBindingTest.kt
class LibraryViewModelBindingTest {
    private lateinit var mockViewModel: MockLibraryViewModel
    private lateinit var wrapper: LibraryViewModelWrapper

    @Before
    fun setup() {
        mockViewModel = MockLibraryViewModel()
        wrapper = LibraryViewModelWrapper(mockViewModel)
    }

    @Test
    fun loadBooks_callsViewModel() {
        // When
        wrapper.loadBooks()

        // Then
        assertTrue(mockViewModel.loadBooksCalled)
    }

    @Test
    fun addBook_passesCorrectParameters() {
        // When
        wrapper.addBook("Test", "Author")

        // Then
        assertTrue(mockViewModel.addBookCalled)
        assertEquals("Test", mockViewModel.lastBookTitle)
        assertEquals("Author", mockViewModel.lastBookAuthor)
    }

    @Test
    fun state_collectsUpdates() = runTest {
        // Given
        val states = mutableListOf<LibraryState>()
        val job = launch {
            wrapper.state.collect { states.add(it) }
        }

        // When
        mockViewModel.emitState(LibraryState(listOf(testBook), false, null))
        advanceUntilIdle()

        // Then
        assertEquals(2, states.size) // Initial + emitted
        assertEquals(1, states.last().books.size)

        job.cancel()
    }
}
```

### 3. Integration Testing

```text
INTEGRATION TEST SCOPE:
- Repository + API (with MockWebServer)
- Repository + Database (with in-memory DB)
- Navigation flows
- Platform services (with test doubles)

REQUIREMENTS:
- May need device/emulator
- Network mocked at HTTP level
- Real database (in-memory)
- Medium execution time
```

#### API Integration Test

```kotlin
// shared/src/commonTest/kotlin/data/BookRepositoryIntegrationTest.kt
class BookRepositoryIntegrationTest {
    private lateinit var mockWebServer: MockWebServer
    private lateinit var repository: BookRepository

    @BeforeTest
    fun setup() {
        mockWebServer = MockWebServer()
        mockWebServer.start()

        val api = createTestApi(mockWebServer.url("/"))
        val database = createInMemoryDatabase()
        repository = BookRepositoryImpl(api, database)
    }

    @AfterTest
    fun teardown() {
        mockWebServer.shutdown()
    }

    @Test
    fun `getBooks fetches from API and caches in database`() = runTest {
        // Given
        mockWebServer.enqueue(MockResponse()
            .setBody("""[{"id":"1","title":"Test","author":"Author"}]""")
            .setHeader("Content-Type", "application/json"))

        // When
        val result = repository.getBooks()

        // Then
        assertTrue(result.isSuccess)
        assertEquals(1, result.getOrNull()?.size)

        // Verify cached
        val cached = repository.getCachedBooks()
        assertEquals(1, cached.size)
    }

    @Test
    fun `getBooks returns cached data when offline`() = runTest {
        // Given
        repository.cacheBooks(listOf(testBook))
        mockWebServer.enqueue(MockResponse().setResponseCode(503))

        // When
        val result = repository.getBooks()

        // Then
        assertTrue(result.isSuccess)
        assertEquals(1, result.getOrNull()?.size)
    }
}
```

### 4. E2E Testing with Maestro

```yaml
# maestro/flows/library_browse.yaml
appId: com.app.bookreader
---
- launchApp:
    clearState: true

- assertVisible: "My Library"

- tapOn: "Add Book"

- inputText:
    id: "title_input"
    text: "Test Book"

- inputText:
    id: "author_input"
    text: "Test Author"

- tapOn: "Save"

- assertVisible: "Test Book"
- assertVisible: "Test Author"

- tapOn: "Test Book"

- assertVisible: "Start Reading"

- tapOn: "Start Reading"

- assertVisible:
    text: "Chapter 1"
    timeout: 5000

- back

- assertVisible: "My Library"
```

```yaml
# maestro/flows/reader_settings.yaml
appId: com.app.bookreader
---
- launchApp

- runFlow: "open_book.yaml"

- tapOn:
    id: "settings_button"

- assertVisible: "Font Size"

- tapOn: "Increase Font"
- tapOn: "Increase Font"

# Verify font size persists
- back
- tapOn:
    id: "settings_button"

- assertVisible:
    id: "font_size_value"
    text: "18"
```

### 5. Accessibility Testing

```text
ACCESSIBILITY REQUIREMENTS:

iOS:
- All interactive elements have accessibilityLabel
- accessibilityHint for non-obvious actions
- accessibilityTraits set correctly
- VoiceOver navigation tested

Android:
- contentDescription for all images/icons
- labelFor linking labels to inputs
- TalkBack navigation tested
- Touch target ≥ 48dp

TESTING TOOLS:
- iOS: Accessibility Inspector (Xcode)
- Android: Accessibility Scanner app
- Both: Manual VoiceOver/TalkBack testing
```

```swift
// iOS Accessibility Test
func test_libraryScreen_accessibility() {
    let app = XCUIApplication()
    app.launch()

    // Verify all interactive elements are accessible
    let addButton = app.buttons["Add Book"]
    XCTAssertTrue(addButton.exists)
    XCTAssertTrue(addButton.isHittable)

    // Verify book list is accessible
    let bookList = app.collectionViews["book_list"]
    XCTAssertTrue(bookList.exists)

    // Check dynamic type scaling
    XCTAssertGreaterThanOrEqual(
        app.staticTexts["Library"].frame.height,
        24 // Minimum readable height
    )
}
```

## Quality Gates

| Gate ID | Purpose | Threshold | Blocks |
|---------|---------|-----------|--------|
| QG-TEST-MOBILE-001 | Unit test coverage | ≥ 80% | Implementation |
| QG-TEST-MOBILE-002 | Binding test coverage | 100% | Wave 4 |
| QG-TEST-MOBILE-003 | E2E critical paths | 100% | Release |
| QG-BIND-001 | ViewModel method binding | 100% | Wave 4 |
| QG-BIND-002 | StateFlow observation | 100% | Wave 4 |
| QG-BIND-003 | No platform stubs | 0 violations | Wave 4 |

## Test Task Generation

```text
FOR EACH ViewModel in shared/src/commonMain/**/*ViewModel.kt:
  PARSE public methods
  FOR EACH method:
    GENERATE:
      - [ ] T### [UNIT-TEST:{ViewModel}:{method}] Unit test for {method}
      - [ ] T### [BINDING-TEST:{ViewModel}:{method}] iOS/Android binding test

FOR EACH acceptance scenario AS-xxx:
  IF type == E2E:
    GENERATE:
      - [ ] T### [E2E-TEST:AS-{xxx}] Maestro flow for {scenario}
```

## Verification Commands

```bash
# KMP
./gradlew :shared:allTests
./gradlew :shared:koverReport  # Coverage

# Flutter
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html

# React Native
npm test -- --coverage

# iOS Binding Tests
xcodebuild test -project iosApp.xcodeproj -scheme iosApp -destination 'platform=iOS Simulator,name=iPhone 15'

# Android Binding Tests
./gradlew :androidApp:connectedAndroidTest

# E2E with Maestro
maestro test maestro/flows/
```

## Output

This skill produces:
- Test task list for tasks.md
- Unit test scaffolding per ViewModel
- Binding test scaffolding per platform
- Maestro flow templates for E2E
- Coverage report configuration
- CI/CD test pipeline configuration

## Integration with Spec Kit

- **`/speckit.tasks`**: Generates test tasks from spec
- **`/speckit.implement`**: Scaffolds tests in Wave 2
- **`/speckit.analyze`**: Validates test coverage
- **MQS calculation**: Testing contributes 20 points to MQS

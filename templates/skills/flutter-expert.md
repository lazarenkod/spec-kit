---
description: Flutter expertise for widget architecture, state management, and cross-platform development
---

## User Input
$ARGUMENTS

## Purpose

Provides deep Flutter expertise for building production-ready mobile applications. Covers feature-first architecture, BLoC/Cubit state management, platform channels, and performance optimization.

## When to Use

- Platform detected as `flutter` (via `platform-detection.md`)
- Project has `pubspec.yaml` with Flutter dependencies
- Project has `lib/main.dart` entry point
- Code uses Dart language with Flutter widgets

## Quality Gates

| Gate ID | Purpose | Threshold |
|---------|---------|-----------|
| QG-FLUTTER-001 | Widget tests for all screens | ≥ 80% |
| QG-FLUTTER-002 | Consistent state management | PASS/FAIL |
| QG-FLUTTER-003 | Platform channels documented | PASS/FAIL |
| QG-FLUTTER-004 | No hardcoded strings/colors | 0 violations |

## Execution Steps

### 1. Validate Project Structure

```text
VERIFY structure:
  lib/
  ├── core/                      # Shared utilities
  │   ├── di/                    # Dependency injection (GetIt)
  │   ├── network/               # HTTP client, interceptors
  │   ├── storage/               # Local storage, cache
  │   └── theme/                 # App theme, colors, typography
  ├── features/                  # Feature-first organization
  │   └── {feature}/
  │       ├── data/              # Repositories, models, data sources
  │       │   ├── models/
  │       │   ├── repositories/
  │       │   └── sources/
  │       ├── domain/            # Entities, use cases (optional clean arch)
  │       │   ├── entities/
  │       │   └── usecases/
  │       └── presentation/      # UI layer
  │           ├── bloc/          # BLoC/Cubit for state
  │           ├── pages/         # Screen widgets
  │           └── widgets/       # Reusable components
  ├── l10n/                      # Localization
  └── main.dart

IF structure missing:
  RECOMMEND: Create feature directories
  PROVIDE: flutter_bloc, get_it setup
```

### 2. Configure Dependencies

```yaml
# pubspec.yaml - Recommended dependencies
dependencies:
  flutter:
    sdk: flutter

  # State Management
  flutter_bloc: ^8.1.3
  bloc: ^8.1.2

  # Dependency Injection
  get_it: ^7.6.4
  injectable: ^2.3.2

  # Networking
  dio: ^5.4.0
  retrofit: ^4.0.3

  # Local Storage
  hive: ^2.2.3
  hive_flutter: ^1.1.0

  # Navigation
  go_router: ^13.0.0

  # Utilities
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1
  equatable: ^2.0.5

dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.5
  mocktail: ^1.0.1
  build_runner: ^2.4.7
  freezed: ^2.4.5
  json_serializable: ^6.7.1
  injectable_generator: ^2.4.1
```

### 3. BLoC Pattern Implementation

```dart
// features/library/presentation/bloc/library_bloc.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

part 'library_bloc.freezed.dart';
part 'library_event.dart';
part 'library_state.dart';

class LibraryBloc extends Bloc<LibraryEvent, LibraryState> {
  final BookRepository _repository;

  LibraryBloc(this._repository) : super(const LibraryState.initial()) {
    on<LibraryEvent>((event, emit) async {
      await event.when(
        loadBooks: () => _onLoadBooks(emit),
        addBook: (book) => _onAddBook(book, emit),
        deleteBook: (id) => _onDeleteBook(id, emit),
      );
    });
  }

  Future<void> _onLoadBooks(Emitter<LibraryState> emit) async {
    emit(const LibraryState.loading());
    try {
      final books = await _repository.getBooks();
      emit(LibraryState.loaded(books));
    } catch (e) {
      emit(LibraryState.error(e.toString()));
    }
  }

  Future<void> _onAddBook(Book book, Emitter<LibraryState> emit) async {
    await _repository.addBook(book);
    add(const LibraryEvent.loadBooks());
  }

  Future<void> _onDeleteBook(String id, Emitter<LibraryState> emit) async {
    await _repository.deleteBook(id);
    add(const LibraryEvent.loadBooks());
  }
}

// library_event.dart
part of 'library_bloc.dart';

@freezed
class LibraryEvent with _$LibraryEvent {
  const factory LibraryEvent.loadBooks() = _LoadBooks;
  const factory LibraryEvent.addBook(Book book) = _AddBook;
  const factory LibraryEvent.deleteBook(String id) = _DeleteBook;
}

// library_state.dart
part of 'library_bloc.dart';

@freezed
class LibraryState with _$LibraryState {
  const factory LibraryState.initial() = _Initial;
  const factory LibraryState.loading() = _Loading;
  const factory LibraryState.loaded(List<Book> books) = _Loaded;
  const factory LibraryState.error(String message) = _Error;
}
```

### 4. Widget Implementation

```dart
// features/library/presentation/pages/library_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class LibraryPage extends StatelessWidget {
  const LibraryPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => getIt<LibraryBloc>()
        ..add(const LibraryEvent.loadBooks()),
      child: const LibraryView(),
    );
  }
}

class LibraryView extends StatelessWidget {
  const LibraryView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(context.l10n.libraryTitle), // Localized
      ),
      body: BlocBuilder<LibraryBloc, LibraryState>(
        builder: (context, state) {
          return state.when(
            initial: () => const SizedBox.shrink(),
            loading: () => const Center(
              child: CircularProgressIndicator(),
            ),
            loaded: (books) => books.isEmpty
                ? const EmptyLibraryWidget()
                : BookListWidget(books: books),
            error: (message) => ErrorWidget(message: message),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddBookDialog(context),
        child: const Icon(Icons.add),
      ),
    );
  }

  void _showAddBookDialog(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (_) => AddBookSheet(
        onSubmit: (book) {
          context.read<LibraryBloc>().add(LibraryEvent.addBook(book));
          Navigator.pop(context);
        },
      ),
    );
  }
}
```

### 5. Dependency Injection Setup

```dart
// core/di/injection.dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';

final getIt = GetIt.instance;

@InjectableInit()
Future<void> configureDependencies() async => getIt.init();

// core/di/injection.config.dart (generated)
// Run: dart run build_runner build

// features/library/data/repositories/book_repository_impl.dart
@LazySingleton(as: BookRepository)
class BookRepositoryImpl implements BookRepository {
  final BookApi _api;
  final BookLocalSource _local;

  BookRepositoryImpl(this._api, this._local);

  @override
  Future<List<Book>> getBooks() async {
    try {
      final books = await _api.getBooks();
      await _local.cacheBooks(books);
      return books;
    } catch (_) {
      return _local.getCachedBooks();
    }
  }
}
```

### 6. Platform Channels

```dart
// core/platform/native_bridge.dart
import 'package:flutter/services.dart';

class NativeBridge {
  static const _channel = MethodChannel('com.app/native');

  /// Trigger haptic feedback (uses platform-specific implementation)
  static Future<void> hapticFeedback() async {
    try {
      await _channel.invokeMethod('hapticFeedback');
    } on PlatformException catch (e) {
      debugPrint('Haptic feedback failed: $e');
    }
  }

  /// Get device biometric type
  static Future<BiometricType> getBiometricType() async {
    try {
      final result = await _channel.invokeMethod<String>('getBiometricType');
      return BiometricType.values.firstWhere(
        (t) => t.name == result,
        orElse: () => BiometricType.none,
      );
    } on PlatformException {
      return BiometricType.none;
    }
  }
}

enum BiometricType { none, fingerprint, face, iris }
```

### 7. Performance Optimization

```dart
// Performance best practices

// 1. Use const constructors
const MyWidget(); // ✓ Reuses instance
MyWidget();       // ✗ Creates new instance

// 2. Use ListView.builder for long lists
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
); // ✓ Lazy loading

ListView(
  children: items.map((i) => ItemWidget(i)).toList(),
); // ✗ Builds all at once

// 3. Use RepaintBoundary for isolated updates
RepaintBoundary(
  child: AnimatedWidget(), // Repaints independently
);

// 4. Cache expensive computations
final computed = useMemoized(() => expensiveComputation(), [dep]);

// 5. Use Image.cacheWidth/cacheHeight
Image.network(
  url,
  cacheWidth: 200,  // Resize in memory
  cacheHeight: 200,
);
```

### 8. Testing Patterns

```dart
// test/features/library/presentation/bloc/library_bloc_test.dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockBookRepository extends Mock implements BookRepository {}

void main() {
  late LibraryBloc bloc;
  late MockBookRepository repository;

  setUp(() {
    repository = MockBookRepository();
    bloc = LibraryBloc(repository);
  });

  tearDown(() => bloc.close());

  group('LibraryBloc', () {
    blocTest<LibraryBloc, LibraryState>(
      'emits [loading, loaded] when loadBooks succeeds',
      build: () {
        when(() => repository.getBooks())
            .thenAnswer((_) async => [testBook]);
        return bloc;
      },
      act: (bloc) => bloc.add(const LibraryEvent.loadBooks()),
      expect: () => [
        const LibraryState.loading(),
        LibraryState.loaded([testBook]),
      ],
    );

    blocTest<LibraryBloc, LibraryState>(
      'emits [loading, error] when loadBooks fails',
      build: () {
        when(() => repository.getBooks())
            .thenThrow(Exception('Network error'));
        return bloc;
      },
      act: (bloc) => bloc.add(const LibraryEvent.loadBooks()),
      expect: () => [
        const LibraryState.loading(),
        const LibraryState.error('Exception: Network error'),
      ],
    );
  });
}

// Widget test
testWidgets('LibraryPage displays books', (tester) async {
  when(() => mockBloc.state).thenReturn(
    LibraryState.loaded([testBook]),
  );

  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider.value(
        value: mockBloc,
        child: const LibraryPage(),
      ),
    ),
  );

  expect(find.text(testBook.title), findsOneWidget);
});
```

## Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Widget rebuild spam | Missing const, BlocBuilder too high | Use const, granular BlocBuilders |
| Memory leak | Stream not closed | Use BlocProvider, cancel subscriptions |
| Janky scrolling | Heavy itemBuilder | Use const widgets, cache images |
| State lost on rotate | Using StatefulWidget wrong | Use BLoC, persist to storage |
| Platform crash | Missing null check in channel | Always catch PlatformException |

## Verification Commands

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html

# Analyze code
flutter analyze

# Check for unused dependencies
dart pub deps --no-dev

# Build for release
flutter build apk --release
flutter build ios --release
```

## Output

This skill produces:
- Feature-first project structure
- BLoC/Cubit state management setup
- GetIt dependency injection configuration
- Platform channel integration patterns
- Widget test templates
- Performance optimization checklist

## Integration with Spec Kit

- **`/speckit.plan`**: Recommends Flutter patterns when detected
- **`/speckit.tasks`**: Generates BLoC-specific implementation tasks
- **`/speckit.implement`**: Uses Flutter patterns for implementation
- **`/speckit.analyze`**: Validates QG-FLUTTER gates

# Flutter Integration Test Template

## Purpose

Template for creating Flutter integration tests that:
- Run on real devices/emulators
- Test complete user journeys
- Map to acceptance scenarios (AS-xxx)
- Support TDD Red/Green phases

## Directory Structure

```text
your_app/
  integration_test/
    app_test.dart           # Main integration test entry
    robots/                 # Page object pattern
      home_robot.dart
      login_robot.dart
    utils/
      test_helpers.dart     # Common utilities
  test_driver/
    integration_test.dart   # Driver for running tests
```

## Main Test File

```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:{{app_name}}/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Feature: {{feature_name}}', () {
    // @speckit:AS-001
    testWidgets('AS-001: {{scenario_description}}', (tester) async {
      // Arrange
      app.main();
      await tester.pumpAndSettle();

      // Act
      // TODO: Implement user actions
      await tester.tap(find.byKey(const Key('button_key')));
      await tester.pumpAndSettle();

      // Assert - MUST FAIL initially (TDD Red)
      expect(find.text('Expected Result'), findsOneWidget);
    });

    // @speckit:AS-002
    testWidgets('AS-002: {{scenario_description}}', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // TODO: Implement test
      expect(find.byType(ExpectedWidget), findsOneWidget);
    });
  });
}
```

## Robot Pattern (Page Objects)

```dart
// integration_test/robots/login_robot.dart
import 'package:flutter_test/flutter_test.dart';

class LoginRobot {
  final WidgetTester tester;

  LoginRobot(this.tester);

  Future<void> enterEmail(String email) async {
    await tester.enterText(
      find.byKey(const Key('email_field')),
      email,
    );
    await tester.pumpAndSettle();
  }

  Future<void> enterPassword(String password) async {
    await tester.enterText(
      find.byKey(const Key('password_field')),
      password,
    );
    await tester.pumpAndSettle();
  }

  Future<void> tapLogin() async {
    await tester.tap(find.byKey(const Key('login_button')));
    await tester.pumpAndSettle();
  }

  Future<void> verifyErrorMessage(String message) async {
    expect(find.text(message), findsOneWidget);
  }

  Future<void> verifyLoggedIn() async {
    expect(find.byKey(const Key('home_screen')), findsOneWidget);
  }
}
```

## Test Driver

```dart
// test_driver/integration_test.dart
import 'package:integration_test/integration_test_driver.dart';

Future<void> main() => integrationDriver();
```

## Running Tests

```bash
# Run on connected device/emulator
flutter test integration_test/

# Run on specific device
flutter test integration_test/ --device-id=emulator-5554

# Run with coverage
flutter test integration_test/ --coverage

# Run specific test file
flutter test integration_test/app_test.dart
```

## CI Configuration

```yaml
# .github/workflows/mobile-tests.yml
mobile-tests:
  runs-on: macos-latest
  steps:
    - uses: actions/checkout@v4
    - uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'

    - name: Start iOS Simulator
      run: |
        xcrun simctl boot "iPhone 15 Pro"

    - name: Run integration tests
      run: flutter test integration_test/
```

## TDD Workflow

### Red Phase (Wave 2)
1. Write test with assertion that WILL FAIL
2. Add `@speckit:AS-xxx` annotation
3. Run test - verify it fails
4. Mark AS-xxx as having test coverage

### Green Phase (Wave 3)
1. Implement feature code
2. Run test - should pass now
3. Verify coverage threshold (70%)

## Common Assertions

```dart
// Widget exists
expect(find.byType(MyWidget), findsOneWidget);

// Text exists
expect(find.text('Hello'), findsOneWidget);

// Widget with key
expect(find.byKey(const Key('my_key')), findsOneWidget);

// Multiple widgets
expect(find.byType(ListTile), findsNWidgets(5));

// Widget not found
expect(find.text('Error'), findsNothing);

// Widget enabled/disabled
expect(tester.widget<ElevatedButton>(find.byType(ElevatedButton)).enabled, isTrue);
```

## Traceability

| AS-xxx | Test | File |
|--------|------|------|
| AS-001 | {{scenario}} | integration_test/app_test.dart:15 |
| AS-002 | {{scenario}} | integration_test/app_test.dart:28 |

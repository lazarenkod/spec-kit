# Flutter Platform Constitution

**Inherits from**: `constitution.base.md` → `constitution.domain.md` (if applicable)

## Overview

Flutter enables building natively compiled applications for mobile, web, and desktop from a single codebase using Dart. This constitution defines mandatory principles for Flutter projects.

## Platform Principles

### FLT-001: Project Structure [MUST]

Flutter projects MUST follow the standard structure:

```text
project/
├── lib/
│   ├── main.dart              # App entry point
│   ├── app.dart               # MaterialApp/CupertinoApp
│   ├── features/              # Feature-based modules
│   │   └── feature_name/
│   │       ├── presentation/  # Widgets, pages
│   │       ├── domain/        # Use cases, entities
│   │       └── data/          # Repositories, data sources
│   ├── core/                  # Shared utilities
│   │   ├── theme/
│   │   ├── router/
│   │   └── di/
│   └── l10n/                  # Localization
├── test/                      # Unit and widget tests
├── integration_test/          # Integration tests
├── ios/                       # iOS native code
├── android/                   # Android native code
└── pubspec.yaml               # Dependencies
```

**Rationale**: Feature-based structure scales better than layer-based for medium+ projects.

### FLT-002: State Management [MUST]

State management MUST use one of the approved patterns:

| Pattern | Use Case | Package |
|---------|----------|---------|
| BLoC | Complex business logic | `flutter_bloc` |
| Riverpod | Dependency injection + state | `flutter_riverpod` |
| Provider | Simple state sharing | `provider` |

**Rationale**: Consistent state management prevents spaghetti code and improves testability.

### FLT-003: iOS Configuration [MUST]

iOS project MUST be properly configured:

**ios/Podfile**:
```ruby
platform :ios, '12.0'  # Minimum iOS version

post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '12.0'
    end
  end
end
```

**ios/Runner/Info.plist** (required keys):
- `NSCameraUsageDescription` (if using camera)
- `NSPhotoLibraryUsageDescription` (if accessing photos)
- `NSLocationWhenInUseUsageDescription` (if using location)

**Rationale**: Missing configurations cause App Store rejection.

### FLT-004: Android Configuration [MUST]

Android project MUST be properly configured:

**android/app/build.gradle**:
```groovy
android {
    compileSdk 34

    defaultConfig {
        minSdk 21
        targetSdk 34
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

**Rationale**: Proper SDK targets ensure Play Store compatibility.

### FLT-005: Null Safety [MUST]

All Dart code MUST be null-safe:

```yaml
# pubspec.yaml
environment:
  sdk: '>=3.0.0 <4.0.0'
```

**Rationale**: Null safety prevents runtime null reference errors.

### FLT-006: Widget Testing [MUST]

All user-facing widgets MUST have widget tests:

```dart
testWidgets('Counter increments', (tester) async {
  await tester.pumpWidget(const MyApp());
  expect(find.text('0'), findsOneWidget);
  await tester.tap(find.byIcon(Icons.add));
  await tester.pump();
  expect(find.text('1'), findsOneWidget);
});
```

**Coverage target**: >= 80% for widgets

**Rationale**: Widget tests catch UI regressions faster than manual testing.

### FLT-007: Platform Channels [SHOULD]

Platform-specific native code SHOULD use method channels:

```dart
// Dart side
static const platform = MethodChannel('com.example/native');

Future<String> getNativeData() async {
  try {
    return await platform.invokeMethod('getData');
  } on PlatformException catch (e) {
    return 'Error: ${e.message}';
  }
}
```

**Rationale**: Method channels provide type-safe native communication.

### FLT-008: Error Handling [MUST]

Global error handling MUST be configured:

```dart
void main() {
  FlutterError.onError = (details) {
    // Log to crash reporting service
    FirebaseCrashlytics.instance.recordFlutterError(details);
  };

  PlatformDispatcher.instance.onError = (error, stack) {
    // Log async errors
    FirebaseCrashlytics.instance.recordError(error, stack);
    return true;
  };

  runApp(const MyApp());
}
```

**Rationale**: Unhandled exceptions crash the app; global handling enables graceful recovery.

## Integration Requirements

### iOS Setup

1. **Install dependencies**: `cd ios && pod install`
2. **Configure signing**: Xcode → Signing & Capabilities
3. **Add capabilities**: Push Notifications, Background Modes (if needed)
4. **Verify**: `flutter build ios --debug`

### Android Setup

1. **Configure signing**: Create keystore, add to build.gradle
2. **Add permissions**: AndroidManifest.xml
3. **Configure ProGuard**: proguard-rules.pro
4. **Verify**: `flutter build apk --debug`

### Development Workflow

1. **Check environment**: `flutter doctor`
2. **Get dependencies**: `flutter pub get`
3. **Run app**: `flutter run`
4. **Run tests**: `flutter test`
5. **Build release**: `flutter build ios/apk --release`

## Quality Gates

| Gate ID | Check | Severity |
|---------|-------|----------|
| QG-FLT-001 | flutter doctor passes | CRITICAL |
| QG-FLT-002 | iOS build succeeds | CRITICAL |
| QG-FLT-003 | Android build succeeds | CRITICAL |
| QG-FLT-004 | flutter analyze has no errors | HIGH |
| QG-FLT-005 | Widget test coverage >= 80% | HIGH |
| QG-FLT-006 | No deprecated APIs used | MEDIUM |

## Testing Strategy

### Unit Tests

- Business logic, use cases
- Repository implementations
- BLoC/Cubit state transitions

### Widget Tests

- All screens and major components
- User interaction flows
- Error state rendering

### Integration Tests

- Critical user journeys
- Navigation flows
- Platform channel communication

## Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| CocoaPods error | Outdated pods | `cd ios && pod repo update && pod install` |
| Gradle sync fail | Wrong JDK | Use JDK 17+ |
| Hot reload broken | StatefulWidget issue | Restart app |
| iOS build slow | CocoaPods cache | Use CocoaPods CDN |
| Android 64-bit crash | Missing ABI | Add all ABIs in build.gradle |

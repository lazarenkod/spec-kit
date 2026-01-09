# React Native Platform Constitution

**Inherits from**: `constitution.base.md` → `constitution.domain.md` (if applicable)

## Overview

React Native enables building native mobile apps using JavaScript and React. This constitution defines mandatory principles for React Native projects.

## Platform Principles

### RN-001: Project Structure [MUST]

React Native projects MUST follow a scalable structure:

```text
project/
├── src/
│   ├── app/                   # App entry, navigation
│   │   ├── App.tsx
│   │   └── navigation/
│   ├── features/              # Feature modules
│   │   └── feature_name/
│   │       ├── screens/
│   │       ├── components/
│   │       ├── hooks/
│   │       └── api/
│   ├── shared/                # Shared code
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── theme/
│   └── services/              # API, storage, etc.
├── __tests__/                 # Tests
├── ios/                       # iOS native
├── android/                   # Android native
├── package.json
├── metro.config.js
└── react-native.config.js
```

**Rationale**: Feature-based structure improves code discoverability and team scaling.

### RN-002: TypeScript [MUST]

All code MUST be written in TypeScript:

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

**Rationale**: TypeScript catches errors at compile time and improves IDE support.

### RN-003: iOS Configuration [MUST]

iOS project MUST be properly configured:

**ios/Podfile**:
```ruby
platform :ios, '13.4'  # Minimum for React Native 0.73+

use_frameworks! :linkage => :static

# For Hermes
use_react_native_codegen!(react_native_path)
```

**Info.plist** required keys based on features:
- `NSCameraUsageDescription`
- `NSPhotoLibraryUsageDescription`
- `NSLocationWhenInUseUsageDescription`

**Rationale**: Incorrect configuration causes build failures and App Store rejection.

### RN-004: Android Configuration [MUST]

Android project MUST be properly configured:

**android/gradle.properties**:
```properties
# New Architecture (React Native 0.71+)
newArchEnabled=true

# Hermes engine
hermesEnabled=true

# Optimize build
org.gradle.jvmargs=-Xmx4g
org.gradle.parallel=true
```

**android/app/build.gradle**:
```groovy
android {
    compileSdk 34

    defaultConfig {
        minSdk 23
        targetSdk 34
    }

    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

**Rationale**: Proper configuration ensures Play Store compatibility and optimal performance.

### RN-005: Navigation [MUST]

Navigation MUST use React Navigation:

```typescript
// App.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator<RootStackParamList>();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

**Rationale**: React Navigation is the de facto standard with best native performance.

### RN-006: State Management [MUST]

State management MUST use one of:

| Pattern | Use Case | Package |
|---------|----------|---------|
| Zustand | Simple global state | `zustand` |
| Redux Toolkit | Complex state with middleware | `@reduxjs/toolkit` |
| React Query | Server state | `@tanstack/react-query` |
| Jotai | Atomic state | `jotai` |

**Rationale**: Consistent state management prevents prop drilling and improves predictability.

### RN-007: Native Modules [SHOULD]

Native modules SHOULD use Turbo Modules (New Architecture):

```typescript
// specs/NativeCalculator.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  multiply(a: number, b: number): number;
}

export default TurboModuleRegistry.getEnforcing<Spec>('Calculator');
```

**Rationale**: Turbo Modules provide synchronous native calls and better type safety.

### RN-008: Error Boundaries [MUST]

Error boundaries MUST wrap critical sections:

```typescript
class ErrorBoundary extends React.Component<Props, State> {
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to crash reporting
    crashlytics().recordError(error);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

**Rationale**: Unhandled JS errors crash the app; boundaries enable graceful recovery.

### RN-009: Metro Configuration [MUST]

Metro bundler MUST be properly configured:

```javascript
// metro.config.js
const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

const defaultConfig = getDefaultConfig(__dirname);

const config = {
  resolver: {
    sourceExts: [...defaultConfig.resolver.sourceExts, 'svg'],
  },
  transformer: {
    babelTransformerPath: require.resolve('react-native-svg-transformer'),
  },
};

module.exports = mergeConfig(defaultConfig, config);
```

**Rationale**: Proper Metro config enables SVG support, custom transforms, and performance.

## Integration Requirements

### iOS Setup

1. **Install dependencies**: `cd ios && bundle install && bundle exec pod install`
2. **Configure signing**: Xcode → Signing & Capabilities
3. **Add capabilities**: Push Notifications, Background Modes
4. **Verify**: `npx react-native run-ios`

### Android Setup

1. **Configure signing**: Create keystore, update gradle
2. **Add permissions**: AndroidManifest.xml
3. **Configure ProGuard**: proguard-rules.pro
4. **Verify**: `npx react-native run-android`

### Development Workflow

1. **Check environment**: `npx react-native doctor`
2. **Install dependencies**: `npm install` or `yarn`
3. **Start Metro**: `npx react-native start`
4. **Run app**: `npx react-native run-ios/android`
5. **Run tests**: `npm test`

## Quality Gates

| Gate ID | Check | Severity |
|---------|-------|----------|
| QG-RN-001 | npx react-native doctor passes | CRITICAL |
| QG-RN-002 | iOS build succeeds | CRITICAL |
| QG-RN-003 | Android build succeeds | CRITICAL |
| QG-RN-004 | TypeScript compiles without errors | HIGH |
| QG-RN-005 | ESLint passes | HIGH |
| QG-RN-006 | Jest test coverage >= 70% | HIGH |

## Testing Strategy

### Unit Tests

- Business logic, utilities
- Custom hooks
- State management (reducers, stores)

### Component Tests

- React Native Testing Library
- Screen rendering
- User interactions

### E2E Tests

- Detox or Maestro
- Critical user flows
- Platform-specific behavior

## Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Metro cache stale | Changed config | `npx react-native start --reset-cache` |
| CocoaPods error | Version mismatch | `cd ios && pod deintegrate && pod install` |
| Android build fail | Wrong JDK | Use JDK 17 |
| Flipper crash | Debug build issue | Disable Flipper or update |
| Hot reload broken | Large change | Full restart with `r` |
| New Arch issues | Incompatible lib | Check library compatibility |

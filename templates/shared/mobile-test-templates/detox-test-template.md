# Detox Test Template (React Native)

## Purpose

Template for creating Detox E2E tests for React Native apps that:
- Test on both iOS and Android
- Support gray-box testing (control app state)
- Map to acceptance scenarios (AS-xxx)
- Follow TDD Red/Green phases

## Directory Structure

```text
your_app/
  e2e/
    config/
      detox.config.js      # Detox configuration
    tests/
      firstTest.e2e.js     # Test files
      login.e2e.js
    utils/
      testHelpers.js       # Common utilities
    screens/               # Screen objects
      loginScreen.js
      homeScreen.js
  .detoxrc.js              # Detox RC file
```

## Detox Configuration

```javascript
// .detoxrc.js
module.exports = {
  testRunner: {
    args: {
      '$0': 'jest',
      config: 'e2e/jest.config.js'
    },
    jest: {
      setupTimeout: 120000
    }
  },
  apps: {
    'ios.debug': {
      type: 'ios.app',
      binaryPath: 'ios/build/Build/Products/Debug-iphonesimulator/{{app_name}}.app',
      build: 'xcodebuild -workspace ios/{{app_name}}.xcworkspace -scheme {{app_name}} -configuration Debug -sdk iphonesimulator -derivedDataPath ios/build'
    },
    'android.debug': {
      type: 'android.apk',
      binaryPath: 'android/app/build/outputs/apk/debug/app-debug.apk',
      build: 'cd android && ./gradlew assembleDebug assembleAndroidTest -DtestBuildType=debug && cd ..'
    }
  },
  devices: {
    simulator: {
      type: 'ios.simulator',
      device: {
        type: 'iPhone 15 Pro'
      }
    },
    emulator: {
      type: 'android.emulator',
      device: {
        avdName: 'Pixel_6_API_33'
      }
    }
  },
  configurations: {
    'ios.sim.debug': {
      device: 'simulator',
      app: 'ios.debug'
    },
    'android.emu.debug': {
      device: 'emulator',
      app: 'android.debug'
    }
  }
};
```

## Main Test File

```javascript
// e2e/tests/feature.e2e.js

describe('Feature: {{feature_name}}', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  // @speckit:AS-001
  it('AS-001: {{scenario_description}}', async () => {
    // Arrange - app launched in beforeAll

    // Act
    await element(by.id('login_button')).tap();
    await element(by.id('email_input')).typeText('test@example.com');
    await element(by.id('password_input')).typeText('password123');
    await element(by.id('submit_button')).tap();

    // Assert - MUST FAIL initially (TDD Red)
    await expect(element(by.id('home_screen'))).toBeVisible();
  });

  // @speckit:AS-002
  it('AS-002: {{scenario_description}}', async () => {
    // TODO: Implement test - must FAIL initially
    await expect(element(by.text('Expected Text'))).toBeVisible();
  });
});
```

## Screen Objects Pattern

```javascript
// e2e/screens/loginScreen.js

class LoginScreen {
  get emailInput() {
    return element(by.id('email_input'));
  }

  get passwordInput() {
    return element(by.id('password_input'));
  }

  get loginButton() {
    return element(by.id('login_button'));
  }

  get errorMessage() {
    return element(by.id('error_message'));
  }

  async login(email, password) {
    await this.emailInput.typeText(email);
    await this.passwordInput.typeText(password);
    await this.loginButton.tap();
  }

  async verifyErrorVisible(message) {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toHaveText(message);
  }
}

module.exports = new LoginScreen();
```

## Jest Configuration

```javascript
// e2e/jest.config.js
module.exports = {
  rootDir: '..',
  testMatch: ['<rootDir>/e2e/tests/**/*.e2e.js'],
  testTimeout: 120000,
  maxWorkers: 1,
  globalSetup: 'detox/runners/jest/globalSetup',
  globalTeardown: 'detox/runners/jest/globalTeardown',
  reporters: ['detox/runners/jest/reporter'],
  testEnvironment: 'detox/runners/jest/testEnvironment',
  verbose: true
};
```

## Running Tests

```bash
# Build app for testing
detox build --configuration ios.sim.debug
detox build --configuration android.emu.debug

# Run tests
detox test --configuration ios.sim.debug
detox test --configuration android.emu.debug

# Run specific test file
detox test --configuration ios.sim.debug e2e/tests/login.e2e.js

# Run with recording (for debugging)
detox test --configuration ios.sim.debug --record-videos all
```

## CI Configuration

```yaml
# .github/workflows/detox-tests.yml
jobs:
  ios-tests:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci
      - run: brew tap wix/brew && brew install applesimutils
      - run: detox build --configuration ios.sim.debug
      - run: detox test --configuration ios.sim.debug

  android-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      - name: Start emulator
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          script: |
            npm ci
            detox build --configuration android.emu.debug
            detox test --configuration android.emu.debug
```

## Common Matchers

```javascript
// Visibility
await expect(element(by.id('element'))).toBeVisible();
await expect(element(by.id('element'))).not.toBeVisible();

// Text content
await expect(element(by.id('title'))).toHaveText('Hello');

// Existence (even if not visible)
await expect(element(by.id('element'))).toExist();

// Focusable
await expect(element(by.id('input'))).toBeFocused();

// By different selectors
element(by.id('testID'));
element(by.text('Button Text'));
element(by.label('Accessibility Label'));
element(by.type('UIButton'));
```

## Common Actions

```javascript
// Tap
await element(by.id('button')).tap();

// Type text
await element(by.id('input')).typeText('Hello');
await element(by.id('input')).clearText();
await element(by.id('input')).replaceText('New text');

// Scroll
await element(by.id('scrollView')).scroll(100, 'down');
await element(by.id('scrollView')).scrollTo('bottom');

// Swipe
await element(by.id('card')).swipe('left');

// Long press
await element(by.id('item')).longPress();

// Multi-tap
await element(by.id('item')).multiTap(2);
```

## TDD Workflow

### Red Phase (Wave 2)
1. Write test with assertion that WILL FAIL
2. Add `@speckit:AS-xxx` annotation in comment
3. Build app: `detox build`
4. Run test - verify it fails

### Green Phase (Wave 3)
1. Implement feature in React Native
2. Rebuild: `detox build`
3. Run test - should pass now

## Traceability

| AS-xxx | Test | File |
|--------|------|------|
| AS-001 | {{scenario}} | e2e/tests/feature.e2e.js:15 |
| AS-002 | {{scenario}} | e2e/tests/feature.e2e.js:28 |

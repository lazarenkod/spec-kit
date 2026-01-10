# Test Framework Registry

**Version**: 1.0.0
**Last Updated**: 2026-01-10
**Purpose**: Centralized registry of test frameworks for universal auto-installation

This registry contains metadata for all supported test frameworks across multiple categories, languages, and platforms. It serves as the single source of truth for framework detection, installation, and verification.

---

## Registry Schema

Each framework entry contains:

```yaml
framework_id: <unique-identifier>
name: <display-name>
description: <brief-description>
category: <test-category>
languages: [<supported-languages>]
platforms: [<supported-platforms>]
priority: <0-100>  # Higher = preferred when multiple options fit
alternative_to: [<alternative-frameworks>]
compatible_with: [<coexist-frameworks>]

detection:
  explicit_markers:
    - pattern: <regex-or-string>
      source: [tasks.md, plan.md]
  project_files:
    - file: <filename>
      exists: true | contains: <pattern>
  dependencies:
    - package: <package-name>
      type: dev | prod

installation:
  <package-manager>:
    command: <install-command>
    config_gen: <optional-config-generation>
    manual_steps: <platform-specific-steps>

verification:
  - command: <verification-command>
    expected_exit_code: <number>
    expected_output_contains: [<optional-patterns>]

configuration:
  required_files: [<config-files>]
  template: <optional-template-path>

quality_gate: <associated-quality-gate>
prerequisites: [<system-requirements>]
docs_url: <official-documentation>
```

---

## Categories

- **unit_integration**: Unit and integration testing frameworks
- **e2e_web**: End-to-end web testing frameworks
- **e2e_mobile**: End-to-end mobile testing frameworks
- **e2e_desktop**: End-to-end desktop testing frameworks
- **api**: API testing frameworks
- **performance**: Performance and load testing frameworks
- **visual**: Visual regression testing frameworks
- **contract**: Contract testing frameworks

---

## Unit & Integration Testing Frameworks

### jest

```yaml
framework_id: jest
name: Jest
description: Delightful JavaScript Testing Framework with built-in assertions and mocking
category: unit_integration
languages: [javascript, typescript]
platforms: [node, react, react-native, next, nest, vue, angular]
priority: 90
alternative_to: [mocha, jasmine, ava]
compatible_with: [playwright, cypress, supertest]

detection:
  explicit_markers:
    - pattern: "Test Framework: Jest"
      source: [tasks.md, plan.md]
    - pattern: "jest"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"jest"'
    - file: jest.config.js
      exists: true
    - file: jest.config.ts
      exists: true
  dependencies:
    - package: jest
      type: dev

installation:
  npm:
    command: "npm install -D jest @types/jest ts-jest"
    config_gen: |
      # Use template instead of interactive init
      # npx jest --init is interactive
  yarn:
    command: "yarn add -D jest @types/jest ts-jest"
  pnpm:
    command: "pnpm add -D jest @types/jest ts-jest"

verification:
  - command: "npx jest --version"
    expected_exit_code: 0
  - command: "npx jest --listTests || true"
    expected_exit_code: 0

configuration:
  required_files:
    - jest.config.js OR jest.config.ts OR package.json:jest
  template: templates/shared/test-configs/jest.config.ts

quality_gate: QG-TEST-002
docs_url: https://jestjs.io/docs/getting-started
```

### vitest

```yaml
framework_id: vitest
name: Vitest
description: Blazing fast unit test framework powered by Vite
category: unit_integration
languages: [javascript, typescript]
platforms: [vite, vue, react, svelte]
priority: 95  # Higher priority for Vite projects
alternative_to: [jest, mocha]
compatible_with: [playwright, cypress]

detection:
  explicit_markers:
    - pattern: "Test Framework: Vitest"
      source: [tasks.md, plan.md]
    - pattern: "vitest"
      source: [tasks.md, plan.md]
  project_files:
    - file: vite.config.ts
      exists: true
    - file: vitest.config.ts
      exists: true
    - file: package.json
      contains: '"vitest"'
  dependencies:
    - package: vitest
      type: dev

installation:
  npm:
    command: "npm install -D vitest @vitest/ui"
  yarn:
    command: "yarn add -D vitest @vitest/ui"
  pnpm:
    command: "pnpm add -D vitest @vitest/ui"

verification:
  - command: "npx vitest --version"
    expected_exit_code: 0

configuration:
  required_files:
    - vitest.config.ts OR vite.config.ts
  template: templates/shared/test-configs/vitest.config.ts

quality_gate: QG-TEST-002
docs_url: https://vitest.dev/guide/
```

### pytest

```yaml
framework_id: pytest
name: pytest
description: The pytest framework makes it easy to write small tests, yet scales to support complex functional testing
category: unit_integration
languages: [python]
platforms: [python, fastapi, django, flask]
priority: 95
alternative_to: [unittest, nose2]
compatible_with: [playwright, selenium]

detection:
  explicit_markers:
    - pattern: "Test Framework: pytest"
      source: [tasks.md, plan.md]
    - pattern: "pytest"
      source: [tasks.md, plan.md]
  project_files:
    - file: pytest.ini
      exists: true
    - file: pyproject.toml
      contains: '[tool.pytest'
    - file: requirements.txt
      contains: 'pytest'
  dependencies:
    - package: pytest
      type: dev

installation:
  pip:
    command: "pip install pytest pytest-asyncio pytest-cov pytest-mock"
  poetry:
    command: "poetry add --group dev pytest pytest-asyncio pytest-cov pytest-mock"
  pipenv:
    command: "pipenv install --dev pytest pytest-asyncio pytest-cov pytest-mock"

verification:
  - command: "pytest --version"
    expected_exit_code: 0
  - command: "pytest --collect-only"
    expected_exit_code: 0

configuration:
  required_files:
    - pytest.ini OR pyproject.toml
  template: templates/shared/test-configs/pytest.ini

quality_gate: QG-TEST-002
docs_url: https://docs.pytest.org/
```

### go-test

```yaml
framework_id: go-test
name: Go test
description: Built-in Go testing framework
category: unit_integration
languages: [go]
platforms: [go]
priority: 100  # Built-in, always preferred
alternative_to: []
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: Go test"
      source: [tasks.md, plan.md]
    - pattern: "go test"
      source: [tasks.md, plan.md]
  project_files:
    - file: go.mod
      exists: true
  dependencies: []  # Built-in

installation:
  go:
    command: "# No installation needed - built into Go"
    manual_steps: |
      Go test is built into the Go toolchain.
      No additional installation required.

verification:
  - command: "go test ./... -count=0"
    expected_exit_code: 0

configuration:
  required_files: []  # No config needed
  template: null

quality_gate: QG-TEST-002
docs_url: https://go.dev/doc/tutorial/add-a-test
```

### cargo-test

```yaml
framework_id: cargo-test
name: cargo test
description: Built-in Rust testing framework
category: unit_integration
languages: [rust]
platforms: [rust]
priority: 100  # Built-in, always preferred
alternative_to: []
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: cargo test"
      source: [tasks.md, plan.md]
    - pattern: "cargo test"
      source: [tasks.md, plan.md]
  project_files:
    - file: Cargo.toml
      exists: true
  dependencies: []  # Built-in

installation:
  cargo:
    command: "# No installation needed - built into Cargo"
    manual_steps: |
      Cargo test is built into the Rust toolchain.
      No additional installation required.

verification:
  - command: "cargo test --no-run"
    expected_exit_code: 0

configuration:
  required_files: []  # No config needed
  template: null

quality_gate: QG-TEST-002
docs_url: https://doc.rust-lang.org/book/ch11-00-testing.html
```

### junit5

```yaml
framework_id: junit5
name: JUnit 5
description: The next generation of JUnit testing framework
category: unit_integration
languages: [java, kotlin]
platforms: [jvm, spring, android]
priority: 90
alternative_to: [junit4, testng]
compatible_with: [rest-assured, mockito]

detection:
  explicit_markers:
    - pattern: "Test Framework: JUnit"
      source: [tasks.md, plan.md]
    - pattern: "JUnit 5"
      source: [tasks.md, plan.md]
  project_files:
    - file: build.gradle.kts
      contains: 'junit-jupiter'
    - file: pom.xml
      contains: 'junit-jupiter'
  dependencies:
    - package: junit-jupiter
      type: dev

installation:
  gradle:
    command: |
      # Add to build.gradle.kts:
      dependencies {
          testImplementation("org.junit.jupiter:junit-jupiter:5.10.1")
          testRuntimeOnly("org.junit.platform:junit-platform-launcher")
      }
      tasks.test {
          useJUnitPlatform()
      }
  maven:
    command: |
      # Add to pom.xml:
      <dependency>
          <groupId>org.junit.jupiter</groupId>
          <artifactId>junit-jupiter</artifactId>
          <version>5.10.1</version>
          <scope>test</scope>
      </dependency>

verification:
  - command: "./gradlew test --dry-run"
    expected_exit_code: 0
  - command: "mvn test -DskipTests"
    expected_exit_code: 0

configuration:
  required_files:
    - build.gradle.kts OR pom.xml
  template: null

quality_gate: QG-TEST-002
docs_url: https://junit.org/junit5/docs/current/user-guide/
```

### testng

```yaml
framework_id: testng
name: TestNG
description: Testing framework inspired by JUnit with more powerful features
category: unit_integration
languages: [java]
platforms: [jvm, spring]
priority: 75
alternative_to: [junit5]
compatible_with: [rest-assured]

detection:
  explicit_markers:
    - pattern: "Test Framework: TestNG"
      source: [tasks.md, plan.md]
  project_files:
    - file: build.gradle.kts
      contains: 'testng'
    - file: pom.xml
      contains: 'testng'
  dependencies:
    - package: testng
      type: dev

installation:
  gradle:
    command: |
      dependencies {
          testImplementation("org.testng:testng:7.8.0")
      }
  maven:
    command: |
      <dependency>
          <groupId>org.testng</groupId>
          <artifactId>testng</artifactId>
          <version>7.8.0</version>
          <scope>test</scope>
      </dependency>

verification:
  - command: "./gradlew test --dry-run"
    expected_exit_code: 0

configuration:
  required_files:
    - testng.xml
  template: templates/shared/test-configs/testng.xml

quality_gate: QG-TEST-002
docs_url: https://testng.org/doc/documentation-main.html
```

### rspec

```yaml
framework_id: rspec
name: RSpec
description: Behaviour Driven Development for Ruby
category: unit_integration
languages: [ruby]
platforms: [ruby, rails]
priority: 90
alternative_to: [minitest]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: RSpec"
      source: [tasks.md, plan.md]
  project_files:
    - file: Gemfile
      contains: 'rspec'
    - file: spec/spec_helper.rb
      exists: true
  dependencies:
    - package: rspec
      type: dev

installation:
  bundler:
    command: "bundle add rspec --group=test"
    config_gen: "rspec --init"

verification:
  - command: "rspec --version"
    expected_exit_code: 0

configuration:
  required_files:
    - .rspec
    - spec/spec_helper.rb
  template: null

quality_gate: QG-TEST-002
docs_url: https://rspec.info/documentation/
```

### xunit

```yaml
framework_id: xunit
name: xUnit.net
description: Free, open source, community-focused unit testing tool for .NET
category: unit_integration
languages: [csharp, fsharp]
platforms: [dotnet]
priority: 85
alternative_to: [nunit, mstest]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: xUnit"
      source: [tasks.md, plan.md]
  project_files:
    - file: "*.csproj"
      contains: 'xunit'
  dependencies:
    - package: xunit
      type: dev

installation:
  dotnet:
    command: "dotnet add package xunit && dotnet add package xunit.runner.visualstudio"

verification:
  - command: "dotnet test --list-tests"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://xunit.net/docs/getting-started/netcore/cmdline
```

### nunit

```yaml
framework_id: nunit
name: NUnit
description: Unit-testing framework for all .NET languages
category: unit_integration
languages: [csharp, fsharp]
platforms: [dotnet]
priority: 80
alternative_to: [xunit, mstest]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: NUnit"
      source: [tasks.md, plan.md]
  project_files:
    - file: "*.csproj"
      contains: 'nunit'
  dependencies:
    - package: nunit
      type: dev

installation:
  dotnet:
    command: "dotnet add package NUnit && dotnet add package NUnit3TestAdapter"

verification:
  - command: "dotnet test --list-tests"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://docs.nunit.org/
```

### unittest

```yaml
framework_id: unittest
name: unittest
description: Built-in Python unit testing framework
category: unit_integration
languages: [python]
platforms: [python]
priority: 60  # Lower priority - pytest preferred
alternative_to: [pytest]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: unittest"
      source: [tasks.md, plan.md]
  project_files:
    - file: "test_*.py"
      contains: 'import unittest'
  dependencies: []  # Built-in

installation:
  pip:
    command: "# No installation needed - built into Python"
    manual_steps: |
      unittest is built into Python standard library.
      No additional installation required.

verification:
  - command: "python -m unittest --help"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://docs.python.org/3/library/unittest.html
```

### mocha

```yaml
framework_id: mocha
name: Mocha
description: Simple, flexible JavaScript test framework
category: unit_integration
languages: [javascript, typescript]
platforms: [node]
priority: 70
alternative_to: [jest, ava]
compatible_with: [chai, sinon]

detection:
  explicit_markers:
    - pattern: "Test Framework: Mocha"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"mocha"'
    - file: .mocharc.json
      exists: true
  dependencies:
    - package: mocha
      type: dev

installation:
  npm:
    command: "npm install -D mocha @types/mocha chai @types/chai"
  yarn:
    command: "yarn add -D mocha @types/mocha chai @types/chai"
  pnpm:
    command: "pnpm add -D mocha @types/mocha chai @types/chai"

verification:
  - command: "npx mocha --version"
    expected_exit_code: 0

configuration:
  required_files:
    - .mocharc.json OR mocha.opts
  template: templates/shared/test-configs/.mocharc.json

quality_gate: QG-TEST-002
docs_url: https://mochajs.org/
```

---

## E2E Web Testing Frameworks

### playwright

```yaml
framework_id: playwright
name: Playwright
description: Fast and reliable end-to-end testing for modern web apps
category: e2e_web
languages: [javascript, typescript, python, java, csharp]
platforms: [web]
priority: 95
alternative_to: [cypress, selenium]
compatible_with: [jest, vitest]

detection:
  explicit_markers:
    - pattern: "Test Framework: Playwright"
      source: [tasks.md, plan.md]
    - pattern: "playwright"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"@playwright/test"'
    - file: playwright.config.ts
      exists: true
  dependencies:
    - package: "@playwright/test"
      type: dev

installation:
  npm:
    command: "npm install -D @playwright/test"
    config_gen: "npx playwright install chromium"
  yarn:
    command: "yarn add -D @playwright/test && npx playwright install chromium"
  pnpm:
    command: "pnpm add -D @playwright/test && npx playwright install chromium"
  pip:
    command: "pip install playwright && playwright install chromium"
  maven:
    command: |
      <dependency>
          <groupId>com.microsoft.playwright</groupId>
          <artifactId>playwright</artifactId>
          <version>1.40.0</version>
      </dependency>

verification:
  - command: "npx playwright --version"
    expected_exit_code: 0

configuration:
  required_files:
    - playwright.config.ts
  template: templates/shared/test-configs/playwright.config.ts

quality_gate: QG-TEST-002
docs_url: https://playwright.dev/docs/intro
```

### cypress

```yaml
framework_id: cypress
name: Cypress
description: Fast, easy and reliable testing for anything that runs in a browser
category: e2e_web
languages: [javascript, typescript]
platforms: [web]
priority: 85
alternative_to: [playwright, selenium]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: Cypress"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"cypress"'
    - file: cypress.config.ts
      exists: true
  dependencies:
    - package: cypress
      type: dev

installation:
  npm:
    command: "npm install -D cypress"
  yarn:
    command: "yarn add -D cypress"
  pnpm:
    command: "pnpm add -D cypress"

verification:
  - command: "npx cypress --version"
    expected_exit_code: 0

configuration:
  required_files:
    - cypress.config.ts
  template: templates/shared/test-configs/cypress.config.ts

quality_gate: QG-TEST-002
docs_url: https://docs.cypress.io/guides/overview/why-cypress
```

### selenium

```yaml
framework_id: selenium
name: Selenium WebDriver
description: Browser automation framework
category: e2e_web
languages: [javascript, typescript, python, java, csharp, ruby]
platforms: [web]
priority: 70
alternative_to: [playwright, cypress]
compatible_with: [junit5, pytest]

detection:
  explicit_markers:
    - pattern: "Test Framework: Selenium"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"selenium-webdriver"'
  dependencies:
    - package: selenium-webdriver
      type: dev

installation:
  npm:
    command: "npm install -D selenium-webdriver chromedriver"
  pip:
    command: "pip install selenium webdriver-manager"
  maven:
    command: |
      <dependency>
          <groupId>org.seleniumhq.selenium</groupId>
          <artifactId>selenium-java</artifactId>
          <version>4.16.0</version>
      </dependency>

verification:
  - command: "node -e \"require('selenium-webdriver')\""
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://www.selenium.dev/documentation/webdriver/
```

### puppeteer

```yaml
framework_id: puppeteer
name: Puppeteer
description: Node library which provides a high-level API to control Chrome/Chromium
category: e2e_web
languages: [javascript, typescript]
platforms: [web]
priority: 75
alternative_to: [playwright]
compatible_with: [jest]

detection:
  explicit_markers:
    - pattern: "Test Framework: Puppeteer"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"puppeteer"'
  dependencies:
    - package: puppeteer
      type: dev

installation:
  npm:
    command: "npm install -D puppeteer"
  yarn:
    command: "yarn add -D puppeteer"
  pnpm:
    command: "pnpm add -D puppeteer"

verification:
  - command: "node -e \"require('puppeteer')\""
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://pptr.dev/
```

### webdriverio

```yaml
framework_id: webdriverio
name: WebdriverIO
description: Next-gen browser and mobile automation test framework
category: e2e_web
languages: [javascript, typescript]
platforms: [web]
priority: 70
alternative_to: [playwright, cypress]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: WebdriverIO"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"@wdio/cli"'
    - file: wdio.conf.ts
      exists: true
  dependencies:
    - package: "@wdio/cli"
      type: dev

installation:
  npm:
    command: "npm install -D @wdio/cli"
    config_gen: "npx wdio config"

verification:
  - command: "npx wdio --version"
    expected_exit_code: 0

configuration:
  required_files:
    - wdio.conf.ts
  template: null

quality_gate: QG-TEST-002
docs_url: https://webdriver.io/docs/gettingstarted
```

---

## E2E Mobile Testing Frameworks

### maestro

```yaml
framework_id: maestro
name: Maestro
description: The easiest way to automate UI testing for mobile apps
category: e2e_mobile
languages: [yaml]
platforms: [ios, android]
priority: 90
alternative_to: [detox, appium]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: Maestro"
      source: [tasks.md, plan.md]
  project_files:
    - file: .maestro
      exists: true
  dependencies: []  # Standalone CLI

installation:
  curl:
    command: 'curl -Ls "https://get.maestro.mobile.dev" | bash'
    manual_steps: |
      1. Install via curl: curl -Ls "https://get.maestro.mobile.dev" | bash
      2. Add to PATH: export PATH=$PATH:$HOME/.maestro/bin
      3. Verify: maestro --version

verification:
  - command: "maestro --version"
    expected_exit_code: 0

configuration:
  required_files:
    - .maestro/
  template: null

quality_gate: QG-TEST-002
docs_url: https://maestro.mobile.dev/getting-started/installing-maestro
```

### xcuitest

```yaml
framework_id: xcuitest
name: XCUITest
description: Apple's official UI testing framework for iOS
category: e2e_mobile
languages: [swift]
platforms: [ios]
priority: 95
alternative_to: [detox, appium]
compatible_with: [xctest]

detection:
  explicit_markers:
    - pattern: "Test Framework: XCUITest"
      source: [tasks.md, plan.md]
    - pattern: "XCUITest"
      source: [tasks.md, plan.md]
  project_files:
    - file: "*.xcodeproj"
      exists: true
  dependencies: []  # Built into Xcode

installation:
  xcode:
    command: "# Built into Xcode - no separate installation"
    manual_steps: |
      XCUITest is built into Xcode.
      1. Install Xcode from App Store (macOS only)
      2. Create UI Test target in Xcode project
      3. Verify: xcodebuild -list | grep -i test

verification:
  - command: "xcodebuild -version"
    expected_exit_code: 0
  - command: "xcodebuild -list | grep -i test"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
prerequisites:
  - macOS
  - Xcode installed
docs_url: https://developer.apple.com/documentation/xctest/user_interface_tests
```

### espresso

```yaml
framework_id: espresso
name: Espresso
description: Google's Android UI testing framework
category: e2e_mobile
languages: [java, kotlin]
platforms: [android]
priority: 95
alternative_to: [detox, appium]
compatible_with: [junit5]

detection:
  explicit_markers:
    - pattern: "Test Framework: Espresso"
      source: [tasks.md, plan.md]
  project_files:
    - file: build.gradle.kts
      contains: 'androidx.test.espresso'
  dependencies:
    - package: espresso-core
      type: dev

installation:
  gradle:
    command: |
      dependencies {
          androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
          androidTestImplementation("androidx.test:runner:1.5.2")
          androidTestImplementation("androidx.test:rules:1.5.0")
      }

verification:
  - command: "./gradlew tasks | grep connectedAndroidTest"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
prerequisites:
  - Android SDK
  - ANDROID_HOME environment variable
docs_url: https://developer.android.com/training/testing/espresso
```

### detox

```yaml
framework_id: detox
name: Detox
description: Gray box end-to-end testing framework for mobile apps
category: e2e_mobile
languages: [javascript, typescript]
platforms: [react-native, ios, android]
priority: 90
alternative_to: [maestro, appium]
compatible_with: [jest]

detection:
  explicit_markers:
    - pattern: "Test Framework: Detox"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"detox"'
    - file: .detoxrc.js
      exists: true
  dependencies:
    - package: detox
      type: dev

installation:
  npm:
    command: "npm install -D detox detox-cli"
    config_gen: "npx detox init -r jest"
  yarn:
    command: "yarn add -D detox detox-cli && npx detox init -r jest"

verification:
  - command: "npx detox --version"
    expected_exit_code: 0

configuration:
  required_files:
    - .detoxrc.js
  template: templates/shared/test-configs/.detoxrc.js

quality_gate: QG-TEST-002
docs_url: https://wix.github.io/Detox/docs/introduction/getting-started
```

### flutter-test

```yaml
framework_id: flutter-test
name: flutter_test
description: Built-in Flutter testing framework
category: e2e_mobile
languages: [dart]
platforms: [flutter, ios, android, web]
priority: 95
alternative_to: []
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: Flutter test"
      source: [tasks.md, plan.md]
  project_files:
    - file: pubspec.yaml
      contains: 'flutter_test'
  dependencies:
    - package: flutter_test
      type: dev

installation:
  flutter:
    command: "# Built into Flutter SDK"
    manual_steps: |
      flutter_test is included with Flutter SDK.
      Add integration_test package for E2E tests:

      flutter pub add dev:integration_test
      flutter pub add dev:flutter_test

verification:
  - command: "flutter test --version"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
prerequisites:
  - Flutter SDK
docs_url: https://docs.flutter.dev/testing/overview
```

### appium

```yaml
framework_id: appium
name: Appium
description: Cross-platform mobile automation framework
category: e2e_mobile
languages: [javascript, typescript, python, java, ruby]
platforms: [ios, android]
priority: 75
alternative_to: [maestro, detox]
compatible_with: [junit5, pytest]

detection:
  explicit_markers:
    - pattern: "Test Framework: Appium"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"appium"'
  dependencies:
    - package: appium
      type: dev

installation:
  npm:
    command: "npm install -D appium"
  pip:
    command: "pip install Appium-Python-Client"

verification:
  - command: "npx appium --version"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://appium.io/docs/en/2.0/intro/
```

### xctest

```yaml
framework_id: xctest
name: XCTest
description: Apple's unit and UI testing framework for Swift/Objective-C
category: unit_integration  # Can also do UI tests
languages: [swift, objective-c]
platforms: [ios, macos]
priority: 85
alternative_to: []
compatible_with: [xcuitest]

detection:
  explicit_markers:
    - pattern: "Test Framework: XCTest"
      source: [tasks.md, plan.md]
  project_files:
    - file: "*.xcodeproj"
      exists: true
  dependencies: []  # Built into Xcode

installation:
  xcode:
    command: "# Built into Xcode"
    manual_steps: |
      XCTest is built into Xcode.
      Create test target in Xcode project.

verification:
  - command: "xcodebuild -version"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
prerequisites:
  - macOS
  - Xcode
docs_url: https://developer.apple.com/documentation/xctest
```

---

## E2E Desktop Testing Frameworks

### tauri-test

```yaml
framework_id: tauri-test
name: Tauri Test
description: Testing framework for Tauri desktop applications
category: e2e_desktop
languages: [rust, javascript, typescript]
platforms: [tauri]
priority: 90
alternative_to: []
compatible_with: [cargo-test]

detection:
  explicit_markers:
    - pattern: "Test Framework: Tauri test"
      source: [tasks.md, plan.md]
  project_files:
    - file: src-tauri/Cargo.toml
      exists: true
  dependencies:
    - package: tauri-driver
      type: dev

installation:
  npm:
    command: "npm install -D @tauri-apps/cli"
  cargo:
    command: "cargo install tauri-driver"

verification:
  - command: "tauri-driver --version"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
prerequisites:
  - Rust toolchain
  - Tauri CLI
docs_url: https://tauri.app/v1/guides/testing/webdriver/introduction
```

### spectron

```yaml
framework_id: spectron
name: Spectron
description: Test Electron apps using ChromeDriver
category: e2e_desktop
languages: [javascript, typescript]
platforms: [electron]
priority: 80
alternative_to: [wdio-electron]
compatible_with: [mocha, jest]

detection:
  explicit_markers:
    - pattern: "Test Framework: Spectron"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"spectron"'
  dependencies:
    - package: spectron
      type: dev

installation:
  npm:
    command: "npm install -D spectron"

verification:
  - command: "node -e \"require('spectron')\""
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://www.electronjs.org/spectron
```

### wdio-electron

```yaml
framework_id: wdio-electron
name: WebdriverIO Electron
description: WebdriverIO service for Electron apps
category: e2e_desktop
languages: [javascript, typescript]
platforms: [electron]
priority: 85
alternative_to: [spectron]
compatible_with: [webdriverio]

detection:
  explicit_markers:
    - pattern: "Test Framework: WebdriverIO Electron"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"wdio-electron-service"'
  dependencies:
    - package: wdio-electron-service
      type: dev

installation:
  npm:
    command: "npm install -D wdio-electron-service @wdio/cli"

verification:
  - command: "npx wdio --version"
    expected_exit_code: 0

configuration:
  required_files:
    - wdio.conf.ts
  template: null

quality_gate: QG-TEST-002
docs_url: https://webdriver.io/docs/desktop-testing/electron
```

---

## API Testing Frameworks

### supertest

```yaml
framework_id: supertest
name: Supertest
description: Super-agent driven library for testing HTTP servers
category: api
languages: [javascript, typescript]
platforms: [node, express, fastify, nest]
priority: 90
alternative_to: []
compatible_with: [jest, mocha]

detection:
  explicit_markers:
    - pattern: "Test Framework: Supertest"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"supertest"'
  dependencies:
    - package: supertest
      type: dev

installation:
  npm:
    command: "npm install -D supertest @types/supertest"
  yarn:
    command: "yarn add -D supertest @types/supertest"
  pnpm:
    command: "pnpm add -D supertest @types/supertest"

verification:
  - command: "npm list supertest"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://github.com/ladjs/supertest
```

### rest-assured

```yaml
framework_id: rest-assured
name: REST Assured
description: Java DSL for easy testing of REST services
category: api
languages: [java, kotlin]
platforms: [jvm, spring]
priority: 90
alternative_to: []
compatible_with: [junit5, testng]

detection:
  explicit_markers:
    - pattern: "Test Framework: REST Assured"
      source: [tasks.md, plan.md]
  project_files:
    - file: build.gradle.kts
      contains: 'rest-assured'
    - file: pom.xml
      contains: 'rest-assured'
  dependencies:
    - package: rest-assured
      type: dev

installation:
  gradle:
    command: |
      dependencies {
          testImplementation("io.rest-assured:rest-assured:5.4.0")
      }
  maven:
    command: |
      <dependency>
          <groupId>io.rest-assured</groupId>
          <artifactId>rest-assured</artifactId>
          <version>5.4.0</version>
          <scope>test</scope>
      </dependency>

verification:
  - command: "./gradlew dependencies | grep rest-assured"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://rest-assured.io/
```

### postman-newman

```yaml
framework_id: postman-newman
name: Newman (Postman CLI)
description: Command-line collection runner for Postman
category: api
languages: [json]
platforms: [any]
priority: 80
alternative_to: []
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: Newman"
      source: [tasks.md, plan.md]
    - pattern: "Postman"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"newman"'
  dependencies:
    - package: newman
      type: dev

installation:
  npm:
    command: "npm install -D newman"

verification:
  - command: "npx newman --version"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/
```

### requests-mock

```yaml
framework_id: requests-mock
name: requests-mock
description: Mock library for Python requests
category: api
languages: [python]
platforms: [python, fastapi, django, flask]
priority: 85
alternative_to: []
compatible_with: [pytest, unittest]

detection:
  explicit_markers:
    - pattern: "Test Framework: requests-mock"
      source: [tasks.md, plan.md]
  project_files:
    - file: requirements.txt
      contains: 'requests-mock'
  dependencies:
    - package: requests-mock
      type: dev

installation:
  pip:
    command: "pip install requests-mock"
  poetry:
    command: "poetry add --group dev requests-mock"

verification:
  - command: "python -c \"import requests_mock\""
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://requests-mock.readthedocs.io/
```

### httptest

```yaml
framework_id: httptest
name: httptest
description: Built-in Go HTTP testing utilities
category: api
languages: [go]
platforms: [go]
priority: 95
alternative_to: []
compatible_with: [go-test]

detection:
  explicit_markers:
    - pattern: "Test Framework: httptest"
      source: [tasks.md, plan.md]
  project_files:
    - file: go.mod
      exists: true
  dependencies: []  # Built into Go stdlib

installation:
  go:
    command: "# Built into Go standard library"
    manual_steps: |
      httptest is part of Go's standard library.
      No installation needed.

verification:
  - command: "go doc net/http/httptest"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://pkg.go.dev/net/http/httptest
```

---

## Performance Testing Frameworks

### k6

```yaml
framework_id: k6
name: k6
description: Modern load testing tool built for developers
category: performance
languages: [javascript]
platforms: [any]
priority: 90
alternative_to: [artillery, jmeter]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: k6"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"k6"'
  dependencies:
    - package: k6
      type: dev

installation:
  npm:
    command: "npm install -D k6"
  brew:
    command: "brew install k6"
  curl:
    command: |
      # Linux
      curl -L https://github.com/grafana/k6/releases/download/v0.48.0/k6-v0.48.0-linux-amd64.tar.gz | tar xvz
      # macOS
      curl -L https://github.com/grafana/k6/releases/download/v0.48.0/k6-v0.48.0-macos-amd64.tar.gz | tar xvz

verification:
  - command: "k6 version"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://k6.io/docs/
```

### artillery

```yaml
framework_id: artillery
name: Artillery
description: Cloud-scale load testing for DevOps and SRE
category: performance
languages: [yaml, javascript]
platforms: [any]
priority: 85
alternative_to: [k6, jmeter]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: Artillery"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"artillery"'
  dependencies:
    - package: artillery
      type: dev

installation:
  npm:
    command: "npm install -D artillery"

verification:
  - command: "npx artillery --version"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://www.artillery.io/docs
```

### locust

```yaml
framework_id: locust
name: Locust
description: Scalable load testing tool written in Python
category: performance
languages: [python]
platforms: [any]
priority: 80
alternative_to: [k6, jmeter]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: Locust"
      source: [tasks.md, plan.md]
  project_files:
    - file: requirements.txt
      contains: 'locust'
  dependencies:
    - package: locust
      type: dev

installation:
  pip:
    command: "pip install locust"

verification:
  - command: "locust --version"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://docs.locust.io/
```

### jmeter

```yaml
framework_id: jmeter
name: Apache JMeter
description: Open source load testing tool
category: performance
languages: [java]
platforms: [any]
priority: 75
alternative_to: [k6, artillery]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: JMeter"
      source: [tasks.md, plan.md]
  project_files: []
  dependencies: []

installation:
  brew:
    command: "brew install jmeter"
  manual:
    manual_steps: |
      1. Download from https://jmeter.apache.org/download_jmeter.cgi
      2. Extract archive
      3. Add bin/ to PATH
      4. Run: jmeter --version

verification:
  - command: "jmeter --version"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://jmeter.apache.org/usermanual/index.html
```

---

## Visual Regression Testing Frameworks

### percy

```yaml
framework_id: percy
name: Percy
description: Visual testing and review platform
category: visual
languages: [javascript, typescript, python, ruby, java]
platforms: [web]
priority: 85
alternative_to: [chromatic, backstopjs]
compatible_with: [cypress, playwright, selenium]

detection:
  explicit_markers:
    - pattern: "Test Framework: Percy"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"@percy/"'
  dependencies:
    - package: "@percy/cli"
      type: dev

installation:
  npm:
    command: "npm install -D @percy/cli @percy/playwright"

verification:
  - command: "npx percy --version"
    expected_exit_code: 0

configuration:
  required_files:
    - .percy.yml
  template: null

quality_gate: QG-TEST-002
prerequisites:
  - Percy account and PERCY_TOKEN
docs_url: https://www.browserstack.com/docs/percy
```

### chromatic

```yaml
framework_id: chromatic
name: Chromatic
description: Visual testing for Storybook
category: visual
languages: [javascript, typescript]
platforms: [web]
priority: 90
alternative_to: [percy]
compatible_with: [storybook]

detection:
  explicit_markers:
    - pattern: "Test Framework: Chromatic"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"chromatic"'
    - file: .storybook
      exists: true
  dependencies:
    - package: chromatic
      type: dev

installation:
  npm:
    command: "npm install -D chromatic"

verification:
  - command: "npx chromatic --version"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
prerequisites:
  - Storybook installed
  - Chromatic account
docs_url: https://www.chromatic.com/docs/
```

### backstopjs

```yaml
framework_id: backstopjs
name: BackstopJS
description: Visual regression testing for web apps
category: visual
languages: [javascript]
platforms: [web]
priority: 80
alternative_to: [percy, chromatic]
compatible_with: []

detection:
  explicit_markers:
    - pattern: "Test Framework: BackstopJS"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"backstopjs"'
    - file: backstop.json
      exists: true
  dependencies:
    - package: backstopjs
      type: dev

installation:
  npm:
    command: "npm install -D backstopjs"

verification:
  - command: "npx backstop --version"
    expected_exit_code: 0

configuration:
  required_files:
    - backstop.json
  template: null

quality_gate: QG-TEST-002
docs_url: https://github.com/garris/BackstopJS
```

### playwright-visual

```yaml
framework_id: playwright-visual
name: Playwright Visual Comparisons
description: Built-in visual regression testing in Playwright
category: visual
languages: [javascript, typescript, python]
platforms: [web]
priority: 85
alternative_to: [percy, backstopjs]
compatible_with: [playwright]

detection:
  explicit_markers:
    - pattern: "Visual Testing: Playwright"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"@playwright/test"'
  dependencies:
    - package: "@playwright/test"
      type: dev

installation:
  npm:
    command: "npm install -D @playwright/test"

verification:
  - command: "npx playwright --version"
    expected_exit_code: 0

configuration:
  required_files:
    - playwright.config.ts
  template: null

quality_gate: QG-TEST-002
docs_url: https://playwright.dev/docs/test-snapshots
```

---

## Contract Testing Frameworks

### pact

```yaml
framework_id: pact
name: Pact
description: Consumer-driven contract testing framework
category: contract
languages: [javascript, typescript, python, java, ruby, go, csharp]
platforms: [any]
priority: 90
alternative_to: [spring-cloud-contract]
compatible_with: [jest, pytest, junit5]

detection:
  explicit_markers:
    - pattern: "Test Framework: Pact"
      source: [tasks.md, plan.md]
  project_files:
    - file: package.json
      contains: '"@pact-foundation/pact"'
  dependencies:
    - package: "@pact-foundation/pact"
      type: dev

installation:
  npm:
    command: "npm install -D @pact-foundation/pact"
  pip:
    command: "pip install pact-python"
  maven:
    command: |
      <dependency>
          <groupId>au.com.dius.pact.consumer</groupId>
          <artifactId>junit5</artifactId>
          <version>4.6.4</version>
      </dependency>

verification:
  - command: "node -e \"require('@pact-foundation/pact')\""
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://docs.pact.io/
```

### spring-cloud-contract

```yaml
framework_id: spring-cloud-contract
name: Spring Cloud Contract
description: Contract testing for JVM-based applications
category: contract
languages: [java, kotlin, groovy]
platforms: [spring]
priority: 85
alternative_to: [pact]
compatible_with: [junit5]

detection:
  explicit_markers:
    - pattern: "Test Framework: Spring Cloud Contract"
      source: [tasks.md, plan.md]
  project_files:
    - file: build.gradle.kts
      contains: 'spring-cloud-contract'
    - file: pom.xml
      contains: 'spring-cloud-contract'
  dependencies:
    - package: spring-cloud-contract
      type: dev

installation:
  gradle:
    command: |
      dependencies {
          testImplementation("org.springframework.cloud:spring-cloud-starter-contract-verifier")
      }
  maven:
    command: |
      <dependency>
          <groupId>org.springframework.cloud</groupId>
          <artifactId>spring-cloud-starter-contract-verifier</artifactId>
          <scope>test</scope>
      </dependency>

verification:
  - command: "./gradlew dependencies | grep spring-cloud-contract"
    expected_exit_code: 0

configuration:
  required_files: []
  template: null

quality_gate: QG-TEST-002
docs_url: https://spring.io/projects/spring-cloud-contract
```

---

## Usage Notes

### Priority System

When multiple frameworks match detection criteria, the framework with the **highest priority** is selected:

- **90-100**: Strongly recommended (best practices, modern, well-supported)
- **70-89**: Good choice (mature, widely used)
- **60-69**: Alternative option (older or specialized)

### Platform-Specific Constraints

Some frameworks have platform requirements:

| Framework | Constraint | Auto-Install |
|-----------|-----------|--------------|
| XCUITest | macOS + Xcode | ❌ Manual (App Store) |
| XCTest | macOS + Xcode | ❌ Manual (App Store) |
| Espresso | Android SDK + $ANDROID_HOME | ⚠️  Requires SDK setup |
| Tauri Test | Rust toolchain | ⚠️  Requires Rust |
| Flutter test | Flutter SDK | ⚠️  Requires Flutter |

### Built-in Frameworks

These frameworks require no installation:

- **go-test** (Go)
- **cargo-test** (Rust)
- **unittest** (Python)
- **httptest** (Go)
- **XCTest** (Xcode)
- **XCUITest** (Xcode)
- **flutter_test** (Flutter SDK)

### Multi-Language Support

Some frameworks support multiple languages:

- **Playwright**: JS/TS, Python, Java, C#
- **Selenium**: JS/TS, Python, Java, C#, Ruby
- **Pact**: JS/TS, Python, Java, Ruby, Go, C#
- **Appium**: JS/TS, Python, Java, Ruby

### Compatible Frameworks

Frameworks can coexist when they serve different purposes:

- **Jest + Playwright** (unit + E2E web)
- **pytest + Playwright** (unit + E2E web)
- **Jest + Maestro + XCUITest** (unit + E2E mobile multi-platform)
- **JUnit5 + Espresso + REST Assured** (unit + E2E mobile + API)

### Alternative Frameworks

When explicit markers specify alternatives, respect user preference:

- "Test Framework: Mocha" → Use Mocha (not Jest)
- "Test Framework: NUnit" → Use NUnit (not xUnit)
- "Test Framework: Appium" → Use Appium (not Maestro)

---

## Extending the Registry

To add a new framework:

1. **Choose category**: unit_integration, e2e_web, e2e_mobile, e2e_desktop, api, performance, visual, contract
2. **Assign priority**: 60-100 based on maturity and best practices
3. **Define detection rules**: explicit markers, project files, dependencies
4. **Provide installation commands**: for each package manager
5. **Add verification commands**: to confirm installation
6. **Document prerequisites**: if platform-specific

Example template:

```yaml
framework_id: new-framework
name: New Framework
description: Brief description
category: <category>
languages: [<languages>]
platforms: [<platforms>]
priority: <0-100>
alternative_to: [<alternatives>]
compatible_with: [<compatible>]

detection:
  explicit_markers:
    - pattern: "Test Framework: New Framework"
      source: [tasks.md, plan.md]
  project_files:
    - file: config-file
      exists: true
  dependencies:
    - package: package-name
      type: dev

installation:
  npm:
    command: "npm install -D package-name"

verification:
  - command: "npx package-name --version"
    expected_exit_code: 0

configuration:
  required_files:
    - config.file
  template: templates/shared/test-configs/config.file

quality_gate: QG-TEST-002
docs_url: https://example.com/docs
```

---

## Registry Statistics

| Category | Frameworks | Coverage |
|----------|-----------|----------|
| Unit/Integration | 11 | JS/TS, Python, Go, Rust, Java, Kotlin, Ruby, C#, F# |
| E2E Web | 5 | Multi-language |
| E2E Mobile | 7 | iOS, Android, React Native, Flutter |
| E2E Desktop | 3 | Tauri, Electron |
| API | 5 | Node, Python, Java, Go |
| Performance | 4 | Multi-platform |
| Visual | 4 | Web-focused |
| Contract | 2 | Multi-language |
| **Total** | **41 frameworks** | **12+ languages, 5 platforms** |

---

**Registry Version**: 1.0.0
**Last Updated**: 2026-01-10
**Maintained By**: Spec Kit Core Team
**License**: MIT

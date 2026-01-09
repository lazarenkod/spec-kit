# Maestro Flow Template (React Native / Flutter / Native)

## Purpose

Template for creating Maestro flows that:
- Test mobile apps with declarative YAML
- Support iOS and Android
- Map to acceptance scenarios (AS-xxx)
- Enable quick iteration without recompilation

## Directory Structure

```text
your_app/
  .maestro/
    config.yaml           # Global configuration
    flows/
      login.yaml          # Login flow
      onboarding.yaml     # Onboarding flow
      checkout.yaml       # Checkout flow
    utils/
      common.yaml         # Reusable sub-flows
    data/
      test-users.yaml     # Test data
```

## Global Configuration

```yaml
# .maestro/config.yaml
appId: com.example.{{app_name}}
name: {{app_name}} Test Suite

# Environment variables
env:
  API_URL: http://localhost:3000
  TEST_USER: test@example.com
```

## Main Flow File

```yaml
# .maestro/flows/feature.yaml
# @speckit:AS-001
# Feature: {{feature_name}}
# Scenario: {{scenario_description}}

appId: com.example.{{app_name}}
---

# AS-001: {{scenario_description}}
- launchApp:
    clearState: true

# Arrange - Navigate to feature
- tapOn:
    id: "feature_button"

# Act - Perform user action
- tapOn:
    id: "action_button"

- inputText:
    id: "input_field"
    text: "Test input"

- tapOn:
    id: "submit_button"

# Assert - MUST FAIL initially (TDD Red)
- assertVisible:
    id: "success_message"
    text: "Operation completed"
```

## Multi-Scenario Flow

```yaml
# .maestro/flows/login.yaml
# @speckit:AS-001, AS-002, AS-003

appId: com.example.{{app_name}}
---

# Setup: Clear app state
- launchApp:
    clearState: true

# -------------------------------------------
# AS-001: Successful login with valid credentials
# -------------------------------------------
- tapOn: "Login"

- inputText:
    id: "email_input"
    text: "user@example.com"

- inputText:
    id: "password_input"
    text: "ValidPassword123"

- tapOn:
    id: "login_button"

# Assert: Should see home screen (MUST FAIL initially)
- assertVisible:
    id: "home_screen"

# -------------------------------------------
# AS-002: Login fails with invalid password
# -------------------------------------------
- launchApp:
    clearState: true

- tapOn: "Login"

- inputText:
    id: "email_input"
    text: "user@example.com"

- inputText:
    id: "password_input"
    text: "WrongPassword"

- tapOn:
    id: "login_button"

# Assert: Should see error message
- assertVisible:
    text: "Invalid credentials"

# -------------------------------------------
# AS-003: Login fails with empty fields
# -------------------------------------------
- launchApp:
    clearState: true

- tapOn: "Login"

- tapOn:
    id: "login_button"

# Assert: Should see validation error
- assertVisible:
    text: "Email is required"
```

## Sub-Flows (Reusable Components)

```yaml
# .maestro/utils/login-helper.yaml
# Reusable login sub-flow

appId: com.example.{{app_name}}

- inputText:
    id: "email_input"
    text: "${EMAIL}"

- inputText:
    id: "password_input"
    text: "${PASSWORD}"

- tapOn:
    id: "login_button"
```

```yaml
# Using the sub-flow
- launchApp

- runFlow:
    file: utils/login-helper.yaml
    env:
      EMAIL: "test@example.com"
      PASSWORD: "password123"

- assertVisible:
    id: "home_screen"
```

## Test Data

```yaml
# .maestro/data/test-users.yaml
users:
  valid:
    email: test@example.com
    password: ValidPass123
  invalid:
    email: wrong@example.com
    password: wrongpass
  admin:
    email: admin@example.com
    password: AdminPass123
```

## Running Tests

```bash
# Run single flow
maestro test .maestro/flows/login.yaml

# Run all flows in directory
maestro test .maestro/

# Run with specific device
maestro test --device emulator-5554 .maestro/flows/login.yaml

# Run with environment variables
maestro test --env API_URL=http://localhost:3000 .maestro/

# Record test execution
maestro record .maestro/flows/login.yaml

# Run in cloud (Maestro Cloud)
maestro cloud .maestro/
```

## CI Configuration

```yaml
# .github/workflows/maestro-tests.yml
jobs:
  android-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup JDK
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Install Maestro
        run: |
          curl -Ls "https://get.maestro.mobile.dev" | bash
          echo "$HOME/.maestro/bin" >> $GITHUB_PATH

      - name: Start emulator
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          script: |
            maestro test .maestro/

  ios-tests:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Maestro
        run: |
          curl -Ls "https://get.maestro.mobile.dev" | bash
          echo "$HOME/.maestro/bin" >> $GITHUB_PATH

      - name: Boot iOS Simulator
        run: xcrun simctl boot "iPhone 15 Pro"

      - name: Run Maestro tests
        run: maestro test .maestro/
```

## Common Commands

```yaml
# Navigation
- launchApp
- launchApp:
    clearState: true
    clearKeychain: true

- stopApp
- killApp

# Tapping
- tapOn: "Button Text"
- tapOn:
    id: "button_id"
- tapOn:
    point: "50%,90%"

# Text Input
- inputText: "Hello World"
- inputText:
    id: "input_field"
    text: "Value"
- clearText:
    id: "input_field"

# Scrolling
- scroll
- scrollUntilVisible:
    element:
      id: "target_element"
    direction: DOWN

# Swiping
- swipe:
    direction: LEFT
    duration: 400

# Waiting
- waitForAnimationToEnd
- extendedWaitUntil:
    visible:
      id: "element"
    timeout: 10000

# Assertions
- assertVisible: "Text"
- assertVisible:
    id: "element_id"
- assertNotVisible: "Text"

# Conditional
- runFlow:
    when:
      visible: "Skip Button"
    commands:
      - tapOn: "Skip Button"

# Screenshots
- takeScreenshot: "screenshot_name"
```

## TDD Workflow

### Red Phase (Wave 2)
1. Write flow with assertions that WILL FAIL
2. Add `@speckit:AS-xxx` comment at top
3. Run: `maestro test .maestro/flows/feature.yaml`
4. Verify test fails

### Green Phase (Wave 3)
1. Implement feature in app
2. Rebuild app (if needed)
3. Run flow - should pass now

## Traceability

| AS-xxx | Flow | File |
|--------|------|------|
| AS-001 | Login success | .maestro/flows/login.yaml:10 |
| AS-002 | Login failure | .maestro/flows/login.yaml:35 |
| AS-003 | Validation | .maestro/flows/login.yaml:55 |

## Debugging Tips

```bash
# Interactive mode (step through)
maestro studio

# View hierarchy
maestro hierarchy

# Record and generate flow
maestro record
```

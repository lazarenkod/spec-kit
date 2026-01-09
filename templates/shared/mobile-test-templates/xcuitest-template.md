# XCUITest Template (Native iOS)

## Purpose

Template for creating XCUITest tests for native iOS apps that:
- Test UI interactions and flows
- Map to acceptance scenarios (AS-xxx)
- Support TDD Red/Green phases
- Integrate with Xcode test plans

## Directory Structure

```text
YourApp/
  YourApp/                    # Main app target
  YourAppTests/               # Unit tests
  YourAppUITests/             # UI tests (XCUITest)
    YourAppUITests.swift      # Main UI test file
    Screens/                  # Screen/Page objects
      LoginScreen.swift
      HomeScreen.swift
    Helpers/
      TestHelpers.swift       # Common utilities
      XCTestCase+Extensions.swift
    TestPlans/
      UITests.xctestplan      # Test plan configuration
```

## Main Test File

```swift
// YourAppUITests/FeatureUITests.swift

import XCTest

final class FeatureUITests: XCTestCase {

    var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["--uitesting"]
        app.launch()
    }

    override func tearDownWithError() throws {
        app = nil
    }

    // MARK: - AS-001: {{scenario_description}}
    // @speckit:AS-001
    func testAS001_{{scenario_name}}() throws {
        // Arrange
        let loginButton = app.buttons["loginButton"]

        // Act
        loginButton.tap()

        // Assert - MUST FAIL initially (TDD Red)
        let homeScreen = app.otherElements["homeScreen"]
        XCTAssertTrue(homeScreen.waitForExistence(timeout: 5))
    }

    // MARK: - AS-002: {{scenario_description}}
    // @speckit:AS-002
    func testAS002_{{scenario_name}}() throws {
        // TODO: Implement test - must FAIL initially
        let expectedElement = app.staticTexts["Expected Text"]
        XCTAssertTrue(expectedElement.exists)
    }
}
```

## Screen Objects (Page Object Pattern)

```swift
// YourAppUITests/Screens/LoginScreen.swift

import XCTest

struct LoginScreen {
    let app: XCUIApplication

    // MARK: - Elements

    var emailTextField: XCUIElement {
        app.textFields["emailTextField"]
    }

    var passwordTextField: XCUIElement {
        app.secureTextFields["passwordTextField"]
    }

    var loginButton: XCUIElement {
        app.buttons["loginButton"]
    }

    var errorLabel: XCUIElement {
        app.staticTexts["errorLabel"]
    }

    // MARK: - Actions

    func enterEmail(_ email: String) {
        emailTextField.tap()
        emailTextField.typeText(email)
    }

    func enterPassword(_ password: String) {
        passwordTextField.tap()
        passwordTextField.typeText(password)
    }

    func tapLogin() {
        loginButton.tap()
    }

    func login(email: String, password: String) {
        enterEmail(email)
        enterPassword(password)
        tapLogin()
    }

    // MARK: - Assertions

    func verifyErrorMessage(_ message: String) {
        XCTAssertTrue(errorLabel.waitForExistence(timeout: 3))
        XCTAssertEqual(errorLabel.label, message)
    }

    func verifyLoginButtonEnabled() {
        XCTAssertTrue(loginButton.isEnabled)
    }
}
```

```swift
// YourAppUITests/Screens/HomeScreen.swift

import XCTest

struct HomeScreen {
    let app: XCUIApplication

    var welcomeLabel: XCUIElement {
        app.staticTexts["welcomeLabel"]
    }

    var profileButton: XCUIElement {
        app.buttons["profileButton"]
    }

    var isDisplayed: Bool {
        app.otherElements["homeScreen"].exists
    }

    func verifyWelcomeMessage(_ name: String) {
        XCTAssertTrue(welcomeLabel.waitForExistence(timeout: 5))
        XCTAssertTrue(welcomeLabel.label.contains(name))
    }
}
```

## Test Helpers

```swift
// YourAppUITests/Helpers/XCTestCase+Extensions.swift

import XCTest

extension XCTestCase {

    /// Wait for element to exist with custom timeout
    func waitForElement(
        _ element: XCUIElement,
        timeout: TimeInterval = 5,
        file: StaticString = #file,
        line: UInt = #line
    ) {
        let exists = element.waitForExistence(timeout: timeout)
        XCTAssertTrue(exists, "Element \(element) did not appear within \(timeout)s", file: file, line: line)
    }

    /// Wait for element to disappear
    func waitForElementToDisappear(
        _ element: XCUIElement,
        timeout: TimeInterval = 5
    ) {
        let predicate = NSPredicate(format: "exists == false")
        let expectation = XCTNSPredicateExpectation(predicate: predicate, object: element)
        let result = XCTWaiter.wait(for: [expectation], timeout: timeout)
        XCTAssertEqual(result, .completed)
    }

    /// Dismiss keyboard
    func dismissKeyboard() {
        let app = XCUIApplication()
        if app.keyboards.count > 0 {
            app.typeText("\n")
        }
    }
}
```

## Test Plan Configuration

```json
// YourAppUITests/TestPlans/UITests.xctestplan
{
  "configurations" : [
    {
      "name" : "Default",
      "options" : {
        "targetForVariableExpansion" : {
          "containerPath" : "container:YourApp.xcodeproj",
          "identifier" : "YourAppUITests"
        }
      }
    }
  ],
  "defaultOptions" : {
    "codeCoverage" : true,
    "targetForVariableExpansion" : {
      "containerPath" : "container:YourApp.xcodeproj",
      "identifier" : "YourAppUITests"
    }
  },
  "testTargets" : [
    {
      "target" : {
        "containerPath" : "container:YourApp.xcodeproj",
        "identifier" : "YourAppUITests"
      }
    }
  ],
  "version" : 1
}
```

## Running Tests

```bash
# Run all UI tests
xcodebuild test \
  -project YourApp.xcodeproj \
  -scheme YourApp \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro'

# Run specific test class
xcodebuild test \
  -project YourApp.xcodeproj \
  -scheme YourApp \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
  -only-testing:YourAppUITests/FeatureUITests

# Run with test plan
xcodebuild test \
  -project YourApp.xcodeproj \
  -scheme YourApp \
  -testPlan UITests \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro'

# Run with coverage
xcodebuild test \
  -project YourApp.xcodeproj \
  -scheme YourApp \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
  -enableCodeCoverage YES
```

## CI Configuration

```yaml
# .github/workflows/ios-tests.yml
jobs:
  ios-ui-tests:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -switch /Applications/Xcode_15.2.app

      - name: Build and Test
        run: |
          xcodebuild test \
            -project YourApp.xcodeproj \
            -scheme YourApp \
            -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
            -enableCodeCoverage YES \
            -resultBundlePath TestResults.xcresult

      - name: Upload Test Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: TestResults.xcresult
```

## Common Assertions

```swift
// Element exists
XCTAssertTrue(element.exists)
XCTAssertTrue(element.waitForExistence(timeout: 5))

// Element text
XCTAssertEqual(element.label, "Expected")
XCTAssertTrue(element.label.contains("partial"))

// Element state
XCTAssertTrue(element.isEnabled)
XCTAssertTrue(element.isSelected)
XCTAssertTrue(element.isHittable)

// Element count
XCTAssertEqual(app.cells.count, 5)

// No element
XCTAssertFalse(element.exists)
```

## Common Actions

```swift
// Tap
element.tap()
element.doubleTap()
element.press(forDuration: 1.0)

// Text input
textField.tap()
textField.typeText("Hello")
textField.clearText()

// Clear text field
textField.tap()
textField.buttons["Clear text"].tap()

// Swipe
element.swipeUp()
element.swipeDown()
element.swipeLeft()
element.swipeRight()

// Scroll
scrollView.scroll(byDeltaX: 0, deltaY: -100)

// Pinch
element.pinch(withScale: 0.5, velocity: -1.0)

// Rotate
element.rotate(CGFloat.pi, withVelocity: 1.0)
```

## TDD Workflow

### Red Phase (Wave 2)
1. Create test file with assertions that WILL FAIL
2. Add `@speckit:AS-xxx` comment
3. Run: `xcodebuild test ...`
4. Verify test fails

### Green Phase (Wave 3)
1. Implement feature in SwiftUI/UIKit
2. Add accessibility identifiers
3. Run test - should pass now

## Accessibility Identifiers

```swift
// In your SwiftUI view
Button("Login") {
    // action
}
.accessibilityIdentifier("loginButton")

// In your UIKit view
loginButton.accessibilityIdentifier = "loginButton"
```

## Traceability

| AS-xxx | Test Method | File |
|--------|-------------|------|
| AS-001 | testAS001_{{scenario}} | FeatureUITests.swift:25 |
| AS-002 | testAS002_{{scenario}} | FeatureUITests.swift:38 |

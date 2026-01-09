# Espresso Test Template (Native Android)

## Purpose

Template for creating Espresso tests for native Android apps that:
- Test UI interactions on Android
- Map to acceptance scenarios (AS-xxx)
- Support TDD Red/Green phases
- Work with Android instrumented tests

## Directory Structure

```text
app/
  src/
    main/                           # Main app code
    androidTest/                    # Instrumented tests (Espresso)
      java/com/example/app/
        FeatureTest.kt              # Feature tests
        screens/                    # Screen objects
          LoginScreen.kt
          HomeScreen.kt
        utils/
          TestHelpers.kt            # Common utilities
          CustomMatchers.kt         # Custom Espresso matchers
        rules/
          RetryRule.kt              # Test retry rule
    test/                           # Unit tests
```

## Main Test File

```kotlin
// app/src/androidTest/java/com/example/app/FeatureTest.kt

package com.example.app

import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class FeatureTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    // @speckit:AS-001
    // AS-001: {{scenario_description}}
    @Test
    fun testAS001_{{scenario_name}}() {
        // Arrange - Activity launched by rule

        // Act
        onView(withId(R.id.loginButton))
            .perform(click())

        onView(withId(R.id.emailInput))
            .perform(typeText("test@example.com"), closeSoftKeyboard())

        onView(withId(R.id.passwordInput))
            .perform(typeText("password123"), closeSoftKeyboard())

        onView(withId(R.id.submitButton))
            .perform(click())

        // Assert - MUST FAIL initially (TDD Red)
        onView(withId(R.id.homeScreen))
            .check(matches(isDisplayed()))
    }

    // @speckit:AS-002
    // AS-002: {{scenario_description}}
    @Test
    fun testAS002_{{scenario_name}}() {
        // TODO: Implement test - must FAIL initially
        onView(withText("Expected Text"))
            .check(matches(isDisplayed()))
    }
}
```

## Screen Objects (Page Object Pattern)

```kotlin
// app/src/androidTest/java/com/example/app/screens/LoginScreen.kt

package com.example.app.screens

import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*
import com.example.app.R

class LoginScreen {

    // Elements
    private val emailInput = onView(withId(R.id.emailInput))
    private val passwordInput = onView(withId(R.id.passwordInput))
    private val loginButton = onView(withId(R.id.loginButton))
    private val errorMessage = onView(withId(R.id.errorMessage))

    // Actions
    fun enterEmail(email: String): LoginScreen {
        emailInput.perform(typeText(email), closeSoftKeyboard())
        return this
    }

    fun enterPassword(password: String): LoginScreen {
        passwordInput.perform(typeText(password), closeSoftKeyboard())
        return this
    }

    fun clickLogin(): LoginScreen {
        loginButton.perform(click())
        return this
    }

    fun login(email: String, password: String): LoginScreen {
        return enterEmail(email)
            .enterPassword(password)
            .clickLogin()
    }

    // Assertions
    fun verifyErrorMessage(message: String): LoginScreen {
        errorMessage.check(matches(isDisplayed()))
        errorMessage.check(matches(withText(message)))
        return this
    }

    fun verifyLoginButtonEnabled(): LoginScreen {
        loginButton.check(matches(isEnabled()))
        return this
    }

    fun verifyLoginButtonDisabled(): LoginScreen {
        loginButton.check(matches(isNotEnabled()))
        return this
    }
}
```

```kotlin
// app/src/androidTest/java/com/example/app/screens/HomeScreen.kt

package com.example.app.screens

import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*
import com.example.app.R
import org.hamcrest.Matchers.containsString

class HomeScreen {

    private val welcomeLabel = onView(withId(R.id.welcomeLabel))
    private val profileButton = onView(withId(R.id.profileButton))
    private val homeContainer = onView(withId(R.id.homeScreen))

    fun verifyIsDisplayed(): HomeScreen {
        homeContainer.check(matches(isDisplayed()))
        return this
    }

    fun verifyWelcomeMessage(name: String): HomeScreen {
        welcomeLabel.check(matches(isDisplayed()))
        welcomeLabel.check(matches(withText(containsString(name))))
        return this
    }
}
```

## Test Helpers

```kotlin
// app/src/androidTest/java/com/example/app/utils/TestHelpers.kt

package com.example.app.utils

import android.view.View
import androidx.test.espresso.UiController
import androidx.test.espresso.ViewAction
import androidx.test.espresso.matcher.ViewMatchers.isRoot
import org.hamcrest.Matcher

object TestHelpers {

    /**
     * Wait for specified duration
     */
    fun waitFor(millis: Long): ViewAction {
        return object : ViewAction {
            override fun getConstraints(): Matcher<View> = isRoot()

            override fun getDescription(): String = "Wait for $millis milliseconds"

            override fun perform(uiController: UiController, view: View?) {
                uiController.loopMainThreadForAtLeast(millis)
            }
        }
    }

    /**
     * Wait until view is displayed
     */
    fun waitForView(viewMatcher: Matcher<View>, timeout: Long = 5000): ViewAction {
        return object : ViewAction {
            override fun getConstraints(): Matcher<View> = isRoot()

            override fun getDescription(): String = "Wait for view with timeout"

            override fun perform(uiController: UiController, view: View?) {
                val endTime = System.currentTimeMillis() + timeout
                while (System.currentTimeMillis() < endTime) {
                    try {
                        val viewInteraction = androidx.test.espresso.Espresso.onView(viewMatcher)
                        viewInteraction.check(
                            androidx.test.espresso.assertion.ViewAssertions.matches(
                                androidx.test.espresso.matcher.ViewMatchers.isDisplayed()
                            )
                        )
                        return
                    } catch (e: Exception) {
                        uiController.loopMainThreadForAtLeast(50)
                    }
                }
                throw androidx.test.espresso.PerformException.Builder()
                    .withCause(TimeoutException("View not found within $timeout ms"))
                    .build()
            }
        }
    }
}

class TimeoutException(message: String) : Exception(message)
```

## Custom Matchers

```kotlin
// app/src/androidTest/java/com/example/app/utils/CustomMatchers.kt

package com.example.app.utils

import android.view.View
import android.widget.EditText
import androidx.test.espresso.matcher.BoundedMatcher
import org.hamcrest.Description
import org.hamcrest.Matcher

object CustomMatchers {

    /**
     * Match EditText with error
     */
    fun hasError(expectedError: String): Matcher<View> {
        return object : BoundedMatcher<View, EditText>(EditText::class.java) {
            override fun describeTo(description: Description) {
                description.appendText("has error: $expectedError")
            }

            override fun matchesSafely(item: EditText): Boolean {
                return item.error?.toString() == expectedError
            }
        }
    }

    /**
     * Match view with hint
     */
    fun withHint(expectedHint: String): Matcher<View> {
        return object : BoundedMatcher<View, EditText>(EditText::class.java) {
            override fun describeTo(description: Description) {
                description.appendText("has hint: $expectedHint")
            }

            override fun matchesSafely(item: EditText): Boolean {
                return item.hint?.toString() == expectedHint
            }
        }
    }
}
```

## Gradle Configuration

```kotlin
// app/build.gradle.kts

android {
    defaultConfig {
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    testOptions {
        animationsDisabled = true
    }
}

dependencies {
    // Espresso
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation("androidx.test.espresso:espresso-contrib:3.5.1")
    androidTestImplementation("androidx.test.espresso:espresso-intents:3.5.1")

    // AndroidX Test
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test:runner:1.5.2")
    androidTestImplementation("androidx.test:rules:1.5.0")
}
```

## Running Tests

```bash
# Run all instrumented tests
./gradlew connectedAndroidTest

# Run specific test class
./gradlew connectedAndroidTest \
  -Pandroid.testInstrumentationRunnerArguments.class=com.example.app.FeatureTest

# Run specific test method
./gradlew connectedAndroidTest \
  -Pandroid.testInstrumentationRunnerArguments.class=com.example.app.FeatureTest#testAS001_scenario

# Run with coverage
./gradlew createDebugCoverageReport

# Run on specific device
./gradlew connectedAndroidTest \
  -Pandroid.testInstrumentationRunnerArguments.device=emulator-5554
```

## CI Configuration

```yaml
# .github/workflows/android-tests.yml
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

      - name: Setup Gradle
        uses: gradle/gradle-build-action@v3

      - name: Run tests on emulator
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          target: google_apis
          arch: x86_64
          script: ./gradlew connectedAndroidTest

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: app/build/reports/androidTests/
```

## Common Matchers

```kotlin
// By ID
withId(R.id.button)

// By text
withText("Hello")
withText(containsString("partial"))

// By content description
withContentDescription("Button description")

// State matchers
isDisplayed()
isEnabled()
isNotEnabled()
isClickable()
isChecked()
isNotChecked()
isFocused()

// Hierarchy
isDescendantOfA(withId(R.id.container))
hasSibling(withText("Sibling"))
withParent(withId(R.id.parent))
```

## Common Actions

```kotlin
// Click
click()
doubleClick()
longClick()

// Text input
typeText("Hello")
typeTextIntoFocusedView("Hello")
replaceText("New text")
clearText()
closeSoftKeyboard()

// Scroll
scrollTo()

// Swipe
swipeUp()
swipeDown()
swipeLeft()
swipeRight()

// Press
pressBack()
pressKey(KeyEvent.KEYCODE_ENTER)
```

## TDD Workflow

### Red Phase (Wave 2)
1. Create test with assertions that WILL FAIL
2. Add `@speckit:AS-xxx` comment
3. Run: `./gradlew connectedAndroidTest`
4. Verify test fails

### Green Phase (Wave 3)
1. Implement feature in Kotlin/XML
2. Add view IDs for test access
3. Run test - should pass now

## Traceability

| AS-xxx | Test Method | File |
|--------|-------------|------|
| AS-001 | testAS001_{{scenario}} | FeatureTest.kt:25 |
| AS-002 | testAS002_{{scenario}} | FeatureTest.kt:45 |

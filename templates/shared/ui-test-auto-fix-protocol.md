# UI Test Auto-Fix Protocol

> **Version**: 1.0.0
> **Status**: Active
> **Applies to**: `/speckit.implement` Wave 2 (TDD Red) and Wave 4 (Test Verification)

## Overview

The UI Test Auto-Fix Protocol provides self-healing capabilities for E2E UI tests across **Web (Playwright)**, **Mobile (XCUITest, Espresso, Maestro)**, and **Desktop (Electron, Tauri)** platforms.

Unlike the PBT JIT Protocol (which handles property-based test failures), this protocol targets **UI-specific failure patterns** such as:
- Stale element references
- Selector timeouts
- Element not found errors
- Click interception

**Two Modes:**
- **Basic Mode (Default)**: 2 attempts - Retry + fallback selectors - No AI, no external dependencies
- **Advanced Mode (Optional)**: 3 attempts - Basic + AI selector suggestion - Requires `GEMINI_API_KEY`

---

## Execution Flow

### Basic Mode (Default)

```
attempt = 0
max_attempts = 2

WHILE test_fails AND attempt < max_attempts:
    1. Run UI test
    2. IF test passes:
         break (success)
    3. Capture failure details (stderr, screenshot if available)
    4. Classify failure pattern
    5. Apply healing strategy based on pattern
    6. Increment attempt

IF attempt >= max_attempts AND still_failing:
    block_task_completion()
    report_to_user()
```

### Advanced Mode (Optional)

```
attempt = 0
max_attempts = 3

WHILE test_fails AND attempt < max_attempts:
    1. Run UI test
    2. IF test passes:
         break (success)
    3. Capture failure details + DOM snapshot
    4. Classify failure pattern
    5. Apply healing strategy:
         IF attempt < 3:
             Apply basic healing (retry, fallback selectors)
         ELSE (attempt == 3):
             Apply AI healing (LLM selector suggestion)
    6. Increment attempt

IF attempt >= max_attempts AND still_failing:
    block_task_completion()
    report_to_user()
```

---

## Failure Pattern Classification

### Pattern Enum

```python
class UIFailurePattern(Enum):
    STALE_ELEMENT = "stale_element"
    TIMEOUT = "timeout"
    ELEMENT_NOT_FOUND = "element_not_found"
    CLICK_INTERCEPTED = "click_intercepted"
    TEXT_MISMATCH = "text_mismatch"
    NETWORK_ERROR = "network_error"
    UNKNOWN = "unknown"
```

### Detection Heuristics

```yaml
STALE_ELEMENT:
  playwright: "Element is not attached"
  xcuitest: "Stale element reference"
  espresso: "StaleDataException"
  maestro: "Element no longer exists"

TIMEOUT:
  playwright: "Timeout .* exceeded"
  xcuitest: "Waiting for .* to exist"
  espresso: "IdlingResourceTimeoutException"
  maestro: "Timeout after"

ELEMENT_NOT_FOUND:
  playwright: "locator.* not found"
  xcuitest: "No matches found for"
  espresso: "NoMatchingViewException"
  maestro: "Element .* not found"

CLICK_INTERCEPTED:
  playwright: "Element is not clickable at point"
  xcuitest: "not hittable"
  espresso: "ViewNotCompletelyDisplayedException"
  maestro: "Tap failed"

TEXT_MISMATCH:
  playwright: "Expected .* but got"
  xcuitest: "Unexpected .* value"
  espresso: "withText .* view assertion"
  maestro: "assertVisible .* failed"

NETWORK_ERROR:
  playwright: "net::ERR_"
  xcuitest: "NSURLError"
  espresso: "IOException"
  maestro: "Network request failed"
```

---

## Healing Strategies

### Basic Mode (2 Attempts)

#### Attempt 1: Explicit Waits

**For STALE_ELEMENT:**
```typescript
// Before (failing)
await page.click('button[data-testid="submit"]');

// After (healed)
await page.waitForSelector('button[data-testid="submit"]', { state: 'attached' });
await page.click('button[data-testid="submit"]');
```

**For TIMEOUT:**
```typescript
// Before (failing)
await page.click('button[data-testid="submit"]', { timeout: 5000 });

// After (healed)
await page.click('button[data-testid="submit"]', { timeout: 15000 });
await page.waitForLoadState('networkidle');
```

**For ELEMENT_NOT_FOUND:**
```typescript
// Before (failing)
await page.click('button[data-testid="submit"]');

// After (healed)
await page.waitForSelector('button[data-testid="submit"]', { timeout: 10000 });
await page.click('button[data-testid="submit"]');
```

**For CLICK_INTERCEPTED:**
```typescript
// Before (failing)
await page.click('button[data-testid="submit"]');

// After (healed)
await page.locator('button[data-testid="submit"]').scrollIntoViewIfNeeded();
await page.waitForTimeout(500);  // Wait for scroll animation
await page.click('button[data-testid="submit"]');
```

---

#### Attempt 2: Fallback Selectors

**Selector Hierarchy:**
```
1. data-testid="..." (most stable)
2. aria-label="..." (semantic, accessible)
3. role + accessible name (e.g., role=button[name="Submit"])
4. text content (fragile, last resort)
```

**Example:**
```typescript
// Before (failing with testId)
await page.click('button[data-testid="submit-button"]');

// Attempt 1: Add wait (failed)
await page.waitForSelector('button[data-testid="submit-button"]');
await page.click('button[data-testid="submit-button"]');

// Attempt 2: Fallback to aria-label
await page.click('button[aria-label="Submit"]');

// If aria-label fails, fallback to role + name
await page.click('button:has-text("Submit")');
```

---

### Advanced Mode (3rd Attempt): AI Selector Healing

**Trigger:** Only if `--ui-autofix-mode=advanced` and `GEMINI_API_KEY` set

**Prerequisites:**
- `google-generativeai` Python package installed
- Environment variable: `GEMINI_API_KEY=<your-key>`

**Process:**

1. **Capture Context:**
   ```python
   context = {
       "failed_selector": 'button[data-testid="submit-button"]',
       "semantic_intent": "Click submit button",
       "dom_snapshot": page.content()[:2000],  # First 2000 chars
       "failure_pattern": "ELEMENT_NOT_FOUND",
       "previous_attempts": [
           "button[data-testid='submit-button']",
           "button[aria-label='Submit']"
       ]
   }
   ```

2. **LLM Prompt:**
   ```python
   prompt = f"""You are a UI test automation expert. Suggest a robust Playwright selector.

   Failed Selector: {failed_selector}
   Semantic Intent: {intent}
   Previous Attempts: {previous_attempts}
   DOM Snapshot:
   {dom_snapshot}

   Rules:
   - Prefer data-testid or aria-label
   - Avoid text content if possible
   - Return ONLY the selector string (no explanation)

   Example Output: button:has-text("Submit")
   """
   ```

3. **API Call:**
   ```python
   import google.generativeai as genai

   genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
   model = genai.GenerativeModel("gemini-2.0-flash-exp")

   response = model.generate_content(
       prompt,
       generation_config={
           "temperature": 0.0,
           "max_output_tokens": 100,
       }
   )

   suggested_selector = response.text.strip()
   ```

4. **Apply Suggestion:**
   ```typescript
   // Attempt 3: AI-suggested selector
   await page.click(suggested_selector);
   ```

5. **Graceful Fallback:**
   - If API call fails (network error, rate limit), report as 2-attempt failure
   - If suggested selector fails, report as 3-attempt failure
   - Cache suggestions: `(failed_selector, intent) → suggested_selector`

---

## Test Framework Adaptations

### Playwright (Web/Electron)

```typescript
// config in playwright.config.ts
export default defineConfig({
  use: {
    // Auto-wait strategies
    actionTimeout: 10_000,
    navigationTimeout: 30_000,
  },
  retries: 0,  // Disable built-in retry (handled by auto-fix loop)
});
```

### XCUITest (iOS)

```swift
// Add to test helpers
extension XCUIElement {
    func tapWithRetry(maxAttempts: Int = 2) {
        for attempt in 1...maxAttempts {
            if self.waitForExistence(timeout: 5) && self.isHittable {
                self.tap()
                return
            }
            // Fallback: scroll into view
            if attempt < maxAttempts {
                self.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5)).tap()
            }
        }
    }
}
```

### Espresso (Android)

```kotlin
// Custom matcher with retry
fun clickWithRetry(viewMatcher: Matcher<View>, maxAttempts: Int = 2) {
    for (attempt in 1..maxAttempts) {
        try {
            onView(viewMatcher)
                .check(matches(isDisplayed()))
                .perform(click())
            return
        } catch (e: NoMatchingViewException) {
            if (attempt < maxAttempts) {
                // Fallback: scroll to view
                onView(viewMatcher).perform(scrollTo())
            } else {
                throw e
            }
        }
    }
}
```

### Maestro (Cross-Platform Mobile)

```yaml
# .maestro/utils/retry-tap.yaml
- tapOn:
    id: "submit-button"
    retries: 2
    timeout: 10000
- onFlowFailed:
    # Fallback: tap by text
    - tapOn: "Submit"
```

---

## Configuration

### Wave Scheduler Config

```python
@dataclass
class UIAutoFixConfig:
    enabled: bool = False
    mode: str = "basic"  # "basic" or "advanced"
    timeout_ms: int = 60_000  # 1 minute per UI test
    ai_model: str = "gemini-2.0-flash-exp"
    fallback_to_normal_flow: bool = True

    @property
    def max_attempts(self) -> int:
        """2 for basic, 3 for advanced."""
        return 2 if self.mode == "basic" else 3

    @property
    def ai_enabled(self) -> bool:
        """AI only in advanced mode."""
        return self.mode == "advanced"
```

### Command Line Flags

```bash
# Basic mode (default)
/speckit.implement

# Advanced mode (with AI)
/speckit.implement --ui-autofix-mode=advanced
# Requires: export GEMINI_API_KEY=<your-key>
```

---

## Integration with TDD Workflow

### Wave 2: TDD Red Phase

**Goal:** Verify tests FAIL initially (QG-TEST-003)

```python
async def _verify_ui_test_tdd_red(
    test_file: str
) -> TestVerificationResult:
    """
    Run UI test and verify it FAILS (TDD Red).
    No auto-fix applied at this stage.
    """
    result = await run_test(test_file, timeout_ms=60_000)

    if result.success:
        raise QgTest003ViolationError(
            f"UI test passed when it should fail: {test_file}"
        )

    return result
```

### Wave 4: Test Verification

**Goal:** Verify tests PASS (QG-UI-002) with auto-fix

```python
async def _verify_ui_test_and_heal(
    test_file: str,
    mode: str = "basic"
) -> TestVerificationResult:
    """
    Run UI test with auto-fix loop.
    """
    runner = UIAutoFixRunner(mode=mode)
    result = await runner.execute_with_autofix(test_file)

    if not result.success:
        raise QgUi002ViolationError(
            f"UI test failed after {runner.max_attempts} auto-fix attempts"
        )

    return result
```

---

## Block Conditions

**BLOCK immediately if:**
- Max attempts exceeded (2 for basic, 3 for advanced)
- All healing strategies exhausted
- Test failure is NOT a selector issue (e.g., assertion failure, business logic error)
- Advanced mode enabled but `GEMINI_API_KEY` not set (graceful fallback to basic mode)

**WARN but continue if:**
- AI API call fails (network error, rate limit) - fall back to basic mode result
- Screenshot capture fails (non-critical)
- DOM snapshot too large (truncate to 2000 chars)

---

## Logging and Diagnostics

### Success Log

```json
{
  "test_file": "tests/e2e/login.spec.ts",
  "result": "success",
  "attempts": 2,
  "healing_applied": [
    {
      "attempt": 1,
      "pattern": "ELEMENT_NOT_FOUND",
      "strategy": "explicit_wait",
      "duration_ms": 450
    },
    {
      "attempt": 2,
      "pattern": "ELEMENT_NOT_FOUND",
      "strategy": "fallback_selector",
      "healed_selector": "button[aria-label='Submit']",
      "duration_ms": 380
    }
  ],
  "total_duration_ms": 830
}
```

### Failure Log

```json
{
  "test_file": "tests/e2e/login.spec.ts",
  "result": "failure",
  "attempts": 2,
  "healing_applied": [
    {
      "attempt": 1,
      "pattern": "ELEMENT_NOT_FOUND",
      "strategy": "explicit_wait",
      "outcome": "failed"
    },
    {
      "attempt": 2,
      "pattern": "ELEMENT_NOT_FOUND",
      "strategy": "fallback_selector",
      "outcome": "failed"
    }
  ],
  "final_error": "Unable to locate element after 2 attempts",
  "diagnostics": {
    "failed_selectors": [
      "button[data-testid='submit-button']",
      "button[aria-label='Submit']"
    ],
    "dom_snapshot": "<!DOCTYPE html><html>..."
  }
}
```

---

## Best Practices

### 1. testId-First Approach

**Always use `data-testid` as primary selector:**

```typescript
// ✅ Good
await page.click('button[data-testid="submit-button"]');

// ❌ Bad
await page.click('button:has-text("Submit")');
```

**Rationale:** testIds are:
- Framework-agnostic
- Resilient to text changes (i18n, UX copy updates)
- Not affected by CSS changes

### 2. Avoid Hardcoded Waits

**Use explicit waits instead:**

```typescript
// ❌ Bad
await page.waitForTimeout(2000);
await page.click('button');

// ✅ Good
await page.waitForSelector('button[data-testid="submit"]', { state: 'visible' });
await page.click('button[data-testid="submit"]');
```

**Enforced by QG-UI-003.**

### 3. Semantic Selectors

**Use ARIA attributes for fallback:**

```typescript
// Priority order
const selectors = [
  'button[data-testid="submit"]',          // 1st: testId
  'button[aria-label="Submit form"]',      // 2nd: aria-label
  'button:has-text("Submit")',             // 3rd: text (last resort)
];
```

### 4. Idempotent Tests

**Ensure tests can run multiple times:**

```typescript
test('login flow', async ({ page }) => {
  // Reset state before each attempt
  await page.goto('/login');
  await page.evaluate(() => localStorage.clear());

  // Test logic
});
```

---

## Comparison with PBT JIT Protocol

| Feature | PBT JIT Protocol | UI Auto-Fix Protocol |
|---------|------------------|----------------------|
| **Target** | Property-based tests | E2E UI tests |
| **Failure Types** | Implementation bugs, property over-constraints | Selector issues, timing problems |
| **Max Attempts** | 3 (always) | 2 (basic) or 3 (advanced) |
| **AI Usage** | Always enabled | Optional (advanced mode only) |
| **Healing Strategies** | Code fixes (off-by-one, null checks) | Selector fixes (retry, fallback, AI) |
| **Block Condition** | Test fails after 3 attempts | Test fails after 2-3 attempts |
| **Phase** | Wave 3.5 (PBT JIT Validation) | Wave 2 (TDD Red) + Wave 4 (Verification) |

---

## Cost Estimation (Advanced Mode)

**AI API Costs** (Gemini 2.0 Flash):
- Input: ~500 tokens (prompt + DOM snapshot)
- Output: ~20 tokens (selector string)
- Cost: FREE up to 1500 RPM (Gemini 2.0 Flash free tier)
- **Budget:** $0 for most use cases (free tier covers typical CI/CD usage)

**Mitigation:**
- Cache suggestions: `(selector, intent) → suggested_selector`
- Circuit breaker: max 10 AI calls per test run
- Only on 3rd attempt (last resort)

---

## Future Enhancements

1. **Visual Regression Integration** (v2.0)
   - Auto-update baseline screenshots on intentional UI changes
   - Detect false positives via pixel diff analysis

2. **Cross-Browser Healing** (v2.1)
   - Browser-specific selector strategies (e.g., Safari vs Chrome)
   - Detect browser-specific failures and apply tailored fixes

3. **ML-Based Selector Prediction** (v3.0)
   - Train local model on historical failures
   - Predict best selector without API call

---

## References

- PBT JIT Protocol: `templates/shared/pbt/just-in-time-protocol.md`
- Test Framework Registry: `memory/domains/test-framework-registry.md`
- Quality Gates: `memory/domains/quality-gates.md` (QG-UI-001, QG-UI-002, QG-UI-003)
- Playwright Docs: https://playwright.dev/docs/selectors
- XCUITest Docs: https://developer.apple.com/documentation/xctest
- Espresso Docs: https://developer.android.com/training/testing/espresso

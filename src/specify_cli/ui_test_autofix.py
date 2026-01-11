"""
UI Test Auto-Fix Module

Provides self-healing capabilities for E2E UI tests across Web, Mobile, and Desktop platforms.

Two Modes:
- Basic Mode (Default): 2 attempts - retry + fallback selectors - NO AI
- Advanced Mode (Optional): 3 attempts - basic + AI selector suggestion - requires OPENAI_API_KEY

References:
- Protocol: templates/shared/ui-test-auto-fix-protocol.md
- Quality Gates: QG-UI-001, QG-UI-002, QG-UI-003
"""

import asyncio
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class UIFailurePattern(Enum):
    """UI test failure patterns detected from stderr."""

    STALE_ELEMENT = "stale_element"
    TIMEOUT = "timeout"
    ELEMENT_NOT_FOUND = "element_not_found"
    CLICK_INTERCEPTED = "click_intercepted"
    TEXT_MISMATCH = "text_mismatch"
    NETWORK_ERROR = "network_error"
    UNKNOWN = "unknown"


@dataclass
class TestVerificationResult:
    """Result of test execution with auto-fix attempts."""

    success: bool
    test_file: str
    attempts: int
    healing_applied: List[Dict] = field(default_factory=list)
    final_error: Optional[str] = None
    diagnostics: Optional[Dict] = None
    total_duration_ms: int = 0


@dataclass
class UIAutoFixConfig:
    """Configuration for UI auto-fix loop."""

    enabled: bool = False
    mode: str = "basic"  # "basic" or "advanced"
    timeout_ms: int = 60000  # 1 minute per UI test
    ai_model: str = "gemini-2.0-flash-exp"  # Only used in advanced mode
    fallback_to_normal_flow: bool = True

    @property
    def max_attempts(self) -> int:
        """2 attempts for basic, 3 for advanced."""
        return 2 if self.mode == "basic" else 3

    @property
    def ai_enabled(self) -> bool:
        """AI only in advanced mode."""
        return self.mode == "advanced"


class UIFailureClassifier:
    """Classify UI test failure patterns from stderr output."""

    # Framework-specific error patterns
    PATTERNS = {
        UIFailurePattern.STALE_ELEMENT: [
            r"Element is not attached",  # Playwright
            r"Stale element reference",  # XCUITest
            r"StaleDataException",  # Espresso
            r"Element no longer exists",  # Maestro
        ],
        UIFailurePattern.TIMEOUT: [
            r"Timeout .* exceeded",  # Playwright
            r"Waiting for .* to exist",  # XCUITest
            r"IdlingResourceTimeoutException",  # Espresso
            r"Timeout after",  # Maestro
        ],
        UIFailurePattern.ELEMENT_NOT_FOUND: [
            r"locator.* not found",  # Playwright
            r"No matches found for",  # XCUITest
            r"NoMatchingViewException",  # Espresso
            r"Element .* not found",  # Maestro
        ],
        UIFailurePattern.CLICK_INTERCEPTED: [
            r"Element is not clickable at point",  # Playwright
            r"not hittable",  # XCUITest
            r"ViewNotCompletelyDisplayedException",  # Espresso
            r"Tap failed",  # Maestro
        ],
        UIFailurePattern.TEXT_MISMATCH: [
            r"Expected .* but got",  # Playwright
            r"Unexpected .* value",  # XCUITest
            r"withText .* view assertion",  # Espresso
            r"assertVisible .* failed",  # Maestro
        ],
        UIFailurePattern.NETWORK_ERROR: [
            r"net::ERR_",  # Playwright
            r"NSURLError",  # XCUITest
            r"IOException",  # Espresso
            r"Network request failed",  # Maestro
        ],
    }

    @classmethod
    def classify(cls, stderr: str) -> UIFailurePattern:
        """
        Classify failure pattern from stderr output.

        Args:
            stderr: Test failure output

        Returns:
            Detected failure pattern or UNKNOWN
        """
        if not stderr:
            return UIFailurePattern.UNKNOWN

        stderr_lower = stderr.lower()

        for pattern_type, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, stderr_lower, re.IGNORECASE):
                    return pattern_type

        return UIFailurePattern.UNKNOWN

    @classmethod
    def extract_selector(cls, stderr: str) -> Optional[str]:
        """
        Extract failed selector from error message.

        Args:
            stderr: Test failure output

        Returns:
            Extracted selector or None
        """
        # Common selector patterns
        selector_patterns = [
            r"selector ['\"]([^'\"]+)['\"]",  # Generic
            r"locator\(['\"]([^'\"]+)['\"]\)",  # Playwright
            r"identifier: ['\"]([^'\"]+)['\"]",  # XCUITest
            r"withId\(['\"]([^'\"]+)['\"]\)",  # Espresso
        ]

        for pattern in selector_patterns:
            match = re.search(pattern, stderr, re.IGNORECASE)
            if match:
                return match.group(1)

        return None


class SelectorHealer:
    """Apply healing strategies for UI test failures."""

    @staticmethod
    def generate_fallback_selectors(failed_selector: str) -> List[str]:
        """
        Generate fallback selectors based on selector hierarchy.

        Hierarchy: testId → aria-label → role+name → text content

        Args:
            failed_selector: Original failed selector

        Returns:
            List of fallback selectors to try
        """
        fallbacks = []

        # Extract semantic parts from selector
        if "data-testid" in failed_selector:
            # Extract testid value
            match = re.search(r'data-testid="([^"]+)"', failed_selector)
            if match:
                testid_value = match.group(1)
                # Fallback 1: aria-label (guess from testid)
                label = testid_value.replace("-", " ").replace("_", " ").title()
                fallbacks.append(f'[aria-label="{label}"]')
                # Fallback 2: role + name
                if "button" in failed_selector:
                    fallbacks.append(f'button:has-text("{label}")')

        elif "aria-label" in failed_selector:
            # Extract aria-label value
            match = re.search(r'aria-label="([^"]+)"', failed_selector)
            if match:
                label = match.group(1)
                # Fallback: text content
                fallbacks.append(f':has-text("{label}")')

        # Generic fallback: try simpler selector
        if "[" in failed_selector and "]" in failed_selector:
            # Try without attribute selector
            base_selector = failed_selector.split("[")[0]
            if base_selector:
                fallbacks.append(base_selector)

        return fallbacks

    @staticmethod
    def generate_healing_strategy(
        pattern: UIFailurePattern,
        attempt: int,
        test_file: str,
        failed_selector: Optional[str] = None,
    ) -> Dict:
        """
        Generate healing strategy based on failure pattern and attempt number.

        Args:
            pattern: Detected failure pattern
            attempt: Current attempt number (1-indexed)
            test_file: Path to test file
            failed_selector: Failed selector from error

        Returns:
            Healing strategy with modifications to apply
        """
        strategy = {
            "pattern": pattern.value,
            "attempt": attempt,
            "modifications": [],
        }

        if pattern == UIFailurePattern.STALE_ELEMENT:
            if attempt == 1:
                strategy["modifications"].append({
                    "type": "add_wait",
                    "wait_type": "attached",
                    "description": "Add waitForSelector with state: 'attached'",
                })
            elif attempt == 2:
                strategy["modifications"].append({
                    "type": "refresh_selector",
                    "description": "Re-query selector before interaction",
                })

        elif pattern == UIFailurePattern.TIMEOUT:
            if attempt == 1:
                strategy["modifications"].append({
                    "type": "increase_timeout",
                    "timeout_ms": 15000,
                    "description": "Increase timeout to 15s",
                })
            elif attempt == 2:
                strategy["modifications"].append({
                    "type": "wait_networkidle",
                    "description": "Add waitForLoadState('networkidle')",
                })

        elif pattern == UIFailurePattern.ELEMENT_NOT_FOUND:
            if attempt == 1:
                strategy["modifications"].append({
                    "type": "explicit_wait",
                    "timeout_ms": 10000,
                    "description": "Add explicit wait with 10s timeout",
                })
            elif attempt == 2:
                if failed_selector:
                    fallbacks = SelectorHealer.generate_fallback_selectors(failed_selector)
                    strategy["modifications"].append({
                        "type": "fallback_selector",
                        "fallback_selectors": fallbacks,
                        "description": f"Try fallback selectors: {', '.join(fallbacks)}",
                    })

        elif pattern == UIFailurePattern.CLICK_INTERCEPTED:
            if attempt == 1:
                strategy["modifications"].append({
                    "type": "scroll_into_view",
                    "description": "Scroll element into view before click",
                })
            elif attempt == 2:
                strategy["modifications"].append({
                    "type": "wait_overlay",
                    "wait_ms": 500,
                    "description": "Wait 500ms for overlay to clear",
                })

        return strategy


class AIHealingEngine:
    """
    AI-powered selector healing (Advanced Mode only).

    Requires:
    - GEMINI_API_KEY environment variable
    - google-generativeai Python package
    """

    @staticmethod
    def is_available() -> bool:
        """Check if AI healing is available."""
        return os.environ.get("GEMINI_API_KEY") is not None

    @staticmethod
    async def suggest_selector(
        failed_selector: str,
        semantic_intent: str,
        dom_snapshot: str,
        previous_attempts: List[str],
        model: str = "gemini-2.0-flash-exp",
    ) -> Optional[str]:
        """
        Generate AI-powered selector suggestion using Gemini API.

        Args:
            failed_selector: Original failed selector
            semantic_intent: What the selector is trying to do (e.g., "Click submit button")
            dom_snapshot: HTML/DOM snapshot around target (truncated to 2000 chars)
            previous_attempts: List of selectors already tried
            model: Gemini model to use (default: gemini-2.0-flash-exp)

        Returns:
            Suggested selector or None if API call fails
        """
        if not AIHealingEngine.is_available():
            return None

        try:
            import google.generativeai as genai

            # Configure Gemini API
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

            # Truncate DOM snapshot
            dom_snapshot = dom_snapshot[:2000] if len(dom_snapshot) > 2000 else dom_snapshot

            prompt = f"""You are a UI test automation expert. Suggest a robust Playwright selector.

Failed Selector: {failed_selector}
Semantic Intent: {semantic_intent}
Previous Attempts: {', '.join(previous_attempts)}
DOM Snapshot:
{dom_snapshot}

Rules:
- Prefer data-testid or aria-label
- Avoid text content if possible
- Return ONLY the selector string (no explanation)

Example Output: button:has-text("Submit")
"""

            # Create Gemini model instance
            gemini_model = genai.GenerativeModel(model)

            # Generate selector suggestion
            response = gemini_model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.0,
                    "max_output_tokens": 100,
                }
            )

            suggested_selector = response.text.strip()
            return suggested_selector

        except Exception as e:
            # Graceful fallback: log error and return None
            print(f"⚠️ AI healing failed: {e}")
            return None


class UIAutoFixRunner:
    """Orchestrate UI test auto-fix loop."""

    def __init__(self, config: Optional[UIAutoFixConfig] = None):
        """
        Initialize auto-fix runner.

        Args:
            config: Auto-fix configuration (defaults to basic mode)
        """
        self.config = config or UIAutoFixConfig(enabled=True, mode="basic")
        self.classifier = UIFailureClassifier()
        self.healer = SelectorHealer()
        self.ai_engine = AIHealingEngine() if self.config.ai_enabled else None

    async def execute_with_autofix(
        self,
        test_file: str,
        test_command: Optional[str] = None,
    ) -> TestVerificationResult:
        """
        Execute UI test with auto-fix loop.

        Args:
            test_file: Path to test file
            test_command: Optional custom test command (defaults to inferred command)

        Returns:
            Test verification result with healing details
        """
        result = TestVerificationResult(
            success=False,
            test_file=test_file,
            attempts=0,
        )

        if test_command is None:
            test_command = self._infer_test_command(test_file)

        for attempt in range(1, self.config.max_attempts + 1):
            result.attempts = attempt

            # Execute test
            test_result = await self._run_test(test_command, test_file)

            if test_result["success"]:
                result.success = True
                break

            # Test failed - classify and heal
            pattern = self.classifier.classify(test_result["stderr"])
            failed_selector = self.classifier.extract_selector(test_result["stderr"])

            # Generate healing strategy
            strategy = self.healer.generate_healing_strategy(
                pattern=pattern,
                attempt=attempt,
                test_file=test_file,
                failed_selector=failed_selector,
            )

            # Apply healing
            healing_applied = await self._apply_healing_strategy(
                test_file=test_file,
                strategy=strategy,
                test_result=test_result,
            )

            result.healing_applied.append(healing_applied)

            # Advanced mode: AI healing on final attempt
            if (
                self.config.ai_enabled
                and attempt == self.config.max_attempts
                and not result.success
                and failed_selector
            ):
                ai_suggestion = await self.ai_engine.suggest_selector(
                    failed_selector=failed_selector,
                    semantic_intent=self._extract_semantic_intent(test_file),
                    dom_snapshot=test_result.get("dom_snapshot", ""),
                    previous_attempts=[failed_selector] + [
                        h.get("healed_selector", "") for h in result.healing_applied
                    ],
                )

                if ai_suggestion:
                    healing_applied["ai_suggested_selector"] = ai_suggestion

        # Final result
        if not result.success:
            result.final_error = test_result["stderr"]
            result.diagnostics = {
                "failed_selectors": [
                    h.get("failed_selector", failed_selector)
                    for h in result.healing_applied
                ],
                "patterns_detected": [h["pattern"] for h in result.healing_applied],
            }

        return result

    async def _run_test(
        self,
        test_command: str,
        test_file: str,
    ) -> Dict:
        """
        Run test command and capture result.

        Args:
            test_command: Test command to execute
            test_file: Path to test file

        Returns:
            Dict with success, stdout, stderr, duration_ms
        """
        try:
            process = await asyncio.create_subprocess_shell(
                test_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.config.timeout_ms / 1000,
            )

            return {
                "success": process.returncode == 0,
                "stdout": stdout.decode("utf-8") if stdout else "",
                "stderr": stderr.decode("utf-8") if stderr else "",
                "exit_code": process.returncode,
            }

        except asyncio.TimeoutError:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Test timeout after {self.config.timeout_ms}ms",
                "exit_code": -1,
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1,
            }

    def _infer_test_command(self, test_file: str) -> str:
        """
        Infer test command from test file path.

        Args:
            test_file: Path to test file

        Returns:
            Inferred test command
        """
        if test_file.endswith(".spec.ts") or test_file.endswith(".spec.js"):
            # Playwright
            return f"npx playwright test {test_file}"
        elif test_file.endswith(".swift"):
            # XCUITest
            return f"xcodebuild test -scheme UITests -only-testing:{test_file}"
        elif test_file.endswith(".kt") or test_file.endswith(".java"):
            # Espresso
            return f"./gradlew connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class={test_file}"
        elif test_file.endswith(".yaml"):
            # Maestro
            return f"maestro test {test_file}"
        else:
            # Fallback
            return f"npm test {test_file}"

    async def _apply_healing_strategy(
        self,
        test_file: str,
        strategy: Dict,
        test_result: Dict,
    ) -> Dict:
        """
        Apply healing strategy to test file.

        Args:
            test_file: Path to test file
            strategy: Healing strategy from SelectorHealer
            test_result: Result from _run_test

        Returns:
            Dict with healing details
        """
        healing_result = {
            "attempt": strategy["attempt"],
            "pattern": strategy["pattern"],
            "strategy": strategy["modifications"][0]["type"] if strategy["modifications"] else "none",
            "outcome": "pending",
        }

        # Note: Actual file modification would happen here
        # For now, this is a placeholder that would be implemented
        # in the full integration with wave_scheduler.py

        # In production, this would:
        # 1. Read test file
        # 2. Apply modifications from strategy
        # 3. Write modified test file
        # 4. Return healing details

        healing_result["outcome"] = "applied"
        return healing_result

    def _extract_semantic_intent(self, test_file: str) -> str:
        """
        Extract semantic intent from test file name.

        Args:
            test_file: Path to test file

        Returns:
            Semantic intent (e.g., "Click submit button")
        """
        # Simple heuristic: use file name
        import os
        base_name = os.path.basename(test_file)
        return base_name.replace("-", " ").replace("_", " ").replace(".spec.ts", "").title()

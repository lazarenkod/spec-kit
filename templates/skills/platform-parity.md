---
skill_name: platform-parity
category: qa-automation
subcategory: cross-platform-validation
complexity: medium
prerequisites:
  - Cross-platform mobile framework (KMP, Flutter, React Native)
  - iOS and Android implementations
  - Access to both codebases
related_personas:
  - parity-validator-agent
related_skills:
  - binding-test-generator
  - native-profiling
integration_points:
  - /speckit.analyze --profile parity
  - /speckit.analyze --profile qa (conditional)
---

# Platform Parity Validation Skill

## Overview

This skill enables automated validation of cross-platform mobile applications to ensure:
1. **Feature Parity** (QG-PARITY-001): ≥95% of features available on both iOS and Android
2. **UX Adaptation** (QG-PARITY-002): ≥80% of platform-specific patterns correctly applied
3. **Zero Regressions** (QG-PARITY-003): No platform-specific bugs or crashes

## Skill Components

### 1. Feature Inventory Algorithm

#### iOS Feature Detection

**Objective**: Build a complete list of features/screens in the iOS codebase.

**Detection Patterns**:

```swift
// Pattern 1: UIKit ViewControllers
class ProfileViewController: UIViewController { }
class SettingsViewController: UIViewController { }
→ Extract: ["Profile", "Settings"]

// Pattern 2: SwiftUI Views
struct HomeView: View { }
struct SearchView: View { }
→ Extract: ["Home", "Search"]

// Pattern 3: Coordinators (if using Coordinator pattern)
class AuthCoordinator: Coordinator { }
→ Extract: ["Auth"]

// Pattern 4: Tab Bar Items (from storyboards or code)
tabBarController.viewControllers = [homeVC, searchVC, profileVC]
→ Extract: ["Home", "Search", "Profile"]

// Pattern 5: Navigation (from storyboards, segues)
performSegue(withIdentifier: "ShowDetail", sender: self)
→ Extract: ["Detail"]
```

**Grep Commands**:
```bash
# Find all ViewControllers
grep -r "class.*ViewController.*UIViewController" ios/ --include="*.swift" | \
  sed -E 's/.*class ([A-Za-z0-9]+)ViewController.*/\1/' | sort -u

# Find all SwiftUI Views
grep -r "struct.*View.*View" ios/ --include="*.swift" | \
  sed -E 's/.*struct ([A-Za-z0-9]+)View.*/\1/' | sort -u

# Find tab bar items
grep -r "tabBarItem.title" ios/ --include="*.swift" | \
  sed -E 's/.*title = "(.+)".*/\1/' | sort -u
```

**Output Format**:
```json
{
  "platform": "ios",
  "features": [
    {"name": "Home", "type": "UIViewController", "path": "ios/App/Features/Home/HomeViewController.swift"},
    {"name": "Profile", "type": "SwiftUI", "path": "ios/App/Features/Profile/ProfileView.swift"},
    {"name": "Settings", "type": "UIViewController", "path": "ios/App/Features/Settings/SettingsViewController.swift"}
  ],
  "feature_count": 3
}
```

#### Android Feature Detection

**Objective**: Build a complete list of features/screens in the Android codebase.

**Detection Patterns**:

```kotlin
// Pattern 1: Activities
class ProfileActivity : AppCompatActivity() { }
class SettingsActivity : AppCompatActivity() { }
→ Extract: ["Profile", "Settings"]

// Pattern 2: Fragments
class HomeFragment : Fragment() { }
class SearchFragment : Fragment() { }
→ Extract: ["Home", "Search"]

// Pattern 3: Jetpack Compose Screens
@Composable
fun ProfileScreen() { }
→ Extract: ["Profile"]

// Pattern 4: Navigation Graph (from navigation.xml)
<fragment android:id="@+id/homeFragment"
          android:name="com.app.HomeFragment" />
→ Extract: ["Home"]

// Pattern 5: Bottom Navigation (from menu XML)
<item android:id="@+id/navigation_home"
      android:title="Home" />
→ Extract: ["Home"]
```

**Grep Commands**:
```bash
# Find all Activities
grep -r "class.*Activity.*AppCompatActivity" android/ --include="*.kt" | \
  sed -E 's/.*class ([A-Za-z0-9]+)Activity.*/\1/' | sort -u

# Find all Fragments
grep -r "class.*Fragment.*Fragment" android/ --include="*.kt" | \
  sed -E 's/.*class ([A-Za-z0-9]+)Fragment.*/\1/' | sort -u

# Find all Composable screens
grep -r "@Composable" android/ --include="*.kt" -A 1 | \
  grep "fun.*Screen" | sed -E 's/.*fun ([A-Za-z0-9]+)Screen.*/\1/' | sort -u

# Find navigation destinations
grep -r "android:name.*Fragment" android/app/src/main/res/navigation/ --include="*.xml" | \
  sed -E 's/.*\.([A-Za-z0-9]+)Fragment.*/\1/' | sort -u
```

**Output Format**:
```json
{
  "platform": "android",
  "features": [
    {"name": "Home", "type": "Fragment", "path": "android/app/src/main/kotlin/com/app/features/home/HomeFragment.kt"},
    {"name": "Profile", "type": "Composable", "path": "android/app/src/main/kotlin/com/app/features/profile/ProfileScreen.kt"},
    {"name": "Settings", "type": "Activity", "path": "android/app/src/main/kotlin/com/app/features/settings/SettingsActivity.kt"}
  ],
  "feature_count": 3
}
```

#### Feature Matching Algorithm

**Challenge**: Feature names may not match exactly across platforms.

**Fuzzy Matching**:
```python
def match_features(ios_features, android_features):
    """
    Match features across platforms using fuzzy name matching.

    Returns:
        common: List of features present on both platforms
        ios_only: List of features only on iOS
        android_only: List of features only on Android
    """
    from difflib import SequenceMatcher

    def similarity(a, b):
        # Normalize names (lowercase, remove suffixes like ViewController/Activity)
        a_normalized = a.lower().replace("viewcontroller", "").replace("view", "")
        b_normalized = b.lower().replace("activity", "").replace("fragment", "").replace("screen", "")
        return SequenceMatcher(None, a_normalized, b_normalized).ratio()

    common = []
    ios_only = []
    android_only = []

    matched_android = set()

    for ios_feature in ios_features:
        best_match = None
        best_score = 0.0

        for android_feature in android_features:
            if android_feature in matched_android:
                continue

            score = similarity(ios_feature["name"], android_feature["name"])
            if score > best_score:
                best_score = score
                best_match = android_feature

        # Threshold: 0.8 similarity = match
        if best_score >= 0.8:
            common.append({
                "ios": ios_feature,
                "android": best_match,
                "similarity": best_score
            })
            matched_android.add(best_match["name"])
        else:
            ios_only.append(ios_feature)

    # Remaining Android features = Android-only
    for android_feature in android_features:
        if android_feature["name"] not in matched_android:
            android_only.append(android_feature)

    return common, ios_only, android_only
```

**Example**:
```python
ios_features = [
    {"name": "ProfileViewController"},
    {"name": "SettingsView"},
    {"name": "BiometricAuthView"}
]

android_features = [
    {"name": "ProfileActivity"},
    {"name": "SettingsFragment"},
    {"name": "NotificationSettingsFragment"}
]

common, ios_only, android_only = match_features(ios_features, android_features)

# common = [
#     {"ios": "ProfileViewController", "android": "ProfileActivity", "similarity": 0.85},
#     {"ios": "SettingsView", "android": "SettingsFragment", "similarity": 0.82}
# ]
# ios_only = ["BiometricAuthView"]
# android_only = ["NotificationSettingsFragment"]
```

#### Feature Parity Score Calculation (QG-PARITY-001)

```python
def calculate_parity_score(common, ios_only, android_only):
    """
    Calculate feature parity score.

    Formula:
        Parity Score = (Common Features / Total Unique Features) × 100%

    Target: ≥95%
    """
    total_unique = len(common) + len(ios_only) + len(android_only)

    if total_unique == 0:
        return 100.0  # No features = perfect parity (edge case)

    parity_score = (len(common) / total_unique) * 100.0

    return {
        "score": parity_score,
        "common": len(common),
        "ios_only": len(ios_only),
        "android_only": len(android_only),
        "total": total_unique,
        "threshold": 95.0,
        "status": "PASS" if parity_score >= 95.0 else "FAIL"
    }
```

**Output**:
```json
{
  "score": 96.0,
  "common": 24,
  "ios_only": 1,
  "android_only": 0,
  "total": 25,
  "threshold": 95.0,
  "status": "PASS"
}
```

---

### 2. UX Adaptation Analysis

#### iOS Platform Patterns Checklist

**Pattern 1: Navigation**
```swift
// ✅ CORRECT: UINavigationController with back button
navigationController?.pushViewController(detailVC, animated: true)

// ❌ INCORRECT: Manual back button (Android pattern)
let backButton = UIButton()
backButton.setTitle("←", for: .normal)
```

**Pattern 2: Tab Bar**
```swift
// ✅ CORRECT: UITabBarController at bottom
let tabBarController = UITabBarController()
tabBarController.viewControllers = [homeVC, searchVC, profileVC]

// ❌ INCORRECT: Top navigation (Android pattern)
let segmentedControl = UISegmentedControl(items: ["Home", "Search", "Profile"])
```

**Pattern 3: Modals**
```swift
// ✅ CORRECT: Sheet presentation with swipe-to-dismiss
present(modalVC, animated: true)

// ❌ INCORRECT: Fullscreen modal without dismiss gesture
modalVC.modalPresentationStyle = .fullScreen
```

**Pattern 4: List Actions**
```swift
// ✅ CORRECT: Swipe actions (leading/trailing)
func tableView(_ tableView: UITableView, trailingSwipeActionsConfigurationForRowAt indexPath: IndexPath) -> UISwipeActionsConfiguration? {
    let deleteAction = UIContextualAction(style: .destructive, title: "Delete") { ... }
    return UISwipeActionsConfiguration(actions: [deleteAction])
}

// ❌ INCORRECT: Long press menu (Android pattern)
let longPress = UILongPressGestureRecognizer(target: self, action: #selector(showMenu))
```

**Pattern 5: Haptic Feedback**
```swift
// ✅ CORRECT: UIFeedbackGenerator for haptics
let impactFeedback = UIImpactFeedbackGenerator(style: .medium)
impactFeedback.impactOccurred()

// ❌ INCORRECT: No haptic feedback (missed iOS pattern)
```

**Pattern 6: Share Sheet**
```swift
// ✅ CORRECT: UIActivityViewController
let activityVC = UIActivityViewController(activityItems: [shareText], applicationActivities: nil)
present(activityVC, animated: true)

// ❌ INCORRECT: Custom share dialog
```

**Pattern 7: Search**
```swift
// ✅ CORRECT: UISearchController in navigation bar
let searchController = UISearchController(searchResultsController: nil)
navigationItem.searchController = searchController

// ❌ INCORRECT: Search button that opens full-screen search
```

#### Android Platform Patterns Checklist

**Pattern 1: Navigation**
```kotlin
// ✅ CORRECT: Jetpack Navigation with back gesture
findNavController().navigate(R.id.action_home_to_detail)

// ❌ INCORRECT: iOS-style back button in top-left
```

**Pattern 2: Bottom Navigation**
```kotlin
// ✅ CORRECT: BottomNavigationView or NavigationBar
binding.bottomNav.setOnItemSelectedListener { ... }

// ❌ INCORRECT: Top tabs (iOS pattern)
```

**Pattern 3: FAB (Floating Action Button)**
```kotlin
// ✅ CORRECT: FAB for primary action
binding.fab.setOnClickListener { createNewItem() }

// ❌ INCORRECT: "+" button in top-right toolbar (iOS pattern)
```

**Pattern 4: Snackbars**
```kotlin
// ✅ CORRECT: Material Snackbar for feedback
Snackbar.make(view, "Item deleted", Snackbar.LENGTH_LONG)
    .setAction("UNDO") { undoDelete() }
    .show()

// ❌ INCORRECT: iOS-style alert dialog for simple feedback
AlertDialog.Builder(context).setMessage("Item deleted").show()
```

**Pattern 5: Material Animations**
```kotlin
// ✅ CORRECT: Material motion transitions
startActivity(intent, ActivityOptions.makeSceneTransitionAnimation(this).toBundle())

// ❌ INCORRECT: No transitions (static)
```

**Pattern 6: Share Intent**
```kotlin
// ✅ CORRECT: Intent.ACTION_SEND for sharing
val shareIntent = Intent().apply {
    action = Intent.ACTION_SEND
    putExtra(Intent.EXTRA_TEXT, shareText)
    type = "text/plain"
}
startActivity(Intent.createChooser(shareIntent, "Share via"))

// ❌ INCORRECT: Custom share dialog
```

**Pattern 7: Search**
```kotlin
// ✅ CORRECT: SearchView in toolbar/ActionBar
override fun onCreateOptionsMenu(menu: Menu): Boolean {
    menuInflater.inflate(R.menu.main_menu, menu)
    val searchItem = menu.findItem(R.id.action_search)
    val searchView = searchItem.actionView as SearchView
    return true
}

// ❌ INCORRECT: Separate search screen (iOS pattern)
```

#### UX Adaptation Scoring Algorithm

```python
def score_ux_adaptation(screen_name, ios_code, android_code):
    """
    Score UX adaptation for a single screen (0-100).

    Checks:
    - Navigation pattern (20pt)
    - Primary action placement (20pt)
    - Modal/dialog presentation (15pt)
    - List interactions (15pt)
    - Haptic/feedback (10pt)
    - Share functionality (10pt)
    - Search UI (10pt)

    Returns:
        ios_score: 0-100
        android_score: 0-100
        issues: List of detected issues
    """
    ios_score = 0
    android_score = 0
    issues = []

    # Check 1: Navigation (20pt)
    if "UINavigationController" in ios_code or "navigationController?.push" in ios_code:
        ios_score += 20
    else:
        issues.append(f"{screen_name} (iOS): Missing UINavigationController pattern")

    if "findNavController()" in android_code or "NavController" in android_code:
        android_score += 20
    else:
        issues.append(f"{screen_name} (Android): Missing Jetpack Navigation pattern")

    # Check 2: Primary Action (20pt)
    if "navigationItem.rightBarButtonItem" in ios_code:
        ios_score += 20

    if "FloatingActionButton" in android_code or "fab.setOnClickListener" in android_code:
        android_score += 20
    else:
        issues.append(f"{screen_name} (Android): Missing FAB for primary action")

    # Check 3: Modal Presentation (15pt)
    if "present(" in ios_code and "animated: true" in ios_code:
        ios_score += 15

    if "BottomSheetDialogFragment" in android_code or "Dialog" in android_code:
        android_score += 15

    # Check 4: List Interactions (15pt)
    if "trailingSwipeActionsConfiguration" in ios_code:
        ios_score += 15
    else:
        issues.append(f"{screen_name} (iOS): Missing swipe actions on lists")

    if "ItemTouchHelper" in android_code or "onItemLongClick" in android_code:
        android_score += 15

    # Check 5: Haptic/Feedback (10pt)
    if "UIFeedbackGenerator" in ios_code or "impactOccurred()" in ios_code:
        ios_score += 10
    else:
        issues.append(f"{screen_name} (iOS): Missing haptic feedback")

    if "performHapticFeedback" in android_code:
        android_score += 10

    # Check 6: Share (10pt)
    if "UIActivityViewController" in ios_code:
        ios_score += 10

    if "Intent.ACTION_SEND" in android_code:
        android_score += 10
    else:
        issues.append(f"{screen_name} (Android): Using custom share dialog instead of Intent.ACTION_SEND")

    # Check 7: Search (10pt)
    if "UISearchController" in ios_code:
        ios_score += 10

    if "SearchView" in android_code:
        android_score += 10

    return {
        "screen": screen_name,
        "ios_score": ios_score,
        "android_score": android_score,
        "issues": issues
    }
```

**Aggregate Score Calculation (QG-PARITY-002)**:

```python
def calculate_adaptation_score(all_screens):
    """
    Calculate overall UX adaptation score across all screens.

    Target: ≥80%
    """
    total_ios_score = sum(s["ios_score"] for s in all_screens)
    total_android_score = sum(s["android_score"] for s in all_screens)
    num_screens = len(all_screens)

    avg_ios_score = total_ios_score / (num_screens * 100) * 100 if num_screens > 0 else 0
    avg_android_score = total_android_score / (num_screens * 100) * 100 if num_screens > 0 else 0

    overall_score = (avg_ios_score + avg_android_score) / 2

    return {
        "overall_score": overall_score,
        "ios_avg": avg_ios_score,
        "android_avg": avg_android_score,
        "threshold": 80.0,
        "status": "PASS" if overall_score >= 80.0 else "FAIL"
    }
```

---

### 3. Regression Detection

#### Platform-Specific Crash Detection (QG-PARITY-003)

**iOS Crash Log Parsing**:

```bash
# Parse iOS crash logs (.crash files)
grep -r "Exception Type:" ios/CrashLogs/ --include="*.crash" | \
  sed -E 's/.*Exception Type: (.+)/\1/' | sort | uniq -c

# Extract crash stack traces
awk '/Thread 0 Crashed:/,/^$/' ios/CrashLogs/*.crash
```

**Android Crash Log Parsing**:

```bash
# Parse Android crash logs (logcat, Crashlytics)
grep -r "FATAL EXCEPTION" android/CrashLogs/ | \
  sed -E 's/.*FATAL EXCEPTION: (.+)/\1/' | sort | uniq -c

# Extract stack traces
grep -A 20 "FATAL EXCEPTION" android/CrashLogs/*.log
```

**Regression Detection Algorithm**:

```python
def detect_platform_specific_crashes(ios_crashes, android_crashes):
    """
    Identify crashes that only occur on one platform.

    Returns:
        ios_only_crashes: List of crashes only on iOS
        android_only_crashes: List of crashes only on Android
        common_crashes: List of crashes on both platforms
    """
    ios_crash_types = set(c["type"] for c in ios_crashes)
    android_crash_types = set(c["type"] for c in android_crashes)

    ios_only = [c for c in ios_crashes if c["type"] not in android_crash_types]
    android_only = [c for c in android_crashes if c["type"] not in ios_crash_types]
    common = [c for c in ios_crashes if c["type"] in android_crash_types]

    return {
        "ios_only_crashes": ios_only,
        "android_only_crashes": android_only,
        "common_crashes": common,
        "regression_detected": len(ios_only) > 0 or len(android_only) > 0,
        "status": "FAIL" if len(ios_only) > 0 or len(android_only) > 0 else "PASS"
    }
```

**Example Output**:
```json
{
  "ios_only_crashes": [],
  "android_only_crashes": [
    {
      "type": "NullPointerException",
      "location": "ProfileViewModel.updateBio",
      "stack_trace": "at com.app.ProfileViewModel.updateBio(ProfileViewModel.kt:45)",
      "frequency": 12,
      "first_seen": "2026-01-10"
    }
  ],
  "common_crashes": [],
  "regression_detected": true,
  "status": "FAIL"
}
```

#### Synchronization Validation

**Check 1: Offline-First Implementation**

```kotlin
// iOS (Swift)
func syncData() async throws {
    let localData = try await localDatabase.fetchAll()
    let remoteData = try await apiClient.fetchAll()
    let merged = merge(local: localData, remote: remoteData)
    try await localDatabase.save(merged)
}

// Android (Kotlin)
suspend fun syncData() {
    val localData = localDatabase.fetchAll()
    val remoteData = apiClient.fetchAll()
    val merged = merge(local = localData, remote = remoteData)
    localDatabase.save(merged)
}
```

**Validation**:
```python
def validate_sync_logic(ios_code, android_code):
    """
    Verify sync logic is equivalent on both platforms.

    Checks:
    - Both have local database access
    - Both have API client calls
    - Both have merge logic
    - Conflict resolution is identical
    """
    issues = []

    # Check local database access
    if "localDatabase" not in ios_code:
        issues.append("iOS: Missing local database access in sync logic")
    if "localDatabase" not in android_code:
        issues.append("Android: Missing local database access in sync logic")

    # Check API calls
    if "apiClient" not in ios_code:
        issues.append("iOS: Missing API client calls in sync logic")
    if "apiClient" not in android_code:
        issues.append("Android: Missing API client calls in sync logic")

    # Check merge logic exists
    if "merge(" not in ios_code:
        issues.append("iOS: Missing merge logic in sync")
    if "merge(" not in android_code:
        issues.append("Android: Missing merge logic in sync")

    return {
        "sync_parity": len(issues) == 0,
        "issues": issues
    }
```

#### Performance Comparison

```python
def compare_performance_metrics(ios_metrics, android_metrics):
    """
    Compare performance metrics across platforms.

    Flag if disparity > 30%
    """
    def calculate_disparity(ios_val, android_val):
        avg = (ios_val + android_val) / 2
        return abs(ios_val - android_val) / avg * 100 if avg > 0 else 0

    cold_start_disparity = calculate_disparity(
        ios_metrics["cold_start_ms"],
        android_metrics["cold_start_ms"]
    )

    fps_disparity = calculate_disparity(
        ios_metrics["fps_p95"],
        android_metrics["fps_p95"]
    )

    memory_disparity = calculate_disparity(
        ios_metrics["memory_peak_mb"],
        android_metrics["memory_peak_mb"]
    )

    issues = []
    if cold_start_disparity > 30:
        issues.append(f"Cold start disparity: {cold_start_disparity:.1f}% (iOS: {ios_metrics['cold_start_ms']}ms, Android: {android_metrics['cold_start_ms']}ms)")
    if fps_disparity > 30:
        issues.append(f"FPS disparity: {fps_disparity:.1f}% (iOS: {ios_metrics['fps_p95']} FPS, Android: {android_metrics['fps_p95']} FPS)")
    if memory_disparity > 30:
        issues.append(f"Memory disparity: {memory_disparity:.1f}% (iOS: {ios_metrics['memory_peak_mb']}MB, Android: {android_metrics['memory_peak_mb']}MB)")

    return {
        "cold_start_disparity": cold_start_disparity,
        "fps_disparity": fps_disparity,
        "memory_disparity": memory_disparity,
        "issues": issues,
        "status": "PASS" if len(issues) == 0 else "WARNING"
    }
```

---

## Integration Workflow

### Command: `/speckit.analyze --profile parity`

**Phase 1: Feature Inventory** (2-3 minutes)
```text
1. Detect platform (KMP, Flutter, React Native)
2. Scan iOS codebase in parallel:
   - ViewControllers (grep for "class.*ViewController")
   - SwiftUI Views (grep for "struct.*View.*View")
   - Tab bar items
3. Scan Android codebase in parallel:
   - Activities (grep for "class.*Activity")
   - Fragments (grep for "class.*Fragment")
   - Composables (grep for "@Composable.*Screen")
4. Build feature matrices (JSON)
```

**Phase 2: Feature Parity Analysis** (1-2 minutes)
```text
1. Match features using fuzzy matching algorithm
2. Calculate parity score
3. Classify missing features (critical vs. nice-to-have)
4. Generate recommendations
```

**Phase 3: UX Adaptation Analysis** (3-5 minutes)
```text
1. For each matched feature:
   - Read iOS implementation file
   - Read Android implementation file
   - Score iOS patterns (0-100)
   - Score Android patterns (0-100)
2. Calculate average adaptation score
3. Identify pattern violations
```

**Phase 4: Regression Detection** (2-3 minutes)
```text
1. Parse crash logs (if available)
2. Compare crash types (iOS-only vs Android-only)
3. Validate sync logic equivalence
4. Compare performance metrics
5. Flag platform-specific issues
```

**Phase 5: Report Generation** (1 minute)
```text
1. Generate reports/parity-report.md
2. Update MQS parity score (0-20 points)
3. Exit with code 0 (pass) or 1 (fail)
```

**Total Time**: ~9-14 minutes

---

## Report Format

### reports/parity-report.md

```markdown
# Cross-Platform Parity Report

**Generated**: 2026-01-11 14:30:00
**Platform**: Kotlin Multiplatform (KMP)
**iOS Version**: 1.2.0
**Android Version**: 1.2.0

---

## Executive Summary

| Metric | Score | Threshold | Status |
|--------|-------|-----------|--------|
| Feature Parity | 96% | ≥95% | ✅ PASS |
| UX Adaptation | 85% | ≥80% | ✅ PASS |
| Platform Regressions | 1 crash | 0 | ❌ FAIL |

**Overall Status**: ⚠️ REGRESSION BLOCKING RELEASE

---

## 1. Feature Parity Analysis (QG-PARITY-001)

### Feature Matrix

| Feature | iOS | Android | Status |
|---------|-----|---------|--------|
| Home | ✅ | ✅ | ✅ |
| Profile | ✅ | ✅ | ✅ |
| Settings | ✅ | ✅ | ✅ |
| Search | ✅ | ✅ | ✅ |
| Notifications | ✅ | ✅ | ✅ |
| Biometric Auth | ✅ | ❌ | ⚠️ iOS-only |

### Missing Features

#### Android Missing (1 feature)
- **Biometric Authentication**
  - **Criticality**: HIGH
  - **Reason**: Android BiometricPrompt API not implemented
  - **Recommendation**: Implement BiometricPrompt in AuthViewModel wrapper
  - **Estimated Effort**: 2-3 hours

### Parity Score: 24/25 features = 96% ✅

---

## 2. UX Adaptation Analysis (QG-PARITY-002)

### Screen-by-Screen Scores

| Screen | iOS Score | Android Score | Average |
|--------|-----------|---------------|---------|
| Home | 95 | 90 | 92.5 |
| Profile | 100 | 100 | 100 |
| Settings | 70 | 75 | 72.5 |
| Search | 90 | 85 | 87.5 |
| Notifications | 85 | 80 | 82.5 |

### Issues Found

#### Settings Screen (iOS: 70/100)
- ❌ Missing swipe actions on list items (expected iOS pattern)
- ❌ No haptic feedback on toggle switches
- ✅ UINavigationController used correctly
- ✅ Share sheet implemented

#### Settings Screen (Android: 75/100)
- ❌ Share action uses custom dialog instead of Intent.ACTION_SEND
- ✅ Bottom navigation implemented
- ✅ Material snackbar for feedback
- ✅ Jetpack Navigation used

### Overall Adaptation Score: 85/100 ✅

---

## 3. Regression Detection (QG-PARITY-003)

### Platform-Specific Crashes

#### iOS-Only Crashes: 0 ✅

#### Android-Only Crashes: 1 ❌

**Crash #1: NullPointerException in ProfileViewModel**
- **Location**: `ProfileViewModel.updateBio (ProfileViewModel.kt:45)`
- **Frequency**: 12 occurrences in last 7 days
- **First Seen**: 2026-01-10
- **Stack Trace**:
  ```
  java.lang.NullPointerException: Parameter specified as non-null is null
      at com.app.ProfileViewModel.updateBio(ProfileViewModel.kt:45)
      at com.app.ProfileActivity.onSaveClicked(ProfileActivity.kt:102)
  ```
- **Root Cause**: Android wrapper doesn't null-check bio parameter before calling shared ViewModel
- **Fix**: Add null check in Android wrapper:
  ```kotlin
  fun updateBio(bio: String?) {
      viewModel.updateBio(bio ?: return)
  }
  ```

### Synchronization Issues: 0 ✅

### Performance Disparities

| Metric | iOS | Android | Disparity | Status |
|--------|-----|---------|-----------|--------|
| Cold Start | 1.2s | 1.4s | 16% | ✅ |
| Scroll FPS | 60 | 58 | 3% | ✅ |
| Memory Peak | 110MB | 125MB | 13% | ✅ |

**Status**: ❌ FAIL (1 platform-specific crash detected)

---

## 4. Recommendations (Priority Order)

### CRITICAL (Blocking Release)
1. **Fix Android NullPointerException** in ProfileViewModel.updateBio
   - Add null check in Android wrapper
   - Estimated time: 15 minutes
   - Test: Run ProfileActivityTest.testUpdateBio

### HIGH (Pre-Release)
2. **Implement Biometric Auth on Android**
   - Use BiometricPrompt API
   - Estimated time: 2-3 hours
   - Achieves 100% feature parity

### MEDIUM (Post-Release)
3. **Add swipe actions on iOS Settings screen**
   - Implement trailingSwipeActionsConfiguration
   - Estimated time: 1 hour

4. **Fix Android share action**
   - Replace custom dialog with Intent.ACTION_SEND
   - Estimated time: 30 minutes

---

## 5. MQS Impact

**Platform Parity Component**: 18/20 points

**Breakdown**:
- Feature Parity (10pt): 9.6/10 (96% vs 95% threshold)
- UX Adaptation (6pt): 5.1/6 (85% vs 80% threshold)
- Regressions (4pt): 0/4 (1 crash vs 0 threshold) ❌

**Total MQS**: 84/100 (down from 88/100 due to regression)

---

## Validation Commands

```bash
# Re-run parity validation
specify analyze --profile parity

# Check QG-PARITY-001
if [ $(jq '.parity_score' reports/parity-score.json) -ge 95 ]; then echo "PASS"; else echo "FAIL"; fi

# Check QG-PARITY-002
if [ $(jq '.adaptation_score' reports/parity-score.json) -ge 80 ]; then echo "PASS"; else echo "FAIL"; fi

# Check QG-PARITY-003
if [ $(jq '.regression_count' reports/parity-score.json) -eq 0 ]; then echo "PASS"; else echo "FAIL"; fi
```

---

**Report Version**: 1.0
**Generated by**: parity-validator-agent (platform-parity skill)
```

---

## Quality Gate Definitions

### QG-PARITY-001: Feature Parity ≥ 95%

**Validation**:
```bash
parity_score=$(jq '.parity_score' reports/parity-score.json)
if [ "$parity_score" -ge 95 ]; then
    echo "QG-PARITY-001: PASS ($parity_score%)"
    exit 0
else
    echo "QG-PARITY-001: FAIL ($parity_score% < 95% threshold)"
    exit 1
fi
```

### QG-PARITY-002: UX Adaptation Score ≥ 80%

**Validation**:
```bash
adaptation_score=$(jq '.adaptation_score' reports/parity-score.json)
if [ "$adaptation_score" -ge 80 ]; then
    echo "QG-PARITY-002: PASS ($adaptation_score%)"
    exit 0
else
    echo "QG-PARITY-002: FAIL ($adaptation_score% < 80% threshold)"
    exit 1
fi
```

### QG-PARITY-003: Zero Platform-Specific Regressions

**Validation**:
```bash
regression_count=$(jq '.regression_count' reports/parity-score.json)
if [ "$regression_count" -eq 0 ]; then
    echo "QG-PARITY-003: PASS (0 regressions)"
    exit 0
else
    echo "QG-PARITY-003: FAIL ($regression_count regressions detected)"
    jq '.regressions' reports/parity-score.json
    exit 1
fi
```

---

## Success Criteria

**Parity Validation Succeeds When**:
1. ✅ Feature parity ≥ 95% (QG-PARITY-001)
2. ✅ UX adaptation score ≥ 80% (QG-PARITY-002)
3. ✅ Zero platform-specific regressions (QG-PARITY-003)

**All three quality gates must pass for release approval.**

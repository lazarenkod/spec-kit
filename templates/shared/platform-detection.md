# Platform Detection Module

## Purpose

Automatically detect cross-platform mobile frameworks from constitution, user input, or codebase analysis.
This module is consumed by `/speckit.constitution`, `/speckit.plan`, and `/speckit.tasks` commands.

## Platform Keywords

```text
PLATFORM_KEYWORDS = {
  "kmp": [
    "kotlin multiplatform",
    "kmp",
    "kmm",
    "iosMain",
    "androidMain",
    "shared module",
    "commonMain",
    "linkDebugFramework",
    "kotlin native"
  ],
  "flutter": [
    "flutter",
    "dart",
    "pubspec.yaml",
    "lib/main.dart",
    "flutter_bloc",
    "flutter_riverpod",
    "widget"
  ],
  "react_native": [
    "react native",
    "react-native",
    "metro.config",
    "index.js",
    "react-native.config",
    "expo",
    "react-native-cli"
  ],
  "compose_multiplatform": [
    "compose multiplatform",
    "composeApp",
    "jetbrains compose",
    "compose desktop"
  ]
}
```

## Detection Algorithm

### Step 1: Check Constitution

```text
READ constitution.md

SEARCH for Technology Stack section:
  IF contains any PLATFORM_KEYWORDS[platform]:
    DETECTED_PLATFORM = platform
    DETECTION_SOURCE = "constitution"
    RETURN DETECTED_PLATFORM
```

### Step 2: Check User Input (if /speckit.constitution)

```text
IF user_input contains any PLATFORM_KEYWORDS[platform]:
  DETECTED_PLATFORM = platform
  DETECTION_SOURCE = "user_input"
  RETURN DETECTED_PLATFORM
```

### Step 3: Scan Codebase

```text
# KMP Detection
IF exists(build.gradle.kts OR build.gradle):
  READ content
  IF contains "kotlin(\"multiplatform\")" OR "KotlinMultiplatform":
    IF contains "iosMain" OR "iosArm64" OR "iosX64":
      DETECTED_PLATFORM = "kmp"
      DETECTION_SOURCE = "codebase:build.gradle.kts"
      RETURN DETECTED_PLATFORM

# Flutter Detection
IF exists(pubspec.yaml):
  READ content
  IF contains "flutter:" AND "sdk: flutter":
    DETECTED_PLATFORM = "flutter"
    DETECTION_SOURCE = "codebase:pubspec.yaml"
    RETURN DETECTED_PLATFORM

# React Native Detection
IF exists(package.json):
  READ content
  IF contains "react-native" in dependencies:
    DETECTED_PLATFORM = "react_native"
    DETECTION_SOURCE = "codebase:package.json"
    RETURN DETECTED_PLATFORM

# Compose Multiplatform Detection
IF exists(build.gradle.kts):
  IF contains "org.jetbrains.compose" OR "composeApp":
    DETECTED_PLATFORM = "compose_multiplatform"
    DETECTION_SOURCE = "codebase:build.gradle.kts"
    RETURN DETECTED_PLATFORM

DETECTED_PLATFORM = null
DETECTION_SOURCE = "none"
RETURN null
```

## Output Format

```text
PLATFORM_DETECTION_RESULT = {
  platform: "kmp" | "flutter" | "react_native" | "compose_multiplatform" | null,
  source: "constitution" | "user_input" | "codebase:{file}" | "none",
  confidence: "high" | "medium" | "low",
  constitution_file: "memory/platforms/{platform}.md" | null,
  checklist_file: "templates/shared/platforms/{platform}-integration-checklist.md" | null
}
```

## Platform to File Mapping

| Platform | Constitution File | Integration Checklist |
|----------|------------------|----------------------|
| `kmp` | `memory/platforms/kmp.md` | `templates/shared/platforms/kmp-integration-checklist.md` |
| `flutter` | `memory/platforms/flutter.md` | `templates/shared/platforms/flutter-integration-checklist.md` |
| `react_native` | `memory/platforms/react-native.md` | `templates/shared/platforms/rn-integration-checklist.md` |
| `compose_multiplatform` | `memory/platforms/kmp.md` | `templates/shared/platforms/kmp-integration-checklist.md` |

## Integration Points

### /speckit.constitution

```text
IF app_type == "Mobile Application":
  Run platform detection
  IF DETECTED_PLATFORM != null:
    SKIP Question 4 (already detected)
    COPY platform constitution to memory/constitution.platform.md
  ELSE:
    ASK Question 4: "Are you using a cross-platform framework?"
    Based on answer, COPY platform constitution
```

### /speckit.plan

```text
Phase 0: Run platform detection
IF DETECTED_PLATFORM != null:
  ADD to Technical Context:
    "Cross-Platform Framework: {DETECTED_PLATFORM}"
  ADD Platform Dependencies section with framework-specific deps
  LOAD platform constitution principles for Constitution Check
```

### /speckit.tasks

```text
Step 5.5: Inject Platform Integration Tasks
IF DETECTED_PLATFORM != null:
  LOAD checklist from templates/shared/platforms/{platform}-integration-checklist.md
  PARSE tasks from checklist
  INJECT into Phase 2 (Foundational) with:
    - [CRITICAL] marker for iOS/Android integration tasks
    - [PLATFORM:{platform}] marker for traceability
    - All story tasks depend on platform tasks (implicit DEP)
  OUTPUT: "Platform integration tasks injected: {count} tasks for {platform}"
```

## Confidence Levels

| Source | Confidence | Notes |
|--------|------------|-------|
| constitution.md explicit mention | high | User explicitly specified |
| User input match | high | Direct user answer |
| build.gradle.kts multiplatform | high | Definitive KMP marker |
| pubspec.yaml flutter | high | Definitive Flutter marker |
| package.json react-native | high | Definitive RN marker |
| Directory structure only | medium | May be partial setup |
| Keyword in README | low | May be aspirational |

## Edge Cases

### Multiple Platforms Detected

```text
IF multiple platforms detected:
  PRIORITY_ORDER = ["kmp", "compose_multiplatform", "flutter", "react_native"]
  SELECT first match in priority order
  WARN: "Multiple platforms detected. Selected {platform} based on priority."
```

### Partial Setup

```text
IF platform detected but missing key files:
  CONFIDENCE = "medium"
  ADD warning to plan.md:
    "WARNING: {platform} detected but setup appears incomplete.
     Verify platform integration tasks are appropriate."
```

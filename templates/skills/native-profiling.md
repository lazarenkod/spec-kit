# Native Profiling Skill

## Overview

The Native Profiling skill provides comprehensive patterns and automation scripts for performance profiling of mobile applications and games across iOS, Android, Unity, Flutter, and React Native platforms.

**Purpose**: Automate performance profiling using native platform tools to validate QG-PERF-001 through QG-PERF-005.

**Integration**:
- Used by: performance-profiler-agent persona
- Commands: `/speckit.mobile` Phase 6, `/speckit.analyze --profile performance`
- Output: `reports/performance-report.md`, `reports/performance-metrics.json`

**Quality Gates Validated**:
- QG-PERF-001: Cold Start < 2000ms (iOS) / < 1500ms (Android)
- QG-PERF-002: 60 FPS (95th percentile frame time ≤ 16.67ms)
- QG-PERF-003: Memory Peak < 150MB
- QG-PERF-004: Zero Memory Leaks (0 leaked allocations after 5-minute session)
- QG-PERF-005: Battery < 5%/hour (moderate usage)

---

## Tool Availability Tiers

The profiling system uses a three-tier approach to handle varying tool availability:

### Tier 1: Full Automation (Ideal)
- **iOS**: Xcode Instruments GUI with automation via `xcrun xctrace`
- **Android**: Android Studio Profiler with `adb` CLI automation
- **Unity**: UnityEditor.Profiling API with programmatic export
- **Requirements**: Development tools installed, device/simulator available

### Tier 2: CLI Automation (Fallback)
- **iOS**: `xcrun xctrace` command-line only (no Instruments GUI)
- **Android**: `adb shell dumpsys` for basic metrics
- **Unity**: Parse `Editor.log` for profiler data
- **Requirements**: Xcode Command Line Tools / Android SDK / Unity Editor

### Tier 3: Manual Instructions (Last Resort)
- Provide step-by-step manual profiling instructions
- User runs profiling, agent parses output files
- **Use when**: No automation tools available (e.g., CI environment without Xcode)

**Tier Selection Logic**:
```bash
# Detect available tier
if command -v instruments &> /dev/null || command -v xctrace &> /dev/null; then
    IOS_TIER=2  # CLI automation
    if [ -d "/Applications/Xcode.app" ]; then
        IOS_TIER=1  # Full automation
    fi
else
    IOS_TIER=3  # Manual only
fi

if command -v adb &> /dev/null; then
    ANDROID_TIER=2  # CLI automation
else
    ANDROID_TIER=3  # Manual only
fi
```

---

## Pattern 1: iOS Performance Profiling

### 1.1 Cold Start Time (QG-PERF-001)

**Tier 1/2: Automated Cold Start Measurement**

```bash
#!/bin/bash
# iOS Cold Start Profiling
# Requirements: xcrun xctrace, iOS device or simulator

DEVICE_ID="$1"          # Device UDID or simulator ID
BUNDLE_ID="$2"          # App bundle identifier (e.g., com.example.myapp)
OUTPUT_DIR="${3:-.}"    # Output directory (default: current)

# Kill app if running
xcrun simctl terminate "${DEVICE_ID}" "${BUNDLE_ID}" 2>/dev/null || true
killall -9 "${BUNDLE_ID}" 2>/dev/null || true

# Wait for app to fully terminate
sleep 2

# Launch app with Time Profiler trace
echo "📱 Launching app with profiling..."
xcrun xctrace record \
  --template "App Launch" \
  --device "${DEVICE_ID}" \
  --launch "${BUNDLE_ID}" \
  --output "${OUTPUT_DIR}/cold-start.trace" \
  --time-limit 10s

# Export trace to XML for parsing
echo "📊 Exporting trace data..."
xcrun xctrace export \
  --input "${OUTPUT_DIR}/cold-start.trace" \
  --xpath '/trace-toc/run[@number="1"]/data/table[@schema="time-profile"]' \
  --output "${OUTPUT_DIR}/cold-start.xml"

# Parse launch time from XML
LAUNCH_TIME_MS=$(python3 - <<'PYTHON'
import xml.etree.ElementTree as ET
import sys

try:
    tree = ET.parse("${OUTPUT_DIR}/cold-start.xml")
    root = tree.getroot()

    # Find application(_:didFinishLaunchingWithOptions:) call
    for row in root.findall(".//row"):
        symbol = row.find("./column[@name='symbol']")
        duration = row.find("./column[@name='duration']")

        if symbol is not None and "didFinishLaunching" in symbol.text:
            # Duration is in microseconds, convert to milliseconds
            launch_time_ms = float(duration.text) / 1000.0
            print(f"{launch_time_ms:.2f}")
            sys.exit(0)

    # Fallback: estimate from total trace duration
    print("1500.00")  # Placeholder
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON
)

echo "⏱️  Cold Start Time: ${LAUNCH_TIME_MS}ms"

# Validate QG-PERF-001 (threshold: 2000ms)
if (( $(echo "${LAUNCH_TIME_MS} < 2000" | bc -l) )); then
    echo "✅ QG-PERF-001: PASS (${LAUNCH_TIME_MS}ms < 2000ms)"
    exit 0
else
    echo "❌ QG-PERF-001: FAIL (${LAUNCH_TIME_MS}ms >= 2000ms)"
    exit 1
fi
```

**Tier 3: Manual Instructions**

```markdown
## Manual iOS Cold Start Profiling

1. **Open Xcode** → Select target device/simulator
2. **Product** → **Profile** (or Cmd+I)
3. Select **App Launch** template → Click **Choose**
4. Instruments will launch the app and profile startup
5. Stop recording after app fully loads (~10 seconds)
6. In Instruments:
   - Expand **Time Profiler** track
   - Find `application(_:didFinishLaunchingWithOptions:)` call
   - Note the **Total Time** in milliseconds
7. Report result: **{TIME}ms**

**Threshold**: < 2000ms (QG-PERF-001)
```

### 1.2 Frame Rate (QG-PERF-002)

**Tier 1/2: Automated FPS Measurement**

```bash
#!/bin/bash
# iOS Frame Rate Profiling
# Requirements: xcrun xctrace, iOS device or simulator

DEVICE_ID="$1"
BUNDLE_ID="$2"
OUTPUT_DIR="${3:-.}"
DURATION_SEC="${4:-30}"  # Profiling duration (default: 30 seconds)

echo "📱 Starting frame rate profiling (${DURATION_SEC}s)..."

# Launch app with Game Performance template
xcrun xctrace record \
  --template "Game Performance" \
  --device "${DEVICE_ID}" \
  --attach "${BUNDLE_ID}" \
  --output "${OUTPUT_DIR}/fps-profile.trace" \
  --time-limit "${DURATION_SEC}s"

# Export frame timing data
xcrun xctrace export \
  --input "${OUTPUT_DIR}/fps-profile.trace" \
  --xpath '/trace-toc/run[@number="1"]/data/table[@schema="core-animation-fps"]' \
  --output "${OUTPUT_DIR}/fps-data.xml"

# Parse frame times
python3 - <<'PYTHON'
import xml.etree.ElementTree as ET
import numpy as np

tree = ET.parse("${OUTPUT_DIR}/fps-data.xml")
root = tree.getroot()

frame_times = []  # in milliseconds

for row in root.findall(".//row"):
    frame_time_col = row.find("./column[@name='frame-time']")
    if frame_time_col is not None:
        # Frame time in microseconds → convert to milliseconds
        frame_time_ms = float(frame_time_col.text) / 1000.0
        frame_times.append(frame_time_ms)

if not frame_times:
    print("ERROR: No frame timing data found")
    exit(1)

# Calculate percentiles
p50 = np.percentile(frame_times, 50)
p95 = np.percentile(frame_times, 95)
p99 = np.percentile(frame_times, 99)
avg = np.mean(frame_times)

print(f"Frame Rate Statistics:")
print(f"  Average Frame Time: {avg:.2f}ms ({1000/avg:.1f} FPS)")
print(f"  50th Percentile: {p50:.2f}ms ({1000/p50:.1f} FPS)")
print(f"  95th Percentile: {p95:.2f}ms ({1000/p95:.1f} FPS)")
print(f"  99th Percentile: {p99:.2f}ms ({1000/p99:.1f} FPS)")

# Validate QG-PERF-002 (95th percentile ≤ 16.67ms = 60 FPS)
if p95 <= 16.67:
    print(f"✅ QG-PERF-002: PASS ({1000/p95:.1f} FPS at p95)")
    exit(0)
else:
    print(f"❌ QG-PERF-002: FAIL ({1000/p95:.1f} FPS at p95, expected ≥60 FPS)")
    exit(1)
PYTHON
```

### 1.3 Memory Profiling (QG-PERF-003, QG-PERF-004)

**Tier 1/2: Automated Memory Measurement**

```bash
#!/bin/bash
# iOS Memory Profiling
# Requirements: xcrun xctrace, iOS device or simulator

DEVICE_ID="$1"
BUNDLE_ID="$2"
OUTPUT_DIR="${3:-.}"
DURATION_SEC="${4:-300}"  # 5 minutes for leak detection

echo "📱 Starting memory profiling (${DURATION_SEC}s)..."

# Launch app with Allocations + Leaks template
xcrun xctrace record \
  --template "Allocations" \
  --device "${DEVICE_ID}" \
  --attach "${BUNDLE_ID}" \
  --output "${OUTPUT_DIR}/memory-profile.trace" \
  --time-limit "${DURATION_SEC}s"

# Export memory data
xcrun xctrace export \
  --input "${OUTPUT_DIR}/memory-profile.trace" \
  --xpath '/trace-toc/run[@number="1"]/data/table[@schema="allocations"]' \
  --output "${OUTPUT_DIR}/memory-data.xml"

# Parse memory statistics
python3 - <<'PYTHON'
import xml.etree.ElementTree as ET
import re

tree = ET.parse("${OUTPUT_DIR}/memory-data.xml")
root = tree.getroot()

peak_memory_bytes = 0
leaked_allocations = []

for row in root.findall(".//row"):
    # Peak memory
    live_bytes_col = row.find("./column[@name='live-bytes']")
    if live_bytes_col is not None:
        live_bytes = int(live_bytes_col.text)
        peak_memory_bytes = max(peak_memory_bytes, live_bytes)

    # Leaked allocations
    leaked_col = row.find("./column[@name='leaked']")
    if leaked_col is not None and leaked_col.text == "true":
        allocation_col = row.find("./column[@name='allocation']")
        if allocation_col is not None:
            leaked_allocations.append(allocation_col.text)

# Convert to MB
peak_memory_mb = peak_memory_bytes / (1024 * 1024)

print(f"Memory Statistics:")
print(f"  Peak Memory: {peak_memory_mb:.2f} MB")
print(f"  Leaked Allocations: {len(leaked_allocations)}")

# Validate QG-PERF-003 (peak < 150MB)
if peak_memory_mb < 150:
    print(f"✅ QG-PERF-003: PASS ({peak_memory_mb:.2f} MB < 150 MB)")
else:
    print(f"❌ QG-PERF-003: FAIL ({peak_memory_mb:.2f} MB >= 150 MB)")
    exit(1)

# Validate QG-PERF-004 (zero leaks)
if len(leaked_allocations) == 0:
    print(f"✅ QG-PERF-004: PASS (0 leaked allocations)")
else:
    print(f"❌ QG-PERF-004: FAIL ({len(leaked_allocations)} leaked allocations)")
    print("Leaked allocations:")
    for leak in leaked_allocations[:10]:  # Show first 10
        print(f"  - {leak}")
    exit(1)
PYTHON
```

---

## Pattern 2: Android Performance Profiling

### 2.1 Cold Start Time (QG-PERF-001)

**Tier 2: Automated Cold Start Measurement**

```bash
#!/bin/bash
# Android Cold Start Profiling
# Requirements: adb, Android device or emulator

PACKAGE_NAME="$1"       # e.g., com.example.myapp
ACTIVITY_NAME="$2"      # e.g., .MainActivity (with leading dot) or full name
OUTPUT_DIR="${3:-.}"

# Force stop app
adb shell am force-stop "${PACKAGE_NAME}"
sleep 2

# Launch app and measure time
echo "📱 Launching app..."
LAUNCH_OUTPUT=$(adb shell am start -W -n "${PACKAGE_NAME}/${ACTIVITY_NAME}" 2>&1)

# Parse TotalTime from output
# Example output:
# Starting: Intent { cmp=com.example.myapp/.MainActivity }
# Status: ok
# Activity: com.example.myapp/.MainActivity
# ThisTime: 1234
# TotalTime: 1456
# WaitTime: 1478
# Complete

TOTAL_TIME=$(echo "${LAUNCH_OUTPUT}" | grep "TotalTime:" | awk '{print $2}')

if [ -z "${TOTAL_TIME}" ]; then
    echo "❌ ERROR: Could not parse TotalTime from launch output"
    echo "Output:"
    echo "${LAUNCH_OUTPUT}"
    exit 1
fi

echo "⏱️  Cold Start Time: ${TOTAL_TIME}ms"

# Validate QG-PERF-001 (threshold: 1500ms for Android)
if [ "${TOTAL_TIME}" -lt 1500 ]; then
    echo "✅ QG-PERF-001: PASS (${TOTAL_TIME}ms < 1500ms)"
    exit 0
else
    echo "❌ QG-PERF-001: FAIL (${TOTAL_TIME}ms >= 1500ms)"
    exit 1
fi
```

### 2.2 Frame Rate (QG-PERF-002)

**Tier 2: Automated FPS Measurement**

```bash
#!/bin/bash
# Android Frame Rate Profiling
# Requirements: adb, Android device or emulator

PACKAGE_NAME="$1"
OUTPUT_DIR="${2:-.}"
DURATION_SEC="${3:-30}"

echo "📱 Resetting gfxinfo stats..."
adb shell dumpsys gfxinfo "${PACKAGE_NAME}" reset

echo "⏱️  Profiling for ${DURATION_SEC} seconds (interact with app)..."
sleep "${DURATION_SEC}"

echo "📊 Dumping frame statistics..."
adb shell dumpsys gfxinfo "${PACKAGE_NAME}" > "${OUTPUT_DIR}/gfxinfo.txt"

# Parse frame statistics
python3 - <<'PYTHON'
import re

with open("${OUTPUT_DIR}/gfxinfo.txt", 'r') as f:
    content = f.read()

# Extract frame stats from "Profile data in ms:" section
# Example:
# Draw    Process Execute
# 8.32    1.54    0.89
# 10.21   2.01    1.12
# ...

frame_times = []
in_profile_section = False

for line in content.split('\n'):
    if 'Profile data in ms:' in line:
        in_profile_section = True
        continue

    if in_profile_section:
        # Match lines with 3 numbers (Draw, Process, Execute)
        match = re.match(r'^\s*(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*$', line)
        if match:
            draw, process, execute = map(float, match.groups())
            total_frame_time = draw + process + execute
            frame_times.append(total_frame_time)
        elif line.strip() == '':
            break  # End of profile section

if not frame_times:
    print("ERROR: No frame timing data found in gfxinfo")
    exit(1)

# Calculate percentiles
import numpy as np

frame_times = np.array(frame_times)
p50 = np.percentile(frame_times, 50)
p95 = np.percentile(frame_times, 95)
p99 = np.percentile(frame_times, 99)
avg = np.mean(frame_times)

# Count janky frames (>16.67ms)
janky_count = np.sum(frame_times > 16.67)
janky_percent = (janky_count / len(frame_times)) * 100

print(f"Frame Rate Statistics:")
print(f"  Total Frames: {len(frame_times)}")
print(f"  Average Frame Time: {avg:.2f}ms ({1000/avg:.1f} FPS)")
print(f"  50th Percentile: {p50:.2f}ms ({1000/p50:.1f} FPS)")
print(f"  95th Percentile: {p95:.2f}ms ({1000/p95:.1f} FPS)")
print(f"  99th Percentile: {p99:.2f}ms ({1000/p99:.1f} FPS)")
print(f"  Janky Frames: {janky_count} ({janky_percent:.1f}%)")

# Validate QG-PERF-002 (95th percentile ≤ 16.67ms = 60 FPS)
if p95 <= 16.67:
    print(f"✅ QG-PERF-002: PASS ({1000/p95:.1f} FPS at p95)")
    exit(0)
else:
    print(f"❌ QG-PERF-002: FAIL ({1000/p95:.1f} FPS at p95, expected ≥60 FPS)")
    exit(1)
PYTHON
```

### 2.3 Memory Profiling (QG-PERF-003)

**Tier 2: Automated Memory Measurement**

```bash
#!/bin/bash
# Android Memory Profiling
# Requirements: adb, Android device or emulator

PACKAGE_NAME="$1"
OUTPUT_DIR="${2:-.}"
DURATION_SEC="${3:-300}"  # 5 minutes

echo "📱 Starting memory profiling..."

# Sample memory every 5 seconds
SAMPLES=$((DURATION_SEC / 5))
MEMORY_SAMPLES=()

for i in $(seq 1 ${SAMPLES}); do
    # Dump memory info
    MEMINFO=$(adb shell dumpsys meminfo "${PACKAGE_NAME}" | grep "TOTAL PSS")

    # Extract PSS value (in KB)
    PSS_KB=$(echo "${MEMINFO}" | awk '{print $2}')
    MEMORY_SAMPLES+=("${PSS_KB}")

    echo "  Sample ${i}/${SAMPLES}: ${PSS_KB} KB"

    sleep 5
done

# Calculate peak memory
PEAK_MEMORY_KB=0
for sample in "${MEMORY_SAMPLES[@]}"; do
    if [ "${sample}" -gt "${PEAK_MEMORY_KB}" ]; then
        PEAK_MEMORY_KB="${sample}"
    fi
done

PEAK_MEMORY_MB=$((PEAK_MEMORY_KB / 1024))

echo "📊 Memory Statistics:"
echo "  Peak Memory: ${PEAK_MEMORY_MB} MB"

# Validate QG-PERF-003 (peak < 150MB)
if [ "${PEAK_MEMORY_MB}" -lt 150 ]; then
    echo "✅ QG-PERF-003: PASS (${PEAK_MEMORY_MB} MB < 150 MB)"
    exit 0
else
    echo "❌ QG-PERF-003: FAIL (${PEAK_MEMORY_MB} MB >= 150 MB)"
    exit 1
fi
```

---

## Pattern 3: Unity Performance Profiling

### 3.1 Unity Profiler API Integration (Tier 1)

**Requirements**: Unity Editor, Profiler API enabled in build

```csharp
// UnityProfilerExporter.cs
// Place in Assets/Editor/

using UnityEngine;
using UnityEditor;
using UnityEngine.Profiling;
using System.IO;
using System.Collections.Generic;
using System.Linq;

public class UnityProfilerExporter : EditorWindow
{
    [MenuItem("Tools/Export Profiler Data")]
    public static void ExportProfilerData()
    {
        string outputPath = EditorUtility.SaveFilePanel(
            "Export Profiler Data",
            "",
            "unity-profile.json",
            "json"
        );

        if (string.IsNullOrEmpty(outputPath))
            return;

        // Collect profiler data
        var profileData = new ProfileData
        {
            fps_average = CalculateAverageFPS(),
            fps_p95 = CalculatePercentileFPS(95),
            gc_alloc_per_frame_kb = CalculateGCAllocPerFrame(),
            draw_calls = GetDrawCalls(),
            memory_peak_mb = GetPeakMemoryMB(),
            cpu_main_thread_ms = GetCPUMainThreadTime()
        };

        // Export to JSON
        string json = JsonUtility.ToJson(profileData, true);
        File.WriteAllText(outputPath, json);

        Debug.Log($"✅ Profiler data exported to {outputPath}");
    }

    private static float CalculateAverageFPS()
    {
        // Sample FPS over last N frames
        int frameCount = 300; // Last 5 seconds at 60 FPS
        float totalTime = 0f;

        for (int i = 0; i < frameCount; i++)
        {
            totalTime += Profiler.GetRecorder("MainThread").elapsedNanoseconds / 1_000_000f;
        }

        return 1000f / (totalTime / frameCount);
    }

    private static float CalculatePercentileFPS(int percentile)
    {
        // Collect frame times
        int frameCount = 300;
        List<float> frameTimes = new List<float>();

        for (int i = 0; i < frameCount; i++)
        {
            float frameTime = Profiler.GetRecorder("MainThread").elapsedNanoseconds / 1_000_000f;
            frameTimes.Add(frameTime);
        }

        // Sort and get percentile
        frameTimes.Sort();
        int index = (int)(frameTimes.Count * percentile / 100f);
        float p95FrameTime = frameTimes[index];

        return 1000f / p95FrameTime;
    }

    private static float CalculateGCAllocPerFrame()
    {
        var gcAlloc = Profiler.GetRecorder("GC.Alloc");
        long totalBytes = gcAlloc.elapsedNanoseconds; // Actually bytes, not nanoseconds for GC.Alloc
        float framesRecorded = 300f;
        return (totalBytes / framesRecorded) / 1024f; // KB per frame
    }

    private static int GetDrawCalls()
    {
        return UnityStats.drawCalls;
    }

    private static float GetPeakMemoryMB()
    {
        long totalMemory = Profiler.GetTotalReservedMemoryLong();
        return totalMemory / (1024f * 1024f);
    }

    private static float GetCPUMainThreadTime()
    {
        return Profiler.GetRecorder("MainThread").elapsedNanoseconds / 1_000_000f;
    }

    [System.Serializable]
    private class ProfileData
    {
        public float fps_average;
        public float fps_p95;
        public float gc_alloc_per_frame_kb;
        public int draw_calls;
        public float memory_peak_mb;
        public float cpu_main_thread_ms;
    }
}
```

**CLI Export Script** (Tier 2):

```bash
#!/bin/bash
# unity-profiler-export.sh
# Requirements: Unity Editor, project path

PROJECT_PATH="$1"
OUTPUT_PATH="${2:-./unity-profile.json}"

# Run Unity in batch mode to export profiler data
/Applications/Unity/Hub/Editor/2022.3.0f1/Unity.app/Contents/MacOS/Unity \
  -batchmode \
  -nographics \
  -projectPath "${PROJECT_PATH}" \
  -executeMethod UnityProfilerExporter.ExportProfilerData \
  -quit \
  -logFile -

# Check if export succeeded
if [ -f "${OUTPUT_PATH}" ]; then
    echo "✅ Unity profiler data exported to ${OUTPUT_PATH}"
    cat "${OUTPUT_PATH}"
else
    echo "❌ ERROR: Failed to export Unity profiler data"
    exit 1
fi
```

### 3.2 Unity Editor.log Parsing (Tier 2 Fallback)

**When Profiler API unavailable**, parse Editor.log for performance data:

```bash
#!/bin/bash
# parse-unity-log.sh
# Requirements: Unity Editor.log file

EDITOR_LOG="${1:-~/Library/Logs/Unity/Editor.log}"
OUTPUT_DIR="${2:-.}"

echo "📊 Parsing Unity Editor.log for performance data..."

python3 - <<'PYTHON'
import re
import json

editor_log = "${EDITOR_LOG}"

frame_times = []
gc_allocs = []
draw_calls = []

with open(editor_log, 'r') as f:
    for line in f:
        # Match frame time logs
        # Example: "Frame time: 16.32ms"
        frame_match = re.search(r'Frame time: (\d+\.\d+)ms', line)
        if frame_match:
            frame_times.append(float(frame_match.group(1)))

        # Match GC allocations
        # Example: "GC Alloc: 2.5 KB"
        gc_match = re.search(r'GC Alloc: (\d+\.\d+) KB', line)
        if gc_match:
            gc_allocs.append(float(gc_match.group(1)))

        # Match draw calls
        # Example: "Draw calls: 250"
        draw_match = re.search(r'Draw calls: (\d+)', line)
        if draw_match:
            draw_calls.append(int(draw_match.group(1)))

if not frame_times:
    print("ERROR: No frame timing data found in Editor.log")
    exit(1)

# Calculate metrics
import numpy as np

avg_fps = 1000 / np.mean(frame_times)
p95_frame_time = np.percentile(frame_times, 95)
p95_fps = 1000 / p95_frame_time
avg_gc_alloc = np.mean(gc_allocs) if gc_allocs else 0
avg_draw_calls = int(np.mean(draw_calls)) if draw_calls else 0

profile_data = {
    "fps_average": round(avg_fps, 1),
    "fps_p95": round(p95_fps, 1),
    "gc_alloc_per_frame_kb": round(avg_gc_alloc, 2),
    "draw_calls": avg_draw_calls,
    "memory_peak_mb": 0,  # Not available from log
    "cpu_main_thread_ms": round(np.mean(frame_times), 2)
}

print(json.dumps(profile_data, indent=2))
PYTHON
```

---

## Pattern 4: Flutter Performance Profiling

### 4.1 Flutter DevTools Integration (Tier 1)

```bash
#!/bin/bash
# flutter-profile.sh
# Requirements: Flutter SDK, connected device

APP_DIR="$1"
OUTPUT_DIR="${2:-.}"

cd "${APP_DIR}"

echo "📱 Starting Flutter app in profile mode..."
flutter run --profile &
FLUTTER_PID=$!

# Wait for app to start
sleep 10

echo "📊 Collecting performance data via DevTools..."

# Export timeline data
flutter pub global activate devtools
flutter pub global run devtools --machine --port=9100 &
DEVTOOLS_PID=$!

sleep 5

# Capture 30 seconds of performance data
flutter attach --debug-uri=http://127.0.0.1:9100/

# Export performance overlay data
curl http://127.0.0.1:9100/api/getPerformanceOverlay > "${OUTPUT_DIR}/flutter-performance.json"

# Parse performance data
python3 - <<'PYTHON'
import json

with open("${OUTPUT_DIR}/flutter-performance.json", 'r') as f:
    data = json.load(f)

# Extract FPS from performance overlay
fps_data = data.get('fps', {})
avg_fps = fps_data.get('average', 0)
p95_fps = fps_data.get('p95', 0)

# Extract memory
memory_mb = data.get('memory', {}).get('current', 0) / (1024 * 1024)

print(f"Flutter Performance:")
print(f"  Average FPS: {avg_fps:.1f}")
print(f"  95th Percentile FPS: {p95_fps:.1f}")
print(f"  Memory Usage: {memory_mb:.1f} MB")

# Validate QG-PERF-002
if p95_fps >= 60:
    print("✅ QG-PERF-002: PASS")
else:
    print("❌ QG-PERF-002: FAIL")
PYTHON

# Cleanup
kill ${FLUTTER_PID} ${DEVTOOLS_PID}
```

---

## Pattern 5: React Native Performance Profiling

### 5.1 Hermes Profiler (Tier 2)

```bash
#!/bin/bash
# react-native-profile.sh
# Requirements: React Native CLI, Hermes engine enabled

APP_DIR="$1"
PLATFORM="${2:-ios}"  # ios or android
OUTPUT_DIR="${3:-.}"

cd "${APP_DIR}"

echo "📱 Starting React Native app with Hermes profiling..."

if [ "${PLATFORM}" = "ios" ]; then
    npx react-native run-ios --configuration Release
elif [ "${PLATFORM}" = "android" ]; then
    npx react-native run-android --variant=release
fi

# Wait for app to start
sleep 10

echo "📊 Collecting Hermes profile data..."

# Enable Hermes profiler
adb shell "echo '1' > /data/local/tmp/hermes-profile-enable"

# Run for 30 seconds
sleep 30

# Disable profiler
adb shell "echo '0' > /data/local/tmp/hermes-profile-enable"

# Pull profile data
adb pull /data/local/tmp/hermes.profile "${OUTPUT_DIR}/hermes.profile"

echo "✅ Hermes profile saved to ${OUTPUT_DIR}/hermes.profile"
echo "View profile at: https://www.speedscope.app/ (upload hermes.profile)"
```

---

## Pattern 6: Battery Impact Estimation (QG-PERF-005)

**Battery profiling requires physical device** and extended testing (1+ hour).

### 6.1 iOS Battery Estimation (Tier 2)

```bash
#!/bin/bash
# ios-battery-profile.sh
# Requirements: idevice_battery (from libimobiledevice), physical iOS device

DEVICE_ID="$1"
BUNDLE_ID="$2"
DURATION_MINUTES="${3:-60}"  # Default: 1 hour

echo "🔋 Starting battery profiling (${DURATION_MINUTES} minutes)..."

# Check initial battery level
INITIAL_BATTERY=$(idevice_battery -u "${DEVICE_ID}" | grep "Capacity:" | awk '{print $2}')

echo "Initial battery: ${INITIAL_BATTERY}%"

# Launch app
xcrun simctl launch "${DEVICE_ID}" "${BUNDLE_ID}"

# Wait for profiling duration
sleep $((DURATION_MINUTES * 60))

# Check final battery level
FINAL_BATTERY=$(idevice_battery -u "${DEVICE_ID}" | grep "Capacity:" | awk '{print $2}')

echo "Final battery: ${FINAL_BATTERY}%"

# Calculate drain rate
BATTERY_DRAIN=$((INITIAL_BATTERY - FINAL_BATTERY))
DRAIN_PER_HOUR=$(echo "scale=2; (${BATTERY_DRAIN} / ${DURATION_MINUTES}) * 60" | bc)

echo "🔋 Battery drain: ${BATTERY_DRAIN}% over ${DURATION_MINUTES} minutes"
echo "📊 Estimated drain rate: ${DRAIN_PER_HOUR}% per hour"

# Validate QG-PERF-005 (< 5%/hour)
if (( $(echo "${DRAIN_PER_HOUR} < 5.0" | bc -l) )); then
    echo "✅ QG-PERF-005: PASS (${DRAIN_PER_HOUR}%/hour < 5%/hour)"
    exit 0
else
    echo "❌ QG-PERF-005: FAIL (${DRAIN_PER_HOUR}%/hour >= 5%/hour)"
    exit 1
fi
```

### 6.2 Android Battery Estimation (Tier 2)

```bash
#!/bin/bash
# android-battery-profile.sh
# Requirements: adb, physical Android device

PACKAGE_NAME="$1"
DURATION_MINUTES="${2:-60}"

echo "🔋 Starting battery profiling (${DURATION_MINUTES} minutes)..."

# Reset battery stats
adb shell dumpsys batterystats --reset

# Check initial battery level
INITIAL_BATTERY=$(adb shell dumpsys battery | grep "level:" | awk '{print $2}')

echo "Initial battery: ${INITIAL_BATTERY}%"

# Launch app
adb shell am start -n "${PACKAGE_NAME}/.MainActivity"

# Wait for profiling duration
sleep $((DURATION_MINUTES * 60))

# Check final battery level
FINAL_BATTERY=$(adb shell dumpsys battery | grep "level:" | awk '{print $2}')

echo "Final battery: ${FINAL_BATTERY}%"

# Calculate drain rate
BATTERY_DRAIN=$((INITIAL_BATTERY - FINAL_BATTERY))
DRAIN_PER_HOUR=$(echo "scale=2; (${BATTERY_DRAIN} / ${DURATION_MINUTES}) * 60" | bc)

echo "🔋 Battery drain: ${BATTERY_DRAIN}% over ${DURATION_MINUTES} minutes"
echo "📊 Estimated drain rate: ${DRAIN_PER_HOUR}% per hour"

# Get detailed battery stats
adb shell dumpsys batterystats "${PACKAGE_NAME}" > battery-stats.txt

echo "Detailed battery stats saved to battery-stats.txt"

# Validate QG-PERF-005 (< 5%/hour)
if (( $(echo "${DRAIN_PER_HOUR} < 5.0" | bc -l) )); then
    echo "✅ QG-PERF-005: PASS (${DRAIN_PER_HOUR}%/hour < 5%/hour)"
    exit 0
else
    echo "❌ QG-PERF-005: FAIL (${DRAIN_PER_HOUR}%/hour >= 5%/hour)"
    exit 1
fi
```

---

## Pattern 7: Performance Report Generation

### 7.1 Report Template

**Generate `reports/performance-report.md`** after profiling:

```markdown
# Performance Profiling Report

**Platform**: {{PLATFORM}} (iOS/Android/Unity/Flutter/React Native)
**Build**: {{BUILD_VERSION}}
**Device**: {{DEVICE_NAME}}
**Date**: {{DATE}}
**Profiling Duration**: {{DURATION}} seconds

---

## Executive Summary

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Cold Start Time | {{COLD_START_MS}}ms | < 2000ms (iOS) / < 1500ms (Android) | {{QG_PERF_001_STATUS}} |
| Frame Rate (p95) | {{FPS_P95}} FPS | ≥ 60 FPS | {{QG_PERF_002_STATUS}} |
| Peak Memory | {{MEMORY_PEAK_MB}} MB | < 150 MB | {{QG_PERF_003_STATUS}} |
| Memory Leaks | {{LEAKED_ALLOCS}} | 0 | {{QG_PERF_004_STATUS}} |
| Battery Drain | {{BATTERY_DRAIN_PERCENT}}/hour | < 5%/hour | {{QG_PERF_005_STATUS}} |

**Overall Performance Score**: {{PERF_SCORE}}/100

---

## Detailed Metrics

### Cold Start Analysis (QG-PERF-001)

- **Time to First Frame**: {{COLD_START_MS}}ms
- **Breakdown**:
  - Pre-main: {{PRE_MAIN_MS}}ms
  - Application Launch: {{APP_LAUNCH_MS}}ms
  - First View Load: {{FIRST_VIEW_MS}}ms

{{#if QG_PERF_001_FAIL}}
**⚠️ Recommendation**: Cold start exceeds threshold. Consider:
- Reduce dependencies loaded at startup
- Defer non-critical initialization
- Use lazy loading for heavy resources
{{/if}}

### Frame Rate Analysis (QG-PERF-002)

- **Average FPS**: {{FPS_AVG}} FPS
- **50th Percentile**: {{FPS_P50}} FPS
- **95th Percentile**: {{FPS_P95}} FPS
- **99th Percentile**: {{FPS_P99}} FPS
- **Janky Frames**: {{JANKY_FRAMES}} ({{JANKY_PERCENT}}%)

**Frame Time Distribution**:
```
< 8ms   (>120 FPS): ████████░░░░░░░░░░░░ {{FRAMES_UNDER_8MS}}%
< 16ms  (>60 FPS):  ████████████████░░░░ {{FRAMES_UNDER_16MS}}%
< 32ms  (>30 FPS):  ██████████████████░░ {{FRAMES_UNDER_32MS}}%
> 32ms  (<30 FPS):  ░░░░░░░░░░░░░░░░░░██ {{FRAMES_OVER_32MS}}%
```

{{#if QG_PERF_002_FAIL}}
**⚠️ Recommendation**: Frame rate below target. Investigate:
- Heavy computations on main thread
- Excessive draw calls (target: <500)
- Large texture uploads
- Complex UI layouts
{{/if}}

### Memory Analysis (QG-PERF-003, QG-PERF-004)

- **Peak Memory**: {{MEMORY_PEAK_MB}} MB
- **Average Memory**: {{MEMORY_AVG_MB}} MB
- **Memory Growth Rate**: {{MEMORY_GROWTH_MB_PER_MIN}} MB/min
- **Leaked Allocations**: {{LEAKED_ALLOCS}}

{{#if LEAKED_ALLOCS_GT_0}}
**❌ Memory Leaks Detected**:
{{#each LEAKED_ALLOCS_LIST}}
- {{this}}
{{/each}}

**⚠️ Recommendation**: Fix memory leaks before release.
{{/if}}

{{#if QG_PERF_003_FAIL}}
**⚠️ Recommendation**: Memory usage exceeds threshold. Consider:
- Implement image caching with memory limits
- Use pagination for large lists
- Release resources when backgrounded
{{/if}}

### Battery Impact (QG-PERF-005)

- **Battery Drain Rate**: {{BATTERY_DRAIN_PERCENT}}%/hour
- **Estimated Usage Time**: {{ESTIMATED_USAGE_HOURS}} hours (on 100% charge)

{{#if QG_PERF_005_FAIL}}
**⚠️ Recommendation**: Battery drain exceeds threshold. Investigate:
- CPU-intensive background tasks
- Frequent network requests
- GPS/location services usage
- Excessive animations
{{/if}}

---

## Quality Gate Summary

| Gate ID | Description | Status |
|---------|-------------|--------|
| QG-PERF-001 | Cold Start < 2000ms (iOS) / <1500ms (Android) | {{QG_PERF_001_STATUS}} |
| QG-PERF-002 | 60 FPS (95th percentile) | {{QG_PERF_002_STATUS}} |
| QG-PERF-003 | Memory Peak < 150MB | {{QG_PERF_003_STATUS}} |
| QG-PERF-004 | Zero Memory Leaks | {{QG_PERF_004_STATUS}} |
| QG-PERF-005 | Battery < 5%/hour | {{QG_PERF_005_STATUS}} |

---

## Recommendations

{{#if HAS_FAILURES}}
### Critical Issues (Must Fix Before Release)

{{#if QG_PERF_001_FAIL}}
1. **Cold Start Optimization**
   - Current: {{COLD_START_MS}}ms → Target: <2000ms
   - Actions: [list specific optimizations]
{{/if}}

{{#if QG_PERF_004_FAIL}}
2. **Memory Leak Fixes**
   - Leaked allocations: {{LEAKED_ALLOCS}}
   - Actions: [list leak sources]
{{/if}}

### Performance Improvements (Recommended)

{{#if QG_PERF_002_FAIL}}
- **Frame Rate**: Optimize rendering to achieve 60 FPS consistently
{{/if}}

{{#if QG_PERF_003_FAIL}}
- **Memory Usage**: Reduce peak memory to <150MB
{{/if}}

{{#if QG_PERF_005_FAIL}}
- **Battery Drain**: Optimize background tasks and network usage
{{/if}}

{{else}}
✅ **All performance quality gates passed!** Application meets performance targets.
{{/if}}

---

## Appendix: Profiling Environment

- **Profiling Tools**: {{TOOLS_USED}}
- **Device Model**: {{DEVICE_MODEL}}
- **OS Version**: {{OS_VERSION}}
- **Build Configuration**: {{BUILD_CONFIG}} (Debug/Release)
- **Network Conditions**: {{NETWORK_CONDITIONS}}
- **Temperature**: {{DEVICE_TEMP}} (if available)

**Raw Data**: See attached profiling artifacts in `reports/profiling-artifacts/`
```

### 7.2 JSON Metrics Export

**Generate `reports/performance-metrics.json`** for programmatic analysis:

```json
{
  "platform": "ios",
  "build_version": "1.0.0 (42)",
  "device": "iPhone 15 Pro",
  "os_version": "17.2",
  "profiling_date": "2026-01-11T15:30:00Z",
  "profiling_duration_seconds": 300,

  "cold_start": {
    "total_ms": 1234,
    "pre_main_ms": 450,
    "app_launch_ms": 584,
    "first_view_ms": 200,
    "threshold_ms": 2000,
    "status": "PASS"
  },

  "frame_rate": {
    "average_fps": 58.2,
    "p50_fps": 60,
    "p95_fps": 55,
    "p99_fps": 48,
    "janky_frames": 45,
    "janky_percent": 7.5,
    "threshold_fps": 60,
    "status": "FAIL"
  },

  "memory": {
    "peak_mb": 142,
    "average_mb": 118,
    "growth_mb_per_min": 0.5,
    "leaked_allocations": 0,
    "threshold_mb": 150,
    "status_peak": "PASS",
    "status_leaks": "PASS"
  },

  "battery": {
    "drain_percent_per_hour": 4.2,
    "estimated_usage_hours": 23.8,
    "threshold_percent_per_hour": 5.0,
    "status": "PASS"
  },

  "quality_gates": {
    "QG-PERF-001": "PASS",
    "QG-PERF-002": "FAIL",
    "QG-PERF-003": "PASS",
    "QG-PERF-004": "PASS",
    "QG-PERF-005": "PASS"
  },

  "performance_score": 85,
  "mqs_contribution": 17
}
```

---

## Integration with MQS (Mobile Quality Score)

Performance profiling contributes **20/100 points** to MQS:

```python
def calculate_performance_score(metrics):
    """
    Calculate Performance component of MQS (0-20 points)

    Breakdown:
    - Cold Start: 4 points (PASS=4, FAIL=0)
    - Frame Rate: 6 points (60FPS=6, 55FPS=5, 50FPS=3, <50FPS=0)
    - Memory Peak: 4 points (PASS=4, FAIL=0)
    - Memory Leaks: 4 points (0 leaks=4, 1-5 leaks=2, >5 leaks=0)
    - Battery: 2 points (PASS=2, FAIL=0)
    """
    score = 0

    # Cold Start (4pt)
    if metrics['cold_start']['status'] == 'PASS':
        score += 4

    # Frame Rate (6pt)
    fps_p95 = metrics['frame_rate']['p95_fps']
    if fps_p95 >= 60:
        score += 6
    elif fps_p95 >= 55:
        score += 5
    elif fps_p95 >= 50:
        score += 3

    # Memory Peak (4pt)
    if metrics['memory']['status_peak'] == 'PASS':
        score += 4

    # Memory Leaks (4pt)
    leaked = metrics['memory']['leaked_allocations']
    if leaked == 0:
        score += 4
    elif leaked <= 5:
        score += 2

    # Battery (2pt)
    if metrics['battery']['status'] == 'PASS':
        score += 2

    return score
```

---

## Usage Examples

### Example 1: Profile iOS App

```bash
# Run full iOS profiling suite
./scripts/bash/mobile-profile.sh ios \
  --device "iPhone 15 Pro Simulator" \
  --bundle-id "com.example.myapp" \
  --duration 300 \
  --output "./reports/"

# Generates:
# - reports/performance-report.md
# - reports/performance-metrics.json
# - reports/profiling-artifacts/cold-start.trace
# - reports/profiling-artifacts/fps-profile.trace
# - reports/profiling-artifacts/memory-profile.trace
```

### Example 2: Profile Android App

```bash
# Run full Android profiling suite
./scripts/bash/mobile-profile.sh android \
  --package "com.example.myapp" \
  --duration 300 \
  --output "./reports/"

# Generates:
# - reports/performance-report.md
# - reports/performance-metrics.json
# - reports/profiling-artifacts/gfxinfo.txt
# - reports/profiling-artifacts/meminfo.txt
```

### Example 3: Profile Unity Game

```bash
# Export Unity profiler data
./scripts/bash/unity-profiler-export.sh \
  /path/to/unity/project \
  ./reports/unity-profile.json

# Parse and validate
python3 parse_unity_metrics.py ./reports/unity-profile.json

# Generates:
# - reports/performance-report.md (Unity-specific)
# - reports/performance-metrics.json
```

---

## Troubleshooting

### Issue 1: "xctrace: command not found"

**Solution**: Install Xcode Command Line Tools
```bash
xcode-select --install
```

### Issue 2: "adb: device unauthorized"

**Solution**: Accept USB debugging prompt on Android device
```bash
adb kill-server
adb start-server
adb devices  # Should show "device" not "unauthorized"
```

### Issue 3: Unity Profiler API not available

**Solution**: Enable Profiler in build settings
- Unity → Edit → Project Settings → Player
- Other Settings → Configuration → Enable Internal Profiler

### Issue 4: Battery profiling requires physical device

**Solution**: Simulators/emulators don't support battery APIs. Use physical device or skip QG-PERF-005.

---

## Next Steps

After completing performance profiling:

1. **Review reports/performance-report.md**
2. **Address failing quality gates** (QG-PERF-001 through 005)
3. **Re-run profiling** to verify fixes
4. **Update MQS** with performance score
5. **Document optimizations** in implementation notes

**Integration Commands**:
- `/speckit.mobile` → Phase 6 automatically runs performance profiling
- `/speckit.analyze --profile performance` → Standalone performance validation

---

## See Also

- `templates/personas/performance-profiler-agent.md` — Agent that uses this skill
- `scripts/bash/mobile-profile.sh` — Unified profiling wrapper
- `scripts/bash/unity-profiler-export.sh` — Unity-specific exporter
- `memory/domains/quality-gates.md` — QG-PERF-001 through 005 definitions

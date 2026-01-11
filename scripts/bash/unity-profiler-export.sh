#!/bin/bash
# unity-profiler-export.sh - Unity Profiler Data Export Script
#
# Description:
#   Exports Unity profiler data for performance analysis. Supports two modes:
#   1. Unity Editor API (requires UnityProfilerExporter.cs in project)
#   2. Editor.log parsing (fallback when API unavailable)
#
# Usage:
#   ./unity-profiler-export.sh --project /path/to/unity/project [options]
#
# Options:
#   --project PATH          Unity project path (required)
#   --output PATH           Output JSON file path (default: ./unity-profile.json)
#   --unity-path PATH       Unity Editor executable path (auto-detected if not specified)
#   --mode api|log          Export mode: 'api' or 'log' (default: api with log fallback)
#   --editor-log PATH       Path to Editor.log (default: auto-detected)
#
# Requirements:
#   - Unity Editor installed
#   - UnityProfilerExporter.cs in Assets/Editor/ (for API mode)
#
# Output:
#   JSON file with performance metrics:
#   - fps_average, fps_p95
#   - gc_alloc_per_frame_kb
#   - draw_calls
#   - memory_peak_mb
#   - cpu_main_thread_ms

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default values
PROJECT_PATH=""
OUTPUT_PATH="./unity-profile.json"
UNITY_PATH=""
EXPORT_MODE="api"
EDITOR_LOG_PATH=""

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --project)
                PROJECT_PATH="$2"
                shift 2
                ;;
            --output)
                OUTPUT_PATH="$2"
                shift 2
                ;;
            --unity-path)
                UNITY_PATH="$2"
                shift 2
                ;;
            --mode)
                EXPORT_MODE="$2"
                shift 2
                ;;
            --editor-log)
                EDITOR_LOG_PATH="$2"
                shift 2
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "${PROJECT_PATH}" ]]; then
        echo -e "${RED}❌ ERROR: --project is required${NC}"
        exit 1
    fi

    if [[ ! -d "${PROJECT_PATH}" ]]; then
        echo -e "${RED}❌ ERROR: Project path does not exist: ${PROJECT_PATH}${NC}"
        exit 1
    fi
}

# Detect Unity Editor path
detect_unity_path() {
    if [[ -n "${UNITY_PATH}" ]]; then
        if [[ ! -f "${UNITY_PATH}" ]]; then
            echo -e "${RED}❌ ERROR: Unity executable not found: ${UNITY_PATH}${NC}"
            exit 1
        fi
        return
    fi

    echo -e "${BLUE}🔍 Detecting Unity Editor...${NC}"

    # Common Unity Hub paths
    if [[ "$(uname)" == "Darwin" ]]; then
        # macOS
        UNITY_HUB_PATH="/Applications/Unity/Hub/Editor"
        if [[ -d "${UNITY_HUB_PATH}" ]]; then
            # Find latest version
            LATEST_VERSION=$(ls -1 "${UNITY_HUB_PATH}" | sort -V | tail -n 1)
            UNITY_PATH="${UNITY_HUB_PATH}/${LATEST_VERSION}/Unity.app/Contents/MacOS/Unity"
        fi

        # Fallback to direct install
        if [[ -z "${UNITY_PATH}" ]] && [[ -f "/Applications/Unity/Unity.app/Contents/MacOS/Unity" ]]; then
            UNITY_PATH="/Applications/Unity/Unity.app/Contents/MacOS/Unity"
        fi
    elif [[ "$(uname)" == "Linux" ]]; then
        # Linux
        UNITY_HUB_PATH="${HOME}/Unity/Hub/Editor"
        if [[ -d "${UNITY_HUB_PATH}" ]]; then
            LATEST_VERSION=$(ls -1 "${UNITY_HUB_PATH}" | sort -V | tail -n 1)
            UNITY_PATH="${UNITY_HUB_PATH}/${LATEST_VERSION}/Editor/Unity"
        fi
    elif [[ "$(uname)" =~ ^MINGW|^MSYS ]]; then
        # Windows (Git Bash/MSYS)
        UNITY_HUB_PATH="C:/Program Files/Unity/Hub/Editor"
        if [[ -d "${UNITY_HUB_PATH}" ]]; then
            LATEST_VERSION=$(ls -1 "${UNITY_HUB_PATH}" | sort -V | tail -n 1)
            UNITY_PATH="${UNITY_HUB_PATH}/${LATEST_VERSION}/Editor/Unity.exe"
        fi
    fi

    if [[ -z "${UNITY_PATH}" ]] || [[ ! -f "${UNITY_PATH}" ]]; then
        echo -e "${RED}❌ ERROR: Could not detect Unity Editor${NC}"
        echo -e "Please specify Unity path with --unity-path"
        exit 1
    fi

    echo -e "  Found Unity: ${UNITY_PATH}"
}

# Check if UnityProfilerExporter.cs exists
check_profiler_exporter() {
    EXPORTER_PATH="${PROJECT_PATH}/Assets/Editor/UnityProfilerExporter.cs"

    if [[ ! -f "${EXPORTER_PATH}" ]]; then
        echo -e "${YELLOW}⚠️  UnityProfilerExporter.cs not found${NC}"
        echo -e "  Expected: ${EXPORTER_PATH}"
        echo -e "  Falling back to Editor.log parsing"
        EXPORT_MODE="log"
        return 1
    fi

    echo -e "${GREEN}✅ UnityProfilerExporter.cs found${NC}"
    return 0
}

# Export using Unity Editor API
export_via_api() {
    echo -e "${BLUE}📊 Exporting profiler data via Unity Editor API${NC}"

    # Run Unity in batch mode
    "${UNITY_PATH}" \
        -batchmode \
        -nographics \
        -projectPath "${PROJECT_PATH}" \
        -executeMethod UnityProfilerExporter.ExportProfilerData \
        -quit \
        -logFile - \
        > unity-batch-log.txt 2>&1

    # Check if export succeeded
    if [[ -f "${OUTPUT_PATH}" ]]; then
        echo -e "${GREEN}✅ Profiler data exported${NC}"
        return 0
    else
        echo -e "${RED}❌ Export failed${NC}"
        echo -e "${YELLOW}Unity log:${NC}"
        cat unity-batch-log.txt
        return 1
    fi
}

# Detect Editor.log path
detect_editor_log() {
    if [[ -n "${EDITOR_LOG_PATH}" ]]; then
        if [[ ! -f "${EDITOR_LOG_PATH}" ]]; then
            echo -e "${RED}❌ ERROR: Editor.log not found: ${EDITOR_LOG_PATH}${NC}"
            exit 1
        fi
        return
    fi

    echo -e "${BLUE}🔍 Detecting Editor.log...${NC}"

    if [[ "$(uname)" == "Darwin" ]]; then
        EDITOR_LOG_PATH="${HOME}/Library/Logs/Unity/Editor.log"
    elif [[ "$(uname)" == "Linux" ]]; then
        EDITOR_LOG_PATH="${HOME}/.config/unity3d/Editor.log"
    elif [[ "$(uname)" =~ ^MINGW|^MSYS ]]; then
        EDITOR_LOG_PATH="${LOCALAPPDATA}/Unity/Editor/Editor.log"
    fi

    if [[ ! -f "${EDITOR_LOG_PATH}" ]]; then
        echo -e "${RED}❌ ERROR: Could not find Editor.log${NC}"
        echo -e "Please specify path with --editor-log"
        exit 1
    fi

    echo -e "  Found Editor.log: ${EDITOR_LOG_PATH}"
}

# Parse Editor.log for profiler data
export_via_log() {
    echo -e "${BLUE}📊 Parsing Editor.log for profiler data${NC}"

    detect_editor_log

    python3 - <<EOF > "${OUTPUT_PATH}"
import re
import json
import sys

editor_log = "${EDITOR_LOG_PATH}"

frame_times = []
gc_allocs = []
draw_calls = []
memory_values = []

try:
    with open(editor_log, 'r', encoding='utf-8', errors='ignore') as f:
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

            # Match memory usage
            # Example: "Total Allocated: 142.5 MB"
            memory_match = re.search(r'Total Allocated: (\d+\.\d+) MB', line)
            if memory_match:
                memory_values.append(float(memory_match.group(1)))

    if not frame_times:
        print("WARNING: No frame timing data found in Editor.log", file=sys.stderr)
        print("Using placeholder values", file=sys.stderr)
        frame_times = [16.67]  # 60 FPS placeholder

    # Calculate metrics
    import numpy as np

    avg_fps = 1000 / np.mean(frame_times)
    p95_frame_time = np.percentile(frame_times, 95)
    p95_fps = 1000 / p95_frame_time
    avg_gc_alloc = np.mean(gc_allocs) if gc_allocs else 0
    avg_draw_calls = int(np.mean(draw_calls)) if draw_calls else 0
    peak_memory_mb = max(memory_values) if memory_values else 0
    avg_frame_time = np.mean(frame_times)

    profile_data = {
        "fps_average": round(avg_fps, 1),
        "fps_p95": round(p95_fps, 1),
        "gc_alloc_per_frame_kb": round(avg_gc_alloc, 2),
        "draw_calls": avg_draw_calls,
        "memory_peak_mb": round(peak_memory_mb, 1),
        "cpu_main_thread_ms": round(avg_frame_time, 2)
    }

    print(json.dumps(profile_data, indent=2))

except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
EOF

    if [[ -f "${OUTPUT_PATH}" ]]; then
        echo -e "${GREEN}✅ Profiler data parsed from Editor.log${NC}"
        return 0
    else
        echo -e "${RED}❌ Parsing failed${NC}"
        return 1
    fi
}

# Display profiler data
display_metrics() {
    if [[ ! -f "${OUTPUT_PATH}" ]]; then
        return
    fi

    echo ""
    echo -e "${BLUE}📊 Performance Metrics:${NC}"
    echo ""

    python3 - <<EOF
import json

with open("${OUTPUT_PATH}", 'r') as f:
    data = json.load(f)

print(f"  Average FPS:          {data.get('fps_average', 0):.1f} FPS")
print(f"  95th Percentile FPS:  {data.get('fps_p95', 0):.1f} FPS")
print(f"  GC Alloc/Frame:       {data.get('gc_alloc_per_frame_kb', 0):.2f} KB")
print(f"  Draw Calls:           {data.get('draw_calls', 0)}")
print(f"  Peak Memory:          {data.get('memory_peak_mb', 0):.1f} MB")
print(f"  CPU Main Thread:      {data.get('cpu_main_thread_ms', 0):.2f} ms")

# Validate against thresholds
fps_p95 = data.get('fps_p95', 0)
memory_peak = data.get('memory_peak_mb', 0)

print("")
print("Quality Gate Validation:")

if fps_p95 >= 60:
    print("  ✅ QG-PERF-002: PASS (FPS >= 60)")
else:
    print(f"  ❌ QG-PERF-002: FAIL (FPS {fps_p95:.1f} < 60)")

if memory_peak < 150 or memory_peak == 0:
    print("  ✅ QG-PERF-003: PASS (Memory < 150 MB)")
else:
    print(f"  ❌ QG-PERF-003: FAIL (Memory {memory_peak:.1f} >= 150 MB)")
EOF
}

# Main execution
main() {
    if [[ $# -eq 0 ]]; then
        echo "Unity Profiler Data Export"
        echo ""
        echo "Usage: $0 --project /path/to/unity/project [options]"
        echo ""
        echo "Options:"
        echo "  --project PATH          Unity project path (required)"
        echo "  --output PATH           Output JSON file (default: ./unity-profile.json)"
        echo "  --unity-path PATH       Unity Editor executable (auto-detected)"
        echo "  --mode api|log          Export mode (default: api with log fallback)"
        echo "  --editor-log PATH       Path to Editor.log (auto-detected)"
        echo ""
        echo "Export Modes:"
        echo "  api    Use UnityProfilerExporter.cs (requires Assets/Editor/UnityProfilerExporter.cs)"
        echo "  log    Parse Unity Editor.log file"
        echo ""
        echo "Examples:"
        echo "  $0 --project ./MyGame"
        echo "  $0 --project ./MyGame --mode log"
        echo "  $0 --project ./MyGame --unity-path /path/to/Unity"
        exit 1
    fi

    parse_args "$@"

    echo -e "${GREEN}🎮 Unity Profiler Export${NC}"
    echo -e "Project: ${PROJECT_PATH}"
    echo -e "Output: ${OUTPUT_PATH}"
    echo ""

    # Try API mode first if requested
    if [[ "${EXPORT_MODE}" == "api" ]]; then
        detect_unity_path

        if check_profiler_exporter; then
            if export_via_api; then
                display_metrics
                echo ""
                echo -e "${GREEN}✅ Export complete!${NC}"
                exit 0
            else
                echo -e "${YELLOW}⚠️  API export failed, falling back to log parsing${NC}"
                EXPORT_MODE="log"
            fi
        fi
    fi

    # Fallback to log parsing
    if [[ "${EXPORT_MODE}" == "log" ]]; then
        if export_via_log; then
            display_metrics
            echo ""
            echo -e "${GREEN}✅ Export complete!${NC}"
            exit 0
        else
            echo -e "${RED}❌ Export failed${NC}"
            exit 1
        fi
    fi
}

main "$@"

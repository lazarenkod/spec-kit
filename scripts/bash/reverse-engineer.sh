#!/usr/bin/env bash

set -e

JSON_MODE=false
SCOPE=""
EXCLUDE_PATTERNS=("node_modules/" "dist/" "build/" "__pycache__/" "venv/" ".git/")
MIN_CONFIDENCE="0.70"
LANGUAGE=""
OUTPUT_DIR="reverse-engineered"
MERGE_MODE=false
ARGS=()

i=1
while [ $i -le $# ]; do
    arg="${!i}"
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --scope)
            if [ $((i + 1)) -gt $# ]; then
                echo 'Error: --scope requires a value' >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            if [[ "$next_arg" == --* ]]; then
                echo 'Error: --scope requires a value' >&2
                exit 1
            fi
            SCOPE="$next_arg"
            ;;
        --exclude)
            if [ $((i + 1)) -gt $# ]; then
                echo 'Error: --exclude requires a value' >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            if [[ "$next_arg" == --* ]]; then
                echo 'Error: --exclude requires a value' >&2
                exit 1
            fi
            EXCLUDE_PATTERNS+=("$next_arg")
            ;;
        --min-confidence)
            if [ $((i + 1)) -gt $# ]; then
                echo 'Error: --min-confidence requires a value' >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            if [[ "$next_arg" == --* ]]; then
                echo 'Error: --min-confidence requires a value' >&2
                exit 1
            fi
            MIN_CONFIDENCE="$next_arg"
            ;;
        --language)
            if [ $((i + 1)) -gt $# ]; then
                echo 'Error: --language requires a value' >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            if [[ "$next_arg" == --* ]]; then
                echo 'Error: --language requires a value' >&2
                exit 1
            fi
            LANGUAGE="$next_arg"
            ;;
        --output-dir)
            if [ $((i + 1)) -gt $# ]; then
                echo 'Error: --output-dir requires a value' >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            if [[ "$next_arg" == --* ]]; then
                echo 'Error: --output-dir requires a value' >&2
                exit 1
            fi
            OUTPUT_DIR="$next_arg"
            ;;
        --merge-mode)
            MERGE_MODE=true
            ;;
        --help|-h)
            echo "Usage: $0 --scope <patterns> [options]"
            echo ""
            echo "Options:"
            echo "  --scope <patterns>        Scan scope patterns (required): \"src/**/*.ts\", \"api/**/*.py\""
            echo "  --exclude <pattern>       Exclude pattern (can be specified multiple times)"
            echo "  --min-confidence <value>  Minimum confidence threshold (0.0-1.0, default: 0.70)"
            echo "  --language <lang>         Force language (typescript, python, go, java, kotlin)"
            echo "  --output-dir <dir>        Override output directory (default: reverse-engineered/)"
            echo "  --merge-mode              Auto-merge verified FRs into canonical spec"
            echo "  --json                    Output in JSON format"
            echo "  --help, -h                Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --scope \"src/**/*.ts\" --exclude \"*.test.ts\""
            echo "  $0 --scope \"api/**/*.py\" --min-confidence 0.80"
            echo "  $0 --scope \"src/**/*.go\" --language go --output-dir extracted"
            exit 0
            ;;
        *)
            ARGS+=("$arg")
            ;;
    esac
    i=$((i + 1))
done

# Validation: --scope is required
if [ -z "$SCOPE" ]; then
    if [ "$JSON_MODE" = true ]; then
        echo '{"error": "Missing required argument: --scope", "exit_code": 1}'
    else
        echo "Error: --scope is required" >&2
        echo "Run '$0 --help' for usage information." >&2
    fi
    exit 1
fi

# Validation: check if output directory already exists
if [ -d "$OUTPUT_DIR" ]; then
    if [ "$JSON_MODE" = true ]; then
        echo "{\"error\": \"Output directory already exists: $OUTPUT_DIR\", \"exit_code\": 1}"
    else
        echo "Error: Output directory already exists: $OUTPUT_DIR" >&2
        echo "To re-extract, delete the directory first or specify a different --output-dir" >&2
    fi
    exit 1
fi

# Validation: check min-confidence range
if ! echo "$MIN_CONFIDENCE" | grep -qE '^0\.[0-9]+$|^1\.0$|^1$'; then
    if [ "$JSON_MODE" = true ]; then
        echo "{\"error\": \"Invalid --min-confidence value. Must be between 0.0 and 1.0\", \"exit_code\": 1}"
    else
        echo "Error: Invalid --min-confidence value. Must be between 0.0 and 1.0" >&2
    fi
    exit 1
fi

# Validation: check supported languages
if [ -n "$LANGUAGE" ]; then
    if ! echo "$LANGUAGE" | grep -qE '^(typescript|python|go|java|kotlin)$'; then
        if [ "$JSON_MODE" = true ]; then
            echo "{\"error\": \"Unsupported language: $LANGUAGE. Supported: typescript, python, go, java, kotlin\", \"exit_code\": 1}"
        else
            echo "Error: Unsupported language: $LANGUAGE" >&2
            echo "Supported languages: typescript, python, go, java, kotlin" >&2
        fi
        exit 1
    fi
fi

# Output JSON if requested
if [ "$JSON_MODE" = true ]; then
    exclude_json=""
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if [ -n "$exclude_json" ]; then
            exclude_json="$exclude_json,"
        fi
        exclude_json="$exclude_json\"$pattern\""
    done

    echo "{"
    echo "  \"status\": \"ready\","
    echo "  \"scope\": \"$SCOPE\","
    echo "  \"exclude\": [$exclude_json],"
    echo "  \"min_confidence\": $MIN_CONFIDENCE,"
    echo "  \"language\": \"$LANGUAGE\","
    echo "  \"output_dir\": \"$OUTPUT_DIR\","
    echo "  \"merge_mode\": $MERGE_MODE"
    echo "}"
else
    echo "✓ Reverse-engineering prerequisites check passed"
    echo ""
    echo "Configuration:"
    echo "  Scope:          $SCOPE"
    echo "  Exclude:        ${EXCLUDE_PATTERNS[*]}"
    echo "  Min confidence: $MIN_CONFIDENCE"
    if [ -n "$LANGUAGE" ]; then
        echo "  Language:       $LANGUAGE (forced)"
    else
        echo "  Language:       auto-detect"
    fi
    echo "  Output dir:     $OUTPUT_DIR"
    echo "  Merge mode:     $MERGE_MODE"
    echo ""
    echo "Next step: Run /speckit.reverse-engineer in your AI agent"
fi

exit 0

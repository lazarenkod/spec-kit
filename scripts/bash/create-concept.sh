#!/usr/bin/env bash

set -e

JSON_MODE=false
ARGS=()
i=1
while [ $i -le $# ]; do
    arg="${!i}"
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --help|-h)
            echo "Usage: $0 [--json] [project_description]"
            echo ""
            echo "Creates or returns path to specs/concept.md for capturing full project concept."
            echo ""
            echo "Options:"
            echo "  --json    Output in JSON format"
            echo "  --help    Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 'Task management app for teams'"
            echo "  $0 --json 'E-commerce platform'"
            exit 0
            ;;
        *)
            ARGS+=("$arg")
            ;;
    esac
    i=$((i + 1))
done

PROJECT_DESCRIPTION="${ARGS[*]}"

# Function to find the repository root by searching for existing project markers
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -d "$dir/.specify" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

# Resolve repository root
SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
else
    REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
    if [ -z "$REPO_ROOT" ]; then
        echo "Error: Could not determine repository root. Please run this script from within the repository." >&2
        exit 1
    fi
fi

cd "$REPO_ROOT"

SPECS_DIR="$REPO_ROOT/specs"
mkdir -p "$SPECS_DIR"

CONCEPT_FILE="$SPECS_DIR/concept.md"
TEMPLATE="$REPO_ROOT/.specify/templates/concept-template.md"

# Check if concept.md already exists
ALREADY_EXISTS=false
if [ -f "$CONCEPT_FILE" ]; then
    ALREADY_EXISTS=true
    >&2 echo "[concept] Using existing concept file: $CONCEPT_FILE"
else
    # Create from template or empty file
    if [ -f "$TEMPLATE" ]; then
        cp "$TEMPLATE" "$CONCEPT_FILE"
        >&2 echo "[concept] Created concept file from template: $CONCEPT_FILE"
    else
        # Create minimal structure if template doesn't exist
        cat > "$CONCEPT_FILE" << 'EOF'
# Concept: [PROJECT_NAME]

**Version**: 1.0 | **Created**: [DATE] | **Status**: Draft

## Vision Statement

[Describe the core vision of this project]

## Business Context

### Problem Space

- [Problem 1]

### Target Users

| Persona | Description | Primary Goals |
|---------|-------------|---------------|
| [Persona 1] | [Description] | [Goals] |

## Feature Hierarchy

### Epic: [EPIC-001] [Epic Name]

**Goal**: [High-level outcome]
**Priority**: P1

#### Feature: [EPIC-001.F01] [Feature Name]

##### Stories:

- [EPIC-001.F01.S01] As a [user], I want [capability] so that [benefit]

## User Journeys

### Journey: [J001] [Journey Name]

| Step | Action | Features Involved |
|------|--------|-------------------|
| 1 | [Action] | [Features] |

## Cross-Feature Dependencies

| Feature | Depends On | Blocks |
|---------|------------|--------|
| [Feature] | - | - |

## Ideas Backlog

- [ ] [Idea 1]

## Glossary

| Term | Definition |
|------|------------|
| [Term] | [Definition] |

## Traceability Skeleton

| Concept ID | Spec Created | Status |
|------------|--------------|--------|
| [ID] | [ ] | Not started |
EOF
        >&2 echo "[concept] Created minimal concept file: $CONCEPT_FILE"
    fi
fi

# Output result
if $JSON_MODE; then
    printf '{"CONCEPT_FILE":"%s","SPECS_DIR":"%s","ALREADY_EXISTS":%s,"PROJECT_DESCRIPTION":"%s"}\n' \
        "$CONCEPT_FILE" "$SPECS_DIR" "$ALREADY_EXISTS" "$PROJECT_DESCRIPTION"
else
    echo "CONCEPT_FILE: $CONCEPT_FILE"
    echo "SPECS_DIR: $SPECS_DIR"
    echo "ALREADY_EXISTS: $ALREADY_EXISTS"
    if [ -n "$PROJECT_DESCRIPTION" ]; then
        echo "PROJECT_DESCRIPTION: $PROJECT_DESCRIPTION"
    fi
fi

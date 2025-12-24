#!/usr/bin/env bash
set -euo pipefail

# orchestrate-handoff.sh
# Manages handoff documents between phases in multi-agent workflow
# Usage: orchestrate-handoff.sh <action> <phase> [feature_dir]
#   Actions: generate | load | validate | list
#   Phases: specify | plan | tasks | implement

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Default paths
SPECS_DIR="specs/features"
HANDOFFS_SUBDIR="handoffs"
TEMPLATE_PATH=".specify/templates/handoff-template.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    cat << EOF
Usage: $(basename "$0") <action> <phase> [feature_dir]

Actions:
  generate  Create a handoff document for the specified phase
  load      Read and display the handoff from the previous phase
  validate  Verify handoff document completeness
  list      List all handoffs for a feature

Phases:
  specify   Product Agent → Architect Agent
  plan      Architect Agent → Decomposer Agent
  tasks     Decomposer Agent → Developer Agent
  implement Developer Agent (receives tasks handoff)

Examples:
  $(basename "$0") generate specify specs/features/001-login
  $(basename "$0") load plan specs/features/001-login
  $(basename "$0") validate tasks specs/features/001-login
  $(basename "$0") list specs/features/001-login

EOF
    exit 1
}

# Map phases to handoff file names
get_handoff_file() {
    local phase=$1
    case $phase in
        specify)  echo "specify-to-plan.md" ;;
        plan)     echo "plan-to-tasks.md" ;;
        tasks)    echo "tasks-to-implement.md" ;;
        *)        echo "" ;;
    esac
}

# Map phases to persona names
get_source_persona() {
    local phase=$1
    case $phase in
        specify)  echo "Product Agent" ;;
        plan)     echo "Architect Agent" ;;
        tasks)    echo "Decomposer Agent" ;;
        implement) echo "Developer Agent" ;;
        *)        echo "Unknown" ;;
    esac
}

get_target_persona() {
    local phase=$1
    case $phase in
        specify)  echo "Architect Agent" ;;
        plan)     echo "Decomposer Agent" ;;
        tasks)    echo "Developer Agent" ;;
        implement) echo "QA Agent" ;;
        *)        echo "Unknown" ;;
    esac
}

# Get the previous phase's handoff file (for loading)
get_previous_handoff() {
    local phase=$1
    case $phase in
        plan)     echo "specify-to-plan.md" ;;
        tasks)    echo "plan-to-tasks.md" ;;
        implement) echo "tasks-to-implement.md" ;;
        *)        echo "" ;;
    esac
}

# Generate a new handoff document
generate_handoff() {
    local phase=$1
    local feature_dir=$2

    local handoff_file
    handoff_file=$(get_handoff_file "$phase")

    if [[ -z "$handoff_file" ]]; then
        echo -e "${RED}Error: Invalid phase '$phase' for generate action${NC}"
        exit 1
    fi

    local handoffs_dir="$feature_dir/$HANDOFFS_SUBDIR"
    local output_path="$handoffs_dir/$handoff_file"

    # Create handoffs directory if needed
    mkdir -p "$handoffs_dir"

    # Check if handoff already exists
    if [[ -f "$output_path" ]]; then
        echo -e "${YELLOW}Warning: Handoff already exists at $output_path${NC}"
        read -p "Overwrite? (y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo "Aborted."
            exit 0
        fi
    fi

    # Extract feature info
    local feature_name
    feature_name=$(basename "$feature_dir")
    local feature_id
    feature_id=$(echo "$feature_name" | grep -oE '^[0-9]+' || echo "000")

    # Get persona names
    local source_persona
    source_persona=$(get_source_persona "$phase")
    local target_persona
    target_persona=$(get_target_persona "$phase")

    # Find template
    local template_file=""
    if [[ -f "$REPO_ROOT/$TEMPLATE_PATH" ]]; then
        template_file="$REPO_ROOT/$TEMPLATE_PATH"
    elif [[ -f "$REPO_ROOT/templates/handoff-template.md" ]]; then
        template_file="$REPO_ROOT/templates/handoff-template.md"
    fi

    if [[ -n "$template_file" ]]; then
        # Copy and substitute template
        sed -e "s/{SOURCE_PHASE}/$phase/g" \
            -e "s/{TARGET_PHASE}/$(echo "$phase" | sed 's/specify/plan/;s/plan/tasks/;s/tasks/implement/')/g" \
            -e "s/{FEATURE_ID}/$feature_id/g" \
            -e "s/{FEATURE_NAME}/${feature_name#*-}/g" \
            -e "s/{DATE}/$(date +%Y-%m-%d)/g" \
            -e "s/{SOURCE_PERSONA}/$source_persona/g" \
            -e "s/{TARGET_PERSONA}/$target_persona/g" \
            "$template_file" > "$output_path"
    else
        # Generate minimal handoff
        cat > "$output_path" << EOF
# Handoff: $phase → $(echo "$phase" | sed 's/specify/plan/;s/plan/tasks/;s/tasks/implement/')

> **Feature**: $feature_name
> **Generated**: $(date +%Y-%m-%d)
> **Source Agent**: $source_persona
> **Target Agent**: $target_persona

---

## Summary

<!-- Complete this section with phase outcomes -->

## Key Decisions Made

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| | | |

## Constraints for Next Phase

-

## Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| | | |

## Open Questions

- [ ]

---

EOF
    fi

    echo -e "${GREEN}Generated handoff: $output_path${NC}"
    echo -e "${BLUE}Next: Fill in the template with phase-specific context${NC}"
}

# Load and display a handoff document
load_handoff() {
    local phase=$1
    local feature_dir=$2

    local handoff_file
    handoff_file=$(get_previous_handoff "$phase")

    if [[ -z "$handoff_file" ]]; then
        echo -e "${YELLOW}No previous handoff for phase '$phase' (this is the first phase)${NC}"
        exit 0
    fi

    local handoff_path="$feature_dir/$HANDOFFS_SUBDIR/$handoff_file"

    if [[ ! -f "$handoff_path" ]]; then
        echo -e "${RED}Error: Handoff not found at $handoff_path${NC}"
        echo -e "${YELLOW}The previous phase may not have generated a handoff.${NC}"
        echo -e "${BLUE}Suggestion: Run '$(basename "$0") generate <previous_phase> $feature_dir'${NC}"
        exit 1
    fi

    echo -e "${GREEN}=== Loading Handoff: $handoff_file ===${NC}"
    echo ""

    # Display key sections
    echo -e "${BLUE}## Summary${NC}"
    sed -n '/^## Summary/,/^## /p' "$handoff_path" | head -n -1

    echo -e "${BLUE}## Key Decisions${NC}"
    sed -n '/^## Key Decisions/,/^## /p' "$handoff_path" | head -n -1

    echo -e "${BLUE}## Constraints${NC}"
    sed -n '/^## Constraints/,/^## /p' "$handoff_path" | head -n -1

    echo -e "${BLUE}## Risks${NC}"
    sed -n '/^## Risks/,/^## /p' "$handoff_path" | head -n -1

    echo -e "${YELLOW}## Open Questions${NC}"
    sed -n '/^## Open Questions/,/^## /p' "$handoff_path" | head -n -1

    echo ""
    echo -e "${GREEN}Full handoff available at: $handoff_path${NC}"
}

# Validate handoff document completeness
validate_handoff() {
    local phase=$1
    local feature_dir=$2

    local handoff_file
    handoff_file=$(get_handoff_file "$phase")

    if [[ -z "$handoff_file" ]]; then
        echo -e "${RED}Error: Invalid phase '$phase' for validate action${NC}"
        exit 1
    fi

    local handoff_path="$feature_dir/$HANDOFFS_SUBDIR/$handoff_file"

    if [[ ! -f "$handoff_path" ]]; then
        echo -e "${RED}Error: Handoff not found at $handoff_path${NC}"
        exit 1
    fi

    echo -e "${BLUE}Validating: $handoff_path${NC}"
    echo ""

    local errors=0
    local warnings=0

    # Check for required sections
    for section in "Summary" "Key Decisions" "Constraints" "Risks" "Open Questions"; do
        if ! grep -q "^## $section" "$handoff_path"; then
            echo -e "${RED}✗ Missing section: $section${NC}"
            ((errors++))
        else
            echo -e "${GREEN}✓ Found section: $section${NC}"
        fi
    done

    # Check for placeholder content
    if grep -q '{DECISION_' "$handoff_path" || grep -q '{RISK_' "$handoff_path"; then
        echo -e "${YELLOW}⚠ Contains unfilled placeholders${NC}"
        ((warnings++))
    fi

    # Check for empty tables
    if grep -qE '^\|[[:space:]]*\|[[:space:]]*\|[[:space:]]*\|$' "$handoff_path"; then
        echo -e "${YELLOW}⚠ Contains empty table rows${NC}"
        ((warnings++))
    fi

    # Check validation checklist
    local checked
    checked=$(grep -c '\[x\]' "$handoff_path" 2>/dev/null || echo "0")
    local unchecked
    unchecked=$(grep -c '\[ \]' "$handoff_path" 2>/dev/null || echo "0")

    echo ""
    echo "Checklist: $checked checked, $unchecked unchecked"

    echo ""
    if [[ $errors -gt 0 ]]; then
        echo -e "${RED}Validation FAILED: $errors errors, $warnings warnings${NC}"
        exit 1
    elif [[ $warnings -gt 0 ]]; then
        echo -e "${YELLOW}Validation PASSED with warnings: $warnings warnings${NC}"
        exit 0
    else
        echo -e "${GREEN}Validation PASSED${NC}"
        exit 0
    fi
}

# List all handoffs for a feature
list_handoffs() {
    local feature_dir=$1
    local handoffs_dir="$feature_dir/$HANDOFFS_SUBDIR"

    echo -e "${BLUE}Handoffs for: $(basename "$feature_dir")${NC}"
    echo ""

    if [[ ! -d "$handoffs_dir" ]]; then
        echo -e "${YELLOW}No handoffs directory found${NC}"
        exit 0
    fi

    for handoff in "$handoffs_dir"/*.md; do
        if [[ -f "$handoff" ]]; then
            local filename
            filename=$(basename "$handoff")
            local modified
            modified=$(stat -c %y "$handoff" 2>/dev/null || stat -f %Sm "$handoff" 2>/dev/null || echo "unknown")
            echo -e "${GREEN}✓${NC} $filename (modified: $modified)"
        fi
    done
}

# JSON output mode
output_json() {
    local action=$1
    local phase=$2
    local feature_dir=$3

    case $action in
        list)
            local handoffs_dir="$feature_dir/$HANDOFFS_SUBDIR"
            echo "{"
            echo "  \"feature\": \"$(basename "$feature_dir")\","
            echo "  \"handoffs\": ["
            local first=true
            for handoff in "$handoffs_dir"/*.md 2>/dev/null; do
                if [[ -f "$handoff" ]]; then
                    if [[ "$first" == "false" ]]; then
                        echo ","
                    fi
                    echo -n "    \"$(basename "$handoff")\""
                    first=false
                fi
            done
            echo ""
            echo "  ]"
            echo "}"
            ;;
        validate)
            local handoff_file
            handoff_file=$(get_handoff_file "$phase")
            local handoff_path="$feature_dir/$HANDOFFS_SUBDIR/$handoff_file"
            local valid="true"
            [[ ! -f "$handoff_path" ]] && valid="false"
            echo "{"
            echo "  \"valid\": $valid,"
            echo "  \"path\": \"$handoff_path\""
            echo "}"
            ;;
    esac
}

# Main
main() {
    if [[ $# -lt 2 ]]; then
        usage
    fi

    local action=$1
    local phase_or_dir=$2
    local feature_dir=${3:-""}

    # Handle --json flag
    local json_mode=false
    for arg in "$@"; do
        if [[ "$arg" == "--json" ]]; then
            json_mode=true
        fi
    done

    # For list action, phase_or_dir is actually the feature_dir
    if [[ "$action" == "list" ]]; then
        feature_dir=$phase_or_dir
        if [[ ! -d "$feature_dir" ]]; then
            echo -e "${RED}Error: Directory not found: $feature_dir${NC}"
            exit 1
        fi
        if [[ "$json_mode" == "true" ]]; then
            output_json list "" "$feature_dir"
        else
            list_handoffs "$feature_dir"
        fi
        exit 0
    fi

    # Validate phase
    local phase=$phase_or_dir
    case $phase in
        specify|plan|tasks|implement) ;;
        *)
            echo -e "${RED}Error: Invalid phase '$phase'${NC}"
            echo "Valid phases: specify, plan, tasks, implement"
            exit 1
            ;;
    esac

    # Feature dir is required for other actions
    if [[ -z "$feature_dir" ]]; then
        echo -e "${RED}Error: feature_dir is required${NC}"
        usage
    fi

    if [[ ! -d "$feature_dir" ]]; then
        echo -e "${RED}Error: Directory not found: $feature_dir${NC}"
        exit 1
    fi

    case $action in
        generate)
            generate_handoff "$phase" "$feature_dir"
            ;;
        load)
            load_handoff "$phase" "$feature_dir"
            ;;
        validate)
            if [[ "$json_mode" == "true" ]]; then
                output_json validate "$phase" "$feature_dir"
            else
                validate_handoff "$phase" "$feature_dir"
            fi
            ;;
        *)
            echo -e "${RED}Error: Unknown action '$action'${NC}"
            usage
            ;;
    esac
}

main "$@"

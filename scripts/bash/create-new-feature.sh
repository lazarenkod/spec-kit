#!/usr/bin/env bash

set -e

JSON_MODE=false
SHORT_NAME=""
BRANCH_NUMBER=""
EXTENDS_FEATURE=""
ARGS=()
i=1
while [ $i -le $# ]; do
    arg="${!i}"
    case "$arg" in
        --json) 
            JSON_MODE=true 
            ;;
        --short-name)
            if [ $((i + 1)) -gt $# ]; then
                echo 'Error: --short-name requires a value' >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            # Check if the next argument is another option (starts with --)
            if [[ "$next_arg" == --* ]]; then
                echo 'Error: --short-name requires a value' >&2
                exit 1
            fi
            SHORT_NAME="$next_arg"
            ;;
        --number)
            if [ $((i + 1)) -gt $# ]; then
                echo 'Error: --number requires a value' >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            if [[ "$next_arg" == --* ]]; then
                echo 'Error: --number requires a value' >&2
                exit 1
            fi
            BRANCH_NUMBER="$next_arg"
            ;;
        --extends)
            if [ $((i + 1)) -gt $# ]; then
                echo 'Error: --extends requires a feature ID or branch name' >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            if [[ "$next_arg" == --* ]]; then
                echo 'Error: --extends requires a feature ID or branch name' >&2
                exit 1
            fi
            EXTENDS_FEATURE="$next_arg"
            ;;
        --help|-h)
            echo "Usage: $0 [--json] [--short-name <name>] [--number N] [--extends <feature>] <feature_description>"
            echo ""
            echo "Options:"
            echo "  --json               Output in JSON format"
            echo "  --short-name <name>  Provide a custom short name (2-4 words) for the branch"
            echo "  --number N           Specify branch number manually (overrides auto-detection)"
            echo "  --extends <feature>  Extend a merged feature (ID like '001' or full name '001-login')"
            echo "  --help, -h           Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 'Add user authentication system' --short-name 'user-auth'"
            echo "  $0 'Implement OAuth2 integration for API' --number 5"
            echo "  $0 'Add rate limiting to login' --extends 001"
            exit 0
            ;;
        *) 
            ARGS+=("$arg") 
            ;;
    esac
    i=$((i + 1))
done

FEATURE_DESCRIPTION="${ARGS[*]}"
if [ -z "$FEATURE_DESCRIPTION" ]; then
    echo "Usage: $0 [--json] [--short-name <name>] [--number N] <feature_description>" >&2
    exit 1
fi

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

# Function to get highest number from specs directory
get_highest_from_specs() {
    local specs_dir="$1"
    local highest=0
    
    if [ -d "$specs_dir" ]; then
        for dir in "$specs_dir"/*; do
            [ -d "$dir" ] || continue
            dirname=$(basename "$dir")
            number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
            number=$((10#$number))
            if [ "$number" -gt "$highest" ]; then
                highest=$number
            fi
        done
    fi
    
    echo "$highest"
}

# Function to get highest number from git branches
get_highest_from_branches() {
    local highest=0

    # Get all branches (local and remote)
    branches=$(git branch -a 2>/dev/null || echo "")

    if [ -n "$branches" ]; then
        while IFS= read -r branch; do
            # Clean branch name: remove leading markers and remote prefixes
            clean_branch=$(echo "$branch" | sed 's/^[* ]*//; s|^remotes/[^/]*/||')

            # Extract feature number if branch matches pattern N+- (one or more digits followed by hyphen)
            # This handles: 1-feature, 12-feature, 123-feature, 1234-feature, etc.
            if echo "$clean_branch" | grep -qE '^[0-9]+-'; then
                number=$(echo "$clean_branch" | grep -oE '^[0-9]+' || echo "0")
                number=$((10#$number))
                if [ "$number" -gt "$highest" ]; then
                    highest=$number
                fi
            fi
        done <<< "$branches"
    fi

    echo "$highest"
}

# Function to check if a branch number is already taken
is_branch_number_taken() {
    local num="$1"
    local padded=$(printf "%03d" "$((10#$num))")

    # Check local branches
    if git branch --list "${padded}-*" 2>/dev/null | grep -q .; then
        return 0
    fi

    # Check remote branches
    if git branch -r --list "*/${padded}-*" 2>/dev/null | grep -q .; then
        return 0
    fi

    # Also check without padding (1-, 12-, etc.)
    if git branch --list "${num}-*" 2>/dev/null | grep -q .; then
        return 0
    fi
    if git branch -r --list "*/${num}-*" 2>/dev/null | grep -q .; then
        return 0
    fi

    return 1
}

# Function to check if a spec directory number is already taken
is_spec_number_taken() {
    local num="$1"
    local specs_dir="$2"
    local padded=$(printf "%03d" "$((10#$num))")

    if [ -d "$specs_dir" ]; then
        # Check for directories starting with this number (padded or not)
        for dir in "$specs_dir"/*; do
            [ -d "$dir" ] || continue
            dirname=$(basename "$dir")
            if echo "$dirname" | grep -qE "^(0*)?${num}-"; then
                return 0
            fi
        done
    fi

    return 1
}

# Function to check existing branches (local and remote) and return next available number
check_existing_branches() {
    local specs_dir="$1"

    # Fetch all remotes to get latest branch info (suppress errors if no remotes)
    git fetch --all --prune 2>/dev/null || true

    # Get highest number from ALL branches (not just matching short name)
    local highest_branch=$(get_highest_from_branches)

    # Get highest number from ALL specs (not just matching short name)
    local highest_spec=$(get_highest_from_specs "$specs_dir")

    # Take the maximum of both
    local max_num=$highest_branch
    if [ "$highest_spec" -gt "$max_num" ]; then
        max_num=$highest_spec
    fi

    # Start with next number
    local next_num=$((max_num + 1))

    # Double-check: ensure this number is truly not taken (handles edge cases)
    while is_branch_number_taken "$next_num" || is_spec_number_taken "$next_num" "$specs_dir"; do
        next_num=$((next_num + 1))
    done

    echo "$next_num"
}

# Function to clean and format a branch name
clean_branch_name() {
    local name="$1"
    echo "$name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//'
}

# Update the feature manifest with a new feature entry
update_manifest() {
    local feature_id="$1"
    local feature_name="$2"
    local manifest_file="$3"
    local today=$(date +%Y-%m-%d)

    # Create manifest if it doesn't exist
    if [[ ! -f "$manifest_file" ]]; then
        mkdir -p "$(dirname "$manifest_file")"
        cat > "$manifest_file" << 'EOF'
# Feature Manifest

| ID | Name | Status | Created | Last Updated |
|----|------|--------|---------|--------------|
EOF
    fi

    # Append new feature entry
    echo "| $feature_id | $feature_name | CREATED | $today | $today |" >> "$manifest_file"
}

# Set the active feature in .speckit/active
set_active_feature() {
    local feature_full_name="$1"
    local repo_root="$2"
    local active_dir="$repo_root/.speckit"
    local active_file="$active_dir/active"

    mkdir -p "$active_dir"
    echo "$feature_full_name" > "$active_file"
}

# Find parent feature directory by ID or full name
# Returns: full feature directory name (e.g., "001-login") or empty if not found
find_parent_feature() {
    local parent_ref="$1"
    local features_dir="$2"

    # Normalize: if just a number like "001" or "1", pad it
    if [[ "$parent_ref" =~ ^[0-9]+$ ]]; then
        local padded=$(printf "%03d" "$((10#$parent_ref))")
        # Search for directories starting with this number
        for dir in "$features_dir"/*; do
            [ -d "$dir" ] || continue
            local dirname=$(basename "$dir")
            if [[ "$dirname" =~ ^${padded}- ]] || [[ "$dirname" =~ ^${parent_ref}- ]]; then
                echo "$dirname"
                return 0
            fi
        done
    else
        # Full name provided - check if directory exists
        if [ -d "$features_dir/$parent_ref" ]; then
            echo "$parent_ref"
            return 0
        fi
    fi

    return 1
}

# Check if parent feature is merged (has .merged marker)
is_feature_merged() {
    local feature_name="$1"
    local features_dir="$2"

    if [ -f "$features_dir/$feature_name/.merged" ]; then
        return 0
    fi
    return 1
}

# Get system specs affected by parent feature from .merged file
get_parent_system_specs() {
    local feature_name="$1"
    local features_dir="$2"
    local merged_file="$features_dir/$feature_name/.merged"

    if [ -f "$merged_file" ]; then
        # Extract system_specs_created and system_specs_updated from JSON
        local created=$(grep -o '"system_specs_created":\s*\[[^]]*\]' "$merged_file" 2>/dev/null | sed 's/"system_specs_created":\s*\[//;s/\]//;s/"//g;s/,/ /g' || echo "")
        local updated=$(grep -o '"system_specs_updated":\s*\[[^]]*\]' "$merged_file" 2>/dev/null | sed 's/"system_specs_updated":\s*\[//;s/\]//;s/"//g;s/,/ /g' || echo "")
        echo "$created $updated" | tr ' ' '\n' | sort -u | grep -v '^$' | tr '\n' ',' | sed 's/,$//'
    fi
}

# Update manifest to add "Extended By" link to parent feature
update_parent_extended_by() {
    local parent_name="$1"
    local child_num="$2"
    local manifest_file="$3"

    if [[ ! -f "$manifest_file" ]]; then
        return 0
    fi

    # Extract parent ID (first 3 digits)
    local parent_id=$(echo "$parent_name" | grep -o '^[0-9]\+')
    parent_id=$(printf "%03d" "$((10#$parent_id))")

    # This is a simple implementation - in production, use proper CSV/markdown parsing
    # For now, we'll note this in the manifest as a comment or separate tracking
    # Full implementation would update the "Extended By" column
    :
}

# Update manifest with extends relationship
update_manifest_with_extends() {
    local feature_id="$1"
    local feature_name="$2"
    local extends_id="$3"
    local manifest_file="$4"
    local today=$(date +%Y-%m-%d)

    # Create manifest if it doesn't exist (with new schema)
    if [[ ! -f "$manifest_file" ]]; then
        mkdir -p "$(dirname "$manifest_file")"
        cat > "$manifest_file" << 'EOF'
# Feature Manifest

| ID | Name | Status | Extends | Created | Last Updated |
|----|------|--------|---------|---------|--------------|
EOF
    fi

    # Append new feature entry with extends info
    local extends_col="${extends_id:-"-"}"
    echo "| $feature_id | $feature_name | CREATED | $extends_col | $today | $today |" >> "$manifest_file"
}

# Resolve repository root. Prefer git information when available, but fall back
# to searching for repository markers so the workflow still functions in repositories that
# were initialised with --no-git.
SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
    if [ -z "$REPO_ROOT" ]; then
        echo "Error: Could not determine repository root. Please run this script from within the repository." >&2
        exit 1
    fi
    HAS_GIT=false
fi

cd "$REPO_ROOT"

# Two-folder architecture: features/ for historical specs, system/ for living specs
SPECS_DIR="$REPO_ROOT/specs"
FEATURES_DIR="$SPECS_DIR/features"
SYSTEM_DIR="$SPECS_DIR/system"
mkdir -p "$FEATURES_DIR"
mkdir -p "$SYSTEM_DIR"

# Validate --extends parameter if provided
PARENT_FEATURE_NAME=""
PARENT_FEATURE_ID=""
PARENT_SYSTEM_SPECS=""

if [ -n "$EXTENDS_FEATURE" ]; then
    # Find the parent feature
    PARENT_FEATURE_NAME=$(find_parent_feature "$EXTENDS_FEATURE" "$FEATURES_DIR")
    if [ -z "$PARENT_FEATURE_NAME" ]; then
        echo "Error: Parent feature '$EXTENDS_FEATURE' not found in $FEATURES_DIR" >&2
        echo "Available features:" >&2
        ls -1 "$FEATURES_DIR" 2>/dev/null | head -10 >&2
        exit 1
    fi

    # Extract parent feature ID (first 3 digits)
    PARENT_FEATURE_ID=$(echo "$PARENT_FEATURE_NAME" | grep -o '^[0-9]\+')
    PARENT_FEATURE_ID=$(printf "%03d" "$((10#$PARENT_FEATURE_ID))")

    # Check if parent is merged (warning if not, but allow to proceed)
    if ! is_feature_merged "$PARENT_FEATURE_NAME" "$FEATURES_DIR"; then
        >&2 echo "[specify] Warning: Parent feature '$PARENT_FEATURE_NAME' is not yet merged."
        >&2 echo "[specify] Extension relationships are typically used for merged features."
        >&2 echo "[specify] Proceeding anyway..."
    fi

    # Get system specs affected by parent
    PARENT_SYSTEM_SPECS=$(get_parent_system_specs "$PARENT_FEATURE_NAME" "$FEATURES_DIR")
fi

# Function to generate branch name with stop word filtering and length filtering
generate_branch_name() {
    local description="$1"
    
    # Common stop words to filter out
    local stop_words="^(i|a|an|the|to|for|of|in|on|at|by|with|from|is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|should|could|can|may|might|must|shall|this|that|these|those|my|your|our|their|want|need|add|get|set)$"
    
    # Convert to lowercase and split into words
    local clean_name=$(echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/ /g')
    
    # Filter words: remove stop words and words shorter than 3 chars (unless they're uppercase acronyms in original)
    local meaningful_words=()
    for word in $clean_name; do
        # Skip empty words
        [ -z "$word" ] && continue
        
        # Keep words that are NOT stop words AND (length >= 3 OR are potential acronyms)
        if ! echo "$word" | grep -qiE "$stop_words"; then
            if [ ${#word} -ge 3 ]; then
                meaningful_words+=("$word")
            elif echo "$description" | grep -q "\b${word^^}\b"; then
                # Keep short words if they appear as uppercase in original (likely acronyms)
                meaningful_words+=("$word")
            fi
        fi
    done
    
    # If we have meaningful words, use first 3-4 of them
    if [ ${#meaningful_words[@]} -gt 0 ]; then
        local max_words=3
        if [ ${#meaningful_words[@]} -eq 4 ]; then max_words=4; fi
        
        local result=""
        local count=0
        for word in "${meaningful_words[@]}"; do
            if [ $count -ge $max_words ]; then break; fi
            if [ -n "$result" ]; then result="$result-"; fi
            result="$result$word"
            count=$((count + 1))
        done
        echo "$result"
    else
        # Fallback to original logic if no meaningful words found
        local cleaned=$(clean_branch_name "$description")
        echo "$cleaned" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//'
    fi
}

# Generate branch name
if [ -n "$SHORT_NAME" ]; then
    # Use provided short name, just clean it up
    BRANCH_SUFFIX=$(clean_branch_name "$SHORT_NAME")
else
    # Generate from description with smart filtering
    BRANCH_SUFFIX=$(generate_branch_name "$FEATURE_DESCRIPTION")
fi

# Determine branch number (check features/ subfolder for existing specs)
if [ -z "$BRANCH_NUMBER" ]; then
    if [ "$HAS_GIT" = true ]; then
        # Check existing branches on remotes
        BRANCH_NUMBER=$(check_existing_branches "$FEATURES_DIR")
    else
        # Fall back to local directory check
        HIGHEST=$(get_highest_from_specs "$FEATURES_DIR")
        BRANCH_NUMBER=$((HIGHEST + 1))
    fi
fi

# Force base-10 interpretation to prevent octal conversion (e.g., 010 → 8 in octal, but should be 10 in decimal)
FEATURE_NUM=$(printf "%03d" "$((10#$BRANCH_NUMBER))")
BRANCH_NAME="${FEATURE_NUM}-${BRANCH_SUFFIX}"

# GitHub enforces a 244-byte limit on branch names
# Validate and truncate if necessary
MAX_BRANCH_LENGTH=244
if [ ${#BRANCH_NAME} -gt $MAX_BRANCH_LENGTH ]; then
    # Calculate how much we need to trim from suffix
    # Account for: feature number (3) + hyphen (1) = 4 chars
    MAX_SUFFIX_LENGTH=$((MAX_BRANCH_LENGTH - 4))
    
    # Truncate suffix at word boundary if possible
    TRUNCATED_SUFFIX=$(echo "$BRANCH_SUFFIX" | cut -c1-$MAX_SUFFIX_LENGTH)
    # Remove trailing hyphen if truncation created one
    TRUNCATED_SUFFIX=$(echo "$TRUNCATED_SUFFIX" | sed 's/-$//')
    
    ORIGINAL_BRANCH_NAME="$BRANCH_NAME"
    BRANCH_NAME="${FEATURE_NUM}-${TRUNCATED_SUFFIX}"
    
    >&2 echo "[specify] Warning: Branch name exceeded GitHub's 244-byte limit"
    >&2 echo "[specify] Original: $ORIGINAL_BRANCH_NAME (${#ORIGINAL_BRANCH_NAME} bytes)"
    >&2 echo "[specify] Truncated to: $BRANCH_NAME (${#BRANCH_NAME} bytes)"
fi

if [ "$HAS_GIT" = true ]; then
    git checkout -b "$BRANCH_NAME"
else
    >&2 echo "[specify] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME"
fi

# Feature specs go in specs/features/ (two-folder architecture)
FEATURE_DIR="$FEATURES_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"

TEMPLATE="$REPO_ROOT/.specify/templates/spec-template.md"
SPEC_FILE="$FEATURE_DIR/spec.md"
if [ -f "$TEMPLATE" ]; then cp "$TEMPLATE" "$SPEC_FILE"; else touch "$SPEC_FILE"; fi

# If extending a feature, pre-populate the Feature Lineage section
if [ -n "$PARENT_FEATURE_NAME" ]; then
    # Determine system specs string for the table
    SYSTEM_SPECS_COL="${PARENT_SYSTEM_SPECS:-"[check parent .merged file]"}"

    # Create the Feature Lineage content to insert
    LINEAGE_CONTENT="## Feature Lineage *(for modifications of merged features)*

**Extends Feature(s)**:

| Parent Feature | Relationship | System Specs Affected |
|----------------|--------------|----------------------|
| [$PARENT_FEATURE_NAME](../$PARENT_FEATURE_NAME/spec.md) | EXTENDS | $SYSTEM_SPECS_COL |

**Relationship Types**:
- \`EXTENDS\`: Adds new capability to parent feature's functionality
- \`REFINES\`: Improves or modifies parent feature's behavior
- \`FIXES\`: Corrects issues or bugs in parent feature
- \`DEPRECATES\`: Replaces functionality from parent feature

**Context from Parent**:

<!-- Review the parent spec and summarize:
- Key design decisions that must be respected
- Constraints that carry over
- Integration points with parent's implementation
-->

[TODO: Review $PARENT_FEATURE_NAME/spec.md and summarize inherited context]

---"

    # Try to insert after ## Context section, or append if section not found
    if grep -q "^## Feature Lineage" "$SPEC_FILE"; then
        # Section exists (from template), replace it
        # Use awk to replace the section
        awk -v content="$LINEAGE_CONTENT" '
            /^## Feature Lineage/ {
                print content
                in_lineage = 1
                next
            }
            in_lineage && /^## / { in_lineage = 0 }
            !in_lineage { print }
        ' "$SPEC_FILE" > "$SPEC_FILE.tmp" && mv "$SPEC_FILE.tmp" "$SPEC_FILE"
    fi
fi

# Update feature manifest with extends relationship
MANIFEST_FILE="$FEATURES_DIR/.manifest.md"
if [ -n "$PARENT_FEATURE_ID" ]; then
    update_manifest_with_extends "$FEATURE_NUM" "$BRANCH_SUFFIX" "$PARENT_FEATURE_ID" "$MANIFEST_FILE"
else
    update_manifest "$FEATURE_NUM" "$BRANCH_SUFFIX" "$MANIFEST_FILE"
fi

# Set active feature in persistent state
set_active_feature "$BRANCH_NAME" "$REPO_ROOT"

# Set the SPECIFY_FEATURE environment variable for the current session
export SPECIFY_FEATURE="$BRANCH_NAME"

if $JSON_MODE; then
    if [ -n "$PARENT_FEATURE_NAME" ]; then
        printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","FEATURE_NUM":"%s","EXTENDS":"%s","EXTENDS_ID":"%s"}\n' \
            "$BRANCH_NAME" "$SPEC_FILE" "$FEATURE_NUM" "$PARENT_FEATURE_NAME" "$PARENT_FEATURE_ID"
    else
        printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","FEATURE_NUM":"%s"}\n' "$BRANCH_NAME" "$SPEC_FILE" "$FEATURE_NUM"
    fi
else
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "SPEC_FILE: $SPEC_FILE"
    echo "FEATURE_NUM: $FEATURE_NUM"
    if [ -n "$PARENT_FEATURE_NAME" ]; then
        echo "EXTENDS: $PARENT_FEATURE_NAME"
        echo "EXTENDS_ID: $PARENT_FEATURE_ID"
    fi
    echo "SPECIFY_FEATURE environment variable set to: $BRANCH_NAME"
fi

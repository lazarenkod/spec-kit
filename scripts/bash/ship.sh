#!/usr/bin/env bash
# Ship orchestrator: provision + deploy + verify
# Usage: ship.sh [--env <environment>] [--only <stage>] [--destroy] [--dry-run] [--cloud <provider>]

set -euo pipefail

# Source common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# =============================================================================
# CONFIGURATION
# =============================================================================

# Defaults
ENV="staging"
ONLY="all"
DESTROY=false
DRY_RUN=false
CLOUD=""
SKIP_VERIFY=false
JSON_OUTPUT=false
VERBOSE=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# =============================================================================
# ARGUMENT PARSING
# =============================================================================

print_usage() {
    cat << EOF
Usage: ship.sh [OPTIONS]

Orchestrate infrastructure provisioning, application deployment, and verification.

Options:
    --env <environment>     Target environment: local, staging, production (default: staging)
    --only <stage>          Run only specific stage: infra, deploy, verify (default: all)
    --destroy               Tear down infrastructure and deployment
    --dry-run               Show plan without executing
    --cloud <provider>      Override cloud provider: vk, yandex, gcp
    --skip-verify           Skip verification stage
    --json                  Output in JSON format
    --verbose               Verbose output
    -h, --help              Show this help message

Examples:
    ship.sh --env staging                    # Full cycle: provision -> deploy -> verify
    ship.sh --env staging --only infra       # Only provision infrastructure
    ship.sh --env staging --only deploy      # Only deploy application
    ship.sh --env staging --only verify      # Only run verification
    ship.sh --env local                      # Local docker-compose environment
    ship.sh --env staging --destroy          # Tear down everything
EOF
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENV="$2"
            shift 2
            ;;
        --only)
            ONLY="$2"
            shift 2
            ;;
        --destroy)
            DESTROY=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --cloud)
            CLOUD="$2"
            shift 2
            ;;
        --skip-verify)
            SKIP_VERIFY=true
            shift
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            print_usage
            exit 1
            ;;
    esac
done

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

log_info() {
    if [[ "$JSON_OUTPUT" != "true" ]]; then
        echo -e "${BLUE}[INFO]${NC} $1"
    fi
}

log_success() {
    if [[ "$JSON_OUTPUT" != "true" ]]; then
        echo -e "${GREEN}[SUCCESS]${NC} $1"
    fi
}

log_warning() {
    if [[ "$JSON_OUTPUT" != "true" ]]; then
        echo -e "${YELLOW}[WARNING]${NC} $1"
    fi
}

log_error() {
    if [[ "$JSON_OUTPUT" != "true" ]]; then
        echo -e "${RED}[ERROR]${NC} $1" >&2
    fi
}

log_stage() {
    if [[ "$JSON_OUTPUT" != "true" ]]; then
        echo ""
        echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${CYAN}  $1${NC}"
        echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
        echo ""
    fi
}

# Check if command exists
check_command() {
    local cmd="$1"
    if ! command -v "$cmd" &> /dev/null; then
        log_error "Required command not found: $cmd"
        return 1
    fi
}

# Get current git info
get_git_info() {
    GIT_SHA=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
    GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    FEATURE_SLUG=$(echo "$GIT_BRANCH" | sed 's/[^a-zA-Z0-9]/-/g' | tr '[:upper:]' '[:lower:]' | cut -c1-63)
    TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
}

# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

setup_environment() {
    REPO_ROOT=$(get_repo_root)
    CURRENT_BRANCH=$(get_current_branch)

    # Feature directory
    if [[ -d "$REPO_ROOT/specs/features/$CURRENT_BRANCH" ]]; then
        FEATURE_DIR="$REPO_ROOT/specs/features/$CURRENT_BRANCH"
    elif [[ -d "$REPO_ROOT/specs/$CURRENT_BRANCH" ]]; then
        FEATURE_DIR="$REPO_ROOT/specs/$CURRENT_BRANCH"
    else
        FEATURE_DIR=""
    fi

    # State directory
    STATE_DIR="$REPO_ROOT/.speckit/state/$ENV"
    mkdir -p "$STATE_DIR"

    # Get git info
    get_git_info

    # Check for configuration files
    INFRA_YAML=""
    DEPLOY_YAML=""
    VERIFY_YAML=""

    # Look in feature dir first, then project root
    for search_dir in "$FEATURE_DIR" "$REPO_ROOT"; do
        [[ -z "$search_dir" ]] && continue

        [[ -z "$INFRA_YAML" && -f "$search_dir/infra.yaml" ]] && INFRA_YAML="$search_dir/infra.yaml"
        [[ -z "$DEPLOY_YAML" && -f "$search_dir/deploy.yaml" ]] && DEPLOY_YAML="$search_dir/deploy.yaml"
        [[ -z "$VERIFY_YAML" && -f "$search_dir/verify.yaml" ]] && VERIFY_YAML="$search_dir/verify.yaml"
    done

    # Cloud provider detection
    if [[ -z "$CLOUD" && -n "$INFRA_YAML" ]]; then
        CLOUD=$(grep -E "^\s*cloud:" "$INFRA_YAML" 2>/dev/null | head -1 | awk '{print $2}' || echo "vk")
    fi
    CLOUD="${CLOUD:-vk}"

    if [[ "$VERBOSE" == "true" ]]; then
        log_info "Repository root: $REPO_ROOT"
        log_info "Feature directory: $FEATURE_DIR"
        log_info "State directory: $STATE_DIR"
        log_info "Environment: $ENV"
        log_info "Cloud provider: $CLOUD"
        log_info "Git SHA: $GIT_SHA"
        log_info "Feature slug: $FEATURE_SLUG"
    fi
}

# =============================================================================
# STAGE: PROVISION
# =============================================================================

run_provision() {
    log_stage "PROVISION: Infrastructure"

    # Skip for local environment
    if [[ "$ENV" == "local" ]]; then
        log_info "Skipping infrastructure provisioning for local environment"
        return 0
    fi

    # Check requirements
    if [[ -z "$INFRA_YAML" ]]; then
        log_warning "No infra.yaml found, skipping provision"
        return 0
    fi

    check_command "terraform" || return 1

    # Call provision script
    if [[ -f "$SCRIPT_DIR/provision.sh" ]]; then
        "$SCRIPT_DIR/provision.sh" \
            --env "$ENV" \
            --cloud "$CLOUD" \
            --config "$INFRA_YAML" \
            --state-dir "$STATE_DIR" \
            ${DRY_RUN:+--dry-run} \
            ${VERBOSE:+--verbose}
    else
        log_error "provision.sh not found"
        return 1
    fi
}

# =============================================================================
# STAGE: DEPLOY
# =============================================================================

run_deploy() {
    log_stage "DEPLOY: Application"

    if [[ -z "$DEPLOY_YAML" ]]; then
        log_warning "No deploy.yaml found, skipping deploy"
        return 0
    fi

    if [[ "$ENV" == "local" ]]; then
        check_command "docker" || return 1
        check_command "docker-compose" || check_command "docker" || return 1
    else
        check_command "kubectl" || return 1
        check_command "helm" || return 1
    fi

    # Call deploy script
    if [[ -f "$SCRIPT_DIR/deploy.sh" ]]; then
        "$SCRIPT_DIR/deploy.sh" \
            --env "$ENV" \
            --config "$DEPLOY_YAML" \
            --state-dir "$STATE_DIR" \
            --git-sha "$GIT_SHA" \
            --feature-slug "$FEATURE_SLUG" \
            ${DRY_RUN:+--dry-run} \
            ${VERBOSE:+--verbose}
    else
        log_error "deploy.sh not found"
        return 1
    fi
}

# =============================================================================
# STAGE: VERIFY
# =============================================================================

run_verify() {
    log_stage "VERIFY: Running System"

    if [[ "$SKIP_VERIFY" == "true" ]]; then
        log_info "Verification skipped (--skip-verify)"
        return 0
    fi

    # Determine base URL
    local base_url
    case "$ENV" in
        local)
            base_url="http://localhost:8080"
            ;;
        staging)
            base_url="https://${FEATURE_SLUG}.staging.example.com"
            ;;
        production)
            base_url="https://app.example.com"
            ;;
        *)
            base_url="http://localhost:8080"
            ;;
    esac

    # Call verify script
    if [[ -f "$SCRIPT_DIR/verify.sh" ]]; then
        "$SCRIPT_DIR/verify.sh" \
            --env "$ENV" \
            --base-url "$base_url" \
            --config "${VERIFY_YAML:-}" \
            --state-dir "$STATE_DIR" \
            --feature-dir "${FEATURE_DIR:-$REPO_ROOT}" \
            ${VERBOSE:+--verbose}
    else
        log_error "verify.sh not found"
        return 1
    fi
}

# =============================================================================
# STAGE: DESTROY
# =============================================================================

run_destroy() {
    log_stage "DESTROY: Tearing Down Environment"

    log_warning "This will destroy all resources in the $ENV environment!"
    read -p "Type 'yes' to confirm: " confirm

    if [[ "$confirm" != "yes" ]]; then
        log_info "Destruction cancelled"
        return 0
    fi

    # Destroy deployment first
    if [[ "$ENV" == "local" ]]; then
        log_info "Stopping local containers..."
        local compose_file="$REPO_ROOT/.speckit/local/docker-compose.yml"
        if [[ -f "$compose_file" ]]; then
            docker-compose -f "$compose_file" down -v --remove-orphans
        fi
    else
        log_info "Uninstalling Helm release..."
        local namespace="staging-$FEATURE_SLUG"
        helm uninstall app -n "$namespace" 2>/dev/null || true
        kubectl delete namespace "$namespace" 2>/dev/null || true
    fi

    # Destroy infrastructure (only feature-specific, not shared)
    if [[ "$ENV" != "local" && -n "$INFRA_YAML" ]]; then
        log_info "Note: Shared infrastructure (database, cache) is NOT destroyed"
        # terraform destroy would go here for feature-specific resources
    fi

    # Clean up state
    rm -f "$STATE_DIR/deployed-version.json"
    log_success "Environment $ENV destroyed"
}

# =============================================================================
# JSON OUTPUT
# =============================================================================

output_json() {
    local provision_status="$1"
    local deploy_status="$2"
    local verify_status="$3"

    cat << EOF
{
  "environment": "$ENV",
  "feature": "$CURRENT_BRANCH",
  "feature_slug": "$FEATURE_SLUG",
  "git_sha": "$GIT_SHA",
  "timestamp": "$TIMESTAMP",
  "stages": {
    "provision": "$provision_status",
    "deploy": "$deploy_status",
    "verify": "$verify_status"
  },
  "state_dir": "$STATE_DIR",
  "feature_dir": "$FEATURE_DIR",
  "config": {
    "infra_yaml": "$INFRA_YAML",
    "deploy_yaml": "$DEPLOY_YAML",
    "verify_yaml": "$VERIFY_YAML"
  }
}
EOF
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    setup_environment

    local provision_status="skipped"
    local deploy_status="skipped"
    local verify_status="skipped"

    # Handle destroy
    if [[ "$DESTROY" == "true" ]]; then
        run_destroy
        exit 0
    fi

    # Run stages based on --only flag
    case "$ONLY" in
        all)
            if run_provision; then
                provision_status="success"
            else
                provision_status="failed"
            fi

            if run_deploy; then
                deploy_status="success"
            else
                deploy_status="failed"
            fi

            if run_verify; then
                verify_status="success"
            else
                verify_status="failed"
            fi
            ;;
        infra)
            if run_provision; then
                provision_status="success"
            else
                provision_status="failed"
            fi
            ;;
        deploy)
            if run_deploy; then
                deploy_status="success"
            else
                deploy_status="failed"
            fi
            ;;
        verify)
            if run_verify; then
                verify_status="success"
            else
                verify_status="failed"
            fi
            ;;
        *)
            log_error "Unknown stage: $ONLY"
            exit 1
            ;;
    esac

    # Output results
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        output_json "$provision_status" "$deploy_status" "$verify_status"
    else
        echo ""
        log_stage "Ship Complete"
        echo "Environment: $ENV"
        echo "Git SHA:     $GIT_SHA"
        echo "Feature:     $FEATURE_SLUG"
        echo ""
        echo "Stages:"
        echo "  Provision: $provision_status"
        echo "  Deploy:    $deploy_status"
        echo "  Verify:    $verify_status"
        echo ""

        # Overall status
        if [[ "$provision_status" == "failed" || "$deploy_status" == "failed" || "$verify_status" == "failed" ]]; then
            log_error "Ship completed with errors"
            exit 1
        else
            log_success "Ship completed successfully"
        fi
    fi
}

main "$@"

#!/usr/bin/env bash
# mobile-staging-provision.sh - iOS Simulator and mobile staging helper
# Part of Spec Kit - https://github.com/Anthroware/spec-kit
# Note: iOS Simulator requires macOS. Android emulator uses Docker (see staging-provision.sh)
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Defaults
IOS_DEVICE="iPhone 15 Pro"
IOS_OS="17.2"
ACTION="boot"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --device)
      IOS_DEVICE="$2"
      shift 2
      ;;
    --os)
      IOS_OS="$2"
      shift 2
      ;;
    --boot)
      ACTION="boot"
      shift
      ;;
    --shutdown)
      ACTION="shutdown"
      shift
      ;;
    --status)
      ACTION="status"
      shift
      ;;
    --list)
      ACTION="list"
      shift
      ;;
    -h|--help)
      echo "Usage: mobile-staging-provision.sh [OPTIONS]"
      echo ""
      echo "iOS Simulator management for mobile testing (macOS only)"
      echo ""
      echo "Options:"
      echo "  --device <name>   iOS device name (default: iPhone 15 Pro)"
      echo "  --os <version>    iOS version (default: 17.2)"
      echo "  --boot            Boot the simulator (default action)"
      echo "  --shutdown        Shutdown the simulator"
      echo "  --status          Show simulator status"
      echo "  --list            List available simulators"
      echo "  -h, --help        Show this help"
      echo ""
      echo "Examples:"
      echo "  mobile-staging-provision.sh --boot"
      echo "  mobile-staging-provision.sh --device \"iPhone SE\" --boot"
      echo "  mobile-staging-provision.sh --shutdown"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Check if running on macOS
check_macos() {
  if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}ERROR: iOS Simulator requires macOS${NC}"
    echo "For Android testing on Linux/Windows, use:"
    echo "  staging-provision.sh --mobile"
    exit 1
  fi
}

# Check if Xcode command line tools are installed
check_xcode() {
  if ! command -v xcrun &> /dev/null; then
    echo -e "${RED}ERROR: Xcode command line tools not found${NC}"
    echo "Install with: xcode-select --install"
    exit 1
  fi
}

# Get simulator UDID by device name
get_simulator_udid() {
  local device_name="$1"
  xcrun simctl list devices -j | \
    python3 -c "
import json, sys
data = json.load(sys.stdin)
for runtime, devices in data.get('devices', {}).items():
    for device in devices:
        if device['name'] == '$device_name' and device['isAvailable']:
            print(device['udid'])
            sys.exit(0)
sys.exit(1)
" 2>/dev/null || echo ""
}

# Boot iOS Simulator
boot_simulator() {
  echo -e "${BLUE}Booting iOS Simulator: $IOS_DEVICE${NC}"

  local udid=$(get_simulator_udid "$IOS_DEVICE")

  if [ -z "$udid" ]; then
    echo -e "${RED}ERROR: Simulator '$IOS_DEVICE' not found${NC}"
    echo "Available simulators:"
    xcrun simctl list devices available | grep -E "iPhone|iPad" | head -10
    exit 1
  fi

  # Check if already booted
  local state=$(xcrun simctl list devices -j | python3 -c "
import json, sys
data = json.load(sys.stdin)
for runtime, devices in data.get('devices', {}).items():
    for device in devices:
        if device['udid'] == '$udid':
            print(device['state'])
            sys.exit(0)
" 2>/dev/null)

  if [ "$state" == "Booted" ]; then
    echo -e "${GREEN}Simulator '$IOS_DEVICE' is already booted${NC}"
    return 0
  fi

  # Boot the simulator
  xcrun simctl boot "$udid" 2>/dev/null || true

  # Wait for boot
  local waited=0
  local max_wait=60

  while [ $waited -lt $max_wait ]; do
    state=$(xcrun simctl list devices -j | python3 -c "
import json, sys
data = json.load(sys.stdin)
for runtime, devices in data.get('devices', {}).items():
    for device in devices:
        if device['udid'] == '$udid':
            print(device['state'])
            sys.exit(0)
" 2>/dev/null)

    if [ "$state" == "Booted" ]; then
      echo -e "${GREEN}Simulator '$IOS_DEVICE' booted successfully${NC}"

      # Open Simulator app
      open -a Simulator 2>/dev/null || true

      return 0
    fi

    sleep 2
    waited=$((waited + 2))
    echo -e "  ${YELLOW}Waiting for simulator to boot... (${waited}s)${NC}"
  done

  echo -e "${RED}ERROR: Simulator failed to boot within ${max_wait}s${NC}"
  return 1
}

# Shutdown iOS Simulator
shutdown_simulator() {
  echo -e "${BLUE}Shutting down iOS Simulator: $IOS_DEVICE${NC}"

  local udid=$(get_simulator_udid "$IOS_DEVICE")

  if [ -z "$udid" ]; then
    echo -e "${YELLOW}Simulator '$IOS_DEVICE' not found, nothing to shutdown${NC}"
    return 0
  fi

  xcrun simctl shutdown "$udid" 2>/dev/null || true
  echo -e "${GREEN}Simulator '$IOS_DEVICE' shutdown complete${NC}"
}

# Show simulator status
show_status() {
  echo -e "${BLUE}iOS Simulator Status${NC}"
  echo ""

  # List booted simulators
  local booted=$(xcrun simctl list devices -j | python3 -c "
import json, sys
data = json.load(sys.stdin)
booted = []
for runtime, devices in data.get('devices', {}).items():
    for device in devices:
        if device['state'] == 'Booted':
            booted.append(f\"  - {device['name']} ({device['udid'][:8]}...)\")
if booted:
    print('Booted simulators:')
    print('\\n'.join(booted))
else:
    print('No simulators currently booted')
" 2>/dev/null)

  echo "$booted"
  echo ""

  # Check if target device exists
  local udid=$(get_simulator_udid "$IOS_DEVICE")
  if [ -n "$udid" ]; then
    echo -e "${GREEN}Target device '$IOS_DEVICE' is available${NC}"
  else
    echo -e "${YELLOW}Target device '$IOS_DEVICE' not found${NC}"
  fi
}

# List available simulators
list_simulators() {
  echo -e "${BLUE}Available iOS Simulators${NC}"
  echo ""
  xcrun simctl list devices available | grep -E "iPhone|iPad"
}

# Validate QG-MOB-001 for iOS
validate_ios_gate() {
  echo -e "\n${BLUE}Validating QG-MOB-001: iOS Simulator Ready${NC}"

  local booted_count=$(xcrun simctl list devices -j | python3 -c "
import json, sys
data = json.load(sys.stdin)
count = 0
for runtime, devices in data.get('devices', {}).items():
    for device in devices:
        if device['state'] == 'Booted':
            count += 1
print(count)
" 2>/dev/null)

  if [ "$booted_count" -gt 0 ]; then
    echo -e "  ${GREEN}iOS Simulator: PASS ($booted_count booted)${NC}"
    echo -e "\n${GREEN}QG-MOB-001 (iOS): PASSED${NC}"
    return 0
  else
    echo -e "  ${RED}iOS Simulator: FAIL (no booted simulators)${NC}"
    echo -e "\n${RED}QG-MOB-001 (iOS): FAILED${NC}"
    return 1
  fi
}

# Main execution
main() {
  check_macos
  check_xcode

  case "$ACTION" in
    boot)
      boot_simulator
      validate_ios_gate
      ;;
    shutdown)
      shutdown_simulator
      ;;
    status)
      show_status
      ;;
    list)
      list_simulators
      ;;
    *)
      echo -e "${RED}Unknown action: $ACTION${NC}"
      exit 1
      ;;
  esac
}

main "$@"

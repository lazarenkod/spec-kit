#!/usr/bin/env bash
# staging-provision.sh - Provision Docker Compose staging environment for testing
# Part of Spec Kit - https://github.com/Anthroware/spec-kit
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Defaults
SERVICES="postgres,redis"
SKIP_PLAYWRIGHT=false
RESET=false
STATUS_ONLY=false
DOWN=false
JSON_OUTPUT=false
# Mobile testing defaults
MOBILE_ENABLED=false
ANDROID_ONLY=false
IOS_ONLY=false
APPIUM_ENABLED=false
EMULATOR_DEVICE="pixel_6"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --services)
      SERVICES="$2"
      shift 2
      ;;
    --skip-playwright)
      SKIP_PLAYWRIGHT=true
      shift
      ;;
    --reset)
      RESET=true
      shift
      ;;
    --status)
      STATUS_ONLY=true
      shift
      ;;
    --down)
      DOWN=true
      shift
      ;;
    --json)
      JSON_OUTPUT=true
      shift
      ;;
    --mobile)
      MOBILE_ENABLED=true
      shift
      ;;
    --android-only)
      MOBILE_ENABLED=true
      ANDROID_ONLY=true
      shift
      ;;
    --ios-only)
      MOBILE_ENABLED=true
      IOS_ONLY=true
      shift
      ;;
    --appium)
      APPIUM_ENABLED=true
      shift
      ;;
    --emulator-device)
      EMULATOR_DEVICE="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: staging-provision.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --services <list>    Services to provision (default: postgres,redis)"
      echo "  --skip-playwright    Skip Playwright container"
      echo "  --reset              Tear down and recreate all services"
      echo "  --status             Show current status only"
      echo "  --down               Stop all staging services"
      echo "  --json               Output results as JSON"
      echo ""
      echo "Mobile Testing Options:"
      echo "  --mobile             Enable Android emulator for mobile testing"
      echo "  --android-only       Only provision Android emulator (skip iOS)"
      echo "  --ios-only           Only provision iOS simulator (macOS only)"
      echo "  --appium             Include Appium server for native automation"
      echo "  --emulator-device    Android device type (default: pixel_6)"
      echo "                       Options: pixel_6, pixel_8, galaxy_s24"
      echo ""
      echo "  -h, --help           Show this help"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Detect project root
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STAGING_DIR="$PROJECT_ROOT/.speckit/staging"
STATE_DIR="$PROJECT_ROOT/.speckit/state/staging"

# Check Docker is running
check_docker() {
  if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Docker is not running${NC}"
    echo "Please start Docker Desktop and try again"
    exit 1
  fi

  # Check docker-compose (v1 or v2)
  if docker compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
  elif docker-compose --version > /dev/null 2>&1; then
    DOCKER_COMPOSE="docker-compose"
  else
    echo -e "${RED}ERROR: docker-compose not found${NC}"
    echo "Please install Docker Compose and try again"
    exit 1
  fi
}

# Create docker-compose.yaml
create_compose_file() {
  mkdir -p "$STAGING_DIR"

  cat > "$STAGING_DIR/docker-compose.yaml" << 'EOF'
version: '3.8'

services:
  test-db:
    image: postgres:16-alpine
    container_name: speckit-test-db
    ports:
      - "5433:5432"
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: test_db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test -d test_db"]
      interval: 5s
      timeout: 5s
      retries: 5
    volumes:
      - test-db-data:/var/lib/postgresql/data

  test-redis:
    image: redis:7-alpine
    container_name: speckit-test-redis
    ports:
      - "6380:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
    profiles:
      - redis

  playwright:
    image: mcr.microsoft.com/playwright:v1.40.0-jammy
    container_name: speckit-playwright
    working_dir: /app
    volumes:
      - ../..:/app
    environment:
      - CI=true
    profiles:
      - e2e
    command: ["tail", "-f", "/dev/null"]
    depends_on:
      test-db:
        condition: service_healthy

  # Mobile Testing Services
  android-emulator:
    image: budtmo/docker-android:emulator_12.0
    container_name: speckit-android-emulator
    privileged: true
    ports:
      - "5554:5554"
      - "5555:5555"
      - "5037:5037"
      - "6080:6080"
    environment:
      EMULATOR_DEVICE: "${EMULATOR_DEVICE:-pixel_6}"
      WEB_VNC: "true"
      DATAPARTITION: "2048m"
    healthcheck:
      test: ["CMD-SHELL", "adb devices | grep -q emulator || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 10
      start_period: 120s
    profiles:
      - mobile
      - android
    volumes:
      - android-avd-data:/root/.android
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2'

  appium:
    image: appium/appium:latest
    container_name: speckit-appium
    ports:
      - "4723:4723"
    environment:
      - APPIUM_ARGS=--relaxed-security
    profiles:
      - appium
    depends_on:
      android-emulator:
        condition: service_healthy

volumes:
  test-db-data:
  android-avd-data:

networks:
  default:
    name: speckit-staging
EOF

  echo -e "${GREEN}Created docker-compose.yaml${NC}"
}

# Create test-config.env
create_config_file() {
  cat > "$STAGING_DIR/test-config.env" << 'EOF'
# Auto-generated by /speckit.staging - DO NOT EDIT
# Staging environment configuration for tests

# Database
DATABASE_URL=postgresql://test:test@localhost:5433/test_db
TEST_DATABASE_HOST=localhost
TEST_DATABASE_PORT=5433
TEST_DATABASE_USER=test
TEST_DATABASE_PASSWORD=test
TEST_DATABASE_NAME=test_db

# Redis
REDIS_URL=redis://localhost:6380
TEST_REDIS_HOST=localhost
TEST_REDIS_PORT=6380

# Playwright
PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
CI=true

# Mobile Testing (Android)
ANDROID_EMULATOR_HOST=localhost
ANDROID_ADB_PORT=5555
ANDROID_VNC_PORT=6080
ANDROID_DEVICE=${EMULATOR_DEVICE:-pixel_6}

# Mobile Testing (iOS - macOS only)
IOS_SIMULATOR_DEVICE=iPhone 15 Pro
IOS_SIMULATOR_OS=17.2

# Appium Server
APPIUM_HOST=localhost
APPIUM_PORT=4723

# Test Configuration
NODE_ENV=test
LOG_LEVEL=error
EOF

  echo -e "${GREEN}Created test-config.env${NC}"
}

# Build compose profiles from services
build_profiles() {
  local profiles=""

  IFS=',' read -ra SERVICE_ARRAY <<< "$SERVICES"
  for service in "${SERVICE_ARRAY[@]}"; do
    case "$service" in
      redis)
        profiles="${profiles:+$profiles,}redis"
        ;;
      playwright)
        if [ "$SKIP_PLAYWRIGHT" = false ]; then
          profiles="${profiles:+$profiles,}e2e"
        fi
        ;;
    esac
  done

  # Add mobile profiles
  if [ "$MOBILE_ENABLED" = true ]; then
    if [ "$IOS_ONLY" = false ]; then
      profiles="${profiles:+$profiles,}mobile"
    fi
  fi

  # Add appium profile
  if [ "$APPIUM_ENABLED" = true ]; then
    profiles="${profiles:+$profiles,}appium"
  fi

  echo "$profiles"
}

# Check service health
check_health() {
  local service=$1
  local container=$2

  if docker ps --filter "name=$container" --filter "health=healthy" --format "{{.Names}}" | grep -q "$container"; then
    return 0
  fi
  return 1
}

# Wait for all services to be healthy
wait_for_healthy() {
  local max_wait=60
  local mobile_max_wait=180  # Mobile emulators need more time
  local waited=0
  local current_max_wait=$max_wait

  # Increase timeout if mobile testing is enabled
  if [ "$MOBILE_ENABLED" = true ] && [ "$IOS_ONLY" = false ]; then
    current_max_wait=$mobile_max_wait
    echo -e "${YELLOW}Mobile testing enabled - extended timeout to ${mobile_max_wait}s${NC}"
  fi

  echo -e "${BLUE}Waiting for services to be healthy...${NC}"

  while [ $waited -lt $current_max_wait ]; do
    local all_healthy=true

    # Check postgres (always required)
    if check_health "postgres" "speckit-test-db"; then
      echo -e "  ${GREEN}postgres: healthy${NC}"
    else
      all_healthy=false
    fi

    # Check redis if enabled
    if [[ "$SERVICES" == *"redis"* ]]; then
      if check_health "redis" "speckit-test-redis"; then
        echo -e "  ${GREEN}redis: healthy${NC}"
      else
        all_healthy=false
      fi
    fi

    # Check Android emulator if mobile enabled (and not iOS-only)
    if [ "$MOBILE_ENABLED" = true ] && [ "$IOS_ONLY" = false ]; then
      if check_health "android" "speckit-android-emulator"; then
        echo -e "  ${GREEN}android-emulator: healthy${NC}"
      else
        all_healthy=false
        echo -e "  ${YELLOW}android-emulator: starting (can take 2-3 minutes)...${NC}"
      fi
    fi

    # Check Appium if enabled
    if [ "$APPIUM_ENABLED" = true ]; then
      if docker ps --filter "name=speckit-appium" --format "{{.Names}}" | grep -q "speckit-appium"; then
        echo -e "  ${GREEN}appium: running${NC}"
      else
        all_healthy=false
      fi
    fi

    if [ "$all_healthy" = true ]; then
      return 0
    fi

    sleep 5
    waited=$((waited + 5))
  done

  echo -e "${RED}ERROR: Services did not become healthy within ${current_max_wait}s${NC}"
  $DOCKER_COMPOSE -f "$STAGING_DIR/docker-compose.yaml" logs
  return 1
}

# Validate QG-STAGING-001
validate_gate() {
  echo -e "\n${BLUE}Validating QG-STAGING-001: Staging Environment Ready${NC}"

  local all_passed=true
  local checks=()

  # Check PostgreSQL
  if docker exec speckit-test-db pg_isready -U test -d test_db > /dev/null 2>&1; then
    checks+=("postgres:PASS:5433")
    echo -e "  ${GREEN}PostgreSQL: PASS${NC}"
  else
    checks+=("postgres:FAIL:5433")
    echo -e "  ${RED}PostgreSQL: FAIL${NC}"
    all_passed=false
  fi

  # Check Redis if enabled
  if [[ "$SERVICES" == *"redis"* ]]; then
    if docker exec speckit-test-redis redis-cli ping 2>/dev/null | grep -q "PONG"; then
      checks+=("redis:PASS:6380")
      echo -e "  ${GREEN}Redis: PASS${NC}"
    else
      checks+=("redis:FAIL:6380")
      echo -e "  ${RED}Redis: FAIL${NC}"
      all_passed=false
    fi
  fi

  # Check Playwright if enabled
  if [[ "$SERVICES" == *"playwright"* ]] && [ "$SKIP_PLAYWRIGHT" = false ]; then
    if docker ps --filter "name=speckit-playwright" --format "{{.Names}}" | grep -q "speckit-playwright"; then
      checks+=("playwright:PASS:0")
      echo -e "  ${GREEN}Playwright: PASS${NC}"
    else
      checks+=("playwright:FAIL:0")
      echo -e "  ${RED}Playwright: FAIL${NC}"
      all_passed=false
    fi
  fi

  # Check Android emulator if mobile enabled (and not iOS-only)
  if [ "$MOBILE_ENABLED" = true ] && [ "$IOS_ONLY" = false ]; then
    if docker exec speckit-android-emulator adb devices 2>/dev/null | grep -q "emulator"; then
      checks+=("android-emulator:PASS:5555")
      echo -e "  ${GREEN}Android Emulator: PASS${NC}"
    else
      checks+=("android-emulator:FAIL:5555")
      echo -e "  ${RED}Android Emulator: FAIL${NC}"
      all_passed=false
    fi
  fi

  # Check iOS simulator if enabled (macOS only)
  if [ "$MOBILE_ENABLED" = true ] && [ "$ANDROID_ONLY" = false ]; then
    if [[ "$(uname)" == "Darwin" ]]; then
      if xcrun simctl list devices 2>/dev/null | grep -q "Booted"; then
        checks+=("ios-simulator:PASS:0")
        echo -e "  ${GREEN}iOS Simulator: PASS${NC}"
      else
        checks+=("ios-simulator:WARN:0")
        echo -e "  ${YELLOW}iOS Simulator: NOT BOOTED (run manually or use --android-only)${NC}"
        # Don't fail for iOS - it's optional unless --ios-only
        if [ "$IOS_ONLY" = true ]; then
          all_passed=false
        fi
      fi
    else
      checks+=("ios-simulator:SKIP:0")
      echo -e "  ${YELLOW}iOS Simulator: SKIPPED (macOS required)${NC}"
    fi
  fi

  # Check Appium if enabled
  if [ "$APPIUM_ENABLED" = true ]; then
    if curl -s http://localhost:4723/status 2>/dev/null | grep -q "ready"; then
      checks+=("appium:PASS:4723")
      echo -e "  ${GREEN}Appium: PASS${NC}"
    else
      checks+=("appium:FAIL:4723")
      echo -e "  ${RED}Appium: FAIL${NC}"
      all_passed=false
    fi
  fi

  if [ "$all_passed" = true ]; then
    echo -e "\n${GREEN}QG-STAGING-001: PASSED${NC}"
    # Validate mobile-specific gate if mobile enabled
    if [ "$MOBILE_ENABLED" = true ]; then
      echo -e "${GREEN}QG-MOB-001: Mobile Staging Ready - PASSED${NC}"
    fi
    return 0
  else
    echo -e "\n${RED}QG-STAGING-001: FAILED${NC}"
    return 1
  fi
}

# Write staging state
write_state() {
  mkdir -p "$STATE_DIR"

  local redis_healthy=false
  local playwright_enabled=false
  local android_enabled=false
  local ios_available=false
  local appium_enabled=false

  if [[ "$SERVICES" == *"redis"* ]]; then
    redis_healthy=true
  fi

  if [[ "$SERVICES" == *"playwright"* ]] && [ "$SKIP_PLAYWRIGHT" = false ]; then
    playwright_enabled=true
  fi

  if [ "$MOBILE_ENABLED" = true ] && [ "$IOS_ONLY" = false ]; then
    android_enabled=true
  fi

  if [[ "$(uname)" == "Darwin" ]] && [ "$MOBILE_ENABLED" = true ] && [ "$ANDROID_ONLY" = false ]; then
    ios_available=true
  fi

  if [ "$APPIUM_ENABLED" = true ]; then
    appium_enabled=true
  fi

  cat > "$STATE_DIR/staging-status.json" << EOF
{
  "status": "ready",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "services": {
    "postgres": {"port": 5433, "healthy": true},
    "redis": {"port": 6380, "healthy": $redis_healthy},
    "playwright": {"enabled": $playwright_enabled},
    "android-emulator": {"port": 5555, "enabled": $android_enabled, "device": "$EMULATOR_DEVICE"},
    "ios-simulator": {"available": $ios_available},
    "appium": {"port": 4723, "enabled": $appium_enabled}
  },
  "gate": {
    "QG-STAGING-001": "PASSED",
    "QG-MOB-001": "$( [ "$MOBILE_ENABLED" = true ] && echo "PASSED" || echo "N/A" )"
  },
  "mobile": {
    "enabled": $MOBILE_ENABLED,
    "android_only": $ANDROID_ONLY,
    "ios_only": $IOS_ONLY,
    "emulator_device": "$EMULATOR_DEVICE"
  }
}
EOF
}

# Show status
show_status() {
  echo -e "${BLUE}Staging Environment Status${NC}"
  echo ""

  if [ -f "$STAGING_DIR/docker-compose.yaml" ]; then
    $DOCKER_COMPOSE -f "$STAGING_DIR/docker-compose.yaml" ps
  else
    echo "No staging environment found. Run without --status to create one."
  fi

  if [ -f "$STATE_DIR/staging-status.json" ]; then
    echo ""
    echo -e "${BLUE}Last State:${NC}"
    cat "$STATE_DIR/staging-status.json"
  fi
}

# Stop services
stop_services() {
  echo -e "${YELLOW}Stopping staging services...${NC}"

  if [ -f "$STAGING_DIR/docker-compose.yaml" ]; then
    $DOCKER_COMPOSE -f "$STAGING_DIR/docker-compose.yaml" down -v
    echo -e "${GREEN}Staging services stopped and volumes removed${NC}"
  else
    echo "No staging environment found."
  fi

  # Clean up state
  rm -f "$STATE_DIR/staging-status.json"
}

# Output JSON
output_json() {
  cat << EOF
{
  "FEATURE_DIR": "$(pwd)",
  "PROJECT_ROOT": "$PROJECT_ROOT",
  "STAGING_DIR": "$STAGING_DIR",
  "COMPOSE_FILE": "$STAGING_DIR/docker-compose.yaml",
  "CONFIG_FILE": "$STAGING_DIR/test-config.env",
  "DATABASE_URL": "postgresql://test:test@localhost:5433/test_db",
  "REDIS_URL": "redis://localhost:6380",
  "MOBILE_ENABLED": $MOBILE_ENABLED,
  "ANDROID_EMULATOR_HOST": "localhost",
  "ANDROID_ADB_PORT": 5555,
  "ANDROID_VNC_PORT": 6080,
  "ANDROID_DEVICE": "$EMULATOR_DEVICE",
  "APPIUM_HOST": "localhost",
  "APPIUM_PORT": 4723,
  "APPIUM_ENABLED": $APPIUM_ENABLED
}
EOF
}

# Main execution
main() {
  check_docker

  # JSON output mode
  if [ "$JSON_OUTPUT" = true ]; then
    output_json
    exit 0
  fi

  # Status only
  if [ "$STATUS_ONLY" = true ]; then
    show_status
    exit 0
  fi

  # Stop services
  if [ "$DOWN" = true ]; then
    stop_services
    exit 0
  fi

  echo -e "${BLUE}Provisioning Staging Environment${NC}"
  echo ""

  # Reset if requested
  if [ "$RESET" = true ]; then
    echo -e "${YELLOW}Resetting staging environment...${NC}"
    stop_services
  fi

  # Create configuration files
  create_compose_file
  create_config_file

  # Build profiles
  COMPOSE_PROFILES=$(build_profiles)

  # Start services
  echo -e "\n${BLUE}Starting services...${NC}"
  if [ -n "$COMPOSE_PROFILES" ]; then
    COMPOSE_PROFILES=$COMPOSE_PROFILES $DOCKER_COMPOSE -f "$STAGING_DIR/docker-compose.yaml" up -d
  else
    $DOCKER_COMPOSE -f "$STAGING_DIR/docker-compose.yaml" up -d
  fi

  # Wait for health
  if ! wait_for_healthy; then
    exit 1
  fi

  # Validate gate
  if ! validate_gate; then
    exit 1
  fi

  # Write state
  write_state

  # Success summary
  echo ""
  echo -e "${GREEN}========================================${NC}"
  echo -e "${GREEN}Staging Environment Ready${NC}"
  echo -e "${GREEN}========================================${NC}"
  echo ""
  echo "Configuration files:"
  echo "  - Docker Compose: $STAGING_DIR/docker-compose.yaml"
  echo "  - Test Config:    $STAGING_DIR/test-config.env"
  echo ""
  echo "Usage:"
  echo "  source $STAGING_DIR/test-config.env"
  echo "  npm test"
  echo ""

  # Mobile testing info
  if [ "$MOBILE_ENABLED" = true ]; then
    echo -e "${BLUE}Mobile Testing:${NC}"
    if [ "$IOS_ONLY" = false ]; then
      echo "  - Android Emulator: localhost:5555 (ADB), localhost:6080 (VNC)"
      echo "  - Device: $EMULATOR_DEVICE"
    fi
    if [ "$ANDROID_ONLY" = false ]; then
      if [[ "$(uname)" == "Darwin" ]]; then
        echo "  - iOS Simulator: Use 'xcrun simctl boot \"iPhone 15 Pro\"' to start"
      else
        echo "  - iOS Simulator: Skipped (requires macOS)"
      fi
    fi
    if [ "$APPIUM_ENABLED" = true ]; then
      echo "  - Appium Server: localhost:4723"
    fi
    echo ""
    echo "Mobile Test Commands:"
    echo "  flutter test integration_test/           # Flutter"
    echo "  detox test --configuration android       # React Native (Detox)"
    echo "  maestro test .maestro/                   # React Native (Maestro)"
    echo ""
  fi

  echo "Commands:"
  echo "  /speckit.staging --status    Check status"
  echo "  /speckit.staging --down      Stop services"
  echo "  /speckit.staging --reset     Recreate services"
  if [ "$MOBILE_ENABLED" = false ]; then
    echo "  /speckit.staging --mobile    Enable mobile testing"
  fi
  echo ""
  echo -e "${GREEN}Next: Run /speckit.implement to start TDD implementation${NC}"
}

main "$@"

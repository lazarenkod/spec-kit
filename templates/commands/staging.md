---
description: Provision Docker Compose staging environment before implementation
persona: devops-agent
handoff:
  requires: tasks.md  # Must have tasks before staging
  template: templates/handoff-template.md
handoffs:
  - label: Start Implementation
    agent: speckit.implement
    prompt: |
      Staging environment is ready. Start TDD implementation:
      - Wave 2: Create failing tests first
      - Wave 3: Implement to make tests pass
    auto: true
    condition:
      - "All staging services pass health checks"
      - "QG-STAGING-001 passed"
    gates:
      - name: "Staging Ready Gate"
        check: "docker-compose services are healthy"
        block_if: "Any service failed health check"
        message: "Fix staging services before implementation"
pre_gates:
  - name: "Tasks Exist Gate"
    check: "tasks.md exists in FEATURE_DIR"
    block_if: "No tasks.md found"
    message: "Run /speckit.tasks first to generate task breakdown"
  - name: "Docker Available Gate"
    check: "docker and docker-compose commands available"
    block_if: "Docker not installed or not running"
    message: "Install Docker Desktop and ensure it is running"
scripts:
  sh: scripts/bash/staging-provision.sh
  ps: scripts/powershell/staging-provision.ps1
flags:
  - name: --thinking-depth
    type: choice
    choices: [standard, ultrathink]
    default: standard
    description: |
      Thinking budget control:
      - standard: 2K budget, fast provision (~$0.03) [RECOMMENDED]
      - ultrathink: 8K budget, deep validation (~$0.12)
claude_code:
  model: haiku
  reasoning_mode: standard
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 2000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 4000
        max_parallel: 3
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 2000
        max_parallel: 6
        batch_delay: 1500
        wave_overlap_threshold: 0.65
      ultrathink:
        thinking_budget: 8000
        max_parallel: 4
        batch_delay: 3000
        wave_overlap_threshold: 0.60
        cost_multiplier: 4.0

  depth_defaults:
    standard:
      thinking_budget: 2000
      timeout: 30
    ultrathink:
      thinking_budget: 8000
      additional_analysis: [docker-health-validator, service-dependency-checker]
      timeout: 60

  user_tier_fallback:
    enabled: true
    rules:
      - condition: "user_tier != 'max' AND requested_depth == 'ultrathink'"
        fallback_depth: "standard"
        fallback_thinking: 2000
        warning_message: |
          ⚠️ **Ultrathink mode requires Claude Code Max tier** (8K thinking budget).
          Auto-downgrading to **Standard** mode (2K budget).

  cost_breakdown:
    standard: {cost: $0.03, time: "15-30s"}
    ultrathink: {cost: $0.12, time: "30-60s"}

  subagents:
    - role: docker-provisioner
      role_group: INFRA
      parallel: false
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        Provision Docker Compose staging environment for testing.

        Tasks:
        1. Check Docker is running
        2. Generate docker-compose.yaml with test services
        3. Start services and wait for health checks
        4. Generate test-config.env with connection strings
        5. Validate QG-STAGING-001

        Output:
        - .speckit/staging/docker-compose.yaml
        - .speckit/staging/test-config.env
        - Health check results

    # Wave 3: Analytics Services Configuration (conditional)
    - role: analytics-services-configurator
      role_group: INFRA
      parallel: false
      depends_on: [docker-provisioner]
      priority: 35
      model_override: haiku
      prompt: |
        CONDITIONAL: Only execute if analytics enabled in constitution.

        1. Read /memory/constitution.md § Project Settings
        2. Check analytics_enabled, analytics_types, analytics_provider
        3. IF analytics_enabled == true:
           a. IF "web" in analytics_types:
              - Include Umami service (always from observability-stack.md)
           b. IF "product" in analytics_types AND analytics_provider == "posthog":
              - Include PostHog services (posthog, posthog-worker, posthog-postgres, posthog-redis)
              - Add to docker-compose.yml from observability-stack.md
           c. IF "product" in analytics_types AND analytics_provider in ["mixpanel", "amplitude"]:
              - Skip Docker services (cloud-only providers use SDK)
           d. Verify health checks pass for included services
        4. IF analytics_enabled == false:
           Skip all analytics services

        Output: docker-compose.yml with conditional analytics services
---

## User Input

```text
$ARGUMENTS
```

Parse arguments for:
- `--services <list>`: Override default services (postgres,redis,playwright). Comma-separated.
- `--skip-playwright`: Skip Playwright container (useful for unit-test-only features)
- `--reset`: Tear down and recreate all services
- `--status`: Show current staging status without changes
- `--down`: Stop all staging services

**Mobile Testing Options:**
- `--mobile`: Enable Android emulator for mobile app testing
- `--android-only`: Only provision Android emulator (skip iOS simulator)
- `--ios-only`: Only provision iOS simulator (macOS only, skip Android)
- `--appium`: Include Appium server for native automation
- `--emulator-device <name>`: Android device type (default: pixel_6). Options: pixel_6, pixel_8, galaxy_s24

## Outline

### Phase 0: Prerequisites Check

1. Run `{SCRIPT} --json` from repo root and parse:
   - `FEATURE_DIR`: Current feature directory
   - `PROJECT_ROOT`: Repository root

2. Verify prerequisites:
   ```bash
   # Check Docker is available and running
   docker info > /dev/null 2>&1 || {
     echo "ERROR: Docker is not running"
     exit 1
   }

   # Check docker-compose is available
   docker-compose --version > /dev/null 2>&1 || docker compose version > /dev/null 2>&1 || {
     echo "ERROR: docker-compose not found"
     exit 1
   }
   ```

3. Load feature context:
   - **IF EXISTS**: Read tasks.md for test requirements
   - **IF EXISTS**: Read spec.md for infrastructure hints (database type, cache needs)

### Phase 1: Service Configuration

1. **Detect required services from spec.md and tasks.md:**
   ```text
   services = ["postgres"]  # Default database

   IF spec.md mentions "Redis" OR "cache" OR "session":
     services.append("redis")

   IF tasks.md has "[TEST:AS-xxx]" with type="e2e" OR type="playwright":
     services.append("playwright")

   # Mobile platform detection
   IF constitution.md OR spec.md mentions "mobile" OR "iOS" OR "Android":
     mobile_enabled = true

   IF pubspec.yaml exists (Flutter):
     mobile_enabled = true

   IF package.json contains "react-native":
     mobile_enabled = true

   IF build.gradle.kts contains kotlin("multiplatform"):
     mobile_enabled = true

   IF --mobile specified:
     mobile_enabled = true

   IF --services specified:
     services = parse_comma_separated(--services)

   IF --skip-playwright:
     services.remove("playwright")
   ```

2. **Generate docker-compose.yaml:**
   ```yaml
   # .speckit/staging/docker-compose.yaml
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
         - ${PROJECT_ROOT:-.}:/app
       environment:
         - CI=true
       profiles:
         - e2e
       depends_on:
         test-db:
           condition: service_healthy

   volumes:
     test-db-data:
     android-avd-data:

   networks:
     default:
       name: speckit-staging
   ```

   **Mobile services (added with `--mobile` flag):**
   ```yaml
     # Android Emulator Container
     android-emulator:
       image: budtmo/docker-android:emulator_12.0
       container_name: speckit-android-emulator
       privileged: true
       ports:
         - "5554:5554"   # ADB
         - "5555:5555"   # ADB wireless
         - "6080:6080"   # VNC/noVNC web interface
       environment:
         EMULATOR_DEVICE: "${EMULATOR_DEVICE:-pixel_6}"
         WEB_VNC: "true"
       healthcheck:
         test: ["CMD-SHELL", "adb devices | grep -q emulator"]
         interval: 30s
         timeout: 10s
         retries: 10
         start_period: 120s
       profiles:
         - mobile

     # Appium Server (optional, with --appium flag)
     appium:
       image: appium/appium:latest
       container_name: speckit-appium
       ports:
         - "4723:4723"
       profiles:
         - appium
   ```

   **Desktop services (added with `--electron` or `--tauri` flag):**
   ```yaml
     # Playwright Electron Container
     playwright-electron:
       image: mcr.microsoft.com/playwright:v1.40.0-jammy
       container_name: speckit-playwright-electron
       working_dir: /app
       environment:
         - DISPLAY=:99
         - PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
         - CI=true
       volumes:
         - ${PROJECT_ROOT:-.}:/app
         - playwright-data:/ms-playwright
       healthcheck:
         test: ["CMD-SHELL", "npx playwright --version"]
         interval: 30s
         timeout: 10s
         retries: 3
       profiles:
         - electron

     # Tauri WebDriver (requires native setup)
     # Note: Tauri WebDriver runs on host, not in Docker
     # This is a placeholder for future Docker support
   ```

3. **Generate test-config.env:**
   ```env
   # .speckit/staging/test-config.env
   # Auto-generated by /speckit.staging - DO NOT EDIT

   # Database
   DATABASE_URL=postgresql://test:test@localhost:5433/test_db
   TEST_DATABASE_HOST=localhost
   TEST_DATABASE_PORT=5433
   TEST_DATABASE_USER=test
   TEST_DATABASE_PASSWORD=test
   TEST_DATABASE_NAME=test_db

   # Redis (if enabled)
   REDIS_URL=redis://localhost:6380
   TEST_REDIS_HOST=localhost
   TEST_REDIS_PORT=6380

   # Playwright (if enabled)
   PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
   CI=true

   # Mobile Testing - Android (if --mobile enabled)
   ANDROID_EMULATOR_HOST=localhost
   ANDROID_ADB_PORT=5555
   ANDROID_VNC_PORT=6080
   ANDROID_DEVICE=pixel_6

   # Mobile Testing - iOS (macOS only)
   IOS_SIMULATOR_DEVICE=iPhone 15 Pro
   IOS_SIMULATOR_OS=17.2

   # Appium Server (if --appium enabled)
   APPIUM_HOST=localhost
   APPIUM_PORT=4723

   # Desktop Testing - Electron (if --electron enabled)
   ELECTRON_ENABLE_LOGGING=true
   PLAYWRIGHT_ELECTRON=true

   # Desktop Testing - Tauri (if --tauri enabled)
   # Note: Tauri WebDriver runs on host, native setup required
   TAURI_WEBDRIVER_PORT=4444

   # Test Configuration
   NODE_ENV=test
   LOG_LEVEL=error
   ```

### Phase 2: Service Provisioning

1. **Handle --down flag:**
   ```bash
   IF --down:
     docker-compose -f .speckit/staging/docker-compose.yaml down -v
     echo "Staging services stopped and volumes removed"
     EXIT 0
   ```

2. **Handle --reset flag:**
   ```bash
   IF --reset:
     docker-compose -f .speckit/staging/docker-compose.yaml down -v
     # Continue to start fresh
   ```

3. **Handle --status flag:**
   ```bash
   IF --status:
     docker-compose -f .speckit/staging/docker-compose.yaml ps
     EXIT 0
   ```

4. **Start services with appropriate profiles:**
   ```bash
   COMPOSE_PROFILES=""

   IF "redis" in services:
     COMPOSE_PROFILES="${COMPOSE_PROFILES},redis"

   IF "playwright" in services:
     COMPOSE_PROFILES="${COMPOSE_PROFILES},e2e"

   # Remove leading comma
   COMPOSE_PROFILES=${COMPOSE_PROFILES#,}

   # Start services
   COMPOSE_PROFILES=$COMPOSE_PROFILES docker-compose \
     -f .speckit/staging/docker-compose.yaml \
     up -d --wait
   ```

5. **Wait for health checks:**
   ```bash
   echo "Waiting for services to be healthy..."

   MAX_WAIT=60
   WAITED=0

   while [ $WAITED -lt $MAX_WAIT ]; do
     ALL_HEALTHY=true

     # Check each service
     for service in test-db test-redis; do
       if docker ps --filter "name=speckit-$service" --filter "health=healthy" | grep -q $service; then
         echo "  $service: healthy"
       else
         ALL_HEALTHY=false
       fi
     done

     if $ALL_HEALTHY; then
       break
     fi

     sleep 2
     WAITED=$((WAITED + 2))
   done

   if [ $WAITED -ge $MAX_WAIT ]; then
     echo "ERROR: Services did not become healthy within ${MAX_WAIT}s"
     docker-compose -f .speckit/staging/docker-compose.yaml logs
     exit 1
   fi
   ```

### Phase 3: Analytics Services Configuration (Conditional)

**Condition**: Only execute if `analytics_enabled == true` in constitution

**Purpose**: Conditionally include analytics services in Docker Compose stack based on project configuration.

#### Decision Tree

```text
IF analytics_enabled == false:
  → Skip all analytics services

IF analytics_enabled == true:
  IF "web" in analytics_types:
    → Include Umami service (port 3002)

  IF "product" in analytics_types:
    IF analytics_provider == "posthog":
      → Include PostHog stack:
        - posthog-postgres (port 5433)
        - posthog-redis (port 6380)
        - posthog (port 8001)
        - posthog-worker
    ELSE IF analytics_provider in ["mixpanel", "amplitude"]:
      → Skip Docker services (cloud-only)
      → Note: Use SDK with API key
```

#### PostHog Stack (Self-Hosted)

When `analytics_provider == "posthog"`, include these services from `templates/shared/observability-stack.md`:

| Service | Port | Purpose | Health Check |
|---------|------|---------|--------------|
| posthog-postgres | 5433 | Database for events | PostgreSQL ready |
| posthog-redis | 6380 | Cache for queries | Redis ping |
| posthog | 8001 | Web UI + API | `/_health` endpoint |
| posthog-worker | N/A | Background jobs | N/A |

**Environment Variables**:
```bash
POSTHOG_SECRET_KEY=random-secret-key-change-in-production
```

#### Health Check Validation

After provisioning, verify:
```bash
# Umami (if web analytics enabled)
curl -f http://localhost:3002/_health

# PostHog (if product analytics + self-hosted)
curl -f http://localhost:8001/_health
```

#### Cloud Providers (Mixpanel / Amplitude)

For cloud providers, no Docker services are needed. Instead:

1. **Set environment variables**:
   ```bash
   # Mixpanel
   MIXPANEL_TOKEN=your_project_token

   # Amplitude
   AMPLITUDE_API_KEY=your_api_key
   ```

2. **Initialize SDK in code** (see `templates/shared/analytics/event-tracking-patterns.md`)

3. **No local infrastructure** - all events sent to cloud endpoints

### Phase 4: Quality Gate Validation

1. **Validate QG-STAGING-001:**
   ```text
   GATE: QG-STAGING-001 - Staging Environment Ready

   checks = []

   # Check PostgreSQL
   result = docker exec speckit-test-db pg_isready -U test -d test_db
   checks.append({
     service: "postgres",
     status: result.exit_code == 0 ? "PASS" : "FAIL",
     port: 5433
   })

   # Check Redis (if enabled)
   IF "redis" in services:
     result = docker exec speckit-test-redis redis-cli ping
     checks.append({
       service: "redis",
       status: result.output == "PONG" ? "PASS" : "FAIL",
       port: 6380
     })

   # Check Playwright (if enabled)
   IF "playwright" in services:
     result = docker exec speckit-playwright npx playwright --version
     checks.append({
       service: "playwright",
       status: result.exit_code == 0 ? "PASS" : "FAIL"
     })

   # Gate verdict
   all_passed = all(c.status == "PASS" for c in checks)

   IF NOT all_passed:
     LOG "QG-STAGING-001: FAILED"
     FOR check IN checks WHERE check.status == "FAIL":
       LOG f"  - {check.service}: FAILED"
     EXIT 1

   LOG "QG-STAGING-001: PASSED"
   ```

2. **Write staging state:**
   ```bash
   mkdir -p .speckit/state/staging

   cat > .speckit/state/staging/staging-status.json << EOF
   {
     "status": "ready",
     "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
     "services": {
       "postgres": {"port": 5433, "healthy": true},
       "redis": {"port": 6380, "healthy": true},
       "playwright": {"enabled": true}
     },
     "gate": {
       "QG-STAGING-001": "PASSED"
     }
   }
   EOF
   ```

---

## Output Summary

After successful provisioning:

```markdown
## Staging Environment Ready

**Status**: All services healthy
**Quality Gate**: QG-STAGING-001 PASSED

### Services

| Service | Container | Port | Status |
|---------|-----------|------|--------|
| PostgreSQL | speckit-test-db | 5433 | Healthy |
| Redis | speckit-test-redis | 6380 | Healthy |
| Playwright | speckit-playwright | - | Ready |
| Android Emulator | speckit-android-emulator | 5555 (ADB), 6080 (VNC) | Healthy (if --mobile) |
| Appium | speckit-appium | 4723 | Ready (if --appium) |
| iOS Simulator | - | - | Booted (macOS only) |
| Umami | speckit-umami | 3002 | Healthy (if web analytics) |
| PostHog | speckit-posthog | 8001 | Healthy (if product analytics + self-hosted) |
| PostHog PostgreSQL | speckit-posthog-postgres | 5433 | Healthy (if PostHog) |
| PostHog Redis | speckit-posthog-redis | 6380 | Healthy (if PostHog) |
| PostHog Worker | speckit-posthog-worker | - | Ready (if PostHog) |

### Configuration Files

- Docker Compose: `.speckit/staging/docker-compose.yaml`
- Test Config: `.speckit/staging/test-config.env`

### Usage

Load environment variables in your tests:
```bash
source .speckit/staging/test-config.env
npm test
```

Or with dotenv:
```javascript
require('dotenv').config({ path: '.speckit/staging/test-config.env' })
```

### Commands

- Check status: `/speckit.staging --status`
- Stop services: `/speckit.staging --down`
- Reset (recreate): `/speckit.staging --reset`

**Next Step**: Run `/speckit.implement` to start TDD implementation
```

---

## Self-Review

Before completing, verify:

1. **Docker State**:
   - [ ] All containers are running
   - [ ] All health checks pass
   - [ ] Ports are not conflicting with other services

2. **Configuration**:
   - [ ] docker-compose.yaml is valid
   - [ ] test-config.env has correct connection strings
   - [ ] Volumes are created for data persistence

3. **Quality Gates**:
   - [ ] QG-STAGING-001 passed
   - [ ] staging-status.json written

4. **Cleanup Info**:
   - [ ] User informed how to stop services
   - [ ] User informed about port mappings

**If any check fails, report the issue and suggest remediation steps.**

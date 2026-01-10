# verify-prerequisites.ps1 - Check prerequisites for /speckit.verify command
#
# Checks:
# 1. Implementation complete (all tasks done)
# 2. Staging environment available (Docker or remote URL)
# 3. Test framework ready (test command runs)
#
# Exit codes:
# 0 - All prerequisites met
# 1 - One or more prerequisites failed

param()

$ErrorActionPreference = "Continue"

# Counters
$script:PassCount = 0
$script:FailCount = 0

# Helper functions
function Write-Pass {
    param([string]$Message)
    Write-Host "✅ PASS: $Message" -ForegroundColor Green
    $script:PassCount++
}

function Write-Fail {
    param([string]$Message)
    Write-Host "❌ FAIL: $Message" -ForegroundColor Red
    $script:FailCount++
}

function Write-Warn {
    param([string]$Message)
    Write-Host "⚠️  WARN: $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message"
}

# ============================================================================
# CHECK 1: Implementation Complete (tasks.md)
# ============================================================================
function Test-ImplementationComplete {
    Write-Info "Checking if implementation is complete..."

    # Find tasks.md in specs/ directory
    $TasksFile = Get-ChildItem -Path "specs" -Filter "tasks.md" -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1

    if (-not $TasksFile) {
        Write-Fail "tasks.md not found in specs/ directory"
        Write-Host "   Run /speckit.implement first"
        return $false
    }

    $TasksContent = Get-Content $TasksFile.FullName -Raw

    # Count tasks by status
    $TotalTasks = ([regex]::Matches($TasksContent, "^- \[.\] T\d+", [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
    $CompletedTasks = ([regex]::Matches($TasksContent, "^- \[x\] T\d+", [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
    $SkippedTasks = ([regex]::Matches($TasksContent, "^- \[~\] T\d+", [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
    $InProgressTasks = ([regex]::Matches($TasksContent, "^- \[>\] T\d+", [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
    $PendingTasks = ([regex]::Matches($TasksContent, "^- \[ \] T\d+", [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count

    $DoneTasks = $CompletedTasks + $SkippedTasks

    if ($TotalTasks -eq 0) {
        Write-Fail "No tasks found in $($TasksFile.Name)"
        return $false
    }

    if ($InProgressTasks -gt 0) {
        Write-Fail "Implementation not complete: $InProgressTasks tasks in progress"
        Write-Host "   Complete all tasks before verification"
        return $false
    }

    if ($PendingTasks -gt 0) {
        Write-Fail "Implementation not complete: $PendingTasks tasks pending"
        Write-Host "   Complete all tasks before verification"
        return $false
    }

    Write-Pass "Implementation complete ($DoneTasks/$TotalTasks tasks done)"
    return $true
}

# ============================================================================
# CHECK 2: Staging Environment Available
# ============================================================================
function Test-StagingAvailable {
    Write-Info "Checking if staging environment is available..."

    # Check for remote staging URL in environment
    $StagingUrl = $env:STAGING_URL
    if ($StagingUrl) {
        try {
            $response = Invoke-WebRequest -Uri $StagingUrl -Method Head -TimeoutSec 5 -ErrorAction Stop
            Write-Pass "Remote staging URL accessible: $StagingUrl"
            return $true
        }
        catch {
            Write-Warn "Remote staging URL not accessible: $StagingUrl"
        }
    }

    # Check for Docker Compose staging
    $ComposeFile = $null
    if (Test-Path ".speckit/staging/docker-compose.yaml") {
        $ComposeFile = ".speckit/staging/docker-compose.yaml"
    }
    elseif (Test-Path ".speckit/staging/docker-compose.yml") {
        $ComposeFile = ".speckit/staging/docker-compose.yml"
    }

    if ($ComposeFile) {
        # Check if Docker is available
        $dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
        if (-not $dockerCmd) {
            Write-Fail "Docker not found (required for local staging)"
            Write-Host "   Install Docker or set STAGING_URL environment variable"
            return $false
        }

        # Check for docker-compose or docker compose
        $dockerComposeCmd = Get-Command docker-compose -ErrorAction SilentlyContinue
        if (-not $dockerComposeCmd) {
            # Try docker compose (V2)
            try {
                docker compose version | Out-Null
                $ComposeCmd = "docker compose"
            }
            catch {
                Write-Fail "docker-compose not found"
                Write-Host "   Install docker-compose or set STAGING_URL environment variable"
                return $false
            }
        }
        else {
            $ComposeCmd = "docker-compose"
        }

        # Check if services are running
        $runningServices = & $ComposeCmd -f $ComposeFile ps --services --filter "status=running" 2>$null
        $serviceCount = ($runningServices | Measure-Object).Count

        if ($serviceCount -eq 0) {
            Write-Fail "Staging services not running"
            Write-Host "   Run: /speckit.staging or manually start services"
            return $false
        }

        # Check health of key services
        $Unhealthy = 0

        # Check postgres (test-db)
        $testDbRunning = & $ComposeCmd -f $ComposeFile ps test-db 2>$null | Select-String "running"
        if ($testDbRunning) {
            $containerId = docker ps -q -f "name=test-db"
            if ($containerId) {
                $pgReady = docker exec $containerId pg_isready 2>$null
                if (-not $pgReady) {
                    Write-Warn "PostgreSQL (test-db) not ready"
                    $Unhealthy++
                }
            }
        }

        # Check redis (test-redis)
        $testRedisRunning = & $ComposeCmd -f $ComposeFile ps test-redis 2>$null | Select-String "running"
        if ($testRedisRunning) {
            $containerId = docker ps -q -f "name=test-redis"
            if ($containerId) {
                $redisPing = docker exec $containerId redis-cli ping 2>$null
                if ($redisPing -ne "PONG") {
                    Write-Warn "Redis (test-redis) not ready"
                    $Unhealthy++
                }
            }
        }

        if ($Unhealthy -gt 0) {
            Write-Fail "Staging services unhealthy ($Unhealthy services)"
            Write-Host "   Wait for services to become healthy or restart them"
            return $false
        }

        Write-Pass "Local staging available ($serviceCount services healthy)"
        return $true
    }

    # Check for localhost application
    $ports = @(3000, 8000, 8080, 5000)
    foreach ($port in $ports) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:$port" -Method Head -TimeoutSec 2 -ErrorAction Stop
            Write-Pass "Application running on localhost:$port"
            return $true
        }
        catch {
            # Continue to next port
        }
    }

    Write-Fail "No staging environment found"
    Write-Host "   Options:"
    Write-Host "   1. Run /speckit.staging to provision Docker staging"
    Write-Host "   2. Start your application locally"
    Write-Host "   3. Set STAGING_URL environment variable to remote staging"
    return $false
}

# ============================================================================
# CHECK 3: Test Framework Ready
# ============================================================================
function Test-TestFrameworkReady {
    Write-Info "Checking if test framework is ready..."

    # Detect test framework from common files
    $TestCmd = $null
    $Framework = $null

    # Node.js / TypeScript
    if (Test-Path "package.json") {
        $packageJson = Get-Content "package.json" -Raw
        if ($packageJson -match '"jest"') {
            $TestCmd = "npm test -- --passWithNoTests"
            $Framework = "Jest"
        }
        elseif ($packageJson -match '"vitest"') {
            $TestCmd = "npm test"
            $Framework = "Vitest"
        }
        elseif ($packageJson -match '"mocha"') {
            $TestCmd = "npm test"
            $Framework = "Mocha"
        }
        elseif ($packageJson -match '"test":') {
            $TestCmd = "npm test"
            $Framework = "npm test"
        }
    }

    # Python
    if ((Test-Path "pyproject.toml") -or (Test-Path "pytest.ini") -or (Test-Path "setup.py")) {
        $pytestCmd = Get-Command pytest -ErrorAction SilentlyContinue
        if ($pytestCmd) {
            $TestCmd = "pytest --collect-only"
            $Framework = "pytest"
        }
        elseif (Test-Path "pyproject.toml") {
            $pyprojectContent = Get-Content "pyproject.toml" -Raw
            if ($pyprojectContent -match "pytest") {
                $TestCmd = "python -m pytest --collect-only"
                $Framework = "pytest"
            }
        }
    }

    # Go
    if (Test-Path "go.mod") {
        $TestCmd = "go test ./... -count=0"
        $Framework = "go test"
    }

    # Rust
    if (Test-Path "Cargo.toml") {
        $TestCmd = "cargo test --no-run"
        $Framework = "cargo test"
    }

    if (-not $TestCmd) {
        Write-Fail "Test framework not detected"
        Write-Host "   Install a test framework (Jest, pytest, etc.)"
        Write-Host "   See: memory/domains/test-framework-registry.md"
        return $false
    }

    # Run test command to verify it works
    Write-Info "Testing framework: $Framework"
    try {
        Invoke-Expression "$TestCmd 2>&1 | Out-Null"
        if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq $null) {
            Write-Pass "Test framework ready ($Framework)"
            return $true
        }
        else {
            Write-Fail "Test command failed: $TestCmd"
            Write-Host "   Fix test framework configuration"
            return $false
        }
    }
    catch {
        Write-Fail "Test command failed: $TestCmd"
        Write-Host "   Fix test framework configuration"
        return $false
    }
}

# ============================================================================
# MAIN
# ============================================================================
function Main {
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host "Verification Prerequisites Check"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host ""

    # Run all checks
    Test-ImplementationComplete | Out-Null
    Write-Host ""
    Test-StagingAvailable | Out-Null
    Write-Host ""
    Test-TestFrameworkReady | Out-Null

    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host "Summary: $script:PassCount passed, $script:FailCount failed"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if ($script:FailCount -gt 0) {
        Write-Host ""
        Write-Host "Prerequisites not met. Cannot run verification." -ForegroundColor Red
        exit 1
    }
    else {
        Write-Host ""
        Write-Host "All prerequisites met. Ready for verification." -ForegroundColor Green
        exit 0
    }
}

Main

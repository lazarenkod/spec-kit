#!/usr/bin/env pwsh
# Create or return path to concept.md for capturing full project concept
[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$Help,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ProjectDescription
)
$ErrorActionPreference = 'Stop'

# Show help if requested
if ($Help) {
    Write-Host "Usage: ./create-concept.ps1 [-Json] [project description]"
    Write-Host ""
    Write-Host "Creates or returns path to specs/concept.md for capturing full project concept."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Json    Output in JSON format"
    Write-Host "  -Help    Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  ./create-concept.ps1 'Task management app for teams'"
    Write-Host "  ./create-concept.ps1 -Json 'E-commerce platform'"
    exit 0
}

$projectDesc = if ($ProjectDescription) { ($ProjectDescription -join ' ').Trim() } else { '' }

# Find repository root
function Find-RepositoryRoot {
    param(
        [string]$StartDir,
        [string[]]$Markers = @('.git', '.specify')
    )
    $current = Resolve-Path $StartDir
    while ($true) {
        foreach ($marker in $Markers) {
            if (Test-Path (Join-Path $current $marker)) {
                return $current
            }
        }
        $parent = Split-Path $current -Parent
        if ($parent -eq $current) {
            return $null
        }
        $current = $parent
    }
}

# Resolve repository root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = $null

try {
    $gitRoot = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0 -and $gitRoot) {
        $repoRoot = $gitRoot
    }
} catch {
    # Git not available or not in repo
}

if (-not $repoRoot) {
    $repoRoot = Find-RepositoryRoot -StartDir $scriptDir
    if (-not $repoRoot) {
        Write-Error "Could not determine repository root. Please run this script from within the repository."
        exit 1
    }
}

Set-Location $repoRoot

$specsDir = Join-Path $repoRoot 'specs'
if (-not (Test-Path $specsDir)) {
    New-Item -ItemType Directory -Path $specsDir -Force | Out-Null
}

$conceptFile = Join-Path $specsDir 'concept.md'
$templateFile = Join-Path $repoRoot '.specify/templates/concept-template.md'

$alreadyExists = $false

if (Test-Path $conceptFile) {
    $alreadyExists = $true
    Write-Host "[concept] Using existing concept file: $conceptFile" -ForegroundColor Yellow
} else {
    if (Test-Path $templateFile) {
        Copy-Item -Path $templateFile -Destination $conceptFile
        Write-Host "[concept] Created concept file from template: $conceptFile" -ForegroundColor Green
    } else {
        # Create minimal structure if template doesn't exist
        $minimalContent = @'
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
'@
        Set-Content -Path $conceptFile -Value $minimalContent -Encoding UTF8
        Write-Host "[concept] Created minimal concept file: $conceptFile" -ForegroundColor Green
    }
}

# Output result
if ($Json) {
    $output = @{
        CONCEPT_FILE = $conceptFile
        SPECS_DIR = $specsDir
        ALREADY_EXISTS = $alreadyExists
        PROJECT_DESCRIPTION = $projectDesc
    }
    $output | ConvertTo-Json -Compress
} else {
    Write-Host "CONCEPT_FILE: $conceptFile"
    Write-Host "SPECS_DIR: $specsDir"
    Write-Host "ALREADY_EXISTS: $alreadyExists"
    if ($projectDesc) {
        Write-Host "PROJECT_DESCRIPTION: $projectDesc"
    }
}

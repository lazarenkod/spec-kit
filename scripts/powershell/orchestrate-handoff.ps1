<#
.SYNOPSIS
    Manages handoff documents between phases in multi-agent workflow.

.DESCRIPTION
    orchestrate-handoff.ps1 handles generation, loading, and validation of
    handoff documents that transfer context between agent phases.

.PARAMETER Action
    The action to perform: generate, load, validate, or list

.PARAMETER Phase
    The phase: specify, plan, tasks, or implement

.PARAMETER FeatureDir
    Path to the feature directory (e.g., specs/features/001-login)

.PARAMETER Json
    Output in JSON format

.EXAMPLE
    .\orchestrate-handoff.ps1 generate specify specs/features/001-login
    .\orchestrate-handoff.ps1 load plan specs/features/001-login
    .\orchestrate-handoff.ps1 validate tasks specs/features/001-login
    .\orchestrate-handoff.ps1 list specs/features/001-login
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet("generate", "load", "validate", "list")]
    [string]$Action,

    [Parameter(Mandatory=$true, Position=1)]
    [string]$PhaseOrDir,

    [Parameter(Position=2)]
    [string]$FeatureDir = "",

    [switch]$Json
)

$ErrorActionPreference = "Stop"

# Constants
$SPECS_DIR = "specs/features"
$HANDOFFS_SUBDIR = "handoffs"
$TEMPLATE_PATH = ".specify/templates/handoff-template.md"

# Map phases to handoff file names
function Get-HandoffFile {
    param([string]$Phase)
    switch ($Phase) {
        "specify"  { return "specify-to-plan.md" }
        "plan"     { return "plan-to-tasks.md" }
        "tasks"    { return "tasks-to-implement.md" }
        default    { return "" }
    }
}

# Map phases to persona names
function Get-SourcePersona {
    param([string]$Phase)
    switch ($Phase) {
        "specify"   { return "Product Agent" }
        "plan"      { return "Architect Agent" }
        "tasks"     { return "Decomposer Agent" }
        "implement" { return "Developer Agent" }
        default     { return "Unknown" }
    }
}

function Get-TargetPersona {
    param([string]$Phase)
    switch ($Phase) {
        "specify"   { return "Architect Agent" }
        "plan"      { return "Decomposer Agent" }
        "tasks"     { return "Developer Agent" }
        "implement" { return "QA Agent" }
        default     { return "Unknown" }
    }
}

# Get the previous phase's handoff file
function Get-PreviousHandoff {
    param([string]$Phase)
    switch ($Phase) {
        "plan"      { return "specify-to-plan.md" }
        "tasks"     { return "plan-to-tasks.md" }
        "implement" { return "tasks-to-implement.md" }
        default     { return "" }
    }
}

# Get next phase name
function Get-NextPhase {
    param([string]$Phase)
    switch ($Phase) {
        "specify" { return "plan" }
        "plan"    { return "tasks" }
        "tasks"   { return "implement" }
        default   { return "" }
    }
}

# Generate a new handoff document
function New-Handoff {
    param(
        [string]$Phase,
        [string]$FeaturePath
    )

    $handoffFile = Get-HandoffFile -Phase $Phase
    if ([string]::IsNullOrEmpty($handoffFile)) {
        Write-Host "Error: Invalid phase '$Phase' for generate action" -ForegroundColor Red
        exit 1
    }

    $handoffsDir = Join-Path $FeaturePath $HANDOFFS_SUBDIR
    $outputPath = Join-Path $handoffsDir $handoffFile

    # Create handoffs directory if needed
    if (-not (Test-Path $handoffsDir)) {
        New-Item -ItemType Directory -Path $handoffsDir -Force | Out-Null
    }

    # Check if handoff already exists
    if (Test-Path $outputPath) {
        Write-Host "Warning: Handoff already exists at $outputPath" -ForegroundColor Yellow
        $confirm = Read-Host "Overwrite? (y/N)"
        if ($confirm -notmatch "^[Yy]$") {
            Write-Host "Aborted."
            exit 0
        }
    }

    # Extract feature info
    $featureName = Split-Path $FeaturePath -Leaf
    $featureId = if ($featureName -match "^(\d+)") { $Matches[1] } else { "000" }
    $featureNameClean = $featureName -replace "^\d+-", ""

    # Get persona names
    $sourcePersona = Get-SourcePersona -Phase $Phase
    $targetPersona = Get-TargetPersona -Phase $Phase
    $nextPhase = Get-NextPhase -Phase $Phase

    # Find template
    $repoRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
    $templateFile = $null

    $possiblePaths = @(
        (Join-Path $repoRoot $TEMPLATE_PATH),
        (Join-Path $repoRoot "templates/handoff-template.md")
    )

    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $templateFile = $path
            break
        }
    }

    $today = Get-Date -Format "yyyy-MM-dd"

    if ($templateFile) {
        # Copy and substitute template
        $content = Get-Content $templateFile -Raw
        $content = $content -replace '\{SOURCE_PHASE\}', $Phase
        $content = $content -replace '\{TARGET_PHASE\}', $nextPhase
        $content = $content -replace '\{FEATURE_ID\}', $featureId
        $content = $content -replace '\{FEATURE_NAME\}', $featureNameClean
        $content = $content -replace '\{DATE\}', $today
        $content = $content -replace '\{SOURCE_PERSONA\}', $sourcePersona
        $content = $content -replace '\{TARGET_PERSONA\}', $targetPersona
        Set-Content -Path $outputPath -Value $content -NoNewline
    }
    else {
        # Generate minimal handoff
        $content = @"
# Handoff: $Phase → $nextPhase

> **Feature**: $featureName
> **Generated**: $today
> **Source Agent**: $sourcePersona
> **Target Agent**: $targetPersona

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

"@
        Set-Content -Path $outputPath -Value $content
    }

    Write-Host "Generated handoff: $outputPath" -ForegroundColor Green
    Write-Host "Next: Fill in the template with phase-specific context" -ForegroundColor Cyan
}

# Load and display a handoff document
function Get-Handoff {
    param(
        [string]$Phase,
        [string]$FeaturePath
    )

    $handoffFile = Get-PreviousHandoff -Phase $Phase
    if ([string]::IsNullOrEmpty($handoffFile)) {
        Write-Host "No previous handoff for phase '$Phase' (this is the first phase)" -ForegroundColor Yellow
        exit 0
    }

    $handoffPath = Join-Path $FeaturePath $HANDOFFS_SUBDIR $handoffFile

    if (-not (Test-Path $handoffPath)) {
        Write-Host "Error: Handoff not found at $handoffPath" -ForegroundColor Red
        Write-Host "The previous phase may not have generated a handoff." -ForegroundColor Yellow
        Write-Host "Suggestion: Run 'orchestrate-handoff.ps1 generate <previous_phase> $FeaturePath'" -ForegroundColor Cyan
        exit 1
    }

    Write-Host "=== Loading Handoff: $handoffFile ===" -ForegroundColor Green
    Write-Host ""

    $content = Get-Content $handoffPath -Raw

    # Display key sections
    $sections = @("Summary", "Key Decisions", "Constraints", "Risks", "Open Questions")
    foreach ($section in $sections) {
        $color = if ($section -eq "Open Questions") { "Yellow" } else { "Cyan" }
        Write-Host "## $section" -ForegroundColor $color

        # Extract section content
        if ($content -match "(?ms)^## $section.*?(?=^## |\z)") {
            $sectionContent = $Matches[0] -replace "^## $section\s*", ""
            Write-Host $sectionContent.Trim()
        }
        Write-Host ""
    }

    Write-Host "Full handoff available at: $handoffPath" -ForegroundColor Green
}

# Validate handoff document completeness
function Test-Handoff {
    param(
        [string]$Phase,
        [string]$FeaturePath,
        [bool]$JsonOutput
    )

    $handoffFile = Get-HandoffFile -Phase $Phase
    if ([string]::IsNullOrEmpty($handoffFile)) {
        Write-Host "Error: Invalid phase '$Phase' for validate action" -ForegroundColor Red
        exit 1
    }

    $handoffPath = Join-Path $FeaturePath $HANDOFFS_SUBDIR $handoffFile

    if (-not (Test-Path $handoffPath)) {
        if ($JsonOutput) {
            @{
                valid = $false
                path = $handoffPath
                error = "File not found"
            } | ConvertTo-Json
        }
        else {
            Write-Host "Error: Handoff not found at $handoffPath" -ForegroundColor Red
        }
        exit 1
    }

    $content = Get-Content $handoffPath -Raw
    $errors = 0
    $warnings = 0

    if (-not $JsonOutput) {
        Write-Host "Validating: $handoffPath" -ForegroundColor Cyan
        Write-Host ""
    }

    $requiredSections = @("Summary", "Key Decisions", "Constraints", "Risks", "Open Questions")
    $foundSections = @()

    foreach ($section in $requiredSections) {
        if ($content -match "(?m)^## $section") {
            $foundSections += $section
            if (-not $JsonOutput) {
                Write-Host "✓ Found section: $section" -ForegroundColor Green
            }
        }
        else {
            $errors++
            if (-not $JsonOutput) {
                Write-Host "✗ Missing section: $section" -ForegroundColor Red
            }
        }
    }

    # Check for placeholder content
    if ($content -match '\{DECISION_|\{RISK_') {
        $warnings++
        if (-not $JsonOutput) {
            Write-Host "⚠ Contains unfilled placeholders" -ForegroundColor Yellow
        }
    }

    # Check for empty tables
    if ($content -match '\|[\s]*\|[\s]*\|[\s]*\|') {
        $warnings++
        if (-not $JsonOutput) {
            Write-Host "⚠ Contains empty table rows" -ForegroundColor Yellow
        }
    }

    # Check checklist
    $checked = ([regex]::Matches($content, '\[x\]')).Count
    $unchecked = ([regex]::Matches($content, '\[ \]')).Count

    if ($JsonOutput) {
        @{
            valid = ($errors -eq 0)
            path = $handoffPath
            errors = $errors
            warnings = $warnings
            checklist = @{
                checked = $checked
                unchecked = $unchecked
            }
            sections = $foundSections
        } | ConvertTo-Json -Depth 3
    }
    else {
        Write-Host ""
        Write-Host "Checklist: $checked checked, $unchecked unchecked"
        Write-Host ""

        if ($errors -gt 0) {
            Write-Host "Validation FAILED: $errors errors, $warnings warnings" -ForegroundColor Red
            exit 1
        }
        elseif ($warnings -gt 0) {
            Write-Host "Validation PASSED with warnings: $warnings warnings" -ForegroundColor Yellow
        }
        else {
            Write-Host "Validation PASSED" -ForegroundColor Green
        }
    }
}

# List all handoffs for a feature
function Get-HandoffList {
    param(
        [string]$FeaturePath,
        [bool]$JsonOutput
    )

    $handoffsDir = Join-Path $FeaturePath $HANDOFFS_SUBDIR
    $featureName = Split-Path $FeaturePath -Leaf

    if (-not (Test-Path $handoffsDir)) {
        if ($JsonOutput) {
            @{
                feature = $featureName
                handoffs = @()
            } | ConvertTo-Json
        }
        else {
            Write-Host "No handoffs directory found" -ForegroundColor Yellow
        }
        exit 0
    }

    $handoffs = Get-ChildItem -Path $handoffsDir -Filter "*.md" -ErrorAction SilentlyContinue

    if ($JsonOutput) {
        @{
            feature = $featureName
            handoffs = @($handoffs | ForEach-Object { $_.Name })
        } | ConvertTo-Json
    }
    else {
        Write-Host "Handoffs for: $featureName" -ForegroundColor Cyan
        Write-Host ""

        foreach ($handoff in $handoffs) {
            $modified = $handoff.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
            Write-Host "✓ $($handoff.Name) (modified: $modified)" -ForegroundColor Green
        }
    }
}

# Main execution
$validPhases = @("specify", "plan", "tasks", "implement")

if ($Action -eq "list") {
    # For list, PhaseOrDir is actually the feature directory
    if (-not (Test-Path $PhaseOrDir)) {
        Write-Host "Error: Directory not found: $PhaseOrDir" -ForegroundColor Red
        exit 1
    }
    Get-HandoffList -FeaturePath $PhaseOrDir -JsonOutput $Json.IsPresent
}
else {
    $Phase = $PhaseOrDir

    if ($Phase -notin $validPhases) {
        Write-Host "Error: Invalid phase '$Phase'" -ForegroundColor Red
        Write-Host "Valid phases: $($validPhases -join ', ')"
        exit 1
    }

    if ([string]::IsNullOrEmpty($FeatureDir)) {
        Write-Host "Error: FeatureDir is required" -ForegroundColor Red
        exit 1
    }

    if (-not (Test-Path $FeatureDir)) {
        Write-Host "Error: Directory not found: $FeatureDir" -ForegroundColor Red
        exit 1
    }

    switch ($Action) {
        "generate" { New-Handoff -Phase $Phase -FeaturePath $FeatureDir }
        "load"     { Get-Handoff -Phase $Phase -FeaturePath $FeatureDir }
        "validate" { Test-Handoff -Phase $Phase -FeaturePath $FeatureDir -JsonOutput $Json.IsPresent }
    }
}

#!/usr/bin/env pwsh
# Reverse-engineer specifications from existing codebase
[CmdletBinding()]
param(
    [switch]$Json,
    [string]$Scope,
    [string[]]$Exclude = @("node_modules/", "dist/", "build/", "__pycache__/", "venv/", ".git/"),
    [double]$MinConfidence = 0.70,
    [ValidateSet("typescript", "python", "go", "java", "kotlin")]
    [string]$Language,
    [string]$OutputDir = "reverse-engineered",
    [switch]$MergeMode,
    [switch]$Help
)
$ErrorActionPreference = 'Stop'

# Show help if requested
if ($Help) {
    Write-Host "Usage: ./reverse-engineer.ps1 -Scope <patterns> [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Scope <patterns>        Scan scope patterns (required): 'src/**/*.ts', 'api/**/*.py'"
    Write-Host "  -Exclude <pattern>       Exclude pattern (can be specified multiple times)"
    Write-Host "  -MinConfidence <value>   Minimum confidence threshold (0.0-1.0, default: 0.70)"
    Write-Host "  -Language <lang>         Force language (typescript, python, go, java, kotlin)"
    Write-Host "  -OutputDir <dir>         Override output directory (default: reverse-engineered/)"
    Write-Host "  -MergeMode               Auto-merge verified FRs into canonical spec"
    Write-Host "  -Json                    Output in JSON format"
    Write-Host "  -Help                    Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  ./reverse-engineer.ps1 -Scope 'src/**/*.ts' -Exclude '*.test.ts'"
    Write-Host "  ./reverse-engineer.ps1 -Scope 'api/**/*.py' -MinConfidence 0.80"
    Write-Host "  ./reverse-engineer.ps1 -Scope 'src/**/*.go' -Language go -OutputDir extracted"
    exit 0
}

# Validation: -Scope is required
if (-not $Scope) {
    if ($Json) {
        $error = @{
            error     = "Missing required argument: -Scope"
            exit_code = 1
        }
        Write-Output ($error | ConvertTo-Json -Compress)
    }
    else {
        Write-Error "Missing required argument: -Scope"
        Write-Host "Run './reverse-engineer.ps1 -Help' for usage information." -ForegroundColor Yellow
    }
    exit 1
}

# Validation: check if output directory already exists
if (Test-Path $OutputDir) {
    if ($Json) {
        $error = @{
            error     = "Output directory already exists: $OutputDir"
            exit_code = 1
        }
        Write-Output ($error | ConvertTo-Json -Compress)
    }
    else {
        Write-Error "Output directory already exists: $OutputDir"
        Write-Host "To re-extract, delete the directory first or specify a different -OutputDir" -ForegroundColor Yellow
    }
    exit 1
}

# Validation: check min-confidence range
if ($MinConfidence -lt 0.0 -or $MinConfidence -gt 1.0) {
    if ($Json) {
        $error = @{
            error     = "Invalid -MinConfidence value. Must be between 0.0 and 1.0"
            exit_code = 1
        }
        Write-Output ($error | ConvertTo-Json -Compress)
    }
    else {
        Write-Error "Invalid -MinConfidence value. Must be between 0.0 and 1.0"
    }
    exit 1
}

# Output JSON if requested
if ($Json) {
    $result = @{
        status         = "ready"
        scope          = $Scope
        exclude        = $Exclude
        min_confidence = $MinConfidence
        language       = if ($Language) { $Language } else { "" }
        output_dir     = $OutputDir
        merge_mode     = $MergeMode.IsPresent
    }
    Write-Output ($result | ConvertTo-Json -Depth 3)
}
else {
    Write-Host "✓ Reverse-engineering prerequisites check passed" -ForegroundColor Green
    Write-Host ""
    Write-Host "Configuration:"
    Write-Host "  Scope:          $Scope"
    Write-Host "  Exclude:        $($Exclude -join ', ')"
    Write-Host "  Min confidence: $MinConfidence"
    if ($Language) {
        Write-Host "  Language:       $Language (forced)"
    }
    else {
        Write-Host "  Language:       auto-detect"
    }
    Write-Host "  Output dir:     $OutputDir"
    Write-Host "  Merge mode:     $($MergeMode.IsPresent)"
    Write-Host ""
    Write-Host "Next step: Run /speckit.reverse-engineer in your AI agent"
}

exit 0

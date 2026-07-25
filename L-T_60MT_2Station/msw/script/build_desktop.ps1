$ErrorActionPreference = 'Stop'

function Write-Step {
    param([string]$Message)
    Write-Host "`n=== $Message ===" -ForegroundColor Cyan
}

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Ensure-Tool {
    param([string]$Name, [string]$DownloadUrl, [string]$InstallHint)
    if (Test-Command $Name) {
        & $Name --version 2>$null | Select-Object -First 1 | Out-Null
        Write-Host "[OK] $Name is available" -ForegroundColor Green
        return
    }

    Write-Host "[MISSING] $Name was not found on PATH." -ForegroundColor Yellow
    Write-Host "Download: $DownloadUrl" -ForegroundColor Yellow
    Write-Host "Install hint: $InstallHint" -ForegroundColor Yellow
    throw "Missing required tool: $Name"
}

$projectRoot = $PSScriptRoot
$desktopDir = Join-Path $projectRoot 'desktop/L-T_60MT_2STATION'
$repoRoot = $projectRoot
$msiOutputDir = Join-Path $desktopDir 'src-tauri/target/release/bundle/msi'

if (-not (Test-Path $desktopDir)) {
    throw "Desktop folder not found: $desktopDir"
}

$rustBin = 'C:\Users\haris\.cargo\bin'
if (Test-Path $rustBin) {
    $env:Path = "$rustBin;$env:Path"
}

Write-Host "Project root: $projectRoot" -ForegroundColor DarkGray
Write-Host "Desktop app folder: $desktopDir" -ForegroundColor DarkGray
Write-Host "Installer output folder: $msiOutputDir" -ForegroundColor DarkGray

Write-Step 'Checking prerequisites'
Ensure-Tool -Name 'python' -DownloadUrl 'https://www.python.org/downloads/' -InstallHint 'Install Python 3.11 or 3.12 and enable Add Python to PATH'
Ensure-Tool -Name 'node' -DownloadUrl 'https://nodejs.org/' -InstallHint 'Install Node.js LTS'
Ensure-Tool -Name 'npm' -DownloadUrl 'https://nodejs.org/' -InstallHint 'Install Node.js LTS'
Ensure-Tool -Name 'cargo' -DownloadUrl 'https://rustup.rs/' -InstallHint 'Install Rust via rustup'
Ensure-Tool -Name 'rustc' -DownloadUrl 'https://rustup.rs/' -InstallHint 'Install Rust via rustup'

Write-Step 'Checking project files'
if (-not (Test-Path "$repoRoot\manage.py")) { throw "manage.py not found in $repoRoot" }
if (-not (Test-Path "$repoRoot\start_backend.py")) { throw "start_backend.py not found in $repoRoot" }
if (-not (Test-Path "$desktopDir\package.json")) { throw "package.json not found in $desktopDir" }

Write-Step 'Preparing Django static files'
Set-Location $repoRoot
if (Test-Path '.\venv\Scripts\python.exe') {
    .\venv\Scripts\python.exe .\manage.py collectstatic --noinput | Out-Null
} else {
    Write-Warning 'Virtual environment not found; continuing without collectstatic.'
}

Write-Step 'Installing desktop dependencies'
Set-Location $desktopDir
npm install

Write-Step 'Building Tauri MSI installer'
npm run tauri build -- --bundles msi

Write-Step 'Build completed'
if (Test-Path $msiOutputDir) {
    Get-ChildItem -Path $msiOutputDir -File | Select-Object Name, FullName | Format-Table -AutoSize
} else {
    throw "Installer output folder was not created: $msiOutputDir"
}
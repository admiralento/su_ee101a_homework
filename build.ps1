<#
.SYNOPSIS
  Compile the homework currently selected in config/current_assignment.tex to out.pdf.

.DESCRIPTION
  Mirrors Overleaf: the main document is main_solutions.tex or main_student.tex, compiled
  with a XeTeX engine and rerun until the .aux point totals are stable. Uses Tectonic
  (https://tectonic-typesetting.github.io), looked up first in .tools\tectonic\ and then on PATH.
  Intermediate files go to build\ (git-ignored); the final PDF is copied to out.pdf.

.EXAMPLE
  .\build.ps1                 # solutions (default)
  .\build.ps1 -Mode student
  .\build.ps1 -Mode questionbank   # every question in the bank (main_questionbank.tex)
#>
param(
    [ValidateSet('solutions', 'student', 'questionbank')]
    [string]$Mode = 'solutions',

    # Download Tectonic into .tools\tectonic\ (one-time setup), then exit.
    [switch]$Install
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
Set-Location $root

if ($Install) {
    $version = '0.17.0'
    $url = "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%40$version/tectonic-$version-x86_64-pc-windows-msvc.zip"
    $dest = Join-Path $root '.tools\tectonic'
    New-Item -ItemType Directory -Force $dest | Out-Null
    $zip = Join-Path $env:TEMP "tectonic-$version.zip"
    Write-Host "Downloading Tectonic $version ..."
    Invoke-WebRequest $url -OutFile $zip
    Expand-Archive $zip -DestinationPath $dest -Force
    Remove-Item $zip
    & (Join-Path $dest 'tectonic.exe') --version
    return
}

$tectonic = Join-Path $root '.tools\tectonic\tectonic.exe'
if (-not (Test-Path $tectonic)) {
    $cmd = Get-Command tectonic -ErrorAction SilentlyContinue
    if ($cmd) { $tectonic = $cmd.Source }
    else { throw "Tectonic not found. Run .\build.ps1 -Install once, or put tectonic.exe on PATH." }
}

$main = "main_$Mode.tex"
$outDir = Join-Path $root 'build'
New-Item -ItemType Directory -Force $outDir | Out-Null

# Show which assignment is being built (config/current_assignment.tex is shared Overleaf state).
Get-Content 'config\current_assignment.tex' | Where-Object { $_ -match '\\def' } | ForEach-Object { "  $_" }
Write-Host "Compiling $main ..."

& $tectonic $main --outdir $outDir --keep-intermediates --keep-logs
if ($LASTEXITCODE -ne 0) {
    throw "Compilation failed (exit $LASTEXITCODE). See build\main_$Mode.log"
}

Copy-Item (Join-Path $outDir "main_$Mode.pdf") (Join-Path $root 'out.pdf') -Force
Write-Host "Wrote $(Join-Path $root 'out.pdf')"

<#
.SYNOPSIS
  Compile one homework (or the question bank catalog) to out.pdf.

.DESCRIPTION
  Mirrors Overleaf: every homework has two root files in its folder,
  assignments/<Semester>/<HWxx>/<Semester>_<HWxx>_student.tex and ..._solutions.tex. This script
  compiles one of them with Tectonic (XeTeX engine, reruns until the .aux point totals are stable),
  from the project root so paths resolve as on Overleaf. Tectonic is looked up in .tools\tectonic\
  and then on PATH. Intermediate files go to build\ (git-ignored); the PDF is copied to out.pdf.

.EXAMPLE
  .\build.ps1 -Semester "Fall 2026" -Assignment HW07                  # solutions (default)
  .\build.ps1 -Semester "Fall 2026" -Assignment HW07 -Mode student
  .\build.ps1 -File "assignments\Fall 2026\HW07\Fall2026_HW07_student.tex"
  .\build.ps1 -Mode questionbank                                       # catalog, with solutions
  .\build.ps1 -Mode questionbank-student                               # catalog, without solutions
#>
param(
    # A root .tex file to compile (a homework root file or main_questionbank_*.tex)
    [string]$File,

    [string]$Semester,
    [string]$Assignment,

    [ValidateSet('solutions', 'student', 'questionbank', 'questionbank-student')]
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

# Which root file to compile
if ($File) {
    $target = (Resolve-Path $File).Path
} elseif ($Mode -eq 'questionbank') {
    $target = Join-Path $root 'main_questionbank_solutions.tex'
} elseif ($Mode -eq 'questionbank-student') {
    $target = Join-Path $root 'main_questionbank_student.tex'
} elseif ($Semester -and $Assignment) {
    $name = "$($Semester -replace ' ', '')_$($Assignment)_$Mode.tex"
    $target = Join-Path $root "assignments\$Semester\$Assignment\$name"
} else {
    throw 'Give -File <root .tex>, or -Semester "Fall 2026" -Assignment HW07 [-Mode student], or -Mode questionbank.'
}
if (-not (Test-Path $target)) { throw "Not found: $target (run python tools\check.py --fix-mains?)" }
$rel = Resolve-Path -Relative $target
$stem = [IO.Path]::GetFileNameWithoutExtension($target)

$outDir = Join-Path $root 'build'
New-Item -ItemType Directory -Force $outDir | Out-Null
Write-Host "Compiling $rel ..."

# -Z search-path=. : resolve \input/\includegraphics from the project root, as Overleaf does
& $tectonic $rel --outdir $outDir --keep-intermediates --keep-logs -Z search-path=.
if ($LASTEXITCODE -ne 0) {
    throw "Compilation failed (exit $LASTEXITCODE). See build\$stem.log"
}

Copy-Item (Join-Path $outDir "$stem.pdf") (Join-Path $root 'out.pdf') -Force
Write-Host "Wrote $(Join-Path $root 'out.pdf')"

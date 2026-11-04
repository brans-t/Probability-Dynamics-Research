# Windows PowerShell 5 treats native stderr as ErrorRecord objects when output
# is redirected. Use process exit codes to decide whether TeX/Biber succeeded.
$ErrorActionPreference = 'Continue'

foreach ($tool in @('xelatex', 'biber')) {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "Required tool not found: $tool. Install TeX Live or MiKTeX and add its executables to PATH."
    }
}

Push-Location (Join-Path $PSScriptRoot 'paper') -ErrorAction Stop
try {
    New-Item -ItemType Directory -Path 'Tmp' -Force -ErrorAction Stop | Out-Null
    $texArguments = @(
        '-output-directory=Tmp', '-synctex=1', '-interaction=nonstopmode',
        '-halt-on-error', '-file-line-error', 'main.tex'
    )
    & xelatex @texArguments
    if ($LASTEXITCODE -ne 0) { throw 'XeLaTeX failed; see paper/Tmp/main.log.' }
    $previousBiberLocale = [Environment]::GetEnvironmentVariable('LC_ALL', 'Process')
    try {
        $env:LC_ALL = 'C'
        & biber --input-directory=Tmp --output-directory=Tmp main
        $biberExitCode = $LASTEXITCODE
    }
    finally {
        if ($null -eq $previousBiberLocale) {
            Remove-Item Env:LC_ALL -ErrorAction SilentlyContinue
        }
        else {
            $env:LC_ALL = $previousBiberLocale
        }
    }
    if ($biberExitCode -ne 0) { throw 'Biber failed; see paper/Tmp/main.blg.' }
    foreach ($pass in 1..2) {
        & xelatex @texArguments
        if ($LASTEXITCODE -ne 0) { throw "XeLaTeX pass $pass failed; see paper/Tmp/main.log." }
    }
    Write-Host "Compiled $(Join-Path $PSScriptRoot 'paper/Tmp/main.pdf')"
}
finally {
    Pop-Location
}

<#
Stops the lcp-web site on this PC (docker compose stop), so the GPU is free, e.g. for games.
The container stays stopped after a reboot too (restart: unless-stopped remembers a manual stop)
until site_start runs again. Tailscale Funnel stays on; visitors get an error meanwhile.

Double-click scripts\site_stop.cmd, or:  pwsh -File scripts\site_stop.ps1 [-Docker]
  -Docker   also quit Docker Desktop, which frees the RAM held by its WSL machine (up to 12 GB)
#>
param([switch]$Docker)

$repo = Split-Path $PSScriptRoot -Parent

function Test-Engine { docker info --format '{{.ServerVersion}}' 2>$null | Out-Null; $LASTEXITCODE -eq 0 }

Write-Host '== lcp-web: oprire =='
if (Test-Engine) {
    Push-Location $repo
    docker compose stop
    $rc = $LASTEXITCODE
    Pop-Location
    if ($rc -ne 0) { Write-Host 'docker compose stop a esuat.' -ForegroundColor Red; exit 1 }
    Write-Host 'Server oprit.'
    if ($Docker) {
        Write-Host 'Inchid Docker Desktop...'
        docker desktop stop 2>$null | Out-Null
    }
} else {
    Write-Host 'Docker nu ruleaza, deci serverul e deja oprit.'
}

Write-Host "VRAM acum: $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)"
Write-Host 'Site oprit. Nu porneste singur nici la restart; ca sa-l pornesti: site_start.' -ForegroundColor Green
Write-Host 'UptimeRobot iti trimite mail "Down"; daca nu vrei mailul, pune monitorul pe Pause in dashboard.'

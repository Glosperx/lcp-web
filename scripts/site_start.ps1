<#
Starts the lcp-web site on this PC: Docker Desktop (if it is not running), a VRAM check (Gemma needs
the card almost empty, otherwise WDDM silently spills it into shared memory and readings get ~2x
slower), the container (docker compose up -d), a wait for /api/health, Tailscale Funnel on port 8000,
then VRAM and spill after loading.

Double-click scripts\site_start.cmd, or:  pwsh -File scripts\site_start.ps1 [-Yes]
  -Yes   do not stop when VRAM is too full (only warn)
#>
param([switch]$Yes)

$repo = Split-Path $PSScriptRoot -Parent
$ts = Join-Path $env:ProgramFiles 'Tailscale\tailscale.exe'
$healthUrl = 'http://127.0.0.1:8000/api/health'
$vramLimit = 700    # MiB in use before the model loads
$spillLimit = 300   # MiB of shared GPU memory for the container (vmwp); ~190 is normal pinned memory

function Test-Engine { docker info --format '{{.ServerVersion}}' 2>$null | Out-Null; $LASTEXITCODE -eq 0 }
function Get-Health { curl.exe -s -o NUL -m 5 -w '%{http_code}' $healthUrl }
function Get-VramUsed { [int](nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits) }
function Get-GpuMemory([string]$kind) {
    # MiB per process from the "GPU Process Memory" counters (kind: Dedicated or Shared)
    $samples = (Get-Counter "\GPU Process Memory(*)\$kind Usage" -ErrorAction SilentlyContinue).CounterSamples
    $samples | Where-Object { $_.InstanceName -match '^pid_(\d+)_' } | ForEach-Object {
        $p = Get-Process -Id ([int]$Matches[1]) -ErrorAction SilentlyContinue
        [pscustomobject]@{ App = $(if ($p) { $p.ProcessName } else { '?' }); Bytes = $_.CookedValue }
    } | Group-Object App | ForEach-Object {
        [pscustomobject]@{ App = $_.Name; MiB = [int](($_.Group | Measure-Object Bytes -Sum).Sum / 1MB) }
    } | Sort-Object MiB -Descending
}

Write-Host '== lcp-web: pornire =='

# 1. Docker Desktop
if (-not (Test-Engine)) {
    Write-Host 'Docker Desktop nu ruleaza, il pornesc...'
    docker desktop start 2>$null | Out-Null
    $t0 = Get-Date
    while (-not (Test-Engine)) {
        if (((Get-Date) - $t0).TotalSeconds -gt 180) {
            Write-Host 'Docker nu a pornit in 3 minute. Porneste Docker Desktop manual si reia.' -ForegroundColor Red
            exit 1
        }
        Start-Sleep 3
    }
    Write-Host ('Docker pornit in {0:N0} s.' -f ((Get-Date) - $t0).TotalSeconds)
}

# 2. VRAM check and container
Push-Location $repo
$running = docker compose ps -q api 2>$null
if ($running) {
    Write-Host 'Containerul ruleaza deja.'
} else {
    while (($used = Get-VramUsed) -gt $vramLimit) {
        Write-Host "VRAM ocupat inainte de pornire: $used MiB (maxim $vramLimit)." -ForegroundColor Yellow
        Write-Host 'Modelul nu ar mai incapea in placa si analiza ar fi ~2x mai lenta. Ce foloseste placa:'
        Get-GpuMemory Dedicated | Where-Object MiB -ge 30 | Format-Table -AutoSize | Out-String | Write-Host
        if ($Yes) { Write-Host 'Continui oricum (-Yes).'; break }
        $a = Read-Host 'Inchide aplicatiile (Firefox, jocuri, al doilea monitor) si apasa Enter ca sa reverific, sau scrie c ca sa continui oricum'
        if ($a -eq 'c') { break }
    }
    Write-Host "VRAM inainte de pornire: $(Get-VramUsed) MiB."
    docker compose up -d
    if ($LASTEXITCODE -ne 0) { Pop-Location; Write-Host 'docker compose up a esuat.' -ForegroundColor Red; exit 1 }
}
Pop-Location

# 3. Wait until the models are loaded
Write-Host -NoNewline 'Astept serverul (incarcarea modelelor dureaza ~70 s)'
$t0 = Get-Date
do {
    $code = Get-Health
    if ($code -eq '200') { break }
    if ($code -eq '500') {
        Write-Host ''
        Write-Host 'Serverul raporteaza eroare. Detalii: docker compose logs api' -ForegroundColor Red
        exit 1
    }
    Write-Host -NoNewline '.'
    Start-Sleep 3
} while (((Get-Date) - $t0).TotalSeconds -lt 300)
Write-Host ''
if ($code -ne '200') {
    Write-Host "Serverul nu a raspuns in 5 minute (ultimul cod: $code). Detalii: docker compose logs api" -ForegroundColor Red
    exit 1
}
Write-Host ('Server gata in {0:N0} s.' -f ((Get-Date) - $t0).TotalSeconds) -ForegroundColor Green

# 4. Tailscale Funnel
$fs = & $ts funnel status 2>&1 | Out-String
if ($fs -notmatch 'Funnel on' -or $fs -notmatch '127\.0\.0\.1:8000') {
    Write-Host 'Funnel nu e pornit pe portul 8000, il pornesc...'
    & $ts funnel --bg 8000 | Out-Null
    $fs = & $ts funnel status 2>&1 | Out-String
}
if ($fs -match 'Funnel on') { Write-Host 'Funnel pornit: https://lcp.tail6e4ef5.ts.net' }
else { Write-Host 'Funnel nu a pornit. Verifica Tailscale (iconita din bara).' -ForegroundColor Red }

# 5. VRAM after loading
$shared = (Get-GpuMemory Shared | Where-Object App -eq 'vmwp' | Measure-Object MiB -Maximum).Maximum
Write-Host "VRAM acum: $(Get-VramUsed) MiB; memorie shared a containerului: $shared MiB."
if ($shared -gt $spillLimit) {
    Write-Host 'Modelul a trecut partial in memoria shared (analiza ~2x mai lenta). Inchide aplicatiile care folosesc placa, apoi ruleaza site_stop si site_start.' -ForegroundColor Yellow
}
Write-Host 'Site pornit: https://lcp-web-static.vercel.app' -ForegroundColor Green

@echo off
rem Double-click wrapper for site_stop.ps1 (PowerShell 7 if installed, else Windows PowerShell).
where pwsh >nul 2>nul
if %errorlevel%==0 (set PS=pwsh) else (set PS=powershell)
%PS% -NoProfile -ExecutionPolicy Bypass -File "%~dp0site_stop.ps1" %*
pause

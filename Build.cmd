@echo off
REM © 2026 Mr-Aurevo-X · QrMake · 100% local · free · updates not guaranteed
cd /d "%~dp0"
if exist "%~dp0ui\vendor\pc-command-kit\" if exist "..\..\UI proprietaire\scripts\sync-ui-kit.ps1" (
  powershell -NoProfile -ExecutionPolicy Bypass -File "..\..\UI proprietaire\scripts\sync-ui-kit.ps1" -Target "%~dp0ui\vendor\pc-command-kit" -KitRoot "..\..\UI proprietaire"
)
python -m PyInstaller --noconfirm --clean QrMake.spec
if exist "dist\QrMake.exe" (
  copy /Y "dist\QrMake.exe" "QrMake.exe" >nul
  echo OK: QrMake.exe
) else (
  echo Build failed.
  exit /b 1
)

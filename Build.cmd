:: Copyright (c) 2026 Mr-Aurevo-X. All rights reserved.
:: SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
:: Author: Mr-Aurevo-X

@echo off
REM (c) 2026 Mr-Aurevo-X / QrTools / 100% local / free / updates not guaranteed
cd /d "%~dp0"
if exist "%~dp0ui\vendor\pc-command-kit\" if exist "..\..\02_Shared_Infrastructure\UI-proprietaire\scripts\sync-ui-kit.ps1" (
  powershell -NoProfile -ExecutionPolicy Bypass -File "..\..\02_Shared_Infrastructure\UI-proprietaire\scripts\sync-ui-kit.ps1" -Target "%~dp0ui\vendor\pc-command-kit" -KitRoot "..\..\02_Shared_Infrastructure\UI-proprietaire"
)
if exist "%~dp0.venv\Scripts\python.exe" (
  "%~dp0.venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean QrTools.spec
) else (
  python -m PyInstaller --noconfirm --clean QrTools.spec
)
if exist "dist\QrTools.exe" (
  copy /Y "dist\QrTools.exe" "QrTools.exe" >nul
  echo OK: QrTools.exe
) else (
  echo Build failed.
  exit /b 1
)

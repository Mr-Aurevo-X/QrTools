@echo off
REM © 2026 Mr-Aurevo-X · QrTools · 100% local · free · updates not guaranteed
REM Prefer windowed QrTools.exe (no lasting CMD). Fallback: detached pythonw.
cd /d "%~dp0"

if exist "%~dp0QrTools.exe" (
  start "" /D "%~dp0" "%~dp0QrTools.exe"
  exit /b 0
)

if exist "%~dp0.venv\Scripts\pythonw.exe" (
  start "" /D "%~dp0" "%~dp0.venv\Scripts\pythonw.exe" "%~dp0host\host.py"
  exit /b 0
)

where pythonw >nul 2>&1
if %ERRORLEVEL%==0 (
  start "" /D "%~dp0" pythonw "%~dp0host\host.py"
  exit /b 0
)

where py >nul 2>&1
if %ERRORLEVEL%==0 (
  start "" /D "%~dp0" py -3w "%~dp0host\host.py"
  exit /b 0
)

exit /b 1
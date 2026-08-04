@echo off
REM © 2026 Mr-Aurevo-X · QrMake · 100% local · free · updates not guaranteed
REM Optional alias — same preference: exe first, then pythonw
cd /d "%~dp0"
if exist "%~dp0QrMake.exe" (
  start "" /D "%~dp0" "%~dp0QrMake.exe"
  exit /b 0
)
if exist "%~dp0.venv\Scripts\pythonw.exe" (
  start "" /D "%~dp0" "%~dp0.venv\Scripts\pythonw.exe" "%~dp0host\host.py"
) else (
  start "" /D "%~dp0" pythonw "%~dp0host\host.py"
)
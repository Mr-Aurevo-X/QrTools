@echo off
REM © 2026 Mr-Aurevo-X · QrMake · 100% local · free · updates not guaranteed
REM Mr-Aurevo-X-LAUNCHER-ID: Mr-Aurevo-X
cd /d "%~dp0"
if exist "%~dp0.venv\Scripts\pythonw.exe" (
  "%~dp0.venv\Scripts\pythonw.exe" host\host.py
) else (
  pythonw host\host.py
)

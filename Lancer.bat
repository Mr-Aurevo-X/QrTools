@echo off
REM © 2026 Mr-Aurevo-X · QrMake · 100% local · free · updates not guaranteed
REM Silent launcher — no lingering CMD console (pythonw / exe)
cd /d "%~dp0"

if exist "%~dp0QrMake.exe" (
  start "" "%~dp0QrMake.exe"
  exit /b 0
)

if /I "%~1"=="_hidden" goto :run
mshta "javascript:var sh=new ActiveXObject('WScript.Shell');sh.Run('\"%~f0\" _hidden',0,false);close();"
exit /b 0

:run
if exist "%~dp0.venv\Scripts\pythonw.exe" (
  "%~dp0.venv\Scripts\pythonw.exe" "%~dp0host\host.py"
  exit /b %ERRORLEVEL%
)
where pythonw >nul 2>&1
if %ERRORLEVEL%==0 (
  pythonw "%~dp0host\host.py"
  exit /b %ERRORLEVEL%
)
where py >nul 2>&1
if %ERRORLEVEL%==0 (
  py -3w "%~dp0host\host.py"
  exit /b %ERRORLEVEL%
)
exit /b 1

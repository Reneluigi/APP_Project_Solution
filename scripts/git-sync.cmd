@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0git-sync.ps1" %*
set EXITCODE=%ERRORLEVEL%
if not "%EXITCODE%"=="0" (
    echo.
    echo git-sync finished with errors. Exit code: %EXITCODE%
    pause
)
exit /b %EXITCODE%

@echo off
REM SessionStart hook runner for superpowers plugin
REM Usage: run-hook.cmd <hook-name>
REM This dispatches to the appropriate hook script based on the argument.

setlocal enabledelayedexpansion

set "HOOK_NAME=%~1"
set "SCRIPT_DIR=%~dp0"
set "PLUGIN_ROOT=%SCRIPT_DIR%.."

if "%HOOK_NAME%"=="" (
    echo Usage: run-hook.cmd ^<hook-name^> >&2
    exit /b 1
)

REM Dispatch to hook script
set "HOOK_SCRIPT=%SCRIPT_DIR%%HOOK_NAME%"
if exist "%HOOK_SCRIPT%" (
    call "%HOOK_SCRIPT%"
) else if exist "%HOOK_SCRIPT%.cmd" (
    call "%HOOK_SCRIPT%.cmd"
) else if exist "%HOOK_SCRIPT%.bat" (
    call "%HOOK_SCRIPT%.bat"
) else (
    echo Hook script not found: %HOOK_SCRIPT% >&2
    exit /b 1
)

endlocal

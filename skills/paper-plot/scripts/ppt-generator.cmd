@echo off
REM ppt-generator.cmd — Windows variant. Generate PPT from JSON spec.
REM Usage: ppt-generator.cmd --spec <spec.json> --output <output.pptx> [--rough] [--polish]

setlocal enabledelayedexpansion

REM Collect all arguments
set "ARGS=%*"

where bash >nul 2>&1
if %ERRORLEVEL% equ 0 (
    bash "%~dp0ppt-generator.sh" %ARGS%
) else (
    python "%~dp0ppt-generator.py" %ARGS%
)

endlocal

@echo off
REM ppt-slide-analyzer.cmd — Windows variant. Analyzes PPT template slides.
REM Usage: ppt-slide-analyzer.cmd <template.pptx>

setlocal enabledelayedexpansion

set "TEMPLATE=%~1"
if "%TEMPLATE%"=="" (
    echo {"error": "Usage: ppt-slide-analyzer.cmd ^<template.pptx^>"}
    exit /b 1
)

if not exist "%TEMPLATE%" (
    echo {"error": "File not found: %TEMPLATE%"}
    exit /b 1
)

REM Delegate to the .sh script via bash if available, otherwise use python directly
where bash >nul 2>&1
if %ERRORLEVEL% equ 0 (
    bash "%~dp0ppt-slide-analyzer.sh" "%TEMPLATE%"
) else (
    python "%~dp0ppt-slide-analyzer.py" "%TEMPLATE%"
)

endlocal

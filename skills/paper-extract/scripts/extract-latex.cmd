@echo off
REM Windows wrapper for extract-latex.py
REM Usage: extract-latex.cmd <main.tex> [--output <dir>]

set SCRIPT_DIR=%~dp0
python "%SCRIPT_DIR%extract-latex.py" %*

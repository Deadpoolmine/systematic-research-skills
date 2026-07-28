@echo off
REM Windows wrapper for extract-pdf.py
REM Usage: extract-pdf.cmd <paper.pdf> [--output <dir>]

set SCRIPT_DIR=%~dp0
python "%SCRIPT_DIR%extract-pdf.py" %*

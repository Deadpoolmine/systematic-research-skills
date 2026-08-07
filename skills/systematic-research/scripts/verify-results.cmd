@echo off
REM Cross-Validation — verify consistency between results.json and output
python "%~dp0verify-results.py" %*

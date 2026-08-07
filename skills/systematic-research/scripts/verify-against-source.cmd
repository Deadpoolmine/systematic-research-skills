@echo off
REM Source-API Cross-Verification — verify results.json against source APIs
python "%~dp0verify-against-source.py" %*

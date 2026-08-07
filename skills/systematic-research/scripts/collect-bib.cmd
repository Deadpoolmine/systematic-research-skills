@echo off
REM BibTeX Collector — aggregate all bibentry.bib into references.bib
python "%~dp0collect-bib.py" %*

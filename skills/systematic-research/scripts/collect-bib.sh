#!/usr/bin/env bash
# BibTeX Collector — aggregate all bibentry.bib into references.bib
python "$(dirname "$0")/collect-bib.py" "$@"

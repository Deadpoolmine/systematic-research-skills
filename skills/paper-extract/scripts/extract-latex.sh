#!/bin/bash
# Linux/macOS wrapper for extract-latex.py
# Usage: ./extract-latex.sh <main.tex> [--output <dir>]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/extract-latex.py" "$@"

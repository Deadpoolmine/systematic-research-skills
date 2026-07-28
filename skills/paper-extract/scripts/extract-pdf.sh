#!/bin/bash
# Linux/macOS wrapper for extract-pdf.py
# Usage: ./extract-pdf.sh <paper.pdf> [--output <dir>]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/extract-pdf.py" "$@"

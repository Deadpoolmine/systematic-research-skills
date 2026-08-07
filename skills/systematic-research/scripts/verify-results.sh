#!/usr/bin/env bash
# Cross-Validation — verify consistency between results.json and output
python "$(dirname "$0")/verify-results.py" "$@"

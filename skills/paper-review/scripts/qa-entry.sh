#!/usr/bin/env bash
# ============================================================
# qa-entry.sh — Append a QA entry to a reviewer's qa-log.md
#
# Usage: ./qa-entry.sh <ReviewerNumber> "<UserQuestion>"
# Example: ./qa-entry.sh 3 "Why did you rate the evaluation as weak?"
# ============================================================
set -euo pipefail

REVIEWER_NUM="$1"
USER_QUESTION="$2"
BASE_DIR="review/reviews/reviewer${REVIEWER_NUM}"
QA_LOG="${BASE_DIR}/qa-log.md"
REVIEW_MD="${BASE_DIR}/review.md"

# --- Validate inputs ---
if [[ -z "$REVIEWER_NUM" ]]; then
    echo "ERROR: Reviewer number required."
    echo "Usage: qa-entry.sh <N> \"<question>\""
    exit 1
fi
if [[ -z "$USER_QUESTION" ]]; then
    echo "ERROR: User question required."
    echo "Usage: qa-entry.sh <N> \"<question>\""
    exit 1
fi

# --- Check that review exists ---
if [[ ! -f "$REVIEW_MD" ]]; then
    echo "ERROR: No review found for Reviewer ${REVIEWER_NUM} at ${REVIEW_MD}"
    echo "Run Step 2 first to generate reviews."
    exit 1
fi

# --- Ensure directory and qa-log.md exist ---
mkdir -p "$BASE_DIR"
if [[ ! -f "$QA_LOG" ]]; then
    {
        echo "# QA Log — Reviewer ${REVIEWER_NUM}"
        echo ""
        echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "---"
        echo ""
    } > "$QA_LOG"
fi

# --- Determine next Q number ---
QNUM=1
if [[ -f "$QA_LOG" ]]; then
    LAST_Q=$(grep -oP '^## Q\K[0-9]+' "$QA_LOG" | tail -1)
    if [[ -n "$LAST_Q" ]]; then
        QNUM=$((LAST_Q + 1))
    fi
fi

# --- Get current date ---
DATE_STR=$(date '+%Y-%m-%d')

# --- Append QA entry ---
{
    echo "## Q${QNUM}: ${DATE_STR}"
    echo ""
    echo "**User Question:**"
    echo "${USER_QUESTION}"
    echo ""
    echo "**Reviewer Response:**"
    echo "<TO BE FILLED BY AGENT — respond in Reviewer ${REVIEWER_NUM}'s voice>"
    echo ""
    echo "**Internal Reasoning:**"
    echo "<TO BE FILLED BY AGENT — record why Reviewer ${REVIEWER_NUM} answered this way>"
    echo ""
    echo "---"
    echo ""
} >> "$QA_LOG"

echo "QA entry Q${QNUM} appended to ${QA_LOG}"
echo "Next: agent must fill Reviewer Response and Internal Reasoning."

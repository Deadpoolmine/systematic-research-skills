#!/usr/bin/env bash
# ============================================================
# aggregate-report.sh — Aggregate all reviews into a formatted report
#
# Usage: ./aggregate-report.sh [output_path]
# Default output: review/aggregate-report.md
# ============================================================
set -euo pipefail

OUTPUT="${1:-review/aggregate-report.md}"
REVIEWERS_DIR="review/reviewers"
REVIEWS_DIR="review/reviews"
PROFILES="${REVIEWERS_DIR}/profiles.md"
DATE_STR=$(date '+%Y-%m-%d %H:%M')

# --- Validate prerequisites ---
if [[ ! -f "$PROFILES" ]]; then
    echo "ERROR: Profiles not found at ${PROFILES}. Run Step 1 first."
    exit 1
fi

REVIEW_COUNT=0
for i in 1 2 3 4 5; do
    if [[ -f "${REVIEWS_DIR}/reviewer${i}/review.md" ]]; then
        REVIEW_COUNT=$((REVIEW_COUNT + 1))
    fi
done
if [[ $REVIEW_COUNT -eq 0 ]]; then
    echo "ERROR: No reviews found. Run Step 2 first."
    exit 1
fi

# --- Helper: extract value from review ---
extract_rating() { grep -oP '(?<=^\*\*Overall Rating:\*\* ).*' "$1" 2>/dev/null || echo "N/A"; }
extract_confidence() { grep -oP '(?<=^\*\*Confidence:\*\* ).*' "$1" 2>/dev/null || echo "N/A"; }
extract_section() {
    # Extract content between two markdown headings
    awk "/^## ${2}/,/^## /" "$1" | tail -n +2 | sed '/^## /,$d' | sed '/^$/d' | head -20
}

# --- Build report ---
{
    echo "# Aggregate Review Report"
    echo ""
    echo "**Generated:** ${DATE_STR}"
    echo "**Reviews collected:** ${REVIEW_COUNT}/5"
    echo ""
    echo "---"
    echo ""

    # === Reviewer Overview Table ===
    echo "## Reviewer Overview"
    echo ""
    echo "| # | Name | Domain | Expertise | Rating | Confidence |"
    echo "|---|------|--------|-----------|--------|------------|"

    for i in 1 2 3 4 5; do
        REVIEW="${REVIEWS_DIR}/reviewer${i}/review.md"
        if [[ -f "$REVIEW" ]]; then
            NAME=$(head -3 "$REVIEW" | grep -oP '(?<=^\*\*Reviewer:\*\* ).*?(?= \()' 2>/dev/null || echo "Reviewer ${i}")
            DOMAIN=$(head -3 "$REVIEW" | grep -oP '(?<=Domain: ).*?(?=,)' 2>/dev/null || echo "N/A")
            EXPERTISE=$(head -3 "$REVIEW" | grep -oP '(?<=Expertise: ).*?(?=\))' 2>/dev/null || echo "N/A")
            RATING=$(extract_rating "$REVIEW")
            CONFIDENCE=$(extract_confidence "$REVIEW")
            echo "| ${i} | ${NAME} | ${DOMAIN} | ${EXPERTISE} | ${RATING} | ${CONFIDENCE} |"
        else
            echo "| ${i} | *(missing)* | — | — | — | — |"
        fi
    done

    echo ""
    echo "---"
    echo ""

    # === Rating Matrix ===
    echo "## Rating Matrix"
    echo ""
    echo "| Criterion | R1 | R2 | R3 | R4 | R5 |"
    echo "|-----------|---|---|---|---|---|"

    CRITERIA=("Problem Significance" "Design Quality" "Implementation" "Evaluation" "Presentation")
    # Try AI-paper criteria if system criteria not found
    if ! grep -q "Problem Significance" "${REVIEWS_DIR}/reviewer1/review.md" 2>/dev/null; then
        CRITERIA=("Novelty" "Technical Quality" "Empirical Rigor" "Clarity" "Significance")
    fi

    for crit in "${CRITERIA[@]}"; do
        ROW="| ${crit} |"
        for i in 1 2 3 4 5; do
            REVIEW="${REVIEWS_DIR}/reviewer${i}/review.md"
            if [[ -f "$REVIEW" ]]; then
                VAL=$(grep -P "^\|.*${crit}.*\|" "$REVIEW" | grep -oP '\| *([0-9]+) *\|' | head -1 | grep -oP '[0-9]+' || echo "—")
                ROW="${ROW} ${VAL} |"
            else
                ROW="${ROW} — |"
            fi
        done
        echo "$ROW"
    done

    echo ""
    echo "---"
    echo ""

    # === Per-Reviewer Details ===
    echo "## Per-Reviewer Details"
    echo ""

    for i in 1 2 3 4 5; do
        REVIEW="${REVIEWS_DIR}/reviewer${i}/review.md"
        QA_LOG="${REVIEWS_DIR}/reviewer${i}/qa-log.md"

        if [[ ! -f "$REVIEW" ]]; then
            echo "### Reviewer ${i} — *(review not found)*"
            echo ""
            continue
        fi

        NAME=$(head -3 "$REVIEW" | grep -oP '(?<=^\*\*Reviewer:\*\* ).*?(?= \()' 2>/dev/null || echo "Reviewer ${i}")
        echo "### Reviewer ${i}: ${NAME}"
        echo ""

        # --- Profile snippet ---
        echo "<details><summary><b>Profile</b></summary>"
        echo ""
        awk "/^## Reviewer ${i}:/,/^## Reviewer $((i+1)):/" "$PROFILES" 2>/dev/null | head -n -1 || echo "*(profile not found)*"
        echo ""
        echo "</details>"
        echo ""

        # --- Review summary ---
        echo "<details><summary><b>Review Summary</b></summary>"
        echo ""
        SUMMARY=$(extract_section "$REVIEW" "Paper Summary")
        STRENGTHS=$(extract_section "$REVIEW" "Strengths")
        WEAKNESSES=$(extract_section "$REVIEW" "Weaknesses")
        QUESTIONS=$(extract_section "$REVIEW" "Questions for Authors")
        RATING=$(extract_rating "$REVIEW")
        CONFIDENCE=$(extract_confidence "$REVIEW")

        echo "**Summary:** ${SUMMARY}"
        echo ""
        echo "**Rating:** ${RATING} (Confidence: ${CONFIDENCE})"
        echo ""
        echo "**Key Strengths:**"
        echo "${STRENGTHS}"
        echo ""
        echo "**Key Weaknesses:**"
        echo "${WEAKNESSES}"
        echo ""
        echo "**Questions for Authors:**"
        echo "${QUESTIONS}"
        echo ""
        echo "</details>"
        echo ""

        # --- Full review ---
        echo "<details><summary><b>Full Review</b></summary>"
        echo ""
        cat "$REVIEW"
        echo ""
        echo "</details>"
        echo ""

        # --- QA log ---
        if [[ -f "$QA_LOG" ]]; then
            QA_COUNT=$(grep -c '^## Q[0-9]' "$QA_LOG" 2>/dev/null || echo "0")
            echo "<details><summary><b>QA Log (${QA_COUNT} exchanges)</b></summary>"
            echo ""
            cat "$QA_LOG"
            echo ""
            echo "</details>"
            echo ""
        fi

        echo "---"
        echo ""
    done

    echo "## Quick Summary"
    echo ""
    echo "| Rating | Count |"
    echo "|--------|-------|"
    for r in "Accept" "Weak Accept" "Weak Reject" "Reject"; do
        COUNT=0
        for i in 1 2 3 4 5; do
            REVIEW="${REVIEWS_DIR}/reviewer${i}/review.md"
            if [[ -f "$REVIEW" ]]; then
                R=$(extract_rating "$REVIEW")
                if [[ "$R" == "$r" ]]; then COUNT=$((COUNT + 1)); fi
            fi
        done
        echo "| ${r} | ${COUNT} |"
    done

} > "$OUTPUT"

echo "Aggregate report written to: ${OUTPUT}"
echo "Reviews collected: ${REVIEW_COUNT}/5"

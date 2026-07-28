---
name: paper-extract
description: Use when extracting and analyzing academic papers from PDF or LaTeX sources. Use when the user provides a paper, asks to analyze a paper, understand a paper's contributions, decompose a paper into HLS components, or needs a structured paper breakdown with Overview, Big Background, Small Background, Problems, Root Cause, Key Idea, Design Points, and System evaluation.
---

# Paper Extract — Reverse HLS Decomposition

## Overview

Inverse of paper-writing HLS: decomposes a paper into HLS components for deep understanding, gap identification, and research positioning. Where paper-writing builds paper from ideas (L0→L1→L2→L3), paper-extract extracts HLS from an existing paper.

## When to Use

Decision flowchart → [references/decision-flow.md](references/decision-flow.md).

**Use when:** user provides PDF/LaTeX to analyze; literature review; pre-review deep read; gap identification; paper comparison.

**Don't use for:** writing → paper-writing; reviewer feedback → paper-review; figures → paper-plot.

## Process Flow

| Phase | Role | Output |
|-------|------|--------|
| **E0** | **Extractor** — text + figures from PDF/LaTeX | `output/analysis/` |
| **E1** | **Decomposer** — HLS 7+1 core points with evidence | `output/results/hls-L0.md` |
| **E1.5** | **Condenser** — TLDR, Abstract+Intro only | `output/results/tldr.md` |
| **E2** | **Architect** — Section flow chains | `output/results/hls-L1.md` |
| **E3** | **Critic** — innovation, gaps, positioning | `output/analysis/critical-assessment.md` |

Output layout → [references/extraction-guide.md](references/extraction-guide.md).

## Hard Gates

<HARD-GATE-E0>
Full text + figure PNGs + captions + references extracted. Verify `output/analysis/full-text.md` and `figures/` exist.
</HARD-GATE-E0>

<HARD-GATE-E1>
ALL 7+1 points in `hls-L0.md` with evidence citations. Descriptive, not evaluative. Overview ≤5 sentences. Key Idea = 1 sentence.
</HARD-GATE-E1>

<HARD-GATE-E1.5>
TLDR from Abstract+Intro ONLY. Structured sub-points (1)(2)(3) per section, each 1-2 sentences. No citations, no `[MISSING]` flags.
</HARD-GATE-E1.5>

<HARD-GATE-E2>
Each Section's A→B→C chain + figure placements + dependency graph. User confirms.
</HARD-GATE-E2>

<HARD-GATE-E3>
Innovation level + 3 strengths + 3 weaknesses + gap analysis + positioning map. Every claim cites paper text.
</HARD-GATE-E3>

## E1: The 7+1 Core Points

| # | Point | Question Answered | Paper Section Clue |
|---|-------|-------------------|-------------------|
| **1** | **Overview** | What does this paper do in one paragraph? | Abstract + Introduction |
| **2** | **Big Background** | What broad research wave/trend enables this? | Introduction ¶1-2 |
| **3** | **Small Background** | What specific prior work does this directly extend? | Introduction ¶3-4, Related Work |
| **4** | **Problems** | What concrete problems does this paper solve? | Introduction (gap statements), Problem Formulation |
| **5** | **Root Cause** | What fundamental bottleneck underlies all problems? | Motivation, Design Rationale |
| **6** | **Key Idea** | What is the ONE core insight? (≤1 sentence) | Introduction (thesis statement), Contribution list |
| **7** | **Design Points** | What are the 2-5 technical contributions? | Method/Design/Architecture sections |
| **+1** | **System & Experiment** | How was it implemented and evaluated? | Implementation, Evaluation |

For each point: state claim → cite evidence (quote or section:paragraph) → flag `[MISSING]` if no evidence found.

## E1.5: TLDR

Structured (1)(2)(3) sub-points per section, 1-2 sentences each. Abstract+Intro ONLY. Template → [references/tldr-format.md](references/tldr-format.md).

## E2: Section Flow Chains

For each Section: name, purpose, A→B→C chain, figure refs to `output/analysis/figures/`, dependencies. Dependency graph → [references/extraction-guide.md](references/extraction-guide.md).

## E3: Critical Assessment

Innovation level (Breakthrough/Novel/Incremental/Engineering), 3+ strengths/weaknesses, gap analysis, positioning map (approach type × scope, 3-5 prior works). Details → [references/extraction-guide.md](references/extraction-guide.md).

## Quick Reference

| User says | Trigger mode |
|-----------|-------------|
| "Analyze this paper" | E0→E1→E1.5→E2→E3 |
| "Give me a quick summary" | E0→E1→E1.5 |
| "Just the TLDR" | E0→E1.5 |
| "What's the core idea?" | E0→E1 (Key Idea + Design Points) |
| "Find the gaps" | E0→E1→E3 (Gap Analysis) |
| "Compare these two papers" | Full pipeline on both, side-by-side |
| "Is this paper good?" | E0→E1→E3 (Strengths/Weaknesses) |

## Source Type Handling

**PDF:** `scripts/extract-pdf.py <paper.pdf> --output output`
**LaTeX:** `scripts/extract-latex.py <main.tex> --output output`

Details → [references/extraction-guide.md](references/extraction-guide.md). Run scripts with `--help` for options.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| **Summarizing instead of decomposing** | Each HLS point is a distinct dimension |
| **Evaluating during E1** | E1 = descriptive only. Judgment → E3 |
| **Fabricating missing points** | Mark `[MISSING]` — don't invent |
| **Confusing Problems with Root Cause** | Problems = what's broken; Root Cause = WHY |
| **Skipping evidence citations** | Every hls-L0.md point MUST cite paper text |
| **Relying on captions alone** | Extract figure images to `figures/` for visual inspection |
| **TLDR using full paper** | TLDR = Abstract+Intro ONLY |
| **TLDR as single blob paragraph** | Must use (1)(2)(3) line breaks — never a wall of text |

## Cross-Skill Integration

| Skill | Relationship |
|-------|-------------|
| **paper-writing** | Inverse: paper→HLS vs HLS→paper |
| **paper-review** | E3 feeds into review dimensions |
| **analyze-plot** | E2 figure maps guide regeneration |

---

**REQUIRED BACKGROUND:** paper-writing's HLS framework (L0 core points, L1 flow chains).

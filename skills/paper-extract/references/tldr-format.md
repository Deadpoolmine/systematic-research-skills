# TLDR Format Reference

**Load when:** generating `output/results/tldr.md` during E1.5.

## Template

```markdown
# TLDR — [Paper Title]

**Authors:** [authors]
**Venue:** [venue, year]

## Overview
(1) [1-2 sentences — what problem does this paper solve?]
(2) [1-2 sentences — what is the key approach?]
(3) [1-2 sentences — what is the main result?]

## Big Background
(1) [What broad research trend/movement enables this work?]
(2) [What technological shift or inflection point is relevant?]
(3) [Why is now the right time for this work?]

## Small Background
(1) [Closest prior work A — what gap does it leave?]
(2) [Closest prior work B — what gap does it leave?]
(3) [Closest prior work C — what gap does it leave?]

## Problems
(1) [Concrete problem 1 the paper addresses]
(2) [Concrete problem 2 the paper addresses]
(3) [Concrete problem 3 — if fewer than 3, list what exists]

## Root Cause
(1) [Fundamental bottleneck underlying the problems]
(2) [Why existing approaches can't address this bottleneck]
(3) [What constraint must be relaxed to solve it?]
[NOT STATED] if the paper omits Root Cause entirely from Abstract/Introduction.

## Key Idea
(1) [The ONE core insight — stated as a clear claim]
(2) [How this insight differs from prior assumptions]
(3) [Why this insight leads to a solution]

## Design Points
(1) [Design point 1 — specific technical mechanism]
(2) [Design point 2 — specific technical mechanism]
(3) [Design point 3 — list 2-5 total, one per sub-point]

## System & Experiment
(1) [Implementation scale/scope — e.g., "Implemented as an X with Y lines of code"]
(2) [Evaluation setup — datasets, baselines, metrics]
(3) [Key result — the single most compelling number or finding]
```

## Rules

- **Source restriction:** Abstract + Introduction ONLY. Do NOT consult Method, Evaluation, or Conclusion.
- **Structured sub-points:** Each of the 8 sections uses `(1)`, `(2)`, `(3)` — each on its own line for readability.
- **Sub-point count:** 2-3 sub-points per section. If the paper only has 1-2 problems, list what exists — don't fabricate.
- **No citations:** No `[1]`, `Author et al.`, or reference markers.
- **No evidence markers:** No `[MISSING]` flags. Use `[NOT STATED]` only for Root Cause when the paper omits it.
- **No bullet lists or markdown lists:** Use plain `(1)`, `(2)`, `(3)` — these are scan-friendly line breaks, not markdown rendering.
- **Pure condensed claims:** Each sub-point is 1-2 sentences. The essence without justification — a reader scans vertically.
- **Write for a reader who has NOT read the paper:** TLDR must be self-contained.
- **TLDR is distinct from hls-L0.md:** hls-L0 has evidence citations and multi-paragraph exposition. TLDR has structured, scannable sub-points.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| **Using Method/Evaluation content** | TLDR = Abstract + Introduction only. Results live in hls-L0.md. |
| **Single blob paragraph** | Must use `(1)` `(2)` `(3)` line breaks — never a single wall of text. |
| **Adding citations** | TLDR has zero citations. Move all references to hls-L0.md. |
| **Copying hls-L0.md verbatim** | TLDR is a fresh structured condensation with sub-points. |
| **Skipping Root Cause** | If not in Abstract/Intro, write `[NOT STATED]` — don't leave empty. |
| **Missing a section** | All 8 sections (7+1) are required even if some have only 1-2 sub-points. |

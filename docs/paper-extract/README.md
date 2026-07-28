# Paper Extract — Reverse HLS Decomposition

Decompose any academic paper (PDF/LaTeX) into its core ideas, narrative architecture, and critical assessment — in one command.

## Quick Start

In any conversation:

```
/paper-extract analyze Helmsman@OSDI'26.pdf
```

The agent runs 5 phases automatically:

| Phase | What It Does | Output |
|-------|-------------|--------|
| **E0 Extract** | Pull full text, export figure PNGs, capture references | `output/analysis/` |
| **E1 Decompose** | Map paper to 7+1 HLS core points with evidence citations | `output/results/hls-L0.md` |
| **E1.5 Condense** | Structured TLDR from Abstract+Intro only | `output/results/tldr.md` |
| **E2 Reconstruct** | Recover Section A→B→C narrative chains + dependency graph | `output/results/hls-L1.md` |
| **E3 Critique** | Innovation level, strengths/weaknesses, gap analysis, positioning map | `output/analysis/critical-assessment.md` |

## Output Structure

After completion, `output/` looks like this:

```
output/
├── analysis/                          # Raw extraction artifacts
│   ├── full-text.md                   # Full text with section markers + page numbers
│   ├── figures.md                     # Figure/table index: captions, context, image previews
│   ├── figures/                       # Extracted figure images (PNG, 200 DPI)
│   │   ├── fig-01.png
│   │   └── fig-02.png
│   ├── references.md                  # Bibliography
│   ├── metadata.json                  # Title, authors, abstract
│   └── critical-assessment.md         # E3: critical assessment report
│
└── results/                           # HLS analysis ★ primary deliverables
    ├── hls-L0.md                      # Full 7+1 core points with paper citations
    ├── hls-L1.md                      # Section narrative chains + dependency graph
    └── tldr.md                        # One-page scan: (1)(2)(3) sub-points per section
```

### Primary Deliverables

**`results/tldr.md`** — Read this first. Structured sub-points, everything from Abstract+Intro only:

```markdown
## Big Background
(1) Large language models are driving demand for scalable inference infrastructure...
(2) Transformer compute patterns are shifting from pure matmul to mixed attention...
(3) Existing systems face memory-wall and communication bottlenecks on GPU clusters...

## Small Background
(1) vLLM — solves single-GPU KV-cache management, but does not address multi-node...
(2) Sarathi-Serve — introduces chunked preemption, but scheduling granularity is coarse...

## Key Idea
(1) Semantic-aware scheduling can eliminate redundant KV-cache recomputation...
(2) Unlike prior work that treats all requests uniformly, Helmsman clusters by attention pattern...
(3) This insight reduces cross-node communication by treating similar requests as a fused batch...
```

**`results/hls-L0.md`** — Deep analysis. Each core point includes:
- Extracted claim in plain language
- Source citation (Section:Paragraph)
- `[MISSING]` flag if the paper omits a dimension (e.g., no explicit Root Cause)

**`results/hls-L1.md`** — Narrative architecture. Each Section includes:
- Section name and argument purpose
- A→B→C logical flow (e.g., Motivation → Design → Justification)
- Figure placement and narrative role
- Inter-section dependency graph

### Supporting Artifacts

**`analysis/critical-assessment.md`** — Critical evaluation:
- Innovation level: Breakthrough / Novel / Incremental / Engineering
- 3+ strengths + 3+ weaknesses
- Gap analysis: what the paper does NOT solve
- Positioning map: 2D comparison vs. 3–5 closest prior works

**`analysis/figures/`** — Figure image extraction:
- PDF papers: pages rendered at 200 DPI, cropped to figure regions
- LaTeX sources: `\includegraphics` paths extracted, surrounding context captured

## Common Usage Patterns

| What You Want | Example |
|---------------|---------|
| Quick scan only | `/paper-extract give me the TLDR for Helmsman.pdf` |
| Find research gaps | `/paper-extract what gaps does Helmsman.pdf leave open?` |
| Compare two papers | `/paper-extract compare Helmsman.pdf and vLLM.pdf` |
| Quality assessment | `/paper-extract is Helmsman.pdf a good paper?` |
| LaTeX source | `/paper-extract analyze main.tex` |

## Dependencies

Python 3 required. For PDF figure extraction:

```bash
pip install PyPDF2 pdfplumber Pillow
```

LaTeX extraction uses stdlib only — no extra dependencies.

## Related Skills

| Skill | Relationship |
|-------|-------------|
| **paper-writing** | Inverse of paper-extract: HLS → paper |
| **paper-review** | paper-extract's E3 feeds directly into review dimensions |
| **paper-plot** | paper-extract's E2 figure maps guide figure regeneration |

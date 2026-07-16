# L2 — Parallel Writing Stream (The Builder Phase)

**Load when:** executing L2. Writing protocol and skeleton usage.

**REQUIRED BACKGROUND:** SKILL.md hard gates. L1 must be complete.

## Checklist

1. **Discover skeleton** — explore `templates/` to find the category and format matching the venue (from L0). Read its `README.md` for format constraints.
2. **Discover writing guide** — `writing-guide.md` in the same category directory. Voice, conventions, per-section pitfalls.
3. **Copy skeleton to `paper/`** — `cp -r <skeleton-path> paper/`. Never edit skeleton in-place.
4. **For each L1 Section:** create `paper/sections/<Name>.tex` → add `\input` to `paper/main.tex` → draft following L1 flow chain AND writing guide.
5. **Execute figure placeholders:** for each `[Figure: ...]` in L1 → insert full LaTeX `\begin{figure}...\end{figure}` with draft caption and `\label{}`. Placeholder PDF in `paper/figs/`.
6. **Draft mode:** if experiments incomplete → `[TODO: actual number]` for pending data. Setup and methodology must be complete.
7. **Self-check** each Section against writing guide pitfalls before user review.
8. **Add references** to `paper/references.bib` as cited.

## Skeleton Rules

- Read-only. Never edit inside `templates/`.
- `sections/` and `figs/` contain only `.gitkeep` — fill during L2.
- AAAI: `\input` forbidden → write all sections inline in `main.tex`.

## Figure Convention

```latex
% [Figure: Architecture overview — components and data flow]
\begin{figure}[t]
    \centering
    \includegraphics[width=\columnwidth]{figs/architecture.pdf}
    \caption{Architecture overview. ...}
    \label{fig:architecture}
\end{figure}
```

Every figure must trace to an L1 `[Figure: ...]` marker. Text references before display (`Figure~\ref{...}`).

## Transition

Commit `paper/` with `L2: draft for <topic>`. Proceed to L3.

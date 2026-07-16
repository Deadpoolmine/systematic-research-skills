# AAAI Conference Skeleton

## Format Constraints
- **Class:** `article` with `aaai2026.sty`
- **Page limit:** **7 pages** (submission), **8 pages** (camera-ready with +1)
- **Column:** two-column (`letterpaper`)
- **References:** unlimited
- **Style:** `\bibliographystyle{aaai2026}`
- **CRITICAL:** Single `.tex` file — `\input` forbidden
- **Forbidden packages:** hyperref, float, titlesec, geometry, fullpage, setspace, ulem, wrapfig, tabu, authblk, balance, flushend, fontenc, grffile, navigator, savetrees, stfloats, tocbibind, multicol, indentfirst, layout, nameref

## Typical Venues
AAAI, IJCAI

## Directory Structure
```
aaai/
├── CameraReady/LaTeX/     # Final submission (with author block)
├── AnonymousSubmission/   # Review submission (anonymous)
│   ├── LaTeX/
│   └── sections/          # Drafting stubs — merge into main.tex
└── Copyright/             # AAAI copyright forms
```

## General Chapter Planning
AAAI papers typically follow:
1. Introduction
2. Related Work
3. Preliminaries
4. Method
5. Experiments
6. Discussion
7. Conclusion

## Required Files
This skeleton contains `aaai2026.sty`, `aaai2026.bst`, `aaai2026.bib` placeholder, `main.tex` for both CameraReady and AnonymousSubmission, and AAAI copyright forms. Copy to `paper/` to begin writing.

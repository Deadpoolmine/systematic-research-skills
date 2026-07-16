# ACM SigConf Skeleton

## Format Constraints
- **Class:** `acmart.cls` (ACM Primary Article Template, sigconf format)
- **Page limit:** varies by venue (typically 10-12 pages)
- **Column:** two-column
- **References:** unlimited
- **Style:** `\bibliographystyle{ACM-Reference-Format}`
- **Submission mode:** `\documentclass[sigconf,10pt,review,anonymous,screen]{acmart}`
- **Camera-ready:** `\documentclass[sigconf,10pt]{acmart}`

## Typical Venues
EuroSys, ASPLOS, SIGCOMM, ISCA, MICRO, and other ACM SIG conferences

## General Chapter Planning
ACM SIG papers typically follow:
1. Introduction
2. Background
3. Motivation / Observations
4. Design
5. Implementation
6. Evaluation
7. Related Work
8. Discussion / Limitations
9. Conclusion

## Required Files
This skeleton contains `acmart.cls`, `ACM-Reference-Format.bst`, BibLaTeX files (bbx/cbx/dbx), a `main.tex` preamble, `references.bib` + `software.bib` placeholders, and `appendix.tex` stub. Copy to `paper/` to begin writing.

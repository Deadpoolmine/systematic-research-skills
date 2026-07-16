# 8-Page Systems Paper Blueprint

**Load this reference when:** writing an 8-page systems paper targeting HotStorage, HotOS, or short/position papers at top systems venues. Provides condensed page budget and per-section plans adapted from the 12-page blueprint.

**Skeleton:** `templates/cs/system/usenix/` (USENIX format, 8 pages)

---

## Page Budget

**All page limits exclude references.** The 8 pages are for main content only. References, appendices, and acknowledgments are extra.

| Section | Pages | Key Constraint |
|---------|-------|---------------|
| Abstract | ~0.2 | 100-150 words, 3-4 sentences |
| S1 Introduction | 1-1.5 | Must state thesis + contributions in the first 0.5 page |
| S2 Background & Motivation | 0.5-1 | Condensed — define only essential terms |
| S3 Design | 2-2.5 | Architecture overview + key design points (no deep alternatives discussion) |
| S4 Implementation | 0.3-0.5 | One paragraph: language, LOC, key engineering |
| S5 Evaluation | 2-2.5 | Setup + end-to-end only; microbenchmarks only if space permits |
| S6 Related Work | 0.5 | One paragraph grouping by methodology |
| S7 Conclusion | 0.3 | 2-3 sentence summary |
| **Total** | **~8 + refs** | References unlimited |

---

## What to Cut from 12-Page Format

| Element | 12-Page | 8-Page |
|---------|---------|--------|
| Background depth | 2-3 paragraphs per concept | 1 paragraph per concept |
| Design alternatives | Full subsection for each major choice | 1-2 sentences each |
| Microbenchmarks / ablation | 1-1.5 pages | Omit or 1 paragraph |
| Scalability analysis | 0.5 page | Omit |
| Related Work | 1 page, multiple groups | 0.5 page, 2-3 groups max |
| Motivation observations | 2-3 observations with data | 1 observation, most compelling |

---

## Per-Section Paragraph Plans (Condensed)

### Abstract (3-4 sentences)
1. Problem + gap
2. Key insight
3. Approach + key result
4. (optional) Impact

### S1 Introduction (1-1.5p)
- Problem statement: 1 paragraph with concrete numbers
- Gap: 1 paragraph — state the single most important gap
- Key insight: 1 paragraph
- Contributions: 2-3 numbered items

### S3 Design (2-2.5p)
- Architecture overview: figure + 1-paragraph walkthrough
- Each design point: what → why → connection to key idea (0.5-0.7p each)
- Skip alternatives section; discuss inline

### S5 Evaluation (2-2.5p)
- Setup: 1 paragraph (hardware, baselines, workloads, methodology)
- End-to-end: 1-1.5 pages
- Skip microbenchmarks unless space allows

---

## Quality Checklist

- [ ] Thesis stated in first 0.5 page
- [ ] Every design point traces to key idea
- [ ] Evaluation setup is reproducible
- [ ] Page budget within 8 pages
- [ ] No filler — every paragraph earns its space

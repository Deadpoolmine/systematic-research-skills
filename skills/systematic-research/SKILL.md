---
name: systematic-research
description: Use when conducting systematic research from web or academic sources. Use when the user asks to research a topic, search for information, gather knowledge, build a knowledge base, or needs structured research output with provenance tracking and HLS decomposition.
---

# Systematic Research — HLS Knowledge Extraction Wrapper

## Overview

This skill handles **search + download**. Decomposition is delegated to `paper-extract`.

Pipeline: **R0: search & download → paper-extract E0→E1→E1.5→E2 → R3: verify**.

**CRITICAL: No direct generation. No manual construction.** Every item follows: search → download source → extract from source. Never fabricate content.

**CRITICAL: results.json is READ-ONLY after search.** Never manually construct, edit, or "enrich" results.json entries. If search results are insufficient, re-run search with better queries — never invent entries. Authors, titles, summaries, DOIs, and all metadata MUST come exclusively from executed search script output.

**Don't use for:** single-paper analysis → `paper-extract`; writing → `paper-writing`.

## Anti-Hallucination Rules (ALWAYS ACTIVE)

These rules apply to ALL phases and override any conflicting instructions:

1. **`results.json` is immutable.** After search scripts produce `results.json`, you may merge/dedup entries from multiple search engines, but you MUST NOT:
   - Add entries not present in any search output
   - Change authors, titles, summaries, or DOIs
   - "Enrich" entries with fabricated metadata
   - Manually construct entries in a Python script (e.g., `combine_results.py`)

2. **Source-API cross-verification (R0-d).** After building `results.json`, for every entry:
   - Query the source API (arXiv/DOI/OpenAlex) with the entry's identifier
   - Verify: authors (first 3), title (first 80 chars), summary/abstract (semantic match)
   - Flag MISMATCHes and fix from source API data ONLY
   - If source API is unreachable for an entry, mark it `"verified": false` and note the risk

3. **Field provenance.** Every field in `results.json` must be traceable to either:
   - A search script output file, OR
   - A source API response (for R0-d corrections)
   - Never to the model's internal knowledge

4. **When search fails,** re-run with different queries or engines. Never fall back to manual construction.

## Process Flow

| Phase | Who | What | Template |
|-------|-----|------|----------|
| **R0** | This skill | Execute multi-engine search → merge & dedup → cross-verify with source API → download | — |
| **R0-d** | This skill | Cross-verify: query source API for each entry, validate authors/title/summary | — |
| **E0** | `paper-extract` | Extract full text from downloaded source | — |
| **E1** | `paper-extract` | Decompose to 7+1 core points → `l0.md` | `../../paper-extract/templates/l0.md` |
| **E1.5** | `paper-extract` | Condensed TLDR → `tldr.md` | `../../paper-extract/templates/tldr.md` |
| **E2** | `paper-extract` | Section flow chains → `l1.md` | `../../paper-extract/templates/l1.md` |
| — | This skill | BibTeX citation → `bibentry.bib` (use `bibtexparser`) | — |
| — | This skill | Aggregate → `collect-bib.py` | — |
| **R3** | This skill | Verify → `verify-results.py` | — |

Output format → `../../paper-extract/references/okf-format.md`.
Paper-extract ref → `../../paper-extract/SKILL.md` (templates: `../../paper-extract/templates/`).

## Item Directory

```
knowledge/<category>/<subcategory>/<item>/
  source.pdf         # ← downloaded material (mandatory)
  tldr.md            # ← paper-extract E1.5
  l0.md              # ← paper-extract E1
  l1.md              # ← paper-extract E2
  bibentry.bib       # ← bibtexparser
```

## Hard Gates

<HARD-GATE-R0>
**R0-a: Search.** Search **multiple engines in parallel** for comprehensive coverage:
  1. List `scripts/search-*.py` and `search-engines/` to discover available engines
  2. Execute ALL matching engines in parallel (e.g., cs topic → arXiv + OpenAlex + USENIX)
  3. Merge `results.json` files, dedup by URL/DOI
  4. For domain-specific research, always pair domain engines with general engines

Output: merged `results.json`. ALL data MUST come from executed scripts.
Never hardcode engine choice — always discover from the filesystem first.

**R0-a-verify: Anti-Hallucination Cross-Check.** After merge, for EVERY entry in `results.json`:
  - Extract the entry's identifier (arxiv_id, DOI, or URL)
  - Query the source API directly (arXiv API, CrossRef DOI, or OpenAlex)
  - Compare: authors (≥3 match), title (≥80% prefix match), summary (semantic overlap)
  - If MISMATCH: replace with source API data, DO NOT keep fabricated version
  - If API unreachable: mark `"verified": false` in the entry
  - Implementation: `python scripts/verify-against-source.py results.json --fix`

This gate MUST pass before proceeding to R0-b (download). Never skip.

**R0-b: Download.** For EACH result in `results.json`, download the source material:
  - `python scripts/download-source.py "<url>" --output knowledge/<category>/<subcategory>/<item>/`
  - Verify `source.pdf` (or `source.html`) exists and is non-empty.
  - Never skip this step. No download = no extraction.

**R0-c: BibTeX.** Generate `bibentry.bib` using `bibtexparser`. Format → `../../paper-extract/references/okf-format.md`. URL/DOI MUST match `results.json`.
</HARD-GATE-R0>

<HARD-GATE-E1>
**Delegated to paper-extract.** See `../../paper-extract/SKILL.md` for E0→E1→E1.5→E2 hard gates.
Paper-extract uses its own OKF templates (`../../paper-extract/templates/`). Copy its output files:
  - `l0.md` → `l0.md` (template: `../../paper-extract/templates/l0.md`)
  - `tldr.md` → `tldr.md` (template: `../../paper-extract/templates/tldr.md`)
  - `l1.md` → `l1.md` (template: `../../paper-extract/templates/l1.md`)
</HARD-GATE-E1>

<HARD-GATE-R3>
Run `python scripts/verify-results.py knowledge/<category>/<subcategory>/`:
- `source.pdf` (or source.html) exists and is non-empty
- `tldr.md`, `l0.md`, `l1.md`, `bibentry.bib` all present
- `bibentry.bib` URL/DOI traceable to `results.json`
- **`bibentry.bib` authors match `results.json` (not just URL — check at least first author)**
All checks must pass before declaring complete.

**Post-R3: Spot-check decomposition quality.** Random-sample 2-3 `tldr.md`/`l0.md` files:
- Verify system names (e.g., \"FlyTrap\" not \"PMFuzz\") match the actual paper
- Verify key claims cite real sections from the paper
- If errors found, flag all entries from the same batch for review
</HARD-GATE-R3>

## Quick Reference

| User says | Pipeline |
|-----------|----------|
| "Research X" | R0→E1→E1.5→R3 |
| "Research X deeply" | R0→E1→E1.5→E2→R3 |
| "Quick research on X" | R0→E1.5→R3 |

## Source Scripts

Discover available engines at runtime — list `scripts/` and `search-engines/` to see what's available.

General engines (`scripts/`):

| Script | Source | Best For |
|--------|--------|----------|
| `search-web.py` | DuckDuckGo | News, blogs, general web |
| `search-academic.py` | OpenAlex | Published papers, cross-domain |
| `search-arxiv.py` | arXiv API | CS/AI/ML preprints |

Domain engines (`search-engines/`): list directory to discover. Currently: `cs/system/search-usenix.py`, more added over time.

Match engine to topic: `cloud infrastructure` → USENIX/OpenAlex, `transformer attention` → arXiv, `market trends` → Web.

## Verification

```bash
python scripts/verify-results.py knowledge/<category>/<subcategory>/
```

Checks: source material exists, all output files present, URL/DOI consistency.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Generating content without downloading source | R0-b is mandatory; no source.pdf = stop |
| Hallucinating search results | Execute script; read `results.json` |
| **Manually constructing `results.json` entries** | **NEVER write scripts like `combine_results.py` that hardcode paper metadata. All data must come from search script output or source API.** |
| **Fabricating authors/summaries** | **Run R0-d cross-verification against source API. If entry fails, replace with API data or remove.** |
| **Using wrong system names in decomposition** | **Post-R3 spot-check: verify tldr.md/l0.md system names against the paper abstract.** |
| Writing own decomposition instead of paper-extract | Delegate to paper-extract; only copy its output files |
| Missing source material | Run `download-source.py` before extraction |
| Title-URL mismatch | Run `verify-results.py` |
| **Skipping R0-d cross-verification** | **R0-d is mandatory. Unverified results.json = stop. No exceptions.** |

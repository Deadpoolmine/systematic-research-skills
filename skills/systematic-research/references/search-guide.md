# Search Guide

**Load when:** executing R0 retrieval.

## Search Sources

### 1. General Search Scripts (`scripts/`)

#### Web Search

```
scripts/search-web.py "<query>" --limit N --output <dir>
```

Uses DuckDuckGo (no API key required). Returns: title, URL, snippet, retrieved timestamp.

#### Academic Search (OpenAlex)

```
scripts/search-academic.py "<query>" --limit N --year-from YYYY --output <dir>
scripts/search-academic.py "<query>" --quality strict --skip-low-cited 5
```

Uses OpenAlex API (free, no key). Returns: title, authors, journal, year, DOI, abstract, cited_by_count, type, source_type.

**Quality filters (on by default):**
- Default: only `journal-article` + `proceedings-article` (peer-reviewed types) — excludes preprints, book chapters, letters, editorials
- `--quality strict`: above + cited_by > 0 (exclude uncited papers)
- `--skip-low-cited N`: exclude papers with < N citations
- Sorted by `cited_by_count:desc` to surface influential works

#### arXiv Search

```
scripts/search-arxiv.py "<query>" --limit N --category cs.AI --year-from YYYY --output <dir>
scripts/search-arxiv.py "<query>" --published-only            # only papers with DOI/journal_ref
```

Uses [arXiv API](https://info.arxiv.org/help/api/index.html) (free, no key, ATOM XML). Returns: title, authors, summary (abstract), arxiv_id, pdf_url, year, categories, doi, journal_ref, is_published.

**Quality notice:** arXiv contains preprints (not peer-reviewed). Use `--published-only` to filter to papers with DOI/journal reference. Cross-check all arXiv results against published versions.

### 2. Domain Search Engines (`search-engines/`)

Venue-specific scrapers for targeted conference/journal search.

#### USENIX (`search-engines/cs/system/`)

```
search-engines/cs/system/search-usenix.py osdi --year 2026 --output <dir>
search-engines/cs/system/search-usenix.py atc --year 2025,2024 --limit 100 --output <dir>
```

Supported: OSDI, ATC, NSDI, FAST, EuroSys, and more.

### 3. Multi-Agent Parallel Processing

After R0 search produces `results.json`, dispatch **one subagent per result** in parallel:

1. R0 runs search engine(s) → `results.json` with N items
2. For each item → launch a subagent that fetches full content + runs R1+R1.5+R2
3. All subagents run in parallel
4. After all complete → aggregate with `collect-bib.py` + write `summary/`

```
R0 Search → results.json (N items)
  ├─ Subagent 1: fetch + decompose item 1 → item1/tldr.md, l0.md, l1.md, bibentry.bib
  ├─ Subagent 2: fetch + decompose item 2 → item2/tldr.md, l0.md, l1.md, bibentry.bib
  └─ Subagent N: fetch + decompose item N → ...
→ Aggregate: collect-bib.py + summary/index.md
```

## Output Format

Each search produces a JSON results file in `<subcategory>/`:

```json
{
  "query": "...",
  "timestamp": "...",
  "source": "web | academic",
  "results": [
    {
      "title": "...",
      "url": "...",
      "snippet": "...",
      "retrieved": "..."
    }
  ]
}
```

Agent reads results → selects relevant items → fetches full content → writes per-item folder:

```
knowledge/<category>/<subcategory>/<item>/
  tldr.md       # TLDR condensed summary
  l0.md         # L0 section-level summary
  l1.md         # L1 paragraph flow
  bibentry.bib  # BibTeX citation entry (use bibtexparser)
```

After all items processed:
- Write aggregated summary in `knowledge/<category>/<subcategory>/summary/`
- Run `scripts/collect-bib.py knowledge/<category>/` → generates `knowledge/<category>/references.bib`

## Academic Search Strategy

1. Broad keyword search → identify key papers
2. Narrow keyword search → specific direction
3. Sort by cited_by_count for seminal works
4. Sort by publication_date for latest research
5. Check references of key papers for missed works

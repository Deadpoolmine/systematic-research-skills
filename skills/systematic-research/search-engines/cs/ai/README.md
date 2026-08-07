# CS / AI — Search Engines

Domain-specific search engines for AI/ML research.

## Available Engines

| Engine | Script | Source |
|--------|--------|--------|
| **arXiv** | `../../scripts/search-arxiv.py` | [arXiv API](https://info.arxiv.org/help/api/index.html) — preprints in cs.AI, cs.LG, cs.CL, cs.CV, stat.ML |
| *(pending)* | — | NeurIPS, ICML, ICLR proceedings |

## arXiv Search

```
scripts/search-arxiv.py "diffusion models" --category cs.LG --year-from 2024 --limit 50 --output <dir>
```

Categories: `cs.AI`, `cs.LG`, `cs.CL`, `cs.CV`, `cs.NE`, `cs.IR`, `stat.ML`.

Output fields: title, authors, summary (abstract), arxiv_id, pdf_url, year, categories, doi, journal_ref.

See [../system/](../system/) for USENIX systems conference search.

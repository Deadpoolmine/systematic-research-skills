# CS — Search Engines

Computer science domain-specific search engines.

## Sub-Domains

| Domain | Path | Focus |
|--------|------|-------|
| **AI / ML** | [ai/](ai/) | arXiv (cs.AI, cs.LG, cs.CL, cs.CV), NeurIPS, ICML |
| **Systems** | [system/](system/) | USENIX proceedings (OSDI, ATC, NSDI, FAST, EuroSys) |

## Usage Pattern

Each search engine produces `results.json` → consumed by the R0 Retriever in the systematic-research pipeline:

```
search-engines/cs/system/search-usenix.py osdi --year 2026 --output knowledge/technology/osdi2026/
→ knowledge/technology/osdi2026/results.json
→ R0 reads results.json → fetches full paper content → writes per-item folder
```

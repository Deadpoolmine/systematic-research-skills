# Parallel Search Guide

**Load when:** executing Multi-Agent Parallel Search.

## When to Use

Dispatch subagents when there are ≥3 search results. Serial processing for 1-2 results.

## Pipeline

```
R0: execute search script → results.json (N items)
  For each item: download source → paper-extract E0
  ├─ Subagent 1: paper-extract E1+E1.5+E2 → tldr.md, l0.md, l1.md + bibentry.bib
  ├─ Subagent 2: paper-extract E1+E1.5+E2 → tldr.md, l0.md, l1.md + bibentry.bib
  └─ Subagent N: ...
→ R3: run verify-results.py
→ Aggregate: collect-bib.py + summary/index.md
```

## Subagent Prompt

> Process this item. The source material is already downloaded at `source.pdf`.
> 
> Run paper-extract pipeline on this file:
> - E0: already done (text extracted from downloaded source)
> - E1: decompose into 7+1 core points → write `l0.md`
> - E1.5: condensed TLDR → write `tldr.md`
> - E2: section flow chains → write `l1.md`
> - Generate BibTeX citation → write `bibentry.bib`
>
> All output goes to `knowledge/<category>/<subcategory>/<item>/`.

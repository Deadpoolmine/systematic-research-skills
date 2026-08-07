# OKF Format for Research Items

**Owned by:** `paper-extract`. Load when writing any research output in OKF format.

**Used by:** `paper-extract` (generates l0/tldr/l1), `systematic-research` (orchestrates pipeline, generates bibentry).

## Required Frontmatter

```yaml
---
type: Research                      # REQUIRED
title: "<descriptive title>"
description: "<one-line summary>"
tags: [<category>, <sub-topic>, ...]
status: draft | stable | deprecated
generated: { by: <actor>, at: <ISO 8601> }
sources:
  - id: <stable-key>
    resource: <retrieval URL>
    title: <source title>
    retrieved: <ISO 8601>
---
```

## OKF Bundle Structure

```
knowledge/
  index.md                           # Bundle root: okf_version + directory listing
  log.md                             # Update history (optional)
  <category>/
    index.md                         # Category listing with descriptions
    references.bib                    # Aggregated BibTeX — all bibentries merged
    <subcategory>/
      <search-item>/                 # One folder per search target
        source.pdf                   # Downloaded material (or source.html)
        tldr.md                      # TLDR — condensed summary (OKF)
        l0.md                        # L0 — section-level summary (OKF)
        l1.md                        # L1 — paragraph flow (OKF)
        bibentry.bib                 # BibTeX citation entry
      summary/                       # Aggregated summary for subcategory
        index.md
```

## Per-File Content

### `tldr.md` — Condensed Summary

```markdown
---
type: Research
title: "<descriptive title>"
description: "<one-line summary>"
tags: [<category>, <subcategory>]
status: draft
level: TLDR
generated: { by: <actor>, at: <ISO 8601> }
sources:
  - id: <stable-key>
    resource: <retrieval URL>
    title: <source title>
    retrieved: <ISO 8601>
---

# TLDR

**Source:** [title], [date], via [source-type]

## Overview
(1) [1-2 sentences — what is this about?]
(2) [1-2 sentences — key takeaway]

## Key Claims
(1) [Main claim 1]
(2) [Main claim 2]
(3) [Main claim 3]

## Implications
(1) [What this means / why it matters]
```

### `l0.md` — Section-Level Summary

```markdown
---
type: Research
title: "<descriptive title>"
description: "<one-line summary>"
tags: [<category>, <subcategory>]
status: draft
level: L0
generated: { by: <actor>, at: <ISO 8601> }
sources:
  - id: <stable-key>
    resource: <retrieval URL>
    title: <source title>
    retrieved: <ISO 8601>
---

# Overview
...

# Background
...

# Key Claims
...

# Evidence
...

# Implications
...

## Section: <name>
[1-2 sentence summary — descriptive, not evaluative]
Evidence: [quote or paragraph reference]
<!-- Repeat per section -->
```

### `l1.md` — Paragraph Flow

```markdown
---
type: Research
title: "<descriptive title>"
description: "<one-line summary>"
tags: [<category>, <subcategory>]
status: draft
level: L1
generated: { by: <actor>, at: <ISO 8601> }
sources:
  - id: <stable-key>
    resource: <retrieval URL>
    title: <source title>
    retrieved: <ISO 8601>
---

## Section: <name> — Flow

Purpose: [why this section exists in the argument]

| Unit | Paragraphs | What it says | Role |
|------|-----------|-------------|------|
| A | ¶1-2 | [summary] | Setup/Context |
| B | ¶3-5 | [summary] | Argument/Counter |
| C | ¶6-7 | [summary] | Resolution/Transition |
<!-- Repeat per section -->
```

### `bibentry.bib` — BibTeX Citation

Every search result MUST generate a BibTeX entry for citation purposes.

For academic sources (`@article`):

```bibtex
@article{<citation-key>,
  title     = {<title>},
  author    = {<authors>},
  journal   = {<journal>},
  year      = {<year>},
  doi       = {<DOI>},
  url       = {<URL>}
}
```

For web sources (`@misc`):

```bibtex
@misc{<citation-key>,
  title     = {<title>},
  author    = {<author or organization>},
  year      = {<year>},
  url       = {<URL>},
  note      = {Accessed: <ISO 8601>}
}
```

Citation key format: `<author-lastname><year><first-title-word>`, e.g., `huang2026clustering`.

### `references.bib` — Category-Level Aggregated BibTeX

Run `scripts/collect-bib.py knowledge/<category>/` to merge all `bibentry.bib` files across all subcategories into a single `references.bib` at the category root. This is the file you import into reference managers (Zotero, Mendeley, Paperpile) or `\bibliography{}` in LaTeX.

```
knowledge/<category>/references.bib
```

## BibTeX Generation Toolchain

Use **[python-bibtexparser](https://github.com/sciunto-org/python-bibtexparser)** (v2, MIT license) for programmatic BibTeX generation:

```python
import bibtexparser

# Build entry programmatically
entry = bibtexparser.model.Entry(
    entry_type="article",
    citation_key="huang2026clustering",
    fields=[
        ("title", "The Clustering Strikes Back: ..."),
        ("author", "Yuchen Huang and Baiteng Ma and ..."),
        ("journal", "USENIX OSDI"),
        ("year", "2026"),
    ]
)

# Write to file
library = bibtexparser.Library([entry])
bibtexparser.write_file("bibentry.bib", library)
```

Install: `pip install bibtexparser --pre`

## Provenance

Every research item MUST record `sources`:
- `resource`: The URL where content was retrieved
- `retrieved`: When the source was accessed
- `id`: Stable key for per-claim attribution via footnotes

Per-claim attribution uses markdown footnotes: `[^source-id]`

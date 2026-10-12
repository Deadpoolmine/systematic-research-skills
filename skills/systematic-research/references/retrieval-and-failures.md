# Retrieval, failures, and evidence

## Setup and discovery

Use Python 3.10+ with UTF-8 output (`PYTHONUTF8=1` on Windows terminals).
arXiv and OpenAlex search need no third-party packages. Optional engines:

```text
python -m pip install -r <skill-directory>/requirements.txt
```

OpenAlex accepts `OPENALEX_API_KEY` from the environment and sends it in an
Authorization header, not URLs or output artifacts. Anonymous access has a
smaller budget; authentication/budget errors are failures, not zero hits.
See [OpenAlex authentication](https://help.openalex.org/api/authentication/).

List scripts and engine directories, then read each script's `--help` before
dispatching. Engines do not share argument syntax. In particular, USENIX takes
a conference and years, not a free-text positional query:

```text
python <usenix-script> fast --year 2025,2024 --query snapshot --output <directory>
```

Discover the sibling `paper-extract` skill and its templates/references from the
installed skill catalog or parent directory; do not use `../../paper-extract`
from this skill root. That resolves one directory too high in normal installs.

## Search outcomes

- Exit 0 plus `status: success`: the request and parsing succeeded. `count: 0`
  means no matching hits, not a connection failure.
- Nonzero plus `search-error.json`: failed invocation; do not consume an older
  result file as this run's output. Successful old results are preserved.
- arXiv/OpenAlex/USENIX retry transport errors, HTTP 429 and 5xx up to three
  attempts. They honor bounded Retry-After values. Authentication, invalid query
  and other 4xx errors fail immediately; long Retry-After values ask for a later run.
- Never overwrite an outage with a fabricated empty result set.
- OpenAlex article/review types are candidates, not proof of peer review.
  Confirm venue/publication status against the primary source.
  The old Crossref names are not current OpenAlex types; see
  [OpenAlex work types](https://help.openalex.org/data/work-types/).

Use separate output directories per engine/run. Preserve raw outputs before
merge/dedup. Query reformulation cannot fix missing dependencies, permissions,
invalid engine arguments, or authentication; diagnose the reported cause first.

## Callable-tool fallback

If local networking is restricted, use an available built-in search/browser
tool. Save its actual returned text/structured output with query, tool name,
retrieval time and source URLs. Do not manufacture author/DOI/abstract fields
absent from that output. Record a source response separately before resolving
missing fields. This is an evidence-backed retrieval path, not permission to
fill a catalog from model memory. Do not claim exhaustive multi-engine coverage
when engines were unavailable.

## Verification and source access

Keep raw results immutable. The current `verify-against-source.py` implements
arXiv verification only: run it on a COPY of arXiv results. `--fix` may change
metadata only from the API response; retain raw input and verification logs.
For DOI/OpenAlex records, inspect the respective source API or publisher page
and save its response and a field-by-field verification record. Do not route
non-arXiv IDs into the arXiv verifier or treat unavailable APIs as a match.

If an API is blocked but an accessible primary paper/page establishes the
identity, retain that evidence and explicitly record `verification_method` and
the unavailable API. A search snippet alone cannot validate technical claims.
Unresolved identity mismatches block extraction of the affected item; continue
with independently verified items and report incomplete coverage.

Download source through the supplied downloader, or save source content returned
by an accessible browser/resource tool. Preserve actual content and provenance;
never create a dummy source file to pass checks. Analyze only the material
actually accessible, and label abstracts-only analysis accordingly.

Separate exploratory discussion from a completed knowledge library: evidence
supported discussion can continue while retrieval is incomplete. A complete
library still requires downloaded sources, extraction outputs, bibliography
and R3 checks. Never claim the whole pipeline passed on partial evidence.

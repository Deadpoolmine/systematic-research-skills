# Retrieval and Provenance Workflow

Use this workflow when the research project needs new web or academic sources.

## Systematic scope

Before searching, record the research question, databases and engines, date and
language boundaries, query log, inclusion criteria, exclusion criteria, screening
record, exclusion reasons, and stopping condition. A systematic claim requires this
protocol; an ordinary supporting search must be labeled as non-exhaustive.

For each local PDF supplied by the user, preserve its original filename and content
hash, record how it was obtained, verify title and available authors against the
document or a primary index, and keep the identity record beside extracted outputs.

## R0: Retrieval and identity

1. List `scripts/search-*.py` and `search-engines/`; read matching engines' help.
   Pair domain and general engines where available. Do not send a free-text topic
   to a conference-listing engine. Use separate output directories for each run.
2. Install optional dependencies only when needed. Read
   [retrieval-and-failures](retrieval-and-failures.md) for setup, USENIX syntax,
   output contracts, retries, and callable-tool fallback.
3. Inspect exit status. Failure is not zero hits. Nonzero invocations write
   `search-error.json`; successful invocations include `status: success` and count.
   Do not merge stale results left by failed invocations.
4. Preserve raw script or tool outputs. Merge and deduplicate by URL or DOI without
   inventing entries or fields. Every field must trace to a retrieved response.
5. Verify title, available authors, and abstract against a source API or primary
   source. Compare up to the first three authors, allowing fewer-author papers.
   Preserve the response, method, and discrepancies. API failures are not matches.
6. The bundled verifier supports arXiv only. Run it on a copy while retaining raw
   input. DOI, OpenAlex, and web items use saved source responses and verification
   records; never send unrelated identifiers to the arXiv API.
7. Download or save actual PDF or HTML content before extraction. A search snippet
   cannot support design or evaluation claims. Flag abstracts-only access.

Unresolved identity mismatches block the affected item. Continue independently
verified items and report unavailable sources or incomplete coverage.

## E: Source extraction

Read the sibling `paper-extract` skill and follow the requested E0, E1, E1.5, and E2
stages. Use E3 when the task needs innovation assessment, gaps, or positioning.
Recursively discover its templates and references; do not assume a path.
Record claims with actual sections or pages and distinguish source claims from
proposed designs or hypotheses.

Each knowledge item contains actual source material, `tldr.md`, `l0.md`, `l1.md`
when required, and `bibentry.bib`. Citation metadata must trace to retrieval or
verification evidence. Aggregate with `collect-bib.py` as needed.

## R3: Completion

Run `verify-results.py` on the knowledge subtree and retain its output. Check source
existence, required extraction files, citation URL or DOI, and author identity.
Spot-check two or three decompositions against their sources for system names,
claims, and section evidence. Correct errors before declaring the library complete.

Do not claim a complete systematic review, exhaustive search, or passed R3 until
the required sources, extraction artifacts, bibliography, and checks exist.

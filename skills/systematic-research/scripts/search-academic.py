#!/usr/bin/env python3
"""
Academic Search — search OpenAlex API for academic papers.

Prioritizes peer-reviewed publications from top venues.
Defaults to journal-article + proceedings-article types only
to exclude preprints, book chapters, and non-peer-reviewed content.

Usage:
    python search-academic.py "<query>" [--limit N] [--year-from YYYY] [--output <dir>]
    python search-academic.py "<query>" --quality strict          # top venues, highly cited
    python search-academic.py "<query>" --skip-low-cited 5        # min 5 citations

Output: JSON results file in <output>/search-results.json
"""

import sys
import os
import json
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.parse import quote, urlencode
from pathlib import Path


OPENALEX_WORKS = "https://api.openalex.org/works"

# Only peer-reviewed types by default
PEER_REVIEWED_TYPES = "journal-article|proceedings-article"


def search_academic(
    query: str,
    limit: int = 20,
    year_from: int = None,
    quality: str = "normal",
    skip_low_cited: int = 0,
) -> list[dict]:
    """Search OpenAlex API and return structured results.

    Quality levels:
      - normal: peer-reviewed only (journal + proceedings), sorted by citations
      - strict: normal + cited_by >= 1 (exclude uncited papers)
    """
    params = {
        "search": query,
        "per_page": min(limit, 200),
        "sort": "cited_by_count:desc",
    }

    filters = [f"type:{PEER_REVIEWED_TYPES}"]

    if year_from:
        filters.append(f"publication_year:>{year_from - 1}")

    if quality == "strict":
        filters.append("cited_by_count:>0")

    if skip_low_cited > 0:
        filters.append(f"cited_by_count:>={skip_low_cited}")

    params["filter"] = ",".join(filters)

    url = f"{OPENALEX_WORKS}?{urlencode(params)}"
    results = []

    try:
        req = Request(url, headers={
            "User-Agent": "systematic-research-skill/1.0 (mailto:research@example.com)"
        })
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        for work in data.get("results", [])[:limit]:
            authorship = work.get("authorships", [])
            authors = [a.get("author", {}).get("display_name", "") for a in authorship[:5]]

            source = work.get("primary_location", {}).get("source", {}) or {}
            source_display = source.get("display_name", "")
            source_type = source.get("type", "")

            results.append({
                "title": work.get("title", ""),
                "authors": authors,
                "journal": source_display,
                "year": work.get("publication_year"),
                "doi": work.get("doi", ""),
                "cited_by_count": work.get("cited_by_count", 0),
                "abstract": _truncate(work.get("abstract_inverted_index"), 500),
                "url": work.get("primary_location", {}).get("landing_page_url", ""),
                "openalex_id": work.get("id", ""),
                "type": work.get("type", ""),
                "source_type": source_type,
                "retrieved": datetime.now(timezone.utc).isoformat()
            })
    except Exception as e:
        print(f"Search error: {e}", file=sys.stderr)

    return results


def _truncate(inverted_index: dict, max_chars: int = 500) -> str:
    """Reconstruct abstract from OpenAlex inverted index."""
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    text = " ".join(w for _, w in word_positions)
    return text[:max_chars] + ("..." if len(text) > max_chars else "")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--help", "-h"):
        print(__doc__)
        print("\nOptions:")
        print("  --limit N          Max results (default: 20)")
        print("  --year-from YYYY   Filter by publication year")
        print("  --quality MODE     normal | strict")
        print("                       normal = peer-reviewed journals + proceedings")
        print("                       strict = normal + cited_by > 0")
        print("  --skip-low-cited N Exclude papers with < N citations")
        print("  --output DIR       Output directory (default: knowledge/)")
        sys.exit(0)

    query = args[0]
    limit = 20
    year_from = None
    quality = "normal"
    skip_low_cited = 0
    output_dir = "knowledge"

    i = 1
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        elif args[i] == "--year-from" and i + 1 < len(args):
            year_from = int(args[i + 1])
            i += 2
        elif args[i] == "--quality" and i + 1 < len(args):
            quality = args[i + 1]
            i += 2
        elif args[i] == "--skip-low-cited" and i + 1 < len(args):
            skip_low_cited = int(args[i + 1])
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        else:
            i += 1

    desc = f"Searching OpenAlex: {query} (limit={limit}, quality={quality}"
    desc += f", year>={year_from}" if year_from else ""
    desc += f", min_cited={skip_low_cited}" if skip_low_cited else ""
    desc += ")"
    print(desc)
    results = search_academic(query, limit, year_from, quality, skip_low_cited)

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "search-results.json")
    output = {
        "query": query,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "academic",
        "quality": quality,
        "results": results,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} results to {out_path}")


if __name__ == "__main__":
    main()

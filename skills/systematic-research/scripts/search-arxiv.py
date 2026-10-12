#!/usr/bin/env python3
"""
arXiv Search — search arXiv API for preprints.

Uses the official arXiv API (http://export.arxiv.org/api/query).
Returns ATOM XML → parsed to structured JSON. No API key required.

NOTE: arXiv contains preprints, not necessarily peer-reviewed.
Use --published-only to filter to papers with DOI or journal reference.
Cross-check results against published versions.

Usage:
    python search-arxiv.py "<query>" --limit N --output <dir>
    python search-arxiv.py "<query>" --limit N --year-from YYYY --category cs.AI --output <dir>
    python search-arxiv.py "<query>" --published-only --output <dir>

Reference: https://info.arxiv.org/help/api/index.html

Rate limit: polite delays; avoid bursts. Max results per call: depends on query.
"""

import sys
import json
import time
import shlex
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from search_support import read_url, SearchError, search_failed, search_succeeded

ARXIV_API = "https://export.arxiv.org/api/query"

# Common arXiv CS categories
ARXIV_CATEGORIES = {
    "cs.AI": "Artificial Intelligence",
    "cs.CL": "Computation and Language",
    "cs.CV": "Computer Vision",
    "cs.LG": "Machine Learning",
    "cs.NE": "Neural and Evolutionary Computing",
    "cs.IR": "Information Retrieval",
    "cs.SE": "Software Engineering",
    "cs.DB": "Databases",
    "cs.DC": "Distributed/Parallel/Cluster Computing",
    "cs.OS": "Operating Systems",
    "cs.NI": "Networking and Internet Architecture",
    "cs.AR": "Architecture",
    "cs.CR": "Cryptography and Security",
    "cs.PL": "Programming Languages",
    "cs.SY": "Systems and Control",
    "stat.ML": "Machine Learning (Statistics)",
}

# arXiv namespace in ATOM XML
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def build_query(search_terms: str, category: str = None) -> str:
    """Build arXiv API search query string."""
    # urlencode is the only encoding step. Retain explicit arXiv field syntax.
    if re.search(r'\b(?:all|ti|au|abs|cat|id|submittedDate|lastUpdatedDate):', search_terms):
        terms = search_terms
    else:
        tokens = shlex.split(search_terms)
        terms = ' AND '.join('all:' + (f'"{term}"' if ' ' in term else term) for term in tokens)
    if category:
        return f"cat:{category} AND ({terms})"
    return terms


def search_arxiv(
    query: str,
    limit: int = 20,
    year_from: int = None,
    category: str = None,
    published_only: bool = False,
) -> list[dict]:
    """Search arXiv API and return structured results."""
    search_query = build_query(query, category)

    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": min(limit, 100),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "systematic-research-skill/1.0"},
        )
        xml_data = read_url(req).decode("utf-8")
    except Exception as e:
        raise SearchError(f"arXiv API error: {e}") from e

    # Parse ATOM XML
    root = ET.fromstring(xml_data)
    if root.tag != '{http://www.w3.org/2005/Atom}feed':
        raise SearchError('arXiv returned a non-Atom response')
    results = []

    for entry in root.findall("atom:entry", NS):
        if 'api/errors' in entry.findtext('atom:id', default='', namespaces=NS):
            raise SearchError(entry.findtext('atom:summary', default='arXiv query error', namespaces=NS))
        title_el = entry.find("atom:title", NS)
        title = title_el.text.strip().replace("\n", " ") if title_el is not None else ""

        summary_el = entry.find("atom:summary", NS)
        summary = summary_el.text.strip().replace("\n", " ") if summary_el is not None else ""

        # Authors
        authors = []
        for author in entry.findall("atom:author", NS):
            name_el = author.find("atom:name", NS)
            if name_el is not None:
                authors.append(name_el.text.strip())

        # arXiv ID — extract from the <id> tag
        id_el = entry.find("atom:id", NS)
        arxiv_id = ""
        arxiv_url = ""
        if id_el is not None:
            raw_id = id_el.text.strip()
            # Format: http://arxiv.org/abs/2106.12345v1
            arxiv_id = raw_id.split("/abs/")[-1]
            arxiv_url = raw_id

        # PDF URL
        pdf_url = ""
        for link in entry.findall("atom:link", NS):
            if link.get("title") == "pdf":
                pdf_url = link.get("href", "")
                break

        # Published date
        published_el = entry.find("atom:published", NS)
        year = None
        if published_el is not None:
            published = published_el.text.strip()
            year = int(published[:4]) if len(published) >= 4 else None

        # Categories
        categories = []
        for cat in entry.findall("atom:category", NS):
            term = cat.get("term", "")
            if term:
                categories.append(term)

        # DOI
        doi = ""
        for doi_el in entry.findall("arxiv:doi", NS):
            doi = doi_el.text.strip()

        # Journal reference
        journal_ref = ""
        for jr in entry.findall("arxiv:journal_ref", NS):
            journal_ref = jr.text.strip()

        # Year filter
        if year_from and year and year < year_from:
            continue

        # Skip if published-only mode and paper lacks DOI/journal_ref
        if published_only and not doi and not journal_ref:
            continue

        results.append({
            "title": title,
            "authors": authors,
            "summary": summary[:500],
            "arxiv_id": arxiv_id,
            "url": arxiv_url,
            "pdf_url": pdf_url,
            "year": year,
            "published": published_el.text.strip() if published_el is not None else "",
            "categories": categories,
            "doi": doi,
            "journal_ref": journal_ref,
            "is_published": bool(doi or journal_ref),
            "retrieved": datetime.now(timezone.utc).isoformat(),
        })

        if len(results) >= limit:
            break

    return results


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        print("\nOptions:")
        print("  --limit N         Max results (default: 20)")
        print("  --year-from YYYY  Filter by publication year")
        print("  --category CAT    arXiv category (e.g., cs.AI, cs.LG)")
        print("  --published-only  Only papers with DOI or journal reference")
        print("  --output DIR      Output directory")
        print("\nCategories:")
        for k, v in ARXIV_CATEGORIES.items():
            print(f"  {k:12s} {v}")
        sys.exit(0)

    query = sys.argv[1]
    limit = 20
    year_from = None
    category = None
    published_only = False
    output_dir = "knowledge"

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--year-from" and i + 1 < len(sys.argv):
            year_from = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--category" and i + 1 < len(sys.argv):
            category = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--published-only":
            published_only = True
            i += 1
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    print(f"Searching arXiv for: {query}")
    try:
        if limit < 1:
            raise ValueError('--limit must be positive')
        results = search_arxiv(query, limit=limit, year_from=year_from, category=category,
                               published_only=published_only)
    except Exception as error:
        search_failed(output_dir, 'arxiv', query, error)
        print(f'Search failed: {error}', file=sys.stderr)
        sys.exit(1)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    output = {
        "query": query,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "arxiv",
        "category": category,
        "count": len(results),
        "results": results,
    }

    result_file = output_path / "results.json"
    search_succeeded(output_dir, 'results.json', output)
    print(f"Done: {len(results)} papers → {result_file}")


if __name__ == "__main__":
    main()

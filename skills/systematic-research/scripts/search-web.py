#!/usr/bin/env python3
"""
Web Search — search the web via DuckDuckGo and save structured results.

Usage:
    python search-web.py "<query>" [--limit N] [--output <dir>]

Output: JSON results file in <output>/search-results.json
"""

import sys
import os
import json
from datetime import datetime, timezone
from pathlib import Path
from search_support import SearchError, search_failed, search_succeeded


def search_web(query: str, limit: int = 10) -> list[dict]:
    """Search DuckDuckGo and return structured results."""
    results = []
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            try:
                from duckduckgo_search import DDGS
            except ImportError as error:
                raise SearchError('Install optional engines with: python -m pip install -r ' +
                                  str(Path(__file__).resolve().parents[1] / 'requirements.txt')) from error
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=limit):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "retrieved": datetime.now(timezone.utc).isoformat()
                })
    except Exception as e:
        raise SearchError(f'Web search failed: {e}') from e
    return results


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--help", "-h"):
        print(__doc__)
        print("\nOptions:")
        print("  --limit N     Max results (default: 10)")
        print("  --output DIR  Output directory (default: knowledge/)")
        sys.exit(0)

    query = args[0]
    limit = 10
    output_dir = "knowledge"

    i = 1
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        else:
            i += 1

    print(f"Searching: {query} (limit={limit})")
    try:
        if limit < 1:
            raise ValueError('--limit must be positive')
        results = search_web(query, limit)
    except Exception as error:
        search_failed(output_dir, 'web', query, error)
        print(f'Search failed: {error}', file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "search-results.json")
    output = {
        "query": query,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "web",
        "results": results
    }

    search_succeeded(output_dir, 'search-results.json', output)

    print(f"Saved {len(results)} results to {out_path}")
    for i, r in enumerate(results, 1):
        print(f"  [{i}] {r['title']}")
        print(f"      {r['url']}")


if __name__ == "__main__":
    main()

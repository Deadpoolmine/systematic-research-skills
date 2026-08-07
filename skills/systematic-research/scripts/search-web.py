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

try:
    from duckduckgo_search import DDGS
except ImportError:
    print("Error: duckduckgo-search not installed. Run: pip install duckduckgo-search")
    sys.exit(1)


def search_web(query: str, limit: int = 10) -> list[dict]:
    """Search DuckDuckGo and return structured results."""
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=limit):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "retrieved": datetime.now(timezone.utc).isoformat()
                })
    except Exception as e:
        print(f"Search error: {e}", file=sys.stderr)
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
    results = search_web(query, limit)

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "search-results.json")
    output = {
        "query": query,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "web",
        "results": results
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} results to {out_path}")
    for i, r in enumerate(results, 1):
        print(f"  [{i}] {r['title']}")
        print(f"      {r['url']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
USENIX Proceedings Scraper — extract paper listings from USENIX conference proceedings.

Fetches paper titles, authors, and URLs from USENIX technical-sessions pages.
Supports OSDI, ATC, NSDI, FAST, and other USENIX conferences.

Usage:
    python search-usenix.py osdi --year 2026 --output <dir>
    python search-usenix.py osdi --year 2026,2025,2024 --output <dir>
    python search-usenix.py atc --year 2025 --limit 50 --output <dir>
    python search-usenix.py fast --year 2025 --query snapshot --output <dir>

Dependencies: beautifulsoup4 (see skill requirements.txt)
"""

import sys
import json
import re
import time
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request

SKILL_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SKILL_ROOT / 'scripts'))
from search_support import read_url, SearchError, search_failed, search_succeeded

# Supported USENIX conferences and their URL prefixes
USENIX_CONFERENCES = {
    "osdi": "OSDI",
    "atc": "ATC",
    "nsdi": "NSDI",
    "fast": "FAST",
    "eurosys": "EuroSys",
    "sosp": "SOSP",
    "hotos": "HotOS",
    "hotdep": "HotDep",
    "hotcloud": "HotCloud",
    "hotstorage": "HotStorage",
    "vee": "VEE",
    "icac": "ICAC",
    "taas": "Taas",
    "soups": "SOUPS",
    "security": "USENIX Security",
}

BASE_URL = "https://www.usenix.org"
USER_AGENT = "USENIX-Research-Crawler/1.0 (academic research)"


def build_url(conf: str, year: int | str) -> str:
    """Build USENIX conference technical-sessions URL."""
    year_short = str(year)[-2:] if len(str(year)) == 4 else str(year)
    return f"{BASE_URL}/conference/{conf}{year_short}/technical-sessions"


def fetch_page(url: str, max_retries: int = 3) -> str | None:
    """Fetch page content with retry logic."""
    headers = {"User-Agent": USER_AGENT}
    return read_url(Request(url, headers=headers), attempts=max_retries).decode('utf-8')


def parse_papers(html: str, conf: str, year: str) -> list[dict]:
    """Parse paper listings from USENIX technical-sessions HTML."""
    try:
        from bs4 import BeautifulSoup
    except ImportError as error:
        raise SearchError('Install optional engines with: python -m pip install -r ' +
                          str(SKILL_ROOT / 'requirements.txt')) from error
    soup = BeautifulSoup(html, "html.parser")
    papers = []
    seen = set()

    # Find all paper presentation links
    # USENIX uses links like /conference/osdi26/presentation/<slug>
    pattern = re.compile(rf"/conference/{conf}\d{{2}}/presentation/([^/\"]+)")

    # Strategy 1: Find all links matching the presentation pattern
    for link in soup.find_all("a", href=True):
        href = link["href"]
        m = pattern.search(href)
        if not m:
            continue

        slug = m.group(1)
        if slug in seen or slug in ("keynote",):
            continue
        seen.add(slug)

        title = link.get_text(strip=True)
        if not title or len(title) < 10:
            continue

        # Try to find authors in nearby text
        authors = []
        parent = link.parent
        # Authors are usually in a sibling or the next paragraph
        for _ in range(5):
            if parent is None:
                break
            text = parent.get_text(strip=True)
            # The link text is the title, the rest of text in this block contains authors
            if text and text != title:
                # Remove the title portion, what remains is likely authors
                author_text = text.replace(title, "").strip()
                # Clean up common markers
                author_text = re.sub(
                    r"AVAILABLE MEDIA.*|Operational Systems Paper|Awarded Best Paper!|Distinguished Artifact Award Winner|Show details|Hide details",
                    "", author_text, flags=re.DOTALL
                ).strip()
                if author_text and len(author_text) > 10:
                    authors = [a.strip() for a in author_text.split(",") if a.strip()]
                    break
            parent = parent.parent

        papers.append({
            "title": title,
            "url": f"{BASE_URL}{href}",
            "authors": authors,
            "conference": USENIX_CONFERENCES.get(conf, conf.upper()),
            "year": year,
            "slug": slug,
        })

    return papers


def main():
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        return
    if len(sys.argv) < 2:
        print("Usage: python search-usenix.py <conference> --year <years> [--output <dir>] [--limit N]")
        print(f"  Conferences: {', '.join(USENIX_CONFERENCES.keys())}")
        sys.exit(1)

    conf = sys.argv[1].lower()
    if conf not in USENIX_CONFERENCES:
        print(f"Unknown conference '{conf}'. Supported: {', '.join(USENIX_CONFERENCES.keys())}")
        sys.exit(1)

    years = []
    if "--year" in sys.argv:
        idx = sys.argv.index("--year")
        years_str = sys.argv[idx + 1]
        years = [y.strip() for y in years_str.split(",")]

    output_dir = Path(".")
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        output_dir = Path(sys.argv[idx + 1])

    limit = None
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        limit = int(sys.argv[idx + 1])
    if not years or any(not re.fullmatch(r'\d{4}', year) for year in years):
        print('Supply --year with four-digit years, e.g. --year 2026,2025', file=sys.stderr)
        sys.exit(2)
    if limit is not None and limit < 1:
        print('--limit must be positive', file=sys.stderr)
        sys.exit(2)
    query = ''
    if '--query' in sys.argv:
        query = sys.argv[sys.argv.index('--query') + 1]

    all_papers = []
    for year in years:
        url = build_url(conf, year)
        print(f"Fetching {USENIX_CONFERENCES[conf]} '{year}: {url}")
        try:
            html = fetch_page(url)
            papers = parse_papers(html, conf, year)
            if not papers:
                raise SearchError('No presentation links parsed; check conference/year or page format')
        except Exception as error:
            search_failed(output_dir, 'usenix', f'{conf}:{",".join(years)} {query}', error)
            print(f'Search failed: {error}', file=sys.stderr)
            sys.exit(1)
        print(f"  Found {len(papers)} papers")
        all_papers.extend(papers)

        # Be polite — rate limit
        if len(years) > 1:
            time.sleep(1)

    if query:
        terms = query.lower().split()
        all_papers = [paper for paper in all_papers
                      if all(term in paper['title'].lower() for term in terms)]
    if limit:
        all_papers = all_papers[:limit]

    # Output
    output_dir.mkdir(parents=True, exist_ok=True)

    output = {
        "query": f"conference:{USENIX_CONFERENCES[conf]} years:{','.join(years)}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "usenix",
        "conference": USENIX_CONFERENCES[conf],
        "years": years,
        "count": len(all_papers),
        "results": all_papers,
    }

    output_path = output_dir / "results.json"
    search_succeeded(output_dir, 'results.json', output)
    print(f"\nDone: {len(all_papers)} papers → {output_path}")


if __name__ == "__main__":
    main()

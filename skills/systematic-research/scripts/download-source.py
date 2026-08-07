#!/usr/bin/env python3
"""
Source Downloader — download search result materials to local storage.

Downloads PDF/HTML from URLs and saves to the item folder.
Supports arXiv, USENIX, OpenAlex, and general web URLs.

Usage:
    python download-source.py "<url>" --output knowledge/<category>/<subcategory>/<item>/
    python download-source.py "<url>" --output <dir> --name source.pdf

Output: source.pdf (or source.html for web pages) in the output directory.
"""

import sys
import os
import time
import urllib.request
import urllib.parse
from pathlib import Path
from urllib.parse import urlparse

USER_AGENT = "systematic-research-skill/1.0 (research crawler)"


def _is_arxiv(url: str) -> bool:
    return "arxiv.org" in url


def _is_usenix(url: str) -> bool:
    return "usenix.org" in url


def _resolve_arxiv_pdf(url: str) -> str:
    """Convert arxiv.org/abs/ID to arxiv.org/pdf/ID.pdf."""
    # https://arxiv.org/abs/2407.04363 → https://arxiv.org/pdf/2407.04363.pdf
    parsed = urlparse(url)
    path = parsed.path.replace("/abs/", "/pdf/")
    if not path.endswith(".pdf"):
        # Strip version suffix: 2407.04363v3 → 2407.04363
        parts = path.rsplit(".", 1)
        if len(parts) == 2 and parts[1].startswith("v") and parts[1][1:].isdigit():
            path = parts[0]
        path += ".pdf"
    return f"https://arxiv.org{path}"


def download(url: str, output_dir: Path, filename: str = None) -> Path | None:
    """Download content from URL to output_dir. Returns path or None."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Resolve arXiv to PDF
    if _is_arxiv(url):
        url = _resolve_arxiv_pdf(url)

    # Determine filename
    if filename:
        out_path = output_dir / filename
    else:
        suffix = ".pdf" if url.endswith(".pdf") else ".html"
        out_path = output_dir / f"source{suffix}"

    # Skip if already downloaded and non-empty
    if out_path.exists() and out_path.stat().st_size > 0:
        print(f"  [SKIP] Already downloaded: {out_path}")
        return out_path

    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as resp:
            content = resp.read()
            out_path.write_bytes(content)
            size_kb = len(content) / 1024
            print(f"  [OK] Downloaded {size_kb:.0f} KB → {out_path}")
            return out_path
    except Exception as e:
        print(f"  [FAIL] Download error: {e}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)

    url = sys.argv[1]
    output_dir = Path(".")
    filename = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_dir = Path(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--name" and i + 1 < len(sys.argv):
            filename = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    result = download(url, output_dir, filename)
    if result:
        print(f"Saved to: {result}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

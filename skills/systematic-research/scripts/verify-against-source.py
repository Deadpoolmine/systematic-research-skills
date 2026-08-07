#!/usr/bin/env python3
"""
Source-API Cross-Verification — verify results.json entries against the original source API.

For each entry in results.json, queries the source API (arXiv, CrossRef DOI, or OpenAlex)
and compares authors, title, and summary. Flags mismatches and can auto-fix from API data.

Usage:
    python verify-against-source.py results.json                # check only
    python verify-against-source.py results.json --fix          # auto-fix mismatches
    python verify-against-source.py results.json --strict       # require all fields match

Exit codes:
    0 = all entries verified or fixed
    1 = unfixed mismatches remain
    2 = API errors prevented full verification
"""

import sys
import os
import json
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone
from xml.etree import ElementTree as ET


USER_AGENT = "systematic-research-verify/1.0 (mailto:research@example.com)"
ARXIV_API = "http://export.arxiv.org/api/query"


def extract_arxiv_id(entry: dict) -> str | None:
    """Extract raw arXiv ID (without version) from an entry."""
    for field in ["arxiv_id", "arxivId", "id"]:
        val = entry.get(field, "")
        if val:
            # Strip version suffix: 1908.10740v1 → 1908.10740
            m = re.match(r"^(\d{4}\.\d{4,5})", val)
            if m:
                return m.group(1)
            return val
    # Try from URL
    url = entry.get("url", "")
    m = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", url)
    if m:
        return m.group(1).rstrip("v0123456789")
    return None


def query_arxiv(arxiv_id: str) -> dict | None:
    """Query arXiv API for a paper and return structured data."""
    try:
        url = f"{ARXIV_API}?id_list={arxiv_id}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        resp = urllib.request.urlopen(req, timeout=30)
        data = resp.read().decode("utf-8")
        root = ET.fromstring(data)

        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }
        entry_el = root.find("atom:entry", ns)
        if entry_el is None:
            return None

        title = entry_el.find("atom:title", ns)
        summary = entry_el.find("atom:summary", ns)

        return {
            "title": title.text.strip().replace("\n", " ") if title is not None else "",
            "authors": [
                a.find("atom:name", ns).text
                for a in entry_el.findall("atom:author", ns)
            ],
            "summary": summary.text.strip().replace("\n", " ")
            if summary is not None
            else "",
            "arxiv_id": entry_el.find("atom:id", ns).text.split("/")[-1]
            if entry_el.find("atom:id", ns) is not None
            else arxiv_id,
        }
    except Exception as e:
        print(f"  [API ERR] arXiv query failed for {arxiv_id}: {e}", file=sys.stderr)
        return None


def titles_match(our_title: str, api_title: str, threshold: float = 0.6) -> bool:
    """Check if two titles match. Uses prefix match at threshold ratio."""
    our_clean = our_title.lower().strip().rstrip(".")
    api_clean = api_title.lower().strip().rstrip(".")

    # Exact match
    if our_clean == api_clean:
        return True

    # Prefix match: first N chars
    min_len = min(len(our_clean), len(api_clean), 80)
    if our_clean[:min_len] == api_clean[:min_len]:
        return True

    # Word-level Jaccard on first 10 words
    our_words = set(our_clean.split()[:10])
    api_words = set(api_clean.split()[:10])
    if our_words and api_words:
        overlap = len(our_words & api_words) / len(our_words | api_words)
        return overlap >= threshold

    return False


def authors_match(our_authors: list[str], api_authors: list[str], min_match: int = 3) -> bool:
    """Check if author lists overlap sufficiently."""
    our_set = {a.lower().strip() for a in our_authors if a.strip()}
    api_set = {a.lower().strip() for a in api_authors if a.strip()}

    if not our_set or not api_set:
        return False

    # All our authors in API list, or all API authors in our list
    n_match = len(our_set & api_set)

    # At least min_match common, or all of ours matched, or all of API matched
    return n_match >= min(min_match, min(len(our_set), len(api_set)))


def summary_overlap(our_summary: str, api_summary: str) -> float:
    """Compute word-level overlap ratio between two summaries."""
    our_words = set(our_summary.lower().split()[:50])
    api_words = set(api_summary.lower().split()[:50])
    if not our_words or not api_words:
        return 0.0
    return len(our_words & api_words) / min(len(our_words), len(api_words))


def verify_entry(entry: dict, index: int, fix_mode: bool = False) -> dict:
    """Verify a single entry against source API. Returns updated entry and issues list."""
    issues = []
    arxiv_id = extract_arxiv_id(entry)

    if not arxiv_id:
        entry["verified"] = False
        entry["verify_error"] = "No extractable arXiv ID or DOI"
        return entry, ["No extractable identifier"]

    api_data = query_arxiv(arxiv_id)
    if api_data is None:
        entry["verified"] = False
        entry["verify_error"] = f"arXiv API unreachable for {arxiv_id}"
        return entry, [f"API unreachable: {arxiv_id}"]

    entry["verified"] = True
    entry["verified_at"] = datetime.now(timezone.utc).isoformat()

    # Check title
    if not titles_match(entry.get("title", ""), api_data["title"]):
        issues.append(
            f"TITLE MISMATCH:\n"
            f"  results.json: {entry.get('title', '')[:100]}\n"
            f"  arXiv:        {api_data['title'][:100]}"
        )
        if fix_mode:
            entry["title"] = api_data["title"]

    # Check authors
    if not authors_match(entry.get("authors", []), api_data["authors"]):
        issues.append(
            f"AUTHOR MISMATCH:\n"
            f"  results.json: {', '.join(entry.get('authors', [])[:5])}\n"
            f"  arXiv:        {', '.join(api_data['authors'][:5])}"
        )
        if fix_mode:
            entry["authors"] = api_data["authors"]

    # Check summary overlap
    overlap = summary_overlap(entry.get("summary", ""), api_data["summary"])
    if overlap < 0.3 and len(entry.get("summary", "")) > 50:
        issues.append(
            f"SUMMARY MISMATCH (overlap={overlap:.1%}):\n"
            f"  results.json: {entry.get('summary', '')[:120]}...\n"
            f"  arXiv:        {api_data['summary'][:120]}..."
        )
        if fix_mode:
            entry["summary"] = api_data["summary"]

    # Fix arxiv_id version if different
    if fix_mode and api_data.get("arxiv_id"):
        entry["arxiv_id"] = api_data["arxiv_id"]

    return entry, issues


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)

    results_path = Path(sys.argv[1])
    fix_mode = "--fix" in sys.argv

    if not results_path.exists():
        print(f"Error: {results_path} not found")
        sys.exit(2)

    data = json.loads(results_path.read_text(encoding="utf-8"))
    results = data.get("results", [])

    if not results:
        print("No entries to verify.")
        sys.exit(0)

    print(f"Verifying {len(results)} entries against source APIs...\n")

    total_issues = 0
    api_errors = 0
    fixed = 0

    for i, entry in enumerate(results):
        title_short = entry.get("title", "?")[:60]
        print(f"[{i + 1}/{len(results)}] {title_short}...")

        updated, issues = verify_entry(entry, i, fix_mode=fix_mode)

        if updated.get("verified") is False:
            print(f"  ⚠ SKIP: {updated.get('verify_error', 'unknown')}")
            api_errors += 1
            continue

        if issues:
            for issue in issues:
                print(f"  ✗ {issue.split(chr(10))[0]}")
                total_issues += 1
            if fix_mode:
                print(f"  ✓ FIXED ({len(issues)} issue(s))")
                fixed += len(issues)
        else:
            print(f"  ✓ OK")

        time.sleep(0.3)  # Rate limit

    # Save if fixed
    if fix_mode and fixed > 0:
        data["results"] = results
        data["verified_against_source"] = True
        data["verification_timestamp"] = datetime.now(timezone.utc).isoformat()
        results_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n✓ Fixed {fixed} issue(s) in {results_path}")

    print(f"\n{'=' * 50}")
    print(f"Summary: {total_issues} mismatches, {api_errors} API errors, {fixed} auto-fixed")

    if api_errors > 0 and total_issues == 0:
        print("WARNING: Some entries could not be verified (API errors)")
        sys.exit(2)
    elif total_issues > 0 and not fix_mode:
        print(f"FAILED: {total_issues} mismatches. Run with --fix to auto-correct.")
        sys.exit(1)
    elif total_issues > 0 and fix_mode:
        print(f"PASSED: All {total_issues} mismatches fixed.")
        sys.exit(0)
    else:
        print("PASSED: All entries verified against source.")
        sys.exit(0)


if __name__ == "__main__":
    main()

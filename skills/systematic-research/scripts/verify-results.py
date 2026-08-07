#!/usr/bin/env python3
"""
Cross-Validation — verify consistency between results.json and output files.

Checks:
  1. results.json exists and has valid entries
  2. Every item folder has source.pdf (or source.html), tldr.md, l0.md, l1.md, bibentry.bib
  3. source.pdf exists and is non-empty
  4. bibentry.bib URL/DOI matches results.json entry
  5. bibentry.bib first author matches results.json first author
  6. results.json entries have verified=true (or user accepts risk)

Usage:
    python verify-results.py knowledge/<category>/<subcategory>/
    python verify-results.py knowledge/<category>/<subcategory>/ --check-urls
"""

import sys
import json
import re
import textwrap
from pathlib import Path


def load_results(results_path: Path) -> list[dict]:
    """Load and validate results.json."""
    if not results_path.exists():
        print(f"  [FAIL] results.json not found: {results_path}")
        return None

    try:
        data = json.loads(results_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  [FAIL] Invalid JSON: {e}")
        return None

    results = data.get("results", [])
    if not results:
        print(f"  [WARN] results.json is empty")
    return results


def find_item_folders(root: Path) -> list[Path]:
    """Find all item folders (containing tldr.md)."""
    return sorted([p.parent for p in root.rglob("tldr.md")])


def check_item_folder(folder: Path) -> list[str]:
    """Check that an item folder has all required files."""
    issues = []
    # Check source material exists (PDF or HTML)
    has_source = (folder / "source.pdf").exists() or (folder / "source.html").exists()
    if not has_source:
        issues.append("Missing source.pdf (or source.html)")
    # Check source is non-empty
    for src in ["source.pdf", "source.html"]:
        sp = folder / src
        if sp.exists() and sp.stat().st_size == 0:
            issues.append(f"Empty file: {src}")
    for fname in ["tldr.md", "l0.md", "l1.md", "bibentry.bib"]:
        if not (folder / fname).exists():
            issues.append(f"Missing {fname}")
    return issues


def extract_url_from_bib(bib_path: Path) -> str | None:
    """Extract URL field from bibentry.bib."""
    if not bib_path.exists():
        return None
    content = bib_path.read_text(encoding="utf-8")
    m = re.search(r'url\s*=\s*\{([^}]+)\}', content, re.IGNORECASE)
    return m.group(1).strip() if m else None


def extract_doi_from_bib(bib_path: Path) -> str | None:
    """Extract DOI field from bibentry.bib."""
    if not bib_path.exists():
        return None
    content = bib_path.read_text(encoding="utf-8")
    m = re.search(r'doi\s*=\s*\{([^}]+)\}', content, re.IGNORECASE)
    return m.group(1).strip() if m else None


def extract_first_author_from_bib(bib_path: Path) -> str | None:
    """Extract first author's last name from bibentry.bib."""
    if not bib_path.exists():
        return None
    content = bib_path.read_text(encoding="utf-8")
    # Match: author = {LastName, FirstName and ...}
    m = re.search(r'author\s*=\s*\{([^}]+)\}', content, re.IGNORECASE)
    if not m:
        return None
    authors_str = m.group(1)
    # Get first author: "LastName, FirstName" or "FirstName LastName"
    first_author = authors_str.split(" and ")[0].strip()
    # Normalize: extract last name (before comma, or last word)
    if "," in first_author:
        last_name = first_author.split(",")[0].strip()
    else:
        parts = first_author.split()
        last_name = parts[-1] if parts else first_author
    return last_name.lower()


def extract_first_author_last_name(full_name: str) -> list[str]:
    """Extract possible last names from a full author name string.
    Returns list of candidates: [last_word, last_two_words_lower] for names like 'van Breukelen'.
    """
    parts = full_name.strip().split()
    if not parts:
        return [full_name.lower()]
    candidates = [parts[-1].lower()]
    if len(parts) >= 2:
        candidates.append(" ".join(parts[-2:]).lower())
    return candidates


def authors_consistent(bib_path: Path, result_entry: dict) -> tuple[bool, str]:
    """Check if bibentry first author is consistent with results.json.
    Returns (is_consistent, detail_message).
    """
    bib_author = extract_first_author_from_bib(bib_path)
    result_authors = result_entry.get("authors", [])

    if not bib_author:
        return True, "(no author in bib)"
    if not result_authors:
        return True, "(no authors in results.json)"

    result_candidates = extract_first_author_last_name(result_authors[0])

    if bib_author in result_candidates:
        return True, f"✓ first author matches: {bib_author}"
    else:
        return False, f"bib={bib_author} vs results.json={result_candidates[0]}"


def match_result(results: list[dict], url: str) -> dict | None:
    """Find matching result entry by URL."""
    for r in results:
        if r.get("url", "").strip() == url:
            return r
    return None


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)

    root = Path(sys.argv[1])
    check_urls = "--check-urls" in sys.argv

    if not root.is_dir():
        print(f"Error: '{root}' is not a directory")
        sys.exit(1)

    results_path = root / "results.json"
    results = load_results(results_path)

    if results is None:
        sys.exit(1)

    if results is not None:
        print(f"✓ results.json: {len(results)} entries")

    item_folders = find_item_folders(root)
    print(f"  Found {len(item_folders)} item folder(s)")

    passes = 0
    warnings = 0
    failures = 0

    for folder in item_folders:
        rel = folder.relative_to(root)
        print(f"\n[{rel}]")

        # Check required files
        missing = check_item_folder(folder)
        if missing:
            for m in missing:
                print(f"  [FAIL] {m}")
                failures += 1
            continue

        # Check bibentry URL matches results.json
        bib_url = extract_url_from_bib(folder / "bibentry.bib")
        bib_doi = extract_doi_from_bib(folder / "bibentry.bib")

        if bib_url:
            matched = match_result(results, bib_url)
            if matched:
                print(f"  ✓ URL matches results.json → {matched.get('title', '?')[:60]}")
                passes += 1

                # NEW: Check author consistency between bibentry and results.json
                author_ok, author_msg = authors_consistent(folder / "bibentry.bib", matched)
                if author_ok:
                    print(f"  {author_msg}")
                else:
                    print(f"  [FAIL] Author mismatch: {author_msg}")
                    failures += 1

                # NEW: Check if results.json entry was source-verified
                if not matched.get("verified", True):
                    print(f"  [WARN] Entry not verified against source API (R0-d skipped)")
                    warnings += 1
            else:
                print(f"  [FAIL] URL not found in results.json: {bib_url}")
                failures += 1
        else:
            print(f"  [WARN] No URL in bibentry.bib")
            warnings += 1

        # Check DOI consistency (if both have DOI)
        if bib_doi and results:
            for r in results:
                r_doi = r.get("doi", "")
                if r_doi and bib_doi.lower() == r_doi.lower():
                    print(f"  ✓ DOI matches results.json")
                    break
            else:
                print(f"  [WARN] DOI '{bib_doi}' not matched in results.json")
                warnings += 1

    print(f"\n{'='*50}")
    print(f"Results: {passes} passed, {warnings} warnings, {failures} failures")

    if failures > 0:
        print("CROSS-VALIDATION FAILED")
        sys.exit(1)
    elif warnings > 0:
        print("CROSS-VALIDATION PASSED (with warnings)")
    else:
        print("CROSS-VALIDATION PASSED")


if __name__ == "__main__":
    main()

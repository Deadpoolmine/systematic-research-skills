# CS / Systems — Search Engines

Domain-specific search engines for computer systems research.

## Available Engines

| Engine | Script | Source |
|--------|--------|--------|
| **USENIX** | [search-usenix.py](search-usenix.py) | USENIX conference proceedings (OSDI, ATC, NSDI, FAST, EuroSys, etc.) |

## USENIX Engine

Scrapes paper listings from USENIX technical-sessions pages.

### Usage

```bash
# Search OSDI 2026 papers
python search-usenix.py osdi --year 2026 --output <dir>

# Search multiple years
python search-usenix.py osdi --year 2026,2025,2024 --output <dir>

# Search multiple conferences
python search-usenix.py atc --year 2025,2024 --limit 100 --output <dir>
```

### Supported Conferences

| Key | Full Name | URL Pattern |
|-----|-----------|-------------|
| `osdi` | OSDI | `/conference/osdiYY/technical-sessions` |
| `atc` | USENIX ATC | `/conference/atcYY/technical-sessions` |
| `nsdi` | NSDI | `/conference/nsdiYY/technical-sessions` |
| `fast` | FAST | `/conference/fastYY/technical-sessions` |
| `eurosys` | EuroSys | `/conference/eurosysYY/technical-sessions` |

### Output

Each result includes: `title`, `url`, `authors`, `conference`, `year`, `slug`.

Results saved as `results.json` in the output directory.

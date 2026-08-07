# Search Engines

Domain-specific search engine registry. Each engine scrapes/APIs a specific venue and outputs `results.json` for the systematic-research pipeline.

## Directory Structure

```
search-engines/
  <domain>/
    <subdomain>/
      README.md            # Engine documentation
      search-<venue>.py    # Python search script
      search-<venue>.cmd   # Windows wrapper
      search-<venue>.sh    # Linux/macOS wrapper
```

## Available Engines

| Domain | Subdomain | Engine | Venue |
|--------|-----------|--------|-------|
| **CS** | [system/](cs/system/) | `search-usenix.py` | USENIX (OSDI, ATC, NSDI, FAST, EuroSys) |
| **CS** | [ai/](cs/ai/) | `search-arxiv.py` | arXiv (cs.AI, cs.LG, cs.CL, cs.CV) |

## Adding a New Engine

1. Create `search-engines/<domain>/<subdomain>/search-<venue>.py`
2. Must output `results.json` with: `query`, `timestamp`, `source`, `results[]`
3. Each result: `title`, `url`, `authors`, `year`
4. Add `.cmd` and `.sh` wrappers
5. Update `README.md` with usage docs

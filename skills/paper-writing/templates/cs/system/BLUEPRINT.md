# System Paper Blueprints — Index

**Load this reference when:** L1 needs page-budget and structural guidance. Each blueprint provides page allocation, per-section paragraph plans, and venue conventions.

## Venue → Blueprint Mapping

The skill auto-identifies the blueprint from the target venue's page limit:

| Target Venue | Pages | Blueprint | Skeleton |
|-------------|-------|-----------|----------|
| OSDI, SOSP, FAST, NSDI, ATC, EuroSys, ASPLOS | 12 | [12pages](blueprints/12pages.md) | `templates/cs/system/usenix/` or `acm/` |
| HotStorage, HotOS, short papers | 8 | [8pages](blueprints/8pages.md) | `templates/cs/system/usenix/` |
| *(generic — venue not yet listed)* | *ask user* | — | `templates/cs/system/ieee/` |

**Rule:** The page count determines the blueprint. The venue determines the skeleton (USENIX vs ACM vs IEEE format).

## Available Blueprints

| Blueprint | Page Budget | Typical Venues |
|-----------|------------|----------------|
| [12pages](blueprints/12pages.md) | 12 pages | OSDI, SOSP, FAST, NSDI, ATC, EuroSys, ASPLOS |
| [8pages](blueprints/8pages.md) | 8 pages | HotStorage, HotOS, short/position papers |

## How to Use

During L1, after the user states the target venue:
1. Identify the page count from the venue → load the matching blueprint
2. Use the page budget as a constraint when proposing section structures
3. Reference per-section paragraph plans when defining A→B→C flow chains
4. The blueprint is **advisory** — the actual structure is determined through discussion

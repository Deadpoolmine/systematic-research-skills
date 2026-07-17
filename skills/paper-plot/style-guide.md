# Style Guide — Visual Conventions

Default visual conventions for paper-plot figures. Override per paper or venue requirements.

## Color Palette

**Default (Blue theme):**

| Role | Hex | Preview |
|------|-----|---------|
| Primary | `#1565C0` | Main system modules, core components |
| Secondary | `#42A5F5` | Sub-modules, helpers, caches |
| Tertiary | `#90CAF9` | Background layers, optional components |
| External | `#78909C` | Users, third-party systems, environment |
| Highlight | `#FF7043` | Critical path, bottleneck, key insight |
| Success | `#66BB6A` | Optimizations, improvements |
| Border | `#455A64` | All shape outlines (1pt) |
| Text | `#212121` | All text (dark, high contrast) |

**Alternate palettes:**
- Green theme: Primary `#2E7D32`, Secondary `#66BB6A`, Tertiary `#A5D6A7`
- Purple theme: Primary `#6A1B9A`, Secondary `#AB47BC`, Tertiary `#CE93D8`

Select palette at P0. Do NOT change mid-figure.

## Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Figure title | Arial | 12pt | Bold | `#212121` |
| Component name | Arial | 10pt | Regular | `#212121` |
| Component sub-label | Arial | 8pt | Regular | `#616161` |
| Connector label | Arial | 8pt | Regular | `#616161` |
| Annotation / note | Arial | 7pt | Italic | `#9E9E9E` |
| Table header | Arial | 9pt | Bold | `#FFFFFF` (on dark bg) |
| Table cell | Arial | 9pt | Regular | `#212121` |

## Shapes

| Semantic | PPT Shape | Corner | Border |
|----------|-----------|--------|--------|
| System module | `ROUNDED_RECTANGLE` | 0.15cm radius | 1pt solid |
| Sub-component | `RECTANGLE` | square | 1pt solid |
| Decision / branch | `DIAMOND` | — | 1pt solid |
| External entity | `ROUNDED_RECTANGLE` | 0.15cm radius | 1pt dashed |
| Group / layer box | `RECTANGLE` | square | 0.5pt dashed |
| Data store (DB) | `CYLINDER` | — | 1pt solid |
| Document / file | `FOLDER` or `RECTANGLE` | waved bottom | 1pt solid |

## Connectors

| Relationship | Style | Weight | Arrow |
|-------------|-------|--------|-------|
| Data flow | Solid | 1pt | Open triangle end |
| Control flow | Solid | 1pt | Open triangle end |
| Optional / async | Dashed | 0.75pt | Open triangle end |
| Bidirectional | Solid | 1pt | Open triangle both ends |
| Annotation pointer | Dotted | 0.5pt | None |

## Layout

- Grid: 0.25cm
- Minimum component size: 1.5cm × 1.0cm
- Horizontal gap: 0.3cm (same layer), 0.5cm (different groups)
- Vertical gap: 0.4cm (same layer), 0.6cm (different groups)
- Layer padding: 0.3cm inside group boundary
- Page margin: 0.3cm from slide edge

## Export

- Format: PNG
- Resolution: 300 dpi
- Single column: 8.9cm → 1051px wide
- Double column: 17.8cm → 2102px wide
- Background: white (not transparent)

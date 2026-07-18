# Paper Style Lock

> Paper-wide visual contract. All figures in this paper share these values.
> P1 MUST read this before writing per-figure `figure-spec-lock.md` files.
> P3 MUST verify each figure against this lock (Cross-Figure Consistency check).
> Per-figure overrides must be explicitly declared in the figure's spec-lock.

---

## typography

```
- font_family: "Times New Roman"       # MANDATORY — never Arial, never Calibri
- figure_title: 10pt bold
- section_title: 9pt bold
- body_label: 7pt
- sub_label: 6.5pt
- annotation: 6pt
- detail: 5.5pt
```

**Single-column figures (w=8.9cm)**: scale all sizes down by 1pt (e.g., figure_title → 9pt, body_label → 6pt).

## color_palette

> **Nature Blue** — recommended for AAAI / academic submissions.
> 90/10 Rule: ONLY ONE element per figure uses `primary_dark`. All others use neutral or lighter tones.

### Signal family
```
- primary_dark: "#0F4D92"        # Hero fill — EXACTLY ONE element per figure
- primary_mid: "#2C6FB7"         # Secondary module fills
- primary_light: "#7BABDB"       # Light borders / decorative accents
- primary_bg: "#E8F0F9"          # Container background tints
```

### Neutral family
```
- neutral_dark: "#272727"         # Primary text on light backgrounds
- neutral_mid: "#767676"          # Secondary text / region labels
- neutral_light: "#CFCECE"        # Borders / subtle dividers
- white: "#FFFFFF"                # White fill
- sub_fill: "#F8F9FC"             # Near-white background for edge regions
```

### Text on colored backgrounds
```
- text_white: "#FFFFFF"           # Text on dark fills
- text_dim: "#BBD4F0"             # Dimmed text on primary_dark
- text_gray: "#616161"            # Description text on white cards
```

### Connector colors
```
- connector_primary: "#4D6A7A"   # Main flow arrows / data flow
- connector_secondary: "#8A9BA8" # Control flow / feedback / cycle arrows
```

### Accent (≤2 uses per figure)
```
- accent_gold: "#E8A817"          # Stars / emphasis markers
- accent_teal: "#42949E"          # Alternative positive indicator
- accent_red: "#B64342"           # Warning / negative indicator
```

### Luminance-aware text rule

Every filled shape MUST use `is_dark(fill_color)` to select text color:
- Dark fill (luminance < 128) → `text_white`
- Light fill (luminance ≥ 128) → `neutral_dark`

```python
def is_dark(hex_color):
    """RGBColor → True if luminance < 128."""
    h = str(hex_color)  # RGBColor → hex string
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) < 128
```

## shape_vocabulary

> Pick ≥3 distinct MSO_SHAPE types per figure from this vocabulary.

| Shape | Semantic | When to Use |
|-------|----------|-------------|
| `ROUNDED_RECTANGLE` | Module / container / card | Default for most containers |
| `OVAL` | State node / lifecycle stage | Tree roots, state machines |
| `CHEVRON` | Pipeline step / process | Sequential flow stages |
| `CAN` | Data store / database | File cabinet, storage, pool |
| `STAR_5_POINT` | Highlight marker | Hero emphasis (≤2 per figure) |
| `RECTANGLE` | Dashed container | Grouping boundary (dashed only) |
| `DIAMOND` | Decision point | Branching logic |
| `CLOUD` | Remote service | External / internet entity |
| `HEXAGON` | Special concept | Distinct from standard modules |
| `FOLDED_CORNER` | Document / file | Configuration files, documents |

## spacing_defaults

```
- grid_snap: 0.25cm              # All coordinates snapped to this grid
- page_margin: 0.3cm             # Minimum distance from slide edges
- intra_group_gap: 0.15cm        # Gap between elements within same group
- inter_group_gap: 0.3cm         # Gap between adjacent groups
- region_gap: 0.4cm              # Gap between major regions
- container_padding: 0.2cm       # Internal padding inside containers
- text_margin: 1pt               # Margin inside text boxes
- connector_channel: 0.3cm       # Minimum clearance for connector paths
- min_shape_size: 0.4cm          # Smallest allowed shape dimension
```

## connector_defaults

```
- primary_flow: solid, 0.8pt, connector_primary     # Main data/control flow
- secondary_flow: solid, 0.6pt, connector_secondary  # Internal flow
- feedback: dashed, 0.6pt, connector_secondary       # Feedback / reverse flow
- annotation: dotted, 0.5pt, "#9E9E9E"               # Decorative / annotation
- arrow_head: triangle (tailEnd)                      # Standard for all arrows
- max_cross_module_arrows: 5                          # Per-figure arrow budget
```

## layer_stack

> All figures use the standard 5-layer stack. L1 drawn first (behind), L5 drawn last (on top).

```
L1: Connectors & Arrows    (drawn first → behind all shapes)
L2: Module Containers       (region backgrounds, panels)
L3: Sub-components & Nodes  (cards, pills, circles, icons)
L4: Highlights & Accents    (stars, markers ①②③)
L5: Text & Annotations      (drawn last → always on top)
```

**Hard rule**: Draw ALL of L1, then ALL of L2, then ALL of L3, etc. Never mix layers (e.g., L1 connector → L2 container → L1 connector → L3 shape).

## hard_gates

### 90/10 Color Rule
- 90% of elements use neutral/low-saturation colors
- 10% (hero) gets saturated signal color (`primary_dark`)
- ONLY ONE element per figure uses `primary_dark` fill
- Squint test: ONE dark block must pop out. 2+ blocks competing → FAIL.

### Fitts's Law for Visual Hierarchy
- Hero area ≥ 1.5× the area of any other individual module
- Measure and verify: `hero_area / max_other_area ≥ 1.5`

### Shape Variety
- ≥3 distinct MSO_SHAPE types per figure
- Each shape type must have a semantic reason for its choice

### Structural Integrity
- Every module's visual structure must match its semantic structure
- A "box containing 3 small boxes" is NOT a valid visual structure
- Each relationship must have an identified structure signature (tree/pipeline/cycle/etc.)

### Physical Associations
- ≥2 physical-world analogs per figure
- Each association must be visible and recognizable in the final figure

### Connector Discipline
- No chained straight segments (use single connectors)
- All connectors anchored to shape edges
- Labels near connector midpoint
- Bidirectional parallel pairs spaced 0.3-0.5cm apart
- All connectors in L1 (behind shapes)

### Typography Discipline
- Times New Roman for ALL text runs
- Luminance-aware text color on every filled shape
- Text box width ≥ longest word width
- Label-to-shape distance ≤ 50% of label-to-nearest-other-shape distance

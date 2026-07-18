# Figure Spec Lock Template

> Machine-readable execution contract for figure generation.
> P1 writes `figures/<name>/figure-spec-lock.md` alongside `figure-layout.md`.
> P2 MUST `read_file` this before placing a single shape.
> Values not listed here MUST NOT appear in the generated figure.
> P3 verifies the figure against this lock.
>
> **Source of truth hierarchy**: `paper-style-lock.md` (paper-wide) → `figure-spec-lock.md` (per-figure, can override where declared) → generated code (must match both).

---

## How to Use (for P1 — Architect)

After completing the layout plan in `figure-layout.md`, extract all numeric and semantic constants into this spec lock. Every value that P2 needs for code generation must be here — no value should be invented during P2.

The spec lock serves three purposes:
1. **Precision**: P2 generates from exact values, not from memory or guesswork
2. **Consistency**: All figures in a paper share the same typography, color, and spacing defaults via `paper-style-lock.md`
3. **Verifiability**: P3 can mechanically check that the generated figure matches this lock

## How to Use (for P2 — Builder)

```
Step A: Read this file and paper-style-lock.md BEFORE any shape code
Step B: Declare named constants from the values below (no inline literals)
Step C: Build text inventory with typography roles
Step D: Calculate text dimensions → derive container sizes
Step E: Place shapes layer-by-layer (L1→L5), group-by-group
Step F: Self-check each group after completion
Step G: Verify all text fits, no overlaps, no spec-lock violations
```

**Hard rule**: Container sizes are derived FROM text dimensions, not guessed. Never shrink text to fit a container — expand the container.

**Hard rule**: Every shape belongs to exactly one group. No orphan elements.

**Forbidden**: Inventing values not in this lock during P2. If a new value is genuinely needed, stop, update this lock, then continue.

---

## canvas

```
- width_cm: 17.8       # single-column = 8.9, double-column = 17.8
- height_cm: ~11.0     # flexible; P2 calculates actual height from content
- grid_snap_cm: 0.25   # all coordinates snapped to this grid
- orientation: left-right | top-bottom | center-out
- figure_type: architecture | flowchart | comparison | concept | data-plot
```

## typography_roles

> **LOCKED per figure.** Every text element uses exactly one role. Same role = same font size across the entire figure. No role may drift in size.

```
- font_family: "Times New Roman"     # MANDATORY — never Arial, never Calibri
- figure_title: 10pt bold            # Hero title / main figure title
- section_title: 9pt bold            # Region headers / module titles
- body_label: 7pt                    # Internal labels / sub-module names
- sub_label: 6.5pt                   # Description text / secondary labels
- annotation: 6pt                    # Footnotes / connector labels / citations
- detail: 5.5pt                      # Leaf-level text / tertiary information
```

Fill actual values based on the figure's complexity and column width. Single-column figures may scale down by 0.5-1pt across all roles.

## color_roles

> **LOCKED per paper (from paper-style-lock.md).** Fill the semantic roles used by THIS figure. Every fill/stroke in generated code references exactly one role below.

```
# Signal family (Nature Blue — default for academic submissions)
- primary_dark: "#0F4D92"          # Hero fill — ONLY ONE element per figure (90/10 rule)
- primary_mid: "#2C6FB7"           # Secondary module fills / hero sub-containers
- primary_light: "#7BABDB"         # Light borders / decorative accents
- primary_bg: "#E8F0F9"            # Container background tints

# Neutral family
- neutral_dark: "#272727"           # Primary text on light backgrounds
- neutral_mid: "#767676"            # Secondary text / region labels
- neutral_light: "#CFCECE"          # Borders / subtle dividers
- white: "#FFFFFF"                  # White fill
- sub_fill: "#F8F9FC"               # Near-white background for edge regions

# Text on colored backgrounds
- text_white: "#FFFFFF"             # Text on dark fills (auto-selected by is_dark())
- text_dim: "#BBD4F0"               # Dimmed text on primary_dark
- text_gray: "#616161"              # Description text on white cards

# Connector colors
- connector_primary: "#4D6A7A"     # Main flow arrows / data flow
- connector_secondary: "#8A9BA8"   # Control flow / feedback / cycle arrows

# Accent (≤2 uses per figure)
- accent_gold: "#E8A817"            # Stars / emphasis markers
```

## shape_vocabulary

> **Minimum 3 distinct MSO_SHAPE types per figure.** Map each semantic concept to a shape type. All shapes used in the figure must be listed here.

```
- ROUNDED_RECTANGLE   # Default module / container / card
- OVAL                # State node / lifecycle stage / tree root
- CHEVRON             # Pipeline step / sequential process
- CAN                 # Data store / database / file cabinet
- STAR_5_POINT        # Highlight / emphasis marker (≤2 per figure)
- RECTANGLE           # Only for dashed-border containers or special cases
- DIAMOND             # Decision point
- CLOUD               # Remote service / external entity
- HEXAGON             # Hexagonal node / special concept
- FOLDED_CORNER       # Document / file
```

Actual selection (≥3):

```
- [SHAPE_TYPE_1]      # [semantic purpose in this figure]
- [SHAPE_TYPE_2]      # [semantic purpose]
- [SHAPE_TYPE_3]      # [semantic purpose]
```

## spacing_constants

> **LOCKED per paper (from paper-style-lock.md).** All gaps and margins in the figure derive from these values.

```
- intra_group_gap: 0.15cm    # Gap between elements within the same group
- inter_group_gap: 0.3cm     # Gap between adjacent groups
- region_gap: 0.4cm          # Gap between major regions (panels)
- container_padding: 0.2cm   # Internal padding inside containers
- text_margin: 1pt           # Margin inside text boxes
- connector_channel: 0.3cm   # Minimum clearance for connector routing paths
- min_shape_size: 0.4cm      # Smallest allowed shape dimension
```

## layer_inventory

> All 5 layers must be accounted for. Every element in the figure belongs to exactly one layer.
> L1 drawn first (behind), L5 drawn last (on top).

```
L1_connectors:
  - {id: "arrow_<name>", from: "<src>", to: "<dst>", style: solid|dashed|dotted, label: "<text>"}
  # ...

L2_containers:
  - {id: "bg_<name>", region: "<region>", fill: "<color_role>", bbox: {x, y, w, h}}
  # ...

L3_subcomponents:
  - {id: "<name>", group: "<group>", shape: "<SHAPE_TYPE>", bbox: {x, y, w, h}, fill: "<color_role>", border: "<color_role>"}
  # ...

L4_highlights:
  - {id: "<name>", group: "<group>", shape: STAR_5_POINT, bbox: {cx, cy, r}}
  - {id: "marker_01", group: "<group>", type: reading_marker, text: "①"}
  # ...

L5_text:
  - {id: "<name>", group: "<group>", role: "<typography_role>", text: "<content>", bbox: {x, y, w, h}}
  # ...
```

## groups

> Every shape and text element belongs to exactly one group. Groups declare their structure type and bounding box. No orphan elements.

```yaml
groups:
  - id: "<group_name>"
    layer: L2 | L3 | L4 | L5
    parent_region: "<region_name>"
    structure: tree | pipeline | cycle | container | bridge | hub-spoke | parallel | state-machine
    bbox: {x: <cm>, y: <cm>, w: <cm>, h: <cm>}
    physical_assoc: "<real-world analog>"   # e.g., "file cabinet", "tree", "bookshelf"
    elements:
      - "<element_id_1>"
      - "<element_id_2>"
      # ...
```

## connectors

> Cross-module connectors with explicit routing.

```
connectors:
  - {id: "<name>", from_element: "<id>", to_element: "<id>", from_anchor: top|bottom|left|right, to_anchor: top|bottom|left|right, style: solid|dashed|dotted, label: "<text>", label_position: midpoint|near_source|near_target}
  # ...

# Arrow budget: ≤ 5 explicit cross-module connectors per figure.
# Use position/proximity for same-module relationships.
```

## physical_associations

> **Minimum 2 physical-world analogs per figure.** Abstract concepts mapped to recognizable visual metaphors.

```
- association_1: "<abstract concept>" → "<physical analog>" (<shape type> + <visual detail>)
- association_2: "<abstract concept>" → "<physical analog>" (<shape type> + <visual detail>)
```

## per_figure_overrides

> Declare any values that differ from `paper-style-lock.md`. If no overrides, this section is empty. All overrides must be explicitly listed — implicit deviation is a P3 failure.

```
# Example:
# - paper-style-lock sets figure_title: 10pt bold
# - This figure uses figure_title: 9pt bold because single-column
#   → Declare: figure_title: 9pt bold (override: single-column scaling)
```

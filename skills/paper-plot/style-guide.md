# Style Guide — Visual Conventions

Default visual conventions for paper-plot figures. Override per paper or venue requirements.

## Core Principle: Restrained Palette

**1 neutral family + 1 signal family + 1 accent family per figure.** No more. A figure with 5+ unrelated colors signals visual chaos. The same entity keeps the same hue across all panels — don't change a module's color just because it needs contrast in a different context.

Green/red are reserved for directional semantics (improvement ↑ / regression ↓), never for general categorical distinction.

## Color Palette

### Default: Nature Blue (推荐用于论文投稿)

**Signal family (your method / core modules):**

| Token | Hex | Role |
|-------|-----|------|
| `primary_dark` | `#0F4D92` | Hero module, main system |
| `primary_mid` | `#2C6FB7` | Secondary module |
| `primary_light` | `#7BABDB` | Sub-module, helper |
| `primary_bg` | `#E8F0F9` | Container background tint |

**Neutral family (external / reference / environment):**

| Token | Hex | Role |
|-------|-----|------|
| `neutral_light` | `#CFCECE` | Reference, background |
| `neutral_mid` | `#767676` | Border, secondary text |
| `neutral_dark` | `#272727` | Primary text |

**Accent family (use sparingly — ≤3 elements per figure):**

| Token | Hex | Role |
|-------|-----|------|
| `accent_gold` | `#E8A817` | Critical path, key insight |
| `accent_teal` | `#42949E` | Optimization, improvement |
| `accent_red` | `#B64342` | Bottleneck, regression (directional only) |

**Panel & connector colors:**

| Token | Hex | Role |
|-------|-----|------|
| `panel_border` | `#BDBDBD` | Panel/group boundary (0.5pt dashed) |
| `connector_primary` | `#4D6A7A` | Primary data flow arrows |
| `connector_secondary` | `#8A9BA8` | Secondary/control flow arrows |

### Blue Theme (legacy — for quick drafts)

| Role | Hex | Usage |
|------|-----|-------|
| Primary | `#1565C0` | Main system modules |
| Secondary | `#42A5F5` | Sub-modules, helpers |
| Tertiary | `#90CAF9` | Background layers |
| External | `#78909C` | Users, third-party systems |
| Highlight | `#FF7043` | Critical path (≤2 uses) |
| Text | `#212121` | All text |

### Palette Selection Rule

Select palette at P0. Do NOT change mid-figure. For a multi-figure paper, all figures share the same signal family — only accent colors may vary per figure.

### 90/10 Color Noise Reduction Rule

**90% of visual elements should use grayscale or low-saturation neutral tones. Only 10% — the hero module and its direct outputs — get the saturated signal color.**

This is the single most powerful rule for creating visual hierarchy. When every module uses the same saturated blue, nothing stands out and the reader scans randomly.

| Element Category | % of Canvas | Color Treatment |
|---|---|---|
| **Hero module** (core innovation) | ~10% | `primary_dark` (#0F4D92) — the ONLY element with saturated signal color |
| **Direct support** (hero's immediate context) | ~20% | `primary_light` (#7BABDB) or `primary_bg` (#E8F0F9) — tinted but not competing |
| **Infrastructure** (everything else) | ~70% | Grayscale: `neutral_light` (#CFCECE) fill, `neutral_mid` (#767676) border, `neutral_dark` (#272727) text |

**Checklist before finalizing any figure:**
- [ ] Can I identify the ONE hero element in under 0.5 seconds? (Squint Test)
- [ ] Are there any non-hero elements using `primary_dark`? If so, demote them to `primary_light` or grayscale.
- [ ] Do supporting modules recede visually, letting the hero dominate? If not, reduce their saturation.
- [ ] Would the figure still communicate its core claim if all non-hero elements were gray? If not, the hero isn't prominent enough.

### Semantic Color Constraints

1. **Identity:** Same module = same hue across all figures in the paper
2. **Direction:** Green/red ONLY for improvement/regression semantics
3. **Contrast:** Dark fill → white text. Light fill → dark text. Always check readability.
4. **White background:** All panels have white or near-white backgrounds
5. **Saturation budget:** At most ONE element per figure uses the darkest signal color. Everything else is lighter or gray.

## Typography

**Font family: Times New Roman — MANDATORY for all text.** No Arial, no Calibri, no Helvetica. Times New Roman only. This applies to every text run in every shape, text box, and connector label. The serif font matches academic paper body text and ensures visual consistency across all figures.

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Module title (on dark fill) | Times New Roman | 9pt | Bold | `#FFFFFF` |
| Module title (on light fill) | Times New Roman | 9pt | Bold | `#272727` |
| Sub-component label | Times New Roman | 8pt | Bold | `#272727` |
| Sub-component description | Times New Roman | 6.5pt | Regular | `#616161` |
| Connector label | Times New Roman | 6.5pt | Regular | `#4D6A7A` |
| Annotation | Times New Roman | 6pt | Italic | `#9E9E9E` |
| Panel/group label | Times New Roman | 7pt | Italic | `#9E9E9E` |

**Key rules:**
- Font sizes are a 3-level hierarchy: 9pt (title) → 8pt (label) → 6.5pt (detail). Never use more than 3 sizes per figure.
- All text must remain editable (never convert to paths/outlines).
- Vertical alignment: middle (`MSO_ANCHOR.MIDDLE`) for all component shapes.
- Text margin: 1pt all sides.
- Word wrap: enabled on all text frames.
- Prefer direct labels over legends when spatial positions are fixed.

### Luminance-Aware Text Color (MANDATORY)

**Every filled shape MUST verify text contrast against its fill.** This is not optional — dark fill → white text, light fill → dark text.

```python
def is_dark(hex_color, threshold=128):
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return (0.299*r + 0.587*g + 0.114*b) < threshold
```

| Fill Type | Text Color | Example |
|-----------|-----------|---------|
| `primary_dark` (#0F4D92) | `#FFFFFF` (white) | Hero module title |
| `primary_mid` (#2C6FB7) | `#FFFFFF` (white) | Secondary module title |
| `primary_light` (#7BABDB) | `#272727` (dark gray) | Sub-module on light blue |
| `primary_bg` (#E8F0F9) | `#272727` (dark gray) | Light tint backgrounds |
| `neutral_light` (#CFCECE) | `#272727` (dark gray) | Gray backgrounds |
| White (#FFFFFF) | `#272727` (dark gray) | Default |

**Hard check:** Before declaring a figure done, verify every filled shape's text color. A light fill with white text = invisible. A dark fill with black text = unreadable.

### Text Box Width Constraints

Text boxes must be sized to their content. Neither too narrow (splits words) nor too wide (one long sprawl).

| Constraint | Rule | Check |
|-----------|------|-------|
| **Min width** | Must fit the longest word at the given font size without breaking | At 7pt Times New Roman, "Internalized" ≈ 1.2cm — so text boxes < 1.0cm are almost always too narrow |
| **Max width** | Multi-word labels should wrap to 2–3 lines, not sprawl as one line | If a 5+ word label fits on one line, the box is too wide |
| **Optimal** | Text fills 60–80% of the box width, wraps naturally | Adjust box width until text looks balanced |

**Anti-pattern:** `TB(slide, x, y, 0.8, 1.5, 'Actions')` — a 0.8cm-wide box cannot fit "Actions" at 6pt without breaking mid-word.

## Shapes

| Semantic | PPT Shape | Corner Radius | Border | Fill |
|----------|-----------|---------------|--------|------|
| Module container | `ROUNDED_RECTANGLE` | 0.25cm | 1pt solid | Signal family |
| Sub-component | `ROUNDED_RECTANGLE` | 0.15cm | 0.5pt solid | White or `primary_bg` |
| Decision / branch | `DIAMOND` | — | 1pt solid | White |
| External entity | `ROUNDED_RECTANGLE` | 0.2cm | 1pt dashed | Neutral family |
| Panel / group box | `RECTANGLE` | none | 0.5pt dashed | Very light tint |
| Data store (DB) | `CAN` | — | 1pt solid | Signal family |
| Status node / state | `OVAL` (circle) | — | 0.8pt solid | White or tinted |
| Process step / flow | `CHEVRON` | — | 0.8pt solid | Signal family |
| Highlight / special | `STAR_5_POINT` or `STAR_4_POINT` | — | 0.5pt | Accent gold |
| Cloud / remote | `CLOUD` | — | 0.8pt solid | Neutral family |
| Document / file | `FOLDED_CORNER` | — | 0.5pt solid | White |
| Tag / badge | `ROUNDED_RECTANGLE` | 0.4 (pill) | 0.5pt solid | Accent family |
| Hexagon node | `HEXAGON` | — | 0.8pt solid | Signal family |

**Shape variety requirement: ≥ 3 distinct MSO_SHAPE types per figure.** A figure with only ROUNDED_RECTANGLE + OVAL is acceptable but minimal. A figure with ROUNDED_RECTANGLE + OVAL + CHEVRON + STAR is rich. Use shapes that match the semantics:

- Tree structure → OVAL (root) + line connectors (branches) + ROUNDED_RECTANGLE (leaf nodes)
- Pipeline → CHEVRON arrows for flow direction + ROUNDED_RECTANGLE for stages
- Lifecycle → OVAL in a ring arrangement + curved connectors
- Data flow → CAN for data stores + ROUNDED_RECTANGLE for processors
- Cloud services → CLOUD shape for remote/cloud components

**Visual hierarchy through borders:**
- Level 1 (module container): 1pt solid, signal color fill
- Level 2 (sub-component): 0.5pt solid, white/tinted fill
- Level 3 (annotation): no border, transparent fill

### Text-Shape Binding

Every text label MUST be visually bound to the shape it describes. A floating label equidistant from two shapes is ambiguous.

| Binding Method | When to Use | Example |
|---------------|-------------|---------|
| **Internal label** | Text fits inside the shape with ≥1pt margin | Module name inside its container |
| **Adjacent label** | Text placed outside, aligned to shape edge, gap ≤ 0.15cm | Short annotation next to a node |
| **Leader line** | Text placed at a distance, connected by a thin dotted line | Callout for a small or crowded element |
| **Shared background** | Text and shape share a tinted background zone | Group label over multiple sub-components |

**Binding rules:**
- A label's distance to its own shape must be **≤ 50% of the distance to any other shape**. If a label is 0.3cm from shape A and 0.3cm from shape B → ambiguous → use a leader line or reposition.
- Two shapes must not share the same label position — if two labels overlap, one must move.
- Internal labels: the shape MUST be wide enough for the text + 2× text_margin. If text doesn't fit, enlarge the shape or abbreviate.

### Text Alignment

| Property | Default |
|----------|---------|
| Horizontal | Center (`PP_ALIGN.CENTER`) |
| Vertical | Middle (`MSO_ANCHOR.MIDDLE`) |
| Text margin (all sides) | 1pt |
| Word wrap | Enabled |

## Connectors

| Relationship | Style | Weight | Arrow | Color |
|-------------|-------|--------|-------|-------|
| Data flow (primary) | Solid | 1.2pt | Filled triangle end | `connector_primary` |
| Control flow | Solid | 0.8pt | Filled triangle end | `connector_secondary` |
| Feedback / loop | Dashed | 0.75pt | Filled triangle end | `connector_secondary` |
| Optional / async | Dashed | 0.5pt | Open triangle end | `connector_secondary` |
| Bidirectional | Solid | 1pt | Filled triangle both ends | `connector_primary` |
| Annotation pointer | Dotted | 0.5pt | None | `#9E9E9E` |
| Panel boundary | Dashed | 0.5pt | None | `panel_border` |

**Routing rules:**
- Avoid diagonal lines crossing the canvas. Use elbow connectors or segmented routing.
- Cross-panel connectors: route through a central channel or panel edge ports.
- No connector may pass through a component box or its label.
- Arrow style: Filled triangle (`EndArrow=4`).
- Dash semantics: Solid = synchronous/certain/primary. Dashed = async/optional/feedback. Dotted = annotation only.

### Connector Routing Discipline

Connectors are the #1 source of visual chaos. A figure with well-routed connectors looks professional; one with spaghetti lines looks amateur.

**Hard rules:**

1. **No chained straight connectors.** Three separate straight segments pretending to be one routed line produce visible gaps at joints. Use ONE connector per logical connection. If you must bend, use the shape edges as natural routing points.

2. **Anchor to shape edges, not arbitrary coordinates.** A connector from (5.0, 5.7) to (7.5, 2.0) that doesn't touch any shape edge looks disconnected. Begin/end connectors AT the edge of the source/target shape.

3. **Label placement on connectors:** Connector labels must be positioned adjacent to the line midpoint, not floating at an unrelated coordinate. A label at (0.15, 5.5) for a connector spanning (0.6, 9.6)→(0.6, 2.0) is ambiguous.

4. **Z-order is mandatory.** All connectors MUST render behind all shapes. The `reorder_connectors_behind()` function must run before every save. A connector that obscures a shape or label is a critical bug.

5. **Routing channels:** When multiple connectors cross between the same two regions, route them through a shared channel (a narrow vertical or horizontal band) rather than scattering them across the canvas. This creates visual order.

6. **Bidirectional pairs:** Two opposing arrows (A→B and B→A) must be parallel, spaced 0.3–0.5cm apart, with clear directional labels. Never cross them.

## Layout

### Grid & Spacing

- Grid snap: 0.25cm
- Page margin: 0.25cm from slide edge
- Horizontal gap: 0.3cm (same panel), 0.5cm (between panels)
- Vertical gap: 0.35cm (same module), 0.5cm (between modules)
- Padding inside containers: 0.3cm (top, for title), 0.2cm (sides)
- Panel padding: 0.3cm inside panel boundary

### Minimum Sizes

- Module container: 2.5cm × 1.5cm
- Sub-component: 1.2cm × 0.8cm
- Text box: 0.5cm × 0.3cm

### Drawing Order (z-order matters!)

Connectors and lines MUST be drawn BEFORE shapes so they sit behind, never obscuring components or text:

1. Background / panel tints → 2. All connectors & arrows → 3. Module containers → 4. Sub-components → 5. Text labels & annotations

**Connectors behind, shapes on top, text always front.** A connector crossing through a component label is a critical bug.

### No Decorative Panel Boxes

**Do not draw dashed boundary boxes around logical groups** (e.g., "SERVER" and "CLIENT" regions). Use whitespace, alignment, and proximity to convey grouping. Dashed boxes add visual noise without information. Top-tier papers use spacing, not boxes.

Exception: image plates, microscopy panels, or when the venue template explicitly requires panel boundaries.

### Luminance-Aware Text Color

Text color on filled shapes must adapt to background brightness:

```python
def is_dark(hex_color, threshold=128):
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return (0.299*r + 0.587*g + 0.114*b) < threshold
# dark fill → white text; light fill → dark text
```

Never hardcode white text — a light-colored sub-component needs dark text for readability.

## Visual Richness

### Internal Structure Must Reflect Semantics

A "box containing smaller boxes" is lazy. The internal layout of a module must communicate its semantic structure:

| If the data/logic is... | Draw it as... | Not as... |
|---|---|---|
| Linear pipeline (A→B→C) | Horizontal chain with flow arrows between stages | 3 rectangles in a row with no connectors |
| Hierarchical tree (Root→Branches→Leaves) | Root node + branch lines downward + leaf nodes | Stacked rectangles |
| Lifecycle / state cycle (L0→L1→L2→L0) | Circular ring, or horizontal sequence with return arrow | 4 adjacent rectangles |
| Parallel independent items | Side-by-side cards/pills with equal visual weight | List inside one big box |

**Shape variety rule:** Minimum 3 distinct MSO_SHAPE types per figure. Use circles (`OVAL`) for status nodes, cylinders (`CAN`) for data stores, diamonds (`DIAMOND`) for decision points, pills (high-radius `ROUNDED_RECTANGLE`) for tags/badges.

### Text-to-Graphics Ratio

Target **70% visual structure, 30% text labels.** If a component communicates purely through "text in a box," ask whether a visual structure can replace or supplement it.

- Good: A lifecycle shown as 4 circular nodes with connecting arrows + short labels
- Bad: A lifecycle described as "Active → Idle → Sleep → Off" in a single text box

## Relationship Economy

Not every logical relationship needs an explicit arrow. Use the lightest visual tool that works:

| Expression | Visual Weight | When to Use |
|---|---|---|
| **Position / proximity** | Lightest | Same-module upstream→downstream |
| **Text label** | Light | Supplementary note that would clutter if drawn as line |
| **Shared color / tint** | Light | Components belonging to same function |
| **Explicit arrow** | Heavy | Cross-module data flow, control flow, bidirectional protocol |
| **Bold annotated arrow** | Heaviest | The single most important relationship in the figure |

**Arrow budget: ≤ 5 explicit cross-module arrows per figure.** If you need more:
1. Check if some relationships can be expressed by position/proximity
2. Check if some modules should be merged into a shared parent (making their arrows intra-module, thus implicit)
3. Use text labels for supplementary relationships

## Reading Guidance

Every figure MUST have a designed reading path — the reader should never wonder "where do I look first?"

### Three Elements

| Element | Definition |
|---|---|
| **Entry point** | Which component draws the eye first? Mark by **size** (largest), **position** (top-left), and **color** (darkest fill) |
| **Reading path** | Natural traversal: top→bottom, left→right, or numbered ①②③ |
| **Traversal end** | Where the path concludes — usually bottom or bottom-right |

### Fitts's Law for Visual Hierarchy

The hero module MUST dominate the canvas. Derived from Fitts's Law in UI design: the most important target should have the largest visual footprint and strongest contrast.

**Hard requirement:** The hero module's area must be **≥ 1.5× the area of any other individual module.** If two modules have similar visual weight, the reader cannot distinguish primary from secondary.

```
Hero area ≥ 1.5 × max(any_other_module_area)
Hero color = primary_dark (darkest in palette)
Hero position = top-left or center (natural entry points)
```

**Check:** Remove all text labels. Can you still identify the hero? If not, the size/color distinction is insufficient.

### Four Guidance Tools

| Tool | Mechanism | Usage |
|---|---|---|
| **Size** | Hero module ≥ 1.5× area of any other module (Fitts's Law) | "This is the hero — start here" |
| **Position** | Entry at top-left or center; follow natural reading direction | Matches left→right, top→bottom scanning habit |
| **Color depth** | Hero = `primary_dark` (ONLY element with saturated signal color per 90/10 rule) | Darker = more important, guides eye naturally |
| **Sequence markers** | ① ② ③ labels or "Step 1 / Step 2 / 3" annotations | For complex multi-step flows where position alone isn't enough |

### Anti-Patterns

- All modules identical size → no visual hierarchy → reader scans randomly
- Entry point at bottom-right → violates reading habit → cognitive friction
- Core module in pale color while background is bold → inverted visual weight
- Dense arrows forming a "spaghetti" mesh → reader cannot trace any single flow
- Multiple modules using `primary_dark` → violates 90/10 rule → nothing stands out
- Hero module < 1.5× area of other modules → violates Fitts's Law → no clear entry point

### Squint Test (MANDATORY before declaring done)

Step back from the screen, squint your eyes until details blur. Ask:

1. **What pops out first?** It MUST be the hero module (core innovation). If a border, gridline, or secondary module pops out instead → visual hierarchy is broken.
2. **How many saturated color blocks do you see?** You should see exactly ONE. If you see 2+ → violated 90/10 rule.
3. **Can you trace the reading path with blurred vision?** The entry→flow→end sequence should be visible even without reading any text.

Fix any failures before export. The squint test catches what normal inspection misses.

## Export

| Format | Usage | Settings |
|--------|-------|----------|
| PPTX | Editable source | Native shapes, no embedded images |
| PNG | Quick preview, submission | 300 dpi, white background |
| SVG | Vector handoff, post-processing | Editable text (`<text>` tags, not paths) |
| PDF | Review, print | From saved PPTX |

- Single column: 8.9cm → PNG 1051px wide
- Double column: 17.8cm → PNG 2102px wide
- Background: white (not transparent)
- **Always save PPTX before exporting.** Exporting from an unsaved state = stale output.

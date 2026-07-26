# Academic Layout System

## Contents

1. Measurement model
2. Shared geometry
3. Page-role allocations
4. Conference and defense variants
5. Density and whitespace
6. Common failure patterns

## 1. Measurement Model

Treat image-to-text ratios as planning ranges, not quotas. Measure only the usable content zone after title, footer, citation, and optional navigation areas are removed.

- `visual` includes figures, charts, tables, equations, scientific images, and explanatory diagrams.
- `text` includes titles inside the content zone, bullets, annotations, metric labels, and conclusions.
- `whitespace` includes clear separation around evidence; it is not unused failure space.
- Visual and text bounding boxes may overlap, so automated coverage values do not need to sum to 100%.

The observed academic examples used about half of the total canvas for text and visual object bounds, with the remainder carrying margins, hierarchy, and separation. Use that as a warning against both sparse drafts and full-canvas packing, not as a target for every slide.

## 2. Shared Geometry

Use a 1440 x 810 canvas.

```text
Top:      54-76 px title zone
Body:     610-660 px usable evidence zone
Bottom:   30-44 px citation/page zone
Sides:    72-96 px safe margin
Gutter:   28-48 px between primary regions
```

For an institutional defense rail:

```text
Rail:     150-205 px
Gap:      24-32 px
Content:  remaining width with at least 64 px right margin
```

Keep the rail at roughly 11-14% of slide width. Shorten labels before widening it. Use one active state and neutral inactive states. The agenda wording, rail wording, title numbering, and section assignment must match.

## 3. Page-Role Allocations

Choose the page role first. Percentages refer to the usable content zone.

| Page role | Visual share | Text share | Preferred composition |
|---|---:|---:|---|
| Cover | 0-25% | 20-35% | Strong title block, identity metadata, generous negative space |
| Agenda/orientation | 0-20% | 45-65% | Ordered sequence or compact chapter map |
| Motivation/gap | 30-50% | 30-45% | One observation plus one explicit gap |
| Concept/background | 35-55% | 25-40% | Diagram or example with only essential definitions |
| Method/architecture | 50-70% | 20-35% | Dominant process, architecture, equation, or experimental design |
| Result | 55-75% | 15-30% | Large evidence figure, takeaway title, one annotation or metric strip |
| Comparison/ablation | 45-65% | 20-35% | Aligned chart/table plus verified comparison and boundary |
| Synthesis/contribution | 20-40% | 40-60% | Two or three evidence-backed conclusions, not feature cards |
| Limitations | 10-30% | 45-65% | Boundary, consequence, and mitigation/future test |
| Progress/risk/plan | 20-35% | 50-65% | Milestone sequence plus risk and response |
| Close/Q&A | 0-20% | 20-40% | Intellectual conclusion with generous negative space |

Use visual-to-text ratios of roughly `65:35` for result pages, `60:40` for method pages, `45:55` for explanation pages, and `30:70` for progress/plan pages. Do not add decorative images or empty labels to reach a ratio.

## 4. Conference And Defense Variants

### Conference Or Seminar

- Use the full width for evidence; omit persistent navigation.
- Keep most slides to one primary figure or one coherent diagram.
- Use a compact footer only when venue, page, and source context materially help orientation.
- Alternate silhouettes across the deck: split, full-width figure, process, result, and synthesis.
- Keep most pages in the 35-68% whole-canvas object-coverage range.

### Thesis, Proposal, Or Dissertation Defense

- Use persistent chapter navigation only when the talk has at least four substantive sections.
- Reserve more room for definitions, validity, progress, limitations, and decisions.
- Use section dividers sparingly; the rail and title numbering already provide orientation.
- Allow slightly higher information density than a short conference talk, but keep body text at 18 pt or larger where institutional constraints allow.
- Put detailed derivations, full tables, and committee-specific evidence in backup slides.

### Bilingual Deck

- Use one language as the primary visual language.
- Put the translation in notes or a short secondary line; do not duplicate every paragraph.
- Reserve 15-25% extra vertical space for translated titles and technical term mapping.

## 5. Density And Whitespace

Use these review triggers after PPTX export:

- Whole-slide object coverage below 28%: inspect for a draft-like or unfinished page.
- Whole-slide object coverage above 78%: inspect for crowding, clipping, and unreadable figures.
- More than four independent visual regions: merge, prioritize, or split the slide.
- More than two full sentences outside the title and conclusion: move detail to notes or backup.
- A figure below 40% of the content-zone width when it is the primary evidence: enlarge or change the layout.
- A title requiring body-size type: rewrite the claim or use an intentional two-line title.

Whitespace must separate conceptual groups and protect projection readability. It should not create a large dead quadrant while evidence is compressed elsewhere.

## 6. Common Failure Patterns

- Do not place a wide multi-panel figure in a narrow side column.
- Do not stretch figures to a fixed box; preserve aspect ratio.
- Do not fill empty areas with pale rounded cards, labels, icons, or unsupported copy.
- Do not repeat the same card grid on every slide.
- Do not put a conclusion in a large bordered box when a rule and short emphasized sentence will work.
- Do not let a defense navigation rail compete with the evidence area.
- Do not use tiny manuscript screenshots when a high-resolution crop or focused redraw is possible.
- Do not solve overflow by shrinking body text below the selected design minimum.

# Academic Presentation Design

## Contents

1. Design intent
2. Canvas and grid
3. Typography
4. Color systems
5. Page roles
6. Scientific visuals
7. Conference and defense differences
8. Conversion constraints
9. Reusable academic style families

## 1. Design Intent

Make evidence easy to see, compare, and remember. Academic design should feel precise, restrained, and authored for the field. It should not resemble a startup pitch, product dashboard, poster collage, or science-fiction interface.

Use one primary composition per slide. Let a strong figure, chart, equation, or claim occupy the visual center. Avoid repeated card grids, pill labels, button-like boxes, decorative gradients, glowing lines, bokeh, and arbitrary 3D effects.

## 2. Canvas And Grid

- Canvas: 1440 x 810 px, 16:9.
- Safe outer margin: 72-96 px left/right and 56-76 px top/bottom.
- Title zone: reserve 72-104 px; never allow a one-line title to wrap accidentally.
- Footer zone: reserve 28-40 px for citation and page number.
- Default alignment: equal left and right margins.
- Use 8 px spacing increments. Keep repeated baselines and gutters exact.
- Do not place evidence-critical content within 32 px of an edge.

Vary adjacent slide silhouettes: full-width figure, text/figure split, process, comparison, synthesis, and text-led close. Variation must follow content, not decoration.

## 3. Typography

Use fonts available on the delivery machine. Prefer Arial, Aptos, Source Sans, Noto Sans, Microsoft YaHei for Chinese sans-serif decks, Times New Roman for a deliberately classical conference treatment, or an explicitly supplied institutional typeface. Use no more than one body family plus one math/symbol fallback.

| Role | HTML authoring size | Approx. PPT size | Rule |
|---|---:|---:|---|
| Deck title | 56-72 px | 42-54 pt | Short, two lines only when intentional |
| Slide title | 40-48 px | 30-36 pt | Prefer one line; write as a takeaway |
| Section title | 48-64 px | 36-48 pt | Minimal copy |
| Subheading/callout | 27-34 px | 20-25.5 pt | One clear hierarchy level |
| Body | 24-32 px | 18-24 pt | Use 1.25-1.45 line height |
| Dense body | 21-24 px | 16-18 pt | Use only after shortening and reflow |
| Figure labels recreated on slide | 21-27 px | 16-20 pt | Must survive projection |
| Citation/footer | 16-21 px | 12-16 pt | Never hide essential qualifiers here |

Shorten copy or select a different layout before going below these ranges. Do not scale typography with viewport width. Use letter spacing 0 except for short uppercase metadata labels.

## 4. Color Systems

### Academic Light (Default)

| Token | Value | Use |
|---|---|---|
| Ink | `#16324F` | Titles, axes, primary text |
| Evidence | `#2D6A4F` | Positive emphasis, selected series |
| Contrast | `#C65D3A` | Exceptions, limitations, second series |
| Neutral | `#5B6470` | Secondary text |
| Rule | `#D7DCE2` | Dividers, table rules |
| Paper | `#FFFFFF` | Background |
| Soft field | `#F3F5F7` | Sparse grouping only |

### Academic Technical (Conditional)

Use only for computing, engineering, data, or similarly technical work when a dark room and projector support it.

| Token | Value | Use |
|---|---|---|
| Field | `#111827` | Background |
| Paper | `#F8FAFC` | Primary text |
| Signal | `#38BDF8` | Primary evidence |
| Validation | `#A3E635` | Secondary evidence |
| Warning | `#FB923C` | Failure/limitation |
| Grid | `#334155` | Rules and connectors |

Do not add neon glow, digital rain, HUD rings, or code-window decoration. Test dark slides on the actual projector when possible. Keep a light fallback for print or bright rooms.

Use color to encode meaning consistently. Do not rely on red/green alone; add labels, line styles, or shapes. Keep most text neutral and reserve accents for evidence.

## 5. Page Roles

### Cover

Show title, optional research question, presenter, institution, venue, and date. Keep the title slide minimal. Use an actual scientific visual only when it is legible and central to the work.

### Motivation And Gap

Prefer one key observation plus one gap statement. Show a compact literature map, trend, or representative example only if it establishes the gap.

### Research Question Or Contribution

Use a clean hierarchy: question, scope, and why it is answerable. Avoid three-card feature layouts.

### Method

Show the minimum structure needed to interpret results. Use a pipeline, experimental design, data flow, or equation. Put implementation inventory in backup slides.

### Results

Let the figure or chart dominate. Use a takeaway title, one annotation, and a compact source/method footer. Avoid surrounding the result with decorative panels.

### Comparison Or Ablation

Use aligned axes or a restrained table. Highlight only the cells or series that prove the claim. Keep baseline semantics visible.

### Limitations

State boundary, consequence, and mitigation or future test. Use the contrast color sparingly; do not frame limitations as marketing disclaimers.

### Close

Resolve the opening question with two or three evidence-backed conclusions. A generic `Thank you` may appear as metadata, but it must not replace the intellectual conclusion.

## 6. Scientific Visuals

- Preserve figure aspect ratio and labels.
- Use `object-contain` by default; crop only after visual inspection.
- Make the active result visually dominant while keeping comparison context.
- Add direct labels where they reduce legend lookup.
- Use the same colors for the same methods or cohorts across slides.
- Use tables for exact lookup and charts for patterns; do not use both for the same data without a reason.
- Use diagrams only when relationships are harder to explain linearly. Keep labels short and connectors unambiguous.
- For qualitative examples, show enough context to prevent cherry-picking.

## 7. Conference And Defense Differences

| Dimension | Conference/seminar | Defense |
|---|---|---|
| Pace | Faster; fewer details | Slower; more auditability |
| Opening | Stakes and gap quickly | Scope, gap, and research questions |
| Method | Only what results require | Assumptions, validity, and reproducibility |
| Results | Selective central evidence | Complete contribution chain |
| Limitations | Brief but explicit | Explicit threats to validity and scope |
| Appendix | Extra benchmarks | Methods, derivations, robustness, committee Q&A |

## 8. Conversion Constraints

The HTML is converted to editable PowerPoint objects through PptxGenJS. Use export-safe primitives:

- solid fills, simple borders, standard text, raster/vector images, and uncomplicated flex/grid layouts;
- no animation-dependent meaning;
- no CSS filters, masks, blend modes, pseudo-elements, or browser-only effects;
- no important content in background images;
- no auto-height containers whose size depends on late font loading;
- no unsupported icon font glyphs.

Browser screenshots are an authoring check, not final proof. Always inspect the rendered PPTX because line breaks, image placement, and font substitution may change.

## 9. Reusable Academic Style Families

Choose one family before authoring. Do not mix them casually.

### Modern Academic Sans

Use the default light palette with Arial, Aptos, Source Sans, Noto Sans, or Microsoft YaHei. This is the safest choice for mixed audiences, defenses, and bilingual decks. Use a strong title line, restrained rules, and figures without decorative frames.

### Classical Conference Serif

Use Times New Roman only when the venue or reference deck clearly benefits from a traditional scholarly tone. Use a white field, navy title/footer bands, red only for the active claim, and larger body type than a manuscript. Avoid imitating the paper's dense typography.
When you need a helper-level reference for this treatment, read [conference-genjs-few-shot.md](conference-genjs-few-shot.md) and borrow hierarchy, footer, and takeaway geometry without changing the skill's HTML-first workflow.

### Institutional Defense

Recreate the institution's cover, chapter marker, title rule, page marker, and navigation language in HTML. Do not import a source PPTX master or switch to COM. Keep the content zone wider than the navigation zone; the rail exists for committee orientation, not decoration.

### Technical Dark

Reserve for a deliberate section or an entire engineering deck in a dark room. Keep the same geometry and evidence discipline as the light system. Provide a light fallback when the projector or printing conditions are unknown.

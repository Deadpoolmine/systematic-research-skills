# P0: Director — Figure Intent & Type Selection

## Role

Director determines WHY a figure exists and WHAT type it should be. No shapes drawn yet — only intent and classification.

## Input

- Paper section text (from L1 figure placement or user paste)
- User description of desired figure
- Existing figures list (for consistency context)

## Process

### 0. Template Cleanup (MANDATORY — before anything else)

The template PPT files contain example figures from previous work. These are reference slides for structure analysis only. When the generator clones a template slide, it **automatically strips ALL existing shapes** before adding new ones. 

<HARD-GATE>
After P1/P2 generation, verify: the output slide contains ONLY the shapes defined in our spec. Zero template artifacts. If any residual shapes appear, the generator's `clean_slide()` has a bug — fix it before proceeding.
</HARD-GATE>

The templates serve two separate purposes:
- **Analysis (P0):** `ppt-slide-analyzer.sh` reads template slides to determine structure patterns → matches figure type
- **Generation (P1/P2):** `ppt-generator.sh` clones the slide layout (size + theme), **cleans all shapes**, then builds from scratch

### 1. Figure Type Classification

Match the content against the 5 predefined types:

| Type | Signal Words | Max Top-Level Modules | Typical Internal Structure |
|------|-------------|----------------------|---------------------------|
| `architecture` | "system", "architecture", "module", "layer", "component", "overview" | 2–3 | pipeline, tree, parallel |
| `flowchart` | "flow", "pipeline", "process", "algorithm", "step", "stage" | 3–5 (stages) | linear pipeline |
| `comparison` | "compare", "versus", "baseline", "ablation", "trade-off" | 2 (side-by-side) | parallel columns |
| `concept` | "idea", "concept", "motivation", "problem", "illustration" | 1–2 | tree or cycle |
| `data-plot` | "throughput", "latency", "performance", "distribution", "trend" | 1 (per chart) | axes + series |

**Module budget rule:** If your architecture figure has > 3 top-level modules, some of them are actually sub-modules. Merge them into shared parent containers before proceeding to P1.

<HARD-GATE>
If NONE of the 5 types clearly match, STOP and ask user: "What kind of figure do you envision? (architecture / flowchart / comparison / concept / data-plot)"
</HARD-GATE>

### 2. Column Width Selection

- **Single column (w=8.9cm):** Simple diagrams, small figures, concept illustrations
- **Double column (w=17.8cm):** Complex architectures, large flowcharts, multi-table comparisons

Default to double-column for architecture/flowchart/comparison unless user specifies single.

### 3. Template Slide Matching

Run `scripts/ppt-slide-analyzer.sh` (Linux) or `scripts/ppt-slide-analyzer.cmd` (Windows) to auto-discover available template slides and their structure fingerprints.

Match the figure type to the most structurally similar template slide:
- Count shape types (rectangles, diamonds, arrows, tables, text boxes)
- Match layout pattern (top-down layers? left-right flow? grid? centered?)
- Select the slide with closest structural signature

### 4. Core Element Extraction

List every component that must appear in the figure:
- Named components (from paper text)
- Relationships (data flow, control flow, dependency)
- Groupings / layers
- External entities (users, other systems)

## Output

Write `figures/<name>/figure-intent.md`:

```markdown
# Figure Intent: <figure-name>

## Figure Contract
A figure is a visual argument, not a collection of pretty boxes.

- **Core Claim:** <one sentence with an ACTIVE VERB — "X reduces Y by restoring Z", not "X results". Must be a defensible thesis the figure proves.>
- **Evidence Chain:** Map each visual element to the claim:
  - Element A → supports claim by showing <what>
  - Element B → supports claim by showing <what>
  - (If an element carries no unique evidence, REMOVE it — it's decoration)

## Context
- Paper Section: <section-number> <section-title>
- Purpose: <one-sentence why this figure exists>

## Classification
- Type: architecture | flowchart | comparison | concept | data-plot
- Column: single (w8.9) | double (w17.8)
- Template: templates/<file>.pptx Slide N

## Canvas
- Width: 8.9cm (single) | 17.8cm (double)
- Orientation: top-down | left-right | grid | centered | radial
- Aspect ratio: estimated height / width (flexible height)
- Whitespace distribution: margins 0.3cm, gap between major regions ~0.5cm

## Reading Order
- Primary: top→bottom | left→right | center→out | cyclic | feedback-loop
- Secondary (if multi-panel): panel reading order (A→B→C or row-major)

## Core Elements
### Components
1. <Component A> — <brief description, role: primary/secondary/external/highlight>
2. <Component B> — <brief description>
...

### Relationships
- A → B: <relationship type, solid/dashed/dotted, direction, label if any>
- B → C: <relationship type>
...

### Connector Semantics
- Solid lines: data flow, control flow
- Dashed lines: feedback, optional paths
- Dotted lines: annotations (if any)
- Bidirectional: <list if any>

### Repeated Motifs
- <stacked blocks / process stages / NN layers / tables / grid nodes / icons>
- If none, write "No repeated motifs — each component is unique"

### Groups / Layers
- Layer 1 (<name>): A, B
- Layer 2 (<name>): C, D
...

## Style Tokens
- Font family: Times New Roman (MANDATORY — never Arial/Calibri)
- Font size bands: title 12pt, label 10pt, sublabel 8pt, annotation 7pt
- Accent colors: <list if different from default blue #1565C0>
- Line weights: main border 1pt, internal 0.5pt, connectors 1pt
- Corner radius: 0.2cm (rounded rects) | none (sharp rects)
- Dash patterns: where used and why

## Editability Risks
- Dense text in small boxes: <identify if any, plan mitigation>
- Overlapping labels: <identify high-density regions>
- Multi-line text overflow: <identify components with long names>
```

## Hard Gate

User MUST confirm each of these ONE AT A TIME:
1. Core Claim clear? (one sentence, the figure's thesis)
2. Evidence Chain complete? (every visual element defends the claim)
3. Figure type correct?
4. Column width correct?
5. Template slide appropriate?
6. Core element list complete?

Do NOT batch all confirmations. Present each → discuss → confirm → next.

## Red Flags

- "This is obvious, let's skip P0" → Skipping = wrong type = full redo at P2
- "Just use the first template slide that looks similar" → Run the analyzer, don't guess
- "All components are clear from the text" → Extract explicitly; unstated assumptions cause missing elements
- "Style tokens can be figured out later" → Color scheme decided at P0; inconsistency across figures is visible in print

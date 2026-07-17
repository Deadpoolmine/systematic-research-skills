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

| Type | Signal Words | Template Structure |
|------|-------------|-------------------|
| `architecture` | "system", "architecture", "module", "layer", "component", "overview" | Rectangles + arrows + groups |
| `flowchart` | "flow", "pipeline", "process", "algorithm", "step", "stage" | Rectangles + diamonds + arrow chains |
| `comparison` | "compare", "versus", "baseline", "ablation", "trade-off" | Tables + side-by-side blocks |
| `concept` | "idea", "concept", "motivation", "problem", "illustration" | Simple shapes + groups + brief connections |
| `data-plot` | "throughput", "latency", "performance", "distribution", "trend" | Axes + data series |

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

## Context
- Paper Section: <section-number> <section-title>
- Purpose: <one-sentence why this figure exists>

## Classification
- Type: architecture | flowchart | comparison | concept | data-plot
- Column: single (w8.9) | double (w17.8)
- Template: templates/<file>.pptx Slide N

## Core Elements
### Components
1. <Component A> — <brief description>
2. <Component B> — <brief description>
...

### Relationships
- A → B: <relationship type>
- B → C: <relationship type>
...

### Groups / Layers
- Layer 1 (<name>): A, B
- Layer 2 (<name>): C, D
...

## Style Notes
- Preferred color palette: <if known>
- Must match style of: <existing figure name or "new style">
```

## Hard Gate

User MUST confirm each of these ONE AT A TIME:
1. Figure type correct?
2. Column width correct?
3. Template slide appropriate?
4. Core element list complete?

Do NOT batch all confirmations. Present each → discuss → confirm → next.

## Red Flags

- "This is obvious, let's skip P0" → Skipping = wrong type = full redo at P2
- "Just use the first template slide that looks similar" → Run the analyzer, don't guess
- "All components are clear from the text" → Extract explicitly; unstated assumptions cause missing elements

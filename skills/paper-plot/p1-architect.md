# P1: Architect — Layout & Spatial Structure

## Role

Architect designs the spatial organization. Two outputs: a structured natural-language layout plan (authoritative spec) and a rough PPT draft (visual preview). Both from the figure-intent.

## Input

- `figures/<name>/figure-intent.md` (from P0)
- `figures/paper-style-lock.md` (paper-wide style lock — shared typography/colors/spacing)
- Template PPT file path
- User feedback from P0 confirmation

## Process

### 0. Hierarchy Analysis (MANDATORY — before any layout)

<HARD-GATE>
Answer these 3 questions BEFORE placing a single component. Write answers to `figure-layout.md`. If top-level modules > 3, STOP and merge.
</HARD-GATE>

**Q1: Top-Level Modules (2–3 max)**

What are the 2–3 highest-level modules? What is their relationship?

| Relationship | Visual Treatment |
|---|---|
| Peer (parallel) | Side-by-side, equal visual weight |
| Master → Slave | Master larger/darker, slave smaller/lighter, vertical offset |
| Input → Process → Output | Left → center → right, or top → bottom |

If you have > 3 top-level modules, some of them are actually sub-modules. Merge them into a shared parent.

**Q2: Intra-Module Organization**

For EACH top-level module, what is its internal structure type?

| Semantic | Visual Structure | Example |
|---|---|---|
| Pipeline (linear stages) | Horizontal/vertical chain with flow arrows | Data processing: Ingest → Clean → Analyze |
| Tree (hierarchical branching) | Root node + branch lines + leaf nodes | Skill taxonomy: Root → Category → Rule |
| Cycle (lifecycle / loop) | Circular ring or horizontal sequence with feedback | State machine: L0→L1→L2→L0 |
| Parallel (independent co-components) | Side-by-side cards, no arrows between them | Two independent analyzers |
| Bento Grid (heterogeneous blocks) | Modular grid with varied cell sizes, unified by alignment | Figure 1 overview: architecture + workflow + examples |

**Bento Grid** is the default for comprehensive architecture overviews (Figure 1 type). The canvas is divided into an orthogonal grid where each cell holds a distinct content type (diagram, table, example, legend). Cells vary in size but align to the same grid. The hero cell spans more grid units. Whitespace between cells defines grouping.

**This mapping is mandatory.** A "box containing 3 small boxes" is NOT a valid visual structure. The internal layout must communicate the semantic relationship.

**Q2b: Gap-to-Answer Mapping (for architecture figures)**

For system architecture figures: every problem mentioned in the paper's introduction must have a visible corresponding solution module in the figure. Map explicitly:

| Paper's Stated Gap/Problem | Visual Element that Addresses It | Location in Figure |
|---|---|---|
| <Gap 1> | <Module/Arrow/Annotation> | <region> |
| <Gap 2> | <Module/Arrow/Annotation> | <region> |

If a gap has no visual answer → the figure is incomplete. If a module addresses no gap → it may be unnecessary.

**Q3: Cross-Module Connections — Arrow Budget**

Which relationships MUST be explicit arrows? Which can be implicit?

| Expression | When to use | Example |
|---|---|---|
| **Explicit arrow** | Cross-module data/control flow, bidirectional protocols | "Data upload: Client→Server" |
| **Position / proximity** | Same-module upstream→downstream | "Parser produces AST" — AST is drawn below Parser |
| **Text label / annotation** | Supplementary relationship that would clutter if drawn as arrow | "Cache eviction: LRU + TTL" as small italic text |
| **Visual grouping** | Components that belong to same function | Shared background tint or proximity |

**Arrow budget: ≤ 5 explicit cross-module arrows per figure.** If you need more, some of them should be implicit (position/proximity/text).

### 0b. Structural Decomposition (MANDATORY — before any drawing)

Hierarchy Analysis (0.) tells you WHAT the modules are. Structural Decomposition tells you HOW they relate — the structural signatures that determine visual form. This is the step where you transition from "list of boxes" thinking to "interconnected organic structure" thinking.

<HARD-GATE>
Complete ALL 4 sub-steps below BEFORE drawing a single shape. Write results to `figure-layout.md`. If you cannot describe the full mental image, do not proceed.
</HARD-GATE>

#### Step 1: Relationship Structure Extraction

Don't list modules. List RELATIONSHIPS and identify each one's structural signature.

```
For each relationship in the paper:
  Who → Who: <description of interaction>
  Structure signature: cycle | tree | pipeline | container/collector | bridge | layer | hub-spoke | ...
  Data shape (if any): What shape does the data/resource have? (tree? stream? table? set?)
```

| Structure Signature | Visual Must-Have | Real-World Analog |
|--------------------|------------------|-------------------|
| **Cycle** | Ring/circular arrangement, arrows showing closed loop direction | Water cycle, feedback loop, engine cycle |
| **Tree** | Root node + branching lines + levels of leaf nodes | Org chart, file system, phylogenetic tree |
| **Pipeline** | Sequential stages with directional flow arrows | Factory assembly line, water pipe |
| **Container/Collector** | Enclosed volume, contents visible inside or flowing in | Bucket, file cabinet, reservoir, drawer |
| **Bridge** | Two sides connected by a spanning structure with bidirectional flow | Physical bridge, network link, handshake |
| **Layer/Hierarchy** | Stacked horizontal bands, upper→lower or lower→upper | OSI stack, geological strata, building floors |
| **Hub-Spoke** | Central node with radiating connections to peripheral nodes | Wheel, star network, airport hub |
| **State Machine** | Nodes in ring/sequence with transition arrows, each node distinct | Traffic light, vending machine, life stages |

<HARD-GATE>
Each relationship MUST have an identified structure signature. A relationship without a structure signature is a relationship you don't understand yet — stop and re-read the paper.
</HARD-GATE>

#### Step 2: Nested Structure Map

Structures don't exist in isolation. They nest. The outer structure is the figure's dominant visual organization; inner structures populate each region.

Draw the nesting as an indented tree:

```
Outer structure (dominates the figure layout):
├── Region A internal structure:
│   ├── Sub-structure A1
│   └── Sub-structure A2
├── Region B internal structure:
│   └── Sub-structure B1
└── Cross-cutting structure (spans regions):
    └── ...
```

The outer structure determines the figure's overall layout (ring? left-right? top-bottom?). Inner structures determine what each region looks like inside.

#### Step 3: Physical Entity Association

For each key concept in the paper, ask: "What does this look like in the physical world?" This is NOT decoration — it's about finding visual metaphors that readers instantly recognize.

| Abstract Concept | Physical Association | How to Render in PPT |
|-----------------|---------------------|---------------------|
| Data pool / buffer | File cabinet, reservoir, drawer stack | CAN shape + horizontal divider lines |
| Skill library | Bookshelf, card catalog | Stacked cards or labeled dividers |
| Skill tree | Actual tree with branches | OVAL root → line branches → ROUNDED_RECTANGLE leaves |
| Analyzer / diagnosis | Magnifying glass, inspection desk | Distinct box with "inspect" visual emphasis |
| Communication link | Bridge, two-way road | Parallel arrows in a distinct channel |
| Lifecycle / evolution | Circular process, recycling symbol | OVAL nodes in ring + cycle arrows |
| Adapter / plugin | Physical plug, connector piece | Small box "docked" to a larger box |
| Cloud (remote) | Actual cloud shape | CLOUD MSO_SHAPE |
| Storage / database | Stacked disks, cabinet | CAN shape or stacked cylinders |
| Merge / distillation | Funnel, filter | Downward-narrowing shape or arrow |

**Rule: minimum 2 physical associations per figure.** Without them, the figure is abstract boxes. With them, the figure is a recognizable landscape.

#### Step 4: Mental Image Synthesis

Before drawing, write a paragraph describing the complete figure as if you're looking at a photograph of the final result. Don't use coordinates or PPT terminology — describe what the viewer SEES:

```
"When a reader first looks at this figure, they see...
[Describe the dominant visual element — the hero]
Around it, they see...
[Describe supporting elements, their spatial relationships, their structural forms]
The flow begins at... then moves through... and ends at...
The overall impression is of a [cycle / bridge / layered system / ...]"
```

<HARD-GATE>
If you cannot write this paragraph with confidence and clarity, your mental model of the figure is not complete. Re-read the paper section, revisit Steps 1-3.
</HARD-GATE>

### 0c. Overview Figure Design Principles (MANDATORY — before any layout)

These principles apply to ALL overview/architecture figures (Figure 1 type). They separate what an overview MUST show from what it MUST NOT.

#### What vs How Separation

An overview figure answers **WHAT** (components, connections, stages), not **HOW** (math, algorithms, formulas).

| Show in Overview (WHAT) | Defer to Technical Figures (HOW) |
|-------------------------|----------------------------------|
| Components and their roles | Internal algorithms or equations |
| Data flow between components | Mathematical derivations |
| Temporal stages (when things run) | Implementation details |
| What is preserved vs what is lost | Proof of optimality |
| Input → process → output pathways | Hyperparameter values |

**Anti-pattern**: An overview filled with formulas, matrix notation, or step-by-step algorithmic pseudocode. The reader cannot see the architecture through the math.

**Test**: If you remove all text, does the visual structure still communicate the system's organization?

#### Data Entities Must Be Visible

Every major data entity discussed in the paper must appear in the overview as a VISUAL object, not just a text label.

| Paper Discusses | Figure Must SHOW |
|----------------|------------------|
| "Key-Value caches" | Visual blocks representing KVs (selected vs unselected) |
| "Attention scores" | A connection between query and key with visible weight |
| "The prior distribution" | A distinct visual block representing the prior |
| "Sparse selection budget B" | A visual boundary showing what fits in budget |

**Anti-pattern**: Abstract boxes labeled with component names but no visual representation of the actual data that flows through them.

#### Temporal Stage Separation

If the system has distinct temporal phases (e.g., offline vs online, prefill vs decode, training vs inference), the layout MUST physically separate them.

```
[One-time Setup Phase]          [Per-step Execution Phase]
 ┌──────────────────┐            ┌──────────────────┐
 │  Precompute once  │ ──prior──→│  Reuse each step │
 └──────────────────┘            └──────────────────┘
```

**Rule**: Components that run once and components that run repeatedly belong in different visual regions, separated by a visible boundary.

**Anti-pattern**: All components in one homogenous pipeline, with "computed once" buried in a text annotation.

#### Baseline-Constrast Pattern

When the paper's contribution IMPROVES upon an existing method:

```
[Baseline: What existing methods do]  →  [Problem: What is lost/ignored]
                                              ↓
[Our Method: How we recover/compensate] → [Result: What is gained]
```

Do NOT show only the proposed method in isolation. The reader must see:
1. What the baseline does (and what it loses)
2. How the proposed method recovers the loss
3. The connection between 1 and 2

**Anti-pattern**: A figure showing only the proposed system with no visual reference to what it improves upon.

#### Data Loss/Recovery Visualization

When the core contribution is about "recovering lost information" or "estimating what was ignored":

- **Selected/kept data**: Rendered in full color, solid borders
- **Ignored/lost data**: Rendered in gray, dashed borders, or reduced opacity
- **Estimated/recovered data**: Rendered in a distinct accent color, showing it bridges the gap

**Rule**: The reader must be able to identify, at a glance, what information would have been lost AND how the method recovers it. If this distinction is not visually obvious without reading text, the figure has failed.

#### Principle Priority for Overview Figures

When designing Figure 1, apply these checks in order:

1. [ ] **Data entities visible**: Can I see the actual data objects (KVs, queries, tokens)?
2. [ ] **Time stages separated**: Can I see what runs once vs repeatedly?
3. [ ] **Baseline visible**: Can I see what the improvement is relative to?
4. [ ] **Loss/recovery shown**: If information is lost, can I see both the loss and the recovery?
5. [ ] **How-free**: If I cover all text, does the structure still make sense?
6. [ ] **Math-free**: Are there zero formulas or algorithm pseudocode in the overview?
7. [ ] **Visual-sufficiency**: For each text label, ask: "Can this be communicated purely through position, shape, color, or grouping?" If YES, remove the label. Text is for what CANNOT be shown visually. If the primary contribution is a novel STRUCTURAL ORGANIZATION, the structure itself IS the argument — labeling it diminishes impact.

### 0d. Layout Density & Visual Hierarchy (MANDATORY — before any layout)

Academic overview figures are dense, not spacious. A sparse overview reads as "not much to show."

#### Density Rule

Target content density: relevant elements should be tightly packed. Whitespace separates major conceptual groups ONLY — never pads individual elements.

| Element Relationship | Gap |
|---------------------|-----|
| Within same group | 2-4 px (tight) |
| Between adjacent groups | 8-12 px |
| Between major regions | 16-24 px |

**Anti-pattern**: Every element surrounded by equal, generous whitespace. The reader cannot tell what belongs together.

**Test**: Can you draw a bounding box around each logical group with ≤4px clearance? If a group's internal gaps are indistinguishable from inter-group gaps, the spacing is wrong.

#### Aspect Ratio Rule

Overview figures for systems papers are WIDE, not tall.

| Canvas | Recommended Aspect Ratio | Typical viewBox |
|--------|------------------------|-------------------|
| Double-column (17.8cm) | 2.5:1 to 3.5:1 | `0 0 1780 600` to `0 0 1780 750` |
| Single-column (8.9cm) | 2.0:1 to 2.8:1 | `0 0 890 350` to `0 0 890 450` |

**Anti-pattern**: A double-column overview at 1.6:1 aspect ratio (nearly square). The figure is 2× too tall for its content density.

#### Text Budget Rule

```
Title: ≤ 12 words (the paper's name is enough)
Component labels: ≤ 3 words each
Annotations: ≤ 5 words each
Body text in figure: NONE — use caption instead
```

**Anti-pattern**: A component box containing a sentence of description. If the visual structure cannot communicate the idea without a paragraph of text, the visual structure is wrong.

#### Single-Instance Baseline Rule

When using the Baseline-Contrast pattern, show the shared baseline pipeline ONCE, then branch to show the vanilla outcome vs the improved outcome. Never duplicate the entire baseline pipeline for each branch.

```
                    ┌→ [Vanilla Output (degraded)]
[Shared Baseline] ──┤
                    └→ [ + New Components] → [Improved Output]
```

**Anti-pattern**: Two identical copies of the baseline pipeline stacked vertically, doubling canvas height for no information gain.

#### Focal Point Rule

The proposed new component(s) must be visually dominant in the figure. Everything else is context.

| Element Role | Visual Treatment |
|-------------|-----------------|
| **Proposed new component** | Bold border (≥2px), accent fill, largest in its region |
| Existing pipeline (context) | Thin border (≤1px), neutral fill, standard size |
| Data entities (KV, tokens) | Small, repeated blocks — densely packed |
| Annotations | Smallest font, lightest color |

**Anti-pattern**: All components having equal visual weight. The reader cannot tell what the paper actually contributed.

**Test**: Squint. The proposed new components must pop out. If they blend into the baseline pipeline, the hierarchy is wrong.

#### Inline Legend Rule

Do NOT create a separate legend box. Waste of canvas. Instead, use consistent color coding throughout the figure where the meaning of each color is self-evident from its first use.

```
✗ BAD:  [Legend box] ■ Selected  □ Unselected  ▣ Estimated
✓ GOOD: First KV block uses blue=selected, gray=unselected. Meaning obvious from context.
```

#### Token-Level Granularity

Show individual data items (tokens, KVs, queries) as small repeated blocks, not just abstract containers labeled "KV Cache" or "Queries."

```
✗ BAD:  [KV Cache]  ← one big empty box
✓ GOOD: [k0][k1][k2][k3][k4]...  ← individual visible tokens
```

The reader should see that k0, k1, k2 are individual items being selected, attended, or ignored.

#### Overlapping Integration

Components can share visual space. The Prior Estimator can overlap the KV Cache region. The Aggregator can overlap the output region. This creates density through integration, not separation.

**Anti-pattern**: Every component in its own bounding box with generous padding. The figure reads as a wiring diagram, not an integrated system.

#### Step Progression Visibility

When the system has a per-step loop (e.g., decoding), show at least 2-3 steps visually. Not just "loops per token" text — actual step1, step2 markers with visible progression.

#### Group Density Rule

Visual density comes from GROUP NESTING DEPTH, not from cramming more individual elements. Compose related elements into hierarchical groups where each group reads as a single visual unit. A 5-element group conveys more information than 5 scattered elements, in less visual space.

```
✗ BAD: 10 scattered rectangles, equally spaced, each labeled
✓ GOOD: 3 groups containing 3-4 nested elements each, tighter internal spacing
```

**Rule**: SVG `<g>` elements should be nested at least 2 levels deep for complex structures. Flat element lists (all shapes at root level) are an anti-pattern for density.

### 1. Reading Guidance Design

Every figure MUST have a clear reading path. The reader should know where to start and how to traverse.

**Define 3 elements:**

```
Entry point:    <which component draws the eye first, and HOW?>
                (by size / color / position / annotation)
Reading path:   <top→bottom, left→right, or numbered sequence ①②③>
Traversal end:  <where does the path conclude?>
```

**Four guidance tools:**

| Tool | How | When |
|---|---|---|
| **Size** | Hero module ≥ 1.5× the area of any other module (Fitts's Law). Not "40-50% larger" — measure: hero_area / max_other_area ≥ 1.5 | Hero panel draws first attention |
| **Position** | Entry at top-left or center, follow natural reading direction | Matches left→right, top→bottom habit |
| **Color depth** | Hero = `primary_dark` — the ONLY element with saturated signal color (90/10 rule) | Darker = more important |
| **Sequence markers** | ① ② ③ or "Step 1 / Step 2" labels | Complex multi-step flows |

**Anti-patterns to avoid:**

- All modules same size → reader doesn't know what matters most → **violates Fitts's Law (need ≥1.5× area ratio)**
- Entry point at bottom-right → violates reading habit
- Core module in pale color, background in bold → inverted visual weight
- Multiple modules using `primary_dark` → violates 90/10 rule → nothing stands out
- Dense arrows forming a "spaghetti" mesh → reader cannot trace the flow

### 2. Layer Planning (MANDATORY — before any layout)

A figure is not a flat drawing. It is a stack of visual layers, each with a distinct logical role. Planning layers BEFORE placing shapes prevents the #2 cause of visual chaos (after missing hierarchy): z-order confusion where connectors obscure shapes, highlights hide behind containers, or text gets buried.

<HARD-GATE>
Define the layer stack BEFORE placing any shape. Every element you draw later must be assigned to exactly one layer.
</HARD-GATE>

#### The Standard 5-Layer Stack

From bottom (drawn first) to top (drawn last):

```
┌─────────────────────────────────────────────┐
│ L5: TEXT & ANNOTATIONS              (top)   │  Last drawn → always visible
├─────────────────────────────────────────────┤
│ L4: HIGHLIGHTS & ACCENTS                   │  Stars, badges, emphasis markers
├─────────────────────────────────────────────┤
│ L3: SUB-COMPONENTS & NODES                 │  Cards, pills, circles, icons
├─────────────────────────────────────────────┤
│ L2: MODULE CONTAINERS                      │  Main boxes, regions, panels
├─────────────────────────────────────────────┤
│ L1: CONNECTORS & ARROWS           (bottom) │  First drawn → behind everything
└─────────────────────────────────────────────┘
```

| Layer | What Goes Here | Drawn When | Must NOT Contain |
|-------|---------------|------------|------------------|
| **L1: Connectors** | All arrows, lines, connector labels | FIRST (renders behind) | Shapes, text boxes |
| **L2: Containers** | Module backgrounds, region tints, panel boxes | Second | Sub-components that should float on top |
| **L3: Sub-components** | Cards, pills, circles, icons, CAN shapes, CHEVRON steps | Third | Module-level backgrounds |
| **L4: Highlights** | Stars, gold accents, emphasis badges, numbered markers ①②③ | Fourth | Body text, labels |
| **L5: Text** | All text boxes, internal labels, annotations, titles | LAST (always on top) | Shapes, connectors |

#### Layer Assignment Rules

1. **Every element belongs to exactly one layer.** If you're unsure which layer an element belongs to, ask: "What should this be visually above, and what should it be below?"
2. **No cross-layer mixing.** Don't draw a container (L2), then a connector (L1), then a sub-component (L3). Draw ALL of L1 first, then ALL of L2, then ALL of L3.
3. **Connector labels are L1 (with their connector), not L5.** A label that describes an arrow should render at the same depth as the arrow.
4. **Region/panel backgrounds are L2.** They sit behind sub-components but in front of connectors.
5. **Hero elements span L2+L3+L4.** The hero's background is L2, its internal icons are L3, its star highlights are L4, and its text is L5. Plan these sub-layers within the hero.

#### Layer Plan Template

Before drawing, fill this out:

```
## Layer Plan: <figure-name>

### L1: Connectors & Arrows (drawn first → behind all shapes)
- Cross-module arrows: <list each with source→target>
- Internal arrows: <list>
- Connector labels: <list>

### L2: Module Containers (drawn second)
- <Module A>: position, size, fill
- <Module B>: position, size, fill
- Region backgrounds: <list>

### L3: Sub-components & Nodes (drawn third)
- <Sub-component A1>: position, size, fill
- Icons, circles, pills, CAN shapes: <list>
- CHEVRON steps: <list>

### L4: Highlights & Accents (drawn fourth)
- Stars, gold markers: <list>
- Reading path markers ①②③: <list>

### L5: Text & Annotations (drawn last → always on top)
- Module titles: <list>
- Descriptions: <list>
- Callout text: <list>
```

#### Layer Integrity Check (quick self-review before P2)

- [ ] Does every element appear in exactly one layer? (no orphans, no duplicates)
- [ ] Are all connectors in L1? (a connector in L3 would render on top of containers → bug)
- [ ] Are all text elements in L5? (text in L2 would be hidden by sub-components)
- [ ] Do L4 highlights sit above their associated L3 sub-components? (a star that should highlight a card must be drawn after the card)

### 3. Layout Design — Graphics First, Text Second

**Workflow order is critical.** The #1 cause of cluttered figures is placing text before the graphic structure is settled.

**Step A: Shape Layout (graphics only)**
Design the spatial structure considering:
- **Reading order:** top→bottom, left→right, or center-out?
- **Grouping:** which elements belong together? same layer? same function?
- **Hierarchy:** primary flow path vs secondary details
- **Proportions:** relative sizes of components (entry module larger, support smaller)
- **Shape variety plan:** Which MSO_SHAPE types will you use? List at least 3. Map each semantic concept to a shape type.

At this stage, place ONLY empty shapes (no text) and connectors. Verify the visual structure communicates the idea without a single word.

**Step B: Identify Text Gaps**
After shapes are placed, identify the whitespace gaps where text can fit:
- Which labels go INSIDE shapes? → Check shape dimensions against text length
- Which labels go ADJACENT to shapes? → Find the nearest whitespace gap
- Which labels need leader lines? → Only for crowded regions

**Step C: Place Text in Gaps**
Insert text boxes into the identified gaps. Adjust shape sizes if a label doesn't fit. The canvas should feel "filled but not crowded" — whitespace is intentional, not accidental.

**Step D: Verify Text-Shape Binding**
Check every label: is it closer to its shape than to any other shape? If a label is equidistant from two shapes → binding is ambiguous → reposition.

### 3a. Layout Pattern Library

Choose a proven layout pattern BEFORE placing components. The pattern determines the canvas partition, not the other way around.

#### Pattern 0: Baseline-Contrast (Improvement/Compensation figures)

**When**: The paper's core contribution IMPROVES an existing method, COMPENSATES for its weakness, or ADDS a new component to a known pipeline. This is the MOST COMMON pattern for systems paper overviews.

```
[Baseline Pipeline]        →    [Problem: What is lost / broken]
                                         ↓
[Proposed Method]          →    [Result: What is gained / fixed]
  (new components               (improvement metric)
   highlighted)
```

**Layout**: Two-row or two-column. Top/left = existing method and its limitation. Bottom/right = proposed solution showing how the limitation is addressed.

**Key rules**:
1. The baseline MUST be visible — do not show only the proposed method
2. New components MUST be visually distinct (accent color, bolder border, star highlight)
3. The connection between "what is lost" and "how it's recovered" must be visually explicit
4. Data entities (not just component names) must appear — if the method selects KVs, show selected vs unselected blocks

**Real-world analog**: Before/after photo — you must see both to understand the improvement.

**Anti-pattern**: Showing only the proposed system with no visual reference to what it improves. A figure labeled "Overview of X" that only shows X's internals, not X's relationship to the problem it solves.

#### Pattern 1: Three-Column Bridge (Architecture figures, system overviews)

**When**: Two systems communicate through a protocol/interaction mechanism. The figure needs to show what each side does AND how they connect.

```
[System A]  ←→  [Interaction Protocol]  ←→  [System B]
  35-40%          25-30%                    35-40%
```

**Column allocation**: Left 35%, Center 30%, Right 35% of canvas width.
**Center role**: The bridge/protocol — NOT a hero block. It explains the communication mechanism.
**Flow**: Top channel = A→B (downlink), Bottom channel = B→A (uplink).
**Key rule**: Both sides have roughly equal visual weight. The center is the connector, not the star.

**Real-world analog**: A bridge with two-way traffic lanes.

**Anti-pattern**: Center column dominates with a dark block that crushes the side columns. The reader cannot see what the side systems do.

#### Pattern 2: Pipeline (Flowcharts, data processing)

**When**: Data flows through sequential stages from input to output.

```
[Input] → [Stage 1] → [Stage 2] → [Stage 3] → [Output]
```

**Flow**: Left→right (preferred) or top→bottom.
**Key rule**: Arrows BETWEEN stages are mandatory. Boxes in a row without arrows = NOT a pipeline.

#### Pattern 3: Tree (Hierarchical structures, taxonomies)

**When**: Content has parent→child→leaf hierarchy. MUST show multiple levels clearly.

```
        [Root]           ← L0
       /  |  \
   [B1] [B2] [B3]       ← L1 (branches)
   /|\   /|\   /|\
  L L L L L L L L L     ← L2 (leaves)
```

**Key rule**: At least 3 levels visible. Root different shape from branches. Leaves different from branches. Level labels (L0/L1/L2) recommended.
**Vertical space**: Tree MUST occupy ≥ 1/3 of its column height. A tree scrunched into 1/4 of a column is not readable.
**Real-world analog**: A real tree with trunk, branches, and leaves.

#### Pattern 4: Cycle/Lifecycle (State machines, feedback loops)

**When**: States transition in a closed loop.

```
    [State A] → [State B]
        ↑           ↓
    [State D] ← [State C]
```

**Key rule**: Circular or elliptical arrangement. Arrows showing the closed loop direction. Each state visually distinct.

#### Pattern 5: Parallel Comparison (Benchmarks, ablations, before/after)

**When**: Two or more independent items compared side-by-side.

```
[Method A]  |  [Method B]  |  [Method C]
```

**Key rule**: Equal visual weight. No arrows between them (they're independent). Clear labels.

#### Pattern 6: Spatial-Transformation (Placement, topology, physical rearrangement)

**When**: The paper's core contribution is SPATIALLY rearranging things — expert placement, data sharding, topology optimization, load balancing across physical nodes. The visual argument IS the before/after spatial layout.

```
[Before: Original Placement]     [After: Optimized Placement]
 ┌────┬────┐                      ┌────┬────┐
 │ E0 │ E1 │  ←LB→  │ E2 │ E3 │   │E0 │E2 │  hiBW  │ E1 │ E3 │
 │ D0 │ D1 │        │ D2 │ D3 │   │D0 │D2 │        │ D1 │ D3 │
 └────┴────┘                      └────┴────┘
  Many cross-region links          Fewer cross-region links
```

**Key rules**:
1. Show the same entities (experts, data, GPUs) in BOTH before and after layouts
2. Color-code communication links by bandwidth/cost (red = expensive cross-DC, blue = cheap intra-DC)
3. Count and display the number of expensive links in each layout
4. The "after" layout MUST have visibly fewer red links than "before"

**Real-world analog**: Furniture rearrangement — same items, better layout, less walking.

**Anti-pattern**: Describing the rearrangement with text labels instead of showing the two spatial layouts side by side.

**Note**: This pattern is NOT Baseline-Contrast. Baseline-Contrast shows "old pipeline → new pipeline." Spatial-Transformation shows "same entities, different physical arrangement → visible reduction in costly links."

#### Pattern Selection Decision Tree

```
Paper is about SPATIAL REARRANGEMENT of entities (placement, topology, load balancing)?
  └ YES → Pattern 6 (Spatial-Transformation)
  └ NO:
    Paper IMPROVES/COMPENSATES an existing method (most systems papers)?
      └ YES → Pattern 0 (Baseline-Contrast)
      └ NO:
        Content has two communicating systems?
      └ YES → Pattern 1 (Three-Column Bridge)
      └ NO:
        Content has sequential stage-by-stage flow?
          └ YES → Pattern 2 (Pipeline)
          └ NO:
            Content has parent→child hierarchy with ≥3 levels?
              └ YES → Pattern 3 (Tree)
              └ NO:
                Content has states that transition in a loop?
                  └ YES → Pattern 4 (Cycle)
                  └ NO → Pattern 5 (Parallel) or free-form Bento Grid
```

#### Column Budget Rules

For ANY multi-column layout, declare the column widths explicitly:

```
# Canvas partition (example for 1780px wide SVG):
COL_LEFT   = {x: 30,  w: 480}   # 27% — Cloud Brain
COL_CENTER = {x: 540, w: 670}   # 38% — Protocol + Tree visualization
COL_RIGHT  = {x: 1240, w: 510}  # 29% — Edge Agent
```

Never allocate > 45% to any single column in a 3-column layout.
Center column is for interaction, not domination.

### 3b. Structure Verification (MANDATORY)

Before proceeding to P2, verify that each module's visual structure matches its semantic structure. This is the difference between "drawing boxes" and "drawing meaning."

| Semantic | Minimum Visual Requirements | FAIL Example |
|----------|---------------------------|--------------|
| **Tree** (hierarchical) | 1 root node (OVAL) + ≥2 branch lines + ≥3 leaf nodes. Branches must radiate from root. | One circle + 3 adjacent rectangles = NOT a tree |
| **Pipeline** (linear flow) | ≥3 sequential stages + arrows BETWEEN stages (not just boxes in a row) | 3 boxes with no arrows between them |
| **Cycle** (lifecycle) | ≥3 nodes in a ring/circular arrangement + arrows showing the loop direction | 4 boxes in a row labeled "L0→L1→L2→L0" |
| **Parallel** (independent) | ≥2 cards/pills side-by-side with equal visual weight, NO arrows between them | Cards with random arrows criss-crossing |
| **Bento Grid** (heterogeneous) | ≥3 distinct cell sizes, aligned to orthogonal grid, ≥2 content types | Same-size boxes in a checkerboard |

<HARD-GATE>
If any module's visual structure fails the minimum requirements, redesign BEFORE writing any text. Text cannot rescue a broken visual structure.
</HARD-GATE>

### 3. Structured Layout Plan

Write a precise, hierarchical natural-language layout spec. Format:

```
## Layout Plan: <figure-name>

### Canvas
- Width: 8.9cm (single) | 17.8cm (double)
- Orientation: top-down | left-right | grid | centered

### Panels (optional — for multi-region figures)
- Panel A (<name>): top-left (x, y), size (w, h)
  - Color: <panel background tint>
- Panel B (<name>): top-left (x, y), size (w, h)

### Spatial Structure

#### Region 1: <name> (position, size)
- [Component A] at (x, y), size (w, h) — or panel-local (x_rel, y_rel)
  - Sub-component A1 at ...
- [Component B] at (x, y), size (w, h)

#### Region 2: <name> (position, size)
...

### Connections
- A → B: arrow, label "<text>", style solid|dashed|dotted
- B → C: arrow, label "<text>"

### Notes
- Drawing order: panels → main flow arrows → component boxes → sub-components → annotations
- Alignment: grid 0.5cm
- Group boxes: rounded rect, dashed border
- Estimated total height: ~X cm
```

**Panel-local coordinates:** When a figure has distinct regions (e.g., "Server Side" and "Client Side"), declare them as panels. Components inside panels use `x_rel`, `y_rel` (0-1 normalized positions relative to panel top-left). The generator converts to absolute coordinates and validates boundaries.

```json
// In the P1 JSON spec:
{
  "panels": [
    {"name": "Server Side", "x": 0.3, "y": 0.3, "w": 8.5, "h": 2.5}
  ],
  "components": [
    {"name": "Request Handler", "panel": "Server Side", "x_rel": 0.1, "y_rel": 0.15, "w": 3.0, "h": 1.2}
  ]
}
```

This prevents the failure mode where nested elements drift when drawn in global coordinates.

Use approximate positions relative to canvas. Exact coordinates set in P2.

### 3. Rough PPT Draft

Generate a fast rough draft using `scripts/ppt-generator.sh` with `--rough` flag:
- Clone template slide
- Place blank placeholder rectangles for each component (no text yet)
- Draw basic connector lines for relationships
- Do NOT apply color/font polish

Purpose: user sees spatial proportions immediately, confirms "this is roughly right."

## Output

- `figures/<name>/figure-layout.md` — structured layout spec (narrative)
- `figures/<name>/figure-spec-lock.md` — machine-readable execution contract (YAML)
- `figures/<name>/figure-draft.pptx` — rough visual preview

### Writing the Figure Spec Lock

After the layout plan is approved, extract all numeric and semantic constants into `figure-spec-lock.md`. This is the machine-readable contract that P2 will use for code generation.

**Extraction order** (follow the template at `skills/paper-plot/figure-spec-lock.md`):

1. **Canvas**: Copy width, height, grid_snap, orientation, figure_type from layout plan
2. **Typography roles**: Fill font sizes based on column width (single: scale -1pt from paper-style-lock defaults). Inherit defaults from `paper-style-lock.md`
3. **Color roles**: Inherit from `paper-style-lock.md`. Declare any per-figure overrides explicitly
4. **Shape vocabulary**: List ≥3 MSO_SHAPE types selected for this figure, with semantic purpose
5. **Spacing constants**: Inherit from `paper-style-lock.md`. Override if needed for this figure's density
6. **Layer inventory**: Populate L1-L5 from the Layer Plan in the layout spec. Every element gets an id
7. **Groups**: From the layout plan's spatial structure, declare each group with id/layer/parent_region/structure/bbox/elements
8. **Connectors**: List all cross-module connectors with from/to/anchor/style/label
9. **Physical associations**: List ≥2 physical-world analogs
10. **Per-figure overrides**: List any values that differ from paper-style-lock.md

**Verification before proceeding to P2:**
- [ ] Every color used in the layout plan appears in color_roles
- [ ] Every font size is tied to a typography role
- [ ] ≥3 distinct shape types in shape_vocabulary
- [ ] Every element belongs to exactly one group
- [ ] Every group has a declared structure type
- [ ] All spacing values are explicit (no "automatic" or "default" gaps)

## Hard Gate

User confirms:
1. Layout spec captures all elements from P0 intent
2. Figure spec-lock is complete — all values extracted, no gaps
3. Rough PPT draft looks directionally correct
4. "Good enough to start building" — exact positions adjustable in P2

Do NOT require pixel-perfect approval. "Move X to the left" is for P2.

## Red Flags

- "Layout spec is enough, skip rough draft" → Visual intuition catches problems text misses
- "Rough draft looks fine, skip layout spec" → Spec is the authority for P2; draft is disposable
- "Let me design the layout in my head" → Write it down; unexamined layout = rework

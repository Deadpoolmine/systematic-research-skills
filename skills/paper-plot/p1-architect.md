# P1: Architect — Layout & Spatial Structure

## Role

Architect designs the spatial organization. Two outputs: a structured natural-language layout plan (authoritative spec) and a rough PPT draft (visual preview). Both from the figure-intent.

## Input

- `figures/<name>/figure-intent.md` (from P0)
- Template PPT file path
- User feedback from P0 confirmation

## Process

### 1. Layout Design

Design the spatial structure considering:

- **Reading order:** top→bottom, left→right, or center-out?
- **Grouping:** which elements belong together? same layer? same function?
- **Hierarchy:** primary flow path vs secondary details
- **Proportions:** relative sizes of components (main module larger, helper smaller)

### 2. Structured Layout Plan

Write a precise, hierarchical natural-language layout spec. Format:

```
## Layout Plan: <figure-name>

### Canvas
- Width: 8.9cm (single) | 17.8cm (double)
- Orientation: top-down | left-right | grid | centered

### Spatial Structure

#### Region 1: <name> (position, size)
- [Component A] at (x, y), size (w, h)
  - Sub-component A1 at ...
- [Component B] at (x, y), size (w, h)

#### Region 2: <name> (position, size)
...

### Connections
- A → B: arrow, label "<text>"
- B → C: arrow, label "<text>"

### Notes
- Alignment: grid 0.5cm
- Group boxes: rounded rect, dashed border
- Estimated total height: ~X cm
```

Use approximate positions relative to canvas. Exact pixel coordinates set in P2.

### 3. Rough PPT Draft

Generate a fast rough draft using `scripts/ppt-generator.sh` with `--rough` flag:
- Clone template slide
- Place blank placeholder rectangles for each component (no text yet)
- Draw basic connector lines for relationships
- Do NOT apply color/font polish

Purpose: user sees spatial proportions immediately, confirms "this is roughly right."

## Output

- `figures/<name>/figure-layout.md` — structured layout spec
- `figures/<name>/figure-draft.pptx` — rough visual preview

## Hard Gate

User confirms:
1. Layout spec captures all elements from P0 intent
2. Rough PPT draft looks directionally correct
3. "Good enough to start building" — exact positions adjustable in P2

Do NOT require pixel-perfect approval. "Move X to the left" is for P2.

## Red Flags

- "Layout spec is enough, skip rough draft" → Visual intuition catches problems text misses
- "Rough draft looks fine, skip layout spec" → Spec is the authority for P2; draft is disposable
- "Let me design the layout in my head" → Write it down; unexamined layout = rework

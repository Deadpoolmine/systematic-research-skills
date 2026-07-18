# P3: Stylist — Visual Polish, Verification & Export

## Role

Stylist applies the final visual layer: color, fonts, line styles, alignment. Then verifies structural correctness (cross-check), layout integrity (no overlap), and output robustness. This is the last gate before submission.

## Input

- `figures/<name>/figure-v{N}.pptx` (approved draft from P2)
- Existing figure files (for style consistency check)
- Paper section text (for component name cross-check)
- `figures/<name>/figure-intent.md` (for semantic verification)

## Process

### 13-Point Verification Rubric

Check and fix in order. Points 1-6 cover visual style; 7-9 cover correctness and robustness; 10-13 are final sanity checks (reviewer risk, squint test, layer integrity, cross-figure consistency).

#### 1. Color Palette

Apply consistent color scheme. Default: blue `#1565C0`. Adjust per paper theme.

| Element | Color | Usage |
|---------|-------|-------|
| Primary components | `#1565C0` (blue) | Main system modules |
| Secondary components | `#42A5F5` (light blue) | Helper modules, sub-components |
| External entities | `#78909C` (grey) | Users, external systems |
| Highlights | `#FF7043` (orange) | Attention points, bottlenecks |
| Borders | `#455A64` (dark grey) | Shape outlines |
| Connectors | `#546E7A` (grey) | Arrows, lines |
| Text | `#212121` (dark) | All labels |

If other figures exist, inspect them and match their palette. Do not use the same palette for all modules when the figure uses color to distinguish submodules — preserve semantic color grouping.

#### 2. Font

- Font family: Times New Roman (MANDATORY — verify every text run, no Arial/Calibri)
- Title: 12pt bold
- Component label: 10pt
- Annotation: 8pt
- Connector label: 8pt
- All text: auto-fit to shape, no overflow
- Vertical alignment: middle (MSO_ANCHOR.MIDDLE) for all component shapes
- Text margin: 1pt on all sides (TxtMarginLeft/Right/Top/Bottom)

Check for text overflow after font changes — if a box's text no longer fits after font substitution, either reduce font size or enlarge the box.

#### 3. Arrows & Lines

- Connector weight: 1.0pt (primary flow), 0.75pt (secondary)
- Arrow style: filled triangle end (EndArrow=4)
- Solid lines: data flow, control flow
- Dashed lines: feedback, optional paths, async communication
- Dotted lines (0.5pt): annotation pointers only
- No overlapping lines (re-route if needed)
- Arrows must not pass through unrelated component boxes

#### 4. Alignment

- Snap all shapes to 0.25cm grid
- Equal spacing between same-level components
- Center-align text within shapes (horizontally + vertically)
- Align grouped components to same baseline
- Panel/group boundary edges align to grid

#### 5. Spacing

- Minimum gap between shapes: 0.2cm
- Padding inside shapes: 0.15cm all sides
- Layer/group padding: 0.3cm inside group box
- No overlapping shapes
- Horizontal gap: 0.3cm (same layer), 0.5cm (different groups)
- Vertical gap: 0.4cm (same layer), 0.6cm (different groups)

#### 6. Width & Export

- Verify slide width: exactly 8.9cm (single) or 17.8cm (double)
- Export as PNG 300dpi using PowerPoint or python-pptx + PIL
- Single column: 8.9cm → 1051px wide
- Double column: 17.8cm → 2102px wide
- Background: white (not transparent)
- Check PNG renders correctly at 100% zoom

#### 7. Semantics — Text-Figure Cross-Check

Read the paper section that references this figure. Verify:

- Every component name in the figure appears in the text (and vice versa)
- Every acronym in the figure is defined in the text
- Arrow labels match the relationships described in text
- Every named module, caption, and important label exists as editable text (not as pasted image)
- No placeholder text ("TODO", "???", "Label") remains

<HARD-GATE>
If ANY component name mismatch found, return to P2 to fix text labels. This is a consistency requirement.
</HARD-GATE>

#### 8. Layout — Panel Bounds & Anti-Overlap

Verify spatial integrity:

- No child shape crosses outside its parent panel/group boundary
- No adjacent panels collide or overlap
- No connector arrows pass through unrelated component boxes
- Major panels are aligned to calibrated bounds with no submodule drift
- If the figure has explicit panels (from P1 panel spec), every child component stays within its declared parent panel

If overlap is detected, return to P2 to fix coordinates.

#### 9. Robustness — Backup & Verification Record

Before declaring done:

- The working `.pptx` file is saved before export (not exporting from a stale unsaved version)
- A backup of the final `.pptx` exists (git commit counts)
- Representative text labels have been spot-checked (open the file and read 3-5 random labels)
- Check that no reference/template images were left embedded in the file
- The export ran from the saved file (not from an unsaved in-memory state)

#### 10. Reviewer-Risk Preflight

Before declaring done, simulate a skeptical reviewer. Ask:

- **Minimalism:** Could the same conclusion be conveyed with fewer components or simpler structure?
- **Clarity:** Would a first-time reader understand the figure's main message within 10 seconds?
- **Redundancy:** Do any two visual elements convey the same information? If so, merge or remove one.
- **Connector routing:** Do any lines cross component boxes or labels? If so, re-route.
- **Color semantics:** Is every color choice justified by the data/structure (not decoration)?
- **Decorative elements:** Are there any dashed boxes, excessive borders, or ornamental shapes that could be replaced by whitespace and alignment?

Fix any "no" answers before final export.

#### 11. Squint Test (MANDATORY)

Step back from the screen. Squint until details blur. Verify:

- **Hero check:** The ONE element that pops out MUST be the core innovation module. If a border, gridline, or secondary module pops out instead → visual hierarchy is broken → return to P2.
- **Saturation check:** Count the saturated color blocks. You should see exactly ONE (the hero). If 2+ blocks compete → violated 90/10 color noise reduction rule → demote non-hero elements to grayscale or `primary_light`.
- **Flow check:** Can you trace the reading path (entry→flow→end) with blurred vision? The sequence should be visible from size/position alone, without reading labels.
- **Area check:** Measure the hero module area. Verify it is ≥ 1.5× the area of any other individual module (Fitts's Law).

<HARD-GATE>
If Squint Test fails, do NOT export. Return to P2 to fix visual hierarchy. This is the #1 cause of "looks cluttered, no clear hierarchy" reviewer feedback.
</HARD-GATE>

#### 12. Layer Integrity Review

The layer stack defined in P1 must be preserved in the final output. This review checks for layer violations — elements at the wrong depth, accidental occlusion, and missing inter-layer coherence.

Dispatch a review pass (can be a sub-agent or manual checklist) that checks:

**A. Layer Assignment Audit**
- [ ] Every shape on the slide is assigned to exactly one layer (L1–L5). No orphan elements.
- [ ] All connectors and lines are in L1 (drawn first, behind all shapes).
- [ ] All module backgrounds and region fills are in L2.
- [ ] All sub-components, cards, circles, and icons are in L3.
- [ ] All highlight markers (stars, badges, ①②③) are in L4.
- [ ] All text labels and annotations are in L5 (drawn last, on top of everything).

**B. Inter-Layer Occlusion Check**
- [ ] No L1 element (connector) visually obscures any L3-L5 element. If a connector crosses a shape, re-route it.
- [ ] No L2 element (container) hides an L4 highlight that should be visible on top.
- [ ] No L3 element (sub-component) covers an L5 text label.
- [ ] L4 highlights are visually above their associated L3 sub-components (a star highlighting a card must be drawn AFTER the card).

**C. Layer Merge Check**
- [ ] Are there two layers that could be one? (e.g., if L3 has only 1 element, merge it into L2 or L4)
- [ ] Are there elements in a layer that don't belong there? (e.g., a text box accidentally placed in L2)
- [ ] Is the layer count ≤ 5? If more, some layers should be merged.

**D. Global Layer Coherence**
- [ ] When all layers are mentally stacked bottom→top, does the figure read correctly?
- [ ] Does the reading path (①→②→③) flow through the layers naturally, or does it jump between depths?
- [ ] Are there "layer gaps" — a region where L2 is missing but L3 elements are present (floating sub-components without a container)?

<HARD-GATE>
If any layer violation is found, fix BEFORE export. Layer bugs are invisible in code but obvious to the eye — a connector on top of a module title, a text box hidden behind a shape, a highlight rendered below what it highlights.
</HARD-GATE>

### 13. Cross-Figure Consistency

Compare ALL figures in the paper against `figures/paper-style-lock.md`:

- [ ] **Color palette**: Same semantic colors used across all figures? (primary_dark means the same hex in every figure)
- [ ] **Font**: All Times New Roman? Same size hierarchy? (figure_title = same pt across all figures)
- [ ] **Line weights**: Same connector weights? (primary_flow = same pt across all figures)
- [ ] **Shape vocabulary**: Consistent semantic→shape mapping? (CAN always means data store, not sometimes pipeline)
- [ ] **Spacing**: Same grid snap and gap values? Same region_gap?
- [ ] **Per-figure overrides explicitly declared**: Any figure that deviates from paper-style-lock.md must list the override in its figure-spec-lock.md

If any figure is inconsistent with the paper lock, either:
- Fix the figure to match (recommended), or
- Declare the override explicitly in that figure's spec-lock (only for justified cases like single-column scaling)

Fix any "no" answers before final export.

### Text-Figure Cross-Check Detail

Read the paper section that references this figure. Verify:
- Every component name in the figure appears in the text (and vice versa)
- Every acronym in the figure is defined in the text
- Arrow labels match the relationships described in text

<HARD-GATE>
If ANY component name mismatch found, return to P2 to fix text labels. This is a consistency requirement.
</HARD-GATE>

## Output

- `figures/<name>/figure-final.pptx` — polished PPT file
- `figures/<name>/figure-final.png` — exported 300dpi PNG

## Hard Gate

All 13 rubric items MUST pass. Report result for each:

```
P3 Style Report: <figure-name>
[PASS] 1. Color palette — Nature Blue #0F4D92, consistent with Fig 2,3
[PASS] 2. Font — Times New Roman, 9/8/6.5pt hierarchy, no overflow, vertical middle
[PASS] 3. Arrows — 1pt weight, filled triangle, no crossings
[PASS] 4. Alignment — 0.25cm grid snap, equal spacing
[PASS] 5. Spacing — min 0.2cm gaps, no overlaps
[PASS] 6. Width & Export — 17.8cm verified, SVG editable text, PNG 300dpi
[PASS] 7. Semantics — all components match paper text, no placeholders
[PASS] 8. Layout — no cross-panel overlap, children within parent bounds
[PASS] 9. Robustness — saved before export, git committed, labels spot-checked
[PASS] 10. Reviewer Risk — minimal elements, 10s clarity, no redundancy, no decoration
[PASS] 11. Squint Test — hero pops first, exactly 1 saturated block, flow traceable, hero ≥ 1.5x area
[PASS] 12. Layer Integrity — L1 connectors behind, L5 text on top, no occlusion, ≤5 layers, reading path coherent across layers
[PASS] 13. Cross-Figure Consistency — colors/fonts/line-weights/shapes/spacing consistent with paper-style-lock.md
```

## Red Flags

- "The colors look fine as-is" → Check against other figures; inconsistency is visible in print
- "Alignment doesn't matter for a draft" → This IS the final; alignment matters
- "PNG export can wait" → Export now; rendering issues found later are expensive
- "The text labels are close enough" → Cross-check every label against the paper; mismatches cause reviewer confusion
- "No time to check overlap, it's probably fine" → Overlapping elements make figures unreadable; check now
- "Exporting from memory is the same as from file" → Always save first; stale exports waste rounds of review

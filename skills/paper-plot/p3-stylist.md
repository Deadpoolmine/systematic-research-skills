# P3: Stylist — Visual Polish & Consistency

## Role

Stylist applies the final visual layer: color, fonts, line styles, alignment. Also cross-checks figure-text consistency.

## Input

- `figures/<name>/figure-v{N}.pptx` (approved draft from P2)
- Existing figure files (for style consistency check)
- Paper section text (for component name cross-check)

## Process

### 6-Point Style Checklist

Each point checked and fixed in order:

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

If other figures exist, inspect them and match their palette.

#### 2. Font

- Font family: Arial (or Calibri if Arial unavailable)
- Title: 12pt bold
- Component label: 10pt
- Annotation: 8pt
- Connector label: 8pt
- All text: auto-fit to shape, no overflow

#### 3. Arrows & Lines

- Connector weight: 1.0pt
- Arrow style: open triangle, size medium
- Dashed lines: for group boundaries, optional flows
- No overlapping lines (re-route if needed)

#### 4. Alignment

- Snap all shapes to 0.25cm grid
- Equal spacing between same-level components
- Center-align text within shapes
- Align grouped components to same baseline

#### 5. Spacing

- Minimum gap between shapes: 0.2cm
- Padding inside shapes: 0.15cm all sides
- Layer/group padding: 0.3cm inside group box
- No overlapping shapes

#### 6. Width & Export

- Verify slide width: exactly 8.9cm (single) or 17.8cm (double)
- Export as PNG 300dpi using PowerPoint or python-pptx + PIL
- Check PNG renders correctly at 100% zoom

### Text-Figure Cross-Check

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

All 6 checklist items MUST pass. Report result for each:

```
P3 Style Report: <figure-name>
[PASS] 1. Color palette — blue #1565C0, consistent with Fig 2,3
[PASS] 2. Font — Arial, 10pt labels, no overflow
[PASS] 3. Arrows — 1pt weight, open triangle, no overlaps
[PASS] 4. Alignment — 0.25cm grid snap, equal spacing
[PASS] 5. Spacing — min 0.2cm gaps, no overlaps
[PASS] 6. Width — 17.8cm verified, PNG 300dpi exported
[PASS] Cross-check: all 8 components match Section 3.1 text
```

## Red Flags

- "The colors look fine as-is" → Check against other figures; inconsistency is visible in print
- "Alignment doesn't matter for a draft" → This IS the final; alignment matters
- "PNG export can wait" → Export now; rendering issues found later are expensive

# P2: Builder — PPT Generation & Component Population

## Role

Builder turns the layout spec into a real PPT file. This is the heavy-lifting layer — python-pptx generation, text population, iterative refinement.

## Input

- `figures/<name>/figure-layout.md` (from P1)
- Template PPT file (matched in P0)
- User feedback from P1 confirmation

## Process

### 1. Initial Build

Run `scripts/ppt-generator.sh` (Linux) or `scripts/ppt-generator.cmd` (Windows):

```bash
scripts/ppt-generator.sh \
  --layout figures/<name>/figure-layout.md \
  --template templates/<template-file>.pptx \
  --slide <N> \
  --output figures/<name>/figure-v1.pptx
```

The generator:
1. Clones the matched template slide as base
2. Creates shapes per layout spec (rectangles, rounded-rects, diamonds, arrows, text boxes, tables)
3. Populates text from component names and labels
4. Applies initial positioning from layout spec
5. Calculates and sets appropriate slide height (fixed width, flexible height)
6. Adjusts positions for proper spacing

### Shape Type Mapping

| Layout Element | PPT Shape Type | When to Use |
|---------------|----------------|-------------|
| Component box | `MSO_SHAPE.RECTANGLE` or `ROUNDED_RECTANGLE` | System modules, functions |
| Decision point | `MSO_SHAPE.DIAMOND` | Branching in flowcharts |
| Connector | `MSO_CONNECTOR.STRAIGHT` or `ELBOW` | Data/control flow |
| Text label | `MSO_SHAPE.TEXT_BOX` | Annotations, titles |
| Table | `ppt.table` | Comparisons, results |
| Group boundary | `MSO_SHAPE.RECTANGLE` (dashed) | Layer/group outlines |

### 2. User Review & Iteration

User opens `figure-v1.pptx` in PowerPoint/WPS → provides feedback → Builder revises:

- "Move X to position Y" → adjust shape coordinates
- "Make X bigger/smaller" → resize shape
- "Add a connector from A to B" → add arrow
- "Change text to ..." → update shape text
- "Split this into two boxes" → add shape + reconnect

Each revision: `figure-v2.pptx`, `figure-v3.pptx`, ...

### 3. Iteration Loop

```
Generate v1 → User review → Feedback → Generate v2 → ... → User approves
```

<HARD-GATE>
Do NOT exit P2 until user explicitly says "looks good" or "move to P3."
</HARD-GATE>

## Technical Notes

### python-pptx Key Operations

```python
from pptx import Presentation
from pptx.util import Inches, Cm, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR_TYPE
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn

# Clone slide dimensions from template
prs = Presentation(template_path)
slide = prs.slides[slide_index]

# Add shape
shape = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Cm(x), Cm(y), Cm(w), Cm(h)
)
shape.text = "Component Name"

# Add connector
connector = slide.shapes.add_connector(
    MSO_CONNECTOR_TYPE.STRAIGHT,
    Cm(x1), Cm(y1), Cm(x2), Cm(y2)
)

# Adjust slide height dynamically
slide_height = max(Cm(4), calculated_height)
prs.slide_height = slide_height
```

### Slide Height Calculation

Fixed width + flexible height: sum all vertical regions + gaps + margins. Minimum 4cm (template default).

## Output

- `figures/<name>/figure-v{N}.pptx` — versioned drafts until user approval

## Hard Gate

User MUST review final v{N} and confirm:
1. All P0 core elements present
2. All relationships shown
3. All text labels correct
4. Ready for P3 styling

## Red Flags

- "One version is enough" → First attempt is rarely final; budget 2-4 iterations
- "I'll add the text labels later in PowerPoint" → AI should populate text now; manual editing breaks automation
- "The layout spec was exact, why adjust?" → Visual reality differs from text spec; adjust as needed

#!/usr/bin/env bash
# ppt-slide-analyzer.sh — Analyze PPT template slides and output structure fingerprints.
# Usage: ppt-slide-analyzer.sh <template.pptx>
# Output: JSON describing each slide's shape composition, layout pattern, and figure type hints.

set -euo pipefail

TEMPLATE="${1:?Usage: ppt-slide-analyzer.sh <template.pptx>}"

if [ ! -f "$TEMPLATE" ]; then
  echo "{\"error\": \"File not found: $TEMPLATE\"}"
  exit 1
fi

python3 - "$TEMPLATE" << 'PYEOF'
import sys, json
from pptx import Presentation
from pptx.util import Inches, Emu, Cm
from pptx.enum.shapes import MSO_SHAPE_TYPE

def classify_shape(shape):
    """Map shape type to simple category."""
    t = shape.shape_type
    if t == MSO_SHAPE_TYPE.AUTO_SHAPE:
        return "auto_shape"
    elif t == MSO_SHAPE_TYPE.LINE:
        return "connector"
    elif t == MSO_SHAPE_TYPE.TEXT_BOX:
        return "text_box"
    elif t == MSO_SHAPE_TYPE.GROUP:
        return "group"
    elif t == MSO_SHAPE_TYPE.TABLE:
        return "table"
    elif t == MSO_SHAPE_TYPE.FREEFORM:
        return "freeform"
    elif t == MSO_SHAPE_TYPE.PICTURE:
        return "picture"
    elif t == MSO_SHAPE_TYPE.CHART:
        return "chart"
    else:
        return f"other({t})"

def detect_layout_pattern(shapes):
    """Heuristic: detect spatial layout pattern from shape positions."""
    if len(shapes) < 3:
        return "simple"

    # Collect centers of auto_shapes
    centers = []
    for s in shapes:
        if hasattr(s, 'left') and hasattr(s, 'top') and hasattr(s, 'width') and hasattr(s, 'height'):
            cx = s.left + s.width // 2
            cy = s.top + s.height // 2
            centers.append((cx, cy, s.width, s.height))

    if len(centers) < 3:
        return "simple"

    # Check if shapes are arranged in horizontal rows
    y_values = sorted(set(cy for _, cy, _, _ in centers))
    y_clusters = []
    for y in y_values:
        cluster = [c for c in centers if abs(c[1] - y) < Emu(500000)]
        if len(cluster) >= 2:
            y_clusters.append(y)

    # Check if shapes are arranged in vertical columns
    x_values = sorted(set(cx for cx, _, _, _ in centers))
    x_clusters = []
    for x in x_values:
        cluster = [c for c in centers if abs(c[0] - x) < Emu(500000)]
        if len(cluster) >= 2:
            x_clusters.append(x)

    n_arrows = sum(1 for s in shapes if s.shape_type == MSO_SHAPE_TYPE.LINE)
    n_tables = sum(1 for s in shapes if s.shape_type == MSO_SHAPE_TYPE.TABLE)
    n_groups = sum(1 for s in shapes if s.shape_type == MSO_SHAPE_TYPE.GROUP)

    # Pattern detection
    if n_tables >= 2:
        return "table-grid"
    if len(y_clusters) >= 3 and n_arrows >= 5:
        return "top-down-flow"
    if len(x_clusters) >= 3 and n_arrows >= 3:
        return "left-right-flow"
    if len(y_clusters) >= 2 and n_arrows >= 3:
        return "layered-architecture"
    if n_groups >= 2:
        return "multi-group"
    if n_arrows >= 10:
        return "complex-flowchart"

    return "free-layout"

def guess_figure_type(shapes, pattern):
    """Guess figure type from shapes and layout pattern."""
    counts = {}
    for s in shapes:
        cat = classify_shape(s)
        counts[cat] = counts.get(cat, 0) + 1

    n_auto = counts.get('auto_shape', 0)
    n_conn = counts.get('connector', 0)
    n_tables = counts.get('table', 0)
    n_text = counts.get('text_box', 0)
    n_groups = counts.get('group', 0)

    if n_tables >= 3:
        return "comparison"
    if n_conn >= 8 and n_auto >= 10:
        return "flowchart"
    if n_auto >= 8 and n_conn >= 3 and pattern in ("layered-architecture", "top-down-flow"):
        return "architecture"
    if n_groups >= 2 and n_auto <= 15:
        return "concept"
    if n_auto >= 15 and n_conn >= 5:
        return "architecture"
    if n_auto <= 5:
        return "concept"

    return "architecture"

def main():
    template_path = sys.argv[1]
    prs = Presentation(template_path)

    slide_width_cm = prs.slide_width / 360000  # EMU to cm approximate
    slide_height_cm = prs.slide_height / 360000

    slides_info = []
    for i, slide in enumerate(prs.slides):
        shapes_info = []
        for s in slide.shapes:
            shape_data = {
                "name": s.name,
                "type": classify_shape(s),
            }
            if hasattr(s, 'left'):
                shape_data["x_cm"] = round(s.left / 360000, 1)
                shape_data["y_cm"] = round(s.top / 360000, 1)
                shape_data["w_cm"] = round(s.width / 360000, 1)
                shape_data["h_cm"] = round(s.height / 360000, 1)
            if s.has_text_frame:
                txt = s.text_frame.text.strip()
                if txt:
                    shape_data["text"] = txt[:60]
            shapes_info.append(shape_data)

        pattern = detect_layout_pattern(list(slide.shapes))
        fig_type = guess_figure_type(list(slide.shapes), pattern)

        slides_info.append({
            "index": i + 1,
            "shape_count": len(slide.shapes),
            "layout_pattern": pattern,
            "guessed_type": fig_type,
            "shapes": shapes_info,
        })

    output = {
        "file": template_path,
        "slide_width_cm": round(slide_width_cm, 1),
        "slide_height_cm": round(slide_height_cm, 1),
        "column_type": "single" if slide_width_cm < 12 else "double",
        "slide_count": len(slides_info),
        "slides": slides_info,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
PYEOF

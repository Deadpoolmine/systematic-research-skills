#!/usr/bin/env bash
# ppt-generator.sh — Generate PPT figure from JSON spec.
# Usage: ppt-generator.sh --spec <spec.json> --output <output.pptx>
#        [--rough] [--polish] [--style <style.json>]
# Modes:
#   Default (P2): Full generation with text, shapes, connectors
#   --rough (P1): Placeholder shapes only, no text fill
#   --polish (P3): Apply style guide to existing PPT

set -euo pipefail

SPEC_FILE=""
OUTPUT_FILE=""
MODE="full"
STYLE_FILE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --spec) SPEC_FILE="$2"; shift 2 ;;
        --output) OUTPUT_FILE="$2"; shift 2 ;;
        --rough) MODE="rough"; shift ;;
        --polish) MODE="polish"; shift ;;
        --style) STYLE_FILE="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ "$MODE" != "polish" ]; then
    if [ -z "$SPEC_FILE" ] || [ -z "$OUTPUT_FILE" ]; then
        echo "Usage: ppt-generator.sh --spec <spec.json> --output <output.pptx> [--rough] [--polish]"
        exit 1
    fi
    if [ ! -f "$SPEC_FILE" ]; then
        echo "{\"error\": \"Spec file not found: $SPEC_FILE\"}"
        exit 1
    fi
fi

if [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: ppt-generator.sh --output is required"
    exit 1
fi

python3 - "$SPEC_FILE" "$OUTPUT_FILE" "$MODE" "${STYLE_FILE:-}" << 'PYEOF'
import sys, json, copy
from pptx import Presentation
from pptx.util import Inches, Cm, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR_TYPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from copy import deepcopy

# ── Style defaults ──────────────────────────────────────────────
DEFAULT_STYLE = {
    "colors": {
        "primary": "1565C0", "secondary": "42A5F5", "tertiary": "90CAF9",
        "external": "78909C", "highlight": "FF7043", "success": "66BB6A",
        "border": "455A64", "border_internal": "78909C",
        "text": "212121", "text_secondary": "616161",
        "connector": "546E7A", "connector_dashed": "78909C",
        "connector_dotted": "9E9E9E", "background": "FFFFFF"
    },
    "fonts": {
        "family": "Arial",
        "title_size": 12, "label_size": 10, "sublabel_size": 8,
        "annotation_size": 7
    },
    "connector_weight": 1.0,          # pt, primary data flow
    "connector_weight_control": 0.75, # pt, control flow
    "connector_weight_dashed": 0.5,   # pt, optional/feedback
    "connector_arrow": "triangle",
    "border_weight": 1.0,             # pt, primary component outlines
    "border_weight_internal": 0.5,    # pt, sub-component outlines
    "corner_radius": 0.2,             # cm, rounded rectangle default
    "grid_snap": 0.25,   # cm
    "min_gap": 0.2,       # cm
    "padding": 0.15,      # cm, inside shapes
    "group_padding": 0.3, # cm
    "page_margin": 0.3,   # cm
    "text_margin_pt": 1,  # pt, TxtMargin on all sides
}

def load_style(style_path):
    if style_path and style_path != "":
        try:
            with open(style_path) as f:
                return {**DEFAULT_STYLE, **json.load(f)}
        except:
            return DEFAULT_STYLE
    return DEFAULT_STYLE

def hex_to_rgb(hex_str):
    h = hex_str.lstrip('#')
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def get_shape_type(name):
    mapping = {
        "rectangle": MSO_SHAPE.RECTANGLE,
        "rounded_rect": MSO_SHAPE.ROUNDED_RECTANGLE,
        "rounded_rectangle": MSO_SHAPE.ROUNDED_RECTANGLE,
        "diamond": MSO_SHAPE.DIAMOND,
        "cylinder": MSO_SHAPE.CAN,
        "can": MSO_SHAPE.CAN,
    }
    return mapping.get(name.lower(), MSO_SHAPE.RECTANGLE)

def apply_style_to_shape(shape, style, role="primary"):
    """Apply color, font, border from style to shape."""
    colors = style["colors"]
    fonts = style["fonts"]

    color_map = {
        "primary": colors["primary"],
        "secondary": colors["secondary"],
        "tertiary": colors["tertiary"],
        "external": colors["external"],
        "highlight": colors["highlight"],
        "success": colors["success"],
    }
    fill_hex = color_map.get(role, colors["primary"])

    # Fill
    shape.fill.solid()
    shape.fill.fore_color.rgb = hex_to_rgb(fill_hex)

    # Border — internal vs main
    is_internal = role in ("tertiary",)
    border_hex = colors.get("border_internal", colors["border"]) if is_internal else colors["border"]
    border_weight = style.get("border_weight_internal", 0.5) if is_internal else style.get("border_weight", 1.0)
    shape.line.color.rgb = hex_to_rgb(border_hex)
    shape.line.width = Pt(border_weight)

    # Corner radius for rounded rectangles
    corner_radius = style.get("corner_radius", 0.2)
    if shape.shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            shape.adjustments[0] = corner_radius / 2.0  # approximation
        except:
            pass

    # Text
    if shape.has_text_frame:
        tf = shape.text_frame
        tf.word_wrap = True
        # Vertical alignment: middle
        try:
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        except:
            pass
        try:
            from pptx.oxml.ns import qn
            txBody = shape._element.txBody
            bodyPr = txBody.find(qn('a:bodyPr'))
            if bodyPr is not None:
                bodyPr.set('anchor', 'ctr')  # middle
        except:
            pass
        for para in tf.paragraphs:
            para.alignment = PP_ALIGN.CENTER
            for run in para.runs:
                run.font.name = fonts["family"]
                run.font.size = Pt(fonts["label_size"])
                run.font.color.rgb = hex_to_rgb(colors["text"])

def snap_to_grid(value_cm, grid_cm):
    """Snap a cm value to nearest grid line."""
    return round(value_cm / grid_cm) * grid_cm

def clean_slide(slide):
    """Remove ALL existing shapes from a slide. Called first before adding new ones."""
    shapes_elements = list(slide.shapes)
    for shape in shapes_elements:
        sp = shape._element
        sp.getparent().remove(sp)

def reorder_connectors_behind(slide):
    """Move all connector lines (cxnSp) to the back of z-order so shapes render on top.
    Connectors obscuring component boxes or text is a critical visual bug."""
    from pptx.oxml.ns import qn
    spTree = slide._element.find(qn('p:cSld')).find(qn('p:spTree'))
    if spTree is None:
        return
    children = list(spTree)
    # Collect connector elements
    cxn_elements = []
    for child in children:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag == 'cxnSp':
            cxn_elements.append(child)
    # Remove and re-insert at the beginning (behind all shapes)
    for elem in cxn_elements:
        spTree.remove(elem)
    # Insert after the first non-connector element (typically a group shape or sp)
    first_idx = 0
    for i, child in enumerate(list(spTree)):
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag != 'cxnSp':
            first_idx = i
            break
    for elem in reversed(cxn_elements):
        spTree.insert(first_idx, elem)

def generate_ppt(spec_path, output_path, mode, style):
    with open(spec_path) as f:
        spec = json.load(f)

    template_path = spec.get("template")
    slide_index = spec.get("slide_index", 0)  # 0-based
    slide_width_cm = spec.get("width_cm", 17.8)
    components = spec.get("components", [])
    connectors = spec.get("connectors", [])
    groups = spec.get("groups", [])
    panels = spec.get("panels", [])  # NEW: panel abstraction

    # Build panel lookup
    panel_map = {}  # name → {x_cm, y_cm, w_cm, h_cm}
    for panel in panels:
        panel_map[panel["name"]] = {
            "x": panel.get("x", 0),
            "y": panel.get("y", 0),
            "w": panel.get("w", slide_width_cm),
            "h": panel.get("h", 4.0),
            "color": panel.get("color", "panel_bg"),
            "label": panel.get("label", panel["name"]),
        }

    # Validate: all panel-referenced components have valid panel names
    for comp in components:
        if "panel" in comp:
            pname = comp["panel"]
            if pname not in panel_map:
                raise ValueError(f"Component '{comp['name']}' references unknown panel '{pname}'. Known panels: {list(panel_map.keys())}")

    # Load or create presentation
    if template_path and mode != "polish":
        prs = Presentation(template_path)
        # Clone the target slide: use its layout but start clean
        target_slide = prs.slides[slide_index]
        slide_layout = target_slide.slide_layout
        # CRITICAL: remove ALL template artifacts before adding our shapes
        clean_slide(target_slide)
        slide = target_slide
    else:
        prs = Presentation()
        # Set custom slide size
        prs.slide_width = Cm(slide_width_cm)
        prs.slide_height = Cm(4.0)  # initial, will adjust
        slide_layout = prs.slide_layouts[6]  # blank
        slide = prs.slides.add_slide(slide_layout)

    # Calculate content area
    margin = Cm(style["page_margin"])
    content_w = Cm(slide_width_cm) - 2 * margin
    usable_w_cm = slide_width_cm - 2 * style["page_margin"]

    created_shapes = {}  # name → shape reference
    component_panels = {}  # name → panel_name for overlap checking

    # ── Draw panel backgrounds first ──────────────────────────
    for panel in panels:
        pname = panel["name"]
        px = Cm(panel_map[pname]["x"])
        py = Cm(panel_map[pname]["y"])
        pw = Cm(panel_map[pname]["w"])
        ph = Cm(panel_map[pname]["h"])
        pcolor = panel.get("fill", "F5F7FA")  # very light background

        panel_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, py, pw, ph)
        panel_shape.name = f"panel_{pname}"
        panel_shape.fill.solid()
        panel_shape.fill.fore_color.rgb = hex_to_rgb(pcolor)
        panel_shape.line.color.rgb = hex_to_rgb(style["colors"]["border"])
        panel_shape.line.width = Pt(0.5)
        panel_shape.line.dash_style = 2  # dash

        # Panel label at top-left inside
        tb = slide.shapes.add_textbox(px + Cm(0.1), py + Cm(0.05), Cm(4), Cm(0.5))
        p = tb.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = panel_map[pname]["label"]
        run.font.name = style["fonts"]["family"]
        run.font.size = Pt(style["fonts"]["sublabel_size"])
        run.font.color.rgb = hex_to_rgb(style["colors"]["text_secondary"])
        run.font.italic = True

    # ── Create components ──────────────────────────────────────
    for comp in components:
        name = comp["name"]
        shape_type = comp.get("shape", "rounded_rect")
        role = comp.get("role", "primary")
        text = comp.get("text", name)
        sub_text = comp.get("subtext", "")

        # Panel-local coordinates: if "panel" specified, use x_rel/y_rel
        if "panel" in comp:
            pname = comp["panel"]
            pinfo = panel_map[pname]
            px0 = pinfo["x"]
            py0 = pinfo["y"]
            pw = pinfo["w"]
            ph = pinfo["h"]
            x_rel = comp.get("x_rel", 0)
            y_rel = comp.get("y_rel", 0)
            # Absolute position from relative coordinates
            x_cm = px0 + x_rel * pw
            y_cm = py0 + y_rel * ph
            component_panels[name] = pname
        else:
            x_cm = comp.get("x", 0)
            y_cm = comp.get("y", 0)
        w_cm = comp.get("w", 2)
        h_cm = comp.get("h", 1)

        x = Cm(x_cm)
        y = Cm(y_cm)
        w = Cm(w_cm)
        h = Cm(h_cm)

        ppt_shape_type = get_shape_type(shape_type)
        shape = slide.shapes.add_shape(ppt_shape_type, x, y, w, h)
        shape.name = name

        if mode == "rough":
            # P1: placeholder only — light grey fill, no text
            shape.fill.solid()
            shape.fill.fore_color.rgb = hex_to_rgb("E0E0E0")
            shape.line.color.rgb = hex_to_rgb("BDBDBD")
            shape.line.width = Pt(0.5)
        else:
            # P2: full generation
            apply_style_to_shape(shape, style, role)
            if shape.has_text_frame:
                tf = shape.text_frame
                tf.clear()
                tf.word_wrap = True
                # Main text
                p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                run = p.add_run()
                run.text = text
                run.font.name = style["fonts"]["family"]
                run.font.size = Pt(style["fonts"]["label_size"])
                run.font.color.rgb = hex_to_rgb(style["colors"]["text"])
                run.font.bold = True
                # Sub text
                if sub_text:
                    p2 = tf.add_paragraph()
                    p2.alignment = PP_ALIGN.CENTER
                    run2 = p2.add_run()
                    run2.text = sub_text
                    run2.font.name = style["fonts"]["family"]
                    run2.font.size = Pt(style["fonts"]["sublabel_size"])
                    run2.font.color.rgb = hex_to_rgb(style["colors"]["text_secondary"])
                    run2.font.bold = False

        created_shapes[name] = shape

    # ── Create connectors ──────────────────────────────────────
    for conn in connectors:
        from_name = conn["from"]
        to_name = conn["to"]
        label = conn.get("label", "")
        conn_type = conn.get("type", "straight")

        if from_name in created_shapes and to_name in created_shapes:
            s1 = created_shapes[from_name]
            s2 = created_shapes[to_name]

            # Calculate connection points (center-bottom to center-top by default)
            x1 = s1.left + s1.width // 2
            y1 = s1.top + s1.height
            x2 = s2.left + s2.width // 2
            y2 = s2.top

            connector_type = MSO_CONNECTOR_TYPE.STRAIGHT if conn_type == "straight" else MSO_CONNECTOR_TYPE.ELBOW
            connector = slide.shapes.add_connector(connector_type, x1, y1, x2, y2)

            if mode == "rough":
                connector.line.color.rgb = hex_to_rgb("BDBDBD")
                connector.line.width = Pt(0.5)
            else:
                connector.line.color.rgb = hex_to_rgb(style["colors"]["connector"])
                connector.line.width = Pt(style["connector_weight"])
                # Arrow head
                try:
                    connector.end_xml  # access to check existence
                except:
                    pass

            # Connector label (text box near midpoint)
            if label and mode != "rough":
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                tb = slide.shapes.add_textbox(mid_x - Cm(1.5), mid_y - Cm(0.4), Cm(3), Cm(0.6))
                tb.text_frame.word_wrap = True
                p = tb.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                run = p.add_run()
                run.text = label
                run.font.name = style["fonts"]["family"]
                run.font.size = Pt(style["fonts"]["sublabel_size"])
                run.font.color.rgb = hex_to_rgb(style["colors"]["connector"])

    # ── Create group boundaries ────────────────────────────────
    for group in groups:
        gname = group["name"]
        members = group.get("members", [])

        if len(members) >= 1 and all(m in created_shapes for m in members):
            shapes_in_group = [created_shapes[m] for m in members]
            # Compute bounding box
            padding_emu = Cm(style["group_padding"])
            min_x = min(s.left for s in shapes_in_group) - padding_emu
            min_y = min(s.top for s in shapes_in_group) - padding_emu
            max_x = max(s.left + s.width for s in shapes_in_group) + padding_emu
            max_y = max(s.top + s.height for s in shapes_in_group) + padding_emu

            gx = min_x
            gy = min_y
            gw = max_x - min_x
            gh = max_y - min_y

            group_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, gx, gy, gw, gh)
            group_shape.name = f"group_{gname}"
            group_shape.fill.background()  # transparent
            group_shape.line.color.rgb = hex_to_rgb(style["colors"]["border"])
            group_shape.line.width = Pt(0.5)
            group_shape.line.dash_style = 2  # dash

            # Group label at top-left inside
            tb = slide.shapes.add_textbox(gx + Cm(0.1), gy + Cm(0.05), Cm(4), Cm(0.5))
            p = tb.text_frame.paragraphs[0]
            run = p.add_run()
            run.text = gname
            run.font.name = style["fonts"]["family"]
            run.font.size = Pt(style["fonts"]["sublabel_size"])
            run.font.color.rgb = hex_to_rgb(style["colors"]["text_secondary"])
            run.font.italic = True

    # ── Z-order: connectors behind shapes ────────────────────
    reorder_connectors_behind(slide)

    # ── Anti-Overlap Verification ─────────────────────────────
    overlap_errors = []

    # Check 1: children stay within parent panels
    for name, pname in component_panels.items():
        if name not in created_shapes:
            continue
        shape = created_shapes[name]
        pinfo = panel_map[pname]
        px0 = Cm(pinfo["x"])
        py0 = Cm(pinfo["y"])
        px1 = px0 + Cm(pinfo["w"])
        py1 = py0 + Cm(pinfo["h"])

        sx0 = shape.left
        sy0 = shape.top
        sx1 = shape.left + shape.width
        sy1 = shape.top + shape.height

        if sx0 < px0 or sy0 < py0 or sx1 > px1 or sy1 > py1:
            overlap_errors.append(
                f"OVERLAP: '{name}' extends outside panel '{pname}'. "
                f"Shape bounds ({shape.left/360000:.2f},{shape.top/360000:.2f})-"
                f"({(shape.left+shape.width)/360000:.2f},{(shape.top+shape.height)/360000:.2f}) cm "
                f"exceed panel ({pinfo['x']},{pinfo['y']})-({pinfo['x']+pinfo['w']},{pinfo['y']+pinfo['h']}) cm"
            )

    # Check 2: panels don't collide
    panel_list = list(panel_map.items())
    for i in range(len(panel_list)):
        for j in range(i + 1, len(panel_list)):
            a_name, a = panel_list[i]
            b_name, b = panel_list[j]
            ax0, ay0 = a["x"], a["y"]
            ax1, ay1 = a["x"] + a["w"], a["y"] + a["h"]
            bx0, by0 = b["x"], b["y"]
            bx1, by1 = b["x"] + b["w"], b["y"] + b["h"]
            if ax0 < bx1 and ax1 > bx0 and ay0 < by1 and ay1 > by0:
                overlap_errors.append(
                    f"PANEL COLLISION: '{a_name}' and '{b_name}' overlap. "
                    f"Panel A ({ax0},{ay0})-({ax1},{ay1}), Panel B ({bx0},{by0})-({bx1},{by1})"
                )

    if overlap_errors:
        for err in overlap_errors:
            print(f"WARNING: {err}")
        print(f"ANTI-OVERLAP: {len(overlap_errors)} violation(s) found.")
        raise RuntimeError(f"Overlap check failed with {len(overlap_errors)} violation(s). Fix component/panel coordinates before proceeding to P3.")

    # ── Adjust slide height ────────────────────────────────────
    if components:
        max_bottom = max(
            (created_shapes[c["name"]].top + created_shapes[c["name"]].height)
            for c in components if c["name"] in created_shapes
        )
        new_height = max_bottom + Cm(style["page_margin"])
        if new_height > prs.slide_height:
            prs.slide_height = new_height

    # ── Remove unused template slides ──────────────────────────
    # Keep only the target slide; delete all others
    sldIdLst = prs.slides._sldIdLst
    entries = list(sldIdLst)
    for idx, entry in enumerate(entries):
        if idx != slide_index:
            sldIdLst.remove(entry)

    # ── Save ────────────────────────────────────────────────────
    prs.save(output_path)

    # ── Report ──────────────────────────────────────────────────
    result = {
        "output": output_path,
        "mode": mode,
        "components": len(components),
        "connectors": len(connectors),
        "groups": len(groups),
        "panels": len(panels),
        "panel_children": len(component_panels),
        "overlap_check": "passed",
        "slide_width_cm": slide_width_cm,
        "slide_height_cm": round(prs.slide_height / 360000, 1),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

def polish_ppt(output_path, style):
    """P3: Polish existing PPT — apply style guide to all shapes."""
    prs = Presentation(output_path)

    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, 'fill') and shape.has_text_frame:
                # Check if it's a primary component (has bold text)
                tf = shape.text_frame
                if tf.paragraphs and tf.paragraphs[0].runs:
                    run = tf.paragraphs[0].runs[0]
                    if run.font.bold:
                        apply_style_to_shape(shape, style, "primary")
                    else:
                        apply_style_to_shape(shape, style, "secondary")

    prs.save(output_path)
    print(json.dumps({"polished": output_path, "status": "ok"}, indent=2))

# ── Main ───────────────────────────────────────────────────────
spec_path = sys.argv[1]
output_path = sys.argv[2]
mode = sys.argv[3]
style_path = sys.argv[4] if len(sys.argv) > 4 else ""

style = load_style(style_path)

if mode == "polish":
    # P3: Polish mode — input is the PPT itself, not a spec
    polish_ppt(output_path, style)
else:
    # P1 (rough) or P2 (full)
    # Output path for polish: spec_path is actually input PPT
    generate_ppt(spec_path, output_path, mode, style)
PYEOF

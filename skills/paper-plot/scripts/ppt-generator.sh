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
        "border": "455A64", "text": "212121", "text_secondary": "616161",
        "connector": "546E7A", "background": "FFFFFF"
    },
    "fonts": {
        "family": "Arial",
        "title_size": 12, "label_size": 10, "sublabel_size": 8,
        "annotation_size": 7
    },
    "connector_weight": 1.0,
    "connector_arrow": "triangle",
    "grid_snap": 0.25,   # cm
    "min_gap": 0.2,       # cm
    "padding": 0.15,      # cm
    "group_padding": 0.3, # cm
    "page_margin": 0.3,   # cm
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

    # Border
    shape.line.color.rgb = hex_to_rgb(colors["border"])
    shape.line.width = Pt(1.0)

    # Text
    if shape.has_text_frame:
        tf = shape.text_frame
        tf.word_wrap = True
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

def generate_ppt(spec_path, output_path, mode, style):
    with open(spec_path) as f:
        spec = json.load(f)

    template_path = spec.get("template")
    slide_index = spec.get("slide_index", 0)  # 0-based
    slide_width_cm = spec.get("width_cm", 17.8)
    components = spec.get("components", [])
    connectors = spec.get("connectors", [])
    groups = spec.get("groups", [])

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

    # ── Create components ──────────────────────────────────────
    for comp in components:
        name = comp["name"]
        x = Cm(comp.get("x", 0))
        y = Cm(comp.get("y", 0))
        w = Cm(comp.get("w", 2))
        h = Cm(comp.get("h", 1))
        shape_type = comp.get("shape", "rounded_rect")
        role = comp.get("role", "primary")
        text = comp.get("text", name)
        sub_text = comp.get("subtext", "")

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

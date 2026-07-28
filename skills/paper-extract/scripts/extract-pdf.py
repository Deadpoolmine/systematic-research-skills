#!/usr/bin/env python3
"""
PDF Paper Extractor — extract structured text AND figure images from academic PDFs.

Usage:
    python extract-pdf.py <paper.pdf> [--output <dir>]
    
Output directory structure:
    <output>/
      analysis/
        full-text.md        Complete extracted text with section markers
        figures.md           Figure/table captions with page numbers and context
        figures/             Extracted figure images (PNG, one per figure)
          fig-01.png
          fig-02.png
          ...
        references.md        Reference list
        metadata.json        Title, authors, abstract
      results/               (created empty, ready for E1 output)

Dependencies: PyPDF2, pdfplumber, Pillow (install via pip)
"""

import sys
import os
import json
import re
from pathlib import Path


def extract_with_pdfplumber(pdf_path: str, output_base: str) -> dict:
    """Extract text and figure images using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        return None
    
    figures = []
    references = []
    metadata = {"title": "", "authors": [], "abstract": ""}
    page_texts = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        full_text = []
        
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                page_texts[i] = text
                full_text.append(f"<!-- PAGE {i+1} -->\n{text}")
        
        raw = "\n\n".join(full_text)
    
    # Try to detect title
    lines = raw.split("\n")
    title_candidates = [l.strip() for l in lines[:20] if len(l.strip()) > 20 and not l.startswith("<!--")]
    if title_candidates:
        metadata["title"] = title_candidates[0]
    
    # Detect abstract
    abs_match = re.search(
        r'(?:Abstract|ABSTRACT)[\s—-]*\n?(.{200,2000}?)(?:\n\s*(?:\d+\.?\s+)?(?:Introduction|1\.|I\.))',
        raw, re.DOTALL | re.IGNORECASE
    )
    if abs_match:
        metadata["abstract"] = abs_match.group(1).strip()
    
    # ---- FIGURE EXTRACTION (text + image) ----
    fig_pattern = re.compile(
        r'(?:Figure|Fig\.)\s*(\d+)[.:]?\s*(.+?)(?=\n(?:Figure|Fig\.)\s*\d+|\n\s*(?:\d+\.?\s+)?(?:Table|$))',
        re.DOTALL | re.IGNORECASE
    )
    
    for match in fig_pattern.finditer(raw):
        fig_num = match.group(1)
        caption = match.group(2).strip()
        
        # Find which page this figure caption appears on
        page_num = None
        cap_start = match.start()
        for pg, text in page_texts.items():
            pg_start = raw.find(f"<!-- PAGE {pg+1} -->")
            pg_end = raw.find(f"<!-- PAGE {pg+2} -->") if pg + 1 < total_pages else len(raw)
            if pg_start <= cap_start < pg_end:
                page_num = pg + 1
                break
        
        # Extract surrounding context (2-3 paragraphs around the caption)
        cap_pos = match.start()
        context_start = max(0, raw.rfind('\n\n', 0, cap_pos - 100))
        context_end = raw.find('\n\n', cap_pos + len(match.group()))
        if context_end == -1:
            context_end = min(len(raw), cap_pos + 2000)
        surrounding = raw[context_start:context_end].strip()
        
        figures.append({
            "number": fig_num,
            "caption": caption,
            "page": page_num,
            "type": "figure",
            "context": surrounding[:1500]
        })
    
    # Table captions
    tab_pattern = re.compile(
        r'(?:Table)\s*(\d+)[.:]?\s*(.+?)(?=\n(?:Figure|Fig\.|Table)\s*\d+|\n\s*(?:\d+\.?\s+)?(?:Section|$))',
        re.DOTALL | re.IGNORECASE
    )
    for match in tab_pattern.finditer(raw):
        tab_num = match.group(1)
        caption = match.group(2).strip()
        
        page_num = None
        cap_start = match.start()
        for pg, text in page_texts.items():
            pg_start = raw.find(f"<!-- PAGE {pg+1} -->")
            pg_end = raw.find(f"<!-- PAGE {pg+2} -->") if pg + 1 < total_pages else len(raw)
            if pg_start <= cap_start < pg_end:
                page_num = pg + 1
                break
        
        figures.append({
            "number": tab_num,
            "caption": caption,
            "page": page_num,
            "type": "table",
            "context": ""
        })
    
    # Extract references
    ref_match = re.search(r'(?:References|REFERENCES|Bibliography)\s*\n(.*?)$', raw, re.DOTALL | re.IGNORECASE)
    if ref_match:
        ref_text = ref_match.group(1)
        ref_items = re.split(r'\n(?=\[\d+\])', ref_text)
        references = [r.strip() for r in ref_items if r.strip()]
    
    # ---- Extract figure images from pages ----
    _extract_figure_images(pdf_path, figures, output_base)
    
    return {
        "raw": raw,
        "metadata": metadata,
        "figures": figures,
        "references": references,
    }


def _extract_figure_images(pdf_path: str, figures: list, output_base: str):
    """Extract figure images by rendering pages as high-res images."""
    try:
        from PIL import Image
        import pdfplumber
    except ImportError:
        print("[E0] WARN: Pillow not available — skipping figure image extraction.")
        print("     Install: pip install Pillow")
        return
    
    figures_dir = os.path.join(output_base, "analysis", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    # Group figures by page
    page_figs = {}
    for fig in figures:
        if fig.get("page") and fig["type"] == "figure":
            pg = fig["page"]
            if pg not in page_figs:
                page_figs[pg] = []
            page_figs[pg].append(fig)
    
    if not page_figs:
        print("[E0] No figure captions detected on known pages — skipping image extraction.")
        return
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, figs_on_page in page_figs.items():
                page_idx = page_num - 1
                if page_idx >= len(pdf.pages):
                    continue
                
                page = pdf.pages[page_idx]
                page_img = page.to_image(resolution=200)
                pil_img = page_img.original
                
                for fig in figs_on_page:
                    fig_num = fig["number"]
                    out_path = os.path.join(figures_dir, f"fig-{fig_num.zfill(2)}.png")
                    
                    if len(figs_on_page) == 1:
                        pil_img.save(out_path, "PNG")
                    else:
                        idx = figs_on_page.index(fig)
                        total = len(figs_on_page)
                        crop_height = pil_img.height // total
                        top = idx * crop_height
                        bottom = (idx + 1) * crop_height if idx < total - 1 else pil_img.height
                        cropped = pil_img.crop((0, top, pil_img.width, bottom))
                        cropped.save(out_path, "PNG")
                    
                    fig["image_path"] = f"figures/fig-{fig_num.zfill(2)}.png"
                
                pil_img.close()
        
        count = sum(1 for f in figures if f.get("image_path"))
        print(f"[E0] Extracted {count} figure image(s) to {figures_dir}/")
    except Exception as e:
        print(f"[E0] WARN: Figure image extraction failed: {e}")
        print("     Figures will have captions only. Install pdfplumber + Pillow for image extraction.")


def extract_with_pypdf2(pdf_path: str) -> dict:
    """Fallback extraction using PyPDF2 (no image support)."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        return None
    
    reader = PdfReader(pdf_path)
    full_text = []
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text.append(f"<!-- PAGE {i+1} -->\n{text}")
    
    raw = "\n\n".join(full_text)
    
    return {
        "raw": raw,
        "metadata": {"title": "", "authors": [], "abstract": ""},
        "figures": [],
        "references": [],
    }


def detect_sections(text: str) -> str:
    """Add markdown section headers based on common paper section patterns."""
    section_patterns = [
        (r'(?i)(?<=\n)(\d+\.?\s*)?(Introduction)\s*\n', '## '),
        (r'(?i)(?<=\n)(\d+\.?\s*)?(Related Work|Background)\s*\n', '## '),
        (r'(?i)(?<=\n)(\d+\.?\s*)?(Method|Approach|Design|Architecture)\s*\n', '## '),
        (r'(?i)(?<=\n)(\d+\.?\s*)?(Experiment|Evaluation|Results)\s*\n', '## '),
        (r'(?i)(?<=\n)(\d+\.?\s*)?(Discussion|Analysis)\s*\n', '## '),
        (r'(?i)(?<=\n)(\d+\.?\s*)?(Conclusion|Summary)\s*\n', '## '),
        (r'(?i)(?<=\n)(\d+\.?\s*)?(References|Bibliography)\s*\n', '## '),
    ]
    
    result = text
    for pattern, prefix in section_patterns:
        result = re.sub(pattern, lambda m: f"\n{prefix}{m.group(0).strip()}\n", result)
    
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract-pdf.py <paper.pdf> [--output <dir>]")
        print("  --output <dir>   Top-level output dir (default: output)")
        print("                   Creates <dir>/analysis/ and <dir>/results/")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_base = "output"
    
    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            output_base = sys.argv[i + 1]
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found: {pdf_path}")
        sys.exit(1)
    
    print(f"[E0] Extracting: {pdf_path}")
    
    # Create output directories
    analysis_dir = os.path.join(output_base, "analysis")
    results_dir = os.path.join(output_base, "results")
    os.makedirs(analysis_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    # Try pdfplumber first, fall back to PyPDF2
    result = extract_with_pdfplumber(pdf_path, output_base)
    if result is None:
        print("[E0] pdfplumber not available, trying PyPDF2...")
        result = extract_with_pypdf2(pdf_path)
    
    if result is None:
        print("ERROR: Install PyPDF2 or pdfplumber: pip install PyPDF2 pdfplumber Pillow")
        sys.exit(1)
    
    # Write outputs to analysis/
    structured_text = detect_sections(result["raw"])
    
    with open(os.path.join(analysis_dir, "full-text.md"), "w", encoding="utf-8") as f:
        f.write(f"# Extracted Text\n\n{structured_text}")
    
    with open(os.path.join(analysis_dir, "figures.md"), "w", encoding="utf-8") as f:
        f.write("# Figures & Tables\n\n")
        for fig in result["figures"]:
            img_ref = f" ![fig-{fig['number'].zfill(2)}](figures/fig-{fig['number'].zfill(2)}.png)" if fig.get("image_path") else ""
            f.write(f"### {fig['type'].capitalize()} {fig['number']} (Page {fig.get('page', '?')}){img_ref}\n\n")
            f.write(f"**Caption:** {fig['caption']}\n\n")
            if fig.get("context"):
                f.write(f"<details>\n<summary>Surrounding context</summary>\n\n{fig['context']}\n\n</details>\n\n")
            f.write("---\n\n")
    
    with open(os.path.join(analysis_dir, "references.md"), "w", encoding="utf-8") as f:
        f.write("# References\n\n")
        for i, ref in enumerate(result["references"], 1):
            f.write(f"{i}. {ref}\n\n")
    
    with open(os.path.join(analysis_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(result["metadata"], f, indent=2)
    
    # Count stats
    section_count = structured_text.count("\n## ")
    word_count = len(structured_text.split())
    fig_count = len([f for f in result["figures"] if f["type"] == "figure"])
    tab_count = len([f for f in result["figures"] if f["type"] == "table"])
    img_count = len([f for f in result["figures"] if f.get("image_path")])
    
    print(f"[E0] Done. Output: {output_base}/")
    print(f"     analysis/full-text.md   — {word_count} words, ~{section_count} sections")
    print(f"     analysis/figures.md     — {fig_count} figures + {tab_count} tables")
    if img_count:
        print(f"     analysis/figures/       — {img_count} extracted image(s)")
    else:
        print(f"     analysis/figures/       — (no images extracted — install Pillow)")
    print(f"     analysis/references.md  — {len(result['references'])} references")
    print(f"     analysis/metadata.json  — title, abstract")
    print(f"     results/                — (ready for E1 decomposition)")
    print(f"\n[E1 ready] Run paper-extract E1 decomposition on {analysis_dir}/full-text.md")


if __name__ == "__main__":
    main()

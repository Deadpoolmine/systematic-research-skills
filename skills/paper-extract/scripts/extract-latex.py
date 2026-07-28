#!/usr/bin/env python3
"""
LaTeX Paper Extractor — parse structured content from LaTeX sources.

Usage:
    python extract-latex.py <main.tex> [--output <dir>]
    
Output directory structure:
    <output>/
      analysis/
        full-text.md        Extracted text with section structure
        figures.md           Figure/table captions with includegraphics paths and context
        references.md        Parsed \\cite commands and bibliography
        metadata.json        Title, authors, abstract
        structure.json       Section tree
      results/               (created empty, ready for E1 output)

Dependencies: none (stdlib only)
"""

import sys
import os
import json
import re
from pathlib import Path


def read_tex_file(filepath: str) -> str:
    """Read .tex file, handling \\input and \\include directives."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    
    base_dir = os.path.dirname(os.path.abspath(filepath))
    
    # Resolve \input{...} and \include{...}
    def resolve_input(match):
        filename = match.group(1).strip()
        for ext in [".tex", ""]:
            candidate = os.path.join(base_dir, filename + ext)
            if os.path.exists(candidate):
                return read_tex_file(candidate)
        print(f"  [WARN] Could not resolve: {filename}")
        return f"% [UNRESOLVED: {filename}]"
    
    content = re.sub(r'\\(?:input|include)\{([^}]+)\}', resolve_input, content)
    
    return content


def strip_comments(text: str) -> str:
    """Remove LaTeX comments (lines starting with %, but not \%)."""
    lines = []
    for line in text.split("\n"):
        stripped = re.sub(r'(?<!\\)%.*$', '', line)
        if stripped.strip():
            lines.append(stripped)
    return "\n".join(lines)


def strip_commands(text: str) -> str:
    """Remove common LaTeX formatting commands, keep text content."""
    text = re.sub(r'\\(?:begin|end)\{[^}]+\}', '', text)
    text = re.sub(r'\\(?:cite|ref|label|autoref|Cref|cref)\{[^}]+\}', '', text)
    text = re.sub(r'\\(?:textbf|textit|texttt|textsf|textsc|emph)\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\(?:section|subsection|subsubsection)\*?\{([^}]+)\}', r'\n## \1\n', text)
    text = re.sub(r'\\[a-zA-Z]+\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'\$[^$]+\$', '[math]', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text


def extract_metadata(content: str) -> dict:
    """Extract title, author, abstract from LaTeX."""
    metadata = {"title": "", "authors": [], "abstract": ""}
    
    title_match = re.search(r'\\title\{((?:[^{}]|\{[^{}]*\})*)\}', content, re.DOTALL)
    if title_match:
        metadata["title"] = strip_commands(title_match.group(1)).strip()
    
    author_match = re.search(r'\\author\{((?:[^{}]|\{[^{}]*\})*)\}', content, re.DOTALL)
    if author_match:
        author_text = strip_commands(author_match.group(1)).strip()
        metadata["authors"] = [a.strip() for a in re.split(r'(?:\\and|,)\s*', author_text) if a.strip()]
    
    abs_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
    if abs_match:
        metadata["abstract"] = strip_commands(abs_match.group(1)).strip()
    
    return metadata


def extract_sections(content: str) -> list:
    """Extract section hierarchy."""
    sections = []
    section_pattern = re.compile(
        r'\\(section|subsection|subsubsection)\*?\{((?:[^{}]|\{[^{}]*\})*)\}',
        re.DOTALL
    )
    
    for match in section_pattern.finditer(content):
        level = match.group(1)
        title = strip_commands(match.group(2)).strip()
        depth = {"section": 1, "subsection": 2, "subsubsection": 3}.get(level, 1)
        sections.append({"depth": depth, "title": title, "level": level})
    
    return sections


def extract_figures(content: str) -> list:
    """Extract figure/table captions with includegraphics paths and context."""
    captions = []
    
    # ---- Figure extraction with context ----
    fig_env_pattern = re.compile(
        r'\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}',
        re.DOTALL
    )
    
    for i, match in enumerate(fig_env_pattern.finditer(content), 1):
        env_content = match.group(1)
        env_start = match.start()
        env_end = match.end()
        
        # Extract caption
        cap_match = re.search(
            r'\\caption\{((?:[^{}]|\{[^{}]*\})*)\}',
            env_content, re.DOTALL
        )
        caption = strip_commands(cap_match.group(1)).strip() if cap_match else "[NO CAPTION]"
        
        # Extract includegraphics paths
        img_paths = re.findall(
            r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}',
            env_content
        )
        
        # Extract surrounding context (2-3 paragraphs before and after the figure)
        context_before = content[max(0, env_start - 1500):env_start].strip()
        # Get last 2-3 paragraphs of context_before
        para_splits = re.split(r'\n\s*\n', context_before)
        context_before_trimmed = '\n\n'.join(para_splits[-3:]) if len(para_splits) > 3 else context_before
        
        context_after = content[env_end:min(len(content), env_end + 1500)].strip()
        para_splits = re.split(r'\n\s*\n', context_after)
        context_after_trimmed = '\n\n'.join(para_splits[:3]) if len(para_splits) > 3 else context_after
        
        surrounding = (context_before_trimmed + '\n\n[FIGURE HERE]\n\n' + context_after_trimmed).strip()
        
        captions.append({
            "type": "figure",
            "number": str(i),
            "caption": caption,
            "image_paths": img_paths,
            "context": strip_commands(surrounding)[:2000]
        })
    
    # ---- Table extraction with context ----
    tab_env_pattern = re.compile(
        r'\\begin\{table\*?\}(.*?)\\end\{table\*?\}',
        re.DOTALL
    )
    
    for i, match in enumerate(tab_env_pattern.finditer(content), 1):
        env_content = match.group(1)
        env_start = match.start()
        env_end = match.end()
        
        cap_match = re.search(
            r'\\caption\{((?:[^{}]|\{[^{}]*\})*)\}',
            env_content, re.DOTALL
        )
        caption = strip_commands(cap_match.group(1)).strip() if cap_match else "[NO CAPTION]"
        
        context_before = content[max(0, env_start - 800):env_start].strip()
        context_after = content[env_end:min(len(content), env_end + 800)].strip()
        surrounding = (context_before + '\n\n[TABLE HERE]\n\n' + context_after).strip()
        
        captions.append({
            "type": "table",
            "number": str(i),
            "caption": caption,
            "image_paths": [],
            "context": strip_commands(surrounding)[:1000]
        })
    
    return captions


def extract_citations(content: str) -> list:
    """Extract all \\cite commands."""
    cites = set()
    cite_pattern = re.compile(r'\\(?:cite|citep|citet)\{([^}]+)\}')
    for match in cite_pattern.finditer(content):
        for key in match.group(1).split(","):
            cites.add(key.strip())
    return sorted(cites)


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract-latex.py <main.tex> [--output <dir>]")
        print("  --output <dir>   Top-level output dir (default: output)")
        print("                   Creates <dir>/analysis/ and <dir>/results/")
        sys.exit(1)
    
    tex_path = sys.argv[1]
    output_base = "output"
    
    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            output_base = sys.argv[i + 1]
    
    if not os.path.exists(tex_path):
        print(f"ERROR: File not found: {tex_path}")
        sys.exit(1)
    
    print(f"[E0] Extracting: {tex_path}")
    
    # Read and resolve
    content = read_tex_file(tex_path)
    print(f"  Resolved source: {len(content)} chars")
    
    # Strip comments
    content = strip_comments(content)
    
    # Extract components
    metadata = extract_metadata(content)
    sections = extract_sections(content)
    figures = extract_figures(content)
    citations = extract_citations(content)
    
    # Strip commands for readable text
    clean_text = strip_commands(content)
    
    # Create output directories
    analysis_dir = os.path.join(output_base, "analysis")
    results_dir = os.path.join(output_base, "results")
    os.makedirs(analysis_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    with open(os.path.join(analysis_dir, "full-text.md"), "w", encoding="utf-8") as f:
        f.write(f"# {metadata['title']}\n\n")
        if metadata["authors"]:
            f.write(f"**Authors:** {', '.join(metadata['authors'])}\n\n")
        if metadata["abstract"]:
            f.write(f"## Abstract\n\n{metadata['abstract']}\n\n")
        f.write(clean_text)
    
    with open(os.path.join(analysis_dir, "figures.md"), "w", encoding="utf-8") as f:
        f.write("# Figures & Tables\n\n")
        for fig in figures:
            img_info = ""
            if fig.get("image_paths"):
                img_info = f"\n**Source files:** {', '.join(fig['image_paths'])}"
            f.write(f"### {fig['type'].capitalize()} {fig['number']}{img_info}\n\n")
            f.write(f"**Caption:** {fig['caption']}\n\n")
            if fig.get("context"):
                f.write(f"<details>\n<summary>Surrounding context</summary>\n\n{fig['context']}\n\n</details>\n\n")
            f.write("---\n\n")
    
    with open(os.path.join(analysis_dir, "references.md"), "w", encoding="utf-8") as f:
        f.write("# Citations\n\n")
        for cite in citations:
            f.write(f"- `{cite}`\n")
    
    with open(os.path.join(analysis_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    
    with open(os.path.join(analysis_dir, "structure.json"), "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2)
    
    print(f"[E0] Done. Output: {output_base}/")
    print(f"     analysis/full-text.md    — cleaned text")
    print(f"     analysis/figures.md      — {len(figures)} figures/tables with context")
    print(f"     analysis/references.md   — {len(citations)} citation keys")
    print(f"     analysis/metadata.json   — title, {len(metadata['authors'])} authors, abstract")
    print(f"     analysis/structure.json  — {len(sections)} sections")
    print(f"     results/                 — (ready for E1 decomposition)")
    print(f"\n[E1 ready] Run paper-extract E1 decomposition on {analysis_dir}/full-text.md")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()

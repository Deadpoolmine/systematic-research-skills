# HLS Mapping for Research

**Load when:** executing R1 (L0) or R2 (L1) decomposition.

## Level Mapping

| HLS Level | File | Research Equivalent | Question |
|-----------|------|--------------------|----------|
| **TLDR** | `tldr.md` | Condensed summary | What's the essence? |
| **L0** | `l0.md` | Section-level claims | What does each section say? |
| **L1** | `l1.md` | Paragraph flow | How does each section build its argument? |
| **BibEntry** | `bibentry.bib` | BibTeX citation | How to cite this source? |

All files live in the same item folder: `knowledge/<category>/<subcategory>/<item>/`.

## TLDR (`tldr.md`)

Template → [templates/tldr.md](../templates/tldr.md).

```markdown
# TLDR

**Source:** [title], [date], via [source-type]

## Overview
(1) [1-2 sentences — what is this about?]
(2) [1-2 sentences — what is the key takeaway?]

## Key Claims
(1) [Main claim 1]
(2) [Main claim 2]
(3) [Main claim 3 — 2-5 total]

## Implications
(1) [What this means / why it matters]
```

## L0: Section Summary (`l0.md`)

Template → [templates/l0.md](../templates/l0.md).

For each major section in the source:

```markdown
## Section: <name>
[1-2 sentence summary of what this section says — descriptive, not evaluative]
Evidence: [quote or paragraph reference]
```

## L1: Paragraph Flow (`l1.md`)

Template → [templates/l1.md](../templates/l1.md).

For each section, trace the argument chain:

```markdown
## Section: <name> — Flow

Purpose: [why this section exists in the argument]

| Unit | Paragraphs | What it says | Role |
|------|-----------|-------------|------|
| A | ¶1-2 | [summary] | Setup/Context |
| B | ¶3-5 | [summary] | Argument/Counter |
| C | ¶6-7 | [summary] | Resolution/Transition |
```

A paragraph unit is 1-3 consecutive paragraphs that form a logical group.
